# Salesforce Tower — reference dossier (v2)

v2 checked 2026-10-25 for the Transbay landmark batch. It reuses the v1 research
(2026-08-10) where it still holds and corrects it where the batch's sources or the
photographs disagree. Labels: **published** (architect / CTBUH / owner),
**measured** (OSM geometry, our own measurement), **inferred** (read from photographs),
**estimated** (a modelling choice).

## Sources

- [Pelli Clarke & Partners — Salesforce Tower](https://pcparch.com/work/salesforce-tower): architect, 1,070 ft height, tapered rounded plan, exterior sunshades.
- [CTBUH / Skyscraper Center — building 290](https://www.skyscrapercenter.com/building/building/290): architectural height 326 m, 61 floors, roof/architectural distinction.
- [Salesforce Tower — Artwork](https://salesforcetower.com/artwork/) and [Jim Campbell — Day for Night](https://www.jimcampbell.tv/portfolio/day-for-night): the six-floor, ~11,000-LED crown installation.
- [OpenStreetMap way 431972186](https://www.openstreetmap.org/way/431972186): the tower footprint used by the batch (82 nodes, 2,656 m², OBB 54.5 × 54.1 m, bearing 139.5°, `height=326`, `building:levels=61`). v1 cited way 119890395; the batch re-resolved the building and this is the way it uses.
- [Wikipedia — Salesforce Tower](https://en.wikipedia.org/wiki/Salesforce_Tower): cross-check of height, floors, completion (2018).
- Commons: [Salesforce Tower from Sacramento and Davis Street 2021](https://commons.wikimedia.org/wiki/File:Salesforce_Tower_from_Sacramento_and_Davis_Street_2021.jpg) and [Salesforce tower facing south](https://commons.wikimedia.org/wiki/File:Salesforce_tower_facing_south.jpg) — the two photos the v2 review was done against.
- DataSF building footprints / 2010 LiDAR: **no usable record** — the survey predates construction.

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Address | 415 Mission Street (Mission x Fremont x First) | published |
| Architectural height (crown rim) | **326.0 m** | published (CTBUH, architect) |
| Occupied roof | ~297 m | published CTBUH roof ≈ 296 m; model 297 m (estimated) |
| LED crown floors | top six floors, modelled 272–297 m | published (Campbell); heights estimated |
| Footprint across the flats | 54.5 × 54.1 m | measured (OSM OBB) |
| Plan at the crown rim | ~56% of the base width | inferred from photographs |
| Anchor (manifest) | **-122.3969300, 37.7897750** | measured: OSM OBB centre, shifted by the bbox recentre (`tk.run`) |
| Floors / completion / architect | 61 / 2018 / Pelli Clarke Pelli | published |

The v1 anchor (-122.3969271, 37.7897756, an OSM centroid) and the v2 anchor differ by
about 0.3 m — immaterial; v2 uses the batch convention (OBB centre).

## Orientation

The flats face **45° / 135° / 225° / 315°** (OSM OBB bearing 139.5°; model yaw 44.6°).
Blender +Y = true north, +X = east; the loader applies no rotation. Street sides:
**Mission St = NW face (315°)**, **Fremont St = NE face (45°)**, First St = SW face,
the Transit Center / Salesforce Park side = SE face. v1 moved its entrance cue to
canonical −Y for an older contract; v2 puts both entrances on their real faces.

## Recognition cues (ranked)

1. The **bullet silhouette**: a rounded square that tapers gently, then rolls in at the
   shoulders (~215 m) to a blunt, open top about half the base width. Not a point.
2. **Pale silvery skin**: light glass crossed by white horizontal sunshades. From any
   distance it reads as near-white, not blue (v1's dark `Toy_glass` read navy).
3. The **perforated white crown screen** above the roof, open at the top, with the LED
   floors and roof plant seen inside it from above.
4. **Night**: the LED crown glowing cool white over a warm, sparsely lit shaft.
5. Ground: tall glass lobby behind white piers, canopies on Mission and Fremont, the
   blue cloud sign by the Mission doors (semantically enlarged).

## Preserved

- 326 m crest, OSM footprint and heading; rounded-square plan; shoulder roll-in.
- Horizontal sunshade rhythm (one band per two real floors, 8.3 m pitch).
- Open crown with deck, plant, BMU and masts visible from the aerial camera.
- Both entrances on their real streets.

## Simplified

- 61 floors → ~34 white bands; fine fins and the mesh screen → 11 hoops + vertical ribs.
- LED artwork → one flat `Toy_white_Glow` skin (no imagery, no animation).
- Office lighting → hashed scattered panes (`Toy_sand_Glow`), stable per build.
- Plaza → a stone apron with four street trees; Transit Center and Salesforce Park are
  separate assets and are not in this GLB.

## Uncertainties

- The shoulder height (215 m) and crown-rim width (≈ 56%) are read from photographs;
  no published section was found.
- Roof height 297 m vs CTBUH ~296 m is within a band; the crest (326 m) is what the
  loader scales on and is exact.
- `Toy_glassg` (pale silvery glass) is off the core palette (a WARN, not a fail); it is
  the documented batch extra for this tower and Park Tower.

## v1 (2026-08)

v1 (20,086 tris, Blender 4.5) was a dark-blue tapered shaft closing to an ogive point,
with six broad crown hoops, a single entrance cue on −Y and its own render/validate
scripts. It was integrated in August 2026 as the manifest's `salesforce-tower`
(replacing the procedural `salesforceTower`). v2 keeps the id, file name and height;
see REPORT.md for what changed.
