// Downloads every raw source into pipeline/data/. Idempotent: existing files
// are kept unless FORCE=1.
//
// This script plus `loredata.mjs` must together produce EVERY file the bake
// reads. That invariant was broken once and cost a landmark integration a full
// session: `overture_buildings.geojsonseq` was fetched by hand in some early
// session and then simply inherited from worktree to worktree, so nobody
// noticed it was missing from here. On a clean checkout the bake then ran to
// completion and silently produced a WORSE city — `overtureAdded: 0`, tallest
// procedural building 175.4 m instead of 244.4 m, the whole post-2015 SoMa
// skyline flattened — and `validate.mjs` caught it only because it happens to
// assert a height range. If you add a source, add its download here.

import { spawn } from 'node:child_process';
import { createWriteStream, existsSync, statSync } from 'node:fs';
import { mkdir, rename, writeFile } from 'node:fs/promises';
import { Readable } from 'node:stream';
import { pipeline } from 'node:stream/promises';
import { BBOX } from './lib/geo.mjs';

const DATA = new URL('./data/', import.meta.url);
const FORCE = process.env.FORCE === '1';

async function ensureDir() {
  await mkdir(DATA, { recursive: true });
}

function localPath(name) {
  return new URL(name, DATA);
}

function exists(name) {
  const p = localPath(name);
  return !FORCE && existsSync(p) && statSync(p).size > 1024;
}

async function fetchRetry(url, init, attempts = 5) {
  let lastErr;
  for (let i = 0; i < attempts; i++) {
    try {
      const res = await fetch(url, init);
      if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
      return res;
    } catch (err) {
      lastErr = err;
      const wait = 2000 * (i + 1);
      console.warn(`  retry ${i + 1}/${attempts} after ${err.message} (waiting ${wait}ms)`);
      await new Promise((r) => setTimeout(r, wait));
    }
  }
  throw lastErr;
}

async function downloadTo(name, url, init) {
  if (exists(name)) {
    console.log(`= ${name} (cached, ${(statSync(localPath(name)).size / 1e6).toFixed(1)} MB)`);
    return;
  }
  console.log(`↓ ${name} <- ${url}`);
  const res = await fetchRetry(url, init);
  await pipeline(Readable.fromWeb(res.body), createWriteStream(localPath(name)));
  console.log(`  done (${(statSync(localPath(name)).size / 1e6).toFixed(1)} MB)`);
}

// DataSF building footprints: ~177k LiDAR/Pictometry-derived footprints with
// ground elevation + roof height fields.
async function buildings() {
  await downloadTo(
    'buildings_datasf.geojson',
    'https://data.sfgov.org/api/geospatial/ynuv-fyni?method=export&format=GeoJSON'
  );
}

// Overture Maps buildings: the gap-fill source `buildings.mjs` uses for current
// heights, because the 2010 DataSF refresh predates the post-2015 skyline.
// Overture publishes GeoParquet only, so this shells out to Overture's own CLI
// rather than adding a parquet reader to the repo — the same pattern
// `loredata.mjs` already uses for Overture Places. Not a repo dependency: a
// one-time local tool, and a missing CLI fails loudly with the install command.
function overtureBuildings(name) {
  if (exists(name)) {
    console.log(`= ${name} (cached, ${(statSync(localPath(name)).size / 1e6).toFixed(1)} MB)`);
    return Promise.resolve();
  }
  const tmp = `${localPath(name).pathname}.part`;
  console.log(`↓ ${name} <- overturemaps CLI`);
  return new Promise((resolve, reject) => {
    const child = spawn(
      'overturemaps',
      [
        'download',
        `--bbox=${BBOX.minLon},${BBOX.minLat},${BBOX.maxLon},${BBOX.maxLat}`,
        '-f',
        'geojsonseq',
        '--type=building',
        '-o',
        tmp,
      ],
      { stdio: ['ignore', 'inherit', 'inherit'] }
    );
    child.on('error', (err) =>
      reject(
        new Error(
          `overturemaps CLI unavailable (${err.message}). Install it with ` +
            '`pip3 install overturemaps`. Without it buildings.mjs silently ' +
            'skips the height gap-fill and the downtown skyline bakes flat.'
        )
      )
    );
    child.on('close', async (code) => {
      if (code !== 0) return reject(new Error(`overturemaps exited ${code}`));
      await rename(tmp, localPath(name).pathname);
      console.log(`  done (${(statSync(localPath(name)).size / 1e6).toFixed(1)} MB)`);
      resolve();
    });
  });
}

// DataSF street centerlines, paged through the Socrata API.
async function streets() {
  if (exists('streets_datasf.geojson')) {
    console.log('= streets_datasf.geojson (cached)');
    return;
  }
  const features = [];
  const limit = 20000;
  for (let offset = 0; ; offset += limit) {
    const url = `https://data.sfgov.org/resource/3psu-pn9h.geojson?$limit=${limit}&$offset=${offset}`;
    console.log(`↓ streets page offset=${offset}`);
    const res = await fetchRetry(url);
    const json = await res.json();
    const page = json.features || [];
    features.push(...page);
    if (page.length < limit) break;
  }
  console.log(`  ${features.length} street features`);
  await writeFile(
    localPath('streets_datasf.geojson'),
    JSON.stringify({ type: 'FeatureCollection', features })
  );
}

// DataSF Enterprise Addressing System, base addresses only. Stable ordering is
// required because Socrata pages are assembled into one cached JSON file.
async function addresses() {
  if (exists('addresses_datasf.json')) {
    console.log('= addresses_datasf.json (cached)');
    return;
  }
  const pages = [];
  const limit = 50000;
  const select = [
    'address_number',
    'street_name',
    'street_type',
    'street_full_street_name',
    'unit_number',
    'longitude',
    'latitude',
    'nhood',
  ].join(',');
  for (let offset = 0; ; offset += limit) {
    const params = new URLSearchParams({
      '$limit': String(limit),
      '$offset': String(offset),
      '$order': 'eas_baseid',
      '$select': select,
      '$where': 'unit_number IS NULL AND latitude IS NOT NULL',
    });
    const url = `https://data.sfgov.org/resource/ramy-di5m.json?${params}`;
    console.log(`↓ addresses page offset=${offset}`);
    const res = await fetchRetry(url);
    const page = await res.json();
    pages.push(...page);
    if (page.length < limit) break;
  }
  console.log(`  ${pages.length} base address rows`);
  await writeFile(localPath('addresses_datasf.json'), JSON.stringify(pages));
}

const OVERPASS_ENDPOINTS = [
  'https://overpass-api.de/api/interpreter',
  'https://overpass.kumi.systems/api/interpreter',
];

// Overpass mirrors reject requests without a conventional User-Agent (HTTP 406).
const UA = 'sf-3d-pipeline/1.0 (https://github.com/davidfromkansas/sf-3d)';

const BB = `${BBOX.minLat},${BBOX.minLon},${BBOX.maxLat},${BBOX.maxLon}`;

const OVERPASS_QUERIES = {
  'osm_landcover.json': `[out:json][timeout:600];
(
  way["leisure"~"^(park|garden|pitch|golf_course|nature_reserve|recreation_ground)$"](${BB});
  relation["leisure"~"^(park|garden|golf_course|nature_reserve)$"](${BB});
  way["landuse"~"^(grass|forest|cemetery|recreation_ground|meadow|village_green)$"](${BB});
  relation["landuse"~"^(grass|forest|cemetery|recreation_ground)$"](${BB});
  way["natural"~"^(beach|sand|wood|scrub|water|grassland|wetland|bare_rock|cliff)$"](${BB});
  relation["natural"~"^(wood|water|beach)$"](${BB});
  relation["natural"="wetland"](${BB});
);
out geom;`,
  'osm_features.json': `[out:json][timeout:600];
(
  way["man_made"="pier"](${BB});
  way["historic"](${BB});
  node["historic"](${BB});
  node["tourism"="attraction"](${BB});
  way["tourism"="attraction"](${BB});
  way["aeroway"~"^(runway|taxiway|apron)$"](${BB});
);
out geom;`,
  // Highway structures: the bridge/layer tags are the only public source that
  // says which freeway sections ride a viaduct, and the two bespoke bridges are
  // built from these centrelines instead of hand-picked coordinates.
  'osm_structures.json': `[out:json][timeout:600];
(
  way["highway"]["name"="Golden Gate Bridge"](${BB});
  way["highway"~"^(motorway|trunk)$"]["bridge"]["ref"~"I 80"](${BB});
  way["highway"~"^(motorway|motorway_link|trunk|trunk_link)$"]["bridge"](${BB});
  way["man_made"="tower"]["bridge:support"](${BB});
  way["man_made"="tower"]["tower:type"="bridge"](${BB});
);
out geom;`,
};

async function overpass() {
  for (const [name, query] of Object.entries(OVERPASS_QUERIES)) {
    if (exists(name)) {
      console.log(`= ${name} (cached)`);
      continue;
    }
    let saved = false;
    for (const endpoint of OVERPASS_ENDPOINTS) {
      try {
        console.log(`↓ ${name} <- ${endpoint}`);
        const res = await fetchRetry(
          endpoint,
          {
            method: 'POST',
            headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
              'User-Agent': UA,
              Accept: '*/*',
            },
            body: new URLSearchParams({ data: query }),
          },
          2
        );
        const text = await res.text();
        const parsed = JSON.parse(text); // fail fast on HTML error pages
        if (!parsed.elements || parsed.elements.length === 0) {
          throw new Error('empty element list from mirror');
        }
        await writeFile(localPath(name), text);
        console.log(`  done (${(text.length / 1e6).toFixed(1)} MB)`);
        saved = true;
        break;
      } catch (err) {
        console.warn(`  ${endpoint} failed: ${err.message}`);
      }
    }
    if (!saved) throw new Error(`could not download ${name} from any Overpass mirror`);
  }
}

await ensureDir();
await buildings();
await overtureBuildings('overture_buildings.geojsonseq');
await streets();
await addresses();
await overpass();
console.log('all raw data present');
console.log('next: `npm run loredata` for the identity sources lore.mjs needs');
