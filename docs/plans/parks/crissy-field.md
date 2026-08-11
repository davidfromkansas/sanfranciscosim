# Crissy Field — park plan

<!--
Generated as a planning document. Nothing here has been built yet: no pipeline
code, tile data, GLB or app code has been changed by this plan.
-->

| Field | Value |
|---|---|
| Park | Crissy Field |
| Slug | `crissy-field` |
| OSM | `way/32649967` |
| Anchor (lon, lat) | `-122.464058, 37.804463` |
| Area | 10.9 ha |
| Bounding span | 752.6 × 365.5 m (E–W × N–S) |
| Oriented box | 796.9 × 241.3 m, long axis 13.6° from east |
| Elevation | 3.1–4.9 m (relief 1.8 m, mean 3.9 m) |
| Steepest 50 m grade | 15.4% |
| Baked landcover today | grass 100% |
| In `NAMED_PARKS` | yes — `crissyField` |
| Effort | Medium. Small area, but it needs the new marsh kind and a careful shoreline. |

**In one sentence:** a flat 1 km strip of shoreline lawn, restored tidal marsh and beach between the Presidio bluff and the Bay, with the Golden Gate Bridge looming immediately to the west.

---

## Part 1 — Task prompt (copy this into a fresh session)

````markdown
# Build Crissy Field for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Make Crissy Field read, from the app's high three-quarter diorama camera, as
a flat 1 km strip of shoreline lawn, restored tidal marsh and beach between the Presidio bluff and the Bay, with the Golden Gate Bridge looming immediately to the west.

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

- **Flat.** Measured relief inside the OSM polygon is 1.8 m over 10.9 ha — the flattest ground in this plan set. Everything else in the frame (bluff, bridge, city) is vertical by comparison.
- **A layered strip**, north to south: Bay, beach, promenade, lawn/airfield, marsh, Mason Street, Presidio bluff.
- **The former airfield** reads as an unnaturally rectangular green plain — that geometry is the historical cue and should stay crisp.
- **Crissy Marsh** as a distinct olive-green tidal shape, not lawn and not open water.
- **The bridge**, immediately west and enormous, is the backdrop the whole park is composed against.

## Layer A — ground and planting (the marsh kind, the shoreline and a mostly flat ground plan)

1. **Add the `marsh` land kind** (README §E1) and handle `natural=wetland` in `classify()`. Crissy Marsh (`relation/12622483`, 6.4 ha, tidal flat) currently bakes as *nothing* — the tag is dropped. This is the single most visible fix for this park.
2. **Shoreline.** The beach is `natural=beach`/`sand` and already classifies; verify it survives and meets the water plane cleanly with no z-fighting at the tide line.
3. **Airfield geometry.** Keep the rectangular lawn's edges straight and its interior uniform. Resist scattering trees across it — the historic airfield is defined by its emptiness.
4. **Trees.** Only the scattered Monterey cypress windbreaks along the southern edge and around the historic buildings; `cypress` species, low density, deliberately sparse.
5. **Promenade.** The waterfront promenade is the one path here that must read: bake it as a `pathdg` ribbon running the full length just inland of the beach.
6. **Scope check.** The OSM `Crissy Field` way (`way/32649967`) covers only the western portion (`-122.4687` to `-122.4602`); Crissy Marsh sits east of it at `-122.4568`. Decide the working boundary explicitly and record it — the plan assumes the full shoreline from Fort Point to the Marina, not just the OSM polygon.

## Layer B — hero assets

Crissy Field's buildings are small, low and historic. None of them is a monument; treat them as a cluster.

| Hero asset | Slug | Anchor (lon, lat) | Measured footprint | Status |
|---|---|---|---|---|
| Historic hangar / Coast Guard cluster | `crissy-hangars` | `-122.46740, 37.80560` | 5 buildings, OSM `height` 5–10 m | **new** — one small multi-building GLB, or baked |
| Greater Farallones Visitor Center | — | `-122.467059, 37.805428` | `height=10` | part of the cluster |
| 1890 Boathouse | — | `-122.467641, 37.805748` | `height=5` | part of the cluster |
| Coast Guard Pier | — | `-122.466519, 37.805969` | `man_made=pier` | baked pier geometry, not a GLB |
| Golden Gate Bridge | `golden-gate-bridge` | existing asset | — | already shipped — do not modify |

Every hero GLB follows the normal asset route: author it per
`.agents/skills/sf-asset-check/SKILL.md` under `artifacts/<slug>/` with a
deterministic Blender build script, review renders, `validation.json` and
`REPORT.md`, then integrate it with `docs/asset-plans/INTEGRATION-PROMPT.md`.
Assets that already have a plan are listed with their file — do not re-research
those, run their plan.

## Layer C — placement, camera and scatter

1. Keep the `crissyField` `NAMED_PARKS` entry.
2. Add a `VIEW_PRESETS` camera looking west along the shoreline with the bridge filling the left of frame (about `-122.4600, 37.8045`, distance 900 m, low pitch ~14°). This park is the best bridge-context view in the city and deserves a preset.
3. The marsh needs a tidal inlet connecting it to the Bay — it is the shape that makes it read as a marsh rather than a pond. Bake the channel, do not model it.
4. Keep the lawn empty. If the diorama camera makes it look bare, add life at the promenade edge (benches, a few instanced figures from the existing prop vocabulary), never in the middle of the airfield.

## Budgets and gates

- Draw calls stay under 300 with the park filling the screen; the park's ground
  and trees stay merged/instanced per cell (`app/src/city.js` already does this
  — do not add per-feature meshes).
- Report the before/after byte size of the `landcover`/`toyland` tiers for the
  cells this park touches. Gate: Crissy Field is small; its landcover payload should grow by less than 50% even with the marsh added.
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
`crissyfield: [-122.4640, 37.8045]`
Do a full bake before shipping, and commit the regenerated files under
`app/public/tiles/` that changed.

Then, with `cd app && npm run dev`:

- Crissy Marsh renders as olive marsh with a tidal channel, not as bare ground or a blue pond.
- Beach, promenade, lawn and marsh read as four distinct parallel bands from the diorama camera.
- The bridge sits correctly in frame from the new preset with no seam against the shoreline.
- No green landcover triangles hang over the water at the shoreline.
- Night: the park is dark, with the bridge lighting dominant.

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
- do not modify the Golden Gate Bridge asset
- do not plant trees across the airfield lawn
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
| Area (OSM `way/32649967`) | 10.9 ha / 109,358 m² |
| Extent | 753 × 366 m bounding span; oriented box 797 × 241 m at 13.6° |
| Elevation range | 3.1–4.9 m, mean 3.9 m — relief 1.8 m |
| Steepest 50 m grade | 15.4% (only at the inland edge) |
| Crissy Marsh | `relation/12622483`, `natural=wetland`, `wetland=tidalflat`, 64,222 m², 644 × 134 m oriented box, anchor `-122.455556, 37.80466` |
| Current landcover | 100% `grass` inside the OSM polygon |
| Named features | 9 named, mostly the historic maritime cluster |

### 2.3 Terrain

- 1.8 m of relief across the whole park: this is reclaimed flat ground and must not be given artificial undulation.
- The land rises sharply immediately south into the Presidio bluff — that contrast is the park's section.
- Water level in the app is y=0; the park sits at 3–5 m, so the beach slope between them is only a few metres and needs care to avoid a visible step.

### 2.4 What the bake produces today

- The entire OSM polygon bakes as `grass` — 100% of samples.
- Crissy Marsh is not baked at all: `classify()` has no branch for `natural=wetland`, so the polygon is skipped.
- The beach and shoreline west of the polygon classify as `sand` where tagged.
- The historic buildings come through the ordinary building bake.

The measured landcover mix inside the park boundary, sampled from the committed
`app/public/tiles/landuse.bin` on a 5 m grid (4374 samples):

| Land kind | Share of park |
|---|---|
| grass | 100% |

### 2.5 Recognition cues, ranked

1. A flat green strip pinned between the Bay and the Presidio bluff.
2. The Golden Gate Bridge immediately west, dominating the frame.
3. The olive tidal marsh with its channel to the Bay.
4. The rectangular former-airfield lawn.
5. The low white historic hangars and the promenade line.

### 2.6 Preserve / simplify / exaggerate

**Preserve**

- Flatness and the parallel band structure.
- The marsh outline and its tidal connection.
- The airfield rectangle.
- The real distance and sightline to the bridge.

**Simplify**

- 61 path ways → the promenade only.
- The historic cluster → one small building group.
- Dune and marsh vegetation detail → flat colour bands.

**Exaggerate (authoring only — never move or rescale the real feature)**

- The marsh's colour separation from lawn, so it reads at city scale.
- The crispness of the airfield rectangle.
- The beach's width, slightly, so the sand band survives at distance.

### 2.7 Feature inventory with real anchors

| Feature | OSM | Anchor (lon, lat) | Note |
|---|---|---|---|
| Crissy Field (OSM polygon) | `way/32649967` | `-122.464058, 37.804463` | 10.9 ha, western portion only |
| Crissy Marsh | `relation/12622483` | `-122.455556, 37.80466` | 6.4 ha tidal flat |
| Greater Farallones Visitor Center | way | `-122.467059, 37.805428` | `height=10`, museum |
| Ocean Climate Center | way | `-122.467432, 37.805623` | `height=7` |
| 1890 Boathouse | way | `-122.467641, 37.805748` | `height=5` |
| Shop and Garage | way | `-122.466766, 37.805468` | `height=6` |
| Coast Guard Pier | way | `-122.466519, 37.805969` | `man_made=pier` |
| Military Intelligence Service Learning Center | way | `-122.462707, 37.802831` | `height=7` |
| Fort Point Coast Guard Station Historic District | `way/934681747` | `-122.466802, 37.805895` | district |
| Golden Gate Bridge | existing GLB | — | west backdrop |

### 2.8 Ground and planting recipe

1. Bands from north to south: `water` (Bay), `sand` (beach), `pathdg` (promenade), `grass` (airfield lawn), `marsh` (Crissy Marsh with channel), `paved` (Mason Street), then Presidio forest.
2. Cypress windbreak scatter along the southern edge only, low density.
3. Historic buildings as a pale cluster with dark roofs.
4. No flower-bed accents here — the palette stays cool and restrained.

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
| Historic hangar / Coast Guard cluster | `crissy-hangars` | `-122.46740, 37.80560` | 5 buildings, OSM `height` 5–10 m | **new** — one small multi-building GLB, or baked |
| Greater Farallones Visitor Center | — | `-122.467059, 37.805428` | `height=10` | part of the cluster |
| 1890 Boathouse | — | `-122.467641, 37.805748` | `height=5` | part of the cluster |
| Coast Guard Pier | — | `-122.466519, 37.805969` | `man_made=pier` | baked pier geometry, not a GLB |
| Golden Gate Bridge | `golden-gate-bridge` | existing asset | — | already shipped — do not modify |

### 2.11 Budget

- Small area; the added marsh geometry is a handful of triangles.
- Tree count barely changes.
- One optional small GLB cluster.

### 2.12 Integration notes

- `crissyField` is already in `NAMED_PARKS`.
- The marsh kind is shared engine work (README §E1) and also serves the Presidio plan.
- If the hangar cluster ships as a GLB it is Case B in `docs/asset-plans/INTEGRATION-PROMPT.md`.

### 2.13 Validation checklist

- Re-baked cells load with no console 404 and no tile-format warning.
- Draw calls stay under 300 with the park filling the frame (stats overlay, `F3`).
- Frame rate unchanged at street level in the Mission and downtown stress cells.
- No per-frame allocation added: trees, paths and props stay instanced/merged.
- Every hero GLB independently passes `sf-asset-check` after re-import.
- Fallback drill: removing the new tier degrades to plain baked ground with one warning.
- Day and night screenshots from the diorama camera on the deployed site.
- The marsh appears in the landuse raster after the bake (it is currently absent).
- No shoreline z-fighting between beach, water plane and landcover.

### 2.14 Risks and open questions

- The OSM `Crissy Field` polygon does not cover the marsh or the eastern shoreline; using it as the working boundary would leave out the park's best feature. The boundary decision must be explicit.
- Water-plane interaction at 3–5 m elevation is fiddly; expect iteration at the tide line.
- The `marsh` kind is new engine work shared with the Presidio — coordinate so it is implemented once.

### 2.15 Sources

- OpenStreetMap `way/32649967`, `relation/12622483`, and the Crissy Field building ways via the OSM API and an Overpass bbox query (99 elements, 9 named).
- This repository's `terrain.bin`/`landuse.bin` for elevation and current bake state.
- `pipeline/landcover.mjs` `classify()` — verified to have no `natural=wetland` branch.
