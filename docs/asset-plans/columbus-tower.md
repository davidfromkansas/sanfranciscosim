# Columbus Tower (Sentinel Building) — SF-SIM asset plan

The smallest building in the set and one of the most distinctive: a copper-green flatiron wedge at Columbus and Kearny. Small enough that the whole budget can go into bay windows and the roofline.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/columbus-tower/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `columbus-tower` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4050773, 37.7965842` |
| Target height | **29 m** (OSM `height`, 7-8 storeys) |
| OSM footprint | 17.4 x 15.8 m wedge, ~168 deg cw from true north (OSM way/288485994, 156 m2) |
| Triangle cap | 12,000 |
| Category | `3` (Office / mixed use) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Columbus Tower (Sentinel Building) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Columbus Tower (Sentinel Building) in San Francisco and deliver it
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
8. `docs/asset-plans/columbus-tower.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Narrow triangular/Flatiron footprint
- Distinctive green copper facade
- White bay windows
- Rounded corner bays
- Ornate roofline
- Wedge-shaped form following the Columbus/Kearny intersection

## Research Columbus Tower (Sentinel Building) independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Storey count (Wikidata says 8, OSM says 7) and the true parapet height
- The rounded corner turret/cupola detail at the apex
- Bay-window rhythm on each of the three elevations

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/columbus-tower/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Columbus Tower (Sentinel Building), consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the Sentinel Building itself, including its ground-floor storefronts and roof cornice/turret.

Do not include unrelated surrounding city geometry: Columbus Avenue, Kearny and Jackson Streets, neighbouring buildings, street furniture, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The apex points roughly north-west into the Columbus/Kearny intersection. Author true-world orientation and document the heading; the apex, not a flat face, is the identity.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/columbus-tower/build_columbus_tower.py` (deterministic build script),
`artifacts/columbus-tower/columbus-tower.blend`, and `artifacts/columbus-tower/columbus-tower.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`columbus-tower-top.png`, `columbus-tower-north.png`, `columbus-tower-east.png`, `columbus-tower-south.png`,
`columbus-tower-west.png`, plus `columbus-tower-contact-sheet.png` and at least one high
three-quarter aerial beauty render `columbus-tower-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the wedge plan, the cornice, the apex turret and the roof plant; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `columbus-tower.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/columbus-tower/validation.json` and
`artifacts/columbus-tower/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "columbus-tower",
  "file": "columbus-tower.glb",
  "anchor": [
    -122.4050773,
    37.7965842
  ],
  "targetHeightM": 29,
  "cat": 3,
  "name": "Columbus Tower (Sentinel Building)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/columbus-tower.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Name | Sentinel Building; briefly Columbus Tower 1958-1972 | Wikipedia |
| Completed | 1907 | Wikipedia, Wikidata |
| Height | 29 m | OSM `height` |
| Floors | 7 (OSM) or 8 (Wikidata) above ground | conflicting — *verify* |
| Footprint | 17.4 x 15.8 m, 156 m2 | OSM way/288485994 (measured) |
| Facade | Copper-green oxidised sheet metal with white-painted bay windows | Wikipedia description; colour *inferred* |
| Occupant | American Zoetrope (Francis Ford Coppola) | Wikipedia |
| Landmark status | SF Designated Landmark No. 33 | Wikipedia |

### 2.2 Sources

- https://www.openstreetmap.org/way/288485994 — wedge footprint, 29 m height, 7 levels
- https://en.wikipedia.org/wiki/Sentinel_Building — flatiron form, copper-green facade, 1907, landmark status, Zoetrope
- https://www.wikidata.org/wiki/Q5150141 — 8 floors, 1907 inception
- https://sfplanning.org — SF landmark designation records for Landmark No. 33
- https://commons.wikimedia.org/wiki/Category:Sentinel_Building — apex view, both street elevations, roofline close-ups

### 2.3 Orientation and placement

A triangular lot bounded by Columbus Avenue (north-west), Kearny Street (east) and Jackson Street (south). The acute apex points north-west into the Columbus/Kearny fork; the mapped long axis is ~168 deg cw from true north. Author `+Y` = north and rotate the wedge to match.

### 2.4 What each side shows

**North-west apex** — The hero view: a narrow rounded corner bay running the full height, capped by a small turret/cupola, with the two flanks receding on either side.

**North-east (Columbus)** — Regular rhythm of projecting white bay windows, four to five bays wide, over a storefront base.

**South-east (Kearny)** — The same bay rhythm, slightly longer.

**South (Jackson)** — The short back of the wedge, plainest elevation.

**Top** — A small triangular roof: heavy cornice all round, the apex turret, one or two plant boxes, and a flat deck.

### 2.5 Recognition cues (ranked)

1. The acute triangular plan
2. Oxidised copper-green colour — unique in the neighbourhood
3. White projecting bay windows in a strong vertical rhythm
4. The rounded corner bay and its cap

### 2.6 Miniature translation

**Preserve**

- The true wedge angle from the OSM polygon
- 29 m height with 7-8 readable floors
- The rounded apex bay running full height
- Green wall / white bay colour contrast

**Simplify / exaggerate**

- Ornate cornice becomes two chunky beveled bands
- Bay windows become simple projecting boxes with a `Toy_glass` face and `Toy_white` frame
- The apex turret becomes a short cylinder with a domed cap
- Storefront details become one recessed `Toy_ink` band with `Toy_glass` panels

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the real triangular footprint (rounded at the apex, radius ~3 m) from z=0 to z=26, `Toy_verdigris`.
2. Storefront base: recess the lower 5 m by 0.5 m, `Toy_ink` with `Toy_glass` panels and a `Toy_trim` lintel band.
3. Bays: 4 projecting bays on each long flank, 2.6 m wide, projecting 0.9 m, from z=5 to z=24; `Toy_white` frames, `Toy_glass` faces.
4. Apex bay: rounded, full height z=5 to z=26, 12 segments, same materials.
5. Cornice: two `Toy_trim` bands at z=24.5 and z=26 projecting 0.7 m.
6. Apex turret: cylinder radius 2.4 m, z=26 to z=28, with a dome cap to z=29.
7. Roof: flat `Toy_roofd` deck with a low parapet, one stair penthouse and two plant boxes.
8. Bevel 0.1 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_verdigris` | `#9fb8a8` | copper-green wall surfaces |
| `Toy_white` | `#f7f4ec` | bay window frames |
| `Toy_glass` | `#2a4d73` | bay glazing and storefronts |
| `Toy_trim` | `#f3efe6` | cornice bands and lintels |
| `Toy_ink` | `#3a3530` | storefront recess and reveals |
| `Toy_roofd` | `#45454a` | roof deck, penthouse, plant |
| `Toy_white_Glow` | `#f7f4ec` | the ground-floor cafe front at night |

Night glow: a single small glow at the ground-floor cafe frontage — the building is known for it and it gives the block a life cue.

### 2.9 Top surface

A tiny triangular roof, but the app camera looks right into it. Design it fully: parapet, turret, stair penthouse, two plant boxes and a visible deck surface. At this size a blank roof would be ~40% of the visible asset.

### 2.10 Scope

**In the GLB:** the Sentinel Building itself, including its ground-floor storefronts and roof cornice/turret

**Not in the GLB:** Columbus Avenue, Kearny and Jackson Streets, neighbouring buildings, street furniture, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 12,000. Suggested split: body and storefront ~4k, bays ~4k, apex bay and turret ~2k, roof ~1k, spare ~1k

### 2.12 Draft manifest entry

```json
{
  "id": "columbus-tower",
  "file": "columbus-tower.glb",
  "anchor": [
    -122.4050773,
    37.7965842
  ],
  "targetHeightM": 29,
  "cat": 3,
  "name": "Columbus Tower (Sentinel Building)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'columbusTower'`, `exclude: ~35`) and re-bake, or the baked block building will occupy the same wedge.
- Manifest id `columbus-tower` maps to `columbusTower`.
- At 29 m this is barely landmark-scale; consider whether it deserves a camera preset key or just quiet placement.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 12,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the ground-floor cafe front
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Floor-count sources conflict (7 vs 8). Pick one, cite it, and keep the parapet at the measured 29 m.
- Verdigris is a palette colour but the real building is more saturated; do not drift off-palette to chase the photo.
- The wedge angle must come from the polygon, not from a perspective photograph.
