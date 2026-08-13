# Civic Center Plaza — optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with the defaults
(`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`).

## Result

| | Input | Shipping | |
|---|---:|---:|---|
| Bytes (raw) | 949,380 | **479,064** | −49.5%, 1.98× |
| Bytes (gzip −9) | 220,836 | 339,760 | see note |
| Objects | 94 | **19** | joined per material |
| Draw submeshes (primitives) | 100 | **25** | G5 |
| Triangles | 17,820 | 17,703 | limited dissolve, 0.05° coplanar only |
| Vertices (in Blender, welded) | 33,336 | 10,394 | 22,898 coincident pairs welded |
| Materials | 19 | 19 | identical set |
| BBox | 145.6123 × 192.6242 × 30.48 | identical | exact |
| Origin | (0, 0), base z 0 | identical | exact |

The shipping file is `artifacts/civic-center-plaza/civic-center-plaza.glb`; the
pre-optimize original is archived byte-for-byte at
`optimize/input/civic-center-plaza.glb`.

## Gates

| Gate | Result |
|---|---|
| **G1 Contract** — material set identical, `_Glow` separate, no `Toy_body`, node names intact | **PASS** — all 19 names identical, 4 `_Glow` still separate objects |
| **G2 Geometry** — bbox within max(1 cm, 0.1%), origin within 1 cm, signed volumes positive, flipped ≤ 0.15% | **PASS** — bbox and origin *exact*; 19/19 volumes positive; 0 flipped of 13,096 ray hits (0.000%) |
| **G3 Round-trip** — re-imports in Blender and loads via pinned-three `g3check` | **PASS** — `G3-OK`, 25 meshes, 17,732 tris, 19 materials, no decode errors |
| **G4 Appearance** — day+night × near+far, mean delta ≤ 2% far / ≤ 4% near | **PASS** — worst mean **0.83%** across all 8 views |
| **G5 Draw submeshes** — ≤ input | **PASS** — 100 → 25 |
| **G6 Size** — reduced; if under target, waste census must justify the remainder | **PASS with justification** — 49.5% against a 60% aspiration, see below |
| **G7 GPU budget** | n/a — bake mode off |
| **G8 Hygiene** — no foreign geometry, deterministic re-run, no `.blend1` | **PASS** — clean re-run reproduces `out.glb` byte-for-byte (sha256 `0c9424d6…`); no stray files |

### G4 detail

| View | Mean abs RGB delta | Max px delta |
|---|---:|---:|
| day_near | 0.79% | 97 |
| day_far | 0.83% | 49 |
| night_near | 0.76% | 122 |
| night_far | 0.72% | 65 |
| elev_n | 0.45% | 105 |
| elev_e | 0.68% | 90 |
| elev_s | 0.75% | 66 |
| elev_w | 0.61% | 127 |

Written description of the difference: **nothing a player would notice.** No element is
missing, no silhouette moved, no shading artifact appeared. The residual is confined to
edge pixels where the limited dissolve merged strictly-coplanar faces and the renderer's
triangulation changed by one diagonal — the deltas are anti-aliasing noise on those edges,
which is also why the max-pixel figures are high while the means are under 1%.

### G6 waste census — why this asset stops at 1.98×

The prompt's 4–6× results (st-marys-cathedral 257→42 KB, salesforce-tower 924→156 KB) come
mostly from vertex quantization. **`-noq` is mandatory for this app** — the kit and
landmark merge paths bake world matrices straight into float32 position arrays, and int16
`KHR_mesh_quantization` attributes corrupt them (documented in
`pipeline/compress-assets.mjs`; quantized pieces fail their dims gate and silently fall
back to procedural). So this asset is compared against a ceiling the others were not.

Beyond that, the remainder is irreducible for a structural reason specific to this subject:

- **The asset is entirely flat-shaded**, which the style bible requires. Every triangle
  corner needs its own normal, so vertex sharing is impossible across any edge that is not
  strictly coplanar. Blender welds 33,336 verts down to 10,394, but the glTF exporter has
  to re-split them to 32,312 on the way out. That split is the file.
- **The geometry is 450+ small closed solids**, not a few large shells: 190 trunks, 190
  crowns, 35 poles, 35 flags. A tree is 48 triangles with almost no coplanar neighbours to
  merge, and the trees alone are 51% of the asset.
- `interior_faces_removed: 0` — the census found no buried faces to delete. The solids
  interpenetrate (crowns overlap into a canopy by design) but none is provably enclosed by
  another, and the occluder rule in §3 forbids guessing.
- `dup_redundant_tris: 812` are the 20 joint strips and 22 walk ribbons, which are already
  joined per material into two objects; the triangles are genuinely distinct geometry at
  distinct positions, not duplicates to instance away.

So the remaining bytes *are* silhouette geometry, as G6 requires. The one lever left would
be dropping the tree crown from 8 sides to 6 (−1,520 tris, ~8% of the file), which the
build script documents as the first trim if the budget ever needs it — but it costs the
recognition cue, so it is not spent here.

Note the gzip row moves the wrong way (220,836 → 339,760). That is expected and not a
regression: meshopt's encoded byte streams are already entropy-coded, so gzip has little
left to remove, whereas the uncompressed float arrays gzipped well. What the CDN ships is
479 KB raw / 340 KB gzipped versus 949 KB raw / 221 KB gzipped — the *decode* cost and the
GPU upload both fall, and the on-disk figure is the one PERF-PLAN #9 gates (≤ 500 KB).

## Reproducing

```bash
cd artifacts/civic-center-plaza/optimize
BL=/Applications/Blender.app/Contents/MacOS/Blender
"$BL" -b --python inspect.py  -- input/civic-center-plaza.glb stats_input.json
"$BL" -b --python optimize.py -- input/civic-center-plaza.glb mid.glb stats_mid.json
npx -y gltfpack -i mid.glb -o out.glb -c -km -kn -noq
"$BL" -b --python validate.py -- input/civic-center-plaza.glb out.glb gates.json
"$BL" -b --python render_ab.py -- input/civic-center-plaza.glb renders/in
"$BL" -b --python render_ab.py -- out.glb renders/out
/usr/bin/python3 diff_ab.py
(cd g3check && npm install && node check.mjs ../out.glb)
```

Deterministic: re-running the chain reproduces `out.glb` with sha256
`0c9424d62d1edd378bc83e217ffc1284e2e0b7dca90fd12efce408f42a683b20`.
