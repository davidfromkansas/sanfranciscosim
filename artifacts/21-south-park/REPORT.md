# 21–29 South Park — build report

Asset: `artifacts/21-south-park/21-south-park.glb`
Plan: `docs/asset-plans/21-south-park.md`
Dossier: `REFERENCE.md` (which beats the plan wherever they disagree)

## 1. Shipped numbers

| | |
|---|---|
| Triangles | **8,664** (cap 9,000) |
| Objects | **9** after the stage-4 join (130 as authored), all positive-volume |
| Dimensions (AABB) | **47.361 × 51.493 × 11.730 m** |
| Oriented footprint | 32.749 × 40.676 m, 1,115.1 m² |
| `min Z` | 0.000 |
| XY centre offset | (−0.336, +0.132) m — cornice and bulkhead overhang; the footprint itself centres to (0.003, −0.005) |
| Crest | **11.730 m**, the stair/lift bulkhead — loader scale lands on 1.0 |
| Cornice crest | 10.20 m; roof deck 9.50 m |
| File | **236,856 bytes** shipped (pre-optimize 504,136; see `optimize/REPORT.md`) |
| Materials | 9, all `Toy_*`, flat, opaque, no textures, no `Toy_body` |
| Glow materials | `Toy_mustard_Glow`, `Toy_glassl_Glow` |
| Validation | `validation.json` — **overall PASS**, all 16 checks true |
| Normals | per-object signed volume clean on all 9 shipped objects; 31,500 visibility rays, **0.0 %** flipped; `invalid_or_nonunit_loop_normal_count: 0` |
| Anchor | −122.3931063, 37.7817676 |
| Front headings | 315.7° (main plane) and 286.7° (angled plane) |

## 2. Corrections and decisions made against the plan

**2.1 The anchor is the footprint's world-AABB centre, not the OBB centre.** The plan
already called this out and the build confirms why it matters: the OBB centre sits 2.63 m
from the AABB centre on this skewed quadrilateral, and anchoring there would have placed
the building 2.63 m west of its real footprint. Centred on the AABB centre the footprint's
own XY centre lands on (0.003, −0.005) m. This is a deliberate departure from the habit of
the nineteen neighbouring South Park plans and it is recorded in the registry comment as
well, so it does not get "fixed" later.

**2.2 Bay and window counts were kept at the plan's numbers, and they remain the softest
part of the asset.** Re-counting from the January 2025 panos did not settle them: the
crape myrtles in front of the building cut the frontage into fragments and the oblique
angle makes the far plane foreshorten badly. Shipped: **four loft bays + five arches** on
the 19.69 m main plane, **one loft bay + freight doors + office entrance + three arches**
on the 12.07 m angled plane. Spacing is regular (4.45 m bay centres, 3.55 m and 3.30 m
arch centres), which is the part the evidence actually supports. If a better photograph
settles the count, only the constants at the top of `build_21_south_park.py` change.

**2.3 The spandrel ribs were cut from three to one, and drawn PALE.** The plan asked for
three ribs in the sash colour. The first render showed three 0.05 m ribs merging into one
bright line at diorama distance, and same-colour relief vanishing entirely. Shipped: one
0.12 m rib in `Toy_stone` across a dark `Toy_sash` panel. This is a semantic
exaggeration — the real panels are relief in one colour — justified because the ornament
reads as light-on-dark in the photography and because the alternative is a blank dark
band.

**2.4 The roof deck is `Toy_steel`, not `Toy_stone`.** The plan specified a pale deck with
a darker coping. Rendered, that gave a 1,115 m² pale field indistinguishable from the
white walls, with no parapet ring at all from directly above — which is the view the app's
camera uses most. Inverted: a **grey membrane deck** (`Toy_steel`) with a **pale coping**
(`Toy_stone`) and **dark plant** (`Toy_roofd`). This is also the more truthful reading —
the real membrane is grey and the walls are painted white — and the top render now
resolves the bent outline, the empty apron and the equipment field in that order.

**2.5 The roof plant was enlarged and respread.** The first pass put four clusters of
1.30 × 0.90 m units in the rear third; from the aerial they read as specks on an empty
plane. Shipped: **seven clusters of four 2.05 × 1.45 × 0.95 m units**, a 17.5 m duct run,
a 3.4 × 2.6 m plant housing, three vents and the bulkhead, spread across the whole field
behind the apron. The apron itself (everything within ~13 m of the front wall) is kept
clear, which is what the Esri nadir shows and what keeps the cornice edge legible from
above. `build_21_south_park.py`'s `report()` runs a point-in-polygon test on every roof
object against the footprint inset 0.9 m and prints any stray; it prints `none`.

**2.6 Window reveals: the frame/fill depth relationship was reverted to the reference
implementation.** An intermediate build set the frames proud (0.11) and the glass behind
them (0.05) to fake a real recess. Because `face_panel` builds a solid prism of the whole
opening profile, this buried the glazing completely and every opening rendered as a flat
teal slab. Shipped: the `102-south-park` relationship — frame plane at 0.09, fill inset in
u/z and proud at 0.15 — which reads as a border ring around the opening. A true recessed
reveal would need the frame built as four boxes rather than one panel; that is a
~1,200-triangle change and was not worth it at this scale.

**2.7 The glow shells are wide, short bands rather than window-filling panels.** A closed
`_Glow` shell presents **two** blended layers to the daytime camera, not one, so a shell
covering the whole pane tints it visibly by day — the first night pass looked right and
the day pass showed muddy purple-brown rectangles where mustard sat over navy. Shipped: a
band inset 0.28 m horizontally and 0.45/0.35 m vertically inside the glazing, which is
still unmistakably a lit interior at night and confines the daytime tint to a strip.

**2.9 The roof bulkhead z-fought, and only the app showed it.** The bulkhead box and its
pale cap were both authored to `Z_BULKHEAD` = 11.73, leaving two coplanar top faces. The
Blender review rig rendered it as a clean cap; the app's own aerial camera rendered a
mottled dark-and-pale patch on the roof. Fixed by stopping the box at 11.59 and letting
the cap own the top 0.22 m. **This is the argument for stage 5's local QA being a real
gate and not a formality** — a coplanar-face defect is invisible to a validator that only
checks volumes and normals, and invisible to a renderer that resolves depth differently.
The day glow band was also halved in the same pass, because the app's `_Glow` day layer
(a closed shell is two blended layers) tinted more of the glazing than the rig suggested.

**2.8 No terrain drape.** The site falls 1.49 m across the footprint (DataSF `gnd_min`
11.96 m, `gnd_max` 13.45 m). That is small enough for `placeGeneric()`'s single elevation
sample, unlike `64-south-park` next door which falls 6.11 m and had to be draped. `min_z`
is therefore a normal 0.0 and `targetHeightM` is a real height, not a vertical extent.

## 3. Contract deviations, declared

- **`Toy_sash` (`#2f4f49`) is off-palette.** The observed joinery is a very dark
  blue-green; the palette's nearest keys are `Toy_roofd` (`#45454a`, neutral dark grey) and
  `Toy_navy` (`#2c4a70`, distinctly blue), and neither is the colour. The joinery is the
  second-strongest identity cue after the bend, so it gets its own key. Off-palette is a
  WARN in `sf-asset-check`, not a FAIL, and the validator's
  `materials_follow_contract` check (which tests the `Toy_` prefix and the `Toy_body`
  exclusion) passes. **Watch this one at stage 5**: dark values that look right in the
  Blender rig can render near-black in the app's lighting. If that happens, lighten toward
  `#375a53` rather than switching to `Toy_roofd` — the tint is the point.
- **"Front faces −Y" is not honoured**, and cannot be: the building is at a ~46° heading
  and has two front planes. Real-world orientation wins (AGENTS rule 5). The substitute
  assertions are the measured outward normals, 315.7° and 286.7°, printed by the build and
  recorded in `validation.json`.
- **The axis-aligned bbox is 47.4 × 51.5 m for a 32.7 × 40.7 m building.** Expected
  consequence of the heading, not a scale error; the validator asserts the AABB range
  explicitly so it cannot be mistaken for one.

## 3b. Stage 4 — optimize

`optimize/REPORT.md` has the full record. Summary: 504,136 → **236,856 bytes**
(−53.0 %), 130 → **9** draw submeshes, triangles and bounding box unchanged, all eight
gates PASS, and the stage-2 contract validator re-run on the shipped packed file still
reports **overall PASS** with zero invalid loop normals. The limited-dissolve step was
deliberately skipped — this asset has four coplanar ring bands and that step is the one
that can manufacture invisible slivers (the `350-brannan` failure).

## 3c. Stage 5 — local integration QA (batch mode)

`app/public/sf-assets/landmarks/21-south-park.glb` + one appended manifest entry + one
`pipeline/lib/landmarks.mjs` entry (`21SouthPark`, `exclude: 16`). Case B, so the tiles
were re-baked, QA'd on the bake, and then **thrown away** — this branch carries source
only, per `docs/asset-pipeline/ADDRESS-TO-ASSET.md` batch mode.

| Check | Result | Evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | `validate_21_south_park.py` overall PASS, 16/16 checks, 0 invalid loop normals |
| Manifest entry | **PASS** | appended as TEXT (never `JSON.stringify` — that rewrites `11.0` to `11` across unrelated entries); `git diff` is +19 lines, nothing else touched |
| id mapping | **PASS** | `camelId('21-south-park')` = `21SouthPark`, which is the registry id |
| Registry + re-bake | **PASS** | full chain terrain→…→context→muni-shapes; `validate` logs `landmark in extent: 21-29 South Park — cell 23_13` |
| Audit 1.6 | **PASS** | `no procedural footprint inside a bespoke landmark exclusion zone — 83 zones over 80 landmarks clear` |
| Re-bake blast radius | **PASS** | `verify-rebake.mjs`: 584 of 585 cells unchanged; `23_13 201 -> 200 <- 21SouthPark`; nearest surviving footprint **18.8 m vs the 16 m radius** (12.8 m tall) |
| Single building, no twin | **PASS** | `qa-local-day.png` — one building on the site, no procedural block, no z-fighting |
| Scale factor | **PASS** | `sf-assets: 21-south-park merged 9 objects / 9 materials -> batched (5050 tris body); uniform x1.0000 at 3906, -1301` |
| Orientation | **PASS** | the bend faces the park at the Second Street end, the long plane runs south-west — the mirror check holds in the app, not just the rig |
| Terrain seating | **PASS** | placed at sampled elevation 12.38 m (DataSF `gnd_mean` 12.58 m); no float, no sink |
| Night glow | **PASS** | `qa-local-night.png` — warm bands in the loft bays bending round the corner, three cool second-floor windows, everything else dark |
| Draw calls | **PASS** | **96 peak scene-pass calls** at street level on the oval, against the 300 budget. Measured by wrapping `renderer.render` and sampling `info.render.calls` AFTER each pass — sampling inside rAF reads 1, because the counter resets at the start of a frame |
| Console 404s | **PASS** | the only 404s are `/api/flights`, `/api/weather`, `/api/satfog`, `/api/muni`, `/api/ferries` — expected with no Vercel functions behind a static server. **Zero tile or asset 404s** |
| Fallback drill | **PASS** | GLB renamed → app boots, area renders, **exactly one** warning (`sf-assets: 21-south-park failed to load ... 404`), site is bare ground inside the exclusion zone (expected for Case B). `qa-local-fallback.png` |
| Lint / build | **PASS** | `npm run lint` clean; `npm run build` — 26/26 tests pass, 3,315 tiles compressed |
| Batch-mode sanity | **PASS** | `git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/` |

**One defect was found by this stage and fixed** (§2.9). **Two pre-existing conditions were
observed and are NOT caused by this landmark** (§3c-notes).

### 3c-notes — observed, not ours

- `GL_INVALID_OPERATION: glDrawArraysInstanced: Vertex buffer is not big enough for the
  draw call` appears in the console. It is **still there with this landmark's GLB removed**
  (confirmed during the fallback drill), so it is pre-existing and belongs to an instanced
  subsystem, not to this asset.
- `pipeline/audit.mjs` reports three FAILs — 1.2b (p95 height 13.9 m vs a 25–120 m band),
  1.3c (Telegraph Hill terrain 90.5 m vs 60–85 m), 1.7b (1 of 792 sampled trees offshore).
  All three are city-wide terrain/DEM/source-data checks with no relationship to a single
  South Park footprint. **1.6, the check this integration owns, passes.**

### The local QA environment, for whoever runs this next

The Browser pane was out of dev-server slots (5 of 5 held by sibling sessions), and a
hidden pane stops `requestAnimationFrame`, which stalls landmark streaming — `assets.update()`
never runs, so only the 18 always-loaded landmarks ever place and the canvas stays black.
The QA above was therefore run against the **built** app (`app/dist`, served statically on
:5021) in **headless Chrome over CDP**. That path renders, streams and reports normally.

## 4. Reproduce

```
blender -b --python build_21_south_park.py
blender -b --python render_21_south_park.py -- --samples 128
blender -b --python render_21_south_park.py -- --night --samples 128
python3 make_contact_sheet.py
blender -b --python validate_21_south_park.py
```

The build is deterministic — no random numbers, no interactive modelling. The renders are
EEVEE at 128 samples (`--engine CYCLES` reproduces in Cycles); these materials are flat,
untextured and opaque, so the two engines are visually equivalent here.

## 5. Review renders

`21-south-park-{north,east,south,west,top,aerial,aerial-night}.png` and
`21-south-park-contact-sheet.png`, all regenerated from the final export. The four
elevations share one rig — same orthographic scale, framing, lighting, exposure and
projection — and differ only in azimuth. The aerial stands at bearing 300° because that is
the only informative eye: the two front planes face 315.7° and 286.7° and every other side
is a party wall, so standing square on either normal collapses the other plane and the
bend with it.

## 6. Approval

Standing approval given by David in the session prompt, 16 August 2026, verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

The contact sheet, the day aerial and the night aerial were presented at the stage-3 gate
with the numbers above before the pipeline advanced. No revision round was requested.

## 7. Draft manifest entry

```json
{
  "id": "21-south-park",
  "file": "21-south-park.glb",
  "anchor": [-122.3931063, 37.7817676],
  "targetHeightM": 11.73,
  "cat": 3,
  "name": "21-29 South Park",
  "estimated": true,
  "dims": [47.3614, 51.4933, 11.73],
  "tris": 8664,
  "loadRadius": 2500
}
```

`estimated: true` because the crest is a LiDAR maximum *interpreted* as a bulkhead and the
cornice line is read off photographs. `cat: 3` is Office — what the building has been since
1991 and what every permit since then calls it; the assessor's "Industrial" describes 1919.
`dims` and `tris` are the shipped, post-optimize figures — the stage-4 pass changed
neither (130 objects joined to 9, 504,136 → 236,856 bytes, geometry untouched).
