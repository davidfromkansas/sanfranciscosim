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

// Dev-only: serve the live feeds the way the deployed dispatcher does.
// `vite dev` serves static files only, so without this every /api/<feed> call
// 404s locally and the city always runs on its procedural fallbacks — which
// makes any live feature impossible to see before deploying. Mirrors
// api/[...path].mjs; `apply: 'serve'` keeps it out of the production build.
// Specifiers are built at runtime from a file URL so the config bundler cannot
// follow them: importing the feed index statically would drag every feed's
// server-side dependency into app/, which does not have them (muni needs
// gtfs-realtime-bindings). Each feed is imported on its own and a failure only
// costs that one feed — locally, a missing dependency should disable a feed,
// not the dev server.
let feedsPromise = null;
function loadFeeds(server) {
  if (feedsPromise) return feedsPromise;
  feedsPromise = (async () => {
    const dir = new URL('../api/_lib/', import.meta.url).href;
    const core = await import(/* @vite-ignore */ `${dir}feedcore.mjs`);
    // Read the directory rather than keeping a list: a hardcoded one silently
    // omitted a newly added feed, which then 404'd locally while working fine
    // in production.
    const { readdirSync } = await import('node:fs');
    const dirPath = new URL('../api/_lib/feeds/', import.meta.url);
    const names = readdirSync(dirPath)
      .filter((f) => f.endsWith('.mjs') && f !== 'index.mjs')
      .sort();
    for (const name of names) {
      try {
        await import(/* @vite-ignore */ `${dir}feeds/${name}`);
      } catch (error) {
        server.config.logger.warn(`[live-feeds] ${name} unavailable locally: ${error?.message || error}`);
      }
    }
    return core;
  })().catch((error) => {
    server.config.logger.warn(`[live-feeds] disabled: ${error?.message || error}`);
    return null;
  });
  return feedsPromise;
}

// Dev-only: put the repo-root .env into process.env so keyed feeds actually
// run locally. Vite loads .env for the CLIENT bundle; the feed fetchers are
// server-side Node in this same process and read process.env, so without this
// every keyed feed (ferries, Muni, the residents' writer) is permanently
// offline in dev and you cannot see a live feature until it is deployed.
// Existing variables win, so an env var on the command line still overrides
// the file. .env* is gitignored — nothing here reaches the browser or a commit.
function loadDotEnv() {
  const file = new URL('../.env', import.meta.url);
  let text;
  try {
    text = readFileSync(file, 'utf8');
  } catch {
    return [];
  }
  const loaded = [];
  for (const line of text.split('\n')) {
    const match = line.match(/^\s*(?:export\s+)?([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(.*)$/);
    if (!match || line.trimStart().startsWith('#')) continue;
    const [, name, raw] = match;
    if (process.env[name] !== undefined) continue;
    process.env[name] = raw.trim().replace(/^["']|["']$/g, '');
    loaded.push(name);
  }
  return loaded;
}

function liveFeeds() {
  return {
    name: 'sf-live-feeds',
    apply: 'serve',
    configureServer(server) {
      const loaded = loadDotEnv();
      console.log(
        loaded.length
          ? `sf-live-feeds: loaded ${loaded.join(', ')} from .env`
          : 'sf-live-feeds: no .env at the repo root — keyed feeds will report themselves offline'
      );
      server.middlewares.use(async (req, res, next) => {
        const pathname = new URL(req.url, 'http://localhost').pathname.replace(/\/+$/, '');
        if (!pathname.startsWith('/api/')) return next();
        try {
          const core = await loadFeeds(server);
          if (!core) return next();
          // The registry writes through an Express-style res; adapt node's.
          const shim = {
            setHeader: (k, v) => res.setHeader(k, v),
            status(code) {
              res.statusCode = code;
              return this;
            },
            json(body) {
              res.setHeader('content-type', 'application/json');
              res.end(JSON.stringify(body));
            },
          };
          if (pathname === '/api/live') return void (await core.serveLive(shim));
          const entry = core.getFeed(pathname.replace(/^\/api\//, ''));
          if (!entry) return next();
          await core.serveFeed(shim, entry);
        } catch (error) {
          server.config.logger.warn(`[live-feeds] ${pathname}: ${error?.message || error}`);
          next();
        }
      });
    },
  };
}

export default defineConfig({
  base: '/',
  plugins: [liveFeeds()],
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
