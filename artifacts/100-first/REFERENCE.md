# 100 First Plaza — reference dossier

Checked 2026-10-25 for the Transbay landmark batch. Labels: **published**, **measured**,
**inferred** (photo), **estimated** (modelling choice).

## Sources

- [OpenStreetMap way 91626348](https://www.openstreetmap.org/way/91626348) (`name=100 First Street`, `building:levels=3`): podium outline, 22 nodes, OBB 78.5 × 49.4 m, 3,518 m², bearing 45.2°. Tower part [1410929341](https://www.openstreetmap.org/way/1410929341): OBB 35.3 × 30.4 m, bearing 135.3°.
- [DataSF footprints / 2010 LiDAR](https://data.sf.gov/resource/ynuv-fyni), `sf16_bldgid` 201006.0001162 (MBLR SF3721003): max 122.36 m, majority 115.90 m.
- [Wikipedia — 100 First Plaza](https://en.wikipedia.org/wiki/100_First_Plaza): 27 floors, spire 136.25 m, roof 116 m, 19 m spire, SOM, 1988, postmodern, setbacks and a grooved faceted facade.
- [Commons — 100 First Plaza from Salesforce Park.jpg](https://commons.wikimedia.org/wiki/File:100_First_Plaza_from_Salesforce_Park.jpg) (April 2021).

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Spire tip | **136.25 m** | published |
| Roof | 116 m | published; LiDAR majority 115.9 m agrees |
| Tower plan | 34 × 29.5 m, 3.4 m corner notches | measured OBB; notch estimated |
| Setbacks | 96 / 106 / 116 m, insets 3 / 6 m | estimated (photo) |
| Podium | OSM outline, 13 m | outline measured; height estimated (3 levels) |
| Anchor (manifest) | **-122.3977206, 37.7891952** | bbox centre after `tk.run` recentre (authored around tower OBB centre -122.3975827, 37.7892919) |

## Orientation

Tower yaw −45.3° (local +x bearing 135.3°). +Y = true north. The podium runs ~40 m
toward the SW of the tower; NW = Mission side, NE = First St side.

## Recognition cues (ranked)

1. Setbacks climbing to a pointed crown and thin spire.
2. Pink-cream stone against deep blue-glass notches.
3. Square plan with notched corners.

## Preserved

- Spire and roof heights, both OSM outlines, the tower heading.

## Simplified

- The real crown's several gabled glass roofs → two stacked pyramids.
- Faceted bay windows → flat punched panes; the mid-face glass slots of the photo are
  left out (only the corner notches are glass).
- Podium west steps → one diagonal.

## Uncertainties

- Setback heights and notch size are photo estimates.
- `Toy_sand` is less pink than the real stone.
- Two faces are not in the photo (assumed identical); podium roof not photographed.
