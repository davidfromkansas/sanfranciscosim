# 350 Brannan Street — reference dossier

Research behind `artifacts/350-brannan/`. Compiled 12 August 2026, independently of
(and in two places correcting) `docs/asset-plans/350-brannan.md`. Everything marked
**measured** comes from a public dataset or from geometry computed from one; everything
marked *inferred* is a visual or derived estimate.

## 1. Identification — this one needed proving

The address does not resolve to a building through the usual route, and getting this
wrong would have meant modelling the wrong box.

- Nominatim returns `way/1120695896` for "350 Brannan Street, San Francisco". That way is
  the **Brannan Street roadway** (`highway=secondary`, TIGER-derived), not a building. The
  hit is an address interpolation along the street centreline.
- No building footprint on the block carries `addr:housenumber=350`. The block's tagged
  addresses are 318, 326, 334, 340, 358, 362/366, 370, 372/374 and 380.
- Resolution actually used: DataSF Addresses (`ramy-di5m`) maps `350 BRANNAN ST` to
  **parcel 3775016** at 37.780947 / −122.393435. The DataSF parcel polygon (`acdm-wktn`)
  for `blklot=3775016` carries `from_address_num = to_address_num = 350` and has centroid
  37.781021 / −122.393528.
- That centroid falls inside **OSM way/113545692** (`building=yes`, `height=12`, no address
  tags) and inside DataSF building footprint **`mblr = SF3775016`**.
- Corroboration by area: assessor lot area 5,797 sq ft = 538.6 m²; DataSF footprint
  537.3 m²; OSM footprint 534.2 m². The building covers essentially its whole lot, which is
  why the three numbers agree.

Confidence: high. Independent confirmation from a photograph of the "350" address plate
beside the northeast arched portal (Google Street View, Brannan Street, May 2025 capture).

## 2. Verified dimensions and location

| Item | Value | Source |
|---|---|---|
| Anchor (WGS84) | **−122.3935234, 37.7810229** | DataSF footprint centroid, reprojected — **measured** |
| Footprint area | 537.3 m² | DataSF `ynuv-fyni` — **measured** |
| Brannan (SE) frontage | 21.60 m | **measured** |
| Jack London Alley (NE) | 24.22 m | **measured** |
| Varney Place (NW) | 22.00 m | **measured** |
| Southwest party wall | 24.52 m | **measured** |
| Front heading | SE, outward normal **135.8°** true | **measured** |
| Roof deck | 12.02 m above grade | DataSF LiDAR `hgt_median_m` — **measured** |
| Tallest feature | 13.85 m above grade | DataSF LiDAR `hgt_maxcm` — **measured** |
| Parapet crest | ~12.90 m | *inferred* (deck + 0.88 m) |
| Ground (NAVD88) | 10.55 m | DataSF LiDAR `gnd_min_m` — the app's terrain handles this |
| Built | 1929 | SF Assessor secured roll, block 3775 lot 016 |
| Storeys | 3 | SF Assessor **and** all 25 building permits 1985–2026 — no conflict |
| Construction | Assessor class **C** (reinforced concrete), painted | SF Assessor roll + photography |
| Building area | 18,055 sq ft (assessor) / 19,662 sq ft (listing) | ≈3.1× footprint, consistent with 3 full floors |

**Why 13.85 m is the target height, not 12.** OSM's `height=12` matches the LiDAR *median*
(12.02 m) almost exactly, which makes it look authoritative; it describes the roof deck. The
crest is the roof penthouse at 13.85 m. Confirmed independently:
`peak_1st_m − gnd_min_m = 24.55 − 10.55 = 14.0 m`, and `hgt_maxcm = 1385`.

**Why the 2010 LiDAR is still valid.** All 25 permits from 1985 to 2026 are interior work,
reroofing (1990, 2010), an elevator replacement, parapet bracing (1993) and a freight-elevator
demolition (2023). Nothing added height. This is the check that 550 Third Street failed.

## 3. Orientation

The building fills a corner lot bounded by three public ways and one party wall — an
unusual configuration for this block and the reason the leasing copy advertises
"window lines on 3 sides".

| Face | Outward bearing | Length | What is beyond it |
|---|---|---|---|
| SE | 135.8° | 21.60 m | **Brannan Street** |
| NE | 44.5° | 24.22 m | **Jack London Alley** (5.2 m away) |
| NW | 315.9° | 22.00 m | **Varney Place** (4.1 m away) |
| SW | 225.3° | 24.52 m | party wall — 358 Brannan Street, nearest vertex 1.15 m |

Jack London Alley and Varney Place meet at the building's north corner (OSM node shared
between ways 8919615 and 8921605, at 37.7812301 / −122.3935240, 22.9 m due north of the
anchor). Two further sub-metre segments (0.42 m, 1.02 m) are survey jogs at the west and
south corners; both are kept in the model.

Authored with Blender `+Y` = true north, so the model drops in at its real heading; the
loader applies no rotation. Consequence: the axis-aligned bounding box is 33.3 × 33.3 m for
a 21.6 × 24.2 m building. That is the 45° heading, not a scale error.

## 4. Observations by side

**Southeast — Brannan Street (hero).** White/off-white painted wall, three storeys. Ground
floor is a colonnade: square piers framing recessed storefront glazing that reads pale
blue-green, with solid spandrels below — and it is **closed at both ends by a round-arched
portal** with a pale, lightly textured cast-stone surround. The northeast portal is the
"350" address entrance and carries the tenant signage; the southwest one is a recessed
secondary entry. Above: a string course, then two floors of large multi-light steel-sash
industrial windows with dark frames, the top floor visibly taller. The parapet is plain
with small raised attic panels stepping up over the pier positions.

**Northeast — Jack London Alley.** Same white wall and the same window rhythm, without the
arches. The **black zig-zag fire escape** hangs off the upper two floors, right of centre.
Ground level has service doors and the secondary accessible entrance — SF permits from
March 2008 record the ground-floor suite's designated entry being moved from the Brannan
entry to "jack london alley entry", and a separate application requests a new street
address for that entrance.

**Northwest — Varney Place.** *Not directly observed.* Neither Varney Place nor Jack London
Alley has Street View car coverage, and the satellite imagery only resolves the roof edge.
Modelled as a plainer version of the Jack London Alley elevation: same five-bay rhythm, one
service door, no arch, no fire escape. **This is the weakest part of the model and is
flagged in REPORT.md.**

**Southwest.** Party wall, 1.15 m from 358 Brannan Street's footprint. Blind, no openings.
Never visible in the app.

**Top.** Bright light-grey membrane roof inside a continuous parapet. Resolvable from
satellite: a **large raised rectangular penthouse** roughly centred and set slightly toward
Varney Place (the natural candidate for the 13.85 m LiDAR maximum), a row of small
rectangular skylights on the deck southwest of it, a mechanical/HVAC cluster toward the
Jack London Alley edge, and diagonal membrane seams.

## 5. Recognition cues (ranked)

1. **Two round-arched portals bookending the Brannan colonnade** — nothing else on the
   block does this, and it is the only cue that survives to thumbnail size
2. A white-painted three-storey box on a 45° corner site, finished on three sides
3. Two floors of large steel-sash industrial windows, the top floor taller
4. The black zig-zag fire escape on the Jack London Alley elevation
5. The big raised roof penthouse, clearly proud of the parapet

## 6. Preserved vs simplified

**Preserved** — the single chunky volume at its real 45° heading; both arched portals as
real arches at the ends of the ground floor; the three-finished-sides/one-blind-side
asymmetry; the white body against dark glazing, which is the building's whole value
structure.

**Simplified** — the Brannan ground floor is regularised to exactly 2 arches + 5
pier-framed bays and the upper floors to 5 identical bays per finished elevation;
cast-stone voussoirs become one flat surround band; steel-sash mullion grids become a
single recessed panel with no muntins; the fire escape becomes two chunky landings, rails
and one stringer, with no treads; tenant signage and the "350" numerals are dropped as
sub-pixel and dated.

**Exaggerated** — the portals only. Widened to 3.20 m and raised to a 1.25 m rise so they
still read from the app's aerial camera; this is the one place the asset spends semantic
exaggeration, per the style bible's conversion process.

## 7. Uncertainties and conflicting evidence

- **The brick trap.** Every neighbour is a brick warehouse, the sibling asset `380-brannan`
  *is* brick, and the South End Historic District literature describes brick warehouses at
  length. This building is **not** brick: the assessor records construction class C and
  every photograph shows smooth painted wall with no coursing. The historic district is
  also bounded by Stillman/First/Ritch/King and does not contain this lot, so district-level
  descriptions are not evidence about it.
- **Property class vs use.** The assessor still classes the property Industrial (`IND`);
  every permit since 1990 records `existing_use = office` and it is leased as creative
  office. The manifest uses `cat: 3` (office), matching its neighbour 380 Brannan.
- **The Varney Place elevation is unobserved** (section 4). Largest gap.
- **The bay count is *inferred***, from photography partly screened by mature street trees.
  The regularisation to 5 bays is a design decision, not a survey.
- **Whether 13.85 m is the penthouse or a raised parapet element is *inferred***. The
  satellite view shows a clearly raised central block and that is the natural reading, but
  the LiDAR maximum is a single cell. Either way the export's bounding-box top lands on
  13.85 m; only the shape of what tops out is at stake.
- No architect is recorded for the 1929 building in any source consulted.

## 8. Sources

- OSM way/113545692 (footprint, `height=12`), ways 8919615 / 8921605 (Jack London Alley,
  Varney Place), way 124890324 (358 Brannan Street)
- DataSF `ramy-di5m` — Addresses with Units
- DataSF `acdm-wktn` — Parcels
- DataSF `ynuv-fyni` — Building Footprints (2010 LiDAR-derived)
- DataSF `wv5m-vpq2` — Assessor Historical Secured Property Tax Rolls
- DataSF `i98e-djp9` — Building Permits (25 records, 1985–2026)
- Google Street View, Brannan Street and the Brannan/Jack London Alley corner, May 2025
  capture — the SE and NE elevations
- Google Maps satellite (Airbus / Maxar / Vexcel, 2026) — the roof
- Commercial listing copy (LoopNet / Showcase / Tandem) — 19,662 sq ft, 1929, high
  ceilings, "window lines on 3 sides"
- noehill.com South End Historic District page — consulted and **rejected as context**,
  see section 7

No copyrighted imagery is committed to this repository; the observations above are
descriptions of what the cited sources show.
