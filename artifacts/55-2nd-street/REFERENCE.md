# KPMG Building (55 Second Street) — reference dossier

Checked 2026-10-25 for the Financial District landmark batch. Labels: **published**
(Wikipedia / Wikidata / assessor), **measured** (OSM geometry, DataSF 2010 LiDAR), **inferred**
(read from the photograph or description), **estimated** (a modelling choice).
Plan: `docs/asset-plans/55-2nd-street.md`.

## Sources

- OSM way 79377189 — https://www.openstreetmap.org/way/79377189
- Wikipedia — https://en.wikipedia.org/wiki/KPMG_Building; https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_San_Francisco
- Commons photo — https://commons.wikimedia.org/wiki/File:KPMG_Building_from_the_street_level.jpg
- DataSF 2010 LiDAR ring 201006.0001193 (mblr SF3708096) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): 0055 2nd St, 2002, 24 storeys

## Verified dimensions and location

| Item | Value | Basis |
|---|---|---|
| Roof | 100.6 m | published; LiDAR majority 107.6 m (higher) |
| Floors / year / architects | 25 / 2002 / Heller Manus, HKS | published (Wikipedia) |
| Footprint | 50.5 × 36.5 m, 1,825 m² | measured (OSM) |
| Podium cornice ≈ 44 m (11 storeys), setbacks ≈ 84 and 92 m |  | inferred (photo) |
| Anchor (manifest) | **-122.4003340, 37.7888147** | OSM OBB centre shifted by the `tk.run` recentre |
| Model bbox | 68.5501 × 67.9062 × 100.6 m | validation.json |

## Orientation

Long axis 134° along Second Street. SW face = Second St; NW toward Stevenson/Market; SE toward Jessie St; NE party side.

## Recognition cues (ranked)

1. Warm beige granite with green-glass vertical window strips.
2. Strong cornice at the eleventh floor over a full-site podium.
3. Notched corners and two setbacks to a small crowned top.

## Simplified

- Finials/urns and masts on the crown omitted.
- Window strips drawn as punched panes.

## Uncertainties

- Published 100.6 m vs LiDAR roof plane 107.6 m: the model may sit ~7 m low against the LiDAR city mesh.
- Setback heights read from one upward-looking photo.
- Party faces not photographed.
