// Making every ferry route tell itself apart from every other one.
//
// THE PROBLEM: the published liveries are not a palette. San Francisco Bay
// Ferry gives each of its seven routes a distinct colour, but Golden Gate
// Ferry paints ALL FIVE of its routes the same red (#cc3333) — Sausalito,
// Tiburon, Larkspur, Angel Island and the Triangle are one colour in the feed —
// so on the water they read as a single tangled service instead of five
// crossings. Treasure Island and Angel Island–Tiburon then land close to
// colours WETA is already using.
//
// THE RULE: a published colour is kept whenever it is already unique, because
// it is the service's real identity and the whole point of using it. Only
// routes that COLLIDE get moved, and they are moved as little as the eye needs
// — spread around their own hue rather than reassigned — so Golden Gate's five
// still read as a family of reds while being individually followable.
//
// This is a palette decision, not a data one: rule 5 governs where things are
// (footprints, heights, alignments), and none of that moves here. The
// alignments, terminals and operators stay exactly as published, and each
// route keeps its `publishedColor` for anything that wants to state the truth.
//
// Pure functions, no three.js, no DOM — covered by
// app/test/ferry-palette.test.mjs, which asserts the property that matters:
// no two routes end up looking alike.

// Two colours are "the same" to a viewer glancing at a wall across the Bay if
// their hues are within this many degrees AND their lightness is within this
// much. Generous, because these are semi-transparent ribbons over bright water.
export const HUE_APART = 14;
export const LIGHT_APART = 0.13;
// How far a colliding group may be spread around its shared hue. Golden Gate
// red spread ±30° stays unmistakably red at both ends (vermillion to crimson);
// much wider and Sausalito turns orange, which is a different claim.
export const HUE_SPREAD = 30;

export function hexToHsl(hex) {
  const clean = String(hex).replace(/^#/, '');
  const r = parseInt(clean.slice(0, 2), 16) / 255;
  const g = parseInt(clean.slice(2, 4), 16) / 255;
  const b = parseInt(clean.slice(4, 6), 16) / 255;
  const max = Math.max(r, g, b);
  const min = Math.min(r, g, b);
  const l = (max + min) / 2;
  const d = max - min;
  if (d === 0) return { h: 0, s: 0, l };
  const s = l > 0.5 ? d / (2 - max - min) : d / (max + min);
  let h;
  if (max === r) h = ((g - b) / d + (g < b ? 6 : 0)) * 60;
  else if (max === g) h = ((b - r) / d + 2) * 60;
  else h = ((r - g) / d + 4) * 60;
  return { h, s, l };
}

export function hslToHex({ h, s, l }) {
  const hue = ((h % 360) + 360) % 360;
  const c = (1 - Math.abs(2 * l - 1)) * s;
  const x = c * (1 - Math.abs(((hue / 60) % 2) - 1));
  const m = l - c / 2;
  const seg = Math.floor(hue / 60) % 6;
  const rgb = [
    [c, x, 0],
    [x, c, 0],
    [0, c, x],
    [0, x, c],
    [x, 0, c],
    [c, 0, x],
  ][seg];
  const to = (v) =>
    Math.max(0, Math.min(255, Math.round((v + m) * 255)))
      .toString(16)
      .padStart(2, '0');
  return `#${to(rgb[0])}${to(rgb[1])}${to(rgb[2])}`;
}

// Shortest distance between two hues, in degrees (0..180).
export function hueGap(a, b) {
  const d = Math.abs(((a - b) % 360) + 360) % 360;
  return d > 180 ? 360 - d : d;
}

export function tooAlike(a, b) {
  // A grey has no meaningful hue, so only lightness separates it.
  const chromatic = a.s > 0.12 && b.s > 0.12;
  const hueClose = !chromatic || hueGap(a.h, b.h) < HUE_APART;
  return hueClose && Math.abs(a.l - b.l) < LIGHT_APART;
}

// routes: [{ id, color }] — returns Map(id -> hex), deterministic for a given
// input order-independently (it sorts by id first), so a re-bake never reshuffles
// the map's colours underneath a user.
export function resolveRouteColors(routes) {
  const sorted = [...routes].sort((a, b) => String(a.id).localeCompare(String(b.id)));

  const groups = new Map();
  for (const route of sorted) {
    const key = String(route.color || '').toLowerCase();
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(route);
  }

  // A route whose published colour nobody else uses is PINNED: it keeps its
  // livery exactly, and never moves to make room for anyone. Using the real
  // identity is the whole reason we read route_color at all, so the routes that
  // caused the problem are the ones that pay for it.
  const pinned = [];
  const movable = [];
  for (const [, group] of groups) {
    if (group.length === 1) {
      pinned.push({ id: group[0].id, hsl: hexToHsl(group[0].color) });
      continue;
    }
    const base = hexToHsl(group[0].color);
    const n = group.length;
    group.forEach((route, i) => {
      const t = n === 1 ? 0 : (i / (n - 1)) * 2 - 1; // -1..1
      if (base.s <= 0.12) {
        // An achromatic livery has no hue to fan, so the only axis left is
        // lightness — spread evenly rather than zigzagged, or a group of three
        // collapses to two distinct values.
        movable.push({
          id: route.id,
          hsl: { h: base.h, s: base.s, l: 0.2 + (i / Math.max(1, n - 1)) * 0.58 },
        });
        return;
      }
      // Spread mostly by LIGHTNESS, only gently by hue. Lightness is what keeps
      // five reds five reds: `tooAlike` needs hue AND lightness to be close, so
      // a lightness ladder separates them while every rung stays red. Marching
      // hue instead walked Golden Gate's reds into yellow-green, which is a
      // different service, not a distinguishable one.
      movable.push({
        id: route.id,
        hsl: {
          h: base.h + t * (HUE_SPREAD / 2),
          s: Math.min(1, base.s * (i % 2 ? 0.9 : 1)),
          // Rungs must clear LIGHT_APART with room to spare: at exactly the
          // threshold, hex rounding put a pair a thousandth under it and they
          // read as the same red.
          l: 0.2 + (i / Math.max(1, n - 1)) * 0.58,
        },
      });
    });
  }

  // Settle the movable ones around the pinned ones and each other. Walk in id
  // order so the result never depends on which route was examined first.
  const placed = [...pinned];
  // Candidate nudges, ordered by how little they disturb the authored colour.
  // Lightness moves come first and cost less than hue moves, because a lighter
  // red is still that route's red while a rotated one is another service.
  const NUDGES = [];
  for (const dl of [0, 0.14, -0.14, 0.28, -0.28, 0.42, -0.42]) {
    for (const dh of [0, 17, -17, 34, -34, 51, -51]) {
      NUDGES.push({ dl, dh, cost: Math.abs(dl) / 0.14 + (Math.abs(dh) / 17) * 1.6 });
    }
  }
  NUDGES.sort((a, b) => a.cost - b.cost);

  const minGap = (hsl) =>
    placed.reduce((worst, p) => {
      const hue = hueGap(p.hsl.h, hsl.h) / HUE_APART;
      const light = Math.abs(p.hsl.l - hsl.l) / LIGHT_APART;
      return Math.min(worst, Math.max(hue, light));
    }, Infinity);

  for (const route of movable.sort((a, b) => String(a.id).localeCompare(String(b.id)))) {
    let best = null;
    for (const nudge of NUDGES) {
      const hsl = {
        h: route.hsl.h + nudge.dh,
        s: route.hsl.s,
        l: Math.max(0.16, Math.min(0.8, route.hsl.l + nudge.dl)),
      };
      if (!placed.some((p) => tooAlike(p.hsl, hsl))) {
        best = hsl;
        break;
      }
      // Keep the roomiest option seen, in case nothing ever fully clears.
      const gap = minGap(hsl);
      if (!best || gap > best._gap) best = Object.assign(hsl, { _gap: gap });
    }
    delete best._gap;
    placed.push({ id: route.id, hsl: best });
  }

  const out = new Map(placed.map((p) => [p.id, hslToHex(p.hsl)]));
  // Emit in the caller's own order for readability of any debug dump.
  return new Map(sorted.map((r) => [r.id, out.get(r.id)]));
}
