// Stage-5: for every footprint within 14 m of the 164 South Park anchor, print
// which exclusion zone (if any) takes it. This is the check that proves the
// radius drops our own two rings and spares OSM way/124884344, the 76 m2
// `158 South Park` sliver that shares a party-wall vertex with ours.
//
//   cd pipeline && node ../artifacts/164-south-park/integration/which-zone-drops.mjs
//
// Needs pipeline/data/ present. Reads only.

import { createReadStream, existsSync } from 'node:fs';
import { createInterface } from 'node:readline';
import { project } from '../../../pipeline/lib/geo.mjs';
import { ringArea, ringCentroid, simplifyRing } from '../../../pipeline/lib/poly.mjs';
import { streamFeatures, outerRings } from '../../../pipeline/lib/geojsonStream.mjs';
import { exclusionZones } from '../../../pipeline/lib/landmarks.mjs';
const TOL = 0.6, DATA = new URL('../../../pipeline/data/', import.meta.url);
const Z = exclusionZones().map(z => { const [x, zz] = project(z.lon, z.lat); return { id: z.id, x, z: zz, r: z.r, r2: z.r * z.r }; });
const [AX, AZ] = project(-122.3949366, 37.7812097);
function pr(c){const o=[];for(const p of c){if(!Number.isFinite(p[0]))continue;const [x,z]=project(p[0],p[1]);o.push(x,z);}return o;}
function report(ring, tag, src){
  const r = simplifyRing(ring, TOL); if (r.length/2 < 3) return;
  const A = Math.abs(ringArea(r)); if (A < 12) return;
  const [cx,cz]=ringCentroid(r);
  let near = Math.hypot(cx-AX,cz-AZ);
  for(let i=0;i<r.length;i+=2) near = Math.min(near, Math.hypot(r[i]-AX, r[i+1]-AZ));
  if (near > 14) return;
  const hits=[];
  for(const e of Z){
    if((cx-e.x)**2+(cz-e.z)**2 < e.r2){hits.push(`${e.id}(centroid,r=${e.r})`);continue;}
    for(let i=0;i<r.length;i+=2) if((r[i]-e.x)**2+(r[i+1]-e.z)**2<e.r2){hits.push(`${e.id}(vertex,r=${e.r})`);break;}
  }
  console.log(`${src} ${tag} area=${A.toFixed(0)} centroidDist=${Math.hypot(cx-AX,cz-AZ).toFixed(2)} nearest=${near.toFixed(2)} -> ${hits.length?('DROPPED by '+hits.join(', ')):'KEPT'}`);
}
for await (const f of streamFeatures(new URL('buildings_datasf.geojson', DATA).pathname)) {
  const p=f.properties||{};
  for (const ring of outerRings(f.geometry)) { const q=pr(ring); if(q.length>=6) report(q, p.mblr||'?', 'datasf'); }
}
const op=new URL('overture_buildings.geojsonseq',DATA).pathname;
if(existsSync(op)){
  const rl=createInterface({input:createReadStream(op,{encoding:'utf8'}),crlfDelay:Infinity});
  for await (const line of rl){ if(!line.trim())continue; let f; try{f=JSON.parse(line);}catch{continue;}
    const g=f.geometry; if(!g)continue;
    const polys=g.type==='Polygon'?[g.coordinates]:g.coordinates||[];
    for(const poly of polys){ const o=poly&&poly[0]; if(!o||o.length<4)continue;
      if(Math.abs(o[0][0]+122.3949)>0.001||Math.abs(o[0][1]-37.7812)>0.001) continue;
      const q=pr(o); if(q.length>=6) report(q,(f.id||'').slice(0,12),'overture'); } }
}
