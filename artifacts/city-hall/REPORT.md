# San Francisco City Hall asset report

## Result

**PASS** — `city-hall.glb` meets the landmark contract in `.agents/skills/sf-asset-check/SKILL.md` and was validated after fresh-scene re-import in Blender 4.5.3 LTS (empty factory scene, `import_scene.gltf`, no source scene state). Every review render, including the validator's own beauty render, was produced from that exact exported GLB.

Not integrated: the production manifest, `pipeline/lib/landmarks.mjs`, and app code are untouched. Integration is a separate job (`docs/asset-plans/INTEGRATION-PROMPT.md`).

`validation.json` is the machine-readable authority for every number below.

## Deliverables

- `REFERENCE.md` — research dossier, sources, verified dimensions, recognition cues, conflicts
- `build_city_hall.py` — deterministic build + export script
- `render_city_hall.py` — controlled review renders from the exported GLB
- `validate_city_hall.py` — isolated fresh-scene re-import validator
- `make_contact_sheet.py` — labelled contact sheet assembly (Pillow)
- `city-hall.blend` — authoring scene (asset geometry only, no cameras/lights)
- `city-hall.glb` — final binary deliverable (1.44 MB)
- `validation.json` — full object-level machine report
- `city-hall-{north,east,south,west,top,aerial}.png`, `city-hall-{night,night-east}.png`, `city-hall-contact-sheet.png`
- `city-hall-validation-aerial.png` — review render made by the validator from the re-import

Rebuild from this directory:

```bash
blender -b --python build_city_hall.py
blender -b --python validate_city_hall.py -- --glb city-hall.glb --out validation.json
blender -b --python render_city_hall.py
python3 make_contact_sheet.py
```

## Verified research (independent of the supplied plan)

| Fact | Value | How verified |
|---|---|---|
| Architectural height | 93.73 m (307.5 ft) to the top of the lantern finial | SF Public Works / SFGOV building description and Emporis-era architectural records; consistent across sources. Dome-only figures (~94 m) and "taller than the US Capitol" claims agree. |
| WGS84 anchor | −122.4192838, 37.7793223 | Falls inside the OSM building polygon `way/24219553`, within ~4 m of its centroid. Accepted unchanged. |
| Footprint (published plan) | ~390 × 273 ft ≈ 118.9 × 83.2 m | Historic plan descriptions / NRHP-era literature |
| Footprint (engineering) | ~92 × 122 m base | WJE base-isolation retrofit paper |
| Footprint (measured) | ~97.8 m E–W × 126.6 m N–S, ~11,033 m² | Direct measurement of the OSM outline |
| Long-axis heading | **350.4° / 170.4° true (9.62° west of north)** | Least-squares fit of the OSM outline's long edges |
| Ceremonial front | East, to Polk Street / Civic Center Plaza | Grand stair, main pedimented portico, and the mayor's balcony all face the plaza; confirmed in geolocated photography and civic event coverage |
| Dome | ~33–34 m outer diameter, drum ~15 m tall, 16-bay drum colonnade, gilded ribs and lantern | Retrofit documentation plus elevation photography |

Sources are listed with what each establishes in `REFERENCE.md`, including the footprint conflict (published plan vs. engineering base vs. measured outline) and the decision to follow the measured outline for map fit.

## Orientation decision

Authored in **true-world orientation: Blender +X = east, +Y = true north, +Z = up**, so `placeGeneric` can scale and position without any rotation. All local geometry is generated on the building's own axes and then rotated **+9.62°** about +Z (counter-clockwise seen from above), giving the measured 350.4° long-axis heading. The ceremonial pedimented portico and grand stair therefore face east toward Civic Center Plaza, and the axis-aligned bounding box is larger than the building because the building sits skewed inside it.

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 1.44 MB self-contained `city-hall.glb` |
| Real-world metres, plausible dimensions | PASS | 122.9836 × 144.92 × 93.75 m AABB (building block ~104 × 130 m skewed 9.62° in plan; height 93.75 m vs. 93.73 m target) |
| Origin at base centre, min Z ≈ 0 | PASS | bbox min Z = 0.0 m; XY centre offset [0.4954, 0.0] m — 0.4 % of the east–west extent, caused by the grand stair projecting further east than the west portico |
| Orientation | PASS | +Y = true north, 350.4° heading, east front |
| Triangle budget | PASS | 20,808 / 27,000 |
| Applied transforms | PASS | all 10 objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals outward | PASS | 0 invalid/non-unit loop normals; 0 flipped visible faces across 4,866 deterministic exterior first-hit rays |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No image textures | PASS | 0 image-texture nodes, 0 textured materials |
| No transparency | PASS | every material alpha = 1.0 |
| Flat-colour `Toy_*` palette, no `Toy_body` | PASS | `Toy_cream`, `Toy_glass`, `Toy_gold`, `Toy_gold_Glow`, `Toy_roofc`, `Toy_roofd`, `Toy_sand`, `Toy_stone`, `Toy_trim`, `Toy_white_Glow` |
| `_Glow` only where it glows | PASS | two night materials on lit panes, the drum openings, the gilded dome ribs/ring/medallions and the lantern core — see "Night state" below. Exported emission strength is 0.0 on every material: the app, not the file, decides when they burn |
| No cameras / lights / animation / armatures / constraints | PASS | 0 / 0 / 0 / 0 / 0 |
| No unexpected or foreign geometry | PASS | 10 mesh objects, one per palette material, unique names, nothing else in the file |

### Re-import metrics

| Metric | Value |
|---|---|
| Object count (all mesh) | 10 |
| Triangles | 20,808 |
| Dimensions (m) | 122.9836 × 144.92 × 93.75 |
| BBox min (m) | −60.9964, −72.46, 0.0 |
| BBox max (m) | 61.9872, 72.46, 93.75 |
| Min Z (m) | 0.0 |
| XY centre offset (m) | 0.4954, 0.0 |
| Image textures / cameras / lights / animation f-curves | 0 / 0 / 0 / 0 |

Per-object triangles: `CityHall_trim` 6,920 · `CityHall_gold_Glow` 3,324 · `CityHall_glass` 2,636 · `CityHall_gold` 2,520 · `CityHall_cream` 2,216 · `CityHall_roofd` 1,148 · `CityHall_stone` 1,136 · `CityHall_roofc` 432 · `CityHall_sand` 432 · `CityHall_white_Glow` 44.

## Night state

The app has no per-asset night switch to configure: `app/src/env.js` derives `uNight` from the solar elevation of the current clock — 0 while the sun is above the horizon, ramping to 1 once it is 10° below — and `updateLandmarkGlow` drives the `_Glow` mesh's opacity from it (`0.12 + uNight * 0.95`). So the only thing an asset has to do to have a night state is carry `_Glow` materials; the loader splits them into a second, unlit mesh (a second draw call) and the city's own clock ignites them. The GLB therefore ships with emission strength 0.0 everywhere.

What lights up, and why:

| Surface | Material | Reasoning |
|---|---|---|
| Gilded meridian ribs, the dome ring, the eight medallions | `Toy_gold_Glow` | The real dome is floodlit after dark and the gilding is what answers the light. These are second, fractionally fatter tubes/spheres *sheathing* the daytime gold pieces, so the day silhouette is unchanged and the dome keeps its shape against a night sky instead of reading as a black hole. |
| The 16 drum-colonnade openings | `Toy_gold_Glow` | The rotunda behind them burns all night and is the building's brightest real feature at distance. |
| Lit panes on the giant-order and basement windows of all four elevations, the corner-pavilion bays, the portico's tall bays, and the north/south centre bays | `Toy_gold_Glow` | Warm office light. One bay in five is deliberately left dark (`occupied()`), so the facade reads as a working building rather than a lantern. |
| The three ceremonial portal doors under the east portico | `Toy_gold_Glow` | The brightest thing at street level, which is where the grand stair leads the eye. |
| The lantern core | `Toy_white_Glow` | The beacon at the top — the one cool-white light on the model, so the finial still separates from the warm dome below. |

Nothing on the roofscape, the terrace or the stone base glows: at the city camera those would smear into a bright blob and cost the dome its silhouette.

The night surfaces cost 3,368 triangles (17,440 → 20,808) and one extra draw call for the whole landmark.

## Design decisions (per `docs/styles/miniature-toy.md` §22)

Recognition cues kept and exaggerated:

1. **The dome.** Oversized dark ribbed shell with 16 gilded meridian ribs, gold ring, medallions, and an open gold lantern with a dark spire — the single strongest identity cue, deliberately enlarged and given the only saturated colour in the model.
2. **The east portico and grand stair.** Rusticated arcaded podium with three gold-arched portals, a free-standing giant-order screen of 8 columns between antae, full entablature and a deep triangular pediment, approached by a 40 m-wide nine-tread stair.
3. **Long, low, symmetrical cream Beaux-Arts block** with a rusticated base, giant-order pilaster rhythm, an attic storey and a strong crowning cornice.
4. **The 16-bay drum colonnade** — paired columns, dark openings, urns, entablature — reading clearly at aerial distance.
5. **A designed roofscape**: verdigris hipped perimeter band, two glazed light courts with solar arrays, four dark-roofed pavilions around the dome base, and the raised crossing block.

Simplified: individual window mullions, sculpture and cartouches, the perimeter's small plan jogs, interior rotunda, and the porticos' coffered soffits. Facade information is reduced to broad bay rhythms (6 m pilaster spacing) so the model stays legible from the app's high three-quarter camera.

Excluded from the GLB as required: Civic Center Plaza, lawns, fountains, flagpoles, Van Ness Avenue, neighbouring buildings, trees, people, vehicles, plinths, cameras and lights. The review renders add a temporary floor and lights that are created only in `render_city_hall.py`.

## Review renders

The four elevations share one orthographic camera rig (identical scale, framing, sun, exposure, and projection) and are labelled from the researched orientation; the top view shows the dome, lantern, drum colonnade, light courts and the four roof pavilions; `city-hall-aerial.png` uses the style bible's camera (≈38° down, 85 mm long lens, neutral warm background). Every image is the same exported GLB.

`city-hall-night.png` (aerial camera) and `city-hall-night-east.png` (plaza-side, low) review the night state: the studio drops to a cold moonlit key and the `_Glow` materials are given emission *in the render scene only*, standing in for the runtime's dusk ramp. Conversely the daylight renders hide the `_Glow` mesh, because the runtime holds it at 12% opacity while the sun is up — neither adjustment touches the exported file.

## Draft manifest entry (not applied)

```json
{
  "id": "city-hall",
  "file": "city-hall.glb",
  "anchor": [
    -122.4192838,
    37.7793223
  ],
  "targetHeightM": 93.73,
  "cat": 18,
  "name": "San Francisco City Hall",
  "estimated": false,
  "dims": [
    122.9836,
    144.92,
    93.75
  ],
  "tris": 20808
}
```

Scaling note for integration: `targetHeightM / measuredHeight` = 93.73 / 93.75 = 0.99979, i.e. the asset is authored essentially at final size.

## Known limitations

- The axis-aligned `dims` are inflated by the 9.62° skew; the building's own plan is ~104 × 130 m including porticos and stair.
- The grand stair projects ~7.6 m beyond the mapped OSM outline on the east; this is deliberate (the plaza steps are part of the asset per the brief) and is the cause of the 0.5 m XY centre offset.
- Facade bay counts are stylised rhythms, not a window-by-window survey.
