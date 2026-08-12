# Letterman Digital Arts Center — SF-SIM asset plan

Lucasfilm's Presidio campus at One Letterman Drive: four low brick-and-stucco
buildings around a Lawrence Halprin landscape of lawn, stream and lagoon, with
the Yoda Fountain at the front door. The user chose the **whole campus** as one
grouped landmark (the painted-ladies model: several structures, one GLB).

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/letterman-digital-arts-center/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `letterman` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.449439, 37.799731` (campus AABB centre, measured; re-derive from the modelled extent) |
| Target height | **~22 m** to Building B/C/D roof ridge (*estimated* — 4 storeys + hipped roof; OSM tags say 15–18 m, no published architectural height found) |
| OSM footprint | 4 building ways sharing `addr 1 Letterman Drive`; campus building AABB 294 × 280 m (measured, see 2.1) |
| Triangle cap | 27,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Letterman Digital Arts Center GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Letterman Digital Arts Center
campus (One Letterman Drive, Presidio, San Francisco) and deliver it as a
downloadable, validated GLB.

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
7. `artifacts/salesforce-tower/` — the reference implementation of this exact
   deliverable (dossier, deterministic build script, validator, renders, report)
8. `docs/asset-plans/letterman-digital-arts-center.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Four separate low brick-red buildings with white/cream stucco bands and
  terracotta hipped roofs, arranged around a central landscape — Presidio
  military architecture reinterpreted as a modern campus
- The Halprin landscape: sloping green meadow, a boulder-lined lagoon, a rocky
  stream winding down to it
- The Yoda Fountain in the entrance forecourt of Building B — the campus's
  single most famous object; semantic exaggeration is expected
- Regular window grids in deep punched openings; arcaded/columned ground floors
  facing the park
- Buildings read as a family: same materials, same roof, different footprints

## Research the Letterman Digital Arts Center independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the four footprints, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations of each building (A, B, C, D)
- Aerial and roof/top views — the hipped terracotta roofs and their dormers,
  vents and mechanical courts are the surfaces the app camera sees most
- Ground-level views of the Building B entrance and the Yoda Fountain
- The lagoon, stream and meadow layout (aerial imagery; TCLF's landscape
  description)
- Day and night appearance — campus lighting is warm and restrained
- Publicly available drawings, plans or diagrams (Presidio Trust planning
  documents cover this site)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/letterman-digital-arts-center/REFERENCE.md` containing: source links and
what each establishes; verified dimensions and location; orientation;
observations from all four sides and above; the 3-5 strongest recognition cues;
features to preserve; features to simplify; uncertainties and conflicting
evidence. A contact sheet of attributed reference thumbnails is welcome if
legally permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Letterman Digital
Arts Center, consistent with the real campus from all four sides and above,
architecturally credible, and a premium handcrafted miniature — not
photorealistic, not voxel art, not generic low-poly, and never accurate in one
view while invented in the others.

## Scope of the exported asset

Export the four buildings (A, B, C, D) on their real relative footprints, the
Building B entrance forecourt with the Yoda Fountain, the lagoon with its
boulder edge, the stream course, the central meadow surface immediately between
and east of the buildings, and a few grouped tree clusters that frame the
architecture (style bible §12).

Do not include the wider 17-acre parkland toward the Lombard Gate, Letterman
Drive itself, O'Reilly Avenue, the Thoreau Center or any neighbouring Presidio
buildings, the Palace of Fine Arts, parked cars, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into
the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 27,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The campus
grid is rotated roughly 25° off north (measured from the OSM footprints);
Building B's entrance and the Yoda Fountain face southwest onto Letterman
Drive. Author true-world orientation and document the heading in `REPORT.md`.

**Height normalization:** the roof ridge of the tallest building is the model's
highest point — no tree, chimney or flagpole may exceed it — and the bbox top
must equal the verified target height exactly, so the loader's
`targetHeightM / measuredHeight` scale lands at 1.0.

## Reproducible Blender workflow

Blender headless only: `blender -b --python script.py -- args`; no GPU
assumptions, so use Workbench or CPU Cycles.

Keep `artifacts/letterman-digital-arts-center/build_letterman_digital_arts_center.py`
(deterministic build script),
`artifacts/letterman-digital-arts-center/letterman-digital-arts-center.blend`, and
`artifacts/letterman-digital-arts-center/letterman-digital-arts-center.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`letterman-digital-arts-center-top.png`, `-north.png`, `-east.png`, `-south.png`,
`-west.png`, plus `letterman-digital-arts-center-contact-sheet.png` and at least one
high three-quarter aerial beauty render `letterman-digital-arts-center-aerial.png`,
plus a night render `letterman-digital-arts-center-night.png` showing the glow
design.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the four terracotta
roofs, the lagoon and the stream; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral
warm background, minimal depth of field, and every image must depict the same
exported model.

## Validate the exported GLB

Re-import `letterman-digital-arts-center.glb` into a fresh isolated Blender scene and
validate the re-import, not the source scene. Report object count, triangle
count, dimensions, bounding-box min/max, min Z, XY center offset, material
names, image-texture count, camera count, light count, animation count,
applied-transform status, negative-scale status, normal-orientation status
(per-object signed volume for union-of-solids; ray test ≤ 0.15% residual),
unexpected geometry, and per-material contract compliance. Render at least one
review image from the re-imported asset. Write
`artifacts/letterman-digital-arts-center/validation.json` and
`artifacts/letterman-digital-arts-center/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include
this draft entry in `REPORT.md`. Do not edit the production manifest in this
task.

```json
{
  "id": "letterman",
  "file": "letterman-digital-arts-center.glb",
  "anchor": [
    -122.449439,
    37.799731
  ],
  "targetHeightM": 22,
  "cat": 3,
  "name": "Letterman Digital Arts Center",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a
separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md`
for that, together with the integration notes in
`docs/asset-plans/letterman-digital-arts-center.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are
visual or derived estimates, not published figures — the executing agent must
re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Opened | July 2005 (construction from November 2002) | Wikipedia |
| Design architect / architect of record | Gensler / HKS, Inc. | Wikipedia |
| Landscape architect | Lawrence Halprin | Wikipedia, TCLF |
| Program | 850,000 sq ft, ~$350M, home of ILM + Lucasfilm divisions | Wikipedia |
| Site | 23 acres; 4 buildings on a 6-acre footprint; 17 acres public parkland | Wikipedia, TCLF |
| Storeys | Four, all buildings | Wikipedia, One Letterman leasing site |
| Materials | Red brick, white stucco, terracotta roofs echoing Presidio historic stock | Wikipedia |
| Building A footprint | OBB 137.7 × 75.5 m, 10,400 m² | OSM way/288374441 (measured) |
| Building B footprint | OBB 93.7 × 121.5 m, 11,386 m² | OSM way/288374442 (measured) |
| Building C footprint | OBB 86.1 × 86.4 m, 7,441 m² | OSM way/288374438 (measured) |
| Building D footprint | OBB 88.4 × 88.3 m, 7,801 m² | OSM way/288374439 (measured) |
| Campus building AABB | 294.3 × 279.9 m; centre `-122.449439, 37.799731` | OSM (measured) |
| Campus grid rotation | ~25° off cardinal (Building B OBB 24.9°) | OSM (measured) |
| OSM height tags | A 15 m; B, C, D 18 m | OSM — **shell values, do not use as target** (README warning) |
| Height to ridge | ~22 m | *estimated*: 4 storeys × ~4.5 m (raised floors, tall ceilings) + hipped roof; verify |
| Yoda Fountain | node/665688981 at `-122.45049, 37.79882` — Building B's SW entrance corner | OSM (measured) |
| Lagoon | way/32651841 centred `-122.44856, 37.80035` — NE of Building A, boulder-lined | OSM (measured), TCLF |
| Landscape structure | Sloping central meadow; cascading rocky stream → lagoon and plaza; groves of trees; two stone overlook plazas | TCLF |

### 2.2 Sources

- https://en.wikipedia.org/wiki/Letterman_Digital_Arts_Center — dates, architects, program, materials, four four-storey buildings
- https://www.wikidata.org/wiki/Q6533683 — entity record
- https://www.tclf.org/landscapes/letterman-digital-arts-center — Halprin landscape: meadow, stream, lagoon, plazas, groves
- https://www.openstreetmap.org/way/288374441 (A), /288374442 (B), /288374438 (C), /288374439 (D) — footprints, addr tags, shell heights
- https://www.openstreetmap.org/node/665688981 — Yoda Fountain position
- https://www.openstreetmap.org/way/32651841 — lagoon polygon
- https://www.onelettermandrive.com/ — leasing material: floor plates, "ceiling heights up to 24 feet", LEED Gold
- https://www.webcor.com/projects/letterman-digital-arts-center — builder's project page
- https://www.lucasfilm.com/campuses/san-francisco/ — owner material with campus imagery

### 2.3 Orientation and placement

The campus sits just inside the Presidio's Lombard Gate, bounded by Letterman
Drive (south/west) and O'Reilly Avenue (north). The building group occupies the
west half of the site; the land slopes gently down eastward, meadow → stream →
lagoon. Building B is the front-of-house: its southwest corner carries the main
ILM entrance and the Yoda Fountain forecourt facing Letterman Drive. A is the
long bar on the south, C and D pair up on the east side of the group with a
courtyard gap between them. The campus grid is rotated ~25° from north —
author the true rotation; the loader will not correct it.

### 2.4 What each side shows

**Southwest (Letterman Drive front)** — Building B's entrance elevation:
arcaded ground floor, brick body with stucco bands, deep punched windows, the
Yoda Fountain on a small circular plaza before the door. The hero elevation.

**Northwest (O'Reilly Avenue)** — Buildings A/B rear elevations to the street:
same family language, more continuous, service access. Plainer.

**Northeast / East (park side)** — The postcard view: all four buildings
looking over the meadow, stream and lagoon; arcades and terraces on the ground
floors; the lagoon reflecting Building A and the Palace of Fine Arts dome
beyond (the Palace is NOT in scope).

**Top** — Four large terracotta hipped roofs with ridge lines, clipped hips,
dormers and recessed mechanical courts; the green meadow, the blue lagoon and
the winding stream between them. At the app's camera this IS the landmark —
spend the detail here.

### 2.5 Recognition cues (ranked)

1. Four matching brick-and-terracotta courtyard buildings around a green — a
   campus, not a tower
2. The lagoon with its boulder edge and the stream winding down the meadow
3. The Yoda Fountain at the front door (tiny in reality — exaggerate
   semantically, style bible §9)
4. Terracotta hipped roofs with white-stucco banded brick facades — Presidio
   DNA
5. Ground-floor arcades facing the park

### 2.6 Miniature translation

**Preserve**

- Four distinct buildings on true relative footprints — the gaps between them
  read from the air
- The meadow-stream-lagoon diagonal
- Roof form: hipped terracotta, consistent family
- Brick body / stucco band / arcade base tripartite facades

**Simplify / exaggerate**

- Yoda Fountain: a real ~1.4 m statue becomes a readable miniature marker
  (~3-4 m with plinth and circular pool) — the one saturated
  storytelling object
- Hundreds of windows become clean recessed grids, all identical per building
- Dormers and roof clutter become 2-3 tidy clusters per roof
- Trees become 6-10 grouped crowns framing the buildings, not a forest
- The stream becomes one confident curved ribbon; the lagoon one clean
  boulder-edged shape

### 2.7 Massing recipe

Build order for the deterministic script; dimensions from 2.1 footprints are
the starting point, not a straitjacket — adjust after the first aerial review
render. All buildings share the recipe, varying footprint:

1. Ground plinth per building: footprint polygon (from OSM, simplified to
   8-14 verts), z=0 to z=1, `Toy_stone` — the arcade base reads as a band.
2. Body: footprint inset 0.5 m, z=1 to z=17, `Toy_brick`, with two `Toy_trim`
   stucco string courses and recessed `Toy_glass` window grids (per-elevation
   grid, openings ~1.6 × 2.4 m, recessed 0.25 m, merged per facade).
3. Arcade: park-facing elevations get 6-10 chunky square `Toy_trim` piers with
   a flat canopy at z=5.
4. Roof: hipped mass z=17 to z=22, `Toy_brick`-adjacent terracotta —
   use `Toy_rust` (a86444) for the tile read; ridge caps and 2-3 dormer/vent
   clusters per roof in `Toy_trim`/`Toy_roofd`.
5. Landscape slab: one contoured ground plane covering the campus extent,
   `Toy_mint`-toned green (use `Toy_mint` 8fd0a8) for meadow, `Toy_stone`
   plaza patches, gentle 2-3 m fall toward the lagoon.
6. Lagoon: OSM polygon simplified, `Toy_sky` water inset 0.4 m below meadow,
   ring of 8-12 `Toy_stone` boulders; stream: one curved swept ribbon of
   `Toy_sky` from the meadow's high corner to the lagoon.
7. Yoda Fountain: circular `Toy_stone` pool (r ≈ 2.5 m), plinth, and a
   ~1.5 m `Toy_mint`/`Toy_verdigris` figure — the saturated accent; sits on
   B's SW forecourt.
8. Trees: 6-10 instanced low-seg crowns (`Toy_mint` / darker green mix) with
   `Toy_ink` trunks, grouped in 2-3 groves (style bible §12).
9. Bevel 0.12 m, 2 segments, on building masses and roof edges.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | building bodies |
| `Toy_rust` | `#a86444` | terracotta roofs |
| `Toy_trim` | `#f3efe6` | stucco bands, arcade piers, dormers |
| `Toy_stone` | `#d9d2c2` | plinths, plazas, boulders, fountain |
| `Toy_glass` | `#2a4d73` | windows |
| `Toy_roofd` | `#45454a` | mechanical clusters, trunks/details |
| `Toy_mint` | `#8fd0a8` | meadow, tree crowns (vary value), Yoda |
| `Toy_verdigris` | `#9fb8a8` | Yoda figure bronze-patina read |
| `Toy_sky` | `#6db3d9` | lagoon and stream water |
| `Toy_white_Glow` | `#f7f4ec` | arcade soffits + B entrance at night |

Night glow: the Building B entrance/forecourt (hero) plus a restrained band of
lit arcade soffits on the park elevations (supporting accents). A campus at
night is warm pools of light, not a lit tower — keep it to those two groups.

### 2.9 Top surface

The camera looks down on four big roofs and a park. Roof: clean hips with
crisp ridge lines, 2-3 dormer/vent clusters each, one recessed mechanical
court on the largest roof. Ground: meadow with mowing-band value variation is
NOT wanted (noise) — one clean green, the stream ribbon, the lagoon, two stone
plazas, tree groves. The composition from above should read: four terracotta
rectangles, a green wedge, a blue comma.

### 2.10 Scope

**In the GLB:** Buildings A, B, C, D on true relative footprints; B's entrance
forecourt with the exaggerated Yoda Fountain; the lagoon, stream and central
meadow surface; grouped framing trees; two stone plazas.

**Not in the GLB:** the wider parkland toward Lombard Gate, Letterman Drive,
O'Reilly Avenue, the Thoreau Center / Tides Converge buildings, the Palace of
Fine Arts, cars, people, plinths, cameras or lights.

### 2.11 Triangle budget

Cap 27,000. Suggested split: four buildings with window grids and arcades
~16k, roofs ~4k, landscape slab + lagoon + stream ~2k, trees ~2.5k, fountain +
boulders + plazas ~1.5k, reserve ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "letterman",
  "file": "letterman-digital-arts-center.glb",
  "anchor": [
    -122.449439,
    37.799731
  ],
  "targetHeightM": 22,
  "cat": 3,
  "name": "Letterman Digital Arts Center",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`targetHeightM` stays `estimated: true` unless a published architectural
height surfaces. `loadRadius` = default rule `max(2500, 22 × 30) = 2500`.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'letterman'`, `lon: -122.449439`, `lat: 37.799731`, `height: 22`,
  `exclude: ~170` — it must clear all four baked footprints plus the lagoon,
  camera preset ~`{ distance: 700, yaw: 220, pitch: 24 }`) and re-bake the
  affected tiles, or the baked procedural buildings will intersect the GLB.
- Manifest id `letterman` → registry id `letterman` (no camel conversion).
- The asset is campus-scale (≈ 330 × 300 m): the exclusion radius and the
  anchor must be re-derived from the **modelled** extent, which includes the
  lagoon east of the building AABB — expect the anchor to shift ~20-30 m east
  of the buildings-only centre.
- Consider `clearTrees: true` like the Palace of Fine Arts — the grounds are
  hand-modelled and baked tree scatter will conflict.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Bbox top exactly at the verified target height (scale factor 1.0)
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the B entrance and arcade soffit groups
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume + ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **No published architectural height.** ~22 m ridge is derived from storey
  count and leasing-material ceiling heights; the OSM 15/18 m tags look like
  shell/eave values. Verify against imagery at build time; ship
  `estimated: true` either way.
- **Sloped site.** The land falls several meters from Letterman Drive to the
  lagoon. The loader seats the GLB at one terrain sample at the anchor; a
  300 m-wide asset may float or sink at its edges. The modelled ground slab's
  own contouring must absorb this — verify terrain seating carefully at
  integration (stage 5), and be prepared to flatten the slab's perimeter.
- **Water in a GLB.** The lagoon is `Toy_sky` flat color per the contract (no
  transparency). Confirm it reads as water next to the app's real water
  material, or nudge toward `Toy_glassl`.
- **Trees taller than buildings would break height normalization** — the
  recipe caps crowns below the 22 m ridge deliberately.
- **Four buildings, one asset**: the loader merges to ≤ 2 draw calls, so a
  grouped GLB is fine (precedent: painted-ladies), but the OBB rotation of
  each footprint must be authored true — errors compound across a campus.
