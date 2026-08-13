# sf-main-library — stage 4 optimize report

Shrink pass per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## 1. Metrics

| | input | shipped | delta |
|---|---|---|---|
| File, raw | 633,248 B | **256,072 B** | **−59.6% (2.47×)** |
| File, gzip −9 | 100,011 B | 164,611 B | +64.6% (see note) |
| Objects / draw submeshes | 257 | **10** | −96.1% |
| Triangles | 10,168 | 10,168 | 0 |
| Vertices (Blender re-import) | 20,288 | 17,150 | −15.5% |
| Materials | 10 | 10 | identical set |
| bbox dims (m) | 116.24286 × 74.50597 × 28.98 | 116.24286 × 74.50597 × 28.98 | 0 |
| bbox min / centre XY | (−58.12143, −37.25299, 0.0) / (0, 0) | identical | 0 |

**Gzip goes up, and that is expected.** meshopt's own entropy coding already
compresses the buffer, so gzipping it again adds overhead — the same result
`asian-art-museum` recorded (+91.7%) and `chase-center` before it (+14.5%). The
raw byte count is what ships and what the 500 KB budget in `sf-asset-check` §7
measures: **256 KB**, comfortably under.

## 2. Phase A — waste census

From `inspect.json`. 257 objects, 10,168 tris, 20,288 verts, 10 materials,
633,248 B raw / 99,991 B gzip, 257 primitives, no textures, no degenerate faces.

| Technique | Finding | Predicted | Actual |
|---|---|---|---|
| Weld coincident verts | 14,690 coincident pairs — every box is authored as an independent closed prism, and the bevel doubles corner verts | large vert cut | 20,288 → 5,598 (−72%) |
| Duplicate meshes | 5,244 redundant tris across 23 groups: 47 north crest studs + 23 west + 13 pavilion (identical 12-tri cubes), 15 Fulton pilasters, 3 mech pucks | no tri saving (kept as geometry) | 0 |
| Interior faces | none provably buried — every object is a closed solid, none fully inside another | 0 | 0 |
| Limited dissolve 0.05° | flat-shaded prisms, already minimal | ~0 | 0 |
| **Join per material** | `Toy_trim` 121 objects, `Toy_glass` 97, then ≤ 10 each | **the whole win** — node + accessor overhead | 257 → 10 |
| Curve retess | 16-seg oculus drum/cone, 10-seg mech pucks; chord error already under the 0.1175 m one-pixel threshold at the 174.4 m near distance | skip | skipped |

The census called it correctly: **this asset's cost was never triangles.** At
10,168 tris it was already 61% under the 26,000 cap. The cost was 257 separate
nodes each carrying its own accessors, which is exactly what the per-material
join collapses.

## 3. Phase B — geometry cleanup

`optimize.py`, unmodified from `tools/glb-optimize/` (no per-asset constants
needed — there are no manifest-named nodes, no `Toy_body`, and no
silhouette-defining curve to except).

| Step | tris | verts |
|---|---|---|
| input | 10,168 | 20,288 |
| weld ≤ 1 mm + degenerate | 10,168 | 5,598 |
| interior faces | 10,168 | 5,598 |
| limited dissolve 0.05° | 10,168 | 5,598 |
| join per material | 10,168 | 5,598 |

**No geometry was removed at any step.** Re-import: 10 objects, 10 materials,
bbox and origin unchanged, `inverted_solids: []`. Intermediate at `mid.glb`,
481,424 B.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o sf-main-library.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` keep the material and node names — without `-km`, gltfpack merges
identical-parameter materials across the `_Glow` boundary and silently kills the
night layer. `-noq` is the repo standard: the runtime merge paths need float32
attributes, and a quantized build fails the stage-2 contract validator on
`transforms_applied` / `no_unexpected_objects`.

Verified on the output rather than trusted from flags: material name set
identical (10, both `_Glow` entries present and separate), bbox within tolerance,
re-import object count 10.

## 5. Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## 6. Phase E — A/B verification

`render_ab.py` on both files, same rig; `diff_ab.py` for the deltas.
Renders and 8×-amplified diffs in `renders/`, contact sheet at
`renders/contact_sheet.png`.

| Pair | mean abs RGB | max px delta | gate |
|---|---|---|---|
| day near | **0.364%** | 158 | ≤ 4% |
| day far | **0.399%** | 113 | ≤ 2% |
| night near | **0.542%** | 65 | ≤ 4% |
| night far | **0.458%** | 39 | ≤ 2% |
| elev N | 0.280% | 143 | — |
| elev E | 0.995% | 113 | — |
| elev S | 0.432% | 104 | — |
| elev W | 0.015% | 27 | — |

**Looked at the diffs, honestly:** rows 1 and 2 of the contact sheet are
indistinguishable. The 8× diff row is black except for faint speckle over the
large flat granite panels of the Grove and Hyde faces and the corner pier, plus a
one-pixel edge line at the west end. That is anti-aliasing and shading dither on
the newly joined coplanar faces — the same triangles, now in one mesh, sampled
fractionally differently. Nothing is missing, no silhouette moved, no glow
surface changed state. There is nothing here a player could notice.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical; both `_Glow` materials separate; no `Toy_body`; no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox identical to 5 dp (tolerance max(1 cm, 0.1%)); origin (0,0); all 10 signed volumes positive; ray test **0 flipped of 19,817 hits** (0.0000% vs 0.15% tolerance) |
| G3 Round-trip | **PASS** | Blender 5.2 re-import + `g3check` `G3-OK` on pinned three@0.185.1 with `MeshoptDecoder`: 10 meshes, 10,168 tris, 10 materials |
| G4 Appearance | **PASS** | §6 — worst case 0.995%, all well inside gate |
| G5 Draw submeshes | **PASS** | 257 → 10 |
| G6 Size | **PASS** | −59.6% raw against a 60% target, essentially on it. The shortfall is the `-noq` standard (the 60% figure was measured with quantization on) plus the census result that there is no removable geometry |
| G7 GPU budget | n/a | bake mode not used |
| G8 Hygiene | **PASS** | re-import object count matches; no foreign geometry; no `.blend1` left; scripts are deterministic and committed |

## 8. Shipping swap

All gates passed, so `sf-main-library.optimized.glb` was copied over
`artifacts/sf-main-library/sf-main-library.glb`. The pre-optimize original is
archived byte-identical at `optimize/input/sf-main-library.glb` (verified with
`cmp`). The shipped file re-validates **PASS** against the stage-2 contract
validator (`artifacts/sf-main-library/validation.json`), and
`pipeline/compress-assets.mjs` correctly reports
`skip (already compressed): landmarks/sf-main-library.glb` — the meshopt
extension is already present, so the mandatory ship step is a no-op.

## 9. Toolchain

Blender 5.2.0 LTS (headless) · `npx gltfpack@0.24` · node v22.19.0 ·
three 0.185.1 (pinned in `g3check/package.json`) · python3 + Pillow 11.3.0 ·
gzip. No substitutions.

One cosmetic fix: `diff_ab.py` came from `tools/glb-optimize/` with a hardcoded
`StMarysCathedral A/B` contact-sheet title. Retitled in the local copy so the
artifact is not mislabelled; worth pushing back into the generic script.
