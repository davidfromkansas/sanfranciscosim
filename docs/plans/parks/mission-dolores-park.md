# Mission Dolores Park — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Mission Dolores Park |
| Slug | `mission-dolores-park` |
| OSM | `way/23871270` |
| Anchor (lon, lat) | `-122.427615, 37.759729` |
| Area | 6.4 ha |
| Bounding span | 212.4 × 356.5 m (E–W × N–S) |
| Oriented box | 345.3 × 187.3 m, long axis 85.7° from east |
| Elevation | 16–46.3 m (relief 30.4 m, mean 28.1 m) |
| Steepest 50 m grade | 21.1% |
| Baked landcover today | grass 93%, pitch 3.8%, unclassified 3.1% |
| In `NAMED_PARKS` | yes — `doloresPark` (anchor `-122.4271, 37.7596`) |
| Effort | Small–medium. No hero GLB required; it is a slope, a lawn, palms and a view. |

**In one sentence:** a bright, treeless, steeply raked green rectangle in the middle of dense colourful Mission blocks, with a palm row along its spine and the downtown skyline framed from its high south-west corner.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Mission Dolores Park for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Mission Dolores Park read, from the app's high three-quarter diorama camera, as
a bright, treeless, steeply raked green rectangle in the middle of dense colourful Mission blocks, with a palm row along its spine and the downtown skyline framed from its high south-west corner.

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

- **A raked rectangle.** 345 × 187 m oriented box, long axis 85.7° from east, 6.4 ha, with 30.4 m of relief across it and a 21.1% steepest grade. The slope *is* the park.
- **Bright, not dark.** It should read as the lightest green in the Mission, in deliberate contrast to Buena Vista's dark canopy a kilometre north-west.
- **Mostly open.** Trees are a perimeter and a palm row, not a canopy. Do not close it over.
- **Framed by colour.** The surrounding blocks are dense, low and colourful; the park is a hole punched in them.
- **The view.** From the high south-west corner the downtown skyline is unobstructed. That sightline is the park's identity and must be checked in-engine.

## Layer A — ground and planting (slope fidelity, palms, courts and paths)

1. **Verify the slope reads.** The terrain already carries the 30.4 m fall (16.0 m at the north-east corner, 46.3 m at the south-west); confirm the landcover drapes onto it without flattening. `triangulateDraped()` subdivides at `MAX_EDGE = 55` m — for a 6.4 ha park on a 21% grade that is coarse. Consider a smaller max edge inside steep park polygons (README §E6) so the lawn follows the hill instead of faceting across it.
2. **Palms.** The palm row along the central walk is the park's most photographed feature and there is no palm archetype in the app today. Implement the species encoding (README §E3), add a palm archetype (bare trunk, small sparse crown) and place palms *only* where they really are — the central spine and the north edge — not scattered.
3. **Perimeter trees.** A single ring of broadleaf canopy around the edges; keep the interior lawn clear.
4. **Courts and playground.** The tennis/basketball courts at the north end and the Helen Diller Playground (`-122.426874, 37.758732`) are already `leisure=pitch`/`playground`. Give the courts the new `court` kind (README §E1) so they do not read as more lawn; the playground gets a small accent-coloured patch.
5. **Paths.** The park's diagonal walks are legible at 6.4 ha. Bake them as `pathdg` ribbons (README §E5) — this is the smallest park in the set where paths clearly pay for themselves.
6. **Church Street tracks.** The Muni J-Church line runs along the west edge. Check whether the existing rail bake already draws it; if it does, leave it. If not, this is a rail-tier question, not a park question — record it and move on.

## Layer B — hero assets

**No hero GLB is required for this park.** Two related items:

| Item | Slug | Anchor (lon, lat) | Status |
|---|---|---|---|
| Mission Dolores Basilica |  `mission-dolores` | see `docs/asset-plans/mission-dolores.md` | plan exists — two blocks north, reads with the park |
| Public restroom / clubhouse | — | `-122.427751, 37.76079` | baked building, not a GLB |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Keep the `doloresPark` `NAMED_PARKS` entry; note its anchor (`-122.4271, 37.7596`) sits slightly east of the measured centroid (`-122.427615, 37.759729`) but is still inside the polygon, so the match check passes. Leave it unless you are re-baking anyway.
2. Add a `VIEW_PRESETS` camera at the high south-west corner (about `-122.42834, 37.75855`, elevation ~46 m) looking north-east at downtown, distance 1,200 m, pitch about 12°. This is the one preset that proves the park works.
3. Mexico's Liberty Bell monument (`-122.426272, 37.759819`) is small; include it only if a monument prop already exists in the vocabulary.
4. Consider a light scatter of instanced figures/blanket props on the upper slope if the lawn reads dead at the diorama camera — this park is defined by being full of people. Only if the prop system already supports it; do not build one for this.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: a 6.4 ha park; the payload change should be marginal. Palms and courts must not add draw calls.
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
`dolorespark: [-122.4276, 37.7597]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- The slope is visible from the diorama camera — the lawn clearly falls to the north-east.
- The palm row reads as palms, distinct from every other tree in the city.
- Courts read as a hard surface, not lawn.
- From the new preset, downtown is unobstructed above the park's high corner.
- The park is visibly brighter green than Buena Vista Park in the same frame.

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
- do not close the lawn over with trees
- do not add a hero building; this park does not have one
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
| Area | 6.4 ha / 64,434 m² (`way/23871270`) |
| Extent | 212 × 357 m bounding span; oriented box 345 × 187 m at 85.7° |
| Elevation | 16.0–46.3 m, mean 28.1 m, relief 30.4 m |
| Steepest 50 m grade | 21.1% |
| Low point | north-east corner (local `991, 959`) |
| High point | south-west corner (local `836, 1309`) |
| Current landcover | 93.0% grass, 3.8% pitch, 3.1% unclassified |
| Playground | Helen Diller Playground, `-122.426874, 37.758732` |
| OSM tags | `leisure=park`, `wikidata=Q11519`, SF Rec & Park listed |

### 2.3 Terrain

- The fall is diagonal: high at the south-west, low at the north-east, which is exactly why the south-west corner has the skyline view.
- 30.4 m over roughly 250 m of diagonal is a sustained 12% average with a 21% steepest pitch — steep enough to read strongly from the air if the mesh is subdivided finely enough.
- The terrain data is already right; the risk is the landcover mesh being too coarse to follow it.

### 2.4 What the bake produces today

- 93% of the park bakes as `grass`, which is broadly correct here — this is one of the few parks where the current classification is close.
- 3.8% bakes as `pitch` (the courts), which currently uses the pitch green rather than a hard-court colour.
- Trees scatter at the sparse park rate with the single lollipop archetype — no palms.
- The internal paths are not baked; the park is a plain green quadrilateral.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 5 m grid (2576 samples):

| Land kind | Share of park |
|---|---|
| grass | 93% |
| pitch | 3.8% |
| unclassified | 3.1% |

### 2.5 Recognition cues, ranked

1. The steep diagonal rake of a bright green rectangle.
2. The palm row along the central walk.
3. Dense, colourful low blocks pressed against all four sides.
4. The downtown skyline framed from the high south-west corner.
5. Courts and playground at the north end.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The real grade and its diagonal direction.
- The rectangle's crisp street-aligned edges.
- The open, treeless interior.
- The south-west sightline to downtown.

**Simplify**

- 74 path ways → the two or three main diagonals.
- Playground equipment → one accent patch.
- Individual bench and light furniture → omit or instance.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Lawn brightness, to separate it from every wooded park.
- Palm slenderness and height, so the row reads at distance.
- Court colour contrast.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Park boundary | `way/23871270` | `-122.427615, 37.759729` | 6.4 ha |
| Helen Diller Playground | way (`leisure=playground`) | `-122.426874, 37.758732` | north end |
| Mexico's Liberty Bell | node (`historic=memorial`) | `-122.426272, 37.759819` | small monument |
| Public restroom | way | `-122.427751, 37.76079` | small building |
| Tennis / basketball courts | `leisure=pitch` | north end | 3.8% of park area |
| Muni J-Church tracks | rail | west edge along Church St | existing rail tier |
| Mission Dolores Basilica | see asset plan | `-122.4270156, 37.7643402` | two blocks north |

### 2.8 Ground and planting recipe

1. Ground: `grass` across the whole polygon, brighter than the default park green.
2. `court` for the courts, small accent patch for the playground.
3. `pathdg` for the main diagonals and the central walk.
4. Palms along the central walk and north edge; broadleaf ring on the perimeter; nothing in the middle.
5. Finer landcover subdivision so the drape follows the 21% grade.

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

**No hero GLB is required for this park.** Two related items:

| Item | Slug | Anchor (lon, lat) | Status |
|---|---|---|---|
| Mission Dolores Basilica |  `mission-dolores` | see `docs/asset-plans/mission-dolores.md` | plan exists — two blocks north, reads with the park |
| Public restroom / clubhouse | — | `-122.427751, 37.76079` | baked building, not a GLB |

### 2.11 Budget

- Negligible geometry growth; the palm archetype is shared engine work.
- Path ribbons add a small amount of merged geometry to one cell.
- No GLBs.

### 2.12 Integration notes

- `doloresPark` is already in `NAMED_PARKS`; no registry change needed.
- Palm archetype and the `court` kind are shared engine work — see `docs/plans/parks/README.md`.
- Finer subdivision for steep park polygons also benefits Alamo Square, Lafayette Park and Buena Vista Park.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- Screenshot from the south-west preset showing the skyline sightline.
- Side-by-side with Buena Vista Park in one frame showing the colour contrast.

### 2.14 Risks and open questions

- If the palm archetype is added globally without per-polygon species weighting, palms will appear all over the city. The species work must be data-driven from the start.
- Reducing `MAX_EDGE` inside park polygons increases triangle counts city-wide; scope it to steep parks only.
- The Muni track question may turn out to belong to a different tier entirely — do not expand scope into the rail bake.

### 2.15 Sources

- OpenStreetMap `way/23871270` and an Overpass bbox query (126 elements, 74 path ways, 3 named).
- This repository's `terrain.bin`/`landuse.bin`.
- `pipeline/landcover.mjs` `MAX_EDGE`, `TREE_AREA_PARK`; `app/src/city.js` `toyTreeArchetype()`.
