# Painted Ladies — SF-SIM asset plan

Six Victorians at 710-720 Steiner Street, modelled as one asset. The subject is the rhythm: identical massing, varied colour, one continuous roofline stepping down the hill.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/painted-ladies/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `painted-ladies` |
| Existing procedural builder | `paintedLadies()` in `app/src/landmarks.js` (no key, exclusion 55 m) |
| WGS84 anchor | `-122.4327400, 37.7761850` |
| Target height | **~12.5 m** to the ridge of each house (OSM tags them at 12 m) |
| OSM footprint | six houses of ~16 x 7 m each, row axis ~171 deg cw from true north, spanning ~38 m along Steiner Street |
| Triangle cap | 27,000 |
| Category | `1` (House) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Painted Ladies GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Painted Ladies in San Francisco and deliver it
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
8. `docs/asset-plans/painted-ladies.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Row of tightly packed Victorian houses
- Colourful individual facades
- Steep roofs
- Projecting bay windows
- Ornate trim and cornices
- Front staircases
- Varied rooflines while preserving the famous side-by-side rhythm

## Research Painted Ladies independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The exact six houses (710, 712, 714, 716, 718, 720 Steiner) and their current colour schemes
- Bay-window type per house (slanted vs square) and gable vs false-front parapet
- The ~1 m per house grade step down Steiner Street

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/painted-ladies/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Painted Ladies, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the six houses at 710-720 Steiner Street, their front stoops and stairs, and their shared party walls.

Do not include unrelated surrounding city geometry: Alamo Square park and its lawn, the street, sidewalk, parked cars, the larger corner house at 700 Steiner unless research says it belongs, trees, people, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The facades face **east** onto Steiner Street and Alamo Square. Author true-world orientation — the `-Y` rule cannot hold; document the heading in `REPORT.md`, because getting this backwards points six front doors at a back yard.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/painted-ladies/build_painted_ladies.py` (deterministic build script),
`artifacts/painted-ladies/painted-ladies.blend`, and `artifacts/painted-ladies/painted-ladies.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`painted-ladies-top.png`, `painted-ladies-north.png`, `painted-ladies-east.png`, `painted-ladies-south.png`,
`painted-ladies-west.png`, plus `painted-ladies-contact-sheet.png` and at least one high
three-quarter aerial beauty render `painted-ladies-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the six steep roof planes, ridge direction and the chimney/parapet rhythm; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `painted-ladies.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/painted-ladies/validation.json` and
`artifacts/painted-ladies/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "painted-ladies",
  "file": "painted-ladies.glb",
  "anchor": [
    -122.43274,
    37.776185
  ],
  "targetHeightM": 12.5,
  "cat": 1,
  "name": "Painted Ladies",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/painted-ladies.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Addresses | 710, 712, 714, 716, 718, 720 Steiner Street | OSM ways 261412896/895/900/894/879/899 |
| Per-house footprint | ~15.9-16.1 x 6.8-7.1 m | OSM (measured) |
| Height | 12 m tagged; ~12.5 m to ridge | OSM `height`; ridge *inferred* |
| Roof | Gabled (720 is tagged hipped) | OSM `roof:shape` |
| Row extent | ~38 m along Steiner from lat 37.77606 to 37.77637 | OSM (measured) |
| Built | 1892-1896, Matthew Kavanaugh | Wikipedia — *verify* |
| Style | Queen Anne Victorian | Wikidata P149 |
| Row centroid | -122.43274, 37.776185 | mean of the six mapped footprints |

### 2.2 Sources

- https://www.openstreetmap.org/way/261412896 (and 895, 900, 894, 879, 899) — per-house footprints, heights, roof shapes
- https://en.wikipedia.org/wiki/Painted_ladies — the term, the Steiner Street row, Queen Anne style
- https://en.wikipedia.org/wiki/Alamo_Square,_San_Francisco — the 'Postcard Row' framing and park relationship
- https://commons.wikimedia.org/wiki/Category:Painted_Ladies_(San_Francisco) — the canonical east elevation, side and aerial views

### 2.3 Orientation and placement

The row runs north-south along the west side of Steiner Street (row axis ~171 deg cw from true north) with all six facades facing east across the street to Alamo Square. The ground falls to the south, so each house sits roughly 0.6-1.0 m below its northern neighbour — that step is a recognition cue, not an error.

### 2.4 What each side shows

**East (Steiner Street front)** — The famous elevation: six near-identical facades, each with a two-storey slanted bay, ornate cornice, gabled or false-front top, and a stoop with a short flight of steps to a raised entry.

**West (rear)** — Plain stacked rear elevations, minimal trim, small rear extensions. Keep simple but not blank.

**North / South ends** — Only the end houses show a side wall; it is flat, mostly windowless, and shows the roof profile.

**Top** — Six steep roof planes running east-west with ridge lines parallel, plus chimneys and small rear-extension roofs. From the aerial camera the roof colour rhythm matters as much as the facades.

### 2.5 Recognition cues (ranked)

1. Six near-identical houses in a tight row, stepping down a hill
2. Individually coloured facades against a shared silhouette
3. Projecting two-storey bay windows repeated six times
4. Steep roofs with ornate cornice and gable trim

### 2.6 Miniature translation

**Preserve**

- Six units, correct spacing, no gaps between party walls
- The grade step along the row
- Bay windows projecting a real ~1 m from the facade
- Individual colour identity per house

**Simplify / exaggerate**

- Victorian ornament becomes three chunky trim bands: cornice, bay cap, and stoop rail
- Windows become simple recessed rectangles with a `Toy_trim` surround; no muntins
- Each stoop becomes one flight of 6-8 chunky steps with a solid balustrade
- Roof shingles, brackets and finials disappear entirely

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Build one parametric house function, call it six times with per-house colour, height and grade offset.
2. House body: 16 x 7 m, z=0 to z=9.5 (front wall), gable to z=12.5.
3. Bay: 4.5 x 1.1 m projection with 45 deg returns, from z=2.5 to z=9.5 on the east face.
4. Cornice: 0.5 m `Toy_trim` band at the top of the front wall, projecting 0.4 m.
5. Gable/false front: alternate between a triangular gable and a flat parapet across the six houses for the varied-roofline cue.
6. Windows: 2 per floor beside the bay, plus 2 in the bay face; recessed 0.15 m.
7. Stoop: 2.5 x 3 m platform at z=1.8 with 7 steps down to the east, solid `Toy_trim` balustrades.
8. Roof: gable, ridge running east-west, pitch ~40 deg, `Toy_roofd`; one chimney per house.
9. Grade: shift each successive house south by 16 m along the row axis and down 0.7 m; the GLB's overall min Z must still be 0.
10. Bevel 0.1 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream / Toy_sand / Toy_mint / Toy_sky / Toy_mustard / Toy_coral` | `#see palette` | one saturated facade colour per house — the documented SF exception to the neutral-architecture rule |
| `Toy_trim` | `#f3efe6` | cornices, window surrounds, bay caps, balustrades — shared across all six for rhythm |
| `Toy_roofd` | `#45454a` | roof planes and chimneys |
| `Toy_glass` | `#2a4d73` | windows |
| `Toy_ink` | `#3a3530` | doorways and deep recesses |
| `Toy_stone` | `#d9d2c2` | stoop bases and foundation band |

Night glow: none, or at most a tiny warm accent at each doorway. Do NOT glow the windows; the row is a daytime subject and glowing windows would break the palette contract's intent.

### 2.9 Top surface

Six steep planes seen straight-on from the app camera. Vary the roof value slightly per house, keep the ridge direction consistent, add one chimney each, and let the rear extensions read as smaller lower roofs. This is where the 'row' rhythm is read from above.

### 2.10 Scope

**In the GLB:** the six houses at 710-720 Steiner Street, their front stoops and stairs, and their shared party walls

**Not in the GLB:** Alamo Square park and its lawn, the street, sidewalk, parked cars, the larger corner house at 700 Steiner unless research says it belongs, trees, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: ~3.5k per house x6 = 21k, plus shared stoops/trim ~3k, spare ~3k

### 2.12 Draft manifest entry

```json
{
  "id": "painted-ladies",
  "file": "painted-ladies.glb",
  "anchor": [
    -122.43274,
    37.776185
  ],
  "targetHeightM": 12.5,
  "cat": 1,
  "name": "Painted Ladies",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `paintedLadies` exists procedurally and in the registry (exclusion 55 m, no camera key); manifest id `painted-ladies` maps to it.
- Set `targetHeightM: 12.5`. Because the loader scales by height, a small error here is very visible on a 16 m-wide house — measure carefully.
- The row sits on a slope but the loader places the whole group at one sampled elevation; verify the south end does not float after placement, and if it does, bake the grade step into the model as planned.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on nothing (optional door lamps only)
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Facing the row the wrong way is the single most likely failure. Verify against the Alamo Square postcard view before exporting.
- Colour choice is subjective and the real houses have been repainted; pick from the project palette and document the mapping rather than eyedropping photographs.
- Six copies of a detailed house blows the triangle budget fast — build one and instance it.
