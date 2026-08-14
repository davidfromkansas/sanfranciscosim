# Civic Center Plaza — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, from
`docs/asset-plans/civic-center-plaza.md`. **This report beats the plan wherever they
disagree**; the corrections are in §4 and in `REFERENCE.md` §7.

## 1. What shipped

| | |
|---|---|
| File | `civic-center-plaza.glb` |
| Manifest id | `civic-center-plaza` |
| Triangles | **17,703** shipping / 17,820 pre-optimize (cap 18,000; hard gate 30,000) |
| Objects | 19 shipping / 94 pre-optimize (joined per material at stage 4) |
| Dimensions | **145.612 × 192.624 × 30.480 m** |
| min Z / XY centre | 0.000 m / (0.000, 0.000) |
| Height datum | US flagpole finial at exactly 30.480 m — validator confirms the extreme vertex belongs to the `flagpoles` object |
| Anchor (bbox centre) | lon **−122.4176184**, lat **37.7794818** |
| Plaza OBB centre | lon −122.4176170, lat 37.7794913 (`recentre()` shift: 0.13 m W, 1.05 m S) |
| Long axis heading | 170.94° true (toward Grove Street) |
| Materials | 19, all `Toy_*`, 4 `_Glow` |
| Shipping GLB | **479,064 bytes** (meshopt, stage 4); pre-optimize 949,380 |

The axis-aligned XY box is 145.6 × 192.6 m because the plaza is a 177.88 × 121.48 m
rectangle sitting 9.06° off the world axes. That is the expected consequence of the real
heading, not a scale error.

## 2. Validation

`validate_civic_center_plaza.py` factory-resets Blender, re-imports **the exported GLB**
(not the source `.blend`) and writes `validation.json`. **Overall: PASS**, 19/19 checks.

| Check | Result |
|---|---|
| metres and plausible dimensions | PASS |
| crest normalized to target (30.48 ± 0.01) | PASS |
| height datum is the US flagpole | PASS |
| tree count matches survey (190) | PASS |
| tree positions match survey | PASS — max error **0.0206 m** on the shipping file (0.0007 m before meshopt rounding; gate 0.05 m) |
| base at z = 0 | PASS |
| centred in XY | PASS |
| under triangle budget | PASS — 17,703 / 18,000 |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward — per-object signed volume | PASS — 0 inverted of 19 |
| normals outward — ray residual | PASS — **0.000%** of 31,500 rays (gate 0.15%) |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

The normals result is worth noting: this asset is a union of ~450 separate closed solids
(deck, kerbs, slabs, 190 trunks, 190 crowns, 35 poles, 35 flags, fences, kit, furniture,
figures) and the ray test still comes back at exactly zero flipped visible faces. Per-object
signed volume is the authoritative test here and every object encloses positive volume.

### 2.1 Four validator bugs found and fixed

All were in the *validator*, not the asset, and all would have produced a false FAIL. Worth
recording because a validator that cries wolf on a good asset is as expensive as one that
passes a bad one — and this validator did in fact pass a mirrored plaza:

1. **Tree clustering split each tree into ~2.75 clusters** (523 "trees" for 190) because it
   clustered every vertex with a 1.5 m radius while the crown drum is 3.3 m across. Fixed
   by clustering trunk vertices only (`z < 5.0`), where the 0.38 m trunk against 3.2 m row
   spacing is unambiguous.
2. **Cluster centres were biased 0.126 m off-axis** because the seed vertex sits on the
   trunk hexagon rather than on its axis. Fixed with a second pass that averages every
   member of each cluster. Error dropped to 0.0007 m.
3. **The `z < 5.0` trunk-band filter stopped working** once the trees were rebuilt as
   pollards, because the crown underside moved to 4.90 m (4.61 m at the low end of the
   ±6% jitter) and its 3.3 m-radius ring started passing the filter: 414 "trees" for 190.
   Now a named `TRUNK_BAND_Z = 4.0` constant with the reasoning next to it.
4. **The validator carried the build's own mirror bug**, reconstructing expected positions
   with `vdir = (-udir[1], udir[0])`. Had it been fixed alone, it would have failed a
   correct asset; had the build been fixed alone, it would have passed a mirrored one.
   Both now derive `+v = west` the same way.

## 3. Design read

The recognition rests on ground pattern and repeated rhythm, not massing — this is the
first asset in the set with no building in it.

- **Two bosques**: six rows of pollarded London planes, 190 trees at their surveyed
  positions with ~3.2 m spacing, crowns 6.6 m across so they interpenetrate into one
  continuous canopy slab per bosque. The rows sit only 2-3.5 m apart in the survey, so
  each bosque reads as one long linear band rather than a deep grove — that is what the
  real planting is, and the top render confirms it.
- **Central court**: the 13.2 × 72.3 m fine-gravel panel on the Fulton axis, pointing west
  at City Hall's dome.
- **Pavilion of American Flags**: 18 poles at 15.24 m in two rows of nine, 48.5 m apart,
  flanking the court.
- **Four lawn panels** plus two east strips, hard-edged and kerbed 0.15 m proud of the
  paving, with the measured notches kept.
- **Two playgrounds** on the Larkin side carrying the only saturated non-green colour.
- **The 100 ft US flagpole** in the south-west lawn, the model's height datum.

Night state: the walk grid is the hero glow. The four allée walks, the perimeter walk and
the cross links light up as a luminous orthogonal grid on a dark field; lawns and bosques
go dark; the US pole gets a floodlit band; each playground gets a restrained accent. Four
`_Glow` materials, every one a thin shell proud of an opaque parent, day colours matching
their non-glow neighbours.

## 4. Corrections to the plan

Eight, all recorded in `REFERENCE.md` §7. The four that changed geometry:

1. **The whole plaza was mirrored east-west** — the most serious defect in this build,
   and one that **passed all 19 automated checks**. The playgrounds came out on the City
   Hall side instead of the Larkin side; every lawn, walk and kiosk was on the wrong side
   of the axis. AGENTS rule 5 violation.

   Cause: `data/plaza_uv.json` defines `+v = west`, which makes `(u, v)` a **left-handed**
   frame in world space (x east, y north). The first build wrote
   `V_DIR = (-U_DIR[1], U_DIR[0])` to keep the mapping right-handed so that
   counter-clockwise rings would stay counter-clockwise and extrusion caps would face
   outward — fixing the winding by silently swapping east and west. Fixed by pointing
   `V_DIR` west where it belongs and inverting the winding convention where it belongs
   instead, in `orient_for_world()` and `ngon_uv()`. Normals stayed clean through the
   change: 0 inverted objects, 0.000% ray residual, before and after.

   Caught only by the **top render**, which is why the plan makes the top view this
   asset's primary review image rather than a supporting one. The un-mirrored bbox is
   145.6 × 192.6 m rather than 146.5 × 192.3 m — the plaza is asymmetric, so the change in
   dimensions is itself confirmation that the mirror was real.

2. **Triangle blow-out (caught by the build's own cap assertion).** The first build came in
   at **33,664 triangles — over the 30,000 hard gate.** Cause: the bevel pass was running
   over the merged multi-solid objects, where a 0.12/2 bevel multiplies each of dozens of
   small boxes by about nine (lamps 448 → 3,640; people 480 → 4,320; benches, fences and
   play kit similarly). Those objects now ship unbevelled — their tapered profiles carry
   the soft read at the app's camera distance — while the chunky single solids keep the
   full bevel and the paving slabs take a token 0.05/1. Result: 17,896.
3. **Trees were lollipops (caught in the first north elevation).** Authored with the trunk
   stopping at 3.55 m and the crown starting at 7.55 m, which left a 4 m gap of bare pole
   under every tree; the bosques read as crowns floating over stumps. A pollard is a stout
   trunk that ends *in* its crown. Rebuilt with trunk 0.38 m radius to 5.40 m and the crown
   spanning 4.90–11.00 m at 3.30 → 2.55 m radius. Same triangle count.
4. **Glow shells were being bevelled.** The bevel exclusion tested
   `obj.name.endswith("_glow")`, but the playground shells are named
   `play_glow_playground_n/s` — the token is a prefix there, not a suffix — so each
   48-triangle lit frame came back as 432. It had been inflating them since the first
   build and only surfaced when the four-box frame made it large enough to breach the
   budget (18,588). Now `"_glow" in obj.name`. Net effect of the final fix round: the
   gravel kerb, the restrained playground glow and the semantic-scale figures cost 700
   triangles, the bevel bug refunded 768, and the asset landed at **17,820**.
5. **Playground pads are raised (+0.42 m), not recessed** as the plan's §2.7 asked. A
   recessed pad would sit *below* the scored joint grid at +0.32 m and the joints would
   float across it. Raised pads also read better from above.

Three further changes came out of reviewing the corrected renders:

- **The gravel court did not read as a distinct shape.** `Toy_sand` (ece4d4),
  `Toy_cream` (f2ede3) and `Toy_stone` (d9d2c2) are all within ~6% of each other, so on
  the first aerial the central court melted into the surrounding paving — a failure of one
  of the six shapes §2.9 requires. Given a dark kerb reads at any distance and costs 48
  triangles, that was the cheaper fix than pushing a paving tone off-palette.
- **The playground glow was a lit pad, not a lit edge.** At night each 36 × 22 m pad
  out-shone the walk grid that is supposed to be the hero glow. Rebuilt as a perimeter
  frame, which is also the more plausible reading.
- **People were sub-pixel.** At 0.48 m across the figures vanished at the app's camera
  distance and the plaza read empty; enlarged to 0.72 m per style bible §9/§15.

A further change: **tree trunks moved from `Toy_rust` to `Toy_steel`.**
London plane bark is pale mottled grey-cream, not orange-brown, and 190 saturated trunks
were competing with the two playground pads for the eye in a composition whose whole point
is that the playgrounds are the only saturated accent (style bible §7).

The other three (address 355 not 335 McAllister; the Rickey sculpture measuring outside the
plaza polygon; the joint grid at 14 m rather than 6 m; walks modelled one box per OSM way)
are in `REFERENCE.md` §7.

## 5. Manifest draft

Not applied — integration is a separate job.

```json
{
  "id": "civic-center-plaza",
  "file": "civic-center-plaza.glb",
  "anchor": [-122.4176184, 37.7794818],
  "targetHeightM": 30.48,
  "cat": 0,
  "name": "Civic Center Plaza",
  "estimated": true,
  "dims": [145.612, 192.624, 30.48],
  "tris": 17703,
  "loadRadius": 2500
}
```

**Streaming decision (mandatory):** `loadRadius: 2500`, the default
`max(2500, 30.48 × 30 = 914)`. The usual caveat — beyond the radius the site is empty
because the baked buildings were carved out — is unusually gentle here: outside 2,500 m
this site is an empty park in the baked city, which is roughly what it should look like.
Not `alwaysLoaded`: at 30.48 m this is not a skyline piece.

`"estimated": true` because the height datum is an OSM tag (`height=30.48` on node
`7797674733`, a suspiciously round 100 ft), not a published dimension. Everything else in
the entry is measured.

## 6. Integration notes (Case B — do not apply in this stage)

Registry entry for `pipeline/lib/landmarks.mjs`:

```js
{
  // A 5-acre plaza, not a building: `exclude` has to clear the three kiosk
  // footprints the procedural builder extrudes to 22-23 m inside the plaza
  // (nearest vertices 67.8 / 74.2 / 83.5 m) without touching the first real
  // neighbour at 109.9 m. Measured against buildings/19_13.bin and 19_14.bin.
  id: 'civicCenterPlaza',
  name: 'Civic Center Plaza',
  lon: -122.4176184,
  lat: 37.7794818,
  height: 30.48,
  exclude: 95,
  clearTrees: true,
  clearTreesRadius: 110,
  camera: { distance: 620, yaw: 90, pitch: 30 },
}
```

Two things the integrator must not skip:

- **Three phantom towers stand in this plaza in the current build.** The garage kiosk, the
  Grove-corner cafe and the Pit Stop are single-storey structures the procedural builder
  extrudes to 22–23 m. Until the re-bake applies the exclusion, the asset cannot be judged:
  an unbaked check shows nothing wrong with a plaza that is in fact hidden behind three
  towers.
- **`clearTreesRadius` does not exist yet.** `treeblockers.mjs` currently reuses `exclude`
  as the tree-clear radius, and a 95 m tree-clear circle would delete real street trees on
  Larkin, McAllister and Grove. The proposed change is one line
  (`r: l.clearTreesRadius ?? l.exclude`). If it is declined, the fallback is `clearTrees`
  at the full 95 m and the loss of one block of street trees on each side — a deliberate,
  recorded decision, not a silent one.

Batch mode applies: run the bake, do the full QA on it, then
`git checkout -- app/public/tiles api/_data` and commit source only.

## 7. Reproducing

```bash
cd artifacts/civic-center-plaza
/Applications/Blender.app/Contents/MacOS/Blender -b --python build_civic_center_plaza.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python validate_civic_center_plaza.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python render_civic_center_plaza.py
/Applications/Blender.app/Contents/MacOS/Blender -b --python render_civic_center_plaza.py -- --night
python3 make_contact_sheet.py
```

The build is deterministic: all "random" variation comes from `hash01(index)`, the same
mixer `pipeline/lib/geo.mjs` uses, so a rebuild is diffable. The 190 tree positions, 35
flagpole positions and every polygon come from `data/plaza_uv.json`, which carries its OSM
provenance in the file.

## 8. Stage 4 — optimize

Run and passed; full detail in `optimize/REPORT.md`. Headlines: 949,380 → **479,064 bytes**
(−49.5%), 100 → **25 draw submeshes**, 94 → 19 objects, bbox and origin exact, worst
appearance delta **0.83%** against a 2%/4% gate, deterministic re-run reproduces the file
byte-for-byte. G6 falls short of the 60% aspiration for a documented reason: `-noq` is
mandatory in this app, and the asset is flat-shaded 450-solid geometry whose vertices
cannot be shared.

The optimized GLB is now the shipping file; the original is archived at
`optimize/input/civic-center-plaza.glb`. `validation.json` above re-runs against the
shipping file.

## 9. Approval

Stage 3 of the pipeline. The user pre-approved stages 3 onward in the invoking message
("I approve everything -- go ahead and do your thing. you dont need to ask for stage 3
approval. proceed w everything", 2026-08-13), so the pipeline advanced without a separate
approval round. The review set was still produced and reviewed, and four defects were
found in it — the east-west mirror, the lollipop trees, the illegible gravel court and the
over-bright playground glow — each fixed and re-rendered before the asset was frozen.


## 10. Stage 5 — integration (batch mode)

Case B. Source-only branch; the bake was run, QA'd, and discarded per
`ADDRESS-TO-ASSET.md` batch mode.

| Item | Result |
|---|---|
| Re-validation of the shipping GLB | **PASS** 19/19 |
| GLB dropped in `app/public/sf-assets/landmarks/` | 479,064 bytes, already meshopt-compressed at stage 4 |
| Manifest entry | added; JSON valid, 36 entries |
| id mapping | `civic-center-plaza` -> `civicCenterPlaza`, matches the registry |
| Registry entry | added: `exclude: 95`, `clearTrees`, `clearTreesRadius: 110`, camera yaw 90 |
| Re-bake | full chain ran; only 8 of 3,312 generated files differ, all in cells 19_13/19_14 |
| audit 1.6 | **PASS** — 42 landmarks clear |
| `verify-rebake` | **PASS** — 583/585 cells unchanged, nearest survivor 109.8 m vs 95 m |
| Footprints removed | exactly the 3 phantom kiosk towers (68.8 / 73.3 / 82.9 m; 88 / 93 / 10 m2; baked tops 22-23.4 m) |
| Single building at the site | PASS — no procedural twin, no baked block poking through |
| Scale factor | **x1.0000** — `sf-assets: civic-center-plaza merged 25 objects / 19 materials -> batched (10529 tris body); uniform x1.0000 at 1749, -1048` |
| Placement | (1749, -1048) vs plaza OBB centre (1749.6, -1049.2) |
| Orientation | PASS — playgrounds on the Larkin (east) side, court on the City Hall axis |
| Terrain seating | PASS — no floating, no sinking |
| Night glow | PASS — lit walk grid on a dark field; playground frames; lawns and bosques dark; nothing else lights |
| Fallback drill | **PASS** — exactly one warning, no crash, 26 other landmarks still live |
| Draw calls < 300 | **NOT MEASURED LOCALLY** — see below |
| lint / build | PASS / PASS |

### The tree radius was wrong, and only measuring caught it

`clearTreesRadius` shipped at 60 m on the theory that a wider circle would eat real
street trees on Larkin, McAllister and Grove. The first in-app screenshot showed **109
procedural lollipop trees still standing inside the plaza**, among the 190 hand-placed
pollards, looking like a different world. Counting against the baked landcover:

| radius | left inside the plaza | cut outside it |
|---:|---:|---:|
| 60 m | 109 | 0 |
| 80 m | 34 | 7 |
| 95 m | 6 | 10 |
| 110 m | **0** | **14** |

The blocks around the plaza are civic buildings with almost no mapped street trees, so
the feared regression was 14 trees, not hundreds. Set to 110 m; the re-bake dropped the
city tree count 178,282 -> 178,160, i.e. 122 trees, matching 109 + 14 (± sampling).

The lesson is the one `505VanNess` already taught for buildings and this asset had to
learn again for trees: **size the radius by counting against the real bake input, not by
reasoning about what a circle probably overlaps.** Both the registry comment and
`treeblockers.mjs` now say so.

### Draw calls — not measured locally, and why

The Browser pane stops its `requestAnimationFrame` loop between tool calls, so the
in-app stats overlay reports `fps 0 / draw calls 1` regardless of the scene. The tool
built for this is `pipeline/landmark-streaming-check.mjs`, which drives a headless
Chrome where rendering runs continuously; it needs a second preview server and this
session was already at the Browser pane's per-folder limit. **Run it against a
`vite preview` of the build before shipping.** The architectural expectation is that
this asset costs nothing extra: it merges into the shared landmark `BatchedMesh` pair
(2 draw calls for all landmarks, no matter how many), which the merge line confirms with
`-> batched`.

### Not done, deliberately

Push, PR and deployed production QA. `ADDRESS-TO-ASSET.md` replaces the
INTEGRATION-PROMPT's Step 7 with a stop, and batch mode ends at a source-only branch;
the city is baked once for the whole batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`,
which is also where the single PR is opened.
