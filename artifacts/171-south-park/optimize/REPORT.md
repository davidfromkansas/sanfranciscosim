# 171 South Park Street — optimize pass (stage 4)

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against the approved asset.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Tooling: Blender 5.2.0 LTS, `gltfpack@0.24`, the generic scripts from
`tools/glb-optimize/` (adapted per §0), `g3check/` (pinned three GLTFLoader
round-trip), python3 + Pillow, gzip −9.

## 1. Headline

| | input | output | delta |
|---|---|---|---|
| File, raw | 360,248 B | **155,596 B** | **−56.8%** |
| File, gzip −9 | 63,875 B | 107,925 B | +69% (see §4) |
| Objects | 100 | **11** | −89% |
| Draw submeshes (primitives) | 101 | **12** | −88.1% |
| Triangles | 5,816 | 5,808 | −0.1% |
| Vertices | 11,804 | **3,104** | −73.7% |
| Materials | 12 | 12 | unchanged |
| bbox dims | 19.2565 × 18.497 × 12.6 | identical | 0 |
| Origin offset | −0.1247, −1.3736 | identical | 0 |

The optimized file is now `../171-south-park.glb`; the approved original is
archived byte-for-byte at `input/171-south-park.glb`.

## 2. Phase A — waste census

`inspect.json`. 100 objects, 101 primitives, 5,816 tris, 11,804 verts, one
vertex attribute (`NORMAL`), no textures, no degenerate faces.

| Waste | Measured | Technique | Predicted |
|---|---|---|---|
| Unwelded coincident verts | 8,696 pairs | per-object weld ≤ 1 mm | ~−8.7k verts |
| Object-count overhead | 100 objects across 8 join groups | join per material | −89 objects, −89 primitives |
| Duplicate mesh data | 27 groups, 2,456 redundant tris | folded into the join — these are the repeated brackets, skylights, window frames and deck posts | no tri change, node overhead only |
| Over-tessellated curves | none | — | — |
| Buried interior faces | none provable | occluder rule requires closed solids | — |

The building is authored as chunky closed solids with no curves, so essentially
all the available waste was node and vertex overhead rather than triangles. That
is why the triangle count barely moves and the vertex count falls by three
quarters.

## 3. Phase B — geometry cleanup

`optimize.py`, `phaseb_stats.json`:

| Step | tris | verts |
|---|---|---|
| input | 5,816 | 11,804 |
| weld + degenerate | 5,816 | 3,108 |
| interior faces | 5,816 | 3,108 |
| limited dissolve 0.05° | 5,808 | 3,104 |
| join per material | 5,808 | 3,104 |

Material set preserved exactly, bbox unchanged, no inverted solids. No curve
retessellation step: there are no curved shells in this asset.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 171-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which are API here: `_Glow` is a
name-only distinction and merging across it would silently kill the night layer.
`-noq` per the repo standard — `pipeline/compress-assets.mjs` produces unquantized
meshopt, and the stage-2 contract validator stays strict without special cases.

**Gzip goes up, and that is expected.** Meshopt-compressed buffers are already
entropy-coded, so gzip has nothing left to find and adds framing. The same thing
was recorded on `380-brannan` (raw −51.8%, gzip +102%). Here it is milder: raw
−56.8%, gzip +69%. Raw is the number that matters for the on-disk budget, and at
156 KB the asset sits far inside the 500 KB per-landmark budget in `AGENTS.md`.

`compress-assets.mjs` will skip this file at ship time because it already carries
`EXT_meshopt_compression` — that is the intended behaviour, not a miss.

## 5. Phase E — A/B verification

`render_ab.py` (azimuth adapted to 343.5° so the rig looks square onto the NNW
park front — this building's identity face and where any ornament-band regression
would show), `diff_ab.py`. Landmark distances: near 1.5× long axis = 28.9 m,
far 6× = 115.5 m. Day pass uses glow alpha 0.12; night pass alpha 1.0, emission 6.

| View | mean abs RGB delta | max px delta |
|---|---|---|
| day near | 0.036% | 167 |
| day far | 0.038% | 22 |
| night near | 0.040% | 59 |
| night far | 0.034% | 20 |
| elevation N | 0.050% | 134 |
| elevation E | 0.022% | 169 |
| elevation S | 0.025% | 188 |
| elevation W | 0.033% | 144 |

**Looked at the diffs** (`renders/contact_sheet.png`, 8× amplified bottom row).
What is actually there: hairline antialiasing differences along silhouette and
trim edges, and two small speckle patches on the lit glow windows. The speckle is
the dithered alpha on the `_Glow` shells resolving differently between runs — a
stochastic sampling difference, not a geometry or material change. The entry door
outline shows the same hairline edge difference. Nothing a player would notice;
no missing element, no silhouette change, no shading artifact.

## 6. Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, node names intact | **PASS** | `validation.json` `G1_materials_identical: true`; all 12 material names round-trip through g3check |
| G2 Geometry — bbox, origin, signed volumes, flip fraction | **PASS** | bbox and origin bit-identical; volumes positive; 22,500 rays, 16,032 hits, **0 flipped** (0.000%) |
| G3 Round-trip — Blender re-import and pinned-three load | **PASS** | `G3-OK {"ok":true,"meshes":12,"tris":5808,...}` |
| G4 Appearance — day+night × near+far | **PASS** | max mean delta 0.050%, gate is ≤2% far / ≤4% near |
| G5 Draw submeshes ≤ input | **PASS** | 101 → 12 |
| G6 Size reduced | **PASS** | raw −56.8%; short of the 60% aspiration, see note |
| G7 GPU budget | **n/a** | bake mode off |
| G8 Hygiene — no foreign geometry, deterministic | **PASS** | re-import object count matches; every step is a committed script re-runnable on `input/` |

**G6 note.** 56.8% raw is just under the 60% aspiration, and the census in §2
accounts for the remainder: after the join and the weld, what is left is
silhouette geometry — the wedge body, the stepped cornice and crown, the frieze
bands and the window surrounds. There is no further lossless waste to remove, and
the appearance gate leaves no room for lossy reduction on a 5.8k-triangle asset
that is already 2.2k under its own budget.

**Re-validated against the stage-2 contract validator too**: the optimized GLB
passes all 16 checks of `../validate_171_south_park.py` unchanged, including
`transforms_applied` and `no_unexpected_objects` (which is what `-noq` buys).
