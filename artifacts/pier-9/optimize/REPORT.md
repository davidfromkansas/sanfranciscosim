# Pier 9 — optimize report (stage 4)

`GLB-OPTIMIZE-PROMPT.md` v2 run against `artifacts/pier-9/`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS (headless), `npx gltfpack@0.24`, node + `three@0.185.1`
(`g3check/`), python3 + Pillow, gzip. Scripts copied from `tools/glb-optimize/` via the
pier-1 run and re-used unchanged except for arguments.

## Metrics

| | input | shipped |
|---|---|---|
| Raw bytes | 937,716 (915.7 KB) | **290,000 (283.2 KB)** |
| Gzip-9 bytes | 131,431 | 140,511 |
| Objects | 675 | 16 |
| Draw submeshes (primitives) | 680 | **19** |
| Triangles | 11,820 | 11,788 (weld dropped 32 degenerate slivers) |
| Vertices | 23,504 | 23,091 as re-expanded on import |
| Materials | 13, three `_Glow` | identical set |
| bbox dims / min Z | 235.2816 × 188.4245 × 17.6 / −2.6 | identical |

**69.1 % smaller raw**, against a 60 % target; well under the 500 KB intake cap. Gzip
rises 9 KB — expected: meshopt output is already entropy-coded.

## Judgment calls

- **Limited dissolve SKIPPED** (`DISSOLVE = False`), same reasoning as pier-1: the deck
  slab, monitor, plinth ring and coping are long coplanar bands; a strict dissolve
  re-triangulates them into metre-long micro-slivers that pass area tests and fail the
  stage-2 validator only after the shipping swap.
- **Packing**: `gltfpack -c -km -kn -noq`. `-km` keeps the three `_Glow` materials
  separate (the night layer is name-keyed); `-noq` is the repo standard.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (13, `Toy_glass_Glow` / `Toy_glassl_Glow` / `Toy_amber_Glow` all separate); no `Toy_body` |
| G2 Geometry | **PASS** | bbox and origin identical to 1e-4 m; all volumes positive; 0 / 22,500 flipped rays |
| G3 Round-trip | **PASS** | `g3check` (pinned three 0.185): `{"ok":true,"meshes":19,"tris":11788}`, correct bbox |
| G4 Appearance | **PASS** | worst mean 0.33 % (night far), best 0.0019 % (elev W); gates ≤ 2 % far / ≤ 4 % near |
| G5 Draw submeshes | **PASS** | 680 → 19 |
| G6 Size | **PASS** | −69.1 % raw vs 60 % target |
| Stage-2 revalidation on the SHIPPED file | **PASS** | `validation.json` regenerated from `pier-9.glb` post-swap |

## One validator adaptation, recorded

The per-material join renames the merged lamp-globe object to `Toy_amber_Glow`, which
routed 576 closed-sphere faces into the validator's open-strip ray test (160 deck-facing
sphere faces can never be "first hit from outside along the normal", so the shipped file
briefly read FAIL). The globes are **closed by design** — they are the light source, not
a glow shell over an opaque surface — so `validate_pier_9.py` now routes amber-glow
objects to the signed-volume test and keeps the strip test for the true open strips
(36 / 36 outward). The next pier that ships glowing lamp globes will hit the same thing.
