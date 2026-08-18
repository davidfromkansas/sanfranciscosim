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
// A cold start writes eight posts and twenty-odd replies at once and needs
// about a hundred votes to cover them. Rationing it to a normal tick left most
// of the subreddit sitting at zero, which reads as broken rather than as quiet.
// One-off, and about two cents.
const FIRST_BUILD_VOTES = 130;

const OPENING_THREADS = 8; // how many posts a cold start puts up, so a fresh
// deploy is a subreddit rather than one lonely thread
// Then ONE post every tick, with whatever replies its own probability earns it.
// A thread is finished the moment its roll fails, so new posts are the only
// thing that keeps the feed moving.
const NEW_THREADS_PER_REFRESH = 1;
const RETIRE_AFTER = 24 * 60 * 60 * 1000;
// A day at one post every ten minutes is 144 threads, so a 50-thread cap would
// have filled in eight hours and then silently stopped the subreddit — new
// posts blocked, nothing retiring for another sixteen. The cap has to be a
// backstop against runaway generation, not a limit the normal rate walks into.
const MAX_THREADS = 200;
const REFRESH_MS = 10 * 60 * 1000;
// The budget rail. Everything else here is taste; this is the line that stops a
// bad day costing real money. Ten covers the worst case for one tick — a post
// whose probability earns it the full eight replies, plus a spare for resuming
// a thread the previous tick cut short. The average tick spends about three.
const MAX_MESSAGES_PER_REFRESH = 10;
const FIRST_BUILD_MESSAGES = 34;

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
    `${livesIn(persona)}\n\n` +
    `SUBREDDIT GOAL\n${subreddit.goal}\n\n` +
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
    `${livesIn(persona)}\n\n` +
    `SUBREDDIT GOAL\n${subreddit.goal}\n\n` +
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
    `${livesIn(persona)}\n\n` +
    `SUBREDDIT GOAL\n${subreddit.goal}\n\n` +
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
  if (mood === "negative") {
    const down = votersOf(cast, thread, -1);
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

// Threads live in memory. Per the registry's own accepted limits this dies on a
// cold start and the subreddit begins again — acceptable, because a fresh
// instance produces a real feed rather than a broken one.
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
  // Nobody voted, so nobody cared. The post stands on its own and the thread is
  // finished before it starts — which is most of what a real subreddit is, and
  // costs nothing to render.
  if (mood === "ignored") {
    thread.done = true;
    return;
  }
  // Score decides WHETHER a thread happens and WHO is in it; the thread's own
  // probability still decides HOW LONG it runs. The paper's continuation loop
  // is untouched — it just no longer runs on posts nobody looked at.
  while (
    thread.replies.length < simulationConfig.maxReplies &&
    Math.random() < thread.replyProbability
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

const blobConfigured = () =>
  Boolean(
    process.env.BLOB_READ_WRITE_TOKEN ||
    (process.env.VERCEL_OIDC_TOKEN && storeId()),
  );

// Credentials for every call in one place. An explicit storeId beats relying on
// the SDK's env lookup, which only knows the unprefixed name.
const blobAuth = () => (storeId() ? { storeId: storeId() } : {});

let etag = null; // of the copy we last read or wrote
let restored = false;

async function restore() {
  if (restored) return;
  restored = true;
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
    etag = found.blob.etag;
    // Drop anything already past its life rather than reviving a stale feed.
    const now = Date.now();
    const kept = (saved.threads ?? []).filter(
      (t) => now - t.startedAt <= RETIRE_AFTER,
    );
    live.length = 0;
    live.push(...kept);
    if (Number.isInteger(saved.lastWindow)) lastWindow = saved.lastWindow;
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
      // Another instance got there first. Theirs stands; ours is dropped, and
      // the next cold start will read whatever won.
      console.warn(
        `${SUBREDDIT.name}: another instance saved first — skipping`,
      );
      etag = null;
      return;
    }
    console.warn(`${SUBREDDIT.name}: could not save state — ${error.message}`);
  }
}

async function fetchSubreddit() {
  await restore();
  const people = await loadCast();
  if (!people.length)
    throw new Error("personas.json has no people with a paragraph");

  const now = Date.now();
  const cold = live.length === 0;
  const allowance = cold ? FIRST_BUILD_MESSAGES : MAX_MESSAGES_PER_REFRESH;
  let budget = allowance;
  let failures = 0;
  // One accountant for the whole refresh. Returns false when the allowance is
  // gone, which is how a thread's continuation loop learns to stop without
  // knowing anything about budgets.
  const spend = () => (budget > 0 ? (budget--, true) : false);
  // Voting gets its own allowance so a busy tick cannot quietly spend the
  // generation budget on opinions about posts that were never written.
  let voteBudget = cold ? FIRST_BUILD_VOTES : MAX_VOTES_PER_REFRESH;
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

  const wanted = cold ? OPENING_THREADS : NEW_THREADS_PER_REFRESH;
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
  // Bounded by how many people are on screen, not by the size of the cast.
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
    // The rules verbatim, so the panel shows exactly what every resident is
    // told when they write. Empty today; populate the array and both the
    // prompts and this list pick it up with no other change.
    rules: SUBREDDIT.rules,
    model: MODEL,
    cast: people.length,
    written: allowance - budget,
    threads: scored,
  };
}

registerFeed("feed", {
  ttl: REFRESH_MS,
  fetcher: fetchSubreddit,
  empty: { live: false, threads: [] },
  describe: `${SUBREDDIT.name} — what the residents are posting today`,
  // A generation takes a while and costs money: do not retry a broken gateway
  // every thirty seconds, and keep serving the last conversation for an hour
  // rather than blanking the panel over one bad refresh.
  backoffMs: 5 * 60_000,
  staleMs: 60 * 60_000,
});
