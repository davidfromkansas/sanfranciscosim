# Neiman Marcus Union Square (City of Paris rotunda) — SF-SIM asset plan

Neiman Marcus, 150 Stockton Street at Geary (Philip Johnson / John Burgee, 1982), on the site of the City of Paris department store (1896), whose glass rotunda and stained-glass dome were kept and set into the new store's Stockton × Geary corner. A long, nearly windowless box clad in a rose-and-white granite checkerboard, a green glass corner pavilion around the rotunda, and a lighter service storey on the roof.

**Deliverable:** `artifacts/150-stockton-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `150-stockton-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4059211, 37.7873699` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **33.9 m** — LiDAR crest from the batch facts file (measured); DataSF ring 201006.0000451 majority 32.86 m, median 28.44 m (main roof), max 39.41 m (spill from Macy's, not used); OSM `height=28` |
| Footprint | OSM way 332521036: 10 nodes (bowed east end simplified to 6), 3,876 m², OBB 92.9 × 42.2 m, bearing 80.9° |
| Triangle cap | 3,000 (built: 1,528) |
| Category | `4` (Retail — `CAT.retail` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Crest (rooftop storey) | 33.9 m | measured (facts-file LiDAR); ring majority 32.9 m |
| Main roof | 28 m | measured (ring median 28.4 m; OSM 28) |
| Year / architects | 1982 / Philip Johnson & John Burgee | published (Wikipedia, City of Paris article) |
| Rotunda and dome from the 1896 City of Paris |  | published (Wikipedia) |
| Footprint | 92.9 × 42.2 m, 3,876 m² | measured (OSM) |

### Sources

- OSM way 332521036 — https://www.openstreetmap.org/way/332521036 (`wikidata=Q5123857`, City of Paris)
- Wikipedia — https://en.wikipedia.org/wiki/City_of_Paris_Dry_Goods_Co.
- Commons photo — https://commons.wikimedia.org/wiki/File:View_on_Neiman_Marcus_vom_Westin_St_Francis.jpg (aerial view east along Geary; Macy's on the right)
- DataSF 2010 LiDAR ring 201006.0000451 (mblr SF0313018) — https://data.sf.gov/resource/ynuv-fyni

### Orientation

Long axis 80.9° along Geary Street. North face = Geary; west end = Stockton (facing Union Square); the rotunda pavilion is the NW (Stockton × Geary) corner; south toward Macy's.

### What each side shows

- North (Geary) and the NW corner: checkerboard granite, glass corner pavilion, roof storey set back (photo).
- West (Stockton): checkerboard **inferred** same.
- South and east: party sides toward Macy's and neighbours, **inferred**.

### Recognition cues (ranked)

1. Rose-and-white granite checkerboard box.
2. Green glass corner pavilion (the old City of Paris rotunda) at Stockton × Geary.
3. Lit glass dome at the corner.
4. Paler set-back roof storey.

### Massing recipe

- 0–28 m `Toy_granite` box; `Toy_rust` checker cells (3.75 m, alternate courses offset) on all faces; dark glass storefront band with lit ring, stone fascia.
- Corner pavilion: `Toy_glassl` 12-sided cylinder r 11 m to 29 m with lit panes on the exposed arcs; a low glass dome with a `Toy_gold_Glow` cap.
- Roof: parapet and deck; a `Toy_stone` set-back storey (46 × 30 m, east half) with panes to 32.3 m; low plant to 33.9 m.

### Palette

`Toy_granite`, `Toy_rust`, `Toy_glassl`, `Toy_glassd`, `Toy_stone`, `Toy_roofd`, `Toy_steel`; glow `Toy_sand_Glow`, `Toy_gold_Glow`. Off-palette: `Toy_granite` (documented).

### Roof

Dark deck with granite parapet, the paler upper storey with plant, and the rotunda dome at the corner.

### Triangle budget

1,528 tris (body 1,410, night glow 118) against a 3,000 cap.

### Draft manifest entry

```json
{"id": "150-stockton-street", "file": "150-stockton-street.glb", "anchor": [-122.4059211, 37.7873699], "targetHeightM": 33.9, "cat": 4, "name": "Neiman Marcus Union Square (City of Paris rotunda)", "estimated": false, "dims": [104.715, 63.0629, 33.9], "tris": 1528, "loadRadius": 2500}
```

### Integration notes

Case B (retail landmark, 33.9 m). Exclusion radius ~48 m along the long axis — use the polygon; Macy's and the Maiden Lane buildings must survive. loadRadius 2,500 m.

### Open risks

- Corner pavilion geometry and dome visibility from outside are approximations.
- Size and position of the rooftop storey estimated from one aerial photo.
- OSM footprint's bowed east end simplified.
