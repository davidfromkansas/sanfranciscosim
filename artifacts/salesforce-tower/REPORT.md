# Salesforce Tower asset report

## Result

**PASS** — `salesforce-tower.glb` meets the repository's landmark contract and was validated after fresh-scene re-import in Blender 4.5.3 LTS. The reviewed GLB is copied to `app/public/sf-assets/landmarks/` and registered in the production landmark manifest, where it replaces the procedural `salesforceTower` after successful asynchronous load while preserving that model as fallback.

The exact exported GLB was re-imported before all seven review renders were produced. `validation.json` is the machine-readable authority for the metrics below.

## Deliverables

- `REFERENCE.md` — research dossier and design decisions
- `build_salesforce_tower.py` — deterministic model build/export script
- `render_salesforce_tower.py` — fresh-GLB controlled render script
- `validate_salesforce_tower.py` — isolated re-import validator
- `salesforce-tower.blend` — reproducible authoring scene (asset only)
- `salesforce-tower.glb` — final binary deliverable
- `validation.json` — full object-level machine report
- `salesforce-tower-{north,east,south,west,top,aerial}.png`
- `salesforce-tower-contact-sheet.png`

Rebuild from this directory with:

```bash
blender -b --python build_salesforce_tower.py
blender -b --python validate_salesforce_tower.py
blender -b --python render_salesforce_tower.py
```

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, external dependencies | PASS | self-contained `salesforce-tower.glb` |
| Plausible real-world meters | PASS | 73.3818 × 73.5321 × 326.0 m overall; width includes the semantically enlarged entrance canopy |
| Origin / base | PASS | bounding box min Z 0.0 m; XY center offset [0.0, -0.0752] m |
| Orientation, front faces `-Y` | PASS | true north = Blender +Y; shell keeps the measured SoMa yaw; the entrance/canopy/cloud identity cue is placed on the `-Y` face |
| Triangle budget | PASS | 20,086 / 27,000 triangles |
| Applied transforms | PASS | all 42 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | source meshes recalculate face normals; re-import has 0 invalid/non-unit loop normals and 0 flipped visible first-hits across 22,500 deterministic rays |
| Unexpected / leaked geometry | PASS | 42 mesh objects only; no studio plane, context, camera or light in GLB |
| Image textures / PBR maps | PASS | 0 images and 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque |
| Flat material contract | PASS | nine `Toy_*` materials; roughness 0.85; no `Toy_body` |
| Glow naming | PASS | `Toy_white_Glow` on the crown skin and the upper LED floors, `Toy_sand_Glow` on the lit office panes and lobby, `Toy_red_Glow` only on the beacon |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-reset then imported the final GLB; render script independently repeats that isolation |

## Geometry and materials

- Object count: **42 mesh objects**
- Triangle count: **20,086**
- Dimensions: **[73.3818, 73.5321, 326.0] m**
- Bounding box min: **[-36.6909, -36.8412, 0.0] m**
- Bounding box max: **[36.6909, 36.6909, 326.0] m**
- Minimum Z: **0.0 m**
- XY center offset: **[0.0, -0.0752] m**
- Materials: `Toy_glass`, `Toy_red_Glow`, `Toy_roofd`, `Toy_sand_Glow`, `Toy_sky`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_white_Glow`

The mapped structural footprint is approximately 54–55 m across its flats. The ~73.5 m axis-aligned bounds are expected: the rounded-square plan is rotated about 44° to true north and the entrance canopy projects beyond the glass shaft.

## Visual design

The miniature preserves the five cues identified in `REFERENCE.md`: the slender rounded-square taper, continuous pale horizontal sunshade rhythm, upper-third curvature, perforated/luminous crown, and blue cloud at the entrance. Fine real-floor/perforation detail is grouped into large readable forms in line with `docs/styles/miniature-toy.md`; the finished asset uses matte flat colors rather than photoreal glass or textures.

The review elevations share the same orthographic scale, 900 × 1500 resolution, camera height, warm tabletop lighting, exposure and projection. The top view reveals the open crown and mechanical roof; the aerial render uses a 38° downward, 105 mm restrained-perspective camera.

## Night state

The app has no day/night switch on the asset: `assets.js` splits the GLB at load
into a body mesh and a glow mesh by material name, and `updateLandmarkGlow`
drives the glow material's opacity from `uNight` (`env.js`), which ramps 0 to 1
as the sun drops from the horizon to 10 degrees below it. A `_Glow` face is
therefore nearly transparent in daylight, so every lit surface here is authored
as a thin skin laid **over** solid body geometry rather than carved out of it:
the daylight silhouette is unchanged and only the light is added.

- `windows_office` - scattered lit panes over the glass bays, one pane per plan
  segment, chosen by a deterministic hash so the pattern is stable per build.
  Warm `Toy_sand_Glow`, matching the baked city's window lights.
- `windows_led` - the upper LED floors, dense and cool, so the shaft brightens
  into the crown instead of stopping under it.
- `crown_light_*` - the crown hoops are solid `Toy_trim` with a separate glow
  skin over them. Previously the hoops were glow-only, which made the crown a
  see-through cage in daylight.
- `lobby_light` - a continuous ring, since a two-storey lobby reads as one lantern.
- `beacon` - the aviation light, unchanged.

## Applied manifest entry

```json
{
  "id": "salesforce-tower",
  "file": "salesforce-tower.glb",
  "anchor": [-122.3969270512, 37.7897756184],
  "targetHeightM": 326,
  "cat": 16,
  "name": "Salesforce Tower",
  "estimated": false,
  "dims": [73.3818, 73.5321, 326.0],
  "tris": 20086
}
```

The anchor is the OpenStreetMap building centroid cross-checked against 415 Mission Street. Architectural height follows the architect and CTBUH. The `dims` reflect complete asset bounds, including the entrance canopy, not merely the structural shaft.

## Scope confirmation

No Salesforce Transit Center, Salesforce Park, neighboring buildings, roads, general landscaping, people, vehicles, plinth, studio background, camera or light is present in the GLB. Temporary studio elements exist only inside the render process and are never exported.

## App replacement behavior

`assets.js` converts `salesforce-tower` to the baked landmark id `salesforceTower`. Once the GLB passes loader validation and placement, `landmarks.useBridgeAsset()` hides the matching code-built object before its bridge-only approach logic returns. If the manifest or GLB fails, the callback is never invoked and the existing procedural tower stays visible, preserving the repository's fallback guarantee.
