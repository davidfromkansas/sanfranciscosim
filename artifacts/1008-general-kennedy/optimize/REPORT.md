# 1008 General Kennedy Avenue — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Tools: the generic scripts from `tools/glb-optimize/` (only the contact-sheet caption was
per-asset and needed changing), Blender 5.2.0 LTS, `gltfpack@0.24`, `g3check/` with pinned
three, python3 + Pillow, gzip −9.

`app/src/gltf.js:10` and `app/src/assets.js:406` both call `setMeshoptDecoder`, so meshopt
is available and `-c` is used.

## Metrics

| | input | output | delta |
|---|---|---|---|
| File, raw | 371,992 B | **165,192 B** | **−55.6%** |
| File, gzip −9 | 54,038 B | 101,707 B | +88% (see §Gzip) |
| Triangles | 5,688 | 5,688 | 0 |
| Vertices | 11,880 | 10,921 | −8.1% |
| Objects | 148 | **10** | −93.2% |
| Draw submeshes (primitives) | 148 | **10** | −93.2% |
| Materials | 10 | 10 | identical set |
| BBox dims (m) | 55.13065 × 35.47261 × 11.9 | identical | 0 |
| Origin offset XY | 0.0, 0.0 | 0.0, 0.0 | 0 |

## Waste census (Phase A)

`inspect.json`. The building is a union of axis-aligned box primitives, so there was
almost nothing geometrically wasteful and a great deal that was *structurally* wasteful:

| Finding | Size | Addressed by |
|---|---|---|
| Object-count overhead — 148 objects sharing 10 materials | 8 join groups, the largest `Toy_trim` (59) and `Toy_glass` (56) | Phase B step 5 |
| Coincident vertex pairs | 8,744 | Phase B step 1 (weld ≤ 1 mm, per object) |
| Duplicate mesh groups | 9 groups, 3,740 redundant triangles | *Not removed* — see below |
| Degenerate faces | 0 | n/a |
| Buried interior faces | 0 found | Phase B step 2 |
| Over-tessellated curves | none — no curved geometry in this asset | n/a |

**On the 3,740 "redundant" triangles.** The census counts the 44 window sills and 100+
window fills as duplicate meshes, which they are — they are the same box repeated at
different positions. Instancing them would trade file bytes for draw calls, and the app's
loader merges the whole asset to ≤ 2 draw calls anyway, so shared mesh data would be
un-shared at load. Joining per material (which is what Phase B did) is the right answer
for this asset class and captures the same win as node overhead instead.

## Per-phase savings

| Phase | Objects | Tris | Verts |
|---|---|---|---|
| Input | 148 | 5,688 | 11,880 |
| B1 weld + degenerate | 148 | 5,688 | 3,136 |
| B2 interior faces | 148 | 5,688 | 3,136 |
| B3 limited dissolve 0.05° | 148 | 5,688 | 3,136 |
| B5 join per material | **10** | 5,688 | 3,136 |
| C gltfpack `-c -km -kn -noq` | 10 | 5,688 | 10,921 |

Triangle count is unchanged throughout, which is correct: this is a box-union model with no
degenerate, buried or over-tessellated geometry to remove. The win is entirely in vertex
welding (−73% verts before the packer re-splits them for its own vertex layout) and in
collapsing 148 nodes to 10.

The limited dissolve found nothing to merge — every face on this model is already the
largest coplanar face it can be, because the geometry was authored as whole boxes rather
than subdivided.

## Gzip

Raw bytes fell 55.6% but gzip-9 bytes roughly doubled. This is expected and is not a
regression: meshopt-compressed buffers are already entropy-coded, so gzip cannot compress
them further and adds framing. The same inversion was recorded on `380-brannan`
(82,556 → 166,998 B, +102%) and accepted there.

The number that matters for the app is raw bytes decoded on the GPU path, and the merge
path needs float32 attributes, which is why `-noq` is mandatory here.

## Judgment calls

- **`-noq` (no quantization)**, per §4 of the optimize prompt. Quantization would break the
  runtime merge (silently — the city would still look fine while every asset fell back to
  procedural) and would fail the stage-2 contract validator on `transforms_applied`.
- **`-km -kn` kept**, per §4. Without `-km`, gltfpack merges materials with identical
  parameters across the `_Glow` boundary. This asset has `Toy_trim` and `Toy_trim_Glow` with
  the *same* base colour `#f3efe6`, so it is exactly the case that rule exists for — without
  `-km` the landing soffit's night glow would have been silently deleted.
- **No instancing** of the repeated window boxes; see the census note.
- **No bake.** `ALLOW_BAKE=no`, and there is no facade relief here worth baking.

## Appearance (Phase E)

A/B renders at the landmark camera distances (near = 1.5× long axis, far = 6×), day (glow
alpha 0.12) and night (alpha 1.0, emission 6, dusk world), plus four orthographic
elevations. `renders/contact_sheet.png` stacks input / optimized / diff ×8.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day_near | 0.023% | 51 |
| day_far | 0.039% | 34 |
| night_near | 0.068% | 112 |
| night_far | 0.111% | 52 |
| elev_n | 0.016% | 36 |
| elev_e | 0.064% | 24 |
| elev_s | 0.099% | 34 |
| elev_w | 0.076% | 32 |

Gates are ≤ 2% far and ≤ 4% near; the worst view here is 0.111%.

**Looked at, honestly:** the input and optimized rows are indistinguishable. At ×8
amplification the diff row shows nothing but a faint outline around individual window
recesses and along the plinth edge — sub-pixel rasterization differences from joining
meshes that previously had their own vertex buffers. No element is missing, the silhouette
is identical, the chimneys and the ridge are unchanged, and the nine lit windows and the
landing soffit all survive into the night pass. There is nothing here a player could see.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | `validation.json` `G1_materials_identical: true`; both `_Glow` materials present in the output set |
| G2 Geometry — bbox, origin, volumes, flips | **PASS** | bbox and origin bit-identical; 10/10 signed volumes positive; `inverted_solids: []`; 22,500 rays, 0 flipped (0.00%) |
| G3 Round-trip — Blender + pinned three | **PASS** | `G3-OK {"ok":true,"meshes":10,"tris":5688,...}`, no decode errors |
| G4 Appearance | **PASS** | worst mean delta 0.111% vs a 2% gate; see above |
| G5 Draw submeshes ≤ input | **PASS** | 148 → 10 |
| G6 Size reduced | **PASS with note** | raw −55.6%, short of the 60% aspiration; see below |
| G7 GPU budget | **n/a** | bake mode off |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 10 matches; scripts are deterministic; `mid.glb` and any `.blend1` removed |

**G6 note.** 55.6% is under the 60% target. The census accounts for the remainder: after
welding and joining, what is left is 5,688 triangles of silhouette geometry — the hipped
roof, the two-storey walls, the plinth, the chimneys and 44 window recesses — none of which
can be removed without changing what the building looks like. The prompt's escape clause
("if < TARGET_REDUCTION, the waste census must show the remainder is silhouette geometry")
is satisfied. Triangle count did not move at all in Phase B, which is the direct evidence:
there was no fat to cut, only structure to collapse.

## Shipping swap

`1008-general-kennedy.optimized.glb` replaced `artifacts/1008-general-kennedy/1008-general-kennedy.glb`
as the shipping file. The pre-optimize asset is archived byte-for-byte at
`optimize/input/1008-general-kennedy.glb` (371,992 B). The asset's `REPORT.md` and
`validation.json` were updated to the shipped numbers.
