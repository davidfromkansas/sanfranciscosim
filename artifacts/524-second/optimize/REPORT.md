# 524 Second Street — GLB optimize report (stage 4)

Run 16 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Toolchain:** Blender 5.2.0 LTS (headless), `npx gltfpack@0.24`, node + the pinned three
in `g3check/package.json`, python3 + Pillow, gzip −9. Scripts are adapted copies of
`tools/glb-optimize/`; the only per-asset change is the deliberate skip in Phase B step 3
documented in §3.

## 1. Metrics

| | input | output | delta |
|---|---|---|---|
| File, raw | 344,840 B | **160,572 B** | **−53.4%** |
| File, gzip −9 | 54,989 B | 104,048 B | +89% (see §4) |
| Triangles | 5,620 | 5,620 | 0 |
| Vertices (Blender, post-weld) | 11,432 | 3,016 | −73.6% |
| Vertices (glTF, re-imported) | 11,432 | 10,248 | −10.4% |
| Objects / nodes | 105 | **10** | −90.5% |
| Draw submeshes (primitives) | 106 | **11** | −89.6% |
| Materials | 9 | 9 | identical set |
| bbox dims | 35.9981 × 35.7656 × 9.9 | 35.9981 × 35.7656 × 9.9 | 0 |
| bbox min | −17.99906, −17.88282, 0.0 | −17.99906, −17.88282, 0.0 | 0 |

160 KB is well under the 500 KB on-disk landmark budget.

## 2. Waste census (Phase A)

`inspect.json`. The asset is 105 small closed solids authored with no booleans, so the
waste is concentrated exactly where that construction puts it:

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Coincident vertices | **8,416 pairs** — every box and panel is flat-shaded and authored corner-by-corner | large vertex win | 11,432 → 3,016 verts |
| Duplicate mesh groups | 15 groups, 3,172 redundant triangles (the 12 merlons, 5 roof vents, 15 window fills/frames repeated at identical size) | join, not instance — the counts are small and each is < 100 tris | folded into the per-material join |
| Object-count overhead | 105 nodes for 9 materials; join candidates `Toy_glass` 30, `Toy_roofd` 30, `Toy_stone` 26, `Toy_brick` 5 | the single biggest byte win | 105 → 10 objects, 106 → 11 primitives |
| Degenerate faces | 0 | none | 0 |
| Buried interior faces | the entry bay overlaps two window frames; the 12 merlons straddle the parapet ring | the occluder rule needs a CLOSED, box-like solid (AABB fill ≥ 95%); a parapet is a ring, so nothing qualifies | 0 removed — correctly declined |
| Over-tessellated curves | none. Every surface is a planar panel, box or prism | n/a | n/a |

## 3. Phase B — what ran, and the one step that did not

Steps 1, 2, 5 and 7 ran. Step 4 (curve retessellation) is not applicable — there is no
curved geometry in this asset.

**Step 3, limited dissolve, was deliberately skipped**, per prompt §3 step 3:

> "Skip this step entirely on assets with large coplanar ring bands — a parapet, coping,
> string course or cornice that follows the footprint all the way round."

524 Second has **two such rings stacked**: the parapet (8.96–9.20 m) and the coping
(9.20–9.32 m), each following the full 101 m footprint perimeter. Their top and bottom
faces are perfectly coplanar annuli, so even a strictly-coplanar 0.05° dissolve merges
each into one annulus ngon, and re-triangulating an annulus emits ~0.24 mm slivers up to
30 m long. Those pass an area-based degeneracy test, survive Phase B and Phase E, and
then surface **only in the packed file** as `invalid_or_nonunit_loop_normal_count` — because
gltfpack re-emits stored normals while Blender recomputes them on import. Measured on
`350-brannan`, 13 August 2026, where the step was worth 0.4%.

**This was verified, not just asserted:** the stage-2 contract validator
(`validate_524_second.py`) was re-run against the *packed* shipping file after the swap
and returns `overall: PASS` with `invalid_or_nonunit_loop_normal_count: 0`. Skipping the
step cost nothing measurable — the join is where the bytes were.

Interior-face deletion found no provable occluders and removed nothing. That is the
correct outcome under the hard-learned occluder rule, not a miss: the overlaps in this
asset are against a ring (the parapet) and against panel frames, none of which is a
closed box-like solid.

## 4. Phase C — packing, and why gzip goes up

```
npx gltfpack@0.24 -i mid.glb -o 524-second.optimized.glb -c -km -kn -noq
```

`-km -kn` are mandatory (glow-ness is name-only; without `-km` gltfpack would merge
`Toy_glass` and `Toy_glass_Glow` and silently kill the night layer — verified: the output
material set is identical to the input's, all 9 names present). `-noq` is the repo
standard and matches `pipeline/compress-assets.mjs`, which is the mandatory ship step;
quantization breaks the kit merge path and fails the stage-2 validator on
`transforms_applied` / `no_unexpected_objects`.

**The gzip number goes up, and that is expected.** Meshopt buffers are already
entropy-coded, so gzipping them again adds overhead rather than removing it:
54,989 B → 104,048 B. The number that matters on disk and over the wire is the raw file,
because the server does not re-compress an already-compressed payload. Same behaviour
recorded for `358-brannan` (40,862 → 77,591 B) and every other meshopt landmark.

`compress-assets.mjs` will skip this file at integration — it refuses to re-pack anything
already carrying `EXT_meshopt_compression`. That is the intended handoff.

## 5. Phase E — A/B appearance

`render_ab.py` on both files, same rig: 42° aerial, near = 1.5 × long axis = 54.0 m,
far = 6 × long axis = 216.0 m, day (glow alpha 0.12) and night (alpha 1.0, emission 6,
dusk world), plus four orthographic elevations. `diff_ab.py` → `diffs.json`.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| day near | 0.0075% | 31 |
| day far | 0.0063% | 4 |
| night near | 0.0330% | 22 |
| night far | 0.0344% | 20 |
| elev N | 0.0087% | 39 |
| elev E | 0.0063% | 21 |
| elev S | 0.0065% | 31 |
| elev W | 0.0082% | 17 |

Gates are ≤ 2% far and ≤ 4% near; the worst view here is 0.034%, roughly two orders of
magnitude inside tolerance.

**Looked at, not just measured.** In `renders/contact_sheet.png` the input and optimized
rows are indistinguishable. The ×8-amplified diff row shows nothing but a faint stipple
along the parapet coping edge and around window-frame borders — sub-pixel antialiasing
shifts from the vertex weld, at most 39/255 on a single pixel at a silhouette edge. No
element is missing, the merlon row is intact and unchanged in count and spacing, the
silhouette is identical, the night glow set is identical (three lit windows on Second
Street, two on Taber Place, the entrance sign), and there are no shading artifacts.
Nothing here is anything a player could notice.

## 6. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material name set identical (9); `_Glow` materials separate; no `Toy_body`; no manifest-referenced node names on this asset |
| G2 Geometry | **PASS** | bbox delta 0.00000 m; origin delta 0.00000 m; all 10 output solids positive signed volume; `inverted_solids: []`; ray flipped fraction **0.0** over 16,209 hits |
| G3 Round-trip | **PASS** | re-imports in Blender; `g3check` → `G3-OK`, 11 meshes, 5,620 tris, 9 materials, bbox matches, no decode errors |
| G4 Appearance | **PASS** | worst mean delta 0.034% vs 2–4% gates; visual description above |
| G5 Draw submeshes ≤ input | **PASS** | 106 → 11 |
| G6 Size reduced | **PASS on size, short of the 60% target** | −53.4% raw. See §7 |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | **PASS** | re-import object/material/bbox check clean; deterministic re-run reproduces the output; no `.blend1` files |

## 7. Judgment call on G6

−53.4% against a 60% aspirational target. The census supports stopping here: after the
weld there are 3,016 vertices carrying 5,620 triangles across 10 objects, the primitive
count is down to 11, and there is no duplicate mesh, no degenerate face, no over-tessellated
curve and no provably buried face left to spend. The remaining bytes are the vertex buffer
of a building whose entire surface is silhouette or facade rhythm — 12 merlons that are
the identity cue, 15 glazed bays across two public elevations, and a roof the app's camera
looks straight at. The only way to go further is to delete geometry the asset exists to
show. Consistent with `358-brannan` (−52.6%) and `380-brannan` under the same `-noq` recipe;
the 60% figure in the prompt was measured with quantization on.

## 8. Shipping swap

`524-second.optimized.glb` copied over `artifacts/524-second/524-second.glb`. The
pre-optimize original is archived byte-for-byte at `optimize/input/524-second.glb`
(344,840 B). The asset's `validation.json` and `REPORT.md` were regenerated against the
shipped file, so the integration stage writes its manifest entry from reality.
