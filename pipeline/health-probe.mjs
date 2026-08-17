#!/usr/bin/env node
// Health probe — the non-fps half of the guardrail.
//
// The perf harness answers "how fast is a frame", which this VM's software
// rasterizer cannot honestly measure. Everything in here is either
// GPU-independent or a structural count, so the numbers are real even on a
// GPU-less box and comparable against a real machine:
//
//   loading      time to first frame, to the boot curtain lifting, bytes and
//                requests on a cold cache-cleared visit
//   main thread  long tasks (>50 ms), total blocking time, event-loop lag —
//                the stutter you feel while the city streams, measured off the
//                JS side rather than the frame cadence
//   memory       heap start/peak/end and slope over a sustained flight, plus
//                the renderer's own geometry/texture/program counts
//   work/frame   peak draw calls and triangles
//   stability    webglcontextlost, page crashes, console errors, 404s
//
// Node 22 (native WebSocket), zero dependencies, headless Chrome over CDP.
// Reads only window.SF and standard browser APIs; changes no app behaviour.
//
//   node pipeline/health-probe.mjs --url https://sf-3d.vercel.app --label prod
//   node pipeline/health-probe.mjs --profile mobile --flight 180
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

// A loop over the city: hero, down into the Mission, across downtown at street
// level, out to the bridge. Camera never stops, which is the case that used to
// grow memory without bound.
const WAYPOINTS = [
  { lon: -122.4194, lat: 37.7749, distance: 3200, yaw: 200, pitch: 55 },
  { lon: -122.418, lat: 37.76, distance: 200, yaw: 210, pitch: 42 },
  { lon: -122.4098, lat: 37.7749, distance: 400, yaw: 160, pitch: 40 },
  { lon: -122.4, lat: 37.789, distance: 200, yaw: 210, pitch: 42 },
  { lon: -122.3937, lat: 37.7955, distance: 900, yaw: 240, pitch: 45 },
  { lon: -122.4783, lat: 37.8199, distance: 1400, yaw: 120, pitch: 40 },
  { lon: -122.4862, lat: 37.7694, distance: 1200, yaw: 90, pitch: 45 },
  { lon: -122.4194, lat: 37.7749, distance: 3200, yaw: 200, pitch: 55 },
];

const PROFILES = {
  desktop: {
    label: 'desktop (unthrottled)',
    metrics: { width: 1600, height: 900, deviceScaleFactor: 1, mobile: false },
    cpuThrottle: 1,
    userAgent: null,
  },
  mobile: {
    label: 'mobile-class (CPU 4x, 390x844 @ dpr 3)',
    metrics: { width: 390, height: 844, deviceScaleFactor: 3, mobile: true },
    cpuThrottle: 4,
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
  },
};
// "Fast 4G" as DevTools defines it. The cold load runs throttled; the flight
// does not, so streaming is never the thing being measured twice.
const FAST_4G = {
  offline: false,
  latency: 70,
  downloadThroughput: (4 * 1024 * 1024) / 8,
  uploadThroughput: (3 * 1024 * 1024) / 8,
};

function parseArgs(argv) {
  const args = {
    profiles: ['desktop', 'mobile'],
    url: null,
    serve: true,
    label: '',
    flight: 150,
    loadTimeout: 240,
    chrome: process.env.CHROME_PATH || null,
    out: OUT_DIR,
  };
  for (let i = 0; i < argv.length; i++) {
    const next = () => argv[++i];
    const arg = argv[i];
    if (arg === '--profile') args.profiles = next().split(',');
    else if (arg === '--url') { args.url = next(); args.serve = false; }
    else if (arg === '--label') args.label = next();
    else if (arg === '--flight') args.flight = Number(next());
    else if (arg === '--load-timeout') args.loadTimeout = Number(next());
    else if (arg === '--chrome') args.chrome = next();
    else if (arg === '--out') args.out = path.resolve(next());
    else if (arg === '--help' || arg === '-h') {
      console.log(`health-probe — loading, main-thread, memory and stability baselines

  --url <url>          app URL (default: spawn 'vite preview' on app/dist)
  --profile a,b        desktop,mobile (default both)
  --flight <s>         sustained flight length per profile (default 150)
  --load-timeout <s>   cap on the throttled cold load (default 240)
  --label <text>       label stored in the JSON
  --out <dir>          output directory (default artifacts/perf)`);
      process.exit(0);
    } else throw new Error(`unknown argument ${arg}`);
  }
  return args;
}

// --------------------------------------------------------------- CDP client
class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    this.listeners = new Set();
    ws.addEventListener('message', (event) => {
      const msg = JSON.parse(event.data);
      if (msg.id !== undefined) {
        const entry = this.pending.get(msg.id);
        if (!entry) return;
        this.pending.delete(msg.id);
        if (msg.error) entry.reject(new Error(`${entry.method}: ${msg.error.message}`));
        else entry.resolve(msg.result);
        return;
      }
      for (const listener of this.listeners) listener(msg);
    });
  }

  static async connect(url) {
    if (typeof WebSocket !== 'function') throw new Error('global WebSocket missing — run on Node 22');
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

  on(listener) {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }

  close() {
    this.ws.close();
  }
}

// -------------------------------------------------------------- page probe
// Installed before any app script. Everything it records is main-thread or
// browser-reported, so none of it depends on the host having a GPU.
const PROBE = `(() => {
  const p = {
    longTasks: [],
    lag: [],
    contextLost: 0,
    contextRestored: 0,
    errors: [],
    firstFrameAt: null,
    curtainGoneAt: null,
    peakCalls: 0,
    peakTriangles: 0,
    frames: 0,
    rasterMs: 0,
    wrapped: false,
  };
  try {
    new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) p.longTasks.push({ t: entry.startTime, ms: entry.duration });
    }).observe({ entryTypes: ['longtask'] });
  } catch (e) { p.longTaskSupport = false; }

  // Event-loop lag: a timer that should fire every 250 ms. How late it is, is
  // how long the main thread was busy — the same block that makes a drag feel
  // stuck. Recorded, never acted on.
  let expected = performance.now() + 250;
  setInterval(() => {
    const now = performance.now();
    p.lag.push(Math.max(0, now - expected));
    expected = now + 250;
  }, 250);

  addEventListener('error', (e) => p.errors.push(String(e.message).slice(0, 200)));
  addEventListener('unhandledrejection', (e) => p.errors.push('rejection: ' + String(e.reason).slice(0, 200)));
  addEventListener('webglcontextlost', () => p.contextLost++, true);
  addEventListener('webglcontextrestored', () => p.contextRestored++, true);

  const poll = setInterval(() => {
    const r = window.SF && window.SF.renderer;
    if (p.firstFrameAt === null && r && r.info.render.frame > 0) p.firstFrameAt = performance.now();
    if (p.curtainGoneAt === null && !document.getElementById('boot')) p.curtainGoneAt = performance.now();
    // renderer.info resets on every render() call, so peaks have to be read
    // inside the call, not polled. Time spent inside render() is rasterization,
    // which on a software rasterizer dwarfs everything; keeping it separate
    // leaves the app's own per-frame JS visible underneath.
    if (r && !p.wrapped) {
      p.wrapped = true;
      const original = r.render.bind(r);
      r.render = (scene, camera) => {
        const t0 = performance.now();
        original(scene, camera);
        p.rasterMs += performance.now() - t0;
        p.frames++;
        if (r.info.render.calls > p.peakCalls) p.peakCalls = r.info.render.calls;
        if (r.info.render.triangles > p.peakTriangles) p.peakTriangles = r.info.render.triangles;
      };
    }
    if (p.firstFrameAt !== null && p.curtainGoneAt !== null && performance.now() > 300000) clearInterval(poll);
  }, 50);

  p.mark = () => {
    const r = window.SF && window.SF.renderer;
    const m = performance.memory || null;
    const tasks = p.longTasks;
    const blocking = tasks.reduce((sum, t) => sum + Math.max(0, t.ms - 50), 0);
    const lag = p.lag.slice().sort((a, b) => a - b);
    return {
      atMs: performance.now(),
      firstFrameMs: p.firstFrameAt,
      curtainGoneMs: p.curtainGoneAt,
      longTasks: tasks.length,
      longTasksOver200: tasks.filter((t) => t.ms > 200).length,
      longestTaskMs: tasks.reduce((max, t) => Math.max(max, t.ms), 0) || null,
      totalBlockingMs: Math.round(blocking),
      eventLoopLagP50Ms: lag.length ? Math.round(lag[Math.floor(lag.length * 0.5)]) : null,
      eventLoopLagP95Ms: lag.length ? Math.round(lag[Math.floor(lag.length * 0.95)]) : null,
      eventLoopLagMaxMs: lag.length ? Math.round(lag[lag.length - 1]) : null,
      heapMB: m ? +(m.usedJSHeapSize / 1048576).toFixed(1) : null,
      heapLimitMB: m ? +(m.jsHeapSizeLimit / 1048576).toFixed(1) : null,
      drawCallsPeak: p.peakCalls,
      trianglesPeak: p.peakTriangles,
      frames: p.frames,
      rasterMsPerFrame: p.frames ? +(p.rasterMs / p.frames).toFixed(1) : null,
      geometries: r ? r.info.memory.geometries : null,
      textures: r ? r.info.memory.textures : null,
      programs: r ? r.info.programs.length : null,
      contextLost: p.contextLost,
      contextRestored: p.contextRestored,
      errors: p.errors.slice(0, 10),
      cityStats: window.SF && window.SF.city ? JSON.parse(JSON.stringify(window.SF.city.stats)) : null,
      quality: window.SF && window.SF.governor && window.SF.governor.state ? window.SF.governor.state().tier : null,
    };
  };
  p.resetWindow = () => {
    p.longTasks.length = 0;
    p.lag.length = 0;
    p.frames = 0;
    p.rasterMs = 0;
    p.peakCalls = 0;
    p.peakTriangles = 0;
  };
  window.__health = p;
})();`;

// ------------------------------------------------------------ small helpers
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

function findChrome(explicit) {
  const candidates = [
    explicit,
    process.env.CHROME_PATH,
    '/home/ubuntu/.local/bin/google-chrome',
    '/usr/bin/google-chrome',
    '/usr/bin/google-chrome-stable',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);
  for (const candidate of candidates) if (existsSync(candidate)) return candidate;
  throw new Error('no Chrome binary found — pass --chrome <path> or set CHROME_PATH');
}

async function waitForHttp(url, timeoutMs = 60000) {
  const deadline = Date.now() + timeoutMs;
  for (;;) {
    try {
      const response = await fetch(url, { redirect: 'manual' });
      if (response.status < 500) return true;
    } catch { /* not up yet */ }
    if (Date.now() > deadline) throw new Error(`timed out waiting for ${url}`);
    await sleep(300);
  }
}

async function startPreview() {
  const port = await freePort();
  const child = spawn('npx', ['vite', 'preview', '--port', String(port), '--strictPort'], {
    cwd: path.join(ROOT, 'app'),
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  child.stdout.on('data', () => {});
  child.stderr.on('data', () => {});
  const url = `http://127.0.0.1:${port}/`;
  await waitForHttp(url);
  return { url, stop: () => child.kill('SIGTERM') };
}

async function launchChrome(chrome) {
  const port = await freePort();
  const userDataDir = await mkdtemp(path.join(os.tmpdir(), 'health-probe-'));
  const child = spawn(findChrome(chrome), [
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--enable-unsafe-swiftshader',
    '--headless=new',
    '--window-size=1600,900',
    '--no-sandbox',
  ], { stdio: ['ignore', 'pipe', 'pipe'] });
  child.stdout.on('data', () => {});
  child.stderr.on('data', () => {});
  await waitForHttp(`http://127.0.0.1:${port}/json/version`, 30000);
  return { port, stop: () => child.kill('SIGTERM') };
}

class Session {
  constructor(cdp, sessionId) {
    this.cdp = cdp;
    this.sessionId = sessionId;
  }

  send(method, params) {
    return this.cdp.send(method, params, this.sessionId);
  }

  async eval(expression, awaitPromise = false) {
    const result = await this.send('Runtime.evaluate', { expression, returnByValue: true, awaitPromise });
    if (result.exceptionDetails) {
      throw new Error(`eval failed: ${result.exceptionDetails.exception?.description || result.exceptionDetails.text}`);
    }
    return result.result.value;
  }
}

// -------------------------------------------------------------- the two runs
async function coldLoad(page, network, args, traffic) {
  await page.send('Network.clearBrowserCache');
  await page.send('Network.emulateNetworkConditions', network);
  traffic.reset();
  const startedAt = Date.now();
  await page.send('Page.navigate', { url: args.url });

  const deadline = startedAt + args.loadTimeout * 1000;
  let mark = null;
  for (;;) {
    mark = await page.eval('window.__health ? window.__health.mark() : null').catch(() => null);
    if (mark && mark.curtainGoneMs !== null) break;
    if (Date.now() > deadline) break;
    await sleep(500);
  }
  // A few seconds past the reveal is what a visitor actually waits through:
  // the curtain lifts on a presentable city, not a complete one.
  await sleep(5000);
  const after = await page.eval('window.__health.mark()');
  await page.send('Network.emulateNetworkConditions', { offline: false, latency: 0, downloadThroughput: -1, uploadThroughput: -1 });
  return {
    network: 'Fast 4G (4 Mbps / 70 ms RTT), cold cache',
    timeToFirstFrameMs: after.firstFrameMs === null ? null : Math.round(after.firstFrameMs),
    timeToCurtainLiftMs: after.curtainGoneMs === null ? null : Math.round(after.curtainGoneMs),
    curtainLifted: after.curtainGoneMs !== null,
    wallSeconds: +((Date.now() - startedAt) / 1000).toFixed(1),
    ...traffic.summary(),
    totalBlockingMs: after.totalBlockingMs,
    longTasks: after.longTasks,
    longTasksOver200: after.longTasksOver200,
    longestTaskMs: after.longestTaskMs === null ? null : Math.round(after.longestTaskMs),
    eventLoopLagP95Ms: after.eventLoopLagP95Ms,
    eventLoopLagMaxMs: after.eventLoopLagMaxMs,
    heapMB: after.heapMB,
    cityStats: after.cityStats,
    quality: after.quality,
    errors: after.errors,
  };
}

async function flight(page, args, traffic) {
  await page.eval('window.__health.resetWindow(), 1');
  traffic.reset();
  const samples = [];
  const started = Date.now();
  const legMs = (args.flight * 1000) / WAYPOINTS.length;
  for (const point of WAYPOINTS) {
    await page.eval(
      `window.SF.goTo(${point.lon}, ${point.lat}, ${point.distance}, ${point.yaw}, ${point.pitch}), 1`
    ).catch(() => {});
    const legEnd = Date.now() + legMs;
    while (Date.now() < legEnd) {
      await sleep(Math.min(5000, Math.max(500, legEnd - Date.now())));
      const mark = await page.eval('window.__health.mark()').catch(() => null);
      if (mark) samples.push(mark);
    }
  }
  const heaps = samples.map((s) => s.heapMB).filter((v) => v !== null);
  const last = samples[samples.length - 1] || {};
  return {
    seconds: +((Date.now() - started) / 1000).toFixed(1),
    waypoints: WAYPOINTS.length,
    heapStartMB: heaps[0] ?? null,
    heapPeakMB: heaps.length ? Math.max(...heaps) : null,
    heapEndMB: heaps.length ? heaps[heaps.length - 1] : null,
    heapGrowthMBPerMin:
      heaps.length > 1 ? +(((heaps[heaps.length - 1] - heaps[0]) / (args.flight / 60))).toFixed(1) : null,
    heapLimitMB: last.heapLimitMB ?? null,
    drawCallsPeak: last.drawCallsPeak ?? null,
    trianglesPeak: last.trianglesPeak ?? null,
    frames: last.frames ?? null,
    rasterMsPerFrame: last.rasterMsPerFrame ?? null,
    geometriesEnd: last.geometries ?? null,
    texturesEnd: last.textures ?? null,
    programsEnd: last.programs ?? null,
    longTasks: last.longTasks ?? null,
    longTasksOver200: last.longTasksOver200 ?? null,
    longestTaskMs: last.longestTaskMs === null || last.longestTaskMs === undefined ? null : Math.round(last.longestTaskMs),
    totalBlockingMs: last.totalBlockingMs ?? null,
    eventLoopLagP50Ms: last.eventLoopLagP50Ms ?? null,
    eventLoopLagP95Ms: last.eventLoopLagP95Ms ?? null,
    eventLoopLagMaxMs: last.eventLoopLagMaxMs ?? null,
    contextLost: last.contextLost ?? null,
    contextRestored: last.contextRestored ?? null,
    errors: last.errors ?? [],
    cityStats: last.cityStats ?? null,
    quality: last.quality ?? null,
    ...traffic.summary(),
    samples: samples.map((s) => ({ atMs: Math.round(s.atMs), heapMB: s.heapMB, geometries: s.geometries })),
  };
}

// Bytes on the wire, counted from the network events rather than from the
// resource timings, so cached and preflight traffic is included.
function trackTraffic(cdp, sessionId) {
  let bytes = 0;
  let requests = 0;
  let failures = 0;
  const notFound = new Set();
  cdp.on((msg) => {
    if (msg.sessionId !== sessionId) return;
    if (msg.method === 'Network.requestWillBeSent') requests++;
    else if (msg.method === 'Network.loadingFinished') bytes += msg.params.encodedDataLength || 0;
    else if (msg.method === 'Network.loadingFailed') failures++;
    else if (msg.method === 'Network.responseReceived' && msg.params.response.status === 404) {
      notFound.add(msg.params.response.url.slice(-80));
    }
  });
  return {
    reset() {
      bytes = 0;
      requests = 0;
      failures = 0;
      notFound.clear();
    },
    summary() {
      return {
        transferredMB: +(bytes / 1048576).toFixed(1),
        requests,
        failedRequests: failures,
        notFound: [...notFound].slice(0, 5),
      };
    },
  };
}

async function runProfile(chromePort, profile, args) {
  const config = PROFILES[profile];
  const version = await (await fetch(`http://127.0.0.1:${chromePort}/json/version`)).json();
  const cdp = await Cdp.connect(version.webSocketDebuggerUrl);
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const page = new Session(cdp, sessionId);
  let crashed = false;
  cdp.on((msg) => {
    if (msg.sessionId === sessionId && msg.method === 'Inspector.targetCrashed') crashed = true;
  });
  await page.send('Page.enable');
  await page.send('Runtime.enable');
  await page.send('Network.enable');
  await page.send('Inspector.enable');
  await page.send('Page.addScriptToEvaluateOnNewDocument', { source: PROBE });
  await page.send('Emulation.setDeviceMetricsOverride', {
    ...config.metrics,
    screenWidth: config.metrics.width,
    screenHeight: config.metrics.height,
  });
  if (config.userAgent) {
    await page.send('Emulation.setUserAgentOverride', { userAgent: config.userAgent, platform: 'Linux armv8l' });
    await page.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  }
  await page.send('Emulation.setCPUThrottlingRate', { rate: config.cpuThrottle });

  const traffic = trackTraffic(cdp, sessionId);
  console.log(`[${profile}] cold load on Fast 4G…`);
  const load = await coldLoad(page, FAST_4G, args, traffic);
  console.log(`[${profile}] ${args.flight}s flight…`);
  const flown = await flight(page, args, traffic);

  await cdp.send('Target.closeTarget', { targetId });
  cdp.close();
  return { profile, label: config.label, crashed, load, flight: flown };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  let server = null;
  if (!args.url) {
    server = await startPreview();
    args.url = server.url;
    console.log(`serving ${args.url}`);
  }
  const chrome = await launchChrome(args.chrome);
  const profiles = [];
  try {
    for (const profile of args.profiles) profiles.push(await runProfile(chrome.port, profile, args));
  } finally {
    chrome.stop();
    if (server) server.stop();
  }

  const stamp = new Date().toISOString().replace(/[:.]/g, '-');
  const file = path.join(args.out, `${args.label || 'health'}-${stamp}.json`);
  await mkdir(args.out, { recursive: true });
  await writeFile(file, JSON.stringify({ tool: 'health-probe', label: args.label, url: args.url, startedAt: stamp, profiles }, null, 2));

  for (const p of profiles) {
    console.log(`\n=== ${p.profile} — ${p.label}${p.crashed ? '  *** RENDERER CRASHED ***' : ''}`);
    console.log('  cold load  first frame %s ms | curtain %s | %s MB over %s requests | TBT %s ms | longest task %s ms',
      p.load.timeToFirstFrameMs, p.load.curtainLifted ? `${p.load.timeToCurtainLiftMs} ms` : 'NEVER LIFTED',
      p.load.transferredMB, p.load.requests, p.load.totalBlockingMs, p.load.longestTaskMs);
    console.log('  flight     heap %s → %s MB (peak %s, %s MB/min) | geometries %s | calls %s | tris %sM',
      p.flight.heapStartMB, p.flight.heapEndMB, p.flight.heapPeakMB, p.flight.heapGrowthMBPerMin,
      p.flight.geometriesEnd, p.flight.drawCallsPeak, ((p.flight.trianglesPeak || 0) / 1e6).toFixed(2));
    console.log('  main thread lag p50 %s ms / p95 %s ms / max %s ms | long tasks %s (%s over 200 ms)',
      p.flight.eventLoopLagP50Ms, p.flight.eventLoopLagP95Ms, p.flight.eventLoopLagMaxMs,
      p.flight.longTasks, p.flight.longTasksOver200);
    console.log('  stability  context lost %s | failed requests %s | 404s %s | errors %s',
      p.flight.contextLost, p.flight.failedRequests, p.flight.notFound.length, p.flight.errors.length);
  }
  console.log(`\nwrote ${path.relative(ROOT, file)}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
