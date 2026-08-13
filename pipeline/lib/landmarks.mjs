// Bespoke landmark registry: true coordinates, the exclusion radius that keeps
// procedural footprints from fighting the hand-built model, and the camera
// preset the runtime flies to. Consumed by buildings.mjs (exclusion) and
// emitted to the app as landmarks.json (presets + placement).
//
// A landmark is normally one circle around its anchor. A site whose lot carries
// more than one baked footprint can declare `extraExclusions: [{lon, lat, r}]`
// for the ones a single radius cannot reach without eating a neighbour — see
// 551Third. Build the zone list with exclusionZones() below rather than reading
// `exclude` directly, so the bake and audit 1.6 can never disagree about what
// is cleared.

export const LANDMARKS = [
  {
    id: 'goldenGateBridge',
    name: 'Golden Gate Bridge',
    lon: -122.4783,
    lat: 37.8199,
    height: 227,
    exclude: 900,
    key: '1',
    camera: { distance: 2600, yaw: 150, pitch: 22 },
  },
  {
    id: 'bayBridge',
    name: 'Bay Bridge',
    lon: -122.3771,
    lat: 37.7988,
    exclude: 700,
    key: '2',
    camera: { distance: 2400, yaw: 250, pitch: 22 },
  },
  {
    id: 'salesforceTower',
    name: 'Salesforce Tower',
    lon: -122.3969,
    lat: 37.7897,
    height: 326,
    exclude: 90,
    key: '3',
    camera: { distance: 900, yaw: 40, pitch: 18 },
  },
  {
    id: 'transamerica',
    name: 'Transamerica Pyramid',
    lon: -122.4028,
    lat: 37.7952,
    height: 260,
    exclude: 70,
    key: '4',
    camera: { distance: 800, yaw: 60, pitch: 20 },
  },
  {
    id: 'columbusTower',
    name: 'Columbus Tower (Sentinel Building)',
    lon: -122.4050266,
    lat: 37.7965554,
    height: 29,
    exclude: 35,
    camera: { distance: 260, yaw: 210, pitch: 16 },
  },
  {
    id: '555California',
    name: '555 California Street',
    lon: -122.4037741,
    lat: 37.7921047,
    height: 237.4,
    exclude: 70,
    camera: { distance: 800, yaw: 40, pitch: 18 },
  },
  {
    id: 'coitTower',
    name: 'Coit Tower',
    lon: -122.4058,
    lat: 37.8024,
    exclude: 60,
    key: '5',
    camera: { distance: 600, yaw: 200, pitch: 18 },
  },
  {
    id: 'sutroTower',
    name: 'Sutro Tower',
    lon: -122.4528,
    lat: 37.7552,
    height: 298,
    exclude: 160,
    key: '6',
    camera: { distance: 1400, yaw: 70, pitch: 20 },
  },
  {
    id: 'ferryBuilding',
    name: 'Ferry Building',
    lon: -122.3936,
    lat: 37.7955,
    exclude: 120,
    key: '7',
    camera: { distance: 700, yaw: 100, pitch: 16 },
  },
  {
    id: 'palaceOfFineArts',
    name: 'Palace of Fine Arts',
    lon: -122.4484,
    lat: 37.8029,
    exclude: 170,
    clearTrees: true, // the rotunda grounds are hand-modelled; scatter conflicts
    key: '8',
    camera: { distance: 700, yaw: 330, pitch: 16 },
  },
  {
    id: 'cityHall',
    name: 'City Hall',
    lon: -122.4193,
    lat: 37.7793,
    exclude: 110,
    key: '9',
    camera: { distance: 700, yaw: 90, pitch: 18 },
  },
  {
    id: 'oraclePark',
    name: 'Oracle Park',
    lon: -122.3893,
    lat: 37.7786,
    exclude: 190,
    camera: { distance: 900, yaw: 230, pitch: 28 },
  },
  {
    id: 'alcatraz',
    name: 'Alcatraz',
    lon: -122.423,
    lat: 37.8267,
    exclude: 300,
    camera: { distance: 1100, yaw: 170, pitch: 20 },
  },
  {
    id: 'paintedLadies',
    name: 'Painted Ladies',
    lon: -122.4326,
    lat: 37.7761,
    exclude: 55,
    camera: { distance: 260, yaw: 100, pitch: 12 },
  },
  {
    id: 'graceCathedral',
    name: 'Grace Cathedral',
    lon: -122.4128,
    lat: 37.7919,
    exclude: 80,
    camera: { distance: 500, yaw: 110, pitch: 16 },
  },
  {
    id: 'fairmont',
    name: 'Fairmont San Francisco',
    lon: -122.4100666,
    lat: 37.7924244,
    height: 99.06,
    exclude: 80,
    camera: { distance: 520, yaw: 110, pitch: 18 },
  },
  {
    id: 'stIgnatius',
    name: 'St. Ignatius Church',
    lon: -122.4506,
    lat: 37.7766,
    exclude: 80,
    camera: { distance: 550, yaw: 120, pitch: 16 },
  },
  {
    id: 'conservatoryOfFlowers',
    name: 'Conservatory of Flowers',
    lon: -122.4602321,
    lat: 37.7725965,
    height: 18.3,
    exclude: 70,
    camera: { distance: 260, yaw: 170, pitch: 16 },
  },
  {
    id: 'calAcademy',
    name: 'California Academy of Sciences',
    lon: -122.4662432,
    lat: 37.7698424,
    height: 19.3,
    exclude: 120,
    camera: { distance: 700, yaw: 225, pitch: 20 },
  },
  {
    id: 'deYoung',
    name: 'de Young Museum',
    lon: -122.4688156,
    lat: 37.7715,
    height: 43.9,
    exclude: 100,
    camera: { distance: 700, yaw: 135, pitch: 20 },
  },
  {
    id: 'operaHouse',
    name: 'War Memorial Opera House',
    lon: -122.4209170,
    lat: 37.7786126,
    height: 44,
    exclude: 62,
    camera: { distance: 700, yaw: 90, pitch: 18 },
  },
  // Fills its own Civic Center block with no attached neighbours, so a plain
  // radius works. Half the 122.6 m envelope is 61 m, but the block's south edge
  // is only ~40 m from this anchor and Hayes Street is ~20 m wide — 62 m would
  // reach real buildings on the far side. 55 m clears the Davies footprint (its
  // centroid sits ~5 m from the anchor) and leaves the Hayes and Grove
  // frontages alone.
  {
    id: 'daviesSymphonyHall',
    name: 'Davies Symphony Hall',
    lon: -122.4206030,
    lat: 37.7776227,
    height: 35,
    exclude: 55,
    camera: { distance: 620, yaw: 45, pitch: 18 },
  },
  {
    // The Veterans Building, the Opera House's twin across the memorial court.
    // Exclusion 58 m covers the 83 x 67 m footprint plus a margin (the Opera
    // House uses 62 for its larger 104 x 73 m plan).
    id: 'herbstTheatre',
    name: 'Herbst Theatre',
    lon: -122.4210157,
    lat: 37.7795789,
    height: 31,
    exclude: 58,
    camera: { distance: 700, yaw: 90, pitch: 18 },
  },
  {
    id: 'fishermansWharf',
    name: "Pier 39 / Fisherman's Wharf",
    lon: -122.4098,
    lat: 37.8087,
    exclude: 260,
    camera: { distance: 900, yaw: 180, pitch: 20 },
  },
  {
    id: 'stMarysCathedral',
    name: 'Cathedral of Saint Mary of the Assumption',
    lon: -122.4253877,
    lat: 37.7842352,
    height: 78.7,
    exclude: 90,
    camera: { distance: 700, yaw: 200, pitch: 20 },
  },
  {
    id: 'missionDolores',
    name: 'Mission Dolores Basilica',
    lon: -122.4269098,
    lat: 37.7643109,
    height: 41,
    exclude: 45,
    camera: { distance: 500, yaw: 90, pitch: 16 },
  },
  // A 7.00 x 23.83 m sliver two doors NE of 380Brannan on the same block face,
  // with party walls on both long sides. This is the TIGHTEST exclusion radius
  // in the registry and it has to be: 372-374 next door (DataSF SF3775021) is
  // itself a 7 m sliver, so its footprint centroid sits only 6.57 m from this
  // anchor. Measured from this anchor against the DataSF footprints excluded()
  // consumes:
  //
  //   own footprint centroid        0.59 m
  //   SF3775021 (372-374) centroid  6.57 m   <- the binding constraint
  //   nearest ring vertex, anything 11.98 m
  //
  //   exclude 1-6 m  -> drops 1 building (correct: this one only)
  //   exclude 7 m    -> drops 2 (eats 372-374, which has no GLB to replace it)
  //   exclude 9 m    -> what 380Brannan uses 60 m away; here it eats a neighbour
  //
  // 3 m sits in the middle of the (0.6, 6.5) window and also catches the
  // Overture/OSM gap-fill footprint for this parcel, whose centroid is 1.4 m
  // from the anchor. Do NOT raise it without re-running that measurement.
  {
    id: '370Brannan',
    name: '370 Brannan Street',
    lon: -122.3938572,
    lat: 37.7807602,
    height: 7.63,
    exclude: 3,
    camera: { distance: 150, yaw: 45, pitch: 28 },
  },
  // Mid-block in SoMa with neighbours a few metres off both flanks, so this
  // exclusion radius is deliberately TIGHT rather than generous. excluded() drops
  // a footprint if its centroid OR any ring vertex falls inside the radius.
  //
  // Measured against the 921 baked footprints in tiles 22..24_12..14, the target
  // (23_13 #102, h 20.5 m) sits 0.04 m from this anchor and its nearest neighbour
  // centroid is 13.3 m away:
  //
  //   exclude  9-12 m -> drops 1 building  (correct: #102 only)
  //   exclude 15 m    -> drops 2  (eats neighbour #146)
  //   exclude 18 m    -> drops 3
  //   exclude 35 m    -> drops 12 (a crater through the block)
  //
  // 9 m is the middle of the safe band. Do not raise it past 12 without re-running
  // that check — on a mid-block site a generous radius removes the neighbours.
  // 362 Brannan St (Standard Sheet Metal & Marine Plumbing, 1925) — a through lot
  // four doors northeast of 380, party walls on both flanks. `excluded()` in
  // buildings.mjs tests every ring VERTEX as well as the centroid, which is what
  // makes a generous radius dangerous here; measured against the real bake input
  // (data/buildings_datasf.geojson):
  //
  //   exclude  6-10 m -> drops 1  (correct: this building, centroid 3.49 m)
  //   exclude 11 m    -> drops 2  (eats 370 Brannan, nearest VERTEX 10.00 m)
  //
  // 8 m is the middle of the safe band. Do not raise it past 10. Note that
  // 370 Brannan's centroid is 13.33 m away — reasoning from centroids alone would
  // wrongly license 12 and delete it.
  {
    id: '362Brannan',
    name: '362 Brannan Street',
    lon: -122.393745,
    lat: 37.780843,
    height: 8.6,
    exclude: 8,
    camera: { distance: 200, yaw: 45, pitch: 24 },
  },
  // 358 Brannan, three lots northeast, is the tightest site in this registry: a
  // single 25-foot lot, 6.93 m wide, with both neighbours' walls ON the property
  // line. Measured against the committed tile 23_13 (233 footprints):
  //
  //   target #98 (the through-lot itself, h 11.2 m): centroid 4.06 m from the
  //   anchor, nearest ring vertex 2.47 m
  //   nearest neighbour #63 (350 Brannan, h 13.7 m): nearest vertex 12.01 m
  //
  //   exclude  3-12 m -> drops 1 building  (correct: #98 only)
  //   exclude 13-16 m -> drops 3  (eats BOTH party-wall neighbours)
  //   exclude 20 m    -> drops 5
  //
  // 7 m is the middle of the safe band. The baked footprint is TALLER than the
  // asset (11.2 m vs 9.6 m), so shipping the manifest entry without this
  // exclusion would hide the GLB completely rather than merely clash with it.
  {
    id: '358Brannan',
    name: '358 Brannan Street',
    lon: -122.3936350,
    lat: 37.7809258,
    height: 9.6,
    exclude: 7,
    camera: { distance: 190, yaw: 315, pitch: 26 },
  },
  {
    id: '380Brannan',
    name: '380 Brannan Street',
    lon: -122.3940217,
    lat: 37.7806308,
    height: 12.6,
    exclude: 9,
    camera: { distance: 220, yaw: 45, pitch: 24 },
  },
  // Full-lot corner building two lots northeast of 380, so the same TIGHT-radius
  // logic applies for the same reason. Measured against the 943 baked footprints
  // in the 3x3 cell block around 23_13:
  //
  //   target (23_13, 537 m2, h 13.7 m) centroid sits 0.01 m from this anchor
  //   nearest NEIGHBOUR: centroid 14.42 m, nearest vertex 16.21 m (165 m2, h 11.2 m)
  //
  //   exclude  6-14 m -> drops 1 building  (correct: the target only)
  //   exclude 16 m    -> drops 2  (eats that neighbour on its centroid)
  //   exclude 20 m    -> drops 3
  //
  // The binding limit is the neighbour's CENTROID at 14.42 m, not its nearest
  // vertex — excluded() tests centroid OR any ring vertex, so the centroid is
  // what bites first here. 8 m is the middle of the safe band. An independent
  // estimate off the OSM/DataSF footprints put the nearest neighbour at 13.79 m,
  // which agrees within 0.6 m. Do not raise past 12 without re-running the check.
  {
    id: '350Brannan',
    name: '350 Brannan Street',
    lon: -122.3935234,
    lat: 37.7810229,
    height: 13.85,
    exclude: 8,
    camera: { distance: 230, yaw: 80, pitch: 26 },
  },
  {
    // Through lot with party walls on both long sides, so the exclusion window
    // is narrow: this footprint's simplified ring centroid sits 0.96 m from the
    // anchor while the nearest NEIGHBOUR vertex is 11.17 m (SF3776007). Anything
    // from ~1 to ~11 m drops this building alone; 12 would take the neighbour.
    id: '550Third',
    name: '550 Third Street',
    lon: -122.3953409,
    lat: 37.7804407,
    height: 11,
    exclude: 8,
    camera: { distance: 190, yaw: 260, pitch: 34 },
  },
  // 574 Third (the 1907 apartment block at 566-586 Third), the largest footprint
  // in this family at 1,906 m2 — which is exactly why the tight 8-12 m radii used
  // on the small Brannan lots do not transfer. THREE footprints stand on this
  // plan: DataSF SF3776008 (97.9% of it, centroid 2.10 m) and two Overture
  // pieces that split the same mass (50.8% and 40.3% cover, nearest vertices
  // 6.84 m). Measured against the real bake input:
  //
  //   exclude  6 m    -> drops 1  (both Overture halves survive)
  //   exclude 8-16 m  -> drops 3  (correct: all three, zero collateral)
  //   exclude 18 m    -> drops 5  (eats 560 Third, SF3776007, vertex 16.35 m)
  //
  // 12 m is the middle of the safe band. Note the unusually wide window: it
  // exists because this building's own ring reaches ~30 m from the anchor while
  // its neighbours' nearest vertices are 16 m away, so the radius never has to
  // reach the ring to catch the footprint — the centroid test does it.
  {
    id: '574Third',
    name: '574 Third Street',
    lon: -122.3950551,
    lat: 37.7801937,
    height: 15.4,
    exclude: 12,
    camera: { distance: 260, yaw: 45, pitch: 28 },
  },
  // The corner block at Third and Brannan (also 590 Third). Sized by AREA
  // COVERAGE against the real bake input rather than by nearest-neighbour
  // distance, because on this block every neighbour shares a party-wall vertex
  // with this footprint and a vertex-distance reading says "collateral" for
  // buildings that are only touching. Two footprints actually stand on this
  // plan — DataSF SF3776114 (98.5% of it, centroid 8.70 m from this anchor) and
  // the Overture gap-fill 80ad8a83 (87.7%, centroid 4.72 m) — and both have to
  // go or the GLB shares its site with a procedural twin:
  //
  //   exclude  8 m    -> drops 1 (SF3776114 survives on its 8.70 m centroid)
  //   exclude 10-12 m -> drops 2  (correct: both, nothing else)
  //   exclude 14 m    -> drops 4  (starts eating 574 Third's footprints)
  //   exclude 16 m    -> drops 5  (eats 414 Brannan, SF3776011)
  //
  // 11 m is the middle of the safe band. The binding limit at the bottom is
  // SF3776114's CENTROID, not any vertex — this footprint is an L and its
  // centroid sits well off the anchor.
  {
    id: '400Brannan',
    name: '400 Brannan Street',
    lon: -122.3946805,
    lat: 37.7800981,
    height: 8.8,
    exclude: 11,
    camera: { distance: 170, yaw: 90, pitch: 26 },
  },
  {
    // Shell service station, across 3rd Street from 550 Third. The asset is a
    // forecourt, not a building, and the lot carries TWO baked footprints — the
    // canopy at the anchor and the kiosk 19.7 m away at the Brannan end. No
    // single radius takes both: reaching the kiosk needs r > 16.40 m, and 181
    // South Park's footprint behind the lot comes within 16.37 m. Hence the
    // second zone on the kiosk, which drops it by the centroid test with 2.9 m
    // of clearance to that neighbour. See docs/asset-plans/551-third.md 2.13.
    id: '551Third',
    name: '551 Third Street (Shell Station)',
    lon: -122.3946431,
    lat: 37.7806625,
    height: 6.6,
    exclude: 8,
    extraExclusions: [{ lon: -122.3944594, lat: 37.7805609, r: 4 }],
    // Camera offset is (sin yaw east, cos yaw south), so yaw 315 puts the eye
    // south-west of the site: the 3rd Street frontage, with the umbrellas
    // reading in front of the kiosk. No `key` — at 6.6 m this is texture in the
    // block, not a destination, and the number keys stay for skyline pieces.
    camera: { distance: 170, yaw: 315, pitch: 32 },
  },
  {
    // Ames Harris Neville Co. Building, 1926 — a whole block corner, so the
    // exclusion radius has to clear a 41 m footprint half-diagonal. 42 m is
    // deliberately tight: Alabama and Florida Streets are only ~20 m wide and a
    // generous radius would punch holes in the facing blocks. Verified against
    // the re-bake: procedural footprints dropped by exactly one.
    id: '375Alabama',
    name: '375 Alabama Street',
    lon: -122.4118477,
    lat: 37.7645633,
    height: 22.5,
    exclude: 42,
    camera: { distance: 330, yaw: 215, pitch: 18 },
  },
  {
    id: 'letterman',
    name: 'Letterman Digital Arts Center',
    lon: -122.4494466,
    lat: 37.7997327,
    height: 22,
    // The asset is the whole campus — four buildings AND the Halprin grounds
    // (312 x 298 m). The radius must clear all four baked footprints plus the
    // lagoon, measured from the anchor to the far corner of the modelled base.
    exclude: 185,
    // The grounds are hand-modelled; baked tree scatter fights the meadow,
    // the lagoon and the groves (Palace of Fine Arts precedent).
    clearTrees: true,
    camera: { distance: 700, yaw: 220, pitch: 24 },
  },
  {
    // Mission Bay's arena. The exclusion radius is unusually tight for a 155 m
    // footprint, and deliberately so: `excluded()` drops a footprint when ANY
    // of its vertices is in the zone, and here Che Fico Pizzeria's nearest
    // vertex is 80.4 m out with Uber HQ Buildings 4 and 3 at 84.4 and 85.7 m.
    // The only footprints that reach under the skin are the arena itself and a
    // 16 m outbuilding whose nearest vertex is 74.7 m out, so (74.7, 80.4) is
    // the entire usable window. Anything near the 115 m the plan suggested
    // would delete two real office towers and a restaurant from the baked city.
    //
    // Today the zone drops nothing: DataSF's footprints predate the 2019 arena
    // and have no vertex within 108.8 m of this anchor, and Overture's gap-fill
    // adds none. It is insurance for the next data refresh.
    id: 'chaseCenter',
    name: 'Chase Center',
    lon: -122.3873962,
    lat: 37.7678739,
    height: 40.8,
    exclude: 78,
    camera: { distance: 850, yaw: 250, pitch: 20 },
  },
  // ---------------------------------------------------------------------
  // Presidio Boulevard row, Bldgs. 540-543. Four of the twelve near-identical
  // WWI-era officers' family quarters (540-551) that step down the hill from
  // Lombard Gate, integrated together so the row reads as a row. Every radius
  // below was sized against the metric `excluded()` actually uses — centroid OR
  // any ring vertex inside the circle — and every one is small enough to drop
  // only its own baked footprint. That is what keeps the four consistent: the
  // circles do not reach each other, so each house is replaced independently
  // and 544 onward stay baked. Do NOT widen any of them to the 70-120 m typical
  // of the standalone landmarks; on a row spaced ~25 m apart that punches a
  // hole where neighbours have no GLB to replace them.
  // ---------------------------------------------------------------------
  {
    id: '540PresidioBlvd',
    name: '540 Presidio Boulevard',
    lon: -122.4519224,
    lat: 37.7966667,
    height: 11.5,
    // The house's own footprint reaches 12.2 m from the anchor (14.47 x 19.72 m
    // OBB, half-diagonal), so the radius has to clear that. 541's nearest vertex
    // is 19.1 m away — measured out of the shipped tile
    // app/public/tiles/buildings/13_10.bin, where this house is building 33 and
    // 541 is building 39. 15 m sits in the middle of that 12.2-19.1 m window.
    exclude: 15,
    // camera.js places the eye at target + distance*(sin yaw, ., cos yaw) with
    // +x east and +z south, so yaw 52 stands east-south-east of the house —
    // the three-quarter that shows the porch front and the south hip together,
    // matching the asset's beauty render.
    camera: { distance: 120, yaw: 52, pitch: 20 },
  },
  {
    // Sized on OSM rings measured against this anchor: 541's own centroid is
    // 0.36 m out and its nearest vertex 6.15 m, while the nearest NEIGHBOUR
    // vertices are 18.86 m (540) and 20.43 m (542). The safe window is
    // (0.36, 18.86) m; 12 m leaves 6.9 m of headroom before 540 is at risk —
    // margin that matters because the baked ring comes from DataSF/Overture,
    // not OSM, and may differ by a metre or two.
    id: '541Presidio',
    name: '541 Presidio Boulevard',
    lon: -122.4518601,
    lat: 37.7969312,
    height: 10,
    exclude: 12,
    // Deliberately NO clearTrees, unlike Letterman: this asset has no
    // hand-modelled grounds, and the baked cypress/eucalyptus scatter around it
    // IS the East Housing character. The Presidio PARK_COVER entry should keep
    // running right up to the house.
    camera: { distance: 170, yaw: 300, pitch: 22 },
  },
  {
    // Mid-row, with the narrowest window of the four: measured from the anchor,
    // 542's own footprint reaches 11.3 m, while the nearest neighbour vertex
    // (543, way/288361199) is 18.1 m and 541 is 20.2 m. 14 leaves ~2.7 m over
    // its own ring and ~4.1 m of clearance to 543.
    id: '542PresidioBlvd',
    name: '542 Presidio Boulevard',
    lon: -122.4516862,
    lat: 37.7971579,
    height: 10.6,
    exclude: 14,
    // `camera` is NOT optional, even for a building too small to deserve a
    // fly-to preset: context.mjs bakes `camera: l.camera` straight into
    // context/landmarks.json, and camera.js reads `preset.yaw` unconditionally,
    // so omitting it ships a landmark whose preset is undefined and the whole
    // city fails to boot with "Cannot read properties of undefined (reading
    // 'yaw')". Verified by doing exactly that first.
    // yaw 30 puts the camera to the SSE, looking at the ESE entrance front and
    // the SSW hip end; 200 m suits a 10.6 m house (cf. 380Brannan at 220).
    camera: { distance: 200, yaw: 30, pitch: 26 },
  },
  {
    // This house's own footprint reaches 10.1 m from the anchor, and the nearest
    // neighbouring DataSF footprint (201006.0016579, the larger duplex type)
    // reaches 15.9 m. The window is 10.1 < r < 15.9 and 12 m sits in the middle
    // of it. Anything past ~15.5 m deletes the neighbour.
    id: '543PresidioBlvd',
    name: '543 Presidio Blvd',
    lon: -122.4515766,
    lat: 37.7973711,
    height: 9.55,
    exclude: 12,
    camera: { distance: 120, yaw: 130, pitch: 28 },
  },
  {
    id: 'civicCenterCourthouse',
    name: 'Civic Center Courthouse',
    lon: -122.4192537,
    lat: 37.7804897,
    height: 29.6,
    // Footprint 83.5 x 37 m at 81.22 deg; half-diagonal 45.6 m, so 52 m clears
    // it with a small margin. City Hall's 110 m zone (132 m away) already
    // overlaps part of this block - that is pre-existing and harmless.
    exclude: 52,
    camera: { distance: 420, yaw: 135, pitch: 20 },
  },
  {
    id: 'billGrahamCivicAuditorium',
    name: 'Bill Graham Civic Auditorium',
    lon: -122.4173309,
    lat: 37.7780621,
    height: 37,
    // Footprint 128 x 78.6 m at 80.69 deg; half-diagonal 75.1 m, so 80 m clears
    // it. Checked against the neighbours: City Hall is 228 m away (110 m zone)
    // and the Opera House 322 m (62 m zone) - neither zone is touched.
    exclude: 80,
    camera: { distance: 700, yaw: 200, pitch: 24 },
  },
  {
    // Governor Edmund G. "Pat" Brown Building — California PUC headquarters.
    // The radius looks absurdly small for a 113 x 93 m building, and it has to
    // be: excluded() drops a whole footprint when its centroid OR ANY ring
    // vertex is inside the radius, and this block has a close neighbour.
    // Measured against the committed tile (buildings/18_13.bin):
    //   this footprint  (6,339 m2, matches the 6,263 m2 survey) nearest vertex 12.7 m
    //   SW neighbour    (1,296 m2, a separate building)          nearest vertex 14.4 m
    //   City Hall                                                nearest vertex 58.2 m
    // So 12.7 < r < 14.4 is the ONLY window that clears this building and
    // spares the neighbour; a centroid-only reading (12.0 m vs 36.3 m) would
    // suggest a comfortable 30 m and silently delete a real building. One
    // vertex inside is enough to remove all 6,339 m2, so 13.5 does the full job.
    id: '505VanNess',
    name: '505 Van Ness Avenue',
    lon: -122.4212915,
    lat: 37.7804835,
    height: 27,
    exclude: 13.5,
    camera: { distance: 420, yaw: 126, pitch: 26 },
  },
  {
    // Civic Center corner block on Grove at Polk, 63 x 37 m, facing City Hall.
    // `excluded()` drops a footprint when its centroid OR any of its vertices
    // lands in the zone, and here it is the CENTROID test that does the work:
    // this block's centroid sits on the anchor while its own corners are
    // 28.5-34.2 m out. The vertex window is closed from the other side —
    // DataSF's nearest foreign vertex is 29.45 m away (OSM agrees: 30.1 m,
    // way/940206561 "The Civic" across Polk and way/35176282 immediately
    // south, then 31.5 and 31.9 m) — so a radius wide enough to also catch
    // this building's own corners would start taking neighbours.
    // 24 m verified against the re-bake: cell 19_14 goes 80 -> 79 buildings,
    // zero footprints left with a vertex inside the zone, nearest surviving
    // vertex 29.45 m. Exactly one building dropped, and it is this one.
    id: '101Grove',
    name: '101 Grove Street (Public Health Building)',
    lon: -122.4186747,
    lat: 37.7781359,
    height: 21.4,
    exclude: 24,
    camera: { distance: 300, yaw: 35, pitch: 22 },
  },
  {
    // The Kelsey Civic Center, 2025 (WRNS Studio + Santos Prescott). An
    // eight-storey L that wraps the 171 Grove corner lot rather than holding
    // the corner itself.
    //
    // 14 m sits in the 12-17 m band that drops exactly the three DataSF
    // footprints on and beside the site and nothing else. Measured against
    // pipeline/data/buildings_datasf.geojson with the real rule (centroid OR
    // any ring vertex inside the radius), nearest vertex to this anchor:
    //   SF0811019  6.14 m  demolished 2023 for this building
    //   SF0811020  6.14 m  171 Grove, STILL STANDING - unavoidable collateral
    //   SF0811018 11.67 m  demolished 2023 for this building
    //   SF0811001 17.49 m  101 Grove, already excluded by its own entry above
    //   next      30.11 m  200-214 Van Ness
    // The two demolished footprints and the standing corner building share a
    // party-wall vertex at exactly the same 6.14 m, so NO radius removes the
    // stale pair without also removing 171 Grove. Shipping the drop is the
    // lesser error: the alternative is leaving two demolished buildings
    // standing inside a 2025 landmark. See docs/asset-plans/234-van-ness.md
    // 2.12. A follow-up 171 Grove asset would close the gap.
    id: '234VanNess',
    name: 'The Kelsey Civic Center (234 Van Ness Avenue)',
    lon: -122.4193071,
    lat: 37.7780541,
    height: 30.12,
    exclude: 14,
    camera: { distance: 320, yaw: 225, pitch: 30 },
  },
  {
    // Letterman Hospital ward, 1930s, now part of the Thoreau Center. DataSF
    // stores the WHOLE campus — twelve surviving buildings — as ONE 159x147 m
    // comb-shaped footprint, so there is no radius that clears 1008 alone: its
    // nearest vertex is 4.70 m from the anchor while the ring's centroid is
    // 41.2 m away. Dropping that one footprint therefore removes the whole
    // campus, which is the deliberate, approved trade (David, 12 Aug 2026) —
    // the alternative was leaving this asset buried inside a 16.5 m procedural
    // mass. The next separate footprint is 51.52 m out, so anything from ~5 to
    // ~51 m does the same job. 34 m is chosen because `exclude` is reused as the
    // radius for BOTH the tree-clear circle below and the runtime street-furniture
    // exclusion, and the model's own half-diagonal is 32.8 m (55.13 x 35.47) — a
    // radius under that leaves trees and lamps standing inside the building. 34 m
    // covers the shell with margin and is still 17 m clear of the neighbours.
    //
    // Note this sits inside `letterman`'s 185 m zone, which is fine: exclusion
    // circles union, and that asset's grounds stop short of this ward.
    id: '1008GeneralKennedy',
    name: '1008 General Kennedy Avenue',
    lon: -122.4514809,
    lat: 37.8007878,
    height: 11.9,
    exclude: 34,
    // Parkland site: without this the Presidio canopy scatters straight through
    // the ward, because dropping the campus footprint also removed its tree veto.
    clearTrees: true,
    camera: { distance: 200, yaw: 150, pitch: 28 },
  },
  {
    // Civic Center is the tightest site in the registry, so this radius is
    // measured, not guessed. excluded() drops a footprint when ANY vertex
    // falls inside, and around this anchor the vertex distances are:
    //   18.3 m  the museum's own footprint (Overture; 18.9 m DataSF)
    //   42.7 m  a 4 m utility structure at the block's north-east corner,
    //           outside this asset's outline and worth keeping
    //   50.2 m  the Abigail Hotel — the nearest real neighbour
    // 40 m therefore drops the museum in both sources with a 22 m margin,
    // and clears the utility structure by 2.7 m and every real building by
    // 10 m. Anything near the 70 m half-diagonal the plan first suggested
    // would have deleted the new Main Library and UC Law across the street.
    //
    // Note the baked city currently renders this building 46 m tall, because
    // Overture carries the same height=46 tag that is really the NAVD88 roof
    // elevation. Excluding it fixes that too.
    id: 'asianArtMuseum',
    name: 'Asian Art Museum',
    lon: -122.4159859,
    lat: 37.7802817,
    height: 28.1,
    exclude: 40,
    camera: { distance: 600, yaw: 268, pitch: 20 },
  },
  {
    // The tightest exclusion window in this file, and the failure mode is
    // silent. `excluded()` drops a footprint when its ring centroid OR any
    // vertex lands inside the radius, and measured against the rings the bake
    // actually sees (DataSF, after simplifyRing(0.6)) from this anchor:
    // this building's own ring triggers at 0.57 m, 165-167 South Park
    // (SF3775028) at 3.83 m, 181 (SF3775172) at 3.92 m, 159 (SF3775029) at
    // 11.02 m. So the window is (0.6, 3.8) m and 2 sits in the middle of it.
    // Anything from 4 m up deletes two party-wall historic contributors from
    // the baked city and nothing crashes to tell you.
    //
    // This is also why the anchor is the footprint's AREA CENTROID rather than
    // its OBB centre: at the OBB centre the nearest neighbour vertex is 2.74 m
    // and the window nearly closes.
    id: '171SouthPark',
    name: '171 South Park Street',
    lon: -122.3945219,
    lat: 37.7809,
    height: 12.6,
    exclude: 2,
    // Camera bearing = 180 - yaw (camera.js apply(): offset is
    // (sin yaw, ., cos yaw) and +z is south), so yaw 197 stands the camera at
    // 343 deg = NNW, square onto the three-facet park front. Cross-checked
    // against 380Brannan, whose SE-facing front carries yaw 45 = bearing 135.
    camera: { distance: 200, yaw: 197, pitch: 26 },
  },
  // Kleiner Perkins' office on the South Park oval. The exclusion window here is
  // the tightest in this file, because 117 South Park is ATTACHED: the two
  // footprints share their party-wall vertices, and `excluded()` drops a
  // footprint when any RING VERTEX — not just its centroid — falls inside the
  // radius. Measured from this anchor against the DataSF footprints:
  //
  //   own ring area centroid            0.26 m  (OSM cross-check 1.54 m)
  //   shared party-wall vertex, no. 117 6.40 m  <- the ceiling
  //   no. 117's own centroid           10.59 m
  //   next neighbour vertex (no. 123)  13.17 m
  //
  // So the safe band is 1.6-6.4 m and the exclusion has to work through the
  // centroid test — this building's own vertices sit at 6.40 m, outside any
  // radius that spares the neighbour. 4 m is the middle of that band. Do NOT
  // raise it: at 6.5 m this deletes a real building that has no hand-built
  // replacement. Same situation as 550Third's through-lot note above.
  {
    id: '101SouthPark',
    name: 'Kleiner Perkins (101 South Park)',
    lon: -122.3937582,
    lat: 37.7812624,
    height: 10.9,
    exclude: 4,
    camera: { distance: 200, yaw: 318, pitch: 26 },
  },
  {
    // Party-wall row on the South Park oval, so this is the tightest exclusion
    // zone in the registry. Measured against the committed tile 23_13 rather
    // than guessed, because `excluded()` drops a footprint whose centroid OR any
    // ring vertex is inside the radius, and on a row the neighbours' vertices
    // are what bind:
    //
    //   this footprint (#94)   centroid  0.48 m   -> dropped by anything > 0.5
    //   159 South Park (#164)  vertex    5.42 m   -> the binding constraint
    //   147 South Park (#80)   vertex   12.30 m
    //
    // Safe band 0.5-5.4 m; 3 m is the middle of it. The plan's suggested 6 m
    // would have taken 159 South Park out with it and punched a hole in the row.
    // Do not raise this without re-decoding the tile.
    id: '155SouthPark',
    name: '155 South Park',
    lon: -122.3942202,
    lat: 37.7808993,
    height: 10.1,
    exclude: 3,
    camera: { distance: 170, yaw: 147, pitch: 26 },
  },
  {
    // The tightest exclusion window in this registry, so the radius is derived
    // rather than guessed. `excluded()` in pipeline/buildings.mjs drops a
    // footprint when its centroid OR any ring vertex falls inside the circle,
    // and the bake reads DataSF first then gap-fills from Overture (which
    // carries OSM geometry), so both sources bind. Measured from this anchor:
    //
    //                                  nearest vertex   centroid
    //   own footprint (OSM)                  1.03 m       3.04 m
    //   own footprint (DataSF SF3775033)     4.68 m       3.29 m
    //   nearest neighbour (OSM way/1311547493, the rear building)
    //                                        6.18 m      12.96 m
    //   nearest neighbour (DataSF SF3775036)
    //                                       10.32 m      15.37 m
    //
    // So the safe window is 4.68 < r < 6.18 if the rear building arrives via
    // Overture, and 3.29 < r < 10.32 if it arrives via DataSF. 5 satisfies
    // both, with 0.3 m of headroom over our own DataSF ring and 1.2 m below the
    // nearest neighbour. Do NOT raise it: at 7 the rear building vanishes and
    // leaves a hole no GLB fills, and at 11 so does 123 South Park — which
    // shares this building's north-east party wall at a 0.0 m gap.
    id: '135SouthPark',
    name: '135 South Park',
    lon: -122.3940203,
    lat: 37.781103,
    height: 8.5,
    exclude: 5,
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with +x
    // east and +z south, so yaw 225 stands north-west of the building — square
    // onto the South Park front, which is also the side the roof monitor reads
    // from. 150 m suits an 8.5 m building (cf. 543 Presidio at 120 for 9.55 m).
    camera: { distance: 150, yaw: 225, pitch: 26 },
  },
  {
    // The tightest site in the registry: a 6.2 m frontage in an unbroken
    // party-wall row on the south rim of South Park. Two things are unusual and
    // both are deliberate.
    //
    // 1. THE lon/lat BELOW IS NOT THE MANIFEST ANCHOR, and must not be
    //    "corrected" to match it. These fields are independent: placeGeneric()
    //    in app/src/assets.js positions the GLB from the manifest anchor alone
    //    (-122.3943764, 37.7808599 — the surveyed parcel's centroid, where the
    //    building actually stands), while this lon/lat is only the centre of
    //    the exclusion circle. They sit 1.4 m apart because from the manifest
    //    anchor NO radius works at all: 159 South Park's footprint shares a
    //    party-wall vertex 0.50 m away, exactly as close as this building's own
    //    nearest vertex, so every circle that drops one drops both. Centring
    //    the circle on the DataSF LiDAR footprint's area centroid instead opens
    //    the only viable window.
    //
    // 2. THE WINDOW IS 0.4 m WIDE. excluded() drops a footprint when its
    //    centroid OR any vertex is inside the radius. Measured from this point
    //    against the two sources the bake actually reads
    //    (pipeline/data/buildings_datasf.geojson and
    //    overture_buildings.geojsonseq, 13 Aug 2026):
    //
    //          polygon              DataSF    Overture
    //          165-167 (this)         0.00 m    1.08 m
    //          159 South Park         1.49 m    2.33 m
    //          171 South Park         3.34 m    4.15 m
    //
    //    So r must EXCEED 1.08 (or the Overture gap-fill re-adds this building
    //    after the DataSF footprint is dropped — addBuilding() returns null on
    //    exclusion, so markOccupied() never runs and occupiedFraction() cannot
    //    be relied on to block it) and stay UNDER 1.49 (or 159 disappears and
    //    leaves a hole where a real building stands, an AGENTS rule 5
    //    violation). 1.3 keeps 0.22 m and 0.19 m of margin. Do not round it.
    //
    // No clearTrees: the crape myrtle on the sidewalk in front is real and
    // should stay, and at 1.3 m this radius clears no street furniture anyway —
    // which is correct here, since South Park's furniture sits along the street
    // well outside a 6 m lot.
    id: '165SouthPark',
    name: '165-167 South Park',
    lon: -122.3943963,
    lat: 37.7808764,
    height: 9.0,
    exclude: 1.3,
    camera: { distance: 160, yaw: 350, pitch: 26 },
  },
  {
    // A 43.2 x 13.8 m slab running the full depth of the block, from the South
    // Park oval back to the Varney Place alley, sharing a party wall with 171
    // South Park. That party wall makes the exclusion radius unusually
    // constrained on BOTH sides, so this number is measured, not guessed.
    // excluded() drops a footprint when its centroid OR any ring vertex falls
    // inside the radius. Measured against the Overture footprints the bake
    // actually consumes (not OSM — the two differ here and it matters):
    //    4.05 m  this building's own footprint, via its centroid — the trigger
    //            that removes the procedural slab
    //    7.00 m  171 South Park, via a ring vertex that is a node SHARED with
    //            this building's own outline
    //    9.17 m  the Shell canopy at 551 Third Street
    //   12.32 m  167 South Park
    // So the whole safe window is (4.06, 7.00) — 2.9 m wide, one of the
    // tightest in this registry. 5 sits in it with 0.95 m of margin below and
    // 2.00 m above. Below 4.06 the procedural slab survives and pokes through
    // the model; at 7.00 the re-bake punches a hole where 171 should be.
    // Verified on the re-bake: exactly one footprint dropped, 23 kept within
    // 60 m. Do not widen this without re-running that check.
    id: '181SouthPark',
    name: '181 South Park',
    lon: -122.3945113,
    lat: 37.7807582,
    height: 16.5,
    exclude: 5,
    camera: { distance: 190, yaw: 255, pitch: 24 },
  },
  {
    // The new Main Library, one block south of the Old Main across Fulton, on a
    // near-identical 106 x 57 m block. Same radius rule as its neighbour and for
    // the same reason: excluded() drops a footprint when its centroid OR ANY ring
    // vertex falls inside, so the circle has to clear this building's NEAREST
    // vertex while staying inside the nearest neighbour's. Measured from this
    // anchor against the actual bake input:
    //   28.9 m  this footprint's nearest vertex (Overture; 30.7 m in DataSF)
    //   30.3 m  a 1.2 m site structure inside the block (DataSF only) - fine to drop
    //   50.6 m  the nearest REAL neighbour, the 9 m and 15.9 m buildings across
    //           Hyde towards Market, agreed by both sources
    //   60.3 m  the OBB half-diagonal - too large, it would eat that frontage
    // 40 m drops the library in both sources with a 9.3 m margin and clears every
    // real neighbour by 10.6 m. The Asian Art Museum's own 40 m circle sits 92 m
    // away, so the two do not overlap.
    //
    // Overture carries height=46 for this footprint - the NAVD88 roof elevation,
    // the same tag error as the museum - so the baked city renders it 46 m tall
    // and it reads as a Civic Center mid-rise. Excluding it fixes that too.
    id: 'sfMainLibrary',
    name: 'San Francisco Main Public Library',
    lon: -122.4157709,
    lat: 37.7791281,
    height: 28.98,
    exclude: 40,
    camera: { distance: 600, yaw: 268, pitch: 20 },
  },
  {
    // 1927 concrete loft filling the quarter block at 3rd and Bryant. Unusually
    // forgiving exclusion window, measured against the bake input (DataSF
    // footprints, projected + simplified at the 0.6 m tolerance): this
    // footprint's ring centroid sits 0.93 m from the anchor and the nearest
    // NEIGHBOUR vertex is 35.59 m (SF3776100), so anything from ~1 to ~35 m
    // drops this building alone. 20 m sits in the middle of that window.
    // targetHeight is the rooftop bulkhead (LiDAR max 26.62 m), not the 23 m
    // parapet that OSM and the LiDAR median both describe.
    id: '500Third',
    name: '500 Third Street',
    lon: -122.3958224,
    lat: 37.7808279,
    height: 26.5,
    exclude: 20,
    camera: { distance: 240, yaw: 25, pitch: 26 },
  },
  {
    // 599 Third Street — 4-storey live/work lofts on the north corner of 3rd
    // and Brannan, completing that corner alongside 550 Third and 380 Brannan.
    //
    // exclude: 10 is MEASURED against the bake's own input (DataSF footprints
    // streamed through geojsonStream + ringCentroid), not derived from the OSM
    // polygon. The asset plan's estimate of 22 came from this building's OSM
    // corner vertices and is wrong: the DataSF ring is a 16-vertex outline
    // whose centroid sits 2.08 m from the anchor and whose nearest vertex is
    // 15.56 m, while the nearest NEIGHBOUR vertex is only 17.24 m away. Since
    // excluded() drops a ring on centroid OR any-vertex, the window that drops
    // exactly this building is 2.08 < r <= 17.24; 22 would have taken three
    // neighbours with it. 10 sits in the middle of the real band.
    id: '599Third',
    name: '599 Third Street',
    lon: -122.3942739,
    lat: 37.7804504,
    height: 18.3,
    exclude: 10,
    // `camera` is mandatory even though this building gets no number `key` —
    // see the note on 542PresidioBlvd. main.js maps EVERY manifest landmark
    // into `presets`, and camera.js reads `preset.yaw` unconditionally, so
    // omitting it boots to "Cannot read properties of undefined (reading
    // 'yaw')". Verified by doing exactly that here too.
    // yaw 0 stands the camera due south (app yaw = 180 − true bearing), which
    // is the bisector of the 3rd Street front (normal 224.8°) and the Brannan
    // front (135.2°) — the one angle where both designed elevations and the
    // corner between them read at once. 240 m suits an 18.3 m block (cf.
    // 380Brannan 220 at 12.6 m, 550Third 190 at 11 m).
    camera: { distance: 240, yaw: 0, pitch: 26 },
  },
  {
    // 590 Third Street — the two-storey 1905-ish commercial corner block on the
    // WEST corner of 3rd and Brannan, directly across 3rd from 599Third. Between
    // them the intersection reads "shops below, homes above".
    //
    // exclude: 7 is MEASURED against the bake's own input (DataSF ynuv-fyni
    // footprints reprojected with the app's tangent projection), not derived
    // from OSM. Around this anchor:
    //   this building's ring centroid          0.88 m
    //   this building's nearest vertex        11.24 m
    //   nearest NEIGHBOUR vertex (SF3776008)  13.82 m  <- must survive
    //   second neighbour vertex (SF3776011)   15.08 m
    // excluded() drops a ring on centroid OR any vertex, so the window that
    // drops exactly this building is 0.88 < r <= 13.82. The upper end is thin
    // because SF3776008 is the 1,906 m² brick warehouse sharing this building's
    // NW party wall — and it is TALLER than the asset (LiDAR median 11.05 m vs
    // 9.5 m), so swallowing it would leave a very visible hole. 7 sits clear of
    // both ends and in line with the neighbours already integrated (550Third 8,
    // 551Third 8, 380Brannan 9, 599Third 10).
    id: '590Third',
    name: '590 Third Street',
    lon: -122.3946749,
    lat: 37.7800837,
    height: 9.5,
    exclude: 7,
    // `camera` is mandatory even without a number `key` — main.js maps EVERY
    // manifest landmark into `presets` and camera.js reads `preset.yaw`
    // unconditionally, so omitting it boots to "Cannot read properties of
    // undefined (reading 'yaw')". See the note on 599Third.
    // yaw 90 stands the camera due east (app yaw = 180 − true bearing), the
    // bisector of the 3rd Street front (normal 45.2°) and the Brannan front
    // (135.1°) — the one angle where both designed elevations and the raised
    // corner parapet over them read at once. 180 m suits a 9.5 m block
    // (cf. 550Third 190 at 11 m, 380Brannan 220 at 12.6 m).
    camera: { distance: 180, yaw: 90, pitch: 30 },
  },
  {
    // 592 Third Street — the 1905 two-storey loft on the WEST corner of 3rd and
    // Brannan, directly across 3rd from 599Third. Kinoko Real Estate, Cafe
    // Buenos Aires and four Brannan-side tenants under one black shopfront band.
    //
    // The exclusion here is doing more than tidying: Overture gives this
    // footprint a top of 16.7 m over a base of 6.5 m, so the baked procedural
    // block is 10.2 m tall against the asset's 8.2 m. Without the exclusion the
    // GLB is not merely intersected, it is entirely INSIDE a taller block and
    // invisible. Anyone judging this landmark on an unbaked tree sees nothing
    // wrong with a building that is not there.
    //
    // exclude: 6 is MEASURED two ways, both against rings excluded() actually
    // consumes. Against the committed bake (app/public/tiles/buildings/23_13.bin):
    // this footprint's ring centroid is 1.64 m from the anchor and the nearest
    // NEIGHBOUR vertex is 12.87 m (SF3776008, the 11 m building on the NW party
    // wall). Against the raw DataSF LiDAR polygons: 0.90 m and 12.20 m. Since
    // excluded() drops a ring on centroid OR any vertex, the window that drops
    // exactly this building is 1.7 < r < 12.2; 6 sits in the middle with better
    // than 5 m of margin at both ends. Note this building's OWN nearest vertex
    // is 10.2 m out, so the exclusion fires on the centroid test, not the vertex
    // test — do not shrink r below 2 thinking the vertices will catch it.
    //
    // targetHeight is the parapet crest, LiDAR-derived rather than published:
    // the roof-deck mode is 7.82 m and the parapet adds ~0.38 m. The LiDAR
    // hgt_max of 11.65 m on this footprint is NOT the crest — it is the two
    // street trees overhanging the 3rd Street parapet, a 6-sigma outlier on a
    // roof whose height std is 0.64 m. See docs/asset-plans/592-third.md 2.15.
    id: '592Third',
    name: '592 Third Street',
    lon: -122.3946805,
    lat: 37.780091,
    height: 8.2,
    exclude: 6,
    // `camera` is mandatory even without a number `key` — main.js maps every
    // manifest landmark into `presets` and camera.js reads `preset.yaw`
    // unconditionally (see the note on 542PresidioBlvd and 599Third).
    // App yaw = 180 − true bearing. The bisector of the 3rd Street front
    // (normal 45.1°) and the Brannan front (135.2°) is 90.2°, so the camera
    // wants app yaw 180 − 90.2 = 90: due east of the building, the one angle
    // where both designed elevations and the corner between them read at once
    // (the same construction 599Third used to arrive at its yaw 0).
    // Verified in the local QA, not derived on paper: yaw 315 was tried first
    // and puts the camera to the SOUTH-WEST, staring at the two blank party
    // walls. On a corner building the yaw is worth rendering before believing.
    // 200 m suits an 8.2 m building (cf. 370Brannan 150 at 7.63 m, 550Third
    // 190 at 11 m).
    camera: { distance: 200, yaw: 90, pitch: 26 },
  },
  {
    // A 5-acre PLAZA, not a building, and the exclusion has to do two different
    // jobs at two different radii — which is why this is the first entry to
    // carry `clearTreesRadius`.
    //
    // `exclude: 95` is the buildings job. Three single-storey structures stand
    // inside the plaza (the garage kiosk, the Grove-corner cafe and the Pit
    // Stop) and the procedural builder extrudes all three to 22-23 m, so
    // without the exclusion three phantom towers stand on the plaza. Measured
    // against the committed bake input (buildings/19_13.bin, 19_14.bin),
    // nearest VERTEX not centroid, per the method 505VanNess established:
    //   garage kiosk       67.8 m   (88 m2, baked top 23.4 m)
    //   Grove-corner cafe  74.2 m   (93 m2, baked top 22.0 m)
    //   Pit Stop           83.5 m   (10 m2, baked top 22.5 m)
    //   first neighbour   109.9 m   (6,165 m2, baked top 62.0 m)  <- must survive
    // The window is 83.5 < r < 109.9 and 95 sits in the middle of it.
    //
    // `clearTreesRadius: 110` is the trees job, and it has to be BIGGER — it
    // covers the plaza's 107.6 m half-diagonal. The plaza is leisure=park, so
    // the landcover scatter drops procedural trees across it that stand among
    // the 190 hand-placed pollards looking like a different world.
    //
    // This was first set to 60 m on the theory that a wider circle would eat
    // real street trees on Larkin, McAllister and Grove. That theory was never
    // measured and it was wrong. Counted against the baked landcover:
    //   radius   left INSIDE the plaza   cut OUTSIDE the plaza
    //     60 m        109                       0
    //     80 m         34                       7
    //     95 m          6                      10
    //    110 m          0                      14
    // The blocks around the plaza are civic buildings with almost no mapped
    // street trees, so covering the whole plaza costs 14 of them and removes
    // 109 lollipops from a hero landmark. Measure the tree radius against the
    // bake the same way the building radius is measured; do not reason about it.
    id: 'civicCenterPlaza',
    name: 'Civic Center Plaza',
    lon: -122.4176184,
    lat: 37.7794818,
    height: 30.48,
    exclude: 95,
    clearTrees: true,
    clearTreesRadius: 110,
    // Looks WEST along the central court so the fly-to lands on the plaza's own
    // axis with City Hall filling the far end — the one composition that
    // explains what this place is.
    camera: { distance: 620, yaw: 90, pitch: 30 },
  },
  // A PARTY-WALL site, so this radius is far tighter than the usual
  // half-diagonal rule. The Earl Warren Building shares its block with the
  // 54 m Hiram W. Johnson State Office Building, whose wall is a few metres
  // off this building's north wings. Measured against the real bake input
  // (`pipeline/data/overture_buildings.geojsonseq`) with the metric
  // `excluded()` uses — centroid OR any ring vertex inside the radius — over
  // the 13 footprints in the surrounding bbox:
  //
  //   exclude  6-20 m -> drops 1  (correct: the Earl Warren footprint, whose
  //                                nearest point is 5.1 m from this anchor)
  //   exclude 22-40 m -> drops 2  (eats the Hiram W. Johnson slab at 20.2 m)
  //   exclude 60 m    -> drops 3  (also the Civic Center Plaza Garage kiosk)
  //
  // 12 m is the middle of the safe band. The 59.9 m OBB half-diagonal that
  // most entries here use would have punched a 54 m building out of the block.
  {
    id: 'earlWarrenBuilding',
    name: 'Earl Warren Building',
    lon: -122.4178413,
    lat: 37.7806865,
    height: 27.0,
    exclude: 12,
    camera: { distance: 420, yaw: 183, pitch: 20 },
  },
];

// Parks/green spaces the landcover bake must match at least one source polygon
// for; validate.mjs fails if any of these come up empty.
// Every circle the bake clears, one row per zone. A landmark contributes its
// own `exclude` circle plus any `extraExclusions`; `id`/`name` stay attached so
// audit 1.6 can name the landmark responsible for an intrusion.
export function exclusionZones() {
  const zones = [];
  for (const l of LANDMARKS) {
    if (l.exclude) zones.push({ id: l.id, name: l.name, lon: l.lon, lat: l.lat, r: l.exclude });
    for (const e of l.extraExclusions ?? []) {
      zones.push({ id: l.id, name: l.name, lon: e.lon, lat: e.lat, r: e.r });
    }
  }
  return zones;
}

export const NAMED_PARKS = [
  { id: 'goldenGatePark', name: 'Golden Gate Park', lon: -122.4862, lat: 37.7694 },
  { id: 'presidio', name: 'Presidio', lon: -122.4662, lat: 37.7989 },
  { id: 'mclarenPark', name: 'John McLaren Park', lon: -122.4183, lat: 37.7199 },
  { id: 'lakeMerced', name: 'Lake Merced', lon: -122.4933, lat: 37.7261 },
  { id: 'glenCanyon', name: 'Glen Canyon Park', lon: -122.4438, lat: 37.7405 },
  { id: 'buenaVista', name: 'Buena Vista Park', lon: -122.4408, lat: 37.7686 },
  { id: 'alamoSquare', name: 'Alamo Square', lon: -122.4348, lat: 37.7764 },
  { id: 'doloresPark', name: 'Mission Dolores Park', lon: -122.4271, lat: 37.7596 },
  { id: 'marinaGreen', name: 'Marina Green', lon: -122.4405, lat: 37.8066 },
  { id: 'crissyField', name: 'Crissy Field', lon: -122.464, lat: 37.8045 },
  { id: 'lincolnPark', name: 'Lincoln Park', lon: -122.4996, lat: 37.7825 },
];

export const PARK_COVER = {
  presidio: {
    base: 'trees',
    treeArea: 180,
    mode: 'grid',
    species: { broadleaf: 0.1, cypress: 0.45, eucalyptus: 0.45 },
  },
};

// Extra hero/overview camera presets.
export const VIEW_PRESETS = [
  {
    id: 'hero',
    name: 'Hero view (whole city)',
    lon: -122.4315,
    lat: 37.7739,
    camera: { distance: 9000, yaw: 225, pitch: 30 },
    key: '0',
  },
  {
    id: 'twinPeaks',
    name: 'Twin Peaks',
    lon: -122.4477,
    lat: 37.7544,
    camera: { distance: 1300, yaw: 60, pitch: 18 },
  },
  {
    id: 'marketStreet',
    name: 'Market Street',
    lon: -122.4079,
    lat: 37.7864,
    camera: { distance: 320, yaw: 232, pitch: 11 },
  },
  {
    id: 'lombard',
    name: 'Lombard switchbacks',
    lon: -122.4187,
    lat: 37.8021,
    camera: { distance: 300, yaw: 90, pitch: 14 },
  },
  {
    id: 'sunset',
    name: 'Sunset grid',
    lon: -122.4907,
    lat: 37.7532,
    camera: { distance: 700, yaw: 75, pitch: 12 },
  },
  {
    id: 'presidio',
    name: 'Presidio Main Post',
    lon: -122.468,
    lat: 37.8035,
    camera: { distance: 4600, yaw: 45, pitch: 24 },
  },
];
