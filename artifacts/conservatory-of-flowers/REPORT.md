# Conservatory of Flowers asset report

## Result

**PASS** — `conservatory-of-flowers.glb` meets the repository's landmark contract and
was validated after fresh-scene re-import in Blender 5.2.0 LTS. Not integrated:
per the task, no app code, production manifest or pipeline data was touched.
Integration is a separate job (`docs/asset-plans/INTEGRATION-PROMPT.md` plus the
notes in `docs/asset-plans/conservatory-of-flowers.md` §2.13 — this is a NEW
landmark and needs a `pipeline/lib/landmarks.mjs` entry + re-bake).

The exact exported GLB was re-imported before all seven review renders were
produced. `validation.json` is the machine-readable authority for the metrics
below.

## Deliverables

- `REFERENCE.md` — research dossier and design decisions
- `build_conservatory_of_flowers.py` — deterministic model build/export script
- `render_conservatory_of_flowers.py` — fresh-GLB controlled render script
- `validate_conservatory_of_flowers.py` — isolated re-import validator
- `make_contact_sheet.py` — contact-sheet composer
- `conservatory-of-flowers.blend` — reproducible authoring scene (asset only)
- `conservatory-of-flowers.glb` — final binary deliverable (~830 KB)
- `validation.json` — full object-level machine report
- `conservatory-of-flowers-{north,east,south,west,top,aerial,night}.png`
- `conservatory-of-flowers-contact-sheet.png`

Rebuild from this directory with (Blender binary on PATH as `blender`; on this
machine `/Applications/Blender.app/Contents/MacOS/Blender`):

```bash
blender -b --python build_conservatory_of_flowers.py
blender -b --python validate_conservatory_of_flowers.py
blender -b --python render_conservatory_of_flowers.py
python3 make_contact_sheet.py
```

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | ~830 KB self-contained `conservatory-of-flowers.glb` |
| Plausible real-world meters | PASS | 78.80 × 30.94 × 18.30 m axis-aligned bounds; the structural length is 75.8 m along the wings and the bounds grow because the measured 81° heading (a 9° yaw) is baked in |
| Origin / base | PASS | bounding-box min Z 0.0 m; XY centre offset [0.30, −1.20] m (the dome axis is the origin; the offset is the south vestibule + E-plan step, matching the real plan) |
| Orientation, front faces −Y | PASS | authored +Y = true north; long axis baked at the measured 81° cw bearing; the south vestibule's outward normal is (0.156, −0.988), within 9° of −Y |
| Triangle budget (≤ 24,000) | PASS | 13,814 triangles |
| Applied transforms | PASS | all 298 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | 0 invalid/non-unit loop normals; 0 flipped visible first-hits across 30,000 deterministic visibility rays (27,274 hits) |
| Unexpected / leaked geometry | PASS | 298 mesh objects only; no studio plane, context, camera or light in the GLB |
| Image textures / PBR maps | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque |
| Flat material contract | PASS | seven `Toy_*` materials from the project palette; roughness 0.85; no `Toy_body` |
| Glow naming | PASS | `Toy_white_Glow` only on thin night shells over the rotunda, lantern and end-pavilion domes; `Toy_gold_Glow` only on the entry transom; wings stay dark |
| Cameras / lights / animations / armatures / constraints | PASS | 0 / 0 / 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets then imports only the final GLB; the render script independently repeats that isolation |

## Geometry and materials

- Object count: **298 mesh objects**
- Triangle count: **13,814** (budget 24,000)
- Dimensions: **[78.799, 30.9373, 18.30] m** (axis-aligned, heading baked)
- Bounding box min: **[−39.1023, −16.671, 0.0] m**
- Bounding box max: **[39.6967, 14.2663, 18.30] m**
- Minimum Z: **0.0 m**
- XY centre offset: **[0.2972, −1.2023] m**
- Materials: `Toy_brick` (plinth), `Toy_white` (ribs/frames/knee walls),
  `Toy_trim` (cresting, cupolas, finials, lantern), `Toy_glassl` (all glazing),
  `Toy_glass` (entry doors), `Toy_white_Glow` (night shells: great dome,
  clerestory, lantern, both end-pavilion domes), `Toy_gold_Glow` (entry
  transom lamp)

## Orientation decision (recorded per the task prompt)

The model is authored with Blender +Y = true north and the real-world heading
baked in: the wings' long axis sits at the **measured 81.0° cw from true
north** (PCA over the 58 OSM footprint nodes of way/30675038), implemented as a
+9° yaw of the authoring axes. The loader (`placeGeneric` in
`app/src/assets.js`) applies no rotation, so the building drops onto its real
alignment. The entrance vestibule projects from the south face toward JFK
Drive; its outward normal is 9° off −Y, which satisfies the front-faces-−Y
rule without any loader-side correction.

## Visual design

The miniature preserves the five cues ranked in `REFERENCE.md`: the ribbed
great dome on its two-tier pedestal (drum → ribbed skirt roof with S/E/W
dormers → gallery → clerestory → 16-rib dome → lantern + finial at exactly
18.30 m); strict bilateral symmetry with octagonal domed end pavilions and
ogee cupolas; a dense fattened white rib rhythm (1.6 m pitch, 0.36 m ribs —
deliberately oversized so it survives the city camera); the gabled south
vestibule with projecting porch; and Victorian cresting teeth plus ridge
ventilator monitors along the wing ridges. The raised masonry base is kept as
a red-brick plinth (`Toy_brick`) following a simplified E-plan outline.

Documented deviations from the plan dossier (reasons in `REFERENCE.md`): the "6 barrel ridge turrets" became cresting + 2 ventilator
monitors per wing (what the HABS photos actually show); the anchor is moved
~4.9 m from the plan's footprint centroid to the dome axis; the rear modern
service boxes are excluded, so the model's depth (≈27 m structural) is
intentionally less than the raw 35.6 m OSM bounding depth. Flower beds, the
formal parterre, the terrace stair and JFK Drive are excluded — park data
supplies planting (plan §2.10).

The review elevations share one orthographic rig (same scale, 1500 × 700
resolution, lighting, exposure); the top view shows the dome ribs, vault
roofs, vents and cresting; the aerial render uses a 38°-down, 105 mm
restrained-perspective camera per the style bible; the night render previews
the dusk system with the same aerial camera.

## Night state (how it works)

The asset does not decide when it is night — the app does. `_Glow` materials
are split out by the loader (`app/src/assets.js`) into one merged unlit
`MeshBasicMaterial` layer flagged `nightOnly`; `updateLandmarkGlow`
(`app/src/kit.js`) drives that layer's opacity as `0.12 + 0.95 * uNight`.
`uNight` comes from the real-time sky (`app/src/env.js`): the app computes the
actual sun elevation over San Francisco from the live SF wall clock and ramps
`uNight` from 0 (sun on the horizon) to 1 (sun 10° below) — so the glow
ignites through dusk automatically, every real evening, with no per-asset
logic. QA: pin the clock from the console with `SF.setClock(...)` (see
`.agents/skills/testing-sf-3d/SKILL.md`).

Because glow surfaces live ONLY in that night layer (12 % opacity by day), the
primary glazing stays opaque `Toy_glassl` and the night state is carried by
**thin shells riding 3–5 cm proud of the glazing**: the great dome, the
clerestory band, the lantern and both end-pavilion domes in warm `Toy_white_Glow`
(the white ribs stand further proud, so they read as dark silhouette lines over
the lit glass — the classic lit-glasshouse look), plus a `Toy_gold_Glow`
transom lamp over the entrance doors. The wings and rear lean-to stay dark for
contrast, per the plan. Every shell edge is buried inside a solid band so the
30,000-ray normals gate stays at zero flipped faces. The review renders mimic
both app states: day passes render the glow layer at the app's 12 % daytime
opacity; the night pass lights it emissively under a moonlit sky
(`conservatory-of-flowers-night.png`).

## Draft manifest entry (do not apply in this task)

The anchor below is the **dome axis** computed from the OSM footprint
(centroid moved to the vestibule/dome axis), because the model's origin is the
dome axis and the raw centroid is skewed ~4.9 m ESE by the asymmetric rear
service rooms. If integration prefers the plan's centroid anchor
(−122.4601775, 37.7725877), the dome lands ~5 m east-southeast of true.

```json
{
  "id": "conservatory-of-flowers",
  "file": "conservatory-of-flowers.glb",
  "anchor": [
    -122.4602321,
    37.7725965
  ],
  "targetHeightM": 18.3,
  "cat": 16,
  "name": "Conservatory of Flowers",
  "estimated": false,
  "dims": [
    78.799,
    30.9373,
    18.3
  ],
  "tris": 13814
}
```

The model's bounding-box top is exactly 18.30 m, so the loader's
`targetHeightM / measuredHeight` scale is exactly **1.0** — the console merge
line must show `uniform x1.00`; any other factor means a stale height was
used somewhere.
