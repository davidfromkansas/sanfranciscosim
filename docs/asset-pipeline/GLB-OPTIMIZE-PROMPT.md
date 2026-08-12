# GLB Optimize — shrink-pass prompt (v2, in-repo)

Stage 4 of the address-to-asset pipeline (`ADDRESS-TO-ASSET.md`), also runnable
standalone. Input: a finished, approved asset at `artifacts/<slug>/`. Output: a
byte-lean GLB that looks identical in the app and becomes the shipping file.

Every GLB under `app/public/sf-assets/` is expected to be meshopt-compressed on
intake — the loaders register `MeshoptDecoder` (`app/src/gltf.js`,
`app/src/assets.js`). This document is the intake compression procedure.

**Reference implementation:** `tools/glb-optimize/` holds generic, proven
scripts — `inspect.py`, `optimize.py`, `validate.py`, `render_ab.py`,
`diff_ab.py`, and `g3check/` (a pinned-three GLTFLoader round-trip test). Copy
them into the asset's `optimize/` dir and adapt the per-asset constants
(dims-plausibility ranges, silhouette exceptions) rather than writing from
scratch. Results achieved with them: st-marys-cathedral 257→42 KB (49→9 draw
submeshes), salesforce-tower 924→156 KB, war-memorial-opera-house 549→99 KB,
one-rincon-hill 733→124 KB.

---

## 0. Inputs

| Parameter | Default | Notes |
|---|---|---|
| `ASSET_DIR` | `artifacts/<slug>/` | Must contain exactly one shipping `.glb` (basename = slug). Its `REPORT.md`/`validation.json` document intended dims, tris, and glow design — read them and use them to sharpen Gate G2. |
| `OUTPUT_DIR` | `ASSET_DIR/optimize/` | Scripts, stats, renders, report land here. |
| `ASSET_CLASS` | `landmark` | Or `kit` / `streetkit` / `vehicle` / `flora` — sets contract rules and §7 camera distances. |
| `TARGET_REDUCTION` | 60% file size | Aspirational — see Gate G6. |
| `ALLOW_MESHOPT` | `yes` | The app registers MeshoptDecoder. Before relying on it, verify: `grep -rn setMeshoptDecoder app/src/` must hit. If it doesn't, use quantization-only mode. |
| `ALLOW_BAKE` | `no` | Destructive high→low texture bake (§5). Off unless explicitly requested — the contract forbids textures without a recorded exception. |
| `BLENDER` | Blender 4.5+/5.x on PATH or `/Applications/Blender.app/Contents/MacOS/Blender` | Headless: `"$BLENDER" -b --python script.py -- <args>`. Blender 5.x: `surface_render_method`, not `blend_method`. |

Copy the input GLB byte-for-byte to `OUTPUT_DIR/input/<slug>.glb`, verify the
byte size matches, and run everything against the copy. Never modify the
original in place; the shipping swap happens only after all gates pass (§9).

All steps are **deterministic scripts** committed in `OUTPUT_DIR` — re-running
them on the input must reproduce the output.

## 1. Hard invariants — the asset contract (NEVER violate)

1. **Material names are API.** The loader splits `*_Glow` materials into the
   unlit night layer (`opacity = 0.12 + 0.95·uNight`) and merges the rest.
   Output material-name set must equal the input's. Glow-ness is name-only —
   two materials with identical parameters but different names must stay
   separate (see the `-km` rule in §4).
2. **`Toy_body` stays independently addressable** (kit pieces only — per-instance tinting).
3. **Transform contract unchanged**: base-center origin on z=0, true-world
   orientation, real meters. Output bbox dims within max(1 cm, 0.1%) of input;
   origin offset within 1 cm. (Vehicles: front −Z, origin centered.)
4. **No textures added** unless `ALLOW_BAKE=yes`.
5. **Silhouette is sacred** at the app's high three-quarter aerial camera.
   Facade-plane micro-detail is negotiable only under §5.
6. **Node names referenced by manifests stay intact.**
7. **Leak-proof export**: temp scene + `use_active_scene=True` +
   `export_apply=True`; re-import and verify object count / bbox / materials.
   Wrap exporter calls in `contextlib.redirect_stdout`.

## 2. Phase A — Forensic inspection

Run `inspect.py` against the input; record in the report: raw AND gzipped
bytes, objects, tris, verts, per-object top-20 table, material list with glow
flags, primitive count, vertex attributes, bbox/origin. Cross-check against
the asset's own `validation.json`.

Then the **waste census** (drives Phase B): duplicate meshes, buried interior
faces, degenerate faces, unwelded coincident verts, over-tessellated curves
(chord error < 1 screen pixel at §7 near distance), object-count overhead
(objects sharing a material that could join). Write a per-technique plan with
predicted savings before executing.

## 3. Phase B — Lossless & near-lossless geometry cleanup (always on)

`optimize.py` implements this order; measure tri/vert deltas per step:

1. **Weld** coincident verts ≤ 1 mm, per object only (glow shells are separate
   objects; per-object weld can never fuse glow onto base surfaces).
2. **Delete degenerate faces**; delete interior faces provably buried inside
   another solid. **Occluder rule (hard-learned):** only treat a mesh as an
   occluder if it is a CLOSED solid — signed volume of an open shell is
   meaningless and lets it masquerade as a box that "hides" real faces. No
   boolean unions as a shortcut.
3. **Limited dissolve at 0.05°** (strictly coplanar), delimit by material +
   sharp. NOT 0.5°: dissolve merges transitively, and on curved shells a
   0.5° chain accumulates twisted ngons that re-triangulate with flipped
   windings. Savings at 0.05° are nearly identical.
4. **Retessellate over-segmented curves** (halve segments while chord error
   < 1 px at near distance). Skip silhouette-defining curved shells — note
   the skip in the report.
5. **Join objects per material** — except manifest-named nodes and `Toy_body`.
   Usually the single biggest win (node/accessor overhead + draw submeshes).
6. **Instance vs join** for repeated geometry: join small counts, share mesh
   data for large counts of heavy repeats; justify per case.
7. **Normals audit**: per-object signed volume positive (closed meshes only —
   see step 2's rule); ray-test residual ≤ 0.15% documented as
   `flipped_fraction` in `validation.json`, `inverted_solids: []`.

## 4. Phase C — Packing pass (always on)

```
npx gltfpack@0.24 -i mid.glb -o out.glb -c -km -kn -noq
```

- **`-km` is mandatory**, not optional: without it gltfpack merges
  identical-parameter materials ACROSS the `_Glow` boundary (glow-ness is
  name-only), silently killing the night layer. Always keep `-kn -km`.
- **`-noq` is also mandatory for this repo — do NOT quantize.** The recipe above
  originally read `-cc -kn -km`, which quantizes by default. That conflicts with
  `pipeline/compress-assets.mjs` (the mandatory ship step per `sf-asset-check` §8),
  which runs `-c -km -kn -noq` because the runtime kit/landmark merge needs float32
  attributes, and with `sf-asset-check`'s warning that quantization "silently breaks
  the app's merge paths (every piece falls back to procedural and the city looks
  fine)". A quantized build also fails the stage-2 contract validator on
  `transforms_applied` and `no_unexpected_objects`, because gltfpack stores the
  dequantize matrix as a node transform and splits each node into an empty parent
  plus a `Mesh_N` child. Every shipped landmark except `st-marys-cathedral` is
  unquantized. Use:

  ```
  npx gltfpack@0.24 -i mid.glb -o out.glb -c -km -kn -noq
  ```

  Expect a smaller headline win than the numbers quoted above — those were measured
  with quantization on. Recorded 12 Aug 2026 while optimizing `380-brannan`
  (see `artifacts/380-brannan/optimize/REPORT.md` §4). **`st-marys-cathedral.glb` is
  quantized and may be falling back to procedural in production — worth one console
  check.**
- `ALLOW_MESHOPT=no` fallback: drop `-c` only.
- Verify on the output, never trust flags: material name set, manifest node
  names, re-imported bbox within tolerance.
- Record raw + gzipped bytes and estimated GPU vertex-buffer bytes
  (quantization ≈ −60% GPU vertex memory even when file delta is modest).

## 5. Phase D — High→low bake (ONLY if `ALLOW_BAKE=yes`)

Partition silhouette (keep) vs facade shading (bakeable: bevels, window
insets, trim relief). Low mesh must cut bakeable-region tris ≥ 3× or abort the
phase. Bake tangent normal + AO (512², 1024² only above ~150 m long axis) from
the ORIGINAL pre-Phase-B mesh. Colors stay materials — never bake albedo;
`_Glow` excluded entirely. Compress KTX2 (`-tc`; UASTC for normal maps, never
ETC1S). Gate G7 checks total GPU bytes. Flag the contract exception in the
report. When in doubt: don't.

## 6. Optional micro-passes

AO→vertex-colors only if the app material path multiplies vertex colors for
this asset class (check `app/src/assets.js` first). Prune unused data (shape
keys, UV layers, custom normals on flat shading, loose geometry).

## 7. Phase E — A/B verification renders (always on)

`render_ab.py` + `diff_ab.py`: input vs output, same rig, day (glow alpha
0.12 — mimics the day pass) AND night (alpha 1.0, emission ≈ 6, dusk world),
each at near and far:

| Class | Near | Far |
|---|---|---|
| landmark | 1.5× long-axis | 6× long-axis |
| kit / streetkit | 80 m | 400 m |
| vehicle | 15 m | 120 m |
| flora | 30 m | 300 m |

**Set `cam.data.clip_end = 50000`** — far views of tall landmarks exceed the
1 km default and render empty. Plus a 4-elevation contact sheet. Compute mean
absolute RGB delta ignoring background; then LOOK at the diffs and describe
any visible change honestly.

## 8. Acceptance gates (all must pass; any FAIL ⇒ keep original, report why)

- **G1 Contract**: material set identical; `_Glow` separate; `Toy_body`
  separate; manifest node names intact.
- **G2 Geometry**: bbox within max(1 cm, 0.1%); origin within 1 cm; signed
  volumes positive (closed meshes); flipped fraction ≤ 0.15%.
- **G3 Round-trip**: re-imports in Blender AND loads via `g3check/`
  (`npm install && node check.mjs <glb>` — pinned three, asserts submesh
  count, no decode errors, only the extensions the mode allows).
- **G4 Appearance**: day+night × near+far — no missing elements, no
  silhouette change, no shading artifacts; mean delta ≤ 2% far / ≤ 4% near;
  written description contains nothing a player would notice.
- **G5 Draw submeshes**: ≤ input count.
- **G6 Size**: reduced; if < TARGET_REDUCTION, the waste census must show the
  remainder is silhouette geometry.
- **G7 GPU budget** (bake mode only): total GPU bytes strictly reduced.
- **G8 Hygiene**: no foreign geometry (re-import count check); deterministic
  re-run reproduces output; no `.blend1` files left.

## 9. Deliverables & the shipping swap

```
artifacts/<slug>/optimize/
  input/<slug>.glb          # untouched archive of the pre-optimize asset
  <slug>.optimized.glb      # the winner
  inspect.py optimize.py validate.py render_ab.py diff_ab.py   # adapted copies
  inspect.json phaseb_stats.json diffs.json validation.json
  renders/                  # A/B day/night near/far + contact sheet + diffs
  REPORT.md                 # metrics table (raw/gzip bytes, tris, verts,
                            # submeshes, GPU bytes, pixel deltas), census,
                            # per-phase savings, judgment calls, gate results
```

Only after ALL gates pass: copy `<slug>.optimized.glb` over
`artifacts/<slug>/<slug>.glb` (the shipping file integration will pick up).
The pre-optimize original stays archived at `optimize/input/<slug>.glb`.
Update `validation.json`/`REPORT.md` tri and byte counts to the shipped
numbers so the integration stage's manifest entry is written from reality.

## 10. Toolchain & preflight

Blender (headless), `npx gltfpack@<pinned>`, node + the pinned three in
`tools/glb-optimize/g3check/package.json`, python3 + Pillow, gzip. Record all
versions in REPORT.md. Pin npx versions explicitly. If a tool is unreachable,
stop and report — no substitutions without documenting them.

## 11. Failure & rollback

Phases are independent: revert any phase that regresses bytes or Gate G4 and
keep the rest. Never ship with a failed gate. When this document conflicts
with observed app behavior, the app wins — record the conflict and update
this document in the same change.
