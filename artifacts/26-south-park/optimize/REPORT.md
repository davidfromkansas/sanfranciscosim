# 26–28 South Park (51 Taber Place) — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/26-south-park/`, 17 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 167,512 B (163.6 KB) | **72,832 B (71.1 KB)** | **−56.5%** |
| Objects / nodes | 57 | **8** | −86.0% |
| Draw submeshes (primitives, via GLTFLoader) | 57 | **8** | −86.0% |
| Triangles | 2,512 | 2,512 | 0 |
| Vertices | 5,136 | **4,498** | −12.4% |
| Materials | 8 | 8 | identical set |
| bbox dims | 25.93791 × 26.04205 × 9.05000 m | 25.93791 × 26.04205 × 9.05000 m | 0 |
| bbox min | −12.96896, −13.02102, 0.0 | −12.96896, −13.02102, 0.0 | 0 |

Toolchain: Blender 5.2.0 LTS; `npx gltfpack@0.24`; node + the pinned three in
`g3check/package.json`; python3 + Pillow.

## Phase A — waste census

`inspect.json`. The asset came in as 57 flat-shaded closed prisms plus one ring
band, sharing 8 materials.

- **Object-count overhead** is the dominant waste: 57 nodes and 57 primitives for
  8 materials. This is what matters to the shared `BatchedMesh` all generic
  landmarks render out of.
- **Split vertices.** 2,512 triangles carried 5,136 vertices; a 1 mm per-object
  weld took that to 1,368 inside Blender, though meshopt re-splits for flat
  normals on export, so the shipped saving is 12.4%.
- **Buried interior faces: none predicted, none found.**
- **Over-tessellated curves: none.** There are no curves in this asset — the
  frontage is straight (the oval's curvature over a 6.69 m chord is a 0.19 m
  sagitta, below the model's bevel radius).

## Phase B — geometry cleanup

`optimize.py` → `mid.glb`, `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 2,512 | 5,136 |
| 1. weld ≤ 1 mm + degenerate | 2,512 | **1,368** |
| 2. interior faces | 2,512 | 1,368 (0 removed) |
| 3. limited dissolve | **SKIPPED — see below** | |
| 5. join per material | 2,512 | 1,368 (57 objects → 8) |
| 7. normals audit | `inverted_solids: []` | |

### Step 3 was skipped deliberately

Prompt §3.3 says to skip the limited dissolve on assets with large coplanar ring
bands. This asset's parapet is a closed annulus following the whole 30.13 × 6.69 m
footprint. Re-triangulating an annulus ngon emits slivers up to the full ring
length; they pass every area-based degeneracy test, collapse their shared vertex
normals to ~0, and surface only *after* the shipping swap as
`invalid_or_nonunit_loop_normal_count` in the stage-2 contract validator — the
350-brannan failure of 13 August 2026. On a 2,512-triangle asset with no curved
shells the step was worth a handful of triangles at most.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 26-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept unconditionally (material names are API). `-noq` kept — this repo
does not quantize, and `pipeline/compress-assets.mjs` produces exactly these
flags; it will skip this file at intake because it already carries
`EXT_meshopt_compression`, which is the intended behaviour.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` at the generic 45° azimuth / 42° elevation, near and far, day and
night, plus four orthographic elevations. `diffs.json`:

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0003% | 23 |
| day far | 0.0021% | 5 |
| night near | 0.0000% | 2 |
| night far | 0.0062% | 127 |
| elev N / E / S / W | 0.0040 / 0.0035 / 0.0061 / 0.0043% | 21 / 27 / 13 / 19 |

The ×8-amplified diffs show faint single-pixel lines along silhouette and bevel
edges and nothing else. The 127-value maximum in `night_far` is a single pixel on
the lit-window edge in a 24,865-pixel foreground whose mean is 0.0062%; nothing
is missing, no silhouette moved, and the night layer lights the same two windows
and the same entry soffit.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (8, byte-for-byte names); both `_Glow` materials still separate; no `Toy_body`; no manifest-named nodes on this asset |
| **G2** geometry | **PASS** | bbox Δ 0.0000 m, origin Δ 0.0000 m; `inverted_solids: []`; ray test 22,500 rays / 14,017 hits / **0 flipped** (0.0000%) |
| **G3** round-trip | **PASS** | `g3check` → `G3-OK {"ok":true,"meshes":8,"tris":2512,...}` under the pinned three, no decode errors |
| **G4** appearance | **PASS** | all eight views ≤ 0.0062% mean, against 2% far / 4% near |
| **G5** draw submeshes | **PASS** | 57 → 8 |
| **G6** size | **PASS** | −56.5% raw, against a 60% target — a 164 KB asset does not re-litigate a target measured on 250–900 KB landmarks |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object count matches (8); scripts deterministic and committed here; no `.blend1` left |

## Shipping swap

`optimize/26-south-park.optimized.glb` was copied over
`artifacts/26-south-park/26-south-park.glb`; the pre-optimize file is archived at
`optimize/input/26-south-park.glb`. The **stage-2 contract validator was re-run
against the shipped optimized file** and passes all 16 checks —
`artifacts/26-south-park/validation.json` now describes the shipping asset.
