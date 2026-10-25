# PG&E General Office Building Annex — reference dossier

Checked 2026-10-25 for the Financial District landmark batch. Labels: **published**
(Wikipedia / Wikidata / assessor), **measured** (OSM geometry, DataSF 2010 LiDAR), **inferred**
(read from the photograph or description), **estimated** (a modelling choice).
Plan: `docs/asset-plans/pge-annex.md`.

## Sources

- OSM way 260291406 — https://www.openstreetmap.org/way/260291406
- Wikipedia — https://en.wikipedia.org/wiki/Pacific_Gas_and_Electric_Company_General_Office_Building_and_Annex
- Commons photo of the main building (annex not visible) — https://commons.wikimedia.org/wiki/File:Pacific_Gas_and_Electric_Co._General_Office_Building_full_view.JPG
- DataSF 2010 LiDAR rings 201006.0003729 / 0000848 / 0000581 (all mblr SF3711014A) — https://data.sf.gov/resource/ynuv-fyni
- Lead's existing landmark: artifacts/pge-general-office/ and docs/asset-plans/pge-general-office.md

## Verified dimensions and location

| Item | Value | Basis |
|---|---|---|
| Crest | 55.8 m | measured (LiDAR ring max); consistent with 13 storeys |
| Storeys | 13 | OSM `building:levels` |
| Year / architects | 1945 / Bakewell & Brown (designed to match the 1925 building) | published (Wikipedia, NRHP) |
| Footprint | 42.2 × 40.9 m, 1,715 m² | measured (OSM) |
| Cladding, base, cornice | match the general office | inferred (NRHP text), not photographed |
| Anchor (manifest) | **-122.3965063, 37.7921155** | OSM OBB centre shifted by the `tk.run` recentre |
| Model bbox | 65.7542 × 65.3062 × 55.8 m | validation.json |

## Orientation

Plan rotated 45° like the general office. NW face = party wall with the 1925 tower (no windows modelled); SW = Beale Street; SE toward 77 Beale's plaza; NE toward the Matson annex.

## Recognition cues (ranked)

1. Same cream terracotta and arcaded base as the general office, a storey-height lower block behind it.
2. Terracotta cornice and balustrade with a set-back attic.
3. Punched-window grid at the general office's storey pitch.

## Simplified

- Ornament and pilasters omitted; all exposed faces share one treatment.

## Uncertainties

- **No photograph of the annex**: every facade is inferred from "designed to match". If the annex is plainer (likely for 1945), the arcade and balustrade overstate it.
- Height rests on one LiDAR ring statistic (max 55.8 m); the ring is small and its median (18.9 m) shows it also covers low structures.
- OSM footprint touches the general office's footprint along the NW face (≈0.5 m overlap).
