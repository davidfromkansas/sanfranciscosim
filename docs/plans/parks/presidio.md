# The Presidio — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | The Presidio |
| Slug | `presidio` |
| OSM | `relation/8346137` |
| Anchor (lon, lat) | `-122.468877, 37.800939` |
| Area | 381.0 ha |
| Bounding span | 3465.8 × 2678.4 m (E–W × N–S) |
| Oriented box | multipolygon, 340 boundary points |
| Elevation | 0–119.5 m (relief 119.5 m, mean 50.5 m) |
| Steepest 50 m grade | 69.9% |
| Baked landcover today | grass 95.3%, trees 2.3%, unclassified 1.8%, sand 0.6% |
| In `NAMED_PARKS` | yes — `presidio` |
| Effort | Large. Comparable to Golden Gate Park, with a bridge relationship to get right. |

**In one sentence:** a 381 ha forested headland in the city's north-west corner, dark with cypress and eucalyptus, dotted with white red-roofed military buildings, and physically continuous with the Golden Gate Bridge approach.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build The Presidio for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make The Presidio read, from the app's high three-quarter diorama camera, as
a 381 ha forested headland in the city's north-west corner, dark with cypress and eucalyptus, dotted with white red-roofed military buildings, and physically continuous with the Golden Gate Bridge approach.

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

- **A forested headland**, not a park inside the grid: the street grid stops at its edge and does not resume.
- **Planted forest geometry.** The Presidio forest was planted in rows in the 1880s; its edges are unnaturally straight and its interior is dark. That artificiality is part of the read.
- **White walls, red roofs.** The Main Post and officers' housing are a large, regular cluster of pale buildings with terracotta roofs — the one strong warm accent in an otherwise dark green mass.
- **Tunnel Tops and the bluff** stepping down to Crissy Field and the Bay on the north side.
- **The bridge.** The Golden Gate Bridge approach emerges from the park's north-west corner. This is the single most important relationship in the whole park; the bridge asset already exists and the park must meet it credibly.

## Layer A — ground and planting (forest cover, species and the bluff edge)

1. **Forest.** Today the Presidio bakes 95.3% `grass` and 2.3% `trees` — the most wrong ground in the city. Apply the park-interior forest rule (README §E4) so the wooded areas bake as `trees` and only the real lawns (Main Post parade ground, Tunnel Tops, Crissy Field lawns, the golf course, MacArthur Meadow) stay `grass`.
2. **Species.** Weight the interior heavily toward `cypress` and `eucalyptus` (README §E3). The Presidio's tall, thin, grey-green blue-gum stands are visually distinct from Golden Gate Park's mix and the difference should be visible from the air.
3. **Planted-row edges.** Where the historic forest has straight edges, keep them straight — do not soften the boundary with a random scatter fade.
4. **Wetland.** `natural=wetland` is not handled by `classify()` at all, so MacArthur Meadow (`relation/13712744`, `wet_meadow`) and Quartermaster Reach (`way/958745402`, tidalflat) currently bake as nothing. Add the `marsh` kind from README §E1.
5. **Coastal edge.** The western bluff drops to the ocean; check that the landcover boundary meets the terrain cleanly and no green triangles hang over the water.
6. **Trails.** Bake only the main named roads and the Tunnel Tops promenade; the trail network is too fine to read.

## Layer B — hero assets

The Presidio's buildings are a texture, not a set of monuments — with three exceptions that carry the park's identity.

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| Presidio Tunnel Tops | `tunnel-tops` | `-122.456479, 37.802857` | 385.6 × 242.1 m, 5.7 ha | **new** — mostly landform + overlook, not a building |
| Presidio Officers' Club | `presidio-officers-club` | `-122.459126, 37.797422` | 56.0 × 56.5 m, OSM `height=5` | **new** — the Main Post anchor building |
| Fort Point | `fort-point` | `-122.477075, 37.810588` | 97.9 × 56.8 m, OSM `height=15` | **new** — brick casemate fort directly under the bridge |
| Main Post building cluster | — | `-122.458479, 37.800197` | block of white/red-roof buildings | kit/baked, not a hero GLB — see Layer C |
| Batteries and fortifications | — | see inventory | ruins, 1–4 m | baked props, not GLBs |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. The Main Post is the one place where the *baked* buildings matter more than any GLB: they must read as a regular block of pale walls under terracotta roofs. Check what the toy building bake currently gives them and, if they come out generic, add a district/roof-colour rule rather than hand-placing models.
2. Verify the join with the Golden Gate Bridge asset: the bridge GLB is placed by `placeBridge()` and its southern approach lands inside the Presidio. Walk the seam at ground level and confirm no floating road, no gap, and no forest growing through the roadway.
3. Batteries: about 10 named `historic=fort` ruins along the coastal bluff (`Battery West`, `Battery Saffold`, `Battery Dynamite`, `Battery Lancaster`, and others in the inventory). Represent them as low pale concrete platforms cut into the bluff — flat, dark-shadowed rectangles read correctly from above and cost almost nothing.
4. Add a `VIEW_PRESETS` camera looking north-west across the Main Post with the bridge in frame (about `-122.4620, 37.7990`, distance 1,400 m, yaw pointing at the bridge). The park's identity is its relationship to the bridge; the preset should show it.
5. Keep the `presidio` `NAMED_PARKS` entry and confirm it still matches after re-classification.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: the Presidio's cells may not more than double their landcover payload. It is a big area at forest density, so measure before and after.
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
`presidio: [-122.4689, 37.8009]` (the park spans many cells; also try `-122.4770, 37.8106` for Fort Point)
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- From the hero view the Presidio reads as a dark forested headland distinct from Golden Gate Park's colour.
- From the new preset: Main Post pale cluster, forest, bluff and the bridge all in one frame.
- The Golden Gate Bridge approach meets the park cleanly at ground level.
- MacArthur Meadow and Quartermaster Reach render as marsh, not as bare terrain.
- Night: the Main Post shows a small cluster of warm windows inside an otherwise dark mass.

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
- do not touch the Golden Gate Bridge asset or its placement — if the seam is wrong, report it
- do not model individual officers' housing units as GLBs
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
| Area (OSM boundary) | 381.0 ha measured from `relation/8346137` outer members |
| Extent | 3,466 m east–west × 2,678 m north–south bounding span |
| Elevation range | 0 m to 119.5 m, mean 50.5 m |
| Relief | 119.5 m; steepest 50 m grade 69.9% (coastal bluffs) |
| Named features in bbox | 154 named elements, 1,715 footway/path ways |
| Tunnel Tops | `way/91114607`, 56,522 m², 386 × 242 m oriented box |
| Fort Point | `relation/5504536`, `building=fort`, `height=15`, brick, 3 levels |
| Officers' Club | `way/32775201`, 2,761 m², OSM `height=5` |
| Mountain Lake | `natural=water`, `-122.470828, 37.788255` |
| Crissy Marsh | `relation/12622483`, tidal flat (shared with the Crissy Field plan) |
| Batteries | at least 10 `historic=fort` ruins along the bluff |

### 2.3 Terrain

- The relief runs from sea level at Crissy Field and Fort Point to 119.5 m on the inland ridge — this is a headland with a genuine spine, not a flat park.
- The 69.9% steepest grade is the coastal bluff on the west side; it should read as a cliff edge, not a slope.
- The northern third steps down in terraces (ridge → Main Post → Tunnel Tops → Crissy Field → Bay). Getting those steps to read is more important than any individual building.
- Fort Point sits at sea level directly beneath the bridge's southern tower — the vertical relationship there is dramatic and worth composing the preset camera around.

### 2.4 What the bake produces today

- 95.3% of the Presidio bakes as `grass` and only 2.3% as `trees`, so the city's densest forest currently renders as the city's largest lawn.
- 1.8% is unclassified (no landcover polygon at all) and 0.6% sand.
- Wetland polygons are dropped entirely by `classify()`.
- Buildings come from the ordinary toy building bake with no Presidio-specific roof or wall treatment.
- The Golden Gate Bridge is already a hand-made GLB placed by the asset loader; the park around its southern approach is baked ground.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 22 m grid (8117 samples):

| Land kind | Share of park |
|---|---|
| grass | 95.3% |
| trees | 2.3% |
| unclassified | 1.8% |
| sand | 0.6% |

### 2.5 Recognition cues, ranked

1. A dark forested headland where the street grid simply stops.
2. The Golden Gate Bridge emerging from its north-west corner.
3. The pale, red-roofed Main Post cluster embedded in the forest.
4. The stepped north edge: ridge, Main Post, Tunnel Tops, Crissy Field, Bay.
5. Coastal bluffs and low concrete batteries on the ocean side.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The park's outline, especially where the grid terminates against it.
- The bridge relationship and the Fort Point / bridge-tower vertical.
- The Main Post's regularity and its warm roof colour.
- The stepped north-side terraces.

**Simplify**

- 1,715 path ways → the named roads and the Tunnel Tops promenade only.
- The 154 named features → the three hero assets plus batteries as platforms.
- Individual housing units → baked building texture.
- The golf course → mown grass with sparse trees, no bunkers or greens detail.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Canopy darkness and height, to separate the Presidio from Golden Gate Park.
- The red of the Main Post roofs, so the cluster reads from 1.5 km.
- The bluff edge's sharpness on the ocean side.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Park boundary | `relation/8346137` | `-122.468877, 37.800939` | 381.0 ha |
| Presidio Tunnel Tops | `way/91114607` | `-122.456479, 37.802857` | 5.7 ha landform park |
| Main Post | `node/1278501872` | `-122.458479, 37.800197` | building cluster |
| Presidio Officers' Club | `way/32775201` | `-122.459126, 37.797422` | `height=5` |
| Fort Point | `relation/5504536` | `-122.477075, 37.810588` | `height=15`, brick |
| Fort Point Light | `way/1358282761` | `-122.477294, 37.810543` | disused lighthouse |
| Mountain Lake | way (`natural=water`) | `-122.470828, 37.788255` | small lake |
| MacArthur Meadow | `relation/13712744` | `-122.455155, 37.797610` | `wetland=wet_meadow` |
| Quartermaster Reach | `way/958745402` | `-122.453181, 37.803603` | `wetland=tidalflat` |
| Battery West | node | `-122.477817, 37.802337` | ruins |
| Battery Saffold | node | `-122.477458, 37.799798` | ruins |
| Battery Dynamite | node | `-122.476804, 37.801392` | ruins |
| Battery Lancaster | node | `-122.475752, 37.808168` | ruins, near the bridge |
| Battery Howe-Wagner | node | `-122.47218, 37.80249` | ruins |
| Battery Blaney | node | `-122.46184, 37.802007` | ruins |
| Battery Sherwood | node | `-122.464165, 37.802448` | ruins |
| Battery Baldwin | node | `-122.465228, 37.802263` | ruins |
| Battery McKinnon-Stotsenberg | node | `-122.474588, 37.794945` | ruins |
| Fort Winfield Scott | node | `-122.47461, 37.801638` | historic fort complex |
| Letterman Digital Arts Center | `way/1074177195` | `-122.449482, 37.799485` | eastern edge |
| Palace of Fine Arts | see `docs/asset-plans/palace-of-fine-arts.md` | — | just outside, reads as adjacent |

### 2.8 Ground and planting recipe

1. Ground base: `trees` across the historic forest blocks, `grass` for the parade ground, Tunnel Tops, golf course and meadows.
2. `marsh` for MacArthur Meadow and Quartermaster Reach.
3. `sand` at Baker Beach and the Crissy shoreline (Crissy Field itself has its own plan).
4. `rock`/bare for the exposed coastal bluff faces where terrain grade exceeds roughly 45%.
5. Tree scatter: cypress and eucalyptus dominant, planted-row regularity near historic blocks, sparse toward the bluff.
6. Batteries as low pale platforms; no gun barrels unless one reads from the diorama camera.
7. Main Post handled through building colour rules, not GLBs.

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
| Presidio Tunnel Tops | `tunnel-tops` | `-122.456479, 37.802857` | 385.6 × 242.1 m, 5.7 ha | **new** — mostly landform + overlook, not a building |
| Presidio Officers' Club | `presidio-officers-club` | `-122.459126, 37.797422` | 56.0 × 56.5 m, OSM `height=5` | **new** — the Main Post anchor building |
| Fort Point | `fort-point` | `-122.477075, 37.810588` | 97.9 × 56.8 m, OSM `height=15` | **new** — brick casemate fort directly under the bridge |
| Main Post building cluster | — | `-122.458479, 37.800197` | block of white/red-roof buildings | kit/baked, not a hero GLB — see Layer C |
| Batteries and fortifications | — | see inventory | ruins, 1–4 m | baked props, not GLBs |

### 2.11 Budget

- 381 ha at forest density is the second-largest tree-count increase in this plan set, after Golden Gate Park.
- The batteries add roughly 10 small baked platforms — negligible.
- Three hero GLBs, all small; Fort Point is the most detailed and should still sit far below the cap.

### 2.12 Integration notes

- `presidio` is already in `NAMED_PARKS`.
- Tunnel Tops, the Officers' Club and Fort Point are new landmarks — Case B in `docs/asset-plans/INTEGRATION-PROMPT.md`, needing `pipeline/lib/landmarks.mjs` entries and a re-bake so baked buildings do not intersect them.
- Fort Point's exclusion radius must not clip the Golden Gate Bridge asset — check the bridge's own placement first.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- The bridge/park seam is walked at ground level and screenshotted.
- Landuse raster inside the Presidio flips from ~95% grass to forest-dominant; report the numbers.

### 2.14 Risks and open questions

- The bridge seam is the highest-risk item: the bridge is an existing, already-shipped asset and this work must not disturb it.
- Reclassifying the golf course and the housing areas as forest would be wrong — the override table must be feature-level, not a blanket park-level flip.
- OSM heights for the Presidio buildings are sparse and low-confidence; verify before any of them drive `targetHeightM`.
- The relation's outer members were fetched with a member cap; the boundary here is good enough for planning but should be re-fetched in full before it drives geometry.

### 2.15 Sources

- OpenStreetMap `relation/8346137`, `way/91114607`, `way/32775201`, `relation/5504536`, `relation/13712744`, `way/958745402` and the battery nodes, via the OSM API and an Overpass bbox query (4,314 elements, 154 named).
- This repository's `app/public/tiles/terrain.bin` and `landuse.bin` for elevation and current bake state.
- `pipeline/landcover.mjs` `classify()` for the wetland gap; `pipeline/lib/classes.mjs` for `LAND_KINDS`.
