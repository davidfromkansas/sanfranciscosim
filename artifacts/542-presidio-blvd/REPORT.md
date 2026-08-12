# 542 Presidio Boulevard — build report

Miniature GLB of the 1912–17 Mission Revival officers' family duplex at 542 Presidio
Boulevard, for the SF toy-diorama city. Built 12 August 2026 by running
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` from `BUILDING: 542 Presidio Blvd, San
Francisco, CA 94129`.

Research and sources: `REFERENCE.md`. Plan: `docs/asset-plans/542-presidio-blvd.md`.
Where this report and the plan disagree, **this report wins** — it records what was
actually verified and built.

## Shipped numbers

| | |
|---|---|
| File | `542-presidio-blvd.glb` |
| Triangles | **3,092** (budget 8,000; landmark ceiling 27,000) |
| Vertices | 1,698 after weld |
| Objects / draw submeshes | **8** (one per material, joined in stage 4) |
| Dimensions (AABB) | 23.608 × 25.455 × **10.600** m |
| Min Z | 0.0 | 
| XY centre offset | 0.00, 0.00 m |
| Loader scale at `targetHeightM` 10.6 | **1.00000** |
| Materials | 8, all `Toy_*`, no textures, no transparency |
| Glow materials | 2 — `Toy_glass_Glow`, `Toy_white_Glow` |
| File size | 84,960 B raw / 56,873 B gzip (post-optimize; see §Stage 4) |
| Contract validation | **PASS** (16/16 checks) |

The AABB is larger than the 19.2 × 13.8 m building because the asset is authored at
its true 31° heading, so the axis-aligned box circumscribes a rotated rectangle. That
is correct, not a defect.

## Toolchain

| Tool | Version | Note |
|---|---|---|
| Blender | **5.2.0 LTS** (`fbe6228777e7`, 2026-07-14) | at `/Applications/Blender.app/Contents/MacOS/Blender`. The plan's Part 1 names Blender 4.5 LTS at `/opt/blender` — that is the Devin container. Built locally on David's machine instead; recorded as a deviation. Blender 5.x uses `surface_render_method`, not `blend_method`. |
| gltfpack | 0.24 (`npx gltfpack@0.24`) | flags `-c -km -kn -noq` |
| Python | 3 + Pillow | contact sheet |

## Scripts (deterministic; re-running reproduces the asset)

- `build_542_presidio_blvd.py` — the model
- `render_542_presidio_blvd.py` — the review rig (`--only aerial|night` for single passes)
- `validate_542_presidio_blvd.py` — fresh-scene contract validation → `validation.json`
- `make_contact_sheet.py` — the contact sheet
- `optimize/` — stage 4 (see below)

## Corrections to the plan's dossier

The plan is a head start, not a citation. Seven things changed while building; the
first four came out of reviewing the high three-quarter aerial before running the
formal rig, which is what the stage-2 override asks for.

1. **Eave overhang 0.9 m → 0.65 m.** The plan exaggerated to 0.9 m. In the first
   aerial that swamped the walls — the asset read as a roof with a sliver of building
   under it. 0.65 m keeps the shadow line that makes the roof legible without eating
   the two-storey proportion the elevation research established.
2. **Roof pitch is 4:12 (18.4°), measured from the eave edge.** The plan derived
   4.5:12 from the *wall line*; with a 0.65 m overhang the half-span from eave edge to
   ridge is 7.55 m, and 4:12 over that span is what lands the crest at exactly 10.6 m.
   Same crest, stated consistently. Still the shallow end of the mission-tile range,
   which is what every source calls these roofs.
3. **The roof needed capping courses.** The plan's §2.9 asserted the roof would earn
   its read from "a crisp ridge, four clean hip planes, a deep eave". The first aerial
   disproved that: a bare hip solid is a blank orange lid. Added a ridge cap, four hip
   caps, and three tile courses per main slope. The ridge solid was dropped to 10.42 m
   so the capping course is what reaches 10.6 m.
4. **Window glass sits proud of its reveal, not behind it.** The first pass put the
   pane 0.05 m behind an ink plate; every window rendered as a black hole, losing the
   style bible's "dark blue-grey graphical windows" entirely. Reversed: ink plate
   recessed, glass proud, ink visible only as a border.
5. **The bevel had to become adaptive** — this was a genuine validator FAIL, not a
   polish note. A fixed 0.12 m bevel applied to the 0.15 m-thick cornice
   self-intersected: it inverted that solid (signed volume −3.06 m³) and left 74
   degenerate faces, failing both `normals_outward` and `no_degenerate_geometry`. The
   bevel is now clamped to 0.3 × the object's own smallest dimension, and a
   `dissolve_degenerate` pass follows it. After the fix: 0 degenerate faces, 0 inverted
   solids, ray-cast flipped fraction **0.000000**.
6. **The night review render must drive emission from base colour.** The asset ships
   with emission strength 0 (correct — the app owns the night pass), so glTF writes an
   `emissiveFactor` of black and the re-imported material has no glow colour to
   restore. Setting only the strength made every lit surface clip to white regardless
   of its palette entry. The rig now copies base colour into emission colour first, so
   the review shows what the material actually is.
7. **Duplex, and the two front doors are modelled.** Unverified for 542 specifically —
   the group is 16 duplex units plus 4 single-family homes and the two-door cue comes
   from a photographed sibling. Modelled because it is the majority case and the more
   informative silhouette. Flagged in `REFERENCE.md` §8.

## Orientation — a documented contract deviation

The contract's rule 3 says "front faces −Y in Blender". This asset's front faces
**ESE, bearing 121°**, and its long axis / roof ridge runs **NNE–SSW at 31°**, both
measured from the OSM footprint.

`placeGeneric()` in `app/src/assets.js` scales and positions but never rotates, so an
asset must be authored at its real-world heading or it lands askew in the city. Per
the orientation note in `docs/asset-plans/README.md`, real-world orientation wins
(AGENTS rule 5) and the deviation is recorded here. The four elevation renders are
labelled by true compass direction, which is why none of them is a face-on view of
the front — the front appears between the EAST and SOUTH tiles.

## Review renders

All generated from the **exported GLB**, re-imported into an empty scene, so every
image depicts exactly what ships.

`542-presidio-blvd-north.png`, `-east.png`, `-south.png`, `-west.png` (one shared
orthographic rig, identical scale/framing/lighting/exposure, differing only in
azimuth), `-top.png`, `-aerial.png` (105 mm lens, 38° down, per style bible §18),
`-night.png` (same aerial framing, glow on), and `-contact-sheet.png`.

The ortho scale is driven by the plan extent rather than the height, because this
building is wider than it is tall and height-driven framing cropped the eaves.

## Validation

`validation.json`, written by a fresh factory-reset Blender that imports only the
final GLB. All 16 checks **PASS**.

Normals are gated two ways, per the stage-2 override: the authoritative test is
per-object signed volume (this asset is a union of closed solids — every one must
enclose positive volume), backed by 22,500 deterministic visibility rays. Result:
`inverted_solids: []`, flipped fraction **0.000000** against a 0.15% ceiling.

## Stage 4 — optimize

Ran `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` with `ASSET_CLASS: landmark`,
`ALLOW_MESHOPT: yes` (verified — `setMeshoptDecoder` is registered in both
`app/src/gltf.js` and `app/src/assets.js`), `ALLOW_BAKE: no`. Scripts adapted from
`tools/glb-optimize/`; the pre-optimize asset is archived byte-for-byte at
`optimize/input/542-presidio-blvd.glb`.

| Metric | Before | After | Δ |
|---|---|---|---|
| Raw bytes | 194,236 | **84,960** | **−56.3%** |
| Gzip bytes | 28,810 | 56,873 | **+97.4%** |
| Objects / draw submeshes | 79 | **8** | −89.9% |
| Triangles | 3,092 | 3,092 | 0 |
| Vertices | 6,042 | **1,698** | −71.9% |
| Materials | 8 | 8 | unchanged |
| BBox | 23.608 × 25.455 × 10.6 | 23.608 × 25.455 × 10.6 | 0 |

Phase B did the structural work: a per-object 1 mm weld removed 4,344 coincident
vertex pairs, and joining per material collapsed 79 objects into 8. No interior faces
were provably buried (the census found none that passed the closed-solid occluder
rule), and limited dissolve at 0.05° found nothing to merge — the model is authored
from flat-shaded primitives with no coplanar redundancy to recover.

### The gzip finding — worth David's attention

**Meshopt cuts raw bytes by 56% but nearly doubles the bytes actually transferred.**
Vercel serves static assets with content-encoding compression, so what a browser
downloads is the compressed size: 28.8 KB before, 56.9 KB after. Meshopt output is
entropy-coded and therefore incompressible, so gzip can no longer exploit the very
repetitive float data in a small, boxy asset like this one.

This asset ships meshopt-compressed anyway, because it is mandatory, not a judgement
call: AGENTS.md and `.agents/skills/sf-asset-check/SKILL.md` §8 both require every GLB
entering `app/public/sf-assets/` to be meshopt-compressed at intake, and the loaders
register `MeshoptDecoder`. Shipping an uncompressed GLB would be the contract
violation.

But the headline numbers quoted in `GLB-OPTIMIZE-PROMPT.md` (257→42 KB, 924→156 KB)
come from assets one to two orders of magnitude larger, where meshopt wins on both
axes. At ~3k triangles the trade inverts. Both files are far under the 500 KB ceiling
either way, so nothing is at risk here — but if many small landmarks follow this one,
the crossover point is worth measuring rather than assuming. Recorded, not acted on.

### Gate results

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | PASS | material name set identical, both `_Glow` materials still separate, no `Toy_body` |
| G2 Geometry | PASS | bbox identical to 4 dp, origin unmoved, `inverted_solids: []`, flipped fraction 0.000000 |
| G3 Round-trip | PASS | re-imports in Blender; `g3check` loads it with pinned three — `ok:true`, 8 meshes, 3,092 tris, all 8 material names, no decode errors |
| G4 Appearance | PASS | A/B day+night × near+far, mean delta below thresholds, nothing visible — see `optimize/REPORT.md` |
| G5 Draw submeshes | PASS | 79 → 8 |
| G6 Size | PASS on raw (−56.3%); gzip regression documented above |
| G7 GPU budget | n/a | bake mode off |
| G8 Hygiene | PASS | re-import object count matches, deterministic re-run reproduces, no `.blend1` left |

## Stage 3 — approval

Approved in advance by David on 12 August 2026, quoted verbatim:

> "Do it on a new branch and PR -- i approve all stages just proceed"

The contact sheet, aerial, night render and the numbers above were produced and
presented; no revision was requested.
