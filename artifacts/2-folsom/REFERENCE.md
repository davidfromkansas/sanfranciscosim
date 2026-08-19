# 2 Folsom Street — reference dossier

Gap Inc.'s owner-occupied global headquarters on the Embarcadero waterfront, at the foot
of Folsom Street. Robert A.M. Stern Architects (design) with Gensler (architect of
record), completed 2001. Also addressed **250 Embarcadero**; listed on SkyscraperPage as
"the Gap Building".

Compiled 19 August 2026 for `artifacts/2-folsom/`. The plan behind this build is
`docs/asset-plans/2-folsom.md`; **where this file and the plan disagree, this file wins**
(the plan is research, this is what was verified and built).

---

## 1. Sources, and what each establishes

| Source | Establishes |
|---|---|
| [ramsa.com — Gap Inc. Offices](https://www.ramsa.com/projects/project/gap-inc-offices) | The design intent, in the architect's words: the six-storey base; the superstructure "set back from the Embarcadero to minimize shadows on the waterfront park"; "a cubical background mass and a slender foreground tower"; tawny French limestone and red brick; "multiple porticoes of columns and lintels at the tower and the building's entrances", "at its boldest facing the harbor"; the seven-storey skylit atrium with Richard Serra's "Charlie Brown"; the sixth-floor Olin Partnership roof garden with "low geometric parterres"; **two entrances — one from the Embarcadero, one mid-block on Folsom** |
| [kriebelandassociates.com](http://kriebelandassociates.com/projects05.html) — written by Gap's own Senior Director of Corporate Architecture & Construction | "250 Embarcadero (also known as 2 Folsom)"; 600,000 sf; structural steel with a **precast panel exterior with brick and limestone**; the 7th-floor cafeteria opening onto the outdoor plaza |
| [cbengineers.com](https://www.cbengineers.com/project/gap/) — the MEP engineer | "**15-story**, 540,000 square foot design"; cafeteria, art gallery, two levels of underground parking, outdoor decks, rooftop garden; **10'8" ceilings** and underfloor air distribution |
| [gapinc.com press release, June 2022](https://www.gapinc.com/en-us/articles/2022/06/gap-inc-welcomes-customers-to-four-new-retail-stor) — the owner | "2 Folsom boasts **15 floors** of flexible, creative office space, a rooftop cafeteria and outdoor dining terrace overlooking the Bay, a coffee bar and lounge in the lobby, and a ground floor 'Co-Lab'"; four Gap-brand retail stores opened on the ground floor |
| [therealdeal.com, Feb 2022](https://therealdeal.com/san-francisco/2022/02/07/gap-to-open-banana-republic-old-navy-athleta-in-embarcadero-hq/) | 545,000 sq ft, **Gap-owned**; ~18,000 sq ft of ground-floor office converted to retail |
| [skyscraperpage.com id 4212](https://skyscraperpage.com/cities/?buildingID=4212) | "Gap Building", 2 Folsom Street, R.A.M. Stern, 2001; floor count 14, roof **275 ft — flagged Unconfirmed**. Rejected, see §7 |
| [OSM way 93817368](https://www.openstreetmap.org/way/93817368) | `addr:housenumber=2`, `addr:street=Folsom Street`, `building=office`, `building:levels=15`, `height=91`; a 20-node ring whose OBB is 84.49 x 77.32 m |
| [DataSF Building Footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni) record `201006.0000175` (mblr `SF3741035`) | The LiDAR row this whole build's vertical dimension rests on: 25,463 cells at 50 cm; `hgt_median 32.28`, `hgt_majority 72.11`, `hgt_mean 44.98`, `hgt_std 20.01`, `hgt_max 87.95`, `hgt_min 0.76`; `gnd_min_m 3.32`, `gnd_mean 3.60`, `gnd_std 0.07`; `peak_1st_m 91.55` |
| Google Maps satellite, near-nadir z20 (2026 capture) | The roof: the atrium skylight grid, both lawn parterres, the ranks of hedge parterres, the superstructure deck with its screened mechanical pen and two round fans, and the stepped crown. Also the measured building lean used to de-project it (§3) |
| [Wikimedia Commons — "The Gap headquarters.jpg"](https://commons.wikimedia.org/wiki/File:The_Gap_headquarters.jpg) (2010) | The one clean elevation photograph found: the brick field with limestone piers and frames, the base parapet with glass railing and planted edge, and the limestone tower's **double setback** up to a **crenellated crown pavilion** |
| OSM `building:part` ways 944981401, 1487162810, 1487162811 | Used only as a weak third check on the crown's plan area (197 + 103 m2). Their positions and `building:levels` disagree with every other source and were **not** used for placement — see §7 |

No copyrighted imagery is committed to this repo; the URLs above are the record.

---

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| WGS84 anchor | `-122.390975, 37.790787` | **measured** — the OBB centre of the DataSF footprint, reprojected through the app's tangent projection |
| Footprint | **84.31 x 77.14 m**, 6,341 m2, 97.5% rectangular fill | **measured**. OSM's independent OBB is 84.49 x 77.32 m — a 0.2% agreement, so there was no conflict to adjudicate |
| Cell-count cross-check | 25,463 LiDAR cells x 0.25 m2 = 6,366 m2 | agrees with the polygon area to 0.4% |
| Base roof / 7th-floor terrace | **32.28 m** | **measured** (`hgt_median`), and corroborated by RAMSA's sixth-floor roof garden and the 7th-floor cafeteria plaza |
| Superstructure roof deck | **72.11 m** | **measured** (`hgt_majority` — a large dead-flat deck produces a sharp mode) |
| Crown / architectural top | **87.95 m**, shipped as **88.00 m** | **measured** (`hgt_max`); `peak_1st_m 91.55` less `gnd_mean 3.60` reproduces it exactly; OSM independently tags `height=91` |
| Storeys | **15** | Gap Inc., CB Engineers and OSM agree; and 32.28 m / 7 = 4.61 m and (72.11 - 32.28) / 4.61 = 8.6, i.e. 7 + 8 = 15 |
| Floor-to-floor | **4.6 m** | derived from the two measured planes; consistent with CB Engineers' 10'8" ceiling over an underfloor air plenum |
| Ground elevation | 3.32 m NAVD88 min, 3.60 m mean, sigma 0.07 m | a dead-flat reclaimed waterfront site; the app's terrain handles it, not the asset |
| Level area split | base 70.6%, superstructure 23.1% (1,467 m2), crown 6.3% (402 m2) | **derived** — see §3 |

---

## 3. How the three roof planes and their areas were established

DataSF publishes one summary row per footprint, not the raw returns, so the split was
solved from that row and then checked twice by unrelated methods.

**The solve.** Fix the base plane at the median (32.28 m) — over half the cells are there,
which is what makes the median that number. Fix the two upper planes at the mode (72.11 m)
and the maximum (87.95 m). The published mean (44.98) and standard deviation (20.01) then
determine the three area fractions uniquely:

```
f2*(72.11-32.28) + f3*(87.95-32.28)                     = 44.98 - 32.28
f1*(32.28-44.98)^2 + f2*(72.11-44.98)^2 + f3*(87.95-44.98)^2 = 20.01^2
```

giving f1 = 0.706, f2 = 0.231 (1,467 m2), f3 = 0.063 (402 m2).

**Check 1 — the satellite.** The near-nadir Google capture shows the building leaning; the
lean was measured against the surveyed footprint at the block's south corner (64 px of
displacement over the 32.28 m base = **1.98 px/m**, 13.2 deg off nadir) and the upper
masses de-projected with it. That puts the 72.11 m deck at ~44 x 42 m centred 14.4 m
southwest of the block centre, and the crown at ~20 x 20 m near the block centre. The
model's superstructure-plus-tower union is 44 x 44 m centred 16 m southwest; its
above-72 m mass is 20 x 20 m.

**Check 2 — the OSM parts.** The two small `building:part` rings at the crown are 197 m2
and 103 m2, summing to 300 m2 against the solve's 402 m2 for everything above 72.11 m.

Three methods, none tuned to the others. The 42-44 m superstructure and the 20 m crown
remain the least certain dimensions in the asset; the three heights are the certain ones.

---

## 4. Orientation

The block is rotated **44.81 deg** off the world axes, like the whole SoMa grid; its
corners point north, east, south and west and its faces point at the four intercardinals.
Authored with Blender `+Y` = true north, `+X` = east — `placeGeneric()` in
`app/src/assets.js` scales and positions but never rotates.

| Face | Length | Outward bearing | What it is |
|---|---|---|---|
| northeast | 77.14 m | **45.2 deg** | **The Embarcadero** — the harbour elevation, the central projecting pavilion, one atrium entrance |
| southeast | 84.31 m | **135.2 deg** | **Folsom Street** — the address, the mid-block atrium entrance |
| southwest | 77.14 m | **225.2 deg** | **Spear Street** |
| northwest | 84.31 m | **315.2 deg** | toward the 201 Spear / One Steuart Lane block |

**Correction against the plan.** The plan's §2.3 lists the footprint corners as
`(-57.10, -2.35) west`, `(-2.72, -57.08) south`, `(57.10, 2.35) east`, `(2.72, 57.08)
north`. Those are the corners of the plain OBB. The **real** ring is not a plain
rectangle (§5), so the build uses the 24-vertex simplification, not those four points.

---

## 5. Observations, side by side and from above

**The footprint carries two of the architect's moves, and both are in the ring itself:**

- a **13.59 x 3.02 m recess in the middle of the Folsom face** — this is RAMSA's
  "mid block entrance on Folsom Street", present in the survey, not inferred;
- a **15.15 m central projecting pavilion on the Embarcadero face**, flanked by
  symmetric 1.3-1.55 m steps down to the flanks — the porticoes "at its boldest facing
  the harbor". The composition is symmetric about the face's centre, exactly as RAMSA
  describes;
- a matching **13.20 x 3.22 m service recess** in the middle of the northwest face;
- the **two Spear-side corners step in 4.7 m**; the two Embarcadero-side corners are
  square. This asymmetry is why the asset's axis-aligned bounding-box centre sits 2.04 m
  from its origin (§6).

**Northeast — The Embarcadero.** The elevation the whole composition is aimed at. Brick
over a limestone ground storey, limestone piers and spandrel bands, the central pavilion,
and the portico. Above the base parapet the terrace runs back 36 m before the
superstructure begins, so from the water the tower reads as standing behind a garden.

**Southeast — Folsom Street.** The address and the longest face. Same system; the
mid-block entrance portico sits in the real recess. The 2022 Gap-brand retail fronts are
at ground level (represented as the glowing sign band, not as shopfronts).

**Southwest — Spear Street.** The longest unbroken plane, 68.56 m. The superstructure sits
close to this edge because it is set back from the water, so from Spear the mass is
directly overhead.

**Northwest.** Free-standing, not a party wall (*inferred* from imagery — see §7). Same
system, plainest rhythm; the service recess is here.

**Above** — the most important view, and 6,341 m2 of designed surface at 32.3 m:
the atrium skylight as a gridded translucent panel in the northeast quadrant; two Olin
lawn parterres with water strips; ranks of clipped hedge parterres on the Folsom and
northwest terraces and one rank in the narrow Spear-side band; a wide paved ring inside
the limestone parapet. Above that, the superstructure deck in pale membrane with a
screened mechanical pen, two round fans and a stair penthouse, and then the crown.

---

## 6. Recognition cues, ranked

1. **The three-mass step-up toward the harbour** — base, brick block, limestone tower
2. **Brick body, limestone tower**, the two-material split that tells the masses apart
3. **A whole-block base with a garden and a glass roof on it**
4. **88 m on the Embarcadero**, between the Ferry Building and Hills Plaza
5. The crenellated stepped crown, the only silhouette here that is not a flat parapet

**Preserved:** the footprint and all three measured planes exactly; the 16 m southwest
setback and the tower's northeast placement; the material split; the skylight and both
gardens; the two entrance porticoes; the real Folsom entrance recess.

**Simplified:** the skylight's ~11 x 8 glazing grid becomes 6 x 5; the crown's merlons
become eight chunky blocks; the hedge parterres become extruded strips; brick coursing,
mullions, railings, furniture, louvres and downpipes are dropped; the retail fronts
become a glowing sign band with no lettering.

---

## 7. Uncertainties and conflicting evidence

- **"A six story base with a fifteen story superstructure" is 15 storeys in total**, not
  21. RAMSA's sentence is the single most misreadable fact about this building; Gap Inc.,
  CB Engineers and OSM all say fifteen, and the measured planes divide into 7 + 8 at
  4.6 m. Resolved.
- **SkyscraperPage's 275 ft / 14 floors is rejected.** It is flagged *Unconfirmed* on its
  own page, 83.8 m falls between the measured 72.11 m deck and the measured 87.95 m
  crown, and 14 floors contradicts four sources.
- **OSM `height=91` vs LiDAR 87.95 m.** The LiDAR maximum is used. The two agree closely
  enough to corroborate each other, and 87.95 is a measurement of this footprint.
- **The 42 x 42 m superstructure and the 20 x 20 m crown are the least certain
  dimensions** (§3). The heights are measured; these plan sizes are solved and
  cross-checked but not surveyed.
- **The tower's setback levels (78.0 m and 84.0 m) are estimated**, read off the 2010
  photograph by counting window rows between the measured terrace and the measured crown.
- **Bay counts are inferred** from that same photograph plus the satellite; neither shows
  a square-on face. This is the most likely place for the model to be visibly wrong.
- **The northwest condition is inferred.** Imagery suggests a service way rather than a
  party wall, but no source consulted states it.
- **The 2022 renovation's exterior scope is unknown** beyond the four ground-floor retail
  fronts; the 2010 photograph may predate a ground-level facade change.
