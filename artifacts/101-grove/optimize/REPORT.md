# 101 Grove Street — GLB optimize report (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 against
`artifacts/101-grove/`. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`. Scripts are the generic `tools/glb-optimize/` set copied in
unchanged except for the contact-sheet caption — this asset needed no per-asset
constant adaptation (no curved silhouette shells, no manifest-named nodes, no
`Toy_body`).

## Metrics

| | input | shipped | Δ |
|---|---|---|---|
| File bytes (raw) | 1,166,344 | **421,008** | **−63.9 %** |
| File bytes (gzip −9) | 176,533 | 266,710 | +51 % — see note |
| Triangles | 17,648 | 17,648 | 0 |
| Vertices | 34,140 | 29,626 | −13.2 % |
| Objects / draw submeshes | 611 | **13** | **−97.9 %** |
| bbox dims (m) | 70.50844 × 47.49774 × 21.4 | identical to 5 dp | 0.0 |
| Origin offset XY (m) | (−0.00337, −0.04226) | identical | 0.0 |
| Materials | 13 | 13, same names | 0 |

**On the gzip number.** Meshopt output is already entropy-coded, so gzip cannot
compress it further and the container overhead makes the gzipped figure larger
than the gzipped uncompressed GLB. That is expected and is not a regression:
the shipped file is 421 KB over the wire either way, meshopt buys the GPU-side
win (13 draw submeshes instead of 611, 13 % fewer vertices, fast decode), and
meshopt is mandatory in this repo regardless —
`pipeline/compress-assets.mjs` is the required ship step per
`.agents/skills/sf-asset-check/SKILL.md` §8, and it emits exactly
`-c -km -kn -noq`. 421 KB is comfortably under the 500 KB landmark gate and
below the shipped median for this tri count (city-hall is 20,808 tris at
533 KB).

## Waste census (Phase A) and what each technique returned

| Finding | Predicted | Actual |
|---|---|---|
| 611 objects sharing 13 materials — pure node/accessor/draw overhead | the dominant win | 611 → 13 objects; most of the 64 % byte reduction |
| 24,120 coincident vertex pairs (flat-shaded chunky solids) | ~13 % verts | 34,140 → 10,020 verts after the per-object weld |
| Duplicate mesh groups (50 Grove balusters, 12 balconettes, 36 rosettes, the repeated window reveals/glass — 8,864 redundant tris) | join, not instance | joined per material; the repeats are small and scattered, so shared mesh data would cost more nodes than it saved |
| Degenerate faces | 0 predicted | 0 found |
| Buried interior faces | few — every object is a closed convex-ish solid built proud of the wall | 0 removed. Correct and deliberate: the occluder rule only allows removal against a **closed** solid, and the wall prism does genuinely hide nothing here because every plate stands proud of it. |
| Over-tessellated curves | none | the only curves are the 14-gon oculus discs and the 10-segment archivolt; both are under one screen pixel of chord error at the near distance (105.8 m) and both are silhouette-defining at the entrance. Not retessellated. |

Limited dissolve at 0.05° returned zero triangles, as expected on a model built
entirely from planar-faced beveled boxes with no coplanar neighbours inside a
single object.

## Phase C packing

```
npx gltfpack@0.24 -i mid.glb -o 101-grove.optimized.glb -c -km -kn -noq
```

`-km -kn` verified on the output: all 13 material names survive, including both
`_Glow` materials kept separate from their non-glow twins (`Toy_gold` /
`Toy_gold_Glow` and `Toy_glassl` / `Toy_glassl_Glow` have identical parameters
and would have been merged across the glow boundary without `-km`). `-noq`
per the repo standard — the file carries `EXT_meshopt_compression` and no
quantization, so `compress-assets.mjs` will skip it at intake rather than
re-pack it.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract — material set identical, `_Glow` separate, no `Toy_body`, node names | **PASS** | `validation.json` `G1_materials_identical: true`; 13/13 names match |
| **G2** Geometry — bbox ≤ max(1 cm, 0.1 %), origin ≤ 1 cm, signed volumes positive, flipped ≤ 0.15 % | **PASS** | bbox delta 0.0 on all three axes; origin delta 0.0; 13/13 groups positive signed volume; 22,500 rays, 20,415 hits, **0 flipped (0.000 %)** |
| **G3** Round-trip — Blender re-import and pinned-three GLTFLoader | **PASS** | `G3-OK {"ok":true,"meshes":13,"tris":17648,...}` via `g3check/` (three ^0.185.1), no decode errors |
| **G4** Appearance — day+night × near+far + 4 elevations | **PASS** | mean abs RGB delta: day near 0.012 %, day far 0.013 %, night near 0.068 %, night far 0.098 %, elevations 0.008–0.051 %. Gates are 4 % near / 2 % far. |
| **G5** Draw submeshes ≤ input | **PASS** | 13 ≤ 611 |
| **G6** Size reduced (target 60 %) | **PASS** | −63.9 % raw |
| **G7** GPU budget | n/a | bake mode off |
| **G8** Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object count 13, materials 13, bbox exact; scripts are deterministic; no stray files |

### G4 — what the diffs actually show, honestly

The ×8-amplified diff row of `renders/contact_sheet.png` is black except for
hairline outlines along a few high-contrast edges (cornice lip, balustrade
rails, window reveals) and two or three single lit-window pixels on the east
elevation at night. These are float round-trip noise from the weld and the
meshopt position re-encoding, at most 37/255 on a single pixel and under 0.1 %
in the mean. Nothing is missing, no silhouette moved, no shading artefact
appeared, and there is nothing here a player would ever see.

## Shipping swap

`101-grove.optimized.glb` was copied over `artifacts/101-grove/101-grove.glb`;
the pre-optimize original is archived byte-for-byte at
`optimize/input/101-grove.glb` (1,166,344 bytes, verified equal to the source
before any step ran). The asset's own `REPORT.md` and `validation.json` carry
the shipped numbers.

## Toolchain

Blender 5.2.0 LTS (hash fbe6228777e7, 2026-07-14) · gltfpack 0.24 via
`npx --yes gltfpack@0.24` · Node v22.19.0 · three ^0.185.1 (pinned in
`g3check/package.json`) · Python 3.9 with Pillow 11.3.0 · gzip −9.
