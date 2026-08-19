# 424 Brannan Street (Tower Valet Parking lot) — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run 18 August 2026 against
`docs/asset-plans/424-brannan.md`. **REPORT beats plan**: every place this build
departs from the plan is listed in §3, and the plan was corrected first in
`REFERENCE.md` rather than silently followed.

## 1. What was built

A terrain-draped miniature of the surface parking lot at 424 Brannan Street —
block 3776 lot 455, run as Tower Valet Parking, 60 permitted stalls. **There is
no building on this site and none was modelled.** DataSF returns zero building
footprints on the parcel, the assessor carries it as class V vacant with $0 of
improvements, and the entitled SOM office scheme (288 Ritch / 55 Zoe) has never
broken ground — its two 2019 DBI permits are still at status `filed`.

Deliverables in `artifacts/424-brannan/`:

| File | What it is |
|---|---|
| `424-brannan.glb` | the shipping asset — **356,972 bytes**, meshopt-packed at stage 4 |
| `424-brannan.blend` | the authoring scene |
| `build_424_brannan.py` | deterministic rebuild (`blender -b --python …`) |
| `extract_site.mjs` | DataSF parcel → `data/site_uv.json` (the measured ring) |
| `sample_terrain.mjs` | baked heightmap → `data/terrain_uv.json` (the drape grid) |
| `render_424_brannan.py` | the review rig, day and `--night` |
| `validate_424_brannan.py` | the contract gate → `validation.json` |
| `make_contact_sheet.py` | assembles the contact sheet |
| `REFERENCE.md` | the research dossier behind every number |
| 8 PNG renders + contact sheet | top, aerial, grazing, night, four elevations |

## 2. Numbers

| | |
|---|---|
| Triangles | **8,940** / 18,000 cap (12,632 before the stage-4 census; see §10) |
| Objects | 37 authored, 21 after the per-material join |
| Dimensions | 88.8432 x 59.9340 x **8.5649** m |
| Shipped GLB | **356,972 bytes** meshopt-packed (514,628 unpacked) |
| `min_z` | **−1.0844 m** — negative by design, see §4 |
| XY centre offset | −0.0002, 0.1181 m |
| `targetHeightM` | **8.5649 m** = the measured bbox height, so loader scale = 1.0000 |
| Anchor | −122.3954857, 37.7798744 |
| Anchor ground | 5.8894 m |
| Terrain fall | 1.4692 m, planar to 0.1022 m |
| Plate clearance above terrain | 0.1200 m everywhere; spread **0.00000 m** over 1,236 top-cap vertices |
| Stalls | **60** — matches SFPD permit 500106 exactly |
| Cars | 18 |
| Fence posts | 93 |
| Wheel stops | 44 |
| Draw primitives | 22 (from 38) |
| Materials | 20, all `Toy_*`, all on-palette, no textures, no alpha, no `Toy_body` |
| Glow | 4 — `Toy_red_Glow`, `Toy_white_Glow` (the sign), `Toy_trim_Glow` (booth window), `Toy_gold_Glow` (three lamp heads) |

Triangle split (shipped): plate 1,236 · fence posts 1,116 · striping 1,056 ·
car cabins 792 · wheel stops 528 · cars (7 colours) 1,728 · crowns 384 · fence
rail 288 · everything else under 200 each.

## 3. Where this build departs from the plan

Six departures, all deliberate, all found by looking at renders rather than by
reasoning.

1. **Row Z holds 7 bays, not 10, and the balance moved to a parallel row on
   Brannan.** The plan allocated 10 stalls along the 25.62 m Zoe frontage; minus
   a 7 m gate that frontage only holds 7 at a 2.65 m pitch. The five extra
   stalls are **parallel** bays in the 4 m strip the Brannan neck's bay module
   leaves over — which is what such strips carry in life. Final allocation:
   R 23, M 11, C1 8, C2 6, Z 7, A 5 = **60**.
2. **Row C2 lost a bay to the thicket** (7 → 6). The volunteer thicket measured
   at (u −2.0, v −30.8) straddles the parcel line into the private lot next
   door; pulling it wholly inside put its crowns over C2's last bay.
3. **The fence has no full-height mesh panel.** The first build gave it a
   1.05 m opaque band in a near-plate tone, and the Ritch elevation came back as
   a continuous white wall with the cars hidden behind it — the exact "walling
   in" failure the plan warned about. Replaced with posts (2.30 m) + top rail +
   mid rail + a 0.87 m `Toy_steel` band, which reads as chain-link at street
   level and as a line from the aerial, and hides nothing.
4. **Aisle direction arrows were added** (7 of them). Not in the plan. Without
   them the spine aisle and the belly cross-aisle are ~700 m2 of blank slab,
   which style bible §13 forbids; with them the lot reads as a one-way loop —
   in at Brannan, up the spine, round the belly, out at Zoe, with a return lane
   against the south-west party wall.
5. **The concrete patch is `Toy_sand`, not `Toy_trim`.** Against a `Toy_stone`
   plate the trim white read as a hole punched in the slab.
6. **No `Toy_mustard` car.** The plan's colour list included one; mustard is the
   striping colour and a mustard car sitting on mustard stripes disappeared.
   Replaced by a second `Toy_stone`.

Two plan values were confirmed rather than corrected: the sign at 6.80 m (still
*inferred*, see `REFERENCE.md` §7.2) and the 18-car count.

## 3a. What stage 4 sent back into the build

The optimize pass's waste census (`optimize/REPORT.md`) found no geometry to
remove — no duplicate meshes, no buried faces, no over-tessellation — and
pointed instead at two bevels: 93 fence posts carrying 3,652 triangles of
chamfer on a 90 mm section, and 18 car cabins at two bevel segments. Both are
sub-pixel at every distance the app renders this from, and together they were a
fifth of the file. `build_424_brannan.py` was changed to drop the post bevel and
halve the cabin segments and the asset was rebuilt — 12,632 → 8,944 triangles,
726,280 → 514,628 bytes — before packing. Without that the packed file would
have been 519 KB, over the 500 KB per-landmark budget in `AGENTS.md`; it ships
at 357 KB.

## 4. The two deliberate contract deviations

Both are asserted by `validate_424_brannan.py` as named checks, not tolerated as
slips. The full argument is in `REFERENCE.md` §4.

- **D1 — `min_z` is negative (−1.0844 m).** This asset IS the ground.
  `placeGeneric()` seats a landmark from one terrain sample at the anchor, so
  z = 0 must mean the anchor's ground, not the bottom of the model. The check
  that replaces "min_z ≈ 0" is **D2**: the plate's top face stands a constant
  0.1200 m above the sampled terrain across its whole area — measured spread
  **0.00000 m** over 1,236 vertices.
- **D3 — `targetHeightM` is the vertical extent (8.5649 m), not an architectural
  height**, because the loader's scale is `targetHeightM / bbox height` and has
  to land on 1.0.

A third judgement worth recording: the drape interpolates the **sampled grid**,
not the fitted plane. The terrain here is planar to 0.1022 m, and 0.1022 m of
residual against 0.1200 m of plate clearance would have left the slab 18 mm off
the ground at the worst point. The grid is what the runtime samples; using it
put the spread at zero.

## 5. The normals gate, and why the whole-model ray test reads 27%

`validation.json` reports three numbers:

| Probe | Value | Meaning |
|---|---|---|
| whole-model ray residual | 27.17% | meaningless here |
| exposed-geometry ray residual | 25.48% | still meaningless |
| **per-object self-ray residual** | **2.16%** | the diagnostic |
| **per-object signed volume** | **all positive** | **the gate** |

This asset is a union of 37 solids that deliberately abut and interpenetrate:
the plate is 103 side-by-side prisms, every superstructure's bottom cap is
buried inside it so nothing is coplanar with the paving, the fence band passes
through every post, and each car's cabin sits in its body. A scene-wide outward
probe therefore hits a neighbouring solid on a quarter of all faces by
construction. `artifacts/64-south-park/validate_64_south_park.py` makes the same
argument and lands in the same place: **per-object signed volume is the
authoritative test for a union of closed solids**, and it passes for all 37.

The self-ray probe (each face tested only against its own object) is the
inversion tripwire beside it. Its offenders are listed and every one is an
overlap by design: `fence_barb`/`fence_mesh`/`fence_rail` 12.5% (adjacent runs
overlap by one end cap at each corner), `striping` 9.1% (each arrow's barbs on
its shaft), `kerb` 4.5% (the Ritch/Brannan corner), `crowns` 1.3% (the three
thicket crowns in each other). An inside-out solid would score near 100%, so the
gate is set at 40% per object — comfortably clear of both.

## 6. Validation

`validation.json`, from a fresh-scene re-import of the shipped GLB:

```
PASS  single_glb                        PASS  no_negative_scale
PASS  triangles_within_cap              PASS  transforms_applied
PASS  no_textures                       PASS  normals_outward_signed_volume
PASS  no_alpha                          PASS  no_object_self_ray_above_40pct
PASS  all_materials_toy_prefixed        PASS  xy_centred_within_1m
PASS  no_toy_body                       PASS  D1_min_z_is_negative_by_design
PASS  has_glow                          PASS  D2_plate_clearance_constant
PASS  no_cameras                        PASS  D3_targetHeight_is_bbox_extent
PASS  no_lights                         PASS  D4_terrain_residual_recorded
PASS  no_animations
PASS  no_armatures                      OVERALL: PASS
```

## 7. Night state

Three lit things in a dark field, which is what this lot is after dark: the
**PUBLIC PARKING sign** (hero — a lit box sign in reality), the **booth window**,
and **three lamp heads**. The plate, the striping, the fence and the cars all go
dark. Glow surfaces are thin plates 20 mm proud of the sign board's Brannan face
only, never closed shells around it — the app's day pass would otherwise show
them at ~23% rather than 12% and tint the board. `fade_glow()` in the render rig
zeroes emission as well as alpha, and `light_glow()` drives emission from Base
Color rather than the re-imported material's default white.

## 8. Draft manifest entry

```json
{
  "id": "424-brannan",
  "file": "424-brannan.glb",
  "anchor": [
    -122.3954857,
    37.7798744
  ],
  "targetHeightM": 8.5649,
  "cat": 23,
  "name": "424 Brannan Street Parking",
  "estimated": false,
  "dims": [
    88.815,
    59.9199,
    8.5649
  ],
  "tris": 12632,
  "loadRadius": 2500
}
```

`cat 23` is `parking_garage` in `pipeline/taxonomy.mjs`'s `CATS`, the first
landmark in the manifest to use it. `loadRadius` takes the default
`max(2500, 8.5649 x 30) = 2500` m.

## 9. Approval

**Approved 18 August 2026**, in advance and for the whole run, by David:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Recorded verbatim per stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`. The
contact sheet, the aerial day and night renders and the numbers in §2 were
presented at the same time so the approval has something behind it; no
iteration was requested. Nothing was integrated by this stage — the production
manifest, `pipeline/lib/landmarks.mjs` and the baked tiles are untouched.

---

## 10. Stage 5 — integration (batch mode), 18 August 2026

Run from `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1, Case B, in batch mode:
the branch carries **source only**, and the city is baked once for the whole
batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

### What changed

| File | Change |
|---|---|
| `app/public/sf-assets/landmarks/424-brannan.glb` | new, 356,972 bytes, byte-identical to `artifacts/424-brannan/424-brannan.glb` |
| `app/public/sf-assets/landmarks_manifest.json` | +19 lines, one appended entry — **appended as text**, never re-serialised, so no other landmark's `11.0` became `11` |
| `pipeline/lib/landmarks.mjs` | +42 lines, one `424Brannan` entry **with no `exclude`** and the measurement that justifies it |

`git diff --name-only origin/main` lists nothing under `app/public/tiles/` or
`api/_data/` — the batch-mode sanity check.

### The exclusion decision, measured

Every other landmark in the registry needs an `exclude` radius to delete the
procedural building standing where its GLB goes. This one has no procedural
building. Measured against the real bake inputs from the anchor, by nearest ring
**vertex** or centroid — which is what `excluded()` fires on:

```
  10.27 m  Overture b9c9690e-43b        <- the first thing at risk
  10.63 m  DataSF SF3776151 (426 Brannan, the Brickhouse block)
  19.58 m  Overture b9c91621-afe
  21.27 m  DataSF SF3776015 (434 Brannan)
  25.18 m  DataSF SF3776106
```

Footprints with a **centroid inside the parcel: DataSF 0, Overture 0.** So the
safe band is (0, 10.27) m and every radius in it drops exactly nothing. The entry
therefore ships **without** `exclude`; `exclusionZones()` skips a falsy value.

Three independent proofs that this makes the geometry bake a no-op:

1. `exclusionZones()` is **byte-identical** before and after the registry edit —
   99 zones, sha256 `c6af9b30…`, over 96 → 97 landmarks.
2. A full re-bake of the three geometry tiers from `pipeline/data` produced
   **585/585 building tiles, 522/522 street tiles and 549/549 landcover tiles
   byte-identical** to the committed ones. (`buildings.json` differs only because
   `pipeline/out` writes it pretty and the publish step minifies it; parsed, the
   two are equal.) That snapshot reproducing `main` exactly also means there is
   no data-vintage drift to explain.
3. `node pipeline/audit.mjs` check **1.6 PASS** — "no procedural footprint inside
   a bespoke landmark exclusion zone: 99 zones over 97 landmarks clear".

Only the **context** tier changes, to give the lot a pick box, a search-index row
and a `context/landmarks.json` entry; the batch bake regenerates it. Audit also
reports 1.2b, 1.3c and 1.7b as FAIL — all three are pre-existing properties of
the source data (height percentile vs the DataSF roof distribution, the Terrarium
DEM's 90.5 m Telegraph Hill against a surveyed 84 m, one of 792 sampled trees
30 m offshore) and none of them touch a landmark exclusion.

### Local QA

Headless Chrome against the Vite dev server on this worktree (91 manifest
entries served, this entry among them — checked before trusting anything).

| Check | Result |
|---|---|
| id round-trip | `camelId('424-brannan')` = `424Brannan` = the registry id — **PASS** |
| merge line | `sf-assets: 424-brannan merged 22 objects / 20 materials -> batched (7060 tris body); uniform x1.0000 at 3697, -1092` — **PASS** |
| loader scale | **x1.0000** — the drape's `targetHeightM` = bbox-extent rule lands exactly |
| placement | pivot `3697.08, -1091.52` against the computed anchor `3697.078, -1091.514` — **PASS** |
| exactly one building | **PASS** — no procedural twin exists for this site, and no baked footprint has a centroid in the parcel |
| footprint size | the Z reads at its real 88.7 x 59.6 m against the neighbouring block faces — **PASS** |
| orientation | authored in true-world heading, no `yawDeg` override; the neck meets Brannan and the long fence meets Ritch — **PASS** |
| terrain seating | **PASS** — no floating, no sinking; the plate follows the 1.47 m fall |
| night glow | **PASS** — the PUBLIC PARKING sign reads red-and-white at the Brannan corner, booth window and lamp heads faint, everything else dark |
| draw calls | **82** at the landmark, 89 on the drill pass — budget is 300 — **PASS** |
| lint / build | `npm run lint` clean; `npm run build` succeeds — **PASS** |
| fallback drill | **PASS** — see below |

Screenshots: `424-brannan-in-app-day.png`, `424-brannan-in-app-night.png`.

### Fallback drill

GLB moved aside, page reloaded: the app boots, the city is alive, 84 other
landmarks stay live, draw calls 89, and exactly **one** warning appears —

```
sf-assets: 424-brannan failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)
```

The parse error rather than a 404 is Vite's dev server answering a missing
`public/` path with the SPA `index.html` at HTTP 200; the drill still proves what
it is for. Case B: the site degrades to **empty ground**, which is expected here
and is also exactly what the real parcel is. The file was restored afterwards.

### One FAIL, and it is not this asset

On the **stock** `app/src/assets.js` constants the QA pass reports `failed: 1`.
The measurement:

```
with 424-brannan present:  landmark-bodies  1,187,405 / 1,200,000 verts, 83 geoms   -> the 84th fails
with 424-brannan removed:  landmark-bodies  1,187,405 / 1,200,000 verts, 83 geoms   -> identical
with BODY_VERTS raised:    landmark-bodies  1,208,586 / 2,000,000 verts, 84 geoms   -> failed: 0
```

The shared landmark `BatchedMesh` reserve (`BODY_VERTS = 1_200_000`) is **already
98.95% consumed by `origin/main` alone** in the SoMa/South Park cluster — the
1,187,405 / 83 figures are identical with this landmark's file removed, and match
what was recorded on `414-brannan` earlier the same day. Whichever landmark
arrives 84th loses; on one run that was `555-california`, on another it was this
one. Raising the reserve to 2,000,000 / 6,000,000 makes `failed` go to 0 and
places all 84 including this one at `uniform x1.0000`, which is the proof that
the asset itself is sound. **That change was reverted before committing** — a
landmark branch must not carry an `app/src/assets.js` edit, and raising the
reserve for real is a GPU-memory decision for the owner (1.2M → 2.0M vertices is
roughly 43 → 72 MB of body buffer, plus indices 14 → 24 MB).

### A note on the merge line's triangle count

`(7060 tris body)` against a manifest `tris` of 8,940 is not dropped geometry:
`place()` computes it as `bodyGeometry.attributes.position.count / 3`, i.e.
vertices ÷ 3, and the merged geometry is indexed because the meshopt pass
reindexes every GLB. Every shipped landmark shows the same understatement.

### Gate 5

Local QA PASS table above; the ship decision (push / PR / deploy) is the user's
and has not been taken. Nothing has been pushed.
