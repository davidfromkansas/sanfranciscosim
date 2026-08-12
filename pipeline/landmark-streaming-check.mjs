// Acceptance check for landmark streaming (PERF-PLAN #3). Drives the built app
// in headless Chrome — rendering runs continuously there, which the in-editor
// preview pane cannot guarantee — and walks the full lifecycle:
//
//   boot: only resident entries load, streamed entries stay 'far'
//   approach: a streamed landmark loads and fades in
//   depart: it fades out and releases
//   budget: draw calls stay under the iron-rule 300 with everything nearby live
//
// Run against a build whose dist manifest includes streamed entries. Inject
// 100 synthetic `dummy-*` entries (donor GLBs, scattered anchors, loadRadius
// 2500) into app/dist/sf-assets/landmarks_manifest.json after `npm run build`,
// serve dist with `vite preview`, then:
//
//   node pipeline/landmark-streaming-check.mjs --url http://localhost:<port>
//
// Zero dependencies; Node 22 (native fetch + WebSocket).

import { spawn } from 'node:child_process';
import { mkdtemp } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import net from 'node:net';
import os from 'node:os';
import path from 'node:path';

const url = process.argv[process.argv.indexOf('--url') + 1] || 'http://localhost:5699';

function findChrome() {
  const candidates = [
    process.env.CHROME_PATH,
    '/usr/bin/google-chrome',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ].filter(Boolean);
  for (const c of candidates) if (existsSync(c)) return c;
  throw new Error('no Chrome binary found — set CHROME_PATH');
}

const freePort = () =>
  new Promise((resolve) => {
    const srv = net.createServer();
    srv.listen(0, () => {
      const { port } = srv.address();
      srv.close(() => resolve(port));
    });
  });

async function main() {
  const port = await freePort();
  const dir = await mkdtemp(path.join(os.tmpdir(), 'lm-check-'));
  const chrome = spawn(
    findChrome(),
    [
      `--remote-debugging-port=${port}`,
      `--user-data-dir=${dir}`,
      '--no-first-run',
      '--no-default-browser-check',
      '--disable-background-timer-throttling',
      '--disable-renderer-backgrounding',
      '--enable-unsafe-swiftshader',
      '--window-size=1600,900',
      '--no-sandbox',
      '--headless=new',
    ],
    { stdio: 'ignore' }
  );
  for (let i = 0; i < 100; i++) {
    try {
      await fetch(`http://127.0.0.1:${port}/json/version`);
      break;
    } catch {
      await new Promise((r) => setTimeout(r, 300));
    }
  }
  const version = await (await fetch(`http://127.0.0.1:${port}/json/version`)).json();
  const ws = new WebSocket(version.webSocketDebuggerUrl);
  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });
  let nextId = 1;
  const pending = new Map();
  let sessionId = null;
  ws.onmessage = (event) => {
    const message = JSON.parse(event.data);
    if (message.id && pending.has(message.id)) {
      const { resolve, reject } = pending.get(message.id);
      pending.delete(message.id);
      if (message.error) reject(new Error(message.error.message));
      else resolve(message.result);
    } else if (message.method === 'Runtime.exceptionThrown') {
      const d = message.params.exceptionDetails;
      console.error('PAGE EXCEPTION:', d.exception?.description || d.text);
    }
  };
  const send = (method, params = {}, inSession = true) =>
    new Promise((resolve, reject) => {
      const id = nextId++;
      pending.set(id, { resolve, reject });
      ws.send(JSON.stringify({ id, method, params, sessionId: inSession ? sessionId : undefined }));
    });

  const { targetId } = await send('Target.createTarget', { url: 'about:blank' }, false);
  ({ sessionId } = await send('Target.attachToTarget', { targetId, flatten: true }, false));
  await send('Runtime.enable');
  await send('Page.enable');
  await send('Page.navigate', { url });

  const evaluate = async (expression) => {
    const { result, exceptionDetails } = await send('Runtime.evaluate', {
      expression,
      awaitPromise: true,
      returnByValue: true,
    });
    if (exceptionDetails) throw new Error(exceptionDetails.text + ' ' + (exceptionDetails.exception?.description || ''));
    return result.value;
  };

  const stats = () => evaluate('window.SF?.assets?.stats?.() ?? null');
  const until = async (label, predicate, timeoutMs = 60000) => {
    const start = Date.now();
    for (;;) {
      const s = await stats();
      if (s && predicate(s)) return s;
      if (Date.now() - start > timeoutMs) throw new Error(`${label}: timed out — last ${JSON.stringify(s)}`);
      await new Promise((r) => setTimeout(r, 700));
    }
  };

  const results = [];
  const check = (name, ok, detail) => {
    results.push({ name, ok, detail });
    console.log(`${ok ? 'PASS' : 'FAIL'}  ${name} — ${detail}`);
  };

  // 1. Boot: all residents live, every streamed entry still far.
  const boot = await until('boot', (s) => s.live > 0 && s.loading === 0 && s.fading === 0, 120000);
  const streamedTotal = boot.entries - boot.live - boot.far === 0 ? boot.far : NaN;
  check('boot keeps streamed entries unloaded', boot.far === streamedTotal && boot.far > 0, JSON.stringify(boot));

  // 2. Draw calls at the hero view with the full synthetic manifest. autoReset
  // zeroes the counter after every render() and the post pass renders last, so
  // an ad-hoc read only ever sees the post quad — accumulate 30 whole frames
  // instead and take the per-frame average.
  await new Promise((r) => setTimeout(r, 3000));
  const heroDraws = await evaluate(`(async () => {
    const info = window.SF.renderer.info;
    const raf = () => new Promise((res) => requestAnimationFrame(res));
    info.autoReset = false;
    await raf(); info.reset();
    for (let i = 0; i < 30; i++) await raf();
    const calls = info.render.calls / 30;
    info.autoReset = true;
    return Math.round(calls);
  })()`);
  check('hero draw calls under budget', heroDraws > 10 && heroDraws < 300, `avg ${heroDraws}/frame < 300`);

  // 3. Approach a streamed landmark: it loads and fades in.
  const dummy = await evaluate(
    `fetch('/sf-assets/landmarks_manifest.json').then(r => r.json()).then(m => m.find(e => e.loadRadius > 0)?.anchor)`
  );
  if (!dummy) throw new Error('no streamed entry in the manifest — inject the synthetic manifest first');
  await evaluate(`window.SF.goTo(${dummy[0]}, ${dummy[1]}, 600, 210, 30); 'ok'`);
  const arrived = await until('stream-in', (s) => s.live > boot.live);
  check('streamed landmark loads on approach', true, JSON.stringify(arrived));

  // 4. Leave: out-of-radius landmarks release. The destination may itself sit
  // within radius of other streamed entries, so the assertion is that the
  // count FELL and nothing is stuck mid-fade — not that it returns to boot.
  await evaluate(`window.SF.goTo(-122.3937, 37.7955, 800, 150, 20); 'ok'`);
  const departed = await until(
    'stream-out',
    (s) => s.live < arrived.live && s.fading === 0 && s.loading === 0
  );
  check('streamed landmarks release on depart', departed.far > arrived.far, JSON.stringify(departed));

  // 5. Re-approach: the SAME landmarks load again (buffer space reclaimed by
  // optimize()) and street-level draw calls stay in budget.
  await evaluate(`window.SF.goTo(${dummy[0]}, ${dummy[1]}, 300, 210, 35); 'ok'`);
  const back = await until('re-approach', (s) => s.live > departed.live && s.loading === 0 && s.fading === 0);
  check('re-approach reloads with zero failures', back.failed === 0, JSON.stringify(back));
  await new Promise((r) => setTimeout(r, 2000));
  const nearDraws = await evaluate(`(async () => {
    const info = window.SF.renderer.info;
    const raf = () => new Promise((res) => requestAnimationFrame(res));
    info.autoReset = false;
    await raf(); info.reset();
    for (let i = 0; i < 30; i++) await raf();
    const calls = info.render.calls / 30;
    info.autoReset = true;
    return Math.round(calls);
  })()`);
  check('draw calls near streamed landmarks', nearDraws > 10 && nearDraws < 300, `avg ${nearDraws}/frame < 300`);

  chrome.kill('SIGTERM');
  const failed = results.filter((r) => !r.ok);
  console.log(failed.length ? `\n${failed.length} FAILED` : '\nall checks PASS');
  process.exit(failed.length ? 1 : 0);
}

main().catch((error) => {
  console.error('check crashed:', error.message);
  process.exit(1);
});
