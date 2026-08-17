# 92 South Park — optimize pass (stage 4)

Run of `docs/asset-pipeline/GLB-OPTIMIZE-PROMPT.md` against
`artifacts/92-south-park/`. `ASSET_CLASS: landmark`, `ALLOW_MESHOPT: yes`,
`ALLOW_BAKE: no`.

**All eight gates PASS. The optimized file is now the shipping GLB.**

## Metrics

| | Input | Shipped | Δ |
|---|---|---|---|
| Raw bytes | 535,412 | **249,832** | **−53.3%** |
| gzip -9 bytes | 75,497 | 156,835 | +107.7% (see note) |
| Triangles | 7,736 | 7,736 | 0 |
| Vertices | 16,708 | 16,767 | +59 (glTF re-splits for flat shading) |
| Objects | 195 | **16** | −91.8% |
| Draw submeshes (primitives) | 201 | **17** | −91.5% |
| Materials | 15 | 15 | 0 |
| bbox dims | 31.8607 × 32.0512 × 13.28 | identical | 0 |
| bbox min | −15.93033, −16.0256, 0.0 | identical | 0 |
| XY origin offset | 0.0, 0.0 | 0.0, 0.0 | 0 |

**On the gzip figure.** The input is uncompressed float32 geometry, which gzip crushes;
the output is meshopt-compressed, which is already entropy-coded and gzips badly. The
comparison to make is against the rest of the shipped set, not against the input:
`135-south-park` ships 108,524 raw / 79,703 gzip, `188-south-park` 119,312 / 61,724,
`551-third` 252,408 / 168,650. At **249,832 / 156,835** this asset sits alongside
`551-third` — it is the second-largest asset on the South Park oval because it carries
roughly twice the triangles of its neighbours (three masses, a modelled court, and a
deliberately non-repeating facade), and it is well inside the 500 KB budget in
`AGENTS.md`.

## Toolchain

Blender 5.2.0 LTS (fbe6228777e7), `npx gltfpack@0.24`, node v22.19.0,
three ^0.185.1 (pinned in `g3check/package.json`), python3 + Pillow 11.3.0, gzip -9.

## Phase A — waste census

`inspect.json`. 195 objects, 201 primitives, 7,736 tris, 16,708 verts, 15 materials, no
textures, `NORMAL` the only non-position attribute.

| Finding | Count | Plan |
|---|---|---|
| Coincident vertex pairs (≤1 mm) | 12,466 | weld per object — the bevel pass leaves every box with duplicated corner verts. 16,708 → 4,242 verts |
| Objects joinable per material | 195 → 15 groups | join; this is the whole win here |
| Duplicate mesh groups | 1,000 redundant tris reported | left alone — they are the repeated window solids, and joining per material collapses their *node* overhead, which is what actually costs bytes |
| Degenerate tris | 0 | — |
| Buried interior faces | 0 provable | the occluder rule needs a closed solid with ≥95% AABB fill; every solid here stands at 45° to the world axes, so none qualifies. Correctly conservative — no faces removed |
| Over-tessellated curves | `court_curve` only (332 tris, 10 segments) | left alone: it is the one non-orthogonal element on the lot and its arc is the court's identity from directly overhead |

## Phase B — geometry cleanup

`optimize.py`, `phaseb_stats.json`. Weld ≤1 mm per object → delete degenerates → buried
interior faces (none provable) → limited dissolve at 0.05° → join per material.

**Asset adaptation:** eight objects are skipped by the dissolve — `A1_parapet`,
`A2_parapet`, `B_parapet`, `C_parapet`, `stripe_front`, `stripe_rear`, `roof_rail`,
`balcony_rail`. They are closed ring bands following a rectangle all the way round,
i.e. exactly the case GLB-OPTIMIZE-PROMPT §3 step 3 warns about: their top and bottom
faces are coplanar annuli, a strictly-coplanar dissolve merges each into one ngon, and
re-triangulating an annulus emits sub-millimetre slivers that only the stage-2 contract
validator sees, two steps later and after the shipping swap.

Joins: `Toy_ink` 96 objects → 1, `Toy_glass` 41 → 1, `Toy_glass_Glow` 7 → 1, and twelve
smaller groups. After the stage-5 colour fix `Toy_roofd` is down to the eight court-stair
treads, and the mass boxes join straight into the `Toy_steel` group because their top
faces are now the same material as their walls.

## Phase C — meshopt

```
npx gltfpack@0.24 -i mid.glb -o 92-south-park.optimized.glb -c -km -kn -noq
```

`-c` meshopt-compresses (the app registers `MeshoptDecoder` in `app/src/gltf.js` and
`app/src/assets.js`); `-km -kn` keep the material and node names the loader treats as
API; `-noq` keeps float32 attributes, which the merge paths need.

## Gates

| Gate | Result | Evidence |
|---|---|---|
| G1 Contract | **PASS** | material name set identical (15/15); `Toy_gold_Glow` and `Toy_glass_Glow` still their own objects and materials; no `Toy_body` in a landmark; node names intact |
| G2 Transform | **PASS** | bbox dims and min identical to 6 dp; XY origin 0,0; all 16 signed volumes positive; 22,500-ray visibility test, 15,577 hits, **0 flipped** |
| G3 Round-trip | **PASS** | `g3check` (pinned three ^0.185.1) reports `G3-OK`, 17 meshes, 7,736 tris, 15 materials, correct bbox, no decode errors |
| G4 Appearance | **PASS** | table below; **worst 0.0078%** against a 2% (aerial) / 4% (elevation) gate |
| G5 Draw calls | **PASS** | 201 → 17 primitives |
| G6 Size | **PASS** | −53.3% raw; 249,832 bytes against the 500 KB landmark budget |
| G7 Stage-2 re-validation | **PASS** | `blender -b --python ../validate_92_south_park.py --` on the **shipped** file: all 16 contract checks, 31,492 ray first-hits, 0 flipped |
| G8 Determinism | **PASS** | the pass was re-run four times end to end (see below); same input bytes give the same output bytes |

### G4 pixel deltas (`diffs.json`)

| View | mean abs RGB | max px delta |
|---|---|---|
| day_near | 0.0028% | 8 |
| day_far | 0.0039% | 8 |
| night_near | 0.0008% | 8 |
| night_far | 0.0078% | 42 |
| elev_n | 0.0064% | 3 |
| elev_e | 0.0011% | 4 |
| elev_s | 0.0005% | 5 |
| elev_w | 0.0001% | 2 |

## The colour defect stage 5 found, and why it came back here

After the pass above, the stage-5 app check measured the shipped asset in the running
diorama and found every roof deck rendering at **rgb(9,9,12)** — black — while this same
asset's `Toy_steel` parapet caps read **rgb(94,103,112)** in the same frame and
132 South Park's `Toy_steel` roof membrane read **rgb(97,110,120)**. The cause was the
palette, not the merge: `Toy_roofd` (`45454a`) simply has too little luminance for the
diorama's ambient, which is far lower than the stage-2 Blender rig's three suns plus 0.30
world ambient. Every large up-facing surface on this building was `Toy_roofd`, so from
the app's downward camera the whole landmark was a hole in the row.

Fixed by moving the roof decks to `Toy_steel` — also the truthful choice on a zinc-clad
building whose 2026 aerial imagery shows mid-gray roofs — and the pass was re-run from
the rebuilt input. Roofs now measure **rgb(94,105,111)** in the app, matching the caps.
`Toy_roofd` survives only on the court stair treads. The precedent is
`108-south-park` (2026-08-16), where a dark green needed roughly 3x its luminance for the
same reason.

## The z-fighting defect this pass found in the asset

The **first** run of this pass reported elev_s at 0.18% and elev_w at 0.32% with max
deltas of 147 and 163 — an order of magnitude worse than every other view, and all of it
in two small rectangles on the Jack London Alley elevation. The diff images localised it
to the two roll-up garage doors, and the A/B *input* render showed the cause: they were
solid z-fight speckle **before** optimization. This was a stage-2 defect, not an
optimizer artifact.

Two coincident planes, from the same root cause. The tile plinth stands `PLINTH_PROJ =
0.12 m` proud of the body wall above it, but every ground-floor opening — the two
shopfronts, the entry recess and door, the two garage doors, the alley and rear service
doors, and the two court glow patches — was authored with its outward offsets measured
from the **body wall**, so each frame layer sat buried inside the plinth and each
outermost layer landed exactly in the plinth's own outer plane. The garage leaf was the
worst case because it stopped precisely at 0.12.

Fixed at the source rather than accepted against the gate: `shopfront()` gained a
`base_d` parameter defaulting to `PLINTH_PROJ`, and the seven other openings were
re-based the same way. The asset was rebuilt, re-rendered, re-validated, and this pass
re-run from scratch. The elevations now diff at 0.0005% and 0.0001% — the two lowest
figures in the table — and the shopfront and garage frames are visible on the shipped
renders for the first time.

Worth carrying forward: **a landmark with a projecting plinth needs every plinth-level
opening dimensioned from the plinth face, not the wall behind it.** The optimize pass's
A/B render is what caught it, because the stage-2 rig's own elevations resolved the
depth fight the other way and looked clean.
