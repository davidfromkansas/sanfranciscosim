# Mills Building — SF-SIM asset plan

The city's second skyscraper (1892), a ten-storey Chicago-school block with Romanesque detail on the Montgomery × Bush corner: a two-storey white marble base with the great round entrance arch on Montgomery, a buff-brick shaft whose middle storeys form an arcade of tall engaged colonnettes ending in round arches, an ornamental frieze, an attic storey and a heavy cornice. Two light courts open the roof. The 1931 Mills Tower annex (`artifacts/220-bush-street/`, a separate landmark) stands against its whole east wall.

**Deliverable:** `artifacts/mills-building/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `mills-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4018804, 37.7913406` (OSM OBB centre via `tk.run`) |
| Target height | **47.0 m** — published 47 m (Wikipedia text; infobox roof 46.94 m). DataSF 2010 LiDAR: majority 43.65 m, median 44.8 m = the roof deck inside the cornice/parapet (measured) |
| Footprint | OSM relation 3492808 (multipolygon outer ring): OBB 85.9 × 48.0 m, 3811 m², long-axis bearing 81.1° |
| Triangle cap | 3,000 (building < 60 m; built: 2,929) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (top of parapet) | 47.0 m | published (Wikipedia 47 m; infobox 46.94 m) |
| Roof deck | 43.7–44.8 m | measured (LiDAR footprint 201006.0000960: majority 43.65, median 44.8, 9,540 cells) |
| Storeys / year / architect | 10 / 1892 / Burnham & Root | published (Wikipedia; OSM `building:levels=10`) |
| Footprint | OBB 85.9 × 48.0 m, outer ring 3,812 m² less two light courts (407 + 260 m²) | measured (OSM relation 3492808) |
| East wall | party wall with Mills Tower (220 Bush St, 92 m) along its full length | measured (the OSM rings share the edge) |
| Base / shaft materials | white marble two-storey base, buff brick and terracotta shaft | published + photo |
| Storey pitch above the base | 4.175 m (8 storeys from 10.4 to 43.8 m) | estimated |
| Main entrance | round Romanesque arch, Montgomery St | photo (HABS); centred on the face — inferred |

### Sources

- OSM relation 3492808 — https://www.openstreetmap.org/relation/3492808
- Wikipedia — https://en.wikipedia.org/wiki/Mills_Building_and_Tower
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni (footprint 201006.0000960)
- DataSF assessor roll — https://data.sf.gov/resource/wv5m-vpq2.json (220 Bush parcel: 1930, 22 st = the tower)
- Commons photo (HABS, Wikipedia article) — https://commons.wikimedia.org/wiki/File:Mills_Building_(San_Francisco).jpg (Montgomery × Bush corner, from above)

### Orientation

Plan is the OSM ring itself in metres (+x east, +y north). Bush St edge runs at bearing 81° (outward normal 171°, the **S** face); Montgomery St edge at 351° (normal 261°, the **W** face); the **N** face looks over lower Pine St buildings; the **E** face is the Mills Tower party wall. +Y = true north.

### What each side shows

- S (Bush) and W (Montgomery): marble base, brick arcade with colonnettes and round arches, frieze, attic, cornice — photographed.
- W (Montgomery): the cream entrance surround and round arch, mid-face (photo shows the arch; exact bay inferred).
- N: plain punched brick windows above the neighbours (**inferred**, not photographed); no arcade.
- E: blank party wall, entirely covered by Mills Tower — nothing projects past it (cornice, bands and sidewalk are clipped 2–8 cm short of the shared edge).

### Recognition cues (ranked)

1. A broad ten-storey palazzo block with a white base, buff shaft and heavy cornice on the corner of Montgomery and Bush.
2. The arcade: tall colonnettes rising to a row of round arches on both street faces.
3. The great round entrance arch on Montgomery.
4. Paired with the taller buff Mills Tower rising directly behind it to the east.
5. Two dark light courts in the roof (aerial).

### Massing recipe

- Plan: `tk.ccw` of the OSM outer ring, clipped 8 cm west of the Mills Tower party line.
- 0–10.4 m `Toy_white` marble base with storefront and second-floor panes (lit storefronts at night); `Toy_cream` belt course.
- 10.4–43.8 m `Toy_terracotta` shaft, eight storeys of 4.175 m; panes every 3.6 m on S/W/N.
- Arcade on S and W: `Toy_stone` colonnettes every 3.6 m from storey 4 to the arches; round-headed `Toy_glassd` arches in storey 8.
- `Toy_cream` frieze band, attic band, two-step cornice at 43.8–45.4 m; `Toy_terracotta` parapet to 47.0 m.
- Montgomery entrance: `Toy_cream` surround 9 m wide × 11.4 m with a dark round arch and a lit inner arch.
- Roof: dark deck at 45.5 m, the two light courts as `Toy_ink` wells with brick coping, a low plant cluster and stair house.
- Sidewalk on Bush and Montgomery only, two street trees on Montgomery.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_terracotta`, `Toy_cream`, `Toy_stone`, `Toy_glassd`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_leaf`/`Toy_leafd`/`Toy_rust` (trees); glow `Toy_sand_Glow`.
- Roof: Dark deck inside the parapet, the two light courts as dark wells with coping, one low plant cluster and a stair house; all under 47 m.
- Budget: 2,929 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "mills-building", "file": "mills-building.glb", "anchor": [-122.4018804, 37.7913406], "targetHeightM": 47.0, "cat": 3, "name": "Mills Building", "estimated": false, "dims": [95.6553, 60.2391, 47.0], "tris": 2929, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM relation 3492808 (multipolygon outer ring) from the
procedural bake, batch re-bake. Sits against `220-bush-street` (Mills Tower): the two GLBs share the party line without overlapping; check in-app that neither procedural mass is double-baked there.

### Open risks

- N face not photographed; window rhythm assumed.
- Colonnettes run the full length of both street faces; the real corner pavilions have plain punched windows instead (simplified).
- Light courts modelled as dark wells at roof level; their real depth/skylights unknown.
- Mills Tower's model uses an OBB rectangle, so a few centimetres of gap may show along the party line in-app.
