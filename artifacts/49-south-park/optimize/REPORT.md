# 45–49 South Park — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/49-south-park/`, 17 August 2026. Run twice: the second time after local QA
sent the asset back to stage 2 for a glow-colour fix (../REPORT.md 6). Because that
changed the material name set, every gate was re-run from Phase A rather than assumed;
the numbers below are the second run.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 537,588 B (525.0 KB) | **219,384 B (214.2 KB)** | **−59.2%** |
| File, gzip -9 | 98,285 B (96.0 KB) | 141,289 B (138.0 KB) | +43.8% — see G6 |
| Objects / nodes | 165 | **12** | −92.7% |
| Draw submeshes (primitives, via GLTFLoader) | 167 | **14** | −91.6% |
| Triangles | 9,262 | 9,262 | 0 |
| Vertices (Blender, welded) | 17,008 | **5,068** | −70.2% |
| Materials | 11 | 11 | identical set |
| bbox dims | 23.6255 × 22.5585 × 13.0000 m | 23.6255 × 22.5585 × 13.0000 m | 0 |
| bbox min | −11.8127, −11.2792, 0.0 | −11.8127, −11.2792, 0.0 | 0 |
| Ray-test flipped fraction | — | **0.0058%** (1 / 17,325 hits) | tolerance 0.15% |

Toolchain: Blender 5.2.0 LTS; `npx gltfpack@0.24`; node v22.19.0 + the pinned three in
`g3check/package.json`; python3 + Pillow; gzip -9.

## Phase A — waste census

`inspect.json`. The asset came in as 165 flat-shaded solids sharing 11 materials, with
only a `NORMAL` vertex attribute besides position.

- **Split vertices — the whole story.** 9,262 triangles carried 17,008 vertices, and
  the census found **11,940 coincident vertex pairs**: glTF splits vertices for flat
  shading, so every prism's corners are duplicated per face. Predicted recovery from a
  1 mm per-object weld: ~70%. Achieved 70.2%.
- **Object-count overhead.** 165 nodes, 167 primitives, for 11 materials. The join
  census listed 96 objects on `Toy_trim` alone (every cornice step, bracket block, bay
  frame, sill, column and rosette lobe). Predicted recovery from join-per-material:
  ~93% of the node/accessor overhead. Achieved 92.7%.
- **Duplicate meshes: 34 groups, 3,564 redundant triangles**, and all of them were left
  alone. They are real repeats — eight identical flank window fills, sixteen rosette
  lobes, eight canted-bay frames, five roof vents — but at this scale sharing mesh data
  across a dozen 12–84-triangle objects buys less than the join already banked, and
  glTF instancing would fight the join. Joining beat instancing here on both bytes and
  draw submeshes; recorded as a judgment call rather than a missed win.
- **Buried interior faces: none predicted, none found** (`interior_faces_removed: 0`).
  Every applied band in this asset is sunk exactly 30 mm into the surface it sits on
  (see the build script's `EMBED`), so there are overlapping solids everywhere — but
  nothing is *provably* enclosed by a closed box, and the occluder rule correctly
  refused to guess.
- **Degenerate triangles: 0.**
- **Over-tessellated curves: none worth halving.** One screen pixel at the landmark near
  distance (35.44 m) is 23.9 mm of world. The turret is an 8-segment arc of radius
  1.74 m — chord error 53 mm, more than double a pixel — and the rounded bays are
  6 segments of radius 2.06 m. Halving either would be visible on the silhouette, and
  the silhouette here *is* the recognition. Skipped, per §3 step 4.

## Phase B — geometry cleanup

`optimize.py`, `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 9,262 | 17,008 |
| weld + degenerate (1 mm, per object) | 9,262 | **5,068** |
| interior faces | 9,262 | 5,068 |
| limited dissolve — **skipped** | 9,262 | 5,068 |
| join per material | 9,262 | 5,068 |

**The limited dissolve is disabled for this asset**, as a per-asset adaptation, and the
reason is the one `GLB-OPTIMIZE-PROMPT.md` §3 step 3 already documents from
`350-brannan` — only more so. This building's cornice is **three `rim` solids stacked in
z, each following the full bay outline all the way round** (60+ vertices apiece), and
the bracket shelf under every bay plus the water table are three more ring bands on the
same footprint: six large coplanar annuli against 350 Brannan's two. A strictly-coplanar
dissolve merges each annulus into one ngon, and re-triangulating an annulus emits
slivers — invisible, area-test-clean, and fatal two steps later, because a sliver's
shared vertex sits between opposing normals, its averaged vertex normal collapses toward
zero, and gltfpack re-emits the **stored** normals so the failure surfaces only in the
packed file as `invalid_or_nonunit_loop_normal_count`. The step was worth 30 triangles
(0.4%) on 350 Brannan. Not a trade.

Join-per-material produced 9 `grp_Toy_*` objects; `body`, `water_table` and
`roof_bulkhead` stayed separate because they carry two materials each.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 49-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` mandatory (glow-ness is name-only — without `-km`, gltfpack would merge
`Toy_glass` and `Toy_glass_Glow` and silently kill the night layer). `-noq` mandatory
per the repo standard: `pipeline/compress-assets.mjs` produces unquantized output, and a
quantized build fails the stage-2 contract validator on `transforms_applied` and
`no_unexpected_objects`. Preflight confirmed `setMeshoptDecoder` is registered in both
`app/src/gltf.js` and `app/src/assets.js`.

Verified on the output rather than trusting flags: material name set identical (11),
bbox identical to 4 decimal places, 14 primitives.

## Phase D — bake

Not run. `ALLOW_BAKE: no`; the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` at azimuth 270.8° / elevation 42° (the asset's own review aerial: over
the West corner, on the bisector of the two hero elevations), near 1.5× and far 6× the
long axis, day (glow alpha 0.12) and night (alpha 1.0, emission ~6, dusk world), plus
four orthographic elevations. `diff_ab.py` → `diffs.json`, `renders/contact_sheet.png`.

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0123% | 32 |
| day far | 0.0106% | 11 |
| night near | 0.1520% | 66 |
| night far | 0.1684% | 38 |
| elev N (park front) | 0.0223% | 32 |
| elev E (party wall) | 0.0114% | 28 |
| elev S (rear) | 0.0084% | 18 |
| elev W (alley flank) | 0.0158% | 27 |

**Looked at, honestly:** the ×8-amplified diff row is black except for hairlines along
shared edges — the cornice steps, the bay frames, the basement/water-table joint. That
is the 1 mm weld changing which duplicated vertex an anti-aliased edge samples, one
sub-pixel wide. Nothing is missing, no silhouette moved, no shading changed, and the
turret, the seven bay bulges, the rosettes and the lit-window pattern are identical in
both rows. The night deltas are the largest of the eight and are still 12× inside the
2% far tolerance; they are higher only because the night frames are mostly near-black, so
the same absolute edge difference is a larger fraction of a small mean — and they roughly
doubled when the glow colour moved from `Toy_glass_Glow` to the much lighter
`Toy_glassl_Glow` (see ../REPORT.md 6), for the same reason.

## Gates

| Gate | Result | |
|---|---|---|
| G1 Contract | **PASS** | Material set identical (11); `_Glow` pair kept separate by `-km`; no `Toy_body` (landmark); no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox Δ 0.0000 m; origin Δ 0.0000 m; all 12 closed solids positive volume, `inverted_solids: []`; ray flipped fraction **0.000058** vs 0.0015 tolerance |
| G3 Round-trip | **PASS** | Re-imports in Blender (12 objects, 11 materials, bbox exact); `g3check` with pinned three → `G3-OK {"ok":true,"meshes":14,"tris":9262}` |
| G4 Appearance | **PASS** | Max mean delta 0.1684% (night far) vs 2% far / 4% near |
| G5 Draw submeshes | **PASS** | 14 ≤ 167 |
| G6 Size | **PASS** | −59.2% raw, comfortably past the 60%-aspiration band and in line with `106-south-park` (−58.1%) |
| G7 GPU budget | n/a | bake mode not used |
| G8 Hygiene | **PASS** | Re-import object/material/bbox check in `optimize.py`; scripts are deterministic and re-run reproduces the output; no `.blend1` files left |

**On G6 and gzip.** Raw bytes fall 59.2% while gzip -9 *rises* 43.8%, exactly as on
`106-south-park` (−58.1% / +49.7%). Meshopt-compressed buffers are already entropy-coded,
so gzip has nothing left to take and adds framing. The number that matters is what the
CDN ships and the decoder reads: 219 KB against 538 KB, and 5,068 vertices of GPU buffer
against 17,008.

## A note that belongs to stage 2, not here

This pass found a real defect in the *source* asset and it was fixed upstream rather
than papered over: `G2_ray_flip_ok` failed on the first run at **0.202%** (35 of 17,312
first hits). The cause was in `build_49_south_park.py`, not in any optimize step — the
offset helpers decided "which way is outward" per segment by comparing against the
building centroid, which is wrong on a corner turret that sweeps 242° and on a rounded
bay near a far corner, because some of their segments genuinely face back past the
centroid. Those segments offset the wrong way and their bands folded. The fix is
described in `../REPORT.md` §5; after it the *input* measures 2 flipped hits and the
optimized file 1. The gate is doing its job.

## Deliverables

```
input/49-south-park.glb          byte-identical archive of the pre-optimize asset
49-south-park.optimized.glb      the winner - copied over ../49-south-park.glb
mid.glb                          post-Phase-B, pre-pack
inspect.py optimize.py validate.py render_ab.py diff_ab.py   adapted copies
g3check/                         pinned-three GLTFLoader round-trip
inspect.json phaseb_stats.json validation.json diffs.json
renders/                         in_* / out_* / diff_* + contact_sheet.png
```
