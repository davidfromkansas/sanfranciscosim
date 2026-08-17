# 95 Jack London Alley (Gran Oriente Filipino Masonic Temple) — build report

Built 17 August 2026 from `docs/asset-plans/95-jack-london-alley.md`, Blender
5.2.0 LTS, headless. **REPORT beats plan.** Where a number here differs from the
plan, this file is the one that shipped.

## Shipped numbers

| | |
|---|---|
| File | `95-jack-london-alley.glb` |
| Objects | **13** mesh, 0 other (48 before the stage-4 optimize pass) |
| Triangles | **3,888** (budget 6,000) |
| Dimensions | 16.196 × 16.093 × **8.400** m |
| bbox min / max | `[-7.997, -7.943, 0.000]` / `[8.199, 8.151, 8.400]` |
| min Z | 0.000 |
| XY centre offset | `[0.101, 0.104]` m |
| File size | **110.3 KB raw** as shipped (230.6 KB before the stage-4 optimize pass, −52.2%) |
| Materials | 13, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow materials | `Toy_gold_Glow`, `Toy_trim_Glow` |
| Anchor | `-122.3934430, 37.7813460` (DataSF LiDAR area centroid) |
| Facade heading | 225.9° true (SW, onto Jack London Alley) |
| Target height | 8.40 m — bbox top lands on it exactly, loader scale 1.0 |

`validation.json` — **overall PASS**, all 16 checks, re-run against the shipped
(meshopt-packed) file. 13/13 objects enclose positive signed volume; 31,500
deterministic visibility rays, **0** flipped first-hit faces; 0 degenerate
triangles; 0 invalid or non-unit loop normals.

The 16.2 × 16.1 m axis-aligned bounding box is correct for an 8.60 × 13.70 m box
standing at 45.9°, and is not a scale error. The validator's plausibility window
is deliberately tight (15.6–16.6 × 15.5–16.5 m) so that a model built on OSM's
rejected 9.37 × 20.35 m footprint, which would land near 21 × 21 m, cannot pass.

## Dossier corrections made at build time

**1. The footprint, and therefore the anchor, is not OSM's.** Confirmed the plan's
correction independently before modelling. OSM `way/71211338` traces 20.35 × 9.37 m;
sampling that rectangle along its own long axis against every DataSF polygon in the
block puts its south-west 13.0 m in the temple's footprint (median 7.84 m), the next
3.0 m in **41–43 South Park's** footprint (median 9.83 m), and the last 2.0 m in no
building at all — and Bing z20 shows a tree canopy standing exactly there. Built on
the DataSF polygon: **8.60 × 13.70 m**, anchor `-122.3934430, 37.7813460`, which is
2.64 m south-west of the OSM centroid. Everything downstream — the target height's
plausibility, the exclusion window in the plan's 2.13 — depends on this.

**2. The height ships as `estimated`, and that is the honest call.** The 7.84 m roof
deck is a DataSF LiDAR median over 457 cells and is solid. No published figure for
the crest exists: the designation report gives no dimension, the OSM building way
carries no `height` tag, and the assessor's record for lot 3775/039 describes the
1909 apartment building in front instead. The 8.40 m parapet crest is derived — two
photogrammetric reductions of the one square-on photograph gave 8.3 m and 8.6 m.
The LiDAR maximum of 12.99 m was rejected as 45–49 South Park bleeding across a
0.5 m raster cell (its own maximum is 13.00 m).

**3. The facade is built SYMMETRIC, against what the photograph seems to show.**
In the 2016 square-on shot the north-west flanking window sits visibly closer to
the entrance than the south-east one — roughly 2.7 m of wall on one side against
1.0 m on the other. Attempting to correct for perspective made it worse, not
better: the photograph's verticals converge to a vanishing point 2,180 px above
frame while its horizontals converge to one that is geometrically incompatible with
that, so the image cannot be rectified and the apparent asymmetry cannot be
separated from a wide-angle lens used close to a building on a 6 m alley. The
plan's own risk-3 fallback applies — a wrong asymmetry looks deliberate and gets
copied forward — so both windows sit at ±2.85 m. **This is the weakest facade call
in the asset and the first thing to fix if better photography turns up.**

**4. There is no architect to attribute.** The designation report says
"Architects: Unknown". Nothing was found to contradict it, which is unsurprising
for a 1951 lodge hall built by its own membership.

## Revision log

**Round 1 — the parapet read as a fussy triple cornice.** The first pass carried a
continuous coping ring right round at 8.05–8.15 and then stacked the facade
parapet and its own coping on top of it. From square-on that is three stacked
mouldings; the real building's alley parapet is one flat plane with a single thin
cap. The ring now stops dead at the two front corners — which is exactly where the
real parapet steps up — and the facade parapet runs flush with the wall below it.

**Round 1b — the name course read as an applied sign panel.** `GRAN ORIENTE
FILIPINO / MASONIC TEMPLE` was a 6.00 × 1.02 m `Toy_stone` slab and looked like a
board screwed to the wall. The real thing is text cut into pink stucco with nothing
behind it. It is now 5.60 × 0.85 m in **`Toy_peach`**, proud 0.035 m, so the bevel's
shadow line is the whole of it — which is what incised text looks like from 150 m
up. The DEDICATED… course keeps a light `Toy_stone` value, because the photograph
really does show a lighter incised band under the coping, and it is thinner now.

**Round 2 — the recess came out of the boolean in the wrong colour.** The arch
cutter was given `Toy_coral` on the assumption that Blender's exact boolean carries
the operand's material onto the newly created faces. **It does not** — the entire
recess came through in `Toy_peach`, and `Toy_coral` was absent from the exported
material list. The tympanum is now an explicit coral plane at the back of the
opening, which is also where the warmth actually shows in the reference
photographs; the arch reveal itself really is the same stucco as the facade, so it
stays peach. Worth remembering for the next asset that cuts a recess.

**Round 2b — the roof patch read as a sheet of paper.** The lighter membrane area
the Bing aerial shows was modelled 6.40 × 3.20 m in `Toy_stone` on a `Toy_roofd`
deck, which is a huge value jump over a third of the roof. Now 3.00 × 2.20 m in
`Toy_steel`, a 20 mm inlay — enough to give the deck a composition without
inventing plant that is demonstrably not there.

**Round 3 — coping stubs poking out of the facade cap.** The three flank panels
were extended 0.145 m past *both* their ends so the corners would close, which left
two coping stubs sticking out either side of the taller facade cap like door
handles. Only the rear panel oversails now; the flanks stop on the front corners.

**Round 3b — the north-west flank was completely blank.** It is the one secondary
elevation there *is* a photograph of, and the 2016 oblique shows a small opening
near the alley end and a projecting element above it. Both are now modelled.

**Round 4 — four zero-area triangles and two non-unit loop normals.** Traced to
`recess_back`. `pointed_profile()` appended `(-a, z_spring)` to close the profile,
but the left arc's `k == 0` term already lands on that point exactly, so the
profile closed on a duplicate vertex. It had been present in the arch cutter from
the first build and never surfaced, because every other object goes through the
bevel pass and its `remove_doubles` was silently cleaning it up; `recess_back` is
on the no-bevel list. Fixed at the source.

## Night state

Category 8 is night profile 3 (dark), and a lodge that meets a few evenings a
month should be one of the quietest things in the night city. Hero: the **gold
square-and-compass** on the centre transom lobe. Supporting: the **two globes** on
Jachin and Boaz, and a thin warm spill across the recess threshold. Nothing else
lights — not the second-floor window, not the flanking windows, not the roof, not
the text courses. The night render is a dark box with a lit doorway, which is
exactly the intent.

**Glow-shell discipline.** The app renders `_Glow` in a separate layer at
`0.12 + 0.95·uNight` opacity, so a **closed** shell is two alpha layers deep and
reads ~23% by day rather than 12%. The validator, meanwhile, requires every object
to enclose positive signed volume, so open shells are not an option. The resolution
here: every glow surface is closed **and** sits over opaque geometry of the *same*
colour, and the three of them together cover under 0.6 m² of a 72 m² facade —
`Toy_trim_Glow` `f6e6c4` over `Toy_trim` `f3efe6` on two 0.32 m spheres, and
`Toy_gold_Glow` `e6c46a` over `Toy_gold` `caa64a` on a 0.44 m emblem. A 23% wash of
near-white over near-white, and of gold over gold, is invisible by day. The
threshold spill sits inside a 0.75 m deep recess where nothing can see it by day
either.

## Off-palette materials (accepted WARNs)

Two hexes are off-palette, pre-authorised in the plan's 2.8 under the style
bible's SF exception for tinted facades, following the convention 165 South Park
set (keep the palette **key** so the contract check stays meaningful, move the
value to the building's real colour):

| Material | Palette hex | Shipped hex | Why |
|---|---|---|---|
| `Toy_peach` | — (new key) | `e8cdc9` | the building is blush pink in a block of gray, white and olive; this is recognition cue #2 and desaturating it toward `Toy_sand` would make the asset invisible |
| `Toy_coral` | — (new key) | `d9a189` | the entrance recess is distinctly warmer than the facade in every photograph, and that warmth is what makes the notch read as a doorway rather than a hole |

The hue is *inferred*. The two available photographs sample `#c7b8be` (a facade lit
only by blue sky, so it reads cold and mauve) and `#ddc7ca` (overcast); `e8cdc9` is
the reconciled warm reading. The value **relation** — warm light pink body,
off-white trim, warmer recess, dark doors, charcoal roof — is confident. The hue is
not. Move it if better photography turns up.

## Renders

All regenerated from the final export: `-north`, `-east`, `-south`, `-west`,
`-top`, `-aerial`, `-aerial-night`, plus two extras the plan asked for because
this building stands at 45.9° and none of the four cardinal elevations shows its
public face square-on:

- `-facade.png` — orthographic, square-on at 225.9°
- `-entrance.png` — a close three-quarter of the arch, columns, globes and transom
  at a scale where the modelling can actually be judged

`-contact-sheet.png` composites all nine.

## Gate 2

`validation.json` overall **PASS**. Committed pre-approval as
`assets: build 95-jack-london-alley (pre-approval)`.

## Gate 4 — optimize

All gates G1–G6 and G8 PASS; see `optimize/REPORT.md`. 236,120 → 112,904 bytes
(−52.2%), 49 → 14 draw primitives, triangles unchanged, mean pixel delta
0.0009–0.0130% across day/night × near/far and four elevations. The optimized
file is now the shipping file; the pre-optimize original is archived at
`optimize/input/`.

## Gate 3 — approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 16 August 2026, given
> in the invoking message alongside `BUILDING:` and `BATCH: yes`.

Standing approval for this pipeline run, quoted verbatim per stage 3. The contact
sheet, the aerial day and night renders and the numbers above were produced and
presented; no revision was requested.

## Gate 5 — local integration QA (Case B, batch mode)

Verified against a production build of `app/dist` served on :5209 and driven in
headless Chrome over CDP. `preview_start` was out of slots (five dev servers
belonging to other chats), which is the documented fallback. Software WebGL, so
frame rate is environment-limited and not reported as a measurement.

| Check | Result | Evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | fresh-scene re-import of the packed file, all 16 contract checks, 3,888 tris, 13 materials |
| GLB in place | **PASS** | `app/public/sf-assets/landmarks/95-jack-london-alley.glb`, byte-identical to the artifact; served 200, `Content-Length: 112904` |
| Manifest entry | **PASS** | 19-line append, JSON valid, no other entry reformatted (appended as text — `JSON.stringify` rewrites `11.0`→`11` across unrelated landmarks) |
| id mapping | **PASS, after a correction** | `camelId('95-jack-london-alley')` → `95JackLondonAlley`. The plan's §2.13 drafted `95JackLondon`, which would **not** have matched and would have left the procedural building standing under the GLB. Registry uses the correct id |
| Case B registry entry | **PASS** | `pipeline/lib/landmarks.mjs`, `exclude: 4.8`, `camera: { distance: 120, yaw: 314, pitch: 24 }` |
| Exclusion against the real bake input | **PASS** | measured before baking: DataSF drops **1** ring (`201006.0108499`, centroid, 0.05 m); Overture drops **1** ring (centroid, 2.64 m); nearest spared ring 7.07 m. Two rings, one source each, exactly as the plan predicted |
| Tile re-bake | **PASS** | full chain terrain→muni-shapes. `lore.json` in 156.5 s; 230,771 toy building records in 585 cells; context 596 sidecars, all four context validations ok |
| `verify-rebake` | **PASS** | `584 of 585 cells unchanged; 23_13 201 → 200 ← 95JackLondonAlley`; nearest surviving footprint **7.1 m vs 4.8 m radius** (and it is 13.2 m tall) |
| audit 1.6 | **PASS** | "no procedural footprint inside a bespoke landmark exclusion zone — 83 zones over 80 landmarks clear". The three audit FAILs present (1.2b p95 height, 1.3c Telegraph Hill DEM, 1.7b one offshore tree) are the pre-existing baseline — identical in the 135-south-park, 126-south-park and 101-grove worktrees' committed `audit.json` |
| Single building on the site | **PASS** | no procedural twin, no baked block poking through, no z-fighting |
| Scale factor | **PASS** | `sf-assets: 95-jack-london-alley merged 14 objects / 13 materials -> batched (2141 tris body); uniform x1.0000 at 3877, -1254` |
| Orientation | **PASS** | the alley facade faces the alley; the entrance reads square-on from the `yaw: 314` preset |
| Terrain seating | **PASS** | base flush with the sidewalk, no float, no sink |
| Night glow | **PASS** | only the two globes and the gold emblem light; the rest of the building goes dark while the warehouse next door is fully lit |
| Draw calls < 300 | **PASS** | peak scene-pass draw calls (measured with the render wrapper from `.agents/skills/testing-sf-3d/SKILL.md` §"Measuring draw calls" — the overlay always reads 1): **96** at the landmark, **92** downtown at street level, **106** downtown at night |
| Fallback drill | **PASS with one honest note** | GLB renamed, cache cleared, reloaded: the app boots, the block renders, the site is **empty ground** inside the exclusion zone (expected for Case B), both neighbours intact, no crash. **The warning fires twice, not once** — `assets.js:560` (the streaming re-attempt path) logs `sf-assets: … failed to load (…)` without the once-only `warned` guard that `warn()` at `assets.js:362` has, and without its " — keeping the code-built landmark" suffix. Pre-existing loader behaviour, not caused by this asset; flagged as separate work rather than fixed inside a landmark integration |
| lint / test / build | **PASS** | `eslint src test` clean; 26/26 node tests pass; `vite build` ok; `compress-tiles` 3315 tiles 56.8 → 31.8 MB |
| Batch-mode handoff | **PASS** | bake discarded with `git checkout -- app/public/tiles api/_data`; `git diff --name-only origin/main` lists **0** files under `app/public/tiles/` or `api/_data/` |

**One observation, not a defect.** The `Toy_roofd` `#45454a` deck renders close to
pure black in the app, far darker than in the Blender rig. This is the documented
`Toy_roofd` behaviour across the whole landmark set, not something this asset
introduces: a control screenshot of **135 South Park**, which shipped with the same
deck material, is equally black under the same camera and clock. The deck was left
alone for consistency with the shipped set, and the real roof genuinely is a dark
membrane against white neighbours. The `Toy_steel` membrane patch and the two
`Toy_rust` vent boxes are what keep it from being a featureless void, and they do
read — better, in fact, than 135's single vent cowl.

**Step 7 is replaced by a stop**, per `ADDRESS-TO-ASSET.md` stage 5: no push, no PR,
no deploy. The branch `pipeline/95-jack-london-alley` is a source-only Case B branch
awaiting `docs/asset-pipeline/BATCH-INTEGRATE.md`.
