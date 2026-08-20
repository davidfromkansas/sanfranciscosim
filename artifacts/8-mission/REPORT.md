# 8 Mission Street — build report

**Asset:** `artifacts/8-mission/8-mission.glb` — 1 Hotel San Francisco (Hotel Vitale),
8 Mission Street, San Francisco. Built from `docs/asset-plans/8-mission.md`
via `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, `BATCH: yes`.

## Shipped numbers (post-optimize — these are the numbers the manifest is written from)

| | pre-optimize | **shipped** |
|---|---|---|
| Triangles | 19,082 | **19,082** (cap 26,000) |
| Mesh objects | 689 | **14** |
| Draw submeshes | 696 | **16** |
| Dimensions | 74.138 × 56.548 × 28.660 m | **identical to 5 dp** |
| min Z / XY centre offset | 0.000 m / (0.000, 0.000) | unchanged |
| Materials | 12, all `Toy_*` | 12, identical set |
| Glow materials | `Toy_glass_Glow`, `Toy_glassl_Glow`, `Toy_gold_Glow` | unchanged |
| File | 1,330,784 B raw | **485,656 B** raw (−63.5%), meshopt |
| Roof plateaus | 25.10 / 19.64 / 14.18 m; turret crown 28.66 m | |
| **Manifest anchor** | **`-122.3932861, 37.7936872`** | |
| Validation | overall PASS | `validation.json` — **overall PASS**, 17/17, re-run on the packed file |

Stage 4 detail is in `optimize/REPORT.md`; the pre-optimize asset is archived
byte-for-byte at `optimize/input/8-mission.glb`.

Normals (on the shipped file): 14/14 closed solids enclose positive signed volume; 206/206 open glow-strip
faces are the first face a ray along their own normal meets; 31,432 visibility rays from
nine interior targets, **0 flipped** (tolerance 0.15%); 0 degenerate triangles; 0
non-unit loop normals.

The axis-aligned XY box is 74.14 × 56.55 m for a 64.08 × 42.07 m building because the
block sits at 45.37° to the world axes. It is **not** square, which a rotated rectangle
would be: the L-shape's missing north quadrant shortens one world diagonal.

## Dossier corrections

Seven, all listed with their reasoning in `REFERENCE.md` § "Corrections". In summary:
plateau C is **14.18 m** not 13.80 (the plan printed a figure from a discarded storey
grid); the shipping anchor is 5.45 m south of the plan's OBB centre; the XY box is
74 × 57 m not 75 × 75; the Mission wall runs 30.68 m not 26.4; the notch tangent is
solved rather than read off a vertex; `-steps.png` is rendered from the south-west
because that is the only elevation carrying all three plateaus; and the renders are
EEVEE.

## Build iterations

Every one of these was caught by looking at the high three-quarter aerial first, as the
style bible requires, and none of them was visible in any elevation.

**1. A duplicated polygon vertex deleted the plaster attic.** The concave notch arc was
spliced into the footprint next to the wall point it starts from, leaving a ~20 mm edge
whose direction is numerical noise. Every offset ring built from that polygon then shot
a spike out of that corner — and `inset_polygon(pa, +0.30)`, which should have set the
attic 0.30 m *back*, put it 0.29 m *proud* instead. The recess simply did not exist, the
parapet rendered as a dashed brick band, and the Mission elevation read as one
undifferentiated brick block. Fixed by solving both notch tangents from the fitted
circle and running a `dedupe(poly, tol=0.02)` over every spliced outline. The tolerance
has to be centimetres, not `1e-9`: the arc tangents and the wall corners genuinely
disagree at that scale.

**2. The piers hid the attic even after that.** The brick pier run was carried from the
arcade head to the parapet on every elevation, so on plateau A it stood at the outer
wall plane straight across the recessed attic. Piers now stop at the setback and a stone
sill course marks the top of the brick; the attic carries its own shorter windows on the
recessed plane.

**3. The roof membrane poked out through the notch.** It was built as a bounding
rectangle over the Mission end. Invisible in all four elevations, obvious from directly
above. It now follows the plateau polygon.

**4. The turret's outline left the wall through the wrong tangent.** The drum crosses
both walls it stands in (it clears Mission by 0.09 m and The Embarcadero by 0.29 m), so
each wall has two crossings. The first build took the far one on each, burying ~1.8 m of
wall inside the drum. Both tangents are now derived, and the outline runs round the
outside of the circle between them.

**5. The lantern crown was a propeller.** Eight fins at r 5.90 m around a small centre
cap read from the aerial as a black rotor. The brim came in to r 5.45 and the centre
drum became the tall part, so it reads as a lantern with the fins as a rim.

**6. The terraces were a billiard table.** Seven large rectangles of `Toy_leaf` — which
is what the satellite image looks like at a glance — read as one green slab. Replaced by
a grid of ~30 small panels with wide `Toy_stone` paths between them.

**7. The arch rings were a quad strip between two open paths**, which pinched to zero at
each springing and produced 4 degenerate triangles and 28 non-unit loop normals across
nine of eleven arches. Rebuilt as two nested extruded profiles — a stone reveal and a
glass void — which is both cheaper and clean.

**8. Two thirds of the turret's night glow was inside the building.** A glow band round
the full circumference is mostly buried, because below the roofline only ~122° of the
drum is outside the walls. The two shaft bands are now limited to the exposed arc; the
crown band above the parapet wraps 260° but stops short of the quadrant that faces the
roof screen and the vent stacks.

**9. Glow winding cannot be inferred from the model centroid on this building.** The
turret sweeps past it and the concave notch faces the opposite way from every convex
surface on the asset. All glow strips are now wound from an explicitly supplied outward
vector (radial for the turret, *inward*-radial for the notch, the face normal for
windows), never recalculated and never inferred. That change alone took the ray-test
residual from 1.49% to 0.

**10. The canopy had no arch in it.** It was swept as a half-cylinder whose axis ran out
from the wall, with the back half clamped to d = 0 — a dark wedge. The curve belongs in
the *wall* plane: it is now a segmental arch ~6.4 m wide rising 1.55 m, extruded 2.2 m
forward, with glazed infill and a warm strip underneath.

**11. Windows broke the wall they were in.** The top body row's head landed 0.07 m above
the setback and would have pushed through the parapet in the attic. The runs now cap
against the wall they belong to, and the attic gets its own shorter opening.

## Night state

Hero: **the turret's glazed bands**, sitting 0.05 m proud *inside* the eight brick ribs
so the ribs break the lantern into lit bays — seven circular suites, not a floodlit drum.
The crown band above the parapet has to clear the ribs instead (0.26 m), because up
there they are the outermost thing. Supporting: the `Toy_gold_Glow` strip under the
entrance canopy, the curved lobby glazing in the notch, and 40 lit guest-room windows
scattered by a deterministic hash across all three plateaus — about a fifth of the
openings, irregular, which is the truthful pattern for a 200-room hotel.

Every glow surface is an **open single-layer strip**. None is a closed shell: the app
draws `_Glow` in a separate layer that is translucent by day, and a closed box shows its
front and its back face, reading at roughly twice the intended day alpha.

## Renders

Engine **`BLENDER_EEVEE`**, 64 TAA samples, `Standard` view transform. Load average on
the build machine was 149 with ~16 concurrent Blender processes; CPU Cycles makes no
progress there, and nothing this pass judges — silhouette, massing, step, material band,
which surfaces glow — needs path tracing. All eight images are rendered from the
**re-imported GLB**, never from the authoring scene.

`8-mission-south.png` (Mission), `-east.png` (The Embarcadero), `-west.png` (Steuart),
`-north.png` (Don Chee Way), `-steps.png` (the massing check, south-west),
`-top.png` (the three parapet rings), `-aerial.png` (due east, the app's own preset
azimuth), `-aerial-night.png`, `-contact-sheet.png`.

## Integration (stage 5) — DONE, source-only per `BATCH: yes`

Case B. Cell **`23_10`**. Ran on `pipeline/8-mission`, rebased onto `origin/main`
`2c14d5f9f`.

### The branch moved under us

`origin/main` advanced 20 commits mid-session — PR #157 merged thirteen more SoMa
landmarks **and their city re-bake**. The first `verify-rebake.mjs` run therefore
flagged a stray cell (`23_13`, 169 → 182 buildings) that had nothing to do with this
radius: it is the South Park / Brannan super-cell carrying 52 exclusions, and the
thirteen new ones were missing from the pre-rebase registry. Rebasing onto current
`main` took the registry from 97 to **110 landmarks** and the whole bake was redone
against it. The rebase also picks up `perf(assets): raise the landmark body reserve to
1.6M vertices`, which matters here: the shared landmark `BatchedMesh` was running near
full in SoMa and silently dropping a different landmark on each reload, so a QA pass on
the old tree could have shown this building missing for an unrelated reason.

After the rebase the diff against `origin/main` is a pure append — 19 manifest lines,
40 registry lines, one README row — and **nothing under `app/public/tiles/` or
`api/_data/`**.

### Exclusion: `exclude: 10` m, proven from the tile

The window, measured against `excluded()`'s real test (ring CENTROID inside the circle
**or** any ring vertex inside it) from the shipping anchor, against all three bake
sources — including `pipeline/data/overture_buildings.geojsonseq`, which is what the
bake actually reads:

| Ring | centroid | nearest vertex |
|---|---|---|
| The hotel — OSM `193054134` | **2.29 m** | 15.01 m |
| The hotel — DataSF `201006.0001079` | **3.36 m** | 14.69 m |
| The hotel — Overture (h 27.4 m, area 2,133 m²) | **2.29 m** | 15.01 m |
| Muni vent pavilion — OSM `260290226` | 31.22 m | **21.07 m** |
| Muni vent pavilion — Overture (h 4.0 m) | 31.22 m | **21.07 m** |
| Audiffred Building | 60.48 m | 56.16 m |
| One Market Plaza | 90.09 m | 45.72 m |

Safe window **3.36 < r < 21.07 m**; `r = 10` sits with 6.6 m of margin below and 11.1 m
above. Overture carries exactly ONE ring for this building, so there is no second trace
to catch. The footprint half-diagonal is 39.35 m and would have deleted the Muni subway
vent shaft.

**Penetration depth, before and after** — not a boolean and not a changed-file count:

| | `origin/main` | re-baked |
|---|---|---|
| buildings in cell `23_10` | 49 | **48** |
| deepest penetration into the 64.08 × 42.07 m OBB | **+19.78 m** (top 27.5 m) | +14.70 m (top 8.9 m) |
| rings with a vertex inside the **real L footprint** | **1** | **0** |

The residual +14.70 m is the vent pavilion, which sits inside the OBB *rectangle* but
outside the L — the rectangle covers the notch at the north corner. A rectangle-only
test reads that as a permanent failure; the point-in-polygon test against the real
36-vertex footprint is the one that answers the question, and it goes 1 → 0. Exactly one
footprint was dropped and it is the right one.

### Verification

| Check | Result |
|---|---|
| `verify-rebake.mjs` | **PASS** — 584 of 585 cells unchanged; only `23_10` moved (49 → 48); nearest surviving footprint 21.4 m vs the 10 m radius |
| `audit.mjs` check 1.6 | **PASS** — 114 zones over 110 landmarks clear |
| `audit.mjs` overall | 29 passed, 3 failed, 1 info. The three (1.2b citywide p95 height, 1.3c Telegraph Hill Terrarium DEM, 1.7b one offshore tree) are pre-existing on `main` and unrelated |
| `context` validation | ok on all four checks; 174,682 / 174,682 buildings have a pick box and an identity |
| `npm run lint` | **PASS** |
| `npm test` | **PASS** — 26/26 |

### Local QA (Step 5)

Real headless Chrome over CDP against the Vite dev server; rAF measured at **30 frames
in 3 s**, so the app's own loop drove the pass rather than hand-pumping.

```
sf-assets: 8-mission merged 16 objects / 12 materials -> batched
           (11740 tris body); uniform x1.0000 at 3891, -2618
```

| Item | Result |
|---|---|
| Served manifest | 104 entries, `8-mission` present |
| Placed | yes — `SF.assets.placed.has('8Mission')` |
| **Scale factor** | **×1.0000** — the authored crest and `targetHeightM` agree exactly |
| Position | 3891, −2618, the anchor to the metre |
| Merge | 16 objects / 12 materials → one batched body + glow set |
| Single building | yes — no procedural twin, no baked block poking through, no z-fighting |
| Orientation | Mission arcade and turret face the real street corner |
| Terrain seating | sits on the ground, no float, no sink |
| Night glow | only the turret lantern, the canopy strip and scattered rooms |
| Streamer | `entries 104, live 84, loading 0, fading 0, failed 0` |
| **Draw calls** | **171** peak (hooked `renderer.render`, max over the app's own frames) against the 300 budget |

Screenshots: day at the landmark, day wide, night at the landmark.

### Fallback drill (Step 6)

GLB moved aside, page reloaded with a cache-buster:

- `failed: 1` — the loader genuinely reached for the file. (`failed: 0` would have been
  meaningless: it also describes a run where the camera never got near enough to try.)
- Exactly **one** console line:
  `sf-assets: 8-mission failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)`
  — Vite answers a missing `public/` path with the SPA shell at HTTP 200, so the failure
  is a parse error rather than a 404. That is a dev-server artifact, not a bug.
- `live: 83` (was 84): only this landmark dropped. App booted, city alive, every other
  landmark still placed.
- Case B, so the site is **empty ground** inside the exclusion zone rather than a
  procedural building. Expected and correct.
- GLB restored byte-identical; no `.drill-aside` left behind.

### Batch handoff

`BATCH: yes`, so the bake was run, QA'd on, and then thrown away
(`git checkout -- app/public/tiles api/_data`). The `pipeline/data` symlink into a
sibling worktree was deleted before committing. `compress-assets.mjs` was never run —
the stage-4 output already carries `EXT_meshopt_compression` — so the usual
`vehicles/passenger-airplane.glb` collateral does not appear.

Sanity check passes: `git diff --name-only origin/main` lists **nothing** under
`app/public/tiles/` or `api/_data/`.

The city gets rebuilt once for the whole batch by
`docs/asset-pipeline/BATCH-INTEGRATE.md`.

## Gate 3 — approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 18 August 2026, in the
> session's opening instruction alongside `BUILDING: 8 Mission St` and `BATCH: yes`.

Taken as standing approval for the human gate. Recorded verbatim as the pipeline
requires; the asset was still presented (contact sheet, aerial day and night, numbers)
before advancing.
