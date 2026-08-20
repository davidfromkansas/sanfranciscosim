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
const COMPOSE_ENDPOINT = `${import.meta.env.BASE_URL}api/compose`;
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

// The community's rules, shown verbatim. These are not decoration: whatever is
// in this list is handed to every resident in every prompt, so the panel and
// the writers are reading the same document. Empty today, and the empty state
// says so plainly rather than inventing house rules nobody agreed.
function createRulesCard() {
  const back = el("div", "rs-modal-back");
  back.hidden = true;
  const card = el("div", "rs-modal");
  const close = el("button", "rs-modal-close", "×");
  close.setAttribute("aria-label", "Close");
  const heading = el("h2", "rs-rules-title", "Community rules");
  const sub = el("p", "rs-rules-sub", "");
  const body = el("div", "rs-rules-body");
  card.append(close, heading, sub, body);
  back.append(card);
  document.body.append(back);

  const hide = () => {
    back.hidden = true;
  };
  close.addEventListener("click", hide);
  back.addEventListener("click", (e) => {
    if (e.target === back) hide();
  });
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !back.hidden) hide();
  });

  return {
    show(name, rules) {
      sub.textContent = `Every rule here is given to each resident of ${name} whenever they write.`;
      if (!rules?.length) {
        body.replaceChildren(
          el(
            "p",
            "rs-rules-empty",
            `No rules have been set for ${name} yet. Residents are writing to the community's stated purpose alone.`,
          ),
        );
      } else {
        const list = el("ol", "rs-rules-list");
        for (const rule of rules) list.append(el("li", null, rule));
        body.replaceChildren(list);
      }
      back.hidden = false;
      close.focus();
    },
  };
}

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
  // An in-flight visit. Fetching somebody can take seconds — their
  // neighbourhood has to stream first — and in that time the reader can close
  // the card or open somebody else's. Whoever they picked LAST is the one the
  // camera should end up on, so any earlier visit is abandoned rather than
  // left to land on top of it.
  let trip = null;
  const abandon = () => {
    trip?.abort();
    trip = null;
    visit.disabled = false;
    visit.textContent = "Find them in the city";
  };
  const hide = () => {
    abandon();
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
  visit.addEventListener("click", async () => {
    if (!current) return;
    abandon();
    const person = current;
    const controller = new AbortController();
    trip = controller;
    visit.disabled = true;
    visit.textContent = "Finding them…";
    const where = PUMA_NAMES[person.puma];
    note.textContent = where
      ? `Flying to ${where} and loading the streets.`
      : "Flying to their neighbourhood and loading the streets.";

    let result;
    try {
      result = await onVisit(person, { signal: controller.signal });
    } catch (error) {
      result = { ok: false, reason: "error", error };
    }
    // Somebody else's card is open, or this one was closed — the reader has
    // moved on and this answer is no longer about anything on screen.
    if (controller.signal.aborted || trip !== controller) return;
    trip = null;
    visit.disabled = false;
    visit.textContent = "Find them in the city";
    if (result?.ok) return hide();
    note.textContent =
      result?.reason === "unknown"
        ? "They are not among the residents walking the city."
        : result?.reason === "timeout"
          ? "Their neighbourhood is taking a long time to load. Try again in a moment."
          : "Something went wrong getting to them.";
  });

  return {
    show(person) {
      abandon();
      current = person;
      note.textContent = "";
      face.replaceChildren(avatar(person, 52));
      name.textContent = person.name;
      job.textContent = person.occupation || "No occupation recorded";
      hood.textContent = person.mood
        ? `${PUMA_NAMES[person.puma] ?? "San Francisco"} · ${person.mood.toLowerCase()}`
        : (PUMA_NAMES[person.puma] ?? "San Francisco");
      persona.textContent =
        person.persona || "No description written for this resident yet.";
      back.hidden = false;
      close.focus();
    },
  };
}

function createComposer({ onPosted }) {
  const fab = el("button", "rs-create-fab", "+ Create Post");
  fab.type = "button";
  fab.setAttribute("aria-label", "Create a post");

  const back = el("div", "rs-compose-back");
  back.hidden = true;
  back.setAttribute("aria-labelledby", "rs-compose-title");
  const card = el("div", "rs-modal rs-composer");
  const heading = el("h2", "rs-compose-title", "Create a post");
  heading.id = "rs-compose-title";
  const intro = el(
    "p",
    "rs-compose-intro",
    "Share something relevant to San Francisco. Every post is reviewed before it appears.",
  );
  const form = el("form", "rs-compose-form");
  const headerLabel = el("label", "rs-compose-label", "Header");
  const header = el("input", "rs-compose-input");
  header.id = "rs-compose-header";
  header.name = "title";
  header.type = "text";
  header.maxLength = 80;
  header.required = true;
  header.autocomplete = "off";
  header.setAttribute("aria-describedby", "rs-compose-header-count");
  const headerCount = el("span", "rs-compose-count", "80 characters remaining");
  headerCount.id = "rs-compose-header-count";
  headerLabel.htmlFor = header.id;
  headerLabel.append(headerCount);

  const bodyLabel = el("label", "rs-compose-label", "Body Text");
  const body = el("textarea", "rs-compose-input rs-compose-body");
  body.id = "rs-compose-body";
  body.name = "body";
  body.maxLength = 240;
  body.required = true;
  body.rows = 5;
  body.setAttribute("aria-describedby", "rs-compose-body-count");
  const bodyCount = el("span", "rs-compose-count", "240 characters remaining");
  bodyCount.id = "rs-compose-body-count";
  bodyLabel.htmlFor = body.id;
  bodyLabel.append(bodyCount);

  const message = el("p", "rs-compose-message");
  message.setAttribute("aria-live", "polite");
  const actions = el("div", "rs-compose-actions");
  const cancel = el("button", "rs-compose-cancel", "Cancel");
  cancel.type = "button";
  const post = el("button", "rs-compose-post", "Post");
  post.type = "submit";
  actions.append(cancel, post);
  form.append(headerLabel, header, bodyLabel, body, message, actions);
  card.append(heading, intro, form);
  back.append(card);
  document.body.append(fab, back);

  let loading = false;

  function updateCounts() {
    headerCount.textContent = `${80 - header.value.length} characters remaining`;
    bodyCount.textContent = `${240 - body.value.length} characters remaining`;
    post.disabled = loading || !header.value.trim() || !body.value.trim();
  }

  function clear() {
    header.value = "";
    body.value = "";
    message.textContent = "";
    message.className = "rs-compose-message";
    updateCounts();
  }

  function hide({ reset = true } = {}) {
    if (loading) return;
    back.hidden = true;
    if (reset) clear();
    fab.focus();
  }

  function show() {
    back.hidden = false;
    updateCounts();
    header.focus();
  }

  async function submit() {
    if (loading || !header.value.trim() || !body.value.trim()) return;
    loading = true;
    // Covers the whole wait, not just its first phase. The request grades the
    // post, samples its voters and writes its first replies before it answers,
    // so "reviewing" alone left the reader watching a spinner wondering what
    // was taking so long.
    message.textContent =
      "Reviewing your post and showing it to the neighbours…";
    message.className = "rs-compose-message rs-compose-loading";
    form.classList.add("rs-compose-is-loading");
    post.innerHTML =
      '<span class="rs-compose-spinner" aria-hidden="true"></span> Posting…';
    cancel.disabled = true;
    header.disabled = true;
    body.disabled = true;
    updateCounts();
    try {
      const response = await fetch(COMPOSE_ENDPOINT, {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ title: header.value, body: body.value }),
      });
      let result;
      try {
        result = await response.json();
      } catch {
        throw new Error("The post review returned an unreadable response.");
      }
      if (!response.ok)
        throw new Error(result.error || "Could not review the post.");
      if (result.posted) {
        clear();
        back.hidden = true;
        fab.focus();
        // The feed as it stands WITH their post in it, straight out of the
        // response. Handing this to the panel rather than asking it to go and
        // fetch is what makes their own post appear the moment the composer
        // closes: /api/feed is CDN-cached for thirty seconds with
        // stale-while-revalidate, so a refresh fired now is precisely the one
        // likely to be answered from an edge copy that predates the post.
        onPosted(result.feed ?? null);
        return;
      }
      message.textContent = `Score ${result.score}/${result.threshold}: ${result.reason}`;
      message.className = "rs-compose-message rs-compose-verdict";
    } catch (error) {
      message.textContent = error?.message || "Could not post right now.";
      message.className = "rs-compose-message rs-compose-error";
    } finally {
      loading = false;
      form.classList.remove("rs-compose-is-loading");
      post.textContent = "Post";
      cancel.disabled = false;
      header.disabled = false;
      body.disabled = false;
      updateCounts();
    }
  }

  header.addEventListener("input", updateCounts);
  body.addEventListener("input", updateCounts);
  fab.addEventListener("click", show);
  cancel.addEventListener("click", () => hide());
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    submit();
  });
  back.addEventListener("click", (event) => {
    if (event.target === back) hide();
  });
  document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && !back.hidden) hide();
  });
  updateCounts();
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
function identity(who, at, onOpen, human = false) {
  const block = el("div", "rs-who");

  const top = el("div", "rs-who-top");
  const name = human
    ? el("span", "rs-author rs-author-human", who.name)
    : el("button", "rs-author", who.name);
  if (!human) name.addEventListener("click", () => onOpen(who));
  top.append(name);
  if (human) top.append(el("span", "rs-human-pill", "HUMAN"));
  top.append(el("span", "rs-sep", "·"), timeLabel(at));

  const sub = human
    ? "Visiting from outside the simulation"
    : who.occupation
      ? `${who.occupation} · ${PUMA_NAMES[who.puma] ?? "San Francisco"}`
      : (PUMA_NAMES[who.puma] ?? "San Francisco");

  block.append(top, el("div", "rs-who-sub", sub));
  return block;
}

function byline(who, at, onOpen, human = false) {
  const row = el("div", "rs-byline");
  row.append(avatar(who, 22), identity(who, at, onOpen, human));
  return row;
}

// The score, with the residents behind it in the tooltip. A bare number invites
// the question "who?", and unlike a real subreddit we can actually answer it.
function score(item) {
  const wrap = el("span", "rs-score");
  const n = item.score ?? 0;
  wrap.classList.add(n > 0 ? "up" : n < 0 ? "down" : "zero");
  wrap.textContent = `${n > 0 ? "▲" : n < 0 ? "▼" : "•"} ${n}`;
  wrap.title = `${item.upvotes ?? 0} up · ${item.downvotes ?? 0} down`;
  return wrap;
}

function renderThread(thread, speakers, onOpen, onDetail) {
  const who = { ...thread.author, ...(speakers[thread.authorId] ?? {}) };
  const card = el("article", thread.event ? "rs-post rs-event" : "rs-post");

  // A wire story is reported, not said: it gets a kicker naming what it is
  // instead of a resident byline, and a credit that links to the newsroom.
  // Restating somebody's reporting without saying whose would be the wrong
  // thing to do.
  if (thread.event) {
    const kicker = el("div", "rs-event-kicker");
    kicker.append(
      el("span", "rs-event-tag", "SF WIRE"),
      el("span", "rs-sep", "·"),
      timeLabel(thread.at),
    );
    card.append(kicker);
  } else {
    card.append(byline(who, thread.at, onOpen, thread.human));
  }
  card.append(el("h2", "rs-title", thread.title));
  card.append(el("p", "rs-body", thread.body));
  if (thread.event && thread.source) {
    const credit = el("p", "rs-event-credit");
    const a = el("a", "rs-event-link", thread.source.name);
    a.href = thread.source.url;
    a.target = "_blank";
    a.rel = "noopener noreferrer";
    credit.append("Reporting: ", a);
    card.append(credit);
  }

  const count = thread.replies.length;
  const actions = el("div", "rs-actions");
  actions.append(score(thread));
  // The count is a button whenever there is something behind it. A thread with
  // no replies still shows the zero — it is a fact about the post, and hiding
  // it would make an unanswered post look like one nobody had counted.
  const label = count === 1 ? "1 comment" : `${count} comments`;
  if (count) {
    const open = el("button", "rs-count rs-count-btn", label);
    open.type = "button";
    open.addEventListener("click", () => onDetail(thread.id));
    actions.append(open);
  } else {
    actions.append(el("span", "rs-count rs-count-none", label));
  }
  card.append(actions);
  return card;
}

// The comment list, used only by the detail view now. Kept as its own function
// because the shape of a comment is a separate decision from where it appears.
function renderComments(thread, speakers, onOpen) {
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
    main.append(score(reply));
    item.append(avatar(speaker, 22), main);
    comments.append(item);
  }
  return comments;
}

// The post detail: one thread, its comments under it, stacked OVER the feed
// rather than replacing it. Being a real layer rather than a swap is what keeps
// the list's scroll position — the feed underneath is never touched, so
// dismissing this puts you back exactly where you were reading.
function createDetailView({ onOpen }) {
  const view = el("section", "rs-detail");
  view.hidden = true;
  const bar = el("div", "rs-detail-bar");
  const back = el("button", "rs-back");
  back.type = "button";
  back.setAttribute("aria-label", "Back to r/simfrancisco");
  back.innerHTML =
    '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" stroke="currentColor" ' +
    'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">' +
    '<path d="M10 3L5 8l5 5"/></svg><span>r/simfrancisco</span>';
  bar.append(back);
  const body = el("div", "rs-detail-body");
  view.append(bar, body);

  let openId = null;
  let speakers = {};

  function draw(thread) {
    if (!thread) return close();
    const who = { ...thread.author, ...(speakers[thread.authorId] ?? {}) };
    const post = el(
      "article",
      thread.event ? "rs-post rs-post-full rs-event" : "rs-post rs-post-full",
    );
    if (thread.event) {
      const kicker = el("div", "rs-event-kicker");
      kicker.append(
        el("span", "rs-event-tag", "SF WIRE"),
        el("span", "rs-sep", "·"),
        timeLabel(thread.at),
      );
      post.append(kicker);
    } else {
      post.append(byline(who, thread.at, onOpen, thread.human));
    }
    post.append(el("h2", "rs-title", thread.title));
    post.append(el("p", "rs-body", thread.body));
    if (thread.event && thread.source) {
      const credit = el("p", "rs-event-credit");
      const a = el("a", "rs-event-link", thread.source.name);
      a.href = thread.source.url;
      a.target = "_blank";
      a.rel = "noopener noreferrer";
      credit.append("Reporting: ", a);
      post.append(credit);
    }
    const actions = el("div", "rs-actions");
    actions.append(score(thread));
    const n = thread.replies.length;
    actions.append(
      el("span", "rs-count", n === 1 ? "1 comment" : `${n} comments`),
    );
    post.append(actions);
    body.replaceChildren(post, renderComments(thread, speakers, onOpen));
  }

  function open(thread, people) {
    speakers = people;
    openId = thread.id;
    draw(thread);
    view.hidden = false;
    // Its own scroll, starting at the top of the post being opened.
    view.scrollTop = 0;
    back.focus({ preventScroll: true });
  }

  function close() {
    openId = null;
    view.hidden = true;
    body.replaceChildren();
  }

  // Called on every poll. A reply landing while somebody is reading should
  // appear under what they are reading, not close the view or throw them to
  // the top — so this redraws in place and puts the scroll back where it was.
  function sync(threads, people) {
    if (!openId) return;
    const thread = threads.find((t) => t.id === openId);
    if (!thread) return close(); // retired out from under us
    speakers = people;
    const at = view.scrollTop;
    draw(thread);
    view.scrollTop = at;
  }

  back.addEventListener("click", close);
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape" && !view.hidden) close();
  });

  return {
    view,
    open,
    close,
    sync,
    get openId() {
      return openId;
    },
  };
}

export function createFeedPanel({
  // Resolves { ok } once the camera is on them, which can take seconds when
  // their neighbourhood has to stream in first.
  onVisit = async () => ({ ok: false, reason: "unknown" }),
  castCount = () => 0,
} = {}) {
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
  // The size of the cast, counted from the baked population rather than the
  // feed: every resident the simulation carries, whether or not their
  // neighbourhood has streamed in yet. It only moves once, when the bake
  // lands, which is why it ticks rather than being written at build time.
  const census = el("p", "rs-census", "");
  const goal = el("p", "rs-goal", "");
  const rulesButton = el("button", "rs-rules-open", "Community rules");
  // The button rides the name's line, pushed to the far edge — it is a
  // reference, not something the header is asking you to do, so it belongs out
  // of the reading path rather than under the description.
  const nameRow = el("div", "rs-name-row");
  nameRow.append(title, rulesButton);
  titles.append(nameRow, census, goal);

  function refreshCensus() {
    const n = castCount();
    const text = `${n.toLocaleString()} simfranciscan${n === 1 ? "" : "s"} live here`;
    if (census.textContent !== text) census.textContent = text;
  }
  refreshCensus();
  // The bake is fetched, so the count is zero for the first moments.
  setInterval(refreshCensus, 2000);

  // Below the desktop breakpoint the panel is a bottom sheet, and this raises
  // and lowers it. CSS hides the button above that width; the class it toggles
  // means nothing there, so there is no state to keep in sync with the layout.
  // It starts closed: on a phone the city is what somebody came for, and a
  // panel that opens over two thirds of it uninvited is a wall.
  const sheet = el("button", "rs-sheet");
  sheet.type = "button";
  sheet.innerHTML =
    '<svg viewBox="0 0 16 16" aria-hidden="true" fill="none" ' +
    'stroke="currentColor" stroke-width="2.4" stroke-linecap="round" ' +
    'stroke-linejoin="round"><path d="M3 10l5-5 5 5"/></svg>';
  function setSheet(open) {
    root.classList.toggle("rs-open", open);
    sheet.setAttribute("aria-expanded", String(open));
    sheet.setAttribute("aria-label", open ? "Hide the feed" : "Show the feed");
  }
  setSheet(false);
  sheet.addEventListener("click", () =>
    setSheet(!root.classList.contains("rs-open")),
  );
  bar.append(icon, titles, sheet);

  const status = el("p", "rs-status", "Loading…");
  head.append(bar, status);
  const list = el("div", "rs-list");
  const profile = createProfileCard({ onVisit });
  // Inside the panel, so it covers exactly the panel and nothing else — the
  // right-hand column on a desktop, the sheet on a phone, without either
  // measurement being repeated here.
  const detail = createDetailView({ onOpen: profile.show });
  root.append(head, list, detail.view);
  const rulesCard = createRulesCard();
  let refresh;
  // A fresh post hands its own feed straight in; anything else falls back to
  // fetching, with the cache stepped round so the reader is never shown an
  // edge copy older than the thing they just did.
  createComposer({ onPosted: (feed) => refresh?.({ feed, bust: true }) });
  let community = { name: "r/simfrancisco", rules: [] };
  rulesButton.addEventListener("click", () =>
    rulesCard.show(community.name, community.rules),
  );
  let lastKey = "";
  // Everything loaded so far, newest first, and where the next page starts.
  // The poll refreshes the TOP of this and leaves the rest alone: a reader
  // forty posts down must not have the ground move under them every thirty
  // seconds.
  let loaded = [];
  let speakers = {};
  let nextBefore = null;
  let more = false;
  let loadingPage = false;

  // Renders whatever is loaded. Separate from fetching so a page arriving and a
  // poll arriving go through exactly the same path.
  function draw() {
    list.replaceChildren(
      ...loaded.map((t) =>
        renderThread(t, speakers, profile.show, (id) => {
          const thread = loaded.find((x) => x.id === id);
          if (thread) detail.open(thread, speakers);
        }),
      ),
    );
    detail.sync(loaded, speakers);
  }

  // The next page, when the reader gets near the bottom. Guarded so a fast
  // scroll cannot fire three requests for the same page.
  async function loadMore() {
    if (loadingPage || !more || !nextBefore) return;
    loadingPage = true;
    const cursor = nextBefore;
    try {
      const res = await fetch(`${ENDPOINT}?before=${cursor}&limit=20`);
      const page = await res.json();
      const have = new Set(loaded.map((t) => t.id));
      const fresh = (page.threads ?? []).filter((t) => !have.has(t.id));
      loaded = [...loaded, ...fresh].sort((a, b) => b.startedAt - a.startedAt);
      speakers = { ...speakers, ...(page.speakers ?? {}) };
      nextBefore = page.page?.nextBefore ?? null;
      more = Boolean(page.page?.more);
      if (fresh.length) {
        draw();
        fillViewport();
      }
    } catch {
      // A page that will not load is not worth an error in the reader's face —
      // they still have everything above it. The next scroll tries again.
    } finally {
      loadingPage = false;
    }
  }

  // A page that does not fill the panel leaves nothing to scroll, and a feed
  // whose only way to ask for more is a scroll event would stop dead there —
  // on a tall screen, or a short first page. Keep pulling until there is
  // something to scroll, or nothing left to pull.
  function fillViewport() {
    if (!more || loadingPage) return;
    if (root.scrollHeight <= root.clientHeight + 200) loadMore();
  }

  // Near the bottom, not at it, so the next page is usually there before the
  // reader arrives.
  root.addEventListener("scroll", () => {
    if (root.scrollTop + root.clientHeight > root.scrollHeight - 900)
      loadMore();
  });

  refresh = async function refresh({ feed = null, bust = false } = {}) {
    let payload = feed;
    if (!payload) {
      try {
        // `bust` makes the URL unique so the CDN has nothing stored against it
        // and has to ask the origin. Only used after the reader did something
        // whose result they are entitled to see immediately; the polling path
        // stays cacheable, which is what keeps a busy feed cheap.
        const url = bust ? `${ENDPOINT}?t=${Date.now()}` : ENDPOINT;
        const res = await fetch(url);
        payload = await res.json();
      } catch {
        status.textContent = "Cannot reach the feed.";
        return;
      }
    }
    // Name and purpose both come from the server, so the panel can never claim
    // to be a community the writers were not told they were posting in.
    if (payload.community && title.textContent !== payload.community)
      title.textContent = payload.community;
    community = {
      name: payload.community ?? community.name,
      rules: payload.rules ?? [],
    };
    if (payload.goal && goal.textContent !== payload.goal)
      goal.textContent = payload.goal;

    const threads = payload.threads ?? [];
    if (!threads.length) {
      status.textContent =
        payload.live === false ? "Quiet right now." : "Nobody has posted yet.";
      list.replaceChildren();
      // Reset the paging state too, or a feed that empties leaves a stale
      // cursor behind and the next scroll asks for a page of a city that is
      // no longer there.
      loaded = [];
      nextBefore = null;
      more = false;
      lastKey = "";
      return;
    }
    // Only touch the DOM when something was actually said — a viewer reading a
    // post should not have it yanked out from under them every poll.
    const key = threads.map((t) => `${t.id}:${t.replies.length}`).join("|");
    // The key includes every thread's reply count, so any new comment changes
    // it and falls through to the render below — which is what keeps an open
    // detail view current. A poll that changes nothing returns here and leaves
    // both the list and the detail untouched, which is the point.
    if (key === lastKey) return;
    lastKey = key;

    // Posts and comments are separate counts. The old line added the posts into
    // the second number and then called it "comments and posts", so it counted
    // them twice and read as nonsense. "Last 24 hours" rather than "today"
    // because retirement is a rolling twenty-four hours, not a calendar day.
    // From the server's totals when it sends them: the feed serves a window of
    // the most recent threads, so counting what arrived would under-report the
    // day. Falls back to counting locally for an older payload.
    const posts = payload.totals?.posts ?? threads.length;
    const comments =
      payload.totals?.comments ??
      threads.reduce((n, t) => n + t.replies.length, 0);
    const plural = (n, word) => `${n} ${word}${n === 1 ? "" : "s"}`;
    status.textContent = `${plural(posts, "post")} · ${plural(comments, "comment")} · last 24 hours`;
    // Page one replaces the top of the list. Anything already loaded BELOW it
    // is kept: a poll bringing one new post must not throw away the four pages
    // somebody scrolled through to get where they are.
    const arrived = new Map(threads.map((t) => [t.id, t]));
    const below = loaded.filter((t) => !arrived.has(t.id));
    loaded = [...threads, ...below].sort((a, b) => b.startedAt - a.startedAt);
    speakers = { ...speakers, ...(payload.speakers ?? {}) };
    if (payload.page && loaded.length <= threads.length) {
      nextBefore = payload.page.nextBefore;
      more = payload.page.more;
    }
    // draw() syncs the open thread against everything LOADED. Syncing against
    // this page alone would tell a reader four pages down that the thread they
    // are reading had been retired, and close it under them.
    draw();
    fillViewport();
  };

  refresh();
  setInterval(refresh, POLL_MS);
  // Ages tick on their own clock. The feed only rebuilds when something is
  // actually said, so without this a post written five minutes ago still reads
  // "5m ago" an hour later. One pass over a few dozen spans, once a minute.
  setInterval(refreshStamps, 60 * 1000);
  return { refresh };
}
