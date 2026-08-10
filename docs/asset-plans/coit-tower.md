# Coit Tower — SF-SIM asset plan

A single fluted white concrete cylinder — the easiest silhouette in the set and therefore the one where proportion, flute count and the crown arcade do all the work.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/coit-tower/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `coit-tower` |
| Existing procedural builder | `coitTower()` in `app/src/landmarks.js` (key `5`, exclusion 60 m) |
| WGS84 anchor | `-122.4058407, 37.8023762` |
| Target height | **64 m** (210 ft) above its own base on Telegraph Hill |
| OSM footprint | 22.3 x 22.1 m at the base (OSM way/28824850, 395 m2) |
| Triangle cap | 12,000 |
| Category | `0` (Miscellaneous / attraction) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Coit Tower GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Coit Tower in San Francisco and deliver it
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
8. `docs/asset-plans/coit-tower.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Simple white Art Deco concrete cylinder
- Vertical fluting
- Slightly wider observation deck at the top
- Rows of narrow windows near the crown
- Hilltop base so the tower visibly rises above Telegraph Hill

## Research Coit Tower independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Flute count and how the flutes terminate at top and bottom
- The crown arcade: opening count, skylight ring and the deck 32 ft below the top

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/coit-tower/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Coit Tower, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the tower shaft, its crown arcade and the small entrance lobby block at its foot.

Do not include unrelated surrounding city geometry: Pioneer Park, the parking circle, Telegraph Hill itself (the app's terrain supplies it), trees, roads, people, vehicles, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 12,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The tower is a cylinder with one entrance; place the entrance on the real south-east approach from the parking circle and note the `-Y` convention in `REPORT.md`.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/coit-tower/build_coit_tower.py` (deterministic build script),
`artifacts/coit-tower/coit-tower.blend`, and `artifacts/coit-tower/coit-tower.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`coit-tower-top.png`, `coit-tower-north.png`, `coit-tower-east.png`, `coit-tower-south.png`,
`coit-tower-west.png`, plus `coit-tower-contact-sheet.png` and at least one high
three-quarter aerial beauty render `coit-tower-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the crown arcade, skylight ring and observation deck; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `coit-tower.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/coit-tower/validation.json` and
`artifacts/coit-tower/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "coit-tower",
  "file": "coit-tower.glb",
  "anchor": [
    -122.4058407,
    37.8023762
  ],
  "targetHeightM": 64,
  "cat": 0,
  "name": "Coit Tower",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/coit-tower.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Height | 64 m / 210 ft | Wikidata P2048, OSM `height` |
| Structure | Three nested concrete cylinders; outer fluted shaft is 180 ft | Wikipedia |
| Observation deck | 32 ft below the top, arcade and skylights above it | Wikipedia |
| Built | 1932-1933 | Wikipedia, OSM `start_date` |
| Architect | Arthur Brown Jr. and Henry Temple Howard | Wikipedia, OSM `architect` |
| Material / colour | Unpainted reinforced concrete, tagged `#E0E0E0` | OSM `building:material`, `building:colour` |
| Base footprint | 22.3 x 22.1 m, 395 m2 (includes the lobby block) | OSM way/28824850 (measured) |
| Hilltop elevation | Telegraph Hill summit ~84 m | *inferred* — the app samples terrain, so the GLB still starts at z=0 |

### 2.2 Sources

- https://www.openstreetmap.org/way/28824850 — footprint, 64 m height, concrete material, architect, 1933
- https://en.wikipedia.org/wiki/Coit_Tower — nested cylinders, 180 ft fluted shaft, deck 32 ft below top, arcade and skylights
- https://www.wikidata.org/wiki/Q1107297 — height, Art Deco style, architect
- https://sfrecpark.org/facilities/facility/details/Coit-Tower-290 — city operator material
- https://commons.wikimedia.org/wiki/Category:Coit_Tower — elevations from all sides, crown close-ups, aerials

### 2.3 Orientation and placement

A cylinder has no meaningful heading, but the entrance and lobby block do: they face the parking circle on the south-east side. Author `+Y` = north, place the lobby accordingly, and let the app's terrain sampling put the base on the hilltop — the GLB must still have min Z = 0.

### 2.4 What each side shows

**All four elevations** — Nearly identical: a slightly tapering fluted cylinder, unbroken for most of its height, with small window slots near the crown.

**South-east** — The only elevation with the entrance: a low rectangular lobby block with a recessed doorway and the phoenix relief above it (simplify to a flat panel).

**Top** — A wider crown ring with tall arched openings all round, a skylight/lantern band above, and a flat cap with a rail.

### 2.5 Recognition cues (ranked)

1. Plain white cylinder with a subtly wider crown
2. Vertical fluting running the full shaft
3. The arched arcade openings at the top
4. Reading as a tower on a hill, not a tower on flat ground

### 2.6 Miniature translation

**Preserve**

- 64 m height and ~14 m shaft diameter (the 22 m footprint includes the lobby)
- Slight upward taper of the shaft
- Crown wider than the shaft
- Unbroken flute rhythm

**Simplify / exaggerate**

- Fluting becomes 24-32 shallow vertical channels, cut as geometry, not texture
- The crown arcade becomes 12 arched openings with a solid ring above and below
- The phoenix relief becomes one flat `Toy_trim` panel over the door
- Interior murals, elevator core and stair are not modelled at all

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Shaft: cylinder, 24 segments, radius 7.4 m at base tapering to 6.9 m at z=52, `Toy_white`.
2. Flutes: 28 vertical half-round channels 0.35 m deep, from z=3 to z=50.
3. Crown ring: cylinder radius 8.4 m, z=52 to z=60, with 12 arched openings 2.2 m wide; `Toy_white` outside, `Toy_ink` reveals.
4. Skylight band: radius 8.0 m, z=60 to z=62, `Toy_glass` panels between `Toy_white` mullions.
5. Cap: flat disc z=62 to z=64 with a low `Toy_steel` rail.
6. Lobby block: 12 x 8 x 6 m on the south-east side, `Toy_white`, recessed `Toy_ink` doorway, `Toy_trim` relief panel above.
7. Base plinth: radius 9 m, 1.2 m tall, `Toy_stone`.
8. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | shaft, crown, lobby walls |
| `Toy_ink` | `#3a3530` | arch reveals, doorway, window slots |
| `Toy_glass` | `#2a4d73` | skylight band |
| `Toy_trim` | `#f3efe6` | relief panel, string courses |
| `Toy_stone` | `#d9d2c2` | base plinth |
| `Toy_steel` | `#9aa0a6` | cap rail |
| `Toy_white_Glow` | `#f7f4ec` | crown arcade at night |

Night glow: the crown arcade band — the tower is floodlit at night and the crown is what reads.

### 2.9 Top surface

Small but highly visible from above: give the cap a designed ring — rail, a central skylight lantern and a flat deck surface in a slightly darker `Toy_stone` so it does not blow out white.

### 2.10 Scope

**In the GLB:** the tower shaft, its crown arcade and the small entrance lobby block at its foot

**Not in the GLB:** Pioneer Park, the parking circle, Telegraph Hill itself (the app's terrain supplies it), trees, roads, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 12,000. Suggested split: shaft and flutes ~6k, crown and arcade ~3k, lobby and plinth ~2k, spare ~1k

### 2.12 Draft manifest entry

```json
{
  "id": "coit-tower",
  "file": "coit-tower.glb",
  "anchor": [
    -122.4058407,
    37.8023762
  ],
  "targetHeightM": 64,
  "cat": 0,
  "name": "Coit Tower",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `coitTower` exists procedurally and in the pipeline registry (exclusion 60 m, key `5`); manifest id `coit-tower` maps to it.
- The tiles entry has no `height`; set `targetHeightM: 64` in the asset manifest.
- The base sits on sampled terrain — verify in-app that the tower does not float or sink on the hill crown after placement.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the crown arcade
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Under-tapering or over-tapering the shaft is the most common failure; check against a straight-on elevation.
- The 22 m OSM footprint is the whole base including the lobby — do not use it as the shaft diameter.
- At 64 m the tower is small relative to the city camera; the crown must be exaggerated slightly or it disappears.
