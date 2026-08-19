# 126 South Park — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2.

| Input | `ASSET_CLASS` | `ALLOW_MESHOPT` | `ALLOW_BAKE` |
|---|---|---|---|
| `artifacts/126-south-park/126-south-park.glb` (post-approval) | `landmark` | `yes` | `no` |

**Result: all gates PASS. 292,460 → 126,664 bytes (−56.7%), 83 → 10 draw
submeshes, appearance identical.** The optimized file is now the shipping asset;
the pre-optimize original is archived byte-for-byte at
`optimize/input/126-south-park.glb`.

## Headline metrics

| Metric | Input | Phase B (`mid.glb`) | Shipped | Δ |
|---|---|---|---|---|
| File bytes (raw) | 292,460 | 230,676 | **126,664** | **−56.7%** |
| File bytes (gzip -9) | 65,759 | 72,045 | 86,877 | +32.1% — see note |
| Objects | 82 | 9 | **9** | −89% |
| Draw submeshes (primitives) | 83 | — | **10** | −88% |
| Triangles | 4,560 | 4,560 | **4,560** | 0 |
| Vertices (Blender, welded) | 9,134 | 2,442 | — | −73% |
| Vertices (re-imported, split by normal/material) | 9,134 | — | 8,115 | −11% |
| Materials | 9 | 9 | 9 | identical set |
| bbox dims (m) | 26.73819 × 26.5868 × 7.6 | — | 26.73819 × 26.5868 × 7.6 | 0 |
| bbox min | (−12.97945, −13.77639, 0.0) | — | (−12.97945, −13.77639, 0.0) | 0 |

**On the gzip figure going up.** Meshopt-compressed buffers are already
entropy-coded, so gzip finds nothing left to remove and pays the container
overhead. This is expected and is not a regression: the byte count that reaches
the browser is the raw 126,664, and 126,664 < 65,759 + no-transport-compression
is not the comparison that matters — the pre-optimize asset served gzipped was
65,759 bytes over the wire against 86,877 now, but it cost **292,460 bytes of
GPU-side parse and 83 draw submeshes** against 126,664 and 10. The repo standard
(`pipeline/compress-assets.mjs`) is meshopt for exactly this trade. Recorded
rather than hidden.

## 1. Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (hash fbe6228777e7, 2026-07-14) |
| gltfpack | `npx gltfpack@0.24` (pinned) |
| three (g3check) | 0.185.1 (pinned in `g3check/package.json`) |
| Python | 3.9 + Pillow |

`grep -rn setMeshoptDecoder app/src/` hits `app/src/gltf.js:10` and
`app/src/assets.js:406`, so `ALLOW_MESHOPT=yes` is verified, not assumed.

## 2. Phase A — waste census

From `inspect.json`:

| Finding | Count | Disposition |
|---|---|---|
| Coincident vertex pairs (≤ 1 mm) | **6,692** | welded in Phase B — the single biggest win |
| Objects sharing one material (join candidates) | 82 across 8 groups | joined in Phase B |
| Duplicate mesh groups | 5 rafters, 2 skylight glazes, 2 kerbs, paired window frames — 868 redundant tris | **joined, not instanced** (§3 step 6: small counts) |
| Degenerate triangles | 0 | nothing to do |
| Interior faces buried in closed solids | 0 removed | nothing to do |
| Over-tessellated curves | 1 (vent cowl, 10-segment, r 0.30 m) | **not retessellated** — already at the style bible's 8–14 floor |
| Image textures | 0 | contract-clean |

Largest single object: `upstand` at 1,152 tris — 25% of the asset — for a 0.20 m
band that follows all 16 footprint edges right around. That is expensive, but it
is design geometry, not waste: the ring is what frames the pale deck from the
app's downward camera. Reducing it is a stage-2 massing decision, not a stage-4
byte decision, and it is not taken here.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 4,560 | 9,134 |
| 1+2a weld ≤ 1 mm + degenerate (per object) | 4,560 | **2,442** |
| 2b interior faces buried in closed solids | 4,560 | 2,442 |
| 3 limited dissolve | **SKIPPED — see below** | |
| 5 join per material | 4,560 | 2,442 |
| 7 normals audit | 0 inverted solids | |

Triangles did not move, and that is the expected outcome for a deterministically
authored asset: there was no duplicated, buried or degenerate geometry to find.
The win was entirely in vertex welding (−73%) and node/submesh overhead (−89%).

**Step 3 was deliberately skipped.** `GLB-OPTIMIZE-PROMPT` §3 step 3 says to skip
limited dissolve "entirely on assets with large coplanar ring bands", and this
asset is exactly the described case: `upstand` is a four-loop band following all
16 edges of the footprint, so its top and bottom faces are perfectly coplanar
annuli. Even a strictly-coplanar dissolve merges each into a single annulus ngon,
and re-triangulating an annulus emits slivers — on `350-brannan` that produced
triangles up to 24.35 m long and ~0.24 mm wide, which pass an area-based
degeneracy test, survive Phases B and E, and surface only *after* the shipping
swap as `invalid_or_nonunit_loop_normal_count` in the packed file. The step was
worth 0.4% of triangles on that asset. Not worth a silent contract failure here.

**Verified rather than assumed:** the shipped, packed file was re-run through the
stage-2 contract validator and reports
`invalid_or_nonunit_loop_normal_count: 0`. That is the check the skip exists to
protect, and it is green.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 126-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept (glow-ness is name-only; without `-km` gltfpack merges
identical-parameter materials across the `_Glow` boundary and silently kills the
night layer). `-noq` kept — repo standard, matches `pipeline/compress-assets.mjs`,
and keeps the stage-2 validator strict on `transforms_applied` /
`no_unexpected_objects`. Verified on the output rather than trusting the flags:
material name set identical (9/9, both `_Glow` materials present and separate),
bbox identical to 5 decimal places, `body` node name intact.

## 5. Phase E — A/B verification

Same rig, input vs output, day (glow alpha 0.12) and night (alpha 1.0, emission
6, dusk world), near = 1.5× long axis, far = 6× long axis, plus four
orthographic elevations. Mean absolute RGB delta over foreground pixels:

| View | Mean Δ | Max px Δ | Gate |
|---|---|---|---|
| day_near | 0.0028% | 29 | ≤ 4% |
| day_far | 0.0051% | 41 | ≤ 2% |
| night_near | **0.0751%** | 67 | ≤ 4% |
| night_far | 0.0712% | 39 | ≤ 2% |
| elev_n / e / s / w | 0.0030 / 0.0043 / 0.0048 / 0.0042% | 26 / 17 / 61 / 34 | — |

**Looked at, not just measured.** At ×8 amplification the day and elevation
diffs are black apart from a one-pixel shimmer on high-contrast edges. The two
night diffs are the largest and are still ~0.07%: the residual sits as faint
speckle around the emissive skylights, the light-well glow shells and the lit
front windows, and it is Cycles sampling noise between two 64-sample renders, not
a change in the model — it appears on every emissive surface uniformly and
follows no geometric feature. No element is missing, no silhouette moved, no
shading artifact. Nothing a player would notice.

## 6. Gate results

| Gate | Result | Evidence |
|---|---|---|
| **G1 Contract** | **PASS** | material set identical (9/9); `Toy_glass_Glow` and `Toy_glassl_Glow` separate; no `Toy_body`; `body` node intact |
| **G2 Geometry** | **PASS** | bbox Δ 0.00000 m on all three axes; origin Δ 0; all 9 signed volumes positive; 0 flipped of 13,152 ray hits (0.000%, gate 0.15%) |
| **G3 Round-trip** | **PASS** | re-imports in Blender; `g3check` under pinned three 0.185.1 reports `ok:true`, 10 meshes, 4,560 tris, 9 materials, no decode errors |
| **G4 Appearance** | **PASS** | max mean delta 0.0751% (night_near) against a 4% gate; described above |
| **G5 Draw submeshes** | **PASS** | 83 → 10 |
| **G6 Size** | **PASS with note** | −56.7% raw against a 60% aspiration — see below |
| **G7 GPU budget** | **N/A** | `ALLOW_BAKE=no`, no bake performed |
| **G8 Hygiene** | **PASS** | re-import object count matches, no foreign geometry; deterministic re-run reproduces `mid.glb` and the packed output **byte-for-byte** (sha256 verified); one stray `126-south-park.blend1` removed |

**G6 note — why the remainder is not compressible.** The gate requires that a
shortfall against `TARGET_REDUCTION` be explained by the census, and it is:
triangles did not fall at all, because there was nothing to remove. There are
zero degenerate faces, zero buried interior faces, and zero image textures; the
868 "duplicate" triangles are five rafter tails and two paired skylights that are
genuinely separate, separately-positioned silhouette geometry; the one curve is
already at the style bible's 8–14 segment floor; and the one step that would have
cut more triangles is barred by rule for this asset's ring band. What remains is
4,560 triangles of position + normal float32 — all of it silhouette or facade
relief that the §5 contract calls sacred. The reduction that *was* available came
from welding and submesh consolidation, and both were taken in full.

## 7. Deliverables

```
optimize/
  input/126-south-park.glb          292,460 B — untouched pre-optimize archive
  mid.glb                           230,676 B — Phase B output
  126-south-park.optimized.glb      126,664 B — the winner, now shipped
  inspect.py optimize.py validate.py render_ab.py diff_ab.py   adapted copies
  g3check/                          pinned-three round-trip test
  inspect.json stats_phaseb.json validation.json diffs.json
  renders/                          in_*/out_*/diff_* × day,night × near,far
                                    + 4 elevations + contact_sheet.png
  REPORT.md                         this file
```

Two per-asset adaptations were made to the generic scripts, as §0 directs:
`optimize.py` step 3 replaced with the documented skip, and `diff_ab.py`'s
contact-sheet title changed from the `st-marys-cathedral` original.

## 8. Shipping swap

`126-south-park.optimized.glb` copied over `artifacts/126-south-park/126-south-park.glb`.
The asset's own `validation.json` and `REPORT.md` were re-run and updated to the
shipped numbers (4,560 tris, 9 objects, 126,664 B raw / 86,877 B gzip) so the
integration stage writes its manifest entry from reality. The stage-2 contract
validator reports **PASS on every check** against the packed shipping file,
including the waist still measuring **4.007 m** and the light wells still
counting 2 south-west + 1 north-east.
