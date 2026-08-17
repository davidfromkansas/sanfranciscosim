# 26–28 South Park (51 Taber Place) — build report

Asset: `artifacts/26-south-park/26-south-park.glb`
Plan: `docs/asset-plans/26-south-park.md`
Dossier: `REFERENCE.md`
Built: 17 August 2026, Blender 5.2.0 LTS, headless.

**REPORT beats plan.** Where this file and the plan disagree, this file is what
shipped.

## Shipped numbers

| | |
|---|---|
| Triangles | **2,512** (cap 6,000) |
| Objects | 8 after stage 4 (57 as built) |
| Dimensions | 25.938 × 26.042 × **9.050** m |
| Footprint in plan | 30.13 × 6.69 m = 201.6 m² |
| min Z | 0.000 m |
| XY centre offset | 0.000, 0.000 m |
| Materials | 8 — `Toy_glass`, `Toy_glassl_Glow`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_trim`, `Toy_trim_Glow` |
| Glow groups | 2 (`Toy_glassl_Glow`, `Toy_trim_Glow`) |
| GLB on disk | **71.1 KB** meshopt-compressed (stage 4); 163.6 KB pre-optimize |
| `targetHeightM` | 9.05 — bbox top is the parapet, so the loader's scale is **1.0** |
| Manifest anchor | `-122.3937438, 37.7822369` |
| Validation | **PASS**, all 16 checks, re-run against the shipped optimized file — `validation.json` |

The XY bounding box is ~26.0 × 26.0 m for a 6.69 × 30.13 m building. That is the
exact consequence of a 315.18° real-world heading, not a scale error.

## 1. The height decision, and why the LiDAR maximum was thrown away

This is the one consequential judgement in the asset, and it was made against the
record rather than from it.

DataSF's LiDAR footprint SF3775049 reports `hgt_max = 13.59 m`. Taking it would
have produced a building 4.5 m taller than the one that shipped. It was rejected
on three independent grounds:

1. **It matches the neighbour to 7 cm.** 44–46 South Park (SF3775217) has a roof
   plane median of **13.52 m**. This footprint is 7.65 m wide in a raster of
   50 cm cells, dilated at both edges into party walls with *taller* buildings
   behind them. `docs/asset-plans/README.md` records this exact failure on the
   Earl Warren Building — "treat a single-cell `hgt_max` on a party wall as
   unusable".
2. **The distribution is right-skewed.** Mean 8.95 m against median 8.35 m and
   majority 8.36 m, with std 1.48 m. A minority of high cells is dragging the
   mean; median and majority agreeing to 1 cm says the true plane is very well
   determined.
3. **The 2026 aerial shows nothing there.** The roof is a plain pale plane — no
   penthouse, no plant tower, no second storey-and-a-half.

Shipped: **deck 8.35 m** (the median), **parapet crest 9.05 m** (a conventional
0.70 m parapet). Two storeys at ~4.2 m each is consistent with 8.35 m, with the
"high ceilings" the leasing listing advertises, and with the double-height
interior visible in the January 2012 business photosphere at this address.

Unlike most height questions in this set, the risk here is **not** contained by
the loader's scale-to-1.0: if 8.35 m is wrong the building is a hole in the row.
It is flagged in the plan's 2.15 and left open for a better photograph.

## 2. Corrections made against the plan

**2.1 Glow shells are closed, not open faces.** The plan as first written said
every `_Glow` surface should be "a single open face", on the reasoning that a
closed shell is two 12%-alpha layers by day. That is the right *observation* and
the wrong *conclusion*: the repo's normals contract runs a per-object
signed-volume test, an open plane has no signed volume, and the first build
failed `normals_outward_signed_volume` and `normals_outward_ray_residual` on
exactly the three glow objects (ray residual 0.86% against a 0.15% allowance).

The established repo convention — and what `artifacts/106-south-park/` does — is a
thin **closed** shell, with the doubled day alpha handled by *sizing and colour*
rather than by topology. Shipped: each glow shell covers only the **lower 55%** of
its opening, in `Toy_glassl_Glow` (`#6f95b8`, desaturated) or `Toy_trim_Glow`
(`#f3efe6`, near-white), at a distinct offset from both the glass fill and the
frame so no two planes are coplanar. Validation then passed with a ray residual of
**0.0**. The plan text has been corrected to match.

**2.2 The entry notch is a real void.** The plan's step 4 described "a 1.8 m-wide,
1.6 m-deep entry notch". The first build added reveals and a soffit *inside* a
solid ground-storey prism, which buried the entrance completely — the facade
rendered as a blank wall with a floating head band. The ground storey is now built
as four prisms (front-south-west, front-north-east, header, main) that leave the
notch as an actual gap in the mass.

**2.3 Two coplanar-cap bugs.** The roof membrane and the open-deck floor were both
authored *flush into* the storey cap below them (top at Z_DECK and Z_FLOOR2
respectively). Coplanar faces z-fight and the darker one won, so the first build
had a black roof and an invisible terrace — the two things this asset exists to
show. Both slabs now sit **on** the cap rather than in it (`Z_DECK` → `Z_DECK +
0.12`), and the skylights and plant ride the raised slab.

**2.4 Five skylights, not three.** The plan's step 11 called for three. On the
first good render a 30 m pale roof with three small boxes read as an
under-designed blank — and the style bible is explicit that the camera looks down
and roofs are facades. Shipped: five, at 2.40 × 1.55 × 0.38 m, on the centre line
at 4.0 m spacing over the rear two thirds. The count is not documented anywhere
(the leasing listing says "skylights" without a number), so this is a composition
decision, not a discovered fact.

## 3. What stayed inferred

- **The Taber Place rear.** Modelled from a January 2025 pano labelled "22 Taber
  Pl" showing a dark-brown lap-sided two-storey face with large grid windows, a
  glazed garage door and a personnel door. Position and colour fit, but the pano
  that resolves cleanly onto *this* lot could not be isolated. **This is the most
  valuable single observation left to make about the building.**
- **The garage is at the Taber Place end**, on the strength of the Assessor's
  address of record (51 Taber Place). The 2019 permit's "man doors to garage on
  1st floor" does not say which end.
- **The 3.0 m setback depth** of the top floor. The railing and the set-back wall
  are observed; the depth is not.

## 4. Deviations from the technical contract

**"Front faces −Y" is not honoured.** The building is authored at its real-world
heading, so its street elevation faces 135.18° rather than −Y. AGENTS rule 5
(real coordinates, real orientation) wins over the contract's default, exactly as
in every other South Park asset. The loader applies no rotation.

No other deviations. No textures, no transparency, no `Toy_body`, no cameras,
lights, animations, armatures or constraints; transforms applied; no negative
scales; normals outward by per-object signed volume with a 0.0% ray residual.

## 5. Scope — what is deliberately not in the GLB

South Park and its trees, Taber Place, the sidewalk, the street tree standing
directly in front of the entry, the utility pole and overhead wires, the
neighbours at 22–24 and 44–46, vehicles, people, plinths, cameras and lights.

Also omitted, and each real: the **entry wall lantern**, the **notice board** on
the entry return, the **six wall-mounted bike racks** the leasing listing
advertises, the **security camera**, and all signage. Every one is under a pixel
at the app's camera.

## 6. Review iterations

| # | What was seen | What changed |
|---|---|---|
| 1 | Roof and terrace both rendered black; entrance invisible; facade a blank dark plane | coplanar caps raised (2.3); ground storey split to void the entry notch (2.2) |
| 2 | Roof legible but under-designed — three small boxes on 30 m of blank membrane; deck cropped in the top view | five larger skylights (2.4); top-view ortho scale 33.5 → 34.5 so the terrace is in frame |
| 3 | Validation FAIL on normals: the three glow objects | closed glow shells at 55% coverage (2.1) — validation PASS, ray residual 0.0 |

Reviewed from the high three-quarter aerial first at every iteration, per the
plan's Part 1; the formal rig was run only after the aerial read correctly.

## 7. Draft manifest entry

```json
{
  "id": "26-south-park",
  "file": "26-south-park.glb",
  "anchor": [
    -122.3937438,
    37.7822369
  ],
  "targetHeightM": 9.05,
  "cat": 3,
  "name": "26–28 South Park",
  "estimated": false,
  "dims": [
    25.938,
    26.042,
    9.05
  ],
  "tris": 2512,
  "loadRadius": 2500
}
```

Registry entry for `pipeline/lib/landmarks.mjs`: `lon: -122.3937438`,
`lat: 37.7822369`, `height: 9.05`, **`exclude: 3.4`** — the midpoint of a
measured (2.21, 4.62) m band, the tightest in the South Park set. The ceiling is
44–46 South Park's nearest DataSF vertex and the floor is this building's own
**Overture** ring, not its DataSF one. See the plan's 2.13 for the full table and
for why the drop list must be checked *by which rings*, not by how many.

## 8. Approval

Stage 3 approval, quoted verbatim from the session that commissioned this asset
(16 August 2026):

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Recorded as a standing pre-approval covering stages 3 through 5 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` for this building. No per-iteration
approval was sought; the review iterations in §6 were self-directed against the
style bible.

## 9. Stage 5 — local integration QA (batch mode)

Run 17 August 2026 against this worktree's own Vite dev server, driven in real
headless Chrome over CDP. The served manifest was checked first — 74 entries,
`26-south-park` present — because a dev server pointed at the wrong tree is the
failure mode that wastes the most time here.

| Check | Result |
|---|---|
| Placement | `uniform x1.0000 at 3850, -1353` — the loader's `targetHeightM / measuredHeight` lands on **exactly 1.0** |
| Orientation | camera preset yaw 45°; the slot runs South Park → Taber Place with the open deck at the near end |
| Terrain seating | seats on the rim with no gap or sink at either party wall |
| **The step** | reads exactly as designed — the roof sits clearly below both neighbours and the building is the dark notch in the row |
| Streaming | `entries 74, live 18, failed 0` at `loadRadius: 2500` |
| Draw calls | **125** max per frame at the landmark, against a 300 budget |
| Night glow | the quietest in the set, on purpose: one lit second-floor window and the entry spill, while every neighbour lights up in yellow |
| `pipeline/audit.mjs` 1.6 | **PASS** — 83 zones over 80 landmarks clear |
| Cell 23_13 | `origin/main` 201 buildings → re-baked **200**; the two rings left within 12 m of the anchor are the Hotel Madrid at 8.6 m and 44–46 South Park at 10.3 m — **both neighbours standing**, which is what the 1.2 m margin above the 4.60 m ceiling was for |

Draw calls were measured by hooking `renderer.render` and keeping the per-frame
maximum; the in-app stats overlay reads `1` because `toypost.js` renders a
fullscreen quad after the scene and three resets `renderer.info` on every
`render()`.

Note that the landmark must be **polled for**, not waited on: the rig eases to the
target and the streaming scan only fetches once the camera is genuinely inside
`loadRadius`, so a fixed sleep after `SF.goTo` reports `placed: false` perhaps half
the time and looks exactly like a broken radius.

### Fallback drill

With `app/public/sf-assets/landmarks/26-south-park.glb` moved aside: the app boots,
all 74 manifest entries load, the entry goes to **`failed: 1`**, 18 other landmarks
go live and nothing crashes.

As with its neighbour, the site is then an **empty lot** rather than a procedural
block — for a Case B landmark the exclusion has already removed that footprint from
the baked tiles. This is inherent to Case B, not a defect in this asset.

### Batch-mode handoff

The re-bake was run in full and QA'd on, then discarded with
`git checkout -- app/public/tiles api/_data`. `git diff --name-only origin/main`
lists nothing under `app/public/tiles/` or `api/_data/`. The branch carries source
only. `node pipeline/compress-assets.mjs` again re-compressed the unrelated
`vehicles/passenger-airplane.glb`; it was reverted. This asset was correctly
skipped as already carrying `EXT_meshopt_compression` from stage 4.
