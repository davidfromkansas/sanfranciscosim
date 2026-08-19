# Pier 19 — build report

**Status: built, validated (all-PASS), awaiting approval.**

A stylized miniature of Pier 19, The Embarcadero (1936–38, Contributing
Resource, Port of San Francisco Embarcadero Historic District), delivered as
`artifacts/pier-19/pier-19.glb` per `docs/asset-plans/pier-19.md`.

## Numbers

| | |
|---|---|
| Triangles | **7,782** (cap 18,000) |
| Objects | 447 |
| Dims (axis-aligned) | 243.39 × 191.89 × **17.20** m |
| Vertical extent = targetHeightM | **17.2** (scale lands at 1.0) |
| Min Z | −2.2 (pile stubs; **negative by design**, see below) |
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
deck. Deck fascia and pile stubs run to −2.2 m; `targetHeightM` (17.2) is the
model's total vertical extent, **not** a height above water. Above-water
quantities: deck 2.0, gable crest 17.0.

## Dossier corrections while building

- The plan was drafted water-datum ("min z = 0 at the waterline") following
  pier-3's draft; the shipped pier-1 convention (deck-top origin, negative
  pile stubs, targetHeightM = vertical extent) replaces it. REPORT beats plan.
  Manifest values change accordingly: `targetHeightM` **17.2** (not 17.0);
  anchor **-122.3988181, 37.8030032** (bbox centre; 1.6 m from the plan's
  deck-rectangle centre because the bulkhead wings and proud pavilion skew the
  bbox slightly).
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
  "targetHeightM": 17.2,
  "cat": 25,
  "name": "Pier 19",
  "estimated": false,
  "dims": [243.387, 191.892, 17.2],
  "tris": 7782,
  "loadRadius": 2500
}
```

## Approval log

- (pending)
