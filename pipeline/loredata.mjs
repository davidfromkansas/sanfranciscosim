// Downloads the identity sources used by lore.mjs and context.mjs into
// pipeline/data/. Every source is a free bulk download: no API key, no billing,
// no display restriction. Idempotent — existing files are kept unless FORCE=1.
//
// Foursquare OS Places note: the legacy public S3 bucket described in the
// original plan is gone (Foursquare moved OS Places behind a Places Portal
// token / gated HuggingFace repo in 2025). Overture Places carries the same
// Foursquare records under the Overture GERS release, is still an anonymous
// bulk download, and is used in its place as the third identity source.

import { spawn } from 'node:child_process';
import { existsSync, statSync } from 'node:fs';
import { mkdir, rename, writeFile } from 'node:fs/promises';
import { BBOX } from './lib/geo.mjs';

const DATA = new URL('./data/', import.meta.url);
const FORCE = process.env.FORCE === '1';

const UA = 'sf-3d-pipeline/1.0 (https://github.com/davidfromkansas/sanfranciscosim)';

function localPath(name) {
  return new URL(name, DATA);
}

function cached(name) {
  const p = localPath(name);
  if (FORCE || !existsSync(p) || statSync(p).size < 1024) return false;
  console.log(`= ${name} (cached, ${(statSync(p).size / 1e6).toFixed(1)} MB)`);
  return true;
}

async function fetchRetry(url, init, attempts = 5) {
  let lastErr;
  for (let i = 0; i < attempts; i++) {
    try {
      const res = await fetch(url, { ...init, headers: { 'User-Agent': UA, ...(init?.headers || {}) } });
      if (!res.ok) throw new Error(`HTTP ${res.status} for ${url}`);
      return res;
    } catch (err) {
      lastErr = err;
      await new Promise((r) => setTimeout(r, 2000 * (i + 1)));
      console.warn(`  retry ${i + 1}/${attempts}: ${err.message}`);
    }
  }
  throw lastErr;
}

// Socrata pages at 50k rows; every dataset here is well under a million rows.
async function socrata(name, id, { select, where, order = ':id', geojson = false } = {}) {
  if (cached(name)) return;
  const rows = [];
  const limit = 50000;
  for (let offset = 0; ; offset += limit) {
    const params = new URLSearchParams({ $limit: String(limit), $offset: String(offset), $order: order });
    if (select) params.set('$select', select);
    if (where) params.set('$where', where);
    const url = `https://data.sfgov.org/resource/${id}.${geojson ? 'geojson' : 'json'}?${params}`;
    console.log(`↓ ${name} offset=${offset}`);
    const json = await (await fetchRetry(url)).json();
    const page = geojson ? json.features || [] : json;
    rows.push(...page);
    if (page.length < limit) break;
  }
  await writeFile(localPath(name), JSON.stringify(rows));
  console.log(`  ${name}: ${rows.length} rows (${(statSync(localPath(name)).size / 1e6).toFixed(1)} MB)`);
}

const BB = `${BBOX.minLat},${BBOX.minLon},${BBOX.maxLat},${BBOX.maxLon}`;

// Appendix E's pull: `out tags center` gives ways a centre point, so nodes and
// ways join through the same point-in-footprint path.
const OVERPASS_POIS = `[out:json][timeout:300][bbox:${BB}];
( node["amenity"]; way["amenity"];
  node["shop"];    way["shop"];
  node["tourism"]; way["tourism"];
  node["leisure"="fitness_centre"]; way["leisure"="fitness_centre"];
  node["railway"="station"]; way["railway"="station"];
  way["building"]["building"!~"^(yes|residential|house|apartments|garage|roof|shed|hut)$"]; );
out tags center;`;

const OVERPASS_ENDPOINTS = [
  'https://overpass-api.de/api/interpreter',
  'https://overpass.kumi.systems/api/interpreter',
];

async function overpass(name, query) {
  if (cached(name)) return;
  for (const endpoint of OVERPASS_ENDPOINTS) {
    try {
      console.log(`↓ ${name} <- ${endpoint}`);
      const res = await fetchRetry(
        endpoint,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/x-www-form-urlencoded', Accept: '*/*' },
          body: new URLSearchParams({ data: query }),
        },
        2
      );
      const text = await res.text();
      const parsed = JSON.parse(text);
      if (!parsed.elements?.length) throw new Error('empty element list');
      await writeFile(localPath(name), text);
      console.log(`  ${name}: ${parsed.elements.length} elements`);
      return;
    } catch (err) {
      console.warn(`  ${endpoint} failed: ${err.message}`);
    }
  }
  throw new Error(`could not download ${name} from any Overpass mirror`);
}

// Overture's own CLI streams the SF bbox out of the public parquet release
// without credentials. ~52k SF places in well under a minute.
function overturePlaces(name) {
  if (cached(name)) return Promise.resolve();
  const tmp = `${localPath(name).pathname}.part`;
  console.log(`↓ ${name} <- overturemaps CLI`);
  return new Promise((resolve, reject) => {
    const child = spawn(
      'overturemaps',
      [
        'download',
        `--bbox=${BBOX.minLon},${BBOX.minLat},${BBOX.maxLon},${BBOX.maxLat}`,
        '-f',
        'geojson',
        '--type=place',
        '-o',
        tmp,
      ],
      { stdio: ['ignore', 'inherit', 'inherit'] }
    );
    child.on('error', (err) =>
      reject(
        new Error(
          `overturemaps CLI unavailable (${err.message}). Install it with \`pip3 install overturemaps\`.`
        )
      )
    );
    child.on('close', async (code) => {
      if (code !== 0) return reject(new Error(`overturemaps exited ${code}`));
      await rename(tmp, localPath(name).pathname);
      console.log(`  ${name}: ${(statSync(localPath(name)).size / 1e6).toFixed(1)} MB`);
      resolve();
    });
  });
}

await mkdir(DATA, { recursive: true });

// DataSF authoritative facility datasets — the highest-priority identity source.
await socrata('datasf_facilities.json', 'nc68-ngbr', {
  where: `city='San Francisco' AND latitude IS NOT NULL`,
  order: 'facility_id',
});
await socrata('datasf_schools.json', '7e7j-59qk', {
  where: `latitude IS NOT NULL AND status='Active'`,
  order: 'cds_code',
});
// Registered Business Locations: NAICS + trade name for every active business.
await socrata('datasf_business.json', 'g8m3-pdis', {
  select:
    'dba_name,full_business_address,self_reported_naics_code,lic_code_description,location,neighborhoods_analysis_boundaries,transient_occupancy_tax',
  where: `city='San Francisco' AND location_end_date IS NULL AND location IS NOT NULL`,
  order: 'uniqueid',
});
// Land Use: per-parcel use mix, the "everything else" fallback classifier.
await socrata('datasf_landuse.json', 'c5ge-t6pj', {
  select: 'the_geom,resunits,cie,med,mips,retail,pdr,visitor,parking_lo,garage,open_space,residentia',
  order: 'ludb_id',
});
// Context-layer geometry.
await socrata('datasf_neighborhoods.json', 'j2bu-swwd', { order: 'nhood' });
await socrata('datasf_parks.json', 'gtr9-ntp6', { order: 'objectid' });

await overpass('osm_pois.json', OVERPASS_POIS);
await overturePlaces('overture_places.geojson');

console.log('lore sources ready');
