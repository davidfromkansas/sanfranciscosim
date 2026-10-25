# 181 Fremont — asset report

## Result

**PASS** — `181-fremont.glb` meets the landmark contract: the kit validator (`tools/landmark-kit/validate.py`,
Blender 5.2.3 LTS) re-imported only the exported GLB into a fresh scene and printed "all checks pass".
`validation.json` is the machine-readable authority. Not yet integrated (the batch is integrated in one pass).

## Deliverables

- `build_181_fremont.py`, `181-fremont.glb`, `181-fremont.blend`
- `validate_181_fremont.py` → `validation.json`; `render_181_fremont.py` → 7 renders + `181-fremont-contact-sheet.png`
- `REFERENCE.md`; plan at `docs/asset-plans/181-fremont.md`

## Contract results

| Check | Value |
|---|---|
| Triangles | 3,346 / 27,000 |
| Dimensions | 50.43 × 50.43 × 244.4 m |
| Min Z | 0.0 |
| XY centre offset | [0.0, 0.0] |
| Crest | 244.4 m (target 244.4) |
| Materials | flat `Toy_*`, roughness 0.85, opaque, no textures |
| Normals, volume, glow facing, degenerates | pass |

Anchor **-122.3953090, 37.7897660**, category `3`.

## Night state

Glow skins over solid geometry: `Toy_red_Glow`, `Toy_sand_Glow`, `Toy_white_Glow`.

## Iterations and notes

- Braces rebuilt as stacked X braces on every face (a tall diamond round each corner), per the photo; the draft had one 'A' per face.
- Lit panes hidden behind braces and mullions removed (glow-outward check was failing); window density raised to 0.5.
- Inferred: crown slope, roof heights (206–220 m) and the two faces the photo does not show.

## Gate 3 — approval

Approved by David on 2026-10-25 (contact sheets sent in four batches of five): "approve all".

## Stage 4 — optimize

Shipped as `app/public/sf-assets/landmarks/181-fremont.glb`, meshopt-compressed with the intake flags of `pipeline/compress-assets.mjs` (`gltfpack -c -km -kn -noq`): **167 KB → 85 KB** (49% smaller). Geometry is unchanged. The kit merges every landmark into one body mesh and one glow mesh, so the Phase B cleanup in `tools/glb-optimize/` finds nothing to join or weld; a trial run saved 0 triangles and grew the file 1–5%, so it was not applied. The limited dissolve is skipped as GLB-OPTIMIZE-PROMPT §3 step 3 requires for assets with ring bands and parapets. Gate G3 (three.js GLTFLoader round-trip with MeshoptDecoder, `tools/glb-optimize/g3check`) passes.
