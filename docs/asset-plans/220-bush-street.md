# Mills Tower (220 Bush Street) — SF-SIM asset plan

The 22-storey 1931 annex (Lewis P. Hobart) behind the 1892 Burnham & Root Mills Building: a thin north–south slab in buff brick and terracotta matched to the older block, window strips between piers, round-arched top storeys under a cornice. NRHP / SF Landmark 76 with the Mills Building.

**Deliverable:** `artifacts/220-bush-street/` (build script, GLB, validate/render wrappers, renders, REFERENCE.md, REPORT.md).

| | |
|---|---|
| Manifest id | `220-bush-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4013027, 37.7914191` (OSM way 256066232 OBB centre, recentred by `tk.run`) |
| Target height | **92 m** — published (Wikipedia infobox roof 92 m); LiDAR roof 93.1 m majority |
| Footprint | OSM way 256066232: OBB 43.1 x 13.7 m, 589 m², 4 nodes, long axis 171° (N–S) |
| Triangle cap | 5,000 (built: 2,226) |
| Category | `3` (office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 92 m | published (Wikipedia infobox) |
| Floors / year / architect | 22 / 1931 / Lewis P. Hobart | published |
| Mills Building (west neighbour) | 10 storeys, 46.94 m | published |
| Footprint | OBB 43.1 x 13.7 m | measured (OSM) |
| LiDAR ring 201006.0004820 | majority 93.1 m, max 95.8 m | measured (DataSF) |

### Sources

- OSM way 256066232 — https://www.openstreetmap.org/way/256066232
- Wikipedia, Mills Building and Tower — https://en.wikipedia.org/wiki/Mills_Building_and_Tower
- Commons photo, Mills Building wide.jpg — https://commons.wikimedia.org/wiki/File:Mills_Building_wide.jpg
- DataSF LiDAR ring 201006.0004820 — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Local +X = bearing 171° (south). **Bush St = S face (13.5 m)**; the long E face looks toward Sansome over lower buildings; the long W face is against the Mills Building up to 47 m; N face toward Pine.

### What each side shows

- S (Bush): stone base with the entrance portal, then the strip facade.
- E and N: same strips (inferred from the distant photo).
- W: blank to 47 m (Mills Building), strips above.

### Recognition cues (ranked)

1. Thin buff slab rising behind the Mills Building.
2. Vertical window strips.
3. Arched top storeys and cornice.
4. Stepped penthouse.

### Massing recipe

- Terracotta prism; dark full-height window strips (`tk.panes`, 2.65 m) with a proud spandrel band each storey.
- Base 0–6.5 m stone with shop panes and a portal on Bush.
- Attic 82.5–88.8 m arched windows (lit), cornice, parapet, penthouse to 92 m with a lit band.

### Palette

`Toy_terracotta`, `Toy_cream`, `Toy_stone`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`.

### Roof

Parapet, a terracotta penthouse with a cornice cap and a lit band, plant on the north end.

### Triangle budget

2,226 tris (body 1,568, night_glow 658) against a cap of 5,000.

### Draft manifest entry

```json
{"id": "220-bush-street", "file": "220-bush-street.glb", "anchor": [-122.4013027, 37.7914191], "targetHeightM": 92.0, "cat": 3, "name": "Mills Tower (220 Bush Street)", "estimated": false, "dims": [25.6872, 50.3996, 92.0], "tris": 2226, "loadRadius": 2760}
```

### Integration notes

Case B. The Mills Building (10 storeys) shares the block; exclude only this way (radius ≈ 23 m along the slab, not the older building).

### Open risks

- Only a distant photo of the tower; E/N facade detail inferred.
- Penthouse form simplified.
