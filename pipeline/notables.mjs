// Deterministic selection of the 5,000 buildings worth a written identity.
// Everything here is derived from the lore join and the footprints, so the same
// inputs always produce the same list in the same order.

import { readFile, writeFile } from 'node:fs/promises';
import { project } from './lib/geo.mjs';
import { LANDMARKS } from './lib/landmarks.mjs';
import { ringArea, ringCentroid } from './lib/poly.mjs';
import { CAT_INDEX, CATS, LABELS } from './taxonomy.mjs';

const OUT = new URL('./out/', import.meta.url);
const TOTAL = 5000;
const TIER_A = 300;
const LANDMARK_RADIUS = 100;

const fp = JSON.parse(await readFile(new URL('footprints.json', OUT), 'utf8'));
const lore = JSON.parse(await readFile(new URL('lore.json', OUT), 'utf8'));

const anchors = LANDMARKS.map((l) => {
  const [x, z] = project(l.lon, l.lat);
  return { x, z, id: l.id, name: l.name };
});

const CIVIC = new Set(
  [
    'worship',
    'school',
    'university',
    'hospital',
    'fire_station',
    'police',
    'library',
    'museum',
    'theater_cinema',
    'government',
    'transit_station',
  ].map((c) => CAT_INDEX.get(c))
);

const rows = [];
for (let id = 0; id < fp.buildings.length; id++) {
  const rec = lore[id];
  if (!rec) continue;
  const ring = fp.buildings[id][0];
  const [x, z] = ringCentroid(ring);
  const height = fp.buildings[id][1];
  const area = Math.abs(ringArea(ring));
  let landmark = null;
  let landmarkDistance = Infinity;
  for (const a of anchors) {
    const d = Math.hypot(a.x - x, a.z - z);
    if (d <= LANDMARK_RADIUS && d < landmarkDistance) {
      landmark = a;
      landmarkDistance = d;
    }
  }
  const named = Boolean(rec.name) && (rec.source === 'datasf' || rec.source === 'osm' || rec.source === 'manual');
  const tagged = Boolean(rec.tourism || rec.historic || rec.wikidata);
  const civic = CIVIC.has(rec.cat) && Boolean(rec.name);
  const tallLandUse = rec.source === 'landuse' && rec.floors > 10;
  const forced = named || tagged || civic || tallLandUse || Boolean(landmark);
  rows.push({
    id,
    rec,
    x,
    z,
    height,
    area,
    landmark,
    landmarkDistance,
    named,
    tagged,
    civic,
    forced,
    score: height * Math.sqrt(area),
  });
}

const forced = rows.filter((r) => r.forced);
// Deterministic order: strongest evidence first, then physical prominence, then
// the stable building id so ties never reorder between runs.
const evidence = (r) => (r.landmark ? 4 : 0) + (r.tagged ? 3 : 0) + (r.named ? 2 : 0) + (r.civic ? 1 : 0);
forced.sort((a, b) => evidence(b) - evidence(a) || b.score - a.score || a.id - b.id);

const rest = rows.filter((r) => !r.forced).sort((a, b) => b.score - a.score || a.id - b.id);

const picked = forced.slice(0, TOTAL);
for (const r of rest) {
  if (picked.length >= TOTAL) break;
  picked.push(r);
}

// Tier A is the top slice of the same deterministic ordering: landmarks, the
// wikidata/historic/tourism set and the biggest civic names.
const ordered = [...picked].sort((a, b) => evidence(b) - evidence(a) || b.score - a.score || a.id - b.id);
const tierA = new Set(ordered.slice(0, TIER_A).map((r) => r.id));

// A landmark's name belongs to one footprint, not to every building inside its
// 100 m radius: the closest footprint takes the name and its neighbours stay
// unnamed rather than becoming five more "Coit Tower"s.
const landmarkOwner = new Map();
for (const r of picked) {
  if (!r.landmark) continue;
  const held = landmarkOwner.get(r.landmark.id);
  if (!held || r.landmarkDistance < held.landmarkDistance) landmarkOwner.set(r.landmark.id, r);
}

const notables = picked
  .map((r) => {
    const ownsLandmark = r.landmark && landmarkOwner.get(r.landmark.id) === r;
    // With no recorded name the entry keeps a descriptive label — what the data
    // does say — and is flagged so nothing presents it as this building's name.
    const name = r.rec.name || (ownsLandmark ? r.landmark.name : null);
    const entry = {
      id: r.id,
      name: name || `Unnamed ${(LABELS[r.rec.sub] || CATS[r.rec.cat]).toLowerCase()}`,
      cat: r.rec.cat,
      tier: tierA.has(r.id) ? 'A' : 'B',
    };
    if (!name) entry.needs_review = true;
    if (r.rec.sub) entry.sub = r.rec.sub;
    if (r.rec.wikidata) entry.wikidata = r.rec.wikidata;
    if (ownsLandmark) entry.landmark = r.landmark.id;
    entry.srcUrl = r.rec.wikidata
      ? `https://www.wikidata.org/wiki/${r.rec.wikidata}`
      : r.rec.source === 'osm'
        ? 'https://www.openstreetmap.org/copyright'
        : r.rec.source === 'datasf'
          ? 'https://data.sfgov.org/City-Infrastructure/City-Facilities/nc68-ngbr'
          : 'https://docs.overturemaps.org/guides/places/';
    return entry;
  })
  .sort((a, b) => a.id - b.id);

await writeFile(new URL('notables.json', OUT), JSON.stringify(notables));

const tierACount = notables.filter((n) => n.tier === 'A').length;
const byCat = new Map();
for (const n of notables) byCat.set(n.cat, (byCat.get(n.cat) || 0) + 1);
console.log(`notables: ${notables.length} (Tier A ${tierACount}, Tier B ${notables.length - tierACount})`);
console.log(`forced-include pool: ${forced.length}; needs_review: ${notables.filter((n) => n.needs_review).length}`);
console.log(
  [...byCat.entries()]
    .sort((a, b) => b[1] - a[1])
    .slice(0, 12)
    .map(([c, n]) => `${CATS[c]}:${n}`)
    .join('  ')
);
if (notables.length !== TOTAL) {
  console.error(`expected exactly ${TOTAL} notables`);
  process.exitCode = 1;
}
