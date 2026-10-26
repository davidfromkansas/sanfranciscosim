# 450 Sutter Street (Four Fifty Sutter Building) — build report

Miniature GLB for SF-SIM, Financial District batch (stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode), built 2026-10-26 from
`docs/asset-plans/450-sutter-street.md` with the shared kit in `tools/landmark-kit/`.

## Result

Validation **PASS** ("all checks pass", run with `--budget 5000`). 4,172 triangles.
Crest 105.0 m = target height — published roof 105 m / 344 ft (Wikipedia, Emporis 118820); DataSF LiDAR max 103.3 m, majority 95.0 m, median 88.5 m.

## Deliverables

- `build_450_sutter_street.py` — deterministic build (`blender -b --python build_450_sutter_street.py`)
- `450-sutter-street.glb`, `450-sutter-street.blend`
- `validate_450_sutter_street.py` → `validation.json`; `render_450_sutter_street.py` → renders below
- Renders: `450-sutter-street-aerial-night.png`, `450-sutter-street-aerial.png`, `450-sutter-street-contact-sheet.png`, `450-sutter-street-east.png`, `450-sutter-street-north.png`, `450-sutter-street-south.png`, `450-sutter-street-top.png`, `450-sutter-street-west.png`
- `REFERENCE.md` (sources, dimensions, cues, uncertainties)

## Contract (from validation.json, fresh-scene re-import)

| | |
|---|---|
| Triangles | 4,172 |
| Dimensions | 55.4222 x 58.9497 x 105.0 m (world-axis bbox) |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| Objects | 2 |
| Materials | Toy_bronze, Toy_cream, Toy_glassd, Toy_leaf, Toy_leafd, Toy_roofd, Toy_rust, Toy_sand_Glow, Toy_stone, Toy_terracotta, Toy_white_Glow |
| Anchor | [-122.4078718, 37.7896331] |

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

- Podium: the true OSM polygon (13 nodes), 0–7.5 m terracotta, arched bronze openings + lit arches on the Sutter face, cream band.
- Sutter wing 40.8 × 18.2 m and rear wing 40.4 × 17 m (local frame, yaw 8.6°): `tk.shaft` with dark glass and recessed terracotta spandrels, 24 / 21 storeys at 3.646 m.
- `tk.pier_grid` cream piers every 3 m, 0.85 m deep, running 1.8 m past each roof; 6-sided terracotta corner drums (rounded corners).
- Link 24 × 5 m between the wings (light courts E and W); central block 15 × 9 m to 101.5 m with piers, windows, a crown light band and a cap to 105 m.
- Roofs: terracotta parapet ring and a dark deck raised 0.1 m clear of the glass cap.

All materials are flat `Toy_*` (roughness 0.85, no textures, no alpha). Off-palette: `Toy_terracotta`, `Toy_glassd`, `Toy_bronze` (kit EXTRA_HEX).

## Night state

Scattered lit office panes on the outer faces of both wings (30%), lit Sutter arches, lit windows and a white crown band on the central block. Glow materials: `Toy_sand_Glow`, `Toy_white_Glow`; all laid as thin outward skins over solid faces (705 of 706 glow faces unobstructed outward).

## Iterations

- v1: 4,910 tris — bevelled podium and a punched-window link dropped (4,428); glow check failed (47 lit panes hidden inside piers and the link) — panes moved in front of the piers and the faces toward the link left unlit.
- v1 render: the central block floated over the light courts in the W/N elevations; v2 runs it down onto the link with windows: 4,172 tris, all checks pass.

## Gate 3 — approval

Approved by David on 2026-10-26 (renders sent as twelve day/night overview sheets): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/450-sutter-street.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **207 KB → 97 KB** (53% smaller). Geometry is unchanged. Kit assets are already one body mesh and one glow mesh, so the Blender cleanup pass and the limited dissolve are skipped, as for the Transbay batch. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
