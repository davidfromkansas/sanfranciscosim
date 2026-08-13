# 155 – 157 South Park Street — build report

Miniature GLB for SF-SIM, built 12–13 August 2026 from
`docs/asset-plans/155-south-park.md` via the address-to-asset pipeline
(`docs/asset-pipeline/ADDRESS-TO-ASSET.md`).

**This report beats the plan.** Where the dossier in the plan file and this report
disagree, this report and `REFERENCE.md` are correct.

## 1. Headline numbers

| | As built |
|---|---|
| Triangles | 4,048 (cap 7,000) |
| Objects | 63 |
| Dimensions (AABB) | 25.5223 x 28.2942 x 10.10 m |
| Min Z | 0.0 |
| XY centre offset | (0.230, 0.537) m |
| Materials | 13, all `Toy_*`, flat, opaque |
| Glow materials | `Toy_gold_Glow`, `Toy_glass_Glow` |
| File, raw | 243,456 B |
| Contract validation | **PASS on all 16 checks** |
| Anchor | `-122.3942202, 37.7808993` |
| Target height | 10.1 m (bbox top normalized exactly, so loader scale = 1.0) |
| Front heading | 327.2° true (NNW), authored in true-world orientation |

The AABB is ~25.5 x 28.3 m for an 8.2 x 31.2 m building. That is the expected
consequence of authoring at the real 41.4° SoMa heading, not a scale error.

Normal orientation: 63 of 63 objects enclose positive signed volume, and 0 of
31,500 deterministic visibility rays hit an inward-facing first surface (residual
0.000%, tolerance 0.15%).

## 2. Dossier corrections and decisions made during the build

1. **Three levels, not two.** The SF Assessor roll records 2 storeys and 2 units.
   Every photograph shows three levels. The 2009 DPR form settles it: the
   ground-floor garage was converted to commercial space while the upper floors
   stayed residential, so the assessor is counting dwelling floors. Built as three,
   with the ground floor (3.80 m) clearly taller than the two above it (2.35 m and
   2.15 m of window band).

2. **OSM `height = 9` and the LiDAR median 8.87 m are the roof deck, not the
   crest**, and their near-agreement is a coincidence that makes both look
   trustworthy. The LiDAR *modal* cell — 9.25 m — is the better deck figure, and the
   parapet stands above it. Target height 10.1 m. This is the same trap the plans
   README documents for 543 Presidio Blvd.

3. **The LiDAR max of 16.23 m is the South Park street tree**, not the building.
   Using it would have produced a building 60% too tall.

4. **The assessor's 2,350 sq ft floor area was discarded**, not used to derive floor
   heights or a storey count: 218 m2 against a 209 m2 through-lot footprint is less
   than one full floor and cannot describe a three-level front block. It describes
   the flats only — the same signal as the business registration's "155 South Park
   St **Bldg A**".

5. **The two survey light-well notches were dropped.** The DataSF ring has a
   1.8 x 0.85 m notch in the north-east party wall and a 1.55 m notch in the
   south-west one. Both are invisible between party walls, and both would have
   broken the convex-polygon assumption in `offset_polygon` that the parapet rings
   rely on. The rest of the survey — including the skewed street edge — is built
   exactly.

6. **`Toy_peach` (`#dcb6a0`) is a deliberate palette extension** for the rear block,
   documented here as a WARN, exactly as 380 Brannan's `Toy_slate` was. The real
   rear is a warm salmon: `Toy_sand` (`#ece4d4`) is too pale to separate from the
   white front block, and `Toy_coral` (`#e8735a`) is far too saturated for a whole
   wall. The first render used `#e0a98c` and it fought the timber roof deck for
   attention, so it was softened one step toward the style bible's neutral
   architecture.

## 3. Review iterations

Each round was judged from the high three-quarter aerial first, per stage 2 of the
pipeline document.

**Round 1.** Four problems.
- The aerial rig inherited from 380 Brannan frames a near-square object; a 105 mm
  lens at 2.45x span covers ~13 m of subject, so a 31 m lot rendered as a plan view
  with the one designed elevation cropped out of frame. Moved to 4.3x span, pitch
  25°, azimuth 337° (10° off square so a flank reads too), and the studio floor
  enlarged to match the new camera distance.
- The rear timber roof deck was the largest and most saturated element in the whole
  model, which is backwards for a private deck on the service end of the lot.
  Halved and pushed to the Varney end.
- The screen walls enclosed the entire rear roof like a tray rail. Shrunk to the
  deck they actually screen and thickened to 0.30 m so they read as walls.
- The front roof was an empty dark tray. Added the stair skylight a 1925 flats
  building actually had and spread the furniture.

**Round 2.** Two problems.
- The recessed entrance was invisible: the ink frame panel covered the full opening
  at `SKIN + 0.06` while the door sat at `SKIN − 0.04`, so the frame occluded it.
  Rebuilt with the same frame / proud-fill idiom every other opening uses.
- The residential security gate was rendered in `Toy_steel` and read as a bright
  grey stripe that pulled the eye off the café. It is black wrought iron in every
  photograph; changed to `Toy_roofd`.

**Round 3.** One problem. The brass entrance doors in `Toy_gold` were a saturated
yellow slab and became the loudest thing on the building. The real doors are pale
curtained glass with brass hardware, so the leaves moved to `Toy_trim` and gold is
now spent only on the slim centre mullion and the awning fascia line.

**Round 4 — night pass.** The first night render came back with every glow surface
pure white. This is the failure the asset-plans README documents: glTF writes
`emissiveFactor = 0` when the authored emission strength is 0, so a re-imported
`_Glow` material carries a default **white** emission and raising the strength
alone renders white slabs. Fixed in `render_155_south_park.py` by copying Base
Color into Emission Color before raising the strength, and the strength dropped
from 6.0 to 4.0.

## 4. Night state

Hero glow: the café shopfront — the two display windows and the entrance transom in
`Toy_gold_Glow`, reading as the one lit thing on a dark residential street.
Supporting accent: the second-floor flat in `Toy_glass_Glow`, cool; the third floor
stays dark, so the two lit floors do not read as an office block. The rear service
block does not glow at all.

All glow surfaces are thin shells standing proud of the opaque glazing behind them
(`SKIN + 0.10` to `SKIN + 0.17`), never a primary surface, because the app renders
`_Glow` in a separate layer at ~12% alpha by day. The day renders preview that
correctly via `fade_glow()`.

## 5. Deliverables

| File | What it is |
|---|---|
| `build_155_south_park.py` | deterministic Blender 5.2 build, world-space metres, true-world heading |
| `155-south-park.blend` | authoring scene |
| `155-south-park.glb` | the shipping asset |
| `render_155_south_park.py` | controlled review rig; always re-imports the exported GLB |
| `make_contact_sheet.py` | contact sheet assembly |
| `validate_155_south_park.py` | fresh-scene contract validation |
| `validation.json` | machine-readable validation result, all 16 checks PASS |
| `155-south-park-{north,east,south,west}.png` | four elevations, one rig, identical everything but azimuth |
| `155-south-park-top.png` | both roofs, the step, the deck and the screen |
| `155-south-park-aerial.png` | beauty render from the app's camera band |
| `155-south-park-aerial-night.png` | night state |
| `155-south-park-contact-sheet.png` | all seven views |

## 6. Manifest entry

```json
{
  "id": "155-south-park",
  "file": "155-south-park.glb",
  "anchor": [
    -122.3942202,
    37.7808993
  ],
  "targetHeightM": 10.1,
  "cat": 1,
  "name": "155 South Park",
  "estimated": false,
  "dims": [
    25.5223,
    28.2942,
    10.1
  ],
  "tris": 4048,
  "loadRadius": 2500
}
```

## 7. Approval (gate 3)

Approved by David on 13 August 2026, verbatim:

> "continue going -- dont ask me for permission its all good! use your judgement
> and continue proceeding till the end"

That is a blanket authorisation for the remainder of the pipeline given after the
stage 0/1 gate report, not a review of these specific renders. Recorded here as the
gate-3 approval so the provenance is honest: **no one has looked at these images
but the authoring agent.** If the building is later judged wrong, this is the gate
that was taken on trust.
