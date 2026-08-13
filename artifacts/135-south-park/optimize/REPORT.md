# 135 South Park — GLB optimize pass (stage 4)

Run per [`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`](../../../docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md).
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Tools: Blender 5.2.0 LTS, gltfpack 0.24, `g3check/` (pinned three GLTFLoader),
python3 + Pillow, gzip −9.

## 1. Result

| Metric | Input | Output | Δ |
|---|---|---|---|
| File, raw | 247,772 B | **108,524 B** | **−56.2%** |
| File, gzip −9 | 57,848 B | 79,722 B | +37.8% (see §4) |
| Triangles | 4,016 | **3,836** | −4.5% |
| Vertices | 7,810 | **2,044** | **−73.8%** |
| Objects / nodes | 65 | **10** | −84.6% |
| Draw submeshes (primitives) | 66 | **11** | **−83.3%** |
| Materials | 9 | 9 | unchanged |
| bbox dims | 34.4526 × 25.9498 × 8.5 | identical | 0 |

The optimized file is now `artifacts/135-south-park/135-south-park.glb`; the original is
archived byte-for-byte at `optimize/input/135-south-park.glb`.

## 2. Phase A — waste census

From `stats_input.json`:

- **5,676 coincident vertex pairs** — the dominant waste. Every window is a
  frame + fill + (sometimes) glow shell built as separate closed prisms, so
  shared corners were duplicated many times over.
- **65 objects sharing 9 materials** — `Toy_trim` alone had 26 users, `Toy_glass` 20.
  Node and accessor overhead, and 66 draw submeshes for a 4,016-triangle building.
- **720 triangles in duplicate mesh groups** — the five identical front window frames,
  the four wing frames, and the monitor kerb/lid pair. Genuinely distinct objects at
  distinct positions, so they were joined rather than instanced (§3 step 6: join small
  counts).
- 0 degenerate triangles, 0 interior faces buried inside another closed solid.
- Over-tessellation: the only curve is the 10-segment `vent_cowl`, r = 0.4 m. At the
  landmark near distance its chord error is well under one pixel, but halving it to 5
  segments would make a 0.8 m cylinder visibly polygonal for a saving of ~20 triangles.
  **Skipped, deliberately** — recorded here per §3 step 4.

Predicted before executing: weld and per-material join together account for essentially
all of the win; triangle count barely moves. That is what happened.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 4,016 | 7,810 |
| weld ≤ 1 mm (per object) | 4,016 | 2,134 |
| degenerate + buried interior faces | 4,016 | 2,134 |
| limited dissolve 0.05° | 3,836 | 2,044 |
| join per material | 3,836 | 2,044 |

The weld is per-object by design: glow shells are separate objects, so a per-object weld
can never fuse a `_Glow` surface onto the opaque geometry behind it. 0 interior faces were
removed — every solid here is a genuinely separate box, and the occluder rule only permits
deleting faces provably buried inside a *closed* solid.

Normals audit after joining: all signed volumes positive, `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 135-south-park.glb -c -km -kn -noq
```

Verified on the output rather than trusted from the flags:

- `extensionsUsed` / `extensionsRequired` = `["EXT_meshopt_compression"]` **only**.
  No `KHR_mesh_quantization`.
- All accessors are `5126 / VEC3` (float32) for position and normal.
- No node carries a `matrix`/`translation`/`rotation`/`scale` — the dequantize-matrix and
  `Mesh_N` child-node split that quantization introduces is absent.
- All 9 material names present and distinct, `_Glow` pair intact.

**On the gzip increase.** Raw bytes fall 56.2% but gzip −9 rises 37.8%, because meshopt
data is already entropy-coded and does not gzip further. This is the documented,
expected consequence of the mandatory `-noq`, not a regression:
`380-brannan` measured −51.8% raw / **+102%** gzip on the same recipe and shipped the
`-noq` build anyway. This asset is better than that precedent on both axes. `-noq` is the
repo standard because it is what `pipeline/compress-assets.mjs` produces, the runtime
merge paths need float32 attributes, and one encoding across all assets is worth more than
the bytes.

`ALLOW_BAKE` was `no` and Phase D did not run — correct for an asset with no textures and
a contract that forbids them.

## 5. Phase E — A/B verification

`render_ab.py` on both files through one rig; `diff_ab.py` for the deltas. Landmark camera
distances: near 1.5× long axis, far 6×.

| View | Mean abs RGB Δ | Max px Δ | Gate |
|---|---|---|---|
| day near | 0.109% | 25 | ≤ 4% |
| day far | 0.084% | 8 | ≤ 2% |
| night near | 0.342% | 72 | ≤ 4% |
| night far | 0.359% | 54 | ≤ 2% |
| elevation N | 0.063% | 110 | — |
| elevation E | 0.094% | 25 | — |
| elevation S | 0.051% | 34 | — |
| elevation W | 0.053% | 31 | — |

**Looked at the diffs, not just the numbers.** At ×8 amplification the diff row of
`renders/contact_sheet.png` is black apart from hairline tracing on silhouette edges and
one or two thin vertical lines at wall junctions. That is antialiasing moving by a
fraction of a pixel where the limited dissolve merged coplanar faces and changed the
triangulation underneath an unchanged surface. No element is missing, no silhouette moved,
no shading artifact appeared, and the night state — the four lit front bays and the
monitor's glowing clerestory — is identical in both rows.

The night deltas are the largest of the eight, which is expected: the night frames are
mostly near-black, so identical absolute differences are a larger fraction of a small
mean. At 0.36% they are an order of magnitude inside the gate.

Nothing here is anything a player would notice.

## 6. Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** Contract: material set identical, `_Glow` separate, node names intact | **PASS** | 9 in, 9 out, same names; `G1_materials_identical: true` |
| **G2** Geometry: bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox identical to 4 dp; 0 flipped of 22,500 rays (0.00%) |
| **G3** Round-trip: Blender + pinned-three GLTFLoader | **PASS** | `G3-OK` — 11 meshes, 3,836 tris, 9 materials, no decode errors |
| **G4** Appearance: day+night × near+far | **PASS** | max 0.359% vs 2% far / 4% near gates; diffs inspected, §5 |
| **G5** Draw submeshes ≤ input | **PASS** | 66 → 11 |
| **G6** Size reduced | **PASS with note** | raw −56.2%, short of the 60% aspiration — see below |
| **G7** GPU budget | **n/a** | bake mode off |
| **G8** Hygiene: no foreign geometry, deterministic | **PASS** | re-import object count 10 = expected; all steps are committed scripts |

**G6 note.** 56.2% raw is under the 60% aspiration, and the census explains the remainder
honestly: after welding and joining, what is left is 3,836 triangles of actual silhouette
and facade relief — the L body, the parapet and coping rings (720 triangles each before
dissolve, and they *are* the roof's read), the window frames, and the monitor. There is no
further lossless win available that does not remove geometry a viewer can see. At 108 KB
the asset sits far inside the 500 KB per-asset budget in `sf-asset-check` §7.

## 7. Post-swap re-validation

The optimized file was re-run through the **stage-2 contract validator**
(`validate_135_south_park.py`), not just the optimize-side gates:

```
overall PASS — 16/16 checks
tris 3836   objects 10   dims [34.4526, 25.9498, 8.5]   min_z 0.0
materials: Toy_glass, Toy_glass_Glow, Toy_glassl, Toy_glassl_Glow,
           Toy_ink, Toy_roofd, Toy_rust, Toy_steel, Toy_trim
```

Crest still lands on 8.500 m exactly, so the loader's `targetHeightM / measuredHeight`
scale is still 1.0. `validation.json` in the parent directory now describes the **shipped**
file.

## 8. Files

| File | What it is |
|---|---|
| `input/135-south-park.glb` | the pre-optimize asset, byte-for-byte |
| `mid.glb` | after Phase B, before packing |
| `135-south-park.glb` | the packed output (copied up as the shipping file) |
| `inspect.py` / `stats_input.json` | Phase A census |
| `optimize.py` / `stats_mid.json` | Phase B |
| `validate.py` / `validation.json` | gates G1, G2, G5 |
| `g3check/` | gate G3 |
| `render_ab.py` / `diff_ab.py` / `renders/` / `diffs.json` | gate G4 |

`diff_ab.py`'s contact-sheet label was hardcoded to "St Marys Cathedral" in the generic
tool it was copied from; corrected to this asset before the sheet was committed.
