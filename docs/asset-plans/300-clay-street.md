# One Maritime Plaza (Alcoa Building) — SF-SIM asset plan

A 27-storey SOM office slab of 1967 at 300 Clay Street, built for Alcoa: reflective bronze-tinted glass caged by an external lattice of bronze aluminium-clad steel X-braces, one of the earliest towers to show its seismic bracing on the outside. It rises from Maritime Plaza, a raised garden over a parking podium. In the miniature it is the dark tower wrapped in giant Xs at the foot of the Embarcadero Center slabs.

**Deliverable:** `artifacts/300-clay-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `300-clay-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3992506, 37.7956183` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **121.3 m** — published roof 121.3 m (Wikipedia); DataSF LiDAR max 120.98 m agrees |
| Footprint | OSM way 28240176: OBB 64.3 × 33.3 m, 2,117 m², bearing 171° (long axis N–S); modelled as a 63.6 × 32.6 m rectangle |
| Triangle cap | 5,000 (built: 4,622) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 121.3 m | published (Wikipedia); LiDAR 120.98 m |
| Floors / year / architect | 27 (25 office) / 1967 / Skidmore, Owings & Merrill | published |
| Footprint | 64.3 × 33.3 m, bearing 171° | measured (OSM) |
| Lattice: 4 X-bays on the long faces, 2 on the ends, ~7 tiers |  | inferred (photo) |
| Open base ~9 m at plaza level |  | estimated |

### Sources

- OSM way 28240176 — https://www.openstreetmap.org/way/28240176
- Wikipedia — https://en.wikipedia.org/wiki/One_Maritime_Plaza
- Commons photo — https://commons.wikimedia.org/wiki/File:2025-11-09_-_One_Maritime_Plaza_(FKA_Alcoa_Building)_in_San_Francisco_US.jpg (Nov 2025, aerial from the south-west)
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Yaw −81° (long axis bearing 171°). +Y = true north. Long faces east (toward Front St / the Embarcadero) and west (toward Battery); short ends north (Washington St side) and south (Clay St).

### What each side shows

- All four faces carry the bronze X lattice (photo shows a long face with 4 bays and an end with 2).
- Top: a louvred plant storey behind the lattice (dark band).
- Base: the tower stands on the Maritime Plaza garden deck; the parking podium below is a separate structure and only a strip of plaza is modelled.

### Recognition cues (ranked)

1. Giant dark X-brace lattice on every face.
2. Reflective glass slab with a plain flat top.
3. Garden plaza round the base.

### Massing recipe

- Plan `tk.rect(63.6, 32.6)` on yaw −81°.
- 0–9 m recessed dark lobby (3 m in) with warm lit ring.
- 9–118 m `tk.shaft`: 27 storeys of pale reflective `Toy_glassg` glass with `Toy_bronze` spandrels; lit panes every 5.3 m.
- Lattice 1.2 m proud: per face 4 (long) / 2 (end) bays × 7 tiers of X tubes (`tk.tube`, `Toy_ink`), bay columns, tier ties and 1.8 m corner columns to the ground.
- 118–121.3 m dark fascia (the louvred plant band), deck, plant; white light line.
- Stone plaza deck 9 m round the tower with two trees.

### Palette

`Toy_ink` (lattice), `Toy_glassg`, `Toy_bronze`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`, trees; glow `Toy_sand_Glow`, `Toy_white_Glow`. Off-palette: `glassg`, `bronze`, `glassd`.

### Roof

Flat dark deck with a plant cluster inside the fascia; white light line round the top at night.

### Triangle budget

4,622 tris (body 4,024, night glow 598) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "300-clay-street", "file": "300-clay-street.glb", "anchor": [-122.3992506, 37.7956183], "targetHeightM": 121.3, "cat": 3, "name": "One Maritime Plaza (Alcoa Building)", "estimated": false, "dims": [62.7108, 88.4797, 121.3], "tris": 4622, "loadRadius": 3639}
```

### Integration notes

Case B. The tower sits on the Maritime Plaza podium (OSM `layer=2`); the podium and garden belong to the surrounding ground/bake, so clear only this footprint (~36 m radius from the anchor reaches the long-axis ends) and check the plaza is not cut. loadRadius 3,639 m.

### Open risks

- The real lattice starts lower and has more members; tier count read from one photo.
- Base height above street is uncertain because the plaza is raised; the model sits at ground with a 0.6 m plaza deck.
- Lit panes sit behind the lattice; all glow faces still pass the outward test.
