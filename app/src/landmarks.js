// The fifteen bespoke landmarks. Each one is hand-modelled at its true
// coordinates, sitting on the baked terrain, at real height — the procedural
// bake left an exclusion hole for every one of them.

import { Group, Vector3 } from 'three';
import { Kit, updateLandmarkGlow } from './kit.js';

const DEG = Math.PI / 180;
// Local +Z points south, so a shape facing compass bearing B needs this yaw.
const bearing = (deg) => Math.PI - deg * DEG;

const ORANGE = '#c0492a';
const CABLE = '#9d3b22';
const CONCRETE = '#cfc7b6';
const STEEL = '#8d9299';
const WHITE = '#efe9dd';
const GLASS = '#9fb6c4';
const ROOF = '#5b4b41';
const LAMP = '#ffcf8a';

// ---------------------------------------------------------------- bridges ---
// Shared suspension-bridge builder: deck ribbon draped along a polyline,
// towers, catenary main cables, vertical suspenders and a night necklace.
function suspensionBridge(kit, { nodes, towers, deckWidth, towerHeight, deckColor, towerColor, sag }) {
  const path = nodes.map((n) => new Vector3(n[0], n[1], n[2]));

  // Deck: quads between consecutive nodes, with a low parapet on each side.
  for (let i = 0; i < path.length - 1; i++) {
    const a = path[i];
    const b = path[i + 1];
    const mid = a.clone().add(b).multiplyScalar(0.5);
    const dx = b.x - a.x;
    const dz = b.z - a.z;
    const len = Math.hypot(dx, dz);
    const yaw = Math.atan2(dx, dz);
    const rise = b.y - a.y;
    kit.box(deckWidth, 2.6, Math.hypot(len, rise), deckColor, {
      x: mid.x,
      y: mid.y,
      z: mid.z,
      rotY: yaw,
      rotX: -Math.atan2(rise, len),
    });
    kit.box(0.7, 1.6, Math.hypot(len, rise), STEEL, {
      x: mid.x + Math.cos(yaw) * (deckWidth / 2),
      y: mid.y + 2,
      z: mid.z - Math.sin(yaw) * (deckWidth / 2),
      rotY: yaw,
    });
    kit.box(0.7, 1.6, Math.hypot(len, rise), STEEL, {
      x: mid.x - Math.cos(yaw) * (deckWidth / 2),
      y: mid.y + 2,
      z: mid.z + Math.sin(yaw) * (deckWidth / 2),
      rotY: yaw,
    });
    // Under-deck truss.
    kit.box(deckWidth * 0.8, 4.5, Math.hypot(len, rise), STEEL, {
      x: mid.x,
      y: mid.y - 3.4,
      z: mid.z,
      rotY: yaw,
      rotX: -Math.atan2(rise, len),
    });
  }

  // Towers: two stepped legs braced by cross members.
  for (const tower of towers) {
    const [tx, , tz] = tower.at;
    const yaw = tower.yaw;
    const legOffset = deckWidth / 2 - 2;
    for (const side of [-1, 1]) {
      const lx = tx + Math.cos(yaw) * legOffset * side;
      const lz = tz - Math.sin(yaw) * legOffset * side;
      let y = 0;
      const segments = 5;
      for (let s = 0; s < segments; s++) {
        const h = towerHeight / segments;
        const w = 9 - s * 1.1;
        kit.box(w, h * 0.98, w, towerColor, { x: lx, y: y + h / 2, z: lz, rotY: yaw });
        y += h;
      }
    }
    // Cross braces, including the portal below the deck.
    for (const frac of [0.16, 0.42, 0.62, 0.84, 0.97]) {
      const y = towerHeight * frac;
      kit.box(legOffset * 2, 4.5, 5, towerColor, { x: tx, y, z: tz, rotY: yaw });
    }
  }

  // Main cables: catenary between anchorages and tower tops.
  const anchors = [path[0], ...towers.map((t) => new Vector3(t.at[0], towerHeight - 8, t.at[2])), path[path.length - 1]];
  for (const side of [-1, 1]) {
    for (let i = 0; i < anchors.length - 1; i++) {
      const a = anchors[i];
      const b = anchors[i + 1];
      const yaw = Math.atan2(b.x - a.x, b.z - a.z);
      const ox = Math.cos(yaw) * (deckWidth / 2 - 1.5) * side;
      const oz = -Math.sin(yaw) * (deckWidth / 2 - 1.5) * side;
      const span = a.distanceTo(b);
      const dip = i === 0 || i === anchors.length - 2 ? sag * 0.35 : sag;
      const points = [];
      const steps = 14;
      for (let s = 0; s <= steps; s++) {
        const t = s / steps;
        const x = a.x + (b.x - a.x) * t + ox;
        const z = a.z + (b.z - a.z) * t + oz;
        // Parabolic sag between the two supports.
        const y = a.y + (b.y - a.y) * t - Math.sin(Math.PI * t) * dip;
        points.push([x, y, z]);
        // Suspenders down to the deck, plus the night-time necklace lights.
        if (s > 0 && s < steps && span > 200) {
          const deckY = deckLevelAt(path, x, z);
          kit.strut([x, y, z], [x, deckY + 1.5, z], 0.35, CABLE);
          kit.glowSphere(1.5, LAMP, { x, y: y + 1.5, z });
        }
      }
      kit.tube(points, 1.5, CABLE, 4);
    }
  }
}

// Deck elevation at an arbitrary point: nearest-segment interpolation.
function deckLevelAt(path, x, z) {
  let best = path[0].y;
  let bestDist = Infinity;
  for (let i = 0; i < path.length - 1; i++) {
    const a = path[i];
    const b = path[i + 1];
    const dx = b.x - a.x;
    const dz = b.z - a.z;
    const l2 = dx * dx + dz * dz || 1;
    const t = Math.min(1, Math.max(0, ((x - a.x) * dx + (z - a.z) * dz) / l2));
    const px = a.x + dx * t;
    const pz = a.z + dz * t;
    const d = (x - px) ** 2 + (z - pz) ** 2;
    if (d < bestDist) {
      bestDist = d;
      best = a.y + (b.y - a.y) * t;
    }
  }
  return best;
}

// Deck nodes and tower anchors as baked by pipeline/bridges.mjs: real OSM
// centrelines, real tower positions, deck profile that meets both abutments.
function bakedBridge(ctx) {
  const spec = ctx.bridge;
  const p = (lon, lat, y) => {
    const [x, z] = ctx.project(lon, lat);
    return [x, y, z];
  };
  const nodes = spec.nodes.map(([lon, lat, y]) => p(lon, lat, y));
  const anchors = spec.towers.map(([lon, lat]) => p(lon, lat, 0));
  const first = anchors[0] ?? nodes[0];
  const last = anchors[anchors.length - 1] ?? nodes[nodes.length - 1];
  const yaw = Math.atan2(last[0] - first[0], last[2] - first[2]);
  return { spec, p, nodes, towers: anchors.map((at) => ({ at, yaw })), yaw };
}

const builders = {
  // 1,280 m main span, 227 m towers, deck 67 m over the strait, International
  // Orange. Geometry comes from the baked OSM centreline.
  goldenGateBridge(ctx) {
    const kit = new Kit(160);
    const { spec, nodes, towers } = bakedBridge(ctx);
    suspensionBridge(kit, {
      nodes,
      towers,
      deckWidth: spec.deckWidth,
      towerHeight: spec.towerHeight,
      deckColor: ORANGE,
      towerColor: ORANGE,
      sag: spec.sag,
    });
    // Aircraft beacons on the tower tops.
    for (const t of towers) {
      kit.glowSphere(3, '#ff5544', { x: t.at[0], y: spec.towerHeight + 2, z: t.at[2] });
    }
    return kit.finish('goldenGateBridge');
  },

  // West span double suspension into Yerba Buena, tunnel, then the east span's
  // single self-anchored tower toward Oakland.
  bayBridge(ctx) {
    const kit = new Kit(150);
    const { spec, p, nodes, towers, yaw } = bakedBridge(ctx);
    suspensionBridge(kit, {
      nodes,
      towers,
      deckWidth: spec.deckWidth,
      towerHeight: spec.towerHeight,
      deckColor: '#9aa0a6',
      towerColor: '#9aa0a6',
      sag: spec.sag,
    });

    // Yerba Buena tunnel portal at the west end of the east span.
    const portal = p(...spec.portal);
    kit.box(26, 16, 40, CONCRETE, { x: portal[0], y: portal[1] + 4, z: portal[2], rotY: yaw });

    // East span: skyway on concrete columns, then the self-anchored tower.
    const east = spec.east.nodes.map(([lon, lat, y]) => p(lon, lat, y));
    let sinceColumn = Infinity;
    for (let i = 0; i < east.length - 1; i++) {
      const a = east[i];
      const b = east[i + 1];
      const dx = b[0] - a[0];
      const dz = b[2] - a[2];
      const len = Math.hypot(dx, dz);
      if (len < 0.5) continue;
      const rise = b[1] - a[1];
      kit.box(spec.east.deckWidth, 2.6, Math.hypot(len, rise), '#9aa0a6', {
        x: (a[0] + b[0]) / 2,
        y: (a[1] + b[1]) / 2,
        z: (a[2] + b[2]) / 2,
        rotY: Math.atan2(dx, dz),
        rotX: -Math.atan2(rise, len),
      });
      sinceColumn += len;
      if (sinceColumn >= 120) {
        sinceColumn = 0;
        const groundY = Math.min(a[1] - 4, Math.max(-8, ctx.sampleElevation(a[0], a[2])));
        kit.box(9, a[1] - groundY, 9, CONCRETE, { x: a[0], y: (a[1] + groundY) / 2, z: a[2] });
      }
    }
    const eastTower = p(...spec.east.tower, 0);
    const towerTop = spec.east.towerHeight;
    kit.box(9, towerTop, 9, WHITE, { x: eastTower[0], y: towerTop / 2, z: eastTower[2] });
    kit.tube(
      [
        [east[0][0], east[0][1], east[0][2]],
        [eastTower[0], towerTop * 0.94, eastTower[2]],
        [east[east.length - 1][0], east[east.length - 1][1], east[east.length - 1][2]],
      ],
      1.4,
      '#d8d3c8',
      4
    );
    kit.glowSphere(3, '#ff5544', { x: eastTower[0], y: towerTop + 2, z: eastTower[2] });
    return kit.finish('bayBridge');
  },

  // 326 m, tapered glass shaft with the lantern crown.
  salesforceTower(ctx) {
    const kit = new Kit(200);
    const { x, z, y } = ctx;
    kit.box(58, 14, 58, '#b9b2a6', { x, y: y + 7, z, rotY: 12 * DEG });
    kit.glassCylinder(15.5, 25, 274, GLASS, { x, y: y + 14 + 137, z, rotY: 12 * DEG }, y + 14, 20);
    // Crown: perforated lattice fins above the top occupied floor.
    for (let i = 0; i < 20; i++) {
      const a = (i / 20) * Math.PI * 2;
      kit.box(1.6, 38, 3.2, '#cfd6dc', {
        x: x + Math.cos(a) * 14,
        y: y + 288 + 19,
        z: z + Math.sin(a) * 14,
        rotY: -a,
      });
    }
    kit.glowSphere(2.4, '#cfe4ff', { x, y: y + 326, z });
    return kit.finish('salesforceTower');
  },

  // 260 m: quartz-clad pyramid on a plaza base, with the two shoulder wings.
  transamerica(ctx) {
    const kit = new Kit(210);
    const { x, z, y } = ctx;
    const rot = 45 * DEG;
    kit.box(64, 12, 64, '#d7d2c6', { x, y: y + 6, z, rotY: rot });
    // Frustum via a 4-sided cone truncated by scale: model as stacked slabs so
    // the taper is visibly stepped like the real spandrel bands.
    const shaftTop = 212;
    const steps = 26;
    for (let i = 0; i < steps; i++) {
      const t0 = i / steps;
      const t1 = (i + 1) / steps;
      const w0 = 45 * (1 - t0) + 4 * t0;
      const h = (shaftTop - 12) / steps;
      kit.box(w0, h * 1.02, w0, i % 2 === 0 ? '#e8e4d9' : '#d5d0c3', {
        x,
        y: y + 12 + t0 * (shaftTop - 12) + h / 2,
        z,
        rotY: rot,
      });
      void t1;
    }
    // Shoulder wings holding the lifts.
    for (const side of [-1, 1]) {
      kit.box(9, 132, 22, '#dcd7cb', { x: x + side * 17, y: y + 78, z, rotY: rot });
    }
    kit.box(5, 40, 5, '#e8e4d9', { x, y: y + shaftTop + 20, z, rotY: rot });
    kit.glowSphere(2, '#ffe6b0', { x, y: y + 260, z });
    return kit.finish('transamerica');
  },

  // 64 m fluted cylinder on Telegraph Hill.
  coitTower(ctx) {
    const kit = new Kit(120);
    const { x, z, y } = ctx;
    kit.cylinder(9.5, 11, 6, '#d9d2c2', { x, y: y + 3, z }, 16);
    kit.cylinder(7.4, 8.6, 48, '#e2dbca', { x, y: y + 30, z }, 20);
    // Flutes.
    for (let i = 0; i < 18; i++) {
      const a = (i / 18) * Math.PI * 2;
      kit.box(1.1, 48, 1.1, '#cec7b6', { x: x + Math.cos(a) * 8, y: y + 30, z: z + Math.sin(a) * 8 });
    }
    kit.cylinder(8.2, 7.6, 7, '#d6cfbe', { x, y: y + 57, z }, 20);
    // Open observation arches.
    for (let i = 0; i < 8; i++) {
      const a = (i / 8) * Math.PI * 2;
      kit.box(2.4, 6, 2.4, '#c8c1b0', { x: x + Math.cos(a) * 7.2, y: y + 57, z: z + Math.sin(a) * 7.2 });
    }
    kit.cylinder(6.6, 8.2, 3, '#cdc6b5', { x, y: y + 62, z }, 20);
    kit.glowSphere(1.6, LAMP, { x, y: y + 64, z });
    return kit.finish('coitTower');
  },

  // 298 m three-legged lattice, red/white banded.
  sutroTower(ctx) {
    const kit = new Kit(90);
    const { x, z, y } = ctx;
    const legs = [];
    for (let i = 0; i < 3; i++) {
      const a = (i / 3) * Math.PI * 2 - Math.PI / 2;
      legs.push([x + Math.cos(a) * 48, z + Math.sin(a) * 48]);
    }
    const waist = 150;
    const top = 298;
    const bands = 22;
    for (const [lx, lz] of legs) {
      for (let s = 0; s < bands; s++) {
        const t0 = s / bands;
        const t1 = (s + 1) / bands;
        const h0 = t0 * top;
        const h1 = t1 * top;
        const k0 = h0 < waist ? 1 - (h0 / waist) * 0.82 : 0.18;
        const k1 = h1 < waist ? 1 - (h1 / waist) * 0.82 : 0.18;
        const p0 = [x + (lx - x) * k0, y + h0, z + (lz - z) * k0];
        const p1 = [x + (lx - x) * k1, y + h1, z + (lz - z) * k1];
        kit.strut(p0, p1, 2.1, s % 2 === 0 ? '#c8442e' : '#eae5da');
        // Inward lacing toward the mast axis.
        kit.strut(p1, [x + (lx - x) * k1 * 0.4, y + h1, z + (lz - z) * k1 * 0.4], 0.9, '#b9b3a6');
      }
    }
    for (let s = 1; s < bands; s++) {
      const t = s / bands;
      const h = t * top;
      const k = h < waist ? 1 - (h / waist) * 0.82 : 0.18;
      for (let i = 0; i < 3; i++) {
        const a = legs[i];
        const b = legs[(i + 1) % 3];
        kit.strut(
          [x + (a[0] - x) * k, y + h, z + (a[1] - z) * k],
          [x + (b[0] - x) * k, y + h, z + (b[1] - z) * k],
          0.8,
          '#c9c3b6'
        );
      }
    }
    // The three cross arms carrying the broadcast antennas.
    for (const [h, span] of [
      [186, 30],
      [214, 26],
      [242, 20],
    ]) {
      for (let i = 0; i < 3; i++) {
        const a = (i / 3) * Math.PI * 2 - Math.PI / 2;
        kit.box(span, 2.2, 2.4, '#d8d3c8', {
          x: x + Math.cos(a) * span * 0.35,
          y: y + h,
          z: z + Math.sin(a) * span * 0.35,
          rotY: -a,
        });
      }
    }
    kit.glowSphere(3, '#ff5544', { x, y: y + top + 3, z });
    return kit.finish('sutroTower');
  },

  // 1898 arcade with the 74 m clock tower on the Embarcadero.
  ferryBuilding(ctx) {
    const kit = new Kit(140);
    const { x, z, y } = ctx;
    const yaw = bearing(24); // long axis runs NNE along the Embarcadero
    const cos = Math.cos(yaw);
    const sin = Math.sin(yaw);
    const along = (d) => [x + sin * d, z + cos * d];

    kit.box(34, 19, 200, '#dcd4c0', { x, y: y + 9.5, z, rotY: yaw });
    kit.box(37, 2.4, 204, '#c3b9a2', { x, y: y + 20, z, rotY: yaw });
    // Arcade arches down both long facades.
    for (let d = -92; d <= 92; d += 8) {
      const [ax, az] = along(d);
      for (const side of [-1, 1]) {
        kit.box(2.4, 13, 3.2, '#cfc6b0', {
          x: ax + cos * 17 * side,
          y: y + 7,
          z: az - sin * 17 * side,
          rotY: yaw,
        });
      }
    }
    // Clock tower, modelled on the Giralda.
    kit.box(19, 46, 19, '#e2dac6', { x, y: y + 23, z, rotY: yaw });
    kit.box(15, 14, 15, '#ded6c2', { x, y: y + 53, z, rotY: yaw });
    for (const side of [-1, 1]) {
      kit.box(0.6, 7, 7, '#2b2b2b', { x: x + cos * 7.6 * side, y: y + 55, z: z - sin * 7.6 * side, rotY: yaw });
      kit.box(7, 7, 0.6, '#2b2b2b', { x: x + sin * 7.6 * side, y: y + 55, z: z + cos * 7.6 * side, rotY: yaw });
      kit.glowSphere(1.1, LAMP, { x: x + cos * 8 * side, y: y + 55, z: z - sin * 8 * side });
    }
    kit.box(11, 9, 11, '#d8d0bc', { x, y: y + 64, z, rotY: yaw });
    kit.cone(7.5, 9, '#b9ab8f', { x, y: y + 72, z, rotY: yaw }, 4);
    kit.glowSphere(1.4, LAMP, { x, y: y + 74.5, z });
    // Piers behind the building.
    for (const d of [-70, 70]) {
      const [px, pz] = along(d);
      kit.box(22, 2, 90, '#8e8477', { x: px + cos * 60, y: 2.4, z: pz - sin * 60, rotY: yaw });
    }
    return kit.finish('ferryBuilding');
  },

  // 1915 rotunda, colonnades and lagoon.
  palaceOfFineArts(ctx) {
    const kit = new Kit(170);
    const { x, z, y } = ctx;
    // Lagoon.
    kit.box(150, 0.6, 90, '#26404a', { x, y: y + 0.3, z: z + 60 });
    // Rotunda: octagonal base, colonnade, coffered dome.
    kit.cylinder(22, 24, 12, '#d3c4aa', { x, y: y + 6, z }, 8);
    for (let i = 0; i < 16; i++) {
      const a = (i / 16) * Math.PI * 2;
      kit.cylinder(1.5, 1.7, 24, '#dccdb3', { x: x + Math.cos(a) * 19, y: y + 24, z: z + Math.sin(a) * 19 }, 8);
    }
    kit.cylinder(20, 21, 6, '#cdbea4', { x, y: y + 39, z }, 16);
    kit.dome(19, 22, '#c6a87e', { x, y: y + 42, z }, 20);
    kit.sphere(2.2, '#c6a87e', { x, y: y + 65, z });
    // Curved colonnades sweeping either side.
    for (const side of [-1, 1]) {
      for (let i = 0; i < 14; i++) {
        const a = side * (0.35 + (i / 14) * 1.25);
        const r = 70;
        const cx = x + Math.sin(a) * r;
        const cz = z + (1 - Math.cos(a)) * r * 0.6;
        kit.cylinder(1.4, 1.6, 18, '#d9caaf', { x: cx, y: y + 9, z: cz }, 8);
        kit.box(6, 3, 6, '#cbbc9f', { x: cx, y: y + 19, z: cz, rotY: -a });
      }
    }
    return kit.finish('palaceOfFineArts');
  },

  // Beaux-Arts block under a 93 m gilded dome.
  cityHall(ctx) {
    const kit = new Kit(180);
    const { x, z, y } = ctx;
    const yaw = bearing(90);
    kit.box(122, 28, 82, '#e7e0cf', { x, y: y + 14, z, rotY: yaw });
    kit.box(126, 3, 86, '#d6cfbc', { x, y: y + 29, z, rotY: yaw });
    // Colonnaded entrance.
    for (let i = -5; i <= 5; i++) {
      kit.cylinder(1.7, 1.9, 22, '#efe8d7', { x: x - 42, y: y + 11, z: z + i * 6.4, rotY: yaw }, 10);
    }
    // Drum + dome + lantern.
    kit.box(46, 12, 46, '#e4ddcc', { x, y: y + 36, z, rotY: yaw });
    kit.cylinder(17, 19, 22, '#e9e2d1', { x, y: y + 53, z }, 20);
    for (let i = 0; i < 20; i++) {
      const a = (i / 20) * Math.PI * 2;
      kit.cylinder(1.2, 1.3, 20, '#f2ebda', { x: x + Math.cos(a) * 18, y: y + 53, z: z + Math.sin(a) * 18 }, 6);
    }
    kit.dome(17, 24, '#b9a05c', { x, y: y + 64, z }, 24);
    kit.cylinder(4, 5, 8, '#c8ae66', { x, y: y + 90, z }, 12);
    kit.sphere(2, '#d8bd74', { x, y: y + 95, z });
    kit.glowSphere(1.6, LAMP, { x, y: y + 97, z });
    return kit.finish('cityHall');
  },

  // Ballpark: asymmetric bowl, the brick facade, light towers and the field.
  oraclePark(ctx) {
    const kit = new Kit(60);
    const { x, z, y } = ctx;
    const yaw = bearing(45);
    // Field.
    kit.box(150, 0.5, 150, '#3f6b33', { x, y: y + 0.25, z, rotY: yaw });
    kit.box(28, 0.6, 28, '#8a6a4a', { x: x - 20, y: y + 0.35, z: z + 20, rotY: yaw + 45 * DEG });
    // Bowl: concentric rings of raked seating, open toward the Bay in the east.
    const tiers = [
      { r: 96, h: 12, color: '#8f8577' },
      { r: 112, h: 22, color: '#7d7469' },
      { r: 126, h: 32, color: '#6f675d' },
    ];
    for (const tier of tiers) {
      for (let i = 0; i < 40; i++) {
        const a = (i / 40) * Math.PI * 2;
        // Leave the right-field corner low, like the real waterfront gap.
        const open = Math.cos(a - 0.6) > 0.72;
        const h = open ? tier.h * 0.35 : tier.h;
        kit.box(22, h, 12, tier.color, {
          x: x + Math.cos(a) * tier.r,
          y: y + h / 2,
          z: z + Math.sin(a) * tier.r,
          rotY: -a,
        });
      }
    }
    // Brick outer facade.
    for (let i = 0; i < 44; i++) {
      const a = (i / 44) * Math.PI * 2;
      kit.box(20, 26, 4, '#8c5a44', {
        x: x + Math.cos(a) * 134,
        y: y + 13,
        z: z + Math.sin(a) * 134,
        rotY: -a,
      });
    }
    // Light towers.
    for (let i = 0; i < 6; i++) {
      const a = (i / 6) * Math.PI * 2 + 0.4;
      const lx = x + Math.cos(a) * 128;
      const lz = z + Math.sin(a) * 128;
      kit.box(4, 46, 4, STEEL, { x: lx, y: y + 23, z: lz });
      kit.box(24, 5, 3, '#d8d3c8', { x: lx, y: y + 47, z: lz, rotY: -a });
      for (let l = -2; l <= 2; l++) {
        kit.glowSphere(1.7, '#eef4ff', { x: lx + Math.cos(-a) * l * 5, y: y + 48, z: lz + Math.sin(-a) * l * 5 });
      }
    }
    return kit.finish('oraclePark');
  },

  // The island: rock, cellhouse, lighthouse and its sweeping beacon.
  alcatraz(ctx) {
    const kit = new Kit(100);
    const { x, z } = ctx;
    // Rock: two stacked lathes so the island reads as a bluff, not a cone.
    kit.cylinder(84, 128, 14, '#7d7466', { x, y: 7, z }, 16);
    kit.cylinder(56, 84, 16, '#8a8171', { x, y: 21, z }, 14);
    kit.cylinder(40, 56, 8, '#6f7a5f', { x, y: 32, z }, 12);
    const yaw = bearing(300);
    // Cellhouse.
    kit.box(34, 17, 118, '#cfc7b4', { x, y: 44, z, rotY: yaw });
    kit.box(37, 2.5, 121, '#8f5f4a', { x, y: 53.5, z, rotY: yaw });
    kit.box(20, 9, 24, '#c6bda9', { x: x + 14, y: 40, z: z + 30, rotY: yaw });
    // Lighthouse.
    const lx = x + 30 * Math.sin(yaw);
    const lz = z + 30 * Math.cos(yaw);
    kit.cylinder(3, 4.2, 26, WHITE, { x: lx, y: 47, z: lz }, 12);
    kit.cylinder(3.4, 3.4, 4, '#5a5a5a', { x: lx, y: 62, z: lz }, 12);
    kit.glowSphere(2.6, '#fff3cf', { x: lx, y: 62, z: lz });
    // Water tower.
    kit.box(2, 18, 2, STEEL, { x: x - 26, y: 45, z: z - 44 });
    kit.cylinder(6, 6, 9, '#b9b3a6', { x: x - 26, y: 58, z: z - 44 }, 10);
    return kit.finish('alcatraz');
  },

  // The Steiner Street row: seven Victorians with gables and bays.
  paintedLadies(ctx) {
    const kit = new Kit(220);
    const { x, z, y } = ctx;
    const yaw = bearing(84); // facing east across Alamo Square
    const colors = ['#e9d8b8', '#dfa9a0', '#cfd6c0', '#e6c98d', '#c8b7d2', '#e4d3a6', '#d9b39a'];
    const trim = '#f4efe4';
    for (let i = 0; i < 7; i++) {
      const off = (i - 3) * 9.2;
      const bx = x + off * Math.cos(yaw);
      const bz = z - off * Math.sin(yaw);
      const color = colors[i];
      kit.box(11.4, 13.5, 8.6, color, { x: bx, y: y + 6.75, z: bz, rotY: yaw });
      // Bay window stack.
      kit.box(4.6, 11, 3.4, color, {
        x: bx + Math.sin(yaw) * 5.4,
        y: y + 6,
        z: bz + Math.cos(yaw) * 5.4,
        rotY: yaw,
      });
      // Gable + cornice.
      kit.box(11.8, 1, 9, trim, { x: bx, y: y + 13.8, z: bz, rotY: yaw });
      kit.cone(6.6, 5.2, ROOF, { x: bx, y: y + 16.6, z: bz, rotY: yaw + Math.PI / 4 }, 4);
      // Stoop.
      kit.box(3.4, 2.4, 4, trim, {
        x: bx + Math.sin(yaw) * 7.4,
        y: y + 1.2,
        z: bz + Math.cos(yaw) * 7.4,
        rotY: yaw,
      });
      // Lit windows at dusk.
      for (let f = 0; f < 3; f++) {
        kit.glowSphere(0.7, LAMP, {
          x: bx + Math.sin(yaw) * 4.5,
          y: y + 3.5 + f * 3.6,
          z: bz + Math.cos(yaw) * 4.5,
        });
      }
    }
    return kit.finish('paintedLadies');
  },

  // Gothic cathedral on Nob Hill: nave, twin west towers, rose window.
  graceCathedral(ctx) {
    const kit = new Kit(190);
    const { x, z, y } = ctx;
    const yaw = bearing(90);
    const stone = '#cfc9ba';
    kit.box(34, 26, 88, stone, { x, y: y + 13, z, rotY: yaw });
    kit.box(58, 20, 24, stone, { x, y: y + 10, z, rotY: yaw }); // transept
    kit.box(36, 3, 90, '#a9a294', { x, y: y + 27, z, rotY: yaw });
    // Twin towers on the east facade.
    for (const side of [-1, 1]) {
      const tx = x - 40 * Math.sin(yaw) + side * 12 * Math.cos(yaw);
      const tz = z - 40 * Math.cos(yaw) - side * 12 * Math.sin(yaw);
      kit.box(13, 48, 13, stone, { x: tx, y: y + 24, z: tz, rotY: yaw });
      kit.box(14.5, 3, 14.5, '#b8b1a2', { x: tx, y: y + 49, z: tz, rotY: yaw });
      for (let i = 0; i < 4; i++) {
        const a = (i / 4) * Math.PI * 2 + Math.PI / 4;
        kit.cone(1.6, 6, stone, { x: tx + Math.cos(a) * 5.6, y: y + 53, z: tz + Math.sin(a) * 5.6 }, 4);
      }
      kit.cone(6.5, 10, '#9aa08f', { x: tx, y: y + 55, z: tz, rotY: Math.PI / 4 }, 4);
    }
    // Central spire over the crossing + rose window.
    kit.cone(9, 22, '#9aa08f', { x, y: y + 38, z, rotY: Math.PI / 4 }, 4);
    kit.torus(5.5, 0.9, '#8a94a6', { x: x - 34 * Math.sin(yaw), y: y + 19, z: z - 34 * Math.cos(yaw), rotY: yaw });
    kit.glowSphere(4.2, '#9fc3ff', { x: x - 34 * Math.sin(yaw), y: y + 19, z: z - 34 * Math.cos(yaw) });
    // Buttresses.
    for (let i = -3; i <= 3; i++) {
      for (const side of [-1, 1]) {
        kit.box(6, 18, 3, stone, {
          x: x + side * 19 * Math.cos(yaw) + i * 12 * Math.sin(yaw),
          y: y + 9,
          z: z - side * 19 * Math.sin(yaw) + i * 12 * Math.cos(yaw),
          rotY: yaw,
        });
      }
    }
    return kit.finish('graceCathedral');
  },

  // USF's twin-spired church.
  stIgnatius(ctx) {
    const kit = new Kit(175);
    const { x, z, y } = ctx;
    const yaw = bearing(100);
    const stone = '#d8d0bd';
    kit.box(30, 24, 76, stone, { x, y: y + 12, z, rotY: yaw });
    kit.box(32, 3, 78, '#b0a894', { x, y: y + 25, z, rotY: yaw });
    kit.dome(11, 14, '#b9b2a0', { x, y: y + 26, z }, 16);
    for (const side of [-1, 1]) {
      const tx = x - 34 * Math.sin(yaw) + side * 13 * Math.cos(yaw);
      const tz = z - 34 * Math.cos(yaw) - side * 13 * Math.sin(yaw);
      kit.box(11, 44, 11, stone, { x: tx, y: y + 22, z: tz, rotY: yaw });
      kit.box(9, 10, 9, '#e3dbc8', { x: tx, y: y + 48, z: tz, rotY: yaw });
      kit.cone(6.4, 20, '#a8ac98', { x: tx, y: y + 62, z: tz, rotY: Math.PI / 4 }, 4);
      kit.glowSphere(1.1, LAMP, { x: tx, y: y + 71, z: tz });
    }
    kit.box(24, 16, 5, stone, { x: x - 30 * Math.sin(yaw), y: y + 8, z: z - 30 * Math.cos(yaw), rotY: yaw });
    return kit.finish('stIgnatius');
  },

  // Pier 39 / Fisherman's Wharf: finger piers, sheds, carousel, ferry slips.
  fishermansWharf(ctx) {
    const kit = new Kit(130);
    const { x, z } = ctx;
    const yaw = bearing(0); // piers run north into the Bay
    const pier = (ox, length, width) => {
      // Deck on piles.
      kit.box(width, 1.8, length, '#8a8074', { x: x + ox, y: 4.2, z: z - length / 2, rotY: yaw });
      for (let d = 6; d < length; d += 14) {
        for (const side of [-1, 1]) {
          kit.cylinder(0.8, 0.8, 8, '#6b6157', { x: x + ox + side * (width / 2 - 2), y: 0.5, z: z - d });
        }
      }
    };
    pier(-70, 150, 34);
    pier(0, 190, 44);
    pier(74, 130, 30);
    // Pier 39 sheds with red roofs and shops.
    for (let i = 0; i < 5; i++) {
      kit.box(30, 9, 26, '#d6cdba', { x, y: 9.6, z: z - 26 - i * 32, rotY: yaw });
      kit.box(32, 1.6, 28, '#a24a3a', { x, y: 15, z: z - 26 - i * 32, rotY: yaw });
    }
    // Carousel.
    kit.cylinder(9, 9.5, 6, '#e7dcc4', { x: x + 14, y: 8, z: z - 20 }, 16);
    kit.cone(10, 5, '#b8412f', { x: x + 14, y: 13.5, z: z - 20 }, 16);
    kit.glowSphere(1.4, LAMP, { x: x + 14, y: 16.5, z: z - 20 });
    // Ferry terminal (Pier 41) + boats.
    kit.box(24, 8, 18, '#cdc4b1', { x: x - 70, y: 9, z: z - 40, rotY: yaw });
    kit.box(26, 1.4, 20, '#5d6b74', { x: x - 70, y: 13.5, z: z - 40, rotY: yaw });
    for (let i = 0; i < 8; i++) {
      const bx = x + 74 + (i % 2 ? 11 : -11);
      const bz = z - 24 - i * 12;
      kit.box(4, 2.4, 11, '#e6e1d5', { x: bx, y: 1.6, z: bz, rotY: yaw });
      kit.box(2.4, 2.6, 3.4, '#cfd6dc', { x: bx, y: 3.8, z: bz + 1.4, rotY: yaw });
      kit.strut([bx, 4, bz], [bx, 13, bz], 0.22, '#d8d3c8');
    }
    // Wharf-side lamps.
    for (let i = -4; i <= 4; i++) {
      kit.glowSphere(1.1, LAMP, { x: x + i * 22, y: 9, z: z + 6 });
    }
    return kit.finish('fishermansWharf');
  },
};

export function createLandmarks(scene, data) {
  const { manifest, sampleElevation, project } = data;
  const group = new Group();
  group.name = 'landmarks';
  const built = [];

  for (const landmark of manifest.landmarks) {
    const builder = builders[landmark.id];
    if (!builder) continue;
    // The two bridges are built from baked OSM centrelines; without them there
    // is nothing to draw.
    const bridge = manifest.bridges?.[landmark.id];
    if (!bridge && /Bridge$/.test(landmark.id)) continue;
    const [x, z] = project(landmark.lon, landmark.lat);
    const y = Math.max(0, sampleElevation(x, z));
    const object = builder({ x, y, z, project, sampleElevation, landmark, bridge });
    group.add(object);
    built.push({ landmark, object, position: new Vector3(x, y, z) });
  }
  scene.add(group);

  return {
    group,
    built,
    update() {
      for (const entry of built) updateLandmarkGlow(entry.object);
    },
  };
}
