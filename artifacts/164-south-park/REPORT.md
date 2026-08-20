# 164 South Park — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed against
`docs/asset-plans/164-south-park.md`. **This report beats the plan wherever they
disagree**; `REFERENCE.md` carries the sources and the photogrammetric working.

## Shipped numbers

| | |
|---|---|
| File | `artifacts/164-south-park/164-south-park.glb` |
| Triangles | **3,366** (cap 8,000) — unchanged by stage 4 |
| Mesh objects | **8** (shipped; 56 before the stage-4 join-per-material) |
| Dimensions | **37.2385 × 36.4711 × 5.4000 m** |
| Crest | **5.4000 m** exactly — loader scale `targetHeightM / measuredHeight` = 1.0000 |
| Min Z / XY centre offset | 0.0000 m / (0.0000, 0.0000) |
| Raw / gzipped | **92,552 B** / 64,988 B (shipped, post stage 4; pre-optimize was 206,060 / 46,999) |
| Materials | 8: `Toy_red`, `Toy_brick`, `Toy_ink`, `Toy_glass`, `Toy_steel`, `Toy_trim`, `Toy_glass_Glow`, `Toy_trim_Glow` |
| Glow groups | 2 (`Toy_glass_Glow` on the ribbon + entry band, `Toy_trim_Glow` on the canopy soffit) |
| Manifest anchor | **-122.3949366, 37.7812097** (after recentring on the model's XY bbox) |
| Design anchor | -122.3949238, 37.7812072 (parcel-union area centroid) |
| Street facet headings | 86.0°, 91.1°, 95.8°, 100.6° plus the 135.2° chamfer |
| Long-axis heading | 315.1° / 135.1° |

The 37.2 × 36.5 m XY bounding box is the ~45° world rotation of a 42 × 16 m wedge plus
the canopy's 1.5 m projection. It is **not** a 37 m building and it is not a scale error.

## Validation

`validate_164_south_park.py` factory-resets Blender 5.2.0 LTS, imports only the exported
GLB, and runs every check on the re-import. **`overall: PASS`**, all 16 checks true:

| Check | Result |
|---|---|
| meters and plausible dimensions | PASS |
| crest normalized to target (5.400 m) | PASS |
| base at z = 0 | PASS |
| centred in XY | PASS |
| under triangle budget (3,366 / 8,000) | PASS |
| no image textures / no transparency | PASS |
| materials follow contract (`Toy_*`, no `Toy_body`) | PASS |
| no cameras, lights, animation, skins, constraints | PASS |
| transforms applied, no negative scales | PASS |
| **normals outward — per-object signed volume** | PASS (56/56 positive, 0 inverted) |
| **normals outward — ray test** | PASS (31,500 first hits, **0** flipped, residual 0.000000) |
| no degenerate geometry | PASS (0) |
| no unexpected objects | PASS |

The signed-volume test is the authoritative one for this union of solids; the ray residual
came out at exactly zero, which is better than the 0.15% the contract allows.

## What was built

Two volumes and five attachments, all swept along mitred chains derived from the surveyed
parcel polygon:

1. **Body** — the 9-vertex footprint extruded to the 5.10 m roof deck, `Toy_brick`, with the
   entry recess notched 0.65 m into the street wall **only up to 3.30 m**.
2. **Parapet and coping** — a swept ring, crest 5.400 m, `Toy_brick` with a `Toy_trim` cap.
3. **Screen** — the Saitowitz panel wall standing **0.35 m proud** of the body along all five
   exposed street planes, parapet 4.10 m, `Toy_red`, with joint reveals cut every 0.94 m.
4. **Ribbon** — 13.9 m of continuous glazing, sill 1.55 m, head 2.95 m, mitred at every facet
   corner, with `Toy_ink` sill/head bars and nine mullions at 1.6 m centres.
5. **Entry** — a 3.60 m recess from 1.90 m to 5.50 m south of v6, straddling the v5 corner,
   glazed to 3.30 m, with a transom at 2.35 m and a pair of black doors.
6. **Canopy** — a 0.14 m blade, soffit 2.98 m, projecting 1.50 m, four outriggers, and the
   **164** numerals block-built at 0.35 m tall on its fascia.
7. **Roof** — four skylight monitors (pale curbs, dark glazing) in two staggered rows and two
   mechanical boxes, all under the 5.40 m crest.

## Corrections to the plan, made during the build

Recorded in full in `REFERENCE.md` §6. The material ones:

1. **Screen returns dropped.** The plan asked for 0.40 m returns around v1 and v6. A return
   offset 0.35 m proud of a party line penetrates the neighbour's wall. The screen now caps
   flush at both ends, which is what `003.jpg` shows anyway.
2. **The entry recess is not full height.** The plan said cut the screen 0–4.10 m; the
   photographs show red panel continuing above the canopy to the parapet, so the recess runs
   0–3.30 m with a red lintel band above it. A full-height cut would have opened the recess
   to the sky.
3. **The numerals were mis-sized in the plan** at 0.09 m. `005c.jpg` puts them at ~0.41 m.
   Built at 0.35 m.
4. **Roof furniture heights reduced** — monitors 0.35 → 0.28 m, mechanical boxes 0.60 →
   0.26 m — because nothing may exceed the 5.400 m crest and 5.10 + 0.35 does.
5. **Roof furniture materials changed.** `Toy_steel` curbs on a `Toy_steel` deck are
   invisible from above; the curbs are now `Toy_trim` (which is also what the aerial shows)
   and the mechanical boxes `Toy_ink`.
6. **The body is only notched below 3.30 m.** Notching the full height carried the recess up
   into the parapet and put a notch in the roof outline that does not exist.

## Iterations (the ones worth recording)

1. **The screen was built inside the building.** The street chain runs v6 → v1, which is
   *backwards* along the CCW footprint ring, so its segment normals point inward and the
   first build put the entire red screen, the ribbon, the canopy and the numerals inside the
   brick body, where nothing was visible. The aerial review caught it immediately — the
   facade was a blank brick wall. Fixed by threading an explicit `nsign` through `sweep()`
   and passing −1 for every street-chain sweep; the function's docstring now says so. This
   is the offset-handedness trap the plan's §2.7 warns about, arriving from a direction the
   plan did not anticipate: not a folded corner, but a wholesale inversion.
2. **The numerals read `b9l`.** `t` increases *southward* along the frontage, but a viewer on
   the sidewalk has north on the right, so reading order left-to-right is *decreasing* t.
   The glyph layout is now reversed in `t` and each block mirrored within its cell.
3. **The joint reveals read as clapboard.** Cut at the real 0.47 m course they gave the
   building horizontal siding — the exact opposite of "large scale panels". Halved to 0.94 m
   per the plan's own §2.6, which was right and which the first build ignored.
4. **81 degenerate triangles and 28 non-unit loop normals** on the first validation. Two
   causes: `resample()` emitted duplicate stations whenever a `t` bound landed exactly on a
   facet corner, making zero-length swept segments; and the 0.035 m bevel was wider than half
   the 0.035 m joint reveal, collapsing the groove faces. Fixed by de-duplicating stations at
   0.1 mm and dropping the bevel to 0.020 m, plus a `finalise()` pass per object (weld at
   0.1 mm, dissolve degenerates, recalc face normals outward, force flat shading). The weld
   threshold is deliberately tiny: a generous weld smooths flat shading across the bevels and
   the app renders the result as a soft blob.

## Two things about the renders

**The review rig is EEVEE, not Cycles.** Every other asset in this repo renders its review
images with Cycles at 64 CPU samples. While this asset was being built, four parallel
landmark sessions had this machine's load average above 200 and a single 1200x1000 Cycles
frame was taking more than two minutes; the same frame in EEVEE takes about five seconds.
Nothing gate 2 or gate 3 judges — silhouette, massing, the 1.3 m step, the ribbon's
continuity across the facets, which surfaces glow — depends on path tracing, so the rig was
switched and the change is recorded in `render_164_south_park.py` next to the engine line.
The images still come from a re-import of the exported GLB, on the same cameras, with the
same lights.

**The night render's glow is whiter than the app's will be.** The rig drives `_Glow`
materials to emission strength 6.0, which is the repo convention, and at that strength
`Toy_glass_Glow` blows out to white. The app does not do this: it draws `_Glow` in an unlit
layer, so what a player sees at night is the material's **base colour, `#6f95b8`**, at
`opacity = 0.12 + 0.95·uNight`. Judge the night composition from this render — one continuous
lit band that tracks the oval and drops at the entry, plus a thin canopy spill, and nothing
else — but not its colour.

## Reproducing

```
blender -b --python build_164_south_park.py --          # -> .blend + .glb
blender -b --python render_164_south_park.py --         # 4 elevations, top, aerial
blender -b --python render_164_south_park.py -- --night # night aerial
python3 make_contact_sheet.py
blender -b --python validate_164_south_park.py --       # -> validation.json
```

Blender 5.2.0 LTS (hash `fbe6228777e7`, built 2026-07-14). The build is deterministic — no
randomness, no time or file-system dependence.

## Draft manifest entry

```json
{
  "id": "164-south-park",
  "file": "164-south-park.glb",
  "anchor": [-122.3949366, 37.7812097],
  "targetHeightM": 5.4,
  "cat": 3,
  "name": "164 South Park",
  "estimated": true,
  "dims": [37.2385, 36.4711, 5.4],
  "tris": 3366,
  "loadRadius": 2500
}
```

`"estimated": true` — no published height exists; 5.4 m is the DataSF LiDAR **median**, and
the LiDAR **maximum of 9.25 m is deliberately rejected**. The reasoning is in the plan's
§2.15 and summarised in `REFERENCE.md` §5: the LiDAR distribution is too tight (sd 0.84 m) to
contain a 4 m step, the assessor records one storey on both parcels, the aerial shows an
unbroken flat roof, and both two-storey neighbours visibly overtop this building.

`dims` and `tris` above are the **shipped** figures — stage 4 changed neither. What it changed is the file (206,060 → 92,552 raw bytes, −55.1%) and the draw submesh count (56 → 8). Full metrics, gates and the deliberate skip of the limited-dissolve step are in `optimize/REPORT.md`. The stage-2 contract validator was re-run on the shipped file and still reports `overall: PASS`.

## Stage 3 — approval

Standing approval was given for the whole run ("APPROVE EVERYTHING DONT ASK ME FOR
PERMISSION", 2026-08-18). The contact sheet, the day and night aerials and the numbers above
are presented as the gate-3 evidence rather than as a request.

---

## Stage 5 — integration (Case B, batch mode)

Executed per `docs/asset-plans/INTEGRATION-PROMPT.md` with the batch-mode amendment from
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`. Filled in as each step completed; the QA table is
below.

**Source changes (the only things committed):**

- `app/public/sf-assets/landmarks/164-south-park.glb` — the stage-4 file, copied byte-for-byte.
  `node pipeline/compress-assets.mjs` reports `skip (already compressed)` for it, as expected
  for a post-optimize asset. It also re-compressed `vehicles/passenger-airplane.glb`, which is
  somebody else's file and unrelated to this landmark; reverted.
- `app/public/sf-assets/landmarks_manifest.json` — one appended entry, written as **text**
  so `JSON.stringify` could not renormalise other entries' float formatting. Diff: 19
  insertions, 0 deletions.
- `pipeline/lib/landmarks.mjs` — one appended `LANDMARKS` entry (verified it landed in
  `LANDMARKS`, not in `VIEW_PRESETS`: 97 landmarks, 6 presets after the edit).
- `docs/asset-plans/164-south-park.md` — §2.13 rewritten with the measured exclusion.

**`camelId` round trip:** `164-south-park` → `164SouthPark`, which is the registry id. Checked
against the actual `camelId()` in `app/src/assets.js` rather than by eye, because a digit-led
slug is exactly where that mapping has bitten before.

**The re-bake, and a false reassurance from `verify-rebake.mjs`.**

The full chain ran green (`terrain → bridges → buildings → streets → landcover → validate →
lore → toy → notables → context → muni-shapes`, exit 0). `node pipeline/audit.mjs` check
**1.6 PASSES** — "no procedural footprint inside a bespoke landmark exclusion zone,
100 zones over 97 landmarks clear". `node pipeline/verify-rebake.mjs` also passes, and reports
the nearest surviving footprint at **3.8 m against the 2.6 m radius**.

But it also prints this, and it is wrong:

```
23_13   unchanged  <- 164SouthPark: exclusion dropped nothing (no footprint in the source data?)
```

It is a *count* comparison, and cell 23_13 holds 182 footprints before and after. What
actually happened is that this landmark dropped one footprint and the `pipeline/data` snapshot
this bake ran against — cloned from a sibling worktree — differs slightly in vintage from the
one `origin/main` was baked with, so one other footprint appeared in the same cell. Net zero.
Counts cannot see that; identities can.

Settled from the tiles instead, decoding `app/public/tiles/buildings/23_13.bin` and running
point-in-polygon at the anchor:

| | Rings covering the anchor | Nearest ring |
|---|---|---|
| `origin/main` | **1**, height **8.5 m** | 0 m (it covers the anchor) |
| after this re-bake | **0** | 3.76 m, height 8.7 m — the 158 sliver, deliberately kept |

The 8.5 m procedural block is the point. The asset is 5.4 m. Without the exclusion the
landmark would have been *completely invisible* inside a taller baked box, and no amount of
looking at the GLB would have shown it — which is exactly why `ADDRESS-TO-ASSET.md` insists
the bake runs even in batch mode before the QA.

The three `audit.mjs` failures (1.2b p95 height, 1.3c Telegraph Hill terrain, 1.7b one
sampled tree offshore) are all pre-existing on `origin/main` and unrelated to this landmark.

### Local QA (Step 5)

Run in real headless Chrome over CDP against the Vite dev server for **this worktree**
(manifest served: 91 entries, ours confirmed present before anything else was believed).
Script kept at `artifacts/164-south-park/integration/qa-headless.mjs`. `requestAnimationFrame`
measured at 200 frames in 3 s, so the app's own loop drove the streaming scan and nothing had
to be pumped by hand.

| Item | Result |
|---|---|
| Landmark streams in and merges | **PASS** — `sf-assets: 164-south-park merged 8 objects / 8 materials -> batched (1961 tris body); uniform x1.0000 at 3745, -1239` |
| Loader scale | **1.0000** exactly — the authored crest and `targetHeightM` agree |
| `SF.assets.stats()` | `entries: 91, live: 77, fading: 0, **failed: 0**` |
| Exactly one building on the site | **PASS** — no procedural twin, no z-fighting; settled from the tile as well (see above) |
| Footprint size against neighbours | **PASS** — reads as the 42 m wedge it is, against 160 to the north and 166 to the south-west |
| Orientation | **PASS** — the red screen faces the oval; the entry and canopy sit at the north end of the frontage, as researched |
| Terrain seating | **PASS** — no float, no sink; pivot ground at y = 7.11 m |
| Night glow | **PASS** — the ribbon reads as one continuous lit band dropping at the entry, and **nothing else on the building lights** |
| Draw calls | **85** against the 300 budget (hooked `renderer.render` and took the max over the app's own frames — the stats overlay's own line reads 1 because `toypost.js` renders a second fullscreen quad and three resets `renderer.info` each `render()`) |

Screenshots: `integration/qa-in-city-day.png`, `integration/qa-in-city-night.png`.

### Fallback drill (Step 6) — mandatory, and it passes

GLB moved aside, page re-navigated with a cache-buster:

- The app **boots and the area renders** — `SF.city.stats` still reports 1,277 cells loaded,
  35,571 trees, 11,463 kit instances. Nothing else broke.
- **`failed: 1`** and exactly one console warning:
  `sf-assets: 164-south-park failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)`.
  That is Vite answering a missing `public/` path with the SPA `index.html` at HTTP 200 —
  a dev-server artifact, not a real 404. The drill still proves what it is meant to prove.
- **Case B behaviour confirmed:** the site is empty ground inside the exclusion zone, which is
  the expected and documented outcome for a new landmark — there is no procedural version to
  fall back to, because the exclusion removed it.
- GLB restored; `git status` clean apart from the intended changes.

### Batch mode — source-only branch

`git checkout -- app/public/tiles api/_data` after the QA, per
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`. Sanity check passes:
`git diff --name-only origin/main | grep -E '^app/public/tiles/|^api/_data/'` returns **0**
lines. The bake rewrote 1,977 generated files and every one of them was discarded; the batch
gets rebuilt once by `docs/asset-pipeline/BATCH-INTEGRATE.md`.

`cd app && npm run lint && npm run build` — both clean.

### Gate 5

| Item | Result |
|---|---|
| Re-bake chain | **PASS** (exit 0) |
| `audit.mjs` 1.6 | **PASS** — 100 zones over 97 landmarks clear |
| `verify-rebake.mjs` | **PASS** — nearest surviving footprint 3.8 m vs 2.6 m radius (its "dropped nothing" line is a count artefact; see above) |
| Tile point-in-polygon at the anchor | **PASS** — 1 ring (8.5 m) before, **0** after |
| Streams, merges, scale 1.0000 | **PASS** |
| Exactly one building on the site | **PASS** |
| Orientation, footprint, terrain seating | **PASS** |
| Night glow, intended surfaces only | **PASS** |
| Draw calls 85 / 300 | **PASS** |
| Fallback drill | **PASS** |
| Source-only branch | **PASS** — 0 generated files staged |
| lint + build | **PASS** |

**Not pushed, no PR, not deployed** — the pipeline ends at a local verified integration and
asks. Branch: `pipeline/164-south-park`.
