# 135 South Park — reference dossier

Research behind `135-south-park.glb`. Compiled 12 August 2026.
Plan: [`docs/asset-plans/135-south-park.md`](../../docs/asset-plans/135-south-park.md).

**Read this first.** This dossier is deliberately asymmetric, and the asset was built
knowing it. The building's *position, footprint, orientation and height* are measured
from primary survey data and are trustworthy. Its *facade* is a typological
reconstruction: **no photograph of 135 South Park's street elevation was located during
this work.** §7 lists exactly what that means for the model. Nothing in §4's north-west
paragraph should be cited as fact by anyone who reads this later.

---

## 1. Sources, and what each one establishes

| Source | Establishes | Confidence |
|---|---|---|
| [OSM way/113545684](https://www.openstreetmap.org/way/113545684) | the 10-vertex footprint polygon, the address `135 South Park`. Carries **no** `height` and **no** `building:levels`. | measured |
| DataSF Building Footprints `ynuv-fyni`, record `mblr = SF3775033` | LiDAR roof statistics: deck mode 7.06 m, median 6.95 m, **max 8.52 m**; ground 8.77 m NAVD88; an independent footprint whose centroid agrees with OSM's to 0.6 m | measured (2010 survey) |
| DataSF Assessor rolls `wv5m-vpq2`, block 3775 lot 033 | built **1925**, **2 storeys**, use class **Industrial** — identical in all 19 annual rows 2007–2025 | high |
| DataSF Building Permits `i98e-djp9`, block 3775 lot 033 | 1986 interior partitions (2 existing storeys); **1990 parapet strengthening**; 1999 reroofing | high |
| Esri World Imagery (`World_Imagery` z20, tiles 167788–167790 / 405272–405274), ~0.12 m/px | the roof: dark membrane deck, a raised lighter linear element along the deep wing, a round cowl, a rear mechanical cluster, the parapet ring, the open rear yard, the tan courtyard beyond | measured position, *inferred* interpretation |
| LoopNet listing, 135 South Park (APN 3775-033) | office use; a second-floor suite with kitchen and shower offered for lease | medium |
| Yelp business listing, Mark Horton / Architecture, 135 S Park St | current occupant is an architecture practice | medium |
| Wikimedia Commons, geotagged South Park photographs | **neighbourhood character only.** None of them shows this building. | context |
| [`docs/asset-plans/380-brannan.md`](../../docs/asset-plans/380-brannan.md) | the district's material language, 55 m away on the same block — the basis for the typological reconstruction in §4 | analogy, not evidence |

### Sources that were sought and not obtained

- **Google Street View.** South Park has coverage (a January 2025 pano sits outside 157
  South Park). Google Maps would not render in the available browser environment — the
  SPA loaded its chrome but neither the vector map nor the panorama canvas ever painted.
- **LoopNet and Yelp photo galleries.** Both returned HTTP 403 to the available fetcher.
- **mh-a.com**, the occupant's own site, which might publish photographs of its studio.
  The host serves a certificate for `*.myserverhosts.com` and the fetch aborted on the
  hostname mismatch.
- **SF Planning historic-resource survey records.** No dataset covering this parcel was
  found in the DataSF catalogue, and no Article 10/11 designation surfaced for the South
  Park oval.

Any future revision of this asset should start by getting one good photograph of the
north-west elevation. It would upgrade half this dossier in a single step.

## 2. Location, dimensions, orientation

| | |
|---|---|
| Anchor (WGS84) | `-122.3940203, 37.7811030` — the footprint polygon's **area** centroid, not its vertex mean or bbox centre |
| Block / lot (APN) | 3775 / 033 |
| Footprint area | 383.1 m² (OSM). DataSF's polygon is 432.1 m² — see §7 |
| Frontage | 19.71 m on South Park |
| Depth | 28.65 m along the north-east party wall |
| Heading | South Park front faces **315.4° true (NW)**; party wall outward 45.0°; ~45° off the world axes, like the whole SoMa grid |
| Roof deck | 7.0 m above grade |
| Parapet crest | 7.9 m (*inferred*: deck + 0.9 m) |
| **Crest / target height** | **8.5 m** — the roof monitor, matching the 8.52 m LiDAR maximum |
| Axis-aligned XY bbox | 34.45 × 25.95 m — the expected consequence of the 45° heading, not a scale error |

### The footprint, resolved

The polygon is an L. In building-local coordinates — `u` along the party wall from the
rear corner towards the front, `v` the depth into the block away from that wall:

```
 v=19.71 |  v1(28.79) ------------------- v2(14.85)         front block:
         |      |                              |            full 19.71 m width
 v=11.08 |      |                    v3(14.79)-v4(16.59)    for the front 13.9 m
  v=7.75 |      |          v6(1.535)--------------v5(16.57) --------------------
         |      |              |                            deep wing: a 7.75 m
   v=0   |  v0(28.64) -- v9(23.56) ------------ v8(0)       strip along the wall
         +---------------------------------------------->  u
            front                                rear
```

The full 19.71 m frontage runs back only **13.9 m**. Past that only the **7.75 m strip
along the party wall** continues another 14.8 m to the rear. The missing rectangle —
roughly **14.8 × 12.0 m** — is a **re-entrant rear yard**, open to the south-west (the
5.6 m gap to 147 South Park) and to the south-east (the courtyard). It is not an enclosed
light well. The 1.80 × 3.33 m jog at vertices 3–4 is a real step in the survey and is
modelled literally.

### Neighbours, measured from the anchor

| | nearest vertex | note |
|---|---|---|
| **123 South Park** (OSM way/113545683) | 10.08 m | **shares the party wall, gap 0.0 m**; OSM `height=7` |
| 147 South Park (OSM way/124889475) | 18.61 m | 5.6 m gap to our south-west flank; OSM `height=12` |
| unnamed rear building (OSM way/1311547493) | **6.18 m** | the binding constraint on the exclusion radius |
| nearest DataSF footprint (`SF3775036`) | 10.32 m | |

## 3. Recognition cues (ranked)

1. **The L footprint with its re-entrant rear yard** — measured, unusual on this row, and
   the first thing a top-down camera reads
2. **The dark roof deck** against the light-gray roofs of 123 and the buildings across the
   courtyard — a real, visible value contrast
3. **The raised glazed roof monitor** on the deep wing
4. Low two-storey brick box, flat roof, continuous parapet, 45° to the world grid
5. The unbroken north-east party wall

All of the top three are read from above. That is the correct hierarchy for this building:
at the app's aerial camera, 135 South Park is a roof.

## 4. What each side shows

**North-west (South Park front, 19.71 m).** *Unconfirmed — reconstructed.* A two-storey
brick wall under a plain parapet, a band of tall industrial upper glazing, and a ground
floor with a wide freight or garage opening beside a pedestrian entrance. This is what a
1925 building with an Industrial assessor class and an unreinforced-masonry parapet permit
looks like on this block; it is not what a photograph of this building shows, because none
was found.

**North-east (party wall, 28.65 m).** *Measured.* Shared with 123 South Park along its
entire length, gap 0.0 m. A party wall cannot carry openings. **Modelled completely
blank**, and this is the one facade decision in the asset that rests on evidence rather
than inference.

**South-west (front-block flank, then the rear yard).** 13.93 m of flank facing the 5.6 m
gap to 147 South Park; then the plan steps back and the deep wing presents its 15.04 m
flank to the open yard. Both the gap and the yard are real, so this side genuinely has
daylight — presumably why the building was cut back at all. Modelled as brick with a
modest scatter of openings, not a full grid.

**South-east (rear, 7.75 m + the 8.63 m rear wall of the front block).** Onto a tan open
courtyard with parked cars, clearly visible in the aerial. Service elevation: a roll-up
door and a few small openings.

**Top.** The surface that matters, and the one with real evidence. From the Esri aerial:

- a **mid-to-dark gray flat membrane roof**, conspicuously darker than the light-gray
  roofs either side;
- a **raised, lighter-toned linear element** running north-west/south-east along the deep
  wing — parallel to the party wall — roughly 11–13 m long and 4–5 m wide, casting its own
  shadow to the south-west. This is the tallest thing on the building and the most likely
  explanation for 8.52 m of LiDAR over a 7.06 m deck. Read as a **roof monitor /
  clerestory**: the standard daylighting device of a 1925 industrial building, and exactly
  what an architecture practice would keep. *Inferred* — see §7;
- a small **round object** (~1 m) on the north-west half of the deck, read as a vent cowl;
- a **mechanical cluster** at the rear, and a probable roof hatch;
- a continuous **parapet ring**, bright against the deck on the north-west and south-west.

## 5. Preserve / simplify

**Preserved**

- The L footprint and the rear yard as a true void, at the real 45° heading
- The monitor's position, orientation and dominance of the roof composition
- The blank party wall
- The value contrast: dark deck, bright coping ring, lighter monitor glazing

**Simplified / exaggerated**

- The monitor is the one place semantic exaggeration is spent: 1.5 m above the deck and
  clearly glazed, so it reads as a lantern from the aerial camera rather than as another
  mechanical box
- Individual bricks become flat colour
- Upper glazing reduces to 5 bays on the front, 3 on the front-block flank, 4 on the wing
- Ground-floor openings reduce to one wide opening, an entrance with a canopy, a few
  windows, and one rear roll-up door
- Roof clutter becomes one mechanical pair, one hatch, one cowl — nothing else
- Fire escapes, downpipes, window bars and signage: omitted. Nothing in the sources puts
  any of them on this building, and inventing them would add fiction, not information

## 6. Materials

| Material | Hex | Used for |
|---|---|---|
| `Toy_rust` | `a86444` | all four walls, parapet |
| `Toy_trim` | `f3efe6` | coping ring, opening frames, entrance canopy, monitor upstand |
| `Toy_glass` | `2a4d73` | windows |
| `Toy_glassl` | `6f95b8` | roof-monitor clerestory glazing |
| `Toy_roofd` | `45454a` | roof deck, monitor cap, freight and roll-up doors, roof hatch |
| `Toy_steel` | `9aa0a6` | HVAC blocks, vent cowl |
| `Toy_ink` | `3a3530` | entrance recess |
| `Toy_glassl_Glow` | `6f95b8` | the lit monitor at night — the hero glow |
| `Toy_glass_Glow` | `6f95b8` | four lit windows on the front |

Masonry is `Toy_rust` (`a86444`) rather than the palette's `Toy_brick` (`c96f4a`) — the
same swap 380 Brannan made 55 m away. `c96f4a` is saturated enough that a whole building
of it becomes an accent, and the style bible §7 reserves saturation for identity; here the
identity is the monitor. Using the browner value also makes the two assets read as one
district.

**Night state.** The monitor is the hero glow: a lit lantern on a dark roof, which is
legible from the app's aerial camera in a way an 8.5 m brick box never is. Four of the five
front bays light; the fifth stays dark so the row does not read as a switchboard. Nothing
else glows. Every glow surface is a thin shell proud of the opaque glazing behind it —
the app draws `_Glow` in a separate layer at ~12% alpha by day, so a primary surface must
never be authored as glow.

## 7. Uncertainties and conflicting evidence

- **The facade is unverified. This is the dominant risk in this asset.** See §1's
  "sought and not obtained". Everything in §4's north-west paragraph, the bay counts, and
  the choice of raw brick over a painted front are typological reasoning from the 1925
  date, the Industrial class, the masonry parapet permit and 380 Brannan's material
  language. They are *plausible*, not *established*. AGENTS rule 5 makes massing accuracy
  non-negotiable; it does not license presenting an inferred facade as researched, so it
  is flagged here, in `REPORT.md`, and in the plan's 2.15.

- **Is 8.52 m a roof monitor or just the parapet?** A 7.06 m deck plus a 0.9–1.1 m parapet
  lands at 7.9–8.2 m; 8.52 m is only 0.3 m above that, so the LiDAR maximum alone cannot
  separate the two readings. The aerial decides it in favour of a raised element — a
  distinct lighter plane with its own shadow, far wider than a parapet line — but at
  0.12 m/px that is *inferred*, and whether it is **glazed** or **solid** is not resolved
  at all. It does not change the target height either way (8.5 m is the crest regardless).
  It changes the design completely: the glazed reading is this asset's identity cue and
  its entire night state.

- **Storey count conflict, resolved.** The 1990 parapet permit records 1 existing storey;
  the 1986 permit and all 19 assessor rolls record 2, and a 7.0 m deck is two ~3.4 m
  industrial floors. The 1990 figure is almost certainly clerical — a parapet permit has
  no reason to survey the building. **Built as 2 storeys.**

- **DataSF and OSM disagree about the rear boundary.** DataSF's polygon (432.1 m²) extends
  ~7 m further south-east than OSM's (383.1 m²), into what the aerial shows as open
  courtyard. The centroids agree to 0.6 m, so this is not a registration error — DataSF's
  2010 trace includes something (a canopy, a shed, a since-removed rear structure) that
  OSM's later trace does not. **The OSM footprint is modelled**: it matches the aerial, and
  the LiDAR's 1.05 m *minimum* height over the DataSF polygon is consistent with low
  structure or open ground in exactly that overshoot — which also explains why the LiDAR
  mean (6.04 m) sits well below its median (6.95 m).

- **The rear yard is measured in plan but not in section.** Whether the notch is open to
  the ground, a first-floor setback with the upper storey oversailing, or a roofed
  single-storey infill is unresolved. Modelled as a full-height void: right at the roof
  (which is what the camera sees) and defensible at ground level.

- **The exclusion radius has almost no margin** — 4.68 m of our own DataSF ring below,
  6.18 m of the nearest OSM neighbour above. See the plan's 2.13; it must be verified
  against the actual re-bake, not assumed.

- No architect is recorded for the 1925 building in any source consulted, and the building
  carries no name.
