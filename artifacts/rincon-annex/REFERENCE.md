# Rincon Annex (Rincon Center) — reference dossier

Checked 2026-10-25 for the Transbay landmark batch. Labels: **published**, **measured**,
**inferred** (photo/LiDAR reading), **estimated** (modelling choice).

## Sources

- [OpenStreetMap way 44106213](https://www.openstreetmap.org/way/44106213) (`name=Rincon Annex`, `height=33`): 15 nodes, OBB 82.6 × 91.5 m, 7,357 m², bearing 45.7°.
- [DataSF footprints / 2010 LiDAR](https://data.sf.gov/resource/ynuv-fyni), `sf16_bldgid` 201006.0000121 (MBLR SF3716021): max 29.74 m, majority 18.08 m.
- [Wikipedia — Rincon Center](https://en.wikipedia.org/wiki/Rincon_Center): Underwood, Streamline Moderne, 1939–40, 330 × 266 ft, three floors + half basement, dolphin friezes above doors and windows, NRHP 1979.
- [Commons — IMG 2185 Rincon Center San Francisco.JPG](https://commons.wikimedia.org/wiki/File:IMG_2185_Rincon_Center_San_Francisco.JPG): the Mission St front.

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Crest | **29.7 m** (atrium skylight) | measured (LiDAR max) |
| Parapet | 18.1 m | measured (LiDAR majority) |
| Footprint | OSM outline, ~82 × 92 m OBB | measured; published 101 × 81 m is the original building |
| Anchor (manifest) | **-122.3931571, 37.7925049** | bbox centre after `tk.run` recentre (authored around OSM OBB centre -122.3931459, 37.7925002) |

## Orientation

Yaw +45.7° (local +x bearing 44.3°). +Y = true north. NW = Mission St front, NE =
Steuart, SW = Spear, SE = atrium and The Towers at Rincon (`towers-at-rincon`, not
modelled here).

## Recognition cues (ranked)

1. Long white Moderne front, tall dark windows.
2. Blue dolphin friezes over the windows.
3. Blue-grey base and blue cornice line.
4. Glass atrium pyramid behind.

## Preserved

- Parapet and crest heights, OSM outline and heading, the window/dolphin rhythm of the
  Mission front.

## Simplified

- Dolphin reliefs → flat `Toy_sky` panels; gridded windows → single dark quads.
- The set-back third storey is drawn flush; the black-granite entry is omitted.
- OSM outline: tiny jogs dropped (15 → 8 points).

## Uncertainties

- Atrium plan and position are **inferred** from the LiDAR crest — verify against an
  aerial image and the `towers-at-rincon` GLB.
- Spear/Steuart and SE elevations **inferred** from the Mission front; roof skylight
  strips **inferred**.
