# 541 Presidio Boulevard — GLB optimize (shrink) pass

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with `ASSET_CLASS: landmark`,
`ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: all gates PASS. Raw file −54.5% (220,396 → 100,200 B), draw submeshes
−89.6% (77 → 8), geometry byte-identical in appearance.** The optimized build is now
the shipping file at `artifacts/541-presidio/541-presidio.glb`; the pre-optimize
original is archived byte-for-byte at `optimize/input/541-presidio.glb`.

**Toolchain:** Blender 5.2.0 LTS (hash fbe6228777e7), `npx gltfpack@0.24`,
node v22.19.0, three@0.185.1 via `g3check/`, python3 + Pillow 11.3.0, `gzip -9`.

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 220,396 B | **100,200 B** | **−54.5%** |
| File, gzip −9 | 32,615 B | 64,888 B | +99% (see §4) |
| Triangles | 3,404 | 3,404 | unchanged |
| Vertices (re-imported) | 7,044 | 6,259 | −11.1% |
| Vertices (in-scene, pre-export) | 7,044 | 1,852 | −73.7% |
| Objects | 77 | **8** | −89.6% |
| Draw submeshes (primitives) | 77 | **8** | −89.6% |
| Materials | 8 | 8 | unchanged |
| Est. GPU vertex bytes (pos+nrm f32) | 169,056 B | 150,216 B | −11.1% |
| BBox | 22.25916 × 25.09943 × 10.0 | 22.25916 × 25.09943 × 10.0 | 0 (exact) |
| BBox min / origin | −11.12958, −12.54972, 0.0 | identical | 0 (exact) |

Triangles are deliberately unchanged: this asset was authored at 3,404 tris against
an 8,000 cap, so there was no tessellation slack to reclaim. The win here is
**encoding and node overhead**, not geometry.

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Coincident vertex pairs | 5,192 | welded, per-object, ≤ 1 mm |
| Degenerate triangles | 0 | none to remove |
| Objects sharing one material | 77 across 6 materials | joined per material → 8 objects |
| Duplicate mesh groups | 6 groups, 1,756 "redundant" tris | **not removable** — see below |
| Interior buried faces | 0 removed | occluder heuristic does not fire — see below |
| Over-tessellated curves | none | **N/A**: the asset has no curved geometry at all |
| Image textures | 0 | nothing to do |
| Vertex attributes | NORMAL only (no UV, no COLOR) | already minimal |

**The 1,756 "redundant" duplicate-mesh triangles are not recoverable.** The census
flags them because 31 window fills and 33 sills share identical vertex/triangle
counts and dimensions. But this asset is authored in **world space with identity
transforms on every object** (the stage-2 contract requires applied transforms), so
two identically-shaped windows at different positions have genuinely different vertex
data. Sharing mesh data would mean re-introducing per-node translations, which fails
the contract's `transforms_applied` check. Counted and left alone.

**Interior-face removal found nothing, and that is a limitation worth recording.**
`optimize.py`'s occluder rule (correctly conservative) only treats a mesh as an
occluder if it is a closed solid filling ≥ 95% of its axis-aligned bounding box.
Because this building sits **30.68° off the world axes**, nothing qualifies: the main
block fills ≈ 50% of its AABB, the plinth ≈ 54%, and the hip-roof prisms far less.
So genuinely buried faces survive — the main block's top cap under the roof, the
plinth's top cap, the rear bay's shared wall face, both roof base caps, and the
chimney bottoms — on the order of **100–150 triangles (~3–4%)**.

That was left as-is rather than fixed. An oriented-box occluder test using the known
heading would recover it, but the payoff is ~3% of a 3.4k-triangle asset and the
failure mode of a wrong occluder test is *deleting real faces* — the exact bug the
prompt's "hard-learned" occluder rule exists to prevent. Not worth the risk at this
asset size. Any rotated asset in this repo will hit the same ceiling; if it is ever
worth fixing, fix it in `tools/glb-optimize/optimize.py` for everyone, not here.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts (in-scene) | Note |
|---|---|---|---|
| input | 3,404 | 7,044 | 77 objects |
| weld + degenerate | 3,404 | **1,852** | −73.7% verts; the bevel pass had left split vertices everywhere |
| interior faces | 3,404 | 1,852 | 0 removed (§2) |
| limited dissolve 0.05° | 3,404 | 1,852 | 0 removed — post-bevel there are no adjacent strictly-coplanar faces inside one material |
| join per material | 3,404 | 1,852 | **77 → 8 objects** |

Phase B output `mid.glb`: 177,908 B raw (−19.3% from input).
`bbox_ok: true`, `material_set_ok: true`, `inverted_solids: []`.

Curve retessellation (§3 step 4) is skipped as genuinely inapplicable — every volume
in this asset is a box or a hip prism, with no segmented curves to halve.

## 4. Phase C — packing, and the gzip inversion

```
npx gltfpack@0.24 -i mid.glb -o 541-presidio.optimized.glb -c -km -kn -noq
```

`-noq` was used from the start, per the correction recorded in
`artifacts/380-brannan/optimize/REPORT.md` §4 and the mandatory ship step in
`.agents/skills/sf-asset-check/SKILL.md` §8. Verified on the output rather than
trusted from the flags:

- `extensionsRequired: ["EXT_meshopt_compression"]` — **no `KHR_mesh_quantization`**
- 8 nodes, **0 of 8 carry a matrix/translation/rotation/scale** — the same shape as
  the other shipped landmarks, and what keeps `transforms_applied` passing
- 8 meshes / 8 primitives, 0 images
- material name set unchanged, both `_Glow` materials still separate

This command is byte-for-byte the one `pipeline/compress-assets.mjs` runs, so the
**mandatory intake compression is already satisfied by this output**. Do not run
`compress-assets.mjs` over this file again at integration.

**The gzip number goes the wrong way, and that is expected.** Raw drops 54.5% but
`gzip -9` rises from 32,615 to 64,888 B (+99%), because meshopt's encoded buffers are
high-entropy and no longer compress. The identical inversion is on record for
`380-brannan` (raw −51.8%, gzip +102%) and it shipped, so raw bytes are this repo's
metric and the meshopt build is the correct shipping form — it is also what the
runtime decoder is wired for (`setMeshoptDecoder` in both `app/src/gltf.js` and
`app/src/assets.js`).

Worth stating plainly rather than burying: **if the CDN serves this asset gzipped,
the pre-optimize file would have been ~32 KB on the wire against ~65 KB for the
shipped one.** The optimize pass still wins on what actually costs the user — 8 draw
submeshes instead of 77, and 11% less GPU vertex memory — but the "smaller download"
framing is false here at this asset size. At 100 KB raw / 65 KB gzipped the asset is
far inside the 500 KB per-asset budget of `sf-asset-check` §7 either way, so nothing
turns on it for 541 Presidio. It would be worth measuring properly before assuming
the optimize pass reduces transfer bytes for *small* assets in general.

## 5. Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures without a recorded
exception. Nothing here needs it: the asset has no facade micro-detail worth baking
and no texture budget to spend.

## 6. Phase E — A/B verification renders

Same rig on both files, day (glow alpha 0.12, the app's day pass) and night
(alpha 1.0, emission 6, dusk world), near = 1.5 × long axis = 37.6 m,
far = 6 × long axis = 150.6 m, plus four orthographic elevations. Mean absolute RGB
delta over foreground pixels only:

| View | Mean Δ | Max px Δ | Gate |
|---|---|---|---|
| day_near | **0.0116%** | 93 | ≤ 4% |
| day_far | **0.0142%** | 37 | ≤ 2% |
| night_near | **0.0635%** | 215 | ≤ 4% |
| night_far | **0.1104%** | 89 | ≤ 2% |
| elev_n | 0.0196% | 35 | — |
| elev_e | 0.0519% | 35 | — |
| elev_s | 0.0523% | 31 | — |
| elev_w | 0.0181% | 49 | — |

Every view is two orders of magnitude inside its gate.

**Looked at the diffs, not just the numbers.** At ×8 amplification the diff frames
are almost entirely black. What is visible: hairline outlines along the plinth top,
the eave fascia and the porch roof edge — one-pixel rasterisation differences at
seams where two joined objects now share a mesh — plus, in the night frames, faint
rectangles over the three lit windows and a speckle patch on one wall. The speckle is
Cycles sampling noise (`render_ab.py` sets `use_denoising = False`, so the two runs
have independent noise), which is also where the max_px_delta of 215 comes from: a
handful of isolated pixels, not a structure. The glow rectangles are the `_Glow`
shells' alpha blend resolving in a different draw order after the join.

No missing elements, no silhouette change, no shading artifacts. **Nothing a player
would notice.**

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | 8 in / 8 out, both `_Glow` materials distinct; `validation.json` `G1_materials_identical: true` |
| G2 Geometry — bbox, origin, signed volumes, flipped fraction | **PASS** | bbox and origin exact to 1e-5 m; 8/8 signed volumes positive; 22,500 rays, **0 flipped** (0.0000) |
| G3 Round-trip — Blender + pinned three | **PASS** | `G3-OK`, 8 meshes, 3,404 tris, 8 materials, bbox match, no decode errors, only `EXT_meshopt_compression` |
| G4 Appearance — day+night × near+far | **PASS** | max mean Δ 0.1104% against a 2% gate; diffs inspected (§6) |
| G5 Draw submeshes ≤ input | **PASS** | 77 → 8 |
| G6 Size reduced | **PASS with note** | raw −54.5%, short of the 60% aspiration; see below |
| G7 GPU budget | **N/A** | bake mode not used |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object/material/bbox match; re-run reproduces `mid.glb` **and** the final GLB byte-identically (sha256 verified); `.blend1` removed |

**G6 note.** 54.5% raw reduction is under the 60% aspiration, and the census in §2
accounts for the remainder honestly: after welding and joining, what is left is 3,404
triangles of silhouette and facade geometry at float32 — float32 being a deliberate
contract constraint (§4), not slack — plus the ~100–150 buried triangles the rotated
occluder heuristic cannot reach. Choosing the quantized build would have gone further
and broken the runtime merge. At 100 KB the asset is far inside the 500 KB budget.

Also re-ran the asset's own **stage-2 contract validator** against the optimized
file (`contract_on_optimized.json`): `overall: PASS`, **16/16 checks**, same as the
pre-optimize asset. This is the check the quantized build fails.

## 8. The shipping swap

Performed only after all gates passed:

- `541-presidio.optimized.glb` copied over `artifacts/541-presidio/541-presidio.glb`
- pre-optimize original retained at `optimize/input/541-presidio.glb` (sha256
  `3037065239b622f5c9469a707592927efb52018517d2fa3e2bfa09da2304b00f`)
- the parent `validation.json` and `REPORT.md` updated to the **shipped** numbers, so
  the integration stage writes its manifest entry from reality

## 9. Deliverables

```
optimize/
  input/541-presidio.glb           byte-identical archive of the pre-optimize asset
  541-presidio.optimized.glb       the winner (copied over ../541-presidio.glb)
  mid.glb                          Phase B output, pre-packing
  inspect.py optimize.py validate.py render_ab.py diff_ab.py   adapted copies
  g3check/                         pinned-three round-trip test
  inspect.json                     Phase A census
  phaseb_stats.json                per-step tri/vert deltas, re-import verify
  validation.json                  G1/G2/G5 gates + ray test
  contract_on_optimized.json       stage-2 contract validator on the shipped file
  diffs.json                       Phase E pixel deltas
  renders/                         in_/out_/diff_ × day,night × near,far + 4 elevations
                                   + contact_sheet.png
  REPORT.md                        this file
```

Reproduce:

```
B=/Applications/Blender.app/Contents/MacOS/Blender
"$B" -b --python inspect.py  -- input/541-presidio.glb inspect.json
"$B" -b --python optimize.py -- input/541-presidio.glb mid.glb phaseb_stats.json
npx -y gltfpack@0.24 -i mid.glb -o 541-presidio.optimized.glb -c -km -kn -noq
"$B" -b --python validate.py -- input/541-presidio.glb 541-presidio.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../541-presidio.optimized.glb)
"$B" -b --python render_ab.py -- input/541-presidio.glb renders/in
"$B" -b --python render_ab.py -- 541-presidio.optimized.glb renders/out
python3 diff_ab.py
```
