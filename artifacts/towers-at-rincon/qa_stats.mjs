import { spawn } from 'node:child_process';
const CHROME='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const PORT=9334;
const chrome=spawn(CHROME,[`--remote-debugging-port=${PORT}`,'--headless=new','--window-size=1600,1000',
 '--disable-backgrounding-occluded-windows','--disable-renderer-backgrounding','--disable-background-timer-throttling',
 '--use-gl=angle','--enable-unsafe-swiftshader','--user-data-dir=/tmp/r88/chromeprofile2','about:blank'],{stdio:'ignore'});
const sleep=ms=>new Promise(r=>setTimeout(r,ms));
let wsUrl; for(let i=0;i<60;i++){try{const r=await fetch(`http://127.0.0.1:${PORT}/json/version`);if(r.ok){wsUrl=(await r.json()).webSocketDebuggerUrl;break}}catch{}await sleep(500)}
const {default:WS}=await import('ws');
const ws=new WS(wsUrl); await new Promise(r=>ws.on('open',r));
let id=0;const pend=new Map();
ws.on('message',m=>{const d=JSON.parse(m);if(d.id&&pend.has(d.id)){pend.get(d.id)(d);pend.delete(d.id)}});
const send=(method,params={},sessionId)=>new Promise(res=>{const i=++id;pend.set(i,res);ws.send(JSON.stringify({id:i,method,params,sessionId}))});
const {result:{targetId}}=await send('Target.createTarget',{url:process.argv[2]});
const {result:{sessionId}}=await send('Target.attachToTarget',{targetId,flatten:true});
const ev=async e=>{const r=await send('Runtime.evaluate',{expression:e,awaitPromise:true,returnByValue:true},sessionId);
  if(r.result?.exceptionDetails)return{err:r.result.exceptionDetails.exception?.description||r.result.exceptionDetails.text};return r.result?.result?.value};
await sleep(9000);
await ev(`(async()=>{for(let i=0;i<80&&!window.SF;i++)await new Promise(r=>setTimeout(r,300));SF.boot.reveal('qa');return 1})()`);
// Street level in the Mission and downtown are the stress cells per AGENTS rule 2.
for (const [name, lon, lat, dist, pitch] of [
  ['towers-at-rincon', -122.3924907, 37.791991, 620, 22],
  ['towers-street', -122.3924907, 37.791991, 190, 8],
  ['downtown-street', -122.4009, 37.7899, 190, 8],
  ['mission-street', -122.4180, 37.7599, 190, 8],
]) {
  await ev(`SF.goTo(${lon}, ${lat}); SF.rig.state.distance=${dist}; SF.rig.state.pitch=${pitch}; true`);
  await sleep(9000);
  // Read the app's OWN overlay, not renderer.info sampled from a rAF callback:
  // main.js reads renderer.info inside its frame, after render(), and three
  // resets those counters every frame — sampling from an outside callback lands
  // before the draw and reports 1 call / 2 triangles for a full city.
  // The overlay is #debug, unhidden by F3 on the WINDOW keydown listener.
  await ev(`(()=>{document.getElementById('debug').hidden=false;return 1})()`);
  await sleep(4000);
  const s = await ev(`(()=>{const t=document.getElementById('debug').textContent||'';
    const g=(re)=>{const m=t.match(re);return m?m[1]:null};
    return {fps:g(/fps\\s+(\\S+)/), drawCalls:g(/draw calls\\s+(\\S+)/), triM:g(/triangles\\s+(\\S+)/), tiles:g(/tiles\\s+(\\S+)/)};})()`);
  console.log(name, JSON.stringify(s));
}
ws.close(); chrome.kill();
