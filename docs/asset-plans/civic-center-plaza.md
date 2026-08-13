# Civic Center Plaza — SF-SIM asset plan

The 5-acre formal plaza east of City Hall: two dense bosques of pollarded London plane
trees flanking a central east–west court on the old Fulton Street axis, four geometric
lawn panels, eighteen historic flagpoles standing in two rows like a colonnade of masts,
two walled playgrounds on the Larkin side, and a garage kiosk at the McAllister end. It is
a **deck**, not a park: the north block sits on the roof of a three-storey 1960 parking
garage and Brooks Hall, and the whole composition is a Modernist re-cut (Douglas Baylis,
1956–58) of John Galen Howard's 1911 Beaux-Arts plaza.

This is the first plan in the set whose subject has **no building**. Its recognition does
not come from massing at all — it comes from a *ground pattern* and a *repeated vertical
rhythm*. The design brief is "the most legible civic carpet in the city", not "monument"
and not "park".

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/civic-center-plaza/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `civic-center-plaza` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4176170, 37.7794913` (oriented-bounding-box centre, measured) |
| Target height | **30.48 m** — the crest of the 100 ft United States flagpole in the south-west lawn. Historic flagpoles 15.24 m; tree crowns ~11 m; ground plate +0.30 m |
| Footprint | 177.88 m × 121.48 m oriented (heading 9.06°), 20,495 m² = 5.06 acres, measured from OSM way `284764947` |
| Axis-aligned XY bbox | ~146.6 m × 192.4 m — expected, the plaza is 9° off the world axes |
| Triangle cap | 18,000 |
| Category | `0` (Miscellaneous — the same slot Palace of Fine Arts, Coit Tower and Chase Center use) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Civic Center Plaza GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Civic Center Plaza**, San Francisco (the open
plaza block east of City Hall, bounded by McAllister, Larkin, Grove and Dr. Carlton B.
Goodlett Place), and deliver it as a downloadable, validated GLB.

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
7. `artifacts/palace-of-fine-arts/` — the closest reference implementation in *kind*: the
   only other landmark that is mostly hand-modelled **grounds** rather than a building,
   and the precedent for `clearTrees`
8. `artifacts/asian-art-museum/` — the closest reference in scale and neighbourhood; it is
   the building this plaza faces across Larkin Street, and the two must read as one world
9. `docs/asset-plans/civic-center-plaza.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- **The two bosques.** Six rows of severely pollarded London plane trees — three rows
  north of the central court, three south — 190 trees at roughly 3.2 m spacing, forming
  two dense flat-topped green slabs. This is the single strongest recognition cue and it
  must survive at thumbnail size. Pollarded planes are *not* lollipops: knuckled stubby
  trunks under a wide, flat, almost hedge-like crown.
- **The central east–west court on the Fulton axis** — a 13.2 m × 72.3 m fine-gravel
  panel dead-centre, aligned on City Hall's dome. Everything else is symmetric about it.
- **The eighteen historic flagpoles** of the Pavilion of American Flags: two rows of nine,
  48.5 m apart, 11.2 m pole-to-pole, 15.24 m tall, one flanking each side of the central
  court. Flags read as small chunky solid slabs, never as transparent cloth.
- **The 100 ft United States flagpole** in the south-west lawn — the tallest thing on site
  and the model's height datum.
- **Four geometric lawn panels** (two 36 × 36 m squares on the centre line, two long west
  panels) and the two east strip lawns — crisp rectangles with hard edges, mown, saturated
  green, sitting slightly proud of the paving.
- **The two Helen Diller playgrounds** on the Larkin (east) side, one north-east and one
  south-east, each a fenced 36 × 22 m pad with a strong colour accent — the only saturated
  non-green colour in the composition and therefore the plaza's storytelling anchor.
- **The orthogonal path grid**: four long east–west walks, a perimeter walk, and short
  cross links. Paving is the majority material on this site; it must be *designed*, not
  a blank slab.
- **The garage kiosk** at the McAllister end and the ramp mouth beside it — the reminder
  that the north block is a roof deck.

## Research Civic Center Plaza independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the WGS84
anchor, the plaza polygon, the 30.48 m flagpole height, and the real-world orientation,
and gather references covering:

- Aerial and satellite imagery, which is the primary reference for this subject — the
  camera looks down and this asset is almost entirely a ground plane
- The four street elevations (McAllister, Larkin, Grove, Dr. Carlton B. Goodlett) and what
  the plaza edge does at each: kerb, wall, steps, or ramp
- Ground-level views along the central court looking west toward City Hall — the money
  shot of the real place and the one composition the model must reproduce
- The pollarding cycle: these trees are cut back hard on a multi-year cycle and look very
  different immediately after pollarding (bare knuckled armature) than in full leaf.
  Model the **in-leaf** state.
- Day and night appearance. The plaza is lit by pole lights along the walks and the
  playgrounds are lit; City Hall's floodlighting is *not* part of this asset.
- The current condition of the site. SF has repeatedly proposed and partly executed
  changes to Civic Center Plaza since 2020 — confirm against recent imagery which
  elements are still present before modelling them.

Prefer the Cultural Landscape Foundation, SF Planning's Civic Center cultural-landscape
documentation, SF Recreation & Parks, the National Historic Landmark nomination (Civic
Center was NHL-designated 1987, NRHP-listed 1978), Andrea Cochran Landscape Architecture's
own documentation of the 2018 playgrounds, geolocated photography and aerial imagery.
Never rely on a single photograph, a single AI-generated image, or a single unsourced 3D
model. Separate verified facts from visual inference; if sources disagree, document the
disagreement and decide.

**Four source problems are already known and resolved in 2.1 and 2.15 — re-check them, do
not silently re-inherit the wrong value:**

1. **The address in the brief was 335 McAllister Street; the plaza's own address is 355
   McAllister Street** (the Civic Center Garage pay point). 335 geocodes to a bare address
   point on the north sidewalk. Same site, and 355 is the number to record.
2. **Wikipedia gives 4.53 acres, SF Rec & Park 4.53–5.38 acres; the OSM polygon measures
   5.06 acres.** The spread is real — it depends on whether the perimeter sidewalks and
   the Fulton right-of-way count. The OSM polygon is what the model is built on, because
   it is the polygon the pipeline's exclusion and landcover already use.
3. **OSM tags every one of the 190 trees `height=4.5`.** That is a bulk default, not a
   survey. Pollarded London planes in this plaza read at roughly 10–12 m. Do not build
   4.5 m trees; see 2.15.
4. **The 30.48 m flagpole height is an OSM tag, not a published figure.** It is a suspiciously
   round 100 ft. It is used as the height datum anyway because it is the only vertical the
   loader can scale from, and the manifest entry is therefore marked `"estimated": true`.

## Create a reference dossier

Write `artifacts/civic-center-plaza/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed reference
thumbnails is welcome if legally permissible — do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22, adapted: there is no
massing to rebuild, so the equivalent moves are **§12 Landscaping**, **§13 Roads and
Ground Plane** and **§17 Composition** — identify the recognition cues, strip nonessential
information, rebuild the ground pattern from a few confident shapes, exaggerate only the
signature features, deliberately design every surface visible from above (which here is
all of them), evaluate from the app's high three-quarter aerial camera, then simplify
again.

This is a **hero landmark** in the style bible's detail budget (§21) — it is one of the
five or six places in the city a visitor will fly to on purpose — but its detail must go
into *pattern and rhythm*, not into props. The temptation on an empty site is to fill it
with clutter. Resist it: the real plaza's power is its emptiness and its repetition.

Two style-bible rules carry unusual weight here:

- **§13, last sentence.** "Break up any large empty asphalt with trees, vehicles,
  markings, medians, planters, activity, small structures." Two thirds of this asset is
  paving. Give the paving a designed joint pattern, a change of tone between the gravel
  court and the concrete walks, and a kerb line you can read from the air.
- **§15 and §16.** This is a *public* place; a plaza with nobody in it reads as a car
  park. Place small clusters of people at three or four deliberate activity nodes — the
  playgrounds, the central court, the City Hall steps end — not an even sprinkle.

The finished asset must be immediately recognizable as this plaza, consistent with the
real place from all four sides and above, credible as landscape architecture, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic low-poly,
and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the plaza block only: the ground plate and its kerb, all paving, the six lawn
panels, the central gravel court, the six tree rows, the 18 historic flagpoles, the 16
Pride flagpoles at the McAllister and Grove entrances, the 100 ft US flagpole, the two
Helen Diller playgrounds with their fences and play structures, the garage kiosk and ramp
mouth, the small cafe and Pit Stop kiosks at the Grove/Larkin corner, and the plaza's own
benches, lamp poles, planters, litter bins and people clusters.

Do not include unrelated surrounding city geometry: City Hall, the Asian Art Museum, the
Main Library, Bill Graham Civic Auditorium, the Civic Center Courthouse, United Nations
Plaza, McAllister/Larkin/Grove/Goodlett roadways or their sidewalks, street trees outside
the plaza polygon, traffic signals, buses, terrain, cameras or lights. Temporary context
may appear in review renders but must not leak into the GLB.

The three-storey garage and Brooks Hall are *underground*. Do not model them. Their only
visible evidence is the kiosk, the ramp mouth, and the fact that the deck is raised.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ≈ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 18,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The plaza's long axis
runs **350.94° / 170.94°** (north–south, matching the Civic Center street grid) and its
cross axis **80.94° / 260.94°** (the Fulton/City Hall axis). Build directly in the
measured `(u, v)` plaza frame given in 2.3 and map to world X/Y once, rather than
modelling an axis-aligned rectangle and rotating it.

> **The grid leans 9.06° EAST of north, so the southward bearing is 170.94°
> (= 180 − 9.06), not 189.06° (= 180 + 9.06).** Those two are mirror images about
> north, and every bounding-box measurement reads the same 9.06° for both — the
> first build shipped 189.06° and put the plaza 18.12° out of true against its own
> block while the report still validated. Only a SIGNED angle catches it. If you
> change anything here, check the sign against the neighbours (City Hall 9.62°,
> Main Library 9.06°, Bill Graham 9.31°) rather than against a bbox.

**Height normalization:** the tallest geometry in the export (the US flagpole finial) must
land at exactly **30.48 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.
Because the height datum is a single thin pole and the asset is 178 m wide, a 1% error in
the pole scales the ground plane by 1.8 m. Drive the pole height from a named constant and
assert it in the validator.

**Flatness caution:** every surface in this asset is within 0.5 m of z=0 except the poles
and the play structures. Author the ground plate with real thickness (0.30 m to the paving
top, lawn tops 0.35 m) so the loader's merge does not produce coplanar z-fighting against
the baked landcover, which sits at +0.06 m above terrain.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/civic-center-plaza/build_civic_center_plaza.py` (deterministic build
script), `artifacts/civic-center-plaza/civic-center-plaza.blend`, and
`artifacts/civic-center-plaza/civic-center-plaza.glb`. The script must rebuild the model
reliably enough for future revision. The 190 tree positions and the plaza/lawn/path
polygons are measured data, not invention — commit them alongside the script under
`artifacts/civic-center-plaza/data/` with their OSM element ids, and have the script read
or embed them rather than eyeballing a grid. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`civic-center-plaza-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`civic-center-plaza-contact-sheet.png`, at least one high three-quarter aerial beauty
render `civic-center-plaza-aerial.png`, and a night render
`civic-center-plaza-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation.

Two subject-specific requirements:

- **The top view is the primary review image for this asset**, not a supporting one. It
  must clearly show the six tree rows, the central court, the four lawn panels, the two
  playgrounds and the path grid. Render it larger than the elevations.
- Add one extra render, `civic-center-plaza-axis.png`: a low three-quarter view looking
  **west along the central court**, the real plaza's signature composition. Frame it as if
  City Hall were at the end of it, even though City Hall is not in this asset.

Because the site is 178 m × 121 m and only 30 m tall, the elevations will be extremely
wide and mostly empty above the tree line. Frame them to the plan dimension and accept the
empty sky rather than zooming each view to fit.

## Validate the exported GLB

Re-import `civic-center-plaza.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count, camera
count, light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/civic-center-plaza/validation.json` and `artifacts/civic-center-plaza/REPORT.md`.

Three subject-specific validator checks, in addition to the standard ones:

1. **`max_z == 30.48 ± 0.01`** and the vertex achieving it belongs to the US flagpole.
2. **Tree count == 190** and every tree's `(x, y)` matches the committed data file to
   within 0.05 m.
3. **XY bbox ≈ 146.6 × 192.4 m.** That is the expected consequence of the 9.06° heading on
   a 177.9 × 121.5 m rectangle, not a scale error.

The normals test needs care on this asset: it is a union of many separate closed solids
(plate, kerbs, lawn slabs, poles, crowns), so **per-object signed volume is the
authoritative check**; the whole-model ray test will show a small residual and ≤ 0.15% is
the gate.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "civic-center-plaza",
  "file": "civic-center-plaza.glb",
  "anchor": [
    -122.4176170,
    37.7794913
  ],
  "targetHeightM": 30.48,
  "cat": 0,
  "name": "Civic Center Plaza",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate — the height datum is an OSM flagpole tag, not a
published figure. See 2.15.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/civic-center-plaza.md`.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Name | Civic Center Plaza | OSM way `284764947`, Wikidata `Q49478335` | verified |
| Address | 355 McAllister Street, San Francisco CA 94102 | OSM `addr:*` on the Civic Center Garage node `267294237` | verified |
| Boundaries | McAllister (N), Larkin (E), Grove (S), Dr. Carlton B. Goodlett Pl / former Polk (W) | Wikipedia; confirmed against OSM street ways | verified |
| Polygon area | 20,495 m² = 5.06 acres | shoelace over OSM way `284764947` | measured |
| Published area | 4.53 acres (Wikipedia); 4.53–5.38 acres (SF Rec & Park) | Wikipedia *Civic Center Plaza* | verified, conflicting — see 2.15 |
| Oriented bounding box | 177.88 m × 121.48 m, heading 9.06° | minimum-area OBB over the OSM ring | measured |
| OBB centre | lon −122.4176170, lat 37.7794913 | reprojected from the OBB | measured |
| Original plan | John Galen Howard, 1911; Beaux-Arts commission of Howard, Frederick Meyer and John Reid Jr., 1915 | Wikipedia; TCLF | verified |
| Modernist redesign | Douglas Baylis with Wurster, Bernardi & Emmons and SOM, 1956–58; rows of pollarded London plane **and olive** trees, olives removed 1998 | TCLF | verified |
| Underground garage | three storeys, completed 1960, 317 × 374 ft, 9 ft 3 in – 10 ft clear, Gould and Degenkolb | Wikipedia | verified |
| Brooks Hall | underground exhibition hall, completed 1958, connected to Bill Graham Civic Auditorium basement | Wikipedia; OSM node `368172530` | verified |
| Division | north and south blocks split by the former Fulton Street alignment | Wikipedia | verified |
| Central composition | "Two aisles of London plane trees flank an east–west pathway leading to City Hall, with formal plantings north and south of the tree aisle" | Wikipedia | verified |
| Trees | 190 mapped, 189 `Platanus × acerifolia` + 1 `Platanus × hispanica` (a synonym, so: 190 London planes) | OSM nodes inside the polygon | measured |
| Tree rows | six, at u = −18.0, −16.0, −12.5 (north bosque) and +14.5, +16.5, +20.0 (south bosque); ~3.2 m along-row spacing | histogram of the 190 tree nodes in the plaza frame | measured |
| Historic flagpoles | 18, height 15.24 m (50 ft), two rows of nine at u = ±24.2, 11.2 m apart | OSM `man_made=flagpole` nodes | measured (positions), OSM tag (height) |
| Pavilion of American Flags | 18 flags first raised on Flag Day, 14 June 1964; curated by Stanley Bergman on 18 poles that had stood bare | KQED; parkerhiggins.net | verified |
| US flagpole | 30.48 m (100 ft), at u +76.6, v +50.1 (south-west lawn) | OSM node `7797674733` | OSM tag — see 2.15 |
| Pride flagpoles | 16, two rows of eight at the McAllister (u −66.6) and Grove (u +68.9) entrances, ~4.9 m apart, height untagged | OSM nodes | measured (positions) |
| Playgrounds | Helen Diller Civic Center Playgrounds, NE and SE corners on the Larkin side, each ~36 × 22 m; north theme "spiderweb"-adjacent, opened 2018 | OSM ways `941235071` / `941235072`; TCLF; Wikipedia | verified |
| Playground designer | Andrea Cochran Landscape Architecture with The Trust for Public Land; $10 M renovation 2017–18; originals 1993 (N) and 1998 (S) | TCLF; Wikipedia | verified |
| Central court | fine-gravel recreation ground, 72.38 × 13.23 m, dead-centre on the plaza | OSM way `941346736` (`landuse=recreation_ground`, `surface=fine_gravel`) | measured |
| Lawns | six `landuse=grass` panels: 43.6 × 29.6 (NW), 36.7 × 36.2 (N centre), 11.7 × 7.6 (NE strip), 45.7 × 29.4 (SW), 36.2 × 36.0 (S centre), 36.7 × 12.2 (S strip) | OSM ways `128534081/93/68/94/79/62` | measured |
| Garage kiosk | 12.81 × 6.63 m, single storey, built 1958, "pay point for garage parking" | OSM way `941716707` | verified |
| Historic status | Civic Center NRHP-listed 1978, National Historic Landmark 1987 | TCLF | verified |

### 2.2 Sources

- OpenStreetMap, Overpass API — plaza polygon (way `284764947`, relation `1735770`), the
  190 tree nodes, 35 flagpole nodes, six grass polygons, the gravel court, both
  playgrounds, the kiosk and the full footway network. Everything marked *measured* above
  was computed from this pull. The raw pull and the derived plaza-frame coordinates are
  reproduced under `artifacts/civic-center-plaza/data/`.
- Wikipedia, *Civic Center Plaza* — acreage, boundaries, the Fulton division, the two
  tree aisles, Brooks Hall, the garage's dimensions and architects, playground history.
- The Cultural Landscape Foundation, *Civic Center Plaza — San Francisco* — the 1911/1915
  Beaux-Arts plan, Thomas Church's 1936 War Memorial Court, Douglas Baylis's 1956–58
  Modernist redesign and its pollarded plane/olive planting, Halprin's 1975 UN Plaza, the
  2018 Helen Diller playgrounds, NRHP/NHL status.
- KQED, *Why is There a Texas Flag in Front of City Hall?* and its accompanying
  *Civic Center Plaza Flagpoles Historical Background* — the 1964 Pavilion of American
  Flags, Stanley Bergman, and the fact that the poles predate the flags.
- parkerhiggins.net, *The 18 flags of San Francisco's Civic Center Plaza* — the individual
  flag identities, which match the OSM `flag:name` tags one for one.
- SF Planning, *Civic Center Cultural Landscape Inventory — Thomas Dolliver Church* —
  Church's role, for the record that he did **not** design this plaza.
- The repo's own committed tiles (`app/public/tiles/buildings/19_13.bin`, `19_14.bin`) —
  the exclusion-radius measurements in 2.13. This is the authoritative input, not OSM.

### 2.3 Orientation and placement

The plaza sits on the Civic Center grid, rotated 9.06° from north. All geometry is authored
in a local `(u, v)` frame and mapped to world once:

```
u  = along the long (north–south) axis, POSITIVE TOWARD THE SOUTH  (Grove Street)
     bearing 170.94 deg true  — NOT 189.06; see the orientation note in Part 1
v  = along the short (east–west) axis,  POSITIVE TOWARD THE WEST   (City Hall)
     bearing 260.94 deg true
u ∈ [−88.9, +88.9]   v ∈ [−60.7, +60.7]
world_x =  u·sin(9.06°) − v·cos(9.06°)
world_y = −u·cos(9.06°) − v·sin(9.06°)      (Blender +Y = north)
```

The origin is the OBB centre, `lon −122.4176170, lat 37.7794913`. Model Z = 0 is the
surrounding sidewalk level; the plaza deck top is +0.30 m.

Measured plaza ring, in `(u, v)` — note the chamfered south-west and north-west corners
and the notch at `u ≈ −80` where the garage ramp cuts in:

```
(88.9, 54.3) (88.9,−60.7) (−14.9,−60.1) (−29.9,−52.3) (−36.8,−51.1) (−70.6,−51.4)
(−70.6,−60.7) (−80.9,−60.7) (−85.6,−55.8) (−88.8,−52.5) (−88.9,−26.2) (−79.5,−26.2)
(−79.8, 17.7) (−80.4, 21.4) (−81.6, 24.9) (−85.1, 31.7) (−87.0, 35.8) (−87.8, 40.1)
(−87.8, 54.4) (−80.5, 60.7) (82.4, 60.7) (88.9, 54.3)
```

Measured element layout, all in `(u, v)`:

| Element | Extent |
|---|---|
| Perimeter walk | north u ≈ −78, south u ≈ +83.8, west v ≈ +55.1, east v ≈ −48.9 |
| East–west allée walks | u = −20.9, −9.8, +10.9, +21.9, each running v −49 → +55 |
| North–south cross links | v = −19.4 and +20.1 (north half), v = −19.4 and +21.1 (south half) |
| Central gravel court | u ∈ [−6.0, +7.2], v ∈ [−35.5, +36.8] |
| Lawn NW | u ∈ [−77.0, −33.5], v ∈ [+23.8, +53.4] |
| Lawn N centre | u ∈ [−64.4, −27.7], v ∈ [−17.4, +18.8] |
| Lawn NE strip | u ∈ [−77.2, −69.4], v ∈ [−46.8, −34.9] |
| Lawn SW | u ∈ [+34.4, +80.1], v ∈ [+23.7, +53.2] |
| Lawn S centre | u ∈ [+28.6, +64.7], v ∈ [−17.5, +18.7] |
| Lawn S strip | u ∈ [+67.7, +79.9], v ∈ [−17.7, +18.9] |
| Playground N | u ∈ [−64.7, −21.1], v ∈ [−43.7, −21.1] |
| Playground S | u ∈ [+28.5, +64.8], v ∈ [−43.8, −21.2] |
| Garage kiosk | u ∈ [−74.9, −68.3], v ∈ [−5.6, +7.2] |
| Historic flagpoles | u = −24.2 and +24.2; nine each at v = −43, −32, −21, −10, +1, +12, +23, +34, +45 |
| Pride flagpoles | u = −66.6 and +68.9; eight each at v = −16 → +18, step 4.9 |
| US flagpole (100 ft) | u = +76.6, v = +50.1 |

The 190 tree positions are listed in `artifacts/civic-center-plaza/data/trees_uv.json`.

Note that the OSM tree rows are *not* perfectly straight — they carry real survey jitter of
a few decimetres. Keep it. A perfectly ruled grid is the single easiest way to make this
asset look procedural rather than surveyed.

### 2.4 What each side shows

- **North (McAllister Street).** The garage kiosk, the ramp mouth notch, the north row of
  eight Pride flagpoles, and the NW lawn's long edge. The busiest and least symmetric
  edge — this is the service end of the plaza.
- **East (Larkin Street).** The two playgrounds, presented end-on as two fenced colour
  blocks with the NE and S strip lawns between them. The most colourful edge, and the one
  the Asian Art Museum and the Main Library look at.
- **South (Grove Street).** The mirror of the north: eight Pride poles, the SW lawn edge,
  and the 100 ft US flagpole rising behind them. The tallest silhouette.
- **West (Dr. Carlton B. Goodlett Place).** The ceremonial front. The central court runs
  straight out of this edge at City Hall's dome; the two big west lawns flank it. Read
  from City Hall's steps, the whole plaza is a symmetric carpet — this is the elevation to
  get right.
- **Above.** The composition: two dark-green bosque slabs, four bright lawn rectangles, a
  pale gravel bar across the middle, two colour-accented playground pads on the east, and
  the flagpole rows reading as two dotted lines. If the top view does not read as a
  deliberate pattern, the asset has failed.

### 2.5 Recognition cues (ranked)

1. **Two dense bosques of flat-topped pollarded planes** flanking a central bar. Nothing
   else in San Francisco looks like this from the air.
2. **The east–west axis pointing at City Hall's dome.**
3. **The double row of flagpoles** — a colonnade of masts, unmistakable at any distance.
4. **The four crisp geometric lawn panels** and the symmetry about the central axis.
5. **The two playgrounds' colour** on the Larkin side, the only saturated accent.

### 2.6 Miniature translation

Style bible §26: "deliberate compression of reality".

| Reality | Miniature |
|---|---|
| 190 individually surveyed planes with real canopy variation | 190 trees, real positions kept, but **two crown sizes only** and one silhouette — a stubby knuckled trunk under a wide flat drum |
| Pollarded canopy, ragged, ~10–12 m | a clean drum crown, semantically enlarged to read as a continuous green slab from the air; slight per-tree scale jitter driven by a hash of the tree index, never random |
| Concrete paving with expansion joints, patched and stained | two paving tones — warm pale concrete for the walks, a lighter sand tone for the gravel court — with a broad joint grid scored at ~6 m, and **no** weathering (§6) |
| Lawn with real edge wear | hard-edged slabs 0.05 m proud of the paving, saturated green (§7 allows vegetation to be unusually vivid) |
| 35 flagpoles with cloth flags | chunky tapered poles with a gold finial and a small solid slab flag, angled consistently as if in one breeze — flags are **opaque geometry**, never alpha |
| Two densely equipped playgrounds | two fenced pads, each with one oversized signature structure and two small ones, in one saturated accent colour per pad (§9 semantic scale) |
| A working city plaza | four deliberate activity nodes: the two playgrounds, the central court, and the west end facing City Hall |
| Garage ramp, vents, stair heads, utility boxes | the kiosk, the ramp mouth, and exactly one vent block. Everything else deleted. |

The plaza is 178 m across in a city where the loader's shared batch is a shared budget.
Every simplification above is also a triangle saved; take them all.

### 2.7 Massing recipe

There is no massing. The recipe is a stack of plates plus two families of repeated objects.

1. **Deck plate.** Extrude the measured plaza ring to 0.30 m, with a 0.06 m chamfer on the
   top outer edge to read as a kerb. This is the single largest object and the thing every
   other element sits on.
2. **Paving inlays.** The four allée walks, the perimeter walk and the cross links as
   flat inlays at +0.30 m in the walk tone; the rest of the plate in the field tone. Score
   a 6 m joint grid into the field as shallow 0.02 m recesses — cheap, and it is what
   stops the plate reading as a blank slab from above.
3. **Gravel court.** A 13.2 × 72.3 m slab at +0.31 m in sand, inset 0.05 m from the
   surrounding paving so its edge catches a contact shadow.
4. **Lawn slabs.** Six extruded rectangles to +0.35 m, saturated green, with a 0.04 m
   chamfer. Two of them (NW, SW) have the notched corners recorded in 2.3 — keep the
   notches, they are what makes the panels look surveyed.
5. **Bosques.** 190 instances of one tree object at the measured `(u, v)`: a six-sided
   tapered trunk 0.55 m across rising to 3.2 m, then a ten-sided drum crown 5.6 m across
   and 2.2 m deep with a 0.25 m chamfer top and bottom, crown centre at ~9.5 m, crest at
   ~11 m. Per-tree scale jitter ±6% from `hash01(index)`.
6. **Flagpole family.** One pole object at 15.24 m (six-sided, 0.22 m tapering to 0.14 m,
   gold finial, 0.9 m octagonal base block) instanced 18 times at the measured positions,
   with a 2.6 × 1.5 m solid flag slab near the top; the same object scaled to 30.48 m once
   for the US pole with a 4.4 × 2.6 m flag; a shorter 9 m variant for the 16 Pride poles.
7. **Playground pads.** Two 36 × 22 m recessed pads at +0.28 m in a soft accent tone, a
   0.9 m railing fence around each (a chamfered rail bar on posts at 3 m — do **not** model
   pickets), and per pad one oversized signature structure plus two small ones.
8. **Kiosks.** Garage kiosk 12.8 × 6.6 × 3.4 m with a flat overhanging roof; the ramp mouth
   as a 9 × 6 m recess with a low retaining wall; the Grove-corner cafe and the Pit Stop as
   two small boxes.
9. **Furniture and life.** Lamp poles at the walk intersections, benches lining the central
   court, planters at the west end, and four people clusters. Budget-capped; if the
   triangle count runs hot, this is the section that gets cut, in this order: people,
   planters, benches, lamps.

### 2.8 Materials and palette

All from the project palette in `.agents/skills/sf-asset-check/SKILL.md`.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `d9d2c2` | deck plate, field paving, kerb |
| `Toy_cream` | `f2ede3` | allée and perimeter walks (a half-tone lighter than the field, so the grid reads) |
| `Toy_sand` | `ece4d4` | the gravel court |
| `Toy_mint` | `8fd0a8` | lawn slabs |
| `Toy_verdigris` | `9fb8a8` | tree crowns — the darker, greyer green that separates the bosques from the lawns from the air |
| `Toy_rust` | `a86444` | tree trunks |
| `Toy_steel` | `9aa0a6` | flagpoles, railings, lamp poles |
| `Toy_gold` | `caa64a` | pole finials |
| `Toy_red` / `Toy_navy` / `Toy_white` | `c4453c` / `2c4a70` / `f7f4ec` | the flags — three flat slabs, no attempt at devices |
| `Toy_coral` | `e8735a` | playground N accent |
| `Toy_teal` | `3fa8a0` | playground S accent |
| `Toy_trim` | `f3efe6` | kiosk walls |
| `Toy_roofd` | `45454a` | kiosk roofs, bench slats, litter bins |
| `Toy_ink` | `3a3530` | joint recesses, contact-shadow edges |

**Night state** (`_Glow` variants, required by stage 2 of the pipeline):

- `Toy_cream_Glow` — a warm pool at the foot of each walk lamp. The hero glow: the four
  allée walks and the perimeter walk light up as a luminous grid, which is exactly what the
  real plaza does and reads beautifully from the aerial camera.
- `Toy_gold_Glow` — the US flagpole is floodlit (`lit=yes` on the OSM node); a small glow
  band at its top only.
- `Toy_coral_Glow` / `Toy_teal_Glow` — a restrained accent on each playground pad.

Nothing else glows. The lawns and the bosques go dark, and that contrast is the point: at
night the plaza should read as a lit grid drawn on a dark field. Every `_Glow` surface is a
thin shell proud of its opaque parent, never the parent itself, and its day colour matches
its non-glow neighbour (the app renders the glow layer at ~12% alpha by day).

### 2.9 Top surface

For every other asset in this set §2.9 is "the roof". Here the top surface *is* the asset,
so the whole of 2.7 is the answer. The one rule worth restating: judged from the app's
high three-quarter camera at 400–800 m, the plaza must resolve into six shapes — two green
slabs, four bright rectangles, one pale bar, two colour pads. If any of those six merges
into its neighbour, increase the tonal separation before adding any detail.

### 2.10 Scope

**In:** the plaza polygon and everything standing on it, as listed in Part 1.

**Out:** City Hall, the Asian Art Museum, the Main Library, Bill Graham Civic Auditorium,
the Civic Center Courthouse, UN Plaza, all four bounding roadways and their sidewalks and
street trees, terrain, the underground garage and Brooks Hall, cameras, lights.

**Deliberately omitted despite being on site:** the `Double L Excentric Gyratory` (George
Rickey, 1982) — it measures outside the plaza polygon, on the Fulton/Larkin side, and
belongs to UN Plaza rather than here; the Bay Wheels dock; individual waste baskets,
hydrants and street cabinets; the drinking fountain; the elevator heads at the McAllister
entrance beyond the one kiosk.

### 2.11 Triangle budget

| Group | Count | Tris each | Tris |
|---|---:|---:|---:|
| Deck plate + kerb + joint grid | 1 | — | 900 |
| Paving inlays (walks, cross links) | 12 | ~40 | 480 |
| Gravel court | 1 | 60 | 60 |
| Lawn slabs | 6 | ~90 | 540 |
| Trees (trunk 20 + crown 28) | 190 | 48 | 9,120 |
| Historic flagpoles + flags | 18 | 36 | 648 |
| Pride flagpoles + flags | 16 | 36 | 576 |
| US flagpole | 1 | 120 | 120 |
| Playground pads, fences, structures | 2 | ~700 | 1,400 |
| Kiosks, ramp mouth, vent | 4 | ~120 | 480 |
| Lamp poles | 14 | 40 | 560 |
| Benches, planters, bins | ~30 | 30 | 900 |
| People clusters | 4 | ~90 | 360 |
| | | **total** | **≈ 16,100** |

Cap 18,000; hard gate 30,000 (PERF-PLAN #9). The trees are 57% of the budget and are the
only place worth optimizing: if the count runs over, drop the crown from ten sides to
eight (−1,520) before touching anything else. Do **not** reduce the tree count — 190 is
measured data and the density is the recognition cue.

### 2.12 Draft manifest entry

```json
{
  "id": "civic-center-plaza",
  "file": "civic-center-plaza.glb",
  "anchor": [-122.4176170, 37.7794913],
  "targetHeightM": 30.48,
  "cat": 0,
  "name": "Civic Center Plaza",
  "estimated": true,
  "dims": [146.6, 192.4, 30.48],
  "tris": 16100,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule `max(2500, 30.48 × 30 = 914) = 2500`. The rule's
usual caveat — "beyond the radius the site is empty because the baked buildings were carved
out" — is unusually gentle here: outside the radius this site is an empty park in the baked
city, which is roughly what it should look like. 2,500 m is comfortable.

`"estimated": true` because the height datum is an OSM tag (see 2.15), not a published
dimension. Everything else in the entry is measured.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** There is no `civicCenterPlaza` in `pipeline/lib/landmarks.mjs`
or `app/src/landmarks.js`, so integration needs a registry entry and a tile re-bake.

**Exclusion radius: 95 m, measured against the committed bake input** (`app/public/tiles/
buildings/19_13.bin` and `19_14.bin`), per the method that `505VanNess` established —
nearest *vertex*, not centroid:

| Footprint | Nearest vertex from the anchor | Area | Baked top |
|---|---:|---:|---:|
| garage kiosk | 67.8 m | 88 m² | 23.4 m |
| Grove-corner cafe | 74.2 m | 93 m² | 22.0 m |
| Pit Stop / small structure | 83.5 m | 10 m² | 22.5 m |
| **first neighbour to protect** | **109.9 m** | 6,165 m² | 62.0 m |

The window is 83.5 < r < 109.9 — unusually wide. **95 m** sits in the middle, clears all
three plaza structures with 11.5 m of margin, and spares the neighbour by 14.9 m. Note
what those three baked footprints are: single-storey kiosks that the procedural builder
extruded to 22–23 m. Three phantom towers stand in the plaza in the current build; the
exclusion is what removes them, and **the asset cannot be judged before the re-bake** —
this is exactly the case the batch-mode note in `ADDRESS-TO-ASSET.md` warns about.

**Tree scatter.** The plaza is `leisure=park`, so the landcover scatter drops procedural
trees across it, which would grow through the modelled bosques. The `clearTrees` flag
(Palace of Fine Arts, Letterman, 1008 General Kennedy) is the right mechanism, **but it
reuses `exclude` as its radius**, and a 95 m tree-clear circle would also delete real
street trees on Larkin, McAllister and Grove — a visible regression around a hero landmark.

The recommendation is therefore a small, additive pipeline change: an optional
`clearTreesRadius` on the landmark record, defaulting to `exclude`, read by
`pipeline/lib/treeblockers.mjs` where it currently does `r: l.exclude`. Set it to **60 m**:
the modelled trees all sit within r = 54 m, so 60 m clears exactly the ground the asset
covers, stays inside the plaza's 60.7 m half-width, and leaves the procedural scatter
intact at the plaza's north and south ends where the asset models no trees. Whoever runs
integration should confirm that reading against the re-bake rather than taking it on trust.

Draft registry entry:

```js
{
  // A 5-acre plaza, not a building: `exclude` has to clear the three kiosk
  // footprints the procedural builder extrudes to 22-23 m inside the plaza
  // (nearest vertices 67.8 / 74.2 / 83.5 m) without touching the first real
  // neighbour at 109.9 m. Measured against buildings/19_13.bin and 19_14.bin.
  id: 'civicCenterPlaza',
  name: 'Civic Center Plaza',
  lon: -122.4176170,
  lat: 37.7794913,
  height: 30.48,
  exclude: 95,
  clearTrees: true,
  clearTreesRadius: 60,   // needs the treeblockers.mjs change described above
  camera: { distance: 620, yaw: 90, pitch: 30 },
}
```

The camera preset deliberately looks **west along the central court** (yaw 90) so the
fly-to lands on the plaza's own axis with City Hall filling the far end — the one
composition that explains what this place is.

**Batch mode applies.** A Case B re-bake rewrites ~600 generated files; run the bake, do
the full QA on it, then `git checkout -- app/public/tiles api/_data` and commit source
only, per `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

### 2.14 Validation checklist

- [ ] Binary GLB, real metres, applied transforms, no negative scales
- [ ] `min_z ≈ 0`, XY centre within 0.5 m of the origin
- [ ] `max_z == 30.48 ± 0.01`, achieved by the US flagpole finial
- [ ] XY bbox ≈ 146.6 × 192.4 m (the 9.06° heading, not a scale error)
- [ ] ≤ 18,000 triangles; ≤ 500 KB compressed
- [ ] Exactly 190 trees, positions matching `data/trees_uv.json` within 0.05 m
- [ ] 18 historic poles at 15.24 m, 16 Pride poles, 1 pole at 30.48 m
- [ ] All materials `Toy_*` and in the palette; no textures, no transparency, no `Toy_body`
- [ ] `_Glow` materials present, all thin shells proud of an opaque parent, day colours
      matching their non-glow neighbours
- [ ] No cameras, lights, animations, armatures, constraints, or foreign geometry
- [ ] Per-object signed-volume normals test clean; whole-model ray residual ≤ 0.15%
- [ ] Top view resolves into the six shapes of §2.9
- [ ] Night render shows a lit walk grid on a dark field, not a uniformly glowing slab

### 2.15 Open questions and risks

1. **The height datum is a single OSM tag on a thin pole.** `targetHeightM = 30.48` comes
   from `height=30.48` on node `7797674733`. It is a round 100 ft, which is plausible for a
   civic flagpole and is exactly the kind of number that gets entered by hand. Because the
   loader scales by `targetHeightM / measuredHeight`, a wrong pole height rescales the
   *entire 178 m plaza*. Mitigations: drive the pole from a named constant, assert it in
   the validator, and mark the manifest entry `"estimated": true`. If better evidence
   emerges, changing the constant and re-exporting is a two-minute job — changing it after
   the plaza has been visually approved at the wrong scale is not.
2. **Tree heights are a bulk OSM default.** All 190 nodes carry `height=4.5`. That is not
   a survey and 4.5 m would make the bosques disappear at aerial distance. The plan builds
   ~11 m crests, inferred from pollarded London planes of this age and from photography.
   This is the largest *visual* assumption in the dossier and it should be re-checked
   against recent imagery before the build, not after.
3. **Acreage disagrees across sources** (4.53 / 4.53–5.38 / 5.06 measured). The model is
   built on the OSM polygon because that is the polygon the pipeline's landcover and
   exclusion already use, so the model and the baked city agree with each other even if
   they both differ slightly from the Rec & Park figure. Recorded, not resolved.
4. **The site changes.** SF has repeatedly proposed and partly executed changes to Civic
   Center Plaza since 2020, and the OSM data has mixed vintages (the playgrounds are 2018;
   several nodes carry `check_date` values in 2022 and 2026). Confirm against recent
   imagery which elements are still present before modelling them, especially the Pride
   flagpoles, which are the newest and least-documented feature here.
5. **`docs/asset-plans/README.md` says parks are planned in `docs/plans/parks/`, not
   here.** That rule exists because a park is landcover + scatter + a few hero assets, not
   one GLB. Civic Center Plaza is treated as a landmark instead because it is a designed
   hardscape with a fixed, surveyed layout and no natural component — the same argument
   that made the Palace of Fine Arts grounds a landmark. If the parks pipeline later grows
   the ability to bake a designed plaza, this asset is a candidate to migrate.
6. **The `clearTreesRadius` field does not exist yet.** 2.13 proposes it. If the integrator
   declines the pipeline change, the fallback is `clearTrees: true` at the full 95 m and
   accepting the loss of one block of street trees on each side — which should be a
   deliberate, recorded decision, not a silent one.
7. **The flags are political objects.** The 18 historic flags have been edited by the city
   in recent years (the "Appeal to Heaven" flag was quietly removed in 2024). The model
   deliberately renders flags as abstract three-colour slabs with no devices, which sidesteps
   the question entirely and is also the correct call under style-bible §26. Do not model
   individual flag designs.
