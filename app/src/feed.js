// The residents' feed panel. Reads /api/feed and renders what the neighbours
// are saying about today's real city events.
//
// Every name here is a person walking the streets outside the panel — same id,
// same neighbourhood, same colour dot as their sphere in the diorama. That is
// the whole point of the column: the city and the conversation are the same
// people, not two datasets that happen to share a window.
//
// The endpoint returns `{ live: false, threads: [] }` whenever the writer is
// offline (no key, or a bad refresh past its stale horizon). The panel then
// says so plainly rather than inventing filler — the same contract the ferry
// and Muni layers keep.

const ENDPOINT = `${import.meta.env.BASE_URL}api/feed`;
// The server rebuilds every 30 minutes; polling a touch more often than that
// means a viewer who leaves the tab open sees the new posts without a reload,
// and the CDN absorbs the checks in between.
const POLL_MS = 5 * 60 * 1000;

// Matches the PUMA tints on the spheres in population.js, so the dot beside a
// name is the colour of that person out in the city.
const PUMA_COLORS = {
  "07507": "#d9762f",
  "07508": "#3f8f6b",
  "07509": "#c8442f",
  "07510": "#4a6bb5",
  "07511": "#8a5bb0",
  "07512": "#2f8fa8",
  "07513": "#b0873a",
  "07514": "#c4508c",
};
const PUMA_NAMES = {
  "07507": "Bayview & Hunters Point",
  "07508": "Richmond & Presidio",
  "07509": "Chinatown & North Beach",
  "07510": "Mission & SoMa",
  "07511": "Bernal & the Castro",
  "07512": "The Sunset",
  "07513": "Ingleside",
  "07514": "Marina & Western Addition",
};

function ago(at) {
  const mins = Math.max(0, Math.round((Date.now() - at) / 60000));
  if (mins < 1) return "now";
  if (mins < 60) return `${mins}m`;
  return `${Math.round(mins / 60)}h`;
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function byline(who, at) {
  const head = el("header", "feed-who");
  const dot = el("span", "feed-dot");
  dot.style.background = PUMA_COLORS[who.puma] ?? "#6b7280";
  head.append(
    dot,
    el("span", "feed-name", who.name),
    el("span", "feed-time", ago(at)),
  );
  return head;
}

function meta(who) {
  return el(
    "p",
    "feed-meta",
    `${who.occupation} · ${PUMA_NAMES[who.puma] ?? "San Francisco"}`,
  );
}

function renderThread(thread) {
  const wrap = el("section", "feed-thread");

  const post = el("article", "feed-post");
  post.append(byline(thread.author, thread.at), meta(thread.author));
  post.append(el("h2", "feed-post-title", thread.title));
  post.append(el("p", "feed-text", thread.body));
  wrap.append(post);

  for (const reply of thread.replies) {
    const item = el("article", "feed-post feed-reply");
    item.append(byline(reply, reply.at), meta(reply));
    item.append(el("p", "feed-text", reply.body));
    wrap.append(item);
  }
  return wrap;
}

export function createFeedPanel() {
  const root = document.getElementById("feed");
  if (!root) return { update() {} };

  const head = el("header", "feed-head");
  head.append(el("h1", "feed-title", "r/simfrancisco"));
  // The community's own description of itself, straight from the server, so
  // the panel and the writers' prompt can never drift apart. Changing the goal
  // changes the feed's character AND this line, together.
  const goal = el("p", "feed-goal", "");
  const status = el("p", "feed-status", "Listening…");
  head.append(goal, status);
  const list = el("div", "feed-list");
  root.append(head, list);

  let lastKey = "";

  async function poll() {
    let payload;
    try {
      const res = await fetch(ENDPOINT);
      payload = await res.json();
    } catch {
      status.textContent = "Cannot reach the feed.";
      return;
    }
    const threads = payload.threads ?? [];
    if (!threads.length) {
      status.textContent =
        payload.live === false ? "Quiet right now." : "Nobody has posted yet.";
      list.replaceChildren();
      lastKey = "";
      return;
    }
    // Only touch the DOM when something was actually said — a viewer reading a
    // post should not have it yanked out from under them every poll.
    const key = threads.map((t) => `${t.id}:${t.replies.length}`).join("|");
    if (key === lastKey) return;
    lastKey = key;

    // Name and purpose both come from the server, so the panel can never claim
    // to be a community the writers were not told they were posting in.
    if (payload.community && title.textContent !== payload.community)
      title.textContent = payload.community;
    if (payload.goal && goal.textContent !== payload.goal)
      goal.textContent = payload.goal;
    const posts = threads.reduce((n, t) => n + 1 + t.replies.length, 0);
    status.textContent = `${posts} posts · ${threads.length} conversations${payload.stale ? " · catching up" : ""}`;
    list.replaceChildren(...threads.map(renderThread));
  }

  poll();
  setInterval(poll, POLL_MS);
  return { refresh: poll };
}
