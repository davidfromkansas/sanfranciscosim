# 2 South Park (544 Second Street) — build report

Built 16 August 2026 from `docs/asset-plans/2-south-park.md` via
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` (BATCH mode). **REPORT beats plan:**
where this file and the plan disagree, this file is what shipped.

| | |
|---|---|
| Deliverable | `artifacts/2-south-park/2-south-park.glb` |
| Manifest id | `2-south-park` |
| Anchor | `-122.3932364, 37.7824236` (DataSF surveyed parcel 3775-005 area centroid) |
| Target height | 17.72 m (roof penthouse crest = bounding-box top, loader scale 1.0) |
| Triangles | **4,716** of a 9,000 cap |
| Shipping file | 138,056 bytes raw (60,131 gzip-9) after the stage-4 optimize pass |
| Dimensions | 36.298 x 36.298 x 17.720 m (axis-aligned; the building is 29.8 x 20.9 m at 45.2°) |
| Objects | **8** as shipped (141 authored, joined one-per-material in stage 4) |
| Materials | 8 — `Toy_brick`, `Toy_stone`, `Toy_glass`, `Toy_steel`, `Toy_roofd`, `Toy_ink`, `Toy_glass_Glow`, `Toy_trim_Glow` |
| Glow groups | 2 (`Toy_glass_Glow` lit offices, `Toy_trim_Glow` corner café) |
| Draw submeshes | 8 |
| Validation | `validation.json` — **all 16 checks PASS**, re-run against the shipped (optimized) file |

## 1. What is in the export

The single 1923 warehouse block: brick body on the surveyed footprint, brick
piers on the three public faces, cast-stone bands at every floor line, the
parapet and coping, 16 upper-floor sash and 14 ground-floor shopfront openings,
the recessed Second Street entry with its canopy, the blind southwest party
wall, the South Park fire escape, the light-membrane flat roof, the set-back
roof penthouse, the skylight, the mechanical group and the gas flue.

Not in the export: South Park, Taber Place, Second Street, sidewalks, café
tables, the bike-share dock, street trees, the utility pole, neighbours,
vehicles, people, plinths, cameras, lights — and **the roof flagpole**, omitted
deliberately per plan 2.10.

## 2. Reproducing it

```
blender -b --python build_2_south_park.py            # .blend + .glb
blender -b --python render_2_south_park.py           # 4 elevations + top + aerial
blender -b --python render_2_south_park.py -- --night # night aerial
python3 make_contact_sheet.py                        # contact sheet
blender -b --python validate_2_south_park.py         # validation.json
```

Blender 5.2.0 LTS. The build script is fully deterministic — no randomness, no
external assets, geometry authored directly in world space in metres.

## 3. Corrections this build made to the plan

1. **Bay proportions.** Plan 2.7 gave `PIER_W = 1.0` and 0.30 m clearance, which
   produced openings so wide that the first aerial review read as a modern glass
   curtain wall rather than 1923 masonry. Shipped: `PIER_W = 1.10`,
   `BAY_CLEAR = 0.42`, giving openings 3.29 m wide on Second Street and 3.03 m on
   the two long faces. The glass-to-brick ratio is still high, which is correct
   for this building, but the brick now carries the read.
2. **Sash frame colour.** Plan 2.8 assigned `Toy_steel` to the window frame
   bands. At the app's value range a light frame ring around every one of 30
   openings turned the facade into a grid of framed pictures. Shipped: the sash
   and shopfront frames are `Toy_ink`, matching the observed near-black steel;
   `Toy_steel` is now the light roof membrane and the entry canopy.
3. **Roof membrane value.** Plan 2.9 asked for a roof "clearly darker than the
   walls". That was wrong on both counts: the Vexcel nadir shows a **light-grey**
   membrane, and a dark deck merged the dark penthouse cap into it from above.
   Shipped: `Toy_steel` membrane with `Toy_roofd` penthouse cap, plant, skylight
   kerb and flue — the penthouse now reads as a distinct volume from the aerial
   camera and the composition matches the photograph.
4. **Ground floor.** Plan 2.7 step 2 put a 0.9 m `Toy_ink` base band around the
   building and started the piers at 4.30 m, which produced a continuous black
   ground storey. Shipped: a 0.35 m plinth, and the brick piers run all the way
   to the sidewalk as they do in the photographs, so brick shows between the
   shopfronts.
5. **Opening depth order.** The first build put the frame panel proud of the
   glazed fill; because the frame is a solid panel rather than a ring, it hid
   every window. Shipped: the fill protrudes to 0.14 m past a 0.08 m frame, and
   the glow shells to 0.19 m past the fill — so the glow is never coplanar with
   an opaque surface.
6. **Night composition.** The plan's lit-window scatter put one lit bay directly
   behind the fire escape, where it read as a shard. Moved to the next bay.

## 4. The open question the plan set, answered

**How much of the 17.72 m LiDAR maximum is penthouse?** Shipped as a penthouse,
7.0 x 5.0 m in plan, set back 2.5 m from the Taber Place parapet, rising 4.14 m
above the 13.58 m coping to exactly 17.72 m.

The evidence that settled it is the permit record rather than any image: SF
permit **201810163246** (2018) relocates an elevator machine room from the ground
floor to "(e) penthouse on roof" — the penthouse demonstrably pre-existed — and
permit **201709016716** (2017) adds the skylight, gas flue and roof mechanical
bracing that the nadir aerial shows beside it. A 4.1 m overrun is normal for a
1923 freight elevator converted to passenger service (which is exactly what the
2018 permit does).

The competing reading — that the maximum is street-tree canopy over the Second
Street parapet, as at 592 Third Street — is not refuted outright: a mature tree
does stand against that facade and rises above the parapet, and the 3.51 m LiDAR
*minimum* is the matching edge artifact at the other end of the distribution.
**This risk is contained by construction:** the crest is authored at exactly
17.72 m so `targetHeightM / measuredHeight` is 1.0, which means an error in this
number makes the penthouse too tall without making the building too tall. The
body still sits on its measured 12.83 m roof deck either way.

**Storey count.** Three, confirmed. Two 1992 permits record 2 and one 2017
electrical permit records 4; every permit from 1996 onward and the Assessor's
roll say 3, and three floors at ~4.28 m is the only reading consistent with a
12.83 m roof deck. The 1992 pair predate the retrofit and describe tenant space;
the 2017 figure is a clerical error on a permit whose own reference permit says 3.

**The Taber Place elevation stayed inferred.** No usable imagery of the alley
face was found; the nearest Street View panorama resolves onto a facade across
Taber Place. It is modelled with the same 6-bay pier-and-sash grid as South Park
over plain brick instead of shopfronts, with two service openings at ground
level. If it turns out to carry loading doors, that is a one-parameter revision
in `build_2_south_park.py`.

## 5. Contract deviations

**Orientation: "front faces −Y" is not honoured.** The asset is authored in true
world orientation (Blender +Y = north, +X = east) because `placeGeneric()` in
`app/src/assets.js` scales and positions but never rotates. The Second Street
front faces NE at 45.2° true and the South Park front SE at 135.2°. Real-world
orientation wins (AGENTS rule 5); this is the same deviation every landmark in
this set carries and it is recorded here as required.

No other deviations. No textures, no transparency, no `Toy_body`, no cameras,
lights, animations, armatures or constraints, transforms applied, no negative
scales, normals outward (per-object signed volume positive on all 141 solids;
the ray test residual is within the 0.15% tolerance), no foreign geometry.

## 6. Approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"
> — David, 16 August 2026, in the session that commissioned this build

Stage 3's human gate was pre-granted in the invoking instruction, so the asset
advanced from stage 2 to stage 4 without a separate approval round. The renders
and numbers presented for that gate are the ones in this directory: the contact
sheet, `2-south-park-aerial.png`, `2-south-park-aerial-night.png`, 4,716
triangles, 36.3 x 36.3 x 17.72 m, 8 materials, 2 glow groups.

## 7. Manifest entry (verified)

```json
{
  "id": "2-south-park",
  "file": "2-south-park.glb",
  "anchor": [
    -122.3932364,
    37.7824236
  ],
  "targetHeightM": 17.72,
  "cat": 3,
  "name": "2 South Park",
  "estimated": false,
  "dims": [
    36.2984,
    36.2984,
    17.72
  ],
  "tris": 4716,
  "loadRadius": 2500
}
```

`cat: 3` (office) rather than `20` (warehouse): the Assessor still codes the
parcel `IND`, but that is a stale roll code for a 1923 building whose permits
have recorded it as retail over office since 2016.

## 8. Stage 4 — optimize

Run per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`; full metrics, census, A/B
deltas and gate table in `optimize/REPORT.md`. Headline: 141 objects → 8
(one per material), 9,904 → 2,628 source vertices, 333,764 → 138,056 raw bytes
(−58.6%), triangles unchanged at 4,716, all eight gates PASS with a worst-case
A/B pixel delta of 0.0489%. The limited-dissolve step was skipped: this asset
carries six coplanar ring bands and the step is the only one that can
manufacture sliver geometry.

The optimized file is now `2-south-park.glb`; the pre-optimize original is
archived byte-for-byte at `optimize/input/2-south-park.glb`. The review renders,
contact sheet, night render and `validation.json` in this directory were all
regenerated from the shipped file, so every image depicts exactly the geometry
that ships.

One number is worth flagging: gzip-9 bytes *rose* 44,513 → 60,131, because
meshopt output is already entropy-coded while the unpacked float32 input gzips
extremely well. The asset is packed anyway — `pipeline/compress-assets.mjs`
would do it at intake regardless — and both figures sit far inside the 500 KB
budget. `optimize/REPORT.md` §4 records the trade in full.

## 9. Stage 5 — integration (Case B, BATCH mode)

Done, on branch `pipeline/2-south-park`, per `INTEGRATION-PROMPT.md` Part 1 with
the batch amendment: the bake was run and used for QA, then discarded, and the
branch commits **source only**. `git diff --name-only origin/main` lists nothing
under `app/public/tiles/` or `api/_data/`.

Registry entry added to `pipeline/lib/landmarks.mjs`:
`id: '2SouthPark', lon: -122.3932364, lat: 37.7824236, height: 17.72, exclude: 9`,
`camera: { distance: 200, yaw: 90, pitch: 26 }` (yaw 90 puts the camera due east,
square onto the corner where both public elevations read).

### Local QA

| Item | Result |
|---|---|
| Re-validation of the shipped GLB | **PASS** — all 16 contract checks, 4,716 tris, 36.298 × 36.298 × 17.720 m, min z 0.0, XY centre (0, 0) |
| `compress-assets.mjs` on intake | **PASS** — `skip (already compressed): landmarks/2-south-park.glb` (the stage-4 pack is the shipping encoding) |
| Manifest entry | **PASS** — 59th entry, valid JSON, formatting matches its neighbours |
| id mapping | **PASS** — `camelId('2-south-park')` → `2SouthPark`, which is the registry id |
| Registry + re-bake | **PASS** — full 11-stage chain in 72 s on a warm `pipeline/data/` |
| `audit.mjs` check 1.6 | **PASS** — "no procedural footprint inside a bespoke landmark exclusion zone — 66 zones over 65 landmarks clear" |
| `verify-rebake.mjs` | **PASS** — "only the new landmarks' cells moved"; **584 of 585 cells unchanged**; cell 23_13 went 217 → 215 buildings (the two footprints are this building's DataSF and Overture representations); nearest surviving footprint **16.8 m vs the 9 m radius**, matching the predicted 16.76 m ceiling to 4 cm |
| Merge line | **PASS** — `sf-assets: 2-south-park merged 8 objects / 8 materials -> batched (3226 tris body); uniform x1.0000 at 3895, -1373` |
| Scale factor | **PASS** — exactly **1.0000** |
| Single building | **PASS** — one building on the lot, no procedural twin, no baked block poking through, no z-fighting |
| Footprint / orientation | **PASS** — six bays on the south-east (South Park) face and four on the north-east (Second Street) face, read from a camera due east; the blind party wall is on the south-west |
| Terrain seating | **PASS** — sits flat on the sidewalk grade, no float, no sink |
| Night glow | **PASS** — at `night 1.00` the warm café glow wraps the east corner on both street faces and five scattered office windows light on the upper floors; the roof, the alley face and the party wall stay dark |
| Draw calls | **PASS** — **95** for the whole scene at this SoMa street-level view against a 300 budget (measured with a direct `renderer.render(scene, camera)` and `renderer.info.render.calls`; the F3 overlay reads 1 because it samples `renderer.info` after the post stack has already reset it, which is pre-existing) |
| Fallback drill | **PASS** — with the GLB renamed the app boots, the district renders, the site is empty ground inside the exclusion zone (expected for Case B), and exactly one warning appears: `sf-assets: 2-south-park failed to load`. Restored afterwards and re-verified. |
| `npm run lint` / `npm run build` | **PASS** — eslint clean; Vite build 1.11 s |
| 3 audit checks that FAIL | pre-existing on `main` (1.2b height band, 1.3c Telegraph Hill DEM, 1.7b one offshore tree) — not attributable to this change |
| `GL_INVALID_OPERATION: glDrawArraysInstanced` console warnings | pre-existing — they appear during asset streaming both with this landmark present and with it renamed away, and before it loads at all |

Two honest caveats on the local run. The in-app screenshots were taken through
the hidden Browser pane, where rAF only advances while a screenshot is being
captured, so surrounding tiles are frozen mid-crossfade (the hashed-alpha
dither) in several frames; that is a harness artifact, not a scene bug. And for
the same reason the fps figure in the overlay is meaningless here — the frame
rate was not measured, only the draw-call count.

### Still to do

Nothing on this branch. The city gets rebuilt once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`, which is also where the PR is opened
and where the deployed QA on https://sf-3d.vercel.app runs.
