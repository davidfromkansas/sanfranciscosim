# One Rincon Hill — SF-SIM asset plan

A very slender residential tower with an exposed crown — and a decision to make: the complex is two towers sharing a podium. This plan models the South Tower as the hero and treats the North Tower as optional.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/one-rincon-hill/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `one-rincon-hill` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3921820, 37.7857621` |
| Target height | **195 m** (641 ft) for the South Tower, 60 storeys |
| OSM footprint | 32.1 x 22.3 m, ~134 deg cw from true north (OSM way/944990390, 604 m2) |
| Triangle cap | 18,000 |
| Category | `2` (Apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready One Rincon Hill GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of One Rincon Hill in San Francisco and deliver it
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
8. `docs/asset-plans/one-rincon-hill.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Extremely tall, slender rectangular residential tower
- Blue-gray glass
- Strong vertical facade lines
- Projecting balconies
- Flat roof
- Prominent external diagonal damping structure/crown near the top

## Research One Rincon Hill independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The crown structure: it houses a tuned liquid mass damper; confirm the diagonal bracing geometry from photographs
- Whether to include the North Tower (541 ft) and the shared townhouse podium
- Balcony pattern: which faces carry them and at what rhythm

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/one-rincon-hill/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as One Rincon Hill, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the South Tower and its podium base; optionally the North Tower and the shared townhouse podium if research shows the pair reads better in the skyline.

Do not include unrelated surrounding city geometry: the Bay Bridge approach ramps, Rincon Hill streets, neighbouring towers, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The tower's broad faces look north-east (bay/bridge) and south-west. Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/one-rincon-hill/build_one_rincon_hill.py` (deterministic build script),
`artifacts/one-rincon-hill/one-rincon-hill.blend`, and `artifacts/one-rincon-hill/one-rincon-hill.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`one-rincon-hill-top.png`, `one-rincon-hill-north.png`, `one-rincon-hill-east.png`, `one-rincon-hill-south.png`,
`one-rincon-hill-west.png`, plus `one-rincon-hill-contact-sheet.png` and at least one high
three-quarter aerial beauty render `one-rincon-hill-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the crown truss, the flat roof deck and the mechanical penthouse; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `one-rincon-hill.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/one-rincon-hill/validation.json` and
`artifacts/one-rincon-hill/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "one-rincon-hill",
  "file": "one-rincon-hill.glb",
  "anchor": [
    -122.392182,
    37.7857621
  ],
  "targetHeightM": 195,
  "cat": 2,
  "name": "One Rincon Hill",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/one-rincon-hill.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| South Tower height | 195 m / 641 ft above Fremont and Harrison | Wikipedia |
| North Tower height | 165 m / 541 ft | Wikipedia |
| Floors | 60 above ground (sources vary 55-62) | Wikipedia, Wikidata |
| Completed | 2008 | Wikidata, Wikipedia |
| Architect | Solomon Cordwell Buenz | Wikidata P84 |
| Footprint | 32.1 x 22.3 m, 604 m2 | OSM way/944990390 (measured) |
| Hill elevation | site is 100+ ft above sea level, so apparent height exceeds 700 ft | Wikipedia |
| Damper | Tuned liquid mass damper near the top; the crown expresses it | Wikipedia — *verify the visual form* |

### 2.2 Sources

- https://www.openstreetmap.org/way/944990390 — South Tower footprint, 195 m, 60 levels
- https://en.wikipedia.org/wiki/One_Rincon_Hill — both tower heights, floor-count disputes, damper, hill elevation
- https://www.wikidata.org/wiki/Q3352644 — architect, 2008, floors
- https://www.skyscrapercenter.com/building/one-rincon-hill-south-tower/1425 — CTBUH height record
- https://commons.wikimedia.org/wiki/Category:One_Rincon_Hill — skyline views showing the crown, close-ups of the bracing, both towers together

### 2.3 Orientation and placement

The South Tower's mapped long axis is ~134 deg cw from true north — it sits on the Rincon Hill grid, rotated well off cardinal, with broad faces to the north-east and south-west. Author `+Y` = north and apply the measured yaw.

### 2.4 What each side shows

**North-east (bay/bridge)** — The face most seen from downtown: continuous vertical mullion lines, balcony bands, and the crown truss silhouetted at the top.

**South-west** — Mirror composition, slightly more solid where the service core sits.

**North-west / south-east (narrow ends)** — The slenderness reads most extremely here; almost pure glass with a strong vertical spine.

**Top** — A flat roof with the crown truss framing it, the damper enclosure, mechanical penthouse and a beacon.

### 2.5 Recognition cues (ranked)

1. Extreme slenderness — a knife-edge tower on a hill
2. The white external crown truss with diagonal bracing
3. Cool blue-grey glass with strong vertical lines
4. Stacked balcony bands

### 2.6 Miniature translation

**Preserve**

- 195 m over a 32 x 22 m plan — the aspect ratio IS the building
- The crown truss as a distinct, open structure
- Vertical emphasis over horizontal floor bands
- The blue-grey glass value

**Simplify / exaggerate**

- 60 floors become continuous vertical mullion ribs plus a subtle horizontal band every ~10 floors
- Balconies become 4-6 projecting bands rather than one per floor
- The crown truss becomes 8-12 chunky diagonal members on a rectangular frame
- Podium townhouses become one simple stepped base block

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Podium: 46 x 34 m block, z=0 to z=14, `Toy_stone` with `Toy_glass` bands — the shared townhouse base, simplified.
2. Shaft: 32 x 22 m from z=14 to z=180, `Toy_glass` with `Toy_white` vertical mullion ribs every 3 m projecting 0.3 m.
3. Balcony bands: 6 projecting slabs 1.2 m deep at even intervals, `Toy_white`.
4. Corner spine: a slightly proud `Toy_white` vertical strip at each corner to sharpen the silhouette.
5. Crown frame: open rectangular frame 34 x 24 m, z=180 to z=195, `Toy_white`, with 10 diagonal members 1.2 m section.
6. Damper enclosure: 12 x 8 x 6 m `Toy_steel` box inside the crown frame.
7. Roof deck: `Toy_roofd` with a small penthouse and a `Toy_red_Glow` beacon.
8. Optional North Tower: same recipe at 165 m, 28 x 20 m plan, sharing the podium.
9. Bevel 0.1 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_glass` | `#2a4d73` | curtain wall |
| `Toy_glassl` | `#6f95b8` | a lighter glass band to break up the shaft |
| `Toy_white` | `#f7f4ec` | mullion ribs, balcony slabs, crown truss |
| `Toy_stone` | `#d9d2c2` | podium |
| `Toy_steel` | `#9aa0a6` | damper enclosure |
| `Toy_roofd` | `#45454a` | roof deck and penthouse |
| `Toy_red_Glow` | `#c4453c` | aviation beacon |
| `Toy_white_Glow` | `#f7f4ec` | crown truss lighting at night |

Night glow: the crown truss and the beacon. The crown is lit and is the tower's night identity.

### 2.9 Top surface

The roof sits inside the crown frame, so from above you see the frame, the damper box, the penthouse and the deck together. Compose those four elements deliberately — this is the most distinctive top surface in the set after Sutro.

### 2.10 Scope

**In the GLB:** the South Tower and its podium base; optionally the North Tower and the shared townhouse podium if research shows the pair reads better in the skyline

**Not in the GLB:** the Bay Bridge approach ramps, Rincon Hill streets, neighbouring towers, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 18,000. Suggested split: shaft and ribs ~8k, balconies ~2k, crown truss ~4k, podium ~3k, roof ~1k

### 2.12 Draft manifest entry

```json
{
  "id": "one-rincon-hill",
  "file": "one-rincon-hill.glb",
  "anchor": [
    -122.392182,
    37.7857621
  ],
  "targetHeightM": 195,
  "cat": 2,
  "name": "One Rincon Hill",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: 'oneRinconHill'`, `exclude: ~60`) and re-bake.
- Manifest id `one-rincon-hill` maps to `oneRinconHill`.
- The site is on a real hill; the loader samples terrain at the anchor, so verify the podium sits correctly rather than cutting into the slope.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 18,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the crown truss and beacon
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Two towers or one? Decide early — it changes the footprint, the anchor and the manifest height. The plan defaults to the South Tower only.
- Floor counts in sources range from 55 to 62; that does not affect the model but should be reported honestly.
- The crown is often modelled as a solid hat. It must read as an open frame or the identity is lost.
