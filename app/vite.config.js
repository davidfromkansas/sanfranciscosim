import { readFileSync } from 'node:fs';
import { defineConfig } from 'vite';

// Baked tiles live under stable, unhashed names, so every tile URL carries the
// bake timestamp as a query key: a re-bake invalidates the browser cache even
// though the filenames never change. The key is the newest stamp of any tier —
// the toy tier re-bakes on its own, and a stale key would keep serving the
// previous toy tiles from cache long after they were replaced.
const stamp = (file) => {
  try {
    return JSON.parse(readFileSync(new URL(`./public/tiles/${file}`, import.meta.url), 'utf8'))
      .generated;
  } catch {
    return null;
  }
};
const tilesVersion = [stamp('manifest.json'), stamp('toy.json')]
  .filter(Boolean)
  .sort()
  .pop();

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
