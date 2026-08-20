# 1 Market Street — GLB optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run on `artifacts/1-market/`,
19 August 2026. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## 0. Result

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 1,276,992 (1,247.1 KB) | **485,348 (474.0 KB)** | **−62.0%** |
| Gzip −9 bytes | 184,913 | 241,022 | +30.3% (see §5) |
| Triangles | 18,508 | 18,508 | 0 |
| Vertices (Blender topological) | 30,142 | 10,704 | −64.5% |
| Objects | 733 | **13** | −98.2% |
| Draw submeshes (glTF primitives) | 734 | **14** | −98.1% |
| Materials | 12 | 12 | identical set |
| bbox | 112.2081 × 112.0981 × 48.7 | identical | 0 |
| Origin offset XY | −0.0005, −0.0005 | identical | 0 |

**All gates G1–G6 and G8 PASS.** G7 not applicable (`ALLOW_BAKE: no`).

Toolchain: Blender 5.2.0 LTS, `gltfpack 0.24` via `npx`, node v22.19.0,
python3 + Pillow, gzip −9.

## 1. Forensic inspection (`inspect.json`)

733 objects, 18,508 tris, 734 estimated primitives, one vertex attribute
(`NORMAL`), no textures, no UVs.

Waste census:

| Finding | Size | Technique |
|---|---|---|
| **Coincident vertex pairs** | **29,362** | per-object weld ≤ 1 mm |
| **Duplicate mesh groups** | 12,676 redundant tris across 63 signature groups (165 mullions, 110 colonnettes, 58 arcade piers, 53 arch plates, the per-storey spandrel/glazing/sill bands) | join-per-material (the app merges into one `BatchedMesh` anyway, so instancing buys nothing at runtime) |
| **Object-count overhead** | 733 objects → 10 material groups | join-per-material |
| Degenerate tris | 0 | — |
| Buried interior faces | 0 removable | see §3 |
| Over-tessellated curves | 6 fan discs at 10 segments; chord error already < 1 px at the 168 m near distance | left alone |

## 2. Phase B — geometry cleanup

Both switchable steps were **measured, not assumed** — four variants, all packed
and all re-validated:

| Variant | Verts after B | Packed raw | Packed gzip |
|---|---|---|---|
| weld + dissolve | 10,704 | 476,328 | 276,355 |
| **weld only (shipped)** | **10,704** | **485,348** | **247,022** |
| dissolve only | 30,142 | — | — |
| neither | 30,142 | — | — |

The **weld is the whole win**: 29,362 coincident pairs collapse and the exported
vertex count drops by two thirds. The **limited dissolve removes zero triangles**
and is worth 9 KB raw (1.9%) while costing 29 KB gzip (11.8%).

`GLB-OPTIMIZE-PROMPT` §3 step 3 says to skip the dissolve entirely on assets with
large coplanar ring bands, and this asset has **eight** of them (plinth, base
band, base cornice, frieze, balustrade, cornice architrave, corona, cornice cap),
each following the footprint all the way round. The documented failure — an
annulus ngon re-triangulating into hairline slivers whose stored normals collapse
— was explicitly tested for and **did not occur here** (0 ngons and 0 triangles
under 1e-4 m² in both variants; `slivergeo.py`, and `slivercheck.py` reads the
packed file's normal accessors directly rather than trusting Blender's recomputed
loop normals). The bevels on those ring bands break each annulus into separate
coplanar runs, which is why.

**Shipped without the dissolve anyway**, on two grounds: it transfers 11.8% fewer
bytes over the wire, and the prompt's standing advice for this asset shape costs
1.9% of on-disk size to follow. The measurement is recorded here so the question
does not have to be re-opened.

## 3. Judgment calls

- **No interior-face removal.** The occluder rule requires a closed solid filling
  ≥ 95% of its own AABB. This building's body is a **U**, so its AABB fill is 29%
  and it is correctly rejected as an occluder — the rule did exactly what it is
  for. The ~730 applied plates do each bury one face in the wall behind them
  (≈ 1,460 tris, 7.9%), but proving that requires a point-in-polygon test against
  the U footprint rather than an AABB, and the prompt forbids boolean shortcuts.
  Left on the table and recorded.
- **No curve retessellation.** The only curved geometry is six 10-segment fan
  discs on the roof; at the landmark near distance (168.3 m) one pixel is 0.113 m
  of world and their chord error is already below it.
- **No instancing.** 12,676 tris are duplicate mesh data, but the landmark loader
  merges every object into one shared `BatchedMesh`, so instancing would save
  file bytes only and would cost the join that produced the 98% submesh
  reduction. Joined instead.
- **A tri-reduction pass ran upstream, in the build.** The forensic census on the
  first build (21,292 tris) showed six beveled 10-gon fan cylinders at 276 tris
  each and ~20 roof boxes beveled at two segments at 108 tris each. Those bevels
  are invisible at the app's camera distance, so `build_1_market.py` was changed
  to drop them — 21,292 → **18,508** tris, −13.1%, before the optimize pass ran
  at all. That is a build fix, not an optimize step, and it is why
  `optimize/input/1-market.glb` is the 18,508-tri build.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid_weldonly.glb -o 1-market.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names — mandatory, because `_Glow` is
name-only and gltfpack would otherwise merge `Toy_glassl_Glow` into `Toy_glassl`
(identical parameters) and silently kill the night layer. Verified on the output:
**all 12 material names present, `Toy_glassl_Glow` and `Toy_gold_Glow` still
distinct.**

`-noq` (no quantization) per the repo standard — float32 attributes, matching
`pipeline/compress-assets.mjs`. `EXT_meshopt_compression` is the only extension
in the output; `app/src/gltf.js:10` and `app/src/assets.js:416` both register
`MeshoptDecoder`, checked before relying on it.

## 5. Why gzip goes up

The input is uncompressed float32 geometry with enormous redundancy, so gzip
alone takes it to 185 KB. Meshopt already removes that redundancy, so the packed
stream is near-incompressible and gzip only reaches 241 KB. The number that
matters is the **on-disk / on-GPU byte count**, which is what the app fetches and
decodes and what AGENTS.md's ≤ 500 KB landmark budget measures: **474.0 KB,
inside budget**, against a family in which `palace-of-fine-arts` (750 KB),
`painted-ladies` (623 KB), `ferry-building` (557 KB) and `city-hall` (521 KB)
already sit above it.

## 6. Gates

| Gate | Result |
|---|---|
| **G1 Contract** — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** |
| **G2 Geometry** — bbox identical to 4 dp, origin within 0.0005 m, 0 inverted signed volumes, ray residual 0.00% | **PASS** |
| **G3 Round-trip** — Blender re-import + `g3check/` pinned-three loader: `G3-OK {"ok":true,"meshes":14,"tris":18508,...}`, no decode errors, only `EXT_meshopt_compression` | **PASS** |
| **G4 Appearance** — day+night × near+far + 4 elevations | **PASS**, mean abs RGB delta **0.06%–0.19%** (gates: ≤ 2% far, ≤ 4% near) |
| **G5 Draw submeshes** — 734 → 14 | **PASS** |
| **G6 Size** — 1,276,992 → 485,348, −62.0% against a 60% target | **PASS** |
| **G7 GPU budget** | n/a (`ALLOW_BAKE: no`) |
| **G8 Hygiene** — re-import object count 13 both sides, deterministic re-run reproduces byte-identical output, no `.blend1` left | **PASS** |

**G4 in words:** nothing a player would notice. Side by side at the near
three-quarter, the far three-quarter and all four elevations, day and night, the
input and the output are indistinguishable — the residual is denoiser sampling
noise on the brick field, not geometry. No missing elements, no silhouette
change, no shading artefacts, the atrium lantern and the arcade band both
present at night.

## 7. Shipping swap

`1-market.optimized.glb` copied over `artifacts/1-market/1-market.glb`. The
pre-optimize build is archived byte-for-byte at `optimize/input/1-market.glb`.
The asset's `validation.json` and `REPORT.md` were re-generated from the shipped
file, so the integration stage writes its manifest entry from reality:
**18,508 tris, 474.0 KB, 13 objects, 14 draw submeshes, bbox top exactly
48.700 m, loader scale 1.000.**

Two constants in `validate_1_market.py` were still the 300 Brannan copy's and
failed a correct asset: the dimension-plausibility range (25.1–25.3 m crest,
46.5–48.5 m XY) and the recorded anchor/headings. Adapted, not rewritten, per
the prompt's instruction.
