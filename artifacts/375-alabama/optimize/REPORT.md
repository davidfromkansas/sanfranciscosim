# 375 Alabama Street — GLB optimize report (stage 4)

Run 12 August 2026 per `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md`.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

Toolchain: Blender 5.2.0 LTS, `npx gltfpack@0.24`, node v22.19.0, pinned three via
`g3check/`, python3 + Pillow 11.3.0, gzip −9.

## 1. Metrics

| Metric | Input | Shipped | Delta |
|---|---|---|---|
| File, raw | 753,288 B | **318,672 B** | **−57.7%** |
| File, gzip −9 | 105,946 B | 182,944 B | +72.7% (see §4) |
| Triangles | 11,604 | 11,604 | 0% |
| Vertices | 23,128 | 6,488 | **−71.9%** |
| Objects | 345 | 13 | −96.2% |
| Draw submeshes (primitives) | 346 | **14** | −96.0% |
| Materials | 12 | 12 | unchanged |
| BBox | 67.3172 × 61.6109 × 22.5 | 67.3172 × 61.6109 × 22.5 | within 1e-4 m |

## 2. Waste census (Phase A)

| Finding | Value | Action |
|---|---|---|
| Coincident vertex pairs | 16,640 | welded (per-object, ≤ 1 mm) |
| Objects sharing a material | 345 across 11 groups | joined per material |
| Duplicate mesh groups | 43 groups / 8,340 redundant tris | absorbed by the per-material join |
| Degenerate triangles | 0 | — |
| Buried interior faces | 0 removable | see §3 |
| Over-tessellated curves | none eligible | see §3 |

The 345-object count is the dominant waste here and it is structural: the night state
alone is 126 separate glow shells (one per lit bay), and the medallion frieze is 23 cogs
plus 23 hubs. Every one of those was a distinct node, mesh, and draw primitive in the
input.

## 3. Phase B — geometry cleanup

| Step | Tris | Verts |
|---|---|---|
| input | 11,604 | 23,128 |
| weld + degenerate | 11,604 | 6,488 |
| interior faces | 11,604 | 6,488 |
| limited dissolve 0.05° | 11,604 | 6,488 |
| join per material | 11,604 | 6,488 |

Joins: `Toy_glass_Glow` 126, `Toy_stone` 76, `Toy_cream` 73, `Toy_ink` 26, `Toy_glass` 15,
`Toy_steel` 12, `Toy_glassl` 5, `Toy_trim` 3, `Toy_trim_Glow` 3, `Toy_glassl_Glow` 2,
`Toy_roofd` 2. `Toy_mauve` is a single object already.

Triangles did not move at all. That is the expected outcome for an asset authored as
closed, non-overlapping-shell primitives with flat shading: there were no degenerate faces
to remove, and limited dissolve at 0.05° found no strictly coplanar merges that survive the
material and sharp-edge delimiters. The entire win is in vertices (−71.9%) and node count
(−96.2%). Welding alone took 23,128 verts to 6,488 — flat shading splits every vertex per
face on export, and the weld puts them back.

**Zero interior faces removed, deliberately.** The occluder rule requires a CLOSED solid.
The candidates here are the body prism and the tower body, both closed — but the body's
AABB fill is only 87% (the block sits at 4.32° to the world axes) and the geometry it
would "hide" is the pier, glazing-band and parapet panels applied to its own outer faces,
which are coplanar with it rather than inside it. Treating it as an occluder would have
deleted real facade geometry. This is the hard-learned rule in the prompt's §3.2 doing its
job.

**No curve retessellation.** The only curved shells are the 23 cog medallions and their
hubs. The chord-error arithmetic says a 24-gon at r = 0.85 m could be halved and stay
inside one screen pixel at the near distance — but the medallions are not tessellated
circles, they are 12-tooth gears where every second vertex is a tooth root. Halving the
segments would make them 6-tooth stars, which destroys recognition cue #1. Skipped, and
noted here as the prompt requires.

Limited dissolve was run at 0.05°, not 0.5°.

Normals after Phase B: 13/13 signed volumes positive, `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 375-alabama.optimized.glb -c -km -kn -noq
```

`-noq` rather than the prompt's `-cc`, following the decision recorded in
`artifacts/380-brannan/optimize/REPORT.md` §4: `-noq` is what
`pipeline/compress-assets.mjs` — the mandatory ship step per `sf-asset-check` §8 — runs,
and its stated intent is keeping attributes float32. The quantized build was produced for
comparison and measured at **131,920 B (−82.5%)**, but it carries
`KHR_mesh_quantization`, stores the dequantize matrix as a node transform, and splits every
node into an empty parent plus a `Mesh_N` child — which fails two checks of this asset's own
stage-2 contract validator (`transforms_applied`, `no_unexpected_objects`). The `-noq`
build passes all 16. 318 KB is well inside the 500 KB per-asset budget, so matching the
repo's own tool is the cheaper trade.

Verified on the output rather than trusted from flags:

- `extensionsRequired: ["EXT_meshopt_compression"]` only
- 12 material names identical to the input, both `_Glow` names separate
- 13 nodes, **0** carrying scale/translation/rotation
- node names intact: `body`, `tower_panel`, `grp_Toy_*`

**gzip goes up, not down.** 105,946 → 182,944 B. Meshopt buffers are already
entropy-coded, so gzip has nothing left to find and adds framing; the raw byte count is
what the CDN and the loader actually move. Same behaviour as `380-brannan`.

## 5. Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures without a recorded exception.

## 6. Phase E — A/B verification

Same rig, input vs shipped, day and night at near (1.5× long axis = 101 m) and far (6×),
plus four orthographic elevations. Renders in `renders/`, amplified diffs and
`renders/contact_sheet.png`, numbers in `diffs.json`.

| View | Mean abs RGB delta | Max px delta |
|---|---|---|
| day_near | 0.0086% | 33 |
| day_far | 0.0150% | 25 |
| night_near | 0.1512% | 152 |
| night_far | 0.2225% | 72 |

| Elevation | Mean abs RGB delta | Max px delta |
|---|---|---|
| north | 0.0419% | 49 |
| east | 0.0449% | 81 |
| south | 0.0079% | 44 |
| west | 0.0069% | 32 |

Gate is ≤ 2% far / ≤ 4% near; worst observed 0.22%.

**Looked at, not just measured.** Side by side the night pair is indistinguishable: the
same 125 lit bays in the same staggered pattern, the same two lit sawtooth stretches, the
same tower crown. At ×8 amplification the night diff is a wash of speckle across the
emissive-lit roof plane and a faint outline on window-frame edges — Cycles sampling and
denoiser variance in a scene lit almost entirely by emission, which is why the night
numbers run an order of magnitude above the day ones while the day diffs are almost blank.
The day diffs are a hairline tracing shared edges where welded vertices land a fraction of
a millimetre apart. No element is missing, the silhouette is unchanged, no shading
artifacts, the glow set is identical. There is nothing here a player could notice.

## 7. Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract — material set identical, `_Glow` separate, node names intact | **PASS** | 12 → 12 materials; `Toy_glass_Glow`, `Toy_glassl_Glow`, `Toy_trim_Glow` all preserved; `-km -kn` |
| G2 Geometry — bbox ≤ max(1 cm, 0.1%), origin ≤ 1 cm, volumes positive, flips ≤ 0.15% | **PASS** | bbox delta < 1e-4 m; 13/13 positive; flipped 0/20,745 = 0.0% |
| G3 Round-trip — Blender + pinned-three GLTFLoader | **PASS** | `G3-OK … meshes:14 tris:11604`, 12 materials, no decode errors |
| G4 Appearance — day+night × near+far | **PASS** | worst 0.22% vs 2%/4% gate; §6 description |
| G5 Draw submeshes ≤ input | **PASS** | 346 → 14 |
| G6 Size reduced | **PASS with note** | raw −57.7%, just short of the 60% target; see below |
| G7 GPU budget | **N/A** | bake mode not used |
| G8 Hygiene — no foreign geometry, deterministic, no `.blend1` | **PASS** | re-import object/material/bbox match; scripts committed; no `.blend1` |

**G6 note.** 57.7% raw reduction is 2.3 points under the 60% aspiration. The census
accounts for the remainder: after welding and joining, what is left is 11,604 triangles of
silhouette and facade geometry at float32, and float32 is a deliberate constraint (§4), not
slack. The quantized build would have hit 82.5% and failed the contract validator.

The asset's own stage-2 contract validator was re-run against the shipped file after the
swap: **overall PASS, 16/16**, 11,604 triangles, 13 objects.

## 8. Deliverables

```
optimize/
  input/375-alabama.glb          # byte-identical archive of the pre-optimize asset
  375-alabama.optimized.glb      # the shipped file (copied over ../375-alabama.glb)
  inspect.py optimize.py validate.py render_ab.py diff_ab.py  g3check/
  inspect.json phaseb_stats.json validation.json diffs.json
  renders/                       # in_/out_ day+night near+far, 4 elevations, diffs, contact sheet
  REPORT.md
```

Re-running `optimize.py` then the gltfpack command on `input/375-alabama.glb` reproduces
the shipped file.
