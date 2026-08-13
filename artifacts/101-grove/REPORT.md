# 101 Grove Street — build report

A validated miniature GLB of the San Francisco Department of Public Health
Building (Samuel Heiman, 1931–32) for the SF-SIM toy diorama city. Built from
`docs/asset-plans/101-grove.md`; research in `REFERENCE.md`. **This report beats
the plan wherever the two disagree.**

## Shipped numbers

| | |
|---|---|
| File | `101-grove.glb` (binary glTF, meshopt-compressed) |
| Size | **421,008 bytes** shipped (1,166,344 pre-optimize) |
| Triangles | **17,648** (budget 22,000; hard gate 30,000) |
| Objects / draw submeshes | **13** after the stage-4 join (611 closed solids as authored) |
| Dimensions | 70.508 × 47.498 × **21.400** m |
| Crest | balustrade top rail, exactly 21.40 m → loader scale factor **1.000000** |
| Min Z | 0.0 m; XY centre offset (−0.003, −0.042) m |
| Materials | 13, all `Toy_*`, no `Toy_body` |
| Glow materials | `Toy_gold_Glow`, `Toy_glassl_Glow` |
| Normals | all groups positive signed volume; ray residual **0.000 %** shipped (0.0032 % as authored; gate 0.15 %) |
| Validation | `validation.json` — **PASS**, 15/15 checks, re-run against the shipped file |

Stage 4 changed no geometry: 17,648 triangles in, 17,648 out, bbox identical to five
decimal places. It joined 611 objects into 13 per-material groups and
meshopt-packed the result — full metrics and gate results in
`optimize/REPORT.md`.

## Reproduce

```
blender -b --python build_101_grove.py          # -> 101-grove.blend, 101-grove.glb
blender -b --python render_101_grove.py         # -> aerial, top, 4 elevations
blender -b --python render_101_grove.py -- --night
python3 make_contact_sheet.py                   # -> 101-grove-contact-sheet.png
blender -b --python validate_101_grove.py       # -> validation.json
```

Blender 5.2.0 LTS, headless, CPU Cycles. Every render and the validation
re-import the **exported GLB**, never the source `.blend`.

## Dossier corrections and decisions made during the build

1. **The plan's target height survived verification, but only as an estimate.**
   The eave is measured twice and independently — 2010 city LiDAR
   (`hgt_median_m` 19.77, `hgt_majoritycm` 20.29) and the OSM `height=20` tag —
   so **20.3 m is solid**. The 21.4 m crest is eave + a balustrade read at
   ~1.1 m off the 2008 reference photograph. No published architectural height
   was found. `estimated: true` in the manifest entry is deliberate.

2. **Nothing on the roof breaks the balustrade.** The LiDAR record's 32.4 m max
   return is unexplained; the orthoimagery shows a slender mast on the west
   roof field, which is the only plausible source. It is **not modelled**: at
   the app's camera it is sub-pixel, and modelling it would make the mast the
   bounding-box top and silently break the `targetHeightM / measuredHeight`
   normalization. The corner penthouse tops out at 20.85 m for the same reason,
   which is also true to the building — nothing breaks the cornice silhouette
   from the street.

3. **Orientation deviates from the contract, deliberately.** The contract asks
   for "front faces −Y". The Grove Street front faces **north** (outward normal
   350.6° true) and the entrance bay faces **north-east** (34.4°). The asset is
   authored in true-world orientation because `placeGeneric()` in
   `app/src/assets.js` never rotates an asset, so real-world orientation wins
   (AGENTS rule 5 and the orientation note in `docs/asset-plans/README.md`).

4. **South and west elevations are inferred, and remain so.** No photograph of
   either was located during the build. Both are modelled as the same
   four-storey punched grid on the same floor lines, without rustication,
   pediments or balconettes, and with a solid capped parapet instead of the open
   balustrade. This is the asset's largest correctness risk. If a photograph
   turns up and contradicts it, the fix is local to `BAYS` and the parapet loop
   in `build_101_grove.py`.

5. **Bay counts are proportional, not counted.** 12 bays on Grove (4.79 m
   pitch), 6 on Polk, 1 on the chamfer, 13 on the south, 7 across the three west
   segments. The 2008 photograph is foreshortened and never shows the whole
   Grove elevation.

## Review iterations

Every round was judged from the high three-quarter aerial first, per the style
bible §18 — the formal rig ran only after the aerial was right.

| # | Finding | Fix |
|---|---|---|
| 1 | The entrance arch rendered as a shimmering crumpled slab that hid the door and the oculus entirely. Two causes: the arched recess plate was authored at depth 0.0, coplanar with the solid wall prism, so it z-fought; and the archivolt was built as **one concave n-gon**, which Blender fans from its first vertex — the fan of a C-shape fills its own hole and drew a blank cap over the whole opening. | Added `facade_strip()`, which builds a band as a chain of convex segment solids, and moved every corner-bay element clear of the wall. |
| 2 | With the arch fixed, it filled with cream course lines instead of shadow: the rusticated base courses stand 0.20 m proud, so the arch group at 0.05 m was buried **behind** them. | The whole corner-bay group now clears 0.22 m, in a strict depth order (archivolt 0.22–0.50, recess 0.23–0.31, door and oculus 0.32–0.52, glow shells beyond). Ground-floor windows were pushed out to match. |
| 3 | The rusticated base did not read as rusticated — three courses with a 0.10 m joint step vanished at distance. | Four proud courses, three joints at a real 0.18 m step. |
| 4 | The corner penthouse vanished from above: `Toy_trim` on a `Toy_white` membrane is the same value. | Penthouse rebuilt in `Toy_stone` with a `Toy_roofd` monitor curb. |
| 5 | The light court read as a hole punched in the roof — a `Toy_roofd` field that large is near-black from the app's camera. | A `Toy_steel` kerb with a smaller `Toy_roofd` pad inside it, and the single long plant slab split into three blocks. |
| 6 | A full-length roof walk read as a slash across the membrane; two roof hatches sat as stray objects. | Walk shortened to an L tying the plant cluster to the court; hatches regrouped against existing clusters. |
| 7 | The fourth floor did not read as the short storey it is. | Fourth-floor band narrowed to 15.60–17.70 m. |
| 8 | The corner aedicule's pediment did not span its pilasters. | The chamfer's enrichment widened to 4.20 m so balconette and pediment span the full bay — which is also right: this is the grand bay. |
| 9 | Elevations wasted half the frame on empty sky and the top view clipped. | Elevation rig at 1500 × 640 aimed at mid-height; top view widened to 1.16 × span. |

## Night state

One hero, one supporting group. **Hero:** the corner entrance — two lantern
sconces, the oculus and the door transom read as a single warm gold pool at the
chamfer, which is how the building is lit in life. **Supporting:** a
deterministic irregular scatter of lit windows on Grove and Polk only
(`(bay * 7 + floor * 3) % 5 == 0`), never a full grid — a 24-hour public health
building. **Nothing on the roof glows.** Every glow surface is a thin shell,
inset and lifted clear of the opaque glazing behind it: the app draws `_Glow` in
a separate layer at ~12 % alpha by day, and coincident faces read as a
triangulated smear.

## Contract compliance

| Rule | Status |
|---|---|
| Real-world metres, plausible dimensions | PASS |
| Origin base-centre, min Z ≈ 0 | PASS (0.0; XY offset 4 cm) |
| Orientation | true-world, deviation recorded above |
| Flat-colour materials only, `Toy_*` names | PASS (13 materials) |
| `_Glow` only on night-glow surfaces | PASS |
| No `Toy_body` | PASS |
| No image textures, no transparency | PASS |
| No cameras, lights, animation, armatures, constraints | PASS |
| Transforms applied, no negative scales | PASS |
| Outward normals | PASS (signed volume + 31,500-ray test) |
| No degenerate geometry | PASS |
| Triangle budget | PASS (17,648 ≤ 22,000) |

## Approval

Approved by David on 12 August 2026, quoted verbatim:

> "Do it on a new branch and PR -- i approve all stages just proceed"

Given in advance of the renders, as an explicit blanket approval of every gate
in `docs/asset-pipeline/ADDRESS-TO-ASSET.md` for this building.

## Draft manifest entry

```json
{
  "id": "101-grove",
  "file": "101-grove.glb",
  "anchor": [-122.4186747, 37.7781359],
  "targetHeightM": 21.4,
  "cat": 18,
  "name": "101 Grove Street (Public Health Building)",
  "estimated": true,
  "dims": [70.508, 47.498, 21.4],
  "tris": 17648,
  "loadRadius": 2500
}
```

`cat: 18` is `government` in `pipeline/taxonomy.mjs`. `estimated: true` because
the crest is an inference on a measured eave. `loadRadius` follows the default
rule `max(2500, 21.4 × 30)` = 2500; there is no case for `alwaysLoaded` on a
21 m building.
