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
const MAX_CHARS = 180;

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
  const system =
    `You write a single message for a neighbourhood social feed in San Francisco. ` +
    `You are writing AS this person, in their own words.\n\n` +
    `WHO YOU ARE\n${speaker.iss}\n\n` +
    `RULES\n` +
    `- Under ${MAX_CHARS} characters. One or two sentences.\n` +
    `- Write only the message. No name, no quotation marks, no hashtags, no emoji.\n` +
    `- Speak from your own life. Do not describe yourself in the third person.\n` +
    `- You are a neighbour, not a spokesperson. Be specific, partial and ordinary.\n` +
    `- Never mention being an AI, a persona, or the Census.`;

  const thread = posts.length
    ? `\n\nTHE CONVERSATION SO FAR\n${posts.map((p) => `${p.name}: ${p.text}`).join("\n")}`
    : "";
  const why = grounding ? `\n\nWHY THIS REACHES YOU\n${grounding}` : "";
  const user =
    `WHAT HAPPENED (${event.source}, ${event.where})\n${event.headline}${event.detail ? `\n${event.detail}` : ""}` +
    why +
    thread +
    `\n\n${posts.length ? "Reply to this conversation." : "Post about this."}`;

  const res = await fetch(ENDPOINT, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${credential}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      model: MODEL,
      temperature: TEMPERATURE,
      max_tokens: 120,
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
  // Models like to open with the speaker's own name however firmly you ask them
  // not to. Cheaper to take it off here than to argue in the prompt.
  return text
    .replace(/^["'“]|["'”]$/g, "")
    .replace(new RegExp(`^${speaker.name.split(" ")[0]}\\s*[:,-]\\s*`, "i"), "")
    .slice(0, MAX_CHARS + 40)
    .trim();
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
    thread.posts.push({
      id: slot.id,
      speakerId: speaker.id,
      name: speaker.name,
      occupation: speaker.occupation,
      puma: speaker.puma,
      text: await write({
        speaker,
        event: thread.event,
        because: slot.because,
        posts: [],
      }),
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
      thread.posts.push({
        id: slot.id,
        speakerId: speaker.id,
        name: speaker.name,
        occupation: speaker.occupation,
        puma: speaker.puma,
        text: await write({
          speaker,
          event: thread.event,
          because: slot.because,
          posts: thread.posts,
        }),
        at: Date.now(),
      });
      thread.cursor++;
      budget--;
    }
  }

  return {
    live: true,
    day: data.label,
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
