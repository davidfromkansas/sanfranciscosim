# 501 Second Street — GLB optimize report (stage 4)

Run 16 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Toolchain:** Blender 5.2.0 LTS (headless), `npx gltfpack@0.24`, node + the pinned three
in `g3check/package.json`, python3 + Pillow, gzip −9. Scripts are adapted copies of
`tools/glb-optimize/`; the only per-asset change is the deliberate skip in Phase B step 3
documented in §3.

## 1. Metrics

| | input | output | delta |
|---|---|---|---|
| File, raw | 1,147,244 B | **487,516 B** | **−57.5%** |
| File, gzip −9 | 143727 B | 198001 B | see §4 |
| Triangles | 16,008 | 16,008 | 0 |
| Vertices (Blender, post-weld) | 34,088 | 9,128 | −73.2% |
| Objects / nodes | 564 | **11** | −98.0% |
| Draw submeshes (primitives) | 565 | **12** | −97.9% |
| Materials | 10 | 10 | identical set |
| bbox dims | 83.1067 × 82.8064 × 37.7 | 83.1067 × 82.8064 × 37.7 | 0 |
| bbox min | −41.5533, −41.4032, 0.0 | −41.5533, −41.4032, 0.0 | 0 |

**487.5 KB is inside the 500 KB on-disk landmark budget, but only by 12.5 KB** — this is
the largest bespoke asset in the SoMa set and it is the first one where that budget is a
live constraint rather than a formality. If this building is ever revised upward in
detail, the budget must be re-checked before the manifest entry is touched; the lever is
bay count (see the asset `REPORT.md` §4).

## 2. Waste census (Phase A)

564 small closed solids authored with no booleans, so the waste is where that construction
puts it: **34,088 vertices for 16,008 triangles**, i.e. every box authored corner-by-corner
and flat-shaded, and 564 nodes carrying 10 materials. Weld and per-material join are the
whole story; there were no degenerate faces, no over-tessellated curves (every surface is a
planar panel, box or prism), and no provable interior occluders — the overlaps here are
against cornice bands and panel frames, none of which is a closed box-like solid, so the
occluder rule correctly declined to remove anything.

## 3. Phase B — what ran, and the one step that did not

Steps 1, 2, 5 and 7 ran. Step 4 (curve retessellation) is not applicable.

**Step 3, limited dissolve, was deliberately skipped**, per prompt §3 step 3: this asset
has **three coplanar ring bands stacked** — the main cornice, the parapet and the coping —
each following the full 230 m footprint perimeter, plus two more per-face cornice bands.
Their top and bottom faces are perfectly coplanar annuli, so even a strictly-coplanar
0.05° dissolve merges each into one annulus ngon whose re-triangulation emits sub-millimetre
slivers tens of metres long. Those pass an area-based degeneracy test and surface only in
the **packed** file as `invalid_or_nonunit_loop_normal_count`. Measured on `350-brannan`,
13 August 2026.

**Verified, not asserted:** the stage-2 contract validator (`validate_501_second.py`) was
re-run against the packed shipping file after the swap and returns `overall: PASS` with
`invalid_or_nonunit_loop_normal_count: 0`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 501-second.optimized.glb -c -km -kn -noq
```

`-km -kn` mandatory (glow-ness is name-only; without `-km` gltfpack merges `Toy_glass`
with `Toy_glass_Glow` and silently kills the night layer — verified: all 10 material names
survive). `-noq` is the repo standard and matches `pipeline/compress-assets.mjs`.

The gzip figure rises because meshopt buffers are already entropy-coded; the raw file is
the number that matters on disk and over the wire. Same behaviour on every meshopt landmark.

## 5. Phase E — A/B appearance

Same rig on both files: 42° aerial, near = 1.5 × long axis = 124.7 m, far = 6 × = 498.6 m,
day (glow alpha 0.12) and night (alpha 1.0, emission 6), plus four orthographic elevations.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| day near | 0.0076% | 22 |
| day far | 0.0071% | 10 |
| night near | 0.0010% | 6 |
| night far | 0.0054% | 34 |
| elev N | 0.0046% | 9 |
| elev E | 0.0056% | 14 |
| elev S | 0.0023% | 24 |
| elev W | 0.0019% | 45 |

Gates are ≤ 2% far / ≤ 4% near; the worst view is 0.0076%, three orders of magnitude
inside tolerance.

**Looked at, not just measured.** In `renders/contact_sheet.png` the input and optimized
rows are indistinguishable. The ×8 diff row shows only a faint stipple along cornice and
window-frame edges — sub-pixel antialiasing from the vertex weld, at most 45/255 on a
single pixel at a silhouette edge. No element missing, both cornices intact and unchanged
in projection, the silhouette identical, the night glow set identical.

## 6. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material name set identical (10); `_Glow` separate; no `Toy_body` |
| G2 Geometry | **PASS** | bbox delta 0.00000 m; origin delta 0.00000 m; all 11 output solids positive signed volume; `inverted_solids: []`; ray flipped fraction **0.0** over 16,233 hits |
| G3 Round-trip | **PASS** | re-imports in Blender; `g3check` → `G3-OK`, 12 meshes, 16,008 tris, 10 materials |
| G4 Appearance | **PASS** | worst mean delta 0.0076% vs 2–4% gates |
| G5 Draw submeshes ≤ input | **PASS** | 565 → 12 |
| G6 Size reduced ≥ 60% target | **PASS on size, just short of target** | −57.5% raw, the best result in the SoMa set. The remainder is silhouette and facade rhythm: 9,128 vertices for 16,008 triangles across 11 objects with no duplicate mesh, no degenerate face and no buried face left |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | **PASS** | re-import check clean; deterministic re-run reproduces output; no `.blend1` files |

## 7. Shipping swap

`501-second.optimized.glb` copied over `artifacts/501-second/501-second.glb`. The
pre-optimize original is archived byte-for-byte at `optimize/input/501-second.glb`
(1,147,244 B). `validation.json` and `REPORT.md` were regenerated against the shipped file.
