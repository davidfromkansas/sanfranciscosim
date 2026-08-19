# 49 Zoe Street — reference dossier

Compiled for the SF-SIM miniature asset. Everything here was re-verified against
primary sources during the build; where this document and
`docs/asset-plans/49-zoe.md` disagree, **this document and `REPORT.md` win**.

Confidence labels: **measured** (survey / open-data record / metric
rectification), **observed** (read off a photograph), **inferred** (reasoned from
typology or a related record), **estimated** (a judgement call with a stated basis).

No copyrighted imagery is committed. Sources are cited by URL and by what each
one establishes.

## 1. Identity

| | | Confidence |
|---|---|---|
| Address | 49 Zoe Street, San Francisco CA 94107 | measured |
| Block / lot | Block 3776, `mapblklot` 3776128, condo lots 128–143 plus five parking-stall lots | measured |
| OSM | `way/147508937` — `building=yes`, `addr:housenumber=49`, `addr:street=Zoe Street`, `height=14`, `source=Bing` | measured |
| Built | **1997** (assessor); construction permits 1996–97 | measured |
| Predecessor | a two-storey office/commercial/storage building, demolished under permit **9421357**, issued Dec 1994 | measured |
| Use | **artist live/work**, 16 units; assessor class `LZ` "Live/Work Condominium" | measured |
| Unit tiers | **two identical tiers of eight.** Assessor areas repeat exactly — 694, 775, 860, 937, 832, 987, 900, 693 sq ft on lots 128–135 and again on 136–143 | measured |
| Total unit area | 13,356 sq ft = 1,241 m² | measured |
| Storeys | **5** on the 2018 re-roofing permit; visually one CMU garage level plus **two double-height loft tiers** (four window rows) | measured / observed |
| Zoning | CMUO today; SLI when built | measured |
| Architect | **not established** — see §7 trap 1 | — |

## 2. Location, footprint and orientation

| | | Confidence |
|---|---|---|
| Anchor (WGS84) | **−122.3960338, 37.7800764** — centroid of the four regularised corners | measured |
| Cross-check | Nominatim returns −122.3960408, 37.7800750 (0.6 m away); the DataSF address point is −122.3960123, 37.7800761 (1.9 m, the parcel centroid) | measured |
| Footprint | **28.24 m × 19.78 m**, 558.6 m². The raw DataSF ring is 561 m² and every one of its eleven vertices lies within **0.09 m** of the regularised rectangle | measured |
| Grid | the standard 45° SoMa grid | measured |

Corners in the app's local tangent frame (`x=(lon+122.4375)·111320·cos 37.77°`,
`z=−(lat−37.77)·110540`):

| Corner | x | z |
|---|---|---|
| A north — Zoe frontage at the party wall | 3631.94 | −1116.89 |
| B west — rear at the party wall | 3645.89 | −1130.85 |
| C east — rear at the parking lot | 3665.77 | −1110.85 |
| D south — Zoe frontage at the parking lot | 3651.81 | −1096.77 |

| Face | Length | Outward normal | Beyond it |
|---|---|---|---|
| **South-west (Zoe Street)** | 28.24 m | **225.4°** | the alley; the facade stands 6.2 m from the centreline of a ~13 m right-of-way. **The only street-visible elevation** |
| North-west (party wall) | 19.78 m | 315.4° | 33–35 Zoe (`SF3776144`), touching at 0.00 m and 10.8–11.9 m tall, so our top ~2.5–3.5 m stands clear |
| North-east (rear) | 28.24 m | 45.4° | a 2.4–2.7 m light gap, then `SF3776456` (15.9 m) and `SF3776105` (8.0 m) fronting Ritch Street |
| South-east (parking lot) | 19.78 m | 135.4° | an open surface parking lot — fully exposed, and the second-most-seen face from the app's aerial camera |

The raw survey ring carries two 0.33 m in/out jogs part-way along the south-east
face. They are digitising-scale articulation, below the miniature's resolution;
the plan is regularised to a clean rectangle and the simplification is recorded
in `REPORT.md`.

Ground is flat: DataSF LiDAR ground across the footprint ranges 5.12–5.60 m
NAVD88, a 0.48 m spread, so no terrain compensation is needed.

## 3. Height

| Level | Value | Confidence |
|---|---|---|
| **Crest (penthouse vent)** | **17.00 m** — DataSF `hgt_maxcm` 1699 | measured / inferred attribution |
| Parapet | **14.40 m** | measured |
| Roof deck | 13.60 m | estimated (parapet − 0.80) |
| CMU base / shelf | 2.95 m | measured (rectification) |

The roof plane is the best-supported number in this dossier. DataSF `ynuv-fyni`
record `SF3776128` gives, over **2,268 half-metre cells**: median 14.42 m, mean
14.41 m, modal 14.38 m, **sd 1.13 m**. Mean ≈ median ≈ mode within 4 cm, with a
sd that cannot contain a step, is a textbook **single flat plane**. There is no
second roof level.

The 16.99 m maximum is therefore a discrete object standing on that plane, and
the aerial shows exactly one candidate: a pale rectangular penthouse with a round
vent at the south-east end, ~2.6 m proud of the deck — the elevator overrun and
stair bulkhead that the listing's "elevator and easy staircase access" and its
roof deck both require. It is **not** tree canopy: `peak_1st_m` (22.29 m) minus
`gnd_min_m` (5.12 m) is 17.17 m, i.e. the first-return peak and `hgt_max` agree,
whereas canopy over a footprint pushes them apart.

**Independent corroboration.** A metric rectification of Street View panorama
`c2ZLvpFONJnFRVJgvl9OMw` (method in §6) put the parapet at **13.2 m ± 0.7 m** —
agreement within its own error, which is dominated by the solved camera-to-facade
distance at a ~60° look-up angle. OSM's Bing `height=14` is a third, independent
agreement. **14.4 m is the roof; 17.0 m is the crest.**

## 4. What each side shows

### South-west — Zoe Street (the subject)

Measured off the rectified elevation, ±0.35 m (the fit's rms residual):

| Element | Band |
|---|---|
| Split-face CMU base, sidewalk to shelf | 0.00 – 2.95 m |
| Roll-up doors within the base | ~0.15 – 2.40 m |
| Panel wall starts, oversailing the base ~0.20 m | 2.95 – 3.10 m |
| Tier 1 main glazing (floor-to-ceiling) | 3.10 – 5.55 m |
| Tier 1 juliet rail (horizontal slats) | 3.35 – 4.30 m |
| Tier 1 spandrel | 5.55 – 5.90 m |
| Tier 1 mezzanine window | 5.90 – 7.80 m |
| Panel band between tiers | 7.80 – 8.40 m |
| Tier 2 main glazing | 8.40 – 10.70 m |
| Tier 2 juliet rail | 8.55 – 9.50 m |
| Tier 2 spandrel | 10.70 – 11.00 m |
| Tier 2 mezzanine window | 11.00 – 12.50 m |
| Blank panel (roof structure zone) | 12.50 – 13.60 m |
| Parapet | 13.60 – 14.40 m |

Horizontally: **four bays on a ~7.06 m module**, each carrying ~3.2–3.5 m of
glazing. The base carries **five roll-up doors** of about 2.9–3.4 m with 0.5–0.9 m
CMU piers between them, and a **recessed pedestrian entry** at the south-east end
under a galvanised steel awning. Two large street trees occlude bays 2 and 3 in
every available photograph.

The cladding: full-height vertical panel bands, roughly thirty of them across the
frontage, widths from about 0.35 m to 1.5 m, in five near-neutral tones
(off-white, warm pale, warm grey, sage-grey, blue-grey). They continue across the
spandrels and the blank band below the parapet; the windows are cut through them.
No cornice, no coping projection, no expressed structure.

### North-west — party wall
Blind. **inferred:** plain panel or painted blockwork, no openings. The top
~2.5–3.5 m stands clear of 33–35 Zoe next door.

### North-east — rear
Onto a 2.4–2.7 m light gap with a 15.9 m neighbour immediately behind.
**observed (oblique aerial):** a plain pale wall with a small number of punched
openings.

### South-east — parking lot
**observed (oblique aerial):** a largely blank cream wall with small punched
windows in vertical stacks, and a black steel **fire escape** — permit **9621922**,
$8,000, completed 1996–97, "install fire escape at east elevation".

### Above — the roof (558 m²)
**observed (Google satellite z21/z22, rectified into building-local plan
coordinates against the DataSF ring):**

- A pale grey membrane over the whole footprint, inside a continuous parapet ring.
- **A central spine of three raised glazed monitors**, staggered rather than
  collinear, each about 7 m long and 2 m wide, made of five or six mullioned
  panes. They light the internal circulation between the Zoe-facing and rear
  units and are the roof's subject.
- **A scatter of square dome skylights**, ~1.5–2 m, six to eight of them.
- **Small vent cans**, 0.3–0.5 m, in loose clusters near the monitors.
- **The stair/elevator penthouse** at the south-east end, roughly 8 × 6 m in plan
  and 2.6 m proud of the deck, with a round vent or dome on top.
- **A paved common roof deck** at the north-west end — documented by the sale
  listings, and matching a walled paved area visible on the aerial there. See
  §7 trap 5 for why its ownership is not fully resolved.

## 5. Recognition cues (ranked)

1. **The irregular vertical stripe facade.** Nothing else in the scene has it.
2. **The double-height loft rhythm** — two tall tiers, not four floors, each with
   a juliet rail across its lower window.
3. **The rusticated CMU garage base** with its row of grey roll-up doors, in its
   own shadow line under the oversailing panel wall.
4. **The monitor spine on the roof** — three staggered glazed ridges down the
   middle of an otherwise plain grey membrane.
5. **The penthouse with its round vent**, breaking the flat silhouette once.

**Preserve:** the stripe irregularity, the two-tier rhythm, the base shadow line,
the monitor spine, the flat unbroken parapet.
**Simplify:** ~30 real stripes to 23; mullion grids to single panes; the CMU
coursing to one horizontal reveal; the SE and NE elevations to a handful of
punched openings.

## 6. Method note — making the Street View elevation metric

Following `sf3d-streetview-photogrammetry`: the equirectangular tile set (zoom 3,
4096 × 2048) for panorama `c2ZLvpFONJnFRVJgvl9OMw` was downloaded with a browser
user-agent and referer; **the panorama's own reported lat/lon was not trusted**.
The two facade corners were read off the equirect at columns 183 and 1665, giving
a subtended angle of 130.2°. Constraining the camera to the Zoe Street centreline
then fixes it at 6.2 m from the facade plane and 18.9 m along it from the
north-west corner, with a yaw offset of 136.07° and a panorama roll of −2.2°.
Every facade point's horizontal distance is then known, and the equirect resamples
into a true orthographic elevation whose scale is fixed by the surveyed 28.24 m
frontage. The parapet fit has an **rms residual of 0.35 m** across 146 sampled
columns — that is the accuracy attached to every height in §4.

The roof was handled the same way: the z21/z22 satellite tiles were resampled
into building-local plan coordinates (u along the Zoe face, v into the block) so
roof features could be read in metres rather than eyeballed.

## 7. Uncertainties, conflicting evidence and source traps

1. **No architect of record.** Two plausible attributions are both wrong.
   *Kaplan Architects* appears at "49 Zoe St, Suite 10" in the SF business
   registry (location start 1997-06-01) and on LinkedIn — it is a two-person
   residential practice **occupying a unit**, which is exactly what a live/work
   building is for. *Santos Prescott and Associates* really did build a Zoe Street
   live/work loft in 1998, but it is 33–35 Zoe (the "Ritch / Zoe Studio", client
   Adele Santos, `mapblklot` 3776144) — our party-wall neighbour — and the Curbed
   piece about a $1.95M concrete loft with 20-foot ceilings is about that
   building, not this one.

2. **The facade is from 2013, not 1997.** Permit **201110187089** (filed Oct 2011,
   completed 31 May 2013, $300,000) re-clad the whole exterior and replaced every
   window "to eliminate water intrusion issues". Any pre-2013 photograph shows a
   different building. The asset models the current state.

3. **OSM `height=14` is a Bing trace.** It happens to agree with the LiDAR roof
   plane, but it is not the architectural top and must not be the normalisation
   target.

4. **Bay widths and stripe rhythm are the weakest measured numbers.** Two street
   trees stand in front of bays 2 and 3 in the only available panorama, and the
   stripe widths were read from a rectification with a 0.35 m rms residual. The
   four-bay module is solid — it is corroborated by the assessor's
   eight-units-per-tier fingerprint, four fronting Zoe and four to the rear. The
   individual widths are not.

5. **Whose roof deck?** The aerial shows a walled, paved area with furniture at the
   north-west end, straddling the party-wall line to within the accuracy of the
   imagery. Two readings fit the pixels: (a) it is 49 Zoe's common roof deck,
   which the Unit 6 listing independently proves exists; (b) it is the *central
   courtyard* Santos Prescott describe carving out of 33–35 Zoe. Relief
   displacement cannot separate them, because our roof (14.4 m) and the
   neighbour's (10.8–11.9 m) are displaced by different amounts in a view ~8–19°
   off nadir. The asset places a modest 7.0 × 4.4 m deck at that end because the
   evidence for *a* deck is direct; **the position is inferred.**

6. **`hgt_max` attribution is inference.** 16.99 m is certainly a real return on
   the footprint and the aerial certainly shows a penthouse; that the two are the
   same object is inferred. If a later capture shows the penthouse is shorter, the
   fix is to lower the penthouse and re-normalise — **not** to change the 14.4 m
   roof plane.

7. **Only one elevation is street-visible.** The north-east and south-east faces
   are described from oblique satellite pixels at ~0.02 m/px, which is enough for
   "blank wall with small punched windows" and not enough for their positions.
   They are *inferred*. The fire escape is the exception — the permit is
   documentary — though the permit's word "east" has been read as the south-east
   face on the grounds that a fire escape must discharge to the open parking lot
   rather than into a 2.5 m light gap.

## 8. Sources

**Open data (primary):**
- DataSF `ynuv-fyni` Building Footprints (2010 LiDAR-derived), record `SF3776128`
  — footprint ring, `hgt_mediancm` 1442, `hgt_maxcm` 1699, `hgt_stdcm` 113.4,
  `hgt_cells50cm` 2268, `gnd_min_m` 5.12, `peak_1st_m` 22.29.
- DataSF `acdm-wktn` Parcels — block 3776, `mapblklot` 3776128, condo lots
  128–143 plus five parking-stall lots, zoning CMUO.
- DataSF `ramy-di5m` Addresses — "49 ZOE ST #1" … "#16" all at a single point;
  **no other street number shares this footprint**, so the one-parcel-many-
  addresses trap does not apply.
- DataSF `wv5m-vpq2` Assessor secured roll (2025) — year built 1997, class `LZ`,
  the eight-value area fingerprint repeated across two tiers.
- DataSF `i98e-djp9` Building permits — 2018 re-roof (5 existing storeys, 16
  units); 2019 unit alteration ("artist live/work", 16 units).
- OpenStreetMap `way/147508937`; Zoe Street centrelines `way/1459359169` and
  `way/8917324` (used to establish which face is the frontage).

**Permit history** (SF DBI, via checkpermits.com):
`9421357` Dec 1994 demolition · `9421358` + revision `9623952` the new building ·
`9611330` Jun 1996 sprinklers · `9618982` Oct 1996 fire alarm · `9621922` fire
escape, east elevation · `9704456` Mar 1997 galvanised steel entry awning ·
`201110187089` Oct 2011 → May 2013 re-clad + all-new windows + new roof, $300,000 ·
`201804186674` Apr 2018 re-roof, $133,500.

**Imagery:**
- Google Street View panorama `c2ZLvpFONJnFRVJgvl9OMw`, on Zoe Street in front of
  the building, imagery ©2026 — the only street-visible elevation.
- Google Street View panorama `HoUosdm6QHhH_l1AhoKXVw`, Zoe at Freelon —
  establishes the parking lot and alley context; the building itself is occluded.
- Google satellite tiles z21 and z22 (`mt1.google.com/vt/lyrs=s`) — the roof.

**Listings** (observed, listing copy — the building as marketed):
- `compass.com/homedetails/49-Zoe-St-Unit-6-…` and
  `meryl.realestatesf.com/properties/49-zoe-street-unit-6` — *16 unit boutique
  building*, *elevator and easy staircase access*, *common area roofdeck offers
  spectacular urban views*, *grand exclusive use patio*, *soaring floor to ceiling
  windows*, *parking and storage in garage*. Unit 6, 987 sq ft, sold $880,000 on
  2020-07-27.

A domain-restricted photo search across redfin / zillow / compass / sf.curbed /
socketsite produced **no exterior photograph of 49 Zoe**. Street View is therefore
the only elevation reference, which is what makes the rectification in §6
load-bearing rather than a nicety.
