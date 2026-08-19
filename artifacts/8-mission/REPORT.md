# 8 Mission Street — build report

**Asset:** `artifacts/8-mission/8-mission.glb` — 1 Hotel San Francisco (Hotel Vitale),
8 Mission Street, San Francisco. Built from `docs/asset-plans/8-mission.md`
via `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, `BATCH: yes`.

## Shipped numbers (pre-optimize)

| | |
|---|---|
| Triangles | **19,082** (cap 26,000) |
| Mesh objects | 689 |
| Dimensions | 74.138 × 56.548 × **28.660** m |
| min Z / XY centre offset | 0.000 m / (0.000, 0.000) |
| Materials | 12, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow materials | `Toy_glass_Glow`, `Toy_glassl_Glow`, `Toy_gold_Glow` |
| File | 1,330,784 B raw / 242,232 B gzip (pre-meshopt) |
| Roof plateaus | 25.10 / 19.64 / 14.18 m; turret crown 28.66 m |
| **Manifest anchor** | **`-122.3932861, 37.7936872`** |
| Validation | `validation.json` — **overall PASS**, 17/17 checks |

Normals: 636/636 closed solids enclose positive signed volume; 206/206 open glow-strip
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

## Integration (stage 5, not done here)

Case B. Cell **`23_10`**. The bake currently puts a 64.4 × 41.8 m, **24.2 m** procedural
block on this exact footprint (`app/public/tiles/ctx/23_10.json`, pick id `103461`), so
the asset cannot be judged before the re-bake.

**`exclude: 10` m**, re-measured against the *shipping* anchor rather than the plan's
OBB centre:

| Ring | centroid distance | nearest vertex |
|---|---|---|
| The hotel, OSM `193054134` | **2.29 m** | 15.01 m |
| The hotel, DataSF `201006.0001079` | **3.36 m** | 14.69 m |
| Muni vent pavilion, OSM `260290226` | 31.22 m | **21.07 m** |
| Muni vent pavilion, DataSF `201006.0017562` | 31.89 m | 21.37 m |
| Audiffred Building, OSM `193054136` | 60.48 m | 56.16 m |

Safe window **3.36 < r < 21.07 m** against `excluded()`'s real test (ring centroid inside
the circle **or** any ring vertex inside it). `r = 10` sits with 6.6 m of margin below
and 11.1 m above. The footprint half-diagonal is 39.35 m and would delete the vent
pavilion. Re-verify both bounds against `pipeline/data/overture_buildings.geojsonseq`
before committing, and prove the result from penetration depth, not from a file count.

## Gate 3 — approval

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" — David, 18 August 2026, in the
> session's opening instruction alongside `BUILDING: 8 Mission St` and `BATCH: yes`.

Taken as standing approval for the human gate. Recorded verbatim as the pipeline
requires; the asset was still presented (contact sheet, aerial day and night, numbers)
before advancing.
