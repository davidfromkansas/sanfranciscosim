# Embarcadero Center West (275 Battery Street) — SF-SIM asset plan

A 30-storey 1989 John Portman office tower at Battery and Clay, built as Embarcadero West, the outlier of the Embarcadero Center group. Grey-green precast piers and dark glass wrap a near-square shaft whose corners are notched, and the notches deepen in steps at the top. In the miniature it is the dark ribbed tower with serrated corners west of the Embarcadero slabs.

**Deliverable:** `artifacts/embarcadero-center-west/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `embarcadero-center-west` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4004675, 37.7938599` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **123.1 m** — published roof 123.1 m (Wikipedia); DataSF LiDAR majority 120.1 m, max 126.9 m |
| Footprint | OSM way 32947500: OBB 41.2 × 36.4 m, 1,497 m², bearing 80.8°; modelled as a 40.6 × 36.0 m rectangle with 3 m corner notches |
| Triangle cap | 5,000 (built: 4,460) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 123.1 m | published (Wikipedia) |
| LiDAR | majority 120.1 m, max 126.9 m | measured (DataSF 2010) |
| Floors / year / architect | 30 (+3 below) / 1989 / John Portman & Associates | published |
| Footprint | 41.2 × 36.4 m, bearing 80.8° | measured (OSM) |
| Crown steps at 107 m and 115 m; corner notch 3 / 6 / 9 m |  | inferred (photo) / estimated |

### Sources

- OSM way 32947500 — https://www.openstreetmap.org/way/32947500
- Wikipedia — https://en.wikipedia.org/wiki/275_Battery_Street
- Commons photo — https://commons.wikimedia.org/wiki/File:Embarcadero_West.jpg (April 2021)
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Yaw 9.2° (bearing 80.8°, the north-of-Market grid). +Y = true north. West face = Battery St, south face = Clay St (inferred from the address and OSM), north and east toward Commercial St / the block interior.

### What each side shows

- All four faces carry the same pier-and-spandrel grid (photo shows two street faces).
- Every corner is notched; at the top the notches widen twice (photo).
- Base: rose granite with storefront glass (photo, street faces; other faces **inferred**).

### Recognition cues (ranked)

1. Dark, strongly ribbed shaft.
2. Notched, serrated corners running the full height.
3. Stepped crown where the notches deepen.
4. Rose granite base.

### Massing recipe

- Plan `tk.notch_rect(40.6, 36.0, 3.0)` on yaw 9.2°.
- 0–9 m granite base with storefront panes and warm lit ring.
- 9–107 m `tk.shaft`, 13 two-storey groups of `Toy_glassd` with `Toy_steel` bands and fins every 4 m; lit panes cut per storey.
- Crown: 107–115 m with 6 m notches, 115–121.4 m with 9 m notches, steel ledges at each step; parapet to 123.1 m round a deck and plant.

### Palette

`Toy_steel` (grey-green precast stand-in), `Toy_glassd`, `Toy_granite`, `Toy_roofd`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_white_Glow`. Off-palette: `glassd`, `granite`.

### Roof

Parapet round a dark deck with three plant boxes; the stepped notches read from above as a cross-shaped roof. White light line under the parapet.

### Triangle budget

4,460 tris (body 3,920, night glow 540) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "embarcadero-center-west", "file": "embarcadero-center-west.glb", "anchor": [-122.4004675, 37.7938599], "targetHeightM": 123.1, "cat": 3, "name": "Embarcadero Center West (275 Battery Street)", "estimated": false, "dims": [51.7243, 47.9189, 123.1], "tris": 4460, "loadRadius": 3693}
```

### Integration notes

Case B. Free-standing on its block corner; exclusion ~24 m radius clears only this footprint (check the low buildings on Commercial St survive). loadRadius 3,693 m.

### Open risks

- Precast colour is a grey-green in the photo; `Toy_steel` is a little bluer.
- Crown step heights are read from one upward photo.
- Street-face assignment (Battery west, Clay south) is inferred from the address.
