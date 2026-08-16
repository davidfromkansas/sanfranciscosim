# Transamerica Pyramid miniature — delivery report

## Result: PASS

`transamerica-pyramid.glb` was factory-reset/re-imported in Blender 4.5.3 LTS
and passed every contract check in `validation.json`. All seven review images
were rendered from that re-imported GLB, not from the authoring scene.

## Deliverables

- `REFERENCE.md` — independently verified source dossier and design decisions
- `build_transamerica_pyramid.py` — deterministic authoring/export script
- `transamerica-pyramid.blend` — reproducible authoring scene
- `transamerica-pyramid.glb` — final binary glTF asset
- `validate_transamerica_pyramid.py` / `validation.json` — fresh-scene validator and result
- `render_transamerica_pyramid.py` — controlled re-import render rig
- `make_contact_sheet.py` — deterministic six-view sheet composer
- `transamerica-pyramid-{north,east,south,west,top,aerial}.png`
- `transamerica-pyramid-contact-sheet.png`

## Contract results

| Check | Result | Re-imported result |
|---|---:|---|
| Binary GLB, self-contained | PASS | One 839 KB `.glb`; no external dependencies |
| Real metre dimensions | PASS | 60.8376 × 60.8376 × 260.0000 m axis-aligned bounding box; 53.3 m shell width across its rotated faces |
| Origin/base | PASS | bbox min `[-30.4188, -30.4188, 0.0000]`; XY centre `[0.0000, 0.0000]` |
| Triangle budget | PASS | 15,666 / 24,000 triangles |
| Applied transforms | PASS | all 74 mesh objects at zero location/rotation, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | finite/unit loop normals; 12/12 targeted exterior pier probes hit outward faces, 0 flipped |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Materials | PASS | seven `Toy_*` materials; no `Toy_body` |
| Textures/transparency | PASS | 0 images, 0 image nodes, all alpha 1 |
| Scene leakage | PASS | 0 cameras, 0 lights, 0 animations, 0 armatures, 0 constraints, no unexpected object types |

The validator retains a broad 22,500-ray diagnostic in addition to the gating
exterior test. Some broad rays deliberately enter a recessed window channel and
hit the opposite open facade from behind; this is recorded as diagnostic data,
not misclassified as a flipped exterior surface. The gating probes strike solid
facade piers from outside and all pass.

## Geometry and materials

- Objects: 74 mesh objects
- Triangles: 15,666
- Dimensions: `[60.8376, 60.8376, 260.0]` m
- Bbox min/max: `[-30.4188, -30.4188, 0.0]` / `[30.4188, 30.4188, 260.0]`
- Minimum Z: `0.0` m
- XY centre offset: `[0.0, 0.0]` m
- Materials: `Toy_trim`, `Toy_glass`, `Toy_stone`, `Toy_steel`, `Toy_roofd`, `Toy_white_Glow`, `Toy_red_Glow`

## Night state

Nothing in the GLB decides day from night. `app/src/assets.js` splits every
`*_Glow` material into a second, unlit mesh at load, and `updateLandmarkGlow`
(`app/src/kit.js`) drives that mesh's opacity as `0.12 + uNight * 0.95`.
`uNight` comes from `app/src/env.js`, which computes the real solar elevation
for San Francisco: exactly 0 while the sun is up, ramping to exactly 1 once it
is 10° below the horizon. So the night state is authored here purely as
geometry wearing a `_Glow` material, and the city turns it on.

`Toy_white_Glow` covers, from the top down: the crown-jewel collar on the spire,
a slim floodlit cornice under the parapet, the lit office panes, the slot over
the colonnade, the lobby and the Montgomery Street entrance. `Toy_red_Glow` is
the aviation beacon at the tip. Both have emission strength zero in the GLB —
the app's glow mesh is unlit, so emission would be meaningless.

A lit office pane is a separate quad 5 cm proud of its glass, so the daylight
facade keeps its dark window grid (the pane is only a 12% cream tint by day) and
the night facade lights up without a second material on the body mesh. Which
panes are lit is decided by `lit_window()`, a deterministic hash: the rate is
drawn per floor and shared by all four faces (12–74% of that floor's windows),
then each pane is picked inside its floor. Rebuilding gives the same pattern,
and the result reads as offices, not as noise: some floors nearly dark, some
nearly full, the scatter random within a floor.

`transamerica-pyramid-night.png` and `-night-east.png` show the state; the day
renders apply the same 0.12 opacity the app uses, so both sides of the ramp are
reviewable.

## Visual design

The model follows the §22 miniature conversion sequence:

- massing is one confident 260 m, four-sided pyramid plus the narrower spire;
- fifteen recessed window channels per face are tiled into individual panes by a
  pale precast spandrel on every 3.66 m floor line, giving a real window grid
  while preserving the triangular cutoff pattern and wide blank corners;
- the east and west wings retain their verified floor-29-to-crown extents and
  vertical outer faces, making them triangular in profile;
- five chunky chevron bays per face ground the tower over a recessed lobby;
- parapets, wing hatches, hip roof and BMU give the aerial camera intentional top
  surfaces without adding surrounding city context.

## Orientation and identity convention

Blender `+Y` is true north and `+X` is east. The measured OSM footprint face
normals are approximately **351.03° / 80.90° / 171.03° / 260.90° clockwise from
true north**, so the model is yawed **−9.10°** from the cardinal axes. No loader
rotation is required.

The address/identity entrance is on the Montgomery Street face, whose outward
normal is 80.90° (east, slightly north). This is the requested "north-east face"
in practical street-grid terms. Because this near-four-way-symmetric landmark
has no meaningful south-front silhouette, the Salesforce Tower convention is
used: orientation is set from researched real-world heading and the explicitly
documented entrance face satisfies the generic `-Y` front rule by convention.

## Anchor decision and manifest draft

The four current OSM footprint corners yield centroid
**`[-122.4027858, 37.7951663]`**. This agrees with the independently published
Wikipedia coordinate (`37.7952, -122.4028`). The plan's supplied
`[-122.4026508, 37.7951872]` is approximately 12 m east of the measured footprint
centre, so it is not used in this draft. Architectural height is independently
confirmed as 260 m by CTBUH, OSM, Wikidata and multiple institutional sources.

```json
{
  "id": "transamerica",
  "file": "transamerica-pyramid.glb",
  "anchor": [
    -122.4027858,
    37.7951663
  ],
  "targetHeightM": 260,
  "cat": 3,
  "name": "Transamerica Pyramid",
  "estimated": false,
  "dims": [
    60.8376,
    60.8376,
    260.0
  ],
  "tris": 15666
}
```

This is a draft only. The production manifest was not modified.

## Scope confirmation

The GLB contains only the pyramid facade/massing, east and west wings, crown and
spire, and the tower's own ground colonnade/lobby. It contains no park, trees,
neighbours, roads, landscaping, people, vehicles, plinth, studio floor,
background, camera or light. No application, pipeline or production-manifest
file was changed.

## Rebuild and validation

From this directory:

```bash
blender -b --python build_transamerica_pyramid.py
blender -b --python validate_transamerica_pyramid.py -- \
  --glb transamerica-pyramid.glb --out validation.json
blender -b --python render_transamerica_pyramid.py
python3 make_contact_sheet.py
```
