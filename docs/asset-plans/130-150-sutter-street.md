# Hallidie Building — SF-SIM asset plan

Willis Polk's seven-storey office building whose Sutter Street front is one of the first glass curtain walls in the US: a sheer grid of glass hung in front of the structure, framed in dark blue, laced with gilded cast-iron bands, flanked by stacked semicircular fire-escape balconies and crowned by a gilded cornice with a row of finials. In the miniature it is the blue-and-gold glass front on Sutter.

**Deliverable:** `artifacts/130-150-sutter-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `130-150-sutter-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4030681, 37.7902120` (OSM OBB centre via `tk.run`) |
| Target height | **30.3 m** — LiDAR median roof 30.3 m (DataSF 2010, parcel 0288027); OSM 30 m; the list's 34.2 m was a LiDAR peak |
| Footprint | OSM way 151195286: OBB 45.6 × 34.5 m, 1486 m², long-axis bearing 170.6° |
| Triangle cap | 3,000 (building < 60 m; built: 1,182) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Completed / architect | 1918 / Willis Polk | published (Wikipedia, NRHP) |
| Storeys | 7 (assessor: built 1917, 7 storeys) | published |
| Roof | 30.3 m median, 29.9 m mode, 38.1 m max | measured (DataSF LiDAR) |
| Footprint | OBB 45.6 × 34.5 m, 1,486 m² (lot 16,169 sq ft) | measured (OSM, assessor) |
| Sutter frontage on the SOUTH face | OSM centreline 7 m off the south edge | measured (OSM) |
| Floor lines of the glass front | 5.0 / 9.0 / 23.6 / 27.6 m | inferred (photo) |

### Sources

- OSM way 151195286 — https://www.openstreetmap.org/way/151195286
- Wikipedia — https://en.wikipedia.org/wiki/Hallidie_Building
- Wikidata — https://www.wikidata.org/wiki/Q5642964
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2
- OSM street centrelines via Nominatim (frontage check) — https://nominatim.openstreetmap.org/
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:Hallidie_Building_in_San_Francisco_dllu.jpg (2021, straight-on front)

### Orientation

The building stands on the north side of Sutter, so the glass front faces SOUTH (bearing 170.6°). The build authors it facing local +y with yaw for bearing 260.6°. East and west are party walls; the north side is the rear light court (the plan widens 2.4 m there).

### What each side shows

- S (Sutter): curtain wall, gilded bands, fire-escape balconies, cornice and finials — photographed.
- E and W: plain party walls (photo shows the upper east wall plain buff).
- N (rear court): plain wall with punched windows (**inferred**).

### Recognition cues (ranked)

1. Full-width glass grid in a dark-blue frame.
2. Gilded horizontal cast-iron bands and the gilded cornice cresting with finials.
3. Stacked semicircular fire-escape balconies at both ends of the front.

### Massing recipe

- Body: `Toy_sand` prism on the 6-node plan to 28.3 m, rear-court windows only.
- Front: `Toy_navy` frame slab 5.0–27.6 m with `Toy_glassl` panes on a 1.75 m grid (mezzanine, four office floors, top floor).
- Storefront: inset `Toy_glassd` with a warm lit band.
- Four `Toy_gold` bands, a navy cornice with gold cresting and 15 pyramid finials (centre one to 30.3 m).
- Eight gold cylinder balconies (two stacks of four) and gold side jambs.

### Palette, roof, budget

- Palette: `Toy_navy`, `Toy_glassl`, `Toy_gold`, `Toy_sand`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a sand parapet with a tidy plant cluster; a white light strip on the cornice at night.
- Budget: 1,182 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "130-150-sutter-street", "file": "130-150-sutter-street.glb", "anchor": [-122.4030681, 37.790212], "targetHeightM": 30.3, "cat": 3, "name": "Hallidie Building", "estimated": false, "dims": [47.1872, 55.7648, 30.3], "tris": 1182, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 151195286 from the
procedural bake, batch re-bake. 

### Open risks

- Popular accounts give the glass front a north exposure; the OSM Sutter centreline sits on the footprint's south edge, so it is modelled facing south — worth a glance at integration.
- Rear (north) court and its windows are not photographed.
- Finials and balconies are simplified solids.
