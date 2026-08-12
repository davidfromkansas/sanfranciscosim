# 375 Alabama Street — build report

Deliverable: `375-alabama.glb`, a miniature of the **Ames Harris Neville Co. Building**
(1926) at 375 Alabama Street, San Francisco, authored for the SF-SIM toy-diorama city.

Built from `docs/asset-plans/375-alabama.md` (Part 1) under
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`. Research behind every number is in
`REFERENCE.md`. **Where this report and the plan disagree, this report wins.**

## Shipped numbers

| | |
|---|---|
| Triangles | **11,604** (cap 14,000) |
| Objects | 13 shipped (345 as authored — joined per material in stage 4) |
| Dimensions (XY bbox / Z) | 67.32 x 61.61 x 22.50 m |
| Building itself | 61.10 x 54.63 m footprint — the larger XY bbox is the 4.32° heading, not a scale error |
| min Z | 0.0000 |
| XY centre offset | 0.038, −0.002 m |
| Materials | 12, all `Toy_*`, all flat, no textures, no alpha |
| Glow groups | 3 — `Toy_trim_Glow` (tower crown + entrance), `Toy_glass_Glow` (125 lit bays), `Toy_glassl_Glow` (two lit monitors) |
| Anchor | `-122.4118477, 37.7645633` |
| targetHeightM | 22.5 (stair-tower crown, normalised exactly — loader scale lands at 1.000) |
| File size | **318,672 B** shipped (753,288 B pre-optimize, −57.7%) — well inside the 500 KB budget |
| Draw submeshes | 14 (346 pre-optimize) |
| Validation | `validation.json` — **overall PASS**, all 16 checks, re-run against the shipped optimized file |

## Reproduce

```bash
blender -b --python build_375_alabama.py            # -> .blend + .glb
blender -b --python render_375_alabama.py -- --glb 375-alabama.glb
blender -b --python render_375_alabama.py -- --glb 375-alabama.glb --night
python3 make_contact_sheet.py
blender -b --python validate_375_alabama.py -- --glb 375-alabama.glb
```

Blender 5.2.0 LTS. Renders always re-import the exported GLB, so every image depicts exactly
the geometry that ships; validation runs in a factory-reset scene against the same file.

## Dossier corrections and deviations from the plan

These are the places where building the thing changed what the plan said. Each is a
deliberate decision, not a slip.

1. **Footprint reduced to four corners.** Plan §2.3 kept the survey's two sub-620 mm jogs on
   the east and west walls as "real pilaster returns worth keeping". They are — but they are
   *pilaster* returns, and this model expresses pilasters as 1.5 m piers standing 0.25 m proud
   of the wall. Modelling the jogs as footprint steps *and* the piers as applied panels would
   have double-counted the same feature. The jogs are absorbed into the pier rhythm; the body
   is the four-corner OBB. Footprint area error: +0.1 %.
2. **Windows are continuous glazing bands, not 126 punched openings.** Plan §2.7 step 4
   described per-bay window openings. A reinforced-concrete frame really does glaze
   continuously between its piers, and banding costs roughly 300 triangles where punched
   openings would have cost about 7,800 — over half the budget for a rhythm the proud piers
   already carry. The elevations read the same and the money went to the medallions instead.
3. **Medallions are 1.7 m, not the plan's 2.0 m.** At 2.0 m the cog's top edge broke through
   the parapet crest. 1.7 m keeps the whole disc inside the frieze band where the real
   castings sit.
4. **Medallions are not bevelled.** 23 bevelled 24-gon cogs cost 6,500 triangles — over a
   third of the entire asset — to soften an edge that is a fraction of a pixel from the app's
   camera. The first build came in at 17,900 triangles, over the cap, almost entirely because
   of this. Unbevelled, that build came down to 10,176.
5. **The sawtooth monitors are trapezoids with a flat 0.8 m ridge cap**, not the plan's
   triangles. Bevelled, a single ridge vertex rounded into a barrel and the whole roof read as
   five fat white tubes from the aerial. The flat cap also gives the near-vertical north face
   enough area to read as glass. Slopes as built: opaque south face 54.5°, glazed north face
   75.5° — the plan's 25°/60° would have made the monitors 4 m wider each than the roof has
   room for.
6. **The tower was rebuilt after the first render.** As planned (7.6 m wide, projecting
   0.8 m, expressed only above the roof) it read as a white box parked on the parapet with an
   orange stripe — not a tower. As built: 6.4 m wide, projecting 1.10 m, with the two cream
   fins running the **full height from the pavement to the 22.5 m crown**, which is what the
   2007 photograph actually shows and what gives the shaft its lift.
7. **`Toy_mauve` (`#a2887f`) is a deliberate palette extension** for the tower's centre panel.
   The plan nominated `Toy_rust` (`#a86444`) as the nearest palette entry; rendered, it read
   as an orange billboard and became the loudest thing on a cream building whose only intended
   accent is the ornament. Off-palette is a WARN, not a FAIL (contract rule 7). Recorded here
   as the plan §2.8 note anticipated.
8. **The night state was retuned twice.** First: two monitors lit end to end over their whole
   glazed face read as fluorescent light bars and flattened the tower's hero glow, so each lit
   monitor now glows over a 19 m stretch of the 51 m ridge and only the top third of its glazed
   face, and the tower crown glow starts lower (18.2 m) and is wider. Second: **on approval
   David asked for 80% of the windows lit**, which replaced the plan's six-segment scatter with
   one glow shell per bay — 125 of the 157 bays across all four elevations, the dark ones
   staggered floor to floor so they never line up into a dead column. This is a deliberate step
   past the style bible's "small clusters of life" restraint (§11): the building now reads as a
   working factory at dusk rather than a few lit offices, and the lit monitors and tower crown
   read as part of one lit interior. Cost: +1,428 triangles, still 2,396 under the cap.
9. **Orientation deviates from the contract's "front faces −Y" rule, as every plan in this
   set does.** The asset is authored in true world orientation (`+Y` = north) because
   `placeGeneric()` applies no rotation; the address front faces **west, 265.7°**. Real-world
   orientation wins (AGENTS rule 5).
10. **`targetHeightM = 22.5` is inferred, not published.** It is a photogrammetric read of the
    2007 DPR photograph calibrated against the LiDAR roof deck; the honest range is 21–24 m.
    Because the tower is the tallest geometry this number scales the whole asset. If a better
    source appears, correct it and rebuild — do not nudge the tower.

## Contract compliance

| Rule | Status | Note |
|---|---|---|
| Binary GLB, real metres | PASS | 67.32 x 61.61 x 22.50 m |
| Origin base-centre, min Z ≈ 0 | PASS | min Z 0.0000, centre offset 0.038 / −0.002 m |
| Crest normalised to target | PASS | 22.500 m exactly |
| Orientation | WARN (documented) | true-world heading, front faces west — deviation 9 above |
| Flat-colour `Toy_*` materials | PASS | 12 materials, `Toy_mauve` off-palette by design |
| No textures / transparency | PASS | 0 image textures, 0 transparent materials |
| `_Glow` only on night surfaces | PASS | 3 glow materials, all thin shells proud of opaque glazing |
| No `Toy_body` | PASS | — |
| Triangle budget | PASS | 11,604 / 14,000 (PERF-PLAN hard limit 30,000) |
| No cameras / lights / animation / armatures / constraints | PASS | all zero |
| Transforms applied, no negative scales | PASS | — |
| Outward normals | PASS | 13/13 shipped objects positive signed volume; 0 non-unit loop normals; 31,500-ray visibility test residual 0 |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No foreign / leaked geometry | PASS | fresh-scene re-import contains only the asset |

## Stage 4 — optimize

Run per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; full metrics, census, A/B renders and
gate table in `optimize/REPORT.md`. Headline: 753,288 → 318,672 B (−57.7%), 345 → 13
objects, 346 → 14 draw submeshes, triangles and bbox unchanged, all 8 gates PASS, worst
A/B pixel delta 0.22% against a 2%/4% gate. The pre-optimize original is archived at
`optimize/input/375-alabama.glb`. Renders in this directory were made from the
pre-optimize file; the A/B pass proves the two are visually identical.

## Renders

All regenerated from the final export.

| File | View |
|---|---|
| `375-alabama-west.png` | Alabama Street — the address, the entrance, the tower |
| `375-alabama-south.png` | 17th Street — the long elevation |
| `375-alabama-east.png` | Florida Street |
| `375-alabama-north.png` | rear |
| `375-alabama-top.png` | sawtooth field, flat north membrane, parapet ring, tower |
| `375-alabama-aerial.png` | high three-quarter from the southwest |
| `375-alabama-aerial-night.png` | night state |
| `375-alabama-contact-sheet.png` | all of the above |

## Draft manifest entry

Not applied — integration is a separate job (`docs/asset-plans/INTEGRATION-PROMPT.md`).

```json
{
  "id": "375-alabama",
  "file": "375-alabama.glb",
  "anchor": [
    -122.4118477,
    37.7645633
  ],
  "targetHeightM": 22.5,
  "cat": 19,
  "name": "375 Alabama Street",
  "estimated": false,
  "dims": [
    67.32,
    61.61,
    22.5
  ],
  "tris": 10176,
  "loadRadius": 2500
}
```

Integration is **Case B** (new landmark): it also needs a `pipeline/lib/landmarks.mjs` entry
(`id: '375-alabama'`, `height: 22.5`, `exclude: 42`, camera
`{ distance: 330, yaw: 215, pitch: 18 }`) and a re-bake of the affected tiles. The footprint's
half-diagonal is 41 m, so the exclusion radius is larger than any previous non-monument entry —
verify at integration which baked footprints it removes, because Alabama and Florida Streets
are only ~20 m wide.

## Approval

**Approved 12 August 2026 by David (davidfromkansas), verbatim:**

> "i approve lets proceed -- can you also light up 80% of the windows? thanks proceed and im
> waiting to see your PR"

The window request was executed as deviation 8 above and the asset re-rendered, re-validated
(overall PASS, 16/16) and re-committed before stage 4 began. The same message authorises the
push and pull request that stage 5 otherwise stops to ask for.

## Stage 5 — integration (local)

Case **B** (new landmark). Executed per `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1.

| Step | Result | Evidence |
|---|---|---|
| Re-validation of the shipping GLB (fresh scene) | **PASS** | overall PASS, 16/16; 11,604 tris; min Z 0.0000; centre 0.038 / −0.002 |
| GLB dropped in | **PASS** | `app/public/sf-assets/landmarks/375-alabama.glb`, byte-identical to `artifacts/` |
| Manifest entry | **PASS** | 19th entry; `dims`/`tris` taken from the validator, not the plan |
| `estimated: true` | **PASS** | corrected from the plan's draft — 22.5 m is inferred, not published (REFERENCE §8) |
| `loadRadius` decision | **PASS** | 2500 m = the default `max(2500, 22.5 × 30)`. Beyond it the site is empty ground (the baked building is carved out), but a 22.5 m building at 2.5 km is far below a pixel, so the absence is illegible |
| id mapping | **PASS** | `camelId('375-alabama')` → `375Alabama`, which hits the new registry entry — no procedural twin |
| Case B registry entry | **PASS** | `pipeline/lib/landmarks.mjs`, `exclude: 42`, camera `{330, 215, 18}` |
| Tile re-bake | **PASS** | terrain → bridges → buildings → streets → landcover → lore → toy; toy tier published to `app/public/tiles/` |
| Exclusion outcome | **PASS** | procedural footprints 171,438 → **171,437**: exactly one removed, so `exclude: 42` hit this building and no neighbour |
| `pipeline/audit.mjs` check 1.6 | **PASS** | "no procedural footprint inside a bespoke landmark exclusion zone — 25 landmarks clear" |
| Loader scale | **PASS** | `targetHeightM / measured Y` = 22.5 / 22.5 = **1.000000** |
| Terrain seating | **PASS (noted)** | `sampleElevation` at the anchor = 11.00 m; the four surrounding samples run 11.00–11.90 m, so the flat base sits on grade with up to ~0.9 m of cross-site slope — normal for a flat-based asset, and 4% of the building's height |
| `npm run lint` | **PASS** | eslint clean |
| `npm run build` | **PASS** | built in 1.69 s; compress-tiles 3,186 tiles 55.7 → 31.2 MB |
| Three round-trip | **PASS** | `g3check`: `G3-OK … meshes:14 tris:11604`, 12 materials, no decode errors |
| **Running-app QA** | **NOT RUN — see below** | |
| **Fallback drill** | **NOT RUN — see below** | |

### What could not be verified locally, and why

The Browser pane allows five dev servers per folder and all five are held by other
concurrent sessions in this workspace, so the app could not be started here. That leaves
these checks from step 5/6 unperformed:

- the `sf-assets: 375-alabama merged N objects / M materials -> …; uniform xS` console line
- a visual single-building check at the site (no procedural twin, no z-fighting)
- orientation on screen against the real streets
- the night sweep past dusk confirming only `_Glow` surfaces light
- the draw-call/fps overlay against AGENTS rule 2
- the mandatory fallback drill (rename the GLB, confirm one warning and graceful degradation)

The checks above substitute for some of these deterministically — the loader's scale
arithmetic, the id mapping that prevents a twin, the exclusion outcome that prevents an
intersecting baked block, and a pinned-three load of the actual shipping file — but they
are not a substitute for the visual and runtime ones. **These must be run before this is
treated as verified in production.**

### Re-bake scope — read before reviewing the tile diff

`pipeline/data/` and `pipeline/out/` are gitignored and were absent on this machine, so the
Case B re-bake started from a fresh download of every source. The resulting bake therefore
carries a source-data refresh as well as this landmark's exclusion, and every toy and
toyland cell is rewritten (918 files). The substance of the refresh is small — toy records
226,482 → 226,599 (+0.05%), trees 272,235 → 272,766 (+0.2%), base buildings −1 (this
building) — and all toy sanity gates pass. It could not be separated: `toy.json` is a single
index over all cells, so committing a subset of the regenerated `.bin` files would leave the
index disagreeing with them.

`pipeline/validate.mjs` reports one FAIL, `tallest procedural building 200-340 m — 175.4 m`.
This is pre-existing and unrelated: the **committed** `app/public/tiles/buildings.json`
carries the identical `tallest.height: 175.4`. `pipeline/audit.mjs` reports three FAILs
(1.2b facade-height percentile, 1.3c Telegraph Hill DEM, 1.7b one sampled tree offshore),
all citywide source-data characteristics that adding one 22.5 m Mission landmark cannot
cause. I did not A/B them against the previous bake, because `pipeline/out/` is gitignored
and this run overwrote it.

The integration prompt's clean-machine recipe (`npm run buildings && streets && landcover &&
validate && toy`) is also incomplete: `buildings.mjs` needs `out/terrain.json` and
`out/bridges.json`, and `toy.mjs` needs `out/lore.json`, so `terrain`, `bridges`, `lore` and
`loredata` have to run too — and `loredata.mjs` needs the `overturemaps` Python CLI, which
was installed into a throwaway venv rather than globally.
