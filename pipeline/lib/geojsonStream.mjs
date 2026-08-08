// Streaming reader for very large GeoJSON FeatureCollections (the DataSF
// building footprint export is ~300 MB, far past JSON.parse comfort).
// Splits the top-level "features" array into individual objects by brace
// counting, then JSON.parses one feature at a time.

import { createReadStream } from 'node:fs';

export async function* streamFeatures(path) {
  const stream = createReadStream(path, { encoding: 'utf8', highWaterMark: 1 << 20 });
  let buf = '';
  let started = false;
  let depth = 0;
  let start = -1;
  let pos = 0; // scan cursor into buf; never rescans, so string state stays valid
  let inString = false;
  let escaped = false;

  for await (const chunk of stream) {
    buf += chunk;
    if (!started) {
      const idx = buf.indexOf('"features"');
      if (idx === -1) {
        if (buf.length > 1 << 22) buf = buf.slice(-1024);
        continue;
      }
      const bracket = buf.indexOf('[', idx);
      if (bracket === -1) continue;
      buf = buf.slice(bracket + 1);
      started = true;
      pos = 0;
    }

    let consumed = 0;
    for (; pos < buf.length; pos++) {
      const c = buf[pos];
      if (inString) {
        if (escaped) escaped = false;
        else if (c === '\\') escaped = true;
        else if (c === '"') inString = false;
        continue;
      }
      if (c === '"') {
        inString = true;
      } else if (c === '{') {
        if (depth === 0) start = pos;
        depth++;
      } else if (c === '}') {
        depth--;
        if (depth === 0 && start >= 0) {
          yield JSON.parse(buf.slice(start, pos + 1));
          consumed = pos + 1;
          start = -1;
        }
      }
    }
    if (consumed > 0) {
      buf = buf.slice(consumed);
      pos -= consumed;
      if (start > 0) start -= consumed;
    }
  }
}

// Yield each outer ring (flat lon/lat array) of a Polygon/MultiPolygon geometry.
export function* outerRings(geometry) {
  if (!geometry) return;
  if (geometry.type === 'Polygon') {
    if (geometry.coordinates[0]) yield geometry.coordinates[0];
  } else if (geometry.type === 'MultiPolygon') {
    for (const poly of geometry.coordinates) {
      if (poly[0]) yield poly[0];
    }
  }
}

export function* polygonsOf(geometry) {
  if (!geometry) return;
  if (geometry.type === 'Polygon') yield geometry.coordinates;
  else if (geometry.type === 'MultiPolygon') for (const p of geometry.coordinates) yield p;
}

export function* linesOf(geometry) {
  if (!geometry) return;
  if (geometry.type === 'LineString') yield geometry.coordinates;
  else if (geometry.type === 'MultiLineString') for (const l of geometry.coordinates) yield l;
}
