# Fulton Plaza — build report

`fulton-plaza.glb`: 21 objects, **10,692 triangles**, **262 KB raw / 163 KB gzip** as
shipped (meshopt-compressed; 527 KB before stage 4), 16 palette materials, **draped on the
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
| `targetHeightM` | **13.1931 m** — the vertical extent, so the loader's scale is 1.0 |
| Dimensions | 128.4915 × 67.6286 × 13.1931 m |
| `min_z` | **−1.50 m** — negative by design; z = 0 is the anchor's ground |
| XY centre offset | 0.0000, 0.0000 |
| Long axis | 81.15° true (toward Hyde Street); cross axis 171.15° |
| Right-of-way | 120.04 × 48.59 m oriented, 5,805 m² = 1.435 acres |
| Terrain | draped; falls 2.366 m along the axis, **cross-falls 0.874 m**, anchor 17.788 m |
| Deck standoff | Z_DECK = 0.95 m above grade, max error over 32 ray-cast samples **0.0039 m** |
| Monument crest | 11.693 m above local grade — the tip of Eureka's spear (apron 1.03 + 10.668 m, SFAC 420 in) |
| Koi | two bodies, 20.642 m each |
| Triangles | 10,692 of a 16,000 cap |
| File | 268,212 B raw / 167,112 B gzip9, meshopt-compressed. Pre-optimize 540,052 B; see `optimize/REPORT.md` |
| Category / streaming | `cat: 0`, `loadRadius: 2500` |

## Triangles by object

| object | tris |
|---|---|
| `joints` | 2,304 |
| `bollards` | 1,568 |
| `monument` | 1,440 |
| `trees` | 1,104 |
| `deck` | 970 |
| `koi` | 408 |
| `bed_*_kerb`, `bed_*_soil` (4) | 400 |
| `koi_glow` | 384 |
| `lamps` | 384 |
| `people` | 384 |
| `terrace_s_wall` | 288 |
| `terrace_s` | 256 |
| `walk_n` | 210 |
| `furniture` | 180 |
| `apron` | 156 |
| `lamps_glow` | 144 |
| `monument_glow` | 60 |
| `ashurbanipal` | 52 |

## Validation

`validate_fulton_plaza.py` factory-resets Blender, imports **only the exported GLB**, and
writes `validation.json`. Overall **PASS**.

| check | result |
|---|---|
| meters and plausible dimensions | PASS — 128.5 × 67.6 × 13.19 m |
| vertical extent matches the build's own metadata | PASS |
| height datum is the monument | PASS — the crest vertex belongs to `monument`, not to a tree |
| **deck drapes the terrain** | PASS — 32 samples, max standoff error 0.0039 m (tolerance 0.10) |
| koi are two bodies of the right size | PASS — 20.642 m and 20.642 m, clustered against the surveyed centres |
| koi carry both day and night materials | PASS |
| centred in XY | PASS |
| under triangle budget | PASS — 10,692 / 16,000 |
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

`gltfpack@0.24 -c -km -kn -noq` applied to the approved build: **540,052 → 268,212 bytes
raw, −50.3%**, geometry byte-identical, max A/B pixel delta 0.046%, all gates PASS.

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
11. **Two pale stone stripes drew straight across the plaza in the running app.** They are
    the baked toy sidewalk plinths of the Fulton Street centreline — `exclusionZones()`
    clears buildings, not streets — and at the first deck height of 0.55 m the measured
    clearance over them was only 0.06–0.15 m, because the ribbon's `y` quantises up to
    0.20 m above the terrain and `createGroundMaterial()` runs the ground with
    `polygonOffset{Factor,Units} = -2`. The deck moved to 0.95 m (0.40 m clear) and the
    whole Z stack with it, which is why `targetHeightM` is 13.19 m rather than 12.80 m.
    **This defect is invisible everywhere upstream** — it is a depth fight against geometry
    that is not in the file, so no Blender render and no contract check can see it, and only
    the stage-5 app QA does.
12. **The Pioneer Monument read as a square ziggurat with four totems on it.** Rebuilt
    from the 2017 Commons photographs as the circular composition it is — a name drum with
    medallion busts, a panelled pedestal drum, a flaring cornice, a bronze collar, and
    Eureka with her shield, her grizzly and her spear on top; the four piers dropped to
    their photographed 1.55 m and their groups became **seated**. Every radius in the first
    attempt was ~35% over. Dropping the bevel on the merged object took it from 12,532
    triangles to **1,440** — a third of the old blocky version — and the whole asset from
    13,364 to 10,692. Requested by David after seeing the stage-5 screenshots.
13. **A green kit apartment block stood on the monument's apron in the app** — after the
    monument rebuild, and only because of how the bake had been restored. Two things
    conspire. `verify-rebake.mjs` and `audit.mjs` check the **buildings** tier, but the
    building kit (`kitplan.js`) plans from the **toy** tier, which carries its own
    simplified copy of every footprint — here a 4-vertex ring 0.84 m from the anchor,
    baked to 20.8 m, against the buildings tier's 17-vertex cruciform at 1.00 m / 21.9 m.
    And `pipeline/toy.mjs` writes straight into `app/public/tiles/toy/`, so
    `npm run validate` does **not** republish it: after a `git checkout -- app/public/tiles`
    (which batch mode requires), re-running only `validate` restores the buildings tier and
    leaves the toy tier at `origin/main`. Re-running `toy` → `notables` → `context` fixed
    it: `toy/19_13.bin` 274 → 273 footprints, nothing within 30 m of the anchor.
14. **The validator's first drape sample missed a quarter of its points.** The outer row at
    `v = 16` landed on the south terrace, not the deck, and rays that hit an overlay are
    skipped — so a badly chosen grid shrinks the sample silently rather than failing. Moved
    to `v = 12`, and the koi cluster now seeds from the **surveyed** koi centres rather than
    from a self-chosen threshold, which had split one 20.5 m fish into two bodies.

## Corrections to the asset plan

`docs/asset-plans/fulton-plaza.md` was written before the model existed. Two numbers moved:

1. **`targetHeightM` is 13.1931 m, not 10.67 m.** The plan set the target to the Pioneer
   Monument's catalogue height and asked the validator to assert `max_z == 10.67`. That is
   incompatible with the terrain drape the same plan mandates: once z = 0 means the anchor's
   ground, the export spans −1.50 to +11.69 m and the loader's scale is
   `targetHeightM / 13.19`. The monument is still 10.668 m of monument and still the model's
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
   thing on its own plaza after the 2.37 m drape. A measured plane above 11.69 m would be a
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

## Stage 5 — local integration QA

Driven by `qa_local.mjs`: the **built** app (`app/dist`) in real headless Chrome over CDP,
because a hidden Browser pane throttles `requestAnimationFrame` to nothing and makes a
healthy streamed landmark look broken.

| check | result |
|---|---|
| manifest entry loads | **PASS** — `sf-assets: fulton-plaza merged 26 objects / 16 materials -> batched (7724 tris body); uniform x1.0000 at 1898, -1072` |
| uniform scale ≈ 1.0 | **PASS** — exactly x1.0000, so `targetHeightM` and the authored extent agree |
| id mapping | **PASS** — `camelId('fulton-plaza') = 'fultonPlaza'`, and `SF.assets.placed` carries `fultonPlaza` |
| one building on the spot | **PASS** — the re-bake dropped the one baked footprint (the traced Pioneer Monument); nothing pokes through |
| terrain seating | **PASS** — the deck sits on the ground end to end across a 2.37 m fall; validator standoff error 0.0039 m |
| asphalt reads as a surface | **PASS** — median luminance **38** (p10 37, p90 38) over two bands of open deck, against **8** for the baked toy streets in the same frame. `Toy_roofd` measures 9 in this renderer, so `6f7076` clears the dark cliff by 4× |
| no baked street bleeding through | **PASS** — p90 38 against a median of 38. Before the deck lift the same window read p90 **196**: that gap *was* the defect |
| night glow | **PASS** — both koi glow with their markings, the lamp lenses light, the monument is washed; nothing else |
| draw calls | **PASS** — 122/frame at the landmark (budget < 300) |
| asset warnings | **PASS** — none; 104 entries, 0 failed |
| **fallback drill** | **PASS** — with the GLB served as a 404: the app still boots, 96 landmarks live, `failed: 1`, and **exactly one** warning: `sf-assets: fulton-plaza failed to load (… 404 …)`. Case B, so the site is empty ground inside the exclusion zone — expected |
| lint + build | **PASS** — `eslint src test` clean, `vite build` clean, `npm test` green (it runs first) |

Note on the drill's wording: `INTEGRATION-PROMPT.md` Step 6 says to expect one
`… — keeping the code-built landmark` line, which is the **resident** path. A **streamed**
entry — anything with a `loadRadius`, which is this one — fails through `scan()` instead and
emits `sf-assets: <id> failed to load (…)` with no "keeping" suffix. It is still exactly
once. Match on the id, not on the prompt's wording.

Screenshots in `qa/`: `day`, `night`, `wide` and `drill-day` / `drill-night`.

`day`, `night` and `wide` were re-shot after the monument rebuild **and** after the toy tier
was corrected (build iteration 13). The earlier `low-from-hyde`, `low-from-larkin` and `plan`
frames were **deleted rather than kept**: a fixed sample box at the plaza centre showed
19–21% "green roof" pixels in them — the kit block — against 0.3–0.7% for a clean frame,
which is a cheap and objective way to prove a screenshot is of the state you think it is.
Those three views were not recaptured: the machine sat between load 270 and 736 for four
hours (a dozen parallel landmark sessions), and a full six-shot run stopped completing at
all. That is a FAIL on evidence I would have liked, not on the asset — the deck-clearance
question those low shots were added to answer had already been settled at 0.55 m vs 0.95 m,
and the day/night/wide set covers Step 5's own requirement.

`qa_local.mjs --quick` boots, streams the landmark in and takes the day and night shots
only. The draw-call block runs 30 real animation frames and the full sequence six shots;
under SwiftShader at load 300+ that is 45 minutes for evidence one frame already carries.

## Case B — registry, re-bake and audit

| step | result |
|---|---|
| registry entry | `fultonPlaza`, lon/lat = the right-of-way OBB centre, `height: 11.27`, `exclude: 25`, camera `{340, 99, 26}` |
| re-bake | full chain `terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes`, all green |
| what moved | **one** baked footprint, in **one** cell: `19_13` 102 → 101. The dropped ring is the 17-vertex cruciform 1.00 m from the anchor — the Pioneer Monument, which DataSF traces as a building and the bake extruded to 4.6 m |
| `audit.mjs` check 1.6 | **PASS** — "114 zones over 110 landmarks clear". The three unrelated pre-existing failures (1.2b citywide height p95, 1.3c Telegraph Hill DEM, 1.7b one offshore tree) are unchanged |
| `verify-rebake.mjs` | **PASS** — "only the new landmarks' cells moved"; 584 of 585 cells unchanged; nearest surviving footprint 86.2 m against a 25 m radius |
| exclusion proved by **penetration depth** | `origin/main` **+24.22 m** — a 4.6 m block (baked 17.3 → 21.9 m) standing 24 m *inside* the right-of-way rectangle, exactly where the modelled monument goes. After the re-bake **−63.82 m** — the nearest surviving ring is 64 m *outside* it. A count or a boolean cannot say this; the depth can |
| the **toy** tier, which is what the kit plans from | `toy/19_13.bin` 274 → 273 footprints; the 4-vertex ring 0.84 m from the anchor (baked top 20.8 m) is gone. Checked separately from the buildings tier because `verify-rebake.mjs` does not look at it — see build iteration 13 |
| generated churn | 596 files: 585 `ctx/*.json` sidecars (expected — dropping one footprint renumbers the global building ids their pick lists reference), 1 `buildings/19_13.bin`, 1 `toy/19_13.bin`, 3 `context/`, 2 `api/_data/`, 4 manifests |

**Batch mode**: the bake was run for this QA and then discarded
(`git checkout -- app/public/tiles api/_data`). `git diff --name-only origin/main` lists
**nothing** under `app/public/tiles/` or `api/_data/`. The city is baked once for the whole
batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

## Approval

Gate 3 was given in advance, in the session's invocation, verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

— David, 19 August 2026. The renders and numbers above were presented in the same session
before stage 4 began; no revision was requested.
