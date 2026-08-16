# Civic Center Plaza — reference dossier

Research behind `civic-center-plaza.glb`. The asset plan
(`docs/asset-plans/civic-center-plaza.md`) is the starting point; this file records what
was re-verified for the build and what was corrected. **Where the two disagree, this file
and `REPORT.md` win.**

## 1. What this is

The 5-acre formal plaza immediately east of San Francisco City Hall, bounded by McAllister
Street (north), Larkin Street (east), Grove Street (south) and Dr. Carlton B. Goodlett
Place — formerly Polk Street — (west). It is divided by the former alignment of Fulton
Street, and the north block is the roof of a three-storey parking garage.

It is not a park in any natural sense. It is a designed hardscape: John Galen Howard's
1911 Beaux-Arts plaza, re-cut in Modernist terms by landscape architect **Douglas Baylis**
with Wurster, Bernardi & Emmons and SOM in **1956–58**, whose planting plan of rows of
pollarded London plane and olive trees is what the site still reads as today (the olives
were removed in 1998).

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OpenStreetMap via Overpass API (way `284764947`, relation `1735770`, Wikidata `Q49478335`) | The plaza polygon; 190 tree nodes; 35 flagpole nodes with heights and flag identities; six `landuse=grass` panels; the `surface=fine_gravel` central court; both playground polygons; the garage kiosk; the full footway network. **Every measured number in this dossier comes from this pull**, reprojected into the SF-SIM local tangent plane and then into the plaza frame. |
| Wikipedia, *Civic Center Plaza* | Acreage (4.53 acres; 4.53–5.38 per SF Rec & Park); the four boundary streets; the Fulton division; "two aisles of London plane trees flank an east–west pathway leading to City Hall"; Brooks Hall (1958, underground, connected to Bill Graham Civic Auditorium's basement); the garage (three storeys, 1960, 317 × 374 ft, 9 ft 3 in – 10 ft clear, Gould and Degenkolb); playground history (1993 north, 1998 south, renovated 2017–18 at $10 M as the Helen Diller Civic Center Playgrounds). |
| The Cultural Landscape Foundation, *Civic Center Plaza — San Francisco* | The 1911 Howard plan and the 1915 Howard / Meyer / Reid Beaux-Arts commission; Thomas Church's 1936 War Memorial Court (**not** this plaza); Douglas Baylis's 1956–58 Modernist redesign and its pollarded plane and olive planting, olives removed 1998; Halprin's 1975 UN Plaza on the eastern edge; the 2018 Helen Diller Playgrounds by Andrea Cochran Landscape Architecture with The Trust for Public Land; NRHP listing 1978 and National Historic Landmark designation 1987. |
| KQED, *Why is There a Texas Flag in Front of City Hall?* and the accompanying *Civic Center Plaza Flagpoles Historical Background* | The Pavilion of American Flags: 18 flags first raised on **Flag Day, 14 June 1964**, curated by Stanley Bergman on 18 poles that had stood bare for years. |
| parkerhiggins.net, *The 18 flags of San Francisco's Civic Center Plaza* | The individual flag identities, which match the OSM `flag:name` tags one for one — an independent confirmation that the OSM flagpole data is real survey work rather than a guess. |
| SF Planning, *Civic Center Cultural Landscape Inventory — Thomas Dolliver Church* | Church's actual scope in the Civic Center, for the record that he did not design this plaza. |
| `app/public/tiles/buildings/19_13.bin`, `19_14.bin` (this repo) | The exclusion-radius measurements in §8. This is the authoritative input for integration, not OSM. |

## 3. Verified dimensions and location

| | Value | How |
|---|---|---|
| Polygon area | 20,495 m² = **5.06 acres** | shoelace over the OSM ring |
| Oriented bounding box | **177.88 m × 121.48 m**, heading **9.06°** | minimum-area OBB over the ring |
| OBB centre | lon **−122.4176170**, lat **37.7794913** | reprojected from the OBB |
| Model anchor (bbox centre) | lon **−122.4176184**, lat **37.7794818** | OBB centre + the shift `recentre()` applies |
| Axis-aligned XY bbox | **145.61 × 192.62 m** | measured on the export |
| Height | **30.48 m** to the US flagpole finial | OSM node `7797674733` |
| Address | 355 McAllister Street, SF CA 94102 | OSM `addr:*` on the Civic Center Garage node `267294237` |

## 4. Orientation

The plaza sits on the Civic Center grid, 9.06° off north. The build authors everything in a
local frame and maps to world once:

```
u  = long axis, POSITIVE TOWARD THE SOUTH (Grove Street), bearing 170.94° true
v  = short axis, POSITIVE TOWARD THE WEST (City Hall),    bearing 260.94° true
u ∈ [−88.9, +88.9]   v ∈ [−60.7, +60.7]
```

The plaza has no "front" in the building sense; the contract's "front faces −Y" rule cannot
be honoured literally, and real-world orientation wins (AGENTS rule 5). The *ceremonial*
front is the west edge, on the City Hall axis. That is the direction the camera preset in
`REPORT.md` looks along.

## 5. What each side shows

- **North (McAllister).** The garage kiosk, the sunken ramp mouth at the notch in the plaza
  ring around u = −80, the north row of eight Pride flagpoles, and the long edge of the NW
  lawn. The busiest, least symmetric edge — the service end.
- **East (Larkin).** Both Helen Diller playgrounds presented end-on as two fenced colour
  blocks, with the NE and S strip lawns between them. The most colourful edge, and the one
  the Asian Art Museum and Main Library face.
- **South (Grove).** The mirror of the north — eight Pride poles, the SW lawn edge — with
  the 100 ft US flagpole rising behind. The tallest silhouette.
- **West (Dr. Carlton B. Goodlett Place).** The ceremonial front. The central court runs
  straight out of this edge toward City Hall's dome; the two big west lawns flank it
  symmetrically.
- **Above.** The design. Two dark bosque slabs, four bright lawn rectangles, a pale gravel
  bar across the middle, two colour-accented playground pads on the east, and two dotted
  lines of flagpoles. This is the view that has to work.

## 6. Recognition cues (ranked)

1. **Two dense bosques of flat-topped pollarded planes** flanking a central bar. Six rows,
   190 trees, ~3.2 m spacing. Nothing else in San Francisco reads like this from the air.
2. **The east–west axis pointing at City Hall's dome.**
3. **The double row of flagpoles** — a colonnade of masts.
4. **Four crisp geometric lawn panels**, symmetric about the central axis.
5. **The two playgrounds' colour** on the Larkin side, the only saturated accent.

## 7. Corrections to the plan's dossier

These were found while building and are the reason `REPORT.md` beats the plan.

0. **The whole plaza built mirrored east-west on the first pass**, and passed all 19
   automated contract checks that way. `data/plaza_uv.json` defines `+v = west`, making
   `(u, v)` left-handed in world space; the build compensated for the winding consequence
   by flipping `V_DIR` to east, which swapped the playgrounds onto the City Hall side and
   every lawn and walk with them. Fixed in `V_DIR` / `orient_for_world()` / `ngon_uv()`.
   **Anyone reusing this authoring frame should read the `V_DIR` comment before touching
   it.** Caught by the top render, not by the validator.

1. **The address in the original brief was 335 McAllister Street.** The plaza's own address
   is **355** McAllister. 335 geocodes to a bare address point on the north sidewalk.
   Same site; 355 is the number recorded.
1b. **Tree trunk colour.** Built first in `Toy_rust` (a86444). London plane bark is pale
   mottled grey-cream, and 190 saturated orange-brown trunks competed with the two
   playground pads in a composition whose whole point is that the playgrounds carry the
   only saturated accent (style bible §7). Moved to `Toy_steel` (9aa0a6), which also saves
   a material.

2. **Tree heights.** OSM tags every one of the 190 trees `height=4.5`, which is a bulk
   default, not a survey. Built at an 11.0 m crest with a 7.55–11.00 m crown, which is what
   pollarded planes of this age read as and what makes the bosques legible at the app's
   camera distance. This remains the largest visual assumption in the asset.
3. **The `Double L Excentric Gyratory` (George Rickey, 1982) is not in this plaza.** Its
   OSM node reprojects to v = −93 m, well east of the plaza's −60.7 m edge; it belongs to
   the UN Plaza / Fulton Street side. Dropped from scope. The plan already flagged this,
   and re-measurement confirmed it.
4. **Playground pads are raised, not recessed.** The plan's §2.7 called for pads recessed
   below the paving. Built raised to +0.42 m instead, because a recessed pad would sit
   *below* the scored joint grid at +0.32 m and the joints would float across it. Raised
   pads also read better from above. Deviation recorded.
5. **The scored joint grid is 14 m, not 6 m.** A 6 m grid over a 178 × 121 m deck is 50+
   lines and reads as noise from the app's camera. 14 m gives 12 lines each way — enough to
   stop the deck reading as a blank slab, few enough to stay a pattern.
6. **Walks are modelled one box per way, not segment-by-segment.** Every walk in the
   measured data is straight to within a metre over its full length, so a single box per
   OSM way is both accurate and ~4× cheaper.
7. **Bevels are spent selectively.** A 0.12/2 bevel multiplies a box's triangle count by
   about nine. Applied to the merged multi-solid objects (trees, flagpoles, lamps, benches,
   planters, people, fences, play kit) it cost 15,800 triangles for detail under one pixel
   and pushed the asset to 33,664 — over the 30,000 hard gate. Those objects ship
   unbevelled; their tapered profiles carry the soft read. The chunky single solids (deck,
   kiosks, ramp walls) keep the full bevel and the paving slabs take a token 0.05/1.

## 8. Integration measurements (for the integration pass, not this build)

Measured against the committed bake input, nearest **vertex** not centroid, per the method
`505VanNess` established:

| Footprint | Nearest vertex from the anchor | Area | Baked top |
|---|---:|---:|---:|
| garage kiosk | 67.8 m | 88 m² | 23.4 m |
| Grove-corner cafe | 74.2 m | 93 m² | 22.0 m |
| Pit Stop / small structure | 83.5 m | 10 m² | 22.5 m |
| **first neighbour to protect** | **109.9 m** | 6,165 m² | 62.0 m |

Exclusion window 83.5 < r < 109.9; **95 m** chosen. Note that the three plaza footprints
are single-storey kiosks the procedural builder extrudes to 22–23 m: three phantom towers
stand in the plaza in the current build, and **this asset cannot be judged before the
re-bake removes them.**

Tree scatter: the plaza is `leisure=park`, so the landcover scatter drops procedural trees
across it that would grow through the modelled bosques. See `REPORT.md` and the plan's
§2.13 for the `clearTrees` / `clearTreesRadius` recommendation.

## 9. Uncertainties carried into the build

1. **The height datum is one OSM tag on one thin pole** (`height=30.48`, a round 100 ft).
   The loader scales the entire 178 m plaza off it. Driven by the `Z_FLAG_US` constant and
   asserted in both the build script and the validator; the manifest entry is marked
   `"estimated": true`.
2. **Tree heights are inferred** (see §7.2).
3. **Pride flagpole heights are untagged**; built at 9.0 m from photography.
4. **Acreage disagrees across sources** (4.53 / 4.53–5.38 / 5.06 measured). The model uses
   the OSM polygon so that it and the baked city agree with each other.
5. **The site changes.** SF has repeatedly proposed and partly executed changes to Civic
   Center Plaza since 2020, and the OSM nodes carry `check_date` values spread across 2022
   and 2026. The Pride flagpoles are the newest and least documented feature here.
6. **Flags are modelled as abstract three-colour slabs with no devices.** The 18 historic
   flags have been edited by the city in recent years. Abstraction is both the correct
   style-bible call (§26) and the one that keeps this asset out of a live political
   argument.
