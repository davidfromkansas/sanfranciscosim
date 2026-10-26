# 201 Mission Street — reference dossier

Checked 2026-10-25 for the Transbay landmark batch. Labels: **published**, **measured**,
**inferred** (photo), **estimated** (modelling choice).

## Sources

- [OpenStreetMap way 32862919](https://www.openstreetmap.org/way/32862919) ("Providian Financial Building", `height=138 m`, `building:levels=30`): whole footprint, OBB 99.7 × 53.3 m, 3,541 m², bearing 136.3°. Building parts [616813259](https://www.openstreetmap.org/way/616813259) (tower octagon) and [616813260](https://www.openstreetmap.org/way/616813260) (podium).
- [DataSF footprints / 2010 LiDAR](https://data.sf.gov/resource/ynuv-fyni), `sf16_bldgid` 201006.0000504 (MBLR SF3718026): max 135.89 m, majority 127.24 m.
- [Wikipedia — Providian Financial Building](https://en.wikipedia.org/wiki/Providian_Financial_Building): 417 ft (127 m) roof, 30 floors, 1981, architect Primiani Weaver, 489,284 sq ft, trapezoidal lot from Mission to Howard.
- [Commons — 201 Mission Street.jpg](https://commons.wikimedia.org/wiki/File:201_Mission_Street.jpg): the infobox photo, street level from the podium plaza side. Fetched in this pass (the batch had none).

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Crest | **135.9 m** | measured (LiDAR max): the penthouse |
| Main roof | 127.2 m | measured (LiDAR majority); published 127 m agrees |
| Tower plan | elongated octagon ~60 × 36 m | measured (OSM part) |
| Podium | lot-filling OSM part, 17 m | outline measured; height estimated |
| Lower wing | 18 × 11 m, top 57 m | estimated (photo storey count) |
| Anchor (manifest) | **-122.3949073, 37.7911895** | bbox centre after `tk.run` recentre (authored around the podium OBB centre -122.3949072, 37.7910519) |

## Orientation

+Y = true north. Tower octagon in raw OSM east/north metres (long axis ≈ −7.8° from
east); podium on the street grid (bearing 44.6°/136.3°). NW = Mission St,
SE = Howard St; NE and SW sides face neighbouring lots.

## Recognition cues (ranked)

1. Pale concrete shaft finely ribbed full height (slot windows between ribs).
2. Stretched octagonal plan with chamfered corners.
3. A lower wing stepping off one face.
4. Notched parapet.
5. Grey concrete podium with planted terraces.

## Preserved

- Crest and roof heights, OSM tower and podium outlines.

## Simplified

- Real rib rhythm is finer; ribs every 2.7 m with one slot window per bay and storey.
- Podium terraces → one deck with a hedge ring and a few trees.

## Uncertainties

- Which face carries the lower wing is **inferred** (placed toward Howard); its 57 m
  top is **estimated**.
- Faces not in the photo are assumed identical. Roof not photographed.
- Podium height 17 m **estimated**.
