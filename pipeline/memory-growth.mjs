#!/usr/bin/env node
// Memory-growth probe — what a long mobile session actually retains.
//
// The health probe says whether the heap grows; this says WHICH pool grows.
// It flies a continuous loop for as long as you ask and samples, every 15 s:
//
//   heap            usedJSHeapSize against the tab's own limit
//   renderer        geometries / textures / programs (GPU-side objects three owns)
//   live classes    counts per constructor via Runtime.queryObjects, which walks
//                   the heap for reachable instances — this is what separates
//                   "the city is streaming" from "nothing is ever released"
//   subsystems      city residency, resident population, feed posts, agents
//
// GPU-independent: every number is a count or a byte total, so a software
// rasterizer only makes the run slower, not wrong. Note that a slow host also
// streams less city per minute, so growth rates here are floors.
//
//   node pipeline/memory-growth.mjs --url https://sf-3d.vercel.app --minutes 10
//
import { spawn } from 'node:child_process';
import { mkdir, mkdtemp, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT_DIR = path.join(ROOT, 'artifacts', 'perf');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const LOOP = [
  { lon: -122.4194, lat: 37.7749, distance: 3200, yaw: 200, pitch: 55 },
  { lon: -122.418, lat: 37.76, distance: 220, yaw: 210, pitch: 42 },
  { lon: -122.4098, lat: 37.7749, distance: 400, yaw: 160, pitch: 40 },
  { lon: -122.4, lat: 37.789, distance: 220, yaw: 210, pitch: 42 },
  { lon: -122.3937, lat: 37.7955, distance: 900, yaw: 240, pitch: 45 },
  { lon: -122.4783, lat: 37.8199, distance: 1400, yaw: 120, pitch: 40 },
  { lon: -122.4862, lat: 37.7694, distance: 1200, yaw: 90, pitch: 45 },
  { lon: -122.4351, lat: 37.8005, distance: 700, yaw: 180, pitch: 45 },
];

function parseArgs(argv) {
  const args = { url: null, minutes: 10, profile: 'mobile', settle: 60, label: '', chrome: process.env.CHROME_PATH || null, out: OUT_DIR };
  for (let i = 0; i < argv.length; i++) {
    const next = () => argv[++i];
    const arg = argv[i];
    if (arg === '--url') args.url = next();
    else if (arg === '--minutes') args.minutes = Number(next());
    else if (arg === '--profile') args.profile = next();
    else if (arg === '--settle') args.settle = Number(next());
    else if (arg === '--label') args.label = next();
    else if (arg === '--chrome') args.chrome = next();
    else if (arg === '--out') args.out = path.resolve(next());
    else throw new Error(`unknown argument ${arg}`);
  }
  if (!args.url) throw new Error('--url is required');
  return args;
}

const PROFILES = {
  desktop: { metrics: { width: 1600, height: 900, deviceScaleFactor: 1, mobile: false }, cpuThrottle: 1, userAgent: null },
  mobile: {
    metrics: { width: 390, height: 844, deviceScaleFactor: 3, mobile: true },
    cpuThrottle: 4,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
  },
};

class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id === undefined) return;
      const entry = this.pending.get(msg.id);
      if (!entry) return;
      this.pending.delete(msg.id);
      if (msg.error) entry.reject(new Error(`${entry.method}: ${msg.error.message}`));
      else entry.resolve(msg.result);
    });
  }

  static async connect(url) {
    const ws = new WebSocket(url);
    await new Promise((resolve, reject) => {
      ws.addEventListener('open', resolve, { once: true });
      ws.addEventListener('error', () => reject(new Error(`cannot connect to ${url}`)), { once: true });
    });
    return new Cdp(ws);
  }

  send(method, params = {}, sessionId) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    return new Promise((resolve, reject) => this.pending.set(id, { resolve, reject, method }));
  }

  close() {
    this.ws.close();
  }
}

function findChrome(explicit) {
  const candidates = [explicit, process.env.CHROME_PATH, '/home/ubuntu/.local/bin/google-chrome', '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean);
  for (const candidate of candidates) if (existsSync(candidate)) return candidate;
  throw new Error('no Chrome binary found — pass --chrome <path>');
}

async function freePort() {
  return new Promise((resolve, reject) => {
    const server = net.createServer();
    server.on('error', reject);
    server.listen(0, '127.0.0.1', () => {
      const { port } = server.address();
      server.close(() => resolve(port));
    });
  });
}

async function waitForHttp(url, timeoutMs) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    try {
      const response = await fetch(url, { redirect: 'manual' });
      if (response.status < 500) return;
    } catch { /* not up */ }
    if (Date.now() > deadline) throw new Error(`timed out waiting for ${url}`);
    await sleep(300);
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const config = PROFILES[args.profile];
  const port = await freePort();
  const userDataDir = await mkdtemp(path.join(os.tmpdir(), 'memgrowth-'));
  const chrome = spawn(findChrome(args.chrome), [
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--enable-unsafe-swiftshader',
    '--js-flags=--expose-gc',
    '--headless=new',
    '--no-sandbox',
  ], { stdio: ['ignore', 'pipe', 'pipe'] });
  chrome.stdout.on('data', () => {});
  chrome.stderr.on('data', () => {});
  await waitForHttp(`http://127.0.0.1:${port}/json/version`, 30000);

  const version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
  const cdp = await Cdp.connect(version.webSocketDebuggerUrl);
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const send = (method, params) => cdp.send(method, params, sessionId);
  const evaluate = async (expression) => {
    const result = await send('Runtime.evaluate', { expression, returnByValue: true });
    if (result.exceptionDetails) return null;
    return result.result.value;
  };

  await send('Page.enable');
  await send('Runtime.enable');
  await send('HeapProfiler.enable');
  await send('Emulation.setDeviceMetricsOverride', { ...config.metrics, screenWidth: config.metrics.width, screenHeight: config.metrics.height });
  if (config.userAgent) {
    await send('Emulation.setUserAgentOverride', { userAgent: config.userAgent, platform: 'Linux armv8l' });
    await send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  }
  await send('Emulation.setCPUThrottlingRate', { rate: config.cpuThrottle });

  console.log(`loading ${args.url} (${args.profile})…`);
  await send('Page.navigate', { url: args.url });

  // Wait for the app handle, then let it settle before the first sample so the
  // baseline is a loaded city rather than a half-built one.
  const ready = Date.now() + 180000;
  while (Date.now() < ready) {
    if (await evaluate('!!(window.SF && window.SF.city)')) break;
    await sleep(2000);
  }
  await sleep(args.settle * 1000);

  // three is bundled, so its constructors are not reachable from `window` and
  // Runtime.queryObjects has no prototype to walk. Traversing the live scene
  // graph answers the same question for the objects that matter, and attributes
  // the bytes to the subsystem that owns them.
  const SCENE_CENSUS = `(() => {
    const S = window.SF; if (!S || !S.scene) return null;
    const census = { objects: 0, meshes: 0, instanced: 0, geometries: 0, attributeMB: 0, materials: 0, byName: {} };
    const geometries = new Set();
    const materials = new Set();
    // Interleaved attributes keep their typed array one level down, and a
    // BatchedMesh's geometry is a reserved buffer shared by every landmark in
    // it — both read wrong through the attribute's own array alone.
    const bytesOf = (a) => (a && a.array ? a.array.byteLength : a && a.data && a.data.array ? a.data.array.byteLength : 0);
    S.scene.traverse((o) => {
      census.objects++;
      if (o.isInstancedMesh) census.instanced++;
      if (!o.isMesh && !o.isPoints && !o.isLine) return;
      census.meshes++;
      if (o.geometry && !geometries.has(o.geometry)) {
        geometries.add(o.geometry);
        let bytes = 0;
        for (const key in o.geometry.attributes) bytes += bytesOf(o.geometry.attributes[key]);
        bytes += bytesOf(o.geometry.index);
        if (o.isInstancedMesh) {
          bytes += bytesOf(o.instanceMatrix);
          bytes += bytesOf(o.instanceColor);
        }
        census.attributeMB += bytes / 1048576;
        const bucket = (o.name || (o.parent && o.parent.name) || o.type).replace(/[0-9].*$/, '') || 'unnamed';
        census.byName[bucket] = +((census.byName[bucket] || 0) + bytes / 1048576).toFixed(2);
      }
      const m = o.material;
      for (const mat of Array.isArray(m) ? m : [m]) if (mat && !materials.has(mat)) materials.add(mat);
    });
    census.geometries = geometries.size;
    census.materials = materials.size;
    census.attributeMB = +census.attributeMB.toFixed(1);
    return census;
  })()`;

  const SUBSYSTEMS = `(() => {
    const S = window.SF; if (!S) return null;
    const r = S.renderer;
    const m = performance.memory || null;
    // Every subsystem read is optional: a debug accessor that throws (or hands
    // back something unserialisable) must cost one field, not the sample.
    const safe = (read) => { try { return JSON.parse(JSON.stringify(read())); } catch { return null; } };
    return {
      heapMB: m ? +(m.usedJSHeapSize / 1048576).toFixed(1) : null,
      heapLimitMB: m ? +(m.jsHeapSizeLimit / 1048576).toFixed(1) : null,
      geometries: r ? r.info.memory.geometries : null,
      textures: r ? r.info.memory.textures : null,
      programs: r ? r.info.programs.length : null,
      frames: r ? r.info.render.frame : null,
      city: safe(() => S.city.stats),
      residents: safe(() => S.population.stats()),
      residentCount: safe(() => S.population.residentCount),
      castCount: safe(() => S.population.castCount),
      cars: safe(() => S.agents.carCount),
      quality: safe(() => S.governor.state().tier),
    };
  })()`;

  const samples = [];
  const started = Date.now();
  const endAt = started + args.minutes * 60000;
  let leg = 0;
  while (Date.now() < endAt) {
    const point = LOOP[leg++ % LOOP.length];
    await evaluate(`window.SF.goTo(${point.lon}, ${point.lat}, ${point.distance}, ${point.yaw}, ${point.pitch}), 1`);
    await sleep(15000);
    const [subsystems, census] = await Promise.all([evaluate(SUBSYSTEMS), evaluate(SCENE_CENSUS)]);
    const sample = { atSeconds: Math.round((Date.now() - started) / 1000), ...(subsystems || {}), census };
    samples.push(sample);
    console.log(
      `  ${String(sample.atSeconds).padStart(4)}s heap ${sample.heapMB} MB | geo ${sample.geometries} | tex ${sample.textures} | scene ${census ? census.meshes : '?'} meshes / ${census ? census.attributeMB : '?'} MB attrs | cells ${sample.city ? sample.city.cellsLoaded : '?'} | ground ${sample.city ? sample.city.groundGroups : '?'} | trees ${sample.city ? sample.city.trees : '?'}`
    );
  }

  // One forced collection at the end separates "retained" from "not yet swept".
  await evaluate('window.gc && window.gc()');
  await sleep(3000);
  const afterGc = await evaluate(SUBSYSTEMS);
  const finalCensus = await evaluate(SCENE_CENSUS);

  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const file = path.join(args.out, `${args.label || 'memory-growth'}-${stamp}.json`);
  await mkdir(args.out, { recursive: true });
  await writeFile(file, JSON.stringify({ tool: 'memory-growth', url: args.url, profile: args.profile, minutes: args.minutes, samples, afterGc, finalCensus }, null, 2));

  const heaps = samples.map((s) => s.heapMB).filter((v) => v !== null);
  if (heaps.length > 1) {
    console.log(`\nheap ${heaps[0]} → ${heaps[heaps.length - 1]} MB (peak ${Math.max(...heaps)}), after gc ${afterGc ? afterGc.heapMB : '?'} MB`);
    console.log(`growth ${(((heaps[heaps.length - 1] - heaps[0]) / args.minutes)).toFixed(1)} MB/min over ${args.minutes} min`);
  }
  if (finalCensus) {
    const top = Object.entries(finalCensus.byName).sort((a, b) => b[1] - a[1]).slice(0, 12);
    console.log('\nscene attribute memory by object name (MB):');
    for (const [name, mb] of top) console.log(`  ${String(mb).padStart(8)}  ${name}`);
  }
  console.log(`\nwrote ${path.relative(ROOT, file)}`);

  await cdp.send('Target.closeTarget', { targetId });
  cdp.close();
  chrome.kill('SIGTERM');
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
