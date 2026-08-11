# Grace Cathedral — SF-SIM asset plan

French Gothic in concrete on Nob Hill: a long cruciform body, twin west towers and a rose window. The style translation is about vertical rib rhythm, not tracery.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/grace-cathedral/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `grace-cathedral` |
| Existing procedural builder | `graceCathedral()` in `app/src/landmarks.js` (no key, exclusion 80 m) |
| WGS84 anchor | `-122.4136014, 37.7918406` |
| Target height | **~53 m** at the twin west towers (OSM `height`=53) |
| OSM footprint | 95.7 x 43.4 m, long axis ~81 deg cw from true north (OSM way/32946942, 2,444 m2); published 329 x 162 ft |
| Triangle cap | 27,000 |
| Category | `8` (Place of worship) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Grace Cathedral GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Grace Cathedral in San Francisco and deliver it
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
8. `docs/asset-plans/grace-cathedral.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Twin Gothic towers
- Large central rose window
- Pointed entrance arches
- Vertical stone ribs
- Flying-buttress-like exterior forms
- Gray stone facade
- Long cruciform body and steep roof

## Research Grace Cathedral independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Tower height vs nave ridge height, and whether the towers carry spires or flat crowns
- Rose window diameter and its position on the east front
- Whether the buttresses are true flying buttresses or engaged piers

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/grace-cathedral/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Grace Cathedral, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the cathedral: nave, transepts, chancel, twin towers, west/east fronts, buttresses and the entrance steps.

Do not include unrelated surrounding city geometry: Huntington Park, the Masonic, the cathedral school and Diocesan House, Taylor and California Streets, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance and rose window face **east** onto Taylor Street; the long axis is nearly east-west. Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/grace-cathedral/build_grace_cathedral.py` (deterministic build script),
`artifacts/grace-cathedral/grace-cathedral.blend`, and `artifacts/grace-cathedral/grace-cathedral.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`grace-cathedral-top.png`, `grace-cathedral-north.png`, `grace-cathedral-east.png`, `grace-cathedral-south.png`,
`grace-cathedral-west.png`, plus `grace-cathedral-contact-sheet.png` and at least one high
three-quarter aerial beauty render `grace-cathedral-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the steep nave roof, crossing, tower tops and buttress rhythm; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `grace-cathedral.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/grace-cathedral/validation.json` and
`artifacts/grace-cathedral/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "grace-cathedral",
  "file": "grace-cathedral.glb",
  "anchor": [
    -122.4136014,
    37.7918406
  ],
  "targetHeightM": 53,
  "cat": 8,
  "name": "Grace Cathedral",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/grace-cathedral.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Length | 329 ft / 100 m | Wikipedia infobox (Structurae) |
| Width | 162 ft / 49 m | Wikipedia infobox (Structurae) |
| Height | 53 m tagged (towers) | OSM `height` — *verify* against a published figure |
| Mapped footprint | 95.7 x 43.4 m, 2,444 m2 | OSM way/32946942 (measured) |
| Architect | Lewis P. Hobart | Wikipedia infobox |
| Style | French Gothic (built in reinforced concrete, 1928-1964) | Wikipedia |
| Doors | Cast replicas of Ghiberti's Gates of Paradise, installed 1964 | Wikipedia |
| Colour | Grey concrete simulating stone | *inferred* — verify |

### 2.2 Sources

- https://www.openstreetmap.org/way/32946942 — footprint, orientation, 53 m height, worship tags
- https://en.wikipedia.org/wiki/Grace_Cathedral,_San_Francisco — 329 x 162 ft, architect, style, construction history, doors
- https://gracecathedral.org — owner material: elevations, rose window, labyrinth, tower imagery
- https://structurae.net/structures/grace-cathedral — dimensional record cited by Wikipedia
- https://commons.wikimedia.org/wiki/Category:Grace_Cathedral,_San_Francisco — east front, side elevations, aerials

### 2.3 Orientation and placement

The nave runs almost due east-west (mapped long axis ~81 deg cw from true north) with the twin-towered entrance front and rose window facing east toward Taylor Street and Huntington Park. The chancel is at the west end.

### 2.4 What each side shows

**East (entrance front)** — The hero elevation: twin towers flanking a tall gabled centre, three pointed portals below, the large rose window above them.

**North / South (nave flanks)** — Long repeating bays: tall pointed windows between projecting buttress piers, a clerestory band above the aisle roof, and the transept gable interrupting the rhythm.

**West (chancel)** — A polygonal apse end, lower and plainer, with radiating buttresses.

**Top** — A long steep gable roof, lower aisle roofs each side, a crossing point, tower crowns, and the buttress tops reading as a regular comb from above.

### 2.5 Recognition cues (ranked)

1. Twin towers on a long cruciform body
2. The big rose window centred between them
3. Repeating buttress piers down both flanks
4. Steep grey roof, unusually monochrome for a landmark

### 2.6 Miniature translation

**Preserve**

- 100 m length and 49 m width
- Twin towers at ~53 m with a clearly lower nave ridge
- Cruciform plan with readable transepts
- Buttress rhythm on both flanks

**Simplify / exaggerate**

- Tracery becomes one recessed pointed opening per bay with a `Toy_trim` surround
- The rose window becomes a recessed disc with 8-12 chunky radial spokes
- Portals become three pointed recesses with a flat tympanum panel
- Pinnacles, crockets and statuary disappear; tower crowns get a simple crenellated cap

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Nave: 70 x 22 m body, walls to z=30, gable ridge to z=38, `Toy_stone`.
2. Aisles: 8 m wide each side, walls to z=16, mono-pitch roofs to z=20.
3. Transepts: 34 x 16 m crossing arms, same wall and ridge heights as the nave.
4. Chancel/apse: polygonal end, 5 facets, radius 12 m, ridge to z=34.
5. Towers: two 12 x 12 m shafts at the east corners, z=0 to z=50, with a 3 m crenellated cap to z=53.
6. Buttresses: 14 piers per flank, 2 x 3.5 m, stepping from z=18 down, with a sloped upper shoulder to fake the flying form.
7. East front: gable wall to z=42 between the towers; rose window disc radius 5.5 m recessed 0.6 m at z=26; three pointed portals below.
8. Windows: one pointed opening per bay, 2.5 x 8 m, recessed 0.4 m, `Toy_glass`.
9. Steps: 18 m wide, 8 treads on the east front, `Toy_stone`.
10. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | all wall surfaces, towers, buttresses |
| `Toy_trim` | `#f3efe6` | window surrounds, string courses, cornice caps |
| `Toy_glass` | `#2a4d73` | window openings |
| `Toy_roofd` | `#45454a` | nave, aisle, transept and apse roofs |
| `Toy_ink` | `#3a3530` | portal recesses |
| `Toy_gold` | `#caa64a` | the bronze Ghiberti doors — one small saturated accent |
| `Toy_white_Glow` | `#f7f4ec` | rose window and portal uplight at night |

Night glow: the rose window face plus a modest wash on the tower crowns. Keep it to two glow surfaces.

### 2.9 Top surface

A large, steep, mostly-uniform roof is a risk from above. Design it: distinct ridge, visible aisle roof steps, a crossing marker, and the buttress comb. A subtle value break between nave and aisle roofs keeps it from reading as one grey slab.

### 2.10 Scope

**In the GLB:** the cathedral: nave, transepts, chancel, twin towers, west/east fronts, buttresses and the entrance steps

**Not in the GLB:** Huntington Park, the Masonic, the cathedral school and Diocesan House, Taylor and California Streets, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: nave/aisles ~8k, transepts and apse ~5k, towers ~4k, buttresses ~5k, east front and rose ~3k, spare ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "grace-cathedral",
  "file": "grace-cathedral.glb",
  "anchor": [
    -122.4136014,
    37.7918406
  ],
  "targetHeightM": 53,
  "cat": 8,
  "name": "Grace Cathedral",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `graceCathedral` exists procedurally and in the registry (exclusion 80 m, no key); manifest id `grace-cathedral` maps to it.
- Set `targetHeightM: 53` (verify the tower height first — the OSM tag is the only figure found).
- Nob Hill has real slope; check the east steps sit on sampled terrain sensibly.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the rose window and tower crowns
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- No authoritative published height was found — only the OSM tag. Verify before committing, and mark `estimated` in the manifest if it stays unconfirmed.
- Gothic detail is a triangle trap. The plan deliberately spends on buttresses and the rose window and nothing else.
- An all-grey model can look dead. The Ghiberti-door gold accent and a slight roof/wall value split are what save it.
