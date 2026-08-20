# 131 Steuart Street (Steuart Place) — reference dossier

Compiled 18 August 2026 for `artifacts/131-steuart/`. Plan of record:
`docs/asset-plans/131-steuart.md`. **This file beats the plan wherever they
disagree**; every correction made during the build is flagged below.

## 1. What the building is

Steuart Place, 131 Steuart Street, San Francisco CA 94105. A 1907 red-brick
commercial block on the Steuart Street waterfront row, four doors southeast of
the Audiffred Building, renovated in 1983 and owned since November 2000 by the
131 Steuart Street Foundation / Jewish Community Federation, which runs it as a
below-market nonprofit office hub. Class B office, Assessor use code COMO,
welfare exemption.

It occupies the **131 half of parcel 3715-025**, which the Assessor records as
"131–141 Steuart St". 141 Steuart is a separate two-storey classical block with
a curved glass addition on the same parcel; it is **not** part of this asset.

The lot is a **through-lot**: 14.16 m of Steuart Street frontage carrying 42.07 m
of depth all the way to The Embarcadero, blind on both long flanks. It therefore
has two public ends and they do not look alike — the Steuart end is the 1907
brick building, the Embarcadero end is the 1983 re-clad.

## 2. Sources, and what each established

| Source | Established |
|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3715025` | address range 131–141, C-3-O zoning, parcel centroid |
| DataSF Assessor roll `wv5m-vpq2`, block 3715 lot 025 | built 1907, **7 stories**, COMO office, welfare exemption, lot 12,603 sq ft, sold 2000-11-02 |
| DataSF Building Footprints `ynuv-fyni`, `mblr=SF3715025` | LiDAR: `hgt_max` 27.77 m, `hgt_majority` 24.99, `hgt_median` 23.07, `hgt_mean` 22.69, `hgt_std` 3.70, 2,461 cells, ground 3.52 m |
| DataSF Addresses `ramy-di5m` | suites through `#700`; the 115 / 121 / 131 / 133 / 139 / 141 / 155 sequence |
| DataSF Street Centrelines `3psu-pn9h` | which face is Steuart and which is The Embarcadero |
| OSM way 193054132 (+ 193054135 / 193054137 / 193054133 / 256969674 / 193054136) | footprint geometry for this building and its neighbours |
| Transwestern, "Steuart Place" | 1907, renovated 1983, 7 stories, class B |
| CompStak property 2765 | APN 3715-025, 68,400 sq ft, tenants; **claims 6 stories — wrong, see §6** |
| SKYDB 137152324 | 7 floors, low-rise, commercial office |
| j. weekly, 6 Oct 2000, "JCF proceeds with plan to buy 2 next-door buildings" | the JCF bought 131 **and** 141 as two adjacent buildings; ground-floor restaurants |
| Google Street View — Steuart St, panoids `bGhpWtWQe6cDHkmec2tCsA` (2022), `0F4-09tgUjGg6sPgyJ31Gg` (2013), `CmtflDlV1RNYt6bOrZhq-Q`, `44TDz4Q3xLN7ddQOI0pCsw` | the 1907 elevation, bay count, storefront, cornice and string course, and the photogrammetric height solve |
| Google Street View — The Embarcadero, panoid `bItenxt1tDuMrvL05opHTQ` (2025) | the 1983 elevation, the set-back barrel-roofed penthouse, the ground-floor restaurant |
| Google satellite tiles z21/z22 | flat roof, roof plant, the light-monitor spine; disproves OSM's `roof:shape=gabled` |

## 3. Measured geometry

Local tangent projection (`AGENTS.md`): `x=(lon+122.4375)·111320·cos(37.77)`,
`z=−(lat−37.77)·110540`.

Footprint (OSM way 193054132), a near-perfect parallelogram:

| Corner | lon, lat | Meaning |
|---|---|---|
| P0 | −122.3926647, 37.7929668 | Steuart frontage, 121 Steuart side |
| P1 | −122.3925508, 37.7928763 | Steuart frontage, 141 Steuart side |
| P2 | −122.3922125, 37.7931452 | Embarcadero frontage, 141 side |
| P3 | −122.3923291, 37.7932374 | Embarcadero frontage, 121 side |

- **14.16 m × 42.07 m**, 601.8 m² (OSM). Minimum-area OBB 14.462 × 42.068 m.
- DataSF LiDAR ring 611 m², 92 % overlap with the OSM ring — same building.
- **Anchor (model origin) `-122.3924386, 37.7930568`** = the footprint AABB
  centre. *Correction to the plan, which quoted the polygon centroid
  `-122.3924393, 37.7930564`; the two differ by 7.6 cm and the AABB centre is
  what makes the exported XY offset exactly zero.*

Edge normals, true bearings:

| Edge | Length | Normal | What it is |
|---|---|---|---|
| P0→P1 | 14.16 m | **224.9°** | Steuart Street front |
| P1→P2 | 42.07 m | 135.0° | party wall, 141 Steuart |
| P2→P3 | 14.46 m | **44.8°** | The Embarcadero front |
| P3→P0 | 42.03 m | 314.6° | party wall, 121 Steuart |

Method validated first against the shipped `500Third` anchor, which reproduced
`build_500_third.py`'s documented `E_THIRD` 44.9°, `E_RITCH` 225.0° and
`E_BRYANT` 314.0° to within 0.2°.

## 4. Measured heights

| Element | Height | How |
|---|---|---|
| Ground-floor cornice / green band | **5.2 m** | photogrammetry, both ends agree (5.2 / 5.0) |
| Window rows (6) | 5.55, 7.90, 10.25, 12.60, 14.95, 18.25 m | photogrammetry, Steuart elevation |
| Green string course | **17.4–17.6 m** | photogrammetry |
| Brick cornice, top | **21.8 m** | photogrammetry, Steuart pano (Embarcadero pano gives 21.6 m for the same parapet) |
| Roof deck | 21.4 m | derived |
| Penthouse walls / glazing head | 24.7 m | photogrammetry, Embarcadero pano (21.94–24.52 m) |
| **Penthouse barrel crown** | **27.7 m** | photogrammetry 27.5 m; DataSF LiDAR `hgt_max` **27.77 m** |

**How the heights were solved, and why the first attempt was wrong.** Two traps:

1. The 2013-era panorama `0F4-09tgUjGg6sPgyJ31Gg` stitches to a **3584 × 1664**
   equirect, not 4096 × 2048 — 0.1004°/px with the horizon at row 832. Assuming
   the modern geometry made every height read ~10 % low.
2. The panoramas' reported lat/lon are not reliable enough for a 15 m baseline.
   The camera was instead solved by least squares against four **known party-line
   corners** along the street wall (111/121, 121/131, 131/141, 141/155): RMS
   **0.9 px** (0.08°), perpendicular distance **15.00 m**. A sensitivity sweep
   proves the solve is not degenerate despite the targets being collinear —
   forcing D to 15.5 m raises the RMS to 9.3 px and 16.0 m to 18.1 px, so D is
   good to ±0.4 m.

The Embarcadero pano was solved the same way (D 14.99 m) and independently put
the same parapet at 21.6 m and the crown at 27.5 m.

**Why the LiDAR maximum is real here.** `hgt_std` is **3.70 m** over 2,461
cells — far too wide for one flat plane with an outlier, so by the `164-south-park`
sd test the footprint is genuinely two-level and the maximum must not be
discarded. Solving the two-level model against the measured 21.4 m roof deck puts
roughly a quarter of the plan area on the upper level, which is exactly the
penthouse footprint read off the Embarcadero elevation. Three independent
sources agree to 0.3 m.

## 5. What each side shows

- **Southwest, Steuart Street (14.16 m).** Red brick, **five bays**, six storeys
  of punched windows over a tall dark-green painted metal storefront with a
  recessed entry and gold "131 / STEUART PLACE" lettering. Green string course
  under the top floor; projecting dark-green sheet-metal cornice topping at
  21.8 m. The penthouse is set back 32 m and is **not** visible from the street.
- **Northeast, The Embarcadero (14.46 m).** Pale cast stone with rounded
  corners, five continuous horizontal steel-sash glazing bands, a white-painted
  ground floor of restaurant shopfront glass with a parklet, and above the
  parapet the set-back glazed penthouse under a shallow cream barrel roof.
- **Southeast, party wall with 141 Steuart (42.07 m).** Blind brick. 141 only
  reaches ~21.8 m, so this flank is genuinely exposed above about 18 m and the
  penthouse is exposed outright.
- **Northwest, party wall with 121 Steuart (42.03 m).** Blind brick, hidden to
  ~29 m by 121 Steuart; only the penthouse's northwest face is seen.
- **Top.** Flat membrane at 21.4 m behind the cornice ring, a light-monitor spine
  down the middle, a stair head, clustered plant, one skylight, and the barrel
  penthouse over the northeast quarter.

## 6. Corrections and conflicts resolved

1. **Storey count.** CompStak says 6; Transwestern, SKYDB and the Assessor say 7.
   **Seven is right**: six window rows are countable above the ground floor on
   the rectified Steuart elevation, and DataSF lists suites through `#700`.
2. **OSM `roof:shape=gabled` is wrong.** The aerial and both elevations show a
   flat roof behind a parapet with a barrel-roofed penthouse at one end. No
   gable was built. Worth fixing upstream in OSM.
3. **Anchor.** Moved 7.6 cm from the plan's polygon centroid to the footprint
   AABB centre so the export's XY offset is exactly zero (§3).
4. **Palette.** The plan proposed `Toy_slate` `6f7883` for the cornice and
   storefront joinery. That is a blue-grey; the real metalwork is a near-black
   green. Shipped with **`Toy_sash` `2f4f49`** instead (precedent
   `artifacts/21-south-park`).
5. **Every square-foot figure online (68,400 / 75,000 / 79,800) covers 131 and
   141 together.** None of them divides usefully by 7.
6. **Architect: still unknown.** Eight searches across listing sites, permit
   aggregators and the local press found nothing, and the 1983 renovation is
   likewise unattributed. The SF Planning Article 11 downtown conservation-
   district inventory is the remaining lead.

## 7. Recognition cues, in the order they survive scale

1. The pale barrel-roofed penthouse at the northeast end, 6 m proud of a cornice
   line the whole block shares — the only silhouette break for 100 m.
2. The narrow-and-deep proportion: 14 m wide, 42 m deep.
3. Dark-green cornice and dark-green ground-floor band bracketing a red brick middle.
4. Red brick at the street end, pale cast stone at the water end, one mass.
5. A five-bay window grid at a tight floor rhythm — a dense 1907 texture.

## 8. Simplified away, deliberately

Window muntins and sash divisions beyond one meeting rail; the storefront
roll-down grilles; the entry arch mouldings; the cornice modillions; the "Saigon"
and "Cartridge World" signage; the Embarcadero parklet; the rounded cast-stone
corner radii (built as bevels, not as arcs).
