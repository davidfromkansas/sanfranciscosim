# Cathedral of Saint Mary of the Assumption — SF-SIM asset plan

Four hyperbolic-paraboloid concrete shells rising to a cross-shaped crown. Pure geometry, almost no ornament — the entire asset is one surface done correctly.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/st-marys-cathedral/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `st-marys-cathedral` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4252894, 37.7839772` |
| Target height | **~58 m** (190 ft) at the cupola crown (*estimated* — OSM tags 18.9 m for the low shell) |
| OSM footprint | site polygon 124.1 x 106.4 m (OSM relation/7814696); the cathedral proper is ~77 x 77 m (*inferred*) |
| Triangle cap | 18,000 |
| Category | `8` (Place of worship) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Cathedral of Saint Mary of the Assumption GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Cathedral of Saint Mary of the Assumption in San Francisco and deliver it
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
8. `docs/asset-plans/st-marys-cathedral.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The extraordinary hyperbolic-paraboloid roof: four enormous curving concrete surfaces sweeping upward and meeting in a cross-like crown
- White concrete
- Low rectangular base
- Very minimal ornamentation

## Research Cathedral of Saint Mary of the Assumption independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The exact cupola height and shell span (published figures around 190 ft / 255 ft square)
- The stained-glass cross that separates the four shells at the crown
- The low plaza/parking podium the cathedral sits on

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/st-marys-cathedral/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Cathedral of Saint Mary of the Assumption, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the cathedral shell, its low base/plaza podium and the entrance canopy.

Do not include unrelated surrounding city geometry: the parish centre and school, the parking structure beyond the podium, Geary Boulevard, trees, people, vehicles, plinths, cameras or lights. Temporary
context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 18,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance faces Geary Boulevard on the south. Author true-world orientation; the form is four-way symmetric so the `-Y` rule is nearly moot — document the decision.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/st-marys-cathedral/build_st_marys_cathedral.py` (deterministic build script),
`artifacts/st-marys-cathedral/st-marys-cathedral.blend`, and `artifacts/st-marys-cathedral/st-marys-cathedral.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`st-marys-cathedral-top.png`, `st-marys-cathedral-north.png`, `st-marys-cathedral-east.png`, `st-marys-cathedral-south.png`,
`st-marys-cathedral-west.png`, plus `st-marys-cathedral-contact-sheet.png` and at least one high
three-quarter aerial beauty render `st-marys-cathedral-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the cross where the four shells meet and the ruled surfaces sweeping down from it; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `st-marys-cathedral.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/st-marys-cathedral/validation.json` and
`artifacts/st-marys-cathedral/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "st-marys-cathedral",
  "file": "st-marys-cathedral.glb",
  "anchor": [
    -122.4252894,
    37.7839772
  ],
  "targetHeightM": 58,
  "cat": 8,
  "name": "Cathedral of Saint Mary of the Assumption",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/st-marys-cathedral.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Dedicated | 1971 | Wikidata inception, Wikipedia |
| Architects | Pietro Belluschi and Pier Luigi Nervi with McSweeney, Ryan & Lee | Wikidata P84 |
| Roof | Four hyperbolic-paraboloid concrete shells meeting in a cross | Wikipedia, Wikidata style `modern` |
| Cupola height | ~190 ft / 58 m | *commonly cited; verify* — OSM only tags 18.9 m |
| Mapped site | 124.1 x 106.4 m, 10,600 m2 | OSM relation/7814696 (measured; includes plaza) |
| Base | Low square travertine-clad base under the shells | *inferred* from photography |
| Material | White reinforced concrete | Wikipedia |

### 2.2 Sources

- https://www.openstreetmap.org/relation/7814696 — site polygon and low-shell height tag
- https://en.wikipedia.org/wiki/Cathedral_of_Saint_Mary_of_the_Assumption_(San_Francisco) — hyperbolic paraboloid description, Nervi/Belluschi, 1971
- https://www.wikidata.org/wiki/Q1049744 — architects, inception, style
- https://www.stmarycathedralsf.org — parish material: the cupola, the cross windows, dimensions
- https://commons.wikimedia.org/wiki/Category:Cathedral_of_Saint_Mary_of_the_Assumption_(San_Francisco) — all four elevations, aerials of the cross crown, interior shell views

### 2.3 Orientation and placement

The building is a square in plan, rotated with the Cathedral Hill grid; the main entrance and steps face south to Geary Boulevard. Because the OSM relation covers the whole site including plaza and parking, derive the cathedral's own square from imagery rather than the polygon.

### 2.4 What each side shows

**All four elevations** — Near-identical: a low horizontal base, then a shell surface that starts almost vertical at the corners and curves inward as it rises, with a full-height glazed slot at the centre of each side.

**South (Geary)** — The entrance side: a wide flight of steps and a low canopy under the shell.

**Top** — The defining view: four ruled surfaces meeting along two crossing ridges, with the glazed cross between them and a small cupola at the intersection.

### 2.5 Recognition cues (ranked)

1. The hyperbolic-paraboloid silhouette — nothing else looks like it
2. White concrete with no ornament
3. The cross formed where the four shells meet
4. A tall dramatic roof on a very low base

### 2.6 Miniature translation

**Preserve**

- The true ruled-surface curvature — a faceted cone or pyramid will not read as this building
- ~58 m crown height over a ~77 m square base
- The four full-height glazed slots between the shells
- The stark white monochrome

**Simplify / exaggerate**

- Generate the hypar surfaces mathematically at a modest resolution (12-16 divisions per edge), then shade flat
- The stained-glass cross becomes a `Toy_glass` strip along each ridge
- Base cladding becomes one flat `Toy_stone` band
- Interior structure, organ and baldachin are not modelled

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Podium: 100 x 100 m plate, 1.5 m tall, `Toy_stone` (trim to the real plaza extent).
2. Base: 77 x 77 m block, z=1.5 to z=12, `Toy_stone`, with recessed `Toy_glass` bands.
3. Shells: four hyperbolic-paraboloid surfaces generated parametrically from the base square edges up to the crown at z=58, thickness ~0.8 m, `Toy_white`. Use `z = a*x*y` ruled patches; 14 divisions per edge is enough.
4. Ridge slots: `Toy_glass` strips 1.6 m wide along the four crossing ridges from base to crown.
5. Cupola: small 6 x 6 x 4 m `Toy_white` cap at the crown with a `Toy_gold` cross to z=62.
6. Entrance canopy: 20 x 6 m flat slab at z=6 on the south side, with 4 chunky piers.
7. Steps: 24 m wide, 8 treads, `Toy_stone`.
8. Bevel: minimal (0.06 m) on the shells so the curvature stays clean; 0.12 m elsewhere.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f7f4ec` | the concrete shells and cupola |
| `Toy_stone` | `#d9d2c2` | base and podium |
| `Toy_glass` | `#2a4d73` | ridge slots and base glazing |
| `Toy_trim` | `#f3efe6` | canopy and edge accents |
| `Toy_gold` | `#caa64a` | crown cross |
| `Toy_white_Glow` | `#f7f4ec` | the ridge slots at night |

Night glow: the four ridge glazing slots — at night the cross of light is the building's signature.

### 2.9 Top surface

The roof is the entire building. Spend the budget here: smooth ruled surfaces, crisp ridges, a correct crown intersection. From the app's aerial camera this asset will be judged almost entirely on the top view.

### 2.10 Scope

**In the GLB:** the cathedral shell, its low base/plaza podium and the entrance canopy

**Not in the GLB:** the parish centre and school, the parking structure beyond the podium, Geary Boulevard, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 18,000. Suggested split: shells ~11k, base and podium ~4k, ridges and cupola ~2k, canopy and steps ~1k

### 2.12 Draft manifest entry

```json
{
  "id": "st-marys-cathedral",
  "file": "st-marys-cathedral.glb",
  "anchor": [
    -122.4252894,
    37.7839772
  ],
  "targetHeightM": 58,
  "cat": 8,
  "name": "Cathedral of Saint Mary of the Assumption",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'stMarysCathedral'`, `exclude: ~90`) and re-bake.
- Manifest id `st-marys-cathedral` maps to `stMarysCathedral`.
- Set `targetHeightM` to the verified cupola height; mark `"estimated": true` if the ~58 m figure cannot be sourced.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 18,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the ridge glazing slots
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- The 58 m height is widely repeated but was not confirmed in a primary source during this research. Verify first.
- A hypar generated with too few divisions reads as a folded paper cone. Test the aerial render before fixing the resolution.
- The OSM footprint is the whole site, not the building. Do not extrude it.
