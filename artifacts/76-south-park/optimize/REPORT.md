# 76–82 South Park — GLB optimize pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executing
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with `ASSET_CLASS: landmark`,
`ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`. Run 17 August 2026.

**Result: all gates PASS. `76-south-park.optimized.glb` is the shipping file.**

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 299,404 B (292.4 KB) | **116,636 B (113.9 KB)** | **−61.0 %** |
| File, gzip -9 | 47,983 B (46.9 KB) | 67,228 B (65.7 KB) | **+40.1 %** — see G6 |
| Objects / nodes | 118 | **11** | −90.7 % |
| Draw submeshes (primitives, via GLTFLoader) | 120 | **12** | −90.0 % |
| Triangles | 4,376 | 4,376 | 0 |
| Vertices (in Blender, post-weld) | 8,888 | **2,426** | −72.7 % |
| Materials | 10 | 10 | identical set |
| bbox dims | 26.61454 × 26.02415 × 16.28 m | 26.61454 × 26.02415 × 16.28 m | 0 |
| bbox min | −13.30727, −13.01207, 0.0 | −13.30727, −13.01207, 0.0 | 0 |
| Ray-flip fraction | 0.1016 % | **0.0779 %** | improved |

Toolchain: Blender 5.2.0 LTS (hash `fbe6228777e7`, 2026-07-14); `npx gltfpack@0.24`;
node v22.19.0 + the pinned three in `g3check/package.json`; python3 + Pillow 11.3.0;
gzip -9.

`optimize/input/76-south-park.glb` was verified byte-identical to the pre-swap shipping
file with `cmp` before the swap, and every step ran against the copy.

## Phase A — waste census

`inspect.json`. The asset came in as 118 flat-shaded closed prisms, one per feature,
sharing 10 materials. Predictions, and what happened:

- **Split vertices — the big one.** 4,376 triangles carried 8,888 vertices: glTF splits
  vertices for flat shading, so every prism's corners were duplicated per face.
  6,462 coincident vertex pairs measured. Predicted recovery from a 1 mm per-object
  weld ~70 %; **achieved 72.7 %**.
- **Object-count overhead.** 118 nodes, 120 primitives, for 10 materials. Predicted
  ~90 % recovery from join-per-material; **achieved 90.7 %** (11 objects, 12 primitives —
  the extra object and primitive are the two-material `body` prism, whose roof cap is
  `Toy_roofd` while its walls are `Toy_ink`).
- **Duplicate meshes: 1,480 redundant triangles identified** across eleven identical
  window sills, nine balcony balusters, ten festoon lamps and eighteen railing posts.
  **Not deduplicated by instancing**, and deliberately: at 4,376 triangles total the
  node overhead of shared mesh data costs more than the triangles save, and
  join-per-material already collapses them into one buffer. Prompt §3.6 asks for a
  justification per case; this is it.
- **Buried interior faces: none predicted, none found.** The build script places every
  feature proud of or recessed into the wall plane. The one nested pair —
  `service_bay` sitting inside the arch recess — is not a closed solid inside a closed
  solid at the 95 % AABB-fill threshold, and the occluder rule (§3.2) forbids treating
  an open shell as an occluder, so it was correctly left alone.
- **Degenerate triangles: 0.**
- **Over-tessellated curves: none.** The only curved geometry is the twelve-segment
  arch head, whose chord error at the near distance (39.9 m, 1 px = 26.9 mm) is well
  inside a pixel and which is silhouette-adjacent on the street elevation. Not touched.

## Phase B — geometry cleanup

`optimize.py` → `mid.glb`, `phaseb_stats.json`. Per-step:

| Step | Tris | Verts |
|---|---|---|
| input | 4,376 | 8,888 |
| weld + degenerate | 4,376 | **2,426** |
| interior faces | 4,376 | 2,426 |
| limited dissolve | *skipped* | *skipped* |
| join per material | 4,376 | 2,426 |

Joins: `Toy_steel` 31 → 1, `Toy_trim` 29 → 1, `Toy_glass` 20 → 1, `Toy_ink` 13 → 1,
`Toy_trim_Glow` 11 → 1, `Toy_stone` 5 → 1, `Toy_glassl_Glow` 3 → 1, `Toy_roofd` 2 → 1,
plus the two-material body group and the two standalone single-material objects
(`roof_deck` / `Toy_rust`, `flank_sw_band` / `Toy_sand`).

**The limited dissolve was skipped deliberately** (prompt §3.3). This asset has two
closed annuli that follow the whole 6.90 × 29.70 m footprint — `parapet` (13.08 → 13.43 m)
and `roof_rail` round the roof deck — plus long coplanar strips in the stone base, its
two rustication grooves, the south-west flank band and the rear face. Re-triangulating
an annulus ngon emits slivers up to the full 29.7 m length; they pass every area-based
degeneracy test, collapse their shared vertex normals to ~0, and surface only *after* the
shipping swap as `invalid_or_nonunit_loop_normal_count` in the stage-2 contract validator
(precedent `350-brannan`, 13 Aug 2026; same call made on `106-south-park`). At 4,376
triangles the step was worth a handful at most. The skip is recorded in `optimize.py`
itself, not just here.

**The weld did not smooth the flat shading.** This is the known hazard — welding a
flat-shaded box's corners averages three face normals into one — and it is the thing only
Gate G4 catches. It did not happen: Blender kept the meshes flat-shaded and the exporter
re-split by normal on write, which is also why the packed file's vertex count (7,928 on
re-import) is close to the input's rather than to the 2,426 Blender carries internally.
Confirmed visually on the elevation A/B pairs — every wall is a flat field, no gradients.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 76-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept, `-noq` kept, per prompt §4. `grep -rn setMeshoptDecoder app/src/` hits
`app/src/gltf.js:10` and `app/src/assets.js:406`, so meshopt is safe to rely on.
Verified on the output rather than trusting flags: material name set identical (10),
both `_Glow` materials still separate, bbox and origin unchanged, no
`KHR_mesh_quantization` in the extension list.

## Phase D — bake

Not run. `ALLOW_BAKE: no`.

## Phase E — A/B verification

`render_ab.py` (aerial azimuth 172°, matched to the asset's own review aerial so the
street facade, the 29.7 m depth, the exposed south-west flank band and the roof deck all
appear in one frame) + `diff_ab.py`. Day at glow alpha 0.12, night at alpha 1.0 /
emission 6, near = 1.5 × long axis, far = 6 ×, plus four orthographic elevations.

| View | Mean abs RGB Δ | Max px Δ | Gate |
|---|---|---|---|
| day_near | **0.0031 %** | 24 | ≤ 4 % |
| day_far | **0.0045 %** | 16 | ≤ 2 % |
| night_near | **0.0508 %** | 66 | ≤ 4 % |
| night_far | **0.0663 %** | 33 | ≤ 2 % |
| elev_n | 0.0049 % | 22 | — |
| elev_e | 0.0078 % | 34 | — |
| elev_s | 0.0063 % | 33 | — |
| elev_w | 0.0035 % | 27 | — |

**What the diffs actually show, having looked at them at ×8 amplification:** hairlines
one pixel wide along geometry edges, and Monte Carlo speckle on the roof-deck surface in
the two night frames. The speckle is the largest signal in the whole set and it is
Cycles sampling variance between two independent renders, not a geometry change — the
deck is the only surface lit by the ten emissive festoon dashes, so it carries the most
path-tracing noise. Nothing is missing, no silhouette moved, no flat surface gained a
gradient, the three lit windows and the entry lintel are unchanged, and the arch, the
bay, the grid window and the penthouse all read identically. There is nothing here a
player would notice.

## Gate results

| Gate | Verdict | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (10); both `_Glow` materials separate; no `Toy_body`; no manifest-named nodes to preserve on this asset |
| **G2** geometry | **PASS** | bbox Δ 0; origin Δ 0; 11/11 signed volumes positive; ray flip 0.0779 % ≤ 0.15 % |
| **G3** round-trip | **PASS** | re-imports in Blender (11 objects, 10 materials); `g3check` → `G3-OK {"ok":true,"meshes":12,"tris":4376,...}` |
| **G4** appearance | **PASS** | max mean Δ 0.0663 % against a 2 % far gate; diffs inspected and described above |
| **G5** draw submeshes | **PASS** | 120 → 12 |
| **G6** size | **PASS on raw, qualified on gzip** | −61.0 % raw; +40.1 % gzipped — below |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object count matches (11); scripts deterministic and committed here; no `.blend1` left |

### G6 — the gzip number, honestly

Raw bytes fell 61 %, gzipped bytes rose 40 %. Both are real. Meshopt output is already
entropy-coded so it does not gzip further, while the pre-optimize file was plain glTF
buffers that gzip compressed 6:1. **Over the wire the un-optimized file would have been
~19 KB smaller.**

Shipping the optimized file anyway, for the three reasons `165 South Park` first recorded
and `104–106 South Park` repeated:

1. Meshopt compression is the **mandatory intake step** for everything entering
   `app/public/sf-assets/` (`AGENTS.md` ship step). This is not an optional trade.
2. The **structural wins are the real ones**: 120 → 12 draw submeshes and the vertex
   collapse both matter to the shared `BatchedMesh` that every generic landmark renders
   out of. 19 KB over the wire does not, on an asset that is 66 KB against a 500 KB
   budget.
3. One encoding across all assets is worth more than the bytes.

The prompt's 60 % target was measured on 250–900 KB landmarks where raw and compressed
move together; a sub-120 KB asset does not re-litigate it. Noted for the third time in
this set — the target line in `GLB-OPTIMIZE-PROMPT.md` §0 could usefully say so itself.

## Shipping swap

`76-south-park.optimized.glb` copied over `artifacts/76-south-park/76-south-park.glb`;
the pre-optimize original is archived at `optimize/input/76-south-park.glb`
(byte-identical, verified with `cmp` before any step ran).

The asset's **stage-2 contract validator was re-run against the packed shipping file**
and still returns `overall: PASS` on all 16 checks — 4,376 triangles, 11 objects,
26.6145 × 26.0241 × 16.28 m, min Z 0.0, XY centre (0.0, 0.0), 11/11 signed volumes
outward, ray-flip 0.1016 %. `validation.json` and `REPORT.md` in the asset root carry the
shipped numbers, so the integration stage writes its manifest entry from reality.
