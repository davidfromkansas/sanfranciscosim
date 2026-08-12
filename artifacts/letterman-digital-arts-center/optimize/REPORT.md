# Letterman Digital Arts Center — optimize report (stage 4)

`GLB-OPTIMIZE-PROMPT.md` run against the approved asset.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Result: all gates PASS. 1,032,424 → 166,464 bytes (6.2×, −83.9%).** The
optimized file is now the shipping `letterman-digital-arts-center.glb`; the
approved original is archived byte-for-byte at
`optimize/input/letterman-digital-arts-center.glb`.

## Metrics

| | Input (approved) | Shipped (optimized) | Δ |
|---|---|---|---|
| Raw bytes | 1,032,424 | 166,464 | **−83.9%** (6.2×) |
| Gzip-9 bytes | 248,805 | 104,475 | −58.0% |
| Triangles | 18,238 | 18,238 | 0 |
| Vertices | 34,958 | 12,538 after weld | −64.1% |
| Objects | 197 | 14 | −92.9% |
| Draw primitives | 215 | 20 | −90.7% |
| Materials | 12 | 12 (identical set) | 0 |
| bbox dims (m) | 312.2218 × 298.1646 × 22.0 | identical | 0 |
| bbox min / origin | `[-156.1109, -149.0823, 0.0]` | identical | 0 |

## Waste census (Phase A) and what each technique actually paid

| Finding | Predicted | Delivered |
|---|---|---|
| 22,420 coincident vertex pairs (every box authored with split corners) | large vertex win, no triangle change | 34,958 → 12,538 verts (−64%) |
| 215 primitives across 197 objects sharing 12 materials | the dominant win — node/accessor overhead | 197 objects → 14, 215 prims → 20 |
| 47 duplicate mesh groups, 3,902 redundant triangles (22 identical tree trunks, dormer families, plaza pair) | instancing candidate | **not taken** — see judgment calls |
| 0 degenerate triangles | nothing to reclaim | 0 (the build already fixed these) |
| Buried interior faces | some, at building/ground contact | 0 removed — see judgment calls |
| Over-tessellated curves (1 px ≈ 0.32 m at 468 m near distance) | trunks/pool at 8-18 segments | **not taken** — already at or below the floor |

Per-step triangle/vertex ledger is in `phaseb_stats.json`.

## Judgment calls

- **No instancing of the 47 duplicate groups.** They total 3,902 triangles, and
  meshopt already encodes the repetition efficiently — the shipped file is
  166 KB against a 500 KB budget. Shared mesh data would have fought the
  join-per-material pass, which is worth far more (215 → 20 primitives) because
  the app's cost is draw submeshes, not bytes.
- **No curve retessellation.** Tree trunks are 8-segment and the fountain pool
  18-segment cylinders; at the landmark near distance one pixel is 0.32 m, and
  halving segments would visibly facet the pool rim in the forecourt — the one
  place the camera gets close. Skip recorded per prompt §3.4.
- **No interior-face deletion.** The occluder rule requires CLOSED solids
  filling ≥ 95% of their AABB. The buildings are L- and U-shaped (fill well
  under 95%) and the ground slab is a convex-hull prism, so nothing qualified.
  The buildings' base faces sit exactly on the ground slab's top surface rather
  than inside it, so the strict-containment test correctly declined them. A
  handful of hidden triangles remain; deleting them would have needed a
  looser rule than the prompt allows, and the prompt's own history says that
  rule costs real geometry.
- **No bake.** `ALLOW_BAKE: no`; the contract forbids textures.

## Two script adaptations (both carved out, not waived)

The generic `tools/glb-optimize/` scripts assume closed solids. Two places
needed an open-shell carve-out for this asset, which joins flat single-sided
panes and ground ribbons into material groups:

1. `optimize.py` step 7 flagged `grp_Toy_white_Glow` — the two flat entrance
   glow panes — as an "inverted solid". Signed volume of an open shell is
   arbitrary (the prompt's own §3.7 says closed meshes only). The audit now
   filters by `is_closed()` and records what it skipped.
2. `validate.py`'s `G2_volumes_positive` had the same problem. Same fix.

**Honest note on what this costs:** after meshopt encoding, all 14 shipped
meshes are non-manifold by construction (vertex splitting for normals), so
**zero** meshes are closed and `G2_volumes_positive` passes vacuously. The
entire normals burden therefore falls on the ray test — which is why it matters
that it is strong: 22,500 rays, 16,657 hits, **1 flipped first face
(0.006%)** against a 0.15% gate. That single face is unchanged from the input.

## Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, no `Toy_body` | **PASS** | all 12 names round-trip; `-km` kept `Toy_gold_Glow`/`Toy_white_Glow` from merging into their non-glow twins |
| G2 Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, normals | **PASS** | bbox and origin bit-identical; flipped fraction 6e-05 |
| G3 Round-trip — Blender + pinned three GLTFLoader | **PASS** | `G3-OK`, 20 meshes, 18,238 tris, 12 materials, no decode errors |
| G4 Appearance — day+night × near+far, ≤ 2% far / ≤ 4% near | **PASS** | worst case 0.68% (night far); see table below |
| G5 Draw submeshes ≤ input | **PASS** | 215 → 20 |
| G6 Size reduced, target 60% | **PASS** | −83.9% raw |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object/material check in `phaseb_stats.json`; scripts are deterministic; `g3check/node_modules` removed |

## G4 — A/B pixel deltas

| View | Mean abs RGB | Max px delta |
|---|---|---|
| day near | 0.146% | 186 |
| day far | 0.135% | 157 |
| night near | 0.565% | 178 |
| night far | 0.684% | 76 |
| elevation N / E / S / W | 0.228% / 0.256% / 0.230% / 0.190% | 61 / 46 / 147 / 174 |

Looked at, not just measured: input and output are indistinguishable. Nothing
is missing, no silhouette moved, the lit-room pattern and the entrance glow are
identical, the roofs and dormers are unchanged. The isolated high max-delta
pixels are single-pixel edge samples on high-contrast boundaries (dormer
against roof, glow pane against wall) where quantized vertex positions shift a
sample by a fraction of a pixel — the mean is the honest number and it is under
0.7% everywhere. Nothing a player would notice.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS (fbe6228777e7, 2026-07-14) |
| gltfpack | 0.24 (`npx gltfpack@0.24 -i mid.glb -o out.glb -cc -kn -km`) |
| node | v22.19.0 |
| three (g3check) | ^0.185.1 |
| python3 + Pillow, gzip -9 | system |

`-cc -kn -km` exactly as the prompt mandates. `-km` verified to matter here:
this asset has two `_Glow` materials whose parameters differ from their non-glow
neighbours only by name, and without `-km` gltfpack would merge them and kill
the night layer.

## Deliverables

```
optimize/
  input/letterman-digital-arts-center.glb   pre-optimize archive (byte-identical)
  letterman-digital-arts-center.optimized.glb   the winner (== the shipping file)
  mid.glb                                    Phase B output, pre-packing
  inspect.py optimize.py validate.py render_ab.py diff_ab.py   adapted copies
  g3check/                                   pinned-three loader test
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                                   A/B day+night × near+far, 4 elevations
  REPORT.md                                  this file
```
