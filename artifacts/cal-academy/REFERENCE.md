# California Academy of Sciences reference dossier

Research checked 2026-08-10. Facts below distinguish published figures from
visual inference. No third-party reference imagery is committed with the model;
the model and review renders are original. This dossier corrects two claims in
`docs/asset-plans/cal-academy.md` (see *Corrections to the plan*).

## Verified facts

| Item | Value | Confidence / source |
|---|---:|---|
| Address | 55 Music Concourse Drive, Golden Gate Park, San Francisco | OSM tags, calacademy.org |
| WGS84 anchor | **-122.4662432, 37.7698424** | OSM way/28695389 centroid, recomputed from live Overpass geometry this session; matches the plan anchor exactly |
| Footprint (oriented bbox) | **161.3 × 102.5 m**, ~16,400 m² | OSM way/28695389, measured locally in the project tangent projection |
| Long-axis bearing | **48.3° / 228.3° true**; short axis 138.3° / 318.3° | Computed from OSM edge geometry (long edges 48.3°, short edges 138.0°/317.9°) |
| Roof plane elevation | **~10 m** above ground | RPBW project page ("lifted 10 m above the ground") |
| Perimeter canopy / eave | **11.3 m** | Fondazione Renzo Piano project data ("11,3 canopy") — agrees with OSM `height=11` |
| Maximum height (hill peaks) | **19.3 m** | Fondazione Renzo Piano ("19,3 m max") |
| Floors | 3 above grade + 2 basements (OSM tags 5 levels) | Fondazione Renzo Piano; OSM |
| Roof area | 18,302 m² (2.5-acre living portion, 87% planted) | Fondazione Renzo Piano; calacademy.org |
| Roof hills | **Seven** (SF's seven hills), incl. two dominant domes | calacademy.org Living Roof page; RPBW |
| Dome diameters | Planetarium **90 ft / 27.4 m**; rainforest **90 ft / 27.4 m** | Wikipedia (Morrison Planetarium, Osher Rainforest) |
| Central piazza canopy ("Bolla") | **27 m diameter** concave glazed spider-web canopy, open at center | Josef Gartner (facade contractor) project page |
| Perimeter glass canopy | **4,800 m²** glazed area at roof level with integrated PV | Josef Gartner |
| Photovoltaic cells | **60,000** in the canopy fringe, ~5% of building electricity | RPBW; Wikipedia; Fondazione |
| Living roof planting | 1.7 M native plants in 50,000 biodegradable trays | calacademy.org |
| Opened | September 27, 2008; architect Renzo Piano Building Workshop + Stantec | Wikipedia; RPBW |
| Skylight count | **Not published.** Aerial photography shows rings of circular automated skylights around the two main domes plus scattered portholes | Multiple sources describe them; no source gives a count — treated as design freedom |

## Corrections to the plan (`docs/asset-plans/cal-academy.md`)

1. **The entrance faces north-west, not north-east.** The task prompt says "the
   main entrance faces the Music Concourse on the north-east." Live OSM geometry
   places the Music Concourse and the de Young Museum (~-122.4688, 37.7715)
   north-west of the Academy; the 161 m front facade's outward normal bears
   **~318° true (NW)**. The plan's "~171° cw from true north" orientation note
   is also inconsistent with the measured 48.3°/138.3° edge bearings.
2. **`targetHeightM` must be 19.3, not 11.** OSM's `height=11` describes the
   flat perimeter canopy (Fondazione RP: 11.3 m), while the roof hills crest at
   19.3 m. The loader scales by `targetHeightM / measuredHeight` against the
   model's full bounding box; a model containing 19.3 m peaks scaled to 11 m
   would shrink the footprint ~42%. The plan itself flags this as its most
   consequential unknown (§2.15) — resolved here with the architect's own figure.

## Source list and what each establishes

- [OpenStreetMap way/28695389](https://www.openstreetmap.org/way/28695389) —
  footprint polygon (fetched live via Overpass), centroid anchor, edge bearings,
  `height=11`, 5 levels, glass material, grass roof. Geometry measured locally
  in the project's tangent projection.
- [Fondazione Renzo Piano — project data](https://www.fondazionerenzopiano.org/en/project/california-academy-of-sciences/) —
  the authoritative dimensional split: **19.3 m max height, 11.3 m canopy**,
  3 + 2 floors, 18,302 m² roof, 60,000 PV cells, design/construction dates.
- [RPBW — California Academy of Sciences](https://www.rpbw.com/project/california-academy-of-sciences) —
  roof plane "lifted 10 m", 37,000 m² complex, the concave spider-web piazza
  canopy, three historic halls retained inside, automated dome skylights.
- [calacademy.org — Living Roof](https://www.calacademy.org/exhibits/living-roof) —
  owner's description: 2.5 acres, **seven hills**, 87% planted, 1.7 M plants,
  50,000 trays, storm-water capture, automated skylights + weather stations.
- [Josef Gartner / Permasteelisa project page](https://josef-gartner.permasteelisagroup.com/project-detail?project=2212) —
  facade contractor: **27 m diameter "Bolla"** piazza canopy, **4,800 m²**
  perimeter glazed canopy with integrated PV, 350 prefabricated wall units.
- [Wikipedia — California Academy of Sciences](https://en.wikipedia.org/wiki/California_Academy_of_Sciences) —
  90 ft diameters for both the Morrison Planetarium and Osher Rainforest domes,
  opening date, 400,000 sq ft size, LEED Platinum, 60,000 PV cells.
- [Dezeen](https://www.dezeen.com/2008/10/03/california-academy-of-sciences-by-renzo-piano/) and
  [Designboom](https://www.designboom.com/architecture/renzo-pianos-california-academy-of-science/) —
  architectural-press descriptions of the undulating roof, the "lift a piece of
  the park" concept, and photography of all elevations used to cross-check
  massing, eave depth, mullion rhythm and skylight distribution.
- Aerial/satellite imagery (Google/Bing/OSM-listed imagery reviewed, not
  committed) — hill placement, skylight ring positions around the two domes,
  PV fringe location on the flat perimeter, piazza position at center.

The "27.43 m high free-standing domes" phrasing found in some case-study
aggregators is a garbled restatement of the 27.4 m (90 ft) *diameters*; the
architect's own 19.3 m max height is used instead.

## Orientation

The long axis bears **48.3° true** (ENE–WSW in casual terms; NE–SW formally).
The model is authored with Blender `+Y` = true north, `+X` = east: the local
long axis is yawed **+41.7° CCW from +X**, which places the front (concourse)
facade normal at **318.3° true — north-west**, facing the Music Concourse and
the de Young across it. The loader applies no rotation, so the GLB drops into
the city at this real heading. There is no separate "front = −Y" concession:
this asset's identity is its roof, and the true heading governs (same decision
hierarchy as the Salesforce Tower asset, which also keeps its measured yaw).

## Directional observations

### North-west (front, Music Concourse)

- A thin, very long horizontal composition: dark glass wall band under a deep,
  flat, white-fascia canopy that reads as a floating line.
- The eave overhang is deep (the 4,800 m² glazed PV canopy) — the strongest
  ground-level cue after the roof itself.
- Central main entrance; regular fine mullion rhythm across the whole facade.
- The green hills bulge above the eave line: the two big domes read clearly
  even from the ground.

### North-east / south-west (short ends)

- Same glass-under-eave language, ~103 m wide.
- From these ends the roof reads as a single big hill in profile (one dome
  fronting the other).

### South-east (rear, toward the AIDS Memorial Grove)

- Service side; plainer, with back-of-house massing behind the same glass and
  eave language. Simplified to the identical facade system in the miniature —
  the asset never shows a "dead" elevation.

### Top (the hero view)

- A green undulating field filling the wall line; **two dominant round hills**
  (planetarium WSW of center, rainforest ENE of center) flanking the circular
  glazed piazza at dead center; **five smaller mounds** asymmetrically placed
  toward the corners and rear.
- **Rings of circular porthole skylights** wrap the lower slopes of both big
  domes (they read like crater fields from the air); more portholes scatter
  across the secondary mounds.
- The **flat perimeter band** carries the PV fringe: a dark speckled strip
  inboard of the white fascia, running the whole way round.
- The piazza is a crisp round hole: white spider-web canopy, open center,
  glazed courtyard walls visible below.

## Day and night appearance

- **Day:** vivid but natural green roof (drought-hardy natives are golden-green
  in late summer; rendered as the project's clean toy green), white eave
  fascia, dark PV band, dark tinted glass walls in shadow under the overhang.
- **Night:** the roof goes dark; the glass perimeter glows warmly from inside,
  the porthole skylights glow from the lit exhibit halls below, and the piazza
  becomes a luminous core under the spider-web canopy. The miniature's night
  state (all via the `_Glow` material contract, emissive only in the app's
  night pass): the **piazza canopy dish** (`Toy_white_Glow`) is the white
  lantern at the heart of the roof; the **26 porthole rims**
  (`Toy_white_Glow`) become rings of light on the dark hills; a **clerestory
  ribbon** at the top of the glass walls (`Toy_gold_Glow`) runs the whole
  perimeter under the floating eave — the lit interior seen through the
  glass, visually broken into warm bays by the dark mullions; and the
  **entrance doors** (`Toy_trim_Glow`) mark the NW front. By day every glow
  surface matches its non-glow palette neighbour (white rims stay white, the
  gold ribbon hides in the eave shadow, the cream doors read as trim), so the
  daylight look is unchanged.

## Strongest recognition cues (ranked)

1. **The undulating living green roof** — seven rounded hills, two dominant —
   no other building in San Francisco has one.
2. **Circular porthole skylights** ringing the domes like craters.
3. **The very low, very wide profile** — a park block, not a building block.
4. **The thin flat floating eave** with its dark PV fringe wrapping the whole
   perimeter above continuous glass walls.
5. **The round central piazza** punched through the green field.

## Translation to the SF-SIM miniature style

### Preserved

- 161.3 × 102.5 m footprint, 48.3° long-axis bearing, base-center origin.
- The 10 m roof plane / 11.3 m eave / 19.3 m peak vertical split.
- Two 27 m-class dominant domes flanking a central 27 m piazza; seven hills
  total, asymmetrically placed.
- Skylights as real geometry, ringing the dome slopes.
- The deep flat overhanging eave with PV fringe, contrasting the curved hills.
- Continuous glass perimeter under the eave.

### Simplified / exaggerated

- The living roof becomes one smooth displaced surface with clean toy-green
  material — no plant geometry, no seasonal browning.
- Unpublished skylight count → **26 modelled portholes** (two rings of eight
  around the big domes + scattered on the mounds), semantically enlarged to
  ~3.6 m diameter so they read from the app camera.
- Fine mullions → chunky white mullions on a ~6.7 m rhythm; corner notches in
  the OSM footprint (3–4 m service notches) are dropped.
- The spider-web canopy becomes a white rim + 12 radial ribs + 2 ring ribs
  over a shallow concave glass dish with an open oculus.
- The PV fringe becomes a flat dark band inset on the eave top.
- Entrance = a modest recessed portal + steps at front center; the roof is the
  identity, so no oversized signage is added (style bible §8 "exaggerate
  meaningful identifiers" — here that is the roof, not a wordmark).

## Uncertainties and conflicting evidence

- **Skylight count and diameters are unpublished.** Design freedom exercised;
  documented as such. Real portholes are ~2–3 m; modelled at 3.6 m for
  city-scale readability.
- **Hill positions beyond the two domes** are read from aerial photography,
  not surveyed drawings; the five secondary mounds are placed to match the
  photographed asymmetry (heavier toward the rear/SE and the WSW end).
- **Eave depth varies** in reality (deepest at the front entry bay). The
  miniature uses a constant 8.5 m overhang, inside the 4,800 m²-derived ~9 m
  average, for a clean toy silhouette.
- The "27.43 m high domes" claim in aggregator articles conflicts with the
  architect's 19.3 m max height; resolved in favor of Fondazione Renzo Piano
  (the 27.4 m figure is the domes' diameter).
