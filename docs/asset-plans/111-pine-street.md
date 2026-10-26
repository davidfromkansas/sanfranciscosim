# 111 Pine Street — SF-SIM asset plan

A 19-storey 1963 office slab on the south side of Pine Street between Front and Battery, next to One Front Street: a flat grey precast grid of punched windows divided into tall bays by dark recessed piers, on a polished red-brown granite base with arched bank entrances (First Republic Bank), finished by a slatted top storey. The list's facts file carried no name; the address and assessor roll identify it.

**Deliverable:** `artifacts/111-pine-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `111-pine-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3989068, 37.7921569` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **76.0 m** — DataSF 2010 LiDAR roof plane: ring 201006.0002437 median 76.07 m, majority 75.99 m (measured). The facts file's 105.9 m and the ring max 135.7 m are spill from One Front Street next door; OSM `height=84` is unsourced |
| Footprint | OSM way 148710880: 5 nodes (one near-collinear node dropped), 1,201 m², OBB 43.2 × 27.9 m, bearing 81.3° |
| Triangle cap | 5,000 (built: 4,548) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof / crest | 76.0 m | measured (LiDAR median/majority plane) |
| Year / storeys / use | 1963 / 19 / office | published (DataSF assessor roll, block 0266 lot 001) |
| Footprint | 43.2 × 27.9 m, 1,201 m² | measured (OSM) |
| Granite base 2 storeys ≈ 8 m |  | inferred (photo) |
| Bay rhythm: 6 bays of 3 windows on the Pine face |  | inferred (photo) |
| Architect | not found | — |

### Sources

- OSM way 148710880 — https://www.openstreetmap.org/way/148710880 (address node 3661035833 `111 Pine Street`)
- Commons photo — https://commons.wikimedia.org/wiki/File:111_Pine_Street,_San_Francisco,_CA.jpg (Pine St face, street level)
- DataSF 2010 LiDAR ring 201006.0002437 (mblr SF0266001) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): 1963, 19 storeys, commercial office
- Nominatim reverse geocode (101/111 Pine Street, 94111)

### Orientation

Footprint used directly (long axis 81.3°). North face = Pine St (the photographed front); east toward Front St and One Front Street; south toward Market's back lots.

### What each side shows

- North (Pine): precast grid, dark piers, granite base with arched entrances (photo).
- East/west ends and south: same grid **inferred** (ends are partly party walls).

### Recognition cues (ranked)

1. Flat grey punched-window grid split into tall bays by dark piers.
2. Polished red-brown granite base with round-arched openings.
3. Slatted (louvred) top storey under a flat roof.
4. Plain rectangular slab beside the much taller One Front Street.

### Massing recipe

- 0–8 m `Toy_granite` base, round-arched `Toy_glassd` openings at 7.2 m with `Toy_sand_Glow` behind; `Toy_ink` fascia.
- 8–70 m `tk.punched_block`: 17 storeys of 3.65 m, `Toy_concrete` wall, `Toy_glassd` panes at 2.4 m; `Toy_ink` piers every 7.2 m, 0.08 m proud (thin enough that the lit panes stay in front).
- 70–73.8 m louvred top storey: `Toy_steel` slats at 2.4 m, white crown line.
- Coping, dark deck, low plant cluster to 76.0 m.

### Palette

`Toy_concrete`, `Toy_granite`, `Toy_ink`, `Toy_glassd`, `Toy_steel`, `Toy_roofd`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_white_Glow`. Off-palette: `Toy_concrete`, `Toy_granite` (documented).

### Roof

Dark deck inside a concrete coping with a tidy cluster of low plant boxes.

### Triangle budget

4,548 tris (body 3,776, night glow 772) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "111-pine-street", "file": "111-pine-street.glb", "anchor": [-122.3989068, 37.7921569], "targetHeightM": 76.0, "cat": 3, "name": "111 Pine Street", "estimated": false, "dims": [52.4675, 39.6667, 76.0], "tris": 4548, "loadRadius": 2500}
```

### Integration notes

Case B. Exclusion radius ~22 m; One Front Street (way 148710877) abuts to the east and must survive, as must way 148710883 (a separate building to the west). loadRadius 2,500 m.

### Open risks

- Height comes from LiDAR only; the facts-file 105.9 m was rejected as neighbour spill.
- No published architect or name; the building is anonymous apart from its address.
- Concrete reads beige-grey; the real precast is a cooler grey-brown.
