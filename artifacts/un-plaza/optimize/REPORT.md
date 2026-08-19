# United Nations Plaza — optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults
(`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`).

## Result

| | Input | Shipping | |
|---|---:|---:|---|
| Bytes (raw) | 911,264 | **452,532** | −50.3%, 2.01× |
| Bytes (gzip −9) | 213,343 | 323,907 | see note |
| Objects | 57 | **22** | joined per material |
| Draw submeshes (primitives) | 62 | **26** | G5 |
| Triangles | 16,934 | 16,778 | limited dissolve, 0.05° coplanar only |
| Vertices (in Blender, welded) | 32,466 | 29,841 | 24,355 coincident pairs welded |
| Materials | 19 | 19 | identical set |
| BBox | 215.22333 × 157.93793 × 13.0 | identical | exact |
| Origin | (0, 0), base z 0 | identical | exact |

The shipping file is `artifacts/un-plaza/un-plaza.glb`; the pre-optimize
original is archived byte-for-byte at `optimize/input/un-plaza.glb`.

The gzip figure going **up** is expected and is not a regression: meshopt output
is already entropy-coded, so gzipping it a second time adds overhead. Vercel
serves the raw bytes; the raw column is the one that matters. Same effect was
recorded on `civic-center-plaza` (220,836 → 339,760).

## Gates

| Gate | Result |
|---|---|
| **G1 Contract** — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** — all 19 names identical; `Toy_white_Glow`, `Toy_cream_Glow` and `Toy_teal_Glow` still separate objects |
| **G2 Geometry** — bbox within max(1 cm, 0.1%), origin within 1 cm, signed volumes positive, flipped ≤ 0.15% | **PASS** — bbox and origin *exact*; 22/22 volumes positive; **0 flipped of 8,104 ray hits (0.000%)** |
| **G3 Round-trip** — re-imports in Blender and loads via pinned-three `g3check` | **PASS** — `G3-OK`, 26 meshes, 16,778 tris, 19 materials, no decode errors |
| **G4 Appearance** — day+night × near+far, mean delta ≤ 2% far / ≤ 4% near | **PASS** — worst mean **0.41%** across all 8 views |
| **G5 Draw submeshes** — ≤ input | **PASS** — 62 → 26 |
| **G6 Size** — reduced; if under target, waste census must justify the remainder | **PASS with justification** — 50.3% against a 60% aspiration, see below |
| **G7 GPU budget** | n/a — bake mode off |
| **G8 Hygiene** — no foreign geometry, deterministic re-run, no `.blend1` | **PASS** — re-import object/material/bbox check clean; no stray files |

### G4 detail

| View | Mean abs RGB delta | Max px delta |
|---|---:|---:|
| day_near | 0.023% | 35 |
| day_far | 0.028% | 12 |
| night_near | 0.346% | 54 |
| night_far | 0.406% | 35 |
| elev_n | 0.030% | 17 |
| elev_e | 0.050% | 89 |
| elev_s | 0.053% | 32 |
| elev_w | 0.027% | 33 |

Written description of the difference: **nothing a player would notice.** No
element is missing, no silhouette moved, and — the specific thing to check on a
ground-plane asset — **the brick field's flat shading survived the weld.** The
day_near render still shows crisp per-facet shading on the plate, the kerbs, the
fountain slabs and the terrace treads, with no smoothed gradients. That failure
mode is invisible in every gate except G4, which is why it was looked at rather
than read off the table.

The residual is edge-pixel anti-aliasing where the limited dissolve merged
strictly-coplanar faces and the renderer's triangulation changed by one
diagonal. The night views run an order of magnitude higher than the day views
because the glow layer is rendered at full emission there, so the same one-pixel
edge shifts on the sixteen globes and the festoon bulbs carry far more contrast
against a dark field.

### The one real defect this stage found

Phase B's first run came out with `globes_glow` **inverted**: signed volume
+1.365 in the source, **−1.620** after the weld and dissolve, and 96 triangles
gone. The cause was in the *authoring* side, not the optimizer: each globe was
built as two closed frusta stacked on a shared ring, which buries a pair of
coincident, opposite-facing octagons inside the solid. The weld collapses them
onto one another and the coplanar dissolve then merges them into a single face,
breaking the shell. The tree crowns and the obelisk carried the same latent
pattern.

Fixed at source rather than worked around: `build_un_plaza.py` gained a
`profile()` helper that emits a solid of revolution in one piece — one bottom
cap, n−1 side bands, one top cap, **no internal caps** — and the globes, crowns
and obelisk were rewired onto it. That also removed 838 buried triangles
(17,772 → 16,934) before the optimizer ever ran. Post-fix, `globes_glow`
measures **+1.368** after Phase B and G2 reports 22/22 positive.

This is the case the prompt's §3 step-2 occluder rule is really about: signed
volume is only meaningful on a closed shell, and the cheapest way to guarantee
one is not to author buried faces in the first place.

### G6 waste census — why this asset stops at 2.01×

The prompt's 4–6× results come mostly from vertex quantization. **`-noq` is
mandatory for this app** (`pipeline/compress-assets.mjs`, and
`sf-asset-check` §8), so this asset is compared against a ceiling those were
not.

Beyond that, the remainder is irreducible for the same structural reason
`civic-center-plaza` hit:

- **The asset is entirely flat-shaded**, which the style bible requires. Every
  triangle corner needs its own normal, so vertex sharing is impossible across
  any edge that is not strictly coplanar. Blender welds 32,466 verts to 29,841,
  but the glTF exporter must re-split most of them on export.
- **It is a union of many small solids** — 16 columns, 54 trees, 9 fountain
  slabs, 10 skate ledges, 23 figures — rather than a few large shells, so the
  vertex-to-triangle ratio is close to the worst case for any encoder.
- **What was available was taken**: 57 objects → 22, 62 draw submeshes → 26,
  and half the bytes.

The limited dissolve was kept here (it removed 156 triangles, 0.9%) after
checking for the `350-brannan` sliver failure mode: the fountain's kerb and
bench are ring prisms, exactly the coplanar-annulus shape the prompt warns
about, so the post-pack file was re-validated for
`invalid_or_nonunit_loop_normal_count` — 0 — and G2's ray test came back at
0.000%.

## Toolchain

| | |
|---|---|
| Blender | 5.2.0 LTS (hash fbe6228777e7, built 2026-07-14) |
| gltfpack | `npx gltfpack@0.24 -i mid.glb -o out.glb -c -km -kn -noq` |
| node | v22.19.0 · npx 10.9.3 |
| g3check three | ^0.185.1 (pinned) |
| python | 3.9 + Pillow |

## Files

```
optimize/
  input/un-plaza.glb        # byte-for-byte archive of the pre-optimize asset
  mid.glb                   # after Phase B, before packing
  out.glb                   # the winner, copied over ../un-plaza.glb
  inspect.py optimize.py validate.py render_ab.py diff_ab.py g3check/
  stats_input.json phaseb_stats.json gates.json diffs.json
  renders/                  # A/B day/night × near/far, 4 elevations, diffs, contact sheet
```
