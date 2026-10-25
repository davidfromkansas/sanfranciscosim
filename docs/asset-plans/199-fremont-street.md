# 199 Fremont Street — SF-SIM asset plan

A 27-storey office tower (KMD Architects, 2000) at Fremont and Howard, also addressed 300 Howard: pale granite with a regular grid of paired blue windows, a full-height blue glass slot at its corner and a stepped-back top behind a granite parapet. In the miniature it is the light stone tower among the glass of the Transbay district.

**Deliverable:** `artifacts/199-fremont-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `199-fremont-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.3948792, 37.7900023` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **110.9 m** — published roof 110.9 m (Wikipedia); DataSF LiDAR max 111.31 m agrees |
| Footprint | OSM way 192883913: 16 nodes, 2,063 m², OBB 57 × 40 m, bearing 133.9°; used as-is |
| Triangle cap | 5,000 (built: 4,814) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof | 110.9 m | published (Wikipedia); LiDAR 111.31 m |
| Floors / year / architect | 27 / 2000 / KMD Architects | published |
| Footprint | 57 × 40 m, bearing 133.9°, jogged south-east face | measured (OSM) |
| Top two storeys set back; glazed corner slot |  | inferred (photo) |

### Sources

- OSM way 192883913 — https://www.openstreetmap.org/way/192883913
- Wikipedia — https://en.wikipedia.org/wiki/199_Fremont_Street
- Commons photo — https://commons.wikimedia.org/wiki/File:199_Fremont_Street.jpg (2021)
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Footprint used directly; long axis bearing 133.9° (along Fremont). The long NE/SW faces run along Fremont and the block interior; the short NW/SE ends face Howard and the alley; the glass slot is placed on the west corner (**inferred** as the street corner).

### What each side shows

- Street faces: granite grid of paired windows over a tall glazed base (photo).
- West corner: full-height blue glass slot (photo shows one glazed corner; which corner is inferred).
- Other faces: same grid assumed (**inferred**).

### Recognition cues (ranked)

1. Pale granite tower with a crisp blue window grid.
2. Full-height glass corner slot.
3. Set-back top storeys behind a granite parapet.

### Massing recipe

- Plan = OSM polygon.
- 0–8 m granite base with tall blue storefront panes; band to 8.8 m.
- 8.8–102.6 m `punched_block` in `Toy_stone`, 24 storeys of 3.9 m, paired `Toy_glass` panes every 4.6 m.
- 4 × 4 m `Toy_glass` corner column at the west corner with its own lit panes.
- 102.6–108.3 m set-back glass storeys (49 × 31 m chamfered) with stone piers; parapet to 110.9 m round deck and plant.

### Palette

`Toy_stone`, `Toy_glass`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_white_Glow`. All core palette.

### Roof

Granite parapet with a white light line round a dark deck carrying an eight-box plant cluster.

### Triangle budget

4,814 tris (body 4,060, night glow 754) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "199-fremont-street", "file": "199-fremont-street.glb", "anchor": [-122.3948792, 37.7900023], "targetHeightM": 110.9, "cat": 3, "name": "199 Fremont Street", "estimated": false, "dims": [74.2273, 69.6048, 110.9], "tris": 4814, "loadRadius": 3327}
```

### Integration notes

Case B. Neighbours (181 Fremont landmark to the north-west, 201 Mission) are close: keep the exclusion to this footprint (~30 m radius) and confirm 181 Fremont's footprint is untouched. loadRadius 3,327 m.

### Open risks

- Which corner carries the glass slot is inferred; the photo shows one corner only.
- The real crown has small serrated steps; simplified to one set-back tier.
- The jogged south-east face is kept as mapped; it may be service bays.
