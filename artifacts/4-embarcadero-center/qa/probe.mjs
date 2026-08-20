// Focused probe: is the 4EC geometry actually IN the landmark batch, and where?
import { spawn } from 'node:child_process';
import { mkdtemp } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import net from 'node:net'; import os from 'node:os'; import path from 'node:path';
const WT='/Users/david_lietjauw/sf-worktrees/4-embarcadero-center';
const sleep=(ms)=>new Promise(r=>setTimeout(r,ms));
const freePort=()=>new Promise(res=>{const s=net.createServer();s.listen(0,()=>{const{port}=s.address();s.close(()=>res(port));});});
const chromeBin='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const appPort=await freePort();
const dev=spawn('npm',['run','dev','--prefix',`${WT}/app`,'--','--port',String(appPort),'--strictPort'],{stdio:['ignore','pipe','pipe']});
await new Promise((res,rej)=>{const t=setTimeout(()=>rej(new Error('dev timeout')),120000);dev.stdout.on('data',d=>{if(String(d).includes('Local:')){clearTimeout(t);res();}});});
const cdp=await freePort(); const dir=await mkdtemp(path.join(os.tmpdir(),'ec4-probe-'));
const chrome=spawn(chromeBin,[`--remote-debugging-port=${cdp}`,`--user-data-dir=${dir}`,'--no-first-run','--no-default-browser-check','--disable-background-timer-throttling','--disable-renderer-backgrounding','--enable-unsafe-swiftshader','--window-size=1600,900','--no-sandbox','--headless=new'],{stdio:'ignore'});
for(let i=0;i<200;i++){try{await fetch(`http://127.0.0.1:${cdp}/json/version`);break}catch{await sleep(300)}}
const v=await (await fetch(`http://127.0.0.1:${cdp}/json/version`)).json();
const ws=new WebSocket(v.webSocketDebuggerUrl); await new Promise((res,rej)=>{ws.onopen=res;ws.onerror=rej});
let id=1;const pend=new Map();let sess=null;const logs=[];
ws.onmessage=e=>{const m=JSON.parse(e.data);
 if(m.id&&pend.has(m.id)){const p=pend.get(m.id);pend.delete(m.id);m.error?p.reject(new Error(m.error.message)):p.resolve(m.result);}
 else if(m.method==='Runtime.consoleAPICalled')logs.push(m.params.args.map(a=>a.value??a.description??'').join(' '));};
const send=(m,p={},s=true)=>new Promise((rs,rj)=>{const i=id++;pend.set(i,{resolve:rs,reject:rj});ws.send(JSON.stringify({id:i,method:m,params:p,sessionId:s?sess:undefined}));setTimeout(()=>{if(pend.has(i)){pend.delete(i);rs({__timeout:true})}},180000);});
const {targetId}=await send('Target.createTarget',{url:'about:blank'},false);
({sessionId:sess}=await send('Target.attachToTarget',{targetId,flatten:true},false));
await send('Runtime.enable');await send('Page.enable');
const ev=async e=>{const r=await send('Runtime.evaluate',{expression:e,awaitPromise:true,returnByValue:true});
 if(r.__timeout)return'__TIMEOUT__'; if(r.exceptionDetails)return'ERR: '+(r.exceptionDetails.exception?.description||r.exceptionDetails.text); return r.result?.value;};
await send('Page.navigate',{url:`http://localhost:${appPort}/?t=${Date.now()}`});
for(let i=0;i<120;i++){if(await ev('!!window.SF'))break;await sleep(2000);}
await ev(`SF.goTo(-122.3961998, 37.7953001, 900, 42, 24)`);
for(let i=0;i<60;i++){if(await ev("SF.assets.placed.has('4EmbarcaderoCenter')")===true)break;await sleep(2000);}
await sleep(6000);
console.log('placed keys:', await ev("JSON.stringify(Object.keys(SF.assets.placed.get('4EmbarcaderoCenter')||{}))"));
console.log('entry:', await ev("JSON.stringify(SF.assets.placed.get('4EmbarcaderoCenter')?.entry)"));
console.log('placement (non-obj):', await ev("JSON.stringify(Object.fromEntries(Object.entries(SF.assets.placed.get('4EmbarcaderoCenter')||{}).map(([k,v])=>[k, (v&&typeof v==='object')?'[obj]':v])))"));
console.log('batch geometry bounds for our instance:', await ev(`(()=>{
  const g=SF.scene.getObjectByName('landmark-assets'); if(!g) return 'no landmark-assets group';
  const bm=g.getObjectByName('landmark-bodies'); if(!bm) return 'no body batch';
  const out={geometries:bm._geometryCount??bm.geometryCount, instances:bm._instanceInfo?bm._instanceInfo.length:'?', visible:bm.visible};
  return JSON.stringify(out);})()`));
console.log('merge lines:', JSON.stringify(logs.filter(l=>/4-embarcadero|batch|overflow|keeping the code-built/i.test(l))));
console.log('all warnings:', JSON.stringify(logs.filter(l=>/warn|error|fail|keeping/i.test(l)).slice(0,10)));
// what is directly above the anchor?
console.log('ray down at anchor:', await ev(`(()=>{
  const T=SF.THREE||window.THREE; 
  const g=SF.scene.getObjectByName('landmark-assets');
  const bm=g&&g.getObjectByName('landmark-bodies');
  if(!bm) return 'no batch';
  bm.computeBoundingBox&&bm.computeBoundingBox();
  const b=bm.geometry.boundingBox;
  return JSON.stringify({batchBox:b?{min:b.min,max:b.max}:null});})()`));
chrome.kill();dev.kill();process.exit(0);
