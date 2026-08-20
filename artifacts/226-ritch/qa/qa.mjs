// Stage-5 local QA for 226-ritch, headless Chrome over CDP against the Vite dev
// server. Flags and settle gate copied from pipeline/landmark-streaming-check.mjs.
//   node qa.mjs [--drill]
import { spawn } from 'node:child_process';
import { mkdtemp, writeFile } from 'node:fs/promises';
import { existsSync, renameSync } from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const WT = '/Users/david_lietjauw/sf-worktrees/226-ritch';
const SLUG = '226-ritch';
const CAMEL = '226Ritch';
const LON = -122.3960899, LAT = 37.7804376;
const GLB = `${WT}/app/public/sf-assets/landmarks/${SLUG}.glb`;
const DRILL = process.argv.includes('--drill');
const OUT = '/tmp/ritch226/qa';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const freePort = () => new Promise((res) => { const s = net.createServer(); s.listen(0, () => { const { port } = s.address(); s.close(() => res(port)); }); });
function findChrome() {
  for (const c of ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/usr/bin/google-chrome']) if (existsSync(c)) return c;
  throw new Error('no Chrome');
}

const log = [];
const say = (...a) => { const s = a.join(' '); log.push(s); console.log(s); };

async function main() {
  const appPort = await freePort();
  const dev = spawn('npm', ['run', 'dev', '--prefix', `${WT}/app`, '--', '--port', String(appPort), '--strictPort'], { stdio: ['ignore', 'pipe', 'pipe'] });
  await new Promise((res, rej) => {
    const t = setTimeout(() => rej(new Error('dev server timeout')), 120000);
    dev.stdout.on('data', (d) => { if (String(d).includes('Local:')) { clearTimeout(t); res(); } });
  });
  say('dev server on', appPort);

  const mani = await (await fetch(`http://localhost:${appPort}/sf-assets/landmarks_manifest.json`)).json();
  const mine = mani.find((e) => e.id === SLUG);
  say(`manifest served: ${mani.length} entries; ${SLUG} present: ${!!mine}`);
  if (mine) say('  entry:', JSON.stringify(mine));

  if (DRILL) { renameSync(GLB, GLB + '.away'); say('DRILL: moved GLB aside'); }

  const cdp = await freePort();
  const dir = await mkdtemp(path.join(os.tmpdir(), 'ritch-qa-'));
  const chrome = spawn(findChrome(), [
    `--remote-debugging-port=${cdp}`, `--user-data-dir=${dir}`, '--no-first-run',
    '--no-default-browser-check', '--disable-background-timer-throttling',
    '--disable-renderer-backgrounding', '--enable-unsafe-swiftshader',
    '--window-size=1600,900', '--no-sandbox', '--headless=new',
  ], { stdio: 'ignore' });
  for (let i = 0; i < 200; i++) { try { await fetch(`http://127.0.0.1:${cdp}/json/version`); break; } catch { await sleep(300); } }
  const version = await (await fetch(`http://127.0.0.1:${cdp}/json/version`)).json();
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  let nextId = 1; const pending = new Map(); let sessionId = null;
  const consoleLines = [];
  ws.onmessage = (ev) => {
    const m = JSON.parse(ev.data);
    if (m.id && pending.has(m.id)) { const p = pending.get(m.id); pending.delete(m.id); m.error ? p.reject(new Error(m.error.message)) : p.resolve(m.result); }
    else if (m.method === 'Runtime.consoleAPICalled') consoleLines.push(m.params.args.map((a) => a.value ?? a.description ?? '').join(' '));
    else if (m.method === 'Runtime.exceptionThrown') consoleLines.push('EXCEPTION: ' + (m.params.exceptionDetails.exception?.description || m.params.exceptionDetails.text));
  };
  const send = (method, params = {}, inSession = true) => new Promise((resolve, reject) => {
    const id = nextId++; pending.set(id, { resolve, reject });
    ws.send(JSON.stringify({ id, method, params, sessionId: inSession ? sessionId : undefined }));
    setTimeout(() => { if (pending.has(id)) { pending.delete(id); resolve({ __timeout: true }); } }, 180000);
  });
  const { targetId } = await send('Target.createTarget', { url: 'about:blank' }, false);
  ({ sessionId } = await send('Target.attachToTarget', { targetId, flatten: true }, false));
  await send('Runtime.enable'); await send('Page.enable');
  const evaluate = async (expr) => {
    const r = await send('Runtime.evaluate', { expression: expr, awaitPromise: true, returnByValue: true });
    if (r.__timeout) return '__TIMEOUT__';
    if (r.exceptionDetails) return 'ERR: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text);
    return r.result?.value;
  };
  await send('Page.navigate', { url: `http://localhost:${appPort}/?t=${Date.now()}` });

  // wait for SF
  for (let i = 0; i < 120; i++) { if (await evaluate('!!window.SF')) break; await sleep(2000); }
  say('SF present:', await evaluate('!!window.SF'));
  // rAF health
  say('rAF frames in 3s:', await evaluate("new Promise(r=>{let n=0;const s=()=>{n++;n<200?requestAnimationFrame(s):r(n)};requestAnimationFrame(s);setTimeout(()=>r(n),3000)})"));
  // hook renderer.render for real draw calls
  await evaluate("(()=>{const r=SF.renderer;const o=r.render.bind(r);window.__max=0;r.render=(s,c)=>{o(s,c);window.__max=Math.max(window.__max,r.info.render.calls);};return 1})()");

  await evaluate(`SF.setClock('2026-08-18T13:30:00-07:00')`);
  await evaluate(`SF.goTo(${LON}, ${LAT}, 180, 134, 28)`);
  let placed = false;
  for (let i = 0; i < 90; i++) { placed = await evaluate(`SF.assets.placed.has('${CAMEL}')`); if (placed === true) break; await sleep(2000); }
  say('placed:', placed);
  say('stats:', JSON.stringify(await evaluate('SF.assets.stats()')));
  say('log line:', await evaluate(`(SF.assets.placed.get('${CAMEL}')||{}).log || 'none'`));
  say('rig:', await evaluate('JSON.stringify({yaw:SF.rig.state.yaw*180/Math.PI, pitch:SF.rig.state.pitch*180/Math.PI, dist:SF.rig.state.distance, pivot:SF.rig.state.pivot})'));

  if (!DRILL) {
    // settle then shoot
    let prev = '', stable = 0;
    for (let i = 0; i < 60; i++) {
      const s = await evaluate('JSON.stringify(SF.assets.stats())');
      const o = JSON.parse(s || '{}');
      if (s === prev && o.loading === 0 && o.fading === 0) stable++; else stable = 0;
      prev = s; if (stable >= 4) break; await sleep(2000);
    }
    say('settled stats:', prev);
    await evaluate("document.querySelectorAll('[class*=\"boot\"],[id*=\"boot\"]').forEach(n=>n.remove())");
    await sleep(3000);
    for (const [tag, clock] of [['day', '2026-08-18T13:30:00-07:00'], ['night', '2026-08-18T21:30:00-07:00']]) {
      await evaluate(`SF.setClock('${clock}')`);
      await sleep(6000);
      const shot = await send('Page.captureScreenshot', { format: 'png' });
      if (shot?.data) { await writeFile(`${OUT}-${tag}.png`, Buffer.from(shot.data, 'base64')); say('shot', tag, `${OUT}-${tag}.png`); }
    }
    // wide shot
    await evaluate(`SF.setClock('2026-08-18T13:30:00-07:00'); SF.goTo(${LON}, ${LAT}, 700, 134, 34)`);
    await sleep(12000);
    const wide = await send('Page.captureScreenshot', { format: 'png' });
    if (wide?.data) { await writeFile(`${OUT}-wide.png`, Buffer.from(wide.data, 'base64')); say('shot wide'); }
    say('max draw calls:', await evaluate('window.__max'));
  } else {
    say('drill stats:', JSON.stringify(await evaluate('SF.assets.stats()')));
    say('city alive:', await evaluate('!!SF.city && !!SF.city.stats'));
  }

  const rel = consoleLines.filter((l) => /sf-assets|226-ritch|226Ritch|failed|warn|error|404/i.test(l));
  say('--- console (filtered) ---'); rel.slice(0, 40).forEach((l) => say('  ' + l));

  if (DRILL && existsSync(GLB + '.away')) { renameSync(GLB + '.away', GLB); say('DRILL: restored GLB'); }
  chrome.kill(); dev.kill();
  await writeFile(`${OUT}-${DRILL ? 'drill' : 'main'}.log`, log.join('\n'));
  process.exit(0);
}
main().catch(async (e) => {
  console.error('FATAL', e);
  if (existsSync(GLB + '.away')) renameSync(GLB + '.away', GLB);
  process.exit(1);
});
