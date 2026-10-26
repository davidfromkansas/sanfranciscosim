# San Francisco Marriott Marquis — SF-SIM asset plan

A 39-storey postmodern hotel tower at 4th and Mission that Herb Caen likened to a jukebox. The light precast tower is cross-shaped, its wings stepping down in ziggurat terraces each capped by a glass greenhouse storey and marked by a fan-shaped glass window; dark glass slots run up the re-entrant corners and the core ends in a glass crown under a big glass barrel vault with fan-shaped ends (the View lounge). It rises from a six-storey podium that fills the site from 4th St to Jessie Square.

**Deliverable:** `artifacts/marriott-marquis/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `marriott-marquis` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4044800, 37.7853374` (OSM OBB centre via `tk.run`) |
| Target height | **133.0 m** — published 132.89 m / 133 m (Wikipedia infobox / text; OSM `height=133`). DataSF 2010 LiDAR max 128.14 m over the whole complex (measured, the vault top is thin) |
| Footprint | OSM relation 6483285 (multipolygon outer ring): OBB 160.1 × 75.2 m, 8871 m², long-axis bearing 135.1° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,820) |
| Category | `7` (Hotel — `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (top of the crown vault) | 133.0 m | published (Wikipedia 132.89 m; OSM 133; OSM tower part says 137) |
| LiDAR | max 128.14 m, median 31.2 m, majority 23.6 m | measured (footprint 201006.0000099, 33,043 cells) |
| Podium roof | 23.6 m (6 storeys) | measured (LiDAR majority; OSM building:part `building:levels=6`) |
| Storeys / year / rooms | 39 / 1989 / 1,362 + 137 suites | published (Wikipedia) |
| Site | OBB 160.1 × 75.2 m, 8,874 m² less a 349 m² podium court | measured (OSM relation 6483285) |
| Tower plan | cross of two 20–22 m wide slabs, ~64 × 58 m overall, hub at the meeting of the OSM tower-part arms | inferred (OSM building:part 436648569 + photos) |
| Wing terrace heights | SW wing 5 steps (104–55 m), others 2 steps (110–89 m), core 116.6 m | estimated from the two photos |

### Sources

- OSM relation 6483285 — https://www.openstreetmap.org/relation/6483285 (and building:parts 436648569, 616813832–5)
- Wikipedia — https://en.wikipedia.org/wiki/San_Francisco_Marriott_Marquis
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni (footprint 201006.0000099)
- Commons photo (infobox, from Yerba Buena Gardens, SE) — https://commons.wikimedia.org/wiki/File:2017_San_Francisco_Marriott_Marquis_Hotel_from_Yerba_Buena_Gardens.jpg
- Commons photo (crown from Market St, NW) — https://commons.wikimedia.org/wiki/File:2017_Marriott_Marquis_San_Francisco_from_Market_Street_top.jpg

### Orientation

Street grid: local +u = bearing 45° (NE, along Mission St), +w = 315° (NW, toward Market). SW face = 4th St, SE face = Mission St, NE = Jessie Square / Contemporary Jewish Museum, the narrow NW tail reaches toward Market. The tower hub sits about 22 m into the site from its centre toward Mission. +Y = true north.

### What each side shows

- SE (Mission / Yerba Buena Gardens): core face with the vault's fan end, SW wing stepping down at left with fan windows — photographed.
- NW (Market): the vault's other fan end over the core, stepped wings to both sides — photographed (crown only).
- SW (4th St) and NE (Jessie Square): wing ends with fan windows and terrace glass boxes (**inferred** from the same vocabulary).
- Podium: six storeys of precast with lit lobby frontage on 4th, Mission and Jessie Square (**inferred**; photos show only its top behind trees).

### Recognition cues (ranked)

1. The jukebox crown: a glass barrel vault with fan-shaped arched ends on top of a glass crown box.
2. Light stone tower with wings stepping down in terraces, each topped by a glass greenhouse storey.
3. Fan-shaped glass windows on the terrace faces.
4. Dark glass slots up the re-entrant corners.
5. Broad six-storey podium filling the 4th St block.

### Massing recipe

- Podium: `tk.ccw` of the OSM outer ring, `Toy_sand`, 0–23.6 m; dark deck; the podium court as an `Toy_ink` well; panes and a lit lobby band on the 4th, Mission and Jessie Square faces.
- Tower hub 20 × 22 m, `Toy_stone`, 23.6–116.6 m (30 storeys of 3.1 m) on yaw = bearing 45°.
- Four wings: SW 5 terraces (26/22/18/14/10 storeys), NE (28/24), NW (27/23), SE (26/21); each terrace a stone prism whose top storey is an inset `Toy_glassg` greenhouse box.
- Fan windows (`Toy_glassg`, narrow foot, semicircular head, ~7 m wide × 9 m) on every terrace end face, with a smaller `Toy_sky_Glow` fan over each.
- `Toy_glassd` 2.2 m slots up the four re-entrant corners.
- Crown: `Toy_glassg` box 116.6–124.6 m with a white lit band; glass barrel vault (r 8.4 m, axis NW–SE) to 133.0 m with white-lit fan ends.
- Punched `Toy_glassd` windows one per 5 m per storey on every exposed stone face; scattered lit panes.
- Plant cluster on the podium roof, sidewalk on 4th and Mission, three street trees on 4th.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_sand`, `Toy_glassg`, `Toy_glassd`, `Toy_glassl`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, trees; glow `Toy_sand_Glow`, `Toy_sky_Glow`, `Toy_white_Glow`.
- Roof: Glass greenhouse tops on every terrace, the glass crown and vault on the hub, dark podium deck with a plant cluster and the court well.
- Budget: 4,820 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "marriott-marquis", "file": "marriott-marquis.glb", "anchor": [-122.40448, 37.7853374], "targetHeightM": 133.0, "cat": 7, "name": "San Francisco Marriott Marquis", "estimated": false, "dims": [149.4689, 157.2098, 133.0], "tris": 4820, "loadRadius": 3990}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM relation 6483285 (multipolygon outer ring) from the
procedural bake, batch re-bake. OSM building:parts 436648569 and 616813832–5 belong to this relation and must be excluded from the procedural bake too.

### Open risks

- Tower position and cross plan are inferred: OSM has no separate tower outline (its 39-level part is an irregular remainder of the podium parts), and DataSF LiDAR gives only footprint statistics. The hub was put where the OSM part's arms meet.
- Terrace counts and heights are read from two photos; only the SW wing's long stair is clearly photographed.
- Real tower has more facets (sub-slabs, rounded glass bays); simplified to a clean cross.
- Podium facades not photographed.
