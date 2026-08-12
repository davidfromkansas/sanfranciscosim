#!/usr/bin/env bash
# Rebuild the Powell cable car end to end, in the order the gates depend on.
#
#   ./make.sh
#
# BLENDER may point at any Blender 5.x. Intermediates live in build/ and are
# not committed; the committed outputs are cable-car.blend, the shipped
# cable-car-powell.glb, validation.json, validation-final.json,
# shrink-stats.json and renders/.
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
BLENDER="${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
BUILD="$HERE/build"
mkdir -p "$BUILD" "$HERE/renders"

echo "== 1. build (authored export, one object per component) =="
"$BLENDER" -b --python "$HERE/build_cable_car.py" -- --out "$HERE" | grep '^\[build\]'
mv "$HERE/cable-car-powell.authored.glb" "$BUILD/authored.glb"

echo "== 2. contract validation of the AUTHORED export =="
"$BLENDER" -b --python "$HERE/validate_cable_car.py" -- \
  --glb "$BUILD/authored.glb" --out "$HERE/validation.json" --stage authored >/dev/null
python3 -c "
import json,sys
d=json.load(open('$HERE/validation.json'))
bad=[k for k,v in d['checks'].items() if not v]
print('   tris',d['triangle_count'],'dims',d['dimensions_m'],'objects',d['object_count'],'->',d['overall'])
sys.exit(1 if bad else 0) or print('   FAILED:',bad)"

echo "== 3. shrink pass (transit README Part 3, ASSET_CLASS=vehicle) =="
"$BLENDER" -b --python "$HERE/optimize_cable_car.py" -- \
  "$BUILD/authored.glb" "$BUILD/shrunk.glb" "$HERE/shrink-stats.json" \
  | grep -E '^STEP|^bbox_ok|ALARM|HARD FAIL'

echo "== 4. meshopt intake (pipeline/compress-assets.mjs flag set) =="
npx -y gltfpack -i "$BUILD/shrunk.glb" -o "$HERE/cable-car-powell.glb" \
  -c -km -kn -noq >/dev/null 2>&1
ls -l "$BUILD/authored.glb" "$BUILD/shrunk.glb" "$HERE/cable-car-powell.glb" | awk '{print "   ",$5,$9}'

echo "== 5. validation of the SHIPPED file =="
"$BLENDER" -b --python "$HERE/validate_cable_car.py" -- \
  --glb "$HERE/cable-car-powell.glb" --out "$HERE/validation-final.json" --stage shipped >/dev/null
python3 -c "
import json,sys
d=json.load(open('$HERE/validation-final.json'))
bad=[k for k,v in d['checks'].items() if not v]
print('   tris',d['triangle_count'],'dims',d['dimensions_m'],'objects',d['object_count'],'->',d['overall'])
sys.exit(1 if bad else 0) or print('   FAILED:',bad)"

echo "== 6. review renders from the SHIPPED file =="
node "$HERE/export_city_cell.mjs" >/dev/null
"$BLENDER" -b --python "$HERE/render_cable_car.py" -- --glb "$HERE/cable-car-powell.glb" >/dev/null
"$BLENDER" -b --python "$HERE/render_scenarios.py" -- --glb "$HERE/cable-car-powell.glb" \
  | grep '^\[scenario\] tilted' || true
python3 "$HERE/make_contact_sheet.py"

echo "== done =="
