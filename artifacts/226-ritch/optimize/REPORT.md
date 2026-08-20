# 226 Ritch Street — optimize pass (stage 4)

Run 18 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`, defaults
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`. Scripts here are
adapted copies of `tools/glb-optimize/`.

## Headline

| | input | shipped | delta |
|---|---|---|---|
| Raw bytes | 364,412 | **163,016** | **−55.3 %** |
| gzip -9 bytes | 55,351 | 89,392 | +61.5 % (see note) |
| Triangles | 5,144 | 5,144 | 0 |
| Vertices | 10,960 | 10,851 | −1.0 % |
| Objects | 149 | **13** | −91 % |
| Draw submeshes (primitives) | 153 | **17** | −89 % |
| Materials | 14 | 14 | identical set |
| bbox dims (m) | 25.08244 / 24.92443 / 18.1 | identical | 0 |
| bbox min z | 0.0 | 0.0 | 0 |

**The gzip number going up is expected and is not a regression.** The shipped file
carries `EXT_meshopt_compression`, whose payload is already entropy-coded, so gzip
has nothing left to take and adds framing. What the CDN and the browser actually
move is 163 KB against 364 KB. The repo standard is `-noq` (no quantization), so
the headline win is smaller than the quantized numbers quoted in the prompt's
preamble — that is the documented trade (see the prompt §4 and
`artifacts/380-brannan/optimize/REPORT.md` §4).

## Phase A — waste census

`inspect.json`. 149 objects, 153 primitives, 5,144 tris, 10,960 verts, raw 364,412 B.

| Waste | Found | Plan |
|---|---|---|
| Duplicate meshes | 0 by signature (the five skylight domes are identical meshes at different positions, so a signature match would not have let them share data without instancing, and at 92 tris each it is not worth it) | none |
| Unwelded coincident verts | large — every solid is authored as an unindexed prism and then bevelled | weld ≤ 1 mm per object |
| Buried interior faces | none provable: the only candidate occluders are `body_base`/`body_upper`, and every window/loggia panel stands *proud* of them by construction | none |
| Object-count overhead | **the dominant waste**: 149 objects over 14 materials, i.e. 153 draw submeshes for a 5,144-triangle building | join per material |
| Over-tessellated curves | none: the only curved geometry is five 8-gon skylight domes | none |

Predicted before executing: verts roughly −70 % from the weld, primitives to ~14-17
from the join, triangles unchanged. All three held.

## Phase B — geometry cleanup (`optimize.py`, `phaseb_stats.json`)

| Step | tris | verts |
|---|---|---|
| input | 5,144 | 10,960 |
| weld ≤ 1 mm + degenerate delete | 5,144 | 2,864 |
| interior-face delete | 5,144 | 2,864 (0 faces removed) |
| **limited dissolve — SKIPPED** | — | — |
| join per material | 5,144 | 2,864 (149 → 13 objects) |

**The limited dissolve was skipped deliberately**, per the prompt §3 step 3. This
asset has three coplanar ring bands that follow the whole footprint — `parapet`,
`base_cap` and `deck_rail`. A strictly-coplanar dissolve merges each band's top and
bottom annulus into one ngon, and re-triangulating an annulus emits slivers whose
averaged vertex normals collapse to ~0. gltfpack re-emits stored normals, so that
failure would surface only in the packed file, after the shipping swap, as
`invalid_or_nonunit_loop_normal_count`. On `350-brannan` the same step was worth 30
triangles; here it would have been worth fewer. Not taken.

Joins: `Toy_white` 72 objects → 1, `Toy_glass` 34 → 1, `Toy_steel` 16 → 1,
`Toy_trim` 11 → 1, `Toy_ink` 5 → 1, `Toy_glass_Glow` 4 → 1. Objects that are the
sole holder of their material (`body_base`, `body_upper`, `bulkhead`, `roof_deck`,
`mech`, `garage_fill`, `entry_glow`) were left alone.

## Phase C — packing (`gltfpack@0.24`)

```
npx gltfpack@0.24 -i mid.glb -o 226-ritch.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names — mandatory, because `_Glow` is
name-only and without `-km` gltfpack would merge `Toy_glass_Glow` into `Toy_glass`
and silently kill the night layer. `-noq` is the repo standard (float32 attributes
for the runtime merge path). Verified on the output rather than trusted from the
flags: material name set identical (14), bbox identical, node names intact.

304,668 B (mid) → 163,016 B.

## Phase D — high→low bake

Not run. `ALLOW_BAKE: no`, and this asset has no texture-bakeable region worth the
contract exception: it is 5,144 flat-shaded triangles.

## Phase E — A/B verification (`renders/`, `diffs.json`)

Input vs shipped, one rig, day (glow alpha 0.12) and night (alpha 1.0, emission),
near (1.5× long axis = 37.6 m) and far (6× = 150.5 m), plus four orthographic
elevations. Camera azimuth is 45° — **north-east**, because this building presents
its one designed elevation to Ritch Street at bearing 45.6°; the generic script's
default comment said south-west, which here would have pointed the gate at a blind
party wall.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| day_near | 0.0022 % | 21 |
| day_far | 0.0015 % | 5 |
| night_near | 0.0013 % | 9 |
| night_far | 0.0010 % | 3 |
| elev_n | 0.0009 % | 23 |
| elev_e | 0.0010 % | 21 |
| elev_s | 0.0007 % | 16 |
| elev_w | 0.0009 % | 27 |

Gates are ≤ 2 % far and ≤ 4 % near; these are three orders of magnitude inside them.

**Looked at, not just measured.** `renders/contact_sheet.png` puts input, shipped
and an ×8-amplified diff in three rows. The diff row is black except for a scatter
of single pixels along high-contrast silhouette edges — the window frames, the
fire-escape stringers and the parapet cap — which is the antialiasing consequence
of the ≤ 1 mm weld moving coincident vertices onto each other. Nothing is missing,
no silhouette moved, the night glow lights the same four loft windows and the same
entry, and there is nothing here a player could notice.

**Engine deviation, recorded per §10.** The generic `render_ab.py` renders
Cycles/64 on CPU. This machine was at load average 265 with several parallel
sessions on it and a single Cycles night frame did not finish in 90 seconds. The
script was switched to EEVEE at 128 TAA samples (~7 s/frame), which still does
emission so the night half of the gate means something, and which is the engine the
asset's own stage-2 review rig uses. The comparison is differential — the same rig
on both sides — so the substitution costs the gate nothing.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (14, incl. both `_Glow`); no `Toy_body` in this asset; node names intact (`-kn`) |
| G2 Geometry | **PASS** | bbox delta 0.00000 m, origin delta 0.00 m; all closed solids' signed volumes positive; ray test 22,500 rays / 16,803 hits / **0 flipped** (0.000 %) |
| G3 Round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three) `G3-OK`, 17 meshes, 5,144 tris, 14 materials, bbox 25.0824 / 18.1 / 24.9244 |
| G4 Appearance | **PASS** | table above; max delta 0.0022 % against a 4 % gate; visual inspection clean |
| G5 Draw submeshes | **PASS** | 153 → 17 |
| G6 Size | **PASS** | −55.3 % raw against a 60 % aspiration. The remainder is silhouette geometry and a 14-material set that cannot be merged (glow-ness is name-only); triangles were already at 5,144 for a 9,000 cap, so there was no fat to cut |
| G7 GPU budget | n/a | bake mode not used |
| G8 Hygiene | **PASS** | re-import object count matches; scripts are deterministic and re-run reproduces the output; no `.blend1` left |

## Shipping swap

`226-ritch.optimized.glb` copied over `artifacts/226-ritch/226-ritch.glb`; the
pre-optimize original is archived at `optimize/input/226-ritch.glb` (364,412 B).
The asset's `validation.json` was re-run against the shipped file and is still
all-PASS at 5,144 triangles and 18.100 m; `REPORT.md` carries the shipped bytes.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14) · `npx gltfpack@0.24` ·
node v22.19.0 with the pinned three in `g3check/package.json` · python3 with
Pillow 11.3.0 · gzip -9.
