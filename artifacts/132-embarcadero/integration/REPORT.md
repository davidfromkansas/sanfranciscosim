# 132 The Embarcadero — stage 5 integration (BATCH mode, local only)

**Not pushed, not deployed.** `docs/asset-pipeline/ADDRESS-TO-ASSET.md` replaces
`INTEGRATION-PROMPT.md` Step 7 with a stop: the deliverable is a locally verified,
**source-only** branch plus this evidence, and the ship decision is the owner's.

Case **B** — `132Embarcadero` did not exist in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`, so this needed a registry entry, an exclusion radius and a
tile re-bake.

## QA table

| Item | Result | Evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | fresh-scene re-import, 16/16 contract checks, `artifacts/132-embarcadero/validation.json`; 4,960 tris (cap 27,000), min Z 0.000, XY centre 0.000, 16 `Toy_*` materials, 0 textures, 0 cameras/lights |
| Intake compression | **PASS (no-op)** | `node pipeline/compress-assets.mjs` → `skip (already compressed): landmarks/132-embarcadero.glb`. The stage-4 output already carries `EXT_meshopt_compression` |
| Manifest entry | **PASS** | +19 lines, text-appended so no other entry was reformatted; `estimated: true` because the 29.57 m crest is inferred |
| id → camelId round trip | **PASS** | `camelId('132-embarcadero')` = `132Embarcadero`, which is the registry id; the app reported `placed.has('132Embarcadero') === true` |
| Registry entry + exclusion | **PASS** | `exclude: 7`, inside the measured safe window (1.42 m, 13.74 m) |
| Tile re-bake | **PASS** | full chain `terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes`; `pipeline/out/` regenerated from this branch, `pipeline/data/` symlinked from a warm worktree cache |
| audit check 1.6 | **PASS** | `no procedural footprint inside a bespoke landmark exclusion zone — 114 zones over 110 landmarks clear` |
| verify-rebake | **PASS** | `584 of 585 cells unchanged; 23_10 49 → 48 ← 132Embarcadero`; nearest surviving footprint 20.7 m against a 7 m radius, and it is 17.9 m tall — below this asset's 27.4 m parapet |
| Exactly one building on the site | **PASS** | measured from the tile, not the pixels: no ring in `app/public/tiles/buildings/23_10.bin` has a centroid **or a vertex** within the 7 m radius; nearest centroid 14.13 m, nearest vertex 20.70 m |
| Merge line / draw calls | **PASS** | `sf-assets: 132-embarcadero merged 17 objects / 16 materials -> batched (3355 tris body); uniform x1.0000 at 3956, -2559` |
| Uniform scale ≈ 1.0 | **PASS** | **x1.0000** exactly — the authored crest and `targetHeightM` agree |
| Placement | **PASS** | placed at local (3956, −2559); the anchor projects to (3955.6, −2558.8) |
| Orientation | **PASS** | camera preset yaw 135 (= 180 − 44.95) looks down the Embarcadero elevation's outward normal; the screenshot shows the storefront, the glazed ribbon and the six-bay grid facing the Embarcadero, and the party walls hidden between neighbours |
| Terrain seating | **PASS** | base meets the pavement, no float and no sink (`qa/day.png`) |
| Night glow | **PASS** | only the intended `_Glow` surfaces light: the second-floor ribbon and storefront as one continuous horizontal, plus the scattered upper windows (`qa/night.png`) |
| Draw calls < 300 | **PASS** | **102/frame** averaged over 30 real frames at the landmark (103 in the drill run) |
| Asset warnings, healthy run | **PASS** | none |
| Fallback drill | **PASS** | GLB served as a real 404: app boots, `failed: 1`, `entries: 104`, exactly one `sf-assets: 132-embarcadero failed to load (… 404 …)`, and the Case B site is **empty ground** inside the exclusion zone as designed (`qa/drill-day.png`) |
| `cd app && npm run lint` | **PASS** | clean |
| `cd app && npm test` | **PASS** | 26/26 |
| `cd app && npm run build` | **PASS** | built in 2.19 s |
| Batch-mode sanity check | **PASS** | `git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/` |

## The defect this bake found, and the fix

**Excluding a landmark's footprint can make a surviving neighbour taller.**

`pipeline/buildings.mjs` runs a DataSF pass, then an Overture pass that corrects
heights on parcels DataSF measured before the current building existed: for any
Overture ring with `height >= 20`, it finds the nearest baked footprint within 30 m
and, if the Overture height beats it by 1.4×, overwrites it. `addBuilding()` applies
`excluded()`, so a landmark's own footprint is already gone by the time that pass
runs — and the Overture ring standing on the landmark's site then re-targets the
nearest *survivor*.

Measured here. Overture's rings within 35 m of this anchor:

| Distance | Overture height | Floors | Building |
|---|---|---|---|
| 0.18 m | **28.7 m** | 7 | 132 The Embarcadero (this landmark) |
| 13.74 m | 20.3 m | 4 | 110–116 The Embarcadero |
| 13.92 m | 24.8 m | 7 | Steuart Place |

On `origin/main` the neighbour at 110–116 bakes at its DataSF height, **17.9 m**.
With this landmark's `exclude: 7` and no guard, our own 28.7 m Overture ring lost
its footprint, matched the neighbour 13.7 m away, cleared the 1.4× test
(28.7 > 17.9 × 1.4) and raised it to **29.2 m** — 1.8 m above this asset's own
parapet, along the full 43 m of shared party wall. An 11.3 m error on the one
footprint that touches the landmark.

The fix is four lines in `pipeline/buildings.mjs`: skip an Overture ring whose own
centroid falls inside an exclusion zone. Such a ring *is* the landmark, its height
belongs to the hand-built GLB, and it cannot be added as a footprint either
(`addBuilding` runs `excluded()`), so skipping it outright is the whole correct
behaviour.

**Blast radius, measured rather than assumed.** Baked the whole city both ways and
diffed every footprint in all 585 cells:

- **0 cells** change building count.
- **2 footprints** change height, both corruptions being undone:
  - cell `23_10`: 29.2 → **17.9 m** — this landmark's party-wall neighbour.
  - cell `22_11`: 32.5 → **15.9 m** — a footprint 103 m from the Salesforce Tower
    anchor, inside its 90 m exclusion zone. A pre-existing instance of the same bug,
    shipped before this session.
- Overture height corrections: 260 → 258. Exactly the two.

**This is a shared-file change in a batch branch and the batch integrator needs to
know.** It is not an append-only list, and it changes the bake for every landmark
in the batch — always in the direction of restoring a measured DataSF height that
an exclusion had displaced. It is committed here because shipping a landmark that
visibly corrupts the neighbour it shares a wall with is worse than the merge risk,
but it is the owner's call to keep it.

## Batch mode

The bake ran and was fully QA'd, then discarded:

```
git checkout -- app/public/tiles api/_data
```

Committed source only: the GLB, the manifest entry, the registry entry, the asset
plan, `artifacts/132-embarcadero/`, and the `pipeline/buildings.mjs` guard above.
The city is baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

## Notes for the batch integrator

1. **`pipeline/buildings.mjs` carries a four-line behaviour change** — see above.
   Re-run the two-way diff after merging the batch; more exclusions mean more
   opportunities for the bug, so the corrected-footprint count should rise, and
   every entry in it should be a neighbour of a landmark.
2. **`pipeline/lib/landmarks.mjs` gained `132Embarcadero`** with `exclude: 7`. Do
   not round that up: 14 would delete 110–116 The Embarcadero from the bake.
3. **A parallel branch `pipeline/121-steuart` exists and is the same building.**
   121 Steuart Street and 132 The Embarcadero are both parcel 3715-003. Only one
   can ship; the other must be retired rather than merged.
4. `node pipeline/compress-assets.mjs` re-compresses
   `app/public/sf-assets/vehicles/passenger-airplane.glb` as a side effect. It was
   reverted here and is not in this branch.

## Observations, not defects

- **Night reads cool against a warm city.** The landmark's lit glass is
  `#6f95b8`, so at 21:45 it glows blue-white while the procedural neighbours glow
  warm yellow. That is the repo's established landmark convention (`#6f95b8` on 72
  of the shipped glow materials) and it is also true to life for an office block
  next to converted warehouses — but it is the most visible difference between this
  asset and its surroundings at night.
- **The pale roof dominates from far out.** At the 900 m wide shot the `Toy_sand`
  deck is most of what the building shows, and the red brick that carries the
  identification is barely visible. `Toy_roofd` is not the alternative — it measures
  rgb(9,9,12) on a horizontal deck in this app — but if the owner wants the brick to
  read at district scale, `Toy_stone` on the deck is the next thing to try.
- **The 2:30 PM frame is dark.** The Embarcadero elevation faces northeast, so it
  is in shade all afternoon; the whole block including the roadway renders dark in
  that frame. The neighbours are equally dark, so this is the scene's lighting at
  that hour, not the asset.
