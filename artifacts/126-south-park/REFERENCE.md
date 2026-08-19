# 126 South Park — reference dossier

Research behind `126-south-park.glb`. Compiled 16 August 2026 by re-verifying
`docs/asset-plans/126-south-park.md` rather than trusting it. Where this file and the
plan disagree, this file is right and `REPORT.md` records why.

**Read this first:** this dossier is the inverse of most in this set. The **street
elevation is photographed and near-certain**; the **roof and the rear are inferred**.
Section 8 says exactly which statements are which.

---

## 1. What this building is

126 South Park is a two-storey wood-frame commercial building of 1907 on the west arc
of the South Park oval in SoMa. It is a **sliver**: 6.90 m of frontage on a lot that runs
29.79 m back, with party walls down both long flanks. Its plan is pinched to **4.01 m**
at the waist by two light wells cut in from opposite sides about ten metres back from the
street — the only way daylight reaches the middle of a 30 m tube, and the feature the
leasing agent sells as "3 sides of window line, plus an atrium garden".

| | |
|---|---|
| Address | 126 South Park, San Francisco, CA 94107 |
| Block / lot | **3775 / 061** |
| OSM | way/124884348 |
| DataSF footprint | `SF3775061` |
| Built | 1907 |
| Storeys | 2 |
| Construction type | D (wood frame) |
| Use | Commercial Office |
| Zoning | SPD (South Park District) |
| Lot area | 2,143 SF (199.1 m²) |
| Anchor (WGS84) | **-122.3945863, 37.7816006** (footprint area centroid) |
| Footprint | **195.3 m²**, 16 vertices |
| Frontage | **6.90 m**, facing SE, outward bearing **135.3°** |
| Depth | **29.79 m** |
| Width | 6.99–7.02 m, pinched to **4.01 m** at the waist |
| Roof deck | **7.32 m** (LiDAR mode and median) |
| Target height | **7.6 m** — front eave crest |

## 2. Sources, and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| OSM way/124884348 (Overpass) | footprint geometry, address, `height=7` | **measured** |
| DataSF Building Footprints `ynuv-fyni`, `SF3775061` | roof deck 7.32 m (`hgt_majoritycm` = `hgt_mediancm` = 732), mean 7.34, σ 0.64 over 715 cells, max 1016, min 374, ground 8.25 m NAVD88 | **measured** |
| SF Assessor rolls `wv5m-vpq2`, block 3775 lot 061 | 1907, 2 storeys, Commercial Office, construction type D, 15 rooms, SPD, lot 2,143 SF — identical across all 19 rolls 2007–2025 | **measured** |
| SF Building Permits `i98e-djp9`, block 3775 | lot 061 = "126 South Park"; 1999-12-20 "repair damaged dry rot siding & trim" (2 existing storeys); 2023-08-28 "re-roofing" (2 existing storeys); plus the block-face storey counts in §6 | **measured** |
| [The Hawthorne Group leasing page](https://www.thgcommercial.com/project/126-south-park/) | a current (Sept 2025), straight-on, unobstructed colour photograph of the whole street elevation; "NATURAL LIGHT VIA 3-SIDES OF WINDOW LINE, PLUS AN ATRIUM GARDEN"; ~1,800 RSF ground floor | **observed (listing photo)** |
| [LoopNet listing 15125827](https://www.loopnet.com/Listing/126-S-Park-Ave-San-Francisco-CA/15125827/) | "Directly on South Park. Great Natural Light (skylights and windows on 4 sides)"; "Atrium"; renovated 1990; 2 tandem parking | observed (listing text); its **"3 Stories / 5,442 SF" is rejected**, §8 |
| California Energy Commission, Title 24 Part 6 §141.0(b)2Bi and the CRRC 2022 summary | a nonresidential low-slope re-roof of >50% or >2,000 sq ft (whichever is less) must reach an **aged solar reflectance ≥ 0.63** in every California climate zone | **measured (code text)** — the basis for the pale roof, §5 |
| [Gran Oriente Filipino National Register nomination](https://commissions.sfplanning.org/hpcpackets/2016-008192SRV%20-%20Gran%20Oriente.pdf) | block-face character: the surrounding buildings are "mainly two to four-story attached, mixed-use flats and multi-unit apartment buildings primarily constructed between 1906 and 1924" | context only |
| Esri World Imagery z20, tiles 167786–167788 / 405270–405272 | **nothing usable.** Washed out to near-white at this location; z21 returns "Map data not yet available" | **failed** |

### Sources rejected

- **Perkins&Will "South Park Venture Capital Firm"** and the matching **Office Snapshots**
  article. Search returns both for this address and summarises them as being at it.
  Both were fetched directly: **neither contains this address, or any address.** They
  describe a 16,420 sq ft brick-clad 1920s building — four times this building's floor
  area and the wrong construction. Not this building.
- **SF Planning case 2010.0959CV.** Also returned for this address. Its own header reads
  `Project Address: 147 SOUTH PARK AVENUE`, `Block/Lot: 3775/031` — the far side of the
  oval. Its "demolish the existing two-story single family dwelling" is not this building.

No photograph of the roof or the rear elevation was located. No architect is recorded and
the building carries no name.

## 3. Orientation

Front faces **south-east, outward bearing 135.3°**, onto South Park street 7.20 m away
and the park itself 12.06 m away. Rear faces **north-west, 315.4°**, onto a mid-block
yard with the nearest neighbouring vertex 5.53 m off. Both long flanks are party walls:
**north-east 45.0°** against 112 South Park at a 0.6 m gap, **south-west 224.9°** against
130/134 South Park at a 0.6 m gap.

The model is authored with Blender `+Y` = true north and `+X` = east, on the measured
polygon, so it drops into the city at its real heading with no loader rotation. Because
of the ~45° heading the axis-aligned bounding box is **26.74 × 26.59 m** for a building
6.9 m wide — near-square, and not an error. (That near-squareness is why `validation.json`
measures the waist by ray-cast section: the bounding box alone cannot distinguish this
model from one rotated 90°.)

## 4. The plan, measured

Depth `d` runs back from the street front; width `w` across from the south-west party
wall.

```
  w=7.02 |======================================================|  NE party wall (112)
         |            |####|  <- NE well 1.65 deep              |
  w=5.36 |            +----+                                    |
         |                                                      |
  w=1.34 |        +------+          +--------+                  |
         |   SW#1 |######|     SW#2 |########|  0.84 deep       |
  w=0    |========+------+==========+--------+==================|  SW party wall (130/134)
         d=0    9.86  13.35      16.88   20.72              29.79
        front                                                rear
              NE well spans d = 9.48 .. 11.85
```

| Well | Flank | Depth range | Length | Cut in |
|---|---|---|---|---|
| NE | north-east | d 9.48 – 11.85 | 2.37 m | 1.65 m |
| SW #1 | south-west | d 9.86 – 13.35 | 3.49 m | 1.28 m |
| SW #2 | south-west | d 16.88 – 20.72 | 3.84 m | 0.84 m |

The NE well and SW #1 overlap between **d = 9.86 and d = 11.85**, and over that 1.99 m the
plan is only **4.01 m** wide. The exported GLB measures **4.007 m** there.

## 5. What each side shows

**South-east (South Park front)** — *observed*, from the Sept 2025 photograph:

- **Horizontal wood siding**, wide boards (~200 mm exposure) with crisp shadow lines,
  painted a **cool mid gray with a faint green cast**, roughly `#8e9791`. Walls, eave and
  gate frame are all the same colour.
- A **projecting shed eave** across the full width, on **exposed rafter tails** (six or
  seven visible), with a light fascia along its outer edge and a plain frieze band where
  it meets the wall. The building's only ornament.
- **Upper floor**: a two-part double-hung window group in one shared surround, set toward
  the north-east; the south-west half is blank siding, with one narrower opening at the
  extreme south-west edge.
- A **belt course** at the floor line between the storeys.
- **Ground floor**, south-west to north-east: a flush door panel; a **recessed entrance
  bay closed by a tall dark expanded-metal security gate** carrying the number **126**;
  then two **tall multi-pane windows** on a continuous sill over a plain siding spandrel.
- One flat plane — no bay window, no projection but the eave.

**North-east and south-west (party walls)** — *measured*: blank, no openings, apart from
the light wells. In the photograph the north-east party line is completely covered by a
climbing vine growing on 112's side; it is the neighbour's and is not modelled.
130/134 to the south-west is three storeys and stands about 4.5 m above this roof.

**The light wells** — *measured in plan, inferred in section*: the only elevations besides
the front and rear that can carry glazing, and the reason the building has "3 sides of
window line". Modelled as full-height voids with two storeys of glazing on each well back.

**North-west (rear)** — *inferred*: no photograph found. Modelled as a plain service
elevation: one door, two small upper windows.

**Top** — *level measured, composition inferred*: flat at 7.32 m, and genuinely flat —
σ 0.64 m over 715 LiDAR cells with mode and median both landing on 7.32.

The deck is modelled **pale**, not the dark membrane this set usually uses. That is
evidence rather than taste: the 2023-08-28 re-roofing permit covers the whole ~2,100 sq ft
roof, which clears Title 24 Part 6 §141.0(b)2Bi's "more than 50 percent or 2,000 square
feet, whichever is less" trigger, and that section requires an aged solar reflectance of
**0.63** on a low-slope nonresidential re-roof in every California climate zone. A 0.63-SR
membrane is a pale roof. (135 South Park one block away is dark because an aerial was
actually read for it. Here the aerial is unusable and the building code is the better
source.) The washed-out Esri tile is weakly consistent with a pale roof but is not
evidence on its own.

Roof furniture is deliberately sparse — two skylights, a hatch, a vent cowl — and there
is **no mechanical plant**. Nothing in the evidence supports plant, and anything 0.7 m
tall would break the 7.6 m crest.

## 6. Row context

| Address | Lot | Storeys | Height |
|---|---|---|---|
| 106 South Park (Gran Oriente Filipino) | 058 | 3 | OSM 11 m |
| 108 / 110 South Park | 059 | 2 | OSM 8 m |
| 112 South Park | 060 | — | OSM 6 m; LiDAR majority 7.32 m, max 8.04 m |
| **126 South Park** | **061** | **2** | **LiDAR 7.32 m deck** |
| 130 / 134 South Park | 062 | 3 | LiDAR median 8.40 m and 11.77 m across its two parts |
| 140 South Park | — | — | OSM 10 m |

126 is among the lowest on its block face, and markedly lower than its south-west
neighbour.

## 7. Recognition cues, ranked

1. **The proportion** — 6.9 m wide, 29.8 m deep, at 45° to the world grid. A plank on edge.
2. **The waist** — two opposing light wells pinching the plan to 4.01 m.
3. **The projecting bracketed eave** over the street front.
4. **Gray painted horizontal siding**, low between taller neighbours.
5. The narrow front's composition: dark gated bay south-west, two tall windows north-east.

Cues 1–2 read from above, 3–5 from the street.

## 8. Confirmed vs inherited

**Confirmed by this pass** (independently re-derived, not taken from the plan):

- footprint geometry, area, anchor, all three well positions and the 4.01 m waist —
  recomputed from the Overpass response
- block/lot 3775/061, and that DataSF `SF3775061` is this building (its ring sits 0.58 m
  from ours at the nearest vertex)
- 1907, 2 storeys, wood frame, Commercial Office — 19 assessor rolls
- the roof deck at 7.32 m and its unusually tight distribution
- the entire street elevation, from the Hawthorne Group photograph
- that the LoopNet "3 storeys", the two Perkins&Will-adjacent pages and Planning case
  2010.0959CV do not describe this building

**Inherited or inferred, NOT confirmed:**

- the **eave crest at 7.6 m** (+0.28 m over the measured deck) — read off the photograph's
  proportions
- the **eave's slope direction** — a sidewalk-level photograph cannot settle whether the
  hood falls down-and-out or up-and-out; the commoner detail was chosen
- the **roof composition** — skylight count and positions, the hatch, the vent cowl.
  LoopNet establishes that skylights exist; nothing establishes where or how many
- the **pale deck colour** — inferred from the 2023 permit plus Title 24, not seen
- the **rear elevation** entirely
- whether the light wells are open to the ground, roofed, or planted
- the exact paint colour, and whether the party walls are painted at all
