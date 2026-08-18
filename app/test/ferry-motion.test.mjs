// Regression lock for the live ferry motion rules (app/src/ferry-motion.js).
//
// The headline test here is the freeze bug: the browser polls /api/ferries
// every 60 s, the server caches for 90 s, so a large share of polls hand back a
// byte-identical payload. Reading that repeat as "the boat did not move" set
// speed to 0, switched dead reckoning off and froze the vessel mid-Bay. That is
// the same class of bug muni-motion.js was created for, and it is pinned here
// so it cannot come back through an unrelated pass over ferries.js.
//
// A failure means a fix is being reverted — fix the code, not the expectation.
//
// Run: cd app && npm test

import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
  DEAD_RECKON_MAX_S,
  WORST_FRESH_FIX_GAP_S,
  DWELL_STEP_M,
  IDLE_SPEED,
  MAX_SPEED,
  MISSES_TO_DROP,
  MOVING_M,
  STALE_MS,
  bearingToYaw,
  deadReckonRun,
  deadReckonSeconds,
  headingFor,
  isFreshFix,
  shouldDrop,
  shouldRender,
  targetSpeedFor,
  usableBearing,
} from '../src/ferry-motion.js';

const SEC = 1000;

describe('invariant 4 — liveness and freshness are different clocks', () => {
  it('treats a repeated snapshot as not fresh', () => {
    // THE BUG. 511 stamps the whole fleet with one recordedAt per snapshot; our
    // 60 s poll against a 90 s cache guarantees we see the same one repeatedly.
    assert.equal(isFreshFix(1787006780000, 1787006780000), false);
  });

  it('treats an advanced snapshot as fresh', () => {
    assert.equal(isFreshFix(1787006780000, 1787006893000), true);
  });

  it('assumes fresh when the feed publishes no timestamp', () => {
    // Unknown must never read as stale: that is the freeze bug by another door.
    assert.equal(isFreshFix(1787006780000, null), true);
    assert.equal(isFreshFix(null, 1787006780000), true);
    assert.equal(isFreshFix(null, null), true);
  });

  it('keeps extrapolating a boat whose fix is old but whose polls are current', () => {
    // A vessel seen in three repeated payloads has a current lastFixAt and a
    // 75 s old lastFreshFixAt. It must still be running, not frozen.
    const now = 1_000_000;
    const since = deadReckonSeconds({ now, lastFreshFixAt: now - 75 * SEC });
    assert.equal(since, 75);
    assert.ok(deadReckonRun({ speed: 9, sinceFreshS: since }) > 0);
  });

  it('does not let a repeat reset the dead-reckon clock', () => {
    // Measuring from the last POLL rather than the last FRESH fix is what made
    // a 90 s old fix look brand new, so the boat under-ran its own course.
    const now = 1_000_000;
    const fromPoll = deadReckonSeconds({ now, lastFreshFixAt: now - 1 * SEC });
    const fromFresh = deadReckonSeconds({ now, lastFreshFixAt: now - 80 * SEC });
    assert.ok(fromFresh > fromPoll, 'the fresh-fix clock must be the older one');
  });

  it('extrapolates far enough to cover the worst wait for a new fix', () => {
    // The regression this pins: a cap SHORTER than the gap between fresh fixes
    // stalls every moving boat once per cycle, which looks exactly like the
    // freeze bug this module exists to prevent.
    assert.ok(
      DEAD_RECKON_MAX_S >= WORST_FRESH_FIX_GAP_S,
      `cap ${DEAD_RECKON_MAX_S}s must cover the ${WORST_FRESH_FIX_GAP_S}s worst-case fix gap`
    );
    const now = 1_000_000;
    // A boat two minutes past its last fresh fix is still running.
    const since = deadReckonSeconds({ now, lastFreshFixAt: now - 120 * SEC });
    assert.equal(since, 120);
    assert.ok(deadReckonRun({ speed: 9, sinceFreshS: since }) > 0);
  });

  it('stops extrapolating once the fix is beyond the cap', () => {
    const now = 1_000_000;
    const since = deadReckonSeconds({ now, lastFreshFixAt: now - 10 * 60 * SEC });
    assert.equal(since, DEAD_RECKON_MAX_S);
  });

  it('counts a vessel present while repeats keep mentioning it', () => {
    // Repeats bump lastFixAt, so tenure survives even though nothing moved.
    const now = 1_000_000;
    assert.equal(shouldDrop({ misses: 0, lastFixAt: now }, now), false);
  });
});

describe('invariants 1 and 2 — dwell is displacement, measured fix to fresh fix', () => {
  it('gives a boat that crossed open water a real speed', () => {
    const speed = targetSpeedFor({ fixStep: 900, gapSeconds: 90 });
    assert.ok(Math.abs(speed - 10) < 0.001);
  });

  it('treats drift at a berth as lying still', () => {
    assert.equal(targetSpeedFor({ fixStep: DWELL_STEP_M - 0.1, gapSeconds: 90 }), 0);
    assert.ok(targetSpeedFor({ fixStep: DWELL_STEP_M, gapSeconds: 90 }) > 0);
  });

  it('never exceeds the hull speed cap', () => {
    assert.equal(targetSpeedFor({ fixStep: 50_000, gapSeconds: 60 }), MAX_SPEED);
  });

  it('never returns a negative or NaN speed', () => {
    assert.equal(targetSpeedFor({ fixStep: 0, gapSeconds: 90 }), 0);
    assert.equal(targetSpeedFor({ fixStep: NaN, gapSeconds: 90 }), 0);
    assert.equal(targetSpeedFor({ fixStep: 900, gapSeconds: 0 }), MAX_SPEED);
  });
});

describe('invariant 3 — a vessel keeps moving between fixes', () => {
  it('runs a moving boat forward', () => {
    assert.ok(deadReckonRun({ speed: 10, sinceFreshS: 30 }) === 300);
  });

  it('does not creep a berthed boat', () => {
    assert.equal(deadReckonRun({ speed: IDLE_SPEED, sinceFreshS: 60 }), 0);
    assert.equal(deadReckonRun({ speed: 0, sinceFreshS: 60 }), 0);
  });
});

describe('heading', () => {
  it('reads an exact bearing of 0 as unknown', () => {
    // The SB feed sends 0 for every vessel it has no heading for.
    assert.equal(usableBearing(0), false);
    assert.equal(usableBearing(null), false);
    assert.equal(usableBearing(360), true);
    assert.equal(usableBearing(90), true);
  });

  it('maps compass bearings to scene yaw', () => {
    // Compared by magnitude: negating zero yields -0, which is a perfectly good
    // yaw but is not strict-equal to 0.
    assert.ok(Math.abs(bearingToYaw(0)) < 1e-9);
    assert.ok(Math.abs(bearingToYaw(90) + Math.PI / 2) < 1e-9);
  });

  it('prefers a published bearing', () => {
    const yaw = headingFor({ bearingDeg: 90, speed: 8, dx: 0, dz: -100 });
    assert.ok(Math.abs(yaw + Math.PI / 2) < 1e-9);
  });

  it('derives heading from motion when the bearing is unusable', () => {
    // Moving north in scene space is -z, which is yaw 0.
    const yaw = headingFor({ bearingDeg: 0, speed: 8, dx: 0, dz: -100 });
    assert.ok(Math.abs(yaw) < 1e-9);
  });

  it('holds the heading of a berthed boat with no bearing', () => {
    // null means "keep what you had" — a docked boat must not spin on the spot.
    assert.equal(headingFor({ bearingDeg: 0, speed: 0.1, dx: 0.3, dz: 0.2 }), null);
  });
});

describe('scene tenure', () => {
  it('drops a vessel the feed has stopped reporting', () => {
    const now = 1_000_000;
    assert.equal(shouldDrop({ misses: MISSES_TO_DROP, lastFixAt: now }, now), true);
    assert.equal(shouldDrop({ misses: 0, lastFixAt: now - STALE_MS - 1 }, now), true);
  });

  it('survives a single truncated response', () => {
    const now = 1_000_000;
    assert.equal(shouldDrop({ misses: 1, lastFixAt: now }, now), false);
  });

  it('draws an in-service vessel that is inside the scene', () => {
    const now = 1_000_000;
    const drawn = shouldRender({ lastFixAt: now, inService: true, moved: 0, inScene: true }, now);
    assert.equal(drawn, true);
  });

  it('draws an out-of-service boat only when it is actually going somewhere', () => {
    const now = 1_000_000;
    const base = { lastFixAt: now, inService: false, inScene: true };
    assert.equal(shouldRender({ ...base, moved: MOVING_M - 1 }, now), false);
    assert.equal(shouldRender({ ...base, moved: MOVING_M + 1 }, now), true);
  });

  it('never draws a vessel outside the water plane', () => {
    const now = 1_000_000;
    // Vallejo is ~36 km north; the water plane is 30 km across.
    const drawn = shouldRender({ lastFixAt: now, inService: true, moved: 900, inScene: false }, now);
    assert.equal(drawn, false);
  });

  it('never draws a vessel whose last fix has gone stale', () => {
    const now = 1_000_000;
    const drawn = shouldRender(
      { lastFixAt: now - STALE_MS - 1, inService: true, moved: 900, inScene: true },
      now
    );
    assert.equal(drawn, false);
  });
});
