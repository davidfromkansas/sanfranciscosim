# Ferry Building asset report

## Result

**PASS** — `ferry-building.glb` meets the repository's landmark contract and was validated after a factory-reset, fresh-scene re-import in Blender 4.5.3 LTS. The asset is **not** integrated: `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs` and all app code are untouched, and nothing was deployed.

Every review render was produced from the exact exported GLB re-imported into an isolated scene. `validation.json` is the machine-readable authority for the numbers below.

## Deliverables

- `REFERENCE.md` — research dossier, sources, conflicting evidence and design decisions
- `build_ferry_building.py` — deterministic model build/export script
- `validate_ferry_building.py` — isolated fresh-scene re-import validator
- `render_ferry_building.py` — controlled render script (re-imports the final GLB)
- `make_contact_sheet.py` — contact-sheet composer
- `ferry-building.blend` — reproducible authoring scene (asset only)
- `ferry-building.glb` — final binary deliverable (730 KB)
- `validation.json` — full object-level machine report
- `ferry-building-{north,east,south,west,top,aerial}.png`, `ferry-building-contact-sheet.png`

Rebuild from this directory with:

```bash
blender -b --python build_ferry_building.py
blender -b --python validate_ferry_building.py
blender -b --python render_ferry_building.py
python3 make_contact_sheet.py
```

## Orientation decision (AGENTS rule 5)

The Ferry Building is a northwest–southeast waterfront slab, so the generic "front faces −Y" convention cannot hold together with real placement; real placement wins.

- Measured from OSM way `558731934` with a minimum-area oriented rectangle: **long axis 143.6° / 323.6°**, short axis **53.6° / 233.6°** clockwise from true north.
- The Market Street (west) front's outward normal points **≈233.6°**.
- The model is authored with Blender **+Y = true north, +X = east**, its local long axis yawed **−53.6° from world +X**. Its local `-Y` side is the Market Street elevation, which in world space faces southwest at the measured heading.
- `placeGeneric` in `app/src/assets.js` only scales and positions, so this baked heading is what the city will see.

Consequence: the axis-aligned bounds (167.5 × 197.8 m) are the rotated envelope of the real ~201 × 56 m footprint, not the building's own dimensions.

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 730 KB self-contained `ferry-building.glb` |
| Real-world meters | PASS | 74.7 m tower height, 201 × 56 m authored footprint |
| Origin / base at z≈0 | PASS | bbox min Z 0.0 m; XY center offset [0.0, 0.0] m |
| Orientation | PASS | +Y true north; measured 143.6°/323.6° heading baked in (see above) |
| Triangle budget | PASS | 12,392 / 24,000 triangles |
| Applied transforms | PASS | all 323 imported mesh objects at loc 0, rot 0, scale 1 |
| Negative scales | PASS | none |
| Normals outward | PASS | 0 invalid/non-unit loop normals; 16 flipped first-hits of 5,324 rays (0.3%, all coplanar decorative planes) within the validator's 0.5% tolerance |
| Unexpected / leaked geometry | PASS | 323 mesh objects only; no plinth, context, studio floor, camera or light |
| Image textures | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | all material alpha 1.0 |
| Flat `Toy_*` materials, no `Toy_body` | PASS | `Toy_glass`, `Toy_gold`, `Toy_ink`, `Toy_roofd`, `Toy_sand`, `Toy_steel`, `Toy_trim`, `Toy_white_Glow` |
| `_Glow` only where it glows at night | PASS | `Toy_white_Glow` used only for the four illuminated clock dials |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets, then imports only the final GLB |

## Geometry and materials

- Object count: **323 mesh objects**
- Triangle count: **12,392**
- Dimensions: **[167.4984, 197.8239, 74.7] m** (rotated envelope; authored body 201.0 × 56.0 m)
- Bounding box min / max: **[-83.7492, -98.912, 0.0]** / **[83.7492, 98.912, 74.7] m**
- Minimum Z: **0.0 m** — XY center offset: **[0.0, 0.0] m**
- Materials: `Toy_glass`, `Toy_gold`, `Toy_ink`, `Toy_roofd`, `Toy_sand`, `Toy_steel`, `Toy_trim`, `Toy_white_Glow`

## Verified dimensions and discrepancies

| Quantity | Adopted | Conflict documented in `REFERENCE.md` |
|---|---|---|
| Tower height | **74.7 m** (245 ft) | The National Register nomination cites 235 ft; the current/common published figure is 245 ft. Adopted 245 ft, matching the manifest draft. |
| Clock dial diameter | **6.7 m** (22 ft) | Historic descriptions give ~23 ft; current material gives 22 ft. |
| Body length × width | **201.0 × 56.0 m** | OSM way `558731934` measures 201.0 × 56.08 m (area 9,846.9 m²); the "660 ft nave" figure agrees. |
| Anchor | **[-122.3933697, 37.7955227]** | The OSM polygon centroid is [-122.3934398, 37.7955325], 6–8 m away. Kept the supplied anchor: it sits on the tower/central-body point, and the loader positions by anchor, not centroid. |

## Visual design

Recognition cues preserved: the 201 m low cream Beaux-Arts slab, the central clock tower with four large dials and a Giralda-derived open two-stage belvedere crown, gilded dome and flagpole, the continuous two-tier arcade rhythm (14 upper / 12 ground arches per wing plus three monumental central arches), and end pavilions with gables. Simplified per `docs/styles/miniature-toy.md` §22: cornice mouldings are single chunky bands, the arcade becomes a broad repeated rhythm of dark graphical openings rather than modelled tracery, and the roof is deliberately designed for the app's downward camera with a clerestory ridge, glazed skylight bands and four tidy plant clusters.

The four elevations share orthographic projection, ortho scale, camera height, exposure and the same warm tabletop lighting; each camera stands on the outward normal of the facade it is named for (north 323.6°, east 53.6°, south 143.6°, west 233.6°), so the elevations are true elevations of a rotated building. The aerial render is a 38°-down, 82 mm camera from the southwest/Market side.

## Draft manifest entry (not applied)

```json
{
  "id": "ferry-building",
  "file": "ferry-building.glb",
  "anchor": [
    -122.3933697,
    37.7955227
  ],
  "targetHeightM": 74.7,
  "cat": 25,
  "name": "Ferry Building",
  "estimated": false,
  "dims": [167.4984, 197.8239, 74.7],
  "tris": 12392
}
```

## Scope confirmation

The GLB contains the Ferry Building only: arcade body, end pavilions, central pavilion, ground-floor arcade, roof/clerestory, tower, crown and flagpole. No ferry gates or gangways, Embarcadero Plaza or roadway, palm trees, streetcars, market stalls, people, vehicles, plinth, studio floor, camera or light. Studio elements exist only inside the render process and are never exported.
