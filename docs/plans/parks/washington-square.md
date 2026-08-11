# Washington Square — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Washington Square |
| Slug | `washington-square` |
| OSM | `way/18583270` |
| Anchor (lon, lat) | `-122.41021, 37.800858` |
| Area | 0.9 ha |
| Bounding span | 137.0 × 93.6 m (E–W × N–S) |
| Oriented box | 83.8 × 127.5 m, long axis 81.8° from east |
| Elevation | 21.8–27.4 m (relief 5.6 m, mean 24.4 m) |
| Steepest 50 m grade | 6.2% |
| Baked landcover today | grass 90.1%, unclassified 9.9% |
| In `NAMED_PARKS` | **no** — not in `NAMED_PARKS`; add `washingtonSquare` if the park should be checked and camera-targeted |
| Effort | Small. One church asset and a tidy little park. |

**In one sentence:** a 0.9 ha rectangular green in the middle of North Beach, pressed hard on all four sides by dense blocks, with the twin white spires of Saints Peter and Paul rising over its northern edge.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Washington Square for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Washington Square read, from the app's high three-quarter diorama camera, as
a 0.9 ha rectangular green in the middle of North Beach, pressed hard on all four sides by dense blocks, with the twin white spires of Saints Peter and Paul rising over its northern edge.

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

- **Small and enclosed.** 0.9 ha, oriented box 84 × 128 m; the surrounding buildings are taller than anything in the park, so it reads as a courtyard in the city fabric.
- **Nearly flat.** 5.6 m of relief, 6.2% steepest grade — the flattest park in this set after Crissy Field and Yerba Buena.
- **Structured by paths.** At this size the diagonal and curving walks are a large fraction of the visible surface. They must be baked or the park is a plain green rectangle.
- **The church.** Saints Peter and Paul's twin white spires on the north side are the whole reason this square is recognisable.

## Layer A — ground and planting (paths, perimeter trees and a small flat lawn)

1. **Paths first.** For a park this small, the `pathdg` ribbon tier (README §E5) is not optional — the walks are the composition. Bake the diagonals and the curving central walks.
2. **Perimeter canopy.** Mature trees around the edges, open in the middle, same ring pattern as Alamo Square.
3. **Lawn.** Bright mown `grass`; 90.1% already classifies correctly.
4. **Playground.** Washington Square Playground (`-122.410719, 37.800977`) as a small accent patch.
5. **Do not** add relief. The park is genuinely flat and any invented undulation will look wrong against the surrounding blocks.

## Layer B — hero assets

One hero asset, and it is not in the park.

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| Saints Peter and Paul Church | `sts-peter-and-paul` | `-122.410252, 37.80156` | 42 × 48 m footprint, OSM `height=23` (façade — the spires are taller; verify) | **new** — needs an asset plan; the hero for this park |
| Benjamin Franklin statue | — | `-122.410013, 37.80082` | small | prop, not a GLB |
| Fire Fighter's Memorial | — | `-122.410683, 37.800838` | small | prop, not a GLB |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Add `washingtonSquare` to `NAMED_PARKS` (`-122.41021, 37.800858`) so the landcover bake verifies a polygon matches it, then re-bake.
2. Add a `VIEW_PRESETS` camera on the square's south side looking north at the church (about `-122.41021, 37.7999`, distance 350 m, pitch about 18°) — the classic North Beach postcard.
3. The central monument and statues are small enough to omit; include them only if a generic monument prop already exists.
4. North Beach's surrounding blocks are dense and low. Check the baked buildings crowd the square properly and there is no accidental gap.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: trivial — under 1 ha.
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
`washingtonsquare: [-122.4102, 37.8009]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- Paths are clearly legible from the diorama camera; the park is not a plain rectangle.
- The church's twin spires dominate the north side once the asset ships.
- The surrounding buildings press against all four edges with no gaps.
- The park is flat — no invented mounding.

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
- do not give the park artificial relief
- do not scatter trees across the middle
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
| Area | 0.9 ha / 8,897 m² (`way/18583270`) |
| Extent | 137 × 94 m span; oriented box 84 × 128 m at 81.8° |
| Elevation | 21.8–27.4 m, mean 24.4 m, relief 5.6 m |
| Steepest 50 m grade | 6.2% |
| Current landcover | 90.1% grass, 9.9% unclassified |
| Saints Peter and Paul Church | `way/29902626`, 1,660 m², oriented 42 × 48 m, OSM `height=23` |
| Named features | 4 (two memorials, a memorial bench, the playground) |

### 2.3 Terrain

- Flat by SF standards; the ground drops gently to the north-west.
- The square sits in a shallow saddle between Telegraph Hill and Russian Hill, which is why it is one of the few level open spaces in that quarter.

### 2.4 What the bake produces today

- 90.1% grass, 9.9% unclassified — a plain green rectangle.
- No baked paths, so at this scale the park is featureless.
- The church is an ordinary baked building; its spires are not represented.
- The park is not in `NAMED_PARKS`, so the bake does not verify it.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 5 m grid (355 samples):

| Land kind | Share of park |
|---|---|
| grass | 90.1% |
| unclassified | 9.9% |

### 2.5 Recognition cues, ranked

1. Twin white spires over the north edge.
2. A small green rectangle tightly enclosed by dense blocks.
3. The crossing diagonal and curving walks.
4. Mature perimeter trees with an open lawn centre.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The flatness and the tight enclosure.
- The path pattern.
- The church's position on the north side, across Filbert Street.

**Simplify**

- 22 path ways → the main diagonals and the central curve.
- Statues and benches → omit or use existing props.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Spire height, modestly, so the church reads from the diorama camera (authoring only — the anchor and the real height stay honest).
- Path width, so the walks survive at distance.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Park boundary | `way/18583270` | `-122.410210, 37.800858` | 0.9 ha |
| Saints Peter and Paul Church | `way/29902626` | `-122.410252, 37.80156` | `height=23`, hero asset |
| Saints Peter and Paul School | node | `-122.410465, 37.801368` | adjacent |
| Washington Square Playground | way | `-122.410719, 37.800977` | small |
| Benjamin Franklin statue | node | `-122.410013, 37.80082` | monument |
| Fire Fighter's Memorial | node | `-122.410683, 37.800838` | monument |

### 2.8 Ground and planting recipe

1. `grass` across the polygon.
2. `pathdg` diagonals and central curve — the priority here.
3. Perimeter broadleaf ring, open centre.
4. Small accent patch at the playground.

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
| Saints Peter and Paul Church | `sts-peter-and-paul` | `-122.410252, 37.80156` | 42 × 48 m footprint, OSM `height=23` (façade — the spires are taller; verify) | **new** — needs an asset plan; the hero for this park |
| Benjamin Franklin statue | — | `-122.410013, 37.80082` | small | prop, not a GLB |
| Fire Fighter's Memorial | — | `-122.410683, 37.800838` | small | prop, not a GLB |

### 2.11 Budget

- Under 1 ha; costs essentially nothing.
- One small church GLB, well under the cap.

### 2.12 Integration notes

- Needs a new `NAMED_PARKS` entry — the only park in this set besides Lafayette and Yerba Buena that does.
- Saints Peter and Paul is a new landmark: Case B in `docs/asset-plans/INTEGRATION-PROMPT.md`, needing a `pipeline/lib/landmarks.mjs` entry and a re-bake so the baked church footprint is cleared.
- It also has no asset plan yet — write one using the 19 landmark plans as the template before authoring.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- `missingParks` stays empty after adding `washingtonSquare`.
- Screenshot from the preset with the spires reading clearly.

### 2.14 Risks and open questions

- OSM `height=23` almost certainly describes the church body, not the spire tips (the same pattern flagged for City Hall and St Mary's in the landmark plans). Verify before it drives `targetHeightM`.
- At 0.9 ha the park is near the limit of what reads from the diorama camera at all; if paths do not survive, the park will look empty however correct the data is.

### 2.15 Sources

- OpenStreetMap `way/18583270`, `way/29902626`, plus an Overpass bbox query (34 elements, 22 path ways, 4 named).
- This repository's `terrain.bin`/`landuse.bin`.
