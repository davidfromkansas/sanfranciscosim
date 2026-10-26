# San Francisco Marriott Marquis — reference dossier

780 Mission Street / 55 Fourth Street (4th × Mission), San Francisco. Anthony J. Lumsden (DMJM) with Zeidler Partnership Architects, 1989.
Plan: `docs/asset-plans/marriott-marquis.md`. Labels: **published**, **measured** (OSM / DataSF LiDAR),
**inferred** (read from a photo or the description), **estimated** (a modelling choice).

## Sources

- OSM relation 6483285 — https://www.openstreetmap.org/relation/6483285 (and building:parts 436648569, 616813832–5)
- Wikipedia — https://en.wikipedia.org/wiki/San_Francisco_Marriott_Marquis
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni (footprint 201006.0000099)
- Commons photo (infobox, from Yerba Buena Gardens, SE) — https://commons.wikimedia.org/wiki/File:2017_San_Francisco_Marriott_Marquis_Hotel_from_Yerba_Buena_Gardens.jpg
- Commons photo (crown from Market St, NW) — https://commons.wikimedia.org/wiki/File:2017_Marriott_Marquis_San_Francisco_from_Market_Street_top.jpg

## Dimensions and location

- Anchor `-122.4044800, 37.7853374` (OSM OBB centre, `tk.run` recentre).
- Footprint: OSM relation 6483285 (multipolygon outer ring), OBB 160.1 × 75.2 m, 8871 m², bearing 135.1° (measured).
- Height **133.0 m** — published 132.89 m / 133 m (Wikipedia infobox / text; OSM `height=133`). DataSF 2010 LiDAR max 128.14 m over the whole complex (measured, the vault top is thin).


## Orientation

Street grid: local +u = bearing 45° (NE, along Mission St), +w = 315° (NW, toward Market). SW face = 4th St, SE face = Mission St, NE = Jessie Square / Contemporary Jewish Museum, the narrow NW tail reaches toward Market. The tower hub sits about 22 m into the site from its centre toward Mission. +Y = true north.

## Recognition cues (ranked)

1. The jukebox crown: a glass barrel vault with fan-shaped arched ends on top of a glass crown box.
2. Light stone tower with wings stepping down in terraces, each topped by a glass greenhouse storey.
3. Fan-shaped glass windows on the terrace faces.
4. Dark glass slots up the re-entrant corners.
5. Broad six-storey podium filling the 4th St block.

## Simplified

- Window pairs per bay → one pane per 5 m per storey (5,000-tri cap).
- Rounded glass bay towers and the second (perpendicular) fan hood on the crown omitted.

## Uncertainties

- Tower position and cross plan are inferred: OSM has no separate tower outline (its 39-level part is an irregular remainder of the podium parts), and DataSF LiDAR gives only footprint statistics. The hub was put where the OSM part's arms meet.
- Terrace counts and heights are read from two photos; only the SW wing's long stair is clearly photographed.
- Real tower has more facets (sub-slabs, rounded glass bays); simplified to a clean cross.
- Podium facades not photographed.
