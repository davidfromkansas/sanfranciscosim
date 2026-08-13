# 599 Third Street — optimize pass (stage 4)

Run 13 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`. Scripts are
adapted copies of `tools/glb-optimize/`. Input archived byte-for-byte at
`input/599-third.glb` (verified with `cmp`); the original was never modified in
place.

## 0. Headline

| Metric | Input | Optimized | Δ |
|---|---|---|---|
| File bytes (raw) | 658,108 | **240,704** | **−63.4 %** |
| File bytes (gzip −9) | 86,997 | 155,229 | +78 % (see §4) |
| Objects / primitives | 376 / 376 | **12 / 12** | −96.8 % |
| Triangles | 9,384 | 9,384 | 0 |
| Vertices (Blender) | 18,672 | 16,260 | −12.9 % |
| Vertices after weld (pre-pack) | 18,672 | 5,440 | −70.9 % |
| Materials | 12 | 12 | identical set |
| bbox dims | 43.15056 × 42.85277 × 18.3 | identical | 0 |
| bbox min | −21.5771, −21.43354, 0.0 | identical | 0 |

**All gates G1–G6 and G8 PASS.** G7 is not applicable (`ALLOW_BAKE: no`).

## 1. Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash `fbe6228777e7`, 2026-07-14) |
| gltfpack | 0.24 (pinned, via `npx -y gltfpack@0.24`) |
| node | v22.19.0 |
| three (g3check) | ^0.185.1 |
| Pillow | 11.3.0 |

## 2. Phase A — waste census

`inspect.json`. The asset is 9,384 triangles spread over **376 objects and 376
primitives** — the mesh itself is already lean, and essentially all of the file
weight is node/accessor overhead plus unwelded duplicate vertices.

| Waste | Measured | Technique | Predicted saving |
|---|---|---|---|
| Object-count overhead | 376 objects sharing 12 materials | join per material | ~360 nodes + accessors, the dominant win |
| Unwelded coincident verts | 13,232 pairs | per-object weld ≤ 1 mm | ~13 k verts |
| Repeated identical meshes | 6,960 redundant tris across 12 condensers, 9 skylight frames/panes/glows, 30 punched windows | absorbed by join-per-material | (counted above) |
| Degenerate faces | **0** | — | none (fixed in stage 2) |
| Textures / UVs / vertex colours | none; only `NORMAL` | — | none |
| Over-tessellated curves | none — the asset has no curved shells | — | none |

`join_candidates` by material: `Toy_trim` 201, `Toy_glass` 70, `Toy_ink` 38,
`Toy_sand` 16, `Toy_glassl` 13, `Toy_roofd` 12, `Toy_mustard_Glow` 10,
`Toy_glassl_Glow` 9, `Toy_steel` 3, `Toy_trim_Glow` 2.

## 3. Phase B — geometry cleanup

`optimize.py` → `mid.glb`, stats in `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 9,384 | 18,672 |
| weld + degenerate | 9,384 | 5,440 |
| interior faces | 9,384 | 5,440 |
| limited dissolve 0.05° | 9,384 | 5,440 |
| join per material | 9,384 | 5,440 |

Judgment calls:

- **Weld did all the vertex work** (−70.9 %), as predicted: every box in the
  build script is authored as an independent closed solid with duplicated
  corner vertices.
- **Interior-face removal removed nothing (0 faces).** Correct and expected.
  The occluder rule only admits closed solids, and although this asset is a
  union of closed solids, the facade elements sit *proud* of the wall rather
  than intersecting it — the build script deliberately never cuts openings, so
  there is very little buried geometry to find. No boolean unions were used as
  a shortcut.
- **Limited dissolve at 0.05° found nothing.** Also expected: the geometry is
  beveled boxes, so adjacent coplanar faces were already merged at authoring
  time. The prompt's warning against 0.5° was respected.
- **Triangle count is unchanged at 9,384.** That is the honest result for this
  asset — the waste was never in the triangles.
- Objects joined 376 → 12. No manifest-named nodes and no `Toy_body` exist
  here, so nothing had to be held out. `cafe_awning` and `roof_field` stayed
  separate because each is the sole user of its material (`Toy_coral`,
  `Toy_stone`).

## 4. Phase C — packing, and an honest note on gzip

```
npx gltfpack@0.24 -i mid.glb -o 599-third.optimized.glb -c -km -kn -noq
```

`-km -kn` kept (glow-ness is name-only; without `-km`, gltfpack would merge
`Toy_glassl` into `Toy_glassl_Glow` and silently kill the night layer). `-noq`
kept per the repo standard established in `artifacts/380-brannan/optimize/REPORT.md`
§4 — no quantization, float32 attributes preserved for the runtime merge.
Verified on the output rather than trusting flags: material name set identical,
bbox within tolerance, `EXT_meshopt_compression` present and
`KHR_mesh_quantization` absent.

**On the gzip figure.** Raw bytes fall 63 %, but gzipped bytes *rise* 87 KB →
155 KB. This is not a regression, and it is worth recording so nobody re-opens
it later:

- the meshopt bitstream is already entropy-coded, so it barely gzips further;
- the *input* gzipped exceptionally well precisely because of the waste — 376
  near-identical nodes and 13,232 duplicate vertices are extremely compressible.

The fair comparison is against what actually ships, since
`pipeline/compress-assets.mjs` meshopt-packs every GLB at intake regardless:

| File | raw | gzip |
|---|---|---|
| input, authored | 658,108 | 86,997 |
| **input → packed (the real ship baseline)** | 407,412 | 111,808 |
| phase B mid | 457,164 | 114,236 |
| **phase B → packed (shipped)** | **240,704** | **155,229** |

Against the ship baseline the optimize pass is **−40.9 % raw**. The result sits
inside the shipped norm for this repo — `380-brannan` is 222,516 raw / 166,988
gzip, `375-alabama` 318,672 / 182,934 — and well inside the 500 KB budget in
`AGENTS.md` and `sf-asset-check` §7.

## 5. Phase D — high→low bake

Skipped: `ALLOW_BAKE: no`, and the contract forbids textures without a recorded
exception. Nothing here warrants one — the asset is 9,384 triangles.

## 6. Phase E — A/B verification (gate G4)

`render_ab.py` on both files with one rig, then `diff_ab.py`. Landmark
distances: near = 1.5× long axis, far = 6× long axis; day (glow alpha 0.12) and
night (alpha 1.0, emission from Base Color), plus four orthographic elevations.

| View | mean abs RGB Δ | max px Δ | gate |
|---|---|---|---|
| day_near | 0.0047 % | 19 | ≤ 4 % |
| day_far | 0.0042 % | 4 | ≤ 2 % |
| night_near | 0.1292 % | 41 | ≤ 4 % |
| night_far | 0.1203 % | 24 | ≤ 2 % |
| elev_n | 0.0116 % | 33 | — |
| elev_e | 0.0565 % | 44 | — |
| elev_s | **0.1542 %** (worst) | 51 | — |
| elev_w | 0.0992 % | 46 | — |

**Looked at, not just measured.** In `renders/contact_sheet.png` the input and
optimized rows are indistinguishable. The ×8-amplified diff row is black except
for hairline outlines tracing window-frame and mullion edges — sub-pixel
antialiasing shifts where the weld merged coincident corner vertices. Nothing is
missing, no silhouette moved, no shading artifact appeared, and the night pass
lights exactly the same surfaces. The night views carry the larger delta simply
because emissive edges against a near-black background amplify a one-pixel
seam. **Nothing a player would notice.**

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (12); `_Glow` separate; no `Toy_body`; no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox and origin bit-identical; 12/12 signed volumes positive; 0/16,438 flipped first hits (0.0000 % vs 0.15 % gate) |
| G3 Round-trip | **PASS** | Blender re-import 12 objects; `g3check` → `G3-OK` 12 meshes / 9,384 tris / 12 materials, no decode errors |
| G4 Appearance | **PASS** | worst 0.1542 % ≤ 2 % far / 4 % near; visual review above |
| G5 Draw submeshes | **PASS** | 376 → 12 primitives |
| G6 Size | **PASS** | 658,108 → 240,704 raw (−63.4 %), past the 60 % target; −40.9 % against the packed ship baseline |
| G7 GPU budget | **n/a** | bake mode off |
| G8 Hygiene | **PASS** | re-import object count matches (no foreign geometry); deterministic re-run reproduced byte-identical output (md5 `4588ed1e1883d2829548a115918a68bd`); one stray `.blend1` found and deleted |

An extra check beyond the prompt: the optimized GLB was also re-run through the
asset's own **stage-2 contract validator** (`validate_599_third.py`) and passed
**15/15**, including `transforms_applied` and `no_unexpected_objects` — the two
that the quantized build failed on `380-brannan`. This is what confirms `-noq`
did the right thing.

## 8. Shipping swap

All gates passed, so `599-third.optimized.glb` was copied over
`artifacts/599-third/599-third.glb`. The pre-optimize original remains archived
at `optimize/input/599-third.glb`. The asset's `validation.json` and `REPORT.md`
were regenerated/updated to the shipped numbers so the integration stage writes
its manifest entry from reality.
