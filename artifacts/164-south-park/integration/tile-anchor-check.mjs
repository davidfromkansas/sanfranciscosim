// Stage-5: decode the committed building tiles around 164 South Park and report
// whether any baked ring COVERS the anchor, before (origin/main) and after the
// re-bake.
//
// This exists because verify-rebake.mjs compares per-cell COUNTS, and on a bake
// whose pipeline/data snapshot differs in vintage from the reference's, one
// footprint dropped and one appeared cancel out — it then reports
// "exclusion dropped nothing" for a landmark whose exclusion worked perfectly.
// Counts cannot see identities; point-in-polygon can.
//
//   cd pipeline && node ../artifacts/164-south-park/integration/tile-anchor-check.mjs
//
// Reads only.

import { execFileSync } from 'node:child_process';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { project } from '../../../pipeline/lib/geo.mjs';
const REPO = fileURLToPath(new URL('../../../', import.meta.url));
function footprints(buf){
  const dv=new DataView(buf.buffer,buf.byteOffset,buf.byteLength);
  const version=dv.getUint16(4,true), count=dv.getUint32(8,true), vertexTotal=dv.getUint32(12,true);
  const originX=dv.getFloat32(20,true), originZ=dv.getFloat32(24,true), quant=dv.getFloat32(28,true);
  let off=32; const vertOffsetAt=off; off+=4*count; off+=4*count;
  const vertCountAt=off; off+=2*count; off+=2*count;
  const baseYAt=off; off+=2*count; const topYAt=off; off+=2*count; off+=2*count;
  if(version>=2) off+=2*count; if(version>=3) off+=3*count;
  off=Math.ceil(off/2)*2; const vertsAt=off;
  const out=[];
  for(let i=0;i<count;i++){
    const vo=dv.getUint32(vertOffsetAt+4*i,true), vc=dv.getUint16(vertCountAt+2*i,true);
    const ring=[];
    for(let k=0;k<vc;k++){const p=vertsAt+(vo+k)*4; ring.push([originX+dv.getInt16(p,true)*quant, originZ+dv.getInt16(p+2,true)*quant]);}
    out.push({ring,height:(dv.getInt16(topYAt+2*i,true)-dv.getInt16(baseYAt+2*i,true))/10});
  }
  return out;
}
const inside=(p,r)=>{let c=false;for(let i=0,j=r.length-1;i<r.length;j=i++){const [xi,yi]=r[i],[xj,yj]=r[j];if((yi>p[1])!==(yj>p[1])&&p[0]<(xj-xi)*(p[1]-yi)/(yj-yi)+xi)c=!c;}return c;};
const A=project(-122.3949366,37.7812097);
const cells=['23_13','23_12','22_13','24_13','23_14'];
for(const rev of ['origin/main','WORKING']){
  let hits=0, total=0;
  for(const c of cells){
    let buf;
    try{ buf = rev==='WORKING' ? readFileSync(`${REPO}/app/public/tiles/buildings/${c}.bin`)
                               : execFileSync('git',['show',`origin/main:app/public/tiles/buildings/${c}.bin`],{cwd:REPO,maxBuffer:1<<28}); }
    catch{ continue; }
    const fps=footprints(buf); total+=fps.length;
    for(const f of fps){
      if(inside(A,f.ring)) { hits++; console.log(`${rev} ${c}: RING COVERS ANCHOR height=${f.height.toFixed(1)} m verts=${f.ring.length}`); }
      else {
        let d=1e9; for(const v of f.ring) d=Math.min(d,Math.hypot(v[0]-A[0],v[1]-A[1]));
        if(d<6) console.log(`${rev} ${c}: ring within ${d.toFixed(2)} m of anchor, height=${f.height.toFixed(1)}`);
      }
    }
  }
  console.log(`${rev}: ${total} footprints in ${cells.length} cells, ${hits} covering the anchor`);
}
