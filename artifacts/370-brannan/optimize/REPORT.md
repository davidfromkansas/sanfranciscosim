# 370 Brannan Street — GLB optimize report (stage 4)

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against `artifacts/370-brannan/`
on 13 August 2026. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`. Scripts are adapted copies of `tools/glb-optimize/` (only
`diff_ab.py`'s contact-sheet title differs from the generic version).

**Result: all gates PASS. The optimized GLB is now the shipping file.**

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| File size, raw | 93,428 B | **46,796 B** | **−49.9%** |
| File size, gzip -9 | 19,933 B | 31,246 B | +56.8% (see §4) |
| Triangles | 1,428 | 1,428 | 0 |
| Vertices | 2,880 | 2,475 | −14.1% |
| Objects | 28 | 11 | −60.7% |
| Draw submeshes (primitives) | 29 | **12** | −58.6% |
| Materials | 10 | 10 | identical set |
| bbox dims (m) | 21.87273 × 21.70572 × 7.63 | identical | 0 |
| bbox min | −10.89616, −10.89828, 0.0 | identical | 0 |

Toolchain: Blender 5.2.0 LTS, `gltfpack` 0.24, node v22.19.0, Python 3.9 +
Pillow 11.3.0, gzip -9.

## §2 Waste census (Phase A, `inspect.json`)

| Technique | Finding | Predicted saving |
|---|---|---|
| Object-count overhead | 28 objects across 10 materials; 7 join groups (`Toy_ink` 5, `Toy_greige` 5, `Toy_glass` 4, `Toy_trim` 4, `Toy_glassl` 3, `Toy_roofd` 3, `Toy_stone` 2) | the dominant win — node + accessor overhead on a 1,428-tri asset |
| Unwelded coincident verts | 2,112 pairs | ~2,100 verts |
| Duplicate meshes | 6 groups, 308 redundant tris (`skylight0/1`, `skylight_kerb0/1`, `frame_pier_ne/sw`, `rwin0/1_frame`, `mullion0/1/2`, `rwin0/1_fill`) | not exploited — see judgment calls |
| Degenerate faces | 0 | — |
| Buried interior faces | 0 removable | — |
| Over-tessellated curves | none (no curved shells in this asset) | — |

On an asset this small the geometry is already lean; the file is almost entirely
glTF structure, which is exactly what the join and the pack attack.

## §3 Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 1,428 | 2,880 |
| weld ≤ 1 mm + degenerate removal | 1,428 | 768 |
| interior-face removal | 1,428 | 768 |
| limited dissolve 0.05° | 1,428 | 768 |
| join per material | 1,428 | 768 |

Lossless: not one triangle changed. The weld took 2,880 → 768 verts (−73%);
per-object welding cannot fuse glow onto base surfaces because the glow shells
are separate objects. Objects 28 → 11: ten single-material joins plus `body`,
which carries two materials (`Toy_greige` walls, `Toy_roofd` deck cap) and so
cannot join into a single-material group.

Curve retessellation (step 4) was **skipped — not applicable**: this asset has
no curved shells at all, only boxes and planar panels.

Normals audit after Phase B: per-object signed volume positive on every closed
solid; ray-test flipped fraction **0.0**.

## §4 Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 370-brannan.optimized.glb -c -km -kn -noq
```

`-km -kn` kept (glow-ness is name-only; without `-km` gltfpack would merge
identical-parameter materials across the `_Glow` boundary and silently kill the
night layer). `-noq` per the repo standard — output carries
`EXT_meshopt_compression` and float32 attributes, matching what
`pipeline/compress-assets.mjs` produces.

**Honest note on the gzip number.** Raw bytes halve, but gzipped bytes go *up*,
19,933 → 31,246. That is expected and is not a regression to fix: meshopt output
is already entropy-coded, so gzip has nothing left to remove, while the
uncompressed input gzips well. On an asset this small the two effects cross over
and the plain GLB would actually be ~11 KB cheaper over the wire. Meshopt is
kept anyway because `AGENTS.md` mandates it at intake for every GLB under
`app/public/sf-assets/` and `compress-assets.mjs` would apply it at ship time
regardless — one encoding across all assets is worth more than 11 KB on one
building. Recorded so the next reader does not treat it as a bug.

## §5 Phase D — bake

Not run (`ALLOW_BAKE: no`). No textures added; the asset remains texture-free.

## §7 Phase E — A/B verification

Input vs output, same rig, day + night × near + far, plus four orthographic
elevations. Landmark distances: near 1.5× long axis, far 6×.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day_near | 0.0619% | 41 |
| day_far | 0.0589% | 38 |
| night_near | 0.0075% | 10 |
| night_far | 0.0082% | 15 |
| elev_n | 0.0527% | 30 |
| elev_e | 0.0655% | 33 |
| elev_s | 0.0176% | 45 |
| elev_w | 0.0048% | 101 |

Gates allow ≤ 2% far and ≤ 4% near; the worst view here is 0.066%, thirty times
inside the tightest gate.

**Looked at the diffs, honestly:** at 8× amplification the only visible change is
a hairline along the top edge of the parapet and a few one-pixel slivers down the
window-frame and door-surround edges. Those are the welded coincident vertices
moving an antialiased edge by a fraction of a pixel. Nothing is missing, the
silhouette is bit-identical in bbox, no shading artifact appears anywhere, and at
1× the two rows of the contact sheet are indistinguishable. There is nothing here
a player could notice.

## §8 Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (10), `_Glow` pair kept separate, no `Toy_body`, node names intact |
| G2 Geometry | **PASS** | bbox identical to 5 dp, origin identical, all signed volumes positive, flipped fraction 0.0 |
| G3 Round-trip | **PASS** | re-imports in Blender (stage-2 validator re-run: overall PASS); `g3check` pinned-three: `{"ok":true,"meshes":12,"tris":1428,...}` |
| G4 Appearance | **PASS** | worst mean delta 0.066% vs 2%/4% gates; visual description above |
| G5 Draw submeshes | **PASS** | 29 → 12 |
| G6 Size | **PASS** | raw −49.9%. Below the 60% aspiration, and the census explains why: with 0 degenerates, 0 buried faces and no curves, the only geometry lever was the weld, and 1,428 tris of pure silhouette-and-facade box geometry is what remains. |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | **PASS** | re-import object count matches (11), no foreign geometry, no `.blend1` left, intermediate `mid.glb` removed, scripts deterministic |

## §9 Shipping swap

`370-brannan.optimized.glb` was copied over `artifacts/370-brannan/370-brannan.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/370-brannan.glb` (verified with `cmp`). The asset's
`validation.json` and `REPORT.md` were re-generated / updated against the
shipped file, so the manifest entry is written from the shipped numbers.
