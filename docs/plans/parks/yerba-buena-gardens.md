# Yerba Buena Gardens — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Yerba Buena Gardens |
| Slug | `yerba-buena-gardens` |
| OSM | `way/28842443` |
| Anchor (lon, lat) | `-122.402406, 37.784645` |
| Area | 1.6 ha |
| Bounding span | 168.7 × 185.2 m (E–W × N–S) |
| Oriented box | 113.9 × 167.0 m, long axis 136.7° from east |
| Elevation | 9.5–13.3 m (relief 3.8 m, mean 11.1 m) |
| Steepest 50 m grade | 5% |
| Baked landcover today | grass 95.5%, water 2.9%, unclassified 1.6% |
| In `NAMED_PARKS` | **no** — not in `NAMED_PARKS`; add `yerbaBuenaGardens` if it should be checked and camera-targeted |
| Effort | Medium. Small area but the most 'built' park in the set, and it sits on top of a convention centre. |

**In one sentence:** a 1.6 ha manicured urban plaza-park on a Moscone Center roof deck, hemmed in by SoMa towers, geometric rather than natural, with the Martin Luther King Jr. Memorial waterfall as its one dramatic element.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Yerba Buena Gardens for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Yerba Buena Gardens read, from the app's high three-quarter diorama camera, as
a 1.6 ha manicured urban plaza-park on a Moscone Center roof deck, hemmed in by SoMa towers, geometric rather than natural, with the Martin Luther King Jr. Memorial waterfall as its one dramatic element.

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

- **Urban, not wild.** Straight edges, terraces, paved geometry, trees in rows. If it looks like a meadow, it is wrong.
- **Enclosed and overshadowed.** 1.6 ha surrounded by towers 25–50 m and taller; the park is a floor at the bottom of a room.
- **Built on a roof.** The lawn is a deck over Moscone Center. The ground plane here is architecture, and the surrounding baked buildings must not intersect it.
- **The waterfall.** The MLK Memorial (`-122.402253, 37.784531`) is the one vertical, dramatic element and the only place water belongs.
- **Flat.** 3.8 m of relief, 5% steepest grade — the terraces are built, not terrain.

## Layer A — ground and planting (paved geometry, rows of trees, and a built ground plane)

1. **Geometric ground.** Split the polygon into a mown `grass` lawn rectangle plus surrounding `paved` terraces and walks. This is the one park in the set where paved area should be a large fraction of the total.
2. **Tree rows.** Place trees along paths in rows, not scattered. README §E3's placement modes must include a `row` mode along path centrelines; this park is the reason it exists.
3. **Water.** The 2.9% water already in the raster is the memorial's basin; keep it, and give the waterfall a vertical element (see Layer B).
4. **No forest, no scrub, no meadow.** Keep the kind list here to `grass`, `paved`, `water` and small `bloom` accents.
5. **Roof-deck check.** Confirm the baked Moscone Center buildings do not poke through the park's ground plane. If they do, that is a building/landcover height-ordering problem worth fixing properly.

## Layer B — hero assets

Small, built elements. The surrounding cultural buildings are baked; only the waterfall really needs authoring.

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| MLK Jr. Memorial waterfall | `mlk-memorial-waterfall` | `-122.402253, 37.784531` | wall + basin, small | **new** — small hero, high identity value |
| Yerba Buena Center for the Arts | — | `-122.401325, 37.785078` | OSM `height=36` | baked building |
| YBCA Gallery | — | `-122.402101, 37.785596` | `height=28` | baked building |
| Moscone North / South | — | `-122.401865, 37.784344` / `-122.401253, 37.783867` | `height=25` / `12` | baked; must not intersect the deck |
| Metreon | — | `-122.403128, 37.784289` | `height=50` | baked building |
| St Patrick Catholic Church | — | `-122.403552, 37.785573` | `height=46` | baked; a strong edge marker |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Add `yerbaBuenaGardens` to `NAMED_PARKS` (`-122.402406, 37.784645`) and re-bake.
2. Add a `VIEW_PRESETS` camera looking down into the gardens from the south-west with towers framing it (about `-122.4035, 37.7838`, distance 400 m, pitch about 35°) — a steeper pitch than most presets, because this park is seen as a floor.
3. The Esplanade Main Stage and East Garden are small distinct zones; represent them as paved/garden patches rather than objects.
4. SFMOMA and the surrounding museums are just outside; do not model them here.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: 1.6 ha; trivial geometry. The care is in composition, not cost.
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
`yerbabuena: [-122.4024, 37.7846]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- The park reads as a built plaza: straight edges, paved terraces, trees in rows.
- The waterfall is visible and reads as the focal point.
- No Moscone geometry pokes through the deck.
- Surrounding towers enclose the park with no gaps.
- Night: the plaza reads as lit urban ground, not dark parkland.

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
- do not scatter trees randomly here
- do not model SFMOMA or the surrounding museums as part of this park
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
| Area | 1.6 ha / 15,562 m² (`way/28842443`) |
| Extent | 169 × 185 m span; oriented box 114 × 167 m at 136.7° |
| Elevation | 9.5–13.3 m, mean 11.1 m, relief 3.8 m |
| Steepest 50 m grade | 5.0% |
| Current landcover | 95.5% grass, 2.9% water, 1.6% unclassified |
| MLK Jr. Memorial | `historic=memorial`, `-122.402253, 37.784531` |
| Ohlone Indian Memorial | `-122.402936, 37.784816` |
| Surrounding heights (OSM) | Metreon 50 m, St Patrick's 46 m, YBCA 36 m, YBCA Gallery 28 m, Moscone North 25 m |

### 2.3 Terrain

- Effectively flat: 3.8 m across the whole park, most of it built terracing rather than natural grade.
- The whole site sits on filled ground at 9–13 m; the terrain data is unremarkable and needs no work.
- The visual drama comes entirely from the surrounding towers, which already exist in the baked city.

### 2.4 What the bake produces today

- 95.5% grass — the park currently reads as a lawn, when it is roughly half hard landscape.
- 2.9% water is present (the memorial basin), which is unusually good.
- Trees scatter randomly rather than in rows.
- Not in `NAMED_PARKS`.
- The Moscone roof-deck relationship is not modelled at all.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 5 m grid (625 samples):

| Land kind | Share of park |
|---|---|
| grass | 95.5% |
| water | 2.9% |
| unclassified | 1.6% |

### 2.5 Recognition cues, ranked

1. A manicured green rectangle at the bottom of a well of SoMa towers.
2. Geometric terraces, paved walks and rows of trees.
3. The MLK Memorial waterfall.
4. Moscone's low bulk beneath and alongside it.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The straight edges and geometric layout.
- The proportion of paved to lawn.
- The waterfall's position and the basin.
- The enclosure by towers.

**Simplify**

- 73 path ways → the main geometric walk pattern.
- Individual sculptures and the carousel → omit or accent patches.
- Planting variety → rows of one canopy type plus small bloom accents.

**Exaggerate (authoring only — never move or rescale the real feature)**

- The regularity of the tree rows.
- The lawn's manicured brightness against the grey plaza.
- The waterfall's scale, modestly, so it reads from the preset.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Gardens boundary | `way/28842443` | `-122.402406, 37.784645` | 1.6 ha |
| MLK Jr. Memorial | node | `-122.402253, 37.784531` | waterfall, hero |
| Ohlone Indian Memorial | node | `-122.402936, 37.784816` | small |
| East Garden | way (`leisure=garden`) | `-122.401661, 37.785514` | garden zone |
| Esplanade Main Stage | way | `-122.40238, 37.784986` | open-air stage |
| Yerba Buena Center for the Arts | way | `-122.401325, 37.785078` | `height=36` |
| YBCA Gallery | way | `-122.402101, 37.785596` | `height=28` |
| Moscone Convention Center North | way | `-122.401865, 37.784344` | `height=25` |
| Moscone Convention Center South | way | `-122.401253, 37.783867` | `height=12` |
| Metreon | way | `-122.403128, 37.784289` | `height=50` |
| St Patrick Catholic Church | way | `-122.403552, 37.785573` | `height=46` |

### 2.8 Ground and planting recipe

1. Central `grass` rectangle, sharply edged.
2. `paved` terraces and walks around it — roughly half the park.
3. `water` at the memorial basin.
4. Row-placed trees along the walk centrelines.
5. Small `bloom` accents in the East Garden only.
6. One small waterfall GLB.

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
| MLK Jr. Memorial waterfall | `mlk-memorial-waterfall` | `-122.402253, 37.784531` | wall + basin, small | **new** — small hero, high identity value |
| Yerba Buena Center for the Arts | — | `-122.401325, 37.785078` | OSM `height=36` | baked building |
| YBCA Gallery | — | `-122.402101, 37.785596` | `height=28` | baked building |
| Moscone North / South | — | `-122.401865, 37.784344` / `-122.401253, 37.783867` | `height=25` / `12` | baked; must not intersect the deck |
| Metreon | — | `-122.403128, 37.784289` | `height=50` | baked building |
| St Patrick Catholic Church | — | `-122.403552, 37.785573` | `height=46` | baked; a strong edge marker |

### 2.11 Budget

- 1.6 ha; the geometry is trivial.
- One small GLB, likely under 2,000 triangles.
- Row placement is a scatter-mode change, not a cost change.

### 2.12 Integration notes

- Needs a new `NAMED_PARKS` entry and a re-bake.
- The waterfall is a new landmark — Case B in `docs/asset-plans/INTEGRATION-PROMPT.md`, though its exclusion radius should be very small.
- The `row` placement mode is shared engine work (README §E3) and also serves the Music Concourse in Golden Gate Park.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- `missingParks` stays empty after adding `yerbaBuenaGardens`.
- A screenshot proving no Moscone geometry intersects the deck.

### 2.14 Risks and open questions

- The roof-deck relationship may expose a real ordering problem between the building bake and landcover. If it does, fix it generally rather than special-casing this park.
- At 1.6 ha surrounded by 50 m towers, the park may be barely visible from the standard diorama camera; the steeper preset exists for this reason, and the park may simply be a close-range feature.
- OSM heights here are a mix of `25` and `25 m` string forms — check the parser handles both before trusting them.

### 2.15 Sources

- OpenStreetMap `way/28842443` and an Overpass bbox query (109 elements, 73 path ways, 10 named).
- This repository's `terrain.bin`/`landuse.bin`.
