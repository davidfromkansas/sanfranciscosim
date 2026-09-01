# Oracle Park asset report

## Result

**PASS** — `oracle-park.glb` meets the repository landmark contract and was validated after a factory-reset, fresh-scene re-import in Blender 4.5.3 LTS. The asset is **not integrated**: the production manifest, pipeline and app code are untouched, and nothing was deployed.

Every review render was produced from the exact exported GLB re-imported into an isolated scene. `validation.json` is the machine-readable authority.

## Deliverables

- `REFERENCE.md` — independent research dossier, sources, conflicts and design decisions
- `build_oracle_park.py` — deterministic model build/export script
- `validate_oracle_park.py` — isolated fresh-scene re-import validator
- `render_oracle_park.py` — controlled render script, re-importing the final GLB
- `make_contact_sheet.py` — labeled contact-sheet composer
- `oracle-park.blend` — asset-only authoring scene
- `oracle-park.glb` — final self-contained binary asset
- `validation.json` — full machine-readable object/material report
- `oracle-park-{north,east,south,west,top,aerial}.png`
- `oracle-park-contact-sheet.png`

Rebuild from this directory:

```bash
blender -b --python build_oracle_park.py
blender -b --python validate_oracle_park.py
blender -b --python render_oracle_park.py
python3 make_contact_sheet.py
```

## Design translation

The model follows `docs/styles/miniature-toy.md` §22:

1. Recognition cues selected: open east-facing bowl, brick/green split, waterfront arcade, five light standards, giant scoreboard and asymmetric field.
2. Literal seats, ramps, concourses and facade detail removed.
3. Massing rebuilt as three seating rings, one street shell, one canopy, one low waterfront edge and a few identity volumes.
4. The scoreboard, five arches, aisles and light arrays are semantically enlarged for the high aerial camera.
5. Facades use broad brick pier/window and arcade rhythms.
6. The top view is intentionally designed around the field graphic, dark seating horseshoe, pale aisle rhythm, canopy and open Bay side.
7. A final simplification pass removed most bevel-generated topology; the asset totals 14,604 triangles.

### Revision after visual review

A reviewer found the first delivery disconnected: the field read as misaligned against the bowl, the scoreboard floated, and the plaza gate stood apart from the shell. The model was rebuilt against fresh Esri World Imagery and photo references:

- Every part — field graphic, diamond, fence, bowl, decks, shell, gate, scoreboard — is now generated in one home-plate-centred field frame at the re-measured 85.5° bearing, so nothing can drift out of alignment.
- The bowl is three constant-depth terraces lofted between the field boundary and the smoothed surveyed footprint, with pale fascias and rake-hugging aisles.
- The scoreboard stands on a solid brick pedestal growing out of the centre-field concourse block.
- The Willie Mays Plaza gate towers, lintel, sign, clock and portal are a thickening of the shell wall itself at the shell radius.
- The brick shell steps from 24 m on the street sides down to an 18.5 m outfield arcade, opening the bowl to the Bay, with an arched glazing rhythm on the surveyed silhouette.

## Orientation decision

Real placement overrides the generic “front faces -Y” shorthand because this irregular stadium has multiple meaningful elevations.

- Blender **+Y = true north, +X = east, +Z = up**.
- Independent OSM minimum-area footprint measurement: long axis **44.9° / 224.9° clockwise from true north**.
- Mound-line satellite measurement (cross-checked against the 339 ft left-field pole): home plate toward center field **approximately 85.5° clockwise from true north**.
- The model's local field axis is baked at that 85.5° true-world bearing. The tall horseshoe wraps the west/north street sides; the low right-field/Portwalk edge opens east toward the Bay.
- Willie Mays Plaza identity block is authored at the north-west/Second-and-King side.
- `placeGeneric` only scales and positions, so no loader rotation is expected.

The exported axis-aligned bounds are **233.80 × 203.59 m**. They are a true-world rotated envelope of the box-filtered surveyed footprint, comparable to the OSM oriented bound of 212.2 × 191.2 m.

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, self-contained | PASS | `oracle-park.glb`; no external dependencies |
| Real-world meters | PASS | 233.80 × 203.59 × 45.0 m re-imported bounds |
| Origin / base at z≈0 | PASS | bbox min Z 0.0 m; XY center [0.0, 0.0] m |
| True-world orientation | PASS | +Y north, +X east; 85.5° home-to-center bearing baked in |
| Triangle budget | PASS | 14,604 / 27,000 triangles |
| Applied transforms | PASS | all 295 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals outward | PASS | 0 invalid/non-unit loop normals; 0 flipped visible first hits |
| Unexpected/leaked geometry | PASS | 295 mesh objects only; no context, plinth, floor, cameras or lights |
| Image textures | PASS | 0 images and 0 image texture nodes |
| Transparency | PASS | all material alpha 1.0 |
| Flat `Toy_*` materials | PASS | `Toy_brick`, `Toy_glass`, `Toy_gold`, `Toy_ink`, `Toy_mint`, `Toy_roofd`, `Toy_rust`, `Toy_steel`, `Toy_trim`, `Toy_verdigris`, `Toy_white_Glow`; no `Toy_body` |
| Glow usage | PASS | scoreboard face, five lamp-array faces and the north-west entry clock only |
| Cameras / lights | PASS | 0 / 0 in exported GLB |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Duplicate names | PASS | none |

## Required recognition cues

| Cue | Treatment |
|---|---|
| Large open baseball bowl facing the Bay | Three-tier horseshoe stops at the low eastern field edge |
| Brick exterior | Continuous west/north street shell plus entrance and right-field wall |
| Green steel details | Upper structural ring, arcade elements, scoreboard supports and light masts |
| Arched waterfront facade | Five enlarged right-field view arches set into the low Portwalk arcade |
| Recognizable light towers | Five owner-verified standards, each with paired masts and glow face |
| Giant scoreboard | Glow-faced board on a solid brick pedestal rising from the center-field concourse |
| Right-field arcade and wall | 7.32 m brick wall, top walk, pale arcade and five principal arches |
| Waterfront / McCovey Cove relationship | Low porous east edge authored at true heading; water/context intentionally excluded from GLB |

## Height decision

The requested architectural/manifest height is **45 m** from the OSM tag. Giants owner material says the tallest light standard is 178 ft / 54.3 m, likely using a different site/field datum and including fixture height. Because the app scales every dimension by `targetHeightM / measuredHeight`, authoring the model at 54.3 m and manifesting 45 m would shrink its already large footprint by 17%. The export therefore tops exactly at **45.0 m**, preserving the requested integration scale; the conflict is documented in `REFERENCE.md`.

## Draft manifest entry (not applied)

```json
{
  "id": "oracle-park",
  "file": "oracle-park.glb",
  "anchor": [
    -122.3897993,
    37.7786282
  ],
  "targetHeightM": 45,
  "cat": 0,
  "name": "Oracle Park",
  "estimated": false,
  "dims": [
    233.8009,
    203.5874,
    45.0
  ],
  "tris": 14604
}
```

The requested anchor differs from the independently computed OSM outer-polygon centroid `[-122.3894652, 37.7785478]` by roughly 32 m. It is retained because it matches the existing project plan/procedural landmark and placement anchors need not be polygon centroids.

## Scope confirmation

Included: ballpark shell, seating bowl, canopy, five light standards, scoreboard, right-field arcade/wall and field graphic.

Excluded: McCovey Cove water, bridge, streets, parking, boats, people, vehicles, sculptures, plinths, cameras and lights.

No integration files were edited. Integration remains a separate task using `docs/asset-plans/INTEGRATION-PROMPT.md` and the notes in `docs/asset-plans/oracle-park.md`.
