# TREE-CLEANUP-PROMPT — remove trees from roads, buildings, and water

You are working in the `sanfranciscosim` repo. Read `AGENTS.md` at the repo root first — the iron rules there override everything, especially rule 2 (perf budgets, see `docs/plans/PERF-PLAN.md` THE GUARDRAIL), rule 3 (procedural fallback), rule 5 (data accuracy), and rule 6 (commit hygiene + deploy/report format). Read `.agents/skills/testing-sf-3d/SKILL.md` before QA.

## Mission

Trees currently appear in places they obviously don't belong: standing in roadways, poking through house roofs, giant lollipops perched on rooftops, and occasionally floating in the bay. Fix the placement logic in the bake pipeline and the one runtime scale bug, re-bake the tiles, and prove the cleanup with before/after screenshots on the deployed site.

This is a **placement cleanup only**. Do not redesign the tree look, do not touch the tree archetypes' shapes/colors, do not add species variety (a separate flora-kit effort owns that — see `docs/asset-plans/flora-kit.md`; if `app/src/flora.js` exists on main when you start, stop and flag the conflict in the PR instead of merging around it blindly).

## How trees flow through the system (read this so you don't rediscover it)

1. `pipeline/landcover.mjs` scatters trees inside OSM landcover polygons (`natural=wood`/`landuse=forest` at 1 per 90 m², parks/grass at 1 per 200 m²) → written per cell into `out/landcover/*.bin` as (x, y, z, variant) with variant 0–2 random.
2. `pipeline/toy.mjs` reads those blobs and writes the diorama tier `out/toyland/*.bin`: it duplicates roughly every other tree with a seeded 6 m nudge (the "1.5× density" pass, ~line 613–625), and appends **roof-garden trees** collected during the building bake (`addGarnish`, ~line 290–305: 15% of flat-roofed buildings get a garden slab + 2–4 trees at `roofY + 0.3`), appended with variant `2` (~line 625).
3. `pipeline/toy.mjs` publishes `out/toyland/` → `app/public/tiles/toyland/` (and `pipeline/validate.mjs` publishes the base tier). Tiles are committed to the repo.
4. Runtime: `app/src/city.js` builds one `InstancedMesh` of the lollipop archetype per ground group (~line 531–558). Scale comes from the variant: `s = 0.62 + variant * 0.26 + jitter` — **linear in variant**.

The app boots the diorama tier only, so `toyland` is what users see; the base tier is the fallback and gets the same fixes for free since toyland derives from it.

## The three root causes (all confirmed in code on main)

**A. Roof trees render giant.** `addGarnish` intends "small trees" on rooftop gardens, but they're baked as variant 2 — the *largest* scale bucket. The runtime formula makes them 1.14–1.49× of an ~11 m archetype: 13–17 m lollipops standing on rooftops, including on small flat-roofed houses (the garnish only requires a ~6×6 m roof after inset). This is the "trees on top of houses" complaint.

**B. The base scatter tests nothing but the source polygon.** `scatterTrees` (`pipeline/landcover.mjs` ~line 247) accepts any point inside the outer ring and outside the holes. But OSM park polygons contain their internal roads (roads are separate ways, not holes — JFK Drive runs *through* the Golden Gate Park polygon), and `landuse=grass` / `landuse=cemetery` / `natural=wood` polygons routinely overlap parcels that contain buildings (Presidio housing sits inside forest polygons). So trees are planted in roadways and inside building footprints — a terrain-height tree inside a 2-storey house pokes through its roof and reads as "a tree on the house". There's also no water test, which is where the occasional bay tree comes from (the audit's note 1.7b already counts these).

**C. The densifier nudge escapes the polygon.** The toy tier's extra-density pass moves each duplicate 6 m in a seeded random direction with **no re-test at all** — any source tree within 6 m of a park boundary can spawn its duplicate in the adjacent street or building.

## The fix

### 1. New shared module: `pipeline/lib/treeblockers.mjs`

A tree-placement veto oracle, used by both bake steps. API:

```js
export async function loadTreeBlockers({ sampleElevation });
// returns  blocked(x, z) -> boolean   (world meters, same space as everything else)
```

Implementation:

- **Building occupancy grid.** Read every `out/buildings/*.bin` with `readBuildingsBlob` (see `pipeline/audit.mjs` for a working example of decoding footprint rings from those blobs). Rasterize each footprint into a citywide occupancy grid at **2.5 m** resolution (point-in-ring test per grid-cell center over the ring's bbox — reuse the `pointInRing` pattern from `landcover.mjs`). Dilate by one grid cell so trees can't hug a wall so tightly the canopy clips through it.
- **Street corridors.** Read every `out/streets/*.bin` with `readStreetsBlob`. For each polyline segment of **every** class, mark grid cells within `classWidth / 2 + 1.5` m of the segment (class widths are in `pipeline/lib/classes.mjs`: freeway 22 … other 6). Include freeways and ramps — they're elevated, and a tree poking through a deck looks as wrong as one in a lane. Do NOT widen further than the ribbon + 1.5 m: sidewalk street trees are real and welcome; only the roadway itself is forbidden.
- **Water.** `blocked` also returns true when `sampleElevation(x, z) < 0.35` (water level is y = 0; landcover sits at +0.06, water surfaces at ≥ 0.25).

Memory note: the city extent at 2.5 m is on the order of a few hundred MB as bytes if you allocate naively per-city — use one flat `Uint8Array` for the whole extent like `buildings.mjs` does with its 5 m occupancy raster (`OCC_RES` section, ~line 177). If a flat 2.5 m grid is too large for the pipeline's memory comfort, 3 m is acceptable; do not go coarser.

### 2. `pipeline/landcover.mjs` — veto scatter candidates

In `scatterTrees`, after the hole test, reject the candidate when `blocked(x, z)`. Keep everything else identical — same hash sequence, same attempt cap, same seeding — so untouched areas bake byte-identically. A polygon may now place fewer trees than its target; that is the intended outcome, not a bug to compensate for.

### 3. `pipeline/toy.mjs` — veto the nudged duplicates

In the densifier loop (~line 619), skip the duplicate when `blocked(nudgedX, nudgedZ)`. Load the blockers once at the top of the landcover section (streets and buildings bakes have already run by this point in `npm run all`; in `--only=streets` mode the landcover section doesn't run, so guard the load accordingly). Do not change the hash calls or their order — determinism elsewhere must be preserved.

### 4. `pipeline/toy.mjs` — fix the roof trees

In `addGarnish`:
- Only emit rooftop-garden **trees** when the building has **4 or more floors** (pass `floors` into `addGarnish`; the garden slab itself may stay on any qualifying roof — a green slab is fine, a tree on a garage is not).
- Where roof trees are appended to the toyland blobs (~line 625), bake them as **variant 3** instead of 2. Variant is a uint8 in the blob format (`writeLandcoverBlob` / `readLandcoverBlob` in `pipeline/lib/`), so no format change is needed; 3 is currently unused (the base scatter rolls 0–2).

### 5. `app/src/city.js` — small scale for variant 3

In the instancing loop (~line 536–547), special-case variant 3 (roof trees): use a small scale, e.g.

```js
const s = variant === 3
  ? 0.34 + ((x * 7.3 + z * 3.1) % 1) * 0.12   // roof-garden tree: reads as a shrub from the aerial camera
  : 0.62 + variant * 0.26 + ((x * 7.3 + z * 3.1) % 1) * 0.35;
const sy = variant === 3 ? s : s * (0.85 + variant * 0.2);
```

Variants 0–2 must render exactly as before. Base-tier blobs never contain variant 3, so the base path is unaffected.

### 6. `pipeline/audit.mjs` — make the cleanup a permanent gate

Add checks (follow the existing `check(id, ...)` style):

- **Trees clear of buildings:** sample every ~200th tree across all `out/toyland/*.bin`; every sampled tree with variant ≤ 2 must NOT sit in the building occupancy grid. Zero tolerance.
- **Roof trees on roofs:** every sampled variant-3 tree MUST sit inside the building occupancy grid (inverse check — a floating "roof" tree means the bake and the buildings disagree).
- **Trees clear of roadways:** every sampled variant ≤ 2 tree must be outside all street corridors (same corridor definition as the blocker).
- **Upgrade note 1.7b** (trees sampled >30 m offshore) from a `note` to a hard `check` expecting **0**.
- Existing check 1.1c (`tree instances > 30,000`) must still pass — if the cleanup drops the count below that, something is over-aggressive; investigate rather than lowering the threshold.

## What NOT to do

- Do not modify the tree archetype geometry, the tree material, or add assets/dependencies.
- Do not filter trees at runtime — placement is a bake-time concern; the runtime change is the variant-3 scale only.
- Do not touch `app/src/streetkit.js`, the landmark loader, or any landmark GLB/manifest.
- Do not "fix" trees near bespoke landmark grounds (e.g. inside exclusion radii) in this task — landmark integrations own their own suppression; note anything you spot in the PR instead.
- Do not delete or weaken the procedural fallback paths (iron rule 3).

## Re-bake and publish

```
cd pipeline && npm ci && npm run all
```

This re-downloads source data (Overpass can throttle — retry; a free DataSF app token helps, see AGENTS.md gotchas) and re-publishes both tiers into `app/public/tiles/`. A full re-bake will also pick up unrelated upstream OSM edits — that is accepted practice in this repo (precedent: the exclusion-zone re-bake commit `7f8c357`), but state it in the PR.

Record in the PR description:
- tree totals before → after for the base bake (`landcover.mjs` log line) and the toy bake (`toy.mjs` "toy landcover" log line);
- a sane delta is roughly **3–20% fewer** trees. If more than ~40% vanished, the corridor widths or occupancy dilation are too aggressive — stop and investigate.

## Visual QA (deployed site, day AND night, per AGENTS.md QA norms)

Deploy with `vercel deploy --prod`, report the production URL as the first line of your summary. Take **before/after screenshot pairs** (before = current production) at each of these known-bad spots, using the search box / concierge or manual navigation:

1. **Golden Gate Park — JFK Drive near the Conservatory of Flowers**: the drive should be clear of trees; the lawns stay densely treed.
2. **Golden Gate Park — Crossover Drive (Hwy 1) and MLK Jr Drive**: same.
3. **The Panhandle at Oak St and Fell St**: no trees standing in either roadway edge.
4. **Dolores Park perimeter (Church St / 20th St)**: streets and the rail reservation clear; park lawns still treed.
5. **Alamo Square perimeter (Hayes / Steiner)**: streets clear; confirm the painted-ladies landmark view is unchanged.
6. **Presidio — Lincoln Blvd and the housing clusters**: no trees inside the houses that sit within the forest polygons; forest still dense around them.
7. **Downtown / SoMa rooftop sweep (aerial)**: zero giant rooftop lollipops anywhere; towers ≥ 4 floors may show small shrub-scale garden trees on green slabs.
8. **Sunset & Richmond residential blocks**: no canopies poking through row-house roofs.
9. **Shoreline sweep (Marina Green, Ocean Beach, Mission Bay)**: zero trees standing in water.

Then the standard gates:
- Stats overlay at street level in the Mission and downtown: < 300 draw calls, 60 fps steady (tree instance counts only went down, so any regression is a bug you introduced).
- Cold cache-cleared load boots the diorama first-frame.
- Picking, search, and cards still work.
- Fallback drill: temporarily rename one `toyland` tile → that cell degrades to base landcover with one console warning, no hole, no crash; restore it after.

## Acceptance checklist (report PASS/FAIL per line in the PR)

| # | Gate |
|---|------|
| 1 | Audit: 0 sampled ground trees inside building footprints |
| 2 | Audit: 0 sampled ground trees inside street corridors |
| 3 | Audit: 0 sampled trees offshore (1.7b now a hard check) |
| 4 | Audit: all variant-3 trees inside a building footprint; 1.1c still passes |
| 5 | Roof trees only on ≥ 4-floor buildings and rendered at shrub scale |
| 6 | All 9 before/after screenshot pairs show the cleanup, day and night |
| 7 | Tree-count delta within the sane band and reported |
| 8 | Perf gates hold (stats overlay evidence at both stress cells) |
| 9 | Fallback drill passes |
| 10 | Commit hygiene: noreply author email, PR from a `devin/*` branch |

Work on a `devin/*` branch. Keep the diff surgical: `pipeline/lib/treeblockers.mjs` (new), `pipeline/landcover.mjs`, `pipeline/toy.mjs`, `pipeline/audit.mjs`, `app/src/city.js`, plus the re-baked tiles. An honest FAIL with an explanation beats a hidden one.
