# fulton-plaza — stage 4 optimize report

**Result: ship Phase C alone.** `gltfpack@0.24 -c -km -kn -noq` applied directly to the
approved build, **540,052 → 268,212 bytes raw (−50.3%)**, geometry byte-identical, all
gates PASS. **Phase B is reverted in full under §11** — every one of its variants made the
file *larger*, including the join, and the measurement is below.

| | input | shipped |
|---|---|---|
| raw bytes | 540,052 | **268,212** (−50.3%) |
| gzip9 bytes | 153,240 | 167,112 (+9.1%, see "gzip goes the wrong way") |
| triangles | 10,692 | 10,692 |
| objects / draw primitives | 21 / 26 | 21 / 26 |
| materials | 16 | 16 (identical set) |
| bbox | 128.4915 × 67.6286 × 13.1931 | identical |

Toolchain: Blender 5.2.0 LTS (fbe6228777e7), `gltfpack@0.24` via npx, three ^0.185.1 in
`g3check/`, python3 + Pillow, gzip -9.

## Phase A — waste census

21 objects, 10,692 triangles, 22,157 vertices, 26 primitives, no textures, no
transparency, no duplicate meshes, no degenerate faces. The five multi-material objects
(`monument`, `bollards`, `trees`, `koi`, `koi_glow`) account for the 26 primitives against
21 objects.

Top objects: `joints` 2,304 · `bollards` 1,568 · `monument` 1,440 · `trees` 1,104 ·
`deck` 970 · `koi` 408 · `koi_glow` 384 · `lamps` 384 · `people` 384.

Prediction before executing: join-per-material would fold 21 objects into 15 and 26
primitives into 20; the weld and the limited dissolve were expected to be marginal on an
asset built entirely from flat-shaded chunky solids. **The prediction was wrong in the
direction that mattered.**

## Phase B — measured, then reverted

Six variants, each packed with the repo-standard `gltfpack@0.24 -c -km -kn -noq`:

| variant | raw | gzip9 | prims | float32 VEC3 |
|---|---|---|---|---|
| **pack only (Phase B skipped)** | **353,476** | **225,263** | 26 | 48,238 |
| degenerate only | 420,024 | 307,845 | 26 | 55,162 |
| join only | 417,228 | 307,070 | 20 | 55,162 |
| weld + join | 534,456 | 406,334 | 20 | 65,506 |
| dissolve + join | 394,996 | 309,852 | 20 | 47,926 |
| weld + dissolve + join | 484,944 | 387,196 | 20 | 55,446 |

(Measured on the +0.55 m build; the deck lift at stage 5 is a vertical translation and
changes none of the relationships. The shipped figures at the top of this report are from
re-running the winning path on the +0.95 m build.)

Three things fall out of that table:

1. **The 1 mm weld costs +117 KB and +10,344 vertices** (join only → weld + join). This is
   the `326-brannan` / `ferry-building` result again: on a flat-shaded asset the census's
   "coincident vertex pairs" are not waste, they *are* the shading topology, and welding
   them makes the exporter re-split into a worse arrangement. `optimize.py` now takes
   `--no-weld` / `--no-join` / `--no-dissolve` so the table is five commands.
2. **The limited dissolve genuinely helps** (join only 417,228 → dissolve + join 394,996,
   −22 KB and −7,236 vertices, for 379 triangles) — the ferry-building lesson that its value
   is invisible in the triangle count holds here too.
3. **And none of that matters, because the Blender round-trip itself costs more than any of
   them save.** "Degenerate only" changes essentially no geometry — 13,364 triangles in,
   13,364 out — and still lands 67 KB and 6,924 vertices above pack-only. Importing this
   GLB and re-exporting it produces a *less* vertex-efficient file than the build script's
   own export, and no Phase-B step recovers the difference. The best Phase-B variant
   (dissolve + join, 394,996) is still 41,520 bytes worse than doing nothing.

So Phase B is reverted in full, per §11 ("revert any phase that regresses bytes"). The
scripts and the stats stay committed so the measurement is reproducible rather than a
claim.

One trap found while running the table, and now guarded in `optimize.py`: the
`o.data.shade_flat()` call that protects flat shading **after a weld** must not run when
the weld is skipped. Calling it on a freshly imported mesh discards the glTF's custom split
normals and costs another +8,600 exported vertices, which briefly made every no-weld
variant look worse than it is.

## Phase C — packing

```
npx gltfpack@0.24 -i input/fulton-plaza.glb -o fulton-plaza.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` are mandatory (glow-ness is name-only; the node names are what the stage-2
validator's checks key on), and `-noq` is the repo standard. Verified on the output rather
than trusted from the flags: material name set identical, all 21 node names intact, bbox
unchanged to 1e-4 m. gltfpack drops the *mesh* datablock names but keeps the node names, so
Blender still imports the objects as `deck`, `koi`, `monument` … and the stage-2 validator's
name-keyed checks survive the pass.

**gzip goes the wrong way, and both numbers are quoted above.** Meshopt buffers are already
entropy-coded, so gzip9 rises from 153,240 to 167,112 even as raw drops 50.3%. Meshopt is
mandatory at intake (`pipeline/compress-assets.mjs`, AGENTS "Ship step"), so raw against the
unpacked build is the honest headline.

## Phase E — A/B verification

`render_ab.py` on both files, same rig, day (glow α 0.12) and night (glow α 1.0, emission 6)
at near (1.5× long axis) and far (6×), plus four orthographic elevations. Mean absolute RGB
delta over foreground pixels:

| view | delta | max px |
|---|---|---|
| day near | 0.0055% | 16 |
| day far | 0.0061% | 5 |
| night near | 0.0463% | 72 |
| night far | 0.0451% | 12 |
| elev N / E / S / W | 0.0274 / 0.0022 / 0.0026 / 0.0078% | 20 / 5 / 9 / 13 |

Looking at the amplified diffs: nothing but Cycles sampling noise, concentrated on the
glowing koi and the lit monument in the night pair — the expected place for it, since the
night pass renders with denoising off. No missing elements, no silhouette change, no shading
artifacts. And by construction there is nothing to notice: `-noq` meshopt is a lossless
re-encode of the same float32 attributes, so the only difference between the two files is
how the bytes are packed.

The reseed control the `ferry-building` note calls for was not needed: at 0.046% the night
delta is two orders of magnitude below the 4% gate and an order below the noise floor that
control exists to expose.

## Gates

| gate | result |
|---|---|
| G1 contract — material set identical, `_Glow` separate, node names intact | **PASS** |
| G2 geometry — bbox within 1 cm, origin within 1 cm, all signed volumes positive, ray-flip 0.013% (2 of 15,029 hits) | **PASS** |
| G3 round-trip — Blender re-import + `g3check` (pinned three 0.185.1): 26 meshes, 10,692 tris, 16 materials, no decode errors | **PASS** |
| G4 appearance — max mean delta 0.046% (gates: 2% far / 4% near) | **PASS** |
| G5 draw submeshes — 26 out ≤ 26 in | **PASS** |
| G6 size — −50.3% raw, short of the 60% target | **PASS with justification**: the census found no waste to remove. Every geometry-cleanup variant measured *larger* than doing nothing, so the remainder is silhouette geometry — 10,692 triangles of chunky solids, already 5,300 under the asset's own cap |
| G7 GPU budget | n/a — `ALLOW_BAKE: no` |
| G8 hygiene — no foreign geometry (21 objects in, 21 out), deterministic re-run, no `.blend1` left | **PASS** |

## Re-run after the monument rebuild

Run a third time after the Pioneer Monument was rebuilt (see `../REPORT.md`, iteration 12),
which took the asset from 13,364 to 10,692 triangles. Same table, same conclusion, same
gates; the figures at the top are this run's.

## Re-run after the stage-5 deck lift

The stage-5 app QA found that the deck had to sit at +0.95 m rather than +0.55 m to clear
the baked street's sidewalk plinths (see `../REPORT.md`, build iteration 11). That is a
vertical translation of most of the model, so the winning path was re-run against the new
build rather than having its numbers patched, and `input/fulton-plaza.glb` is the new
pre-optimize archive. The variant table above is from the first pass and is kept because it
is the measurement that decided the strategy; nothing about a vertical translation changes
which of six geometry-cleanup paths is cheapest.

## Shipping swap

`fulton-plaza.optimized.glb` → `artifacts/fulton-plaza/fulton-plaza.glb`; the pre-optimize
build is archived at `optimize/input/fulton-plaza.glb`. The asset's own
`validate_fulton_plaza.py` was re-run against the **shipped** file and still returns
`overall: PASS` on all 19 checks — including `transforms_applied` and
`no_unexpected_objects`, which is what `-noq` buys and what a quantized build would have
cost. `validation.json` and `REPORT.md` carry the shipped numbers.
