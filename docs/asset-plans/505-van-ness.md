# 505 Van Ness Avenue — Governor Edmund G. "Pat" Brown Building

California Public Utilities Commission headquarters, San Francisco Civic Center.
Slug `505-van-ness`, manifest id `505-van-ness`, runtime status **new landmark**
(Case B: registry entry + tile re-bake required).

> **Identity note, read this first.** "Public Utilities Commission" at 505 Van
> Ness is the **California** PUC (a state agency), not the **San Francisco**
> PUC, whose headquarters is a different building at 525 Golden Gate Avenue
> (KMD Architects, LEED Platinum). The address given is unambiguous and this
> plan models the building at that address. If the SFPUC was intended, this
> whole plan is the wrong building — see §2.15.

---

## Part 1 — ready-to-run task prompt

> Build the SF-SIM miniature of **505 Van Ness Avenue (Governor Edmund G. "Pat"
> Brown Building)** as a validated GLB under `artifacts/505-van-ness/`.
>
> Read first, in this order: `AGENTS.md` (iron rules), `docs/styles/miniature-toy.md`
> (the artistic gate, in full), `.agents/skills/sf-asset-check/SKILL.md` (the
> technical contract). The reference implementation to mirror is
> `artifacts/380-brannan/` — same four deterministic scripts, same headless
> invocation, same report structure.
>
> **Re-verify §2.2–2.5 of this dossier before modelling.** Plans in this repo
> have been wrong before; if the model and the plan disagree, REPORT.md wins and
> the correction is written up prominently.
>
> Produce, in `artifacts/505-van-ness/`:
> `build_505_van_ness.py`, `render_505_van_ness.py`, `validate_505_van_ness.py`,
> `make_contact_sheet.py`, `505-van-ness.blend`, `505-van-ness.glb`, four
> elevations + top + day aerial + night aerial, `505-van-ness-contact-sheet.png`,
> `validation.json` (all-PASS), `REFERENCE.md` and `REPORT.md`.
>
> Hard requirements: geometry authored in true-world orientation (Blender +Y =
> north, +X = east — the loader never rotates); origin at the footprint bbox
> centre; `min z = 0`; **bbox top normalized to exactly 27.000 m** so the
> loader's `targetHeightM / measuredHeight` scale lands at 1.000; flat `Toy_*`
> materials only; a designed roof (the camera looks down); a required night
> state via `_Glow` shells proud of the opaque glazing; ≤ 20,000 triangles.
>
> Review the high three-quarter aerial FIRST and iterate on it before running
> the formal rig.

---

## Part 2 — research and design dossier

### 2.1 Identification

| Field | Value | Source |
|---|---|---|
| Address | 505 Van Ness Ave, San Francisco, CA 94102 | DGS building directory (official) — *measured/verified* |
| Official name | Governor Edmund G. "Pat" Brown Building | DGS building directory |
| Principal tenant | California Public Utilities Commission (HQ) | CPUC contact page; Commons photo captions |
| OSM object | `relation/1735766`, `name=State of California Building` | OSM API — *measured* |
| OSM tags | `building=government`, `building:levels=6`, `height=27 m` | OSM API |
| Completed | 1986 | secondary web sources — *inferred, single-sourced* |
| Architect | Skidmore, Owings & Merrill | secondary web sources — *inferred, single-sourced* |

### 2.2 Anchor and footprint — *measured*

Outer ring of `relation/1735766` pulled from the Overpass API, reprojected with
the app's tangent projection (`LON0 −122.4375`, `LAT0 37.77`), closed-ring
Douglas–Peucker simplified at ε = 0.6 m.

| Quantity | Value |
|---|---|
| Measured ring | 27 vertices, area **6,277 m²** |
| Simplified ring (modelled) | 18 vertices, area **6,263 m²** (−0.2 %) |
| Minimum-area OBB | 109.93 × 83.18 m at −170.75° |
| Axis-aligned extent | **113.4 m (E–W) × 93.4 m (N–S)** |
| **Anchor (model origin = ring bbox centre)** | **lon −122.4212915, lat 37.7804835** |

The plan **anchors on the ring bbox centre, not the OBB centre**. The building is
an L — a full-block northern bar with a southern wing along Van Ness — and the
two centres differ by (−3.35 m, +3.16 m). The bbox centre is the point the model
is actually built around and is verified to lie inside the footprint; the OBB
centre is reported only for continuity with the other plans.

Modelled ring, metres, x east / y north, origin at the anchor:

```
(-56.71, 26.04) (-52.84,  -0.05) (-13.69,  5.70) ( -5.33,-46.70)
( -3.92,-46.48) ( -4.18,-44.49) ( 15.79,-41.28) ( 15.44,-38.52)
( 30.75,-33.77) ( 39.99,-27.80) ( 43.60,-24.48) ( 50.20,-15.64)
( 55.65,  -1.71) ( 56.71,  6.36) ( 55.83, 16.53) ( 50.82, 46.71)
(-53.72, 29.68) (-56.10, 27.80)
```

Edge roles (outward-normal headings, true):

| Edge | Length | Normal | Reads as |
|---|---|---|---|
| 15→16 | 105.9 m | 350.8° | north elevation (long rear bar) |
| 0→1 | 26.4 m | 261.6° | west elevation, north wing |
| 2→3 | 53.1 m | 260.9° | west elevation, south wing (inner face of the L) |
| 1→2 | 39.6 m | 171.6° | south face of the north bar (the L notch) |
| 5→6 | 20.2 m | 170.9° | south elevation (McAllister side) |
| **7→14** | **~97 m of chord** | **162.8° → 80.6°** | **the bowed drum front** |
| 14→15 | 30.6 m | 80.6° | east elevation on Van Ness |

### 2.3 Height — *estimated, flagged*

**Target height 27.0 m.** OSM carries `height=27 m` with `building:levels=6`, and
unlike the known-bad cases in this repo (City Hall 30 m, St Mary's 18.9 m) the two
tags are mutually consistent: 27 m over 6 storeys is 4.5 m floor-to-floor, which
is right for a monumental civic office building and matches the storey rhythm
counted in the reference photographs (6 window bands above a raised plinth, then
a deep roof fascia).

No Wikidata height claim, architect statement or LiDAR figure was found for this
building, so **27.0 m is `estimated: true` in the manifest** — this is the one
number in the dossier that a later source could move. Eave vs crest: the 27.0 m
is taken as the **crest** (top of the roof fascia / mechanical penthouse); the
occupied roof deck sits at ≈ 24.5 m.

### 2.4 Orientation — *measured*

Authored in true-world orientation (+Y north, +X east), per the standing
orientation note in this directory: `placeGeneric()` never rotates, so real-world
heading wins over the contract's "front faces −Y". The **entrance faces ≈ 120°
(ESE)**, centred on the bowed front where it addresses the Van Ness / McAllister
corner plaza. This deviation from the −Y rule is recorded in REPORT.md.

### 2.5 Four elevations and the roof — *observed from photographs*

Reference: two CC BY-SA 4.0 photographs on Wikimedia Commons by *Mattnotmatte*
(2025-06-20), "CPUC HQ in San Francisco (Governor Edmund G Pat Brown Building)"
— *Front* and *Courtyard* — plus `File:Edmund G. Brown Building.jpg`.

- **Front (the bowed drum, ESE).** A broad convex curved facade in near-white
  warm-gray precast concrete. Heavy **rounded pilaster piers** run full height,
  dividing the curve into bays; between them sit horizontal ribbons of strongly
  blue-tinted glass, three per bay per floor, separated by flat spandrel panels.
  A deep **recessed central bay** interrupts the curve: within it, the **Great
  Seal of California** as a large polychrome medallion (pale blue field, tan and
  white figures) and, on the lintel band below, incised *STATE OF CALIFORNIA*.
- **The plaza.** A sweep of **concentric curved steps** descends from the
  entrance to the corner sidewalk, flanked by two **cylindrical drum pedestals**
  with rounded caps and by two flagpoles (US and California). Low curved
  retaining walls and street trees frame the sides. This is as much of the
  building's identity as the facade and is modelled.
- **Roof.** A **dark red-brown sloped metal fascia band** caps the drum and
  returns around the whole building — the single dark element in an otherwise
  pale composition, and the thing that gives the silhouette its lid. Behind it a
  flat roof carries mechanical penthouses.
- **Courtyard.** The ring encloses an interior light court (OSM inner ring, ≈ 39
  × 21 m). Its faces are fully glazed with a **faceted glass stair/lift tower**
  rising in the middle and warm yellow-orange spandrel bands — a strong,
  legible feature from the app's downward camera, so the court is modelled open
  with a glazed tower rather than roofed over.
- **North / west elevations.** Same pier-and-ribbon system, plainer, no recessed
  bay — *inferred* from the corner views; no dedicated photograph was found.

### 2.6 Recognition cues (the 3–5)

1. The great **bowed drum front** — the silhouette, and unmistakable in Civic Center.
2. The oversized **Great Seal of California** medallion in the recessed bay.
3. The **rounded-pier + blue-ribbon** facade rhythm wrapping the whole building.
4. The **concentric curved stair** and its two drum pedestals.
5. The **dark red-brown roof fascia** lid.

### 2.7 Massing recipe

One extruded body on the 18-vertex ring, the drum arc resampled to 14 segments
for a smooth landmark curve (style bible §4, low-seg curves 8–14). Six storey
bands from the plinth at 2.0 m to the roof deck at 24.5 m; fascia 24.5 → 26.2 m;
parapet to 26.5 m; the roof stair penthouse sets the crest at exactly 27.000 m.
Courtyard cut as an inner ring with its own glazed faces and a faceted tower.
Plinth, curved stair, drum pedestals and flagpoles at the ESE corner.

### 2.8 Palette map

| Element | Material | Hex |
|---|---|---|
| Precast piers, spandrels, plinth, stair | `Toy_stone` | d9d2c2 |
| Pier highlight / coping / lintel band | `Toy_trim` | f3efe6 |
| Ribbon glazing | `Toy_glass` | 2a4d73 |
| Courtyard glazing / seal field | `Toy_glassl`, `Toy_sky` | 6f95b8, 6db3d9 |
| Roof fascia lid | `Toy_rust` | a86444 |
| Roof deck, mechanical | `Toy_roofd`, `Toy_steel` | 45454a, 9aa0a6 |
| Recessed-bay shadow | `Toy_ink` | 3a3530 |
| Seal rim / courtyard spandrels | `Toy_gold` | caa64a |
| Night: lit windows, seal ring, entrance soffit | `Toy_glass_Glow`, `Toy_trim_Glow` | 6f95b8, f3efe6 |

The building is the neutral kind (style bible §7): one dark accent (the fascia),
one saturated accent (the seal). Nothing else competes.

### 2.9 Night state

Required. A restrained scatter of lit ribbon windows, the recessed entrance
soffit, and — the hero — the **seal ring**, so the identity survives after dusk.
Glow shells are thin panels proud of the opaque glazing, never the primary
surface (the app renders `_Glow` at ~12 % alpha by day).

### 2.10 Triangle budget

**≤ 20,000**, well inside the 27,000 landmark cap. The perimeter is long (~330 m)
so the pier count, not the detail, is the cost driver: ~52 piers at 2-segment
bevels plus six ribbon rings.

### 2.11 Draft manifest entry

```json
{ "id": "505-van-ness", "file": "505-van-ness.glb",
  "anchor": [-122.4212915, 37.7804835], "targetHeightM": 27.0,
  "cat": 18, "name": "505 Van Ness Avenue", "estimated": true,
  "dims": [113.4, 93.4, 27.0], "tris": 0, "loadRadius": 2500 }
```

`cat` 18 matches `city-hall`, the other Civic Center government building.
`loadRadius` takes the 2500 m floor from the default rule
(`max(2500, 27 × 30)` = 2500).

### 2.12 Integration — Case B

No `505-van-ness` id exists in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so integration needs a registry entry **and a re-bake of
the affected tiles**, or the baked procedural block will intersect the GLB.
Proposed entry: `id: '505VanNess'`, lon/lat as above, `height: 27`,
`exclude: 70` (the ring's furthest vertex is 60.1 m from the anchor; 70 m clears
the whole footprint without reaching City Hall across Van Ness or the Veterans
Building to the south).

### 2.13 Open risks / what is not verified

1. **The identity question** — CPUC (state) vs SFPUC (city). See the note at the
   top. This is the single largest risk in the plan and it is a routing question,
   not a modelling one.
2. **27.0 m height** is `estimated` — OSM-derived and photo-consistent, but not
   independently sourced.
3. **1986 / SOM** are single-sourced secondary claims and are not used for any
   geometry; they appear in REFERENCE.md as attribution only.
4. **North and west elevations** are *inferred* from the same facade system as
   the photographed sides.
5. The **courtyard inner ring** is taken from OSM at face value; its glazing
   colours come from one photograph looking up, so the spandrel banding is
   stylised rather than surveyed.
