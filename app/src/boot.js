// Boot curtain controller: drives the fog + Y2K/Tron progress bar in
// index.html, decides when the city is presentable, and then dissipates the
// fog and removes itself from the DOM.
//
// Markup and styling live in index.html / boot.css so the curtain paints on the
// first frame, before this module has parsed. Everything here is defensive: if
// the markup is missing, every method is a no-op and the app boots exactly as
// it did before the curtain existed (AGENTS.md rule 3).

// ------------------------------------------------------------------- policy

// What the bar measures, in three phases. Nothing can render until the core
// data is in, so that gets the first third; the tile stream owns the long
// middle; the last slice is real rendered frames, so the fog never lifts onto
// an unpainted canvas.
const PHASES = {
  core: [0, 0.35],
  stream: [0.35, 0.92],
  frames: [0.92, 1],
};

// The curtain's job is to cover the part of the boot that is not presentable —
// a black canvas, then a nearly empty one. It is NOT to wait for a complete
// city: a full load is ~1590 cells and takes over two minutes on a slow
// connection (artifacts/perf baselines), and the city has always filled in
// progressively. So the stream gate opens on whichever comes first:
//
//   - REVEAL_CELLS cells have arrived (fast connections: a couple of seconds), or
//   - REVEAL_GRACE_MS has passed since the first rendered frame (slow ones).
//
// Cells arrive nearest-to-the-hero-pivot first (city.js preload()), so the
// middle of the opening frame is what fills first either way, and the rest
// streams in behind the dissipating fog.
// Measured (production build, artifacts/perf network profile): un-throttled,
// the data gate wins at ~3.5 s with the whole city already in. On Fast 4G the
// grace gate wins — 28 s after the first frame lands ~260 cells, which reads as
// San Francisco; revealing at 18 s (~156 cells) did not. Raising the grace is
// the one knob for "hold the fog longer on slow connections".
const REVEAL_CELLS = 340;
const REVEAL_GRACE_MS = 28000;

// Rendered frames required before the reveal, so the curtain never uncovers an
// unpainted canvas.
const MIN_FRAMES = 3;

// The curtain is shown for at least this long, so a warm-cache reload gets the
// beat rather than a flash.
const MIN_MS = 2400;

// Hard backstop. However slow the connection, however broken the plumbing, the
// fog lifts by now — a user is never trapped behind it. Kept clear of the
// grace gate above so it stays a true backstop rather than the operative gate.
const CAP_MS = 60000;

// How far the creep may run ahead of measured progress. Wide enough to drift
// across the gap between two loadCore steps, narrow enough that the bar is
// never meaningfully dishonest.
const LEAD = 0.11;

// Bar reads 100% for this long before the fog starts moving. Must outlast the
// fill's own width transition in boot.css, so the bar is visibly full first.
const HOLD_MS = 560;

// Must outlast the longest transition in boot.css (--boot-clear-ms plus the
// staggered delays and the trailing opacity fade).
const CLEAR_MS = 2750;

const TICK_MS = 100;

export function createBootScreen() {
  const root = document.getElementById('boot');
  const fill = root?.querySelector('.boot-fill');
  const pct = root?.querySelector('.boot-pct');
  const status = root?.querySelector('.boot-status');

  if (!root || !fill || !pct || !status) {
    if (root) root.remove();
    return inert();
  }

  const startedAt = performance.now();
  const ORDER = ['core', 'stream', 'frames'];
  let phase = 'core';
  let real = 0; // monotonic, real progress across all phases
  let shown = 0; // what the bar displays: eased, creeping, monotonic
  let creep = 0;
  let firstFrameAt = 0;
  let framesAfterStream = 0;
  let streamDone = false;
  let statusText = '';
  let streamLabel = 'STREAMING CITY GRID';
  let lastPct = -1;
  let cleared = false;
  let clearing = false;
  let failed = false;

  const ticker = setInterval(tick, TICK_MS);
  const watchdog = setTimeout(() => reveal('watchdog'), CAP_MS);

  upgradeFog(root);

  // Map a 0..1 fraction within a phase onto its slice of the bar. Phases only
  // ever move forward, and the bar never goes backwards — city.js resets
  // stats.cellsLoaded on a tier swap, and city.progress can exceed 1 because
  // cellsLoaded counts blobs that cellsTotal does not.
  function advance(name, fraction) {
    if (cleared || clearing) return;
    if (ORDER.indexOf(name) < ORDER.indexOf(phase)) return;
    phase = name;
    const [from, to] = PHASES[name];
    const value = from + clamp01(fraction) * (to - from);
    if (value > real) real = value;
  }

  function tick() {
    if (cleared) return;
    // The bar must keep breathing through the long silent stretches — the
    // module graph before loadCore even starts, and terrain.bin + landuse.bin
    // (9 MB) arriving as two fetches with no progress events between them. The
    // creep is a decelerating approach to the current phase ceiling, held to
    // LEAD ahead of measured truth so it can drift across a gap but never
    // invent a phase it has not reached.
    const ceiling = PHASES[phase][1] - 0.012;
    const floor = Math.max(creep, real);
    creep = floor + (ceiling - floor) * 0.02;
    const goal = clearing ? 1 : Math.min(Math.max(real, creep), ceiling, real + LEAD);
    if (goal > shown) shown += (goal - shown) * 0.22;
    paint();
  }

  function paint() {
    const value = Math.round(clamp01(shown) * 100);
    if (value !== lastPct) {
      lastPct = value;
      fill.style.width = `${value}%`;
      pct.textContent = `${value}%`;
    }
    if (failed) return;
    const next = describe();
    if (next !== statusText) {
      statusText = next;
      status.textContent = next;
    }
  }

  function describe() {
    if (clearing) return 'ONLINE';
    if (phase === 'core') return shown < 0.16 ? 'INITIALIZING' : 'LOADING ELEVATION GRID';
    if (phase === 'stream') return streamLabel;
    return 'RENDERING DIORAMA';
  }

  function reveal(reason) {
    if (cleared || clearing) return;
    clearing = true;
    clearTimeout(watchdog);
    if (reason !== 'ready') console.info(`boot curtain lifted early (${reason})`);

    // Snap to 100%, let it read, then dissipate.
    shown = 1;
    real = 1;
    paint();
    status.textContent = 'ONLINE';

    setTimeout(() => {
      root.classList.add('is-clearing');
      setTimeout(teardown, CLEAR_MS);
    }, HOLD_MS);
  }

  function teardown() {
    if (cleared) return;
    cleared = true;
    clearInterval(ticker);
    clearTimeout(watchdog);
    root.remove();
  }

  return {
    // loadCore progress, 0..1.
    core(fraction) {
      advance('core', fraction);
    },

    // Called once per rendered frame with city.stats. This is the whole reveal
    // gate: it is the only signal that proves the renderer is actually
    // painting, and it carries the stream numbers with it.
    rendered(stats) {
      if (clearing || cleared) return;
      const now = performance.now();
      if (!firstFrameAt) firstFrameAt = now;

      if (!streamDone) {
        const loaded = stats?.cellsLoaded ?? 0;
        const total = stats?.cellsTotal ?? 0;
        const byData = loaded / REVEAL_CELLS;
        const byTime = (now - firstFrameAt) / REVEAL_GRACE_MS;
        const ratio = clamp01(Math.max(byData, byTime));
        advance('stream', ratio);
        if (total > 0) streamLabel = `STREAMING CITY GRID ${loaded}/${Math.max(loaded, total)}`;
        if (ratio >= 1) streamDone = true;
        return;
      }

      // The last slice only starts once the stream gate is open, or the very
      // first frames would jump the bar to 96% over an empty city.
      framesAfterStream++;
      advance('frames', framesAfterStream / MIN_FRAMES);
      if (framesAfterStream < MIN_FRAMES) return;
      if (now - startedAt < MIN_MS) return;
      reveal('ready');
    },

    // The app threw. Stop the fog, mark the bar, and get out of the way so the
    // failure message underneath is readable.
    fail(message) {
      if (cleared) return;
      failed = true;
      clearInterval(ticker);
      clearTimeout(watchdog);
      root.classList.add('is-failed');
      statusText = String(message || 'BOOT FAILED').toUpperCase().slice(0, 64);
      status.textContent = statusText;
      setTimeout(() => {
        root.classList.add('is-clearing');
        setTimeout(teardown, CLEAR_MS);
      }, 1400);
    },

    // Force the curtain up (QA, and anything that needs the city unobscured).
    reveal(reason = 'manual') {
      reveal(reason);
    },

    get cleared() {
      return cleared;
    },

    get state() {
      return {
        phase,
        real: +real.toFixed(4),
        shown: +shown.toFixed(4),
        streamDone,
        framesAfterStream,
        clearing,
        cleared,
        failed,
        msSinceStart: Math.round(performance.now() - startedAt),
        policy: { REVEAL_CELLS, REVEAL_GRACE_MS, MIN_MS, CAP_MS },
      };
    },
  };
}

// Progressive fog tiers. The SVG in boot.css is already on screen and costs
// nothing; these are strict upgrades, applied only once a tier has fully
// decoded. Every failure path is "keep the tier below", never a hole and never
// a delayed reveal (AGENTS.md rule 3) — nothing here is awaited by the curtain.
const FOG_TIERS = [
  { flag: 'has-doors', files: ['karl-door-left.webp', 'karl-door-right.webp'] },
  { flag: 'has-wisps', files: ['karl-wisp.webp'] },
];

function upgradeFog(root) {
  const base = `${import.meta.env.BASE_URL}boot/`;
  for (const tier of FOG_TIERS) {
    Promise.all(
      tier.files.map(
        (file) =>
          new Promise((resolve, reject) => {
            const image = new Image();
            image.onload = () => resolve(image);
            image.onerror = () => reject(new Error(file));
            image.src = base + file;
          })
      )
    )
      .then((images) => {
        // decode() rather than onload alone: a mask swapped in before the
        // bitmap is ready pops on the first paint that uses it.
        const decoded = images.map((image) =>
          typeof image.decode === 'function' ? image.decode().catch(() => {}) : Promise.resolve()
        );
        return Promise.all(decoded);
      })
      .then(() => {
        if (root.isConnected) root.classList.add(tier.flag);
      })
      .catch((err) => {
        console.warn(`boot fog: ${tier.flag} unavailable, keeping the tier below`, err.message);
      });
  }
}

function inert() {
  return {
    core() {},
    rendered() {},
    fail() {},
    reveal() {},
    get cleared() {
      return true;
    },
    get state() {
      return { phase: 'absent', cleared: true };
    },
  };
}

function clamp01(value) {
  return Number.isFinite(value) ? Math.min(1, Math.max(0, value)) : 0;
}
