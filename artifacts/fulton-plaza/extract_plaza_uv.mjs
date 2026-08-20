// Extract Fulton Plaza's measured geometry into the plaza's own (u, v) frame.
//
//     node extract_plaza_uv.mjs        # writes data/plaza_uv.json
//
// Every number below is a measurement with a named source, not an eyeball. The
// script's whole job is the projection + frame change, so that the build script
// never has to know about lon/lat and the provenance stays readable in a diff.
//
// Sources, in the order they appear:
//
//   ROW        DataSF parcels `acdm-wktn`. Fulton Plaza has no parcel of its
//              own — it is a street. Its polygon is therefore the gap between
//              the two block parcels that face it: the NORTH line of blklot
//              0354001 (the Main Library block) and the SOUTH line of blklot
//              0353001 (the Asian Art Museum block), closed at each end by the
//              Larkin and Hyde property lines those two share.
//   monument   The Pioneer Monument's ring as the CITY BAKE sees it —
//              app/public/tiles/buildings/19_13.bin footprint #101, a
//              17-vertex cruciform. DataSF traces the monument as a building,
//              which is both why it needs an exclusion (plan 2.13) and why we
//              have a survey-grade outline of it for free.
//   beds       OSM ways 1469745033 (west) and 1469745032 (east),
//              area=yes + highway=pedestrian + surface=dirt.
//   walks      OSM sidewalk centrelines 399142439 (south/library) and
//              696627437 (north/museum).
//   nodes      OSM: Ashurbanipal 6465902729, the 1996 "California Native
//              Americans" plaque 13481001521 (on the monument's EAST pier —
//              the empty one), street lamps 13480967445/13480967446.
//   koi        Esri World Imagery, warm-pixel centroid of each fish at
//              0.110 m/px. The least precise input in the file; see plan 2.15
//              risk 1.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const REPO = path.resolve(HERE, '../..');
const { project } = await import(`${REPO}/pipeline/lib/geo.mjs`);

const ANCHOR = [-122.4159189, 37.7796904]; // ROW oriented-bounding-box centre
const HEADING_LONG = 81.15;   // +u, toward Hyde Street (east). Signed; see plan 2.3.
const HEADING_CROSS = 171.15; // +v, toward the Main Library (south)

const [ax, az] = project(...ANCHOR);
const H = (HEADING_LONG * Math.PI) / 180;
const C = (HEADING_CROSS * Math.PI) / 180;
const U = [Math.sin(H), Math.cos(H)];
const V = [Math.sin(C), Math.cos(C)];

// world (x east, z south) -> (u, v). Inverse of the build script's to_world().
function toUV(lon, lat) {
  const [x, z] = project(lon, lat);
  return fromWorld(x, z);
}
function fromWorld(x, z) {
  const dx = x - ax;
  const dn = -(z - az); // north-positive, matching U/V which are bearings
  const u = dx * U[0] + dn * U[1];
  const v = dx * V[0] + dn * V[1];
  return [round(u), round(v)];
}
const round = (n) => Math.round(n * 1000) / 1000;

// ---------------------------------------------------------------- the ROW
const ROW_LL = [
  [-122.4165461, 37.7793902], // SW  Larkin x library block line
  [-122.4152008, 37.7795570], // SE  Hyde   x library block line
  [-122.4152951, 37.7799901], // NE  Hyde   x museum  block line
  [-122.4166336, 37.7798241], // NW  Larkin x museum  block line
];

// ------------------------------------------------- the monument, from the bake
function monumentRing() {
  const buf = fs.readFileSync(`${REPO}/app/public/tiles/buildings/19_13.bin`);
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const version = dv.getUint16(4, true);
  const count = dv.getUint32(8, true);
  const vertexTotal = dv.getUint32(12, true);
  const ox = dv.getFloat32(20, true);
  const oz = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);
  let off = 32;
  const vertOffset = new Uint32Array(buf.buffer, buf.byteOffset + off, count); off += 4 * count;
  off += 4 * count; // idxOffset
  const vertCount = new Uint16Array(buf.buffer, buf.byteOffset + off, count); off += 2 * count;
  off += 2 * count; // idxCount
  const baseY = new Int16Array(buf.buffer, buf.byteOffset + off, count); off += 2 * count;
  const topY = new Int16Array(buf.buffer, buf.byteOffset + off, count); off += 2 * count;
  off += 2 * count;                       // palette, seed
  if (version >= 2) off += 2 * count;     // flags, roofPalette
  if (version >= 3) off += 3 * count;     // cat, yaw, night
  if (off % 2) off++;
  const verts = new Int16Array(buf.buffer, buf.byteOffset + off, vertexTotal * 2);

  // The footprint whose centroid is nearest the anchor IS the monument: nothing
  // else is baked inside the right-of-way at all (plan 2.13).
  let best = null;
  for (let i = 0; i < count; i++) {
    const n = vertCount[i];
    const vo = vertOffset[i];
    let sx = 0, sz = 0;
    for (let k = 0; k < n; k++) {
      sx += verts[(vo + k) * 2] * quant + ox;
      sz += verts[(vo + k) * 2 + 1] * quant + oz;
    }
    const d = Math.hypot(sx / n - ax, sz / n - az);
    if (!best || d < best.d) best = { d, i, n, vo };
  }
  const ring = [];
  for (let k = 0; k < best.n; k++) {
    ring.push(fromWorld(verts[(best.vo + k) * 2] * quant + ox,
                        verts[(best.vo + k) * 2 + 1] * quant + oz));
  }
  return {
    ring,
    centroid_dist_from_anchor_m: round(best.d),
    baked_base_m: baseY[best.i] * 0.1,
    baked_top_m: topY[best.i] * 0.1,
    note: 'buildings/19_13.bin footprint #' + best.i + ' — DataSF traces the Pioneer Monument as a building',
  };
}

// ------------------------------------------------------------------- OSM data
const BED_W = [
  [-122.416661, 37.779838], [-122.416648, 37.779776],
  [-122.416045, 37.779851], [-122.416058, 37.779914],
];
const BED_E = [
  [-122.415927, 37.779932], [-122.415915, 37.779868],
  [-122.415333, 37.779939], [-122.415345, 37.780002],
];
const WALK_S = [
  [-122.415226, 37.779617], [-122.415689, 37.779557],
  [-122.416130, 37.779500], [-122.416623, 37.779437],
];
const WALK_N = [
  [-122.415295, 37.779945], [-122.415752, 37.779874],
  [-122.416197, 37.779819], [-122.416685, 37.779760],
];
const NODES = {
  ashurbanipal: [-122.415985, 37.779894],
  monument_plaque_east_pier: [-122.415833, 37.779714],
  lamp_a: [-122.415993, 37.779469],
  lamp_b: [-122.415809, 37.779491],
  koi_west: [-122.416292, 37.779652],
  koi_east: [-122.415622, 37.779777],
};

const out = {
  _: 'GENERATED by extract_plaza_uv.mjs — do not hand-edit',
  anchor_lonlat: ANCHOR,
  heading_long_deg: HEADING_LONG,
  heading_cross_deg: HEADING_CROSS,
  frame: '+u toward Hyde St (east, bearing 81.15), +v toward the Main Library (south, bearing 171.15)',
  ring: ROW_LL.map(([lon, lat]) => toUV(lon, lat)),
  ring_source: 'DataSF acdm-wktn: north line of blklot 0354001, south line of blklot 0353001',
  monument: monumentRing(),
  beds: { west: BED_W.map((p) => toUV(...p)), east: BED_E.map((p) => toUV(...p)) },
  beds_source: 'OSM ways 1469745033 (west) and 1469745032 (east)',
  walks: { south: WALK_S.map((p) => toUV(...p)), north: WALK_N.map((p) => toUV(...p)) },
  walks_source: 'OSM sidewalk centrelines 399142439 (south) and 696627437 (north)',
  nodes: Object.fromEntries(Object.entries(NODES).map(([k, p]) => [k, toUV(...p)])),
  nodes_source: 'OSM 6465902729, 13481001521, 13480967445, 13480967446; koi from Esri World Imagery',
};

// Derived, and asserted rather than assumed: the ROW must come out as a
// rectangle in this frame if the heading is right.
const us = out.ring.map((p) => p[0]);
const vs = out.ring.map((p) => p[1]);
out.extent_u = [Math.min(...us), Math.max(...us)];
out.extent_v = [Math.min(...vs), Math.max(...vs)];
out.length_m = round(Math.max(...us) - Math.min(...us));
out.width_m = round(Math.max(...vs) - Math.min(...vs));

fs.mkdirSync(path.join(HERE, 'data'), { recursive: true });
fs.writeFileSync(path.join(HERE, 'data', 'plaza_uv.json'), JSON.stringify(out, null, 1));

console.log(`ROW in the plaza frame  ${out.length_m} x ${out.width_m} m`);
console.log(`  corners  ${out.ring.map((p) => `(${p[0]}, ${p[1]})`).join('  ')}`);
console.log(`monument centroid ${out.monument.centroid_dist_from_anchor_m} m from the anchor,` +
            ` baked ${out.monument.baked_base_m} -> ${out.monument.baked_top_m} m,` +
            ` ${out.monument.ring.length} verts`);
for (const [k, p] of Object.entries(out.nodes)) console.log(`  ${k.padEnd(26)} u=${p[0]}  v=${p[1]}`);
console.log('wrote data/plaza_uv.json');
