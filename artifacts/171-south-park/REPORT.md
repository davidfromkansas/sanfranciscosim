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
| Triangles | **5,816** (cap 8,000) |
| Objects | 100 |
| Materials | 12, all `Toy_*`, flat, no textures, no alpha |
| Glow groups | 2 (`Toy_glass_Glow`, `Toy_trim_Glow`) |
| min Z | 0.000 |
| Validation | **PASS** — all 16 checks, see `validation.json` |

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
  "tris": 5816,
  "loadRadius": 2500
}
```

Integration is a separate job — see the plan's 2.13, in particular the exclusion
window (`0.59 m < exclude < 3.83 m`, use `exclude: 2`), which is the tightest in
the registry and whose failure mode is the silent deletion of two neighbouring
historic contributors from the baked city.

## 9. Approval

Awaiting the user's stage-3 decision. Nothing beyond this artifact folder has been
touched: no manifest entry, no registry entry, no app code, no tiles.
