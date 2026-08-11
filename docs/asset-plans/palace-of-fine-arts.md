# Palace of Fine Arts — SF-SIM asset plan

The most ornament-heavy subject in the set: a Roman rotunda plus a long curved colonnade. The plan deliberately budgets triangles for repeated columns and spends nothing on sculpture detail beyond blocky silhouettes.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/palace-of-fine-arts/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `palace-of-fine-arts` |
| Existing procedural builder | `palaceOfFineArts()` in `app/src/landmarks.js` (key `8`, exclusion 170 m) |
| WGS84 anchor | `-122.4484012, 37.8029215` |
| Target height | **49.4 m** to the top of the rotunda (162 ft) |
| OSM footprint | rotunda block 67 x 58 m (OSM way/288371295, 2,313 m2); the curved pergola runs ~335 m (1,100 ft) |
| Triangle cap | 27,000 |
| Category | `0` (Miscellaneous / attraction) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Palace of Fine Arts GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Palace of Fine Arts in San Francisco and deliver it
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
8. `docs/asset-plans/palace-of-fine-arts.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Enormous Roman-inspired central rotunda
- Reddish-orange domed roof
- Tall Corinthian columns
- Curved colonnades extending outward
- Ornate sculptural details
- Lagoon immediately surrounding / reflection beneath it

## Research Palace of Fine Arts independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Column count in the rotunda peristyle and in the curved pergola
- The weeping-women capitals on the colonnade boxes
- Where the lagoon edge sits relative to the rotunda base

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/palace-of-fine-arts/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Palace of Fine Arts, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the rotunda, its peristyle, the two curved pergola colonnades, and the low plinth/terrace they stand on.

Do not include unrelated surrounding city geometry: the lagoon water itself (the app's park and water data supplies it), the exhibition hall behind the colonnade unless research shows it reads from the air, trees, paths, swans, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The rotunda's principal axis faces the lagoon to the south-east. Author true-world orientation and document the heading; `-Y` cannot be honoured literally here.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/palace-of-fine-arts/build_palace_of_fine_arts.py` (deterministic build script),
`artifacts/palace-of-fine-arts/palace-of-fine-arts.blend`, and `artifacts/palace-of-fine-arts/palace-of-fine-arts.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`palace-of-fine-arts-top.png`, `palace-of-fine-arts-north.png`, `palace-of-fine-arts-east.png`, `palace-of-fine-arts-south.png`,
`palace-of-fine-arts-west.png`, plus `palace-of-fine-arts-contact-sheet.png` and at least one high
three-quarter aerial beauty render `palace-of-fine-arts-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the dome, the peristyle ring and the roofline of the curved pergola; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `palace-of-fine-arts.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/palace-of-fine-arts/validation.json` and
`artifacts/palace-of-fine-arts/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "palace-of-fine-arts",
  "file": "palace-of-fine-arts.glb",
  "anchor": [
    -122.4484012,
    37.8029215
  ],
  "targetHeightM": 49.4,
  "cat": 0,
  "name": "Palace of Fine Arts",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/palace-of-fine-arts.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Height | 49.4 m (162 ft) at the rotunda | Wikidata P2048 |
| Pergola length | ~1,100 ft / 335 m of curved colonnade | Wikipedia |
| Built / rebuilt | 1915 for the Panama-Pacific Exposition; rebuilt 1964-1974 in concrete | Wikipedia, Wikidata |
| Architect | Bernard Maybeck (with William Gladstone Merchant on the rebuild) | Wikidata P84, Wikipedia |
| Site area | 17 acres | Wikipedia infobox |
| Rotunda footprint | 67 x 58 m, 2,313 m2 | OSM way/288371295 (measured) |
| Materials | Originally staff (plaster/fibre); rebuilt in concrete | Wikidata P186 |
| Colour | Warm ochre/terracotta stone with a reddish-orange tiled dome | *inferred* from photography — verify |

### 2.2 Sources

- https://www.openstreetmap.org/way/288371295 — rotunda footprint, 48 m height tag, 1915 date
- https://en.wikipedia.org/wiki/Palace_of_Fine_Arts — 1,100 ft pergola, rebuild history, Maybeck
- https://www.wikidata.org/wiki/Q966263 — 49.4 m height, architect, materials, style
- https://palaceoffinearts.org — venue material and current imagery
- https://commons.wikimedia.org/wiki/Category:Palace_of_Fine_Arts — aerials showing the colonnade curve, dome close-ups, lagoon views

### 2.3 Orientation and placement

The rotunda opens toward the lagoon on its south-east side, with the two colonnade arms sweeping around to the north-east and south-west. Get the curve direction right from an aerial: mirrored colonnades are an immediately visible error. Author `+Y` = north.

### 2.4 What each side shows

**From the lagoon (south-east)** — The hero view: rotunda framed between the two colonnade arms, dome and peristyle reflected in water.

**North-east / south-west** — The colonnade reads as a long rhythm of paired columns with heavy entablature boxes at intervals.

**North-west (rear)** — The back of the rotunda and the exhibition hall wall; much plainer, largely hidden by trees in reality.

**Top** — Circular dome with a ribbed tile pattern, the peristyle ring around it, and the flat roof strip of the pergola arms.

### 2.5 Recognition cues (ranked)

1. The domed rotunda's silhouette above the treeline
2. The reddish-orange dome against ochre stone
3. Long curved colonnade sweeping away on both sides
4. Massive freestanding columns with heavy entablature boxes

### 2.6 Miniature translation

**Preserve**

- 49 m rotunda height and the dome's diameter relative to the peristyle
- The curve and length of the colonnade arms
- Freestanding columns — they must read as separate cylinders, not a wall
- Chunky entablature boxes at the colonnade intervals

**Simplify / exaggerate**

- Corinthian capitals become a two-step beveled block; no acanthus geometry
- The weeping-women figures become simple blocky silhouettes on top of the entablature boxes, or are dropped entirely if noisy
- Frieze relief and coffering become flat colour changes
- The dome becomes a ribbed hemisphere with 12-16 segments and an oculus ring

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Terrace plinth: rounded platform ~70 x 60 m, 1.5 m tall, `Toy_stone`.
2. Rotunda drum: cylinder radius 15 m, z=1.5 to z=26, `Toy_sand`, with four large arched openings.
3. Peristyle: 16 columns radius 1.4 m, z=1.5 to z=24, ringing the drum at radius 19 m, `Toy_sand`; entablature ring 3 m tall above.
4. Dome: hemisphere radius 15 m from z=29 to z=46, 16 radial ribs, `Toy_ioorange`; oculus ring `Toy_trim`; finial to z=49.4.
5. Colonnade arms: two arcs of 22 paired columns each (radius 1.1 m, 12 m tall) following the real curve, `Toy_sand`.
6. Entablature: continuous 3 m beam over the arms with a chunky box every 4 pairs; boxes carry simple blocky figures.
7. Bevel 0.12 m, 2 segments; keep column segments at 10-12 to control the budget.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | columns, drum, entablature |
| `Toy_ioorange` | `#c0402a` | dome tiles |
| `Toy_trim` | `#f3efe6` | cornices, oculus ring, capitals |
| `Toy_stone` | `#d9d2c2` | terrace plinth and steps |
| `Toy_ink` | `#3a3530` | arch reveals and deep shadow recesses |
| `Toy_mustard` | `#d9a441` | finial accent |
| `Toy_white_Glow` | `#f7f4ec` | uplit dome and colonnade at night |

Night glow: a restrained set: the dome underside/oculus and one band along the colonnade entablature. The Palace is uplit at night and reads warm.

### 2.9 Top surface

The dome IS the roof and it is the single most-seen surface from the app camera. Give it real ribs, an oculus ring and a finial. The colonnade arms need a designed top too: a flat entablature walkway with the box rhythm visible from above.

### 2.10 Scope

**In the GLB:** the rotunda, its peristyle, the two curved pergola colonnades, and the low plinth/terrace they stand on

**Not in the GLB:** the lagoon water itself (the app's park and water data supplies it), the exhibition hall behind the colonnade unless research shows it reads from the air, trees, paths, swans, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: rotunda and dome ~9k, peristyle ~5k, colonnade arms ~10k, terrace ~2k, spare ~1k

### 2.12 Draft manifest entry

```json
{
  "id": "palace-of-fine-arts",
  "file": "palace-of-fine-arts.glb",
  "anchor": [
    -122.4484012,
    37.8029215
  ],
  "targetHeightM": 49.4,
  "cat": 0,
  "name": "Palace of Fine Arts",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `palaceOfFineArts` exists procedurally and in the registry (exclusion 170 m, key `8`); manifest id `palace-of-fine-arts` maps to it.
- Set `targetHeightM: 49.4`. Because the colonnade is far wider than it is tall, verify the loader's height-based scale does not shrink the plan — measure in-app.
- The lagoon is park/water data, so check the model's base plinth height against the sampled terrain after placement.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the dome and colonnade uplight bands
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- This is the highest-risk subject for triangle budget. Columns are cylinders: keep segments low and instance them.
- The colonnade curve is easy to get wrong (mirrored or too shallow) — trace it from an aerial before building.
- Sculptural ornament is where the style bible says stop. If the figures read as noise at aerial distance, remove them.
