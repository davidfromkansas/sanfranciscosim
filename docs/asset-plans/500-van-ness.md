# 500 Van Ness Avenue — The Corinthian

Four-storey 1915 apartment building over a ground-floor bank/retail base, at the
north-east corner of Van Ness Avenue and McAllister Street, San Francisco Civic
Center. Slug `500-van-ness`, manifest id `500-van-ness`, runtime status
**new landmark** (Case B: registry entry + tile re-bake required).

> **Address note, read this first.** `500 Van Ness Ave` is the *retail* address of
> a single building that spans **500–524 Van Ness Avenue**; the assessor and OSM
> both file the parcel under **512 Van Ness Avenue**, and the building's name is
> **The Corinthian**. All three addresses are the same structure (Block 0766,
> Lot 006) — one 1,232 m² footprint, one roof, one cornice. The Chase branch at
> 500 occupies the corner storefront. It is **not** 505 Van Ness (the state
> office building across the avenue, already planned as
> [`505-van-ness.md`](./505-van-ness.md)) and not 501/536/544 Van Ness.

---

## Part 1 — ready-to-run task prompt

> Build the SF-SIM miniature of **500 Van Ness Avenue (The Corinthian)** as a
> validated GLB under `artifacts/500-van-ness/`.
>
> Read first, in this order: `AGENTS.md` (iron rules), `docs/styles/miniature-toy.md`
> (the artistic gate, in full), `.agents/skills/sf-asset-check/SKILL.md` (the
> technical contract). The reference implementation to mirror is
> `artifacts/505-van-ness/` — same four deterministic scripts, same headless
> invocation, same report structure.
>
> **Re-verify §2.2–2.5 of this dossier before modelling.** Plans in this repo
> have been wrong before; if the model and the plan disagree, REPORT.md wins and
> the correction is written up prominently.
>
> Produce, in `artifacts/500-van-ness/`:
> `build_500_van_ness.py`, `render_500_van_ness.py`, `validate_500_van_ness.py`,
> `make_contact_sheet.py`, `500-van-ness.blend`, `500-van-ness.glb`, four
> elevations + top + day aerial + night aerial, `500-van-ness-contact-sheet.png`,
> `validation.json` (all-PASS), `REFERENCE.md` and `REPORT.md`.
>
> Hard requirements: geometry authored in true-world orientation (Blender +Y =
> north, +X = east — the loader never rotates); origin at the footprint bbox
> centre; `min z = 0`; **bbox top normalized to exactly 17.000 m** so the
> loader's `targetHeightM / measuredHeight` scale lands at 1.000; flat `Toy_*`
> materials only; a designed roof (the camera looks down); a required night
> state via `_Glow` shells proud of the opaque glazing; ≤ 14,000 triangles.
>
> This is a **secondary building, not a hero** (style bible §21): clear massing,
> one strong facade rhythm, a simple designed roof, one or two identity cues.
> Spend the geometry on the bay-window rhythm and the parapet, not on ornament.
>
> Review the high three-quarter aerial FIRST and iterate on it before running
> the formal rig.

---

## Part 2 — research and design dossier

### 2.1 Identification

| Field | Value | Source |
|---|---|---|
| Addresses | 500–524 Van Ness Ave (retail), 512 Van Ness Ave (parcel of record), San Francisco, CA 94102 | SF assessor roll; commercial listing for "Corinthian Court" — *verified* |
| Building name | The Corinthian | OSM `name`; rental listings — *verified* |
| Assessor parcel | Block 0766, Lot 006 (`mblr` SF0766006) | DataSF secured property roll — *measured* |
| OSM object | `way/355209013`, `building=apartments` | OSM / Overpass API — *measured* |
| OSM tags | `building:levels=4`, `height=15`, `addr:housenumber=512` | OSM API |
| Built | 1915 | SF assessor `year_property_built`; corroborated by a rental listing — *verified* |
| Storeys / units | 4 storeys, 55 units, 128 rooms | SF assessor roll — *measured* |
| Use | Multi-family residential (A15, "Apartment 15 units or more") over ground-floor retail; the corner storefront is a Chase branch addressed 500 Van Ness | SF assessor roll; branch directory — *verified* |
| Architect | not found | — *unknown; no geometry depends on it* |

### 2.2 Anchor and footprint — *measured*

Ring of `way/355209013` pulled from the Overpass API, reprojected with the app's
tangent projection (`LON0 −122.4375`, `LAT0 37.77`), closed-ring Douglas–Peucker
simplified at ε = 0.3 m.

| Quantity | Value |
|---|---|
| Measured ring | 14 vertices, area **1,231.9 m²** |
| Simplified ring (modelled) | 8 vertices, area **1,230.1 m²** (−0.15 %) |
| Minimum-area OBB | 34.8 × 37.0 m at −171.22° |
| Axis-aligned extent | **40.0 m (E–W) × 41.8 m (N–S)** |
| Parcel cross-check | assessor lot area 13,076 sq ft = **1,215 m²**; 2010 LiDAR footprint 4,853 cells × 0.25 m² = **1,213 m²** |
| **Anchor (model origin = ring bbox centre)** | **lon −122.4199220, lat 37.7804082** |

The ring is a clean rectangle rotated 8.8° off the compass grid (the Civic Center
street grid), with one rectangular notch cut into the Van Ness side — the
entrance light court, §2.5. The west wall's four vertices are exactly colinear
either side of that notch, so the simplification is lossless there; the only
points DP removed are six near-colinear survey points on the east party wall
(max deviation 0.06 m).

Modelled ring, metres, x east / y north, origin at the anchor, CCW:

```
(-20.00,  15.62) (-17.67,   0.87) (-10.17,   2.11) ( -9.17,  -4.68)
(-16.61,  -5.87) (-14.29, -20.91) ( 20.00, -15.62) ( 14.27,  20.91)
```

Edge roles (outward-normal headings, true):

| Edge | Length | Normal | Reads as |
|---|---|---|---|
| 0→1 | 14.93 m | 261.0° | **west elevation, north pavilion** (Van Ness) |
| 1→2 | 7.60 m | 170.6° | north wall of the entrance court |
| 2→3 | 6.86 m | 261.6° | back wall of the entrance court (the entrance itself) |
| 3→4 | 7.53 m | 350.9° | south wall of the entrance court |
| 4→5 | 15.22 m | 261.2° | **west elevation, south pavilion** (Van Ness) |
| 5→6 | 34.70 m | 171.2° | **south elevation** (McAllister — the long show face) |
| 6→7 | 36.98 m | 81.1° | east elevation (party wall, abuts the Courthouse block) |
| 7→0 | 34.68 m | 351.2° | north elevation (party wall / rear) |

### 2.3 Height — *estimated from a measured roof deck*

**Target height 17.0 m (crest = top of the parapet).**

| Datum | Value | Source |
|---|---|---|
| Roof deck (flat membrane) | **15.48 m** | 2010 city LiDAR, `hgt_median_m` over the footprint — *measured* |
| LiDAR mean / max over the footprint | 15.23 m / 23.42 m | same record |
| OSM `height` | 15 m | consistent with the LiDAR median, i.e. it describes the deck |
| Storeys | 4 | assessor + OSM, and countable in the reference photographs |
| **Crest (parapet coping + urn finials)** | **17.0 m** | *estimated*: deck + ~1.5 m of cornice, parapet and finials read off the photographs |

This is the reverse of the usual failure mode in this repo: the OSM `height` is
not a low shell, it is the *roof surface*, and what it omits is the crowning
cornice-and-parapet that this building's silhouette is mostly made of. The
LiDAR `hgt_median` over a flat roof is the deck by construction (the parapet is
a thin ring and cannot move a median); the LiDAR `hgt_max` of 23.42 m is not
usable as a crest — it is a single-cell maximum over a footprint that abuts a
taller neighbour to the north, and nothing 8 m above the roof appears in any
photograph of the building.

Storey rhythm that lands on the measured deck: a tall commercial ground floor at
**4.7 m** plus three residential floors at **3.6 m** = 15.5 m. That matches both
the LiDAR deck and the storey bands counted in the photographs.

`estimated: true` in the manifest, because the 1.5 m of parapet above the
measured deck is photo-derived.

### 2.4 Orientation — *measured*

Authored in true-world orientation (+Y north, +X east), per the standing
orientation note in this directory: `placeGeneric()` never rotates, so real-world
heading wins over the contract's "front faces −Y". The building is rotated
**8.8° anticlockwise** off the compass grid, with the residential **entrance
facing 261.6° (W)** at the back of the Van Ness court and the retail entrance on
the McAllister corner. This deviation from the −Y rule is recorded in REPORT.md.

### 2.5 Four elevations and the roof — *observed*

Reference: Google Street View panoramas at the Van Ness/McAllister intersection
(captures Dec 2024 and Jan 2025) looking east at the Van Ness elevation and north
at the McAllister elevation; Esri World Imagery (z20) for the roof.

- **West (Van Ness) — the composed front.** Symmetrical: **two equal pavilions**
  (14.9 m and 15.2 m) flanking a **recessed central court** 6.9 m wide and 7.5 m
  deep, open to the avenue above the ground floor and holding the residential
  entrance at its back wall. Each pavilion carries **two projecting bay windows**
  running floors 2–4; the outer bays at the corners are **rounded**, the inner
  ones **square**. Walls are painted near-white stucco. A **heavy bracketed
  cornice** caps the composition, over it a **panelled parapet** whose piers carry
  small **urn / ball finials** — the strongest thing in the silhouette. The ground
  floor is a continuous dark storefront band behind a light stucco frame.
- **South (McAllister) — the long face.** 34.7 m of the same system, four bays of
  the same alternating rounded/square oriels, small iron **juliet balconies**
  between them, and two black **zigzag fire escapes** — the single most
  San-Franciscan cue on the building. The retail base runs the full length with
  the bank's blue fascia sign band and its glass corner entrance.
- **Roof.** Flat, pale grey membrane. Two deep **light wells**: the Van Ness
  entrance court (open to the west) and a second interior well roughly mid-plan.
  A **stair penthouse**, a small cluster of mechanical boxes and a scatter of
  vents. No tower, no pitched roof, nothing above the parapet line.
- **East and north.** Party walls: the Courthouse block abuts to the east (its
  nearest surveyed vertex is 17.7 m from our anchor) and a neighbouring building
  to the north. Plain painted stucco, punched windows only where the light wells
  allow — *inferred*; neither face is photographable from the street.

### 2.6 Recognition cues (the 3–5)

1. The **parapet with its urn finials** over a heavy bracketed cornice — the lid,
   and what makes the silhouette read as Edwardian rather than as a box.
2. The **rounded + square bay-window rhythm** wrapping both street faces.
3. The **recessed entrance court** splitting the Van Ness front into two pavilions.
4. The black **zigzag fire escapes** on McAllister.
5. The **dark retail band with its saturated blue sign fascia** grounding the
   whole composition.

### 2.7 Massing recipe

One extruded body on the 8-vertex ring — no secondary volume. Vertical scheme:
ground-floor retail band 0 → 4.7 m behind a stucco frame; a belt course at 4.7;
three residential storeys 4.7 → 15.5 m; bracketed cornice 15.5 → 16.2 m
(projecting 0.7 m); panelled parapet 16.2 → 16.7 m; urn finials setting the crest
at exactly **17.000 m**. Bays project 0.9 m over floors 2–4 and stop under the
cornice: eight of them (two per Van Ness pavilion, four on McAllister),
alternating rounded (10-segment half-cylinder, style bible §4 low-seg curves) and
square. Entrance court cut as a notch in the ring, its back wall carrying the
recessed residential entrance. Roof: deck, two light-well voids, stair penthouse,
three mechanical blocks, a skylight pair.

### 2.8 Palette map

| Element | Material | Hex |
|---|---|---|
| Painted stucco walls, bay sides | `Toy_cream` | f2ede3 |
| Cornice, parapet, belt course, bay caps, finials | `Toy_trim` | f3efe6 |
| Upper-floor windows | `Toy_glass` | 2a4d73 |
| Ground-floor storefront glazing, fire escapes, balcony rails | `Toy_ink` | 3a3530 |
| Retail base frame / plinth | `Toy_stone` | d9d2c2 |
| Retail sign fascia (the one saturated accent) | `Toy_navy` | 2c4a70 |
| Roof deck | `Toy_steel` | 9aa0a6 |
| Penthouse, mechanical | `Toy_roofd` | 45454a |
| Skylights, light-well glazing | `Toy_glassl` | 6f95b8 |
| Night: lit apartment windows | `Toy_gold_Glow` | caa64a |
| Night: sign fascia, entrance soffit | `Toy_sky_Glow` | 6db3d9 |

Neutral building (style bible §7): one dark accent (the storefront band) and one
saturated accent (the blue sign fascia). Nothing else competes. Note this is
*not* the SF painted-lady exception — the building is genuinely painted
near-white and stays in the neutral family.

### 2.9 Night state

Required. Residential profile: a **restrained scatter of warm lit apartment
windows** (roughly a third of them, never a full grid), the **entrance-court
soffit**, and — the hero — the **retail sign fascia** glowing along both street
faces, so the building reads as a lit plinth under a dark residential block.
Glow surfaces are thin panels proud of the opaque glazing, never the primary
surface (the app renders `_Glow` at ~12 % alpha by day).

### 2.10 Triangle budget

**≤ 14,000**, well inside the 27,000 landmark cap. The cost drivers are the eight
bays (four of them curved) and the parapet finials; everything else is planar.

### 2.11 Draft manifest entry

```json
{ "id": "500-van-ness", "file": "500-van-ness.glb",
  "anchor": [-122.4199220, 37.7804082], "targetHeightM": 17.0,
  "cat": 2, "name": "500 Van Ness Avenue", "estimated": true,
  "dims": [40.0, 41.8, 17.0], "tris": 0, "loadRadius": 2500 }
```

`cat` 2 = *Apartments* in `CATEGORY_LABELS` (`app/src/context.js`) — the parcel is
assessed as A15 multi-family residential, and the retail is a tenant of the base,
not the building's use. `loadRadius` takes the 2500 m floor from the default rule
(`max(2500, 17 × 30)` = 2500).

### 2.12 Integration — Case B

No `500-van-ness` id exists in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry **and a re-bake of
the affected tiles**, or the baked procedural block will intersect the GLB.
Proposed entry: `id: '500VanNess'`, lon/lat as above, `height: 17`,
**`exclude: 16`**.

That radius needs its own justification, because this is a **tight-neighbour
site** and `excluded()` in `pipeline/buildings.mjs` drops a footprint when *any*
of its ring vertices — not just its centroid — falls inside the radius:

| Distance from anchor | What is there |
|---|---|
| 10.3 m | our own nearest ring vertex (the entrance-court corner) → we are excluded ✓ |
| **17.7 m** | the **Courthouse**'s nearest surveyed vertex — the east party wall |
| 25.4 m | our own furthest ring vertex |
| 31.4 m | the next-nearest neighbouring building |

So the radius must sit **above ~10.3 m and below 17.7 m**. 16 m clears our own
footprint through its centroid and its two court vertices while leaving the
Courthouse block — which has no GLB of its own on `main` — standing. Sizing off
centroids instead would have deleted the Courthouse and left a hole where a 25 m
government building belongs. **Re-measure this against the actual bake input
before committing the registry entry** (the pipeline bakes Overture/OSM
footprints, which are not necessarily the ring measured here), and confirm with
`node pipeline/verify-rebake.mjs` + `node pipeline/audit.mjs`.

### 2.13 Open risks / what is not verified

1. **The 17.0 m crest** is the deck (LiDAR-measured, 15.48 m) plus a photo-read
   parapet. A facade drawing or a permit elevation could move it ±0.5 m.
   `estimated: true`.
2. **The east and north elevations** are inferred; they are party walls and no
   photograph of them exists from public space.
3. **The second interior light well** is read off one aerial image; its size and
   position are designed, not surveyed. Only the roof reads it.
4. **The architect and the building's history** were not found. Nothing in the
   model depends on them; REFERENCE.md carries the gap explicitly rather than
   repeating an unsourced attribution.
5. **`exclude: 16`** has only 1.7 m of margin to the Courthouse. It is the one
   number in this plan that must be re-measured against the bake input rather
   than trusted (see §2.12).
