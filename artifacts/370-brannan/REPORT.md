# 370 Brannan Street — build report

Asset: `artifacts/370-brannan/370-brannan.glb`
Built 12–13 August 2026 with `build_370_brannan.py` (Blender 5.2.0 LTS, headless).
Where this report disagrees with `docs/asset-plans/370-brannan.md`, **this report
wins** — the plan is a head start, not a citation.

## Shipped numbers

| | Pre-optimize | **Shipped (post stage 4)** |
|---|---|---|
| Triangles | 1,428 | **1,428** |
| Vertices | 2,880 | 2,475 |
| Objects / draw submeshes | 28 / 29 | **11 / 12** |
| File size, raw | 93,428 B | **46,796 B** |
| File size, gzip -9 | 19,933 B | 31,246 B (see §4) |
| Materials | 10 | 10 (identical set) |
| Dimensions (m) | 21.8727 × 21.7057 × 7.63 | unchanged |
| min Z | 0.0 | 0.0 |
| XY centre offset (m) | 0.0402, −0.0454 | unchanged |
| Triangle cap | 7,000 | 20% of cap |

Contract validation re-run against the **shipped** (post-optimize) file:
**PASS**, all 16 checks
(`validation.json`, `validate_370_brannan.py`, fresh-scene re-import of the
exported GLB). 31,500 deterministic visibility rays, **0 flipped**; per-object
signed volume positive on every closed solid. The pre-optimize build validated
the same way (28 solids, 0 flipped) — see `optimize/REPORT.md` for the A/B.

## Placement

| | |
|---|---|
| WGS84 anchor | `-122.3938572, 37.7807602` |
| Target height | **7.63 m** (parapet crest = DataSF LiDAR `hgt_maxcm`) |
| Front heading | 134.9° true (SE), onto Brannan Street |
| Authored orientation | true-world (`+Y` = north), no rotation applied by the loader |

The tallest geometry in the export is the parapet ring and it lands at exactly
7.63 m, so the loader's `targetHeightM / measuredHeight` scale is 1.0000.

## Dossier corrections made during the build

Three, all recorded in `REFERENCE.md` and all against the OSM data the plan
started from:

1. **The OSM footprint was rejected.** Way/124890321 traces 5.83 × 24.24 m; the
   DataSF LiDAR footprint (`SF3775020`) says 7.00 × 23.83 m and the assessor's
   1,760 sq ft lot agrees with DataSF to 2%. The OSM way is `source=Bing` — a
   rooftop trace on a building whose neighbours are a metre taller on both
   sides, exactly where such a trace loses the eaves. **A 1.2 m error on a 7 m
   frontage is 17%**, which on this asset is the difference between the
   proportion reading and not.
2. **OSM `height=7` is the roof deck, not the crest.** It matches the LiDAR
   median (7.07 m) to within 1%. The crest is 7.63 m. Same trap as 380
   Brannan's `height=11`.
3. **The roof carries no plant.** The plan allowed for the possibility; the
   satellite imagery settles it — two square skylights, one small roof light,
   one hatch, and nothing else. No HVAC, no penthouse, no masts were modelled.

## Design decisions taken during the build

**Two deliberate palette extensions.** Both are off-palette, which the contract
makes a WARN not a FAIL, and both were forced by the first render pass:

- `Toy_greige` `#b0aa9e` for the body and parapet. In the palette's `Toy_stone`
  the whole building rendered as a cream slab with the `Toy_trim` frame
  invisible against it — which loses the one composition this building has. The
  real wall is a mid warm gray, so the extension is also the more accurate
  choice. Same precedent as 380 Brannan's `Toy_slate`.
- `Toy_cobalt` `#2f5fb0` for the door (glow `Toy_cobalt_Glow` `#6db3d9`).
  Palette `Toy_navy` `#2c4a70` is within two points of `Toy_glass` `#2a4d73`,
  so the door disappeared into the storefront beside it. The door is this
  building's only saturated colour and its strongest cue at thumbnail size.

**The painted "370" numerals are not modelled.** The contract forbids textures
and glyph geometry on a 7 m frontage is sub-pixel noise at every camera the app
uses. The mid-band that carries them is modelled and is the cue that survives.
A decision, not an oversight.

**The flanks are blank.** Both long sides are party walls against neighbours
~1 m taller. The app's aerial camera draws them, so they exist, but they carry
no openings because the real walls carry none.

**The roof deck is `Toy_roofd` charcoal, not the real pale membrane.** This
follows the repo convention (380 Brannan's real "light-gray membrane" roof is
`Toy_roofd` too) and the style bible's requirement that the deck read clearly
darker than the parapet so the ring is legible from above. Noted as a knowing
deviation from the photography.

**Night state.** The upper steel-sash band lights as ONE continuous panel, not
a scatter of individually lit windows: on a 7 m frontage a scatter is
indistinguishable mush, and one lit loft floor over a dark shopfront is what
the street actually looks like. Supporting accent is a narrow spill at the
door. The storefront does not glow.

## Iterations

1. **First build**, `Toy_stone` body / `Toy_navy` door. Elevation renders showed
   a cream slab with an invisible frame and a door that read as a dark slot.
   → the two palette extensions above.
2. **Aerial camera rig.** The 380 Brannan rig (105 mm at `span × 3.1`) crops
   this asset: `span` is the *plan* diagonal here (21.9 m) against a 7.6 m
   height, so the same numbers run off the top and bottom of frame. Widened to
   72 mm at `span × 3.6` and recorded in `render_370_brannan.py`.
3. **Night render was wrong and was re-rendered.** The inherited `light_glow()`
   only raised `Emission Strength`, so the re-imported `_Glow` materials carried
   Blender's default **white** emission (glTF writes `emissiveFactor = 0`
   whenever authored strength is 0) and every glow surface rendered as a white
   slab. Fixed to copy Base Color into Emission Color at strength 1.0, per
   `docs/asset-plans/README.md` and `tools/glb-optimize/render_ab.py`.
   **`artifacts/380-brannan/render_380_brannan.py` still has this bug** and its
   committed night render is affected — out of scope here, but worth fixing.

## Approval (gate 3)

The human approval gate was **explicitly waived by the owner**, 12 August 2026,
verbatim:

> "Yes confirm -- proceed fully. no need to ask for approval"

No approval iteration was run. The renders below are the record.

## Renders

`370-brannan-{north,east,south,west}.png` (orthographic, one rig, identical
scale/framing/lighting/exposure), `-top.png`, `-aerial.png` (72 mm, 38° down,
from the SE), `-aerial-night.png`, and `-contact-sheet.png`.

Note on reading the elevations: the building sits at ~45° to the world axes, so
each world-direction orthographic camera shows two faces at once. They are
labelled by world direction as the spec requires; judge the facades from the
aerial.

## Manifest entry

```json
{
  "id": "370-brannan",
  "file": "370-brannan.glb",
  "anchor": [
    -122.3938572,
    37.7807602
  ],
  "targetHeightM": 7.63,
  "cat": 3,
  "name": "370 Brannan Street",
  "estimated": false,
  "dims": [
    21.8727,
    21.7057,
    7.63
  ],
  "tris": 1428,
  "loadRadius": 2500
}
```

`loadRadius` decision: the default formula `max(2500, 7.63 × 30)` gives 2500 m.
Taken as-is. Beyond that radius the carved-out site is a gap rather than a
stand-in, but at 2.5 km a 7 m building is far below a pixel, so the absence is
illegible.

`estimated: false` — the height is a measured LiDAR figure, not an inference.

## Integration (Case B)

Registry entry added to `pipeline/lib/landmarks.mjs` as `370Brannan`
(`camelId('370-brannan')` round-trips correctly), `exclude: 3`. The reasoning
for that radius — the tightest in the registry — is in the comment above the
entry: 372–374 next door is itself a 7 m sliver whose footprint centroid is
only 6.57 m from this anchor, so the entire safe window is (0.6, 6.5) m.

## Local QA (gate 5, batch mode)

Run 13 August 2026 against a production build (`npm run build`) served
statically, because the Vite 8 dev server in this environment returns the SPA
fallback for `.glb` requests — it does that for every landmark GLB including
ones already on `main`, so it is an environment quirk, not a regression.

| Check | Result | Evidence |
|---|---|---|
| Re-validation of the shipped GLB | **PASS** | `validation.json` overall PASS, 16/16 checks, against the post-optimize file |
| Manifest entry | **PASS** | 36 entries parsed, `entries: 36` in `SF.assets.stats()` |
| id mapping (`camelId`) | **PASS** | `370-brannan` → `370Brannan`, matches the registry entry |
| Registry entry + re-bake | **PASS** | see below |
| Audit check 1.6 | **PASS** | `node pipeline/audit.mjs` — "no procedural footprint inside a bespoke landmark exclusion zone, 42 landmarks clear" |
| `verify-rebake` | **PASS** | "only the new landmarks' cells moved, and every asset has clear ground under it"; nearest surviving footprint 12.4 m vs the 3 m radius |
| Exactly one footprint dropped | **PASS** | cell 23_13 233 → 232; all other 584 cells unchanged in building count |
| Merge line + scale | **PASS** | `sf-assets: 370-brannan merged 12 objects / 10 materials -> batched (809 tris body); uniform x1.0000 at 3840, -1189` |
| Anchor placement | **PASS** | placed at local (3840, −1189), which is the projected anchor to the metre |
| Draw calls for landmarks | **PASS** | `SF.assets.group` children are `landmark-bodies` + `landmark-glow` — 2 draw calls for all 36 generic landmarks |
| Neighbour unaffected | **PASS** | `380-brannan merged … uniform x1.0000 at 3826, -1175` in the same session |
| Fallback drill | **PASS** | with the GLB renamed: network log shows `GET …/370-brannan.glb → 404` while `380-brannan.glb → 200`; exactly one warning, `sf-assets: 370-brannan failed to load (… responded with 404 …)`; the app booted, streamed all 1,656 cells and rendered the block with no hole and no crash. File restored afterwards. |
| Lint / build | **PASS** | `npm run build` clean (`✓ built in 5.00s`) |
| **In-situ beauty screenshot, terrain seating, night glow in scene, stats-overlay draw calls / fps** | **NOT VERIFIED** | see below |

**What could not be verified, honestly.** The app's tile LOD cross-fade
(hashed-alpha discard with distance hysteresis) never completed in this QA
session: the far shells kept drawing over the near tier indefinitely, so every
close-range screenshot shows both tiers superimposed. It affects the whole
city, not this asset — the same double-draw appears in blocks nowhere near
Brannan Street, and it appeared in the run where this GLB was 404 and absent
from the batch. The likely cause is the QA method (teleporting the camera with
`SF.goTo` plus direct `rig.state` mutation on a machine running ~10 competing
Blender jobs) rather than anything in the change, but that is a hypothesis, not
a measurement. Consequently there is **no clean in-situ day/night screenshot,
no terrain-seating check and no stats-overlay draw-call or fps reading** in this
report. Those should be picked up in the batch integration run
(`docs/asset-pipeline/BATCH-INTEGRATE.md`) on a quiet machine before the PR.

The functional evidence above — merge line, scale 1.0000, correct anchor, two
draw calls, one footprint dropped, clear ground, fallback drill — is
independent of that rendering issue and stands.

**Batch mode.** Per `ADDRESS-TO-ASSET.md` the bake was run and used for the QA
above, then discarded (`git checkout -- app/public/tiles api/_data`). The branch
carries source only: the GLB, its manifest entry, its
`pipeline/lib/landmarks.mjs` entry, the plan and `artifacts/370-brannan/`.
`git diff --name-only origin/main` lists nothing under `app/public/tiles/` or
`api/_data/`.
