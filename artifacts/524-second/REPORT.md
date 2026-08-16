# 524 Second Street — build report

Miniature GLB of 522–524 Second Street, San Francisco, for the SF-SIM toy-diorama city.
Built 16 August 2026 by `build_524_second.py` (Blender 5.2.0 LTS, headless), validated by
`validate_524_second.py` into `validation.json`, rendered by `render_524_second.py`.

**REPORT beats plan.** Where this file disagrees with `docs/asset-plans/524-second.md`,
this file is what shipped, and every deviation is listed in §4.

## 1. Shipped numbers

| | |
|---|---|
| Manifest id | `524-second` |
| File | `524-second.glb` |
| File size | **160,740 B** raw, meshopt-compressed (was 345,036 B pre-optimize, −53.4%) |
| Triangles | **5,620** (budget 11,000) |
| Objects / draw submeshes | 10 objects, 11 primitives after stage 4 (was 105 / 106); the loader merges these to 2 draw calls |
| Dimensions (axis-aligned) | 35.998 x 35.766 x 9.900 m |
| Building along its own axes | 20.92 m frontage x 29.63 m deep |
| min Z / XY centre offset | 0.000 m / (0.000, 0.000) |
| Crest | **9.900 m** — merlon tops; loader scale `targetHeightM / measuredHeight` = 1.000 |
| Anchor (WGS84) | `-122.3934330, 37.7825731` |
| Second Street front heading | **45.6° true (NE)** |
| Taber Place flank heading | 315.4° true (NW) |
| Materials | 10, all `Toy_*`: brick, sand, stone, glass, glassl, roofd, steel, ink, gold_Glow, glass_Glow |
| Glow surfaces | `Toy_gold_Glow` (entrance sign), `Toy_glass_Glow` (5 windows) |
| Category | `19` (industrial) |

The ~36 m axis-aligned bounding box for a 20.92 x 29.63 m building is the expected
consequence of the 45.6° real-world heading, not a scale error.

## 2. Validation — `validation.json`

`overall: PASS`. Fresh factory-reset scene, re-importing the exported GLB; the authoring
`.blend` was not inspected. Re-run after the stage-4 shipping swap, so these are the
**packed** file's numbers — which is the run that matters, because the sliver failure mode
described in `optimize/REPORT.md` §3 shows up only in the packed file.

| Check | Result |
|---|---|
| meters_and_plausible_dimensions | PASS |
| crest_normalized_to_target (9.90 ± 0.02) | PASS |
| base_at_z_zero | PASS (0.000) |
| centered_xy | PASS (0.000, 0.000) |
| under_triangle_budget (11,000) | PASS (5,620) |
| no_image_textures | PASS |
| no_transparency | PASS |
| materials_follow_contract (`Toy_*`, no `Toy_body`) | PASS |
| no_cameras_or_lights | PASS |
| no_animation_skin_or_constraints | PASS |
| transforms_applied | PASS |
| no_negative_scales | PASS |
| normals_outward_signed_volume | PASS — all 10 shipped shells enclose positive volume |
| normals_outward_ray_residual_within_tolerance | PASS |
| no_degenerate_geometry | PASS |
| no_unexpected_objects | PASS |

Normal-orientation method: every source mesh runs `bmesh.ops.recalc_face_normals` before
export; re-imported loop normals must be finite and unit; **per-object signed volume is
authoritative** for this union of interpenetrating solids; 31,500 deterministic
visibility rays from nine interior targets test the first visible face, with a 0.15%
residual allowed at coincident faces.

## 3. Renders

All regenerated from the final export: `524-second-north.png`, `-east.png`, `-south.png`,
`-west.png` (one orthographic rig, identical scale/framing/lighting/exposure, differing
only in azimuth), `-top.png`, `-aerial.png`, `-aerial-night.png`, and
`524-second-contact-sheet.png`.

Because the building sits at 45.6°, every axis-aligned elevation shows it obliquely and
each sees two faces: NORTH and EAST see a public elevation together with a party wall,
SOUTH sees both party walls, WEST sees Taber Place and the rear. That is the expected
consequence of the real heading. The aerial azimuth is **due north** — the only direction
that shows the Second Street front and the Taber Place flank together, which is the corner
condition this asset exists to carry.

## 4. Dossier corrections and design decisions

Everything below changed after the plan was written. Four came out of review renders.

1. **Floor levels were ~1 m too high in the first build.** The plan's §2.7 put ground
   glazing at 1.10–4.20 m and second-floor glazing at 5.55–8.10 m. The first aerial
   review showed a second storey riding hard against the parapet. Re-rectifying the May
   2025 panorama against the measured 20.92 m frontage — and solving the camera height
   from the same image, which gives 2.35 m and makes the width- and height-derived scales
   agree to 6% — put the paint line at 4.05 m, ground glazing at 0.80–3.75 m and second-
   floor glazing at 4.70–7.75 m. **Shipped values are the re-measured ones.**
2. **The merlons were too weak.** At the plan's 0.85 x 0.40 x 0.45 m on a 9.45 m coping
   they read as a faint dotted line from the aerial camera — fatal for the one cue this
   building has. Widened to 1.00 m, deepened to 0.48 m, and the coping dropped to 9.32 m
   so the blocks stand **0.58 m** proud. The crest stays at 9.90 m.
3. **The coping is brick, not stone.** Authored pale per plan §2.7, a continuous
   `Toy_stone` band under nine `Toy_stone` blocks read as one lumpy ledge. A brick parapet
   with pale blocks on it is both what the panorama shows and by far the higher-contrast
   reading of the cue. The parapet ring is also uniform on all four sides rather than
   dropping 0.30 m on the party sides as the plan proposed — with merlons on only two
   edges, that distinction already reads, and a continuous parapet is what a real
   warehouse has.
4. **The night composition is windows-led, not sign-led.** Plan §2.8 called the entrance
   sign the hero. The first night review reversed it: a 1923 office conversion tenanted
   by a venture firm has lit desks, not a marquee. Three lit second-floor windows on
   Second Street and two on Taber Place lead; the permitted door sign (SF permit
   2012-03-27, electric single-faced door/window sign) is the single warm accent against
   them. It was widened from 1.52 to 1.90 m so it holds its own.
5. **Roof plant is capped at 0.85 m.** The plan allowed 1.6 m; at 1.10 m the largest
   rooftop unit out-topped the merlons and took the crest, breaking height normalization
   and stealing the silhouette. 0.85 m also matches the street panorama, where nothing
   shows above the parapet line.
6. **Five roof vents, not three.** The Vexcel aerial shows a straight diagonal run of
   small fixtures crossing the deck; two more on that line keep the rear half of a 620 m2
   roof from reading dead without inventing anything the imagery does not show.
7. **The roof membrane is `Toy_sand` (`#ece4d4`), after two earlier attempts.** The plan
   said `Toy_roofd`; that was rejected at authoring time on `358-brannan`'s recorded
   lesson that a dark deck reads as a black slot from the app's downward camera, and
   `Toy_steel` (`#9aa0a6`) shipped instead. **The stage-5 local QA overturned that too**:
   in the live scene the lit deck measured (90, 98, 107) against (146, 133, 104) on the
   baked neighbours — 27% darker and cooler, the darkest roof on the block, on the single
   biggest surface the app's camera sees. The Vexcel aerial shows this roof as a
   near-white membrane, so `Toy_sand` is both truer and the better top-down read, and it
   lets the brick parapet ring carry the roof edge instead of fighting a mid-grey deck.
   This is the only change made after integration began; the asset was rebuilt,
   re-optimized, re-validated and re-shot end to end.
8. **The entrance bay is 2.40 m wide, not 3.10 m,** and projects 0.45 m. It straddles the
   centre pier and overlaps the neighbouring window frames by ~0.45 m each side — these
   are independent closed solids, not a boolean union, so the overlap is geometrically
   fine and each shell still passes the signed-volume test.
9. **Footprint source: OSM, not DataSF LiDAR.** Three sources disagree by 12% (LiDAR
   569.7 m2, OSM 619.9 m2, parcel 639.1 m2). OSM sits exactly where a lot-line wall sits,
   inset ~0.3 m per side from the property line; the LiDAR polygon is short specifically
   on the Second Street edge, shadowed by a 19.7 m neighbour across a 6 m alley. This is
   the **opposite** call from `358-brannan`, where OSM was wrong — the lesson is to
   reconcile all three every time.
10. **A build bug worth recording.** The Taber Place merlon return was first placed with
    `len_t - u`, which put it 22 m away at the rear corner instead of at the street
    corner. `EDGE_TABER` starts *at* the Second Street corner, so `u` is already measured
    from the street. Caught in the orthographic NORTH elevation, not the aerial.

## 5. Height provenance

| Level | Value | Basis |
|---|---|---|
| Roof membrane | 8.96 m | DataSF LiDAR `hgt_mediancm 896` over 2,293 cells, std 0.95 m — **measured** |
| Parapet coping | 9.32 m | photogrammetric, estimated |
| Merlon tops (crest) | **9.90 m** | photogrammetric, estimated, ±0.6 m |

`"estimated": true` in the manifest entry, because the crest is photogrammetric even
though the membrane under it is measured.

Cross-checks: OSM `height=9` agrees with the LiDAR membrane to 0.04 m. DataSF
`hgt_maxcm = 13.32 m` is **not** this building — against a 0.95 m standard deviation over
2,293 cells it is a handful of cells bleeding from 512 Second Street, 19.7 m tall across a
6 m alley. Neighbours confirm the "lowest on the block" cue: 512 Second 19.71 m, 500 Second
13.66 m, 544 Second 12.83 m.

## 6. Approval (stage 3)

Approved by the owner in advance for this batch, quoted verbatim from the session
instruction of 16 August 2026:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

No revision round was requested; the four review-driven corrections in §4 (items 1–5)
were made by the modeller before presentation.

## 7. Draft manifest entry

```json
{
  "id": "524-second",
  "file": "524-second.glb",
  "anchor": [
    -122.3934330,
    37.7825731
  ],
  "targetHeightM": 9.9,
  "cat": 19,
  "name": "524 Second Street",
  "estimated": true,
  "dims": [
    36.0,
    35.77,
    9.9
  ],
  "tris": 5620,
  "loadRadius": 2500
}
```

`loadRadius`: the skill's default formula gives `max(2500, 9.9 * 30) = 2500` m. Default
taken — at 2.5 km a 9.9 m building is far below a pixel, so the absence of its baked
stand-in beyond the radius is illegible.

## 8. Stage 4 — optimize

Run 16 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2; full detail in
`optimize/REPORT.md`. Headline: 345,036 B → **160,740 B** raw (−53.4%), 106 → 11 draw
submeshes, triangles and bounding box unchanged, worst A/B pixel delta 0.034% against
2–4% gates, all gates G1–G8 PASS. Phase B's limited-dissolve step was **deliberately
skipped** — this asset has two stacked coplanar ring bands (parapet and coping) following
the full footprint, the documented sliver trap; the stage-2 contract validator was re-run
against the *packed* file after the swap and returns `overall: PASS` with zero invalid
loop normals, confirming the skip was correct.

The pre-optimize original is archived at `optimize/input/524-second.glb`. The numbers in
§1 and §2 of this report are the **shipped** ones.

## 9. Stage 5 — local integration QA (batch mode)

Case **B** (new landmark). Registry entry `524Second` in `pipeline/lib/landmarks.mjs`,
manifest entry in `app/public/sf-assets/landmarks_manifest.json`, GLB at
`app/public/sf-assets/landmarks/524-second.glb`.

| Check | Result | Evidence |
|---|---|---|
| Stage-1 re-validation of the shipping GLB | **PASS** | `validation.json`, `overall: PASS`, fresh-scene re-import of the packed file |
| Manifest entry valid + consistently formatted | **PASS** | 59 entries, JSON parses |
| id mapping `524-second` -> `524Second` | **PASS** | `camelId()` round trip; the placed key in `SF.assets.placed` is `524Second`, matching `pipeline/lib/landmarks.mjs` |
| Case B registry entry | **PASS** | `exclude: 11` m, sized from bake-input ring **vertices** |
| Tile re-bake | **PASS** | full chain `terrain -> ... -> context -> muni-shapes`, exit 0 |
| audit 1.6 (no procedural footprint in an exclusion zone) | **PASS** | 66 zones over 65 landmarks clear |
| verify-rebake (only this landmark's cell moved) | **PASS** | 584/585 cells unchanged; `23_13` 217 -> 215; nearest surviving footprint **15.2 m vs the 11 m radius** |
| Single building, no procedural twin, no z-fighting | **PASS** | `integration/524-second-day.png` |
| Loader merge line | **PASS** | `sf-assets: 524-second merged 11 objects / 10 materials -> batched (3368 tris body); uniform x1.0000 at 3878, -1390` |
| Scale factor | **PASS** | **x1.0000** — authored crest and `targetHeightM` agree exactly |
| Orientation | **PASS** | the placement matrix is pure uniform scale + translation with no rotation terms, so the authored true-world heading (front 45.6 deg NE) is the scene heading |
| Terrain seating | **PASS** | placed at y = 14.857 m; DataSF LiDAR ground for this footprint is 14.73 m NAVD88 |
| Night glow | **PASS** | `integration/524-second-night.png` — only the five lit windows and the entrance sign light; the rest of the building stays dark against blazing neighbours |
| Draw calls < 300 | **PASS** | `landmark-streaming-check`: 158/frame at hero, **92/frame** near this landmark |
| Streaming lifecycle | **PASS** | all six `landmark-streaming-check` assertions PASS: unloaded at boot, loads on approach, releases on depart, re-approach with zero failures |
| Fallback drill (mandatory) | **PASS** | GLB renamed away: app boots, city renders, exactly one `sf-assets: 524-second failed to load` warning, `failed: 1`, and the site is **empty ground inside the exclusion zone** — expected for Case B. `integration/524-second-fallback-day.png`. Restored afterwards |
| `npm run lint` / `npm run build` | **PASS** | eslint clean; build ok |

**Local-QA environment note.** The in-app Browser pane runs its tab with
`document.hidden === true`, which stops rAF — the app rendered 22 frames in two minutes
and every screenshot came back black. This is the documented behaviour in
`.agents/skills/testing-sf-3d/SKILL.md` ("a hidden tab never reveals on its own... drive
it with a real foregrounded Chrome"). The screenshots above were therefore taken with
`integration/shoot.mjs`, a small CDP harness modelled on `pipeline/perf-harness.mjs`
that launches headless Chrome with `--disable-backgrounding-occluded-windows
--disable-renderer-backgrounding` and changes no app runtime code. Second gotcha, also
already known: Vite answers a missing GLB with `index.html` at **200**, so the
fallback-drill warning reads `Unexpected token '<'` rather than a 404.

**Batch mode.** Per `ADDRESS-TO-ASSET.md`, the bake was run and QA'd, then discarded with
`git checkout -- app/public/tiles api/_data`; only source is committed. Sanity check
passes: `git diff --name-only origin/main` lists **0** files under `app/public/tiles/` or
`api/_data/`.

## 10. Integration notes

- **New landmark (Case B).** Needs a `pipeline/lib/landmarks.mjs` entry and a tile
  re-bake, or the baked procedural building on this footprint will intersect the GLB.
- **Exclusion radius.** Size it from neighbour *vertices*, not centroids, and measure it
  against the real bake input. The southeast party wall is shared with 544 Second Street
  and the rear wall with the 10 South Park block, so those neighbours' footprints have
  vertices *on* this outline and some collateral is unavoidable. The footprint
  half-diagonal is 18.1 m; start near the half-width, 10.5 m, plus a small margin. Taber
  Place gives free clearance on the northwest side, so the risk is entirely southeast and
  southwest.
- Judge it in the aerial next to `358-brannan`, 200 m away on the same block and from the
  same decade. If the two read as the same building at different widths, the merlon row is
  not doing enough work.
