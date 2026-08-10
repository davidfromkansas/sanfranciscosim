# Salesforce Tower asset report

## Result

**PASS** — `salesforce-tower.glb` meets the repository's landmark contract and was validated after fresh-scene re-import in Blender 4.5.3 LTS. The asset is not integrated into the app and the production landmark manifest was not modified.

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
| Binary GLB, external dependencies | PASS | 817 KB self-contained `salesforce-tower.glb` |
| Plausible real-world meters | PASS | 73.3818 × 73.3818 × 326.0 m overall; width includes the semantically enlarged entrance canopy |
| Origin / base | PASS | bounding box min Z 0.0 m; XY center offset [0.0, 0.0] m |
| Orientation | PASS | true north = Blender +Y; footprint aligned to measured SoMa grid; identity entrance defines front treatment |
| Triangle budget | PASS | 18,412 / 27,000 triangles |
| Applied transforms | PASS | all 33 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | source meshes recalculate face normals; re-import has 0 invalid/non-unit loop normals; all controlled views inspected without inverted surfaces |
| Unexpected / leaked geometry | PASS | 33 mesh objects only; no studio plane, context, camera or light in GLB |
| Image textures / PBR maps | PASS | 0 images and 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque |
| Flat material contract | PASS | eight `Toy_*` materials; roughness 0.85; no `Toy_body` |
| Glow naming | PASS | `Toy_white_Glow` only on crown/upper media surfaces, `Toy_red_Glow` only on beacon |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-reset then imported the final GLB; render script independently repeats that isolation |

## Geometry and materials

- Object count: **33 mesh objects**
- Triangle count: **18,412**
- Dimensions: **[73.3818, 73.3818, 326.0] m**
- Bounding box min: **[-36.6909, -36.6909, 0.0] m**
- Bounding box max: **[36.6909, 36.6909, 326.0] m**
- Minimum Z: **0.0 m**
- XY center offset: **[0.0, 0.0] m**
- Materials: `Toy_glass`, `Toy_red_Glow`, `Toy_roofd`, `Toy_sky`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_white_Glow`

The mapped structural footprint is approximately 54–55 m across its flats. The 73.38 m axis-aligned bounds are expected: the rounded-square plan is rotated about 44° to true north and the entrance canopy projects beyond the glass shaft.

## Visual design

The miniature preserves the five cues identified in `REFERENCE.md`: the slender rounded-square taper, continuous pale horizontal sunshade rhythm, upper-third curvature, perforated/luminous crown, and blue cloud at the entrance. Fine real-floor/perforation detail is grouped into large readable forms in line with `docs/styles/miniature-toy.md`; the finished asset uses matte flat colors rather than photoreal glass or textures.

The review elevations share the same orthographic scale, 900 × 1500 resolution, camera height, warm tabletop lighting, exposure and projection. The top view reveals the open crown and mechanical roof; the aerial render uses a 38° downward, 105 mm restrained-perspective camera.

## Draft manifest entry (not applied)

```json
{
  "id": "salesforce-tower",
  "file": "salesforce-tower.glb",
  "anchor": [-122.3969270512, 37.7897756184],
  "targetHeightM": 326,
  "cat": 16,
  "name": "Salesforce Tower",
  "estimated": false,
  "dims": [73.3818, 73.3818, 326.0],
  "tris": 18412
}
```

The anchor is the OpenStreetMap building centroid cross-checked against 415 Mission Street. Architectural height follows the architect and CTBUH. The `dims` reflect complete asset bounds, including the entrance canopy, not merely the structural shaft.

## Scope confirmation

No Salesforce Transit Center, Salesforce Park, neighboring buildings, roads, general landscaping, people, vehicles, plinth, studio background, camera or light is present in the GLB. Temporary studio elements exist only inside the render process and are never exported.
