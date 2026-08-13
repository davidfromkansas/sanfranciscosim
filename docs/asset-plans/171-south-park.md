# 171 South Park Street — SF-SIM asset plan

A ca. 1910 Edwardian flats building at the south corner of South Park's oval — and the
only wedge in the district. Where the park's curve cuts across the 45° SoMa grid, this lot
is left as a flatiron: a broad, three-facet front bowing along the oval, narrowing over
20 m to a 5.4 m tail behind. From the app's camera, which looks down, **the plan shape is
the building**. It is a contributor to the South Park Historic District and, per the
district record, the southern corner where the district boundary turns.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/171-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `171-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3945219, 37.7809000` |
| Target height | **12.6 m** to the roof penthouse; front cornice crest ~11.9 m; roof deck 11.41 m |
| Footprint | wedge, 131.2 m2 measured; 11.36 m faceted park front narrowing to a 5.44 m tail, ~20.6 m long |
| Triangle cap | 8,000 |
| Category | `2` (apartments) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 171 South Park Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 171 South Park Street in San Francisco and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/380-brannan/` — the closest reference implementation in scale, district and
   character (small SoMa block one street away, 45° heading, designed flat roof, night
   state). `artifacts/painted-ladies/` is the reference for tinted residential facades.
8. `docs/asset-plans/171-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **wedge plan**: a broad park-facing front tapering back to a narrow tail. This is
  the single strongest cue and the camera sees it constantly. Build on the measured
  polygon in 2.3 — never on an axis-aligned box.
- The **three-facet front** bowing along the oval (outward bearings 321.3°, 348.2°,
  1.1°) — the facets must stay readable as facets, not be smoothed into a curve or
  flattened into one plane.
- An Edwardian-era residential flats building: flat roof, **decorative cornice**,
  **angled bay windows**, painted wood facade, raised ground level with a stoop.
- Four levels read from the street (see the storey-count conflict below).
- A designed flat roof: skylights, the elevator/stair penthouse, the rear deck.

## Research 171 South Park Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- **The front elevation — this is the dossier's weakest area and your first job.**
  No street-level photograph of this building was obtainable during planning (no
  KartaView/Mapillary coverage inside the oval; listing sites blocked). Everything in
  2.4 about the front is typology-derived, not observed. Open Google Street View on
  South Park at the south end of the oval and settle, at minimum: flat front vs
  angled bay windows and how many bays; the number of levels visible; the paint
  colours; whether there is a garage door; where the entry sits among the three facets.
- Aerial and roof/top views (skylight layout, penthouse, rear deck)
- The two flanks — both are party walls in reality, but the app's camera sees them,
  so establish what is actually finished there
- Day and night appearance

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**Three source conflicts are already known and analysed in 2.1 and 2.15 — re-check them,
do not silently re-inherit the wrong value:** the storey count is recorded as **3** in
most permits and **4** in the 2005–2008 elevator/deck permits (the dossier reads this as
three flats over a raised ground level and asks you to confirm from the street); the
construction date is 1908 in the Assessor roll and **ca. 1910** in the historic district
record; and OSM `height=11` describes the roof deck, not the crest — the LiDAR maximum is
12.62 m.

## Create a reference dossier

Write `artifacts/171-south-park/REFERENCE.md` containing: source links and what each
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

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly
two identity cues carried hard — the wedge plan and the faceted bay-window front. Resist
adding hero-tier ornament. `AGENTS.md`'s SF exception applies: painted residential rows
keep their tinted facades, so this building may carry more facade colour than a
commercial neighbour would.

The finished asset must be immediately recognizable as 171 South Park Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single flats building: body on the measured wedge footprint, all four
elevations, cornice, bay windows, roof deck and roof furniture, rear deck.

Do not include unrelated surrounding city geometry: South Park street or the oval park,
165–167 or 181 South Park (both share party walls with it), Varney Place, street trees,
the sidewalk, parked cars, people, plinths, cameras or lights. Temporary context may
appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 8,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The park front faces
**NNW, average outward bearing 343.5°**, so the contract's "front faces −Y" rule cannot be
honoured literally; real-world orientation wins (AGENTS rule 5) and the deviation goes in
`REPORT.md`. Build directly on the measured footprint polygon in 2.3.

**Height normalization:** the tallest geometry in the export (the roof penthouse) must
land at exactly **12.6 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/171-south-park/build_171_south_park.py` (deterministic build script),
`artifacts/171-south-park/171-south-park.blend`, and
`artifacts/171-south-park/171-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`171-south-park-top.png`, `171-south-park-north.png`, `171-south-park-east.png`,
`171-south-park-south.png`, `171-south-park-west.png`, plus
`171-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`171-south-park-aerial.png`, and a night render `171-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the wedge plan, the cornice ring,
skylights, penthouse and rear deck; the aerial view uses the style bible's camera
assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral warm
background, minimal depth of field, and every image must depict the same exported model.

**The top view is the acceptance render for this asset.** If the wedge does not read
instantly from directly above, the model has failed its main job.

## Validate the exported GLB

Re-import `171-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/171-south-park/validation.json` and
`artifacts/171-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **18.5 x 17.5 m** even though
the building is a 20.6 m long wedge only 11.4 m across at its widest — that is the
expected consequence of a ~45° real-world heading, not a scale error. The XY centre of
the bounding box will **not** be (0, 0): the origin is the footprint's area centroid, and
on a wedge that sits about 1.5 m from the bbox centre. Keep the area centroid; do not
"fix" it by recentring on the bounding box, or the building will land off its own lot.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "171-south-park",
  "file": "171-south-park.glb",
  "anchor": [
    -122.3945219,
    37.7809
  ],
  "targetHeightM": 12.6,
  "cat": 2,
  "name": "171 South Park Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/171-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 13 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on. This dossier is unusually thin on **observed** facade detail; see
2.15 before treating any of 2.4's front-elevation description as fact.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **ca. 1910** | SF Planning South Park Historic District Record (DPR 523D, 2009) — see the 1908 conflict below |
| Assessor build year | 1908 | SF Assessor secured roll, block 3775 lots 137/138/139 (consistent 2007-2025) |
| Type | Residential flats, wood frame | DPR 523D: listed under "Flats", "Residential buildings … are primarily wood frame in construction and are clad in wood or stucco siding" |
| Historic status | **Contributor** to the South Park Historic District, CHRSC **5D3** | DPR 523D contributor table (`3775137-139 171 SOUTH PARK HP3. Multiple Family Property ca. 1910 5D3`) |
| District position | The district boundary turns at this lot: it runs "down Varney Place to the south corner of 171 South Park Street (3775-137 to -139)", then northwest along its southwest lot line | DPR 523D, D4 Boundary Description |
| Units | **3 condominium units** — 1,064 / 1,102 / 1,102 sq ft, 2 bed each | SF Assessor roll 2025, lots 137 / 138 / 139, `property_location` `0171 SOUTH PARK 0001/0002/0003` |
| Storeys | **3** in most permits, **4** in the 2005–2008 permits | SF Building Permits; read here as 3 flats over a raised ground level — see 2.15 |
| Use | Apartments / condominium (`SRES`, class `Z`) | SF Assessor roll |
| Block / lots | 3775 / 137, 138, 139 | SF Assessor, DataSF footprint `mblr = SF3775137` |
| Footprint | **131.2 m2** (OSM), **132.2 m2** (DataSF) — a wedge, not a rectangle | OSM way 124889458 + DataSF `ynuv-fyni` SF3775137, both reprojected — **measured**, and they agree within 0.8% |
| Front width | **11.36 m** in three facets (3.64 + 3.83 + 3.89 m) | measured from the footprint polygon |
| Tail width | **5.44 m** | measured |
| Overall length | ~20.6 m front-to-tail | measured (minimum-area OBB 20.58 x 9.50 m) |
| Roof deck height | **11.41 m** above ground | DataSF LiDAR `hgt_median_m` — **measured** |
| Maximum feature height | **12.62 m** above ground | DataSF LiDAR `hgt_maxcm` — **measured** |
| OSM height tag | 11 m | OSM way 124889458, `source=Bing` — matches the roof deck, **not** the crest |
| Front cornice crest | ~11.9 m | *inferred*, roof deck + a typical Edwardian cornice |
| Ground elevation | 7.29 m (NAVD88) | DataSF LiDAR `gnd_min_m` — the app's terrain handles this, not the asset |
| Front heading | park front faces NNW, facet bearings 321.3° / 348.2° / 1.1°, average **343.5°** | measured from the footprint polygon |
| Elevator | Installed 2005–2009, "replacement (n) elevator to service all floors" | SF permit 200509062106 and its 2007–2009 revisions/finals |
| Rear deck | New rear deck, same 2005 permit; steel-framed stair alternate 2008 | SF permits |
| Windows / paint | 2012: wood single-pane windows replaced with wood double-pane, wood window trims replaced, **exterior facade painted** | SF permit, 2012-01-06 |
| Roof | Re-roofed March 2026, no structural sheathing work | SF permit, 2026-03-17 |
| Party walls | 165–167 South Park (NE, 1908, flats, contributor) and 181 South Park (SW/S) both touch this footprint — zero gap | OSM + DataSF geometry, **measured** |

### 2.2 Sources

- https://www.openstreetmap.org/way/124889458 — footprint, address `171 South Park`, `height=11`, `source=Bing`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived), record `SF3775137` — authoritative footprint polygon and the 11.41 m / 12.62 m / 7.29 m heights. **This is also the bake's primary footprint source**, which is what makes 2.13's exclusion arithmetic binding.
- https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf — SF Planning, *South Park Historic District*, DPR 523D District Record, Christina Dikas / Page & Turnbull, 30 June 2009. Establishes: contributor status and CHRSC 5D3; ca. 1910; the flats typology and its Edwardian-era vocabulary; the district boundary turning at this lot.
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1908, block/lot, three condo units and their areas
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — storey counts, the elevator and rear deck, the 2012 window/paint job, the 2026 re-roof
- Google Maps satellite (Vexcel/Airbus imagery, 2026) — flat light-tan roof (consistent with the March 2026 re-roof), a row of roughly four small skylights toward the front third, a further pair mid-roof, a pale mechanical/penthouse box, and a deck structure toward the tail
- Nominatim / OSM API `map.json` for the block — the neighbour footprints, the oval road and the sidewalk geometry used for the orientation and party-wall findings

**Not obtained:** any street-level photograph of the building. KartaView's nearest coverage
is 45+ m away on 3rd Street with the building out of frame; Commons has no geolocated
image within 150 m; Redfin/Movoto listing pages are bot-blocked and their unit copy carries
no building description; Google Street View would not render in the available browser
(no WebGL). This is the dossier's main gap and Part 1 makes closing it the first task.

### 2.3 Orientation and placement

The building sits at the south corner of South Park's oval. The oval road and its sidewalk
run past the **north-northwest** face at 1.3–7 m; 165–167 South Park abuts on the
east-northeast and 181 South Park on the southwest, both with zero gap. It is a wedge
because the park's curve cuts across the block's 45° SoMa grid: a broad, three-facet front
on the oval narrowing over ~20.6 m to a 5.44 m tail at the back of the block.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
clockwise, already centred on the anchor `-122.3945219, 37.7809000`:

```
( -9.513,   4.415)
( -6.670,   6.693)
( -2.922,   7.477)
(  0.968,   7.400)
(  3.036,   0.591)
(  4.329,  -0.879)
(  7.215,  -4.174)
(  8.940,  -6.208)
(  5.024,  -9.988)
( -0.476,  -4.527)
(  0.343,  -3.742)
( -2.007,  -1.498)
( -3.371,  -1.664)
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `v0→v1` | 3.64 m | NW 321.3° | **park front, west facet** |
| `v1→v2` | 3.83 m | NNW 348.2° | **park front, centre facet** |
| `v2→v3` | 3.89 m | N 1.1° | **park front, east facet** |
| `v3→v4` | 7.12 m | ENE 73.1° | northeast flank, forward run (party wall with 165–167) |
| `v4→v5` | 1.96 m | NE 48.7° | northeast flank |
| `v5→v6` | 4.38 m | NE 48.8° | northeast flank |
| `v6→v7` | 2.67 m | NE 49.7° | northeast flank |
| `v7→v8` | 5.44 m | SE 136.0° | **tail (rear) elevation** |
| `v8→v9` | 7.75 m | SW 224.8° | southwest flank (party wall with 181) |
| `v9→v10` | 1.13 m | NW 316.2° | notch — light well *inferred* |
| `v10→v11` | 3.25 m | SW 223.7° | southwest flank |
| `v11→v12` | 1.37 m | S 173.1° | notch return |
| `v12→v0` | 8.64 m | SW 224.7° | southwest flank |

The `v9→v11` notch is a 1.1 x 3.3 m re-entrant on the southwest flank, almost certainly a
light well between this building and 181. Keep it: it is 2 m of silhouette that costs
nothing and it is visible from above, which is the view that matters.

Because of the ~45° heading the axis-aligned bounding box is 18.45 x 17.47 m for a
building that is 11.4 m wide at most. That is correct. The anchor is the footprint's
**area centroid**, which on a wedge is about 1.5 m from the bounding-box centre — that
offset is intentional (see 2.13; it is what buys the exclusion radius its margin).

### 2.4 What each side shows

**North-northwest (park front)** — The hero elevation, and the only one the public ever
sees. Three flat facets, each ~3.7–3.9 m wide, angled about 27° and 13° from each other so
the front bows gently along the oval. Per the district record's flats typology, expect: a
raised ground level with the entry up a short stoop, a flat roof behind a **decorative
bracketed cornice**, and **angled bay windows** rising through the upper floors — the DPR
notes South Park's flats are "primarily designed in the Edwardian-era style with either a
flat front or angled bay windows", and the neighbouring contributors on this side of the
oval carry bays. Painted wood, repainted 2012, with wood-sash double-hung windows and wood
trim from the same job. **All of this paragraph is typology, not observation — verify it
before you model it.**

**East-northeast flank** — Party wall with 165–167 South Park (a 1908 flats contributor,
8.55 m to its roof deck, so ~3 m lower than this building). The upper ~3 m of this flank
therefore stands proud of the neighbour and is genuinely visible; below that it is buried.
Build it as a plain painted wall with a sparse scatter of windows in the exposed upper
band only.

**Southwest flank** — Party wall with 181 South Park (14.18 m to its roof deck, so
*taller* than this building — this flank is fully buried in reality). Build it plain, with
the light-well notch and no window rhythm invented.

**Southeast (tail)** — 5.44 m wide, the back of the wedge. The 2005 permit's rear deck and
its steel-framed stair land here, and the satellite imagery shows a deck structure at this
end. This is the one back elevation that is actually exposed to open space, and the aerial
camera reads it clearly.

**Top** — A flat, light-tan membrane roof (re-roofed March 2026, which is why it reads
noticeably paler than its neighbours in current imagery), inside the cornice line. Visible
from satellite: a row of about four small skylights across the wide front third, a further
pair mid-roof, a pale mechanical/penthouse box (the 2005 elevator's overrun is the natural
explanation for the 12.62 m LiDAR maximum), and the rear deck at the tail. The wedge plan
is at its most legible here — design this surface hardest.

### 2.5 Recognition cues (ranked)

1. **The wedge plan** — broad on the park, tapering to a narrow tail. Nothing else in
   South Park has this footprint, and it is the cue the app's downward camera sees first.
2. **The three-facet front bowing along the oval** — the facets, not a curve.
3. Edwardian flats vocabulary: flat roof, bracketed cornice, angled bay windows.
4. Four levels of painted wood with a raised ground floor and a stoop.
5. The pale, newly re-roofed deck with its skylight row and penthouse.

### 2.6 Miniature translation

**Preserve**

- The wedge, at its real proportions and its real ~45° heading
- The three front facets as three distinct planes with visible creases
- The cornice as a continuous projecting band with real shadow
- The light-well notch on the southwest flank
- The tall/short relationship with the two neighbours (lower on the NE, higher on the SW)

**Simplify / exaggerate**

- Roughly a dozen window openings per floor become 2–3 clean bays per elevation
- The cornice's brackets become a row of identical chunky blocks, front facets only
- Bay windows become simple three-plane canted boxes, no mullion detail
- The stoop becomes three chunky steps and a slab landing; no railings beyond two posts
- Window sashes lose their divisions entirely — flat glazing panes
- The cornice is thickened to ~0.5 m so it survives at thumbnail size; this and the bay
  projection are the only places semantic exaggeration is spent
- Roof clutter becomes four skylight boxes in a row plus one pair, one penthouse, one
  deck slab with a rail

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render, and after the Street View
check settles the storey count and bay configuration.

1. Body: extrude the 2.3 footprint from z=0 to z=11.41, `Toy_sand`. Keep every vertex,
   including the notch — this shape is the asset.
2. Level lines at z = 2.85 / 5.70 / 8.55 (four levels of ~2.85 m). If the Street View
   check says three levels, use z = 3.80 / 7.60 instead and say so in `REPORT.md`.
3. Raised ground level, z=0 to z=2.85, on the front facets: a stoop of three 0.3 m steps
   and a 1.4 x 1.0 m landing to the entry on the **centre facet** (`v1→v2`); a garage
   door 2.6 m wide on the **west facet** (`v0→v1`) *if* the street check confirms one;
   two small windows otherwise.
4. Bay windows: one canted three-plane bay on the west facet and one on the east facet,
   from z=2.85 to z=11.41, projecting 0.6 m, 2.6 m wide at the wall and 1.8 m at the
   face, glazing `Toy_glass` on all three planes. The centre facet stays flat above the
   entry, so the front reads bay–entry–bay.
5. Flank and tail openings: two windows per exposed level on the tail; on the northeast
   flank, windows **only above z=8.5** (below that the neighbour hides it); nothing
   invented on the southwest flank.
6. Cornice: z=11.41 to z=11.91, projecting 0.35 m, `Toy_trim`, continuous around the
   front facets and returning 0.8 m onto each flank. A row of 0.25 x 0.35 m brackets
   under it on the front facets only, spaced ~1.1 m.
7. Roof deck at z=11.41, `Toy_roofd` in a paler mix than its neighbours (the 2026
   re-roof). Four skylight boxes 1.1 x 0.8 x 0.25 m in a row parallel to the front, one
   further pair mid-roof, all `Toy_glassl`.
8. Penthouse: 2.6 x 2.2 m from z=11.41 to **z=12.6**, `Toy_roofd` — this sets the
   bounding-box top and must land exactly on 12.6.
9. Rear deck at the tail: a 3.6 x 2.4 x 0.15 m slab at z=8.55 with two 1.0 m rail posts,
   `Toy_ink`.
10. Bevel 0.10 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | painted body walls, all four elevations |
| `Toy_trim` | `#f3efe6` | cornice, brackets, bay corner boards, window trim, stoop landing |
| `Toy_glass` | `#2a4d73` | all windows, bay glazing |
| `Toy_glassl` | `#6f95b8` | roof skylights |
| `Toy_roofd` | `#45454a` | roof deck, penthouse |
| `Toy_ink` | `#3a3530` | entry door, garage door, rear deck and rails |
| `Toy_stone` | `#d9d2c2` | stoop steps, sills |
| `Toy_glass_Glow` | `#2a4d73` | lit upper windows at night |
| `Toy_trim_Glow` | `#f3efe6` | entry lamp at night |

**The paint colours are unverified.** `Toy_sand` body with `Toy_trim` detailing is the
safe Edwardian default and the one to fall back on. But `AGENTS.md`'s SF exception exists
for exactly this building type: if Street View shows a genuinely tinted facade, take the
nearest palette entry for the body (`Toy_verdigris`, `Toy_sky`, `Toy_mustard` and
`Toy_cream` are all plausible South Park colours) and keep `Toy_trim` on the cornice and
bay boards for contrast. Off-palette is a WARN not a FAIL, so a dedicated colour is
permissible if the render justifies it. Record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque glazing —
the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a primary surface
must never be authored as glow. Hero glow: three or four lit windows scattered across the
two bays, not the whole front — this is three flats, not an office. Supporting accent: a
single lamp over the entry on the centre facet. The skylights do **not** glow; a lit
skylight on a residential roof reads as a studio, and there are four of them.

### 2.9 Top surface

The most important surface on this asset. A flat, pale roof filling a wedge, ringed by the
cornice line, with a row of four skylights across the wide front third, a pair mid-roof,
the penthouse set back near the tail, and the rear deck beyond it. Keep the deck value
clearly lighter than the neighbours' roofs (the 2026 re-roof is genuinely paler in current
imagery) and clearly darker than the `Toy_trim` cornice, so the wedge outline reads as a
ring from directly above. Do not centre the roof furniture: pushing it toward the tail
leaves the broad front third clean and makes the taper read.

### 2.10 Scope

**In the GLB:** the single flats building — body on the measured wedge footprint, all four
elevations, cornice and brackets, bay windows, stoop and entry, roof deck, skylights,
penthouse and rear deck

**Not in the GLB:** South Park street, the oval park, 165–167 South Park, 181 South Park,
Varney Place, street trees, sidewalk, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 8,000 — smaller and simpler than 380 Brannan (9,000), and the cap should bind.
Suggested split: body, notch and cornice ~2k, the two bays ~2k, front ground level with
stoop and doors ~1k, flank/tail openings ~1k, roof furniture ~1.5k, rear deck ~0.5k.

### 2.12 Draft manifest entry

```json
{
  "id": "171-south-park",
  "file": "171-south-park.glb",
  "anchor": [
    -122.3945219,
    37.7809
  ],
  "targetHeightM": 12.6,
  "cat": 2,
  "name": "171 South Park Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

**New landmark, Case B.** A `pipeline/lib/landmarks.mjs` entry and a tile re-bake are
required, or the baked procedural block on this exact footprint will intersect the GLB.

**The exclusion radius is the tightest in the registry and the arithmetic is not
optional.** `excluded()` in `pipeline/buildings.mjs` drops a footprint when its ring
centroid **or any ring vertex** falls inside the radius, and the bake's primary footprint
source is the same DataSF layer measured above. Against those rings, from the anchor
`-122.3945219, 37.7809000`:

| | distance from anchor |
|---|---|
| this building's own DataSF ring centroid (`SF3775137`) | **0.59 m** — anything above this drops it |
| nearest neighbour trigger, `SF3775028` (165–167 South Park) | **3.83 m** |
| next, `SF3775172` (181 South Park) | 3.92 m |
| next, `SF3775029` (159 South Park) | 11.02 m |

So the workable window is **0.59 m < exclude < 3.83 m**, and the entry should use
`exclude: 2` — 1.4 m of margin on each side. Anything from 4 m up deletes 165–167 and 181,
two contributors that share party walls with this building, and punches a two-lot hole in
the district's south side. Anything at or below 0.5 m leaves the procedural block standing
inside the GLB.

This is also why the anchor is the footprint's **area centroid** rather than its
bounding-box or OBB centre: on this wedge the OBB centre sits only 2.74 m from the nearest
neighbour vertex, which closes the window to nothing. Do not "tidy" the anchor.

Registry entry (matching the `380Brannan` / `550Third` id convention — camelCase in
`landmarks.mjs`, kebab-case in the manifest):

```js
{
  // Wedge lot at the south corner of the oval, party walls on both long sides,
  // so the exclusion window is the tightest in this file: this footprint's ring
  // centroid sits 0.59 m from the anchor while the nearest NEIGHBOUR trigger is
  // 3.83 m (SF3775028, 165-167 South Park). Anything from ~1 to ~3.5 m drops this
  // building alone; 4 would take 165-167 and 181 with it.
  id: '171SouthPark',
  name: '171 South Park Street',
  lon: -122.3945219,
  lat: 37.7809,
  height: 12.6,
  exclude: 2,
  camera: { distance: 200, yaw: ..., pitch: 26 },
}
```

Set `yaw` so the preset looks at the NNW park front, and confirm the yaw convention
against an existing small-building entry (`380Brannan` uses 45 for a front facing 135.6°)
before committing it — do not copy the number from this plan.

Run `node pipeline/verify-rebake.mjs` after the bake: it asserts that the nearest
*surviving* procedural footprint is farther from the anchor than the radius, which at
`exclude: 2` passes with 1.8 m to spare — and would fail loudly if the radius crept up.
Audit 1.6 must also come back clean.

`loadRadius`: the skill's default formula gives `max(2500, 12.6 * 30) = 2500` m. Take the
default; at 2.5 km a 12 m building is far below a pixel, so the carved-out gap beyond that
radius is illegible.

**Batch mode applies to this build** (`BATCH: yes`), and four sibling South Park landmarks
were in flight when it was planned (101, 135, 155, 165 South Park). Run the bake and do
the full Step 5/6 QA on it — a Case B landmark cannot be judged without its exclusion
applied — then throw the bake away with `git checkout -- app/public/tiles api/_data`
before committing, and commit source only. If two of these South Park landmarks integrate
together, re-run the exclusion arithmetic above with both entries present: their radii do
not overlap at 2 m, but 165 South Park is 3.83 m away and its own radius will be looking
back at this footprint.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0
- [ ] Origin at the footprint **area centroid**, not the bbox centre (expect a ~1.5 m XY
      offset between them — that is correct, see 2.3)
- [ ] Bounding-box top exactly 12.6 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~18.5 x 17.5 m is
      expected)
- [ ] The wedge reads instantly from the top render
- [ ] Triangles at or under 8,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit bay windows and the entry lamp; glow shells proud of opaque
      glazing; skylights not glowing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed, with the Street View
      findings recorded against every *inferred* item in 2.4

### 2.15 Open questions and risks

- **No street-level photograph was obtained.** Everything about the front elevation —
  bays vs flat front, bay count, entry position, garage, paint colours, stoop — is derived
  from the district record's typology for South Park flats and from permit descriptions,
  not from looking at the building. This is the single largest risk in the dossier and
  Part 1 makes closing it the executing agent's first task. Sources tried and why they
  failed are listed at the end of 2.2.
- **Storey count: 3 or 4?** Most permits (2007, 2012, 2026) record 3 existing storeys; the
  2005–2008 elevator and rear-deck permits record 4. The three condo units are 1,064 /
  1,102 / 1,102 sq ft on a 131 m2 (1,412 sq ft) footprint, so three floor-through flats
  account for the residential area exactly — which, with a 11.41 m roof deck, gives 3.80 m
  per floor if there are only three levels and 2.85 m if there are four. 3.80 m is
  implausibly tall for 1910 flats; 2.85 m is normal. The district record notes that South
  Park flats are "often built atop a raised basement… the space below has often been
  converted to uses including garages". **Read as three flats over a raised ground level =
  four levels visible from the street, and confirm from Street View.** The 2005 permit's
  elevator "to service all floors" is consistent with four.
- **Build date: 1908 or ca. 1910?** The Assessor roll says 1908 in every year 2007–2025;
  the 2009 historic district record says ca. 1910 and uses "ca." deliberately. Both are
  post-earthquake reconstruction and neither changes the design. The district record is the
  better-researched source; use ca. 1910 and note the Assessor value.
- **What carries the 12.62 m LiDAR maximum?** The dossier assumes the elevator/stair
  penthouse installed 2005–2009, which the 2010 LiDAR would have caught. The alternative
  is that 12.62 m is the cornice crest and there is no penthouse, which would make the
  cornice 1.2 m proud of the deck — possible but tall. Settle it from the roof imagery.
  Whichever feature wins, the bounding-box top must still land on exactly 12.6 m.
- **The light-well notch** on the southwest flank (`v9→v11`) is present in both the OSM and
  DataSF outlines, so it is real geometry, but its depth and whether it runs full height
  are *inferred*.
- **Both long flanks are party walls**, so their window rhythms are unobservable and
  largely irrelevant — but the northeast flank stands ~3 m above 165–167's roof deck and
  that exposed band **is** visible from the app's camera. Do not leave it blank and do not
  invent a full grid; a sparse scatter in the upper band only.
- **The exclusion window is 3.2 m wide** (2.13). This is the tightest in the registry and
  the failure mode is silent: too large a radius deletes two neighbouring historic
  contributors from the baked city and nothing crashes. Re-derive the numbers at
  integration time rather than trusting this plan's.
- No architect or builder is recorded for this building in any source consulted.
