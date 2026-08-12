# 543 Presidio Blvd — build report

**What shipped:** a validated miniature GLB of the WWI-era officers' family
residence at 543 Presidio Boulevard, San Francisco — 2,848 triangles, 9 flat
`Toy_*` materials, crest normalised to 9.55 m exactly, all contract gates PASS.

This file beats `docs/asset-plans/543-presidio-blvd.md` wherever they disagree, and
beats `REFERENCE.md` on anything about what was actually built.

| | |
|---|---|
| Slug / manifest id | `543-presidio-blvd` |
| Blender | 5.2.0 LTS |
| Build script | `build_543_presidio_blvd.py` (deterministic; no manual editing) |
| Triangles | **2,848** (plan cap 9,000; contract 27,000; PERF-PLAN hard limit 30,000) |
| Mesh objects | **9** (63 as built; joined per material in stage 4) |
| Dimensions (x, y, z) | **17.197 × 17.727 × 9.550 m** |
| bbox min / max | (−8.599, −8.863, 0.000) / (8.599, 8.863, 9.550) |
| min Z | 0.000 |
| XY centre offset | (0.000, 0.000) |
| Materials | `Toy_brick`, `Toy_glass`, `Toy_glass_Glow`, `Toy_ink`, `Toy_red`, `Toy_stone`, `Toy_trim`, `Toy_trim_Glow`, `Toy_white` |
| Glow materials | `Toy_glass_Glow`, `Toy_trim_Glow` |
| Textures / transparency / cameras / lights / animation | none |
| File size (**shipped**, meshopt) | **87,484 B** raw · 57,162 B gzip |
| File size (as built, pre-optimize) | 184,296 B raw · 30,524 B gzip — archived at `optimize/input/` |
| Draw submeshes | 9 (63 as built) |
| Validation | `validation.json`, overall **PASS** — re-run against the shipped optimized GLB, not the as-built one |

## Dimensions — why the XY box is 17 m for a 13.7 m house

The house is 13.72 m × 12.79 m in plan and sits **11° off the world axes**
(front-wall bearing 190.7° / 10.7° true). The GLB is authored in true-world
orientation, so its *axis-aligned* bounding box is the rotated envelope — 13.72 ×
12.79 m plus 0.62 m of eave overhang on all four sides plus the 1.5 m entry porch,
rotated. 17.197 × 17.727 m is that rotation. It is **not** a scale error, and the
validator's dimension band is written around it with a note to that effect.

The loader scales uniformly by `targetHeightM / measuredHeight`. Since the crest is
normalised to 9.55 m exactly and `targetHeightM` is 9.55, **the expected scale
factor is 1.000**. Anything else at integration time means the manifest and the
asset disagree.

## Anchor

| | |
|---|---|
| Footprint OBB centre (measured) | `−122.4515779, 37.7973711` |
| `recentre()` shift | +0.111 m east, −0.001 m north |
| **Manifest anchor** | **`−122.4515766, 37.7973711`** |

The house is not symmetric about its footprint centre — the entry porch projects
1.5 m past the street wall while the rear carries only the eave — so the XY
bounding-box centre lands 0.111 m east of the footprint centre. The geometry is
shifted so the origin is the bbox centre (contract rule 2) and the *same* shift is
carried into the anchor, which keeps the house on its real footprint (AGENTS rule 5).

## Orientation — a deliberate contract deviation

The contract says "front faces −Y in Blender". This asset's front faces **100.7°
true (ESE)**, onto Presidio Boulevard.

`placeGeneric()` in `app/src/assets.js` scales and positions but never rotates, so
every landmark must be authored in true-world orientation. Where that conflicts
with "front faces −Y", real-world orientation wins — `docs/asset-plans/README.md`
"Orientation note that applies to every plan", and AGENTS rule 5. Recorded here as
required.

Local authoring frame: **u** along the front wall, positive toward the SSW
(bearing 190.7°); **v** across, positive toward the boulevard (bearing 100.7°).
Right-handed, so CCW polygons in (u, v) stay CCW in world (x, y) and normals stay
outward.

## Corrections to the plan

The plan's dossier was a head start, not a citation. Three things changed:

**1. One hip, not two (plan §2.7 items 5–6).** The plan specified a main hip over
the notched block with its ridge along v, plus a lower subordinate hip over the
front wing. Carried at a matched pitch the wing hip's ridge lands at 7.58 m —
entirely swallowed by the main hip, reading as a lump rather than a wing. The built
asset carries **one hip over the full 13.72 × 12.79 m envelope with the ridge along
u**, parallel to the street front, because at the eave line the u span (14.82 m)
exceeds the v span (13.89 m). That is what the aerial imagery shows; it is what a
hipped roof over rectangular framing actually does when a rear corner is recessed
as a porch; and it keeps the roof one legible red shape, which is recognition cue
#1. The notch still reads — as a wall setback on the rear and NNE elevations, and
in the footprint the asset occupies.

**2. Ridge and hip caps added (not in the plan at all).** The first render pass
produced a large blank red pyramid: correct geometry, no identity. Five raised caps
— one ridge, four hips — in the same `Toy_red` as the field are what a clay-tile hip
roof actually has, and they are what makes it read as one from the app's camera. The
line comes from the normal break, not from colour. ~250 triangles for the single
strongest roof cue in the asset. A sixth, smaller cap finishes the porch hip, which
read as a flat red slab from directly above without it.

**3. 19 windows, not 12 (plan §2.7 item 9).** The plan's count left large blank
wall fields on the NNE flank and the rear, visible in the second render pass. Final
count: 5 front, 6 SSW, 4 NNE, 4 rear. Five are lit at night.

## Iterations

| Pass | What the render showed | What changed |
|---|---|---|
| 1 | A bevel groove ran down the centre of the street elevation where two coplanar wall solids met — a crack, from the camera that matters. Roof was a blank red pyramid. Aerial camera framed at 2.15 spans and overflowed the frame on two sides. Chimney read as an orange peg. | Walls rebuilt as **one** closed n-gon prism on the measured six-vertex footprint. Ridge + four hip caps added. Aerial standoff 2.15 → 3.10 spans, pitch 31° → 35°. Chimney section 0.85×0.70 → 1.00×0.82 with a corbelled cap. Eave overhang 0.55 → 0.62, fascia 0.38 → 0.42. |
| 2 | Porch read as a **carport**: 4.6 m wide × 2.0 m deep on 0.4 m sticks, canopy floating halfway up a 7 m wall. Blank wall fields on the NNE flank and the rear. | Porch to 3.6 m × 1.5 m, canopy dropped to 3.30 m (sitting right on the 3.15 m door head), entablature deepened to 0.45 m, posts to 0.46 m square piers, step narrowed. Porch ridge cap added. Windows 17 → 19. |
| 3 | Reviewed: roof reads as tile, porch reads as an entry, night state reads as a house at 9pm. | Shipped. |

Reviewed from the high three-quarter aerial first at every pass, per the style
bible §18 and the pipeline's stage-2 override.

## Night state

Five `Toy_glass_Glow` shells (front upper N, front lower S, SSW upper centre, SSW
lower front, NNE upper rear) spread across **three** elevations, plus a
`Toy_trim_Glow` porch soffit that spills onto the entry. Domestic and sparse — a
house at 9pm, not an office block. A night state confined to one facade would be
invisible from half the app's orbit.

Every glow surface is a thin shell **proud of** the opaque glazing behind it, never
a primary surface: `assets.js` renders `_Glow` in a separate layer at
`0.12 + 0.95 × uNight` opacity, so a primary surface authored as glow would be
12% alpha in daylight. Day colours of both glow materials match their non-glow
palette neighbours (`Toy_glass` / `Toy_trim`).

## Validation (fresh isolated scene, re-imported GLB)

Every check in `validation.json` passes.

| Check | Result |
|---|---|
| metres and plausible dimensions | PASS |
| crest normalised to target (9.55 ± 0.02) | PASS — 9.550 |
| base at z = 0 | PASS — 0.000 |
| centred in XY | PASS — (0.000, 0.000) |
| under triangle budget | PASS — 2,848 / 9,000 |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS — 9 × `Toy_*`, no `Toy_body` |
| no cameras or lights | PASS |
| no animation / skin / constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| **normals outward — signed volume** | PASS — 63 / 63 solids positive, 0 inverted |
| **normals outward — ray test** | PASS — **0 flipped of 31,500 first hits (0.000%)**, tolerance 0.15% |
| no degenerate geometry | PASS — 0 |
| no unexpected objects | PASS |

Re-run against the **shipped** (stage-4 optimized) GLB. Triangles, dimensions,
crest, origin and material set are bit-identical to the as-built asset; only the
object count (63 → 9) and the encoding changed. Stage-4 gates and the gzip
finding are in `optimize/REPORT.md`.

The signed-volume test is the authoritative one for a union of interpenetrating
solids; the 31,500-ray visibility test is the secondary check and came back exactly
zero, which is the right answer for an asset built entirely from closed prisms.

## Renders

All eight depict the exported GLB re-imported into an empty scene, so every image
is the geometry that ships. Elevations share one camera rig — same orthographic
scale, framing, lighting, exposure and projection — differing only in azimuth.
Directions are true compass directions (north = Blender +Y).

`543-presidio-blvd-north.png` · `-east.png` · `-south.png` · `-west.png` ·
`-top.png` · `-aerial.png` · `-aerial-night.png` · `-contact-sheet.png`

The front elevation faces 100.7°, so the **east** view is the near-frontal one.

## Draft manifest entry

Not applied here — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md`, Case B).

```json
{
  "id": "543-presidio-blvd",
  "file": "543-presidio-blvd.glb",
  "anchor": [-122.4515766, 37.7973711],
  "targetHeightM": 9.55,
  "cat": 1,
  "name": "543 Presidio Blvd",
  "estimated": true,
  "dims": [17.1972, 17.7268, 9.55],
  "tris": 2848,
  "loadRadius": 2500
}
```

- `cat: 1` = House (`CATEGORY_LABELS`, `app/src/context.js`).
- `estimated: true` — the anchor and the 9.55 m crest are measured, but the
  eave/ridge split is inferred (REFERENCE §4).
- **Streaming decision (mandatory, PERF-PLAN #3):** `loadRadius: 2500`, the default
  rule `max(2500, 9.55 × 30)`. `alwaysLoaded` would be absurd for a 9.5 m house.
  Beyond the radius the stand-in is the baked procedural building — which for
  Case B is carved out by the exclusion zone, so the site reads as empty ground at
  range. At 2,500 m a 9.5 m house is sub-pixel and that absence is illegible.

## OUTSTANDING: the Case B tile re-bake is NOT in this branch

Everything else shipped. The tile re-bake did not, and this is a real, visible
defect until it does: **the baked procedural house still stands on 543's
footprint, so it intersects the GLB.** The registry entry that excludes it is
committed; only the regenerated tiles are missing.

Why it was held back rather than shipped:

The re-bake was run, verified, and then deliberately discarded. `pipeline/data/`
is a gitignored download cache, and the cache on this machine is a **different
data vintage** from the one that produced `origin/main`'s committed tiles. The
control run proves it: re-baking with main's *exact* registry config — no 543
entry at all, nothing changed — still produced **523 building tiles differing
from main's**, at an identical building count of 174,770. Shipping those tiles
would have silently replaced the Chase Center branch's bake with a different
snapshot of DataSF and Overture, under a commit message about one house.

What the re-bake looked like when it ran against a self-consistent baseline
(recorded here so the numbers are known good):

- buildings 174,770 → 174,769 — the procedural footprint on 543's site is
  dropped and **nothing else**; 541 and 545 both survive
- `node pipeline/audit.mjs` check 1.6 goes from 28 to 29 landmarks clear
- only cell `13_9` loses a pick box (21 → 20)
- the ~580 changed `ctx/*.json` sidecars are mechanical: baked building ids are
  sequential indices, so removing one shifts every later id down by exactly 1.
  Sampling 25 cells gave an id-delta histogram of `{0: 2633, -1: 3468}` and no
  other value.

To finish it, on top of current `main` and with a fresh cache:

```bash
cd pipeline && npm install
npm run download && npm run loredata
node buildings.mjs && node validate.mjs && node lore.mjs \
  && node toy.mjs && node notables.mjs && node context.mjs
node audit.mjs   # check 1.6 must read "29 landmarks clear"
```

`lore.mjs` alone takes ~3 min and the chain ~12 min. Run `lore` **before** `toy`
or `context.mjs` fails with `every building has a pick box and an identity`.

## Integration notes (Case B)

No `543-presidio-blvd` id exists in `pipeline/lib/landmarks.mjs` or
`app/src/landmarks.js`. Integration needs a registry entry plus a tile re-bake.

**The exclusion radius is the one thing to get right.** 541 and 545 Presidio Blvd
sit roughly 7 m from this footprint — closer than any subject in this set so far. A
careless radius deletes the neighbours from the baked city. The plan suggests ~11 m;
verify visually against the re-baked tile and against `node pipeline/audit.mjs`
check 1.6 before shipping.

## What is deliberately not in the asset

The detached garage (a separate DataSF footprint), the terraced lawn, the retaining
wall and its stair, Presidio Boulevard, the neighbouring houses, all planting,
vehicles, people, display plinths, cameras and lights. The raised basement band
**is** part of the building and hides the terrain seam.
