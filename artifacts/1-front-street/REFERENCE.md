# One Front Street — reference dossier

1 Front Street (formerly 444 Market Street), San Francisco. Skidmore, Owings & Merrill, 1979; formerly Shaklee Terraces.
Plan: `docs/asset-plans/1-front-street.md`. Labels: **published**, **measured** (OSM / DataSF LiDAR),
**inferred** (read from a photo or the description), **estimated** (a modelling choice).

## Sources

- OSM way 148710877 — https://www.openstreetmap.org/way/148710877
- Wikipedia — https://en.wikipedia.org/wiki/One_Front_Street
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:Shaklee_Terraces.jpg (looking up the stepped corner)

## Dimensions and location

- Anchor `-122.3988578, 37.7917996` (OSM OBB centre, `tk.run` recentre).
- Footprint: OSM way 148710877, OBB 54.6 × 43.6 m, 1945 m², bearing 171.2° (measured).
- Height **164.0 m** — published roof 164 m (Wikipedia); LiDAR 158.06 m is the main roof, so the top 6 m is modelled as a white roof screen.


## Orientation

Street grid yaw: local +x = bearing 81.2°, +y = 351.2°; +Y = true north. West face = Front St; the SW chamfer = Front × Market corner; the four saw-tooth steps = Market St (SE); north and east faces are party walls toward the block.

## Recognition cues (ranked)

1. Alternating white spandrel and dark ribbon-window bands, roughly half and half.
2. Saw-tooth stepped Market corner (reads from above and from Market).
3. Flat white-screened top.

## Simplified

- Round-nosed spandrels → flat white bands; vertical mullions → 0.35 m gaps every ~6.5 m.
- Small rounding nodes of the saw-tooth dropped.

## Uncertainties

- Published 164 m vs LiDAR 158 m: the 6 m difference is modelled as a roof screen; its exact form is not photographed.
- The rounded spandrel noses are flat in the model.
- N and E elevations not photographed.
