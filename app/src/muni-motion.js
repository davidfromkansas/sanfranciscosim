// Live Muni motion & service kernel — the rules that decide whether a vehicle
// is moving, dwelling, or has no business being in the scene at all.
//
// WHY THIS FILE EXISTS (read before changing anything in it)
//
// "The buses are frozen" and "parked buses are cluttering the city" have been
// fixed five separate times (9e9accd8, 10b388aa, 5f0ea041, 73bb2a96, 4cd32464)
// and each fix was later undone by an unrelated pass through muni.js, because
// the rules lived inline in a 1500-line renderer where they looked like
// arbitrary arithmetic. They live here instead: pure functions, no three.js, no
// closure state — covered by app/test/muni-motion.test.mjs, which encodes every
// past regression as a test. If a change makes one of those tests fail, it is
// re-introducing a bug the city has already shipped once.
//
// THE FOUR INVARIANTS
//
// 1. Dwell is a DISPLACEMENT test, never a speed reading. GTFS-RT `speed` is an
//    instantaneous sample; 260 of 507 Muni vehicles report exactly 0 at any
//    instant (stopped at a light when sampled). Treating that as "parked" froze
//    half the fleet every poll.
// 2. Dwell is measured from fix to fix (`fixStep`), never from the render
//    position to the target (`gapS`): dead reckoning legitimately drives a bus
//    past its target, so gapS goes negative on a bus that just covered 900 m.
// 3. A vehicle keeps moving between fixes. Fresh fixes are up to ~120 s apart
//    (60 s poll vs 90 s server TTL, worse in degraded mode) and identical
//    payloads must not stop anything — the target extrapolates along the shape.
// 4. Liveness and freshness are different clocks. `lastFixAt` (bumped on EVERY
//    poll, stale ones included) decides whether a vehicle still exists;
//    `lastFreshFixAt` (bumped only by a new fix) drives speed and the
//    dead-reckon cap. Merging them evicted the whole fleet every 3 minutes.
//
// Removal from the scene is the other half of the contract: a vehicle that the
// data says is parked, on layover, or off its alignment sinks out (dormancy),
// and one that stops being reported at all is dropped (staleness).

// ------------------------------------------------------------------ tuning

// Displacement across one fix gap below which a vehicle is standing still.
export const DWELL_STEP_M = 14; // ~one 40-foot coach at 1.6x
export const MAX_SPEED = 20; // m/s hard cap (45 mph); transit never exceeds it
// Cap on how far past the last fresh fix a vehicle may extrapolate along its
// shape (seconds). Fresh fixes arrive at most ~120 s apart in normal mode, so
// this bridges the gap; beyond it the vehicle eases to a stop and waits.
export const DEAD_RECKON_MAX_S = 120;
// A first fix has no previous position to compare against, so its only movement
// evidence is the worthless instantaneous `speed`. A vehicle whose own
// predictions say it is working gets a modest provisional speed instead of
// standing still until the second fix lands.
export const PROVISIONAL_SPEED = 5; // m/s, ~18 km/h: Muni's average speed
export const PROVISIONAL_LEAD_M = 150; // how far that guess may run unconfirmed
// Displacement-free fix span after which a vehicle is standing, not rolling.
// One poll gap plus slack, so a single missed fix can't trip it.
export const STILL_MS = 100 * 1000;
// Standing this long with no movement at all -> yard, layover, or off shift.
export const PARK_HIDE_MS = 5 * 60 * 1000;
// Standing, and the next predicted stop is this far out (or there is none while
// the feed is predicting for others) -> the run hasn't started yet.
export const LAYOVER_LEAD_MS = 5 * 60 * 1000;
// No fix at all for this long -> the vehicle leaves the scene.
export const STALE_MS = 3 * 60 * 1000;
// Consecutive polls a vehicle may be absent from before it is dropped.
export const MISSES_TO_DROP = 2;

// ------------------------------------------------------------ in service?

// Do the vehicle's own predictions say it is working right now? No predictions
// while the feed is publishing them for others means "not yet"; no predictions
// anywhere (degraded mode) means unknown, so assume working.
export function inService(stops, at, predictionsSeen) {
  const eta = stops?.[0]?.arrivalAt ?? null;
  if (eta == null) return !predictionsSeen;
  return eta - at < LAYOVER_LEAD_MS;
}

// Speed to start a newly sighted vehicle at. See PROVISIONAL_SPEED.
export function seedSpeed(bus, now, predictionsSeen) {
  if (Number.isFinite(bus.speedMs) && bus.speedMs > 0) return Math.min(MAX_SPEED, bus.speedMs);
  return inService(bus.stops, now, predictionsSeen) ? PROVISIONAL_SPEED : 0;
}

// Why this vehicle does not belong in the scene right now, or null. Measured in
// FIX time, not wall clock (invariant 4): a stale payload delivers no new
// fixes, and that must freeze this clock rather than quietly empty the city.
export function dormantReason(state, predictionsSeen) {
  const still = state.lastFreshFixAt - state.movedAt;
  if (still > PARK_HIDE_MS) return 'parked';
  if (still > STILL_MS && !inService(state.stops, state.lastFreshFixAt, predictionsSeen)) {
    return 'layover';
  }
  return null;
}

// Has this vehicle stopped being reported? `lastFixAt` is bumped by every poll
// that mentions it, stale payloads included (invariant 4).
export function shouldDrop(state, now) {
  return state.misses >= MISSES_TO_DROP || now - state.lastFixAt > STALE_MS;
}

// ---------------------------------------------------------------- movement

// Speed to run at so the vehicle covers the ground it actually covered.
// `fixStep` is the ONLY dwell evidence (invariants 1 and 2); `reported` merely
// biases how fast a vehicle runs once we know it is moving, and `gapS` only
// lets an on-shape vehicle catch up to a target it is behind.
export function targetSpeedFor({ fixStep, gapSeconds, gapS = 0, reported = null, onShape }) {
  const gap = Math.max(1, gapSeconds);
  if (fixStep < DWELL_STEP_M) return 0;
  if (!onShape) return Math.min(MAX_SPEED, fixStep / gap);
  const behind = Math.max(0, gapS) / gap;
  return Math.min(MAX_SPEED, Math.max(behind, fixStep / gap, (reported ?? 0) * 0.6));
}

// How far to extrapolate a moving vehicle's target along its shape this frame
// (invariant 3), or 0 when it must wait for real data. Called only when the
// vehicle has caught up with its target, i.e. `lead` has run out.
export function deadReckonAdvance({ lead, targetSpeed, sinceFreshS, provisional, targetS, provisionalCap, dt }) {
  if (lead >= DWELL_STEP_M || targetSpeed <= 0) return 0;
  if (sinceFreshS >= DEAD_RECKON_MAX_S) return 0;
  // A vehicle still running on its first-fix guess only rolls
  // PROVISIONAL_LEAD_M before waiting, so a genuinely parked one drifts half a
  // block, not half a route.
  if (provisional && !(targetS < provisionalCap)) return 0;
  return targetSpeed * dt;
}
