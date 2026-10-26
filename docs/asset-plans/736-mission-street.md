# Contemporary Jewish Museum (736 Mission Street) — SF-SIM asset plan

Willis Polk's 1907 Jessie Street Substation — red brick, white terracotta cornice and a tall round-arched window — gutted and extended by Daniel Libeskind (2008) with a tilted blue-steel cube (the "Yud") over a dark slanted wing (the "Chet") at its south-west end, facing Jessie Square. The museum has been on hiatus since December 2024; the building stands.

**Deliverable:** `artifacts/736-mission-street/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `736-mission-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4036821, 37.7860166` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **24.0 m — measured** LiDAR max 24.05 m = the blue cube (SF3706276); the brick hall roof is the LiDAR median 14.0 m. OSM `height=14` is the hall |
| Footprint | OSM way 118106934: OBB 85.2 x 28.2 m, 2,038 m², long axis 45° (along Mission) |
| Triangle cap | 3,000 (built: 638) |
| Category | `16` (museum, `CAT.museum` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (blue cube) | 24.0 m | measured (LiDAR max 24.05 m) |
| Substation roof | 14.0 m | measured (LiDAR median 13.95 m) |
| Substation 1907 / Libeskind addition 2008 |  | published (Wikipedia) |
| Footprint | OSM way split at its setback: hall ~50 x 24 m, addition SW | measured / inferred split |
| Cube ~17 m square, tilted 14°, roof sloping up to the SW |  | inferred (photo) |

### Sources

- OSM way 118106934 — https://www.openstreetmap.org/way/118106934
- Wikipedia — https://en.wikipedia.org/wiki/Contemporary_Jewish_Museum
- Wikidata Q5164991 — https://www.wikidata.org/wiki/Q5164991
- Commons photo — https://commons.wikimedia.org/wiki/File:Contemporary_Jewish_Museum.jpg
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF3706276)

### Orientation

Long axis bearing 45° (parallel to Mission). The SE long face fronts Jessie Square / Mission; the cube sits at the SW end, the great arched window near the NE end of the SE face.

### What each side shows

- SE (Jessie Square): brick hall, white cornice, arched window and portal (photo).
- SW end: the Libeskind cube and dark wing with the glazed lobby (photo shows them from the square).
- NW / NE: brick with upper windows (**inferred**); the NW side backs onto Yerba Buena Lane buildings.

### Recognition cues (ranked)

1. The tilted blue cube beside a red-brick hall: unique in the city.
2. Red brick with a white terracotta cornice and one huge round arch.
3. Dark slanted wing below the cube.

### Massing recipe

- Hall: granite base 0–1.2 m, brick prism to 13.2 m, cream cornice, dark roof with a glass skylight.
- SE front: cream arch frame (7 m arch to 12 m) and portal (4 m arch) with dark glass and lit arches.
- Addition: ink prism with a sloping top (`tilted_block`), lit lobby panes on the street faces.
- Yud: 17 m square, rotated +14°, from 4 m to a tilted roof plane cresting at 24.0 m, leaning 1.2 m out; nine small white-glow window squares on its roof plane.
- Stone apron and three trees on Jessie Square.

### Palette

Toy_brick, Toy_cream, Toy_stone, Toy_sky (cube), Toy_ink, Toy_glassd, Toy_glassl, Toy_roofd, Toy_leaf/leafd/rust (trees); glow Toy_sand_Glow, Toy_white_Glow.

### Roof

Dark hall roof with a long skylight; the cube's tilted blue top with its scatter of lit squares.

### Triangle budget

638 tris (body 580, night glow 58) against a cap of 3,000.

### Draft manifest entry

```json
{"id": "736-mission-street", "file": "736-mission-street.glb", "anchor": [-122.4036821, 37.7860166], "targetHeightM": 24.0, "cat": 16, "name": "Contemporary Jewish Museum (736 Mission Street)", "estimated": false, "dims": [81.9536, 83.2589, 24.0], "tris": 638, "loadRadius": 2500}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 24.0) = 2500. Build:
`blender -b --python artifacts/736-mission-street/build_736_mission_street.py`.

### Open risks

- The hall/addition split line is inferred from the footprint setback.
- Cube size and tilt are from one oblique photo.
- Museum operations paused in 2024; the building itself is unchanged.
