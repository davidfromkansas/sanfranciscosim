# Painted Ladies asset report

## Result

**PASS** — `painted-ladies.glb` meets the repository landmark contract and was validated after a factory-reset, fresh-scene re-import in Blender 4.5.3 LTS. The asset is **not integrated**: `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs` and all app code are untouched, and nothing was deployed.

Every review render was produced by re-importing the exact final GLB into an isolated scene. `validation.json` is the machine-readable authority for the figures below.

## Deliverables

- `REFERENCE.md` — independently verified dossier, sources, conflicts and design decisions
- `build_painted_ladies.py` — deterministic six-house build/export script
- `validate_painted_ladies.py` — isolated fresh-scene GLB validator
- `render_painted_ladies.py` — controlled review renderer, importing only the final GLB
- `make_contact_sheet.py` — labeled contact-sheet composer
- `painted-ladies.blend` — reproducible authoring scene (3.1 MB)
- `painted-ladies.glb` — self-contained binary deliverable (976 KB)
- `validation.json` — complete object- and material-level validation report
- `painted-ladies-{north,east,south,west,top,aerial}.png`
- `painted-ladies-contact-sheet.png`

Rebuild from this directory with:

```bash
blender -b --python build_painted_ladies.py
blender -b --python validate_painted_ladies.py
blender -b --python render_painted_ladies.py
python3 make_contact_sheet.py
```

## Orientation decision

The plan's statement that the facades face east is contradicted by independently checked map geometry. The six OSM footprints lie **east of Steiner Street**, and Alamo Square lies **west** of Steiner Street. The postcard-facing facade therefore looks west-southwest toward the park.

- Least-squares bearing through the six OSM front-edge centres: **350.87° toward 720 / 170.87° toward 710**.
- Front outward normal: **260.87°**; main roof ridges run approximately **80.87° / 260.87°**.
- Blender is authored with **+Y = true north, +X = east, +Z = up**. A 9.13° yaw is baked directly into all vertices.
- The model's front doors and stoops are on the west-southwest side. Consequently `painted-ladies-west.png` is the famous Alamo Square/postcard elevation; direction names identify where each camera stands.
- `placeGeneric` only scales and positions, so no loader rotation is expected or required.

This correction is deliberate and documented in `REFERENCE.md`; following the plan's east-facing statement would point the doors toward the back yards.

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 976 KB self-contained `painted-ladies.glb` |
| Real-world meters | PASS | ~16 × 6.9 m houses; 12.5 m individual main ridges; measured 2.9 m grade baked in |
| Origin / base at z≈0 | PASS | bbox min Z 0.0 m; XY centre offset [0.0, 0.0] m |
| True-world orientation | PASS | +Y true north; 350.87° row heading and 260.87° front normal baked into vertices |
| Triangle budget | PASS | 15,744 / 27,000 triangles |
| Applied transforms | PASS | all 430 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals outward | PASS | 0 invalid/non-unit loop normals; 0 flipped visible faces in 9,693 deterministic first-hit rays |
| Unexpected / leaked geometry | PASS | 430 mesh objects only; no context, plinth, studio floor, camera or light |
| Image textures | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | all material alpha 1.0 |
| Flat `Toy_*` materials, no `Toy_body` | PASS | 16 approved flat-colour materials; see list below |
| `_Glow` use | PASS | `Toy_gold_Glow` appears only on the six entry lamps and the 18 lit front window panes; exported emission strength is 0 for daytime |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets and imports only the final GLB |

## Geometry and materials

- Object count: **448 mesh objects**
- Triangle count: **15,960**
- Axis-aligned dimensions: **[25.3658, 44.2368, 16.51] m**
- Bounding box min / max: **[-12.6829, -22.1184, 0.0]** / **[12.6829, 22.1184, 16.51] m**
- Minimum Z: **0.0 m** — XY centre offset: **[0.0, 0.0] m**
- Materials: `Toy_brick`, `Toy_cream`, `Toy_glass`, `Toy_gold`, `Toy_gold_Glow`, `Toy_ink`, `Toy_mint`, `Toy_mustard`, `Toy_red`, `Toy_roofd`, `Toy_rust`, `Toy_sand`, `Toy_sky`, `Toy_stone`, `Toy_trim`, `Toy_verdigris`

The X/Y dimensions are the true-north rotated envelope, including the west-facing stoops. The local house bodies are 16.0 m deep and 6.88 m wide at 7.0 m centres. The 16.51 m total Z envelope includes the 2.9 m baked site fall plus the southern house's chimney; each main roof ridge is 12.5 m above its own local base.

## Verified dimensions and discrepancies

| Quantity | Adopted | Decision |
|---|---|---|
| Per-house footprint | **15.85–16.14 × 6.85–7.14 m** measured; modeled 16.0 × 6.88 m | Independent recomputation from OSM nodes agrees with the plan's broad dimensions. |
| Individual height | **12 m mapped; 12.5 m to main ridge adopted** | OSM supplies 12 m. The 12.5 m ridge preserves the prompt's architectural target while allowing small chimney/finial projections. |
| Grade | **2.9 m total; 0.58 m average per house** | NED10m samples contradict the prompt's approximate 1 m per-house wording. The measured average is baked into the base courses. |
| Anchor | **[-122.432740, 37.776228]** | Combined OSM six-footprint bounding-box centre. The prompt's latitude 37.776185 is about 4.8 m south. |
| Row / front bearing | **350.87° / 260.87°** | Independently fit from the six front-edge centres and checked against street/park geometry. |

## Visual design

The parametric `build_house()` function is called six times with address-specific facade, roof, gable, rear-wing and chimney choices. Recognition is concentrated into the repeated stepped silhouette: six pale-trimmed coloured fronts, two-storey canted bays, narrow recessed entries, eight chunky stoop steps, raised garage/basement openings, steep front gables, parallel roofs, cornice corbels and one chimney per house.

The style-bible §22 reduction removed muntins, shingles, spindlework, carved brackets, utilities and vegetation. It retained broad facade rhythms and exaggerated bay projection, trim thickness and stair readability for the high three-quarter camera. Rear elevations are deliberately plainer but include lower varied extensions, rails, windows and doors so no aerial-facing surface is blank or unrelated.

The four cardinal elevations share orthographic projection, scale, framing, exposure and one warm tabletop rig. The aerial uses a 105 mm camera at 38° down from the park/front side. The top render clearly shows six parallel ridge systems, address-specific lower rear roofs and the chimney rhythm.

## Night lighting revision

The first export lit only six 0.24 m entry lamps, tucked under the door hoods. Runtime QA of the integrated asset found zero warm pixels at `night 1.00` — the lamps were both occluded and far below the resolvable size at the app's 150 m minimum camera distance. The revision enlarges each lamp to 0.56 m, moves it clear of the hood, warms `Toy_gold_Glow` from `caa64a` to `ffd489`, and adds an 18-pane set of lit front windows (both bay storeys plus the entry window on each house) sitting 0.04 m proud of the glass. Those panes are pure `_Glow`, so the loader keeps them at low opacity by day and fades them up at dusk; the daytime silhouette and material contract are unchanged.

## Draft manifest entry (not applied)

The loader scales an entire asset by its total bounding-box height. Because this GLB contains a real 2.9 m grade step and chimneys, using the plan's `targetHeightM: 12.5` would shrink every individual 12.5 m ridge to about 9.5 m. The technically correct no-rescale draft therefore uses the validated total envelope height **16.51 m** while retaining 12.5 m as the architectural ridge height.

```json
{
  "id": "painted-ladies",
  "file": "painted-ladies.glb",
  "anchor": [
    -122.43274,
    37.776228
  ],
  "targetHeightM": 16.51,
  "cat": 1,
  "name": "Painted Ladies",
  "estimated": false,
  "dims": [25.3658, 44.2368, 16.51],
  "tris": 15960
}
```

Integration should verify the one-sample terrain placement at both ends of the row before applying this draft. No manifest change is included in this task.

## Scope confirmation

The GLB contains only the six 710–720 Steiner houses: foundations and shared party-wall massing, facade and rear volumes, roofs, chimneys, windows, doors, cornices, bays, stoops and stairs. It does not contain 700 or 722 Steiner, Alamo Square, lawn, terrain, road, sidewalk, cars, trees, people, fences, neighboring buildings, a display plinth, cameras or lights. Studio floor and lighting exist only in the render process and never enter the GLB.
