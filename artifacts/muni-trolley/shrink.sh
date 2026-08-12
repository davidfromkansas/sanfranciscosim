#!/usr/bin/env bash
# Full reproducible pipeline for muni-trolley-40, ASSET_CLASS=vehicle.
#
#   ./shrink.sh
#
# build/    raw build output (pre-shrink baseline for the before/after table)
# shrunk/   after Stage 2, the geometry shrink pass
# ./*.glb   THE DELIVERABLES: Stage 2 + Stage 1 meshopt intake
#
# The body comes from ../muni-bus/build_muni_bus.py — this asset imports those
# component functions rather than forking them, so a bus rebuild is a trolley
# rebuild. If muni-bus changes, re-run this.
#
# Stage 1 flags are docs/asset-plans/transit/README.md's `-cc -kn -km -noq`.
# -km is load-bearing (without it gltfpack merges materials with identical
# parameters ACROSS the _Glow boundary and silently destroys the night layer);
# -noq is load-bearing (int16 KHR_mesh_quantization corrupts the positions the
# merge paths bake world matrices into).
#
# The high->low texture bake is deliberately NOT run — out of scope for transit
# assets, reason in the README.
set -euo pipefail
cd "$(dirname "$0")"

BLENDER="${BLENDER:-/Applications/Blender.app/Contents/MacOS/Blender}"
mkdir -p build shrunk renders

echo "== build =="
"$BLENDER" -b --python build_muni_trolley.py -- --out build --all-routes 2>&1 | grep -E '^\[build'

cp build/muni-trolley.blend ./muni-trolley.blend

echo "== stage 2: geometry shrink (poles excluded from retessellation) =="
"$BLENDER" -b --python optimize_muni_trolley.py -- \
  --glb build/muni-trolley-40.glb build/muni-trolley-40-22-fillmore.glb \
        build/muni-trolley-40-24-divisadero.glb \
  --out shrunk 2>&1 | grep -E '^\[shrink'

echo "== stage 1: meshopt intake =="
for f in shrunk/*.glb; do
  n="$(basename "$f")"
  npx -y gltfpack -i "$f" -o "./$n" -cc -kn -km -noq
  printf '  %-38s %7d -> %7d bytes\n' "$n" "$(stat -f%z "$f")" "$(stat -f%z "./$n")"
done

echo "== validate the DELIVERABLES (fresh-scene re-import) =="
"$BLENDER" -b --python validate_muni_trolley.py -- \
  --glb muni-trolley-40.glb muni-trolley-40-22-fillmore.glb \
        muni-trolley-40-24-divisadero.glb 2>&1 | grep -E '^\[validate'

echo "== raw glTF check (no Blender axis conversion in the way) =="
node glb_inspect.mjs muni-trolley-40.glb
