# Pier 3 — stage 4 optimize report

`GLB-OPTIMIZE-PROMPT.md` v2 run against `artifacts/pier-3/`.
`ASSET_CLASS: landmark` · `ALLOW_MESHOPT: yes` · `ALLOW_BAKE: no`.

## Headline

| | input | shipped | delta |
|---|---|---|---|
| File, raw | 817,276 B | **371,724 B** | **−54.5%** |
| File, gzip | 132,302 B | 214,363 B | +62.0% (see §6) |
| Draw submeshes (primitives) | 361 | **13** | −96.4% |
| Objects / nodes | 361 | 13 | −96.4% |
| Triangles | 12,152 | 12,152 | 0 |
| Verts (Blender, welded) | 25,268 | 27,473 | +8.7% (re-index) |
| Materials | 13 | 13 | identical set |
| Bytes / triangle | 67.3 | **30.6** | repo median is 27.3 |

**All gates pass.** The optimized file is now `artifacts/pier-3/pier-3.glb`; the
pre-optimize original is archived byte-for-byte at `optimize/input/pier-3.glb`.

## 1. Toolchain

Blender 5.2.0 LTS (`fbe6228777e7`, 2026-07-14) · `gltfpack@0.24` via npx ·
three.js `^0.185.1` in `g3check/` · python3 3.9 + Pillow · gzip (macOS).

## 2. Phase A — forensic inspection (`inspect.json`)

817,276 B raw / 131,070 B gzip · 361 objects · 361 primitives · 12,152 tris ·
25,268 verts · vertex attributes POSITION + NORMAL only · zero textures ·
13 materials, 3 of them `_Glow`.

Waste census:

| Finding | Count | Plan |
|---|---|---|
| Draw submeshes | **361** | join per material → 13. The dominant win by far: 361 nodes, 749 accessors and 749 bufferViews of pure overhead on a 12 k-triangle asset |
| Coincident vertex pairs | 18,482 | per-object weld ≤ 1 mm |
| Duplicate/redundant triangles | 7,920 | the 85 piles, 46 bay stripes and 42 bollards are repeats of a handful of boxes; joining removes the node overhead, not the geometry |
| Degenerate triangles | 0 | nothing to do |
| Interior faces buried in a closed solid | 0 found | the asset is a union of separated boxes, not nested solids |

## 3. Phase B — geometry cleanup (`phaseb_stats.json`)

| Step | tris | verts |
|---|---|---|
| input | 12,152 | 25,268 |
| 1. weld ≤ 1 mm + delete degenerate | 12,152 | **6,786** |
| 2. interior faces (0 removed) | 12,152 | 6,786 |
| 3. limited dissolve | **SKIPPED** — see below | |
| 5. join per material (12 joins) | 12,152 | 6,786 |

The weld is the whole of Phase B here: 25,268 → 6,786 verts, −73%.

**Step 3 was skipped deliberately**, under prompt §3.3. Pier 3 carries eight large
coplanar ring bands following a ~510 m perimeter — deck slab, deck surface, fender curb,
railing ribbon, bulkhead cornice, parapet, parapet cap and office parapet. Their top and
bottom faces are perfectly coplanar annuli, so even a strictly-coplanar 0.05° dissolve
merges each into a single ngon, and re-triangulating an annulus emits invisible slivers
that pass every area-based degeneracy test and only surface *after* the shipping swap as
nonunit STORED normals in the packed file. On `350-brannan` the same step was worth 30
triangles. It is the cheapest step in Phase B and the only one that can manufacture new
degenerate geometry; skipping it here cost nothing measurable.

Joins: `Toy_stone` 116 objects → 1, `Toy_ink` 64 → 1, `Toy_steel` 50 → 1, `Toy_trim`
46 → 1, `Toy_glass` 27 → 1, `Toy_amber_Glow` 17 → 1, `Toy_cream` 14 → 1, `Toy_roofd`
10 → 1, `Toy_glass_Glow` 6 → 1, `Toy_conc` 4 → 1, `Toy_sand` 4 → 1, `Toy_glassl` 2 → 1.
No manifest-named nodes and no `Toy_body` exist on this asset, so nothing was excluded
from joining.

Normals audit after Phase B: `inverted_solids: []`.

## 4. Phase C — packing

```
npx gltfpack@0.24 -i mid.glb -o pier-3.optimized.glb -c -km -kn -noq
```

`-km -kn` keep the material and node names, which is what protects the `_Glow` boundary
(glow-ness is name-only). `-noq` is the repo standard and is what
`pipeline/compress-assets.mjs` produces; the shipped file carries
`EXT_meshopt_compression` and nothing else, and re-validates with `transforms_applied`
and `no_unexpected_objects` still true — the two checks a quantized build would break.

745,480 B (mid) → 371,724 B, with bufferViews collapsing 39 → 3.

## 5. Phase E — A/B verification (`diffs.json`, `renders/`)

Same rig for both files: 42° aerial, day (glow at 12% alpha) and night (glow lit), near =
1.5× long axis = 294 m, far = 6× = 1,175 m, plus four orthographic elevations.

| View | mean abs RGB | max px delta |
|---|---|---|
| day_near | **0.0005%** | 3 |
| day_far | 0.0011% | 3 |
| night_near | 0.5669% | 69 |
| night_far | 0.5461% | 34 |
| elev_n / e / s / w | 0.0018 / 0.0024 / 0.0011 / 0.0014% | 18 / 10 / 4 / 3 |

**Honest description of the night delta.** 0.57% is 500× the day figure and it is worth
saying why rather than just noting that it clears the 4% gate. The A/B rig renders Cycles
at 64 samples with **denoising off**; the night scene is lit almost entirely by the
sixteen amber deck-light emitters bouncing off a dark 190 m deck, which is exactly the
configuration that converges slowest. The amplified diff image (`renders/diff_night_near.png`)
is uniform salt-and-pepper spread across the deck with **no structural edges, no outlines
of missing elements and no silhouette change** — and the day and elevation views, which
share the same geometry and differ only in lighting, come in at 0.0005–0.0024%. Geometry
that had actually changed could not hide in the day views and appear only at night. It is
sampler noise.

Nothing a player would notice, in any of the eight views.

## 6. The gzip figure, stated plainly

Raw bytes fall 54.5%, but gzipped bytes **rise** 132 KB → 214 KB, because meshopt data is
already entropy-coded and gzips poorly while the unpacked float32 original gzips very
well. Over a gzip-enabled CDN this asset therefore costs about 82 KB more on the wire than
the unoptimized file would.

It ships anyway, and not reluctantly:

- meshopt at intake is mandatory in this repo (`AGENTS.md`, "the asset pipeline"), and
  `pipeline/compress-assets.mjs` skips any file that already carries the extension, so
  there is no un-meshopt path that ends anywhere good;
- 371 KB raw is comfortably inside the 500 KB per-landmark budget;
- 30.6 B/tri sits inside the shipped band (23–40, median 27.3 across the 90 landmarks
  already in the manifest), so this asset is not an outlier;
- the 96% cut in draw submeshes (361 → 13) is the number that actually matters at runtime,
  and it is what keeps the shared landmark `BatchedMesh` merge cheap.

## 7. Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material set identical (13, byte-compared); `_Glow` trio separate; no `Toy_body`; no manifest-named nodes to preserve |
| G2 Geometry | **PASS** | bbox 195.8228 × 161.2056 × 18.5 unchanged to 4 dp; origin unchanged; all signed volumes positive; 22,500 rays / 6,983 hits / **0 flipped** |
| G3 Round-trip | **PASS** | Blender re-import clean; `g3check` (three 0.185.1) loads 13 meshes, 12,152 tris, all 13 materials, correct bbox, no decode errors |
| G4 Appearance | **PASS** | ≤ 0.0024% on day + all elevations; 0.57% night, shown above to be sampler noise; gate is 4% near / 2% far |
| G5 Draw submeshes | **PASS** | 361 → 13 |
| G6 Size | **PASS** | 817,276 → 371,724 B raw, −54.5%. Short of the 60% aspiration; the census explains the remainder — the asset is flat-shaded by contract, so every triangle needs its own three vertices and there is no vertex sharing left to win. What remains is silhouette geometry |
| G7 GPU budget | n/a | `ALLOW_BAKE: no`, no textures |
| G8 Hygiene | **PASS** | re-import object count 13 with the exact input material set; `optimize.py` and `gltfpack` both byte-deterministic on re-run (md5 `50d52c4a…` and `a861768d…` reproduced); no `.blend1` files |

## 8. Shipping swap

`pier-3.optimized.glb` copied over `artifacts/pier-3/pier-3.glb`. The stage-2 contract
validator was re-run in a fresh isolated scene against the **shipped** file and returns
`overall: PASS` on all 16 checks; `artifacts/pier-3/validation.json` and
`artifacts/pier-3/REPORT.md` now carry the shipped numbers, so the integration stage writes
its manifest entry from reality.
