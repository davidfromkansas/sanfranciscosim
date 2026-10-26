# Palace Hotel — reference dossier

2 New Montgomery Street at Market, San Francisco. Trowbridge & Livingston, opened 1909 on the site of the 1875 Palace; Garden Court SF Landmark 1969, whole building 1984.
Plan: `docs/asset-plans/palace-hotel.md`. Labels: **published**, **measured** (OSM / DataSF LiDAR),
**inferred** (read from a photo or the description), **estimated** (a modelling choice).

## Sources

- OSM relation 3492933 — https://www.openstreetmap.org/relation/3492933
- Wikipedia — https://en.wikipedia.org/wiki/Palace_Hotel,_San_Francisco
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (Wikidata P18) — https://commons.wikimedia.org/wiki/File:Palace_Hotel_from_1_Montgomery_St._roof_garden.JPG (Market × New Montgomery corner)

## Dimensions and location

- Anchor `-122.4019446, 37.7879687` (OSM OBB centre, `tk.run` recentre).
- Footprint: OSM relation 3492933 (multipolygon outer ring), OBB 102.7 × 78.6 m, 8028 m², bearing 134.7° (measured).
- Height **40.0 m** — DataSF 2010 LiDAR majority 40.0 m of ring 201006.0000105 (measured; median 37.0, max 50.2). Wikipedia gives 35 m; the LiDAR roof surface is used because the lead asked for LiDAR heights and 9 storeys + cornice fit 38–40 m.


## Orientation

Plan on the 134.7° grid: local +x = SE along New Montgomery, +y = NE. Market St = NW face (local −x), New Montgomery = NE face (+y); Jessie St SE, Annie St SW.

## Recognition cues (ranked)

1. Huge block-filling nine-storey hotel, tan brick over a pale stone base.
2. Deep cornice over a row of round-headed windows.
3. Lit Garden Court glass roof in the middle of the roof.

## Simplified

- Rustication, balconies and the corner flagpoles omitted; light courts drawn on the roof rather than cut.

## Uncertainties

- LiDAR majority (40 m) vs published 35 m: the crest may be ~5 m high if the published figure is the true roof.
- Light courts and the Garden Court's exact size are estimated; the hotel actually has several deep light courts.
- `Toy_granite` stands in for the tan brick.
