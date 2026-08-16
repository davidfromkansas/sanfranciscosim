# 102 South Park (The Park View) — reference dossier

Compiled 16 August 2026 for `artifacts/102-south-park/`. This is the *verification* pass
over `docs/asset-plans/102-south-park.md`: what was checked, against what, and what
changed. Corrections made during modelling are in `REPORT.md` §3 — REPORT beats plan.

## 1. Identity

**102 South Park St, San Francisco, CA 94107.** Built 1912–13 as the **Hotel Bo-Chow**, in
what was then the Japanese quarter of South Park; later the **Park View Hotel**; today
**The Park View**, a 40-room single-room-occupancy building owned by Mission Housing
Development Corporation, with **Caffe Centro** in the ground-floor commercial space.

Rehabilitated 2019–2022 as one third of the 108-unit *South Park Scattered Sites* project
(Park View 40 units + Hotel Madrid 44 + Gran Oriente Filipino 24), financed with a
$34.2 M JPMorgan Chase construction bond plus MOHCD tax credits. The rehab is where the
roof's solar array comes from.

Caffe Centro — South Park's oldest coffee shop — closed in August 2023 and reopened on
24 May 2024 as a worker-owned collective. As of July 2026 it is the only operating
restaurant on the oval.

## 2. Source links and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/124884353](https://www.openstreetmap.org/way/124884353) | the footprint polygon; `addr:housenumber=102`, `addr:street=South Park`; `building=retail` (describes the café, **not** the building — do not inherit) |
| [DataSF Building Footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni), record `SF3775057` | LiDAR height statistics: median **12.88 m**, majority 12.71 m, mean 12.58 m, σ 1.60 m, max 15.20 m, min 2.41 m; ground 9.62 m NAVD88; footprint 251.3 m² |
| [DataSF Assessor roll `wv5m-vpq2`](https://data.sfgov.org/resource/wv5m-vpq2), block 3775 lot 057, rolls 2018–2025 | address; **4 storeys**; "Residential Hotel & SRO" / "Commercial Hotel"; **built 1912**; lot 2,583.75 sq ft (240.0 m²); building 10,350 sq ft |
| [Alamy J7M52Y](https://www.alamy.com/stock-photo-caffe-centro-formerly-the-park-view-and-bo-chow-hotels-built-1913-142428579.html) (photo located at 102 South Park St, 23 May 2017) | "Built as the Hotel Bo-Chow in **1913** in the Japanese community of South Park … Later the Park View Hotel" |
| [missionhousing.org/parkview](https://www.missionhousing.org/parkview) | 40 units plus one commercial space; SRO programme; Hyder Property Management |
| [missionhousing.org/granoriente](https://www.missionhousing.org/granoriente) | the attached SW neighbour at 106 South Park, built 1907, 24 units |
| [Bisnow](https://www.bisnow.com/san-francisco/news/affordable-housing/mission-housing-locks-in-funding-for-soma-redevelopments-106048), [ConnectCRE](https://www.connectcre.com/stories/chase-provides-funding-for-rehab-of-three-historic-sros-in-san-francisco/) | the three-hotel 108-unit deal, its financing and its 2018–2020 timeline |
| [SCCS Group project page](https://www.sccsgroupllc.com/projects/south-park-scattered-sites) | Type V wood frame; ground-floor restaurant tenancy; "preserved historic integrity" |
| [Calisphere / SFPL](https://calisphere.org/item/f5f8b90a1a0a9f8bbe6e5220afc76544/) | catalogue record "Park View Hotel, 102 South Park", 24 January 1955 — **the image itself was not examined** |
| [Mission Local, Jul 2026](https://missionlocal.org/2026/07/south-park-offices-overshadow-the-only-operating-restaurant/), [The Dissent SF, Jul 2026](https://thedissentsf.com/article/the-last-table-at-south-park) | current context: three SROs on the block, Caffe Centro worker-owned since 2024 |
| Google Street View, South Park pano, **capture January 2025**, viewed at two zoom levels | the entire front-elevation description in §5 |
| Google Maps satellite, **2026 Vexcel imagery** | the roof description in §5; its "The Park View" / "Caffe Centro SP" / "Gran Oriente Filipino Hotel" labels are what confirm which roof is which address |

**What does not exist.** Six Exa searches were run across architecture press, planning
records and historic surveys (`102 South Park San Francisco building Caffe Centro`;
`102 South Park Street San Francisco SRO residential hotel 1912`; `Park View Hotel 102
South Park San Francisco Mission Housing SRO rehabilitation historic`; `Mission Housing
South Park Community three SRO hotels rehab Park View Madrid Gran Oriente`; `Hotel Bo-Chow
1913 South Park San Francisco Japanese community history`; `South Park San Francisco
historic resource survey 102 South Park brick facade`). **No architectural description, no
DPR 523 form, no Article 10/11 designation and no elevation drawing was found.** Everything
in §5 below the assessor row is read off photographs. That is the honest state of the
evidence and it is why three of the four elevations are marked *inferred*.

## 3. Verified dimensions and location

| Item | Value | How |
|---|---|---|
| Anchor (WGS84) | **-122.3943678, 37.7817707** | footprint OBB centre; the polygon's area centroid is 0.18 m away, so either would do |
| Footprint | **7.78 m** frontage × **29.76 m** deep, 217.8 m², OBB fill 93.7 % | OSM way/124884353 reprojected through the app's tangent projection |
| Cross-check | DataSF `SF3775057` = 251.3 m², 84 % of it overlapping the OSM polygon; assessor lot 240.0 m² | grid-sampled overlap, 0.25 m step |
| Storeys | 4 | assessor + photograph |
| Roof deck | **12.90 m** | DataSF LiDAR median. σ is only 1.60 m and the majority value is 12.71 m, so the deck is well determined |
| Cornice crest | **14.00 m** — *estimated* ±0.6 m | 12.90 m deck + a cornice/parapet read off the Jan 2025 pano |
| Front heading | outward normal **135.4°** (SE, onto the park) | measured from the footprint |
| NE flank | outward normal 45.0°, 29.76 m | measured |
| Rear | outward normal 315.4°, 7.78 m | measured; two collinear OSM segments merged |
| SW party wall | outward normal 225.0°, ~29.4 m net, **three light-well notches** 2.32 × 2.54 m, 0.79 × 3.44 m and 2.09 × 2.35 m | measured |

Ground elevation is 9.62 m NAVD88; the app's terrain handles that, not the asset.

## 4. Orientation

The building sits on the **north rim** of the South Park oval near its west end. Narrow
front on the park (southeast), long plan running back toward Bryant Street. The Gran
Oriente Filipino (106 South Park, ~11 m) is **attached** on the southwest; the northeast
flank faces open ground toward Jack London Alley and is genuinely exposed. Like the whole
SoMa grid the lot is rotated ~45° from the world axes.

The asset is authored in true-world orientation (`+Y` = north, `+X` = east) because
`placeGeneric()` never rotates. The contract's "front faces −Y" rule therefore cannot be
honoured literally — see `REPORT.md` §2.

## 5. What each side shows

**Southeast (South Park front)** — *observed*, Google Street View January 2025, the only
well-photographed elevation. Warm greige stucco, four registers:

- **Ground**: the Caffe Centro storefront — dark shopfront joinery over a panelled
  bulkhead, a large fixed window, a recessed café door, a wall-mounted menu case, and a
  **projecting dark-green awning** with the café's name on the valance. A separate narrow
  entrance at the northeast end serves the 40 rooms above. A plain pale beltcourse caps the
  whole ground floor.
- **Second and third floors**: three **round-arched windows** each, on identical bay
  centres. Semicircular fanlight over a double-hung sash, **dusty blue-gray architrave**,
  projecting **keystone** at the crown, small impost blocks at the springing, projecting
  sill. A shallow blue-gray band runs under the third-floor sills.
- **Fourth floor**: three **plain rectangular** double-hung windows on the same centres,
  same blue-gray flat surrounds and sills, no arches. The register change is real and is
  one of the building's better cues.
- **Cornice**: a heavy projecting pale cornice with a regular row of small brackets or
  dentils beneath it, and a flat parapet cap above. No signage above the storefront.

Two colours, plus the green awning. That is the whole palette of the building.

**Northeast flank (Jack London Alley side)** — *inferred*. 29.76 m facing open paved
ground; genuinely visible in the real world and unavoidably visible to the app's camera.
No usable ground-level photography found. Modelled as the same greige stucco with a regular
eight-bay rhythm of plain rectangular SRO windows on the three upper floors, and a blind
ground floor.

**Southwest flank** — *inferred*. Attached to 106 South Park for its whole length, with the
three light wells of §3 between the two buildings. The top ~3 m stands above the neighbour
and is visible. Modelled blank; the light wells are the only articulation.

**Northwest (rear)** — *inferred*. 7.78 m facing the interior of the block. No photography
found. Modelled as a service elevation: one door and two small openings per upper floor.

**Top** — *observed*, 2026 Vexcel satellite imagery. Bright membrane roof carrying **large
arrays of dark solar panels in regular rows**, from the 2019–2022 rehab; mechanical units
and a stair bulkhead toward the middle and rear; the light wells visible as slots along the
southwest edge; the park end of the roof comparatively clear.

## 6. Recognition cues (ranked)

1. **Three round-arched blue-gray windows per floor on a greige wall**, twice over — the
   only period facade on the oval
2. The **7.78 m frontage on a 29.76 m depth**: four storeys on a 25-foot lot
3. The **pale bracketed cornice** over a facade with no other ornament
4. The **register change at the fourth floor** — arches below, plain rectangles above
5. The **green café awning** at the base, the one saturated thing on the building
6. The **white roof striped with dark solar panels**

## 7. Preserve / simplify

**Preserved:** the narrow-front proportion and the real 45° heading; three bays; the
arch-to-rectangle register change; the two-colour scheme; the cornice as a front-elevation
event with a plain parapet elsewhere; the light-well slots; the solar array.

**Simplified:** fanlight muntins dropped (sub-pixel), arches drawn at 7 segments with a
0.22 m frame; impost blocks and under-sill band merged into one projecting sill; cornice
brackets replaced by a two-step cornice profile; storefront reduced to one window, two
doors and one awning; flank openings regularised to eight bays; roof clutter reduced to two
solar rows, one bulkhead and two vents.

**Exaggerated (style bible §9):** front windows widened from ~1.25 m observed to 1.40 m;
flank windows enlarged to 1.30 × 1.50 m; the awning made deeper and thicker than reality
and given a saturated green, because it is the only saturated element on a facade 7.78 m
wide.

## 8. Uncertainties and conflicting evidence

1. **1912 vs 1913.** Assessor vs the Alamy caption. Does not affect the model.
2. **The Bo-Chow / Japanese-quarter attribution rests on a single stock-photo caption.**
   Plausible — South Park was a Japanese neighbourhood before 1942 — but uncorroborated. It
   is not used in the manifest `name`.
3. **The 15.20 m LiDAR maximum is not used as the crest.** See `REPORT.md` §3.2.
4. **Three of the four elevations are inferred.** Only the front has usable photography.
5. **The light wells may be a ground-floor condition only.** They are traced from a plan
   outline. If they do not run full height the roof loses its slots; nothing else changes.
6. **No historic-resource survey was found.** If one exists it would settle the facade
   description completely, and it remains the highest-value source still missing.
