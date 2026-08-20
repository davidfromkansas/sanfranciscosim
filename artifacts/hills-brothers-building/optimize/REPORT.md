# hills-brothers-building — GLB optimize report (stage 4)

Run 19 Aug 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`
(ASSET_CLASS landmark, ALLOW_MESHOPT yes, ALLOW_BAKE no).
Toolchain: Blender 5.2.0 LTS, gltfpack 0.24 (`-c -km -kn -noq`), pinned-three
g3check, python3 + Pillow.

## Metrics

| | input | shipped | Δ |
|---|---|---|---|
| raw bytes | 752,532 | **266,580** | −65% |
| gzip bytes | 96,486 | 136,340 | +41% (meshopt streams don't gzip; raw is what ships and is the budget metric — ≤ 500 KB ✓) |
| triangles | 10,242 | 10,242 | 0 |
| Blender verts | 19,476 | 6,153 (mid) | weld −68% |
| objects / draw submeshes | 516 / 522 | **13 / 15** | −97% |

Variant table (memory: always measure pack-only):

| variant | raw bytes |
|---|---|
| input | 752,532 |
| pack only | 488,960 |
| Phase B + pack (**shipped**) | **266,580** |

Phase B per-step: weld ≤1 mm −13,323 vert pairs (tris unchanged);
interior-face pass 0; limited dissolve 0.05° **zero savings** (all faces
already minimal quads — kept since it manufactured nothing, verified by the
stage-2 validator on the shipped file); join-per-material 516→13 objects —
the dominant win with meshopt.

## Gates

- **G1** PASS — material set identical (12, glow separate; `-km -kn`).
- **G2** PASS — bbox exact (84.85281/84.85281/53.2), origin exact, all 13
  signed volumes positive, ray flips 0/13,683 (0.0%).
- **G3** PASS — g3check: 15 meshes, 10,242 tris, no decode errors.
- **G4** PASS — A/B day/night × near/far + 4 elevations: mean |ΔRGB|
  day 0.021%/0.015%, night 0.63%/0.49%, elevations ≤ 0.028% (gates 2%/4%);
  night near pair inspected side-by-side — visually identical, no smoothed
  shading from the weld, sign red + arcade white intact.
- **G5** PASS — 522 → 15 submeshes.
- **G6** PASS — 65% raw reduction (> 60% target).
- **G7** n/a (no bake). **G8** PASS — deterministic scripts committed, no
  foreign geometry (re-import counts match), no .blend1.

## Shipping swap

`hills-brothers-building.optimized.glb` copied over
`artifacts/hills-brothers-building/hills-brothers-building.glb`; original
archived at `optimize/input/`. The stage-2 contract validator re-run on the
shipped file: **all checks PASS** (`../validation.json` regenerated).
