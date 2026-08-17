# Hotel Madrid (22–24 South Park) — reference dossier

Compiled 16–17 August 2026 for `artifacts/22-south-park/`. The plan behind it is
`docs/asset-plans/22-south-park.md`; this file records what was verified at build
time, what was corrected, and what stayed inferred.

## 1. Identity

| | |
|---|---|
| Name | **Hotel Madrid**, built as the **Eimoto Hotel** |
| Addresses | 22 South Park (business/tenant), 24 South Park (storefront) |
| APN | 3775-048 (block 3775, lot 048) |
| Built | 1915 |
| Storeys | 3 over a basement |
| Structure | Type V wood frame, lap siding |
| Rooms / units | 55 rooms on the Assessor's roll; 43–44 tenanted SRO units + 1 commercial space |
| Owner | Mission Housing Development Corporation, acquired and rehabilitated 1987; sold into the Scattered Sites partnership 29 May 2020 |
| Zoning | SPD (South Park District) |
| Assessor use code | COMH / Commercial Hotel, with a **welfare exemption** (nonprofit ownership) |

A through-lot on the north rim of the South Park oval, running from South Park at
the south-east to Taber Place at the north-west, with blind party walls on both
long sides: 10 South Park to the north-east and 26–28 South Park to the
south-west. It is the third building in the **South Park Scattered Sites**
affordable-housing rehabilitation, alongside the Park View at 102 South Park and
the Gran Oriente Filipino at 104–106 — both already modelled in this repo.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, blklot 3775048 | **the geometry**: a trapezoid, 444.5 m², with the South Park frontage traced as a 25-vertex concave arc |
| SF Assessor secured roll `wv5m-vpq2` | 1915, 3 storeys, 55 rooms, 16 bathrooms, lot 4,893.3 sq ft, building 12,729 sq ft, COMH, welfare exemption, sold May 2020 |
| DataSF Building Footprints `ynuv-fyni`, SF3775048 (**2010** LiDAR) | heights: **max 14.22**, **median 12.39**, mean 12.35, majority 12.52, min 9.31 m, **std 0.63 m**, ground 12.36 m NAVD88; footprint **372.3 m²** on a 444.5 m² lot |
| SF Building Permits `i98e-djp9`, 30 records | the 1983–85 rehabilitation ($492 k) and community-kitchen expansion; 1985 **solar hot-water panels on the roof**; 1996 reroof; 1997 **elevator serving ground floor and basement only** (so no roof overrun); 2011 fire-alarm upgrade (80 horn/strobes, 21 detectors); 2017 **mandatory soft-storey retrofit**, filed twice (residential + commercial); Dec 2019 **$2.1 M SRO rehab** with roof drains/gutters and exterior paint "in kind"; 2023 **awning repair**; 2023 **light-well waterproofing** |
| OSM way/112926338 | `addr:housenumber=22;24`, `height=12` |
| missionhousing.org/madrid | SRO acquired and rehabbed 1987, permanent housing for formerly homeless and very low-income adults, 44+ units plus one commercial space |
| sccsgroupllc.com — South Park Scattered Sites | the current rehabilitation: Hotel Madrid with the Parkview (102) and Gran Oriente (106); **Type V Wood Framed**; 106 units at ≤ 80% AMI; ground floors reserved for restaurant tenants |
| DAHLIA `a0W4U00000KnGxgUAF` | 43 SRO units, 80–290 sq ft, community room, shared kitchens, 24-hour desk |
| apartments.com | "22-26 S Park St", 1915, 3 stories, 44 units |
| Alamy stock caption + Wikipedia *South Park, San Francisco* | the **Eimoto Hotel** attribution and the Japanese-community context — **single-thread, see §6** |
| foundsf.org, *Residential vs. Tourist Hotels* | the Madrid as a residential (not tourist) hotel through the 1980s conversion fights |
| opengovus SF business 0955172-02-001 | Mission Housing Dev Corp DBA Hotel Madrid at 22 S Park St, 1988-07-01 to 2020-05-31 |
| Google Street View, **Jan 2025**, pano near `37.78205,-122.39356`, headings 300–360° | **the South Park elevation** — observed |
| Google Street View, **Jan 2025**, pano near `37.78249,-122.39391`, heading 150° | **the Taber Place rear** — observed, and unmistakably this building (the sage/clay scheme appears nowhere else on the block) |
| Google Maps satellite (Vexcel 2026, near-nadir, z21, pinned at the parcel centroid) | **the roof**: a large dark PV array, plant at the Taber end |

## 3. Verified dimensions and location

- **Anchor (design):** `-122.3936498, 37.7822952` — the surveyed parcel's area
  centroid. After recentring on the model's XY bbox the manifest anchor is
  `-122.3936099, 37.7823247` (a 4.8 m shift, because the trapezoid's bbox centre
  is not its area centroid).
- **Footprint — a trapezoid, not a rectangle:**

  | edge | length | faces | elevation |
  |---|---|---|---|
  | East → South corner | 14.99 m chord, **15.14 m of arc** | chord normal 159.4° | South Park front (curved) |
  | South → West corner | **30.13 m** | 225.18° | party wall with 26–28 (blind) |
  | West → North corner | **13.68 m** | 315.15° | Taber Place rear |
  | North → East corner | **36.28 m** | 45.19° | party wall with 10 South Park (blind) |

  The two party walls are parallel; the Taber Place rear is square to them; **the
  South Park frontage is not** — the oval turns 31° through this lot, which is
  what makes one party wall 6.15 m longer than the other. Chord-quad area
  454.2 m²; the concave arc removes a 9.7 m² segment, giving the measured
  444.5 m². The Assessor's `lot_area` (454.6 m²) matches the chord quad.
- **Frontage curvature:** concave toward the park, sagitta 0.93 m, radius ≈ 28 m,
  sweep ≈ 31°. The tangent runs ~263° at the East corner and ~225° at the South
  corner — where it meets 26–28 South Park's straight frontage square, because
  the neighbour sits on the part of the rim that has stopped turning.
- **Roof deck:** 12.39 m. **Cornice crest / `targetHeightM`:** 14.22 m.
- **Building vs lot:** the DataSF footprint is 372.3 m² against a 444.5 m² lot.
  372.3 × 3 storeys = 1,117 m² ≈ the Assessor's 12,729 sq ft. The 72 m²
  difference is the light well.

## 4. Observations, side by side

**South-east (South Park) — observed, Jan 2025.** Three storeys over a
storefront, on 15.14 m of curved face. The body is **sage/sea-green** in lap
siding. The upper two floors carry **paired double-hung sash in single wide
openings with flat salmon-clay casings** roughly 150 mm wide, sashes white,
several with venetian blinds. Four bays; reading south-west to north-east: window
pair, window pair, the **fire-escape bay** (a door onto the landing), window pair.

The **fire escape** is painted the same sage green as the body — the unusual
thing about it, since almost every fire escape in SF is black. Cantilevered
landings at both upper floors with horizontal-bar railings, a diagonal stair, and
a drop ladder.

A **deep bracketed cornice** in rust-clay crowns the wall. A **rust-clay belt
course** separates the storefront from the upper floors and returns at both ends.

The **ground floor is a dark slate-blue storefront band**. South-west half: the
taqueria — plate glass in white frames, a recessed glazed entrance, "24" above the
door, a transom sign band, and a **round white louvered exhaust fan** at the
south-west end. North-east half: the residential entrance framed in rust-clay
under a **curved barrel awning**, with a further glazed bay beside it. A low dark
bulkhead runs beneath the glazing.

**North-west (Taber Place) — observed, Jan 2025.** A finished elevation, not a
service back: the same **sage-green lap siding** (clearly readable as horizontal
boards here) with the same **salmon-clay trim**. A shallow canted **bay window**
at the upper floors, two tall **arched-headed ground-floor windows behind ornate
clay-painted security grilles**, a flush clay door beside them, and a wide clay
panelled service door at the south-west end. The green fire escape returns onto
this face at the top.

**North-east and south-west — party walls.** Blind. 10 South Park to the
north-east is 11.88–12.27 m and 26–28 South Park to the south-west is 8.35 m, so
roughly **4 m of the south-west flank stands exposed above its neighbour's roof**
and is seen from the aerial camera. The north-east flank is effectively buried.

**Top — observed, Vexcel 2026 near-nadir.** A flat roof at 12.39 m carrying a
**large dark PV array** in long bands running north-west to south-east —
consistent with the 2019–21 rehabilitation and with the arrays on the other
rehabilitated SRO roofs on this block. A **light-well slot** is notched into the
north-east flank around mid-depth. Mechanical plant is grouped toward the Taber
Place end. The cornice reads as a bright edge along the curved South Park end.

## 5. Recognition cues (ranked)

1. **Sage green and salmon clay** — the colour pair is unique on this block.
2. **The bracketed cornice**, deep and projecting, over three storeys on a rim
   where the immediate neighbours are flat-topped.
3. **The green fire escape on the street face.**
4. **The curved frontage** following the oval — 0.93 m of bow over 15.14 m, and a
   lot 6 m deeper on one side than the other because of it.
5. The dark slate-blue storefront with its round white fan and the curved barrel
   awning over the residential entrance.

## 6. Uncertainties and conflicting evidence

- **The 14.22 m LiDAR maximum was believed**, where its neighbour's was not. It
  sits 1.83 m above the median on a footprint with a 0.63 m standard deviation —
  2.9σ. The party-wall trap that killed 26–28's maximum is **ruled out here**:
  both neighbours are *shorter* (10 South Park 11.88–12.27 m, 26–28 South Park
  8.35 m), so a bleeding cell could only pull the maximum down. The street-tree
  trap (592 Third Street) is not ruled out — mature trees stand hard against this
  frontage — but the 9.31 m minimum is explained by a **permit-confirmed light
  well** rather than by an edge artifact, which raises confidence in the record as
  a whole. Read as a 1.83 m parapet-frieze-cornice assembly.
- **The Eimoto Hotel attribution rests on one source** — an Alamy caption and a
  Wikipedia summary of the same claim. Highly plausible (pre-war South Park had a
  substantial Japanese population, and the Gran Oriente at 104–106 was itself the
  Hotel Maruichi/Omiya in the 1920s), but no primary source was found. A SoMa or
  Japantown historic context statement is where to look next.
- **The unit count has four different values** — 55 rooms (roll), 44 (Mission
  Housing, apartments.com), 43 (DAHLIA). They count rooms, tenanted units and
  subsidised units respectively. None of them drove the window count, which came
  from the photographs.
- **Front cladding: siding or stucco?** The Taber Place rear is unambiguously lap
  siding; the front reads smooth at Street View resolution with faint horizontal
  banding. Modelled as siding throughout, with grooves only on the rear.
- **The PV array's attribution** to *this* roof rather than the neighbour's rests
  on a pin-centred z21 near-nadir crop; the 2010 LiDAR predates the array and
  cannot corroborate it.
- **The current rehabilitation is live** and may have changed the exterior since
  the January 2025 capture the model was built from.

## 7. Features preserved, simplified and omitted

**Preserved:** the trapezoid footprint and the 315.18° party-wall heading exactly;
the curved frontage as four measured segments; the sage/clay colour pair on both
public elevations; the cornice as a real projecting volume with brackets; the
fire escape as a green object on the street face; three storeys; the flat roof
with its PV array and light-well slot.

**Simplified:** paired sash → one glazed panel per opening inside a flat clay
casing; the multi-pane storefront → one dark band with four openings; the fire
escape → two solid-sided landings and one diagonal stair slab, no balusters and
no drop ladder; the Taber Place bay → one shallow canted box; the arched grille
windows → two plain recessed openings in clay surrounds; lap siding → flat colour
with three grooves per storey on the rear only; the PV array → two solid slabs on
a rail, never individual modules; the light well → a dark recessed pocket in a
raised curb rather than a 3 m shaft (see REPORT.md §2.4).

**Omitted deliberately:** all tenant signage — the "MEXICAN GRILL • TAQUERIA •
BURRITOS • TACOS" transom lettering, the "TCP TOUCHSTONE FOR LEASE" banner and
the "24" address numeral — plus the wall-mounted security camera and lantern on
Taber Place, and the 1985 solar hot-water collectors (superseded by the modern
PV array).
