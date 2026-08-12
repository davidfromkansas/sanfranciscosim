# 375 Alabama Street — SF-SIM asset plan

The **Ames Harris Neville Co. Building** (1926), a full-block four-storey reinforced-concrete
daylight factory on the corner of 17th and Alabama in the Inner Mission — later the Koret of
California garment plant, later still a City College campus, and today marketed as "The Koret
Building". It is not a monument, but it is not an ordinary box either: a cream concrete wall
of tall steel-sash bays, an Art Deco parapet frieze studded with cast **cog-wheel medallions
carrying the "AHN" monogram**, and a stepped Art Deco stair tower rising over the Alabama
Street entrance. The roof is a **sawtooth monitor roof** — which matters more here than the
elevations, because the app's camera looks down.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/375-alabama/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `375-alabama` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4118477, 37.7645633` |
| Target height | **22.5 m** to the stair-tower crest; sawtooth ridges 19.2 m; parapet crest 17.6 m; roof deck 15.9 m |
| Footprint | 61.10 m (17th Street frontage) x 54.63 m deep; 3,321 m2, measured; heading 85.7° |
| Triangle cap | 14,000 |
| Category | `19` (industrial) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 375 Alabama Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 375 Alabama Street — the Ames Harris Neville Co.
Building — in San Francisco and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render review
images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/380-brannan/` — the closest reference implementation in character (an ordinary
   industrial street building rather than a monument, one identity cue carried hard)
8. `docs/asset-plans/375-alabama.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md` governs
repository and integration rules. Do not invent a new style and do not copy visual
instructions from unrelated prompts.

## Must capture

- A **four-storey cream concrete daylight factory** filling a whole block corner: wide flat
  piers, recessed spandrels, and tall multi-light steel-sash industrial windows that fill
  nearly every bay
- The **stepped Art Deco stair tower** on the Alabama Street (west) elevation, rising ~6.6 m
  above the roof deck over the arched main entrance, with pale vertical fins flanking a
  darker centre panel and a notched crown
- The **cog-wheel medallions** in the parapet frieze — cast concrete gear discs with the
  "AHN" monogram, one over each pier on the two street elevations. This is the building's
  whole identity and the one place to spend semantic exaggeration
- The **stepped parapet**: a continuous band that steps up over every pier, with taller
  stepped caps at the corner bays
- The **sawtooth monitor roof** across the southern half — the surface the app's camera
  actually sees
- Ground-floor industrial openings: the arched pedestrian entrance with the "375" numerals
  under the tower, and wide roll-up freight doors on all three street-facing sides

## Research 375 Alabama Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation, and
gather references covering:

- All four elevations, with attention to which sides carry medallions and which are plain
- Aerial and roof/top views — the sawtooth count, direction and pitch, and the rooftop
  antenna/equipment cluster
- Ground-level views, day and night
- The bay rhythm of the Alabama and 17th Street elevations — this plan's 10/11-bay reading
  is *simplified*, not surveyed
- The stair tower: its exact position along the west wall, its plan dimensions, and above
  all its **height**, which is the weakest number in this dossier (2.15)

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. The SF Planning DPR 523 survey form for APN 3966002 (2.2) is the single best
source and carries four dated photographs. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from visual
inference; if sources disagree, document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the building is universally marketed as "the Koret
Building" but its historic name and its ornament are **Ames Harris Neville Co.**; OSM
`height=16` and the LiDAR median 15.89 m describe the **roof deck**, not the architectural
top, which is the stair tower ~6.6 m higher; and the LiDAR maximum of 36.84 m is an
artefact of the overhead trolley and utility wires that cross this corner, not a building
feature — do not build to it.

## Create a reference dossier

Write `artifacts/375-alabama/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed reference
thumbnails is welcome if legally permissible — do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few confident
volumes, exaggerate only the signature features, simplify the facade into broad rhythms,
deliberately design every surface visible from above, evaluate from the app's high
three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark — but it is a *large* secondary building whose roof is a real designed surface.
Spend the budget on: one clean bay rhythm, the medallion frieze, the tower, and the
sawtooth roof. Resist adding hero-tier ornament anywhere else.

The finished asset must be immediately recognizable as 375 Alabama Street, consistent with
the real building from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and never
accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1926 factory block: concrete body, piers and spandrels, all four
elevations' openings, the medallion frieze, the stepped parapet, the stair tower, the
sawtooth roof and the rooftop equipment.

Do not include unrelated surrounding city geometry: 17th Street, Alabama Street, Florida
Street, the neighbouring buildings, the overhead trolley wires and poles, street trees,
the sidewalk, parked cars, people, plinths, cameras or lights. Temporary context may appear
in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; no external dependencies; at most 14,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric` in
`app/src/assets.js` only scales and positions). The block is rotated **+4.32° CCW** from the
world axes: the 17th Street (south) wall runs at bearing 85.68°, the Alabama Street (west)
wall at 355.68°. Build on the measured footprint polygon in 2.3 rather than modelling an
axis-aligned box and rotating it by eye. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the stair-tower crown) must
land at exactly **22.5 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/375-alabama/build_375_alabama.py` (deterministic build script),
`artifacts/375-alabama/375-alabama.blend`, and `artifacts/375-alabama/375-alabama.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `375-alabama-top.png`,
`375-alabama-north.png`, `375-alabama-east.png`, `375-alabama-south.png`,
`375-alabama-west.png`, plus `375-alabama-contact-sheet.png`, at least one high
three-quarter aerial beauty render `375-alabama-aerial.png`, and a night render
`375-alabama-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the sawtooth field, the flat north roof, the parapet ring, the
tower and the rooftop equipment; the aerial view uses the style bible's camera assumptions
(30-50 degrees down, long lens) and should be flown from the **southwest**, which is the
only angle that shows the tower, the entrance and both medallion elevations at once. Simple
tabletop lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

## Validate the exported GLB

Re-import `375-alabama.glb` into a fresh isolated Blender scene and validate the re-import,
not the source scene. Report object count, triangle count, dimensions, bounding-box
min/max, min Z, XY center offset, material names, image-texture count, camera count, light
count, animation count, applied-transform status, negative-scale status, normal-orientation
status, unexpected geometry, and per-material contract compliance. Render at least one
review image from the re-imported asset. Write `artifacts/375-alabama/validation.json` and
`artifacts/375-alabama/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **65.1 x 59.1 m** even though the
building is 61.1 x 54.6 m — that is the expected consequence of the 4.32° heading, not a
scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "375-alabama",
  "file": "375-alabama.glb",
  "anchor": [
    -122.4118477,
    37.7645633
  ],
  "targetHeightM": 22.5,
  "cat": 19,
  "name": "375 Alabama Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or
any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/375-alabama.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify anything it
relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Historic name | **Ames Harris Neville Co.** | SF Planning DPR 523 survey form, APN 3966002 (Tim Kelley Consulting, 12 Jun 2008) — **the ornament confirms it**: the parapet medallions carry an "AHN" monogram |
| Common name today | "The Koret Building" | commercial listings; Koret of California occupied it after Ames Harris Neville |
| Built | 1926 | SF Assessor secured roll, block 3966 lot 002 (`year_property_built = 1926`); DPR form agrees |
| Storeys | **4** | SF Assessor roll (`number_of_stories = 4.0`) and every building permit from 1984 to 2023 (`number_of_existing_stories = 4`) |
| Construction | Reinforced concrete | Assessor `construction_type = C`; commercial listings ("reinforced concrete"); confirmed visually — flat cast piers and spandrels, not masonry |
| Survey status | HP8 Industrial Building, **Intensive** survey, "BSOR" status | SF Planning DPR 523 form, APN 3966002 |
| Block / lot / APN | 3966 / 002 / 3966002 | SF Assessor; DataSF footprint `mblr = SF3966002` |
| Zoning / use | M1, Industrial, Inner Mission | SF Assessor roll |
| Property area | 129,940 sq ft (12,072 m2) | SF Assessor roll; listings say ~128,000 sq ft. 12,072 / 4 ≈ 3,018 m2 per floor ≈ 91% of the footprint — consistent with 4 full floors |
| Lot area | 38,000 sq ft (3,530 m2) | SF Assessor roll |
| Footprint | 3,321 m2; OBB **61.10 m x 54.63 m**, 99.5% rectangular fill | DataSF LiDAR building footprint `SF3966002`, reprojected — **measured** |
| OSM footprint (cross-check) | 3,275 m2, 60.72 x 54.00 m | OSM way/242990064 — agrees with DataSF within ~0.7 m |
| Heading | long (17th St) walls bear **85.68°**, short (Alabama/Florida) walls **355.68°** | measured from the DataSF footprint polygon |
| Roof deck height | **15.89 m** above minimum ground | DataSF LiDAR `hgt_median_m` — **measured**; OSM `height=16` independently agrees |
| Sawtooth ridge height | **19.21 m** | DataSF LiDAR `hgt_majoritycm` — the modal height over 13,355 cells, which for this roof is the monitor field, not the deck; **measured, interpreted** |
| LiDAR maximum | 36.84 m | DataSF `hgt_maxcm` — **rejected**, see 2.15: overhead trolley/utility wires, not building |
| Ground elevation | 10.07 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Parapet crest | ~17.6 m | *inferred*, photogrammetric from the DPR photograph |
| Stair tower crest | **~22.5 m** | *inferred*, photogrammetric — the weakest number here, see 2.15 |
| Rooftop wireless facility | present since 2000, extended 2001/2012/2015/2019 | SF building permits: "install antennas at roof provide equipment rm at roof", "9 panel antennas, one gps antenna", "(3) 1' microwave dishes", "install 6 new antennas on roof" |
| Street context | Alabama St (west), Florida St (east), 17th St (south); the block runs north to 16th St | OSM highway ways within 120 m |

### 2.2 Sources

- `https://sfplanninggis.org/docs/DPRForms/3966002.pdf` — SF Planning DPR 523 survey form,
  South Mission survey, recorded by Tim Kelley Consulting 12 Jun 2008. Establishes the
  historic name (Ames Harris Neville Co.), the 1926 date, HP8 industrial classification, and
  carries four photographs dated 16 Nov 2007: `100_5330` (view to NE — the 17th/Alabama
  corner, the best single image), `100_5325` (tower detail), `100_5327` (view to W),
  `100_5328` (parapet detail — the AHN cog medallion, full frame)
- https://www.openstreetmap.org/way/242990064 — footprint, `addr:housenumber=375`,
  `addr:street=Alabama Street`, `building=yes`, `height=16`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived),
  record `mblr = SF3966002` — authoritative footprint polygon, `hgt_median_m = 15.89`,
  `hgt_majoritycm = 1921`, `gnd_min_m = 10.07`
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax
  Rolls), parcel 3966002 — 1926, 4 storeys, industrial, M1, areas
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits), block 3966 lot 002, 50
  records 1981–2023 — storey count, the rooftop wireless build-out, 2012 reroofing, the 2023
  ground-floor lobby renovation
- Esri World Imagery (z20 aerial, reprojected and overlaid on the measured footprint) —
  sawtooth field, flat north roof section, rooftop clutter
- Commercial listings (LoopNet / Showcase / SquareFoot, "The Koret Bldg") — 4 storeys,
  reinforced concrete, ~128,000–129,940 sq ft, current PDR/office/warehouse tenancy
- Flickr, `anomalous_a/3397380379` — "375 Alabama Street, San Francisco (built 1926)",
  photographed 26 Oct 2007

### 2.3 Orientation and placement

The building fills the northeast corner of 17th and Alabama, running the full block width
east to Florida Street. Alabama Street is its address and its front. The block is rotated
**+4.32° counter-clockwise** from the world axes, like the rest of the Mission grid.

Measured footprint polygon, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.4118477, 37.7645633`:

```
(  28.359,  29.537)
(  30.120,   6.196)
(  30.742,  -1.359)
(  30.428,  -1.394)
(  32.429, -24.754)
( -28.407, -29.541)
( -30.026,  -6.061)
( -30.575,   0.730)
( -32.354,  24.938)
```

(sub-30 mm duplicate vertices in the source polygon dropped; the two ~0.5 m jogs on the east
and west walls are real pilaster returns and are worth keeping.)

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-28.407,-29.541) -> (32.429,-24.754)` | 61.02 m | S 175.7° | **17th Street** — long street elevation |
| `(32.429,-24.754) -> (28.359,29.537)` | 54.44 m | E 85.7° | **Florida Street** — service elevation |
| `(28.359,29.537) -> (-32.354,24.938)` | 60.88 m | N 355.7° | rear, faces the yard and the rest of the block |
| `(-32.354,24.938) -> (-28.407,-29.541)` | 54.62 m | W 265.7° | **Alabama Street** — the address, the entrance, the tower |

Because of the 4.32° heading the axis-aligned bounding box is ~65.1 x 59.1 m. That is
correct.

### 2.4 What each side shows

**West (Alabama Street)** — The address elevation and the hero. A cream painted concrete
wall divided by wide flat piers into roughly ten bays, each filled almost edge to edge with
a tall multi-light steel-sash industrial window on floors 2–4 and a shorter one at ground
level. Spandrel panels between floors are slightly recessed and read a shade darker. Above
the top-floor windows runs the frieze: a **cast cog-wheel medallion over each pier**, and a
parapet that steps up over every pier so the skyline is a low crenellated rhythm rather than
a flat line. Roughly two to three bays north of the 17th Street corner the wall breaks for
the **stair tower** — a shallow projecting shaft, pale vertical fins flanking a darker
centre panel, rising about 6.6 m above the parapet to a notched Art Deco crown. Directly
under it is the arched pedestrian entrance with the **"375" numerals** on the pier beside
it, and immediately south of that a wide roll-up freight door.

**South (17th Street)** — The long elevation, ~61 m, same grammar: eleven bays of piers and
steel sash, the same medallion frieze and stepped parapet, and a corner bay at the southwest
whose parapet cap is taller and chamfered at 45°. Ground floor is mostly service: two wide
roll-up freight doors and a scatter of arched openings. No tower.

**East (Florida Street)** — Same structural grammar, plainer treatment: the bay rhythm and
the steel sash continue, but the medallion frieze thins out or stops and the parapet is
mostly a straight band. Ground floor is loading. *Inferred* — no photograph in the sources
covers this side straight on.

**North (rear)** — Faces a narrow yard and the rest of the block, not a street. Largely
blank concrete with sparse openings and service doors; the app's aerial camera sees it
plainly, so it must be built properly, but it carries no medallions and no ornament.

**Top** — The most important surface. The southern ~60% of the roof is a **sawtooth monitor
field**: five parallel ridges running east–west, ridge line at ~19.2 m, glazed slope facing
north (*inferred* — the standard for a daylight factory of this date), opaque slope facing
south. The northern ~40% is a large flat dark membrane roof at deck level, notably clean.
The stair tower sits on the west edge. A rooftop antenna/equipment cluster — panel antennas,
small microwave dishes and an equipment room, permitted from 2000 onward — sits toward the
east side. Vent stacks are scattered along the west strip. A continuous parapet rings the
whole thing.

### 2.5 Recognition cues (ranked)

1. **The cog-wheel "AHN" medallions** in the parapet frieze — the one ornament nobody else
   in the Mission has, and the reason this building is worth a bespoke asset
2. **The stepped Art Deco stair tower** over the Alabama Street entrance, the only thing
   that breaks the skyline
3. The **sawtooth monitor roof** — the identity from above, which is the app's default view
4. A long cream four-storey wall of tall steel-sash bays between expressed piers, wrapping a
   whole block corner
5. The stepped parapet with raised pier caps and chamfered corner bays

### 2.6 Miniature translation

**Preserve**

- The single chunky block at its real 4.32° heading, full-block-corner scale
- The medallion frieze on the two street elevations — exaggerated, see below
- The tower's stepped silhouette and its position over the entrance
- The sawtooth roof as real geometry, not a texture or a decal
- The pier/spandrel/window grammar as a clear rhythm

**Simplify / exaggerate**

- Roughly twelve real bays per short elevation become **10** (5.46 m pitch); the long
  elevations become **11** (5.55 m pitch), all identical
- Multi-light steel sash becomes one flat recessed `Toy_glass` panel per bay per floor —
  no mullion grid; the recess and the pier shadow carry the rhythm
- The medallions are enlarged to **2.0 m diameter** (from a real ~1.2 m) and cut as a
  12-tooth cog silhouette proud 0.15 m. This is where the semantic exaggeration is spent;
  the "AHN" monogram inside them is dropped — it is sub-pixel and the cog reads alone
- The medallion frieze runs on the **west and south elevations only**; east and north get a
  plain stepped parapet. Real-world accuracy is uncertain on the east side and the budget is
  better spent than doubled
- Five sawteeth, not the real count if it differs by one; a clean constant pitch
- The rooftop antenna farm becomes one equipment block, two dish discs and a short mast
- Window guardrails and fire-escape ironwork disappear entirely — sub-pixel at city scale
- Ground-floor openings reduce to: one arched entrance, four roll-up freight doors (one
  west, two south, one east), and a handful of service doors

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 footprint from z=0 to z=15.9, `Toy_cream`. Everything else is
   added to this shell.
2. Pier grid: on all four elevations, piers 1.5 m wide proud 0.25 m, from z=0 to the
   parapet. 10 piers on the west and east walls, 11 on the north and south.
3. Ground floor, z=0 to z=4.9: bay infill recessed 0.3 m, `Toy_sand`. On the west wall, the
   arched entrance (2.4 m wide, 8-segment arch, rise 0.6 m, `Toy_ink` reveal) in the bay
   under the tower, with a `Toy_trim` "375" plaque on the pier to its north, and a 4.5 m
   roll-up door `Toy_steel` in the bay to its south. Two roll-up doors on the south wall,
   one on the east. Remaining ground bays get a short window, `Toy_glass`.
4. Upper floors: three bands of windows, sills at z=5.4 / 9.1 / 12.8, openings 3.9 m wide x
   2.9 m tall, recessed 0.25 m, `Toy_glass`. Spandrels between them `Toy_sand`, recessed
   0.12 m.
5. Frieze band: z=15.9 to z=17.0, `Toy_cream`, continuous.
6. **Medallions**: 2.0 m diameter, 12-tooth cog discs, proud 0.15 m, `Toy_stone`, centred on
   each pier of the west and south elevations at z=16.45.
7. Parapet: base band z=15.9 to z=17.6 following the footprint, 0.4 m thick, `Toy_stone`
   cap. Over each pier the cap steps up to z=18.4. At the four corner bays the cap steps to
   z=18.4 with a 45° chamfer on the outer corner.
8. Roof deck at z=15.9, `Toy_roofd`. North 40% (y > +5 m in local terms) stays flat.
9. **Sawtooth field** over the south 60%: five monitors, pitch 4.6 m, ridge z=19.2, valley
   z=15.9; north-facing slope glazed `Toy_glassl` at ~60° from horizontal, south-facing
   slope opaque `Toy_stone` at ~25°. Ends closed with `Toy_cream` gables. Ridges run east–
   west, held 3 m clear of the parapet on all sides.
10. **Stair tower**: shaft 5.6 m (E–W) x 7.6 m (N–S), projecting 0.8 m proud of the west
    wall, centred 13 m north of the southwest corner, from z=0 to z=20.6 in `Toy_cream`,
    with a 3.2 m wide `Toy_rust` centre panel on the west face flanked by two `Toy_trim`
    fins that continue to **z=22.5** — this sets the bounding-box top and must land exactly
    on 22.5. Crown notched: centre panel steps back and up to z=21.8, fins to 22.5.
11. Rooftop equipment on the northeast quadrant of the flat roof: one 4 x 3 x 2.2 m
    `Toy_steel` equipment block, two 1.2 m dish discs, one 3.5 m mast, four 0.6 m vent
    stacks along the west strip.
12. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | main concrete walls, piers, tower shaft, sawtooth gables |
| `Toy_sand` | `#ece4d4` | recessed bay infill and spandrel panels |
| `Toy_stone` | `#d9d2c2` | parapet caps, **the cog medallions**, sawtooth opaque slopes |
| `Toy_trim` | `#f3efe6` | tower fins, the "375" plaque |
| `Toy_rust` | `#a86444` | the tower's centre panel |
| `Toy_glass` | `#2a4d73` | all wall windows |
| `Toy_glassl` | `#6f95b8` | sawtooth glazing (lighter, reads as up-facing) |
| `Toy_roofd` | `#45454a` | flat roof membrane |
| `Toy_steel` | `#9aa0a6` | roll-up doors, rooftop equipment, dishes, mast |
| `Toy_ink` | `#3a3530` | entrance reveal, door recesses, vent stacks |
| `Toy_glass_Glow` | `#2a4d73` | lit windows at night |
| `Toy_glassl_Glow` | `#6f95b8` | two lit sawtooth monitors at night |
| `Toy_trim_Glow` | `#f3efe6` | the tower crown fins at night |

Note on the tower centre panel: in the 2007 photograph it reads as a dusty mauve-taupe with
no exact palette match. `Toy_rust` is the closest and is warmer than reality; off-palette is
a WARN not a FAIL, so a dedicated `Toy_mauve` at roughly `#a2887f` is permissible if the
render justifies it. Decide from the aerial render and record the decision in `REPORT.md`.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow.

- **Hero glow:** the tower crown fins. It is the only thing that breaks the skyline, and a
  lit Art Deco crown is the single most legible night cue this building can have.
- **Supporting:** two of the five sawtooth monitors lit from within — a factory still
  working after dark, and it reads from directly overhead where the elevations do not.
- **Accent:** a scatter of perhaps eight to ten lit upper-floor windows across the west and
  south elevations, and the arched entrance.
- The medallions do **not** glow. They are a daylight identity feature; lighting them would
  misread as signage.

### 2.9 Top surface

This building's roof is its best asset and the reason the triangle cap is 14,000 rather than
9,000. Five sawtooth monitors across the south, a clean dark flat membrane across the north,
a continuous stepped parapet ring, the tower breaking the west edge, and one honest little
antenna cluster to the northeast. Keep the flat membrane clearly darker than both the
parapet cap and the sawtooth slopes so all three read as separate planes from above, and
keep the sawtooth glazing lighter than the wall glass so the roof does not go muddy.

### 2.10 Scope

**In the GLB:** the single 1926 factory block — concrete body, piers, spandrels, all four
elevations' openings, the medallion frieze, the stepped parapet, the stair tower, the
sawtooth roof, the rooftop equipment cluster

**Not in the GLB:** 17th / Alabama / Florida Streets, the neighbouring buildings, the yard
to the north, the overhead trolley wires and poles, street trees, sidewalk, vehicles,
people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 14,000. Suggested split: body, piers and spandrels ~3k; window openings across four
elevations ~3.5k; medallion frieze (21 cogs at ~120 tris) ~2.5k; stepped parapet ~1.5k;
sawtooth field ~1.5k; tower ~1k; ground-floor openings and roof equipment ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "375-alabama",
  "file": "375-alabama.glb",
  "anchor": [
    -122.4118477,
    37.7645633
  ],
  "targetHeightM": 22.5,
  "cat": 19,
  "name": "375 Alabama Street",
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

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '375-alabama'`,
  `height: 22.5`, `exclude: 42`) and re-bake the affected tiles, or the baked procedural
  building on this exact footprint will intersect the GLB. The footprint's half-diagonal is
  41 m, so the exclusion radius has to be larger than any previous non-monument entry;
  **verify at integration which baked footprints it removes** — Alabama and Florida Streets
  are only ~20 m wide and a careless radius will punch holes in the facing blocks.
- Suggested camera preset: `{ distance: 330, yaw: 215, pitch: 18 }` — the southwest
  three-quarter that shows the tower, the entrance and both medallion elevations.
- `loadRadius`: the skill's default formula gives `max(2500, 22.5 * 30) = 2500` m. The
  procedural stand-in is carved out, so beyond that radius the site is a gap — but at 2.5 km
  a 22 m building is far below a pixel. Take the default.
- This is the second non-monument building in the landmark manifest after `380-brannan`, and
  it is a much bigger one. The same question applies: if the intent is to keep doing
  individual Mission and SoMa blocks, the kit/instancing route
  (`KIT-INTEGRATION-PROMPT.md`) is the better long-term home for buildings of this class.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 22.5 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~65.1 x 59.1 m is expected)
- [ ] Triangles at or under 14,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the tower crown, two sawtooth monitors, the scattered lit windows and
      the entrance; glow shells proud of opaque glazing
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for
      the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The stair-tower height is the weakest number in this dossier.** 22.5 m is a
  photogrammetric read of the 2007 DPR photograph, calibrated against the LiDAR roof deck
  (15.89 m) using the four floor lines as a ruler; the honest range is **21–24 m**. Because
  the tower is the tallest geometry, this number *is* `targetHeightM` and it scales the whole
  asset. If a better source turns up, correct it and rebuild rather than nudging the tower.
- **The tower's position along the west wall is *inferred*** at ~13 m north of the southwest
  corner, from bay counting in one oblique photograph. Aerial imagery at the resolution
  available did not resolve it. Two bays either way would not be a visual failure, but the
  tower must stay on the **Alabama Street** side and over the arched entrance — that pairing
  is certain, because the "375" numerals are on the pier beside that arch.
- **`hgt_maxcm = 36.84 m` in the DataSF LiDAR record is not the building.** This corner
  carries a dense web of overhead trolley and utility wires (plainly visible across the 2007
  photograph) and the LiDAR first return picked them up. `hgt_mincm = 0.24 m` in the same
  record shows the polygon also samples ground, so neither extreme is usable. Use the median
  and the mode.
- **`height=16` in OSM is the roof deck.** It agrees with the LiDAR median to within 0.11 m,
  which makes it look like a well-sourced architectural height. It is not. This is exactly
  the trap the plans README warns about.
- **The sawtooth orientation is *inferred*.** North-facing glazing is the standard for a
  daylight factory of this date and the aerial imagery is consistent with it, but the
  imagery is not sharp enough to prove which slope is glass. If it turns out to be
  south-facing the roof reads differently at night.
- **The east (Florida Street) elevation is unphotographed in the sources consulted.** The
  plan assumes it repeats the bay grammar without the medallion frieze. Confirm before
  building, or model it plainly and record the assumption.
- **The bay counts (10 / 11) are a design simplification**, not a survey. The real building
  appears to have roughly twelve bays on the short elevations. Do not present them as
  measured.
- The large flat north roof section reads in aerial imagery as a single dark membrane at
  deck level. It could also be a slightly lower roof over a light court. Modelling it flat at
  deck level is the safe choice either way.
- No architect is recorded for the 1926 building in any source consulted; the DPR form names
  only the surveyor.
