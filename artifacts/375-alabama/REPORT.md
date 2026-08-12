# 375 Alabama Street — build report

Deliverable: `375-alabama.glb`, a miniature of the **Ames Harris Neville Co. Building**
(1926) at 375 Alabama Street, San Francisco, authored for the SF-SIM toy-diorama city.

Built from `docs/asset-plans/375-alabama.md` (Part 1) under
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`. Research behind every number is in
`REFERENCE.md`. **Where this report and the plan disagree, this report wins.**

## Shipped numbers

| | |
|---|---|
| Triangles | **10,176** (cap 14,000) |
| Objects | 226 |
| Dimensions (XY bbox / Z) | 67.32 x 61.61 x 22.50 m |
| Building itself | 61.10 x 54.63 m footprint — the larger XY bbox is the 4.32° heading, not a scale error |
| min Z | 0.0000 |
| XY centre offset | 0.038, −0.002 m |
| Materials | 12, all `Toy_*`, all flat, no textures, no alpha |
| Glow groups | 3 — `Toy_trim_Glow` (tower crown + entrance), `Toy_glass_Glow` (window scatter), `Toy_glassl_Glow` (two lit monitors) |
| Anchor | `-122.4118477, 37.7645633` |
| targetHeightM | 22.5 (stair-tower crown, normalised exactly — loader scale lands at 1.000) |
| Validation | `validation.json` — **overall PASS**, all 16 checks |

## Reproduce

```bash
blender -b --python build_375_alabama.py            # -> .blend + .glb
blender -b --python render_375_alabama.py -- --glb 375-alabama.glb
blender -b --python render_375_alabama.py -- --glb 375-alabama.glb --night
python3 make_contact_sheet.py
blender -b --python validate_375_alabama.py -- --glb 375-alabama.glb
```

Blender 5.2.0 LTS. Renders always re-import the exported GLB, so every image depicts exactly
the geometry that ships; validation runs in a factory-reset scene against the same file.

## Dossier corrections and deviations from the plan

These are the places where building the thing changed what the plan said. Each is a
deliberate decision, not a slip.

1. **Footprint reduced to four corners.** Plan §2.3 kept the survey's two sub-620 mm jogs on
   the east and west walls as "real pilaster returns worth keeping". They are — but they are
   *pilaster* returns, and this model expresses pilasters as 1.5 m piers standing 0.25 m proud
   of the wall. Modelling the jogs as footprint steps *and* the piers as applied panels would
   have double-counted the same feature. The jogs are absorbed into the pier rhythm; the body
   is the four-corner OBB. Footprint area error: +0.1 %.
2. **Windows are continuous glazing bands, not 126 punched openings.** Plan §2.7 step 4
   described per-bay window openings. A reinforced-concrete frame really does glaze
   continuously between its piers, and banding costs roughly 300 triangles where punched
   openings would have cost about 7,800 — over half the budget for a rhythm the proud piers
   already carry. The elevations read the same and the money went to the medallions instead.
3. **Medallions are 1.7 m, not the plan's 2.0 m.** At 2.0 m the cog's top edge broke through
   the parapet crest. 1.7 m keeps the whole disc inside the frieze band where the real
   castings sit.
4. **Medallions are not bevelled.** 23 bevelled 24-gon cogs cost 6,500 triangles — over a
   third of the entire asset — to soften an edge that is a fraction of a pixel from the app's
   camera. The first build came in at 17,900 triangles, over the cap, almost entirely because
   of this. Unbevelled, the whole asset is 10,176.
5. **The sawtooth monitors are trapezoids with a flat 0.8 m ridge cap**, not the plan's
   triangles. Bevelled, a single ridge vertex rounded into a barrel and the whole roof read as
   five fat white tubes from the aerial. The flat cap also gives the near-vertical north face
   enough area to read as glass. Slopes as built: opaque south face 54.5°, glazed north face
   75.5° — the plan's 25°/60° would have made the monitors 4 m wider each than the roof has
   room for.
6. **The tower was rebuilt after the first render.** As planned (7.6 m wide, projecting
   0.8 m, expressed only above the roof) it read as a white box parked on the parapet with an
   orange stripe — not a tower. As built: 6.4 m wide, projecting 1.10 m, with the two cream
   fins running the **full height from the pavement to the 22.5 m crown**, which is what the
   2007 photograph actually shows and what gives the shaft its lift.
7. **`Toy_mauve` (`#a2887f`) is a deliberate palette extension** for the tower's centre panel.
   The plan nominated `Toy_rust` (`#a86444`) as the nearest palette entry; rendered, it read
   as an orange billboard and became the loudest thing on a cream building whose only intended
   accent is the ornament. Off-palette is a WARN, not a FAIL (contract rule 7). Recorded here
   as the plan §2.8 note anticipated.
8. **The night state was retuned after the first night render.** Two monitors lit end to end
   over their whole glazed face read as fluorescent light bars and flattened the tower's hero
   glow. As shipped, each lit monitor glows over a 19 m stretch of the 51 m ridge and only the
   top third of its glazed face, and the tower crown glow starts lower (18.2 m) and is wider,
   so the hierarchy is tower first, monitors second, window scatter third.
9. **Orientation deviates from the contract's "front faces −Y" rule, as every plan in this
   set does.** The asset is authored in true world orientation (`+Y` = north) because
   `placeGeneric()` applies no rotation; the address front faces **west, 265.7°**. Real-world
   orientation wins (AGENTS rule 5).
10. **`targetHeightM = 22.5` is inferred, not published.** It is a photogrammetric read of the
    2007 DPR photograph calibrated against the LiDAR roof deck; the honest range is 21–24 m.
    Because the tower is the tallest geometry this number scales the whole asset. If a better
    source appears, correct it and rebuild — do not nudge the tower.

## Contract compliance

| Rule | Status | Note |
|---|---|---|
| Binary GLB, real metres | PASS | 67.32 x 61.61 x 22.50 m |
| Origin base-centre, min Z ≈ 0 | PASS | min Z 0.0000, centre offset 0.038 / −0.002 m |
| Crest normalised to target | PASS | 22.500 m exactly |
| Orientation | WARN (documented) | true-world heading, front faces west — deviation 9 above |
| Flat-colour `Toy_*` materials | PASS | 12 materials, `Toy_mauve` off-palette by design |
| No textures / transparency | PASS | 0 image textures, 0 transparent materials |
| `_Glow` only on night surfaces | PASS | 3 glow materials, all thin shells proud of opaque glazing |
| No `Toy_body` | PASS | — |
| Triangle budget | PASS | 10,176 / 14,000 (PERF-PLAN hard limit 30,000) |
| No cameras / lights / animation / armatures / constraints | PASS | all zero |
| Transforms applied, no negative scales | PASS | — |
| Outward normals | PASS | 226/226 objects positive signed volume; 0 non-unit loop normals; 31,500-ray visibility test residual 0 |
| No degenerate geometry | PASS | 0 degenerate triangles |
| No foreign / leaked geometry | PASS | fresh-scene re-import contains only the asset |

## Renders

All regenerated from the final export.

| File | View |
|---|---|
| `375-alabama-west.png` | Alabama Street — the address, the entrance, the tower |
| `375-alabama-south.png` | 17th Street — the long elevation |
| `375-alabama-east.png` | Florida Street |
| `375-alabama-north.png` | rear |
| `375-alabama-top.png` | sawtooth field, flat north membrane, parapet ring, tower |
| `375-alabama-aerial.png` | high three-quarter from the southwest |
| `375-alabama-aerial-night.png` | night state |
| `375-alabama-contact-sheet.png` | all of the above |

## Draft manifest entry

Not applied — integration is a separate job (`docs/asset-plans/INTEGRATION-PROMPT.md`).

```json
{
  "id": "375-alabama",
  "file": "375-alabama.glb",
  "anchor": [
    -122.4118477,
    37.7645633
  ],
  "targetHeightM": 22.5,
  "cat": 19,
  "name": "375 Alabama Street",
  "estimated": false,
  "dims": [
    67.32,
    61.61,
    22.5
  ],
  "tris": 10176,
  "loadRadius": 2500
}
```

Integration is **Case B** (new landmark): it also needs a `pipeline/lib/landmarks.mjs` entry
(`id: '375-alabama'`, `height: 22.5`, `exclude: 42`, camera
`{ distance: 330, yaw: 215, pitch: 18 }`) and a re-bake of the affected tiles. The footprint's
half-diagonal is 41 m, so the exclusion radius is larger than any previous non-monument entry —
verify at integration which baked footprints it removes, because Alabama and Florida Streets
are only ~20 m wide.

## Approval

Not yet approved. Stage 3 of `ADDRESS-TO-ASSET.md` is a human gate; the user's approval is
quoted here verbatim, with its date, before stage 4 (optimize) runs.
