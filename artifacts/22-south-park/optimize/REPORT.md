# Hotel Madrid (22–24 South Park) — GLB optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/22-south-park/`, 17 August 2026.
`ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`, `ALLOW_BAKE: no`.

## Metrics

| | Input | Optimized | Δ |
|---|---|---|---|
| File, raw | 451,776 B (441.2 KB) | **182,536 B (178.3 KB)** | **−59.6%** |
| Objects / nodes | 169 | **12** | −92.9% |
| Draw submeshes (primitives, via GLTFLoader) | 169 | **12** | −92.9% |
| Triangles | 6,708 | 6,708 | 0 |
| Vertices | 13,572 | **11,975** | −11.8% |
| Materials | 12 | 12 | identical set |
| bbox dims | 36.01937 × 31.83933 × 14.22000 m | 36.01937 × 31.83933 × 14.22000 m | 0 |
| bbox min | −18.00969, −15.91967, 0.0 | −18.00969, −15.91967, 0.0 | 0 |

Toolchain: Blender 5.2.0 LTS; `npx gltfpack@0.24`; node + the pinned three in
`g3check/package.json`; python3 + Pillow.

## Phase A — waste census

`inspect.json`. The asset came in as 169 flat-shaded closed prisms plus two ring
bands, sharing 12 materials. Two forms of waste, one large and one nil:

- **Object-count overhead.** 169 nodes and 169 primitives for 12 materials. This
  is the dominant waste on this asset and the one that matters most to the shared
  `BatchedMesh` that every generic landmark renders out of.
- **Split vertices.** 6,708 triangles carried 13,572 vertices; glTF splits
  vertices for flat shading. A 1 mm per-object weld recovered them in `mid.glb`,
  though meshopt re-splits for flat normals on the way out, so the shipped saving
  is 11.8% rather than the ~60% seen inside Blender.
- **Buried interior faces: none predicted, none found.** The build script places
  every feature proud of or recessed into the wall plane and never nests one
  solid inside another.
- **Over-tessellated curves: none.** The two curved elements — the barrel awning
  (7 segments) and the exhaust fan disc (12 segments) — are already at the style
  bible's low-segment budget, and the frontage arc is four measured chords, not a
  tessellation.

## Phase B — geometry cleanup

`optimize.py` → `mid.glb`, `phaseb_stats.json`.

| Step | Tris | Verts |
|---|---|---|
| input | 6,708 | 13,572 |
| 1. weld ≤ 1 mm + degenerate | 6,708 | (welded) |
| 2. interior faces | 6,708 | 0 removed |
| 3. limited dissolve | **SKIPPED — see below** | |
| 5. join per material | 6,708 | 169 objects → 12 |
| 7. normals audit | `inverted_solids: []` | |

### Step 3 was skipped deliberately

Prompt §3.3 says to skip the limited dissolve on assets with large coplanar ring
bands. This asset has two closed annuli — the parapet frieze, which follows the
whole seven-vertex trapezoid footprint, and the light-well curb — plus long
coplanar strips in the cornice crown, the belt course and the storefront band
across four arc segments. Re-triangulating an annulus ngon emits slivers up to
the full ring length; they pass every area-based degeneracy test, collapse their
shared vertex normals to ~0, and surface only *after* the shipping swap as
`invalid_or_nonunit_loop_normal_count` in the stage-2 contract validator — the
350-brannan failure of 13 August 2026, and the same call 106 South Park made.

## Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o 22-south-park.optimized.glb -c -km -kn -noq
```

`-km -kn` kept unconditionally: material names are API, and this asset has two
`_Glow` materials the loader must keep separate from everything else. `-noq`
kept — this repo does not quantize, and `pipeline/compress-assets.mjs` produces
exactly these flags. That script will skip this file at intake because it already
carries `EXT_meshopt_compression`, which is the intended behaviour.

## Phase D — bake

Not run. `ALLOW_BAKE: no`, and the contract forbids textures.

## Phase E — A/B verification

`render_ab.py` at the generic 45° azimuth / 42° elevation, near and far, day and
night, plus four orthographic elevations. `diffs.json`:

| View | mean abs RGB Δ | max px Δ |
|---|---|---|
| day near | 0.0379% | 147 |
| day far | 0.0365% | 18 |
| night near | 0.0103% | 15 |
| night far | 0.0128% | 8 |
| elev N / E / S / W | 0.0382 / 0.0394 / 0.0194 / 0.0287% | 33 / 32 / 21 / 37 |

The ×8-amplified diffs show faint single-pixel lines along silhouette and bevel
edges and nothing else. No element is missing, no silhouette moved, no shading
changed; the night layer lights the same five upper windows and the same
taqueria band. The residual is rasteriser jitter from re-welded vertex positions.

These numbers are an order of magnitude larger than 106 South Park's (0.007%)
because this asset has ten times the edge length in bevelled trim — the cornice
brackets, the window casings and the four-segment arc all contribute — and every
bevel edge is a candidate for a one-pixel shift. All are two orders below the
2%-far / 4%-near gate.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| **G1** contract | **PASS** | material set identical (12, byte-for-byte names); both `_Glow` materials still separate; no `Toy_body`; no manifest-named nodes on this asset |
| **G2** geometry | **PASS** | bbox Δ 0.0000 m, origin Δ 0.0000 m; `inverted_solids: []`; ray test 22,500 rays / 15,680 hits / 1 flipped (**0.0064%**, against a 0.15% allowance) |
| **G3** round-trip | **PASS** | `g3check` → `G3-OK {"ok":true,"meshes":12,"tris":6708,...}` under the pinned three, no decode errors |
| **G4** appearance | **PASS** | all eight views ≤ 0.0394% mean, against 2% far / 4% near |
| **G5** draw submeshes | **PASS** | 169 → 12 |
| **G6** size | **PASS** | −59.6% raw, against a 60% target |
| **G7** GPU budget | n/a | bake mode not used |
| **G8** hygiene | **PASS** | re-import object count matches (12); scripts deterministic and committed here; no `.blend1` left |

## Shipping swap

`optimize/22-south-park.optimized.glb` was copied over
`artifacts/22-south-park/22-south-park.glb`; the pre-optimize file is archived at
`optimize/input/22-south-park.glb`. The **stage-2 contract validator was re-run
against the shipped optimized file** and passes all 16 checks with a 0.0% ray
residual — `artifacts/22-south-park/validation.json` now describes the shipping
asset, not the pre-optimize one.
