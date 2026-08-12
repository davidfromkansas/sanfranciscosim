# 540 Presidio Boulevard — integration record

Stage 5 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executing
`docs/asset-plans/INTEGRATION-PROMPT.md` Part 1 as **Case B** (new landmark).

**Read this first: the integration is complete except for one step I could not
run — the tile re-bake.** Until it runs, the baked procedural building is still
on this footprint and the GLB sits on top of it. Details and the exact commands
are in "The outstanding step" below, and
`node artifacts/540-presidio-blvd/check_baked_twin.mjs` reproduces the finding
in one second on any checkout.

## What changed

| File | Change |
|---|---|
| `app/public/sf-assets/landmarks/540-presidio-blvd.glb` | new — the shipping asset, 112,108 bytes, already meshopt-compressed |
| `app/public/sf-assets/landmarks_manifest.json` | one entry appended, 19 lines, no other entry touched |
| `pipeline/lib/landmarks.mjs` | one `LANDMARKS` entry appended (Case B registry + exclusion zone) |
| `artifacts/540-presidio-blvd/` | the asset, its scripts, renders, dossier, report and optimize pass |
| `docs/asset-plans/540-presidio-blvd.md`, `docs/asset-plans/README.md` | the plan and its row in the set table |

No app code changed. No procedural builder was deleted or edited (AGENTS rule 3).
No generated tile was hand-edited (and none was regenerated — see below).

## Step 1 — Re-validation before touching the app

Re-imported `artifacts/540-presidio-blvd/540-presidio-blvd.glb` into a fresh,
isolated Blender scene and re-ran the full contract check on the **shipped,
post-optimize** file. `validation.json`, **overall PASS**, all 16 checks true:
3,690 triangles (cap 6,000), min Z 0.0, XY centre (0, 0), max Z 11.5000 exactly,
10 materials all `Toy_*`, no textures, no alpha < 1, no `Toy_body`, no cameras or
lights, no animation, transforms applied, no negative scales, 10/10 solids
outward by signed volume, 0 flipped faces in 31,500 rays, 0 degenerate triangles.

The measured `dims` and `tris` from that run — not the plan's estimates — are
what went into the manifest.

## Step 2 — Drop-in and the mandatory compression step

Copied to `app/public/sf-assets/landmarks/540-presidio-blvd.glb`, not renamed,
not re-exported. `node pipeline/compress-assets.mjs` reported
`skip (already compressed): landmarks/540-presidio-blvd.glb` — the stage-4
optimize pass had already applied the identical `-c -km -kn -noq` gltfpack
invocation, which is the point of doing it there.

## Step 3 — Manifest entry

```json
{
  "id": "540-presidio-blvd",
  "file": "540-presidio-blvd.glb",
  "anchor": [-122.4519224, 37.7966667],
  "targetHeightM": 11.5,
  "cat": 1,
  "name": "540 Presidio Boulevard",
  "estimated": true,
  "dims": [16.6623, 22.7566, 11.5],
  "tris": 3690,
  "loadRadius": 2500
}
```

Appended as text so the diff is 19 added lines and nothing else — a JSON
round-trip would have silently rewritten `11.0` to `11` in an unrelated entry.

- `estimated: true` — the 11.5 m height is derived, not published (`REFERENCE.md` §4).
- `loadRadius: 2500` — the default `max(2500, targetHeightM × 30)`. The
  absence-illegibility test passes at any radius past ~600 m for an 11.5 m
  house, so there was no reason to tune below the default. Explicitly **not**
  `alwaysLoaded`.
- **id mapping verified live:** `camelId('540-presidio-blvd')` → `540PresidioBlvd`,
  which is the id used in `pipeline/lib/landmarks.mjs`. Confirmed in the running
  app: `SF.assets.placed` contains the key `540PresidioBlvd`.

## Step 4 — Case B registry entry

Added to `LANDMARKS` in `pipeline/lib/landmarks.mjs` with `exclude: 15`.

That radius is measured, not guessed:

| Distance from the anchor | What is there |
|---|---|
| 12.2 m | the far corner of this house's own footprint (14.47 × 19.72 m OBB, half-diagonal) — the radius must be at least this |
| **15 m** | **chosen** |
| 19.1 m | the nearest vertex of **541 Presidio Boulevard**, a separate baked building with no bespoke replacement — the radius must stay under this |

Both numbers were read out of the shipped tile
`app/public/tiles/buildings/13_10.bin`, where this house is baked building 33
and 541 is building 39. A generous circle would have deleted a neighbour and
left a hole. `check_baked_twin.mjs` confirms the radius catches exactly one
footprint — this one — and no others.

## The outstanding step — the tile re-bake

**Status: NOT DONE. This is the one thing standing between this branch and a
visually correct scene, and it is called out here rather than buried.**

`pipeline/buildings.mjs` builds its exclusion list from `LANDMARKS` **at bake
time**, and the results are the committed binaries under `app/public/tiles/`.
Adding the registry entry without re-baking therefore changes nothing on screen:
the baked procedural building is still on this footprint.

**Verified, not assumed.** Decoding `app/public/tiles/buildings/13_10.bin`
against the format in `pipeline/lib/binio.mjs` finds baked building index 33
with a 12-vertex footprint whose nearest vertex is **5.68 m** from the anchor —
this house, baked at `topY` 51.5 m absolute. In the running app, hiding the
`landmark-assets` group leaves that procedural mass standing on the same spot.
Screenshots of both states are in the PR description.

Why it was not run here:

1. `pipeline/download.mjs` requires the `overturemaps` CLI, which is not
   installed on this machine, and PR #94 deliberately made the bake **fail loudly
   without Overture** rather than silently bake a flat skyline. Installing it
   plus fetching the sources is a ~700 MB, long-running step.
2. More importantly, a re-bake today pulls **today's** OSM / DataSF / Overture
   data. That would rewrite tiles across the whole city and bury a one-house
   change in an unreviewable diff of the 84 MB tile set — and could regress
   other landmarks in ways nobody would spot in review.

`node pipeline/audit.mjs` check 1.6 is the canonical test for this, but it
cannot run on a checkout that has never baked (it loads `pipeline/out/terrain.json`,
which is gitignored). `check_baked_twin.mjs` was written to answer the same
question from the **shipped** tiles alone:

```bash
node artifacts/540-presidio-blvd/check_baked_twin.mjs
# 540PresidioBlvd: cell 13_10, 65 baked buildings, exclusion radius 15 m
# FAIL — 1 baked footprint(s) still inside the exclusion zone:
#   {"index":33,"nearestVertexM":5.68,"topY":51.5,"verts":12}
```

To clear it, on a machine with the pipeline sources:

```bash
pip3 install overturemaps
cd pipeline && npm install
npm run download && npm run loredata
npm run terrain && npm run bridges && npm run buildings && npm run streets \
  && npm run landcover && npm run validate && npm run lore && npm run toy \
  && npm run notables && npm run context
node audit.mjs                                    # check 1.6 must pass
node ../artifacts/540-presidio-blvd/check_baked_twin.mjs   # must exit 0
```

Then commit only the tiles under `app/public/tiles/` that actually changed.

## Step 5 — Local verification

`npm run dev` in `app/`, real browser, camera flown to the anchor.

| Check | Result | Evidence |
|---|---|---|
| Manifest served | **PASS** | `/sf-assets/landmarks_manifest.json` → 200, entry present and correct |
| GLB served | **PASS** | `/sf-assets/landmarks/540-presidio-blvd.glb` → 200, `content-length: 112108` |
| Asset placed | **PASS** | `SF.assets.placed` contains `540PresidioBlvd`; `failed: 0` |
| Merge to 2 draw calls | **PASS** | placed into the shared `landmark-bodies` / `landmark-glow` `BatchedMesh` pair, as every generic landmark is |
| **Scale factor** | **PASS** | log line `uniform x1.0000 at -1269, -2948` — **exactly 1.000**, so the authored height and `targetHeightM` agree perfectly |
| id → pipeline id round trip | **PASS** | `camelId` → `540PresidioBlvd`, matches the registry entry |
| Orientation | **PASS** | the porch front faces east onto the walk down to Presidio Boulevard; the plan sits at its +6.49° heading against the real street grid |
| Terrain seating | **PASS** | placed at y 42.75 m from `sampleElevation`; no floating, no sinking on the rise |
| Footprint size vs neighbours | **PASS** | reads correctly against the adjacent baked houses and the roadway width |
| Night glow | **PASS** | at `night 1.00` only the two lit east windows and the porch lantern light; the roof, walls and all other windows stay dark |
| **Exactly one building at the spot** | **FAIL** | the baked procedural twin is still there — the re-bake above. This is the known, declared gap, not a surprise. |
| Draw calls / fps under 300 | **NOT MEASURED** | the in-app stats overlay reported `fps 0 · draw calls 1` because the automated browser pane throttles the render loop when hidden; those are artefacts of the harness, not readings. This asset adds **zero** draw calls by construction — it joins the existing shared batch pair — but the number was not independently measured here and is not claimed. |

## Step 6 — Fallback drill

Pointed the manifest entry at a nonexistent file
(`540-presidio-blvd.FALLBACK-DRILL.glb`) and reloaded.

- **PASS:** the app boots and the Presidio renders normally.
- **PASS:** all 18 other in-range landmarks load and merge as usual;
  `SF.assets.stats.failed` stays **0**; nothing throws.
- **PASS:** the 540 entry is simply absent from `SF.assets.placed` — no hole, no
  crash.
- **NOT OBSERVED:** the specific one-line
  `sf-assets: … — keeping the code-built landmark` warning. This entry is
  *streamed* (`loadRadius: 2500`), so that warning fires on the approach fetch,
  which the throttled headless browser pane never triggered. The boot-path
  fallback is verified; the streamed-fetch warning is not, and is reported as
  unverified rather than assumed.

Manifest restored afterwards; `git status` clean of drill leftovers.

Note that for a Case B landmark the correct fallback appearance is *empty
ground* inside the exclusion zone, since the baked footprint is carved out and
there is no code-built version to fall back to. Today, pre-re-bake, the baked
building is still present — so the drill currently degrades to "the baked house
is there", which is friendlier than the post-re-bake behaviour will be.

## Step 7 — Lint and build

```
cd app && npm run lint   # clean
cd app && npm run build  # ✓ built in 2.13s; compress-tiles 3314 tiles 56.0 MB -> 31.5 MB
```

Per the pipeline doc, stage 5's Step 7 (push / PR / deploy / production QA) is
replaced by a stop-and-ask. The user explicitly asked for a branch and a PR up
front, so the branch is pushed and the PR opened; **deployment and production QA
are not done** and should wait for the re-bake.
