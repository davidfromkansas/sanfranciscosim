# Mission Dolores Basilica — SF-SIM asset plan

Two buildings in one asset: the 1918 Churrigueresque basilica and, beside it, the 1791 adobe chapel that is the oldest intact building in San Francisco. The pairing is the story.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/mission-dolores/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `mission-dolores` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4270156, 37.7643402` |
| Target height | **~30 m** at the twin bell towers (*estimated* — OSM tags the eaves at 14 m) |
| OSM footprint | basilica 58.6 x 33.1 m, long axis ~85 deg cw from true north (OSM way/256442760, 1,501 m2); adobe chapel 45.7 x 17.0 m alongside (way/256442765) |
| Triangle cap | 24,000 |
| Category | `8` (Place of worship) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Mission Dolores Basilica GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Mission Dolores Basilica in San Francisco and deliver it
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
8. `docs/asset-plans/mission-dolores.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Cream stucco exterior
- Twin symmetrical bell towers
- Red/orange tiled roof
- Central arched entrance
- Ornate Spanish Colonial/Baroque facade
- Ideally the smaller historic Mission Dolores adobe building immediately beside it

## Research Mission Dolores Basilica independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Basilica tower height (no published figure found) and tower cap shape
- The adobe chapel's four-column facade and its exact offset from the basilica
- Facade ornament: the ornate central bay, rose window and statuary niches

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/mission-dolores/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Mission Dolores Basilica, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the basilica, its twin towers and entrance stair, plus the adjoining adobe chapel.

Do not include unrelated surrounding city geometry: the cemetery and its planting, the parish school, Dolores Street, 16th Street, the surrounding Victorian block, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). Both facades face **north** onto Dolores Street. Author true-world orientation; a north-facing front means the `-Y` rule is inverted, so state that explicitly in `REPORT.md`.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/mission-dolores/build_mission_dolores.py` (deterministic build script),
`artifacts/mission-dolores/mission-dolores.blend`, and `artifacts/mission-dolores/mission-dolores.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`mission-dolores-top.png`, `mission-dolores-north.png`, `mission-dolores-east.png`, `mission-dolores-south.png`,
`mission-dolores-west.png`, plus `mission-dolores-contact-sheet.png` and at least one high
three-quarter aerial beauty render `mission-dolores-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the tiled basilica roof, the two tower caps and the low adobe chapel roof beside it; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `mission-dolores.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/mission-dolores/validation.json` and
`artifacts/mission-dolores/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "mission-dolores",
  "file": "mission-dolores.glb",
  "anchor": [
    -122.4270156,
    37.7643402
  ],
  "targetHeightM": 30,
  "cat": 8,
  "name": "Mission Dolores Basilica",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/mission-dolores.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Basilica built | 1918; designated a minor basilica 1952 | Wikipedia |
| Adobe chapel completed | 1791 — the oldest intact structure in San Francisco | Wikipedia |
| Basilica footprint | 58.6 x 33.1 m, 1,501 m2 | OSM way/256442760 (measured) |
| Adobe footprint | 45.7 x 17.0 m, 604 m2, tagged 8 m tall | OSM way/256442765 (measured) |
| Basilica eaves | 14 m tagged | OSM `height` |
| Tower height | ~30 m | *estimated from photographs* — must be verified |
| Style | Spanish Colonial / Churrigueresque revival | *inferred* — verify |
| Roof | Red-orange clay tile | *inferred* from photography |

### 2.2 Sources

- https://www.openstreetmap.org/way/256442760 — basilica footprint and height tag
- https://www.openstreetmap.org/way/256442765 — 'Old Mission Dolores' adobe footprint and height
- https://en.wikipedia.org/wiki/Mission_San_Francisco_de_As%C3%ADs — the two-building complex, 1791 adobe, 1918 basilica, basilica designation
- https://missiondolores.org — parish material: facade, towers, interior, history
- https://commons.wikimedia.org/wiki/Category:Mission_Dolores — north elevation of both buildings, tower close-ups, aerials

### 2.3 Orientation and placement

Both buildings front north onto Dolores Street, side by side, with the adobe chapel to the east (right as you face them) and the taller basilica to the west. The mapped long axes run ~85 deg cw from true north, i.e. the naves run north-south into the block.

### 2.4 What each side shows

**North (Dolores Street front)** — The whole identity: the basilica's ornate central bay flanked by twin domed-cap bell towers, and immediately east the low adobe chapel with its four-column porch and three small bells in the gable.

**East / West flanks** — Plain cream stucco walls with regular arched windows and buttress-like piers; the basilica's flank is much taller than the adobe's.

**South (rear)** — Apse end and parish additions; keep simple.

**Top** — Two roofs at very different heights: the basilica's long red-tile gable with the tower caps at each front corner, and the adobe's low tile roof beside it.

### 2.5 Recognition cues (ranked)

1. Twin bell towers with domed caps
2. Cream stucco against a red-orange tile roof
3. The ornate central entrance bay
4. The tiny adobe chapel sitting right beside a much larger church

### 2.6 Miniature translation

**Preserve**

- The two-building composition and their real size difference
- Twin towers, symmetric about the central bay
- Red tile roofs on both
- The adobe's four-column facade and gable bells

**Simplify / exaggerate**

- Churrigueresque ornament becomes one recessed decorative panel plus two niche recesses
- Tile roofs become flat `Toy_ioorange` planes with a chunky ridge and eave band — no individual tiles
- Tower caps become simple domes on an octagonal drum with a small cross
- Windows become plain arched recesses

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Basilica body: 33 x 45 m, walls to z=17, gable ridge to z=23, `Toy_cream`.
2. Towers: two 7 x 7 m shafts at the north corners, z=0 to z=24, with an octagonal belfry to z=27 and a dome cap plus cross to z=30.
3. Central bay: 12 m wide projection on the north face, z=0 to z=21, with a 5 m arched entrance recess, a decorative panel above and two niches.
4. Roof: gable, `Toy_ioorange`, with a 0.6 m eave overhang and a chunky ridge cap.
5. Steps: 10 m wide, 5 treads, `Toy_stone`.
6. Adobe chapel: 22 x 12 m body, walls to z=7, low gable to z=9.5, `Toy_cream`, placed to the east with the real ~10 m gap.
7. Adobe porch: four square columns 0.9 m, z=0 to z=6, supporting a flat entablature; three small arched bell openings in the gable above.
8. Windows: 5 arched openings per basilica flank, 2 per adobe flank.
9. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | stucco walls of both buildings |
| `Toy_ioorange` | `#c0402a` | clay tile roofs |
| `Toy_trim` | `#f3efe6` | cornices, entrance surround, decorative panel |
| `Toy_glass` | `#2a4d73` | window recesses |
| `Toy_ink` | `#3a3530` | entrance and bell-opening reveals |
| `Toy_gold` | `#caa64a` | crosses and the small facade accents |
| `Toy_white_Glow` | `#f7f4ec` | facade uplight at night |

Night glow: a single restrained facade uplight band on the north front. Nothing else.

### 2.9 Top surface

Two tile roofs at different heights, seen together from above, are the asset's aerial signature. Give both a proper ridge, eave overhang and a couple of vents, and keep the orange value consistent between them.

### 2.10 Scope

**In the GLB:** the basilica, its twin towers and entrance stair, plus the adjoining adobe chapel

**Not in the GLB:** the cemetery and its planting, the parish school, Dolores Street, 16th Street, the surrounding Victorian block, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 24,000. Suggested split: basilica body and roof ~9k, towers ~5k, central bay ~3k, adobe ~5k, steps/details ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "mission-dolores",
  "file": "mission-dolores.glb",
  "anchor": [
    -122.4270156,
    37.7643402
  ],
  "targetHeightM": 30,
  "cat": 8,
  "name": "Mission Dolores Basilica",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add an entry to `pipeline/lib/landmarks.mjs` (`id: 'missionDolores'`, real lon/lat, `height`, `exclude: ~70`, optional camera preset) and re-bake the affected tiles — otherwise the baked procedural buildings will intersect the GLB.
- Manifest id `mission-dolores` maps to `missionDolores` via `camelId`; there is no procedural builder to hide, so the fallback is simply the baked city block.
- Set `targetHeightM` to the verified tower height, and mark `"estimated": true` if it is still inferred.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the north facade uplight
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- No published tower height was found. This is the biggest open value in the plan — verify it or mark the manifest entry estimated.
- Including the adobe is a judgement call. It is a separate OSM building; the plan includes it because the user asked and because the pairing is the recognition cue. Document the decision.
- Ornate facades tempt over-detailing; the style bible caps this at one panel plus two niches.
