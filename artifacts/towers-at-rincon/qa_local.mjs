// Local QA for a landmark integration, driven over CDP against a REAL, foregrounded
// Chrome. The in-app preview pane runs its tab hidden, which stops rAF — and the
// landmark streamer, the renderer and the boot reveal all run per frame — so a
// hidden pane reports zero draw calls and zero placed assets for a perfectly good
// integration. Chrome is launched with the backgrounding guards off for the same reason.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';

const URL_BASE = process.argv[2] || 'http://127.0.0.1:5233/';
const LON = Number(process.argv[3]), LAT = Number(process.argv[4]);
const OUT = process.argv[5] || '/tmp/r88/shots';
const SLUG = process.argv[6] || 'towers-at-rincon';
mkdirSync(OUT, { recursive: true });

const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9333;
const chrome = spawn(CHROME, [
  `--remote-debugging-port=${PORT}`, '--headless=new', '--window-size=1600,1000',
  '--disable-backgrounding-occluded-windows', '--disable-renderer-backgrounding',
  '--disable-background-timer-throttling', '--use-gl=angle', '--enable-unsafe-swiftshader',
  '--user-data-dir=/tmp/r88/chromeprofile', 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function endpoint() {
  for (let i = 0; i < 60; i++) {
    try { const r = await fetch(`http://127.0.0.1:${PORT}/json/version`); if (r.ok) return (await r.json()).webSocketDebuggerUrl; } catch {}
    await sleep(500);
  }
  throw new Error('no CDP');
}
const wsUrl = await endpoint();
const { default: WS } = await import('ws').catch(() => ({ default: null }));
if (!WS) { console.error('need ws: npm i -g ws'); process.exit(2); }
const ws = new WS(wsUrl);
await new Promise((r) => ws.on('open', r));
let id = 0; const pend = new Map();
ws.on('message', (m) => { const d = JSON.parse(m); if (d.id && pend.has(d.id)) { pend.get(d.id)(d); pend.delete(d.id); } });
const send = (method, params = {}, sessionId) => new Promise((res) => { const i = ++id; pend.set(i, res); ws.send(JSON.stringify({ id: i, method, params, sessionId })); });

const { result: { targetId } } = await send('Target.createTarget', { url: URL_BASE });
const { result: { sessionId } } = await send('Target.attachToTarget', { targetId, flatten: true });
const evalJs = async (expr, awaitPromise = true) => {
  const r = await send('Runtime.evaluate', { expression: expr, awaitPromise, returnByValue: true }, sessionId);
  if (r.result?.exceptionDetails) return { error: r.result.exceptionDetails.text + ' ' + (r.result.exceptionDetails.exception?.description || '') };
  return r.result?.result?.value;
};
const shot = async (name) => {
  const r = await send('Page.captureScreenshot', { format: 'png' }, sessionId);
  if (r.result?.data) writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.result.data, 'base64'));
};
await send('Page.enable', {}, sessionId);
await send('Runtime.enable', {}, sessionId);
const logs = [];
ws.on('message', (m) => { const d = JSON.parse(m); if (d.method === 'Runtime.consoleAPICalled') logs.push(d.params.args.map(a => a.value ?? a.description ?? '').join(' ')); });

await sleep(9000);
console.log('boot:', JSON.stringify(await evalJs(`(async()=>{for(let i=0;i<80&&!window.SF;i++)await new Promise(r=>setTimeout(r,300));return {sf:!!window.SF,hidden:document.hidden,cleared:window.SF&&SF.boot.cleared}})()`)));
await evalJs(`SF.boot.reveal('qa'); SF.setClock && SF.setClock('2026-08-19T13:30:00-07:00'); true`);
await evalJs(`SF.goTo(${LON}, ${LAT}); SF.rig.state.distance=620; SF.rig.state.yaw=90; SF.rig.state.pitch=22; true`);
await sleep(14000);
const day = await evalJs(`(()=>{const p=SF.assets.placed; const m=p instanceof Map?p.get('${SLUG}'):(p||{})['${SLUG}'];
  return {stats:SF.assets.stats(), placed:(p instanceof Map?[...p.keys()]:Object.keys(p||{})).length,
   mine:!!m, scale:m&&(m.scale?.x??m.uniform??null), draws:SF.renderer.info.render.calls,
   tris:SF.renderer.info.render.triangles, pivotY:SF.rig.state.pivot.y, hidden:document.hidden};})()`);
console.log('DAY', JSON.stringify(day, null, 1));
await shot('day');
await evalJs(`SF.rig.state.distance=1400; SF.rig.state.pitch=30; true`); await sleep(3500); await shot('day_wide');
await evalJs(`SF.setClock && SF.setClock('2026-08-19T22:00:00-07:00'); SF.rig.state.distance=620; SF.rig.state.pitch=22; true`);
await sleep(9000);
const night = await evalJs(`({night:SF.sky&&SF.sky.uNight, draws:SF.renderer.info.render.calls})`);
console.log('NIGHT', JSON.stringify(night));
await shot('night');
console.log('CONSOLE with slug:'); logs.filter(l => l.includes('${SLUG}') || l.includes('towers-at-rincon') || l.toLowerCase().includes('sf-assets')).forEach(l => console.log('  ', l));
writeFileSync(`${OUT}/console.txt`, logs.join('\n'));
ws.close(); chrome.kill();
