// Post-build step (PERF-PLAN #4): gzip every baked .bin tile in dist/ so the
// first visit ships ~3x fewer bytes. The raw .bin stays alongside as the
// fallback (iron rule 3): a missing archive or a browser without
// DecompressionStream degrades to exactly what shipped before this existed.
//
// Zero dependencies — node's own zlib. Runs as part of `npm run build`.

import { promises as fs } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { gzip, constants } from 'node:zlib';
import { promisify } from 'node:util';

const gz = promisify(gzip);
const DIST_TILES = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../dist/tiles');

async function* binFiles(dir) {
  for (const entry of await fs.readdir(dir, { withFileTypes: true })) {
    const p = path.join(dir, entry.name);
    if (entry.isDirectory()) yield* binFiles(p);
    else if (entry.name.endsWith('.bin')) yield p;
  }
}

let files = 0;
let rawBytes = 0;
let gzBytes = 0;
const started = Date.now();
const tasks = [];
for await (const file of binFiles(DIST_TILES)) {
  tasks.push(
    (async () => {
      const raw = await fs.readFile(file);
      const packed = await gz(raw, { level: constants.Z_BEST_COMPRESSION });
      await fs.writeFile(file + '.gz', packed);
      files++;
      rawBytes += raw.length;
      gzBytes += packed.length;
    })()
  );
}
await Promise.all(tasks);

const mb = (n) => (n / 1024 / 1024).toFixed(1);
console.log(
  `[compress-tiles] ${files} tiles: ${mb(rawBytes)} MB -> ${mb(gzBytes)} MB ` +
    `(${(rawBytes / gzBytes).toFixed(2)}x) in ${((Date.now() - started) / 1000).toFixed(1)}s`
);
