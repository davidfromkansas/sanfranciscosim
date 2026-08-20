# Hiram W. Johnson State Office Building — stage 4 optimize report

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 against
`artifacts/hiram-johnson-state-office-building/`, 19 August 2026.
Defaults: `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.
Blender 5.2.0 LTS, `gltfpack@0.24`, three@0.185.1.

## Metrics

| | input | output | delta |
|---|---|---|---|
| Raw bytes | 893,324 | **421,380** | **−52.8 %** |
| gzip(9) bytes | 187,101 | 275,639 | +47 % — expected: the meshopt payload is already entropy-coded, so gzip cannot compress it further; the raw byte count is what the CDN serves |
| Triangles | 16,908 | 16,908 | 0 |
| Vertices | 32,352 | 29,218 | −9.7 % (8,710 in the pre-pack `mid.glb` after the per-material join; gltfpack re-splits shared verts per primitive) |
| Objects / draw submeshes | **129** | **9** | **−93 %** |
| Materials | 9 | 9 | identical set |
| bbox dims | 130.6549 × 67.1789 × 61.9 | identical | 0 |
| bbox min | −65.3274, −33.5895, 0.0 | identical | 0 |
| Origin XY | 0.000, 0.000 | 0.000, 0.000 | 0 |

## Waste census (Phase A) and what each phase bought

| technique | predicted | actual |
|---|---|---|
| Weld coincident verts ≤ 1 mm, per object | modest | 16,908 tris, verts 32,352 → 8,710 across weld + join |
| Interior faces buried in closed solids | none — every part is an applied band on an outer face, nothing is enclosed | **0 faces** |
| Limited dissolve 0.05° | ~0, and negative in risk | **skipped by policy**, see below |
| Join per material | the big one: 129 nodes over 9 materials | **129 → 9 objects**, 9 draw submeshes |
| gltfpack `-c -km -kn -noq` | ~50 % of file | 893,324 → 421,380 B |

**The limited dissolve was skipped, deliberately.** Prompt §3 step 3 says to skip
it entirely on assets with large coplanar ring bands, and this asset is made of
them — the parapet ring, the granite base, the sill and cap courses and every
storey spandrel follow the footprint the whole way round. Their top and bottom
faces are perfectly coplanar annuli, so even a strictly-coplanar dissolve merges
each into one annulus ngon and re-triangulating an annulus emits slivers. The
savings it would have bought were already taken at the source: the build script
removes duplicate and collinear points from every generated ring
(`dedupe_ring`), which is where this asset's coplanar runs came from.

That is not theoretical here. An earlier build of this asset shipped 2,624
sub-5 mm faces on the parapet ring — created by a 0.12 m bevel on a ring that
long, not by a dissolve — and the Phase B weld collapsed two of them into
zero-length vertex normals. gltfpack re-emits the STORED normals, so the failure
appeared only in the packed file, as `invalid_or_nonunit_loop_normal_count: 2`,
and only when the stage-2 contract validator was re-run against the shipped GLB.
Fixed at the source by dropping the parapet's bevel; the asset lost 4,160
triangles it did not need (21,068 → 16,908) and the census now shows zero
degenerate geometry at every stage.

## Gates

| gate | result | evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical, both `_Glow` materials still separate, no `Toy_body` |
| G2 Geometry | **PASS** | bbox and origin bit-identical; all 9 signed volumes positive; flipped fraction **0.045 %** (tolerance 0.15 %) |
| G3 Round-trip | **PASS** | Blender re-import + `g3check` (pinned three, MeshoptDecoder): 9 meshes, 16,908 tris, 9 materials, no decode errors |
| G4 Appearance | **PASS** | mean \|Δ\| **0.002–0.115 %** across day/night × near/far and four elevations (limits 2 % far / 4 % near); ×8-amplified diffs are black; nothing a player could notice |
| G5 Draw submeshes | **PASS** | 129 → 9 |
| G6 Size | **PASS with a note** | −52.8 %, short of the 60 % aspiration. The census shows the remainder is silhouette geometry: zero interior faces, zero duplicate-redundant triangles beyond the joins, dissolve skipped by policy. `-noq` is mandatory in this repo, and the residue is 29,218 float32 positions+normals of geometry that is all on the outside of the model. |
| G8 Hygiene | **PASS** | re-import object/material/bbox check in `optimize.py`; deterministic re-run; no `.blend1` |

Pixel deltas, per frame:

| frame | mean \|Δ\| RGB | max px delta |
|---|---|---|
| day_near | 0.0049 % | 10 |
| day_far | 0.0063 % | 8 |
| night_near | 0.0754 % | 103 |
| night_far | 0.1147 % | 69 |
| elev_n | 0.0092 % | 14 |
| elev_e | 0.0074 % | 15 |
| elev_s | 0.0021 % | 12 |
| elev_w | 0.0135 % | 19 |

The night maxima are Cycles denoiser variance on the emissive entrance bay at 24
samples, not a geometry change: the same pixels differ between two renders of the
*same* file, and the amplified diff shows noise, not an edge.

## Shipping swap

`hiram-johnson-state-office-building.optimized.glb` was copied over
`artifacts/hiram-johnson-state-office-building/hiram-johnson-state-office-building.glb`
and into `app/public/sf-assets/landmarks/`. The pre-optimize original is archived
byte-for-byte at `optimize/input/`. The asset's `validation.json` and `REPORT.md`
carry the shipped numbers (16,908 tris, 9 objects, 421,380 B), which is what the
manifest entry was written from.
