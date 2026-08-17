# 140 South Park — build report

Asset: `140-south-park.glb` · built 16 August 2026 · Blender 5.2.0 LTS
Plan: `docs/asset-plans/140-south-park.md` · Dossier: `REFERENCE.md` (outranks the plan)

## Shipped numbers

| | |
|---|---|
| Triangles | **3,136** (budget 7,000) |
| Objects | **11** mesh after the stage-4 join (87 as authored), nothing else |
| File size | **87,540 B** raw, meshopt-compressed (212,588 B pre-optimize) |
| Dimensions (m) | 26.229 × 26.167 × **10.680** |
| bbox min / max Z | 0.000 / 10.680 |
| XY centre offset | (0.175, −0.206) m |
| Materials | 10, all `Toy_*`, flat, no textures, no alpha |
| Glow groups | 2 — `Toy_gold_Glow`, `Toy_glass_Glow` |
| Anchor (WGS84) | −122.3947379, 37.7814643 |
| Front heading | 135.0° true (SE), onto the South Park oval |
| Target height | 10.68 m (cornice crest) — loader scale lands at 1.0 |

The XY bbox is near-square because a 29.81 × 6.84 m bar standing at 45° to the world axes
projects to a ~26 × 26 m axis-aligned box. That is expected. The 4.4 : 1 stick is checked
on the elevations and the top view, and the validator's plausible-dimensions gate was
rewritten to say so rather than to assert a rectangle.

## Validation — `validation.json`, overall **PASS**

| Check | Result |
|---|---|
| Fresh factory-reset scene, only the exported GLB imported | PASS |
| Metres, plausible dimensions | PASS |
| Crest normalised to target (10.68 ± 0.02) | PASS |
| Base at z = 0 | PASS |
| Centred in XY | PASS |
| Under triangle budget | PASS |
| No image textures | PASS |
| No transparency | PASS |
| Materials follow the `Toy_*` contract, no `Toy_body` | PASS |
| No cameras or lights | PASS |
| No animation, skinning or constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward — per-object signed volume (11/11 shipped; 87/87 as authored) | PASS |
| Normals outward — 31,500 visibility rays, 0 flipped first hits (0.000% residual) | PASS |
| No degenerate geometry | PASS |
| No unexpected objects or leaked foreign geometry | PASS |

## WARN — deliberate palette extension

**`Toy_olive` = `5f655c`** is not in the shared palette. The building is a dark
desaturated gray-green; `Toy_slate` (`6f7883`) is a blue-gray and too light, `Toy_pine`
(`3f6b4f`) is a saturated green and far too strong for a whole wall. Neither is this
building. Logged here in the same form as 155 South Park's `Toy_peach` and 380 Brannan's
`Toy_slate`, for a palette review to fold in or reject.

## Iterations

1. **First build, first aerial (2,680 tris).** Massing, cornice, shopfront and roof all
   read correctly at the app's camera on the first pass. Three problems:
   - the review aerial stood at azimuth 145°, which swung it 10° toward the **south-west
     party wall** — a deliberately blank 29.8 m slab. Moved to 125° so it swings toward
     the north-east side passage, which is a real elevation. Day and night both.
   - the transom band was `Toy_glassl`, and a bright blue bar across the full frontage
     read as a light fixture rather than as glazing. Changed to `Toy_glass` with three
     `Toy_ink` mullions, which is what the photograph shows.
   - the lap-siding shadow lines were too shallow to survive the aerial. Strip height
     0.07 → 0.09 m, proud depth 0.05 → 0.06 m.
2. **Second aerial (2,716 tris).** Reads correctly, but 200 m² of roof deck carried only
   a condenser pair, a hatch and a vent — a blank-roof failure under style bible §10 and
   §27. Added **two flush skylights** over the middle of the plan as a labelled
   typological reconstruction (a 29.8 × 6.8 m loft with window walls only at its two
   short ends has no daylight in its middle 20 m; their 0.18 m kerbs sit inside the 2010
   LiDAR's noise, so the survey neither confirms nor rules them out). Recorded as
   *inferred* in `REFERENCE.md` §4, not as a measurement.
3. **Top view review (3,148 tris).** Every roof object sat in one 6 m band, leaving the
   front 12 m of deck dead. Redistributed along the full 29.8 m: vent forward at v −11,
   skylights at v ±6, condensers at centre, hatch at v +11.
4. **Night review.** All three upper windows glowed, which reads as a render rather than
   as a building and competed with the gold shopfront that is meant to be the hero.
   Dropped the glow from the north-east light. Final: gold shopfront + transom, two cool
   upper windows, nothing on the flanks, rear or roof.
5. **Validator constants.** The script was seeded from `validate_155_south_park.py` and
   still asserted 155's anchor, heading, 10.1 m crest and rectangle-shaped bbox bounds.
   Corrected to this building's values and re-run: overall PASS.

Final: **3,136 triangles**, all gates PASS.

## Stage 4 — optimize

Run in the same session; see `optimize/REPORT.md` for the full metrics, census, gates and
A/B verification. Headline: **212,588 → 87,540 bytes (−58.8%)**, 87 objects → 11,
88 draw submeshes → 12, triangles and bounding box unchanged, worst A/B pixel delta
0.0194% against a 2%/4% gate. The optimized file is now the shipping GLB; the
pre-optimize original is archived at `optimize/input/140-south-park.glb`. The numbers in
"Shipped numbers" above are the post-optimize ones.

## Deliverables

```
artifacts/140-south-park/
  build_140_south_park.py      deterministic build -> .blend + .glb
  validate_140_south_park.py   fresh-scene contract validation -> validation.json
  render_140_south_park.py     six review renders + the night aerial
  make_contact_sheet.py        contact sheet
  140-south-park.blend
  140-south-park.glb
  140-south-park-{north,east,south,west,top,aerial,aerial-night}.png
  140-south-park-contact-sheet.png
  validation.json
  REFERENCE.md
  REPORT.md
  optimize/                    stage 4: scripts, A/B renders, gates, archived input
```

## Approval (stage 3)

Standing approval given by David at the top of the 16 August 2026 pipeline session:

> "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"

Recorded here as the gate-3 authorisation. The contact sheet, the day and night aerials
and the numbers above were presented in the session before stage 4 began.
