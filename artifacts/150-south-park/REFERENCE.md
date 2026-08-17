# 150 South Park — reference dossier

150 S Park St, San Francisco, CA 94107. APN 3775-065. DataSF footprint `mblr SF3775065`.
OSM way/124884352. Manifest id `150-south-park`.

Compiled 16 August 2026 for `artifacts/150-south-park/`. This dossier records what was
verified for the model that shipped; where it disagrees with
`docs/asset-plans/150-south-park.md`, the disagreement is called out and REPORT.md carries
the decision.

---

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Building Footprints, LiDAR-derived (`ynuv-fyni`), record `mblr = SF3775065` | The authoritative footprint polygon (161.7 m2) and the roof-deck height: `hgt_majoritycm = 748` (modal cell), `hgt_median_m = 7.63`, `hgt_meancm = 793`, `hgt_stdcm = 78`, `gnd_min_m = 7.76` NAVD88. Also the pipeline's own primary bake input (`pipeline/buildings.mjs` header), so the exclusion radius is sized against this exact geometry |
| `pipeline/data/overture_buildings.geojsonseq` | The bake's gap-fill layer. Carries this footprint at 166.6 m2 with `height = 8.0`; 156 South Park at `6.0` and 140 South Park at `10.0` |
| OpenStreetMap way/124884352 | `addr:housenumber = 150`, `addr:street = South Park`, `height = 8`, `source = Bing`. A Bing trace — cross-check only |
| SF Assessor Historical Secured Property Tax Rolls (`wv5m-vpq2`), block 3775 lot 065 | Built **1959**; 2.0 stories; 0 dwelling units; 3,520 sq ft property area on a 3,060 sq ft lot; construction type `C`; use `COMO` (Commercial Office); zoning `SPD` |
| SF Building Permits (`i98e-djp9`), block 3775 lot 065 — 13 permits, 1988–2024 | The 2017–18 re-face that produced the current facade, the two-storey count at every filing, the 10 ft rear fence, and the absence of any rooftop structure |
| SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D, 30 June 2009 | District period of significance **1854–1935** (all 27 in-period buildings built 1906–1935, 23 contributing). Parcel table row: `3775065 | 150 | SOUTH PARK | HP6. 1-3 Story Commercial Building | 1959 | 6L`. 150 South Park is a **non-contributor** |
| SF Registered Business Locations (`g8m3-pdis`) | Tenant history; "150 South Park St **2nd Fl**" (Renzu Inc, 2014–15) independently confirms two occupied floors; Jeremy Kidson registered at the address Dec 2022 |
| Google Street View, South Park Street, capture **Jan 2025** | The entire front elevation — the black painted brick, the white stucco base, the two oxblood-framed windows, the steel canopy on two rod stays, the two gooseneck lamps, the shopfront divisions, the vertically stacked "150", the "FOR LEASE — Kidson Land Company" sign |
| Google Street View, Taber Place, capture **Jan 2025** | The rear: a walled yard behind a ~3 m black steel fence with spear finials and festoon lights, and beyond it the charcoal rear wall with a band of two brown-framed windows under a plain flat parapet |
| Google Maps satellite (Vexcel, 2026) | The flat roof, its skylights, and the wedge plan against the curving street |
| Exa `web_search_advanced_exa`, 16 Aug 2026 | LoopNet (APN + 3,520 SF office record), Kidson Land Company (owner/manager), the Kidson lease flyer PDF, CompStak on the neighbour at 140 South Park. **No architect, no builder, no architectural press, and no published photograph of this building exists in any source found** |

## 2. Verified dimensions and location

| | |
|---|---|
| Anchor (WGS84) | `-122.3947673, 37.7813810` — the area centroid of the DataSF ring |
| Footprint area | 161.7 m2 (DataSF, measured); 166.6 m2 (Overture) |
| Plan | A **wedge**: 5.54 m wide at South Park Street, 9.72 m at the rear, 18.7 m deep |
| OBB | 18.89 x 10.29 m, 83.2% rectangular fill |
| Roof deck | 7.50 m (LiDAR modal cell 7.48 m) |
| Parapet crest | **8.00 m** — the target height and the bbox top |
| Ground elevation | 7.76 m NAVD88 (the app's terrain handles this, not the asset) |
| Storeys | 2 |

## 3. Orientation

The building stands on the **north-west rim of the South Park oval at its west tip**, where
South Park Street curves around the end of the ellipse. Frontage normals swing 24 degrees
across four lots as the street bends — 140 South Park 135.0°, **150 South Park 133.5°**,
156 South Park 117.2°, 160 South Park 111.0° — while the party walls stay on the old
rectilinear lot lines. That mismatch is what makes this lot a wedge.

Footprint in Blender world metres (+X east, +Y north), CCW, centred on the anchor:

| # | (x, y) | corner |
|---|---|---|
| 0 | (-2.69, 9.27) | rear, north-east side |
| 1 | (-9.59, 2.42) | rear, south-west side |
| 2 | (-5.46, -2.73) | the 26° kink in the south-west party wall |
| 3 | (6.36, -8.13) | street, south-west corner |
| 4 | (10.14, -4.15) | street, north-east corner |

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| 0→1 | 9.72 m | NW 315.2° | rear yard / Taber Place |
| 1→2 | 6.61 m | SW 231.3° | party wall, 156 South Park (rear run) |
| 2→3 | 13.03 m | SW 204.8° | party wall, 156 South Park (front run) |
| 3→4 | **5.54 m** | SE 133.1° | **South Park Street — the hero elevation** |
| 4→0 | 18.56 m | NE 46.3° | party wall, 140 South Park (one straight run) |

The taper is entirely on the south-west side: the north-east party wall is dead straight
for its whole 18.56 m. The building is rotated ~43° off the world axes, which is why the
axis-aligned bounding box is 19.9 x 17.6 m for a building nowhere wider than 9.72 m.

## 4. Observations by side

**South-east (South Park Street) — the hero elevation, 5.54 m of it.**

Two storeys, split hard by a horizontal finish line with a projecting white drip. Above it,
**near-black painted brick** with the coursing legible under the paint, rising to a
completely plain flat parapet — no cornice, no coping band, no ornament of any kind, and
noticeably lower than 140 South Park's bracketed cornice next door. Two square-ish punched
windows in thick **oxblood / copper-brown** frames with matching sills. Below the split,
**bright white stucco** carrying, left to right (viewer facing the building):

| Element | u from the SW corner | z | Notes |
|---|---|---|---|
| secondary door | 0.21 – 1.11 m | 0 – 2.05 | narrow, black frame |
| display window | 1.85 – 3.74 m | 0.40 – 2.75 | large plate glass, black frame |
| "150" numerals | 3.93 – 4.22 m | 1.70 – 2.56 | **stacked vertically**, thin black strokes |
| entrance door | 4.43 – 5.33 m | 0 – 2.75 | glazed, black frame, transom bar at ~2.10 |
| canopy | 1.11 – 4.11 m | 3.60 – 3.85 | flat black steel, projects ~0.95 m |
| rod stays | at u 1.35 and 3.85 | 4.32 → 3.85 | thin diagonal tension rods |
| gooseneck lamps | u 0.60 and 4.87 | ~3.40 – 3.72 | outboard of the canopy, one over each door |

A small security camera sits at the black/white junction on the south-west side. The
"FOR LEASE — Kidson Land Company" sign between the upper windows is temporary and is not
modelled.

**North-west (rear, onto the yard and Taber Place).** The same charcoal wall, a horizontal
band of two large windows in the same brown frames, the same plain flat parapet. Blunter
and flatter than the front: no canopy, no white base. Seen in the real world only over a
3.05 m black steel fence with spear finials, across a planted yard strung with festoon
lights. *This elevation rests on one Jan 2025 pano shot through that fence; its dimensions
are inferred.*

**North-east and south-west flanks.** Party walls, blank painted brick, hard up against 140
and 156 for their whole length. No windows and no light wells — there is no gap on either
side. 156 South Park is 5.67 m to 150's 8.00 m, so the upper 2.3 m of the south-west wall
is exposed to the app's aerial camera; it is plain brick there, which is correct.

**Top.** One flat membrane roof at 7.50 m inside a plain parapet ring, with skylights and a
small vent cluster in the 2026 satellite imagery. Thirteen permits from 1988 to 2024 record
no penthouse, no stair bulkhead, no solar and no rooftop plant.

## 5. Recognition cues (ranked)

1. **Black brick box on a white stucco base** — a hard, high-contrast horizontal split, and
   the exact inverse of 155 South Park across the oval
2. The **wedge plan**: a 5.5 m frontage on an 18.7 m deep lot that widens to 9.7 m behind
3. The **two oxblood-framed windows**, the only warm colour on the building
4. The **flat black canopy on diagonal rod stays** with a gooseneck lamp outboard of each end
5. The **vertically stacked "150"** on white stucco

## 6. Preserved / simplified

**Preserved** — the two-tone split and its height on the wall; the plain parapet (its
plainness next to 140's cornice is a cue, so no coping band was added beyond the slim metal
flashing a painted-brick parapet actually carries); the wedge with its straight north-east
wall and 26° south-west kink; the oxblood frames; exactly two upper windows; the four
ground-floor elements in their measured positions.

**Simplified** — brick coursing to flat colour (asset contract: no textures); window frames
thickened to 0.17 m with 0.09 m relief; the canopy to one slab plus two rods; the gooseneck
lamps to an arm-and-shade pair; the numerals to bar glyphs with the stroke exaggerated from
~25 mm to 60 mm and the column from 0.86 m to 1.04 m; the rear window band to one three-part
opening; roof clutter to three skylights, a vent pair and a hatch. Dropped entirely: the
security camera, downpipes, the lease sign, the rear yard and its fence.

## 7. Uncertainties and conflicting evidence

1. **The crest, 8.00 m, is the weakest load-bearing number.** It rests on OSM `height = 8`
   (which Overture repeats, so those are one source, not two) on top of a measured 7.48 m
   LiDAR roof-deck mode. A photogrammetric check against the Jan 2025 pano does **not**
   settle it: solving the same pano two ways gives 6.4 m (absolute, assuming a 2.5 m camera
   at 6.2 m) and 9.2 m (relative to 140 South Park's 9.88 m LiDAR median), and the same
   method applied to 140 itself returns 6.8 m against its known 9.88 m. A zoomed Street View
   frame cannot support better than about ±1.5 m here, so the LiDAR plus tag consensus wins.
2. **The LiDAR `hgt_max` of 9.95 m is discarded.** It is 3σ above the median on a footprint
   whose height standard deviation is 0.78 m, with a matching 5.20 m `hgt_min` artifact at
   the other end; there is a large street tree at the corner of this frontage in the 2026
   satellite imagery; and the permit record contains no rooftop structure. Same failure mode
   as 592 Third Street and 250 Van Ness (asset-plans README).
3. **The black/white split is at 4.55 m, not the 3.80 m the plan assumed.** The plan derived
   3.80 m from a storey count. The photograph puts the split at ~58% of the wall's pixel
   height, which after the pano's tan expansion is 4.5–4.9 m. It is not a floor line: it is
   a painted finish line with a projecting drip, and it need not coincide with the second
   floor. Built at 4.55 m.
4. **The Assessor's "Commercial Office" use code is only half the building.** The 2017
   permits name an "upper level unit", a "live/work bathroom" and a "residential entry"
   alongside the "commercial tenant space". The upper storey is residential live/work. This
   drives one decision — both upper windows are lit at night, because a home with one window
   lit and one dark reads as an office.
5. **The rear elevation is the weakest evidence here.** One Jan 2025 pano through a 3 m
   fence, at an angle that puts the parapet against bright sky. The charcoal wall, the flat
   parapet and the band of two brown-framed windows are legible; their dimensions are not.
6. **No architect, no builder, no published photograph.** Unlike the contributors on this
   block, 150 South Park has no DPR narrative — the district form records it as a table row.
   Everything visual here is Street View and satellite.
7. **The 5.54 m frontage feels too narrow and is correct.** It is corroborated by its
   neighbours (140 at 6.84 m, 150 at 5.34 m survey / 5.54 m as built from the deduped ring,
   156 at 5.92 m, 160 at 6.26 m) and by the photograph, where 150's facade is visibly about
   four fifths the width of 140's.
