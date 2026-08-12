# 380 Brannan Street — GLB optimize report (stage 4)

Run 12 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node v22.19.0, pinned three via
`g3check/`, python3 + Pillow 11.3.0, gzip -9.

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 461,728 B | **222,516 B** | **−51.8%** |
| File, gzip −9 | 82,556 B | 166,998 B | +102% (see §4) |
| Triangles | 7,832 | 7,760 | −0.9% |
| Vertices | 15,707 | 13,582 | −13.5% |
| Objects | 115 | 12 | −89.6% |
| Draw submeshes (primitives) | 116 | **13** | −88.8% |
| Materials | 11 | 11 | unchanged |
| BBox | 31.3134 × 31.5872 × 12.6 | 31.3134 × 31.5872 × 12.6 | within 1e-4 m |

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Coincident vertex pairs | 11,583 | welded (per-object, ≤ 1 mm) |
| Objects sharing a material | 115 across 9 groups | joined per material |
| Duplicate mesh groups | 19 groups / 3,560 redundant tris | absorbed by the per-material join |
| Degenerate triangles | 15 | removed |
| Buried interior faces | 0 removable | see §3 |
| Over-tessellated curves | none | the only curves are 4-segment arch heads, already minimal |

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 7,832 | 15,707 |
| weld + degenerate | 7,784 | 4,118 |
| interior faces | 7,784 | 4,118 |
| limited dissolve 0.05° | 7,760 | 4,106 |
| join per material | 7,760 | 4,106 |

Joins: `Toy_glass` 36, `Toy_rust` 31, `Toy_stone` 15, `Toy_ink` 9, `Toy_steel` 6,
`Toy_glassl` 5, `Toy_roofd` 4, `Toy_coral` 3, `Toy_glass_Glow` 3. `Toy_slate` and
`Toy_trim_Glow` are single objects already.

**Zero interior faces removed, deliberately.** The occluder rule requires a CLOSED
solid; the only candidate here is the masonry body, whose AABB fill is 48.5% because
the building sits at 45° to the world axes. Treating it as a box-like occluder would
have deleted real facade geometry. This is the hard-learned rule in the prompt's §3.2
doing its job.

Limited dissolve was run at 0.05°, not 0.5°.

Normals after Phase B: 12/12 signed volumes positive, `inverted_solids: []`.

## 4. Phase C — packing, and a documented conflict

**The prompt's `-cc -kn -km` recipe is wrong for this repo.** Run as written it
produced a 90,328-byte file — a headline 5.1× reduction — but with
`KHR_mesh_quantization` in `extensionsRequired`. That output:

- failed two checks of the asset's own stage-2 contract validator
  (`transforms_applied`, `no_unexpected_objects`), because gltfpack stores the
  dequantize matrix as a node transform and splits every node into an empty parent
  plus a `Mesh_N` child;
- contradicts `pipeline/compress-assets.mjs`, the **mandatory** ship step per
  `.agents/skills/sf-asset-check/SKILL.md` §8, which runs `-c -km -kn -noq` with the
  code comment *"-noq keeps attributes float32: the kit/landmark merge …"*;
- sits against `sf-asset-check`'s warning that *"default quantization silently
  breaks the app's merge paths (every piece falls back to procedural and the city
  looks fine)"*.

**That last warning turns out to be overstated, and this report originally
over-claimed on the back of it.** `st-marys-cathedral.glb` ships quantized, and the
running app merges it perfectly well:

```
sf-assets: st-marys-cathedral merged 9 objects / 8 materials -> batched (1606 tris body); uniform x1.0000 at 1066, -1574
```

A merge line with a scale factor is the success path — a genuine failure warns and
keeps the code-built version instead. So quantization does **not** break the runtime
merge, three's `GLTFLoader` handles `KHR_mesh_quantization` natively, and St Mary's is
fine in production. The skill's warning is most likely about gltfpack's *other*
defaults (without `-km` it merges materials across the `_Glow` boundary, without
`-kn` it drops the node names), which genuinely are silent killers.

Evidence from what is already shipped in `app/public/sf-assets/landmarks/`:

| Asset | Quantized | Primitives |
|---|---|---|
| st-marys-cathedral | **yes** | 9 |
| city-hall | no | 10 |
| columbus-tower | no | 306 |
| coit-tower | no | 194 |
| de-young | no | 112 |

Only `st-marys-cathedral` — the one asset previously taken through this optimize
prompt — is quantized. Everything else went through `compress-assets.mjs` and is not.

**Decision: ship the `-noq` build.** Not because quantization is broken — it isn't —
but because `-noq` matches `pipeline/compress-assets.mjs`, the mandatory ship step,
and its stated intent of keeping attributes float32; and because the `-noq` output
passes all 16 checks of the stage-2 contract validator where the quantized build
passes only 14. The cost is 132 KB on a file that is well inside the 500 KB budget,
which is a cheap price for matching the repo's own tool.

A reasonable person could ship the quantized 90 KB build instead. If that becomes the
house style, the contract validator's `transforms_applied` and
`no_unexpected_objects` checks need relaxing for quantized assets first — right now
they would fail every one.

Final command:

```
npx gltfpack@0.24 -i mid.glb -o 380-brannan.optimized.glb -c -km -kn -noq
```

`extensionsRequired: ["EXT_meshopt_compression"]`, 0 of 12 nodes carry a
scale/translation — byte-for-byte the same shape as the other shipped landmarks.

`st-marys-cathedral.glb` was left untouched, and needs no action: it merges correctly
despite being quantized (see the console line above).

## 5. Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures without a recorded
exception.

## 6. Phase E — A/B verification

Same rig, input vs shipped, day and night at near (1.5× long axis) and far (6×),
plus four orthographic elevations. Renders in `renders/`, amplified diffs and
`renders/contact_sheet.png`, numbers in `diffs.json`.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day_near | 0.0138% | 189 |
| day_far | 0.0121% | 23 |
| night_near | 0.0038% | 40 |
| night_far | 0.0051% | 16 |
| elev_n | 0.0758% | 58 |
| elev_e | 0.0214% | 115 |
| elev_s | 0.0700% | 42 |
| elev_w | 0.0904% | 47 |

Gate is ≤ 2% far / ≤ 4% near; worst observed 0.09%.

**Looked at, not just measured.** At x8 amplification the diffs are a faint outline
tracing shared edges and a handful of brighter pixels along window frame borders and
the coping edge — single-pixel rasterisation differences from welded vertices landing
a fraction of a millimetre apart. No element is missing, the silhouette is unchanged,
no shading artifacts, and the night glow set is identical. There is nothing here a
player could notice.

## 7. Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, node names intact | **PASS** | 11 → 11 materials; both `_Glow` names preserved; `-km -kn` |
| G2 Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox delta < 1e-4 m; 12/12 positive; flipped 1/17,032 = 0.0059% |
| G3 Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `G3-OK … meshes:13 tris:7760`, 11 materials, no decode errors |
| G4 Appearance — day+night × near+far | **PASS** | worst 0.09% vs 2%/4% gate; §6 description |
| G5 Draw submeshes ≤ input | **PASS** | 116 → 13 |
| G6 Size reduced | **PASS with note** | raw −51.8%, short of the 60% target; see below |
| G7 GPU budget | **N/A** | bake mode not used |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object/material/bbox match; scripts committed; no `.blend1` |

**G6 note.** 51.8% raw reduction is under the 60% aspiration. The census accounts for
the remainder: after welding and joining, what is left is 7,760 triangles of
silhouette and facade geometry at float32 — and float32 is a deliberate constraint
(§4), not slack. Choosing the quantized build would have hit 80.4% and failed the
contract. At 222 KB the asset is well inside the 500 KB per-asset budget of
`sf-asset-check` §7.

## 8. Deliverables

```
optimize/
  input/380-brannan.glb          # byte-identical archive of the pre-optimize asset
  380-brannan.optimized.glb      # the shipped file (copied over ../380-brannan.glb)
  inspect.py optimize.py validate.py render_ab.py diff_ab.py  g3check/
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                       # in_/out_ day+night near+far, 4 elevations, diffs, contact sheet
  REPORT.md
```

Re-running `optimize.py` then the gltfpack command on `input/380-brannan.glb`
reproduces the shipped file.
