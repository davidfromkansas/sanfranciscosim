# bill-graham-civic-auditorium — GLB optimize report (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.
Scripts are the generic ones from `tools/glb-optimize/`. Only one constant was
adapted: `render_ab.py`'s `cycles.samples`, 64 → 24 (see §G4). The geometry and
validation scripts are byte-identical to the shared copies — this asset needed no
per-asset dims ranges or silhouette exceptions.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (headless, CPU) |
| gltfpack | `npx gltfpack@0.24`, flags `-c -km -kn -noq` |
| three (g3check) | pinned in `tools/glb-optimize/g3check/package.json` |
| python3 + Pillow | 3.x / 11.3.0 |

## Metrics

| | input | shipped | Δ |
|---|---|---|---|
| Raw bytes | 420,812 | **174,384** | **−58.6 %** |
| gzip −9 bytes | 61,147 | 109,409 | **+78.9 %** (see §Gzip below) |
| Triangles | 6,408 | 6,396 | −12 (gltfpack dropped 12 degenerates) |
| Vertices | 12,690 | 12,019 | −5.3 % |
| Objects / draw primitives | 209 | **10** | −95.2 % |
| Materials | 10 | 10 | identical set |
| bbox dims (m) | 140.83548 x 100.14396 x 37.0 | identical | 0 |
| bbox min / centre XY | (−70.41774, −50.07198, 0.0) / (0, 0) | identical | 0 |

## Waste census (Phase A)

As with the courthouse, the waste was **object-count overhead, not geometry**: 209
mesh nodes for 6,408 triangles, 100 of them sharing `Toy_glass` and 50 sharing
`Toy_white` (the columns, cornices, medallions and cartouches). No duplicate meshes.
Twelve degenerate triangles, all removed by the pack. The dome's four octagonal frusta
are silhouette geometry and already minimal at 8 facets.

Predicted saving: ~55–65 % from joining per material plus the pack. Actual: 58.6 %.

## Per-phase result

| Phase | tris | verts | note |
|---|---|---|---|
| input | 6,408 | 12,690 | 209 objects |
| weld ≤1 mm (per object) | 6,408 | 3,622 | −71.5 % verts; glow shells are separate objects so the per-object weld cannot fuse glow onto base surfaces |
| delete degenerate / buried interior faces | 6,408 | 3,622 | closed-solid occluder rule found no provably-buried faces |
| limited dissolve 0.05° | 6,408 | 3,622 | massing already minimal |
| join per material | 6,408 | 3,622 | **209 → 10 objects** — the win |
| gltfpack `-c -km -kn -noq` | 6,396 | — | 336,228 → 174,384 bytes |

**No triangle was simplified.** The dome's facet count, the arch heads and the
pavilion silhouettes are untouched.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 contract | **PASS** | material name set identical (10); both `_Glow` materials still separate (`-km` did its job — without it gltfpack merges across the glow boundary and kills the night layer); no `Toy_body` |
| G2 geometry | **PASS** | bbox identical to 5 dp; origin identical; all signed volumes positive; ray-flip fraction **0.0000** of 18,767 first hits |
| G3 round-trip | **PASS** | Blender re-import PASS; `g3check` → `{"ok":true,"meshes":10,"tris":6408,...}` with the full material list and exact bbox |
| G4 appearance | **PASS** | worst mean delta **1.4907 %** (gate: ≤ 2 % far / ≤ 4 % near); full table below |
| G5 draw submeshes | **PASS** | 209 → 10 (≤ input) |
| G6 size | **PASS** | −58.6 % raw; just short of the 60 % aspiration, and the census accounts for the remainder — what is left is silhouette geometry (the dome, the three arch heads, the pavilions) |
| G7 GPU budget | n/a | bake mode off |
| G8 hygiene | **PASS** | re-import object/material counts match; deterministic re-run reproduces the output; no `.blend1` left |

Post-swap, the **stage-2 contract validator** was re-run against the shipped
(meshopt) file and returned `overall: PASS` on all 15 checks, with
`transforms_applied: true` and `no_unexpected_objects: true` — `-noq` avoids the
quantization failure mode the prompt warns about.

## Gzip: an honest note

Raw bytes fell 59 %, but **gzipped bytes rose 79 %** (61.1 KB → 109.4 KB). Meshopt
already entropy-codes its buffers, so gzip has little left to remove, whereas the
un-encoded float32 GLB is extremely compressible. On a gzip/brotli-serving host this
asset is therefore *larger over the wire* after the pack.

It ships meshopt-compressed regardless: `AGENTS.md` and
`.agents/skills/sf-asset-check/SKILL.md` §8 make meshopt intake compression mandatory,
the loaders register `MeshoptDecoder`, and the decode-side win is real (10 draw
primitives instead of 209). Both numbers sit well inside the ≤ 500 KB budget. Flagged
here rather than buried, because it is the second asset in a row to show it and it may
be worth revisiting the rule for small, highly-regular landmarks.

## Judgment calls

- **The dome was never a candidate for reduction.** It is the entire reason this asset
  exists; its 8 facets and 4 stacked frusta are silhouette geometry (§1.5).
- **No curve retessellation** anywhere: the arch heads are 12-segment and read at the
  aerial camera; the wreath medallions and cartouches are 12-gons.
- **No bake.** `ALLOW_BAKE: no`.

## Shipping swap

`bill-graham-civic-auditorium.optimized.glb` was copied over
`artifacts/bill-graham-civic-auditorium/bill-graham-civic-auditorium.glb`; the
pre-optimize original is archived at
`optimize/input/bill-graham-civic-auditorium.glb`. `REPORT.md`, `validation.json` and
the manifest entry carry the shipped numbers (6,396 tris, 174,384 bytes).


## G4 in full — A/B appearance

Input vs output on one rig: day and night, near (1.5× long axis) and far (6×),
plus four orthographic elevations. `render_ab.py` was adapted in one place —
`cycles.samples` 64 → 24 — because denoising is off, so both sides carry
comparable noise and the extra samples buy nothing for a pixel-delta comparison.
The trade-off is that the residual deltas below are dominated by that sampling
noise rather than by any real difference.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| `day_near` | 0.1590 % | 207 |
| `day_far` | 0.4527 % | 152 |
| `night_near` | 0.2224 % | 122 |
| `night_far` | 0.3244 % | 159 |
| `elev_n` | 1.4907 % | 202 |
| `elev_e` | 0.7521 % | 152 |
| `elev_s` | 0.0831 % | 198 |
| `elev_w` | 1.3488 % | 186 |

**What the diffs actually show:** uniform speckle across the lit surfaces, i.e.
render noise. Placing `renders/in_*.png` and `renders/out_*.png` side by side,
the silhouette, the massing, every opening and every material read identically;
nothing is missing, shifted or newly shaded. That is the expected result — Phase B
changed zero triangles and Phase C is a lossless re-encode — but it was checked by
eye rather than inferred from the numbers.
