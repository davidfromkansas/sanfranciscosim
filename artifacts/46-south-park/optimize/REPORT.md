# 44–46 South Park — optimize pass (stage 4)

`docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` run against
`artifacts/46-south-park/`, 17 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

**Outcome: all gates PASS. The optimized file is now the shipping asset.**

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 279,332 B (272.8 KB) | **124,584 B (121.7 KB)** | **−55.4%** |
| File, gzip -9 | 45,963 B (44.9 KB) | 87,807 B (85.7 KB) | **+91.0%** — see §G6 |
| Objects / nodes | 71 | **10** | −85.9% |
| Draw submeshes (primitives, via GLTFLoader) | 73 | **11** | −84.9% |
| Triangles | 4,532 | 4,505 (Blender re-import) / 4,532 (GLTFLoader) | −0.6% / 0 |
| Vertices | 9,324 | **7,800** | −16.3% |
| Materials | 10 | 10 | identical set |
| bbox dims | 27.9295 × 27.6198 × 16.1500 m | 27.9295 × 27.6198 × 16.1500 m | 0 |
| bbox min | −13.9648, −13.8099, 0.0 | −13.9648, −13.8099, 0.0 | 0 |
| XY origin offset | 0.0000, 0.0000 | 0.0000, 0.0000 | 0 |

Toolchain: Blender 5.2.0 LTS; `npx gltfpack@0.24`; node + the pinned
`three@0.185.1` in `g3check/`; python3 + Pillow; gzip -9.

## Phase A — waste census (`inspect.json`)

| Finding | Count | Plan |
|---|---|---|
| coincident vertex pairs | 6,916 | weld ≤ 1 mm, per object (Phase B.1) |
| duplicate mesh groups | 15 groups, 1,588 redundant tris | joined per material (Phase B.5); no shared-mesh instancing — the repeats are 3 fans, 2 vents and 7 PV scoring bands, all small |
| degenerate triangles | 0 | nothing to do |
| interior faces buried in closed solids | 0 found | nothing to do |
| objects sharing a material | 71 objects over 8 material groups | join per material — the biggest win here |
| over-tessellated curves | five 10-segment cylinders; 1 px = 0.0282 m at the 41.9 m near distance, chord error 0.0196 m | **left alone** — under the 1 px threshold, but only by 30%, and these are the roof's only round forms |
| textures | none | n/a |

Predicted savings before executing: vertices −70% (weld), nodes/submeshes −85%
(join), triangles ~0. Actual: vertices −74% at the Blender stage (9,324 →
2,408), submeshes −85%, triangles 0. The gltfpack stage re-expands vertices to
7,800 because meshopt splits shared vertices per attribute stream; that is
expected and is not a regression in GPU cost.

## Phase B — geometry cleanup (`optimize.py`, `phaseb_stats.json`)

| Step | Triangles | Vertices |
|---|---|---|
| input | 4,532 | 9,324 |
| 1. weld ≤ 1 mm + degenerate removal | 4,532 | 2,408 |
| 2. interior faces (0 removed) | 4,532 | 2,408 |
| 3. limited dissolve, 0.05° coplanar | 4,532 | 2,408 |
| 4. curve retessellation — skipped | — | — |
| 5. join per material (71 → 10 objects) | 4,532 | 2,408 |

**The limited dissolve was run, not skipped.** §3.3 of the prompt says to skip it
on assets with large coplanar *ring bands* — closed annuli that follow the whole
footprint, whose re-triangulation emits metre-long slivers (precedent:
`350-brannan`). This asset has none: every parapet, screen and band is an
independent four-sided prism, not a `rim()` annulus, so there is no annulus ngon
for a dissolve to create. It returned 0 triangles anyway, and the post-swap
stage-2 validator — the only place the sliver failure ever shows up, because
gltfpack re-emits stored normals — reports
`invalid_or_nonunit_loop_normal_count: 0`.

**Curve retessellation skipped.** The five cylinders (three roof fans, two rear
vents) are 10-segment at 0.6–0.8 m diameter. Halving to 5 segments would keep
chord error under one screen pixel at the near distance by a 30% margin, and
would save roughly 500 triangles — but they are the only round forms on an
otherwise entirely rectilinear asset, a pentagon reads as a pentagon in
silhouette against a flat roof, and the asset is 4.5k triangles against a 6k plan
cap and a 30k contract cap. Not worth the silhouette risk. Noted per §3.4.

Normals audit after Phase B: all 10 joined solids positive signed volume,
`inverted_solids: []`.

## Phase C — packing (`gltfpack@0.24 -c -km -kn -noq`)

`-km` and `-kn` keep the material and node names, which are API here: the loader
splits `*_Glow` by **name**, and without `-km` gltfpack would merge
`Toy_trim_Glow` into `Toy_trim` (identical parameters, different name) and
silently kill the night layer. `-noq` is the repo standard — quantization breaks
the kit merge path and fails the stage-2 contract validator on
`transforms_applied` / `no_unexpected_objects`. Verified on the output rather
than trusted: material name set identical, 11 primitives, bbox unchanged.

## Phase D — high→low bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification (`renders/`, `diffs.json`)

Landmark camera distances: near = 1.5 × long axis = 41.9 m, far = 6 × = 167.6 m.
Day (glow alpha 0.12) and night (alpha 1.0, emission ≈ 6, dusk world) at both,
plus four orthographic elevations.

| View | mean abs RGB Δ | max px Δ | gate |
|---|---|---|---|
| day near | **0.027%** | 148 | ≤ 4% |
| day far | **0.023%** | 19 | ≤ 2% |
| night near | **0.008%** | 10 | ≤ 4% |
| night far | **0.008%** | 15 | ≤ 2% |
| elevation N | 0.023% | 151 | — |
| elevation E | 0.068% | 163 | — |
| elevation S | 0.079% | 131 | — |
| elevation W | 0.025% | 64 | — |

**Looked at, not just measured.** At ×8 amplification the diffs are a scatter of
single-pixel edge noise along silhouette boundaries and along the mullion and
window-frame edges — antialiasing sampling differences, not geometry. Nothing is
missing: the window grid, the frosted band, the purple entry and awning, the
solar array, the skylight, the mechanical cluster, the rear openings and the
step down to the rear block are all present and identically placed in both. The
night state lights the same surfaces at the same intensity in both — the
ground-floor hero band and four upper panes. The three highest max-pixel numbers
are all on high-contrast edges (the dark screen band against sky, the white
mullions against navy glass) and are one-pixel wide.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (10, including both `_Glow`); no `Toy_body`; no manifest-named nodes on this asset |
| **G2** geometry | **PASS** | bbox identical to 4 dp; origin offset 0.0000, 0.0000; all signed volumes positive; ray test 22,500 rays / 14,546 hits / **0 flipped** |
| **G3** round-trip | **PASS** | Blender re-import 10 objects; `g3check` `G3-OK`, 11 meshes, 10 materials, bbox matches |
| **G4** appearance | **PASS** | max mean Δ 0.079%, gates are 2% / 4%; visual description above |
| **G5** draw submeshes | **PASS** | 73 → 11 |
| **G6** size | **PASS on raw, qualified on gzip** | −55.4% raw; +91.0% gzipped — see below |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object count matches (10); scripts deterministic and committed here; no `.blend1` left |

### G6 — the gzip number, honestly

Raw bytes fell 55%, gzipped bytes rose 91%. Both are real. Meshopt output is
already entropy-coded so it does not gzip further, while the pre-optimize file
was plain glTF buffers that gzip compressed 6:1. **Over the wire the
un-optimized file would have been about 42 KB smaller.**

Shipping the optimized file anyway, for the reasons 165 and 106 South Park
already recorded:

1. Meshopt compression is the **mandatory intake step** for everything entering
   `app/public/sf-assets/` (`AGENTS.md`, asset pipeline §Ship step;
   `pipeline/compress-assets.mjs`). It is not an optional trade — an
   un-meshopted file would simply be compressed at ship time anyway.
2. The **structural wins are the ones that matter**: 73 → 11 draw submeshes and
   71 → 10 nodes both feed the shared `BatchedMesh` that every generic landmark
   renders out of. 42 KB over the wire does not, on an asset that is 122 KB
   against a 500 KB budget.
3. One encoding across all assets is worth more than the bytes.

## Shipping swap

`46-south-park.optimized.glb` copied over
`artifacts/46-south-park/46-south-park.glb`. The pre-optimize original is
archived byte-for-byte at `optimize/input/46-south-park.glb`.

`artifacts/46-south-park/validation.json` and `REPORT.md` were regenerated
against the **shipped** file, so the integration stage writes its manifest entry
from reality: **4,505 triangles, 124,584 bytes, 10 objects**, dims and crest
unchanged. The post-swap stage-2 contract validation is **16 / 16 PASS** — which
is also the check that would have caught a dissolve-manufactured sliver, and did
not.
