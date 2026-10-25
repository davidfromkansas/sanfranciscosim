# 45 Fremont Street — reference dossier

Checked 2026-10-25 for the Transbay landmark batch. Labels: **published**, **measured**,
**inferred** (photo), **estimated** (modelling choice).

## Sources

- [OpenStreetMap way 32946535](https://www.openstreetmap.org/way/32946535): footprint (5 nodes, 1,746 m², OBB 46.8 × 37.5 m, bearing 134.4°; `height=149`, unsourced).
- [DataSF footprints / 2010 LiDAR](https://data.sf.gov/resource/ynuv-fyni), `sf16_bldgid` 201006.0001422 (MBLR SF3710019): max 146.02 m, majority 135.42 m, median 132.14 m.
- [Wikipedia — 45 Fremont Street](https://en.wikipedia.org/wiki/45_Fremont_Street): 34 floors, 476 ft roof, 1978, SOM, "Bechtel Building".
- [CTBUH building 12690](https://www.skyscrapercenter.com/building/45-fremont-street/12690) (cited by the infobox).
- [Commons — 45 Fremont Center, San Francisco.jpg](https://commons.wikimedia.org/wiki/File:45_Fremont_Center,_San_Francisco.jpg): the Wikipedia lead photo (upward view of two faces).

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Roof / crest | **145.0 m** | published (476 ft); LiDAR max 146.0 m agrees |
| Footprint | 46.8 × 37.5 m (model 45.5 × 36.5 m, 4.5 m chamfers) | measured (OSM OBB); chamfer inferred |
| Floors / year / architect | 34 / 1978 / SOM | published |
| Anchor (manifest) | **-122.3971490, 37.7912310** | measured: OSM OBB centre; recentre shift 0 |

## Orientation

Yaw −44.4° (OSM bearing 134.4°). +Y = true north. Faces: **SW = Fremont St** (address
front, street trees), SE toward Mission / 350 Mission, NW toward Market / 333 Market,
NE toward 50 Beale.

## Recognition cues (ranked)

1. Strong cream/dark horizontal striping, one stripe per floor.
2. Softened corners that the stripes wrap round.
3. Plain flat top with a cream band.

## Preserved

- 145 m crest, OSM footprint and heading, 33 storey stripes above an 8 m base.

## Simplified

- Ribbon windows with mullions → continuous dark glass bands between proud cream spandrels.
- The mid-height louvred mechanical band seen in the photo → omitted.
- Base → glazed lobby behind cream columns (inferred).

## Uncertainties

- The LiDAR majority (135 m) suggests most roof returns sit ~10 m below the crest
  (a recessed roof inside a screen?). Modelled as a flat roof with plant; the 0.979 Z
  normalization in `tk.run` brings the plant crest to 145 m.
- Chamfer size read from one photo. NE face not photographed.
