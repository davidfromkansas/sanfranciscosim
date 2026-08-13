# 358 Brannan Street — build report

Asset built 13 August 2026 for `docs/asset-plans/358-brannan.md`, stage 2 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`. Blender 5.2.0 LTS, headless.

**Where the numbers come from:** this file and `REFERENCE.md` beat the plan wherever
they disagree. Two things did disagree — see §3.

## 1. What shipped

| | |
|---|---|
| File | `artifacts/358-brannan/358-brannan.glb` |
| Source | `build_358_brannan.py` (deterministic; re-running reproduces the GLB) |
| Anchor | `-122.3936350, 37.7809258` (footprint OBB centre) |
| Target height | **9.60 m**, the bay cornice cap — the export's bounding-box top |
| Brannan front heading | 135.3° true (SE); Varney Place rear 315.3° (NW) |
| Footprint | 6.93 m x 25.20 m, authored on the measured rectangle |
| Objects / triangles | 55 / 3,860 (cap 7,000) |
| AABB | 22.932 x 23.061 x 9.600 m |
| min Z / XY centre | 0.000 / (−0.014, 0.014) |
| Materials | 10 opaque + 2 `_Glow` |

## 2. Contract compliance

`validate_358_brannan.py` re-imports the exported GLB into a factory-reset scene and
checks the whole contract; `validation.json` is its output. Every check passed on the
first run and again after each revision:

| Check | Result |
|---|---|
| Fresh isolated scene, re-imported final GLB | PASS |
| Metres, plausible dimensions | PASS |
| Crest normalised to 9.60 m exactly | PASS |
| Base at z = 0, centred in XY | PASS |
| Under triangle budget (3,860 / 7,000) | PASS |
| No image textures, no transparency | PASS |
| All materials `Toy_*`, no `Toy_body` | PASS |
| No cameras, lights, animation, armatures, constraints | PASS |
| Transforms applied, no negative scales | PASS |
| Normals outward — per-object signed volume | PASS (55/55 positive, `inverted_solids: []`) |
| Normals outward — 31,500-ray visibility test | PASS (residual within the 0.15% tolerance) |
| No degenerate geometry | PASS (0) |
| No foreign or unexpected objects | PASS |

**Orientation deviation, recorded as the plans README requires:** the contract's "front
faces −Y" cannot be honoured — this building's front faces SE at 135.3°. It is authored
in true-world orientation (`+Y` = north) because `placeGeneric()` applies no rotation,
so real-world orientation wins (AGENTS rule 5).

## 3. Corrections to the dossier made while building

1. **The plan's palette note called for `Toy_steel` on the Varney header and the roof
   furniture, and `Toy_roofd` on both roof decks. Both roof decks were switched to
   `Toy_steel` and the furniture to `Toy_roofd`/`Toy_ink`.** The first aerial review
   showed the reason: `Toy_roofd` (#45454a) over 166 m2 of roof made the building read
   as a black slot from the app's downward camera, which is where it will actually be
   seen, and it is also wrong — the reference aerial shows a pale gray membrane. The
   swap is truthful *and* it lets the dark roof furniture read. `Toy_steel` now doubles
   as the membrane; no new material was added.
2. **The bay sill's overhang was cut from 0.10 m to 0.04 m and the sign band lowered.**
   The first night render showed the hero glow — the tenant's lit sign strip — almost
   entirely shaded out by the bay above it, surviving only as two slivers at the ends.
   A sign under a bay *is* shaded in life, but the app judges this building from a
   30-50° aerial, and a hero cue that only reads from the sidewalk is not a hero cue.

Two further deliberate departures from the plan, both improvements rather than
corrections:

3. **A roof deck was added** — warm decking and two benches inside the railing at the
   Varney end. The plan's §2.7 had only a railing, which left the listing's "roof
   deck/patio" as a line floating over an empty tray. It is the only piece of
   environmental storytelling (style bible §16) a 166 m2 building can carry.
4. **The Varney freight door is glazed** (`Toy_glass`), not a solid roll-up. The Jan
   2025 panorama shows it as a multi-light glazed roll-up, the same as the storefront
   beside it.

## 4. Design decisions worth the reader's time

- **Colour, against a neighbour 100 m away.** `Toy_brick` (#c96f4a) carries the Brannan
  front. Two lots down, `380-brannan` had to *abandon* `Toy_brick` because it merged
  with its coral identity band. Here the problem is inverted: 358's whole job is to
  advance out of a wall of pale warehouses, and it has no second saturated element to
  protect. Both choices are recorded in their respective reports so the block reads as
  two related but distinct buildings rather than one building twice.
- **`Toy_slate` (#6f7883) is a palette extension**, not a project colour — carried over
  from `380-brannan`, where it was introduced for the same slate blue-gray paint.
  Off-palette is a WARN, not a FAIL, under `sf-asset-check` §7.
- **Blind flanks, on purpose.** 25 m of party wall on each side with no openings. Both
  neighbours' walls touch this building; a window grid there would be an invention the
  aerial camera can see, and the baked city puts real neighbours against both faces.
- **The bay sets the crest at 9.60 m, 0.60 m above the parapet.** That lift is the one
  place semantic exaggeration is spent (style bible §8), and it gives an otherwise
  flat-topped box a deliberate high point.

## 5. Night state

Hero glow: the **sign band strip** (`Toy_gold_Glow`, #caa64a) — a batting cage open
until 20:00 has a lit sign, and it is the only warm light on this stretch of Brannan.
Supporting accent: two of the four bay windows (`Toy_glass_Glow`). The Varney Place
elevation does not glow; it is a back alley.

Both glow materials are thin shells standing proud of the opaque surface behind them,
as required — the app draws `_Glow` in a separate layer at `0.12 + 0.95·uNight`
opacity, so a primary surface authored as glow would be a ghost by day. The day renders
preview this correctly (`fade_glow()` sets alpha 0.12).

## 6. Renders

All eight images are rendered from the **exported GLB**, re-imported into an empty
scene, so every one depicts exactly what ships:

`358-brannan-north.png`, `-east.png`, `-south.png`, `-west.png` (one orthographic rig,
identical scale/framing/lighting/exposure, differing only in azimuth; directions are
true compass directions), `-top.png`, `-aerial.png` (the style bible's high
three-quarter camera, 38° down), `-aerial-night.png`, and `-contact-sheet.png`.

Because the building sits at 45°, each elevation view shows a front and a flank
together rather than a single face. That is the heading, not a camera error.

Two rig changes were made to `render_358_brannan.py` versus the `380-brannan` original,
both documented in the file: Cycles now uses the Metal GPU when one is present (~8
minutes per image on CPU versus well under two), falling back silently to CPU; and the
aerial lens dropped from 105 mm to 70 mm at a longer radius, because this asset is 25 m
long on the diagonal inside a 23 m axis-aligned box and the framing heuristic cropped it.

## 7. Draft manifest entry

Written from the measurements above, not from the plan. `estimated` is **true**: no
published height exists for this building and 9.60 m is photogrammetric (see
`REFERENCE.md` §5).

```json
{
  "id": "358-brannan",
  "file": "358-brannan.glb",
  "anchor": [
    -122.3936350,
    37.7809258
  ],
  "targetHeightM": 9.6,
  "cat": 19,
  "name": "358 Brannan Street",
  "estimated": true,
  "dims": [
    22.932,
    23.061,
    9.6
  ],
  "tris": 3860,
  "loadRadius": 2500
}
```

`loadRadius`: the default rule `max(2500, 9.6 × 30)` gives 2500 m. Taken as-is — at
2.5 km a 9.6 m building is far below a pixel, so the empty exclusion zone beyond the
radius is illegible.
</content>
