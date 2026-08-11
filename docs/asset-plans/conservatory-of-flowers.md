# Conservatory of Flowers — SF-SIM asset plan

A white Victorian glasshouse: a central domed pavilion with two arched wings. Delicate in reality, so the plan deliberately fattens every rib to survive at city scale.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/conservatory-of-flowers/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `conservatory-of-flowers` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4601775, 37.7725877` |
| Target height | **~18.3 m** at the dome (60 ft) |
| OSM footprint | 75.0 x 35.2 m, ~81 deg cw from true north (OSM way/30675038, 1,672 m2); published overall length 240 ft |
| Triangle cap | 24,000 |
| Category | `16` (Museum / attraction) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Conservatory of Flowers GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Conservatory of Flowers in San Francisco and deliver it
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
8. `docs/asset-plans/conservatory-of-flowers.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Bright white Victorian greenhouse
- Enormous central glass dome
- Symmetrical wings
- Repeating glass panes and white structural ribs
- Ornate Victorian trim
- Smaller roof vents/turrets
- Landscaped flower beds surrounding it

## Research Conservatory of Flowers independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Rib spacing along the wings and the number of dome ribs
- The vestibule and its gable roof on the south side
- Whether the flower beds should be included at all (see scope)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/conservatory-of-flowers/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Conservatory of Flowers, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the conservatory structure: central pavilion and dome, both wings, the entrance vestibule, roof vents and the low stone plinth it stands on.

Do not include unrelated surrounding city geometry: the formal flower beds and lawn (park data supplies planting; include only a minimal surrounding terrace if research shows it is architecturally integral), John F. Kennedy Drive, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The entrance vestibule faces **south** toward JFK Drive, so the `-Y` front-face rule is naturally satisfied here. Confirm and note it.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/conservatory-of-flowers/build_conservatory_of_flowers.py` (deterministic build script),
`artifacts/conservatory-of-flowers/conservatory-of-flowers.blend`, and `artifacts/conservatory-of-flowers/conservatory-of-flowers.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`conservatory-of-flowers-top.png`, `conservatory-of-flowers-north.png`, `conservatory-of-flowers-east.png`, `conservatory-of-flowers-south.png`,
`conservatory-of-flowers-west.png`, plus `conservatory-of-flowers-contact-sheet.png` and at least one high
three-quarter aerial beauty render `conservatory-of-flowers-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the dome ribs, the barrel-vaulted wing roofs and the vent turrets; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `conservatory-of-flowers.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/conservatory-of-flowers/validation.json` and
`artifacts/conservatory-of-flowers/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "conservatory-of-flowers",
  "file": "conservatory-of-flowers.glb",
  "anchor": [
    -122.4601775,
    37.7725877
  ],
  "targetHeightM": 18.3,
  "cat": 16,
  "name": "Conservatory of Flowers",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/conservatory-of-flowers.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Dome height | nearly 60 ft / ~18.3 m | Wikipedia |
| Overall length | 240 ft / ~73 m of arched wings | Wikipedia; matches the OSM 75 m footprint |
| Opened | 1879 | Wikipedia, Wikidata |
| Manufacturer/style | Lord & Burnham greenhouse; Italianate detailing | Wikidata P84, P149 |
| Dome history | The original saucer dome burned in 1883; the replacement is more domical and 6 ft higher | Wikipedia |
| Footprint | 75.0 x 35.2 m, 1,672 m2 | OSM way/30675038 (measured) |
| Height tag | 15 m | OSM `height` (probably the wing ridge, not the dome) |
| Vestibule | One-storey glazed entry with a gable roof on the south side of the pavilion | Wikipedia |

### 2.2 Sources

- https://www.openstreetmap.org/way/30675038 — footprint, orientation, height tag
- https://en.wikipedia.org/wiki/Conservatory_of_Flowers — 60 ft dome, 240 ft length, 1879, fire history, vestibule
- https://www.wikidata.org/wiki/Q1129107 — Lord & Burnham, Italianate style
- https://conservatoryofflowers.org — operator material with elevations and interior imagery
- https://commons.wikimedia.org/wiki/Category:Conservatory_of_Flowers — south elevation, aerials, dome close-ups

### 2.3 Orientation and placement

The building is symmetric about a north-south axis with the wings running east-west (long axis ~81 deg cw from true north) and the entrance vestibule projecting south toward JFK Drive and the flower beds.

### 2.4 What each side shows

**South (entrance front)** — The hero elevation: central domed pavilion with the projecting gabled vestibule, symmetric arched wings left and right, all white ribs over glass.

**North (rear)** — Similar composition without the vestibule; service doors at the wing ends.

**East / West (wing ends)** — Each wing terminates in a small apsidal or gabled end pavilion.

**Top** — Barrel-vaulted wing roofs running east-west, the ribbed dome in the middle, and a row of small ridge vents/turrets along each wing.

### 2.5 Recognition cues (ranked)

1. The ribbed white dome
2. Perfect bilateral symmetry with two matching arched wings
3. Dense white rib rhythm over glass
4. Small ridge vents punctuating the wing roofs

### 2.6 Miniature translation

**Preserve**

- 18.3 m dome height over ~73 m total length
- Symmetry — both wings must be identical
- Ribs as real geometry, not a texture
- The projecting south vestibule

**Simplify / exaggerate**

- Hundreds of panes become ~40 ribs per wing at a readable 1.8 m spacing
- Victorian ornament becomes a chunky cornice band and simple finials
- Dome ribs reduce to 16 meridians plus two rings
- Vents become 6 small barrel turrets on the ridge

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Plinth: 76 x 36 m, 1.2 m tall, `Toy_stone`, with steps on the south.
2. Wings: two barrel vaults 25 m long x 14 m wide, springing at z=4 to a ridge at z=12, `Toy_glass` with `Toy_white` ribs every 1.8 m and a rib section of 0.45 m (deliberately oversized).
3. Wing end pavilions: 8 x 14 m with a half-dome or gable end.
4. Central pavilion: 20 m diameter drum, z=1.2 to z=8, `Toy_glass` with `Toy_white` mullions.
5. Dome: hemisphere radius 10 m from z=8 to z=17.5, 16 `Toy_white` meridian ribs plus 2 rings, `Toy_glass` panels between; lantern and finial to z=18.3.
6. Vestibule: 8 x 6 m projecting south, gable roof to z=7, `Toy_white` frame and `Toy_glass`.
7. Ridge vents: 6 barrel turrets 2 m long on the wing ridges.
8. Cornice: `Toy_trim` band at the wing eaves and around the drum.
9. Bevel 0.08 m, 2 segments — with this many ribs, bevel cost dominates the budget.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | ribs, mullions, frames, dome meridians |
| `Toy_glassl` | `#6f95b8` | the glazing — a pale glass reads better than dark on a glasshouse |
| `Toy_trim` | `#f3efe6` | cornices and finials |
| `Toy_stone` | `#d9d2c2` | plinth and steps |
| `Toy_mint` | `#8fd0a8` | a hint of interior planting visible through the glass, if used |
| `Toy_white_Glow` | `#f7f4ec` | the dome at night |

Night glow: the dome glazing. The building is lit for events and a glowing dome is a lovely night cue; keep the wings unlit.

### 2.9 Top surface

Barrel vaults plus a dome, seen almost entirely from above by the app camera. The rib rhythm on the vault tops and the vent turret row are the aerial signature — do not flatten them.

### 2.10 Scope

**In the GLB:** the conservatory structure: central pavilion and dome, both wings, the entrance vestibule, roof vents and the low stone plinth it stands on

**Not in the GLB:** the formal flower beds and lawn (park data supplies planting; include only a minimal surrounding terrace if research shows it is architecturally integral), John F. Kennedy Drive, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 24,000. Suggested split: wings and ribs ~12k, dome ~6k, pavilion and vestibule ~3k, plinth and vents ~2k, spare ~1k

### 2.12 Draft manifest entry

```json
{
  "id": "conservatory-of-flowers",
  "file": "conservatory-of-flowers.glb",
  "anchor": [
    -122.4601775,
    37.7725877
  ],
  "targetHeightM": 18.3,
  "cat": 16,
  "name": "Conservatory of Flowers",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'conservatoryOfFlowers'`, `exclude: ~70`) and re-bake.
- Manifest id `conservatory-of-flowers` maps to `conservatoryOfFlowers`.
- Set `targetHeightM: 18.3` (the dome), not the 15 m OSM tag.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the dome glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Rib count vs triangle budget is the central tension. Prototype one wing bay and multiply before committing.
- Thin ribs will alias at city scale; oversizing them is intentional and should be documented.
- Whether to include the flower beds is a genuine scope question — the plan excludes them because park data covers planting, but say so in `REPORT.md`.
