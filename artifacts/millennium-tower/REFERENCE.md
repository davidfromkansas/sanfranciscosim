# Millennium Tower — reference dossier

Checked 2026-10-25 (Transbay landmark batch). Labels: **published**, **measured**,
**inferred** (from photographs), **estimated** (modelling choice).

## Sources

- [OpenStreetMap way 72963089](https://www.openstreetmap.org/way/72963089) — footprint (12 nodes, 1,481 m², OBB 47.9 × 33.1 m, long axis 135.5°), `height=197`, `building:levels=58`.
- [DataSF building footprints + 2010 LiDAR](https://data.sf.gov/resource/ynuv-fyni), `sf16_bldgid` 201006.0001788 (MBLR SF3719020) — height above ground max 194.91 m, majority 184.31 m, median 175.88 m.
- [Wikipedia — Millennium Tower (San Francisco)](https://en.wikipedia.org/wiki/Millennium_Tower_(San_Francisco)) — 645 ft, 58 floors, Handel Architects, 2009, residential (via the batch facts sheet; a re-fetch this session was rate-limited).
- Wikipedia lead photograph (Commons, [category](https://commons.wikimedia.org/wiki/Category:Millennium_Tower_(San_Francisco))) — upward view of a long face and an end: deep-blue glass, fine white vertical mullions, and the mullions stepping down at the top (the terraced crown).

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Crest | **197.0 m** | published 645 ft (196.6 m), rounded as in the batch facts |
| Upper roof region | ~184 m | measured (LiDAR majority) |
| Plan | 46 × 30 m rounded rectangle | OSM OBB (measured), simplified |
| Anchor | **-122.3961910, 37.7904150** | measured (OSM OBB centre via `tk.run`) |

## Orientation

Long axis 135.5° (NW–SE, along Fremont St). Mission St frontage = NW end; Fremont
= SW long face. +Y = true north.

## Recognition cues (ranked)

1. Deep-blue glass column pinstriped by white vertical mullions.
2. The terraced top stepping down along the long axis.
3. The long, round-ended plan.
4. A pale screen on the top tier.

## Preserved

- 197 m crest, OSM heading and proportions, four-tier terraced top, white pinstripes
  (fins every 3 m), glazed lobby with a canopy.

## Simplified

- Irregular OSM plan → one rounded rectangle; tiers shortened from one end only.
- Storeys grouped into ~6 m bands; balconies/terrace railings omitted.
- The tower's settlement and tilt are not modelled (the asset is plumb).

## Uncertainties

- The direction the terraces step toward (modelled: down toward the NW / Mission end)
  is inferred from one photo; an aerial would settle it.
- Tier heights (171 / 179 / 187 / 193.5 m) are estimated; the LiDAR majority of 184 m
  suggests the stepped region sits a little lower than modelled.
- The 2010 LiDAR max (194.9 m) is below the published 197 m; the thin screen top and
  settlement are plausible reasons. The published value drives the crest.
