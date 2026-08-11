# Fairmont San Francisco — SF-SIM asset plan

Two buildings that read as one hotel: the 1907 Beaux-Arts block crowning Nob Hill and the 1961 tower behind it. The user's cues describe the historic block, so that is the hero.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/fairmont-san-francisco/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `fairmont` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4101606, 37.7924935` |
| Target height | **99.06 m** for the 1961 tower; the original 1907 building is 9 storeys (~35 m, *estimated*) |
| OSM footprint | mapped complex 117.9 x 84.0 m (OSM relation/16217497, 9,416 m2); the historic block is the larger part |
| Triangle cap | 24,000 |
| Category | `7` (Hotel) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Fairmont San Francisco GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Fairmont San Francisco in San Francisco and deliver it
as a downloadable, validated GLB.

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
8. `docs/asset-plans/fairmont-san-francisco.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Massive white/cream Beaux-Arts hotel sitting prominently atop Nob Hill
- Symmetrical facade
- Classical columns and cornices
- Rows of repetitive windows
- Projecting central entrance
- Rooftop penthouse structures and flags

## Research Fairmont San Francisco independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The historic block's true height and storey count (9 floors) and its cornice line
- Whether to include the 1961 tower; the mapped relation covers both
- The Mason Street entrance portico, its columns and the flagpoles

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/fairmont-san-francisco/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as Fairmont San Francisco, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the 1907 hotel block with its entrance portico, cornice and rooftop penthouses; optionally the 1961 tower behind it if research shows the pair reads better on the hill.

Do not include unrelated surrounding city geometry: Huntington Park, Grace Cathedral, the Mark Hopkins opposite, California and Mason Streets, the cable car line, trees, people, vehicles, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 24,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance faces **east** onto Mason Street. Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/fairmont-san-francisco/build_fairmont_san_francisco.py` (deterministic build script),
`artifacts/fairmont-san-francisco/fairmont-san-francisco.blend`, and `artifacts/fairmont-san-francisco/fairmont-san-francisco.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`fairmont-san-francisco-top.png`, `fairmont-san-francisco-north.png`, `fairmont-san-francisco-east.png`, `fairmont-san-francisco-south.png`,
`fairmont-san-francisco-west.png`, plus `fairmont-san-francisco-contact-sheet.png` and at least one high
three-quarter aerial beauty render `fairmont-san-francisco-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the historic block's flat roof, penthouse structures, flagpoles and the tower's crown if included; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `fairmont-san-francisco.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/fairmont-san-francisco/validation.json` and
`artifacts/fairmont-san-francisco/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "fairmont",
  "file": "fairmont-san-francisco.glb",
  "anchor": [
    -122.4101606,
    37.7924935
  ],
  "targetHeightM": 99,
  "cat": 7,
  "name": "Fairmont San Francisco",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/fairmont-san-francisco.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Opened | 1907 (after the 1906 earthquake delayed it) | Wikipedia, Wikidata |
| Architects | Reid & Reid; interiors restored by Julia Morgan | Wikidata P84, Wikipedia |
| Floors | Main building 9; tower 29 | Wikipedia infobox |
| Tower height | 99.06 m | Wikipedia infobox |
| Main block height | ~35 m | *estimated from 9 storeys* — verify |
| Mapped complex | 117.9 x 84.0 m, 9,416 m2 | OSM relation/16217497 (measured; covers both buildings) |
| Style | Beaux-Arts | Wikidata P149 |
| Location | 950 Mason Street, atop Nob Hill | OSM tags |

### 2.2 Sources

- https://www.openstreetmap.org/relation/16217497 — complex footprint and hotel tags
- https://en.wikipedia.org/wiki/Fairmont_San_Francisco — 1907 opening, Reid & Reid, Julia Morgan, 9/29 floors, 99.06 m tower
- https://www.wikidata.org/wiki/Q1393862 — architects, opening, style
- https://www.fairmont.com/san-francisco — owner material with exterior and rooftop imagery
- https://commons.wikimedia.org/wiki/Category:Fairmont_San_Francisco — Mason Street elevation, aerials showing both buildings, night views

### 2.3 Orientation and placement

The historic block sits at the corner of Mason and California with the principal entrance facing east onto Mason Street and the porte-cochere below it; the 1961 tower stands behind (west of) it. Confirm the block's rotation from the mapped polygon and imagery, because the relation covers both structures.

### 2.4 What each side shows

**East (Mason Street front)** — The hero elevation: rusticated base, a projecting central entrance with paired columns, seven regular window bays each side, heavy cornice and a balustraded roof edge with flagpoles.

**North (California Street)** — Long symmetrical flank with the same window rhythm and a secondary entrance.

**South / West** — The tower rises behind; the historic block's rear is plainer and partly obscured by the tower's podium.

**Top** — The historic block's flat roof with penthouse structures, a rooftop garden terrace, flagpoles and mechanical clusters; the tower crown beyond if modelled.

### 2.5 Recognition cues (ranked)

1. A big pale symmetrical block crowning Nob Hill
2. Regular grid of identical windows over a rusticated base
3. Heavy cornice with a roof balustrade and flags
4. Projecting classical entrance portico

### 2.6 Miniature translation

**Preserve**

- The historic block's mass and 9-storey proportion
- Facade symmetry and window grid regularity
- The cornice and balustrade line
- Hilltop prominence — do not shrink it

**Simplify / exaggerate**

- Roughly 200 windows become a clean recessed grid, all identical
- Ornament becomes three horizontal bands: base, mid string course, cornice
- The portico becomes four chunky columns and a flat canopy
- Rooftop clutter becomes two penthouse blocks and a terrace with three flagpoles

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Base: 76 x 60 m block, z=0 to z=8, `Toy_stone`, rusticated with deep horizontal grooves.
2. Body: same plan, z=8 to z=32, `Toy_cream`, with a 7 x 5 window grid per elevation, openings 1.8 x 3 m recessed 0.25 m.
3. String course: `Toy_trim` band at z=20.
4. Cornice: 1.5 m `Toy_trim` at z=32 projecting 1.2 m, with a 1.4 m balustrade above.
5. Portico: 14 m wide projection on the east face, 4 columns radius 1.2 m, z=0 to z=10, flat `Toy_trim` canopy; porte-cochere drive beneath.
6. Roof: flat `Toy_roofd` with two penthouse blocks (16 x 10 x 6 m and 10 x 8 x 4 m), a terrace and three `Toy_steel` flagpoles.
7. Optional 1961 tower: 34 x 26 m slab, z=0 to z=99, `Toy_sand` with a `Toy_glass` window grid and a flat crown; place it west of the historic block.
8. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | main hotel walls |
| `Toy_stone` | `#d9d2c2` | rusticated base and portico steps |
| `Toy_trim` | `#f3efe6` | cornice, balustrade, string course, canopy |
| `Toy_glass` | `#2a4d73` | windows |
| `Toy_roofd` | `#45454a` | roof, penthouses |
| `Toy_steel` | `#9aa0a6` | flagpoles |
| `Toy_red` | `#c4453c` | flag accents — one saturated spot of colour |
| `Toy_white_Glow` | `#f7f4ec` | the portico and facade uplight at night |

Night glow: the entrance portico plus a soft facade uplight band. Grand hotels read as lit at night; keep it to two surfaces.

### 2.9 Top surface

A large flat roof at the top of a hill is very exposed to the app camera. Design it properly: two penthouse blocks, a terrace with a different surface value, three flagpoles and one tidy plant cluster.

### 2.10 Scope

**In the GLB:** the 1907 hotel block with its entrance portico, cornice and rooftop penthouses; optionally the 1961 tower behind it if research shows the pair reads better on the hill

**Not in the GLB:** Huntington Park, Grace Cathedral, the Mark Hopkins opposite, California and Mason Streets, the cable car line, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 24,000. Suggested split: body and window grid ~10k, base and portico ~4k, cornice and balustrade ~3k, roof ~3k, optional tower ~4k

### 2.12 Draft manifest entry

```json
{
  "id": "fairmont",
  "file": "fairmont-san-francisco.glb",
  "anchor": [
    -122.4101606,
    37.7924935
  ],
  "targetHeightM": 99,
  "cat": 7,
  "name": "Fairmont San Francisco",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'fairmont'`, `exclude: ~80`) and re-bake.
- Manifest id `fairmont` maps to `fairmont` directly (no camel conversion needed).
- If the 1961 tower is included, the anchor and `targetHeightM` change substantially (99 m vs ~35 m). Decide before setting the manifest values.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the portico and facade uplight
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- One building or two? This is the biggest scope decision. The user's cues describe the 1907 block, so that is the default hero; the tower is optional.
- No published height was found for the historic block. The ~35 m figure is derived from the storey count and must be verified or marked estimated.
- The mapped OSM relation covers the whole complex, so it cannot be extruded directly.
