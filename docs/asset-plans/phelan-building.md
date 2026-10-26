# Phelan Building — SF-SIM asset plan

An eleven-storey flatiron at the meeting of Market, O'Farrell and Grant, clad in cream glazed terra cotta: a dark shopfront storey, a tall cream shaft of closely spaced windows, a top storey of arched windows, a deep cornice and balustrade, and a rounded prow at the eastern tip. A low arcaded wing continues the Market frontage at the west end.

**Deliverable:** `artifacts/phelan-building/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `phelan-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4054628, 37.7863863` (OSM OBB centre via `tk.run`) |
| Target height | **47.0 m** — DataSF 2010 LiDAR median 47.0 m of ring 201006.0000308 (measured; the ring, 4,620 m², also covers lower neighbours — majority 21.7, max 56.3). OSM height 42 (survey) is lower; 11 storeys published |
| Footprint | OSM relation 1547962 (multipolygon outer ring): OBB 92.6 × 62.4 m, 2883 m², long-axis bearing 81.4° |
| Triangle cap | 3,000 (building < 60 m; built: 2,748) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (balustrade) | 47.0 m | measured (LiDAR median of a merged ring) |
| Storeys / year / architect | 11 / 1908 / William Curlett | published (Wikipedia, Wikidata) |
| Cladding | cream glazed terra cotta, metal windows | published (Wikipedia) |
| Footprint | OSM relation 1547962 outer ring, 92.6 × 62.4 m OBB, 2,883 m², rounded east prow | measured (OSM) |
| Low arcaded west wing (x < −30 m local) |  | inferred (photo shows a low arched block at the west end) |

### Sources

- OSM relation 1547962 — https://www.openstreetmap.org/relation/1547962
- Wikipedia — https://en.wikipedia.org/wiki/Phelan_Building
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:Phelan_Building_in_San_Francisco.JPG (from Central Tower, prow and both faces)

### Orientation

Street grid: local +x = bearing 81.4° (east, toward the prow), +y = north. O'Farrell St = north face, Market St = the long SE diagonal, rounded prow at Grant/O'Farrell/Market.

### What each side shows

- Market and O'Farrell faces and the prow: photographed — dark shop storey, cream shaft, arched top storey, cornice, balustrade.
- West end: wall of the tall block above a low arcaded wing (wing form **inferred** from the photo's far end).

### Recognition cues (ranked)

1. Cream terra-cotta flatiron with a rounded prow on Market.
2. Arched top storey under a deep cornice and balustrade.
3. Dark shopfront base.

### Massing recipe

- Tall block = OSM ring east of x = −30 m (prow thinned to 5 nodes); `Toy_ink` shop storey 0–5.2 m with lit shopfronts.
- 5.8–40 m `Toy_cream` punched shaft (9 storeys of 3.8 m, panes 3.1 m apart; west face unwindowed where the wing covers it).
- Frieze, arched top storey 40.6–44.2 m, trim cornice band, balustrade to 47 m; dark deck, small penthouse and plant.
- West wing: 11 m cream block with arched panes on the Market side.

### Palette, roof, budget

- Palette: `Toy_cream`, `Toy_trim`, `Toy_ink`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_concrete`; glow `Toy_sand_Glow`.
- Roof: Dark deck inside the balustrade with a small cream penthouse and a low plant cluster.
- Budget: 2,748 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "phelan-building", "file": "phelan-building.glb", "anchor": [-122.4054628, 37.7863863], "targetHeightM": 47.0, "cat": 3, "name": "Phelan Building", "estimated": false, "dims": [96.6113, 82.16, 47.0], "tris": 2748, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM relation 1547962 (multipolygon outer ring) from the
procedural bake, batch re-bake. 

### Open risks

- Height from a LiDAR ring that merges neighbours; OSM says 42 m. 11 storeys at ~4 m supports 44–47 m.
- West wing's extent and height are inferred; OSM maps it inside the same outer ring.
- The building's projecting bay windows are not modelled.
