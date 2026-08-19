# 300 Brannan Street — SF-SIM asset plan

The **Blinn Estate Building** of 1912: a six-storey reinforced-concrete wholesale
furniture warehouse holding the whole east corner of Second and Brannan, and the
tallest thing on this block by a wide margin. Its neighbours in the scene are two-
and three-storey boxes; this is the one that gives the South Park edge of SoMa a
wall. Three things make it: the **canted corner** cut across the Second/Brannan
intersection and carrying one window bay per floor, the **light pilaster grid over
dark deeply-recessed bays** of huge multi-lite industrial sash, and the **charcoal
two-storey-tall base** the 2008 renovation gave it, with segmental-arched openings
on Second Street.

It is a South End Historic District *contributor* — the district's own
character-defining list ("rectangular-massed, utilitarian, rough-textured,
earth-tone-coloured concrete structures with rhythmically spaced and deeply
recessed fenestration … flattened arch window treatment … abstract pilaster-like
elements") reads as a specification for this building.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/300-brannan/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `300-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3925543, 37.7818313` (simplified-footprint AABB centre, measured) |
| Target height | **25.2 m** (rooftop plant/elevator penthouse crest); parapet **21.34 m** = 70 ft, surveyed; roof deck **20.84 m**, LiDAR |
| Footprint | 1,136.5 m2 seven-vertex ring; 28.18 m (Second St, NE) x 27.73 m (Brannan, SE) x 30.03 m (Stanford, SW) x 36.60 m (NW party) + a 5.05 m canted east corner |
| Triangle cap | 15,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 300 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 300 Brannan Street — the Blinn Estate
Building, at the east corner of Second and Brannan in San Francisco — and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/500-third/` — **the reference implementation.** 500 Third Street is
   the same building type at the same altitude of abstraction: a big concrete
   industrial loft on the 45 deg SoMa grid, one tall charcoal storefront floor under
   identical upper floors of steel-sash window grid, pilaster strips, flat parapet,
   rooftop bulkhead crest, restrained night state. Its `build_500_third.py` is the
   script skeleton to **adapt, not rewrite** — the footprint/edge helpers
   (`poly_edge`, `offset_polygon`, `wall_box`, `bay_spans`, `pilasters`,
   `window_unit`, `glazed_elevation`) all carry over. `artifacts/599-third/` is the
   secondary reference for the penthouse-crest height convention.
8. `docs/asset-plans/300-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- A **six-storey** rectangular concrete block filling its whole corner lot, flat
  roof, continuous parapet — visibly the tallest building on its block
- The **canted corner** across the Second/Brannan intersection: a ~5 m diagonal
  face carrying **one window bay per floor**, with a rounded soffit return where
  the base cornice wraps it. This is the building's signature and the one place
  semantic exaggeration is spent
- The **light pilaster grid**: continuous light-toned pilaster strips running the
  full height of both street elevations, framing **dark, deeply recessed** window
  bays — the tonal alternation is the whole facade identity
- **Huge multi-lite industrial steel sash** filling nearly the whole bay width
  (landscape-to-square, not punched holes)
- The **dark charcoal base**: one very tall ground storey, capped by a heavy
  projecting cornice band that wraps all three exposed elevations and the cant
- **Segmental (flattened) arch heads** on the Second Street ground-floor openings,
  one of which is a roll-up loading bay
- A black steel **fire escape** on the Brannan elevation
- A designed roof: parapet ring, the elevator/stair penthouse cluster slightly north
  of centre (the crest), a low mechanical platform south of it, scattered vents

## Research 300 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor and the real-world
orientation, and gather references covering:

- Both street elevations (Second and Brannan), the canted corner face, and the
  Stanford Street (south-west) flank
- Aerial and roof views (penthouse cluster, vents, parapet)
- Ground-level views day and night
- The **bay count** of each elevation — the dossier reads 6 on Second, 6 on
  Brannan, 1 on the cant from May-2025 Street View, and that is the single number
  most worth re-counting
- Whether the **north-west (block-interior) elevation** is a blank party wall for
  its full length, or whether its upper storeys carry windows above the
  neighbouring roofs

**Three source traps are already known and resolved in 2.1 and 2.15 — re-check
them, do not silently re-inherit the wrong value:**

1. OSM way/112758589 traces this building as a **clean 37.7 x 29.8 m rectangle
   with no canted corner**. It is a Bing trace and it is wrong about the corner.
   The DataSF LiDAR-derived footprint (`ynuv-fyni`, `mblr = SF3775008`) is the
   survey, and May-2025 Street View shows the cant plainly.
2. The DataSF ring's raw corner edge is **8.09 m** long because the surveyed corner
   sits ~2.2 m proud of the Second Street wall plane. The **flush** chamfer chord —
   what you should model — is **5.05 m**. Both readings are derived in 2.3.
3. OSM `height=21` and the DataSF LiDAR median 20.84 m are the **roof deck**, not
   the crest. The architectural height is the surveyed **70 ft (21.34 m)** parapet;
   the export's bounding-box top is the rooftop plant crest at **25.2 m**.

## Create a reference dossier

Write `artifacts/300-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides, the cant and above; the 3–5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. Do not
commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from
the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building with landmark presence** in the style bible's detail
budget (§21): it earns a real window grid and a designed roof because it is the
tallest thing for two blocks and the camera passes over it constantly, but it is
not a monument and must not out-shout Oracle Park or the Bay Bridge behind it.

Watch the dark-value budget. Roughly a quarter of this building's surface is
genuinely near-black in life (the base, the recessed bays). The app's lighting is
flatter than the Blender review rig — keep the recesses at the mid-dark
`Toy_roofd` value rather than pushing them to `Toy_ink`, and check the aerial
render before committing to any darker choice.

The finished asset must be immediately recognizable as this corner, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single block: body, base and base cornice, all four elevations plus the
cant, pilasters, window bays, parapet, fire escape, roof deck and roof furniture.

Do not include unrelated surrounding city geometry: Second Street, Brannan Street,
Stanford Street, the neighbouring 577 Second Street and 318 Brannan buildings, the
street trees on both frontages, traffic signals, the sidewalk, the temporary
scaffolding visible in 2025 imagery, parked cars, people, plinths, cameras or
lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; at most 15,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The **Second
Street elevation faces north-east, bearing 45.2°**; the **Brannan Street elevation
faces south-east, bearing 135.5°**; the **canted corner faces east, bearing 95.1°**;
the **Stanford Street flank faces south-west, 225.5°**; the **party wall faces
north-west, 315.1°**. Build directly on the measured footprint polygon in 2.3
rather than modelling an axis-aligned box and rotating it. Record the measured
headings in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the rooftop
penthouse cap) must land at exactly **25.2 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/300-brannan/build_300_brannan.py` (deterministic build script),
`artifacts/300-brannan/300-brannan.blend`, and `artifacts/300-brannan/300-brannan.glb`.
The script must rebuild the model reliably enough for future revision.

## Required review renders

Render the exact final geometry from controlled cameras: `300-brannan-top.png`,
`300-brannan-north.png`, `300-brannan-east.png`, `300-brannan-south.png`,
`300-brannan-west.png`, plus `300-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `300-brannan-aerial.png`, and a night render
`300-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
the top view must clearly show the parapet ring, the penthouse cluster and the vent
scatter. The `east` render is the important one here — it looks straight down the
canted corner's outward normal, which is this building's subject. Place the aerial
camera to see the cant and both frontages at once.

## Validate the exported GLB

Re-import `300-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Write `artifacts/300-brannan/validation.json` and
`artifacts/300-brannan/REPORT.md`.

The axis-aligned XY bounding box will be roughly **45.8 x 47.3 m** even though no
elevation is longer than 36.6 m — that is the expected consequence of a 45°
real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "300-brannan",
  "file": "300-brannan.glb",
  "anchor": [
    -122.3925543,
    37.7818313
  ],
  "targetHeightM": 25.2,
  "cat": 3,
  "name": "300 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/300-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Building name | **Blinn Estate Building** | Page & Turnbull, South End Historic District, building data form — **measured** |
| Address resolution | `300 BRANNAN ST` → parcel **3775008** (block 3775, lot 008) | DataSF EAS address layer (`ramy-di5m`) — measured |
| Date of construction | **1912** | Page & Turnbull survey; SF Assessor secured roll 2025 (`year_property_built = 1912`) — two independent sources agree |
| Architect | **Charles C. Frye & George A. Schastey**; Alvin E. Horlein, engineer | Page & Turnbull survey — measured |
| Original use / tenant | Wholesale furniture and carpet warehouse; Peck & Hills Furniture Co., then Wm. G. Volker & Co. | Page & Turnbull survey |
| Storeys | **Six** | Page & Turnbull survey; SF Assessor roll (`number_of_stories = 6.0`); confirmed by Street View |
| **Height** | **70 ft = 21.34 m** | Page & Turnbull survey — the architectural (parapet) height, **measured** |
| Construction / exterior | Reinforced concrete frame, **stucco** exterior | Page & Turnbull survey; LoopNet/CompStak listings agree on "reinforced concrete" |
| Style / status | "Commercial"; **Contributory** to the South End Historic District; NR status 3D | Page & Turnbull survey |
| Building area | 68,884 sq ft (2025 roll); 67,792 sq ft rentable | SF Assessor roll; CompStak — 6 x 1,136 m2 gross reconciles |
| Lot area | 12,300 sq ft = **1,142.7 m2** | SF Assessor roll — within 0.3% of the surveyed footprint, i.e. **full-lot coverage** |
| Footprint | **1,139.8 m2** surveyed polygon; 1,136.5 m2 as simplified in 2.3 (−0.3%) | DataSF building footprints (`ynuv-fyni`, `mblr = SF3775008`) — measured |
| OSM footprint (cross-check) | 1,123 m2, 37.71 x 29.78 m clean rectangle | OSM way/112758589 (`height=21`) — agrees on area within 1.5%, **wrong about the corner**, see 2.15 |
| Roof deck height | **20.84 m** above grade | DataSF LiDAR `hgt_median_m` (majority 20.82, mean 20.91, σ 1.35 over 4,591 cells) — measured |
| LiDAR maximum | 25.67 m | DataSF LiDAR `hgt_maxcm` — the rooftop plant crest, see 2.15 |
| Ground elevation | 11.64–12.60 m (NAVD88), σ 0.22 m | DataSF LiDAR `gnd_min_m` / `gnd_mediancm` — the app's terrain handles this, not the asset |
| Renovation | 2008 (the charcoal base and current lobby); Fennie & Mehl Architects on later permits | LoopNet/Showcase/Cityfeet listings; openpermitdata.com |
| Frontage headings | Second St front faces **45.2°** (NE); Brannan front **135.5°** (SE); cant **95.1°** (E); Stanford flank **225.5°** (SW); party wall **315.1°** (NW) | measured from the surveyed footprint polygon |
| Current use | Creative office over ground-floor restaurant/retail; South Park Animal Hospital at street level | OSM POI nodes; CompStak tenant list; May-2025 Street View ("FOR LEASE", Colton Partners) |

### 2.2 Sources

- `https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf` —
  Page & Turnbull, *National Register Certification: South End Historic District*
  (26 June 2008). Appendix A2 building data form for 300 Brannan Street is the
  **primary source** for the name, architect, date, storeys, 70 ft height,
  construction type and exterior material. Section V is the district's
  character-defining-features list quoted in the header.
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS Addresses) — address → parcel
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) —
  the authoritative footprint polygon and the 20.84 m / 25.67 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property
  Tax Rolls) — 1912, 6 storeys, industrial use, lot and building area
- `https://www.openstreetmap.org/way/112758589` — cross-check footprint, `height=21`
- Google Street View, **capture May 2025**, panoramas at the Second/Brannan
  intersection (`37.781857,-122.392039`), on Brannan opposite the frontage
  (`37.781665,-122.392344`), and on Second Street north-west of the corner
  (`37.782221,-122.392513` and `37.782068,-122.392320`) — the current paint scheme,
  the canted corner, the bay counts, the segmental arches and the fire escape.
  Retrieved as `https://maps.google.com/maps?q=&layer=c&cbll=<lat>,<lon>&cbp=12,<heading>,0,0,<zoom>`.
- KartaView sequences 2057142 (24 Nov 2019), 1352479 (14 Mar 2019) and several
  2016 community drives on Brannan and Second — the 2019 frames confirm the
  charcoal base, the projecting entrance canopy, the cylindrical wall lanterns and
  the etched **300 BRANNAN** storefront signage. Note that most of the 2016
  sequences at this corner photograph **301** Brannan (the red-brick 1909 Crane
  Company Building, Lewis P. Hobart) on the opposite side of the street — do not
  mistake it for this building.
- Esri World Imagery (z20 nadir, ~2023 vintage) — flat dark membrane roof inside a
  continuous parapet, the penthouse cluster north of centre with its shadow, a low
  light-toned mechanical platform south of it, a round tank west of the cluster,
  pipe runs toward the south corner. No tree canopy overhangs the roof.
- LoopNet 16830204 / CompStak / Showcase / Cityfeet listings — "reinforced concrete",
  6 stories, 1912, renovated 2008, 67,792 sq ft, class B creative office. *Observed
  (listing data)*; the listings' own "footprint" figure is gross building area, not
  a footprint, and the 1926 date that appears in one Exa summary of the district PDF
  is a summarisation error — the PDF itself says 1912.

### 2.3 Orientation and placement

The building holds the **east corner** of Second and Brannan and covers its entire
lot. Its north-east elevation fronts **Second Street**; its south-east elevation
fronts **Brannan Street**; the two meet in a **canted corner** across the
intersection; its south-west flank faces **Stanford Street**, the 8 m alley that
runs through to Townsend; its north-west side is a lot-line party wall against
577 Second Street (a lower light-stucco building) and, further along, 318 Brannan.

Measured DataSF footprint, simplified to seven vertices, in Blender coordinates
(metres, `+X` east, `+Y` north, **CCW**), already centred on the anchor
`-122.3925543, 37.7818313` (the axis-aligned bounding-box centre, which is what the
loader's origin convention needs):

```
(   3.036,  23.634)   N corner — Second St x NW party line
( -22.883,  -2.212)   W corner — NW party line x Stanford St
(  -1.837, -23.634)   S corner — Stanford St x Brannan St
(   1.839, -20.035)   notch, stepping 1.19 m in from the Brannan wall plane
(   2.660, -20.830)   notch, stepping back out — start of the Brannan frontage
(  22.437,  -1.398)   south end of the canted corner
(  22.883,   3.629)   north end of the canted corner
```

That ring encloses 1,136.5 m2 against the survey's 1,139.8 m2 (−0.3%). The
discarded vertices are sub-1.2 m jogs in the Second Street wall plane, plus the
corner-bay projection discussed below. The 5.14 x 1.19 m notch at the south corner
is kept because it is a real setback at the Stanford/Brannan corner, not noise.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| N→W | 36.60 m | NW 315.1° | party wall against 577 Second / 318 Brannan |
| W→S | 30.03 m | SW 225.5° | **Stanford Street flank** (service side) |
| S→notch→Brannan start | 5.14 + 1.14 m | — | the south-corner setback |
| →cant south end | 27.73 m | SE 135.5° | **Brannan Street front** |
| cant | 5.05 m | E 95.1° | **the canted corner** |
| →N | 28.18 m | NE 45.2° | **Second Street front** |

**On the two readings of the cant.** The raw DataSF ring's corner edge runs almost
due north–south for **8.09 m**, but its two ends sit 2.18 m and 0.98 m *proud* of
the Second Street and Brannan wall planes respectively — the survey has captured a
shallow projecting corner bay (or a pilaster pair) rather than a flat chamfer.
Intersecting the cant line with the two facade lines gives the **flush** chamfer
chord: **5.05 m**, from `(22.437, −1.398)` to `(22.883, 3.629)`. 5.05 m is also what
the nadir imagery measures across the corner parapet, and it is exactly one window
bay wide in May-2025 Street View. **Model the 5.05 m flush chamfer.** If a later
photograph clearly shows the corner projecting, add the projection as a 0.2 m
pilaster pair rather than re-cutting the footprint.

Because of the 45° heading the axis-aligned bounding box is ~45.8 x 47.3 m. That is
correct.

### 2.4 What each side shows

**South-east (Brannan Street), 27.73 m** — Documented in May-2025 Street View and
2019 KartaView. One very tall charcoal ground storey with large rectangular
storefront openings, a projecting flat entrance canopy near the middle, light metal
**300** numerals, and cylindrical wall lanterns; above it a heavy projecting cornice
band; then five upper floors of light pilaster strips framing dark recessed bays of
big multi-lite steel sash. A black steel **fire escape** zig-zags from the second
floor to the parapet roughly a third of the way along from the Stanford end. The
south-westernmost ~5 m of the frontage steps back 1.2 m (the 2.3 notch).

**East (the canted corner), 5.05 m** — The identity. One window bay per floor in
the same rhythm as the frontages, over a charcoal base whose cornice returns around
the cant with a rounded soffit. In 2025 imagery a recessed corner entrance sits
under it, behind temporary scaffolding.

**North-east (Second Street), 28.18 m** — The service-and-entry face. Same five-floor
pilaster grid above, but its ground floor carries a run of **segmental
(flattened) arch** openings deeply recessed into the charcoal base — the district's
signature detail — one of which is a **roll-up loading door** with a ramp, and one a
stepped entrance with railings. The 2nd Street face is in shadow most of the day
and reads much darker than the Brannan face in photographs; that is lighting, not
paint.

**South-west (Stanford Street), 30.03 m** — A service flank on a narrow alley. Plain
stucco with a simpler, sparser version of the same window rhythm and no pilaster
capitals. Not photographed at street level in any source consulted; treat its bay
count as *inferred*.

**North-west (party wall), 36.60 m** — A lot-line wall against 577 Second Street and
318 Brannan, both of which are lower (8–18 m), so its upper storeys stand clear and
are visible from the app's aerial camera. Model it as a finished, quiet stucco plane
with at most a sparse scatter of small punched openings on the top two floors. Do
not invent a full window grid here.

**Top** — A flat dark membrane roof inside a continuous parapet. Nadir imagery shows
the **penthouse cluster just north of the roof centre** — two bright box forms with a
clear shadow, the taller of them the elevator/stair overrun and the crest — a low
light-toned mechanical platform immediately south of it, a round tank to its west,
a scatter of small vents, and two or three pipe runs toward the south corner. The
street-facing thirds of the deck are comparatively clean.

### 2.5 Recognition cues (ranked)

1. **The canted corner** carrying one window bay per floor across the Second/Brannan
   intersection — nothing else on this block does this
2. **Six storeys** where every neighbour is two or three — the block's wall
3. The **light pilaster grid over dark recessed bays**: a strong vertical
   light/dark alternation across both frontages
4. The **charcoal base with its heavy projecting cornice**, wrapping the cant
5. **Segmental-arched** ground-floor openings on Second Street; the black fire
   escape on Brannan

### 2.6 Miniature translation

**Preserve**

- The single full-lot volume, the real 45° heading, the canted corner and the
  south-corner notch
- The two-tone split: light pilaster/wall field, dark base and dark recessed bays
- Six-storey proportions: one tall ground floor under five equal upper floors
- The bay rhythm — 6 / 1 / 6 on Second, cant, Brannan

**Simplify / exaggerate**

- The multi-lite sash becomes one recessed glazed panel per bay with a light frame,
  not an individually modelled muntin grid
- The pilaster capitals become a single stepped block at the parapet, not moulding
- The fire escape becomes one flat zig-zag ladder-and-landing form, ~3 boxes deep
- The segmental arches become a shallow arched head cut into the base recess
  (6–8 segment curve), on Second Street only
- The base cornice is **thickened** to ~0.55 m deep so it survives at thumbnail size
  and reads all the way around the cant — this is the one place semantic
  exaggeration is spent, because the cornice line is what makes the cant read as a
  cant from the air
- Signage, lanterns, canopies, address numerals, scaffolding and street trees all
  disappear
- The roof plant becomes: one penthouse (the crest), one lower bulkhead, one low
  mechanical platform, one round tank, three small vents, two pipe runs

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=20.84, `Toy_stone`. Its top cap is
   the roof deck (`Toy_roofd`).
2. Base, z=0 to z=5.00: a `Toy_ink` skin 0.06 m proud on the three exposed
   elevations and the cant, with the ground-floor openings recessed 0.30 m into it —
   rectangular on Brannan, **segmental-arched** on Second Street, one bay of Second
   Street replaced by a `Toy_steel` roll-up door.
3. Base cornice: a continuous `Toy_ink` band z=4.85 to z=5.40 projecting 0.55 m,
   mitred round the cant with a chamfered underside; `Toy_stone` top face.
4. Pilasters: `Toy_stone` strips 0.85 m wide, 0.20 m proud, running z=5.40 to
   z=20.30 at every bay division on Second Street (7 strips), the cant (2) and
   Brannan (7); simpler 0.55 m strips on Stanford. Each terminates in a `Toy_trim`
   stepped capital block in the top 0.45 m.
5. Upper floors: five floors of 3.17 m from z=5.40. Per bay, a window unit recessed
   0.28 m: `Toy_roofd` reveal, `Toy_glass` pane, `Toy_trim` frame 0.10 m proud of
   the pane. Window band 0.55–2.75 m within each floor, i.e. tall and nearly
   bay-wide.
6. Parapet: z=20.84 to z=21.34 following the footprint, 0.40 m thick, `Toy_stone`
   with a `Toy_trim` coping in the top 0.16 m.
7. Fire escape: `Toy_ink`, on the Brannan elevation at bay 2–3, landings at each
   upper floor, 0.9 m projection.
8. Roof deck at z=20.84, `Toy_roofd`. Penthouse 8.0 x 6.4 m in `Toy_slate` from
   z=20.84 to **z=25.20** with a `Toy_trim` cap — this sets the bounding-box top and
   must land exactly on 25.20. Secondary bulkhead 5.0 x 4.0 m to z=23.40. Mechanical
   platform 9.0 x 5.5 x 0.9 m in `Toy_steel`, three vent boxes, one round tank
   (10 segments) 2.2 m diameter x 2.4 m.
9. Bevel 0.12 m, 2 segments on the chunky solids; 0.05 m / 1 segment on window
   frames and capitals; none on fills and glow shells.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette (`Toy_slate` follows the
existing precedent in `artifacts/` for a cool mid-gray key).

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `d9d2c2` | pilasters, upper wall field, parapet |
| `Toy_trim` | `f3efe6` | pilaster capitals, parapet coping, window frames, penthouse cap |
| `Toy_ink` | `3a3530` | ground-floor base skin, base cornice, fire escape |
| `Toy_roofd` | `45454a` | window reveals and spandrel recesses, roof deck |
| `Toy_slate` | `6f7883` | penthouse and bulkhead walls (so they read against the deck) |
| `Toy_glass` | `2a4d73` | upper-floor glazing |
| `Toy_glassl` | `6f95b8` | ground-floor storefront glazing |
| `Toy_steel` | `9aa0a6` | roll-up door, roof mechanical platform, vents, tank |
| `Toy_glassl_Glow` | `6f95b8` | lit upper windows at night |
| `Toy_trim_Glow` | `f3efe6` | the lit ground-floor band under the base cornice |

**Value budget.** This building is genuinely dark over about a quarter of its
surface. `Toy_ink` is reserved for the one-storey base and the cornice; every
upper-floor recess uses the lighter `Toy_roofd`. Do not darken further without
checking the aerial render — the app's lighting is flatter than the review rig, and
a facade that reads "slate" in Blender can read "black hole" in the scene.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day
(and closer to 23% where a closed shell stacks two layers), so a primary surface
must never be authored as glow. **Hero glow: the canted corner** — its window bay
lit on all five upper floors, plus the ground-floor band under the cornice returning
around the cant. That is a single vertical stripe of light on the corner of a dark
block, and it is exactly what a lit lobby-and-lift-core corner looks like at night.
Supporting accent: roughly a third of the upper bays lit, scattered unevenly and
differently per floor, on Second Street and Brannan only — never on the party wall.

### 2.9 Top surface

A 1,136 m2 flat roof 21 m up, higher than anything within two blocks, in a district
the camera flies over constantly. Keep the deck (`Toy_roofd`) clearly darker than
the `Toy_trim` parapet coping so the ring reads from above. Group the penthouse
cluster **just north of centre** and the mechanical platform immediately south of
it, matching the nadir imagery, and leave the Second Street and Brannan thirds of
the deck comparatively clean — the real roof is empty there. The penthouse is the
crest and the only thing that breaks the 21.34 m parapet silhouette, so give it a
deliberate shape: a plain slab-capped box, long axis parallel to Brannan.

### 2.10 Scope

**In the GLB:** the single block — body, base, base cornice, all four elevations and
the cant, pilasters, window bays, ground-floor openings and roll-up door, fire
escape, parapet, roof deck and roof furniture

**Not in the GLB:** Second Street, Brannan Street, Stanford Street, 577 Second
Street, 318 Brannan, the street trees, the 2025 scaffolding, traffic signals,
sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 15,000 — a six-storey building with three finished elevations, a cant and a
designed roof. Suggested split: body, parapet and base ~1.2k; pilasters (22 strips
with capitals) ~2.6k; window units (13 street bays + 6 Stanford bays x 5 floors =
95) ~5.7k; ground-floor openings and arches ~1.3k; base cornice ~0.5k; fire escape
~0.5k; roof furniture ~1.6k; glow shells ~0.6k.

If the count runs over, cut the Stanford Street window units to three floors before
touching the street elevations.

### 2.12 Draft manifest entry

```json
{
  "id": "300-brannan",
  "file": "300-brannan.glb",
  "anchor": [
    -122.3925543,
    37.7818313
  ],
  "targetHeightM": 25.2,
  "cat": 3,
  "name": "300 Brannan Street",
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
  (`id: '300Brannan'`, lon/lat as above, `height: 25.2`) and re-bake the affected
  tiles, or the baked procedural building on this exact footprint will intersect the
  GLB.
- **Exclusion radius must be measured, not guessed.** This is a full-lot corner
  parcel whose north-west party wall is shared with 577 Second Street and whose
  neighbours' rings touch its own. `excluded()` tests every ring vertex as well as
  the centroid, so size the radius against the real bake input
  (`data/buildings_datasf.geojson`) and expect the safe band to be narrow. Start the
  measurement at ~12 m (the footprint's own half-diagonal is ~24 m, so the radius
  must clear the building's own vertices) and walk it up until a second building
  drops. Expect to lose the small structure the survey shows immediately east of the
  cant if there is one.
- `loadRadius`: the default formula gives `max(2500, 25.2 x 30) = 2500` m. Take the
  default.
- This is the seventh asset in the Brannan family (with 350/358/362/370/380/400) and
  sits directly across Stanford Street from the South Park group. **Batch mode
  applies** — see 2.15.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 25.2 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~45.8 x 47.3 m is expected)
- [ ] Triangles at or under 15,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the corner-bay stripe, the ground-floor band and the scattered
      lit upper bays; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **OSM is wrong about the corner.** OSM way/112758589 traces a clean 37.71 x 29.78 m
  rectangle with a sharp east corner. It agrees with the survey on area to within
  1.5%, which makes it a plausible-looking trap: take the shape from DataSF
  (`ynuv-fyni`), not from OSM. The corner is canted and both the survey and May-2025
  Street View say so.
- **The cant has two lengths and only one of them is the one to build.** 8.09 m raw,
  **5.05 m flush**; see 2.3. Building the 8.09 m edge would push the corner ~2 m into
  Second Street.
- **The crest is the least certain number in this dossier.** The LiDAR maximum is
  25.67 m over a roof whose deck is 20.84 m (σ 1.35 m over 4,591 cells). A 4.8 m
  penthouse is entirely normal for a 1912 freight-elevator loft, and the nadir
  imagery shows a real, bright, shadow-casting box cluster there — but a mast,
  railing or antenna would also return 25.67 m. The plan takes **25.2 m**, shading
  the LiDAR maximum down by ~0.5 m for that reason. The reconciliation that makes
  this dossier hang together is the deck: 20.84 m LiDAR + a ~0.5 m parapet = the
  surveyed **70 ft / 21.34 m**, so the deck and the architectural height agree, and
  only the penthouse is estimated. If a photograph of the roof turns up, use it and
  re-normalize.
- **The bay counts are read off oblique Street View** — 6 on Second, 6 on Brannan,
  1 on the cant — and the Stanford Street count (6) is *inferred* with no
  street-level photograph at all. Re-count before modelling.
- **Whether the north-west party wall carries windows above its neighbours' roofs is
  unresolved.** 577 Second Street and 318 Brannan are both lower, so several storeys
  of that wall stand clear; a 1912 lot-line wall would normally be blank, but this
  one has had a century to acquire light wells. The plan builds it blank with a
  sparse top-floor scatter; if imagery shows otherwise, follow the imagery.
- **The paint scheme is post-2008 and could change again.** The 1990/2008 survey
  records the exterior as stucco with no colour; the current light-pilaster /
  charcoal-base scheme dates from the renovation and is documented only by
  photography. It is also the whole visual identity of the asset, so record the
  capture date of whatever imagery you settle it from.
- **Do not model 301 Brannan by mistake.** The red-brick six-storey Crane Company
  Building (1909, Lewis P. Hobart) stands directly across Brannan and dominates most
  community street-level imagery of this intersection. 300 Brannan is the *stucco*
  one, on the north-west side of Brannan and the south-west side of Second.
- **Batch:** this asset is being built alongside the rest of the Brannan and South
  Park families. Stage 5 must run in batch mode (source-only branch, bake discarded)
  or the landmarks' tile re-bakes will collide.
