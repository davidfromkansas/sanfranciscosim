# Hills Brothers Building (2 Harrison Street) — SF-SIM asset plan

George Kelham's 1926 Romanesque Revival coffee plant on the Embarcadero at Harrison —
red patterned brick, an arcaded top floor, a projecting campanile with a terracotta
pyramid roof, and the rooftop neon "HILLS BROS COFFEE" sign that still faces the bay
under the Bay Bridge approach. San Francisco Landmark No. 157, today the Hills Plaza 2
offices (Wharton SF, Google, Mozilla have all tenanted it).

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/hills-brothers-building/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `hills-brothers-building` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3892854, 37.7894167` (outer-ring bbox centre, measured) |
| Target height | **53.2 m** (tower pyramid finial, LiDAR `hgt_max`; main parapet ≈ 25.6 m, penthouse crest ≈ 29.5 m *estimated*) |
| OSM footprint | relation/2280956: outer ring 3,526 m², OBB 75.8 × 57.1 m at 45° to north; inner lightwell 247 m² |
| Triangle cap | 24,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Hills Brothers Building GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Hills Brothers Building (2 Harrison
Street, San Francisco) and deliver it as a downloadable, validated GLB.

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
8. `docs/asset-plans/hills-brothers-building.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- Red patterned-brick industrial quad around an inner lightwell, six storeys
  under a tall parapet
- The square campanile with paired slit windows up the shaft, an arcaded top
  stage, corbelled cornice and terracotta pyramid roof — the silhouette
- The rooftop neon "HILLS BROS COFFEE" sign facing the bay
- Arcaded top (6th) floor of round-arched windows under a corbel band
- The 1985 set-back cream penthouse floor with hipped terracotta roofs

## Research the Hills Brothers Building independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views (the 2011 HPC case report PDF in 2.2 contains an
  oblique aerial, a Pier 14 elevation photo and a parapet/roof-deck photo)
- Ground-level views, day and night appearance (the sign is lit red at night)
- The tower's exact plan position (it projects from the north-west long facade,
  vertices 13–16 in the 2.3 table) and its stage heights
- Window bay count and rhythm on the Embarcadero facade

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/hills-brothers-building/REFERENCE.md` containing: source links
and what each establishes; verified dimensions and location; orientation;
observations from all four sides and above; the 3-5 strongest recognition cues;
features to preserve; features to simplify; uncertainties and conflicting
evidence. A contact sheet of attributed reference thumbnails is welcome if
legally permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Hills Brothers
Building, consistent with the real building from all four sides and above,
architecturally credible, and a premium handcrafted miniature — not
photorealistic, not voxel art, not generic low-poly, and never accurate in one
view while invented in the others.

## Scope of the exported asset

Export the 1926 quad (six brick storeys + parapet), the inner lightwell, the
1985 penthouse floor with its hipped roofs, the campanile with its pyramid roof,
and the rooftop neon sign as a miniature lattice sign.

Do not include unrelated surrounding city geometry: the 345 Spear Street
building (Hills Plaza I), the 1989 condominium tower, the brick arched screen
wall and plaza between the buildings, the Embarcadero waterfront pavilion or
seawall, the Bay Bridge, streets, palm trees, people, vehicles, plinths,
cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no
external dependencies; at most 24,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the
model drops into the city at its real-world heading — the loader applies no
rotation (`placeGeneric` in `app/src/assets.js` only scales and positions). The
building's long Embarcadero facade faces south-east (normal ≈ 135°); the
street grid here runs 45° off north. Author true-world orientation from the 2.3
vertex table and document the heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/hills-brothers-building/build_hills_brothers_building.py`
(deterministic build script),
`artifacts/hills-brothers-building/hills-brothers-building.blend`, and
`artifacts/hills-brothers-building/hills-brothers-building.glb`. The script must
rebuild the model reliably enough for future revision. Do not modify or rename
an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`hills-brothers-building-top.png`, `hills-brothers-building-north.png`,
`hills-brothers-building-east.png`, `hills-brothers-building-south.png`,
`hills-brothers-building-west.png`, plus
`hills-brothers-building-contact-sheet.png` and at least one high three-quarter
aerial beauty render `hills-brothers-building-aerial.png`, plus a night render
showing the sign glow.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the quad roof, the
lightwell, the penthouse hips, the tower pyramid and the sign; the aerial view
uses the style bible's camera assumptions (30-50 degrees down, long lens).
Simple tabletop lighting, neutral warm background, minimal depth of field, and
every image must depict the same exported model.

## Validate the exported GLB

Re-import `hills-brothers-building.glb` into a fresh isolated Blender scene and
validate the re-import, not the source scene. Report object count, triangle
count, dimensions, bounding-box min/max, min Z, XY center offset, material
names, image-texture count, camera count, light count, animation count,
applied-transform status, negative-scale status, normal-orientation status,
unexpected geometry, and per-material contract compliance. Render at least one
review image from the re-imported asset. Write
`artifacts/hills-brothers-building/validation.json` and
`artifacts/hills-brothers-building/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include
this draft entry in `REPORT.md`. Do not edit the production manifest in this
task.

```json
{
  "id": "hills-brothers-building",
  "file": "hills-brothers-building.glb",
  "anchor": [
    -122.3892854,
    37.7894167
  ],
  "targetHeightM": 53.2,
  "cat": 3,
  "name": "Hills Brothers Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a
separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the
integration notes in `docs/asset-plans/hills-brothers-building.md`.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026. Values marked *inferred* or *estimated* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | 1924–1926 | SF Planning HPC case 2011.0417A; PCAD 1355 |
| Architect | George W. Kelham | PCAD, noehill, HPC report |
| Style | Romanesque Revival ("Mediterranean Romanesque") | HPC report, HMdb |
| Structure | Concrete frame clad in red brick, wood/steel industrial sash | HPC report |
| Storeys | Six historic + rooftop penthouse; a 7th floor was added inside the roof in 1985 (non-historic); leasing material counts 7 storeys | HPC report; LoopNet |
| Roof | Flat with tall parapet; 2011 roof deck sits 42 in below the parapet | HPC report |
| Sign | Large neon "Hills Bros Coffee" rooftop signage, a named character-defining feature | HPC report |
| Landmark | SF Landmark No. 157 (designation report 7 Nov 1982) | HPC report, noehill |
| Block/Lot | Assessor's Block 3744, Lot 005 | HPC draft motion (the case-report header's "4108/010" is contradicted by the motion and the parcel map) |
| Zoning | RH-DTR, 84-X/105-X | HPC report |
| Footprint | Outer ring 3,526 m², OBB 75.8 × 57.1 m; lightwell 247 m² (~15.8 × 15.7 m) | OSM relation/2280956 (measured) |
| Ground | 3.49 m NAVD88, effectively flat | DataSF LiDAR `ynuv-fyni` bldg 201006.0000430 |
| Main roof deck | 23.88 m (LiDAR mode over 15,681 cells) | DataSF LiDAR (measured) |
| Parapet crest | ≈ 25.6 m | *derived*: deck 23.88 + 24 in pedestal + 42 in parapet-above-deck (HPC) |
| Roof median | 26.23 m, mean 25.53, sd 9.44 (bimodal: deck + penthouse + tower) | DataSF LiDAR (measured) |
| Tower crest | 53.16 m (`hgt_max`); `peak_1st` 58.18 el − 3.49 gnd ≈ 54.7 | DataSF LiDAR; see 2.15 risk 1 (flagpole) |
| OSM height tag | 56 | OSM relation — close to the tower crest+pole; never a shell height here |
| Tenant history | Hills Bros until 1990s; Wharton SF from 2012; Google, Mozilla floors | Wikipedia |
| Complex context | 1950s north addition razed late 1980s; Hills Plaza (345 Spear office + 21-storey condo) built 1989–90 in matching brick | PCAD |

### 2.2 Sources

- https://www.openstreetmap.org/relation/2280956 — footprint, lightwell, `height=56`, name
- https://pcad.lib.washington.edu/building/1355/ — Kelham, 1926, the 1950s addition and its demolition, Hills Plaza chronology
- https://noehill.com/sf/landmarks/sf157.asp — Landmark 157, Romanesque Revival, patterned brickwork, arched doorways/windows, bronze grillwork doors, tower's gravity-blending function
- https://default.sfplanning.org/meetingarchive/planning_dept/commissions.sfplanning.org/hpcpackets/2011.0417A.pdf — SF Planning HPC Certificate of Appropriateness (June 2011): property description, block/lot, 1985 seventh-floor addition, roof-deck dimensions, **parcel map, Sanborn map, oblique aerial photo, Pier 14 elevation photo, roof/parapet photo**
- https://www.hmdb.org/m.asp?m=72585 — historical marker: 1924 "Mediterranean Romanesque", south tower stored beans, rest of complex ground and roasted
- https://en.wikipedia.org/wiki/Hills_Brothers_Coffee — landmark status, Wharton/Google/Mozilla tenancy
- https://www.loopnet.com/Listing/2-Harrison-St-San-Francisco-CA/8306413/ — "Hills Plaza 2", 7 storeys, 213,731 SF, ~30,213 SF floor plate, renovated 1989
- https://commons.wikimedia.org/wiki/File:Hills_Bros._Building_-_San_Francisco.JPG — night elevation from the bay (lit sign, lit tower arcade)
- https://commons.wikimedia.org/wiki/File:Hills_Bros._Building_-_San_Francisco.jpg — courtyard triple-arch screen wall (context only, out of scope)
- DataSF `ynuv-fyni` (LiDAR building footprints): building 201006.0000430 = this building alone; 201006.0000159 = the 1989 complex to the north (its own max 68.5 m is the condo tower, which proves the 53.16 max belongs to this building's tower)
- Esri World Imagery z19 nadir (accessed 19 Aug 2026) — roof plan: quad + lightwell, penthouse hips, tower pyramid, mechanical rows on the north-east wing

Exa searches used: "Hills Brothers Coffee Building 2 Harrison Street San Francisco
architect history landmark" (pcad, noehill, sfplanning, hmdb, theclio, hillsbros);
"Hills Plaza 2 Harrison Street San Francisco building height feet tower clock
campanile stories" (loopnet, jll, gbig, commercialcafe — no published height in any
of them; height rests on LiDAR).

### 2.3 Orientation and placement

The street grid here runs 45° off north: the long Embarcadero facade (75.4 m)
faces **south-east** (normal ≈ 135°), Harrison Street is the **south-west** side,
Folsom/the plaza block interior the north, Spear Street beyond the plaza to the
north-west. The tower projects 12.9 m outward from the **north-west long facade**
(toward the mid-block plaza shared with 345 Spear), 15.5 m wide along that
facade, at its south-west end. The neon sign stands on the roof edge of the
Embarcadero wing near the Harrison (Bay Bridge) corner, its face toward the bay
(north-east-ish reading in photos from Pier 14).

Outer-ring vertices in the app's local meters (x east, z south-negative? — the
projection is `x=(lon−LON0)·111320·cos(LAT0)`, `z=−(lat−LAT0)·110540`, i.e.
**more negative z = further north**):

```
 0: 4230.29, -2165.14    6: 4278.93, -2162.95   12: 4204.50, -2138.42
 1: 4249.49, -2184.97    7: 4284.75, -2157.04   13: 4219.53, -2153.98
 2: 4251.45, -2186.90    8: 4231.27, -2103.91   14: 4210.15, -2162.90
 3: 4253.28, -2188.74    9: 4227.44, -2107.71   15: 4220.91, -2174.06
 4: 4267.02, -2174.94   10: 4223.11, -2112.01   16: 4230.29, -2165.14
 5: 4277.03, -2164.94   11: 4200.62, -2134.34
```

Edge 7→8 is the 75.4 m Embarcadero facade; vertices 13–16 are the tower
projection (15.5 × 12.9 m); the inner lightwell is the square
(4224.4,−2148.3)–(4246.9,−2148.2) rotated 45°, centre ≈ (4235.7, −2148.3).
Manifest anchor = outer-ring **bbox centre** `(-122.3892854, 37.7894167)`
(84.1 × 84.8 m axis-aligned) — author the model so its bbox centre sits at the
origin, or the loader will shift it (the OBB centre and area centroid differ
from the bbox centre by ~5 m here; see `docs/asset-plans/README.md` on the two
anchors).

### 2.4 What each side shows

**South-east (The Embarcadero)** — The hero elevation, 75.4 m: a two-storey
brick base with large arched openings, then floors of paired rectangular
industrial sash between brick piers (~13 bays, *estimated from photos*), an
arcaded 6th floor of round-arched windows, a corbel band, patterned/diapered
brickwork at the tall parapet. The neon sign rides above the parapet near the
south (Harrison/Bay Bridge) end on an open steel lattice.

**South-west (Harrison Street)** — Same composition, 57 m; arched ground-floor
openings with bronze grillwork doors at the entrance; the Bay Bridge approach
passes diagonally overhead just south of the building.

**North-west (plaza side, toward Spear)** — The long rear facade onto the
mid-block plaza; the campanile projects here: smooth brick shaft with paired
slit windows, an arcaded top stage (tall narrow arches on each face), corbelled
cornice, low parapet, terracotta pyramid roof with a finial (and a flagpole —
see 2.15). The brick triple-arch screen wall beyond is the 1989 complex, out of
scope.

**North-east (Folsom side)** — Shorter return facade in the same brick; beyond
it the 1989 Hills Plaza buildings (out of scope).

**Top** — A quad of flat roof around the lightwell. The 1985 penthouse floor
sits back from the parapet as cream stucco volumes with hipped terracotta
(standing-seam, brick-red) roofs around the lightwell — from above the roof
reads as a red-brown "roof ring" inside the brick parapet. The north-east wing
carries pale gravel roof with rows of mechanical/skylight units. The tower
pyramid and the sign lattice complete the top.

### 2.5 Recognition cues (ranked)

1. The square brick campanile with arcaded top stage and terracotta pyramid roof
2. The rooftop neon "HILLS BROS COFFEE" sign facing the bay
3. Red patterned-brick quad, six storeys, arcaded top floor under a corbel
   cornice, right at the water's edge beside the Bay Bridge touchdown
4. The inner lightwell and the red-hipped penthouse ring visible from above

### 2.6 Miniature translation

**Preserve**

- The quad massing on its true 45° grid, with the lightwell
- The campanile's silhouette: shaft, arcade stage, corbel, pyramid, finial
- The sign as a legible miniature lattice sign — the night identity
- The 6th-floor arcade + corbel band as the facade's top accent
- The penthouse's red hipped roofs — the aerial identity

**Simplify / exaggerate**

- Facade rhythm compresses to ~9–11 broad bays of recessed window pads per long
  facade; paired sash becomes one clean recessed panel per bay
- Patterned brickwork becomes one trim band at the parapet, not modeled diaper
- The arcade floor becomes arched-top recesses (low-seg arcs, 8–12 segments)
- The tower arcade becomes 3 arched recesses per face; slit windows become two
  thin recessed strips per face
- Rooftop mechanicals become 2–3 tidy blocks on the north-east wing
- The sign becomes a thin lattice frame carrying chunky letterforms (modeled as
  simple extruded boxes suggesting "HILLS BROS COFFEE", not typographically
  literal)

### 2.7 Massing recipe

Build order for the deterministic script; author in building axes u (along the
75.4 m Embarcadero facade, bearing 225°) × v (toward the plaza, bearing 315°),
then rotate the whole model 45° so it lands true-north (see 2.3 vertex table —
and mind the winding: a uv→world map with a reflection inverts every face, per
`sf3d-building-axis-winding`).

1. Quad body: the outer ring extruded z=0→23.9 (`Toy_brick`), lightwell cut as
   a courtyard (build the quad as four wing prisms sharing corner planes — no
   booleans), parapet band continuing to 25.6 with a 0.4 m `Toy_trim` cap band
   and a corbel band at 23.2.
2. Base: ground-floor arched openings as recessed panels (`Toy_ink` recess,
   arched tops) on the SE and SW facades; two storeys of base articulation to
   z≈8.5.
3. Shaft windows: recessed window pads (0.25 m) floors 3–5, `Toy_glass`; 6th
   floor arched pads under the corbel band.
4. Penthouse (1985): set-back cream volumes (`Toy_cream`) z=25.6→28.0 around
   the lightwell, hipped roofs (`Toy_rust`) cresting ≈ 29.5, gable accent on
   the bay side (the cream gable with arched window visible behind the sign).
5. Tower: 15.5 × 12.9 m projection on the NW facade (embed it into the wall,
   never a floating offset shell): brick shaft z=0→40 with paired slit
   recesses, arcade stage 40→48 with 3 arched recesses per face, corbel band,
   parapet, pyramid roof (`Toy_rust`) 48.5→53.0, finial to 53.2.
6. Sign: on the SE wing roof near the south corner — thin `Toy_steel` lattice
   posts and frame, letter blocks `Toy_red` with `Toy_red_Glow` faces
   (day-matched red, reads as the lit sign at night), top of letters ≈ 30–31 m.
7. Mechanical blocks on the NE wing roof (`Toy_steel` / `Toy_roofd`), one roof
   deck patch (`Toy_stone`) on the SE wing.
8. Bevel 0.10–0.12 m, 2 segments, on exposed massing edges only (never on flat
   window pads — see `sf3d-bevel-budget-flat-panels`).

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `#c96f4a` | all brick: quad body, parapet, tower shaft |
| `Toy_rust` | `#a86444` | terracotta roofs: tower pyramid, penthouse hips |
| `Toy_trim` | `#f3efe6` | parapet cap, corbel bands, window sills, tower arcade trim |
| `Toy_cream` | `#f2ede3` | 1985 penthouse walls |
| `Toy_glass` | `#2a4d73` | window pads |
| `Toy_ink` | `#3a3530` | ground-floor arched recesses, sign lattice shadow faces |
| `Toy_stone` | `#d9d2c2` | roof deck patch, base plinth course |
| `Toy_roofd` | `#45454a` | flat roof field inside the parapet |
| `Toy_steel` | `#9aa0a6` | sign lattice, mechanical blocks, finial |
| `Toy_red` | `#c4453c` | sign letter blocks (day) |
| `Toy_red_Glow` | `#c4453c` | sign letter faces (night glow — the hero glow) |
| `Toy_white_Glow` | `#f7f4ec` | tower arcade openings (soft night accent, per the night photo) |

Night glow: the sign is the hero; the tower's arcade stage openings glow softly
(both are lit in the Commons night photo). Nothing else. Glow faces must be
their own thin plates in front of opaque geometry, never a closed shell and
never coplanar with a solid (`sf3d-glow-face-needs-own-plate`,
`sf3d-glow-shell-day-alpha`).

### 2.9 Top surface

The camera looks down on a quad roof next to the Bay Bridge: design it. The red
penthouse roof ring around the lightwell, the pale NE-wing mechanical rows as
2–3 tidy blocks, one stone roof-deck patch (the 2011 deck), the tower pyramid,
and the sign lattice give the roof five deliberate layers. The lightwell must
read as a real void with visible inner walls, not a dark decal.

### 2.10 Scope

**In the GLB:** the 1926 quad with lightwell, parapet, 1985 penthouse +
hipped roofs, campanile with pyramid and finial, rooftop neon sign lattice,
tidy rooftop mechanicals.

**Not in the GLB:** 345 Spear St / Hills Plaza I, the 1989 condo tower, the
plaza and its triple-arch brick screen wall, the waterfront pavilion and
seawall, the Bay Bridge and its piers, streets, palms, people, vehicles,
plinths, cameras or lights.

### 2.11 Triangle budget

Cap 24,000. Suggested split: quad body + parapet + windows ~11k, tower ~4k,
penthouse + roofs ~3k, sign ~3k, base arches + mechanicals ~2k, bevels within
each budget.

### 2.12 Draft manifest entry

```json
{
  "id": "hills-brothers-building",
  "file": "hills-brothers-building.glb",
  "anchor": [
    -122.3892854,
    37.7894167
  ],
  "targetHeightM": 53.2,
  "cat": 3,
  "name": "Hills Brothers Building",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`targetHeightM` 53.2 is the tower finial crest (LiDAR max) — the export's bbox
top must be normalized to it exactly.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'hills-brothers-building'` → camelId `hillsBrothersBuilding`, lon/lat =
  anchor, `h: 53.2`) and re-bake the affected tiles.
- **Exclusion:** size `exclude` from `excluded()`'s real test — min(centroid,
  any vertex) distance from the ANCHOR — against BOTH bake sources, and check
  which rings each source carries (`sf3d-exclusion-two-rings`,
  `sf3d-exclusion-centroid-catches-overture`). Distances from the anchor
  (4242.7, −2146.3): own-ring vertices run ~8–45 m; the far corners (v3 ≈ 44 m,
  v8 ≈ 44 m, v11 ≈ 43.7 m) set the needed radius ≈ 45 m. The nearest foreign
  structures are the 1989 complex beyond the ~25 m plaza gap to the north-west
  (LiDAR row 201006.0000159) and the small waterfront pavilion across the
  Embarcadero promenade — verify at bake time that r=45–48 clears our rings
  without touching either; if the sources merge the plaza screen wall into a
  neighbour ring, measure, don't assume (`sf3d-merged-parcel-exclusion`).
- **Streaming:** default rule gives `loadRadius: 2500`
  (max(2500, 53.2 × 30 = 1596)); no `alwaysLoaded`.
- The anchor is the OSM bbox centre; the registry entry uses the same lon/lat
  so the exclusion is measured from the point the model actually lands on
  (`sf3d-two-anchors-bbox-vs-footprint`).

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Dimensions ≈ 84 × 85 m plan (rotated quad + tower), height exactly 53.2
- [ ] Triangles at or under 24,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on sign letter faces and tower arcade plates
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (deterministic ray test)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **Is the 53.16 m LiDAR max the masonry finial or the flagpole?** `hgt_max`
   and `peak_1st` are the same point (`sf3d-lidar-max-is-a-flagpole`), and the
   tower flies a flag on a pole above the pyramid. The pyramid+finial vs pole
   difference is a few meters; OSM's `height=56` is consistent with the pole
   tip. The plan takes 53.2 as the finial crest and omits the pole; if build-
   stage photo measurement puts the masonry crest materially lower (< 50 m),
   correct `targetHeightM` and re-normalize — the tower, not the pole, is the
   silhouette.
2. **No published height exists anywhere** — leasing, planning, PCAD and press
   all skip it. Everything vertical here is LiDAR plus the HPC parapet
   arithmetic; the parapet (25.6 m) and penthouse crest (~29.5 m) are derived,
   not published. Labelled estimated accordingly.
3. **Tower stage heights are unmeasured.** Shaft/arcade/pyramid proportions in
   2.7 (40 / 48 / 53.2) are read off oblique photos; verify against a rectified
   elevation before modeling (`sf3d-rectified-elevation-recipe`), and beware
   equirect bowing on any pano crop (`sf3d-cylindrical-projection-fake-curves`).
4. **Bay count on the long facades is estimated (~13)** from oblique photos;
   the miniature compresses it anyway (2.6), but count once from a rectified
   pano so the rhythm is right.
5. **The sign's exact roof position and length are estimated** from the Pier 14
   and night photos (south end of the Embarcadero wing, face to the bay). Its
   letters are a stylized suggestion — do not attempt literal neon typography
   at this scale.
6. **The LiDAR footprint merges two low strips north-west of the OSM ring**
   (plaza-side arcade structures). They are excluded from scope; at integration
   the exclusion radius analysis must remember the bake sources may trace them
   (2.13).
