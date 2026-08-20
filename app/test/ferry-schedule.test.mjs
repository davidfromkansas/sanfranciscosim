// Lock for timetable playback (app/src/ferryschedule.js).
//
// These are the parts that are easy to get subtly wrong and hard to see wrong
// on screen: which services run on a given day, and where a boat sits partway
// through a leg — including the sailing published as "24:40" that belongs to
// yesterday's service day.
//
// Run: cd app && npm test

import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import { activeServices, localDay, metresAt, sailingsAt, serviceRuns } from '../src/ferryschedule.js';

// 2026-08-19 is a Wednesday; 2026-08-22 a Saturday. Noon avoids any DST edge.
const WED_NOON = Date.parse('2026-08-19T12:00:00-07:00');
const SAT_NOON = Date.parse('2026-08-22T12:00:00-07:00');

const WEEKDAY_SVC = { days: [1, 1, 1, 1, 1, 0, 0], start: 20260101, end: 20261231 };
const WEEKEND_SVC = { days: [0, 0, 0, 0, 0, 1, 1], start: 20260101, end: 20261231 };

// A local-midnight helper standing in for astro's, so the test does not depend
// on the app's clock module.
const localDayStart = (ms) => Date.parse(`${new Intl.DateTimeFormat('en-CA', {
  timeZone: 'America/Los_Angeles', year: 'numeric', month: '2-digit', day: '2-digit',
}).format(new Date(ms))}T00:00:00-07:00`);

describe('which day it is, locally', () => {
  it('reads the local date and weekday', () => {
    assert.deepEqual(localDay(WED_NOON), { ymd: 20260819, weekday: 2 });
    assert.deepEqual(localDay(SAT_NOON), { ymd: 20260822, weekday: 5 });
  });

  it('uses SF local time, not the machine or UTC', () => {
    // 00:30 UTC on the 20th is still the evening of the 19th in California.
    assert.equal(localDay(Date.parse('2026-08-20T00:30:00Z')).ymd, 20260819);
  });
});

describe('which services run', () => {
  it('runs a weekday service on a weekday only', () => {
    assert.equal(serviceRuns(WEEKDAY_SVC, localDay(WED_NOON)), true);
    assert.equal(serviceRuns(WEEKDAY_SVC, localDay(SAT_NOON)), false);
    assert.equal(serviceRuns(WEEKEND_SVC, localDay(SAT_NOON)), true);
  });

  it('ignores a service outside its date window', () => {
    const expired = { ...WEEKDAY_SVC, start: 20240101, end: 20241231 };
    assert.equal(serviceRuns(expired, localDay(WED_NOON)), false);
  });

  it('lets a calendar_dates exception add a day', () => {
    const holiday = { ...WEEKEND_SVC, added: [20260819] };
    assert.equal(serviceRuns(holiday, localDay(WED_NOON)), true);
  });

  it('lets a calendar_dates exception remove a day, and removal wins', () => {
    const cancelled = { ...WEEKDAY_SVC, added: [20260819], removed: [20260819] };
    assert.equal(serviceRuns(cancelled, localDay(WED_NOON)), false);
  });

  it('collects the active set', () => {
    const set = activeServices({ wd: WEEKDAY_SVC, we: WEEKEND_SVC }, localDay(WED_NOON));
    assert.deepEqual([...set], ['wd']);
  });
});

describe('where the boat is', () => {
  // Leaves at 10:00 (36000 s) from metre 0, arrives 10:30 at metre 6000.
  const trip = { legs: [[36000, 0], [37800, 6000]] };

  it('is nowhere before it sails or after it lands', () => {
    assert.equal(metresAt(trip, 35999), null);
    assert.equal(metresAt(trip, 37801), null);
  });

  it('is at the berth at departure and arrival', () => {
    assert.equal(metresAt(trip, 36000), 0);
    assert.equal(metresAt(trip, 37800), 6000);
  });

  it('is halfway along at the halfway time', () => {
    assert.equal(metresAt(trip, 36900), 3000);
  });

  it('places a three-stop run by its own leg times, not by overall fraction', () => {
    // Calls at metre 1000 after only a quarter of the elapsed time — a boat
    // assumed to be halfway at the halfway time would be far out here.
    const triangle = { legs: [[36000, 0], [36450, 1000], [37800, 6000]] };
    assert.equal(metresAt(triangle, 36450), 1000);
    const mid = metresAt(triangle, 37125);
    assert.ok(mid > 3000 && mid < 4000, `expected the long leg to dominate, got ${mid}`);
  });

  it('holds position through a dwell rather than dividing by zero', () => {
    const dwell = { legs: [[36000, 0], [36000, 0], [37800, 6000]] };
    assert.equal(Number.isFinite(metresAt(dwell, 36000)), true);
  });

  it('ignores a malformed trip', () => {
    assert.equal(metresAt({ legs: [] }, 36000), null);
    assert.equal(metresAt(null, 36000), null);
  });
});

describe('sailings under way right now', () => {
  const schedule = {
    services: { wd: WEEKDAY_SVC, we: WEEKEND_SVC },
    trips: [
      { service: 'wd', route: 'GF:SSSF', shape: 0, legs: [[43200, 0], [45000, 6000]] }, // 12:00-12:30
      { service: 'we', route: 'GF:TBSF', shape: 1, legs: [[43200, 0], [45000, 6000]] },
      { service: 'wd', route: 'GF:LSSF', shape: 2, legs: [[3600, 0], [5400, 6000]] },   // 01:00-01:30
    ],
  };

  it('returns only the trips actually under way, on the right day', () => {
    const out = sailingsAt(schedule, WED_NOON, localDayStart);
    assert.equal(out.length, 1);
    assert.equal(out[0].trip.route, 'GF:SSSF');
    assert.equal(out[0].metres, 0);
  });

  it('runs the weekend service on a Saturday instead', () => {
    const out = sailingsAt(schedule, SAT_NOON, localDayStart);
    assert.equal(out.length, 1);
    assert.equal(out[0].trip.route, 'GF:TBSF');
  });

  it('finds a sailing published past 24:00 on yesterday\'s service day', () => {
    // 00:20 Thursday. A trip published as 24:00-24:30 on WEDNESDAY's service is
    // under way; forgetting yesterday's timetable makes the Bay empty at night.
    const late = { services: { wd: WEEKDAY_SVC }, trips: [{ service: 'wd', route: 'GF:X', shape: 0, legs: [[86400, 0], [88200, 6000]] }] };
    const out = sailingsAt(late, Date.parse('2026-08-20T00:20:00-07:00'), localDayStart);
    assert.equal(out.length, 1, 'an after-midnight sailing must still be found');
  });

  it('is empty when nothing is scheduled', () => {
    assert.deepEqual(sailingsAt(schedule, Date.parse('2026-08-19T04:00:00-07:00'), localDayStart), []);
    assert.deepEqual(sailingsAt({ trips: [] }, WED_NOON, localDayStart), []);
  });
});
