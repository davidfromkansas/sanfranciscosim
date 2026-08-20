// Supplementary day screenshot for the 131-steuart QA record.
//
// The registry camera preset looks in from the NORTH-EAST, because that is the
// only angle where the barrel-roofed penthouse reads against the brick cornice
// behind it. At 14:30 the sun is south-south-west, so that elevation is backlit
// and the standard qa_local day frame is a silhouette. In the morning the sun is
// east-south-east and lights the same face. Same rig, same anchor, earlier clock.
import { spawn } from 'node:child_process';
import { createReadStream, existsSync, statSync } from 'node:fs';
import { mkdtemp, writeFile } from 'node:fs/promises';
import http from 'node:http';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const DIST = path.resolve('app/dist');
const SHOTS = path.resolve('artifacts/131-steuart/qa');
const LON = -122.3924386, LAT = 37.7930568;
const MIME = { '.html':'text/html', '.js':'text/javascript', '.css':'text/css', '.json':'application/json',
  '.glb':'model/gltf-binary', '.bin':'application/octet-stream', '.png':'image/png', '.jpg':'image/jpeg',
  '.svg':'image/svg+xml', '.woff2':'font/woff2', '.ttf':'font/ttf', '.ico':'image/x-icon' };
const freePort = () => new Promise((r) => { const s = net.createServer(); s.listen(0, () => { const { port } = s.address(); s.close(() => r(port)); }); });
function serveDist(port) {
  const server = http.createServer((req, res) => {
    const url = decodeURIComponent(req.url.split('?')[0]);
    let file = path.join(DIST, url);
    if (!existsSync(file) || statSync(file).isDirectory()) {
      if (existsSync(file + '.gz')) file += '.gz'; else file = path.join(DIST, 'index.html');
    }
    if (!existsSync(file)) { res.writeHead(404); res.end('nope'); return; }
    const h = { 'Content-Type': MIME[path.extname(file.replace(/\.gz$/, ''))] || 'application/octet-stream' };
    if (file.endsWith('.gz')) h['Content-Encoding'] = 'gzip';
    res.writeHead(200, h); createReadStream(file).pipe(res);
  });
  return new Promise((r) => server.listen(port, () => r(server)));
}
const httpPort = await freePort(), cdpPort = await freePort();
const server = await serveDist(httpPort);
const profile = await mkdtemp(path.join(os.tmpdir(), 'qa131am-'));
const chrome = spawn('/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', [
  `--remote-debugging-port=${cdpPort}`, `--user-data-dir=${profile}`, '--no-first-run',
  '--no-default-browser-check', '--no-sandbox', '--headless=new',
  '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
  '--disable-backgrounding-occluded-windows', '--use-angle=swiftshader',
  '--enable-unsafe-swiftshader', '--window-size=1600,900'], { stdio: 'ignore' });
let version;
for (let i = 0; i < 200; i++) { try { version = await (await fetch(`http://127.0.0.1:${cdpPort}/json/version`)).json(); break; } catch { await new Promise((r) => setTimeout(r, 300)); } }
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let nextId = 1, sessionId = null; const pending = new Map();
ws.onmessage = (ev) => { const m = JSON.parse(ev.data); if (m.id && pending.has(m.id)) { const { resolve, reject } = pending.get(m.id); pending.delete(m.id); m.error ? reject(new Error(m.error.message)) : resolve(m.result); } };
const send = (method, params = {}, inSession = true) => new Promise((resolve, reject) => { const id = nextId++; pending.set(id, { resolve, reject }); ws.send(JSON.stringify({ id, method, params, sessionId: inSession ? sessionId : undefined })); });
const { targetId } = await send('Target.createTarget', { url: 'about:blank' }, false);
({ sessionId } = await send('Target.attachToTarget', { targetId, flatten: true }, false));
await send('Runtime.enable'); await send('Page.enable');
await send('Page.navigate', { url: `http://127.0.0.1:${httpPort}/` });
const ev = async (e) => (await send('Runtime.evaluate', { expression: e, awaitPromise: true, returnByValue: true })).result?.value;
const until = async (label, expr, ms = 600000) => { const t0 = Date.now(); for (;;) { const v = await ev(expr).catch(() => null); if (v) return v; if (Date.now() - t0 > ms) throw new Error(label + ' timed out'); await new Promise((r) => setTimeout(r, 800)); } };
await until('boot', 'window.SF && window.SF.assets && window.SF.goTo ? true : null');
await until('manifest', 'window.SF.assets.stats().entries > 0 ? true : null');
await ev(`window.SF.goTo(${LON}, ${LAT}, 200, 135, 28)`);
await ev(`window.__pump = window.__pump || setInterval(() => { try { window.SF.assets.update(window.SF.camera.position, 0.4); } catch {} }, 250)`);
await until('placed', `(() => (window.SF.assets.placed.has('131Steuart') && window.SF.assets.stats().fading === 0 && window.SF.assets.stats().loading === 0) ? true : null)()`);
await ev(`window.SF.setClock('2026-08-17T09:30:00-07:00')`);
await new Promise((r) => setTimeout(r, 6000));
const { data } = await send('Page.captureScreenshot', { format: 'png' });
await writeFile(path.join(SHOTS, 'day-morning.png'), Buffer.from(data, 'base64'));
console.log('wrote day-morning.png; stats', JSON.stringify(await ev('window.SF.assets.stats()')));
ws.close(); chrome.kill(); server.close(); process.exit(0);
