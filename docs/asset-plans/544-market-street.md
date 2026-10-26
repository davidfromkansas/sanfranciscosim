# Flatiron Building (540–544 Market Street) — SF-SIM asset plan

A ten-storey cream terracotta wedge (Havens & Toepke, 1913; SF Landmark 155) on the acute Market x Sutter corner: paired windows between tall piers, a stack of bay windows on the narrow prow, round-arched top-floor windows and a deep bracketed cornice.

**Deliverable:** `artifacts/544-market-street/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `544-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4007860, 37.7900167` (OSM way 132125158 OBB centre, recentred by `tk.run`) |
| Target height | **36.6 m** — published (Wikipedia/Emporis roof 36.58 m / 120 ft); LiDAR roof 38.1 m majority |
| Footprint | OSM way 132125158: wedge, 5 nodes, OBB 21.2 x 21.4 m, 293 m²; Market face 26 m, Sutter face 21 m, 6.5 m prow |
| Triangle cap | 3,000 (built: 1,358) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 36.58 m (120 ft) | published (Wikipedia infobox) |
| Floors / year / architect | 10 / 1913 / Havens & Toepke | published |
| Footprint | 5-node wedge, 293 m² | measured (OSM) |
| LiDAR ring 201006.0011147 | majority 38.1 m, max 42.2 m | measured (DataSF) |
| Bay stack on the prow, arched top floor, cornice |  | photo |

### Sources

- OSM way 132125158 — https://www.openstreetmap.org/way/132125158
- Wikipedia, Flatiron Building (San Francisco) — https://en.wikipedia.org/wiki/Flatiron_Building_(San_Francisco)
- Commons photo, Flatiron Building 540 Market St. San Francisco.jpeg — https://commons.wikimedia.org/wiki/File:Flatiron_Building_540_Market_St._San_Francisco.jpeg
- DataSF LiDAR ring 201006.0011147 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

True footprint used directly (`tk.ccw`). **Market = SE face** (two collinear edges, 26 m), **Sutter = N face** (21 m), the **prow faces E** (6.5 m) at the Market x Sutter point; the W edge is a party wall.

### What each side shows

- Market (SE) and Sutter (N): shopfronts, belt course, 8 floors of paired windows between piers, arched top floor.
- Prow (E): a full-height stack of bay windows.
- W: windowless party wall.

### Recognition cues (ranked)

1. The wedge plan and narrow prow.
2. Deep cornice over arched top windows.
3. Cream terracotta piers.
4. Prow bay stack.

### Massing recipe

- Terracotta prism on the OSM wedge; glass storefront panes with warm glow.
- `tk.panes` 2.2 m rhythm, piers in every other gap so no lit pane is covered.
- Prow: trapezoid bay prism 4.4 m wide, 1 m proud, with its own panes.
- Arched top floor, cornice 1.3 m proud, parapet to 36.6 m, roof stair house and small plant.

### Palette

`Toy_terracotta`, `Toy_cream`, `Toy_glassd`, `Toy_roofd`, `Toy_concrete`, `Toy_steel`, `Toy_stone`, trees; glow `Toy_sand_Glow`.

### Roof

Dark deck inside a parapet, a stair house and a three-box plant.

### Triangle budget

1,358 tris (body 1,130, night_glow 228) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "544-market-street", "file": "544-market-street.glb", "anchor": [-122.400786, 37.7900167], "targetHeightM": 36.6, "cat": 3, "name": "Flatiron Building (540\u2013544 Market Street)", "estimated": false, "dims": [27.2539, 32.456, 36.6], "tris": 1358, "loadRadius": 2500}
```

### Integration notes

Case B. Small (Market-side, load radius 2,500 m). Exclusion must stop at the party wall: radius ≈ 12 m.

### Open risks

- Published 36.6 m vs LiDAR roof 38.1 m: the model follows the published roof.
- Sutter-side detail inferred to match Market.
