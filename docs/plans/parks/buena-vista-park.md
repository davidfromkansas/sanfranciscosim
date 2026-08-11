# Buena Vista Park — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Buena Vista Park |
| Slug | `buena-vista-park` |
| OSM | `way/7459901` |
| Anchor (lon, lat) | `-122.441685, 37.768453` |
| Area | 15.3 ha |
| Bounding span | 470.1 × 529.1 m (E–W × N–S) |
| Oriented box | 537.6 × 418.5 m, long axis 134.5° from east |
| Elevation | 86.3–174.3 m (relief 88 m, mean 132 m) |
| Steepest 50 m grade | 56% |
| Baked landcover today | trees 96.8%, unclassified 2.7%, pitch 0.4% |
| In `NAMED_PARKS` | yes — `buenaVista` |
| Effort | Small–medium. The ground data is already unusually good; the work is canopy character and trails. |

**In one sentence:** a dark green wooded mountain shoved into the Haight-Ashbury street grid, rising 88 m out of the surrounding blocks under a closed eucalyptus canopy.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Buena Vista Park for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Buena Vista Park read, from the app's high three-quarter diorama camera, as
a dark green wooded mountain shoved into the Haight-Ashbury street grid, rising 88 m out of the surrounding blocks under a closed eucalyptus canopy.

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

- **A mountain, not a park.** 15.3 ha, 86–174 m elevation, 88 m of relief, 56% steepest grade. From the hero camera it should read as a dark conical mass, obviously three-dimensional where the surrounding grid is flat.
- **Closed canopy.** No visible lawn from above. This is the darkest green in the city after the Presidio interior.
- **Irregular.** Its boundary follows the hill, not the grid — the one park in the eastern half of the city whose outline is not a rectangle.
- **Streets bend around it.** The grid deforms at its edges; that deformation is part of the read and comes free from the street bake.

## Layer A — ground and planting (canopy species and density, trails, the steep drape)

1. **The good news:** this park already bakes 96.8% `trees`, because the OSM way carries `natural=wood` alongside `leisure=park`. It is the one park in this set whose ground classification is already right. Do not break it while fixing the others — this is the regression test for the Golden Gate Park forest work.
2. **Species.** Blue gum eucalyptus dominates. Use the `eucalyptus` species (README §E3): tall, thin, grey-green, noticeably taller than the broadleaf default. Buena Vista's canopy height is what makes it read as a mountain rather than a hedge.
3. **Drape.** 56% steepest grade with `MAX_EDGE = 55` m will facet badly. This park is the strongest argument for the finer subdivision in README §E6; check the silhouette against the terrain from a low angle.
4. **Trails.** The switchback trails are real but fine. Bake only two or three main ones as `pathdg`; the rest would be noise at this scale.
5. **Small clearings.** A couple of `grass` clearings and overlooks break the canopy and prove it is a park rather than a wood. Keep them small and few.
6. **Playground.** Buena Vista Playground (`-122.442211, 37.769899`) sits at the north-west corner; small accent patch.

## Layer B — hero assets

**No hero GLB is required for this park.** The hill is the asset. Adah's
Stairway (`-122.439035, 37.769981`) is the only named built feature and is a
path-tier ribbon at most.

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Keep the `buenaVista` `NAMED_PARKS` entry.
2. Add a `VIEW_PRESETS` camera from the south-east at a low pitch (about `-122.4385, 37.7660`, distance 700 m, pitch about 12°) so the hill's profile is seen against the flat grid rather than from directly above.
3. This park is the best available regression check for the whole set: after the Golden Gate Park and Presidio forest work, Buena Vista must still be the darkest, densest hill in the eastern city.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: 15.3 ha already at tree density; the change is species and drape resolution, so growth should be small.
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
`buenavista: [-122.4417, 37.7685]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- The hill reads as a dark green mountain from the hero camera.
- Canopy is closed — no lawn visible from above except the small clearings.
- The silhouette does not facet on the steep flanks.
- Eucalyptus canopy is visibly taller and greyer than the broadleaf default elsewhere.
- The street grid visibly bends around the park's edges.

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
- do not regress the existing `natural=wood` classification
- do not open the canopy with large lawns
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
| Area | 15.3 ha / 152,605 m² (`way/7459901`) |
| Extent | 470 × 529 m span; oriented box 538 × 419 m at 134.5° |
| Elevation | 86.3–174.3 m, mean 132.0 m, relief 88.0 m |
| Steepest 50 m grade | 56.0% |
| Current landcover | 96.8% trees, 2.7% unclassified, 0.4% pitch |
| OSM tags | `leisure=park` **and** `natural=wood` — the reason its bake is already correct |
| Playground | `-122.442211, 37.769899` |
| Nearby context | Seaview Apartments `height=27`, Buena Vista Manor House `height=18` |

### 2.3 Terrain

- 88 m of relief over roughly 400 m: this is a genuine hill with a summit at 174.3 m (local `-362, 244`).
- 56% steepest grade is the second-steepest in this set after the Presidio bluffs and Glen Canyon.
- The surrounding streets sit at 86–100 m, so the hill rises roughly 75–85 m above its own edges — that differential is what makes it read.

### 2.4 What the bake produces today

- 96.8% of the park bakes as `trees`, and the trees scatter at the dense `trees` rate (one per 90 m², ×1.5 in the toy tier).
- The canopy uses the same lollipop archetype as everything else, so it is dense but not eucalyptus-shaped.
- No baked trails.
- Landcover drape uses the same 55 m max edge as flat ground, so steep flanks may facet.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 5 m grid (6098 samples):

| Land kind | Share of park |
|---|---|
| trees | 96.8% |
| unclassified | 2.7% |
| pitch | 0.4% |

### 2.5 Recognition cues, ranked

1. A dark green mountain inside the street grid.
2. Closed eucalyptus canopy with no visible lawn.
3. An irregular, non-rectangular outline.
4. Streets bending around its base.
5. Steep switchback trails and stair edges.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The real relief and the irregular boundary.
- Closed-canopy darkness.
- The abruptness of the transition from grid to hill.

**Simplify**

- 182 path ways → two or three switchbacks.
- Staircases → path ribbon segments.
- Understory and clearing detail → a couple of small grass patches.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Canopy height, so the hill's mass reads at city scale.
- Canopy darkness relative to every other eastern-city green.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Park boundary | `way/7459901` | `-122.441685, 37.768453` | 15.3 ha, `natural=wood` |
| Buena Vista Playground | way | `-122.442211, 37.769899` | north-west corner |
| Adah's Stairway | node | `-122.439035, 37.769981` | historic stair |
| Sunset Tunnel | `man_made=tunnel` | `-122.441609, 37.767847` | passes under the hill |
| Seaview Apartments | way | `-122.443546, 37.766337` | `height=27`, context |
| Buena Vista Manor House | way | `-122.440579, 37.766528` | `height=18`, context |

### 2.8 Ground and planting recipe

1. `trees` across nearly the whole polygon — already the case.
2. Two or three small `grass` clearings and overlooks.
3. Eucalyptus-dominant scatter at full forest density, tall and thin.
4. `pathdg` for two or three switchbacks plus Adah's Stairway.
5. Finer drape subdivision on the steep flanks.

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

**No hero GLB is required for this park.** The hill is the asset. Adah's
Stairway (`-122.439035, 37.769981`) is the only named built feature and is a
path-tier ribbon at most.

### 2.11 Budget

- Tree count is already high here and does not need to increase; the archetype change is free.
- Finer subdivision on 15.3 ha of steep ground is the main cost — measure it.
- No GLBs.

### 2.12 Integration notes

- `buenaVista` is already in `NAMED_PARKS`.
- Shares the species, path and subdivision engine work with the rest of the set.
- Use this park as the regression case when changing `classify()` for Golden Gate Park.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- Before/after comparison confirming the tree percentage stays at or above 96%.
- Low-angle silhouette screenshot showing no faceting.

### 2.14 Risks and open questions

- The Golden Gate Park forest changes touch the same `classify()` code path; a careless change here loses the one park that is already right.
- Finer subdivision on steep ground is the biggest triangle-count risk in the small-park group.

### 2.15 Sources

- OpenStreetMap `way/7459901` and an Overpass bbox query (384 elements, 182 path ways, 7 named).
- This repository's `terrain.bin`/`landuse.bin`.
- `pipeline/landcover.mjs` `TREE_AREA_TREES`/`TREE_AREA_PARK`, `MAX_EDGE`.
