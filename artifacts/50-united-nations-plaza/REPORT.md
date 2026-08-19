# 50 United Nations Plaza — build report

**Deliverable:** `50-united-nations-plaza.glb`, a validated miniature of the
Federal Office Building at 50 United Nations Plaza (Arthur Brown Jr., 1934–36),
built for the SF-SIM toy-diorama city.

REPORT beats plan. Where this file and
`docs/asset-plans/50-united-nations-plaza.md` differ, this file is the record of
what was actually built; `REFERENCE.md` is the record of what was measured.

## Numbers

| | |
|---|---|
| Triangles | **13,615** shipped / 24,000 cap (13,624 pre-optimize) |
| Dimensions (axis-aligned, m) | **122.73 × 84.90 × 33.00** |
| Oriented footprint | 112.53 × 66.93 m at bearing 80.92 deg, + 0.90 m cornice |
| `targetHeightM` | **33.0** — bbox top normalised to it exactly, loader scale = 1.000 |
| min Z / XY centre offset | 0.0000 m / (0.0000, 0.0000) m |
| Objects | **11** shipped, one per material (548 pre-optimize); the loader merges them into the shared batch at 2 draw calls |
| Materials | 11, all `Toy_*`, flat, opaque, no textures |
| Glow set | `Toy_gold_Glow` (6 arched entrances) + `Toy_white_Glow` (attic window band) |
| GLB on disk | **330,680 B raw / 156,263 B gzip** (939,600 raw pre-optimize, −64.8%) — under the 500 KB budget |
| Anchor | **−122.4144853, 37.7804351** (see "Corrections") |
| Category | 18 (Government) |

## Validation — `validation.json`, overall **PASS**

Fresh factory-reset Blender scene, re-importing the exported GLB. The authoring
`.blend` was not inspected.

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS |
| base at z = 0 | PASS (min Z 0.0000) |
| centred in XY | PASS (0.0000, 0.0000) |
| under triangle budget | PASS (13,624 / 24,000) |
| no image textures | PASS (0 images, 0 textured materials) |
| no transparency | PASS |
| materials follow contract | PASS (11 × `Toy_*`, no `Toy_body`) |
| no cameras or lights | PASS |
| no animation, skinning or constraints | PASS |
| transforms applied | PASS |
| no negative scales | PASS |
| **normals outward** | PASS |
| no degenerate geometry | PASS (0) |
| no unexpected objects | PASS |

**Normals method.** Every source mesh runs `bmesh.ops.recalc_face_normals` before
export. Because this asset is a *union of solids*, the authoritative test is
**per-object signed volume**: every object encloses a positive volume
(`negative_signed_volume_objects: []`) — 548 objects pre-optimize, the 11
per-material groups on the shipped file. Backing that up, 22,500 deterministic
visibility rays over 15 targets (the four wings and the courtyard at three heights)
produced **0 flipped visible faces** — a 0.000% residual against the 0.15%
allowance, both before and after optimization.

The table above was re-run **on the shipped (optimized) GLB**, not just the
pre-optimize export.

## What was built

Authored in Blender directly in world metres, Z up, +X east, +Y north, then the
whole assembly rotated **+9.08 deg about Z** so it drops into the city at its real
heading with no loader rotation. The hero front faces south onto United Nations
Plaza, so the contract's "front faces −Y" and the real-world heading agree to
within 9 degrees.

- **The ring.** Four abutting bars (south / north / west / east) tile the plan
  exactly, which is what makes the 72.2 × 27.1 m courtyard a real void while
  keeping every piece a closed convex solid.
- **The two south corners are concave scoops** — 8-segment arcs of R 10.4 m bowing
  6.9 m into the building, each carrying an arched entrance. The north corners are
  square. This asymmetry is the plan-level recognition cue.
- **Vertical composition, all four sides:** plinth; rusticated `Toy_stone` base to
  11.0 m with three reveal courses; belt course; a two-storey order to 22.1 m; a
  0.90 m projecting cornice at 23.2 m; a set-back attic behind a balustrade; a top
  cornice at 29.0 m; a hipped metal roof cresting at 33.0 m.
- **South front:** 18 free-standing Doric columns standing 0.85 m proud under that
  cornice, with a continuous balustrade band between them and three arched
  entrances at the centre. West, east and north get proud pilaster strips on the
  same 5.3 m rhythm.
- **North central wing** (|x| < 31 m) stops four storeys up: parapet at 24.7 m,
  flat deck at 23.4 m carrying a `Toy_mint` green roof, two `Toy_navy` PV banks,
  three white mechanical boxes and a `Toy_stone` gravel margin. Its two end
  pavilions stay full height, so the north side reads as a low centre between two
  taller granite pavilions.
- **Roof:** five hip bars of equal pitch (35 deg) and equal eave height. Where two
  meet at a right angle their planes intersect exactly on the 45-degree diagonal,
  which *is* the correct hip line, so the union needs no boolean.
- **Courtyard:** paved floor with a `Toy_sand` walk cross, two planting beds, eight
  tree pucks, light glazed-brick liners with vertical window slots on all four
  walls, and the 2013 elevator bulkhead on the east side.
- **Night:** six `Toy_gold_Glow` arched entrances (three south, one per concave
  corner, one north) and a continuous `Toy_white_Glow` attic window band that
  traces the cornice line all the way round — which is what gives this low, wide
  building a readable silhouette from the app's aerial camera after dark. Two glow
  sets, nothing else, no invented facade floodlighting.

## Palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `f2ede3` | main granite walls, attic storey |
| `Toy_stone` | `d9d2c2` | rusticated base, plinth, courtyard floor, gravel margin, bulkhead |
| `Toy_trim` | `f3efe6` | columns, pilasters, belt course, cornices, balustrades, parapets |
| `Toy_sand` | `ece4d4` | courtyard brick liners and walkways |
| `Toy_glass` | `2a4d73` | all windows and the arched openings |
| `Toy_steel` | `9aa0a6` | the standing-seam metal hip roof and its dormers |
| `Toy_navy` | `2c4a70` | the two photovoltaic banks |
| `Toy_mint` | `8fd0a8` | the green roof and courtyard trees — the one saturated accent |
| `Toy_white` | `f7f4ec` | rooftop mechanical boxes |
| `Toy_white_Glow` | `f7f4ec` | the attic window band (night) |
| `Toy_gold_Glow` | `caa64a` | the six arched entrances (night) |

`Toy_roofd` was deliberately **not** used for the metal roof: it renders as
rgb(9,9,12) on a roof deck in the app and would have turned the building's largest
visible surface black. `Toy_steel` is both the correct zinc colour and safe.

## Corrections and decisions

1. **The anchor moved 0.7 m.** The plan anchored on the OSM OBB centre
   (−122.4144797, 37.7804306). The model centres on its own bounding box, and
   because the two south corners are scooped while the north corners are square,
   that box centre sits 0.49 m east and 0.49 m south. **Shipped anchor:
   `−122.4144853, 37.7804351`**, reported by the build script.
2. **"Roof outline" in plan §2.4 means the CORNICE outline.** With the wall plane
   at 112.53 × 66.93 and a 0.90 m cornice projection, the cornice outline is
   114.33 × 68.73 m against DataSF's LiDAR box of 114.10 × 68.96 — agreement to
   0.25 m, which is the cross-check the plan intended. The metal roof itself sits
   inboard of that.
3. **Height confirmed, not corrected.** 33.0 m crest / 29.0 m parapet / 24.7 m
   north wing all re-derived independently in `REFERENCE.md` §3.
4. **18 columns, not ~26.** A deliberate rhythm reduction; the real count is read
   from photography and is itself *inferred*.
5. **No facade floodlighting.** A targeted search found no documented night scheme,
   so none was invented.

## Defects found and fixed during the build

Each of these shipped once in an intermediate render and was caught in review:

1. **Self-intersecting south outline.** The two concave corner arcs were spliced in
   the wrong order, so the south bar's polygon crossed itself and the whole base
   rendered as broken backfaces. Fixed by walking the outline CCW: west edge → SW
   scoop forward → south wall → SE scoop reversed → east edge.
2. **Black patches on the roof corners.** Overlapping hip bars had *coplanar* flat
   tops which z-fought to black. Each bar now crests a few centimetres below the
   one that hides it (south wins at the south corners, west/east over the
   pavilions).
3. **Whole window rows invisible.** Panes were placed at a single plane offset
   while the rusticated base stands 0.25 m proud of the body, so both base rows
   were buried inside the wall. Every storey now carries its own plane offset, and
   the clearance was raised from 0.01 m to 0.07 m — at 0.01 m a pane only showed
   where a rustication course happened to recess the wall behind it.
4. **Entrance arches invisible, then transparent.** First they were recessed behind
   the proud base (there are no booleans here, so anything behind that face never
   renders). Then, built as one solid whose outward face carried the glow material,
   they went see-through: at the loader's 12% day opacity the ray does *not* land
   on the solid's far cap but on the wall behind it (verified in Cycles with the
   glass recoloured red). The fix, applied to the attic windows too: **an opaque
   dark pane with a thin glow plate standing on its outer face**, so the day read
   is the pane's own colour and depends on nothing behind it.
5. **Corner arches edge-on.** `arch_prism` extrudes along `(-sin yaw, cos yaw)`, so
   the two concave corner entrances needed 135 deg, not the 45 deg their faces sit
   at. The yaw is now derived from the outward normal so it cannot be wrong again.
6. **Pilasters and windows floating in the scooped corners.** The west and east
   walls stop at the concave corners; their rhythms now start north of the scoop.
7. **The courtyard read as a striped billboard.** Horizontal storey bands on the
   courtyard walls became a barcode from the app's three-quarter camera. Replaced
   with vertical slots on the courtyard's own bay rhythm, which read as windows.
8. **Black square in the courtyard.** Two coplanar paving slabs, z-fighting.

## Files

```
artifacts/50-united-nations-plaza/
  build_50_united_nations_plaza.py     deterministic build (Blender headless)
  render_50_united_nations_plaza.py    controlled review renders of the EXPORT
  validate_50_united_nations_plaza.py  fresh-scene contract validation
  make_contact_sheet.py                composes the seven renders
  50-united-nations-plaza.blend
  50-united-nations-plaza.glb          the shipping asset (stage-4 optimized)
  optimize/                            stage-4: input archive, adapted scripts,
                                       four-variant table, A/B renders, REPORT
  50-united-nations-plaza-{north,east,south,west}.png   four elevations, one rig
  50-united-nations-plaza-top.png      courtyard, hip roof, green roof, PV
  50-united-nations-plaza-aerial.png   the app's high three-quarter camera
  50-united-nations-plaza-night.png    the glow set
  50-united-nations-plaza-contact-sheet.png
  qa_local.mjs                         stage-5 local QA over CDP (--drill)
  qa/                                  day/night/wide + the drill's three
  REFERENCE.md  REPORT.md  validation.json
```

Rebuild: `blender -b --python build_50_united_nations_plaza.py`
Re-render: `blender -b --python render_50_united_nations_plaza.py`
Re-validate: `blender -b --python validate_50_united_nations_plaza.py`

## Stage 5 — integrate (batch mode, source-only)

Run of `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1, Case B, with
ADDRESS-TO-ASSET's batch-mode amendment: the bake was run and fully QA'd, then
discarded, so this branch carries source only.

### Local QA — all PASS

`node artifacts/50-united-nations-plaza/qa_local.mjs` drives the BUILT app
(`app/dist`) in real headless Chrome over CDP rather than the editor's Browser
pane: parallel landmark sessions hold every preview slot, and a hidden pane
throttles `requestAnimationFrame` to nothing, which makes a perfectly healthy
streaming landmark look broken.

| Step 5 check | Result |
|---|---|
| manifest entry loads | PASS — `sf-assets: 50-united-nations-plaza merged 11 objects / 11 materials -> batched (7417 tris body); uniform x1.0000 at 2025, -1153` |
| uniform scale ≈ 1.0 | PASS — **x1.0000** exactly; the authored height and `targetHeightM` agree |
| exactly one building on the site | PASS — no procedural twin, no baked block poking through, no z-fighting (see `qa/wide.png`) |
| footprint size against the neighbours | PASS — reads as a whole city block, correctly larger in plan than the Asian Art Museum next door |
| orientation | PASS — the colonnade faces United Nations Plaza; no `yawDeg` override needed |
| terrain seating | PASS — no float, no sink |
| night glow | PASS — only the six arched entrances and the attic band light up (`qa/night.png`) |
| draw calls < 300 | PASS — **98/frame** at the landmark |
| no asset warnings | PASS — none |

`stats()` at the landmark: `{entries: 104, live: 83–89, fading: 0, failed: 0}`.
Screenshots in `qa/`: `day.png`, `night.png`, `wide.png`.

### Step 6 — fallback drill (mandatory), all PASS

The drill serves a real **404** for the GLB rather than renaming the file: Vite
answers a missing public path with `index.html` and HTTP 200, so the rename
trick cannot produce a fetch failure at all.

| Check | Result |
|---|---|
| app still boots with the GLB missing | PASS — `{entries: 104, live: 97, failed: 1}`, no crash |
| exactly one fallback warning | PASS — `sf-assets: 50-united-nations-plaza failed to load (… responded with 404: Not Found)` |
| Case B site behaviour | PASS — **empty ground** inside the exclusion zone, which is the documented Case B outcome, not a hole or a crash (`qa/drill-wide.png`) |

Note the warning *wording*: INTEGRATION-PROMPT Step 6 quotes the RESIDENT
fallback text ("… — keeping the code-built landmark"). A landmark with a
`loadRadius` is STREAMED and fails through `scan()` instead, with
`failed to load (…)` and no "keeping" suffix. The drill matches on the id, not
on the prompt's wording.

### The Case B re-bake

Ran the full chain — `terrain → bridges → buildings → streets → landcover →
validate → lore → toy → notables → context → muni-shapes`. Stopping at `toy` is
a trap: `context.mjs` owns this landmark's pick box, its search-index entry and
its `context/landmarks.json` row, and `validate.mjs` drops `tiles/ctx/` and
`context/` on publish.

- **`pipeline/audit.mjs` check 1.6 PASS** — "no procedural footprint inside a
  bespoke landmark exclusion zone — 114 zones over 110 landmarks clear".
  (Three unrelated checks fail on this bake and on the baseline: 1.2b p95
  height, 1.3c Telegraph Hill DEM, 1.7b one offshore tree. All three are
  city-wide terrain/source-data properties that no single landmark touches.)
- **`pipeline/verify-rebake.mjs` PASS** — "only the new landmarks' cells moved,
  and every asset has clear ground under it". 584 of 585 cells unchanged;
  `20_13` went 184 → 183; nearest surviving footprint 53.9 m against the 40 m
  radius.
- **Settled from the tile, not from the counts.** `verify-rebake` reported cell
  `19_13` as "exclusion dropped nothing", which is the known blind spot — it
  compares per-cell counts, and the circle overlaps that cell without any of
  this building's footprint living there. Decoding the baked blob directly:

  ```
  baked footprints in the 3x3 cell neighbourhood : 1918
  footprint VERTICES inside the 40 m exclusion   : 0
  distinct footprints intruding                  : 0
  nearest baked footprint vertex                 : 53.91 m
  ```

  53.91 m against the 54.54 m predicted from the raw rings before baking — the
  0.6 m is `simplifyRing` plus the 0.02 m tile quantisation.
- **The single-footprint delta is the two-ring story confirming itself.** On
  `main` the DataSF ring was baked, so Overture's ring was skipped by
  `occupiedFraction`. With DataSF excluded the block is empty, Overture's ring
  is attempted — and dropped by the same radius. Net 184 → 183. Without the
  Overture ring inside the radius the gap-fill would have put the building
  straight back and the count would not have moved at all.
- **Zero data-vintage churn.** The bake reused the same raw downloads that
  produced the committed tiles, so exactly one building tile changed. A bake off
  fresher downloads would have rewritten ~520 tiles that have nothing to do with
  this landmark.

### Batch mode — what this branch carries

Per `ADDRESS-TO-ASSET.md`, the bake was **discarded** after the QA above:
`git checkout -- app/public/tiles api/_data`. Sanity check against the
merge-base: `git diff --name-only 74aa2dbe8` lists **nothing** under
`app/public/tiles/` or `api/_data/`.

Source committed: the GLB (both under `artifacts/` and
`app/public/sf-assets/landmarks/`), the `landmarks_manifest.json` entry, the
`pipeline/lib/landmarks.mjs` entry, the asset plan and `artifacts/`. All three
shared files are append-only lists that merge mechanically. The city is baked
once for the whole batch by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

`cd app && npm test` → 26/26 pass. `npm run build` → clean.

### Not done, by design

Step 7 (push, PR, deploy, production QA) is replaced by a stop, per
ADDRESS-TO-ASSET stage 5. Nothing was pushed and no PR was opened.

## Draft manifest entry

```json
{
  "id": "50-united-nations-plaza",
  "file": "50-united-nations-plaza.glb",
  "anchor": [
    -122.4144853,
    37.7804351
  ],
  "targetHeightM": 33.0,
  "cat": 18,
  "name": "50 United Nations Plaza Federal Office Building",
  "estimated": false,
  "dims": [
    122.7264,
    84.8953,
    33.0
  ],
  "tris": 13615,
  "loadRadius": 2500
}
```

**This entry is now live in `app/public/sf-assets/landmarks_manifest.json`** (it
was appended as TEXT, not by re-serialising the file: `json.dumps` rewrites
floats like `11.0` → `11` across unrelated entries — 19 lines added, nothing
else touched).

`loadRadius` is the default rule `max(2500, 33.0 × 30)` = 2500 — the streaming
decision, made explicitly: at 33 m this building is small on screen well before
2.5 km, and because it is Case B the baked footprint is carved out, so past the
radius the site reads as empty ground rather than as a wrong building. 2500 m is
where that absence is illegible.

## Stage 4 — optimize

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; full write-up in
[`optimize/REPORT.md`](optimize/REPORT.md). All gates G1–G6 and G8 PASS
(G7 n/a, bake mode off).

939,600 → **330,680 bytes** (−64.8%), 548 → **11** draw submeshes, 13,624 →
13,615 tris, bbox and origin unchanged, all 11 material names preserved.
Maximum A/B pixel delta 0.139% mean absolute RGB against gates of 4% near /
2% far.

The judgment call: the **limited dissolve was declined**. All four
weld × dissolve variants were built and packed; the dissolve wins 2.8% raw and
loses 18% gzipped, and on an asset made almost entirely of coplanar ring bands
it is the one step that can manufacture hairline slivers which only fail *after*
the shipping swap. Weld alone was kept.

## Approval

Gate 3 was carried by a standing pre-approval given at the top of the session,
quoted verbatim:

> **"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"**

— David, 19 August 2026, in the same message that set `BUILDING: 50 United
Nations Plaza, San Francisco, CA 94102` and `BATCH: yes`.

The evidence was still presented before advancing: the contact sheet, the aerial
day and night renders, the top view, and the one line of numbers (13,624 tris;
122.73 x 84.90 x 33.00 m; 11 materials; 2 glow groups). No iteration was
requested.

Note that this standing approval is read as covering the pipeline's internal
gates only. It is **not** read as authorising a push, a PR or a deploy: batch
mode ends this session at a local source-only branch either way, and
`AGENTS.md` requires an explicit instruction for those.
