// The lore prop vocabulary: the small shapes that make a toy building read as
// what the data says it is — a bay window, a steeple, a marquee, a loading dock.
//
// It is written once and used twice. The tile worker runs it with an emitter
// that writes into its merged geometry buffers, and the pipeline runs it with a
// counting emitter to prove the triangle budget holds before anything ships.
// That is the whole reason these recipes are plain functions over a tiny
// primitive set: box, wedge, plate, cylinder, cone, dome, and nothing else.
//
// Everything is expressed in a building-local frame: `u` runs along the facade
// the building faces (its street), `v` runs into the block, and `y` is metres
// above the ground. The frame is built from the footprint's oriented box, so a
// bay window sits on the street side of a Victorian on any heading.

export const CAT = {
  misc: 0, house: 1, apartments: 2, office: 3, retail: 4, restaurant_cafe: 5, bar: 6, hotel: 7,
  worship: 8, school: 9, university: 10, hospital: 11, clinic: 12, fire_station: 13, police: 14,
  library: 15, museum: 16, theater_cinema: 17, government: 18, industrial: 19, warehouse: 20,
  gas_station: 21, supermarket: 22, parking_garage: 23, gym: 24, transit_station: 25,
};

// Prop flag bits, baked per building alongside the category.
export const PROP = {
  STREET: 1, // a street ribbon runs within 25 m of the front face
  VEHICLE: 2, // this building won the (rationed) vehicle for its category
  TOWER: 4, // six floors or more: penthouse/plant instead of street garnish
  CORNER: 8, // two street-facing sides
  HELIPAD: 16,
};

const GLOW = 1; // marks a prop as a light source at night (sign, marquee, canopy)

// A tiny deterministic hash so every choice below is a pure function of the
// building's baked seed: the same building always grows the same props.
export function rnd(seed, salt) {
  const x = Math.sin(seed * 12.9898 + salt * 78.233) * 43758.5453;
  return x - Math.floor(x);
}

// --------------------------------------------------------------- primitives
// Every primitive emits through `ctx.face(points, ref, colour, glow)`, so the
// worker decides how a face becomes vertices and the pipeline just counts.

function shade(color, k) {
  return [
    Math.max(0, Math.min(255, Math.round(color[0] * k))),
    Math.max(0, Math.min(255, Math.round(color[1] * k))),
    Math.max(0, Math.min(255, Math.round(color[2] * k))),
  ];
}

export function makeCtx(frame, face) {
  const { cx, cz, ux, uz, vx, vz } = frame;
  // (u, v) -> world xz
  const p = (u, v, y) => [cx + ux * u + vx * v, y, cz + uz * u + vz * v];

  const ctx = {
    frame,
    face,
    p,

    // An axis-aligned box in the local frame.
    box(u0, u1, v0, v1, y0, y1, color, glow = 0) {
      const a = p(u0, v0, y0);
      const b = p(u1, v0, y0);
      const c = p(u1, v1, y0);
      const d = p(u0, v1, y0);
      const A = p(u0, v0, y1);
      const B = p(u1, v0, y1);
      const C = p(u1, v1, y1);
      const D = p(u0, v1, y1);
      const mid = p((u0 + u1) / 2, (v0 + v1) / 2, (y0 + y1) / 2);
      const ref = (q) => [q[0] - mid[0], q[1] - mid[1], q[2] - mid[2]];
      face([A, B, C, D], [0, 1, 0], shade(color, 1.06), glow);
      face([a, d, c, b], [0, -1, 0], shade(color, 0.7), 0);
      face([a, b, B, A], ref(p((u0 + u1) / 2, v0, (y0 + y1) / 2)), shade(color, 1.0), glow);
      face([c, d, D, C], ref(p((u0 + u1) / 2, v1, (y0 + y1) / 2)), shade(color, 0.86), 0);
      face([d, a, A, D], ref(p(u0, (v0 + v1) / 2, (y0 + y1) / 2)), shade(color, 0.93), glow);
      face([b, c, C, B], ref(p(u1, (v0 + v1) / 2, (y0 + y1) / 2)), shade(color, 0.93), glow);
    },

    // A flat plate (awning, canopy, sign panel, dock apron).
    plate(u0, u1, v0, v1, y, color, glow = 0) {
      face([p(u0, v0, y), p(u1, v0, y), p(u1, v1, y), p(u0, v1, y)], [0, 1, 0], color, glow);
    },

    // A vertical panel facing along v (blade sign, marquee face, banner).
    panel(u0, u1, v, y0, y1, color, glow = 0) {
      face([p(u0, v, y0), p(u1, v, y0), p(u1, v, y1), p(u0, v, y1)], [vx, 0, vz], color, glow);
      face([p(u1, v, y0), p(u0, v, y0), p(u0, v, y1), p(u1, v, y1)], [-vx, 0, -vz], shade(color, 0.9), glow);
    },

    // A ridge prism: the pitched roof over a rectangle.
    wedge(u0, u1, v0, v1, y0, y1, color) {
      const rv = (v0 + v1) / 2;
      const a = p(u0, v0, y0);
      const b = p(u1, v0, y0);
      const c = p(u1, v1, y0);
      const d = p(u0, v1, y0);
      const r0 = p(u0, rv, y1);
      const r1 = p(u1, rv, y1);
      face([a, b, r1, r0], [vx, 0.6, vz], color, 0);
      face([c, d, r0, r1], [-vx, 0.6, -vz], shade(color, 0.9), 0);
      face([d, a, r0], [-ux, 0.2, -uz], shade(color, 0.95), 0);
      face([b, c, r1], [ux, 0.2, uz], shade(color, 0.95), 0);
    },

    // An n-sided prism (stack, tank, column, bollard). Segments are capped at 8.
    cylinder(u, v, radius, y0, y1, color, segments = 6, glow = 0) {
      const n = Math.min(8, Math.max(3, segments));
      const ring = [];
      for (let i = 0; i < n; i++) {
        const a = (i / n) * Math.PI * 2;
        ring.push([u + Math.cos(a) * radius, v + Math.sin(a) * radius]);
      }
      const top = ring.map(([uu, vv]) => p(uu, vv, y1));
      face(top, [0, 1, 0], shade(color, 1.06), glow);
      for (let i = 0; i < n; i++) {
        const [u0, v0] = ring[i];
        const [u1, v1] = ring[(i + 1) % n];
        const ref = [ux * (u0 - u) + vx * (v0 - v), 0, uz * (u0 - u) + vz * (v0 - v)];
        face([p(u0, v0, y0), p(u1, v1, y0), p(u1, v1, y1), p(u0, v0, y1)], ref, color, glow);
      }
    },

    // A cone (steeple, spire, tree-like finial).
    cone(u, v, radius, y0, y1, color, segments = 6) {
      const n = Math.min(8, Math.max(3, segments));
      const apex = p(u, v, y1);
      for (let i = 0; i < n; i++) {
        const a0 = (i / n) * Math.PI * 2;
        const a1 = ((i + 1) / n) * Math.PI * 2;
        const q0 = p(u + Math.cos(a0) * radius, v + Math.sin(a0) * radius, y0);
        const q1 = p(u + Math.cos(a1) * radius, v + Math.sin(a1) * radius, y0);
        face([q0, q1, apex], [q0[0] - apex[0], 0.5, q0[2] - apex[2]], color, 0);
      }
    },

    // A dome: two stacked rings and a cap, eight segments at most.
    dome(u, v, radius, y0, height, color, segments = 6) {
      const n = Math.min(8, Math.max(3, segments));
      const mid = radius * 0.72;
      const yMid = y0 + height * 0.55;
      for (let i = 0; i < n; i++) {
        const a0 = (i / n) * Math.PI * 2;
        const a1 = ((i + 1) / n) * Math.PI * 2;
        const l0 = [u + Math.cos(a0) * radius, v + Math.sin(a0) * radius];
        const l1 = [u + Math.cos(a1) * radius, v + Math.sin(a1) * radius];
        const m0 = [u + Math.cos(a0) * mid, v + Math.sin(a0) * mid];
        const m1 = [u + Math.cos(a1) * mid, v + Math.sin(a1) * mid];
        const ref = [ux * (l0[0] - u) + vx * (l0[1] - v), 0.6, uz * (l0[0] - u) + vz * (l0[1] - v)];
        face([p(l0[0], l0[1], y0), p(l1[0], l1[1], y0), p(m1[0], m1[1], yMid), p(m0[0], m0[1], yMid)], ref, color, 0);
        face([p(m0[0], m0[1], yMid), p(m1[0], m1[1], yMid), p(u, v, y0 + height)], [ref[0], 1, ref[2]], shade(color, 1.05), 0);
      }
    },

    shade,
  };
  return ctx;
}

// ------------------------------------------------------------------ recipes
// One entry per parent category. `b` carries what the bake knows about this
// building: half-width `hu` along the street, half-depth `hv`, base and top
// elevation, wall and roof colour, the seed, and the prop flags.

const WHITE = [236, 232, 222];
const TRIM = [250, 248, 244];
const DARK = [72, 66, 62];
const GREY = [148, 146, 142];
const RED = [188, 62, 52];
const BLUE = [58, 92, 150];
const GREEN = [72, 122, 84];
const GOLD = [226, 178, 76];
const GLASS = [96, 128, 160];

// The street-facing edge sits at v = -hv; the block side is v = +hv.
const recipes = {
  // A.1 Victorian: a bay window on the street face, a cornice band, and a
  // painted-lady trim course between floors.
  [CAT.house](ctx, b) {
    const { hu, hv, base, top, seed, props, roof } = b;
    const h = top - base;
    ctx.box(-hu * 0.45, hu * 0.45, -hv - 0.9, -hv + 0.15, base + 0.6, Math.min(top - 0.4, base + h * 0.86), TRIM);
    ctx.plate(-hu - 0.35, hu + 0.35, -hv - 1.1, -hv + 0.2, top - 0.25, ctx.shade(roof, 1.02));
    if (rnd(seed, 3) > 0.45 && (props & PROP.STREET)) {
      // Stoop: three steps down to the pavement.
      for (let i = 0; i < 3; i++) {
        ctx.box(-hu * 0.3, hu * 0.3, -hv - 1.5 - i * 0.5, -hv - 0.9 - i * 0.5, base, base + 0.9 - i * 0.3, TRIM);
      }
    }
  },

  // A.3 Apartments: a zig-zag fire escape and a parapet.
  [CAT.apartments](ctx, b) {
    const { hu, hv, base, top, seed } = b;
    const floors = Math.max(2, Math.floor((top - base) / 3.5));
    const steps = Math.min(5, floors - 1);
    for (let i = 1; i <= steps; i++) {
      const y = base + i * 3.5;
      const side = i % 2 === 0 ? 1 : -1;
      ctx.plate(-hu * 0.6, hu * 0.6, -hv - 1.1, -hv - 0.1, y, DARK);
      ctx.panel(-hu * 0.6, hu * 0.6, -hv - 1.05, y, y + 0.9, DARK);
      ctx.box(side * hu * 0.45, side * hu * 0.45 + 0.18, -hv - 1.0, -hv - 0.8, y, y + 3.5, DARK);
    }
    if (rnd(seed, 7) > 0.5) ctx.box(-hu, hu, -hv, hv, top, top + 0.45, ctx.shade(b.wall, 0.92));
  },

  // A.4 Office: a setback penthouse, a plant box and a flagpole on the biggest.
  [CAT.office](ctx, b) {
    const { hu, hv, base, top, seed, props } = b;
    const inset = Math.min(hu, hv) * 0.35;
    ctx.box(-hu + inset, hu - inset, -hv + inset, hv - inset, top, top + 3.2, ctx.shade(b.wall, 0.95));
    ctx.box(-hu * 0.3, hu * 0.1, hv * 0.2, hv * 0.7, top + 3.2, top + 4.6, GREY);
    if (props & PROP.TOWER) {
      ctx.cylinder(hu * 0.5, -hv * 0.4, 0.12, top + 3.2, top + 11, GREY, 4);
      ctx.panel(hu * 0.5, hu * 0.5 + 1.6, -hv * 0.4, top + 9.2, top + 11, RED);
    }
    if (rnd(seed, 11) > 0.6) ctx.plate(-hu + 0.4, hu - 0.4, -hv - 1.4, -hv, base + 4.2, GLASS);
  },

  // A.5 Retail: awning over the shopfront, blade sign perpendicular to it.
  [CAT.retail](ctx, b) {
    const { hu, hv, base, seed, props } = b;
    const tone = [
      [214, 90, 74],
      [64, 132, 132],
      [226, 176, 70],
      [92, 106, 168],
    ][Math.floor(rnd(seed, 13) * 4)];
    ctx.plate(-hu * 0.85, hu * 0.85, -hv - 1.6, -hv, base + 3.3, tone);
    ctx.panel(-hu * 0.85, hu * 0.85, -hv - 1.55, base + 2.7, base + 3.3, ctx.shade(tone, 0.85));
    if (props & PROP.STREET) {
      ctx.box(hu * 0.55, hu * 0.6, -hv - 2.4, -hv - 0.2, base + 3.8, base + 5.6, TRIM, GLOW);
    }
  },

  // A.6 Restaurant / cafe: awning, pavement tables and a menu board.
  [CAT.restaurant_cafe](ctx, b) {
    const { hu, hv, base, seed } = b;
    const cloth = rnd(seed, 17) > 0.5 ? [212, 96, 84] : [236, 226, 208];
    ctx.plate(-hu * 0.8, hu * 0.8, -hv - 1.5, -hv, base + 3.2, cloth);
    const tables = 1 + Math.floor(rnd(seed, 19) * 2);
    for (let i = 0; i < tables; i++) {
      const u = -hu * 0.5 + (i * hu) / tables;
      ctx.cylinder(u, -hv - 2.4, 0.55, base, base + 0.75, WHITE, 6);
      ctx.cylinder(u, -hv - 2.4, 0.09, base, base + 2.2, GREY, 4);
      ctx.plate(u - 1.1, u + 1.1, -hv - 3.5, -hv - 1.3, base + 2.2, cloth);
    }
    ctx.panel(-hu * 0.8, -hu * 0.4, -hv - 1.2, base + 0.2, base + 1.4, DARK);
  },

  // A.7 Bar: a neon blade sign and a dark, glowing shopfront.
  [CAT.bar](ctx, b) {
    const { hu, hv, base } = b;
    ctx.box(-hu * 0.7, -hu * 0.65, -hv - 1.8, -hv - 0.1, base + 3.4, base + 6.4, [232, 74, 96], GLOW);
    ctx.panel(-hu * 0.85, hu * 0.85, -hv - 0.06, base + 0.4, base + 3.1, [46, 40, 44], GLOW);
    ctx.plate(-hu * 0.9, hu * 0.9, -hv - 1.0, -hv, base + 3.6, DARK);
  },

  // A.8 Hotel: a porte-cochere over the entrance and a roof sign.
  [CAT.hotel](ctx, b) {
    const { hu, hv, base, top } = b;
    ctx.plate(-hu * 0.5, hu * 0.5, -hv - 4.2, -hv, base + 4.4, ctx.shade(b.wall, 0.9));
    ctx.cylinder(-hu * 0.45, -hv - 3.8, 0.2, base, base + 4.4, GREY, 5);
    ctx.cylinder(hu * 0.45, -hv - 3.8, 0.2, base, base + 4.4, GREY, 5);
    ctx.panel(-hu * 0.6, hu * 0.6, -hv * 0.2, top + 0.2, top + 2.6, GOLD, GLOW);
  },

  // A.9 Worship: steeple or dome, and a small entry porch.
  [CAT.worship](ctx, b) {
    const { hu, hv, base, top, seed, sub, roof } = b;
    const r = Math.min(hu, hv);
    if (sub === 'cathedral' || rnd(seed, 23) > 0.75) {
      ctx.dome(0, 0, r * 0.55, top, r * 0.9, ctx.shade(roof, 1.02), 8);
      ctx.cylinder(0, 0, 0.16, top + r * 0.9, top + r * 1.25, GOLD, 4);
    } else {
      const steepleBase = top + 0.4;
      ctx.box(-r * 0.28, r * 0.28, -hv * 0.6, -hv * 0.6 + r * 0.56, steepleBase, steepleBase + r * 1.1, ctx.shade(b.wall, 1.04));
      ctx.cone(0, -hv * 0.6 + r * 0.28, r * 0.34, steepleBase + r * 1.1, steepleBase + r * 2.2, ctx.shade(roof, 0.95), 6);
    }
    ctx.plate(-hu * 0.35, hu * 0.35, -hv - 2.2, -hv, base + 3.6, ctx.shade(roof, 0.98));
  },

  // A.10 School: a flagpole, a canopy walk and a yard fence.
  [CAT.school](ctx, b) {
    const { hu, hv, base, top } = b;
    ctx.cylinder(-hu * 0.8, -hv - 3.0, 0.1, base, base + 9, GREY, 4);
    ctx.panel(-hu * 0.8, -hu * 0.8 + 1.5, -hv - 3.0, base + 7.4, base + 9, RED);
    ctx.plate(-hu * 0.6, hu * 0.6, -hv - 2.6, -hv, base + 3.4, ctx.shade(b.roof, 1.0));
    ctx.box(-hu * 0.2, hu * 0.2, -hv * 0.1, hv * 0.1, top, top + 1.4, WHITE);
  },

  // A.11 University: a colonnade and a small clock tower.
  [CAT.university](ctx, b) {
    const { hu, hv, base, top } = b;
    const columns = Math.min(6, Math.max(3, Math.round(hu / 3)));
    for (let i = 0; i < columns; i++) {
      const u = -hu * 0.8 + (i / (columns - 1)) * hu * 1.6;
      ctx.cylinder(u, -hv - 1.2, 0.32, base, base + 5.4, TRIM, 6);
    }
    ctx.plate(-hu * 0.9, hu * 0.9, -hv - 2.0, -hv, base + 5.6, TRIM);
    ctx.box(-hu * 0.16, hu * 0.16, -hv * 0.16, hv * 0.16, top, top + 4.5, ctx.shade(b.wall, 1.03));
    ctx.cone(0, 0, hu * 0.2, top + 4.5, top + 6.6, ctx.shade(b.roof, 0.95), 6);
  },

  // A.12 Hospital: an emergency canopy, a red cross and (sometimes) a helipad.
  [CAT.hospital](ctx, b) {
    const { hu, hv, base, top, props } = b;
    ctx.plate(-hu * 0.55, hu * 0.55, -hv - 5.0, -hv, base + 4.6, WHITE);
    ctx.cylinder(-hu * 0.5, -hv - 4.5, 0.22, base, base + 4.6, GREY, 5);
    ctx.cylinder(hu * 0.5, -hv - 4.5, 0.22, base, base + 4.6, GREY, 5);
    ctx.panel(-0.9, 0.9, -hv - 0.05, base + 5.2, base + 6.4, RED, GLOW);
    ctx.panel(-0.35, 0.35, -hv - 0.06, base + 4.9, base + 6.7, RED, GLOW);
    if (props & PROP.HELIPAD) {
      const r = Math.min(hu, hv) * 0.55;
      ctx.cylinder(0, 0, r, top, top + 0.25, [64, 64, 68], 8);
      ctx.cylinder(0, 0, r * 0.55, top + 0.25, top + 0.33, WHITE, 8);
    }
    if (props & PROP.VEHICLE) vehicle(ctx, b, WHITE, RED);
  },

  // A.13 Clinic: a small canopy and a shingle by the door.
  [CAT.clinic](ctx, b) {
    const { hu, hv, base } = b;
    ctx.plate(-hu * 0.35, hu * 0.35, -hv - 1.8, -hv, base + 3.4, WHITE);
    ctx.panel(hu * 0.4, hu * 0.75, -hv - 0.08, base + 2.6, base + 3.6, [92, 150, 148]);
  },

  // A.14 Fire station: bay doors, an apron and an engine.
  [CAT.fire_station](ctx, b) {
    const { hu, hv, base, props } = b;
    const bays = hu > 9 ? 2 : 1;
    for (let i = 0; i < bays; i++) {
      const c = bays === 1 ? 0 : -hu * 0.45 + i * hu * 0.9;
      ctx.panel(c - hu * 0.32, c + hu * 0.32, -hv - 0.08, base + 0.2, base + 4.4, RED);
      ctx.box(c - hu * 0.34, c + hu * 0.34, -hv - 0.24, -hv - 0.1, base + 4.4, base + 4.8, DARK);
    }
    ctx.plate(-hu, hu, -hv - 4.5, -hv, base + 0.06, [118, 116, 114]);
    if (props & PROP.VEHICLE) vehicle(ctx, b, RED, [210, 210, 210]);
  },

  // A.15 Police: a blue lamp by the door and a cruiser.
  [CAT.police](ctx, b) {
    const { hu, hv, base, props } = b;
    ctx.box(-0.35, 0.35, -hv - 0.7, -hv - 0.05, base + 3.2, base + 4.1, [60, 96, 200], GLOW);
    ctx.plate(-hu * 0.5, hu * 0.5, -hv - 2.0, -hv, base + 4.3, ctx.shade(b.wall, 0.9));
    if (props & PROP.VEHICLE) vehicle(ctx, b, [246, 246, 248], [40, 62, 140]);
  },

  // A.16 Library: a book-return box and a stepped entrance.
  [CAT.library](ctx, b) {
    const { hu, hv, base } = b;
    ctx.box(hu * 0.55, hu * 0.55 + 0.9, -hv - 2.0, -hv - 1.1, base, base + 1.3, GREEN);
    ctx.box(-hu * 0.45, hu * 0.45, -hv - 1.6, -hv, base, base + 0.45, TRIM);
    ctx.plate(-hu * 0.5, hu * 0.5, -hv - 2.2, -hv, base + 4.6, ctx.shade(b.roof, 1.0));
  },

  // A.17 Museum: a colonnade, a banner pair and a plinth sculpture.
  [CAT.museum](ctx, b) {
    const { hu, hv, base, seed } = b;
    for (let i = 0; i < 4; i++) {
      const u = -hu * 0.75 + (i / 3) * hu * 1.5;
      ctx.cylinder(u, -hv - 1.4, 0.38, base, base + 6.2, TRIM, 6);
    }
    ctx.plate(-hu * 0.9, hu * 0.9, -hv - 2.2, -hv, base + 6.4, TRIM);
    ctx.panel(-hu * 0.55, -hu * 0.2, -hv - 1.5, base + 2.6, base + 6.0, rnd(seed, 29) > 0.5 ? RED : BLUE);
    ctx.panel(hu * 0.2, hu * 0.55, -hv - 1.5, base + 2.6, base + 6.0, GOLD);
    ctx.cylinder(0, -hv - 3.4, 0.7, base, base + 1.1, GREY, 6);
    ctx.cone(0, -hv - 3.4, 0.55, base + 1.1, base + 3.0, [120, 128, 118], 5);
  },

  // A.18 Theatre / cinema: a marquee that lights up, and a vertical blade.
  [CAT.theater_cinema](ctx, b) {
    const { hu, hv, base, top } = b;
    ctx.box(-hu * 0.85, hu * 0.85, -hv - 2.6, -hv, base + 4.2, base + 6.2, [40, 36, 40], GLOW);
    ctx.plate(-hu * 0.9, hu * 0.9, -hv - 2.8, -hv, base + 4.1, GOLD, GLOW);
    ctx.box(-0.22, 0.22, -hv - 1.4, -hv - 0.4, base + 6.2, Math.max(base + 12, top - 1), [214, 62, 74], GLOW);
  },

  // A.19 Government: a dome or a pediment, and a flag pair.
  [CAT.government](ctx, b) {
    const { hu, hv, base, top, seed } = b;
    const r = Math.min(hu, hv);
    if (rnd(seed, 31) > 0.55) {
      ctx.cylinder(0, 0, r * 0.5, top, top + r * 0.25, TRIM, 8);
      ctx.dome(0, 0, r * 0.48, top + r * 0.25, r * 0.85, ctx.shade(b.roof, 1.05), 8);
    } else {
      ctx.wedge(-hu * 0.7, hu * 0.7, -hv - 0.6, -hv + hv * 0.35, top, top + 2.2, TRIM);
    }
    ctx.cylinder(-hu * 0.7, -hv - 1.6, 0.1, base, base + 8, GREY, 4);
    ctx.cylinder(hu * 0.7, -hv - 1.6, 0.1, base, base + 8, GREY, 4);
    ctx.plate(-hu * 0.55, hu * 0.55, -hv - 2.4, -hv, base + 5.4, TRIM);
  },

  // A.20 Industrial: stacks, tanks and a pipe run.
  [CAT.industrial](ctx, b) {
    const { hu, hv, base, top, seed } = b;
    ctx.cylinder(-hu * 0.5, hv * 0.3, Math.min(1.1, hu * 0.16), top, top + 7 + rnd(seed, 37) * 5, [126, 122, 118], 6);
    ctx.cylinder(-hu * 0.5, hv * 0.3, Math.min(1.25, hu * 0.18), top + 6.4, top + 7.1, DARK, 6);
    ctx.cylinder(hu * 0.45, hv * 0.45, Math.min(2.4, hu * 0.3), base, base + 6.2, [176, 172, 164], 8);
    ctx.dome(hu * 0.45, hv * 0.45, Math.min(2.4, hu * 0.3), base + 6.2, 1.4, [186, 182, 174], 8);
    ctx.box(-hu * 0.2, hu * 0.2, hv * 0.1, hv * 0.16, top + 0.4, top + 0.8, [150, 146, 140]);
  },

  // A.21 Warehouse: loading docks, a ramp and a box truck.
  [CAT.warehouse](ctx, b) {
    const { hu, hv, base, props } = b;
    const docks = Math.min(4, Math.max(2, Math.round(hu / 5)));
    for (let i = 0; i < docks; i++) {
      const u = -hu * 0.75 + (i / (docks - 1)) * hu * 1.5;
      ctx.panel(u - 1.3, u + 1.3, -hv - 0.07, base + 0.9, base + 4.2, [88, 92, 96]);
      ctx.plate(u - 1.5, u + 1.5, -hv - 1.1, -hv, base + 0.9, GREY);
    }
    ctx.plate(-hu, hu, -hv - 6, -hv, base + 0.05, [116, 114, 112]);
    if (props & PROP.VEHICLE) vehicle(ctx, b, [226, 224, 220], [90, 92, 96], 6.5);
  },

  // A.22 Gas station: a lit canopy on posts, with pumps beneath it.
  [CAT.gas_station](ctx, b) {
    const { hu, hv, base } = b;
    const cu = Math.max(4, hu * 0.9);
    const cv = Math.max(4, hv * 0.9);
    ctx.box(-cu, cu, -cv - 3, cv * 0.2, base + 4.6, base + 5.4, WHITE, GLOW);
    ctx.plate(-cu, cu, -cv - 3, cv * 0.2, base + 4.55, [255, 250, 236], GLOW);
    for (const su of [-cu * 0.8, cu * 0.8]) {
      ctx.cylinder(su, -cv - 1.4, 0.22, base, base + 4.6, GREY, 5);
      ctx.box(su - 0.5, su + 0.5, -cv - 1.9, -cv - 0.9, base, base + 1.6, [214, 74, 66]);
    }
  },

  // A.23 Supermarket: a cart corral, a roof HVAC bank and a fascia sign.
  [CAT.supermarket](ctx, b) {
    const { hu, hv, base, top } = b;
    ctx.panel(-hu * 0.6, hu * 0.6, -hv - 0.06, top - 2.4, top - 0.6, [64, 116, 176], GLOW);
    ctx.plate(-hu * 0.7, hu * 0.7, -hv - 2.6, -hv, base + 4.0, ctx.shade(b.wall, 0.92));
    for (let i = 0; i < 3; i++) {
      ctx.box(-hu * 0.6 + i * hu * 0.45, -hu * 0.3 + i * hu * 0.45, hv * 0.1, hv * 0.5, top, top + 1.3, [176, 174, 170]);
    }
    ctx.box(hu * 0.55, hu * 0.85, -hv - 4.2, -hv - 2.4, base, base + 1.1, [180, 180, 184]);
  },

  // A.24 Parking garage: open deck bands and a ramp stripe.
  [CAT.parking_garage](ctx, b) {
    const { hu, hv, base, top } = b;
    const decks = Math.max(1, Math.floor((top - base) / 3.2));
    for (let i = 1; i <= Math.min(6, decks); i++) {
      const y = base + i * 3.2;
      ctx.panel(-hu * 0.95, hu * 0.95, -hv - 0.05, y - 0.35, y, [70, 70, 74]);
    }
    ctx.panel(-hu * 0.3, hu * 0.3, -hv - 0.07, base + 0.3, base + 2.6, [40, 40, 44]);
    ctx.plate(-hu * 0.32, hu * 0.32, -hv - 2.4, -hv, base + 0.06, [88, 88, 92]);
  },

  // A.25 Gym: a glazed frontage band and a window sign.
  [CAT.gym](ctx, b) {
    const { hu, hv, base } = b;
    ctx.panel(-hu * 0.8, hu * 0.8, -hv - 0.06, base + 1.2, base + 4.6, GLASS);
    ctx.panel(-hu * 0.3, hu * 0.3, -hv - 0.09, base + 4.8, base + 5.6, [232, 108, 62], GLOW);
  },

  // A.26 Transit station: a portal head-house, a canopy and a pylon.
  [CAT.transit_station](ctx, b) {
    const { hu, hv, base, sub } = b;
    ctx.box(-hu * 0.35, hu * 0.35, -hv - 3.2, -hv - 0.6, base, base + 3.0, ctx.shade(b.wall, 1.04));
    ctx.wedge(-hu * 0.38, hu * 0.38, -hv - 3.4, -hv - 0.4, base + 3.0, base + 3.9, ctx.shade(b.roof, 1.0));
    ctx.cylinder(hu * 0.6, -hv - 2.2, 0.16, base, base + 5.2, GREY, 4);
    const tone = sub === 'bart_station' ? [60, 104, 176] : sub === 'ferry_terminal' ? [70, 140, 150] : [200, 76, 60];
    ctx.panel(hu * 0.6, hu * 0.6 + 1.4, -hv - 2.2, base + 3.6, base + 5.2, tone, GLOW);
  },
};

// The rationed vehicle: a two-box toy car parked at the kerb. Never more than
// one per building, and only where the bake granted PROP.VEHICLE.
function vehicle(ctx, b, body, trim, length = 4.4) {
  const { hu, hv, base } = b;
  const u0 = -Math.min(hu * 0.6, length / 2);
  const u1 = u0 + length;
  ctx.box(u0, u1, -hv - 3.4, -hv - 1.6, base + 0.25, base + 1.35, body);
  ctx.box(u0 + length * 0.22, u1 - length * 0.2, -hv - 3.2, -hv - 1.8, base + 1.35, base + 2.05, trim);
  for (const wu of [u0 + 0.7, u1 - 0.7]) {
    ctx.cylinder(wu, -hv - 3.3, 0.34, base, base + 0.25, DARK, 5);
    ctx.cylinder(wu, -hv - 1.7, 0.34, base, base + 0.25, DARK, 5);
  }
}

// A.27 The catch-all garnish for `misc` and anything with a flat roof left
// bare: a HVAC box, a stair bulkhead, and occasionally solar or a roof garden.
function garnish(ctx, b) {
  const { hu, hv, top, seed } = b;
  const r = rnd(seed, 41);
  ctx.box(-hu * 0.3, hu * 0.05, -hv * 0.1, hv * 0.35, top, top + 1.1, [172, 170, 166]);
  ctx.box(hu * 0.3, hu * 0.62, -hv * 0.5, -hv * 0.15, top, top + 1.9, ctx.shade(b.wall, 0.96));
  if (r > 0.72) {
    for (let i = 0; i < 3; i++) {
      ctx.plate(-hu * 0.7 + i * hu * 0.45, -hu * 0.35 + i * hu * 0.45, hv * 0.15, hv * 0.6, top + 0.5, [42, 54, 82]);
    }
  } else if (r > 0.5) {
    ctx.box(-hu * 0.7, -hu * 0.1, hv * 0.2, hv * 0.7, top, top + 0.35, [86, 128, 84]);
  }
}

// Everything the worker needs: give it a building and it emits that building's
// props. Buildings too small to carry a prop legibly get nothing at all.
export function emitProps(ctx, b) {
  if (b.hu < 2.2 || b.hv < 2.2 || b.top - b.base < 3) return;
  const recipe = recipes[b.cat];
  if (recipe) recipe(ctx, b);
  // A tower's roof plant reads at any distance; low buildings get street props
  // from their recipe and a light garnish only when the recipe left the roof bare.
  if (!recipe || b.cat === CAT.misc || (b.props & PROP.TOWER) === 0) {
    if (b.hu > 3.5 && b.hv > 3.5 && rnd(b.seed, 43) > 0.35) garnish(ctx, b);
  }
}

export const RECIPE_CATEGORIES = Object.keys(recipes).map(Number);
