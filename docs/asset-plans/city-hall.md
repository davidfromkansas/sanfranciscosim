# San Francisco City Hall — SF-SIM asset plan

A symmetrical Beaux-Arts block with a gilded dome taller than the US Capitol. The dome is the entire identity; the body's job is to be big, calm and symmetrical underneath it.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/city-hall/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `city-hall` |
| Existing procedural builder | `cityHall()` in `app/src/landmarks.js` (key `9`, exclusion 110 m) |
| WGS84 anchor | `-122.4192838, 37.7793223` |
| Target height | **93.73 m** to the top of the dome (307.5 ft) |
| OSM footprint | 126.6 x 97.8 m, ~171 deg cw from true north (OSM relation/7261820, 11,033 m2) |
| Triangle cap | 27,000 |
| Category | `18` (Government) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready San Francisco City Hall GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of San Francisco City Hall in San Francisco and deliver it
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
8. `docs/asset-plans/city-hall.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Massive central gold dome
- Symmetrical Beaux-Arts facade
- White/cream stone
- Classical columns
- Triangular pediments
- Prominent central staircase
- Smaller roof structures surrounding the dome

## Research San Francisco City Hall independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Dome drum colonnade and lantern proportions
- Which elevation carries the main pedimented portico and grand steps (Polk Street / Civic Center Plaza)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/city-hall/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as San Francisco City Hall, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the City Hall building, its dome, porticos, the plaza-facing steps and the low balustraded terrace.

Do not include unrelated surrounding city geometry: Civic Center Plaza, its lawns and fountains, Van Ness Avenue, flagpoles in the plaza, neighbouring civic buildings, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The ceremonial front faces Civic Center Plaza (east / Polk Street). Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/city-hall/build_city_hall.py` (deterministic build script),
`artifacts/city-hall/city-hall.blend`, and `artifacts/city-hall/city-hall.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`city-hall-top.png`, `city-hall-north.png`, `city-hall-east.png`, `city-hall-south.png`,
`city-hall-west.png`, plus `city-hall-contact-sheet.png` and at least one high
three-quarter aerial beauty render `city-hall-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the dome, lantern, drum colonnade and the four surrounding roof pavilions; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `city-hall.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/city-hall/validation.json` and
`artifacts/city-hall/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "city-hall",
  "file": "city-hall.glb",
  "anchor": [
    -122.4192838,
    37.7793223
  ],
  "targetHeightM": 93.73,
  "cat": 18,
  "name": "San Francisco City Hall",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/city-hall.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Dome height | 93.73 m / 307.5 ft above Civic Center | Wikipedia infobox `antenna_spire`, body text |
| Dome diameter | 112 ft / 34 m | Wikipedia |
| Plan | 390 ft (Van Ness to Polk) x 273 ft (Grove to McAllister) = ~119 x 83 m | Wikipedia |
| Mapped footprint | 126.6 x 97.8 m, 11,033 m2 (includes steps/terrace) | OSM relation/7261820 (measured) |
| Floors | 5 including ground floor | Wikipedia infobox |
| Re-opened | 1915 | Wikipedia, Wikidata |
| Architect | Bakewell & Brown (Arthur Brown Jr.) | Wikidata P84 |
| Colours | Cream granite body tagged `#e3e3de`; dome gilded/gold-leaf ribs over grey | OSM `building:colour`; *inferred* for the dome |

### 2.2 Sources

- https://www.openstreetmap.org/relation/7261820 — footprint, 30 m cornice height tag, colour, address
- https://en.wikipedia.org/wiki/San_Francisco_City_Hall — 307.5 ft dome, 112 ft diameter, 390x273 ft plan, architect
- https://www.wikidata.org/wiki/Q1093944 — style, architect, 1915
- https://sfgsa.org/city-hall — city operator material, tours, elevations
- https://commons.wikimedia.org/wiki/Category:San_Francisco_City_Hall — plaza elevation, aerials of the dome and roof pavilions, night lighting

### 2.3 Orientation and placement

The building's long axis runs roughly north-south with the main pedimented entrance and grand steps facing east onto Civic Center Plaza; the measured mapped long axis is ~171 deg cw from true north (almost cardinal, slightly rotated with the Civic Center grid).

### 2.4 What each side shows

**East (plaza front)** — The hero elevation: central pedimented portico with a giant order of columns, broad steps, symmetrical wings, heavy cornice and balustrade.

**West (Van Ness)** — Nearly identical in composition, slightly plainer; a second portico and steps.

**North / South** — Long wings of repeating rectangular windows in three tiers between engaged pilasters, capped by the same cornice and balustrade.

**Top** — The dome on its colonnaded drum plus a lantern, four roof pavilions at the corners of the crossing, flat roof planes and light wells.

### 2.5 Recognition cues (ranked)

1. The gilded dome — instantly legible from the aerial camera
2. Perfect bilateral symmetry of a long cream Beaux-Arts block
3. Colonnaded drum under the dome
4. Deep pedimented portico over a wide central staircase

### 2.6 Miniature translation

**Preserve**

- Dome apex at 93.73 m with the cornice line around 30 m
- 34 m dome diameter relative to the ~119 x 83 m body
- Symmetry — any asymmetry reads as a bug
- The colonnaded drum, which is what makes the dome look tall

**Simplify / exaggerate**

- Hundreds of windows become three tiers of regular rectangular recesses
- Pilaster orders become chunky vertical ribs, not fluted columns, except at the porticos
- Dome ribs become 16 raised bands with a smooth gold surface between
- Statuary, cartouches and mouldings are dropped; the pediment gets one flat relief panel

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: 119 x 83 m block, z=0 to z=30, `Toy_sand`; rusticated base band 0 to 8 m, `Toy_stone`.
2. Window grid: three tiers of recessed openings 2 m x 3.5 m, spaced 6 m, all four elevations, `Toy_glass`.
3. Cornice + balustrade: 2 m `Toy_trim` band at z=30 with a 1.5 m open balustrade above.
4. Porticos (east and west): 8 columns radius 1.6 m, 18 m tall, projecting 8 m, with a triangular pediment 6 m tall, `Toy_trim`.
5. Grand steps (east): 24 m wide, 12 treads, `Toy_stone`.
6. Crossing block: 46 x 46 m raised to z=40, `Toy_sand`.
7. Drum: cylinder radius 19 m, z=40 to z=58, ringed by 24 columns radius 1.1 m, `Toy_sand` / `Toy_trim`.
8. Dome: ribbed hemisphere radius 17 m, z=58 to z=82, 16 ribs, `Toy_gold`; lantern cylinder radius 4 m to z=90; cupola and finial to z=93.73.
9. Roof pavilions: four 10 x 10 x 8 m `Toy_roofd` blocks at the crossing corners; light-well recesses in the flat roof.
10. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | main walls, drum, crossing |
| `Toy_stone` | `#d9d2c2` | rusticated base, steps, terrace |
| `Toy_trim` | `#f3efe6` | cornice, balustrade, pediments, capitals |
| `Toy_gold` | `#caa64a` | dome ribs and dome surface |
| `Toy_glass` | `#2a4d73` | window recesses |
| `Toy_roofd` | `#45454a` | flat roof planes and pavilions |
| `Toy_gold_Glow` | `#caa64a` | dome and lantern at night |

Night glow: the dome surface and lantern. City Hall is floodlit and frequently colour-washed; a single warm gold glow material is the contract-safe abstraction.

### 2.9 Top surface

Large flat roof areas surround the dome and the camera looks straight at them. Design them: four corner pavilions, two symmetric light wells, a low parapet, and tidy `Toy_roofd` plant rows. Do not leave grey emptiness around the dome.

### 2.10 Scope

**In the GLB:** the City Hall building, its dome, porticos, the plaza-facing steps and the low balustraded terrace

**Not in the GLB:** Civic Center Plaza, its lawns and fountains, Van Ness Avenue, flagpoles in the plaza, neighbouring civic buildings, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: body and windows ~9k, cornice/balustrade ~3k, porticos and steps ~4k, drum and colonnade ~5k, dome and lantern ~4k, roof pavilions ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "city-hall",
  "file": "city-hall.glb",
  "anchor": [
    -122.4192838,
    37.7793223
  ],
  "targetHeightM": 93.73,
  "cat": 18,
  "name": "San Francisco City Hall",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `cityHall` exists procedurally and in the registry (exclusion 110 m, key `9`); manifest id `city-hall` maps to it.
- Set `targetHeightM: 93.73`; the tiles entry currently has no height.
- Check the plaza-side steps do not sink into sampled terrain — Civic Center is nearly flat, so a small base plinth is safer.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the dome and lantern
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Getting the dome-to-body ratio wrong makes it read as a generic capitol. Measure both from the same elevation photograph.
- The gold can look toy-cheap if fully saturated; `Toy_gold` at flat shading with ribbed geometry is the intended look.
- The OSM footprint includes terraces; use the 390 x 273 ft published plan for the body and keep the terrace separate.
