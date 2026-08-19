# Pier 15 (Exploratorium) — build report

**Asset:** `artifacts/pier-15/pier-15.glb` · built 19 Aug 2026 · Blender 5.2.0 LTS
(headless, deterministic script `build_pier_15.py`)

## Shipped numbers (fresh-scene validation of the exported GLB)

| Metric | Value | Gate |
|---|---|---|
| Overall validation | **PASS** (`validation.json`, all checks) | PASS |
| Triangles | **11,152** | ≤ 22,000 ✓ |
| Objects | 324 meshes (loader merges to ≤ 2 draw calls) | ✓ |
| Dimensions | 249.25 x 221.09 x **16.40** m | ✓ |
| min Z | 0.000 (waterline; pile feet touch it exactly) | ✓ |
| Bbox top | 16.400 = targetHeightM → loader scale **1.0** | ✓ |
| XY centre offset | (-4.95, -0.56) m — AABB centre vs the surveyed area-centroid origin; the deck flares at the seawall and carries the south apron, so this is honest, not misplacement | ✓ (documented tolerance 5.5) |
| Materials | 12 `Toy_*`, flat, no textures, no alpha; 3 `_Glow` sets (glassl/amber/glass) | ✓ |
| Normals | signed volume: 0 inverted; 31.5k visibility rays: 0.0% flipped | ✓ |
| Cameras/lights/animations/armatures | none | ✓ |

## Review renders (all from the exported GLB)

`pier-15-{north,east,south,west,frontage,top,water,aerial,aerial-night}.png` +
`pier-15-contact-sheet.png`. The water view is taken from the courtyard side —
the only image that proves the pile field, deck soffit and courtyard notch.

## Iteration log

1. **Review 1 (aerial + frontage, low samples):** monitor read as a plain steel
   bar from above → added glazed cap-slope strips. The "O" ring's upper interior
   showed cream wall — the fanlight arch topped out below the ring → fanlight
   enlarged (span 8.4, crown 9.6), "O" lowered and resized (⌀5.1/4.2, centre
   z 6.9).
2. **Review 2 (arch zoom):** the amber fanlight glow, a filled arch panel,
   washed the whole glazing warm at the app's 12% day alpha; its concave ring
   profile also ear-clipped into a filled cap. Rebuilt as an explicit quad-strip
   arch band (`arch_band_panel`) — night reads as a lit portal outline, day is
   near-invisible. Letter kerning tightened; "R" leg widened.
3. **Validation catch:** three terrace railings carried an unapplied
   `location.z` offset → `rail_chain` gained a `base` parameter; transforms now
   all identity. OVERALL PASS.

## Dossier corrections (REPORT beats plan)

- The plan's expected AABB "~250 x 178 m" was a rotation-math slip; the correct
  expectation for the 245 x 94.8 m OBB at 54.9° is **~249 x 221 m** (measured:
  249.3 x 221.1). `validate_pier_15.py` gates on the corrected numbers.
- Monitor centreline built at **t = +9.0** in the pier frame (7.5 m SE of the
  shed centreline, straight from the rectified aerial) rather than the plan's
  provisional t = 11.
- The flagpole is deliberately omitted (plan 2.15: at true height it would
  become the bbox top and shrink the pier ~27%). The 16.4 m crest cap is the
  architectural top.

## Approval (stage 3)

The pipeline invocation pre-approved all gates: **"APPROVE EVERYTHING DONT ASK
ME FOR PERMISSION"** — David, 19 Aug 2026, in the BATCH: yes invocation of
ADDRESS-TO-ASSET for this building. Recorded here verbatim per gate 3; no
separate design sign-off was requested or given.

## Draft manifest entry (verified values)

```json
{
  "id": "pier-15",
  "file": "pier-15.glb",
  "anchor": [
    -122.3974662,
    37.8016046
  ],
  "targetHeightM": 16.4,
  "cat": 25,
  "name": "Pier 15 (Exploratorium)",
  "estimated": false,
  "dims": [
    249.25,
    221.09,
    16.4
  ],
  "tris": 11152,
  "loadRadius": 2500
}
```

`targetHeightM` is photogrammetric (range 15.8-17.0, method in plan 2.16);
`estimated` stays `false` on the strength of the two-way camera verification,
with the range recorded here. Integration notes incl. the measured exclusion
window (70 m; ceiling 84 m — Pier 17's gate) are in `docs/asset-plans/pier-15.md`
§2.13. **Note for integration: `SF9900015` is one merged DataSF polygon covering
Piers 15 AND 17 — excluding it un-bakes Pier 17 too, which then gap-fills whole
from its own Overture ring (h 16.4). Accepted collateral; verify Pier 17 still
stands in local QA.**
