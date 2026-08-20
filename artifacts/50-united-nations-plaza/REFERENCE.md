# 50 United Nations Plaza — reference dossier

Federal Office Building, 50 United Nations Plaza, San Francisco (Arthur Brown Jr.,
1934–36; renamed the **Senator Dianne Feinstein Federal Building** by GSA). NRHP
#100001018, contributing property to the San Francisco Civic Center National
Historic Landmark district.

This dossier records what was verified for the SF-SIM miniature, what was
inferred, and where the plan (`docs/asset-plans/50-united-nations-plaza.md`) was
confirmed or corrected. **Where this file and the plan disagree, this file wins**
— it is the measured record; `REPORT.md` records the build against it.

---

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [NRHP registration form, 2017](https://npgallery.nps.gov/GetAsset/2a46e6cb-74e7-4320-b96d-5870c139903d) | **The authoritative elevation-by-elevation description.** Storey counts (five + attic, north four), the tripartite composition, the concave corner reentrants, the C-shaped zinc roof with arched dormers, the flat north roof, granite vs Gladding-McBean terra cotta, the courtyard's glazed light-grey brick, the 2013 elevator bulkhead |
| [OSM relation/19309896](https://www.openstreetmap.org/relation/19309896) | Multipolygon footprint: outer way/32865027, inner (courtyard) way/1411159971. `height=29`, `start_date=1933`, wikidata Q5440315 |
| [DataSF building footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json) (`mblr=SF0351035`, `area_id=225`) | LiDAR statistics over 22,235 cells at 50 cm: `hgt_median_m` 29.02, `hgt_majoritycm` 2473, `hgt_maxcm` 3840, `hgt_meancm` 2849, `hgt_stdcm` 370; `p2010_zmaxn88ft` 155.067; ground 12.54–17.23 m (median 14.14) |
| [DataSF street centerlines `3psu-pn9h`](https://data.sfgov.org/resource/3psu-pn9h.json) | Which face is which street, and the 9.0 deg Civic Center grid |
| [Wikipedia](https://en.wikipedia.org/wiki/50_United_Nations_Plaza_Federal_Office_Building_(San_Francisco)) | History, the 1977 504 Sit-in, the AIDS Memorial Quilt origin, "hipped roof covered with light grey lead-coated copper" |
| [GSA historic building page](https://www.gsa.gov/real-estate/find-a-historic-federal-building/senator-dianne-feinstein-federal-building-san-francisco-ca) | Current building name; the same exterior description |
| [GSA Design Excellence monograph (Sept 2020)](https://www.gsa.gov/system/files/50_UNP_Monograph_MASTER_508.pdf) | 350,000 sq ft; "GSA converted 14,000 square feet of the … rooftop into a garden surrounding the facility's new photovoltaic array" |
| [facaderetrofit.org](http://www.facaderetrofit.org/projects/50-united-nations-plaza) | "97 feet" (29.57 m) — the parapet |
| [The Registry, 7 Nov 2013](https://news.theregistrysf.com/san-franciscos-50-united-nations-plaza-renovation-ready-unveiling-official-dedication-ceremony/) | $122 M HKS renovation dedicated 6 Nov 2013, LEED Platinum, 24,000 sq ft courtyard |
| [rooflite](https://www.rooflitesoil.com/project/50-u-n-plaza/), [Henry](https://www.henry.com/knowledge-center/project-profiles/henry-green-roof-system-federal-office-building/) | Green-roof build-up: 8-inch media, gravel drain fields keeping soil off mechanical plant and historic parapets |
| Commons [2017 south-east street view](https://commons.wikimedia.org/wiki/File:2017_50_United_Nations_Plaza_Federal_Office_Building.jpg) (CC BY-SA 4.0) | The colonnade, the corner arch, the cornice/balustrade/attic stack, the roof's shallow pitch |
| Commons [2017 from Hyde Street](https://commons.wikimedia.org/wiki/File:2017_50_United_Nations_Plaza_Federal_Office_Building_from_Hyde_Street.jpg) (CC BY-SA 4.0) | The plainer west elevation, the SW concave corner, the corner hip cap |
| Commons, Carol M. Highsmith 2010, public domain: [LCCN2010718894](https://commons.wikimedia.org/wiki/File:Exterior_from_rooftop,_Federal_Building,_San_Francisco,_California_LCCN2010718894.tif), […899](https://commons.wikimedia.org/wiki/File:Exterior_from_rooftop,_Federal_Building,_San_Francisco,_California_LCCN2010718899.tif), […907](https://commons.wikimedia.org/wiki/File:Exterior_from_rooftop,_Federal_Building,_San_Francisco,_California_LCCN2010718907.tif) | The whole roof plan from the air, the axis to City Hall, the roof surface and dormers, the corner pavilion, the entablature/balustrade/attic stack in close-up. **Pre-renovation (2010): patched lead-coated copper, bare north roof** |
| Esri World Imagery nadir, z19 (0.24 m/px), overlaid on the projected OSM rings | The post-2013 roof: the green roof and its two PV banks on the NORTH wing, the courtyard trees and paving, the concave south corners, the C-shaped metal roof |

No copyrighted imagery is committed here; the URLs above are the record.

---

## 2. Verified geometry (all measured, not quoted)

Local tangent projection, `LON0 −122.4375 / LAT0 37.77` (the repo's one projection).

| Quantity | Value | How |
|---|---|---|
| Outer polygon area | 7,447 m² | OSM way/32865027, reprojected + shoelace |
| Courtyard area | 1,939 m² | OSM way/1411159971 (published figure 24,000 sq ft = 2,230 m², measured to a different line) |
| Built footprint | 5,508 m² | outer − inner. DataSF counted 22,235 LiDAR cells at 50 cm = 5,559 m² — 0.9% agreement |
| Outer oriented box | **112.53 × 66.93 m** | min-area OBB over the OSM outer ring |
| Courtyard oriented box | **72.66 × 27.20 m** | min-area OBB over the OSM inner ring |
| Long-axis bearing | **80.92 deg** (9.08 deg north of due east) | OBB edge; DataSF gives 9.09 deg, the McAllister / UN Plaza centrelines 9.0 deg |
| OSM OBB centre | −122.4144797, 37.7804306 | derived |
| DataSF OBB | 114.10 × 68.96 m, centre −122.4144646, 37.7804226 | 1.60 m from the OSM centre, 1.6–2.0 m larger — see §4 |
| Wing depths (own frame) | N **21.4**, S **18.2**, W **22.4**, E **18.3** m | outer minus inner ring; the courtyard sits 2.05 m east and 1.65 m south of centre |
| Concave south corners | 6.9 × 6.9 m each, four OSM segments turning through 90 deg | OSM outer ring, decomposed in the building's own frame |
| North / square corners | no cut | same |
| Street distances from the anchor | McAllister 44.1 m N, UN Plaza 60.3 m S, Hyde 68.7 m W, Leavenworth 77.3 m E | DataSF centrelines within 180 m |

## 3. The heights — verified, and the two traps

- **Parapet 29.0 m.** Four independent sources land here: OSM `height=29`, Overture
  `height=29`, DataSF `hgt_median_m` 29.02, facaderetrofit.org's 97 ft (29.57 m).
  This is the top of the fifth-floor balustrade — the eave of the metal roof.
- **Crest 33.0 m — this is `targetHeightM`.** Two independent derivations agree to
  0.1 m:
  1. `p2010_zmaxn88ft` 155.0667 ft = 47.263 m NAVD88, minus median grade
     `gnd_mediancm` 14.14 m → **33.1 m**.
  2. Decomposing the LiDAR height statistics. Mode 24.73, median 29.02, mean 28.49,
     sd 3.70. The north wing is 21.4/(21.4+18.2+22.4+18.3) ≈ 41% of the roof area;
     41% at 24.7 m plus 59% spread uniformly from a 29 m eave to a ~33 m flat top
     predicts a mean of 28.4 against a measured 28.49, with the median landing just
     above 29 as observed. No other three-level split fits.
- **North wing 24.7 m** — the LiDAR mode, assigned to the north wing on the area
  argument above and confirmed by the nadir imagery (that wing carries the flat
  green roof). *Inferred* in its attribution, measured in its value.
- **Trap 1: 29 m is not the height.** Taking it as `targetHeightM` builds the
  building 4 m short and flat-topped, losing the metal roof entirely.
- **Trap 2: `hgt_maxcm` 3840 is not the height either.** 38.40 m is the 2013
  elevator bulkhead (NRHP §7 records it, on the east courtyard side) plus rooftop
  mechanical plant, on 22,235 cells with sd 3.70 m. It would make this building
  taller than Bill Graham Civic Auditorium.

## 4. Orientation and placement

Bounded by United Nations Plaza (south), Hyde Street (west), McAllister Street
(north), Leavenworth Street (east) — verified against DataSF centrelines, all of
which run at 9.0 deg off cardinal.

**The hero front faces south.** Authored with Blender `+Y` = true north, `+X` =
east; the assembly is built axis-aligned in the building's own frame and rotated
**+9.08 deg about Z**, so the loader applies no rotation. The contract's "front
faces −Y" and the real-world heading therefore agree to within 9 deg.

The DataSF outline is 1.6–2.0 m larger than OSM's in both directions and its
centre is 1.60 m away. That is not noise, it is *informative*: **DataSF's LiDAR
outline traces the main cornice, OSM's traces the wall plane.** The model is built
at the OSM wall plane (112.53 × 66.93) with a 0.90 m cornice projection, which puts
the cornice outline at 114.33 × 68.73 — DataSF's box to within 0.25 m. That was
used as a free cross-check on the cornice depth, and it held.

The area centroid of the built annulus is 1.2 m from the OBB centre, so there is no
centroid-vs-box argument here; the model centres on the box.

**Shipped anchor: `−122.4144853, 37.7804351`.** The build recentres on the final
bounding box, which sits 0.49 m east and 0.49 m south of the OSM OBB centre because
the two south corners are scooped while the north corners are square. That offset
is reported by the build script and carried into the manifest.

## 5. What each side shows

**South (United Nations Plaza) — the hero.** 98.7 m of wall between the two concave
corners. Two-storey rusticated granite base; slightly projecting belt course; a
colonnade of **free-standing** two-storey Doric columns clear of the wall, with
granite-balustraded balconies at the third floor between them; a projecting dentil
cornice; the fifth floor set back again behind a full-length balustraded balcony.
Three arched double-height entrances at the centre with eagle-and-shield cartouche
keystones. Granite mascarons over every other first-floor lintel.

**West (Hyde Street).** No entrances at all, no basement access. Same tripartite
composition with two-storey **pilasters** instead of columns and balustrades
directly in front of the third-floor windows. The two ends are *slightly recessed*
from the centre — a shallow plane change, well under 1 m: OSM records the whole
elevation as one straight 60.03 m segment.

**North (McAllister Street) — the different one.** Almost entirely Gladding-McBean
terra cotta glazed and tooled to imitate granite; only the two **projecting end
portions** are real granite. The central section is **four storeys with a flat
roof** — no fifth floor, no metal roof. One arched double-height entrance at the
centre over a granite bridge across the sunken areaways.

**East (Leavenworth Street).** As west, with the basement fully exposed, so the
rusticated base reads as three storeys and three service entrances sit at basement
level in a sunken plaza with curving ramps. Out of scope for the GLB.

**Corners.** South-west and south-east are **concave arc** reentrants, each with an
arched entrance and a Doric portico above the second storey. North-west and
north-east are square. Plan-level recognition cue, and cheap to build.

**Top — more than half of what this asset shows.**
- A **C-shaped low-pitch hip roof** in grey standing-seam zinc (2013; replaced the
  original lead-coated copper) wraps the south, east and west wings and the two
  north end pavilions, rising from the 29 m eave to a flat top at 33 m, with small
  arched dormers on the slopes.
- The **north wing's flat roof** sits ~8 m lower at 24.7 m: two long banks of dark
  blue-grey **photovoltaic panels**, a **green roof** wrapping around them, white
  mechanical units, and a gravel margin along the north parapet.
- The **courtyard** (72.7 × 27.2 m) is open to the sky, paved, planted with two rows
  of trees, with a glazed-brick elevator bulkhead on its east side.

## 6. Recognition cues (ranked)

1. The **ring plan with the open courtyard** — the first read from the app's camera,
   and nothing else in Civic Center has it
2. The 99 m south colonnade of free-standing columns over a heavy rusticated base
3. The stepped roofline: 24.7 m north wing / 29 m parapet / 33 m metal crest, with
   the two taller granite pavilions bracketing the low north side
4. From above: grey metal hip roof around a green roof and two solar arrays
5. The two concave scooped corners on the plaza front, each with an arched entrance

## 7. Preserved / simplified

**Preserved:** the 112 × 67 m ring and the 72.7 × 27.2 m courtyard; the uneven wing
depths that put the courtyard off-centre; the 9.08 deg grid rotation; the north
wing's lower flat roof with its two tall end pavilions; one continuous cornice line
all the way round; the concave south corners.

**Simplified:** ~26 real column bays become 18 chunky columns at 1.6 m diameter; the
third-floor balconies become one continuous balustrade band; west/east/north
pilasters become shallow proud strips; every dentil, mascaron, cartouche and sconce
is dropped; paired four-over-four windows become single recessed panes on a regular
rhythm; arched dormers become small bumps; the green roof becomes two PV rectangles
in a mint field with a gravel margin and three plant boxes; the courtyard's planting
becomes two beds and eight tree pucks on a paved cross.

## 8. Corrections to the plan

None to the plan's facts — every measured value in
`docs/asset-plans/50-united-nations-plaza.md` re-derived identically here. Two
clarifications:

1. §2.4 of the plan says the 0.90 m cornice projection makes "the roof outline"
   match the DataSF box. It is the **cornice** outline that matches (114.33 vs
   114.10 × 68.73 vs 68.96 m); the metal roof itself sits inboard of it. The check
   is valid, the noun was loose.
2. The shipped anchor is **−122.4144853, 37.7804351**, 0.7 m from the plan's
   −122.4144797, 37.7804306. The plan anchored on the OSM OBB centre; the model
   centres on its own bounding box, and the scooped south corners move that
   0.49 m east and 0.49 m south. The build script reports the corrected anchor.

## 9. Uncertainties

- The 33.0 m crest is **derived**, not published — one photogrammetric difference
  and one statistical decomposition, agreeing to 0.1 m.
- The north wing's 24.7 m roof height is the LiDAR **mode**; its attribution to the
  north wing is inferred from the area split plus the nadir imagery.
- The green roof's **layout** (two PV banks, planting around them, gravel to the
  north) is read off one nadir image at 0.24 m/px. Its *presence on the north wing*
  is well sourced; the arrangement is inferred.
- Column count (~26 real, 18 modelled) and window bay counts are read from
  photography, not drawings.
- **No night-lighting reference exists.** A targeted search found no documented
  scheme and none of the sourced photography is nocturnal. The night state here is
  a documented design decision, not an observation: the six arched entrances in
  `Toy_gold_Glow` and the attic window band in `Toy_white_Glow`. No facade
  floodlighting was invented.
- The public-domain rooftop photographs are 2010 and predate the 2013 renovation.
  The model is built to the **current** state (zinc roof, green roof, PV array).
