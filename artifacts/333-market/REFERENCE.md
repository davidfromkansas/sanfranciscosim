# 333 Market Street — reference dossier

Checked 2026-10-25 for the Transbay landmark batch. Labels: **published**, **measured**,
**inferred** (photo), **estimated** (modelling choice).

## Sources

- [OpenStreetMap way 288505729](https://www.openstreetmap.org/way/288505729): footprint (114 nodes — serrated corners, 1,806 m², OBB 48.7 × 39.6 m, bearing 45.3°, `height=149 m`, `building:levels=33`).
- [DataSF footprints / 2010 LiDAR](https://data.sf.gov/resource/ynuv-fyni), `sf16_bldgid` 201006.0001373 (MBLR SF3710020): max 146.07 m, majority 135.63 m, median 135.58 m.
- [Wikipedia — 333 Market Street](https://en.wikipedia.org/wiki/333_Market_Street): 33 floors, 144 m (472 ft), 1979, Gin Wong Associates.
- [Commons — 333 Market Street 2021.jpg](https://commons.wikimedia.org/wiki/File:333_Market_Street_2021.jpg): the lead photo, from Market at Beale/Davis.

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Roof / crest | **144.0 m** | published; LiDAR max 146.1 m agrees |
| Footprint | 48.7 × 39.6 m (model 46 × 37 m wall line, 3 × 2.6 m corner stairs) | measured (OSM); stair simplified |
| Floors / year / architect | 33 / 1979 / Gin Wong Associates | published |
| Anchor (manifest) | **-122.3974030, 37.7919380** | measured: OSM OBB centre; recentre shift 0 |

## Orientation

Yaw +45.3° (local +x bearing 44.7°). +Y = true north. Faces: **NW = Market St** (long
face), NE short face toward Beale, SW short face toward Fremont, SE long face toward
the mid-block / 45 Fremont.

## Recognition cues (ranked)

1. Fine full-height vertical pinstripes: pale bronze piers over dark glass.
2. Serrated, stepped corners.
3. Plain flat top.

## Preserved

- 144 m crest, OSM footprint and heading; the serrated outline carried full height.

## Simplified

- Piers → one every 2.8 m (real bays are finer); thin bronze floor lines.
- 114-node outline → three 2.6 m steps per corner.

## Uncertainties

- `Toy_terracotta` piers may read warmer than the real pale bronze/tan cladding.
- Roof not photographed; flat roof with plant assumed. LiDAR majority 135.6 m suggests
  a lower main roof level than the 144 m crest.
- The 0.985 Z normalization in `tk.run` lands the plant crest at 144 m.
