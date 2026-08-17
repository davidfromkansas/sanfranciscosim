# 160 South Park — build report

Miniature GLB for the SF toy-diorama city, built from
`docs/asset-plans/160-south-park.md`. **REPORT beats plan:** where this file and the plan
disagree, this file is what was built and why.

## Shipping numbers

| | |
|---|---|
| Asset | `artifacts/160-south-park/160-south-park.glb` |
| Triangles | **3,792** (cap 7,000) |
| Objects | 50 |
| Dimensions | **25.795 × 17.769 × 9.400 m** |
| Min Z / XY centre | 0.000 / (0.000, 0.000) |
| Materials | `Toy_brick`, `Toy_glass`, `Toy_glass_Glow`, `Toy_glassl_Glow`, `Toy_ink`, `Toy_roofd`, `Toy_rust`, `Toy_steel` |
| Glow groups | 2 — the arched window (hero) and the storefront (accent) |
| File size | 229,048 B raw / 53,426 B gzip (pre-optimize) |
| Manifest anchor | **`-122.3948620, 37.7812804`** |
| Registry / exclusion point | `-122.3949116, 37.7812949` |
| `targetHeightM` | **9.4** |
| Facade heading | 108.13° true |
| Validation | **all-PASS**, `validation.json` |

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
| Normals outward — per-object signed volume | PASS (50/50 positive) |
| Normals outward — ray test | PASS (31,500 first hits, 0 flipped, 0.000% residual) |
| No degenerate geometry | PASS (0) |
| No unexpected objects | PASS |
| **Overall** | **PASS** |

## Renders

All regenerated from the final export. `-facade.png` is the square-on street elevation at
its own scale; `-east/-west/-north/-south.png` share one rig framed to the 26 m dimension
and are named for the nearest compass direction to each building-aligned face;
`-top.png`, `-aerial.png`, `-aerial-night.png`, and `-contact-sheet.png`.

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

`dims` and `tris` will be restated after stage 4 (optimize). The registry entry for
`pipeline/lib/landmarks.mjs` uses the **exclusion** point, not this anchor — see the plan's
2.13; the measured window is `0 < exclude < 1.70 m` and the value is `1.2`.

## Approval

Pending — presented for review at stage 3.
