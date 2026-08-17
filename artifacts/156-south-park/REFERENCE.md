# 156 South Park Street — reference dossier

Research for the SF-SIM miniature asset. Compiled 16 August 2026. Everything below is
either **measured** (from a named dataset, reprojected here), **published** (quoted from a
named document), or **observed** (read off dated imagery) — anything else is marked
*inferred* and is a candidate for correction.

The plan this executes is `docs/asset-plans/156-south-park.md`. Where this file and the
plan disagree, **this file wins**: it is the record of what was verified while building.

---

## 1. What the building is

156 South Park Street is a small two-storey **reinforced-concrete warehouse of 1924** on
the north-west side of the South Park oval in SoMa. It was built by the contractor
**J.A. Bryant** for **J.J. Welter & Co., draymen**; no architect is recorded. From about
1933 to about 1982 it was occupied by **The Anchor Packing Co.**, which is how the current
tenant still refers to it. A 2019 permit changed its use from warehouse to office, and
since **June 2023** it has been the San Francisco studio of the architects **Multistudio**.

It is a **contributor** (CHRSC status code `5D3`, property type `HP8. Industrial`) to the
potential South Park Historic District. The 2009 Page & Turnbull survey that defined that
district recorded one fact about it that decides how this asset should be designed:

> "Of twenty-three contributing buildings in the South Park Historic District, all but one
> features at least minor alterations. The building that appears to be unaltered is 156
> South Park Street."

Eighteen of the district's contributors have replacement doors, fourteen have replacement
windows, several have added parapets or false fronts. This one has none of that. It is the
plainest building on the oval and the only one still saying what it said in 1924 — so the
model carries **no base course, no cornice, no contrasting shopfront and no invented
ornament**. Its flatness is the subject.

## 2. Sources, and what each establishes

| Source | Establishes |
|---|---|
| SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D continuation sheets, 30 June 2009 (53 pp) — `https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf` | Contributor table row `3775066 / 156 / SOUTH PARK / HP8. Industrial / 1924 / 5D3`; *"156 South Park Street (1924) is an example of a small reinforced concrete warehouse at South Park"*; district industrial buildings *"are only two stories in height"*; the J.A. Bryant / J.J. Welter attribution; The Anchor Packing Co. tenancy ca. 1933 – ca. 1982; the Integrity finding quoted above; district period of significance 1854–1935, criteria A and C; style described as 20th Century Commercial or simple utilitarian |
| DataSF Building Footprints, LiDAR-derived — `https://data.sfgov.org/resource/ynuv-fyni`, `mblr = SF3775066` | The authoritative footprint polygon (260.3 m2) and the height statistics that split the two masses: max 8.74 m, modal cell 5.66 m, median 5.67 m, mean 6.14 m, std 1.14 m, min 2.25 m, ground 6.69 m NAVD88 |
| SF Assessor Historical Secured Property Tax Rolls — `https://data.sfgov.org/resource/wv5m-vpq2`, parcel 3775066 | Built 1924; two storeys; zero dwelling units; industrial use class; **construction type `C`** (concrete, corroborating the DPR); zoning `SPD`; 2,688 sq ft. Consistent across every roll year from 2013 to 2025 |
| SF DBI Building Permits — `https://data.sfgov.org/resource/i98e-djp9`, block 3775 lot 066 | 1990 **parapet reinforcing**; 2003 reroofing; 2019-07-10 **change of use warehouse → office** (PA 201907105483); 2021 accessible entrance; 2022 new modified-bitumen Class A roof and a new steel stair to the second floor; 2023 interior fit-out. Existing/proposed storeys are "2 / 2" on every modern permit and several reference an **existing mezzanine** |
| OpenStreetMap way/124884346 | Cross-check footprint (263.2 m2, agrees within 1.1%), `addr:housenumber = 156` with `addr:source:housenumber = survey`. Its `height = 6` is Bing-derived and describes the shed — see §5 |
| Google Street View, South Park Street pano, **capture Jan 2025**, viewed from `37.78120, -122.39465` at headings 310°–318° | The entire street elevation, and both neighbours for comparison. This is the only good photographic source found |
| Esri World Imagery (z20) with the DataSF parcel rings overlaid, and Google Maps satellite (Vexcel, 2026, z21–z22) | The flat roof, the skylight monitor run, the parcel-to-roof correspondence, and 156's roof shadow falling across 150's lower roof |
| `https://www.multi.studio/studios/san-francisco` and the firm's June 2025 studio-leadership post | *"Our current studio, formerly the Anchor Packing Co."*; the June 2023 opening |

**Negative result worth recording:** two Exa searches (`web_search_advanced_exa`) over the
building name, address and the Anchor Packing Co. returned only business listings and firm
news posts — **no exterior photographs and no architectural description**. Nothing was
found on J.A. Bryant, which matches the DPR form's own note that it found nothing on him
at the City, the Public Library or SF Architectural Heritage. The exterior evidence here is
Street View, aerial imagery and the DPR form; there is no press coverage to corroborate it.

## 3. Location, footprint and orientation

**Anchor (manifest):** `-122.3948748, 37.7813535` — the **area centroid** of the DataSF
ring, computed by the shoelace formula, not the vertex average and not the bbox centre.

The lot is a **through lot**: it fronts South Park Street to the east-south-east and backs
onto the Taber Place alley to the west-north-west, with party walls on both long sides. It
is a **tapering strip**, 32.3 m along its axis:

| Position along the lot | Width across it |
|---|---|
| South Park frontage | **5.92 m** (OSM reads the same edge as 6.92 m) |
| 6 m back | 7.2 m |
| 14 m back | 8.4 m |
| 18 m back (widest) | **9.8 m** |
| Taber Place end | **7.94 m**, on a wall cut ~19° off square |

Raw DataSF ring, WGS84, in order:

```
37.7814029, -122.3948763      37.7812913, -122.3948928
37.7813563, -122.3948293      37.7814158, -122.3950244
37.7813073, -122.3946965      37.7814226, -122.3950328
37.7813068, -122.3946949      37.7814722, -122.3949675
37.7812592, -122.3947257
```

Reprojected to the app's local tangent frame and recentred on the anchor (metres,
`+X` east, `+Y` north — the frame the GLB is authored in):

```
( -0.14,  5.46)   (13.12, -10.42)   ( -8.16, 13.12)
(  4.00,  0.31)   ( -1.59,  -6.88)
( 15.69, -5.11)   (-13.17,   6.89)
( 15.83, -5.16)   (-13.91,   7.64)
```

Edges and what they face:

| Edge(s) | Length | Outward bearing | Elevation |
|---|---|---|---|
| street end | 5.92 m | **117.3°** ESE | **South Park Street front** |
| north-east party wall | 19.6 m in three runs | 21–51° | 150 South Park |
| south-west party wall | 34.2 m in three runs | 194–230° | 158 – 160 South Park |
| Taber end | 7.94 m | **316.3°** WNW | **Taber Place rear** |
| Taber end, NE return | 11.09 m | 43.7° | the open rear yard behind 140 – 150 |

The lot sits at roughly 45° to the world axes, so the axis-aligned bounding box of the
finished model is ~30 × 24 m for a 32.3 m building. That is correct, not a scale error.

**Two simplifications were made to the survey ring**, both sub-metre and both invisible
between party walls: the 0.15 m sliver at the north-east street corner and the 1.05 m
sliver at the Taber Place corner are dropped. They are parcel-line artefacts and cost
triangles the window grids need.

**Neighbours.** North-east: **150 South Park**, APN 3775-065, built **1959**, status `6L`
— a *non*-contributor, and visibly lower than 156 in both the pano and the aerial shadow.
South-west: **158 / 160 South Park**, APN 3775-067, built **1924**, `5D3` contributor,
slightly taller, with an arched second-floor window and a red-tile cornice. Both share
party walls with 156.

## 4. What each side shows

**South Park (ESE) front — the only well-documented elevation.** A flat unbroken plane of
slate blue-grey painted render, two storeys, capped by a plain parapet with a slim
projecting cap and no cornice. Reading the Jan 2025 pano from the south-west (158) end
toward the north-east (150) end:

1. a narrow **entrance bay**: a small flat pale **canopy** — the only light-coloured
   element on the building — over a recessed dark flush door with a vertical pull, an
   intercom plate and a mail slot; a tall narrow slot window beside it; the numerals
   **156** on the wall
2. a narrow pier carrying **two black cylindrical wall sconces, stacked vertically**
3. the **ground-floor sash field**: one very large steel-sash window, a dense grid of
   small panes (counted as roughly **6 columns × 5 rows**) in a lightly projecting frame
   on a heavy sill, occupying about two thirds of the frontage, with **multistudio** in
   small white letters low on the right-hand glass
4. above a blank spandrel band, the **upper sash ribbon**: the same industrial sash
   running nearly the full width, counted as roughly **8 columns × 4 rows**, slightly
   recessed with a plain sill and lintel band
5. a broad blank wall band, the parapet, and **two X-shaped steel star tie anchors** set
   high on it
6. service clutter that is deliberately **not** modelled: a downpipe, a CCTV dome, conduit

Wall, sash frames, glazing bars, sills, door and parapet cap are all the same colour. Only
the canopy (pale) and the sconces (black) break it.

**Taber Place (WNW) rear — unverified.** Street View coverage of the alley exists but is
shot from close against the wall and could not be attributed to this lot with confidence.
The nearest pano for this row shows a blue-grey painted industrial wall with multi-pane
steel windows and a large roll-up garage door, which is exactly what a drayage warehouse
presents to a service alley, but that is *inference*. The model gives the alley end one
vehicle door recess and nothing else.

**Party walls (NE and SW).** Shared, blind, invisible in the city. Modelled as plain
closed walls. The step from bar to shed happens on both.

**Roof — the important surface.** Flat throughout, dark membrane (the 2022 modified
bitumen). The front bar carries a parapet ring; the shed carries a run of **raised
skylight monitors** stepping away from the street, legible in both Esri and Vexcel
imagery. Aerial imagery also shows 156's roof shadow falling onto 150's roof, confirming
156 is the taller of the two.

## 5. Heights, and the trap in them

| Figure | Value | What it actually describes |
|---|---|---|
| LiDAR **maximum** | **8.74 m** | the front bar's parapet crest — **the target height** |
| LiDAR modal cell | 5.66 m | the shed roof, which is most of the footprint |
| LiDAR median | 5.67 m | same |
| LiDAR mean | 6.14 m | the area-weighted blend of the two |
| OSM `height` | 6 | the shed again, from Bing |

**OSM's 6 m and the LiDAR median's 5.67 m agree with each other and are both wrong for the
street front.** They corroborate nothing except that the shed dominates the area. The
Jan 2025 photograph plainly shows two full storeys with a tall ground floor, and 156's
parapet is visibly above 150 next door (OSM `height = 8`) and below 140 (`height = 10`).
This is the same trap `docs/asset-plans/README.md` warns about and that 543 Presidio Blvd
fell into. **Target height 8.7 m**, normalised exactly.

**Where the bar ends is derived, not observed** — the weakest number in this dossier.
Solving `A_front × 8.74 + (260.3 − A_front) × 5.66 = 260.3 × 6.14` puts about **41 m2** at
the taller level, which against a 5.9–7.2 m width is a bar about **6 m deep**. The median
independently caps the tall part at under half the footprint, i.e. under ~15 m deep. The
model splits at **10 m** — deeper than the mean-inversion figure, shallower than the
median ceiling — because a 6 m bar looked implausibly thin against a facade with a
3 m-tall ground-floor window, and because the aerial imagery shows the roof tone changing
around a third of the way back. **This is the first thing to re-verify** if a better
oblique aerial or roof view becomes available.

## 6. Recognition cues, ranked

1. **One colour, two grids** — a flat slate blue-grey wall carrying two stacked fields of
   small steel-sash panes and nothing else.
2. **The skylight monitor run** on the long low roof behind — what the app's downward
   camera actually sees.
3. **The step** from a tall two-storey street bar to a low wide shed.
4. **The entrance bay**: pale canopy, recessed dark door, `156`, two stacked sconces.
5. **The X star anchors** high on the parapet.

## 7. Preserve / simplify / omit

**Preserve:** the two masses and the step; the tapering plan and the 117.3° heading; the
monochrome; both sash grids and their proportions; the canopy; the star anchors; the
monitor run; the flat parapet with its slim cap.

**Simplify:** the pane grids are relieved bars over one flat glass plane, never individual
glazed panes; the monitors are regularly spaced boxes with a glazed north-north-east face;
the two sub-metre parcel slivers are dropped; the mezzanine is interior and not modelled.

**Omit:** the downpipe, CCTV dome and conduit; the `multistudio` lettering (a tenancy, not
the building); South Park Street, the oval and its trees; Taber Place; the neighbours;
sidewalks, vehicles and people.

## 8. Uncertainties, carried into REPORT.md

1. **The bar/shed split depth** — derived, see §5. Highest-impact unknown.
2. **The Taber Place elevation** — unverified, see §4.
3. **The pane counts** (6×5 and 8×4) are read off one oblique pano and may be out by a
   column or a row. They matter, because the grid *is* the facade.
4. **The star anchors may not be structural.** They read as classic tie-rod star washers
   and the 1990 "parapet reinforcing" permit would explain them exactly — but the DPR form
   calls this a reinforced-concrete building, and concrete buildings do not normally need
   them. Recorded here as *observed, consistent with the 1990 permit*; no cause asserted.
5. **The assessor's 2,688 sq ft is given as both lot area and property area**, which cannot
   be right for a two-storey building with a mezzanine on a fully covered lot. Not used for
   anything.
