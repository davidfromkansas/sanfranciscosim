# 84 South Park — reference dossier

Compiled for the SF-SIM miniature asset, 16 August 2026, from the sources in §1.
Written *after* re-verifying the plan (`docs/asset-plans/84-south-park.md`) rather
than from it. Where this file and the plan disagree, this file and `REPORT.md`
win — see REPORT's "Dossier corrections".

This building has the **weakest documentary base** of any landmark in the set: no
National Register nomination, no architect, no survey description, no
architectural publication, and the one real-estate record located (a 1990 sale)
carries no photographs. Everything in §4 is read from a single January 2025 Street
View capture and Bing z20 aerial imagery. It is labelled *observed* or *inferred*
throughout and none of it should be mistaken for record.

---

## 1. Sources, and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| DataSF `acdm-wktn` (Parcels), `blklot=3775055` | the lot: a clean surveyed rectangle **30.07 × 6.99 m** (98.66 × 22.94 ft), 210.3 m², long axis **135.18° / 315.18°**; the single `84` address range; SPD zoning | **surveyed** |
| DataSF `ynuv-fyni` (Building Footprints, 2010 LiDAR, refreshed 2023-09-11), `mblr` SF3775055 | main footprint `sf16_bldgid` 201006.0028685: 184.8 m², 746 cells @ 50 cm, OBB 27.31 × 7.43 m. Roof height **median 11.36 m**, majority 11.49, mean 10.95, **min 8.18**, **max 13.24**, σ 1.25. Ground 10.76 / 11.22 / 11.63 m NAVD88. Second footprint 201006.0168103: **16 m², median 7.99 m**, 15.6 m behind the main centroid | **measured** |
| DataSF `wv5m-vpq2` (Assessor secured roll, 2025 + 2024) | built **1907**; use `SRES` / class `D` (single-family dwelling); homeowner exemption; sold **1990-08-28**; lot 2,242.5 sq ft, depth 97.5 ft. Also: 2 storeys, 22 rooms, 7 baths, 4,462 sq ft — **stale**, see §3 | current for use/date, **stale for form** |
| DataSF `i98e-djp9` (Building permits), block 3775 lot 055, 14 permits 1989–2009 | the building's real history — see §3. The decisive records are 1992-12-04 (`$361,782`, "vertical addition", `2 → 3` storeys), 1994-06-13 (revision, `2 → 3`), 1994-06-02 ("move fireplace and garden area to **south deck** revise **skylite**"), 2009-06-11 ("replace waterprof membrane on **roof deck**") | **documentary** |
| OSM `way/113545687` | footprint cross-check: OBB 29.60 × 7.29 m at 135.03°, 203.7 m²; tags `building=yes`, `height=11`, `addr:housenumber=84` | measured, but see §2 |
| Google Street View, South Park, **January 2025** capture — viewed from `37.781845,-122.393885` (headings 309–318°) and `37.781790,-122.393930` (heading 318°), pitched up 18–25° | the entire street elevation: colour, the two-bay split, the ground-floor living green wall, the rust-red door carrying the numerals "84", the pale projecting second-floor box, the recessed terrace with dark rails, and an **open slatted frame standing above the parapet** | **observed** |
| Bing aerial (Virtual Earth `a`-layer, z20, 0.118 m/px), rotated to the building's long axis and cropped to the parcel | the roof plan: the rear terrace and its planting, four skylights mid-roof, a slatted dark rectangle, three skylights on the north-east edge, a roof garden with a small tree, a pale bulkhead and a red object, and the street-edge parapet | **observed**, ±1 m registration |
| Esri World Imagery z20 at the same point | *discarded* — dark, low-contrast, and mis-registered against the footprint by several metres. Recorded here so the next agent does not repeat the attempt | — |
| The Hawthorne Group listing, 76–82 South Park Street | the north-east neighbour is a **three-storey** live/work building (82 first floor, 80 second, 78 third), which is why its LiDAR median is 13.08 m | corroborating |
| The Grubb Company record for 84 S Park Street | 1990-08-28 sale at $360,000; 1907; **no photographs** | corroborating |
| FoundSF "South Park First Buildings"; Curbed SF "Then & Now: South Park" (2012) | neighbourhood history only. **No source describing this building specifically was found.** | context |

Photographs are not committed to the repo. The Street View and Bing views above
are reproducible from the coordinates and headings given.

## 2. Verified dimensions, location and orientation

| | |
|---|---|
| Footprint (design) | **6.99 m frontage × 30.07 m depth**, 210.2 m², the building occupies the whole lot |
| Long axis | **315.18°** street → rear; the street elevation faces **135.18°** |
| Manifest anchor (placement) | **-122.3940683, 37.7819798** — the DataSF parcel area centroid |
| Registry point (bake exclusion only) | **-122.3940709, 37.7819871** — 0.84 m away on bearing 344°, see REPORT |
| Roof deck | **11.20 m** (LiDAR median 11.36, majority 11.49; OSM `height=11` agrees with the deck) |
| Parapet crest | **11.50 m** |
| Pergola crest → **target height** | **13.20 m** (LiDAR max 13.24) |
| Rear wing deck | **8.10 m** (LiDAR min 8.18 on the main footprint; the separate 16 m² footprint's median is 7.99) |
| Storeys | **3** on the front 22.90 m; **2** on the rear 7.17 m |
| Axis-aligned XY bbox | 26.09 × 26.29 m — the exact 45° rotation of a 6.99 × 30.07 m sliver, **not** a 26 m building |

**Three geometries exist and they do not agree.** The parcel is a survey; the LiDAR
footprint stops 2.8 m short at the rear because that end of the building is a
lower wing with an open terrace, not roof; OSM traces the full lot depth. The OSM
centroid sits **2.7 m north-west** of the LiDAR centroid. The parcel centroid lies
between them — 0.68 m from the LiDAR one, 1.93 m from OSM — and is the only
surveyed value of the three, so it is the anchor.

## 3. What the record says, and where it is wrong

The 2025 assessor roll still describes a **two-storey, 22-room, 7-bathroom**
dwelling of 4,462 sq ft. That is the 1907 rooming house. The permit trail
overturns it:

| Date | Storeys | What |
|---|---|---|
| 1989-11-17 | 2 → 2 | abatement complaint; use recorded as **apartments** |
| **1992-12-04** | **2 → 3** | **"vertical addition", $361,782**, use `1 family dwelling → office` |
| 1993-11-08 | 3 → 3 | fire sprinkler installation |
| 1994-03-07 | 3 → 3 | Chapter 38 sprinkler compliance |
| 1994-06-02 | 3 → 3 | "move fireplace and **garden area to south deck** revise **skylite**" |
| 1994-06-13 | 2 → 3 | revision to the vertical-addition application |
| 2008 (×3) | 3 → 3 | renewals and final inspections |
| 2009-06-11 | 3 → 3 | "replace waterprof membrane on **roof deck**. new kitchen cabinets." |
| 2009-07-09 | 3 → 3 | dry rot found under the above |

So: a 1907 shell, two storeys of apartments until 1990, bought that August, and
converted 1992–94 into a three-storey single dwelling with a roof deck, a garden
deck and skylights. The contemporary front is that campaign, not 1907. **A
modeller who trusts the assessor builds a two-storey building** — the LiDAR
median of 11.36 m is far too tall for two storeys of 1907 wood frame.

## 4. Observations, side by side

**South-east (street, 135.18°) — the public face.** Three storeys of smooth matte
**mid-dark slate blue-green**, unbroken by trim or string courses, in a row where
76–82 is brown shingle over cast stone, 86–96 is raw metal panel, and everything
further along the rim is cream or taupe. Two unequal bays:

- *Wide south-west bay* (~4.2 m of the 6.99 m frontage): a recessed ground-floor
  opening containing a **living green wall** — a framed panel of dense planting
  and trailing ferns, roughly 3 × 2 m — with a window beside it. Above it a
  **pale near-white box projects** from the face carrying a large light-framed
  window. Above that, at third-floor level, a wide dark window set back in the
  wall plane.
- *Narrow north-east bay* (~2.7 m): a **tall recessed slot** running most of the
  height. At its foot a **rust-red timber door** with the numerals **84** mounted
  beside its head; above, a terrace behind **dark metal rails** at two levels.

**North-east flank (45.18°, toward 76–82).** Party wall. 76–82's LiDAR median is
**13.08 m** against this building's 11.36 m deck, so the wall is entirely hidden.
Built blind.

**South-west flank (225.18°, toward 86–96).** Party wall. 86–96's LiDAR median is
**11.15 m** — only 0.21 m below this deck. Effectively hidden too. Built blind.
*This is the significant difference from 106 South Park*, whose 3.2 m of exposed
flank above a shorter neighbour was one of its two silhouette cues. 84 has no
such cue: its silhouette is the roof.

**North-west (rear).** Faces the mid-block open space behind the Bryant Street
lots — not a second street, so it is seen in the app only obliquely and from
above. The building steps down here to two storeys. No elevation photograph of
this side was located; the six windows in the model are a plausible domestic
rhythm, *inferred*.

**Top — the whole silhouette.** Reading from the rear to the street, at the
distances measured off the rotated Bing crop (± ~1 m):

| Station (m from anchor, + = toward the street) | What |
|---|---|
| −15.0 → −12.2 | low rear element with a gridded glazed roof |
| −12.2 → −7.9 | pale open **roof terrace** at ~8.1 m, planting round its edges |
| −7.9 → −7.2 | step up to the main roof at 11.2 m |
| −7.2 → −0.1 | **four skylights**, ~1.55 × 1.11 m, at ~1.83 m centres, slightly south-west of the roof's centre line |
| −0.1 → +5.1 | plain membrane deck |
| +5.1 → +7.6 | a **regularly slatted dark rectangle**, ~2.5 × 3.5 m, south-west of centre |
| +8.5 → +12.3 | **three skylights** along the north-east edge |
| +10.6 → +14.0 | **roof garden**: a small tree, a pale bulkhead, a red object, planting |
| +13.8 → +15.0 | bright **parapet** at the street edge |

## 5. Recognition cues (ranked)

1. **The colour.** The only tinted facade on this stretch of the rim. At the
   distance the app usually views the oval, colour is the only channel with
   bandwidth left.
2. **The 4.3:1 sliver.** 6.99 × 30.07 m over three storeys — thinner than 106's
   7.32 m and the thinnest in the set.
3. **The pergola over the roof garden.** At 13.20 m it is the tallest thing on
   this stretch of roofline (13.08 m next door, 11.15 m on the other side), and
   because both flanks are blind it is the only part of this building that breaks
   the row's silhouette.
4. **The two-level roof** — a 11.2 m main deck stepping down to an 8.1 m planted
   rear terrace. From overhead that step is what makes it a building and not a
   slab.
5. **The two-bay front**: a pale projecting box over a green wall, beside a tall
   dark slot with a red door in it.

## 6. Preserved / simplified

**Preserved:** the 6.99 × 30.07 m footprint and the 135.18° heading exactly; the
three-storey front and two-storey rear with their 11.20 / 8.10 m decks; the
11.50 m parapet and 13.20 m pergola crest; the bay handedness (green wall and
projecting box **south-west**, entrance slot **north-east**); the skylight
asymmetry (four mid-roof, three on the north-east edge); the pergola as an
**open** frame.

**Simplified:** the green wall is one flat `Toy_mint` panel, no individual
plants; the projecting box is one clean volume with one window; the terrace rails
are flat slabs, no balusters; the pergola is four posts, two rails and five
beams, no joinery; roof planting is blocked masses and the tree is a trunk plus a
single canopy form; the numerals are sub-pixel and are not modelled; downpipes,
meters, vents and coping profiles are gone; neither neighbour is modelled and
neither flank carries any treatment.

**Deliberately omitted despite being observed:** the red object in the roof
garden (a second saturated red would fight the door, which is the building's one
accent), and the individual planting textures of the green wall.

## 7. Uncertainties and conflicting evidence

1. **The pergola.** The single largest unknown, and it sets the target height.
   *For:* Street View shows an open slatted frame above this building's parapet;
   the Bing aerial shows a regularly slatted dark rectangle in the corresponding
   position; the LiDAR maximum is 1.88 m above the median, which a ~2 m trellis
   explains exactly; and the 1994 permit moved a garden to a deck while the 2009
   permit re-membraned a roof deck. *Against:* 76–82 next door has a LiDAR median
   of 13.08 m, so party-wall bleed would land in the same place — the failure
   mode the Earl Warren and Gran Oriente plans both document; and at 0.118 m/px a
   flush PV array and a slatted pergola are not cleanly separable. *Partial
   counter to the bleed reading:* 86–96 on the other side has its own maximum of
   13.28 m against an 11.15 m median with no tall neighbour to bleed from, so a
   13.2 m rooftop structure is normal on this row. **Decided: real.** Consequence
   if wrong: the target height is 11.50 m, not 13.20 m — a 15% scale error.
2. **The facade colour** is read from a shaded, tree-obscured, north-east-facing
   wall photographed in January. The *relation* is confident (tinted body, pale
   projecting box, red door, green panel); the hue and value are not.
3. **The rear elevation** is entirely unphotographed. Its six windows are a
   plausible rhythm, not a record.
4. **The rear structure** (the separate 16 m² / 7.99 m LiDAR footprint) is
   modelled from two numbers. Whether it is a separate outbuilding or the back of
   the same lower wing is unresolved; it is modelled as the latter.
5. **The skylight counts (4 and 3)** are read at 0.118 m/px. The *asymmetry* is
   clear; the exact counts are not.
6. **Storey heights** (ground 0–3.90, second 3.90–7.55, third 7.55–11.20) are
   inferred by dividing the measured deck height; no floor plan was found.
7. **No historic designation was found**, which is absence of evidence, not
   evidence of absence. South Park has been repeatedly surveyed and the rim
   carries NR-eligible buildings on both sides of this one.
