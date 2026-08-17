# 35 South Park — GLB optimize pass (stage 4)

Run 17 August 2026 against `artifacts/35-south-park/35-south-park.glb` per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`, defaults `ASSET_CLASS: landmark`,
`ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`. Scripts are adapted copies of
`tools/glb-optimize/` (by way of `artifacts/168-south-park/optimize/`, the nearest
asset in shape class).

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node + pinned three in
`g3check/package.json`, python3 + Pillow 11.3.0, gzip.

## 1. Metrics

| | input | shipped | delta |
|---|---|---|---|
| raw bytes | 394,856 | **211,704** | **−46.4%** |
| gzip −9 bytes | 74,661 | 146,649 | +96.4% — see §5 |
| triangles | 6,980 | 6,980 | 0 |
| vertices (Blender re-import) | 13,440 | 14,812 | +10.2% — see §5 |
| mesh objects | 95 | **10** | −89.5% |
| draw submeshes (primitives) | 95 | **10** | −89.5% |
| materials | 10 | 10 | identical set |
| bbox | 42.05858 × 40.29912 × 13.4 | identical to 5 dp | 0 |
| origin (xy centre) | (−0.00009, 0.82907) | identical | 0 |

## 2. Waste census (Phase A)

| technique | finding | acted on |
|---|---|---|
| duplicate meshes | 5 identical archivolts, 5 identical arch reveals, 4 identical roundel rings/discs, 4 identical sconces — **3,884 redundant triangles** across the repeat groups | **not deduplicated**: these are 5 and 4 instances of small meshes, and glTF instancing costs a node each while the join in Phase B already collapses them into one primitive per material. Instancing wins only for large counts of heavy repeats (§3.6). |
| coincident verts | 9,772 pairs | welded (Phase B step 1) |
| degenerate faces | 0 | nothing to do |
| buried interior faces | 0 provably-buried faces found | nothing to do |
| over-tessellation | one-pixel world size at the near distance is 0.0425 m; the arch profiles (10 seg), roundels (14 seg) and the vent (10 seg) are all above that chord error | **skipped** — see §3 |
| object-count overhead | 95 objects over 10 materials | joined (Phase B step 5) — the single biggest win |

## 3. Phase B — what ran and what was skipped

1. **Weld ≤ 1 mm, per object** — 13,440 → 3,668 verts, triangles unchanged. glTF stores
   split vertices for flat shading, so most of that is the exporter's own duplication;
   the export re-splits by material after the join, which is why the shipped vertex
   count comes back up (§5).
2. **Degenerate + buried interior faces** — none found. The build script emits closed
   solids with no coplanar overlaps by construction (that discipline was already forced
   at stage 2 by the roof-slab z-fight, see the asset's `REPORT.md` §4.2).
3. **Limited dissolve — SKIPPED.** `GLB-OPTIMIZE-PROMPT` §3.3. This asset has **six**
   ring bands that follow the whole footprint — `water_table`, `architrave`, `frieze`,
   `cornice`, `parapet`, `coping` — plus a body prism whose cap is a 791 m² coplanar
   ngon. Their top and bottom faces are perfect coplanar annuli, so even a
   strictly-coplanar dissolve merges each ring into one annulus ngon, and
   re-triangulating an annulus emits sub-millimetre slivers tens of metres long that no
   area-based degeneracy test catches and that only surface in the packed file as
   `invalid_or_nonunit_loop_normal_count`. Measured on `350-brannan`, 13 Aug 2026. On an
   asset of this shape the step is worth well under 1% of triangles.
4. **Curve retessellation — SKIPPED.** The only curves are five 10-segment arch
   profiles, four 14-segment roundels and one 10-segment vent. All are at the floor of
   the style bible's 8–14 segment range, and the arches and roundels are the hero
   elevation's silhouette. Halving them is not available.
5. **Join per material** — 95 objects → 10. No manifest-named nodes and no `Toy_body`
   on a landmark, so nothing had to be held out. `roof_slab` stayed separate because it
   is the only object carrying `Toy_steel` alone.
6. **Instance vs join** — see the census: join.
7. **Normals audit** — all 10 output solids have positive signed volume;
   `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 35-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the `_Glow` materials separate from their identically-parametered
non-glow twins (`Toy_glass_Glow` carries the same `6f95b8` as `Toy_glassl`; without
`-km` gltfpack would merge them and silently kill the night layer). `-noq` is the repo
standard and is what `pipeline/compress-assets.mjs` produces.

## 5. Two numbers that went the "wrong" way, and why they are correct

- **gzip grew (74.7 KB → 146.6 KB).** Meshopt-compressed buffers are already
  entropy-coded, so gzip has nothing left to find; the raw byte count is the number
  that matters and it fell 46.4%. Every GLB under `app/public/sf-assets/` is expected
  to be meshopt-compressed on intake because the loaders register `MeshoptDecoder`
  (`app/src/gltf.js`, `app/src/assets.js`), and the alternative — shipping an
  unpacked file that happens to gzip smaller — would fail the intake rule and give up
  the GPU-side win. 211.7 KB is well inside the 500 KB per-landmark budget.
- **Vertices grew after the weld (3,668 → 14,812 on re-import).** The weld is measured
  inside Blender before export; the glTF exporter then re-splits vertices per flat face
  and per material group. The join concentrates ten material groups into ten
  primitives, so the split count rises even though the mesh is topologically welded.
  Triangles, bbox and appearance are unchanged, which is what the gates test.

## 6. Gate results

| gate | result | evidence |
|---|---|---|
| **G1** contract | **PASS** | material name set identical (10, including both `_Glow`); `_Glow` kept separate; no `Toy_body`; no manifest node names on a landmark |
| **G2** geometry | **PASS** | bbox identical to 5 dp; origin identical; all signed volumes positive; ray flip 0/15,446 hits over 22,500 rays = **0.000000** (input also 0.0) |
| **G3** round-trip | **PASS** | Blender re-import clean; `g3check` → `{"ok":true,"meshes":10,"tris":6980,...}` with the full material list and `EXT_meshopt_compression` only |
| **G4** appearance | **PASS** | day near 0.0011%, day far 0.0039%, night near 0.0003%, night far 0.0009%, elevations 0.0016–0.0259% — all far inside the ≤4% near / ≤2% far gate. The diff images are black apart from a scatter of single-pixel edge samples; nothing structural, no missing element, no silhouette change, and the night layer is intact (the lit arcade and the four sconces both render) |
| **G5** draw submeshes | **PASS** | 95 → 10 |
| **G6** size | **PASS with a note** | −46.4% raw, short of the 60% aspiration. The census explains the remainder: Phase B removed **zero** triangles because the input had no degenerate, buried or duplicate-in-place geometry, so every byte saved came from the join and the pack. What is left is silhouette geometry — five arches, four roundels, six ring bands and a penthouse — at 6,980 triangles against a 9,000 budget |
| **G7** GPU budget | n/a | `ALLOW_BAKE=no`, no textures |
| **G8** hygiene | **PASS** | re-import object/material/bbox check in `phaseb_stats.json`; no foreign geometry; no `.blend1` files; scripts are deterministic and committed here |

## 7. Shipping swap

`35-south-park.optimized.glb` was copied over `artifacts/35-south-park/35-south-park.glb`;
the pre-optimize original is archived byte-for-byte at
`optimize/input/35-south-park.glb`. The asset's `REPORT.md` and `validation.json` were
re-generated against the shipped file so the integration stage writes its manifest entry
from reality.
