# 425 California Street — SF-SIM asset plan

A slender 1968 office tower by John Carl Warnecke & Associates on the south side of California Street between Sansome and Leidesdorff: black glass between deep black mullion fins that run the full height and finish in small gold caps at the roofline. In the miniature it is the thin black prism with a gold-tipped crown.

**Deliverable:** `artifacts/425-california-street/` (FiDi batch, stages 1–2; approval, optimize and integration by the lead).

| | |
|---|---|
| Manifest id | `425-california-street` |
| Existing procedural builder | none — **new landmark, Case B** (needs a `pipeline/lib/landmarks.mjs` entry + exclusion + re-bake) |
| WGS84 anchor | `-122.4013729, 37.7928108` (from `tk.run`: OSM OBB centre + recentre shift) |
| Target height | **109.4 m** — published roof 109.4 m (Wikipedia tallest list; infobox 109 m); DataSF LiDAR ring median 108.79 m, max 111.29 m (measured, agrees) |
| Footprint | OSM way 260283289: 4 nodes, 609 m², OBB 25.3 × 24.1 m, bearing 81.7°; used as-is |
| Triangle cap | 5,000 (built: 2,834) |
| Category | `3` (Office — `CAT.office` in `app/src/props.js`) |

## Dossier

### Verified facts

| Fact | Value | Label |
|---|---|---|
| Roof / crest | 109.4 m | published; LiDAR median 108.8 m |
| Year / architect | 1968 / John Carl Warnecke & Associates | published (Wikipedia) |
| Floors | 29 (infobox) / 27 (tallest list) / 26 (assessor) | published, sources disagree |
| Footprint | 25.3 × 24.1 m, 609 m² | measured (OSM) |
| Base height ≈ 6.6 m |  | inferred (photo) |
| Gold fin caps at the roofline |  | inferred (photo) |

### Sources

- OSM way 260283289 — https://www.openstreetmap.org/way/260283289
- Wikipedia — https://en.wikipedia.org/wiki/425_California_Street; https://en.wikipedia.org/wiki/List_of_tallest_buildings_in_San_Francisco
- Commons photo — https://commons.wikimedia.org/wiki/File:425_California_Street.jpg (street level, looking up the corner)
- DataSF 2010 LiDAR ring 201006.0005008 (mblr SF0260001) — https://data.sf.gov/resource/ynuv-fyni
- DataSF https://data.sf.gov/resource/wv5m-vpq2.json (assessor roll): block 0260 lot 001, 1968, 26 storeys

### Orientation

Footprint used directly (edges 81.7° / 171.7°). North face = California St; west toward Sansome, east toward Leidesdorff; south faces the Bank of California block interior.

### What each side shows

- All four faces carry the same black glass and fin rhythm (photo shows two faces; the others **inferred** identical).
- Ground storey: dark granite piers with glass storefronts.

### Recognition cues (ranked)

1. Thin, very dark glass prism among pale stone neighbours.
2. Full-height black mullion fins giving a pinstripe texture.
3. Gold caps at the fin tops along the roofline.
4. Recessed dark granite base.

### Massing recipe

- 0–6.6 m `Toy_glassd` base inset 1 m behind `Toy_ink` piers at 5 m; lit lobby ring.
- 6.6–7.4 m `Toy_ink` transfer band.
- 7.4–105.6 m `tk.shaft`: 26 storeys (3.77 m), `Toy_glassd` glass, `Toy_ink` spandrels, `Toy_ink` fins every 2.6 m (0.55 m deep); lit panes per fin bay.
- Top 2.2 m of every fin capped in `Toy_gold`; `Toy_gold_Glow` crown line just outside the caps.
- `tk.roof_kit` deck, ink parapet and one plant box to the 109.4 m crest.

### Palette

`Toy_glassd`, `Toy_ink`, `Toy_gold`, `Toy_roofd`, `Toy_steel`, `Toy_stone`; glow `Toy_sand_Glow`, `Toy_gold_Glow`. All core palette.

### Roof

Dark deck inside an ink parapet with a single plant box; the gold caps ring it, and the gold crown line outlines it at night.

### Triangle budget

2,834 tris (body 2,296, night glow 538) against a 5,000 cap.

### Draft manifest entry

```json
{"id": "425-california-street", "file": "425-california-street.glb", "anchor": [-122.4013729, 37.7928108], "targetHeightM": 109.4, "cat": 3, "name": "425 California Street", "estimated": false, "dims": [34.2478, 33.0283, 109.4], "tris": 2834, "loadRadius": 3282}
```

### Integration notes

Case B. Small tower on a tight lot: exclusion radius ~17 m around the anchor; the Merchants Exchange (`california-bank-and-trust`) is the next lot east, so check it survives. loadRadius 3,282 m.

### Open risks

- Storey count differs between sources (26–29); only the height matters to the loader.
- Gold caps read from one photo; their exact extent is uncertain.
- South and east faces not photographed.
