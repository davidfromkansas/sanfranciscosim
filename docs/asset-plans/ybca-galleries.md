# Yerba Buena Center for the Arts — Galleries — SF-SIM asset plan

Fumihiko Maki's 1993 Galleries and Forum building: a long, low, precise box of silver-grey aluminium panels and tall glass walls on Mission Street. Toward the gardens a full-height glass wall is crossed by a broad diagonal aluminium band — the grand stair inside — and a thin canopy marks the entrance.

**Deliverable:** `artifacts/ybca-galleries/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `ybca-galleries` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4021445, 37.7855959` (OSM OBB centre via `tk.run`) |
| Target height | **17.3 m** — LiDAR max 17.3 m (DataSF 2010, parcel 3723115; median 10.3 m); the OSM '28 m' tag is rejected |
| Footprint | OSM way 24563073: OBB 87.7 × 71.1 m, 4017 m², long-axis bearing 135.1° |
| Triangle cap | 3,000 (building < 60 m; built: 1,222) |
| Category | `16` (Museum — `CAT.museum` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Opened / architect | 1993 / Fumihiko Maki | published (Wikipedia, Wikidata Q1884883) |
| Heights | median 10.3, mode 11.95, max 17.3 m | measured (DataSF LiDAR) |
| Footprint | OBB 87.7 × 71.1 m, 4,017 m², 19 nodes | measured (OSM) |
| Mission St frontage | NW edge ~12 m from the Mission centreline | measured (OSM) |
| Split into gallery block 12 m / forum wing 9 m / raised hall 17.3 m |  | estimated |

### Sources

- OSM way 24563073 — https://www.openstreetmap.org/way/24563073
- Wikipedia — https://en.wikipedia.org/wiki/Yerba_Buena_Center_for_the_Arts
- Wikidata — https://www.wikidata.org/wiki/Q1884883
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- OSM street centrelines via Nominatim (frontage check) — https://nominatim.openstreetmap.org/
- Commons photo — https://commons.wikimedia.org/wiki/File:Yerba_Buena_Center_for_the_Arts,_exterior,_from_Yerba_Buena_Gardens,_San_Francisco_(May_2013).jpg

### Orientation

Local +x = bearing 135.1° (SE, away from Mission), +y = 45.1° (NE). The gallery block lies along Mission (local −x); its SE face (local +x) and the forum wing face the gardens.

### What each side shows

- Gardens (SE) face of the gallery block: tall glass with the diagonal stair band — photographed.
- Forum wing NE face: entrance canopy — photographed in part.
- Mission (NW) and other faces: aluminium panels over a glazed ground storey (**inferred**).

### Recognition cues (ranked)

1. Low silver aluminium box with a strong diagonal band across a glass wall.
2. Thin flat entrance canopy.
3. A raised skylit hall above the gallery roof.

### Massing recipe

- Two masses from the 19-node OSM outline: gallery block (12 m) and forum wing (9 m), `Toy_steel` with white coping.
- Ground storey glazing (`Toy_glassd`) with lit panes, except on the shared wall.
- Gardens face: full-height `Toy_sky` glass panes (4.4–11.2 m) crossed by a white tube stair band rising from 2.2 to 10 m.
- Raised hall 24 × 32 m to 17.3 m with lit clerestory panes; white canopy; flat dark roofs, low plant.

### Palette, roof, budget

- Palette: `Toy_steel`, `Toy_white`, `Toy_sky`, `Toy_glassl`, `Toy_glassd`, `Toy_roofd`, `Toy_stone`; glow `Toy_sand_Glow`.
- Roof: Flat dark roofs with white coping; the raised hall's lit clerestory glows at night.
- Budget: 1,222 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "ybca-galleries", "file": "ybca-galleries.glb", "anchor": [-122.4021445, 37.7855959], "targetHeightM": 17.3, "cat": 16, "name": "Yerba Buena Center for the Arts \u2014 Galleries", "estimated": false, "dims": [83.8882, 113.4626, 17.3], "tris": 1222, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 24563073 from the
procedural bake, batch re-bake. 

### Open risks

- Only one photo (gardens side); massing split, hall position and the Mission front are inferred.
- The blue pattern in the photo is a temporary artwork on the glass, not modelled.
- The OSM height tag (28 m) disagrees with LiDAR (17.3 m max); LiDAR used.
