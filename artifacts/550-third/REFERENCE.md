# 550 Third Street — reference dossier

Research behind `550-third.glb`. Compiled 12 August 2026 for the SF-SIM
toy-diorama city. Everything below is either **measured** (from an API or a
public dataset, reproducible), **documented** (stated in a permit or a
publication), or **inferred** (read off an image). The three are never mixed in
the same row.

This dossier re-verified the plan in `docs/asset-plans/550-third.md` rather than
trusting it. Corrections found are in §7.

## 1. What the building is

550 Third Street is a two-storey brick-and-timber warehouse of 1921 on the
south-west side of 3rd Street at South Park, in SoMa/South Beach. It is a
**through lot**: it runs the full block depth from 3rd Street back to Ritch
Street, with party walls against its neighbours on both long sides. Between 2022
and February 2025 it was gut-renovated into a single-tenant creative office —
new lobby stair, a double-height atrium with tiered seating, walkable skylights,
and, decisively for this model, a new elevator and stair to the roof with a roof
deck and a penthouse.

It is not a landmark in the civic sense. It is in the set because the app's
camera looks down, and this is a building whose entire character is its roof.

## 2. Sources and what each establishes

| Source | Establishes | Kind |
|---|---|---|
| [OSM way/124889472](https://www.openstreetmap.org/way/124889472) | the footprint polygon, `addr:housenumber=550`, `addr:street=3rd Street`, `height=7` (traced from Bing) | measured (geometry) / unreliable (height) |
| [DataSF building permits `i98e-djp9`](https://data.sfgov.org/resource/i98e-djp9.json), block 3776 lot 005 — 36 records, 1992–2025 | storey count (2), construction type 3, the 1992 parapet bracing, the 2023 roof-deck/penthouse/elevator scope and its **2025-02-25 completion**, the rear garage doors and property-line windows, the atrium tiered platform and walkable skylights, four rooftop heat pumps | documented |
| [DataSF LiDAR building footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json), record `SF3776005` | 4,151 half-metre cells (≈1,038 m²), ground mean 6.41 m, first-return median 13.60 m NAVD88, **height median 7.23 m** | measured (2010) |
| [startuphq.com/southpark](https://www.startuphq.com/southpark) | frames of the architect's December 2022 Design Development set: the roof axonometric, a cut axonometric through the 3rd Street end, the penthouse interior, the atrium. The strongest massing reference available. | documented drawing / inferred detail |
| LoopNet / Showcase / Digsy listings | built 1921, 25,000 sf, two-storey creative office, 2,600 sf rooftop penthouse, 1,400 sf atrium | documented (commercial) |
| Google Maps satellite (Airbus / Maxar / Vexcel, 2026 tiles) | footprint and block context. **Its roof imagery predates the 2025 works** and shows the old plain roof — not used for roof design. | measured (plan) / stale (roof) |

Nothing here relies on a single photograph, a single AI-generated image, or an
unsourced 3D model.

## 3. Verified dimensions and location

| Item | Value | Kind |
|---|---|---|
| Parcel | Block 3776, Lot 005 | documented |
| Anchor (WGS84) | **-122.3953409, 37.7804407** — footprint AABB centre | measured |
| Footprint area | 1,070 m² (11,521 sf) | measured, shoelace on the OSM polygon |
| Overall bar | 48.4 m deep × 23.0 m wide | measured |
| 3rd Street frontage | 23.05 m | measured |
| Ritch Street frontage | 21.79 m | measured |
| Long-axis heading | 45.3° / 225.3° true | measured |
| 3rd Street front outward normal | 44.6° true (north-east) | measured |
| Main roof | 7.23 m above grade | measured (2010 LiDAR median) |
| Modelled roof membrane | 7.45 m (LiDAR + deck build-up) | derived |
| Street parapet | 9.00 m | inferred from the DD cut axonometric |
| Side / rear parapet | 8.20 m | inferred |
| **Architectural crest** | **11.00 m** (penthouse roof slab) | **estimated — see §8** |

The footprint reprojected with the app's tangent projection and recentred on the
AABB centre, CCW, (x east, y north), metres:

```
v0 (-24.507,  -8.943)   west corner   — Ritch / NW party wall
v1  (-9.891, -25.104)   south corner  — Ritch / SE party wall
v2   (7.515,  -7.915)   kink in the SE party wall
v3  (24.507,   8.932)   east corner   — 3rd St / SE party wall
v4   (8.087,  25.104)   north corner  — 3rd St / NW party wall
```

Two independent checks that this is the right building:

* 1,070 m² × 2 floors + a 2,600 sf penthouse ≈ 25,600 sf, against the listings'
  "25,000 sf".
* The LiDAR footprint's 4,151 half-metre cells give ≈1,038 m², within 3% of the
  OSM polygon.

## 4. Orientation

The SoMa grid here is rotated ~45° from true north. 3rd Street and Ritch Street
both run 134.8°/314.8°; the building sits square to them, so its long axis runs
45.3° and its street front faces north-east.

The asset is authored in true-world orientation, `+Y` = north, `+X` = east,
because `placeGeneric()` in `app/src/assets.js` scales and positions but never
rotates. The contract's "front faces −Y" therefore **cannot** be honoured — the
real front faces north-east. Real-world orientation wins (AGENTS rule 5, and the
orientation note in `docs/asset-plans/README.md`).

## 5. What each side shows

**North-east — 3rd Street, the public face.** 23 m wide, two storeys of painted
masonry under a tall solid parapet that screens the roof deck. Pilaster strips
divide the wall; two large industrial steel-sash window grids sit at both levels;
a recessed entry with a dark door and a transom is set off to one side. The
street numerals are on the building. Street trees stand in front of it but belong
to the city, not the asset.

**South-east — the long party wall, ~48 m.** Blind painted masonry, with a
regular rhythm of small punched square windows high up (the "fixed property line
windows" the 2023 permit added) and a dark coping line.

**South-west — Ritch Street, the service face.** 21.8 m wide, the plainest
elevation: two roll-up garage doors reinstated at ground level under a steel
lintel, a pedestrian door, and a window band above.

**North-west — the long party wall, ~47 m.** Blind painted masonry, featureless.

**Top — the primary facade.** Front to back: the garden deck behind the tall
street parapet (pavers, lawn, hedge planters, lounge, fire pit, long table); the
glass penthouse pavilion under a thin cantilevered slab; a mono-pitch stair
penthouse with a linear skylight and an elevator overrun beside it; five large
rectangular skylights in a row; a paver walk dog-legging between them; and the
mechanical cluster of four heat pumps at the Ritch Street end.

## 6. Recognition cues, ranked

1. **The skylight row** — five big glazed rectangles marching down a long low
   white roof. Nothing on the block reads like it from above.
2. **The glass penthouse under its thin floating slab**, with green deck around it.
3. **The proportion** — 48 m long, 23 m wide, two storeys: long and low where its
   neighbours are short and tall.
4. **The 3rd Street front** — tall blank parapet over two big steel-sash grids
   and a small dark recessed entry, with oversized 550 numerals.
5. **The punched property-line window rhythm** on the long blind wall.

### Preserved

The true footprint including the kink at v2; the two-storey proportion; the
five-skylight rhythm and spacing; the penthouse's floating-slab profile; the
green deck as a distinct colour zone; the tall street parapet.

### Simplified

Steel-sash grids become a recessed reveal, one glass slab and a mullion grid —
rhythm, not mullion count (style bible §5). Skylights are simple curbs with a
raised pane. Roof furniture is a handful of chunky primitives. Hedges and lawn
are single flat volumes. The 550 numerals are extruded block glyphs on the
parapet at ~4× realistic size (§8, §9).

### Deliberately omitted

The DD axonometric shows two sculptural built-in bench forms mid-roof. They were
dropped: at city scale they compete with the skylight rhythm, which is the whole
identity, and §10 asks for clear clusters rather than scattered props. Nothing
tower-like, crowned or curved was added — the building's charm is that it is long,
low and quiet with one jewel on top.

## 7. Corrections to the plan's dossier

The plan (`docs/asset-plans/550-third.md`) survived verification with two
adjustments, both recorded in `REPORT.md`:

1. **Duct position.** The plan put the two roof duct runs at the same station as
   the fifth skylight; they intersected it. Moved inboard to u −13.5.
2. **Glow-shell offsets.** The plan did not specify a clearance between a glow
   shell and the opaque surface behind it. Coincident faces z-fight, and at the
   app's 12% day alpha that reads as a triangulated smear across the glass. Every
   glow shell is now inset in plan and lifted clear.
3. **Facade openings must be built PROUD of the wall.** The plan's §2.7 gave
   window and door depths as recesses (negative depth). The walls are solid
   prisms with no cut openings, so every reveal, pane, mullion, garage door and
   entry panel was buried inside the shell and invisible — the first aerial
   review render showed a completely blank 3rd Street elevation. All facade
   assemblies now sit 0–0.16 m out from the wall plane, and the apparent recess
   comes from the pilasters standing 0.20 m in front of them.
4. **Exclusion radius: 8 m, not the plan's 12 m.** §2.13 guessed 12 and said to
   verify. Measured against the actual bake-side geometry (DataSF footprints,
   simplified at the pipeline's 0.6 m tolerance, `ringCentroid`): this building's
   ring centroid is 0.96 m from the anchor, and the nearest *neighbour* vertex is
   11.17 m (SF3776007), with SF3776008 at 12.19 m. The window that drops only
   this building is therefore 0.96 < r ≤ 11.17. **12 would have deleted the
   neighbour at SF3776007.** 8 m sits in the middle of the window.

None of these changes a researched fact about the building.

## 8. Uncertainties and conflicting evidence

* **The crest height is estimated.** 7.23 m to the main roof is measured, but
  from 2010 LiDAR — three years before the penthouse was permitted and fifteen
  before it was finished. 11.00 m assumes one ~3.6 m storey above the roof deck,
  consistent with the DD cut axonometric's proportions and with a 2,600 sf
  occupiable penthouse rather than a bare stair box. A measured elevation, a
  planning drawing, or a dated photograph against a known neighbour would replace
  the estimate. If it moves, only `targetHeightM` and the penthouse volume move;
  the shell is measured.
* **OSM `height=7` and the LiDAR median agree — and both are wrong** as a target
  height, because both describe the pre-2023 building. This is the sharpest case
  in the set of the README's warning about OSM height tags.
* **Which long wall carries the property-line windows** is inferred from a single
  axonometric. The model puts them on the south-east wall. Getting it backwards
  would put the only articulation on the wrong side; it would not affect massing.
* **The DD frames date from December 2022**; the permit completed February 2025.
  The massing is safe; the deck furniture layout is the least certain part and is
  modelled as a plausible arrangement of the documented elements rather than a
  survey.
* **Google's satellite roof imagery is stale.** It shows the old plain roof. The
  model was not corrected against it, deliberately.

## 9. Scope of the export

**In:** the building, parapets, roof membrane, roof deck with its fixed furniture
and landscaping, penthouse, stair penthouse, elevator overrun, five skylights,
paver walk, mechanical plant, the 550 numerals.

**Out:** 3rd Street, Ritch Street, South Park, the neighbours at 560 3rd and
521–527 3rd, street trees, street furniture, people, vehicles, plinths, cameras,
lights.
