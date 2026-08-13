# 1008 General Kennedy Avenue — stage 5 integration: **INTEGRATED**

Stage 5 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` is complete. The asset ships, the
registry carries a 20 m exclusion zone, and the tiles were re-baked so the procedural mass
under the model is gone.

This originally shipped **blocked**: the exclusion that stage 5 prescribes removes the
entire Letterman/Thoreau campus, because DataSF stores all twelve surviving buildings as a
single footprint. That is a real cost, so it was escalated rather than decided quietly.

**David's decision, 12 Aug 2026: delete the whole campus blob.** Asked to choose between
losing the eleven neighbours, teaching the pipeline to clip footprints, modelling the
campus, or leaving the site alone, he chose the first. The section below is kept because
the measurements are the justification for that call, and because the clipping option is
still the better long-term fix for the Presidio's other ward rows.

The first attempt at this branch was also wrong in a way worth recording: it shipped the
plan and the artifacts but nothing under `app/`, so the merge changed the deployed site not
at all. A landmark is not integrated until the manifest, the registry and the tiles all
move together.

## What was verified locally (and it all passed)

The GLB was copied into `app/public/sf-assets/landmarks/`, the manifest entry from
`REPORT.md` was added, and the dev server was run at the site.

| Check | Result | Evidence |
|---|---|---|
| Streams in correctly | **PASS** | lifecycle went `far` → `loading` → `live` as the camera approached inside `loadRadius` 2500 m |
| Merge line | **PASS** | `sf-assets: 1008-general-kennedy merged 10 objects / 10 materials -> batched (3544 tris body); uniform x1.0000 at -1230, -3403` |
| Scale factor | **PASS** | **exactly `x1.0000`** — the authored crest and `targetHeightM` agree |
| Placement | **PASS** | lands at local `(-1230, -3403)`, the projection of the manifest anchor |
| Orientation | **PASS** | the ward runs along its real heading, parallel to 1007 and 1009, head toward General Kennedy Avenue |
| Footprint size vs neighbours | **PASS** | reads correctly against the street width and the neighbouring Presidio blocks |
| Terrain seating | **PASS** | no floating, no sinking |
| Night glow | **PASS** | only the intended `_Glow` surfaces light |
| Draw calls | **PASS** | merges into the existing landmark `BatchedMesh` — **adds zero new draw calls** |
| **Exactly one building at the site** | **FAIL** | see below |

## The blocker

**The procedural footprint at this site is the entire Thoreau Center, as one polygon.**

Decoded directly from the shipped tile `app/public/tiles/buildings/13_9.bin`
(magic `SFB1`, v1, 29 buildings in the cell), building index 20 is:

- 69 vertices, bounding box **159 × 147 m**
- base 8.3 m, top 24.8 m
- **nearest vertex is 4.7 m from this asset's anchor**

That single footprint covers 1007, **1008**, 1009, the Tides Converge block at 1012 Torney,
and the Thoreau Center block at 1016 Lincoln — about 5,845 m² of real buildings. It comes
from DataSF (`ynuv-fyni` building `201006.0000207`); the whole baked city is DataSF-sourced
(`overtureAdded: 0` in `app/public/tiles/buildings.json`), and OSM way `288374440` and
Overture both draw the complex the same undivided way.

`excluded()` in `pipeline/buildings.mjs` drops a footprint **whole** when its centroid *or
any vertex* falls inside a landmark's `exclude` radius:

```js
if ((cx - e.x) ** 2 + (cz - e.z) ** 2 < e.r2) return true;
for (let i = 0; i < ring.length; i += 2) {
  if ((ring[i] - e.x) ** 2 + (ring[i + 1] - e.z) ** 2 < e.r2) return true;
}
```

Because the nearest vertex is 4.7 m away, **any exclusion radius above ~5 m deletes the
entire complex** — and a radius below that leaves the procedural mass in place. There is no
value that clears 1008 alone.

**Compare `550Third` in `pipeline/lib/landmarks.mjs`**, which solved the neighbouring
version of this problem and is the right thing to measure against. There, the target
footprint's centroid sits 0.96 m from the anchor and the nearest *neighbour* vertex is
11.17 m, so any radius in ~1–11 m drops that building alone. The same measurement here:

| | 550 Third Street | **1008 General Kennedy** |
|---|---|---|
| Anchor → target footprint centroid | 0.96 m | 41.1 m |
| Anchor → nearest vertex that must survive | 11.17 m (a neighbour) | **4.68 m (the same footprint)** |
| Usable radius window | ~1–11 m | **none** |

The window is empty because the vertex that must survive belongs to the *same* footprint as
the building being replaced. 1008 is not a separate footprint, so no radius can separate
them. Confirmed visually: with the manifest entry live and no
exclusion, the ward renders correctly but sits inside a ~16.5 m procedural block that
swallows it, and at night the procedural complex's lit windows bury the asset entirely.

This is not a property of the asset. It is a property of the source footprint being
undivided, and it will recur for every building in a connected historic complex.

## The options that were put to David

1. **Teach the pipeline to clip rather than drop.** Give `LANDMARKS` an optional
   `excludePoly` (an oriented rectangle, which this asset already has measured in
   `REPORT.md`) and have `buildings.mjs` subtract it from the footprint ring instead of
   discarding the whole building. This is the only option that generalises — the Presidio's
   ward rows, the Letterman complex and any campus will all hit this. It is a real feature
   with a full re-bake behind it, so it deserves its own PR, not a rider on an asset.
2. **Build 1007 and 1009 as sibling assets** and exclude the group together with a radius
   that covers all three. Still deletes the Tides Converge and Thoreau Center blocks, so it
   only helps if those are modelled too — effectively "model the whole complex".
3. **Drop the whole campus footprint.** ← **chosen.** One radius, no new pipeline feature,
   the asset is visible immediately. The cost is the eleven neighbours.
4. **Ship with the double building.** Rejected on the numbers: the procedural mass is
   16.5 m against the asset's 11.9 m, so the model sits entirely inside it and is invisible
   by day and night. This is why simply adding a manifest entry would not have worked.

Option 1 remains the better long-term fix and is still worth its own PR; option 3 was taken
because it makes this building visible now without one. This asset is also a good argument
for the kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) for repeated historic pavilions
— see §2.13 of the plan.

## What the exclusion actually did

`exclude: 20` on `1008GeneralKennedy`, verified by decoding cell `13_9` before and after
the bake:

| | before | after |
|---|---|---|
| Campus footprint (69 verts, 159×147 m, 16.5 m tall) | present, 4.70 m from the anchor | **gone** |
| Nearest surviving neighbour | 51.52 m | 51.52 m, untouched |
| Footprints within 150 m of the anchor | 11 | 12 |

The count rises rather than falls because clearing the campus frees the `markOccupied`
bitmap over that block, so the Overture gap-fill pass contributes a few separate lower
buildings back into the cleared area. None of them land within 51 m of the anchor, so 1008
stands clear — and the hole reads as a partly-rebuilt block rather than an empty lot.

## Two defects the first integration attempt shipped, and their fixes

Both were caught by verifying in the running app rather than by reading the bake logs,
which reported success throughout.

**1. The GLB was in the wrong directory.** `assets.js:442` loads
`sf-assets/landmarks/${entry.file}`; it was copied to `sf-assets/` instead. Vite answered
with `index.html`, so the loader failed on `Unexpected token '<'` and fell back to the
procedural building — which had just been excluded, leaving an empty site. The fallback
itself behaved exactly as AGENTS rule 3 requires: one console warning, no hole, no crash.

**2. Dropping the campus footprint also dropped its tree veto.** `loadTreeBlockers()` uses
building footprints to keep the Presidio canopy out of buildings, so removing the campus
ring let trees scatter straight through the ward — 23 instances measured inside the shell.
The fix is `clearTrees: true`, an opt-in flag that clears trees inside `exclude` (the
Palace of Fine Arts is the only other user). That also forced `exclude` up from 20 m to
34 m: the flag reuses `exclude` as its radius, and at 20 m the circle was smaller than the
model's own 32.8 m half-diagonal. After the fix, 0 trees stand inside the footprint.

Re-running `buildings.mjs` at 34 m produced **byte-identical** output to the 20 m run, which
is what made the fix cheap — the dropped set was unchanged, so `lore` (80 min), `notables`
and `context` did not need re-running. Only `landcover` → `validate` → `toy` were repeated.

**Known cosmetic residue:** one lamp (`lamps-*` instance plus its light pool) stands 1.4 m
inside the *bounding box* at the far end of the ward. Baked lamps are not covered by
`clearTrees` and the kit is inactive (`kitInstances: 0`), so no existing hook removes it;
it is not visible from the diorama camera. Worth folding into the `excludePoly` work.

**Watch out:** `validate.mjs`/`toy.mjs` republish `app/public/tiles/` and delete the 603
files `context.mjs` writes (`context.json`, `context/`, `ctx/`). Re-run `node context.mjs`
last or the app dies at boot fetching `tiles/context.json`.

## What this branch ships

- `docs/asset-plans/1008-general-kennedy.md` — the plan (stage 1)
- `artifacts/1008-general-kennedy/` — the validated, optimized GLB plus dossier, report,
  deterministic build/render/validate scripts, renders and the optimize pass (stages 2–4)
- `app/public/sf-assets/1008-general-kennedy.glb` + its `landmarks_manifest.json` entry
- `pipeline/lib/landmarks.mjs` — the registry entry with the 20 m exclusion zone
- the re-baked tiles
- this file
