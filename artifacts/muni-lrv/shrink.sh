#!/usr/bin/env bash
# Build -> Stage 2 geometry shrink -> Stage 1 meshopt intake -> validate.
#
#   ./shrink.sh
#
# ASSET_CLASS=vehicle, per docs/asset-plans/transit/README.md Part 3.
# The shipped deliverable is ./muni-lrv.glb; build/ and shrunk/ are the
# intermediates kept so every number in REPORT.md can be re-derived.
set -euo pipefail
cd "$(dirname "$0")"

BLENDER=${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}
mkdir -p build shrunk renders

echo "== build =="
"$BLENDER" -b --python build_muni_lrv.py -- --out build | grep -E '^\[build'

echo "== stage 2: geometry shrink =="
"$BLENDER" -b --python optimize_muni_lrv.py -- \
  --in build/muni-lrv.glb --out shrunk/muni-lrv.glb --json shrink.json \
  | grep -E '^\[shrink'

echo "== stage 1: meshopt intake =="
# -cc -kn -km -noq, the transit README's flag set.
#   -km is load-bearing: without it gltfpack merges materials with identical
#      parameters across the _Glow boundary and silently destroys the night layer.
#   -noq is load-bearing: int16 KHR_mesh_quantization corrupts the positions the
#      app's merge paths bake world matrices into.
#   -kn is load-bearing HERE specifically: it preserves the LRV_Section_A/B and
#      LRV_Bellows node names a future articulation runtime needs.
npx -y gltfpack -i shrunk/muni-lrv.glb -o muni-lrv.glb -cc -kn -km -noq

echo "== verify -kn preserved the section node names =="
node -e '
const fs=require("fs");
const b=fs.readFileSync("muni-lrv.glb");
const jl=b.readUInt32LE(12);
const j=JSON.parse(b.slice(20,20+jl).toString("utf8"));
const names=(j.nodes||[]).map(n=>n.name).filter(Boolean);
const need=["LRV_Section_A","LRV_Section_B","LRV_Bellows"];
const missing=need.filter(n=>!names.includes(n));
console.log("[intake] nodes:", names.join(", "));
console.log("[intake] materials:", j.materials.map(m=>m.name).join(", "));
console.log("[intake] extensions:", (j.extensionsUsed||[]).join(", "));
if(missing.length){console.error("[intake] FAIL missing nodes:",missing);process.exit(1);}
console.log("[intake] PASS section node names survived -kn");
'

echo "== validate the shipped GLB =="
"$BLENDER" -b --python validate_muni_lrv.py -- \
  --glb muni-lrv.glb --out validation.json | grep -E '^\[validate'

ls -l build/muni-lrv.glb shrunk/muni-lrv.glb muni-lrv.glb
