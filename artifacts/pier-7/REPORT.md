# Pier 7 — build report

Asset: `pier-7.glb` — Pier 7, the Broadway public access pier (1990, ROMA Design
Group + T.Y. Lin International; 1993 ASLA National Honor Award). Stage 2 of
`docs/asset-pipeline/ADDRESS-TO-ASSET.md`, executed from `docs/asset-plans/pier-7.md`.

## Shipped numbers (post-optimize, stage 4)

| Metric | Value |
|---|---|
| Triangles | **13,860** (cap 14,000; unchanged by optimize) |
| Objects | 7 (joined per material at stage 4; authored as 540) |
| Dims (AABB) | **219.57 × 165.99 × 7.60 m** — a 257.3 × 26.9 m pier at a 54.65° heading; the diagonal AABB is expected, not a scale error |
| min Z | **0.000 — the WATERLINE**, by design (pier-3 water-datum rule); pile feet reach it, deck top is +3.0 m |
| bbox top | **7.600 m = targetHeightM** (lamp-globe tops; loader scale lands at 1.0) |
| XY centre offset | (−0.56, −0.29) m — origin is the footprint OBB centre (= manifest anchor); the AABB centre differs because the mid bay and end platform flare asymmetrically |
| Materials | Toy_timber, Toy_timberd, Toy_ink, Toy_stone, Toy_steel, Toy_gold, Toy_amber_Glow |
| Glow | `Toy_amber_Glow` on the 44 lamp globes ONLY |
| Validation | `validation.json` — all checks PASS (fresh-scene re-import of the exported GLB) |

**`targetHeightM = 7.6` is a vertical extent above the waterline** (deck +3.0, lamps
+4.6 above deck), not an architectural height — the pier-1/pier-3/64-south-park
convention. **min Z = 0 is a PASS**: Z = 0 is the waterline, `placeGeneric` seats the
origin at `max(0, sampleElevation)` = 0 over the bay (terrain verified 0.00 across the
footprint).

## What was built

Deck slab on 109 pile bents (ink fascia + soffit), timber walking surface with darker
centre lanes, timber bullrail, ~150-post two-rail near-black railing on every edge
except the open shore entry, **44 single-globe Embarcadero lamp standards in two
straight rows** (the identity feature; globes exaggerated to 0.5 m), 22 iron-and-wood
benches, the granite entry-plaza band with Steve Gillman's two "Bay Bench" blocks and
the bronze viewing grill, and two steel fish-cleaning stations on the end platform.
No building — the pier is empty by design and the model keeps it that way.

Night state: the 44 globes and nothing else (two dotted lamp lines over black water,
matching the real pier). Glow authored as solid `Toy_amber_Glow` spheres — the
luminaire IS the object; base colour `f6e3c0` is the night look (the app draws _Glow
unlit at the material colour).

## Dossier corrections made while building (REPORT beats plan)

1. **The plan's first draft had the pier's two wide ends swapped**: the measured OSM
   footprint puts the 26.9 m width at the **Bay-end platform** and 20.7 m at the shore
   plaza. Corrected in the plan before modelling; the model follows the measured
   polygon vertex-for-vertex.
2. **The exclusion radius was re-measured against the bake input and halved (100 → 60)**:
   the pier bakes from exactly one input footprint (DataSF `area_id 855`, 1.4 m from
   the anchor); the tiles' toy roof bumps do not exist in the input (toy-pass
   furniture); and r = 100 would have deleted the **San Francisco Belle** (the moored
   riverboat off Pier 3, nearest vertex 98.6 m). r = 60 spares it by 38.6 m.
3. Railing post beat 3.2 → 3.8 m and globes 8×6 → 8×5 segments to hold the 14k cap;
   22 benches instead of 16 (the end platform takes four, per photographs).

## Renders

`pier-7-{north,east,south,west}.png` (shared ortho rig, 2400×500), `pier-7-top.png`,
`pier-7-water.png` (low from the SE — proves the pile field and soffit),
`pier-7-axis.png` (eye-level down the pier — the classic photograph and the lamp-row
acceptance test), `pier-7-aerial.png` (high three-quarter from the SW, the app's
camera), `pier-7-aerial-night.png`, `pier-7-axis-night.png`, and
`pier-7-contact-sheet.png`. All rendered from the re-imported exported GLB; night
renders drive emission from Base Color at strength 1.0 (glTF drops authored emissive
colour otherwise).

## Draft manifest entry

```json
{
  "id": "pier-7",
  "file": "pier-7.glb",
  "anchor": [-122.3955159, 37.7994429],
  "targetHeightM": 7.6,
  "cat": 0,
  "name": "Pier 7",
  "estimated": false,
  "dims": [219.5688, 165.9949, 7.6],
  "tris": 13860,
  "loadRadius": 2500
}
```

Stage 4 (see `optimize/REPORT.md`): 957,804 → **349,512 bytes raw** (−63.5%), 540 → 7 draw submeshes, geometry and appearance identical within gates; `validation.json` here is the packed shipping file's run (all PASS).

## Stage 3 — approval

The user pre-approved the full pipeline for this session:
**"APPROVE EVERYTHING DONT ASK ME FOR PERMISSION"** (2026-08-19, session
instruction accompanying `BUILDING: Pier 7`, `BATCH: yes`). Logged here per
Gate 3; renders are presented in the session's final report.

## Stage 5 — local QA (batch mode)

Bake: full chain (terrain → muni-shapes) on the cloned 12 Aug `pipeline/data`
(zero-churn recipe); `verify-rebake`: **584 of 585 cells unchanged**, only `23_9`
moved (17 → 18: the pier slab dropped; the fresher input added the San Francisco
Belle at 98.6 m — which *survived* the r = 60 exclusion, proving the sizing) —
overall PASS. `audit.mjs` check 1.6 PASS (114 zones clear; 1.7 allowlists pier
vertices, 0 offenders; the three failing checks — 1.2b p95 height, 1.3c Telegraph
Hill DEM, 1.7b one offshore tree — are dataset-vintage items unrelated to this
landmark). Penetration test on the fresh tiles: **no ring intrudes into the pier
footprint in either tier**. Streets tier: no footway within 110 m.

Headless-Chrome QA against `app/dist` (`qa_local.mjs`, screenshots in `qa/`):

| Check | Result |
|---|---|
| Merge line | PASS — `sf-assets: pier-7 merged 7 objects / 7 materials -> batched (7332 tris body); uniform x1.0000 at 3694, -3255` |
| Uniform scale | PASS — exactly 1.0000 |
| Water seat | PASS — placement matrix y = **0.000** (the water plane; anchor confirmed over open bay) |
| One building at the spot | PASS — pier slab carved out; day screenshot shows only the GLB |
| Night state | PASS — two dotted rows of warm lamp globes, nothing else lit |
| Draw calls | PASS — avg 85/frame at the landmark (< 300) |
| Asset warnings | PASS — none |
| Fallback drill | see `qa/drill.json` — GLB served 404, app boots, one `pier-7 failed to load` warning, empty water at the site (expected for Case B over the bay) |

Batch mode: the bake was then discarded (`git checkout -- app/public/tiles api/_data`)
and only source committed — GLB, manifest entry, registry entry, plan, artifacts.
