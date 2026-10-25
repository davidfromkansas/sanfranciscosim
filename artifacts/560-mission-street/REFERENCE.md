# JPMorgan Chase Building (560 Mission Street) — reference dossier

Checked 2026-10-25 for the Financial District landmark batch. Labels: **published** (Wikipedia),
**measured** (OSM geometry / DataSF LiDAR), **inferred** (read from the photograph), **estimated** (a modelling choice).

## Sources

- OSM way 79377216 — https://www.openstreetmap.org/way/79377216 (footprint, tags: `height=128`, `building:levels=30`)
- Wikipedia — https://en.wikipedia.org/wiki/JPMorgan_Chase_Building_(San_Francisco)
- Commons photo (the Wikipedia lead photo, from a neighbouring tower looking down at the plaza side) — https://commons.wikimedia.org/wiki/File:560_Mission_Street,_San_Francisco.jpg
- DataSF 2010 LiDAR building heights — https://data.sf.gov/resource/ynuv-fyni (`hgt_max` 127.81 m)

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Crest | **128.02 m** | 128.02 m crest (published, Wikipedia); LiDAR 127.81 m agrees |
| Footprint | OBB 54.9 x 37.9 m, 2,035 m² | measured (OSM way 79377216) |
| Anchor (manifest) | **-122.3995478, 37.7888279** | OSM OBB centre -122.3994826, 37.7887773 shifted by the `tk.run` recentre |
| Height | 128.02 m | published (Wikipedia); LiDAR 127.81, OSM 128 |
| Floors / year / architect | 31 / 2002 / Cesar Pelli & Associates | published |
| Plaza | bamboo, maples, a pool and Rickey's 'Annular Eclipse' | published |
| Base 9 m, ledge ~46 m, roof deck 122 m, open frame to 128 m |  | inferred (photo) |
| Plaza on the NW (Mission) side, ~16 m deep |  | inferred (photo) / estimated depth |

## Orientation

Yaw -44.3 deg (OSM bearing 134.3): local +x faces SE, +y faces NE. The building stands on the south side of Mission, so the NW short face fronts **Mission St**, with the plaza between tower and street (photo shows 71 Stevenson across Mission beyond it; **inferred**).

## Recognition cues (ranked)

1. Black steel grid over pale glass.
2. Open steel frame crown above the roof.
3. Columned base and the plaza ring sculpture.

## Simplified

- Per-floor mullion grid -> ink bands every storey and fins every 4.1 m.
- Plaza planting -> three trees and a pool.

## Uncertainties

- Plaza side and ledge height are inferred.
- The plaza apron enlarges the bbox; the anchor shifts ~8 m to keep it centred (tk.run handles this).
