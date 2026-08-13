# 171 South Park Street — build report

Miniature GLB for the SF toy-diorama city, built from
[`docs/asset-plans/171-south-park.md`](../../docs/asset-plans/171-south-park.md)
via `docs/asset-pipeline/ADDRESS-TO-ASSET.md`. Research behind every number is in
[`REFERENCE.md`](./REFERENCE.md).

**Where this report and the plan disagree, this report is correct.**

## 1. What shipped

| | |
|---|---|
| File | `171-south-park.glb` |
| Manifest id | `171-south-park` |
| Anchor (WGS84) | `-122.3945219, 37.7809000` — the footprint's **area centroid** |
| Target height | **12.60 m** (crowning cornice) |
| Dimensions | 19.257 × 18.497 × 12.600 m |
| Triangles | **5,808** (cap 8,000) — 5,816 as built, −8 from the optimize pass |
| Objects | 11 (100 as built; joined per material in stage 4) |
| Materials | 12, all `Toy_*`, flat, no textures, no alpha |
| Glow groups | 2 (`Toy_glass_Glow`, `Toy_trim_Glow`) |
| min Z | 0.000 |
| Validation | **PASS** — all 16 checks on the shipped file, see `validation.json` |
| File size | 155,596 B raw (360,248 B as built, −56.8%) — meshopt-compressed |
| Optimize pass | stage 4 complete, all 8 gates PASS — see [`optimize/REPORT.md`](./optimize/REPORT.md) |

Reproduce with:

```bash
blender -b --python build_171_south_park.py
```

then `render_171_south_park.py` (add `-- --night` for the night render),
`make_contact_sheet.py`, and `validate_171_south_park.py`.

## 2. Corrections to the plan's dossier

The plan required the front elevation to be re-verified before modelling. It was,
from Google Street View pano `tRhqK_-aiVsKi23dOxYSeg`, and that changed several
things. All of these are folded back into the plan file as well.

| Item | Plan (planning stage) | Built (verified) | Why |
|---|---|---|---|
| Front type | angled bay windows expected | **flat front**, every opening flush | Observed. The district record allows either variant for South Park flats; this one has no bays. |
| Storeys | four levels — three flats over a raised ground level | **three**, entry at grade | Observed, and it reconciles the 3-vs-4 permit conflict as a basement count. Floor-to-floor 3.80 m. |
| 12.62 m LiDAR maximum | elevator/stair penthouse (2005 permit) | **the crowning cornice**, raised centre section | Observed: a heavy bracketed cornice with a raised centre, no penthouse visible from the street. 12.62 − 11.41 = 1.21 m fits it. |
| Ornament | not known | **garland friezes at each floor line** + bracketed dentil cornice | Observed. These bands became the building's second identity cue. |
| Entry | on the centre facet, up a stoop, possible garage | **pedimented porch hood on the west facet**, at grade, no garage | Observed. The blue steel gate nearby belongs to 165–167. |
| Body colour | `Toy_sand` cream default | **`Toy_slate` `#a7b3bc`** | Observed light blue-gray clapboard. See §3. |
| Windows per floor | "two pairs on the centre facet, one per outer facet" | one generous pair per facet per floor | An 11.36 m front split three ways only fits one pair per facet honestly. Still *inferred* — a street tree covers the middle of the front. |
| Roof deck colour | "paler than its neighbours" | `Toy_sand` deck, `Toy_roofd` kept for hatch/kerbs | The March 2026 re-roof reads distinctly pale in current satellite imagery. The first render pass used `Toy_roofd` for the deck and the roof read as a dark hole; the pale deck also makes the wedge outline read from above. |
| XY bounding box | ~18.5 × 17.5 m predicted | 19.26 × 18.50 m | The cornice (0.40 m) and rear deck (1.85 m) projections were not in the plan's estimate. |

## 3. Palette extension: `Toy_slate` `#a7b3bc`

The real facade is a light blue-gray. `Toy_steel` (`#9aa0a6`) is the nearest
palette entry but reads neutral-gray and kills the blue that makes this the
coolest-toned building on the oval; `Toy_glassl` (`#6f95b8`) is far too
saturated. `AGENTS.md`'s SF exception — painted residential rows keep their
tinted facades — covers exactly this case, and off-palette is a WARN, not a FAIL
(`sf-asset-check` §7). One custom colour is spent; everything else is on-palette.

Fallback if it ever fights the scene: `Toy_steel`. Do not introduce a second
custom colour.

## 4. Contract deviation: front does not face −Y

The asset contract asks for the front to face −Y. `placeGeneric()` in
`app/src/assets.js` scales and positions but never rotates, so the model must be
authored in true-world orientation, and this building's park front faces **NNW
(343.5° average)**. Real-world orientation wins (AGENTS rule 5). Recorded here as
required by `docs/asset-plans/README.md`.

## 5. Origin is the area centroid, not the bbox centre

The XY bounding-box centre sits at `(-0.125, -1.374)` relative to the origin. That
is **correct and deliberate**: the origin is the footprint's area centroid, which
is the point the loader places at the manifest anchor, and on a wedge the mass is
concentrated at the broad park front. Recentring on the bounding box would push
the building off its own lot — and would also close the integration exclusion
window (see the plan's 2.13). The validator's `origin_at_footprint_area_centroid`
check carries a 2 m budget for this reason instead of the usual 1 m
`centered_xy`.

## 6. Iteration log

1. **First build** — 6,008 tris, geometry and heights correct. First ortho
   elevation render showed every window as a blank cream slab: the trim frame
   panel spans the full opening from depth 0 to 0.09, so it occluded the glazing
   drawn inside its own depth range. Fixed by pushing the glazing **proud** of
   the trim (frame → 0.07, glass → 0.13, glow shell → 0.19), which is how the
   reference implementation does it. 5,816 tris after.
2. **Second build** — roof deck changed from `Toy_roofd` to `Toy_sand`. The dark
   deck read as a hole from the app's downward camera and contradicted the
   March 2026 re-roof, which is the palest roof on the block in current imagery.
   Kerbs and hatch stay `Toy_roofd` so they read as objects on a pale deck.
3. **Validation** — all-PASS on the re-imported GLB, first run, no conform pass
   needed.
4. **Stage 4 optimize** — 100 objects joined to 11, 11,804 verts welded to 3,104,
   meshopt-packed. 360,248 → 155,596 B (−56.8%). Worst A/B pixel delta 0.050%
   against a 2%/4% budget. The shipped GLB re-passes all 16 stage-2 contract
   checks. Details in `optimize/REPORT.md`.

## 7. Night state

Hero glow: a scatter of lit windows — one on the centre facet's middle floor, one
on the east facet's top floor, one on the tail. Three flats, not an office, so
most windows stay dark. Supporting accent: a lamp under the entry hood. The
friezes and cornice do **not** glow (daylight identity, not signage); the
skylights do not glow either (a lit skylight on a residential roof reads as a
studio). Glow shells are thin panels proud of the opaque glazing, as the app's
~12%-alpha day layer requires.

## 8. Draft manifest entry

`dims` and `tris` are the measured values from `validation.json`.

```json
{
  "id": "171-south-park",
  "file": "171-south-park.glb",
  "anchor": [
    -122.3945219,
    37.7809
  ],
  "targetHeightM": 12.6,
  "cat": 2,
  "name": "171 South Park Street",
  "estimated": false,
  "dims": [
    19.257,
    18.497,
    12.6
  ],
  "tris": 5808,
  "loadRadius": 2500
}
```

Integration is a separate job — see the plan's 2.13, in particular the exclusion
window (`0.59 m < exclude < 3.83 m`, use `exclude: 2`), which is the tightest in
the registry and whose failure mode is the silent deletion of two neighbouring
historic contributors from the baked city.

## 9. Stage 5 — integration (batch mode)

Integrated locally on `pipeline/171-south-park`. **Source only**: the Case B bake was
run and QA'd, then discarded. 594 generated files under `app/public/tiles/` and
`api/_data/` were dirty and are not in the commit — a re-bake rewrites ~600 files
whatever landmark triggered it, so committing them would make this branch unmergeable
with its siblings. `git diff --name-only origin/main` lists nothing generated.

### The bake

`pipeline/data/` was seeded as an APFS clone from a sibling worktree (raw downloads
only, never `pipeline/out/`), which is why the bake reproduced `origin/main` exactly
except for this landmark's own cell. `verify-rebake.mjs --out`:

```
584 of 585 cells unchanged
23_13    233 -> 232  <- 171SouthPark
ok   171SouthPark   3.8 m vs 2 m radius  (nearest is 9.9 m tall)
PASS  only the new landmarks' cells moved, and every asset has clear ground under it
```

Exactly one footprint removed. Both party-wall neighbours survive, and the nearest
surviving footprint sits at 3.8 m — matching the 3.83 m predicted for 165–167 South
Park from the DataSF rings before any bake ran.

`audit.mjs` check **1.6 PASS** — "no procedural footprint inside a bespoke landmark
exclusion zone — 42 landmarks clear". The audit's three failures (1.2b, 1.3c, 1.7b)
are pre-existing baseline failures of the data sources: identical on four sibling
worktrees, and none of them concerns landmarks or exclusion zones.

**A duplicate `171SouthPark` registry entry was found and removed** during this stage
(same id, coords and exclusion; different camera preset). Harmless for the exclusion,
but it would have emitted two identically-named presets into `landmarks.json` and two
rows from `context.mjs`. The whole registry was checked for other duplicate ids —
none.

### Local QA

| Check | Result |
|---|---|
| Loader merge line | `sf-assets: 171-south-park merged 12 objects / 12 materials -> batched (3085 tris body); uniform x1.0000 at 3782, -1205` |
| Scale | **x1.0000** — authored height and `targetHeightM` agree exactly |
| Batching | `batched` — joins the shared BatchedMesh pair, so it adds **no new draw calls** |
| One building on the lot | PASS — no procedural twin, no z-fighting, no baked block poking through |
| Footprint vs neighbours | PASS — reads as a small wedge at the correct scale among its SoMa neighbours |
| Orientation | PASS — the three-facet front faces the oval, the tail runs back into the block |
| Terrain seating | PASS — no floating, no sinking |
| Camera preset | PASS — `yaw: 197` frames the NNW park front, as derived |
| Search / context | PASS — the context tier emits exactly one row, `landmark:171SouthPark` at (3781.9, −1204.9) = the anchor, in both `out/context/landmarks.json` and `out/context/search-index.json`. Verified from the bake output, not from a live `SF.search()` call: the running page serves the committed tiles, and the bake was discarded per batch mode, so the live index has no row yet |
| Night state | PASS — only the intended glow shells light; friezes, cornice and skylights stay dark |
| Fallback drill | PASS on the observable assertions — see the note below for what was and was not seen |
| Draw calls | **PASS — 85** at street level over South Park, 89 downtown, 88 in the Mission, against the < 300 budget (AGENTS rule 2) |
| fps | **NOT MEASURED** — see below |

**Draw calls were measured; fps was not.** The QA browser pane only composites while
a screenshot is being taken, so `requestAnimationFrame` never runs freely: a 180-frame
probe captured 0 frames, and the in-app stats overlay consequently read
`fps 0 / draw calls 1`, which is stale rather than real. Draw calls were therefore
taken out of band, by disabling `renderer.info.autoReset` and driving explicit
`renderer.render(scene, camera)` calls, which gives a true per-frame count:

| Camera | draw calls | triangles |
|---|---|---|
| South Park, street level over the landmark | **85** | 6.44 M |
| Downtown (the stress cell) | **89** | 6.64 M |
| Mission (the stress cell) | **88** | 6.96 M |

All far inside the < 300 budget, and consistent with the structural expectation: the
asset reports `batched`, so it renders out of the existing shared BatchedMesh pair and
adds no draw calls of its own.

**fps remains unmeasured** — it cannot be sampled in a pane whose render loop is
suspended, and the second browser was not connected. A frame-rate reading at street
level in a visible browser is still outstanding, and production QA has to cover it.

**What the fallback drill did and did not show.** Two attempts were spoiled by
caching: moving the GLB aside, and then replacing it with 4 KB of noise, both still
merged successfully because the browser served the previously-fetched bytes from its
in-tab memory cache. The drill was made deterministic by pointing the manifest's
`file` field at a filename that had never been fetched (`171-south-park-MISSING-drill.glb`,
which Vite answers with the SPA HTML fallback), reloading, and approaching the site.
Observed then: `SF.assets.stats()` moved from `failed: 0` to **`failed: 1`**,
`171SouthPark` was **absent** from `SF.assets.placed` while the other 29 landmarks
stayed live, the app booted and the area rendered normally, and the site showed
**empty ground** inside the exclusion zone — the documented Case B expectation. The
manifest and the GLB were restored afterwards and the GLB re-verified byte-identical
to `artifacts/`.

The "exactly one console warning" half of the drill was **not observed directly** —
the console hook installed via the automation bridge captured nothing on a freshly
reloaded page, including the app's own merge lines, so absence of captured warnings
proves nothing either way. It rests on the source instead: `warn()` in
`app/src/assets.js:359-363` is latched by a `warned` boolean and can fire at most once
per session. That is an inspection, not a measurement, and is recorded as such.

One number worth not misreading: the loader's "3085 tris body" is a vertex-derived
estimate (`position.count / 3`) that under-reports on indexed geometry, which
meshopt produces. The shipped file is 5,808 triangles (5,664 body + 144 glow) and the
loader's 12 objects / 12 materials match the file exactly, so nothing is missing. The
same under-report shows on known-good assets — `380-brannan` reports 4,496 against a
manifest of 7,760.

## 10. Approval

**Approved 13 August 2026.** Presented at the stage-3 gate (contact sheet, aerial
day and night, and the numbers above, together with the two judgement calls in §3
and §5 and the integration hazard in §8). David's reply, verbatim:

> proceed

That advances the pipeline to stage 4 (optimize) and stage 5 (integrate, batch
mode).
