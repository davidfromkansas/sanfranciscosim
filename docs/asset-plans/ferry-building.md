# Ferry Building — SF-SIM asset plan

A 201 m long, low Beaux-Arts arcade with one 245 ft clock tower in the middle. The whole asset lives or dies on the proportion between the long horizontal body and the single vertical accent, plus four readable clock faces.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/ferry-building/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `ferry-building` |
| Existing procedural builder | `ferryBuilding()` in `app/src/landmarks.js` (key `7`, exclusion 120 m) |
| WGS84 anchor | `-122.3933697, 37.7955227` |
| Target height | **74.7 m** to the top of the clock tower (245 ft) |
| OSM footprint | 201 x 56 m, long axis ~54 deg cw from true north (OSM way/558731934, 9,847 m2) |
| Triangle cap | 24,000 |
| Category | `25` (Transit station) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Ferry Building GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Ferry Building in San Francisco and deliver it
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
8. `docs/asset-plans/ferry-building.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Long, low Beaux-Arts waterfront structure
- Central 245-foot clock tower
- Four large clock faces
- Arched ground-floor openings
- Cream-coloured facade
- Recognizable tower crown and flagpole

## Research Ferry Building independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Arcade bay count and rhythm along the Embarcadero elevation
- Tower crown detail (belvedere, cornice, flagpole) and clock dial diameter

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/ferry-building/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Ferry Building, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the Ferry Building itself: arcade body, clock tower, end pavilions and the ground-floor arcade.

Do not include unrelated surrounding city geometry: the ferry gates and gangways behind it, Embarcadero Plaza, the Embarcadero roadway, palm trees, streetcars, market stalls, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The building's front is the west (Market Street) elevation. Author it in true-world orientation; the `-Y` rule cannot also hold for a NE-SW building, so document the measured heading in `REPORT.md` (AGENTS rule 5 — real placement wins).
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/ferry-building/build_ferry_building.py` (deterministic build script),
`artifacts/ferry-building/ferry-building.blend`, and `artifacts/ferry-building/ferry-building.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`ferry-building-top.png`, `ferry-building-north.png`, `ferry-building-east.png`, `ferry-building-south.png`,
`ferry-building-west.png`, plus `ferry-building-contact-sheet.png` and at least one high
three-quarter aerial beauty render `ferry-building-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the tower crown, the ridge of the long clerestory roof and the roof plant clusters; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `ferry-building.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/ferry-building/validation.json` and
`artifacts/ferry-building/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "ferry-building",
  "file": "ferry-building.glb",
  "anchor": [
    -122.3933697,
    37.7955227
  ],
  "targetHeightM": 74.7,
  "cat": 25,
  "name": "Ferry Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/ferry-building.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 1 Ferry Building, The Embarcadero | OSM tags |
| Clock tower height | 245 ft / 74.7 m | Wikipedia (cited) |
| Clock dials | Four, each 22 ft / 6.7 m diameter | Wikipedia |
| Great Nave length | 660 ft / 201 m | Wikipedia; matches OSM footprint |
| Body height | ~15 m at the cornice | OSM `height`=15 (body only) |
| Opened | 13 July 1898 | Wikipedia, Wikidata |
| Architect | A. Page Brown | Wikidata P84 |
| Style | Beaux-Arts / Classical Revival; tower modelled on the Giralda, Seville | Wikipedia |
| Footprint | 201 x 56 m, 9,847 m2 | OSM way/558731934 (measured) |

### 2.2 Sources

- https://www.openstreetmap.org/way/558731934 — footprint, orientation, height tag, address
- https://en.wikipedia.org/wiki/San_Francisco_Ferry_Building — 245 ft tower, 22 ft dials, 660 ft nave, Giralda reference
- https://www.wikidata.org/wiki/Q1408117 — architect, 1898 opening, style
- https://www.ferrybuildingmarketplace.com — owner imagery of the arcade and tower
- https://commons.wikimedia.org/wiki/Category:San_Francisco_Ferry_Building — geolocated west/east elevations, aerials, night views

### 2.3 Orientation and placement

The building runs NE-SW along the Embarcadero: long axis ~54 deg clockwise from true north. The clock tower stands at the centre of the long west facade, facing straight down Market Street; the east (bay) side faces the ferry slips. Author with `+Y` = north and rotate the whole assembly by the measured heading.

### 2.4 What each side shows

**West (Market Street front)** — The hero elevation: continuous two-storey arcade, repeating round-arched openings, strong cornice, tower dead centre with the clock facing the city.

**East (bay side)** — Similar arcade rhythm, plus the later ferry-gate structures that are NOT part of this asset; keep the elevation clean.

**North / South ends** — Short end pavilions, three or four arched bays wide, with the roof gable and cornice returning around the corner.

**Top** — Long low roof with a central clerestory ridge, mechanical clusters, and the tower crown: cornice, open belvedere stage, small dome/cap and flagpole.

### 2.5 Recognition cues (ranked)

1. Extreme horizontal-to-vertical contrast: a 200 m ribbon with one tower
2. Four large white clock faces near the top of the tower
3. Repeating arched arcade at ground level
4. Cream Beaux-Arts stone with a heavy cornice line

### 2.6 Miniature translation

**Preserve**

- The 201 m length and ~15 m cornice height — do not compress the ribbon
- Tower centred on the long axis at 74.7 m total
- Clock faces on all four tower sides, readable from the air
- Arcade arch rhythm along both long elevations

**Simplify / exaggerate**

- Dozens of arches become ~24 arch openings per long side, each a simple extruded arch recess
- The clock face becomes a flat white disc with two chunky beveled hands and four tick blocks — no numerals
- Cornices and mouldings become two or three chunky beveled bands
- The tower belvedere becomes an open colonnade of eight square piers under a simple cap

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Main body: 201 x 56 m box, 15 m tall, `Toy_cream`-equivalent `Toy_sand` walls, rotated to 54 deg.
2. Ground arcade: recess the lower 7 m by 1.2 m and cut 24 arched openings per long side (semicircular top, 3.2 m wide) plus 4 per end. `Toy_ink` behind the arches.
3. Cornice: 1.2 m tall `Toy_trim` band at z=15 projecting 0.8 m, running the full perimeter.
4. Roof: low hipped/clerestory ridge to z=20, `Toy_roofd`, with a continuous raised lantern strip 8 m wide along the centreline.
5. Tower shaft: 16 x 16 m square, z=0 to z=58, `Toy_sand`, with two `Toy_trim` string courses.
6. Clock stage: 18 x 18 m block z=58 to z=66 with a 6.7 m `Toy_white` disc on each face, `Toy_ink` hands, `Toy_trim` surround ring.
7. Belvedere: eight 1.4 m piers z=66 to z=71 supporting a `Toy_trim` cap; small `Toy_roofd` cupola to z=74.7; flagpole 3 m `Toy_steel`.
8. Roof plant: three `Toy_roofd` blocks and one stair penthouse on the long roof.
9. Bevel 0.12 m, 2 segments, everywhere.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | main walls and tower shaft |
| `Toy_trim` | `#f3efe6` | cornices, string courses, clock surrounds, belvedere cap |
| `Toy_ink` | `#3a3530` | arch reveals, clock hands, window darks |
| `Toy_white` | `#f7f4ec` | clock dials |
| `Toy_roofd` | `#45454a` | roof planes, cupola, plant blocks |
| `Toy_steel` | `#9aa0a6` | flagpole |
| `Toy_white_Glow` | `#f7f4ec` | clock dials at night |

Night glow: the four clock dials only — they are lit at night and are the identity cue.

### 2.9 Top surface

The roof is a major surface at this length. Design it: a central lantern ridge running the full nave, three tidy `Toy_roofd` plant clusters, one stair penthouse, and a clean parapet edge. Avoid scattering props — two or three clusters read best from the aerial camera.

### 2.10 Scope

**In the GLB:** the Ferry Building itself: arcade body, clock tower, end pavilions and the ground-floor arcade

**Not in the GLB:** the ferry gates and gangways behind it, Embarcadero Plaza, the Embarcadero roadway, palm trees, streetcars, market stalls, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 24,000. Suggested split: body and arcade ~10k, roof and lantern ~3k, tower ~5k, clocks ~1k, spare ~5k

### 2.12 Draft manifest entry

```json
{
  "id": "ferry-building",
  "file": "ferry-building.glb",
  "anchor": [
    -122.3933697,
    37.7955227
  ],
  "targetHeightM": 74.7,
  "cat": 25,
  "name": "Ferry Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `ferryBuilding` exists procedurally and in `pipeline/lib/landmarks.mjs` (exclusion 120 m, key `7`); manifest id `ferry-building` maps to it via `camelId`.
- The tiles entry has no `height` field today — adding `targetHeightM: 74.7` in the asset manifest is what sets the runtime scale.
- No re-bake needed; the 120 m exclusion already clears the baked block.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the four clock dials
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- The clock tower is often modelled too fat. Check the shaft-to-body proportion against a straight-on west elevation photograph.
- Arch count is a style decision, not a survey; state the number chosen and why.
- The east side's ferry gates are visually attached in photographs but are a separate structure — leaving them out is correct and should be noted.
