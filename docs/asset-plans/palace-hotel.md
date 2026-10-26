# Palace Hotel — SF-SIM asset plan

The rebuilt Palace Hotel fills most of its block at Market and New Montgomery: plain and massive outside — a two-storey pale stone base with big shop and lobby windows, a tan brick shaft of regular punched windows framed by stone quoins, a top storey of round-headed windows and a deep cornice — with the glass-roofed Garden Court at its heart.

**Deliverable:** `artifacts/palace-hotel/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `palace-hotel` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4019446, 37.7879687` (OSM OBB centre via `tk.run`) |
| Target height | **40.0 m** — DataSF 2010 LiDAR majority 40.0 m of ring 201006.0000105 (measured; median 37.0, max 50.2). Wikipedia gives 35 m; the LiDAR roof surface is used because the lead asked for LiDAR heights and 9 storeys + cornice fit 38–40 m |
| Footprint | OSM relation 3492933 (multipolygon outer ring): OBB 102.7 × 78.6 m, 8028 m², long-axis bearing 134.7° |
| Triangle cap | 3,000 (building < 60 m; built: 2,220) |
| Category | `7` (Hotel — `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (parapet) | 40.0 m | measured (LiDAR majority) |
| Published height | 35 m | published (Wikipedia infobox) — not used |
| Storeys / opened / architects | 9 / 1909 / Trowbridge & Livingston | published (Wikipedia) |
| Footprint | OSM relation 3492933 outer ring, 102.8 × 78.6 m, 8,028 m² | measured (OSM) |
| Garden Court glass roof mid-block |  | published (Wikipedia); size and position estimated |

### Sources

- OSM relation 3492933 — https://www.openstreetmap.org/relation/3492933
- Wikipedia — https://en.wikipedia.org/wiki/Palace_Hotel,_San_Francisco
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (Wikidata P18) — https://commons.wikimedia.org/wiki/File:Palace_Hotel_from_1_Montgomery_St._roof_garden.JPG (Market × New Montgomery corner)

### Orientation

Plan on the 134.7° grid: local +x = SE along New Montgomery, +y = NE. Market St = NW face (local −x), New Montgomery = NE face (+y); Jessie St SE, Annie St SW.

### What each side shows

- Market and New Montgomery: stone base, brick shaft, quoins, arched top storey, cornice — photographed.
- Jessie and Annie faces: same treatment assumed (**inferred**).

### Recognition cues (ranked)

1. Huge block-filling nine-storey hotel, tan brick over a pale stone base.
2. Deep cornice over a row of round-headed windows.
3. Lit Garden Court glass roof in the middle of the roof.

### Massing recipe

- `tk.rect(102.8, 78.6)` on yaw from 134.7°; `Toy_stone` base 0–9 m with shop panes (lit).
- 9.7–31.6 m `Toy_granite` (tan) punched shaft, 6 storeys of 3.65 m, panes 4.6 m apart; stone corner quoins.
- Stone band; top storey 32.3–36.4 m with round-headed panes; 1.6 m cornice band; parapet to 40 m.
- Roof: dark deck, Garden Court (34 × 26 m) glass slab + `Toy_sand_Glow` cap with a stone rim, two dark light wells, a plant cluster on the Market side.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_granite` (tan brick), `Toy_glassd`, `Toy_glassl`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_concrete`; glow `Toy_sand_Glow`.
- Roof: Dark deck with the lit Garden Court skylight, two light wells and a plant cluster.
- Budget: 2,220 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "palace-hotel", "file": "palace-hotel.glb", "anchor": [-122.4019446, 37.7879687], "targetHeightM": 40.0, "cat": 7, "name": "Palace Hotel", "estimated": false, "dims": [136.8422, 136.663, 40.0], "tris": 2220, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM relation 3492933 (multipolygon outer ring) from the
procedural bake, batch re-bake. 

### Open risks

- LiDAR majority (40 m) vs published 35 m: the crest may be ~5 m high if the published figure is the true roof.
- Light courts and the Garden Court's exact size are estimated; the hotel actually has several deep light courts.
- `Toy_granite` stands in for the tan brick.
