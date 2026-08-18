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
  goal:
    "people who actually live in San Francisco talking about what they notice in " +
    "their own neighbourhood — what they saw, what it costs them, what they think " +
    "is going to happen, what they are glad about and what they are sick of",
  rules: [],
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

const OPENING_THREADS = 8; // how many posts a cold start puts up
// A thread is finished the moment its roll fails, so nothing new would ever
// appear without new posts. Every refresh starts a couple.
const NEW_THREADS_PER_REFRESH = 2;
const RETIRE_AFTER = 24 * 60 * 60 * 1000;
const MAX_THREADS = 50; // backstop, not a design limit
const REFRESH_MS = 30 * 60 * 1000;
// The budget rail. Everything else here is taste; this is the line that stops a
// bad day costing real money.
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

export async function generatePost({ persona, subreddit }) {
  const system =
    `You are simulating a person posting in a subreddit.\n\n` +
    `PERSONA\n${persona.persona}\n\n` +
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
    `Return JSON:\n{ "title": "...", "body": "..." }`;

  const { title, body } = parseJson(await complete(system, user, 700));
  if (!title || !body)
    throw new Error("post came back without a title or body");
  return { title: String(title).trim(), body: String(body).trim() };
}

export async function generateReply({ persona, subreddit, post, replies }) {
  const system =
    `You are simulating a person participating in a Reddit discussion.\n\n` +
    `PERSONA\n${persona.persona}\n\n` +
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
  const user =
    `DISCUSSION\n\n` +
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
    `Return JSON:\n{ "body": "..." }`;

  const { body } = parseJson(await complete(system, user, 400));
  if (!body) throw new Error("reply came back without a body");
  return { body: String(body).trim() };
}

// --------------------------------------------------------------- who speaks

const pick = (list) => list[Math.floor(Math.random() * list.length)];

// Selection stays out of the model. Half the time somebody new walks in, half
// the time somebody already arguing comes back — that mix is what makes a
// thread read as a conversation rather than a row of strangers. Nobody follows
// themselves; the original poster may return later.
function pickResponder(cast, thread) {
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

async function openThread(people) {
  const author = pick(people);
  const post = await generatePost({ persona: author, subreddit: SUBREDDIT });
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
async function growThread(people, thread, spend) {
  while (
    thread.replies.length < simulationConfig.maxReplies &&
    Math.random() < thread.replyProbability
  ) {
    if (!spend()) return;
    if (!(await addReply(people, thread))) break;
  }
  thread.done = true;
}

async function addReply(people, thread) {
  const responder = pickResponder(people, thread);
  if (!responder) return false;
  const { body } = await generateReply({
    persona: responder,
    subreddit: SUBREDDIT,
    post: {
      title: thread.title,
      body: thread.body,
      author: thread.author.name,
      authorId: thread.authorId,
    },
    replies: thread.replies,
  });
  thread.replies.push({
    personaId: responder.id,
    name: responder.name,
    occupation: responder.occupation,
    puma: responder.puma,
    body,
    at: Date.now(),
  });
  return true;
}

async function fetchSubreddit() {
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
      await growThread(people, thread, spend);
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
      thread = await openThread(people);
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
      await growThread(people, thread, spend);
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
  return {
    live: true,
    community: SUBREDDIT.name,
    goal: SUBREDDIT.goal,
    model: MODEL,
    cast: people.length,
    written: allowance - budget,
    threads: live,
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
