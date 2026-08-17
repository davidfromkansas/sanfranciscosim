# Hotel Madrid (22–24 South Park) — build report

Asset: `artifacts/22-south-park/22-south-park.glb`
Plan: `docs/asset-plans/22-south-park.md`
Dossier: `REFERENCE.md`
Built: 17 August 2026, Blender 5.2.0 LTS, headless.

**REPORT beats plan.** Where this file and the plan disagree, this file is what
shipped.

## Shipped numbers

| | |
|---|---|
| Triangles | **6,708** (cap 9,000) |
| Objects | 169 |
| Dimensions | 36.019 × 31.839 × **14.220** m |
| Footprint in plan | 445.2 m² (surveyed parcel 444.5 m²) |
| min Z | 0.000 m |
| XY centre offset | 0.000, 0.000 m |
| Materials | 11 — `Toy_glass`, `Toy_glassl_Glow`, `Toy_ink`, `Toy_mustard_Glow`, `Toy_navy`, `Toy_roofd`, `Toy_rust`, `Toy_sand`, `Toy_steel`, `Toy_stone`, `Toy_verdigris` |
| Glow groups | 2 (`Toy_glassl_Glow`, `Toy_mustard_Glow`) |
| GLB on disk | 480 KB uncompressed (pre-optimize) |
| `targetHeightM` | 14.22 — bbox top is the cornice crown, so the loader's scale is **1.0** |
| Manifest anchor | `-122.3936099, 37.7823247` |
| Validation | **PASS**, all 16 checks — `validation.json` |

The XY bounding box is 36.0 × 31.8 m for a building whose longest side is
36.28 m. That is the axis-aligned bound of a **trapezoid** standing at 45° to the
world axes, not a 36 m-square building.

## 1. The dossier was wrong about the footprint, and this is the correction

The plan as first written described the lot as a **36.28 × 13.68 m rectangle**
and gave four "corners" that were in fact the corners of its *oriented bounding
box*. Re-reading the surveyed parcel's own vertices before modelling showed
something else:

| edge | length | |
|---|---|---|
| East → South (South Park) | 14.99 m chord / **15.14 m arc** | curved |
| South → West | **30.13 m** | party wall with 26–28 |
| West → North (Taber Place) | **13.68 m** | rear |
| North → East | **36.28 m** | party wall with 10 South Park |

**The lot is a trapezoid.** The two party walls are parallel at 315.18° and the
Taber Place rear is square to them, but the South Park frontage is 24° off
square, because the oval turns 31° through this frontage. That is what makes one
party wall 6.15 m longer than the other — and it is a real, visible feature of
the building, not a survey artifact: the chord-quad area (454.2 m²) minus the
concave arc's 9.7 m² segment gives exactly the measured 444.5 m², and the
Assessor's `lot_area` matches the chord quad.

The four arc points in the model are **measured parcel vertices**, not
interpolation. Their outward normals came out at 169.7°, 163.6°, 157.7° and
147.9° — a 22° sweep across the frontage, tangent-continuous at the south-west
corner with 26–28 South Park's straight 135.2° front.

The plan's 2.3 has been rewritten to match.

## 2. Other corrections made during the build

**2.1 The LONG frame's cross-axis was inverted.** `PERP` was built as
`AXIS_BEARING + 90°`, but the frame's origin is the **East** corner, on the
north-east party wall, so `u` has to run south-west: `AXIS_BEARING − 90°`. The
first build put the entire PV array, the light well and the mechanical plant
outside the building, floating in space beside it. Caught on the first aerial
review, which is why that review comes before the formal rig.

**2.2 `inset_polygon()` resolved "inward" against the wrong centroid.** It used
the *building's* area centroid to decide which way to offset each edge. That is
correct for the parapet, whose polygon is the footprint — and silently shears any
smaller polygon that sits off to one side. The light-well curb came out inverted
and self-intersecting, and **every one of the 163 flipped rays in the normals
test landed on it** (residual 0.52% against a 0.15% allowance). Fixed to use the
polygon's own area centroid; residual then **0.0**.

**2.3 Coplanar faces.** Twenty-one proud bands, slabs and roof objects were
authored starting exactly on the surface they sit on. Coincident faces are what
the ray test counts as ambiguous, so every one now buries its inner face 3–4 cm.
(This turned out not to be the cause of the residual — 2.2 was — but it is the
right authoring either way and it is what the 106 South Park script does.)

**2.4 The light well is a pocket, not a shaft.** The permit record and the 72 m²
gap between the 372.3 m² building footprint and the 444.5 m² lot both confirm a
real light well, and the 9.31 m LiDAR minimum measures its floor 3 m below the
deck. It is modelled as a **dark recessed rectangle inside a raised curb** rather
than as a 3 m shaft: at the app's 30–50° camera a 1.8 m-wide slot is fully
self-occluding, so the shaft would be geometry nobody can ever see. The first
attempt put the dark floor *under* the roof membrane, where the membrane hid it
completely; it now sits on top.

**2.5 `Toy_roofd` was added to the palette.** The plan put the door onto the fire
escape in `Toy_ink`, the same value as the storefront bulkhead. At the app's
camera an ink door inside an ink-bulkheaded facade read as a hole punched in the
wall rather than as a doorway. `Toy_roofd` (`#45454a`) is a palette entry and one
step lighter.

**2.6 The taqueria glow shell was cut back twice.** The plan's hero glow is the
taqueria storefront in `Toy_mustard_Glow`. The repo's own experience (156 South
Park) is that a saturated warm glow over a whole opening reads as a brown panel
by day, because a closed `_Glow` shell is two 12%-alpha layers, not one. The
shell now covers a band from 1.05 to 1.80 m only — the lower third of the
glazing, which is also what a lit interior actually looks like from outside.

**2.7 Glow shells are closed, not open faces.** Same correction as its sibling at
26–28 South Park: the plan's "single open face" instruction is the right
observation about day alpha and the wrong conclusion, because an open plane has
no signed volume and fails the normals contract. All shells are thin closed
solids covering the lower 55% of their opening. The plan text has been corrected.

## 3. What stayed inferred

- **Front cladding.** The Taber Place rear is unambiguously lap siding; the front
  reads smooth with faint horizontal banding. Modelled as siding throughout, with
  the groove pattern shown only on the rear (where it is legible) and omitted on
  the front (where it would be noise at the app's camera).
- **The PV array's attribution to this roof.** Read from a pin-centred z21
  near-nadir crop. The 2010 LiDAR that gives the heights predates the array and
  cannot corroborate it; the 2019–21 $2.1 M rehabilitation and the arrays on the
  other rehabilitated SRO roofs on this block are the supporting argument.
- **The 14.22 m crest as cornice rather than street tree.** See REFERENCE.md §6.
  The risk is contained: the model is authored with the crown at exactly 14.22 m,
  so the loader's scale is 1.0 and an error makes the cornice deeper, not the
  building taller.

## 4. Deviations from the technical contract

**"Front faces −Y" is not honoured.** The building is authored at its real-world
heading; its street elevation faces 147.9°–169.7° across the arc. AGENTS rule 5
wins over the contract's default, exactly as in every other South Park asset. The
loader applies no rotation.

No other deviations. No textures, no transparency, no `Toy_body`, no cameras,
lights, animations, armatures or constraints; transforms applied; no negative
scales; normals outward by per-object signed volume with a 0.0% ray residual.

## 5. Scope — what is deliberately not in the GLB

South Park and its trees, Taber Place, the sidewalk, street trees, the utility
pole and overhead wires, the neighbours at 10 or 26–28 South Park, vehicles,
motorcycles, people, plinths, cameras and lights.

Also omitted, and each real: **all tenant signage** — the "MEXICAN GRILL •
TAQUERIA • BURRITOS • TACOS" transom lettering, the "TCP TOUCHSTONE FOR LEASE"
banner and the "24" address numeral, all present in the January 2025 capture and
all shorter-lived than this model; the wall-mounted security camera and lantern
on Taber Place; the fire escape's drop ladder and individual balusters; and the
1985 solar hot-water collectors, superseded by the modern PV array.

## 6. Review iterations

| # | What was seen | What changed |
|---|---|---|
| 1 | The PV array, light well and plant floating outside the building | `PERP` axis sign (2.1) |
| 2 | The light well read as a hollow green frame — its dark floor was under the membrane; facade camera cropped | well floor moved on top of the slab (2.4); facade camera pulled back |
| 3 | PV bands running to the parapet edge; the fire-escape door reading as a hole | PV inset to 4.4–11.85 m across; `Toy_roofd` door, deeper landings (2.5) |
| 4 | Validation FAIL: normals ray residual 0.52%, all on `well_curb` | `inset_polygon` centroid fix (2.2) — residual 0.0, validation PASS |

Reviewed from the high three-quarter aerial first at every iteration, per the
plan's Part 1; the formal rig was run only after the aerial read correctly.

## 7. Draft manifest entry

```json
{
  "id": "22-south-park",
  "file": "22-south-park.glb",
  "anchor": [
    -122.3936099,
    37.7823247
  ],
  "targetHeightM": 14.22,
  "cat": 7,
  "name": "Hotel Madrid (22–24 South Park)",
  "estimated": false,
  "dims": [
    36.019,
    31.839,
    14.22
  ],
  "tris": 6708,
  "loadRadius": 2500
}
```

**The registry entry is NOT this anchor.** `pipeline/lib/landmarks.mjs` takes
`lon: -122.3936498`, `lat: 37.7822952` — the parcel's **area centroid**, which is
where the exclusion band in the plan's 2.13 was measured from. The manifest
anchor is the model's bbox centre, 4.8 m away, because a trapezoid's bbox centre
is not its area centroid. Registry `height: 14.22`, **`exclude: 4.5`** (band
(2.21, 6.90) m, measured against both bake inputs).

## 8. Approval

Stage 3 approval, quoted verbatim from the session that commissioned this asset
(16 August 2026):

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

Recorded as a standing pre-approval covering stages 3 through 5 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` for this building. No per-iteration
approval was sought; the review iterations in §6 were self-directed against the
style bible.
