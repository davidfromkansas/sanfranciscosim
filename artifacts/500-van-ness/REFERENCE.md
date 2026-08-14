# 500 Van Ness Avenue — reference dossier

**The Corinthian** — 1915 apartment building over a bank/retail base at the
north-east corner of Van Ness Avenue and McAllister Street, San Francisco Civic
Center. Manifest id `500-van-ness`. Built from `docs/asset-plans/500-van-ness.md`;
where this file and the plan disagree, **this file and REPORT.md win**.

> **Which address.** `500 Van Ness Ave` is the retail address of a building that
> spans **500–524 Van Ness**; the assessor and OSM file the parcel under **512
> Van Ness Ave** and name it **The Corinthian**. Same structure, Block 0766 Lot
> 006. It is not 505 Van Ness (the state office building across the avenue,
> planned separately as `505-van-ness`).

## Sources

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Parcel | Block 0766, Lot 006 (`mblr` SF0766006) | DataSF secured property roll | measured |
| Address of record | 512 Van Ness Ave, SF CA 94102 | same | verified |
| Retail address | 500–524 Van Ness Ave (Chase branch at 500) | commercial listing; branch directory | verified |
| Building name | The Corinthian | OSM `name`; rental listings | verified |
| Built | 1915 | assessor `year_property_built` | verified |
| Storeys / units | 4 storeys, 55 units, 128 rooms | assessor roll | measured |
| Use | A15 multi-family residential over ground-floor retail | assessor roll | verified |
| Footprint | `way/355209013`, 14 vertices, 1,231.9 m² | OSM / Overpass API | measured |
| Lot / LiDAR footprint area | 1,215 m² / 1,213 m² | assessor; 2010 city LiDAR | measured (cross-check) |
| Roof deck height | 15.48 m | 2010 city LiDAR `hgt_median_m` | measured |
| OSM `height` / `building:levels` | 15 m / 4 | OSM API | measured (tag) |
| **Crest** | **17.0 m** | deck + photo-read cornice/parapet/urns | **estimated** |
| Elevations, roof | see below | Google Street View panoramas (Dec 2024 Van Ness/McAllister, Jan 2025 Van Ness); Esri World Imagery z20 for the roof | observed |
| Architect | not found | — | unknown — no geometry depends on it |

## Geometry as built

| Quantity | Value |
|---|---|
| Anchor (model origin) | **lon −122.4199220, lat 37.7804082** |
| Anchor derivation | bbox centre of the measured footprint ring |
| Footprint ring | 8 verts after ε = 0.3 m closed-ring Douglas–Peucker; area 1,230.1 m² vs 1,231.9 m² surveyed (−0.15 %) |
| Footprint extent | 40.0 m (E–W) × 41.8 m (N–S); min-area OBB 34.8 × 37.0 m at −171.22° |
| Grid rotation | 8.8° anticlockwise off compass north (the Civic Center grid) |
| **Asset bbox** | **43.29 × 45.10 × 17.000 m** — 1.45 m wider than the footprint on every side because the cornice overhangs that far; the overhang is symmetric so the bbox centre still sits on the footprint centre |
| Entrance heading | **261.6° true (W)**, at the back of the Van Ness court |
| Entrance court | the OSM notch itself: 6.86 m wide × 7.53 m deep, carved above the retail base |
| Second light well | 7.0 × 5.6 m at (+3.0, +1.0) local — designed from one aerial, not surveyed |

### Vertical scheme

| Datum | z (m) |
|---|---|
| Grade | 0.0 |
| Shopfront band | 0.70 → 3.55 (recessed 0.12–0.36 m) |
| Sign fascia | 3.72 → 4.52 |
| Top of retail base / floor-2 level | 4.70 |
| Belt course | 4.55 → 4.95 |
| Residential storey height (3 floors) | 3.60 |
| Window sill / head within each floor | +1.05 / +2.75 |
| Bay windows | 4.95 → 15.50, projecting 1.30 m |
| Roof deck | 15.50 |
| Bracket band / cornice | 15.02 → 15.50 / 15.50 → 16.20 (projecting 1.45 m) |
| Parapet | 16.20 → 16.60 |
| Parapet piers | 16.60 → 16.85 |
| **Crest (urns + raised pediment panels)** | **17.000** |

The crest is normalized to exactly 17.000 m by scaling vertex data (not object
transforms) so the loader's `targetHeightM / measuredHeight` lands on 1.000.

## Design decisions

1. **The oriels are the building.** Eight bay windows over floors 2–4,
   alternating rounded (segmental bow, 10 segments) and square, two per Van Ness
   pavilion and four along McAllister. The first review pass authored them at the
   real ~0.9 m projection and they vanished at the app's camera; they ship at
   **1.30 m** (style bible §9, semantic scale). The cornice was pushed to a 1.45 m
   projection so it still caps them.
2. **The court is the OSM notch, not an invention.** The Van Ness front reads as
   two equal pavilions in every photograph, and the surveyed ring explains why:
   there is a 6.9 × 7.5 m rectangular notch cut into that side, centred on the
   facade to within 0.2 m. It is carved **above the retail base only** — the
   shopfronts run continuously to the kerb, which is what the Street View
   captures show and what makes the plinth read as one dark band.
3. **One dark accent, one saturated accent.** The recessed `Toy_ink` shopfront
   and the `Toy_navy` sign fascia are the only non-neutral surfaces; everything
   above the belt course is cream and trim (style bible §7). This is *not* the
   SF painted-lady exception — the building really is painted near-white.
4. **Fewer, chunkier parapet elements.** The first pass ran 19 thin finials
   along the parapet and they read as noise from the aerial. Ship: 12 chunky
   piers with urns, plus one raised pediment panel centred on each of the three
   show faces, all landing on the same 17.0 m crest plane.
5. **The roof is one cluster, not a scatter.** Penthouse + three vent pipes in
   one group, a plant room, a skylight pair, a hatch (style bible §10). The first
   pass sprayed twelve lone vents across the deck.
6. **Bevel only real edges.** The generic `bevel()` helper here filters to edges
   whose two faces meet at more than 18°. Bevelling every edge also rounds the
   interior triangulation of the n-gon roof cap left by the light-well boolean,
   which drew bright creases straight across the deck. This also cut the asset
   from 10,562 to 9,246 triangles (9,522 with the shopfront piers added).
7. **Party walls stay plain.** The east and north faces abut neighbours (the
   Courthouse block is 17.7 m from the anchor) and carry no bays, no fire
   escapes and no windows — they are inferred, and inventing detail there would
   be inventing evidence.

## Night state

Hero: the `Toy_sky_Glow` sign fascia running the whole plinth, so the building
reads as a lit base under a dark residential block. Supporting: the entrance-court
soffit, and 14 `Toy_gold_Glow` shells on a deterministic ~30 % of the apartment
windows and bays. All glow surfaces are thin panels proud of the opaque glazing —
the app draws `_Glow` in a separate unlit layer at `0.12 + 0.95·uNight` opacity,
so a primary surface authored as glow would be half-transparent by day.

## Contract

Flat `Toy_*` materials only, no textures, no transparency, no cameras/lights/
animation, transforms applied, min z = 0, XY centred on the footprint, authored
in true-world orientation (+Y north, +X east) because `placeGeneric()` never
rotates. The "front faces −Y" clause of the contract is deliberately not honoured
— real-world heading wins (AGENTS rule 5, and the standing orientation note in
`docs/asset-plans/README.md`).
