# Hyatt Regency San Francisco — build report

`artifacts/hyatt-regency/` — stage 2 (BUILD) and stage 4 (OPTIMIZE) of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run 18 August 2026 from
`docs/asset-plans/hyatt-regency.md`.

**What this is:** a stylized miniature of John Portman's 1973 Hyatt Regency at
5 Embarcadero Center — a stepped concrete wedge falling from a full-height fin
wall on Market Street to a two-storey podium on the Embarcadero Center side,
crowned by the Equinox pavilion at the Market/Drumm end.

## Shipped numbers

| | |
|---|---|
| File | `hyatt-regency.glb` (post-optimize, meshopt-compressed) |
| Bytes | 359,236 raw (was 701,304 pre-optimize, -48.8%) |
| Triangles | 13,604 (cap 27,000) |
| Objects / draw submeshes | 6 (was 87) |
| Dimensions | 121.200 x 98.796 x 80.800 m |
| min Z | 0.0000 m |
| XY centre offset | 0.0000, 0.0000 m |
| Loader scale at `targetHeightM` 80.8 | 1.0000 |
| Materials | `Toy_glass`, `Toy_glassl_Glow`, `Toy_gold_Glow`, `Toy_steel`, `Toy_stone`, `Toy_trim` |
| Glow groups | 2 (`Toy_glassl_Glow` podium arcade — hero; `Toy_gold_Glow` Equinox band) |

Stage 4 detail — waste census, phase-by-phase savings, gate results and the
A/B pixel deltas — is in `optimize/REPORT.md`. The numbers above are the
shipped ones: `validation.json` was regenerated from the packed file after the
shipping swap, and all fifteen contract checks PASS on it.

## Dossier corrections made while building

**REPORT beats plan.** Nothing in the plan's §2.1–2.7 was contradicted by the
build, but four things were pinned down or changed:

1. **The step-back is 3.9 m, not 3.0 m.** The plan proposed 15 terraces at
   3.0 m, which ran the wedge only 42 m back and left a 40 m flat podium roof on
   the Embarcadero Center side that the aerial photography does not show. At
   3.9 m the fifteenth terrace lands at v = -41.5, i.e. essentially on the
   north-west site line at the Drumm end, and the section angle becomes ~44 deg
   — which is what the bay-side telephoto shows. The plan's §2.7 rule is
   otherwise unchanged.
2. **The slab is a dark band under a proud pale ring, not a body under a
   fascia.** The plan's phrasing produced a uniformly pale field when seen from
   directly above, because a solid lip plate covers the whole plan. The lip is
   now a RING (`ring_prism`), so from the app's aerial camera the pale tread
   runs 2.6 m back and then the dark band top shows as a reveal. The staircase
   only reads in plan because of this.
3. **The pier rhythm is 4.8 m, not 3.2 m.** 3.2 m centres with 2.15 m piers
   made the Market frontage a pinstripe at city scale. 4.8 m centres with 3.2 m
   piers matches the plaza photography better and reads at thumbnail size
   (style bible §26).
4. **Piers stand 0.6 m proud and bite 0.2 m into the wall behind.** They must
   cross in front of the slab lips — the real precast fins run past the floor
   lines — and they must not float, per `sf3d-offset-handedness`.

## Two bugs worth recording

**The uv->world map is orientation-reversing.** `world(u, v)` rotates the
building axes onto (east, north) through a reflection, so its Jacobian
determinant is -1 and a polygon that is counter-clockwise in uv comes out
CLOCKWISE in world space. The first build wound every face from the uv area
directly: the validator then reported `inverted_solid_objects` for all 89
meshes and a ray residual of **1.0** — 22,500 of 22,500 visible faces flipped.
Fixed by `world_ccw()`, which flips the sign. Nothing else in the model
changed.

**A half-plane clip that grazes a plan corner makes slivers.** The bottom
slab's clip line passed 0.73 m from P4 and left two sub-millimetre edges;
after the bevel those became 4 degenerate triangles and 8 non-unit loop
normals in `slab_lip_00`, which is a whole-asset FAIL. `simplify()` now drops
points within 0.30 m of a neighbour and points within 0.02 m of the line
through their neighbours. This is the same failure mode the optimize prompt
warns about for annulus ngons, arriving from the other direction.

## Orientation

Authored in true-world orientation: Blender `+Y` = true north, `+X` = east.
The Market Street frontage runs **45.8 deg** true and faces 135.8 deg; the
Embarcadero Plaza prow faces 45.8 deg. `placeGeneric()` applies no rotation, so
the asset drops in at its real heading with no `yawDeg`.

The asset contract's "front faces -Y" rule cannot be honoured literally here —
the building's front is Market Street, which faces south-east. Real-world
orientation wins (AGENTS rule 5); recorded here as the deviation.

## Height

Bbox top normalised to **80.8 m exactly**, so `targetHeightM / measuredHeight`
= 1.0000. Eave (wing roof deck) 72.0 m, parapet 73.4 m, crest (Equinox upper
frame) 80.8 m. Sources and the rejection of 77 m and 83 m: `REFERENCE.md` §3.

## Night design

Two glow groups, both matching a non-glow palette neighbour by day:

- **`Toy_glassl_Glow` (6f95b8) — the podium arcade band, 1.4 to 7.2 m, the
  hero.** The world's largest hotel atrium sits behind it and is not modelled;
  the lit base is what says so. By day it reads as a lighter glass than the
  `Toy_glass` window slots above it.
- **`Toy_gold_Glow` (caa64a) — a 0.5 m band under the Equinox upper frame, the
  supporting accent.** By day a warm metal trim line.

No closed glow shells and no stacked alpha (`sf3d-glow-shell-day-alpha`); the
base colour is the night look (`sf3d-glow-colour-is-unlit`).

## Validation

`validation.json` — re-imported from the **shipped, meshopt-packed** GLB into a
fresh isolated Blender scene, all fifteen checks PASS, including
`normals_outward` by per-object signed volume with a 22,500-ray residual of
**0.0000**. Validating the packed file rather than the Blender scene is
deliberate: gltfpack re-emits stored normals, so a sliver manufactured during
optimization is only visible there.

## Approval (gate 3)

Standing approval, given at the top of the run on 18 August 2026 and quoted
verbatim: **"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"**. No per-iteration
approval was sought; the review renders and contact sheet in this directory are
the evidence that would have been presented.

## Draft manifest entry

```json
{
  "id": "hyatt-regency",
  "file": "hyatt-regency.glb",
  "anchor": [-122.3957275, 37.7942899],
  "targetHeightM": 80.8,
  "cat": 7,
  "name": "Hyatt Regency San Francisco",
  "estimated": false,
  "loadRadius": 2500,
  "dims": [121.1997, 98.796, 80.8],
  "tris": 13604
}
```

`loadRadius` = `max(2500, 80.8 * 30)` = **2500 m**, explicit per the contract's
rule 9. Beyond it the site is empty ground (Case B), which at 2.5 km is one
pixel of the Financial District — illegible, which is the test the prompt sets.

---

## Stage 5 — local QA (Case B, batch mode)

Run 19 August 2026 against a local dev server on the re-baked tree.

| Check | Result | Evidence |
|---|---|---|
| Re-validation of the shipped GLB | PASS | all 15 contract checks on the packed file |
| Manifest entry | PASS | 91 entries load, `failed: 0` |
| id mapping | PASS | `camelId('hyatt-regency')` = `hyattRegency`, matches the registry |
| Registry + re-bake | PASS | cell 23_10 49 → 47 footprints |
| audit 1.6 | PASS | `100 zones over 97 landmarks clear` |
| verify-rebake radius | PASS | nearest surviving footprint 40.8 m vs 28 m radius |
| Single building on the site | PASS | no procedural twin, no baked block through the podium, no z-fighting |
| Merge line / scale | PASS | `sf-assets: hyatt-regency merged 6 objects / 6 materials -> batched (7376 tris body); uniform x1.0000 at 3676, -2685` |
| Orientation | PASS | fin wall faces SE onto Market, terraces fall to the NW, prow points NE at the plaza |
| Footprint size vs neighbours | PASS | reads correctly against the Ferry Building and the Embarcadero Center blocks in the wide shot |
| Terrain seating | PASS | podium sits on the ground, no float, no sink |
| Night glow | PASS | only the podium arcade band and the Equinox band light; the rest of the mass stays dark |
| Draw calls | PASS | **87** at the landmark viewpoint (budget 300), 3.09 M triangles |
| Lint / test | PASS | `eslint src test` clean; 26/26 node tests |
| Fallback drill | PASS | see below |

### Fallback drill

`app/public/sf-assets/landmarks/hyatt-regency.glb` renamed away, page reloaded:

- the app booted and the whole area rendered normally;
- **exactly one** warning:
  `sf-assets: hyatt-regency failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)`
  — the dev server hands back index.html for the missing file. Note the text:
  a **streamed** asset (one with `loadRadius`) fails through `scan()`'s catch,
  not through the single-shot loader, so it does NOT say "keeping the code-built
  landmark" as INTEGRATION-PROMPT Step 6 describes. Same guarantee, different
  sentence;
- `stats().failed` was exactly **1**, with the other 70 landmarks still live;
- the site was **empty ground** inside the exclusion zone. That is the expected
  Case B outcome and it is why `loadRadius` is only 2500 m: past that the
  absence has to be illegible, and at 2.5 km this site is one pixel of the
  Financial District.

File restored afterwards; sha256 verified identical to `artifacts/hyatt-regency/hyatt-regency.glb`.

### Batch handoff

Per `ADDRESS-TO-ASSET.md` "Batch mode": the bake was run and used for the QA
above, then **discarded** (`git checkout -- app/public/tiles api/_data`). This
branch carries source only — the GLB, its manifest entry, its
`pipeline/lib/landmarks.mjs` entry, the plan and this artifacts directory. The
city gets rebuilt once for the whole batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

Sanity check, against the **merge base** rather than the branch tip:

```
git diff --name-only origin/main...HEAD   # three dots
  app/public/sf-assets/landmarks/hyatt-regency.glb
  app/public/sf-assets/landmarks_manifest.json
  docs/asset-plans/README.md
  docs/asset-plans/hyatt-regency.md
  pipeline/lib/landmarks.mjs
  (+ artifacts/hyatt-regency/)
files under app/public/tiles/ or api/_data/: 0
```

Three dots matter here. `origin/main` advanced from 335cb9ac1 to 2c14d5f9f
(PR #159) while this session was running, so the two-dot form lists every file
those newer commits touched — 596 tiles among them — and looks alarming. The
merge-base diff is the one that describes what this branch actually adds.

That same moving reference is why the `verify-rebake` reading in the plan's
§2.13 leans on the control experiment rather than on the raw cell counts: the
control (remove the entry, re-bake, compare) isolates the cause regardless of
which commit the reference happens to point at.
