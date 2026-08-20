// Lock for the ferry route palette (app/src/ferry-palette.js).
//
// The property under test is the whole reason the module exists: no two ferry
// routes may end up looking alike on the water. Golden Gate publishes ONE red
// for all five of its routes, so a naive "use the published colour" makes
// Sausalito, Tiburon, Larkspur, Angel Island and the Triangle indistinguishable.
//
// Run: cd app && npm test

import assert from 'node:assert/strict';
import { describe, it } from 'node:test';

import {
  HUE_SPREAD,
  hexToHsl,
  hslToHex,
  hueGap,
  resolveRouteColors,
  tooAlike,
} from '../src/ferry-palette.js';

// The real published liveries, from 511's GTFS for the four ferry operators.
// Note GF: five routes, one colour.
const REAL = [
  { id: 'SB:OAS', color: '#ffd400' },
  { id: 'SB:HB', color: '#c74a5d' },
  { id: 'SB:OA', color: '#4fab47' },
  { id: 'SB:SSF', color: '#851f83' },
  { id: 'SB:RCH', color: '#004576' },
  { id: 'SB:SEA', color: '#df7a1c' },
  { id: 'SB:VJO', color: '#008c99' },
  { id: 'GF:TRIA', color: '#cc3333' },
  { id: 'GF:AISF', color: '#cc3333' },
  { id: 'GF:LSSF', color: '#cc3333' },
  { id: 'GF:SSSF', color: '#cc3333' },
  { id: 'GF:TBSF', color: '#cc3333' },
  { id: 'AF:Tib-AIF', color: '#7ab8e4' },
  { id: 'TF:TISF', color: '#8fc2ba' },
];

describe('colour conversion round-trips', () => {
  it('survives hex -> hsl -> hex', () => {
    for (const { color } of REAL) {
      const back = hslToHex(hexToHsl(color));
      const a = hexToHsl(color);
      const b = hexToHsl(back);
      assert.ok(hueGap(a.h, b.h) < 2, `${color} -> ${back} hue drifted`);
      assert.ok(Math.abs(a.l - b.l) < 0.02, `${color} -> ${back} lightness drifted`);
    }
  });

  it('measures hue distance the short way round the wheel', () => {
    assert.equal(hueGap(350, 10), 20);
    assert.equal(hueGap(10, 350), 20);
    assert.equal(hueGap(0, 180), 180);
  });
});

describe('the whole point — every route is distinguishable', () => {
  const resolved = resolveRouteColors(REAL);

  it('returns a colour for every route', () => {
    assert.equal(resolved.size, REAL.length);
    for (const { id } of REAL) assert.match(resolved.get(id), /^#[0-9a-f]{6}$/);
  });

  it('leaves no two routes looking alike', () => {
    const entries = [...resolved.entries()];
    for (let i = 0; i < entries.length; i++) {
      for (let j = i + 1; j < entries.length; j++) {
        const [idA, hexA] = entries[i];
        const [idB, hexB] = entries[j];
        assert.ok(
          !tooAlike(hexToHsl(hexA), hexToHsl(hexB)),
          `${idA} (${hexA}) and ${idB} (${hexB}) are too alike`
        );
      }
    }
  });

  it('gives Golden Gate five different reds, not one', () => {
    const gf = REAL.filter((r) => r.id.startsWith('GF:')).map((r) => resolved.get(r.id));
    assert.equal(new Set(gf).size, 5, 'all five Golden Gate routes must differ');
  });

  it('keeps Golden Gate recognisably red rather than reassigning it', () => {
    // The published hue is ~0deg. Every GF route must stay within the spread
    // band (plus the collision nudge), i.e. still a red, not a green.
    const base = hexToHsl('#cc3333');
    for (const route of REAL.filter((r) => r.id.startsWith('GF:'))) {
      const hsl = hexToHsl(resolved.get(route.id));
      assert.ok(
        hueGap(hsl.h, base.h) <= HUE_SPREAD + 40,
        `${route.id} wandered to hue ${hsl.h.toFixed(0)} from ${base.h.toFixed(0)}`
      );
    }
  });

  it('leaves an already-unique livery alone', () => {
    // WETA's seven are distinct in the feed, so they must survive untouched —
    // using the real identity is the entire point of reading route_color.
    for (const id of ['SB:OAS', 'SB:OA', 'SB:SSF', 'SB:VJO']) {
      const want = REAL.find((r) => r.id === id).color;
      assert.equal(resolved.get(id), want, `${id} should keep its published livery`);
    }
  });

  it('is deterministic and independent of input order', () => {
    const shuffled = [...REAL].reverse();
    const again = resolveRouteColors(shuffled);
    for (const { id } of REAL) assert.equal(again.get(id), resolved.get(id), `${id} moved`);
  });
});

describe('degenerate input', () => {
  it('handles a single route', () => {
    const one = resolveRouteColors([{ id: 'X', color: '#123456' }]);
    assert.equal(one.get('X'), '#123456');
  });

  it('handles an empty set', () => {
    assert.equal(resolveRouteColors([]).size, 0);
  });

  it('separates greys by lightness, since they have no hue to move', () => {
    const greys = resolveRouteColors([
      { id: 'A', color: '#808080' },
      { id: 'B', color: '#808080' },
      { id: 'C', color: '#808080' },
    ]);
    assert.equal(new Set(greys.values()).size, 3);
  });
});
