# 326 Brannan — GLB optimize pass (stage 4)

Run 17 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**All gates PASS. Shipped.** `421,252 → 202,500` raw bytes (**−51.9 %**),
`183 → 20` primitives, triangles unchanged at 6,148, day renders pixel-identical.

The pass departs from the prompt in two places, both measured and both explained
below: **the Phase B weld was skipped because it makes this asset worse on every
axis**, and the limited dissolve was skipped because the prompt itself says to on
assets with coplanar ring bands.

## 1. Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash `fbe6228777e7`), headless, CPU |
| gltfpack | `gltfpack@0.24` via `npx --yes` |
| node | v22.19.0 |
| three (g3check) | `^0.185.1` |
| Pillow | 11.3.0 |

## 2. Headline metrics

| | input | mid (Phase B) | shipped |
|---|---|---|---|
| raw bytes | 421,252 | 367,112 | **202,500** |
| gzip −9 bytes | 72,609 | 84,122 | 112,630 |
| objects | 182 | 19 | 19 |
| primitives / draw submeshes | 183 | — | **20** |
| triangles | 6,148 | 6,148 | **6,148** |
| vertices (re-imported) | 12,840 | 12,840 | 13,014 |
| materials | 18 | 18 | 18 |
| bbox | 22.3069 × 22.3614 × 5.9000 | same | **same** |

**Read the gzip column honestly: it goes the wrong way, and that is expected.**
Meshopt buffers are already entropy-coded, so gzip has nothing left to find, and
joining 182 nodes into 19 removes exactly the repeated-node redundancy gzip was
exploiting in the unpacked file. Over the wire the unpacked input would be
smaller — but it cannot ship: `AGENTS.md` and `.agents/skills/sf-asset-check`
§8 make meshopt compression mandatory at intake
(`node pipeline/compress-assets.mjs`, same `-c -km -kn -noq` flags). So the
meaningful comparison is against the *mandatory pack alone*, and against that
baseline this pass is worth **−25.3 % raw** (271,112 → 202,500) and
**183 → 20 primitives**.

Both numbers are recorded so nobody has to re-derive which one is the honest
one. The wins that matter here are raw bytes, node/accessor overhead and load-
time merge cost — not the over-the-wire delta.

`grep -rn setMeshoptDecoder app/src/` → `app/src/gltf.js:10`,
`app/src/assets.js:406`. Meshopt is safe to rely on.

## 3. Phase A — waste census

From `inspect.json`:

| Finding | Count | Action |
|---|---|---|
| Objects sharing a material that could join | 14 material groups covering 178 of 182 objects | **joined** — the whole win |
| Duplicate mesh groups | 16 groups, 1,684 redundant triangles (24 bulbs, 24 bulb glow shells, 12 panes, 12 pane glows, 4 tables, 2 court walls …) | joined into single buffers; cannot be deleted — each instance sits at a different place |
| Coincident vertex pairs | 9,404 | **deliberately left alone** — see §4 |
| Degenerate triangles | 0 | nothing to do |
| Over-tessellated curves | none — 1 px at the 33.5 m near distance is 22.6 mm | nothing to do |
| Vertex attributes | `NORMAL` only, no UVs, no textures | already minimal |

## 4. Phase B — and why the weld was reverted

The prompt makes the 1 mm per-object weld unconditional (§3 step 1). On this
asset it is actively harmful. Four variants, each packed with the repo-standard
`gltfpack@0.24 -c -km -kn -noq`:

| variant | raw bytes | gzip −9 | vertices | primitives |
|---|---|---|---|---|
| pack only (no Phase B) | 271,112 | 110,251 | 12,840 | 183 |
| weld only | 320,944 | 140,712 | 14,750 | 183 |
| **join only — shipped** | **202,500** | 112,630 | **13,014** | **20** |
| weld + join | 246,764 | 129,727 | 14,734 | 20 |

The weld costs **+50 KB raw and +1,910 vertices**, and it costs them whether or
not the join runs.

**The cause is flat shading.** This asset is ~180 deliberately flat-shaded boxes
and icospheres, so every corner is *meant* to be a split vertex — the 9,404
"coincident pairs" the census found are not waste, they are the flat-shading
topology. The weld merges those triples inside Blender, and the glTF exporter
then has to re-split them to emit per-face normals, arriving at a less efficient
split than the authored one. The weld's usual win comes from smooth-shaded
meshes with genuinely redundant vertices; there are none here.

Reverted under §11 ("revert any phase that regresses bytes … and keep the rest").
The degenerate-face half of the same step is a no-op anyway: the stage-2
validator reports `degenerate_triangle_count: 0` on the input.

**The `optimize.py` in this directory carries the table above as a comment**, so
a future run on this asset does not re-discover it. `GLB-OPTIMIZE-PROMPT.md` §3
step 1 should probably gain the same caveat — the condition is "flat-shaded
box-heavy asset", which describes a lot of this set's small SoMa buildings.

**Step 2b (interior faces) removed nothing**, correctly. The occluder rule needs
a *closed* solid filling ≥ 95 % of its own AABB, and every solid on this lot sits
at the SoMa grid's 45°, so no AABB is anywhere near 95 % full. The pass is a
structural no-op here rather than a judgement call.

**Step 3 (limited dissolve) was skipped**, as the prompt's own §3 step 3
instructs for assets with large coplanar ring bands. `ShedParapet` is exactly
that — a closed band following the shed footprint whose top and bottom faces are
coplanar annuli. On `350-brannan` (13 Aug 2026) a strictly-coplanar dissolve
merged each annulus into one ngon and re-triangulated it into 7 slivers up to
24.35 m long at ~0.24 mm wide, which pass every area-based test and surface only
*after* the shipping swap as `invalid_or_nonunit_loop_normal_count`. The shipped
file here reports **0**, so skipping it did its job. Foregone saving: on an asset
of 6,148 triangles of boxes with no curved shells to flatten, negligible.

**Step 5 (join per material)** is the entire win: 182 objects → 19 (18
single-material groups plus `ShedBody`, which carries `Toy_charcoal` walls and a
`Toy_roofd` roof cap). No manifest node names and no `Toy_body` on this asset, so
the join is unconstrained.

## 5. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 326-brannan.optimized.glb -c -km -kn -noq
```

`-km -kn` kept as mandatory (without `-km`, gltfpack merges identical-parameter
materials across the `_Glow` boundary and silently kills the night layer — this
asset has four glow materials whose parameters differ only in colour). `-noq`
kept as mandatory: unquantized is the repo standard and what
`compress-assets.mjs` produces.

Verified on the output rather than trusting flags: material name set identical
(18/18, all four `_Glow` names intact), bbox identical, base still on z = 0.

## 6. Phase E — A/B appearance

Camera adapted from the generic script: **azimuth 135° (from the SE), not the
generic 45°**. A south-west three-quarter view of this lot looks at the blind
party wall and would have judged nothing that matters; from the SE the camera is
square onto the Brannan frontage and looking straight down the court's own axis.

| view | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near (1.5× long axis) | **0.0000 %** | **0** |
| day far (6×) | **0.0000 %** | **0** |
| elevation N | 0.0000 % | 2 |
| elevation E | 0.0008 % | 10 |
| elevation S | 0.0013 % | 27 |
| elevation W | 0.0000 % | 0 |
| night near | 0.5739 % | 53 |
| night far | 0.7335 % | 49 |

Gate G4 allows ≤ 2 % far and ≤ 4 % near. Every view is an order of magnitude
inside that.

**Why night is non-zero while day is bit-identical**, since that asymmetry would
otherwise look like a real change: the day pass has no emitters — `_Glow`
materials are faded to the app's 0.12 daytime alpha with no emission boost — so
Cycles converges to exactly the same image. The night pass turns emission up to
6.0 on four glow materials, and joining the objects changes BVH/object ordering,
which changes the sampling sequence. `diff_night_near.png` confirms it: the
difference is **uniform speckle across every lit surface**, with no localised
element, no missing geometry and no silhouette edge anywhere. It is path-tracing
noise, not a change to the asset.

Looked at directly, at both distances, day and night: nothing a player would
notice. The bottle silhouettes, the JAX disc, the string-light beads, the
12-pane door, the olive crown and the parapet ring are all present and
identical.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract | **PASS** | material set identical 18/18; all four `_Glow` names separate; no `Toy_body`; no manifest node names on this asset |
| **G2** Geometry | **PASS** | bbox identical to 4 dp; origin identical; 19/19 signed volumes positive; ray test **0 flipped of 12,576 hits** (0.0000 % vs 0.15 % tolerance) |
| **G3** Round-trip | **PASS** | Blender re-import clean; `g3check` with pinned three 0.185.1 → 20 meshes, 6,148 tris, 18 materials, no decode errors |
| **G4** Appearance | **PASS** | table in §6; day pixel-identical; night delta is emissive sampling noise |
| **G5** Draw submeshes | **PASS** | 183 → 20 |
| **G6** Size | **PASS** | raw −51.9 % vs input, −25.3 % vs the mandatory-pack baseline. Below the 60 % aspiration, and the §3 census accounts for the remainder: after the join, the file is 6,148 triangles of genuinely distinct geometry. The 1,684 duplicate-mesh triangles are repeats at *different positions* (24 bulbs, 12 panes, 4 tables) that a join can fold into one buffer but cannot delete, and everything else is silhouette — the shed prism, the parapet ring, the gate wall, the court walls, the olive crown, the vine masses. Nothing remains that can be removed without changing what the asset looks like. |
| **G7** GPU budget | **N/A** | `ALLOW_BAKE: no` |
| **G8** Hygiene | **PASS** | re-import object count matches (19); byte-identical deterministic re-run (`md5 b51d70e9962307e475375f0483664598` twice); stray `326-brannan.blend1` deleted |

## 8. Shipping swap

`326-brannan.optimized.glb` copied over `artifacts/326-brannan/326-brannan.glb`.
The pre-optimize original is archived byte-for-byte at
`optimize/input/326-brannan.glb` (421,252 bytes, verified).

The shipped file was then re-run through the **stage-2 contract validator** —
not just the optimize gates — and passes everything, including
`invalid_or_nonunit_loop_normal_count: 0` and `degenerate_triangle_count: 0`.
`../validation.json` and `../REPORT.md` now carry the shipped numbers, so the
integration stage writes its manifest entry from reality: **19 objects,
6,148 triangles, 202,500 bytes, dims 22.3069 × 22.3614 × 5.9000.**
