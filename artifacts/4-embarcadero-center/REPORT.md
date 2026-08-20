# Four Embarcadero Center — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` for
`BUILDING: 4 Embarcadero Center, San Francisco` (`BATCH: yes`).

**Deliverable:** `4-embarcadero-center.glb` — a 179.00 m miniature of Four
Embarcadero Center (55 Clay Street), authored at its real-world heading, 17,904
triangles, all contract checks PASS.

| | |
|---|---|
| Manifest id | `4-embarcadero-center` |
| Anchor (WGS84) | −122.3961998, 37.7953001 |
| Long-axis bearing | 81.09° true; entrance faces **north** (351.09°) |
| Bbox (x, y, z) | 73.02 × 51.98 × **179.000** m |
| min Z / XY centre offset | 0.000 m / (0.310, 0.000) m |
| Triangles | **17,904** (cap 20,000) |
| Objects | 9 shipped (869 pre-optimize) |
| File | **466 KB raw** shipped (1,306 KB pre-optimize, −64.3%) |
| Materials | 9, all `Toy_*`, flat, opaque |
| Glow materials | `Toy_glassl_Glow`, `Toy_red_Glow` |
| Validation | `validation.json` — **overall PASS**, 16/16 checks (re-run on the shipped file) |
| Optimize | `optimize/REPORT.md` — all eight gates PASS, 882 primitives → 10 |

## Corrections this build made to the plan

**REPORT beats plan.** The plan (`docs/asset-plans/4-embarcadero-center.md`) was
re-verified before modelling; these are the places the build departs from it.

1. **The crown is not "three tiers per end zone applied to the whole strip".**
   The plan's §2.8 read as though the six depth-strips carried their tier height
   for the tower's full length. They do not: the near-orthographic north
   elevation (SFYIMBY / Sue Bierman Park) shows a single flat roofline across
   the length, so the stepping is confined to the **outer 10 m at each end**
   (`U_END_E = ±21.70`). The middle 43.4 m of the slab is flat-topped at 173.70.
   This is the reading that satisfies *both* the north elevation and the east-end
   crown photograph; the plan's wording satisfied only the second.

2. **The plan's §2.7 plan-projection exaggeration was not applied as written.**
   It proposed pushing the west spine out from 1.7 m proud to ~3 m. Extending
   the spine would have lengthened the building past its measured 63.45 m, so
   the same read was bought by **recessing the west end's south flank** instead
   (strips 5 and 6 from the measured −30.20 to −29.40 / −28.60). The overall
   −31.72 … +31.73 extent is exactly the measured one.

3. **The long-face window grid runs the full length, not the core span.** The
   first build glazed only `|u| ≤ 21.70` and left the end zones blank; the north
   elevation immediately showed it. The modules now span each long face's true
   extent and drop to the outer fin's parapet beyond the end-zone line.

4. **The crown glow is one pane row's upper 40%, not a band.** Two full rows —
   and, before that, a dedicated ring band — put a pale-blue block across the top
   third of the tower **in daylight**, which is not what the building looks like.
   A `_Glow` material's base colour is its day colour, so a large glow surface is
   a large day-visible surface. The crown is now the top ~8 m of the topmost pane
   row on every module, which still gives three descending lit rings at night
   (each tier's modules end at its own height) and reads as a modest accent by
   day.

5. **`Toy_roofd` is not used anywhere.** It renders near-black on a horizontal
   deck under the app's lighting; the roof, cooling towers and curbs are
   `Toy_steel`.

6. **Module count** came down from the plan's 22 per long face to 20 (pitch
   2.17 m, giving 24 modules across the longer real face extent) to stay inside
   the triangle cap after the full-length glazing fix.

## Height decision

`targetHeightM` is **179.00 m** and the bbox top is normalised to it exactly, so
the loader's `targetHeightM / measuredHeight` scale lands at 1.0.

- 173.70 m is CTBUH's *architectural* top and is the main parapet. It explicitly
  excludes functional-technical equipment.
- 179.05 m is DataSF LiDAR's `hgt_maxcm` over the footprint — 5.35 m above the
  parapet, which is one cooling-tower's worth, and the Google z20 roof plan shows
  exactly four of them.
- Repo convention for a plant crest is to ship the crest (cf. `300-brannan`,
  "25.2 m penthouse crest; 21.34 m parapet"), and AGENTS rule 5 wants the real
  thing in the scene.

The flagpole is deliberately not modelled — too thin for the toy style, and
LiDAR did not catch it either.

## Orientation

Authored with Blender `+Y` = true north, `+X` = east, geometry generated
directly in world space through a `uv(u, v)` map that bakes the 81.09° bearing
in, so transforms are already applied and the loader rotates nothing. The
entrance is on the **north** face (55 Clay Street), so the kit's `-Y` front
convention is *not* satisfied; this is a true-world-oriented landmark like
`555-california`, and that is the intended behaviour for `placeGeneric`.

## Night state

- **Hero:** the crown ring — the top of every module's topmost pane row. Because
  the end-zone modules stop at 135.10 / 154.40 and the core at 173.70, this
  reads as three descending lit rings wrapping the chevron.
- **Supporting:** a seeded (never random) ~1-in-3 scatter of lit window panes
  down the shaft, and the Clay Street lobby band.
- **Accent:** one `Toy_red_Glow` aviation bead on the spine.
- Every glow surface is a thin shell proud of its opaque `Toy_glass` pane, never
  a primary surface and never a closed shell around the body — so the daytime
  facade is not tinted.
- Day check: `Toy_glassl_Glow` is `#6f95b8`, a pale sky-blue that sits beside
  `Toy_glass` `#2a4d73` as a window catching light rather than as a different
  material.

## Validation

`validate_4_embarcadero_center.py` factory-resets Blender, imports **only the
exported GLB**, and reports on the re-import. All 16 checks PASS:

meters and plausible dimensions · crest normalised to 179.00 · base at z = 0 ·
centred in XY · under triangle budget · no image textures · no transparency ·
materials follow contract · no cameras or lights · no animation, skin or
constraints · transforms applied · no negative scales · normals outward by
per-object signed volume (869/869 positive) · normals outward by ray residual
(**0/31,500 flipped visible faces**) · no degenerate geometry · no unexpected
objects.

## Files

| File | What it is |
|---|---|
| `build_4_embarcadero_center.py` | deterministic build (`blender -b --python …`) |
| `render_4_embarcadero_center.py` | the review rig (`--only VIEW`, `--night`, `--samples N`) |
| `validate_4_embarcadero_center.py` | fresh-scene contract validation |
| `make_contact_sheet.py` | composes the contact sheet |
| `4-embarcadero-center.blend` / `.glb` | source scene and the shipping asset |
| `4-embarcadero-center-{north,east,south,west,top,aerial,night}.png` | review renders |
| `4-embarcadero-center-contact-sheet.png` | all seven, labelled |
| `validation.json` | the machine-readable report |

## Draft manifest entry

```json
{
  "id": "4-embarcadero-center",
  "file": "4-embarcadero-center.glb",
  "anchor": [
    -122.3961998,
    37.7953001
  ],
  "targetHeightM": 179.0,
  "cat": 3,
  "name": "Four Embarcadero Center",
  "estimated": false,
  "dims": [
    73.02,
    51.98,
    179.0
  ],
  "tris": 17904
}
```

`loadRadius` is deliberately absent — see the integration notes in the plan's
§2.13: at 179 m this is a skyline piece, and every other manifest landmark over
100 m stays resident.

## Stage 4 — optimize

Run with the pipeline defaults (`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`). Full detail in `optimize/REPORT.md`; the two judgment calls:

- **Pack-only lost, and could not have shipped anyway.** A gltfpack-only build
  (Phase B skipped) is smaller gzipped but 78% larger raw, because this asset's
  waste is object-count overhead — 882 primitives for 17,904 triangles — not
  vertex layout. It also fails the contract validator: the build leaves two
  degenerate triangles that only Phase B's degenerate pass removes.
- **The limited dissolve was measured and rejected.** Worth 7.9% of the bytes,
  but this asset carries 14 large coplanar ring bands and the dissolve
  manufactures a hairline sliver in the packed file — 1 degenerate triangle,
  `no_degenerate_geometry` FAIL. Shipped with `--no-dissolve`.

Shipped: 1,337,932 → **477,540** bytes (−64.3%), vertices 34,813 → 10,662
(−69%), triangles unchanged at 17,904, bbox and origin identical to 4 dp,
max A/B pixel delta 0.338% against a 4%/2% budget.

## Stage 5 — integration (BATCH: yes, source-only)

Case B. `pipeline/lib/landmarks.mjs` gains `4EmbarcaderoCenter`
(`camelId('4-embarcadero-center')` round-trips, verified against
`buildings.mjs`'s kebab regex), the manifest gains one 18-line append written as
text, and the GLB is copied to `app/public/sf-assets/landmarks/` unchanged
(sha256 identical to the artifact; `compress-assets.mjs` correctly skipped it as
already meshopt-compressed).

### The exclusion radius: 20 m, measured, not guessed

The plan's §2.13 suggested starting at 45 and sizing the final value against the
real bake input. Measured against `pipeline/data/` (DataSF + Overture, the two
sources `buildings.mjs` actually reads), only **two rings overlap the tower's
footprint**, and `excluded()` gates on `min(centroid, any vertex)`:

| ring | gate distance | overlaps the footprint? |
|---|---|---|
| Overture "Embarcadero Center 4" | **3.15 m** (centroid) | yes — 13 of its 24 vertices are inside |
| DataSF 201006.0000633 (3,142 m²) | **12.61 m** (centroid) | yes — it *encloses* the OSM ring |
| DataSF 201006.0161607 (Clay/Drumm, must survive) | 29.86 m | no |

Gate = `min(centroid, nearest vertex)`, the quantity `excluded()` compares
against the radius.

The tower's own footprint reaches 36.8 m from the anchor and the circle
deliberately does not cover it — `buildings.mjs` gates on
`min(centroid, any vertex)`, so a small circle at an anchor inside the polygon is
all it needs.

**Why 20 and not 13.** A second consumer gates on the **centroid alone** and sees
a *different ring*: `planKit()` rejects a toy-tier footprint only if its centroid
falls inside this radius (`landmarkExclusions()` in `kitzones.js`), and
`toy.mjs` re-derives its own simplified geometry — on this cell the same building
becomes a **9-vertex ring whose centroid sits at 18.76 m**, not 12.61 m. The bake
makes that moot in practice, because `excluded()` drops the footprint before
`out/footprints.json` is written and that file is `toy.mjs`'s only input, so the
ring can never reach the toy tier. But 20 keeps the kit's own guard covering the
site if a bake is ever restored tier by tier, and it costs nothing: **no ring in
either source has a gate value between 12.61 m and 29.86 m**, so 16 and 20 drop
exactly the same two rings. The QA below was run at 16; the change to 20 is
provably a no-op on the bake and was not re-baked.

### Proving it from the tile, with the right metric

The usual vertex-penetration test **fails silently on this site**. The DataSF
ring is larger than the OSM footprint and encloses it, so every one of its
vertices is outside the 4EC ring: on `origin/main` the depth test reports
**−0.30 m**, "nothing inside", while a **168.6 m** procedural block stands on the
exact site. `qa/tilecheck.mjs` therefore leads with **overlap area**, sampled on
a 0.25 m grid (shape-agnostic, which the staircase plan needs):

| | footprints in 23_10 | largest overlap | deepest vertex penetration |
|---|---|---|---|
| `origin/main` | 49 | **2,169.8 m² = 100.0%** | −0.30 m |
| re-baked | 48 | **0.0 m²** | −0.57 m |

`node pipeline/verify-rebake.mjs`: **584 of 585 cells unchanged**; only 23_10
moved, 49 → 48; nearest surviving footprint 29.9 m against the radius.
Cloning a warm `pipeline/data` with `cp -Rc` is what kept the buildings churn to
**exactly one tile**.

The toy tier was checked separately, because `audit.mjs` 1.6 and
`verify-rebake.mjs` both read only `tiles/buildings/`: on `origin/main` the toy
copy of this building is a 9-vertex ring at 18.76 m centroid / 31.53 m nearest
vertex, and it is gone after the bake for the structural reason above.

`node pipeline/audit.mjs` check **1.6 PASS** — 114 zones over 110 landmarks
clear. Three unrelated checks fail on this branch (1.2b citywide height p95,
1.3c Telegraph Hill terrain from the DEM, 1.7b one sampled tree offshore); all
three read terrain/landcover tiers that this bake regenerated **byte-identically**
(`git status` shows zero changed files under `tiles/terrain`, `tiles/streets`
and `tiles/landcover`), so they are pre-existing, not introduced here.

### Local QA (headless Chrome over CDP against the Vite dev server)

| Check | Result |
|---|---|
| manifest served, entry present | PASS — 104 entries |
| merge line | `4-embarcadero-center merged 10 objects / 9 materials -> batched (10646 tris body); uniform x1.0000 at 3634, -2797` |
| scale factor | **x1.0000** |
| placed / failed | placed true, failed 0, 86 live |
| single building at the site | PASS — A/B against the drill, plus 0.0 m² tile overlap |
| orientation | PASS — long axis along Clay/Sacramento, entrance north |
| terrain seating | PASS — no float, no sink |
| night glow | PASS — only the lit-window scatter, crown ring, lobby band and beacon |
| draw calls (worst observed) | **128** against the 300 budget |
| rAF health | 200 frames in 3 s |
| lint / test / build | PASS — eslint clean, 26/26 tests, `npm run build` OK |

The screenshots are in `qa/`. `qa/ab_present_vs_absent.png` is the one that
settles it: at 42° (the diorama's locked pitch) from 620 m the tower is easy to
mistake for a neighbour, so the honest proof is the pixel A/B — the tower is
present on the left and the site is bare on the right.

### Fallback drill (mandatory)

GLB renamed aside → `placed: false`, `failed: 1`, the app still boots, the city
still renders, and the site is **empty ground inside the exclusion zone**. That
is the expected Case B outcome (there is no procedural stand-in for a landmark
that never had one), and it is why the exclusion radius is kept as small as the
measurement allows. GLB restored automatically.

### One honest observation

At night 4EC reads **cooler** than its procedural neighbours: `Toy_glassl_Glow`
`#6f95b8` against the baked warm-yellow window grid. That matches the real
building's fluorescent-white glazing and it is the repo's own palette entry, but
it does make the tower stand out as a different light temperature in a wide
night shot. Recorded rather than "fixed" by inventing an off-palette colour.

### Batch handoff

`BATCH: yes`, so the bake was run in full for this QA and then discarded
(`git checkout -- app/public/tiles api/_data`). Sanity check passes:
`git diff --name-only origin/main -- app/public/tiles api/_data` is **empty**.
The three things that try to leak in were each dealt with: the cloned
`pipeline/data` was deleted, `compress-assets.mjs`'s re-compression of
`vehicles/passenger-airplane.glb` was reverted, and the 589 generated files were
checked out. The city gets rebuilt once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

For that bake: the ctx churn this landmark causes is a pure global-index
renumber (24 of 25 sampled sidecars are byte-identical once `pick.id` and the
`b` keys are shifted by one), plus one genuine side effect — a North Beach
gallery at 1534 Grant Ave moves from notable tier A to tier B, because dropping
one footprint shifts the notables ranking.

## Stage 3 — approval

Approved 19 August 2026 by David, standing instruction given with the pipeline
invocation, quoted verbatim:

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

The contact sheet, the day and night aerials and the numbers above were
presented in the session before the pipeline advanced. This is a blanket
approval covering stages 3 and 5's ship decision, not a per-render sign-off —
recorded as such so a later reader knows no image-by-image review happened.
