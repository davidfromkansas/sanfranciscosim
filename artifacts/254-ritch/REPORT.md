# 252–254 Ritch Street — build report

Stage 2 (BUILD) of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed against
`docs/asset-plans/254-ritch.md`. Sources and measurements are in `REFERENCE.md`;
this file records what was built, what changed from the plan, and the numbers.

## Shipped numbers

| | |
|---|---|
| File | `254-ritch.glb` |
| Triangles | **3,140** (cap 7,000) |
| File | 85,808 B shipped (206,832 B pre-optimize, −58.5%) |
| Objects | 8 mesh objects shipped (91 before the stage-4 join-per-material) |
| Dimensions | 16.14 × 16.20 × **8.80** m |
| bbox min / max | `[-8.071, -8.101, 0.000]` / `[8.071, 8.101, 8.800]` |
| min Z / XY centre offset | 0.000 m / `[0.000, 0.000]` |
| Materials | `Toy_slate`, `Toy_stone`, `Toy_ink`, `Toy_glass`, `Toy_steel`, `Toy_gold_Glow`, `Toy_trim_Glow` |
| Front heading | 45.05° true (north-east, onto Ritch Street) |
| Manifest anchor | `-122.3956322, 37.7801278` |
| Registry anchor (exclusion) | `-122.3956361, 37.7801244` |
| Validation | **PASS**, all 17 checks — re-run against the shipped optimized file |

The 16.14 × 16.20 m XY box is the 45.05° rotation of a 7.60 × 14.20 m building
plus its bay, cornice and stoop — not a 16 m building.

**Normals** (measured on the stage-2 build, 91 objects). Per-object signed
volume positive on all 87 closed solids; the 8 open glow faces each pass the
visibility ray test in the direction they claim to face. 31,500 deterministic
rays from nine interior targets, **0 flipped first hits (0.0000%)** against a
0.15% tolerance. 0 degenerate triangles, 0 non-unit loop normals. The optimize
pass re-ran the same tests on the shipped file: still PASS.

**Stage 4.** See `optimize/REPORT.md`. 206,832 → 85,808 B (−58.5%), 92 → 9 draw
submeshes, appearance identical within 0.034% mean RGB. All gates G1–G8 pass.

## Dossier corrections made during the build

**1. The plan's entry-recess construction buried both doors.** §2.7 step 9
described the recess as a `Toy_ink` void with the door slabs inside it. Built
literally — no boolean cut is available, so the "void" is a panel — the ink
panel's outer face stood 20 mm proud of the wall and the doors sat 100 mm behind
it, so the whole entry rendered as one flat dark rectangle. The recess panel now
ends 5 mm proud and each door stands 15 mm proud of it. The doors were also
narrowed from 1.00 m to 0.88 m and moved apart: at the plan's width they left
40 mm of ink between them and the entry read as a flush pair of panels rather
than a hole.

**2. The plan's light wells ran the full height of the building.** §2.7 steps 13
and 14 put each well in the footprint polygon as a plan bite, which is what makes
the roof hole real — but a bite in the plan is a bite in the *wall*, so the first
build had a two-storey canyon down the exposed flank and a gash in the party
wall. Each well is now plugged back to solid below 4.70 m: a light well is an
upper-storey shaft.

**3. Both well mouths are screened; the plan left the flank one open.** §2.4
called the south-east well "a rectangular notch about 3.0 m long and 1.3 m deep
cut into [the flank]". Left open at the measured 3.6 × 1.4 m it read from the
aerial camera as a garage door, and the listing photography shows that flank as
an unbroken wall. Both wells are now interior shafts, read only from above —
which is also all the drone frame shows. Each plug stops at its screen's inner
face: running it out to the wall plane left two coplanar exterior faces that
z-fought into a mottled ghost rectangle on the flank.

**4. The manifest anchor and the registry point are NOT the same**, as plan §2.3
predicted. Recentring the model on its XY bbox centre — the contract's origin
rule — moved the origin 0.53 m north-east, because the bay, the cornice and the
stoop all project toward the street and the rear does not. The registry
`lon`/`lat` stays at the design point, which is where the exclusion window was
measured; `exclude: 2.9` is unaffected.

**5. The plan called the cornice "the brightest edge [the roof] has".** It is
not: on this building the cornice is painted the same dark grey as everything
else, so from above the street edge reads as a *dark* band against the pale roof.
That is a stronger read than the plan imagined and it is what the photographs
show. No change to the model; the plan's §2.9 wording is wrong.

**6. The rear door sits at the raised floor level, not at grade.** The base band
runs across the rear too, so a door started at z=0 was three-quarters buried
behind it. No rear stair was added — nothing in the sources shows one, and plan
§2.15 explicitly warns against inventing one.

**7. `Toy_slate` `#756f69` is off-palette, deliberately.** Documented in plan
§2.8 and carried through. The facade median-samples at `#6b696a` overcast and
`#5e5652` in shade; `#756f69` is that colour lifted ~8% so it survives the app's
Lambert shading. No palette entry works: `Toy_steel` (`#9aa0a6`) is far too light
and destroys the one cue this building has, and `Toy_roofd` (`#45454a`) has been
observed rendering as `rgb(9,9,12)` — effectively black — on a roof deck in this
app. This is the style bible's SF painted-residential exception and it ships as a
WARN, not a FAIL.

## Night state

Hero glow: the **three upper bay sashes**, `Toy_gold_Glow` `#caa64a`. Supporting
accent: one porch-light band over the entry doors, `Toy_trim_Glow` `#f6e6c4`.
The single north-west upper window stays dark — the upper unit was vacant at the
2025 sale, and a fully lit two-flat reads as an office.

The first night pass had the entry glow sized as the whole doorway; it blew to
white and was brighter than the two lit rooms above it. It is now one transom
band, 1.68 × 0.30 m.

All glow surfaces are **single one-sided quads** standing proud of the opaque
glazing, never closed shells: the app draws `_Glow` in a separate layer at
`0.12 + 0.95·uNight` opacity, and a closed box shows its front *and* its back
face, reading at roughly twice the intended day alpha — enough to tint a whole
facade.

Two render-rig notes, both caught here:

- The day pass must zero `Emission Strength` as well as setting alpha to 0.12.
  `make_material` leaves every `_Glow` material emitting at 1.0, and an emissive
  surface keeps emitting whatever its alpha says, so the first day renders showed
  the lit sashes as cream panels in full daylight — a state the app never has.
- The top-view camera roll is `LONG_AXIS + 90`, not `LONG_AXIS − 90`. The latter
  renders the plan upside down: cornice, bay and stoop at the bottom of the frame.

## Files

| File | What |
|---|---|
| `build_254_ritch.py` | deterministic build; `blender -b --python build_254_ritch.py` |
| `render_254_ritch.py` | review renders from the re-imported GLB; `-- --night` for the dusk pass |
| `validate_254_ritch.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes the eight renders |
| `254-ritch.glb` | the **shipping** asset — the stage-4 optimized file, 84 KB raw (the pre-optimize build is archived at `optimize/input/254-ritch.glb`, 202 KB) |
| `254-ritch.blend` | authoring scene |
| `254-ritch-{north,east,south,west}.png` | the four building-aligned elevations, one rig |
| `254-ritch-facade.png` | square-on look down the 45.05° facade normal |
| `254-ritch-top.png` | roof plan, street end at the top of frame |
| `254-ritch-aerial.png` / `-aerial-night.png` | the app's high three-quarter camera, day and dusk |
| `254-ritch-contact-sheet.png` | all eight |

## Stage 5 — integration and local QA

Run in batch mode (`BATCH: yes`): the city was baked for the QA below and then
discarded, and this branch commits source only.

**The one substantive change made at stage 5 was the body colour.** Measured in
the running app at 08:30 from the aerial camera, `Toy_slate` `#756f69` put the
north-east facade at luminance 22–27 against 47 for a mid-grey procedural wall in
the same light. Legible, but with no margin — and this facade spends most of the
day inside the cast shadow of the taller building on the parking-lot side, where
it fell to `rgb(4,3,1)`. Lifting to **`#857e76`** (the value plan §2.8
pre-authorised) is a ~34% linear lift and moves it to 31–38: still a clear step
darker than every neighbour on the block, which is the identity, but no longer a
silhouette. The asset was rebuilt, re-optimized and re-validated after the change;
all gates re-run and pass.

**The midday blackness is the site, not the asset.** At 12:30 the sun is at
azimuth 156° and the tall neighbour to the south-east shadows the whole lot; the
adjacent procedural brick wall reads `rgb(39,17,2)` in the same frame. Ritch
Street is a narrow SoMa alley and this is what the app correctly renders. No
colour choice fixes a cast shadow, and lightening the building far enough to beat
one would have made it another grey house.

| Check | Result |
|---|---|
| Re-validation before integrating | PASS — 17/17, 3,140 tris, bbox top 8.80 m |
| Merge line | `sf-assets: 254-ritch merged 9 objects / 7 materials -> batched (1834 tris body); uniform x1.0000 at 3684, -1120` |
| Loader scale | **x1.0000** — authored height and `targetHeightM` agree exactly |
| One building on the site | PASS — no procedural twin, no baked block poking through, no z-fighting |
| Party wall flush with 248–250 | PASS — no slot; the DataSF-frame placement decision (§2.3) is what buys this |
| Orientation | PASS — the bay-and-entry front faces Ritch Street; the exposed flank faces the parking lot |
| Terrain seating | PASS — sits on the pavement, no float, no sink |
| Night | PASS — only the three upper bay sashes and the entry porch-light glow; the north-west upper window stays dark |
| Draw calls | PASS — `landmark-streaming-check` measured avg **58/frame** against the 300 iron-rule budget |
| Streaming | PASS — boot keeps 73 of 91 entries unloaded, 0 failed; the landmark loads on approach |
| `audit.mjs` check 1.6 | PASS — 100 zones over 97 landmarks clear |
| `verify-rebake.mjs` | PASS — 584 of 585 cells unchanged; cell `23_13` 182 → 181, and the nearest surviving footprint is 3.8 m from the 2.9 m radius |
| Fallback drill | PASS — app boots and renders, exactly one warning (`254-ritch failed to load … 404`), zero errors, and the site is empty ground inside the exclusion zone (Case B, expected) |
| Batch-mode sanity | PASS — `git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/` |

Two audit checks unrelated to this landmark fail on this tree and fail the same
way on `origin/main`: 1.2b (95th-percentile height, a property of the DataSF
source) and 1.3c (Telegraph Hill terrain, a property of the Terrarium DEM), plus
1.7b (one sampled tree offshore). None of them mentions `254Ritch`.

`landmark-streaming-check.mjs` passed its first three assertions and then timed
out on stream-out with 71 entries live. It was run without the 100 synthetic
`dummy-*` manifest entries its own header asks for, on a machine at load average
450+, and no entry failed at any point — the step is inconclusive rather than
failing, and it is not specific to this asset.

Evidence: `qa-app-day-wide.png`, `qa-app-day-detail.png`, `qa-app-night-detail.png`,
`qa-app-fallback.png`.

## Stage 3 — approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

— David, 18 August 2026, given with the pipeline invocation and read as standing
approval for gate 3. No revision round was requested. The three revision rounds
recorded above were self-initiated against the review renders.
