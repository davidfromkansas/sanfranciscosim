# Chase Center — SF-SIM asset plan

A 155 m rounded drum standing alone on the flat reclaimed ground of Mission Bay, wrapped in a pale aluminium "sail" skin whose parapet swoops up over the glazed west entry. The largest-diameter single volume in the landmark set, and the only one whose silhouette is a disc.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/chase-center/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `chase-center` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.387433, 37.767883` |
| Target height | **40.8 m** (134 ft, facade/sail crest); roof deck ~31.8 m, OSM `height`=38.1 m |
| OSM footprint | 155.1 x 153.5 m oriented box, long axis 169.9 deg from east (OSM way/579646390, 19,465 m2) |
| Triangle cap | 27,000 |
| Category | `0` (Miscellaneous / attraction — matches Oracle Park) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Chase Center GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Chase Center in San Francisco and deliver it
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
8. `docs/asset-plans/chase-center.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A big low rounded drum sitting alone on flat ground — the silhouette is the asset
- Pale aluminium "sail" skin: vertical panel rhythm under a parapet that rises and falls
- The parapet peak over the glazed west entry atrium facing the Thrive City plaza
- Ground-level glazed retail band that makes the drum appear to float on its base
- A designed roof: pale membrane, central mechanical cluster, perimeter catwalk
- Warriors identity as restrained saturated accent (navy + gold) at the entry, and
  the oversized west video board as the night-glow hero

## Research Chase Center independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- The three published height figures and what each measures (2.1) — decide which is
  the architectural crest and record eave vs crest explicitly
- The west entry atrium, its curtainwall extent, the video board and the canopy
- Whether the parapet's high point is over the west entry or the north-west corner

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/chase-center/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Chase Center, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

This is a wide, low building. The silhouette from the app's aerial camera is a disc,
so the roof and the parapet profile carry almost all of the recognition load —
budget accordingly (§10, "roofs are secondary facades").

## Scope of the exported asset

Export the arena volume only: base drum, main drum, sail parapet, west entry atrium
with its canopy and video board, and the roof with its mechanical cluster.

Do not include unrelated surrounding city geometry: the Thrive City plaza and its
paving, the Seeing Spheres sculpture, Uber Headquarters buildings 2/3/4, the Chase
Center Garage, Bayfront Park, Third Street, 16th Street, Warriors Way, Terry A.
Francois Boulevard, the Muni T line, trees, people, vehicles, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 27,000 triangles.

**Normalize the bbox top to 40.8 m exactly** so the loader's
`targetHeightM / measuredHeight` scale lands at 1.0.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main entrance
faces **west** onto the Thrive City plaza and Third Street. The plan's long axis runs
169.9 deg from east, i.e. essentially square to the compass — do not rotate the drum
to "look better". Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
assume no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/chase-center/build_chase_center.py` (deterministic build script),
`artifacts/chase-center/chase-center.blend`, and `artifacts/chase-center/chase-center.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify
or rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`chase-center-top.png`, `chase-center-north.png`, `chase-center-east.png`,
`chase-center-south.png`, `chase-center-west.png`, plus
`chase-center-contact-sheet.png`, at least one high three-quarter aerial beauty
render `chase-center-aerial.png`, and a night render `chase-center-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the roof membrane, the
mechanical cluster, the perimeter catwalk and the swooping parapet profile; the
aerial view uses the style bible's camera assumptions (30-50 degrees down, long
lens). Simple tabletop lighting, neutral warm background, minimal depth of field,
and every image must depict the same exported model. The night render must show the
video board and atrium glow; put a night tile on the contact sheet.

## Validate the exported GLB

Re-import `chase-center.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals: per-object signed volume is
authoritative for a union of solids; a ray test may show <= 0.15% residual.
Render at least one review image from the re-imported asset. Write
`artifacts/chase-center/validation.json` and `artifacts/chase-center/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "chase-center",
  "file": "chase-center.glb",
  "anchor": [
    -122.387433,
    37.767883
  ],
  "targetHeightM": 40.8,
  "cat": 0,
  "name": "Chase Center",
  "estimated": false,
  "loadRadius": 2500,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes
in `docs/asset-plans/chase-center.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Opened | 6 September 2019 (groundbreaking 17 Jan 2017) | Wikipedia |
| Design architect | MANICA Architecture (with Kendall Heaton; interiors Gensler) | Wikipedia, Enclos |
| Structural engineer | Magnusson Klemencic Associates | Wikipedia |
| Capacity | 18,064 basketball / 19,500 concert | Wikipedia, OSM `capacity` |
| Cost | $1.4 bn | Wikipedia |
| Plan dimensions | 154.397 x 156.781 m | Dlubal structural-model reference |
| Measured footprint | 155.1 x 153.5 m oriented box, 19,465 m2 polygon area | OSM way/579646390 (measured, this doc) |
| Facade / crest height | 134 ft = **40.84 m** | Enclos project page |
| Structural model height | 31.755 m | Dlubal (top of primary roof steel) |
| OSM `height` tag | 38.1 m | OSM way/579646390 — a mid figure, not the crest |
| Facade area | 14,864 m2 rain-screen + 3,716 m2 curtainwall + 465 m2 storefront | Enclos, Dlubal |
| Facade panels | ~1,165 unique aluminium mega-panels, ~7,500 individual metal panels, 14 panel categories | Enclos, Archpaper |
| Roof | Sarnafil single-ply membrane (light-coloured) over complex steel trusses | Hydrotech, DBM Vircon |
| Address | 1 Warriors Way, Mission Bay, SF 94158 | OSM `addr:*` |
| Wikidata | Q15262098 | OSM `wikidata` tag |

**Height decision.** Three published figures measure three different things. The
structural 31.755 m is the top of the primary roof steel (the roof deck); the
aluminium sail parapet continues above it to the 134 ft / 40.84 m facade crest;
OSM's 38.1 m sits between them and is the usual permit-envelope figure. Target
**40.8 m = crest**, roof deck **~31.8 m = eave**. AGENTS rule 5 and the pipeline's
"architectural top" rule both point at the crest.

### 2.2 Sources

- https://www.openstreetmap.org/way/579646390 — footprint, address, capacity, `height`, Wikidata link
- https://en.wikipedia.org/wiki/Chase_Center — opening, architects, capacity, cost, site programme
- https://enclos.com/project/chase-center-arena/ — 134 ft height, 160,000 sq ft facade, 1,165 mega-panels, "stacked drums", AESS curtainwall
- https://www.dlubal.com/en/downloads-and-information/references/customer-projects/001159 — 31.755 m structural height, 154.397 x 156.781 m plan
- https://www.archpaper.com/2020/05/facades-manicas-chase-center-references-san-franciscos-mission-bay-aluminum-panels/ — sail-like aluminium facade concept, 5,000 unique panels, 14 categories
- https://www.hydrotechusa.com/projects/chase-center-golden-state-warriors-stadium — Sarnafil roof system, garden roofs on the adjacent office blocks
- https://www.swagroup.com/projects/chase-center-entertainment-district/ — plaza and landscape context (explicitly out of GLB scope)

### 2.3 Orientation and placement

The plan is a rounded square, essentially aligned to the compass — the minimum-area
oriented box comes out 169.9 deg from east, i.e. ~10 deg off axis, which at this
size and with corner radii this generous is visually square. Author it square to
the world; do not rotate.

Site bearings measured from the footprint centroid (this doc, via OSM):

| Feature | Bearing | Distance |
|---|---|---|
| West Entrance (main) | W | 76 m |
| Box Office | NW | 72 m |
| Warriors Shop | NW | 86 m |
| Third Street / Muni T "UCSF/Chase Center" stop | W | 145–160 m |
| Warriors Way | N | 118 m |
| Chase Center Garage | N | 106 m |
| Terry A. Francois Boulevard | E | 107 m |
| Bayfront Park | E | 162 m |
| Seeing Spheres sculpture | SE | 106 m |
| Uber HQ Building 3 | NW | 112 m |
| Uber HQ Building 4 | SW | 109 m |

The hero elevation is therefore **west**, onto the Thrive City plaza and Third
Street. This conflicts with the contract's nominal "front faces -Y" rule; per the
README's orientation note, real-world orientation wins and the deviation is recorded
in `REPORT.md`.

### 2.4 What each side shows

**West (Thrive City / Third Street front)** — The hero elevation. A tall glazed
atrium cut into the drum, the entry canopy beneath it, the oversized outdoor video
board beside it, and the parapet reaching its high point directly above. This is the
side almost every photograph of the building is taken from.

**North (Warriors Way / 16th Street)** — Continuous sail skin over the glazed
ground-level retail band; secondary entrances; the parapet falls away from the
west peak.

**East (Terry A. Francois / Bayfront Park)** — The bay-facing back. Uninterrupted
panel rhythm, lowest parapet, loading and back-of-house at grade — read as plain
skin at miniature scale.

**South** — Similar to the north; a secondary glazed entry toward the south plaza.

**Top** — A large pale membrane roof, near-circular in read, with a central cluster
of mechanical penthouses, smaller units ringed around it, a perimeter catwalk just
inside the parapet, and the parapet itself visible as a swooping ring whose inner
face is the same aluminium as the walls. *Roof layout beyond "central mechanical
cluster on a light membrane" is inferred from aerial imagery, not from a drawing.*

### 2.5 Recognition cues (ranked)

1. A big low rounded drum standing alone on flat ground — a disc among boxes
2. The swooping parapet: a ring that rises to a peak over the west entry
3. Pale aluminium skin with a fine vertical panel rhythm
4. The glazed west atrium with its canopy and oversized video board
5. The floating read: a dark glazed retail band at grade under the pale drum

### 2.6 Miniature translation

**Preserve**

- The disc silhouette and its 155 m diameter — this is the whole asset
- The parapet's rise and fall, and that its peak is over the west entry
- The pale, near-white aluminium value against dark glazing
- The drum's isolation: nothing else in the GLB

**Simplify / exaggerate**

- ~7,500 real metal panels become ~48 vertical bands of shallow recess
- The 14 panel categories collapse to one flat `Toy_trim` aluminium
- The continuous compound-curved parapet becomes a lofted ring with a smooth
  sine-modulated top edge, single peak west
- The curtainwall atrium becomes one chunky glazed wedge with 5 steel fins
- The video board becomes one oversized flat panel — the night-glow hero
- Roof plant becomes one central block plus six ringed units

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Base drum: rounded-square plan 155.0 x 153.5 m, corner radius 34 m, 40-segment
   outline, z=0 to z=12, `Toy_stone`.
2. Retail band: same outline inset 1.2 m, z=1.5 to z=8, `Toy_glass` — the drum reads
   as floating on a plinth.
3. Main drum: outline inset 2.0 m from the base, z=12 to z=31.8 (roof deck),
   `Toy_trim`, with 48 vertical bands recessed 0.35 m x 1.6 m wide for the panel
   rhythm.
4. Sail parapet: lofted ring on the main-drum outline, z=31.8 to a top edge varying
   34.0–40.8 m, single maximum on the west face at the entry axis, minimum on the
   east. `Toy_trim` outside, `Toy_sand` inside face.
5. West entry atrium: glazed wedge projecting 14 m from the west face, 46 m wide,
   z=0 to z=26, `Toy_glass` with 5 `Toy_steel` fins; `Toy_navy` canopy slab 3 m deep
   at z=7.
6. Video board: 22 x 12 m flat panel on the west face north of the atrium, centre
   z=18, `Toy_sky_Glow`, framed 0.6 m in `Toy_roofd`.
7. Identity: a `Toy_gold` 0.8 m band along the parapet crest for the 60 m centred on
   the west peak — the one saturated accent, Warriors gold.
8. Roof: `Toy_stone` membrane at z=31.8; central mechanical block 34 x 18 x 4.5 m
   `Toy_steel`; six 8 x 6 x 3 m units on a 46 m radius ring; `Toy_roofd` perimeter
   catwalk 2.5 m wide, 0.4 m proud, 4 m inside the parapet.
9. Bevel 0.12 m, 2 segments, on everything.
10. Normalize the bbox top to exactly 40.8 m before export.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_trim` | `#f3efe6` | aluminium sail skin, main drum, parapet outer face |
| `Toy_sand` | `#ece4d4` | parapet inner face |
| `Toy_stone` | `#d9d2c2` | base drum, roof membrane |
| `Toy_glass` | `#2a4d73` | ground retail band, west atrium glazing |
| `Toy_steel` | `#9aa0a6` | atrium fins, roof mechanical |
| `Toy_roofd` | `#45454a` | perimeter catwalk, video-board frame |
| `Toy_navy` | `#2c4a70` | entry canopy — Warriors blue |
| `Toy_gold` | `#caa64a` | parapet crest band over the entry — Warriors gold |
| `Toy_sky_Glow` | `#6db3d9` | the west video board (night-glow hero) |
| `Toy_white_Glow` | `#f7f4ec` | atrium glazing spill + parapet cove, west quadrant only |

Night: the video board is the hero; the atrium and a west-quadrant parapet cove are
the supporting accents. Two glow materials, three surfaces — an arena reads as lit,
but the drum must not become a lantern. Both glow day-colours (`6db3d9`, `f7f4ec`)
are palette members, so the daytime read stays in family.

### 2.9 Top surface

A 19,000 m2 flat roof at 32 m in a district of low buildings is the single most
exposed surface in this asset — the app camera sees the roof and the parapet ring
and very little else. Design it properly: pale membrane, one central mechanical
block, six ringed units for graphical repetition, a perimeter catwalk that draws the
disc's edge, and the parapet's swoop visible as the outline. Do not leave it blank
and do not scatter props.

### 2.10 Scope

**In the GLB:** the arena — base drum, retail band, main drum, sail parapet, west
entry atrium with canopy and video board, roof with mechanical cluster and catwalk

**Not in the GLB:** Thrive City plaza and paving, Seeing Spheres, Uber HQ Buildings
2/3/4, Chase Center Garage, Bayfront Park, Third Street, 16th Street, Warriors Way,
Terry A. Francois Boulevard, the Muni T line, trees, people, vehicles, plinths,
cameras or lights

### 2.11 Triangle budget

Cap 27,000. Suggested split: main drum and vertical band rhythm ~10k, sail parapet
~5k, base drum and retail band ~4k, roof and mechanical ~4k, atrium/canopy/board
~2k. Leaves ~2k of headroom; the 40-segment outline is the main lever if it runs
over.

### 2.12 Draft manifest entry

```json
{
  "id": "chase-center",
  "file": "chase-center.glb",
  "anchor": [
    -122.387433,
    37.767883
  ],
  "targetHeightM": 40.8,
  "cat": 0,
  "name": "Chase Center",
  "estimated": false,
  "loadRadius": 2500,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` follows the default rule `max(2500, 40.8 x 30) = 2500`.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** No `chase-center` id exists in `pipeline/lib/landmarks.mjs`
  or `app/src/landmarks.js`, so integration needs a registry entry and a re-bake of
  the affected tiles, or the baked procedural building will intersect the GLB.
- Suggested registry entry: `id: 'chase-center'`, lon/lat as above, height 40.8,
  `exclude: ~115` m — the footprint's half-diagonal is ~109 m, so 115 clears the
  drum without eating the Uber HQ blocks 109–112 m away. Check that boundary during
  integration; it is the tightest exclusion/neighbour margin in the set.
- `loadRadius: 2500` (default rule). Beyond it the site falls back to the baked
  city — but the exclusion zone means the site is *empty*, not wrong, past the
  radius. At 2500 m in flat Mission Bay that absence may be legible from the
  Bay Bridge approach; verify during integration and raise the radius if so.
- Mission Bay is flat fill at ~2–3 m elevation; confirm terrain seating carefully,
  since a 155 m footprint spans several elevation samples.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox top exactly 40.8 m so the loader scale lands at 1.0
- [ ] Dimensions plausible in meters and consistent with 2.1
- [ ] Triangles at or under 27,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the video board, atrium glazing and west parapet cove
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume authoritative; ray test <= 0.15% residual)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **Which height is architectural?** Three sources give 31.755 m, 38.1 m and 40.84 m.
  This plan reads them as roof deck / permit envelope / facade crest and targets the
  crest. If the executing agent finds a drawing that contradicts that reading, the
  drawing wins and the manifest `targetHeightM` changes.
- **Parapet peak location** is *inferred* from photography (it reads as being over
  the west entry). No published elevation drawing was found. If research shows the
  high point is at the north-west corner instead, move it — the swoop is cue #2 and
  getting its phase wrong is worse than getting its amplitude wrong.
- **Roof layout** beyond "light membrane, central mechanical cluster" is *inferred*
  from aerial imagery. It is also the most-seen surface, so it deserves a second
  look before the build.
- **Exclusion radius vs the Uber blocks.** 115 m exclusion against neighbours at
  109–112 m is the tightest margin in the landmark set; a too-generous radius will
  delete real buildings from the baked city.
- A 155 m disc is by far the widest asset in the set. Nothing in the loader cares,
  but it spans multiple 500 m tile cells and several terrain samples — flagged for
  integration, not for authoring.
