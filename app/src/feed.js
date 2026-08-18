// r/simfrancisco — the residents' feed, in the shape Reddit taught everyone to
// read: a subreddit header, post cards on a tinted ground, a byline, a title,
// the body, then a comment thread hanging off a rail.
//
// Every name here is a person walking the streets outside the panel — same id,
// same neighbourhood colour as their sphere in the diorama. Clicking one flies
// the camera to them and opens what they are, which is the whole reason the
// column and the city are the same product rather than two datasets sharing a
// window.
//
// The endpoint returns `{ live: false, threads: [] }` whenever the writer is
// offline. The panel says so plainly rather than inventing filler — the same
// contract the ferry and Muni layers keep.

const ENDPOINT = `${import.meta.env.BASE_URL}api/feed`;
// The server writes a post every ten minutes or so; polling a touch under that
// means a viewer who leaves the tab open sees new posts without a reload.
const POLL_MS = 2 * 60 * 1000;

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
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.round(mins / 60);
  return hours < 24 ? `${hours}h ago` : `${Math.round(hours / 24)}d ago`;
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

// ---------------------------------------------------------------- the modal

// One modal, built once and reused. Rebuilding it per click would drop focus
// and lose the escape handler.
function createProfileCard({ onVisit }) {
  const back = el("div", "rs-modal-back");
  back.hidden = true;
  const card = el("div", "rs-modal");
  const close = el("button", "rs-modal-close", "×");
  close.setAttribute("aria-label", "Close");
  const head = el("div", "rs-modal-head");
  const avatar = el("div", "rs-modal-avatar");
  const names = el("div", "rs-modal-names");
  const name = el("h2", "rs-modal-name", "");
  const job = el("p", "rs-modal-job", "");
  names.append(name, job);
  head.append(avatar, names);
  const hood = el("p", "rs-modal-hood", "");
  const persona = el("p", "rs-modal-persona", "");
  const visit = el("button", "rs-modal-visit", "Find them in the city");
  const note = el("p", "rs-modal-note", "");
  card.append(close, head, hood, persona, visit, note);
  back.append(card);
  document.body.append(back);

  let current = null;
  const hide = () => {
    back.hidden = true;
    current = null;
  };
  close.addEventListener("click", hide);
  back.addEventListener("click", (e) => {
    if (e.target === back) hide();
  });
  // Escape closes it, and the listener is on the document because the modal is
  // not what has focus after a click on a name.
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !back.hidden) hide();
  });
  visit.addEventListener("click", () => {
    if (!current) return;
    const found = onVisit(current);
    if (found) hide();
    else
      note.textContent =
        "They are not out on the street yet — the city is still loading their neighbourhood.";
  });

  return {
    show(person) {
      current = person;
      note.textContent = "";
      avatar.style.background = PUMA_COLORS[person.puma] ?? "#6b7280";
      name.textContent = person.name;
      job.textContent = person.occupation || "No occupation recorded";
      hood.textContent = PUMA_NAMES[person.puma] ?? "San Francisco";
      persona.textContent =
        person.persona || "No description written for this resident yet.";
      back.hidden = false;
      close.focus();
    },
  };
}

// ----------------------------------------------------------------- rendering

function byline(who, at, onOpen) {
  const row = el("div", "rs-byline");
  const dot = el("span", "rs-dot");
  dot.style.background = PUMA_COLORS[who.puma] ?? "#6b7280";
  const name = el("button", "rs-author", who.name);
  name.title =
    `${who.occupation || ""} · ${PUMA_NAMES[who.puma] ?? "San Francisco"}`.trim();
  name.addEventListener("click", () => onOpen(who));
  row.append(
    dot,
    name,
    el("span", "rs-sep", "·"),
    el("span", "rs-time", ago(at)),
  );
  return row;
}

function renderThread(thread, speakers, onOpen) {
  const who = speakers[thread.authorId] ?? thread.author;
  const card = el("article", "rs-post");

  card.append(byline({ ...thread.author, ...who }, thread.at, onOpen));
  card.append(el("h2", "rs-title", thread.title));
  card.append(el("p", "rs-body", thread.body));

  const count = thread.replies.length;
  card.append(
    el("div", "rs-actions", count === 1 ? "1 comment" : `${count} comments`),
  );

  if (count) {
    const comments = el("div", "rs-comments");
    for (const reply of thread.replies) {
      const item = el("div", "rs-comment");
      const speaker = speakers[reply.personaId] ?? reply;
      item.append(byline({ ...reply, ...speaker }, reply.at, onOpen));
      item.append(el("p", "rs-comment-body", reply.body));
      comments.append(item);
    }
    card.append(comments);
  }
  return card;
}

export function createFeedPanel({ onVisit = () => false } = {}) {
  const root = document.getElementById("feed");
  if (!root) return { refresh() {} };
  root.classList.add("rs");

  const head = el("header", "rs-head");
  const title = el("h1", "rs-name", "r/simfrancisco");
  const goal = el("p", "rs-goal", "");
  const status = el("p", "rs-status", "Loading…");
  head.append(title, goal, status);
  const list = el("div", "rs-list");
  root.append(head, list);

  const profile = createProfileCard({ onVisit });
  let lastKey = "";

  async function refresh() {
    let payload;
    try {
      const res = await fetch(ENDPOINT);
      payload = await res.json();
    } catch {
      status.textContent = "Cannot reach the feed.";
      return;
    }
    // Name and purpose both come from the server, so the panel can never claim
    // to be a community the writers were not told they were posting in.
    if (payload.community && title.textContent !== payload.community)
      title.textContent = payload.community;
    if (payload.goal && goal.textContent !== payload.goal)
      goal.textContent = payload.goal;

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

    const posts = threads.reduce((n, t) => n + 1 + t.replies.length, 0);
    status.textContent = `${threads.length} posts · ${posts} comments and posts today`;
    const speakers = payload.speakers ?? {};
    list.replaceChildren(
      ...threads.map((t) => renderThread(t, speakers, profile.show)),
    );
  }

  refresh();
  setInterval(refresh, POLL_MS);
  return { refresh };
}
