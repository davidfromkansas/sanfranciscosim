# 41–43 South Park — build report

**What was built:** a validated miniature GLB of the 1911 Edwardian two-flat at
41–43 South Park, San Francisco, for the SF-SIM toy-diorama city. It lives at
`artifacts/41-south-park/41-south-park.glb`.

`REPORT.md` and `REFERENCE.md` beat `docs/asset-plans/41-south-park.md` wherever
they disagree. Every disagreement is listed in §3.

## 1. Shipped numbers

The shipping file is the **stage-4 optimized** GLB (see `optimize/REPORT.md`);
the pre-optimize original is archived at `optimize/input/41-south-park.glb`.

| | Pre-optimize | **Shipped** |
|---|---|---|
| Objects | 72 | **13** |
| Draw submeshes (primitives) | 76 | **16** |
| Triangles | 6,380 | **6,380** (cap 8,000) |
| Vertices | 12,822 | 10,577 |
| Dimensions (AABB) | 22.456 × 22.473 × 10.600 m | **22.456 × 22.473 × 10.600 m** |
| Oriented footprint | 7.297 × 24.0 m | **7.297 × 24.0 m** (25.15 m including the 0.95 m bay projection and the 1.20 m stoop) |
| `min Z` | 0.0000 | **0.0000** |
| XY centre offset | 0.0000, 0.0000 | **0.0000, 0.0000** |
| Materials | 11, all `Toy_*`, no `Toy_body` | **11, identical set** |
| Glow materials | `Toy_glass_Glow`, `Toy_glassl_Glow`, `Toy_gold_Glow` | same three |
| Textures / cameras / lights / animations | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Degenerate triangles | 0 | **0** |
| Signed-volume outward objects | 72 / 72 | **13 / 13** |
| Visibility-ray flipped fraction | 0.0032% | **0.0032%** — gate is ≤ 0.15% |
| File size | 380,384 B raw / 78,623 B gzip | **173,108 B raw / 125,781 B gzip** (meshopt; budget ≤ 500 KB) |

The AABB is 22.5 × 22.5 m for a building that is 7.3 × 25.2 m. That is the
135.22° heading, not a scale error — the model is authored in world space so the
loader applies no rotation.

**Height normalization.** The bounding-box top is exactly **10.600 m** and it is
the cornice crest — not the parapet (10.10), not the terrace guard (10.48), not
the spa (10.47). The loader's `targetHeightM / measuredHeight` therefore lands on
1.0000.

**Anchor.** `DESIGN_ANCHOR` (the footprint's area centroid) is
`-122.3934770, 37.7815017`. The build recentres the model on its XY bbox centre,
a shift of (−0.199 m E, +0.206 m N), so the **manifest anchor is
`-122.3934793, 37.7815036`**. The shift exists because the stoop and the bays
hang off the front of the lot.

**Headings.** Street elevation faces **315.22°**; lot axis **135.22°**.

## 2. Contract validation

`validate_41_south_park.py` factory-resets Blender, re-imports the exported GLB
into a fresh isolated scene, and validates the re-import — never the authoring
scene. Full machine-readable output in `validation.json`.

**Overall: PASS.** All sixteen checks pass:

| Check | Result |
|---|---|
| metres and plausible dimensions | PASS |
| crest normalized to 10.60 m target | PASS |
| base at z = 0 | PASS |
| centred in XY | PASS |
| under triangle budget (6,380 / 8,000) | PASS |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS |
| no cameras or lights | PASS |
| no animation, skinning or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward — per-object signed volume | PASS (72/72) |
| normals outward — visibility-ray residual | PASS (0.0032%) |
| no degenerate geometry | PASS |
| no unexpected objects | PASS |

One deliberate WARN, not a FAIL: **`Toy_red` carries the off-palette hex
`6e3947`.** The real oxblood has no close palette entry (`Toy_rust` `a86444` is
far too orange, the palette's own `Toy_red` `c4453c` far too bright), the style
bible's San Francisco exception sanctions a tinted residential facade, and this
accent is the building's second-strongest recognition cue. The material keeps a
palette *name*, so the contract check and the loader's merge path are unaffected
— the same device `165-south-park` used for its siding.

## 3. Corrections made to the plan

**REPORT beats plan.** Eleven changes were made to `docs/asset-plans/41-south-park.md`
during the build. Two of them were real bugs found by the validator.

### Bugs

1. **The arch spandrel polygon duplicated its two springing corners.** The
   semicircular arc was generated inclusive of `ang = 0` and `ang = π`, which
   repeats the rectangle's bottom two vertices. Blender exported degenerate
   slivers there, and the object accounted for **28 of the 52 flipped
   visibility rays**. Fixed by generating interior arc points only
   (`range(1, steps)`), and the arc was refined from 10 segments to 12.

2. **`inset_polygon()` resolved "inward" against the building's footprint
   centroid.** That is correct for the roof parapet, which is concentric with the
   building, and wrong for anything that is not: the spa's ring sits about 5 m
   off that centroid, so the near half of the ring inset *outward* and the
   annulus self-intersected. It accounted for **23 of the remaining 24 flipped
   rays**. Fixed by giving `inset_polygon()` and `rim()` an explicit `centre`
   argument, defaulting to the old behaviour so the parapet is unchanged.

   Normals residual across the three passes: 51 rays (0.162%, FAIL) → 24 rays
   (0.076%) after fix 1 → **1 ray (0.0032%)** after fix 2. Every per-object
   signed volume was positive throughout; the ray test is what found both.

### Design corrections

3. **The body split moved from the arch crown (5.15 m) to the storey line
   (5.60 m).** The building is two closed solids because the ground storey
   carries the entry notch. Split at the crown, the seam rendered as a second
   horizontal line 0.45 m below the bay's belt course, and on a blank 24 m party
   flank two parallel lines that close together read as a modelling error.

4. **The roof terrace moved from mid-roof to the front half** (u 12.5–15.5 →
   9.6–13.4) and grew from 4.0 × 3.0 to 4.2 × 3.8 m. The plan placed it on the
   nadir imagery alone; three independent sources say it *overlooks South Park*,
   and mid-roof left 12 m of blank membrane at the street end, which is where
   the app's camera looks first. The imagery's registration error on this block
   is 2–3 m, so both readings are satisfied.

5. **A slatted timber guard (0.45 m) was added on the terrace's street edge and
   two flanks.** It is what makes the deck read as an occupied place rather than
   a coloured rectangle, and it is the only thing on the roof with a vertical
   face. It was first drawn at 0.60 m, which put its top at 10.63 m and stole
   the bounding-box maximum from the cornice crest — the one number the loader's
   scale depends on. Reduced to 0.45 m (top 10.48 m).

6. **The spa shell became an annulus.** Built as a solid cylinder (the plan's
   recipe step 14), its top cap covered the water and the whole thing rendered as
   a grey pancake from the app's own camera angle. The water now sits 40 mm under
   the rim rather than 70, because deeper than that the shell shadows it back to
   the same grey.

7. **Skylights enlarged from 1.2 × 0.9 m to 2.0 × 1.4 m.** The sources say "huge
   rollaway skylights"; at the plan's size they read as two blue chips on an
   otherwise empty 24 m slab.

8. **A roof hatch was added** (0.55 m tall, 1.5 × 1.3 m), which the plan's recipe
   does not list. It is inferred from function rather than from a source: a roof
   terrace has to be reachable. It is also the only structure on the present roof
   that could plausibly relate to the unexplained 11.88 m LiDAR maximum, and it
   is nowhere near that height.

9. **A 0.03 m overlap (`LAP`) was introduced at every stacked interface** —
   window relief layers into their host wall, cornice band to cornice band, bay
   aprons into the bays, stoop riser into riser, roof furniture into the deck,
   recess linings into the notch. Butted solids leave coincident face pairs; this
   was a systematic cleanup done while chasing the normals residual. It was *not*
   the cause of the residual (bugs 1 and 2 were), but it is correct and it stayed.

10. **The spa's glow disc now bites into the water rather than sitting on it.**
    Butted at the same z, the two caps were coincident and the water surface
    speckled with z-fighting — visible only in the stage-4 near A/B render, where
    Phase B's weld happened to fix it downstream. Fixed at source and the whole
    chain re-run; see `optimize/REPORT.md` §6.

11. **The dentil course is a continuous pale band, not modelled dentils.** The
    plan sanctioned this; recording it because it is the most visible
    simplification on the facade. At 300–500 m a pale line under a dark crown is
    exactly the dentil read, and 24 modelled blocks would have cost ~1,200
    triangles.

## 4. Judgment against the plan's "must capture" list

| Cue | Delivered |
|---|---|
| 1. The asymmetric bays — SW two-storey, NE one-storey | Yes. Verified in the aerial and north-west renders. |
| 2. The oxblood top-storey NE bay | Yes, `Toy_red` `6e3947`, on that bay and nothing else. |
| 3. The recessed arched entry on a stoop | Yes — a real 0.80 m notch in the ground-storey plan with a 12-segment arch spandrel across it and five risers climbing in. It reads as a hole, not a painted arch. |
| 4. The heavy bracketed cornice with a dentil band, returning over each bay | Yes — three bands following the front profile *including* both bay projections. It is also what draws the street end in the top view. |
| 5. The garage door | Yes, 3.10 m wide, layered relief with three grooves. |
| 6. The 7.3 : 24 proportion | Yes, exactly, from the surveyed parcel. |
| 7. The roof terrace with its spa | Yes, plus two skylights and a hatch. |

**Mirror check (the plan's non-negotiable):** in the top and north-west renders
the **oxblood bay and the entry stoop are on the north-east half** and the
**garage is on the south-west half**, matching the Compass photograph read with
the park behind the camera. PASS.

## 5. Approval (pipeline gate 3)

The pipeline's stage-3 human gate was pre-granted for this session. David's
invocation, verbatim, 16 August 2026:

> BUILDING: 41-43 S Park St, San Francisco, CA 94107
>
> BATCH: yes
>
> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Recorded as the gate-3 approval on **16 August 2026**. The contact sheet, the
day and night aerials and the numbers in §1 are presented in the session summary
rather than held for a reply; the pipeline continues to stage 4. This is a
standing pre-approval of the asset review only — it does not extend to pushing,
opening a PR, or deploying, which `ADDRESS-TO-ASSET.md` stage 5 reserves for an
explicit instruction.

## 6. Files

| File | What it is |
|---|---|
| `build_41_south_park.py` | the deterministic build — `blender -b --python build_41_south_park.py -- [--out DIR]` |
| `render_41_south_park.py` | the review rig — add `--night` for the dusk pass, `--only aerial` for the iteration view |
| `validate_41_south_park.py` | fresh-scene contract validation → `validation.json` |
| `make_contact_sheet.py` | composes the seven renders into the contact sheet |
| `41-south-park.blend`, `41-south-park.glb` | the authoring scene and the shipping asset |
| `REFERENCE.md` | the verified dossier: sources, dimensions, orientation, every elevation, uncertainties |
| `validation.json` | machine-readable validation output |
| renders | `-aerial`, `-aerial-night`, `-top`, `-north-west`, `-north-east`, `-south-east`, `-south-west`, `-contact-sheet` |

## 7. Draft manifest entry

```json
{
  "id": "41-south-park",
  "file": "41-south-park.glb",
  "anchor": [
    -122.3934793,
    37.7815036
  ],
  "targetHeightM": 10.6,
  "cat": 1,
  "name": "41–43 South Park",
  "estimated": true,
  "dims": [
    22.4556,
    22.4731,
    10.6
  ],
  "tris": 6380,
  "loadRadius": 2500
}
```

`"estimated": true` because the 10.60 m crest is photogrammetric, not published
(`REFERENCE.md` §9.1). `cat: 1` is House. `loadRadius` is the default rule,
`max(2500, 10.6 × 30) = 2500`.

## 8. Integration (stage 5, batch mode)

**Case B** — new landmark, so a registry entry and a tile re-bake were both
required. `BATCH: yes`, so the bake was run, verified, and then **discarded**;
this branch commits source only.

### 8.1 What was committed

| File | Change |
|---|---|
| `app/public/sf-assets/landmarks/41-south-park.glb` | new, 173,108 B, byte-identical to `artifacts/41-south-park/41-south-park.glb` |
| `app/public/sf-assets/landmarks_manifest.json` | +19 lines, one entry appended **as text** (a JSON round-trip rewrites `11.0` → `11` across six unrelated landmarks) |
| `pipeline/lib/landmarks.mjs` | +43 lines, one `LANDMARKS` entry with its measurement rationale |
| `docs/asset-plans/41-south-park.md`, `docs/asset-plans/README.md` | the plan and its README row |
| `artifacts/41-south-park/**` | the asset, scripts, renders, dossier and reports |

`git diff --stat origin/main` over the three shared append-only files is
**insertions only** (19 + 43 + 1), and lists nothing under `app/public/tiles/`
or `api/_data/` — the batch-mode sanity check in `ADDRESS-TO-ASSET.md`.

### 8.2 The registry entry, and how the radius was sized

```js
{
  id: '41SouthPark',
  name: '41-43 South Park',
  lon: -122.3934867,
  lat: 37.7815158,
  height: 10.6,
  exclude: 2.8,
  camera: { distance: 150, yaw: 225, pitch: 26 },
}
```

`camelId('41-south-park')` → `41SouthPark`, verified against the registry id, so
the loader hides the procedural version.

**The plan's exclusion numbers were replaced.** The plan sized `exclude` against
OSM standing in for Overture, because `pipeline/data/` is gitignored and was not
available when it was written. With the real bake input on disk the picture
changed materially, and the entry now carries the measured table. From the
registry point above:

| Ring | Triggers at | Verdict |
|---|---|---|
| DataSF `SF3775040` — ours | **0.57 m** (centroid) | must drop |
| Overture 177 m² — ours | **1.83 m** (centroid) | must drop |
| DataSF `SF3775039` — 45–49 South Park | **3.73 m** (nearest vertex) | must survive |
| Overture 272 m² — 45–49 South Park | 8.71 m | must survive |
| Overture 791 m² — 35 South Park | 11.08 m | must survive |
| DataSF `SF3775102` — 35 South Park | 12.12 m | must survive |

Safe window **(1.83, 3.73) m**; `2.8` sits in it with 0.97 m of margin below and
0.93 m above. The same measurement taken at the manifest anchor gives a window
of only (2.74, 3.16) — 0.42 m wide, the same knife-edge `165-south-park` had —
which is why the registry `lon`/`lat` is offset **1.50 m** from the manifest
anchor. These are independent fields: `placeGeneric` in `app/src/assets.js`
positions the GLB from the **manifest** anchor alone, and the registry point is
only the centre of the bake-time exclusion circle (plus the search and camera
target, where 1.5 m on a 7 m building flown to from 150 m is not visible).

**No `clearTrees`.** The street tree in front of this house is real, and South
Park's furniture sits inside the oval, outside the lot.

**The plan predicted two rings would disappear; one did.** Both datasets trace
this building, so a correct radius *offers* to drop two — but the bake's
`occupiedFraction(bbox) > 0.25` test blocks the Overture gap-fill here, because
the two party-wall neighbours' bounding boxes already cover this lot's box. The
radius still has to clear the Overture ring in case that changes; it does.

### 8.3 The re-bake

Full chain per `INTEGRATION-PROMPT.md` Step 4.2, nothing skipped:
`terrain → bridges → buildings → streets → landcover → validate → lore → toy →
notables → context → muni-shapes`. `pipeline/data/` was cloned (APFS
copy-on-write) from a sibling worktree rather than re-downloaded;
`pipeline/out/` was generated fresh, never seeded.

| Check | Result |
|---|---|
| `validate.mjs` | all checks ok, including `landmark in extent: 41-43 South Park — cell 23_13` |
| `verify-rebake.mjs` | **PASS** — 584 of 585 cells unchanged; `23_13  201 → 200`; nearest surviving footprint 3.7 m vs the 2.8 m radius |
| `audit.mjs` check **1.6** | **PASS** — no procedural footprint inside a bespoke landmark exclusion zone, 83 zones over 80 landmarks clear |
| `audit.mjs` overall | 29 passed, 3 failed, 1 informational. The three failures (`1.2b` p95 height, `1.3c` Telegraph Hill DEM, `1.7b` one offshore tree in 792 sampled) are **pre-existing and citywide** — identical on the `358-brannan`, `524-second` and `84-south-park` worktrees. Not caused by this landmark. |
| `app` lint + tests | `eslint src test` clean; `node --test` 6/6 pass |

The `pipeline/data/` snapshot reproduced `main`'s tiles exactly — only the one
cell this landmark touches changed its building count, so there is no
data-vintage drift to explain.

### 8.4 Local verification

| Item | Result | Evidence |
|---|---|---|
| Manifest served from this worktree | **PASS** | `curl localhost:5400/sf-assets/landmarks_manifest.json` → 74 entries, last is `41-south-park` |
| GLB served | **PASS** | `HTTP/1.1 200`, `Content-Length: 173108` |
| id mapping | **PASS** | `camelId('41-south-park')` → `41SouthPark` = the registry id |
| Scale factor | **PASS, exactly 1.0000** | `targetHeightM` 10.6 ÷ measured bbox height 10.600 |
| Camera preset lands on the building | **PASS** | `SF.rig.state.pivot` = (3873.64, 11.58, −1271.61) — the manifest anchor's projected position; `yawDeg` 225.0, `pitchDeg` 26.0 |
| Terrain seating | **PASS** | pivot ground 11.58 m against a LiDAR ground median of 11.76 m NAVD88 over the footprint with a 0.67 m range — a flat site, which is the case `placeGeneric`'s single terrain sample is right for |
| Orientation | **PASS** | authored in world space at 315.22°; the loader applies no rotation and the manifest carries no `yawDeg` override |
| **Exactly one building on the site** | **PASS** | settled from the baked tile rather than the screen: `app/public/tiles/buildings/23_13.bin` decoded and every one of its 200 surviving rings clipped against the asset's 175.1 m² design footprint. **True interior overlap: 0.000 m².** Two rings *touch* the footprint — 45–49 South Park and its rear building — but only along shared party-wall vertices, which is what a row of party-wall houses is. |
| Day/night appearance, draw calls | see 8.5 | |
| Fallback drill | see 8.5 | |

### 8.5 In-app verification, and what the machine would not allow

The loader-side evidence is complete and unambiguous. The **console merge line**,
captured from a real headless-Chrome run against the dev server:

```
sf-assets: 41-south-park merged 16 objects / 11 materials -> batched (3458 tris body); uniform x1.0000 at 3874, -1272
```

| Item | Result |
|---|---|
| Loader picks the asset up | **PASS** — 16 objects / 11 materials, the exact counts the optimize pass produced |
| Merged into the shared batch | **PASS** — `-> batched`, so it joins the one `BatchedMesh` pair and adds **zero** draw calls (`AGENTS.md`, streaming & batching) |
| Scale factor | **PASS, `uniform x1.0000`** — the authored crest and `targetHeightM` agree exactly |
| Placement | **PASS** — `at 3874, -1272`, the manifest anchor's projected position |
| Streaming | **PASS** — `{entries: 74, far: 6, loading: 0, live: 68, fading: 0, failed: 0}` with the camera at the preset; the entry moves out of `far` on approach as `loadRadius: 2500` intends |
| Load failures | **PASS** — `failed: 0`, and no 404 or parse error for this asset in the console |

#### The fallback drill (Step 6) — PASS

Run as its own pass, with no `renderer.render()` anywhere in it: the drill needs
no pixels, only that the app survives and the entry fails cleanly.

| Item | Result |
|---|---|
| App still boots with the GLB moved aside | **PASS** — `SF.boot.cleared === true` |
| The entry fails, and only that entry | **PASS** — `{entries: 74, far: 6, loading: 0, live: 67, fading: 0, failed: 1}` |
| Exactly one console line for this landmark | **PASS** — `sf-assets: 41-south-park failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)` |
| Every other landmark unaffected | **PASS** — 66 other `merged … -> batched` lines in the same session |
| The city still renders | **PASS** — 1,144 / 1,656 cells, 18,897 trees, 11,344 kit instances, 4,109 street-furniture pieces |
| Case B site behaviour | empty ground inside the exclusion zone — expected, and noted per the prompt |
| GLB restored afterwards | **PASS** — byte-identical to `artifacts/41-south-park/41-south-park.glb` |

The failure is a *parse* error rather than a 404 because Vite's dev server
answers a missing `public/` path with the SPA `index.html` and HTTP 200
(measured: 2,340 B). That is a dev-server artifact, not a loader bug, and the
drill still proves what it exists to prove — rule 3 holds: one warning, no crash,
no hole anywhere else.

**Two items could not be completed on this machine and are honestly outstanding**
— in-app day/night screenshots and a measured draw-call count. The cause is
machine contention, not the asset: this landmark was built
alongside ~20 sibling `ADDRESS-TO-ASSET` sessions and the Mac sat at a load
average of **150–340** throughout. Concretely:

- Headless Chrome reports `document.hidden === false`, yet a hand-installed rAF
  counter measured **1 frame in 2 seconds**. The app's own render loop is
  therefore effectively stopped, which is why the streaming scan had to be pumped
  by hand (`SF.assets.update(SF.camera.position, 0.25)` on a 250 ms interval) to
  produce the numbers above at all.
- A **single** synchronous `renderer.render(scene, camera)` — the standard way to
  read a true draw-call count, since the stats overlay measures the post-process
  quad instead — did not return inside 180 s and blocked the renderer thread for
  every later CDP call. `Page.captureScreenshot` behaved the same way.

What the draw-call budget rests on instead: the merge line proves this asset went
into the **shared batch**, which is 2 draw calls for every generic landmark in
the city, however many there are. It cannot move the count. The measured figure
for a comparable state on an idle machine is 120 calls at a landmark and 113 at
street level downtown, against the 300 budget.

**Deferred to `BATCH-INTEGRATE.md`, explicitly:**

1. Day and night screenshots at the camera preset, and the wide shot.
2. A hooked draw-call measurement (`renderer.render` wrapped, max per frame).
3. `node pipeline/landmark-streaming-check.mjs` against a build — `AGENTS.md`
   asks for this "after a batch of integrations", and this asset makes
   twenty-one landmarks sharing one `loadRadius` centre, the densest cluster in
   the manifest.

None of these can hide an asset defect that the stage-2 validator, the stage-4
gates, the tile clipping test in 8.4 and the merge line above have not already
ruled out — but they are not done, and this branch should not be treated as
production-verified until the batch run does them.
