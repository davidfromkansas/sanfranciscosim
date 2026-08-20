// Stage-5 local QA for fulton-plaza, INTEGRATION-PROMPT.md Steps 5 and 6.
//
// Adapted from artifacts/434-brannan/qa_local.mjs, which carries the hard-won
// notes about hidden panes, the streaming pump and the drill's warning text.
// Three checks are specific to this asset, and all three exist because it is a
// GROUND-PLANE landmark rather than a building:
//
//   * the deck must HIDE the baked street. exclusionZones() clears buildings,
//     not streets, and a DataSF centreline still bakes down the middle of this
//     plaza — so the two low shots at the Larkin and Hyde ends are the evidence
//     that the +0.55 m deck clears the 0.35 m kerb along the whole block.
//   * the deck must SIT on the terrain at both ends. The plaza falls 2.37 m and
//     placeGeneric() seats from one sample, so a drape error shows as a buried
//     west end or a floating east end — invisible in every Blender render.
//   * the asphalt must not read BLACK. Toy_roofd-dark values come back
//     rgb(9,9,12) in the diorama; this asset's 6f7076 was chosen against that
//     measurement and the app is the only place it can be confirmed.
//
// Drives the BUILT app (app/dist) in real headless Chrome over CDP rather than
// the in-editor Browser pane: parallel landmark sessions hold all five
// preview_start slots, and a hidden pane throttles requestAnimationFrame to
// nothing, which makes a perfectly healthy streaming landmark look broken.
// rAF runs continuously here, so the boot curtain lifts, assets.update() runs
// itself, and Page.captureScreenshot returns real pixels.
//
//   node artifacts/fulton-plaza/qa_local.mjs [--drill]
//
// --drill serves a real 404 for the landmark GLB instead of moving the file,
// which is both honest and reversible (Vite's dev server answers a missing
// public path with index.html and HTTP 200, so the usual rename trick cannot
// produce a fetch failure at all).
//
// Zero dependencies; Node 22 (native fetch + WebSocket).

import { spawn } from 'node:child_process';
import { createReadStream, existsSync, readFileSync, statSync } from 'node:fs';
import { inflateSync } from 'node:zlib';
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
// --quick: boot, stream the landmark in, take the day and night shots, stop.
// The draw-call block runs 30 real animation frames and the full shot sequence
// runs six; under SwiftShader on a machine at load 300+ (David runs a dozen
// landmark sessions at once) that is 45 minutes for evidence a single frame
// already carries. Use it to re-check a visual change, not to replace the run.
const QUICK = process.argv.includes('--quick');

// The REGISTRY lon/lat (the right-of-way's OBB centre), not the manifest anchor
// — this is the camera preset's target, and the two differ by 1.2 m here.
const LON = -122.4159189;
const LAT = 37.7796904;
const SLUG = 'fulton-plaza';
const CAMERA = { distance: 340, yaw: 99, pitch: 26 }; // the registry preset
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

// Minimal PNG reader: enough to median-sample a region of our own screenshots.
// zlib is in the standard library, so this stays dependency-free.
function lumaFromPng(file, ...windows) {
  const buf = readFileSync(file);
  let off = 8;
  let w = 0, h = 0, bitDepth = 0, colorType = 0;
  const idat = [];
  while (off < buf.length) {
    const len = buf.readUInt32BE(off);
    const type = buf.toString('ascii', off + 4, off + 8);
    const data = buf.subarray(off + 8, off + 8 + len);
    if (type === 'IHDR') {
      w = data.readUInt32BE(0); h = data.readUInt32BE(4);
      bitDepth = data[8]; colorType = data[9];
    } else if (type === 'IDAT') idat.push(data);
    else if (type === 'IEND') break;
    off += 12 + len;
  }
  if (bitDepth !== 8 || (colorType !== 6 && colorType !== 2)) {
    throw new Error(`unsupported PNG ${bitDepth}/${colorType}`);
  }
  const ch = colorType === 6 ? 4 : 3;
  const raw = inflateSync(Buffer.concat(idat));
  const stride = w * ch;
  const out = Buffer.alloc(h * stride);
  let p = 0;
  for (let y = 0; y < h; y++) {
    const filter = raw[p++];
    const line = raw.subarray(p, p + stride); p += stride;
    const cur = out.subarray(y * stride, (y + 1) * stride);
    const prev = y ? out.subarray((y - 1) * stride, y * stride) : Buffer.alloc(stride);
    for (let x = 0; x < stride; x++) {
      const a = x >= ch ? cur[x - ch] : 0, b = prev[x], c = x >= ch ? prev[x - ch] : 0;
      let v = line[x];
      if (filter === 1) v += a;
      else if (filter === 2) v += b;
      else if (filter === 3) v += (a + b) >> 1;
      else if (filter === 4) {
        const pa = Math.abs(b - c), pb = Math.abs(a - c), pc = Math.abs(a + b - 2 * c);
        v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c;
      }
      cur[x] = v & 255;
    }
  }
  const lum = [];
  for (let k = 0; k < windows.length; k += 4) {
    const [fx0, fx1, fy0, fy1] = windows.slice(k, k + 4);
    for (let y = Math.round(h * fy0); y < Math.round(h * fy1); y++) {
      for (let x = Math.round(w * fx0); x < Math.round(w * fx1); x++) {
        const i = y * stride + x * ch;
        lum.push(0.2126 * out[i] + 0.7152 * out[i + 1] + 0.0722 * out[i + 2]);
      }
    }
  }
  lum.sort((a, b) => a - b);
  return { n: lum.length, median: Math.round(lum[lum.length >> 1]),
           p10: Math.round(lum[Math.floor(lum.length * 0.1)]),
           p90: Math.round(lum[Math.floor(lum.length * 0.9)]) };
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
  const profile = await mkdtemp(path.join(os.tmpdir(), 'qafulton-'));
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
      : `(() => (window.SF.assets.placed.has('fultonPlaza') && window.SF.assets.stats().fading === 0)
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
    has434: window.SF.assets.placed.has('fultonPlaza'),
    place434: window.SF.assets.placed.get('fultonPlaza') ? JSON.parse(JSON.stringify({ log: window.SF.assets.placed.get('fultonPlaza').log, scale: window.SF.assets.placed.get('fultonPlaza').scale })) : null,
  }))()`);
  console.log('  rig:', JSON.stringify(placed.rig));
  console.log('  placed434:', placed.has434, JSON.stringify(placed.place434));
  console.log('  placedIds:', placed.placedIds.join(','));
  console.log('  console lines:', console_.length);
  for (const l of console_) if (/434|warn|fail|error|keeping/i.test(l)) console.log('    >', l.slice(0, 200));

  const draws = QUICK ? null : await evaluate(`(async () => {
    const info = window.SF.renderer.info;
    const raf = () => new Promise((res) => requestAnimationFrame(res));
    info.autoReset = false; await raf(); info.reset();
    for (let i = 0; i < 30; i++) await raf();
    const calls = info.render.calls / 30; info.autoReset = true;
    return Math.round(calls);
  })()`);
  if (!QUICK) check('draw calls under 300 at the landmark', draws > 5 && draws < 300, `avg ${draws}/frame`);

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
    // The wide shot is in the quick path too: INTEGRATION-PROMPT Step 5 names
    // "day and night plus one wide", and one extra goTo is cheap even at load
    // 700. Everything below it is not.
    await evaluate(`window.SF.setClock('2026-08-17T14:30:00-07:00')`);
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 900, ${CAMERA.yaw}, 34)`);
    await new Promise((r) => setTimeout(r, 4000));
    await shot('wide');
  }
  if (!DRILL && !QUICK) {

    // The two ground-plane checks, both at eye level along the plaza's own axis
    // (bearing 81 deg = app yaw 99, and its reciprocal). A baked street ribbon
    // or a sidewalk plinth poking through the deck shows as a charcoal stripe or
    // a white dash; a drape error shows as a buried or floating end.
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 150, 99, 8)`);
    await new Promise((r) => setTimeout(r, 3000));
    await shot('low-from-hyde');
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 150, 279, 8)`);
    await new Promise((r) => setTimeout(r, 3000));
    await shot('low-from-larkin');
    await evaluate(`window.SF.goTo(${LON}, ${LAT}, 260, 99, 62)`);
    await new Promise((r) => setTimeout(r, 3000));
    await shot('plan');

    // The asphalt tone, measured rather than eyeballed. Read the framebuffer
    // back at the plaza's centre band, well clear of the monument's apron and
    // the two koi, and report the median so one bright pixel cannot flatter it.
    // readPixels straight off the GL back buffer, immediately after an explicit
    // render. drawImage() from the WebGL canvas cannot be used: the renderer runs
    // without preserveDrawingBuffer, so a 2D copy comes back all zeros — which is
    // exactly what the first version of this probe reported, and it looks like a
    // black plaza rather than like a broken measurement.
    // Measured from the SCREENSHOT, in Node, not in the page. Two in-page probes
    // were tried and both are traps under SwiftShader on a loaded machine:
    // drawImage() off the WebGL canvas returns all zeros (the renderer runs
    // without preserveDrawingBuffer, so a black plaza and a broken measurement
    // look identical), and gl.readPixels() forces a full software-pipeline flush
    // that did not return in 25 minutes at load 130. The screenshot is the same
    // pixels and it is already on disk.
    // Sampled off the DAY shot (the registry preset's own framing), in two bands
    // of open asphalt north and south of the monument's apron and clear of both
    // koi. The plan shot's window landed on the library's pale roof and reported
    // a median of 180, which passes the check while measuring the wrong thing.
    const tone = lumaFromPng(path.join(SHOTS, 'day.png'), 0.437, 0.538, 0.221, 0.295,
                                                          0.437, 0.538, 0.738, 0.812);
    console.log('  asphalt luminance:', JSON.stringify(tone));
    // The bar is the measured dark cliff: Toy_roofd read 9 and #35493e read 5,
    // while a lit Toy_steel roof reads ~95 and Toy_stone ~101. Anything above
    // ~20 is a surface rather than a hole; below that the asset needs lifting.
    // p90 is as diagnostic as the median here: the baked street's pale sidewalk
    // plinths, when they win the depth fight against the deck, show up as a p90
    // near 200 against a median near 38. That is what caught them.
    check('asphalt reads as a surface, not a hole', tone.median >= 20,
          `median luminance ${tone.median} (p10 ${tone.p10}, p90 ${tone.p90})`);
    check('no baked street bleeding through the deck', tone.p90 - tone.median <= 25,
          `p90 ${tone.p90} vs median ${tone.median}`);
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
