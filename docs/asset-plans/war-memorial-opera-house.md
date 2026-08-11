# War Memorial Opera House — SF-SIM asset plan

A calm, strongly horizontal Beaux-Arts civic block with a colonnade and arched windows — the counterpoint to City Hall across the plaza. Restraint is the whole brief.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/war-memorial-opera-house/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `opera-house` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4206423, 37.7785955` |
| Target height | **~44 m** at the fly tower (OSM `height`=44); the main cornice is much lower |
| OSM footprint | 103.7 x 73.4 m, ~171 deg cw from true north (OSM way/32865161, 5,928 m2) |
| Triangle cap | 18,000 |
| Category | `17` (Theatre / performing arts) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready War Memorial Opera House GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of War Memorial Opera House in San Francisco and deliver it
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
8. `docs/asset-plans/war-memorial-opera-house.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Monumental symmetrical Beaux-Arts facade
- Cream stone
- Tall classical colonnade
- Repetitive arched windows
- Large central entrance bays
- Flat/low roofline
- Strong horizontal proportions

## Research War Memorial Opera House independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Column count in the Van Ness colonnade and the arched-window bay count
- The fly tower's height and footprint behind the main block
- The near-identical Veterans Building to the north — make sure you are modelling the right one

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/war-memorial-opera-house/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as War Memorial Opera House, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the Opera House block: colonnade, arched-window elevations, entrance bays, cornice, roof and fly tower.

Do not include unrelated surrounding city geometry: the Veterans Building, Davies Symphony Hall, Van Ness Avenue, the memorial court, trees, people, vehicles, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 18,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main facade faces **east** onto Van Ness Avenue. Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/war-memorial-opera-house/build_war_memorial_opera_house.py` (deterministic build script),
`artifacts/war-memorial-opera-house/war-memorial-opera-house.blend`, and `artifacts/war-memorial-opera-house/war-memorial-opera-house.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`war-memorial-opera-house-top.png`, `war-memorial-opera-house-north.png`, `war-memorial-opera-house-east.png`, `war-memorial-opera-house-south.png`,
`war-memorial-opera-house-west.png`, plus `war-memorial-opera-house-contact-sheet.png` and at least one high
three-quarter aerial beauty render `war-memorial-opera-house-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the flat roof planes, the fly tower mass and the parapet rhythm; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `war-memorial-opera-house.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/war-memorial-opera-house/validation.json` and
`artifacts/war-memorial-opera-house/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "opera-house",
  "file": "war-memorial-opera-house.glb",
  "anchor": [
    -122.4206423,
    37.7785955
  ],
  "targetHeightM": 44,
  "cat": 17,
  "name": "War Memorial Opera House",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/war-memorial-opera-house.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Opened | 1932 | Wikipedia infobox, Wikidata |
| Architects | Arthur Brown Jr. and G. Albert Lansburgh | Wikipedia infobox |
| Capacity | 3,146 seated | Wikipedia infobox |
| Footprint | 103.7 x 73.4 m, 5,928 m2 | OSM way/32865161 (measured) |
| Height | 44 m tagged (fly tower) | OSM `height` |
| Style | Beaux-Arts | Wikipedia, Wikidata |
| Twin | Paired with the Veterans Building to the north in a symmetrical civic composition | Wikipedia |

### 2.2 Sources

- https://www.openstreetmap.org/way/32865161 — footprint, height, theatre tags
- https://en.wikipedia.org/wiki/War_Memorial_Opera_House — architects, 1932, capacity, civic-centre context
- https://www.wikidata.org/wiki/Q1930690 — architects, opening, style
- https://sfwarmemorial.org — operator material with elevations and floor plans
- https://commons.wikimedia.org/wiki/Category:War_Memorial_Opera_House — Van Ness elevation, aerials showing the fly tower, night lighting

### 2.3 Orientation and placement

A rectangular block with the long axis roughly north-south (~171 deg cw from true north), front colonnade facing east onto Van Ness Avenue, fly tower and stage house at the rear (west) end. Its twin, the Veterans Building, sits immediately north — verify which polygon you are using.

### 2.4 What each side shows

**East (Van Ness front)** — The hero elevation: a tall colonnade of engaged columns over an arcaded ground floor, five or seven arched entrance bays, heavy cornice, strong symmetry.

**North / South** — Long flanks of repeating arched windows between pilasters, same cornice line; the south flank faces the memorial court.

**West (rear)** — The stage house and fly tower: a tall plain block, much higher than the auditorium roof, largely windowless.

**Top** — Flat roof planes at two levels, the fly tower as a distinct tall box at the west end, parapets and small mechanical clusters.

### 2.5 Recognition cues (ranked)

1. Strong horizontality with a giant-order colonnade
2. Repetitive arched windows in a regular bay rhythm
3. Cream Beaux-Arts stone matching City Hall
4. The fly tower rising quietly behind the calm front

### 2.6 Miniature translation

**Preserve**

- The 104 x 73 m footprint and low cornice with a taller fly tower
- Symmetry about the east-west axis
- The colonnade as freestanding-looking columns, not pilasters
- Arched window rhythm on all visible elevations

**Simplify / exaggerate**

- Column capitals become a two-step beveled block
- Windows become recessed arched openings with a `Toy_trim` surround
- Cornice and balustrade become two chunky bands
- Sculptural and inscription detail is dropped entirely

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: 104 x 73 m block, z=0 to z=26, `Toy_sand`, with a rusticated `Toy_stone` base to z=7.
2. Colonnade (east): 10 columns radius 1.5 m, z=7 to z=22, engaged 0.6 m from the wall, with an entablature band above.
3. Entrance bays: 5 arched openings 5 m wide in the ground floor, `Toy_ink` reveals with `Toy_glass` doors.
4. Arched windows: 12 per long flank, 2.5 x 5 m, recessed 0.4 m, `Toy_glass`.
5. Cornice: 1.5 m `Toy_trim` band at z=26, projecting 1 m, with a 1.2 m parapet above.
6. Auditorium roof: flat `Toy_roofd` at z=28 with a low central raised section.
7. Fly tower: 34 x 26 m block at the west end, z=0 to z=44, `Toy_sand` with a `Toy_trim` cap band and `Toy_roofd` roof.
8. Roof plant: two tidy clusters plus a stair penthouse.
9. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | main walls, colonnade, fly tower |
| `Toy_stone` | `#d9d2c2` | rusticated base and steps |
| `Toy_trim` | `#f3efe6` | cornice, entablature, window surrounds, capitals |
| `Toy_glass` | `#2a4d73` | windows and doors |
| `Toy_ink` | `#3a3530` | entrance reveals |
| `Toy_roofd` | `#45454a` | roof planes, plant, fly-tower roof |
| `Toy_white_Glow` | `#f7f4ec` | colonnade uplight at night |

Night glow: a single uplight band behind the colonnade. Civic restraint.

### 2.9 Top surface

Large flat roofs plus the fly tower. Make the fly tower a deliberate composition element rather than an afterthought, give the auditorium roof a visible raised centre, and keep the plant to two clusters.

### 2.10 Scope

**In the GLB:** the Opera House block: colonnade, arched-window elevations, entrance bays, cornice, roof and fly tower

**Not in the GLB:** the Veterans Building, Davies Symphony Hall, Van Ness Avenue, the memorial court, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 18,000. Suggested split: body and windows ~7k, colonnade ~4k, fly tower ~3k, cornice and parapet ~2k, roof ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "opera-house",
  "file": "war-memorial-opera-house.glb",
  "anchor": [
    -122.4206423,
    37.7785955
  ],
  "targetHeightM": 44,
  "cat": 17,
  "name": "War Memorial Opera House",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'operaHouse'`, `exclude: ~90`) and re-bake.
- Manifest id `opera-house` maps to `operaHouse`.
- Its twin, the Veterans Building, stays procedural — check they still read as a pair after the GLB replaces one of them. If the mismatch is jarring, flag it rather than modelling both.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 18,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the colonnade uplight
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- The Veterans Building is nearly identical and immediately adjacent. Confirm the polygon and the address before modelling.
- A calm symmetrical block is easy to make boring. The colonnade depth and the cornice projection are what give it life.
- Only the OSM height was found; verify the cornice-vs-fly-tower heights from an elevation drawing if one is available.
