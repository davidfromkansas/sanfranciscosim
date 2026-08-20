# 414 Brannan Street (Epic Church) — reference dossier

Compiled 18 August 2026 for `artifacts/414-brannan/`. Everything below was
re-verified for this build rather than inherited from
`docs/asset-plans/414-brannan.md`; the corrections that came out of that
re-verification are listed in `REPORT.md`.

## 1. Identity

A 1924 board-formed concrete industrial building on the west corner of Brannan
and Ritch Streets in SoMa. Built as a trade shop (the Lera Electric Company use
that later kept the building's "general office" grandfathering through a 2017
planning appeal), it ran through Hattery, 1776 and OnePiece Work as co-working
space before **Epic Church San Francisco** bought it on 4 August 2022 for about
$12M, spent roughly $5M converting it, and opened it as their permanent home on
**8 December 2024**.

- Architect of the conversion: **Quezada Architecture** (19,840 sf)
- Structural engineer: **FTF Engineering** — ASCE 41 seismic retrofit of the
  unreinforced concrete walls, added shear walls on the blind sides, FRP-wrapped
  long-span beams under the sanctuary, **original timber roof trusses kept
  exposed**
- No architect is recorded for the 1924 original in any source consulted.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF EAS Addresses (`ramy-di5m`) | `414 BRANNAN ST` → parcel 3776011; it is the **only** address on the lot |
| DataSF Parcels (`acdm-wktn`) | the 530.0 m2 parallelogram, address range 414–414, CMUO zoning |
| DataSF Building Footprints (`ynuv-fyni`) | three LiDAR strips under `mblr = SF3776011`, heights 10.32 / 13.47 / 11.19 m |
| SF Assessor secured roll 2025 (`wv5m-vpq2`) | 1924, 3 storeys, 19,548 sq ft property / 5,852 sq ft basement, welfare exemption, 4 Aug 2022 sale |
| ftfengineering.com/portfolio_page/epic-church | 1924 industrial, board-formed concrete, exposed timber roof trusses, 19,840 sf, all existing openings maintained |
| qa-us.com/project/epic-church | the conversion programme (300-person assembly, café, baptismal pool) |
| sfstandard.com, 10 Jul 2023 | the ~$12M purchase and ~$5M renovation |
| epicsf.com/from-pastor-ben/get-inside-the-story | purchase and opening dates |
| socketsite.com, May 2017 | the Lera Electric legacy use and the co-working history |
| Street View pano `zPv7IB2PjEsWarb0iZ412A` (2021) | the near-orthogonal frontal elevation used for the photogrammetry in §5, and the pre-renovation colours |
| Street View panos `7K6Zh27rKJrFXkI8GmGICw`, `moQcOx7ROM7r7vcRJw04_g` (2025) | the current teal arch and slate body; the sampled hexes in §6 |
| Street View pano `Ow9JzQw5-zEmgIHf_Qk3zw` (2025) | the oblique from the Ritch corner — the only frame that shows the three Juliet balconies |
| Street View panos `auyEb77HUzoro0gQF5UIYg`, `SAz7nIhGlLCIhM4mORH_HQ` | the Ritch Street elevation, its stepped parapet and the tile return |
| Google satellite z21 tiles, stitched and overlaid with the parcel + footprint rings | the roof: light membrane, the tile line seen from overhead, the ficus canopy over the southeast corner of the lot |

No copyrighted imagery is committed; the panoids and tile URLs above reproduce
every frame used.

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | **-122.3948685, 37.7799308** | measured — the parcel AABB centre, the parcel centroid, the EAS address point and the assessor's `the_geom` all agree within 0.02 m |
| Brannan frontage | **24.90 m** | measured, parcel polygon |
| Depth | **21.28 m** | measured, parcel polygon |
| Parcel area | 530.0 m2 | measured |
| Built area | 505.6 m2 (95% lot coverage) | measured, LiDAR strips clipped to the parcel |
| Street parapet / clay-tile ridge | **10.39 m** | measured, photogrammetry §5; LiDAR NE-bay median 10.32 m |
| Southwest bay deck | 11.19 m | LiDAR median over 704 cells |
| Roof monitor deck / crest | 13.47 m / **14.00 m** | LiDAR median over 718 cells / `hgt_max`, +0.74σ — not an outlier |
| Ground-floor opening head | 4.58 m | photogrammetry |
| Upper window sill / head | 5.75 / 8.10 m | photogrammetry |
| Frieze band underside | 9.22 m | photogrammetry |
| Brannan front heading | 135.2° (SE) | measured |
| Ritch front heading | 225.2° (SW) | measured |

Build polygon, Blender metres, `+X` east `+Y` north, centred on the anchor
(a true four-vertex parallelogram — no simplification was needed):

```
(-1.325, -16.306)   S corner — the Brannan / Ritch street corner
(16.353,   1.237)   E corner — Brannan frontage, party line with 400 Brannan
( 1.325,  16.306)   N corner — rear, northeast end
(-16.353, -1.237)   W corner — rear, southwest end
```

## 4. Observations from all four sides and above

**Southeast — Brannan Street (24.90 m), primary.** A **projecting clay-tile pent
roof** in barrel tile runs the full width over a **vermilion frieze band** about
1.1 m tall; below that the slate blue-gray wall runs unbroken to the pavement —
**no base course, no cornice**. Upper floor: punched rectangular windows,
charcoal frames, a large upper light over a two-light row, light stone sills.
The three southwest-most of them carry **curved wrought-iron Juliet balconies**;
a row of mature ficus hides them in every frontal frame. Ground floor: tall
recessed bays (head at 4.58 m) with dark bronze frames around 3-part **frosted
white glazed panels** over **louvred grilles**, separated by plain piers; toward
the southwest the bays give way to large flat blank recessed panels. At the
northeast end, hard against the party line, the **teal arched entry**: round
arch, moulded surround, a cream fan tympanum with a circular medallion at its
centre, a recessed dark doorway behind a diamond-lattice gate.

**Southwest — Ritch Street (21.28 m), secondary but real.** The tile pent
**returns about 6 m round the corner** and then the parapet **steps up toward the
rear**. Along the wall: a rhythm of smaller punched upper windows, a **round wall
plaque** high on the rear half, one more Juliet balcony at the Brannan end, the
Epic Church sign beside a frosted storefront bay, **two roll-up doors** and a
large **louvred vent grille**.

**Northeast — party wall against 400 Brannan.** Blank; invisible from any street
but visible from the app's aerial camera. Finished, quiet wall plane.

**Northwest — rear.** Blank painted concrete against the block interior and the
566–586 Third Street complex behind.

**Top.** Three flat membrane decks with the middle bay's **raised monitor**
dominating: a full-bay-width volume set back from the Brannan parapet, crest at
14.0 m. Light membrane, a loose scatter of small vents and units, one
skylight-sized element. The large dark blob over the lot's southeast corner in
nadir imagery is the ficus canopy, not a roof feature. The **tile line is the
single most identifying thing about this building from directly overhead**.

## 5. Independent height measurement

Photogrammetry on pano `zPv7IB2PjEsWarb0iZ412A`, rendered `pitch=0`,
`thumbfov=90`, 1024 x 640 (so `f = 512 px`, facade parallel to the image plane).

The pano's own reported position puts the lens 15.78 m from the facade. That was
**not used**. Both ends of the 24.90 m frontage are visible — the Ritch corner at
`x = 155`, the 400 Brannan party line at `x = 862` — which solves the geometry:

```
D = 18.03 m (perpendicular),  s = 0.12 m (along-facade offset)
```

a 2.25 m disagreement with the metadata. Heights then follow from
`h = D · (y_ground − y)/f`, anchored on the ground line so camera height never
enters:

| feature | image y | height |
|---|---|---|
| clay-tile ridge | 101.7 | **10.39 m** |
| frieze underside | 135 | 9.22 m |
| upper window head | 166.7 | 8.10 m |
| upper window sill | 233.3 | 5.75 m |
| ground-floor bay head | 266.7 | 4.58 m |

10.39 m against the northeast bay's LiDAR median of 10.32 m — 0.07 m apart from
two unrelated instruments, which is what licenses the rest of the table.

The raised mass behind the parapet measures 8.45 m wide, centred 0.3 m southwest
of the facade centre — i.e. exactly the middle structural bay — with its top
between 13.0 m (if it stood in the facade plane) and 14.1 m (with a 2 m setback).
The 14.0 m target takes the LiDAR maximum, which sits inside that range.

## 6. Colour, measured

Median pixel values sampled from the 2025 Street View frames:

| surface | sampled | shipped | note |
|---|---|---|---|
| body wall, in shade | `#6a798b` | `Toy_slate #8a97a8` | **lifted deliberately** — see REPORT.md |
| body wall, sunlit | `#b0b7bd` | — | the same paint under direct sun |
| frieze band | orange-red | `Toy_ioorange #c0402a` | |
| clay tile | terracotta | `Toy_brick #c96f4a` | eave lip in `Toy_rust #a86444` |
| arch surround | `#277e87` (shade) | `Toy_teal #3fa8a0` | terracotta before the 2024 renovation |
| frosted bay panels | `#a2abae` (shade) | `Toy_trim #f3efe6` | |
| window / bay frames | `#606f80` | `Toy_ink #3a3530` | |
| tympanum fan | `#cfd6d3` | `Toy_trim #f3efe6` | |
| louvres | `#343a3e` | `Toy_roofd #45454a` | small props only |

## 7. Recognition cues, ranked

1. The **red clay-tile pent over a vermilion frieze**, full length of Brannan and
   returning onto Ritch — a red line on a slate box, legible from directly above
2. The **teal arched entry** with its cream fan and gold medallion
3. The **slate blue-gray monolithic body** — no base, no cornice, one tone
4. The **corner condition** — two finished elevations at a sharp 90° on the
   diagonal grid
5. The **three curved iron Juliet balconies** at the southwest end of Brannan
6. The **raised roof monitor** over the middle third

## 8. Preserved / simplified

**Preserved:** the single-volume box on its true parallelogram footprint at the
real 45.2° heading; the two-tone red band mitred round the corner; the arch's
position hard against the party wall; the tall-ground-floor proportion; the
monitor's setback from the street parapet.

**Simplified or exaggerated:** the pent is thickened to a 0.68 m projection with
a rippled top face — the one place the exaggeration budget is spent, because it
is what the app's downward camera sees; barrel tiles become a ripple, not
individual tiles; the window rhythm becomes 7 bays on Brannan and 5 on Ritch;
the ground floor becomes 4 glazed bays plus 2 blank recessed panels; the arch
keeps its surround, fan and medallion and loses its mouldings, plinths and
lattice gate; the balconies become plain half-cylinder rails; the Epic Church
sign, gooseneck lamps, downpipes and meters all disappear; the roof scatter
becomes three units, one hatch and one skylight.

## 9. Uncertainties and conflicting evidence

- **OSM way `124903643`, tagged `addr:housenumber=414`, is the wrong polygon.**
  It overlaps parcel 3776011 by only 68% and sits over the southwest third of the
  lot; its `height=11` is a Bing trace of that wrong polygon. Not used.
- **Three LiDAR footprints, one building.** `SF3776011` returns three ~180 m2
  strips; they are structural bays of one building on one lot with one address
  and one assessor record. All three must be excluded at integration.
- **The monitor's shape is inferred.** Its existence and height are supported by
  a LiDAR median over 718 cells and by the photogrammetry; whether it is a
  daylight monitor, a stair penthouse or a plain raised block is not established.
  It is modelled as a daylight monitor because the building has exposed timber
  trusses over a sanctuary. Better aerial imagery would settle it.
- **The southwest two thirds of the Brannan upper floor is reconstructed** from a
  single oblique, because a row of mature ficus stands in front of it in every
  frontal frame. The 7-bay rhythm is the weakest number here.
- **The assessor says 3 storeys; the street shows 2.** 19,548 sq ft over a
  5,880 sq ft lot with a 5,852 sq ft basement is consistent with a double-height
  ground floor plus a mezzanine. The exterior only ever shows two window lines,
  which is what is modelled.
- **The scheme changed with the renovation.** 2021: warm mid-gray body
  (`#9ea19b`), terracotta arch. 2025: slate blue-gray body, teal arch. The frieze
  and tile stayed red through both. The 2025 state is modelled.
- Permits were still open at the last scrape ($3.0M Quezada, $1.1M Gary Bell), so
  rooftop equipment in particular may have moved since the 2010 LiDAR.
