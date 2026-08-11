#!/usr/bin/env node
// Perf harness (PERF-PLAN.md workstream #0): flies the camera to the stress
// stations, measures what actually happened, and writes one JSON + one console
// table per run under artifacts/perf/.
//
// It changes ZERO app runtime behaviour: everything it needs is read through
// the app's own `window.SF` handle, plus a page-side probe that the harness
// injects into the browser (never into app/src).
//
// Node 22 (native fetch + WebSocket), zero dependencies, headless Chrome over
// the DevTools protocol.
//
//   node pipeline/perf-harness.mjs --label baseline-main
//   node pipeline/perf-harness.mjs --profile desktop --sample 10
//   node pipeline/perf-harness.mjs --url http://localhost:4173 --no-serve
//
// See .agents/skills/testing-sf-3d/SKILL.md ("Perf harness") for the full
// recipe, including the manual window.SF sweep for Safari / Edge / Firefox.

import { execFileSync, spawn } from 'node:child_process';
import { mkdir, mkdtemp, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT_DIR = path.join(ROOT, 'artifacts', 'perf');

// ----------------------------------------------------------------- stations
// Four locations x day/night. The clock is pinned to a fixed calendar date so
// runs taken on different days are comparable (SF.setTime is deprecated —
// SF.setClock is the only deterministic pin, see the testing skill).
const DAY = '2026-08-01T13:00:00-07:00';
const NIGHT = '2026-08-01T22:00:00-07:00';

const STATIONS = [
  { id: 'hero', name: 'Hero view', preset: 0 },
  { id: 'mission-street', name: 'Mission street level', lon: -122.418, lat: 37.76, distance: 200, yaw: 210, pitch: 42 },
  { id: 'downtown-street', name: 'Downtown street level', lon: -122.4, lat: 37.789, distance: 200, yaw: 210, pitch: 42 },
  { id: 'golden-gate', name: 'Golden Gate', preset: 'goldenGateBridge' },
];
const CLOCKS = [
  { id: 'day', iso: DAY },
  { id: 'night', iso: NIGHT },
];

// --------------------------------------------------------------- CLI parsing
function parseArgs(argv) {
  const args = {
    profiles: ['desktop', 'mobile'],
    url: null,
    serve: true,
    sample: 10,
    settle: 90,
    label: '',
    quality: null,
    out: OUT_DIR,
    headless: true,
    chrome: process.env.CHROME_PATH || null,
    attach: null,
    loadTest: true,
    loadTimeout: 420,
  };
  for (let i = 0; i < argv.length; i++) {
    const arg = argv[i];
    const next = () => argv[++i];
    if (arg === '--profile') args.profiles = next().split(',');
    else if (arg === '--url') args.url = next();
    else if (arg === '--no-serve') args.serve = false;
    else if (arg === '--sample') args.sample = Number(next());
    else if (arg === '--settle') args.settle = Number(next());
    else if (arg === '--label') args.label = next();
    else if (arg === '--quality') args.quality = next();
    else if (arg === '--out') args.out = path.resolve(next());
    else if (arg === '--headful') args.headless = false;
    else if (arg === '--chrome') args.chrome = next();
    else if (arg === '--attach') args.attach = Number(next());
    else if (arg === '--no-load-test') args.loadTest = false;
    else if (arg === '--load-timeout') args.loadTimeout = Number(next());
    else if (arg === '--stations') {
      const wanted = next().split(',');
      STATIONS.splice(0, STATIONS.length, ...STATIONS.filter((s) => wanted.includes(s.id)));
    } else if (arg === '--help' || arg === '-h') {
      console.log(HELP);
      process.exit(0);
    } else throw new Error(`unknown argument ${arg}`);
  }
  return args;
}

const HELP = `perf-harness — measure the SF diorama against PERF-PLAN.md's guardrail

  --profile desktop,mobile   which profiles to run (default: both)
  --url <url>                app URL (default: spawn 'vite preview' on a free port)
  --no-serve                 do not spawn a server; requires --url
  --sample <s>               frame-cadence sample length per station (default 10)
  --settle <s>               max wait for tiles/near-tier to settle (default 90)
  --quality <tier>           pin SF quality before sampling (ultra|high|medium|low)
  --label <text>             label stored in the JSON (e.g. baseline-main)
  --stations a,b             subset of hero,mission-street,downtown-street,golden-gate
  --no-load-test             skip the throttled time-to-tiles measurement
  --load-timeout <s>         cap on the throttled cold load (default 420)
  --headful / --chrome <p>   browser control
  --attach <port>            use an already running Chrome's DevTools port
  --out <dir>                output directory (default artifacts/perf)`;

// ------------------------------------------------------------ CDP plumbing
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
    if (typeof WebSocket !== 'function') {
      throw new Error('global WebSocket missing — run this harness on Node 22 (nvm use 22)');
    }
    const ws = new WebSocket(url);
    await new Promise((resolve, reject) => {
      ws.addEventListener('open', resolve, { once: true });
      ws.addEventListener('error', () => reject(new Error(`cannot connect to ${url}`)), { once: true });
    });
    return new Cdp(ws);
  }

  send(method, params = {}, sessionId) {
    const id = ++this.id;
    const payload = { id, method, params };
    if (sessionId) payload.sessionId = sessionId;
    this.ws.send(JSON.stringify(payload));
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

class Page {
  constructor(cdp, sessionId) {
    this.cdp = cdp;
    this.sessionId = sessionId;
  }

  send(method, params) {
    return this.cdp.send(method, params, this.sessionId);
  }

  async eval(expression, { awaitPromise = false } = {}) {
    const result = await this.send('Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise,
    });
    if (result.exceptionDetails) {
      throw new Error(`page eval failed: ${result.exceptionDetails.exception?.description || result.exceptionDetails.text}`);
    }
    return result.result.value;
  }
}

// -------------------------------------------------------------- page probe
// Injected before any app script runs. Keeps its own rAF loop (piggybacks on
// the frames the app already requests) and wraps renderer.render only while a
// sample is running, so the app's own code path is untouched.
const PROBE = `(() => {
  const probe = {
    deltas: [],
    sampling: false,
    peakCalls: 0,
    peakTriangles: 0,
    lastFrame: 0,
    started: 0,
    frames: 0,
  };
  let prev = 0;
  function tick(now) {
    if (probe.sampling) {
      if (prev) probe.deltas.push(now - prev);
      probe.frames++;
    }
    prev = now;
    requestAnimationFrame(tick);
  }
  requestAnimationFrame(tick);

  probe.start = () => {
    probe.deltas.length = 0;
    probe.frames = 0;
    probe.peakCalls = 0;
    probe.peakTriangles = 0;
    probe.started = performance.now();
    const r = window.SF && window.SF.renderer;
    if (r && !r.__perfWrapped) {
      r.__perfWrapped = true;
      const original = r.render.bind(r);
      r.render = (scene, camera) => {
        original(scene, camera);
        const calls = r.info.render.calls;
        // The scene pass, not the fullscreen post quad the overlay reports.
        if (calls > probe.peakCalls) {
          probe.peakCalls = calls;
          probe.peakTriangles = r.info.render.triangles;
        }
      };
    }
    probe.startFrame = r ? r.info.render.frame : 0;
    prev = 0;
    probe.sampling = true;
  };

  probe.stop = () => {
    probe.sampling = false;
    const wall = (performance.now() - probe.started) / 1000;
    const deltas = probe.deltas.slice().sort((a, b) => a - b);
    const r = window.SF && window.SF.renderer;
    const pct = (p) => (deltas.length ? deltas[Math.min(deltas.length - 1, Math.floor(deltas.length * p))] : null);
    const mean = deltas.length ? deltas.reduce((a, b) => a + b, 0) / deltas.length : null;
    const memory = performance.memory || null;
    return {
      sampleSeconds: wall,
      rafFrames: probe.frames,
      // Real cadence, never the overlay's fps field (see the testing skill).
      fpsMean: deltas.length ? 1000 / mean : 0,
      fpsFromWall: probe.frames / wall,
      frameTimeMeanMs: mean,
      frameTimeP50Ms: pct(0.5),
      frameTimeP95Ms: pct(0.95),
      frameTimeMaxMs: deltas.length ? deltas[deltas.length - 1] : null,
      rendererFrames: r ? r.info.render.frame - probe.startFrame : null,
      drawCallsPeak: probe.peakCalls,
      drawCallsLast: r ? r.info.render.calls : null,
      triangles: probe.peakTriangles,
      geometries: r ? r.info.memory.geometries : null,
      textures: r ? r.info.memory.textures : null,
      jsHeapMB: memory ? +(memory.usedJSHeapSize / 1048576).toFixed(1) : null,
      pixelRatio: r ? r.getPixelRatio() : null,
      cityStats: window.SF && window.SF.city ? JSON.parse(JSON.stringify(window.SF.city.stats)) : null,
      cityProgress: window.SF && window.SF.city ? window.SF.city.progress : null,
      governor: window.SF && window.SF.governor ? JSON.parse(JSON.stringify(window.SF.governor.state ? window.SF.governor.state() : window.SF.governor)) : null,
    };
  };

  window.__perf = probe;
})();`;

// ------------------------------------------------------------ small helpers
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

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
    '/usr/bin/chromium-browser',
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
    } catch {
      /* not up yet */
    }
    if (Date.now() > deadline) throw new Error(`timed out waiting for ${url}`);
    await sleep(300);
  }
}

// --------------------------------------------------------------- app server
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

// ------------------------------------------------------------------ browser
async function launchChrome({ headless, chrome }) {
  const port = await freePort();
  const userDataDir = await mkdtemp(path.join(os.tmpdir(), 'perf-harness-'));
  const binary = findChrome(chrome);
  const flags = [
    `--remote-debugging-port=${port}`,
    `--user-data-dir=${userDataDir}`,
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding',
    '--enable-unsafe-swiftshader',
    '--window-size=1600,900',
    '--no-sandbox',
  ];
  if (headless) flags.push('--headless=new');
  const child = spawn(binary, flags, { stdio: ['ignore', 'pipe', 'pipe'] });
  child.stdout.on('data', () => {});
  child.stderr.on('data', () => {});
  await waitForHttp(`http://127.0.0.1:${port}/json/version`, 30000);
  return { port, stop: () => child.kill('SIGTERM') };
}

async function openPage(port, profile) {
  const version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
  const cdp = await Cdp.connect(version.webSocketDebuggerUrl);
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const page = new Page(cdp, sessionId);
  await page.send('Page.enable');
  await page.send('Runtime.enable');
  await page.send('Network.enable');
  await page.send('Page.addScriptToEvaluateOnNewDocument', { source: PROBE });
  await applyProfile(page, profile);
  return { cdp, page, targetId };
}

// The two guardrail profiles. GPU class cannot be emulated by CDP — the mobile
// profile is CPU + viewport/DPR + (for the load test) network only, so real
// mobile-Safari numbers still come from the manual recipe in the testing skill.
const PROFILES = {
  desktop: {
    label: 'desktop (unthrottled)',
    metrics: { width: 1600, height: 900, deviceScaleFactor: 1, mobile: false },
    cpuThrottle: 1,
    network: null,
    userAgent: null,
  },
  mobile: {
    label: 'mobile-class (CPU 4x, 390x844 @ dpr 3)',
    metrics: { width: 390, height: 844, deviceScaleFactor: 3, mobile: true },
    cpuThrottle: 4,
    // "Fast 4G" as DevTools defines it; applied to the load test only.
    network: { offline: false, latency: 70, downloadThroughput: (4 * 1024 * 1024) / 8, uploadThroughput: (3 * 1024 * 1024) / 8 },
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
  },
};

async function applyProfile(page, profile) {
  const config = PROFILES[profile];
  await page.send('Emulation.setDeviceMetricsOverride', {
    ...config.metrics,
    screenWidth: config.metrics.width,
    screenHeight: config.metrics.height,
  });
  if (config.userAgent) {
    await page.send('Emulation.setUserAgentOverride', {
      userAgent: config.userAgent,
      platform: 'Linux armv8l',
    });
    await page.send('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  }
  await page.send('Emulation.setCPUThrottlingRate', { rate: config.cpuThrottle });
}

// ------------------------------------------------------------- measurement
async function waitForCity(page, settleSeconds) {
  const deadline = Date.now() + settleSeconds * 1000;
  let stable = 0;
  let last = null;
  // `progress` only reaches 1 when every cell in the city has streamed, which a
  // street-level view never asks for — so "nothing new for 10 s" also counts as
  // settled, and the reached progress is recorded either way.
  const QUIET_POLLS = 10;
  for (;;) {
    const snapshot = await page.eval(
      `(() => { const c = window.SF && window.SF.city; if (!c) return null;
        return { progress: c.progress, cellsLoaded: c.stats.cellsLoaded, cellsTotal: c.stats.cellsTotal,
                 nearChunks: c.stats.nearChunks, farGroups: c.stats.farGroups }; })()`
    );
    if (snapshot) {
      const key = snapshot ? `${snapshot.cellsLoaded}/${snapshot.nearChunks}/${snapshot.farGroups}` : '';
      // "Loaded" is the streamer's own definition; the near tier must ALSO stop
      // changing, otherwise the sample catches geometry uploads, not steady state.
      if (key === last) stable++;
      else stable = 0;
      last = key;
      if (stable >= (snapshot.progress > 0.985 ? 3 : QUIET_POLLS)) return { settled: true, ...snapshot };
    }
    if (Date.now() > deadline) return { settled: false, ...(snapshot || {}) };
    await sleep(1000);
  }
}

async function gotoStation(page, station) {
  if (station.preset !== undefined) {
    await page.eval(
      `(() => { const presets = window.SF.presets;
        const i = ${typeof station.preset === 'number' ? station.preset : `presets.findIndex((p) => p.id === ${JSON.stringify(station.preset)})`};
        const preset = presets[i < 0 ? 0 : i];
        window.SF.rig.set(preset);
        return preset.name; })()`
    );
    return;
  }
  await page.eval(
    `window.SF.goTo(${station.lon}, ${station.lat}, ${station.distance}, ${station.yaw}, ${station.pitch}), 'ok'`
  );
}

async function measureStation(page, station, clock, args) {
  await gotoStation(page, station);
  await page.eval(`window.SF.setClock(${JSON.stringify(clock.iso)}), 'ok'`);
  const settle = await waitForCity(page, args.settle);
  // Extra breath so freshly built near-tier chunks are uploaded before sampling.
  await sleep(3000);
  await page.eval('window.__perf.start(), "ok"');
  await sleep(args.sample * 1000);
  const sample = await page.eval('window.__perf.stop()');
  return {
    station: station.id,
    name: station.name,
    clock: clock.id,
    clockIso: clock.iso,
    settled: settle.settled,
    ...sample,
  };
}

// One throttled cold load per run: how long until the city is actually there.
async function measureLoad(page, url, profile, args) {
  const config = PROFILES[profile];
  const network = config.network || {
    offline: false,
    latency: 70,
    downloadThroughput: (4 * 1024 * 1024) / 8,
    uploadThroughput: (3 * 1024 * 1024) / 8,
  };
  await page.send('Network.setCacheDisabled', { cacheDisabled: true });
  await page.send('Network.emulateNetworkConditions', network);
  let bytes = 0;
  const off = page.cdp.on((msg) => {
    if (msg.sessionId !== page.sessionId) return;
    if (msg.method === 'Network.loadingFinished') bytes += msg.params.encodedDataLength || 0;
  });
  const started = Date.now();
  await page.send('Page.navigate', { url });
  let firstFrame = null;
  let full = null;
  const deadline = started + args.loadTimeout * 1000;
  for (;;) {
    const state = await page
      .eval('(() => { const c = window.SF && window.SF.city; return c ? { p: c.progress, loaded: c.stats.cellsLoaded, total: c.stats.cellsTotal } : null; })()')
      .catch(() => null);
    if (state) {
      if (firstFrame === null) firstFrame = (Date.now() - started) / 1000;
      if (state.p > 0.985) {
        full = { seconds: +((Date.now() - started) / 1000).toFixed(1), cells: state.loaded, total: state.total };
        break;
      }
    }
    if (Date.now() > deadline) {
      full = { seconds: null, timedOut: true, cells: state?.loaded ?? null, total: state?.total ?? null };
      break;
    }
    await sleep(500);
  }
  off();
  await page.send('Network.emulateNetworkConditions', {
    offline: false,
    latency: 0,
    downloadThroughput: -1,
    uploadThroughput: -1,
  });
  await page.send('Network.setCacheDisabled', { cacheDisabled: false });
  return {
    profileNetwork: 'Fast 4G (4 Mbps / 70 ms RTT)',
    timeToSFms: firstFrame === null ? null : +(firstFrame * 1000).toFixed(0),
    timeToTilesSeconds: full.seconds,
    timedOut: Boolean(full.timedOut),
    cellsLoaded: full.cells,
    cellsTotal: full.total,
    transferredMB: +(bytes / 1048576).toFixed(1),
  };
}

async function runProfile(profile, url, args) {
  const browser = args.attach ? { port: args.attach, stop: () => {} } : await launchChrome(args);
  const { cdp, page, targetId } = await openPage(browser.port, profile);
  const result = { profile, label: PROFILES[profile].label, stations: [], load: null };
  try {
    let load = null;
    if (args.loadTest) {
      process.stderr.write(`[${profile}] cold load on ${PROFILES[profile].network ? 'Fast 4G' : 'Fast 4G (load test)'}…\n`);
      load = await measureLoad(page, url, profile, args);
      result.load = load;
    } else {
      await page.send('Page.navigate', { url });
    }
    await waitForCity(page, args.settle);
    result.environment = await page.eval(
      `(() => { const gl = document.createElement('canvas').getContext('webgl2');
        const ext = gl && gl.getExtension('WEBGL_debug_renderer_info');
        return { userAgent: navigator.userAgent, dpr: window.devicePixelRatio,
                 viewport: [window.innerWidth, window.innerHeight],
                 hardwareConcurrency: navigator.hardwareConcurrency,
                 gpu: ext ? gl.getParameter(ext.UNMASKED_RENDERER_WEBGL) : null }; })()`
    );
    if (args.quality) {
      await page.eval(`(() => { const s = [...document.querySelectorAll('select')].find((el) => [...el.options].some((o) => o.value === ${JSON.stringify(args.quality)}));
        if (s) { s.value = ${JSON.stringify(args.quality)}; s.dispatchEvent(new Event('change')); } return s ? s.value : null; })()`);
    }
    for (const station of STATIONS) {
      for (const clock of CLOCKS) {
        process.stderr.write(`[${profile}] ${station.id} / ${clock.id}…\n`);
        const measurement = await measureStation(page, station, clock, args);
        result.stations.push(measurement);
      }
    }
  } finally {
    await cdp.send('Target.closeTarget', { targetId }).catch(() => {});
    cdp.close();
    browser.stop();
  }
  return result;
}

function gitInfo() {
  const read = (args) => {
    try {
      return execFileSync('git', args, { cwd: ROOT, encoding: 'utf8' }).trim();
    } catch {
      return null;
    }
  };
  return { branch: read(['rev-parse', '--abbrev-ref', 'HEAD']), commit: read(['rev-parse', '--short', 'HEAD']) };
}

// ------------------------------------------------------------------ output
function table(run) {
  const rows = [];
  for (const profile of run.profiles) {
    for (const s of profile.stations) {
      rows.push({
        profile: profile.profile,
        station: `${s.station}/${s.clock}`,
        fps: s.fpsMean === null ? '—' : s.fpsMean.toFixed(1),
        'p95 ms': s.frameTimeP95Ms === null ? '—' : s.frameTimeP95Ms.toFixed(1),
        calls: String(s.drawCallsPeak ?? '—'),
        'tris M': s.triangles === null ? '—' : (s.triangles / 1e6).toFixed(2),
        geom: String(s.geometries ?? '—'),
        'heap MB': String(s.jsHeapMB ?? '—'),
        tiles: s.cityStats ? `${s.cityStats.cellsLoaded}/${s.cityStats.cellsTotal}` : '—',
        settled: s.settled ? 'yes' : 'NO',
      });
    }
  }
  if (!rows.length) return '(no rows)';
  const columns = Object.keys(rows[0]);
  const width = Object.fromEntries(
    columns.map((c) => [c, Math.max(c.length, ...rows.map((r) => String(r[c]).length))])
  );
  const line = (cells) => columns.map((c) => String(cells[c]).padEnd(width[c])).join('  ');
  const header = line(Object.fromEntries(columns.map((c) => [c, c])));
  const rule = columns.map((c) => '-'.repeat(width[c])).join('  ');
  return [header, rule, ...rows.map(line)].join('\n');
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (!args.serve && !args.url) throw new Error('--no-serve requires --url');
  let server = null;
  let url = args.url;
  if (!url) {
    server = await startPreview();
    url = server.url;
    process.stderr.write(`serving ${url}\n`);
  }
  const run = {
    tool: 'pipeline/perf-harness.mjs',
    version: 1,
    label: args.label || null,
    startedAt: new Date().toISOString(),
    url,
    git: gitInfo(),
    settings: { sampleSeconds: args.sample, settleSeconds: args.settle, quality: args.quality },
    host: { platform: os.platform(), arch: os.arch(), cpus: os.cpus().length, node: process.version },
    // The harness cannot emulate a GPU: on a software-rasterizer host every fps
    // number below is host-limited and says nothing about the 60 fps guardrail.
    notes: [],
    profiles: [],
  };
  try {
    for (const profile of args.profiles) {
      if (!PROFILES[profile]) throw new Error(`unknown profile ${profile}`);
      run.profiles.push(await runProfile(profile, url, args));
    }
  } finally {
    server?.stop();
  }
  const gpu = run.profiles[0]?.environment?.gpu || '';
  if (/swiftshader|llvmpipe|software/i.test(gpu)) {
    run.notes.push(
      `host GPU is a software rasterizer (${gpu}) — fps/frame-time figures are host-limited, not guardrail evidence; ` +
        'run on a GPU machine or use the manual recipe in .agents/skills/testing-sf-3d/SKILL.md'
    );
  }
  run.finishedAt = new Date().toISOString();
  await mkdir(args.out, { recursive: true });
  const stamp = run.startedAt.replace(/[:.]/g, '-');
  const file = path.join(args.out, `${args.label ? `${args.label}-` : ''}${stamp}.json`);
  await writeFile(file, `${JSON.stringify(run, null, 2)}\n`);
  console.log(table(run));
  for (const profile of run.profiles) {
    if (profile.load) {
      console.log(
        `\n${profile.profile} cold load (${profile.load.profileNetwork}): ` +
          `${profile.load.timeToTilesSeconds ?? 'timeout'} s to tiles, ` +
          `${profile.load.transferredMB} MB transferred, cells ${profile.load.cellsLoaded}/${profile.load.cellsTotal}`
      );
    }
  }
  for (const note of run.notes) console.log(`\nNOTE: ${note}`);
  console.log(`\nwrote ${file.startsWith(ROOT) ? path.relative(ROOT, file) : file}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
