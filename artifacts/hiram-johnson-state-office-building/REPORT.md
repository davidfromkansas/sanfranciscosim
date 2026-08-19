# Hiram W. Johnson State Office Building — build report

**Asset:** `artifacts/hiram-johnson-state-office-building/hiram-johnson-state-office-building.glb`
**Plan:** `docs/asset-plans/hiram-johnson-state-office-building.md`
**Dossier:** `REFERENCE.md` in this folder — **REPORT and REFERENCE beat the plan.**
**Built:** 19 August 2026, Blender 5.2.0 LTS, headless, deterministic script.

## 1. Numbers

These are the **shipped** numbers — the file in this folder is the stage-4
optimized asset. The pre-optimize authoring output is archived byte-for-byte at
`optimize/input/`.

| | authored | shipped |
|---|---|---|
| Objects (mesh) | 129 | **9** (joined per material) |
| Triangles | 16,908 | **16,908** |
| Dimensions (x, y, z) | 130.655 × 67.179 × **61.900** m | identical |
| Footprint before the 8.73° grid rotation | 127.38 × 47.70 m | identical |
| min Z / max Z | 0.000 / 61.900 m | identical |
| XY centre offset | 0.000, 0.000 m | identical |
| `targetHeightM / measuredHeight` | 1.000000 | **1.000000** |
| Materials | 9, all `Toy_*`, flat, no textures, no alpha | identical set |
| Glow materials | `Toy_glassl_Glow`, `Toy_gold_Glow` | identical |
| GLB bytes | 893,324 | **421,380** (−52.8 %, meshopt) |
| Normals | signed volume positive on every object; ray residual **0.018 %** (tolerance 0.15 %) | same |
| Contract validator | PASS | **PASS**, all 15 checks — `validation.json` |

Reproduce: `blender -b --python build_hiram_johnson.py`, then
`blender -b --python render_hiram_johnson.py --`, then
`python3 make_contact_sheet.py`, then
`blender -b --python validate_hiram_johnson.py`. Stage 4 is
`optimize/` — see `optimize/REPORT.md`.

## 2. Orientation — read this before integrating

Authored with Blender **+Y = true north, +X = east**, so `placeGeneric` in
`app/src/assets.js` (which only scales and positions) drops it in at its real
heading. The long axis runs at bearing **81.27°**; the whole assembly is rotated
**+8.73°** about Z from the grid frame.

**The public entrance faces NORTH (+Y), onto Golden Gate Avenue.** That is the
opposite of the contract's nominal "front faces −Y". Real-world orientation wins
here — `placeGeneric` applies no rotation, so a mirrored building would be wrong
from every side. Do not "fix" the heading at integration time.

## 3. What was built

Grid frame: E 0 → 127.38 (west → east), S 0 → 47.70 (north → south), Z up.

- **Granite base** z 0 → 6.0, `Toy_stone`, projecting 0.3 m
- **Main body** z 6.0 → 42.9, `Toy_cream`, on the sculpted plan outline
- **Punched lattice** on the two long faces: nine `Toy_glass` storey bands
  (2.4 m tall at 3.83 m pitch) behind applied `Toy_cream` piers at 8.40 m pitch
  and applied spandrels, closed top and bottom by `Toy_trim` courses
- **Glazed ribbon** z 42.9 → 53.6, a real 0.55 m set-back block with three
  continuous `Toy_glass` bands and `Toy_trim` spandrels — the change of
  character the plaza photograph shows in the top three storeys
- **End drums**: both short ends built as smooth arcs from the measured OSM
  profile — two convex granite piers (`PIER_BOW` 1.10 m) with a concave
  recessed `Toy_teal` glass bay between them (z 13.4 → 51.5, four `Toy_trim`
  mullion bands), and four `Toy_roofd` full-height louvre slots per end
- **Roof**: `Toy_trim` parapet ring z 53.6 → 55.0, `Toy_steel` deck at 53.75,
  `Toy_cream` mechanical penthouse (E 34–92, S 16.5–31.5) z 53.75 → 59.9 with a
  `Toy_roofd` louvre band and a `Toy_trim` cap to **61.90 m**, two `Toy_teal`
  atrium skylights on `Toy_trim` curbs, three mechanical boxes, one stair penthouse
- **Golden Gate Avenue entrance**: a 30 m convex `Toy_glassl_Glow` bay bulging
  4.2 m north to z 30.6 with three mullion bands and a `Toy_trim` eyebrow,
  flanked by `Toy_cream` granite jambs; a 36 m curved `Toy_trim` canopy on four
  `Toy_stone` piers with a `Toy_gold_Glow` soffit; a `Toy_gold_Glow` lobby plane
  behind it
- **Polk Street shopfront**: one `Toy_glass` recess in the east base

## 4. Night state

Three glow surfaces, all in one place: the entrance bay (`Toy_glassl_Glow`
`#6f95b8`), and the canopy soffit + lobby glazing (`Toy_gold_Glow` `#caa64a`).
The night silhouette is a dark slab with one lit doorway under a lit bulge —
which is what the building actually does after hours, and it keeps a 127 m
facade from out-shouting City Hall's dome 200 m away. The window grid and the
two end bays deliberately do **not** glow. Both glow base colours are palette
neighbours of the non-glow set, so the daylight asset stays calm — the repo's
standing correction applies: a `_Glow` material's base colour *is* its night look.

## 5. Corrections and defects found during the build

1. **The plan's bowed south front does not exist.** Caught before modelling and
   corrected in the plan itself (commit `3c08d981`). The OSM south edge is
   collinear to within 1 cm over 91 m; a **rectilinear** re-projection of the
   Civic Center Plaza panorama shows a dead-straight parapet beside the Earl
   Warren's straight cornice. The arcs in a **cylindrical** crop of the same
   panorama are the projection — the Earl Warren cornice arcs identically there
   and is known to be straight. SOM's "sweeping curve of the tallest slab" is
   realised as the end drums and the north entrance bay. Full argument in
   `REFERENCE.md` §6.
2. **Street View panorama tiles are north-aligned at u = 0 plus 180°, not at the
   metadata `yaw`; and the tile grid at zoom z is 2^z × 2^(z−1).** Both were
   wrong for several research passes, and both failure modes render a
   *plausible* strip of the wrong building — in this case the Phillip Burton
   Federal Building across the street. Calibrated against City Hall's dome.
3. **`Toy_roofd` renders near-black on a large flat roof deck** under the review
   rig; the roof read as a hole in the model. Deck changed to `Toy_steel`.
4. **Coincident faces make Cycles shade the model's unlit interior.** The deck's
   top was coplanar with the ribbon block's top cap, and the parapet's outer wall
   was coincident with the ribbon's outer wall. Both rendered pure black (0,0,0)
   from above while Workbench showed them correctly — it is not a geometry bug
   and no amount of normal-checking finds it. Fixed by offsetting the deck to
   53.75 m and standing the parapet 0.06 m proud.
5. **Collinear runs in the sampled plan outline produced sliver triangles** whose
   shared vertex normals collapsed to zero length: 5
   `invalid_or_nonunit_loop_normal_count`, which failed the contract validator on
   `normals_outward` even though every solid was manifold and the ray residual
   was 0.018 %. Fixed by a collinearity/duplicate cleanup on every generated ring
   (`dedupe_ring`, plus one shared keep-mask for the plan outline so the parapet's
   outer and inner rings stay index-aligned). Side benefit: 24,808 → 21,068 tris.
6. **The same failure came back in the SHIPPED file only.** A 0.12 m bevel on the
   parapet ring manufactured 2,624 sub-5 mm faces where the bevel profiles meet at
   the drum corners. They are harmless in the authored GLB — the validator counted
   zero invalid normals there — but the stage-4 weld collapsed two of them, and
   gltfpack re-emits the STORED normals, so `invalid_or_nonunit_loop_normal_count:
   2` appeared only after the shipping swap. **Re-run the stage-2 contract
   validator against the post-optimize file, not just the authored one.** Fixed by
   dropping that bevel: 21,068 → 16,908 tris and zero sub-5 mm faces anywhere.
7. The entrance bay was too small to read at the first review and was widened
   from 24 m to 30 m, raised from 27.0 m to 30.6 m, and given granite jambs and a
   wider canopy.

## 6. Known limitations

- Stage 4 brought the file to 421,380 B, inside the 500 KB compressed-on-disk
  budget, at −52.8 %. That is short of the prompt's 60 % aspiration; the waste
  census shows the remainder is silhouette geometry (`optimize/REPORT.md` G6).
- Two ~2 px black slivers remain at the parapet's outer corners on the drums in
  the top view, where the mitred offsets of two rings diverge at a concave
  corner. Below the app's pixel budget; recorded rather than chased.
- The roof layout (penthouse extent, skylight positions) is *estimated* — see
  `REFERENCE.md` §6. It satisfies the LiDAR median/maximum/standard deviation and
  the plaza photograph, but no source shows this roof clearly.

## 7. Draft manifest entry

```json
{
  "id": "hiram-johnson-state-office-building",
  "file": "hiram-johnson-state-office-building.glb",
  "anchor": [-122.4179151, 37.7810345],
  "targetHeightM": 61.9,
  "cat": 18,
  "name": "Hiram W. Johnson State Office Building",
  "estimated": false,
  "dims": [130.6549, 67.1789, 61.9],
  "tris": 16908,
  "loadRadius": 2500
}
```

`loadRadius` is the default rule `max(2500, 61.9 × 30)` = 2500.

## 8. Integration measurement done ahead of time

Case B. Measured against the real bake input
(`pipeline/data/overture_buildings.geojsonseq`) with the metric `excluded()` in
`pipeline/buildings.mjs` actually applies — **centroid OR any ring vertex inside
the radius** — over all 45 footprints within 160 m of the anchor:

```
  r =  3 … 26 m -> drops 1   (this building; its centroid is 0.2 m from the anchor)
  r >= 26.81 m  -> drops 2   (also the Earl Warren Building)
```

26.81 m is the party-wall vertex the two footprints **share**, so it is the hard
ceiling. The OBB half-diagonal that most entries use is 68.0 m and would be
badly wrong here. **Use `exclude: 12`** — the middle of the safe band, 14.8 m of
margin to the shared vertex, and the same value the neighbouring
`earlWarrenBuilding` entry uses for the same reason.

## 9. Approval

Presented at stage 3 with the contact sheet, the aerial day and night renders and
the numbers above. Pipeline invocation carried a standing approval
("APPROVE EVERYTHING DONT ASK ME FOR PERMISSION", 19 August 2026), which is
recorded here as the stage-3 gate. No design feedback was received, so no
revision loop was run.
