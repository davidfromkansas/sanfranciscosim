# 434 Brannan Street — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` for `docs/asset-plans/434-brannan.md`.
Built 18 August 2026, Blender 5.2.0 LTS, headless.

## Deliverables

| File | What it is |
|---|---|
| `build_434_brannan.py` | deterministic build; re-run to reproduce the GLB exactly |
| `434-brannan.blend` | the authoring scene the export came from |
| `434-brannan.glb` | **the shipping asset** — the stage-4 optimized, meshopt-packed file: 166 KB raw, 93 KB gzipped |
| `optimize/` | stage-4 pass: scripts, stats, A/B renders, `input/434-brannan.glb` (the pre-optimize archive), `REPORT.md` |
| `render_434_brannan.py` | the review rig (re-imports the exported GLB, never the .blend) |
| `validate_434_brannan.py` | fresh-scene contract validation |
| `make_contact_sheet.py` | composes the seven review frames |
| `434-brannan-{north,east,south,west,top,aerial,aerial-night}.png` | review renders |
| `434-brannan-contact-sheet.png` | the sheet |
| `validation.json` | machine-readable contract report |
| `REFERENCE.md` | the research dossier this build was made from |

## Shipped numbers

| | |
|---|---|
| Triangles | **5,872** (cap 9,000) |
| Mesh objects | 12 as shipped (202 as authored; stage 4 joins per material) |
| Draw submeshes | 13 |
| Dimensions | 40.196 x 40.668 x **13.79** m |
| Min Z | 0.0000 |
| XY centre offset | (0.206, −0.205) m |
| Materials | 11 — `Toy_coral`, `Toy_glass`, `Toy_ink`, `Toy_roofd`, `Toy_rust`, `Toy_steel`, `Toy_stone`, `Toy_trim`, plus `Toy_coral_Glow`, `Toy_glass_Glow`, `Toy_trim_Glow` |
| Glow groups | 3 (frieze crown, sash scatter, entry) |
| File | **170,356 B raw / 94,960 B gzip** as shipped (416,948 / 65,450 as authored) |
| Anchor | −122.3954103, 37.7796003 |
| Brannan front heading | 134.8° true (SE) |

The 40 x 40 m axis-aligned bounding box on a 22.70 x 33.85 m building is the
expected consequence of the 45° SoMa heading, not a scale error. The crest
lands on 13.79 m exactly, so the loader's `targetHeightM / measuredHeight`
scale is 1.0.

## Gate 2 — validation

`validation.json`, from a factory-reset Blender importing only the exported GLB:
**overall PASS**, all sixteen checks true — plausible metric dimensions, crest
normalised to target, base at z 0, centred in XY, under budget, no image
textures, no transparency, all materials on contract, no cameras/lights, no
animation/skin/constraints, transforms applied, no negative scales, normals
outward by per-object signed volume **and** by the 31,500-ray visibility test,
no degenerate geometry, no unexpected objects.

## Dossier corrections and decisions made during the build

1. **The plan put the rooftop penthouse "toward the rear and slightly
   southwest". It is toward the rear and to the NORTHEAST.** Converting the
   nadir-measured local position (−3.0, +9.8) into the roof's own u/v frame puts
   it 6.3 m in from the northeast parapet, and re-measuring the aerial against
   the footprint ring independently gives 6.8 m. The plan's §2.9 was corrected
   before the build; §2.7's coordinates were right all along.

2. **The frieze is a salmon ornament on a pale ground, not a salmon panel.** The
   first build made the whole bay head coral with a pale stepped motif on it. It
   read as a red band and was backwards: the photography shows a pale concrete
   panel carrying a dusty-salmon stylised fan. Swapped, and the crown reads
   better for it — the accent is now the motif, not the field.

3. **The pilaster caps had to be pushed well past life to read.** At the plan's
   12.75 m they cleared the 12.40 m coping by 0.35 m and the roofline looked
   flat from the aerial. Raised to **13.05 m** (0.65 m clear), widened from
   `PIL_W + 0.30` to `PIL_W + 0.44`, and given more projection; the parapet
   coping was moved from `Toy_trim` to `Toy_stone` so the lighter caps read
   against it instead of merging into one white rim. This is the plan's one
   sanctioned exaggeration (§2.6) and it is spent here.

4. **The entry could not be modelled as a recess.** There are no booleans in
   this script, so the plan's "reveal recessed 0.50 m" became a solid `Toy_ink`
   prism sunk into the wall — which swallowed the door leaf and the glow shell
   inside itself. The day render still looked plausible; the **night render is
   what caught it**, showing a dead black rectangle where the lit entrance
   should be. Rebuilt as applied panels stacking outward (dark panel → leaf and
   disc → glow shell), which reads as a deep portal from the app's camera and
   actually lights. The circular graphic moved from behind the door (z 2.30) to
   above it (z 3.25), where it is visible.

5. **The Zoe dado was sliced by its own windows.** At the plan's 2.60 m it cut
   the 1.35–3.60 m ground-floor sash in half. Lowered to **1.15 m**, below the
   sills, where it reads as a base course — which is also what the photography
   shows.

6. **The small roof units were invisible.** `Toy_steel` boxes on a `Toy_steel`
   deck disappeared from the nadir view, which is the view this roof exists for.
   Moved to `Toy_stone`. The deck itself stays `Toy_steel` and never
   `Toy_roofd`: 45454a measures rgb(9,9,12) on a deck in the running app.

7. **The rear gained a third window column** (9 openings, not 6). Two columns
   read as a blank wall with a mistake in it; three matches the loose scatter in
   the Zoe Street photography.

8. The **duct run** was shortened from 16 m to 9 m and widened to 0.75 m — at
   16 m x 0.55 m it read as a scratch across the deck rather than as an object.

## Height decision, restated

`targetHeightM` = **13.79 m**, the DataSF LiDAR maximum, modelled as the rooftop
air-handling unit on its kerbed platform. The roof deck is the measured
11.46 m; the parapet crest (12.40 m) and pilaster caps (13.05 m) are inferred
and openly so. Two photogrammetric solves against the Street View panorama
disagreed by 20% and one returned a wall crest below the measured deck; neither
is quoted. See `REFERENCE.md` §3 and the plan's §2.15.

What makes this survivable: the body is normalised to the *measured* deck and
`targetHeightM` is by definition the export's own top, so if 13.79 m turns out to
be the caps rather than the penthouse, the cost is a penthouse about a metre too
tall — never a mis-scaled building.

## Orientation note

Authored in true-world orientation (Blender `+Y` = north, `+X` = east), because
`placeGeneric()` in `app/src/assets.js` scales and positions but never rotates.
The asset contract's "front faces −Y" therefore cannot be honoured literally: the
Brannan front faces **134.8°** true (SE). Real-world orientation wins (AGENTS
rule 5), and this is the deviation the plans README says to record here.

## Render rig note

The review rig defaults to **EEVEE**, not Cycles. This Mac routinely sits at load
100–700 with a dozen concurrent landmark sessions rendering on it; a CPU-Cycles
frame can take minutes or never finish, while the same rig on EEVEE renders in
seconds with shadows, flat materials and the glow layer intact. Nothing gate 2/3
judges — silhouette, massing, the toothed roofline, which surfaces glow — needs
path tracing. `--engine cycles` forces path tracing; the night frame here was
rendered in Cycles at 40 samples because EEVEE's glow read is less trustworthy.
In Blender 5.2 the enum is `BLENDER_EEVEE`, not `BLENDER_EEVEE_NEXT`.

## Gate 4 — optimize

Run 18 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; full write-up
in `optimize/REPORT.md`. 416,948 → **170,356** raw bytes (−59.1%), 202 → 12 mesh
objects, 203 → 13 draw submeshes, triangles unchanged at 5,872, material set
identical. All gates G1–G6 and G8 PASS (G7 n/a, no bake); worst A/B pixel delta
0.055% against a 2%/4% gate; ray-flip fraction 0.0000. The stage-2 contract
validator was re-run against the shipped file and still returns `overall: PASS`.

Two judgment calls worth carrying forward: the limited dissolve was **skipped**
because this asset has two footprint-following coplanar ring bands (parapet and
coping), which is the documented sliver hazard; and the 1 mm weld was **kept**
after a four-variant measurement, because this asset is beveled and the weld cut
vertices by 72% and raw bytes by a further 4.3 KB on top of the join.

## Gate 3 — approval

**Approved 18 August 2026**, on the session's standing instruction, quoted
verbatim: *"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"* (David, opening
message of this session, given alongside `BUILDING: 434 Brannan St, San
Francisco, CA 94107` and `BATCH: yes`). The contact sheet, the day aerial and the
night aerial were presented with the numbers above at the moment of the gate.

This is a standing pre-approval rather than a reaction to the renders. If the
building is later judged wrong, the fix is a stage-2 revision loop logged in this
section, not a retro-justification here.
