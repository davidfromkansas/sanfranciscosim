# 599 Third Street — reference dossier

Compiled 12 August 2026 for `artifacts/599-third/`. The plan
(`docs/asset-plans/599-third.md`) was the starting point; everything below was
re-verified against primary sources before modelling, and the three places where
this dossier **overrides the plan** are marked ⚠ and repeated in `REPORT.md`.

The building is a four-storey wood-frame artist live/work loft condominium of
1999–2001 holding the north corner of 3rd and Brannan in South Beach. Twenty-four
lofts, buff stucco, white multi-pane industrial window grids, a dark centred entry
recess with a steel chevron brace and oversized **599** numerals, a ground-floor
café in the former garage, and a working roof.

---

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/124890326](https://www.openstreetmap.org/way/124890326) | Footprint geometry (4-vertex rectangle), `addr:housenumber=599` with `addr:source:housenumber=survey`, `height=16` (Bing-traced) |
| [OSM node/13765490836](https://www.openstreetmap.org/node/13765490836) | Golden Goat Coffee, `level=0`, `check_date=2026-04-26` — **and its position**, which is what corrects the café location (⚠1) |
| DataSF parcels `acdm-wktn` | Map lot **3775140** subdivided into 24 active condominium lots 3775140–3775163, all sharing one polygon; zoning CMUO (Central SoMa Mixed Use Office); condo map recorded 2003-08-22; parcel polygon matches OSM |
| DataSF DBI permits `i98e-djp9`, block 3775 | 17 records at 599 3rd (1998–2022): 4 storeys, Type V wood frame, `artist live/work` use, the 2002 as-built roof deck, the 2017 garage→café conversion, the 2022 unit legalizations |
| DataSF 2010 LiDAR `ynuv-fyni`, record `SF3775140` | 3,515 half-metre cells (879 m²), ground mean 7.90 m, height median 15.62 m, mean 15.81 m, **max 18.34 m** |
| Google Street View, capture **May 2025**, from 3rd Street opposite the entry | The 3rd Street elevation in detail: buff stucco, white multi-pane grids, the dark entry recess, the chevron brace, the 599 numerals, the punched-square stack |
| Google Maps / Vexcel aerial imagery, 2026 | The roof: flat membrane, dense scatter of small skylights and condenser boxes, light deck pads, one penthouse mass. A 16 m building leans in this imagery — pattern is real, positions are not |
| Overpass context query (70 m radius) | Neighbour set and street bearings, including the Shell station on the north-west side (⚠2) |
| LoopNet / PropertyShark listings | Build year 2001. Their floor-area figures describe **single condo units** and are not massing evidence |

Nothing here is behind a paywall or a login; no copyrighted imagery is committed
to the repo.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.3942739, 37.7804504` | measured — footprint AABB centre; the polygon is a true rectangle so this equals the vertex mean exactly |
| Footprint | 36.51 × 24.01 m, 876.6 m² | measured (OSM, reprojected + oriented bbox) |
| LiDAR footprint area | 879 m² | independent, agrees to 0.3 % |
| Long-axis heading | 44.8° / 224.8° true | measured |
| Storeys | 4 | DBI permits, every application 1999–2022 |
| Construction | Type V wood frame | DBI permits |
| Main parapet | **16.0 m** | measured two ways: OSM `height=16` and LiDAR median 15.62 m + coping |
| Crest | **18.3 m** | LiDAR `hgt_max` 18.34 m — measured but a single maximum (see §7) |
| Ground | 7.90 m NAVD88 mean, flat | measured |
| Units | 24 condominium lofts + 1 café | DataSF parcels + DBI |

Footprint in the app's tangent projection, recentred on the anchor
(x east, y north, metres, CCW):

```
v0 ( -4.435, -21.323)   south corner — 3rd / Brannan, the hero corner
v1 ( 21.471,   4.411)   east corner  — Brannan / NE
v2 (  4.426,  21.323)   north corner — NE / NW
v3 (-21.471,  -4.411)   west corner  — NW / 3rd
```

| Edge | Length | Outward normal | What it is |
|---|---|---|---|
| v0→v1 | 36.51 m | 135.2° (SE) | **Brannan Street front** |
| v1→v2 | 24.01 m | 44.8° (NE) | interior face, toward 380 Brannan |
| v2→v3 | 36.51 m | 315.2° (NW) | faces the Shell station forecourt ⚠2 |
| v3→v0 | 24.01 m | 224.8° (SW) | **3rd Street front**, entry and café |

## 3. Orientation

Authored with Blender `+Y` = true north, `+X` = east, so the model drops into the
city at its real heading — `placeGeneric()` in `app/src/assets.js` scales and
positions but never rotates. The contract's "front faces −Y" cannot be honoured:
the entry faces **south-west** (224.8°). Real-world orientation wins per
`AGENTS.md` rule 5 and the orientation note in `docs/asset-plans/README.md`.

## 4. What each side shows

**South-west — 3rd Street, the address face (24.0 m).** Observed directly in
Street View (May 2025). Four storeys of buff / pale-yellow stucco under a plain
flat parapet, symmetrical about a **full-height recess in a dark warm taupe** at
the centre. In the recess, bottom to top: glass entry doors in a dark metal
frame; white **599** numerals; a vertical stack of four small square punched
windows; and near the top a **steel chevron — an inverted-V brace** spanning the
recess. Either side, a broad buff pilaster frames a bay carrying **large
white-framed multi-pane window grids**, two per bay per storey, sitting almost
flush in the stucco. Ground-floor openings are taller than the loft ones. The
café occupies the ground floor of the north-west bay ⚠1.

**South-east — Brannan Street, the long face (36.5 m).** Same four storeys, same
buff stucco, the same white grids continuing round the corner in a longer run of
six bays. No recess, no chevron: this face is pure rhythm and it is the face the
app's camera sees most of, because it is the long one. *(Massing and material
observed from aerial imagery and the edge of the Street View frame; the six-bay
count is inferred from the face length and the measured 3rd Street bay spacing.)*

**North-west (36.5 m).** ⚠2 **Not a party wall.** OSM shows a Shell filling
station immediately north-west: way/124889473 (`height=4`, one level — the
forecourt canopy) 23 m from the anchor on bearing 314°, and the station building
at 551 3rd Street 44 m out. So this elevation looks across an open forecourt from
3rd Street and is visible, not buried. Modelled with a reduced but real rhythm —
a row of small square punched windows at each of the three loft levels — rather
than as the blind wall the plan assumed.

**North-east (24.0 m).** Faces the 380 Brannan lot (South Park Commons, 12.6 m,
already in the scene) with Varney Place beyond. Our parapet stands 3.4 m above
that neighbour's, so the top storey is exposed: sparse punched windows at the
upper two levels only.

**Top — the working roof.** Flat grey membrane behind a low continuous parapet,
densely inhabited: a loose two-across grid of small skylights running down the
long axis with a condenser box beside most of them (roughly one cluster per
loft), three light timber deck pads (the 2002 as-built private open space), and
the stair/elevator penthouse — the crest, and the only vertical event. No stepped
massing anywhere.

## 5. Recognition cues (ranked)

1. **The corner** — two fully articulated street faces meeting at a sharp 90° on
   the diagonal SoMa grid, four storeys of continuous rhythm. Nothing on this
   block turns a corner this squarely.
2. **The dark entry bay** with its chevron brace and 599 numerals, dead centre of
   the 3rd Street face.
3. **White multi-pane grids on buff stucco** — the colour signature, and what
   separates it from the grey and brick warehouses either side.
4. **The inhabited roof** — skylights, condensers and deck pads scattered like a
   small settlement.
5. **The café shopfront** with its coral awning: the one saturated accent.

## 6. Preserve / simplify

**Preserve:** the true rectangle and its 44.8° heading; four storeys to a 16.0 m
parapet with the crest at 18.3 m; two designed street faces; the centred dark
recess with chevron and numerals; the buff/white pairing.

**Simplify:** window grids become 3×2 (3rd Street) and 4×2 (Brannan) `Toy_glass`
panes in white `Toy_trim` frames — rhythm, not mullion count (style bible §5).
The numerals and the chevron are deliberately oversized (§8, §9). Roof objects
are two repeated primitives on a loose grid: nine skylights and twelve condensers
stand in for twenty-four of each — the reading is "many", not a census. Deck pads
are flat rectangles. Hedges, railings, aerials and downpipes are omitted.

**Not added:** a crown, a setback, a cornice, a corner turret. The building is a
plain, well-mannered box whose charm is repetition plus one interruption.

## 7. Uncertainties and conflicting evidence

- **The 18.34 m crest is one LiDAR statistic.** `hgt_max` is the highest first
  return anywhere on the footprint; a mast or a parapet corner would produce the
  same number as a penthouse. The 16 m parapet is safe — OSM's independent
  `height=16` and the LiDAR median (15.62 m) agree. If the crest moves, only
  `targetHeightM` and the top of the penthouse volume move with it.
  **This is the single biggest open risk in the asset.**
- **The Brannan bay count (six) is inferred**, not counted from a photograph.
  Getting it wrong changes the rhythm on the building's longest face. Six gives a
  5.15 m bay, which matches the measured 3rd Street bay module closely enough to
  be credible.
- **Roof-object positions are inferred from leaning aerial imagery.** The pattern
  is well supported; the coordinates are free.
- **The 2010 LiDAR predates the 2017 café conversion and the 2022 unit
  legalizations,** but both were interior/ground-floor work — the massing it
  measured is the massing that stands.
- **Listing floor areas are not massing evidence.** The parcel is 24 condo lots;
  a "6,400 sf" commercial listing at this address is one loft, not the building.
  This misled the initial scoping and is called out so it does not mislead again.
- The Street View capture is May 2025 and shows roughly the left two-thirds of
  the 3rd Street face; the right third (toward the Brannan corner) is read from
  symmetry about the entry recess.

## 8. Deliverables in this folder

| File | What it is |
|---|---|
| `build_599_third.py` | deterministic Blender build (headless) |
| `599-third.blend` | authoring scene |
| `599-third.glb` | the shipping asset |
| `render_599_third.py` | controlled review rig, renders the **exported** GLB |
| `validate_599_third.py` | fresh-scene re-import contract validator |
| `make_contact_sheet.py` | montage of the review tiles |
| `599-third-{top,north,east,south,west,aerial,night}.png` | review renders |
| `599-third-contact-sheet.png` | the review sheet |
| `validation.json`, `REPORT.md` | validator output and the build report |
