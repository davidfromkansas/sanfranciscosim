# 400 Brannan Street — build report

Asset: `artifacts/400-brannan/400-brannan.glb` — the miniature corner block at Third and
Brannan for the SF toy-diorama city. Built 13 August 2026 from
`docs/asset-plans/400-brannan.md` Part 1, with the corrections recorded below.

## Shipped numbers

| | |
|---|---|
| Triangles | **3,896** (cap 8,000) |
| File on disk | **115,408 B** meshopt-packed (pre-optimize 257,152 B, −55.1%) |
| Draw submeshes | **11** (pre-optimize 88) |
| Objects | 87 |
| Dimensions (m) | 31.40 x 33.78 x **8.80** (axis-aligned; the building is 23.9 x 23.1 m at a 45° heading) |
| min Z | 0.000 |
| XY centre offset | 0.072, −0.001 m |
| Materials | `Toy_sand`, `Toy_stone`, `Toy_ink`, `Toy_glass`, `Toy_trim`, `Toy_roofd`, `Toy_steel`, `Toy_glass_Glow`, `Toy_trim_Glow` — all on-palette, no textures, no alpha |
| Glow groups | 2 (`Toy_glass_Glow` lit upper sash, `Toy_trim_Glow` shopfront band) |
| Anchor | lon −122.3946805, lat 37.7800981 |
| Headings | Third Street front NE **45.2°**; Brannan front SE **135.2°** |
| Target height | 8.8 m — crest normalized exactly, loader scale lands at 1.0 |
| Validation | `validation.json` → **PASS**, every check true |

## Dossier corrections made during the build

1. **"400 Brannan" is not a parcel.** The SF parcel layer has no lot with that number —
   Brannan's even numbers run 376–380 (block 3775) then jump to 414 (block 3776). The
   address exists only in the EAS address layer, on **block 3776 lot 114**, whose
   assessor address is **590 Third Street** and which also carries 406 and 410 Brannan.
   Nominatim returns a POI node ("Buhler Commercial Construction"), not a building. The
   resolution used is address → EAS → parcel → DataSF LiDAR footprint `SF3776114`.
2. **The LiDAR maximum (11.65 m) was rejected as the crest.** It sits +6σ above a roof
   whose height σ is 0.64 m, and the footprint's LiDAR minimum (2.40 m) is plainly
   vegetation; nadir imagery shows a street tree breaking over the Brannan parapet. The
   deck is the measured 7.77 m median, the parapet an inferred 8.6 m, and the model's
   8.8 m crest is a modest roof bulkhead. This is a deliberate rejection of a published
   number, not an oversight — if newer LiDAR shows a real penthouse, re-normalize.
3. **The footprint was simplified from 13 vertices to 5** (491.7 m2 against the survey's
   489.4, +0.5%). The discarded vertices are sub-1.5 m jogs in the northwest party wall.
   The reflex notch at the west corner is kept: it is where 574 Third wraps around this
   building and it is visible in the roof outline from the app's camera.

## Design decisions

- **Paint scheme.** 2016 street-level photography shows cream stucco with chocolate
  bands; 2019 photography of the same tenant frontage (the Avant Barre awnings are in
  both) reads light-gray over charcoal — the building was repainted between the two. The
  model ships the common denominator: a warm light body (`Toy_sand`) over a near-black
  base (`Toy_ink`), which is right in both epochs and reads at city scale either way.
- **The awning line is the one spent exaggeration.** Thickened to 0.60 m deep and 0.45 m
  tall and carried unbroken around both frontages and the corner. At the app's camera
  distance a corner building is recognised by the continuous dark shelf at shopfront
  height, not by its windows.
- **Landscape sash.** The upper windows are 2.75 x 1.60 m. The first build used
  2.4 x 1.9 m and they read square, which put the building in the residential family it
  does not belong to. Widened after the first aerial review render.
- **Roof.** Nadir imagery shows the street-facing third of the deck empty and the plant
  grouped toward the block interior, so that is where it goes: a low `Toy_roofd` plinth
  carrying three `Toy_steel` units and a duct, a hatch, one skylight, and the bulkhead
  that sets the crest. The plinth was added after the first render, where the loose
  boxes read as crumbs rather than as a plant group.
- **Night state.** Hero glow is the shopfront band under the awnings — three of five
  bays on Third, two of four on Brannan, chosen so the corner itself is lit. Supporting
  accent: five lit upper windows. The first night render lit every shopfront and blew
  out; restraint is the style bible's rule and it reads better. Glow shells are thin
  panels proud of the opaque glazing, never the primary surface.

## Approval (gate 3)

Approved in advance by the owner, verbatim:

> "I approve everything -- go ahead and do your thing. you dont need to ask for stage 3
> approval. proceed w everything"

— David, 13 August 2026, in the session that commissioned this asset.

## Draft manifest entry

```json
{
  "id": "400-brannan",
  "file": "400-brannan.glb",
  "anchor": [
    -122.3946805,
    37.7800981
  ],
  "targetHeightM": 8.8,
  "cat": 3,
  "name": "400 Brannan Street",
  "estimated": false,
  "dims": [
    31.4004,
    33.7824,
    8.8
  ],
  "tris": 3896,
  "loadRadius": 2500
}
```

## Files

- `build_400_brannan.py` — deterministic build (Blender 5.2 LTS, headless)
- `render_400_brannan.py` — the six review renders + `--night`
- `validate_400_brannan.py` — fresh-scene contract validation → `validation.json`
- `make_contact_sheet.py` — the contact sheet
- `400-brannan.blend`, `400-brannan.glb`
- `400-brannan-{top,north,east,south,west,aerial,aerial-night,contact-sheet}.png`
- `REFERENCE.md` — sources and observations

## Stage 4 — optimize

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; all gates G1–G6, G8 PASS.
See `optimize/REPORT.md`. The shipping GLB in this directory is the packed file; the
pre-optimize original is archived at `optimize/input/`.

## Stage 5 — integration (batch mode, source-only branch)

Case **B** (new landmark). Manifest entry added, GLB copied to
`app/public/sf-assets/landmarks/`, registry entry added to `pipeline/lib/landmarks.mjs`,
full tile re-bake run for QA and then **discarded** per `ADDRESS-TO-ASSET.md` batch mode —
`git diff --name-only origin/main` lists nothing under `app/public/tiles/` or `api/_data/`.

| Check | Result |
|---|---|
| Re-validation of the shipped (packed) GLB | **PASS** — every contract check true |
| Manifest entry / id round-trip (`camelId`) | **PASS** — `400-brannan` -> `400Brannan`, found in the registry |
| Loader scale (`targetHeightM` / measured Z) | **PASS** — exactly 1.0000 |
| `loadRadius` decision | **2500 m**, the default `max(2500, h x 30)`; the site is empty ground beyond it (the procedural block is excluded), which is illegible at 2.5 km for a building this size |
| Case B registry + re-bake | **PASS** — bake ran clean end to end (terrain -> context) |
| `pipeline/audit.mjs` check 1.6 | **PASS** — 60 zones over 59 landmarks clear |
| `pipeline/verify-rebake.mjs` | **PASS** — only cell 23_13 moved (219 -> 217 footprints); nearest surviving footprint 15.7 m against the 11 m radius |
| Exclusion radius sizing | **11 m, measured by AREA COVERAGE against the real bake input: two footprints stand on this plan (DataSF SF3776114 at 98.5%, Overture 80ad8a83 at 87.7%) and the safe band that drops both with zero collateral is 10-12 m** |
| `compress-assets.mjs` intake | **PASS** — reports "skip (already compressed)", i.e. the stage-4 packing already satisfies the ship step |
| `npm run lint` / `npm run build` (app) | **PASS** — eslint clean, build 1.5 s |
| Local browser QA (screenshots, console merge line, draw calls, night sweep) | **NOT RUN** — the preview pane refused to start a dev server: "Maximum 5 dev servers per folder reached; 5 belong to other chats". Owner elected to ship without it. |
| Fallback drill | **NOT RUN** — same blocker; it needs the running app |
| `landmark-streaming-check.mjs` | **NOT RUN** — needs a served build |

The three audit checks that FAIL (1.2b p95 height, 1.3c Telegraph Hill DEM, 1.7b one
offshore tree) are pre-existing citywide/data-vintage failures and are untouched by this
work.

### Batch handoff

The gate-5 deliverable is this source-only branch, `pipeline/400-brannan`, carrying
**both** `400-brannan` and `574-third`. The city is baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`. Not pushed — the owner asked to hold.

**Open conflict for the batch to resolve:** two other in-flight sessions
(`~/sf-worktrees/590-third`, `~/sf-worktrees/592-third`) have modelled the **same
building** as `400-brannan`. SF's EAS address layer puts `400`, `406`, `410 BRANNAN ST`
and `588`-`592 THIRD ST` on one parcel, 3776114, and all three anchors fall within 2 m of
each other (`590-third` 9.5 m estimated, `592-third` 8.2 m estimated, this asset 8.8 m
measured). Merging all three would stack three GLBs on one footprint. One has to win.
