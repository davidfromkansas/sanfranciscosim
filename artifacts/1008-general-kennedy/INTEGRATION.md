# 1008 General Kennedy Avenue — stage 5 integration: **BLOCKED, not integrated**

Stage 5 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` was attempted, verified locally, and
then **deliberately backed out**. The asset is finished and correct. Integrating it as the
pipeline prescribes would delete three real buildings from the city, which violates AGENTS
rule 5. This file records the evidence and the options, so the next session does not have
to rediscover any of it.

Nothing under `app/` is changed by this branch.

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
value that clears 1008 alone. Confirmed visually: with the manifest entry live and no
exclusion, the ward renders correctly but sits inside a ~16.5 m procedural block that
swallows it, and at night the procedural complex's lit windows bury the asset entirely.

This is not a property of the asset. It is a property of the source footprint being
undivided, and it will recur for every building in a connected historic complex.

## Options for the follow-up, in order of preference

1. **Teach the pipeline to clip rather than drop.** Give `LANDMARKS` an optional
   `excludePoly` (an oriented rectangle, which this asset already has measured in
   `REPORT.md`) and have `buildings.mjs` subtract it from the footprint ring instead of
   discarding the whole building. This is the only option that generalises — the Presidio's
   ward rows, the Letterman complex and any campus will all hit this. It is a real feature
   with a full re-bake behind it, so it deserves its own PR, not a rider on an asset.
2. **Build 1007 and 1009 as sibling assets** and exclude the group together with a radius
   that covers all three. Still deletes the Tides Converge and Thoreau Center blocks, so it
   only helps if those are modelled too — effectively "model the whole complex".
3. **Ship with the double building.** Rejected: at night the procedural mass completely
   hides the asset, so it is worse than not shipping.

Option 1 is the recommendation. Note that this asset is also a good argument for the
kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) for repeated historic pavilions — see
§2.13 of the plan.

## What this branch ships

- `docs/asset-plans/1008-general-kennedy.md` — the plan (stage 1)
- `artifacts/1008-general-kennedy/` — the validated, optimized GLB plus dossier, report,
  deterministic build/render/validate scripts, renders and the optimize pass (stages 2–4)
- this file

The asset is ready to integrate the moment the exclusion problem is solved; its manifest
entry is in `REPORT.md` and needs no changes.
