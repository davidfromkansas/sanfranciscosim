#!/usr/bin/env bash
# Full reproducible pipeline for muni-bus-40, ASSET_CLASS=vehicle.
#
#   ./shrink.sh
#
# build/    raw build output (pre-shrink baseline for the before/after table)
# shrunk/   after Stage 2, the geometry shrink pass
# ./*.glb   THE DELIVERABLES: Stage 2 + Stage 1 meshopt intake
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
"$BLENDER" -b --python build_muni_bus.py -- --out build --all-routes 2>&1 | grep -E '^\[build'

echo "== stage 2: geometry shrink =="
"$BLENDER" -b --python optimize_muni_bus.py -- \
  --glb build/muni-bus-40.glb build/muni-bus-40-9-san-bruno.glb build/muni-bus-40-43-masonic.glb \
  --out shrunk 2>&1 | grep -E '^\[shrink'

echo "== stage 1: meshopt intake =="
for f in shrunk/*.glb; do
  n="$(basename "$f")"
  npx -y gltfpack -i "$f" -o "./$n" -cc -kn -km -noq
  printf '  %-34s %7d -> %7d bytes\n' "$n" "$(stat -f%z "$f")" "$(stat -f%z "./$n")"
done

echo "== validate the DELIVERABLES (fresh-scene re-import) =="
"$BLENDER" -b --python validate_muni_bus.py -- \
  --glb muni-bus-40.glb muni-bus-40-9-san-bruno.glb muni-bus-40-43-masonic.glb 2>&1 | grep -E '^\[validate'

echo "== raw glTF check (no Blender axis conversion in the way) =="
node glb_inspect.mjs muni-bus-40.glb
