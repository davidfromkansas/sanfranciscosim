# 560 Third Street — GLB optimize pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 with the defaults:
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: all gates PASS. The optimized file is now the shipping
`artifacts/560-third/560-third.glb`;** the pre-optimize original is archived
byte-for-byte at `optimize/input/560-third.glb`
(sha1 `ff7a088d7885ff85fd89f1e8df6d955768c47bb9`).

## Metrics

| | input | shipped | delta |
|---|---:|---:|---:|
| Raw bytes | 141,796 | **67,892** | **−52.1%** |
| gzip -9 bytes | 29,099 | 48,019 | +65.0% (see note) |
| Triangles | 2,356 | 2,356 | 0 |
| Vertices | 4,736 | 4,127 | −12.9% |
| Mesh objects | 33 | **8** | −75.8% |
| Draw submeshes (primitives) | 33 | **8** | −75.8% |
| Materials | 8 | 8 | identical set |
| bbox dims (m) | 23.9031 × 24.0636 × 7.2000 | identical | 0 |
| bbox min / origin offset | (−12.1026, −12.1131, 0.0) | identical | 0 |

**The gzip row is not a regression to fix.** Meshopt-encoded buffers are already
entropy-coded, so they gzip poorly; that is true of every meshopt asset in this
repo. Meshopt compression is *mandatory* on intake regardless
(`AGENTS.md` asset-pipeline §, `sf-asset-check` §8,
`pipeline/compress-assets.mjs`), and what it buys is decode-side: the shipped
file is what the CDN stores, `EXT_meshopt_compression` decodes on the worker,
and the vertex buffer reaching the GPU is smaller. Recorded here honestly rather
than quietly omitted.

The headline win of this pass is **33 → 8 draw submeshes**, not the bytes: every
generic landmark renders out of one shared `BatchedMesh` pair, and submesh count
is what the merge path pays for.

## Phase A — waste census

`inspect.py` on the input (`inspect.json`):

| Finding | Size | Verdict |
|---|---|---|
| 3,496 coincident vertex pairs | ~74% of all verts | **fixed** by the per-object 1 mm weld (4,736 → 1,240 verts mid-pass) |
| 33 objects sharing only 8 materials | 33 primitives | **fixed** by join-per-material → 8 |
| Duplicate mesh groups: `plant0/plant1`, 3 band mullions, 2 shop mullions, 2 skylight frames, 2 skylight glows, 2 skylight panes, 2 vents | 308 redundant tris | joined, not instanced — counts are 2–3, far below the threshold where shared mesh data beats node overhead |
| Two 8-segment vent cylinders | 376 tris (16% of the asset) | **left alone**, see §"judgment calls" |
| Degenerate triangles | 0 | nothing to do |
| Buried interior faces | 0 removable | no object qualifies as an occluder: the shell is a 44°-rotated diamond, so its AABB fill is ~50%, well under the 95% rule |
| Textures | none | n/a |

## Phase B — geometry cleanup (`optimize.py`, `phaseb_stats.json`)

| Step | tris | verts |
|---|---:|---:|
| input | 2,356 | 4,736 |
| 1+2a weld ≤ 1 mm + degenerate, per object | 2,356 | 1,240 |
| 2b interior faces buried in closed solids | 2,356 | 1,240 (0 removed) |
| 3 limited dissolve | **SKIPPED** — see below |
| 5 join per material | 2,356 | 1,240 (33 → 8 objects) |
| 7 normals audit | all signed volumes positive, `inverted_solids: []` | |

**Step 3 was skipped deliberately, per the prompt's own §3.3 rule.** This asset
has three large coplanar ring bands that follow the whole footprint — the
parapet ring, the steel coping ring, and the annulus where the membrane field is
inset from the parapet. A strictly-coplanar dissolve merges each into a single
ngon, and re-triangulating an annulus emits hairline slivers that pass every
area-based degeneracy test and only surface *after* the shipping swap, in the
packed file, as `invalid_or_nonunit_loop_normal_count`. The measured saving on
`350-brannan` was 30 triangles (0.4%); on a 2,356-triangle asset it would be
smaller still. Not worth the failure mode. The skip is recorded in
`phaseb_stats.json` as a step, not silently omitted.

Step 4 (curve retessellation) had one candidate and was declined — see below.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 560-third.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API here: `Toy_*_Glow` is
name-only glow-ness, and without `-km` gltfpack merges identical-parameter
materials across the glow boundary and silently kills the night layer. `-noq`
(no quantization) is the repo standard and is what `compress-assets.mjs`
produces. Verified on the output, not trusted from the flags: material set
identical (8), bbox identical, node names present, `EXT_meshopt_compression`
only.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and there is nothing to bake: the asset has no
textures, one designed elevation, and 2,356 triangles.

## Phase E — A/B verification (`diffs.json`, `renders/`)

Same rig for both files: 42° aerial, near = 1.5 × long axis (36.1 m),
far = 6 × long axis (144.4 m), day (glow at 12% alpha) and night (glow lit),
plus four elevations.

| View | mean abs RGB delta | max px delta |
|---|---:|---:|
| day_near | 0.0034% | 24 |
| day_far | 0.0037% | 4 |
| night_near | 0.0096% | 15 |
| night_far | 0.0140% | 8 |
| elev_n / e / s / w | 0.0032 / 0.0041 / 0.0063 / 0.0054% | 35 / 27 / 32 / 15 |

Gate G4 allows ≤ 2% far and ≤ 4% near; the worst view here is 0.014%.

**Looked at, not just measured.** The ×8-amplified diffs
(`renders/diff_*.png`, `renders/contact_sheet.png`) are black except for
single-pixel threads along silhouette edges — anti-aliasing landing differently
where the weld moved a vertex by sub-millimetre amounts. `renders/night_triptych.png`
puts the night pair side by side: both skylights and the four-pane warm street
band are present and identical in the optimized file, which is the check that
matters, because a lost `_Glow` split is the failure mode this pass is most
likely to cause and it is invisible by day. Nothing here is anything a player
would notice.

The weld is also the step that has historically flattened flat-shaded surfaces
on other assets in this repo; the elevation diffs are the check for that, and
they are clean — no shading banding appears on the membrane field, the parapet
faces or the roof plant.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | PASS | material set identical (8, both `_Glow` materials separate); no `Toy_body`; node names intact |
| **G2 Geometry** | PASS | bbox identical to 5 dp; origin identical; all 8 signed volumes positive; ray test 22,500 rays / 15,302 hits / **0 flipped** |
| **G3 Round-trip** | PASS | Blender re-import OK; `g3check` (pinned three 0.185.1 + MeshoptDecoder) → `G3-OK … meshes:8 tris:2356`, no decode errors |
| **G4 Appearance** | PASS | worst mean delta 0.014% against a 2%/4% budget; diffs inspected, glow layer intact |
| **G5 Draw submeshes** | PASS | 33 → 8 |
| **G6 Size** | PASS with note | −52.1% raw against a 60% aspiration. The census shows the remainder is real shell: 2,356 triangles, 0 degenerate, 0 removable interior faces, and the only fat left is 376 triangles of vent cylinder that were kept on purpose. Nothing further can be removed without removing silhouette. |
| **G7 GPU budget** | n/a | bake mode not run |
| **G8 Hygiene** | PASS | re-import object count matches; deterministic re-run reproduced `mid.glb` and the packed file **byte-identical** (sha1 `c912128e…`); no `.blend1` files |

The stage-2 contract validator (`../validate_560_third.py`) was re-run against
the **shipped, packed** file and returns `overall: PASS` on all 16 checks —
which is the check that would have caught dissolve slivers, and is the reason
Phase B step 3 was skipped rather than worked around.

## Judgment calls

1. **Limited dissolve skipped** (Phase B §3) — coplanar ring bands, per the
   prompt's explicit rule. Cost: perhaps 20–30 triangles unrealised.
2. **Vent cylinders kept at 8 segments.** `inspect.py` reports one screen pixel
   = 0.0243 m at the 36.1 m near distance, and an 8-segment 0.20 m-radius
   cylinder has a chord error of 0.015 m — under the threshold, so halving is
   *technically* allowed. Declined: at 4 segments a vent becomes a visibly square
   post on a roof that has only five objects on it, and the saving is 188
   triangles on an asset already 71% under its 8,000 cap. Byte-shaving that
   costs a shape is the wrong trade here.
3. **Duplicates joined, not instanced.** The largest duplicate group is three
   band mullions; sharing mesh data at counts of 2–3 costs more in node overhead
   than it saves.
4. **`-noq` kept.** Not re-opened — see the prompt's §4 note.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash `fbe6228777e7`, 2026-07-14) |
| gltfpack | 0.24 (`npx gltfpack@0.24`, pinned) |
| three (g3check) | 0.185.1 (pinned in `g3check/package.json`) |
| Python | 3.9 + Pillow |
| gzip | `gzip -9` |

## Reproduce

```bash
cd artifacts/560-third/optimize
blender -b --python inspect.py  -- input/560-third.glb inspect.json
blender -b --python optimize.py -- input/560-third.glb mid.glb phaseb_stats.json
npx gltfpack@0.24 -i mid.glb -o 560-third.optimized.glb -c -km -kn -noq
blender -b --python validate.py -- input/560-third.glb 560-third.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../560-third.optimized.glb)
blender -b --python render_ab.py -- input/560-third.glb        renders/in
blender -b --python render_ab.py -- 560-third.optimized.glb    renders/out
python3 diff_ab.py
cp 560-third.optimized.glb ../560-third.glb    # the shipping swap
```
