# Four Seasons Hotel and Residences (757 Market Street) — SF-SIM asset plan

The Four Seasons hotel-and-condominium development on Market Street between 3rd and 4th (Millennium Partners, 2001): a 40-level tower on the Market Street half of the block over a broad podium of hotel, club and shops that runs back to Yerba Buena Lane. No photograph could be retrieved, so the skin is modelled from the general description; massing and height come from OSM and LiDAR. In the miniature it is the pale tower on Market with a wide low podium behind.

**Deliverable:** `artifacts/757-market-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `757-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4042447, 37.7862212` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **130.1 m** — DataSF 2010 LiDAR max 130.07 m over the site (measured crest; the survey postdates the 2001 tower); tower roof 121 m from OSM `building:part` (40 levels). No published height found |
| Footprint | OSM way 149332498 (whole site): 14 nodes, 5,074 m², OBB 85 × 67 m, bearing 135.1°; tower = OSM `building:part` way 435591307 (9 nodes) on the Market (NW) half |
| Triangle cap | 5,000 (built: 4,738) |
| Category | `7` (Hotel — `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest | 130.1 m | measured (LiDAR max 130.07 m) |
| Tower roof | 121 m, 40 levels | OSM building:part 435591307 |
| Podium | 28.7 m | measured (LiDAR median 28.69 m; OSM height=29) |
| Site footprint | 5,074 m², bearing 135.1° | measured (OSM) |
| Note: per-building facts file gave lidarH 79.4 m | superseded by the DataSF record (max 130.07 m) | measured |
| Skin: pale stone, punched windows; crown screen |  | estimated (no photo) |

### Sources

- OSM way 149332498 — https://www.openstreetmap.org/way/149332498
- OSM building:part 435591307 — https://www.openstreetmap.org/way/435591307
- DataSF footprints / 2010 LiDAR (record SF3706127) — https://data.sf.gov/resource/ynuv-fyni
- Four Seasons — https://www.fourseasons.com/sanfrancisco/ (OSM `website` tag)
- No Commons/Wikipedia photo retrieved (HTTP 429 throughout the batch)

### Orientation

Footprints used directly; site long axis bearing 135.1°, Market St along the NW edge (bearing ~45°). The tower occupies the NW (Market) half; the podium runs SE to Yerba Buena Lane / Mission St side.

### What each side shows

- NW (Market): tower and podium face the street (position measured; skin **inferred**).
- SE: podium roof with a garden and plant; the tower's back face (**inferred**).
- NE/SW: podium walls against neighbours (721–735 Market, the Contemporary Jewish Museum area).

### Recognition cues (ranked)

1. A tall pale tower set right on Market.
2. Broad low podium filling the rest of the block.
3. Set-back crown screen with a light line.

### Massing recipe

- Site = OSM way 149332498, tower = building:part 435591307, both `tk.ccw`.
- Podium: 0–6 m shopfront base, 6–28.7 m `punched_block` (`Toy_sand`, 4 bands, 5.5 m panes), parapet, roof garden and plant.
- Tower: 29.7–121 m `punched_block` (`Toy_sand`, 23 bands, `Toy_glass` panes every 4.8 m), cornice.
- Crown: ring screen inset 4 m to 130.1 m round the roof, white light line.

### Palette

`Toy_sand`, `Toy_stone`, `Toy_glass`, `Toy_glassd`, `Toy_roofd`, `Toy_leafd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### Roof

Tower: a stone mechanical screen ring to the LiDAR crest over a dark deck. Podium: dark roof with a green garden patch and a plant cluster.

### Triangle budget

4,738 tris (body 3,848, night glow 890) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "757-market-street", "file": "757-market-street.glb", "anchor": [-122.4042447, 37.7862212], "targetHeightM": 130.1, "cat": 7, "name": "Four Seasons Hotel and Residences (757 Market Street)", "estimated": false, "dims": [108.8653, 109.8358, 130.1], "tris": 4738, "loadRadius": 3903}
```

### Integration notes

Case B; category 7 (hotel; residences above). The site way covers the whole podium (5,074 m²) — clear only this way, ~55 m from the anchor at the corners, and check that 721–735 Market and the Contemporary Jewish Museum (way 118106934) survive. loadRadius 3,903 m.

### Open risks

- **No photo**: facade materials, window pattern and crown form are estimates; only massing and heights are measured.
- Crest 130.1 m is the LiDAR maximum and may include a rooftop mast; the 121 m roof is from OSM.
- The facts file's lidarH (79.4 m) disagreed with the DataSF record; the record was used.
