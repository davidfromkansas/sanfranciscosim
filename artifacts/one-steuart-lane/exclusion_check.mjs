// Prove the One Steuart Lane exclusion in the BAKED tile, before vs after.
// Decodes app/public/tiles/buildings/24_11.bin with the pipeline's own reader
// (SFB1 blob, not the raw float format) and reports, for every ring in the
// cell, how far it reaches into the r = 20 m exclusion circle.
//
//   node artifacts/one-steuart-lane/exclusion_check.mjs <tile.bin> [<tile2.bin> ...]
import { readBuildingsBlob } from '../../pipeline/lib/blobread.mjs';

const LON0 = -122.4375, LAT0 = 37.77;
const K = 111320 * Math.cos(LAT0 * Math.PI / 180);
const project = (lon, lat) => [(lon - LON0) * K, -(lat - LAT0) * 110540];
const [AX, AZ] = project(-122.3916888, 37.7915643);
const R = 20;

for (const file of process.argv.slice(2)) {
  const { buildings } = await readBuildingsBlob(file);
  let intruders = 0, deepest = 0, tallestIn = -Infinity, nearest = Infinity;
  for (const b of buildings) {
    let near = Infinity, cx = 0, cz = 0, n = b.ring.length / 2;
    for (let k = 0; k < n; k++) {
      const x = b.ring[k * 2], z = b.ring[k * 2 + 1];
      near = Math.min(near, Math.hypot(x - AX, z - AZ));
      cx += x; cz += z;
    }
    const centroid = Math.hypot(cx / n - AX, cz / n - AZ);
    const gate = Math.min(near, centroid);
    nearest = Math.min(nearest, gate);
    if (gate < R) {
      intruders++;
      deepest = Math.max(deepest, R - gate);
      tallestIn = Math.max(tallestIn, b.topY);
    }
  }
  console.log(`${file}`);
  console.log(`  rings in cell: ${buildings.length}`);
  console.log(`  rings intruding into the r=${R} m circle: ${intruders}` +
    (intruders ? `  (deepest ${deepest.toFixed(2)} m past the edge, tallest topY ${tallestIn.toFixed(1)} m)` : ''));
  console.log(`  nearest surviving ring, gate distance: ${nearest.toFixed(2)} m\n`);
}
