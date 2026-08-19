# One Market Plaza (Spear and Steuart Towers) — build report

Stages 2–5 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed 19 August 2026
against `docs/asset-plans/one-market-plaza-towers.md`. **This report beats the
plan** wherever they disagree.

## 1. Shipped numbers

Post-stage-4. The pre-optimize build is archived at
`optimize/input/one-market-plaza-towers.glb`.

| | |
|---|---|
| File | `one-market-plaza-towers.glb` (meshopt-compressed) |
| Triangles | **8,917** (cap 26,000) |
| Objects | 10 joined material groups (329 solids before the optimize join) |
| Draw submeshes | **12** |
| Dimensions | 123.023 x 128.810 x **177.600** m |
| min Z | **0.000**; XY centre offset `[-0.0015, -0.0009]` m |
| Loader scale | **1.000** |
| Materials | 10, all `Toy_*`, flat, opaque | 
| Glow materials | `Toy_glassl_Glow`, `Toy_gold_Glow` |
| Raw / gzip | **213.0 KB** / 125.9 KB (from 629.8 KB raw, **−66.2%**) |
| Anchor | `-122.3941803, 37.7933169` |
| Target height | **177.6 m** (Spear Tower rooftop plant crest) |

Heights as built: podium 0 → **27.80**, podium parapet 28.80; **Steuart Tower**
shaft 27.80 → **111.00**, parapet 112.20, plant crest 115.50; **Spear Tower**
shaft 27.80 → **172.00**, parapet 173.20, plant crest **177.60**.

## 2. The scoping decision, and why the data made it

The request named two towers. They are shipped as **one asset**, because the
survey does not separate them:

- **Steuart Tower has no footprint of its own in DataSF.** It sits inside the
  podium polygon (`mblr = SF3713007`, `sf16_bldgid` 201006.0000212), whose
  `hgt_median` is the *podium's* 27.75 m.
- Two separate landmarks would therefore each need an exclusion covering that
  same shared podium ring, and there is no radius that drops it for one and
  spares it for the other.
- They are also one 1976 building by one architect on one parcel, joined by the
  podium, and the Southern Pacific Building — the third building of the same
  complex, on the same street address — is already a separate asset because it is
  a separate building of a separate date on a separate parcel.

So the asset is the whole of lot 3713/007: both shafts, the podium, and the
plaza between them.

## 3. Validation — all PASS

`validate_one_market_plaza_towers.py` on a fresh-scene re-import of the exported
GLB. Full output in `validation.json`.

| Check | Result |
|---|---|
| Fresh isolated scene, re-imported final GLB | PASS |
| Triangles 8,917 ≤ 26,000 | PASS |
| bbox top exactly 177.600 m → loader scale 1.000 | PASS |
| min Z 0.000, XY centre offset ≤ 0.0015 m | PASS |
| Image textures / transparent materials | 0 / 0 — PASS |
| Material names all `Toy_*`, no `Toy_body` | PASS |
| `_Glow` only on the lit slots, retail band and canopies | PASS |
| Cameras / lights / animations / armatures / constraints | all 0 — PASS |
| Transforms applied, no negative scales | PASS |
| Normals: inverted signed volumes | **0 of 10** — PASS |
| Normals: ray residual (gate ≤ 0.15%) | **0.00%** — PASS |

Two constants inherited from the `1-market` copy of the validator were wrong for
this asset and correctly failed it — the dimension-plausibility range and the
recorded anchor/headings. Adapted, not rewritten.

## 4. Corrections to the plan

1. **Camera framing.** The render rig inherited `span = max(x, y)`, which on a
   177 m tower over a 129 m footprint put the aerial camera inside the building
   and cut Spear's top off. Framing now takes the longest of all three axes.
2. **The garden kerb was a disc and buried the planting.** Rebuilt as a ring
   band. Same class of error as the applied-panel recess trap: a solid cap
   swallows what it is meant to frame.
3. **Pier width raised 1.35 → 1.80 m** (podium 2.10 → 2.80). At the plan's width
   the slots dominated and the towers read as dark glass boxes rather than as
   white piered ones.
4. **Plaza furniture added** — four planters and two paved aprons. The plan's
   plaza was garden + canopies only, which left most of a 7,500 m2 deck blank
   under a camera that looks down.
5. **Steuart's plant crest 115.5 m is inferred**, as the plan said. It does not
   set the export height.

## 5. Stage 4 — optimize

`GLB-OPTIMIZE-PROMPT.md`, `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`. Full detail in `optimize/REPORT.md`.

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 644,940 | **218,144** | **−66.2%** |
| Gzip | 118,999 | 128,963 | +8.4% (meshopt output is near-incompressible) |
| Triangles | 9,428 | 8,917 | −5.4% (buried interior faces) |
| Objects | 329 | **10** | −97.0% |
| Draw submeshes | 330 | **12** | −96.4% |
| Materials | 10 | 10 | identical set |

**The limited dissolve produced a real sliver on this asset and was rejected.**
Both Phase-B variants were built and packed:

| Variant | Tris | Packed raw | Packed gzip | Slivers (area < 1e-4 m2) |
|---|---|---|---|---|
| weld + dissolve | 8,845 | 212,840 | 137,421 | **1** — area 2.4e-07 m2, longest edge **4.71 m**, in `grp_Toy_white` |
| **weld only (shipped)** | 8,925 | 218,144 | **128,963** | **0** |

That is exactly the failure `GLB-OPTIMIZE-PROMPT` §3 step 3 describes, and this
is the first time it has actually been measured in this repo: the neighbouring
`1-market` asset has *eight* coplanar ring bands and produced none, while this
one has five and produced one. It is asset-specific and has to be measured, not
assumed in either direction. The dissolve was worth 5 KB of raw and cost 8 KB of
gzip, so rejecting it is free.

Gates: **G1** material set identical, `_Glow` separate — PASS. **G2** bbox and
origin identical, 0 inverted, 0.00% residual — PASS. **G3** `G3-OK`, 12 meshes,
8,925 tris, only `EXT_meshopt_compression` — PASS. **G4** mean abs RGB delta
**0.0004%–0.0076%** on day and all four elevations, **0.50–0.56%** on the night
pair (gates ≤2% far / ≤4% near) — PASS; the night figure is denoiser noise on
thin bright glow strips against black, and the pairs are indistinguishable side
by side. **G5** 330 → 12 — PASS. **G6** −66.2% against a 60% target — PASS.
**G8** deterministic, no foreign geometry — PASS.

## 6. Stage 5 — integration (batch mode), Case B

- `app/public/sf-assets/landmarks/one-market-plaza-towers.glb` — byte-identical
  to the artifact.
- Manifest entry appended **as text**, `+18 lines, 0 deletions`.
  `camelId('one-market-plaza-towers')` → `oneMarketPlazaTowers`, matching the
  registry id.
- **No `loadRadius` — resident.** At 172 m Spear is over the ~150 m
  skyline-piece threshold and is one of the towers that makes the waterfront
  silhouette behind the Ferry Building; a hole there at 2.5 km would read from
  across the bay. The manifest has 18 residents and uses no `alwaysLoaded` key,
  so this follows that convention and simply omits the field.
- `pipeline/lib/landmarks.mjs` — `id: 'oneMarketPlazaTowers'`, `height: 177.6`,
  **`exclude: 30`**, `camera: { distance: 700, yaw: 58, pitch: 20 }`.

**The registry splice landed in the wrong array on the first attempt.** Seeking
the last `\n  },\n];\n` in the file finds a later array, not `LANDMARKS`; the
entry parsed as valid JavaScript, the file looked right, and `LANDMARKS.length`
did not change. Bound the search to the first `];` *after* `export const
LANDMARKS = [` instead, and assert the count went up.

### 6.1 The exclusion, measured against the real bake input

Both `pipeline/data/buildings_datasf.geojson` and the Overture gap-fill layer,
after `simplifyRing` at 0.6 m, testing centroid **and** every vertex exactly as
`excluded()` does:

| Gate | Ring | Verdict |
|---|---|---|
| **3.3 m** | overture `One Market Plaza` h=28 | drop — the podium envelope, caught by its **centroid**, not by any vertex (its nearest vertex is 42 m away) |
| **10.4 m** | datasf `SF3713007` h=27.75 | drop — podium + Steuart shaft |
| **10.4 m** | datasf `SF3713007` h=172.41 | drop — the Spear shaft |
| **51.8 m** | datasf `SF3713006` h=46.12, `SF3713007` h=39.71 | **must survive** — the Southern Pacific Building and its atrium |

Safe window **(10.4, 51.8)**, 41 m wide; **30 m** sits mid-band. This is the
opposite of the 1 Market case next door, whose window was only 19 m.

**The two assets are complementary by construction.** The anchors are 78.2 m
apart. 1 Market's `exclude: 20` reaches 35.4 m short of this complex's rings, and
this one's `exclude: 30` reaches 51.8 m short of 1 Market's. Neither eats the
other, and each drops exactly its own building's rings plus the Overture
duplicate of it.

### 6.2 Re-bake

Full chain (`terrain → bridges → buildings → streets → landcover → validate →
lore → toy → notables → context → muni-shapes`), 7 min 45 s at machine load
380–430. `pipeline/data` cloned from a sibling worktree with APFS
copy-on-write; it reproduced `origin/main`'s tiles exactly, so **1 of 585
building tiles changed** — the one this landmark drops.

| Check | Result |
|---|---|
| `pipeline/audit.mjs` **1.6** | **PASS** — 114 zones over 110 landmarks clear |
| audit totals | 29 passed / 3 failed / 1 informational — the three failures are pre-existing (p95 height, Telegraph Hill DEM, one offshore tree) |
| `pipeline/verify-rebake.mjs` | **PASS** — `new since origin/main: oneMarketPlazaTowers @ 23_10`; cell 23_10 **49 → 47**; `ok oneMarketPlazaTowers 52.6 m vs 30 m radius` |

**Proved from the tile, not the radius.** Decoding the nine cells around the
anchor and diffing against `origin/main`'s tile:

- **Exactly two footprints dropped**, both this building's: the **Spear shaft**
  (centroid 3783.0, −2575.7 — matching the measured 3783.1, −2575.7 — baked at
  175.5 m) and the **podium + Steuart** polygon (centroid 3820.3, −2567.4, baked
  at 96.2 m).
- **Nothing was added.** No Overture gap-fill ring appeared in the ground the
  exclusion freed, which is the defect that only shows up after a bake.
- Of 601 surviving rings across the nine cells, **two have vertices on the
  envelope boundary at 0.00 m penetration depth** — the Southern Pacific Building
  and its atrium, which share survey vertices along the party edge. Zero depth is
  the correct answer there; a containment boolean would have called it a failure.
  In the merged batch both are dropped by `1Market`'s own exclusion anyway.

### 6.3 Local verification (Step 5) — all PASS

Headless Chrome + CDP against the built `app/dist`.

| Check | Result |
|---|---|
| Merge line | `sf-assets: one-market-plaza-towers merged 12 objects / 10 materials -> batched (4277 tris body); uniform x1.0000 at 3812, -2577` |
| **Uniform scale** | **x1.0000** |
| Placement | `SF.assets.placed.has('oneMarketPlazaTowers')` true, anchored at local (3812, −2577) |
| Exactly one building on the site | yes — no procedural twin, no block poking through (day/wide screenshots and §6.2's tile proof) |
| Orientation | both shafts' long axes NW–SE; the podium fronts Mission Street |
| Terrain seating | flush |
| Night | only the intended `_Glow` surfaces light |
| **Draw calls** | **avg 88/frame** at the landmark, budget 300 |
| Asset warnings | **none** |
| Streaming | 104 entries, 85 live, 0 loading, 0 fading, 0 failed |

Screenshots: `qa/day.png`, `qa/night.png`, `qa/wide.png`.

Note the QA harness's drill-mode gate was changed for this asset: the inherited
`s.failed > 0 || s.live > 20` shortcut is wrong for a **resident** entry, which
merges during boot and satisfies `live > 20` long before the loader ever reaches
for the file. It now waits on `failed > 0` alone.

### 6.4 Fallback drill (Step 6) — all six checks PASS

The throwaway file server returned a real **404** for
`/sf-assets/landmarks/one-market-plaza-towers.glb` rather than renaming the file.

| Check | Result |
|---|---|
| **The drill actually exercised the loader** | `failed: 1` — a drill reporting `failed: 0` measured nothing, however healthy it looks |
| App still boots with the GLB missing | `entries: 104`, **84 live**, 0 loading, 0 fading — the area renders |
| This landmark absent | `SF.assets.placed.has('oneMarketPlazaTowers')` **false** |
| Exactly one warning naming it | yes, 1 of 93 console lines |
| Draw calls with it missing | 87/frame |
| Case B site behaviour | empty ground inside the exclusion zone, as designed |

**The warning text differs from the neighbouring asset's, and the difference is
informative.** This one reads:

```
sf-assets: one-market-plaza-towers failed to load (... 404: Not Found)
  — keeping the code-built landmark
```

The 1 Market asset next door produced the same line **without** the "keeping the
code-built landmark" suffix. That is the streaming mode showing through: a
**resident** entry (no `loadRadius`, as here) fails through the resident path and
gets INTEGRATION-PROMPT Step 6's quoted wording verbatim, while a **streamed**
entry fails through `scan()` and gets the bare `failed to load`. Match on the
id, not on the prompt's wording — and note that Step 6's text is only literally
correct for resident assets.

Full log: `qa/drill.log`. The GLB was verified byte-identical afterwards.

### 6.5 Housekeeping

- `node pipeline/compress-assets.mjs` skips this asset (already carries
  `EXT_meshopt_compression` from stage 4); its only effect was to re-compress
  `vehicles/passenger-airplane.glb`, as on every branch. Reverted.
- `app/public/sf-assets/landmarks/one-market-plaza-towers.glb` is byte-identical
  to the artifact.
- `cd app && npm run lint` clean; `npm run build` green with **26/26** tests.
- **Batch discard done**: `git checkout -- app/public/tiles api/_data`, and
  `git diff --name-only $(git merge-base HEAD origin/main)...HEAD` lists **zero**
  files under either path.
