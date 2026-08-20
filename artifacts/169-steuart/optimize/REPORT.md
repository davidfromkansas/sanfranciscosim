# 169 Steuart Street (Army & Navy YMCA) — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**All gates PASS.** `169-steuart.optimized.glb` becomes the shipping file; the
pre-optimize asset is archived byte-for-byte at `input/169-steuart.glb`.

## Metrics

| | input | optimized | delta |
|---|---|---|---|
| raw bytes | 1,352,416 | **575,032** | **−57.5%** |
| gzip −9 bytes | 194,766 | 306,342 | +57.3% (see §G6) |
| triangles | 19,908 | 19,908 | 0 |
| Blender vertices | 41,198 | 11,148 | −72.9% (weld) |
| exported vertices | — | 40,636 | flat shading splits per face |
| objects | 600 | 14 | −97.7% |
| **draw submeshes (primitives)** | **602** | **15** | **−97.5%** |
| materials | 13 | 13 | identical set |
| bbox dims (m) | 60.13943 × 60.2778 × 46.64 | identical | 0 |
| bbox min / origin offset | −29.8892, −29.95879, 0.0 / 0.18052, 0.18011 | identical | 0 |

## Phase A — waste census

`inspect.json`. 600 objects, 602 primitives, 19,908 triangles, 41,198 vertices, one
vertex attribute beyond position (`NORMAL`), no textures, no degenerate triangles.

| Technique | Predicted | Actual |
|---|---|---|
| Weld coincident vertices (**30,050 pairs** found) | large | 41,198 → 11,148 vertices |
| Delete degenerate faces | 0 (census found none) | 0 |
| Delete buried interior faces | small | 0 — no object is a closed solid that provably swallows another; the panel/fill/glow construction interpenetrates rather than nests |
| Limited dissolve | small, and risky here | **skipped, deliberately** — see below |
| Curve retessellation | n/a | the only non-planar shapes are the 5-segment window arch heads (already minimal to still read as an arch) and the 4-face tile hip (the silhouette) |
| Join per material | very large | 600 objects → 14, 602 primitives → 15 |

The census also found 43 duplicate-mesh groups totalling 13,936 redundant triangles
(11 identical window frames × 5 floors, 24 identical corbels, 34 identical arcade
reveals, and so on). These are **not** removed: the app merges every landmark into one
shared `BatchedMesh` at load, so GPU instancing would buy nothing and joining per
material already collapses the node and accessor overhead they were costing.

**Limited dissolve was skipped** under the prompt's §3 step 3 rule. This asset has three
coplanar ring bands following the whole footprint perimeter — the cast-stone base
(0–9.60 m, 168 m round), the podium roof deck (13.70–13.95 m) and the wing parapet
(27.84–28.14 m). Their top and bottom faces are perfectly coplanar annuli; even a
strictly-coplanar dissolve merges each into one annulus ngon whose re-triangulation
emits sub-millimetre slivers tens of metres long. Those pass an area-based degeneracy
test, survive Phases B and E, and surface only in the packed file as
`invalid_or_nonunit_loop_normal_count`, because gltfpack re-emits stored normals while
Blender recomputes them on import. Measured on `350-brannan`, 13 Aug 2026, where the
step was worth 0.4%. Not run.

## Phase B — geometry cleanup

`optimize.py` → `phaseb_stats.json`. Weld ≤ 1 mm per object (glow shells are separate
objects, so a per-object weld can never fuse glow onto a base surface); degenerate
sweep; dissolve skipped; join per material. Signed volumes positive for all 14 output
objects, `inverted_solids: []`, bbox and material set unchanged on re-import.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 169-steuart.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names — mandatory, because glow-ness is name-only
and gltfpack would otherwise merge `Toy_glass` into `Toy_glass_Glow` and silently kill
the night layer. `-noq` (no quantization) is the repo standard and is what
`pipeline/compress-assets.mjs` produces. Verified on the output, not from the flags:
`EXT_meshopt_compression` present, 13 material names identical, 15 primitives, bbox
unchanged.

## Phase D

Not run. `ALLOW_BAKE: no`; the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` on both files with one rig, `diff_ab.py` → `diffs.json`,
`renders/contact_sheet.png`.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| day near (90.4 m) | **0.014%** | 35 |
| day far (361.7 m) | **0.012%** | 7 |
| night near | **0.919%** | 50 |
| night far | **0.792%** | 36 |
| elevation N / E / S / W | 0.007% / 0.093% / 0.061% / 0.005% | 22 / 67 / 62 / 34 |

**Looked at, described honestly:** the day and elevation diffs are black. The night
diffs are a uniform speckle across the roof deck and the arcade reveals — Monte-Carlo
sampling noise on the surfaces lit by the emissive arcade band, not a structural
difference. There is no silhouette change, no missing element, nothing moved, and no
shading artifact. Nothing here is visible to a player.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | 13 material names identical; all three `_Glow` materials separate; no `Toy_body`; no manifest-named nodes on this asset |
| **G2 Geometry** | PASS | bbox delta 0; origin delta 0; 14/14 signed volumes positive; ray test 22,500 rays, 13,736 hits, **0 flipped (0.000%)** |
| **G3 Round-trip** | PASS | re-imports in Blender; `g3check` (three 0.185.1 + MeshoptDecoder) → `G3-OK`, 15 meshes, 19,908 tris, 13 materials, bbox matches |
| **G4 Appearance** | PASS | all eight views far under the ≤ 2% far / ≤ 4% near limits; worst is 0.919% and it is sampler noise |
| **G5 Draw submeshes** | PASS | 602 → 15 |
| **G6 Size** | PASS with note | raw −57.5%, just under the 60% aspiration. See below |
| **G7 GPU budget** | n/a | bake mode not used |
| **G8 Hygiene** | PASS | re-import object/material/bbox checks in `phaseb_stats.json` and `validation.json`; scripts are deterministic and re-run reproduces the output; no `.blend1` files |

### G6 note — where the remaining bytes are, and the gzip regression

Two honest caveats.

**The 57.5% is short of the 60% aspiration, and the census says why.** After the weld
there is no removable waste left: the file is 19,908 triangles of *silhouette*
geometry — the masses, the cast-stone base, the corbel rank, the cornice and crest
parapets, the arcade band, the tile hip, and the window relief on four elevations.
Nothing in Phase B could touch it, and cutting it would cost a recognition cue. The
per-vertex cost is high because the asset is **flat-shaded by contract**: every face
carries its own normals, so Blender's 11,148 welded vertices export as 40,636. That is
inherent to the toy style, not waste.

**gzip goes the other way, and this is expected.** Meshopt-encoded buffers are already
entropy-coded, so gzipping them adds 57%. On the wire a CDN serves whichever is
smaller, so the served size is the 575 KB raw file rather than the 195 KB gzip of the
unpacked one. Meshopt is still the right call and is not optional here: every GLB under
`app/public/sf-assets/` is meshopt-compressed at intake (AGENTS, ship step), the app's
loaders register `MeshoptDecoder`, and `compress-assets.mjs` would apply it anyway. The
same pattern is visible in shipped assets — `earl-warren-building.glb` is 453 KB raw
and 312 KB gzipped. At 575 KB this asset sits inside the shipped landmark range
(median 176 KB, `city-hall` 534 KB, `ferry-building` 570 KB, `painted-ladies` 639 KB,
`palace-of-fine-arts` 769 KB) and above the 500 KB soft budget in AGENTS; it is a
42 × 42 m ten-storey landmark with four modelled elevations, which is what that budget
is scaled to.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash fbe6228777e7, 2026-07-14) |
| gltfpack | 0.24 via `npx -y gltfpack@0.24` |
| three (g3check) | 0.185.1 (pinned in `g3check/package.json`) |
| python3 + Pillow | system |
| gzip | system, `-9` |

## Shipping swap

`169-steuart.optimized.glb` copied over `../169-steuart.glb`; `../validation.json` and
`../REPORT.md` updated to the shipped numbers so the integration stage writes its
manifest entry from reality. `input/169-steuart.glb` is the untouched archive.

## Reproducing

```
B=/Applications/Blender.app/Contents/MacOS/Blender
"$B" -b --python inspect.py  -- input/169-steuart.glb inspect.json
"$B" -b --python optimize.py -- input/169-steuart.glb mid.glb phaseb_stats.json
npx -y gltfpack@0.24 -i mid.glb -o 169-steuart.optimized.glb -c -km -kn -noq
"$B" -b --python validate.py -- input/169-steuart.glb 169-steuart.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../169-steuart.optimized.glb)
"$B" -b --python render_ab.py -- input/169-steuart.glb renders/in
"$B" -b --python render_ab.py -- 169-steuart.optimized.glb renders/out
python3 diff_ab.py renders diffs.json
```
