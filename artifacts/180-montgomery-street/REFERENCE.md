# 180 Montgomery Street (Bank of the West Building) — reference dossier

**Batch slug `180-montgomery-street` is mis-named:** the OSM footprint (way 132125163, no address tags) is 180 Montgomery Street, the Bank of the West Building (Booth Architects / Fee Munson Ebert, 1979, 25 storeys). DataSF assessor parcel 0289009 and the Wikipedia/CTBUH coordinates both fall on it. A plain beige precast-concrete box with deep horizontal ribbon windows between thick spandrels, a few broad piers per face and solid corners, at Montgomery × Bush.

Plan: `docs/asset-plans/180-montgomery-street.md`.

## Sources

- OSM way 132125163 — https://www.openstreetmap.org/way/132125163
- Wikipedia, 180 Montgomery Street — https://en.wikipedia.org/wiki/180_Montgomery_Street
- Wikipedia tallest list (row 78) / CTBUH — https://www.skyscrapercenter.com/building/180-montgomery-street/39286
- DataSF assessor roll (parcel 0289009) — https://data.sf.gov/resource/wv5m-vpq2.json
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni
- Commons photo — https://commons.wikimedia.org/wiki/File:180_Montgomery_St,_San_Francisco_(full_height).jpg

## Dimensions and location

- Anchor `-122.4020113, 37.7907470` (OSM OBB centre, shifted by the bbox recentre in `tk.run`).
- OSM way 132125163: OBB 37.7 × 41.2 m, 1,511 m², long-axis bearing 171.1°.
- Crest 109.8 m: published 109.8 m (CTBUH via the Wikipedia list; LiDAR roof majority 109.5 m, median 104.2 m).

## Orientation

Street grid, u = bearing 81°, v = 351°. Montgomery St = W face, Bush St = N face. Small notch at the NE corner (OSM).

## Recognition cues (ranked)

1. Strongly horizontal sandy precast grid.
2. Broad piers dividing each face into ~5 bays, solid corners.
3. Plain flat top with a set-back penthouse.

## Simplified

Panel joints and window mullions omitted; spandrels exaggerated in depth to read from the aerial camera.

## Uncertainties

- Slug/name mismatch: the lead should rename the manifest id (e.g. `180-montgomery-street`) or keep the slug with the corrected name.
- Penthouse size and position inferred; 109.8 m vs 98 m sources disagree (LiDAR supports ~109.5 m).
- Lobby height and piers inferred.
