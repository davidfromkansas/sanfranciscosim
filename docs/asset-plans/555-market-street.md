# 555 Market Street (Market Center) — SF-SIM asset plan

The shorter of the two Market Center towers (Hertzka & Knowles, 1964; Standard Oil Building No. 3, later Chevron's headquarters): a 22-storey slab of white precast panels in tight vertical ribs over a granite base, sharing a landscaped plaza with 575 Market. In the miniature it is the crisp white pinstriped slab on Market.

**Deliverable:** `artifacts/555-market-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `555-market-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3999542, 37.7899805` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **94.8 m** — published roof 94.79 m (Wikipedia); DataSF LiDAR majority 96.4 m, max 96.8 m (parapet/plant) |
| Footprint | OSM way 32946577: OBB 42.8 × 26.5 m, 1,127 m², bearing 45.1° (along Market); modelled as a 42.6 × 26.4 m rectangle |
| Triangle cap | 5,000 (built: 3,580) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 94.79 m | published (Wikipedia) |
| LiDAR | majority 96.4 m, max 96.8 m | measured (DataSF 2010) |
| Floors / year / architect | 22 / 1964 / Hertzka & Knowles | published |
| Cladding | precast terracotta panels over a granite base | published (Wikipedia) |
| Footprint | 42.8 × 26.5 m, bearing 45.1° | measured (OSM) |
| Rib spacing 1.6 m, base 7 m |  | estimated |

### Sources

- OSM way 32946577 — https://www.openstreetmap.org/way/32946577
- Wikipedia — https://en.wikipedia.org/wiki/Market_Center_(San_Francisco)
- Commons lead photo (not retrievable during the batch, HTTP 429) — https://commons.wikimedia.org/wiki/File:555-575_Market_Street.jpg
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Yaw 44.9° (long axis bearing 45.1°, along Market). +Y = true north. NW face = Market St; SE face toward Stevenson / Jessie; SW end toward the shared plaza and 575 Market; NE end toward 2nd St neighbours.

### What each side shows

- NW (Market) and SE: the long white ribbed faces.
- SW: faces the Market Center plaza (a strip of plaza with trees is modelled).
- All faces assumed alike (**inferred**: no photo was retrieved).

### Recognition cues (ranked)

1. Bright white vertical pinstripe over dark glass.
2. Plain flat top with a white attic band.
3. Granite base with recessed lobby; plaza shared with the taller 575 Market.

### Massing recipe

- Plan `tk.rect(42.6, 26.4)` on yaw 44.9°.
- 0–7 m dark lobby set 1.5 m in, granite piers every 5.3 m, granite fascia to 8 m.
- 8–91 m `tk.shaft`, 21 storeys, `Toy_glassd` with thin `Toy_white` bands and white ribs every 1.6 m; lit panes per rib bay.
- 91–94.8 m white attic ring, roof deck, white penthouse and plant; white light line.
- Granite apron, stone plaza strip and four trees on the SW.

### Palette

`Toy_white`, `Toy_glassd`, `Toy_granite`, `Toy_stone`, `Toy_roofd`, `Toy_steel`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.

### Roof

White attic band hides a dark deck with a white penthouse block and a small plant cluster.

### Triangle budget

3,580 tris (body 2,568, night glow 1,012) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "555-market-street", "file": "555-market-street.glb", "anchor": [-122.3999542, 37.7899805], "targetHeightM": 94.8, "cat": 3, "name": "555 Market Street (Market Center)", "estimated": false, "dims": [62.1833, 62.1261, 94.8], "tris": 3580, "loadRadius": 2844}
```

### Integration notes

Case B. 575 Market (taller twin) stands across the plaza to the SW; keep the exclusion to this footprint (~22 m) so 575 survives. loadRadius 2,844 m.

### Open risks

- No photograph was retrieved (Commons rate-limited); the skin follows the Wikipedia description and is otherwise **inferred**.
- OSM footprint (1,127 m²) is about half the DataSF parcel footprint (2,046 m²); the extra may be the plaza podium.
- Rib spacing and base height are estimates.
