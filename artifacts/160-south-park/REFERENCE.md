# 160 South Park — reference dossier

Research behind `160-south-park.glb`. Compiled 16 August 2026. The plan
(`docs/asset-plans/160-south-park.md`) is the longer document; this file records what was
verified for the build, what was inferred, and the corrections the build made to the plan.

## 1. What the building is

A two-storey commercial-front building of 1924 on the **north-west rim of South Park**,
the oval laid out in 1852–54 that is San Francisco's oldest planned residential square.
It stands on a 6.17 m frontage between two party walls: 156 South Park to the north (a
two-storey steel-sash industrial building, tenant "multistudio") and 164 South Park to the
south (1907, currently being re-fronted by Stanley Saitowitz | Natoma Architects).

The whole building is painted one flat cool slate charcoal — walls, end pilasters, window
surrounds, the lintel band and the shopfront frame. Its interest is relief, not colour,
and it carries exactly two accents: a **round-arched multi-pane window** centred on the
upper storey under a moulded archivolt, and a **projecting pent roof of red barrel tile**
across the top of the street elevation. At street level a third, smaller accent: a flush
warm-wood door beside the shopfront. The ground floor presently carries a commercial
tenant ("Curie.Bio" decal on the storefront glass).

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF **parcels** `acdm-wktn`, `blklot=3775067` | the surveyed lot polygon — 216.8 m², 6.17 m frontage chord, 6.08 m rear, 36.4 m deep on the south party line and 33.2 m on the north, bending 33° partway back. **The geometric backbone of the model.** |
| DataSF **addresses** `ramy-di5m` | 160 South Park exists as an address and resolves to block 3775 lot 067. Also the rim's ordering: 150, 156, 160, 164, 166 running south-west. |
| DataSF **assessor roll** `wv5m-vpq2`, rolls 2023–25 | built **1924**; **2 storeys**; 6 rooms; 2 baths; 2,291 sq ft lot; use `SRES` with a Homeowners exemption. |
| DataSF **land use** `fdfd-xptc`, `mapblklot=3775067` | **3,674 sq ft** of MIPS (office) floor area, 0 sq ft residential, 1 residential unit. This number is what makes the built depth solvable. |
| DataSF **building permits** `i98e-djp9` | three permits since 2002 (rear-yard fence 2002; rear windows/doors and baths 2004; voluntary seismic upgrade and rear stucco → lap siding 2005), **each recording 2 storeys before and after**. No vertical addition, so the 2010 LiDAR is still current for height. |
| DataSF **LiDAR footprints** `ynuv-fyni`, `mblr=SF3775067` (`201006.0020110`) | ground 6.51–8.05 m NAVD88 (median 6.91); height mode **8.81 m**, max **9.41 m**, median 7.79 m, mean 6.66 m, σ 2.56 m over 882 cells. |
| **Google Street View**, South Park north-west rim, **Jan 2025** capture, viewpoints ≈ `37.78123 / -122.39470–122.39475`, headings 288°–293° | the entire street elevation: the arch and its archivolt, the two flanking multi-pane windows, the red barrel-tile pent, the moulded band beneath it, the proud lintel with two square tie-plates, the recessed shopfront, the warm-wood door, and the roof stack at the north end. Also the **identification**: the numeral "156" is mounted beside the *steel-sash* building's recessed entry, which fixes 160 as the arched building to its south. |
| **Esri World Imagery** (z20, ~0.12 m/px), stitched and overlaid with the DataSF parcels | the flat roof and the vegetated rear yard. Poorly registered against the parcel layer at this scale — used for presence, not for measurement. |
| Redfin public-records mirror for 160 S Park St | corroborates 1924, single-family, 2,291 sq ft lot, last sold 15 Feb 2002 for $600,000. No photography. |
| saitowitz.com/164-south-park; openpermitdata.com/sf/address/164-south-park | the neighbour at 164, so its hoarding is not modelled as part of this building. |

**Negative results.** No Wikipedia or Wikidata entry, no SF Planning historic-resource
record located, no architect attributed, no listing photography, and no rooftop or oblique
aerial photograph of this building anywhere. Its entire web footprint is three
public-records mirrors and one Street View pass.

## 3. Verified dimensions and location

| | Value | Confidence |
|---|---|---|
| Design anchor (design footprint area centroid) | `-122.3948669, 37.7812686` | measured |
| **Manifest anchor** (model XY bbox centre) | **`-122.3948620, 37.7812804`** | measured; design anchor + the build's (0.428 E, 1.310 N) recentring |
| Registry / exclusion point (DataSF LiDAR footprint centroid) | `-122.3949116, 37.7812949` | measured — **deliberately different**, see REPORT.md |
| Street facade heading | **108.13°** (east-south-east) | measured, perpendicular to the parcel's front chord |
| Party lines, front block | 280.4° (south) / 284.0° (north) — the lot fans 3.6°, as radial lots do | measured |
| Party lines, rear block | 315.1°, parallel | measured |
| Front → rear axis | 299.3° | measured |
| Frontage | 6.17 m chord (arc bulge 0.14 m, below the bevel radius) | measured |
| Rear wall | 6.08 m | measured |
| Built depth | 28.1 m on the south party line, 24.9 m on the north | derived — see §4 |
| Built footprint | **166.4 m²** of a 216.8 m² lot | derived |
| Roof deck | **8.81 m** | measured (LiDAR height **mode**) |
| Tile-eave ridge / target height | **9.40 m** | measured (LiDAR height max) |

## 4. The two derivations, and why they were needed

**The DataSF LiDAR polygon for this lot is the LOT, not the roof.** It is 220.0 m² against
a 216.8 m² parcel, and its outline is the parcel's outline simplified. Nothing in the
record says so. The tell is in the statistics: `hgt_min` is 0.56 m and σ is 2.56 m, where
all five block neighbours run 0.75–1.14 m. Something inside that polygon is at ground
level, and the 2002 permit — "new fence at rear yard to replace (e) fence & gate" — names
it.

Two consequences:

1. **The roof height is the mode, not the median.** `hgt_median` 7.79 m is a roof-and-yard
   blend that describes no surface on the building. `hgt_majority` — 8.81 m — is the roof
   deck, and `hgt_max` 9.41 m is the crest. Building to 7.79 m would have produced a
   one-and-a-half storey house.
2. **The built depth had to be reconstructed.** Two independent routes agree:
   *floor area* — 3,674 sq ft over two storeys is 170.7 m² per floor; *LiDAR mixture* —
   with the roof at 8.81 m and the yard at ~0.4 m, a mean of 6.66 m over 882 cells implies
   a built fraction of 0.74–0.76, i.e. 164–168 m². The design footprint is the parcel
   truncated to **166.4 m²**, which reproduces the Planning floor area to within 2.5% and
   leaves a ~50 m² rear yard.

## 5. Observations, side by side

**East-south-east — the street elevation, and the only side the public ever sees.**
Two storeys, uniformly dark slate. *Upper:* three openings in a panel field between two
flat end pilasters — a round-arched multi-pane window ≈1.95 m wide centred, its
semicircular head ringed by a moulded archivolt standing ~60–80 mm proud, flanked by two
rectangular multi-pane windows in plain flat surrounds (the southern slightly wider than
the northern). Pane counts read as ≈6 × 6 for the arch's rectangular portion and 4 × 5 /
3 × 5 for the flanking pair — **inferred from one capture**. *Cornice:* a plain moulded
band the full width, and above it the **red barrel-tile pent**, projecting over the
sidewalk and sloping down toward the park. *Ground:* a recessed dark shopfront under a
proud lintel band carrying two square tie-plates — a narrow pier, a wide storefront window,
a slim pier, then a flush warm-wood-veneer door with a plain transom panel above it.
Surface conduit, a downpipe and a camera are present and are not modelled.

**North-east and south-west — the party flanks.** Blind. The north-east abuts 156's
warehouse, the south-west abuts 164. Neither is visible from the app's camera at any useful
angle; built as flat planes carrying only the base course and the string course.

**West-north-west — the rear.** Faces the ~50 m² rear yard, visible only from directly
above. The 2004 permit replaced its windows and doors with steel and the 2005 permit
changed its finish from stucco to lap siding, so it is plainer and more utilitarian than
the front. Modelled as one door and two plain windows. **Unverified.**

**Top.** A flat roof at 8.81 m running the full 26.5 m, with the tile eave lifting to
9.40 m at the street end only, a low parapet lip elsewhere, and one square stack near the
north party wall at the street end. The tile band is the single most valuable thing in the
asset from the air: it is warm, it is 6 m wide, and no neighbour on this rim has one.

## 6. Recognition cues, ranked

1. **The arched window** — the only arch on this side of the oval, dead centre on a 6.17 m
   facade, where everything else is a rectangle.
2. **The red barrel-tile eave** — the one warm colour, the one non-flat plane, and the only
   cue that survives at thumbnail size from directly overhead.
3. **The monochrome slate facade**, with relief instead of colour.
4. **The proportion** — 6.17 m of frontage against 26.5 m of depth, bending 33° partway back.
5. **The warm-wood door**, the single warm accent at street level.

## 7. Preserved / simplified

**Preserved:** the frontage and rear widths, the built depth, the 315.1° rear axis and the
108.13° facade heading exactly; a true semicircular arch head; the tile eave as a genuinely
projecting, genuinely sloping plane and the flat roof behind it; the tripartite upper
rhythm (small — big-and-arched — small); the single warm door.

**Simplified / exaggerated:** the arch's real ≈6 × 6 glazing becomes three verticals
clipped by the arc and three horizontals, because a 36-pane grid is grey mush at 40 px and
the grid has to read as a *grid*; the archivolt's relief is roughly doubled; the tile's
projection is exaggerated to 0.46 m so it casts a real shadow line; individual tiles become
one flat colour; the flanking windows become plain recessed rectangles with a cross of
muntins each; conduit, meters, downpipes, cameras and decals all disappear; the rear yard
is not modelled at all — the asset stops at the rear wall.

## 8. Uncertainties and conflicting evidence

- **What the 9.41 m maximum is a maximum of.** It is 0.60 m above the 8.81 m mode, which is
  exactly the margin a projecting tiled eave produces — and also exactly the margin a small
  roof stack produces, and this facade appears to have both. The two readings give the same
  target height, which is why 9.40 m was adopted, but they imply different geometry. The
  model resolves it in favour of the tile and caps the stack at 9.30 m; see REPORT.md.
- **The rear wall's position** is a reconciliation of a floor-area record with a LiDAR
  height mixture, not a survey. It is also the part of the model no camera in the app
  ever sees.
- **Every facade number** comes from one Street View pass partly obscured by a street tree:
  pane counts, the archivolt's relief, the tile's projection, the shopfront's division and
  the stack are readings, not measurements.
- **The assessor and SF Planning disagree about what this building is** — `SRES` with a
  Homeowners exemption against 3,674 sq ft of MIPS office and zero residential floor area.
  Both records are current. The manifest takes `cat: 3` (Office) because that is what the
  street shows; it does not affect the geometry.
- **164 next door will not look like its photographs for long**, and in photographs from
  the south its maroon hoarding sits immediately beside 160. None of it belongs to this
  building; 160's south flank is a blind party wall.
