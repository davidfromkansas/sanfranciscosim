# 188 South Park — build report

## Summary

Built a stylized miniature GLB of 188 South Park (South Park Lofts), a 2002
four-storey live/work loft building by Santos-Prescott on the north rim of the
South Park oval. The asset passes all 14 contract checks: 3,864 triangles
(budget 9,000), 276 KB on disk, crest at exactly 15.93 m, origin at base-center,
all `Toy_*` materials, no textures/cameras/lights/animation.

## Numbers

| Metric | Value |
|---|---|
| Triangles | 3,864 |
| Objects | 129 |
| Dimensions (axis-aligned bbox) | 28.57 x 28.61 x 15.93 m |
| Footprint (OBB) | 23.7 x 16.1 m at bearing 45°/225° |
| Min Z | 0.0 m |
| XY center offset | (0.0, 0.0) |
| Materials | 9 (Toy_sand, Toy_stone, Toy_trim, Toy_glass, Toy_roofd, Toy_steel, Toy_ink, Toy_glass_Glow, Toy_trim_Glow) |
| Glow groups | 2 (Toy_glass_Glow, Toy_trim_Glow) |
| GLB file size | 119 KB (optimized, was 276 KB pre-optimization) |
| Validation | ALL PASS |

## Dossier corrections

### 1. Anchor: DataSF area centroid, not OSM OBB center

The plan's 2.13 already specified the DataSF LiDAR footprint area centroid as
the anchor, and the build followed it. The OSM OBB center was considered and
rejected: it sits 3.19 m from the DataSF centroid, which narrows the exclusion
window. The DataSF centroid coincides with the bake input's own ring centroid
(distance ~0 m) while maximising the distance to the nearest neighbour vertex
(12.95 m vs 12.02 m from the OSM center). This is the same choice made for
165-167 South Park.

### 2. Height: 15.93 m confirmed from LiDAR

The LiDAR `hgt_maxcm = 1593` (15.93 m) is the architectural crest — the
penthouse/roof terrace parapet. The median of 13.34 m is the main flat roof.
The build normalizes the bbox top to exactly 15.93 m so the loader's
`targetHeightM / measuredHeight` scale lands at 1.0.

### 3. Storeys: 4 + penthouse, not 5

The 2018 kitchen remodel permit says `number_of_proposed_stories = 5`, but the
1998 new-construction permit and every other permit say 4. The LiDAR height
distribution (max 15.93 m, median 13.34 m) is consistent with a 4-storey
building with a ~2.6 m penthouse, not a 5-storey building. The build treats
the building as 4 storeys with a penthouse. **Source:** SF Building Permit
9823199S (1998, "four story") vs 201807174708 (2018, "5 storeys" — likely a
clerical error or penthouse mezzanine regularisation).

### 4. Facade material: inferred, not observed

No street-level photography was available. The palette (`Toy_sand` for upper
walls, `Toy_stone` for the ground-floor base) is inferred from the Compass
listing's "Construction Materials: Stone, Stucco" and the architect's known
work. This is documented prominently in REFERENCE.md and must be confirmed
from photography in a future revision.

### 5. Window rhythm: 4 bays inferred

The 4-bay reading on the 23.7 m flanks comes from dividing the width by a
plausible loft bay width (~5.9 m centres). The real count and grouping must be
observed from photography.

### 6. Penthouse position: inferred from listing

The penthouse is placed on the SE third of the roof (overlooking South Park)
based on the Curbed article's "private rooftop terrace" on penthouse unit #11.
Aerial imagery was not detailed enough to confirm the exact position.

## Night state

Glow surfaces are thin shells proud of the opaque glazing:
- **Hero glow:** 5 lit windows on the SW flank (facing the park oval) across
  three floors
- **Supporting accent:** 2 lit windows on the SE (park) front, plus the
  storefront spill
- The NW (patio/service) end stays dark
- The roof and penthouse do not glow

The night render previews the app's dusk pass by driving emission from Base
Color at strength 1.0 (the app's night layer is an unlit overlay drawn at the
material's own baked colour).

## Validation results

All 14 checks PASS:
- meters_and_plausible_dimensions: PASS (28.6 x 28.6 x 15.93 m)
- crest_normalized_to_target: PASS (15.93 m exactly)
- base_at_z_zero: PASS (0.0 m)
- centered_xy: PASS (0.0, 0.0)
- under_triangle_budget: PASS (3,864 ≤ 9,000)
- no_image_textures: PASS
- no_transparency: PASS
- materials_follow_contract: PASS (all Toy_*, no Toy_body)
- no_cameras_or_lights: PASS
- no_animation_skin_or_constraints: PASS
- transforms_applied: PASS
- no_negative_scales: PASS
- normals_outward_signed_volume: PASS (129/129 objects)
- normals_outward_ray_residual_within_tolerance: PASS
- no_degenerate_geometry: PASS
- no_unexpected_objects: PASS

## Manifest draft

```json
{
  "id": "188-south-park",
  "file": "188-south-park.glb",
  "anchor": [-122.3950794, 37.7810118],
  "targetHeightM": 15.93,
  "cat": 2,
  "name": "188 South Park",
  "estimated": false,
  "dims": [28.57, 28.61, 15.93],
  "tris": 3864,
  "loadRadius": 2500,
  "optimizedBytes": 119312
}
```

## Stage 3 approval

User pre-approved all stages: "I approve everything -- go ahead and do your
thing. you dont need to ask for stage 3 approval. proceed w everything" —
14 August 2026.
