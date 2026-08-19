# 1 Market Street (Southern Pacific Building) — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed 19 August 2026
against `docs/asset-plans/1-market.md`. **This report beats the plan** wherever
they disagree; every correction is listed in §4.

## 1. Shipped numbers

Post-stage-4. The pre-optimize build is archived at
`optimize/input/1-market.glb`; see `optimize/REPORT.md` for the shrink pass.

| | |
|---|---|
| File | `1-market.glb` (meshopt-compressed) |
| Triangles | **18,508** (cap 28,000) |
| Objects | 13 joined material groups (733 solids before the optimize join) |
| Draw submeshes | **14** |
| Dimensions | 112.208 x 112.098 x **48.700** m |
| bbox min / max | `[-56.105, -56.050, 0.000]` / `[56.104, 56.049, 48.700]` |
| min Z | **0.000** |
| XY centre offset | `[-0.0005, -0.0005]` m |
| Loader scale (`targetHeightM / measuredHeight`) | **1.000** |
| Materials | 12, all `Toy_*`, flat, opaque, no textures |
| Glow materials | `Toy_glassl_Glow`, `Toy_gold_Glow` |
| Raw / gzip size | **474.0 KB** / 241.2 KB (from 1,247.1 KB raw, −62.0%) |
| Anchor | `-122.3948075, 37.7938412` |
| Target height | **48.70 m** (rooftop plant fan-bank cap) |

Heights as built: grade 0.00 → terra-cotta base 13.00 → base entablature and
balustrade 14.00 → eight brick storeys of 3.35 m → attic colonnade 40.80–44.10 →
roof deck 44.10 → cornice architrave 44.60 → corona 45.55 → **crowning cornice
crest 46.10** → plant enclosures 48.10 → plant cap 48.40 → **fan-bank crest
48.70**. Atrium glazing: eaves 35.20, apex 43.50.

Measured frontage headings, recorded from the built footprint: Market **315.2°**,
Steuart **45.2°**, Spear **225.2°**, the two Mission returns **135.2°**.

## 2. Validation — all PASS

`validate_1_market.py` factory-resets Blender, imports **only the exported GLB**
and reports on the re-import, never on the authoring scene. Full machine-readable
output in `validation.json`.

| Check | Result |
|---|---|
| Fresh isolated scene, re-imported final GLB | PASS |
| Triangle count 18,508 ≤ 28,000 | PASS |
| bbox top exactly 48.700 m → loader scale 1.000 | PASS |
| min Z 0.000, XY centre offset ≤ 0.0005 m | PASS |
| Image textures | 0 — PASS |
| Transparent materials | 0 — PASS |
| Material names all `Toy_*`, no `Toy_body` | PASS |
| `_Glow` suffix only on the two intended night materials | PASS |
| Cameras / lights / animations / armatures / constraints | 0 / 0 / 0 / 0 / 0 — PASS |
| Transforms applied, no negative scales | PASS |
| Normals: inverted-signed-volume objects | **0 of 13** — PASS |
| Normals: visibility-ray residual (gate ≤ 0.15%) | **0.00%** — PASS |
| Foreign / leaked geometry | none — PASS |

## 3. Renders

Regenerated from the exported GLB with Cycles on Metal GPU, `Standard` view
transform (AgX would eat the flat palette), 40 samples, denoised.

`1-market-aerial.png` (three-quarter on the Market x Steuart corner, 40° down),
`1-market-top.png`, `1-market-night.png`, and the four true elevations
`1-market-west.png` (Market), `1-market-north.png` (Steuart),
`1-market-east.png` (Mission / the open side of the court),
`1-market-south.png` (Spear), composed into `1-market-contact-sheet.png`.

**One fix to the review rig is worth carrying to other assets.** The night pass
inherited from `render_300_brannan.py` turned `Emission Strength` up on every
`_Glow` material. After a glTF round-trip those materials come back with
**`Emission Color` = white** — the emissive colour is not carried, because the
build exports at strength 0 — so the rig was rendering *every* glow surface
blown-out white and telling us nothing about what the app will draw. The app
draws `_Glow` in a separate **unlit** layer, i.e. at the material's own base
colour. `light_glow()` now copies base colour → emission and uses strength 1.0,
so the night render is what the app will show. It changed the review verdict
here: the atrium reads as a cool pale-blue lantern (112, 152, 189), not white.

## 4. Corrections to the plan

1. **Bounding box.** The plan predicted ~107.1 x 107.0 m from the wall ring. The
   export is **112.21 x 112.10 m**, because the crowning cornice projects 1.85 m
   and the base band 0.34 m beyond the wall plane on a 45°-rotated footprint.
   Expected, not a scale error — but the plan's number was the wall ring's, not
   the asset's.
2. **Storey split.** The plan's massing table gave the shaft 8 storeys of 3.55 m
   to 42.40 m and the attic only 2.20 m. Built as **8 x 3.35 m to 40.80 m** with a
   **3.30 m attic colonnade**, because at the plan's proportions the colonnade
   rendered as a dentil strip rather than the storey it is. Eleven storeys and the
   46.10 m crest are unchanged.
3. **Atrium glazing.** Plan: eaves 33.0, apex 43.0. Built: **eaves 35.20, apex
   43.50** — at the plan's eaves the glazed hip read as a swimming pool from the
   aerial camera rather than a roof.
4. **The atrium night glow is a shell, not a plate under the glazing.** The plan
   specified "a `_Glow` plane *under* the glazing, not a shell". That is
   unbuildable here: the glazing is opaque, so a plate beneath it is invisible —
   the first night render had a completely dark atrium. It is now a thin closed
   shell 0.12 m proud of the glass. A closed shell stacks two alpha layers and
   reads ~23% by day, so its colour is set to the glazing's own `Toy_glassl`
   value: by day the overlay is invisible, at night the hip becomes the lantern.
5. **The portal had to stand proud of its own surround.** Built first as a dark
   arch recessed behind a solid cream surround plate, which swallowed it
   completely — the applied-panel recess trap. The dark arch now sits 0.06 m in
   front of the surround and reads as a deep opening.
6. **Six fan discs and ~20 roof boxes lost their bevels after the first
   forensic census.** A beveled 10-gon cylinder is 276 triangles and there are
   six of them; a two-segment bevel on a roof box is 108. None of it is visible
   at the app's camera distance. 21,292 → **18,508** tris, −13.1%, decided in
   stage 4 but fixed in the build script where it belongs.
7. **Mullions carry no bevel.** They are 0.95 m hairline strips; beveling all 165
   of them cost 5,280 triangles and changed nothing visible. The plan's budget
   assumed they would be beveled.
8. **`Toy_slate` for the roof deck, not `Toy_roofd`.** `Toy_roofd` renders
   near-black on a large horizontal surface in the app; it is used here only on
   small vents.

## 5. Style-bible compliance

- Base / shaft / crown reads at a glance from the high three-quarter aerial.
- Semantic exaggeration spent in one place: the cornice projects 1.85 m against a
  surveyed ~1.15 m, ~+60%, because the silhouette is the building.
- Every roof surface designed: parapet ring, plant enclosures with fan discs,
  bulkheads, ducts, vents, walkways, and the glazed atrium hip in the court.
- Night state is one hero (the atrium) and two supports (the arcade band and the
  portal, warm; a sparse scatter of lit bays, cool). Roughly one bay in six is lit
  and no floor reads as a band. The cornice is not lit.
- No booleans anywhere: every opening is an applied plate standing proud of a
  solid wall.

## 6. Stage 3 — approval

Presented to the user on 19 August 2026 with the contact sheet, the aerial day and
night renders and the numbers above.

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 19 August 2026,
> standing approval given with the pipeline invocation.

Taken as approval to advance to stage 4 (optimize) and stage 5 (integrate, batch
mode).

## 7. Draft manifest entry

```json
{
  "id": "1-market",
  "file": "1-market.glb",
  "anchor": [
    -122.3948075,
    37.7938412
  ],
  "targetHeightM": 48.7,
  "cat": 3,
  "name": "1 Market Street (Southern Pacific Building)",
  "estimated": false,
  "dims": [
    112.2081,
    112.0981,
    48.7
  ],
  "tris": 18508,
  "loadRadius": 2500
}
```

`dims` and `tris` are the **shipped** figures, re-stated after stage 4.

## 8. Stage 5 — integration (batch mode), local QA

Executed 19 August 2026 against `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1,
**Case B**, in batch mode: the bake was run for the QA and then discarded, and the
branch commits source only.

### 8.1 Re-validation before touching the app

`validate_1_market.py` re-run on the shipped GLB in a fresh scene, **every check
PASS**: 18,508 tris (cap 28,000, prompt cap 27,000), min Z 0.000, XY centre offset
0.0005 m, bbox top exactly 48.700 m, 12 `Toy_*` materials, 0 textures, 0
transparent, 0 cameras/lights/animations/armatures/constraints, transforms applied,
0 inverted signed volumes, 0.00% ray residual, no foreign geometry.

Two constants inherited from the `300-brannan` copy of the validator were wrong for
this asset and correctly failed it — the dimension-plausibility range and the
recorded anchor/headings. Adapted (`48.6 ≤ z ≤ 48.8`, `108 ≤ x, y ≤ 116`).

### 8.2 Registry, manifest and the exclusion

`app/public/sf-assets/landmarks_manifest.json` — appended **as text**, `+19 lines,
0 deletions`, so a JSON round-trip could not re-flow floats across the other 103
entries. `camelId('1-market')` → `1Market`, matching the registry id (digits do not
start a segment).

`pipeline/lib/landmarks.mjs` — `id: '1Market'`, `height: 48.7`, **`exclude: 20`**,
`camera: { distance: 330, yaw: 200, pitch: 24 }`.

**The exclusion radius was measured against the real bake input**, not taken from
the plan: both `pipeline/data/buildings_datasf.geojson` and the Overture gap-fill
layer, after `simplifyRing` at 0.6 m, testing centroid **and** every vertex exactly
as `excluded()` does.

| Gate | Ring | Verdict |
|---|---|---|
| **2.4 m** | overture `Southern Pacific Building` h=60.05 | must drop — the OSM trace of *this* building as a solid diamond with no court |
| **7.4 m** | datasf `SF3713006` h=46.12 | must drop — this building |
| **16.0 m** | datasf `SF3713007` h=39.71 | drops — the atrium, on the *tower* parcel; unavoidable collateral |
| **35.4 m** | datasf `SF3713007` h=172.41 and h=27.75 | **must survive** — Spear Tower and the podium |

Safe window **(16, 35.4)**, 19.4 m wide; 20 m sits 4 m above the floor and 15.4 m
below the ceiling, both far over the 0.6 m simplify tolerance. **Do not widen: 35.4
deletes a 172 m tower.** The Overture ring is caught by its *centroid*, not by a
vertex — its nearest vertex is 48.4 m away, which is why a vertex-only measurement
would have sized this wrong.

### 8.3 Re-bake

Full chain (`terrain → bridges → buildings → streets → landcover → validate → lore
→ toy → notables → context → muni-shapes`), 5 min 45 s. `pipeline/data` was cloned
from a sibling worktree with APFS copy-on-write; it reproduced `origin/main`'s tiles
exactly, so **1 of 585 building tiles changed** — the one this landmark drops. No
`hgt`-vintage drift to explain.

| Check | Result |
|---|---|
| `pipeline/audit.mjs` **1.6** — no procedural footprint inside a bespoke landmark exclusion zone | **PASS**, 114 zones over 110 landmarks clear |
| audit totals | 29 passed / 3 failed / 1 informational — **byte-identical to `origin/main`** (verified by stashing); the three failures are pre-existing (p95 height, Telegraph Hill DEM, one offshore tree) |
| `pipeline/verify-rebake.mjs` | **PASS** — `new since origin/main: 1Market @ 23_10`; cell 23_10 **49 → 47**; `ok 1Market 35.4 m vs 20 m radius (nearest is 175.5 m tall)` |

Two footprints dropped, not the three measured — and that is correct: the DataSF
pass runs first and `markOccupied` claims the area, so the Overture duplicate was
never in the tile to begin with. The exclusion still has to cover it, because that
is what stops the gap-fill re-adding a 60 m block into the ground the DataSF drop
just freed.

**Proved from the tile, not from the radius** (`tilecheck.mjs`): decoding the nine
cells around the anchor and point-in-polygon-testing all **601** surviving rings
against the asset's own wall footprint returns **zero vertices inside** — no
penetration at any depth. The nearest surviving footprint is 35.4 m away and 175.5 m
tall, i.e. Spear Tower, exactly as designed.

### 8.4 Local verification (Step 5) — all PASS

Driven headless (Chrome + CDP against the built `app/dist`; the in-editor Browser
pane throttles `requestAnimationFrame` to nothing and makes a healthy streaming
landmark look broken).

| Check | Result |
|---|---|
| Merge line | `sf-assets: 1-market merged 14 objects / 12 materials -> batched (11159 tris body); uniform x1.0000 at 3757, -2635` |
| **Uniform scale** | **x1.0000** — the authored height and `targetHeightM` agree exactly |
| Placement | `SF.assets.placed.has('1Market')` true, anchored at local (3757, −2635) |
| Exactly one building on the site | yes — no procedural twin, no baked block poking through, no z-fighting (day/wide screenshots, and §8.3's tile proof) |
| Orientation | Market frontage faces Market Street; Steuart flank faces Steuart |
| Terrain seating | sits flush, no float, no sink |
| Night | only the intended `_Glow` surfaces light: the atrium as a cool lantern, the arcade band and portal warm, a sparse scatter of lit bays |
| **Draw calls** | **avg 91/frame** at the landmark, budget 300 |
| Asset warnings | **none** (the only console warning is the weather feed, which has no API behind a static file server) |
| Streaming | 104 entries, 83 live, 0 loading, 0 fading, 0 failed |

Screenshots: `artifacts/1-market/qa/day.png`, `night.png`, `wide.png`.

### 8.5 Fallback drill (Step 6) — PASS

Run as its own pass with the throwaway file server returning a real **404** for
`/sf-assets/landmarks/1-market.glb`, rather than renaming the file (Vite's dev
server answers a missing public path with `index.html` and HTTP 200, so a rename
cannot produce a fetch failure at all).

| Check | Result |
|---|---|
| **The drill actually exercised the loader** | `failed: 1` — not `0`. A drill that reports `failed: 0` measured nothing and is inconclusive, however healthy it looks |
| App still boots with the GLB missing | yes — `entries: 104`, 71 other landmarks live, the area renders |
| This landmark absent | `SF.assets.placed.has('1Market')` **false** |
| Exactly one warning naming it | yes — `sf-assets: 1-market failed to load (fetch for ".../1-market.glb" responded with 404: Not Found)` |
| Other console warnings | one, the weather feed, which has no API behind a static file server |
| Case B site behaviour | empty ground inside the exclusion zone, as expected and as designed |

Note the **wording**: INTEGRATION-PROMPT Step 6 quotes the *resident* fallback
message ("… — keeping the code-built landmark"). A landmark with a `loadRadius` is
**streamed** and fails through `scan()` with `failed to load` and no "keeping"
suffix. Match on the id, not on the prompt's wording.

The drill's two cosmetic tail steps — the draw-call average and the drill
screenshots — were **not reached**: the machine was at load average 87–220 from a
dozen parallel landmark sessions and the rAF-driven draw-call measurement did not
return. Neither adds anything to Step 6 (draw calls were measured at 91/frame in
the real pass, and a screenshot of an absent building is not evidence), so the run
was stopped there rather than left hanging. The GLB was verified byte-identical
afterwards. Full log: `artifacts/1-market/qa/drill.log`.

### 8.6 `loadRadius` decision

`max(2500, 48.7 × 30) = 2500` m — the default, taken. **Not `alwaysLoaded`**: at
48.7 m this is not a skyline piece, and that list is the only one that still grows
boot cost. Beyond 2,500 m the site is empty ground rather than a procedural
stand-in (Case B), and at that range the absence is illegible.

### 8.7 The shared `BatchedMesh` is 91.8% full — a batch-level finding

Measured from the GLB accessor counts after integration: 104 landmarks now total
**1,468,242** body vertices against `BODY_VERTS = 1_600_000` in
`app/src/assets.js` — **131,758 spare**. 1 Market alone is 33,478 of them, the
fourth-heaviest landmark in the manifest.

The rest of the Embarcadero/Steuart family is roughly eleven more landmarks; at the
manifest's ~20k average they need ~220k vertices and there are 132k. An overflow is
not a crash — `addGeometry` throws, that landmark drops to its procedural
stand-in, and it reads as *a different* landmark quietly missing on each reload.

**`BATCH-INTEGRATE.md` should raise `BODY_VERTS` to 2,000,000 once, in the batch
PR.** Deliberately not changed here: it is a shared constant and eleven branches
editing it is precisely the collision batch mode exists to prevent.

### 8.8 Housekeeping

- `node pipeline/compress-assets.mjs` skips this asset (it already carries
  `EXT_meshopt_compression` from stage 4) and its only effect was to re-compress
  `vehicles/passenger-airplane.glb`, as it does on every branch. Reverted.
- The shipped `app/public/sf-assets/landmarks/1-market.glb` is byte-identical to
  `artifacts/1-market/1-market.glb`.
- `cd app && npm run lint` clean; `npm run build` green with **26/26** tests
  (including `asset-loading.test.mjs` and `muni-motion.test.mjs`).
- **Batch discard done**: `git checkout -- app/public/tiles api/_data`, and
  `git diff --name-only $(git merge-base HEAD origin/main)` lists **zero** files
  under either path.
