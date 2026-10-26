# San Francisco Marriott Marquis — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-26 from
`docs/asset-plans/marriott-marquis.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,820 triangles.
Crest 133.0 m = target height — published 132.89 m / 133 m (Wikipedia infobox / text; OSM `height=133`). DataSF 2010 LiDAR max 128.14 m over the whole complex (measured, the vault top is thin).

## Deliverables

- `build_marriott_marquis.py` — deterministic build (`blender -b --python build_marriott_marquis.py`)
- `marriott-marquis.glb`, `marriott-marquis.blend`
- `validate_marriott_marquis.py` → `validation.json`; `render_marriott_marquis.py` → renders below
- Renders: `marriott-marquis-aerial-night.png`, `marriott-marquis-aerial.png`, `marriott-marquis-contact-sheet.png`, `marriott-marquis-east.png`, `marriott-marquis-north.png`, `marriott-marquis-south.png`, `marriott-marquis-top.png`, `marriott-marquis-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,820 |
| Dimensions | 149.4689 x 157.2098 x 133.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_glassd, Toy_glassg, Toy_glassl, Toy_ink, Toy_leaf, Toy_roofd, Toy_rust, Toy_sand, Toy_sand_Glow, Toy_sky_Glow, Toy_steel, Toy_stone, Toy_white_Glow |
| Anchor | [-122.40448, 37.7853374] |

| Check | Result |
|---|---|
| Crest = target height | PASS |
| Plausible metre dimensions | PASS |
| Base at Z 0 | PASS |
| Centred in XY | PASS |
| Triangle budget (batch cap) | PASS |
| No image textures | PASS |
| No transparency | PASS |
| Flat `Toy_*` materials | PASS |
| Has night glow | PASS |
| No cameras / lights | PASS |
| No animation / skin / constraints | PASS |
| Transforms applied | PASS |
| No negative scales | PASS |
| Normals outward (signed volume) | PASS |
| Normals outward (ray residual) | PASS |
| Glow skins face outward | PASS |
| No degenerate geometry | PASS |
| No unexpected objects | PASS |

## Geometry and materials

- Podium: `tk.ccw` of the OSM outer ring, `Toy_sand`, 0–23.6 m; dark deck; the podium court as an `Toy_ink` well; panes and a lit lobby band on the 4th, Mission and Jessie Square faces.
- Tower hub 20 × 22 m, `Toy_stone`, 23.6–116.6 m (30 storeys of 3.1 m) on yaw = bearing 45°.
- Four wings: SW 5 terraces (26/22/18/14/10 storeys), NE (28/24), NW (27/23), SE (26/21); each terrace a stone prism whose top storey is an inset `Toy_glassg` greenhouse box.
- Fan windows (`Toy_glassg`, narrow foot, semicircular head, ~7 m wide × 9 m) on every terrace end face, with a smaller `Toy_sky_Glow` fan over each.
- `Toy_glassd` 2.2 m slots up the four re-entrant corners.
- Crown: `Toy_glassg` box 116.6–124.6 m with a white lit band; glass barrel vault (r 8.4 m, axis NW–SE) to 133.0 m with white-lit fan ends.
- Punched `Toy_glassd` windows one per 5 m per storey on every exposed stone face; scattered lit panes.
- Plant cluster on the podium roof, sidewalk on 4th and Mission, three street trees on 4th.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_glassg`, `Toy_glassd` (documented in the kit).

## Night state

Lit lobby frontage (75%), scattered lit rooms (22–28%), sky-blue fan windows on every terrace, a white band round the crown box and white-lit fan ends on the vault. Glow materials: `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (911 of 927 glow faces unobstructed outward).

## Iterations

- Draft: 6,210 tris (over the 5,000 cap). Window spacing 3.8 to 5 m, podium panes 6 to 8 m, terrace sill bands and the podium parapet dropped, one plant cluster. 4,820 tris, PASS first validation.
- Renders accepted: cross, terraces, fans, slots and the vault read in day and night views.

## Gate 3 — approval

Pending: renders sent to David.
