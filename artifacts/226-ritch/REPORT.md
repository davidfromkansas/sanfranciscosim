# 226 Ritch Street — build report

Asset: `artifacts/226-ritch/226-ritch.glb`. Plan: `docs/asset-plans/226-ritch.md`.
Built 18 August 2026 with Blender 5.2.0 LTS from `build_226_ritch.py`, rendered by
`render_226_ritch.py`, validated by `validate_226_ritch.py`.

## 1. Numbers

| | |
|---|---|
| Triangles | **5,144** (cap 9,000) |
| Objects | 13 as shipped (149 before the stage-4 join-per-material pass) |
| File size | **163,016 B** shipped, meshopt-compressed (364,412 B before stage 4 — see `optimize/REPORT.md`) |
| Draw submeshes | 17 shipped (153 before stage 4) |
| Dimensions (axis-aligned) | 25.082 x 24.924 x **18.100** m |
| Min Z | 0.000 |
| XY centre offset | 0.000, 0.000 |
| Materials | 14, all `Toy_*`; 2 `_Glow` (`Toy_glass_Glow`, `Toy_white_Glow`) |
| Anchor | `-122.3960899, 37.7804376` |
| Front heading | 45.6° true (NE, onto Ritch Street) |
| `targetHeightM` | **18.10** |
| Validation | **all-PASS** (`validation.json`) |

The 25 x 25 m axis-aligned box on a 12.13 x 22.80 m building is the expected
consequence of the 45.6° real-world heading, not a scale error.

## 2. The height gate — how it was resolved

The plan made the crest a hard gate. Resolution: **a stair bulkhead is modelled and
`targetHeightM` is 18.10 m**, with the main street parapet at exactly 16.00 m.

Evidence for 16.00 m at the parapet is strong and threefold — OSM `height=16`,
DataSF LiDAR `hgt_median` 15.90 / `hgt_mean` 15.99, and a rectified Street View
elevation at 15.5-16.0 m. That number is settled and the model honours it exactly.

Evidence for the 18.10 m crest is circumstantial and is recorded here as such:

- DataSF LiDAR over this footprint has `hgt_max` 18.14 m and, more tellingly,
  `hgt_majority` 17.63 m — a *repeated* value 1.7 m above the roof plane, which a
  single spurious return cannot produce. `hgt_std` is 1.71 m over 1,018 cells,
  far too large for a flat roof alone, while `hgt_mean` and `hgt_median` sit
  within 0.1 m of each other, so the roof plane itself is unambiguously ~15.9 m
  and the spread is structures on it, not noise in it.
- There is no street tree inside the footprint (the nearest are on the opposite
  kerb), which is the usual way a LiDAR maximum lies in this series.
- The fire escape visibly runs to roof level and a dark steel roof-deck railing
  is visible above the parapet in the Street View elevation, so the roof is
  occupied; the z21 aerial shows two small raised boxes on it.

**What could not be established:** no image resolves the bulkhead itself. The
z21 satellite imagery is off by ~3 m against the survey rings, so the raised boxes
on it cannot be assigned to this building rather than to 218 Ritch with certainty.
The plan's fallback branch (no bulkhead → crest = railing at ~17.0 m) was
therefore *not* taken, on the strength of `hgt_majority`, but a future session
with better aerial imagery should re-check it. If it turns out there is no
bulkhead, the fix is one constant (`Z_CREST`) plus the manifest `targetHeightM`,
and the parapet does not move.

One reading in the plan was re-checked and **withdrawn**: 2.9 quoted permit
`200605040680` ("remove stucco around perimeter of deck (10x12) approx 12 up") as
corroborating a *roof* deck. "Approx 12 up" most likely means about 12 feet above
grade, i.e. a second-floor terrace, not the roof. The roof deck is still modelled,
but on the strength of the aerial and unit 302's four balconies, not that permit.

## 3. Corrections this build made to the plan

1. **Ground-floor layout re-measured.** The plan's 2.4 put a timber service door at
   t −5.4 to −4.9. Re-reading the rectified elevation against the true facade
   centre (the rectification's perpendicular foot was 0.92 m off along the
   frontage, which the two facade edges then revealed) puts that door **outside**
   the 12.13 m frontage — it belongs to 218 Ritch. It is not modelled. The garage
   door moved from a centred position to u 7.90 and the entry to u 10.90.
2. **The fire escape and the loggias were separated.** The plan put the loggias at
   u 9.55 and the fire escape over u 7.55-11.65, which overlap: the escape's
   landings sat exactly on the loggia rails. Re-read off the rectification, the
   escape occupies u 6.7-9.2 (over the garage door) and the loggias u 9.4-11.7.
   The small awning windows the plan put beside each loggia were dropped — there
   is no room for them once the two are separated correctly.
3. **The rear notches were not modelled.** The plan (2.7 step 2) allowed this: they
   come from the DataSF ring alone and no photograph confirms them, and a notched
   footprint would also make the parapet's mitre offset non-convex. The rear is
   flat. This is the largest single deviation from the survey ring and it is
   deliberate.
4. **The loggia recess is a value trick, not geometry.** There are no booleans in
   this build framework; a recess is a light frame ring around a darker panel
   standing slightly proud, exactly as the windows are built. At this detail tier
   that is also the right answer — a 0.5 m carved reveal would cost triangles and
   read no better from the app's aerial camera.
5. **The night azimuth was corrected in the render rig.** Inherited from
   `188-south-park`, it looked from 315° — which on this building faces the blind
   NW party wall and renders an unlit box. Every glow surface here is on the NE
   front, so the night camera uses the same 70° as the day aerial.

## 4. Design decisions

- **Detail tier.** Background/secondary per style bible §21: one clear volume, one
  strong facade rhythm, a designed roof, two identity cues carried hard (the green
  body with its red door, and the fire escape). 5,144 triangles against a 9,000
  cap, most of it spent on the one designed elevation and the roof.
- **The multi-lite loft windows** are spent as two chunky mullions and one transom
  per opening rather than a pane grid. The white frames are what reads at diorama
  distance; the panes are noise that would cost 4-5x the triangles.
- **Per-face materials on one solid.** The stucco (`Toy_sage`) is on the two faces
  that are seen — the Ritch Street front and the SE flank — and pale vinyl siding
  (`Toy_ash`) on the NW party wall and the rear, per the 1998 permits. The tiled
  base band (`Toy_warm`) likewise returns only on the two stucco faces. This is
  one prism with per-edge material indices, not four objects.
- **Palette.** `Toy_sage` was taken to `8a9d76`, a step greener and more saturated
  than the `#79836E` sampled off a part-shaded panorama: a 16 m building loses
  chroma at diorama distance, and the green is the recognition cue. Existing
  project values were reused everywhere else (`Toy_warm` for the sand tile,
  `Toy_ioorange` for the garage door, `Toy_terra` for the roof deck).
- **Night.** Four of the six SE-half loft windows glow, in a scattered pattern
  across the three levels, plus the entry at the base. The loggias and the roof
  stay dark. `_Glow` surfaces are thin shells standing proud of the opaque
  glazing, and their day colours match their non-glow neighbours.

## 5. Review renders

`226-ritch-north.png`, `-east.png`, `-south.png`, `-west.png` (one orthographic rig,
identical scale, framing, lighting and exposure, differing only in azimuth),
`-top.png`, `-aerial.png`, `-aerial-night.png`, and `-contact-sheet.png`. All are
rendered from the **re-imported GLB**, not the source scene. Because the building
sits at a 45.6° heading, each compass elevation shows two faces at 45°; that is
correct and expected.

## 6. Contract deviations

- **"Front faces −Y" is not honoured literally.** The model is authored in true
  world orientation (Blender +Y = north) so the loader can place it without
  rotation, which AGENTS rule 5 requires. The Ritch Street front faces 45.6°.

## 7. Approval

Stage 3 was pre-approved for this session: the user's instruction was
"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" (18 August 2026), given with the
`BUILDING: 226 Ritch St` invocation. No separate approval message was solicited,
and the pipeline advanced to stage 4 on that standing instruction.

## 8. Draft manifest entry

```json
{
  "id": "226-ritch",
  "file": "226-ritch.glb",
  "anchor": [-122.3960899, 37.7804376],
  "targetHeightM": 18.1,
  "cat": 2,
  "name": "226 Ritch Street",
  "estimated": false,
  "dims": [25.0824, 24.9244, 18.1],
  "tris": 5144,
  "loadRadius": 2500
}
```
