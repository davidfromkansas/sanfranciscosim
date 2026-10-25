# San Francisco Museum of Modern Art (SFMOMA) — reference dossier

Checked 2026-10-25 for the Financial District landmark batch. Labels: **published**
(Wikipedia / Wikidata / assessor), **measured** (OSM geometry, DataSF 2010 LiDAR), **inferred**
(read from the photograph or description), **estimated** (a modelling choice).
Plan: `docs/asset-plans/151-3rd-street.md`.

## Sources

- OSM way 41692824 — https://www.openstreetmap.org/way/41692824
- Wikipedia — https://en.wikipedia.org/wiki/San_Francisco_Museum_of_Modern_Art
- Commons photo — https://commons.wikimedia.org/wiki/File:San_Francisco_Museum_of_Modern_Art.jpg (Botta facade from Yerba Buena Gardens, pre-2016)
- DataSF 2010 LiDAR ring 201006.0000183 (mblr SF3722367) — https://data.sf.gov/resource/ynuv-fyni (pre-expansion)

## Verified dimensions and location

| Item | Value | Basis |
|---|---|---|
| Botta oculus / skylight top | 39.6 m (130 ft) | published (Wikipedia, quoting NYT) |
| Snøhetta wing crest | 60 m | **estimated** (10 storeys) |
| Botta building | 5 storeys, 1995 | published |
| Expansion | 235,000 sq ft, Minna to Howard, 2016 | published (Wikipedia) |
| Botta step heights 12 / 20 / 28 m |  | inferred (photo) |
| Anchor (manifest) | **-122.4006347, 37.7859319** | OSM OBB centre shifted by the `tk.run` recentre |
| Model bbox | 137.262 × 112.9403 × 60.0 m | validation.json |

## Orientation

Local axes: x along Third St (bearing 135°), y away from it (45°). SW face = Third St (Botta front, facing Yerba Buena); NW = Minna St; SE = Howard St (Snøhetta's glass gallery); NE = Natoma side (Snøhetta's rippled white facade).

## Recognition cues (ranked)

1. Black-and-white striped cylinder with a slanted oculus.
2. Symmetric red-orange brick blocks stepping up to it.
3. Tall white rippled Snøhetta mass behind.
4. Striped entrance on Third Street.

## Simplified

- Botta's brick striations reduced to two stone courses; the wing's FRP ripples to ten bands.
- The wing's stepped/irregular top and its terraces simplified to one height.

## Uncertainties

- **Wing height estimated** (60 m); the whole model's crest depends on it.
- No post-2016 photo reviewed; the wing's facades are inferred.
- Split line between Botta and Snøhetta parts estimated from the footprint.
