# Alamo Square — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Alamo Square |
| Slug | `alamo-square` |
| OSM | `way/745183964` |
| Anchor (lon, lat) | `-122.434997, 37.776175` |
| Area | 5.1 ha |
| Bounding span | 297.6 × 227.8 m (E–W × N–S) |
| Oriented box | 272.3 × 188.1 m, long axis 170.9° from east |
| Elevation | 51.4–81.8 m (relief 30.3 m, mean 71.9 m) |
| Steepest 50 m grade | 22.3% |
| Baked landcover today | grass 96.5%, unclassified 3.5% |
| In `NAMED_PARKS` | yes — `alamoSquare` |
| Effort | Small. The park itself is simple; the value is in the composition and the Painted Ladies asset. |

**In one sentence:** a small sloping hilltop lawn ringed with mature trees whose entire fame is the composition looking east: the Painted Ladies in the foreground and the downtown skyline behind them.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Alamo Square for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Alamo Square read, from the app's high three-quarter diorama camera, as
a small sloping hilltop lawn ringed with mature trees whose entire fame is the composition looking east: the Painted Ladies in the foreground and the downtown skyline behind them.

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

- **A hilltop block.** 5.1 ha, 272 × 188 m oriented box, sitting at 51–82 m with 30.3 m of relief and a 22.3% steepest grade — high enough that the city drops away to the east.
- **Tree-ringed, open-centred.** A mature perimeter canopy with a clear central lawn and paths crossing it.
- **The composition.** Park → Painted Ladies on Steiner Street → downtown skyline. If that view does not work in-engine, this park has failed, whatever else is right.

## Layer A — ground and planting (slope, perimeter canopy and crossing paths)

1. **Slope drape.** As with Dolores, confirm the landcover follows the 30.3 m of relief rather than facetting across it; use the finer subdivision for steep park polygons (README §E6).
2. **Perimeter ring.** Place trees as a deliberate ring rather than a uniform scatter — this is a distinct planting pattern from any other park here and README §E3 should support an explicit `ring` scatter mode.
3. **Crossing paths.** The park's diagonal walks are its internal structure and should be baked as `pathdg` ribbons.
4. **Playground.** Alamo Square Playground (`-122.433801, 37.776467`) gets a small accent patch.
5. **Keep the lawn bright.** Like Dolores, this is mown lawn, not forest.

## Layer B — hero assets

The park's hero asset is not in the park. It is the row of houses on its eastern edge, and it already has a plan.

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| Painted Ladies | `painted-ladies` | see `docs/asset-plans/painted-ladies.md` | row of 6 Victorians, Steiner St | plan exists — **the** hero for this park |
| Alamo Square Historic District (surrounding blocks) | — | `-122.434971, 37.777152` | — | baked buildings; needs colour, not GLBs |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Keep the `alamoSquare` `NAMED_PARKS` entry.
2. Add the defining `VIEW_PRESETS` camera: stand on the park's western high ground looking east-north-east across the Painted Ladies to downtown — roughly `-122.4360, 37.7763`, pitch about 10°, distance 2,500 m so the skyline is in frame. Tune it against a real photograph of the view.
3. The surrounding Victorian blocks should read as colourful and fine-grained. If the baked building colours make them generic, that is a building-colour rule question for the historic district, not a per-house modelling job.
4. Verify the Painted Ladies asset, once shipped, sits on the correct side of Steiner and at the correct grade — the houses step down the hill.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: trivial; a 5.1 ha park with path ribbons and a tree ring.
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
`alamosquare: [-122.4350, 37.7762]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- The park reads as a raised green block with a tree ring and an open centre.
- From the new preset the Painted Ladies and the skyline compose correctly.
- The slope is visible; the park is clearly higher than the streets east of it.
- Paths cross the lawn legibly at 300 m altitude.

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
- do not re-research the Painted Ladies — run their existing asset plan
- do not forest the park; it is a lawn with a tree ring
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
| Area | 5.1 ha / 51,043 m² (`way/745183964`) |
| Extent | 298 × 228 m span; oriented box 272 × 188 m at 170.9° |
| Elevation | 51.4–81.8 m, mean 71.9 m, relief 30.3 m |
| Steepest 50 m grade | 22.3% |
| Current landcover | 96.5% grass, 3.5% unclassified |
| Playground | `-122.433801, 37.776467` |
| Historic district | `historic=district`, `-122.434971, 37.777152` |

### 2.3 Terrain

- The high ground is on the west side (local `243, -632`, 81.8 m) and it falls east toward Steiner and beyond — which is why the skyline view works from the west edge looking east.
- 30.3 m of relief on a 5.1 ha park is a strong grade for its size; the park should visibly bulge above the surrounding blocks.
- The Painted Ladies row itself steps down the hill; whoever places that asset must respect the grade rather than sitting it on one level.

### 2.4 What the bake produces today

- 96.5% grass — reasonable for this park.
- Sparse lollipop trees scattered uniformly rather than ringed.
- No baked paths.
- The Painted Ladies are currently ordinary baked buildings.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 5 m grid (2042 samples):

| Land kind | Share of park |
|---|---|
| grass | 96.5% |
| unclassified | 3.5% |

### 2.5 Recognition cues, ranked

1. The park → Painted Ladies → skyline composition.
2. A raised, tree-ringed green block in the middle of the Western Addition grid.
3. The open central lawn with crossing diagonal paths.
4. The pronounced east-facing slope.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The real grade and the west-high/east-low direction.
- The perimeter-ring planting with an open centre.
- The relationship to Steiner Street.

**Simplify**

- 95 path ways → three or four crossing walks.
- Playground detail → one accent patch.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Perimeter canopy height slightly, so the ring reads from above.
- The colour saturation of the surrounding Victorian blocks, within the style bible's restraint.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Park boundary | `way/745183964` | `-122.434997, 37.776175` | 5.1 ha |
| Alamo Square (attraction) | way | `-122.434696, 37.776361` | `tourism=attraction` |
| Alamo Square Playground | way | `-122.433801, 37.776467` | small |
| Alamo Square Historic District | way | `-122.434971, 37.777152` | surrounding blocks |
| Painted Ladies | see asset plan | Steiner St, east edge | hero asset |

### 2.8 Ground and planting recipe

1. `grass` across the polygon, bright mown green.
2. `pathdg` for the crossing diagonals.
3. Ring scatter of broadleaf canopy on the perimeter; open centre.
4. Small accent patch for the playground.
5. Finer drape subdivision for the grade.

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
| Painted Ladies | `painted-ladies` | see `docs/asset-plans/painted-ladies.md` | row of 6 Victorians, Steiner St | plan exists — **the** hero for this park |
| Alamo Square Historic District (surrounding blocks) | — | `-122.434971, 37.777152` | — | baked buildings; needs colour, not GLBs |

### 2.11 Budget

- Negligible. One small park, path ribbons, a tree ring.
- The Painted Ladies GLB is budgeted in its own plan.

### 2.12 Integration notes

- `alamoSquare` is already in `NAMED_PARKS`.
- Painted Ladies integration follows `docs/asset-plans/INTEGRATION-PROMPT.md`.
- The ring scatter mode and path tier are shared engine work.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- A screenshot from the preset compared side by side with a real photograph of the view.

### 2.14 Risks and open questions

- The whole park hangs on the Painted Ladies asset. If that asset slips, this park is just a green block — say so rather than substituting something.
- The skyline preset's framing is sensitive; expect to tune it by eye.
- Ring scatter is a new placement mode; if it proves fiddly, an annulus polygon of `trees` kind with normal scatter inside it is an acceptable fallback.

### 2.15 Sources

- OpenStreetMap `way/745183964` and an Overpass bbox query (134 elements, 95 path ways, 3 named).
- This repository's `terrain.bin`/`landuse.bin`.
- `docs/asset-plans/painted-ladies.md` for the hero asset.
