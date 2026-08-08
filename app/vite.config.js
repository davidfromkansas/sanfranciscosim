import { readFileSync } from 'node:fs';
import { defineConfig } from 'vite';

// Baked tiles live under stable, unhashed names, so every tile URL carries the
// bake timestamp as a query key: a re-bake invalidates the browser cache even
// though the filenames never change.
const tilesVersion = JSON.parse(
  readFileSync(new URL('./public/tiles/manifest.json', import.meta.url), 'utf8')
).generated;

export default defineConfig({
  base: '/',
  define: { __TILES_VERSION__: JSON.stringify(tilesVersion) },
  build: {
    target: 'es2022',
    assetsInlineLimit: 0,
    chunkSizeWarningLimit: 1200,
  },
  server: {
    host: '0.0.0.0',
    port: 5173,
  },
});
