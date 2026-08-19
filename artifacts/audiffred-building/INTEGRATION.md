# The Audiffred Building — stage 5 integration report

Stage 5 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executing Part 1 of
`docs/asset-plans/INTEGRATION-PROMPT.md` as **Case B** (new landmark) in
**BATCH mode**.

Batch mode means the bake was run in full, the Step 5/6 QA was done against it,
and then the ~586 generated files under `app/public/tiles/` and `api/_data/`
were discarded before committing. What ships from this branch is source only:
the GLB, its manifest entry, its `pipeline/lib/landmarks.mjs` entry, the asset
plan and `artifacts/audiffred-building/`. The city is baked once for the whole
batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

---

## Step 1 — re-validation before touching the app

Fresh-scene re-import of the **shipping (packed) GLB**, not the authoring scene
and not the pre-optimize file:

```
overall PASS   17 of 17 checks
triangles 9,256 (cap 12,000)   objects 11   materials 12, all Toy_*
dims 40.4244 x 40.2848 x 17.500 m   min Z 0.000   XY centre (0.000, 0.000)
image textures 0   transparent materials 0   cameras 0   lights 0   animations 0
degenerate triangles 0   invalid/non-unit loop normals 0
signed volume positive on 11 of 11 solids   inverted: []
visibility rays flipped: 0 of 31,500
open glow strips facing outward: 40 of 40
```

`dims` and `tris` in the manifest are these measured numbers, not the plan's.

## Step 2 — the asset

`app/public/sf-assets/landmarks/audiffred-building.glb`, copied byte-for-byte
from `artifacts/audiffred-building/audiffred-building.glb` (297,888 bytes). Not
renamed, not re-exported, not re-compressed — it was already meshopt-packed at
stage 4, and `pipeline/compress-assets.mjs` skips a file that already carries
`EXT_meshopt_compression`.

## Step 3 — manifest entry

Appended as **text**, not by `json.load` + `json.dump`: a round trip through
Python's JSON would rewrite every `13.0` to `13` and re-escape the en-dashes
across all 90 existing entries. The diff is `+19 / -0`.

```json
{
  "id": "audiffred-building",
  "file": "audiffred-building.glb",
  "anchor": [-122.3927766, 37.7933230],
  "targetHeightM": 17.5,
  "cat": 3,
  "name": "Audiffred Building (1 Mission Street)",
  "estimated": true,
  "dims": [40.4244, 40.2848, 17.5],
  "tris": 9256,
  "loadRadius": 2500
}
```

- **`loadRadius: 2500`, the explicit streaming decision.** The default rule is
  `max(2500, targetHeightM x 30) = max(2500, 525) = 2500`. Taken as-is. This is
  not an `alwaysLoaded` piece: at 17.5 m it is not skyline, and the
  `alwaysLoaded` list is the only one that still grows boot cost. Beyond 2,500 m
  the site is **empty ground**, because Case B carved the procedural block out —
  at that distance a 586 m² lot is sub-pixel, so the absence is illegible.
- **`"estimated": true`** because the 17.5 m crest is an Overture figure
  corroborated photogrammetrically, not a LiDAR measurement. The 15.4 m deck
  below it *is* measured, but that is not the field.
- **`camelId` round trip verified**: `audiffred-building` → `audiffredBuilding`,
  which is the id used in `pipeline/lib/landmarks.mjs`. A mismatch here is what
  leaves two buildings on one lot.

## Step 4 — Case B

### Registry

`pipeline/lib/landmarks.mjs` gains `id: 'audiffredBuilding'`, `height: 17.5`,
`exclude: 7`, `camera: { distance: 230, yaw: 180, pitch: 26 }`. The full
derivation of the radius and the camera is in the entry's own comment.

### The exclusion, measured against the real bake input

`excluded()` in `pipeline/buildings.mjs` fires on the **centroid OR any ring
vertex**, on rings already passed through `simplifyRing(ring, 0.6)`. Measured
from the anchor against `pipeline/data/buildings_datasf.geojson` and
`pipeline/data/overture_buildings.geojsonseq`:

| Ring | centroid | nearest vertex |
|---|---|---|
| Overture "The Audiffred Building" (h 17.4) | **0.04 m** | 21.99 m |
| DataSF `SF3715001` (h 19.18) | **1.95 m** | 19.99 m |
| DataSF `SF3715002` — 100 The Embarcadero, h 24.4 | 13.70 m | **19.99 m** |
| Overture equivalent of that neighbour (h 20.3) | 13.92 m | 22.03 m |
| DataSF `SF3715003` (h 29.6) | 28.16 m | 28.47 m |

Both of this building's own rings are caught by **centroid at under 2 m**, so
the safe window is **r ∈ (1.95, 13.70)** and 7 sits near its middle. Note that
this building's nearest vertex and the neighbour's nearest vertex are **the same
two points at 19.99 m** — they share the party wall — so no radius can ever
reach this footprint's vertices without eating the neighbour. It does not need
to: the centroid test is what clears this lot.

### The bake

Full chain run, not stopped at `toy`: `terrain → bridges → buildings → streets →
landcover → validate → lore → toy → notables → context → muni-shapes`.
`muni-shapes` printed "no 511 key … leaving the committed file as is" and exited,
which is the expected no-op. `context` re-validated 174,695 / 174,695 buildings
with a pick box and an identity, and 5,000 / 5,000 notables in the search index.

### Audit 1.6

```
1.6  PASS  no procedural footprint inside a bespoke landmark exclusion zone
           100 zones over 97 landmarks clear
```

Three other audit checks fail — `1.2b` city-wide p95 height, `1.3c` Telegraph
Hill terrain from the Terrarium DEM, `1.7b` one sampled tree offshore. All three
are city-wide source-data checks that a 585 m² exclusion cannot move, and all
three fail identically on the control bake below.

### verify-rebake, and the stray cell

```
new since origin/main: audiffredBuilding @ 23_10
  583 of 585 cells unchanged
  23_10     49 -> 48   <- audiffredBuilding
  23_13    169 -> 182  *** not a new landmark cell ***
```

Cell 23_13 is ~1,500 m from a 7 m radius and **gained** 13 footprints, which an
exclusion cannot do. Settled with the control bake the tool itself recommends —
remove the entry from `landmarks.mjs`, re-run `buildings.mjs`, compare:

| Cell | origin/main | control bake (no Audiffred) | with Audiffred |
|---|---|---|---|
| 23_10 | 49 | **49** | **48** |
| 23_13 | 169 | **182** | 182 |

23_13 differs **without** this landmark, so it is the `pipeline/data/` snapshot
drifting from whatever origin/main was last baked against — not this radius.
23_10 is unchanged without the entry and drops exactly one footprint with it.
**This exclusion removes one footprint in one cell and nothing else.**

### Proving it from the tile, not from the count

`verify-rebake` compares per-cell **counts**, which can report "dropped nothing"
on a working exclusion. Decoding `app/public/tiles/buildings/23_10.bin` and
testing point-in-polygon against the real 41.82 × 14.00 m footprint:

| | footprints with a vertex inside | detail |
|---|---|---|
| origin/main | 2 | #23 top 20.5 m (this lot) + #22 top 20.6 m, each 0.770 m in |
| this branch | 1 | only #22, still 0.770 m in |

The procedural block on this lot (top 20.5 m — `datasfHeight()` averaging the
15.36 m median with the 19.18 m maximum, i.e. **within 0.25 m of the asset's own
crest**, so it would have z-fought across the whole roof rather than obviously
poking through) is gone.

**What remains is honest and unfixable:** the neighbour at 100 The Embarcadero
overhangs this footprint by **0.770 m** at the shared party-wall corner. That is
the known ~1.25 m disagreement between DataSF parcels and LiDAR footprints, it
predates this change (identical on origin/main), and no exclusion radius can
spare it — reaching that vertex means deleting a 24.4 m neighbour. The anchor
was **not** moved to hide it, per AGENTS rule 5.

## Step 5 — local QA

Driven against the **built** `app/dist` in real headless Chrome over CDP rather
than the in-editor Browser pane: sibling landmark sessions hold the preview
slots, and a hidden pane throttles `requestAnimationFrame` to nothing, which
makes a healthy streaming landmark look broken.

```
sf-assets: audiffred-building merged 13 objects / 12 materials
           -> batched (6655 tris body); uniform x1.0000 at 3935, -2578
```

| Check | Result |
|---|---|
| manifest entry loads | **PASS** — merge line above |
| uniform scale ≈ 1.0 | **PASS** — exactly **x1.0000** (authored height and `targetHeightM` agree) |
| exactly one building, no procedural twin, no z-fighting | **PASS** — see `qa/day.png` |
| footprint size against the neighbouring blocks | **PASS** — reads as the thin 3:1 slab it is |
| orientation, real front to the real street | **PASS** — the 41.8 m elevation faces Mission, the short end faces The Embarcadero |
| sits on terrain, no float or sink | **PASS** |
| night: only the intended `_Glow` surfaces light | **PASS** — see `qa/night.png` |
| draw calls < 300 | **PASS** — avg **90/frame** over 30 frames |
| no asset warnings | **PASS** — none |

71 landmarks were live simultaneously at this camera with no batch overflow, so
the shared `BODY_VERTS` reserve is not a problem at this corner (it was worth
checking: this is the densest cluster in the bespoke set after SoMa, and nine
more Embarcadero/Steuart landmarks are in flight).

Screenshots: `qa/day.png`, `qa/sunlit.png`, `qa/night.png`, `qa/wide.png`.

**Judgement from the app's own camera.** The wide shot is the one that matters:
the Audiffred reads as *the small dark-roofed building with the green vault*
among pale modern blocks on the waterfront, which is exactly the recognition cue
the plan ranked first. The mansard is very dark in the app's shading — darker
than the Blender rig suggests, which is the known trap — but it is dark
*relative to its own trim and its pale neighbours*, which is the point, and
`Toy_roofd` (which measures rgb(9,9,12) in the live scene) would have been
genuinely black. At night the amber entablature band running all 41.8 m of
Mission and turning the Embarcadero corner is the hero, exactly as designed.

## Step 6 — fallback drill (mandatory)

Run by serving a real **404** for `/sf-assets/landmarks/audiffred-building.glb`
rather than renaming the file: Vite answers a missing public path with
`index.html` and HTTP 200, so the rename trick cannot produce a fetch failure at
all.

| Check | Result |
|---|---|
| app still boots with the GLB missing | **PASS** — `{"entries":91,"far":20,"loading":0,"live":70,"fading":0,"failed":1}` |
| exactly one fallback warning | **PASS** — `sf-assets: audiffred-building failed to load (… responded with 404: Not Found)`, and nothing else |
| Case B: the site is empty ground inside the exclusion zone | **PASS, expected** — `qa/drill-day.png`. The lot renders as bare ground, the streets and the 100 The Embarcadero neighbour are intact, no hole, no crash |
| draw calls still under 300 | **PASS** — avg 81/frame |

The landmark is absent from `assets.placed` and `failed` is exactly 1. Rule 3 is
satisfied: one console warning, graceful degradation, no crash.

**The drill took four attempts, and three of those failures were the machine,
not the asset.** Several sibling landmark sessions were running their own
headless-Chrome QA concurrently; at load average 500–725 the page could not
finish fetching `landmarks_manifest.json` inside the harness's 120 s gate, and
the failure surfaced as a bare `manifest timed out (last null)` — which looks
exactly like a broken asset. Two changes to `qa_local.mjs` came out of it and
are committed:

1. **`until()` now dumps diagnostics before throwing** — `hasSF`, `hasAssets`,
   `stats()`, a direct `fetch()` of the manifest, and the last 25 console lines.
   `entries: 0` with no `no landmark manifest` warning is what proved the fetch
   was still in flight rather than failed, because `states` is populated
   immediately after the manifest parses.
2. **The verdict is written before the screenshots.** The third attempt passed
   all four checks and was then killed mid-capture, leaving no `drill.json` at
   all. Screenshots are evidence, not the verdict, and losing them must not lose
   the verdict.

The default `until()` timeout also went from 120 s to 300 s for the same reason.

## Step 7 — stopped, per the pipeline

`ADDRESS-TO-ASSET.md` stage 5 **replaces** INTEGRATION-PROMPT Step 7 with a
stop. Lint, tests and build were run; push, PR and deploy were not, and are not
covered by the session's standing pre-approval.

```
app: eslint src test          clean
app: npm test                 26 tests, 26 pass, 0 fail
app: npm run build            built, 3,315 tiles compressed 56.8 -> 31.8 MB
```

Branch `pipeline/audiffred-building`, four commits, rebased onto
`origin/main` (`3d98a6a`).

**The rebase hit three conflicts, all of them the append-only kind batch mode
predicts** — sibling landmarks had landed on main mid-session in
`docs/asset-plans/README.md`, `landmarks_manifest.json` and
`pipeline/lib/landmarks.mjs`. Each was resolved by keeping **both** sides, main's
rows first. Verified afterwards: 104 manifest entries, 110 registry landmarks,
no duplicate ids in either, both files parse.

```
git diff --name-only $(git merge-base origin/main HEAD) HEAD -- app/public/tiles api/_data
  (0 files)
```
