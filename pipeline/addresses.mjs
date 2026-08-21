// Bake the DataSF Enterprise Addressing System into a compact, bucketed index.

import { mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { insideBBox, project } from './lib/geo.mjs';
import { lookupAddress, normalizeStreetName, parseAddressQuery } from '../api/_lib/addresses.mjs';

const DATA = new URL('./data/', import.meta.url);
const API_DATA = new URL('../api/_data/', import.meta.url);
const ADDR_DIR = new URL('../app/public/tiles/context/addr/', import.meta.url);
const source = JSON.parse(await readFile(new URL('addresses_datasf.json', DATA), 'utf8'));

const streets = {};
const seen = new Set();
let dropped = 0;
for (const row of source) {
  const number = Number.parseInt(String(row.address_number ?? '').match(/\d+/)?.[0] || '', 10);
  const lon = Number(row.longitude);
  const lat = Number(row.latitude);
  const key = normalizeStreetName(row.street_full_street_name || [row.street_name, row.street_type].filter(Boolean).join(' '));
  if (!Number.isSafeInteger(number) || !key || !Number.isFinite(lon) || !Number.isFinite(lat) || !insideBBox(lon, lat)) {
    dropped++;
    continue;
  }
  const dedupe = `${key}\0${number}`;
  if (seen.has(dedupe)) continue;
  seen.add(dedupe);
  const [x, z] = project(lon, lat);
  const street = streets[key] || (streets[key] = {
    name: key.toUpperCase(),
    n: [],
    x: [],
    z: [],
  });
  street.n.push(number);
  street.x.push(Math.round(x));
  street.z.push(Math.round(z));
}

for (const street of Object.values(streets)) {
  const rows = street.n.map((n, i) => ({ n, x: street.x[i], z: street.z[i] })).sort((a, b) => a.n - b.n);
  street.n = rows.map((row) => row.n);
  street.x = rows.map((row) => row.x);
  street.z = rows.map((row) => row.z);
}

const generated = new Date().toISOString();
const attribution = 'DataSF Enterprise Addressing System (data.sfgov.org, Socrata resource ramy-di5m)';
const index = { generated, count: seen.size, attribution, streets };

await mkdir(API_DATA, { recursive: true });
await rm(ADDR_DIR, { recursive: true, force: true });
await mkdir(ADDR_DIR, { recursive: true });
await writeFile(new URL('addresses.json', API_DATA), JSON.stringify(index));

const buckets = {};
for (const [key, street] of Object.entries(streets)) {
  // Numbered streets are the only non-letter group and are large enough to
  // exceed the browser shard budget as one file. Keep the required `0`
  // namespace while splitting it by the first street-key digit.
  const bucket = /^[a-z]/.test(key) ? key[0] : `0-${key[0] || 'x'}`;
  (buckets[bucket] ||= {})[key] = street;
}
const sizes = [];
for (const [bucket, bucketStreets] of Object.entries(buckets)) {
  const body = JSON.stringify({ generated, count: Object.values(bucketStreets).reduce((sum, street) => sum + street.n.length, 0), attribution, streets: bucketStreets });
  await writeFile(new URL(`${bucket}.json`, ADDR_DIR), body);
  sizes.push({ bucket, bytes: Buffer.byteLength(body) });
}

const failures = [];
function check(label, ok, detail) {
  console.log(`  ${ok ? 'ok  ' : 'FAIL'} ${label} — ${detail}`);
  if (!ok) failures.push(label);
}

console.log(`addresses: ${source.length} source rows, ${seen.size} indexed, ${dropped} dropped, ${Object.keys(streets).length} streets`);
console.log('\naddress validation');
const all = index;
for (const [query, lon, lat] of [
  ['1726 Anza Street', -122.466841605, 37.779217678],
  ['1 Dr Carlton B Goodlett Pl', -122.418727824, 37.779332255],
  ['601 Van Ness Ave', -122.421406327, 37.781385778],
]) {
  const parsed = parseAddressQuery(query);
  const hit = parsed && lookupAddress(all, parsed);
  const [expectedX, expectedZ] = project(lon, lat);
  const error = hit ? Math.hypot(hit.x - expectedX, hit.z - expectedZ) : Infinity;
  check(query, Boolean(hit) && error <= 25, hit ? `${hit.street} ${hit.matchedNumber}, ${error.toFixed(1)} m` : 'not found');
}
const a = lookupAddress(all, parseAddressQuery('1726 Anza St'));
const b = lookupAddress(all, parseAddressQuery('1726 ANZA ST #3'));
check('unit normalization', Boolean(a && b) && a.x === b.x && a.z === b.z, a && b ? `${a.x},${a.z}` : 'not found');
check('total count >= 200000', seen.size >= 200000, `${seen.size}`);
const largest = sizes.reduce((max, item) => Math.max(max, item.bytes), 0);
check('every shard <= 600 KB raw', largest <= 600 * 1024, `${(largest / 1024).toFixed(1)} KB`);
if (failures.length) {
  console.error(`\nADDRESS VALIDATION FAILED: ${failures.join(', ')}`);
  process.exit(1);
}
console.log('\naddress shard sizes');
for (const { bucket, bytes } of sizes.sort((a, b) => a.bucket.localeCompare(b.bucket))) {
  console.log(`  ${bucket}.json ${(bytes / 1024).toFixed(1)} KB (${bytes} bytes)`);
}
const apiBytes = Buffer.byteLength(JSON.stringify(index));
console.log(`\naddress index: ${sizes.length} shards, largest ${(largest / 1024).toFixed(1)} KB, API ${apiBytes} bytes (${(apiBytes / 1e6).toFixed(1)} MB)`);
