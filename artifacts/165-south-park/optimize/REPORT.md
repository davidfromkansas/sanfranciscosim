# 165–167 South Park — optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executing
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.

`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`

**Result: all gates PASS. The optimized GLB is now the shipping file.**

## Metrics

| | input | shipped | delta |
|---|---|---|---|
| File, raw | 121,884 B (119.0 KB) | **54,760 B (53.5 KB)** | **−55.1%** |
| File, gzip -9 | 30,596 B (29.9 KB) | 39,818 B (38.9 KB) | **+30.1%** — see §Size below |
| Objects | 25 | **8** | −68% |
| Draw submeshes (primitives) | 26 | **9** | −65% |
| Triangles | 2,008 | 2,008 | 0 |
| Vertices | 3,924 | **3,124** (1,048 pre-pack) | −20% shipped / −73% in Blender |
| Materials | 8 | 8 | identical set |
| bbox | 19.0972 × 21.9096 × 9.0 | 19.0972 × 21.9096 × 9.0 | 0 |

The shipped vertex count (3,124) is higher than the post-Phase-B Blender count (1,048)
because the glTF exporter splits vertices at material and normal discontinuities. The
1,048 figure is what the weld achieved; 3,124 is what the file carries.

## Toolchain

- Blender 5.2.0 LTS (`fbe6228777e7`, 2026-07-14), headless
- `npx gltfpack@0.24 -c -km -kn -noq`
- node v22.19.0, npx 10.9.3, pinned three in `g3check/`
- python3 + Pillow, gzip -9

## Phase A — waste census

25 objects carrying 26 primitives against 8 materials. The census found no buried
interior faces worth deleting, no over-tessellated curves (there are no curves — the
asset is all planar prisms and rims), and no degenerate faces. Two kinds of waste:

1. **Object-count overhead — the dominant cost.** 25 nodes and 26 accessor sets for
   2,008 triangles. Four window sills are byte-identical duplicates
   (1.188 × 0.302 × 0.12, 44 tris each), and 10 of the 25 objects share `Toy_trim`.
2. **Unwelded coincident verts from the bevel pass.** 3,924 verts for 2,008 tris is
   roughly 2× the theoretical minimum for closed prisms.

Predicted: join-per-material takes 25 → 8 objects; weld takes ~3,900 → ~1,000 verts;
triangles unchanged, because there is nothing to remove that is not silhouette.
All three predictions held exactly.

## Phase B — geometry cleanup

| step | tris | verts |
|---|---|---|
| input | 2,008 | 3,924 |
| weld ≤ 1 mm + degenerate | 2,008 | **1,048** |
| interior faces | 2,008 | 1,048 |
| limited dissolve 0.05° | 2,008 | 1,048 |
| join per material | 2,008 | 1,048 |

Zero interior faces were removed, and correctly so: the occluder rule only admits
CLOSED solids that fill ≥ 95% of their AABB, and this asset's one big closed solid —
`body` — is a bent wedge filling a fraction of its 19 × 21.9 m box. Nothing else is
large enough to bury anything. The limited dissolve found nothing either, because the
build script emits flat-shaded prisms with no coplanar face pairs to merge.

Join-per-material produced 8 objects. `body` stayed separate from the other
`Toy_steel` geometry because it carries two materials (`Toy_steel` + `Toy_roofd`) and
the join groups by material *set*.

Normals audit after the joins: 8/8 positive signed volumes, no inverted solids.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 165-south-park.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` kept both `_Glow` materials distinct from their non-glow twins — the
material set survives byte-for-byte, which is the one thing that would have silently
killed the night layer. `-noq` per repo standard (float32 attributes for the merge
paths).

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and there is nothing to bake: the facade has no relief
beyond a 0.12 m window recess and four proud bands, all of which are silhouette at the
app's camera distance.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (8/8); `Toy_glass_Glow` and `Toy_trim_Glow` remain separate from `Toy_glass` / `Toy_trim`; no `Toy_body` (landmark) |
| **G2** geometry | **PASS** | bbox identical to 5 dp; origin unmoved (`center_xy` 0,0; `min z` 0); 8/8 signed volumes positive; **0 of 14,801** ray hits flipped (0.0000 vs 0.0015 tolerance) |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` (pinned three GLTFLoader) loads it — 9 meshes, 2,008 tris, 8 materials, no decode errors |
| **G4** appearance | **PASS** | see below |
| **G5** draw submeshes | **PASS** | 26 → 9 |
| **G6** size | **PASS on raw, qualified on gzip** | see below |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object count matches; **re-run is byte-identical** (`mid.glb` sha256 `634b1ad9…`, optimized `a44725c9…` reproduced exactly); no `.blend1` files |

The optimized file was also re-run through the **stage-2 contract validator**
(`validate_165_south_park.py`) after the swap: all 16 checks still PASS, including
`transforms_applied` and `no_unexpected_objects` — confirming `-noq` avoided
gltfpack's dequantize-matrix node splitting.

### G4 — appearance, honestly

Mean absolute RGB delta over foreground pixels, input vs shipped, same rig:

| view | mean Δ | max px Δ |
|---|---|---|
| day near | 0.034% | 22 |
| day far | 0.039% | 15 |
| night near | 0.033% | 26 |
| night far | 0.045% | 26 |
| elevation N (street) | 0.079% | 23 |
| elevation E | 0.021% | 31 |
| elevation S | 0.008% | 20 |
| elevation W | 0.034% | 38 |

Tolerances are ≤ 2% far and ≤ 4% near. Every view is two orders of magnitude inside.

**Looking at the ×8-amplified diffs** (`renders/diff_*.png`, `renders/contact_sheet.png`):
the only structure visible anywhere is speckle inside the two upper-storey window
panels and hairlines along the parapet and cornice edges. Both are Cycles sampling
noise — this rig runs 64 samples with denoising **off**, so the semi-transparent glow
shells over the glazing resolve slightly differently between two renders of the same
geometry. The max-pixel-delta column measures that noise, not a change: it is highest
on `elev_w` (38), a view that contains no glow surfaces at all and differs only in
edge anti-aliasing.

No missing elements. No silhouette change. No shading artifacts. The night glow is
present and unchanged in both `night_near` and `night_far`. Nothing here is anything a
player could notice.

### G6 — size, honestly

**Raw bytes fell 55%, and gzipped bytes rose 30%.** Both are real, and the second one
deserves stating plainly rather than burying: meshopt output is already entropy-coded,
so it does not gzip further, while the pre-optimize file was plain glTF buffers that
gzip compressed 4:1. Over the wire, the un-optimized file would have been ~9 KB smaller
than what ships.

The meshopt build ships anyway, for three reasons that are not about this asset's byte
count:

1. **It is mandatory.** AGENTS.md: every GLB entering `app/public/sf-assets/` is
   meshopt-compressed at intake via `pipeline/compress-assets.mjs`. The loaders
   register `MeshoptDecoder` (`app/src/gltf.js:10`, `app/src/assets.js:406`).
   `compress-assets.mjs` skips files already carrying `EXT_meshopt_compression`, so
   this file passes that ship step untouched.
2. **The structural wins are the real ones here.** 26 → 9 draw submeshes and 3,924 →
   1,048 welded vertices matter to the shared `BatchedMesh` merge; 9 KB over the wire
   does not, on an asset that is 39 KB total against a 500 KB budget.
3. **One encoding across all assets** is worth more than the bytes, exactly as §4 of
   the optimize prompt argues for `-noq`.

This inversion is expected for very small assets and is not a defect. The 4–6× wins
quoted in the optimize prompt were measured on 250–900 KB landmarks, where the
container overhead is negligible against the payload. **Recorded here so the next
sub-100 KB asset does not re-litigate it.**

## Deliverables

```
optimize/
  input/165-south-park.glb        untouched pre-optimize archive (121,884 B)
  165-south-park.optimized.glb    the winner — copied over ../165-south-park.glb
  mid.glb                         post-Phase-B, pre-pack
  inspect.py optimize.py validate.py render_ab.py diff_ab.py   adapted copies
  g3check/                        pinned-three round-trip test
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                        in_*/out_*/diff_* day+night × near+far, 4 elevations, contact sheet
```

Per-asset adaptations to the generic scripts: `render_ab.py` azimuth 45° → **80°**
(compass ~10°), so the A/B views frame the street elevation, the blue gate and the
taper — the generic 45° looks straight down the blind east party flank where nothing is
at risk; `diff_ab.py` contact-sheet title.

## Shipping swap

`165-south-park.optimized.glb` → `artifacts/165-south-park/165-south-park.glb`.
The pre-optimize original is archived at `optimize/input/165-south-park.glb`.
`../REPORT.md` and `../validation.json` carry the shipped numbers.
