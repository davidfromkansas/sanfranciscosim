# 110 The Embarcadero — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/110-embarcadero/`, 19 August 2026. Run **twice**: the second time after
local QA sent the asset back to stage 2 for a glow-colour fix (`../REPORT.md` 11).
Because that changed the material name set, every gate was re-run from Phase A
rather than assumed; the numbers below are the second run.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 320,756 B (313.2 KB) | **144,128 B (140.8 KB)** | **−55.1%** |
| File, gzip -9 | 49,923 B (48.8 KB) | 86,511 B (84.5 KB) | +73.3% — see G6 |
| Objects / nodes | 137 | **13** | −90.5% |
| Draw submeshes (primitives, via GLTFLoader) | 140 | **16** | −88.6% |
| Triangles | 4,944 | 4,944 | 0 |
| Vertices, Blender scene (welded) | 9,940 | **2,756** | −72.3% |
| Vertices, re-imported GLB | 9,940 | 9,020 | −9.3% (see Phase B note) |
| Materials | 10 | 10 | identical set |
| bbox dims | 40.47585 × 40.19234 × 17.40000 m | 40.47585 × 40.19234 × 17.40000 m | 0 |
| bbox min | −20.23793, −20.09617, 0.0 | −20.23793, −20.09617, 0.0 | 0 |
| Ray-test flipped fraction | — | **0.0%** (0 / 14,996 hits) | tolerance 0.15% |

Toolchain: Blender 5.2.0 LTS; `npx gltfpack@0.24`; node v22.19.0 + the pinned
three in `g3check/package.json`; python3 + Pillow; gzip -9.

## Phase A — waste census

`inspect.json`. The asset came in as 137 flat-shaded solids sharing 10
materials, with only a `NORMAL` vertex attribute besides position.

- **Object-count overhead — the whole story here.** 137 nodes and 140
  primitives for 10 materials. The join census listed **66 objects on
  `Toy_trim` alone** (every mullion, transom, modillion, window frame,
  storefront frame, trellis post, planter top, jamb, canopy, fascia and the
  penthouse) and 24 on `Toy_stone`. Predicted recovery from join-per-material:
  ~90% of the node/accessor overhead. Achieved 90.5% (137 → 13).
- **Split vertices.** 4,944 triangles carried 9,940 vertices with **7,184
  coincident vertex pairs** — glTF splits vertices for flat shading, so every
  prism's corners are duplicated per face. A 1 mm per-object weld took the
  Blender scene to 2,756 verts (−72.3%). The exporter then re-splits per face on
  the way out, so the *file's* vertex count only falls to 9,020: the weld's
  value here is that it feeds the joiner clean topology, not that it ships fewer
  vertices. Recorded honestly rather than quoted as a −72% file win.
- **Duplicate meshes: 25 groups, 1,658 redundant triangles**, all left alone.
  They are real repeats — six mullions, nine trellis posts each side, four
  planters, three roof lights, six modillions, four window openings — but at
  12–48 triangles apiece, sharing mesh data buys less than the join already
  banked, and glTF instancing would fight the join. Judgment call, not a missed
  win.
- **Buried interior faces: none predicted, none found.** Every applied band is
  sunk 30 mm into the surface it sits on (`EMBED` in the build script), so
  overlapping solids are everywhere — but nothing is *provably* enclosed by a
  closed box, and the occluder rule correctly refused to guess.
- **Degenerate triangles: 0.**
- **Over-tessellated curves: none.** There are no curves in this asset — it is
  built entirely from extruded rectangles and one triangle (the pediment). One
  screen pixel at the landmark near distance (60.71 m) is 40.9 mm of world;
  nothing to halve.

## Phase B — geometry cleanup

`optimize.py`, `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 4,944 | 9,940 |
| weld + degenerate (1 mm, per object) | 4,944 | **2,756** |
| interior faces | 4,944 | 2,756 |
| limited dissolve — **skipped** | 4,944 | 2,756 |
| join per material | 4,944 | 2,756 |

**The limited dissolve is disabled for this asset**, as a per-asset adaptation,
for the reason `GLB-OPTIMIZE-PROMPT.md` §3 step 3 documents from `350-brannan`.
This building is made of coplanar band runs: the main parapet is three slab runs
plus two `Toy_ink` cap lines round the Embarcadero roof, and the Steuart front
carries a cornice, a cornice cap, a frieze pair, a sill band and a plinth — each
following the full 13.9 m frontage — plus five deck-joint bands and two trellis
rails across the roof. A strictly-coplanar dissolve merges each into one ngon,
and re-triangulating those emits slivers: invisible, area-test-clean, and fatal
two steps later, because a sliver's shared vertex sits between opposing normals,
its averaged vertex normal collapses toward zero, and gltfpack re-emits the
**stored** normals — so the failure surfaces only in the packed file as
`invalid_or_nonunit_loop_normal_count`. Comparable assets measured the step at
~0.4% of triangles. Not a trade.

Join-per-material produced 10 `grp_Toy_*` objects; `body_high`, `setback_glass`
and `plant_screen` stayed separate because they carry two materials each, and
`sign_glow` is a single-face glow quad that the joiner leaves alone.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 110-embarcadero.optimized.glb -c -km -kn -noq
```

`-km -kn` mandatory: glow-ness is name-only, and without `-km` gltfpack would
merge `Toy_glassl` with `Toy_glassl_Glow`, and `Toy_cream_Glow` with nothing else
but `Toy_trim_Glow` is a near neighbour (identical parameters, different names),
and silently kill the night layer. `-noq` mandatory per the repo standard —
`pipeline/compress-assets.mjs` produces unquantized output, and a quantized build
fails the stage-2 contract validator on `transforms_applied` and
`no_unexpected_objects`. Preflight confirmed `setMeshoptDecoder` is registered in
both `app/src/gltf.js` and `app/src/assets.js`.

Verified on the output rather than trusting flags: material name set identical
(10), bbox identical to 5 decimal places, 16 primitives.

**The pack-only control (memory: always measure it).** Running the same gltfpack
line straight on the input, with no Blender round-trip at all, gives
**200,092 B**. Phase B is therefore worth 55,964 B on top of packing — a further
−28.0% — which is the node-and-accessor overhead of 124 extra objects. On this
asset the round-trip pays; that is a measurement, not an assumption, and the
control is recorded so the next asset re-measures rather than inheriting the
conclusion.

## Phase D — bake

Not run. `ALLOW_BAKE: no`; the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` at azimuth 44.83° / elevation 38° (the asset's own review aerial:
from the north-east over The Embarcadero, looking back down the long axis), near
1.5× and far 6× the long axis, day (glow alpha 0.12) and night (alpha 1.0,
emission ≈ 6, dusk world), plus four orthographic elevations. `diff_ab.py` →
`diffs.json`, `renders/ab_review.png`.

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0275% | 29 |
| day far | 0.0222% | 22 |
| night near | 0.1815% | 27 |
| night far | 0.1363% | 91 |
| elev N (Embarcadero front) | 0.0012% | 13 |
| elev E (SE party wall) | 0.0022% | 20 |
| elev S (Steuart front) | 0.0439% | 67 |
| elev W (NW party wall) | 0.0438% | 50 |

**Looked at, honestly:** the ×8-amplified diff column is black except for
hairlines along shared edges — the five deck-joint bands, the trellis posts, the
parapet arrises and the Steuart cornice/frieze joints. That is the 1 mm weld
changing which duplicated vertex an anti-aliased edge samples, one sub-pixel
wide. Nothing is missing, no silhouette moved, no shading changed; the five
curtain-wall bays, the spandrel band, the pediment, the three roof lights, the
planted beds and the lit-window pattern are identical in both rows. The night
deltas are the largest of the eight and still 10× inside the 2% far tolerance;
they are higher only because the night frames are mostly near-black, so the same
absolute edge difference is a larger fraction of a small mean.

## Gates

| Gate | Result | |
|---|---|---|
| G1 Contract | **PASS** | Material set identical (10); `Toy_glassl` / `Toy_glassl_Glow` and `Toy_trim` / `Toy_trim_Glow` kept separate by `-km`; no `Toy_body` (landmark); no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox identical to 5 dp; origin offset 0; all signed volumes positive; ray flipped fraction 0.0% (0 / 14,996) |
| G3 Round-trip | **PASS** | Re-imports in Blender; `g3check` (pinned three) reports `{"ok":true,"meshes":16,"tris":4944}` with all 10 materials and the identical bbox |
| G4 Appearance | **PASS** | Worst delta 0.1815% (night near) against a 4% near / 2% far tolerance; visual review above |
| G5 Draw submeshes | **PASS** | 16 ≤ 140 |
| G6 Size | **PASS** | −55.1% raw. Short of the 60% aspiration because this asset had no geometry waste to remove — 0 degenerate faces, 0 buried faces, no curves to retessellate, and the dissolve was correctly declined. The remainder is silhouette geometry, as the census shows |
| G7 GPU budget | n/a | bake mode not used |
| G8 Hygiene | **PASS** | Re-import object/material/bbox check in `optimize.py`; scripts deterministic and a re-run reproduces the output; no `.blend1` files left |

**On G6 and gzip.** Raw bytes fall 55.1% while gzip -9 *rises* 73.4%, as on every
meshopt-packed asset in this repo (`49-south-park` −59.2% / +43.8%,
`106-south-park` −58.1% / +49.7%). Meshopt-compressed buffers are already
entropy-coded, so gzip has nothing left to take and adds framing. The number that
matters is what the decoder reads: 141 KB against 313 KB, well inside the
500 KB-per-landmark budget.

## The shipping swap

`110-embarcadero.optimized.glb` (144,128 B) was copied over
`artifacts/110-embarcadero/110-embarcadero.glb`; the pre-optimize original is
archived byte-for-byte at `optimize/input/110-embarcadero.glb` (320,756 B,
verified with `cmp`).

The **stage-2 contract validator was then re-run against the packed shipping
file** — not just against the pre-pack asset — because §3 step 3 of the optimize
prompt records that stored-normal defects appear only after packing. It returns
**overall PASS**, all 17 checks green, 13 objects, 4,944 triangles, 20 of 20 glow
faces outward, bbox top exactly 17.400. `../validation.json` and `../REPORT.md`
carry the shipped numbers.

**On the stage-2 review renders.** `../110-embarcadero-*.png` were rendered from
the pre-optimize GLB. They are not re-rendered here because Phase E measured the
two files against each other from the same rig and found a worst-case mean
difference of 0.19% with no missing element and no silhouette change — i.e. the
review images do depict the shipping geometry, to well inside the tolerance the
gate is written to.
