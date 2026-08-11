# Coit Tower asset report

## Result

**PASS** — `coit-tower.glb` meets the repository's landmark contract and was
validated after fresh-scene re-import. Per the task scope, the asset is **not**
integrated: `app/public/sf-assets/landmarks_manifest.json`, `pipeline/`, and
all app code are untouched. Integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md` + the notes in
`docs/asset-plans/coit-tower.md` §2.13).

The exact exported GLB was re-imported before all seven review renders were
produced. `validation.json` is the machine-readable authority for the metrics
below.

Environment note: the plan names Blender 4.5 LTS at `/opt/blender`; that path
does not exist on this machine. Everything ran headless on **Blender 5.2.0
LTS** (`/Applications/Blender.app`, CPU Cycles). No 4.5-specific API is used.

## Deliverables

- `REFERENCE.md` — research dossier and design decisions
- `build_coit_tower.py` — deterministic model build/export script
- `render_coit_tower.py` — fresh-GLB controlled render script
- `make_contact_sheet.py` — contact sheet compositor
- `validate_coit_tower.py` — isolated re-import validator
- `coit-tower.blend` — reproducible authoring scene (asset only)
- `coit-tower.glb` — final binary deliverable (565 KB, self-contained)
- `validation.json` — full object-level machine report
- `coit-tower-{north,east,south,west,top,aerial}.png`
- `coit-tower-contact-sheet.png`

Rebuild from this directory with:

```bash
blender -b --python build_coit_tower.py
blender -b --python validate_coit_tower.py
blender -b --python render_coit_tower.py
python3 make_contact_sheet.py
```

## Orientation — decision and measured heading

The generic landmark rule says "front faces −Y". This asset instead follows
the task prompt's stronger requirement: the loader applies no rotation
(`placeGeneric` in `app/src/assets.js`), so the model is authored with
**Blender +Y = true north, +X = east** and the entrance baked at its
real-world heading. The measured heading of the entrance facade is
**bearing ≈ 346°** (the OSM footprint's longest flat edge, the footway to the
parking loop, and the Columbus-statue photograph all agree — see
`REFERENCE.md`). The entrance is therefore on the **+Y (north) side, yawed
14° counter-clockwise**, facing the parking-circle approach — *not* on −Y and
*not* on the south-east as the plan dossier stated; that dossier error is
documented and corrected in `REFERENCE.md`. The four base bays sit on a
regular cross at 346° / 76° / 166° / 256°, matching the measured footprint to
within a few degrees.

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 565 KB self-contained `coit-tower.glb`, 0 images |
| Plausible real-world meters | PASS | 23.8014 × 23.8014 × 64.0 m; rotunda extent matches the 22.4–23.1 m OSM footprint (corners of the yawed bay cross set the axis-aligned bounds), height matches the published 64 m / 210 ft |
| Origin / base | PASS | bbox min Z 0.0 m; XY center offset [0.0, 0.0] m |
| Orientation | PASS | +Y = true north; entrance at measured bearing 346° (see above) |
| Triangle budget (≤ 12,000) | PASS | **11,164** triangles |
| Applied transforms | PASS | all 167 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | 0 invalid/non-unit loop normals; 22,496 deterministic visibility rays, 0 flipped visible faces (all geometry authored as closed manifold solids — no single-sided sheets) |
| Unexpected / leaked geometry | PASS | 167 mesh objects only; no studio plane, context, camera or light in the GLB |
| Image textures / PBR maps | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque |
| Flat material contract | PASS | six `Toy_*` palette materials, roughness 0.85, no `Toy_body` |
| Glow naming | PASS | `Toy_white_Glow` only on the loggia inner drum and lantern arch reveals — the crown openings that light up at night |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets then imports the final GLB; the render script independently repeats that isolation |

## Geometry and materials

- Object count: **167 mesh objects**
- Triangle count: **11,164**
- Dimensions: **[23.8014, 23.8014, 64.0] m**
- Bounding box min: **[-11.9007, -11.9007, 0.0] m**
- Bounding box max: **[11.9007, 11.9007, 64.0] m**
- Minimum Z: **0.0 m**
- XY center offset: **[0.0, 0.0] m**
- Materials: `Toy_glass`, `Toy_ink`, `Toy_stone`, `Toy_trim`, `Toy_white`, `Toy_white_Glow`

The mapped rotunda footprint is ~22.4 m across the bay faces; the 23.8 m
axis-aligned bounds come from the corners of the four rectangular bays on
their 14°-yawed cross (exactly as in the mapped polygon, which measures
22.46 × 23.15 m axis-aligned) plus the thin cornice caps.

## Visual design

The miniature preserves the four cues ranked in `REFERENCE.md`: the plain
white tapering cylinder with its subtly wider two-tier crown; 24 crisp
full-height flutes (3 per crown bay); the ring of 8 tall arched loggia
openings with chunky balustrades, triple slot groups over the piers, and the
open-topped lantern above; and the round rotunda base that grounds the tower
on the hilltop the app's terrain supplies. The lantern well is modelled for
the app's downward camera: open rim, well floor, `Toy_glass` skylight ring
and a small central cap (style bible §10). Scope-limited per the plan: no
Pioneer Park, parking circle, terrain, trees, people, vehicles or plinths.

The four review elevations share one orthographic rig (same scale, framing,
lighting, exposure; directions are true compass directions). The top view
shows the crown arcade, skylight ring and observation-deck ring; the aerial
render uses a 38° downward, 105 mm restrained-perspective camera standing
north-west of the tower so the entrance quadrant is visible.

## Draft manifest entry (do not apply in this task)

```json
{
  "id": "coit-tower",
  "file": "coit-tower.glb",
  "anchor": [
    -122.4058338,
    37.8023742
  ],
  "targetHeightM": 64,
  "cat": 0,
  "name": "Coit Tower",
  "estimated": false,
  "dims": [
    23.8014,
    23.8014,
    64.0
  ],
  "tris": 11164
}
```

The anchor is the OSM way/28824850 polygon centroid computed from raw node
coordinates; it agrees with the plan's anchor (-122.4058407, 37.8023762)
within ~0.6 m — either lands the tower on the same summit spot. Height 64 m
is the tower's height above its own terrace (OSM `height`, Wikipedia 210 ft);
the GLB starts at z = 0 and the app's terrain supplies Telegraph Hill.

## Scope confirmation

No Pioneer Park, parking circle, Telegraph Hill terrain, trees, roads,
people, vehicles, flag, statue, plinth, studio background, camera or light is
present in the GLB. Studio elements exist only inside the render script and
are never exported. No existing GLB was modified or renamed; no app code or
production manifest was touched.
