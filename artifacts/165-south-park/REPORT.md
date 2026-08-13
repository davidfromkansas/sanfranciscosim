# 165–167 South Park — build report

Stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run against
`docs/asset-plans/165-south-park.md`.

**This report beats the plan wherever they disagree.**

## Result

| | |
|---|---|
| Asset | `artifacts/165-south-park/165-south-park.glb` |
| Validation | **all-PASS** (`validation.json`, Blender 5.2.0 LTS, fresh-scene re-import) |
| Triangles | **2,008** (cap 6,000) |
| Objects | 25 |
| Dimensions | 19.097 × 21.910 × **9.000** m |
| min Z / XY centre offset | 0.000 m / (0.000, 0.000) m |
| File | 121.9 KB raw, **30.0 KB gzip** (budget ≤ 500 KB compressed) |
| Materials | `Toy_glass`, `Toy_glass_Glow`, `Toy_ink`, `Toy_roofd`, `Toy_sky`, `Toy_steel`, `Toy_trim`, `Toy_trim_Glow` |
| Manifest anchor | **-122.3943764, 37.7808599** |
| Target height | **9.0 m**, `"estimated": true` |
| Street elevation faces | 349.73° true |

The 19.1 × 21.9 m axis-aligned XY box is the ~145° rotation of a 6.2 × 24.0 m sliver,
not a 19 m building.

## Dossier corrections made during the build

Nothing in the plan's dossier was overturned. Two numbers were tightened and one was
carried forward unresolved:

1. **The footprint was re-derived in the project's own tangent projection** rather than
   the generic one used to write the plan (`110540` m/degree latitude, not `111320`).
   This moved the polygon by up to 0.15 m over its 24 m length and shifted the anchor
   in the seventh decimal place. The plan's stated anchors survive to that precision.
2. **The built area came out at 131.2 m²**, not the plan's "~131 m²" — unchanged in
   substance. Two storeys of it is 2,824 sq ft against the assessor's 2,680, a 5%
   overshoot, which is the best available reconciliation of a surveyed parcel, a
   raster-derived footprint 12% smaller, and a gross floor area that includes interior
   walls the footprint does not.
3. **The 9.90 m LiDAR maximum remains unexplained and is NOT modelled.** The plan's
   2.7 step 9 made a roof bulkhead conditional on confirming it from aerial imagery.
   It could not be confirmed: available imagery of the roof is oblique and partly
   obscured by the street tree, and the maximum is equally consistent with a stair
   bulkhead, a chimney, or a tree return over the roof edge. The shipped crest is
   therefore the 9.0 m cornice, and `"estimated": true` is set for exactly this reason.
   **This is the asset's single largest open risk** — if a bulkhead is later confirmed,
   the target height becomes 9.9 m and the model needs a rebuild, not a rescale.

## Design iterations

Reviewed from the high three-quarter aerial first, per stage 2's session-hardened
overrides. Four rounds:

**Round 1 — the gate disappeared.** The gate leaf was authored 0.10 m *inside* the
passage recess. In the aerial it fell into its own shadow and rendered as a black
doorway, which destroyed the building's only saturated cue and made it indistinguishable
from 171 next door. Moved to 0.07 m **proud** of the siding plane, with the dark recess
behind it. This is also the commoner real configuration for a party-wall passage gate.

**Round 1 — the siding read dead.** `Toy_steel` `#9aa0a6`, the nearest palette entry,
rendered noticeably darker and greener than the real building. Changed to **`#a9b5bd`,
which is off-palette** — a WARN under `sf-asset-check`, not a FAIL. Justification: the
style bible's SF exception (painted residential rows keep their tinted facades) covers
it, the plan's 2.8 pre-authorised it, and the value is the building's actual desaturated
blue-gray. **The material keeps the `Toy_steel` name**, so the contract check and the
loader's colour-bake merge path are unaffected.

**Round 2 — the flat roof read as a bare cut face.** Added a 0.17 m parapet lip in the
siding colour around the whole roof. The roof is the surface the app's camera actually
sees; without an edge the sliver looked like a sawn-off extrusion. The lip sits below
the 9.0 m cornice, so the crest is unchanged.

**Round 2 — 24 m of blank party wall read as a slab.** The floor-line band was running
across the street elevation only. Extended around the whole perimeter. This is not
decoration: 159 next door is only 5.48 m tall against this building's 8.55 m, so the
upper third of the east flank is genuinely visible in the city.

**Round 3 — the base returns read as black boxes.** The stone-tile base was modelled as
a facade band with 0.6 m returns that stopped dead at the corners, which from the air
looked like a black block stuck to the wall. Extended to the whole perimeter. The real
tile is a facade-only treatment, but every building has a base course, and the wrap also
gives the terrain seam somewhere to hide.

**Round 3 — the cornice returns read as lumps.** Shortened from 0.50 m to 0.30 m, so
they read as a cornice die at each front corner rather than as blocks sitting on the
parapet.

**Round 4 — the night accent rendered as nothing.** The gate's supporting glow was
authored as a shell on the back wall of the passage recess, where the opaque gate leaf
in front of it hid it completely: the night render showed two lit windows and a dark
gate. Replaced with a **passage lamp above the gate** (`Toy_trim_Glow`), which is both
visible and true — Street View shows a fixture there. `Toy_sky_Glow` is gone from the
asset; `Toy_sky` remains, on the gate leaf only.

**Round 4 — the top view was mis-rolled and cropped.** The roll put the 24 m sliver
across a portrait frame and cut 4 m off its rear. For a top-down camera image-up maps to
world `(-sin rz, cos rz)`, so the correct roll is `LONG_AXIS - 90`, not
`-(180 - LONG_AXIS)`. Fixed in `render_165_south_park.py`.

## Deliberate deviations from the contract and the plan

| Deviation | Status | Why |
|---|---|---|
| `Toy_steel` is `#a9b5bd`, off-palette | **WARN** | see round 1 above; style bible SF exception; pre-authorised in the plan's 2.8 |
| Front faces 349.73°, not −Y | **expected** | `placeGeneric` applies no rotation, so assets are authored in true-world orientation; real-world orientation wins (asset-plans README, AGENTS rule 5) |
| The street arc is modelled as a chord | **accepted** | the bulge is 0.14 m, below the 0.10 m bevel radius |
| No roof bulkhead | **open risk** | see correction 3 above |
| Party flanks are blind | **correct** | they are party walls; the neighbours are attached on both sides |

## Night state

Hero glow: **two** lit windows on the upper storey of the street elevation. This is a
three-unit house on a quiet residential oval — a fully lit facade would read as an
office. Supporting accent: the passage lamp above the gate. The roof does not glow.
All glow surfaces are thin shells proud of the opaque glazing, so the app's ~12%-alpha
day pass shows the opaque window behind them.

## Files

```
build_165_south_park.py       deterministic build (Blender 5.2 LTS, headless)
render_165_south_park.py      controlled review renders from the EXPORTED GLB
validate_165_south_park.py    fresh-scene contract validation
make_contact_sheet.py         composes the review renders
165-south-park.blend          authoring scene
165-south-park.glb            THE ASSET
165-south-park-{north,south,east,west,top,aerial}.png
165-south-park-aerial-night.png
165-south-park-contact-sheet.png
validation.json               machine-readable contract report
REFERENCE.md                  research dossier
```

Rebuild: `blender -b --python build_165_south_park.py`

## Draft manifest entry

```json
{
  "id": "165-south-park",
  "file": "165-south-park.glb",
  "anchor": [
    -122.3943764,
    37.7808599
  ],
  "targetHeightM": 9.0,
  "cat": 1,
  "name": "165–167 South Park",
  "estimated": true,
  "dims": [
    19.0972,
    21.9096,
    9.0
  ],
  "tris": 2008,
  "loadRadius": 2500
}
```

## Integration note carried forward

The registry entry's `lon`/`lat` must **not** equal the manifest anchor. `placeGeneric`
positions the GLB from the manifest alone, while `pipeline/lib/landmarks.mjs`
`lon`/`lat` is only the centre of the bake-time exclusion circle — and on this site the
two cannot be the same point. Use `-122.3943963, 37.7808764` (the DataSF LiDAR
footprint's area centroid) with **`exclude: 1.3`**. The workable band is 0.4 m wide:
the Overture/OSM polygon for this building triggers at 1.09 m and 159 South Park's
DataSF footprint triggers at 1.49 m. The full measurement table and the Overture
gap-fill risk are in the plan's 2.13, and both must be re-verified against the real
`pipeline/data/overture_buildings.geojsonseq` at stage 5.

## Stage 3 — approval

Pending. Not yet presented.
