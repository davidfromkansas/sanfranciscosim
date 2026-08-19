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

## Gate 5 — local integration QA (stage 5, batch mode)

Run 18 August 2026 per `docs/asset-plans/INTEGRATION-PROMPT.md` Steps 1–6, with
Step 7 replaced by the pipeline's stop-and-ask. Case **B** (new landmark).

### What changed

| File | Change |
|---|---|
| `app/public/sf-assets/landmarks/434-brannan.glb` | the shipped asset, byte-identical to `artifacts/434-brannan/434-brannan.glb` |
| `app/public/sf-assets/landmarks_manifest.json` | one 19-line entry appended **as text** — a `JSON.parse`/`stringify` round trip rewrites unrelated `targetHeightM` values such as `11.0` → `11` across other landmarks |
| `pipeline/lib/landmarks.mjs` | `434Brannan` registry entry, `exclude: 10`, camera `{240, 45, 26}`, with the measurement that sized the radius in the comment above it |

`camelId('434-brannan')` → `434Brannan`, which is the registry id — verified, not
assumed, because a mismatch shows up as two buildings rather than as an error.

`loadRadius`: **2500 m**, the default rule `max(2500, 13.79 × 30)`. Streamed, not
resident. Past the radius this site is empty ground rather than a stand-in
building (Case B), and 2.5 km is far enough that the absence is illegible.

`estimated: true`, because the crest is the LiDAR maximum and the parapet is
inferred — 33 of the 91 manifest entries already carry the flag for the same
reason.

### Step 1 — re-validation of the shipped file

`validate_434_brannan.py` re-run against the **optimized** GLB in a factory-reset
Blender: `overall PASS`, all sixteen checks, 5,872 tris, 40.196 × 40.668 ×
13.79 m, min Z 0.0, XY offset (0.206, −0.205), 11 `Toy_*` materials with three
`_Glow`, 12 objects.

### Step 4 — Case B bake

Full chain run in this worktree: `terrain → bridges → buildings → streets →
landcover → validate → lore → toy → notables → context → muni-shapes`
(`buildings` and `lore` under `--max-old-space-size=12288`; `muni-shapes` no-ops
without a 511 key and leaves the committed file alone). 174,695 buildings baked
into 585 cells.

| Check | Result |
|---|---|
| `pipeline/audit.mjs` 1.6 — no procedural footprint inside a bespoke exclusion zone | **PASS** — 100 zones over 97 landmarks clear |
| `pipeline/verify-rebake.mjs` | **PASS** — 584 of 585 cells unchanged; `23_13` 182 → 181; nearest surviving footprint 12.4 m against a 10 m radius |
| tile decode, near tier `buildings/23_13.bin` | 1 neighbour vertex on the GLB footprint boundary, **0.00 m** inside |
| tile decode, `toy/23_13.bin` | same vertex, **0.24 m** inside |

That 0.24 m is the shared party-wall vertex with 426 Brannan plus tile
quantisation (`QUANT` 0.02 m). It is unavoidable and documented: the two
footprints share that node exactly, so no radius can clear ours without eating
the neighbour — the same geometry that made the safe band 8.11 < r < 12.00 in the
first place. 0.24 m is well inside the modelled wall thickness.

Three audit checks fail and all three are pre-existing global data properties,
untouched by this landmark: 1.2b (p95 height 13.9 m — the DataSF source's own
p95 is 12.4 m), 1.3c (Telegraph Hill 90.5 m from the Terrarium DEM against a
surveyed 84 m), 1.7b (1 of 792 sampled trees more than 30 m offshore).

### Steps 5 and 6 — local QA

Driven through the **built** `app/dist` in real headless Chrome over CDP
(`artifacts/434-brannan/qa_local.mjs`), not the editor's browser pane: parallel
landmark sessions hold the preview slots, and a hidden pane throttles
`requestAnimationFrame` so hard that a healthy streamed landmark looks broken.

| Check | Result |
|---|---|
| manifest entry loads | **PASS** — `sf-assets: 434-brannan merged 13 objects / 11 materials -> batched (3425 tris body); uniform x1.0000 at 3704, -1061` |
| uniform scale ≈ 1.0 | **PASS** — exactly `x1.0000`; the authored crest and `targetHeightM` agree |
| exactly one building on the site | **PASS** — no procedural twin, no baked block through the walls, no z-fighting (`qa/day.png`) |
| orientation | **PASS** — the dressed Brannan front faces Brannan; the plain Zoe flank runs down Zoe |
| terrain seating | **PASS** — no float, no sink |
| night glow | **PASS** — the five frieze panels read as a salmon crown, ~10 sash panes and the entry light, nothing else (`qa/night.png`) |
| draw calls | **PASS** — 96/frame averaged over 30 frames, against a 300 budget |
| asset warnings | **PASS** — none. All 85 landmarks in range merged and batched; nothing was dropped from the shared `BatchedMesh` |
| wide shot | **PASS** — `qa/wide.png`, no holes or artifacts in the district |

The QA run itself is committed as `artifacts/434-brannan/qa_local.mjs` with its
output in `artifacts/434-brannan/qa/`.

### Step 6 — fallback drill (mandatory)

Run by serving a real **404** for `/sf-assets/landmarks/434-brannan.glb` rather
than renaming the file: Vite and the dist server both answer a missing public
path with `index.html` and HTTP 200, so the rename trick the prompt describes
cannot produce a fetch failure at all.

**Empirically confirmed (twice):** with the GLB returning 404, the app boots, the
district renders, every neighbour is present, and the site itself is **empty
ground inside the exclusion zone** — `qa/drill-day.png` and `qa/drill-night.png`.
That is the documented Case B outcome, not a bug: there is no procedural version
of this building to fall back to, which is exactly why the exclusion radius had
to be measured rather than guessed.

**Not empirically confirmed: the console line itself.** The assertion pass of the
drill was attempted four times and never completed — the machine sat at load
**400–620** for the whole window (a dozen parallel landmark sessions, five
concurrent Blender processes), and under SwiftShader the app's throttled
streaming scan left the entry `far` past a 600 s budget. The two screenshots above
come from the one run that got through before load climbed. Rather than keep
waiting, the harness was hardened for the next attempt (`until` budget raised to
600 s; an `SF.assets.update(camera, 0.4)` pump added, which is the documented fix
for a throttled scan) and the run is reproducible in one command:

```
node artifacts/434-brannan/qa_local.mjs --drill
```

**What the code guarantees, by reading rather than by observation.**
`INTEGRATION-PROMPT` Step 6 says to expect exactly one
`... — keeping the code-built landmark` warning. **That wording describes the
RESIDENT path only.** This entry has a `loadRadius`, so it is streamed, and a
streamed failure goes through `scan()` in `app/src/assets.js` (line 560), which
deliberately does *not* use the single-shot `warn()` helper and emits
`sf-assets: 434-brannan failed to load (<reason>)` with no "keeping" suffix — the
comment there says why. It is still exactly once: `place()` sets
`state.status = 'failed'`, and no branch in `scan()` matches `'failed'`, so the
entry can never be retried or re-warned. The harness's filter matches on the
asset id rather than on the prompt's wording, which is the correct test.

This is a partial PASS and it is recorded as one. If the reviewer wants the
console line in a log before shipping, re-run the command above on an idle
machine.

### Batch mode — what is committed

`BATCH: yes`, so per `ADDRESS-TO-ASSET.md` the bake was run and QA'd and then
**discarded** before committing:

```
git checkout -- app/public/tiles api/_data
```

586 generated files changed in the bake and none of them are committed here. The
branch carries source only — the GLB, the manifest entry, the registry entry, the
asset plan and `artifacts/434-brannan/` — all of which are append-only and merge
mechanically. `git diff --name-only origin/main` lists nothing under
`app/public/tiles/` or `api/_data/`. The city gets rebaked once for the whole
batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

`npm run lint` and `npm run build` in `app/` both clean.

### Gate 5 — PASS table

| # | Item | Result |
|---|---|---|
| 1 | shipped GLB re-validated against the contract | PASS |
| 2 | asset dropped in, byte-identical | PASS |
| 3 | manifest entry, appended as text, no collateral edits | PASS |
| 4a | registry entry, `exclude` measured against both bake sources | PASS |
| 4b | re-bake; `audit.mjs` 1.6 | PASS |
| 4c | `verify-rebake.mjs` | PASS |
| 5a | merge line, uniform scale 1.0000 | PASS |
| 5b | one building, orientation, terrain seating | PASS |
| 5c | night glow restrained to the intended surfaces | PASS |
| 5d | draw calls 96 < 300 | PASS |
| 5e | no asset warnings, nothing dropped from the shared batch | PASS |
| 6 | fallback drill — boot and render with the GLB missing | PASS |
| 6 | fallback drill — the console line captured in a log | **NOT CONFIRMED** (machine at load 400–620; see above) |
| 7 | `npm run lint`, `npm run build` | PASS |
| — | batch sanity: nothing under `app/public/tiles/` or `api/_data/` | PASS |

### Gate 5 — ship decision

Pending. Nothing has been pushed, no PR opened, no deploy run. The one
outstanding item is the drill's console line, which is one command on an idle
machine.
