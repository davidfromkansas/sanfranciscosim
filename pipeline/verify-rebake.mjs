// Post-re-bake verification: prove a batch bake changed only what it should.
//
// A landmark's `exclude` radius drops procedural footprints, and the two ways
// that goes wrong are silent. Too small and the baked block stays inside the
// GLB — a landmark taller than its asset is simply invisible. Too large and it
// deletes a real neighbour that has no hand-built replacement, leaving a hole.
// Neither shows up in a diff of 600 regenerated files.
//
// So this checks two things against a reference commit (default origin/main):
//
//   1. Which cells changed their building count. Every one must be a cell that
//      holds a landmark new on this branch. A cell that moves anywhere else
//      means a radius reached further than its author measured — or that the
//      bake ran against a different `pipeline/data/` snapshot than the
//      reference, which churns tiles citywide for no semantic reason.
//   2. Per new landmark, the distance from its anchor to the nearest SURVIVING
//      footprint vertex, against its radius. Above the radius: nothing is left
//      under the asset. Below it: `excluded()` should have taken that footprint
//      and did not.
//
// Run it after `context` (the last stage), from `pipeline/`:
//
//   node verify-rebake.mjs                  # published tiles vs origin/main
//   node verify-rebake.mjs --ref HEAD~1     # against another commit
//   node verify-rebake.mjs --out            # read pipeline/out/ instead, so a
//                                           # bake can be checked before commit
//
// Exits non-zero if a cell outside the new landmarks moved, or if a landmark
// has a surviving footprint inside its radius. Reads only; writes nothing.

import { execFileSync } from 'node:child_process';
import { existsSync, readFileSync, readdirSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

import { project } from './lib/geo.mjs';
import { LANDMARKS } from './lib/landmarks.mjs';

const REPO = fileURLToPath(new URL('..', import.meta.url));
const PUBLISHED = 'app/public/tiles/buildings';

const argv = process.argv.slice(2);
const ref = argv.includes('--ref') ? argv[argv.indexOf('--ref') + 1] : 'origin/main';
const src = argv.includes('--out')
  ? fileURLToPath(new URL('out/buildings/', import.meta.url))
  : fileURLToPath(new URL(`../${PUBLISHED}/`, import.meta.url));

const git = (args, encoding = 'utf8') =>
  execFileSync('git', args, { cwd: REPO, maxBuffer: 1 << 28, encoding });

// Every tile in the reference commit, in one pass. `git show` per file is the
// obvious way to write this and costs ~600 process spawns — slow enough (minutes)
// that it discourages running the check at all. One `cat-file --batch` reads the
// same blobs in about a second.
function readTiles(rev, dir) {
  const blobs = git(['ls-tree', '-r', '-z', rev, '--', dir])
    .split('\0')
    .filter(Boolean)
    .map((row) => {
      const [meta, path] = row.split('\t');
      return { sha: meta.split(' ')[2], name: path.slice(path.lastIndexOf('/') + 1) };
    });
  if (!blobs.length) return new Map();

  const stream = execFileSync('git', ['cat-file', '--batch'], {
    cwd: REPO,
    input: blobs.map((b) => b.sha).join('\n') + '\n',
    maxBuffer: 1 << 30,
  });

  // Each record is "<sha> <type> <size>\n" followed by <size> bytes and a newline.
  const out = new Map();
  let at = 0;
  for (const blob of blobs) {
    const eol = stream.indexOf(0x0a, at);
    const size = Number(stream.toString('utf8', at, eol).split(' ')[2]);
    out.set(blob.name, stream.subarray(eol + 1, eol + 1 + size));
    at = eol + 1 + size + 1;
  }
  return out;
}

// Cell grid: 500 m cells from the world origin at -8000 m on both axes, the
// same derivation buildings.mjs uses to name its output files.
const CELL = 500;
const ORIGIN = -8000;
const cellOf = (lon, lat) => {
  const [x, z] = project(lon, lat);
  return `${Math.floor((x - ORIGIN) / CELL)}_${Math.floor((z - ORIGIN) / CELL)}`;
};

// Buildings blob header (pipeline/lib/binio.mjs, writeBuildingsBlob): magic,
// uint16 version at 4, count at 8. Reading the version instead of the count is
// the classic mistake here — it is the same for every tile, so every tile looks
// unchanged and the check silently passes.
const countOf = (buf) => buf.readUInt32LE(8);

// Full decode, needed only for the landmarks' own neighbourhoods. Ring vertices
// are int16 quantised offsets from the cell origin; the trailing arrays after
// the fixed ones are version-gated, so the vertex block only lands in the right
// place if the version is honoured.
function footprints(buf) {
  const dv = new DataView(buf.buffer, buf.byteOffset, buf.byteLength);
  const version = dv.getUint16(4, true);
  const count = dv.getUint32(8, true);
  const vertexTotal = dv.getUint32(12, true);
  const originX = dv.getFloat32(20, true);
  const originZ = dv.getFloat32(24, true);
  const quant = dv.getFloat32(28, true);

  let off = 32;
  const vertOffsetAt = off;
  off += 4 * count; // vertOffset
  off += 4 * count; // idxOffset
  const vertCountAt = off;
  off += 2 * count; // vertCount
  off += 2 * count; // idxCount
  const baseYAt = off;
  off += 2 * count; // baseY
  const topYAt = off;
  off += 2 * count; // topY
  off += 2 * count; // palette, seed
  if (version >= 2) off += 2 * count; // flags, roofPalette
  if (version >= 3) off += 3 * count; // cat, yaw, night
  off = Math.ceil(off / 2) * 2;
  const vertsAt = off;
  off += 4 * vertexTotal;

  const out = [];
  for (let i = 0; i < count; i++) {
    const vo = dv.getUint32(vertOffsetAt + 4 * i, true);
    const vc = dv.getUint16(vertCountAt + 2 * i, true);
    const ring = [];
    for (let k = 0; k < vc; k++) {
      const p = vertsAt + (vo + k) * 4;
      ring.push([
        originX + dv.getInt16(p, true) * quant,
        originZ + dv.getInt16(p + 2, true) * quant,
      ]);
    }
    out.push({ ring, height: (dv.getInt16(topYAt + 2 * i, true) - dv.getInt16(baseYAt + 2 * i, true)) / 10 });
  }
  return out;
}

// New on this branch = in the working tree's registry but not the reference's.
// Deriving it rather than taking it as an argument means the check cannot be
// run against the wrong list.
const refIds = new Set(
  [...git(['show', `${ref}:pipeline/lib/landmarks.mjs`]).matchAll(/^\s*id:\s*'([^']+)'/gm)].map(
    (m) => m[1],
  ),
);
const added = LANDMARKS.filter((l) => !refIds.has(l.id));

if (!added.length) {
  console.log(`no landmarks added since ${ref} — nothing to verify`);
  process.exit(0);
}

// Every cell the exclusion CIRCLE touches, not just the one holding the anchor.
// A landmark bigger than its distance to a cell seam legitimately rewrites both
// sides of it: Civic Center Plaza is 192 m long and straddles z = -1000, so its
// three excluded kiosks land in 19_13 and 19_14. Attributing only the anchor
// cell reported the second one as a stray and turned a correct re-bake into a
// FAIL. Anything still unattributed after this is a real stray.
const cellsWithin = (lon, lat, radius) => {
  const [x, z] = project(lon, lat);
  const r = radius ?? 0;
  const out = [];
  const c0 = Math.floor((x - r - ORIGIN) / CELL);
  const c1 = Math.floor((x + r - ORIGIN) / CELL);
  const r0 = Math.floor((z - r - ORIGIN) / CELL);
  const r1 = Math.floor((z + r - ORIGIN) / CELL);
  for (let cx = c0; cx <= c1; cx++) {
    for (let cz = r0; cz <= r1; cz++) out.push(`${cx}_${cz}`);
  }
  return out;
};

const targetCells = new Map();
for (const l of added) {
  for (const cell of cellsWithin(l.lon, l.lat, l.exclude)) {
    if (!targetCells.has(cell)) targetCells.set(cell, l.id);
  }
}
console.log(
  `new since ${ref}: ${added
    .map((l) => `${l.id} @ ${cellsWithin(l.lon, l.lat, l.exclude).join('+')}`)
    .join(', ')}\n`
);

// ---------------------------------------------------------------- counts
const reference = readTiles(ref, PUBLISHED);
let identical = 0;
const moved = [];
for (const file of readdirSync(src).filter((f) => f.endsWith('.bin'))) {
  const key = file.replace('.bin', '');
  const mine = countOf(readFileSync(src + file));
  const was = reference.get(file);
  if (!was) moved.push({ key, before: null, after: mine });
  else if (countOf(was) === mine) identical++;
  else moved.push({ key, before: countOf(was), after: mine });
}

const strays = moved.filter((m) => !targetCells.has(m.key));
console.log(`per-cell building counts vs ${ref}`);
console.log(`  ${identical} of ${identical + moved.length} cells unchanged`);
for (const m of moved) {
  const who = targetCells.get(m.key);
  const from = m.before === null ? 'new cell' : m.before;
  console.log(`  ${m.key.padEnd(7)} ${String(from).padStart(4)} -> ${String(m.after).padEnd(4)} ${who ? `<- ${who}` : '*** not a new landmark cell ***'}`);
}
// A landmark whose cell count is unchanged is not necessarily wrong — the
// footprint may be absent from the source data, as the Veterans Building is —
// but it does mean the exclusion is doing nothing today, which is worth saying
// out loud rather than reading a silent PASS as proof it worked.
for (const [cell, id] of targetCells) {
  if (!moved.some((m) => m.key === cell)) {
    console.log(`  ${cell.padEnd(7)} unchanged  <- ${id}: exclusion dropped nothing (no footprint in the source data?)`);
  }
}

// ------------------------------------------------- clearance per landmark
// Footprints near a cell boundary belong to a neighbouring tile, so the search
// covers the 3x3 block around each landmark rather than its own cell.
console.log(`\nnearest surviving footprint vs exclusion radius`);
const tooClose = [];
for (const l of added) {
  const [ax, az] = project(l.lon, l.lat);
  const [col, row] = cellOf(l.lon, l.lat).split('_').map(Number);
  let best = Infinity;
  let nearest = null;
  for (let dc = -1; dc <= 1; dc++) {
    for (let dr = -1; dr <= 1; dr++) {
      const path = `${src}${col + dc}_${row + dr}.bin`;
      if (!existsSync(path)) continue;
      for (const b of footprints(readFileSync(path))) {
        for (const [x, z] of b.ring) {
          const d = Math.hypot(x - ax, z - az);
          if (d < best) {
            best = d;
            nearest = b;
          }
        }
      }
    }
  }
  const ok = best > l.exclude;
  if (!ok) tooClose.push(l.id);
  console.log(
    `  ${ok ? 'ok  ' : 'FAIL'} ${l.id.padEnd(22)} ${best.toFixed(1)} m vs ${l.exclude} m radius` +
      (nearest ? `  (nearest is ${nearest.height.toFixed(1)} m tall)` : ''),
  );
}

// ------------------------------------------------------------------ verdict
console.log();
const problems = [];
if (strays.length) problems.push(`${strays.length} cell(s) changed outside the new landmarks: ${strays.map((s) => s.key).join(', ')}`);
if (tooClose.length) problems.push(`${tooClose.length} landmark(s) still have a footprint inside the exclusion zone: ${tooClose.join(', ')}`);

if (problems.length) {
  for (const p of problems) console.error(`FAIL  ${p}`);
  if (strays.length) {
    console.error(
      '\nA stray cell is usually one of two things: a radius that reaches further than\n' +
        'its author measured, or a bake run against a different pipeline/data/ snapshot\n' +
        `than ${ref} — which rewrites tiles citywide with sub-quantum vertex drift.\n` +
        'Tell them apart by removing the new entries from lib/landmarks.mjs and re-running\n' +
        'buildings.mjs: if the same cells still differ, it is the snapshot, not the radius.',
    );
  }
  if (tooClose.length) {
    console.error(
      '\nA footprint inside the zone means the baked block is still standing where the\n' +
        'GLB goes. If the bake ran after the registry entry was added, the radius is too\n' +
        'small for what the source data actually holds there — check whether the site is\n' +
        'one footprint or a whole campus before widening it, since one vertex inside the\n' +
        'circle drops the entire ring.',
    );
  }
  process.exit(1);
}
console.log(`PASS  only the new landmarks' cells moved, and every asset has clear ground under it`);
