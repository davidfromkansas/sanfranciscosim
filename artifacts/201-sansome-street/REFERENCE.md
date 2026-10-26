# Royal Insurance Building — reference dossier

201 Sansome Street (NW corner of Sansome and Pine), San Francisco. Howells & Stokes, 1907; SF Designated Landmark #160; now condominiums.
Plan: `docs/asset-plans/201-sansome-street.md`. Labels: **published**, **measured** (OSM / DataSF LiDAR),
**inferred** (read from a photo or the description), **estimated** (a modelling choice).

## Sources

- OSM way 256067738 — https://www.openstreetmap.org/way/256067738
- Wikipedia — https://en.wikipedia.org/wiki/Royal_Insurance_Building_(San_Francisco)
- Wikidata — https://www.wikidata.org/wiki/Q26001132
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo — https://commons.wikimedia.org/wiki/File:Royal_Insurance_Building,_SF_corner.JPG (the Sansome/Pine corner)

## Dimensions and location

- Anchor `-122.4012641, 37.7922609` (OSM OBB centre, `tk.run` recentre).
- Footprint: OSM way 256067738, OBB 27.7 × 20.5 m, 480 m², bearing 81.5° (measured).
- Height **41.3 m** — LiDAR median roof 41.3 m (DataSF 2010, parcel 0260017); OSM 41 m agrees; the list's 44.7 m was a higher LiDAR percentile.


## Orientation

Street grid yaw: local +x = bearing 81.5°, +y = 351.5°. East face = Sansome St (20.5 m, entrance and coat of arms), south face = Pine St (27.7 m); north and west are party walls, the NW notch a light court.

## Recognition cues (ranked)

1. Dark red brick shaft between a white marble base and a white terracotta top.
2. Deep white cornice with cartouches below it.
3. Coat of arms with clock over the Sansome entrance.

## Simplified

- Paired windows → single punched panes at 2.55 m; no window surrounds or balconies.
- Arms/clock reduced to a relief block and a disc.

## Uncertainties

- The LiDAR maximum (48 m) suggests a small rooftop structure not modelled.
- Brick tone is approximated by `Toy_rust` (the real brick is darker).
- Party-wall faces are given the street treatment.
