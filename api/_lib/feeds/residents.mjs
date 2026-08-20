// r/simfrancisco — a subreddit simulation after Social Simulacra (arXiv
// 2208.04024). Deliberately small. The whole system is two generators:
//
//   persona paragraph + subreddit goal + rules            -> POST
//   persona paragraph + subreddit goal + rules + thread   -> REPLY
//
// and everything else is arithmetic kept OUT of the model. Nobody picks a topic
// for a resident; they decide what is worth posting from their own paragraph.
// Nobody asks the model who should speak next; that is a coin flip in code.
// There is no news feed, no interests table, no memory, no planner. If a post
// is about a bus route it is because the person in the paragraph rides one.
//
// Replies are generated ONE AT A TIME, each seeing every reply before it.
// Generating a thread in a single call is what makes every voice in it
// converge on the same one — the paper's central mechanical finding.
//
// Without a gateway credential this throws, the registry serves `empty`, and
// the panel says the neighbours are quiet. The city itself never needs a key.

import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { registerFeed } from "../feedcore.mjs";
import { get, put, BlobPreconditionFailedError } from "@vercel/blob";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CAST = path.resolve(HERE, "../../_data/personas.json");

const ENDPOINT = "https://ai-gateway.vercel.sh/v1/chat/completions";
// Chosen for what it is NOT: the only large open-weight model in its price band
// that is not a reasoning model. This is a voice task — a model that
// deliberates first writes a considered summary of what someone might say
// rather than the thing they would post.
const MODEL = "deepseek/deepseek-v3.2";
const TEMPERATURE = 0.9;

// The community. `rules` is empty today and the prompts already handle that;
// populate it and both generators pick it up with no other change.
const SUBREDDIT = {
  id: "simfrancisco",
  name: "r/simfrancisco",
  goal: "Discuss news, events, politics, culture, and everyday life relevant to San Francisco",
  rules: [
    "Be excellent to each other. We want r/simfrancisco to be the best of what San Francisco has to offer. Treat each other with respect, and be inclusive with your comments. The people you're interacting with aren't just names on a screen; they're neighbors who love this city as much as you. We forbid any content that is intolerant, insulting, or hateful, particularly othering any individual or outgroup as second-class citizens or subhuman. Threats of violence, even in \"jest\", will result in an immediate, permanent ban.",
    "Be civil, polite and courteous. Don't use crude language, inappropriate content, or otherwise derogatory remarks towards each other. Do not slander. Criminal allegations, especially against private individuals (as opposed to public people like elected representatives), require a reputable external source like news media.",
    "Be active in contributing to the community. We're a city of creators, artists, professionals, weirdos, activists, and human beings; discuss what interests you and makes you interesting. As you do, please respect those with different points of view, converse with the people who reply, and stick around to engage with our community across a wide range of topics.",
    "Build something you're proud of. Use this subreddit to organize volunteer work and donations. Treat it as a gallery for your SF artwork. Gather a crowd for some bizarre stunt. Organize Zoom meetups on a slow Friday night. A large portion of our city is here, and we all have an opportunity to make San Francisco a better place together!",
    "We forbid any posts that aren't relevant to San Francisco and our stated goal of: Discuss news, events, politics, culture, and everyday life relevant to San Francisco",
  ],
};

// From the paper. Reply rate and thread length are its numbers; the
// new-participant rate is what keeps a thread a conversation rather than a
// queue of strangers each speaking once.
const simulationConfig = {
  // Sampled ONCE per thread, then reused for every continuation decision in it.
  // The paper draws from a normal around .65, and the spread is the whole point:
  // a fixed rate gives every post the same expected length, and a subreddit
  // where every thread runs the same depth reads as machinery. Drawn per thread,
  // one post limps to a single reply and the one next to it argues for eight.
  replyProbability: { mean: 0.65, stdev: 0.18, min: 0.05, max: 0.95 },
  // Every vote a post collects — either direction — makes its conversation
  // likelier to keep going, added straight onto the thread's own probability.
  // The base coin alone left roughly one liked post in three with no replies,
  // which reads wrong: five people moved to click are five people one of whom
  // usually says something. Engagement begets engagement, and a post divisive
  // enough to collect downvotes earns the same pull. The 0.95 ceiling keeps
  // silence possible everywhere; zero votes still means silence outright.
  voteEnergy: 0.08,
  maxReplies: 8,
  newParticipantProbability: 0.5,
  // Asked for in the prompt AND enforced after, because a model told to stay
  // under a limit treats it as a suggestion. The title is not something the
  // spec set, so it gets a length a headline can actually be.
  maxChars: { post: 240, reply: 240, title: 120 },
};

// Box–Muller. Clamped, because the tail of a normal goes past both ends of a
// probability and a thread with p > 1 would only ever stop at maxReplies.
function sampleReplyProbability() {
  const { mean, stdev, min, max } = simulationConfig.replyProbability;
  const u = 1 - Math.random();
  const v = Math.random();
  const z = Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  return Math.min(max, Math.max(min, mean + stdev * z));
}

// Voting. Each sampled resident decides alone — that independence is the point:
// a score has to be an aggregate of many small judgements, not a number a model
// made up. Votes fire ONCE, when a post or reply is created, and never again;
// re-sampling later would multiply the cost by however many passes.
//
// Sizes are small on purpose. At this refresh rate each extra post voter costs
// about $0.74 a month and each extra reply voter about $1.69, because replies
// outnumber posts 2.3 to 1. A score of +4 reads perfectly well — you do not
// need twenty-five voters to make a number look real.
const votingConfig = {
  postVoterSampleSize: 5,
  replyVoterSampleSize: 3,
};

// A separate rail from the generation budget: a vote call costs about a quarter
// of a post, and counting them together would misprice both. A steady tick
// needs about twelve — one post at five voters, two-ish replies at three — so
// this is roughly double headroom.
const MAX_VOTES_PER_REFRESH = 24;

// ONE post every tick, with whatever replies its own probability earns it, and
// the same rate whether the feed holds nothing or a hundred and forty threads.
// There is no opening burst and no catch-up mode: a subreddit that posts faster
// because it is empty is a subreddit whose history is a lie about how busy the
// city was that hour. A thread is finished the moment its roll fails, so new
// posts are the only thing that keeps the feed moving.
const NEW_THREADS_PER_REFRESH = 1;
const RETIRE_AFTER = 24 * 60 * 60 * 1000;
// A day at one post every ten minutes is 144 threads, so a 50-thread cap would
// have filled in eight hours and then silently stopped the subreddit — new
// posts blocked, nothing retiring for another sixteen. The cap has to be a
// backstop against runaway generation, not a limit the normal rate walks into.
const MAX_THREADS = 200;
// How long a served payload is reused before the blob is read again. It is not
// the posting cadence — that is WINDOW_MS, down where the tick decides its
// minute. The two were one constant while the feed both generated and served;
// they became different numbers the moment those split, because a read is a
// blob GET and can be cheap and frequent while a post stays every ten minutes.
const READ_TTL_MS = 30 * 1000;
// The budget rail. Everything else here is taste; this is the line that stops a
// bad day costing real money. Ten covers the worst case for one tick — a post
// whose probability earns it the full eight replies, plus a spare for resuming
// a thread the previous tick cut short. The average tick spends about three.
const MAX_MESSAGES_PER_REFRESH = 10;

// --------------------------------------------------------------------- mood
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
const MOODS = [
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
const MOOD_WEIGHTS = [180, 120, 400, 300];

// How each mood writes. Deliberately about MANNER, not opinion: the identity
// paragraph decides what somebody thinks, and the mood decides what kind of
// day they are having while they say it. A grumpy resident is not a different
// person with different politics; they are the same person, shorter with you.
const MOOD_VOICE = {
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

const moodBlock = (persona) => {
  const mood = moodFor(persona.id);
  return `\n\nMOOD\n${MOOD_VOICE[mood.key]}`;
};

// ------------------------------------------------------------------- prompts

const rulesBlock = () =>
  SUBREDDIT.rules.length
    ? SUBREDDIT.rules.map((r) => `- ${r}`).join("\n")
    : "No additional rules.";

async function complete(system, user, maxTokens) {
  // The gateway takes either a key or the project's OIDC token; the token is
  // what `vercel env pull` writes for local development, so a linked checkout
  // runs the real writer without a production secret landing on a laptop.
  const credential =
    process.env.AI_GATEWAY_API_KEY || process.env.VERCEL_OIDC_TOKEN;
  if (!credential)
    throw new Error(
      "no AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN — feed offline",
    );

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${credential}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      temperature: TEMPERATURE,
      max_tokens: maxTokens,
      messages: [
        { role: "system", content: system },
        { role: "user", content: user },
      ],
    }),
  });
  if (!res.ok)
    throw new Error(
      `gateway ${res.status}: ${(await res.text()).slice(0, 200)}`,
    );
  const body = await res.json();
  const text = (body.choices?.[0]?.message?.content ?? "").trim();
  if (!text) throw new Error("gateway returned an empty message");
  return text;
}

// Models wrap JSON in code fences, or add a sentence before it, however plainly
// you ask. Pulling the outermost braces out costs nothing and turns a whole
// class of retry into a non-event.
function parseJson(text) {
  const start = text.indexOf("{");
  const end = text.lastIndexOf("}");
  if (start !== -1 && end > start) {
    try {
      return JSON.parse(text.slice(start, end + 1));
    } catch {
      // fall through to the salvage below
    }
  }
  // A response that ran out of tokens has an opening brace, real content, and no
  // closing one. Throwing that away wastes a generation already paid for, so
  // read the fields out directly and let the sentence end where it ended.
  const field = (name) => {
    const at = text.search(new RegExp(`"${name}"\\s*:\\s*"`, "i"));
    if (at === -1) return undefined;
    let i = text.indexOf('"', text.indexOf(":", at)) + 1;
    let out = "";
    for (; i < text.length; i++) {
      const c = text[i];
      if (c === "\\") {
        const next = text[i + 1];
        out += next === "n" ? "\n" : next === "t" ? "\t" : (next ?? "");
        i++;
        continue;
      }
      if (c === '"') break;
      out += c;
    }
    return out.trim();
  };
  const title = field("title");
  const body = field("body");
  if (!title && !body)
    throw new Error(`no JSON in model output: ${text.slice(0, 120)}`);
  return { title, body };
}

// Bringing an over-long answer down to the limit WITHOUT losing what it said.
//
// Slicing at a character count is the obvious move and the wrong one: it ends
// posts mid-thought — "takes more than a stripe to slow down" — which reads as
// broken software rather than as brevity, and it throws away the writer's
// actual point. So the model is asked to say the same thing shorter, in its own
// voice, and only if that fails twice do we fall back to dropping whole
// sentences from the end. Nothing is ever cut mid-sentence.
async function fitToLimit({ system, text, limit, maxTokens, attempts = 2 }) {
  let current = String(text).replace(/\s+/g, " ").trim();
  for (let i = 0; i < attempts && current.length > limit; i++) {
    const user =
      `You wrote this:\n\n${current}\n\n` +
      `It is ${current.length} characters, which is too long. Rewrite it in under ${limit} characters.\n\n` +
      `Keep the same point, the same voice, and every idea in it. Say it more briefly — do not add anything, ` +
      `do not trail off, and finish the last sentence.\n\n` +
      `Return JSON:\n{ "body": "..." }`;
    try {
      const { body } = parseJson(await complete(system, user, maxTokens));
      if (!body) break;
      const shorter = String(body).replace(/\s+/g, " ").trim();
      // Only accept a rewrite that actually helped.
      if (shorter.length < current.length) current = shorter;
    } catch {
      break; // a failed repair is not worth failing the whole generation over
    }
  }
  return current.length > limit
    ? dropTrailingSentences(current, limit)
    : current;
}

// Last resort, and only whole sentences. Losing a sentence is a real loss, but
// it is a loss the reader can see the shape of; a half-sentence is a bug.
function dropTrailingSentences(text, limit) {
  const parts = text.match(/[^.!?]+[.!?]+(\s|$)/g);
  if (!parts) return text; // no sentence boundaries at all — leave it whole
  let out = "";
  for (const part of parts) {
    if ((out + part).trim().length > limit) break;
    out += part;
  }
  return out.trim() || text;
}

// Where this person lives. 79% of the paragraphs never say, and the PUMA was
// known to every other part of the system but never reached the writer — so a
// post that needed a place got an invented one, and a Bayview resident wrote
// "it's quiet here in the Sunset" while the panel printed Bayview beside his
// name. The line is deliberately part of WHO YOU ARE: where you live is not a
// property of the subreddit.
const livesIn = (persona) =>
  persona.neighbourhood
    ? `You live in ${persona.neighbourhood}, San Francisco. Write from there — do not place yourself in another neighbourhood.`
    : "";

export async function generatePost({ persona, subreddit }) {
  const system =
    `You are simulating a person posting in a subreddit.\n\n` +
    `PERSONA\n${persona.persona}\n` +
    `${livesIn(persona)}` +
    moodBlock(persona) +
    `\n\nSUBREDDIT GOAL\n${subreddit.goal}\n\n` +
    `SUBREDDIT RULES\n${rulesBlock()}`;
  const user =
    `Generate one top-level Reddit post that this person would realistically choose to make in this subreddit.\n\n` +
    `The post should:\n` +
    `- Fit the person's persona.\n` +
    `- Be relevant to the subreddit goal.\n` +
    `- Follow the subreddit rules, if any.\n` +
    `- Feel like a real Reddit post.\n` +
    `- Let the person decide naturally what is worth posting about.\n` +
    `- Not mention the persona, prompt, subreddit goal, rules, or simulation.\n\n` +
    `The title must be under ${simulationConfig.maxChars.title} characters and the body under ${simulationConfig.maxChars.post} characters. Say one thing and stop.\n\n` +
    `Return JSON:\n{ "title": "...", "body": "..." }`;

  const { title, body } = parseJson(await complete(system, user, 350));
  if (!title || !body)
    throw new Error("post came back without a title or body");
  return {
    title: await fitToLimit({
      system,
      text: title,
      limit: simulationConfig.maxChars.title,
      maxTokens: 120,
    }),
    body: await fitToLimit({
      system,
      text: body,
      limit: simulationConfig.maxChars.post,
      maxTokens: 200,
    }),
  };
}

export async function generateReply({
  persona,
  subreddit,
  post,
  replies,
  stance,
}) {
  const system =
    `You are simulating a person participating in a Reddit discussion.\n\n` +
    `PERSONA\n${persona.persona}\n` +
    `${livesIn(persona)}` +
    moodBlock(persona) +
    `\n\nSUBREDDIT GOAL\n${subreddit.goal}\n\n` +
    `SUBREDDIT RULES\n${rulesBlock()}`;
  const formatted = replies.length
    ? replies.map((r) => `${r.name}: ${r.body}`).join("\n\n")
    : "(no replies yet)";
  // Reddit shows you who wrote the post you are answering, and the responder
  // may BE that person — the poster is allowed back into their own thread. Told
  // neither of those things, they re-introduced themselves to their own
  // readers: the author of a thread about the 22 bus replied to it explaining
  // that he rides the 22, as though meeting a stranger.
  const own = post.authorId && post.authorId === persona.id;
  // Deliberately light. The vote is a fact about them, not a brief: telling
  // somebody "explain your downvote" produces a complaint with a thesis
  // statement, which is not how anyone writes. Naming the reaction and getting
  // out of the way gets the objection in their own voice.
  const voted =
    stance === "down"
      ? `You downvoted this. You did not think it belonged here or did not like it. Say what you think, the way you would actually say it.\n\n`
      : stance === "up"
        ? `You upvoted this. You are glad somebody said it, and others in the thread disagree.\n\n`
        : stance === "defend"
          ? `You did not vote on this, but the thread has turned on the author and you think that is too harsh. Push back the way you actually would.\n\n`
          : "";
  const user =
    `DISCUSSION\n\n` +
    voted +
    `Original post by ${post.author ?? "someone"}:\n\nTitle:\n${post.title}\n\nBody:\n${post.body}\n\n` +
    `Replies so far:\n${formatted}\n\n` +
    (own
      ? `You wrote that original post. You are coming back to your own thread — answer the people who replied to you. Do not re-introduce yourself or restate what you already said.\n\n`
      : "") +
    `Write the next reply as this person.\n\n` +
    `Respond naturally to the discussion as it currently exists.\n` +
    `The reply can respond to the original post or to something another person has already said.\n\n` +
    `The reply should:\n` +
    `- Fit the person's persona.\n` +
    `- Follow the subreddit rules, if any.\n` +
    `- Feel like a real Reddit comment.\n` +
    `- Not mention the persona, prompt, subreddit goal, rules, or simulation.\n` +
    `- Not summarize the whole conversation.\n` +
    `- Avoid unnecessarily repeating comments that have already been made.\n` +
    `- Not sound like an AI assistant.\n\n` +
    `It is okay for the reply to be short, casual, opinionated, uncertain, humorous, or disagree with another commenter.\n\n` +
    `Keep it under ${simulationConfig.maxChars.reply} characters.\n\n` +
    `Return JSON:\n{ "body": "..." }`;

  const { body } = parseJson(await complete(system, user, 200));
  if (!body) throw new Error("reply came back without a body");
  return {
    body: await fitToLimit({
      system,
      text: body,
      limit: simulationConfig.maxChars.reply,
      maxTokens: 200,
    }),
  };
}

// ------------------------------------------------------------------- voting

// One resident, one piece of content, one decision. No context beyond what they
// need to judge it: who they are, what this place is for, and the thing itself.
export async function generateVoteDecision({ persona, subreddit, content }) {
  const system =
    `You are simulating a person browsing a subreddit.\n\n` +
    `PERSONA\n${persona.persona}\n` +
    `${livesIn(persona)}` +
    // Voting is where a mood is VISIBLE. A shift in how somebody phrases a post
    // is subtle; a grumpy resident downvoting is a score, and a score is what
    // brings the negative and contested branches to life — the two sides
    // arguing, the defenders pushing back on a pile-on. That machinery has been
    // built and almost never fires, because a room of even-tempered people
    // agrees with everything.
    moodBlock(persona) +
    `\n\nSUBREDDIT GOAL\n${subreddit.goal}\n\n` +
    `SUBREDDIT RULES\n${rulesBlock()}`;
  const user =
    `CONTENT\n${content}\n\n` +
    `Decide how this person would react to this content.\n\n` +
    `Choose exactly one:\n- "upvote"\n- "downvote"\n- "none"\n\n` +
    `UPVOTE — this person thinks it contributes to the subreddit and fits its goal and rules.\n` +
    `DOWNVOTE — this person thinks it detracts, does not belong, is misleading, low quality, or conflicts with the goal or rules.\n` +
    `NONE — this person would move on without feeling strongly enough to vote.\n\n` +
    `Consider both how well it fits the subreddit, and this person's own interests, opinions and values.\n\n` +
    `Important:\n` +
    `- It is normal to choose "none" — but vote when this person would actually feel something.\n` +
    `- Let the mood weigh on this. Somebody in a foul mood is readier to downvote and stingier with upvotes; somebody in a good mood is the reverse.\n` +
    `- Do not assume every relevant post deserves an upvote.\n` +
    `- Do not assume disagreement alone deserves a downvote.\n` +
    `- Stay consistent with the persona.\n` +
    `- Do not explain the decision.\n\n` +
    `Return JSON:\n{ "action": "upvote" | "downvote" | "none" }`;

  const { action } = parseJson(await complete(system, user, 40));
  return action === "upvote" || action === "downvote" ? action : "none";
}

// Selection stays out of the model, and nobody votes on their own words.
// Without replacement, so one resident cannot be asked twice about one thing.
function sampleVoters(cast, authorId, size) {
  const pool = cast.filter((p) => p.id !== authorId);
  const picked = [];
  const taken = new Set();
  const wanted = Math.min(size, pool.length);
  while (picked.length < wanted) {
    const i = Math.floor(Math.random() * pool.length);
    if (taken.has(i)) continue;
    taken.add(i);
    picked.push(pool[i]);
  }
  return picked;
}

// Every vote is stored individually — who, on what, which way, when. Totals are
// derived from these and never stored as the truth, so a score can always be
// explained by pointing at the residents who produced it.
async function simulateVotes({ cast, authorId, content, size, spend }) {
  const voters = sampleVoters(cast, authorId, size).filter(() => spend());
  if (!voters.length) return [];
  // Independent by definition, so they run at once. Replies cannot do this —
  // each one has to read the last — but a vote reads nothing but the content.
  const decisions = await Promise.all(
    voters.map((persona) =>
      generateVoteDecision({ persona, subreddit: SUBREDDIT, content })
        .then((action) => ({ persona, action }))
        .catch(() => ({ persona, action: "none" })),
    ),
  );
  const at = Date.now();
  return decisions
    .filter((d) => d.action !== "none")
    .map((d) => ({
      personaId: d.persona.id,
      value: d.action === "upvote" ? 1 : -1,
      at,
    }));
}

// Totals from the records, every time. Cheap at this size, and it means the
// stored votes cannot drift out of step with the number on screen.
function tally(votes = []) {
  let up = 0;
  let down = 0;
  for (const v of votes) v.value === 1 ? up++ : down++;
  return { upvotes: up, downvotes: down, score: up - down };
}

// --------------------------------------------------------------- who speaks

const pick = (list) => list[Math.floor(Math.random() * list.length)];

// Selection stays out of the model. Half the time somebody new walks in, half
// the time somebody already arguing comes back — that mix is what makes a
// thread read as a conversation rather than a row of strangers. Nobody follows
// themselves; the original poster may return later.
// What the room made of a post, from the votes it actually got. This is what
// decides whether a thread happens at all and who is in it — attention drives
// conversation, which is the paper's point and, until now, something our votes
// had no say in.
//
//   ignored    nobody voted either way. Nobody cared, so nobody replies. The
//              post stands alone, which is most of what a real subreddit is.
//   positive   more up than down. Anyone may reply, as before.
//   negative   more down than up. The people who disliked it are the ones who
//              speak, and they say why.
//   contested  a genuine tie with votes on both sides. Not indifference — an
//              argument. Both camps reply, alternating.
function moodOf(thread) {
  const { upvotes, downvotes } = tally(thread.votes);
  if (upvotes === 0 && downvotes === 0) return "ignored";
  if (upvotes > downvotes) return "positive";
  if (downvotes > upvotes) return "negative";
  return "contested";
}

// Everyone who voted a given way and has not spoken yet, never following
// themselves. A thread can only be as long as it has voters to draw on.
function votersOf(cast, thread, value) {
  const lastSpoke = thread.replies.at(-1)?.personaId ?? thread.authorId;
  const spoken = new Set(thread.replies.map((r) => r.personaId));
  const ids = (thread.votes ?? [])
    .filter((v) => v.value === value)
    .map((v) => v.personaId)
    .filter(
      (id) => id !== lastSpoke && id !== thread.authorId && !spoken.has(id),
    );
  return cast.filter((p) => ids.includes(p.id));
}

// Who speaks next, and from which camp. On a positive thread it is anyone in
// the city; on a negative or contested one it can only be someone who actually
// voted, because their reply is an account of that vote.
function pickResponder(cast, thread, mood) {
  // An ignored thread has no voters to draw on, and a human's floor has to be
  // fillable anyway — so the floor is served from the whole city, which is what
  // "positive" already means here.
  if (mood === "ignored") {
    const persona = pickAnyone(cast, thread);
    return persona ? { persona, stance: null } : null;
  }
  if (mood === "negative") {
    // Not only the critics. A downvoted post on a real board draws two kinds
    // of reply — the objections, and people arguing the pile-on is unfair —
    // so the floor is open to both, weighted by the vote. The +1 in the
    // denominator keeps a defender's slot open even when nobody upvoted:
    // somebody who never clicked anything can still think the thread is being
    // too hard on the author.
    const down = votersOf(cast, thread, -1);
    const { upvotes, downvotes } = tally(thread.votes);
    const wantCritic =
      Math.random() < downvotes / (downvotes + upvotes + 1) ||
      thread.replies.length === 0; // the first word goes to an objector —
    // a defence of a post nobody has criticised yet reads as noise
    if (wantCritic && down.length)
      return { persona: pick(down), stance: "down" };
    const up = votersOf(cast, thread, 1);
    if (up.length) return { persona: pick(up), stance: "up" };
    const anyone = pickAnyone(cast, thread);
    if (anyone) return { persona: anyone, stance: "defend" };
    return down.length ? { persona: pick(down), stance: "down" } : null;
  }
  if (mood === "contested") {
    // Alternate, so it reads as an argument rather than two monologues: answer
    // whichever side spoke last with the other one.
    const lastStance = thread.replies.at(-1)?.stance;
    const first = lastStance === "down" ? 1 : -1;
    const primary = votersOf(cast, thread, first);
    const other = votersOf(cast, thread, -first);
    const chosen = primary.length ? primary : other;
    if (!chosen.length) return null;
    return {
      persona: pick(chosen),
      stance: (primary.length ? first : -first) === 1 ? "up" : "down",
    };
  }
  const persona = pickAnyone(cast, thread);
  return persona ? { persona, stance: null } : null;
}

function pickAnyone(cast, thread) {
  const lastSpoke = thread.replies.at(-1)?.personaId ?? thread.authorId;
  const spoken = new Set([
    thread.authorId,
    ...thread.replies.map((r) => r.personaId),
  ]);

  const fresh = cast.filter((p) => !spoken.has(p.id));
  const returning = cast.filter((p) => spoken.has(p.id) && p.id !== lastSpoke);

  const wantFresh = Math.random() < simulationConfig.newParticipantProbability;
  if (wantFresh && fresh.length) return pick(fresh);
  if (!wantFresh && returning.length) return pick(returning);
  return fresh.length ? pick(fresh) : returning.length ? pick(returning) : null;
}

// ------------------------------------------------------------- when to post
//
// Six posts an hour, but not on the clock. A post landing at exactly :00, :10,
// :20 reads as a machine the moment anyone notices the pattern, and people
// notice patterns quickly. So the hour is cut into six windows and each window
// draws its OWN minute to fire on.
//
// The draw is deterministic from the window number rather than random, which is
// what lets it work without any shared state: two servers handed the same
// window compute the same minute, so the cron can fire every minute against any
// instance and still produce exactly one post per window. Random would have
// needed somewhere to write the decision down.
const WINDOW_MS = 10 * 60_000;

export function dueMinuteFor(window) {
  // xorshift-multiply on the window index — cheap, and spreads adjacent windows
  // apart instead of drifting one minute at a time the way `window % 10` would.
  // Math.imul, not `*`: a plain multiply of two 32-bit values exceeds what a
  // double holds exactly, and the bits that fall off the end took the sign with
  // them — the first version handed out minute -8.
  let h = Math.imul(window, 2654435761) >>> 0;
  h ^= h >>> 15;
  h = Math.imul(h, 2246822519) >>> 0;
  h ^= h >>> 13;
  return (h >>> 0) % 10;
}

let lastWindow = -1;

// True at most once per ten-minute window. `>=` rather than `===` so a window
// whose minute was missed — a cold start, a deploy, a slow generation running
// long — still gets its post late rather than losing it entirely.
export function postIsDue(now = Date.now()) {
  const window = Math.floor(now / WINDOW_MS);
  if (window === lastWindow) return false;
  const minute = Math.floor((now % WINDOW_MS) / 60_000);
  if (minute < dueMinuteFor(window)) return false;
  lastWindow = window;
  return true;
}

// ------------------------------------------------------------------- feed

let cast = null;
async function loadCast() {
  cast ??= JSON.parse(await readFile(CAST, "utf8")).people;
  return cast;
}

// Threads live in memory for the life of one instance and in blob storage for
// the life of the subreddit: restore() fills this from the blob before any tick
// reads it, and persist() writes it back after. A cold start therefore resumes
// the feed rather than beginning it again — which is the whole reason posts
// accumulate while nobody is looking.
const live = [];

async function openThread(people, spendVote) {
  const author = pick(people);
  const post = await generatePost({ persona: author, subreddit: SUBREDDIT });
  // Once, here, and never again for this post.
  const votes = await simulateVotes({
    cast: people,
    authorId: author.id,
    content: `${post.title}\n\n${post.body}`,
    size: votingConfig.postVoterSampleSize,
    spend: spendVote,
  });
  return {
    id: `${author.id}-${live.length}-${post.title.slice(0, 24)}`,
    authorId: author.id,
    author: {
      name: author.name,
      occupation: author.occupation,
      puma: author.puma,
    },
    title: post.title,
    body: post.body,
    votes,
    replies: [],
    // Sampled here and never resampled: this thread's own appetite for
    // discussion, fixed at birth like a real post's.
    replyProbability: sampleReplyProbability(),
    done: false,
    startedAt: Date.now(),
    at: Date.now(),
  };
}

// Roll, generate, append, roll again — the paper's continuation loop. A failed
// roll ends the thread permanently; `done` is what stops a later refresh from
// quietly reviving a conversation that already finished.
//
// The budget is the one thing allowed to interrupt without ending it: running
// out of allowance mid-thread leaves `done` false so the next refresh picks the
// same thread up where it stopped, rather than a long thread being silently
// truncated because it happened to be last in the loop.
async function growThread(people, thread, spend, spendVote) {
  const mood = moodOf(thread);
  // A visitor is owed an answer. A resident's post going unread is the honest
  // texture of a subreddit; a person from outside typing into one and hearing
  // nothing back is just a dead end, and they have no second post to try
  // again with. So a human thread has a floor and cannot be ignored.
  //
  // The floor is deliberately the only thing bought for them. Their VOTES are
  // sampled exactly like anybody's, so the score still says what the room made
  // of it, and everything above the floor still has to be earned by that score
  // — a lukewarm post gets its two and stops, a good one runs to eight.
  const floor = thread.human ? HUMAN.minReplies : 0;
  if (mood === "ignored" && !floor) {
    // Nobody voted, so nobody cared. The post stands on its own and the thread
    // is finished before it starts — which is most of what a real subreddit is,
    // and costs nothing to render.
    thread.done = true;
    return;
  }
  // Score decides WHETHER a thread happens and WHO is in it; the thread's own
  // probability decides HOW LONG it runs, pulled up by every vote the post
  // collected. The paper's continuation loop is otherwise untouched — it just
  // no longer runs on posts nobody looked at.
  const { upvotes, downvotes } = tally(thread.votes);
  const energy = Math.min(
    simulationConfig.replyProbability.max,
    thread.replyProbability +
      simulationConfig.voteEnergy * (upvotes + downvotes),
  );
  while (
    thread.replies.length < simulationConfig.maxReplies &&
    // Under the floor the roll is skipped entirely rather than weighted, so a
    // visitor's first two answers are a promise and not a good streak.
    (thread.replies.length < floor || Math.random() < energy)
  ) {
    if (!spend()) return;
    if (!(await addReply(people, thread, spendVote, mood))) break;
  }
  thread.done = true;
}

async function addReply(people, thread, spendVote, mood) {
  const chosen = pickResponder(people, thread, mood);
  // On a negative or contested thread the pool is only the people who voted
  // that way, so it runs dry long before maxReplies. That is the thread ending
  // because everyone who objected has said so, which is the right reason.
  if (!chosen) return false;
  const { persona: responder, stance } = chosen;
  const { body } = await generateReply({
    persona: responder,
    stance,
    subreddit: SUBREDDIT,
    post: {
      title: thread.title,
      body: thread.body,
      author: thread.author.name,
      authorId: thread.authorId,
    },
    replies: thread.replies,
  });
  // The reply is judged in its thread: a comment read without the post it
  // answers is a different comment.
  const votes = await simulateVotes({
    cast: people,
    authorId: responder.id,
    content:
      `ORIGINAL POST\n${thread.title}\n${thread.body}\n\n` +
      (thread.replies.length
        ? `EARLIER IN THE THREAD\n${thread.replies
            .slice(-2)
            .map((r) => `${r.name}: ${r.body}`)
            .join("\n")}\n\n`
        : "") +
      `REPLY BEING EVALUATED\n${body}`,
    size: votingConfig.replyVoterSampleSize,
    spend: spendVote,
  });
  thread.replies.push({
    votes,
    stance,
    personaId: responder.id,
    name: responder.name,
    occupation: responder.occupation,
    puma: responder.puma,
    body,
    at: Date.now(),
  });
  return true;
}

// --------------------------------------------------------------- persistence
//
// Until now the subreddit lived in one server's memory: a deploy wiped it, a
// cold start wiped it, and two instances each accumulated a different feed —
// so the scheduled tick could be writing to a server nobody was reading. The
// whole point of generating on a timer is that the posts are there when you
// arrive, which means they have to outlive the process that wrote them.
//
// One JSON blob holds the lot. Reads are uncached (`useCache: false`) because a
// stale read here means regenerating posts that already exist, and writes are
// CONDITIONAL on the etag we read — if another instance saved in between, ours
// is refused and dropped rather than clobbering theirs. That is the fix for the
// race the traffic-driven design would otherwise have: any warm instance can
// answer the cron, and only one of them can win a given write.
//
// Auth is OIDC (VERCEL_OIDC_TOKEN + BLOB_STORE_ID), automatic on Vercel and
// pulled by `vercel env pull` locally, so no long-lived secret is involved.
// With neither credential the whole layer sits out and the feed behaves exactly
// as it did before — in memory, forgetful, working.

const STATE_PATH = "simfrancisco/state.json";
const STATE_VERSION = 1;

// Connecting a store in the dashboard lets you choose an environment-variable
// PREFIX, and this project's connection chose one — so the id arrives as
// `sfsim_STORE_ID`, not the `BLOB_STORE_ID` the SDK looks for by default. Rather
// than depend on whatever prefix some future connection picks, find the id under
// any name ending in STORE_ID and hand it to the SDK explicitly.
function storeId() {
  if (process.env.BLOB_STORE_ID) return process.env.BLOB_STORE_ID;
  const key = Object.keys(process.env).find(
    (k) => k.endsWith("STORE_ID") && /^store_/.test(process.env[k] ?? ""),
  );
  return key ? process.env[key] : null;
}

// The same prefix trap as storeId(): a connection that chose a prefix names the
// token `<prefix>_READ_WRITE_TOKEN`, which the SDK's default lookup misses.
function blobToken() {
  if (process.env.BLOB_READ_WRITE_TOKEN)
    return process.env.BLOB_READ_WRITE_TOKEN;
  const key = Object.keys(process.env).find(
    (k) =>
      k.endsWith("READ_WRITE_TOKEN") &&
      /^vercel_blob_rw_/.test(process.env[k] ?? ""),
  );
  return key ? process.env[key] : null;
}

// Says out loud, once, which credential it found — or that it found none.
//
// This used to return a bare boolean, and when false the whole storage layer
// no-opped in silence: restore() read nothing, persist() wrote nothing, and the
// feed still looked alive because each instance served the posts it had
// generated in its own memory. Production ran that way for hours while every
// log line said 200 and the panel showed a different number of posts on every
// refresh. A missing credential is a deployment being wrong, not a feature
// being off, and it has to say so.
let announced = false;
function blobConfigured() {
  const token = blobToken();
  const ok = Boolean(token || (process.env.VERCEL_OIDC_TOKEN && storeId()));
  if (!announced) {
    announced = true;
    if (ok)
      console.log(
        `${SUBREDDIT.name}: blob storage ready via ${token ? "read-write token" : "OIDC"}, store ${storeId() ?? "(SDK default)"}`,
      );
    else
      console.error(
        `${SUBREDDIT.name}: BLOB STORAGE NOT CONFIGURED — posts cannot be ` +
          `saved or shared between instances. Wanted BLOB_READ_WRITE_TOKEN ` +
          `(or any *_READ_WRITE_TOKEN), or VERCEL_OIDC_TOKEN plus a store id. ` +
          `Saw token=${token ? "yes" : "no"} ` +
          `oidc=${process.env.VERCEL_OIDC_TOKEN ? "yes" : "no"} ` +
          `store=${storeId() ?? "none"}`,
      );
  }
  return ok;
}

// Credentials for every call in one place. An explicit storeId beats relying on
// the SDK's env lookup, which only knows the unprefixed name.
const blobAuth = () => {
  const token = blobToken();
  if (token) return { token };
  return storeId() ? { storeId: storeId() } : {};
};

let etag = null; // of the copy we last read or wrote
let reading = null; // in-flight read, so parallel callers share one GET

// Reads the blob EVERY time, not once per instance. It used to latch on a
// `restored` flag, which quietly broke the whole design the moment there was
// more than one serverless instance: the one that happened to run the cron
// generated a post and served it, while an instance that had started earlier —
// and read an empty blob then — kept answering with nothing, forever. Visitors
// saw the feed flicker between one post and none depending on which instance
// took the request. Re-reading is how an instance learns what the others wrote,
// and it is one GET, throttled by the registry's TTL above.
async function restore() {
  if (reading) return reading;
  reading = readState().finally(() => {
    reading = null;
  });
  return reading;
}

async function readState() {
  if (!blobConfigured()) return;
  try {
    const found = await get(STATE_PATH, {
      access: "private",
      useCache: false,
      ...blobAuth(),
    });
    if (!found || found.statusCode !== 200) return;
    const saved = JSON.parse(await new Response(found.stream).text());
    if (saved.version !== STATE_VERSION) return; // shape changed; start fresh
    // get() reports the etag in HTTP weak form — `W/"abc"` — but put()'s
    // ifMatch only accepts the strong form `"abc"`, and treats the mismatch as
    // a precondition failure. So every write conditioned on an etag learned
    // from READING failed, always, while writes conditioned on an etag from a
    // previous WRITE succeeded — which is why one long-lived dev server saved
    // fine and every fresh serverless instance "lost" a race that never
    // happened. Strip the weak marker at the only place a read hands us one.
    etag = found.blob.etag.replace(/^W\//, "");
    // Drop anything already past its life rather than reviving a stale feed.
    const now = Date.now();
    const kept = (saved.threads ?? []).filter(
      (t) => now - t.startedAt <= RETIRE_AFTER,
    );
    const changed = kept.length !== live.length;
    live.length = 0;
    live.push(...kept);
    // FORWARD only. This adopts a window another instance has already used, so
    // two servers do not both post into it — but it must never rewind ours. It
    // used to assign unconditionally, which was harmless while restore() ran
    // once per instance and became a live-lock the moment it ran on every read:
    // a tick would claim the window, the next visitor's read would reset the
    // claim from a blob that had not been updated yet, and the following minute
    // every instance thought it was due again. They generated at once, fought
    // over one etag, and all but one threw the work away.
    if (Number.isInteger(saved.lastWindow) && saved.lastWindow > lastWindow)
      lastWindow = saved.lastWindow;
    // Only when the count moves. This runs on every read now, and a line a
    // minute per instance saying the same number is how a log stops being
    // somewhere you look.
    if (changed)
      console.log(
        `${SUBREDDIT.name}: restored ${kept.length} threads from blob storage`,
      );
  } catch (error) {
    // A store that is unreachable must not take the subreddit down with it.
    console.warn(
      `${SUBREDDIT.name}: could not restore state — ${error.message}`,
    );
  }
}

async function persist() {
  if (!blobConfigured()) return;
  try {
    const saved = await put(
      STATE_PATH,
      JSON.stringify({ version: STATE_VERSION, lastWindow, threads: live }),
      {
        access: "private",
        contentType: "application/json",
        allowOverwrite: true,
        cacheControlMaxAge: 60,
        ...blobAuth(),
        // Refuse the write if somebody saved after our read. First time round
        // there is nothing to match, so the option is simply absent.
        ...(etag ? { ifMatch: etag } : {}),
      },
    );
    etag = saved.etag;
  } catch (error) {
    if (error instanceof BlobPreconditionFailedError) {
      // Another instance wrote after we read. Do NOT throw this tick's work
      // away — the posts in `live` cost real generation calls, and "skipping"
      // here is how a whole evening of posts got paid for and never shown.
      // Merge instead: re-read what won, fold in any thread of ours it lacks,
      // and write once more against the fresh etag. One retry only; two
      // instances cannot both lose the second round with fresh etags, and if
      // something stranger is going on the next tick's merge picks it up.
      console.warn(
        `${SUBREDDIT.name}: another instance saved first — merging over it`,
      );
      const ours = [...live];
      etag = null;
      await restore(); // refreshes both `live` and the etag from the winner
      const have = new Set(live.map((t) => t.id));
      for (const t of ours) if (!have.has(t.id)) live.push(t);
      live.sort((a, b) => b.startedAt - a.startedAt);
      try {
        const again = await put(
          STATE_PATH,
          JSON.stringify({ version: STATE_VERSION, lastWindow, threads: live }),
          {
            access: "private",
            contentType: "application/json",
            allowOverwrite: true,
            cacheControlMaxAge: 60,
            ...blobAuth(),
            ...(etag ? { ifMatch: etag } : {}),
          },
        );
        etag = again.etag;
      } catch (retryError) {
        etag = null;
        console.warn(
          `${SUBREDDIT.name}: merge retry failed — ${retryError.message}`,
        );
      }
      return;
    }
    // Any other failure — the blob deleted underneath us, a transient network
    // error — must drop the etag too. Holding a stale one meant every later
    // write was conditional on a version that no longer existed, so persistence
    // failed silently and permanently once someone cleared the store.
    etag = null;
    console.warn(`${SUBREDDIT.name}: could not save state — ${error.message}`);
  }
}

// One payload shape for both paths, so a read and a write can never disagree
// about what the feed looks like.
function shape(people, written) {
  // Totals are DERIVED on the way out, never stored. The individual votes stay
  // canonical, so a score can always be explained by naming the residents who
  // produced it — and the number on screen cannot drift from the records.
  const scored = live.map((t) => ({
    ...t,
    ...tally(t.votes),
    replies: t.replies.map((r) => ({ ...r, ...tally(r.votes) })),
  }));

  // Everyone who actually spoke, once, with the paragraph they were written
  // from. The panel needs it to say who somebody is when you click their name,
  // and sending it per-post would repeat ~900 characters for every reply.
  const speaking = new Set();
  for (const t of live) {
    speaking.add(t.authorId);
    for (const r of t.replies) speaking.add(r.personaId);
  }
  const speakers = {};
  for (const person of people) {
    if (!speaking.has(person.id)) continue;
    speakers[person.id] = {
      id: person.id,
      name: person.name,
      occupation: person.occupation,
      puma: person.puma,
      neighbourhood: person.neighbourhood,
      persona: person.persona,
      // What kind of day they are having. Sent so the profile card can say it —
      // otherwise the feature is real but invisible, and a mood you cannot see
      // is indistinguishable from the model being inconsistent.
      mood: moodFor(person.id).label,
    };
  }

  return {
    live: true,
    speakers,
    votes: {
      cast: live.reduce(
        (n, t) =>
          n +
          (t.votes?.length ?? 0) +
          t.replies.reduce((m, r) => m + (r.votes?.length ?? 0), 0),
        0,
      ),
    },
    community: SUBREDDIT.name,
    goal: SUBREDDIT.goal,
    rules: SUBREDDIT.rules,
    model: MODEL,
    cast: people.length,
    written,
    threads: scored,
  };
}

// What a visitor gets: whatever has been written, restored from the blob if this
// instance is cold. It NEVER generates. A cold build is roughly 160 language-model
// round trips and a serverless function has sixty seconds, so asking a visitor to
// trigger one produced FUNCTION_INVOCATION_TIMEOUT in production — on the request
// of the first person to arrive. Writing belongs on the cron.
export async function readSubreddit() {
  await restore();
  const people = await loadCast();
  const now = Date.now();
  for (let i = live.length - 1; i >= 0; i--) {
    if (now - live[i].startedAt > RETIRE_AFTER) live.splice(i, 1);
  }
  live.sort((a, b) => b.startedAt - a.startedAt);
  return shape(people, 0);
}

export async function advanceSubreddit() {
  await restore();
  const people = await loadCast();
  if (!people.length)
    throw new Error("personas.json has no people with a paragraph");

  const now = Date.now();
  // Every invocation gets the SAME small allowance, including the first. A
  // serverless function has a fixed budget of wall-clock and each generation is
  // a round trip, so any opening build big enough to be worth watching cannot
  // fit and must not be attempted. The feed accumulates one post a window from
  // whatever it already holds — slower to watch on day one, and the only
  // version that completes.
  const allowance = MAX_MESSAGES_PER_REFRESH;
  let budget = allowance;
  let failures = 0;
  // One accountant for the whole refresh. Returns false when the allowance is
  // gone, which is how a thread's continuation loop learns to stop without
  // knowing anything about budgets.
  const spend = () => (budget > 0 ? (budget--, true) : false);
  // Voting gets its own allowance so a busy tick cannot quietly spend the
  // generation budget on opinions about posts that were never written.
  let voteBudget = MAX_VOTES_PER_REFRESH;
  const spendVote = () => (voteBudget > 0 ? (voteBudget--, true) : false);

  // Threads leave on age alone. Evicting a finished conversation to make room
  // seems tidy and is not — a long argument gets replaced by somebody's opening
  // line and the panel visibly loses posts. The column scrolls; it has room.
  for (let i = live.length - 1; i >= 0; i--) {
    if (now - live[i].startedAt > RETIRE_AFTER) live.splice(i, 1);
  }

  // Any thread the budget cut short last time resumes before anything new is
  // started: finishing a conversation beats beginning one.
  for (const thread of live.filter((t) => !t.done)) {
    if (budget <= 0) break;
    try {
      await growThread(people, thread, spend, spendVote);
    } catch (error) {
      failures++;
      console.warn(`${SUBREDDIT.name}: reply failed — ${error.message}`);
      if (failures > 6) break;
    }
  }

  const wanted = NEW_THREADS_PER_REFRESH;
  for (let i = 0; i < wanted && budget > 0 && live.length < MAX_THREADS; i++) {
    if (!spend()) break;
    let thread;
    try {
      thread = await openThread(people, spendVote);
    } catch (error) {
      failures++;
      console.warn(`${SUBREDDIT.name}: post failed — ${error.message}`);
      if (failures > 3) break;
      continue;
    }
    live.push(thread);
    // Straight into its own continuation loop, so a post and its discussion
    // arrive together rather than the post sitting alone until the next tick.
    try {
      await growThread(people, thread, spend, spendVote);
    } catch (error) {
      failures++;
      console.warn(`${SUBREDDIT.name}: reply failed — ${error.message}`);
      if (failures > 6) break;
    }
  }

  // Nothing at all written on a cold start IS a real failure — throw, and the
  // registry serves last-good or `empty` rather than an empty subreddit.
  if (!live.length)
    throw new Error("every generation failed — nothing to serve");

  live.sort((a, b) => b.startedAt - a.startedAt);
  await persist();
  return shape(people, allowance - budget);
}

// ------------------------------------------------------ the human's own post
//
// One person from outside the simulation can post into it. Everything AFTER the
// submission is the machinery the residents already live under: the accepted
// post is an ordinary thread, so the same sampled voters judge it and the same
// continuation loop decides whether anybody answers — no special path, which is
// the only way the reaction to it means anything.
//
// The door in front of it is one grading call against the community's own goal
// and rules. The residents are held to those rules by having them in every
// prompt they write from; a submission nobody wrote a persona for has to be held
// to them explicitly, and this is where that happens.

const HUMAN = {
  id: "human-person",
  name: "Human Person",
  // The spec's limits, and shorter than the residents' own title allowance on
  // purpose: a headline somebody types should read like one.
  maxChars: { title: 80, body: 240 },
  // Below this the post does not land. This is the whole product decision of
  // the feature, so it is stated once, here.
  passingScore: 70,
  // Replies a visitor is guaranteed, written before the response comes back so
  // they see the room react rather than an empty thread. Two, because one reads
  // as a courtesy and three is a crowd nobody earned.
  minReplies: 2,
};

export const humanLimits = () => ({ ...HUMAN.maxChars });

// Rejected before a single token is spent: length and emptiness are facts, not
// judgements, and the client enforces the same numbers so this only ever fires
// on a request that did not come from it.
export function validateSubmission({ title, body } = {}) {
  const clean = (value) =>
    String(value ?? "")
      .replace(/\s+/g, " ")
      .trim();
  const t = clean(title);
  const b = clean(body);
  if (!t) return { error: "Write a header before posting." };
  if (!b) return { error: "Write some body text before posting." };
  if (t.length > HUMAN.maxChars.title)
    return {
      error: `The header must be ${HUMAN.maxChars.title} characters or fewer.`,
    };
  if (b.length > HUMAN.maxChars.body)
    return {
      error: `The body must be ${HUMAN.maxChars.body} characters or fewer.`,
    };
  return { title: t, body: b };
}

// One call, one number, and a sentence the author can read. Alignment ONLY —
// the score is not a review of the writing, and a dull post about a bus stop is
// as aligned as a good one about a bus stop.
export async function gradeSubmission({ title, body }) {
  const system =
    `You are the moderator of ${SUBREDDIT.name}, a subreddit about San Francisco.\n\n` +
    `SUBREDDIT GOAL\n${SUBREDDIT.goal}\n\n` +
    `SUBREDDIT RULES\n${rulesBlock()}`;
  const user =
    `A person has submitted this post to the community.\n\n` +
    `TITLE\n${title}\n\n` +
    `BODY\n${body}\n\n` +
    `Score from 0 to 100 how well the title AND the body TOGETHER are aligned with the subreddit's stated goal and its rules.\n\n` +
    `Judge alignment only — not the writing quality, not whether you agree with it, not how interesting it is.\n\n` +
    `- 100: squarely about news, events, politics, culture, or everyday life in San Francisco, and breaks no rule.\n` +
    `- 70: genuinely relevant to San Francisco and breaks no rule, even if it is small, mundane, or narrow.\n` +
    `- below 70: not really about San Francisco, or it breaks a rule — intolerant, insulting, hateful, threatening, crude, slanderous, an unsourced criminal allegation against a private individual — or it is spam, advertising, or nonsense.\n` +
    `- 0: no relationship to San Francisco at all, or it is abusive.\n\n` +
    `Both parts count: a San Francisco title over an unrelated body is not aligned.\n\n` +
    `Then write ONE sentence for the author, addressed to them, saying why it scored that.\n\n` +
    `Return JSON:\n{ "score": 0, "reason": "..." }`;

  const raw = parseJson(await complete(system, user, 200));
  const value = Number(raw.score);
  if (!Number.isFinite(value)) throw new Error("grader returned no score");
  const score = Math.min(100, Math.max(0, Math.round(value)));
  const reason = String(raw.reason ?? "")
    .replace(/\s+/g, " ")
    .trim()
    .slice(0, 240);
  return { score, reason, passed: score >= HUMAN.passingScore };
}

// Grade, then — only if it passed — write it into the same store the residents'
// posts live in, with its first votes already cast so the next tick can see
// what the room made of it and decide whether to reply.
export async function submitHumanPost({ title, body }) {
  const checked = validateSubmission({ title, body });
  if (checked.error) return { status: 400, body: { error: checked.error } };

  const { score, reason, passed } = await gradeSubmission(checked);
  if (!passed)
    return {
      status: 200,
      body: { posted: false, score, threshold: HUMAN.passingScore, reason },
    };

  await restore();
  const people = await loadCast();
  // The same sample size a resident's post gets, on its own small allowance:
  // this is one post, not a tick, and it must not be able to spend a tick's
  // budget.
  let voteBudget = votingConfig.postVoterSampleSize;
  const spendVote = () => (voteBudget > 0 ? (voteBudget--, true) : false);
  const votes = await simulateVotes({
    cast: people,
    authorId: HUMAN.id,
    content: `${checked.title}\n\n${checked.body}`,
    size: votingConfig.postVoterSampleSize,
    spend: spendVote,
  });

  const at = Date.now();
  const thread = {
    id: `${HUMAN.id}-${at}`,
    authorId: HUMAN.id,
    // No occupation and no PUMA, because this person genuinely has neither in
    // this city — inventing them would put a fake resident in the panel beside
    // real ones. `human` is what the panel labels instead.
    author: { name: HUMAN.name, occupation: null, puma: null },
    human: true,
    title: checked.title,
    body: checked.body,
    votes,
    replies: [],
    replyProbability: sampleReplyProbability(),
    done: false,
    startedAt: at,
    at,
  };
  live.push(thread);

  // Answer them NOW rather than at the next tick. Left for the tick, a visitor
  // watched their own post sit in silence for up to ten minutes and reasonably
  // concluded the city had ignored them. This spends its own small allowance,
  // separate from a tick's, so one post can never eat the budget a whole
  // window is meant to cover.
  // Exactly the floor, not a reply more. Everything above it is the tick's
  // work, earned by the score — and every extra reply written here is another
  // few seconds the person sits watching a spinner having already typed.
  let replyBudget = HUMAN.minReplies;
  try {
    await growThread(
      people,
      thread,
      () => (replyBudget > 0 ? (replyBudget--, true) : false),
      // No voting on these two. It is three more model calls per reply and the
      // person is waiting on every one of them — and a reply's score is display
      // only: moods and who may speak are read from the POST's votes, never a
      // reply's. They start unscored, exactly like any reply nobody voted on.
      () => false,
    );
  } catch (error) {
    // A failed reply must not cost them the post itself — it is written, it is
    // theirs, and the next tick will grow it the way it grows any thread that
    // ran out of budget.
    thread.done = false;
    console.warn(
      `${SUBREDDIT.name}: human post replies failed — ${error.message}`,
    );
  }

  live.sort((a, b) => b.startedAt - a.startedAt);
  await persist();

  const payload = shape(people, 0);
  return {
    status: 200,
    body: {
      posted: true,
      score,
      threshold: HUMAN.passingScore,
      reason,
      id: thread.id,
      // The whole feed, with their post at the top of it and its first replies
      // already under it. Sent back in the RESPONSE rather than left for the
      // client to go and fetch, because /api/feed is served through a CDN with
      // a thirty-second window and stale-while-revalidate behind it — a reader
      // refreshing the instant they post is exactly who gets handed an edge
      // copy from before their post existed. This cannot be stale: it is the
      // object their own submission just produced.
      feed: payload,
    },
    // Also published into the registry so this instance serves it too.
    payload,
  };
}

registerFeed("feed", {
  // Reads are one blob GET, so they can be frequent. They have to be: the tick
  // that wrote the new post may have run on a different serverless instance
  // than the one answering this visitor, and the only way that instance learns
  // about it is by re-reading. A ten-minute TTL here would hide a fresh post
  // for ten more minutes.
  ttl: READ_TTL_MS,
  fetcher: readSubreddit,
  empty: { live: false, threads: [] },
  describe: `${SUBREDDIT.name} — what the residents are posting today`,
  // A generation takes a while and costs money: do not retry a broken gateway
  // every thirty seconds, and keep serving the last conversation for an hour
  // rather than blanking the panel over one bad refresh.
  backoffMs: 5 * 60_000,
  staleMs: 60 * 60_000,
});
