# 50 Beale Street — SF-SIM asset plan

SOM's 1967 Bechtel headquarters (later the Blue Shield of California Building) on the west
side of Beale between Market and Mission: a long 23-storey slab of dark bronze glass in a
deep black-anodised grid, standing on a recessed colonnade, with a plaza of mature street
trees on Beale. It is the darkest box on the block and the foil to 77 Beale's pale
granite across the street.

**Deliverable:** validated miniature GLB plus dossier, renders and report under
`artifacts/50-beale/`. Part 1 is the runnable task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `50-beale` |
| Existing procedural builder | none — new landmark, Case B (needs a `pipeline/lib/landmarks.mjs` entry, an exclusion and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3964860, 37.7912570` (OSM OBB centre, from `tk.run`) |
| Target height | **100.0 m** — published 328 ft (Wikipedia); DataSF LiDAR max 101.33 m, majority 97.30 m |
| Footprint | 71.5 x 39.1 m OBB, long axis at bearing 134.8° (along Beale); 2,779 m², OSM way 256065251 |
| Triangle cap | 12,000 (built: 5282) |
| Category | `3` (office) |

---

## Part 1 — Task prompt

````markdown
# Create a production-ready 50 Beale Street GLB for SF-SIM

Work in the sanfranciscosim repo, BATCH mode (docs/asset-pipeline/ADDRESS-TO-ASSET.md).
Build a stylized miniature of 50 Beale Street with the shared kit in tools/landmark-kit/.

Must capture: a long dark bronze-glass slab (71.5 x 39 m) in a heavy black grid; a
recessed glass ground floor behind black columns; a set-back mechanical penthouse;
the Beale Street trees; lit windows at night.

Contract: metres, Z up, +Y north, base centre at origin, crest exactly 100.0 m, flat
Toy_* materials, _Glow as thin skins, <= 12,000 triangles. Build -> validate ("all
checks pass") -> render; write REFERENCE.md and REPORT.md. Do not integrate.
````

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Basis |
|---|---|---|
| Names | Bechtel Building; Blue Shield of California Building (2006–18) | published (Wikipedia) |
| Architect, year | Skidmore, Owings & Merrill, 1967 | published |
| Storeys | 23 | published; OSM levels 23 |
| Height | 328 ft = 100 m roof | published (Wikipedia infobox) |
| LiDAR | max 101.33 m, majority 97.30 m, median 92.42 m | measured (DataSF `201006.0000806`) |
| Footprint | 71.5 x 39.1 m rectangle, 2,779 m² | measured (OSM way 256065251) |
| Skin | dark bronze glass in a black metal grid | observed (Commons photo) |

The model puts the main roof at 93 m (median plane), a 4 m-inset dark penthouse to 96 m,
and roof plant to 100 m — the published figure, about 1.3 m under the LiDAR max.

### 2.2 Sources

- OSM way 256065251 — https://www.openstreetmap.org/way/256065251
- DataSF Building Footprints (2010 LiDAR), https://data.sf.gov/resource/ynuv-fyni — record `201006.0000806`
- Wikipedia — https://en.wikipedia.org/wiki/50_Beale_Street
- Commons photo (infobox): File:Blue_Shield_of_California_Building.jpg (2022 corner view)

### 2.3 Orientation

Authored true-world (+Y north). Local +X (71.5 m long axis) runs to bearing 134.8° (SE),
parallel to Beale Street. Faces: **NE = Beale Street** (long, hero, trees), SE = toward
Mission, NW = toward Market, SW = mid-block.

### 2.4 What each side shows

- **NE / corner (photo):** an unbroken grid of dark bronze glass, ~1.5 m mullion rhythm
  and a spandrel each floor, all dark; ground floor recessed behind black columns with
  shopfront glass; large street trees in front.
- **Other faces:** inferred identical curtain wall (SOM slab, uniform LiDAR roof).

### 2.5 Recognition cues (ranked)

1. The darkest box in the cluster — bronze glass and black grid.
2. Long, flat-topped slab proportion (71.5 x 39 x 100 m).
3. Heavy, regular grid with no setbacks.
4. Recessed colonnade base and the Beale Street trees.

### 2.7 Massing recipe

- Plan 70 x 38 m, yaw −44.8°.
- Base: dark glass recessed 3 m, 0–7.5 m, lit band; black columns at 6.5 m.
- Shaft 7.5–93 m: banded loft, `Toy_bronze` glass, `Toy_ink` 1.2 m spandrels at 3.9 m,
  ink fins at 3.3 m; scattered lit windows.
- Roof: deck and ink parapet at 93 m; ink penthouse inset 4 m to 96 m with louvre fins,
  cap and plant to 100 m.
- Plinth, five large trees along Beale.

### 2.8 Palette

`Toy_bronze` (off-palette, documented), `Toy_ink`, `Toy_glassd`, `Toy_roofd`, `Toy_steel`,
`Toy_stone`, `Toy_leaf`, `Toy_sand_Glow`.

### 2.9 Roof

Dark deck, parapet, louvred penthouse, a row of plant boxes on the penthouse.

### 2.11 Triangle budget

Cap 12,000; the build lands at 5282.

### 2.12 Draft manifest entry

```json
{
  "id": "50-beale",
  "file": "50-beale.glb",
  "anchor": [-122.396486, 37.791257],
  "targetHeightM": 100.0,
  "cat": 3,
  "name": "50 Beale Street",
  "estimated": false,
  "dims": [90.4472, 90.2892, 100.0],
  "tris": 5282
}
```

### 2.13 Integration notes

- **Case B, new landmark**: `pipeline/lib/landmarks.mjs` entry, exclusion, re-bake.
- DataSF ring `201006.0001389` (162 m max, 36 m away) is a separate tower to keep; measure
  the safe radius against OSM, DataSF and Overture rings.
- `loadRadius`: default `max(2500, 100 x 30) = 3000`.

### 2.15 Open risks

1. Side and rear faces are inferred identical.
2. The penthouse height and inset are read from the LiDAR spread (majority 97.3 vs median
   92.4), not measured directly.
3. The 1920 Bechtel railcar inside is not modelled (interior).
