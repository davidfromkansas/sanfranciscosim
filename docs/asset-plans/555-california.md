# 555 California Street — SF-SIM asset plan

The dark red-brown monolith of the Financial District. Its identity is mass and the faceted bay-window facade — a completely different tower language from Salesforce Tower, which makes it valuable in the skyline.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/555-california/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `555-california` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4037739, 37.7920978` |
| Target height | **237 m** (779 ft), 52 storeys |
| OSM footprint | 84.0 x 44.1 m, ~81 deg cw from true north (OSM way/288511106, 3,457 m2) |
| Triangle cap | 24,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 555 California Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 555 California Street in San Francisco and deliver it
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
8. `docs/asset-plans/555-california.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Huge dark reddish-brown granite mass
- Broad rectangular proportions
- Repetitive vertical window bays
- Stepped/setback upper floors
- Imposing flat roofline
- Large plaza and monolithic base

## Research 555 California Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The faceted bay-window module: how many bays per elevation and how deep they project
- The upper setbacks: how many, on which faces, at what heights
- The plaza and its black granite sculpture (part of the site, likely out of scope)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/555-california/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as 555 California Street, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the tower, its faceted facade, the setbacks, the banking-hall base and the low plaza podium wall.

Do not include unrelated surrounding city geometry: the plaza sculpture and paving beyond the podium, California and Kearny Streets, neighbouring towers, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance faces California Street on the south. Author true-world orientation; the tower is close to grid-aligned so the `-Y` convention is nearly satisfied — document it.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/555-california/build_555_california.py` (deterministic build script),
`artifacts/555-california/555-california.blend`, and `artifacts/555-california/555-california.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`555-california-top.png`, `555-california-north.png`, `555-california-east.png`, `555-california-south.png`,
`555-california-west.png`, plus `555-california-contact-sheet.png` and at least one high
three-quarter aerial beauty render `555-california-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the flat crown, its parapet, the mechanical penthouse and the setback shoulders; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `555-california.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/555-california/validation.json` and
`artifacts/555-california/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "555-california",
  "file": "555-california.glb",
  "anchor": [
    -122.4037739,
    37.7920978
  ],
  "targetHeightM": 237,
  "cat": 3,
  "name": "555 California Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/555-california.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Height | 237 m / 779 ft | Wikipedia; OSM tags 226 m — *conflict, verify* |
| Floors | 52 above ground, 4 below | Wikipedia infobox, Wikidata |
| Completed | 1969 (as Bank of America Center) | Wikipedia, Wikidata |
| Architects | Wurster, Bernardi & Emmons with SOM; Pietro Belluschi consulting | Wikipedia, Wikidata |
| Floor area | 1,969,979 sq ft | Wikipedia infobox |
| Footprint | 84.0 x 44.1 m, 3,457 m2 | OSM way/288511106 (measured) |
| Cladding | Carnelian granite (dark red-brown), faceted bay windows | *inferred*/press — verify |
| Site elevation | ~35 ft above sea level at California and Kearny | Wikipedia |

### 2.2 Sources

- https://www.openstreetmap.org/way/288511106 — footprint, 52 levels, 226 m height tag
- https://en.wikipedia.org/wiki/555_California_Street — 779 ft / 237 m, 52 floors, architects, history
- https://www.wikidata.org/wiki/Q243921 — floors, architects, 1969
- https://www.skyscrapercenter.com/building/555-california-street/1414 — CTBUH height record for the 226 vs 237 conflict
- https://commons.wikimedia.org/wiki/Category:555_California_Street — elevations showing the bay facets and setbacks, aerials of the crown

### 2.3 Orientation and placement

The slab runs along California Street with the long axis ~81 deg cw from true north (the Financial District grid). The main entrance and plaza are on the south/California side. Author `+Y` = north and rotate to the measured yaw.

### 2.4 What each side shows

**South (California Street)** — The entrance elevation over the plaza podium: banking-hall base, then the full faceted shaft.

**North** — The broad back of the slab, same faceted rhythm, with the service core setbacks visible near the top.

**East / West (short ends)** — Narrow but tall; the facets read most strongly here because the bays catch light at an angle.

**Top** — A flat crown with a heavy parapet, a mechanical penthouse block, window-washing track and the stepped shoulders where the upper floors set back.

### 2.5 Recognition cues (ranked)

1. A dark red-brown mass in a skyline of pale towers — colour is the primary cue
2. Faceted vertical bay windows creating a serrated facade
3. Broad slab proportions, not a point tower
4. Flat top with pronounced setbacks

### 2.6 Miniature translation

**Preserve**

- 237 m height with 84 x 44 m plan
- The dark carnelian colour value
- Facet rhythm on all four elevations
- Flat crown and setback shoulders

**Simplify / exaggerate**

- Hundreds of bays become ~20 facet modules per long elevation, modelled as a sawtooth profile extruded full height
- Spandrels become a flat colour change, not geometry
- The banking-hall base becomes one recessed glass band under a heavy granite lintel
- Roof plant becomes two clean penthouse blocks

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Podium: 90 x 50 m plate, 2 m tall, `Toy_stone`, matching the plaza edge.
2. Base: 84 x 44 m, z=2 to z=14, `Toy_rust`, with a recessed `Toy_glass` band at z=4-12 behind chunky piers.
3. Shaft: 84 x 44 m from z=14 to z=200, sawtooth facet profile (20 facets per long face, 10 per short face; facet depth 1.6 m). Material `Toy_rust`.
4. Windows: one `Toy_glass` strip in each facet valley, running the full shaft height, inset 0.3 m.
5. Setbacks: step the plan in by 6 m at z=200 and again by 6 m at z=222.
6. Crown: parapet ring 2 m tall at z=237, `Toy_rust`; `Toy_roofd` deck inside.
7. Penthouse: two blocks 18 x 12 x 8 m and 10 x 8 x 6 m on the crown deck.
8. Beacon: small `Toy_red_Glow` bead at the highest point.
9. Bevel 0.12 m, 2 segments — the facet edges must stay crisp, so keep the bevel small.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_rust` | `#a86444` | granite facade (the closest palette entry to carnelian) |
| `Toy_glass` | `#2a4d73` | window strips and banking-hall glazing |
| `Toy_stone` | `#d9d2c2` | plaza podium |
| `Toy_trim` | `#f3efe6` | lintel and parapet cap accents |
| `Toy_roofd` | `#45454a` | crown deck and penthouse |
| `Toy_red_Glow` | `#c4453c` | aviation beacon |

Night glow: the aviation beacon only, plus optionally a thin crown-parapet line. This tower is deliberately dark at night.

### 2.9 Top surface

A large flat crown is very visible from the app camera. Give it a parapet, two penthouse blocks, a window-washing track line and a couple of vent clusters — organised into two groups, not scattered.

### 2.10 Scope

**In the GLB:** the tower, its faceted facade, the setbacks, the banking-hall base and the low plaza podium wall

**Not in the GLB:** the plaza sculpture and paving beyond the podium, California and Kearny Streets, neighbouring towers, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 24,000. Suggested split: shaft facets ~14k, base and podium ~4k, setbacks and crown ~4k, penthouse/plant ~2k

### 2.12 Draft manifest entry

```json
{
  "id": "555-california",
  "file": "555-california.glb",
  "anchor": [
    -122.4037739,
    37.7920978
  ],
  "targetHeightM": 237,
  "cat": 3,
  "name": "555 California Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '555California'` — note `camelId('555-california')` yields `555California` — with `exclude: ~70`) and re-bake, or the baked tower stays.
- Confirm the id round-trips: `buildings.mjs` kebabs camel ids with `/([a-z0-9])([A-Z])/`, so `555California` -> `555-california`. Verify before relying on it.
- Set `targetHeightM` from the verified height (237 vs 226 must be resolved first).

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the aviation beacon
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Height conflict: Wikipedia says 237 m, OSM says 226 m. Resolve with CTBUH before setting `targetHeightM`.
- `Toy_rust` may read too orange next to the real building. It is the nearest palette colour; do not invent a new one — note the deviation instead.
- A sawtooth extruded full height is cheap but can alias badly at distance. Check the aerial render before committing to 20 facets.
