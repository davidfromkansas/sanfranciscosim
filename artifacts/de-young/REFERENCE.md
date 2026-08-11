# de Young Museum — reference dossier

Research for the SF-SIM miniature asset, compiled 2026-08-10. All geometric
figures below were re-measured independently from OpenStreetMap survey geometry
(Overpass API, relation 1652482 and its members) rather than taken from the
asset plan; published facts were cross-checked against at least two sources.
The plan's dossier (`docs/asset-plans/de-young.md` Part 2) was treated as a
starting hypothesis and is corrected in several places below.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM relation 1652482](https://www.openstreetmap.org/relation/1652482) (Overpass full geometry) | Footprint outline (2 outer rings, 5 inner court rings), `height=13` for the main mass, address, Wikidata `Q1470276` |
| [OSM way 444230154 "Hamon Tower"](https://www.openstreetmap.org/way/444230154) | The tower's projected outline — decomposes into the base slab on the museum grid and the twisted top slab (measurements below) |
| [Wikipedia — de Young Museum](https://en.wikipedia.org/wiki/De_Young_Museum) | 2005 building by Herzog & de Meuron with Fong & Chan; Hamon Observation Tower "144 feet tall", ninth-floor observation level, tallest point in Golden Gate Park; 163,118 sq ft of copper cladding, "variably perforated and dimpled copper plates" engineered by Zahner; copper intended to oxidize green; seismic base isolation (up to 3 ft travel) |
| [Zahner project/press pages](https://azahner.com/projects/de-young/) (via search extracts) | ~950,000 lb of copper in ~7,200 panels (sources vary 7,200–8,000), 920,699 perforations, ~1,500,000 dimples; perforation pattern derived from photographs of the park's tree canopy; intended gradual green patina |
| [EAT DRINK SEE ARCHITECTURE — de Young](https://www.eatdrinkseearchitecture.com/deyoung-museum) | "A twisting 144 foot tower anchors the design and turns to align with the city grid beyond"; "the entrance is cut out of the facade and leads to an open air courtyard"; light wells filled with ferns; cantilevered roof |
| [goldengatepark.org — museums](https://goldengatepark.org/great-museums) | Corroborates the tower twisting to align with the city street grid at its top; nine stories |
| OSM way 28695389 (California Academy of Sciences) | The Academy's edges bear the same 48°/138° grid — confirms the shared Music-Concourse grid and that the concourse (and therefore the museum entrance side) is the **south-east** side of the de Young |

## Verified dimensions and location

All bearings are degrees clockwise from true north. "Grid frame" = coordinates
rotated so **u** runs along the building's long axis (bearing 48.2°, pointing
NE) and **v** across it (+v = bearing 138.2°, toward the Music Concourse).

| Item | Value | Confidence |
|---|---|---|
| Museum grid bearing | long axis **48.2°** (edges measured 48.1–48.3° across both outer rings and the Academy) | measured, high |
| Overall footprint (oriented) | **153.7 m** along the axis × **76.1 m** across | measured, high |
| Footprint area | 9,732 m² (main ring) + 1,248 m² (NE wing) ≈ **11,000 m²** | measured, high |
| Main mass height | **13 m** (OSM tag; visually consistent — the 43.9 m tower reads ≈ 3.4× the roofline in elevation photographs) | medium (single mapped source + visual check) |
| Hamon Tower height | **144 ft = 43.9 m**, nine stories, top-floor observation deck | published, high |
| Tower base slab | **9.4 × 27.9 m**, long axis on the museum cross-grid (bearing 138.2°), at grid position u ≈ [58.4, 67.8], v ≈ [−37.9, −10.0] (NE end of the building, JFK-Drive side) | measured, high |
| Tower top slab | **11.2 × 20.4 m**, long axis bearing ≈ **169°** — the top is *wider and shorter* than the base | measured, medium (traced outline) |
| Tower twist | **~31° clockwise** (viewed from above) from base to top as mapped; exact alignment with the true-cardinal avenue grid would be **41.8°**. Direction is unambiguous: clockwise. | measured + published parti |
| Footprint center (WGS84) | ≈ **−122.46872, 37.77150** — note the plan's anchor (−122.4681752, 37.7718982) is ~65 m NE of the footprint center, near the tower | measured, high |
| Opened | October 15, 2005 | published, high |

## Orientation

- The long copper band runs **SW → NE** at bearing 48.2°. (The plan dossier's
  "~171° cw from true north / roughly north-south" is **wrong** — it appears to
  describe a different axis. The Academy of Sciences across the concourse
  shares the 48°/138° grid, which settles it.)
- The **Music Concourse and main entrance are on the south-east long side**
  (+v). The Academy of Sciences faces it from the other side of the concourse.
- **JFK Drive is on the north-west long side** (−v).
- The **Hamon Tower stands at the NE end**, toward the JFK-Drive (NW) side,
  with the education wing's angular "prow" continuing past it to the NE tip.
- The tower twist: base merges with the museum grid; the top slab rotates
  **clockwise** so its long axis approaches true north–south — the architects'
  stated parti is that the top aligns with the city's avenue grid.

## What each side shows

- **South-east (concourse front):** a long, low, almost windowless copper wall;
  the entrance is a cut-out in the facade under the cantilevered roof blade,
  leading into an open-air entry court; the tower rises beyond the NE end.
- **North-east:** the angular prow of the wing and the tower's base slab; the
  twist is most legible here — the wide face of the top slab swings toward the
  viewer while the base presents its narrow edge.
- **North-west (JFK Drive):** long copper band with the two narrow light-court
  "canyons" reading as slots in the roofline; the tower base sits nearly flush
  with this facade.
- **South-west:** the tapering end of the band with ground-level glazing at the
  café/education corner.
- **Above:** a large angular copper roof plane (now visibly weathered), pierced
  by two broad rectangular courtyards toward the SE side and two long narrow
  canyons en echelon toward the NW side, plus skylight strips; the twisted top
  slab of the tower reads clearly against the low roof.

## Courtyards (measured, grid frame, local coords centered on the footprint)

| Court | u range | v range | Size | Reading |
|---|---|---|---|---|
| West court | −73 … −30 | +5 … +20.5 | 43 × 15.5 m | broad open court |
| Entry court (two mapped rings merged) | +15 … +52 | +5 … +20 | 37 × 15 m | the open-air entrance court, connected to the SE facade |
| Canyon 1 | −70 … −11 | −16 … −10 | 59 × 6 m | narrow fern light-well slot |
| Canyon 2 | −3 … +52 | −11 … −5 | 55 × 6 m | second slot, en echelon with the first |

(The fifth mapped inner ring is a ~51 m² light well — dropped at miniature scale.)

## Strongest recognition cues (ranked)

1. **The twisting tower** — a narrow copper slab rotating clockwise to the city
   grid; the only twisting structure in the city.
2. **The long, almost windowless copper band** — 154 m of weathered metal, low
   and horizontal, in a park.
3. **Weathered copper color** — brown-bronze walls with green patina strongest
   on skyward surfaces (2026 state: 21 years of coastal exposure).
4. **The angular plan** — the NE prow, the en-echelon canyon slots, and the
   courtyard voids cut through the roof.
5. **The cantilevered roof blade over the cut-out entrance** on the concourse side.

## Features to preserve

- 44 m tower over a 13 m band — the height contrast is the composition
- Twist direction (clockwise) and the slab (not square) tower section; the top
  wider and shorter than the base
- Tower position: NE end, NW side
- Real oriented footprint 154 × 76 m and the entrance on the SE long side
- Two wide courts + two narrow canyons, en echelon, as roof voids
- Copper distinct from every other material in the diorama

## Features to simplify / exaggerate

- Perforated/dimpled skin → flat `Toy_rust` copper; no texture (contract)
- Patina → a graphic rule: every skyward copper surface is `Toy_verdigris`
  green, every wall face is still brown — reads as 20 years of weather without
  painted-on noise
- The twist → modeled at **42°** (full city-grid alignment, the architects'
  parti) rather than the traced ~31°: the signature feature, deliberately
  completed for legibility (style bible §8/§22-4)
- Five mapped voids → four (two courts, two canyons); micro jogs in the NE end
  wall → one clean prow cut
- Facade slit windows → a handful of dark recessed-reading glass slots
- Skylights → three slim dark strips on the roof
- Night lighting → the repo glow contract: the observation lantern in
  `Toy_white_Glow` plus a warm `Toy_gold_Glow` entry sequence (court liners,
  passage walls, slit windows, café corner), each paired with a dark glass
  backing pane so the day read survives the loader's 12 % day opacity;
  canyons and the west court stay dark for contrast (owner request
  2026-08-10, extending §2.8 of the asset plan)

## Uncertainties and conflicting evidence

- **Twist magnitude:** OSM's traced outline gives ~31°; exact top alignment to
  the cardinal avenue grid implies 41.8°; press describes only "aligns with
  the city grid at top." One tourism source inverts base/top — dismissed, since
  the mapped base slab is physically continuous with the museum-grid wing.
  Decision: model 42°, document both.
- **Main-mass height** rests on the OSM `height=13` tag; consistent with
  elevation photos against the known 43.9 m tower. Risk: low.
- **Patina state:** sources agree the copper is oxidizing toward green but no
  source quantifies the 2026 color; the wall-brown/roof-green split is a
  deliberate graphic interpretation.
- **Wikidata id:** OSM tags the building `Q1470276`; the plan dossier cites
  `Q1181491`. Not load-bearing for the asset.
- **Anchor:** the plan's anchor is not the footprint center (it sits ~65 m NE,
  near the tower). Because the loader positions the GLB's base-center origin at
  the anchor, this asset's manifest draft uses the measured footprint center.

No reference imagery is committed; all observations above are from the listed
public sources and measured open data.
