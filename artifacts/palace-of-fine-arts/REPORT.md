# Palace of Fine Arts asset report

## Result

**PASS** — `palace-of-fine-arts.glb` meets the repository's landmark contract
and was validated after fresh-scene re-import in Blender 5.2.0 LTS (all 14
automated checks green; `validation.json` is the machine-readable authority
for every metric below). Per the task instructions nothing was committed or
integrated: the deliverables live in `artifacts/palace-of-fine-arts/` in the
working tree, the production manifest and app code are untouched, and
integration remains a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md` + the integration notes in
`docs/asset-plans/palace-of-fine-arts.md`).

**Scope amendment (owner directive, 2026-08-10):** after the architecture-only
asset passed, David directed inclusion of the surrounding water and garden in
the same GLB ("option A"), with swans. The asset now also contains the
OSM-traced lagoon with stone shore rims, a lawn plate, 26 grouped toy trees,
8 shrub masses and 3 swans — see "Grounds" below and the matching section in
`REFERENCE.md`. This supersedes the original task prompt's exclusion of the
lagoon and vegetation.

## Deliverables

- `REFERENCE.md` — research dossier and design decisions
- `osm-footprint-trace.png` — the surveyed OSM geometry plotted in the local
  frame (the placement ground truth the model was traced from)
- `build_palace_of_fine_arts.py` — deterministic model build/export script
- `render_palace_of_fine_arts.py` — fresh-GLB controlled render script
- `validate_palace_of_fine_arts.py` — isolated re-import validator
- `make_contact_sheet.py` — contact-sheet composer
- `palace-of-fine-arts.blend` — reproducible authoring scene (asset only)
- `palace-of-fine-arts.glb` — final binary deliverable (1.33 MB, architecture + grounds + night glow set)
- `validation.json` — full object-level machine report
- `palace-of-fine-arts-{north,east,south,west,top,aerial}.png`
- `palace-of-fine-arts-night-{aerial,east}.png` — night-state previews
- `palace-of-fine-arts-contact-sheet.png`

Rebuild from this directory with (Blender binary on PATH or the macOS app):

```bash
blender -b --python build_palace_of_fine_arts.py
blender -b --python validate_palace_of_fine_arts.py
blender -b --python render_palace_of_fine_arts.py
blender -b --python render_palace_of_fine_arts.py -- --night
python3 make_contact_sheet.py
```

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 1.33 MB self-contained `palace-of-fine-arts.glb` |
| Plausible real-world meters | PASS | 173.9495 × 258.3858 × 49.4 m overall — the surveyed crescent plus its lagoon and lawn; apex exactly the published 49.4 m |
| Origin / base | PASS | min Z 0.0 m; dome-apex (= rotunda centroid = manifest anchor) XY offset [0.0, 0.0] m |
| Anchor placement semantics | PASS (documented) | bbox center offset [38.99, 14.19] m is intentional: the lagoon extends east of the anchored rotunda, and `placeGeneric` (app/src/assets.js) drops the model ORIGIN on the anchor without recentering |
| Orientation | PASS (documented) | authored +Y = true north, +X = east, real-world heading — see "Orientation decision" below |
| Triangle budget | PASS | 21,736 / 27,000 triangles |
| Applied transforms | PASS | all 627 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | 0 invalid/non-unit loop normals; 21,912 deterministic visibility rays over nine targets, 0 flipped visible first-hits |
| Unexpected / leaked geometry | PASS | 627 mesh objects only; no studio plane, context, camera or light in the GLB |
| Image textures / PBR maps | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque (the water is opaque flat color per contract) |
| Flat material contract | PASS (2 WARN) | twelve `Toy_*` materials, roughness 0.85, no `Toy_body`; `Toy_pine`/`Toy_leaf` are off-palette vegetation greens — a contract WARN, not a fail (style bible §12: vegetation may be vivid) |
| Glow naming | PASS | `Toy_gold_Glow` on the warm floodlit surfaces (attic frieze panels, main-entablature underside ring, rotunda floor pool, dome-springing ring, colonnade underside bands, gate undersides); `Toy_white_Glow` only on the apex crown ring |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets then imports the final GLB; the render script independently repeats that isolation |

## Geometry and materials

- Object count: **627 mesh objects** (the app loader merges to ≤ 2 draw calls)
- Triangle count: **21,736**
- Dimensions: **[173.9495, 258.3858, 49.4] m**
- Bounding box min: **[−47.9837, −115.0, 0.0] m**
- Bounding box max: **[125.9658, 143.3858, 49.4] m**
- Minimum Z: **0.0 m**
- Dome apex XY offset from origin: **[0.0, 0.0] m**
- Materials: `Toy_sand` (columns, drums, entablatures, boxes), `Toy_trim`
  (capitals, cornices, maidens, urns), `Toy_stone` (terraces, shore rims),
  `Toy_ioorange` (dome), `Toy_glass` (lagoon water), `Toy_mint` (lawn,
  island), `Toy_pine` / `Toy_leaf` (tree crowns, shrubs — off-palette WARN),
  `Toy_ink` (trunks), `Toy_white` (swans), `Toy_gold_Glow` (the warm night
  floodlight set), `Toy_white_Glow` (apex crown ring)

## Grounds (scope amendment)

The lagoon is the surveyed OSM multipolygon (relation 7471537): outer ring
RDP-decimated 159→50 points, the large island kept as a hole with its own
mound, rim and three trees; the 3 m islet dropped as sub-toy-scale. Water is
an opaque flat prism, top at 0.42 m, ringed by lofted stone shore rims; where
the surveyed shoreline meets the anchored architecture, the stone plinths
rise straight from the water, as the rotunda's east base does in reality.
The lawn is a margin-offset smoothed hull of the whole composition
(designed, not surveyed). 26 trees in two silhouette species trace the real
planting pattern from the aerial photo — the screen west of both arms,
groves at the hooks and gates, east-shore specimens — with the tallest crown
at 17 m, far below the dome. Three semantically oversized swans sit on the
water east of the rotunda as the storytelling props.

## Night state (owner directive)

The glow set is designed from the night photographs (warm gold floodlighting,
melancholy-grand): `Toy_gold_Glow` on the eight attic frieze panels, a ring
band under the main entablature, an uplit floor pool inside the open rotunda
(it spills through the arches — the signature of the real night palace), a
ring at the dome springing, the continuous underside bands of both colonnade
arms, and the gate-box undersides; `Toy_white_Glow` only on the apex crown
ring, a single cooler beacon. Per contract the shipped GLB's emission
strength is 0 — the app's night pass raises it. The committed previews
(`palace-of-fine-arts-night-aerial.png`, `palace-of-fine-arts-night-east.png`,
rendered via `--night`, emission 6.0 under moonlight) show the intended look:
a warm glowing crescent doubled in a dark lagoon, dome dark with a lit rim.

## Orientation decision (required by the task prompt)

Authored with **Blender +Y = true north, +X = east** so the model drops onto
its real-world heading with the loader's rotation-free placement. The generic
"front faces −Y" rule cannot be honoured literally for this subject and is
overridden by the task prompt: the composition's principal axis is set by the
surveyed geometry. **Measured heading:** the octagon's eight piers sit at
azimuths 30° + 45k CCW from east, so the rotunda's open arch axis points
~7.5° north of due east — compass bearing ≈ **82°**, straight at the lagoon,
matching the plan's "faces the lagoon" requirement (the lagoon's mapped
centroid is due east of the anchor). The colonnade arms are traced
point-for-point from OSM ways 288371306/288371310 (not mirrored — the real
arms are asymmetric), with terminal gate boxes at the surveyed positions of
ways 288371314/288371313.

## Visual design

The miniature preserves the five cues ranked in `REFERENCE.md`: the open
octagonal rotunda silhouette with its muted red-orange dome (`Toy_ioorange` —
the composition's single saturated accent per the style bible's neutral-plus-
accent rule), the two long surveyed colonnade curves concave to the lagoon,
freestanding columns that read as separate cylinders (paired at the rotunda
piers, double rows along the arms), and the chunky entablature boxes with
blocky weeping-maiden silhouettes at their corners, looking inward. Corinthian
capitals are two-step beveled blocks; the Zimm relief band is a flat inset
panel ring that doubles as the night-glow frieze; the dome is a flat-shaded
20-segment cap whose faceting reads as the ribbed tile pattern from above; no
acanthus, coffering or figure detail below aerial legibility survives
(style bible §22 step 10: simplify again).

The four elevations share one landscape orthographic rig (identical scale,
lighting, exposure; azimuth is the only variable; compass directions are true
because the asset is authored north-up). The top view shows the dome, the
peristyle ring, both curved pergola rooflines and the terminal gates; the
aerial render uses a 38° downward, 105 mm restrained-perspective camera from
the east-southeast — the lagoon side, the composition's true front.

## Draft manifest entry (verified; NOT applied)

```json
{
  "id": "palace-of-fine-arts",
  "file": "palace-of-fine-arts.glb",
  "anchor": [
    -122.4484012,
    37.8029215
  ],
  "targetHeightM": 49.4,
  "cat": 0,
  "name": "Palace of Fine Arts",
  "estimated": false,
  "dims": [
    173.9495,
    258.3858,
    49.4
  ],
  "tris": 21736
}
```

Anchor re-verified: it is the centroid of OSM way/288371295 (the surveyed
rotunda footprint) to 7 decimal places. Height re-verified: Wikidata P2048 and
Wikipedia agree on 162 ft / 49.4 m (OSM's survey tag says 48 m; the published
figure was adopted — see REFERENCE.md). Because the model height equals
`targetHeightM`, the loader's uniform scale will be exactly 1.0 — the plan's
§2.13 concern about height-based scaling shrinking the wide plan does not
arise; the arms will land on their true coordinates.

## Scope confirmation

In the GLB (per the owner's option-A directive): the rotunda with peristyle
and attic, the dome, both surveyed colonnade arms with their terminal gate
boxes, the stone terraces, the surveyed lagoon with shore rims and island,
the lawn plate, 26 trees, 8 shrub masses and 3 swans. NOT in the GLB: the
exhibition hall (a separate OSM building already baked by the app — including
it would double geometry; the procedural landmark this asset replaces
excludes it too), the small ambiguous roof fragment way/1104852117, paths,
people, vehicles, studio floor, cameras or lights. The render studio exists
only inside the render script and is never exported.

## Integration notes (for the later, separate task)

- Manifest id `palace-of-fine-arts` maps to the procedural `palaceOfFineArts`
  (registry key `8`, exclusion 170 m); the loader hides the code-built version
  on successful load and keeps it as fallback.
- The exclusion-zone radius (170 m) is smaller than the composition's 258 m
  north–south span; check for double-drawn procedural neighbours at the arm
  ends after placement.
- **The GLB now carries its own water and vegetation.** The app also renders
  the lagoon from park/water data and bakes park trees there. At integration:
  either suppress baked trees/water inside the composition's footprint, or
  accept the overlay — the GLB water top sits at 0.42 m (above the app's
  water plane, same trick the procedural builder used), but baked trees WILL
  visibly double with the GLB's. Decide there, not here.
- The terrace and lawn bottoms sit at z 0 = the rotunda's ground; verify
  against the sampled terrain at the lagoon edge so the grounds neither
  float nor sink (plan §2.13).
