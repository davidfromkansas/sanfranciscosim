# Pier 9 — reference dossier

Research base: `docs/asset-plans/pier-9.md` Part 2 (compiled the same session), verified
against the primary sources below. This file records what the model relies on and where
each number comes from. Confidence labels: **documentary** (published/official),
**measured** (computed this session from a named dataset, reproducible),
**photogrammetric** (pixel solve, method in plan 2.16), **observed** (read from
photographs), **inferred**.

## Sources

| Source | What it establishes |
|---|---|
| NRHP #06000372 nomination Sec. 7, pp. 135–137 (Corbett, Jan 2006; sfport.com `EmbarcaderoRegisterNominationSec7.pdf`) | **The primary document.** 1936–38 construction (substructure A. W. Kitchen, shed+bulkhead Barrett & Hilp); designers G. A. Wood (shed/substructure) and H. B. Fisher (bulkhead) under Frank G. White; twin of Pier 19, 153 ft × 800 ft; steel-frame shed, scored precast walls, roll-up doors, continuous full-length roof monitor, steel sash + wire glass; east elevation "faintly Art Deco", six profiled piers, gabled central pavilion + flagpole; bulkhead: timber-framed stucco, classical, central pavilion, monumental arch, gabled parapet, `PIER 9` raised metal letters, flagpole; rail spur each apron, bitts/cleats/fender piles |
| Same document, bulkhead-wharf Section 6 (pp. 45–48) | The 1917 bulkhead wharf under the bulkhead building (Clinton Construction, A. C. Griewank plans); site history: Pier 11 (1890s) demolished 1935; pre-1918 "Pier 9" = today's Pier 7 |
| NoeHill district table | "Pier 9 (Ferryboat Klamath), The Embarcadero at Vallejo Street", contributing |
| David Baker Architects project page | Bar Pilots Station House at the end of Pier 9, renovated 1992, 19,560 sf |
| Port Commission memo 2006-10-18 | Bar Pilots lease: ~19.7k sf office + ~20.1k sf shed + ~14.3k sf apron |
| Port of SF WRP012 one-pager (2022) | Bar Pilots + WETA berth vessels at Pier 9; seismic retrofit context |
| Construction Dive / Metropolis / Knowles / Lundberg | Autodesk Pier 9 Workshop 2013–2021, 35,000 sf, south aisle; tugboat berthing on the south apron |
| OSM way 25478417 + DataSF `ynuv-fyni` area_id 77 | Footprint: OBB 254.3 × 49.3 m, area 9,268 m², axis 054.59° — the two datasets agree to < 0.7 m (**measured**) |
| DataSF LiDAR (`SF9900009`, twin `SF9900019H`) | zmax 18.19 / 18.76 m NAVD88 → crest ≈ 15.0–15.1 m above deck (**measured**, datum caveats in plan 2.16) |
| Commons `Pier 9, San Francisco.JPG` (head-on facade) | The photogrammetric solve: arch-radius scale → springing 3.4, intrados crown 8.3, archivolt 9.5, letters band 11.6, gable apex 13.7, attic 15.0, wing parapet ~8.5 (**photogrammetric**) |
| Commons Coit Tower aerial (`Pier 9 and Pier 15 with construction crane`) | Dark built-up roof, full-length monitor with pale glazing, south-plane plant crowd, cleaner north plane, north-apron container run, Bar Pilots lookout + masts, end block (**observed**) |
| Commons `San Francisco Pier 9.jpeg` (night) | The arch glows warm at night — the night-state hero (**observed**) |
| Esri World Imagery z19, pier-frame ortho at 0.33 m/px | Apron widths (~10 m N / ~4 m S), monitor position on the shed centreline, deck edges (**measured**) |
| App `terrain.bin`, sampled directly | DEM ridge 2.4–2.5 m along the centreline, 0 past along ≈ +110; anchor sample 2.50 m (**measured**) |

## Verified dimensions and location

- Building ring in the pier frame (along −127.5…+126.8 from the OBB-centre anchor):
  bulkhead −127.5…−116.5 full width (−23.8…+25.3); shed head −116.5…−91 (north wall
  −20.3); north-wall loft −91…−78 (→ −14.9); main shed −78…+126.8 (walls −14.9 / +19.9,
  centreline +2.6); south taper −116.5…−104 (+23.9 → +19.9). **Measured** (DataSF ring).
- Deck: ~49 m wide; north apron ~10 m, south ~4 m beside the main shed. **Measured.**
- Anchor (model bbox centre, from the build's recentre report):
  **−122.3967994, 37.8006708**. The plan's design anchor differed by 0.8 m; the built
  value is authoritative.
- Heights above deck: shed eaves 7.3 (inferred, OSM `height=8` ≈ eaves); monitor top
  10.3 (inferred from ortho + oblique); wing parapet 8.5 (photogrammetric ±0.8); gable
  apex 13.7, attic crest **15.0** (photogrammetric + dual-LiDAR corroborated).
- Deck datum: origin at deck top; fascia + pile stubs to −2.6 (pier-1 precedent; the
  DEM ridge seats the origin at ~2.5 m and falls to 0 at the tip).

## Recognition cues (ranked, from plan 2.5)

1. The gabled frontispiece: banded piers, big arch, `PIER 9`, gable + pylons + attic.
2. The dark roof with the pale continuous monitor spine.
3. 254 m of length at 54.6°, parallel to Piers 1/3.
4. The working clutter: containers north, plant south, Bar Pilots lookout + masts at the tip.
5. The grey/cream/near-black three-value discipline with no third hue.

## Preserved / simplified / omitted

- **Preserved:** real heading and footprint decomposition incl. the south offset of the
  shed and the head taper; the frontispiece composition; the monitor; the dark roof; the
  asymmetric aprons with rail-spur score lines; the Bar Pilots end; fender/bollard/lamp
  rhythm; pile stubs under the deck edge.
- **Simplified:** shed bays to a 7.5 m repeating unit with one high window band; the
  plant crowd to 13 curated boxes; containers to 6; the arch screen to doors + shutter +
  mullion cross; banded piers to 4 proud bands; the end elevation to 6 pilasters +
  gable + pole.
- **Exaggerated:** arch width ×1.15 (9.8 → 11.3 m); letters extruded at 1.15 m.
- **Omitted:** the full-height flagpole (bbox-top trap, pier-3 §2.15 — the attic block
  must set `targetHeightM`); all vessels; the WETA float; interior fit-outs; palms and
  the Embarcadero.

## Uncertainties carried

Wing parapet (8.5 ± 0.8) and shed eaves (7.3, inferred) are the softest numbers; the
monitor's height/width are read from imagery; the end elevation and Bar Pilots volumes
are modelled restrained because they are described (NRHP) but barely photographed; the
container run and plant crowd are 2015–2020 observations. None of these can rescale the
asset — the bulkhead crest sets the bounding box.
