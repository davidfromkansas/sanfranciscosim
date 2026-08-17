# 84 South Park — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/84-south-park/`, 17 August 2026. **Run twice**: once on the first
shipped build, and again from scratch after stage 5 sent the body colour back to
stage 2 (see the parent `REPORT.md`, correction 1). The numbers below are the
second run. They are identical to the first apart from gzip noise, because the
change was a material colour and this pass never touches a triangle.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 383,108 B (374.1 KB) | **185,352 B (181.0 KB)** | **−51.6%** |
| File, gzip -9 | 62,116 B (60.7 KB) | 126,473 B (123.5 KB) | **+103.6%** — see §G6 |
| Objects / nodes | 65 | **11** | −83.1% |
| Draw submeshes (primitives, via GLTFLoader) | 67 | **12** | −82.1% |
| Triangles | 6,900 | 6,900 | 0 |
| Vertices (Blender re-import) | 13,714 | **11,383** | −17.0% |
| Materials | 12 | 12 | identical set |
| bbox dims | 26.08563 × 26.29176 × 13.20000 m | 26.08563 × 26.29176 × 13.20000 m | 0 |
| bbox min | −13.04282, −13.14588, 0.0 | −13.04282, −13.14588, 0.0 | 0 |

Toolchain: Blender 5.2.0 LTS (`fbe6228777e7`, 2026-07-14); `npx gltfpack@0.24`;
node + the pinned three in `g3check/package.json`; python3 + Pillow; gzip -9.

The input was copied byte-for-byte to `optimize/input/84-south-park.glb` and
verified with `cmp` before any step ran; every step below ran against the copy.

## Phase A — waste census

`inspect.json`. The asset came in as 65 flat-shaded closed prisms, one per
feature, sharing 12 materials. Three predictions, one of which was wrong:

- **Split vertices.** 6,900 triangles carrying 13,714 vertices — glTF splits
  vertices for flat shading, so every prism's corners are duplicated per face.
  Predicted recovery from a 1 mm per-object weld: ~70%. **Realised: 17%.** See
  Phase B.
- **Object-count overhead.** 65 nodes and 67 primitives for 12 materials.
  Predicted recovery from join-per-material: ~83% of the node/accessor
  overhead. **Realised: 83.1% / 82.1%** — this was the whole win.
- **Buried interior faces: none predicted, none found.** The build script places
  every feature proud of or recessed into a wall or deck plane and never nests
  one solid inside another, so nothing is provably invisible.
- **Over-tessellated curves: none.** There are no curves in this asset — the
  tree canopy and trunk are beveled boxes, not lathes.

## Phase B — geometry cleanup

`optimize.py` → `mid.glb`, `phaseb_stats.json`.

| Step | Tris | Verts (Blender-side) |
|---|---|---|
| input | 6,900 | 13,714 |
| weld ≤1 mm + degenerate removal | 6,900 | 3,576 |
| interior faces (0 removed) | 6,900 | 3,576 |
| limited dissolve — **SKIPPED** | 6,900 | 3,576 |
| join per material | 6,900 | 3,576 |

Joins: `Toy_trim` 18 objects, `Toy_glass` 17, `Toy_ink` 14, `Toy_mint` 6,
`Toy_glassl_Glow` 2, `Toy_roofd` 2, and the two 2-material shells
(`body`, `rear_wing`) into `grp_Toy_slate_Toy_stone`. Four singletons
(`door`, `rear_face`, `slot_glow`, `tree_trunk`) stayed as they were. 65 → 11.

**Limited dissolve deliberately skipped** (prompt §3.3). This asset has *two*
coplanar ring bands — `parapet` is a closed annulus round the whole
6.99 × 22.90 m main roof and `rear_parapet` is a second one round the
6.99 × 7.17 m rear wing — plus the long coplanar strips of the entrance slot and
the projecting box. Re-triangulating an annulus ngon emits slivers up to the full
ring length; they pass every area-based degeneracy test and surface only *after*
the shipping swap, as `invalid_or_nonunit_loop_normal_count` in the stage-2
contract validator (precedent: `350-brannan`, 13 Aug 2026). The step was worth at
most a handful of triangles here, so it was not worth working around. **The
shipped file's `invalid_or_nonunit_loop_normal_count` is 0**, which is the check
that proves the skip was the right call.

**The weld's headline number does not survive export, and that is expected.**
The per-object weld took the Blender-side count from 13,714 to 3,576, but the
model is flat-shaded, so the glTF exporter re-splits every corner whose face
normals differ. The re-imported optimized file carries 11,383 vertices — a real
but modest 17% saving, from corners whose normals genuinely matched. Recorded
because the 106 South Park run realised ~73% on the same script and a reader
comparing the two reports would otherwise think something regressed here: the
difference is geometry, not method. This asset has proportionally more small
boxes (skylight kerbs, pergola beams, planters) whose every corner is a
three-way normal discontinuity.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 84-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept, `-noq` kept: the repo standard is unquantized (prompt §4). The
material name set is identical across the pack, verified on the output rather
than trusted from the flags, and `_Glow` stayed separate — `Toy_glassl_Glow` and
`Toy_trim_Glow` both survive as distinct materials in the packed file, which is
the thing `-km` exists to protect.

## Phase D — high→low bake

Not run. `ALLOW_BAKE: no`.

## Phase E — A/B verification

`render_ab.py` on both files with one rig (42° elevation aerial, azimuth 172°,
40° FOV, near = 1.5× long axis, far = 6×), day (glow alpha 0.12) and night
(alpha 1.0, emission ≈ 6, dusk world), plus four orthographic elevations.
`diff_ab.py` → `diffs.json`, contact sheet at `renders/contact_sheet.png`.

| View | Mean abs RGB delta | Max pixel delta |
|---|---|---|
| day near | 0.0065% | 24 |
| day far | 0.0066% | 6 |
| night near | 0.0038% | 9 |
| night far | 0.0039% | 5 |
| elevation N | 0.0136% | 153 |
| elevation E | 0.0135% | 29 |
| elevation S | 0.0055% | 33 |
| elevation W | 0.0054% | 81 |

**Looked at, honestly:** the input and optimized rows of the contact sheet are
indistinguishable. The ×8-amplified diff row is black except for single-pixel
hairlines along silhouette and material-boundary edges — antialiasing landing one
sub-pixel differently where joined objects now share a triangle strip. The
largest single-pixel delta (153, on the north elevation) sits on the rear
elevation's window edges, where a dark `Toy_glass` face meets pale `Toy_steel`,
so one pixel flipping side of the boundary is a large RGB step by itself. No
element is missing, no silhouette moved, the pergola is still open, the skylight
asymmetry is intact, and both lit windows and the entrance spill are still
present at night. Nothing here is visible to a player.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (12 in, 12 out); both `_Glow` materials separate; no `Toy_body` in this asset; no manifest-named nodes to preserve |
| **G2** geometry | **PASS** | bbox identical to 5 dp; origin unchanged; signed volumes positive for all 11 objects, `inverted_solids: []`; ray flipped fraction 0.000073 against a 0.0015 gate |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` → `G3-OK`, 12 meshes, 6,900 tris, 12 materials, bbox matches, no decode errors |
| **G4** appearance | **PASS** | all eight views ≤ 0.0136% mean, against gates of 2% far / 4% near |
| **G5** draw submeshes | **PASS** | 67 → 12 |
| **G6** size | **PASS on raw, qualified on gzip** | −51.6% raw; +103.6% gzipped — see below |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object count matches (11); scripts deterministic and committed here; no `.blend1` left |

### G6 — the gzip number, honestly

Raw bytes fell 52%; gzipped bytes **doubled**. Both are real. Meshopt output is
already entropy-coded so it does not gzip further, while the pre-optimize file was
plain glTF buffers that gzip compressed 6:1. **Over the wire the un-optimized file
would have been ~64 KB smaller.** That is a bigger relative swing than 106 South
Park recorded (+49.7%) because this asset's un-optimized buffers were more
compressible still.

Shipping the optimized file anyway, for the three reasons the 165 and 106 South
Park runs recorded:

1. Meshopt compression is the **mandatory intake step** for everything entering
   `app/public/sf-assets/` (`AGENTS.md`; asset pipeline "Ship step"). It is not an
   optional trade.
2. The **structural wins are the real ones**: 67 → 12 draw submeshes and 65 → 11
   nodes both matter to the shared `BatchedMesh` that every generic landmark
   renders out of. 64 KB over the wire does not, on an asset that is 124 KB
   against a 500 KB budget.
3. One encoding across all assets is worth more than the bytes.

The prompt's 60% reduction target was measured on 250–900 KB landmarks where raw
and compressed move together. A sub-200 KB asset does not re-litigate it.

## Shipping swap

`84-south-park.optimized.glb` copied over `artifacts/84-south-park/84-south-park.glb`;
the pre-optimize original is archived at `optimize/input/84-south-park.glb`
(byte-identical copy, verified with `cmp` before any step ran).

The stage-2 contract validator was then re-run against the **shipped, packed**
file — the step that catches dissolve slivers, which are invisible until
gltfpack re-emits stored normals. Result: **overall PASS**, all 16 checks,
`invalid_or_nonunit_loop_normal_count` 0, 11 objects, 6,900 triangles, bbox top
13.200 m. `artifacts/84-south-park/validation.json` and `REPORT.md` now carry the
shipped numbers.
