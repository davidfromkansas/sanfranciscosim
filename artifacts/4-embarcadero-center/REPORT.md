# Four Embarcadero Center — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` for
`BUILDING: 4 Embarcadero Center, San Francisco` (`BATCH: yes`).

**Deliverable:** `4-embarcadero-center.glb` — a 179.00 m miniature of Four
Embarcadero Center (55 Clay Street), authored at its real-world heading, 17,904
triangles, all contract checks PASS.

| | |
|---|---|
| Manifest id | `4-embarcadero-center` |
| Anchor (WGS84) | −122.3961998, 37.7953001 |
| Long-axis bearing | 81.09° true; entrance faces **north** (351.09°) |
| Bbox (x, y, z) | 73.02 × 51.98 × **179.000** m |
| min Z / XY centre offset | 0.000 m / (0.310, 0.000) m |
| Triangles | **17,904** (cap 20,000) |
| Objects | 869 |
| File | 1,307 KB raw, **168 KB gzip** (pre-optimize) |
| Materials | 9, all `Toy_*`, flat, opaque |
| Glow materials | `Toy_glassl_Glow`, `Toy_red_Glow` |
| Validation | `validation.json` — **overall PASS**, 16/16 checks |

## Corrections this build made to the plan

**REPORT beats plan.** The plan (`docs/asset-plans/4-embarcadero-center.md`) was
re-verified before modelling; these are the places the build departs from it.

1. **The crown is not "three tiers per end zone applied to the whole strip".**
   The plan's §2.8 read as though the six depth-strips carried their tier height
   for the tower's full length. They do not: the near-orthographic north
   elevation (SFYIMBY / Sue Bierman Park) shows a single flat roofline across
   the length, so the stepping is confined to the **outer 10 m at each end**
   (`U_END_E = ±21.70`). The middle 43.4 m of the slab is flat-topped at 173.70.
   This is the reading that satisfies *both* the north elevation and the east-end
   crown photograph; the plan's wording satisfied only the second.

2. **The plan's §2.7 plan-projection exaggeration was not applied as written.**
   It proposed pushing the west spine out from 1.7 m proud to ~3 m. Extending
   the spine would have lengthened the building past its measured 63.45 m, so
   the same read was bought by **recessing the west end's south flank** instead
   (strips 5 and 6 from the measured −30.20 to −29.40 / −28.60). The overall
   −31.72 … +31.73 extent is exactly the measured one.

3. **The long-face window grid runs the full length, not the core span.** The
   first build glazed only `|u| ≤ 21.70` and left the end zones blank; the north
   elevation immediately showed it. The modules now span each long face's true
   extent and drop to the outer fin's parapet beyond the end-zone line.

4. **The crown glow is one pane row's upper 40%, not a band.** Two full rows —
   and, before that, a dedicated ring band — put a pale-blue block across the top
   third of the tower **in daylight**, which is not what the building looks like.
   A `_Glow` material's base colour is its day colour, so a large glow surface is
   a large day-visible surface. The crown is now the top ~8 m of the topmost pane
   row on every module, which still gives three descending lit rings at night
   (each tier's modules end at its own height) and reads as a modest accent by
   day.

5. **`Toy_roofd` is not used anywhere.** It renders near-black on a horizontal
   deck under the app's lighting; the roof, cooling towers and curbs are
   `Toy_steel`.

6. **Module count** came down from the plan's 22 per long face to 20 (pitch
   2.17 m, giving 24 modules across the longer real face extent) to stay inside
   the triangle cap after the full-length glazing fix.

## Height decision

`targetHeightM` is **179.00 m** and the bbox top is normalised to it exactly, so
the loader's `targetHeightM / measuredHeight` scale lands at 1.0.

- 173.70 m is CTBUH's *architectural* top and is the main parapet. It explicitly
  excludes functional-technical equipment.
- 179.05 m is DataSF LiDAR's `hgt_maxcm` over the footprint — 5.35 m above the
  parapet, which is one cooling-tower's worth, and the Google z20 roof plan shows
  exactly four of them.
- Repo convention for a plant crest is to ship the crest (cf. `300-brannan`,
  "25.2 m penthouse crest; 21.34 m parapet"), and AGENTS rule 5 wants the real
  thing in the scene.

The flagpole is deliberately not modelled — too thin for the toy style, and
LiDAR did not catch it either.

## Orientation

Authored with Blender `+Y` = true north, `+X` = east, geometry generated
directly in world space through a `uv(u, v)` map that bakes the 81.09° bearing
in, so transforms are already applied and the loader rotates nothing. The
entrance is on the **north** face (55 Clay Street), so the kit's `-Y` front
convention is *not* satisfied; this is a true-world-oriented landmark like
`555-california`, and that is the intended behaviour for `placeGeneric`.

## Night state

- **Hero:** the crown ring — the top of every module's topmost pane row. Because
  the end-zone modules stop at 135.10 / 154.40 and the core at 173.70, this
  reads as three descending lit rings wrapping the chevron.
- **Supporting:** a seeded (never random) ~1-in-3 scatter of lit window panes
  down the shaft, and the Clay Street lobby band.
- **Accent:** one `Toy_red_Glow` aviation bead on the spine.
- Every glow surface is a thin shell proud of its opaque `Toy_glass` pane, never
  a primary surface and never a closed shell around the body — so the daytime
  facade is not tinted.
- Day check: `Toy_glassl_Glow` is `#6f95b8`, a pale sky-blue that sits beside
  `Toy_glass` `#2a4d73` as a window catching light rather than as a different
  material.

## Validation

`validate_4_embarcadero_center.py` factory-resets Blender, imports **only the
exported GLB**, and reports on the re-import. All 16 checks PASS:

meters and plausible dimensions · crest normalised to 179.00 · base at z = 0 ·
centred in XY · under triangle budget · no image textures · no transparency ·
materials follow contract · no cameras or lights · no animation, skin or
constraints · transforms applied · no negative scales · normals outward by
per-object signed volume (869/869 positive) · normals outward by ray residual
(**0/31,500 flipped visible faces**) · no degenerate geometry · no unexpected
objects.

## Files

| File | What it is |
|---|---|
| `build_4_embarcadero_center.py` | deterministic build (`blender -b --python …`) |
| `render_4_embarcadero_center.py` | the review rig (`--only VIEW`, `--night`, `--samples N`) |
| `validate_4_embarcadero_center.py` | fresh-scene contract validation |
| `make_contact_sheet.py` | composes the contact sheet |
| `4-embarcadero-center.blend` / `.glb` | source scene and the shipping asset |
| `4-embarcadero-center-{north,east,south,west,top,aerial,night}.png` | review renders |
| `4-embarcadero-center-contact-sheet.png` | all seven, labelled |
| `validation.json` | the machine-readable report |

## Draft manifest entry

```json
{
  "id": "4-embarcadero-center",
  "file": "4-embarcadero-center.glb",
  "anchor": [
    -122.3961998,
    37.7953001
  ],
  "targetHeightM": 179.0,
  "cat": 3,
  "name": "Four Embarcadero Center",
  "estimated": false,
  "dims": [
    73.02,
    51.98,
    179.0
  ],
  "tris": 17904
}
```

`loadRadius` is deliberately absent — see the integration notes in the plan's
§2.13: at 179 m this is a skyline piece, and every other manifest landmark over
100 m stays resident.

## Stage 3 — approval

Pending.
