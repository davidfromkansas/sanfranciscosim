// The residents' feed: real San Franciscans, sampled from 2024 ACS PUMS
// microdata and written up as characters, talking about real city events.
//
// The method is Social Simulacra's (arXiv 2208.04024), with the parts that
// belong in code kept OUT of the model:
//
//   * ONE MESSAGE AT A TIME. Never a whole thread in one call. Generating a
//     thread at once is what makes every voice in it converge on the same one.
//     Each call sees the writer's identity paragraph, the event, and the
//     conversation so far — and returns a single line.
//   * WHO SPEAKS is decided offline, from the Census. `feed-seed.json` already
//     fixes the cast and the running order; the model never picks a speaker,
//     so it can never hand the daycare argument to the retired security guard.
//   * REPLIES ARE A COIN FLIP, ~0.65 a round, and a thread stops at 8. Both
//     from the paper. In code, because it is arithmetic, not judgement.
//   * NO REASONING. This is a voice task: there is nothing to work out, and a
//     model that deliberates first writes a considered summary of what a
//     person might say rather than the thing they would actually post.
//
// The feed EXTENDS rather than rebuilds. A rebuild every half hour would delete
// the conversation you were reading mid-sentence, and cost seven times more.
//
// Without AI_GATEWAY_API_KEY this throws and the registry serves `empty` — the
// panel then says the neighbours are quiet. The city itself never needs a key.

import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { registerFeed } from "../feedcore.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const SEED = path.resolve(HERE, "../../_data/feed-seed.json");

const ENDPOINT = "https://ai-gateway.vercel.sh/v1/chat/completions";
// Chosen for what it is NOT: the only large open-weight model in its price band
// that is not a reasoning model. ~$3.50/month at this refresh rate; Sonnet
// would be ~$29. See the model note in the PR.
const MODEL = "deepseek/deepseek-v3.2";
const TEMPERATURE = 0.85;
const MAX_CHARS = 180; // a reply
const TITLE_CHARS = 100; // the headline a resident writes over their own post
const BODY_CHARS = 240; // what they write under it

// The community, in Social Simulacra's terms (arXiv 2208.04024 §4). The paper
// takes a GOAL and RULES from the designer and puts them in every prompt, and
// is specific that a goal which is too broad produces off-topic writing — their
// "UIST warriors" wandered until it became "a place for UIST warriors to
// support each other as they finish writing their papers".
//
// So the goal here is written from a MEMBER's side. The design intent — making
// Sim Francisco feel like a living city — is ours and stays out of the prompt:
// nobody posts to a subreddit in order to make a city feel alive, and a
// resident told that is being told they are a simulation.
//
// Rules are nudges, not enforcement, and the paper states them as things to
// avoid. Change either of these and the whole feed changes character — that is
// the point of them, and the cheapest experiment available here.
const COMMUNITY = {
  name: "r/simfrancisco",
  goal:
    "people who actually live in San Francisco talking about what they notice in " +
    "their own neighbourhood — what they saw, what it costs them, what they think " +
    "is going to happen, what they are glad about and what they are sick of",
  avoid: [
    "sounding like a news report or a press release",
    "speaking for the city or for a group rather than yourself",
    "advertising anything",
    "attacking the person rather than what they said",
  ],
};

const REPLY_CHANCE = 0.65;
const MAX_REPLIES = 8;
const LIVE_THREADS = 8; // how many conversations are on screen at once
const RETIRE_AFTER = 6 * 60 * 60 * 1000;

// The budget rail. Everything else in this file is taste; this is the line that
// stops a bad day costing real money. At ~$0.0003 a message this caps one
// refresh at under a cent, and a month of half-hourly refreshes near $4.
const MAX_MESSAGES_PER_REFRESH = 10;
// The first build is a different problem from the ones after it. Ten messages
// spread over six new conversations is one opening post and a handful of
// replies — technically a feed, but it reads as though the neighbourhood has
// nothing to say. A cold start therefore gets a bigger allowance, once, to
// arrive at something worth reading; every refresh after that is incremental.
// ~1 cent, and only on a cold instance.
const FIRST_BUILD_MESSAGES = 34;

const REFRESH_MS = 30 * 60 * 1000;

let seed = null;
async function loadSeed() {
  seed ??= JSON.parse(await readFile(SEED, "utf8"));
  return seed;
}

// Conversation state, held in memory. Per the registry's own accepted limits
// this dies on a cold start and the feed begins again — acceptable, because a
// fresh instance produces a real feed rather than a broken one.
const live = []; // { id, event, slots, cursor, posts: [{ id, speaker, text, at }], startedAt }
let nextThread = 0;

function pick(list) {
  return list[Math.floor(Math.random() * list.length)];
}

async function write({ speaker, event, because, posts }) {
  // The gateway takes either a key or the project's OIDC token. The token is
  // what `vercel env pull` writes for local development, so a linked checkout
  // runs the real writer without a production secret ever landing on a laptop.
  // It is short-lived; re-run the pull when it expires.
  const credential =
    process.env.AI_GATEWAY_API_KEY || process.env.VERCEL_OIDC_TOKEN;
  if (!credential)
    throw new Error(
      "no AI_GATEWAY_API_KEY or VERCEL_OIDC_TOKEN — feed offline",
    );

  const grounding = because
    .filter((b) => b.fact)
    .map((b) => `- ${b.topic}: ${b.fact}`)
    .join("\n");

  // The transcript, in the paper's shape: who is writing, what happened, what
  // has been said. Nothing else — every extra instruction here is a nudge
  // toward a generic internet voice, which is the failure mode.
  // Order follows the paper: who you are, then how this place behaves, then
  // what it is for. The persona comes first because everything after it is
  // read as constraints on that voice rather than as a character brief.
  // An opening post and a reply are different acts of writing. Opening one is
  // deciding a thing is worth other people's attention and giving it a title;
  // replying is answering what somebody said. The shared rules stay identical
  // so the voice does not change between them.
  const opening = posts.length === 0;
  const common =
    `WHO YOU ARE\n${speaker.iss}\n\n` +
    `WHERE YOU ARE POSTING\n` +
    `${COMMUNITY.name} — ${COMMUNITY.goal}.\n` +
    `People here avoid ${COMMUNITY.avoid.join("; ")}.\n\n`;
  const manners =
    `- Speak from your own life, in the first person.\n` +
    `- You are a neighbour, not a spokesperson. Be specific, partial and ordinary.\n` +
    `- No quotation marks, no hashtags, no emoji, no name.\n` +
    `- Never mention being an AI, a persona, or the Census.`;
  const system = opening
    ? common +
      `HOW TO WRITE\n` +
      `You are starting a thread. Answer on exactly two lines:\n` +
      `TITLE: what you would call this post — under ${TITLE_CHARS} characters. Say the thing, do not repeat the news headline back.\n` +
      `BODY: what you actually want to say about it — under ${BODY_CHARS} characters, two or three sentences.\n` +
      manners
    : common +
      `HOW TO WRITE\n` +
      `- Under ${MAX_CHARS} characters. One or two sentences.\n` +
      `- Write only the message.\n` +
      manners;

  const thread = posts.length
    ? `\n\nTHE CONVERSATION SO FAR\n${posts.map((p) => `${p.name}: ${p.title ? `${p.title} — ` : ""}${p.text}`).join("\n")}`
    : "";
  const why = grounding ? `\n\nWHY THIS REACHES YOU\n${grounding}` : "";
  const user =
    `WHAT HAPPENED (${event.source}, ${event.where})\n${event.headline}${event.detail ? `\n${event.detail}` : ""}` +
    why +
    thread +
    `\n\n${opening ? "Start the thread." : "Reply to this conversation."}`;

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${credential}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      temperature: TEMPERATURE,
      max_tokens: opening ? 220 : 120,
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
  const raw = (body.choices?.[0]?.message?.content ?? "").trim();
  if (!raw) throw new Error("gateway returned an empty message");

  // Models like to open with the speaker's own name however firmly you ask them
  // not to. Cheaper to take it off here than to argue in the prompt.
  // Cut at a sentence, never mid-word. A hard character slice left posts
  // ending "takes more than a stripe to slow down" — which reads as a bug, not
  // as brevity. Prefer the last full sentence inside the limit; failing that,
  // the last whole word.
  const tidy = (t, limit) => {
    const clean = t
      .replace(/^\*\*|\*\*$/g, "")
      .replace(/^["'“]|["'”]$/g, "")
      .replace(
        new RegExp(`^${speaker.name.split(" ")[0]}\\s*[:,-]\\s*`, "i"),
        "",
      )
      .trim();
    if (clean.length <= limit) return clean;
    const window = clean.slice(0, limit);
    const sentence = Math.max(
      window.lastIndexOf(". "),
      window.lastIndexOf("! "),
      window.lastIndexOf("? "),
    );
    // Only honour a sentence break if it leaves a post worth reading; a title
    // cut to four words because the first sentence was short is worse.
    if (sentence > limit * 0.5) return window.slice(0, sentence + 1).trim();
    if (/[.!?]$/.test(window)) return window.trim();
    const word = window.lastIndexOf(" ");
    return (
      (word > 0 ? window.slice(0, word) : window)
        .trim()
        .replace(/[,;:—-]$/, "") + "…"
    );
  };

  if (!opening) return { text: tidy(raw, MAX_CHARS) };

  // TITLE:/BODY: rather than JSON — one fewer thing for a cheap model to get
  // wrong, and a miss degrades to a post with no title rather than an error.
  const title =
    raw.match(/^\s*(?:\*\*)?TITLE(?:\*\*)?\s*:\s*(.+)$/im)?.[1] ?? "";
  const rest =
    raw.match(/(?:\*\*)?BODY(?:\*\*)?\s*:\s*([\s\S]+)$/im)?.[1] ?? "";
  if (!title || !rest) {
    // No labels came back. Treat the first line as the title only if it reads
    // like one — short, and with a body behind it. Otherwise it is just a post.
    const lines = raw
      .split("\n")
      .map((l) => l.trim())
      .filter(Boolean);
    if (lines.length > 1 && lines[0].length <= TITLE_CHARS) {
      return {
        title: tidy(lines[0], TITLE_CHARS),
        text: tidy(lines.slice(1).join(" "), BODY_CHARS),
      };
    }
    return { text: tidy(raw, BODY_CHARS) };
  }
  return {
    title: tidy(title, TITLE_CHARS),
    text: tidy(rest.replace(/\s+/g, " "), BODY_CHARS),
  };
}

async function fetchResidents() {
  const data = await loadSeed();
  if (!data.threads.length) throw new Error("feed-seed.json has no threads");

  const now = Date.now();
  const cold = live.length === 0;
  let budget = cold ? FIRST_BUILD_MESSAGES : MAX_MESSAGES_PER_REFRESH;

  // Threads leave on AGE ALONE. Evicting a finished conversation to make room
  // for a new one seems tidy and is not: a seven-post argument is replaced by
  // somebody's opening line, and the panel visibly loses posts between
  // refreshes. The column scrolls, so it does not need the room — a finished
  // conversation is still worth reading, and it goes when it is genuinely old.
  for (let i = live.length - 1; i >= 0; i--) {
    if (now - live[i].startedAt > RETIRE_AFTER) live.splice(i, 1);
  }

  // Open new conversations up to the on-screen count.
  while (live.length < LIVE_THREADS && budget > 0) {
    const source = data.threads[nextThread % data.threads.length];
    nextThread++;
    const thread = { ...source, cursor: 0, posts: [], startedAt: now };
    const slot = thread.slots[0];
    const speaker = data.speakers[slot.speaker];
    // The opening post carries a title of its own; the spread puts it on the
    // post only when the writer produced one.
    const written = await write({
      speaker,
      event: thread.event,
      because: slot.because,
      posts: [],
    });
    thread.posts.push({
      id: slot.id,
      speakerId: speaker.id,
      name: speaker.name,
      occupation: speaker.occupation,
      puma: speaker.puma,
      ...written,
      at: Date.now(),
    });
    thread.cursor = 1;
    budget--;
    live.push(thread);
  }

  // Extend the ones already running. A coin flip per thread per refresh, which
  // is what keeps some conversations busy and others one lonely post. A cold
  // build goes round more than once: a single pass of coin flips over six
  // threads cannot spend an opening allowance, and the flips still decide
  // WHICH conversations get deep rather than levelling them all.
  const passes = cold ? MAX_REPLIES : 1;
  for (let pass = 0; pass < passes && budget > 0; pass++) {
    for (const thread of live) {
      if (budget <= 0) break;
      if (thread.cursor >= thread.slots.length) continue;
      if (thread.posts.length > MAX_REPLIES) continue;
      if (Math.random() > REPLY_CHANCE) continue;
      const slot = thread.slots[thread.cursor];
      const speaker = data.speakers[slot.speaker];
      if (!speaker) {
        thread.cursor++;
        continue;
      }
      const written = await write({
        speaker,
        event: thread.event,
        because: slot.because,
        posts: thread.posts,
      });
      thread.posts.push({
        id: slot.id,
        speakerId: speaker.id,
        name: speaker.name,
        occupation: speaker.occupation,
        puma: speaker.puma,
        ...written,
        at: Date.now(),
      });
      thread.cursor++;
      budget--;
    }
  }

  return {
    live: true,
    day: data.label,
    community: COMMUNITY.name,
    goal: COMMUNITY.goal,
    model: MODEL,
    written: (cold ? FIRST_BUILD_MESSAGES : MAX_MESSAGES_PER_REFRESH) - budget,
    threads: live.map((t) => ({ id: t.id, event: t.event, posts: t.posts })),
  };
}

registerFeed("feed", {
  ttl: REFRESH_MS,
  fetcher: fetchResidents,
  empty: { live: false, threads: [] },
  describe: "what the residents are saying about today’s city events",
  // A generation takes a while and costs money; do not retry a broken gateway
  // every thirty seconds, and keep serving the last conversation for an hour
  // rather than blanking the panel over one bad refresh.
  backoffMs: 5 * 60_000,
  staleMs: 60 * 60_000,
});
