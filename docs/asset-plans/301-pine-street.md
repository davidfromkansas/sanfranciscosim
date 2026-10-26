# Pacific Coast Stock Exchange — SF-SIM asset plan

The former San Francisco Stock Exchange trading hall: a grey granite temple front on Pine Street, a deep colonnade of tall columns between two blank pylons over a broad flight of steps, with the exchange's name in the entablature and Ralph Stackpole's two monumental granite figure groups on pedestals before the pylons. The 12-storey Stock Exchange Tower (155 Sansome, separate artifact) stands against its south side.

**Deliverable:** `artifacts/301-pine-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `301-pine-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4013037, 37.7918447` (OSM OBB centre via `tk.run`) |
| Target height | **15.9 m** — DataSF 2010 LiDAR median roof 15.9 m of ring 201006.0002868 (measured; OSM height 16). The facts file's 32 m and the ring max 48 m come from the abutting 155 Sansome tower |
| Footprint | OSM way 256066230: OBB 25.4 × 40.2 m, 1018 m², long-axis bearing 171.4° |
| Triangle cap | 3,000 (building < 60 m; built: 1,226) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 15.9 m | measured (LiDAR median; majority 15.6) |
| Year / architects | 1915 Dyer; 1930 Miller & Pflueger remodel | published (Wikipedia) |
| Sculpture | two granite figure groups, Ralph Stackpole | published (Wikipedia) |
| Footprint | 40.2 × 25.4 m (along Pine × along Sansome), 1,018 m² | measured (OSM) |
| Columns | 8 between pylons, about 9.5 m tall | inferred (photo) / estimated |

### Sources

- OSM way 256066230 — https://www.openstreetmap.org/way/256066230
- Wikipedia — https://en.wikipedia.org/wiki/Pacific_Exchange
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor historical secured rolls (year built, storeys) — https://data.sf.gov/resource/wv5m-vpq2
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:Pacific_Exchange_301_Pine.jpg (Pine St front from the east)

### Orientation

Street grid: local +x = bearing 81.4° (east, toward Sansome), +y = north (Pine St front). South face abuts the 155 Sansome tower; west face is a party wall.

### What each side shows

- N (Pine): colonnade, steps, pylons with the two statue groups — photographed.
- E (Sansome): blank granite pylon return — photographed in part; rest **inferred** plain.
- S and W: party walls (no windows modelled).

### Recognition cues (ranked)

1. Colonnade of tall grey columns recessed between two blank pylons.
2. The two huge Stackpole figure groups flanking the steps.
3. Name band in the entablature; low flat granite block among towers.

### Massing recipe

- Hall prism with a 4.2 m colonnade recess on Pine, 0–13 m `Toy_stone`, base course.
- Eight tapered `Toy_white` columns on a three-step stair; tall lit windows on the recessed wall.
- Entablature with a dark name band; cornice; attic and parapet to 15.9 m; trading-hall skylight (lit) and low plant.
- Figure groups: pedestal + three blocky figures + heads on each side.

### Palette, roof, budget

- Palette: `Toy_stone`, `Toy_white`, `Toy_concrete`, `Toy_glassd`, `Toy_glassl`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`.
- Roof: Flat attic roof with a large lit skylight over the old trading floor and a small plant cluster.
- Budget: 1,226 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "301-pine-street", "file": "301-pine-street.glb", "anchor": [-122.4013037, 37.7918447], "targetHeightM": 15.9, "cat": 3, "name": "Pacific Coast Stock Exchange", "estimated": false, "dims": [48.0994, 36.0449, 15.9], "tris": 1226, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 256066230 from the
procedural bake, batch re-bake. 

### Open risks

- Column count and heights read from one photograph.
- Roof height uses the LiDAR median; the front attic may stand a little higher than the hall roof.
- Skylight is inferred from the trading-hall use, not photographed.
