# 76–82 South Park — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run 16–17 August 2026 in
`sf-worktrees/76-south-park` on branch `pipeline/76-south-park`.

**Shipped (post stage-4 optimize):** `76-south-park.glb` — 4,376 triangles,
**11 objects / 12 draw submeshes**, **116,636 B raw / 67,228 B gzipped**, bbox
26.61 × 26.02 × 16.28 m, min Z 0.000, XY centre offset (0.000, 0.000), ten `Toy_*`
materials, contract validator **all-PASS on the packed file**.

The pre-optimize build was 118 objects / 120 submeshes at 299,404 B raw; it is archived
at `optimize/input/76-south-park.glb`. See `optimize/REPORT.md` for the full pass.

---

## 1. Numbers

| | |
|---|---|
| Triangles | **4,376** (cap 9,000) — unchanged by the optimize pass |
| Objects / draw submeshes | **11 / 12** shipped (118 / 120 pre-optimize) |
| File | **116,636 B raw / 67,228 B gzipped** shipped (299,404 B / 47,983 B pre-optimize; budget ≤ 500 KB compressed) |
| Dimensions | 26.6145 × 26.0241 × 16.28 m |
| Footprint | 6.90 × 29.70 m = 204.9 m² |
| Crest | 16.28 m exactly ⇒ loader scale `targetHeightM / measuredHeight` = 1.000 |
| Roof deck | 13.08 m |
| min Z | 0.000 |
| XY centre offset | (0.000, 0.000) |
| Street elevation heading | 135.00° true |
| Long axis heading | 315.00° true |
| Bay face headings | front 135.00°, SW return 188.62°, NE return 81.38° |
| Manifest anchor | `-122.3940170, 37.7820261` |
| Materials | `Toy_glass`, `Toy_glassl_Glow`, `Toy_ink`, `Toy_roofd`, `Toy_rust`, `Toy_sand`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_trim_Glow` |

**The anchor moved 0.18 m.** The design anchor is the DataSF LiDAR area centroid
`-122.3940150, 37.7820265`; `recentre()` shifted the model by (−0.177 m E, −0.050 m N)
to put the XY bbox centre on the origin, because the canted bay projects 0.95 m on the
street end only and pulls the bbox centre toward the street. The manifest anchor carries
that shift, so the building still lands on its real footprint (AGENTS rule 5).

**Why the XY box is 26.6 × 26.0 m for a 6.90 × 29.70 m building.** The footprint stands
at 45° to the world axes, so the axis-aligned box is the rotation of the sliver, not the
building's dimensions. The two figures differ from each other by 0.59 m rather than being
equal because the bay projects on one end only.

## 2. Validator

`validation.json`, from a **fresh-scene re-import of the exported GLB** (not the
authoring scene). All 16 checks PASS. The two normals tests both passed on the
authoritative reading:

- **Signed volume**: 118 of 118 objects outward, 0 inverted (11 of 11 after the
  optimize pass's join-per-material). This is the authoritative test for a
  union-of-solids asset like this one.
- **Ray cast**: 32 flipped first hits out of 31,500 = **0.1016 %** residual, inside the
  ≤ 0.15 % tolerance. The residual is the expected artefact of coincident faces where the
  proud skins (stone base, flank band, rear face) sit against the body wall.

Two validator constants were carried over from `artifacts/106-south-park/` and had to be
retargeted — `target_height_m` 11.58 → 16.28, the plausible-dimensions window, the
`anchor_lonlat`, and `TRI_BUDGET` 7,000 → 9,000. The first run FAILed on exactly those
two checks, which is the correct behaviour for a copied validator and is why it is worth
copying one.

## 3. The penthouse, and how to remove it

`roof_penthouse` is a **single object**, a 2.6 × 3.2 m box from 13.08 m to 16.28 m, set
back 9.9–13.1 m from the street edge toward the north-east party wall. It is the tallest
geometry in the export and therefore what `targetHeightM` normalizes to.

It is kept on the evidence in REFERENCE.md §3, and the setback it is built at (9.9–13.1 m)
is inside the 8–11 m band the photogrammetry needs for a 16.28 m crest to be consistent
with the photograph. **It remains the weakest claim in this asset.** If better imagery
attributes the tall element to 70 South Park instead:

1. delete `roof_penthouse` from `build_76_south_park.py`;
2. set `Z_CREST = Z_PARAPET` (13.43 m);
3. rebuild, re-render, re-validate, and change `targetHeightM` to 13.43 in the manifest.

Nothing else depends on it. That is the whole reason it was authored as one object rather
than being merged into the roof furniture.

## 4. Design decisions and deviations from the plan

The plan's massing recipe was followed with these changes, all made at review:

1. **The arch was raised.** The springing line went from 3.40 m to 4.30 m (crown 3.40 →
   5.40 m). At the plan's height the arch read as a ground-floor opening and left a 2.4 m
   blank cream panel above it on the south-west half of the base — the largest dead area
   on the facade. Raising it lets the arch do the work the plan asked of it ("the one
   genuinely unusual thing on the building").
2. **The grid-window surround was a bug and is now a frame.** The plan called for a
   `Toy_trim` surround; the first build authored it as a solid prism spanning the whole
   opening at depth 0.00–0.08, which sat *in front of* the glazing. The building's
   second-largest window rendered as a blank cream panel. It is now four thin bars.
3. **The roof decking went from `Toy_brick` to `Toy_rust`.** 49 m² of `#c96f4a` on a
   205 m² roof read as a bright orange panel that took over the entire aerial — the same
   failure 104–106's report records for its flank strip. `Toy_rust` `#a86444` is weathered
   redwood, which is both calmer and closer to what an SF roof deck actually looks like.
   The warm accent is kept; its saturation is not.
4. **The juliet balcony moved from the corbel line to the band window.** The plan put it
   at 6.90 m spanning the bay's full width, where the bay's corbel — which projects
   0.95 m over exactly that range — swallowed it completely; it appeared in no render.
   The Hawthorne photograph puts the railing at roughly 37 % of the facade height, which
   is the band-window sill (4.90 m). Moved there, and it now reads.
5. **The rail glow became ten festoon dashes.** A single 8.2 m `Toy_trim_Glow` bar read
   as a neon tube and outshone the three lit windows, which are supposed to be the hero.
   Dashes read as string lights, which is what a roof deck "open nights and weekends"
   has.
6. **The entry glow became a lintel band, not a rectangular ring.** At the app's ~12 %
   day alpha a ring reads as a pale panel floating in the doorway.
7. **The service bay ended up inside the arch recess** rather than being a separate read
   on the elevation, because the raised arch now covers the same ground-floor zone. That
   is the honest outcome: the south-west ground floor reads as one deep dark arched
   opening, which is what the photographs show, and it sidesteps committing to a garage
   door position that is not established (REFERENCE.md §5).

**A bevel-filter bug worth recording.** The bevel skip-list used
`n.endswith(("_fill", "_glow"))`, which missed `roof_lamp_glow_<i>` and spent ~1,000
triangles bevelling ten 0.3 m boxes. It is now substring tests. Same class of mistake as
the surround slab: both came from adapting the reference script's *shape* without
re-checking that its *predicates* still match the new object names.

## 5. Corrections to the dossier

Three, all made before building and folded back into
`docs/asset-plans/76-south-park.md` (commit `fe6da2dd`): the crest photogrammetry was
replaced with a calibrated setback table, the garage was downgraded to an open question
with a neutral service bay, and the first-floor juliet railing was added. See
REFERENCE.md §7.

**One identification error was made and caught.** An early reading of a narrow-field
Street View frame mistook a grey building further down the row for the subject. The fix —
and the check to repeat if anyone doubts the identification — is the January 2025 frame
that has both neighbours' street numbers in shot (REFERENCE.md §1).

## 6. Integration decisions taken at stage 5

- **`exclude: 2.9`**, re-measured on the **simplified** rings the gate actually sees
  (`addBuilding()` runs `simplifyRing(ring, 0.6)` before `excluded()`). That moved the
  window from the plan's raw-ring (1.92, 3.64) to (1.83, 3.97), and 2.9 sits dead centre
  with 1.07 m either side. The plan's §2.13 was corrected to match.
- **Registry `height: 13.08`**, not the manifest's `targetHeightM: 16.28`. The registry
  number only feeds `context/landmarks.json` and from there the search and concierge
  cards, so it should be the measured roof deck, not the penthouse normalization target.
  Same deliberate split as `64SouthPark` (15.0 against 21.0415).
- **`camera: { distance: 130, yaw: 45, pitch: 26 }`**, settled from
  `app/src/camera.js:119-127` rather than from a neighbour's comment: `position = pivot +
  distance × (sin yaw, sin pitch, cos yaw)` with `+z` south, so yaw 45 stands the camera
  south-east, square onto the 135° front. This resolves a disagreement 104–106's plan
  flagged — `126SouthPark`'s comment is right, `64SouthPark`'s is wrong. Neither was
  edited; the integration prompt forbids touching another landmark.
- **No `clearTrees`.** The street trees in front of this building are real and are in
  every photograph of it.
- **`loadRadius: 2500`** (the default formula's floor). Case B with no procedural
  builder, so past that radius the site is empty ground rather than a stand-in block; at
  2.5 km on a 6.9 m frontage that is illegible.

## 7. What is still open

Carried forward from the plan's 2.15, unchanged by the build:

1. **The penthouse attribution** (§3 above) — highest consequence.
2. **The roof layout.** The deck's position on the street third is argued from the
   listings' claimed views, not observed. No oblique aerial could be obtained: Bing Bird's
   Eye returns blank tiles, Google Maps' 3D tilt parameters did not apply from a URL, and
   Google Earth web would not finish streaming on this machine. If the deck is in fact at
   the rear, the roof reads completely differently.
3. **The rear elevation** is unobserved beyond "there are rear stairs".
4. **The body hue.** Dark and warm is solid; the exact hue is read from a shaded pano and
   a possibly-decade-old sunlit photograph.
5. **The bay's return angle** is 53.6° off the facade plane rather than a classic 45°,
   because the projection was exaggerated to 0.95 m on a 0.70 m lateral return. It reads
   correctly as a canted bay but it is steeper than the real one.
6. **The width** (6.90 m, chosen from three sources spanning 6.71–7.22 m) will propagate
   into the row when 70 and 84 are eventually built.

## 8. Approval — gate 3

The pipeline's stage 3 requires an explicit human approval quoted verbatim. The
invocation for this run carried a standing instruction:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

— David, 16 August 2026, in the message that launched this pipeline run (together with
`BUILDING: 76 S Park St, San Francisco, CA 94107` and `BATCH: yes`).

Gate 3 is therefore taken as passed on that standing instruction rather than on a
per-asset review, and stage 4 proceeded. **This is a weaker gate than the pipeline
intends** — no one has looked at these renders but the agent that made them — and it is
recorded as such. The reviewable evidence is `76-south-park-contact-sheet.png`,
`76-south-park-aerial.png`, `76-south-park-aerial-night.png` and
`76-south-park-facade.png`; if any of it is wrong, stage 2 is a rebuild, not a patch.

---

## 9. Stage 5 — local integration QA (batch mode)

Executed `docs/asset-plans/INTEGRATION-PROMPT.md` Part 1, Case B, with the
`ADDRESS-TO-ASSET.md` batch-mode amendment: the bake was **run** for this QA and then
**discarded**, and only source is committed.

`preview_start` refused with *"Maximum 5 dev servers per folder reached; 5 belong to
other chats"*, so the QA ran through the documented escape hatch — Vite on port 5076
driven by real headless Chrome over CDP, where rAF runs normally. The dev server was
confirmed to be serving **this** worktree before anything was trusted
(`lsof -a -p … -d cwd` → `sf-worktrees/76-south-park/app`; served manifest 74 entries,
last id `76-south-park`; GLB 200 at 116,636 B).

| Check | Result | Evidence |
|---|---|---|
| Re-validation of the shipping GLB | **PASS** | contract validator all-16 on the packed file: 4,376 tris, 11 objects, 26.6145 × 26.0241 × 16.28 m, min Z 0.0, XY centre (0,0), 11/11 signed volumes outward, ray-flip 0.1016 % |
| Manifest entry | **PASS** | appended as **text**, not via `json.dump` — 19 insertions, 0 deletions, no churn on the other 73 entries |
| id mapping | **PASS** | `76-south-park` → `camelId()` → `76SouthPark`, matching the registry entry |
| Case B registry entry | **PASS** | `pipeline/lib/landmarks.mjs`, `exclude: 2.9`, `height: 13.08`, `camera { 130, 45, 26 }` |
| Re-bake | **PASS** | full chain `terrain → bridges → buildings → streets → landcover → validate → lore → toy → notables → context → muni-shapes`; `validate` reported `ok landmark in extent: 76-82 South Park — cell 23_13` |
| `verify-rebake.mjs` | **PASS** | *"only the new landmarks' cells moved"* — 584 of 585 cells unchanged; cell 23_13 **201 → 200**, i.e. exactly one footprint dropped; nearest surviving footprint **4.0 m** vs the 2.9 m radius |
| `audit.mjs` check 1.6 | **PASS** | *"no procedural footprint inside a bespoke landmark exclusion zone — 83 zones over 80 landmarks clear"* |
| Merge line / scale | **PASS** | `sf-assets: 76-south-park merged 12 objects / 10 materials -> batched (2547 tris body); uniform x1.0000 at 3826, -1329` — scale exactly **1.0000**, and 3826/−1329 is the anchor's local position to the metre |
| Exactly one building on the site | **PASS** | settled from the tile, not the screen: `verify-rebake` puts the nearest surviving footprint 4.0 m from the anchor, outside the asset's 3.45 m half-width |
| Footprint size | **PASS** | reads as the narrowest thing in the row in the day frame, flush with both party-wall neighbours |
| Orientation | **PASS** | authored at true-world heading, no `yawDeg` override; the bay and arch face the oval in the day frame |
| Terrain seating | **PASS** | no floating or sinking at the base in the day frame; site falls only 0.84 m across the footprint |
| Night glow | **PASS** | only the intended `_Glow` surfaces light: a small number of lit windows plus the entry lintel and the roof-deck festoon line. Restrained against the procedurally-lit neighbours, which is the intent |
| Draw calls | **PASS** | **87–101** max-per-frame across four passes, against the 300 budget. Measured by hooking `renderer.render` and taking the max, because the stats overlay reads the post-process quad (1 call), not the scene |
| Fallback drill | **PASS** | GLB moved aside → exactly one console warning (`sf-assets: 76-south-park failed to load`), `failed: 1`, app boots, city renders, draw calls still 94, and the site is **empty ground** — expected for Case B with no procedural builder. Restored byte-identical. Note: Vite answers the missing path with `index.html` and HTTP **200**, so this surfaces as a parse failure rather than a 404 |
| `npm run lint` | **PASS** | eslint clean |
| `npm run build` | **PASS** | 57 modules, `dist/assets/index-*.js` 950.78 kB / 269.28 kB gzip; `compress-tiles` 3,315 tiles 56.8 → 31.8 MB |
| Batch sanity check | **PASS** | `git diff --name-only origin/main` lists **nothing** under `app/public/tiles/` or `api/_data/` |

Screenshots in `integration/`: `qa-local-day.png`, `qa-local-night.png`,
`qa-local-fallback.png` and the three `-detail` crops.

**Two honest caveats on the visual QA.** (1) The diorama camera clamps to
`minDistance = 150 m` and locks pitch at 42°, so a 6.9 m frontage is small in frame; the
detail crops are enlargements of the frame centre, not closer renders. (2) Frames must
be caught with `SF.assets.stats().fading === 0` — a mid-cross-fade frame is a stack of
half-alpha shells and reads as broken geometry that is not broken. Two frames were
discarded for that reason before the ones committed here.

**Not done, deliberately:** the bake was discarded (batch mode), so no tiles or
`api/_data` are committed, and the city gets baked once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`. Step 7 (push, PR, deploy, production QA) is
replaced by a stop per `ADDRESS-TO-ASSET.md` stage 5 — nothing has been pushed.
