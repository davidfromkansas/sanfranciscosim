# civic-center-courthouse — GLB optimize report (stage 4)

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
| Raw bytes | 313,188 | **122,904** | **−60.8 %** |
| gzip −9 bytes | 54,202 | 81,282 | **+49.9 %** (see §Gzip below) |
| Triangles | 4,712 | 4,712 | 0 |
| Vertices | 8,868 | 8,358 | −5.8 % |
| Objects / draw primitives | 164 | **9** | −94.5 % |
| Materials | 9 | 9 | identical set |
| bbox dims (m) | 91.0774 x 51.30309 x 29.6 | identical | 0 |
| bbox min / centre XY | (−45.5387, −25.65155, 0.0) / (0, 0) | identical | 0 |

## Waste census (Phase A)

The dominant waste was **object-count overhead, not geometry**: 164 separate mesh
nodes for 4,712 triangles, 75 of them sharing `Toy_glass` and 28 sharing `Toy_trim`.
Every node carries its own accessor set and draw primitive. No duplicate meshes, no
degenerate triangles, no over-tessellated curves worth touching (the drum and dome are
8-gons already; the arch heads are 10-segment and silhouette-defining).

Predicted saving: ~55–65 % from joining per material plus the meshopt pack. Actual:
60.8 %.

## Per-phase result

| Phase | tris | verts | note |
|---|---|---|---|
| input | 4,712 | 8,868 | 164 objects |
| weld ≤1 mm (per object) | 4,712 | 2,684 | −69.7 % verts; nothing fused across the glow boundary because glow shells are separate objects |
| delete degenerate / buried interior faces | 4,712 | 2,684 | none found — the closed-solid occluder rule rejected every candidate, correctly |
| limited dissolve 0.05° | 4,712 | 2,684 | the massing is already minimal |
| join per material | 4,712 | 2,684 | **164 → 9 objects** — the win |
| gltfpack `-c -km -kn -noq` | 4,712 | — | 236,888 → 122,904 bytes |

Geometry is byte-authoritative throughout: **no triangle was simplified or removed**,
only re-encoded and re-grouped.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 contract | **PASS** | material name set identical (9); both `_Glow` materials still separate; no `Toy_body`; no manifest-named nodes to preserve |
| G2 geometry | **PASS** | bbox identical to 5 dp; origin identical; all signed volumes positive; ray-flip fraction **0.0000** of 19,450 first hits |
| G3 round-trip | **PASS** | Blender re-import PASS; `g3check` → `{"ok":true,"meshes":9,"tris":4712,...}` with the full material list and exact bbox |
| G4 appearance | **PASS** | worst mean delta **0.3297 %** (gate: ≤ 2 % far / ≤ 4 % near); full table below |
| G5 draw submeshes | **PASS** | 164 → 9 (≤ input) |
| G6 size | **PASS** | −60.8 % raw, above the 60 % target |
| G7 GPU budget | n/a | bake mode off |
| G8 hygiene | **PASS** | re-import object/material counts match; deterministic re-run reproduces the output; no `.blend1` left |

Post-swap, the **stage-2 contract validator** was re-run against the shipped
(meshopt) file and returned `overall: PASS` on all 15 checks, with
`transforms_applied: true` and `no_unexpected_objects: true` — the failure mode the
prompt warns about for quantized output does not occur, because `-noq` is used.

## Gzip: an honest note

Raw bytes fell 61 %, but **gzipped bytes rose 50 %** (54.2 KB → 81.3 KB). This is
inherent to meshopt: the encoder already entropy-codes the buffers, so gzip has almost
nothing left to remove, whereas the un-encoded float32 GLB is extremely compressible.
For this asset the meshopt build is therefore *larger over the wire* on a
gzip/brotli-serving host.

It ships meshopt-compressed anyway, because that is not a judgement call here:
`AGENTS.md` and `.agents/skills/sf-asset-check/SKILL.md` §8 make meshopt intake
compression mandatory, the loaders register `MeshoptDecoder`, and the win is real on
the GPU/decode side (9 draw primitives instead of 164, 5.8 % fewer vertices, one
buffer). Both numbers are well inside the ≤ 500 KB budget either way. Recorded here
so the trade-off is visible rather than buried.

## Judgment calls

- **No curve retessellation.** The drum, dome and oculi are the recognition cue; their
  8- and 12-segment profiles are silhouette geometry and were left alone (§3.4 permits
  the skip if it is noted — this is the note).
- **No interior-face deletion.** The asset is a union of overlapping solids; the
  closed-solid occluder rule found no provably-buried faces, and no boolean shortcut
  was taken.
- **No bake.** `ALLOW_BAKE: no`; the contract forbids textures without a recorded
  exception and nothing here justifies one.

## Shipping swap

`civic-center-courthouse.optimized.glb` was copied over
`artifacts/civic-center-courthouse/civic-center-courthouse.glb`; the pre-optimize
original is archived at `optimize/input/civic-center-courthouse.glb`.
`REPORT.md`, `validation.json` and the manifest entry carry the shipped numbers
(4,712 tris, 122,904 bytes).


## G4 in full — A/B appearance

Input vs output on one rig: day and night, near (1.5× long axis) and far (6×),
plus four orthographic elevations. `render_ab.py` was adapted in one place —
`cycles.samples` 64 → 24 — because denoising is off, so both sides carry
comparable noise and the extra samples buy nothing for a pixel-delta comparison.
The trade-off is that the residual deltas below are dominated by that sampling
noise rather than by any real difference.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| `day_near` | 0.0028 % | 17 |
| `day_far` | 0.0063 % | 13 |
| `night_near` | 0.3297 % | 154 |
| `night_far` | 0.2738 % | 98 |
| `elev_n` | 0.0024 % | 148 |
| `elev_e` | 0.0603 % | 151 |
| `elev_s` | 0.0308 % | 159 |
| `elev_w` | 0.0044 % | 15 |

**What the diffs actually show:** uniform speckle across the lit surfaces, i.e.
render noise. Placing `renders/in_*.png` and `renders/out_*.png` side by side,
the silhouette, the massing, every opening and every material read identically;
nothing is missing, shifted or newly shaded. That is the expected result — Phase B
changed zero triangles and Phase C is a lossless re-encode — but it was checked by
eye rather than inferred from the numbers.
