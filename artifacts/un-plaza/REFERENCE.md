# United Nations Plaza — reference dossier

Research behind `un-plaza.glb`. Everything below was gathered or re-derived for
this build; where it corrects `docs/asset-plans/un-plaza.md`, the correction is
called out and repeated in REPORT.md. **REPORT beats plan, always.**

## 1. What this is, and what it is not

United Nations Plaza is Lawrence Halprin's 1975 gateway to the Civic Center: a
2.78-acre wedge of red brick driven diagonally out of Market Street, up the
closed Fulton Street alignment, toward City Hall. It commemorates the signing of
the UN Charter in San Francisco in 1945 and was built with the Market Street
Reconstruction Project over the new BART/Muni subway.

**It is not Civic Center Plaza.** The building brief for this asset read
"UN Plaza, 355 McAllister St". 355 McAllister is Civic Center Plaza — DataSF
address point `288381-501940-325286` on parcel `0788001`, whose centroid
(−122.41760, 37.77948) is the anchor of the already-integrated
`civic-center-plaza` landmark. United Nations Plaza is 340 m east, has no
McAllister frontage, and is OSM relation `1735771` / Wikidata `Q1311705`. This
asset models United Nations Plaza.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM relation `1735771`, outer way `24588033`, 5 inner rings | the plaza polygon (39 vertices), the fountain, three planting beds, the south terrace with its retaining walls and steps, the dog run |
| OSM nodes `13481539165`–`13481539180` | the sixteen light standards, positions only |
| OSM ways/nodes `1470003860`, `411095145`, `6541967407`, `5318059432`, `7797674773`, `11670188816`, `9225712936`, `128534082` | UN emblem, Simón Bolívar, obelisk, the two flagpoles, fitness station, Pit Stop, dog run |
| DataSF street centrelines `3psu-pn9h` | **both grid bearings.** McAllister reads 260.96/80.96 over seven consecutive blocks; Market (Hyde→Larkin, 192.3 m — the block that fronts the plaza) reads 225.20/45.20 |
| DataSF LiDAR footprints `ynuv-fyni` | the **nine granite fountain slabs**, positions and heights; the Federal Building's 38.40 m |
| DataSF `ramy-di5m` + `acdm-wktn` | that 355 McAllister is Civic Center Plaza |
| Wikipedia, *United Nations Plaza (San Francisco)* | 1975 construction, the design team, 117,000 ft² of herringbone brick, 192 trees in 1975, the 16 light standards, the 1995 Walk of Great Ideas and the 17 ft obelisk, the coordinates cross, the fountain's 673 blocks / 165 ft / 100 ft basin, the removal history |
| The Cultural Landscape Foundation | the Halprin/Ciampi/Warnecke joint venture, the inscribed columns, the Bolívar gift, the 1995 and 2005 rehabilitations |
| SF Arts Commission accession `1975.29` | the fountain as accessioned civic art, 165 ft, granite |
| sf.gov, SF Rec & Park, KQED, SFist, SF Chronicle, SF Examiner, NYT (May 2025) | the $2 M 2023 revitalization (Verde Design, reopened 8 Nov 2023), the 13,000 ft² skate plaza, the Feb 2025 2,100 ft² expansion with three Alexis Sablone art pieces, the fitness station, game tables, café seating, festoon lighting and dog run |
| SF Chronicle, Jan and Apr 2026 | the **Vaillancourt Fountain** removal at Embarcadero Plaza — recorded here only to rule it out. It is a different fountain at a different plaza. The UN Plaza fountain still stands. |
| Google z20 satellite imagery; a levelled Google photosphere at the Hyde end (`CIABIhBTIDVFCMu9Ia0rkJLR_mRK`) | the ground-plane layout, and photogrammetric heights for the light standards and Bolívar |
| `app/public/tiles/buildings/20_13.bin` | the exclusion measurements (REPORT.md §6) |

## 3. Verified dimensions and location

| | |
|---|---|
| Anchor (world-axis-aligned XY bbox centre) | **−122.4138900, 37.7801415** |
| Plaza-frame extent | 220.81 m along Fulton × 150.33 m across |
| World XY bbox | 215.22 × 157.94 m |
| Polygon area | 11,264 m² = 2.78 acres (published: 2.5 TCLF / 2.6 Wikipedia) |
| Fulton axis | 80.94° / 260.94° true |
| Market frontage | 45.20° true |
| Fountain crest | 4.03 m above plaza grade (DataSF LiDAR `159394`) |
| Light standards | 5.90 m to the globe top (photogrammetric, ±0.5) |
| Obelisk | 5.18 m (17 ft, published) |
| Simón Bolívar | 8.10 m overall (photogrammetric) |
| Tallest tree crown | 13.00 m — **authored**, and the model's height datum |

## 4. Orientation

The plaza sits on **two** grids and the model is authored on both:

- Its own axis is the Civic Center grid, **80.94° east / 350.94° north**, the
  same frame `civic-center-plaza`, `sf-main-library` and `city-hall` use.
- Its south-east boundary is **Market Street at 45.20°**.
- The 35.74° between them is the plan shape and the plaza's whole identity.

**Correction to the OSM ring.** A least-squares fit over the ring's own long
edges gives 80.42°, half a degree off the street grid — 1.9 m of error at the
plaza's east end. DataSF's centrelines are authoritative and the model is built
on 80.94. The Market edge is the opposite case: the ring's own 134.6 m Market
segment reads 45.18° against DataSF's 45.20°, so that boundary is trusted as
drawn and is used verbatim.

## 5. Observations from each side and above

- **South-east (Market).** The front door. A 134.6 m diagonal frontage, the
  BART/Muni portal heads and elevator, the coordinates cross in the paving, and
  the stepped terrace rising away from the street.
- **South-west (Hyde).** The ceremonial end. Bolívar closes the axis; the two
  westernmost columns flank him; the Walk of Great Ideas runs underfoot.
- **North (50 UN Plaza).** A 110 m straight edge against the 1936 Federal
  Building's flank — a walk, the north planting bed, the north column row.
  Nothing of the Federal Building is in this asset.
- **East / north-east (Leavenworth, 7th at Market).** The fountain, the Pit
  Stop, the bike dock, four mapped trees, and the planted Leavenworth arm.
- **Above.** A red wedge, two dark-green bed bars, sixteen white globes in two
  ranks, a pale granite band with the UN emblem on it, a pale skate pad, and a
  dark octagonal basin holding a pale granite pile.

## 6. Recognition cues, ranked

1. **The red brick field.** A colour cue, and the only one that works at any
   distance — this is the only large red plaza in San Francisco.
2. **The double colonnade of sixteen globe-topped columns.**
3. **The wedge**, cut at 35.74° against its own grid by Market Street.
4. **The sunken granite fountain** — a pale blocky pile in a dark well.
5. **The pale granite inlays**: the Walk of Great Ideas and the UN emblem.
6. **Bolívar** closing the west end.

## 7. Preserved, simplified, omitted

**Preserved:** the plaza polygon exactly; the sixteen standard positions with
their survey jitter; the nine surveyed fountain slabs at their surveyed heights;
the three bed outlines; the terrace's step and wall lines; the dog run; the UN
emblem's position and size.

**Simplified:** 673 fountain blocks → nine measured masses, each stepped once;
an equestrian bronze → one chunky verdigris mass on a pale pedestal; herringbone
brick → a two-tone joint grid on the colonnade's own 11.77 m bay pitch;
inscribed nation names → one recessed band per shaft; flags → flat slabs with no
devices (style bible §26, and the only defensible call for a plaza whose flags
are themselves contested).

**Omitted:** the farmers-market stalls (they left for Fulton Plaza in 2023 and
would date the model); food trucks and event tents; individual hydrants, sign
poles and cabinets; the BART/Muni station box below; every surrounding building.

## 8. Uncertainties and conflicting evidence

1. **The available aerial imagery predates the November 2023 renovation.** Both
   Google's and Esri's z20 imagery of this block show the pre-2023 plaza. OSM's
   *tags* are current but its *geometry* for the skate area is the old planting
   bed (396 m², against a published 13,000 + 2,100 ft² = 1,404 m²). The 1975
   bones are measured and safe; the 2023–25 layer is placed from news
   photography and the OSM `leisure=pitch` node at (10.4, −21.9), and is the
   least certain part of this asset.
2. **The height datum is authored, not surveyed.** No element of this plaza has
   a published height. See REPORT.md §3 for why that is safe here.
3. **The light standards' 5.90 m is photogrammetric, ±0.5 m.**
4. **Acreage disagrees** across sources (2.5 / 2.6 published, 2.78 measured).
   The model is built on the OSM polygon because that is the polygon the
   pipeline's landcover and exclusion already use.
5. **Tree positions are inferred, not surveyed** — the plaza's trees are not in
   OSM (only four, at the 7th-and-Market corner). See REPORT.md §4.
