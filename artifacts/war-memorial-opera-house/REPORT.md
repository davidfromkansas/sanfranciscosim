# War Memorial Opera House — build report

Deliverable: `war-memorial-opera-house.glb` — a validated toy-diorama miniature of the
War Memorial Opera House (301 Van Ness Avenue), authored per
`docs/styles/miniature-toy.md` (artistic gate) and
`.agents/skills/sf-asset-check/SKILL.md` (technical gate). Research dossier:
`REFERENCE.md`. Built LOCALLY only — nothing committed, no app code touched.

## Files

| File | What |
|---|---|
| `build_war_memorial_opera_house.py` | Deterministic build (headless Blender; local run used Blender 5.2 at `/Applications/Blender.app/Contents/MacOS/Blender`, no GPU) |
| `war-memorial-opera-house.blend` / `.glb` | Source scene and the shipped export |
| `render_war_memorial_opera_house.py` | Review renders — always re-imports the exported GLB |
| `validate_war_memorial_opera_house.py` → `validation.json` | Fresh-scene re-import contract validation |
| `war-memorial-opera-house-{north,east,south,west,top,aerial,night,night-east,contact-sheet}.png` | Review set (one shared ortho rig for the four elevations) |

## Validated result (fresh-scene re-import of the GLB)

- **PASS** — see `validation.json` (all checks; per-object signed-volume normals
  gate authoritative, supplementary 22,500-ray visibility test within the
  documented 0.1% union-of-solids tolerance).
- **222 objects, 9,696 triangles** (budget 18,000), dims **113.97 × 77.69 × 44.00 m**
  (world-axis AABB of the rotated building), min-z 0, centred.
- Materials (all palette, flat, textureless, opaque): `Toy_stone`, `Toy_sand`,
  `Toy_trim`, `Toy_glass`, `Toy_ink`, `Toy_roofd`, `Toy_steel`,
  `Toy_mustard_Glow`, `Toy_white_Glow`. Glow ships with emission 0 (night pass
  is the app's).

## Orientation & placement (for the future integration job)

- **Authored world-true**: auditorium axis bears **81.11° cw from true north**
  (OSM way/32865161 long edges); the colonnade front faces east onto Van Ness.
  The loader (`placeGeneric`) applies no rotation — none is needed.
- **Anchor (recomputed, use this): `-122.4209170, 37.7786126`** — the WGS84
  point under the exported bbox CENTRE (includes the 3.4 m front steps, which
  is why it differs from the raw footprint centre). The plan doc's anchor
  (−122.4206423, 37.7785955) is ~26 m ENE of the footprint centre and would
  push the model into Van Ness Avenue — do not use it.
- `targetHeightM` **44** = the fly-tower summit (OSM `height`), which is the
  exported max-z, so the loader's scale lands at exactly 1.00.

## Design decisions (vs the plan doc)

- **Corrections applied from research** (details in REFERENCE.md): long axis is
  E–W not N–S; front colonnade is **7 open loggia bays separated by 8 PAIRS of
  columns** (Louvre scheme, per Wikipedia/structurae/photos) rather than "10
  columns"; the roofline is **not flat** — the real aerial signature is steep
  dark hipped roofs (front hip with court-facing skylights, auditorium attic
  hip, 44 m fly-tower cap), so those replace the plan's flat `Toy_roofd` planes.
- Four-part massing from the footprint polygon: 48.6 m front pavilion,
  full-width (73.3 m) wings with curved reentrant quadrants, 56 m auditorium
  block, 48 m rear service block; fly tower ~40 × 20 m straddling the
  stage line (position inferred from photos — not mapped in OSM).
- Facade formula per the style bible §22: rusticated `Toy_stone` basement with
  7 arched entrances + marquee'd Grove St flank; giant-order paired columns on
  pedestals; one unbroken entablature/cornice line at 24.5 m; attic parapet
  with inset panels; arched windows in a regular rhythm on every visible
  elevation (8 per auditorium flank, 2 per wing face, 1 per pavilion flank).
- **Night state** (per the app's dusk system — glow shells only, never primary
  surfaces): `Toy_mustard_Glow` lit panes 5 cm behind-proud of every arch
  (7 ground + 7 loggia + 26 flank/wing/pavilion windows) and one thin
  `Toy_white_Glow` soffit strip under the entablature as the colonnade
  floodlight cue. Matches the real night lighting (floodlit colonnade, warm
  lobby glow). Rear service windows deliberately stay dark.
- Heights between the two OSM tags (fly tower 44, twin Veterans parapet 28)
  are proportioned from photographs: base course 9.5, shafts 10.7–20.3,
  cornice 23–24.5, front attic 27, front hip to 31, attic block 24.5–30 with
  hip to 33.5, fly-tower walls to 40.5. Marked *inferred* — no published
  section drawing was found.

## Draft manifest entry (do NOT apply in this task)

```json
{
  "id": "opera-house",
  "file": "war-memorial-opera-house.glb",
  "anchor": [-122.4209170, 37.7786126],
  "targetHeightM": 44,
  "cat": 17,
  "name": "War Memorial Opera House",
  "estimated": false,
  "dims": [113.967, 77.687, 44.0],
  "tris": 9696
}
```

## Integration notes (from the plan §2.13, unchanged)

- New landmark: needs a `pipeline/lib/landmarks.mjs` entry (`id: 'operaHouse'`,
  `exclude: ~90`) and a re-bake; manifest id `opera-house` ↔ `operaHouse`.
- The near-identical Veterans Building (way/32865757, 28 m) stays procedural —
  after integration, check the pair still reads as twins from the app camera;
  flag if jarring rather than modelling both.
- The model includes its own front steps; the memorial court, trees and
  streetscape are app-side.

## QA per the task prompt

| Item | Status |
|---|---|
| Fresh-scene re-import validation (not the authoring scene) | PASS (`validation.json`) |
| min-z ≈ 0, XY centred | PASS (0.0 / 0.0, 0.0) |
| Real-metre dims consistent with research | PASS |
| ≤ 18,000 triangles | PASS (9,696) |
| Materials `Toy_*`, flat, no textures/alpha, no `Toy_body` | PASS |
| `_Glow` only on night-lit surfaces, emission 0 | PASS |
| No cameras/lights/animations/armatures/constraints | PASS |
| Transforms applied, no negative scales, outward normals | PASS |
| No foreign/leaked geometry | PASS (fresh factory scene build) |
| 5 controlled views + aerial + night + contact sheet from the exported GLB | PASS |
| Committed | **NOT COMMITTED — per instruction, local review only** |
