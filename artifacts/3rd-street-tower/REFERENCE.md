# St. Regis Museum Tower — reference dossier

Plan: `docs/asset-plans/3rd-street-tower.md`. Labels: published / measured / inferred / estimated.

## Sources

- OSM way 436648188 and parts — https://www.openstreetmap.org/way/436648188
- Wikipedia — https://en.wikipedia.org/wiki/St._Regis_Museum_Tower
- Wikidata Q7591596 — https://www.wikidata.org/wiki/Q7591596
- Commons photo — https://commons.wikimedia.org/wiki/File:The_St._Regis_San_Francisco_2021.jpg
- DataSF 2010 LiDAR footprints — https://data.sf.gov/resource/ynuv-fyni (SF3722257)
- DataSF assessor rolls — https://data.sf.gov/resource/wv5m-vpq2.json
- Reference photo used: scratchpad `fidi/photos/3rd-street-tower.jpg` (kept out of the repo).

## Dimensions and location

| Item | Value |
|---|---|
| Anchor (manifest) | `-122.4013679, 37.7863061` |
| Crest | 147.5 m — **147.5 m — published** roof 484 ft (Wikipedia infobox). LiDAR max 144.8 m (SF3722257) agrees within 2 % |
| Footprint | OBB 63.0 x 45.8 m, 2,450 m², long axis 45° (OSM way 436648188 (outline) + parts 436648187 / 79377186 / 1365382602) |
| Model bbox | 68.5944 x 81.3845 x 147.5 m (incl. apron) |

## Orientation

Tower edges at 45.8° / 135.5°; +Y = true north. Mission St is the NW side, Third St the SW side (the 1907 Williams Building, not modelled, sits on the corner in front), SFMOMA to the SE, Minna St NE.

## Recognition cues (ranked)

1. Tallest warm-stone tower south of Market at Third: a pale gridded slab, not glass.
2. Two-step massing: broad 89 m hotel block, residential shaft to 147.5 m.
3. Glass penthouse crown with a lit rail line at night.
4. Glassy lit base (MoAD / hotel lobby).

## Simplified

Windows are drawn as two-storey bands (one pane per two floors) to stay under 5,000 tris; the sloped crown parapet, balconies and the lower east wing step are omitted.

## Uncertainties

- Where the hotel block ends and the tower begins is read from OSM parts + LiDAR median, not drawings.
- Two-storey window bands read coarser than the real per-floor grid.
- OSM `building:levels=3` on the outline tag is the podium, not the tower.
