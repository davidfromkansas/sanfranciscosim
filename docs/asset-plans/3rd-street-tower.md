# St. Regis Museum Tower (125 Third Street) — SF-SIM asset plan

A 42-storey hotel and condominium tower by Skidmore, Owings & Merrill (2001–05) at the SE corner of Third and Mission, next to SFMOMA, with the Museum of the African Diaspora in its base. It reads as a warm limestone grid of square punched windows: a broad ~89 m hotel block wrapped around the foot of a slimmer residential shaft, a vertical glass slot with stacked balconies, and a glass-railed penthouse crown.

**Deliverable:** `artifacts/3rd-street-tower/` (Financial District batch, stages 1–2 of
docs/asset-pipeline/ADDRESS-TO-ASSET.md, BATCH mode).

| | |
|---|---|
| Manifest id | `3rd-street-tower` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4013679, 37.7863061` (OSM OBB centre, recentred by `tk.run`) |
| Target height | **147.5 m — published** roof 484 ft (Wikipedia infobox). LiDAR max 144.8 m (SF3722257) agrees within 2 % |
| Footprint | OSM way 436648188 (outline) + parts 436648187 / 79377186 / 1365382602: OBB 63.0 x 45.8 m, 2,450 m², long axis 45° |
| Triangle cap | 5,000 (built: 3,632) |
| Category | `7` (hotel, `CAT.hotel` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof height | 147.5 m (484 ft) | published (Wikipedia) |
| Floors / completed / architect | 42 / 2005 / SOM | published |
| Crest in 2010 LiDAR | max 144.8 m, median 88.5 m, majority 32.9 m | measured (DataSF SF3722257) |
| Hotel block height | 88.4 m (OSM part `height=89`, LiDAR median) | measured |
| Tower part footprint | 32.7 x 24.4 m, edges 135.5° / 45.8° | measured (OSM part 436648187) |
| Assessor | 188 Minna St condominiums, built 2005 | published (DataSF assessor) |
| Penthouse crown 142.8–147.5 m, glass slot on NE face |  | inferred (photo) |

### Sources

- OSM way 436648188 and parts — https://www.openstreetmap.org/way/436648188
- Wikipedia — https://en.wikipedia.org/wiki/St._Regis_Museum_Tower
- Wikidata Q7591596 — https://www.wikidata.org/wiki/Q7591596
- Commons photo — https://commons.wikimedia.org/wiki/File:The_St._Regis_San_Francisco_2021.jpg
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF3722257)
- DataSF assessor rolls — https://data.sf.gov/resource/wv5m-vpq2.json

### Orientation

Tower edges at 45.8° / 135.5°; +Y = true north. Mission St is the NW side, Third St the SW side (the 1907 Williams Building, not modelled, sits on the corner in front), SFMOMA to the SE, Minna St NE.

### What each side shows

- NW / SW (Mission, Third): the photographed limestone grid over the glassy museum base.
- NE: the glass slot with the balcony stack (photo shows it on the slim side face; position inferred).
- SE toward SFMOMA: same grid assumed (**inferred**).

### Recognition cues (ranked)

1. Tallest warm-stone tower south of Market at Third: a pale gridded slab, not glass.
2. Two-step massing: broad 89 m hotel block, residential shaft to 147.5 m.
3. Glass penthouse crown with a lit rail line at night.
4. Glassy lit base (MoAD / hotel lobby).

### Massing recipe

- Plans are the OSM building:part polygons used as-is (`tk.ccw`).
- Low NE strip 0–13 m (3 levels), sand with a roof kit.
- Hotel block 0–88.4 m: glassd lobby 0–10.2 m with lit panes, sand transfer storey, then sand prism with `panes`/`lit_windows` in 6.8 m two-storey bands (13 bands), parapet, deck and plant.
- Residential shaft 88.4–142.8 m on the tower part: same grid (8 bands), glass slot box + sky glow strip.
- Crown 142.8–147.5 m: stone cornice, inset glassl penthouse with lit panes, glassg rail, white crown line.

### Palette

Toy_sand, Toy_stone, Toy_glassl (windows), Toy_glassd, Toy_glass, Toy_glassg (off-palette rail), Toy_roofd, Toy_steel; glow Toy_sand_Glow, Toy_sky_Glow, Toy_white_Glow.

### Roof

Hotel-block deck with plant at 88.4 m; penthouse roof deck with a low plant at 147.5 m; strip roof kit.

### Triangle budget

3,632 tris (body 2,994, night glow 638) against a cap of 5,000.

### Draft manifest entry

```json
{"id": "3rd-street-tower", "file": "3rd-street-tower.glb", "anchor": [-122.4013679, 37.7863061], "targetHeightM": 147.5, "cat": 7, "name": "St. Regis Museum Tower (125 Third Street)", "estimated": false, "dims": [68.5944, 81.3845, 147.5], "tris": 3632, "loadRadius": 4425}
```

### Integration notes

Case B: registry entry, exclusion circle sized to this footprint only, batch re-bake. `dims` is the world-axis
bbox including the sidewalk apron. `loadRadius` = max(2500, 30 x 147.5) = 4425. Build:
`blender -b --python artifacts/3rd-street-tower/build_3rd_street_tower.py`.

### Open risks

- Where the hotel block ends and the tower begins is read from OSM parts + LiDAR median, not drawings.
- Two-storey window bands read coarser than the real per-floor grid.
- OSM `building:levels=3` on the outline tag is the podium, not the tower.
