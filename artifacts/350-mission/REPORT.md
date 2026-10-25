# 350 Mission Street (Salesforce East) — asset report

## Result

**PASS** — `350-mission.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_350_mission.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `350-mission.glb`, `350-mission.blend` — export and authoring scene
- `validate_350_mission.py`, `render_350_mission.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `350-mission-{north,east,south,west,top,aerial,aerial-night}.png`, `350-mission-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_350_mission.py
blender -b --python validate_350_mission.py
blender -b --python render_350_mission.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 129.0 m = 129.0 m |
| Plausible metre dimensions | PASS | 61.3769 × 61.3769 × 129.0 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 3,048 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 12 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 19,446 first hits |
| Glow skins face outward | PASS | 490 / 492 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **3,048** (`350-mission_body` 2,556, `350-mission_night_glow` 492); Blender vertices 5,744
- Dimensions: **[61.3769, 61.3769, 129.0] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.39672, 37.790872]**, target height **129.0 m**, category `3` (Office)
- Materials: `Toy_glass`, `Toy_glassl`, `Toy_leaf`, `Toy_leafd`, `Toy_roofd`, `Toy_rust`, `Toy_sand_Glow`, `Toy_sky`, `Toy_sky_Glow`, `Toy_steel`, `Toy_stone`, `Toy_white_Glow`

- Lobby 0–17 m: `Toy_glassl` prism inset 1.2 m, steel mullions every 4.5 m standing 0.6 m proud, warm lit ring behind them.
- Sky-blue LED screen (26.5 m wide) on the Mission (SE) lobby face; steel transfer band 17–18.2 m.
- Shaft 18.2–124.5 m: 25 storey-groups of `Toy_glass` with `Toy_glassl` bands and fins every 4.6 m (the canted-panel shimmer).
- Crown 124.5–129 m: glass screen ring, dark deck, plant cluster.
- Salesforce cloud (three `Toy_sky` lobes, ~10 m wide) on the Mission face at 22 m near the Fremont corner; stone apron, three trees on Fremont.

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: lobby ring + scattered office panes aligned to the fin bays.
- `Toy_sky_Glow`: the LED media screen on Mission.
- `Toy_white_Glow`: crown light line round the screen.

## Iterations

- Draft (3,350 tris) failed validation: 8 degenerate triangles (the shaft loft ended in a zero-height sliver because 4.2 m did not divide the shaft) and only 731/762 glow faces unobstructed (lit panes under fins; lobby glow behind mullions 0.14 m away; LED glow quad wound inward).
- The LED wall sat inside the opaque lobby glass (invisible) and, with the cloud and trees, on the NE face (toward 45 Fremont), not Mission.
- Fixes: storey pitch = shaft / 25; lit-pane spacing = fin spacing (4.6 m); mullions moved 0.6 m proud; LED wall rebuilt as a screen on the Mission face with an outward glow quad; cloud to the Mission face, trees to Fremont. Result 3,048 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-25 (contact sheets sent in four batches of five): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/350-mission.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **166 KB → 78 KB** (53% smaller). Geometry is unchanged. The kit merges every landmark into one body mesh and one glow mesh, so the Phase B cleanup in `tools/glb-optimize/` finds nothing to join or weld; a trial run saved 0 triangles and grew the file 1–5%, so it was not applied. The limited dissolve is skipped as GLB-OPTIMIZE-PROMPT §3 step 3 requires for assets with ring bands and parapets. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
