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

## Stage 5 — integration

Case **B** (new landmark): manifest entry + `pipeline/lib/landmarks.mjs` registry entry +
tile re-bake. Two bugs were found by doing it, both of which would have shipped broken.

### The `camera` field is not optional — omitting it breaks the whole city

The plan's §2.13 said "No camera preset is warranted: a 10.6 m house does not deserve a
search/fly-to preset of its own. Omit `camera`." **That is wrong and it took the app down.**

`pipeline/context.mjs:258` bakes `camera: l.camera` straight through, and
`app/src/main.js:126` maps every `manifest.landmarks` entry through `toCameraTarget()`,
which reads `preset.camera.yaw` unconditionally. A registry entry without `camera`
therefore produces a landmark whose preset is `undefined`, and the app dies at boot with
`Failed to load the city: Cannot read properties of undefined (reading 'yaw')` — not a
degraded landmark, the entire city. Fixed by giving it
`camera: { distance: 200, yaw: 30, pitch: 26 }`, and the constraint is now commented in
the registry so the next small landmark doesn't repeat it.

### Pipeline step order matters: `validate` must run before `toy`/`lore`/`notables`/`context`

After adding the camera I re-ran `npm run validate` alone to regenerate `manifest.json`.
`validate` republishes the base tile set and clears everything else, which deleted the
`toy/`, `toyland/`, `toystreets/`, `ctx/` and `context/` tiers — 2,260 files. The
documented chain order is not cosmetic. Recovered by re-running
`toy → notables → context` afterwards.

### The tile diff is 598 files, and all of it is required

Removing one baked footprint renumbers the global building index, and the `ctx/*.json`
sidecars store building ids as indices into that array. Verified across 15 randomly
sampled far-away cells: coordinates, identities and search payloads are **byte-identical**
and only the ids shift by exactly 0 or 1. So the citywide diff is not upstream data drift —
it is one deletion propagating — and a partial commit would desync ids from geometry.
`api/_data/stats.json` confirms it: `buildings 174770 → 174769`.

Geometry changes are confined to the affected cells: `buildings/13_9.bin`,
`landcover/13_9.bin`, `landcover/13_10.bin`, `toy/13_9.bin`, `toyland/13_9.bin`,
`toyland/13_10.bin`, plus the indexes.

### Exclusion radius, verified against the bake

`exclude: 14` (not the 13 the plan proposed — 14 centres the margin better). Measured
against the freshly baked footprints: **0 baked footprints have a vertex inside r = 14 m**,
and the nearest surviving baked vertex is **18.91 m** away (543 Presidio Blvd). 542 is
dropped, every neighbour is intact. `node pipeline/audit.mjs` check **1.6 PASS —
29 landmarks clear**.

### Local QA

| Item | Result |
|---|---|
| Re-validation of the shipped GLB | **PASS** — 16/16 contract checks after the optimize swap |
| Manifest entry | **PASS** — matches existing formatting, `dims`/`tris` from the measurement |
| id mapping | **PASS** — `camelId('542-presidio-blvd')` → `542PresidioBlvd`, matches the registry |
| Registry + re-bake | **PASS** — one footprint removed, indexes regenerated |
| audit 1.6 | **PASS** — 29 landmarks clear |
| Single building at the site | **PASS** — no procedural twin, no z-fighting |
| Loader scale | **PASS** — manifest `targetHeightM` 10.6 over measured 10.6 → x1.0000 |
| Orientation | **PASS** — ridge NNE–SSW, porch faces the boulevard |
| Terrain seating | **PASS** — sits on the slope, no floating or sinking |
| Asset loads | **PASS** — `542PresidioBlvd` placed, `failed: 0` |
| Draw calls | **PASS** — `landmark-streaming-check`: **avg 90/frame < 300** |
| Boot with streamed entries unloaded | **PASS** (same harness) |
| Streamed load on approach | **PASS** (same harness) |
| Night glow | **PASS with a note** — only the porch light and the three lit panes light up, but see the open questions |
| Fallback drill | **PASS** — app boots, area renders, neighbours intact, site is empty ground inside the exclusion zone (the documented Case B outcome) |
| Lint / build | **PASS** — `eslint src` clean, `vite build` succeeds |

**Not verified, honestly:** the harness's `stream-out` and `re-approach` phases need the
100-entry synthetic manifest its header documents, so release-on-depart was not exercised
end to end; and fps could not be measured because the preview pane does not composite
continuously (the same reason that harness exists). Draw calls came from the headless
harness, which does render continuously, so the rule-2 budget itself is covered.

### Two art-direction notes for David

1. **The roof reads more saturated in the app than in the Blender review.** `Toy_brick`
   `#c96f4a` is a legitimate palette entry and real Presidio roofs are terracotta, but next
   to the muted baked neighbours it currently reads as a saturated accent rather than
   restrained architecture. If it is too loud, `Toy_rust` `#a86444` is the obvious swap.
2. **The night state is very quiet.** A porch lamp and three panes is deliberate — a house
   is not a skyline piece — but beside the procedurally lit neighbours the building reads
   as almost unlit. Easy to raise; wanted a decision rather than a guess.

## Stage 3 — approval

Approved in advance by David on 12 August 2026, quoted verbatim:

> "Do it on a new branch and PR -- i approve all stages just proceed"

The contact sheet, aerial, night render and the numbers above were produced and
presented; no revision was requested.
