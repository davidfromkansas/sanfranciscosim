# Four Embarcadero Center — SF-SIM asset plan

The tallest of John Portman's four Embarcadero Center towers and the tallest waterfront
building in the Bay Area. Its identity is a contradiction the skyline needs: **a blunt
pale cliff from the north or south, a stepped stack of spiked fins from the east or
west** (John King, SF Chronicle, 2012). A dense cream precast grid, not a glass box —
the opposite language to Salesforce Tower two blocks inland.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/4-embarcadero-center/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `4-embarcadero-center` |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3961998, 37.7953001` (OBB centre of OSM way/616812910) |
| Target height | **179.0 m** rooftop-plant crest — main parapet **173.7 m** (570 ft), 45 storeys (see 2.1) |
| OSM footprint | 63.5 x 37.3 m OBB, long axis bearing **81.09 deg** from true north (OSM way/616812910, 2,170 m2) |
| Triangle cap | 20,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Four Embarcadero Center GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Four Embarcadero Center (55 Clay Street) in San
Francisco and deliver it as a downloadable, validated GLB.

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
8. `docs/asset-plans/4-embarcadero-center.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A pale cream precast slab, not a glass tower — colour and grain are the first cue
- Flat blunt roofline across the long north and south faces
- The **stepped chevron crown at both short (east and west) ends**: parallel N–S fins
  whose tops step down away from a central spine, and whose plan projections step
  back from a central peak. Six fins per end, symmetric about a point just north of
  centre. This is the recognition feature — do not flatten it.
- A dense, fine, dark punched-window grid with strong vertical piers
- The rooftop cooling-tower row (four large circular units) — the camera looks down
- The chopped-back north-west corner where the tower meets Clay and Drumm

## Research Four Embarcadero Center independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views
- Ground-level views
- Day and night appearance
- Publicly available drawings, plans or diagrams
- **The crown step heights.** This plan's tier levels (2.7) are *estimated* from
  perspective photography. Find a rectified or long-lens elevation and count floors.
- **The west end.** Every good photograph found for this plan shows the EAST end.
  The west-end crown is inferred by mirroring. Verify from Drumm Street / Sacramento
  Street or an aerial.
- Whether the roof has a north–south level change (see 2.15 risk 3)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/4-embarcadero-center/REFERENCE.md` containing: source links and what each
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

The finished asset must be immediately recognizable as Four Embarcadero Center, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the tower shaft, its stepped end crowns, the facade rhythm, the rooftop plant,
and a low plinth representing the Embarcadero Center podium immediately under the tower
footprint (2 m tall, footprint + ~3 m).

Do not include unrelated surrounding city geometry: the rest of the Embarcadero Center
complex (towers One–Three, the Hyatt Regency, the retail spine and its elevated
promenade bridges), Sue Bierman Park, Clay/Drumm/Sacramento Streets, neighbouring
towers, trees, people, vehicles, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 20,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). Build the tower with
its long axis along local X and then rotate the whole model **+8.91 deg about Z**
(long axis bearing 81.09 deg), and apply the transform. The main entrance is on the
**north** face (55 Clay Street), so the `-Y` front convention is *not* satisfied —
this is a true-world-oriented landmark like `555-california`. Record the decision and
the measured heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS is at `/opt/blender` (`blender` on PATH). Headless only:
`blender -b --python script.py -- args`; no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/4-embarcadero-center/build_4_embarcadero_center.py` (deterministic build
script), `artifacts/4-embarcadero-center/4-embarcadero-center.blend`, and
`artifacts/4-embarcadero-center/4-embarcadero-center.glb`. The script must rebuild the
model reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`4-embarcadero-center-top.png`, `4-embarcadero-center-north.png`, `4-embarcadero-center-east.png`,
`4-embarcadero-center-south.png`, `4-embarcadero-center-west.png`, plus
`4-embarcadero-center-contact-sheet.png` and at least one high three-quarter aerial beauty
render `4-embarcadero-center-aerial.png`, plus a night render
`4-embarcadero-center-night.png` and a night tile on the contact sheet.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation. **The east and west elevations are the money shots** —
they must show the stepped chevron crown reading clearly. The top view must show the
roof deck, the cooling-tower row, the parapet and the stepped shoulders of both end
crowns. The aerial view uses the style bible's camera assumptions (30-50 degrees down,
long lens). Simple tabletop lighting, neutral warm background, minimal depth of field,
and every image must depict the same exported model.

## Validate the exported GLB

Re-import `4-embarcadero-center.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/4-embarcadero-center/validation.json` and
`artifacts/4-embarcadero-center/REPORT.md`.

**Normalize the bbox top to 179.0 m exactly** so the loader's
`targetHeightM / measuredHeight` scale lands at 1.0. The 179.0 m is the top of the
rooftop cooling towers; the main parapet sits at 173.7 m. Do not model the flagpole.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "4-embarcadero-center",
  "file": "4-embarcadero-center.glb",
  "anchor": [
    -122.3961998,
    37.7953001
  ],
  "targetHeightM": 179.0,
  "cat": 3,
  "name": "Four Embarcadero Center",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/4-embarcadero-center.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Official name | Four Embarcadero Center | CTBUH, Wikidata Q3056626 |
| Street address | 55 Clay Street, San Francisco CA 94111 | CTBUH, Structurae, Wikipedia. **Not 94105** — the prompt's ZIP is wrong, the building is right. |
| Architectural height (roof) | **173.7 m / 570 ft** | CTBUH 173.7; SkyscraperPage 173.7; Wikipedia 173.74; Structurae 174; OSM tag 174. Converged. |
| Rooftop-plant crest | **179.05 m** | DataSF LiDAR 2010 `hgt_maxcm` = 17905 over the tower footprint. 5.35 m above the parapet = the cooling-tower row. Used as `targetHeightM` (see 2.15 risk 1). |
| Floors | 45 above ground | CTBUH, Wikidata, OSM `building:levels=45` |
| Implied floor-to-floor | 3.86 m | 173.7 / 45, *derived* |
| Completed | **1982** | Wikipedia, Structurae, SkyscraperPage, Wikidata all 1982. CTBUH says 1984, Schindler 1981, SFYIMBY 1979 — *conflict, 1982 wins 4–1*. |
| Architect | John Portman & Associates (John C. Portman Jr.) | CTBUH, Wikidata (Q764692), Structurae, PCAD |
| Developer | David Rockefeller / Trammell Crow / Portman | SFYIMBY, SPUR |
| Owner | Boston Properties (since 1998) | Wikipedia, CTBUH |
| Structure | All-steel frame, concrete slabs | CTBUH |
| Cladding | Precast concrete panel grid with punched windows, warm off-white | *inferred from photography* — "buildingsdb" calls it a glass/metal curtain wall, which the photographs contradict; SPUR and bisbeearchitecture describe the complex as precast concrete. Treat as precast. |
| Style | Late Modern / Brutalist-adjacent | SPUR, buildingsdb |
| Floor area | 1.1 M sq ft total, 858,600 sq ft office | SFYIMBY |
| Footprint | 63.46 x 37.34 m OBB, 2,170 m2 actual polygon | OSM way/616812910, measured (2.3) |
| DataSF footprint | 3,142 m2 (`sf16_bldgid` 201006.0000633) | larger than OSM — includes podium apron; matters for `exclude` (2.13) |
| Ground elevation | ~3.6 m NAVD88 | DataSF `peak_1st_m` 182.69 minus `hgt_max` 179.05 |
| Rank | 13th tallest in San Francisco; tallest of the Embarcadero Center complex | CTBUH |

### 2.2 Sources

- https://www.openstreetmap.org/way/616812910 — footprint geometry (24 nodes), `height=174`, `building:levels=45`, `alt_name=Four Embarcadero Center`, `wikidata=Q3056626`
- https://www.wikidata.org/wiki/Q3056626 — 45 floors, 1982, architect Q764692, coordinate
- https://en.wikipedia.org/wiki/Four_Embarcadero_Center — 174 m / 571 ft, roof 173.74 m, 45 storeys, 1982, ownership history
- https://www.skyscrapercenter.com/building/four-embarcadero-center/2589 — CTBUH record: 173.7 m architectural, 45 floors, all-steel, 55 Clay Street, LEED Gold. **Primary photo source** (Terri Meyer Boake ×11, Nathaniel Lindsey ×2, Dan Safarik ×1) — the two Lindsey images are the clearest crown views.
- https://structurae.net/en/structures/four-embarcadero-center — 174 m, 45 floors, 1982
- https://skyscraperpage.com/diagrams/?buildingID=2132 — three orthographic elevation diagrams, roof 173.7 m (not yet mined; **the executing agent should mine these for the crown step heights**)
- https://sfyimby.com/2021/09/number-18-four-embarcadero-center-financial-district-san-francisco.html — five Andrew Campbell Nelson photographs. `…rising-above-Sue-Bierman-Park…` is the **north elevation, near-orthographic** — it establishes the flat blunt north roofline. `…documented-from-the-western-side-of-the-Ferry-Building…` is the clearest **east-end crown**.
- https://www.spur.org/publications/urbanist-article/2014-07-17/urban-field-notes-rockefeller-center-west — John King's silhouette description ("a blunt cliff when viewed from north or south, spiked outcrops from east or west"); the irregular floor plan giving 10–14 corner offices per floor
- https://portmanarchitects.com/project/embarcadero-center/ — architect's own project record for the complex
- https://www.schindler.com/…/four-embarcadero-center.pdf — 23 elevators, LEED Gold retrofit, 571 ft
- https://data.sfgov.org/resource/ynuv-fyni.json — DataSF 2010 LiDAR building heights (`hgt_maxcm` 17905, `hgt_mediancm` 15099, `hgt_stdcm` 6260, 12,569 cells)
- Google satellite tiles z19/z20 at 37.7953/−122.3962 — roof plan: pale deck, **four large circular cooling towers in a row**, mechanical curbs, window-washing davit track

Exa queries run (all `web_search_advanced_exa`): "Four Embarcadero Center San Francisco John Portman tower architecture height" (8 results, summaries on height/floors/architect/facade) and "Embarcadero Center tower Portman precast concrete facade notched corners stepped plan design description" (8 results). Domains that actually yielded photography: `skyscrapercenter.com`, `sfyimby.com`. Facts confirmed by them: 173.7 m, 45 floors, 1982, John Portman & Associates, all-steel, 55 Clay Street. Real-estate listing sources were not used.

### 2.3 Orientation and placement

Measured from the OSM polygon in the project's local tangent projection
(`x=(lon+122.4375)*111320*cos(37.77)`, `z=-(lat-37.77)*110540`):

- Minimum-area OBB: **63.46 m x 37.34 m**, long axis **bearing 81.09 deg** from true
  north (the Financial District grid). Perpendicular 171.09 deg.
- OBB centre `-122.3961998, 37.7953001` — 6 cm from the polygon's shoelace centroid, so
  there is no rear-wing centroid skew here. Use the OBB centre as the anchor.
- Polygon area 2,169.7 m2; OBB area 2,369.9 m2 (the difference is the end steps).

Street check against OSM centrelines, expressed in the OBB frame:

| Street | Nearest distance | Side |
|---|---|---|
| Clay Street | 32.1 m | **north** |
| Drumm Street | 41.4 m | **west** |
| Sacramento Street | 82.9 m | south |

So: **long faces look north (Clay Street / Sue Bierman Park) and south (into the
Embarcadero Center podium plaza); short ends look east (toward the Embarcadero and the
Ferry Building) and west (toward Drumm Street and Embarcadero Center 3).** The address
55 Clay Street puts the entrance on the north face.

Author `+Y` = true north, `+X` = east; build along local X then rotate +8.91 deg about Z.

### 2.4 The footprint, strip by strip

This is the plan's most useful measurement and the reason the building looks the way it
does. In the OBB frame (`u` = along the long axis, +u east; `v` = across, **+v = south**,
origin at the anchor), the polygon is a rectangle whose two short ends are **staircase
chevrons** peaking just north of centre:

**East end** — six N→S strips, with how far east each one reaches:

| Strip (v range, m) | Width | Reaches u = |
|---|---|---|
| −18.61 … −13.29 (north corner) | 5.3 | +26.84 |
| −13.29 … −6.30 | 7.0 | +28.65 |
| −6.30 … −1.00 | 5.3 | +29.28 |
| −1.00 … +4.89 (**centre spine**) | 5.9 | **+31.73** |
| +4.89 … +11.20 | 6.3 | +28.98 |
| +11.20 … +18.67 (south corner) | 7.5 | +26.52 |

**West end** — four strips:

| Strip (v range, m) | Width | Reaches u = |
|---|---|---|
| −18.68 … −13.26 (north corner) | 5.4 | **−24.46** (chopped back 5.5 m at Clay/Drumm) |
| −13.26 … −6.19 | 7.1 | −30.01 |
| −6.19 … −0.20 (**centre spine**) | 6.0 | **−31.72** |
| −0.20 … +18.67 (south half) | 18.9 | −30.20 |

**Long faces** — the south face is one clean straight 56.74 m run at v = +18.67. The
north face is one straight 51.3 m run at v = −18.6, ending at the chopped NW corner.
Both are flat: no bays, no facets, no setbacks. This is King's "blunt cliff".

### 2.5 What each side shows

**North (Clay Street / Sue Bierman Park)** — The flat blunt cliff. A perfectly
horizontal roofline across the full length, then the east-end fins stepping down beyond
it. The entrance side, over a low landscaped podium. Near-orthographic reference:
SFYIMBY "rising above Sue Bierman Park".

**South (podium plaza)** — The same blunt cliff, 63.5 m of it, rising out of the
Embarcadero Center elevated promenade deck (planters, flowering trees). Least
documented side; assume it mirrors the north minus the entrance.

**East (toward the Embarcadero)** — The signature elevation. Six parallel N–S fins
whose plan projections step out to a central spine and whose tops step **down** away
from that spine. Roughly five distinct top levels are visible. The flagpole sits on the
spine. Reference: SFYIMBY "from the western side of the Ferry Building"; CTBUH
Nathaniel Lindsey ×2.

**West (Drumm Street)** — A shallower version of the same chevron (only 1.7 m of plan
projection rather than 5.2 m) plus the chopped-back NW corner. *Inferred* — verify.

**Top** — A pale flat deck at 173.7 m with a parapet. On its north half, a raised
mechanical curb carrying **four large circular cooling towers in a row** (the crest at
179.05 m), a couple of small penthouse boxes, and a window-washing davit and track.
Both end crowns present as descending stepped shoulders. From the app's camera this
roof is a facade — design it.

### 2.6 Recognition cues (ranked)

1. **The stepped chevron crown at both short ends** — spiked outcrops against a flat
   long roofline. Nothing else in the city does this.
2. **Cream precast, not glass** — a pale, warm, opaque tower in a district of dark
   glass. Colour is the second cue and it is doing a lot of work at distance.
3. **The fine dark punched-window grid** — dense, regular, small openings; the facade
   reads as texture, not as reflection.
4. **Slab proportions** — 63.5 x 37.3 m plan at 174 m: broad from north/south, narrow
   from east/west.
5. **The rooftop cooling-tower row** — four circles in a line, visible from above.

### 2.7 Miniature translation

**Preserve**

- 63.5 x 37.3 m plan, 173.7 m parapet, 179.0 m plant crest
- The six-strip east chevron and its stepped tops
- The chopped NW corner
- Flat, unbroken north and south rooflines
- Warm off-white body against dark windows

**Simplify / exaggerate**

- ~45 real window bays per long face become **22 pier/window modules** (2.9 m pitch);
  ~26 per short face become 13. Per-floor spandrel geometry is dropped entirely — the
  window slot runs full height and the horizontal rhythm is carried by trim bands only
  at the base, the step levels and the parapet.
- The end steps are **exaggerated**: give each fin a crisp 0.25 m reveal on both sides
  so the chevron reads at 200 px, and widen the plan projection of the centre spine
  from 5.2 m to ~6 m at the east end and from 1.7 m to ~3 m at the west end.
- The complex's promenade bridges, the retail spine and the neighbouring towers are out
  of scope; the podium becomes a single low plinth.
- Rooftop plant becomes exactly the four cooling towers plus one penthouse box —
  organised in two groups, not scattered.

### 2.8 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. All coordinates in the
pre-rotation local frame (`x` = long axis, `y` = north-positive, i.e. `y = -v`), rotated
+8.91 deg about Z at the end.

1. **Plinth** — 70 x 44 m plate, `z = 0 … 2.0`, `Toy_stone`. Represents the Embarcadero
   Center podium deck the tower stands on. Chamfer the NW corner to match.
2. **Base band** — the tower footprint, `z = 2.0 … 12.0`, `Toy_cream`, with a recessed
   `Toy_glass` lobby band at `z = 3 … 9` on the north face only (55 Clay Street), behind
   chunky piers.
3. **Core shaft** — the full staircase footprint of 2.4 extruded `z = 12.0 … 135.0`,
   `Toy_sand`. Build the footprint from the strip table so the chevron ends and the
   chopped NW corner are real geometry, not a bevel.
4. **Tier 2** — drop the outermost strip of each end (east `u > 26.5` north-corner and
   south-corner strips; west north-corner strip) at `z = 135.0`. Everything else
   continues to `z = 154.4`. *Step heights estimated — see 2.15 risk 2.*
5. **Tier 3** — drop the next strip in on each end at `z = 154.4`. The remaining mass —
   the full long-face slab plus the centre spines — continues to `z = 173.7`.
6. **Parapets** — a 1.2 m `Toy_cream` parapet ring on every tier top (135.0, 154.4,
   173.7), with a `Toy_steel` deck inside each. Three visible roof levels per end.
7. **Facade modules** — 22 vertical `Toy_cream` piers per long face and 13 per short
   face, 0.35 m proud, running `z = 12 … tier top`; between them a `Toy_glass` slot
   inset 0.25 m, full height. Do **not** model individual floors.
8. **Trim bands** — `Toy_trim` horizontal bands 0.6 m tall at `z = 12`, at each tier
   parapet base and under the main parapet, wrapping all faces.
9. **Rooftop plant** — on the main 173.7 m deck, a `Toy_steel` curb 24 x 8 x 1.2 m on
   the north half carrying **four cylinders** (14 segments, r = 2.6 m, h = 4.1 m, top at
   **179.0 m**), `Toy_steel` with a `Toy_ink` grille disc on top. Plus one penthouse box
   9 x 6 x 3.5 m and a 12 m davit track line.
10. **Bevel** 0.12 m, 2 segments — the fin reveals and the pier edges must stay crisp,
    so keep the bevel small.

### 2.9 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | the precast body — warm off-white, the primary colour |
| `Toy_cream` | `#f2ede3` | piers, parapets, base band — a half-step lighter so the crown steps read |
| `Toy_trim` | `#f3efe6` | horizontal trim bands |
| `Toy_glass` | `#2a4d73` | the dark punched-window slots |
| `Toy_stone` | `#d9d2c2` | podium plinth |
| `Toy_steel` | `#9aa0a6` | roof decks, cooling towers, curbs |
| `Toy_ink` | `#3a3530` | cooling-tower grille discs |
| `Toy_glassl_Glow` | `#6f95b8` | lit windows and the crown band at night |
| `Toy_red_Glow` | `#c4453c` | aviation obstruction bead on the spine |

**Do not use `Toy_roofd` for the roof decks.** It renders near-black (rgb 9,9,12) on a
horizontal surface under the app's lighting and destroys the pale-tower read; `Toy_steel`
is the correct choice here.

### 2.10 Night state (required)

Hero glow: a continuous `Toy_glassl_Glow` band on the top three modules of the tower,
wrapping all four faces, so the stepped crown lights up as three descending rings —
the silhouette that identifies the building by day is the one that glows by night.

Supporting: roughly one window slot in three, in an irregular but deterministic pattern
(seeded, not random per build), switched from `Toy_glass` to `Toy_glassl_Glow` down the
shaft; plus the north lobby band. One `Toy_red_Glow` bead at the top of the centre spine.

Day check: `Toy_glassl` `#6f95b8` is a pale sky-blue that sits plausibly among the
daytime facade colours next to `Toy_glass` `#2a4d73` — the lit windows must not read as
a different material in daylight. Do **not** build the glow as a closed shell around the
body; use separate inset faces only, or it will tint the whole facade in daylight.

### 2.11 Top surface

The roof is a facade here — the app camera looks down at it and this tower is tall
enough to be seen from a long way off. Give it: a pale `Toy_steel` deck, the raised
north curb with the four cooling towers, one penthouse box, a davit track, and the two
lower tier decks at each end with their own parapets. Two groups, not scatter. The three
roof levels per end are what makes the crown legible from above as well as from the side.

### 2.12 Scope

**In the GLB:** the tower shaft, both stepped end crowns, the facade pier/window rhythm,
the trim bands, the rooftop plant, and the low podium plinth under the footprint.

**Not in the GLB:** Embarcadero Center towers One–Three, the Hyatt Regency, the retail
spine and its promenade bridges, Sue Bierman Park, Clay/Drumm/Sacramento Streets,
neighbouring towers, trees, people, vehicles, plinths, cameras or lights.

### 2.13 Integration notes (for later, not this task)

- **Case B — new landmark.** There is no `4EmbarcaderoCenter` in
  `pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`, and no manifest entry.
  Integration needs a registry entry plus a tile re-bake.
- **id round trip:** `camelId()` in `app/src/assets.js` is
  `id.replace(/-([a-z])/g, upper)`; digits do not start a segment, so
  `4-embarcadero-center` → **`4EmbarcaderoCenter`**. `buildings.mjs` kebabs camel ids
  with `/([a-z0-9])([A-Z])/`, giving `4-embarcadero-center` back. Verify before relying
  on it — get this wrong and the procedural block stays, with no warning.
- **`exclude` radius:** the footprint's furthest vertex is **36.8 m** from the anchor;
  the nearest neighbouring building vertex is **61.6 m** (a 2.5 m structure at
  Clay/Drumm), then Embarcadero Center 3 at 64.0 m. Start from **`exclude: 45`** — but
  the DataSF footprint here is 3,142 m2 against OSM's 2,170 m2, so it reaches further
  than the OSM polygon does. Size the final value against the **real bake input**, from
  neighbour *vertices* and not centroids, and prove it from tile **penetration depth**
  rather than from a count.
- **Streaming decision:** at 179 m this is a skyline piece. Every other landmark over
  100 m in the manifest (`golden-gate-bridge`, `salesforce-tower`, `transamerica`,
  `555-california`) omits `loadRadius` and stays resident. **Omit `loadRadius`** here
  too and record the reason: the default rule would give 5,370 m, and a tower this tall
  popping in at that distance is more visible than the memory it saves. Check the shared
  landmark `BatchedMesh` headroom before committing — it has overflowed before.
- `targetHeightM` = 179.0 (plant crest), with the main parapet at 173.7. Both numbers go
  in `REPORT.md`.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bbox Z = 179.0 m exactly (so the loader scale lands at 1.0)
- [ ] Bbox X/Y consistent with a 63.5 x 37.3 m plan rotated 8.91 deg (expect ~68.5 x 46.6)
- [ ] Triangles at or under 20,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] No `Toy_roofd` anywhere
- [ ] `_Glow` on the crown band, the scattered lit windows, the lobby band and the beacon only
- [ ] Glow surfaces are inset faces, not a closed shell
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume
      for the union of solids; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night render + contact sheet (with a night tile) regenerated
      from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **`targetHeightM` 179.0 vs 173.7.** CTBUH's 173.7 m is the *architectural* top and
   explicitly excludes "functional-technical equipment", i.e. the cooling towers. The
   repo's convention for a plant crest is to ship the crest (see `300-brannan`:
   "25.2 m penthouse crest; 21.34 m parapet"), and AGENTS rule 5 wants the real thing in
   the scene. 179.05 m is DataSF LiDAR's max over the footprint, 5.35 m above the
   parapet, which is exactly a cooling-tower's worth. If the executing agent decides to
   ship 173.7 instead, it must move the plant *below* the parapet line — it must not
   simply relabel the same model.
2. **Crown step heights are estimated.** 135.0 m and 154.4 m are back-derived from a
   ~5-floor step counted off perspective photography (3.86 m/floor). The step *count*
   (three visible top levels per end) and the *strip widths* (2.4) are measured and
   solid; the *heights* are not. The SkyscraperPage orthographic diagrams
   (buildingID 2132) are the cheapest way to fix this — mine them first.
3. **A possible north–south roof level change.** Google's z20 satellite tile shows the
   bright cooling-tower deck occupying only ~19.5 m of the 37.3 m footprint depth, with a
   differently-toned band to its south. That is either (a) a genuine lower roof level on
   the south half, or (b) the raised mechanical curb reading as the deck. The
   near-orthographic north elevation shows a single flat roofline, which argues for (b),
   and this plan assumes (b). Check an aerial before building.
4. **The west end is inferred.** Every usable photograph found is of the east end. The
   plan geometry (2.4) proves the west end also steps, but with a much shallower
   projection and one chopped corner. Do not mirror the east end blindly.
5. **Cladding material conflict.** `buildingsdb.com` describes a glass-and-metal curtain
   wall; the photographs show punched windows in a solid precast grid, and SPUR and
   contemporary criticism describe the complex as concrete. The photographs win. If a
   primary source contradicts this, say so in `REPORT.md` and change the palette, not
   the geometry.
6. **The facade grid can alias.** 22 full-height pier/slot modules per long face is a
   lot of thin vertical geometry on a 174 m tower that will often be 100 px tall on
   screen. Check the aerial render at realistic distance before committing to 22; 16 may
   read better and costs less.
7. **Completion year 1982 is a 4–1 majority, not a certainty.** CTBUH says 1984. It does
   not affect the model.
