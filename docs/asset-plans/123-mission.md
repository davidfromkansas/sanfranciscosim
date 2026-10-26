# 123 Mission Street — SF-SIM asset plan

SOM's 1986 tower on the south side of Mission between Spear and Main: 29 storeys of warm
cream stone with a dense grid of deep, dark punched windows, notched corners, a tall
colonnaded base, and a slightly set-back crown storey. Among the glass towers of the
Transbay batch it is the pale, solid, finely gridded prism.

**Deliverable:** validated miniature GLB plus dossier, renders and report under
`artifacts/123-mission/`. Part 1 is the runnable task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `123-mission` |
| Existing procedural builder | none — new landmark, Case B (needs a `pipeline/lib/landmarks.mjs` entry, an exclusion and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3944470, 37.7918240` (OSM OBB centre, from `tk.run`) |
| Target height | **124.0 m** — published roof (Wikipedia); DataSF LiDAR max 127.19 m (incl. plant), majority 112.56 m |
| Footprint | 41.6 x 34.2 m OBB, long axis at bearing 134.5°; 1,326 m², 9-vertex ring with corner notches, OSM way 192026933 |
| Triangle cap | 12,000 (built: 5742) |
| Category | `3` (office) |

---

## Part 1 — Task prompt

````markdown
# Create a production-ready 123 Mission Street GLB for SF-SIM

Work in the sanfranciscosim repo, BATCH mode (docs/asset-pipeline/ADDRESS-TO-ASSET.md).
Build a stylized miniature of 123 Mission Street with the shared kit in tools/landmark-kit/.

Must capture: a pale cream stone prism with a dense grid of dark punched windows;
notched corners; a double-height colonnaded base; a set-back crown storey with parapet;
lit windows at night.

Contract: metres, Z up, +Y north, base centre at origin, crest exactly 124.0 m, flat
Toy_* materials, _Glow as thin skins, <= 12,000 triangles. Build -> validate ("all
checks pass") -> render; write REFERENCE.md and REPORT.md. Do not integrate.
````

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Basis |
|---|---|---|
| Architect, year | Skidmore, Owings & Merrill, 1986; developer Shorenstein | published (Wikipedia) |
| Storeys | 29 (article body also says 28) | published |
| Height | 124 m roof | published (Wikipedia infobox) |
| LiDAR | max 127.19 m, majority 112.56 m, median 115.86 m | measured (DataSF `201006.0002143`) |
| Footprint | 41.6 x 34.2 m OBB, 1,326 m²; notched corners and a jog on the SE side | measured (OSM way 192026933) |
| Cladding | cream/beige stone panels, deep-set dark windows, taller ground floor with louvred mezzanine | observed (Commons photo) |

The LiDAR majority plane (112.6 m) is the main roof; the 124 m published figure is taken
as the top of the set-back crown. The model: shaft roof 114 m, crown storey to 120 m,
parapet and plant to 124 m.

### 2.2 Sources

- OSM way 192026933 — https://www.openstreetmap.org/way/192026933
- DataSF Building Footprints (2010 LiDAR), https://data.sf.gov/resource/ynuv-fyni — record `201006.0002143`
- Wikipedia — https://en.wikipedia.org/wiki/123_Mission_Street
- Commons photo (infobox): File:123 Mission Street corner.jpg (2021)

### 2.3 Orientation

Authored true-world (+Y north). Local +X (41.6 m) runs to bearing 134.5° (SE). Faces:
**NW = Mission Street** (34.2 m, hero, street trees), NE / SW = toward Spear and Main
(mid-block neighbours), SE = rear.

### 2.4 What each side shows

- **Mission corner (photo):** uniform grid of square dark windows in cream stone, about
  eight bays per short face; blank stone strips at the notched corners; the top floors
  step in slightly at the corners; ground floor tall with stone piers, a louvred band
  above it.
- **Rear and sides:** inferred identical (the OSM SE jog is simplified away).

### 2.5 Recognition cues (ranked)

1. Pale cream stone prism with a fine dark grid.
2. Notched corners.
3. Set-back crown storey.
4. Tall colonnaded base.

### 2.7 Massing recipe

- Plan 40.5 x 33.5 m notched rectangle (3.2 m notches), yaw −44.5°.
- Base: dark glass recessed 1.6 m, 0–10 m, stone piers at 4.5 m, lit band.
- Shaft: sand punched block 10–114 m, 3.95 m storeys, 2.6 m pitch; stone cornice.
- Crown: 3 m inset, 2.4 m notches, punched sand block 115–120 m, stone parapet, plant
  cluster to 124 m.
- Plinth and three trees on Mission.

### 2.8 Palette

`Toy_sand` (stone), `Toy_stone` (piers, cornice, parapet), `Toy_glassd`, `Toy_roofd`,
`Toy_steel`, `Toy_leaf`, `Toy_sand_Glow`. All on-palette.

### 2.9 Roof

Dark ledge at 114 m around the crown; the crown roof carries the parapet and a tidy plant
cluster.

### 2.11 Triangle budget

Cap 12,000; the build lands at 5742.

### 2.12 Draft manifest entry

```json
{
  "id": "123-mission",
  "file": "123-mission.glb",
  "anchor": [-122.394447, 37.791824],
  "targetHeightM": 124.0,
  "cat": 3,
  "name": "123 Mission Street",
  "estimated": false,
  "dims": [56.2261, 56.1397, 124.0],
  "tris": 5742
}
```

### 2.13 Integration notes

- **Case B, new landmark**: `pipeline/lib/landmarks.mjs` entry, exclusion, re-bake.
- DataSF ring `201006.0002199` (109 m max, 44 m away) is a separate building to keep;
  measure the safe radius against OSM, DataSF and Overture rings.
- `loadRadius`: default `max(2500, 124 x 30) = 3720`.

### 2.15 Open risks

1. Crown height split (114 / 120 / 124 m) is inferred from LiDAR majority vs the
   published roof; the published 124 m may be the main roof.
2. The SE jog in the OSM ring is simplified to a symmetric notched rectangle.
3. Wikipedia gives both 28 and 29 storeys.
