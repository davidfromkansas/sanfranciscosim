#!/usr/bin/env node
// Heap attribution — what the mobile tab is actually holding.
//
// The growth probe answers "does it leak" (it does not); this answers the
// question that replaced it: why the floor is ~300 MB before the city has
// streamed anything. It loads the deployed app in a phone-shaped tab, lets it
// settle, forces a collection, takes a V8 heap snapshot, and aggregates it two
// ways:
//
//   by constructor   self bytes summed per node name — the shape of the floor
//   by owner         for the big typed arrays, the object graph path that keeps
//                    them alive, so a number turns into a subsystem to fix
//
// Nothing here depends on the GPU, so a software rasterizer only makes it slow.
//
//   node pipeline/heap-attribution.mjs --url https://sf-3d.vercel.app --settle 120
//
import { spawn } from 'node:child_process';
import { createWriteStream } from 'node:fs';
import { mkdir, mkdtemp, readFile, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const OUT_DIR = path.join(ROOT, 'artifacts', 'perf');
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

function parseArgs(argv) {
  const args = { url: null, settle: 120, profile: 'mobile', label: 'heap', chrome: process.env.CHROME_PATH || null, keep: false };
  for (let i = 0; i < argv.length; i++) {
    const next = () => argv[++i];
    const arg = argv[i];
    if (arg === '--url') args.url = next();
    else if (arg === '--settle') args.settle = Number(next());
    else if (arg === '--profile') args.profile = next();
    else if (arg === '--label') args.label = next();
    else if (arg === '--chrome') args.chrome = next();
    else if (arg === '--keep') args.keep = true;
    else throw new Error(`unknown argument ${arg}`);
  }
  if (!args.url) throw new Error('--url is required');
  return args;
}

const PROFILES = {
  desktop: { metrics: { width: 1600, height: 900, deviceScaleFactor: 1, mobile: false }, userAgent: null },
  mobile: {
    metrics: { width: 390, height: 844, deviceScaleFactor: 3, mobile: true },
    userAgent:
      'Mozilla/5.0 (Linux; Android 13; Pixel 6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Mobile Safari/537.36',
  },
};

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
    } catch { /* not up yet */ }
    if (Date.now() > deadline) throw new Error(`timed out waiting for ${url}`);
    await sleep(300);
  }
}

async function capture(args) {
  const config = PROFILES[args.profile];
  const port = await freePort();
  const userDataDir = await mkdtemp(path.join(os.tmpdir(), 'heapattr-'));
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
  ], { stdio: ['ignore', 'ignore', 'ignore'] });
  await waitForHttp(`http://127.0.0.1:${port}/json/version`, 30000);

  const version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    ws.addEventListener('open', resolve, { once: true });
    ws.addEventListener('error', () => reject(new Error('cannot attach to Chrome')), { once: true });
  });

  let nextId = 0;
  const pending = new Map();
  const snapshotFile = path.join(OUT_DIR, `${args.label}-${new Date().toISOString().replace(/[:.]/g, '-')}.heapsnapshot`);
  await mkdir(OUT_DIR, { recursive: true });
  const sink = createWriteStream(snapshotFile);
  let chunks = 0;
  ws.addEventListener('message', (event) => {
    const msg = JSON.parse(event.data);
    if (msg.method === 'HeapProfiler.addHeapSnapshotChunk') {
      sink.write(msg.params.chunk);
      if (++chunks % 500 === 0) process.stdout.write('.');
      return;
    }
    if (msg.id === undefined) return;
    const entry = pending.get(msg.id);
    if (!entry) return;
    pending.delete(msg.id);
    if (msg.error) entry.reject(new Error(`${entry.method}: ${msg.error.message}`));
    else entry.resolve(msg.result);
  });
  const send = (method, params = {}, sessionId) => {
    const id = ++nextId;
    ws.send(JSON.stringify({ id, method, params, sessionId }));
    return new Promise((resolve, reject) => pending.set(id, { resolve, reject, method }));
  };

  const { targetId } = await send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await send('Target.attachToTarget', { targetId, flatten: true });
  const at = (method, params) => send(method, params, sessionId);
  const evaluate = async (expression) => {
    const result = await at('Runtime.evaluate', { expression, returnByValue: true });
    return result.exceptionDetails ? null : result.result.value;
  };

  await at('Page.enable');
  await at('Runtime.enable');
  await at('HeapProfiler.enable');
  await at('Emulation.setDeviceMetricsOverride', { ...config.metrics, screenWidth: config.metrics.width, screenHeight: config.metrics.height });
  if (config.userAgent) {
    await at('Emulation.setUserAgentOverride', { userAgent: config.userAgent, platform: 'Linux armv8l' });
    await at('Emulation.setTouchEmulationEnabled', { enabled: true, maxTouchPoints: 5 });
  }

  console.log(`loading ${args.url} (${args.profile})…`);
  await at('Page.navigate', { url: args.url });
  const ready = Date.now() + 240000;
  while (Date.now() < ready) {
    if (await evaluate('!!(window.SF && window.SF.city)')) break;
    await sleep(2000);
  }
  console.log(`settling ${args.settle}s…`);
  await sleep(args.settle * 1000);

  const before = await evaluate(`(() => {
    const S = window.SF; const m = performance.memory;
    const safe = (read) => { try { return JSON.parse(JSON.stringify(read())); } catch { return null; } };
    return {
      heapMB: +(m.usedJSHeapSize / 1048576).toFixed(1),
      geometries: S.renderer.info.memory.geometries,
      textures: S.renderer.info.memory.textures,
      city: safe(() => S.city.stats),
      quality: safe(() => S.governor.state().tier),
    };
  })()`);
  console.log('state at snapshot:', JSON.stringify(before));

  await evaluate('window.gc && window.gc()');
  await sleep(2000);
  console.log('taking heap snapshot');
  await at('HeapProfiler.takeHeapSnapshot', { reportProgress: false, captureNumericValue: false });
  await new Promise((resolve) => sink.end(resolve));
  console.log(`\nsnapshot written to ${path.relative(ROOT, snapshotFile)}`);

  await send('Target.closeTarget', { targetId });
  ws.close();
  chrome.kill('SIGTERM');
  return { snapshotFile, before };
}

// --- snapshot aggregation -------------------------------------------------

function analyse(snapshot) {
  const meta = snapshot.snapshot.meta;
  const nodeFields = meta.node_fields;
  const nodeTypes = meta.node_types[0];
  const edgeFields = meta.edge_fields;
  const edgeTypes = meta.edge_types[0];
  const nodes = snapshot.nodes;
  const edges = snapshot.edges;
  const strings = snapshot.strings;
  const nodeLength = nodeFields.length;
  const edgeLength = edgeFields.length;
  const typeOffset = nodeFields.indexOf('type');
  const nameOffset = nodeFields.indexOf('name');
  const sizeOffset = nodeFields.indexOf('self_size');
  const edgeCountOffset = nodeFields.indexOf('edge_count');
  const edgeTypeOffset = edgeFields.indexOf('type');
  const edgeNameOffset = edgeFields.indexOf('name_or_index');
  const edgeToOffset = edgeFields.indexOf('to_node');
  const nodeCount = nodes.length / nodeLength;

  const label = (index) => `${nodeTypes[nodes[index * nodeLength + typeOffset]]} ${strings[nodes[index * nodeLength + nameOffset]]}`.trim();
  const selfSize = (index) => nodes[index * nodeLength + sizeOffset];

  // Edge offsets per node, so the graph can be walked without a library.
  const firstEdge = new Uint32Array(nodeCount + 1);
  for (let i = 0, cursor = 0; i < nodeCount; i++) {
    firstEdge[i] = cursor;
    cursor += nodes[i * nodeLength + edgeCountOffset];
    firstEdge[i + 1] = cursor;
  }

  // Retainers: for the biggest arrays, "who points at this" is the answer.
  const retainerOf = new Int32Array(nodeCount).fill(-1);
  const retainerEdge = new Int32Array(nodeCount).fill(-1);
  for (let from = 0; from < nodeCount; from++) {
    for (let e = firstEdge[from]; e < firstEdge[from + 1]; e++) {
      const to = edges[e * edgeLength + edgeToOffset] / nodeLength;
      if (to === 0 || retainerOf[to] !== -1) continue;
      retainerOf[to] = from;
      retainerEdge[to] = e;
    }
  }

  const byName = new Map();
  let total = 0;
  for (let i = 0; i < nodeCount; i++) {
    const size = selfSize(i);
    total += size;
    const key = label(i);
    const entry = byName.get(key) || { bytes: 0, count: 0 };
    entry.bytes += size;
    entry.count++;
    byName.set(key, entry);
  }

  const edgeLabel = (e) => {
    const type = edgeTypes[edges[e * edgeLength + edgeTypeOffset]];
    const raw = edges[e * edgeLength + edgeNameOffset];
    return type === 'element' || type === 'hidden' ? `[${raw}]` : strings[raw] || '?';
  };
  const pathOf = (index) => {
    const parts = [];
    let cursor = index;
    for (let depth = 0; depth < 12 && cursor > 0; depth++) {
      const parent = retainerOf[cursor];
      if (parent < 0) break;
      parts.push(`${edgeLabel(retainerEdge[cursor])} in ${label(parent)}`);
      cursor = parent;
    }
    return parts;
  };

  const biggest = [];
  for (let i = 0; i < nodeCount; i++) if (selfSize(i) > 262144) biggest.push(i);
  biggest.sort((a, b) => selfSize(b) - selfSize(a));

  return {
    totalMB: +(total / 1048576).toFixed(1),
    byConstructor: [...byName.entries()]
      .map(([name, v]) => ({ name, mb: +(v.bytes / 1048576).toFixed(1), count: v.count }))
      .sort((a, b) => b.mb - a.mb)
      .slice(0, 40),
    largest: biggest.slice(0, 40).map((i) => ({ node: label(i), mb: +(selfSize(i) / 1048576).toFixed(2), path: pathOf(i) })),
  };
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const { snapshotFile, before } = await capture(args);
  console.log('parsing snapshot…');
  const snapshot = JSON.parse(await readFile(snapshotFile, 'utf8'));
  const report = analyse(snapshot);
  const reportFile = snapshotFile.replace('.heapsnapshot', '.analysis.json');
  await writeFile(reportFile, JSON.stringify({ url: args.url, profile: args.profile, state: before, ...report }, null, 2));

  console.log(`\nheap total ${report.totalMB} MB (self sizes)\n`);
  console.log('top constructors:');
  for (const row of report.byConstructor.slice(0, 20)) {
    console.log(`  ${String(row.mb).padStart(8)} MB  ${String(row.count).padStart(7)}×  ${row.name}`);
  }
  console.log('\nlargest single allocations and what holds them:');
  for (const row of report.largest.slice(0, 15)) {
    console.log(`  ${String(row.mb).padStart(7)} MB  ${row.node}`);
    console.log(`            ← ${row.path.slice(0, 4).join(' ← ')}`);
  }
  console.log(`\nwrote ${path.relative(ROOT, reportFile)}`);
}

main().catch((error) => {
  console.error(error);
  process.exit(1);
});
