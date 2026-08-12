# Columbus Tower (Sentinel Building) — reference dossier

Compiled 2026-08-10 for the SF-SIM miniature asset. Every value used by
`build_columbus_tower.py` traces back to this file. Facts are separated from
visual inference; conflicts are documented and resolved with reasons.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/288485994](https://www.openstreetmap.org/way/288485994) (fetched 2026-08-10 via api.openstreetmap.org, 18-node polygon) | Footprint geometry, `height=29`, `building:levels=7`, `ele=8`, architect Salfield & Kohlberg, name Sentinel Building / alt Columbus Tower, wikidata Q5150141 |
| [Wikipedia — Columbus Tower (San Francisco)](https://en.wikipedia.org/wiki/Columbus_Tower_(San_Francisco)) | Completed 1907 (begun before the 1906 quake); architects Salfield & Kohlberg; developer Abe Ruef; infobox floor_count 8, floor area 22,700 sqft; SF Designated Landmark No. 33 (1970); owner Francis Ford Coppola; American Zoetrope tenancy since 1972; Cafe Zoetrope on the ground floor since 1999; **basement** history (hungry i nightclub 1950, Kingston Trio recording studio) |
| [Wikidata Q5150141](https://www.wikidata.org/wiki/Q5150141) | 8 floors, 1907 inception (agrees with Wikipedia infobox) |
| Commons photo [Columbus Tower, 916 Kearny St, San Francisco.jpg](https://commons.wikimedia.org/wiki/File:Columbus_Tower,_916_Kearny_St,_San_Francisco.jpg) | The hero apex view from the Columbus/Kearny fork: full-height rounded corner bay, turret drum rising a level above the main cornice, copper dome, windowed lantern cupola, gold finial ball + spire; red Cafe Zoetrope awnings at grade |
| Commons photo [Columbus Tower San Francisco.jpg](https://commons.wikimedia.org/wiki/File:Columbus_Tower_San_Francisco.jpg) | Columbus (west) elevation close-up: white glazed-brick flat wall, verdigris bays, arched top-floor window on the flat wall, roof-edge cornice, dormer glimpse |
| Commons photo [Columbus Tower, SF side 2.JPG](https://commons.wikimedia.org/wiki/File:Columbus_Tower,_SF_side_2.JPG) | Facade construction detail: every bay window floor carries a projecting **segmental-arched eyebrow hood**; ornamented spandrels; bays are fully verdigris-clad; wall strips are white glazed brick |
| Commons photo [Columbus Tower, SF side 3.JPG](https://commons.wikimedia.org/wiki/File:Columbus_Tower,_SF_side_3.JPG) | Ground-level view up a white wall strip between two bay stacks; red CAFE awning; fire-escape ladder on the flank |
| Commons photo [Sentinel Building San Francisco at night.jpg](https://commons.wikimedia.org/wiki/File:Sentinel_Building_San_Francisco_at_night.jpg) | Night state: warm amber light in windows across the building, glowing cafe frontage under the red awnings, and a **red light at the cupola/lantern** |
| Commons photo [Columbus Tower and Transamerica Pyramid.jpg](https://commons.wikimedia.org/wiki/File:Columbus_Tower_and_Transamerica_Pyramid.jpg) | Context: scale relationship with the Transamerica Pyramid one block east; confirms the wedge reads green against its neighborhood |

Reference thumbnails were reviewed at ≤960 px from Wikimedia Commons (freely
licensed); none are committed to the repo.

## Verified dimensions and location

- **Footprint** (OSM polygon, projected with the app's tangent projection):
  bbox 18.53 × 16.95 m, area 156.3 m². Edges: **Kearny St (east) 17.83 m at
  bearing 130.4°**, **Jackson St (south) 15.05 m at bearing 260.7°** (two
  collinear segments), **Columbus Ave (west) 12.78 m at bearing 350.3°**, and a
  **14-node rounded apex arc, best-fit circle center (−6.778, 6.005) relative
  to the bbox center, radius 2.482 m** (max residual 3.4 cm), spanning ≈134°.
- **Anchor**: the model origin is the footprint **bbox center** =
  **lon −122.4050266, lat 37.7965554** (computed from the polygon; the plan's
  anchor −122.4050773, 37.7965842 is ~5 m to the NW of it — superseded because
  `placeGeneric` puts the model origin exactly at the anchor and this model is
  authored with the bbox center at the origin).
- **Apex heading**: the bisector at the nose points **330.4° true (NNW)** into
  the Columbus/Kearny fork — matches the plan's "roughly north-west".
- **Height**: OSM `height=29` is the only published number. Adopted as the
  **total height to the finial tip = 29.0 m** (see conflicts below).

## Storey count — conflict and resolution

OSM says 7 levels; Wikipedia/Wikidata say 8 floors. The photos show a ground
storefront + **six** upper bay-window floors below the main cornice, with the
round apex bay continuing one drum level above the cornice before the dome.
Wikipedia's own history documents a substantial occupied **basement** (the
hungry i, later the Kingston Trio recording studio) — the 8-floor count almost
certainly includes it. **Resolution: 7 above-ground levels (ground + 6),
matching OSM and the photo count.** Vertical layout: storefront to 4.0 m, six
3.0 m floors to the wall top at 22.0 m, cornice to 22.7 m, turret drum to
24.5 m, dome to ~27 m, lantern + gold ball + spire to exactly 29.0 m. The
turret share of total height (~24%) matches the street-photo proportions
within perspective error.

Wikipedia's 22,700 sqft floor area is inconsistent with 8 × 156 m² (≈13,400
sqft) — it may include the basement and mezzanines or simply be unreliable;
not used.

## What each side shows

- **NW apex (hero)**: full-height rounded bay on the 2.48 m arc; above the
  main cornice it becomes a windowed turret drum, then the copper dome, an
  open windowed lantern cupola, a gold ball finial and a thin spire.
- **East — Kearny St (17.8 m)**: the long flank. Verdigris bay stacks on white
  glazed brick, each floor with a segmental eyebrow hood; fire escape on one
  white strip (omitted in the miniature). Modeled with **4 bay stacks**.
- **West — Columbus Ave (12.8 m)**: same language, shorter. Modeled with
  **3 bay stacks**. An arched attic window sits on the white strip (simplified
  away; the eyebrow hoods carry the arch motif).
- **South — Jackson St (15.0 m)**: the plain back. Little photo coverage —
  *inferred* as flat white wall with a regular window grid, storefront band
  continuing at grade. No bays, no awnings.
- **Top**: small triangular roof, fully visible to the app camera: cornice all
  round, the apex dome + lantern, flat deck, stair penthouse toward Jackson,
  HVAC pair, one skylight.
- **Night**: warm amber window glow across the building, lit cafe frontage,
  red light at the cupola.

## Recognition cues (ranked)

1. The acute rounded-nose wedge plan filling its triangular lot
2. Verdigris copper bays/cornice/dome against white glazed-brick walls —
   unique in the neighborhood (note: the green is on the BAYS, not the walls)
3. The apex turret: rounded bay → drum → copper dome → lantern → gold finial
4. Per-floor segmental eyebrow hoods over every bay window
5. Red Cafe Zoetrope awnings wrapping the storefront

## Preserve / simplify

**Preserve**: the exact OSM wedge polygon and apex arc; 29 m total height with
7 readable above-ground levels; the full turret sequence (drum, dome, lantern,
gold ball, spire); verdigris-on-white color logic; eyebrow-hood rhythm; red
awning band; warm night glow + red cupola light.

**Simplify**: ornamented spandrels/rosettes → clean verdigris panels; curved
bow-window glass → flat-front bays with rounded (beveled) corners; fire
escapes → omitted (thin dark noise at city scale); the flat-wall attic arches
→ omitted; per-pane sashes → one graphical `Toy_glass` slab per floor per bay;
basement → not modeled (below grade).

## Uncertainties and conflicts

- Whether OSM `height=29` measures the roof or the finial tip is unpublished.
  Adopted: finial tip = 29.0 m (photo proportions support a ~22 m main
  cornice; 7 levels × ~3 m + turret is architecturally consistent). If a
  surveyed figure appears, only `targetHeightM` needs to change — the loader
  rescales.
- The Kearny/Jackson and Columbus/Jackson corner treatments are not clearly
  photographed; modeled as simple square corners.
- The Jackson elevation window layout is inferred, not photographed.
- Real verdigris is more saturated/turquoise than palette `Toy_verdigris`
  (#9fb8a8); the palette color is used deliberately (plan §2.15, style bible
  §7 restraint).
