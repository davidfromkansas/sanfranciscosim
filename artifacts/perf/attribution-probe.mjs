#!/usr/bin/env node
// One-off audit probe (not part of the harness): attributes resident geometry,
// visible triangles and GPU-buffer bytes to the scene objects that own them,
// so the perf plan can be ranked by where the cost actually is.
//
//   node artifacts/perf/attribution-probe.mjs [--url http://127.0.0.1:4173]
//
// Node 22 (native WebSocket). Serves app/dist with vite preview unless --url.

import { spawn } from 'node:child_process';
import { mkdtemp, writeFile } from 'node:fs/promises';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');

const args = process.argv.slice(2);
const opt = (name, dflt) => {
  const i = args.indexOf(name);
  return i === -1 ? dflt : args[i + 1];
};
const URL_ARG = opt('--url', null);
const STATION = opt('--station', 'hero');
const SETTLE = Number(opt('--settle', 90));
const MOBILE = args.includes('--mobile');

function freePort() {
  return new Promise((resolve) => {
    const srv = net.createServer();
    srv.listen(0, '127.0.0.1', () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });
}
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function waitForHttp(url, timeout = 60000) {
  const t0 = Date.now();
  for (;;) {
    try {
      const res = await fetch(url);
      if (res.ok) return;
    } catch {}
    if (Date.now() - t0 > timeout) throw new Error(`server never came up: ${url}`);
    await sleep(250);
  }
}

class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    ws.addEventListener('message', (ev) => {
      const msg = JSON.parse(ev.data);
      const entry = this.pending.get(msg.id);
      if (!entry) return;
      this.pending.delete(msg.id);
      msg.error ? entry.reject(new Error(msg.error.message)) : entry.resolve(msg.result);
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
      this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    });
  }
}

async function main() {
  let server = null;
  let url = URL_ARG;
  if (!url) {
    const port = await freePort();
    const child = spawn('npx', ['vite', 'preview', '--port', String(port), '--strictPort'], {
      cwd: path.join(ROOT, 'app'),
      stdio: 'ignore',
    });
    server = () => child.kill('SIGTERM');
    url = `http://127.0.0.1:${port}/`;
    await waitForHttp(url);
  }

  const port = await freePort();
  const userDataDir = await mkdtemp(path.join(os.tmpdir(), 'attrib-probe-'));
  const chromeBin = process.env.CHROME_PATH || '/usr/bin/google-chrome';
  const chrome = spawn(
    chromeBin,
    [
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${userDataDir}`,
      '--headless=new',
      '--no-first-run',
      '--no-sandbox',
      '--disable-dev-shm-usage',
      '--js-flags=--expose-gc',
      '--window-size=1600,900',
      'about:blank',
    ],
    { stdio: 'ignore' }
  );

  let wsUrl = null;
  for (let i = 0; i < 200 && !wsUrl; i++) {
    try {
      const res = await fetch(`http://127.0.0.1:${port}/json/version`);
      wsUrl = (await res.json()).webSocketDebuggerUrl;
    } catch {
      await sleep(100);
    }
  }
  const ws = new WebSocket(wsUrl);
  await new Promise((r) => ws.addEventListener('open', r, { once: true }));
  const cdp = new Cdp(ws);
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const send = (m, p) => cdp.send(m, p, sessionId);
  const evaluate = async (expression, awaitPromise = false) => {
    const r = await send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result.value;
  };

  await send('Page.enable');
  await send('Runtime.enable');
  if (MOBILE) {
    await send('Emulation.setDeviceMetricsOverride', {
      width: 390, height: 844, deviceScaleFactor: 3, mobile: true,
    });
    await send('Emulation.setCPUThrottlingRate', { rate: 4 });
  }
  await send('Page.navigate', { url });

  // wait for SF, then settle
  for (let i = 0; i < 600; i++) {
    if (await evaluate('!!(window.SF && window.SF.city)')) break;
    await sleep(500);
  }
  await evaluate("SF.setClock('2026-08-01T13:00:00-07:00')");
  await evaluate("SF.boot && SF.boot.reveal && SF.boot.reveal('qa')");
  if (STATION === 'mission') await evaluate('SF.goTo(-122.418, 37.76, 200, 210, 42)');
  if (STATION === 'downtown') await evaluate('SF.goTo(-122.400, 37.789, 200, 210, 42)');

  let prev = -1;
  let stable = 0;
  for (let i = 0; i < SETTLE; i++) {
    const loaded = await evaluate('SF.city.stats.cellsLoaded');
    stable = loaded === prev ? stable + 1 : 0;
    if (stable >= 8) break;
    prev = loaded;
    await sleep(1000);
  }

  const report = await evaluate(
    `(() => {
      const bytesOf = (geo) => {
        let b = 0;
        for (const key in geo.attributes) {
          const a = geo.attributes[key];
          b += a.count * a.itemSize * (a.array?.BYTES_PER_ELEMENT || 4);
        }
        if (geo.index) b += geo.index.count * (geo.index.array?.BYTES_PER_ELEMENT || 4);
        return b;
      };
      const trisOf = (geo) => (geo.index ? geo.index.count : geo.attributes.position?.count || 0) / 3;
      const bucketOf = (o) => {
        const n = o.name || '';
        if (/^trees-/.test(n)) return 'trees (instanced)';
        if (/^lamps|lamp-pool|^pools-/.test(n)) return 'street lamps + light pools';
        if (/^far-|far/.test(n) && !/farm/.test(n)) return 'far city (2km prism meshes)';
        if (/^near-|^chunk-/.test(n)) return 'near buildings (full detail)';
        if (/^ground-|^street|^land/.test(n)) return 'ground / streets / landcover';
        if (/terrain/.test(n)) return 'terrain';
        if (/water/.test(n)) return 'water';
        if (/kit/.test(n)) return 'building kit (batched)';
        if (/furniture|streetkit/.test(n)) return 'street furniture';
        if (/car|agent|ped|bird|boat|ferry|muni|aircraft/i.test(n)) return 'moving agents';
        if (/cloud|rain|fog|sky|plinth|pier|sign/i.test(n)) return 'sky / weather / props';
        return 'other: ' + (n || o.type);
      };
      const buckets = new Map();
      const frustum = new (SF.THREE?.Frustum || Object)();
      let totalTris = 0, totalBytes = 0, meshes = 0;
      SF.scene.traverse((o) => {
        if (!o.geometry || !o.isMesh) return;
        meshes++;
        const inst = o.isInstancedMesh ? o.count : 1;
        const tris = trisOf(o.geometry) * inst;
        const bytes = bytesOf(o.geometry) + (o.isInstancedMesh ? o.count * 16 * 4 : 0);
        let visible = o.visible;
        for (let p = o.parent; p && visible; p = p.parent) visible = p.visible;
        const k = bucketOf(o);
        const b = buckets.get(k) || { objects: 0, tris: 0, visibleTris: 0, bytes: 0, instances: 0 };
        b.objects++; b.tris += tris; b.bytes += bytes; b.instances += inst;
        if (visible) b.visibleTris += tris;
        buckets.set(k, b);
        totalTris += tris; totalBytes += bytes;
      });
      const rows = [...buckets.entries()].map(([name, v]) => ({ name, ...v,
        MB: +(v.bytes / 1048576).toFixed(1) })).sort((a, b) => b.visibleTris - a.visibleTris);
      return {
        rows,
        totals: { meshes, tris: totalTris, MB: +(totalBytes / 1048576).toFixed(1) },
        renderInfo: {
          calls: SF.renderer.info.render.calls,
          triangles: SF.renderer.info.render.triangles,
          geometries: SF.renderer.info.memory.geometries,
          textures: SF.renderer.info.memory.textures,
          programs: SF.renderer.info.programs.length,
        },
        cityStats: { ...SF.city.stats },
        heapMB: performance.memory ? +(performance.memory.usedJSHeapSize / 1048576).toFixed(1) : null,
        governor: SF.governor ? { mode: SF.governor.mode, tier: SF.governor.tier } : null,
        pixelRatio: SF.renderer.getPixelRatio(),
      };
    })()`
  );

  console.log(JSON.stringify(report, null, 1));
  const out = path.join(ROOT, 'artifacts', 'perf', `attribution-${STATION}${MOBILE ? '-mobile' : ''}.json`);
  await writeFile(out, JSON.stringify(report, null, 1));
  console.log('wrote', out);

  chrome.kill('SIGTERM');
  server?.();
  process.exit(0);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
