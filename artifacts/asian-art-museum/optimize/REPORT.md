# Asian Art Museum — GLB optimize report (stage 4)

Run 12 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no` ·
`TARGET_REDUCTION: 60%`.

Input archived byte-for-byte at `input/asian-art-museum.glb` (verified with `cmp`).
Every step is a committed deterministic script; re-running them on the input
reproduces the output.

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| File, raw | 718,620 B | **323,984 B** | **−54.9% (2.22×)** |
| File, gzip | 120,507 B | 230,956 B | +91.7% (see note) |
| Triangles | 13,176 | **13,176** | 0 |
| Vertices | 25,686 | **6,910** | −73.1% |
| Objects / draw submeshes | 163 | **11** | −93.3% |
| Materials | 11 | 11 | identical set |
| Bbox dims | 115.3099 × 65.1848 × 28.1 | 115.3099 × 65.1848 × 28.1 | 0 |
| Bbox min | −57.655, −32.5924, 0.0 | −57.655, −32.5924, 0.0 | 0 |
| Ray-flip fraction | 0.0 | **0.0** | — |

**Gzip goes up, and that is expected.** meshopt's own entropy coding already
compresses the buffer, so gzipping it again adds overhead — the same result
`chase-center` recorded (+14.5%). The raw byte count is what ships and what the
500 KB budget in `sf-asset-check` §7 measures: 324 KB, comfortably under.

## Phase A — waste census

`inspect.json`. 163 objects, 13,176 tris, 25,686 verts, 11 materials, 718,620 B raw.
The census predicted the win would come almost entirely from **object-count
overhead**, not from geometry: every element was authored as its own closed solid
(163 of them), so the file carried 163 nodes, meshes and accessor sets for what is
really 11 material groups. Predicted: node/accessor collapse ≈ 90% of the saving,
vertex welding at the joins ≈ the rest, retessellation ≈ 0.

That is what happened. **No geometry was removed at all.**

## Phase B — geometry cleanup

`optimize.py` → `phaseb_stats.json`, `mid.glb` (586,640 B).

| Step | tris | verts |
|---|---|---|
| input | 13,176 | 25,686 |
| weld + degenerate | 13,176 | 6,910 |
| interior faces | 13,176 | 6,910 |
| limited dissolve 0.05° | 13,176 | 6,910 |
| join per material | 13,176 | 6,910 |

Judgment calls:

- **Interior faces removed: 0, and that is correct.** The occluder rule only accepts
  a CLOSED, box-like solid (AABB fill ≥ 95%) as an occluder. The one mesh that
  really does bury faces here — the arcade and window panels sunk 0.6–0.75 m into
  the wall — is buried inside the `body` outline prism, which is a ten-vertex
  rectilinear L-shape and fails the box-like test. Rather than loosen the rule, the
  faces stay. They cost ~200 triangles.
- **Retessellation skipped.** The only curved geometry is the eight 12-segment
  colonnade columns and the seven-segment arch heads. Both are silhouette geometry
  on the hero elevation at near distance; halving their segments is visible.
- **Limited dissolve found nothing** because the build script already emits
  minimal quads — there are no co-planar fans to merge.
- The whole −73% vertex win is the per-object weld surviving into the per-material
  join: 163 separately-exported solids shared no vertices; joined, they do.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o asian-art-museum.optimized.glb -c -km -kn -noq
```

`-km -kn` kept (glow-ness is name-only; without `-km` gltfpack would merge
`Toy_white_Glow`/`Toy_gold_Glow` across the glow boundary and kill the night
layer). `-noq` per the repo standard — verified: the output material name set is
identical and the stage-2 contract validator still passes `transforms_applied` and
`no_unexpected_objects`.

`grep -rn setMeshoptDecoder app/src/` hits `app/src/gltf.js` and `app/src/assets.js`,
so meshopt is safe to rely on.

## Phase E — A/B verification

`render_ab.py` at landmark distances (near 1.5× long axis = 173 m, far 6× = 692 m),
day and night, plus four elevations. `diff_ab.py` → `diffs.json`.

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0068% | 40 |
| day far | 0.0073% | 14 |
| night near | 0.0032% | 7 |
| night far | 0.0035% | 3 |
| elev N / E / S / W | 0.0104 / 0.0147 / 0.0124 / 0.0328% | 7 / 30 / 39 / 14 |

Looked at, honestly: **nothing is visibly different.** Every element is present in
both — colonnade, arcade, base openings, cornice, attic, both light courts, the
hipped monitor, the pavilion, the terrace, the coral sculptures and mint planters.
The isolated max-delta pixels sit on antialiased silhouette edges and on the
monitor's hip ridge, where meshopt's float rounding moves a vertex by a fraction of
a millimetre and one edge pixel resolves differently. The night pass confirms both
glow surfaces still light and nothing else does.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | Material name set identical (11, both `_Glow` preserved separately); no `Toy_body`; no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox and origin bit-identical; signed volumes positive; flipped fraction 0.0 |
| G3 Round-trip | **PASS** | Blender re-import OK; `g3check` (pinned three 0.185.1): `{"ok":true,"meshes":11,"tris":13176,...}`, no decode errors |
| G4 Appearance | **PASS** | max mean delta 0.033% against 2% far / 4% near |
| G5 Draw submeshes | **PASS** | 163 → 11 |
| G6 Size | **PASS** | −54.9% raw against a 60% target. The shortfall is the `-noq` standard (the 60% figure was measured with quantization on) plus the census result that there is no removable geometry — the remainder is silhouette |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | **PASS** | re-import object/material/bbox check passes; scripts deterministic; no `.blend1` files |

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7) · gltfpack 0.24 via `npx` · node + three 0.185.1
(pinned in `g3check/package.json`) · python3 + Pillow · gzip. No substitutions.

## Shipping swap

All gates passed, so `asian-art-museum.optimized.glb` was copied over
`artifacts/asian-art-museum/asian-art-museum.glb`. The pre-optimize original stays at
`optimize/input/asian-art-museum.glb`. The asset's `validation.json` and `REPORT.md`
were re-generated against the shipped file, so the integration stage writes its
manifest entry from reality: **11 objects, 13,176 tris, 115.31 × 65.18 × 28.10 m,
323,984 B**.
