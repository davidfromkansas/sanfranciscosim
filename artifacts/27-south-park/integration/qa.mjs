// Headless-Chrome QA for the 27 South Park integration, driven over CDP.
// preview_start had no server slots left (five parallel sessions), so this
// drives the built app/dist instead. Same bundle the browser pane would serve.
import { spawn } from 'node:child_process';
import { writeFileSync, mkdirSync } from 'node:fs';

const URLBASE = 'http://127.0.0.1:5027';
const OUT = process.argv[2] || '/private/tmp/claude-501/-Users-david-lietjauw/03d76043-69ed-49ae-9d80-abbc55f65764/scratchpad/sp27/qa';
const NIGHT = process.argv.includes('--night');
mkdirSync(OUT, { recursive: true });
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT = 9227;

const chrome = spawn(CHROME, [
  `--remote-debugging-port=${PORT}`, '--headless=new', '--disable-gpu-sandbox',
  '--use-angle=metal', '--enable-unsafe-swiftshader',
  '--window-size=1600,1000', '--hide-scrollbars', '--mute-audio',
  '--user-data-dir=/tmp/sf27-chrome', 'about:blank',
], { stdio: 'ignore' });

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

async function ws() {
  for (let i = 0; i < 60; i++) {
    try {
      const r = await fetch(`http://127.0.0.1:${PORT}/json/version`);
      return (await r.json()).webSocketDebuggerUrl;
    } catch { await sleep(500); }
  }
  throw new Error('chrome never came up');
}

const url = await ws();
const sock = new WebSocket(url);
await new Promise((r) => (sock.onopen = r));
let id = 0;
const pending = new Map();
const logs = [];
sock.onmessage = (m) => {
  const msg = JSON.parse(m.data);
  if (msg.id && pending.has(msg.id)) { pending.get(msg.id)(msg); pending.delete(msg.id); }
  if (msg.method === 'Runtime.consoleAPICalled') {
    logs.push(msg.params.args.map((a) => a.value ?? a.description ?? '').join(' '));
  }
  if (msg.method === 'Log.entryAdded') logs.push('[' + msg.params.entry.level + '] ' + msg.params.entry.text);
};
const send = (method, params = {}, sessionId) =>
  new Promise((res) => { const i = ++id; pending.set(i, res); sock.send(JSON.stringify({ id: i, method, params, sessionId })); });

const { result: { targetInfos } } = await send('Target.getTargets');
let page = targetInfos.find((t) => t.type === 'page');
const { result: { sessionId } } = await send('Target.attachToTarget', { targetId: page.targetId, flatten: true });
const S = (m, p) => send(m, p, sessionId);
await S('Runtime.enable'); await S('Log.enable'); await S('Page.enable');
await S('Emulation.setDeviceMetricsOverride', { width: 1600, height: 1000, deviceScaleFactor: 1, mobile: false });

const evalJs = async (expr, awaitPromise = true) => {
  const r = await S('Runtime.evaluate', { expression: expr, awaitPromise, returnByValue: true });
  if (r.result?.exceptionDetails) throw new Error(JSON.stringify(r.result.exceptionDetails));
  return r.result?.result?.value;
};

await S('Page.navigate', { url: URLBASE + '/' });
await sleep(1000);
for (let i = 0; i < 90; i++) { if (await evalJs('!!(window.SF && window.SF.goTo)')) break; await sleep(1000); }
console.log('SF api ready:', await evalJs('!!(window.SF && window.SF.goTo)'));
console.log('SF keys:', JSON.stringify(await evalJs('Object.keys(window.SF||{})')));

// SF.goTo takes DEGREES; signature is (lon, lat, distance, yaw, pitch).
// The registry preset for this landmark is distance 170, yaw 225, pitch 26.
await evalJs(`window.SF.setClock(new Date(new Date().setHours(${NIGHT ? 21 : 13},${NIGHT ? 30 : 0},0,0)).toISOString())`);
await evalJs('window.SF.goTo(-122.3931439, 37.7817369, 170, 225, 26)');
await sleep(12000);
await evalJs('window.SF.goTo(-122.3931439, 37.7817369, 170, 225, 26)');
await sleep(10000);

const shot = async (name) => {
  const r = await S('Page.captureScreenshot', { format: 'png' });
  writeFileSync(`${OUT}/${name}.png`, Buffer.from(r.result.data, 'base64'));
  console.log('shot', name);
};
await shot(NIGHT ? 'night' : 'day');
if (!NIGHT) {
  await evalJs('window.SF.goTo(-122.3931439, 37.7817369, 260, 225, 62)');
  await sleep(6000);
  await shot('top');
  await evalJs('window.SF.goTo(-122.3931439, 37.7817369, 900, 225, 34)');
  await sleep(7000);
  await shot('wide');
}

// renderer.info.render.calls is reset per frame, so an arbitrary CDP eval
// reads a partial frame. The app's own debug overlay reads it in the right
// place in the loop, so open that (backtick) and scrape it instead.
await S('Input.dispatchKeyEvent', { type: 'keyDown', key: '`', code: 'Backquote', windowsVirtualKeyCode: 192, nativeVirtualKeyCode: 192 });
await S('Input.dispatchKeyEvent', { type: 'keyUp', key: '`', code: 'Backquote', windowsVirtualKeyCode: 192, nativeVirtualKeyCode: 192 });
await sleep(3000);
const budget = await evalJs(`(function(){
  const el = [...document.querySelectorAll('*')].filter(e => /draw calls/.test(e.textContent||'') && e.children.length===0).pop();
  return el ? el.textContent : 'debug overlay not found';
})()`);
console.log('BUDGET', JSON.stringify(budget));
const info = await evalJs(`JSON.stringify({
  camera: [Math.round(SF.camera.position.x), Math.round(SF.camera.position.y), Math.round(SF.camera.position.z)],
  batchNames: SF.scene.children.flatMap(function walk(o){return [o.name].concat((o.children||[]).flatMap(walk))}).filter(n=>n&&/landmark|batch/i.test(n)),
})`);
console.log('INFO', info);
console.log('CONSOLE-LINES');
for (const l of logs) if (/sf-assets|27-south-park|warn|error|404|fallback|keeping the code-built/i.test(l)) console.log('  ' + l);
writeFileSync(`${OUT}/console${NIGHT ? '-night' : ''}.log`, logs.join('\n'));
chrome.kill();
process.exit(0);
