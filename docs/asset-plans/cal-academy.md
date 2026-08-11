# California Academy of Sciences — SF-SIM asset plan

A wide, low Renzo Piano building whose entire identity is its undulating living roof with round skylights. The hero surface is exactly the one the app camera looks at.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/cal-academy/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `cal-academy` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4662432, 37.7698424` |
| Target height | **~11 m** at the roof hills (OSM `height`=11; *verify* the hill peaks) |
| OSM footprint | 161.2 x 102.6 m, ~171 deg cw from true north (OSM way/28695389, 16,418 m2) |
| Triangle cap | 27,000 |
| Category | `16` (Museum) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready California Academy of Sciences GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of California Academy of Sciences in San Francisco and deliver it
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
8. `docs/asset-plans/cal-academy.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Huge low-profile building integrated into the landscape
- Undulating living green roof with multiple rounded hills
- Circular skylights across the roof
- Glass perimeter walls
- Large central glass-covered piazza
- The roof should be the hero feature

## Research California Academy of Sciences independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The number and position of the roof domes/hills (commonly described as seven)
- Skylight count and diameter across the roof
- The overhanging roof canopy edge and its photovoltaic fringe

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/cal-academy/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as California Academy of Sciences, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the museum building, its living roof, the piazza canopy and the projecting roof eave.

Do not include unrelated surrounding city geometry: Golden Gate Park planting, the Music Concourse, the de Young opposite, paths, trees, people, vehicles, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance faces the Music Concourse on the north-east. Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/cal-academy/build_cal_academy.py` (deterministic build script),
`artifacts/cal-academy/cal-academy.blend`, and `artifacts/cal-academy/cal-academy.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`cal-academy-top.png`, `cal-academy-north.png`, `cal-academy-east.png`, `cal-academy-south.png`,
`cal-academy-west.png`, plus `cal-academy-contact-sheet.png` and at least one high
three-quarter aerial beauty render `cal-academy-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the hill topography, skylight ring positions and the flat overhanging eave; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `cal-academy.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/cal-academy/validation.json` and
`artifacts/cal-academy/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "cal-academy",
  "file": "cal-academy.glb",
  "anchor": [
    -122.4662432,
    37.7698424
  ],
  "targetHeightM": 11,
  "cat": 16,
  "name": "California Academy of Sciences",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/cal-academy.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Current building opened | 2008 (institution founded 1853) | Wikipedia, Wikidata |
| Architect | Renzo Piano Building Workshop | Wikipedia — *verify in the article* |
| Roof | 2.5-acre living roof with rounded domes and circular skylights | Wikipedia — *verify the figure* |
| Footprint | 161.2 x 102.6 m, 16,418 m2 | OSM way/28695389 (measured) |
| Height | 11 m tagged, 5 levels | OSM `height`, `building:levels` |
| Material | Glass perimeter with a planted roof over concrete/steel | OSM `building:material=glass` |
| Roof hills | Commonly described as seven | *inferred* — verify |

### 2.2 Sources

- https://www.openstreetmap.org/way/28695389 — footprint, height, levels, glass material
- https://en.wikipedia.org/wiki/California_Academy_of_Sciences — 2008 building, living roof, Piano
- https://www.calacademy.org/living-roof — owner material describing the roof, domes and skylights
- https://www.rpbw.com — architect project page with sections and roof diagrams
- https://commons.wikimedia.org/wiki/Category:California_Academy_of_Sciences — aerials of the roof, the eave, the piazza

### 2.3 Orientation and placement

A large rectangle aligned with the Golden Gate Park concourse grid (~171 deg cw from true north, close to cardinal). The entrance faces the Music Concourse to the north-east, with the de Young Museum directly opposite.

### 2.4 What each side shows

**North-east (concourse front)** — Glass wall under a deep flat roof overhang, with the entrance and the roof edge reading as a thin horizontal line.

**South-east / north-west** — Long glass elevations with regular structural mullions; the roof hills bulge above the eave line.

**South-west (rear)** — Service side; plainer, with plant enclosures.

**Top** — The hero: a green undulating field with several rounded hills, dozens of circular skylights clustered on the domes, a flat perimeter eave, a glazed central piazza, and PV panels around the fringe.

### 2.5 Recognition cues (ranked)

1. The green hilly roof — no other building in SF has one
2. Circular skylights punched across the hills
3. A very low, very wide profile hugging the park
4. A thin flat overhanging eave all the way round

### 2.6 Miniature translation

**Preserve**

- The 161 x 103 m footprint and low height
- The hill count and their asymmetric placement
- Skylight circles as real geometry, readable from above
- The flat overhanging eave contrasting the curved hills

**Simplify / exaggerate**

- The living roof becomes a smooth displaced surface with 6-8 domes, flat green material — no plant geometry
- Skylights become simple circular discs or shallow cylinders, 20-30 total, not the real count
- Glass walls become a `Toy_glass` band with `Toy_white` mullions every 6 m
- Interior spheres (planetarium, rainforest) are not modelled; their domes read as roof hills

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Base slab: 161 x 103 m plate at z=0, 1 m tall, `Toy_stone`.
2. Glass wall band: full perimeter, z=1 to z=8, `Toy_glass` with `Toy_white` mullions every 6 m.
3. Roof plate: 171 x 113 m (a 5 m overhang all round), 0.8 m thick, at z=8, `Toy_verdigris` edge / `Toy_mint` top.
4. Roof hills: 7 dome bulges of radii 12-26 m and heights 1.5-3 m, blended into the roof plate; smooth-shaded is acceptable here but keep the polycount at ~24 segments per dome.
5. Skylights: 26 cylinders radius 1.6 m, 0.4 m proud, distributed on and between the domes; `Toy_glass` tops with `Toy_white` rims.
6. Piazza: a 30 x 30 m glazed opening in the roof centre with a shallow `Toy_glass` canopy and a `Toy_white` frame grid.
7. PV fringe: a 4 m wide `Toy_ink` band around the eave.
8. Bevel 0.1 m, 2 segments on hard edges only.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_mint` | `#8fd0a8` | living roof surface |
| `Toy_verdigris` | `#9fb8a8` | roof edge and eave underside |
| `Toy_glass` | `#2a4d73` | perimeter walls, skylight tops, piazza canopy |
| `Toy_white` | `#f7f4ec` | mullions, skylight rims, piazza frame |
| `Toy_stone` | `#d9d2c2` | base slab |
| `Toy_ink` | `#3a3530` | photovoltaic fringe |
| `Toy_white_Glow` | `#f7f4ec` | piazza canopy glow at night |

Night glow: the central piazza canopy only — a soft lit core under a dark roof reads beautifully at night.

### 2.9 Top surface

This asset IS its roof. Budget accordingly: smooth hills, correctly clustered skylights, a crisp eave and the piazza opening. If anything gets cut to stay under budget, cut the elevations, not the roof.

### 2.10 Scope

**In the GLB:** the museum building, its living roof, the piazza canopy and the projecting roof eave

**Not in the GLB:** Golden Gate Park planting, the Music Concourse, the de Young opposite, paths, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: roof hills ~12k, skylights ~5k, eave and plate ~4k, glass walls ~4k, piazza ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "cal-academy",
  "file": "cal-academy.glb",
  "anchor": [
    -122.4662432,
    37.7698424
  ],
  "targetHeightM": 11,
  "cat": 16,
  "name": "California Academy of Sciences",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'calAcademy'`, `exclude: ~120`) and re-bake.
- Manifest id `cal-academy` maps to `calAcademy`.
- At 11 m tall and 161 m wide, the loader's height-based scaling is extremely sensitive — a 1 m height error is a ~9% plan error. Verify the height and then verify the footprint in-app.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the piazza canopy
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- The OSM 11 m height may describe the eave, not the hill peaks. This is the most consequential unknown in the plan.
- Very wide, very low assets are where height-driven scaling goes wrong. Measure in-app against the OSM polygon after placement.
- Green roofs can read as a lawn blob. Skylights and the eave line are what make it a building.
