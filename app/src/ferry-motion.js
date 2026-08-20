// Live ferry motion kernel — the rules that decide whether a vessel is under
// way, lying alongside, or has no business being in the scene at all.
//
// WHY THIS FILE EXISTS (read before changing anything in it)
//
// The same shape of bug that froze the buses five times was still live in the
// ferries, because ferries.js predates app/src/muni-motion.js and never
// inherited its lessons. It kept ONE clock, `lastFixAt`, bumped on every poll.
// The browser polls /api/ferries every 60 s; the server caches for 90 s; so a
// large share of polls hand back a byte-identical payload. On such a repeat the
// vessel's displacement is 0, which was read as "this boat is not moving":
// speed went to 0, dead reckoning switched off, the boat froze mid-Bay, its
// wake vanished (length is derived from speed) and its card reported 0 kn while
// it was under way.
//
// The rules therefore live here — pure functions, no three.js, no closure
// state — covered by app/test/ferry-motion.test.mjs. A failure there means a
// fix is being reverted; fix the code, not the expectation.
//
// THE INVARIANTS (1, 2 and 4 are muni-motion.js's, earned again here)
//
// 1. Dwell is a DISPLACEMENT test, never a speed reading. 511's SIRI `speed` is
//    an instantaneous sample and boats at dock report all sorts of things.
// 2. Displacement is measured fix to fresh fix, never render-position to
//    target: dead reckoning legitimately drives a vessel past its target.
// 3. A vessel keeps moving between fixes. Our own cadence guarantees repeats,
//    so an identical payload must not stop anything.
// 4. Liveness and freshness are different clocks. `lastFixAt` (bumped by every
//    poll that mentions the vessel, repeats included) decides whether it still
//    exists; `lastFreshFixAt` (bumped only by a genuinely new fix) drives
//    speed, heading and the dead-reckon cap.
//
// MEASURED, production, 2026-08-17: two polls 60 s apart returned an identical
// `fetchedAt` — the cache serving a repeat, exactly as invariant 3 predicts.
// All 15 vessels carry the SAME `recordedAt`, because 511 publishes one
// fleet-wide snapshot rather than per-vessel timestamps, and that snapshot was
// 4.7 s and 11.3 s old at the two upstream refreshes sampled. So `recordedAt`
// is a sound freshness key, and the upstream is far fresher than our cadence.

// ------------------------------------------------------------------ tuning

// Displacement across one fresh-fix gap below which a vessel is lying still.
// A boat drifting on its lines at a berth moves a few metres between fixes.
export const DWELL_STEP_M = 20;
// m/s hard cap — a Gemini-class boat tops out around 25 kn.
export const MAX_SPEED = 13;
// Below this a vessel is not under way: heading is held rather than derived
// from motion, so a docked boat never spins on the spot.
export const IDLE_SPEED = 0.4;
// The worst realistic wait for a genuinely new position. The browser polls
// every 60 s and the server holds each answer for 90 s, so a client can poll
// just before a refresh and again just after the next one: 60 + 90 = 150 s in
// the worst alignment, ~120 s typically. muni-motion.js sizes its cap off the
// same arithmetic, because it is the same poll and the same TTL.
export const WORST_FRESH_FIX_GAP_S = 150;
// Cap on how far past the last FRESH fix a vessel may be extrapolated.
//
// THIS MUST COVER THE GAP ABOVE, or the boats stall. It was 90 - inherited from
// the version of this file that had one clock, where it never bound because
// every poll reset the timer. Once the clock started running from the last
// FRESH fix (invariant 4), 90 became the binding constraint and left a boat
// sitting still for up to a minute in every two-minute cycle: the exact
// symptom the freshness fix was written to remove, moved one layer down.
//
// Extrapolating further is safe here BECAUSE of invariant 1: a vessel whose
// displacement is under DWELL_STEP_M has speed 0, and deadReckonRun refuses to
// move anything at or below IDLE_SPEED. So a longer cap only ever extends a
// boat that the data says is genuinely under way; a berthed one never creeps.
export const DEAD_RECKON_MAX_S = 150;
// No fix at all for this long -> the vessel leaves the scene. Matches the
// server's own stale horizon.
export const STALE_MS = 10 * 60 * 1000;
// Consecutive polls a vessel may be absent from before it is dropped. Two, so
// one truncated response cannot flicker the fleet out.
export const MISSES_TO_DROP = 2;
// Movement across a fix gap that makes an out-of-service boat worth drawing
// anyway: a repositioning run is still a boat crossing the Bay.
export const MOVING_M = 100;

// ---------------------------------------------------------------- freshness

// Is this payload carrying a position we have not already seen? THE fix for the
// freeze bug (invariant 4).
//
// 511 stamps the whole fleet with one `recordedAt` per snapshot, so this is a
// fleet-wide clock, which is all we need: if the snapshot has not advanced,
// nothing in it has. When the feed omits the timestamp entirely we cannot tell,
// and must assume fresh — treating unknown as stale would freeze the fleet,
// which is the very bug this file exists to prevent.
export function isFreshFix(previousRecordedAt, recordedAt) {
  if (recordedAt == null) return true;
  if (previousRecordedAt == null) return true;
  return recordedAt !== previousRecordedAt;
}

// ---------------------------------------------------------------- movement

// Speed to run at so a vessel covers the ground it actually covered.
// `fixStep` is the ONLY dwell evidence (invariants 1 and 2): it must be measured
// between two FRESH fixes, and `gapSeconds` must be the time between those same
// two fixes, never the time since the last poll.
export function targetSpeedFor({ fixStep, gapSeconds }) {
  const gap = Math.max(1, gapSeconds);
  if (!(fixStep >= DWELL_STEP_M)) return 0;
  return Math.min(MAX_SPEED, fixStep / gap);
}

// Seconds of extrapolation available to a vessel right now, capped
// (invariant 3). Measured from the last FRESH fix — measuring from the last
// poll is what made repeats reset the clock and under-extrapolate.
export function deadReckonSeconds({ now, lastFreshFixAt }) {
  return Math.max(0, Math.min(DEAD_RECKON_MAX_S, (now - lastFreshFixAt) / 1000));
}

// How far ahead of its last fresh fix a vessel should be drawn. A boat below
// idle speed does not run at all, so a berthed vessel never creeps.
export function deadReckonRun({ speed, sinceFreshS }) {
  if (!(speed > IDLE_SPEED)) return 0;
  return speed * sinceFreshS;
}

// ----------------------------------------------------------------- heading

// The SB feed sends Bearing 0 for every vessel it has no heading for — docked
// boats and, at times, boats under way — so an exact 0 is treated as unknown
// and the heading is derived from movement instead. A genuinely north-bound
// boat loses nothing: its motion vector points north too.
export function usableBearing(bearingDeg) {
  return bearingDeg != null && bearingDeg !== 0;
}

// Compass bearing (deg clockwise from true north) to scene yaw. The asset's
// front is -Z and the scene has -z = north, +x = east, so a boat's yaw is just
// the negated bearing.
export function bearingToYaw(bearingDeg) {
  return -(bearingDeg * Math.PI) / 180;
}

// Heading from a movement vector in scene space, same convention as above.
export function motionToYaw(dx, dz) {
  return Math.atan2(-dx, -dz);
}

// Which way a vessel should be pointing after a fresh fix, or null to keep the
// heading it already had (invariant: a docked boat with no bearing must not
// spin on the spot).
export function headingFor({ bearingDeg, speed, dx, dz }) {
  if (usableBearing(bearingDeg)) return bearingToYaw(bearingDeg);
  if (speed > IDLE_SPEED) return motionToYaw(dx, dz);
  return null;
}

// ------------------------------------------------------------ scene tenure

// Has this vessel stopped being reported? `lastFixAt` is bumped by every poll
// that mentions it, repeats included (invariant 4) — a boat sitting in a
// repeated payload is still present, just not newly located.
export function shouldDrop({ misses = 0, lastFixAt }, now) {
  return misses >= MISSES_TO_DROP || now - lastFixAt > STALE_MS;
}

// Should this vessel be drawn? Out-of-service boats only count if they are
// actually going somewhere. Staleness is measured on the liveness clock.
export function shouldRender({ lastFixAt, inService, moved, inScene }, now) {
  if (now - lastFixAt > STALE_MS) return false;
  if (!inScene) return false;
  return Boolean(inService) || moved > MOVING_M;
}
