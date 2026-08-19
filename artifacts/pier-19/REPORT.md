# Pier 19 — build report

**Status: built, approved, optimized (626→211 KB, 447→13 draw submeshes), validated all-PASS on the shipped GLB.**

A stylized miniature of Pier 19, The Embarcadero (1936–38, Contributing
Resource, Port of San Francisco Embarcadero Historic District), delivered as
`artifacts/pier-19/pier-19.glb` per `docs/asset-plans/pier-19.md`.

## Numbers

| | |
|---|---|
| Triangles | **7,782** (cap 18,000) |
| File | **211,424 B meshopt** (was 626,236 raw); archive at `optimize/input/` |
| Objects | 13 shipped (447 authored, joined per material in stage 4) |
| Dims (axis-aligned) | 243.39 × 191.89 × **17.80** m |
| Vertical extent = targetHeightM | **17.8** (scale lands at 1.0) |
| Min Z | −2.8 (pile stubs; **negative by design**, see below) |
| XY centre offset | 0.0, 0.0 |
| Manifest anchor | **-122.3988181, 37.8030032** (bbox centre after recentring) |
| Long axis bearing | 54.89°; facade faces 234.89° |
| Materials | Toy_cream, Toy_white, Toy_stone, Toy_ink, Toy_navy, Toy_glass, Toy_steel, Toy_glassl + Toy_glassl_Glow, Toy_glass_Glow |
| Glow | arch lunette (warm) + 8 scattered monitor clerestory bays × 2 sides (cool), all open single-layer outward-checked quads |

## Origin convention (read before integrating)

Local Z = 0 is the **top of the pier deck**, not the model's lowest point —
the same convention pier-1 shipped with. `placeGeneric()` seats the origin on
one terrain sample at the anchor and the app's DEM carries the Embarcadero
piers as low ridges, so a model sitting on z = 0 would float above its own
deck. Deck fascia and pile stubs run to −2.8 m; `targetHeightM` (17.8) is the
model's total vertical extent, **not** a height above water. Above-water
quantities: deck 2.0, gable crest 17.0.

## Dossier corrections while building

- The plan was drafted water-datum ("min z = 0 at the waterline") following
  pier-3's draft; the shipped pier-1 convention (deck-top origin, negative
  pile stubs, targetHeightM = vertical extent) replaces it. REPORT beats plan.
  Manifest values change accordingly: `targetHeightM` **17.8** (not 17.0);
  anchor **-122.3988181, 37.8030032** (bbox centre; 1.6 m from the plan's
  deck-rectangle centre because the bulkhead wings and proud pavilion skew the
  bbox slightly).
- Local QA found the first build's −2.2 m pile stubs bottoming 21 cm ABOVE the
  water plane (the DEM ridge at the anchor is 2.41 m, not the planned 2.0).
  Stubs deepened to −2.8 m (bottoms land at −0.39, just under water, robust to
  DEM variance along the pier); extent and targetHeightM became 17.8. The full
  stage 2→4 loop was re-run: re-render, re-validate, re-optimize, all gates
  re-passed with identical byte counts and pixel deltas.
- Everything else in the plan's §2.1/2.3 held up (merged footprint, 153×800 ft
  BSHC dims, 54.89° bearing, LiDAR flagpole reading).

## Design decisions of record

- **No flagpole**: the LiDAR max (19.5)/first-return peak (20.4) is the pole;
  a hairline pole as bbox top would rescale every wall by ~13%. Crest cap at
  exactly 15.0 above deck (17.0 above water) is the bbox top.
- **The pier's strip of the 1961 connector era** is modeled as a lower flat
  extension of the shed (a 12→57.6 m, roof 9.0) so the shore end matches the
  satellite massing; the connector across the Pier 23 slip and Pier 23 itself
  are out of scope (future `pier-23` asset owns them).
- Shed walls Toy_cream / roof Toy_stone (the pier-1 pairing, calibrated for
  the app's lighting); south-flank strip windows read as steel plates (they
  are plated in reality), north keeps glass.
- Night: scattered monitor clerestory (8 of 20 bays, both sides) as the hero,
  warm arch lunette as the accent; a storage pier is mostly dark.

## Validation

`validation.json` — **overall PASS**, fresh isolated scene, re-imported GLB:
7,782 tris; no textures, transparency, cameras, lights, animations, armatures,
constraints; transforms applied; no negative scales; materials all `Toy_*`
(no `Toy_body`); signed volume positive for all closed solids; glow strips all
outward (ray-verified); 31,500-ray visibility test residual 0.112% (≤ 0.15%
allowed at coincident faces); no degenerate triangles.

One validator finding fixed during the session: the monitor glow quads were
first named `mglow_*`, which missed the `_glow` naming convention and sent
open quads into the signed-volume test (9 "inverted" objects). Renamed
`mon_glow_*`; geometry unchanged.

## Renders

`pier-19-{west,east,north,south}.png` (shared ortho rig, pier-axis aligned),
`pier-19-top.png`, `pier-19-facade.png` (long-lens square-on),
`pier-19-aerial.png` (high three-quarter from the SSW — the review view),
`pier-19-aerial-ne.png` (bay side), `pier-19-aerial-night.png`,
`pier-19-contact-sheet.png`. All render the exported GLB re-imported into an
empty scene. The aerial was reviewed first and drove one iteration (shed walls
cream over stone monochrome).

## Manifest draft

```json
{
  "id": "pier-19",
  "file": "pier-19.glb",
  "anchor": [-122.3988181, 37.8030032],
  "targetHeightM": 17.8,
  "cat": 25,
  "name": "Pier 19",
  "estimated": false,
  "dims": [243.387, 191.892, 17.8],
  "tris": 7782,
  "loadRadius": 2500
}
```

## Local QA (Case B, batch mode) — 2026-08-19

Bake: full chain (terrain → … → context → muni-shapes) on the pier-1 worktree's
`pipeline/data` vintage (cp -Rc clone), exit 0. **Discarded before commit per
batch mode** — the branch ships source only; the city is re-baked once by
BATCH-INTEGRATE.

| Check | Result |
|---|---|
| Audit 1.6 | PASS — 114 zones over 110 landmarks clear. (1.2b/1.3c/1.7b FAIL pre-existing on main, same values pier-1 and 135-south-park recorded) |
| verify-rebake | PASS — "new since origin/main: pier19 @ 22_8"; 584/585 cells unchanged; 22_8 21→20 (the merged DataSF ring dropped); nearest surviving footprint **146.0 m vs 95 m radius**; zero stray cells (zero-churn data-vintage effect) |
| Exclusion drop set | 2 rings, verified analytically against the bake inputs: DataSF 201006.0000010 (gate 73.8 m) + Overture 8fb7a212 (gate 73.7 m). Keepers: Overture "Pier 17" gates at 120.9 m, DataSF Pier 15/17 at 146.0 m |
| Merge line / scale | `sf-assets: pier-19 merged 16 objects / 10 materials -> batched (5273 tris body); uniform x1.0000 at 3404, -3648` |
| Seated height | y = **2.41 m** (DEM ridge at the anchor). Deck at 2.41; pile stubs reach **−0.39 m**, just under the water plane — after the −2.8 m stub fix this session (the first build's −2.2 m stubs bottomed 21 cm ABOVE water) |
| One building, no twin | PASS — the merged procedural block is gone; the facade meets the promenade cleanly. Collateral as documented: Pier 23's site is its bare DEM ridge until a pier-23 asset ships |
| Orientation | PASS — arch facade faces the Embarcadero at 234.9°; verified against the street and Pier 17 |
| Footprint vs neighbours | PASS — reads at correct length/width against Pier 17 and the Pier 23 slip |
| Night glow | PASS in-app — scattered cool clerestory dashes along the monitor + warm arch lunette; the rest dark (working-pier design) |
| Draw calls | 97 with 90 landmarks live (forced full render, info.autoReset off); streaming-check hero avg 170/frame — both < 300 |
| landmark-streaming-check | **all 6 checks PASS** against the dev server (boot unloaded / hero budget / load on approach / release on depart / re-approach zero failures / near-landmark draw calls) |
| Batch reserve | pier-19 brings the all-resident total to 1,515,933 of the 1,600,000-vert BODY reserve (~84k headroom). One transient `BatchedMesh` overflow warning was observed under QA's forced update pump (71 entries fading at once — double occupancy); steady-state and streaming-check show zero failures. **BATCH-INTEGRATE should re-check the reserve after merging the full batch** |
| Fallback drill | PASS — GLB renamed: app boots, exactly one `sf-assets: pier-19 failed to load` warning, Case B site is empty water/deck inside the zone (expected), restored |
| Lint / tests / build | eslint clean; 26/26 tests pass; `npm run build` completes (compress-tiles 3315 tiles) |

Known pre-existing overlay: a thin route/wake line crosses the water near the
pier (present citywide over the waterfront, unrelated to this asset).

## Approval log

- 2026-08-19 — approved in advance by the owner in the pipeline invocation:
  "APPROVE EVERYTHING DONT ASK ME FOR PERMISSION" (batch run, Pier 19). Gate 3
  recorded on that standing instruction; renders and numbers presented in this
  report and the contact sheet.
