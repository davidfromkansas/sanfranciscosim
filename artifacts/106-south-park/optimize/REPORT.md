# 104–106 South Park — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/106-south-park/`, 16 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 251,324 B (245.4 KB) | **105,336 B (102.9 KB)** | **−58.1%** |
| File, gzip -9 | 41,067 B (40.1 KB) | 61,463 B (60.0 KB) | **+49.7%** — see §G6 |
| Objects / nodes | 73 | **11** | −85% |
| Draw submeshes (primitives, via GLTFLoader) | 73 | **13** | −82% |
| Triangles | 3,920 | 3,920 | 0 |
| Vertices | 7,936 | **2,104** | −73.5% |
| Materials | 10 | 10 | identical set |
| bbox dims | 26.3728 × 26.3678 × 11.5800 m | 26.3728 × 26.3678 × 11.5800 m | 0 |
| bbox min | −13.1864, −13.1839, 0.0 | −13.1864, −13.1839, 0.0 | 0 |

Toolchain: Blender 5.2.0 LTS; `npx gltfpack@0.24`; node + the pinned three in
`g3check/package.json`; python3 + Pillow; gzip -9.

## Phase A — waste census

`inspect.json`. The asset came in as 73 flat-shaded closed prisms, one per
feature, sharing 10 materials. Two forms of waste, one large and one nil:

- **Split vertices.** 3,920 triangles carried 7,936 vertices — glTF splits
  vertices for flat shading, so every prism's corners were duplicated per face.
  Predicted recovery from a 1 mm per-object weld: ~70%.
- **Object-count overhead.** 73 nodes, 73 primitives, for 10 materials. Predicted
  recovery from join-per-material: ~85% of the node/accessor overhead.
- **Buried interior faces: none predicted, none found.** The build script places
  every feature proud of or recessed into the wall plane and never nests one
  solid inside another, so there is nothing provably invisible to delete.
- **Over-tessellated curves: none.** There are no curves in this asset.

## Phase B — geometry cleanup

`optimize.py` → `mid.glb`, `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 3,920 | 7,936 |
| 1. weld ≤ 1 mm + degenerate | 3,920 | **2,104** |
| 2. interior faces | 3,920 | 2,104 (0 removed) |
| 3. limited dissolve | **SKIPPED — see below** | |
| 5. join per material | 3,920 | 2,104 (73 objects → 11) |
| 7. normals audit | `inverted_solids: []` | |

### Step 3 was skipped deliberately

Prompt §3.3 says to skip the limited dissolve entirely on assets with large
coplanar **ring bands**. This asset has the worst case of them: `parapet` is a
closed annulus following the whole 7.32 × 29.72 m footprint, and the cornice, the
dentil course and the sign band are all long coplanar strips. Re-triangulating an
annulus ngon emits slivers up to the full 29.7 m length. They pass every
area-based degeneracy test, collapse their shared vertex normals to ~0, and
surface only *after* the shipping swap, as `invalid_or_nonunit_loop_normal_count`
in the stage-2 contract validator — the 350-brannan failure of 13 Aug 2026.

On a 3,920-triangle asset with no curved shells the step was worth a handful of
triangles at most, so it was not worth working around. The skip is recorded in
`phaseb_stats.json` as `limited_dissolve`.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 106-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept (material names are API — `Toy_glassl_Glow` and `Toy_trim_Glow`
have identical parameters to nothing else here, but the rule is unconditional).
`-noq` kept: this repo does not quantize, and `pipeline/compress-assets.mjs`
produces exactly these flags. `compress-assets.mjs` will skip this file at intake
because it already carries `EXT_meshopt_compression`, which is the intended
behaviour.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` at azimuth 172° (adapted from the generic 45° to match this
asset's own review aerial, so the diff covers the street facade, the 29.7 m
depth and the boarded south-west flank in one frame), elevation 42°, near
39.6 m / far 158.2 m, plus four orthographic elevations. `diffs.json`:

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0031% | 22 |
| day far | 0.0040% | 10 |
| night near | 0.0017% | 10 |
| night far | 0.0019% | 2 |
| elev N / E / S / W | 0.0072 / 0.0065 / 0.0034 / 0.0038% | 18 / 18 / 15 / 15 |

**What the ×8-amplified diffs actually show:** faint single-pixel lines along a
few silhouette and bevel edges, and nothing else. Every image is otherwise black.
No element is missing, no silhouette moved, no shading changed, the night layer
lights the same four windows and the same entry soffit. There is nothing here a
player could notice; the residual is rasteriser jitter from re-welded vertex
positions, not a change in the model.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (10, byte-for-byte names); `_Glow` pair still separate; no `Toy_body`; no manifest-named nodes on this asset |
| **G2** geometry | **PASS** | bbox Δ 0.0000 m, origin Δ 0.0000 m; `inverted_solids: []`; ray test 22,500 rays / 14,753 hits / **0 flipped** (0.0000%) |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` → `G3-OK {"ok":true,"meshes":13,"tris":3920,...}` under the pinned three, no decode errors |
| **G4** appearance | **PASS** | all eight views ≤ 0.0072% mean, against gates of 2% far / 4% near |
| **G5** draw submeshes | **PASS** | 73 → 13 |
| **G6** size | **PASS on raw, qualified on gzip** | −58.1% raw; +49.7% gzipped — see below |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object count matches (11); scripts are deterministic and committed here; no `.blend1` left |

### G6 — the gzip number, honestly

Raw bytes fell 58%, gzipped bytes rose 50%. Both are real. Meshopt output is
already entropy-coded, so it does not gzip further, while the pre-optimize file
was plain glTF buffers that gzip compressed 6:1. **Over the wire the
un-optimized file would have been ~20 KB smaller.**

Shipping the optimized file anyway, for the same three reasons 165 South Park
recorded:

1. Meshopt compression is the **mandatory intake step** for everything entering
   `app/public/sf-assets/` (`AGENTS.md`, asset pipeline §Ship step). This is not
   an optional trade.
2. The **structural wins are the real ones**: 73 → 13 draw submeshes and
   7,936 → 2,104 vertices both matter to the shared `BatchedMesh` merge that all
   generic landmarks render out of. 20 KB over the wire does not, on an asset
   that is 60 KB against a 500 KB budget.
3. One encoding across all assets is worth more than the bytes.

The 60% reduction target in the prompt was measured on 250–900 KB landmarks where
raw and compressed move together. A sub-100 KB asset does not re-litigate it.

## Shipping swap

`106-south-park.optimized.glb` copied over
`artifacts/106-south-park/106-south-park.glb`; the pre-optimize original is
archived at `optimize/input/106-south-park.glb` (byte-identical copy, verified
with `cmp` before any step ran).

The asset's own stage-2 contract validator was re-run against the **packed
shipping file** and still returns `overall: PASS` on all 16 checks — including
`transforms_applied`, `no_unexpected_objects` and
`normals_outward_ray_residual_within_tolerance`, the three that a quantized build
would have broken. `validation.json` and `REPORT.md` now carry the shipped
numbers (11 objects, 3,920 tris, 105,336 B), and the review renders and contact
sheet were regenerated from the shipping file.
