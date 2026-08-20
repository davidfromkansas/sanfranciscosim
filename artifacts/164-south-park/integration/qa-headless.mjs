// Stage-5 local QA for 164-south-park, headless Chrome + CDP against the Vite dev
// server. Flags copied from pipeline/landmark-streaming-check.mjs.
import { spawn } from 'node:child_process';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';
import { mkdtemp, writeFile } from 'node:fs/promises';
import { renameSync, existsSync } from 'node:fs';

const WT = '/Users/david_lietjauw/sf-worktrees/164-south-park';
const SLUG = '164-south-park';
const CAMEL = '164SouthPark';
const LON = -122.3949366, LAT = 37.7812097;
const DRILL = process.argv.includes('--drill');
const OUT = '/tmp/qa164';

const freePort = () => new Promise((res) => { const s = net.createServer(); s.listen(0, () => { const { port } = s.address(); s.close(() => res(port)); }); });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
function findChrome() {
  for (const p of ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
                   '/Applications/Chromium.app/Contents/MacOS/Chromium'])
    if (existsSync(p)) return p;
  throw new Error('no chrome');
}

const vitePort = await freePort();
const vite = spawn('npm', ['run', 'dev', '--prefix', `${WT}/app`, '--', '--port', String(vitePort), '--strictPort'], { stdio: ['ignore', 'pipe', 'pipe'] });
await new Promise((res, rej) => {
  let buf = '';
  const t = setTimeout(() => rej(new Error('vite timeout\n' + buf)), 180000);
  vite.stdout.on('data', (d) => { buf += d; if (/Local:\s+http/.test(buf)) { clearTimeout(t); res(); } });
  vite.stderr.on('data', (d) => { buf += d; });
});
console.log('vite on', vitePort);

const man = await (await fetch(`http://127.0.0.1:${vitePort}/sf-assets/landmarks_manifest.json`)).json();
const mine = man.find((e) => e.id === SLUG);
console.log('MANIFEST-CHECK entries=%d mine=%s', man.length, JSON.stringify(mine));
if (!mine) { vite.kill(); process.exit(2); }

const glbPath = `${WT}/app/public/sf-assets/landmarks/${SLUG}.glb`;
const movedPath = `${glbPath}.qa-moved`;
let moved = false;
const restore = () => { if (moved && existsSync(movedPath)) { renameSync(movedPath, glbPath); moved = false; console.log('restored GLB'); } };
process.on('exit', restore); process.on('SIGINT', () => { restore(); process.exit(1); });

const cdpPort = await freePort();
const dir = await mkdtemp(path.join(os.tmpdir(), 'qa164-'));
const chrome = spawn(findChrome(), [
  `--remote-debugging-port=${cdpPort}`, `--user-data-dir=${dir}`,
  '--no-first-run', '--no-default-browser-check',
  '--disable-background-timer-throttling', '--disable-renderer-backgrounding',
  '--enable-unsafe-swiftshader', '--window-size=1600,900', '--no-sandbox', '--headless=new',
], { stdio: 'ignore' });
for (let i = 0; i < 200; i++) { try { await fetch(`http://127.0.0.1:${cdpPort}/json/version`); break; } catch { await sleep(300); } }
const version = await (await fetch(`http://127.0.0.1:${cdpPort}/json/version`)).json();
const ws = new WebSocket(version.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let nextId = 1; const pending = new Map(); let sessionId = null;
const consoleLines = [];
ws.onmessage = (ev) => {
  const m = JSON.parse(ev.data);
  if (m.id && pending.has(m.id)) { const { resolve, reject } = pending.get(m.id); pending.delete(m.id); m.error ? reject(new Error(m.error.message)) : resolve(m.result); }
  else if (m.method === 'Runtime.consoleAPICalled') consoleLines.push((m.params.args || []).map((a) => a.value ?? a.description ?? '').join(' '));
  else if (m.method === 'Runtime.exceptionThrown') consoleLines.push('EXCEPTION: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
};
const send = (method, params = {}, inSession = true) => new Promise((resolve, reject) => {
  const id = nextId++; pending.set(id, { resolve, reject });
  const t = setTimeout(() => { if (pending.delete(id)) resolve({ __timeout: true }); }, 120000);
  const orig = resolve; pending.set(id, { resolve: (v) => { clearTimeout(t); orig(v); }, reject: (e) => { clearTimeout(t); reject(e); } });
  ws.send(JSON.stringify({ id, method, params, sessionId: inSession ? sessionId : undefined }));
});
const ev = async (expr) => {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
  if (r.__timeout) return '<<timeout>>';
  if (r.exceptionDetails) return 'ERR: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text);
  return r.result?.value;
};

const { targetId } = await send('Target.createTarget', { url: 'about:blank' }, false);
({ sessionId } = await send('Target.attachToTarget', { targetId, flatten: true }, false));
await send('Runtime.enable'); await send('Page.enable');

async function bootAndReport(tag) {
  await send('Page.navigate', { url: `http://127.0.0.1:${vitePort}/?qa=${Date.now()}` });
  for (let i = 0; i < 120; i++) { if (await ev('!!(window.SF && SF.assets)')) break; await sleep(2000); }
  console.log(`[${tag}] SF ready:`, await ev('!!(window.SF && SF.assets)'));
  console.log(`[${tag}] rAF frames/3s:`, await ev(`new Promise(r=>{let n=0;const s=()=>{n++;n<200?requestAnimationFrame(s):r(n)};requestAnimationFrame(s);setTimeout(()=>r(n),3000)})`));
  await ev(`SF.setClock('2026-08-18T13:30:00-07:00')`);
  await ev(`SF.goTo(${LON}, ${LAT}, 120, 85, 26)`);
  let placed = false;
  for (let i = 0; i < 90; i++) { placed = await ev(`!!(SF.assets.placed && SF.assets.placed.has('${CAMEL}'))`); if (placed === true) break; await sleep(2000); }
  console.log(`[${tag}] placed(${CAMEL}):`, placed);
  console.log(`[${tag}] stats:`, JSON.stringify(await ev('JSON.stringify(SF.assets.stats())')));
  console.log(`[${tag}] record.log:`, await ev(`(SF.assets.placed.get('${CAMEL}')||{}).log || '(none)'`));
  console.log(`[${tag}] rig:`, await ev('JSON.stringify({yawDeg: SF.rig.state.yaw*180/Math.PI, pitchDeg: SF.rig.state.pitch*180/Math.PI, dist: SF.rig.state.distance, pivot: SF.rig.state.pivot})'));
  return placed;
}

// ---- main pass -------------------------------------------------------------
if (!DRILL) {
  await bootAndReport('main');
  // draw calls: hook render and take the max over the app's own frames
  await ev(`(()=>{const r=SF.renderer;const o=r.render.bind(r);window.__max=0;r.render=(s,c)=>{o(s,c);window.__max=Math.max(window.__max,r.info.render.calls);};return 1})()`);
  await sleep(8000);
  console.log('[main] max draw calls (hooked):', await ev('window.__max'));
  // settle gate then screenshots
  for (const [tag, clock] of [['day', '2026-08-18T13:30:00-07:00'], ['night', '2026-08-18T21:30:00-07:00']]) {
    await ev(`SF.setClock('${clock}')`);
    let prev = '', same = 0;
    for (let i = 0; i < 60; i++) {
      const s = await ev('JSON.stringify(SF.assets.stats())');
      const st = (() => { try { return JSON.parse(s); } catch { return {}; } })();
      if (s === prev && st.loading === 0 && st.fading === 0) same++; else same = 0;
      prev = s; if (same >= 4) break; await sleep(1500);
    }
    await ev(`document.querySelectorAll('[class*="boot"],[id*="boot"]').forEach(n=>n.remove())`);
    await sleep(1500);
    const shot = await send('Page.captureScreenshot', { format: 'png' });
    if (shot && shot.data) { await writeFile(`${OUT}-${tag}.png`, Buffer.from(shot.data, 'base64')); console.log(`[main] wrote ${OUT}-${tag}.png`); }
    else console.log(`[main] screenshot ${tag} FAILED`);
  }
  console.log('[main] console lines mentioning the slug:');
  consoleLines.filter((l) => /164|sf-assets|merged|failed/i.test(l)).slice(-25).forEach((l) => console.log('   ', l));
} else {
  // ---- fallback drill -------------------------------------------------------
  renameSync(glbPath, movedPath); moved = true;
  console.log('[drill] GLB moved aside');
  await bootAndReport('drill');
  console.log('[drill] stats:', JSON.stringify(await ev('JSON.stringify(SF.assets.stats())')));
  console.log('[drill] city stats:', await ev('JSON.stringify(SF.city && SF.city.stats ? SF.city.stats : "n/a")'));
  console.log('[drill] console lines:');
  consoleLines.filter((l) => /164|keeping the code-built|failed/i.test(l)).slice(-20).forEach((l) => console.log('   ', l));
  restore();
}
chrome.kill(); vite.kill();
process.exit(0);
