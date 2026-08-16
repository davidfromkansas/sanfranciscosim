# South Park (64 South Park) — build report

**What was built:** a validated miniature GLB of South Park, San Francisco's oldest
public park, at `artifacts/64-south-park/64-south-park.glb`. 11,500 triangles, 283,916
bytes meshopt-compressed, 13 palette materials, `max_z` exactly 15.00 m, all contract
checks PASS on the shipped file.

Plan: `docs/asset-plans/64-south-park.md`. As-built dossier: `REFERENCE.md`
(authoritative where it disagrees with the plan). Machine-readable checks:
`validation.json`.

## Shipped numbers

| | |
|---|---|
| Triangles | **11,500** / 12,000 cap |
| GLB on disk | **283,916 bytes** shipped, meshopt-compressed (609,080 B pre-optimize, −53.4%) |
| Oriented footprint | **159.463 × 23.507 m**, heading 45.4669° true |
| Axis-aligned bbox | **122.46 × 121.05 × 15.00 m** |
| Height datum | **15.00 m exactly** — tallest American elm crest, ESTIMATED |
| Anchor | −122.3939704, 37.7815903 (ground plate centre measured at u +0.012, v −0.000) |
| Objects / materials | 15 mesh objects shipped (20 as authored), 13 materials, 2 `_Glow` |
| Signed volumes | all positive |

Triangle split (as authored; the shipped file joins these per material except
`ground_plate` and `tree_crowns`, see `optimize/REPORT.md`):

| Object | Triangles |
|---|---|
| `tree_crowns` | 2584 |
| `shout_tubes` | 1152 |
| `seat_walls` | 1152 |
| `tree_trunks` | 952 |
| `path_tablets` | 864 |
| `furniture_wood` | 728 |
| `furniture_steel` | 644 |
| `kerb` | 564 |
| `ground_plate` | 560 |
| `beds` | 500 |
| `path_field` | 492 |
| `lawns` | 404 |
| `path_glow` | 360 |
| `lamp_heads` | 112 |
| `lamp_glow` | 112 |
| `play_mound` | 104 |
| `lamp_poles` | 80 |
| `play_surfacing` | 52 |
| `shout_nets` | 48 |
| `nest_swing` | 36 |
| **total** | **11,500** |

## Optimize pass (stage 4)

Run with `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` defaults for a landmark
(`ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`). **609,080 → 283,916 bytes (−53.4%)**, 20 → 15
primitives, triangles unchanged at 11,500, materials identical, ray flip fraction 0.0,
A/B pixel deltas ≤ 0.053% against gates of 2% / 4%. All of G1–G6 and G8 pass; the
shipped file re-passes the full stage-2 contract validator above. Two per-asset
adaptations — the limited dissolve is skipped (coplanar ring bands) and `ground_plate` /
`tree_crowns` are held out of the per-material join so the shipped file stays checkable
against the survey. Full metrics, census and gate evidence: `optimize/REPORT.md`.

## How to reproduce

```
python3 extract_park_uv.py                       # OSM survey -> data/park_uv.json
blender -b --python build_64_south_park.py       # -> .blend + .glb
blender -b --python render_64_south_park.py      # 7 day images
blender -b --python render_64_south_park.py -- --night
python3 make_contact_sheet.py
blender -b --python validate_64_south_park.py    # -> validation.json, exit 1 on failure

# stage 4, from optimize/:
blender -b --python optimize.py -- input/64-south-park.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 64-south-park.optimized.glb -c -km -kn -noq
blender -b --python validate.py -- input/64-south-park.glb 64-south-park.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../64-south-park.optimized.glb)
blender -b --python render_ab.py -- <glb> renders/<in|out>   ;  python3 diff_ab.py
```

Deterministic: no random numbers anywhere, variation is the pipeline's `hash01` mixer
seeded off feature indices.

## Iterations, and what each one was fixing

Every one of these was found by looking at the renders, and every one of them passed the
dimension checks while it was wrong. That is the point of reviewing the top view first.

1. **The promenade read as a black zebra.** The tablets were laid straight on the earth
   plate with a 0.4 m joint, and from above the joints read as black bars. Fixed by
   setting them into a continuous concrete field a half-tone darker than the tablets and
   dropping the relief to 30 mm, so the joints read as a fine comb rather than as shadow.
2. **The joints then fanned open on every bend.** Straight stadium chords cut
   perpendicular to a curving centreline diverge on the outside of a curve — at the plaza
   widths a 0.18 m joint opened to 0.84 m and the zebra came back as wedges. Fixed by
   cutting each tablet from the band itself between two arc-length stations, with a
   smoothed tangent, so the joint is constant everywhere. A polygon-area test then narrows
   any tablet that would still bow-tie.
3. **The beds read as a moat.** 790 m² of `Toy_teal` banding both long edges looked like
   water. Moved to `Toy_verdigris`.
4. **The crowns then read as turquoise pom-poms.** `Toy_teal` was tried on the canopy
   instead — style bible §27's "childishly toy-like". Crowns went back to `Toy_verdigris`,
   the same colour civic-center-plaza's bosques use, and `Toy_teal` ended up unused.
5. **Every tree was a cone.** The crest ring tapered to 0.42 of the upper radius on crowns
   that were 11 m tall and 6 m wide: 34 cypresses in a park of elms and pollards. Fixed by
   widening the crowns to roughly 1:1 and doming rather than tapering the top. Widening
   too far closes the canopy over the ground pattern, which on this asset is the subject —
   the shipped radii sit at the point where the canopy rings the park and the promenade
   still reads down the middle, which is also what the aerial shows.
6. **Black polygons all over the paving.** Every superstructure started at `Z_PLATE`,
   exactly coplanar with the ground plate's top face. Fixed with `Z_BASE = 0.26`, burying
   every bottom cap 80 mm inside the plate.
7. **Torn white sails along the seat walls.** `ribbon_poly` self-intersects wherever an
   OSM polyline turns tighter than the band is wide, and the bow-tied ring exports a
   downward-facing top. Both the walls and the promenade's field moved to one overlapping
   box per segment. Worth noting for the next asset: **the signed-volume test does not
   catch this** — a fold is volume-neutral — and neither does any dimension check. Only
   the top render does.
8. **The boxes then shadowed each other.** Overlapping boxes sharing an exactly coplanar
   top surface produce shadow acne, which Cycles renders as hard-edged dark polygons. Fixed
   by staggering the top face 4 mm per segment, and per stub, so no two agree.
9. **A white wedge shot out of the oval into Third Street.** Two entry stubs run to the
   narrow west tip; a 3 m band laid along them left the park. Fixed by clipping stub
   segments to the ring inset 2 m, and dropping the two `surface=asphalt` stubs entirely
   (they are street crossings, not park paths).
10. **The whole park sat 0.92 m off its anchor.** The build was re-centring the model on
    its own axis-aligned bounding box to satisfy the contract's "centred in x/y" rule, and
    because the canopy overhangs the kerb asymmetrically that slid everything sideways —
    the Shout came out at v −0.39 where the survey puts it at −1.29. The authored origin is
    already the park's OBB centre, which is what the manifest anchor means, so the
    normalization now touches Z only and the validator checks the **ground plate's**
    centre (measured: u +0.012, v −0.000) rather than the canopy-inflated box. AGENTS.md
    rule 5 is not negotiable for 0.92 m of convenience.
11. **The aerial cropped both ends off.** The camera distance was a multiple of the park's
    length rather than derived from the lens: a 78 mm lens at 252 m covers 116 m of a
    168 m park. The rig now solves for the distance that covers the subject, and the
    three-quarter aerial stands at azimuth 262° — 36° off the park's own axis — because
    standing at 225°, where the app's fly-to preset sits, foreshortens 160 m of park into a
    narrow vertical strip. That view is `-axis.png`.
12. **The top view was unreadable under the standard key.** A 52° key throws 10-sided
    crown shadows with straight edges across the paving, and in a nadir view those read as
    black polygons cut into the path. The top view now gets a near-overhead key and a
    lifted ambient; the rest of the rig is unchanged.

## Known and accepted

- **~130 near-black pixels remain** in the 2200 × 560 top render (0.02% of the park's
  area), residual hairline cracks between overlapping solids in the Cycles review rig.
  They are sub-pixel at the app's camera distance and the app's renderer — flat Lambert,
  no ray tracing — cannot produce them at all. Down from ~4,900 before item 8.
- **Area disagrees across sources**: 3,478 m² measured from the OSM polygon, ~34,000 sq ft
  (3,159 m²) per Rec & Park, 1.2 acres (4,856 m²) per Fletcher Studio, one acre per TCLF.
  Built on the OSM polygon, because that is the polygon the pipeline's landcover and
  exclusion already use, so the model and the baked city agree with each other even if
  both differ from the published figures. Fletcher's 1.2 acres almost certainly includes
  the street loop, which is out of scope.
- **The lawn and play mounding are estimated.** "Gently sloping meadows", "a grassy
  hillock toward the centre" and the mound that hides the Shout's six posts are documented
  in words and visible in photography, but no source gives grades.
- **The Shout's wave count is read from installation photography**, not from a spec. The
  manufacturer gives the envelope (perfect circle in plan, two tubes side by side,
  0.6 → 3.0 m, six posts below grade) and that is what carries the recognition.
- **`Toy_teal` is declared in the palette but unused** in the shipped build. Left in the
  build script's palette map with the note explaining both roles it was rejected from, so
  the next person does not re-run the experiment.

## Approval

**Gate 3 PASS — 2026-08-16.** Standing approval given by David at the start of the
session, verbatim:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Presented under it: the contact sheet, the day and night aerials and the top view, with
the numbers above. Recorded here rather than treated as silence, because the pipeline
requires an explicit approval and this is one — given in advance, for the whole run,
rather than per gate. It covers the asset gates only; it is **not** authority to push,
open a PR or deploy, which `ADDRESS-TO-ASSET.md` reserves for a separate instruction
(and which this session has not done).
