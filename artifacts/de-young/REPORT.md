# de Young Museum asset report

## Result

**PASS** — `de-young.glb` meets the repository's landmark contract and was
validated after fresh-scene re-import in Blender 5.2.0 LTS. Per the task
instructions the model is **not** integrated: the production manifest,
`pipeline/lib/landmarks.mjs`, and all app code are untouched, and nothing has
been committed. All deliverables live in `artifacts/de-young/`.

The exact exported GLB was re-imported before all seven review renders were
produced. `validation.json` is the machine-readable authority for the metrics
below.

## Deliverables

- `REFERENCE.md` — research dossier and design decisions
- `build_de_young.py` — deterministic model build/export script
- `render_de_young.py` — fresh-GLB controlled render script
- `validate_de_young.py` — isolated re-import validator
- `make_contact_sheet.py` — contact-sheet composer
- `de-young.blend` — reproducible authoring scene (asset only)
- `de-young.glb` — final binary deliverable (~151 KB)
- `validation.json` — full object-level machine report
- `de-young-{north,east,south,west,top,aerial}.png`
- `de-young-night.png` — night-state preview (uNight = 1 emulation)
- `de-young-contact-sheet.png`

Rebuild from this directory with:

```bash
blender -b --python build_de_young.py
blender -b --python validate_de_young.py
blender -b --python render_de_young.py
python3 make_contact_sheet.py
```

(Authored and validated with Blender 5.2.0 LTS at `/Applications/Blender.app`;
the scripts use no 5.x-only APIs knowingly and should run on 4.5 LTS as well.)

## Orientation and heading (recorded decision)

Authored in true-world orientation: Blender **+Y = true north, +X = east**, so
`placeGeneric` drops the model at its real heading with no rotation. The
building's long axis is modeled at its measured real-world bearing of
**48.2° clockwise from true north** (SW → NE); the Music-Concourse entrance
facade faces south-east (bearing ≈ 138°), matching the surveyed grid shared
with the California Academy of Sciences across the concourse. The plan
dossier's "~171°" axis claim was verified to be wrong and is documented in
`REFERENCE.md`. The Hamon tower's base sits on this museum grid and its top is
rotated **41.8° clockwise** so the observation slab's long axis runs true
north–south — the architects' published parti of aligning with the city's
avenue grid (OSM's traced outline measures ~31°; the discrepancy and the
decision are documented in `REFERENCE.md`).

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 151 KB self-contained `de-young.glb` |
| Plausible real-world meters | PASS | 151.87 × 162.57 × 43.9 m world-axis bounds of the 153.7 × 76.1 m footprint rotated to bearing 48.2°, plus eave/canopy projections |
| Origin / base | PASS | bounding box min Z 0.0 m; XY center offset [0.0, 0.0] m |
| Orientation | PASS | true-world heading as recorded above |
| Triangle budget (≤ 24,000) | PASS | 2,201 / 24,000 triangles |
| Applied transforms | PASS | all 88 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | 0 invalid/non-unit loop normals; 0 flipped visible first-hits across 22,500 deterministic rays (15,059 hits) |
| Unexpected / leaked geometry | PASS | 88 mesh objects only; no studio plane, context, camera or light in the GLB |
| Image textures / PBR maps | PASS | 0 images and 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque |
| Flat material contract | PASS | ten `Toy_*` materials from the project palette; roughness 0.85; no `Toy_body` |
| Glow naming | PASS | `Toy_white_Glow` on the tower observation lantern; `Toy_gold_Glow` only on night-lit glazing (entry court, entrance passage, slit windows, café corner) |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets then imports the final GLB; the render script independently repeats that isolation |

## Geometry and materials

- Object count: **88 mesh objects**
- Triangle count: **2,201**
- Dimensions: **[151.8662, 162.5656, 43.9] m**
- Bounding box min: **[−75.9331, −81.2828, 0.0] m**
- Bounding box max: **[75.9331, 81.2828, 43.9] m**
- Minimum Z: **0.0 m**
- XY center offset: **[0.0, 0.0] m**
- Materials: `Toy_brick`, `Toy_glass`, `Toy_gold_Glow`, `Toy_ink`, `Toy_mint`, `Toy_roofd`, `Toy_rust`, `Toy_stone`, `Toy_verdigris`, `Toy_white_Glow`

The triangle count is intentionally far under budget: the de Young's identity
is a long, almost featureless copper monolith plus one twisting tower — padding
it with invented articulation would work against the recognition cues.

## Visual design

The miniature preserves the five cues ranked in `REFERENCE.md`:

1. **The twisting tower** — the measured 9.4 × 27.9 m base slab lofted
   through nine storeys to the wider, shorter 11.2 × 20.4 m observation
   level, twisting 42° clockwise with an eased profile so the swing
   concentrates near the top; recessed dark-glass storey bands are folded
   into the same loft so the glazing rides the warped faces, under the
   glazed lantern (`Toy_white_Glow` liner) and a copper cap with a verdigris
   top.
2. **The long copper band** — 154 × 76 m at 13 m, on its real bearing, with
   a cantilevered copper eave ring and four proud `Toy_brick` panel courses
   giving the facade its horizontal rhythm.
3. **Weathered copper** as a graphic rule: walls `Toy_rust` brown, every
   skyward copper surface (roof plane, tower cap) `Toy_verdigris` green.
4. **The angular plan** — the NE prow wedge, and four REAL roof voids cut
   through a tiled roof plane exactly where OSM maps them: the west garden
   court (tree canopies), the sunken entry-court plaza (stone floor,
   benches), and two narrow en-echelon fern canyons crossed by little stone
   bridges.
5. **The entrance** — a full-height cut in the SE facade into the open entry
   court, under the cantilevered roof-blade canopy, flanked by glazed passage
   walls; a handful of recessed-reading glass slots and the SW café glazing
   complete the "solid institutional facade" language.

The review elevations share one orthographic rig (scale, framing, lighting,
exposure); compass labels are true directions. The top view shows the twisted
tower head, roof planes, skylight strips and courtyard voids; the aerial uses
the style bible's camera (38° down, 105 mm) from the south-east so the
concourse front, entrance and tower read together.

## Night state and how it triggers

The asset carries a designed night state through the repo's existing glow
contract — **no app code is needed and the GLB contains no second geometry
set or animation**:

- **Trigger.** The app runs on San Francisco's real wall clock
  (`America/Los_Angeles`): `api/_lib/astro.mjs` computes solar elevation,
  `main.js` pushes it into `env.setSky(...)` once a second, and `env.js`
  derives `uNight` (exactly 0 by day, exactly 1 at night, blending through
  golden hour and dusk). The landmark loader (`app/src/assets.js`) splits
  every mesh by material name: `Toy_*_Glow` faces merge into a separate unlit
  `MeshBasicMaterial` bucket, and `kit.js updateLandmarkGlow` drives that
  bucket's opacity as `0.12 + uNight × 0.95`. So the glow ignites and fades
  automatically with the real sun — nothing to configure per asset. For
  testing, `SF.setClock(...)` forces any time of day.
- **Design.** Night composition: a dark copper monolith under the moonlit
  verdigris roof; the **white lantern** (`Toy_white_Glow`) crowning the
  twisted tower as the hero; the **entry sequence in warm gold**
  (`Toy_gold_Glow` on the entry-court liner, entrance passage, seventeen
  slit windows across all facades and the café corner); the west court and
  the two canyons stay deliberately dark so the monolith reads and the
  lantern pops.
- **Day safety.** Because glow faces render at 12 % opacity by day, every
  gold pane is a thin overlay 0.07 m proud of a dark `Toy_glass` backing
  pane, and the tower lantern has a dark glazing core — the daytime look
  (navy slit windows, dark glazed observation deck) is preserved.
- **Preview.** `de-young-night.png` emulates `uNight = 1` (unlit-style
  emission on `_Glow` materials, cool moon key, app-floor night zenith). The
  in-app render adds no bounce light from glow surfaces, so the preview's
  soft spill slightly flatters; the flat-colour read is representative.

The asset plan's §2.8 originally scoped `_Glow` to the observation floor
only; the extended night set was an explicit owner request (2026-08-10) and
stays within the contract's definition of `_Glow` ("signs, crowns, beacons,
lit windows").

## Draft manifest entry (verified — do not apply in this task)

```json
{
  "id": "de-young",
  "file": "de-young.glb",
  "anchor": [-122.4688156, 37.7715],
  "targetHeightM": 43.9,
  "cat": 16,
  "name": "de Young Museum",
  "estimated": false,
  "dims": [151.8662, 162.5656, 43.9],
  "tris": 2201
}
```

The anchor is the measured footprint center (world position of the GLB's
base-center origin), computed by the build script from the OSM-derived plan.
It deliberately differs from the plan dossier's anchor
(−122.4681752, 37.7718982), which sits ~65 m NE of the footprint center near
the tower — using it would shift the whole building off its real footprint.
`targetHeightM` 43.9 is the Hamon tower top (144 ft), which is also the
model's exact Z extent, so the loader's height-based scale factor is 1.0.
The anchor is the WGS84 position of the recentred bounding-box origin,
printed deterministically by the build script.

## Scope confirmation

No sculpture garden, park planting, Music Concourse, Academy of Sciences,
paths, trees, people, vehicles, plinth, studio background, camera or light is
present in the GLB. Temporary studio elements exist only inside the render
script and are never exported.

## Integration pointer (separate job)

Integration follows `docs/asset-plans/INTEGRATION-PROMPT.md` plus the notes in
`docs/asset-plans/de-young.md` §2.13: this is a **new** landmark (no existing
procedural builder), so it needs a `pipeline/lib/landmarks.mjs` entry
(`id: 'deYoung'`, exclusion radius ~100 m) and a re-bake, with manifest id
`de-young` mapping to `deYoung`. Verify the in-app footprint after placement:
scaling keys off the 44 m tower, and most of the asset is 13 m low.
