# Oracle Park — SF-SIM asset plan

The largest-footprint asset in the set. A baseball bowl open to the bay: brick outside, green steel inside, with the arcade and the McCovey Cove relationship as the recognition cues. The interior bowl only needs to read from above.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/oracle-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `oracle-park` |
| Existing procedural builder | `oraclePark()` in `app/src/landmarks.js` (no key, exclusion 190 m) |
| WGS84 anchor | `-122.3897993, 37.7786282` |
| Target height | **~45 m** at the highest grandstand/light-tower level (OSM `height`=45) |
| OSM footprint | 212 x 191 m, long axis ~45 deg cw from true north (OSM relation/7325085, 32,754 m2) |
| Triangle cap | 27,000 |
| Category | `0` (Miscellaneous / attraction) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Oracle Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Oracle Park in San Francisco and deliver it
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
8. `docs/asset-plans/oracle-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Large open baseball bowl facing the Bay
- Brick exterior
- Green steel structural details
- Arched waterfront facade
- Recognizable light towers
- Giant scoreboard
- Right-field arcade and wall
- Waterfront promenade and McCovey Cove relationship

## Research Oracle Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Field orientation (home plate bearing) and where the open bay side is
- Light-tower count and positions
- The right-field wall height (24 ft) and arcade arch rhythm

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/oracle-park/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Oracle Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the ballpark: outer brick facade, grandstand bowl, roof canopy, light towers, scoreboard, right-field arcade and wall, and the field surface as a simple graphic.

Do not include unrelated surrounding city geometry: McCovey Cove water, the Lefty O'Doul bridge, Willie Mays Plaza sculptures unless research shows they read, King Street, parking, boats, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance is at Willie Mays Plaza on the north-west (2nd and King) corner; the bowl opens to the bay on the east. Author true-world orientation; document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/oracle-park/build_oracle_park.py` (deterministic build script),
`artifacts/oracle-park/oracle-park.blend`, and `artifacts/oracle-park/oracle-park.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`oracle-park-top.png`, `oracle-park-north.png`, `oracle-park-east.png`, `oracle-park-south.png`,
`oracle-park-west.png`, plus `oracle-park-contact-sheet.png` and at least one high
three-quarter aerial beauty render `oracle-park-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the open bowl, the field diamond graphic, the canopy ring and the light towers; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `oracle-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/oracle-park/validation.json` and
`artifacts/oracle-park/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "oracle-park",
  "file": "oracle-park.glb",
  "anchor": [
    -122.3897993,
    37.7786282
  ],
  "targetHeightM": 45,
  "cat": 0,
  "name": "Oracle Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/oracle-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Opened | 31 March / 11 April 2000 | Wikipedia, Wikidata |
| Architect | Populous (then HOK Sport) | Wikidata P84, Wikipedia |
| Mapped footprint | 212 x 191 m, 32,754 m2 | OSM relation/7325085 (measured) |
| Height | 45 m tagged | OSM `height` |
| Right-field wall | 24 ft / 7.3 m high, honouring Willie Mays | Wikipedia |
| Right-field foul pole | 309 ft from home plate, shortest in the NL | Wikipedia |
| Centre field | 391 ft; right-centre 415 ft ('Triples Alley') | Wikipedia |
| Exterior | Red brick with green painted steel | *inferred* from photography — verify |

### 2.2 Sources

- https://www.openstreetmap.org/relation/7325085 — footprint, orientation, height tag
- https://en.wikipedia.org/wiki/Oracle_Park — dimensions, wall heights, opening, architect, McCovey Cove
- https://www.wikidata.org/wiki/Q298585 — architect, opening date, coordinates
- https://www.mlb.com/giants/ballpark — owner material: seating map, arcade, scoreboard imagery
- https://commons.wikimedia.org/wiki/Category:Oracle_Park — aerials of the bowl, waterfront arcade elevation, light towers

### 2.3 Orientation and placement

The park's long axis measures ~45 deg cw from true north; home plate sits at the west corner with the field opening east-north-east toward the bay, which is why McCovey Cove sits beyond right field. Get the diamond bearing right — from the aerial camera an incorrectly rotated field is obvious.

### 2.4 What each side shows

**North-west (Willie Mays Plaza / 2nd and King)** — The formal entrance: brick piers, arched openings, clock and signage band, tallest grandstand mass behind.

**South-west (King Street)** — Long brick elevation with repeating arched openings and service gates; grandstand roof canopy visible above.

**East (waterfront)** — The signature side: the low right-field arcade with arched openings looking through to the field, the 24 ft wall, and the promenade edge.

**North-east** — Bleachers, scoreboard mass and light towers; the most 'open' part of the ring.

**Top** — An open oval bowl: green field with the brown diamond, concentric seating tiers, a canopy ring over the upper deck, four to six light towers and the scoreboard slab.

### 2.5 Recognition cues (ranked)

1. An open bowl on the waterfront — the only one in the city
2. Red brick perimeter with green steel details
3. The low right-field arcade and its arches
4. Light towers and the big scoreboard breaking the ring

### 2.6 Miniature translation

**Preserve**

- The real footprint and field bearing
- The open (low) east side toward the water
- The tiered bowl profile: tall behind home plate, low in the outfield
- Brick + green colour split

**Simplify / exaggerate**

- Individual seats become three smooth stepped tiers with a colour break, no seat geometry
- The arcade becomes ~16 arch openings in a low brick wall
- Light towers become a mast plus one boxy lamp array each
- The scoreboard becomes one flat slab with a `_Glow` face; no imagery

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Field plate: 200 x 180 m rounded polygon at z=0, `Toy_mint`-adjacent green; inset a `Toy_rust` diamond and base paths as flat inset faces.
2. Bowl: three concentric stepped rings following the real seating bowl — lower tier to z=10, mid to z=22, upper to z=34 on the west/south sides only, tapering to z=12 in the outfield.
3. Outer brick wall: continuous 212 x 191 m perimeter, z=0 to z=22 (west/south) and z=0 to z=10 (east), `Toy_brick`, with a `Toy_trim` cornice band.
4. Arched openings: 16 arches 4 m wide in the east arcade, 20 along King Street.
5. Right-field wall: 7.3 m tall `Toy_verdigris` wall segment along the water side of the field.
6. Canopy: 6 m deep `Toy_steel` roof ring over the upper tier on the west and south, supported by visible green columns.
7. Light towers: six masts 18 m above the canopy with `Toy_roofd` lamp boxes and `Toy_white_Glow` faces.
8. Scoreboard: 30 x 12 m slab on the north-east rim, `Toy_ink` frame, `Toy_white_Glow` face.
9. Entry plaza block: chunky brick piers and a clock at the north-west corner.
10. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | outer facade |
| `Toy_verdigris` | `#9fb8a8` | green structural steel, right-field wall |
| `Toy_trim` | `#f3efe6` | cornice and signage bands |
| `Toy_mint` | `#8fd0a8` | field grass |
| `Toy_rust` | `#a86444` | infield dirt and warning track |
| `Toy_steel` | `#9aa0a6` | canopy and light-tower masts |
| `Toy_ink` | `#3a3530` | seating shadow tiers, scoreboard frame |
| `Toy_white_Glow` | `#f7f4ec` | scoreboard face and light-tower lamps |

Night glow: the scoreboard face and the light-tower lamp arrays. A night ballpark reading as 'lit' is a strong storytelling cue and costs two materials.

### 2.9 Top surface

Almost all of this asset is roof from the app camera. The bowl interior IS the top view: get the field graphic, tier rhythm, canopy ring, light towers and scoreboard placement right and the asset succeeds even if the elevations are plain.

### 2.10 Scope

**In the GLB:** the ballpark: outer brick facade, grandstand bowl, roof canopy, light towers, scoreboard, right-field arcade and wall, and the field surface as a simple graphic

**Not in the GLB:** McCovey Cove water, the Lefty O'Doul bridge, Willie Mays Plaza sculptures unless research shows they read, King Street, parking, boats, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: bowl tiers ~10k, outer wall and arches ~7k, canopy ~4k, light towers and scoreboard ~3k, field graphic ~1k, spare ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "oracle-park",
  "file": "oracle-park.glb",
  "anchor": [
    -122.3897993,
    37.7786282
  ],
  "targetHeightM": 45,
  "cat": 0,
  "name": "Oracle Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `oraclePark` exists procedurally and in the registry (exclusion 190 m, no key); manifest id `oracle-park` maps to it.
- Set `targetHeightM: 45`. Height-based scaling on a 200 m-wide asset amplifies height errors into plan errors — measure the tallest point carefully and re-check the plan size in-app.
- Consider whether the exclusion radius of 190 m still clears every baked footprint once the asset's true extent is known.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the scoreboard and light towers
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Scale error risk is the highest in the set because the loader scales by height, not footprint. Validate the in-app footprint against the OSM polygon.
- The bowl can easily read as a generic stadium. Brick colour, the arcade and McCovey-side openness are what make it Oracle Park.
- Seating tiers modelled literally will blow the budget — three smoothed steps is the plan.
