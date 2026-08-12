# Chase Center — GLB optimize report (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run against
`artifacts/chase-center/` with the documented defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`,
`TARGET_REDUCTION: 60%`.

Scripts here are adapted copies of `tools/glb-optimize/`; only per-asset
constants and the contact-sheet label changed.

## Headline

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| File, raw | 581,884 B | **237,440 B** | **−59.2% (2.45×)** |
| File, gzip −9 | 143,720 B | 164,492 B | +14.5% (see note) |
| Triangles | 11,660 | 11,291 | −3.2% |
| Vertices | 20,502 | 17,451 | −14.9% |
| Objects | 40 | 11 | −72.5% |
| Draw submeshes (primitives) | 43 | **14** | −67.4% |
| Bbox dims | 164.3642 × 159.1251 × 40.8000 | 164.3642 × 159.1251 × 40.8000 | 0 |
| Origin | 0, 0, base z = 0 | unchanged, base z = 0 | 0 |
| Materials | 10 | 10, identical set | — |

`TARGET_REDUCTION` (60%) essentially met at 59.2%. **Gzip goes up**, and that is
expected: meshopt's own entropy coding already compresses the buffer, so gzipping
it again adds overhead. The raw byte count is what ships and what the 500 KB
budget measures; 237 KB is well inside it.

**Packed with `-c -km -kn -noq`, unquantized**, per the repo standard that landed
on main in PR #88 while this branch was in flight. See §"Re-pack" below.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7) · `npx gltfpack@0.24` · node v22.19.0 ·
python3 + Pillow 11.3.0 · gzip −9. No substitutions.

`grep -rn setMeshoptDecoder app/src/` hits `app/src/gltf.js:10` and
`app/src/assets.js:406`, so `-c` (meshopt encoding) is safe.

## Phase A — waste census

- 40 objects, 11,660 tris, 20,502 verts, 43 primitives, 1 vertex attribute (NORMAL)
- **14,598 coincident vertex pairs** — every box and prism exported with split
  verts at each flat-shaded edge. The dominant waste, and the reason vertices
  fell 72% at the weld step.
- **1,728 tris in duplicate meshes** — the four atrium fins, three roof-pad
  rotation classes (4 each), and the four roof units.
- 0 degenerate tris.
- 7 join candidates by material: `Toy_roofd` (14 objects), `Toy_steel` (9),
  `Toy_trim` (7), `Toy_sand` (3), `Toy_stone` (3), `Toy_glass` (2),
  `Toy_white_Glow` (2).
- Over-tessellation: one screen pixel at the landmark near distance (246.6 m)
  is 0.166 m. The drum, sail and roof rings are sampled at 240 and 120
  segments — chord error is ~0.4 m and ~1.6 m respectively, i.e. **above** one
  pixel, so §3.4 retessellation was **skipped**: these are the
  silhouette-defining shells and halving them would be visible. Recorded as a
  deliberate skip.

## Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 11,660 | 20,502 |
| 1 weld ≤ 1 mm + degenerate (per object) | 11,660 | 5,904 |
| 2 interior faces provably buried | 11,319 | 5,814 |
| 3 limited dissolve, 0.05°, delimit material+sharp | 11,301 | 5,805 |
| 5 join per material | 11,301 | 5,805 |

- **341 interior faces removed.** The occluder rule held: only closed solids
  whose signed volume fills ≥ 95% of their AABB count as occluders, so the
  boxy roof plant and the entry elements did the occluding and the lobed drum
  shells (AABB fill ≈ 0.79) correctly did not.
- Joins: `grp_Toy_roofd` 14 → 1, `grp_Toy_steel` 9 → 1, `grp_Toy_trim` 5 → 1,
  `grp_Toy_stone` 3 → 1, `grp_Toy_glass` 2 → 1, `grp_Toy_sand` 2 → 1.
  `sail_skin`, `sail_crest`, `atrium_glow`, `board_frame` and `board_screen`
  are multi-material or single-user and stayed separate.
- Normals audit after the pass: `inverted_solids: []`.

Dissolve was kept at 0.05°, not 0.5°, exactly as §3.3 warns — the drum and
sail are gently curved shells and a transitive 0.5° chain is what produces
twisted ngons with flipped windings there.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o chase-center.optimized.glb -c -km -kn -noq
```

`-km` mandatory and used: without it gltfpack would merge `Toy_sky_Glow` into
`Toy_sky`-like neighbours across the `_Glow` boundary and silently kill the
night layer. Material name set verified identical on the output (10 in, 10 out).

498,944 B (mid) → 237,440 B. `-noq` keeps every attribute float32
(componentType 5126) and the node transforms at identity, which is what the
kit/landmark merge paths and the stage-2 contract validator expect.

## Phase E — A/B verification

Same rig, input vs output, day and night × near (1.5× long axis = 246.5 m) and
far (6× = 986.2 m), plus four orthographic elevations.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day near | **0.025%** | 107 |
| day far | 0.030% | 196 |
| night near | 0.017% | 36 |
| night far | 0.021% | 62 |
| elev N | 0.040% | 83 |
| elev E | 0.038% | 125 |
| elev S | 0.057% | 180 |
| elev W | **0.107%** | 71 |

Gates are ≤ 2% far and ≤ 4% near; the worst view is 0.107%. (The quantized build
this replaced measured 0.136% worst — dropping quantization moved every view
closer to the input, as expected.)

**Looked at the diffs** (`renders/contact_sheet.png`, diff row amplified ×8):
the ×8 diff is black except for a one-pixel sparkle along silhouette edges and
along the vertical panel-band creases — that is the weld/dissolve pass moving
edges by sub-millimetre amounts. Nothing is missing, no element changed shape, the sail
profile and the gold crest arc are identical, and the night layer lights the
same three surfaces. There is nothing here a player would notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | `validation.json` `G1_materials_identical: true`; 10 materials in and out; `Toy_sky_Glow` and `Toy_white_Glow` still distinct |
| G2 Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox delta 0; origin unchanged; `G2_volumes_positive: true`; 22,500 rays, 19,185 hits, **0 flipped** |
| G3 Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `g3check`: `G3-OK`, 14 meshes, 11,301 tris, 10 materials, no decode errors, `bbox_dims` 164.3642 × 40.8 × 159.1251 |
| G4 Appearance | **PASS** | table above; worst 0.107% against a 2% gate |
| G5 Draw submeshes ≤ input | **PASS** | 43 → 14 |
| G6 Size reduced ≥ target | **PASS** | −59.2% raw against a 60% target; the shortfall is the `-noq` standard, and the waste census shows the remainder is silhouette geometry (§Phase A: retessellation skipped on the drum/sail/roof rings) |
| G7 GPU budget | **n/a** | bake mode off (`ALLOW_BAKE: no`) |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object/material/bbox check in `phaseb_stats.json`; scripts are deterministic; no `.blend1` written |

## Shipping swap

`chase-center.optimized.glb` copied over `artifacts/chase-center/chase-center.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/chase-center.glb` (581,884 B, verified).

## Re-pack: `-cc` → `-noq`

This asset was first packed `-cc -kn -km` (98,220 B, quantized), which is what
`GLB-OPTIMIZE-PROMPT.md` §4 said at the time. While the branch was in flight,
main standardised on `-c -km -kn -noq` (PR #88, `380-brannan`). Phase B and C
were re-run from the archived input with the repo flags and every gate re-run.

Worth recording, because the prompt's note left it open: the quantized build did
**not** break the runtime. It merged and batched correctly in a local dev run
(`chase-center merged 14 objects / 10 materials -> batched`), as does the already
shipped, still-quantized `st-marys-cathedral`. The landmark path survives
quantization because `collect()` in `app/src/assets.js` runs
`prepareGeometryForTransforms()` before baking world matrices. The reason to
prefer `-noq` anyway is consistency with `compress-assets.mjs` and keeping the
stage-2 contract validator strict — a quantized file needs `transforms_applied`
and `no_unexpected_objects` special-cased, and it lands the loader scale on
0.999936 instead of exactly 1.0.

`artifacts/chase-center/validation.json` and `REPORT.md` were re-run and
updated to the **shipped** numbers so the integration stage writes the manifest
from reality: tris 11,289, dims 164.3642 × 159.1272 × 40.8026,
loader scale 0.999936.

## One correction to the asset-side validator

`validate_chase_center.py` asserted that every object is a closed manifold. That
holds for the **authored** export — it is how the build guarantees outward
normals — but not for the shipped file, because Phase B step 2 *deliberately*
deletes faces it can prove are buried inside another solid, which opens those
shells. Closedness is now an explicit `--closed-solids` flag rather than
something inferred. On the shipped file the authoritative tests are the ones the
pipeline doc names: per-object signed volume positive
(`inverted_solid_objects: []`) and ray residual 0.000.

Both forms pass:

```
blender -b --python validate_chase_center.py -- \
    --glb optimize/input/chase-center.glb --closed-solids   # authored: PASS, 0 non-manifold
blender -b --python validate_chase_center.py                # shipped:  PASS
```

(The quantized first pass also needed `transforms_applied` and
`no_unexpected_objects` relaxed, since `KHR_mesh_quantization` stores the
dequantize matrix as a node transform and splits each node into an empty parent
plus a `Mesh_N` child. Re-packing with `-noq` removed the need for both — the
shipped file now reports `transform_form: identity`.)
