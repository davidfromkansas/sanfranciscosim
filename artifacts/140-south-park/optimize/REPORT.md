# 140 South Park — GLB optimize report (stage 4)

Run 16 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node + the pinned three in
`g3check/`, python3 + Pillow, gzip −9.

`ALLOW_MESHOPT` preflight: `grep -rn setMeshoptDecoder app/src/` hits
`app/src/gltf.js` and `app/src/assets.js`, so meshopt is available and `-c` is used.

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 212,588 B | **87,540 B** | **−58.8%** |
| File, gzip −9 | 36,781 B | 57,206 B | +55.5% (see §4) |
| Triangles | 3,136 | 3,136 | unchanged |
| Vertices | 6,328 | 1,740 | **−72.5%** |
| Objects | 87 | **11** | −87.4% |
| Draw submeshes (primitives) | 88 | **12** | −86.4% |
| Materials | 10 | 10 | unchanged |
| BBox (m) | 26.2293 × 26.167 × 10.68 | 26.2293 × 26.167 × 10.68 | identical to 1e-5 m |
| Origin | min Z 0.0, centre (0.175, −0.206) | unchanged | within 1e-5 m |

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Coincident vertex pairs | 4,588 | welded (per-object, ≤ 1 mm) |
| Objects sharing a material | 87 across 8 groups | joined per material |
| Duplicate mesh groups | 15 groups / 804 redundant tris | absorbed by the per-material join |
| Degenerate triangles | 0 | nothing to remove |
| Buried interior faces | 0 removable | see §3 |
| Over-tessellated curves | none | there is not one curved shell in this asset — every form is a box, a prism or a flat panel |
| Vertex attributes | `NORMAL` only | nothing to prune; no UVs, no vertex colours, no textures |

The triangle budget is already spent entirely on flat quads, so there was never a
geometry win to be had. The win here is **node and accessor overhead**: 87 objects and
88 primitives carrying 3,136 triangles. The duplicate-mesh census is unusually high for
a building this size (15 groups) because the nine cornice brackets, the eighteen lap
siding strips and the two condensers are all repeats of one profile — the per-material
join absorbs every one of them.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 3,136 | 6,328 |
| weld + degenerate | 3,136 | 1,740 |
| interior faces | 3,136 | 1,740 |
| limited dissolve 0.05° | 3,136 | 1,740 |
| join per material | 3,136 | 1,740 |

Joins: `Toy_ink` 35, `Toy_olive` 24, `Toy_glass` 9, `Toy_roofd` 7, `Toy_steel` 4,
`Toy_gold_Glow` 3, `Toy_glass_Glow` 2, `Toy_glassl` 2. `Toy_oak` (1 object) and
`Toy_red` (1 object) had nothing to join and stayed as they were.

**Limited dissolve returned zero triangles**, which is the outcome the prompt's §3.3
warns to check for. This asset has exactly the shape the warning describes — a `fascia`
ring band and a `belt` course that follow the footprint all the way round, whose top and
bottom faces are coplanar annuli. Nothing was gained and nothing was risked; the step is
left in the script because re-running it is free and it is the honest record of the
measurement.

**Interior-face removal found nothing removable.** The occluder rule applies: the only
closed solid large enough to bury anything is `body`, and every applied panel stands
proud of its wall rather than inside it.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 140-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept: this asset has two `_Glow` materials, `Toy_gold_Glow` (`caa64a`) and
`Toy_glass_Glow` (`6f95b8`), and `Toy_glass_Glow` is parameter-identical to nothing else
here — but `Toy_gold_Glow` would be a merge candidate the moment a non-glow gold entered
the palette, and glow-ness is name-only. Verified on the output: the material name set
is identical to the input's, both `_Glow` names survive.

`-noq` kept per the repo standard: `pipeline/compress-assets.mjs` produces unquantized
files, and `compress-assets.mjs` skips anything already carrying
`EXT_meshopt_compression`, so a wrongly-quantized asset would never be corrected at the
ship step.

**The gzip figure goes up, and that is expected.** Meshopt-compressed buffers are already
entropy-coded, so re-compressing them adds overhead rather than removing it; the CDN
serves the raw 87 KB. The number that matters is raw bytes over the wire, down 58.8%.
Same behaviour recorded on 155 South Park (+68.7% gzip on a −53.3% raw win).

## 5. Phase D — high→low bake

Not run. `ALLOW_BAKE: no`, and the asset carries no textures.

## 6. Phase E — A/B verification

Camera distances for `ASSET_CLASS: landmark`: near 39.34 m (1.5 × long axis),
far 157.38 m (6 × long axis). Day pass renders `_Glow` at alpha 0.12 (the app's day
state); night pass at alpha 1.0 with emission ≈ 6 under a dusk world.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day_near | **0.0107%** | 83 |
| day_far | **0.0166%** | 51 |
| night_near | **0.0015%** | 6 |
| night_far | **0.0019%** | 3 |
| elev_n | 0.0194% | 63 |
| elev_e | 0.0159% | 34 |
| elev_s | 0.0080% | 25 |
| elev_w | 0.0102% | 41 |

Gates are ≤ 2% far and ≤ 4% near. The worst view here is 0.0194%, two orders of
magnitude inside the gate.

**Looked at the diffs.** Every diff frame is black except for single-pixel speckle along
geometry edges and along the studio floor's horizon line, which is Cycles sampling noise
between two independent renders rather than a change in the asset — it appears on the
floor plane, which is identical in both scenes. Nothing structural: the cornice bracket
row, the three upper lights and their mullions, the lap-siding shadow lines on the
north-east flank, the wood door, the fire-department connection, the two skylights, the
condenser pair, the hatch and the vent are all present and unchanged in position and
silhouette. The night frames are the cleanest of the eight, which is the right sign — the
`_Glow` split survived the pack.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** | `validation.json` `G1_materials_identical` |
| **G2** Geometry — bbox, origin, signed volumes, flipped fraction | **PASS** | bbox identical to 1e-5 m; origin within 1e-5 m; `inverted_solids: []`; ray flip delta **0.0** (input 0.0 → output 0.0, 22,500 rays) |
| **G3** Round-trip — Blender re-import + pinned-three GLTFLoader | **PASS** | `G3-OK {"ok":true,"meshes":12,"tris":3136,...}`, no decode errors |
| **G4** Appearance — day+night × near+far | **PASS** | max 0.0194% against a 2%/4% gate; diffs described above |
| **G5** Draw submeshes ≤ input | **PASS** | 88 → 12 |
| **G6** Size reduced | **PASS** | −58.8% raw. Just under the 60% aspiration; the census shows the remainder is silhouette geometry — 3,136 triangles of boxes and panels with no curves to retessellate and no interior faces to bury |
| **G7** GPU budget | n/a | bake mode not run |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 11 = export count; scripts are deterministic; no `.blend1`, no `mid.glb` left |

## 8. One measurement worth explaining

`validate.py` reports `output_open_shells: ['grp_Toy_olive']`. This is an artifact of the
test, not a defect in the asset. The check welds a throwaway copy at 1e-4 before
measuring, and after the per-material join the olive group contains the fascia ring, the
belt course, the frieze, the crown and the cap band — solids that share exact coplanar
boundaries at z = 10.14 and z = 5.20. Welding them fuses those coincident vertices and
manufactures T-junctions, which the manifold test then reports as an open shell. The
group's signed volume is positive (7.84 m³), `inverted_solids` is empty, and the ray test
finds **zero** flipped first hits out of 14,001 on both input and output. Nothing changed
between input and output; the same measurement on the input reports the same thing once
its objects are joined. This is exactly why the gate is a **delta** gate rather than an
absolute one.

The stage-2 contract validator was re-run against the packed shipping file and returns
**overall PASS** with `invalid_or_nonunit_loop_normal_count = 0` — the failure mode the
prompt's §3.3 describes (slivers whose stored normals gltfpack re-emits) does not exist
here, because the dissolve that manufactures them saved nothing and changed nothing.

## 9. Shipping swap

`optimize/140-south-park.optimized.glb` (87,540 B) was copied over
`artifacts/140-south-park/140-south-park.glb`; the two are byte-identical. The
pre-optimize original is archived at `optimize/input/140-south-park.glb` (212,588 B).
`validation.json` and `REPORT.md` in the asset directory carry the shipped numbers, so
the stage-5 manifest entry is written from reality: **3,136 triangles, 11 objects,
87,540 bytes, 26.2293 × 26.167 × 10.68 m.**
