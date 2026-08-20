# 49 Zoe Street — integration report (stage 5, batch mode)

Run of `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 with `<slug> = 49-zoe`,
`<Name> = 49 Zoe Street`, **Case B**, under `ADDRESS-TO-ASSET.md`'s batch-mode
amendment: the bake was run and fully QA'd, then discarded, and the branch ships
**source only**.

Step 7 (push / PR / deploy / production QA) is replaced by a stop, per stage 5 of
`ADDRESS-TO-ASSET.md`. Nothing was pushed.

## Step 1 — re-validation

Re-ran the `sf-asset-check` checklist in a fresh isolated Blender scene against
the **shipped, packed** GLB (not the previous session's report, and not the
pre-gltfpack mid file — gltfpack re-emits stored normals, so that is the only
place a sliver or a zero-length vertex normal can appear).

| | Measured |
|---|---|
| Triangles | **7,688** (landmark cap 27,000) |
| Dimensions | 34.1084 × 34.6128 × **17.0000** m |
| min Z | 0.0000 |
| XY centre offset | (−0.0291, −0.2365) m |
| Materials | 12, all `Toy_*`, 3 `_Glow`, no `Toy_body` |
| Textures / transparency | 0 / none |
| Cameras / lights / animation / armatures | 0 / 0 / 0 / 0 |
| Degenerate triangles | 0 |
| Invalid or non-unit loop normals | **0** |
| Normals — signed volume | 13/13 positive, 0 inverted |
| Normals — ray test | 31,500 rays, **0 flipped (0.000%)** |
| **Overall** | **PASS** |

The 34.1 × 34.6 m XY box on a 28.24 × 19.78 m plan is the 45.4° heading, not a
scale error. `dims` and `tris` in the manifest are these measured numbers.

## Step 2 — the asset

`artifacts/49-zoe/49-zoe.glb` → `app/public/sf-assets/landmarks/49-zoe.glb`,
`cmp`-identical, 218,708 B. Not renamed, not re-exported, not re-compressed — it
already carries `EXT_meshopt_compression` from stage 4, which is exactly what
`pipeline/compress-assets.mjs` would have produced, and that script skips files
that already have it.

## Step 3 — manifest

One entry appended to `app/public/sf-assets/landmarks_manifest.json` (91 entries
now). Appended **as text**, not by re-serialising the parsed array: `json.dumps`
of the whole file rewrites `11.0` → `11` across unrelated entries. The diff is
**19 insertions, 0 deletions**.

```json
{
  "id": "49-zoe", "file": "49-zoe.glb",
  "anchor": [-122.3960338, 37.7800764],
  "targetHeightM": 17.0, "cat": 2, "name": "49 Zoe Street",
  "estimated": false,
  "dims": [34.1084, 34.6128, 17.0], "tris": 7688,
  "loadRadius": 2500
}
```

- **`loadRadius: 2500`** — the default rule `max(2500, 17.0 × 30)`. Explicitly
  **streamed, not `alwaysLoaded`**: at 17 m this is neighbourhood fabric. Beyond
  the radius the site is empty ground (Case B carves the procedural block out),
  and at 2.5 km a 17 m absence on a SoMa alley is illegible.
- **`cat: 2`** (apartments) — a 16-unit live/work condominium.
- **`estimated: false`** — the anchor and plan are surveyed, the height is
  LiDAR-derived.
- **id mapping verified**: `camelId('49-zoe')` → `49Zoe`, which is the id used in
  `pipeline/lib/landmarks.mjs`. Confirmed at runtime — `SF.assets.placed` holds
  the key `49Zoe`.
- `targetHeightM / measured z` = 17.0 / 17.0 = **1.0000 exactly**.

## Step 4 — Case B: registry and re-bake

### The exclusion radius — measured, and the plan's prediction was wrong

`exclude: 9.5`. Measured against the **real bake inputs, both of them**, with the
metric `excluded()` in `pipeline/buildings.mjs` actually applies: a ring is
dropped when its **centroid OR any vertex** falls within `r` of the landmark
**anchor**. Scan over `pipeline/data/buildings_datasf.geojson` *and*
`overture_buildings.geojsonseq`, 53 rings within 80 m:

| Ring | nearest vertex to anchor | centroid to anchor | gate = min |
|---|---|---|---|
| `SF3776128` (this building) | 14.13 | 0.11 | **0.11** |
| Overture twin (this building) | 15.94 | 5.37 | **5.37** ← floor |
| `SF3776144` (33–35 Zoe, party wall) | 14.28 | 21.87 | **14.28** ← ceiling |
| `SF3776144` (second ring) | 14.29 | 19.37 | 14.29 |
| Overture (33–35 Zoe) | 14.39 | 26.52 | 14.39 |
| `SF3776456` (Ritch St, rear) | 14.92 | 24.17 | 14.92 |
| `SF3776105` (Ritch St, rear) | 15.51 | 30.26 | 15.51 |

Band: **(5.37, 14.28] — 8.9 m wide**. Shipped 9.5, near the middle, 4.1 m above
the floor and 4.8 m below the ceiling.

**The plan's §2.13 predicted the opposite and has been corrected in place.** It
tabulated each neighbour's nearest vertex *to this footprint* — 33–35 Zoe touches
at 0.00 m across the party wall — and concluded the site might be an
unavoidable-collateral case. That column answers a question the bake never asks.
The gate is measured from the **anchor**, and a party-wall neighbour's shared
vertex sits a half-width of your own building away from it. Measuring turned an
apparently impossible site into one of the roomiest bands on the block.

The **floor** is this building's own **Overture** centroid (5.37 m), not its
DataSF one (0.11 m): an excluded DataSF ring never calls `markOccupied()`, so the
Overture gap-fill would re-add the building on top of the asset. A radius between
0.11 and 5.37 would have produced exactly that.

No anchor offset was needed.

### Registry entry

Appended to `LANDMARKS` in `pipeline/lib/landmarks.mjs` (97 landmarks now), with
the measured table above in a comment beside it:

```js
{ id: '49Zoe', name: '49 Zoe Street',
  lon: -122.3960338, lat: 37.7800764, height: 17.0, exclude: 9.5,
  camera: { distance: 180, yaw: 338, pitch: 28 } }
```

Camera offset is `(sin yaw, ., cos yaw)` with `+z` south, so camera bearing =
`180 − yaw`. The Zoe elevation faces 225.4° and the parking-lot flank 135.4°;
**yaw 338** stands the eye south-south-west, square enough to the striped Zoe
facade to read its rhythm while the blank south-east flank rakes away. 180 m
suits a 17 m building (cf. `181SouthPark` 190 for 16.5 m, `49SouthPark` 165 for
13.0 m). No `key` — this is fabric, not a destination.

### Re-bake

`pipeline/data/` was APFS-cloned from a sibling worktree
(`cp -Rc`, 1.4 GB in 0.17 s) rather than re-downloaded. `pipeline/out/` was **not**
seeded from anywhere — it was built fresh.

Full chain run, exit 0: `terrain → bridges → buildings → streets → landcover →
validate → lore → toy → notables → context → muni-shapes`. Stopping at `toy`
would have silently deleted ~550 committed `ctx/` and `context/` files, so the
whole chain ran. `muni-shapes` correctly left the committed `muni-shapes.bin`
alone (no `MUNI_511_KEY`).

`pipeline validate` passed, including `landmark in extent: 49 Zoe Street — cell 23_13`.

**Generated-file churn: 586 files.** 575 of them are `ctx/` sidecars rewritten
wholesale by `context.mjs` regardless of which landmark triggered the bake — which
is precisely why batch mode exists. Exactly **one building tile and one toy tile**
changed, both `23_13`.

### Proving the exclusion worked

**`node pipeline/verify-rebake.mjs`:**

```
new since origin/main: 49Zoe @ 23_13
  584 of 585 cells unchanged
  23_13    182 -> 181  <- 49Zoe
nearest surviving footprint vs exclusion radius
  ok   49Zoe   14.3 m vs 9.5 m radius  (nearest is 15.3 m tall)
PASS  only the new landmarks' cells moved, and every asset has clear ground under it
```

The count moved by exactly one, which is the arithmetic we want: our DataSF ring
was already present (so `markOccupied()` had suppressed the Overture twin), and
now both are excluded — net −1.

**But a per-cell count is not proof** (`sf3d-verify-rebake-count-blindspot`: on
`164-south-park` a working exclusion reported "dropped nothing" because the data
snapshot added one ring as this landmark dropped one). Settled from the tile
instead, with point-in-polygon at the anchor —
`artifacts/49-zoe/integration/tile-anchor-check.mjs`, decoder lifted from
`verify-rebake.mjs`:

```
origin/main    rings  182   covering anchor 1 (h 16.3 m)   inside r=9.5  1   nearest  0.12 m
re-baked       rings  181   covering anchor 0              inside r=9.5  0   nearest 14.28 m (h 15.3 m)

PASS  nothing covers the anchor and nothing penetrates the 9.5 m circle
```

That 14.28 m matches the independent geojson scan to the centimetre. And the
before-state is the reason this check is worth running: the procedural block was
**16.3 m** against a 17.0 m asset — un-excluded, it would have swallowed all but
0.7 m of the model, and no amount of inspecting the GLB could have revealed it.

**`node pipeline/audit.mjs` check 1.6:**

```
1.6  PASS  no procedural footprint inside a bespoke landmark exclusion zone
           100 zones over 97 landmarks clear
```

The audit also reports three FAILs — 1.2b (95th-percentile height), 1.3c
(Telegraph Hill terrain), 1.7b (one sampled tree offshore). **These are
pre-existing and not caused by this landmark**: re-running the audit against
`origin/main`'s committed tiles (baked tiles stashed) reproduces all three
identically, and none of them is reachable by dropping one 16.3 m footprint in
SoMa.

## Step 5 — local verification

`app/dist` driven in real headless Chrome over CDP by
`artifacts/49-zoe/qa_local.mjs`, rather than the in-editor Browser pane: parallel
landmark sessions hold the preview slots, and a hidden pane throttles
`requestAnimationFrame` to nothing, which makes a healthy streaming landmark look
broken. Two adaptations recorded in the script: the `until()` budget is 600 s (a
boot that takes 8 s idle takes minutes under SwiftShader at load 100+), and
`assets.update()` is pumped with a real delta, because it gates its scan on `dt`
and the camera can otherwise sit on the anchor with the entry still `far`.

| Check | Result | Evidence |
|---|---|---|
| Manifest entry loads and merges | **PASS** | `sf-assets: 49-zoe merged 14 objects / 12 materials -> batched (4802 tris body); uniform x1.0000 at 3649, -1114` |
| Uniform scale ≈ 1.0 | **PASS** | **×1.0000** — authored height and `targetHeightM` agree exactly |
| Placed at the real anchor | **PASS** | local (3649, −1114) against the computed (3648.85, −1113.85) |
| id mapping | **PASS** | `SF.assets.placed` holds `49Zoe` |
| Exactly one building at the site | **PASS** | day screenshot — no procedural twin, no baked block through the model, no z-fighting |
| Footprint size against the block | **PASS** | reads as one alley lot between its party-wall neighbour and the surface parking lot, which is the real site |
| Orientation | **PASS** | the striped elevation faces Zoe Street; the blank flank faces the parking lot |
| Terrain seating | **PASS** | no floating, no sinking (site is flat — 0.48 m of LiDAR ground range) |
| Night glow | **PASS** | night screenshot — the three roof monitors glow and an uneven scatter of loft windows; nothing else lights |
| Draw calls < 300 | **PASS** | **92/frame** averaged over 30 frames at the landmark |
| Streaming | **PASS** | 91 entries, 73 live, 0 failed at the landmark |
| No asset warnings | **PASS** | none |

Screenshots: `artifacts/49-zoe/qa/day.png`, `night.png`, `wide.png` (900 m).
Raw run data in `artifacts/49-zoe/qa/qa.json`.

One unrelated console line appears and is not ours:
`weather: feed unavailable, holding the last known sky` — the dist server has no
`/api`, so the weather feed 404s to `index.html`. It degrades exactly as designed.

## Step 6 — fallback drill

See `artifacts/49-zoe/qa/drill.json` and `drill-*.png`.

The drill serves a real **404** for `/sf-assets/landmarks/49-zoe.glb` rather than
renaming the file: Vite and a dumb dist server both answer a missing public path
with `index.html` and HTTP 200, so the rename trick cannot produce a fetch failure
at all.

Expected wording, and a correction to the prompt: **INTEGRATION-PROMPT Step 6
quotes the resident path's warning** (`... — keeping the code-built landmark`,
`warn()` at `app/src/assets.js:362`). This landmark has a `loadRadius`, i.e. it is
**streamed**, and a streamed failure goes through `scan()` at `assets.js:560`,
which deliberately does not use the single-shot `warn()`:

```js
console.warn(`sf-assets: ${state.entry.id} failed to load (${error.message})`);
```

— no "keeping" suffix. It is still structurally once: `status = 'failed'` matches
no branch in `scan()`, so the entry can never be retried or re-warned. The drill
therefore matches on the asset id, not on the prompt's wording.

**Case B expectation:** the site is **empty ground** inside the exclusion zone,
not a reappearing procedural building. That is by design — the re-bake carved the
16.3 m block out — and it is what `drill-day.png` shows: flat ground where the
model stood in `day.png`, with the neighbours, the alley, the crosswalks and the
parking lot all rendering normally around it.

| Check | Result | Evidence |
|---|---|---|
| App still boots with the GLB missing | **PASS** | 91 entries, **84 live**, 1 failed — the rest of the city is unaffected |
| Exactly one fallback warning | **PASS** | `sf-assets: 49-zoe failed to load (fetch for ".../49-zoe.glb" responded with 404: Not Found)` — once |
| Draw calls still under 300 | **PASS** | 88/frame |
| Site degrades to empty ground, no hole, no crash | **PASS** | `drill-day.png`, `drill-night.png`, `drill-wide.png` |

`app/src/landmarks.js` was not touched — the procedural fallback stands (AGENTS
rule 3).

## Step 7 — replaced by a stop (batch mode)

Not pushed, no PR, no deploy, no production QA. Per `ADDRESS-TO-ASSET.md` stage 5,
that decision is the owner's.

**The bake was discarded before committing:**

```
git checkout -- app/public/tiles api/_data
```

and the branch commits **source only** — the GLB, the manifest entry, the registry
entry, the asset plan and `artifacts/49-zoe/`. Those are the only files this
landmark shares with its siblings, and all three shared ones are append-only lists
that merge mechanically. The city gets rebuilt once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

Sanity check, from the prompt: `git diff --name-only origin/main` must list
nothing under `app/public/tiles/` or `api/_data/` — verified, see the final report.

## Files touched

| File | Change |
|---|---|
| `app/public/sf-assets/landmarks/49-zoe.glb` | new, 218,708 B |
| `app/public/sf-assets/landmarks_manifest.json` | +19 lines, −0 |
| `pipeline/lib/landmarks.mjs` | +1 `LANDMARKS` entry with the measured exclusion table |
| `docs/asset-plans/49-zoe.md` | §2.13 corrected — the exclusion prediction was wrong |
| `artifacts/49-zoe/integration/` | new — `tile-anchor-check.mjs`, this report |
| `artifacts/49-zoe/qa_local.mjs`, `qa/` | new — the local QA harness and its evidence |

Untouched, deliberately: `app/src/landmarks.js` (the procedural fallback, AGENTS
rule 3), every other landmark, asset and manifest entry, and everything generated
under `app/public/tiles/`.
