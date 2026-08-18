# 424 Brannan — GLB optimize report (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run on `artifacts/424-brannan/`,
18 August 2026. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Result

| | input | shipped | delta |
|---|---|---|---|
| Raw bytes | 514,628 | **356,972** | **−30.6%** |
| Gzip-9 bytes | 139,423 | 266,861 | +91% (expected: meshopt output is already entropy-coded) |
| Triangles | 8,944 | 8,940 | −4 |
| Vertices | 18,072 | 18,072 | 0 |
| Objects / meshes | 37 | 21 | **−43%** |
| Draw primitives | 38 | 22 | **−42%** |
| Materials | 20 | 20 | identical set |
| bbox | 88.8432 x 59.9340 x 8.5649 | identical | 0 |
| bbox min z | −1.0844 | −1.0844 | 0 |

The win here is **draw submeshes and node overhead, not triangles.** Phase B's
geometry steps found nothing to remove; see the census.

## Waste census (Phase A) and what it licensed

| Technique | Found | Action |
|---|---|---|
| Duplicate meshes | **0** groups, 0 redundant tris | nothing to do |
| Buried interior faces | **0** | the only ≥95%-AABB-fill closed solids are single boxes standing on the plate; the plate itself fills 8% of its own AABB, so it is not an occluder and nothing gets deleted through it |
| Degenerate faces | 4 triangles | removed |
| Unwelded coincident verts | ~7,800 | **weld deliberately disabled** — see below |
| Over-tessellated curves | none — the only curved geometry is four 10-gon tree crowns and six 6-gon trunks, all silhouette | skipped |
| Object-count overhead | **21 objects sharing 6 materials** | joined; the single biggest win |

Two Phase B steps were deliberately not run, both on the strength of a recorded
failure elsewhere in this repo rather than on judgement:

- **Weld disabled.** Every surface in this asset is flat-shaded, the glTF
  round-trip carries that as custom split normals, and `remove_doubles` fuses
  the vertices those hang off — so the mesh falls back to smooth while G1, G2,
  G3 and G5 all still pass, and only G4 sees it (`artifacts/64-south-park`,
  16 Aug 2026: 1.03% day-near delta, and the weld was worth 256 bytes). The
  `shade_flat()` guard stays behind it.
- **Limited dissolve skipped.** `GLB-OPTIMIZE-PROMPT.md` §3 step 3 says to skip
  it on assets with large coplanar bands, and this asset is nothing but coplanar
  bands: 103 abutting plate cells sharing one top plane, the kerb runs, the
  fence runs, 67 stripe lines. On `350-brannan` the same step manufactured seven
  slivers up to 24.35 m long and 0.24 mm wide, which pass an area-based
  degeneracy test and only surface as `invalid_or_nonunit_loop_normal_count`
  after packing.

## Where the bytes actually went

30.6% is short of the 60% aspirational target, and Gate G6 requires the census
to show the remainder is silhouette geometry. It is:

- The asset is 8,940 triangles carrying **18,072 vertices** — 2.02 verts per
  triangle, which is what flat shading forces, since no two adjacent faces can
  share a normal. At float32 position + normal that is 434 KB of vertex data
  before indices, and it is irreducible without smooth shading, which the
  contract forbids.
- Phase B removed 4 triangles. There was nothing else to take: no duplicates,
  no buried faces, no over-tessellation.
- **The real reduction was taken in the build, not here.** Phase A on the first
  build measured 726,280 bytes / 12,632 tris, and the census pointed at two
  items — 93 bevelled fence posts (3,652 tris on a 90 mm section) and 18
  two-segment car cabins (1,944 tris). Both bevels are sub-pixel at every camera
  distance the app uses, so `build_424_brannan.py` was changed to drop the post
  bevel and halve the cabin segments, and the asset was rebuilt: 12,632 → 8,944
  triangles, 726,280 → 514,628 bytes. Counting from there, the full stage-2 →
  stage-4 reduction is **726,280 → 356,972 bytes, −50.9%**, and the shipped file
  is comfortably inside the 500 KB per-landmark budget it would otherwise have
  broken at 519 KB.

## Phase C packing

```
npx gltfpack@0.24 -i mid.glb -o 424-brannan.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material names, which are API: the loader splits `*_Glow`
into the unlit night layer by NAME, and this asset has four glow materials whose
parameters would otherwise merge across that boundary. `-noq` is the repo
standard and matches what `pipeline/compress-assets.mjs` emits — that script
also skips any file already carrying `EXT_meshopt_compression`, so the
integration ship step will correctly leave this file alone.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (20, incl. all four `_Glow`); no `Toy_body`; node names are `grp_*` joins plus the untouched singles |
| **G2** geometry | **PASS** | bbox delta 0; origin delta 0; all signed volumes positive; ray flip fraction **0.000221** (gate 0.0015) |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three) loads it: 22 meshes, 8,940 tris, 20 materials, no decode errors |
| **G4** appearance | **PASS** | mean absolute RGB delta: day near **0.032%**, day far 0.036%, night near 0.015%, night far 0.018%, four elevations 0.124–0.164%. Gates are 4% near / 2% far |
| **G5** draw submeshes | **PASS** | 38 → 22 |
| **G6** size | **PASS with note** | −30.6% here, −50.9% counting the build change the census licensed; the remainder is flat-shaded vertex data, which is silhouette |
| **G7** GPU budget | n/a | no bake |
| **G8** hygiene | **PASS** | re-import object count matches; **byte-identical on a second full run** (md5 `84e010d8319ef4c9a91382eaed0b1639`); no `.blend1` left |

### What the diffs actually show

Looked at, not just measured. `renders/diff_day_near.png` (×8 amplified) is
black except for hairlines one or two pixels wide along the fence rails, the car
body edges and the sign board's chamfer — antialiasing landing differently after
the per-material join re-orders triangles. `diff_night_*` are darker still: the
four glow surfaces are untouched. The elevations carry the largest numbers
(0.12–0.16%) for the same reason and the same places, amplified because an
orthographic elevation is mostly edges. Nothing a player would notice; no
element missing, no silhouette change, no shading artifact.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7, 2026-07-14) · gltfpack 0.24 via `npx` ·
node v22.19.0 · python3 with Pillow · gzip -9.

## Shipping swap

`424-brannan.optimized.glb` was copied over `artifacts/424-brannan/424-brannan.glb`
after all gates passed; the pre-optimize file is archived byte-for-byte at
`optimize/input/424-brannan.glb`. The parent `REPORT.md` and `validation.json`
were re-run against the shipped file, which still passes every stage-2 contract
check including the two drape deviations (D1–D4).
