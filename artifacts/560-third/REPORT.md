# 560 Third Street — build report

**Status:** built and validated (all-PASS), pre-approval.
Plan: [`docs/asset-plans/560-third.md`](../../docs/asset-plans/560-third.md).
Dossier: [`REFERENCE.md`](./REFERENCE.md). Machine report:
[`validation.json`](./validation.json).

## Numbers

| | |
|---|---|
| Triangles | **2,356** (cap 8,000) |
| Objects | 33 mesh objects |
| Dimensions | 23.90 × 24.06 × **7.20** m (the XY box is the 44°-rotated footprint's AABB) |
| min Z | 0.0000 |
| XY centre offset | (−0.151, −0.081) m |
| Materials | 8 — `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_glass`, `Toy_glassl`, `Toy_mustard_Glow`, `Toy_glassl_Glow` |
| Glow groups | 2 — the upper window band (+ a door cue), and the two roof skylights |
| Anchor | −122.3951188, 37.7804142 |
| Front heading | outward normal 44.1° true; long axis 43.9° |
| Textures / transparency / cameras / lights / animation | none |
| Files | `560-third.glb`, `560-third.blend`, `build_560_third.py`, `render_560_third.py`, `validate_560_third.py`, `make_contact_sheet.py`, 8 renders |

## Gate 2 — validation

`validate_560_third.py` factory-resets Blender, imports **only the exported
GLB**, and judges the re-import. `overall: PASS`, every check true:

meters_and_plausible_dimensions · crest_normalized_to_target · base_at_z_zero ·
centered_xy · under_triangle_budget · no_image_textures · no_transparency ·
materials_follow_contract · no_cameras_or_lights ·
no_animation_skin_or_constraints · transforms_applied · no_negative_scales ·
normals_outward_signed_volume · normals_outward_ray_residual_within_tolerance ·
no_degenerate_geometry · no_unexpected_objects

Normals were checked both ways: per-object signed volume (authoritative for this
union of closed solids) — every object outward — and the deterministic
visibility-ray test, residual 0.

The bbox top is exactly **7.200 m**, so the loader's `targetHeightM /
measuredHeight` scale lands on 1.0.

## Corrections and decisions made during the build

**REPORT beats plan.** These supersede `docs/asset-plans/560-third.md` where they
differ.

1. **The hero glow is `Toy_mustard_Glow` (#d9a441), not `Toy_glass_Glow`.** The
   plan's §2.8 specified a blue glow on the window band. The February 2017 dusk
   reference is unambiguously *warm* — one amber rectangle in a black facade —
   and a blue glow would have thrown away the single strongest night cue this
   building has. The skylights keep `Toy_glassl_Glow` (#6f95b8), so the night
   composition is a warm street band against two cool roof rectangles.
2. **Nothing on the roof exceeds the parapet.** The first build put the
   mechanical units 0.82 m above the membrane, pushing the bbox to 7.60 m and
   breaking the scale-1.0 rule. The units now top out exactly at 7.20 m and the
   skylight assemblies were lowered to match. This is also the honest reading:
   the LiDAR shows no rooftop object (the 11.43 m maximum is bleed from 574's
   party wall — see REFERENCE §4).
3. **The night-glow shell is deliberately smaller than the glazing.**
   `assets.js` renders `_Glow` surfaces in a separate layer at ~12% alpha by DAY.
   A full-pane shell washed the daytime glazing from navy to grey in the first
   aerial review, so the shell was shrunk to ~55% of the pane area. Day reads
   blue; night still reads as a full lantern.
4. **Two shopfront mullions were added** (not in the plan's §2.7). Without them
   the ground floor read as a hole punched in the wall rather than a storefront.
5. **`Toy_ink` is used as a wall colour**, which no other building in the Third
   Street set does. It is the point of the asset: against 550's cream and 574's
   brown, this building has to read as the dark gap before any detail resolves.
   `Toy_roofd` (#45454a) carries the frames, mullions, head band and base rail —
   one step lighter, so the facade has internal structure without losing its
   value. The steel coping is the one bright line, and it is what draws the roof
   plane from above.
6. **`render_560_third.py` re-seeds the emission colour on re-import.** The glTF
   round-trip exports with emission strength 0, so `emissiveFactor` is black and
   the importer leaves the emission socket white; driving strength alone rendered
   every glow pure white. The night preview now copies each material's base
   colour into its emission colour first. This is a review-rig fix only — the
   shipped GLB is unchanged, and the app drives glow from material names.
7. The aerial camera was refit (78 mm at 3.6× span, 36° down) after the first
   review render cropped the building.

## What the asset is

A single near-black box on the traced footprint, 7.20 m to a flat parapet with a
steel coping. One designed elevation on 3rd Street: dark glazed shopfront with
the entry door at the 574 end, a head band, and above it a four-pane glazed band
filling most of a 9.4 m frontage. Three blind party walls, because all three are
buried behind neighbours 4 m taller. A pale membrane roof — over 90% of what the
app ever shows of this building — with two skylights, a two-unit mechanical
cluster on a curb, a duct, two vents and a hatch in the rear third.

Judge it from the top-down and high-aerial cameras, and judge it **next to**
`artifacts/550-third/` and `artifacts/574-third/`. Alone it is an unremarkable
dark box, because alone it is one; its whole job is the contrast with what stands
on either side.

## Draft manifest entry

Not applied — integration is a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md`).

```json
{
  "id": "560-third",
  "file": "560-third.glb",
  "anchor": [-122.3951188, 37.7804142],
  "targetHeightM": 7.2,
  "cat": 3,
  "name": "560 Third Street",
  "estimated": false,
  "dims": [23.9, 24.06, 7.2],
  "tris": 2356,
  "loadRadius": 2500
}
```

## Open risks carried forward

- The **parapet crest is derived**, not measured (roof plane 6.66 m + 0.55 m).
- The **roof rectangles are inferred** as skylights.
- The **facade imagery is 2016–17**; nothing proves the paint is still charcoal.
- Integration (Case B) needs an exclusion radius **measured from this anchor
  against the real bake input**, not from the OSM polygon. The two known
  distances into this lot — 11.17 m from 550's anchor, 16.35 m from 574's — say
  the safe band is small and in the same 8–10 m family as its neighbours. See
  `docs/asset-plans/560-third.md` §2.13.

## Reproduce

```bash
blender -b --python build_560_third.py
blender -b --python render_560_third.py
blender -b --python render_560_third.py -- --night
python3 make_contact_sheet.py
blender -b --python validate_560_third.py
```
