# 345 Spear Street (Hills Plaza) — GLB optimize report (stage 4)

Run 19 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Toolchain:** Blender 5.2.0 LTS (headless), `npx gltfpack@0.24`, node + pinned
three in `g3check/package.json`, python3 + Pillow, gzip −9. Scripts adapted from
`tools/glb-optimize/`; per-asset changes documented in §3.

## 1. Metrics

| | input | output | delta |
|---|---|---|---|
| File, raw | 1,058,188 B | **489,380 B** | **−53.8%** |
| File, gzip −9 | 173,610 B | 303,978 B | see §4 (meshopt is pre-entropy-coded) |
| Triangles | 17,428 | 17,054 | −374 (buried interior faces) |
| Vertices (post-weld) | 34,774 | 9,128 | −73.7% |
| Objects / nodes | 233 | **16** | −93.1% |
| Draw submeshes | 233 | **17** | −92.7% |
| Materials | 15 | 15 | identical set, `_Glow` intact |
| bbox dims | 106.3305 × 118.9857 × 68.5 | identical | 0 |

489.4 KB sits inside the 500 KB landmark budget with ~11 KB of headroom —
tight, like 501-second. The lever if this is ever revised is the arcade arch
count and the tower spandrel rings.

## 2. Waste census (Phase A)

233 small closed solids authored without booleans: the waste is corner-by-corner
authored vertices (34.8k verts for 17.4k tris), node/accessor overhead, and 374
provably-buried faces (pavilion body inside the frontage bar, tower base inside
the podium, band backs inside the tower core). No degenerate faces; arches are
10-segment and within chord error at the near distance; no over-tessellation.

## 3. The variant table, and two hard-learned adaptations

Four variants measured (raw / gzip bytes):

| variant | raw | gzip |
|---|---|---|
| input (uncompressed) | 1,058,188 | 173,610 |
| pack-only | 568,736 | 214,464 |
| **weld + interior + join, no dissolve (SHIPPED)** | **489,380** | **303,978** |
| full Phase B incl. 0.05° dissolve | 465,828 | 317,084 |

**Dissolve rejected**: it removed ZERO triangles (17,054 both ways), won 23.5 KB
raw purely through index reordering, lost 13 KB gzip, and is the only Phase B
step able to manufacture degenerate geometry (the 350-brannan sliver class).
Nothing bought, risk declined.

**Adaptation 1 — `_Glow` objects are exempt from interior-face deletion.** The
first run deleted the "buried" backs and sides of the six lit-window plates
(they intentionally hug the tower shaft), turning closed boxes into 25 open
quads whose joined signed volume went negative — caught by the stage-2
validator re-run on the packed file (`normals_outward_signed_volume` FAIL),
invisible to the ray test (0 flipped visible faces). Glow shells are now never
occluder targets.

**Adaptation 2 — source fix upstream (stage 2):** the same first run revealed
four lit-window plates z-overlapping the tower's spandrel-band solids (one was
entirely inside a band — both a bury-bug and a visual bug). The build script now
centres every lit plate in a glass strip between bands; the source GLB was
rebuilt and re-validated (PASS) before this stage re-ran. Recorded in the asset
REPORT.md.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 345-spear.optimized.glb -c -km -kn -noq
```

All 15 material names survive (g3check). gzip rises because meshopt streams are
already entropy-coded; raw is the on-disk number that matters (same behaviour
as every meshopt landmark in the repo).

## 5. Phase E — A/B appearance (gates G4)

Same rig both files: 42° aerial, near 178 m / far 714 m, day (glow α 0.12) and
night (α 1.0, emission color = base color per the README night rule), plus four
orthographic elevations.

| view | mean abs RGB | max px |
|---|---|---|
| day near | 0.0096% | 28 |
| day far | 0.0102% | 7 |
| night near | 0.3590% | 82 |
| night far | 0.3792% | 83 |
| elev N/E/S/W | 0.0139 / 0.0092 / 0.0096 / 0.0046% | ≤ 72 |

Night split-view inspected by eye: crown band, arcade glow and lit windows all
continuous across the A|B seam; the night deltas are firefly noise around the
emissive shells, not structure. Nothing a player would notice.

## 6. Gates

| gate | result |
|---|---|
| G1 contract (materials, glow, nodes) | PASS |
| G2 geometry (bbox 0 delta, origin 0, volumes positive, flipped 0.0) | PASS |
| G3 round-trip (Blender + g3check pinned three, 17 meshes) | PASS |
| G4 appearance (≤ 2% far / 4% near; worst 0.38%) | PASS |
| G5 submeshes (233 → 17) | PASS |
| G6 size (−53.8%) | PASS |
| G7 GPU (bake off) | n/a |
| G8 hygiene (deterministic, no .blend1, foreign-geometry count clean) | PASS |

Stage-2 contract validator re-run against the SHIPPED packed file:
`overall: PASS`, `invalid_or_nonunit_loop_normal_count: 0`.

## 7. Shipping swap

`345-spear.optimized.glb` → `artifacts/345-spear/345-spear.glb`; pre-optimize
original archived at `optimize/input/345-spear.glb`. Asset REPORT.md /
validation.json updated to shipped numbers (tris 17,054, 489,380 B).
