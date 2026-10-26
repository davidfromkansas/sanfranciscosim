# The Montgomery — SF-SIM asset plan

An eight-storey classical block built for the San Francisco Call after the 1906 fire: a charcoal-grey base (tall shop floor, mezzanine, banded rusticated third storey), four storeys of cream fluted Corinthian giant pilasters, a deep modillioned cornice and a cream attic of small windows. In the miniature it is the long grey-and-cream colonnaded block on Jessie.

**Deliverable:** `artifacts/74-new-montgomery-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `74-new-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4013268, 37.7874752` (OSM OBB centre via `tk.run`) |
| Target height | **32.7 m** — LiDAR median roof 32.7 m (DataSF 2010, parcel 3707064); OSM 33 m; mode 33.2 m |
| Footprint | OSM way 79377217: OBB 82.1 × 21.3 m, 1747 m², long-axis bearing 45° |
| Triangle cap | 3,000 (building < 60 m; built: 2,068) |
| Category | `2` (Apartments — `CAT.apartments` (107 condominiums since 2005) in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Completed / architect | 1914 / Reid Brothers | published (Wikipedia) |
| Storeys | 8 (condo unit numbers run to 8xx; photo) | published (assessor) / photo |
| Roof | 32.7 m median, 33.2 m mode, 37.3 m max (rooftop palms/plant) | measured (DataSF LiDAR) |
| Footprint | OSM rectangle 82.1 × 21.3 m, 1,747 m², long axis bearing 45° | measured (OSM) |
| Frontages | NE = New Montgomery (5 bays), NW = Jessie (long front) | measured (OSM centrelines) + photo |
| Floor lines 6.0 / 10.2 / 14.6 / 28.0 / 29.6 m |  | inferred (photo) |

### Sources

- OSM way 79377217 — https://www.openstreetmap.org/way/79377217
- Wikipedia — https://en.wikipedia.org/wiki/The_Montgomery_(San_Francisco)
- Wikidata — https://www.wikidata.org/wiki/Q7752115
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- DataSF assessor secured roll 2023 — https://data.sf.gov/resource/wv5m-vpq2
- OSM street centrelines via Nominatim (frontage check) — https://nominatim.openstreetmap.org/
- Commons photo — https://commons.wikimedia.org/wiki/File:The_Montgomery,_San_Francisco.jpg (2012, the New Montgomery/Jessie corner)

### Orientation

Local +x = bearing 45° (parallel to Market), +y = 315°. The NE end (+x) is the 21 m New Montgomery front, the NW side (+y) the 82 m Jessie front; SE and SW are back walls.

### What each side shows

- NE (New Montgomery) and NW (Jessie): grey base, cream pilasters, cornice, attic — photographed.
- SE and SW: plain cream upper walls over the grey base (**inferred**).

### Recognition cues (ranked)

1. Two-tone: dark grey rusticated base under a cream colonnaded body.
2. Giant fluted pilasters with capitals across four storeys.
3. Deep cornice with a low attic storey above it.

### Massing recipe

- Rectangle 82 × 21.3 m at yaw 45°.
- Base 0–14.6 m `Toy_steel`: shop panes (lit), mezzanine and third-storey panes, five rustication bands.
- Body 14.6–29.6 m `Toy_cream` punched block (4 storeys of 3.35 m) with 1.1 m pilasters + capitals on the two street faces every 4.1 m.
- Cornice (1.25 m out) at 28 m, attic with small windows, top cornice, cream parapet to 32.7 m.

### Palette, roof, budget

- Palette: `Toy_cream`, `Toy_steel`, `Toy_glassl`, `Toy_glassd`, `Toy_roofd`; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark deck inside a 0.8 m cream parapet, one low plant cluster; the photo's rooftop palms are omitted.
- Budget: 2,068 triangles against the 3,000 cap (validated with `--budget 3000`).

### Draft manifest entry

```json
{"id": "74-new-montgomery-street", "file": "74-new-montgomery-street.glb", "anchor": [-122.4013268, 37.7874752], "targetHeightM": 32.7, "cat": 2, "name": "The Montgomery", "estimated": false, "dims": [79.9738, 79.9738, 32.7], "tris": 2068, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 79377217 from the
procedural bake, batch re-bake. 

### Open risks

- Back (SE/SW) walls not photographed.
- Real base is darker than `Toy_steel`; chosen so it does not read black in the miniature.
- Rooftop terrace planting omitted to keep the crest at the roofline.
