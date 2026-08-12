#!/usr/bin/env bash
# Rebuild the F-line PCC streetcar end to end, in the order the gates depend on.
#
#   ./make.sh
#
# BLENDER may point at any Blender 5.x. Intermediates live in build/ and are not
# committed; the committed outputs are f-line.blend, the shipped f-line-pcc.glb,
# validation.json, validation-final.json, shrink-stats.json and renders/.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BLENDER="${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
BUILD="$HERE/build"
mkdir -p "$BUILD" "$HERE/renders"

echo "== 1. build (authored export, one object per component) =="
"$BLENDER" -b --python "$HERE/build_f_line.py" -- --out "$HERE" | grep '^\[build\]'
mv "$HERE/f-line-pcc.authored.glb" "$BUILD/authored.glb"

echo "== 2. contract validation of the AUTHORED export =="
"$BLENDER" -b --python "$HERE/validate_f_line.py" -- \
  --glb "$BUILD/authored.glb" --out "$HERE/validation.json" --stage authored >/dev/null
python3 -c "
import json,sys
d=json.load(open('$HERE/validation.json'))
bad=[k for k,v in d['checks'].items() if not v]
print('   tris',d['triangle_count'],'dims',d['dimensions_m'],'objects',d['object_count'],'->',d['overall'])
print('   Toy_body on',d['tintable_objects'])
sys.exit(1 if bad else 0) or print('   FAILED:',bad)"

echo "== 3. shrink pass (transit README Part 3, ASSET_CLASS=vehicle, 0.05 deg) =="
"$BLENDER" -b --python "$HERE/optimize_f_line.py" -- \
  "$BUILD/authored.glb" "$BUILD/shrunk.glb" "$HERE/shrink-stats.json" \
  | grep -E '^STEP|^bbox_ok|ALARM|HARD FAIL'

echo "== 4. meshopt intake (pipeline/compress-assets.mjs flag set) =="
npx -y gltfpack -i "$BUILD/shrunk.glb" -o "$HERE/f-line-pcc.glb" \
  -cc -kn -km -noq >/dev/null 2>&1
# -km is what stops gltfpack merging materials with identical parameters. If it
# ever ate Toy_body, every PCC in the city would be one colour and nothing else
# would complain - so the material list is read back out of the shipped file
# rather than assumed.
node -e "
const fs=require('fs');
const b=fs.readFileSync('$HERE/f-line-pcc.glb');
const j=JSON.parse(b.slice(20,20+b.readUInt32LE(12)).toString());
const names=j.materials.map(m=>m.name);
console.log('   shipped materials:',names.join(' '));
if(!names.includes('Toy_body')){console.error('   HARD FAIL: -km did not preserve Toy_body');process.exit(1);}
"
for f in "$BUILD/authored.glb" "$BUILD/shrunk.glb" "$HERE/f-line-pcc.glb"; do
  printf '    %8d  %s\n' "$(wc -c <"$f")" "$(basename "$f")"
done

echo "== 5. validation of the SHIPPED file =="
"$BLENDER" -b --python "$HERE/validate_f_line.py" -- \
  --glb "$HERE/f-line-pcc.glb" --out "$HERE/validation-final.json" --stage shipped >/dev/null
python3 -c "
import json,sys
d=json.load(open('$HERE/validation-final.json'))
bad=[k for k,v in d['checks'].items() if not v]
print('   tris',d['triangle_count'],'dims',d['dimensions_m'],'objects',d['object_count'],'->',d['overall'])
sys.exit(1 if bad else 0) or print('   FAILED:',bad)"

echo "== 5b. gate G3: the APP'S OWN loader, with the meshopt decoder =="
# A Blender re-import proves the file is valid glTF; it does not prove
# three.js's GLTFLoader can decode EXT_meshopt_compression, nor that Toy_body
# survives mergeVehicle()'s colour bake at exactly #d8d3c8 - which is the value
# kitfleet.js's per-instance tint multiplies.
node "$HERE/loader_roundtrip.mjs" "$HERE/f-line-pcc.glb" "$HERE/loader-roundtrip.json" \
  | python3 -c "
import json,sys
d=json.load(sys.stdin)
print('   meshopt', d['meshopt_extension'], '| Toy_body baked', d['toy_body_baked_hex'],
      '| reversed meshes', d['negative_volume_meshes_mergeVehicle_would_reverse'],
      '->', 'PASS' if d['pass'] else 'FAIL')"

echo "== 6. review renders from the SHIPPED file =="
node "$HERE/export_city_cell.mjs" >/dev/null
"$BLENDER" -b --python "$HERE/render_f_line.py" -- --glb "$HERE/f-line-pcc.glb" >/dev/null
"$BLENDER" -b --python "$HERE/render_scenarios.py" -- --glb "$HERE/f-line-pcc.glb" \
  | grep -E '^\[scenario\] (in-city|livery)' || true
python3 "$HERE/make_contact_sheet.py"

echo "== done =="
