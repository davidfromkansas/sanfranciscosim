# 100 First Plaza — asset report

## Result

**PASS** — `100-first.glb` meets the landmark contract: the kit validator
(`tools/landmark-kit/validate.py`, Blender 5.2.3 LTS) factory-reset the scene, re-imported
only the exported GLB and printed "all checks pass". `validation.json` is the
machine-readable authority for every number below. Not yet integrated: the manifest,
`pipeline/lib/landmarks.mjs` and app code are untouched (the lead integrates the batch).

## Deliverables

- `build_100_first.py` — deterministic build (kit helpers in `tools/landmark-kit/toykit.py`)
- `100-first.glb`, `100-first.blend` — export and authoring scene
- `validate_100_first.py`, `render_100_first.py` — thin wrappers around the kit scripts with this building's arguments
- `validation.json` — full machine report
- `100-first-{north,east,south,west,top,aerial,aerial-night}.png`, `100-first-contact-sheet.png`
- `REFERENCE.md` — sources, dimensions, orientation, cues

Rebuild from this folder:

```bash
blender -b --python build_100_first.py
blender -b --python validate_100_first.py
blender -b --python render_100_first.py
```

## Contract results

| Check | Result | Evidence |
|---|---|---|
| Crest = target height | PASS | max Z 136.25 m = 136.25 m |
| Plausible metre dimensions | PASS | 95.4871 × 91.7661 × 136.25 m |
| Base at Z 0 | PASS | min Z 0.0 m |
| Centred in XY | PASS | offset [0.0, 0.0] m |
| Triangle budget | PASS | 4,800 / 27,000 |
| No image textures | PASS | 0 images |
| No transparency | PASS | all alpha 1.0 |
| Flat `Toy_*` materials | PASS | 13 `Toy_*` materials, no violations |
| Has night glow | PASS | `Toy_red_Glow`, `Toy_sand_Glow`, `Toy_white_Glow` |
| No cameras / lights | PASS | 0 / 0 |
| No animation / skin / constraints | PASS | 0 / 0 / 0 |
| Transforms applied | PASS | 2 mesh objects at identity |
| No negative scales | PASS | none |
| Normals outward (signed volume) | PASS | inverted objects: 0 |
| Normals outward (ray residual) | PASS | 0 flipped of 16,037 first hits |
| Glow skins face outward | PASS | 876 / 876 unobstructed |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No unexpected objects | PASS | none |

## Geometry and materials

- Triangles: **4,800** (`100-first_body` 3,924, `100-first_night_glow` 876)
- Dimensions: **[95.4871, 91.7661, 136.25] m** (axis-aligned box of the rotated plan + apron)
- Anchor: **[-122.3977206, 37.7891952]**, target height **136.25 m**, category `3` (Office)
- Materials: `Toy_glass`, `Toy_glassl`, `Toy_leaf`, `Toy_leafd`, `Toy_red_Glow`, `Toy_roofd`, `Toy_rust`, `Toy_sand`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_white_Glow`

- Podium 0–13 m on the full OSM outline (way 91626348; the stepped west run reduced to one diagonal): `Toy_sand` with three window rows, deck, trim parapet, a `Toy_leaf` lawn with five trees on the free roof SW of the tower, one small plant cluster.
- Tower on the OSM part heading, three tiers of `notch_rect` plan (34 × 29.5 m, 3.4 m notches): 13–96 m, 96–106 m (inset 3 m), 106–116 m (inset 6 m); punched windows in `Toy_sand`, `Toy_glassl` boxes filling every notch, trim curbs at the setbacks.
- Crown: trim deck, `Toy_glass` pyramid 117–126 m, trim pyramid 122.5–129 m, thin trim spire to the 136.25 m tip.
- Off-palette tones (WARN, not fail): `Toy_leaf`, `Toy_leafd`.

## Night state

`_Glow` surfaces are thin outward skins over solid body geometry, so the daylight
silhouette is unchanged and only light is added at dusk:

- `Toy_sand_Glow`: lit panes on the podium and tiers.
- `Toy_white_Glow`: a ring just under the crown pyramid (the lit crown).
- `Toy_red_Glow`: the spire's aviation tip.
- 876 glow faces, all unobstructed outward.

## Iterations

- Draft review (aerial): the setback ledges rendered pure black and the podium roof was blank. Cause: bevelled caps on the concave notched plan (`punched_block` bev and `tk.cornice`) — the setback cornices became plain ring-band curbs and the tiers lost their bevel; the ledges now read cream.
- The draft podium was a 56 × 44 m guess rectangle on the wrong axis; replaced with the real OSM outline (it runs ~40 m SW of the tower) and given a planted terrace + plant. Anchor moved with the larger bbox to -122.3977206, 37.7891952. 4,800 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-25 (contact sheets sent in four batches of five): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/100-first.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **262 KB → 105 KB** (60% smaller). Geometry is unchanged. The kit merges every landmark into one body mesh and one glow mesh, so the Phase B cleanup in `tools/glb-optimize/` finds nothing to join or weld; a trial run saved 0 triangles and grew the file 1–5%, so it was not applied. The limited dissolve is skipped as GLB-OPTIMIZE-PROMPT §3 step 3 requires for assets with ring bands and parapets. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
