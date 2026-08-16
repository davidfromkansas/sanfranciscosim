# 592 Third Street — build report

Miniature GLB of the 1905 corner building at 588–592 3rd Street / 400–414
Brannan Street, San Francisco, for the SF toy-diorama city. Built 13 August 2026
from `docs/asset-plans/592-third.md`; sources and every measured number in
`REFERENCE.md`.

| | |
|---|---|
| Shipping file | `592-third.glb` |
| Manifest id | `592-third` |
| Anchor (WGS84) | `-122.3946805, 37.7800910` |
| Target height | **8.20 m** (parapet crest) |
| Dimensions (AABB) | 31.21 × 32.21 × 8.20 m |
| Triangles | **3,352** (cap 9,000) |
| Objects | 101 |
| Materials | 9, all `Toy_*`, 2 `_Glow` |
| Validation | **PASS** — all 16 checks (`validation.json`) |

## Corrections to the plan

**1. The DataSF ring has a zero-width spike; the 3rd Street frontage is 21.67 m,
not 23.90 m.** Found while converting the published `SF3776114` polygon to
Blender coordinates. The ring's last vertex before closing lies on the 3rd Street
frontage line to within 9 mm, 2.23 m short of the first vertex — so the first
vertex is a degenerate spike past the real corner. Taking the ring literally
would have built the most visible elevation 2.2 m too long and put the anchor
0.79 m out of place. The anchor moved from `37.7800981` to **`37.7800910`** and
the AABB from ~31.0 × 33.2 m to **31.21 × 32.21 m**. The plan, its README row
and this report all now carry the de-spiked numbers. See `REFERENCE.md` ⚠3.

**2. `hgt_max = 11.65 m` is street-tree canopy, not the crest** — confirmed
against both the 2026 satellite imagery and the May 2025 Street View capture,
which show two mature trees at the 3rd Street kerb overhanging the parapet. The
plan called this and it held. Crest stays at 8.20 m (deck 7.82 + 0.38 parapet),
`estimated: true`.

**3. OSM's 478 m² footprint is a Bing trace** and is displaced north on the 3rd
Street edge. Built on DataSF, as the plan instructed.

## Build iterations

Three passes, each judged from the high three-quarter aerial first, per the style
bible.

**Pass 1 — massing.** 82 objects, 2,852 tris. Correct silhouette, correct corner,
but three defects visible in the first aerial:

- *Punched windows read as solid white blocks.* The glazing was authored recessed
  behind the wall plane (`d = -0.10 … 0.02`) inside a proud white surround, so
  from every camera the app uses only the surround was visible. **Fix:** glazing
  now sits proud of its own surround (`0.03 … 0.07`) with a `Toy_trim` centre
  mullion. This is a general lesson for this rig — a recessed fill on a flat-shaded
  toy asset is an invisible fill.
- *The roll-up garage door and the 3rd Street entry were invisible*, both for the
  same reason: dark panels recessed into a near-black band. **Fix:** the garage
  door became `Toy_steel` standing proud (a roll-up shutter really is bare metal,
  and on a black band a dark door is nothing); the entry became a `Toy_trim`
  surround with a glazed door, which carries the same information legibly.
- *Two of the five skylight caps vanished in daylight.* They had been authored
  **as** `Toy_glassl_Glow` — i.e. a primary surface authored as glow, which the
  contract forbids for exactly this reason: the app draws `_Glow` in a separate
  layer at ~12 % alpha by day, so the caps disappeared and the kerbs read as
  empty trays. **Fix:** all eight caps are opaque `Toy_glassl`; two carry a
  separate thin `Toy_glassl_Glow` shell above them for the night pass.

Also in pass 1: the roof deck was `Toy_roofd` (`45454a`), which rendered as a
near-black square. Against 599 Third across the street — whose deck is pale — a
24 m black tile was both wrong for the real weathered mid-grey membrane and out
of family. Changed to `Toy_steel` (`9aa0a6`), in palette.

**Pass 2 — legibility.** 94 objects, 2,980 tris. All four defects resolved. The
remaining problem was the roof: five objects on a 489 m² tray still read as
empty from the app's camera, where the aerial imagery shows roughly a dozen.

**Pass 3 — the roof.** 101 objects, **3,352 tris**. Eight skylights, two hatches,
two vent clusters, in the loose non-grid scatter the imagery shows. Shipped.

## What is in the asset

Stucco body on the measured footprint; a plain parapet ring setting the 8.20 m
crest; a continuous near-black shopfront field and awning fascia on both street
edges, mitred by overlap at the east corner so the band reads as continuous
around it; four glazed bays and a steel roll-up door on Brannan; four glazed bays
plus a glazed entry on 3rd; ten punched upper windows with white surrounds and
centre mullions; four wall-mounted condensers on Brannan; two blank party walls;
a mid-grey roof deck with eight skylights, two hatches and two vent clusters.

**Not in the asset:** 3rd Street, Brannan Street, 599 Third, 414 Brannan, the
north-west neighbour, the two street trees, sidewalk, bike racks, signals,
vehicles, people, plinths, cameras or lights.

## Orientation

Authored in true-world orientation: Blender `+Y` = north, `+X` = east, so the
loader (`placeGeneric` in `app/src/assets.js`, which scales and positions but
never rotates) drops it in at its real heading. The 3rd Street front therefore
faces **45.1° NE** and the Brannan front **135.2° SE**, which means the contract's
"front faces −Y" rule cannot be honoured literally — real-world orientation wins
(AGENTS rule 5, and the standing note in `docs/asset-plans/README.md`). The
axis-aligned XY bounding box of 31.21 × 32.21 m is the expected consequence of a
~45° heading on a 21.67 × 23.07 m building, not a scale error.

## Night state

Hero glow: the shopfront bays on both streets, lit as one warm band wrapping the
corner — a café and an office on a corner are what is actually lit at street
level, and one continuous band is far more legible at city scale than scattered
lit windows. Supporting accent: two skylights faintly lit from the floor below.
The upper storey stays dark. All glow surfaces are thin shells proud of the
opaque glazing they sit on; no primary surface is authored as glow.

The night render drives `_Glow` from **Base Color**, not from the imported
emission — glTF writes `emissiveFactor = 0` when the authored emission strength
is 0, so a re-imported `_Glow` material otherwise renders as a white slab.

## Validation

`validate_592_third.py` re-imports `592-third.glb` into a fresh isolated scene
and validates the re-import, never the authoring scene. All 16 checks PASS:
metres and plausible dimensions, crest normalized to 8.20 m, base at z = 0,
centred in XY (offset 0.169 / −0.001 m), under the triangle budget, no image
textures, no transparency, materials follow the contract, no cameras or lights,
no animation/skin/constraints, transforms applied, no negative scales, normals
outward by per-object signed volume, ray-test residual within tolerance, no
degenerate geometry, no unexpected objects. Full output in `validation.json`.

## Renders

`592-third-{north,east,south,west}.png` (one orthographic rig, identical
scale/framing/lighting/exposure, azimuth only differs),
`592-third-top.png`, `592-third-aerial.png`, `592-third-aerial-night.png`,
`592-third-contact-sheet.png`. All regenerated from the final export.

Because the building sits at 45° to the world axes, the **east** elevation looks
straight at the hero corner and shows both designed street faces at once; that is
the view to judge. North and south each show one street face plus one party
wall; west shows the two party walls and is correctly almost blank.

## Draft manifest entry

```json
{
  "id": "592-third",
  "file": "592-third.glb",
  "anchor": [
    -122.3946805,
    37.780091
  ],
  "targetHeightM": 8.2,
  "cat": 3,
  "name": "592 Third Street",
  "estimated": true,
  "dims": [
    31.2145,
    32.2102,
    8.2
  ],
  "tris": 3352,
  "loadRadius": 2500
}
```

`estimated: true` because the 8.20 m crest is a derived parapet allowance, not a
published or directly measured figure.

## Stage 5 — integration (batch mode, local)

Case **B** (new landmark). Registry entry `592Third` added to
`pipeline/lib/landmarks.mjs` with `exclude: 6`; manifest entry appended; GLB
copied to `app/public/sf-assets/landmarks/592-third.glb`. The city was re-baked
for the QA and then discarded per the batch rule in `ADDRESS-TO-ASSET.md` — this
branch commits source only.

| QA item | Result |
|---|---|
| Re-validation of the shipped GLB | **PASS** — 16/16 contract checks |
| Manifest entry | **PASS** — `592-third`, cat 3, `estimated: true`, `loadRadius` 2500 |
| id mapping | **PASS** — `camelId('592-third')` = `592Third`, matches the registry |
| Registry + re-bake | **PASS** |
| `audit.mjs` check 1.6 | **PASS** — 59 zones over 58 landmarks clear |
| `verify-rebake.mjs` | **PASS** — 584/585 cells unchanged; `23_13` 219 → 218; nearest survivor 12.9 m vs the 6 m radius |
| Single building at the site | **PASS** — no surviving baked ring has a vertex or centroid inside the footprint; nearest is 12.9 m out (the 14.1 m neighbour on the NW party wall) |
| Merge line | **PASS** — `sf-assets: 592-third merged 11 objects / 9 materials -> batched (2145 tris body); uniform x1.0000 at 3768, -1115` |
| Scale factor | **PASS** — exactly **1.0000** |
| Orientation | **PASS** — both street elevations meet the real streets at the east corner |
| Terrain seating | **PASS** — base y 7.00 m against a LiDAR ground mean of 7.25 m |
| Night glow | **PASS** — the shopfront band lights and wraps the corner; upper storey dark; two skylights faintly lit |
| Draw calls | **PASS** — 91 at the site; 88–145/frame in the headless acceptance run (budget 300) |
| `landmark-streaming-check.mjs` | **PASS** — all 6 checks, **0 failed** across boot / approach / depart / re-approach |
| Fallback drill | **PASS** — one warning, `sf-assets: 592-third failed to load (Unexpected token '<', "<!doctype "...)`; app boots, everything else renders, the site is empty ground inside the exclusion zone (expected for Case B) |
| `npm run lint` / `npm run build` | **PASS** |
| Batch sanity | **PASS** — `git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/` |

### One correction found during the QA

**The camera preset yaw was wrong and the render caught it.** The registry first
carried `yaw: 315`, from the corner-bisector construction done carelessly. App
yaw = 180 − true bearing, and the bisector of the 3rd Street front (45.1°) and
the Brannan front (135.2°) is 90.2°, so the correct value is **`yaw: 90`** —
due east. 315 puts the camera to the south-west, staring at the two blank party
walls: the one angle at which this asset shows nothing it was built for. Fixed
in the registry and in the plan's 2.13.

### Note on the local QA rig

The Browser pane runs with `document.hidden === true`, so `requestAnimationFrame`
never fires and the app's own frame loop does not advance. Everything above was
driven by hand — `SF.rig.update`, `SF.city.update(dt, target, cameraPos, quality)`
and `SF.assets.update(cameraPos, dt)` on a `setInterval` pump — and captured by
rendering into an explicit `WebGLRenderTarget` and reading it back, because
`readPixels` on the default framebuffer returns `INVALID_OPERATION` while the
page is not composited. Two traps worth recording: `city.update` takes a
**quality object**, not a tier name (passing `'high'` makes `quality.nearScale`
undefined, every near-chunk test false, and the city silently never leaves its
core massing tier); and a partially-pumped frame renders stale LOD cross-fade
state that looks like broken geometry but is not. The headless
`landmark-streaming-check.mjs` run is the trustworthy counterpart — it drives a
real Chrome where rendering is continuous.

## Approval

Approved in advance by the owner for this batch run, quoted verbatim:
"I approve everything -- go ahead and do your thing. you dont need to ask for
stage 3 approval. proceed w everything" — 13 August 2026.
