# The Audiffred Building — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed against
`docs/asset-plans/audiffred-building.md`. **This report and `REFERENCE.md` beat
the plan** wherever they disagree; the disagreements are listed in §1–§4 below.

| | |
|---|---|
| Asset | `artifacts/audiffred-building/audiffred-building.glb` |
| Triangles | **9,256** (cap 12,000) |
| Objects | 228 |
| Dimensions | 40.42 x 40.28 x **17.500 m** (axis-aligned; the building is 41.82 x 14.00 m at a 45.2° heading) |
| min Z / XY centre | 0.000 m / (0.000, 0.000) |
| Materials | 12, all `Toy_*`, flat, no textures, no alpha |
| Glow | `Toy_gold_Glow` (entablature sign band), `Toy_glassl_Glow` (scattered lit windows) — 40 single-sided faces, 40 outward |
| File | 588,384 bytes raw / 88,207 gzip (pre-optimize) |
| Validation | **PASS**, 17 of 17 checks, normals ray residual **0 of 31,500** |
| Manifest anchor | **−122.3927766, 37.7933230** |

---

## Corrections to the plan

### 1. `hgt_maxcm` 19.18 m rejected; the crest is 17.50 m

The plan flagged this as its weakest number and asked for it to be re-derived.
It was, and the plan's 17.5 m stands. The evidence:

| Source | Value | Reading |
|---|---|---|
| DataSF LiDAR `hgt_majority` / `hgt_median` | 15.44 / 15.36 m | the flat roof deck — **measured**, 2,238 cells |
| Overture ring "The Audiffred Building" | **17.4 m** | independent |
| Photogrammetry on the corner elevation | 17.4–18.1 m | vault crown above the crown moulding, deprojected for a 1.5–2.5 m setback |
| DataSF LiDAR `hgt_max` | 19.18 m | **rejected** |

`hgt_max` is 1.64 σ above the median on a 2.33 σ distribution — inside spike
range, not outside it — and the reference corner photograph shows a large dark
mechanical unit and a tank standing on the deck, which is exactly what a LiDAR
maximum finds. **This is the opposite call from 501 Second Street**, where the
equivalent figure was real: there the standard deviation was 6.41 m over 12,467
cells with a distinct raised block on the aerial. The rooftop plant is modelled
honestly here, capped at 1.70 m above the deck, i.e. 17.10 m — under the crest,
as the contract requires.

### 2. `Toy_glass_Glow #6f95b8` is a name/hex contradiction; the hex wins

The plan's palette asked for `Toy_glass_Glow` with hex `#6f95b8`. Those are two
different materials: `Toy_glass` is `2a4d73` and `Toy_glassl` is `6f95b8`. The
app draws `_Glow` in a separate **unlit** layer, so at night the surface shows
its raw base colour — `2a4d73` is the dark navy of *unlit* glass and would render
a lit window that looks switched off. Shipped as **`Toy_glassl_Glow` (6f95b8)**,
which is also what `49-south-park` settled on for the same reason.

### 3. Thirteen Mission bays kept, and it remains the weakest inference

Re-counted on the two Commons photographs. The three-bay ends are confident (and
the NRHP's double-width corner windows explain their coarser 4.67 m pitch against
Mission's 3.22 m). Thirteen on Mission is still a count off a foreshortened
photograph partly occluded by street trees, and it is still the most likely place
for this model to be visibly wrong. It is also the biggest single line in the
triangle budget: nineteen dormers and nineteen arched openings.

### 4. Two additions the plan did not call for

- **A brick firewall along the party edge of the deck** (0.75 m thick, 0.62 m
  above the membrane). True of the real building, and without it 586 m² of pale
  membrane read as an open tray with one green ribbon dropped into it.
- **A brick facing on the party wall's ground floor.** The cream shopfront prism
  is closed, so it painted cast iron onto a common wall. There was never any.

---

## Iteration log

Reviewed from the high three-quarter aerial first, as the pipeline requires, then
from the formal rig. Six passes:

1. **First build (11,960 tris).** Three bands read; four faults. The brick-storey
   window "surrounds" were *filled* arch plates, so every opening rendered as a
   solid cream arch with the glass hidden behind it. The entablature was 0.40 m
   deep and vanished at distance. The chimneys, placed 0.85 m inside the wall,
   emerged from the mansard as little triangles instead of crossing it. And the
   bevel rounded 5 mm off the vault ridge, so the bbox top came in at 17.495 m.
2. **Rings, deeper entablature, chimneys out to 0.30 m, vault left unbevelled
   (14,532 tris — over budget).** The ring construction cost 3,268 triangles,
   almost all of it bevel: 7,618 for nineteen windows, more than half the model.
   Left them sharp — 401 → 108 triangles each, for an arris invisible at 3.2 m of
   bay — and the budget came back to 9,136.
3. **Everything on the roof was a diamond.** Quoins, chimneys, plant and hatch
   were built as world-axis-aligned boxes on a building set at 45.2°, so from
   directly above they sat at 45° to the walls under them, and a quoin threw a
   0.57 m diagonal spur off the end elevation. All rebuilt in Face frames. The
   quoins became two proud strips per corner, which is what a quoin actually is.
4. **The vault was a sausage.** A full semicircle springing off the deck, 4.2 m
   wide out of a 10.8 m deck. Reduced to a 3.1 m segmental arc on a 0.55 m curb,
   moved out to hug the mansard crest, and given an EVEN segment count so a ring
   point lands exactly on the crown (an odd count left the bbox 23 mm short).
5. **228 degenerate triangles, one duplicate vertex per opening.**
   `arch_outline()` listed the springing points explicitly *and* generated them
   again as the arc's own endpoints, so every opening carried a zero-area quad on
   each of its four strips. Also removed a coincident pair of 585 m² horizontal
   caps where the mansard's base met the brick body's top.
6. **Every glow strip on three of the four elevations faced inward.** The loop
   `t0 → t1 → t1 → t0` has the normal `t × z`, which is *minus* the outward
   normal on a right-handed face and *plus* it on a left-handed one — and
   `Face.__init__` negates the normal on exactly the elevations that need it, so
   Steuart Street has the opposite handedness to the other three. 475 of 31,500
   validator rays, 1.5% against a 0.15% tolerance, and by day the app would have
   drawn each glow shell on the wrong side of the wall it lights. Fixed by
   reversing the winding on `face.hand > 0`. Residual went to **0**.

## What the asset is

| Band | Height | Material | Detail |
|---|---|---|---|
| Cast-iron shopfront | 0 → 5.35 m | `Toy_cream` piers, `Toy_ink` glazing and awnings | 19 bays over three public elevations |
| Entablature | 5.35 → 6.15 m | `Toy_trim`, projecting 0.45 m | + the 1924 nautical frieze as one recessed strip, **eastern half of Mission and the Embarcadero end only** |
| Brick storey | 6.15 → 10.55 m | `Toy_brick` with `Toy_trim` quoins | 19 arched `Toy_glass` openings in white rings |
| Corbel table | 10.55 → 10.95 m | `Toy_trim`, projecting 0.35 m | the second white line |
| Mansard | 10.95 → 15.40 m | `Toy_navy`, leaning in 1.60 m | **three exposed faces only**; 19 dormers with `Toy_trim` pediments and `Toy_glassl` sashes; 7 `Toy_brick` chimneys |
| Party wall | 0 → 15.40 m | `Toy_brick` | blind, plus a 0.62 m firewall above the deck |
| Crown moulding | 15.10 → 15.55 m | `Toy_trim` | three sides |
| Deck | 15.40 m | `Toy_sand` | 4 `Toy_steel` plant blocks + hatch, grouped against the party wall |
| Barrel vault | 15.40 → **17.50 m** | `Toy_verdigris` | 3.1 m wide on a 0.55 m curb, mitred around both end corners |

**`Toy_roofd` appears nowhere in this asset**, deliberately: it measured
rgb(9, 9, 12) on a roof deck in the live scene, and the mansard is the largest
and most identifying surface here. `Toy_navy` is also what the NRHP's "hand-cut
blue-grey slate" reads as in daylight.

## Validation

`validate_audiffred_building.py` factory-resets Blender, imports only the shipped
GLB, and reports on the re-import. All 17 checks PASS:

```
meters_and_plausible_dimensions        crest_normalized_to_target
base_at_z_zero                         centered_xy
under_triangle_budget                  no_image_textures
no_transparency                        materials_follow_contract
no_cameras_or_lights                   no_animation_skin_or_constraints
transforms_applied                     no_negative_scales
normals_outward_signed_volume          glow_strips_face_outward
normals_outward_ray_residual_within_tolerance
no_degenerate_geometry                 no_unexpected_objects
```

Normals: 225 closed shells all enclose positive signed volume (authoritative for
a union of interpenetrating solids); 40 open glow strips all face outward; **0 of
31,500 visibility rays** hit a back face first.

**The axis-aligned bounding box is 40.42 x 40.28 m — nearly square — for a
41.82 x 14.00 m building.** That is the 45.2° heading, not a scale error. The
validator's dimension gate is written around it deliberately, and a reviewer
should check the footprint along the building's own axes before concluding
anything is wrong.

## Draft manifest entry

```json
{
  "id": "audiffred-building",
  "file": "audiffred-building.glb",
  "anchor": [
    -122.3927766,
    37.7933230
  ],
  "targetHeightM": 17.5,
  "cat": 3,
  "name": "Audiffred Building (1 Mission Street)",
  "estimated": true,
  "dims": [
    40.4244,
    40.2848,
    17.5
  ],
  "tris": 9256,
  "loadRadius": 2500
}
```

The anchor is the design anchor `−122.3927748, 37.7933216` (the OSM OBB centre)
moved by the model's recentring shift of −0.159 m east / +0.160 m north, because
the entablature and corbel table project on three sides and not on the fourth.
`"estimated": true` because the 17.5 m crest the model is normalized to is an
Overture figure corroborated photogrammetrically, not a LiDAR measurement.

`dims` and `tris` will be re-measured after stage 4 (optimize) and updated here.

## Approval

*Pending — stage 3 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.*
