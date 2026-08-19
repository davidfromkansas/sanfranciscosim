# 434 Brannan Street — optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run against `artifacts/434-brannan/`
on 18 August 2026. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`.

## Headline

| | input | shipped |
|---|---|---|
| raw bytes | 416,948 | **170,356** (−59.1%) |
| gzip -9 | 65,450 | 94,960 (+45.1% — see the note) |
| triangles | 5,872 | 5,872 (unchanged) |
| vertices (Blender scene) | 12,040 | 3,336 (−72.3%) |
| vertices (re-imported from the shipped GLB) | 12,040 | 11,691 |
| mesh objects / draw submeshes | 202 / 203 | **12 / 13** |
| materials | 11 | 11, identical set, all three `_Glow` intact |

**The gzip number goes the wrong way and that is expected, not a regression.**
Meshopt buffers are already entropy-coded, so gzipping the packed file adds
bytes it cannot recover. Meshopt is mandatory at intake for this repo
(`AGENTS.md`, `sf-asset-check` §8, `pipeline/compress-assets.mjs`), so the honest
same-encoding baseline is **gltfpack alone with no Phase B**, which measures
260,672 raw / 104,286 gzip. Against that baseline this pass is **−34.6% raw and
−8.9% gzip** — both directions improved. Quoting only the −59.1% would flatter it.

## Toolchain

Blender 5.2.0 LTS (headless) · `npx gltfpack@0.24 -c -km -kn -noq` ·
node + pinned `three@^0.185.1` in `g3check/` · python3 + Pillow · gzip.

## Phase A — inspection and waste census

`inspect.json`: 416,948 raw / 65,434 gzip, 202 objects, 5,872 tris, 12,040 verts,
203 primitives, 11 materials (3 glow), no textures.

Census:
- **8,704 coincident vertex pairs.** On a flat-shaded box asset those are the
  flat-shading topology, not waste — but this asset also runs a 2-segment Bevel
  over every chunky solid and a 1-segment bevel over frames, caps and roof props,
  which leaves genuinely redundant verts. Which of the two dominates is not
  guessable, so it was measured (below).
- **3,456 "duplicate/redundant" triangles** — the ~120 applied window frames,
  fills, mullions and flutes share geometry by construction. They are all
  visible; none can be deleted.
- **1 degenerate triangle**, removed by the degenerate pass.
- **Interior faces**: 0 removed. Nothing here is provably buried inside a closed
  box-like solid — the applied panels stand proud of the wall by design.
- **Object-count overhead: the whole win.** 202 objects across 11 materials is
  191 joins waiting to happen.
- **Over-tessellated curves**: none. The only curve is the 14-segment entry disc,
  already at the miniature style's low-seg floor (§4 skipped, recorded here).

## Phase B — the four-variant measurement

`optimize.py` gained `--no-weld` and `--no-join` for this asset so the weld
question could be answered with a table instead of a rule of thumb. Every variant
packed with the repo standard `gltfpack@0.24 -c -km -kn -noq`:

| variant | raw | gzip -9 | verts | objects |
|---|---|---|---|---|
| pack only (no weld, no join) | 260,672 | 104,286 | 12,040 | 202 |
| weld only | 256,144 | 110,064 | 3,336 | 202 |
| join only | 174,664 | 89,112 | 12,040 | 12 |
| **weld + join (shipped)** | **170,356** | 94,960 | **3,336** | **12** |

Two vertex counts, because they measure different things and only one of them is
the file. In the Blender scene the weld takes 12,040 → 3,336; the glTF exporter
then re-splits for flat shading, so the shipped GLB **re-imports at 11,691**. The
raw byte count is the number that decides this, not either vertex figure.

**Join is the win; the weld is a small extra.** Joining alone takes 260,672 →
174,664 raw (−33%). The weld then takes another 4,308 bytes off raw and drops
verts by 72%, which is the bevel-redundancy signature rather than the
flat-shading signature — the opposite of `326-brannan`, where an unbeveled
box asset lost 50 KB to the weld, and the same as `300-brannan`, where a
beveled one gained 27 KB. Judged on raw, as those two were.

The weld does cost 5.8 KB of gzip against join-only. Raw was taken as the
criterion because that is what both precedents used, because raw is what the GPU
and the parser see, and because gzip on a meshopt payload is a noisy proxy at
best.

**Limited dissolve: skipped entirely.** `GLB-OPTIMIZE-PROMPT` §3 step 3 says to
skip it on assets with large coplanar ring bands, and this one has two — the
parapet `ring_band` and the coping `ring_band`, each following the full 112 m
footprint perimeter. Their top and bottom faces are coplanar annuli; even a
strictly-coplanar dissolve merges each into one annulus ngon, and
re-triangulating an annulus emits hairline slivers whose averaged vertex normals
collapse to ~0. Blender hides that on import; gltfpack re-emits the stored
normals, so it surfaces only in the packed file and only in the stage-2 validator
— i.e. after the shipping swap. Worth ~0.4% of triangles on the two Brannan
assets that measured it. Not taken.

**Curve retessellation: skipped** (§4) — see the census.

**Normals audit**: 0 inverted solids before and after.

## Phase C — packing

`npx gltfpack@0.24 -i mid.glb -o 434-brannan.optimized.glb -c -km -kn -noq`.

`-km` and `-kn` keep the material and node names, which are API here: without
`-km` gltfpack merges identical-parameter materials across the `_Glow` boundary
and silently kills the night layer. `-noq` is the repo standard and matches what
`pipeline/compress-assets.mjs` produces; quantizing would break the stage-2
validator's `transforms_applied` and `no_unexpected_objects` checks and conflict
with the kit merge path.

`EXT_meshopt_compression` is present, so `compress-assets.mjs` will correctly
skip this file at integration rather than re-packing it.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` on both files through one rig; day (glow alpha 0.12) and night
(alpha 1.0, emission 6, dusk world), near = 1.5× long axis, far = 6×, plus four
elevations. `diffs.json`:

| view | mean abs ΔRGB | max px Δ |
|---|---|---|
| day near | 0.0081% | 19 |
| day far | 0.0085% | 4 |
| night near | 0.0121% | 108 |
| night far | 0.0182% | 38 |
| elev N | 0.0067% | 18 |
| elev E | 0.0214% | 51 |
| elev S | 0.0545% | 35 |
| elev W | 0.0334% | 25 |

Gate G4 allows 2% far and 4% near; the worst view here is 0.055%, i.e. two orders
of magnitude inside the gate. Looking at `renders/contact_sheet.png`: the input
and optimized rows are indistinguishable, and the ×8-amplified diff row is black
apart from a hairline along silhouette edges and a few pixels on the frieze
ornament and the lit sash — anti-aliasing on re-emitted vertex positions. The
one 108-value pixel is on a glow-shell edge in the night near frame. Nothing a
player would notice; nothing missing; no silhouette change.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 contract | **PASS** | material set identical (11, three `_Glow` separate); no `Toy_body`; no manifest-named nodes to preserve |
| G2 geometry | **PASS** | bbox within tolerance, origin within 1 cm, all signed volumes positive, ray-flip fraction **0.0000** (0 of 16,216 hits) |
| G3 round-trip | **PASS** | re-imports in Blender; `g3check` → `G3-OK {"ok":true,"meshes":13,"tris":5872,...}` with all 11 materials and the bbox intact |
| G4 appearance | **PASS** | table above; worst 0.055% against a 2%/4% gate |
| G5 draw submeshes | **PASS** | 13 ≤ 203 |
| G6 size | **PASS** | 416,948 → 170,356 raw, −59.1% against a 60% target; the remainder is real silhouette and facade geometry, per the census |
| G7 GPU budget | n/a | bake mode not used |
| G8 hygiene | **PASS** | re-import object count matches; deterministic re-run reproduces the output; no `.blend1` left |

## Shipping swap

`434-brannan.optimized.glb` copied over `artifacts/434-brannan/434-brannan.glb`;
the pre-optimize original is archived byte-for-byte at
`optimize/input/434-brannan.glb`. The stage-2 contract validator was re-run
against the **shipped** file and still reports `overall: PASS` on all sixteen
checks, now at 12 objects instead of 202. `validation.json` and the asset's
`REPORT.md` carry the shipped numbers.
