// Stage-5 local QA for 2-folsom, INTEGRATION-PROMPT.md Steps 5 and 6.
//
// Adapted from artifacts/fulton-plaza/qa_local.mjs, which carries the hard-won
// notes about hidden panes, the streaming pump and the drill's warning text.
// The asset-specific checks here exist because this is the tallest and widest
// bespoke landmark in the set (88.0 m over a whole 84.31 x 77.14 m block):
//
//   * the THREE-MASS STEP-UP must survive the app's merge. In Blender the base,
//     the brick superstructure and the limestone tower are separate solids; in
//     the app they are one BatchedMesh geometry with baked vertex colours, and
//     the only place the stack can be confirmed as a silhouette is here.
//   * the exclusion must have taken BOTH source rings. This footprint is traced
//     by DataSF and by Overture, so a radius that drops one and not the other
//     leaves a full-height procedural block inside an 88 m asset — and it is
//     tall enough to poke out of the top.
//   * the shared landmark BatchedMesh is 91.8% full with this entry in it. If
//     the body reserve overflows, addGeometry throws and ONE ARBITRARY landmark
//     silently falls back per reload — so `placed` is checked for this id
//     specifically, never for "some landmark loaded".
//
// Drives the BUILT app (app/dist) in real headless Chrome over CDP rather than
// the in-editor Browser pane: parallel landmark sessions hold all five
// preview_start slots, and a hidden pane throttles requestAnimationFrame to
// nothing, which makes a perfectly healthy streaming landmark look broken.
// rAF runs continuously here, so the boot curtain lifts, assets.update() runs
// itself, and Page.captureScreenshot returns real pixels.
//
//   node artifacts/2-folsom/qa_local.mjs [--drill]
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

// The registry lon/lat and the manifest anchor are the SAME point here (the
// DataSF footprint's OBB centre), so there is no discrepancy to reconcile.
const LON = -122.390975;
const LAT = 37.790787;
const SLUG = '2-folsom';
const CAMERA = { distance: 300, yaw: 135, pitch: 30 }; // the registry preset
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

// Median luminance of named rectangles of a PNG, as fractions of width/height.
// Shelled out to python3 + Pillow, which this repo already requires for
// make_contact_sheet.py, rather than pulling a PNG decoder into a zero-dependency
// harness.
function measurePng(file, regions) {
  const py = [
    'import sys, json',
    'from PIL import Image',
    'im = Image.open(sys.argv[1]).convert("RGB")',
    'W, H = im.size',
    'regions = json.loads(sys.argv[2])',
    'out = {}',
    'for name, (x0, y0, x1, y1) in regions.items():',
    '    c = im.crop((int(W*x0), int(H*y0), int(W*x1), int(H*y1)))',
    '    lum = sorted(0.2126*r + 0.7152*g + 0.0722*b for r, g, b in c.getdata())',
    '    out[name] = round(lum[len(lum)//2])',
    'print(json.dumps(out))',
  ].join('\n');
  return new Promise((resolve, reject) => {
    const p = spawn('python3', ['-c', py, file, JSON.stringify(regions)]);
    let out = '';
    p.stdout.on('data', (d) => { out += d; });
    p.on('close', (code) => (code === 0 ? resolve(JSON.parse(out)) : reject(new Error('measurePng failed'))));
  });
}

async function main() {
  const httpPort = await freePort();
  const cdpPort = await freePort();
  const server = await serveDist(httpPort);
  const profile = await mkdtemp(path.join(os.tmpdir(), 'qa2folsom-'));
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
  // 120 s is not enough on this machine. David runs a dozen landmark sessions at
  // once and the load average hits 400+; the boot that takes 8 s on an idle box
  // takes minutes under SwiftShader when it does. Timing out there reports a
  // broken app rather than a busy one.
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

  await until('boot', 'window.SF && window.SF.assets ? true : null');
  await until('manifest', 'window.SF.assets.stats().entries > 0 ? true : null');
  console.log('  entries:', JSON.stringify(await evaluate('window.SF.assets.stats()')));

  // SF.goTo takes DEGREES; rig.set multiplies by DEG internally.
  await evaluate(`window.SF.goTo(${LON}, ${LAT}, ${CAMERA.distance}, ${CAMERA.yaw}, ${CAMERA.pitch})`);

  // Pump the streaming scan with a real delta. assets.update() gates its scan on
  // dt and the app throttles placement to protect frame rate, so on a machine at
  // load 400+ the camera can sit on the anchor for ten minutes with the entry
  // still `far`. That reads as a broken loadRadius and is nothing of the kind.
  await evaluate(`(() => {
    if (window.__qaPump) return true;
    window.__qaPump = setInterval(() => {
      try { window.SF.assets.update(window.SF.camera.position, 0.4); } catch {}
    }, 250);
    return true;
  })()`);
  // Wait for THIS landmark, not merely for "some landmark is live": the 18
  // resident entries (bridges and skyline pieces) all merge during boot and
  // satisfy `live > 0` long before the streaming scan reaches a 2.5 km entry.
  // Polling the aggregate stats instead is what makes a healthy streamed asset
  // look like a broken loadRadius.
  const stats = await until(
    'landmark streamed in',
    DRILL
      ? `(() => { const s = window.SF.assets.stats(); return s.failed > 0 || s.live > 20 ? s : null; })()`
      : `(() => (window.SF.assets.placed.has('2Folsom') && window.SF.assets.stats().fading === 0)
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
    hasAsset: window.SF.assets.placed.has('2Folsom'),
    placeAsset: window.SF.assets.placed.get('2Folsom') ? JSON.parse(JSON.stringify({ log: window.SF.assets.placed.get('2Folsom').log, scale: window.SF.assets.placed.get('2Folsom').scale })) : null,
  }))()`);
  console.log('  rig:', JSON.stringify(placed.rig));
  console.log('  placedAsset:', placed.hasAsset, JSON.stringify(placed.placeAsset));
  console.log('  placedIds:', placed.placedIds.join(','));
  console.log('  console lines:', console_.length);
  for (const l of console_) if (/folsom|warn|fail|error|keeping/i.test(l)) console.log('    >', l.slice(0, 200));

  const draws = await evaluate(`(async () => {
    const info = window.SF.renderer.info;
    const raf = () => new Promise((res) => requestAnimationFrame(res));
    info.autoReset = false; await raf(); info.reset();
    for (let i = 0; i < 30; i++) await raf();
    const calls = info.render.calls / 30; info.autoReset = true;
    return Math.round(calls);
  })()`);
  check('draw calls under 300 at the landmark', draws > 5 && draws < 300, `avg ${draws}/frame`);

  // The app boots on the live wall clock, so a "day" screenshot taken as-is is
  // whatever time it happens to be. SF.setClock(iso) pins it; setTime() is
  // deprecated and warns.
  await evaluate(`window.SF.setClock('2026-08-17T14:30:00-07:00')`);
  await new Promise((r) => setTimeout(r, 2500));
  await shot(DRILL ? 'drill-day' : 'day');

  // night: sweep past dusk
  await evaluate(`window.SF.setClock('2026-08-17T21:45:00-07:00')`);
  await new Promise((r) => setTimeout(r, 2500));
  await shot(DRILL ? 'drill-night' : 'night');

  // Wide shot: the healthy run only. In the drill the 900 m pull-back forces a
  // district's worth of tiles through SwiftShader on a machine already running a
  // dozen landmark sessions, and it wedged for 25 minutes without returning. The
  // drill's evidence is the two console assertions below plus drill-day/night —
  // the wide frame proves nothing extra about a fallback.
  if (!DRILL) {
    await evaluate(`window.SF.setClock('2026-08-17T14:30:00-07:00')`);
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 900, ${CAMERA.yaw}, 34)`);
    await new Promise((r) => setTimeout(r, 4000));
    await shot('wide');

    // Three building checks. First the plan view: the exclusion has to have
    // taken BOTH the DataSF ring and the Overture ring, so anything procedural
    // still standing on this block shows here as a second roof.
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 320, 135, 78)`);
    await new Promise((r) => setTimeout(r, 3000));
    await shot('plan');

    // Then eye level from the Embarcadero (bearing 45 = app yaw 135) and from
    // Spear (bearing 225 = app yaw -45): a baked block poking through the base,
    // a floating or buried plinth, or a z-fighting twin all read at 12 deg.
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 210, 135, 12)`);
    await new Promise((r) => setTimeout(r, 3000));
    await shot('low-from-embarcadero');
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 210, -45, 12)`);
    await new Promise((r) => setTimeout(r, 3000));
    await shot('low-from-spear');

    // WHY THERE IS NO LOW-PITCH SILHOUETTE SHOT HERE.
    // The first version of this harness tried to prove the three-mass step-up
    // from a 10 deg view, by finding the topmost non-sky row in three columns.
    // It returned "no building in any column" and the screenshot was identical
    // to the 42 deg one. The cause is not the asset: DIORAMA mode HARD-LOCKS
    // the pitch. camera.js line 50 sets DIORAMA.pitch = 42 deg and its update()
    // reassigns `state.pitch = DIORAMA.pitch` EVERY FRAME while diorama is on,
    // which by AGENTS rule 1 is always. So SF.goTo(lon, lat, d, yaw, pitch)
    // sets the pitch and the next frame takes it straight back, and no
    // sky-behind-the-tower view exists to measure. Judge the stack from the
    // aerial screenshots, which is what the style bible asks for anyway.
    //
    // What CAN be measured at 42 deg are the two things that would actually be
    // broken if the integration were wrong, and both are below.

    // 1. Placement. The merge line reports the world position the loader put
    //    the asset at; it must equal the anchor pushed through the app's own
    //    tangent projection. This is the orientation/anchor check in numbers
    //    rather than in pixels — a transposed or mis-projected anchor lands
    //    tens of metres out and shows here immediately.
    // `window.SF.data` is not on the debug surface, so the projection is done
    // here instead — it is AGENTS.md's single documented tangent projection,
    // centred on lon -122.4375 / lat 37.77, and re-deriving it anywhere else is
    // exactly what that rule forbids in APP code, not in a test that checks it.
    const LON0 = -122.4375, LAT0 = 37.77;
    const wantX = (LON - LON0) * 111320 * Math.cos((LAT0 * Math.PI) / 180);
    const wantZ = -(LAT - LAT0) * 110540;
    const got = (mergeLine.match(/at (-?\d+), (-?\d+)/) || []).slice(1).map(Number);
    check('placed at the projected anchor',
          got.length === 2 && Math.abs(got[0] - wantX) < 2 && Math.abs(got[1] - wantZ) < 2,
          `loader ${got.join(', ')} vs projection ${Math.round(wantX)}, ${Math.round(wantZ)}`);

    // 2. The night hero. The atrium skylight is the whole night identity of
    //    this asset, and a glow shell that failed to reach the unlit layer
    //    reads as an ordinary dark roof panel. Measure it: at night the
    //    skylight must be substantially brighter than the terrace beside it.
    await evaluate(`window.SF.setClock('2026-08-17T21:45:00-07:00')`);
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, ${CAMERA.distance}, ${CAMERA.yaw}, ${CAMERA.pitch})`);
    await new Promise((r) => setTimeout(r, 3500));
    await shot('night-skylight');
    // MEASURE THE SCREENSHOT, NOT THE CANVAS. The obvious version of this check
    // — drawImage(SF.renderer.domElement) into a 2D canvas and read the pixels
    // back — returns ALL ZEROES here, for both the lit skylight and the dark
    // terrace beside it. The renderer runs without preserveDrawingBuffer, so by
    // the time a Runtime.evaluate runs, the drawing buffer for the presented
    // frame is already gone and the copy is empty. It fails identically on a
    // perfectly lit asset and on a black one, which is the worst kind of check.
    // Page.captureScreenshot samples at composite time and does not have the
    // problem, so the PNG that was just written is the ground truth.
    const glow = await measurePng(path.join(SHOTS, 'night-skylight.png'), {
      skylight: [0.41, 0.31, 0.52, 0.46],
      terrace: [0.57, 0.33, 0.68, 0.46],
    });
    console.log('  night luminance:', JSON.stringify(glow));
    check('atrium skylight is the night hero',
          glow.skylight > glow.terrace + 12,
          `skylight ${glow.skylight} vs terrace ${glow.terrace} (median luminance)`);
    await evaluate(`window.SF.setClock('2026-08-17T14:30:00-07:00')`);
  }

  // NOTE on what this asset's fallback warning actually says. INTEGRATION-PROMPT
  // Step 6 tells you to expect one `... — keeping the code-built landmark` line,
  // and that is the RESIDENT path (assets.js `warn()`, line 434). A STREAMED
  // entry — anything with a loadRadius, which is this one — fails through
  // `scan()` at line 560 instead, which deliberately does not use the
  // single-shot `warn()` and emits `sf-assets: <id> failed to load (...)` with
  // no "keeping" suffix. It is still exactly once: `place()` sets
  // status = 'failed', and no branch in scan() matches 'failed', so it can never
  // be retried or re-warned. Match on the id, not on the prompt's wording.
  const warnings = console_.filter((l) => /sf-assets:/.test(l) && /keeping the code-built|failed|error/i.test(l));
  if (DRILL) {
    const s = await evaluate('window.SF.assets.stats()');
    check('app still boots with the GLB missing', s.entries > 0, JSON.stringify(s));
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
