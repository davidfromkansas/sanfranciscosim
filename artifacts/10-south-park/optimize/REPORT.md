# 10 South Park — optimize report (stage 4)

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 on `artifacts/10-south-park/`
with the defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`. Scripts here are adapted copies of `tools/glb-optimize/`.

**Result: every gate passes; the optimized file is now the shipping file.** The
pre-optimize asset is archived byte-for-byte at `input/10-south-park.glb`.

## Metrics

| | input | shipped | delta |
|---|---|---|---|
| raw bytes | 769,304 | **361,604** | **−53.0 %** |
| gzip-9 bytes | 127,947 | 213,814 | +67 % — see the note below |
| objects | 258 | **13** | −94.9 % |
| draw submeshes (primitives) | 261 | **14** | −94.6 % |
| triangles | 11,976 | 11,976 | 0 |
| vertices | 24,806 | **6,488** | −73.8 % |
| materials | 12 | 12 | 0 |
| bbox | 39.9401 × 35.9952 × 14.67 | identical to 4 dp | 0 |
| origin | 0.000, 0.000, base z 0 | identical | 0 |

**The gzip line is not a regression, and it is the expected shape of this
change.** Meshopt-compressed buffers are already entropy-coded, so they gzip
poorly, while the input was mostly raw float32 arrays that gzip very well. Every
shipped landmark in this repo has the same profile — the 90 files in
`app/public/sf-assets/landmarks/` have a median gzip/raw ratio of 0.64, and this
asset lands at 0.59, between `501-second` (487 KB raw / 198 KB gzip) and
`101-south-park` (192 / 145). Meshopt is not optional here: `AGENTS.md` §"Ship
step" requires every GLB entering `app/public/sf-assets/` to be meshopt-packed by
`pipeline/compress-assets.mjs`, which runs the same `-c -km -kn -noq`. Both
numbers are comfortably inside the ≤ 500 KB per-landmark budget.

## Waste census (Phase A, `inspect.json`)

| finding | measure | acted on |
|---|---|---|
| coincident vertex pairs | **18,318** | yes — per-object weld at 1 mm, the single biggest win |
| object-count overhead | 258 objects across 12 materials; `Toy_sand` alone on 126 | yes — join per material |
| duplicate mesh groups | 61 groups, 5,788 redundant triangles | not separately — the per-material join absorbs them; no manifest node names and no `Toy_body` here, so nothing had to stay addressable |
| degenerate triangles | 0 | n/a |
| interior faces buried in a closed solid | 0 removable | no — the front block is a notched prism whose AABB fill is far under 95 %, so it is correctly not treated as an occluder |
| over-tessellated curves | one-pixel world size 0.0404 m at the 59.9 m near distance | no — the four bowed-frontage facets, the two oval rings and the pond/tree rings are all silhouette or ornament at that distance |
| textures | none | n/a |

## Phase B — geometry cleanup

| step | tris | verts |
|---|---|---|
| in | 11,976 | 24,806 |
| 1. weld ≤ 1 mm + delete degenerate | 11,976 | **6,488** |
| 2. interior faces | 11,976 | 6,488 |
| 3. limited dissolve | **skipped** | — |
| 5. join per material | 11,976 | 6,488 |

**Step 3 was skipped deliberately**, per §3 step 3 of the prompt: skip on assets
with large coplanar ring bands. This asset has **four** — `front_parapet`,
`front_cap`, `rear_parapet`, `rear_cap`, each an annulus following its block's
whole footprint (576 + 576 + 432 + 432 = 2,016 triangles, 17 % of the asset). A
strictly-coplanar dissolve merges each into one ngon, and re-triangulating an
annulus emits metre-long sub-millimetre slivers that pass an area-based
degeneracy test, survive gltfpack, and then fail the stage-2 contract validator
on `invalid_or_nonunit_loop_normal_count` — the `350-brannan` failure, where the
same step was worth 0.4 % of triangles. Not worth it here either.

Joins performed: `Toy_sand` 126 → 1, `Toy_ink` 67 → 1, `Toy_glass` 26 → 1,
`Toy_glassl_Glow` 16 → 1, `Toy_apricot` 6 → 1, `Toy_rust` 4 → 1, `Toy_steel`
4 → 1, `Toy_apricot+Toy_stone` 3 → 1, `Toy_mint` 2 → 1. Signed volumes stayed
positive throughout; `inverted_solids: []`.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 10-south-park.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep the material and node names, which are API here: the loader
splits `*_Glow` into the unlit night layer, and glow-ness is name-only, so
without `-km` gltfpack would merge `Toy_glassl_Glow` into an identical non-glow
material and silently kill the night state. `-noq` is the repo standard —
`compress-assets.mjs` produces unquantized files because the kit/landmark merge
paths need float32 attributes, and a quantized build also fails the stage-2
validator on `transforms_applied` / `no_unexpected_objects`. Verified on the
output rather than trusted from the flags: material name set identical (12),
`EXT_meshopt_compression` present, bbox identical to 4 dp.

Vertex attributes in the shipped file are `POSITION` and `NORMAL` only — no UV
set survived, matching `132-south-park` and `501-second`.

## Phase D — high→low bake

Not run. `ALLOW_BAKE: no`, and the asset has no textures and no bakeable relief
worth a texture: its facade detail is 0.14 m applied bands that already cost
almost nothing after the join.

## Phase E — A/B verification

`render_ab.py` on both files at the same rig: day and night, near (1.5 × long
axis = 59.9 m) and far (6 × = 239.6 m), plus four orthographic elevations.

**Engine swap, recorded:** the rig was moved from Cycles/64 to
`BLENDER_EEVEE` + `taa_render_samples = 64`. The machine this repo is authored on
runs many Blender sessions at once — load average was 142 during this pass, and
at that level a single Cycles frame takes minutes. EEVEE renders the same eight
frames in seconds with shadows, flat materials and the glow layer intact, and
gate G4 compares two renders of **one** rig against each other, so the engine
only has to match on both sides. Blender 5.2's enum is `BLENDER_EEVEE`.

| view | mean abs RGB delta | max pixel delta |
|---|---|---|
| day near | **0.0046 %** | 14 |
| day far | 0.0061 % | 5 |
| night near | 0.0015 % | 6 |
| night far | 0.0023 % | 1 |
| elevation N | 0.0102 % | 17 |
| elevation E | 0.0106 % | 16 |
| elevation S | 0.0172 % | 18 |
| elevation W | 0.0138 % | 19 |

Gates are ≤ 2 % far and ≤ 4 % near; the worst view here is **0.017 %**, two and a
half orders of magnitude inside.

**And, having looked at the ×8-amplified diffs rather than only the numbers:**
they are black except for hairline outlines along material boundaries — the
parapet cap against the parapet, the window surrounds against the stucco, the
mullions against the glass. That is the per-object weld: fusing coincident
vertices lets one vertex normal be averaged across two faces that previously had
their own, which moves a single row of anti-aliased edge pixels by a few levels.
The night frames are the cleanest of the eight (max delta 1 at far), which is the
check that matters most, because the `_Glow` split is the thing packing could
have broken. Nothing here is visible at 1:1, let alone at the app's camera.

## Gate results

| gate | result |
|---|---|
| **G1 Contract** — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** — 12 in, 12 out, both `_Glow` materials survive |
| **G2 Geometry** — bbox ≤ max(1 cm, 0.1 %), origin ≤ 1 cm, signed volumes positive, flipped ≤ 0.15 % | **PASS** — bbox identical to 4 dp, origin 0, all volumes positive, **0 flipped of 14,641 hits** |
| **G3 Round-trip** — Blender re-import and pinned-three GLTFLoader | **PASS** — `G3-OK`, three 0.185.1, 14 meshes, 11,976 tris, 12 materials |
| **G4 Appearance** — day+night × near+far | **PASS** — worst 0.017 %, described above |
| **G5 Draw submeshes** ≤ input | **PASS** — 261 → 14 |
| **G6 Size** — reduced | **PASS** — raw −53.0 %; short of the 60 % aspiration, and the census explains the remainder: after the weld and the join there is no waste left, only silhouette geometry and the 2,016 triangles of parapet ring the dissolve step is forbidden to touch |
| **G7 GPU budget** | n/a — bake mode not run |
| **G8 Hygiene** — no foreign geometry, deterministic, no `.blend1` | **PASS** — re-import object count matches, scripts are deterministic, no litter |

**And the check the prompt says is the one that catches sliver damage:** the
stage-2 contract validator was re-run against the **packed shipping file**, not
just the mid file — `artifacts/10-south-park/validation.json` now reads
`overall: PASS`, 13 objects, 11,976 triangles, `invalid_or_nonunit_loop_normal_count: 0`,
0 flipped rays of 30,823 first hits.

## Toolchain

Blender 5.2.0 LTS · gltfpack 0.24 (via `npx --yes gltfpack@0.24`) ·
node v22.19.0 · three 0.185.1 (pinned in `g3check/package.json`) ·
Python 3.9.6 · Pillow 11.3.0 · gzip -9.
