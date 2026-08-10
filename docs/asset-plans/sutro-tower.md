# Sutro Tower — SF-SIM asset plan

The hardest technical subject: a lattice tower that must read as delicate from a city camera without exploding the triangle budget or turning into a solid slab. Plan for a faked lattice.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/sutro-tower/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `sutro-tower` |
| Existing procedural builder | `sutroTower()` in `app/src/landmarks.js` (key `6`, exclusion 160 m) |
| WGS84 anchor | `-122.4528562, 37.7552411` |
| Target height | **297.8 m** (977 ft) above its base; 552 m above sea level |
| OSM footprint | leg spread ~59 x 52 m (OSM relation/3829019) |
| Triangle cap | 27,000 |
| Category | `0` (Miscellaneous / infrastructure) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Sutro Tower GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Sutro Tower in San Francisco and deliver it
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
8. `docs/asset-plans/sutro-tower.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Three-legged triangular steel lattice structure
- Extremely thin/tall proportions
- Red-and-white painted sections
- Multiple horizontal antenna platforms
- Dense antenna arrays
- Three legs dramatically spreading outward toward the ground

## Research Sutro Tower independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- Platform heights and how many crossarm levels there are
- The FAA red/white banding sequence up the tower
- Leg batter angle and the ground-anchor blocks

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/sutro-tower/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Sutro Tower, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the tower: three battered legs, the lattice core, all crossarm platforms, antenna masts and the small base anchor blocks.

Do not include unrelated surrounding city geometry: the hillside itself (terrain data supplies it), the transmitter building, access roads, guy fences, trees, people, vehicles, plinths, cameras or lights. Temporary
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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The tower is three-fold symmetric. Orient the leg triangle to match the mapped footprint (one leg pointing roughly north-east), and note the `-Y` convention in `REPORT.md`.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/sutro-tower/build_sutro_tower.py` (deterministic build script),
`artifacts/sutro-tower/sutro-tower.blend`, and `artifacts/sutro-tower/sutro-tower.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`sutro-tower-top.png`, `sutro-tower-north.png`, `sutro-tower-east.png`, `sutro-tower-south.png`,
`sutro-tower-west.png`, plus `sutro-tower-contact-sheet.png` and at least one high
three-quarter aerial beauty render `sutro-tower-aerial.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the crossarm platforms and the antenna cluster silhouette; the aerial
view uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `sutro-tower.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/sutro-tower/validation.json` and
`artifacts/sutro-tower/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "sutro-tower",
  "file": "sutro-tower.glb",
  "anchor": [
    -122.4528562,
    37.7552411
  ],
  "targetHeightM": 297.8,
  "cat": 0,
  "name": "Sutro Tower",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — see the integration notes in `docs/asset-plans/sutro-tower.md`.
````

---

## Part 2 — Research and design dossier

Compiled 10 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Height | 297.8 m / 977 ft above ground | Wikipedia infobox (FCC filing), Wikidata |
| Elevation | 552 m above sea level | Wikipedia |
| Completed | 1973 | Wikidata, OSM `start_date` |
| Structure | Three-legged steel lattice with two large crossarm platform levels | Wikipedia; *verify* platform count |
| Leg spread | ~59 x 52 m mapped | OSM relation/3829019 (measured) |
| Material | Steel | Wikidata P186 |
| Livery | FAA red/white alternating bands | *inferred* from photography — verify band count |

### 2.2 Sources

- https://www.openstreetmap.org/relation/3829019 — leg positions, 298 m height, communications tower tags
- https://en.wikipedia.org/wiki/Sutro_Tower — 297.8 m, 1973, three-legged description, elevation
- https://www.wikidata.org/wiki/Q650097 — height in feet, steel, inception
- https://www.sutrotower.com — operator material, structure and antenna information
- https://commons.wikimedia.org/wiki/Category:Sutro_Tower — elevations from all sides, close-ups of platforms, fog shots

### 2.3 Orientation and placement

Three legs on a roughly equilateral plan; the mapped bounding box is 59 x 52 m. Match the mapped leg bearings so the tower's profile from downtown matches reality, and let the app's terrain sampling put it on the ridge — the GLB base stays at z=0.

### 2.4 What each side shows

**From the east (city)** — The classic view: two legs framing the third, crossarms reading as two wide horizontal bars against the sky.

**From the north / south** — The tower appears narrower; the crossarms overlap and the antenna mast dominates.

**From the west** — Similar to the east view, mirrored; the leg triangle reads as a wide A.

**Top** — The mast and the upper crossarm platform seen end-on: a small dense cluster of vertical antenna elements on a triangular platform.

### 2.5 Recognition cues (ranked)

1. The three splayed legs — the shape no other structure has
2. Two wide horizontal crossarm platforms
3. Red-and-white banding
4. Extreme slenderness above the legs

### 2.6 Miniature translation

**Preserve**

- 297.8 m height and the ~55 m leg spread
- Three legs, splayed, with visible batter
- Two (verify) crossarm levels at their real heights
- The see-through quality of the silhouette

**Simplify / exaggerate**

- The real lattice becomes a small number of chunky members: three leg chords plus regular X-braces, sized up so they survive at city scale
- Antenna arrays become 6-10 simple cylinders and boxes per platform
- Ladders, cables, guys and mounts disappear
- Bands become flat colour changes on the members, no decals

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Legs: three tapered box-section chords from a 55 m-diameter triangle at z=0 converging to an ~11 m triangle at z=150. Section 2.2 m at the base to 1.2 m at the top; `Toy_steel` base with red/white banded segments.
2. Bracing: X-braces between each leg pair every 15 m, member section 0.8 m. Use a repeating module and array it — this is where the budget goes.
3. Core mast: triangular prism 11 m across, z=150 to z=250, same brace module at 12 m spacing.
4. Lower crossarm: platform at z~180, 46 m wide, 4 m deep, `Toy_steel`, with a `Toy_roofd` deck.
5. Upper crossarm: platform at z~215, 38 m wide, 4 m deep.
6. Antenna cluster: z=250 to z=297.8, 8-10 cylinders radius 0.4-0.9 m plus two boxy arrays; `Toy_white` and `Toy_red`.
7. Aviation beacons: `Toy_red_Glow` beads at each crossarm tip and the mast top.
8. Anchor blocks: three 6 x 6 x 2 m `Toy_stone` pads at the leg feet.
9. Bevel 0.08 m, 1-2 segments — bevel cost is multiplied by the brace count, so keep it minimal.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_steel` | `#9aa0a6` | unbanded structural members, platforms |
| `Toy_red` | `#c4453c` | FAA red bands and antenna sections |
| `Toy_white` | `#f7f4ec` | FAA white bands |
| `Toy_roofd` | `#45454a` | platform decks |
| `Toy_stone` | `#d9d2c2` | ground anchor pads |
| `Toy_red_Glow` | `#c4453c` | aviation beacons |

Night glow: aviation beacons only: crossarm tips and the mast top. Nothing else on this structure glows.

### 2.9 Top surface

There is no roof, but the crossarm decks and the antenna cluster are what the downward camera sees. Give the decks a visible surface pattern (railing rhythm and a couple of equipment boxes) rather than a bare plane.

### 2.10 Scope

**In the GLB:** the tower: three battered legs, the lattice core, all crossarm platforms, antenna masts and the small base anchor blocks

**Not in the GLB:** the hillside itself (terrain data supplies it), the transmitter building, access roads, guy fences, trees, people, vehicles, plinths, cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: legs ~8k, braces ~10k, crossarms ~4k, antennas ~3k, anchors ~1k, spare ~1k

### 2.12 Draft manifest entry

```json
{
  "id": "sutro-tower",
  "file": "sutro-tower.glb",
  "anchor": [
    -122.4528562,
    37.7552411
  ],
  "targetHeightM": 297.8,
  "cat": 0,
  "name": "Sutro Tower",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- `sutroTower` exists procedurally and in the registry (exclusion 160 m, key `6`); manifest id `sutro-tower` maps to it.
- `targetHeightM: 298` matches the existing tiles entry — keep them consistent.
- Because the tower straddles a ridge, verify all three legs land plausibly on sampled terrain; the loader places one point, so the model may need slightly longer legs than reality to avoid a floating foot.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the aviation beacons
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- Highest triangle risk in the set. Build ONE brace module and array it; do not model the real lattice.
- Members thin enough to be accurate will vanish or alias at city scale. Deliberately oversize them (style bible §9 semantic scale) and say so in `REPORT.md`.
- Platform heights are not well published; state which photograph you measured them from.
