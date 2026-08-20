# 131 Steuart Street (Steuart Place) — build report

**Asset:** `artifacts/131-steuart/131-steuart.glb` — a validated miniature of the
1907 red-brick block at 131 Steuart Street, San Francisco, with its 1983
cast-stone Embarcadero elevation and its barrel-roofed penthouse crest.

Plan of record: `docs/asset-plans/131-steuart.md`. Research dossier:
`REFERENCE.md` (which beats the plan wherever they disagree).

## Numbers

| | |
|---|---|
| Triangles | **6,842** (cap 12,000) |
| Objects | **13** after the stage-4 join (196 as authored) |
| Dimensions (axis-aligned) | 41.221 × 41.346 × **27.700** m |
| Real dimensions | 14.16 × 42.07 m footprint, 27.7 m to the barrel crown |
| Min Z / max Z | 0.000 / 27.700 |
| Loader scale (`targetHeightM / measuredHeight`) | **1.000000** |
| XY centre offset | (0.0017, 0.0008) m |
| Materials | 11, all `Toy_*` |
| Glow materials | `Toy_glassl_Glow`, `Toy_gold_Glow` |
| File | **191,416 B** raw, meshopt (pre-optimize 448,708 B; see `optimize/REPORT.md`) |
| Normals — ray-cast residual | 0.000127 (gate 0.0015) |
| Normals — inverted signed-volume objects | 0 |
| Anchor | `-122.3924386, 37.7930568` |
| Heading | Steuart front 224.9° true; Embarcadero front 44.8° |

The axis-aligned bounding box is ~41.2 × 41.3 m even though the building is
14.16 × 42.07 m: the footprint sits at 44.8° to the world axes and the model is
authored at its real heading, so this is expected, not a scale error.

## Validation

`validate_131_steuart.py` re-imports the exported GLB into a fresh isolated
scene and validates the re-import. `validation.json` — **overall PASS**, every
check green:

| Check | Result |
|---|---|
| meters_and_plausible_dimensions | PASS |
| base_at_z_zero | PASS |
| crest_is_target_height (27.7 ± 0.01) | PASS |
| centered_xy | PASS |
| under_triangle_budget (6,842 ≤ 12,000) | PASS |
| no_image_textures | PASS |
| no_transparency | PASS |
| materials_follow_contract | PASS |
| no_cameras_or_lights | PASS |
| no_animation_skin_or_constraints | PASS |
| transforms_applied | PASS |
| no_negative_scales | PASS |
| normals_outward | PASS |
| no_degenerate_geometry | PASS |
| no_unexpected_objects | PASS |

## Renders

`131-steuart-contact-sheet.png` collects all seven:

- `131-steuart-top.png` — roof plan: cornice ring, monitor spine, plant, skylight, barrel penthouse at the NE end
- `131-steuart-aerial.png` — high three-quarter from the bay (NE), 40° down, 62 mm
- `131-steuart-night.png` — the same camera, night state
- `131-steuart-south.png` — Steuart Street elevation (SW, 224.9°)
- `131-steuart-north.png` — The Embarcadero elevation (NE, 44.8°)
- `131-steuart-east.png` — SE party wall with 141 Steuart (135.0°)
- `131-steuart-west.png` — NW party wall with 121 Steuart (314.6°)

Rendered from the **exported GLB**, re-imported into an empty scene, so every
image depicts exactly what ships. The review rig ran in its `--fast` mode
(Workbench day / EEVEE night) because this machine was carrying a load average
above 100 from parallel sessions; the flat-colour toy palette survives the swap
intact.

## Corrections made during the build

1. **Anchor moved 7.6 cm**, from the plan's polygon centroid
   (`-122.3924393, 37.7930564`) to the footprint AABB centre
   (`-122.3924386, 37.7930568`), so the exported XY offset is exactly zero.
   **The manifest and registry must use the AABB centre.**
2. **`Toy_slate` → `Toy_sash`.** The plan specified `Toy_slate` `6f7883` for the
   cornice, string course and shopfront joinery. That is a blue-grey and it read
   wrong against the brick; the real metalwork is a near-black green. Shipped
   with `Toy_sash` `2f4f49` (precedent `artifacts/21-south-park`).
3. **Party walls simplified.** The plan's flank treatment (three horizontal floor
   lines plus three vertical strips per flank) rendered as blurry smudges and one
   vertical strip straddled the cast-stone band. The verticals were dropped and
   the horizontals confined to the brick run.
4. **Roof rebalanced.** The monitor spine's first cap was `Toy_ink` and read as a
   black bar down the middle of the roof — the same failure mode as
   `Toy_roofd`. It ships as `Toy_cream` over a `Toy_steel` body, with the plant
   in cream and the skylight in `Toy_glass`.

## Traps hit, for the next asset

1. **A 2013-era Street View panorama stitches to 3584 × 1664, not 4096 × 2048.**
   Measure the non-black extent of the stitched equirect before using it; the
   modern geometry made every height read ~10 % low.
2. **Re-imported `_Glow` materials carry a default WHITE emission**, because
   glTF writes `emissiveFactor = 0` when the authored strength is 0. The first
   night render was a slab of pure white. The render script now copies Base
   Color into Emission Color at strength 1.0 before rendering — which is also
   exactly what the app does, since its night layer is unlit at the baked colour.
   (Already documented in `docs/asset-plans/README.md`; hit anyway.)
3. **Workbench's MATERIAL colour mode reads `material.diffuse_color`**, which the
   glTF importer leaves at the 0.8 grey default. The `--fast` review renders
   showed a maroon building until the render script started syncing
   `diffuse_color` from the BSDF after import.

## Stage 4 — optimize

Run and reported in `optimize/REPORT.md`. All gates G1–G6 and G8 PASS (G7 n/a,
bake mode off): 196 objects → 13, 199 draw primitives → 16, 13,712 verts →
13,444, raw bytes 448,708 → **191,416** (−57.3 %), worst A/B pixel delta
0.1995 % against 2 %/4 % gates. Triangles unchanged at 6,842. The optimized file
is now the shipping GLB; the pre-optimize original is archived at
`optimize/input/131-steuart.glb`. The limited-dissolve step was deliberately
skipped — this asset has four full-footprint coplanar ring bands and that step
is the only one that can manufacture degenerate geometry.

Post-swap re-validation: **overall PASS**, all 15 checks, numbers above.

## Stage 5 — integration (Case B, BATCH mode)

Executed against `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 with the
stage-5 amendments in `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.

**Source changes** (this is a batch, so the bake is NOT committed):

- `app/public/sf-assets/landmarks/131-steuart.glb` — the stage-4 output, copied
  byte-identical, already meshopt-compressed so `compress-assets.mjs` skips it
- `app/public/sf-assets/landmarks_manifest.json` — one entry, appended as text
  (**+19 / −0**, the clean-append signature; a JSON round trip would have
  rewritten floats across unrelated entries)
- `pipeline/lib/landmarks.mjs` — the `131Steuart` registry entry, `exclude: 8`,
  camera preset `{ distance: 200, yaw: 135, pitch: 28 }`

`camelId('131-steuart')` → `131Steuart`, matching the registry id; digits do not
start a segment, so the round trip is exact.

**The re-bake.** Only the cell holding this landmark moved:

```
584 of 585 cells unchanged
23_10     49 -> 48   <- 131Steuart
PASS  only the new landmarks' cells moved, and every asset has clear ground under it
```

`audit.mjs` check 1.6 (no procedural footprint inside a bespoke exclusion zone):
**PASS**, 114 zones over 110 landmarks clear. The three unrelated audit failures
(1.2b city-wide p95 height, 1.3c Telegraph Hill DEM, 1.7b one offshore tree of
792 sampled) are pre-existing city-scale checks.

Two exclusion findings worth keeping:

1. **Two rings measured, one dropped, and that is correct.** The exclusion had to
   cover both the DataSF footprint (centroid 1.80 m) and the Overture ring
   (0.08 m), but the bake runs DataSF first and Overture only gap-fills where
   `markOccupied` has not already claimed the area — so the Overture twin never
   reached the tile. The radius still has to cover it, or the gap-fill would
   re-add a building into the ground the DataSF drop just freed.
2. **121 Steuart survives and overhangs by 0.438 m.** Proved from the tile, not
   from the radius: decoding `app/public/tiles/buildings/23_10.bin` and running
   point-in-polygon against the real footprint gives one intruder at 0.438 m of
   penetration, which is 121 Steuart's party wall. Its centroid is 13.59 m from
   the anchor, so any radius that cleared it would delete a real neighbour with
   no hand-built replacement. 0.438 m sits inside this asset's own 0.52 m cornice
   projection, so it is buried. 141 Steuart (centroid 14.55 m, top 23.0 m)
   survives as required — it shares the parcel but is a separate mass.

**Shared landmark BatchedMesh.** Sized from the GLB accessor counts across the
whole manifest, no browser needed: **1,447,731 body vertices against the
1,600,000 reserve (90.5 %)**, of which this asset contributes 12,967. Glow is
76,838 / 250,000. An overflow is not a crash — `addGeometry` throws and that
landmark silently drops to its procedural stand-in — so the headroom is worth
recording: 9.5 % left, and the next batch into this district should re-measure
before it lands.

**Step 5 — local QA** (headless Chrome over CDP against `app/dist`, because
parallel sessions hold every `preview_start` slot):

| Check | Result |
|---|---|
| manifest entry loads | **PASS** — `sf-assets: 131-steuart merged 16 objects / 11 materials -> batched (4322 tris body); uniform x1.0000 at 3965, -2549` |
| uniform scale ≈ 1.0 | **PASS** — exactly `x1.0000` |
| draw calls < 300 at the landmark | **PASS** — avg **91**/frame |
| no asset warnings | **PASS** |
| single building at the site | **PASS** — from the tile (above), not from a pick: `SF.pick()` throws on the landmark BatchedMesh |
| terrain seating | **PASS** — wide shot, no floating or sinking on the waterfront |
| night glow | **PASS** — penthouse lantern hero, two lit office bands, ground-floor restaurant; nothing else lights |

`SF.assets.stats()` at the landmark: `entries 104, live 84, loading 0, fading 0,
failed 0` — 84 landmarks resident at once in the SoMa/Embarcadero cluster with
no dropped-landmark warning.

**On the day screenshot.** The registry preset looks in from the north-east,
which is the only angle where the barrel-roofed penthouse reads against the brick
cornice. At 14:30 the sun is south-south-west, so that elevation is backlit and
`qa/day.png` is close to a silhouette. `qa/day-morning.png` re-shoots the same
rig at 09:30, when the sun lights the face the preset points at. The preset is
right for silhouette and wrong for a midday portrait; both frames are kept.

**Step 6 — fallback drill.** The GLB is never moved: the throwaway file server
returns a real 404 for `/sf-assets/landmarks/131-steuart.glb`, which is honest
and reversible (Vite answers a missing public path with `index.html` and HTTP
200, so the rename trick cannot produce a fetch failure at all).

`INTEGRATION-PROMPT.md` Step 6 quotes the warning as
`sf-assets: ... — keeping the code-built landmark`. **That is the resident path.**
This landmark is streamed (`loadRadius: 2500`), so the failure goes through
`scan()`, which logs `sf-assets: 131-steuart failed to load (...)` with no
"keeping" suffix. Matching on the prompt's literal wording would have reported a
false FAIL; the harness matches on the asset id.

| Check | Result |
|---|---|
| the loader actually attempted the fetch | **PASS** — `failed: 1` |
| exactly one fallback warning | **PASS** — `sf-assets: 131-steuart failed to load (... 404 ...)` |
| app still boots with the GLB missing | **PASS** — `entries 104, live 80, failed 1` |
| Case B: the site is empty ground inside the exclusion zone | **PASS** — expected and by design; the baked block was removed by `exclude: 8` |

`failed: 1` is the load-bearing line: `failed: 0` proves nothing unless the
loader actually reached for the file, and that exact false pass has been recorded
before. The drill ran as its own pass with **no render call in it** — under this
machine's load (average 85-400 from parallel sessions) that is the one Step-6
item reliably obtainable, and a first attempt with screenshots in it was killed
mid-frame before printing its assertions.

**Files.** `qa/qa.json` and `qa/drill.json` hold the machine-readable records;
`qa/day.png`, `qa/day-morning.png`, `qa/night.png`, `qa/wide.png` and
`qa/drill-day.png` are the frames. `qa_local.mjs` and `qa_morning_shot.mjs` are
the harnesses, committed so the pass is reproducible.

**Honest note on the frames.** All of them carry the city's LOD hashed-alpha
cross-fade dither, which is separate from the landmark streamer the harness gates
on (`fading === 0 && loading === 0` were both satisfied). The landmark itself
renders solid in every frame. The `r/simfrancisco` panel reads "CANNOT REACH THE
FEED" because the throwaway file server has no `/api` — expected locally.


## Approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"
> — David, 18 August 2026 (given up front, covering every gate in this run)

Stage 3 gate satisfied by that standing approval; no revision round was
requested. Recorded here verbatim as the pipeline requires.
