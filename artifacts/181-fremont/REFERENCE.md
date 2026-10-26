# 181 Fremont — reference dossier

Checked 2026-10-25 (Transbay landmark batch). Labels: **published**, **measured**,
**inferred** (from photographs), **estimated** (modelling choice).

## Sources

- [OpenStreetMap way 445566153](https://www.openstreetmap.org/way/445566153) — footprint (10 nodes, 1,289 m², OBB 40.6 × 35.5 m, bearing 45.1°), `height=244.4`, `building:levels=57`.
- [Wikipedia — 181 Fremont](https://en.wikipedia.org/wiki/181_Fremont) — 802 ft / 244 m to the spire, 57 floors, Heller Manus Architects, completed 2018, offices below and condominiums above (via the batch facts sheet; a re-fetch this session was rate-limited, HTTP 429).
- Wikipedia lead photograph (Commons, [Category:181 Fremont](https://commons.wikimedia.org/wiki/Category:181_Fremont)) — an upward view of two faces and the corner between them; the brace pattern, glass tone, mullion grain and base were read from it.
- DataSF building footprints / 2010 LiDAR — no usable record (the survey predates the tower).

## Verified dimensions and location

| Item | Value | Basis |
|---|---:|---|
| Height to spire tip | **244.4 m** | published; OSM tag agrees |
| Crown | sloped, 206 → 220 m | estimated |
| Plan | 39 × 34 m at grade → 29 × 25 m at the crown, chamfered corners | OSM OBB (measured) + taper estimated |
| Anchor | **-122.3953090, 37.7897660** | measured (OSM OBB centre via `tk.run`) |

## Orientation

Faces at 45° / 135° / 225° / 315° (OSM bearing 45.1°); the plan's long axis runs
along Mission/Howard (local +X, bearing 45°). The tower stands on the east side of
Fremont St, so its Fremont frontage is the SW face (inferred from the anchor lying
east of Salesforce Tower). +Y = true north; the model is authored in world orientation.

## Recognition cues (ranked)

1. **The mega-braces**: white diagonal bars standing proud of the glass. In the photo
   each brace runs from near one corner at its base to the far corner halfway up, and
   back — so every face carries two stacked X's and every corner is wrapped by a tall
   diamond. The draft had a single "A" per face; the photo does not show that.
2. The slender, chamfered, tapering prism.
3. Pale aqua glass with a dense white vertical mullion grain.
4. The sloped crown and the spire.

## Preserved

- 244.4 m crest, OSM heading and plan size, chamfered corners, taper.
- Brace topology (stacked X's + mid-height and under-crown ties).
- Mullion grain (fins every 4.5 m), glazed lobby behind white columns.

## Simplified

- Brace nodes placed at exact half-height; real node heights differ slightly.
- Mullions every 4.5 m instead of every module; floor lines grouped in 7.6 m bands.
- Crown reduced to one sloped glass wedge with a white rim.
- Lit panes behind braces and mullions are removed (they would be hidden anyway and
  would fail the glow-outward check).

## Uncertainties

- Only two faces are photographed; the other two are inferred identical.
- Crown slope direction (low SE, high NW) and roof heights are estimated.
- The OSM footprint is an irregular 10-node polygon (it likely includes the base's
  bridge/podium edge); the model uses a symmetric chamfered rectangle on its OBB.
- Category `3` (office) for a mixed office/residential tower is a judgement call.
