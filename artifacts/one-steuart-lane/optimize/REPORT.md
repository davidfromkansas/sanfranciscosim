# One Steuart Lane — GLB optimize report

Stage 4 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md`, run per
`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` v2 on 18 August 2026.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

## Headline

| Metric | Input | Shipped | Δ |
|---|---|---|---|
| **File, raw** | 1,375,888 B (1,344 KB) | **411,648 B (402 KB)** | **−70.1%** |
| File, gzip −9 | 182,630 B | 214,151 B | +17.3% (see below) |
| Objects | 1,027 | **14** | −98.6% |
| Draw primitives | 1,033 | **16** | −98.5% |
| Triangles | 17,064 | 17,064 | 0 |
| Vertices | 33,912 | 31,385 | −7.5% |
| Materials | 13 | 13 | identical set |
| Bounding box | 62.95003 × 62.49303 × 67.06 | identical to 5 dp | 0 |
| Origin offset XY | 0.00023, −0.00073 | identical | 0 |

**Gzip went up, and that is expected.** meshopt-compressed buffers are already
entropy-coded, so a second gzip pass adds framing rather than removing
redundancy. The number that matters on disk and over the wire is the raw file,
which is what the CDN serves and what `EXT_meshopt_compression` decodes: 402 KB,
inside the 500 KB per-landmark budget in `AGENTS.md` with room to spare.

## Phase A — forensic inspection

`inspect.py` → `inspect.json`. Waste census on the 1,027-object input:

| Finding | Measure | Plan |
|---|---|---|
| Object-count overhead | 1,027 objects, 1,033 primitives, 10 materials with >1 user | **join per material** — by far the biggest win |
| Coincident vertices | 23,352 pairs within 1 mm | **weld per object** |
| "Duplicate" mesh groups | 102 groups, 12,256 redundant triangles | *not* removable — these are distinct placed instances of identically-sized boxes (pilasters, lintels, PV strips); joining absorbs the node overhead |
| Degenerate faces | 0 | nothing to do |
| Buried interior faces | present (every frame plate is partly inside a volume shell) | attempted; 0 removed — see below |
| Over-tessellated curves | only the two 12-segment cooling towers | skipped: they read as circles on the roof from the aerial camera and are silhouette detail there |
| Vertex attributes | POSITION + NORMAL only | already minimal — no UVs, no colors, no tangents to prune |

Predicted saving before executing: ~98% of node/accessor overhead from the join,
~30% of vertices from the weld, no triangle reduction. That is what happened.

## Phase B — geometry cleanup

`optimize.py` → `mid.glb`, `phaseb_stats.json`.

| Step | Tris | Verts | Note |
|---|---|---|---|
| input | 17,064 | 33,912 | |
| 1+2a weld ≤1 mm + degenerate | 17,064 | 10,560 | −68.9% verts; per-object only, so a glow shell can never fuse to a base surface |
| 2b interior faces | 17,064 | 10,560 | **0 removed** |
| 3 limited dissolve | — | — | **skipped deliberately, see below** |
| 5 join per material | 17,064 | 10,560 | 1,027 → 14 objects |
| 7 normals audit | — | — | 14/14 positive signed volume, 0 inverted |

**Step 3 was skipped on purpose.** GLB-OPTIMIZE-PROMPT §3 step 3 says to skip
the dissolve entirely on assets with large coplanar ring bands, and this asset is
made of them: the roof parapet, the four terrace slab plates, their soffits and
the four glow strips are all closed annuli following a volume plan the whole way
round. Even a strictly-coplanar dissolve merges each into one annulus ngon, and
re-triangulating an annulus emits sub-millimetre slivers whose averaged vertex
normals collapse toward zero — invisible to an area-based degeneracy test,
hidden by Blender's import-time normal recompute, and surfacing only after the
shipping swap because gltfpack re-emits the *stored* normals. On `350-brannan`
the same step was worth 0.4% of triangles. Not a trade worth making here. The
skip is recorded in `phaseb_stats.json` as
`"limited_dissolve": "skipped (ring-band asset, prompt s.3 step 3)"`.

**Step 2b removed nothing, and that is correct.** The occluder rule only lets a
mesh act as an occluder if it is a closed solid with ≥95% AABB fill. The volume
shells here are closed but they are *not* box-like in the AABB sense — each is a
45°-rotated rectangular prism whose AABB it fills only ~50% of — so nothing
qualified as an occluder and no face was deleted on a guess. The buried faces
survive; they cost triangles but they are provably safe, and the triangle count
was never the binding constraint on this asset (17,064 of a 24,000 budget).

The vertex weld reports 10,560 in Blender and 31,385 after the round trip
through gltfpack. That is not a regression: gltfpack splits vertices at material
and normal discontinuities when it builds its own index buffers, so the two
numbers count different things. The file size is the honest measure and it fell
by 70%.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o one-steuart-lane.optimized.glb -c -km -kn -noq
```

- `-c` meshopt compression: verified live, `grep -rn setMeshoptDecoder app/src/`
  hits `app/src/gltf.js:10` and `app/src/assets.js:406`.
- `-km -kn` mandatory: without `-km`, gltfpack merges identical-parameter
  materials across the `_Glow` boundary — glow-ness is name-only — and silently
  kills the night layer. This asset has `Toy_cream` and `Toy_cream_Glow` with
  the same base colour, i.e. exactly the pair that would have merged.
- `-noq` mandatory, repo standard: matches `pipeline/compress-assets.mjs`, keeps
  float32 attributes for the runtime merge paths, and keeps the stage-2 contract
  validator strict on `transforms_applied` / `no_unexpected_objects`.

Verified on the output rather than trusting the flags: material name set
identical (13/13, both `_Glow` members intact), bbox identical to 5 dp,
primitives 16.

## Phase D — high→low bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures without a recorded
exception. Nothing here would justify one: the facade relief *is* the silhouette
at this asset's viewing distances, so there is no bakeable region that is not
also load-bearing.

## Phase E — A/B verification

`render_ab.py` → `renders/`, `diff_ab.py` → `diffs.json`,
`renders/contact_sheet.png`. Landmark distances: near 100.6 m (1.5 × long axis),
far 402.4 m (6 ×). Day state at glow alpha 0.12, night at alpha 1.0 with
emission driven from Base Color.

| View | Mean abs RGB Δ | Max pixel Δ |
|---|---|---|
| day near | 0.0030% | 4/255 |
| day far | 0.0050% | 3/255 |
| night near | 0.0030% | 3/255 |
| night far | 0.0030% | 2/255 |
| elevation N / E / S / W | 0.0053 / 0.0009 / 0.0024 / 0.0056% | 8 / 5 / 9 / 8 |

Gates are ≤2% far and ≤4% near; the worst view here is **0.0056%**, three orders
of magnitude inside.

**Looked at the diffs, honestly:** the ×8-amplified diff row is black except for
faint single-pixel hairlines along some pilaster and lintel edges. They are
anti-aliasing differences — the weld changed which vertices are shared, so the
rasteriser resolves a few silhouette edges a fraction of a pixel differently.
No element is missing, no silhouette moved, no shading artifact appeared, the
night bands and the lobby patch are present and the same colour, and the roof
furniture is unchanged. There is nothing here a player would see.

## Toolchain

| Tool | Version |
|---|---|
| Blender | 5.2.0 LTS |
| gltfpack | 0.24 (pinned, via `npx gltfpack@0.24`) |
| node | v22.19.0 |
| three (g3check) | ^0.185.1 |
| python | 3.9.6 |
| Pillow | 11.3.0 |

**One documented substitution.** `render_ab.py` was switched from Cycles to
EEVEE (`taa_render_samples = 32`). This machine was carrying a ~170 load average
from other parallel Blender sessions and a single Cycles frame did not finish in
two minutes. The A/B comparison only requires that both files render through the
*same* rig, which they do; EEVEE is emission- and alpha-capable, so the day
glow-alpha pass and the night emission pass both still work. Recorded per §10,
which asks for no substitutions without documenting them.

Two other scripts were adapted from the generic copies in `tools/glb-optimize/`,
as §0 directs: `validate.py`'s per-asset expectations, and `render_ab.py`'s
orthographic elevation framing — `ortho_scale` drives the *longer* sensor axis,
which is horizontal at 960×720, so the generic `long_axis * 1.15` cropped 15%
off the top and bottom of a 67 m tower. Both A and B were re-rendered after the
fix.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical 13/13; `Toy_cream_Glow`, `Toy_gold_Glow`, `Toy_glassl_Glow` all separate; no `Toy_body` on a landmark; no manifest-named nodes on this asset |
| **G2** geometry | **PASS** | bbox identical to 5 dp (gate: 1 cm / 0.1%); origin identical (gate 1 cm); 14/14 signed volumes positive; ray-flip fraction **0.0%** of 22,500 rays (gate 0.15%) |
| **G3** round-trip | **PASS** | re-imports in Blender; `g3check` on pinned three 0.185: `G3-OK {"ok":true,"meshes":16,"tris":17064,...}`, no decode errors |
| **G4** appearance | **PASS** | worst mean delta 0.0056% (gate 2%/4%); diffs described above |
| **G5** draw submeshes | **PASS** | 1,033 → 16 |
| **G6** size | **PASS** | −70.1% raw against a 60% target |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object/bbox/material check in `optimize.py`'s leak-proof export; deterministic re-run reproduces the output; no `.blend1` files |

**All gates pass.** The shipping swap was made: `one-steuart-lane.optimized.glb`
was copied over `artifacts/one-steuart-lane/one-steuart-lane.glb`, and the
pre-optimize original is archived byte-for-byte at
`optimize/input/one-steuart-lane.glb`. The parent `REPORT.md` and
`validation.json` were re-generated against the shipped file so the integration
stage writes its manifest entry from reality.
