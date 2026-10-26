# 350 Mission Street (Salesforce East) — reference dossier

Checked 2026-10-25 for the Transbay landmark batch. Labels: **published** (Wikipedia /
CTBUH / owner), **measured** (OSM geometry), **inferred** (read from the photograph),
**estimated** (a modelling choice).

## Sources

- [OpenStreetMap way 226514310](https://www.openstreetmap.org/way/226514310): footprint (5 nodes, 1,459 m², OBB 39.4 × 37.2 m, bearing 135.0°, `height=129`, `building:levels=27`).
- [Wikipedia — 350 Mission Street](https://en.wikipedia.org/wiki/350_Mission_Street): 30 floors, SOM, 2015, roof 424 ft, location ("northeast corner of Fremont Street and Mission Street"), neighbours.
- [CTBUH building 2929](https://www.skyscrapercenter.com/building/350-mission/2929) (cited by the infobox).
- [Commons — Salesforce East 2021.jpg](https://commons.wikimedia.org/wiki/File:Salesforce_East_2021.jpg): the Wikipedia lead photo, from the Mission × Fremont corner; the review was done against it.
- [DataSF footprints / 2010 LiDAR](https://data.sf.gov/resource/ynuv-fyni): **no usable record** — the survey predates the tower.

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Roof / crest | **129.0 m** | published (424 ft) |
| Footprint | 39.4 × 37.2 m (model 38.5 × 36.5 m wall line) | measured (OSM OBB) |
| Lobby height | 17 m | estimated (photo: about four office storeys) |
| Floors / year / architect | 30 / 2015 / SOM | published |
| Anchor (manifest) | **-122.3967200, 37.7908720** | measured: OSM OBB centre; `tk.run` recentre shift 0 |

## Orientation

Yaw −45° (OSM bearing 135°). +Y = true north. Faces: **SE = Mission St**, **SW = Fremont
St**, NE toward 45 Fremont / the Blue Shield building, NW toward the alley side.
Salesforce Tower stands across both streets to the SSW, Salesforce West across
Fremont, Millennium Tower across Mission.

## Recognition cues (ranked)

1. Compact, almost cubic blue glass prism.
2. Tall, light, see-through lobby that lifts the shaft.
3. Canted "pixel" glass panels — shown as two-tone blue banding with fins.
4. Salesforce cloud on the shaft near the corner; LED media wall in the lobby.

## Preserved

- 129 m crest, OSM footprint and heading, the lobby/shaft proportion.
- Cloud on the Mission face near the Fremont corner, as in the photo.

## Simplified

- Canted panels → 25 storey-groups of alternating `Toy_glass` / `Toy_glassl` bands + fins.
- LED media wall (inside the lobby) → a sky-blue screen on the Mission lobby face with a
  `Toy_sky_Glow` quad, because opaque toy glass would hide an interior wall.
- Roof → glass crown screen around a deck and plant cluster.

## Uncertainties

- Lobby height and the LED wall's face (Mission) are inferred.
- OSM says 27 levels vs 30 published (height unaffected).
- NE/NW faces are not photographed; assumed to repeat the skin.
