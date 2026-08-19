# The Towers at Rincon — SF-SIM asset plan

The residential half of Rincon Center: a six-storey curvilinear office podium filling a whole
Transbay block, with twin 22-storey apartment towers rising diagonally out of it, each capped by
rolled bullnose cornices, an arched penthouse and a slender mast. Postmodern, 1989, Scott Johnson
of Pereira Associates. The historic 1940 Rincon Annex post office on the north-west half of the
same block is **out of scope** — it is a separate footprint and a separate asset.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/towers-at-rincon/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `towers-at-rincon` (registry id `towersAtRincon`) |
| Existing procedural builder | none — **Case B**, new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3924873, 37.7919896` (AABB centre of the DataSF footprint) |
| Target height | **89.0 m** to the mast tip (CTBUH architectural = to tip); LiDAR crest 87.2 m; podium roof 24.5 m |
| DataSF footprint | 5,008 m², AABB 112.3 × 112.6 m, oriented box 89.2 × 76.0 m at −44.7° (`sf16_bldgid 201006.0000265`) |
| Triangle cap | 18,000 |
| Category | `2` (Apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready "The Towers at Rincon" GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of The Towers at Rincon (88 Howard Street, San Francisco)
and deliver it as a downloadable, validated GLB.

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
8. `docs/asset-plans/towers-at-rincon.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **six-storey curvilinear podium filling the whole block** — continuous horizontal
  precast/glazing bands, a serpentine plan with big convex bows on the Steuart and
  Howard frontages, and a colonnade of square piers along the sidewalk under a dark base band
- **Twin apartment towers rising diagonally out of the podium**, one over the south-west
  quadrant, one over the east quadrant; each an elongated ~50 × 26 m lozenge with a
  bowed outer long face and rounded ends
- **Stacked white balcony slabs** sweeping along each tower's convex face — the strongest
  facade rhythm on the building
- **The crown**: heavy rolled (bullnose) cornices capping the rounded tower ends, a taller
  central bay above with its own rolled cornice, an **arched (barrel-vaulted) penthouse**
  with a band of small square windows, and a slim mast on the apex
- The Howard/Steuart corner **entrance**: a glass pyramid canopy and, above it, a large
  semicircular arched window in the precast wall
- The podium roof **courtyard terrace** in the north-west quadrant: a circular paved plaza,
  curved planting beds and low curved pergola structures

## Research The Towers at Rincon independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North-west (Annex party wall), north-east (Steuart St), south-east (Howard St) and
  south-west (Spear St) elevations
- Aerial and roof/top views — the two tower roofs, their mechanical penthouses, and the
  podium terrace
- Ground-level views of the arcade, the entrance canopy and the arched window
- Day and night appearance
- The tower crown in detail: cornice profiles, the arched penthouse, the mast
- Whether the two towers are identical (they read as mirrored twins) and how each is oriented

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/towers-at-rincon/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as The Towers at Rincon, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the 88 Howard block only: the six-storey podium on its real footprint, the two
residential towers with their crowns, the entrance canopy and arched window, and the podium
roof terrace.

Do not include the historic Rincon Annex post office on the north-west half of the block
(it is a separate DataSF footprint and will be its own asset), nor Howard, Spear or Steuart
Street, the Embarcadero, neighbouring buildings, trees, people, vehicles, plinths, cameras
or lights. Temporary context may appear in review renders but must not leak into the GLB.

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
(`placeGeneric` in `app/src/assets.js` only scales and positions). The block is a diamond
whose corners point roughly north, east, south and west; the **Howard Street frontage
(main address, entrance) is the SOUTH-EAST face**, Steuart Street is the NORTH-EAST face,
Spear Street is the SOUTH-WEST face, and the NORTH-WEST face is the party line with the
Rincon Annex. Author true-world orientation and document the heading.
Record the decision and the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/towers-at-rincon/build_towers_at_rincon.py` (deterministic build script),
`artifacts/towers-at-rincon/towers-at-rincon.blend`, and
`artifacts/towers-at-rincon/towers-at-rincon.glb`. The script
must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`towers-at-rincon-top.png`, `towers-at-rincon-north.png`, `towers-at-rincon-east.png`,
`towers-at-rincon-south.png`, `towers-at-rincon-west.png`, plus
`towers-at-rincon-contact-sheet.png` and at least one high three-quarter aerial beauty
render `towers-at-rincon-aerial.png`, plus a night render `towers-at-rincon-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the two tower roofs with their
mechanical penthouses and arched caps, and the podium courtyard terrace; the aerial
view uses the style bible's camera assumptions (30–50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `towers-at-rincon.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/towers-at-rincon/validation.json` and
`artifacts/towers-at-rincon/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "towers-at-rincon",
  "file": "towers-at-rincon.glb",
  "anchor": [
    -122.3924873,
    37.7919896
  ],
  "targetHeightM": 89.0,
  "cat": 2,
  "name": "The Towers at Rincon (88 Howard Street)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2670
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any
app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/towers-at-rincon.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026. Values marked *inferred* or *estimated* are visual or derived
estimates, not published figures — the executing agent must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Complex | Rincon Center, phase two ("Two Rincon Center") | Wikipedia, LA Times 1988 |
| Address | 88 Howard Street, San Francisco CA 94105 | OSM node 2038804804, CTBUH, owner sites |
| Completed | 1988 (podium/offices) / 1989 (residences) | Wikipedia; CTBUH 1989 |
| Architect | Scott Johnson, Pereira Associates (Johnson Fain) | Wikipedia, rinconcenter.wordpress.com |
| Towers | Two — CTBUH "Rincon Center East Tower" (#32367) and "West Tower" (#32366) | CTBUH |
| Architectural height | **89 m / 292 ft** each; "to tip" also 89 m | CTBUH, both towers |
| Floors | CTBUH 22 above ground + 2 below; Wikipedia "twin 23-storey" | CTBUH / Wikipedia (disagree by one; see 2.15) |
| Apartments | 160 per tower, 320 total | CTBUH; RentCafe; Tidewater Capital |
| Podium | six storeys of office + ground-floor retail under the towers | Wikipedia, Tidewater Capital |
| LiDAR crest | **87.13 m** above ground (`hgt_maxcm 8713`), peak elevation 90.63 m NAVD88 | DataSF `sf16_bldgid 201006.0000265` (measured) |
| LiDAR podium level | 24.95 m median / 24.21 m mode | same record (measured) |
| Ground elevation | 3.36 m (min) – 4.67 m (max) NAVD88 | same record (measured) |
| DataSF footprint | 5,008 m²; AABB 112.29 × 112.60 m; oriented box 89.24 × 76.04 m at −44.68° | measured from `buildings_datasf.geojson` |
| OSM outline | way/32862406 "The Towers at Rincon", `height=93`, `building:levels=24`, 4,631 m² | OSM (heights differ from CTBUH; see 2.15) |
| OSM 3D parts | tower parts way/944891683 (868 m²) and way/944891684 (803 m²), both `height=93` | OSM `building:part` |

**The bimodal LiDAR test** (method: [[sf3d-lidar-max-vs-median]] / `docs/asset-plans/README.md`).
The record is strongly bimodal — mean 38.29 m, median 24.95 m, mode 24.21 m, σ 25.93 m, max 87.13 m.
Solving `f·H + (1−f)·L = mean` and `f(1−f)(H−L)² = σ²` with `H = 87.0` gives **L = 24.49 m**
(podium) and **f = 0.221** (tall fraction). Two independent numbers — a six-storey podium at
24.5 m and a tower crest at 87 m — fall straight out of the raw statistics, and both agree with
the published figures. Tower plan area implied: 0.221 × 5,008 ≈ 1,105 m², against 1,671 m² for
the two OSM parts; the difference is the crude two-level model (there are intermediate roof
levels), so treat `f` as corroboration of *H* and *L*, not as a plan-area measurement.

**Height decision.** `targetHeightM = 89.0 m` — CTBUH architectural and "to tip". The LiDAR
crest of 87.2 m is the solid arched penthouse roof (LiDAR does not return a thin mast); the
remaining 1.8 m is the mast. Model the **arch apex at 87.2 m and the mast tip at 89.0 m**, so
the GLB bbox top is exactly 89.0 and the loader's `targetHeightM / measuredHeight` lands at 1.0.
OSM's `height=93` is *not* the architectural top and must not be used.

### 2.2 Sources

- https://www.openstreetmap.org/way/32862406 — outline, name, levels; `building:part` ways
  944891683/944891684 (towers), 944891685/944891687/944891688 (podium), 1301393950/1301393951
  (terrace pergolas)
- https://www.skyscrapercenter.com/building/rincon-center-east-tower/32367 and
  https://www.skyscrapercenter.com/building/rincon-center-west-tower/32366 — 89 m / 292 ft,
  22 floors, 1989, 160 apartments each, address 88 Howard
- https://en.wikipedia.org/wiki/Rincon_Center — Scott Johnson / Pereira Associates, twin
  23-storey towers, 320 apartments, six-storey commercial base, Rincon Annex history, the
  (removed) Rain Column and the five-storey atrium
- https://www.latimes.com/archives/la-xpm-1988-10-16-re-6436-story.html — "Two Rincon Center
  will incorporate a six-story office building as the base for twin **curvilinear** … apartment
  towers", ground-floor promenade and central garden courtyard
- https://www.tidewatercap.com/listings/88-howard-san-francisco — 320 units, two residential
  towers atop six floors of office and ground-floor retail, "23-story"
- https://www.carmelpartners.com/project/the-towers-at-rincon/ — "due to the unique shape of the
  project"; units "encircling a beautiful courtyard"; 23rd-floor decks, 7th-floor resident lounge
  (i.e. the podium roof terrace) — *observed (owner marketing)*
- https://commons.wikimedia.org/wiki/File:Rincon_Towers.jpg — the definitive crown photograph
  (7628 × 10171, monochrome): rolled bullnose cornices, the taller central bay, the arched
  penthouse with its band of small square windows, the mast
- DataSF Building Footprints (`ynuv-fyni`), record `201006.0000265` — footprint geometry and the
  full LiDAR height statistics quoted in 2.1
- Google satellite z20/z21 tiles over 37.79195, −122.39246 — roof plan of both towers, their
  mechanical penthouses, and the podium courtyard terrace. Measured tower-roof centroids sit
  ≈ 9.5 m north-north-west of the OSM ground plans, consistent with ~6° off-nadir lean over an
  87 m building; the **OSM part positions are therefore the correct ground plans** and the
  imagery displacement is lean, not disagreement.
- Two public 360° photospheres near Howard/Steuart (Google Maps user photospheres, Dec 2022 and
  a rooftop sphere at 37.79131, −122.39289) — *observed (user photography)*: the sunlit precast
  colour, the arcade, the entrance canopy, the arched window, and the balcony rhythm.

Exa queries run (`web_search_advanced_exa`): "The Towers at Rincon 88 Howard Street San Francisco
apartments building height architect" (8 results; skyscrapercenter, structurae, rentcafe,
carmelpartners, costar, wikipedia yielded the facts above) and "Rincon Center San Francisco
residential towers 88 Howard facade exterior photo postmodern Scott Johnson" (10 results;
skydb.net, LA Times 1988, thetowersatrincon.com, rinconcenter.wordpress.com yielded the
curvilinear/courtyard description and photo leads).

### 2.3 Orientation and placement

The block is a diamond in the SoMa/Transbay grid, its corners pointing roughly north, east,
south and west (streets run at 45°/135°). Measured from DataSF street centrelines against the
footprint:

| Face | Street | Note |
|---|---|---|
| South-east | **Howard Street** | address frontage; main residential entrance at the Howard/Steuart end |
| North-east | **Steuart Street** | the water side; the east tower bows out over this frontage |
| South-west | **Spear Street** | the west tower bows out over this frontage |
| North-west | *no street* — party line with the Rincon Annex | the Annex (DataSF `201006.0000121`, 29.7 m) abuts here |

Anchor `-122.3924873, 37.7919896` is the AABB centre of the DataSF footprint, which is where the
contract's base-centre origin lands. Author +Y = true north.

**Footprint, in metres relative to the anchor (Blender X = east, Y = north).** The DataSF ring
has 98 vertices; the corners and the governing edges are:

- east corner `(56.1, 1.8)`, north corner `(7.0, 56.3)`, west corner `(−56.1, −6.6)`,
  south corner `(−1.8, −56.3)`
- Howard (SE) face: south corner `(−1.8, −56.3)` to east corner `(56.1, 1.8)`
- Steuart (NE) face: east corner `(56.1, 1.8)` to north corner `(7.0, 56.3)`
- the north-west (Annex) face is stepped and jagged — a party line, not a designed elevation
- the podium's outer faces are **not straight**: the real building bows out in shallow convex
  arcs on the Steuart and Howard frontages and scallops back near the corners

**Tower ground plans** (OSM `building:part`, in the same anchor-relative metres):

- **West tower** (way/944891683, 868 m²): `(−32.4,−28.0) (−20.0,−15.7) (−13.7,−21.8) (−1.7,−21.5)
  (5.4,−15.6) (19.4,−28.8) (7.8,−39.9) (−4.7,−41.5) (−12.2,−41.4) (−21.5,−39.1)` — a lozenge
  ~51.8 m (E–W) × 26 m (N–S), convex on its **south** (Howard/Spear) side, concave on its north
  (courtyard) side.
- **East tower** (way/944891684, 803 m²): `(29.7,−18.5) (16.8,−6.7) (20.8,−2.6) (21.0,11.1)
  (16.0,17.0) (27.8,29.7) (38.6,18.6) (41.2,9.5) (41.9,0.6) (41.5,−7.2)` — a lozenge
  ~48 m (N–S) × 25 m (E–W), convex on its **east** (Steuart) side, concave on its west
  (courtyard) side.

The two lozenges are diagonally opposed with the courtyard terrace between them, in the block's
north-west quadrant against the Annex.

### 2.4 What each side shows

**South-east (Howard Street)** — The address elevation. A dark charcoal base band with a
colonnade of square piers over the sidewalk, then five bands of pale warm-grey precast alternating
with dark grey-green ribbon glazing, the wall bowing gently outward. At the Steuart end a glass
pyramid entrance canopy and, above it, a monumental semicircular arched window. The west tower
rises behind, its bowed balcony face turned this way.

**North-east (Steuart Street)** — Same podium language, more strongly bowed; the east tower stands
directly over this frontage, so this is the elevation where a tower reads full height from the
street. Balcony slabs stack the full height of the bow.

**South-west (Spear Street)** — Podium continues with the scalloped bow; the west tower's bowed
face and rounded west end read here.

**North-west (Annex party line)** — Stepped, plainer, largely blocked by the 29.7 m Annex. Keep
it simple, but not blank: continue the band rhythm.

**Top** — Two tower roofs, each with a long rectangular mechanical penthouse and the arched cap;
between them, in the north-west quadrant, the podium roof terrace: a circular paved plaza,
curved planting beds, low curved pergola structures (OSM ways 1301393950/1301393951, one storey,
3 m) and, at the 7th floor, the resident lounge. The remaining podium roof carries mechanical
plant and skylight rows. This is the surface the app camera sees most; design it fully.

### 2.5 Recognition cues (ranked)

1. **Two curvilinear towers on one podium**, diagonally opposed, with bowed faces stacked full of
   white balcony slabs
2. **The crown**: rolled bullnose cornices, taller central bay, arched penthouse, mast
3. **The six-storey podium filling a whole diamond block**, banded and bowed, with a street arcade
4. The **glass pyramid entrance canopy** and the big **arched window** at the Howard/Steuart corner
5. The **circular courtyard terrace** on the podium roof

### 2.6 Miniature translation

**Preserve**

- The podium-plus-twin-towers silhouette and the diagonal opposition of the two towers
- The bowed (curvilinear) plan — this building is unreadable as boxes
- The balcony rhythm on the bows
- The three-step crown: shoulder cornice → central bay cornice → arched cap → mast
- The whole-block footprint at its true size

**Simplify / exaggerate**

- ~20 storeys of curtain wall become 5 podium bands + 16 tower bands of alternating precast /
  dark glass; no individual mullions
- The 98-vertex DataSF ring becomes ~20 clean segments with true arcs on the two bowed frontages
- Dozens of balconies become one continuous, slightly oversized slab per floor across each bow
- Roof mechanical clutter becomes one long penthouse block plus two HVAC masses per tower
- The rolled cornices are **exaggerated** (a chunky half-round torus, ~1.2 m radius) — they are
  the signature and must read from the aerial camera
- The arched cap is exaggerated to a clean half-cylinder; the mast becomes a chunky tapered
  finial, not a hair-thin spike
- The entrance canopy becomes one clean glass pyramid; the arched window becomes one deep
  recessed arch

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a straitjacket —
adjust after the first aerial review render. All Z values are metres above the model base
(z = 0 sits on grade; the anchor's real ground is ~3.4 m NAVD88 and the loader seats the model
on terrain).

1. **Podium base band** z 0 → 4.5, the full footprint, `Toy_ink`; set back 1.2 m from the outer
   ring on the Howard, Steuart and Spear faces to leave a colonnade, with 8 square
   `Toy_stone` piers (1.1 × 1.1 m) standing on the ring line at ~9 m centres.
2. **Podium body** z 4.5 → 24.5, the full footprint in `Toy_sand`, banded: five 4.0 m storeys,
   each a 2.6 m precast spandrel (`Toy_sand`) plus a 1.4 m recessed glazing ribbon
   (`Toy_glass`, inset 0.3 m). Bow the Steuart and Howard faces outward by ~2.5 m at
   mid-span (12–14 segment arcs).
3. **Entrance** on the Howard/Steuart corner: a 9 m glass pyramid canopy (`Toy_glassl`) at
   z 0 → 6.5, and above it a semicircular arch 11 m wide recessed 0.6 m into the precast,
   z 8 → 21, filled with `Toy_glass`.
4. **Podium roof** z 24.5, `Toy_roofd`, with a 0.9 m `Toy_trim` parapet. In the north-west
   quadrant: a 16 m circular `Toy_stone` plaza, two curved 1.2 m-high planter walls
   (`Toy_stone`) with `Toy_mint` planting, and two low curved pergola bars (`Toy_trim`,
   3 m tall). Elsewhere: two HVAC masses and one skylight row.
5. **West tower** z 24.5 → 75.7: the lozenge plan above, bowed south face (14-segment arc),
   rounded ends (10 segments). Facade = 16 storeys of 3.20 m, each a 2.1 m `Toy_sand` spandrel
   plus a 1.1 m `Toy_glass` ribbon. On the bowed south face only, a 0.35 m-thick `Toy_trim`
   balcony slab projecting 1.5 m at every floor.
6. **East tower** z 24.5 → 75.7: identical language, lozenge rotated so its bow faces east.
7. **Shoulder cornices** at z 75.7: a half-round `Toy_trim` torus of radius 1.2 m following the
   full perimeter of each tower, projecting 1.0 m.
8. **Central bays** z 75.7 → 83.7 (2.5 storeys): a 20 × 26 m block centred on each tower's long
   axis, same banding, its own half-round `Toy_trim` cornice at 83.7 m.
9. **Arched penthouses** z 83.7 → 87.2: a 12 × 10 m half-cylinder cap (barrel axis along the
   tower's long axis, 12 segments) in `Toy_trim`, with a band of eight small square
   `Toy_glass_Glow` windows below the springing.
10. **Masts** z 87.2 → 89.0: a tapered `Toy_steel` finial, 0.45 m base radius, 8 segments, on
    each tower's arch apex. The **taller of the two must top out at exactly 89.00 m.**
11. Bevel 0.12 m, 2 segments, on everything except the arcs' tangent seams.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | podium and tower precast spandrels — the dominant surface |
| `Toy_stone` | `#d9d2c2` | arcade piers, terrace plaza and planter walls |
| `Toy_trim` | `#f3efe6` | balcony slabs, rolled cornices, arched caps, parapets, pergolas |
| `Toy_glass` | `#2a4d73` | all window ribbons and the arched window |
| `Toy_glassl` | `#6f95b8` | the entrance pyramid canopy |
| `Toy_ink` | `#3a3530` | street-level base band |
| `Toy_roofd` | `#45454a` | podium and tower roof decks, mechanical masses |
| `Toy_steel` | `#9aa0a6` | masts, railings |
| `Toy_mint` | `#8fd0a8` | terrace planting — the one saturated accent |
| `Toy_glass_Glow` | `#2a4d73` | *see below* |

**Night glow.** Two towers of 160 apartments each must read as *inhabited*, and the crown must
read as a landmark. Hero glow: the two **arched penthouse window bands**. Supporting: a
scattered subset (~30%) of the tower window ribbons split out as `Toy_glass_Glow`, and the
entrance canopy. Nothing else. Keep the glow material's **base colour the same as its day
neighbour** — a `_Glow` material's base colour *is* its night look, and its day colour must not
make the facade patchy (see [[sf3d-glow-colour-is-unlit]]). Do not build a closed glow shell
around the crown: a closed shell reads as two alpha layers by day and tints the whole cap
(see [[sf3d-glow-shell-day-alpha]]).

### 2.9 Top surface

The whole block is roof, and the camera looks straight at it. Three designed zones:

1. **Tower roofs** (two): a long rectangular mechanical penthouse along each lozenge's spine, the
   arched cap and mast, a `Toy_roofd` deck with a `Toy_trim` parapet, and — matching the owner's
   "23rd-floor decks" — a small railed terrace at one rounded end.
2. **Courtyard terrace** (podium roof, north-west quadrant): circular plaza, curved planters,
   pergolas, planting. This is the building's charm; do not skip it.
3. **Remaining podium roof**: two HVAC masses, one skylight row, otherwise clean `Toy_roofd`
   with the parapet reading as a crisp outline of the diamond block.

### 2.10 Scope

**In the GLB:** the 88 Howard podium on its DataSF footprint, both towers with crowns and masts,
the entrance canopy and arched window, the podium roof terrace and mechanical zones.

**Not in the GLB:** the Rincon Annex post office (separate footprint, separate asset), Howard /
Spear / Steuart Streets, the Embarcadero, neighbouring buildings, street trees, people, vehicles,
plinths, cameras or lights.

### 2.11 Triangle budget

Cap 18,000. Suggested split: podium body and bands ~6k; arcade, entrance and arched window ~1.5k;
podium roof and terrace ~2k; two tower bodies and balcony slabs ~5k; cornices, central bays,
arched caps and masts ~3k. The shared landmark `BatchedMesh` is close to full in SoMa
(see [[sf3d-landmark-batch-full]] / [[sf3d-batch-reserve-overflow]]) — spend less if the model
reads at 12k.

### 2.12 Draft manifest entry

```json
{
  "id": "towers-at-rincon",
  "file": "towers-at-rincon.glb",
  "anchor": [
    -122.3924873,
    37.7919896
  ],
  "targetHeightM": 89.0,
  "cat": 2,
  "name": "The Towers at Rincon (88 Howard Street)",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2670
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`loadRadius` is the default rule `max(2500, 89 × 30) = 2670`; the building is not skyline-scale,
so it streams and must **not** be `alwaysLoaded`.

### 2.13 Integration notes (for later, not this task)

- **Case B — new landmark.** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'towersAtRincon'`, `name: 'The Towers at Rincon'`, `lon: -122.3924873`,
  `lat: 37.7919896`, `height: 89`, `exclude: 32`, camera preset ~`{ distance: 620, yaw: 225,
  pitch: 20 }`) and re-bake.
- Manifest id `towers-at-rincon` → registry id `towersAtRincon` via `camelId()` in
  `app/src/assets.js`.
- **Exclusion sizing** (method: [[sf3d-exclusion-radius]], [[sf3d-exclusion-gate-is-anchor-distance]]).
  Measured from the anchor: my own DataSF ring's nearest vertex 4.2 m and centroid 1.4 m; the
  Overture duplicate ring's centroid 4.2 m; the **Rincon Annex's nearest vertex 34.8 m**. So the
  radius must kill both of my rings while staying under 34.8 m: **`exclude: 32`** (2.8 m margin).
  A radius large enough to cover my whole footprint (56.7 m) would eat the Annex, which is
  unnecessary — a footprint is dropped whole as soon as one vertex or its centroid is inside.
- **Two rings, not one** ([[sf3d-exclusion-two-rings]]): DataSF `201006.0000265` *and* Overture
  `5d51e5b1-…` both trace this building. Today the Overture ring is silently consumed by
  `buildings.mjs`'s height-correction branch because the DataSF ring exists; once the DataSF ring
  is excluded that branch no longer fires, so **the exclusion must cover the Overture ring too**.
  At `exclude: 32` both centroids (1.4 m and 4.2 m) are inside. Verify from the baked tile, not
  from `verify-rebake`'s per-cell counts ([[sf3d-verify-rebake-count-blindspot]]).
- **Two party-line slivers.** Overture also carries two ~240 m² wedges along the Annex party line
  (`314281a1-…` at 31.7 m from the anchor, `f5e0c8be-…` at 34.4 m). Today they are dropped by the
  `occupiedFraction` test; after the exclusion they *may* bake as ~8 m stubs. `exclude: 32`
  catches the first. **Check the baked tile for the second**; if it appears, add
  `extraExclusions: [{ lon, lat, r: 8 }]` centred on it (its centroid is local
  `(3913.4, −2429.0)` ≈ `-122.393328, 37.791970`), which clears it without reaching an Annex
  vertex (nearest Annex vertex to that centroid is ~10 m).
- The Annex itself keeps its procedural block at 29.7 m — correct, and the two buildings really do
  share a party wall, so a little contact between the asset's north-west face and the procedural
  Annex is expected, not a bug ([[sf3d-exclusion-unavoidable-collateral]]).
- A parallel session holds the `pipeline/rincon-center` branch (locked worktree). It presumably
  covers the **Annex**; if it turns out to claim the whole complex, the two plans must be
  reconciled before either merges ([[sf3d-batch-integrate-run]]).

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] bbox height exactly 89.00 m (so the loader's scale is 1.000)
- [ ] Dimensions plausible in meters and consistent with 2.1 (≈112 × 113 × 89 m)
- [ ] Triangles at or under 18,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the arched penthouse window bands, a subset of tower ribbons, and the
      entrance canopy — and no closed glow shell
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the
      union of solids; ray test ≤ 0.15 % residual)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **22 or 23 storeys?** CTBUH says 22 floors above ground for each tower; Wikipedia and the owner
  say 23. The recipe uses 6 podium + 16 typical + 2.5 in the central bay ≈ 24 levels of structure,
  which reproduces the *measured* heights (24.5 m and 87.2 m) at a 3.20 m residential floor. The
  height is measured, so the storey count is a labelling question, not a geometry one — but say
  which you used in `REPORT.md`.
- **OSM `height=93` vs CTBUH 89 m.** OSM is not a height authority here and disagrees with the
  LiDAR crest by 5.9 m. Use 89.0. If a better published figure surfaces, re-check before the
  manifest is written.
- **Tower plan fidelity.** The OSM `building:part` polygons are a mapper's 10-vertex
  approximation of curved towers; the satellite roof outlines are displaced ~9.5 m by lean.
  Treat the OSM parts as correct *positions* and the photographs as correct *shape*, and
  reconcile the two rather than trusting either alone.
- **Are the towers identical?** They read as mirrored twins with the same crown, but the west
  lozenge is ~4 m longer than the east one in OSM. Verify from imagery; if in doubt build one
  tower and mirror it, then adjust the plan outline per tower.
- **The Rain Column is gone.** Wikipedia's famous interior water feature was removed in the early
  2020s and is interior anyway — do not model it.
