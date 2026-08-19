# 104–106 South Park (Gran Oriente Filipino Hotel) — reference dossier

Compiled 16 August 2026 for `artifacts/106-south-park/`. The plan behind it is
[`docs/asset-plans/106-south-park.md`](../../docs/asset-plans/106-south-park.md);
this file records what was actually verified before and during the build, and
`REPORT.md` records what changed as a result.

## 1. What the building is

A three-storey-over-basement wood-frame rooming house at 104–106 South Park
Street, built in 1907 to designs by W. L. Schmolle (builder: McLaughlin and
Walsh), occupying the whole of a 24 ft × 97.5 ft lot on the north-west rim of the
South Park oval. Hotel Maruichi and then the Omiya Hotel in the 1920s, leased from
1935 and bought in 1948 by Gran Oriente Filipino — the first Filipino-founded
Masonic lodge in the United States — and one of the earliest Filipino-owned
buildings in the South of Market. Nominated to the National Register in 2019 under
Criterion A (Filipino ethnic heritage / social history, period of significance
1935–1968); the new owners declined to proceed in 2020, so it is **eligible, not
listed**. Bought in 2018 by Mission Housing Development Corporation and
rehabilitated in 2020–21 as 24 studios of 100% affordable housing, part of the
~$60M "South Park Scattered Sites" project with the Park View and Hotel Madrid.

## 2. Sources, and what each one establishes

| Source | Establishes |
|---|---|
| **SF Planning HPC packet, case 2016-008192SRV** (2 Oct 2019) — `https://commissions.sfplanning.org/hpcpackets/2016-008192SRV%20-%20Gran%20Oriente.pdf`, containing the full National Register Registration Form by Erica Schultz (Architectural Resources Group) | **The backbone.** 1907; W. L. Schmolle; three storeys over basement, wood frame, brick foundation; **thirty-eight feet tall**; 24 ft × 97.5 ft lot fully occupied, frontages on South Park Street and Taber Place; elevation-by-elevation description of all four sides; flat roof with three large rectangular skylights along the south-west end and five small square ones along the north-east end; alterations record |
| **SF Heritage**, "South Park's Gran Oriente Filipino Hotel", published Jan 2021, **updated Oct 2025** | The **post-COVID facade alterations**: repaint, removal of the painted trompe-l'œil pediment lintels, the painted Corinthian columns and the metal entrance gates; retention of the metal "GRAN ORIENTE FILIPINO" lettering. Also the 1996 elevation photograph (Aileen Lainez), Dec 2020 construction photographs, a Sept 2025 street photograph and a 2025 Google Maps crop of the renovated ground floor |
| **DataSF `acdm-wktn`** (Parcels), `blklot=3775058` | Surveyed lot; address range **104–106**; SPD zoning; the neighbour lots — `3775057` = 102 South Park at bearing 53° (north-east) and `3775059` = 108–110 at bearing 217° (south-west) |
| **DataSF `ynuv-fyni`** (Building Footprints, LiDAR, 2010 survey / 2023-09 refresh), `mblr` SF3775058 | Footprint OBB 30.02 × 7.02 m at 45.04°, area centroid `-122.3944106, 37.7817227`; roof-deck height **median 11.02 m** (majority 10.92, mean 11.36, σ 0.67, 824 cells); ground 9.25–10.25 m NAVD88; **`hgt_max` 13.50 m**; and the neighbours' heights — 102 South Park median **12.88 m** (max 15.20), 108–110 median **7.76 m** |
| **OSM `way/124884343`** | Cross-check footprint, OBB 29.80 × 7.29 m at 135.03°; `building=residential`, `height=11`, `name=Gran Oriente Filipino` |
| **Google Street View**, South Park, January 2025 capture, viewed at `37.781575, -122.394230`, headings 300–318°, pitch 105–122° | The current ground floor (mid-slate stucco, recessed vestibule at the south-west end with the metal lettering above it, three-pane shopfront to the north-east) and what can be seen of the pale upper storeys past a full-grown street tree |
| **Bing / Maxar aerial tiles at z20**, stitched and **masked to the DataSF footprint** (see §5) | The roof: a photovoltaic array over the north-east half of the rear two thirds, a run of raised light-coloured boxes along the south-west edge, mechanical plant at the street end, and a pale cool-roof membrane |
| Mission Housing (`missionhousing.org/granoriente`, and the "Preservation and transcendent projects finalized" post); SCCS Group; SF Chronicle (Beth Spotswood); SF Examiner, 10 Mar 2023; California Freemason, 2 Jun 2021; Positively Filipino | 24 studios; the 2018 acquisition and the $5M MOHCD Small Sites loan; the 2020–21 rehabilitation scope including PV and roof upgrades; the history and tenancy |

No copyrighted imagery is committed to this repository. The aerial and street-level
sources above are cited by URL and viewing parameters so any reviewer can
reproduce exactly what was looked at.

## 3. Verified dimensions, location and orientation

| | Value | Confidence |
|---|---|---|
| Footprint | **7.32 × 29.72 m** (24 ft × 97.5 ft), 217 m² | **published** (NR), corroborated by two independent geometries to ~0.2 m/side |
| Roof deck | **11.02 m** | **measured** (LiDAR median over 824 cells; flat roof, so median ≈ deck) |
| Cornice crest | **11.58 m** (38 ft) | **published** (NR §7) — the model's target height |
| Manifest anchor | `-122.3944099, 37.7817221` | DataSF LiDAR area centroid, shifted 0.07 m to put the model's XY bbox centre on the origin |
| Long axis | 315.0° (street → Taber Place) | **measured**, both sources agree to 0.05° |
| Street facade faces | **135.0°** (south-east, onto the oval) | **measured** |
| Neighbours | 102 South Park (NE, **1.9 m taller**), 108–110 (SW, **3.3 m shorter**) | **measured** (LiDAR) |

Three geometries exist for this building and, unusually, all three agree — the NR
lot, the DataSF LiDAR footprint and the OSM way. The two footprint centroids sit
1.58 m apart along the long axis; that gap matters only for the bake-time
exclusion radius, not for placement.

## 4. What each side shows

- **South-east (street, the public face).** Painted stucco. Upper two storeys
  pale warm off-white; ground floor a distinctly darker slate/warm gray; a
  near-black sign band between them carrying the metal "GRAN ORIENTE FILIPINO"
  letters. Upper storeys divided into **three bays**, one double-hung window per
  bay per storey — **six openings in a regular grid**. Simple cornice with painted
  dentils above the third-storey windows. Ground floor: recessed entry vestibule
  with two panelled doors under transoms at the **south-west** end, then **three**
  wood-sash storefront windows over a solid bulkhead to the north-east.
  **Gone since 2020:** the painted trompe-l'œil pediment lintels, the painted
  Corinthian columns, the ornamental metal entrance gates.
- **North-east (toward 102 South Park).** Abuts the neighbour, which is taller.
  Never visible. Blind.
- **South-west (toward 108–110).** Blind for its lower two thirds; the top ~3.2 m
  stands above 108's roof and the nomination records it as horizontal wood boards.
- **North-west (rear, Taber Place).** Asbestos shingle over the original wood
  channel rustic siding. Basement louvre and screened window; central inset
  service entrance to the rear kitchen flanked by one-over-one windows; three
  one-over-one windows on each upper storey (six total); metal fire escape on the
  **two north-eastern bays**.
- **Top.** Flat at 11.02 m, cornice lifting the street end to 11.58 m. Three large
  rectangular skylights along the south-west edge and five small square ones along
  the north-east edge (installed 1927, replaced in kind 1986), covering interior
  light wells. Today the north-east half also carries a photovoltaic array — see §5.

## 5. The roof: how the PV question was settled

The plan (2.9) left this open and forbade splitting the difference. It was settled
before modelling, as follows:

1. Google Maps satellite at z22 showed large dark arrays across this row but could
   not be attributed to individual buildings at that resolution and lean.
2. Esri World Imagery has no z21 tile here and its z20 tile is stale monochrome,
   mis-registered against the footprint by a metre or two.
3. Bing/Maxar z20 tiles were stitched into a 3 × 3 mosaic, upsampled, and the
   **DataSF footprints of all three lots** (3775057, 3775058, 3775059) drawn on
   top. Registration was good: 108–110's plain roof and 102's arrays both landed
   inside their own outlines.
4. The mosaic was then **masked to SF3775058 alone** and rotated so the long axis
   ran vertically, which removes the neighbour-attribution question entirely.

The masked roof shows, from the Taber Place end toward the street: a wide PV block,
a continuous PV run down the north-east side covering roughly the rear two thirds,
a line of raised light-coloured boxes along the south-west edge in the middle
stretch (consistent with the nomination's three large skylights), a pale cool-roof
membrane, and a cluster of mechanical plant at the street end. **PV confirmed.**

The membrane being pale, not dark, is a second finding from the same image and it
changed the asset's roof colour — see `REPORT.md`.

## 6. Recognition cues, ranked

1. The **4:1 sliver at three storeys** — 7.3 × 29.7 m, 11.6 m tall.
2. The **stepped party-wall silhouette** — shorter neighbour south-west, taller
   north-east, with a band of exposed boarded wall above the shorter one.
3. The **three-bay grid over a two-part ground floor**.
4. The **sign band**, the only thing on the building that says what it is.
5. The **roof**: a pale rectangle with a dark array down one side and a line of
   raised skylights down the other.

## 7. Preserved / simplified

**Preserved exactly:** the 7.32 × 29.72 m footprint, the 315° axis, the 135.0°
facade heading, the 11.02 m deck / 11.58 m crest relationship, the three-bay
rhythm, the vestibule at the **south-west** end with the shopfront north-east of
it, the exposed flank band starting at 7.80 m, the skylights on the south-west
roof edge and the array on the north-east.

**Simplified:** double-hung division, muntins and transoms (windows are clean
recessed rectangles with a proud sill); the three shopfront windows (one recessed
glazed band with two mullions); the painted dentils (one proud course under the
cornice); the fire escape (two platforms and two posts, no treads or truss); the
lettering (a light inset strip inside the dark band, no glyphs); asbestos shingle,
wood boarding and stucco (flat colour, distinguished by value); the basement
louvre, meters, downpipes and conduit (omitted); both neighbours, the street tree,
Taber Place and the oval (not modelled).

## 8. Uncertainties carried into the build

- The **current paint hues** are read from shaded photography under a full-grown
  street tree; the value relation (pale above, darker ground floor, near-black
  band) is confident, the hues are not.
- **No photograph of the Taber Place rear elevation** was located; §4's rear
  description is the nomination's 2019 prose and the rehabilitation may have
  changed the cladding or the fire escape.
- Whether the **dentilled cornice** survived the repaint intact, or was simplified,
  is unconfirmed; it is modelled as surviving in simplified form.
- Whether the **wood boarding** on the exposed south-west strip survived the
  repaint is unconfirmed — see `REPORT.md`, where it changed the palette.
- The **unit count** disagrees across sources (24 / 27); it affects nothing
  geometric.
