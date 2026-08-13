# 350 Brannan Street — build report

A validated miniature GLB of 350 Brannan Street, San Francisco: the 1929 three-storey
white-painted concrete industrial building on the corner of Brannan Street, Jack London
Alley and Varney Place, one lot northeast of South Park.

**This report beats the plan.** Where `docs/asset-plans/350-brannan.md` and this file
disagree, this file is what was built and why.

| | |
|---|---|
| Asset | `artifacts/350-brannan/350-brannan.glb` |
| Anchor (WGS84) | `-122.3935234, 37.7810229` |
| Target height | **13.85 m** (roof-penthouse crest; bbox top lands exactly on it) |
| Front heading | SE, outward normal **135.8°** true |
| Triangles | **6,776** / 10,000 budget |
| Objects | 133 |
| Dimensions | 33.27 × 33.30 × 13.85 m (AABB; the building is 21.6 × 24.2 m at 45°) |
| Materials | 10, all `Toy_*`, 2 of them `_Glow` |
| File size | 412 KB raw / 72 KB gzip (pre-optimize; budget is 500 KB compressed) |
| Validation | `validation.json` — **PASS**, all 16 checks |
| Blender | 5.2.0 LTS |

## 1. Dossier re-verification

Everything load-bearing in the plan was re-derived from source before modelling. Two
things needed correcting or hardening; the rest held.

**Confirmed unchanged**

- Anchor, footprint polygon, all four edge lengths and headings — recomputed from DataSF
  `ynuv-fyni` (`mblr = SF3775016`) and cross-checked against OSM way/113545692 (0.6% area
  agreement) and the DataSF parcel for APN 3775-016.
- 1929, three storeys, assessor construction class C. Assessor and all 25 building permits
  (1985–2026) agree on the storey count — unlike 380 Brannan, there is no conflict here.
- Roof deck 12.02 m, tallest feature 13.85 m (DataSF LiDAR).
- Three finished elevations and one blind southwest party wall.

**Hardened: the 2010 LiDAR is still current.** The plan asserted the crest without proving
the data had not aged. Checked: all 25 permits are interior work, reroofing (1990, 2010),
an elevator replacement, parapet bracing (1993) and a freight-elevator demolition (2023).
Nothing added height, so the 2010 LiDAR crest stands. This is exactly the check 550 Third
Street failed, and it is now recorded rather than assumed.

**Confirmed as a real trap: the address does not resolve to a building.** Nominatim
returns the Brannan Street *roadway* for "350 Brannan Street", and no footprint on the
block is tagged with that house number. The identification runs address → DataSF parcel
3775016 → parcel centroid → containing footprint, and is corroborated by a photograph of
the "350" plate beside the northeast portal. See `REFERENCE.md` §1.

**Not resolved: the Varney Place (northwest) elevation was never directly observed.**
Neither Varney Place nor Jack London Alley has Street View car coverage, and satellite
imagery resolves only the roof edge. That face is modelled as a plainer version of the
Jack London Alley elevation — same five-bay rhythm, one service door, no arch, no fire
escape. It is the least evidenced surface on the asset and the first thing a future
revision should attack.

## 2. What was built

A single chunky volume on the measured footprint at its real 45° heading, three storeys
of painted concrete, carrying one identity cue hard:

- **Two round-arched portals bookending the Brannan Street ground floor**, with pale
  cast-stone surrounds, framing a colonnade of five pier-separated storefront bays.
- Two upper floors of large steel-sash industrial windows, five bays per finished
  elevation, the top floor 3.2 m against the middle floor's 3.0 m — that difference is
  what stops them reading as office ribbon glazing.
- Ground-floor bays and one service door each on Jack London Alley and Varney Place; a
  blind southwest party wall.
- The black fire escape on the Jack London Alley elevation: two chunky landings, rails and
  one stringer, no treads.
- A designed roof: the 9 × 6 m penthouse that sets the 13.85 m crest, a four-box skylight
  row, an HVAC pair, a duct, a hatch and two vent stubs, inside a continuous parapet under
  a lighter coping.
- Night state: the two portals lit as entrances, plus six lit windows scattered across the
  Brannan and Jack London Alley elevations.

## 3. Deviations from the plan, and why

| # | Plan said | Built | Why |
|---|---|---|---|
| 1 | Arch surrounds `Toy_trim` (§2.8) | `Toy_stone` | `Toy_trim` (`f3efe6`) against the `Toy_cream` (`f2ede3`) body is a ~1% value step. In the first aerial the surrounds vanished completely and the portals read as blank arched bumps. `Toy_stone` (`d9d2c2`) separates and is honest to cast stone. |
| 2 | Portal glow `Toy_glassl_Glow` (§2.8) | `Toy_trim_Glow` | The portals are lit *entrances*, not glazing; a warm white reads as a doorway light where a blue reads as a window. Also keeps the palette-name convention 380 Brannan established. |
| 3 | Portals 3.0 m wide, rise 1.1 m (§2.7) | 3.20 m, rise 1.25 m | The plan authorised exaggerating the arches as the one place to spend it (§2.6). At the app's camera the survey-width arch was too small to carry. |
| 4 | Portal centres u = 2.00 / 19.60, bay pitch 2.92 m (§2.7) | u = 2.40 / 19.20, pitch 2.72 m | The original centres put the southwest portal on top of the corner jog. Moving both inward one third of a metre clears the corners and keeps the colonnade centred. |
| 5 | "one 2.6 m service door on each" NE/NW face, in addition to five bays (§2.7) | One of the five bays *becomes* the door | A sixth opening overran both elevations. The door is bay 0 on Jack London Alley (matching the 2008 permits' designated accessible entry) and bay 4 on Varney Place. |
| 6 | Attic panels 1.30 m wide (§2.7) | 2.60 m, aligned to the bay module | At 1.30 m they read as random tabs on the parapet rather than as a stepped crest — clutter, which the style bible's detail budget forbids on a secondary building. |
| 7 | — | Hero aerial shot from the **east** (az 100°), not the southeast | Square-on from the SE frames the Brannan front and the *blind party wall*. From the east both finished street elevations and the roof are in one frame, which is what the app's camera actually gets. |

Item 1 is the one that mattered: it was a genuine defect caught by following the
pipeline's "review the aerial FIRST" override, and it would have shipped an asset whose
single identity feature was invisible.

## 4. Iteration log

1. **Build v1** — 133 objects, 6,776 tris, crest exactly 13.85 m, min Z 0.0. Contract-clean
   on the first run.
2. **Aerial review v1** — three defects: (a) the arched portals read as blank bumps, because
   the frame panel was extruded *further* than its fill and swallowed it (the inverse of the
   ordering 380 Brannan uses) and because the surround colour was invisible against the body;
   (b) the attic panels read as noise; (c) the camera cropped the ground floor, i.e. the
   identity feature.
3. **Build v2** — fill protrusion corrected to sit proud of the frame, surrounds moved to
   `Toy_stone`, portals widened and re-centred, attic panels widened to the bay module.
   Aerial camera pulled back to `span × 3.6` on an 85 mm lens.
4. **Aerial review v2** — portals read clearly at both ends of the colonnade, the whole
   building is in frame, the roof furniture is legible, the fire escape reads on the alley
   elevation. Accepted.
5. **Formal rig** — four elevations, top, aerial and night rendered from the re-imported
   export at 64 Cycles samples; contact sheet assembled.
6. **Validation** — fresh-scene re-import, 16/16 checks PASS.

Triangle count did not change between v1 and v2 (6,776): the fixes were dimensional and
material, not topological.

**Two judgement calls worth recording.**

*The stepped attic panels.* In the flat orthographic elevations the five raised parapet
panels read slightly crenellated. They were kept, because the view that governs is the
app's aerial (style bible: judge from the high three-quarter camera first), where they
read as a gentle stepped crest, and because the real parapet does step over the pier
positions. If a reviewer dislikes them, the cheapest fix is dropping their rise from
+0.34 m to +0.18 m in `build_350_brannan.py`.

*What the night render can and cannot show.* `--night` previews the glow surfaces by
raising `Emission Strength`. Any value above ~1.0 clips these colours to white under the
Standard view transform, so `350-brannan-aerial-night.png` is evidence about **which
surfaces glow and how restrained the scatter is** — not about the night palette. The app
draws `_Glow` as an unlit overlay at the material's own baked colour, so the portals are
`Toy_trim` warm white (`f3efe6`) and the lit windows are `Toy_glassl` blue (`6f95b8`),
whatever the render shows. The rig's strength was lowered from 380 Brannan's 6.0 to 2.4
and the docstring now says this explicitly, so the next person does not read a palette
off an image that cannot carry one.

## 5. Validation summary

Fresh factory-reset scene, importing only the shipped GLB — the authoring `.blend` is
never inspected. Full machine-readable results in `validation.json`.

| Check | Result |
|---|---|
| Fresh isolated scene, re-imported final GLB | PASS |
| Metres, plausible dimensions | PASS — 33.27 × 33.30 × 13.85 |
| Crest normalised to target | PASS — bbox top 13.85 m exactly, loader scale 1.000 |
| Base at z = 0 | PASS — min Z 0.0 |
| Centred in XY | PASS — offset (0.036, −0.310) m |
| Under triangle budget | PASS — 6,776 / 10,000 |
| No image textures | PASS — 0 images, 0 textured materials |
| No transparency | PASS |
| Materials follow contract | PASS — 10 materials, all `Toy_*`, no `Toy_body` |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward — per-object signed volume | PASS — 133/133 enclose positive volume |
| Normals outward — ray residual | PASS — 0 flipped visible faces, 0.00% residual |
| No degenerate geometry | PASS — 0 degenerate triangles |
| No unexpected objects | PASS — no foreign or leaked geometry |

The per-object signed-volume test is the authoritative one for this union of
interpenetrating solids; the 31,500-ray visibility test is the secondary check, and here it
returned a zero residual rather than merely landing inside the 0.15% tolerance.

Materials shipped: `Toy_cream`, `Toy_glass`, `Toy_glass_Glow`, `Toy_glassl`, `Toy_ink`,
`Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_trim_Glow`.

## 6. Orientation note

Authored in true-world orientation (Blender `+Y` = north, `+X` = east) as
`docs/asset-plans/README.md` requires, so `placeGeneric()` drops it in at its real heading
without rotation. The asset contract's "front faces −Y" rule cannot be honoured literally
here: the Brannan Street front faces **southeast at 135.8°**. Real-world orientation wins
(AGENTS rule 5), and the axis-aligned bounding box is consequently 33.3 × 33.3 m for a
21.6 × 24.2 m building. That is the heading, not a scale error.

## 7. Draft manifest entry

Not applied — integration is a separate job (`docs/asset-plans/INTEGRATION-PROMPT.md`).

```json
{
  "id": "350-brannan",
  "file": "350-brannan.glb",
  "anchor": [
    -122.3935234,
    37.7810229
  ],
  "targetHeightM": 13.85,
  "cat": 3,
  "name": "350 Brannan Street",
  "estimated": false,
  "dims": [
    33.2738,
    33.2958,
    13.85
  ],
  "tris": 6776,
  "loadRadius": 2500
}
```

Integration is **Case B** (new landmark): it also needs a `pipeline/lib/landmarks.mjs`
entry and a tile re-bake. Measured exclusion band, from this anchor: our own footprint
centroid sits at ~0 m, the nearest *neighbour* ring vertex is at **13.79 m** (358 Brannan
Street and the untagged party-wall neighbour), and the next are at 19.6 m and 20.0 m —
so `exclude: 8` sits in the middle of the safe band. Do not raise it past 12. Batch mode
applies; see `docs/asset-plans/350-brannan.md` §2.13.

## 8. Approval

Pending — presented at stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`. The
approval quote and date go here verbatim before stage 4 begins.

## 9. Files

| File | What it is |
|---|---|
| `build_350_brannan.py` | deterministic build; rebuilds the GLB from scratch |
| `render_350_brannan.py` | review renders from the re-imported export (`--only aerial`, `--samples N`, `--night`) |
| `validate_350_brannan.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | assembles the contact sheet from the elevation renders |
| `350-brannan.blend` | authoring scene |
| `350-brannan.glb` | **the asset** |
| `350-brannan-{north,east,south,west,top}.png` | controlled elevations, one shared rig |
| `350-brannan-aerial.png` | hero three-quarter aerial, from the east |
| `350-brannan-aerial-night.png` | night state |
| `350-brannan-contact-sheet.png` | contact sheet |
| `REFERENCE.md` | research dossier and sources |
| `validation.json` | machine-readable validation |
