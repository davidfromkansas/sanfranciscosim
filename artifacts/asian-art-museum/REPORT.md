# Asian Art Museum — build report

Deliverable: `asian-art-museum.glb`, a validated miniature of the Asian Art Museum of
San Francisco (200 Larkin Street, George Kelham's 1917 Main Library) for SF-SIM.

Built 12 August 2026 with Blender 5.2.0 LTS, headless, from the deterministic script
`build_asian_art_museum.py`. Research and sources: `REFERENCE.md`. This report
overrides `docs/asset-plans/asian-art-museum.md` wherever the two disagree.

## Numbers

| | Authored (stage 2) | **Shipped (after stage 4)** |
|---|---|---|
| Objects / draw submeshes | 163 | **11** |
| Triangles | 13,176 | **13,176** (budget 24,000) |
| Vertices | 25,686 | **6,910** |
| Dimensions | 115.31 × 65.18 × 28.10 m | **115.31 × 65.18 × 28.10 m** |
| Bbox min / max Z | 0.000 / 28.100 | **0.000 / 28.100** |
| XY centre offset | (0.000, 0.000) m | **(0.000, 0.000) m** |
| Loader scale (`targetHeightM / measuredHeight`) | 1.000 | **1.000** |
| Materials | 11, all `Toy_*`, flat, 0 textures, 0 transparency | **identical set** |
| Glow groups | 2 — `Toy_white_Glow`, `Toy_gold_Glow` | **2, preserved separately** |
| File size | 718,620 B raw | **323,984 B raw** (−54.9%) |
| Normals | positive signed volume, ray residual 0.0 | **ray residual 0.0** |
| Cameras / lights / animation / armatures | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |

The shipped file is the stage-4 output (`optimize/REPORT.md`: all gates G1–G6, G8
PASS; the authored original is archived at `optimize/input/`). Geometry is
unchanged — the whole saving is node and vertex overhead, not detail.

`validation.json` holds the full machine-readable report from a fresh-scene
re-import of the exported GLB (never the authoring scene). Overall: **PASS**.

## Corrections to the plan's dossier

Both were found by re-verification before modelling and both changed the geometry.
Detail in `REFERENCE.md` §7.

1. **OSM `height=46` is not a height.** It is the NAVD88 roof *elevation*
   (152.927 ft = 46.61 m), identical to `p2010_zmaxn88ft` in the DataSF LiDAR
   record for the same footprint. The model uses the LiDAR-measured **28.10 m
   crest** (raised central monitor) and **23.22 m main roof plane**. Building to
   the tag would have made the museum 1.6× too tall.
2. **The footprint is not the rectangle the plan described.** Projected into the
   Civic Center street grid, the OSM polygon steps back twice on the north-east
   (north wall S≈0 → 11.5 → 15.75 at E=62.5 and E=70) and once on the south-east
   (south wall leaves S=54.71 at E=93.6 for S=41.78). The east end is a 13 × 26 m
   block, not full depth. The model uses the surveyed ten-vertex rectilinear
   outline; sub-2 m jogs are absorbed and the area error against OSM is under 2%.
   The nadir aerial shows both setbacks independently.

## Design decisions that departed from the plan

| Plan said | Built | Why |
|---|---|---|
| 10 columns, each on its own plinth | 8 columns on one continuous stylobate and abacus | Individual plinths read as a picket fence from the app's aerial camera — rendered, reviewed, rejected |
| Pavilion 5.0 m tall on a 23.4 m deck | Pavilion top at 26.0 m | Above the 24.2 m attic so it reads from the street, below the 28.10 m crest so wHY's "fits within the datum lines" still holds |
| Cornice/attic as solid bands | Cornice and attic as closed **rings** | The first build buried the entire roof — the asset's largest surface — under a solid slab |
| No base openings | A row of small square openings in the rusticated base, south and north | 6.5 m of blank granite along a 94 m elevation read as a plinth, not a building |

## Orientation

Authored in true-world orientation: Blender `+Y` = true north, `+X` = east, whole
assembly rotated **+8.32°** about Z onto the Civic Center grid (long-axis bearing
81.68°). `placeGeneric()` in `app/src/assets.js` applies no rotation, so the asset
drops in at its real heading.

**The contract's "front faces −Y" rule is deliberately not honoured.** The museum's
main entrance faces **west**, onto Larkin Street and Civic Center Plaza. Real-world
orientation wins (AGENTS rule 5, and `docs/asset-plans/README.md`'s orientation
note). Recorded here as the required deviation.

## Night state

Two glow surfaces, both documented in the night reference photograph:

- `Toy_white_Glow` — the uplight cove under the Larkin colonnade (hero)
- `Toy_gold_Glow` — the three sets of bronze entrance doors (supporting)

Both carry palette day colours (`f7f4ec`, `caa64a`) that sit calmly beside their
non-glow neighbours, so the daylight asset is unaffected. The night render drives
emission from Base Color, per `docs/asset-plans/README.md`.

## Review renders

All eight regenerated from the final export, same rig, same lighting, same exposure:
`-north`, `-east`, `-south`, `-west` (orthographic elevations, shared scale),
`-top`, `-aerial` (41° down, 105 mm), `-night`, `-night-larkin`, plus
`-contact-sheet`.

## Approval (Gate 3)

Approved by David, 12 August 2026, verbatim:

> "Do it on a new branch and PR -- i approve all stages just proceed"

## Draft manifest entry

```json
{
  "id": "asian-art-museum",
  "file": "asian-art-museum.glb",
  "anchor": [
    -122.4159859,
    37.7802817
  ],
  "targetHeightM": 28.1,
  "cat": 16,
  "name": "Asian Art Museum",
  "estimated": false,
  "dims": [
    115.31,
    65.18,
    28.1
  ],
  "tris": 13176,
  "loadRadius": 2500
}
```

Measured from the **shipped** file (`validation.json`, fresh-scene re-import).

`cat` 16 = Museum (`CATEGORY_LABELS` in `app/src/context.js`). `loadRadius` is the
default rule `max(2500, 28.1 × 30)` = 2500; this is a low, wide building with no
skyline presence, so streaming it is unambiguously right. `dims` and `tris` are
updated to the shipped file at stage 4.
