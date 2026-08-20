# 246 Ritch Street — build report

Asset: `artifacts/246-ritch/246-ritch.glb`
Plan: `docs/asset-plans/246-ritch.md`
Dossier: `artifacts/246-ritch/REFERENCE.md` — **REFERENCE beats the plan**
Built: 18 August 2026, Blender 5.2.0 LTS, headless.

---

## 1. Numbers

| | Measured (fresh re-import of the shipped GLB) | Contract |
|---|---|---|
| Triangles | **8,492** shipped (8,496 pre-optimize) | cap 9,000 (plan §2.11); landmark limit 27,000 |
| Objects | 11 (joined by material) | — |
| File | **248,928 bytes** meshopt-packed (509,272 authored, −51.1%) | ≤ 500 KB |
| Dimensions | **28.368 x 28.156 x 18.760 m** | XY bbox ~27.9 expected from the 45° heading |
| Building | 16.68 m frontage x 22.70 m deep | measured, OSM way/1174904714 |
| min Z | 0.0000 | ≤ 0.5 m |
| XY centre offset | (0.095, 0.100) m | ≤ 1.0 m |
| Crest | **18.760 m** exactly | = `targetHeightM`, so the loader scale is 1.0 |
| Parapet | 15.87 m | DataSF LiDAR median |
| Materials | 10, all `Toy_*`, flat, no textures, no alpha | — |
| Glow materials | `Toy_glass_Glow`, `Toy_trim_Glow` | — |
| Normals | signed-volume clean on all 11 objects; ray residual **0.0%** | ≤ 0.15% |
| Degenerate triangles | 0 | 0 |

`validation.json` — **overall PASS**, all 16 checks.

## 2. Anchor, orientation and height

- **Anchor** `-122.3958481, 37.7802253` — the OSM oriented-bounding-box centre; the area
  centroid agrees to 1 cm.
- **Front heading 45.0°** (north-east, Ritch Street). Authored in true-world orientation
  (Blender `+Y` = north), as `docs/asset-plans/README.md` requires — the contract's
  "front faces −Y" can only be honoured literally by a south-facing building, and real-world
  orientation wins (AGENTS rule 5). **Recorded here as the deviation.**
- **Height 18.76 m** to the roof stair/elevator penthouse (DataSF LiDAR `hgt_maxcm`), parapet
  **15.87 m** (`hgt_median_m`). Cross-checks: the 2009 entitlement's "five-story, 50-foot-tall"
  = 15.24 m to the roof, and an independent photogrammetric reprojection of Street View pano
  `1EVAdp1_sD5des1l6a3eeQ` putting the parapet at 15.0 ± 1.0 m. Three sources, two of them
  independent of the LiDAR, all inside 0.9 m.
- **Floor structure** 3.40 m ground + 4 × 3.115 m = 15.87 m exactly. The unit numbering in
  DataSF (`#101`, `#201–205`, `#301–305`, `#401–404`, `#501–504`) is what fixes five storeys.

## 3. Dossier corrections and decisions

The plan and this build were authored in the same session, so there are no inherited errors.
The plan's §2.15 listed six open questions; this is what the build did about each.

1. **The 18.76 m crest is a penthouse — built as one.** Attribution, not observation: the 2026
   nadir aerial shows a raised light block near the roof centre casting a shadow; a five-storey
   19-unit building has an elevator and an overrun; 2.9 m above the roof is exactly a bulkhead.
   Ruled out as vegetation — `peak_1st_m` (23.96) − `gnd_min_m` (4.85) = 19.11 m, within 0.35 m
   of `hgt_max`, so nothing overhangs this footprint.
2. **The ~13% of the LiDAR ring at ~4.5 m is NOT modelled as a step.** OSM (378.5 m²) and the
   surveyed lot (383.7 m²) agree with each other against the LiDAR ring (395.4 m²); the build
   uses the OSM rectangle. Modelling a rear step to explain a raster statistic would be
   inventing geometry.
3. **No rear balconies.** The nadir aerial's second row of dark rectangles on the south-west
   edge is unconfirmed and the rear is not photographable from any street. Windows only.
4. **Nine balconies, floors 2–4, three per floor, each floor skipping a different bay**
   (floor 2 skips bay 3, floor 3 skips bay 2, floor 4 skips bay 1, counting from the garage
   end). Floor 5 is flush. This is the metric reprojection's reading; the right ~2 m of the
   frontage is behind a tree in every capture and is the residual uncertainty.
5. **No architect named** — two names recur in permit-agent aggregations with no primary source.
6. **No unobstructed facade photograph exists after ~2019**; everything comes from the
   2015–2019 historical panoramas.

## 4. Design decisions

**Palette extension.** One: `Toy_slate` at **`#5d646d`**, for the charcoal recessed window bays,
the lightwell and the front-elevation recesses. A WARN, not a FAIL, with precedent in `380-brannan` and
`181-south-park` (the repo carries three different `Toy_slate` values; this asset picks its own
and states it here). `Toy_roofd` merges with the near-black balconies and kills the patchwork;
`Toy_steel` is too light for the recesses to read as recesses.

**`Toy_roofd` is kept to small dark props only** — the parapet coping band, the balcony screen
caps, the penthouse fascia, the roof hatch and the mechanical plinth. The roof membrane is
`Toy_steel`: `Toy_roofd` measured rgb(9,9,12) in the running app on a `92-south-park` roof deck,
below what the diorama's ambient can lift, while `Toy_steel` on the same asset read
rgb(94,103,112).

**The ground-floor base band is applied, not projecting.** Every opening layer (garage leaf,
lobby reveal, shopfront frame and their fills) is dimensioned to stand proud of `BASE_D`, so no
frame can land in the band's outer plane and z-fight.

**Glow is restrained and shell-thin.** Hero: the restaurant and lobby as a low warm band inside
the dark base — the inverse of the daytime plinth, and what this building actually looks like at
night at the bottom of a dark alley. Supporting: six lit windows out of twenty on the front.
Each glow shell covers only the lower ~60% of its opening and stands proud of the opaque
glazing, because the app draws `_Glow` in a separate layer at ~12% alpha **per layer** and a
closed shell crosses two, reading at ~23%.

**Iteration log (four passes):**

1. *Pass 1.* The charcoal bays were invisible — the window frame covered the recess panel, so
   recognition cue 4 (the cream/charcoal patchwork) did not exist. The balconies read as thin
   shelves. The roof's penthouse sat directly in front of the lightwell from the app's
   north-east camera and the two merged into one confused frame-and-tab shape.
2. *Pass 2.* Recess panels widened to 3.10 m with a ~0.5 m charcoal border all round the window;
   balconies to 2.95 m wide with a 1.28 m screen projecting 1.05 m; the hero shopfront glow shell
   cut to a low band. Roof recomposed as one long dark bar with the penthouse at one end.
3. *Pass 3.* Penthouse moved clear of the lightwell in plan so neither occludes the other;
   floor-2 balconies lifted 0.22 m off the base band (the photographs show wall between them);
   the top-floor recess shortened so it stops clear of the coping instead of poking into it;
   penthouse cap moved to `Toy_slate` so the block still reads in plan view, where a `Toy_steel`
   cap was the same value as the membrane and vanished.

4. *Pass 4, after the first full Cycles rig.* The charcoal base band was wrapped round all four
   elevations and put a black bar across both party walls — surfaces buried against 7.95 m and
   10.75 m neighbours in the city, so never seen there, but the studio elevations showed a
   building with a plinth on all four sides. Restricted to the front and the rear. And in plan
   view the `Toy_slate` penthouse cap was a second dark rectangle beside the lightwell and the
   two read as one shape; the cap moved to `Toy_trim` so the penthouse is a light block inside
   its dark `Toy_roofd` fascia, which is also what the real one looks like from above.

Passes 1–4 were judged on the high three-quarter aerial first, as the pipeline requires.
Passes 2 and 3 used a Workbench preview (7 s vs ~2 min per frame): this Mac was running a dozen
parallel Blender sessions at load 270+, and Workbench reads `material.diffuse_color`, which the
build script sets. Composition and proportion only — the palette was judged from Cycles.

## 5. Scope

**In the GLB:** the stucco body; the parapet and its dark coping band; the Ritch Street elevation
with nine balconies, sixteen recessed bays and their windows; the charcoal base band with the
garage door, the recessed lobby, the restaurant shopfront and the "246" numerals; the south-east
flank's punched rank above the neighbour's roofline; the rear elevation's windows; the blind
north-west party wall; the roof membrane, penthouse, lightwell and mechanical cluster.

**Not in the GLB:** Ritch Street, the three street trees, 248–250 / 252–254 / 230–236 Ritch, the
Zoe Street buildings, the rear yard, the sidewalk, the restaurant's awning and seating, the
fire-department connection, vehicles, people, plinths, cameras or lights.

## 6. Draft manifest entry

```json
{
  "id": "246-ritch",
  "file": "246-ritch.glb",
  "anchor": [
    -122.3958481,
    37.7802253
  ],
  "targetHeightM": 18.76,
  "cat": 2,
  "name": "246 Ritch Street",
  "estimated": false,
  "dims": [
    28.3678,
    28.1556,
    18.76
  ],
  "tris": 8492,
  "loadRadius": 2500
}
```

`camelId()` maps `246-ritch` → `246Ritch`; digits do not start a segment. The
`pipeline/lib/landmarks.mjs` entry must use exactly that id or the procedural block is never
hidden and there is no warning.

## 6a. Stage 4 — optimize

`gltfpack@0.24 -c -km -kn -noq` applied directly to the authored GLB: **509,272 → 248,928 bytes,
−51.1%**, 8,496 → 8,492 triangles (four degenerates dropped), identical bbox, identical material
set, worst A/B pixel delta 0.0019%. Phase B measured as a net regression and reverted in full —
the build script already joins per material, so the pass had nothing left to do and every
Blender round-trip cost ~9 KB. Full four-variant table, census and gate results in
`optimize/REPORT.md`. The pre-optimize original is archived at `optimize/input/246-ritch.glb`.

## 6b. Stage 5 — integration and local QA

Case **B**. Registry entry `246Ritch` (`camelId('246-ritch')`, verified), `exclude: 5.3`,
`camera: { distance: 130, yaw: 135, pitch: 26 }`. Manifest entry appended as text
(+19 lines, 0 deletions). `loadRadius` 2500 — the default `max(2500, 18.76 × 30)`.
`pipeline/compress-assets.mjs` skips the file: it is already meshopt-compressed from stage 4.

**The re-bake was mandatory here, not a formality.** The procedural block on this parcel baked
to a `topY` of **22.6 m** absolute — `datasfHeight()` takes the midpoint of the LiDAR median and
maximum (17.32 m) and adds ~5.3 m of terrain — against this asset's 21.2 m parapet. The
procedural version is **taller than the asset**, so an unbaked check would have shown nothing
wrong with a building that was in fact entirely buried.

| Check | Result |
|---|---|
| `pipeline/audit.mjs` 1.6 — no procedural footprint inside a landmark exclusion zone | **PASS** — 100 zones over 97 landmarks clear. (1.2b, 1.3c and 1.7b fail on `origin/main` too and are unrelated) |
| `pipeline/verify-rebake.mjs` | **PASS** — 584 of 585 cells unchanged; `23_13` 182 → 181; nearest surviving footprint 11.1 m vs the 5.3 m radius |
| Tile penetration test (decoded `buildings/23_13.bin` and `toy/23_13.bin`, point-in-polygon against the real footprint) | **PASS** — the 386 m² / 22.6 m block whose centroid sat 1.5 m from the anchor is gone from both tiers. The only ring still touching the rectangle is 230/236 Ritch (`SF3776144`) with **one vertex 0.97 m inside** — the shared party-wall corner, present identically **before** the re-bake, and unfixable without deleting a real standing building (AGENTS rule 5) |
| Loader merge line | `sf-assets: 246-ritch merged 12 objects / 10 materials -> batched (5841 tris body); **uniform x1.0000** at 3665, -1130` |
| Scale | **1.0000** — authored crest and `targetHeightM` agree exactly |
| Exactly one building, no procedural twin, no z-fighting | **PASS** (screenshot + tile test) |
| Terrain seating | **PASS** — no floating, no sinking |
| Orientation | **PASS** — the balcony front faces Ritch Street; the camera preset (yaw 135) looks square onto it |
| Night | **PASS** — six lit windows and the warm restaurant/lobby band at the base; balconies, parapet, penthouse and roof stay dark |
| Draw calls | **55–94** across the QA runs, against the 300 iron-rule cap |
| Fallback drill | **PASS** — GLB moved aside: the app boots, the area renders, exactly one warning (`246-ritch failed to load (… 404)`), and the site is empty ground inside the exclusion zone, which is the documented Case B expectation. File restored |

**One finding that is not about this asset.** On `origin/main` the shared landmark
`BatchedMesh` reserve is exhausted, and 246 Ritch is the landmark that tips it over:

```
landmark-bodies:  maxVerts 1,200,000 (origin/main)   nextVert 1,204,928   geoms 84
```

With 84 landmarks live in the SoMa/South Park cluster the batch needs **1,204,928** vertices
against a 1,200,000 reserve — a deficit of **4,928**, about 0.4%. The first QA run therefore
logged `sf-assets: 246-ritch failed to load (THREE.BatchedMesh: Reserved space request exceeds
the maximum buffer size.)` and the asset was fine. Raising `BODY_VERTS` / `BODY_INDICES` in
`app/src/assets.js` to 2,000,000 / 6,000,000 made every check above pass with `failed: 0`; the
change was **reverted before committing**, because a landmark branch must not carry an
`app/src/assets.js` change and the reserve is a GPU-memory decision for the owner (1.2M → 2.0M
verts is roughly 43 → 72 MB for positions+normals+colours, plus 14 → 24 MB of indices).

**Batch mode.** `248-ritch` and `254-ritch` are in flight on the two lots south-east. The bake
was run and QA'd, then discarded with `git checkout -- app/public/tiles api/_data`; this branch
commits source only. `git diff --name-only origin/main` lists nothing under `app/public/tiles/`
or `api/_data/`. The city gets baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`. For the record, the discarded bake touched 583 files:
1 `buildings/`, 1 `toy/`, 572 `ctx/*.json` (global-index renumbering after one dropped
footprint), 3 `context/`, and the manifests plus `api/_data/{stats,search-index}.json`.

## 7. Reproducing

```bash
blender -b --python build_246_ritch.py            # -> 246-ritch.blend, 246-ritch.glb
blender -b --python render_246_ritch.py -- --samples 48
blender -b --python render_246_ritch.py -- --night
python3 make_contact_sheet.py
blender -b --python validate_246_ritch.py         # -> validation.json
```

Add `--workbench` to the render script for a seconds-per-frame iteration pass.

## 8. Approval

Presented at stage 3 on 18 August 2026 (contact sheet, hero aerial from the north-east, night
aerial, and the numbers above). The session's standing instruction, given verbatim in the
invocation, was:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Taken as the gate-3 approval and recorded here as such. It is a standing pre-authorisation
rather than a judgement on these particular renders, so it is quoted as what it is; the
evidence was presented in full before advancing.
