# 164 South Park — reference dossier

Compiled for `artifacts/164-south-park/`. Sources, measurements, orientation, and the
corrections made against `docs/asset-plans/164-south-park.md`. **This file, and REPORT.md,
beat the plan wherever they disagree.**

## 1. What the building is

164 South Park is a single-storey brick-and-timber warehouse at the west tip of the South
Park oval, on the union of two surveyed parcels — block 3775 lots **068** and **069**, both
addressed 164. Lot 069 was built in **1907** (3,170 sq ft assessed, 1 storey); lot 068 in
**1946** (1,581 sq ft, 1 storey). Both are assessed as Industrial, zoning SPD.

In 2024–25 it received a new street front by **Stanley Saitowitz | Natoma Architects** — DBI
permit `202305248506`, issued 2024-05-03, valuation $179,615, with `202406104101` (Atrium
Structural, 2024-06-21) alongside. The architect describes it in three sentences that are
effectively the modelling brief:

> The new façade blends with the brick neighbor using large scale red panels in stretcher
> bond. A ribbon window tracks the shift around the oval, dropping to form the glazed entry
> recess. Above, a slender canopy shelters the front.

The concrete "doormat" at the entry records that Twitter (first office, 2006–2008) and
Instagram (2010) were both founded in this room. That is why the building matters, and it is
also why the roof matters: contemporary accounts describe the space as warehouse-like and
light-starved apart from its skylights, which are visible from the air and are modelled.

## 2. Sources

| Source | Establishes | Confidence |
|---|---|---|
| `saitowitz.com/164-south-park` (project text + 14 photographs) | facade design intent, materials, the ribbon/entry move, the canopy, the numerals | **primary** — the only source for the 2025 facade |
| DataSF `acdm-wktn` (parcels) | the surveyed two-lot footprint, 439.5 m² | measured |
| DataSF `ynuv-fyni` (`SF3775069`) | LiDAR roof statistics: median 5.44 m, modal 4.61, mean 5.53, sd 0.84, min 3.24, max 9.25, 1,715 cells | measured |
| SF Assessor `wv5m-vpq2` (2025 roll, lots 068 + 069) | 1907/1946, **one storey each**, industrial use, assessed areas | measured |
| OSM `way/124884357` | shape cross-check only; `height = 5` is a Bing guess | low |
| Google satellite z21 / Esri z20 | roof membrane, four skylight monitors, two mechanical boxes, party relationships | observed |
| `openpermitdata.com/sf/address/164-south-park` | the three 2024 permits | measured |
| CNBC (2018), Business Insider (2021 ×2) | tenant history; "two skylights", "light-starved" | observed |
| `compass.com`, `cityfeet.com`, `showcase.com` listings | 1907, 1 story / 3,170 sq ft; "recently remodeled facade by Stanley Saitowicz"; "new foundation for the front half" | listing photos — treat as *observed*, and see §5 |

## 3. Measured geometry

**Anchor (design, parcel-union area centroid):** `-122.3949238, 37.7812072`
**Anchor (manifest, after recentring on the model's XY bbox):** see REPORT.md — the build
script prints it.

Footprint, metres east/north of the design anchor:

```
v0 (-19.725,  12.057)   v3 ( 15.061,  -9.380)   v6 ( 15.957,  -0.586)
v1 (  9.974, -17.722)   v4 ( 15.117,  -6.321)   v7 (  3.482,   1.704)
v2 ( 15.275, -12.461)   v5 ( 15.395,  -3.595)   v8 (-13.260,  18.491)
```

| Edge | Length | Outward | Condition |
|---|---|---|---|
| v0→v1 | 42.06 m | 225.1° | party wall, 166 South Park — blind |
| v1→v2 | 7.47 m | 135.2° | **exposed** — chamfer, south end of the frontage |
| v2→v3 | 3.09 m | 86.0° | **exposed** — arc facet |
| v3→v4 | 3.06 m | 91.1° | **exposed** — arc facet |
| v4→v5 | 2.74 m | 95.8° | **exposed** — arc facet |
| v5→v6 | 3.06 m | 100.6° | **exposed** — arc facet |
| v6→v7 | 12.68 m | 10.4° | party line, 160 South Park |
| v7→v8 | 23.71 m | 45.1° | rear flank, mid-block gap |
| v8→v0 | 9.12 m | 315.1° | rear wall |

Exposed street elevation **19.42 m** in five planes turning through 49°. Cross-check: the
DataSF LiDAR building footprint `SF3775069` has **IoU 0.895** against this polygon and its
centroid is 0.96 m away; OSM `way/124884357` is 6.4% larger and 2.60 m off.

Vertical scheme, all above the model's z = 0:

| Element | Height | How |
|---|---|---|
| Rear parapet crest (= target height) | **5.400 m** | LiDAR median 5.44 m, rounded to the shipped figure |
| Roof deck | 5.10 m | inferred: crest − 0.30 m upstand |
| Screen parapet | **4.10 m** | photogrammetric, two photographs |
| Ribbon head / sill | 2.95 / 1.55 m | photogrammetric |
| Entry glazing head | 3.30 m | inferred |
| Canopy soffit / top | 2.98 / 3.12 m | photogrammetric / exaggerated thickness |
| Transom rail | 2.35 m | observed |
| Panel course | 0.47 m | photogrammetric (8.7 uniform courses to the parapet) |

Photogrammetric working for the 4.10 m screen parapet — both frames contain a 2.134 m
commercial door leaf and the parapet, which fixes the horizon and makes the result nearly
independent of the assumed camera height:

* `005c.jpg` — door 1720→1195 px, pier base 1790 px, parapet 595 px → **4.11 m** at eye 1.55 m,
  4.14 m at 1.65 m.
* `001.jpg` — door 722→540 px, pier base 742 px, parapet 348 px → **4.01 m** at 1.55 m,
  4.04 m at 1.65 m.

`022b.jpg` confirms the parapet is **level** along the frontage: apparent wall height falls
700 → 670 → 610 px across three columns exactly in step with the receding base line.

## 4. Orientation — which end the entry is on

Three independent readings, all agreeing that the entry is at the **north** end:

1. `001.jpg`, square from the street (camera facing west, north on the right): the entry sits
   about a quarter in from the right, with a brick neighbour beyond the left end. 166 South
   Park (south, lot 070, 1912 "Flat & Store") is brick; 160 South Park (north, lot 067, 1924)
   is not.
2. `20250526_191412380` looks out of the entry recess along the facade and shows a Bay Wheels
   dock in the direction the facade runs away. The only Bay Wheels station within 200 m is
   42 m out on a bearing of **172°** — due south.
3. `20250526_191348966` shows the entry glazing wrapping an outside corner, which places it on
   the v5 facet corner, 3.06 m south of v6.

Built placement: recess from **1.90 m to 5.50 m south of v6**, straddling v5, leaving a 1.90 m
red pier to the north party line. The ribbon then runs unbroken from 5.50 m south of v6 to v1
— **13.9 m of glass in five mitred planes.**

## 5. Corrections against the plan and against the sources

1. **`hgt_maxcm = 925` is not this building.** The LiDAR distribution is tight and flat
   (sd 0.84 m, modal 4.61, median 5.44) and cannot contain a 4 m step; the assessor records
   one storey on both parcels; the aerial shows an unbroken flat roof; 160 and 166 visibly
   overtop it. Target height is the **median, 5.4 m**. This is the inverse of the
   156 South Park case, where the maximum was real. What sits at 9.25 m is not identified —
   the record's `peak_1st_m` is 16.53 m, a tree, and there is a large tree overhanging the
   north-west end of this roof.
2. **The Showcase listing's "2-story" and 7,400 sq ft are wrong** against the assessor
   (1 storey ×2, 4,751 sq ft assessed on a 4,731 sq ft site) and against the aerial.
3. **Both parcels are addressed 164.** One building spans them. Modelling only lot 069 would
   lose a third of the site.
4. **OSM `height = 5` is Bing-sourced** and right only by luck.
5. **Every dataset predates the facade.** The 2010 LiDAR, the DataSF footprint and the
   satellite tiles all show the previous front. The architect's photographs are the only
   source for the screen, and the photogrammetry above is the only measurement of it.

## 6. Departures from the plan, made during the build

| Plan said | Built | Why |
|---|---|---|
| Screen returns 0.40 m around the v1 and v6 corners | Screen caps flush at v1 and v6 | A 0.40 m return offset 0.35 m proud of a party line penetrates the neighbour's wall. The real panel meets the brick with a clean vertical edge (`003.jpg`), which is what a flush cap gives. |
| Entry recess cut through the screen full height (0–4.10 m) | Recess 0–3.30 m, red lintel band 3.30–4.10 m above it | `005b/005c.jpg` show red panel continuing above the canopy to the parapet. A full-height cut would open the recess to the sky. |
| Joint reveal every 0.94 m ("four bands") | Reveal every 0.94 m — kept | At the real 0.47 m course the reveals read as clapboard from the app's camera, the opposite of "large scale panels". |
| Numerals 0.09 m tall on the fascia | 0.35 m tall block glyphs | 0.09 m was a misreading; `005c.jpg` puts them at ~0.41 m. At 0.09 m they are invisible at every camera distance. |
| Skylight monitors 0.35 m tall | 0.28 m | Nothing may exceed the 5.40 m crest; 5.10 + 0.35 would. |
| Mechanical boxes 0.60 m tall, `Toy_steel` | 0.26 m tall, `Toy_ink` | Height for the same reason; `Toy_steel` plant on a `Toy_steel` deck is invisible from above. |
| Skylight curbs `Toy_steel` | `Toy_trim` | Same invisibility problem; the aerial shows pale curbs against the grey membrane. |
| Body ring notched for the entry recess | Notched only to 3.30 m; the full ring carries above | Otherwise the parapet and the roof outline inherit a notch that does not exist. |

## 7. What to preserve, what to simplify

**Preserve:** the continuity of the ribbon across all five facets; the drop to the ground at
the entry; the 1.3 m step between the 4.10 m screen and the 5.40 m building; the 0.35 m
proudness of the screen (it is what makes that step read as two objects); the wedge plan.

**Simplify:** the panel bond (every second joint only, one staggered vertical per band); the
mullion count; the roof (four monitors, two boxes, nothing else); the rear elevations, which
are blind brick and almost never seen.

**Do not add:** cornice, plinth, signage band, planters, street trees, the sidewalk
inscription. The real building has none of these and the design is an exercise in having none.
