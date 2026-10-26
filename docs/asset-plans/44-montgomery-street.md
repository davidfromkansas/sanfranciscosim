# 44 Montgomery Street — SF-SIM asset plan

A 43-storey office slab that was the tallest building west of Dallas when it opened. Its whole skin is a dense comb of slender white vertical fins over dark glass, running unbroken from the lobby to a crisp flat top where the fins stand proud like teeth. A second, lower slab steps back to the east along Sutter.

**Deliverable:** `artifacts/44-montgomery-street/` (Financial District batch, stages 1–2, BATCH mode).

| | |
|---|---|
| Manifest id | `44-montgomery-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4017708, 37.7896280` (OSM OBB centre via `tk.run`) |
| Target height | **172.2 m** — published roof 172.2 m (Wikipedia); antenna 180.7 m not modelled. LiDAR 90.12 m is unusable for this ring |
| Footprint | OSM way 32963370: OBB 56.6 × 82 m, 2432 m², long-axis bearing 80.9° |
| Triangle cap | 5,000 (tower ≥ 60 m; built: 4,806) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 172.2 m (antenna 180.7 m) | published (Wikipedia infobox) |
| Floors / year / architect | 43 / 1967 / John Graham & Co. | published |
| Footprint | OBB 56.6 × 82 m, 2,432 m², 18 nodes (L-shaped) | measured (OSM) |
| LiDAR | 90.12 m | measured but rejected (ring does not match the tower) |
| East slab height 150.6 m |  | inferred (photo: a few storeys lower) |

### Sources

- OSM way 32963370 — https://www.openstreetmap.org/way/32963370
- Wikipedia — https://en.wikipedia.org/wiki/44_Montgomery
- DataSF building footprints + 2010 LiDAR heights — https://data.sf.gov/resource/ynuv-fyni
- Commons photo (infobox) — https://commons.wikimedia.org/wiki/File:44_Montgomery.jpg (from Market St, Hobart Building at right)

### Orientation

Street grid yaw: local +x = bearing 80.9°, +y = 350.9°. West face = Montgomery St; north = Sutter St; the main slab runs N–S along Montgomery (82 × 19–24 m); the lower east slab (30 × 20.5 m) lines Sutter.

### What each side shows

- W (Montgomery): the long white comb face — photographed.
- S (toward Market): narrow dark-looking end — photographed.
- N (Sutter) and E: same comb (**inferred**); east slab height inferred from the photo.

### Recognition cues (ranked)

1. Unbroken comb of thin white fins over dark glass.
2. Fin tips projecting above a flat roof.
3. Main slab with a lower stepped-back second slab.

### Massing recipe

- Two slabs on the OSM L: main (6-node) to 172.2 m, east to 150.6 m.
- Each: inset dark glass lobby 0–9 m with lit ring, `Toy_glassd` body, `Toy_white` fins 0.45 × 0.65 m every ~1.65 m from the pavement to 1.6 m above the roof deck.
- Night: lit panes on two-storey bands (7.6 m) laid 0.75 m out, over the fins.

### Palette, roof, budget

- Palette: `Toy_white`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`.
- Roof: Dark decks inside the ring of fin tips, low plant clusters; white crown line on the main slab.
- Budget: 4,806 triangles against the 5,000 cap (validated with `--budget 5000`).

### Draft manifest entry

```json
{"id": "44-montgomery-street", "file": "44-montgomery-street.glb", "anchor": [-122.4017708, 37.789628], "targetHeightM": 172.2, "cat": 3, "name": "44 Montgomery Street", "estimated": false, "dims": [63.5031, 96.3661, 172.2], "tris": 4806, "loadRadius": 5166}
```

### Integration notes

Case B: registry entry in `pipeline/lib/landmarks.mjs`, exclusion of OSM way 32963370 from the
procedural bake, batch re-bake. 

### Open risks

- Which part of the L carries full height is read from one photo; the east slab's 150.6 m is inferred.
- LiDAR (90 m) disagrees wildly with the published height; ignored.
- Antenna (180.7 m) omitted so the crest equals the roof.
