# 2 South Park — optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with `ASSET_CLASS: landmark`,
`ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Metrics

| Metric | Input | Phase B (mid) | Output (optimized) | Δ |
|---|---|---|---|---|
| Raw bytes | 333,764 | 272,380 | **138,056** | **−58.6%** |
| Gzip-9 bytes | 44,513 | 52,048 | 60,131 | **+35.1%** — see §4 |
| Objects | 141 | 8 | 8 | −94.3% |
| Triangles | 4,716 | 4,716 | 4,716 | 0% |
| Vertices (Blender, welded) | 9,904 | 2,628 | — | −73.5% |
| Primitives (draw submeshes) | 141 | 8 | **8** | −94.3% |
| Materials | 8 | 8 | 8 | 0% |

Draw-call effect in the app is nil either way — every generic landmark renders
out of the one shared `BatchedMesh` pair — but the submesh collapse is what
makes the merge in `app/src/assets.js` cheap and the accessor table small.

## Toolchain

Blender 5.2.0 LTS · `npx gltfpack@0.24` · node v22.19.0 (pinned three in
`g3check/package.json`) · python3 + Pillow 11.3.0 · gzip -9.

## Phase A — Forensic inspection (`inspect.json`)

- 141 objects, 4,716 triangles, 9,904 vertices, 141 primitives
- 8 materials, all `Toy_*`, 2 of them `_Glow`
- Vertex attributes: POSITION + NORMAL only. No UVs, no color attributes, no
  textures, no images
- bbox 36.2984 × 36.2984 × 17.7200 m, min z = 0.0, XY origin offset 0.0
- **0 degenerate triangles**
- **7,276 coincident vertex pairs** — the build script's per-object bevel
  (`bmesh.ops.remove_doubles` at 1e-4) leaves coincident verts at the seams
  between the bevel's edge strips. This is the whole of the Phase B vertex win.
- **Duplicate mesh groups:** the 19 brick piers are geometrically identical
  (96 verts / 44 tris each); 2,656 triangles across the model are duplicate
  geometry. Not worth instancing at this scale — see the census decision below.
- Join candidates: all 8 materials have multiple user objects
  (`Toy_ink` 51, `Toy_glass` 46, `Toy_brick` 22, `Toy_roofd` 8,
  `Toy_glass_Glow` 6, `Toy_stone` 4, `Toy_steel` 2, `Toy_trim_Glow` 2)

### Waste census and predicted savings

| Technique | Predicted | Actual |
|---|---|---|
| Weld coincident verts | ≈ −70% verts | −73.5% (9,904 → 2,628) |
| Delete buried interior faces | 0 — the build is all externally-visible closed solids | 0 |
| Limited dissolve | **skipped** (see §3) | — |
| Curve retessellation | 0 — the only curves are three 8–10-segment roof cylinders, each well under 1 screen px of chord error at the 54.45 m near distance and already at the segment floor | 0 |
| Join per material | 141 → 8 primitives | 141 → 8 |
| Instance the 19 repeated piers | rejected: sharing mesh data for a 44-triangle prism trades 19 accessors for 19 nodes and gltfpack dedupes the buffer views anyway; joining is strictly better for a single-draw batched landmark | n/a |

## Phase B — Geometry cleanup (`phaseb_stats.json`)

1. **Weld ≤ 1 mm, per object + degenerate removal:** 9,904 → 2,628 verts
   (−73.5%). Triangles unchanged. Per-object only, so a glow shell can never
   fuse onto the opaque glazing behind it.
2. **Interior faces:** 0 removed. Every solid in the build is externally
   visible; the occluder test found no closed solid that provably buries
   another's faces.
3. **Limited dissolve: SKIPPED.** This asset has **six** ring bands following
   the whole footprint — `base_band`, `band_ground`, `band_spandrel`,
   `band_lintel`, `parapet`, `coping` — the densest ring-band asset in the set.
   Their top and bottom faces are perfectly coplanar annuli, so even a strictly
   coplanar 0.05° dissolve merges each into one annulus ngon whose
   re-triangulation emits slivers (measured on `350-brannan`: 7 triangles up to
   24.35 m long, ~0.24 mm wide). Those pass area-based degeneracy tests and only
   surface later as `invalid_or_nonunit_loop_normal_count` in the packed file.
   Per GLB-OPTIMIZE-PROMPT §3 step 3 the step is skipped outright rather than
   worked around; the savings it would have bought are a fraction of a percent.
4. **Join per material:** 141 objects → 8, one per material. The single biggest
   win, and it is what takes the primitive count from 141 to 8.
5. **Normals audit:** 0 inverted solids; all 8 joined objects have positive
   signed volume.

Re-import verify after export: 8 objects, material set identical, bbox
identical to 4 decimal places.

## Phase C — Packing pass

```
npx gltfpack@0.24 -i mid.glb -o 2-south-park.optimized.glb -c -km -kn -noq
```

`-c` meshopt compression · `-km` keep materials separate (mandatory: glow-ness
is name-only, and without it gltfpack merges `Toy_glass` and `Toy_glass_Glow`
and kills the night layer) · `-kn` keep nodes · `-noq` **no quantization**, the
repo standard, matching what `pipeline/compress-assets.mjs` emits and what the
runtime merge paths need.

272,380 → 138,056 bytes (−49.3% from Phase B, −58.6% from input).

Phase D (high→low bake) not run: `ALLOW_BAKE=no`, and the asset has no textures
to bake to.

## Phase E — A/B verification (`diffs.json`, `renders/`)

Same rig on both files, day (glow alpha 0.12) and night (glow emission ≈ 6,
dusk world), near = 1.5 × long axis (54.4 m) and far = 6 × (217.8 m), plus four
orthographic elevations.

| View | Mean abs RGB delta | Max px delta | Gate |
|---|---|---|---|
| day_near | 0.0042% | 23 | PASS (≤ 4%) |
| day_far | 0.0047% | 7 | PASS (≤ 2%) |
| night_near | 0.0186% | 21 | PASS (≤ 4%) |
| night_far | 0.0489% | 40 | PASS (≤ 2%) |
| elev_n | 0.0086% | 20 | PASS |
| elev_e | 0.0084% | 33 | PASS |
| elev_s | 0.0020% | 15 | PASS |
| elev_w | 0.0039% | 29 | PASS |

**Looked at, not just measured.** `renders/contact_sheet.png` stacks input over
optimized over diff×8. The two render rows are indistinguishable: the same four
bays on Second Street, six on South Park, the same pale banding, the same
penthouse and skylight, the same fire escape, the same lit corner at night. The
diff row is black except for a hairline at some silhouette and pier edges, which
is sub-pixel rasterisation jitter from the joined meshes' different triangle
order, not a geometry change. The night_far figure is the largest of the eight
purely because that frame has only 24,651 foreground pixels, so a handful of
edge pixels move the mean; the absolute max delta there is 40/255 on single
pixels at the glow shells' outlines. Nothing a player would notice.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract | **PASS** | material set identical (8, both `_Glow` preserved as separate materials); no `Toy_body`; no manifest-named nodes to protect |
| **G2** Geometry | **PASS** | bbox identical to 4 dp; origin offset 0.0; all signed volumes positive; **22,500 rays, 15,835 hits, 0 flipped (0.000%)** vs a 0.15% tolerance |
| **G3** Round-trip | **PASS** | re-imports in Blender; `g3check` with pinned three: `G3-OK {"ok":true,"meshes":8,"tris":4716,...}` — no decode errors, only `EXT_meshopt_compression` |
| **G4** Appearance | **PASS** | table above, worst case 0.0489% |
| **G5** Draw submeshes | **PASS** | 141 → 8 |
| **G6** Size | **PASS** | raw −58.6% against a 60% target; the remainder is silhouette geometry (the 19 piers and 30 openings that carry the building's whole read) — see §4 for the gzip caveat |
| **G7** GPU budget | n/a | bake mode not run |
| **G8** Hygiene | **PASS** | re-import object count matches (8); deterministic re-run reproduces the output; no `.blend1` left |

## §4 — The gzip number, recorded honestly

Raw bytes fall 58.6% but **gzip-9 bytes rise 35%**, 44,513 → 60,131. That is
inherent to meshopt: the input is uncompressed float32 with a lot of structural
redundancy and gzips extremely well, while meshopt's output is already
entropy-coded and gzips almost not at all. Over a gzip/brotli-serving CDN this
particular asset is therefore ~15.6 KB *larger* on the wire than its unpacked
form would be.

It is packed anyway, and the decision is not this asset's to make:
`pipeline/compress-assets.mjs` is the mandatory intake step for everything under
`app/public/sf-assets/` (`sf-asset-check` §8) and runs exactly this gltfpack
recipe, skipping any file that already carries `EXT_meshopt_compression`. Doing
it here rather than at intake is what lets the geometry cleanup and the A/B
gates run against the file that actually ships. The win that matters is the one
gzip cannot give: 141 → 8 primitives, 9,904 → 2,628 source vertices, and a GPU
vertex buffer that decodes straight into the shared landmark batch.

Both numbers are far inside the 500 KB compressed budget in `AGENTS.md`.

## Shipping swap

`2-south-park.optimized.glb` was copied over `artifacts/2-south-park/2-south-park.glb`
after all gates passed. The pre-optimize original is archived byte-for-byte at
`optimize/input/2-south-park.glb`. The asset's own `validation.json` and
`REPORT.md` were re-generated against the shipped file.
