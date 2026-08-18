# 1 South Park — One South Park — reference dossier

Compiled 18 August 2026 for `artifacts/1-south-park/`. This is the research the model
was built from; `REPORT.md` records what the build actually did, including the places
where it departs from `docs/asset-plans/1-south-park.md`.

A **1919–20 reinforced-concrete tobacco warehouse** closing the east end of the South
Park oval, on the corner of South Park and Second Street. Three storeys of arcaded
concrete wall with a bold cornice, converted in 2004–2007 by **LDP Architecture** for
Santa Fe Partners (builder Webcor) into **One South Park** — 35 loft condominiums,
about 5,000 ft² of ground-floor commercial and 35 at-grade stacked parking spaces —
with **two more storeys added as a set-back rooftop penthouse**, two light courts
carved down through the middle of the plan, and landscaped private roof decks. Gold
Nugget Grand Award 2011; California Construction *Best Renovation of California* 2008.

At 1,570 m² it is the largest building on the oval by a factor of two, and the only one
whose roof carries as much design as its elevations.

## 1. Sources, and what each establishes

| Source | Establishes |
|---|---|
| **OSM** [`way/112759870`](https://www.openstreetmap.org/way/112759870) | The footprint (8 vertices; two are 1.1 m and 2.7 m survey slivers, cleaned to the 6-sided polygon in §4), `addr:housenumber=1`, `addr:street=South Park`, `height=18`. |
| **DataSF Building Footprints** `ynuv-fyni` (2010 LiDAR/Pictometry) | Footprint `SF3775181` / `201006.0002174`, 1,585 m². Roof heights over **5,142 cells**: median **17.77 m**, mean 17.21, mode (majority) **18.76**, max **20.22**, min **9.42**, σ **1.80**; ground 13.33 m NAVD88. The 2010 survey postdates the 2007 completion, so it sees the finished building including the penthouse. Neighbours: `SF3775046` (17–19 South Park) median **6.60 m**; `SF3775042` (21–29 South Park) median 9.60 m. |
| **SF Assessor secured roll** `wv5m-vpq2`, block **3775**, lots **181–216** | 36 condominium lots, every one `year_property_built = 2007`. Lot 181 is `Commercial Retail`, 3,611 ft², unit **103**. The rest are residential and their unit numbers give the section: **101, 102** on level 1, **201–211**, **301–311**, **401–411** — 2 + 11 + 11 + 11 = **35 units**, matching the developer's advertised figure exactly. Eight of the 4xx lots (401, 403, 404, 407, 408, 409, 410, 411) carry `number_of_stories = 2`: the two-level penthouses. Unit areas 724–2,659 ft². |
| **SF Building Permits** `i98e-djp9`, 85 permits at this address | The conversion in sequence. 1999-08-28 "core & shell alt to (e) **3 story** concrete bld seismic strengt"; 2000-08-26 "add 1 story w/in (e) bldg per city planning variance"; **2004-05-19 PA #200405194312 "renovation of (e) 3 story concrete warehouse. add 2 more stories. adding 35 residential units, off street park…", existing 3 storeys → proposed 5**; 2006–07 fire/alarm/access revisions all at 5 storeys; 2009-11-16 "convert (e) vacant office space to new deli (the american)" on the ground floor. |
| **LDP Architecture**, [One South Park](https://www.ldparchitecture.com/renovation-southpark.html) | "adaptive reuse of a 1920's former tobacco warehouse"; 52,164 ft²; 35 residential units; 5,000 ft² first-floor commercial; a penthouse unit; at-grade stackers for 35 cars; a rooftop deck; **"two curving courtyards carved out of the interior"**; "enclosed an existing railroad spur with modern fenestration"; an at-grade terrace preserving the historic railroad tracks. |
| **thefrontsteps**, [Dec 2007 walkthrough](https://thefrontsteps.com/2007/12/16/1-one-south-park-a-walkthrough-and-sales-update/) | Santa Fe Partners / Webcor; 35 units of which **9 penthouses**; seismic retrofit; wrap-around penthouse deck. *observed (sales coverage)*. |
| **Google Street View**, panos `Bm7I6a4Jcm8yGuvM9xB_Iw` (South Park street) and `fsz2ATpXhpoUxD3vwNgjew` (Second Street) | Every elevation number in §4–5. Method in §3. |
| **Google Maps satellite**, z21 (0.0590 m/px) | The roof plan: the raised penthouse block and its extent, the terrace bands with their hedge rows, a lawn patch near the west corner, the light court, the rooftop mechanical. z22 returns the 1,555-byte no-data placeholder over this block, so z21 is the ceiling here. |
| `artifacts/21-south-park/`, `artifacts/300-brannan/` | The two party-wall neighbours: their heights, their `Toy_stone` palettes (see §7), and 21 South Park's `exclude: 16`, which the integration must not disturb. |

Not obtained: interior plans, the LDP drawing set, and photography of either party wall.
None is needed — both party walls are blind, and the south-east one is hidden in the
real city by a 21 m neighbour.

## 2. History

South Park was laid out in 1854 as an English-style residential oval and was industrial
by the 1900s. This block's warehouse went up in 1919–20 and traded tobacco. It was
still a warehouse in 1999, when a seismic-strengthening permit describes it as a "3
story concrete bld". Between 2004 and 2007 it was gutted, retrofitted, given two set-back
storeys and converted to 35 lofts — one of the earliest of the SoMa warehouse-to-loft
conversions to keep its industrial face intact rather than re-skin it. The ground floor
has been retail or restaurant ever since (a deli from 2009; a pharmacy at the time of
the reference photography).

## 3. How the elevation heights were measured

The building has no landmark designation report and no published drawings, so the
storey lines come from **rectified photogrammetry**:

1. Two Street View panoramas were located by their equirectangular tiles. Each pano's
   reported lat/lon was **verified rather than trusted**: three known footprint corners
   were projected to azimuths and matched against the panorama's own columns. The
   residual was **±0.06°** across the three, which pins the camera to well under a metre
   and makes the perpendicular distance to each wall reliable (23.0 m to the north
   corner from the South Park pano; 16.7 m to the Second Street wall from the other).
2. A levelled equirectangular panorama has the horizon exactly on its centre row, so
   elevation angle is `(H/2 − y)/H × 180°` and height is `h_cam + D·tan θ`. Camera
   height was solved from the visible ground line at 2.6 m.
3. Each wall plane was then **reprojected to an orthographic elevation** with a metric
   grid, and the storey lines read straight off it.
4. The vertical calibration was checked independently by the **circular medallions**,
   which come out **0.75 m wide × 0.69–0.75 m tall** — i.e. round — so the vertical
   scale is good to about 8%.

Cross-check: the DataSF LiDAR summary is bimodal (mean 17.21 < median 17.77 < mode
18.76, σ 1.80 over a satellite image that is plainly a bright raised membrane over
about 60% of the plan and darker decking over the rest). Solving

```
f·H + (1−f)·L = 17.21 ,   f(1−f)(H−L)² = 1.80² ,   f = 0.62
```

gives **H = 18.6 m, L = 14.9 m**. That is the penthouse roof and the terrace deck, and
neither number was tuned to the photogrammetry, which independently puts the cornice
crest at 15.75 m with the deck a little below it and planting standing on it. The two
methods agree, so the roof section is treated as **measured**.

## 4. Dimensions, orientation and placement

Cleaned footprint, metres east/north from the wall-box AABB centre
`-122.3928634, 37.7820480` (the shipped anchor; the model's own AABB centre lands
0.001 m from it):

```
S  (  1.939, -26.843)   south corner   (party x party)
E  ( 28.847,  -0.328)   east corner    (party x Second Street)
Cc (  9.003,  19.713)   step, outer
Dd (  5.387,  16.110)   step, inner
N  ( -5.498,  26.843)   north corner   (Second Street x South Park)
W  (-28.847,   3.527)   west corner    (South Park x party)
```

| Face | Length | Outward normal | What it is |
|---|---|---|---|
| S → E | **37.78 m** | **135.4°** | party wall, 300 Brannan (21 m — taller, hides it) |
| E → Cc | **28.20 m** | **45.3°** | hero — Second Street |
| Cc → Dd | **5.11 m** | **315.1°** | hero — the re-entrant return |
| Dd → N | **15.29 m** | **44.6°** | hero — Second Street, recessed 5.1 m |
| N → W | **33.00 m** | **315.0°** | hero — South Park street |
| W → S | **43.25 m** | **224.6°** | party wall, 17–19 South Park (6.6 m — ~9 m exposed) |

Area 1,570 m². The area centroid is 0.69 m from the AABB centre; the **AABB centre** is
the anchor, because `placeGeneric` seats the model's origin and the contract makes that
origin the model's XY bbox centre.

**The re-entrant step is real.** Predicted from the OSM ring at equirect columns 254 and
341 of pano `Bm7I6a4Jcm8yGuvM9xB_Iw`, the return wall shows up there flat-on with one
arch in it. The northern 15.3 m of the Second Street frontage stands 5.1 m back from the
southern 28.2 m.

Because the block sits at ~45° to the world axes, the model's axis-aligned XY bounding
box is **58.9 × 54.9 m** even though its longest side is 43.2 m. That is the rotation,
not a scale error.

### Storey lines

| Feature | z (m) | Source |
|---|---|---|
| Plinth top / arch sill | 1.05 | rectified elevation |
| Arch impost | 6.10 | rectified elevation |
| Arch crown | 7.05 | rectified elevation |
| Medallion centre | 7.00 | rectified elevation |
| String course | 7.50 → 8.20 | rectified elevation |
| Window row 1 (taller) | 8.35 → 11.00 | rectified elevation |
| Window row 2 (shorter) | 11.90 → 13.90 | rectified elevation |
| Cornice bed mould | 14.55 | rectified elevation |
| **Cornice crest** | **15.75** | rectified elevation, ±0.6 m |
| Roof deck / terraces | 15.00 | LiDAR low mode 14.9 |
| Light-court floor | 9.40 | LiDAR `hgt_min` 9.42 |
| **Penthouse roof** | **18.60** | LiDAR mode 18.76 |
| **Stair/lift overrun — model crest** | **20.20** | LiDAR `hgt_max` 20.22 |

Arcade rhythm: measured bay pitch **3.94 m**, arch width **2.63 m**, arch rise/span
**0.38** on Second Street. The model divides each hero face uniformly — 7 bays on the
28.2 m plane, 1 in the step return, 4 on the 15.3 m plane, 8 on South Park — giving
pitches of 4.03, 5.11, 3.82 and 4.13 m, all within 0.2 m of the measurement.

## 5. What each side shows

**North-east (Second Street), 48.6 m over three planes — hero.** A low plinth to
1.05 m; then the **arcade** — round-arched openings 2.63 m wide springing from a plain
impost at 6.10 m to a crown at 7.05 m, the head filled with radiating fanlight glazing
and the body with a gridded steel sash. A **white circular medallion** 0.75 m across
sits in each spandrel at 7.00 m. Above it a **projecting string course**, 7.50 → 8.20 m,
unbroken. Then two window storeys of large steel-sash grids nearly filling their bays:
a taller row 8.35 → 11.00 and a shorter row 11.90 → 13.90. Then the **cornice**: bed
mould 14.55, crest 15.75, a bold projecting crown. Behind and above it the **charcoal
penthouse**, set back several metres, roof at 18.6 m, with roof planting visible over
the parapet from the street.

**North-west (South Park), 33.0 m — hero.** The same three registers in the same
language, eight bays. Two differences. The arches on this side photograph as fuller
semicircles and read taller. And this elevation carries the working openings: one arch
holds a **roller shutter** (the car-stacker entrance) and a wider bay near the west end
holds the **residential entrance**, with the **preserved railroad spur** curving out of
it across the sidewalk. The rails are in the public right of way and are out of scope.

**South-west (party wall, 17–19 South Park), 43.25 m.** Blind. The neighbour's roof is
at 6.60 m against this building's 15.0 m deck, so about **9 m of this wall stands
exposed** and is fully visible in the baked city from the south. Plain concrete, no
openings. *Inferred*, and safe to infer.

**South-east (party wall, 300 Brannan), 37.78 m.** Blind and hidden — 300 Brannan is
21 m to this building's 15.75 m cornice. *Inferred*.

**Top.** Half the design. A **raised penthouse block** over about 60% of the plan,
pushed to the north-east and south-east and set well back from the other two sides,
with a near-white membrane roof, small vents and two low mechanical blocks. A **light
court** cut down through it, dark, with greenery at the bottom. A **stair/lift overrun**
near the middle, the tallest thing on the building. A **north-west terrace band** of
warm timber decking with a continuous clipped **hedge row** along the parapet, planters,
and a small **lawn patch** near the west corner; a **south-west terrace band** with more
decking, pergolas and planters. Both are the private roof decks of the level-4
penthouses, which is why they are furnished rather than empty.

## 6. Recognition cues (ranked)

1. **The arcade of tall round-arched openings** wrapping both hero elevations on an
   otherwise plain wall.
2. **The white circular medallions** in the spandrels — small, cheap, and the detail
   nobody else on this oval has.
3. **The block-ness** — 1,570 m² with a re-entrant step, twice the plan area of
   anything else on the oval.
4. **The dark two-level penthouse over the pale cornice**, with landscaped terraces —
   the aerial camera's first read.
5. **The two window storeys of gridded steel sash**, one tall row and one short row.

## 7. Features preserved, simplified and dropped

**Preserved:** the arcade and its rhythm; the medallions (exaggerated from 0.75 m to
0.90 m); the string course and cornice as unbroken rings; the two window rows and their
different heights; the re-entrant step; the penthouse, its setbacks and its darkness;
the light court as a real cut; the terraces, hedges, lawn, planters and pergolas; the
roller-shutter and entrance bays on South Park.

**Simplified:** the sash grid is one mullion cross per opening, not a pane grid — at a
4 m bay pitch across 48 m of frontage a real grid is sub-pixel and turns the elevation
into corduroy; the fanlight is a single two-tone head, not radiating bars; the cornice
is two steps, not a moulding profile; the arch rise is modelled at 0.42 of the span,
between the 0.38 measured on Second Street and the fuller semicircles photographed on
South Park.

**Dropped:** the sidewalk railroad spur (public right of way, out of scope); the
individual roof furniture; the ground-floor signage; both party walls' articulation
(there is none).

**Palette.** Both party-wall neighbours are `Toy_stone` (d9d2c2) bodies, and three
adjacent stone blocks on one corner merge into a single beige mass from the aerial
camera. This building's paint is measurably cooler and lighter than either — sampled
off the rectified elevation the wall is near-neutral with a faint cool cast — so the
body takes one documented off-palette colour, **`Toy_dove` d4d6d4**. That is a WARN in
`sf-asset-check`, not a fail, and it is the same call `49-south-park` made with
`Toy_sage`. The penthouse is **`Toy_slate` 6f7883**, *not* `Toy_roofd` (45454a): that
renders as rgb(9,9,12) under the app's lighting, and the penthouse is the model's
second-biggest visible mass — it has to read as a dark grey, not a hole.

## 8. Uncertainties and conflicts

1. **The cornice crest carries ±0.6 m.** It is photogrammetric, with camera height as
   the dominant residual. The crest (20.2 m) and the penthouse roof (18.6 m) are
   LiDAR-backed and firm; the cornice is the softest number in the model.
2. **Arch head geometry.** Second Street rectifies to rise/span ≈ 0.38; the South Park
   arches photograph as fuller semicircles. The model uses 0.42 for both.
3. **The 12-foot-ceiling claim.** Listings advertise 12-foot ceilings; the rectified
   elevation gives 3.2 m and 3.0 m floor-to-floor on levels 2 and 3. Both can be true
   only of the double-height ground floor or the penthouses. The elevation wins.
4. **Penthouse setbacks** are estimated from a z21 satellite image whose segmentation
   cannot separate bright roof membrane from bright terrace pavers. The ~60% area
   fraction is solid; the individual setbacks are not.
5. **"Two curving courtyards".** LDP's own description says two, and curving. The
   satellite image shows what reads as one long rectilinear slot with a bulge. The model
   builds one rectilinear court. If better imagery appears, this is the thing to fix —
   it is on the roof and the aerial camera will see it.
6. **Aggregator disagreement.** rubyhome gives "1906, 3 storeys"; Compass gives 2007.
   The permits and the assessor are the authority: a 1919–20 three-storey warehouse,
   converted to five storeys and 35 units, completed 2007.
