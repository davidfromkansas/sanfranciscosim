# South Park (64 South Park) — SF-SIM asset plan

San Francisco's **oldest public park**: a 160 m green lozenge laid out in 1852 inside the
block bounded by Second, Third, Brannan and Bryant, and completely re-cut in 2017 by
Fletcher Studio. The 2017 design is a "contemporary interpretation of the picturesque":
one meandering concrete promenade of oblong "tablet" pavers running the whole length,
thickening and thinning into plazas, dividing the ground into five lawns, held by six
long curved cast-in-place seat walls, edged by thirteen bio-retention garden beds, and
anchored at the south-west by the Berliner Seilfabrik **"Shout"** — a play sculpture that
is a perfect circle in plan and a pair of undulating steel tubes in elevation, rising from
0.6 m to 3.0 m over a mound that hides its six below-grade posts.

This is the **second** plan in the set whose subject has no building, after
`civic-center-plaza.md`, and it follows that plan's argument for treating a designed
landscape as a single landmark GLB rather than routing it through `docs/plans/parks/`
(see 2.15 risk 6). Recognition here comes from **outline, ground pattern and canopy**, not
from massing: a green oval with a bone-white ribbon drawn through it, inside a district
of grey rectangles.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/64-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `64-south-park` |
| Registry id | `64SouthPark` (`camelId()` in `app/src/assets.js` maps one to the other) |
| Existing procedural builder | none — new landmark (**Case B**: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3939704, 37.7815903` (oriented-bounding-box centre, measured from OSM way `24052083`) |
| Target height | **21.04 m** — the asset's VERTICAL EXTENT, because the asset is draped on the terrain: 6.11 m of terrain fall + the 15.0 m tallest elm + the plate's skirt. The architectural number is the 15.0 m elm crest above its own ground, *estimated*; see 2.15 risks 1 and 9 |
| Footprint | 159.51 m × 23.51 m oriented (long axis bearing 45.47° true), 3,478 m² = 0.859 acre, measured from OSM way `24052083` |
| Axis-aligned XY bbox | 122.5 m × 121.0 m — expected, not a scale error: a 6.8:1 lozenge at 45° to the world axes has a near-square AABB, plus canopy overhang |
| Terrain | falls **6.11 m** along the long axis (13.58 m at Second Street, 7.73 m at Third); cross-axis flat to 0.30 m. **The asset is draped** — see 2.15 risk 9 |
| Triangle cap | 12,000 |
| Category | `0` (Miscellaneous — the slot Civic Center Plaza, Palace of Fine Arts, Coit Tower and Chase Center use) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **South Park**, San Francisco (64 South Park,
94107 — the oval public park inside the block bounded by Second, Third, Brannan and
Bryant streets), and deliver it as a downloadable, validated GLB.

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
7. `artifacts/civic-center-plaza/` — **the reference implementation for this asset.** The
   only other landmark that is a designed open space rather than a building. Its build
   script's frame helpers (`to_world`, `orient_for_world`, `prism_uv`, `frustum`,
   `bevel`, `hash01`), its Z-stack discipline (every level a distinct closed solid, no
   coplanar surfaces), its measured-data-in-`data/` pattern and its glow-shell rule are
   all reused here. Read `build_civic_center_plaza.py` before writing a line.
8. `artifacts/181-south-park/` and `artifacts/188-south-park/` — the two nearest
   neighbours on this same oval, for palette and bevel continuity. This asset has to look
   like it came out of the same toy box as the seven houses that already ring it.

Then read Part 2 of `docs/asset-plans/64-south-park.md` — the dossier. Every number in
this task comes from there.

## Must capture

The five recognition cues, in order (2.5):

1. **The oval.** 159.5 × 23.5 m, 6.8:1, long axis bearing 45.47°. It is the only curved
   figure in a district of rectangles and it is what identifies the place from the air.
   The historic rounded kerb — the one element that survives from 1854 — draws it.
2. **The single meandering promenade.** One path, 188 m long, from the south-west entry
   to the north-east entry, of oblong concrete "tablet" pavers, widening into plazas and
   narrowing between them.
3. **The Shout.** A perfect 11.8 m circle in plan; two side-by-side steel tubes
   undulating 0.6 → 3.0 m; nets slung between them; sitting on a mound that hides the
   posts. Centred at (u −36.0, v −1.3).
4. **The six curved seat walls.** 31–81 m each, 370 m in total, cast-in-place concrete
   with backs, following grade along the path and holding the lawns.
5. **The canopy.** Mature elms and pollarded London planes around the perimeter, over
   thirteen bio-retention beds; five sloping lawns in the gaps.

## Research South Park independently

Do not take the dossier on trust. Re-verify before modelling (this is a
session-hardened rule — plans in this repo have been wrong before):

- The park polygon and every feature position, from the OSM API (way `24052083` and the
  ways/nodes inside it). `artifacts/64-south-park/data/park_uv.json` is provided, but
  re-derive it if anything looks off.
- Photographs of the park from above and from all four approaches. Sources in 2.2. The
  camera looks down: the ground pattern is the facade here.
- The Shout's geometry, from the manufacturer (Berliner Seilfabrik) — 0.6 to 3.0 m,
  perfect circle in plan, six posts below grade.
- **Tree heights are the one number nothing verifies.** 2.15 risk 1. If a photograph or
  a LiDAR canopy product settles them, use it and say so in REPORT.md.

Record every correction prominently in `REFERENCE.md` and `REPORT.md`. **REPORT beats
plan, always.**

## Create a reference dossier

`artifacts/64-south-park/REFERENCE.md`: verified facts with sources, the anchor and
heading, the Z stack, the palette map, what each elevation and the top view show, the
recognition cues, every semantic exaggeration with its justification, and every
correction made to this plan.

## Make your own design decisions

The dossier's massing recipe (2.7) is a starting point, not a specification. You are the
art director. What is NOT negotiable:

- the measured plan — the oval, the path centreline, the wall alignments, the bed and
  lawn polygons and the Shout's circle are survey data, not design;
- the style bible (`docs/styles/miniature-toy.md`) and the asset contract;
- the terrain drape, and the two contract deviations it forces (see below);
- a designed night state.

## Scope of the exported asset

**In:** everything inside the park's kerb line — ground plate, kerb, path, seat walls,
lawns and their mounding, garden beds, the playground mound, surfacing and the Shout,
trees, benches, tables, bike racks, picnic tables, waste baskets, the drinking fountain
and the four lamp standards.

**Out:** the South Park street loop and its sidewalks, the bulb-outs and chicanes, the
surrounding buildings, any people or vehicles. The pipeline bakes the street; the seven
neighbouring houses are already their own landmarks.

## Technical asset contract

- Binary GLB, real metres, applied transforms, no negative scales.
- Origin at the OBB centre, geometry sitting on z = 0, XY centre within 0.5 m of origin.
- **The asset is DRAPED on the baked terrain** (2.15 risk 9). `placeGeneric()` in
  `app/src/assets.js` seats a landmark from ONE terrain sample at the anchor, and this
  park falls 6.11 m over its length, so a flat slab is buried at one end and floating at
  the other. Every z is `authored height + dy(u)`, sampled from
  `pipeline/lib/heightmap.mjs` by `sample_terrain.mjs`. Consequences: **`min_z` is
  negative** (z = 0 is the anchor's ground, which is where the loader puts it, not the
  bottom of the model), and **`targetHeightM` is the model's vertical extent**, not an
  architectural height, because the loader's scale is `targetHeightM / bbox height` and
  it must land on 1.0. The 15.00 m elm crest is asserted separately, against its own
  ground.
- Authored in world space at the real heading (long axis bearing 45.47°), like
  `civic-center-plaza`: the loader applies no rotation. The AABB comes out ~117 × 116 m;
  that is correct.
- Flat colours only, no textures, no transparency; materials `Toy_*` from the project
  palette; `_Glow` suffix only on night-glow surfaces, and every glow surface must be a
  thin shell proud of an opaque parent (the app renders `_Glow` at ~12% alpha by day, so
  a primary surface authored as glow disappears in daylight).
- No cameras, lights, animations, armatures or constraints. No foreign geometry.
- ≤ 12,000 triangles, ≤ 500 KB compressed.
- Bevel 0.10–0.15 m, 2 segments, clamped to a third of the thinnest dimension — most of
  this asset is 100–300 mm paving and an unclamped bevel collapses it.

## Reproducible Blender workflow

A single deterministic script, `build_64_south_park.py`, run headless:

```
blender -b --python build_64_south_park.py -- --out artifacts/64-south-park
```

No interactive modelling, no random numbers (use the `hash01` mixer from
`build_civic_center_plaza.py` for any variation, seeded off the feature index). It reads
`data/park_uv.json` and writes `64-south-park.blend` and `64-south-park.glb`.

## Required review renders

`render_64_south_park.py`, headless, deterministic:

- high three-quarter aerial, day — **review this one first and iterate on it**
- the same aerial at night
- top (plan) — the ground pattern is the point of this asset
- four elevations: north-east end, south-west end, north-west side, south-east side
- a contact sheet assembling all of the above (`make_contact_sheet.py`)

## Validate the exported GLB

`validate_64_south_park.py`: fresh isolated scene, re-import the final GLB, and check
every item in 2.14. Per-object signed-volume normals test is authoritative; whole-model
ray residual ≤ 0.15%. Write `validation.json`. All checks must PASS before you present.

## Manifest draft

Produce the entry from 2.12 with the measured `dims` and `tris` filled in. Do not add it
to `landmarks_manifest.json` — integration is a separate task.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Source / confidence |
|---|---|---|
| Name | South Park | OSM `name`, Rec & Park — **verified** |
| Address | 64 South Park (also written 64 South Park Avenue / 64 S Park St), SF 94107 | SF Rec & Park project page, sf-parks.com — **verified**. This address is the PARK, not a building; there is no building numbered 64 on this street |
| OSM feature | way `24052083`, `leisure=park`, `wikidata=Q3492264`, `start_date=1852`, `ele=10` | Overpass — **verified** |
| Established | laid out 1852 by George Gordon; built out from 1854 by architect George Goddard; acquired by the city and opened to the public 1897 | TCLF, Fletcher Studio, HortScience — **verified** |
| Status | the oldest public park in San Francisco | Rec & Park, TCLF — **verified** |
| Historic form | central oval in the Picturesque tradition of Nash's Park Crescent, London; ~550 ft on the major axis; ringed by two-storey Regency row houses (lost in 1906); enclosed by cast-iron railing; Dutch-style windmill at the centre pumping from a well; railing and windmill removed 1897 | TCLF — **verified**. None of this survives except the rounded kerbs |
| 2017 redesign | Fletcher Studio (lead David Fletcher, PM Cory Hallam), opened March 2017, $2.8 M raised, $1 M city allocation; ASLA National Honor Award, ASLA NorCal Honor, SF Design Week Civic Design Award, CODAworx, Kirby Ward Fitzpatrick Prize | Fletcher Studio, ASLA-NCC, Rec & Park — **verified** |
| Oriented footprint | **159.508 × 23.507 m**, long axis bearing **45.467°** true | minimum-area OBB over OSM way `24052083`, 47 vertices — **measured** |
| Anchor (OBB centre) | **−122.3939704, 37.7815903** | **measured**; polygon centroid is −122.3939749, 37.7815892, 0.4 m away |
| Area | 3,478.2 m² = 0.859 acre = 37,439 sq ft | shoelace over the OSM ring — **measured**. Sources disagree: Rec & Park says "approximately 34,000 sq ft", Fletcher Studio says 1.2 acres (52,300 sq ft), TCLF says one acre. See 2.15 risk 3 |
| Ground elevation | 10 m (OSM `ele`) | the app's terrain handles this, not the asset |
| Main path | one way, `549848273`, **188.0 m**, 31 vertices, spanning u −78.6 → +77.9; surface `concrete` | OSM — **measured**. Plus 9 short entry stubs (paved/asphalt/concrete), 55 m in total |
| Seat walls | six ways tagged `amenity=bench, backrest=yes, material=concrete`: 31.2, 50.2, 60.3, 73.5, 73.6, 81.1 m — **369.9 m total** | OSM — **measured** |
| Lawns | four `landcover=grass` polygons, 169 / 250 / 327 / 371 m² = **1,117 m²**; the playground's grass apron is the fifth | OSM — **measured**. TCLF: "a series of five separate lawns" |
| Garden beds | thirteen `leisure=garden` polygons, 3.0 → 157.0 m², **790 m² total**, almost all along the two long edges | OSM — **measured** |
| Playground | `leisure=playground` "South Park Playground", 304 m², u −48.8 → −25.0 | OSM — **measured** |
| Play structure | Berliner Seilfabrik **"Shout"**, custom, with Miracle Playsystems; way `549848249` is an 11.78 × 11.89 m ring (109.1 m²) centred at u −36.03, v −1.29; "a perfect circle in plan"; two curved steel tubes side by side; undulating **0.6 m → 3.0 m**; six posts, all below grade; nets, a nest swing, climbing plates, a banister slide | Berliner Seilfabrik, Russell Play, Miracle Playsystems, OSM — **verified** |
| Furniture | 15 bench nodes, 13 `amenity=table`, 3 picnic tables, 2 picnic sites, 7 waste baskets, 4 bicycle-parking, 1 drinking fountain | OSM — **measured**. The Chronicle notes six benches whose armrests double as laptop tables, and bike racks with table tops |
| Lighting | four `highway=street_lamp`, `lamp_mount=straight_mast`, `support=pole`, at u +73.2, −29.9, −48.6, −73.2 | OSM — **measured**. Site lighting was in the 2017 scope |
| Trees mapped | 20 `natural=tree` nodes, no `height`, no `species` on any of them | OSM — **measured**, and an undercount: see 2.15 risk 2 |
| Tree stand (pre-2017) | 52 assessed in 2015: 31 London plane (*Platanus × acerifolia*), 13 American elm (*Ulmus americana*), 3 silver dollar gum (*Eucalyptus polyanthemos*), 3 white alder, 1 Lombardy poplar, 1 olive. Planes and elms both pollarded when young, attachments at 8–12 ft, several later topped at 12–15 ft; elm crowns "narrow and upright"; DBH 6–24" (planes), 16½–33" (elms) | HortScience *Tree Assessment, South Park*, March 2012 / updated November 2015 — **verified** |
| Tree stand (post-2017) | 30 removed in 2016; 24 mature trees added; "18 aged elm and sycamore trees planted after 1906" retained, replanting the original perimeter ring of shade trees | SF Chronicle (John King, 25 Mar 2017), Rec & Park, TCLF — **verified** |
| Tree heights | **not established by any source consulted** | see 2.15 risk 1 |
| Materials (real) | "honest materials": natural concrete, thermally modified wood, metals stainless / galvanized / raw aluminium, chosen to patinate | Fletcher Studio — **verified** |
| Design systems | four: an expandable modular paving system; large sloping meadows; vegetated infiltration basins; low retaining walls | Fletcher Studio, ASLA — **verified** |
| Neighbouring landmarks | 101, 135, 155, 165, 171, 181 and 188 South Park are already integrated GLBs ringing this oval | `landmarks_manifest.json` — **verified** |

### 2.2 Sources

- Overpass API — way `24052083` (the park) and every way/node inside it; the ways
  numbered `5498482xx`/`5498484xx` are the 2017 as-built survey
- `https://www.fletcher.studio/southpark` — the designer's own project page: programme,
  materials, awards, size
- `https://www.fletcher.studio/blog/2017/5/26/the-parametric-park` — the four material
  systems, the "tablet"-shaped pavers arrayed on the north/south axis, the long walls
  that follow grade, the Grasshopper process
- `https://www.fletcher.studio/blog/2018/9/22/building-south-parks-iconic-climbing-structure`
  — production and installation photography of the Shout
- `https://landezine.com/south-park-san-francisco-by-fletcher-studio/` — the fullest
  photo set (Marion Brenner, ~25 images: aerial, path, walls, play structure, beds).
  **The primary photo source for this asset.** Photos are not downloaded; open the page
- `https://asla-ncc.org/portfolio-items/south-park/` — ASLA NorCal Honor Award, ten images
- `https://www.tclf.org/south-park-ca` — the historic record: 1852 conception, Goddard,
  the 550 ft oval, railing and windmill, the five lawns of the 2017 plan
- `https://www.sfchronicle.com/bayarea/article/Latest-South-Park-rendition-a-place-for-all-11027159.php`
  — John King, 25 Mar 2017: the surviving rounded kerbs, 18 aged elms and sycamores,
  30 trees removed, the east-side lawns and central hillock, the popsicle-stick walkway,
  the six laptop-table benches, the bike racks with table tops
- `https://sfrecpark.org/576/South-Park` and `https://sf-parks.com/park-improvements/completed-projects/south-park/`
  — the city's project record: 34,000 sq ft, 24 mature trees added, March 2017
- `https://sfrecpark.org/DocumentCenter/View/1805/Updated-Certified-Arborist-Report-November-2015-PDF`
  — HortScience tree assessment: species mix, DBH, pollard structure, condition
- `https://sfrecpark.org/DocumentCenter/View/1813/Presentation-PDF` — the 2013 master
  plan boards: existing tree types, proposed site plan key (entry plaza, 20" concrete
  garden wall, plaza, play zone, stone sculpture, concrete pathway, light standard,
  36" box trees, tables and chairs, bike racks)
- `https://berliner-seilfabrik.com/en/references/south-park-san-francisco/`,
  `https://russell-play.com/products/presenting-south-park-san-francisco/`,
  `https://www.miracleplaysystems.com/bay-area-projects/south-park` — the Shout:
  0.6–3.0 m, perfect circle in plan, six below-grade posts, net types, nest swing
- Esri World Imagery, nadir, ~0.15 m/px — **observed**: canopy coverage, the near-
  continuous perimeter ring, the lawn gaps, the pale path threading the length

Exa searches run, for the record: "64 South Park San Francisco building" (which is what
established that 64 South Park is the park itself, not a building — sfrecpark.org and
sf-parks.com both name it); "South Park San Francisco 2017 renovation Fletcher Studio
landscape architects design"; "South Park San Francisco play structure hoops netting
Fletcher Studio height dimensions"; "South Park San Francisco elm sycamore trees arborist
perimeter ring shade trees species". Domains that yielded material: fletcher.studio,
landezine.com, tclf.org, sfchronicle.com, sfrecpark.org, berliner-seilfabrik.com,
russell-play.com, asla-ncc.org.

### 2.3 Orientation and placement

The park's long axis bears **45.467°** true — the SoMa grid, the same heading as every
building on the oval. The authoring frame is:

- **+u** along the long axis toward the **north-east** (the Second Street end), bearing
  45.467°;
- **+v** across the short axis toward the **south-east** (the Brannan side), bearing
  135.467°;
- origin at the OBB centre, `−122.3939704, 37.7815903`.

Extents in this frame: u −79.75 → +79.75, v −11.75 → +11.75.

Geometry is authored **in world space at the real heading**, exactly as
`civic-center-plaza` does — the loader applies no rotation, so the model drops in
correctly oriented. The consequence is that the axis-aligned XY bounding box is
**~117.1 × 115.7 m** for a park that is 159.5 × 23.5 m. That is a 45° lozenge, not a
scale error, and the validator should assert the oriented dimensions, not the AABB.

The contract's "front faces −Y" rule does not apply: a park has no front. The
substitute assertion is the heading itself.

**Watch the sign of the heading.** `civic-center-plaza` shipped a build mirrored about
its own axis because an AABB check cannot distinguish +9° from −9°. Here the check is:
the Shout must come out at the **south-west** end of the park (nearer Third Street), the
big north-east lawn nearer Second Street, and the four lamps on the north-west side plus
one at the far north-east. Verify in the top render before anything else.

### 2.4 What each side shows

- **Top (the real facade).** A green lozenge. A bone-white ribbon of tablets runs corner
  to corner, thickening three times into plazas. A perfect anthracite circle sits at
  u −36 on a pale sand disc. Teal beds line both long edges; five mint lawns fill the
  gaps; grey-green crowns break the outline all round.
- **North-west side** (Bryant side, v = −11.75). The long garden bed `549848244` runs
  52 m along this edge; four of the trees and three of the four lamps stand here; the
  ground rises gently to the central hillock behind.
- **South-east side** (Brannan side, v = +11.75). Beds `549848257`, `549848261`,
  `549848263`, `549848264` step along the edge; the seat wall `549848251` (81 m, the
  longest) backs onto it, presenting its concrete face outward — this is the elevation
  where the walls read as walls rather than as seats.
- **South-west end** (Third Street, u = −79.75). The narrow entry: two path stubs, a
  lamp, the westernmost lawn, and behind it the playground mound with the Shout
  silhouetted at 4.3 m. The most three-dimensional end.
- **North-east end** (Second Street, u = +79.75). The wide entry plaza, the biggest lawn
  (371 m², u +31 → +67), a lamp, and the densest surviving elms.

### 2.5 Recognition cues (ranked)

1. **The oval outline.** 6.8:1, curved, 45° to everything around it. Drawn by the
   historic kerb, which is the only 1854 fabric left.
2. **The single meandering promenade** of oblong tablets, widening into plazas.
3. **The Shout** — a perfect circle in plan, undulating in section, floating on its mound.
4. **The six long curved seat walls** holding grade along the path.
5. **The perimeter canopy ring** over the bio-retention beds, with lawn gaps in the middle.
6. **Colour**: green field, bone path, one anthracite circle, teal edges.

### 2.6 Miniature translation

The park is 159 m long and will be seen from 300–500 m at 25–35° down. What survives at
that distance is outline, value contrast and rhythm. The translation therefore:

- **keeps** every measured plan position — the path centreline, the wall alignments, the
  bed, lawn and playground polygons, the Shout's circle, and the 20 tree positions;
- **compresses** the ground into five clean value steps — dark plate, mint lawn, teal
  bed, bone path, sand playground — instead of the real design's dozen paving tones;
- **exaggerates** five things, each recorded in REFERENCE.md with this justification:
  1. **Path tablets 2.6 m long** instead of the real ~1.2 m, so the popsicle-stick rhythm
     survives at camera distance (style bible §9). ~72 tablets instead of ~155, which is
     also half the triangles.
  2. **Tree crowns generously sized** (5.5–8.0 m diameter) so the perimeter reads as a
     continuous canopy ring, which is what the aerial shows and what 20 mapped points
     alone would not produce (§12: crowns interpenetrate into one canopy volume).
  3. **The Shout's tubes at 0.45 m diameter** instead of the real ~0.15 m, so the circle
     is legible at all (§9: enlarge what carries meaning and would otherwise vanish).
  4. **The kerb proud by 0.12 m** and a half-tone lighter than the plate, so the oval
     outline reads from directly above.
  5. **Furniture ~15% oversized** — benches, tables, bike racks — for scale-cue legibility
     (§14).
- **drops** everything below that threshold: paving joints, the nets' individual cords,
  the drainage inlets, the irrigation, the plant species inside the beds, signage.

### 2.7 Massing recipe

Everything is a closed solid with real thickness, stacked in Z so that nothing is
coplanar with anything else and nothing z-fights the baked landcover (which sits at
+0.06 m above terrain).

| Level | z (m) | Element | Material |
|---|---|---|---|
| plate | 0.00 → 0.34 | the whole oval, the park's earth body; its side wall is the historic rounded kerb | `Toy_stone`, wall `Toy_stone` |
| kerb | 0.34 → 0.46 | a 0.45 m band inset from the boundary — draws the oval | `Toy_cream` |
| beds | 0.34 → 0.62 | thirteen bio-retention beds, measured polygons | `Toy_teal` |
| path | 0.34 → 0.50 | ~72 tablets along the 188 m centreline, 2.6 m long, width tracking the real 2.5–6.5 m thickening; plus nine entry stubs | `Toy_cream` |
| path glow | 0.50 → 0.52 | a thin shell on each tablet — **the hero night state** | `Toy_cream_Glow` |
| lawns | 0.34 → crowned | five lawns, crowned 0.75–1.30 m at their centres (the "gently sloping meadows" and the central hillock) | `Toy_mint` |
| walls | grade → +0.45 | six walls swept along their measured polylines, 0.35 m thick, with a cap | `Toy_stone`, cap `Toy_cream` |
| mound | 0.34 → 1.34 | the playground mound, following the Shout's curvature | `Toy_sand` |
| surfacing | mound top | poured surfacing disc inside the playground polygon | `Toy_sand` |
| Shout | +0.6 → +3.0 above the mound (crest **4.34 m**) | two 0.45 m tubes swept side by side around the 11.8 m circle, sinusoidally undulating, three full waves | `Toy_roofd` |
| nets | between the tubes | four thin slabs, flat-shaded, no transparency | `Toy_ink` |
| nest swing | +1.1 | one disc on two hangers, the play area's saturated accent | `Toy_coral` |
| furniture | 0.34 → 0.80 | 15 benches, 13 tables, 3 picnic tables, 4 bike racks, 7 waste baskets, 1 fountain | slats/tops `Toy_rust` (thermally modified wood), frames `Toy_steel` |
| lamps | 0.34 → 5.50 pole, 5.50 → 5.90 head | four straight-mast standards at measured positions | pole `Toy_steel`, head `Toy_gold` |
| lamp glow | head shell | thin proud shell | `Toy_gold_Glow` |
| trees | trunk 0.34 → 4.6, crown 4.0 → **15.00** | 20 measured + ~14 derived infill (2.15 risk 2); four silhouette families | trunk `Toy_steel`, crown `Toy_verdigris` |

**Tree families** (differentiated by silhouette, not by leaf — style bible §12):

| Family | Count | Silhouette | Crest |
|---|---|---|---|
| American elm | 8 | tall narrow vase, stout trunk to 4.6 m then a high upright crown | 13.5–15.0 m |
| London plane (pollarded) | 16 | stout trunk to 3.6 m ending *inside* a broad flat-topped crown | 10.0–12.5 m |
| Silver dollar gum | 3 | open, taller, narrower crown, higher branch point | 12.0–14.0 m |
| Olive / low broadleaf | 7 | low three-limb dome, 5.5 m crown on a short trunk | 6.0–7.5 m |

The pollard is the crown character of this park and it has a known failure mode: in
`civic-center-plaza`'s first build the trunk stopped 4 m below the crown and every tree
read as a crown floating over a stump. **The trunk must reach into the crown.**

### 2.8 Materials and palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `d9d2c2` | ground plate, kerb base, seat walls |
| `Toy_cream` | `f2ede3` | path tablets, wall caps, kerb — a half-tone lighter than the plate so both read |
| `Toy_cream_Glow` | `f2ede3` | the lit path — hero night state |
| `Toy_mint` | `8fd0a8` | the five lawns |
| `Toy_teal` | `3fa8a0` | the thirteen bio-retention beds — the one saturated ground colour, and defensible: these are drought-tolerant succulent-and-grass plantings, not turf |
| `Toy_verdigris` | `9fb8a8` | every tree crown — greyer than the lawns on purpose, so the canopy separates from the grass from directly above |
| `Toy_steel` | `9aa0a6` | tree trunks (London plane and elm bark is pale mottled grey), lamp poles, furniture frames |
| `Toy_sand` | `ece4d4` | playground mound and surfacing |
| `Toy_roofd` | `45454a` | the Shout's tubes — the manufacturer's "modern, almost industrial colour" |
| `Toy_ink` | `3a3530` | the nets, contact-shadow lines |
| `Toy_rust` | `a86444` | bench slats and table tops — the design's thermally modified wood |
| `Toy_coral` | `e8735a` | the nest swing, the one warm accent, all of it inside the play circle |
| `Toy_gold` | `caa64a` | lamp heads |
| `Toy_gold_Glow` | `caa64a` | lamp heads at night |

Fourteen materials, all on-palette. No `Toy_body` (landmarks are never tintable).

**Night state.** The hero is the **path**: at night South Park reads as a single lit
curve drawn through a dark canopy, which is exactly what the 2017 lighting scheme does.
Supporting accents are the four lamp heads. Lawns, beds and crowns go dark. Nothing else
glows — in particular the play structure does not, because it is not lit in reality and
because a second bright object would compete with the curve that identifies the place.

### 2.9 Top surface

The top view must resolve into six shapes, in this order of legibility:

1. the oval outline (kerb);
2. the bone ribbon of the path, corner to corner, with three plaza thickenings;
3. the anthracite circle at u −36 on its sand disc;
4. five mint lawn panels;
5. the teal beds banding both long edges;
6. the grey-green crowns breaking the outline all round.

If any of those six is not immediately readable in the top render, the asset is not
finished.

### 2.10 Scope

**In:** everything inside the kerb line (2.7). **Out:** the South Park street loop, its
sidewalks, bulb-outs and chicanes; the surrounding buildings (seven of them are already
landmarks); people; vehicles. The pipeline bakes the street and the sidewalk.

### 2.11 Triangle budget

| Element | Estimate |
|---|---|
| ground plate + kerb ring | 400 |
| five lawns, crowned | 700 |
| thirteen beds | 650 |
| ~72 path tablets + 9 stubs + glow shells | 2,000 |
| six seat walls (swept polylines, 108 segments) | 1,000 |
| playground mound + surfacing | 350 |
| the Shout: two swept tubes, 3 waves, 8-gon section, 48 segments each | 1,600 |
| nets, nest swing, climbing plates | 300 |
| ~34 trees (8-gon trunk frustum + two-tier crown) | 3,600 |
| 15 benches, 13 tables, 3 picnic tables, 4 bike racks, 7 baskets, 1 fountain | 1,100 |
| four lamps + glow shells | 300 |
| **Total** | **~12,000** |

Cap: **12,000**. Hard repo limit is 30,000 for a standard landmark (`PERF-PLAN` #9); this
sits well inside it, which matters because the asset also has to fit the shared 400k
batch alongside the seven neighbouring South Park landmarks that stream in with it.

### 2.12 Manifest entry (as shipped)

```json
{
  "id": "64-south-park",
  "file": "64-south-park.glb",
  "anchor": [-122.3939704, 37.7815903],
  "targetHeightM": 21.0415,
  "cat": 0,
  "name": "South Park",
  "estimated": true,
  "dims": [122.4585, 121.0471, 21.0415],
  "tris": 11436,
  "loadRadius": 2500
}
```

`targetHeightM` is the model's **vertical extent**, not an architectural height, because
the asset is draped (2.15 risk 9) and the loader's scale is `targetHeightM / bbox height`
— it has to land on 1.0, and it does: the app logs `uniform x1.0000 at 3830, -1281`.
`estimated: true` on both counts: the extent contains a tree crest no source establishes
(2.15 risk 1). `dims` is the axis-aligned box; the oriented footprint is 159.51 × 23.51 m.
`loadRadius` is the default rule, `max(2500, targetHeightM × 30) = 2500`; `alwaysLoaded`
would be wrong, this is a ground asset, not a skyline piece. Beyond the radius the
stand-in is bare baked landcover with no trees (they are cleared, 2.13), which is
illegible at 2.5 km.

### 2.13 Integration notes (for later, not this task)

**Case B** — new landmark. It needs a `pipeline/lib/landmarks.mjs` entry and a tile
re-bake.

```js
{
  id: '64SouthPark',
  name: 'South Park',
  lon: -122.3939704,
  lat: 37.7815903,
  height: 15.0,
  exclude: <MEASURE IT>,
  clearTrees: true,
  clearTreesRadius: <MEASURE IT>,
  camera: { distance: 400, yaw: 315, pitch: 24 },
}
```

Three things must be measured against the committed bake input, not reasoned about:

1. **`exclude` (the buildings job).** Expected to be **very small or absent** — this is a
   park, and the procedural builder should have nothing inside it. But the surrounding
   row is party-wall construction with the tightest exclusions in the file (101 South
   Park `exclude: 4`, 165 South Park `1.3`, 171 South Park `2`), and the nearest sibling
   *anchor* is only 40.8 m away. The park's own half-length is 79.8 m, so the usual
   half-diagonal rule would delete the entire block including houses that have no GLB and
   would leave holes no asset fills. Measure the nearest baked footprint **vertex** (not
   centroid) to the park boundary, per the method 505VanNess established, and size from
   that. If a footprint does intrude, prefer `extraExclusions` circles over one big radius.
2. **`clearTreesRadius` (the trees job).** Required and **must be set explicitly**:
   `treeblockers.mjs` falls back to `l.exclude`, and if `exclude` ends up absent the
   radius is `undefined` and no trees are cleared at all. The park is `leisure=park`, so
   the landcover scatter drops procedural lollipops the length of it, standing among the
   hand-modelled canopy and looking like a different world. Covering the whole park needs
   ~80 m. **Count trees at candidate radii — inside the park versus outside it — exactly
   as `civicCenterPlaza` did** (that entry was first set to 60 m on an unmeasured theory
   and the theory was wrong). Note the shape problem before you start: a circle is a poor
   fit for a 6.8:1 lozenge, so this radius will cost street trees on all four sides. If
   the count is unacceptable, the honest options are a smaller radius with procedural
   trees surviving at the two ends (recorded as a deliberate decision), or a pipeline
   change to support an oriented rectangle. Do not silently pick one.
3. **The camera yaw.** `yaw 315` puts the eye to the **south-west** (app yaw = 180 − true
   bearing; 180 − 315 = −135 = 225°), looking north-east **along** the park's axis with
   the Shout nearest the camera — the one composition that explains a 160 m lozenge.
   `592Third` is the cautionary tale: its yaw was derived on paper, shipped, and turned
   out to face two blank party walls. **Render it before believing it.**

**Batch mode applies.** A Case B re-bake rewrites ~600 generated files under
`app/public/tiles/` and `api/_data/` whatever the landmark was. Run the bake, do the full
QA on it — a Case B landmark cannot be judged without its clearance applied — then
`git checkout -- app/public/tiles api/_data` and commit source only, per
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

**Streaming check.** This makes eight landmarks on one 160 m oval. After integration run
`node pipeline/landmark-streaming-check.mjs` against a build: eight assets sharing one
`loadRadius` centre is the densest cluster in the manifest and the procedural fallback
would hide a loader failure from the eye.

### 2.14 Validation checklist

- [ ] Binary GLB, real metres, applied transforms, no negative scales
- [ ] ground plate top is exactly 0.34 m above the terrain **along its whole length**
      (the draped equivalent of `min_z ≈ 0`), ground-plate XY centre within 0.5 m of the
      origin
- [ ] `targetHeightM` equals the model's vertical extent to 0.01 m, so the loader's
      scale is 1.0
- [ ] tallest crest is 15.00 ± 0.01 m **above its own ground**; `max_z` equals crest +
      terrain at whichever tree actually peaks (not the tallest tree)
- [ ] Oriented footprint 159.51 × 23.51 m ± 0.5 m; AABB ≈ 117.1 × 115.7 m (the 45.47°
      heading, not a scale error)
- [ ] The Shout's ring is a circle 11.8 m across, centred at (u −36.03, v −1.29), and its
      crest is 4.34 m
- [ ] Path length 188 m ± 2 m along the measured centreline; every tablet inside the kerb
- [ ] Seat walls total 370 m ± 5 m over six runs
- [ ] Trees: the 20 measured positions present within 0.05 m; every derived infill listed
      in `data/park_uv.json` with its rule
- [ ] ≤ 12,000 triangles; ≤ 500 KB compressed
- [ ] All materials `Toy_*` and in the palette; no textures, no transparency, no `Toy_body`
- [ ] `_Glow` materials present, every glow surface a thin shell proud of an opaque
      parent, day colours matching their non-glow neighbours
- [ ] No cameras, lights, animations, armatures, constraints, or foreign geometry
- [ ] Per-object signed-volume normals test clean; whole-model ray residual ≤ 0.15%
- [ ] Top view resolves into the six shapes of 2.9, in that order
- [ ] The Shout is at the **south-west** end and the big lawn at the north-east — the
      mirror check (2.3)
- [ ] Night render shows one lit curve through a dark canopy, not a glowing slab

### 2.15 Open questions and risks

1. **The height datum is a tree, and no source gives its height.** `targetHeightM = 15.0`
   is the modelled crest of the tallest American elm. The 2015 HortScience survey
   measured trunk diameter, not height; OSM tags no height on any of the 20 nodes; the
   2017 works replaced 30 of the trees. 15.0 m is *inferred* from DBH (elms 16½–33"),
   from the pollard-and-topping history (attachments at 8–12 ft, topping at 12–15 ft,
   plus a decade of regrowth), and from the aerial, where the canopy reads at or just
   below the roofs of the 3–4 storey row around it (181 South Park 16.5 m, 188 South Park
   15.93 m, 171 South Park 12.6 m — all measured, all already in the manifest).
   **The error is contained**: because the build normalizes `max_z` to exactly 15.00 and
   the loader scales by `targetHeightM / measuredHeight`, the scale lands at 1.0 and the
   plan dimensions stay exact whatever the trees really are. A wrong number here makes
   the trees wrong, not the park. Mark the manifest entry `"estimated": true`, drive the
   crest from a named constant, and assert it in the validator so it is a two-minute
   change if evidence turns up.
2. **OSM maps 20 trees; the park has roughly twice that.** The Chronicle records 18 aged
   elms and sycamores retained plus 24 mature trees added, and the aerial shows a
   near-continuous perimeter canopy that 20 crowns cannot produce. The build therefore
   places the 20 **measured** positions and then a **derived** infill by an explicit rule
   — one tree at the midpoint of every gap longer than 14 m along the two long
   garden-bed edges, ~14 trees — with every derived position written into
   `data/park_uv.json` and labelled. This is the one place the asset departs from
   measured data, it is deliberate, and it is bounded: it replaces the procedural scatter
   that `clearTrees` removes. If it offends, the fallback is 20 trees and a broken ring,
   which is worse and should be a recorded decision, not a silent one.
3. **Area disagrees across sources**: 3,478 m² measured from the OSM polygon, ~34,000
   sq ft (3,159 m²) per Rec & Park, 1.2 acres (4,856 m²) per Fletcher Studio, one acre
   per TCLF. The model is built on the OSM polygon because that is the polygon the
   pipeline's landcover and exclusion already use, so the model and the baked city agree
   with each other even if both differ from the published figures. Recorded, not resolved.
   (Fletcher's 1.2 acres almost certainly includes the street loop, which is not in scope.)
4. **The mounding is inferred.** "Gently sloping meadows", "a grassy hillock toward the
   centre" and a mound under the play structure are documented in words and visible in
   photography, but no source gives grades. The lawn crowns (0.75–1.30 m) and the 1.0 m
   playground mound are *estimated* from photography. They matter: the mound is what
   makes the Shout appear to float, which is the effect the designers and the
   manufacturer both describe as the point of it.
5. **The Shout's wave count and phase are inferred.** The manufacturer gives the
   envelope (0.6 → 3.0 m, perfect circle in plan, two tubes side by side, six posts below
   grade) but not the number of undulations. Three full waves is read from the
   installation photography. If the photography says otherwise, change the constant —
   the circle and the envelope are what carry the recognition, not the wave count.
6. **`docs/asset-plans/README.md` says parks are planned in `docs/plans/parks/`.** That
   rule exists because a park is landcover + scatter + a few hero assets, not one GLB.
   South Park is treated as a landmark on `civic-center-plaza`'s argument, with one
   difference worth stating plainly: Civic Center Plaza is a hardscape with **no natural
   component**, and South Park is not — it has lawns, beds and a canopy. What justifies
   it here is that the 2017 park is a *designed object at a surveyed layout*, small
   enough (3,478 m²) and singular enough that scatter cannot produce it; and that seven
   of the buildings that ring it are already landmarks, so leaving the middle procedural
   would put a lollipop-scattered green blob inside a hand-built block. If the parks
   pipeline later grows the ability to bake a designed landscape, this asset is a
   candidate to migrate.
7. **The kerb is the oldest thing here and the least documented.** The Chronicle says the
   rounded curbs date to the 1850s and are almost all that survives. No source gives
   their profile or height. Modelled as a 0.45 m band standing 0.12 m proud, which is
   both a plausible kerb and the device that draws the oval from above. If that reads as
   too heavy in the top render, thin the band before lowering it — the outline is the
   first recognition cue and losing it costs more than an over-scaled kerb does.
9. **The park is on a 6.11 m slope, and the loader does not know.** This is the largest
   correction the build made to this plan, and it was found only in the running app.
   `placeGeneric()` seats a landmark by a single `sampleElevation()` at the anchor, which
   is right for a compact building — a hillside building buries its base uphill, exactly
   as the real one does — and wrong for an asset that IS the ground. Flat, South Park was
   buried 2.9 m at the Second Street end and floating 3.2 m at Third; from above, the
   whole north-east half had vanished under the baked landcover with only the tree crowns
   showing. The asset is therefore draped, which costs two contract deviations, both
   deliberate and both asserted in the validator rather than waved through:
   `min_z` is negative, and `targetHeightM` carries the vertical extent rather than an
   architectural height. Anything else that ships a large ground-plane asset in this city
   will hit the same wall; the alternative is a loader change to drape at placement time,
   which is a bigger decision than one landmark should make.
10. **The park is a live site.** OSM's furniture survey is from 2017–2018 with a few 2023
   additions (the covered outdoor seating way `1169236104`, the `South Park Commons`
   building across Brannan). Confirm against recent imagery which elements are still
   present before modelling them, especially the picnic sites and the bike racks.
