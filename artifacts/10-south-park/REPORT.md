# 10 South Park (South Park Lofts) — build report

Deliverable: `10-south-park.glb`, a stylized miniature of the 1993 South Park
Lofts at 10 South Park, San Francisco, for the SF-SIM toy-diorama city.

Sources, measurements and their confidence are in `REFERENCE.md`. The plan this
executes is `docs/asset-plans/10-south-park.md`. **Where they disagree, this
report wins**; §5 lists every disagreement.

## 1. What shipped

| | |
|---|---|
| File | `10-south-park.glb` — **361.6 KB raw, 213.8 KB gzip** (shipped, meshopt-packed; the 751.3 KB pre-optimize original is archived at `optimize/input/`) |
| Objects | **13** shipped (258 before the stage-4 join) |
| Triangles | **11,976** (plan cap 12,000; contract cap 27,000) |
| Dimensions | 39.94 × 36.00 × **14.67** m |
| Min Z | 0.000 |
| XY centre offset | 0.000, 0.000 |
| Materials | 12, all `Toy_*`, two `_Glow` |
| Textures / transparency / cameras / lights / animation | none |
| Validation | `validation.json` — **overall PASS** on the shipped packed file, every check true |
| Build | `build_10_south_park.py` (deterministic), `10-south-park.blend` |
| Renders | four elevations, facade, top, aerial, aerial-night, contact sheet |

The axis-aligned XY box is **39.94 × 36.00 m for a lot that is 14.2 m wide and
42.3 m deep**. That is the expected bound of a trapezoid standing at 45° to the
world axes — the party walls run 45.2°/225.2° — not a scale error.

## 2. Orientation — a deliberate contract deviation

The asset contract asks for "front faces −Y". This building's front faces
**179.7° (very nearly due south) over its bowed south-west two-thirds and 135.2°
(south-east) over its straight north-east third** — two planes, 44.5° apart. The
plans README resolves this: `placeGeneric()` in `app/src/assets.js` scales and
positions but never rotates, so a GLB must be authored in true-world orientation,
and where the two rules conflict **real-world orientation wins** (AGENTS rule 5).

Authored with Blender +Y = true north, +X = east. Measured face headings from the
build log:

- bowed front, four facets: **174.7°, 177.8°, 181.6°, 185.4°**
- straight north-east third: **135.2°**
- Taber Place rear: **315.1°**
- party walls: 45.2° / 225.2°

## 3. Height, and why 14.67 m

`targetHeightM` = **14.67 m**, the roof bulkhead crest, which is the tallest
geometry in the export, so the loader's `targetHeightM / measuredHeight` is
exactly 1.0.

- roof deck **12.27 m** — DataSF LiDAR median, and also its mode, over 1,044
  cells with σ 0.78 m
- parapet crest **13.10 m ± 0.15** — photogrammetric from Street View pano
  `aFRDCNG9w0lcHJ9ngJI8LQ`, flat to ±0.06 m across bearings 314°–354° while the
  range varied 41 % (the full table is in `REFERENCE.md` §3)
- bulkhead crest **14.67 m** — DataSF LiDAR maximum, 2.40 m over the median at
  3.1σ, believed because the tree trap is ruled out by position, the party-wall
  trap by direction (both neighbours are *taller*, so bleed could only pull the
  maximum down — and the rear block reports the same 2.4 m step against different
  neighbours), and because the aerial shows the box itself

Storey heights are *estimated* — garage 0 → 3.30 m, then two loft tiers of
**4.90 m = 16.07 ft** each to the 13.10 m parapet. That the arithmetic lands on
16 ft is the confirmation, not the assumption: the broker's "16 foot ceilings",
the 1991 permit's "three story" (garage plus two loft storeys) and the four
photographed window rows all agree.

Sanity check against the neighbours the loader will stand it beside: the parapet
at 13.10 m is **1.1 m below** 22–24 South Park's 14.22 m crest and **4.6 m below**
2 South Park's 17.72 m. Only the bulkhead pokes above the south-west neighbour,
by 0.45 m. If the finished asset ever towers over either, the height is wrong.

## 4. Design decisions

**Kept, because they are the building.** The two-block plan with the open
courtyard; the 44.5° break in the frontage; two identical stacked loft tiers, each
a wide banded window over a round-arched wood French door on a juliet balcony,
with a recessed loggia at the north-east end; the long flattened **oval mullion
motif** with its curled tail across each band; apricot stucco; the plain parapet
with a pale cap; the roof bulkhead.

**Simplified.** The small-pane glazing grids became three heavy mullions and a
transom per band. The ironwork lost its scrollwork and kept its silhouette. The
Taber Place windows became paired dark rectangles in pale surrounds. The
courtyard elevations became one tall glazed slot per unit — which is both cheaper
and closer to the listings' "wall of windows with French doors to the shared
courtyard" than a grid of separate openings would have been.

**Dropped.** Expansion joints, downpipes, light fittings, the security camera, the
"10 SOUTH PARK" plaque, unit numbers, roof scuppers, the security gate's pattern,
and the sidewalk magnolia that hides the north-east end of the frontage in every
photograph.

**Exaggerated.** The loggia recess (1.2 m, so it reads as black from above); the
pale window surrounds (widened so the bands read as bands at the app's camera);
the courtyard's green.

**Materials.** One off-palette colour: `Toy_apricot` `#dda87b`. The project palette
has no warm mid-orange — `rust a86444` is far too dark, `brick c96f4a` too red,
`mustard d9a441` too yellow — and this building's colour is its second-strongest
recognition cue on a rim of sage clapboard, cream ashlar and red brick. Off-palette
is a WARN, not a FAIL, and this block already carries `Toy_verdigris` (22–24),
`Toy_sash` (21–29) and `Toy_plum` (44–46) on the same argument.

`Toy_roofd` was deliberately **not** used for either roof deck: it renders
`rgb(9, 9, 12)` under the app's lighting and a roof in it reads black from the
only camera that ever sees it. Both decks are `Toy_stone`.

**Night.** The hero glow is the four front window bands plus the Taber Place
windows — this is a residential building whose whole street face is glass. The
loggias, the arched doors, both garages and both roofs stay dark; one warm
`Toy_mustard_Glow` accent sits in the pedestrian entry slot. Glow surfaces are
thin **closed** shells (an open face has no signed volume and fails the normals
contract) covering the lower 45 % of each band rather than the whole opening,
because a closed shell is two alpha layers and reads ~23 % by day, not the
nominal 12 %. The night frame is rendered in Cycles with `_Glow` driven from Base
Color at strength 1.0 — glTF writes `emissiveFactor = 0` when the authored
strength is 0, so a re-imported `_Glow` otherwise renders as a white slab.

## 5. Corrections to the plan, and iterations

Logged in the order they happened.

1. **The plan's triangle budget was met, but only after three passes.** The first
   build came in at 23,896 triangles — twice the cap — because every one of 283
   objects carried a two-segment bevel. Two segments were kept for the fourteen
   volumes that carry the silhouette and one for everything else; then applied
   hairline bands (anything whose smallest dimension is under 0.16 m — surrounds,
   mullions, railings, glow shells, garage reveals) were left unbevelled entirely,
   on the grounds that a 0.05 m chamfer on a 0.13 m strip is sub-pixel at the
   app's camera. That alone was worth about 9,000 triangles.

2. **The offset-handedness trap, twice, in two disguises.** The plan warned about
   deriving "outward" from a centroid. It bit anyway:
   - *On interior faces.* The front block's rear wall sits within a metre of the
     lot's area centroid, so a centroid test there is a coin toss, and on the two
     party walls it points **out** of the building — the first pass put the roof
     bulkhead and the roof mechanical in mid-air over the neighbours. Fixed with
     `facing(a, b, want_heading)`, which builds the face and flips it if its
     normal disagrees with the wall's *known* world heading.
   - *On the parapet inset.* `inset_polygon()` resolved "inward" against the
     polygon's own area centroid. That is correct for a convex outline and wrong
     for the rear block, whose north-east wing puts a **re-entrant corner** in it:
     the inner ring self-intersected around that corner. The per-object signed
     volume still came out positive, so only the ray test caught it — all 127
     flipped visible faces in the first validation run were on `rear_parapet` and
     `rear_cap`. Rewritten to take "inward" from the polygon's **winding**
     (signed area) instead. The flipped fraction went from 0.412 % to **0.000 %**.

3. **The loggia notch has to carry the arc vertex.** The recess spans t = 5.50 to
   7.90 m on an 8.64 m bowed chain whose third vertex sits at t = 6.75. Cutting
   the notch as a simple four-point rectangle folded the bow through that vertex
   and self-intersected the body outline. The notch is a five-point polygon that
   carries the vertex's own inward offset.

4. **The plan's oval motif nearly did not survive.** A 0.05 m bevel on a 0.19 m
   ring band collapsed most of the ellipse — it rendered as a hook and a small
   circle. Ornament rings are now excluded from bevelling outright, the bar is
   0.16 m, and the elevation carries an explicit **depth ladder** so nothing hides
   anything: glass front at d = 0.02, glow shell 0.02–0.05, mullions 0.05–0.11,
   the oval 0.05–0.13, the surround out to 0.14. Before that ladder the glow shell
   sat over the mullions and hid them.

5. **Both roof decks are modelled level, which the plan did not say.** The rear
   block's LiDAR median is 11.88 m against the front block's 12.27 m — but its
   ground is 0.47 m higher (`gnd_meancm` 1472.1 against 1424.6), so in absolute
   terms the two roofs are 26.60 m and 26.52 m: level. Modelling the 0.39 m
   difference would have been modelling the *site slope* as a *building step*. The
   courtyard and the rear block's base rise 0.45 m instead.

6. **The plan's north-east front bands were too wide.** At `(0.70, 3.40)` and
   `(3.90, 6.90)` the straight north-east third read as a curtain wall. Narrowed to
   `(0.85, 2.95)` and `(4.30, 6.85)` so a solid pier stands between them. That end
   of the elevation is behind a magnolia in every photograph and is the least
   certain thing modelled — see `REFERENCE.md` §6.

7. **The top-view render was upside down for one pass.** A track-quat at 89.9°
   pitch resolves its up vector to **south**, so the plan rendered south-up and
   looked, for several minutes, like the building had been built back to front. The
   top camera is now built by hand at a true nadir with `rotation_euler = (0,0,0)`.

8. **Two housekeeping errors worth recording.** The first build ran with the shell
   still inside `sf-worktrees/22-south-park/artifacts/22-south-park/`, so the
   script and its outputs landed in a sibling worktree — removed, and that
   worktree verified clean (`git status` empty) before continuing. And a
   `surround()` with a sill band under a doorway at z = 0 put the entry casing
   0.20 m below the pavement; `min_z` caught it.

## 5b. Approval (stage 3 gate)

Given in the pipeline session on **18 August 2026**, as a standing instruction
covering every gate in this run, quoted verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Presented at the gate: the contact sheet, the day and night aerials, and the
numbers in §1 and §6 (11,976 triangles, 39.94 x 36.00 x 14.67 m, 12 materials,
2 glow groups, validation overall PASS). No revision was requested.

## 6. Validation

`validation.json`, written by `validate_10_south_park.py` from a **fresh
factory-reset scene importing the shipped GLB** — not the build scene. It was run
twice: once on the pre-optimize build, and again on the stage-4 meshopt-packed
file that actually ships, because the sliver failure mode the optimize prompt
warns about appears only in the packed file. Both pass; the numbers below are the
shipped ones.

| check | result |
|---|---|
| meters and plausible dimensions | PASS — 39.94 × 36.00 × 14.67 m |
| crest normalized to target (14.67 ± 0.02) | PASS |
| base at z = 0 | PASS — min Z 0.000 |
| centred in XY | PASS — 0.000, 0.000 |
| under triangle budget (12,000) | PASS — 11,976 |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS — 12 `Toy_*`, no `Toy_body` |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward — per-object signed volume | PASS — 13 / 13 positive (258 / 258 pre-optimize) |
| normals outward — ray residual | PASS — **0 flipped of 30,823 first hits** |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

The per-object signed volume test is authoritative here because the asset is a
union of disjoint and interpenetrating solids; the 31,500-ray visibility test is
the cross-check, and it came back clean rather than merely within tolerance.

## 7. Draft manifest entry

Do not add this to the production manifest in this task — integration is a
separate job (`docs/asset-plans/INTEGRATION-PROMPT.md` plus §2.13 of the plan,
which specifies **three** exclusion zones for this lot).

```json
{
  "id": "10-south-park",
  "file": "10-south-park.glb",
  "anchor": [
    -122.3935162,
    37.7823704
  ],
  "targetHeightM": 14.67,
  "cat": 2,
  "name": "10 South Park (South Park Lofts)",
  "estimated": false,
  "dims": [
    39.94,
    36.0,
    14.67
  ],
  "tris": 11976,
  "loadRadius": 2500
}
```

The anchor is the model's own XY bbox centre as reported by the build, 1.4 m west
of the plan's parcel-AABB estimate (`-122.3934999, 37.7823712`) because the built
outline includes bevels and the courtyard slab. `name` leads with the address
rather than "South Park Lofts" because `188-south-park` already ships under that
marketing name.

## 8. Stage 4 — optimize

Run with the pipeline defaults (`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`). Full metrics, census, per-phase savings and gate results are
in `optimize/REPORT.md`. Headline: **769,304 → 361,604 raw bytes (−53.0 %)**,
258 → 13 objects, 261 → 14 draw submeshes, 24,806 → 6,488 vertices, triangles and
bounding box unchanged, worst A/B pixel delta 0.017 % against gates of 2 % and
4 %. All of G1–G6 and G8 pass. The optimized file is now the shipping file and
the pre-optimize original is archived at `optimize/input/10-south-park.glb`.

Two judgment calls worth carrying forward: the limited-dissolve step was
**skipped** because this asset has four coplanar parapet ring bands and that step
is the one that manufactures slivers; and the A/B rig was moved from Cycles to
EEVEE because the machine was at load 142 and the gate compares two renders of
one rig, so only the match matters.

## 9. Stage 5 — integration (Case B, batch mode)

Executed `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 with `<slug>` =
`10-south-park`, `<Name>` = `10 South Park (South Park Lofts)`, **Case B**, in
**batch mode**: the bake was run and fully QA'd, then discarded, and only source
is committed. `git diff --name-only origin/main` lists nothing under
`app/public/tiles/` or `api/_data/`.

| step | result |
|---|---|
| re-validation of the shipped GLB, fresh scene | **PASS** — `validation.json` overall PASS on the meshopt-packed file |
| GLB copied to `app/public/sf-assets/landmarks/` | **PASS** — byte-identical to `artifacts/` |
| manifest entry appended | **PASS** — +19 lines, 0 deletions (text splice, no JSON round-trip) |
| id mapping | **PASS** — `camelId('10-south-park')` = `10SouthPark`, matching the registry |
| registry entry in `pipeline/lib/landmarks.mjs` | **PASS** — landed in `LANDMARKS`, `exclusionZones()` returns its three zones |
| re-bake | **PASS** — full chain `terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes` |
| `audit.mjs` check 1.6 | **PASS** — "102 zones over 97 landmarks clear" |
| `verify-rebake.mjs` | **PASS** — 584 of 585 cells unchanged; cell **23_13 182 → 180**; nearest surviving footprint 25.5 m / 34.6 m / 11.5 m against the 2 / 5 / 4.5 m radii |
| nothing procedural under the asset | **PASS** — decoded `buildings/23_13.bin` and measured penetration into the real lot polygon: deepest is **−5.68 m**, i.e. the nearest survivor is 5.7 m *outside* the lot |
| single building at the site | **PASS** — one asset, no procedural twin, no z-fighting (screenshot) |
| **loader scale** | **PASS** — `SF.assets.placed.get('10SouthPark').log` = **`uniform x1.0000 at 3870, -1367`** |
| orientation | **PASS** — the bowed front and the loggia face the oval; the blind flanks face the two party walls |
| terrain seating | **PASS** — no float, no sink at the anchor |
| night glow | **PASS** — only the front window bands, the Taber Place windows and the entry accent light up |
| draw calls | **PASS** — **129** max at the landmark (300 budget), measured by hooking `renderer.render` and taking the per-frame max |
| streaming | **PASS** — `entries 91, live 83, loading 0, fading 0, failed 0` after settling |
| **fallback drill** | **PASS** — with the GLB moved aside: `failed: 1`, `live: 82`, the app boots, the city renders (613 cells, 15,263 trees), the landmark is absent and, as expected for Case B, its site is empty ground inside the exclusion zone. File restored. |
| `npm run lint` / `npm test` / `npm run build` | **PASS** — clean lint, 26/26 tests, build 1.53 s |
| batch sanity check | **PASS** — no `app/public/tiles/` or `api/_data/` in the diff |

QA method: headless Chrome over CDP against this worktree's own Vite dev server,
with the flag set from `pipeline/landmark-streaming-check.mjs`
(`--disable-background-timer-throttling --disable-renderer-backgrounding
--enable-unsafe-swiftshader`), which is what makes `requestAnimationFrame` run —
measured 30 frames in 3 s, so nothing had to be hand-pumped. The clock was pinned
with `SF.setClock(...)` for the day and night frames rather than left on live
time. The served manifest was checked for this entry before anything else was
believed, because `preview_start` resolves names from `~/.claude/launch.json` and
can silently serve a different tree.

**One honest observation from the deployed look, not a defect:** the app renders
`Toy_apricot` noticeably more saturated than the Blender review rig does — closer
to a terracotta orange than the authored `#dda87b`. That is the toy post-process,
and every neighbour gets the same treatment (2 South Park's brick and 22–24's
sage both read hotter in the app too). The building still does what the colour is
there to do: it is the one warm-orange lot on a rim of sage clapboard, cream
ashlar and red brick.

Not run, deliberately: push, PR and deployed QA. Stage 5 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` replaces the integration prompt's Step 7
with a stop, and the batch is opened as one PR by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.
