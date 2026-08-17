// Regression lock for the live Muni motion rules (app/src/muni-motion.js).
//
// Every test here is a bug the deployed city has already shipped at least once:
// frozen buses, buses evicted from the scene mid-service, parked coaches
// cluttering the streets. The fixes kept being undone by later passes through
// muni.js, so they are pinned here. A failure means a fix is being reverted —
// do not adjust the expectation, fix the code.
//
// Run: cd app && npm test

import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
  DEAD_RECKON_MAX_S,
  DWELL_STEP_M,
  LAYOVER_LEAD_MS,
  MAX_SPEED,
  MISSES_TO_DROP,
  PARK_HIDE_MS,
  PROVISIONAL_SPEED,
  STALE_MS,
  STILL_MS,
  deadReckonAdvance,
  dormantReason,
  inService,
  seedSpeed,
  shouldDrop,
  targetSpeedFor,
} from '../src/muni-motion.js';

const MIN = 60 * 1000;

describe('invariant 1 — dwell is displacement, never the reported speed', () => {
  it('keeps a vehicle moving that covered ground while reporting speed 0', () => {
    // 9e9accd8: GTFS-RT samples speed instantaneously and 260 of 507 vehicles
    // read exactly 0 at any instant. Trusting it froze half the fleet.
    const speed = targetSpeedFor({ fixStep: 900, gapSeconds: 90, gapS: 900, reported: 0, onShape: true });
    assert.ok(speed > 0, 'a vehicle that moved 900 m must not be treated as dwelling');
    assert.ok(Math.abs(speed - 10) < 0.001);
  });

  it('stops a vehicle that did not move even when it reports a healthy speed', () => {
    const speed = targetSpeedFor({ fixStep: 2, gapSeconds: 90, gapS: 0, reported: 9, onShape: true });
    assert.equal(speed, 0, 'stopped must read as stopped');
  });

  it('treats displacement under one bus length as standing still', () => {
    assert.equal(targetSpeedFor({ fixStep: DWELL_STEP_M - 0.1, gapSeconds: 60, onShape: true }), 0);
    assert.ok(targetSpeedFor({ fixStep: DWELL_STEP_M, gapSeconds: 60, onShape: true }) > 0);
  });

  it('never exceeds the transit speed cap', () => {
    const speed = targetSpeedFor({ fixStep: 5000, gapSeconds: 60, gapS: 5000, reported: 90, onShape: true });
    assert.equal(speed, MAX_SPEED);
  });

  it('applies the same displacement rule off-shape', () => {
    assert.equal(targetSpeedFor({ fixStep: 3, gapSeconds: 60, reported: 12, onShape: false }), 0);
    assert.ok(targetSpeedFor({ fixStep: 600, gapSeconds: 60, onShape: false }) > 0);
  });
});

describe('invariant 2 — dwell is measured fix to fix, not against the target', () => {
  it('keeps a moving vehicle moving when dead-reckon overshot its new target', () => {
    // 73bb2a96: dead-reckon drives the bus past the target, so gapS goes
    // negative on a bus that plainly moved — reading gapS froze it for a
    // whole poll cycle.
    const speed = targetSpeedFor({ fixStep: 900, gapSeconds: 90, gapS: -40, reported: null, onShape: true });
    assert.ok(speed > 0, 'a negative gap to the target is not evidence of dwelling');
  });

  it('uses the gap to the target only to catch up, never to stop', () => {
    const behind = targetSpeedFor({ fixStep: 200, gapSeconds: 60, gapS: 900, onShape: true });
    const level = targetSpeedFor({ fixStep: 200, gapSeconds: 60, gapS: 0, onShape: true });
    assert.ok(behind > level, 'a vehicle behind its fix must speed up to catch up');
  });
});

describe('invariant 3 — vehicles keep moving between fixes', () => {
  const base = {
    lead: 0,
    targetSpeed: 8,
    sinceFreshS: 30,
    provisional: false,
    targetS: 100,
    provisionalCap: Infinity,
    dt: 0.5,
  };

  it('extrapolates a moving vehicle that has caught up with its target', () => {
    // 10b388aa: the client polls every 60 s against a 90 s server TTL, so
    // every other payload is identical. Without extrapolation the bus reaches
    // targetS and freezes there.
    assert.equal(deadReckonAdvance(base), 4);
  });

  it('never extrapolates a genuinely dwelling vehicle', () => {
    assert.equal(deadReckonAdvance({ ...base, targetSpeed: 0 }), 0);
  });

  it('does not extrapolate while the vehicle still has real ground to cover', () => {
    assert.equal(deadReckonAdvance({ ...base, lead: DWELL_STEP_M + 1 }), 0);
  });

  it('gives up after the dead-reckon window instead of inventing a route', () => {
    assert.ok(deadReckonAdvance({ ...base, sinceFreshS: DEAD_RECKON_MAX_S - 1 }) > 0);
    assert.equal(deadReckonAdvance({ ...base, sinceFreshS: DEAD_RECKON_MAX_S }), 0);
  });

  it('limits a first-fix guess to its provisional lead', () => {
    assert.ok(deadReckonAdvance({ ...base, provisional: true, targetS: 100, provisionalCap: 150 }) > 0);
    assert.equal(deadReckonAdvance({ ...base, provisional: true, targetS: 150, provisionalCap: 150 }), 0);
  });

  it('starts a newly sighted in-service vehicle rolling rather than parked', () => {
    const now = Date.now();
    const working = { speedMs: 0, stops: [{ arrivalAt: now + MIN }] };
    assert.equal(seedSpeed(working, now, true), PROVISIONAL_SPEED);
    assert.equal(seedSpeed({ speedMs: 7, stops: [] }, now, true), 7);
  });
});

describe('invariant 4 — liveness (lastFixAt) and freshness (lastFreshFixAt) are different clocks', () => {
  const now = Date.now();

  it('keeps a vehicle that stale polls keep reporting', () => {
    // 5f0ea041: stale payloads stopped bumping lastFixAt, so in degraded mode
    // the entire fleet was evicted every 3 minutes and became unclickable.
    const state = { misses: 0, lastFixAt: now, lastFreshFixAt: now - 8 * MIN };
    assert.equal(shouldDrop(state, now), false);
  });

  it('drops a vehicle the feed has stopped reporting', () => {
    assert.equal(shouldDrop({ misses: MISSES_TO_DROP, lastFixAt: now }, now), true);
    assert.equal(shouldDrop({ misses: 0, lastFixAt: now - STALE_MS - 1 }, now), true);
  });

  it('measures dormancy in fix time, so stale data cannot empty the city', () => {
    // Moving vehicle whose last fresh fix is old because the feed went stale:
    // it moved right up to that fix, so it is not parked.
    const state = {
      lastFreshFixAt: now - 10 * MIN,
      movedAt: now - 10 * MIN,
      stops: [{ arrivalAt: now }],
    };
    assert.equal(dormantReason(state, true), null);
  });
});

describe('removal — only what the data says is out of service leaves the scene', () => {
  const now = Date.now();

  it('hides a vehicle that has not moved for the park window', () => {
    const state = { lastFreshFixAt: now, movedAt: now - PARK_HIDE_MS - 1, stops: [] };
    assert.equal(dormantReason(state, true), 'parked');
  });

  it('hides a standing vehicle whose run has not started yet', () => {
    const state = {
      lastFreshFixAt: now,
      movedAt: now - STILL_MS - 1,
      stops: [{ arrivalAt: now + LAYOVER_LEAD_MS + MIN }],
    };
    assert.equal(dormantReason(state, true), 'layover');
  });

  it('keeps a standing vehicle that is about to serve its next stop', () => {
    const state = {
      lastFreshFixAt: now,
      movedAt: now - STILL_MS - 1,
      stops: [{ arrivalAt: now + MIN }],
    };
    assert.equal(dormantReason(state, true), null, 'a bus at a red light is still in service');
  });

  it('assumes a vehicle is working when the feed publishes no predictions at all', () => {
    // Degraded mode (positions-only poll): nobody has stops, so absence of
    // predictions is not evidence of a layover.
    assert.equal(inService([], now, false), true);
    assert.equal(inService([], now, true), false);
  });
});
