# Omni San Francisco Hotel (Financial Center Building) — reference dossier

Checked 2026-10-25 for the Financial District landmark batch. Labels: **published**
(Wikipedia / Wikidata / assessor), **measured** (OSM geometry, DataSF 2010 LiDAR), **inferred**
(read from the photograph or description), **estimated** (a modelling choice).
Plan: `docs/asset-plans/500-california-street.md`.

## Sources

- OSM way 1279459281 — https://www.openstreetmap.org/way/1279459281 (`wikidata=Q26699326`)
- Wikipedia — https://en.wikipedia.org/wiki/Omni_San_Francisco_Hotel
- Commons photo — https://commons.wikimedia.org/wiki/File:Omni_San_Francisco_Hotel.jpg (California St face)
- DataSF 2010 LiDAR ring 201006.0001979 (mblr SF0240003) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): block 0240 lot 003, hotel, 17 storeys

## Verified dimensions and location

| Item | Value | Basis |
|---|---|---|
| Crest | 65.3 m | measured (facts-file LiDAR); main roof ≈ 62 m (LiDAR majority) |
| Storeys | 15 (1927) → 17 after the 2002 raised roof | published (Wikipedia) / assessor roll |
| Year / architects | 1926–27 / Frederick H. Meyer, Albin R. Johnson | published (Wikipedia) |
| Footprint | 42.5 × 42.2 m, 1,791 m² | measured (OSM) |
| Base 5 storeys ≈ 20 m; arched top storey |  | published (Wikipedia) + photo |
| Anchor (manifest) | **-122.4031981, 37.7931217** | OSM OBB centre shifted by the `tk.run` recentre |
| Model bbox | 54.0911 × 54.1823 × 65.3 m | validation.json |

## Orientation

Plan rotated ~9° from north. South face = California St; east = Montgomery St; west and north abut neighbours (the 2002 rear addition is on the north).

## Recognition cues (ranked)

1. Red-brick shaft on a tall tan rusticated base.
2. Round-arched ground storey and arched top-floor windows.
3. Deep corbelled cornice.

## Simplified

- Rustication, medallions and entrance canopy omitted; all four faces treated alike.
- `Toy_rust` stands in for the red-brown brick.

## Uncertainties

- Crest from the facts-file LiDAR value; the ring spans 61.7–68.3 m.
- The 2002 penthouse form is inferred (Wikipedia says only that the roof was raised).
- West/north faces are party walls in reality.
