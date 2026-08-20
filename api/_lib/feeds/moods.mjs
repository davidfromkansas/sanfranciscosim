// --------------------------------------------------------------------- mood
//
// Its own module, with no dependencies, because the drift test in
// app/test/moods.test.mjs imports moodFor to compare it against the diorama's
// copy — and importing it from residents.mjs dragged @vercel/blob into a test
// run that only installs app/'s dependencies. The build failed on a cacheless
// clone. A pure table has no business sitting behind a blob client.
//
// Every resident carries a mood, after RollerCoaster Tycoon's guest happiness.
// The point of stealing it from a theme park rather than from Social Simulacra
// is what the trait attaches to. Simulacra makes "is a troll" part of the
// PERSONA — and their own paper refuses demographic personas for exactly the
// reason that would bite us here: ours are built from real Census records, so
// a troll flag would land on somebody with a specific birthplace, income and
// language, and the simulation would be saying that kind of person is like
// that. A mood is a state somebody is IN. Nobody is their mood.
//
// A NUMBER, not a word, because in RCT happiness moves — riding a ride lifts
// it, queuing drops it, and it decays if nothing good happens. None of that is
// wired up yet: this demo assigns a mood and leaves it there. Storing the
// number anyway is what makes the moving version a small change rather than a
// migration.
export const MOODS = [
  { at: -2, key: "grumpy", label: "Grumpy", emoji: "\u{1F621}" },
  { at: -1, key: "sad", label: "Sad", emoji: "\u{1F614}" },
  { at: 0, key: "neutral", label: "Neutral", emoji: "\u{1F610}" },
  { at: 2, key: "cheerful", label: "Cheerful", emoji: "\u{1F929}" },
];

// Four, not the seven RCT shows, because the intensity tiers were the weak
// ones: "grumpy" and "very grumpy" are nearly the same instruction to write
// from and identical on a badge the size of a thumbnail. What earns its place
// is the POSTURE — combative, withdrawn, ordinary, generous — and grumpy and
// sad are not two points on one line. One picks fights and the other goes
// quiet, which produces genuinely different posts.
//
// Roughly one resident in five is difficult, which is what makes the contested
// threads fire at all.
export const MOOD_WEIGHTS = [180, 120, 400, 300];

// How each mood writes. Deliberately about MANNER, not opinion: the identity
// paragraph decides what somebody thinks, and the mood decides what kind of
// day they are having while they say it. A grumpy resident is not a different
// person with different politics; they are the same person, shorter with you.
export const MOOD_VOICE = {
  grumpy:
    "You are in a foul mood and past being diplomatic about it. Say the blunt thing. You are short with people, quicker to point out what is wrong than what is fine, and willing to be the one who says what everybody is thinking. Do not be cruel about anyone's identity — you are fed up, not hateful.",
  sad: "You are low today. You are quieter than usual, more resigned than angry, and inclined to notice what has been lost rather than what might be fixed.",
  neutral:
    "You are in an ordinary mood. Nothing is colouring how you say this either way.",
  cheerful:
    "You are in a good mood and it shows. You are warm, generous with people, quick to give something the benefit of the doubt, and glad to be useful — the kind of day where you offer something rather than only comment on it.",
};

// Deterministic from the resident's own id, so a person you met yesterday is in
// the same mood today and a reload does not reshuffle the city's temper.
export function moodFor(id) {
  let h = 2166136261;
  for (let i = 0; i < id.length; i++) {
    h ^= id.charCodeAt(i);
    h = Math.imul(h, 16777619) >>> 0;
  }
  const total = MOOD_WEIGHTS.reduce((a, b) => a + b, 0);
  let roll = (h >>> 8) % total;
  for (let i = 0; i < MOOD_WEIGHTS.length; i++) {
    roll -= MOOD_WEIGHTS[i];
    if (roll < 0) return MOODS[i];
  }
  return MOODS[2]; // neutral
}
