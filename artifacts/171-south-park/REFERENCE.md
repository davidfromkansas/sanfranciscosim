# 171 South Park Street — reference dossier

Research behind the miniature GLB in this folder. Compiled 12–13 August 2026 for the
address-to-asset pipeline (`docs/asset-pipeline/ADDRESS-TO-ASSET.md`), from
`docs/asset-plans/171-south-park.md` plus the independent verification described in §2.

Where this file and the plan's dossier disagree, this file and `REPORT.md` are correct.

## 1. What the building is

A ca. 1910 Edwardian-era residential flats building at the south corner of South Park's
oval in SoMa, San Francisco — three floor-through flats, one per storey, now three
condominium lots (3775-137, -138, -139). It is a **contributor** to the South Park
Historic District (CHRSC 5D3), and the district boundary turns at this lot.

Its form is unusual and is the reason it was worth building by hand: where the oval park's
curve cuts across the 45° SoMa street grid, this lot is left as a **wedge** — a broad,
three-facet front bowing along the oval, narrowing over ~20.6 m to a 5.44 m tail at the
back of the block. Nothing else in the district has this plan, and the app's camera looks
down, so the plan shape is the building's identity.

Architecturally it is the district record's **flat-front** variant rather than the
bay-window one: every opening is flush in the wall plane, and all the relief is carried by
two horizontal ornament bands — a carved garland frieze at each upper floor line and a
heavy bracketed crowning cornice with a raised centre section. Light blue-gray painted
horizontal wood clapboard, repainted 2012.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way [124889458](https://www.openstreetmap.org/way/124889458) | footprint (13 vertices), address, `height=11` (`source=Bing`) |
| DataSF Building Footprints `ynuv-fyni`, record `SF3775137` | authoritative LiDAR footprint; roof deck 11.41 m (`hgt_median_m`), maximum feature 12.62 m (`hgt_maxcm`), ground 7.29 m NAVD88 (`gnd_min_m`). **Also the tile bake's primary footprint source**, which is what makes the exclusion arithmetic in §6 binding |
| [SF Planning, *South Park Historic District*, DPR 523D](https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf) (Christina Dikas / Page & Turnbull, 30 June 2009) | contributor status and CHRSC 5D3; **ca. 1910**; the flats typology ("wood frame… clad in wood or stucco siding", "flat front or angled bay windows", "flat roofs… and decorative cornices"); the district boundary turning at this lot |
| SF Assessor Historical Secured Property Tax Rolls `wv5m-vpq2` | 1908 build year; block/lot; three condo units of 1,064 / 1,102 / 1,102 sq ft, 2 bed each |
| SF Building Permits `i98e-djp9` | storey counts (3 in 2007/2012/2026, 4 in 2005–2008); the 2005 elevator "to service all floors" and rear deck; the 2012 wood window replacement and facade repaint; the March 2026 re-roof |
| Google Street View pano `tRhqK_-aiVsKi23dOxYSeg`, on the oval directly north of the building | **the entire front elevation.** Useful framings: `yaw=200, pitch=-24, fov=85` (full height), `yaw=213, pitch=-20, fov=52` (the faceted west corner and the cornice step), `yaw=205, pitch=-8, fov=70` (the entry porch). Source for every "observed" fact below |
| Google Maps satellite (Vexcel/Airbus, 2026) | roof: pale tan membrane (the March 2026 re-roof), a row of ~4 small skylights across the wide front third, a further pair mid-roof, a pale mechanical box, a deck structure at the tail |
| OSM API `map.json` for the block | neighbour footprints, the oval road and sidewalk geometry — the orientation and party-wall findings |

**Not obtained:** an oblique aerial of the roof, and any view of the tail (southeast)
elevation, which is enclosed by the block. The roof is known only from directly overhead.
KartaView's nearest coverage is 45+ m away on 3rd Street with the building out of frame;
Wikimedia Commons has nothing geolocated within 150 m; Redfin/Movoto listing pages are
bot-blocked and their unit copy carries no building description.

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.3945219, 37.7809000` | measured — the footprint's **area centroid** |
| Footprint area | 131.2 m² (OSM) / 132.2 m² (DataSF) | measured, the two agree within 0.8% |
| Front width | 11.36 m in three facets (3.64 + 3.83 + 3.89 m) | measured |
| Tail width | 5.44 m | measured |
| Front-to-tail | ~20.6 m (min-area OBB 20.58 × 9.50 m) | measured |
| Roof deck | 11.41 m above ground | measured (LiDAR) |
| Crowning cornice crest | 12.6 m — **the target height** | LiDAR maximum 12.62 m, attributed to the observed crown |
| Floor-to-floor | 3.80 m (11.41 / 3) | derived; consistent with the tall floors and deep friezes in the photographs |
| Storeys | 3 above grade, entry at grade | permits **and** counted from Street View |
| Ground elevation | 7.29 m NAVD88 | measured — the app's terrain handles this, not the asset |

## 4. Orientation

The park front faces **NNW**, with the three facets at outward bearings **321.3°**
(west facet, which carries the entry), **348.2°** (centre) and **1.1°** (east) — average
343.5°. The tail faces SE 136.0°.

The asset is authored in true-world orientation (Blender `+Y` = north, `+X` = east)
because `placeGeneric()` in `app/src/assets.js` scales and positions but never rotates.
The contract's "front faces −Y" rule therefore cannot be honoured literally; real-world
orientation wins (AGENTS rule 5) and the deviation is recorded in `REPORT.md` §4.

Footprint in Blender coordinates (metres, `+X` east, `+Y` north), counter-clockwise,
centred on the anchor:

```
(-9.513,  4.415)   (-3.371, -1.664)   (-2.007, -1.498)   ( 0.343, -3.742)
(-0.476, -4.527)   ( 5.024, -9.988)   ( 8.940, -6.208)   ( 7.215, -4.174)
( 4.329, -0.879)   ( 3.036,  0.591)   ( 0.968,  7.400)   (-2.922,  7.477)
(-6.670,  6.693)
```

The `(-2.007,-1.498) → (0.343,-3.742) → (-0.476,-4.527)` run is a 1.13 m re-entrant on the
southwest party wall — a light well against 181 South Park. It is present in both surveys,
so it is real, and it is kept.

**The origin is the area centroid, not the bounding-box centre.** On a wedge those are
~1.4 m apart, and the offset is not cosmetic: it is what creates the exclusion window in
§6. Do not recentre this model on its bounding box.

## 5. What each side shows

**North-northwest — the park front (hero, and the only elevation the public sees).**
Three flat facets, each ~3.6–3.9 m wide, angled ~27° and ~13° from one another so the
front bows gently along the oval. The facet creases are plainly visible on the real
building and **the cornice steps with them** — that step is what keeps the bow legible
rather than reading as one flat wall.

Light blue-gray painted horizontal wood clapboard. Every opening is flush: pale wood-sash
windows in simple trim, generally paired. All relief is in three horizontal bands: a
**swag/garland frieze** at each upper floor line, the same motif returning around the
faceted corner, and a heavy **crowning cornice** — brackets, a dentil course, and a
**raised centre section** stepping above the main cornice line. That crown is the tallest
thing on the building.

Three storeys, entry at grade — one or two steps, no raised basement, and **no garage on
this face** (the bright blue steel gate visible just east belongs to 165–167). The entry
sits at the **west end**: a small projecting **pedimented porch hood** with a carved
tympanum on pilasters, sheltering pale sage-green glazed double doors with the "171"
plate beside them.

**East-northeast flank.** Party wall with 165–167 South Park, a 1908 flats contributor
whose roof deck is 8.55 m — about 3 m lower. The band above that is genuinely exposed and
the app's camera reads it; everything below is buried. Built as plain painted wall with
three windows in the exposed upper band only.

**Southwest flank.** Party wall with 181 South Park, whose roof deck is 14.18 m — taller
than this building, so this flank is fully buried in reality. Built plain, with the light
well, and no window rhythm invented.

**Southeast — the tail.** 5.44 m wide, the back of the wedge, and the one rear elevation
open to space within the block. The 2005 permit's rear deck and steel-framed stair land
here and are visible in satellite imagery.

**Top.** A flat, pale tan membrane roof inside the cornice line, noticeably lighter than
its neighbours because of the March 2026 re-roof. A row of about four small skylights
across the wide front third, a further pair mid-roof, a pale mechanical box, and the rear
deck at the tail. The wedge is at its most legible here, so this surface got the most
design attention.

## 6. Conflicting evidence, and how it was resolved

1. **Storey count: 3, not 4.** Permits from 2007, 2012 and 2026 record 3 existing storeys;
   the 2005–2008 elevator and rear-deck permits record 4. Street View settles it: three
   storeys stand above grade with the entry at sidewalk level, no raised basement. The
   three condo units are therefore one floor-through flat per storey. That puts
   floor-to-floor at 3.80 m, which is tall — and the photographs show exactly that, tall
   rooms with deep ornamented friezes eating the top of each storey. The permits' "4" is
   most likely counting a basement, consistent with the elevator serving "all floors".

2. **OSM `height=11` is the roof deck, not the crest.** It matches the LiDAR median
   (11.41 m) closely enough to look trustworthy, which is exactly the trap the plans
   README warns about. The crest is 12.6 m.

3. **What carries the 12.62 m LiDAR maximum: the cornice, not a penthouse.** The planning
   stage guessed at an elevator overrun from the 2005 permit. The photographs show a
   heavily ornamented crown with a raised centre section standing well above the roof line
   and no penthouse visible from the street; 12.62 − 11.41 = 1.21 m fits that crown. The
   roof mechanical box seen from satellite is a separate, lower object and is modelled
   below the crest.

4. **Flat front, not bays.** The district record allows South Park flats "either a flat
   front or angled bay windows", and several neighbouring contributors have bays. This one
   does not — every opening is flush. The planning dossier assumed bays; that was wrong and
   is corrected here.

5. **Build date: 1908 (Assessor) vs ca. 1910 (district record).** Both are post-earthquake
   reconstruction and neither changes the design. The district record is the
   better-researched source; ca. 1910 is used, with the Assessor value noted.

6. **The exclusion radius has a 3.2 m window, and it is the tightest in the registry.**
   `excluded()` in `pipeline/buildings.mjs` drops a footprint when its ring centroid **or
   any ring vertex** falls inside the radius, and the bake reads the same DataSF layer
   measured above. From this anchor: this building's own ring centroid is **0.59 m** away,
   the nearest neighbour trigger (`SF3775028`, 165–167 South Park) is **3.83 m**, then
   `SF3775172` (181) at 3.92 m and `SF3775029` (159) at 11.02 m. So the radius must sit
   between 0.59 and 3.83 m; `exclude: 2` gives 1.4 m of margin either way. Anything from
   4 m up deletes two party-wall historic contributors and punches a hole in the district's
   south side. This is also why the anchor is the area centroid: at the OBB centre the
   nearest neighbour vertex is only 2.74 m away and the window nearly closes.

## 7. Recognition cues, ranked

1. **The wedge plan** — broad on the park, tapering to a narrow tail. The only one in the
   district, and the first thing the downward camera reads.
2. **The three-facet front bowing along the oval** — facets, not a curve, with the cornice
   stepping at each crease.
3. **The two ornament bands** — the garland frieze at each floor line and the bracketed
   crown. On a building this plain they are the only relief and they carry it at thumbnail
   size.
4. Three storeys of light blue-gray clapboard, entry at grade under a pedimented hood.
5. The pale, newly re-roofed deck with its skylight row.

## 8. Preserved / simplified

**Preserved**

- The wedge at its real proportions and its real ~45° heading
- The three front facets as three distinct planes with visible creases, and the cornice
  stepping with them
- The flat front — no bay was allowed to creep in
- Two ornament bands per upper floor line plus the crowning cornice and its raised centre
- The pedimented entry hood at the west end
- The light well on the southwest flank
- The tall/short relationship with the neighbours (lower on the NE, higher on the SW)

**Simplified / exaggerated**

- Carved garland-and-paterae panels become one continuous proud band per floor line: the
  motif reads as rhythm at city scale, never as carving
- Roughly a dozen openings per floor become three clean flush windows per facet per floor,
  all identical, no mullions
- The dentil course disappears; the brackets become identical chunky blocks on the front
  facets only
- The entry hood becomes a single chunky pediment on two pilaster slabs
- The cornice assembly is thickened so it survives at thumbnail size — that and the frieze
  bands are the only places semantic exaggeration is spent
- Roof clutter becomes six skylight boxes, one mechanical box, a hatch, and the rear deck

## 9. Remaining uncertainties

- The exact number of window openings per facet per floor, and the number of garland
  panels per frieze, are read off a tree-obstructed Street View and are the weakest
  numbers here. Three per facet is a design decision, not a count.
- The tail elevation is unobserved. Its window rhythm is inferred from the front's.
- The light well's depth and whether it runs full height are inferred; only its plan is
  surveyed.
- The northeast flank's exposed upper band is real but its openings are inferred — a
  sparse scatter, deliberately not a grid.
- The roof is known only from directly overhead, so the mechanical box's height is
  inferred. It is modelled below the crest so it cannot steal the bounding-box top.
- No architect or builder is recorded for this building in any source consulted.
