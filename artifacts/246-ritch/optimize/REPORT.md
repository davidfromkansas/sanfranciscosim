# 246 Ritch Street — GLB optimize report (stage 4)

Run 18 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no` · `TARGET_REDUCTION: 60%`

Toolchain: Blender 5.2.0 LTS (headless) · `npx gltfpack@0.24` · node + `g3check` (three 0.185.1)
· python3 3.9 + Pillow 11.3.0 · gzip -9.

## 1. Result

| | raw bytes | gzip -9 | tris | verts | primitives | draw submeshes |
|---|---|---|---|---|---|---|
| input (`optimize/input/246-ritch.glb`) | **509,272** | 104,809 | 8,496 | 18,076 | 12 | 12 |
| **shipped (`246-ritch.optimized.glb`)** | **248,928** | 106,047 | 8,492 | — | 12 | 12 |
| delta | **−51.1%** | +1.2% | −4 | — | 0 | 0 |

**gzip goes the wrong way and that is expected**: meshopt buffers are already entropy-coded, so
recompressing them adds a little. Meshopt is mandatory at intake
(`pipeline/compress-assets.mjs`), so raw bytes are the number that matters on disk and over the
wire, and 248.9 KB is well inside the 500 KB per-landmark budget in `AGENTS.md`.

## 2. Phase A — forensic inspection and waste census

`inspect.py` → `inspect_input.json`. Per-material objects (the build script already joins by
material, so there is one object per material plus one two-material body):

| object | tris | verts |
|---|---|---|
| `part_Toy_trim` | 1,692 | 3,672 |
| `part_Toy_glass` | 1,584 | 3,456 |
| `part_Toy_ink` | 1,364 | 3,024 |
| `part_Toy_roofd` | 896 | 1,872 |
| `part_Toy_white` | 896 | 1,772 |
| `part_Toy_sand` | 684 | 1,272 |
| `part_Toy_slate` | 636 | 1,440 |
| `part_Toy_steel` | 412 | 840 |
| `part_Toy_glass_Glow` | 168 | 384 |
| `part_Toy_sand_Toy_steel` | 108 | 216 |
| `part_Toy_trim_Glow` | 56 | 128 |

Census:

- **duplicate meshes: 0**, redundant tris from duplicates: 0
- **degenerate triangles: 0**
- **buried interior faces: 0** (nothing is enclosed by another closed solid)
- **join candidates: 2** (`Toy_sand` ×2, `Toy_steel` ×2) — and both are unjoinable, because in
  each pair one member is the two-material body object. Joining them would fold a body face
  into a roof-furniture mesh and change the primitive layout for no byte win.
- **coincident vertex pairs: 13,614** — this is the number that looks like waste and mostly
  is not; see §3.
- **textures: 0**. There is one exported UV layer with nothing using it; measured in §3.
- **over-tessellation:** at the landmark near distance (42.55 m) one pixel is 2.87 cm of world.
  The only over-tessellated object is `part_Toy_white`, the "246" numerals — **896 tris and
  1,772 verts, 10.5% of the model, for three digits 0.70 m wide.** That is Blender's text-curve
  resolution, not modelling. It is left in deliberately: see §5.

## 3. Phase B — measured, and deliberately reduced to nothing

`optimize.py` was run in four variants, each packed with the repo standard
`gltfpack@0.24 -c -km -kn -noq`, because the weld is not unconditionally a win — on a flat-shaded box asset the "coincident vertex
pairs" ARE the flat-shading topology and welding them makes the exporter re-split worse
(`326-brannan`: +50 KB), while on a bevelled asset it wins (`300-brannan`: −27 KB). This asset
is bevelled, so neither precedent decides it and the four-variant table does:

| variant | raw | gzip9 |
|---|---|---|
| **pack only (no Phase B at all)** | **248,928** | **106,047** |
| join only (`--no-weld --no-dissolve`) | 258,120 | 131,079 |
| weld + join (`--no-dissolve`) | 249,956 | 139,356 |
| UV-layer pruned + pack | 258,116 | 131,072 |

**Phase B is a net regression here and is reverted in full under §11 of the prompt.** Two
reasons, both worth recording because they are properties of this repo's build scripts rather
than of this building:

1. **The join is already done.** `build_246_ritch.py` ends with `join_by_material()`, so the
   step that is normally Phase B's single biggest win (node/accessor overhead, draw submeshes)
   has nothing left to do — 11 objects in, 11 objects out, 12 primitives either way.
2. **Every variant that round-trips through Blender's importer loses ~9 KB**, including the
   UV-prune one, which is why pruning a genuinely dead UV layer still came out *larger*: the
   re-import/re-export cycle re-splits vertices into a different (slightly worse-packing)
   arrangement than the authored export, and that costs more than the UV layer saves. The weld
   does cut verts hard (18,076 → 4,462) and does clear 72 degenerate triangles, but it cannot
   overcome the round-trip penalty.

So the shipped file is **`gltfpack` applied directly to the authored GLB**, which is also the
simplest thing that could work and the easiest to reproduce.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i input/246-ritch.glb -o 246-ritch.optimized.glb -c -km -kn -noq
```

`-km` and `-kn` are mandatory (without `-km`, gltfpack merges identical-parameter materials
across the `_Glow` boundary — glow-ness is name-only — and silently kills the night layer).
`-noq` is the repo standard: quantization conflicts with `pipeline/compress-assets.mjs` and with
the kit merge path's float32 requirement. Verified on the output, not on the flags: the material
name set is identical (10 names, both `_Glow` materials still separate) and the bbox re-imports
within tolerance.

## 5. Judgment calls

- **The "246" numerals keep their 896 triangles.** They are over-tessellated by Phase B step 4's
  own test — Blender's text-to-mesh curve resolution on 0.46 m digits — and dropping the curve
  resolution in `build_246_ritch.py` would recover ~10% of the model. It was not done, because
  the change is upstream of stage 2 and would invalidate every approved review render for a
  saving no gate needs: the asset is at 8,496 of a 9,000 cap and 248.9 KB of a 500 KB budget.
  Recorded here so the next revision of this asset gets it for free.
- **The dead UV layer stays.** Removing it is a real (if small) win in principle and a measured
  loss in practice, for the round-trip reason in §3.
- **Limited dissolve was never run**, by construction (`--no-dissolve` is this asset's default in
  the adapted `optimize.py`). §3.3 of the prompt says to skip it on assets with large coplanar
  ring bands, and this one has three: the parapet, the dark coping and the roof-deck curb. A
  merged annulus ngon re-triangulates into slivers whose averaged vertex normal collapses to ~0,
  and gltfpack re-emits the STORED normals, so the failure appears only in the packed file.

## 6. Per-asset adaptations to the generic scripts

`tools/glb-optimize/` was copied and adapted, not rewritten. Four changes:

1. `optimize.py` gained `--no-weld` and `--no-dissolve` so the four-variant table in §3 is one
   command each, and the dissolve step is gated off by default for the ring-band reason above.
2. `validate.py` now **welds into a throwaway bmesh before judging closedness.** glTF stores
   split vertices for flat shading, so on re-import every solid reads as an open shell and the
   signed-volume gate is vacuous without it. It also reports which objects are genuinely open
   and excludes them from the gate — `part_Toy_ink` is one, being a per-material join of many
   separate solids.
3. `validate.py`'s ray-flip gate is now a **delta**, not an absolute. The gate exists to catch
   the optimizer flipping windings; an asset's own standing residual is its own business. Here
   both sides measure 0.000000 so the distinction is moot, but the gate is now the right shape.
4. `render_ab.py` runs at 40 Cycles samples rather than 64. The A/B pass is a difference
   measurement with an identical rig on both sides, and this Mac was at load 180–270 with a
   dozen parallel Blender sessions.

## 7. Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material name set identical (10); `Toy_glass_Glow` and `Toy_trim_Glow` still separate; no `Toy_body`; no manifest node names to preserve |
| **G2** geometry | **PASS** | bbox 28.3678 × 28.1556 × 18.76 both sides (delta 0); origin delta 0; signed volumes positive on every closed solid; ray-flip 0.000000 in and out, **delta 0.000000** |
| **G3** round-trip | **PASS** | Blender re-import clean; `g3check` (three 0.185.1 + MeshoptDecoder): `{"ok":true,"meshes":12,"tris":8496,"materials":[10 names],"bbox_dims":[28.3678,18.76,28.1556]}` |
| **G4** appearance | **PASS** | worst view `elev_n` at **0.0019%** mean absolute RGB (gate: ≤ 2% far / ≤ 4% near). day_near 0.0009%, day_far 0.0009%, night_near 0.0001%, night_far 0.0002%, elev_s and elev_w exactly 0. Worst single pixel 21/255 on one anti-aliased edge. **Looked at:** the ×8-amplified diff row of `renders/contact_sheet.png` is black apart from a handful of one-pixel marks on silhouette edges. Nothing a player could notice; no missing element, no silhouette change, no shading artefact, the night layer intact in both |
| **G5** draw submeshes | **PASS** | 12 → 12 |
| stage-2 contract re-check | **PASS** | `validate_246_ritch.py` re-run on the SHIPPED meshopt file: 8,492 tris, dims 28.3678 × 28.1556 × 18.76, min Z 0, 11 objects, 16/16 checks |
| **G6** size | **PASS (with census)** | −51.1% raw, short of the 60% aspiration. The census in §2 shows the remainder is geometry: zero duplicates, zero degenerates, zero buried faces, already joined per material, and the two remaining join candidates are structurally unjoinable. The one genuine piece of waste (the numerals, §5) is named rather than hidden |
| **G7** GPU budget | n/a | `ALLOW_BAKE: no`, no textures |
| **G8** hygiene | **PASS** | re-import object/primitive counts match; no foreign geometry; re-running the single gltfpack command reproduces the output byte-for-byte; no `.blend1` left |

## 8. Shipping swap

`246-ritch.optimized.glb` copied over `artifacts/246-ritch/246-ritch.glb`; the pre-optimize
original is archived at `optimize/input/246-ritch.glb`. `artifacts/246-ritch/validation.json` and
`REPORT.md` carry the shipped numbers, so the integration stage writes its manifest entry from
reality.

## 9. Reproducing

```bash
B=/Applications/Blender.app/Contents/MacOS/Blender
$B -b --python inspect.py  -- input/246-ritch.glb inspect_input.json
npx gltfpack@0.24 -i input/246-ritch.glb -o 246-ritch.optimized.glb -c -km -kn -noq
$B -b --python validate.py -- input/246-ritch.glb 246-ritch.optimized.glb validation.json
(cd g3check && npm install && node check.mjs ../246-ritch.optimized.glb)
$B -b --python render_ab.py -- input/246-ritch.glb   renders/in
$B -b --python render_ab.py -- 246-ritch.optimized.glb renders/out
/usr/bin/python3 diff_ab.py
```

The four-variant table in §3 is reproduced with `optimize.py`'s `--no-weld` / `--no-dissolve`
and `prune_uv.py`.
