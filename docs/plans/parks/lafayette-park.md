# Lafayette Park — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Lafayette Park |
| Slug | `lafayette-park` |
| OSM | `way/16751838` |
| Anchor (lon, lat) | `-122.426857, 37.791483` |
| Area | 4.6 ha |
| Bounding span | 297.3 × 216.9 m (E–W × N–S) |
| Oriented box | 273.0 × 176.3 m, long axis 170.9° from east |
| Elevation | 89.5–114.7 m (relief 25.2 m, mean 104.9 m) |
| Steepest 50 m grade | 25.2% |
| Baked landcover today | grass 93.8%, unclassified 4.7%, pitch 1.5% |
| In `NAMED_PARKS` | **no** — not in `NAMED_PARKS`; add `lafayettePark` if it should be checked and camera-targeted |
| Effort | Small–medium. Mostly planting and grade, no hero GLB. |

**In one sentence:** a steep, densely wooded hilltop block in Pacific Heights sitting at 90–115 m, lusher and higher than Dolores or Alamo Square, ringed by Victorian mansions and climbed by staircases.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Lafayette Park for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Lafayette Park read, from the app's high three-quarter diorama camera, as
a steep, densely wooded hilltop block in Pacific Heights sitting at 90–115 m, lusher and higher than Dolores or Alamo Square, ringed by Victorian mansions and climbed by staircases.

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

- **High.** 89.5–114.7 m — the highest park in this set apart from Buena Vista and Glen Canyon. It should read as a green cap on the Pacific Heights ridge.
- **Wooded, but not a forest.** Dense mature canopy around a large central lawn — deliberately between Alamo Square's ring and Buena Vista's closed canopy.
- **Steep-sided.** 25.2 m of relief on 4.6 ha, 25.2% steepest grade, with staircases on the street edges.
- **Enclosed by mansions.** The surrounding blocks are large, pale and grand rather than colourful — a different texture from Alamo Square's Victorians.

## Layer A — ground and planting (canopy density between ring and forest, grade, paths)

1. **Canopy.** Denser than Alamo Square, lighter than Buena Vista: use a mid density with `trees` cover on the slopes and mown `grass` on the summit lawn. This intermediate setting is the whole point of the park and is worth tuning by eye from the diorama camera.
2. **Grade.** 25.2% steepest — apply the finer drape subdivision for steep park polygons (README §E6).
3. **Winding paths.** The paths switchback up the grade; bake the main ones as `pathdg` ribbons and let them curve rather than straight-lining them.
4. **Courts and playground.** 1.5% of the park already bakes as `pitch`; give the tennis courts the `court` kind and the playground (`-122.428457, 37.791527`) an accent patch.
5. **Staircases.** Real, and characteristic, but tiny. Represent them as short pale ribbon segments in the path tier rather than as stepped geometry — steps will not read from the diorama camera and will cost triangles.

## Layer B — hero assets

**No hero GLB is required for this park.** The surrounding Pacific Heights
mansion blocks are baked buildings; at most they want a colour/scale rule, not
models.

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Add `lafayettePark` to `NAMED_PARKS` (`-122.426857, 37.791483`) and re-bake so the match check covers it.
2. Add a `VIEW_PRESETS` camera on the summit looking north-east toward the Bay (about `-122.42686, 37.7915`, distance 1,800 m, pitch about 10°) — the Bay glimpse is part of the park's character.
3. Check that Lafayette, Alamo Square and Dolores read as three visibly *different* parks in the same city. If they all look the same, the canopy-density work has not landed.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: trivial — 4.6 ha.
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
`lafayettepark: [-122.4269, 37.7915]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- The park reads as a wooded green cap on the ridge, clearly higher than its surroundings.
- Canopy density sits visibly between Alamo Square and Buena Vista.
- Winding paths are legible and actually curve.
- From the preset, the Bay is in view past the north edge.

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
- do not model individual staircases as stepped geometry
- do not make it as dark as Buena Vista Park
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
| Area | 4.6 ha / 46,356 m² (`way/16751838`) |
| Extent | 297 × 217 m span; oriented box 273 × 176 m at 170.9° |
| Elevation | 89.5–114.7 m, mean 104.9 m, relief 25.2 m |
| Steepest 50 m grade | 25.2% |
| Current landcover | 93.8% grass, 4.7% unclassified, 1.5% pitch |
| Playground | `-122.428457, 37.791527` |
| Nearby tall context | Washington Tower `height=36` at `-122.429176, 37.79261` |

### 2.3 Terrain

- The summit is on the west side (local `880, -2421`, 114.7 m); the ground falls to the east and south-east.
- Mean elevation 104.9 m makes this the highest sustained ground in the set outside Buena Vista and Glen Canyon.
- The park's summit is above most of the surrounding roofs, which is why the Bay glimpse exists.

### 2.4 What the bake produces today

- 93.8% grass — the park currently reads as an open lawn, when it should read as wooded.
- 1.5% pitch (the courts).
- Sparse uniform lollipop scatter.
- No baked paths; the switchbacks are invisible.
- Not in `NAMED_PARKS`.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 5 m grid (1852 samples):

| Land kind | Share of park |
|---|---|
| grass | 93.8% |
| unclassified | 4.7% |
| pitch | 1.5% |

### 2.5 Recognition cues, ranked

1. A high, densely wooded green block on the Pacific Heights ridge.
2. Steep sides with switchback paths and stair edges.
3. A large open summit lawn inside the canopy.
4. Grand pale mansion blocks around it.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The elevation and the steep sides.
- The canopy-around-lawn structure.
- The switchback path geometry.

**Simplify**

- 55 path ways → three or four switchbacks.
- Staircases → path ribbon segments.
- Playground and court detail → accent patches.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Canopy density relative to Alamo Square, so the two parks are clearly different species of park.
- The apparent height of the block, via canopy height rather than terrain (terrain stays honest).

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Park boundary | `way/16751838` | `-122.426857, 37.791483` | 4.6 ha |
| Lafayette Park Playground | way | `-122.428457, 37.791527` | small |
| Tennis courts | `leisure=pitch` | inside the park | 1.5% of area |
| Washington Tower | way | `-122.429176, 37.79261` | `height=36`, context |
| Pacific Heights Towers | way | `-122.429503, 37.79068` | context |

### 2.8 Ground and planting recipe

1. `trees` on the slopes, `grass` on the summit lawn.
2. Mid-density canopy: denser than the park default, lighter than forest.
3. `pathdg` switchbacks plus short stair segments.
4. `court` for the tennis courts, accent patch for the playground.
5. Finer drape subdivision for the 25% grade.

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

**No hero GLB is required for this park.** The surrounding Pacific Heights
mansion blocks are baked buildings; at most they want a colour/scale rule, not
models.

### 2.11 Budget

- 4.6 ha at mid density; negligible.
- No GLBs.

### 2.12 Integration notes

- Needs a new `NAMED_PARKS` entry and a re-bake of its cell.
- Shares the canopy-density, path and `court` engine work with the rest of this set.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- `missingParks` stays empty after adding `lafayettePark`.
- A single frame containing Lafayette, Alamo Square and Dolores showing three distinct park characters.

### 2.14 Risks and open questions

- The 'between ring and forest' density is a judgement call with no measurable target; budget iteration time and settle it from screenshots, not from numbers.
- Adding a park to `NAMED_PARKS` requires a re-bake to take effect; do not expect it to change anything at runtime alone.

### 2.15 Sources

- OpenStreetMap `way/16751838` and an Overpass bbox query (76 elements, 55 path ways, 3 named).
- This repository's `terrain.bin`/`landuse.bin`.
