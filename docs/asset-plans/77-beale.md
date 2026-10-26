# 77 Beale Street (Pacific Gas & Electric Building) — SF-SIM asset plan

PG&E's 1971 headquarters tower by Hertzka & Knowles on the Beale/Mission corner: a
34-storey, 150 m slab clad in pale grey granite, finely ribbed by deep vertical piers
between small punched windows, with blank re-entrant notches at every corner and a crown
where the piers run up past the top floor as open slots. It reads as the stone
counterpart to the bronze-glass 50 Beale across the street.

**Deliverable:** validated miniature GLB plus dossier, renders and report under
`artifacts/77-beale/`. Part 1 is the runnable task prompt, Part 2 the dossier.

| | |
|---|---|
| Manifest id | `77-beale` |
| Existing procedural builder | none — new landmark, Case B (needs a `pipeline/lib/landmarks.mjs` entry, an exclusion and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3957540, 37.7917820` (OSM OBB centre, from `tk.run`) |
| Target height | **150.0 m** — published roof 149.96 m (Wikipedia infobox); DataSF LiDAR majority roof plane 144.66 m, max 168.48 m |
| Footprint | 58.4 x 42.4 m OBB, long axis at bearing 44.9°; 2,418 m², notched corners, OSM way 260291405 |
| Triangle cap | 12,000 (built: 8186) |
| Category | `3` (office) |

---

## Part 1 — Task prompt

````markdown
# Create a production-ready 77 Beale Street GLB for SF-SIM

Work in the sanfranciscosim repo, BATCH mode (docs/asset-pipeline/ADDRESS-TO-ASSET.md).
Build a stylized miniature of the Pacific Gas & Electric Building, 77 Beale Street,
with the shared kit in tools/landmark-kit/.

Must capture: a tall grey-granite slab on a 58 x 42 m notched-corner plan; dense vertical
piers with small punched windows; blank notched corners; the slotted crown where piers
rise past the roof; a recessed glazed lobby behind a pier colonnade; lit windows at night.

Contract: metres, Z up, +Y north, base centre at origin, crest exactly 150.0 m, flat
Toy_* materials, _Glow as thin skins, <= 12,000 triangles. Build -> validate ("all
checks pass") -> render; write REFERENCE.md and REPORT.md. Do not integrate.
````

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Basis |
|---|---|---|
| Name / use | Pacific Gas & Electric Building; PG&E HQ 1971–2022, offices | published (Wikipedia) |
| Architect, year | Hertzka & Knowles, 1971 | published |
| Storeys | 34 | published (Wikipedia); OSM levels 34 |
| Height | 149.96 m roof | published (Wikipedia infobox) |
| LiDAR | majority 144.66 m (main roof plane), median 144.78, max 168.48 m | measured (DataSF `201006.0000930`); the max is a rooftop mast/crane hit, not modelled |
| Footprint | 58.4 x 42.4 m OBB, 2,418 m², 13-vertex ring with notched corners (~5 x 1.6 m) | measured (OSM way 260291405) |
| Cladding | pale grey granite piers and spandrels, small dark windows | observed (Commons photo) |
| Status | sold to Hines 2021; Hines proposed (July 2025) replacing it with a 1,225 ft tower | published (Wikipedia) |

The model's crest is the crown parapet at 150.0 m with the main roof deck at 145 m, which
reconciles the published figure with the LiDAR roof plane.

### 2.2 Sources

- OSM way 260291405 — https://www.openstreetmap.org/way/260291405
- DataSF Building Footprints (2010 LiDAR), https://data.sf.gov/resource/ynuv-fyni — record `201006.0000930`
- Wikipedia — https://en.wikipedia.org/wiki/Pacific_Gas_%26_Electric_Building
- Commons photo (infobox): File:Pacific Gas & Electric Building 02.jpg (2021, corner view from Mission/Beale)

### 2.3 Orientation

Authored true-world (+Y north). Local +X (58.4 m long axis) runs to bearing 44.9° (NE),
parallel to Mission Street. Faces: **SE = Mission Street** (long, hero), **SW = Beale
Street** (short), NW and NE toward mid-block neighbours.

### 2.4 What each side shows

- **SE / SW (photo):** identical treatment — a grid of piers about 2.9 m apart running the
  full height, one small window per bay per floor, blank granite at the notched corners,
  open slots at the top where the piers continue above the last floor; at the base,
  double-height piers in front of a recessed dark-glass lobby, with a stair and planters.
- **NW / NE:** not photographed here; inferred identical (the tower is a free-standing
  slab and the LiDAR roof is uniform).

### 2.5 Recognition cues (ranked)

1. Pale grey stone slab, 150 m, among bronze and glass neighbours.
2. Fine vertical ribbing (piers) with tiny punched windows.
3. The slotted crown.
4. Blank notched corners.
5. Pier colonnade over a dark recessed lobby.

### 2.7 Massing recipe

- Plan: 56 x 41 m notched rectangle (3 m notches), yaw 45°.
- Lobby: dark glass recessed 2 m, 0–10 m, behind 1.5 m concrete piers at 5.5 m.
- Shaft: concrete punched block 10–145 m, 3.95 m storeys, 2.9 m pitch; proud piers
  0.7 x 0.55 m at 2.9 m.
- Crown: concrete screen wall 145–150 m with ink slots between the piers; dark roof deck at
  145 m and a plant cluster below the crest.
- Plinth and four street trees on the Mission side.

### 2.8 Palette

`Toy_concrete` (granite — off-palette, documented), `Toy_glassd`, `Toy_ink` (crown
slots), `Toy_roofd`, `Toy_steel`, `Toy_stone`, `Toy_leaf`, `Toy_sand_Glow` (lobby band
and scattered lit windows).

### 2.9 Roof

Deck at 145 m inside the 5 m crown wall; one plant cluster that stays below the crest.

### 2.11 Triangle budget

Cap 12,000; the build lands at 8186.

### 2.12 Draft manifest entry

```json
{
  "id": "77-beale",
  "file": "77-beale.glb",
  "anchor": [-122.395754, 37.791782],
  "targetHeightM": 150.0,
  "cat": 3,
  "name": "Pacific Gas & Electric Building (77 Beale Street)",
  "estimated": false,
  "dims": [74.1048, 74.1048, 150.0],
  "tris": 8186
}
```

### 2.13 Integration notes

- **Case B, new landmark**: `pipeline/lib/landmarks.mjs` entry, exclusion and re-bake.
- Neighbouring DataSF rings `201006.0010301` (34 m) and `201006.0004876` (43 m) are other
  buildings on the block; measure the exclusion window against OSM, DataSF and Overture
  rings so they survive.
- `loadRadius`: default `max(2500, 150 x 30) = 4500`.

### 2.15 Open risks

1. **Demolition proposal.** Hines proposed replacing the tower (July 2025). If demolition
   has started, the asset documents the 1971 building; check before integrating.
2. NW and NE faces are inferred.
3. The LiDAR max (168.5 m) is not modelled; it is taken as a mast or crane.
