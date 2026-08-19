# One Steuart Lane — build report

`artifacts/one-steuart-lane/one-steuart-lane.glb` — a miniature of SOM's 2021
condominium tower at 1 Steuart Lane / 75 Howard Street, built for the SF-SIM
toy-diorama city. Authored 18 August 2026 from
`docs/asset-plans/one-steuart-lane.md`; the dossier behind every number is
`REFERENCE.md`, which **beats the plan** wherever they differ.

## Shipped numbers

| | |
|---|---|
| Triangles | **17,064** / 24,000 budget |
| Objects | 1,027 (the loader merges them to one body mesh + one glow set) |
| Dimensions | 62.95 x 62.493 x **67.06** m |
| Min Z | 0.000 | 
| XY centre offset | 0.0002, −0.0007 m |
| Loader scale factor | **1.000000** (`targetHeightM / measuredHeight`) |
| Materials | 13, all `Toy_*`, 3 of them `_Glow` |
| Image textures / transparency | 0 / 0 |
| Cameras, lights, animation, armatures, constraints | 0 |
| Normals | PASS — 0 inverted signed volumes, ray residual **0.0000%** (gate 0.15%) |
| Anchor | `-122.3916888, 37.7915643` |
| Headings | Steuart NE **44.2°** · SE **134.8°** · SW **224.5°** · Howard NW **314.9°** |

`validation.json` records the full fresh-scene re-import report. **Overall: PASS**,
15 of 15 contract checks.

The XY bounding box is 62.95 x 62.49 m even though no elevation is longer than
47.0 m: that is the 45°-heading bounding box of a 40.5 x 47.0 m lot (62.10 x
61.65 m) plus the 0.44 m travertine frame projection and the 3.4 m entrance
canopy that oversails the Steuart Lane sidewalk. Not a scale error.

## Files

| File | What |
|---|---|
| `build_one_steuart_lane.py` | deterministic build; `blender -b --python build_one_steuart_lane.py` |
| `one-steuart-lane.blend` | the authored scene |
| `one-steuart-lane.glb` | **the asset** |
| `render_one_steuart_lane.py` | review rig; `-- --fast` for Workbench/EEVEE, `--night`, `--only top\|aerial\|elev` |
| `validate_one_steuart_lane.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes the contact sheet from the rendered tiles |
| `one-steuart-lane-{top,north,east,south,west,aerial,aerial-night}.png` | review renders |
| `one-steuart-lane-contact-sheet.png` | all seven in one sheet |
| `REFERENCE.md` | the research dossier, sources, and every correction |

Elevation names are a quarter-turn relabelling of the true face normals, because
the building stands at 45° to the compass: `north` = Steuart Lane (NE 44.2°),
`east` = the south-east flank (134.8°), `south` = the south-west flank (224.5°),
`west` = Howard Street (NW 314.9°).

## What it captures

1. **The stack.** Five volumes of three to four storeys on a two-storey base,
   each stepping back on one pair of sides while cantilevering out over the
   volume below on the other pair, so the east corner zig-zags. On the Steuart
   elevation the successive wall planes stand at 23.49, 18.89, 22.69, 17.89 and
   21.69 m from the anchor.
2. **The travertine cage.** A cream lintel at every floor line and a cream
   pilaster at every module boundary, standing 0.44 m in front of dark recessed
   glass, with the bay module deliberately irregular (the real curtain wall
   cycles 4 / 6 / 8 ft panels).
3. **The terraces.** A thin bright cantilevered slab plate with a dark soffit at
   every junction, a pale balustrade and planters where the volume above is set
   back, and one module-wide slot of deep terraces running up each elevation.
4. **The base.** A double-height dark storefront divided by clusters of vertical
   travertine baguettes, the Steuart Lane entrance in a bronze portal under a
   projecting glass canopy, and a planted set-back amenity level above.
5. **The roof.** Cream parapet, a field of dark PV strips in two bays split by a
   pale walkway, two round cooling towers with a row of plant boxes, the
   mechanical penthouse box (the crest at 67.06 m), and a BMU crane on its track.

## Night state

The real building is downlit from beneath its cantilevers, so the hero glow is a
thin cream line under each of the four terrace slabs plus the base cornice —
**five horizontal bands that restate the horizontal massing** — supported by a
warm gold lobby patch on Steuart Lane and a sparse scatter of pale blue lit
units (never a whole floor, never a regular pattern). Nothing else glows.

Glow materials: `Toy_cream_Glow` (f2ede3), `Toy_gold_Glow` (caa64a),
`Toy_glassl_Glow` (6f95b8). All three are thin single plates, never closed
shells — a closed glow shell stacks two alpha layers and tints the surface it
wraps by day.

## Dossier corrections made during the build

Full detail in `REFERENCE.md` §7. In short:

1. **The massing is not a ziggurat.** The first build used monotonically
   shrinking concentric setbacks and read as a wedding cake. The published
   description is "five masses **cantilevered** over ... private terraces" —
   they alternate. Rebuilt with alternating per-edge insets.
2. **Recessed plates are invisible.** The glass was first authored at a negative
   offset, i.e. inside the solid volume shell, and the whole tower rendered blank
   cream. Every surface stands proud of the shell; the recess comes from the
   frame standing in front of the glass.
3. **Roof furniture belongs inside volume E's plan, not the lot's** — E is 27.1 m
   across against the lot's 47 m, and the first roof hung cooling towers in
   mid-air.
4. **The night rig was rendering white.** glTF writes `emissiveFactor = 0` when
   the authored emission strength is 0, so raising `Emission Strength` on a
   re-imported `_Glow` material gives it a default white emission.
   `light_glow()` now copies Base Color into Emission Color at strength 1.0,
   which is what the app does. Fixed before the night render was judged.
5. **`Toy_roofd` is not used.** It renders near-black under the app's lighting;
   the roof deck is `Toy_steel`.

Two plan values were *confirmed*, not corrected: the 67.06 m height (the plan's
reasoning holds — see the open risk below) and the four face headings.

## Open risk carried forward

**The height is disputed and was not independently measured.** SOM, Swinerton,
the developer's release, SF YIMBY and OSM all say 220 ft = 67.06 m, and that is
what shipped. CTBUH and the SF Chronicle say 240 ft. The arithmetic mildly
favours 240 (20 storeys in 220 ft with a 24 ft entry level leaves ~10 ft
floor-to-floor). A rectified facade elevation from Street View panorama
`FgQeEOFiFPKjWDAfs-1pNg` would settle it and was **not attempted**. If 240 ft
turns out to be right, the fix is a one-line change to `H_CREST` and a rebuild —
the tower body is authored at absolute heights, so nothing else moves.

Setback depths are inferred, sized only by a gross-floor-area cross-check
(~29,600 m2 modelled against 335,000 sq ft = 31,120 m2 published, −5%).

## Renders

Reviewed from the high three-quarter aerial first, iterated three times, then the
formal rig. Rendered with the Workbench/EEVEE fast path rather than Cycles: this
machine was carrying 97 parallel Blender sessions at load 67 while this asset was
built, and a Cycles frame was not going to finish. The flat-colour toy palette
survives the swap; the night pass runs on EEVEE, which is emission-capable.

`one-steuart-lane-contact-sheet.png` carries all seven tiles.

## Manifest draft

Do **not** apply this here — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md`).

```json
{
  "id": "one-steuart-lane",
  "file": "one-steuart-lane.glb",
  "anchor": [-122.3916888, 37.7915643],
  "targetHeightM": 67.06,
  "cat": 2,
  "name": "One Steuart Lane",
  "estimated": false,
  "dims": [62.95, 62.493, 67.06],
  "tris": 17064,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, targetHeightM × 30)` =
`max(2500, 2012)` = 2500. This building was explicitly designed not to have
skyline presence ("It's a tall building, but we weren't trying to have a presence
on the skyline" — SOM's design director), so `alwaysLoaded` would be wrong for it.

Case B integration notes, including the `exclude` sizing, are in
`docs/asset-plans/one-steuart-lane.md` §2.13.

## Approval

*(stage 3 — to be filled in with the user's approval, quoted verbatim, and the
date)*
