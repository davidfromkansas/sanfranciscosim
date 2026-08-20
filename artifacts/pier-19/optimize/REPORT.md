# pier-19 — GLB optimize report

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` (v2) with
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`. Scripts are
the pier-1 adaptations of `tools/glb-optimize/` (this asset shares its origin
convention and family), re-run deterministically against
`optimize/input/pier-19.glb` (byte-identical archive of the approved asset).

## Metrics

| | input | mid (Phase B) | shipped (packed) |
|---|---|---|---|
| raw bytes | 626,236 | 441,676 | **211,424** |
| gzip -9 bytes | 94,165 | — | 110,613 |
| triangles | 7,782 | 7,782 | 7,782 |
| vertices | 15,565 | 4,808 | 4,808 |
| objects / draw submeshes | 447 | 13 | **13** |

626 → 211 KB raw (−66%), 447 → 13 draw submeshes. The gzip figure rises
slightly (meshopt streams don't gzip as well as raw float32), but the shipped
metric is the meshopt file the app actually decodes: 211 KB, well under the
500 KB landmark budget, and −69% GPU-side accessor overhead from the joins.

## Phases

- **B1 weld ≤1 mm (per object)**: 15,565 → 4,808 verts, 0 tris removed.
- **B2 degenerate/interior faces**: nothing to remove (no buried closed-solid
  occluders qualify under the occluder rule).
- **B3 limited dissolve: SKIPPED** by the ring-band rule — the wing copes,
  plinths and monitor cap are coplanar ring bands; the dissolve is the only
  Phase-B step that can manufacture sliver degenerates, and on this asset it
  was projected worth <1% (pier-1 measured the same and skipped).
- **B4 curve retess: skipped** — the only curves are the archivolt (10 segs,
  silhouette-defining at the facade) and 6-8 seg furniture cylinders already
  at minimum.
- **B5 join per material**: 447 objects → 13 (one per material + glow split),
  the dominant win.
- **B7 normals audit**: signed volumes positive, 0 inverted; ray residual 0.0.
- **C pack**: `npx gltfpack@0.24 -c -km -kn -noq` (repo standard; no
  quantization — float32 attributes preserved for the runtime merge).

## Gates

| Gate | Result |
|---|---|
| G1 materials identical (glow split intact) | PASS |
| G2 bbox/origin within tol; volumes positive; flip 0.0 | PASS |
| G3 Blender re-import + g3check pinned-three round-trip (16 meshes, no decode errors) | PASS |
| G4 appearance A/B day+night × near+far + 4 elevations: mean deltas 0.002–0.29%, max 0.29% (night halo around lit clerestory bays — soft emission bloom only; no missing elements, no silhouette change) | PASS |
| G5 draw submeshes 447 → 13 | PASS |
| G6 size −66% raw | PASS |
| G7 (bake mode) | n/a |
| G8 deterministic re-run; no foreign geometry; no .blend1 | PASS |

## Shipping swap

`pier-19.optimized.glb` copied over `artifacts/pier-19/pier-19.glb`; the
pre-optimize original is archived at `optimize/input/pier-19.glb`. The stage-2
contract validator was re-run against the SHIPPED (packed) file —
`validation.json` overall PASS, 13 objects, 0 invalid/non-unit loop normals
(the packed-file sliver trap does not occur here; dissolve was skipped).

Toolchain: Blender 5.2.0 LTS, gltfpack 0.24 (npx, pinned), node + pinned
three in `g3check/`, python3 + Pillow.
