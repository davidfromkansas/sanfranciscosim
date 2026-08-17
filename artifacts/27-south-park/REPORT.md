# 27 South Park — build report

Built 16–17 August 2026 from `docs/asset-plans/27-south-park.md`, on branch
`pipeline/27-south-park`. **This report beats the plan** wherever the two
disagree.

## Shipped numbers (pre-optimize)

| | |
|---|---|
| File | `27-south-park.glb` |
| Objects | 77 |
| Triangles | **4,968** (cap 7,000) |
| Dimensions | 32.613 × 32.507 × **10.200** m |
| Footprint | 12.19 m frontage × 33.55 m deep, long axis 134.8°/314.8° |
| min Z / XY centre | 0.000 m / (0.000, 0.000) |
| Crest | parapet coping at **exactly 10.20 m** → loader scale 1.0 |
| Materials | 11, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow groups | 2 — `Toy_gold_Glow` (ground-floor bays), `Toy_glass_Glow` (2 of 6 arches) |
| Raw / gzip | 289 KB / 51 KB |
| Validation | `validation.json` — **overall PASS**, 16/16 checks |

The ~32.6 × 32.5 m axis-aligned XY box is the expected consequence of a 314.8°
real-world heading on a 12.19 × 33.55 m building, not a squared-up footprint.
The `front`, `top` and `aerial` renders are where the 2.75 : 1 stick is checked.

## Deliverables

`build_27_south_park.py` (deterministic build) · `27-south-park.blend` ·
`27-south-park.glb` · `render_27_south_park.py` ·
`validate_27_south_park.py` · `make_contact_sheet.py` ·
`REFERENCE.md` · `validation.json` · renders `-front -north -east -south -west
-top -aerial -aerial-night -contact-sheet`.

Every render is made from the **exported GLB re-imported into an empty scene**,
so all eight images depict exactly the geometry that ships. `validate` factory-
resets and imports only the final GLB; it never inspects the authoring `.blend`.

## Dossier corrections and deliberate departures

Nothing in the plan's geometry or history turned out to be wrong. Four
authoring decisions depart from it, all made at the render:

1. **A `Toy_stone` archivolt was added to each arch head.** The plan called for
   a `Toy_navy` frame on `Toy_glass` glazing. Both are very dark, and the first
   aerial showed the arcade collapsing into six flat holes — the frames were
   invisible. Each head now carries a 0.12 m proud light band, which is what the
   real proud brick arch does anyway, and the frames moved to `Toy_ink` so the
   frame/glass boundary reads. `Toy_navy` is kept for the ground-floor joinery,
   where the plan's blue-green identity argument still holds and the openings are
   big enough for it to show.
2. **The arcade was raised.** Sill 5.20 → 5.35 m, springing 7.50 → 7.90 m, crown
   8.05 → 8.55 m (rise 0.55 → 0.65 m). At the planned heights 1.55 m of blank
   wall sat between the arch crowns and the roof deck and the arcade read as
   marooned in the middle of the facade. It now sits under the parapet the way
   the Jan 2025 photograph shows.
3. **The roof membrane is `Toy_roofd`, not `Toy_steel`.** The real membrane is
   light warm grey and the plan said so, but a pale roof inside pale parapets
   inside pale walls was one flat shape from the app's downward camera. The
   charcoal deck is what makes the parapet ring and the white plant read. The
   plan's `Toy_roofd` mechanical caps went to `Toy_steel` for the same reason,
   in reverse. Logged as a deliberate style-over-literal call under the style
   bible's §9.
4. **The hero night glow is `Toy_gold_Glow`, not `Toy_trim_Glow`.** `Toy_trim`
   is near-white and previewed as a blown white slab across the ground floor.
   Gold is warmer, reads as lit office rather than as a light fixture, and is
   the same value 140 South Park uses one lot along the oval.

Two smaller notes:

- **The roof plant is spread further than "packed into the middle third".** The
  first aerial bunched every unit into one 6 m band on a black plinth slab that
  read as a hole in the roof. The plinth is gone and the six units, three fans,
  two monitors and two vent pipes now run from about a third of the way back
  from the front to just past the centre, with the rear third left bare as the
  nadir aerial shows. Closer to the photograph and a better composition.
- **96 degenerate triangles were found and fixed.** `arch_profile()` emitted the
  springing points twice — once explicitly and once as the arc's own endpoints —
  putting two zero-area triangles in every cap of every arch element. The
  validator's `no_degenerate_geometry` and `invalid_or_nonunit_loop_normal_count`
  both caught it; both are now clean.

## Contract deviations, stated plainly

- **"Front faces −Y" is not honoured, deliberately.** The asset is authored in
  true world orientation (Blender `+Y` = north, `+X` = east) so the loader can
  place it with no rotation. The South Park elevation faces **north-west,
  bearing 314.8°**. Real-world orientation wins (AGENTS rule 5).
- **The rooftop plant is modelled below the parapet coping.** The DataSF LiDAR
  maximum over this parcel is 11.73 m and the plant plausibly reaches it. Every
  unit here tops out at 10.10 m so the **coping at 10.20 m is the crest**. Had
  the plant been modelled at true height, `targetHeightM` would describe a
  condenser rather than a building and the loader would rescale the whole model
  against it — the same argument that removed 2 South Park's flagpole. See
  `docs/asset-plans/27-south-park.md` §2.10 and §2.15.
- **`Toy_ink` is used and was not in the plan's palette table.** It is a
  standard `sf-asset-check` palette entry, not an extension; see departure 1.

## Open questions carried forward (plan §2.15)

- **The crest question is answered as far as the evidence allows.** The 2026
  nadir aerial at ~3 cm/px shows no penthouse, no stair bulkhead and no roof
  deck inside this ring, and no permit in 53 records adds one; the parcel's
  height standard deviation is 0.45 m over 4,479 LiDAR cells, which is one flat
  roof. So 9.60 m is the deck, 10.20 m (Overture's per-ring USGS-LiDAR value for
  way/112759868) is the coping, and 11.73 m is plant. **An oblique aerial would
  settle it properly; the nadir cannot.**
- **The bay assignment stayed unresolved.** The 12.19 m frontage is measured and
  the "27" numeral sits beside the mahogany door, but no image found resolves the
  party-wall joints, so the six-arch / three-bay rhythm remains *derived from the
  width* (12.19/6 = 2.032 m, 12.19/3 = 4.063 m) rather than counted off a
  photograph of a confirmed 27-only extent. If better imagery contradicts the
  count, the count loses; the width does not.
- **The rear (south-east) elevation is inferred, not observed.** Nothing
  photographs it. It ships as plain painted brick with two small service windows.
  A roll-up loading door would be unsurprising and is the most likely correction.
- **The Perkins&Will attribution was not promoted.** Their 2023 "South Park
  Venture Capital Firm" renovated a 1920s brick-clad South Park building with
  "large, arched metal-clad windows" — which fits this row and nothing else near
  the oval — but the client and address are unpublished and the matching
  2020–2021 permits are filed under **21** South Park. It is cited as evidence
  about the row's window language only.

## Manifest entry (verified against the shipped asset)

```json
{
  "id": "27-south-park",
  "file": "27-south-park.glb",
  "anchor": [
    -122.3931439,
    37.7817369
  ],
  "targetHeightM": 10.2,
  "cat": 3,
  "name": "27 South Park",
  "estimated": false,
  "dims": [
    32.6129,
    32.5074,
    10.2
  ],
  "tris": 4968,
  "loadRadius": 2500
}
```

`loadRadius` takes the default: `max(2500, 10.2 × 30) = 2500` m.

## Integration warning — read before the re-bake

DataSF traces **21, 27 and 29 South Park as ONE 1,115 m² polygon**
(`SF3775042`). Removing this building's procedural mass necessarily removes 21's
and 29's, and no radius avoids it — below 3.45 m nothing is excluded at all and
the 10.67 m procedural block buries this 10.20 m asset entirely. The measured
safe window is **(3.45, 20.07) m** and the registry entry takes **15 m**, which
also excludes all three Overture rings outright so the gap-fill pass cannot
re-add them if occupancy ever changes. Full derivation in
`docs/asset-plans/27-south-park.md` §2.13.

Consequence: until 21 South Park (sibling branch `pipeline/21-south-park`) and
29 South Park have GLBs, the bake leaves a gap on both flanks. That is why both
party walls in this asset are finished blind faces with the parapet carried
across rather than raw slabs.

## Approval

Pending. See §"Stage 3" of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`.
