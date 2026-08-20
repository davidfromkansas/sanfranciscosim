// Stage-5 local QA for pier-7, INTEGRATION-PROMPT.md Steps 5 and 6.
//
// Drives the BUILT app (app/dist) in real headless Chrome over CDP rather than
// the in-editor Browser pane: parallel landmark sessions hold all five
// preview_start slots, and a hidden pane throttles requestAnimationFrame to
// nothing, which makes a perfectly healthy streaming landmark look broken.
// rAF runs continuously here, so the boot curtain lifts, assets.update() runs
// itself, and Page.captureScreenshot returns real pixels.
//
//   node artifacts/pier-7/qa_local.mjs [--drill]
//
// --drill serves a real 404 for the landmark GLB instead of moving the file,
// which is both honest and reversible (Vite's dev server answers a missing
// public path with index.html and HTTP 200, so the usual rename trick cannot
// produce a fetch failure at all).
//
// Zero dependencies; Node 22 (native fetch + WebSocket).

import { spawn } from 'node:child_process';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { mkdtemp, writeFile } from 'node:fs/promises';
import http from 'node:http';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const DIST = path.resolve(HERE, '../../app/dist');
const SHOTS = path.join(HERE, 'qa');
const DRILL = process.argv.includes('--drill');

const LON = -122.3955159;
const LAT = 37.7994429;
const SLUG = 'pier-7';
const CAMERA = { distance: 420, yaw: 215, pitch: 20 }; // the registry preset
const GLB_PATH = `/sf-assets/landmarks/${SLUG}.glb`;

const MIME = {
  '.html': 'text/html', '.js': 'text/javascript', '.css': 'text/css',
  '.json': 'application/json', '.glb': 'model/gltf-binary', '.bin': 'application/octet-stream',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml',
  '.woff2': 'font/woff2', '.ttf': 'font/ttf', '.ico': 'image/x-icon',
};

const freePort = () =>
  new Promise((resolve) => {
    const s = net.createServer();
    s.listen(0, () => { const { port } = s.address(); s.close(() => resolve(port)); });
  });

function serveDist(port) {
  const server = http.createServer((req, res) => {
    const url = decodeURIComponent(req.url.split('?')[0]);
    if (DRILL && url === GLB_PATH) { res.writeHead(404); res.end('gone'); return; }
    let file = path.join(DIST, url);
    if (!existsSync(file) || statSync(file).isDirectory()) {
      // the raw .bin sits beside the .bin.gz, so a dumb file server is enough
      if (existsSync(file + '.gz')) { file += '.gz'; }
      else { file = path.join(DIST, 'index.html'); }
    }
    if (!existsSync(file)) { res.writeHead(404); res.end('nope'); return; }
    const headers = { 'Content-Type': MIME[path.extname(file.replace(/\.gz$/, ''))] || 'application/octet-stream' };
    if (file.endsWith('.gz')) headers['Content-Encoding'] = 'gzip';
    res.writeHead(200, headers);
    createReadStream(file).pipe(res);
  });
  return new Promise((r) => server.listen(port, () => r(server)));
}

function findChrome() {
  for (const c of [process.env.CHROME_PATH, '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                   '/usr/bin/google-chrome', '/usr/bin/chromium'].filter(Boolean)) {
    if (existsSync(c)) return c;
  }
  throw new Error('no Chrome binary found — set CHROME_PATH');
}

async function main() {
  const httpPort = await freePort();
  const cdpPort = await freePort();
  const server = await serveDist(httpPort);
  const profile = await mkdtemp(path.join(os.tmpdir(), 'qaPier7-'));
  const chrome = spawn(findChrome(), [
    `--remote-debugging-port=${cdpPort}`, `--user-data-dir=${profile}`,
    '--no-first-run', '--no-default-browser-check', '--no-sandbox', '--headless=new',
    '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
    '--disable-backgrounding-occluded-windows',
    '--use-angle=swiftshader', '--enable-unsafe-swiftshader',
    '--window-size=1600,900',
  ], { stdio: 'ignore' });

  let version;
  for (let i = 0; i < 120; i++) {
    try { version = await (await fetch(`http://127.0.0.1:${cdpPort}/json/version`)).json(); break; }
    catch { await new Promise((r) => setTimeout(r, 300)); }
  }
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

  let nextId = 1, sessionId = null;
  const pending = new Map();
  const console_ = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) {
      const { resolve, reject } = pending.get(m.id); pending.delete(m.id);
      m.error ? reject(new Error(m.error.message)) : resolve(m.result);
    } else if (m.method === 'Runtime.consoleAPICalled') {
      console_.push(m.params.args.map((a) => a.value ?? a.description ?? '').join(' '));
    } else if (m.method === 'Runtime.exceptionThrown') {
      console_.push('EXCEPTION ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
    }
  };
  const send = (method, params = {}, inSession = true) =>
    new Promise((resolve, reject) => {
      const id = nextId++; pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params, sessionId: inSession ? sessionId : undefined }));
    });

  const { targetId } = await send('Target.createTarget', { url: 'about:blank' }, false);
  ({ sessionId } = await send('Target.attachToTarget', { targetId, flatten: true }, false));
  await send('Runtime.enable');
  await send('Page.enable');
  // The persistent-profile cache will happily serve a stale GLB across a whole
  // rebuild cycle and make a fixed asset look unchanged. Disable it every run.
  await send('Network.enable');
  await send('Network.setCacheDisabled', { cacheDisabled: true });
  await send('Page.navigate', { url: `http://127.0.0.1:${httpPort}/` });

  const evaluate = async (expression) => {
    const { result, exceptionDetails } = await send('Runtime.evaluate', {
      expression, awaitPromise: true, returnByValue: true,
    });
    if (exceptionDetails) throw new Error(exceptionDetails.text + ' ' + (exceptionDetails.exception?.description || ''));
    return result.value;
  };
  const shot = async (name) => {
    const { data } = await send('Page.captureScreenshot', { format: 'png' });
    await writeFile(path.join(SHOTS, `${name}.png`), Buffer.from(data, 'base64'));
    return `${name}.png`;
  };
  const until = async (label, expr, ms = 600000) => {
    const t0 = Date.now(); let last;
    for (;;) {
      last = await evaluate(expr).catch(() => null);
      if (last) return last;
      if (Date.now() - t0 > ms) throw new Error(`${label} timed out (last ${JSON.stringify(last)})`);
      await new Promise((r) => setTimeout(r, 700));
    }
  };

  const results = [];
  const check = (name, ok, detail) => {
    results.push({ name, ok: Boolean(ok), detail });
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${name} — ${detail}`);
  };

  // Gate on the app EXISTING, never on a fixed sleep: under load a goTo fired
  // too early throws `SF is not defined` into a swallowed catch, the camera never
  // moves, and a landmark 2.5 km away is correctly reported out of range — which
  // reads exactly like a broken loadRadius or a missing asset.
  await until('boot', 'window.SF && window.SF.assets && window.SF.goTo ? true : null');
  await until('manifest', 'window.SF.assets.stats().entries > 0 ? true : null');
  console.log('  entries:', JSON.stringify(await evaluate('window.SF.assets.stats()')));
  // The app throttles asset placement to protect frame rate, so under contention
  // the camera can sit on the anchor with the entry still `far`. Pump the scan.
  await evaluate(`window.__pump = window.__pump || setInterval(
    () => { try { window.SF.assets.update(window.SF.camera.position, 0.4); } catch (e) {} }, 250)`);

  // SF.goTo takes DEGREES; rig.set multiplies by DEG internally.
  await evaluate(`window.SF.goTo(${LON}, ${LAT}, ${CAMERA.distance}, ${CAMERA.yaw}, ${CAMERA.pitch})`);
  // Wait for THIS landmark, not merely for "some landmark is live": the 18
  // resident entries (bridges and skyline pieces) all merge during boot and
  // satisfy `live > 0` long before the streaming scan reaches a 2.5 km entry.
  // Polling the aggregate stats instead is what makes a healthy streamed asset
  // look like a broken loadRadius.
  const stats = await until(
    'landmark streamed in',
    DRILL
      ? `(() => { const s = window.SF.assets.stats(); return s.failed > 0 || s.live > 20 ? s : null; })()`
      : `(() => (window.SF.assets.placed.has('pier-7') && window.SF.assets.stats().fading === 0)
             ? window.SF.assets.stats() : null)()`,
    180000
  );
  console.log('  stats:', JSON.stringify(stats));
  await new Promise((r) => setTimeout(r, 3000));

  const mergeLine = console_.filter((l) => l.includes(`sf-assets: ${SLUG}`)).join(' | ');
  const scale = Number((mergeLine.match(/uniform x([0-9.]+)/) || [])[1]);
  check('manifest entry loads', Boolean(mergeLine) || DRILL, mergeLine || '(no merge line)');
  check('uniform scale ~ 1.0', DRILL || (scale > 0.99 && scale < 1.01), DRILL ? 'n/a in drill' : `x${scale}`);

  // SF.pick() raycasts the whole scene and throws on the landmark BatchedMesh
  // (null position attribute on the reserved buffer), so read the rig state and
  // the landmark's own placement record instead.
  const placed = await evaluate(`(() => ({
    stats: window.SF.assets.stats(),
    rig: { x: Math.round(window.SF.rig.state.pivot.x), z: Math.round(window.SF.rig.state.pivot.z),
           yawDeg: Math.round(window.SF.rig.state.yaw * 180 / Math.PI),
           pitchDeg: Math.round(window.SF.rig.state.pitch * 180 / Math.PI),
           distance: Math.round(window.SF.rig.state.distance) },
    placedIds: [...window.SF.assets.placed.keys()],
    hasPier7: window.SF.assets.placed.has('pier-7'),
    placePier7: window.SF.assets.placed.get('pier-7') ? JSON.parse(JSON.stringify({ log: window.SF.assets.placed.get('pier-7').log, scale: window.SF.assets.placed.get('pier-7').scale })) : null,
  }))()`);
  console.log('  rig:', JSON.stringify(placed.rig));
  console.log('  placedPier7:', placed.hasPier7, JSON.stringify(placed.placePier7));
  console.log('  placedIds:', placed.placedIds.join(','));
  console.log('  console lines:', console_.length);
  for (const l of console_) if (/340|warn|fail|error|keeping/i.test(l)) console.log('    >', l.slice(0, 200));

  const draws = await evaluate(`(async () => {
    const info = window.SF.renderer.info;
    const raf = () => new Promise((res) => requestAnimationFrame(res));
    info.autoReset = false; await raf(); info.reset();
    for (let i = 0; i < 30; i++) await raf();
    const calls = info.render.calls / 30; info.autoReset = true;
    return Math.round(calls);
  })()`);
  check('draw calls under 300 at the landmark', draws > 5 && draws < 300, `avg ${draws}/frame`);

  // Pier 3 is the first over-water landmark that is not a bridge. placeGeneric
  // seats generic landmarks at max(0, sampleElevation(x, z)), and the anchor is
  // the pier polygon's centroid, which is open bay — so the origin must land on
  // the water plane at EXACTLY y = 0. A non-zero seat means the anchor drifted
  // onto the seawall, and the fix is to move the anchor back, never to shim the
  // model.
  if (!DRILL) {
    const seat = await evaluate(`(() => {
      const p = window.SF.assets.placed.get('pier-7');
      if (!p || !p.matrix) return null;
      const e = p.matrix.elements;
      return { x: +e[12].toFixed(2), y: +e[13].toFixed(3), z: +e[14].toFixed(2), scale: +e[0].toFixed(4) };
    })()`);
    console.log('  seat:', JSON.stringify(seat));
    check('seated on the water plane (y = 0)', seat && Math.abs(seat.y) < 0.001,
      seat ? `y=${seat.y} scale=${seat.scale}` : '(no placement record)');
  }

  // The app boots on the live wall clock, so a "day" screenshot taken as-is is
  // whatever time it happens to be. SF.setClock(iso) pins it; setTime() is
  // deprecated and warns.
  await evaluate(`window.SF.setClock('2026-08-19T14:30:00-07:00')`);
  await new Promise((r) => setTimeout(r, 2500));
  await shot(DRILL ? 'drill-day' : 'day');

  // night: sweep past dusk
  await evaluate(`window.SF.setClock('2026-08-19T21:45:00-07:00')`);
  await new Promise((r) => setTimeout(r, 2500));
  await shot(DRILL ? 'drill-night' : 'night');

  // wide shot
  await evaluate(`window.SF.setClock('2026-08-19T14:30:00-07:00')`);
  await evaluate(`window.SF.goTo(${LON}, ${LAT}, 1400, ${CAMERA.yaw}, 34)`);
  await new Promise((r) => setTimeout(r, 4000));
  await shot(DRILL ? 'drill-wide' : 'wide');

  const warnings = console_.filter((l) => /sf-assets:/.test(l) && /keeping the code-built|failed|error/i.test(l));
  if (DRILL) {
    const s = await evaluate('window.SF.assets.stats()');
    check('app still boots with the GLB missing', s.entries > 0, JSON.stringify(s));
    // `failed: 0` is meaningless unless the loader actually reached for the file:
    // a drill that never got the camera near the anchor reports a plausible-looking
    // pass while measuring nothing. Refuse to call it until failed > 0.
    check('the loader actually attempted the GLB', s.failed > 0, JSON.stringify(s));
    // Step 6 of INTEGRATION-PROMPT quotes the RESIDENT path's wording
    // ("... — keeping the code-built landmark"). Every ordinary landmark now ships
    // with a loadRadius, i.e. streamed, and scan() deliberately does not use the
    // single-shot warn(): expect `sf-assets: pier-7 failed to load (...)` with no
    // "keeping" suffix. Match on the id, not on the prompt's wording.
    check('exactly one fallback warning', warnings.length === 1, warnings.join(' | ') || '(none)');
  } else {
    check('no asset warnings', warnings.length === 0, warnings.join(' | ') || '(none)');
  }

  await writeFile(path.join(SHOTS, DRILL ? 'drill.json' : 'qa.json'),
    JSON.stringify({ results, stats, placed, draws, mergeLine, console: console_ }, null, 2) + '\n');

  ws.close(); chrome.kill(); server.close();
  console.log('\n' + results.map((r) => `${r.ok ? 'PASS' : 'FAIL'} ${r.name}`).join('\n'));
  process.exit(results.every((r) => r.ok) ? 0 : 1);
}

await main();
