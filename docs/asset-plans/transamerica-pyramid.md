# Transamerica Pyramid — SF-SIM asset plan

San Francisco's most photographed silhouette: a 48-storey white quartz-aggregate pyramid with two structural 'wings' and a hollow 64 m spire. The whole asset is one shape, so the plan spends its budget on the taper, the wings and the window grid.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/transamerica-pyramid/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `transamerica` |
| Existing procedural builder | `transamerica()` in `app/src/landmarks.js` (key `4`, exclusion 70 m) |
| WGS84 anchor | `-122.4026508, 37.7951872` |
| Target height | **260 m** architectural (853 ft, spire included) |
| OSM footprint | 54.5 x 54.3 m square, facade axes ~81 deg / 171 deg cw from true north (OSM way/24222973, 2,953 m2) |
| Triangle cap | 24,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Transamerica Pyramid GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Transamerica Pyramid in San Francisco and deliver it
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
8. `docs/asset-plans/transamerica-pyramid.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Steep four-sided pyramidal silhouette
- Pale white/gray precast quartz-aggregate facade
- Dense vertical window grid
- Two wing-like structural projections on the east and west faces of the upper floors
- Narrow illuminated spire

## Research Transamerica Pyramid independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Where the two wings start and stop, and which faces they sit on
- How the spire meets the pyramid and how it is lit at night

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/transamerica-pyramid/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Transamerica Pyramid, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the pyramid, its two wings, the spire, and the chunky ground-level colonnade/lobby that belongs to the tower.

Do not include unrelated surrounding city geometry: Transamerica Redwood Park and its trees, neighbouring buildings, roads, general landscaping, people, vehicles, plinths, studio backgrounds, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The pyramid is four-way symmetric, so put the entrance/identity cue on the real Montgomery Street (north-east) face and treat the `-Y` front rule as satisfied by the documented convention used for Salesforce Tower.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/transamerica-pyramid/build_transamerica_pyramid.py` (deterministic build script),
`artifacts/transamerica-pyramid/transamerica-pyramid.blend`, and `artifacts/transamerica-pyramid/transamerica-pyramid.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`transamerica-pyramid-top.png`, `transamerica-pyramid-north.png`, `transamerica-pyramid-east.png`, `transamerica-pyramid-south.png`,
`transamerica-pyramid-west.png`, plus `transamerica-pyramid-contact-sheet.png` and at least one high
three-quarter aerial beauty render `transamerica-pyramid-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the spire base, the crown of the pyramid and the wing tops; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `transamerica-pyramid.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/transamerica-pyramid/validation.json` and
`artifacts/transamerica-pyramid/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "transamerica",
  "file": "transamerica-pyramid.glb",
  "anchor": [
    -122.4026508,
    37.7951872
  ],
  "targetHeightM": 260,
  "cat": 3,
  "name": "Transamerica Pyramid",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/transamerica-pyramid.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 600 Montgomery Street | OSM tags, owner site |
| Architectural height | 260 m / 853 ft | Wikidata P2048, CTBUH |
| Pyramid structure top | ~195 m (641 ft); the top 212 ft is the hollow spire | Wikipedia body text — *verify* |
| Floors | 48 | OSM `building:levels`, Wikipedia |
| Completed | 1972 | OSM `start_date`, Wikidata |
| Architect | William L. Pereira & Associates | Wikidata P84 |
| Footprint | 54.5 x 54.3 m, 2,953 m2 at grade | OSM way/24222973 (measured) |
| Facade | Precast quartz-aggregate panels, near-white | Wikidata material `quartz` |
| Wings | Two vertical projections from ~29th floor: east elevator shaft, west stair/smoke tower | *inferred* from elevations — verify |

### 2.2 Sources

- https://www.openstreetmap.org/way/24222973 — footprint, height 260, 48 levels, pyramidal roof tag, address
- https://en.wikipedia.org/wiki/Transamerica_Pyramid — height, spire proportion, wings, architect, history
- https://www.wikidata.org/wiki/Q216865 — 260 m height, architect, 1969 inception, quartz cladding
- https://transamericapyramid.com — owner material, recent lobby/plaza renovation imagery
- https://www.skyscrapercenter.com/building/transamerica-pyramid/1409 — CTBUH height definitions (architectural vs tip)
- https://commons.wikimedia.org/wiki/Category:Transamerica_Pyramid — geolocated elevations, aerials and night shots

### 2.3 Orientation and placement

The mapped footprint sits on the Financial District grid: facade normals measure about 81 deg / 171 deg clockwise from true north, i.e. roughly 9 deg off cardinal. Author with Blender `+Y` = north and rotate the square plan by that measured yaw so the model lands on its real heading — the loader never rotates. The main entrance and the taller wing face the Montgomery Street (north-east) side.

### 2.4 What each side shows

**North** — Clay Street side; full unbroken taper, dense vertical window ribbon, wing reads in profile at the right edge.

**East** — The east wing (elevator shaft) breaks the silhouette as a narrow vertical fin from roughly two-thirds height to the crown.

**South** — Washington/California approach; the most common postcard view, taper reads pure with both wings in profile.

**West** — The west wing (stair/smoke tower) mirrors the east one; slightly slimmer in most photographs.

**Top** — A small flat crown platform, the spire base collar, aviation lighting and the tops of both wings; from above the plan is a square rotated to the street grid.

### 2.5 Recognition cues (ranked)

1. The steep four-sided pyramid — nothing else in SF has this silhouette
2. Near-white precast facade against dark, very narrow vertical windows
3. The two wings breaking the upper taper
4. The thin spire continuing the apex line, lit at night

### 2.6 Miniature translation

**Preserve**

- 260 m overall height and the ~54 m square base
- The constant taper angle — resist rounding or bending it
- Both wings, positioned on the correct faces
- The vertical (not horizontal) facade rhythm

**Simplify / exaggerate**

- 48 floor lines become ~14-18 window columns per face as inset dark strips, not individual panes
- The precast panel joints disappear entirely; the facade is one flat cream surface with recessed window channels
- The spire becomes a single tapered prism with a small glow tip
- The plaza colonnade becomes 8-10 chunky beveled piers under a recessed lobby band

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Square base plate 54 x 54 m, 6 m tall, `Toy_stone`, rotated to the measured yaw.
2. Main pyramid: square frustum from 54 m at z=6 to ~5 m at z=195, `Toy_trim`. Model as a single lofted shell with beveled corner edges.
3. Window channels: per face, 15 evenly spaced vertical inset strips (0.9 m wide, 0.35 m deep) running from z=20 to the point where the face narrows below 8 m. `Toy_glass`.
4. East wing: 5.5 x 3.5 m vertical prism hugging the east face from z=105 to z=200, capped flat, `Toy_trim`.
5. West wing: same profile, z=105 to z=190.
6. Crown collar: 6 x 6 x 3 m block at z=195, `Toy_steel`.
7. Spire: tapered prism 4 m to 1.2 m square, z=198 to z=258, `Toy_trim`; final 2 m `Toy_white_Glow`; a 0.8 m `Toy_red_Glow` bead at the tip.
8. Ground colonnade: 10 piers 2.5 x 2.5 x 8 m around the base perimeter, `Toy_stone`, with a recessed `Toy_glass` lobby band behind them.
9. Bevel every exposed edge 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_trim` | `#f3efe6` | pyramid shell, wings, spire |
| `Toy_glass` | `#2a4d73` | window channels and lobby glazing |
| `Toy_stone` | `#d9d2c2` | base plate and colonnade piers |
| `Toy_steel` | `#9aa0a6` | crown collar and small roof plant |
| `Toy_white_Glow` | `#f7f4ec` | upper spire |
| `Toy_red_Glow` | `#c4453c` | aviation beacon |

Night glow: the top ~2 m of the spire plus the beacon bead. The window channels stay non-emissive.

### 2.9 Top surface

There is almost no roof — but the crown platform, wing tops and spire collar are exactly what the aerial camera sees. Give the crown a small designed cluster: a railed platform ring, two low `Toy_roofd` plant blocks, and the spire collar. Keep it under 400 triangles.

### 2.10 Scope

**In the GLB:** the pyramid, its two wings, the spire, and the chunky ground-level colonnade/lobby that belongs to the tower

**Not in the GLB:** Transamerica Redwood Park and its trees, neighbouring buildings, roads, general landscaping, people, vehicles, plinths, studio backgrounds, cameras or lights

### 2.11 Triangle budget

Cap 24,000. Suggested split: shell and window channels ~12k, wings ~2k, spire and crown ~2k, base/colonnade ~5k, spare ~3k

### 2.12 Draft manifest entry

```json
{
  "id": "transamerica",
  "file": "transamerica-pyramid.glb",
  "anchor": [
    -122.4026508,
    37.7951872
  ],
  "targetHeightM": 260,
  "cat": 3,
  "name": "Transamerica Pyramid",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `transamerica` already exists as a procedural builder and in `pipeline/lib/landmarks.mjs` (exclusion 70 m, camera key `4`), so the manifest id `transamerica` will hide the procedural version automatically once the GLB loads.
- No pipeline re-bake is needed: the exclusion zone already clears the baked footprint.
- Keep `targetHeightM` at 260 so the loader's `targetHeightM / measuredHeight` scale stays ~1.0.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the spire tip and beacon
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Sources disagree on where the pyramid ends and the spire begins (641 ft vs 853 ft). Model the transition, and say which number you used for what in `REPORT.md`.
- The wings are easy to place on the wrong faces — check at least two geolocated photographs from known directions before committing.
- A pure geometric pyramid can read as generic low-poly. The window rhythm, base colonnade and wings are what make it Transamerica.
