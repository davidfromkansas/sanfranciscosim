# 574 Third Street — build report

Asset: `artifacts/574-third/574-third.glb` — the miniature 1907 apartment block at
566–586 Third Street ("Central Apartments") for the SF toy-diorama city. Built
13 August 2026 from `docs/asset-plans/574-third.md` Part 1, with the corrections below.

## Shipped numbers

| | |
|---|---|
| Triangles | **9,856** (cap 12,000) |
| File on disk | **284,644 B** meshopt-packed (pre-optimize 608,272 B, −53.2%) |
| Draw submeshes | **12** (pre-optimize 196) |
| Objects | 195 |
| Dimensions (m) | 64.95 x 60.15 x **15.40** (axis-aligned; the building is 34 x 45 m at a 45° heading) |
| min Z | 0.000 |
| XY centre offset | −0.764, 0.023 m (within the ±1 m contract tolerance; the offset is the painted skin and the canted billboard, both of which project on one side only) |
| Materials | `Toy_cocoa`*, `Toy_stone`, `Toy_ink`, `Toy_glass`, `Toy_glassl`, `Toy_trim`, `Toy_roofd`, `Toy_steel`, `Toy_glass_Glow`, `Toy_trim_Glow` |
| Glow groups | 2 (`Toy_glass_Glow` lit flats, `Toy_trim_Glow` shopfronts + billboard uplight) |
| Anchor | lon −122.3950551, lat 37.7801937 |
| Headings | Third Street front NE **44.8°**; Ritch Street rear SW **224.9°** |
| Target height | 15.4 m — crest normalized exactly, loader scale lands at 1.0 |
| Validation | `validation.json` → **PASS**, every check true |

\* `Toy_cocoa` (`#6b4a3d`) is a deliberate palette extension, see Design decisions.

## Dossier corrections made during the build

1. **The footprint is one building, not two, and OSM does not have it.** No OSM way
   carries any of the eleven addresses (566–586 Third); the two Bing comb traces that
   cover the site (ways 124903634 and 124903638) sum to 1,843 m2 against the survey's
   1,906 and correspond to no real division. Nominatim resolves the address onto the
   Third Street **roadway** by TIGER interpolation. Resolution used: address → DataSF EAS
   → parcel 3776008 → DataSF LiDAR footprint `SF3776008`.
2. **The footprint simplification was redone.** The plan's 2.3 proposed a five-vertex
   pentagon; it hits the right area (+0.26%) but by cancelling errors — it swings the
   northwest wall ~10° off the SoMa grid and deletes the building's ~8.6 m step back
   from the party line near Third Street, which is a real court, not a survey wobble.
   The shipped footprint is a **seven-vertex** simplification (1,909.7 m2 against
   1,906.1, +0.19%) in which **every edge keeps its true grid bearing** (44.8 / 132.9 /
   224.9 / 314.9°) and the court survives. The plan's polygon is superseded.
3. **The two light wells are modelled as recessed roof slots**, not as plan notches, as
   the plan anticipated: between two party-wall neighbours nobody can see the wall faces
   a re-entrant plan would create, and from the app's camera the two read identically.

## Design decisions

- **`Toy_cocoa` palette extension.** The Third Street elevation is painted a dark
  chocolate brown. `Toy_rust` (`#a86444`) is the nearest palette entry and it turns the
  building back into an orange brick box, erasing the painted/bare distinction that is
  the elevation's whole point. Off-palette is a WARN, not a FAIL
  (`sf-asset-check` §7), and the render justified it. Precedent: `Toy_slate` on
  380 Brannan.
- **The paint stops 4.5 m short of the northwest end**, exposing bare `Toy_stone` brick
  under the billboard, exactly as the 2019 photograph shows.
- **The billboard is canted ~22° off the street line** rather than set parallel to it.
  Parallel, it is a hairline from the app's usual approach down Third Street and reads as
  a modelling error; canted — which is how a hoarding is actually turned toward oncoming
  traffic — it reads as a panel from both the aerial and the street. It ships **blank**:
  a `Toy_ink` face in a `Toy_trim` frame on two `Toy_steel` legs. No advertising artwork
  is reproduced.
- **Window rhythm.** 9 bays on Third and 8 on Ritch, two upper floors each, tall and
  narrow (1.35 x 2.10 m) with pale frames. The real count is ~11; the rhythm, not the
  count, is what makes the building recognizable at city scale.
- **Roof.** After the first render the light wells read as *light slabs* — the stone kerb
  was capping them. Fixed by making the kerb a thin lip around an ink box whose top sits
  60 mm proud of the deck, which reads as a dark slot from above. The furniture was also
  re-spread: the first pass grouped everything in the Third Street third of a 45 m deep
  roof and left two thirds empty.
- **Night state.** 104 flats, so a scattered third of the windows are lit across both
  long elevations — irregular, not a checkerboard. Supporting accents: three of five
  shopfronts, both entrance recesses, and a thin uplit strip along the bottom edge of the
  billboard. The billboard face itself is **not** a glow surface.

## Approval (gate 3)

Approved in advance by the owner, verbatim:

> "I approve everything -- go ahead and do your thing. you dont need to ask for stage 3
> approval. proceed w everything"

— David, 13 August 2026, in the session that commissioned this asset.

## Draft manifest entry

```json
{
  "id": "574-third",
  "file": "574-third.glb",
  "anchor": [
    -122.3950551,
    37.7801937
  ],
  "targetHeightM": 15.4,
  "cat": 2,
  "name": "574 Third Street",
  "estimated": false,
  "dims": [
    64.9494,
    60.1454,
    15.4
  ],
  "tris": 9856,
  "loadRadius": 2500
}
```

## Files

- `build_574_third.py` — deterministic build (Blender 5.2 LTS, headless)
- `render_574_third.py` — the six review renders + `--night`
- `validate_574_third.py` — fresh-scene contract validation → `validation.json`
- `make_contact_sheet.py` — the contact sheet
- `574-third.blend`, `574-third.glb`
- `574-third-{top,north,east,south,west,aerial,aerial-night,contact-sheet}.png`
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
| Manifest entry / id round-trip (`camelId`) | **PASS** — `574-third` -> `574Third`, found in the registry |
| Loader scale (`targetHeightM` / measured Z) | **PASS** — exactly 1.0000 |
| `loadRadius` decision | **2500 m**, the default `max(2500, h x 30)`; the site is empty ground beyond it (the procedural block is excluded), which is illegible at 2.5 km for a building this size |
| Case B registry + re-bake | **PASS** — bake ran clean end to end (terrain -> context) |
| `pipeline/audit.mjs` check 1.6 | **PASS** — 60 zones over 59 landmarks clear |
| `pipeline/verify-rebake.mjs` | **PASS** — only cell 23_13 moved; nearest surviving footprint 16.4 m against the 12 m radius |
| Exclusion radius sizing | **12 m: three footprints cover this plan (DataSF SF3776008 at 97.9% plus two Overture halves at 50.8% and 40.3%); the safe band is 8-16 m and 18 m would eat 560 Third** |
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
