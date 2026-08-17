# 160 South Park — build report

Miniature GLB for the SF toy-diorama city, built from
`docs/asset-plans/160-south-park.md`. **REPORT beats plan:** where this file and the plan
disagree, this file is what was built and why.

## Shipping numbers

| | |
|---|---|
| Asset | `artifacts/160-south-park/160-south-park.glb` |
| Triangles | **3,792** (cap 7,000) |
| Objects | 9 (50 before stage 4 joined them per material) |
| Dimensions | **25.795 × 17.769 × 9.400 m** |
| Min Z / XY centre | 0.000 / (0.000, 0.000) |
| Materials | `Toy_brick`, `Toy_glass`, `Toy_glass_Glow`, `Toy_glassl_Glow`, `Toy_ink`, `Toy_roofd`, `Toy_rust`, `Toy_steel` |
| Glow groups | 2 — the arched window (hero) and the storefront (accent) |
| File size | **103,120 B raw** / 74,588 B gzip (meshopt; 229,048 / 53,163 before stage 4) |
| Manifest anchor | **`-122.3948620, 37.7812804`** |
| Registry / exclusion point | `-122.3949116, 37.7812949` |
| `targetHeightM` | **9.4** |
| Facade heading | 108.13° true |
| Draw submeshes | 10 (51 before stage 4) |
| Validation | **all-PASS**, `validation.json`, re-run against the shipped optimized file |

The 25.8 × 17.8 m XY box is the ~108° rotation of a 6.2 × 26.5 m strip, not a 26 m
building. That is expected and is checked explicitly by the validator.

## Corrections to the dossier

None of the plan's measured numbers changed. Three things were resolved during the build
that the plan left open, and one convention was tightened:

1. **The roof stack is capped at 9.30 m, below the tile ridge.** The plan's 2.15 flagged
   that the 9.41 m LiDAR maximum could be the tile eave *or* a stack, and that the facade
   appears to have both. The build resolves it in favour of the tile: the ridge is the
   9.400 m bbox top and the stack stops 0.10 m under it. That keeps `targetHeightM` on a
   6 m-wide band the aerial camera can actually see rather than on a 0.5 m² box. If better
   imagery later shows the stack above the tile, the fix is to raise both, not to clip.
2. **The arch's fan was replaced by a continued grid.** The plan's 2.6 called for "three
   radial bars in the head". Built that way it rendered as a peace sign and read as a
   wheel, not as glazing. The verticals now run from the sill straight up into the lunette,
   clipped by the arc, with three horizontals across — which is also what the real window
   does.
3. **Two glow materials, not one.** The plan asked for a hero (arch) and a lower-value
   supporting accent (storefront) but specified one material for both. The app's night
   layer is an unlit overlay drawn at each material's own baked colour, so one colour would
   have lit them identically. The arch is `Toy_glassl_Glow` (#6f95b8), the storefront
   `Toy_glass_Glow` (#2a4d73).
4. **Anchor convention.** The plan's first draft kept the design footprint's *area
   centroid* at the origin. The build follows `artifacts/165-south-park/`: the model is
   recentred so its XY *bounding-box* centre is the origin (contract rule 2) and the same
   (0.428 E, 1.310 N) shift is carried into the anchor, so the building still lands on its
   real footprint. The plan was updated to match.

## Iteration log

**Build 1 — every window on the building was invisible.** There are no booleans in this
build; the body is a solid to `d = 0`. The openings were authored at `d = -0.14 … -0.07`,
i.e. entirely *inside* the wall. The first facade render showed a blank grey wall with an
archivolt on it. Fixed by adopting an explicit depth convention: glazing slabs run from
`d = -0.16` to `d = +0.015` (just proud), muntins sit on the glass at `+0.02 … +0.07`, and
the "recess" reading comes from surrounds standing further proud still (`+0.07` for
windows, `+0.10` for the pilasters, shopfront frame and door).

**Build 1 — the archivolt was a self-intersecting polygon.** It was assembled by splicing
slices of the arch outline, which jumped across the opening and tessellated into a black
diagonal slab over half the facade. Rewritten as one simple horseshoe loop walked in
order: up the outer left jamb, over the outer arc, down the outer right jamb, in, up the
inner right jamb, back round the inner arc, down the inner left.

**Build 2 — the upper panel field did nothing.** A prism from `d = -0.08` to `+0.01` on a
wall that is already solid to `d = 0` is not a recess. Replaced by standing the two end
**pilasters** proud instead, which gives the same reading and keeps the corners crisp
against the party walls.

**Build 2 — the door was hidden behind its own reveal.** The reveal reached `d = +0.10`
and the door only `+0.08`, so the building's one warm accent rendered as a sliver at the
pavement. Reveal pulled back to `+0.02`, door pushed to `+0.10`.

**Build 2 — the tile eave rendered as an orange sausage.** A 0.16 m slab under the standard
0.10 m bevel rounded into a bolster. Thickness cut to 0.11 m, projection to 0.46 m, and the
tile moved onto the light bevel list (0.03/1). It now reads as a band.

**Build 3 — the muntins blew the windows out to near-white.** `Toy_trim` (#f3efe6) made the
darkest building on the block read as the lightest at distance. Switched to `Toy_steel`
(#9aa0a6) — the real muntins are the same slate as the wall, so any lift is already an
exaggeration, and this is the smallest one that still reads as a grid.

**Build 3 — the night preview was two white slabs.** Emission strength 6.0 saturated both
glow surfaces. Dropped to 3.5 in the review rig, and the glow colours split (above) so the
hierarchy the plan asks for is visible. The rig copies `Base Color` into `Emission Color`
before raising strength, because glTF writes `emissiveFactor = 0` and a re-imported `_Glow`
material otherwise carries a default white emission.

**Build 3 — the top view laid the strip across the frame.** For a top-down camera at
`(0, 0, rz)` image-up maps to world `(-sin rz, cos rz)`; `rz = -LONG_AXIS` puts image-up
along the front → rear direction so the strip runs up the frame with the tile band at the
bottom.

## Deviations from the contract, declared

- **"Front faces −Y" is not honoured**, and cannot be: the facade faces 108.13°. Real-world
  orientation wins (AGENTS rule 5, and the orientation note in
  `docs/asset-plans/README.md`), because `placeGeneric()` in `app/src/assets.js` scales and
  positions but never rotates.
- **`Toy_roofd` is used as the wall colour.** The real paint is a cool blue-charcoal around
  `#4a505a`; `#45454a` is the nearest palette entry, and the roof plane takes `Toy_ink`
  (`#3a3530`) so it stays one clear step darker and the plan outline reads from directly
  overhead. On-palette throughout — no off-palette WARN on this asset.
- **`Toy_brick` appears on the tile eave and nowhere else**; `Toy_rust` on the street door
  and nowhere else. Both are load-bearing for recognition and must not be reused if this
  asset is ever revised.

## Validation

`validation.json`, produced by re-importing the exported GLB into a fresh isolated Blender
5.2 scene — the authoring scene is never validated.

| Check | Result |
|---|---|
| Meters, plausible dimensions | PASS |
| Crest normalized to 9.40 m target | PASS (bbox top 9.400) |
| Base at z = 0 | PASS (min Z 0.000) |
| Centred in XY | PASS (0.000, 0.000) |
| Under triangle budget | PASS (3,792 / 7,000) |
| No image textures | PASS (0) |
| No transparency | PASS |
| Materials follow contract | PASS (all `Toy_*`, no `Toy_body`) |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied, no negative scales | PASS |
| Normals outward — per-object signed volume | PASS (9/9 positive) |
| Normals outward — ray test | PASS (31,500 first hits, 0 flipped, 0.000% residual) |
| No degenerate geometry | PASS (0) |
| No unexpected objects | PASS |
| **Overall** | **PASS** |

## Renders

All regenerated from the final export. `-facade.png` is the square-on street elevation at
its own scale; `-east/-west/-north/-south.png` share one rig framed to the 26 m dimension
and are named for the nearest compass direction to each building-aligned face;
`-top.png`, `-aerial.png`, `-aerial-night.png`, and `-contact-sheet.png`.

## Stage 4 — optimize

Run and reported in `optimize/REPORT.md`. Raw bytes −55.0%, draw submeshes 51 → 10,
vertices 7,480 → 1,990 at the weld, triangles unchanged, all gates G1–G8 PASS, worst
A/B pixel delta 0.0218% against a 2% allowance. The limited-dissolve step was skipped
deliberately: this asset's three full-footprint coplanar ring bands are the exact
`350-brannan` sliver trap. The optimized file is now the shipping GLB; the pre-optimize
original is archived at `optimize/input/160-south-park.glb`. Every render in this
directory was regenerated from the shipped file afterwards.

## Draft manifest entry

```json
{
  "id": "160-south-park",
  "file": "160-south-park.glb",
  "anchor": [
    -122.3948620,
    37.7812804
  ],
  "targetHeightM": 9.4,
  "cat": 3,
  "name": "160 South Park",
  "estimated": false,
  "dims": [
    25.7951,
    17.7692,
    9.4
  ],
  "tris": 3792,
  "loadRadius": 2500
}
```

These are the shipped (post-optimize) numbers. The registry entry for
`pipeline/lib/landmarks.mjs` uses the **exclusion** point, not this anchor — see the plan's
2.13; the measured window is `0 < exclude < 1.70 m` and the value is `1.2`.

## Stage 5 — integration (Case B, BATCH mode)

Executed `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 with the batch-mode amendment
from `ADDRESS-TO-ASSET.md`: the bake was run and QA'd against it, then thrown away, and
only source is committed.

### QA table

| Item | Result |
|---|---|
| Re-validation of the shipped GLB in a fresh Blender scene | **PASS** — all 16 contract checks, `validation.json` |
| GLB dropped in, `compress-assets.mjs` run | **PASS** — skipped as already meshopt-compressed (stage 4 packed it) |
| Manifest entry | **PASS** — 59 entries, valid JSON, `dims`/`tris` from the measurement |
| id → registry mapping | **PASS** — `camelId('160-south-park')` = `160SouthPark`, present in `pipeline/lib/landmarks.mjs` |
| Case B registry entry + re-bake | **PASS** — full twelve-stage chain from a warm `pipeline/data` cache |
| `verify-rebake.mjs` | **PASS** — 584 of 585 cells unchanged; only `23_13` moved |
| audit check 1.6 | **PASS** — 66 zones over 65 landmarks clear |
| Single building at the site | **PASS** — nearest surviving footprint 1.70 m against a 1.2 m radius; hiding the landmark batch leaves bare ground |
| Merge line | **PASS** — `sf-assets: 160-south-park merged 10 objects / 8 materials -> batched (2121 tris body); uniform x1.0000 at 3752, -1247` |
| Scale factor | **PASS** — exactly **1.0000** |
| Orientation | **PASS** — facade faces the park; authored at 108.13° true, loader applies no rotation |
| Terrain seating | **PASS** — sits on grade, no float, no sink; local terrain 6.0–7.3 m |
| Night glow | **PASS** — only the arch (hero, `Toy_glassl_Glow`) and the storefront (accent, `Toy_glass_Glow`) light; nothing else |
| Draw calls | **PASS** — peak 95 with the whole neighbourhood live, against the 300 ceiling. The asset adds **zero**: it goes into the shared `landmark-bodies`/`landmark-glow` batch, and both have `frustumCulled = false` |
| Fallback drill | **PASS** — see below |
| `npm run lint` / `npm run build` | **PASS** — clean |
| Batch sanity: `git diff --name-only origin/main` under `app/public/tiles/` or `api/_data/` | **PASS** — nothing |

Evidence: `integration/in-app-day.jpg`, `integration/in-app-night-glow.png`,
`integration/in-app-fallback-drill.jpg`.

### The re-bake dropped two footprints, and only one of them is mine

`verify-rebake.mjs` reports cell `23_13` going 217 → 215. The second is not a radius that
over-reached:

| Removed | Why |
|---|---|
| 220 m², 9.7 m, at 0.01 m from the exclusion point | this building — correct |
| 565 m², 15.4 m, at 34.60 m | **188 South Park's** exclusion, `exclude: 5`, which its centroid sits 0.06 m from |

`188SouthPark` was merged to `main` as a source-only batch commit
(`0ce3c647 feat: integrate 188 South Park landmark (batch, source-only)`) *after* the last
city re-bake, so `origin/main`'s committed tiles still carry its procedural block. Any full
bake now settles that debt too. This is the batch design working as intended, and it is one
more reason the bake here is discarded rather than committed — `BATCH-INTEGRATE.md` will
bake the whole set once and land both exclusions together.

### Fallback drill

Renamed `app/dist/sf-assets/landmarks/160-south-park.glb`, cold-reloaded:

- the app **booted** and the neighbourhood rendered;
- **exactly one** warning, naming this asset and nothing else:
  `sf-assets: 160-south-park failed to load (fetch for ".../160-south-park.glb" responded with 404: File not found)`;
- zero errors; the other 34 landmarks merged normally;
- the site is **empty ground inside the exclusion zone** — the expected Case B outcome,
  since there is no procedural builder for this id.

Note on the warning text: `INTEGRATION-PROMPT.md` predicts the suffix
"— keeping the code-built landmark". That suffix belongs to the single-shot `warn()` on the
*resident* path (`assets.js:434`). A `loadRadius` entry fails on the streamed path
(`assets.js:560`), which deliberately logs per-asset without the suffix — "each streamed
asset that fails is its own finding". The observed message is the correct one for a
streamed landmark, not a missing case.

### Not done, and why

**Production QA is not run.** `ADDRESS-TO-ASSET.md` stage 5 replaces the integration
prompt's Step 7 with a stop: no push, no PR, no deploy without the owner's explicit
instruction. Local verification is complete and the branch is source-only, ready for
`BATCH-INTEGRATE.md`.

**The local verification used the built `dist/` served statically, not `npm run dev`.** The
five-dev-server cap was fully taken by the parallel South Park sessions. The app under test
is the production build of this branch; the only modification was an rAF shim injected into
the gitignored `dist/index.html`, because the Browser pane does not composite while hidden
and the app drives itself with plain `requestAnimationFrame`. Nothing in the repo was
changed for testing.

## Approval

Granted in advance, 16 August 2026, verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Given with the pipeline invocation (`BUILDING: 160 S Park St`, `BATCH: yes`), so stage 3
was satisfied without a separate round trip. The contact sheet, the aerial day and night
renders and the numbers above were presented at the gate rather than requested at it.
