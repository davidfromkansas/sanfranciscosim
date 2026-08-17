# 54-58 South Park — build report

Miniature GLB for SF-SIM, built 16-17 August 2026 from `docs/asset-plans/58-south-park.md`
via the address-to-asset pipeline (`docs/asset-pipeline/ADDRESS-TO-ASSET.md`), invoked with
`BUILDING: 58 S Park St, San Francisco, CA 94107`, `BATCH: yes`.

**This report beats the plan.** Where the dossier in the plan file and this report disagree,
this report and `REFERENCE.md` are correct.

## 1. Headline numbers

Both columns are real: the asset was built, approved, then optimized in stage 4
(`optimize/REPORT.md`). **The shipped column is what the manifest describes.**

| | As built | **Shipped (post-optimize)** |
|---|---|---|
| Triangles | 4,664 (cap 10,000) | **4,664** |
| Objects | 81 | **11** |
| Draw submeshes | 83 | **13** |
| Dimensions (AABB) | 28.3764 × 28.4853 × 16.90 m | identical to 5 dp |
| Min Z | 0.0 | 0.0 |
| XY centre offset | (0.136, −0.124) m | identical |
| Materials | 10, all `Toy_*`, flat, opaque, untextured | 10, identical set |
| Glow materials | `Toy_glass_Glow` | identical |
| File, raw | 281,428 B | **165,288 B (−41.3%)** |
| Contract validation | PASS on all 16 checks | **PASS on all 16 checks** |
| Anchor | `-122.3938881, 37.7821223` (assessor parcel centroid) | unchanged |
| Target height | 16.9 m — bbox top normalized exactly, so loader scale = 1.0 | unchanged |
| Parapet crest | 13.6 m | unchanged |
| Front heading | 135.2° true (south-east, onto South Park) | unchanged |

Compression is `EXT_meshopt_compression` without `KHR_mesh_quantization`, matching
`pipeline/compress-assets.mjs`. Full stage-4 detail in `optimize/REPORT.md`; the headline is
83 → 13 draw submeshes and a deliberate skip of the limited dissolve, because this asset's
three coplanar ring bands are exactly the case that manufactures invisible slivers.

The AABB is ~28.4 × 28.5 m for a 9.73 × 30.10 m building. That is the expected consequence
of authoring at the real 45.2° SoMa heading, not a scale error.

## 2. Corrections to the dossier made during the build

**The plan's biggest open question is resolved: the low element is at the REAR.** The plan
left it conditional — rear step or mid-depth lightwell — and said the two give visibly
different silhouettes. It was settled by pulling the Google satellite tiles at z21 as raw
imagery (tile `x=335579 y=810539 z=21` and its 8-neighbourhood, 59 mm/px) and registering
them against the assessor parcel polygon: the roof's rear parapet sits about **3 m in from
the rear lot line**, with the strip behind it in permanent shadow from the four-storey block
in front. The asset drops the rear **4.5 m** to 4.0 m. That is 15% of the lot against the
17% a two-level fit to the LiDAR moments wants, and 4.5 m is the depth the imagery supports.

**The same registration gave the roof its programme**, which the plan could only guess at:
furniture cluster at the park end, a planting run along the south-west parapet, a glazed
element mid-depth, and a dark ~3.8 × 3.5 m structure with an adjoining raised block toward
the rear. All four are in the asset, and the dark structure is the roof office that carries
the crest. Full table in `REFERENCE.md`.

**The footprint source changed from OSM to the assessor parcel.** The plan quoted the parcel
(9.73 × 30.10 m, 292.8 m²) and it is what was built, but it is worth stating why: OSM way
`124884349` is 3% smaller and shifted ~2.3 m north-west, and the DataSF LiDAR footprint
`SF3775219` is smaller again (258.9 m²) because it is roof-derived and inset. The parcel
matches the marketed lot area to 0.5% and shares its edges vertex-for-vertex with both
neighbours' parcels, which is what a real party-wall row looks like. This matters at
integration: the exclusion radius has to be measured against the files the bake reads, not
against this polygon (see §6).

**Nothing moved the height.** 13.6 m parapet and 16.9 m crest both survived. The crest keeps
its ±1 m caveat and `estimated: true` — see `REFERENCE.md`, "The height caveat".

## 3. Design decisions, and the ones that were reversed

**The two-tone stack is built as geometry, not as colour.** The dark charcoal top storey
stands `CAP_PROUD = 0.15 m` out of the plaster on the front elevation, so the split throws a
real shadow line. Colour alone flattens at diorama scale; this is the one place semantic
exaggeration was spent (style bible §22).

**The palette roles were inverted after the first aerial.** The first build used `Toy_sand`
(`ece4d4`) for the plaster body and `Toy_stone` (`d9d2c2`) for the roof deck. That is the
wrong way round twice over: the real plaster is a light warm *gray* and the real deck is
paler than the walls, and the render showed a cream building with a slightly darker roof,
which killed the roof read. The two were swapped — body `Toy_stone`, deck `Toy_sand`,
furniture `Toy_trim` (`f3efe6`) — giving a clean value ladder walls < deck < furniture.

**The roof office's coping was coplanar with the office's own top cap** in the first build
and rendered as a black hole from above. The office box now stops at `Z_CREST − 0.16` and
the coping slab caps it.

**The roof stair block moved from `Toy_stone` to `Toy_roofd`** so it groups with the office
into one dark cluster instead of reading as a third pale object (style bible §10: organise
into clear clusters, not scattered props).

**Deck furniture was scaled up ~35%** after the first aerial, where it read as crumbs.
Semantic scale (§9), not accuracy.

**The single-storey rear roof was blank** in the first build — a pale tray with a coping and
nothing in it, directly under the app's downward camera. It now carries a rooflight, a
condenser and a planter. Four objects, 432 triangles.

**The night preview's emission strength dropped from 3.0 to 1.8.** This asset's only glow
colour is the pale blue `Toy_glass_Glow` (`6f95b8`); at the 3.0 that 101 South Park uses for
its warm oak, every lit opening clipped to flat white and the glazed bay read as a hole
punched in the facade rather than as lit glass. Render-script only — the shipped asset is
unchanged.

**Both flanks are deliberately blank.** 44-46 South Park and 70 South Park are attached at
0.00 m. Nothing on those 30 m walls is visible in the real world or in the app, and no
budget was spent there.

## 4. Contract deviations, recorded

**"Front faces −Y" is not honoured, on purpose.** The asset is authored at its real-world
heading — Blender `+Y` = true north, front outward normal **135.2°** — because
`placeGeneric()` in `app/src/assets.js` applies no rotation. This is the deviation the plans
README calls out for the 45°-rotated SoMa grid; real-world orientation wins.

**Everything is a union of closed solids and there are no booleans.** Openings are not cut
into walls: each is a dark border ring standing proud of the wall with the glass standing
proud again inside it, and the eye reads the ring as a reveal. The rear elevation of the
four-storey block is reached by placing panels on `EDGE_REAR` at a negative offset, because
that wall stands 4.5 m in front of the rear lot line.

All objects pass the per-object signed-volume test outward — 81 as built, 11 after stage 4's
per-material join — and the 31,500-ray cast test returns 0 flipped visible faces in both.

## 5. Validation

`validation.json`, written by `validate_58_south_park.py` from a **fresh-scene re-import of
the exported GLB** (never the authoring scene). It was re-run after the stage-4 shipping
swap, so the numbers below describe the **packed file that ships**. All 16 checks PASS:

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS (16.9 m crest; 28.4 × 28.5 m AABB expected at 45°) |
| crest normalized to target | PASS (16.900 vs 16.9) |
| base at z = 0 | PASS (0.000) |
| centred in XY | PASS (0.136, −0.124) |
| under triangle budget | PASS (4,664 / 10,000) |
| no image textures | PASS |
| no transparency | PASS |
| materials follow contract | PASS (10, all `Toy_*`) |
| no cameras or lights | PASS |
| no animation, skin or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| normals outward, signed volume | PASS (11/11 after the stage-4 per-material join) |
| normals outward, ray residual | PASS (0.0%) |
| no degenerate geometry | PASS (0) |
| no unexpected objects | PASS |

## 6. Stage 5 — integration (Case B, batch mode)

Run 17 August 2026. `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1, Steps 1-6; Step 7 is
replaced by a stop, per `ADDRESS-TO-ASSET.md`.

### 6.1 The exclusion radius — 5 m

Measured against **both** files the bake actually reads, not against the parcel this asset is
built on, and remembering that `excluded()` in `pipeline/buildings.mjs` fires on a
footprint's centroid **or any ring vertex**, whichever is closer:

| ring | vertex | centroid | trigger |
|---|---|---|---|
| **this building, Overture `9c9ab1d7`** | 13.31 m | 1.31 m | **1.31 m** |
| **this building, DataSF `SF3775219`** | 14.13 m | 2.26 m | **2.26 m** ← the floor |
| 70 South Park, Overture `7c04d454` | 13.36 m | 7.75 m | 7.75 m ← the ceiling |
| 44-46 South Park, DataSF `SF3775217` | 14.03 m | 9.33 m | 9.33 m |
| 70 South Park, DataSF `SF3775053` | 13.68 m | 10.37 m | 10.37 m |
| 44-46 South Park, Overture `71b35ab5` | 13.31 m | 11.57 m | 11.57 m |

**Two rings are this building** — DataSF and Overture both trace it — and both have to drop,
or the survivor bakes a procedural block straight through the asset. Each ring was checked in
the building's own frame before trusting the distance: the two "ours" rings span the frontage
(v −4.8…+5.1 and −4.2…+4.6) and the four neighbour rings sit clear on either side
(−14.2…−4.5 and +4.5…+12.7). So the safe window is **(2.26, 7.75)** and **5** sits dead
centre with 2.74 m below and 2.75 m above.

Why the window is so much wider than 106 South Park's 2.1 despite the same party-wall
geometry: every ring here triggers on its **centroid**, not a vertex. The shared party-wall
edges are 30 m long, so their endpoints sit 13-14 m from this anchor and the vertex test
never fires inside the useful range.

### 6.2 Re-bake

Full chain — `terrain → bridges → buildings → streets → landcover → validate → lore → toy →
notables → context → muni-shapes`. `lore` before `toy`, and the chain run to the end, because
`context.mjs` imports `LANDMARKS` and the publish step drops `app/public/tiles/ctx/` and
`context/`.

Getting the raw data needed a workaround worth recording: **`npm run download` and
`npm run loredata` both abort at the Overture step**, because `overturemaps` 0.18.0 resolves
every release through `https://stac.overturemaps.org/catalog.json`, which now returns 404 —
and `--release=` does not help, since the same lookup backs the validation callback. The data
is fine (`s3://overturemaps-us-west-2/release/` still lists `2026-07-22.0`); only the index is
gone. Both files were fetched with a scratch wrapper that stubs
`overturemaps.core._get_stac_catalog` from the still-live `labs.overturemaps.org/data/releases.json`
and then calls the CLI unchanged. **This bake used the real 2026-07-22.0 Overture release**,
which matters: without it `buildings.mjs` skips the height gap-fill and the downtown skyline
bakes flat, and an exclusion radius judged against that bake would be judged against the
wrong city. The repo-side fix is filed separately; nothing about it is committed here.

| Check | Result |
|---|---|
| `pipeline/audit.mjs` check **1.6** — no procedural footprint inside a bespoke exclusion zone | **PASS** — 83 zones over 80 landmarks clear |
| `pipeline/verify-rebake.mjs` | **PASS** — 584 of 585 cells unchanged; `23_13` 201 → 200; nearest surviving footprint 13.7 m against the 5 m radius |
| audit overall | 29 pass, 3 fail, 1 informational. The three failures (1.2b p95 height, 1.3c Telegraph Hill terrain, 1.7b one sampled tree offshore) are city-wide source characteristics that pre-date this change and are untouched by a 5 m circle at South Park. |

### 6.3 Local QA

Driven by `qa_local.mjs` — the built app in headless Chrome over CDP, adapted from
`artifacts/340-brannan/qa_local.mjs` (constants only). Screenshots in `qa/`.

| Item | Result |
|---|---|
| Re-validation of the shipped GLB | **PASS** 16/16 (§5) |
| Manifest entry loads | **PASS** — `sf-assets: 58-south-park merged 13 objects / 10 materials -> batched (3610 tris body); uniform x1.0000 at 3838, -1340` |
| id mapping | **PASS** — `camelId('58-south-park')` → `58SouthPark`, matching the registry |
| Uniform scale | **PASS** — **x1.0000**: the authored crest and `targetHeightM` agree exactly |
| Placement | **PASS** — at (3838, −1340), the projected anchor |
| Single building | **PASS** — `qa/day.png`: one building on the site, no procedural twin, no z-fighting |
| Orientation | **PASS** — the front faces the park; the flanks are hard against both neighbours |
| Terrain seating | **PASS** — no float, no sink |
| Night glow | **PASS** — `qa/night.png` at 22:30: only the glazed bay, two middle-storey lights, one cap-band light and the roof-office window |
| Draw calls | **PASS** — 96/frame average at the landmark, against a 300 budget |
| Asset warnings | **PASS** — none; `failed: 0` across all 74 entries |
| Fallback drill | **PASS** — GLB served as 404: app boots, 67 landmarks still live, **exactly one** warning, and the site is empty ground inside the exclusion zone (`qa/drill-day.png`) — the expected Case B outcome |
| `npm run lint` | **PASS** |
| `npm test` | **PASS** — 26/26 |
| `npm run build` | **PASS** |

Two QA-harness corrections were needed and are recorded in `qa_local.mjs`:

1. The inherited harness waited for `stats().live > 0`, which is satisfied instantly by the
   resident/`alwaysLoaded` set and says nothing about a *streamed* landmark. `assets.js`
   scans on a cooldown driven by the **simulation** dt (`SCAN_EVERY_S = 0.4` against a
   clamped dt), so with several parallel headless sessions on this machine the pump advances
   ~0.05 s per frame at ~1 fps and this landmark took minutes of wall time to appear. The
   first run reported a **false FAIL**. It now waits for `assets.placed.has('58SouthPark')`.
2. `SF.setTime(t)` is deprecated and only maps `t` onto 19:00-21:30, so the "day" screenshot
   came out at 9:18 PM. `SF.setClock(msOrIso)` is the real override; day and night frames are
   now taken at a fixed 14:00 and 22:30.

### 6.4 Batch mode

The bake was run and QA'd, then discarded: `git checkout -- app/public/tiles api/_data`.
`git diff --name-only origin/main` lists **nothing** under `app/public/tiles/` or
`api/_data/`. The branch carries source only — the GLB, the manifest entry, the registry
entry, the plan and `artifacts/58-south-park/` — all of which merge mechanically. The city
gets baked once for the whole batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

## 7. Manifest entry (shipped numbers)

```json
{
  "id": "58-south-park",
  "file": "58-south-park.glb",
  "anchor": [
    -122.3938881,
    37.7821223
  ],
  "targetHeightM": 16.9,
  "cat": 2,
  "name": "54-58 South Park",
  "estimated": true,
  "dims": [
    28.3764,
    28.4853,
    16.9
  ],
  "tris": 4664,
  "loadRadius": 2500
}
```

`cat` is `2` (apartments): two dwellings over one commercial condo. `name` is the building's
real name; the id keeps the requested address. `estimated` is `true` because no crest height
is published anywhere.

## 8. Approval

Presented at gate 3 on 17 August 2026: contact sheet, aerial day and night renders, and the
numbers line.

The owner's approval for this run was given **in advance**, in the session's opening
instruction, verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

That is a standing authorization for the pipeline's internal gates, and it is what advances
this asset to stage 4. It is recorded here rather than treated as silent consent, and it is
weaker evidence than a decision taken after seeing the renders — if the design is revised
later, that is a normal stage-2 loop, not a broken gate.

It does **not** cover push, PR or deploy. Stage 5 still ends at a local commit and asks.
