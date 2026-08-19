# 1 Market Street (Southern Pacific Building) — SF-SIM asset plan

The **Southern Pacific Building** of 1916–17, "The Landmark @ One Market": Bliss &
Faville's eleven-storey Italian Renaissance headquarters block holding the whole
south corner of Market and Steuart, the last big building on Market Street before
the Ferry Building and the Embarcadero. It is a **U**, not a box — three deep wings
of Roman brick wrapped around a 55 x 36 m courtyard that opens toward Mission
Street, and that courtyard is now roofed by the glazed atrium of One Market Plaza.

Three things make it: the **cream terra-cotta two-storey arcaded base** with its
monumental arched Market Street portal and the balcony on brackets above it; the
**very fine punched-window rhythm** — a 2.25 m bay repeating thirty-eight times
across an 85 m frontage, which is what makes the mass read as a wall of brick
rather than a grid of glass; and the **enormous bracketed crowning cornice** over a
colonnaded attic storey, the deepest overhang on this stretch of Market.

From the app's camera it is also a **roof**: a U-shaped flat deck ringed by that
cornice, big rooftop plant enclosures, and the glass pyramid of the atrium sitting
in the court — the one thing at this end of Market that is interesting from above.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/1-market/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `1-market` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3948075, 37.7938412` (simplified-footprint AABB centre, measured) |
| Target height | **48.7 m** (rooftop plant crest, LiDAR modal); crowning cornice **46.1 m**, measured two ways; roof deck **44.6 m** |
| Footprint | 3,643.9 m2 eight-vertex **U**; 85.20 m (Market, NW) x 66.15 m (Spear SW / Steuart NE) overall, court 55.49 x 35.90 m open to the south-east |
| Triangle cap | 28,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 1 Market Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 1 Market Street — the Southern Pacific
Building, "The Landmark @ One Market", at the south corner of Market and Steuart in
San Francisco — and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/asian-art-museum/` — **the primary reference implementation.** Same
   problem: a monumental early-20th-century masonry block on a 45 deg downtown grid,
   a heavy classical base, a repeating punched-window shaft and a crowning cornice,
   all resolved at miniature scale. Its build script's elevation helpers are the
   skeleton to **adapt, not rewrite**.
8. `artifacts/300-brannan/` — secondary reference for the pilaster/bay helpers
   (`poly_edge`, `offset_polygon`, `wall_box`, `bay_spans`, `window_unit`,
   `glazed_elevation`) and for the "bounding-box top is the rooftop plant crest"
   height convention.
9. `docs/asset-plans/1-market.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- An **eleven-storey U-plan block** on the 45 deg downtown grid: three deep wings of
  red Roman brick around a courtyard that opens to the south-east. It is not a
  rectangle and it is not solid — the court is the reason this building looks
  different from every other slab on Market Street from above
- The **cream terra-cotta arcaded base**, two storeys tall, running the full Market,
  Steuart and Spear frontages: round columns / piers forming an open loggia, with a
  **monumental arched portal** at the centre of the Market elevation and a
  **projecting balcony on heavy brackets** directly above it
- The **fine punched-window rhythm**: a 2.25 m bay, thirty-eight of them across the
  85 m Market frontage, twenty-nine on each of the Steuart and Spear flanks. Small
  square-ish openings with cream sills in a brick field — the openings must stay
  *small relative to the brick*, or the building stops reading as 1916 masonry
- The **colonnaded attic storey**: a continuous run of paired terra-cotta
  colonnettes just under the crown, one pair per bay, reading as a light band
  between the brick shaft and the cornice
- The **crowning cornice**: a very deep bracketed overhang, the building's silhouette
  from every direction. Exaggerate its projection — this is where the semantic
  exaggeration budget is spent
- A designed roof: the U-shaped deck inside a continuous parapet, two large rooftop
  plant enclosures with fan banks on the Market wing (these set the 48.7 m crest),
  scattered vents and stair bulkheads
- The **glazed atrium roof filling the courtyard** — a hipped/pyramidal glass roof
  with a light frame, eaves well below the parapet, apex below the cornice. See
  "Why the atrium is in scope" below; it is not optional

## Research 1 Market Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the U-plan footprint, the WGS84 anchor and the real-world
orientation, and gather references covering:

- All three street elevations (Market NW, Steuart NE, Spear SW) and the two short
  Mission Street returns
- The courtyard elevations and the atrium roof from above
- Aerial and roof views (parapet, plant enclosures, the glass pyramid)
- Ground-level views day and night
- The **bay counts** — the dossier reads 38 on Market and 29 on each flank from a
  rectified Street View elevation, and those are the numbers most worth re-checking
- The height of the **atrium glazing**, which is the least certain number here

**Four source traps are already known and resolved in 2.1 and 2.15 — re-check them,
do not silently re-inherit the wrong value:**

1. **Wikipedia says 65 m (213 ft). It is wrong.** Two independent measurements put
   the crowning cornice at **46.0–46.1 m**: DataSF LiDAR `hgt_median` 46.12 m, and a
   Street View photogrammetric solve that gives 46.03 m. 213 ft over eleven storeys
   would be 19.4 ft per floor. Derivation and the LiDAR's own validation are in 2.1.
2. **The DataSF LiDAR maximum for this footprint is 114.92 m and must be rejected**
   — that is Spear Tower spilling over the shared boundary, not this building. The
   standard deviation is 5.57 m over 15,524 cells; 5.57 m of spread cannot contain a
   69 m step.
3. **OSM way/132238425 traces this building as a solid diamond with no courtyard**
   (5,544 m2, `height=60.05`). It is wrong about the plan *and* the height. The
   DataSF LiDAR footprint (`ynuv-fyni`, `mblr = SF3713006`, 3,879 m2) is the survey,
   and the assessor's 434,396 sq ft over eleven storeys independently confirms a
   ~3,670 m2 floor plate, i.e. the U, not the diamond.
4. **The courtyard belongs to the neighbouring parcel.** The atrium footprint is
   `mblr = SF3713007` (the tower lot), not SF3713006. Do not let that make you leave
   the court empty — see below.

## Why the atrium is in scope

The exclusion radius that removes this building's own procedural footprint
necessarily removes the atrium's too: the two rings **share a vertex 7.3 m from the
anchor**, so no radius can take one and spare the other (2.13). If the asset does
not carry the atrium roof, the finished scene has a 55 x 36 m hole in the middle of
the model showing bare terrain. Model it. It is also the best thing in this asset
from the app's downward-looking camera and the strongest night feature.

## Create a reference dossier

Write `artifacts/1-market/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides, the court and above; the 3–5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. Do not
commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from
the app's high three-quarter aerial camera, then simplify again.

This is a **landmark**, not a background block: it is one of the largest single
masses on the Embarcadero end of Market and the camera crosses it constantly on the
way to the Ferry Building. It still must not out-shout the Ferry Building or the
Bay Bridge — its job is to be the heavy brick shoulder they stand next to.

The hard call on this building is **window density**. Thirty-eight bays over 85 m is
a real, load-bearing observation: this facade's identity is a *fine* rhythm, and
halving it to nineteen fat bays would turn a 1916 office block into a 1970s one.
Keep the count; pay for it by making each window cheap (a recessed dark quad plus a
cream sill quad, no reveals). Do not spend triangles on window depth here — spend
them on the cornice, the base arcade and the roof.

Watch the dark-value budget. The brick is a mid-warm red and the window openings are
small; keep the openings at the mid-dark glazing value rather than `Toy_ink`, or the
elevations will read as grey static from the aerial camera.

The finished asset must be immediately recognizable as this corner, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single U-plan block: body, terra-cotta base and its arcade, base
entablature and balcony, all three street elevations, the two Mission Street
returns, the three courtyard elevations, the attic colonnade, the crowning cornice,
the roof deck, parapet, plant enclosures and vents, and the glazed atrium roof
filling the court.

Do not include unrelated surrounding city geometry: **Spear Tower and Steuart Tower
and their podium** (a separate 172 m / 111 m complex on the neighbouring lot, and
explicitly out of scope), Market Street, Steuart Street, Spear Street, Mission
Street, the F-line tracks and overhead wire, the street trees on all three
frontages, Embarcadero Plaza, traffic signals, the sidewalk, parked cars, people,
plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; at most 28,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The **Market
Street elevation faces north-west, bearing 315.2°**; the **Steuart Street elevation
faces north-east, 45.2°**; the **Spear Street elevation faces south-west, 225.2°**;
the two **Mission Street returns face south-east, 135.2°**. Build directly on the
measured footprint polygon in 2.3 rather than modelling an axis-aligned box and
rotating it. Record the measured headings in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the rooftop plant
enclosure cap) must land at exactly **48.7 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/1-market/build_1_market.py` (deterministic build script),
`artifacts/1-market/1-market.blend`, and `artifacts/1-market/1-market.glb`.
The script must rebuild the model reliably enough for future revision.

## Required review renders

Render the exact final geometry from controlled cameras: `1-market-top.png`,
`1-market-north.png`, `1-market-east.png`, `1-market-south.png`,
`1-market-west.png`, plus `1-market-contact-sheet.png`, at least one high
three-quarter aerial beauty render `1-market-aerial.png`, and a night render
`1-market-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection.
**The top view is the important one here** — it must clearly show the U, the
courtyard, the glazed atrium roof, the parapet ring and the plant enclosures. Place
the aerial camera north-west of the building so it sees the Market frontage, the
Steuart flank and into the court at once.

## Validate the exported GLB

Re-import `1-market.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Write `artifacts/1-market/validation.json` and
`artifacts/1-market/REPORT.md`.

The axis-aligned XY bounding box will be roughly **107.1 x 107.0 m** even though no
elevation is longer than 85.2 m — that is the expected consequence of a 45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "1-market",
  "file": "1-market.glb",
  "anchor": [
    -122.3948075,
    37.7938412
  ],
  "targetHeightM": 48.7,
  "cat": 3,
  "name": "1 Market Street (Southern Pacific Building)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/1-market.md`.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Building name | **Southern Pacific Building**; `alt_name` "The Landmark @ One Market" | OSM way/132238425; Wikipedia; Wikidata Q7570276 — measured |
| Address resolution | `1 MARKET ST` → block **3713**, lot **006** | DataSF EAS addresses (`ramy-di5m`); SF Planning ZA letter for 1 Market Street — measured |
| Date of construction | started **1916**, completed **1917** | Wikipedia; SF Assessor roll (`year_property_built = 1917`) — two independent sources agree |
| Architect | **Walter Danforth Bliss and William Baker Faville** (Bliss & Faville) | Wikipedia; noehill Bliss & Faville index — measured |
| Original occupant | Southern Pacific Railroad headquarters, from 1917 | Wikipedia |
| Storeys | **Eleven** | SF Assessor roll (`number_of_stories = 11.0`); SF Planning ZA letter ("Lot 006 … 11 stories"); Wikipedia's infobox says "12 floors" and its own body text says 11-storey — take 11 |
| **Architectural height (cornice crest)** | **46.1 m** | DataSF LiDAR `hgt_median` 46.12 m **and** an independent Street View photogrammetric solve at 46.03 m — **measured, two ways** |
| Rooftop plant crest | **48.7 m** | DataSF LiDAR `hgt_majority` (modal) 48.69 m — measured; this is the export's bounding-box top |
| Roof deck (behind parapet) | ~44.6 m | *inferred* — cornice crest less a ~1.5 m parapet/cornice depth |
| Height figure to reject | 65 m / 213 ft (Wikipedia infobox); 60.05 m (OSM `height` tag) | see 2.15 |
| Building area | 434,396 sq ft = 40,357 m2 | SF Assessor roll 2023–2025, lot 3713/006 — measured; ÷ 11 = **3,669 m2 per floor**, which is the U, not the 5,929 m2 outer diamond |
| Lot area | 38,051.62 sq ft = **3,535 m2** | SF Assessor roll — the parcel is itself U-shaped; the court is on lot 007 |
| Footprint | **3,879 m2** surveyed polygon (incl. cornice overhang); 3,643.9 m2 as simplified in 2.3 | DataSF building footprints (`ynuv-fyni`, `mblr = SF3713006`, `sf16_bldgid` 201006.0000435) — measured |
| OSM footprint (cross-check) | 5,544 m2 solid diamond, no court, `height=60.05`, `building:levels=12` | OSM way/132238425 — **wrong about the plan and the height**, see 2.15 |
| Courtyard | 55.49 x 35.90 m, open to the south-east | derived from the DataSF ring in building-local axes, 2.3 — measured |
| Atrium (One Market Plaza) | fills the court; `mblr = SF3713007`, 2,112 m2, LiDAR median 39.71 m, min 25.25 m, modal 27.20 m | DataSF `ynuv-fyni` `sf16_bldgid` 201006.0001118 — measured, but the polygon also covers the 6-storey podium, so the glazing height itself is *inferred*, see 2.15 |
| Neighbours (out of scope) | **Spear Tower** 43 storeys, 172 m (LiDAR median 172.41 m); **Steuart Tower** 27 storeys, 111 m, over a 6-storey podium; both 1976–79, Welton Becket Associates | Wikipedia (One Market Plaza); SF Planning ZA letter; SF Assessor lot 3713/007 (43 stories, 1979) — measured |
| Exterior material | Roman brick over a terra-cotta base; Italian Renaissance; Colorado yule marble lobby | Wikipedia — measured for the material, *observed* for the current colour |
| Bay rhythm | **2.25 m**, 38 bays on Market, 29 on each flank | measured off a rectified Street View elevation, 2.4 — the count is *inferred*, the 2.25 m pitch is measured |
| Frontage headings | Market **315.2°** (NW); Steuart **45.2°** (NE); Mission returns **135.2°** (SE); Spear **225.2°** (SW) | measured from the surveyed footprint polygon |
| Current use | Commercial office over ground-floor retail; Autodesk among the tenants | SF Assessor `use_definition = Commercial Office`; OSM POI node/8748507817 |

**How the height was settled, and why it is not 65 m.** Three lines of evidence,
none of which needs the others:

1. **LiDAR, validated inside its own tile.** DataSF `ynuv-fyni` is 2010 LiDAR. The
   footprint immediately south-east of this one (`sf16_bldgid` 201006.0001309) is
   **Spear Tower**, and its `hgt_median` is **172.41 m** against a published 172 m.
   An instrument that lands within 0.4 m on the tower next door is not wrong by 19 m
   on this building. Its reading here is `hgt_median` **46.12 m**, `hgt_mean` 45.71,
   modal 48.69, σ **5.57 m** over 15,524 cells, min 6.22 m, max 114.92 m.
2. **Photogrammetry, independent of the LiDAR.** Street View pano
   `9Ik_FfJfikwHnE_YlMOsRQ` on Market Street. The cornice silhouette across the whole
   Market frontage fits `tan θ = K·cos φ` with K = 4.0755 and a perpendicular foot at
   column 3096 of the 4096-wide equirect, residual **±0.05°** over 1,650 columns. The
   two silhouette corners sit 1,735 columns apart, so
   `d = L_c / (tan φ_N − tan φ_W) = 87.5 / 8.19 = 10.68 m` to the cornice line, and
   `H = 2.5 + 10.68 × 4.0755 = 46.03 m`. The camera's own reported position is not
   used anywhere in that solve.
3. **Arithmetic.** 434,396 sq ft over eleven storeys is a 3,669 m2 floor plate on a
   3,535 m2 lot — full-lot coverage, no tower element. Eleven storeys at 46.1 m is
   4.19 m per floor, right for a 1916 Class-A office with a two-storey giant-order
   base. 213 ft would be 5.90 m per floor.

The LiDAR **maximum of 114.92 m is rejected**: σ is 5.57 m, and Spear Tower's
footprint shares boundary geometry with this one. `peak_1st_m` 118.52 m less
`gnd_min_m` 3.29 m reproduces the maximum exactly, i.e. it is a first-return artefact
over the shared edge, not a mast on this roof.

The gap between `hgt_median` 46.12 and the modal 48.69 is read as **rooftop plant**:
the Market wing carries two large fan/cooling enclosures in the nadir imagery, and
48.69 m is 2.6 m above the cornice, which is what such an enclosure stands. The
export normalizes to that crest, per the `300-brannan` / `599-third` convention.

### 2.2 Sources

- `https://en.wikipedia.org/wiki/Southern_Pacific_Building` — name, architects, 1916–17,
  "E-shaped 11-storey", the Southern Pacific tenancy. **Its infobox height (65 m /
  213 ft) and floor count (12) are both wrong**; the body text's "11-story" is right.
- `https://en.wikipedia.org/wiki/One_Market_Plaza` — the three-building complex,
  Spear Tower 172 m / 43 storeys, Steuart Tower 111 m / 27 storeys, 1976, Welton
  Becket Associates, César Pelli 1996 renovation. Establishes what is **not** in scope.
- `https://sfplanning.org/sites/default/files/za/1%20Market%20Street.pdf` — SF Planning
  Zoning Administrator letter for One Market Plaza. Lot 006 = The Landmark, **11
  stories**, 434,396 sq ft; lot 007 = Spear Tower 43 stories + Steuart Tower 27
  stories over a 6-story podium. The primary source for the lot split.
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — the authoritative footprint polygon (`mblr = SF3713006`) and every height in 2.1,
  including the Spear Tower record that validates the instrument.
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property
  Tax Rolls), block 3713 lot 006 — 1917, 11 storeys, Commercial Office, 434,396 sq ft
  building area, 38,051.62 sq ft lot area. Lot 007 for the towers: 43 storeys, 1979.
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS Addresses) — `1 MARKET ST`
  and its unit addresses all resolve to `-122.394986, 37.793984`. Note this is the
  **address point**, not the building centre; it sits ~11 m north-west of the
  footprint's AABB centre. Use the measured anchor in 2.3.
- `https://www.openstreetmap.org/way/132238425` — cross-check footprint, `height=60.05`,
  `building:levels=12`, `roof:shape=flat`, `wikidata=Q7570276`. **Wrong about the plan
  and the height**; useful only for the name, the alt_name and the wikidata link.
  `way/132238424` ("One Market Plaza", `height=28`) is the adjoining podium, not this.
- Google Street View equirectangular panorama **`9Ik_FfJfikwHnE_YlMOsRQ`** on Market
  Street opposite the main portal, retrieved at zoom 3 (4096 x 2048). Source for the
  rectified elevation in 2.4, the 2.25 m bay pitch, the base arcade, the attic
  colonnade and the photogrammetric height in 2.1. Fetched keylessly as
  `https://streetviewpixels-pa.googleapis.com/v1/tile?cb_client=maps_sv.tactile&panoid=<ID>&x=&y=&zoom=3&nbt=1&fover=2`
  with a browser User-Agent and a `https://www.google.com/` referer (both required).
- Google satellite tiles at z20/z21 (`https://mt1.google.com/vt/lyrs=s&x=&y=&z=`) —
  the roof: the U, the courtyard, the glass pyramid over it, the two fan enclosures
  on the Market wing, the parapet ring. The z21 imagery over this block is markedly
  **off-nadir** — Steuart Tower shows its facade — so it is good for identifying roof
  furniture and bad for measuring plan positions. All plan geometry here comes from
  the DataSF polygon instead.
- Exa searches (19 Aug 2026): `"Southern Pacific Building 1 Market Street San Francisco
  architect height storeys"` restricted to `en.wikipedia.org, wikidata.org, emporis.com,
  skyscraperpage.com, sfplanning.org, noehill.com` — returned the Wikipedia articles,
  the SF Planning ZA letter and `noehill.com/architects/bliss_and_faville/one_market.asp`
  (architects and 1916, no dimensions). No source found that corroborates 65 m.

### 2.3 Orientation and placement

The building holds the **south corner of Market and Steuart**, one block from the
Ferry Building. Its **north-west** elevation fronts **Market Street**; its
**north-east** elevation fronts **Steuart Street**; its **south-west** flank fronts
**Spear Street**; on the **south-east** it presents two short returns to **Mission
Street** with the courtyard opening between them. Beyond that opening, on the
neighbouring lot, stand Spear Tower and Steuart Tower — out of scope, but they are
what the court faces, and the asset must not overlap them.

Measured DataSF footprint, simplified to eight vertices, in Blender coordinates
(metres, `+X` east, `+Y` north, **CCW**), already centred on the anchor
`-122.3948075, 37.7938412` (the axis-aligned bounding-box centre, which is what the
loader's origin convention needs):

```
(  -6.953, -53.483)   S corner — Spear St x Mission St
(   3.257, -43.356)   inner corner of the Spear wing's Mission return
( -22.025, -17.868)   Spear wing, court face
(  17.371,  21.210)   Market wing, court face — north-east end
(  42.653,  -4.278)   Steuart wing, court face
(  53.537,   6.518)   inner corner of the Steuart wing's Mission return
(   6.952,  53.482)   N corner — Market St x Steuart St
( -53.538,  -6.519)   W corner — Market St x Spear St
```

That ring encloses 3,643.9 m2 against the assessor's 3,669 m2 per-floor plate
(−0.7%) and against the survey's 3,879 m2 gross (−6%, which is the cornice and base
overhang the survey captures and the wall plane does not). The wall plane is set
**1.15 m inside** the DataSF outer ring on all three street faces, so the modelled
cornice can project back out to the surveyed line.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| W→N | 85.20 m | NW 315.2° | **Market Street front** — the portal, the balcony, 38 bays |
| N→(53.537, 6.518) | 66.15 m | NE 45.2° | **Steuart Street flank** — 29 bays |
| →(42.653, −4.278) | 15.33 m | SE 135.2° | Mission Street return, Steuart end |
| →(17.371, 21.210) | 35.90 m | SW 225.2° | courtyard face of the Steuart wing |
| →(−22.025, −17.868) | 55.49 m | SE 135.2° | courtyard face of the Market wing |
| →(3.257, −43.356) | 35.90 m | NE 45.2° | courtyard face of the Spear wing |
| →S | 14.38 m | SE 135.2° | Mission Street return, Spear end |
| S→W | 66.15 m | SW 225.2° | **Spear Street flank** — 29 bays |

Wing depths: the Market wing is **30.25 m** deep, the Spear wing **14.38 m** wide and
the Steuart wing **15.33 m** wide. The courtyard between them is **55.49 x 35.90 m**
and is open across its whole 55.49 m south-east side.

Because of the 45° heading the axis-aligned bounding box is ~107.1 x 107.0 m. That is
correct, and it makes this one of the largest-footprint landmarks in the manifest —
check the shared `BatchedMesh` headroom at integration (2.13).

**On the E versus the U.** Wikipedia calls the plan "E-shaped". The DataSF survey is
a clean **U** — one straight court face 55.49 m long with no middle wing — and the
assessor's floor plate agrees with the U to 0.7%. Build the U. If a 1917 plan turns
up showing a middle wing that has since been demolished, it is not there now.

### 2.4 What each side shows

Read from a **rectified elevation** built from pano `9Ik_FfJfikwHnE_YlMOsRQ`: the
equirect was resampled onto the Market wall plane at 8 px/m using the fitted
perpendicular foot and distance from 2.1, so positions along the facade and storey
bands are metric rather than eyeballed.

**North-west (Market Street), 85.20 m** — The front. Bottom to top:

- a **two-storey cream terra-cotta base**, 0 → ~13.0 m, an open loggia of round
  columns / rectangular piers running the full frontage;
- at the centre, a **monumental arched portal** roughly two bays wide, deeply
  coffered, with a carved tympanum;
- a **base entablature** at ~13.0–14.0 m carrying a balustrade and an inscription
  frieze, with a **projecting balcony on heavy scrolled brackets** directly over the
  portal;
- eight storeys of **red Roman brick** with small punched windows, cream sills, on a
  **2.25 m bay repeated 38 times**; a lighter terra-cotta string course and a run of
  small bracketed balconies interrupt the field at roughly the seventh floor;
- an **attic storey of paired terra-cotta colonnettes**, one pair per bay, reading as
  a continuous light colonnade;
- the **crowning cornice**, a very deep bracketed overhang with dentils and
  modillions, its top at **46.1 m**.

**North-east (Steuart Street), 66.15 m** and **south-west (Spear Street), 66.15 m** —
The flanks. Same base, same shaft, same colonnade, same cornice, wrapped
continuously; **29 bays** each at the same 2.25 m pitch, no portal. *Inferred* from
the Market rectification plus oblique Street View; neither flank was rectified.

**South-east (Mission Street), two returns of 15.33 m and 14.38 m** — Short end
faces, same treatment, with the courtyard opening between them. Beyond the opening
the towers rise; nothing of this asset should extend past the ring in 2.3.

**The courtyard, 55.49 x 35.90 m** — Three inward elevations in the same brick, but
plainer: no terra-cotta base, no colonnade, a simple punched-window field. *Inferred*
— no photograph of the court interior was found. Model it as a reduced version of the
street elevations, because the camera can see into it from the north-west but never
closely.

**Above** — The U-shaped deck sits inside a continuous parapet. Two large rooftop
plant enclosures with exposed fan banks stand on the **Market wing** (nadir imagery
shows them clearly, with shadows); smaller vents and stair bulkheads are scattered
over the same wing. Filling the court is the **glazed atrium roof of One Market
Plaza**: a hipped/pyramidal glass roof on a light frame, with radiating hip members
converging on an apex, its eaves well below the parapet line.

### 2.5 Recognition cues (ranked)

1. **The U and its glazed court** — from the app's downward camera this is the whole
   identity, and nothing else on this stretch of Market looks like it.
2. **The crowning cornice** — a deeper overhang than anything nearby; it is what makes
   the silhouette read as 1916 rather than 1976.
3. **The fine 2.25 m brick rhythm** — small windows in a big brick field.
4. **The cream terra-cotta base with the arched Market portal** and the balcony above it.
5. **The attic colonnade** — the light band that separates the brick from the crown.

### 2.6 Miniature translation

- **Keep** the U, the court, the cornice depth (exaggerate it by ~25%), the base
  arcade as real openings, the portal, the colonnade band, the 38/29 bay counts, the
  two roof plant enclosures, the atrium roof.
- **Simplify** the ornament: the cornice becomes a two-step chamfered band with a
  bracket rhythm implied by a notched underside, not modelled brackets; the
  colonnettes become square-section mullions with a cap; the portal's carving becomes
  a recessed arch head and a plain tympanum panel; the balcony becomes a slab on
  three chunky brackets.
- **Drop** window reveals (recessed quads only), the seventh-floor balconies (a
  string course instead), fire escapes, signage, roof railings, the F-line wire.
- **Exaggerate** the cornice projection and the base-storey height slightly, so the
  building reads as base / shaft / crown at a glance from 800 m up.

### 2.7 Massing recipe

Heights, all *inferred* from the rectified elevation and normalized so the cornice
crest lands on the measured 46.1 m:

| Element | From | To |
|---|---|---|
| Terra-cotta base (2 storeys, arcade) | 0.00 | 13.00 |
| Base entablature + balustrade | 13.00 | 14.00 |
| Brick shaft, 8 storeys at 3.55 m | 14.00 | 42.40 |
| Attic colonnade storey | 42.40 | 44.60 |
| Crowning cornice (projects 1.15 m) | 44.60 | **46.10** |
| Roof deck (behind parapet) | — | 44.60 |
| Rooftop plant enclosures (crest) | 44.60 | **48.70** |
| Atrium glazing: eaves | — | ~33.0 |
| Atrium glazing: apex | — | ~43.0 |

Build order: footprint ring → extrude the shaft solid → inset the base storeys and
cut the arcade openings as applied piers (**not** boolean recesses — see the
`sf3d` note in 2.15) → apply per-bay window quads and sill strips → applied
colonnade band → swept cornice ring → parapet + deck → roof furniture → atrium roof.

### 2.8 Materials and palette

| Surface | Material | Notes |
|---|---|---|
| Brick shaft | `Toy_brick` (warm mid-red) | the dominant value; must not go dark |
| Terra-cotta base, colonnade, cornice, sills, string course | `Toy_cream` | the light band that structures the mass |
| Window openings | `Toy_glassd` (mid-dark blue-grey) | small; do not use `Toy_ink` |
| Roof deck / parapet top | `Toy_roof` | |
| Plant enclosures, vents | `Toy_steel` | **not `Toy_roofd`**, which renders near-black in the app |
| Atrium glazing | `Toy_glass` + `Toy_glass_Glow` | the night hero |
| Atrium frame | `Toy_cream` | thin members only |

Take the exact palette names and values from `docs/styles/miniature-toy.md`; the
column above names roles, not literal identifiers.

**Night state.** One hero and two supports:

- hero: the **atrium roof** glows warm from within — a `_Glow` plane *under* the
  glazing, not a shell wrapping it (a closed glow shell reads as two alpha layers by
  day and tints the whole surface);
- support: the **base arcade** — a continuous warm band behind the loggia piers;
- support: a **sparse scatter of lit upper-floor windows**, not more than one bay in
  five, biased to the Market and Steuart elevations.

The crowning cornice is **not** lit. The `_Glow` materials' base colours must match
their daytime non-glow neighbours.

### 2.9 Top surface

The roof is a first-class elevation here. Inside the parapet ring: a flat deck on all
three wings; on the Market wing two rectangular plant enclosures (the taller one sets
the 48.7 m crest) with visible fan discs on top, a stair bulkhead, and a scatter of
small vents; on the flanks, vents only. Across the court, the atrium's glazed
hip roof with 4–6 radiating hip members meeting at an off-centre apex.

### 2.10 Scope

In: the U-plan block and everything attached to it, plus the atrium roof over the
court. Out: Spear Tower, Steuart Tower, the podium, all streets, trees, plaza,
vehicles and people.

### 2.11 Triangle budget

Cap **28,000**. Indicative split: shaft and wing solids ~1.5k; window quads and
sills (≈1,600 openings at 4 tris) ~6.4k; base arcade piers and portal ~3.5k;
base entablature, balcony and string course ~1.5k; attic colonnade (≈110 mullions)
~1.5k; crowning cornice ring (street + court, swept) ~4.5k; parapet and deck ~1.5k;
roof furniture ~2.5k; atrium roof and frame ~2.0k; glow shells ~1.0k.

If the count runs over, cut the courtyard elevations' window quads to a banded
treatment before touching anything on a street elevation.

### 2.12 Draft manifest entry

```json
{
  "id": "1-market",
  "file": "1-market.glb",
  "anchor": [
    -122.3948075,
    37.7938412
  ],
  "targetHeightM": 48.7,
  "cat": 3,
  "name": "1 Market Street (Southern Pacific Building)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'oneMarket'`, lon/lat as above, `height: 48.7`) and re-bake the affected
  tiles, or the baked procedural building on this exact footprint will intersect the
  GLB.
- **The exclusion window is measured and it is narrow — `exclude: 20`.** Distances
  from the anchor to the nearest vertex of every DataSF footprint in the block:

  | Footprint | Nearest vertex | What it is |
  |---|---|---|
  | 201006.0000435 | **7.3 m** | this building — must be dropped |
  | 201006.0001118 | **7.3 m** | the courtyard/atrium (lot 007) — shares the vertex, so it is dropped too |
  | 201006.0001309 | **35.6 m** | **Spear Tower, 172 m — must survive** |
  | 201006.0000212 | **35.6 m** | the podium / Steuart Tower — must survive |
  | 201006.0000590 | 67.9 m | next nearest |

  Any radius in `(7.3, 35.6)` works; **20 m** sits in the middle of that band. It is
  well inside the building's own 53 m half-diagonal, which is fine — `excluded()`
  drops a ring when *any* vertex falls inside, not when the whole ring does.
- **The atrium is unavoidable collateral, and that is why the asset carries its roof.**
  There is no radius that removes this building's footprint and spares the court's.
- **Verify against the real bake input, not this table.** `pipeline/buildings.mjs`
  runs `simplifyRing` at 0.6 m tolerance and gap-fills from Overture, so the ring the
  bake actually tests may not contain the 7.3 m vertex and Overture may contribute a
  *second* ring for the same building. Check `pipeline/data/buildings_datasf.geojson`
  and the Overture layer, then confirm with `pipeline/verify-rebake.mjs` — and note
  that verify-rebake compares per-cell counts and can report "dropped nothing" for a
  working exclusion; settle any disagreement by decoding the tile.
- `loadRadius`: the default formula gives `max(2500, 48.7 × 30) = 2500` m. Take the
  default. Do **not** set `alwaysLoaded`.
- **Check the shared landmark `BatchedMesh` headroom before integrating.** This is a
  large asset in a district that already holds many landmarks; the batch has
  overflowed before, and the symptom is a *different* landmark silently disappearing
  on each reload, not this one failing.
- **Batch mode applies** — this landmark is being built alongside the rest of the
  Embarcadero/Steuart family (110 Embarcadero, 121/131/165/169 Steuart, 8 Mission,
  the Audiffred Building, Pier 1, Pier 3, Hyatt Regency, Rincon Center). Stage 5 must
  end at a source-only branch with the bake discarded.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 48.7 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~107.1 x 107.0 m is expected)
- [ ] Triangles at or under 28,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the atrium underside, the base arcade band and the scattered lit
      upper bays; glow planes proud of opaque glazing, no closed glow shells
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] The top render shows the U, the court and the atrium roof unambiguously
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Wikipedia's 65 m is the single biggest trap in this dossier**, because it is the
  first number any search returns and it is repeated on the *Southern Pacific* page
  as well. It is rejected on three independent grounds in 2.1. If a further source
  turns up quoting 213 ft, treat it as the same figure propagating, not as
  corroboration — and check whether it is measuring the towers instead.
- **The LiDAR maximum (114.92 m) must not be used either.** σ 5.57 m over 15,524
  cells rules out a 69 m element; it is Spear Tower over the shared boundary.
- **The cornice/plant split is the least certain part of the height.** The measured
  46.1 m is the cornice; the 48.7 m export height rests on the LiDAR *mode* being
  rooftop plant, corroborated only by nadir imagery showing large enclosures on the
  Market wing. If a roof photograph turns up, re-normalize to it. If the plant turns
  out to be lower than the cornice, set `targetHeightM` to 46.1 and rebuild — do not
  leave the model normalized to a crest that is not there.
- **The atrium glazing height is inferred.** The atrium's own LiDAR record (median
  39.71 m, min 25.25 m, modal 27.20 m) covers both the glazed court *and* the
  6-storey podium next to it, so none of those three numbers is the glazing on its
  own. The plan's 33 m eaves / 43 m apex is a design decision constrained by "clearly
  below the 46.1 m cornice and clearly above the 27 m podium". Re-check it against any
  photograph of the court from above, and keep the apex below the cornice whatever
  happens — the atrium reading as *taller* than the building would be a worse error
  than a metre of pitch.
- **The bay counts are derived, not counted in a photograph.** 2.25 m is a measured
  pitch (autocorrelation over the rectified elevation, consistent at two different
  storey bands); 38 and 29 follow by division. Street trees occlude enough of the
  frontage that a direct count returned 32–34. Re-count before modelling.
- **The courtyard elevations are unphotographed.** They are modelled as a plainer
  version of the street elevations on the reasonable assumption that a 1916 light
  court got no terra cotta. If imagery shows otherwise, follow the imagery.
- **No boolean recesses.** The base arcade and the portal must be built from applied
  piers and lintels, not by subtracting prisms from a solid: a "recess" built as a
  solid prism swallows the opening it frames, and only the *night* render shows it.
- **Do not model One Market Plaza.** The complex's two towers are far more
  conspicuous than this building and dominate almost all photography of "1 Market
  Street". The asset is the 1917 brick block only. If a reference photo shows a white
  1970s tower, it is not this building.
- **Batch:** this asset is being built alongside the rest of the Embarcadero and
  Steuart Street family. Stage 5 must run in batch mode (source-only branch, bake
  discarded) or the landmarks' tile re-bakes will collide.
