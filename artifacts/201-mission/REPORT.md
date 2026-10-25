# 201 Mission Street (Providian Financial Building) — asset report

## Result

**PASS** — `201-mission.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_201_mission.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `201-mission.glb`, `201-mission.blend` — export and authoring scene
- `validate_201_mission.py`, `render_201_mission.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `201-mission-{north,east,south,west,top,aerial,aerial-night}.png`, `201-mission-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_201_mission.py
blender -b --python validate_201_mission.py
blender -b --python render_201_mission.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 135.9 m = 135.9 m |
| Plausible metre dimensions | PASS | 114.0744 × 85.5104 × 135.9 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 8,578 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 12 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 1 flipped of 20,266 first hits |
| Glow skins face outward | PASS | 1086 / 1088 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **8,578** (`201-mission_body` 7,490, `201-mission_night_glow` 1,088)
- Dimensions: **[114.0744, 85.5104, 135.9] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.3949073, 37.7911895]**, target height **135.9 m**, category `3` (Office)
- Materials: `Toy_concrete`, `Toy_glass`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_white`

- Podium on the OSM part outline (way 616813260): dark glazed street storey 0–5 m behind `Toy_concrete` piers every 7 m; concrete body 5–17 m with two window rows; concrete deck with a hedge-ring planter and five trees.
- Tower on the OSM octagon (way 616813259), 17–127.2 m: `Toy_stone` body, `Toy_glassd` slot windows (2.7 m bays, 3.75 m storeys), `Toy_white` ribs every 2.7 m (0.9 × 0.55 m) that run 1.8 m past the roof as the notched parapet.
- Lower wing 17–57 m (18 × 11 m) against the tower's south-east face, on the podium's wide Howard-side lobe, same skin, planted roof with three trees. Side, size and height **inferred/estimated** from the photo.
- Roof: dark deck, 22 × 12 m louvred concrete penthouse to the 135.9 m crest, two plant clusters.
- Off-palette tones (WARN, not fail): `Toy_concrete`, `Toy_glassd`, `Toy_leaf`, `Toy_leafd`.

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: podium street-storey ring + ~30% lit slot windows on tower and wing (1,088 faces).

## Iterations

- Draft: banded dark-glass shaft with stone spandrels on a glass podium — the facade was an inferred guess (no photo at the time) and the roof read blank.
- A Commons fetch of the Wikipedia infobox photo (`File:201_Mission_Street.jpg`) showed a pale ribbed concrete tower, so the shaft was rebuilt as concrete ribs + slot windows with a notched crown, the lower wing was added, the podium became grey concrete with planters, and the penthouse was aligned to the tower's long axis with plant at both ends (4,518 → 8,886 tris).
- Contact-sheet review: the 26 × 14 m wing sat almost entirely inside the octagon and did not read. It was moved onto the podium's SE lobe (18 × 11 m, centre 13 m E / 1.5 m S of the anchor origin) so it stands clear of the tower. 8,578 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-25 (contact sheets sent in four batches of five): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/201-mission.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **470 KB → 188 KB** (60% smaller). Geometry is unchanged. The kit merges every landmark into one body mesh and one glow mesh, so the Phase B cleanup in `tools/glb-optimize/` finds nothing to join or weld; a trial run saved 0 triangles and grew the file 1–5%, so it was not applied. The limited dissolve is skipped as GLB-OPTIMIZE-PROMPT §3 step 3 requires for assets with ring bands and parapets. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
