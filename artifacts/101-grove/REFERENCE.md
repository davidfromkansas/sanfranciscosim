# 101 Grove Street — reference dossier

The San Francisco Department of Public Health headquarters, Samuel Heiman,
1931–32. A four-storey Beaux-Arts Classical granite block holding the
Grove/Polk corner of the Civic Center Historic District, one street north of
City Hall and immediately east of the Bill Graham Civic Auditorium.

Compiled for `artifacts/101-grove/` on 12 August 2026. The plan this executes is
`docs/asset-plans/101-grove.md`; where this file and that plan disagree, this
file and `REPORT.md` win.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/35176281](https://www.openstreetmap.org/way/35176281) | the footprint polygon, `building=civic`, `height=20` |
| Nominatim nodes 11198865806 / 358803227 | that "101 Grove Street" and "SF Department of Public Health" both resolve inside way/35176281 — the request's "#105" is a suite, not a separate structure |
| [SF 2010 LiDAR building footprints](https://data.sfgov.org/resource/ynuv-fyni.json), record `SF0811001` | 10,920 half-metre cells; ground min 17.24 m, ground max 19.63 m (the site falls 2.4 m); height median **19.77 m**, height majority **20.29 m**, height max 32.42 m |
| [PCAD 17419](https://pcad.lib.washington.edu/building/17419) | "City and County of San Francisco, Department of Public Health, Headquarters Building", 101 Grove Street, **4 storeys**, **Beaux-Arts Classical**, Civic Center Historic District contributor (district created 27 Feb 1987). Architect field left blank. |
| [San Anselmo Historical Museum — Samuel Heiman](https://sananselmohistory.org/articles/samuel-heiman/) | attributes the building to **Samuel Heiman, designed 1931** — the only attribution located |
| [Commons: *Department of Public Health (San Francisco).JPG*](https://commons.wikimedia.org/wiki/File:Department_of_Public_Health_(San_Francisco).JPG), Sanfranman59, 2 Mar 2008, CC BY-SA 4.0 | **the primary visual reference.** A three-quarter view of the Grove/Polk corner showing the whole corner bay, the second-floor balconettes, the cornice and the balustrade. Sections 3 and 4 below are read off this image. |
| Esri World Imagery (ArcGIS `World_Imagery` export) | the roof, overlaid against the OSM polygon to separate this building from 99 Grove |
| [healthysf.org — 101 Grove in 1935](https://www.healthysf.org/bdi/more/101grove.html) | a 29 July 1935 photograph of the completed building. The page exists; the image file 404s, so it corroborates the completion date only. |
| [SF Examiner, 2020](https://www.sfexaminer.com/news/supervisors-approve-150m-to-relocate-public-health-department-replace-hospital-chillers/) | $150 M approved to relocate DPH out of a building assessed as seismically unsound — occupancy, not form |

No copyrighted imagery is committed to this repository.

## 2. Verified dimensions, location and orientation

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.4186747, 37.7781359` | measured — footprint AABB centre |
| Footprint | 63.2 × 37.1 m oriented block, polygon area 2,274 m² (97 % of its OBB) | measured from OSM geometry |
| Long-axis heading | 80.6° / 260.6° true (the Civic Center grid, 9.4° off cardinal) | measured |
| Grove Street front normal | 350.6° true | measured |
| Corner entrance bay normal | 34.4° true | measured |
| Cornice / eave | **20.3 m** | measured twice and independently: LiDAR median 19.77 / majority 20.29, and OSM `height=20` |
| Crest (balustrade rail) | **21.4 m** | *estimated* — eave + a balustrade read at ~1.1 m off the 2008 photograph |
| Storeys | 4 | PCAD |

Footprint as authored (app tangent projection, recentred on the AABB centre,
x east / y north, CCW):

```
(-34.17,  13.32)  P0  NW corner            (-28.25, -22.72)  P5  SW corner
(-31.87,   0.21)  P1  light-court step     ( 34.17, -12.99)  P6  SE corner
(-28.53,  -0.31)  P2                       ( 28.99,  18.29)  P7  chamfer S end
(-26.81, -11.20)  P3  light-court step     ( 22.52,  22.72)  P8  chamfer N end
(-30.10, -11.62)  P4
```

| Edge | Length | Outward normal | What it is |
|---|---|---|---|
| P8→P0 | 57.46 m | 350.6° | Grove Street front |
| P7→P8 | 7.84 m | 34.4° | the chamfered corner entrance bay |
| P6→P7 | 31.71 m | 80.6° | Polk Street |
| P5→P6 | 63.17 m | 170.6° | Dr. Tom Waddell Place (service alley) |
| P0→P1…P4→P5 | 13.31 + 3.38 + 11.02 + 3.31 + 11.25 m | 260.6° | west wall with two light-court steps, against 99 Grove |

## 3. What each side shows

**North (Grove Street), 57.5 m — the long public face.** Four storeys of light
warm-grey granite. A tall rusticated base with deep horizontal joints carries
three smooth-ashlar storeys above a slim string course. Second-floor windows
are the enriched ones: a small triangular pediment on consoles above, and below
the sill a projecting balconette whose near-black ground carries a row of gold
rosettes — the only saturated colour on the building. Third- and fourth-floor
windows are plain rectangles, the fourth noticeably shorter. Plain frieze, bold
modillion cornice, continuous open balustrade above it.

**North-east chamfer, 7.8 m — the corner bay.** The whole identity. Bottom to
top: a monumental round-arched entrance whose voussoirs radiate into the
rustication; a carved tympanum with a round **oculus** flanked by foliate
relief; a bronze-and-glass double door under a flat entablature lettered
DEPARTMENT OF PUBLIC HEALTH / 101 GROVE STREET; two ornate **bronze lantern
sconces on scroll brackets** flanking the arch; a cartouche keystone; the
gold-rosetted **balconette**; a tall window in a full pedimented aedicule; a
plain window; then cornice and balustrade carrying straight across.

**East (Polk Street), 31.7 m.** The same order and the same enrichment as
Grove, shorter. The corner bay is shared between the two, so the building reads
as one continuous L of public facade wrapping the corner.

**South (Dr. Tom Waddell Place), 63.2 m.** *Inferred — no photograph located.*
The service elevation on a 12 m alley. Period practice for a 1932 civic block,
plus the plain wall visible in orthoimagery, give: the same four-storey punched
grid on the same floor lines, without pediments, balconettes or rustication,
and a solid capped parapet in place of the open balustrade.

**West, 13.3 + 11.0 + 11.3 m in three steps.** *Inferred.* A party/light-court
wall against the Bill Graham Civic Auditorium; the two steps in the OSM polygon
are the court. Plainest of all.

**Top.** A brilliant white cool-roof membrane covering nearly the whole
footprint — a hard bright plane inside a grey cornice frame. A low penthouse
over the north-east corner bay, its plan following the chamfer, carrying a dark
rectangular monitor. An interior light court south of centre: a recessed darker
pad with a long plant block along it. Scattered small plant, ducts, hatches and
a slender mast on the west third. No signage, no terrace, no greenery.

## 4. Recognition cues (ranked)

1. The chamfered corner bay with its arched entrance and oculus.
2. The unbroken cornice-plus-balustrade line at a dead-level 20.3 / 21.4 m.
3. The two-tone vertical order: tall rusticated base under smooth ashlar.
4. The second-floor pediment-and-gold-balconette rhythm.
5. A brilliant white flat roof on a granite Beaux-Arts block.

## 5. Preserved / simplified

**Preserved** — the true footprint including the chamfer and both west steps;
the four-storey proportion with floor lines at 5.4 / 10.3 / 14.6 / 18.6 m;
cornice 20.3 m and crest 21.4 m; the corner bay's full stack; the continuous
cornice/balustrade on the three public faces; the gold rosettes; the white roof.

**Simplified** — ashlar joints, dentils, modillions, acanthus and egg-and-dart
are gone. The cornice is two clean beveled bands. Rustication is four proud
courses with three deep joints, not real coursing. Balusters are plain 0.16 m
blocks at ~1.15 m pitch between solid rails. Windows are an ink reveal plate
with a glass slab proud of it, one per bay per floor, a cross mullion only at
second floor. Each balconette carries three oversized rosettes where the real
one carries nine. The entrance is an archivolt ring, a dark arched field, a gold
oculus disc and a gold door. Lanterns are two gold blocks on ink brackets at
roughly 1.7× true size.

## 6. Uncertainties and conflicting evidence

1. **The crest is estimated.** The eave is measured twice; the +1.1 m
   balustrade is read off one photograph.
2. **South and west elevations are inferred.** No photograph of either was
   located. This is the largest correctness risk in the asset.
3. **Bay counts are a design choice.** The 2008 photograph is foreshortened and
   does not show the whole Grove elevation; 12 bays at 4.79 m is a proportional
   fit, not a count off a drawing.
4. **The LiDAR 32.4 m max return is unexplained** and is read as a slender roof
   mast. Deliberately not modelled — see `REPORT.md`.
5. **Architect attribution** rests on one local-history source; PCAD leaves the
   field blank.
