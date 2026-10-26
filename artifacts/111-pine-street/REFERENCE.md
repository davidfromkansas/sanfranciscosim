# 111 Pine Street — reference dossier

Checked 2026-10-25 for the Financial District landmark batch. Labels: **published**
(Wikipedia / Wikidata / assessor), **measured** (OSM geometry, DataSF 2010 LiDAR), **inferred**
(read from the photograph or description), **estimated** (a modelling choice).
Plan: `docs/asset-plans/111-pine-street.md`.

## Sources

- OSM way 148710880 — https://www.openstreetmap.org/way/148710880 (address node 3661035833 `111 Pine Street`)
- Commons photo — https://commons.wikimedia.org/wiki/File:111_Pine_Street,_San_Francisco,_CA.jpg (Pine St face, street level)
- DataSF 2010 LiDAR ring 201006.0002437 (mblr SF0266001) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): 1963, 19 storeys, commercial office
- Nominatim reverse geocode (101/111 Pine Street, 94111)

## Verified dimensions and location

| Item | Value | Basis |
|---|---|---|
| Roof / crest | 76.0 m | measured (LiDAR median/majority plane) |
| Year / storeys / use | 1963 / 19 / office | published (DataSF assessor roll, block 0266 lot 001) |
| Footprint | 43.2 × 27.9 m, 1,201 m² | measured (OSM) |
| Granite base 2 storeys ≈ 8 m |  | inferred (photo) |
| Bay rhythm: 6 bays of 3 windows on the Pine face |  | inferred (photo) |
| Architect | not found | — |
| Anchor (manifest) | **-122.3989068, 37.7921569** | OSM OBB centre shifted by the `tk.run` recentre |
| Model bbox | 52.4675 × 39.6667 × 76.0 m | validation.json |

## Orientation

Footprint used directly (long axis 81.3°). North face = Pine St (the photographed front); east toward Front St and One Front Street; south toward Market's back lots.

## Recognition cues (ranked)

1. Flat grey punched-window grid split into tall bays by dark piers.
2. Polished red-brown granite base with round-arched openings.
3. Slatted (louvred) top storey under a flat roof.
4. Plain rectangular slab beside the much taller One Front Street.

## Simplified

- Window spacing 2.4 m (real ≈1.6 m); pier/bay alignment approximate.
- Bank awnings and signage omitted.

## Uncertainties

- Height comes from LiDAR only; the facts-file 105.9 m was rejected as neighbour spill.
- No published architect or name; the building is anonymous apart from its address.
- Concrete reads beige-grey; the real precast is a cooler grey-brown.
