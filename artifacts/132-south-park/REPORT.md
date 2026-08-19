# 132 South Park — build report

Asset: `132-south-park.glb` — the 1913 flats at 130-134 South Park Street, block
3775 lot 062, plus the rear cottage on the same lot.

**Status: stage 2 gate PASS, stage 4 gate PASS.** `validation.json` is all-PASS on
a fresh-scene re-import of the **shipped** GLB — i.e. the optimized file, re-validated
after the stage-4 shipping swap. The optimize pass is reported separately in
[`optimize/REPORT.md`](./optimize/REPORT.md); the pre-optimize original is archived
at `optimize/input/132-south-park.glb`.

| | |
|---|---|
| Triangles | **3,928** (cap 9,000) |
| Objects | 11 shipped (108 as authored; joined per material at stage 4) |
| File size | **126,760 bytes** raw shipped (276,436 pre-optimize, −54.1%) |
| Draw submeshes | 13 shipped (112 pre-optimize) |
| Dimensions | 26.684 × 26.706 × **12.07** m |
| min Z | 0.0000 |
| XY centre offset | 0.0000, 0.0000 |
| Materials | 10, all `Toy_*`, one `_Glow` |
| Anchor | `-122.3946173, 37.7815393` |
| Front heading | 135.1° true (south-east) |
| Loader scale | `targetHeightM / measuredHeight` = 12.07 / 12.07 = **1.000** |

Build: `blender -b --python build_132_south_park.py --` (Blender 5.2.0 LTS).
Renders: `render_132_south_park.py` (EEVEE, 128 samples), `--night` for the dusk
pass, then `make_contact_sheet.py`.
Validation: `blender -b --python validate_132_south_park.py --`.
Optimize (stage 4): `optimize/` — Phase B geometry cleanup, then
`npx gltfpack@0.24 -c -km -kn -noq`. 108 objects / 112 draw submeshes / 276 KB
became 11 / 13 / 127 KB with the triangle count and the bounding box untouched.

---

## 1. Corrections this build made to the plan

`docs/asset-plans/132-south-park.md` was re-verified before modelling, as the
pipeline requires. Ten things changed. The plan has been amended in place for the
factual ones (marked *amended*); this list is the authoritative log.

1. **The base openings were mirrored.** *(amended)* The plan put the arched carriage
   gate on the south-west half and the sash window on the north-east. The 2021 drone
   frame says the opposite: the camera looks **north-west** at a **south-east**-facing
   front, so photo-right is **north-east**, and the gate is on photo-right — against
   the party wall shared with 126 South Park. Built with the gate at `s 0.15–2.75`
   and the sash window at `s 3.75–5.45`. This is the kind of error that survives
   every geometric check and is only caught by re-reading the photograph's compass.

2. **Floor levels re-derived from the photograph instead of assumed even.** The plan
   divided the height evenly (base 2.24, floor lines 5.42 / 8.59). Measured off the
   drone frame at 76.2 px/m against the LiDAR crest, the real lines are base **2.10**,
   belts **4.95** and **8.05**, hood **10.45–11.47**, cornice band **11.47–12.07**.
   The cornice therefore hangs *below* the roof deck (11.77) and reads 0.60 m deep,
   which is what the photograph shows and what the plan's flat 0.30 m band did not.

3. **The rear cottage's 0.60 m buried skirt was not built.** The plan called for one
   as insurance against the 0.48 m LiDAR ground difference. It cannot coexist with
   the `min Z ≈ 0` contract — any geometry below zero either becomes the model's
   min Z or has to be excluded from the export by hand. And the difference is almost
   certainly not real: the two footprints are measured from two different LiDAR
   source tiles (`Sanfran_Orig_1384.flt` and `_1380.flt`), and South Park is flat.
   Both volumes sit on one datum.

4. **Bay return windows dropped.** The plan implied glazed bay returns. No source
   shows them; more decisively, the bays run to the party lines, so a return window's
   glass would protrude past the lot boundary into 126 and 136 — visible in the app
   as geometry inside a neighbour. The returns are blank, with a yellow corner board.

5. **Bay glazing re-proportioned.** The plan's "two lights per bay face per floor"
   became two punched 0.95 m openings with 0.51 m of glass each — a warehouse rhythm.
   The photograph shows the bay fronts as almost all glass, so each bay face now
   carries **one 2.28 m two-light group** split by a 0.14 m mullion. Same object
   count, far better read, and it is what the building actually is.

6. **The trim exaggeration was split.** The plan set a single 0.22 m trim width.
   Applied to window surrounds that ate 46% of each opening, the facade rendered as a
   yellow grid with cream infill. Window surrounds are now **0.16 m** (near the real
   0.15) and the exaggeration moved to corner boards and belt courses at **0.18 m**,
   with relief raised to 0.05 m. The trim still reads as a drawn outline from the
   aerial camera; the glass survives.

7. **The hood spans the whole facade, flat-fronted.** The plan's hood "spanning
   between the two bay tops" was built first as a hipped solid sloping back in `t`
   — and disappeared behind the bays, leaving a dark box floating over the recessed
   centre and nothing else. It is now a continuous band across the full width,
   standing 0.12 m proud of the bay faces, hipped in `s` only. `hipped_hood()` grew a
   `hip_t` parameter that defaults to 0 for exactly this reason.

8. **Night glow changed to `Toy_gold_Glow` `#caa64a`.** *(amended)* The plan specified
   `Toy_glass_Glow` at the base glass colour `#2a4d73`, which renders as cold blue
   light — the opposite of the plan's own stated night proposition ("someone is
   home", the one warm residential front on an arc of dark commercial roofs).
   `Toy_gold_Glow` is the shipped set's established warm-window glow (24 uses).

9. **Roof furniture capped below the crest.** The first build put the vent stacks
   1.00 m above the deck, at 12.77 m — which made *them* the tallest geometry and
   drove the height-normalisation scale to 0.945, silently shrinking the whole lot by
   5.5%. Skylight and stacks now top out at 11.97 and 12.05, under the 12.07 crest,
   so the cornice is the tallest thing and the loader scale is exactly 1.0. A
   parapet ring that hides small roof furniture from street level is also what the
   photograph shows.

10. **Anchor moved 4.2 cm** *(amended)*, from `-122.3946190, 37.7815407` to
    `-122.3946173, 37.7815393`, because the built bounding box shifted when the bay
    projection went to its exaggerated 0.85 m. The build script measures the finished
    bounding box and reports the corrected anchor rather than trusting the plan's
    arithmetic. Re-measured against the bake input, the exclusion window at the
    anchor is unchanged in substance: nearest foreign trigger 3.59 m (was 3.60 m).

## 2. Height derivation

Two independent methods agree to 1 cm, which is the strongest height evidence in
this set:

| Method | Crest |
|---|---|
| DataSF LiDAR `ynuv-fyni`, `sf16_bldgid` 201006.0158439, `hgt_maxcm` | 12.07 m |
| 2021 drone frame at 76.2 px/m: plinth 2.24 px-derived 2.06 m + 3 × 3.28 m floors | 12.08 m |

The LiDAR return is unusually clean here — σ 0.36 m across 234 half-metre cells on a
flat roof behind a parapet, which is the case the 2010 survey reads best. Unlike its
neighbours in this set, the building carries **no OSM `height` tag to conflict with**,
because OSM carries no building on the lot at all.

Roof deck (`hgt_median_m`) 11.77 m; rear cottage 8.75 m crest / 8.40 m deck.

## 3. Palette notes

- **`Toy_red` `#c4453c` is brighter than the real base**, which is a dark oxblood
  nearer `#6d2c2e`. The palette carries no dark maroon and the style bible wants
  accents saturated rather than muddy, so the base takes the same step toward candy
  the real painter took. It holds up against the mustard at review.
- **`Toy_mustard` `#d9a441` is the entire accent budget.** The trim is the identity;
  nothing else on this asset takes a second saturated colour.
- The rear cottage is `Toy_sand` `#ece4d4` against the front block's `Toy_cream`
  `#f2ede3` — one step apart, enough to read as two buildings from above without
  turning the cottage into a second focal point.

## 4. Night state

Five of the twelve bay lights are lit, scattered across floors and across both bays
(`bayNE` floor 2; `baySW` floors 1 and 3), plus **one window on the cottage's
courtyard face** so the void between the two volumes stays legible after dark. Glow
shells are thin panels standing 0.12–0.17 m proud of the opaque glazing, never the
glazing itself — the app renders `_Glow` in a separate layer at ~12% alpha by day, so
a primary surface authored as glow would be a daytime hole.

## 5. Validation

`validation.json`, from a fresh-scene re-import of the exported GLB — not the source
scene. All 16 checks PASS:

```
meters_and_plausible_dimensions          crest_normalized_to_target
base_at_z_zero                           centered_xy
under_triangle_budget                    no_image_textures
no_transparency                          materials_follow_contract
no_cameras_or_lights                     no_animation_skin_or_constraints
transforms_applied                       no_negative_scales
normals_outward_signed_volume            normals_outward_ray_residual_within_tolerance
no_degenerate_geometry                   no_unexpected_objects
```

Re-run against the shipped (optimized) GLB after the stage-4 swap, it still reports
`overall: PASS` with `invalid_or_nonunit_loop_normal_count: 0` — the check that
catches dissolve slivers, and the reason `optimize.py` skips the limited dissolve on
this asset's two coplanar ring bands.

Normals: 0 inverted objects by per-object signed volume — the authority here,
because the asset is a union of solids **and two disjoint shells**; the ray test
residual is 0.0000.

The `centered_xy` check passes on a point **in the courtyard with no geometry near
it**. That is expected for this asset, not a mis-centred export: see `REFERENCE.md`
§3.

## 6. Renders

`132-south-park-{north,east,south,west}.png` (one ortho rig, identical scale,
framing, lighting, exposure and projection; azimuth is the only difference),
`-top.png`, `-aerial.png` (105° azimuth, 38° pitch, 105 mm — a three-quarter to the
building's own 135° axis, so the bay fronts and the block/courtyard/cottage rhythm
read in one frame), `-aerial-night.png`, and `-contact-sheet.png`.

The four cardinal elevations show the building obliquely because it stands at 45° to
the world axes. That is correct and is the same rig the rest of the set uses.

## 7. Approval

Stage 3 gate, quoted verbatim, 2026-08-16:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Given at the start of the session as blanket approval for every gate in
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`, including this one.

## 8. Draft manifest entry

```json
{
  "id": "132-south-park",
  "file": "132-south-park.glb",
  "anchor": [
    -122.3946173,
    37.7815393
  ],
  "targetHeightM": 12.07,
  "cat": 2,
  "name": "130-134 South Park",
  "estimated": false,
  "dims": [
    26.684,
    26.706,
    12.07
  ],
  "tris": 3928,
  "loadRadius": 2500
}
```

Integration is a separate job — `docs/asset-plans/INTEGRATION-PROMPT.md` plus the
Case B exclusion design in `docs/asset-plans/132-south-park.md` §2.13, which is the
most intricate in the registry and must not be adjusted without re-measuring.

## 9. Stage 5 — local integration QA (batch mode)

Case B. `camelId('132-south-park')` = `132SouthPark`, matching the registry id.

**Re-bake.** Full chain run: `terrain bridges buildings streets landcover validate
lore toy notables context muni-shapes`. `muni-shapes` printed the expected
"no 511 key ... leaving the committed file as is".

| Check | Result |
|---|---|
| `node pipeline/audit.mjs` check 1.6 | **PASS** — 68 zones over 65 landmarks clear |
| `node pipeline/verify-rebake.mjs` | **PASS** — only 23_13 moved, 217 → 214 buildings |
| zone clearances after the bake | anchor 3.6 m vs r=2; front 5.9 m vs r=3; rear 5.3 m vs r=3 |

**Exactly the two intended footprints were dropped, and nothing else.** Diffing cell
23_13 against `origin/main` for every footprint within 400 m of the anchor:

| | centroid | height | verdict |
|---|---|---|---|
| dropped | (3778.0, −1268.7) | 12.4 m | this lot's front flats |
| dropped | (3764.5, −1283.2) | 9.2 m | this lot's rear cottage |
| dropped | (3732.0, −1214.3) | 15.4 m | **not ours** — 58 m away, inside `188SouthPark`'s existing 5 m zone. `188SouthPark` is on `origin/main` but the committed tiles predate it, which is what batch mode produces: source-only branches whose bake is deferred to `BATCH-INTEGRATE.md`. |
| **survived** | (3777.8, −1278.9) | 9.6 m | **126 South Park** — spared, 3.59 m from the anchor |
| **survived** | (3759.3, −1279.7) | 5.6 m | **136 South Park** — spared |

Zero collateral. The three-zone design in §2.13 of the plan did exactly what it was
sized to do.

**Runtime, local dev server (Vite 8.2, `http://localhost:5132`):**

| Check | Result |
|---|---|
| manifest served | 200, entry present and byte-correct |
| GLB served | 200, `model/gltf-binary`, 126,760 B |
| loader merge line | `132SouthPark … uniform x1.0000 at 3773, -1276` |
| scale | **exactly 1.0000** — authored height and `targetHeightM` agree |
| position | world (3773, −1276) = the surveyed anchor |
| asset system | 59 entries, 53 live, 6 far, **0 failed** |
| batching | one `landmark-bodies` + one `landmark-glow` mesh, 52 instances each, `frustumCulled: false` |
| draw calls | **92** (budget < 300) |
| one building on the site | yes — no procedural twin, no baked block poking through, no z-fighting |
| footprint size / orientation | correct against the block; the front faces the park at 135° |
| terrain seating | sits flat, no float or sink (terrain y 8.82 m vs LiDAR ground 8.98 m) |
| night | only the intended `_Glow` surfaces light — five warm gold bay windows plus the one on the cottage's courtyard face; roof, cornice and base stay dark |

**Fallback drill (mandatory, AGENTS rule 3).** GLB renamed away, page reloaded:

- the app boots and the whole city renders — no crash, no hole
- **exactly one** warning:
  `sf-assets: 132-south-park failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)`
  — one, and only one, from the asset system. The JSON wording is the known dev-server
  gotcha: Vite answers a missing static file with `index.html` and a 200, so the loader
  parses HTML instead of receiving a 404. In production the same path 404s and produces
  the same single warning.
- every other asset still loaded: `live: 52, failed: 1`. One failure does not cascade.
- Case B, as expected: the site is **empty ground inside the exclusion zone**, with 126
  and 136 South Park standing either side. Noted, not a defect.
- file restored; `npm run lint` clean; `npm run build` succeeded (950 kB JS / 269 kB gzip,
  3,315 tiles compressed).

**Batch mode.** The bake was run and used for the QA above, then discarded
(`git checkout -- app/public/tiles api/_data`). `git diff --name-only origin/main`
lists nothing under `app/public/tiles/` or `api/_data/`. The branch carries source only:
the GLB, the manifest entry, the registry entry, this plan and `artifacts/132-south-park/`.

**Environment notes, recorded so the next session does not re-discover them:**

- All five preview-manager dev-server slots were held by concurrent sessions, so Vite
  was started directly and the Browser pane attached to `http://localhost:5132`.
- The Browser pane goes hidden between tool calls, which stalls `requestAnimationFrame`
  and therefore the streaming pump. Landmark promotion had to be driven by hand with
  `SF.assets.update(camera.position, dt)`. Do **not** also call `SF.assets.load()` by
  hand: a second manifest load collides with the app's own and reports ~34 spurious
  `failed` entries. Every number above is from a clean reload.
- Three `audit.mjs` checks unrelated to this landmark fail on this branch and on
  `origin/main` alike — 1.2b (p95 height), 1.3c (Telegraph Hill Terrarium DEM 90.5 m vs
  surveyed 84 m), 1.7b (1 of 793 sampled trees offshore). Pre-existing baseline.
