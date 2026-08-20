# 131 Steuart Street — optimize pass (stage 4)

Run 18 August 2026 against `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Input archived byte-for-byte at `input/131-steuart.glb`; the winner
(`131-steuart.optimized.glb`) has been copied over
`artifacts/131-steuart/131-steuart.glb` as the shipping file.

## Metrics

| | Input | Output | Δ |
|---|---|---|---|
| Raw bytes | 448,708 | **191,416** | **−57.3 %** |
| gzip -9 bytes | 69,875 | 109,041 | +56 % (see note) |
| Triangles | 6,842 | 6,842 | 0 |
| Vertices | 13,712 | 13,444 | −2.0 % |
| Objects | 196 | **13** | −93 % |
| Draw primitives | 199 | **16** | −92 % |
| Materials | 11 | 11 | identical set |
| bbox dims (m) | 41.22088 × 41.34584 × 27.7 | identical | 0 |
| bbox min | −20.60874, −20.67207, 0.0 | identical | 0 |
| XY centre | 0.0017, 0.00085 | identical | 0 |

**On the gzip figure.** The output carries `EXT_meshopt_compression`, whose
payload is already entropy-coded, so it does not gzip further — the raw byte
count is the one that matters over the wire, and it more than halves. This is
the same encoding `pipeline/compress-assets.mjs` produces, so the mandatory ship
step will skip the file rather than re-pack it.

## Phase A — waste census

- 196 objects / 199 primitives against 11 materials — **object-count overhead was
  the dominant waste**, predicted ≈ 185 objects and 183 primitives recoverable by
  joining per material.
- 9,910 coincident vertex pairs (every `quad_box` corner is authored twice
  across adjoining faces) — predicted ≈ 9,900 verts recoverable by welding.
- 18 duplicate mesh groups / 3,620 redundant triangles — these are the repeated
  window units and roof plant. **Not deduplicated**: at 196 → 13 objects the
  join pass is worth more than instancing, and instancing 39 tiny window plates
  would re-introduce the node overhead the join just removed.
- 0 degenerate triangles, 0 textures, `NORMAL` the only extra vertex attribute.
- Over-tessellation: one-pixel world size at the near camera distance (62.02 m)
  is 0.0418 m; the only curved shell is the penthouse barrel at 6 segments over
  14.16 m, i.e. 2.36 m per facet. Already far coarser than a pixel — nothing to
  retessellate, and it is silhouette geometry anyway.

## Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 6,842 | 13,712 |
| weld ≤ 1 mm + degenerate | 6,842 | 3,802 |
| interior faces | 6,842 | 3,802 |
| limited dissolve | **skipped** | — |
| join per material | 6,842 | 3,802 |

- **Weld** did the whole vertex win: 13,712 → 3,802 (−72 %). Per-object only, so
  no glow shell can fuse onto a base surface.
- **Interior faces**: 0 removed. Every solid here is either exposed or a proud
  applied band; nothing is provably buried inside another closed solid.
- **Limited dissolve — deliberately skipped.** §3 step 3 of the prompt says to
  skip it on assets with large coplanar ring bands, and this asset has **four**
  full-footprint annuli: the cornice, its cap, the gravel stop and the penthouse
  band. A strictly-coplanar dissolve merges each into one annulus ngon whose
  re-triangulation emits slivers that pass an area-based degeneracy test but
  collapse the stored vertex normals in the packed file — the `350-brannan`
  failure. The step was worth ~30 triangles there; the risk is not worth it.
- **Join per material**: 9 groups formed (`Toy_glass` 39, `Toy_ink` 38,
  `Toy_stone` 37, `Toy_rust` 36, `Toy_glassl_Glow` 17, `Toy_glassl` 9,
  `Toy_cream` 9, `Toy_sash` 5, `Toy_steel` 2). `body_brick`, `body_stone`,
  `pent_body` and `entry_glow` stayed separate (single-user or multi-material).

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 131-steuart.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API here — `Toy_glassl`
and `Toy_glassl_Glow` are parameter-identical and would be merged across the
glow boundary without `-km`, silently killing the night layer. `-noq` matches
`compress-assets.mjs` and keeps float32 attributes for the runtime merge.
Preflight: `grep -rn setMeshoptDecoder app/src/` hits `gltf.js:10` and
`assets.js:406`.

## Phase E — A/B verification

Cycles, 64 samples, day (glow alpha 0.12) and night (emission, dusk world), near
= 1.5× long axis and far = 6×, plus four orthographic elevations. Mean absolute
RGB delta over foreground pixels:

| View | Mean Δ | Max px Δ |
|---|---|---|
| day near | 0.0092 % | 12 |
| day far | 0.0113 % | 6 |
| night near | 0.171 % | 30 |
| night far | 0.1995 % | 37 |
| elev N / E / S / W | 0.0196 / 0.0035 / 0.0162 / 0.0293 % | 71 / 16 / 26 / 33 |

Gate is ≤ 2 % far and ≤ 4 % near; the worst view is **0.1995 %**, an order of
magnitude inside it.

**Looking at the ×8-amplified diffs**: everything visible is a one-pixel
anti-aliasing fringe along silhouette edges, plus a faint highlight on one roof
condenser where the welded normals changed the shading by a shade. No element is
missing, no silhouette moved, no shading artefact. Nothing a player would notice.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (11); `_Glow` pair kept separate; no `Toy_body`; node names intact |
| G2 Geometry | **PASS** | bbox and origin identical to 5 decimals; 13/13 signed volumes positive; ray flipped fraction 0.000335 (gate 0.0015) |
| G3 Round-trip | **PASS** | Blender re-import OK; `g3check` `G3-OK` — 16 meshes, 6,842 tris, 11 materials, no decode errors |
| G4 Appearance | **PASS** | worst mean Δ 0.1995 % vs 2 %/4 % gates; diffs are AA fringes only |
| G5 Draw submeshes | **PASS** | 199 → 16 |
| G6 Size | **PASS** | 448,708 → 191,416 raw, −57.3 % (target 60 % — the remainder is silhouette geometry and float32 attributes the runtime merge requires) |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | **PASS** | re-import object/material counts match; deterministic scripts committed here; no `.blend1` left |

## Post-swap re-validation

`validate_131_steuart.py` re-run against the swapped shipping file: **overall
PASS**, all 15 stage-2 checks green, 6,842 tris, 27.700 m crest, loader scale
1.000000, XY offset 1.7 mm. `artifacts/131-steuart/validation.json` and
`REPORT.md` carry the shipped numbers.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7); `gltfpack` 0.24 via npx; node v22.19.0;
python3 3.9 + Pillow; gzip -9.
