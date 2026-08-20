# Hills Brothers Building — reference dossier

Research base for the SF-SIM miniature of 2 Harrison Street (Hills Bros. Coffee
Plant, SF Landmark No. 157). Compiled 19 August 2026 for the build in this
folder; the asset plan is `docs/asset-plans/hills-brothers-building.md`.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| SF Planning HPC Certificate of Appropriateness, case 2011.0417A (PDF, sfplanning.org meeting archive) | Authoritative property description: six-storey concrete building clad in red brick, wood/steel industrial sash, flat roof with **tall parapet**, rooftop penthouse and tower, large neon "Hill Bros Coffee" signage; Block 3744 Lot 005; 1985 seventh-floor rooftop addition (non-historic); 2011 roof deck ~24 in above the built-up roof, 42 in below the parapet crest. Attachments: parcel map, 1998 Sanborn sheet, **oblique aerial photo**, **Pier 14 elevation photo**, roof/parapet photo. |
| DataSF LiDAR building footprints (`ynuv-fyni`), building `201006.0000430` | The building's own merged trace (15,681 half-metre cells): ground 3.49 m NAVD88, roof mode 23.88 m, median 26.23 m, sd 9.44 m (bimodal), **max 53.16 m** — the tower. Neighbouring row `201006.0000159` (the 1989 complex) has its own 68.46 m max (the condo tower), proving the 53.16 belongs to this building. |
| OSM relation/2280956 | Footprint measured via Overpass: outer ring 3,526 m², OBB 75.8 × 57.1 m at 45° to true north; inner lightwell ring 247 m²; `height=56` tag (consistent with the flagpole tip, not used). |
| PCAD 1355 (pcad.lib.washington.edu/building/1355/) | Kelham attribution, 1926 construction, the razed 1950s north addition, Hills Plaza chronology. |
| noehill.com/sf/landmarks/sf157.asp | Landmark 157; patterned brickwork, arched doorways and windows, bronze grillwork doors; the tower was decorative **and functional** (gravity bean blending). |
| hmdb.org/m.asp?m=72585 (historical marker) | "Mediterranean Romanesque", 1924 date for design; the south tower stored beans. |
| Wikipedia "Hills Brothers Coffee" | Landmark status; Wharton SF (2012), Google and Mozilla tenancy. |
| LoopNet listing 2 Harrison St ("Hills Plaza 2") | 7 storeys today, 213,731 SF, ~30,213 SF plate, renovated 1989. |
| Wikimedia Commons `Hills Bros. Building - San Francisco.JPG` | Night state from the bay: the sign lit red, the tower arcade lit warm; sign at the south end of the roof. |
| Wikimedia Commons `Hills Bros. Building - San Francisco.jpg` | The plaza triple-arch brick screen wall (1989 complex — out of scope, but confirms the brick language). |
| Esri World Imagery z19 nadir (19 Aug 2026) | Roof plan: quad + offset lightwell, terracotta penthouse roofs ringing the well on three wings, pale mechanical roof with equipment rows on the NE wing, tower pyramid at the NW flank, sign lattice near the Harrison corner. |

## Verified dimensions and location

- Footprint idealized to a 75.5 × 44.2 m rectangle (u along the Embarcadero
  facade, bearing 45/225) with the 15.8 × 15.7 m lightwell at building-frame
  u −11.5..4.3, v −1.5..14.2, and the tower projecting to v 34.9 at
  u −11.1..4.3. Max deviation from the measured OSM ring 0.5 m.
- Heights used: deck 23.9 (LiDAR mode), parapet 25.6 (deck + HPC roof-deck
  arithmetic), penthouse walls 27.9 / crest 29.5 (estimated, LiDAR shoulder),
  tower crest **53.2 m** = `targetHeightM` (LiDAR max; flagpole above omitted).
- Anchor: OSM outer-ring bbox centre `-122.3892854, 37.7894167`.
- Orientation: Embarcadero facade normal 135° true (SE); Harrison to the SW;
  the tower projects NW toward the mid-block plaza.

## Observations by side

- **SE (Embarcadero, hero):** two-storey base with tall segmental-arched
  openings and bronze-grille doors; four floors of paired rectangular sash
  between brick piers (~13 structural bays); arcaded sixth floor of
  round-arched windows; corbel band; tall parapet with light coping. The neon
  sign rides above the parapet near the Harrison end, face to the bay.
- **SW (Harrison):** same grammar, 44 m; principal entrance arch; the Bay
  Bridge approach passes diagonally just south.
- **NW (plaza):** the campanile: smooth brick shaft with paired slit windows,
  arcaded top stage (tall narrow arches), corbelled cornice, low parapet,
  terracotta pyramid roof, finial + flagpole with US flag.
- **NE (Folsom side):** same brick grammar, shorter; the 1989 complex beyond.
- **Top:** flat roof ring around the lightwell; the 1985 penthouse reads as
  cream volumes with hipped terracotta roofs on the SE/SW/NW wings; the NE
  wing carries a pale roof with mechanical rows; a cream gable with an arched
  window peeks over the sign; the 2011 roof deck sits behind the parapet on
  the SE wing.

## Recognition cues (ranked)

1. The campanile silhouette — shaft, arcade, corbel, terracotta pyramid
2. The rooftop "HILLS BROS COFFEE" sign facing the bay (red neon at night)
3. Red brick quad with the arcaded top floor, right at the water beside the
   Bay Bridge touchdown
4. The lightwell + terracotta penthouse ring seen from above

## Preserve / simplify

Preserved: true 45° heading, quad + lightwell massing, tower stage
proportions, sign as the night hero, arcade floor, penthouse hip ring.
Simplified: bay count kept at the module (~12 bays SE), paired sash → one
recessed pad per bay, patterned brick → trim bands (base band, corbel band,
parapet cap), tower arcade 4 arches/face (2 on the embedded SE face), sign
letters as chunky blocks (three word-groups, not literal typography),
mechanical clutter → four tidy blocks, flagpole omitted above the 53.2 m
finial.

## Uncertainties and conflicts

1. **Tower crest vs flagpole:** LiDAR max 53.16 m is a single-point statistic
   and the tower flies a flag on a pole; the masonry crest could be a few
   metres lower (OSM 56 supports "pole above 53"). Taken as the finial crest;
   flagged in REPORT.md.
2. **Penthouse and parapet heights are derived**, not published (HPC gives
   relative inches, LiDAR gives the deck mode). No published architectural
   height exists anywhere for this building.
3. **Tower stage heights** (shaft 40.2 / arcade 47.8 / pyramid spring 49.0)
   are proportioned from oblique photos, not measured drawings.
4. The case-report header says "Block 4108 Lot 010" while the motion, parcel
   map and decision all say Block 3744 Lot 005 — the latter is used.
5. The LiDAR footprint merges two low plaza-side strips beyond the OSM ring
   (arcade/screen structures); they are excluded from the asset and matter
   only to the integration exclusion analysis.
