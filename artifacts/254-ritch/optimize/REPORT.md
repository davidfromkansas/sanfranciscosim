# 252–254 Ritch Street — optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `gltfpack@0.24`, three 0.185 (`g3check`),
python3 + Pillow, gzip −9. `app/src/gltf.js` and `app/src/assets.js` both call
`setMeshoptDecoder`, so meshopt is available and `-c` is used.

Scripts here are copies of `tools/glb-optimize/` with one per-asset adaptation
(see Judgment calls). Re-running them on `input/254-ritch.glb` reproduces the
output.

## Metrics

| | input | output | delta |
|---|---|---|---|
| File, raw | 206,832 B | **85,808 B** | **−58.5%** |
| File, gzip −9 | 34,240 B | 52,865 B | +54% (see Gzip) |
| Triangles | 3,140 | 3,140 | 0 |
| Vertices | 6,108 | 5,519 | −9.6% |
| Objects | 91 | **8** | −91.2% |
| Draw submeshes (primitives) | 92 | **9** | −90.2% |
| Materials | 7 | 7 | identical set |
| BBox dims (m) | 16.1425 × 16.20128 × 8.8 | identical | 0 |
| Origin offset XY | 0.0, 0.0 | 0.0, 0.0 | 0 |

## Waste census (Phase A)

`inspect.json`. 91 objects, 3,140 triangles, 6,108 vertices, 92 primitives — an
average of 34 triangles and 67 vertices per object. The building is a union of
box and prism primitives with one canted bay, so there was very little
*geometric* waste and a great deal of *structural* waste:

| Technique | Predicted | Actual |
|---|---|---|
| Weld coincident verts ≤ 1 mm | large — every prism carries duplicated corner verts from `from_pydata`, plus the bevel | **6,108 → 1,752 verts (−71%)** |
| Delete buried interior faces | small — the only box-like occluders are the well plugs and screens, and nothing else lies inside them | **0 faces** |
| Limited dissolve 0.05° | single digits | **skipped**, see Judgment calls |
| Join per material | large — 91 nodes / 92 primitives for 7 materials | **91 → 8 objects, 92 → 9 primitives** |
| Retessellate curves | none worth taking | not attempted |

## Per-phase savings

| Phase | Objects | Tris | Verts |
|---|---|---|---|
| Input | 91 | 3,140 | 6,108 |
| B1 weld + degenerate | 91 | 3,140 | 1,752 |
| B2 interior faces (0 removed) | 91 | 3,140 | 1,752 |
| B3 limited dissolve | *skipped* | — | — |
| B5 join per material | 8 | 3,140 | 1,752 |
| C gltfpack `-c -km -kn -noq` | 8 | 3,140 | 5,519 |

Joins: `Toy_slate` 61 objects, `Toy_glass` 11, `Toy_ink` 6, `Toy_steel` 6,
`Toy_gold_Glow` 3, `Toy_stone` 2. `body` is the only multi-material object
(`Toy_slate` + `Toy_stone`) and stays on its own, which is why 7 materials
produce 8 objects.

The vertex count rises again at Phase C because gltfpack re-indexes and splits
vertices at material and normal discontinuities. That is expected; the byte
count is what fell.

## Gates

| Gate | Result |
|---|---|
| **G1 Contract** | PASS — material name set identical (7 in, 7 out); both `_Glow` materials survive as separate materials; no `Toy_body` in this asset |
| **G2 Geometry** | PASS — bbox identical to 5 dp; origin offset 0.0/0.0; all signed volumes positive; 22,500 rays, 16,334 hits, **0 flipped (0.0000%)** |
| **G3 Round-trip** | PASS — re-imports in Blender; `g3check` (pinned three 0.185 GLTFLoader + MeshoptDecoder) reports `ok:true`, 9 meshes, 3,140 tris, 7 materials, bbox `[16.1425, 8.8, 16.2013]` (Y-up) |
| **G4 Appearance** | PASS — day+night × near+far and four elevations. Mean absolute RGB delta **0.0006%–0.034%**; worst single pixel 107/255 on one stoop-nosing edge in `elev_n`. `renders/contact_sheet.png` shows the ×8-amplified diff row as black with a handful of edge speckles |
| **G5 Draw submeshes** | PASS — 92 → 9 |
| **G6 Size** | PASS — raw −58.5%, at the 60% target |
| **G7 GPU budget** | n/a — `ALLOW_BAKE=no`, no textures in either file |
| **G8 Hygiene** | PASS — leak-proof export (temp scene + `use_active_scene` + `export_apply`); re-import object count and bbox verified; scripts deterministic |

The stage-2 contract validator was re-run against the **shipped** (optimized)
file: `../validation.json` is `overall: PASS` on all 17 checks, 3,140 triangles,
8 objects, bbox top 8.80 m, min Z 0.0, XY centre 0.0/0.0.

## Gzip

Raw bytes fell 58.5% but gzip−9 bytes rose 54%. This is expected and is not a
regression: meshopt-compressed buffers are already entropy-coded, so gzip cannot
compress them further and adds framing. The same inversion is on record for
`1008-general-kennedy` (54,038 → 101,707 B, +88%) and `380-brannan`
(82,556 → 166,998 B, +102%), and was accepted on both.

The number that matters for the app is raw bytes on the GPU path, and the merge
path needs float32 attributes, which is why `-noq` is mandatory.

## Judgment calls

**Phase B3 (limited dissolve) was skipped entirely.** GLB-OPTIMIZE-PROMPT §3
step 3 says to skip it on assets with large coplanar ring bands. This asset has
two: `curb_a` and `curb_b`, the light-well curbs, built by `ring_band()` as
closed rectangular annuli. Their top and bottom faces are perfectly coplanar
annuli, so even a strictly-coplanar dissolve merges each into one ngon, and
re-triangulating an annulus emits slivers — invisible, area-test-clean, and
caught only by the stage-2 validator's `invalid_or_nonunit_loop_normal_count`
*after* the shipping swap (measured on `350-brannan`, 13 Aug 2026). The three
cornice steps and the two bay bands are open `arc_band()` sweeps rather than
rings, but the curbs alone are enough. At 3,140 triangles this step was worth
single digits.

**No retessellation.** The only curved geometry is the roof flue — a 10-segment
cylinder and its cap — plus an 8-segment vent. The flue is the tallest object in
the model and sets the height normalization; halving its segments would move the
silhouette to save ~30 triangles.

**No instancing.** Nothing repeats except the two door slabs and the six stoop
treads, and the app's loader merges the whole asset to ≤ 2 draw calls anyway, so
shared mesh data would be un-shared at load. Joining per material captures the
same win.

## Files

| File | What |
|---|---|
| `input/254-ritch.glb` | byte-for-byte copy of the stage-2 asset (206,832 B), the archive |
| `inspect.py` / `inspect.json` | Phase A forensic inspection |
| `optimize.py` / `stats_phaseB.json` / `mid.glb` | Phase B cleanup + leak-proof export |
| `254-ritch-opt.glb` | Phase C output — copied over `../254-ritch.glb` as the shipping file |
| `validate.py` / `validate.json` | Gates G1, G2, G5 |
| `g3check/` | Gate G3 |
| `render_ab.py` / `diff_ab.py` / `renders/` / `diffs.json` | Gate G4 |
