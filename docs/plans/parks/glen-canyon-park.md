# Glen Canyon Park — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Glen Canyon Park |
| Slug | `glen-canyon-park` |
| OSM | `way/35800082` |
| Anchor (lon, lat) | `-122.442882, 37.73907` |
| Area | 29.1 ha |
| Bounding span | 724.3 × 1193.9 m (E–W × N–S) |
| Oriented box | 532.7 × 1348.0 m, long axis 153.9° from east |
| Elevation | 69.7–161.9 m (relief 92.1 m, mean 110.8 m) |
| Steepest 50 m grade | 69.1% |
| Baked landcover today | trees 37.4%, grass 36.1%, scrub 20.2%, pitch 4.4%, unclassified 1.9% |
| In `NAMED_PARKS` | yes — `glenCanyon` |
| Effort | Medium. Needs the rock and creek treatment plus a mixed cover recipe. |

**In one sentence:** a wild 29 ha canyon gouged through the southern neighbourhoods, with 92 m of relief, exposed chert outcrops, eucalyptus groves, a creek and playing fields at its southern mouth.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Glen Canyon Park for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Glen Canyon Park read, from the app's high three-quarter diorama camera, as
a wild 29 ha canyon gouged through the southern neighbourhoods, with 92 m of relief, exposed chert outcrops, eucalyptus groves, a creek and playing fields at its southern mouth.

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

- **A gash in the grid.** 724 × 1,194 m span, long axis 153.9°, running roughly north–south. The surrounding streets stop at the rim and resume on the far side.
- **Genuinely wild.** The only park in this set whose current landcover mix is already varied: 37.4% trees, 36.1% grass, 20.2% scrub. That mix is close to right and is worth protecting.
- **Steep and rocky.** 92 m of relief, 69.1% steepest grade, with exposed chert outcrops that no current land kind can express.
- **A creek line.** Islais Creek runs the canyon floor — one of the few daylighted creeks in the city.
- **Fields at the mouth.** The southern entrance has the rec centre and playing fields; the transition from built to wild along the canyon's length is the composition.

## Layer A — ground and planting (rock, creek, and protecting an already-good cover mix)

1. **Add the `rock` kind** (README §E1) and drive it from `natural=bare_rock`/`natural=cliff` where tagged, plus a terrain-grade rule: ground steeper than roughly 55% inside this park bakes as `rock` rather than scrub. The chert outcrops are Glen Canyon's signature and nothing in the current kind list can show them.
2. **Creek.** Islais Creek should bake as a thin `water` ribbon along the canyon floor. The pipeline already treats `waterway` tags as water in `classify()` — verify it survives at creek width and does not disappear into the terrain drape.
3. **Protect the mix.** 37% trees / 36% grass / 20% scrub is unusually good. Improve the *distribution* (groves in the sheltered floor, scrub and grass on the exposed slopes) rather than flattening it into one cover.
4. **Species.** Eucalyptus groves on the canyon floor and lower slopes; nothing on the rock faces.
5. **Drape.** 69.1% steepest grade — the steepest ground in this set. The finer subdivision (README §E6) matters more here than anywhere.
6. **Trails.** Bake the main canyon-floor trail as a `pathdg` ribbon; skip the switchbacks.
7. **Fields.** The rec fields at the southern mouth already bake as 4.4% `pitch`; keep them crisp so the built/wild contrast lands.

## Layer B — hero assets

One small building at the mouth; the canyon itself is landform.

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| Glen Park Recreation Center | — | `-122.440816, 37.737046` | OSM `height=10` | baked building; GLB only if it reads badly |
| Chert outcrops | — | canyon walls | — | landcover `rock`, not a GLB |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Keep the `glenCanyon` `NAMED_PARKS` entry.
2. Add a `VIEW_PRESETS` camera looking north up the canyon from the southern mouth (about `-122.4405, 37.7355`, distance 900 m, pitch about 14°) so the canyon reads as a corridor with walls, not as a green patch.
3. Check the surrounding street bake: the streets on the rim should stop hard at the canyon edge. If roads bridge the canyon where they should not, that is a data issue worth reporting.
4. Consider a small scatter of `rock` prop instances on the steepest faces if the flat rock colour reads too smoothly — only if an instanced prop path already exists.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: 29 ha; the finer subdivision on steep ground is the cost to watch.
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
`glencanyon: [-122.4429, 37.7391]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- The canyon reads as a corridor with walls from the new preset, not as a flat green blob.
- Rock faces are visible on the steepest slopes.
- Islais Creek is followable along the floor.
- The cover mix stays varied — report the post-bake percentages against the current 37/36/20.
- The rec fields at the southern mouth read as a crisp built edge against the wild canyon.

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
- do not homogenise the cover mix into one kind
- do not smooth the terrain; the 69% grades are real
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
| Area | 29.1 ha / 291,218 m² (`way/35800082`) |
| Extent | 724 × 1,194 m span; oriented box 533 × 1,348 m at 153.9° |
| Elevation | 69.7–161.9 m, mean 110.8 m, relief 92.1 m |
| Steepest 50 m grade | 69.1% — the steepest in this set |
| Current landcover | 37.4% trees, 36.1% grass, 20.2% scrub, 4.4% pitch, 1.9% unclassified |
| Rec centre | `-122.440816, 37.737046`, OSM `height=10` |
| Playground | `-122.440504, 37.736682` |
| Named features | 14 in bbox, 163 path ways |

### 2.3 Terrain

- The canyon runs roughly north-north-west to south-south-east; the low point is at the southern mouth (local `-207, 3803`, 69.7 m) and the high ground is on the western rim (161.9 m).
- 92.1 m of relief over a canyon roughly 300–400 m wide gives genuinely steep walls; the 69.1% figure is the real measured maximum over 50 m.
- This is the only park in the set where the terrain does most of the work — get the drape resolution right and much of the character arrives for free.

### 2.4 What the bake produces today

- The cover mix is already the most varied in the city: 37.4% trees, 36.1% grass, 20.2% scrub, 4.4% pitch.
- There is no `rock` kind, so the chert faces bake as scrub or grass.
- Islais Creek's representation depends on whether its `waterway` polygons survive the bake — verify.
- Landcover drape uses the same 55 m max edge as flat ground, on 69% slopes.
- Trees use the single lollipop archetype.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 7 m grid (5964 samples):

| Land kind | Share of park |
|---|---|
| trees | 37.4% |
| grass | 36.1% |
| scrub | 20.2% |
| pitch | 4.4% |
| unclassified | 1.9% |

### 2.5 Recognition cues, ranked

1. A wild canyon interrupting the orderly grid.
2. Steep walls with exposed pale rock.
3. Dark eucalyptus groves on the floor, dry grass and scrub on the exposed slopes.
4. The creek line along the bottom.
5. Playing fields and the rec centre at the southern mouth.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- The real relief and the corridor geometry.
- The varied cover mix.
- The hard boundary where the street grid stops at the rim.
- The built-to-wild gradient from south to north.

**Simplify**

- 163 path ways → the main canyon-floor trail.
- Individual outcrops → `rock` cover driven by grade.
- Creek meander detail → a simplified ribbon.

**Exaggerate (authoring only — never move or rescale the real feature)**

- Rock colour contrast against the vegetation, so the outcrops read at city scale.
- The darkness of the floor groves against the pale dry slopes.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Park boundary | `way/35800082` | `-122.442882, 37.739070` | 29.1 ha |
| Glen Park Recreation Center | way | `-122.440816, 37.737046` | `height=10` |
| Glen Canyon Park Playground | way | `-122.440504, 37.736682` | southern mouth |
| Christopher Playground | way | `-122.440232, 37.743561` | northern end |
| Crags Court Community Garden | way | `-122.44053, 37.741366` | eastern rim |
| Islais Creek | `waterway` | canyon floor | verify it survives the bake |
| "First Dynamite Factory in America" | node | `-122.439947, 37.736214` | historic marker |
| SF Police Academy | way | `-122.441491, 37.744267` | northern rim context |

### 2.8 Ground and planting recipe

1. `trees` for the floor and lower-slope groves.
2. `scrub` and dry `meadowdry` grass on exposed slopes.
3. `rock` where terrain grade exceeds roughly 55%, or where `natural=bare_rock` is tagged.
4. `water` ribbon for Islais Creek.
5. `pitch` for the rec fields, `paved` for the rec centre apron.
6. Eucalyptus-dominant scatter on the floor; nothing on rock.
7. `pathdg` for the main floor trail.
8. Finer drape subdivision throughout.

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
| Glen Park Recreation Center | — | `-122.440816, 37.737046` | OSM `height=10` | baked building; GLB only if it reads badly |
| Chert outcrops | — | canyon walls | — | landcover `rock`, not a GLB |

### 2.11 Budget

- 29 ha at finer subdivision is the main cost; measure the cell payloads before and after.
- Tree count should not increase much — the trees fraction is already 37%.
- No GLBs required.

### 2.12 Integration notes

- `glenCanyon` is already in `NAMED_PARKS`.
- The `rock` kind and the grade-driven rule are shared engine work (README §E1) and also serve the Presidio bluffs.
- The creek ribbon may be more of a `waterway` question than a park question; verify in `classify()` before scoping.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- Post-bake cover percentages reported against the current 37.4/36.1/20.2 baseline.
- A low-angle screenshot showing the canyon walls and rock faces.

### 2.14 Risks and open questions

- The grade-driven `rock` rule is new behaviour and could produce speckled results on noisy terrain; test it on the Presidio bluffs too before shipping.
- Islais Creek may be tagged as a line rather than an area, in which case it needs ribbon treatment rather than polygon classification — check before scoping.
- Finer subdivision on 29 ha of the steepest ground in the city is the largest single triangle risk in this plan set.

### 2.15 Sources

- OpenStreetMap `way/35800082` and an Overpass bbox query (1,084 elements, 163 path ways, 14 named).
- This repository's `terrain.bin`/`landuse.bin`.
- `pipeline/landcover.mjs` `classify()` — verified to have a `waterway` branch but no `natural=bare_rock` branch.
