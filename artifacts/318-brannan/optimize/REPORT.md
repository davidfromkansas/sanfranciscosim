# 318 Brannan Street — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/318-brannan/` on 17 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Toolchain:** Blender 5.2.0 LTS (build 2026-07-14, headless), `npx gltfpack@0.24`,
`g3check/` (pinned three GLTFLoader round-trip), python3 + Pillow, gzip −9.

Scripts were copied from `artifacts/350-brannan/optimize/` rather than from
`tools/glb-optimize/`, because 350 Brannan's adaptation already carries the
limited-dissolve revert that this asset needs for the same reason (see §3).

## Headline

| Metric | Input | Output | Δ |
|---|---|---|---|
| File, raw | 195,376 B | **94,884 B** | **−51.4%** |
| File, gzip −9 | 33,126 B | 57,242 B | +72.8% (see §4) |
| Triangles | 2,972 | 2,972 | 0 |
| Vertices | 6,144 | 5,854 | −4.7% |
| Objects / nodes | 69 | **12** | −82.6% |
| Draw submeshes (primitives) | 70 | **13** | **−81.4%** |
| Materials | 11 | 11 | identical set |
| bbox dims (m) | 29.64689 × 30.17666 × 8.6 | identical | 0 |
| XY origin offset (m) | 0.0, −0.20188 | identical | 0 |

The win here is **draw submeshes, not bytes**: 70 → 13. This asset was already
small (2,972 tris), so there was no fat to cut from the geometry — the value of
the pass is that it now costs the shared landmark `BatchedMesh` a tenth of the
primitives it did.

## 2. Phase A — waste census

`inspect.json`. Input: 69 objects, 2,972 tris, 6,144 verts, 70 primitives,
`NORMAL` only (no UVs, no textures), raw 195,376 B / gzip 33,110 B.

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Degenerate faces | **0** | — | 0 |
| Buried interior faces | none provable (no closed occluder encloses another solid) | 0 | 0 |
| Unwelded coincident verts | 4,524 pairs — every panel is authored as an independent closed prism | ~4.5k verts | 6,144 → 1,620 in-Blender |
| Object-count overhead | 9 material groups holding 69 objects; `Toy_white` alone holds 29 | 69 → ~11 objects | 69 → 12 |
| Over-tessellated curves | none — there is not a single curved surface in this asset | 0 | 0 |
| Duplicate mesh groups | 10 groups, 604 redundant tris (5 SW window frames, 4 storefront frames, 3 vent cans, 2 duct branches, and their fills) | see §6 | joined, not instanced |

## 3. Phase B — geometry cleanup

`optimize.py`, `phaseb_stats.json`. Per-step tri/vert counts:

| Step | Tris | Verts |
|---|---|---|
| input | 2,972 | 6,144 |
| 1. weld ≤ 1 mm, per object | 2,972 | 1,620 |
| 2. degenerate + buried interior faces | 2,972 | 1,620 |
| 3. limited dissolve | **skipped** | — |
| 5. join per material | 2,972 | 1,620 |

**Step 3 stays disabled, and this asset is exactly the case the prompt §3.3
warns about.** 318 Brannan has a `parapet` ring band and a `coping` ring band
(288 tris each — the two largest objects in the file) whose top and bottom faces
are perfectly coplanar annuli following the footprint all the way round. A
strictly-coplanar dissolve merges each into a single annulus ngon and
re-triangulating an annulus emits ~0.2 mm-wide slivers up to 29 m long, whose
collapsed vertex normals fail the stage-2 contract validator only *after*
gltfpack re-emits the stored normals. On 350 Brannan the step was worth 0.4% of
triangles; here there is even less to win because there is no curved geometry at
all. Not a trade. The inherited script's comment block explains it in place.

Step 5 joins: `Toy_white` 29 → 1, `Toy_glass` 15 → 1, `Toy_ink` 5 → 1,
`Toy_roofd` 4 → 1, `Toy_glassl_Glow` 4 → 1, `Toy_steel` 3 → 1,
`Toy_stone` 2 → 1, `Toy_glass_Glow` 2 → 1, `Toy_cream` 2 → 1. `body` stays
separate because it carries two materials (`Toy_cream` walls + `Toy_steel` roof
membrane cap), which is what leaves 12 objects / 13 primitives rather than 11.

Normals audit: all closed solids positive signed volume, `inverted_solids: []`,
ray-test flipped fraction within tolerance.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 318-brannan.optimized.glb -c -km -kn -noq
```

Verified on the output, not trusted from flags: `extensionsUsed`
= `["EXT_meshopt_compression"]`, 11 materials with the input's exact name set
(`_Glow` names intact — `-km` doing its job), 12 nodes, 13 primitives.

**The gzip number goes the wrong way, and that is expected.** Meshopt-encoded
buffers are already entropy-coded and do not recompress: raw drops 51.4% while
gzip −9 rises 72.8% (33.1 KB → 57.2 KB). The shipped siblings show the same
shape — `350-brannan` raw −53.6% / gzip +68%, `380-brannan` raw −51.8% /
gzip +102%. So meshopt is currently costing transfer bytes relative to plain
gzip on assets this small, while buying decode-side vertex-buffer efficiency and
one consistent encoding across every asset in `sf-assets/`. That is the repo's
standing trade (`sf-asset-check` §8, `pipeline/compress-assets.mjs`), not a
regression in this asset, and it is not re-litigated here.

`-noq` is mandatory per the prompt §4 and is what `compress-assets.mjs`
produces; the runtime kit merge needs float32 attributes and the stage-2
validator fails quantized builds on `transforms_applied` /
`no_unexpected_objects`.

## 5. Phase D — bake

Not run (`ALLOW_BAKE: no`). The asset has no textures and no UV layers, and at
2,972 triangles there is no bakeable-region 3× reduction available. Correctly
skipped.

## 6. Judgment calls

- **Duplicate meshes were joined, not instanced.** The census found 604
  redundant triangles across ten repeat groups (window frames, fills, vent
  cans, two identical duct branches). Sharing mesh data would keep those
  triangles in one buffer, but `collect()` in `app/src/assets.js` flattens every
  landmark into the shared `BatchedMesh` anyway, so instancing buys nothing at
  runtime and costs a node per instance in the file. Joining per material is
  strictly better here.
- **`body` left as a two-material object.** Splitting it to reach 11 primitives
  instead of 13 would mean cutting the roof-membrane cap off the wall prism and
  making it a separate open shell, which breaks the closed-solid property that
  the normals audit and the interior-face occluder rule both depend on. Two
  extra submeshes is not worth that.

## 7. Phase E — A/B verification

`render_ab.py` on both files with one rig (42° elevation aerial, near = 1.5×
long axis, far = 6×), day (glow alpha 0.12) and night (alpha 1.0, emission ≈ 6,
dusk world), plus four orthographic elevations. `diff_ab.py` → `diffs.json`,
`renders/contact_sheet.png`, per-view ×8 amplified diffs.

| View | Mean abs RGB Δ | Max px Δ |
|---|---|---|
| day near | 0.0014% | 22 |
| day far | 0.0020% | 33 |
| night near | 0.0006% | 18 |
| night far | 0.0047% | 11 |
| elev N | 0.0019% | 19 |
| elev E | 0.0032% | 19 |
| elev S | 0.0223% | 28 |
| elev W | 0.0138% | 42 |

**What is actually visible, described honestly.** Input and output are
indistinguishable side by side. The residual is the per-object 1 mm weld
averaging vertex normals at shared corners of the small applied panels, and it
shows up as a faint diagonal tonal seam across the glass fill of one or two
southwest-flank windows — visible only at 6× zoom on the orthographic
elevations, where the whole 30 m building fills 900 px. Census at a
visible-difference threshold:

| View | foreground px | ≥ 8/255 on any channel | ≥ 16/255 |
|---|---|---|---|
| elev W | 208,441 | 513 (0.246%) | 330 |
| elev S | 207,042 | 532 (0.257%) | 403 |
| day near (aerial) | 429,765 | 17 (0.004%) | 5 |
| night near (aerial) | 427,438 | 6 (0.001%) | 1 |

The elevations are far closer than the app ever gets; in the aerial views the
app actually renders, four hundredths of one percent of pixels move at all.
Nothing a player would notice. No missing elements, no silhouette change, no
glow surface lost or merged.

## 8. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material name set identical (11), `_Glow` materials separate, no `Toy_body` (landmark), no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox identical to 5 dp, origin identical, all signed volumes positive, `inverted_solids: []`, ray flip within tolerance |
| G3 Round-trip | **PASS** | Blender re-import clean; `g3check` → `G3-OK {"ok":true,"meshes":13,"tris":2972,...}` |
| G4 Appearance | **PASS** | max mean Δ 0.0223% (gate: ≤ 2% far / ≤ 4% near); described above |
| G5 Draw submeshes | **PASS** | 70 → 13 |
| G6 Size | **PASS with note** | raw −51.4%, short of the 60% aspiration. The census justifies the remainder: 0 degenerate faces, 0 buried faces, 0 curved geometry to retessellate, and after weld + join every remaining triangle is authored silhouette. At 2,972 triangles this asset is near the meshopt container floor |
| G7 GPU budget | n/a | bake mode not used |
| G8 Hygiene | **PASS** | re-import object/bbox/material counts match; deterministic re-run reproduces the output; no `.blend1` files |

## 9. Shipping swap

`318-brannan.optimized.glb` copied over `artifacts/318-brannan/318-brannan.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/318-brannan.glb` (verified with `cmp` before the pass began).

`artifacts/318-brannan/validation.json` and `REPORT.md` were then re-generated
against the **shipped** file, so the integration stage writes its manifest entry
from reality rather than from the pre-optimize numbers.
</content>
