# Fulton Plaza — build report

`fulton-plaza.glb`: 21 objects, **13,364 triangles**, **345 KB raw / 220 KB gzip** as
shipped (meshopt-compressed; 676 KB before stage 4), 16 palette materials, **draped on the
baked terrain**, all 19 contract checks PASS in a fresh-scene re-import of the *shipped*
file (`validation.json`).

The asset is the pedestrianised block of Fulton Street between Larkin and Hyde — the 120 m
× 49 m right-of-way between the Asian Art Museum and the Main Library, with the 1894 Pioneer
Monument on its exact centre and Jeremy Novy's two 20-metre koi circling it on the black
asphalt.

## Numbers

| | |
|---|---|
| Manifest anchor | `-122.4159308, 37.7796961` (model XY bbox centre) |
| Right-of-way OBB centre | `-122.4159189, 37.7796904`; the model sits 1.051 m west / 0.626 m north of it |
| `targetHeightM` | **12.7999 m** — the vertical extent, so the loader's scale is 1.0 |
| Dimensions | 128.4915 × 67.6286 × 12.7999 m |
| `min_z` | **−1.50 m** — negative by design; z = 0 is the anchor's ground |
| XY centre offset | 0.0000, 0.0000 |
| Long axis | 81.15° true (toward Hyde Street); cross axis 171.15° |
| Right-of-way | 120.04 × 48.59 m oriented, 5,805 m² = 1.435 acres |
| Terrain | draped; falls 2.366 m along the axis, **cross-falls 0.874 m**, anchor 17.788 m |
| Deck standoff | Z_DECK = 0.55 m above grade, max error over 32 ray-cast samples **0.0039 m** |
| Monument crest | 11.268 m above local grade — apron 0.63 + 10.668 m (SFAC 420 in) |
| Koi | two bodies, 20.642 m each |
| Triangles | 13,364 of a 16,000 cap |
| File | 353,476 B raw / 225,263 B gzip9, meshopt-compressed. Pre-optimize 692,360 B; see `optimize/REPORT.md` |
| Category / streaming | `cat: 0`, `loadRadius: 2500` |

## Triangles by object

| object | tris |
|---|---|
| `monument` | 4,160 |
| `joints` | 2,304 |
| `bollards` | 1,568 |
| `trees` | 1,104 |
| `deck` | 970 |
| `koi` | 408 |
| `koi_glow` | 384 |
| `lamps` | 384 |
| `people` | 384 |
| `terrace_s_wall` | 288 |
| `terrace_s` | 256 |
| `walk_n` | 210 |
| `furniture` | 180 |
| `apron` | 156 |
| `lamps_glow` | 144 |
| `bed_*_kerb`, `bed_*_soil` (4) | 400 |
| `ashurbanipal` | 52 |
| `monument_glow` | 12 |

## Validation

`validate_fulton_plaza.py` factory-resets Blender, imports **only the exported GLB**, and
writes `validation.json`. Overall **PASS**.

| check | result |
|---|---|
| meters and plausible dimensions | PASS — 128.5 × 67.6 × 12.8 m |
| vertical extent matches the build's own metadata | PASS |
| height datum is the monument | PASS — the crest vertex belongs to `monument`, not to a tree |
| **deck drapes the terrain** | PASS — 32 samples, max standoff error 0.0039 m (tolerance 0.10) |
| koi are two bodies of the right size | PASS — 20.642 m and 20.642 m, clustered against the surveyed centres |
| koi carry both day and night materials | PASS |
| centred in XY | PASS |
| under triangle budget | PASS — 13,364 / 16,000 |
| no image textures / no transparency | PASS |
| materials follow the contract | PASS — 16 `Toy_*`, no `Toy_body` |
| no cameras, lights, animation, skins, constraints | PASS |
| transforms applied, no negative scales | PASS |
| normals outward — per-object signed volume | PASS — 21/21 shells enclose positive volume |
| normals outward — 31,500-ray residual | PASS |
| no degenerate geometry, no unexpected objects | PASS |

`min_z ≈ 0` is **not** among the checks and its absence is deliberate: this asset is the
ground, so z = 0 is the anchor's elevation and `min_z` is −1.50 m. The drape check above
replaces it. See REFERENCE.md, "The terrain drape".

## Stage 4 — optimize

`gltfpack@0.24 -c -km -kn -noq` applied to the approved build: **692,360 → 353,476 bytes
raw, −48.9%**, geometry byte-identical, max A/B pixel delta 0.046%, all gates PASS.

**Phase B was measured and reverted in full.** Six variants; every one produced a *larger*
file than doing nothing, including the join — the Blender import/re-export round-trip alone
costs 67 KB and 6,924 vertices on this asset, which no cleanup step recovers. The 1 mm weld
cost a further 117 KB (the flat-shading topology is not waste), and the limited dissolve,
which did help by 22 KB, could not close the gap. Full table in `optimize/REPORT.md`.

## Renders

`fulton-plaza-top.png` (the primary review image), `-aerial.png`, `-axis.png`,
`-north/-east/-south/-west.png`, `-aerial-night.png`, and `-contact-sheet.png`. All are
rendered from a fresh import of the shipped GLB.

The four elevations are extreme letterboxes — 128 m across and 12.8 m tall — and mostly
empty above the tree line. That is framed to the plan dimension on purpose rather than
zoomed to fit, so the four share one rig.

## Build iterations, and what each one fixed

1. **The monument's own datum was 0.60 m short.** The monument's heights were authored above
   local grade while its base stands on the apron, so the catalogue's 420 in landed at
   10.67 m instead of 11.27 m. Now `MON_H` is explicitly measured from the monument's own
   base and `Z_APRON` is added at every use.
2. **Bollards cost 11,134 triangles.** Thirty 8-sided bollards at a 0.10/2 bevel. They are
   1 m tall roadside furniture; the bevel bought nothing and the build blew a 16,000 cap at
   20,118. Added to the unbevelled set: 1,568.
3. **The studio floor sliced through the plaza.** The review rig's contact-shadow catcher
   sat at z = −0.02 and was sized `height × 5`. On a draped asset z = 0 is not the floor, and
   on a 128 m plaza 5 × 12.8 m is not a table — it rendered as a cream slab lying across the
   south terrace. Now it sits at `min_z − 0.02` and is sized from the plan extent.
4. **The koi were white fish with dots on them.** The markings were three small ellipses; at
   the app's camera distance the orange has to be a saddle or the plaza loses its only
   saturated accent. Replaced with three large polygonal saddles covering ~40% of the body.
5. **The monument read as four little chapels.** The central pedestal was too slim and the
   bronzes were hexagonal frusta that read as pagoda spires. The pedestal gained a wider
   base course, and the figures are now chunky silhouettes (tapered body, head) turned to
   their own cardinal directions.
6. **A 45 m scored joint drew straight across the monument's apron.** `prism_verts_faces()`
   puts a plane through four corners, and this site cross-falls 0.87 m, so a long thin prism
   is not draped just because its corners are. Measured in the exported GLB: `joint_u5`
   spanned z +0.40 to +1.19 where the apron topped out at +0.77. Every long bar is now
   segmented (`draped_bar()`) or gridded (`draped_slab()`), and the joints merged from 13
   objects into 1.
7. **The koi sank into the asphalt in patches.** 5 mm of clearance over a deck whose top is
   a 4 m drape grid, interpolated differently by a 20 m polygon. Raised to 30 mm.
8. **The lamps did not light up at night.** The glow box was authored *inside* the opaque
   head. It is now a lens plate under the housing.
9. **The koi lost their markings at night.** One white glow shell was drawn over the orange
   saddles. The markings now glow on top of the shell in their own colour.
10. **The scored joints read as a grid of black bars.** `Toy_ink` divided the plaza into
    tiles. `Toy_seam` (`5f5f68`) gives the asphalt a scale instead of a pattern of its own.
11. **The validator's first drape sample missed a quarter of its points.** The outer row at
    `v = 16` landed on the south terrace, not the deck, and rays that hit an overlay are
    skipped — so a badly chosen grid shrinks the sample silently rather than failing. Moved
    to `v = 12`, and the koi cluster now seeds from the **surveyed** koi centres rather than
    from a self-chosen threshold, which had split one 20.5 m fish into two bodies.

## Corrections to the asset plan

`docs/asset-plans/fulton-plaza.md` was written before the model existed. Two numbers moved:

1. **`targetHeightM` is 12.7999 m, not 10.67 m.** The plan set the target to the Pioneer
   Monument's catalogue height and asked the validator to assert `max_z == 10.67`. That is
   incompatible with the terrain drape the same plan mandates: once z = 0 means the anchor's
   ground, the export spans −1.50 to +11.27 m and the loader's scale is
   `targetHeightM / 12.80`. The monument is still 10.668 m of monument and still the model's
   crest; it now stands on a 0.63 m apron on a draped deck. This is the convention
   `64-south-park` (21.0415 m) and `424-brannan` already ship under, and the plans README
   already documents it.
2. **The expected XY bbox is 128.5 × 67.6 m, not 126.1 × 66.3 m.** The plan's figure was the
   right-of-way alone; the planting beds overhang the museum's property line by up to 2.0 m
   (measured, real, and harmless) and the tree crowns add another 2.3 m beyond that.

Everything else in the plan held — including the exclusion measurement, the "no
`clearTrees`" finding, and the baked-street-under-the-deck hazard.

## Open risks

1. **The koi are the asset, and they are the least-measured thing in it.** Their published
   length (65–70 ft) and their positions are solid; the silhouettes are authored from one
   aerial image at 0.110 m/px of a mural that has been on the ground since 2024 and wears.
   If the outlines are wrong, the asset is wrong — no other element carries this much of the
   recognition.
2. **The tree height is a design decision, not a measurement.** Crowns are set at 7.80 m
   (north) and 5.60 m (south) above local grade so the Pioneer Monument stays the tallest
   thing on its own plaza after the 2.37 m drape. A measured plane above 11.27 m would be a
   real conflict; the honest resolution is to keep the monument as the datum and record the
   trees as restrained, not to move the datum onto a lollipop.
3. **SPECTRA is deliberately absent** — it would occlude the koi from the app's own camera,
   it hangs from two other assets' roofs, and it is a two-year installation. Expect to defend
   this. REFERENCE.md carries the full argument.
4. **The asphalt tone has to be judged in the app, not here.** `Toy_roofd`-dark values come
   back rgb(9,9,12) in the diorama; `6f7076` is chosen against that measurement, but the
   only place it can be confirmed is stage 5.
5. **The plaza may stop being a plaza.** The SFMTA closure runs to 31 August 2027 and is a
   renewable permit, not a permanent change — which is exactly why a street ribbon still
   bakes underneath.

## Approval

Gate 3 was given in advance, in the session's invocation, verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

— David, 19 August 2026. The renders and numbers above were presented in the same session
before stage 4 began; no revision was requested.
