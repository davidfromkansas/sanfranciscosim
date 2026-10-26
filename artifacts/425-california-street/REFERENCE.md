# 425 California Street — reference dossier

Checked 2026-10-25 for the Financial District landmark batch. Labels: **published**
(Wikipedia / Wikidata / assessor), **measured** (OSM geometry, DataSF 2010 LiDAR), **inferred**
(read from the photograph or description), **estimated** (a modelling choice).
Plan: `docs/asset-plans/425-california-street.md`.

## Sources

- OSM way 260283289 — https://www.openstreetmap.org/way/260283289
- Wikipedia — https://en.wikipedia.org/wiki/425_California_Street; https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_San_Francisco
- Commons photo — https://commons.wikimedia.org/wiki/File:425_California_Street.jpg (street level, looking up the corner)
- DataSF 2010 LiDAR ring 201006.0005008 (mblr SF0260001) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): block 0260 lot 001, 1968, 26 storeys

## Verified dimensions and location

| Item | Value | Basis |
|---|---|---|
| Roof / crest | 109.4 m | published; LiDAR median 108.8 m |
| Year / architect | 1968 / John Carl Warnecke & Associates | published (Wikipedia) |
| Floors | 29 (infobox) / 27 (tallest list) / 26 (assessor) | published, sources disagree |
| Footprint | 25.3 × 24.1 m, 609 m² | measured (OSM) |
| Base height ≈ 6.6 m |  | inferred (photo) |
| Gold fin caps at the roofline |  | inferred (photo) |
| Anchor (manifest) | **-122.4013729, 37.7928108** | OSM OBB centre shifted by the `tk.run` recentre |
| Model bbox | 34.2478 × 33.0283 × 109.4 m | validation.json |

## Orientation

Footprint used directly (edges 81.7° / 171.7°). North face = California St; west toward Sansome, east toward Leidesdorff; south faces the Bank of California block interior.

## Recognition cues (ranked)

1. Thin, very dark glass prism among pale stone neighbours.
2. Full-height black mullion fins giving a pinstripe texture.
3. Gold caps at the fin tops along the roofline.
4. Recessed dark granite base.

## Simplified

- Fin spacing 2.6 m (real ≈1.5 m); spandrels drawn as thin ink bands.
- Entrance canopy and signage omitted.

## Uncertainties

- Storey count differs between sources (26–29); only the height matters to the loader.
- Gold caps read from one photo; their exact extent is uncertain.
- South and east faces not photographed.
