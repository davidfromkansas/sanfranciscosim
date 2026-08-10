# de Young Museum — SF-SIM asset plan

A long, low, copper-clad Herzog & de Meuron building with one twisting tower. The tower's twist is the whole trick and it is also the whole geometry risk.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/de-young/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `de-young` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4681752, 37.7718982` |
| Target height | **~44 m** at the top of the Hamon Observation Tower (144 ft); the main building is ~13 m |
| OSM footprint | main building 81.0 x 41.5 m, ~171 deg cw from true north (OSM relation/1652482, 1,965 m2 for the mapped part) |
| Triangle cap | 24,000 |
| Category | `16` (Museum) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready de Young Museum GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of de Young Museum in San Francisco and deliver it
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
8. `docs/asset-plans/de-young.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Long angular copper-clad building
- Perforated/textured copper skin
- Weathered brown/green coloration
- Dramatic twisting observation tower rising above the otherwise low structure
- Sharp geometric forms

## Research de Young Museum independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The tower's twist: how many degrees it rotates from base to top and in which direction
- The building's angular plan — it is not a simple rectangle
- The perforated copper pattern and how weathered the skin currently is

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/de-young/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as de Young Museum, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the museum building, its courtyards as recessed voids, and the Hamon Observation Tower.

Do not include unrelated surrounding city geometry: the sculpture garden, Golden Gate Park planting, the Music Concourse, the Academy of Sciences opposite, paths, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance faces the Music Concourse on the south-east. Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/de-young/build_de_young.py` (deterministic build script),
`artifacts/de-young/de-young.blend`, and `artifacts/de-young/de-young.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`de-young-top.png`, `de-young-north.png`, `de-young-east.png`, `de-young-south.png`,
`de-young-west.png`, plus `de-young-contact-sheet.png` and at least one high
three-quarter aerial beauty render `de-young-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the twisting tower head, the low angular roof planes and the courtyard voids; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `de-young.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/de-young/validation.json` and
`artifacts/de-young/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "de-young",
  "file": "de-young.glb",
  "anchor": [
    -122.4681752,
    37.7718982
  ],
  "targetHeightM": 44,
  "cat": 16,
  "name": "de Young Museum",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/de-young.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Current building opened | 2005 (institution 1895) | Wikidata, Wikipedia |
| Architect | Herzog & de Meuron (with Fong & Chan) | Wikidata P84 |
| Observation tower | Hamon Observation Tower, ~144 ft / 44 m, twisting | Wikipedia |
| Mapped footprint | 81.0 x 41.5 m for the mapped part, 1,965 m2 | OSM relation/1652482 (measured; the real building is larger and more angular) |
| Height tag | 13 m | OSM `height` (main mass only) |
| Cladding | Perforated and dimpled copper, now weathered green-brown | Wikipedia; colour *inferred* |

### 2.2 Sources

- https://www.openstreetmap.org/relation/1652482 — mapped footprint, height tag, museum tags
- https://en.wikipedia.org/wiki/De_Young_Museum — 2005 building, Herzog & de Meuron, Hamon Tower 144 ft, copper skin
- https://www.wikidata.org/wiki/Q1181491 — architects, dates
- https://www.famsf.org/visit/de-young — owner material with plans and tower imagery
- https://commons.wikimedia.org/wiki/Category:De_Young_Museum — tower elevations from several sides, copper skin close-ups, aerials showing the plan

### 2.3 Orientation and placement

The building's long axis runs roughly north-south along the Music Concourse (~171 deg cw from true north), with the entrance facing the concourse to the south-east and the tower at the north-east end. Verify the tower's position on the plan — putting it at the wrong end is a highly visible error.

### 2.4 What each side shows

**South-east (concourse front)** — Long low copper elevation with a deep entrance recess and the tower rising beyond.

**North-east** — The tower base and the angular end of the main mass; the twist is most legible from here.

**North-west / south-west** — Long copper walls with slot windows and courtyard openings; largely blank by design.

**Top** — Low angular roof planes with skylight bands, two or three courtyard voids cut through, and the tower's twisted head rising clear of everything.

### 2.5 Recognition cues (ranked)

1. A long, almost windowless copper box
2. The twisting tower — the only twisting structure in the city
3. Weathered green-brown metal colour
4. Sharp, non-rectangular angular plan

### 2.6 Miniature translation

**Preserve**

- The 44 m tower over a ~13 m building — the contrast is the composition
- The tower's twist, visible as a rotating parallelogram profile
- The angular, non-orthogonal plan edges
- Copper colour distinct from every other asset in the diorama

**Simplify / exaggerate**

- The perforated skin becomes a flat copper material; perforation is texture and is forbidden by the contract
- The twist becomes 8-10 lofted cross-sections rotating a total of ~25-40 degrees (verify the real figure)
- Courtyards become two rectangular voids cut into the roof
- Skylight bands become simple recessed strips

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Main mass: extrude the angular plan (trace from imagery, not the simplified OSM box) from z=0 to z=13, `Toy_rust`.
2. Roof: flat `Toy_roofd` with three recessed skylight bands running the long axis.
3. Courtyards: two voids ~18 x 14 m cut through the mass, with `Toy_glass` inner walls.
4. Entrance recess: 24 m wide, 6 m deep notch on the south-east side with a `Toy_glass` wall and a `Toy_trim` soffit.
5. Tower: loft 9 cross-sections from a 22 x 18 m parallelogram at z=0 to a 22 x 18 m section rotated ~30 deg at z=41; `Toy_rust`.
6. Tower head: glazed observation floor z=41 to z=44, `Toy_glass` with `Toy_white` mullions and a flat `Toy_roofd` cap.
7. Slot windows: 6 recessed vertical slots per long elevation, `Toy_glass`.
8. Base band: 1 m `Toy_stone` at grade.
9. Bevel 0.1 m, 2 segments; keep the tower loft edges crisp.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_rust` | `#a86444` | copper cladding, weathered |
| `Toy_verdigris` | `#9fb8a8` | the greener weathered patches — use as a second band, sparingly |
| `Toy_glass` | `#2a4d73` | slot windows, entrance, tower observation floor |
| `Toy_white` | `#f7f4ec` | tower mullions |
| `Toy_roofd` | `#45454a` | roof planes and tower cap |
| `Toy_stone` | `#d9d2c2` | base band |
| `Toy_white_Glow` | `#f7f4ec` | the tower observation floor at night |

Night glow: the tower observation floor. A single glowing box at 44 m over a dark low building is a strong night read.

### 2.9 Top surface

A big low roof plus a tower head. Design the roof: skylight bands, courtyard voids, a couple of plant clusters and a clean parapet edge. The tower head's cap and glazing should read as deliberate from directly above.

### 2.10 Scope

**In the GLB:** the museum building, its courtyards as recessed voids, and the Hamon Observation Tower

**Not in the GLB:** the sculpture garden, Golden Gate Park planting, the Music Concourse, the Academy of Sciences opposite, paths, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 24,000. Suggested split: main mass and plan ~8k, tower loft ~7k, courtyards and entrance ~4k, roof ~3k, spare ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "de-young",
  "file": "de-young.glb",
  "anchor": [
    -122.4681752,
    37.7718982
  ],
  "targetHeightM": 44,
  "cat": 16,
  "name": "de Young Museum",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'deYoung'`, `exclude: ~100`) and re-bake.
- Manifest id `de-young` maps to `deYoung`.
- `targetHeightM: 44` uses the tower, but most of the asset is 13 m — verify the in-app footprint after placement because height-based scaling keys off the tallest point.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the tower observation floor
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- The OSM relation simplifies the plan badly. Trace the real angular outline from aerial imagery instead.
- Getting the twist direction or magnitude wrong is immediately obvious to anyone who knows the building. Verify from two orthogonal photographs.
- Copper is a texture-heavy material in reality; the flat-colour contract means colour choice does all the work. Pick one and stay on-palette.
