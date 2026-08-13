# 234 Van Ness Avenue (The Kelsey Civic Center) — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed 13 August 2026
against the plan in `docs/asset-plans/234-van-ness.md`.

**Result: the exported GLB passes every contract check.**

## 1. Shipped numbers

| | |
|---|---|
| File | `234-van-ness.glb` |
| Objects / triangles | 790 / **11,656** (cap 24,000) |
| Dimensions (m) | **56.278 × 46.427 × 30.120** |
| min Z | 0.0000 |
| XY centre offset | (0.0000, −0.5995) — within the 1.0 m tolerance |
| Materials | 18, all `Toy_*`, no `Toy_body` |
| Glow materials | `Toy_glassl_Glow`, `Toy_trim_Glow` |
| Image textures / transparency | none / none |
| Cameras / lights / animation / armatures / constraints | 0 / 0 / 0 / 0 / 0 |
| Degenerate triangles | 0 |
| Inverted objects (signed volume) | 0 of 790 |
| Normal ray residual | **0.0000 %** (31,500 rays from 9 interior targets) |
| Anchor | `−122.4193071, 37.7780541` |
| Front heading | 261.8° true — Van Ness Avenue, facing west |
| Target height | **30.120 m**, so `targetHeightM / measuredHeight` = 1.000 |

`validation.json` carries the full machine-readable report; every entry in its
`checks` block is `true` and `overall` is `PASS`.

## 2. Dossier verification — the plan held

Re-verified before modelling, per the stage-2 override. **Nothing in §2.3–2.4 of
the plan needed correcting**, which is unusual in this repo and worth recording:

- **Heights.** Re-read off WRNS Studio's dimensioned `SOUTH ELEVATION - TOM
  WADDELL`. Level 1 at 0'-0" with a 15'-0" storey, levels 2–8 at 9'-11",
  ROOF 84'-5" = 25.730 m, copper fascia +3'-6" = 26.797 m, mechanical penthouse
  +14'-5" over the roof = 30.124 m, normalised to **30.120**. The published
  "84 feet above Van Ness" is the roof, not the crest — both are recorded, and
  the crest is what the bbox top and the manifest use.
- **Footprint.** OSM ways 1547771521 + 1547771522 unioned: 1,304 m² against the
  geotechnical report's 13,815 sq ft (1,283 m²), a 1.6 % agreement. That is the
  evidence that two untagged, one-week-old OSM traces are this building.
- **Anchor** re-derived as the ring AABB centre: `−122.4193071, 37.7780541`.
- **Orientation.** Authored +Y = true north. The address front faces **west**,
  so the contract's "front faces −Y" cannot be honoured literally; real-world
  orientation wins (AGENTS rule 5), as it does for every landmark in this repo.

### Deliberate simplification of the survey ring

The measured ring, expressed in the building's own 80.75° grid, is rectilinear
to within 0.30 m. The model is built on a **regularised L** —
`u ∈ [0, 54.06] × v ∈ [0, 15.47]` plus `u ∈ [31.70, 54.06] × v ∈ [15.47, 36.58]`
— which lands at 1,308 m² against the measured 1,304 m² (+0.3 %). No vertex
moves more than 0.30 m. The 80 mm wobble in the east party line is survey noise,
not architecture, and the L is what the eye reads.

## 3. Departures from the plan

1. **The courtyard's open void is 15.80 × 18.30 m ≈ 289 m², not the published
   3,450 sq ft (320 m²).** The published figure is the *garden courtyard* as
   programmed, which includes the covered ground-level area under the arched
   passage; the modelled open-to-sky void is the part the app's camera can see.
   The floor plate this produces — ≈ 989 m² over seven residential floors — is
   what 112 units actually needs, which is the cross-check that the courtyard is
   in roughly the right place. **Its position remains the largest inference in
   this asset** (REFERENCE.md §8.1).
2. **The party walls are near-blank, not "sparse punched windows".** The plan
   said sparse; the first render made clear that even a sparse *regular grid*
   over a 36.6 m lot-line wall reads as a generic office block (style bible §27).
   The east wall against 101 Grove now carries three high openings; the two
   lot-line walls facing the open sliver lots carry a staggered scatter on the
   upper floors only. This removed 142 objects.
3. **Render engines are split, and that is a compromise, not a preference.** The
   six day views are **Blender Workbench** — the sanctioned headless path
   (`sf-asset-check`: "no GPU, so use Workbench or CPU Cycles") — because this
   machine was running five other landmark sessions' renders concurrently at
   load averages between 100 and 750, and the CPU-Cycles rig could not complete
   a single frame. The night aerial is **Cycles**, because Workbench does not
   render emission and a Workbench "night" image would have been the day image
   with a dark background, which is worse than useless. Every image depicts the
   same exported GLB, and the four elevations share one rig. The rig still
   supports the full Cycles pass (`render_234_van_ness.py` with no `--workbench`
   flag, `--samples` to taste); it is worth re-running when the machine is idle.

## 4. Iteration log

Every pass was judged from the high three-quarter aerial first, per the stage-2
override and style bible §18.

| Pass | What the render showed | What changed |
|---|---|---|
| 1 | The Van Ness canopy cantilevered 2.6 m out over the street, pushing the bbox 2.6 m south and the XY centre 1.383 m off — past the 1.0 m tolerance | Canopy stops at the building line on Van Ness and covers the Waddell sidewalk only. Centre offset → 0.600 m |
| 2 | Party walls carried a full 7×7 grid of square windows — the "generic office block" failure mode, and untrue of a wall built to a lot line | East wall cut to three high openings; the two lot lines to a staggered upper-floor scatter. 909 → 767 objects |
| 3 (top view) | The roof was one undifferentiated tray; the five planters read as green swimming pools; the east bar and Grove wing roofs were empty | Pale-grey membrane with cream pavers **only** over the amenity deck; wider dark planter rims; added the skylight run, two mechanical clusters and a duct run; two-tone courtyard floor |
| 4 (aerial) | Overcorrected — the planters now read as five **black cushions**, and the mechanical screen was one black slab swallowing the roof | Planting stands proud of a low bronze rim; screen cut from 9.2 × 6.2 m to 5.8 × 3.4 m over a pale penthouse |
| 4 (west/south) | The corner bay read as a navy billboard bolted to the corner, and 54 m of Waddell base was blank concrete | Bay given pale end cheeks, four charcoal mullions and floor bands; base given three aluminium vents and two recessed panels |

## 5. What the asset is

An eight-storey L on the regularised survey footprint, wrapping the 171 Grove
corner lot it does not own. Calm outside, loud inside:

- **Street elevations** — a 15'-0" textured-concrete base under seven floors of
  broad white fibre-cement bands alternating with charcoal window-wall bays,
  divided by slim copper-anodized fins running the full seven storeys, capped by
  a copper fascia at 25.73 → 26.80 m. A scatter of coral accent panels. At the
  Van Ness/Waddell corner, a projecting glazed bay with pale cheeks and charcoal
  mullions over a copper soffit and a wood-slat trellis canopy.
- **The courtyard** — the identity, and the only one the app's downward camera
  can see. ~40 full-height vertical stripes in sky blue, coral, mustard, olive,
  pale blue, cream and charcoal from a fixed deterministic sequence; six
  open-air access galleries with a warm orange-red end screen on the west wall;
  a mustard party wall on the east; a big soft segmental arch; pale two-tone
  paving with planters and three chunky trees.
- **The roof** — a pale-grey membrane with a cream-paved amenity deck at the
  west end facing City Hall, five bronze planters with proud green planting,
  four benches, a picket guardrail, a skylight run over the top-floor corridor,
  two mechanical clusters, and the penthouse whose screen sets the 30.120 m
  crest.
- **Night** — the courtyard is the hero (a floor wash plus a festoon line), a
  scatter of 20 lit apartment bays across Waddell, Van Ness and Grove is the
  support, and the Van Ness lobby glazing is lit. Nothing on the roof glows.

## 6. Manifest entry (draft — not applied in this stage)

```json
{
  "id": "234-van-ness",
  "file": "234-van-ness.glb",
  "anchor": [-122.4193071, 37.7780541],
  "targetHeightM": 30.12,
  "cat": 2,
  "name": "The Kelsey Civic Center (234 Van Ness Avenue)",
  "estimated": false,
  "dims": [56.278, 46.427, 30.12],
  "tris": 11656,
  "loadRadius": 2500
}
```

`estimated: false` — the height is measured off the architect's dimensioned
elevation, not inferred. `cat` 2 is Apartments. `loadRadius` follows the default
rule `max(2500, 30.12 × 30)` = 2500 m.

## 7. Carried forward to stage 5

**The exclusion radius takes a standing building with it, and that is the one
thing about this landmark that makes the city less accurate.** Measured against
`pipeline/data/buildings_datasf.geojson` — the file the bake actually reads —
the two demolished footprints on the site (`SF0811018`, `SF0811019`) and the
still-standing 171 Grove corner building (`SF0811020`, 9.71 m) all present a
vertex at the same 6.14 m from the anchor, because they share a party wall. No
radius drops the first two without the third. `exclude: 14` is shipped, and the
loss is flagged rather than hidden; a follow-up 171 Grove asset would close it.
