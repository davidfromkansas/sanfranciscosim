# Golden Gate Park — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Golden Gate Park |
| Slug | `golden-gate-park` |
| OSM | `way/158602261` |
| Anchor (lon, lat) | `-122.480746, 37.768522` |
| Area | 404.5 ha |
| Bounding span | 5076.2 × 1161.7 m (E–W × N–S) |
| Oriented box | 942.3 × 5028.8 m, long axis 85.7° from east |
| Elevation | 6.9–129.2 m (relief 122.3 m, mean 56.9 m) |
| Steepest 50 m grade | 58.3% |
| Baked landcover today | grass 91.7%, trees 3.1%, water 2.2%, pitch 2.2%, unclassified 0.6% |
| In `NAMED_PARKS` | yes — `goldenGatePark` (`pipeline/lib/landmarks.mjs`) |
| Effort | Large. Engine work (Layer A) plus 6–8 hero assets; the biggest park job in the set. |

**In one sentence:** a 5 km dark-green forested corridor cut straight through the Sunset grid, museum-dense and formal at its eastern end, pastoral and open at its western end, ending at the ocean with two windmills.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Golden Gate Park for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Golden Gate Park read, from the app's high three-quarter diorama camera, as
a 5 km dark-green forested corridor cut straight through the Sunset grid, museum-dense and formal at its eastern end, pastoral and open at its western end, ending at the ocean with two windmills.

This is **not** a single-GLB job. A park is ground, planting and a handful of
hero objects, so the work splits into three layers. Deliver them in order and
stop at any gate that fails.

## Read first (in this order)

1. `AGENTS.md` — iron rules. Rule 2 (draw calls < 300, 60 fps, no per-frame
   allocation), rule 3 (procedural fallback is a guarantee), rule 5 (real
   coordinates, real heights — style exaggeration happens in authoring, never
   in placement).
2. `docs/styles/miniature-toy.md` — the art gate for everything below,
   especially planting, ground and landscaping.
3. `docs/plans/parks/README.md` — the shared park engine spec. It defines the
   landcover kinds, tree-species encoding, path tier and density overrides that
   several parks need. **Implement engine changes there, once, not per park.**
4. `.agents/skills/sf-asset-check/SKILL.md` — the GLB contract for every hero
   asset in Layer B.
5. `.agents/skills/testing-sf-3d/SKILL.md` — dev loop, key bindings,
   `window.SF`, and the software-GL gotchas in this browser.
6. This file's Part 2 — the measured dossier. Treat its numbers as the starting
   point and re-verify anything it flags.
7. The code you are about to change: `pipeline/landcover.mjs` (`classify()`,
   `scatterTrees()`, `handlePolygon()`), `pipeline/lib/classes.mjs`
   (`LAND_KINDS`), `pipeline/lib/landmarks.mjs` (`NAMED_PARKS`, `VIEW_PRESETS`),
   `pipeline/toy.mjs` (landcover section, `TREE_MULTIPLIER`), and
   `app/src/city.js` (`toyTreeArchetype()`, the tree `InstancedMesh` loop).

## What the park must read as

- **A corridor, not a blob.** 5.03 km long by 942 m wide, long axis 85.7° from east — essentially due east–west, three Sunset blocks deep, running from Stanyan Street to Ocean Beach.
- **Dark forest, not lawn.** The interior canopy is the park's colour identity; today it bakes 91.7% flat `grass` and only 3.1% `trees`, which is the single biggest fidelity gap in this plan.
- **Two halves.** East (Stanyan → about 19th Ave) is museum-dense and formal: Conservatory, Music Concourse, de Young tower, Academy green roof, Japanese Tea Garden, Blue Heron Lake with Strawberry Hill rising to 129 m. West is pastoral and open: Polo Field, Bison Paddock, Chain of Lakes, windmills and the tulip garden at the ocean end.
- **JFK Promenade** as a continuous car-free ribbon threading the eastern half.
- From the 9 km hero camera it must read as one unbroken dark-green bar; from 800 m it must resolve into the two halves.

## Layer A — ground and planting (the biggest and most important layer here)

1. **Fix the forest.** `classify()` in `pipeline/landcover.mjs` maps `leisure=park` to `KIND.grass`, and the grass polygon for Golden Gate Park covers the whole park, painting over the 30-odd `natural=wood` polygons inside it. Result: 91.7% grass. Implement the park-interior forest rule from `docs/plans/parks/README.md` §E4 so the GGP interior bakes as `trees` with mown `grass` reserved for the meadows, concourse lawns, Polo Field and the athletic fields. Do not simply reorder polygon painting and hope — verify with the landuse raster after the bake.
2. **Species.** Golden Gate Park's canopy is Monterey cypress, Monterey pine and blue gum eucalyptus, not generic lollipops. Implement the species encoding in README §E3 and weight the GGP interior toward `cypress` and `eucalyptus`, with broadleaf around the Music Concourse and palms only where they really are (the Concourse and Conservatory Valley).
3. **Density.** Interior forest at the `trees` rate (one per 90 m², ×1.5 in the toy tier); meadows and the Polo Field keep the sparse park rate. From the diorama camera the canopy must close — you should not see mown ground between trunks in the interior.
4. **JFK Promenade and the main drives.** Bake the park's named drives as ribbons per README §E5, with JFK Promenade (`John F. Kennedy Drive`, car-free east of Transverse) rendered as a pale `pathdg`/paved promenade rather than a charcoal street. This is the one path that must be legible at city scale; the minor trail network can stay implied.
5. **Water.** Blue Heron Lake (formerly Stow Lake) is a ring around Strawberry Hill — the lake must bake with the island as a hole, not as a filled disc. Spreckels Lake, Elk Glen, Lloyd, Metson, Lily Pond and the Chain of Lakes all already carry `natural=water`; confirm each survives the bake and sits at its own local water level, not at y=0.
6. **Ground texture at the edges.** The park's north and south edges are hard, straight streets (Fulton and Lincoln). Keep the boundary crisp — the contrast between the grid and the green bar is the whole silhouette.

## Layer B — hero assets

Golden Gate Park carries more hero assets than any other park. Three already have full asset plans and must not be re-researched.

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| de Young Museum | `de-young` | `-122.4681752, 37.7718982` | 158.3 × 158.5 m | plan exists — `docs/asset-plans/de-young.md` |
| California Academy of Sciences | `cal-academy` | `-122.4662432, 37.7698424` | OSM `height=11`, see plan | plan exists — `docs/asset-plans/cal-academy.md` |
| Conservatory of Flowers | `conservatory-of-flowers` | `-122.4601775, 37.7725877` | OSM `height=15` | plan exists — `docs/asset-plans/conservatory-of-flowers.md` |
| Dutch Windmill | `dutch-windmill` | `-122.509414, 37.77044` | 18.3 × 18.1 m, OSM `height=13` | **new** — needs an asset plan |
| Murphy Windmill | `murphy-windmill` | `-122.508686, 37.765009` | 21.3 × 21.0 m, OSM `height=10` | **new** — needs an asset plan |
| Spreckels Temple of Music (bandshell) | `spreckels-temple` | `-122.46857, 37.769846` | 54.2 × 20.0 m, OSM `height=12` | **new** — needs an asset plan |
| Japanese Tea Garden pagoda + gate | `japanese-tea-garden` | `-122.46999, 37.77003` (garden centroid, verify) | garden ≈ 1.6 ha | **new** — small cluster, not one building |
| McLaren Lodge | `mclaren-lodge` | `-122.454766, 37.771858` | 24.8 × 34.0 m | optional — small but marks the Stanyan gateway |
| Blue Heron Lake Boathouse | `blue-heron-boathouse` | `-122.477108, 37.770609` | OSM `height=6` | optional |
| Beach Chalet | `beach-chalet` | `-122.510218, 37.769473` | verify | optional — closes the ocean end |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Keep the `goldenGatePark` entry in `NAMED_PARKS` and verify it still matches a baked polygon (`landcover.mjs` reports `missingParks` — it must stay empty).
2. Add two `VIEW_PRESETS` cameras, not one: an eastern museum view (about `-122.4680, 37.7705`, distance 700 m) and a western pastoral view (about `-122.4950, 37.7685`, distance 900 m). A single centroid camera cannot show what makes this park recognisable.
3. Bison Paddock (`way/161707029`, about `-122.49812, 37.76971`): a fenced pale-grass rectangle in the western half. Model the enclosure, not the animals, unless the prop budget allows a handful of dark instanced blocks — decide from the diorama camera and record the decision.
4. Polo Field (`way/476267889`, 518 × 219 m oriented box, 10.3 ha): a flat oval track with an inner pitch. It is the largest single readable shape in the western half; bake it as `pitch` inside a `paved`/`pathdg` track ring rather than modelling a stadium.
5. Music Concourse: a sunken formal rectangle (133 × 278 m oriented box) with the bandshell at one end and the two museums facing each other across it. Its pollarded plane-tree grid is a signature — use a regular grid of small canopies here, in deliberate contrast to the scattered forest everywhere else.
6. Queen Wilhelmina Tulip Garden (`-122.509222, 37.77029`, 1,101 m²): the one place in the park where saturated flower-bed accents are correct. Keep them to this plot and the Rose Garden.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: the `landcover`+`toyland` payload for the ~30 cells this park covers may not more than double, even with the denser forest. If it does, reduce tree density in the western half before touching the eastern half.
- Every hero GLB stays inside the landmark triangle cap (27,000) on its own.
- No new runtime dependency, no paid service, no build-time data fetch.

## Re-bake and verify

```
cd pipeline && npm install
npm run download            # only if pipeline/data/ is absent (hundreds of MB, gitignored)
npm run landcover && npm run validate && npm run toy
```
For the fast dev loop, note that `toy.mjs --cells=` only accepts the named keys
in its own `TEST_CELLS` map (`downtown`, `sunset`, `mission`, `russianhill`), so
add an entry for this park's anchor and bake that one cell:
`goldengatepark: [-122.4807, 37.7685]` (and a second, `ggpwest: [-122.5050, 37.7690]`, since the park spans ~30 cells)
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- Hero camera (`0`): the park reads as one continuous dark-green bar across the western half of the city, clearly darker than surrounding blocks.
- Eastern preset: Conservatory, Music Concourse, de Young tower and the Academy roof all read as distinct objects in one frame.
- Western preset: Polo Field oval, Bison Paddock, Chain of Lakes and the two windmills are all identifiable.
- Blue Heron Lake has an island, not a disc, and Strawberry Hill rises out of it.
- JFK Promenade is followable end to end at 400 m altitude.
- Night: the park goes properly dark — it is one of the few large unlit areas in the city, and that contrast is a feature.

Also verify the fallback (AGENTS rule 3): with the new landcover tier removed,
the app must still boot and the park must degrade to plain baked ground with one
console warning — never a hole, never a crash.

## Ship

- `cd app && npm run lint && npm run build`.
- Commit with author email `16072284+davidfromkansas@users.noreply.github.com`;
  stage only intended files; no `git add .`, no force-push, no amend.
- Open a PR with before/after screenshots from the diorama camera, day and
  night, and the deployed-site QA on https://sf-3d.vercel.app.
- Report the production URL first, then PASS/FAIL per gate above.

## Do not

- invent, move or rescale real features (rule 5) — every anchor in Part 2 is
  real and measured
- delete or bypass the procedural/baked fallback (rule 3)
- add per-tree, per-path or per-bench meshes — everything scatters through the
  existing instanced/merged paths
- model surrounding city blocks as part of this park; the baked city already
  provides them
- ship photoreal foliage, noisy detail or generic low-poly filler — the style
  bible governs
- do not re-research de Young, the Academy or the Conservatory — run their existing plans
- do not fill the park with individually placed prop meshes; the tree scatter and ground kinds carry it
````

---

## Part 2 — Research and design dossier

### 2.1 What was measured, and how

- Boundary geometry pulled directly from the OSM API (`/api/0.6/way|relation`), reprojected with the project's own tangent projection (`LON0 -122.4375`, `LAT0 37.77`), and reduced to an area, a bounding span and a minimum-area oriented box.
- Elevation, relief and the steepest 50 m gradient sampled from the repository's own committed terrain (`app/public/tiles/terrain.bin` via `manifest.terrain`) at points inside the boundary polygon — so the numbers match exactly what the app will render, not an external DEM.
- The current baked landcover mix sampled from `app/public/tiles/landuse.bin`, the same raster the terrain shader uses to tint distant ground.
- Feature inventory from an Overpass query over the park's bounding box, filtered to named leisure/natural/historic/man_made/building/tourism features; hero-feature footprints then re-fetched individually from the OSM API for their own anchors and oriented boxes.
- Anything not measured here — visual reads, massing choices, exaggerations — is marked as a design decision, not a fact.

### 2.2 Verified facts

| Field | Value |
|---|---|
| Area (OSM boundary) | 404.5 ha / 4,045,226 m² measured from `way/158602261` |
| Extent | 5,076 m east–west × 1,162 m north–south bounding span |
| Oriented box | 942.3 × 5,028.8 m, long axis 85.7° from east |
| Elevation range | 6.9 m to 129.2 m, mean 56.9 m (project terrain) |
| Relief | 122.3 m — almost entirely at the eastern end and Strawberry Hill |
| Steepest 50 m grade | 58.3% (Strawberry Hill flanks) |
| Strawberry Hill | `node/358807454`, `natural=peak`, `ele=129` |
| Blue Heron Lake | `relation/12908`, `ele=87`; renamed from Stow Lake in 2024 |
| Polo Field | `way/476267889`, 102,826 m², `ele=44` |
| Music Concourse | `way/30899551`, 35,487 m², `ele=75` |
| Dutch Windmill | `way/287921407`, `man_made=windmill`, `height=13`, `ele=11` |
| Murphy Windmill | `way/287927026`, `man_made=windmill`, `height=10`, `ele=6` |
| Named features found in bbox | 163 named elements, 2,547 footway/path ways |

### 2.3 Terrain

- The relief is lopsided: the eastern third climbs to Strawberry Hill (129 m) and the Conservatory terrace, while the western half is a gentle 6–45 m dune plain running down to Ocean Beach.
- The 58.3% steepest grade is Strawberry Hill's flank — the only genuinely steep ground inside the park, and it should read as a wooded knoll rising out of the lake.
- The Polo Field sits at `ele=44` on the western plain; the flatness there is real and should not be smoothed away or exaggerated.
- Terrain is already correct in the app (it comes from the same heightmap these numbers were sampled from). Layer A changes cover, not shape.

### 2.4 What the bake produces today

- The whole park bakes as one `leisure=park` polygon → `KIND.grass`, so 91.7% of the park's ground is mown-lawn green.
- Only 3.1% bakes as `trees`, from the handful of `natural=wood` polygons that survive the paint order.
- Trees still scatter across grass at the sparse park rate (one per 200 m², ×1.5 in the toy tier), so the park has trees but reads as a lawn with trees on it rather than as a forest.
- 2.2% water (the lakes are present), 2.2% pitch (the athletic fields), 0.2% sand.
- All trees use one lollipop archetype (`toyTreeArchetype()` in `app/src/city.js`) with three scale variants; there is no species variation anywhere in the city.
- The park's drives bake as ordinary charcoal streets; JFK Promenade is not distinguished from a road.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 25 m grid (6469 samples):

| Land kind | Share of park |
|---|---|
| grass | 91.7% |
| trees | 3.1% |
| water | 2.2% |
| pitch | 2.2% |
| unclassified | 0.6% |
| sand | 0.2% |
| scrub | 0% |

### 2.5 Recognition cues, ranked

1. The unbroken 5 km east–west dark-green bar through the street grid.
2. Dense closed canopy, distinctly darker than any other green in the city.
3. The museum cluster: de Young's twisting tower and the Academy's bumpy green roof facing each other across the Music Concourse.
4. Blue Heron Lake ringed around the wooded knoll of Strawberry Hill.
5. The pastoral west: Polo Field oval, open meadows, and the two windmills at the ocean end.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The full 5 km length and the hard, straight north and south edges against Fulton and Lincoln.
- The east-formal / west-pastoral gradient.
- Strawberry Hill as an island knoll inside its lake.
- The Music Concourse as a sunken formal rectangle with a tree grid.
- Real anchors for every hero object.

**Simplify**

- The 2,547 individual footway ways — bake only the named drives and JFK Promenade; imply the rest.
- The Botanical Garden's internal plant collections: one varied-canopy zone, not a plant list.
- The 30-plus statues and memorials: keep at most the Prayerbook Cross (17 m, tall enough to read) and skip the busts.
- The Chain of Lakes: three simple water shapes, not their real fringing detail.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Canopy density and canopy-colour contrast — the park should be conspicuously darker than the city.
- Tree height around the Panhandle and eastern edge, so the corridor reads as walled in from the street grid.
- The Music Concourse tree grid's regularity, to contrast the natural scatter.
- The tulip garden's colour, held to its real 1,101 m² plot.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Size / note |
|---|---|---|---|
| Park boundary | `way/158602261` | `-122.480746, 37.768522` | 404.5 ha |
| Blue Heron Lake | `relation/12908` | `-122.474313, 37.769031` | 530 × 363 m bbox, `ele=87` |
| Strawberry Hill | `node/358807454` | `-122.475527, 37.768541` | `natural=peak`, `ele=129` |
| Music Concourse | `way/30899551` | `-122.467332, 37.770794` | 35,487 m², oriented 133 × 278 m |
| Spreckels Temple of Music | `way/30896932` | `-122.46857, 37.769846` | 54 × 20 m, `height=12` |
| de Young Museum | `relation/1652482` | `-122.468528, 37.771585` | 158 × 158 m bbox, `height=13` |
| California Academy of Sciences | `way` (see asset plan) | `-122.4662432, 37.7698424` | `height=11` |
| Conservatory of Flowers | `way` (see asset plan) | `-122.4601775, 37.7725877` | `height=15` |
| Japanese Tea Garden | `way` (`leisure=garden`) | `-122.46999, 37.77003` (verify) | ≈1.6 ha |
| Polo Field & Stadium | `way/476267889` | `-122.492799, 37.768161` | 518 × 219 m, `ele=44` |
| Bison Paddock | `way/161707029` | `-122.498117, 37.769709` | fenced enclosure |
| Dutch Windmill | `way/287921407` | `-122.509414, 37.77044` | 18 × 18 m, `height=13` |
| Murphy Windmill | `way/287927026` | `-122.508686, 37.765009` | 21 × 21 m, `height=10` |
| Queen Wilhelmina Tulip Garden | `way/120483945` | `-122.509222, 37.77029` | 1,101 m² |
| Hippie Hill / Robin Williams Meadow | `way/272711313`, `way/417414585` | `-122.458085, 37.769824` | 4,513 m² |
| McLaren Lodge | `way/159924616` | `-122.454766, 37.771858` | 25 × 34 m |
| Kezar Stadium | `way/30675203` | `-122.456071, 37.766869` | 246 × 137 m, `ele=82` (just outside the boundary) |
| Spreckels Lake / Elk Glen / Lloyd / Metson / Lily Pond | `natural=water` ways | see `features.json` | already baked |
| Beach Chalet athletic fields | `way/27211224` | `-122.508883, 37.767372` | west end, `pitch` |

### 2.8 Ground and planting recipe

1. Ground base: the whole boundary as `trees` (forest floor) rather than `grass`.
2. Carve mown `grass` for: Music Concourse lawns, Hippie Hill/Robin Williams Meadow, Lindley and Marx meadows, Polo Field surrounds, Speedway Meadow, the Beach Chalet fields and the Conservatory Valley terrace.
3. `pitch` for the Polo Field interior, Big Rec diamonds, Beach Chalet soccer fields and the equitation field.
4. `water` for all named lakes, with Strawberry Hill as a hole in Blue Heron Lake.
5. `pathdg` ribbon for JFK Promenade plus the named drives; skip the rest of the trail network.
6. Tree scatter: `cypress`/`eucalyptus` weighted in the interior at forest density; broadleaf around the Concourse; a regular grid of small broadleaf at the Concourse itself; palms only at the Concourse and Conservatory Valley.
7. Flower-bed accents confined to the Tulip Garden, Rose Garden and Conservatory Valley.
8. Hero GLBs placed by the normal manifest route at their real anchors.

### 2.9 Palette

The park palette extends the project palette rather than replacing it. Colours
are flat, unlit-looking miniature paint, per `docs/styles/miniature-toy.md`.

| Use | Token | Hex | Notes |
|---|---|---|---|
| Mown lawn | `grass` | `5c7840` | the existing `LAND_KINDS.grass` |
| Meadow / dry grass | `meadowdry` | `8a8a52` | new; unirrigated western SF grass |
| Forest floor | `trees` | `33562e` | existing `LAND_KINDS.trees` |
| Eucalyptus canopy | `eucalyptus` | `4a6b46` | grey-green, taller and thinner than the default lollipop |
| Cypress / conifer canopy | `cypress` | `2f4a34` | dark, dense, columnar |
| Palm crown | `palm` | `6f8f4a` | brighter, sparse fronds |
| Path (decomposed granite) | `pathdg` | `c2ad8c` | warm sand-buff |
| Paved plaza | `paved` | `6b6b6b` | existing `LAND_KINDS.paved` |
| Sand / beach | `sand` | `c7b78d` | existing |
| Water | `water` | `1f4757` | existing |
| Tidal marsh | `marsh` | `6d7a4a` | new; olive-green, matte |
| Bare rock / chert | `rock` | `9a8f80` | new |
| Flower bed accent | `bloom` | `e8735a` / `d9a441` | style-bible coral and mustard, used sparingly |
| Sports surface | `pitch` | `4f7347` | existing |
| Hard court | `court` | `7a6a55` | new; tennis/basketball |

### 2.10 Hero asset list

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| de Young Museum | `de-young` | `-122.4681752, 37.7718982` | 158.3 × 158.5 m | plan exists — `docs/asset-plans/de-young.md` |
| California Academy of Sciences | `cal-academy` | `-122.4662432, 37.7698424` | OSM `height=11`, see plan | plan exists — `docs/asset-plans/cal-academy.md` |
| Conservatory of Flowers | `conservatory-of-flowers` | `-122.4601775, 37.7725877` | OSM `height=15` | plan exists — `docs/asset-plans/conservatory-of-flowers.md` |
| Dutch Windmill | `dutch-windmill` | `-122.509414, 37.77044` | 18.3 × 18.1 m, OSM `height=13` | **new** — needs an asset plan |
| Murphy Windmill | `murphy-windmill` | `-122.508686, 37.765009` | 21.3 × 21.0 m, OSM `height=10` | **new** — needs an asset plan |
| Spreckels Temple of Music (bandshell) | `spreckels-temple` | `-122.46857, 37.769846` | 54.2 × 20.0 m, OSM `height=12` | **new** — needs an asset plan |
| Japanese Tea Garden pagoda + gate | `japanese-tea-garden` | `-122.46999, 37.77003` (garden centroid, verify) | garden ≈ 1.6 ha | **new** — small cluster, not one building |
| McLaren Lodge | `mclaren-lodge` | `-122.454766, 37.771858` | 24.8 × 34.0 m | optional — small but marks the Stanyan gateway |
| Blue Heron Lake Boathouse | `blue-heron-boathouse` | `-122.477108, 37.770609` | OSM `height=6` | optional |
| Beach Chalet | `beach-chalet` | `-122.510218, 37.769473` | verify | optional — closes the ocean end |

### 2.11 Budget

- Landcover geometry barely changes — the same polygons, re-classified. The growth is the tree scatter: forest density (90 m²/tree) over most of 404.5 ha instead of park density (200 m²/tree) is roughly a 2.2× tree count for this park.
- Trees are one `InstancedMesh` per ground group, so the cost is instance-matrix memory and vertex throughput, not draw calls.
- If the frame rate at the western preset drops, cut density in the west (which is genuinely more open) before the east.
- Hero GLBs: 6–8 assets, each well under the 27,000-triangle landmark cap; the windmills and bandshell should each land nearer 3,000–6,000.

### 2.12 Integration notes

- `goldenGatePark` is already in `NAMED_PARKS`, so the landcover bake already checks that a polygon matches it.
- The three museum assets are separate landmark GLBs and follow `docs/asset-plans/INTEGRATION-PROMPT.md`; two of them (Cal Academy, de Young) are Case B and additionally need `pipeline/lib/landmarks.mjs` entries plus a re-bake.
- New hero assets (windmills, bandshell) are also Case B if they should clear baked footprints; the windmills stand alone in open ground, so their exclusion radius can be small (about 30 m).
- Engine changes in Layer A affect every park in the city — implement them once per `docs/plans/parks/README.md` and re-bake the whole city, not just these cells.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- `landcover.mjs` reports `missingParks: []` after the bake.
- The landuse raster inside the GGP boundary flips from ~92% grass to a forest-dominant mix; report the new percentages.
- Blue Heron Lake renders with its island.

### 2.14 Risks and open questions

- **Forest re-classification is the risky part.** Changing how `leisure=park` classifies affects every park in the city, not just this one. The README specifies a per-park override rather than a global rule for exactly this reason; a global change must be visually checked in Dolores, Alamo Square and Washington Square before shipping.
- Blue Heron Lake's measured area (107,806 m²) is larger than published figures for Stow Lake, because the relation's outer rings were summed including the island ring. Re-measure with proper hole handling before using it for anything numeric.
- The Japanese Tea Garden anchor above is taken from a garden polygon centroid and is not individually verified; verify before authoring.
- Tree density increases are the main performance risk in this whole plan set.
- Kezar Stadium sits just outside the OSM park boundary but reads as part of the park from the air; decide explicitly whether it is in scope.

### 2.15 Sources

- OpenStreetMap `way/158602261` (park boundary), `relation/12908`, `way/476267889`, `way/30899551`, `way/287921407`, `way/287927026`, `way/30896932`, `relation/1652482`, `node/358807454` — geometry and tags via the OSM API.
- Overpass API bbox query over the park (7,281 elements, 163 named) for the feature inventory.
- This repository: `app/public/tiles/terrain.bin` and `landuse.bin` for elevation and current bake state; `pipeline/landcover.mjs`, `pipeline/lib/classes.mjs`, `app/src/city.js` for the pipeline behaviour described above.
- Heights quoted as `height=` are OSM tags and are marked as such; verify any that drive a `targetHeightM` before authoring.
