# Hunter-Dulin Building (111 Sutter Street) — SF-SIM asset plan

A 22-storey 1927 office tower by Schultze & Weaver at Sutter and Montgomery, in buff terracotta with a French chateau top: two corner pavilions under steep brown hipped roofs with copper-green cresting, a lower centre bay between them. In the miniature it is the storybook roofline among the FiDi's flat tops.

**Deliverable:** `artifacts/hunter-dulin-building/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `hunter-dulin-building` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4025497, 37.7897258` (from `tk.run`, OSM OBB centre + recentre shift) |
| Target height | **93.88 m** — published roof 93.88 m (Wikipedia infobox); DataSF LiDAR 93.98 m agrees |
| Footprint | OSM way 942664247: OBB 49.6 × 33.2 m, 1,645 m², long axis bearing 80.9° (along Sutter); modelled as the OBB rectangle |
| Triangle cap | 5,000 (built: 4,190) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof / crest | 93.88 m | published (Wikipedia); LiDAR 93.98 m |
| Floors / year / architect | 22 (25 per article text) / 1927 / Schultze & Weaver | published |
| Footprint | 49.6 × 33.2 m, bearing 80.9° | measured (OSM) |
| Main cornice ~66 m, pavilion eaves ~80 m, centre bay ~78 m |  | inferred (photo) |
| NRHP listed 1997; 'Spade & Archer' office in The Maltese Falcon |  | published |

### Sources

- OSM way 942664247 — https://www.openstreetmap.org/way/942664247
- Wikipedia — https://en.wikipedia.org/wiki/Hunter%E2%80%93Dulin_Building
- Commons photo — https://commons.wikimedia.org/wiki/File:Hunter-Dulin_Building.jpg (from Market St, 2021)
- DataSF footprints / 2010 LiDAR — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Yaw 9.08° (long axis bearing 80.9°). +Y = true north. North face = Sutter St, west face = Montgomery St; south and east faces are party/lane sides.

### What each side shows

- North (Sutter) and west (Montgomery): street fronts, buff terracotta grid of paired windows, shopfront base.
- Pavilions sit at the east and west ends with the lower centre bay between them; seen from Market in the photo (the photo shows two pavilions and a recessed middle).
- South/east: same skin assumed (**inferred**; the real party walls are plainer).

### Recognition cues (ranked)

1. Twin steep brown chateau roofs with green cresting and finials.
2. Warm buff terracotta colour, set apart from grey modern neighbours.
3. Recessed, lower centre bay between the pavilions.
4. Plain punched-window shaft with a cornice at the setback.

### Massing recipe

- Plan `tk.rect(49.6, 33.2)` on yaw 9.08°.
- 0–7.5 m shopfront base (dark panes, warm lit), cream band.
- 8.5–66 m `punched_block` terracotta, 16 storeys of 3.6 m, paired windows (3.6 m spacing); cornice.
- Two 15 m pavilions (full depth) to 80 m, verdigris crest band, hipped `rust` roofs to 93.3 m, dormers, finials, ridge crest to 93.88 m.
- Centre bay 19.6 × 27 m to 78 m with crest band, roof deck and plant.

### Palette

`Toy_terracotta` (off-palette, buff), `Toy_cream`, `Toy_rust` (roofs), `Toy_verdigris` (cresting), `Toy_glassd`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`.

### Roof

Two hipped chateau roofs with dormers and finials; a flat centre deck with a tidy plant cluster. Floodlit pavilion bands at night.

### Triangle budget

4,190 tris (body 3,480, night glow 710) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "hunter-dulin-building", "file": "hunter-dulin-building.glb", "anchor": [-122.4025497, 37.7897258], "targetHeightM": 93.88, "cat": 3, "name": "Hunter-Dulin Building (111 Sutter Street)", "estimated": false, "dims": [61.058, 47.4516, 93.88], "tris": 4190, "loadRadius": 2816}
```

### Integration notes

Case B. The OSM footprint fills its lot; exclusion radius ~25 m clears only this footprint (the Crocker/One Montgomery pavilion is across Montgomery). loadRadius 2,816 m (30 × height).

### Open risks

- Exact pavilion widths, heights and roof pitch are read from one photo.
- Article text says 25 storeys, infobox 22; the height is what matters.
- The real top has a light court and more varied massing toward the back; simplified to one rectangle.
