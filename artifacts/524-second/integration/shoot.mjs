// Local-QA screenshot harness for a single landmark.
//
//   node shoot.mjs --url http://127.0.0.1:5524 --lon .. --lat .. --out DIR --prefix NAME
//
// Drives a real foregrounded headless Chrome over CDP, exactly as
// .agents/skills/testing-sf-3d/SKILL.md prescribes: the in-app preview pane runs
// the tab hidden, which stops rAF and freezes the boot curtain, so screenshots
// of the city have to come from a browser with
// --disable-backgrounding-occluded-windows --disable-renderer-backgrounding.
// Changes no app runtime code.
import { spawn } from 'node:child_process';
import { mkdtemp, writeFile, mkdir } from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import net from 'node:net';

const argv = process.argv.slice(2);
const arg = (f, d) => (argv.includes(f) ? argv[argv.indexOf(f) + 1] : d);
const URL_ = arg('--url', 'http://127.0.0.1:5524');
const LON = Number(arg('--lon', '-122.393433'));
const LAT = Number(arg('--lat', '37.7825731'));
const OUT = arg('--out', '.');
const PREFIX = arg('--prefix', 'shot');
const ID = arg('--id', '524Second');
const CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
const freePort = () =>
  new Promise((res) => {
    const s = net.createServer();
    s.listen(0, '127.0.0.1', () => {
      const p = s.address().port;
      s.close(() => res(p));
    });
  });

async function waitHttp(url, ms = 30000) {
  const t0 = Date.now();
  for (;;) {
    try {
      const r = await fetch(url);
      if (r.ok) return await r.json().catch(() => ({}));
    } catch {}
    if (Date.now() - t0 > ms) throw new Error(`timeout ${url}`);
    await sleep(250);
  }
}

class Cdp {
  constructor(ws) {
    this.ws = ws;
    this.id = 0;
    this.pending = new Map();
    ws.addEventListener('message', (e) => {
      const m = JSON.parse(e.data);
      if (m.id && this.pending.has(m.id)) {
        const { res, rej } = this.pending.get(m.id);
        this.pending.delete(m.id);
        m.error ? rej(new Error(m.error.message)) : res(m.result);
      }
    });
  }
  static connect(url) {
    return new Promise((res, rej) => {
      const ws = new WebSocket(url);
      ws.addEventListener('open', () => res(new Cdp(ws)));
      ws.addEventListener('error', rej);
    });
  }
  send(method, params = {}, sessionId) {
    const id = ++this.id;
    this.ws.send(JSON.stringify({ id, method, params, sessionId }));
    return new Promise((res, rej) => this.pending.set(id, { res, rej }));
  }
}

async function main() {
  await mkdir(OUT, { recursive: true });
  const port = await freePort();
  const dir = await mkdtemp(path.join(os.tmpdir(), 'sf-shoot-'));
  const child = spawn(
    CHROME,
    [
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${dir}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-background-timer-throttling',
      '--disable-backgrounding-occluded-windows',
      '--disable-renderer-backgrounding',
      '--enable-unsafe-swiftshader',
      '--window-size=1600,900',
      '--headless=new',
      '--no-sandbox',
    ],
    { stdio: ['ignore', 'pipe', 'pipe'] }
  );
  child.stdout.on('data', () => {});
  child.stderr.on('data', () => {});

  const version = await waitHttp(`http://127.0.0.1:${port}/json/version`);
  const cdp = await Cdp.connect(version.webSocketDebuggerUrl);
  const { targetId } = await cdp.send('Target.createTarget', { url: 'about:blank' });
  const { sessionId } = await cdp.send('Target.attachToTarget', { targetId, flatten: true });
  const S = (m, p) => cdp.send(m, p, sessionId);

  await S('Page.enable');
  await S('Runtime.enable');
  await S('Log.enable');
  const logs = [];
  cdp.ws.addEventListener('message', (e) => {
    const m = JSON.parse(e.data);
    if (m.method === 'Runtime.consoleAPICalled') {
      logs.push((m.params.args || []).map((a) => a.value ?? a.description ?? '').join(' '));
    }
  });
  await S('Emulation.setDeviceMetricsOverride', {
    width: 1600,
    height: 900,
    deviceScaleFactor: 1,
    mobile: false,
    screenWidth: 1600,
    screenHeight: 900,
  });

  const evalJs = async (expr) => {
    const r = await S('Runtime.evaluate', {
      expression: expr,
      awaitPromise: true,
      returnByValue: true,
    });
    if (r.exceptionDetails) throw new Error(r.exceptionDetails.text + ' :: ' + expr.slice(0, 80));
    return r.result.value;
  };

  await S('Page.navigate', { url: URL_ });
  // boot
  for (let i = 0; i < 200; i++) {
    const ok = await evalJs('!!(window.SF && window.SF.boot && window.SF.boot.cleared)').catch(() => false);
    if (ok) break;
    await sleep(1000);
  }
  await evalJs('window.SF.boot.reveal && window.SF.boot.reveal()').catch(() => {});

  const shots = [];
  for (const [tag, clock] of [
    ['day', '2026-08-16T13:00:00-07:00'],
    ['night', '2026-08-16T21:30:00-07:00'],
  ]) {
    await evalJs(`window.SF.setClock(new Date('${clock}').getTime())`).catch(() => {});
    await evalJs(`window.SF.goTo(${LON}, ${LAT}, 200, 180, 26)`);
    await sleep(14000);
    const state = await evalJs(
      `JSON.stringify({stats:window.SF.assets.stats(), placed: window.SF.assets.placed.has('${ID}'), log:(window.SF.assets.placed.get('${ID}')||{}).log, frame: window.SF.renderer.info.render.frame, calls: window.SF.renderer.info.render.calls, night: (window.SF.sky && window.SF.sky.localTime) || null})`
    );
    const { data } = await S('Page.captureScreenshot', { format: 'png' });
    const file = path.join(OUT, `${PREFIX}-${tag}.png`);
    await writeFile(file, Buffer.from(data, 'base64'));
    shots.push({ tag, file, state });
    console.log(`[shoot] ${tag} -> ${file}\n        ${state}`);
  }

  // wide shot, day
  await evalJs(`window.SF.setClock(new Date('2026-08-16T13:00:00-07:00').getTime())`).catch(() => {});
  await evalJs(`window.SF.goTo(${LON}, ${LAT}, 900, 200, 30)`);
  await sleep(12000);
  const wide = await S('Page.captureScreenshot', { format: 'png' });
  await writeFile(path.join(OUT, `${PREFIX}-wide.png`), Buffer.from(wide.data, 'base64'));
  console.log(`[shoot] wide -> ${path.join(OUT, `${PREFIX}-wide.png`)}`);

  const merge = logs.filter((l) => /sf-assets/.test(l));
  await writeFile(path.join(OUT, `${PREFIX}-console.txt`), logs.join('\n') + '\n');
  console.log('[shoot] sf-assets console lines:');
  for (const l of merge) console.log('   ' + l);

  child.kill('SIGTERM');
}

main().catch((e) => {
  console.error('SHOOT-FAIL', e.message);
  process.exit(1);
});
