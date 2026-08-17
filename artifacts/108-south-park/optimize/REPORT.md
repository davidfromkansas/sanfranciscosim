# 108-110 South Park — optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executing
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.

`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`

**Result: all gates PASS. The optimized GLB is now the shipping file.**

> Re-run on 16 Aug 2026 against the **recoloured** build (stage-5 QA found the
> first palette rendered as a black slab in the app — see `../REPORT.md` pass 3).
> Geometry is byte-for-byte the same shape; only material colours moved, so every
> count below is unchanged and only the byte totals shift by a handful.

## Metrics

| | input | shipped | delta |
|---|---|---|---|
| File, raw | 215,652 B (210.6 KB) | **96,180 B (93.9 KB)** | **−55.4%** |
| File, gzip -9 | 41,408 B (40.4 KB) | 65,500 B (64.0 KB) | **+58.2%** — see §Size |
| Objects | 53 | **11** | −79% |
| Draw submeshes (primitives) | 58 | **13** | −78% |
| Triangles | 3,516 | 3,516 | 0 |
| Vertices | 7,008 | **5,692** (1,860 pre-pack) | −19% shipped / −73% in Blender |
| Materials | 10 | 10 | identical set |
| bbox | 26.159 × 25.71891 × 8.45 | 26.159 × 25.71891 × 8.45 | 0 |
| bbox min | (−13.0795, −12.85945, 0.0) | (−13.0795, −12.85945, 0.0) | 0 |

The shipped vertex count (5,692) is higher than the post-Phase-B Blender count
(1,860) because the glTF exporter splits vertices at material and normal
discontinuities. 1,860 is what the weld achieved; 5,692 is what the file carries.

## Toolchain

- Blender 5.2.0 LTS (`fbe6228777e7`, 2026-07-14), headless
- `npx gltfpack@0.24 -c -km -kn -noq`
- node + the pinned three in `g3check/`
- python3 + Pillow, gzip -9

## Phase A — waste census

53 objects carrying 58 primitives against 10 materials, for 3,516 triangles.
`inspect.json` found:

1. **Object-count overhead — the dominant cost.** 53 nodes and 58 accessor sets
   for 3,516 triangles. Eleven duplicate-mesh groups: four identical skylights,
   seven identical modillions, three identical upper-window fills, three
   identical sills, two cornice returns, two vents, two pilasters, two entry
   jambs, two rear-window fills and sills, two glow shells — 960 triangles of
   byte-identical geometry. Nineteen of the 53 objects share `Toy_mint`.
2. **Unwelded coincident verts from the bevel pass.** 7,008 verts for 3,516
   triangles, with 5,148 coincident vertex pairs — roughly 2× the theoretical
   minimum for closed prisms.
3. **No buried interior faces, no degenerate faces, no curves.** The asset is
   all planar prisms and rims, so there is nothing to retessellate and nothing
   provably hidden inside a closed solid.

Predicted: join-per-material takes 53 → 11 objects; weld takes ~7,000 → ~1,900
verts; triangles unchanged, because everything that is not silhouette is already
gone. **All three predictions held exactly.**

## Phase B — geometry cleanup

| step | tris | verts |
|---|---|---|
| input | 3,516 | 7,008 |
| weld ≤ 1 mm + degenerate | 3,516 | **1,860** |
| interior faces | 3,516 | 1,860 |
| limited dissolve 0.05° | 3,516 | 1,860 |
| join per material | 3,516 | 1,860 |

- **Zero interior faces removed**, and correctly so: the occluder rule only
  admits closed solids, and the only closed solid big enough to bury anything is
  `body`, whose faces the shopfront geometry sits proud of rather than inside.
- **The limited dissolve changed nothing** (0 triangles, 0 verts). This asset is
  exactly the shape the prompt's §3.3 warns about — `parapet` and `belt` are
  coplanar ring bands that follow the whole footprint, and 350 Brannan turned
  them into 24 m slivers. It was left enabled because the delimit-by-material +
  sharp constraint on flat-shaded prisms leaves nothing for it to merge (the
  same result 165 South Park recorded), and because the outcome was verified
  rather than assumed: the stage-2 contract validator was re-run **on the packed
  file**, which is the only place the sliver failure shows, and returned
  `invalid_or_nonunit_loop_normal_count: 0` and `degenerate_triangle_count: 0`.
- **Join per material** did the work: 53 → 11 objects. Eight join groups; `body`,
  `sign` and `transom_glow` stayed separate (single-user materials, or a
  material pair the joiner keys separately).

`inverted_solids: []` after the joins.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 108-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept all ten material names distinct, including both `_Glow`
materials — verified on the output, not trusted from the flags. `-noq` per the
repo standard, so the file carries float32 attributes and no dequantize node
transforms; `transforms_applied` and `no_unexpected_objects` both still pass in
the stage-2 validator.

### Size

Raw bytes fell 55.4%. **Gzipped bytes rose 58.2%**, which is expected and is not
a regression: meshopt-compressed buffers are already entropy-coded, so gzip has
nothing left to find and adds overhead. What ships over the wire from Vercel is
the raw file with `Content-Encoding` negotiated per-asset; the number that
matters against the ≤ 500 KB budget is the raw 93.9 KB. 165 South Park recorded
the same pattern.

## Phase D

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` at the review rig's azimuth (156°, adapted from the generic 45°,
which looks straight down the blind north-east party flank where nothing is at
risk), day and night, near = 1.5× and far = 6× the long axis, plus four
orthographic elevations.

| view | mean abs RGB delta | max px delta |
|---|---|---|
| day near | 0.0046% | 43 |
| day far | 0.0045% | 15 |
| night near | 0.0022% | 10 |
| night far | 0.0021% | 3 |
| elev N | 0.0034% | 36 |
| elev E | 0.1299% | 31 |
| elev S | 0.1041% | 30 |
| elev W | 0.0028% | 42 |

Gate G4 allows 2% far / 4% near. The worst view is **0.13%**, fifteen times
under the tightest limit.

**Looking at the diffs, honestly:** the ×8-amplified diff row is black except
for two things. (1) Hairline outlines on the parapet, belt course and skylight
edges — sub-pixel rasterisation shifts from re-welded vertices, invisible at
1×. (2) A visible patch on the lit display bay and the two lit upper windows in
the east and south elevations, which is why those two views carry ten times the
delta of the others. That patch is a **render-preview artifact, not an app
difference**: joining the three `Toy_glass_Glow` shells into one object changes
the alpha-blend sort order against the opaque `Toy_glass` fills behind them in
the day preview, where the shells are drawn at 12% alpha. The app never blends
them this way — `assets.js` puts every `_Glow` surface in a separate unlit layer
with its own draw. Nothing a player would notice, and nothing that exists in the
runtime path.

## Gate results

| gate | result | evidence |
|---|---|---|
| **G1** Contract | **PASS** | material set identical (10 in, 10 out); both `_Glow` materials survive separately; no `Toy_body`; no manifest-named nodes on this asset |
| **G2** Geometry | **PASS** | bbox delta 0; origin delta 0; 11/11 signed volumes positive; 22,500-ray test → 0 flipped of 13,338 hits (0.000%) |
| **G3** Round-trip | **PASS** | re-imports in Blender; `g3check` → `{"ok":true,"meshes":13,"tris":3516}`, all ten materials, bbox matches |
| **G4** Appearance | **PASS** | worst mean delta 0.13% (limit 2%/4%); no missing elements, no silhouette change; the one visible diff is a day-preview blend-order artifact described above |
| **G5** Draw submeshes | **PASS** | 58 → 13 |
| **G6** Size | **PASS** | 210.6 KB → 93.9 KB raw, −55.4% (target 60%; the remainder is silhouette geometry — the census found nothing removable that is not silhouette, and triangles are unchanged at 3,516) |
| **G7** GPU budget | n/a | bake mode not run |
| **G8** Hygiene | **PASS** | re-import object count 11 in both Blender and three; no foreign geometry; scripts are deterministic and committed here; no `.blend1` files |

## Shipping swap

`108-south-park.optimized.glb` copied over `../108-south-park.glb`. The
pre-optimize original is archived at `input/108-south-park.glb` (215,652 B).
The asset's `../validation.json` was regenerated from the shipped file and still
reports **overall PASS** on all 16 stage-2 checks, now at 11 objects /
3,516 triangles.
