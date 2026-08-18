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

// Elapsed time FLOORS. Rounding made everything older than it was: something
// written ninety minutes ago read "2h ago", and thirty seconds ago read "1m
// ago". Nobody says "two hours" about an hour and a half.
function ago(at) {
  const secs = Math.max(0, (Date.now() - at) / 1000);
  if (secs < 60) return "just now";
  const mins = Math.floor(secs / 60);
  if (mins < 60) return `${mins}m ago`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h ago`;
  const days = Math.floor(hours / 24);
  if (days === 1) return "yesterday";
  if (days < 7) return `${days} days ago`;
  // Past a week, a count stops meaning anything — say the date.
  return new Date(at).toLocaleDateString(undefined, {
    month: "short",
    day: "numeric",
  });
}

// Every rendered time label, so they can be refreshed in place. Rebuilding the
// feed to age a timestamp would yank a post out from under whoever is reading
// it; the panel only rebuilds when something is actually said.
const stamps = new Set();

function timeLabel(at) {
  const node = el("span", "rs-time", ago(at));
  // The exact moment, for anyone who wants it, without spending screen on it.
  node.title = new Date(at).toLocaleString();
  node.dataset.at = String(at);
  stamps.add(node);
  return node;
}

function refreshStamps() {
  for (const node of stamps) {
    if (!node.isConnected) {
      stamps.delete(node); // re-rendered away; stop holding a reference
      continue;
    }
    const text = ago(Number(node.dataset.at));
    if (node.textContent !== text) node.textContent = text;
  }
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
  const face = el("div", "rs-modal-avatar");
  const names = el("div", "rs-modal-names");
  const name = el("h2", "rs-modal-name", "");
  const job = el("p", "rs-modal-job", "");
  names.append(name, job);
  head.append(face, names);
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
      face.replaceChildren(avatar(person, 52));
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

// The stock profile silhouette, drawn rather than fetched: it stays sharp at any
// size, costs no request, and needs no asset in the repo. The ring keeps the
// neighbourhood colour that used to be the whole dot — that colour is the link
// between a name here and their sphere out in the city, and losing it would cut
// the two halves of the product apart.
const SVG_NS = "http://www.w3.org/2000/svg";

function avatar(who, size) {
  const svg = document.createElementNS(SVG_NS, "svg");
  svg.setAttribute("viewBox", "0 0 100 100");
  svg.setAttribute("width", size);
  svg.setAttribute("height", size);
  svg.setAttribute("aria-hidden", "true");
  svg.classList.add("rs-avatar");

  const ring = document.createElementNS(SVG_NS, "circle");
  ring.setAttribute("cx", "50");
  ring.setAttribute("cy", "50");
  ring.setAttribute("r", "47");
  ring.setAttribute("fill", "#eceae4");
  ring.setAttribute("stroke", PUMA_COLORS[who.puma] ?? "#6b7280");
  ring.setAttribute("stroke-width", "6");

  const head = document.createElementNS(SVG_NS, "circle");
  head.setAttribute("cx", "50");
  head.setAttribute("cy", "38");
  head.setAttribute("r", "17");
  head.setAttribute("fill", "#3c4450");

  // Shoulders: a dome whose flat base sits inside the ring, so nothing needs
  // clipping and the shape holds at 20 px as well as at 52.
  const body = document.createElementNS(SVG_NS, "path");
  body.setAttribute("d", "M23 86 a27 27 0 0 1 54 0 Z");
  body.setAttribute("fill", "#3c4450");

  svg.append(ring, head, body);
  return svg;
}

// Who is speaking, in two lines: the name and when, then what they do and
// where they live. The occupation is the whole reason a post reads as coming
// from a particular life rather than from nobody — "Cook, part time" over a
// post about a bakery is most of the meaning — so it belongs on screen and not
// in a tooltip nobody hovers.
function identity(who, at, onOpen) {
  const block = el("div", "rs-who");

  const top = el("div", "rs-who-top");
  const name = el("button", "rs-author", who.name);
  name.addEventListener("click", () => onOpen(who));
  top.append(name, el("span", "rs-sep", "·"), timeLabel(at));

  // A resident with no job still has a place. Census wording like "Not in the
  // labour force" is theirs and is printed as written; only a genuinely empty
  // field falls back to the neighbourhood alone.
  const where = PUMA_NAMES[who.puma] ?? "San Francisco";
  const sub = who.occupation ? `${who.occupation} · ${where}` : where;

  block.append(top, el("div", "rs-who-sub", sub));
  return block;
}

function byline(who, at, onOpen) {
  const row = el("div", "rs-byline");
  row.append(avatar(who, 22), identity(who, at, onOpen));
  return row;
}

function renderThread(thread, speakers, onOpen) {
  const who = { ...thread.author, ...(speakers[thread.authorId] ?? {}) };
  const card = el("article", "rs-post");

  card.append(byline(who, thread.at, onOpen));
  card.append(el("h2", "rs-title", thread.title));
  card.append(el("p", "rs-body", thread.body));

  const count = thread.replies.length;
  card.append(
    el("div", "rs-actions", count === 1 ? "1 comment" : `${count} comments`),
  );

  if (count) {
    const comments = el("div", "rs-comments");
    for (const reply of thread.replies) {
      const speaker = { ...reply, ...(speakers[reply.personaId] ?? {}) };
      // A comment is a two-column row: the face in its own column, everything
      // said in the other. The body then hangs under the name rather than under
      // the picture, which is what makes a long thread scannable — the eye
      // follows one straight edge of text down the whole discussion.
      const item = el("div", "rs-comment");
      const main = el("div", "rs-comment-main");
      main.append(identity(speaker, reply.at, onOpen));
      main.append(el("p", "rs-comment-body", reply.body));
      item.append(avatar(speaker, 22), main);
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

  // The subreddit header, in Reddit's arrangement: a banner, then the icon
  // overlapping its lower edge with the name beside it. Both images live in
  // app/public/feed/ and are set as backgrounds rather than <img> so a missing
  // file shows the painted fallback underneath instead of a broken-image icon.
  const head = el("header", "rs-head");
  head.append(el("div", "rs-banner"));

  const bar = el("div", "rs-bar");
  const icon = el("div", "rs-icon");
  const titles = el("div", "rs-titles");
  const title = el("h1", "rs-name", "r/simfrancisco");
  const goal = el("p", "rs-goal", "");
  titles.append(title, goal);
  bar.append(icon, titles);

  const status = el("p", "rs-status", "Loading…");
  head.append(bar, status);
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
  // Ages tick on their own clock. The feed only rebuilds when something is
  // actually said, so without this a post written five minutes ago still reads
  // "5m ago" an hour later. One pass over a few dozen spans, once a minute.
  setInterval(refreshStamps, 60 * 1000);
  return { refresh };
}
