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
  // 326 Brannan (JAX Vineyards Wine Court) — the NARROWEST exclusion window in
  // this registry, 1.04 m wide, and the reason is geometric rather than sloppy.
  // The parcel is a 7.98 x 24.32 m infill slot carrying TWO DataSF footprints
  // and BOTH have to go: the 5.66 m shed block would z-fight the modelled shed
  // and the court block would stand inside the modelled garden. Measured
  // against the pipeline's OWN cleaned rings (simplifyRing 0.6 m + ringCentroid,
  // i.e. the metric excluded() actually uses), from this anchor:
  //
  //   own court  201006.0135574 (95.2 m2) centroid 4.57 m  nearest vertex 3.54 m
  //   own shed   201006.0157667 (61.6 m2) centroid 6.80 m  nearest vertex 3.54 m
  //   NEIGHBOUR  201006.0007711 = 334 Brannan (462 m2, h 12.14 m):
  //                                         centroid 14.10 m nearest vertex 4.58 m
  //   neighbour  201006.0008516 = 318 Brannan (429 m2, h  8.11 m):        12.22 m
  //
  //   exclude 3.0-3.5 m -> drops 0  (asset stays buried under the baked blocks)
  //   exclude 3.9-4.5 m -> drops 2  (correct: both SF3775012 polygons)
  //   exclude 4.6 m+    -> drops 3  (eats 334 Brannan, holes the block face)
  //
  // The vertex that closes the window, local (3920.45, -1271.10), is PHYSICALLY
  // SHARED: it belongs to 334 Brannan's ring AND to both of 326's rings — the
  // party-wall corner, which the DataSF traces agree on exactly. No re-tracing
  // buys margin. Moving the anchor does not either: a numeric search finds a
  // 6.88 m window 4.60 m away, and displacing a 24 m lot by 4.6 m to buy
  // exclusion margin is what AGENTS rule 5 forbids.
  //
  // No Overture twin can appear on either parcel to spoil this: the Overture
  // gap-fill in buildings.mjs only ADDS a footprint where
  // occupiedFraction(bbox) <= 0.25, and DataSF already occupies both bboxes; its
  // height-correction branch is gated on h >= 20 m, far above either building.
  //
  // 4 is the midpoint, with 0.46 m of margin at each end. Do NOT raise it.
  {
    id: '326Brannan',
    name: '326 Brannan Street',
    lon: -122.3928965,
    lat: 37.7815080,
    height: 5.9,
    exclude: 4,
    camera: { distance: 120, yaw: 45, pitch: 34 },
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
  // The Blinn Estate Building (1912) at the east corner of 2nd and Brannan — six
  // storeys, 70 ft to the parapet, full-lot. The widest exclusion window in this
  // family, because the building fills its lot and its nearest neighbour is a
  // street away. Measured against the real bake inputs (both buildings_datasf and
  // overture_buildings, which each trace this footprint):
  //
  //   target: DataSF SF3775008 (1,140 m2, h 20.84) centroid 1.09 m, vertices 20.13 m
  //           Overture twin    (1,123 m2, h 21)    centroid 1.27 m, vertices 22.84 m
  //   nearest NEIGHBOUR: SF3775181 (1,353 m2, h 17.77) nearest vertex 21.42 m
  //
  //   exclude  2-21 m -> drops 2 rings  (correct: the target and its Overture twin)
  //   exclude 22 m    -> drops 3  (eats SF3775181 on its nearest vertex)
  //   exclude 24 m    -> drops 5
  //
  // TWO rings is the correct answer, not one — DataSF and Overture both carry this
  // building. 12 m is the middle of the safe band: 11 m of headroom under the
  // neighbour and ~11 m over the centroids that actually do the catching. Do not
  // raise past 20 without re-running the measurement.
  {
    id: '300Brannan',
    name: '300 Brannan Street',
    lon: -122.3925543,
    lat: 37.7818313,
    height: 25.2,
    exclude: 12,
    // camera.yaw is 180 - true bearing (camera.js apply() puts the eye at
    // pivot + (sin yaw, sin pitch, cos yaw)*distance with +z south). The view
    // this building wants is straight down the cant's outward normal, 95.1 deg
    // true, which is also the bisector of the two frontage normals — so
    // 180 - 95.1 = 85. yaw 95 would be the mirror image and stare at the party
    // wall. Verified from a rendered frame, not from the arithmetic.
    camera: { distance: 260, yaw: 85, pitch: 26 },
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
  {
    // The 1941 infill sliver between 550 and 574 — 30 x 80 ft, party walls on
    // THREE sides (550 wraps behind it), and the lowest roof on the block face
    // at 7.2 m against 11.0 and 11.05 next door. Its exclusion window is the
    // widest in this family despite the tightest site, because the gate that
    // catches it is its own CENTROID, not a vertex: the ring is only 246 m2, so
    // the centroid sits 0.82 m from the anchor (Overture's copy 0.17 m) while
    // its own vertices are 12.6 m out. Measured against the real bake input:
    //
    //   exclude  2-11 m -> drops 1  (correct: SF3776007 + its Overture twin)
    //   exclude 12 m    -> drops 2  (eats the Overture ring of 574, vertex 11.65 m)
    //   exclude 13 m    -> drops 3  (eats DataSF SF3776008, 574 proper, 12.55 m)
    //   exclude 15 m    -> drops 4  (eats 550 Third, SF3776005, 14.02 m)
    //
    // The band is 0.82 < r <= 11.65. 8 is the value 550Third and 551Third already
    // use on this block and leaves 3.6 m of headroom to the nearest neighbour.
    id: '560Third',
    name: '560 Third Street',
    lon: -122.3951188,
    lat: 37.7804142,
    height: 7.2,
    exclude: 8,
    // Camera offset is (sin yaw east, cos yaw south) — +z is south — so yaw 135
    // is east and NORTH of the pivot: the eye stands on Third Street looking
    // south-west, square onto the outward normal of the one elevation this
    // building has (44.1 deg). Rendered before it was believed: yaw 45 is the
    // mirror image and points at the blind south-east party wall.
    // No `key`: at 7.2 m this is texture in the block, not a destination.
    camera: { distance: 150, yaw: 135, pitch: 30 },
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
  // The 1929 Art Deco concrete loft on the NE corner of Brannan and Zoe, two
  // doors southwest of 400. Measured against the real bake inputs, from the
  // anchor below, using the metric excluded() applies — ring centroid OR any
  // ring vertex:
  //
  //   target: DataSF  SF3776151 (763.6 m2, h 11.46)  centroid 4.65 m, vertices 12.45 m
  //           Overture b9c9690e (788.0 m2, h 11)     centroid 8.11 m, vertices 12.00 m
  //   nearest NEIGHBOUR — 426 Brannan, in BOTH sources:
  //           DataSF  SF3776015 (163.8 m2, h 5.75)   nearest vertex 12.45 m
  //           Overture b9c91621 (178.4 m2, h 6)      nearest vertex 12.00 m
  //
  //   exclude  8 m    -> drops 1  (DataSF only; Overture's copy survives and fights the GLB)
  //   exclude  9-12 m -> drops 2  (correct: this building in both sources)
  //   exclude 12.5 m  -> drops 4  (eats 426 Brannan in both sources)
  //
  // TWO rings is the right answer, not one. The gate BELOW is Overture's
  // CENTROID at 8.11 m, not a vertex — its ring reaches 4 m further northwest
  // than DataSF's and pulls the centroid off the anchor. The gate ABOVE is a
  // SHARED PARTY-WALL VERTEX: 426 Brannan's nearest vertex is numerically
  // identical to this building's own in both sources, so any radius that reaches
  // our corner reaches the neighbour's. Safe band 8.11 < r < 12.00; 10 sits in
  // the middle with 1.9 m under and 2.0 m over. Do not raise past 11.5 or lower
  // under 9 without re-running the measurement.
  {
    id: '434Brannan',
    name: '434 Brannan Street',
    lon: -122.3954103,
    lat: 37.7796003,
    height: 13.79,
    exclude: 10,
    // camera.js apply() puts the eye at pivot + (sin yaw, sin pitch, cos yaw)
    // * distance with +z south, so yaw = 180 - the outward bearing you want to
    // look down. The Brannan front's normal is 134.8 deg true -> yaw 45, which
    // also catches the long Zoe flank obliquely. yaw 225 would be the mirror
    // image and stare at the rear car park.
    camera: { distance: 240, yaw: 45, pitch: 26 },
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
    // 1924 shopfront-and-flat on the north-west rim of the oval, arched upper
    // window under a red barrel-tile pent. Two things about this site are worth
    // reading before touching the numbers.
    //
    // 1. lon/lat is NOT the manifest anchor. The manifest anchor
    //    (-122.394862, 37.7812804) is where the BUILDING stands — the area
    //    centroid of the built footprint, which is the front ~26.5 m of a 36 m
    //    lot. This point is the centroid of the DataSF LiDAR footprint, which is
    //    the polygon the bake actually reads, and which covers the whole lot
    //    including the rear yard. They are 4.89 m apart. Measured from the
    //    manifest anchor no workable radius exists at all: it sits 3.0 m from
    //    156's nearest vertex and 4.89 m from the baked polygon's own centroid.
    //
    // 2. The window is one-sided, not two. `excluded()` in buildings.mjs drops a
    //    footprint whose centroid OR any ring vertex is inside the circle, so
    //    from this point our own building triggers at 0.00 m (its own centroid)
    //    and the ceiling is 156 South Park's shared party-line vertex at 1.70 m.
    //    Measured against committed tile 23_13, not guessed. 1.2 leaves 0.5 m.
    //
    // No clearTrees: there is a real street tree in front of this building — it
    // is the 17.05 m first-return peak in the LiDAR record — and it should stay.
    id: '160SouthPark',
    name: '160 South Park',
    lon: -122.3949116,
    lat: 37.7812949,
    height: 9.4,
    exclude: 1.2,
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with +x
    // east and +z south, so camera bearing = 180 - yaw; the 108.1 deg facade
    // wants yaw 72, standing out over the park. 155 m suits a 9.4 m building
    // (cf. 165-167 at 160 for 9.0 m, 135 at 150 for 8.5 m).
    camera: { distance: 155, yaw: 72, pitch: 26 },
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
    // South Park Lofts, 188 South Park / 549 3rd St. A 2002 four-storey
    // live/work loft building by Santos-Prescott (Adele Santos) on the north
    // rim of the South Park oval, with a penthouse/roof terrace reaching
    // 15.93 m. Through-lot: the building faces SE onto South Park and has a
    // patio/courtyard toward 3rd St at the NW end.
    //
    // The anchor is the DataSF LiDAR footprint's area centroid (not the OSM
    // OBB centre), for the same reason as 165SouthPark next door: on a
    // party-wall site, centring the exclusion circle on the DataSF area
    // centroid opens the widest viable window. excluded() drops a footprint
    // when its centroid OR any ring vertex falls inside the radius. Measured
    // from this anchor against the DataSF footprints excluded() consumes:
    //
    //   0.00 m  this building's own footprint (SF3775125), via centroid
    //   8.76 m  OSM way 124884355 (untagged), nearest vertex — may not be
    //           a separate Overture footprint; if not, the ceiling is 12.95 m
    //   12.95 m SF3775070 (166-168 South Park), nearest ring vertex
    //   17.50 m 521-527 3rd St (way 124884350), nearest vertex
    //   21.53 m 164 South Park (way 124884357), nearest vertex
    //
    // The conservative safe window is (0.1, 8.76) m; the wide window (if the
    // untagged OSM way is not a separate Overture footprint) is (0.1, 12.95).
    // 5 sits in the middle of the conservative window with ~3.8 m of margin
    // at both ends. Do not raise past 8 without re-running audit.mjs check 1.6.
    id: '188SouthPark',
    name: '188 South Park',
    lon: -122.3950794,
    lat: 37.7810118,
    height: 15.93,
    exclude: 5,
    camera: { distance: 190, yaw: 315, pitch: 26 },
  },
  {
    // A 1959 two-storey commercial building at the WEST TIP of the South Park
    // oval, on a wedge lot: 5.5 m of frontage widening to 9.7 m over an 18.7 m
    // depth, because South Park Street curves around the end of the ellipse
    // while the party walls stay on the old rectilinear lot lines.
    //
    // The tightest window in this file, and the clearest demonstration of why
    // the half-diagonal rule is wrong rather than merely risky. excluded() drops
    // a footprint when its centroid OR ANY ring vertex falls inside, and here
    // those two tests point in opposite directions. Measured from this anchor
    // against the actual bake input:
    //
    //                                     nearest vertex   centroid
    //   own footprint (DataSF SF3775065)       6.10 m       3.24 m
    //   own footprint (Overture)               6.56 m       1.37 m
    //   156 South Park (DataSF SF3775066)      6.10 m       8.50 m
    //   156 South Park (Overture)              6.56 m       9.52 m
    //   140 South Park (DataSF SF3775064)     11.34 m      13.18 m
    //   140 South Park (Overture)              9.83 m       9.73 m
    //
    // This building has to be cleared by its CENTROID at 3.24 m, because its
    // own nearest vertex, 6.10 m, is a party-wall node it SHARES with 156 South
    // Park - which is why both report exactly 6.10 m in DataSF and exactly
    // 6.56 m in Overture. That is not a coincidence, it is the same point, so
    // no radius reaches our corner without reaching the neighbour's.
    //
    // Safe window: 3.24 < r < 6.10. 4.5 sits mid-window with 1.3 m of headroom
    // over our own centroid and 1.6 m below 156's vertex. Do NOT raise it: the
    // half-diagonal here would be ~9.5 m and would delete 156 AND 140, punching
    // a two-lot hole in the row at the head of the park, which is far more
    // visible than the building itself.
    //
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with +x
    // east and +z south, so yaw 46 stands south-east of the building - square
    // onto the South Park front, looking back over the head of the oval. 140 m
    // suits an 8 m building (cf. 135 South Park at 150 for 8.5 m).
    id: '150SouthPark',
    name: '150 South Park',
    lon: -122.3947673,
    lat: 37.781381,
    height: 8.0,
    exclude: 4.5,
    camera: { distance: 140, yaw: 46, pitch: 26 },
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
    // 156 South Park Street (1924) — the Anchor Packing Co. warehouse, and the
    // one building of the South Park Historic District's twenty-three
    // contributors that the 2009 Page & Turnbull survey found UNALTERED.
    //
    // The tightest exclusion window in this registry after 155 South Park, and
    // for the same reason: this is a party-wall row, so the neighbours' rings
    // SHARE vertices with this one and `excluded()` drops a footprint when its
    // centroid OR ANY ring vertex falls inside. Measured against the real bake
    // input (DataSF + Overture, from this anchor):
    //
    //   1.62 m  this footprint's centroid, DataSF SF3775066
    //   2.48 m  this footprint's centroid, Overture 13c3c919 (h=6)
    //   3.40 m  SHARED party-wall vertex with 150 South Park, Overture 8fdc6a7d
    //   4.01 m  SHARED party-wall vertex with 150 South Park, DataSF SF3775065
    //
    // So the safe window is [2.6, 3.4): below 2.6 the Overture footprint
    // survives and a 6 m procedural block stands inside the model; at 3.4 the
    // shared vertex takes 150 South Park out with it and punches a hole in the
    // row. 3 sits in the middle with ~0.5 m of margin at both ends. A drop
    // simulation over both sources confirms r=3 removes EXACTLY ONE footprint
    // per source. Do not change this without re-running that simulation.
    //
    // height is the LiDAR MAXIMUM (8.74 m), the two-storey street bar's parapet
    // crest — not the 5.67 m median or OSM's height=6, which both describe the
    // single-storey shed behind it that covers most of the lot.
    //
    // App yaw = 180 − true bearing (see the note on 592Third, and camera.js
    // `apply()`: the offset is (sin yaw, ·, cos yaw) with +z south). The front
    // faces 117.3°, so yaw 63 puts the camera east-south-east, out over the
    // South Park oval, looking back at the only designed elevation.
    id: '156SouthPark',
    name: '156 South Park',
    lon: -122.3948748,
    lat: 37.7813535,
    height: 8.7,
    exclude: 3,
    camera: { distance: 180, yaw: 63, pitch: 26 },
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
    lon: -122.41761,
    lat: 37.7794895,
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
  {
    // The Corinthian, 1915: apartments over a bank/retail base at the NE corner
    // of Van Ness and McAllister. 500 Van Ness is the retail address; the
    // assessor files the parcel as 512 Van Ness (Block 0766, Lot 006).
    //
    // This entry deletes nothing, and that is deliberate. Measured against the
    // committed tiles (buildings/19_13.bin + its eight neighbours):
    //   no footprint covers this anchor at all — civicCenterCourthouse's
    //     exclude: 52 reaches to within 7.5 m of it and already took this block
    //   32.8 m  nearest SURVIVING footprint vertex (1,148 m2, 14.3 m tall,
    //     the office block north of us); its centroid is 47.1 m out
    //   25.4 m  this building's own furthest ring vertex
    // So 28 m covers our own footprint on its own merits — the entry stays
    // correct if the courthouse radius is ever tightened — while leaving 4.8 m
    // of margin to the neighbour. Sizing this off OSM rings instead of the bake
    // suggested a 10-17 m window; the bake's footprints are not OSM's.
    id: '500VanNess',
    name: '500 Van Ness Avenue (The Corinthian)',
    lon: -122.419922,
    lat: 37.7804082,
    height: 17,
    exclude: 28,
    camera: { distance: 320, yaw: 232, pitch: 24 },
  },
  {
    // 1913 flats on the north-west arc of the South Park oval. The lot carries
    // TWO baked footprints — the flats 8.5 m south-east of the anchor and the
    // rear cottage 10.4 m north-west of it — and the anchor itself sits in the
    // open courtyard between them, because that is where the GLB's bounding-box
    // centre has to be. No single radius works. Measured from each candidate
    // centre against the rings the bake actually sees (DataSF ynuv-fyni after
    // simplifyRing(0.6)), remembering that excluded() drops a footprint whose
    // ring CENTROID or any vertex is inside:
    //
    //   from the anchor:          3.59 m  126 South Park vertex  <- the ceiling
    //                             3.78 m  own front block, nearest vertex
    //                             8.49 m  own front block, ring centroid
    //                            10.40 m  own rear block, ring centroid
    //   from the front centroid:  0.00 m  own front block centroid
    //                             5.86 m  126 South Park vertex
    //   from the rear centroid:   0.00 m  own rear block centroid
    //                             5.31 m  136 South Park vertex
    //
    // So the anchor cannot reach either of this lot's own centroids (8.5 /
    // 10.4 m) without eating 126 South Park at 3.59 m, and 136 South Park goes
    // at 9.8 m. Neither has a GLB to replace it and the failure is silent.
    // Hence one zone per structure, each sitting on its footprint's ring
    // centroid and dropping it by the centroid test, exactly as 551Third's
    // kiosk zone does. Margins 2.9 m and 2.3 m.
    //
    // The 2 m zone at the anchor drops nothing today. It is the guard against
    // the Overture gap-fill pass re-filling a lot that markOccupied() no longer
    // sees as occupied once the DataSF footprints are excluded: a whole-lot
    // Overture polygon would centre within ~0.6 m of the anchor and sail past
    // both other zones. Do NOT raise it — 126 South Park's vertex is 3.59 m out.
    // See docs/asset-plans/132-south-park.md 2.13.
    id: '132SouthPark',
    name: '130-134 South Park',
    lon: -122.3946173,
    lat: 37.7815393,
    height: 12.07,
    exclude: 2,
    extraExclusions: [
      { lon: -122.3945566, lat: 37.7814859, r: 3 }, // front flats
      { lon: -122.3947038, lat: 37.7816116, r: 3 }, // rear cottage
    ],
    // Camera bearing = 180 - yaw (camera.js apply(): offset is
    // (sin yaw, ., cos yaw) and +z is south), so yaw 45 stands the camera at
    // bearing 135 = SE, square onto the park front. Same value as 380Brannan,
    // whose front faces the same way. No `key`: at 12 m this is texture in the
    // block, not a destination.
    camera: { distance: 200, yaw: 45, pitch: 26 },
  },
  {
    // The Gran Oriente Filipino Hotel, 104-106 South Park: a 1907 three-storey
    // rooming house by W. L. Schmolle on the north-west rim of the oval,
    // occupying the whole of a 24 x 97.5 ft lot (7.32 x 29.72 m) with frontages
    // on South Park Street and Taber Place. NR-nominated 2019 for Filipino
    // ethnic heritage; 24 units of affordable housing since the 2020-21
    // Mission Housing rehabilitation. Crest 11.58 m (38 ft, published) against
    // a LiDAR roof deck of 11.02 m.
    //
    // The exclusion band here is 0.88 m wide and BOTH ends are set by different
    // sources, so it is measured, not guessed. excluded() drops a footprint when
    // its centroid OR any ring vertex falls inside the radius; measured from
    // this anchor against the two files the bake actually reads
    // (pipeline/data/buildings_datasf.geojson and
    // overture_buildings.geojsonseq, 16 Aug 2026):
    //
    //       polygon                        DataSF    Overture
    //       104-106 (this)                   0.09 m    1.65 m
    //       102 South Park (Caffe Centro)    3.89 m    2.53 m
    //       108-110 South Park               3.83 m    8.07 m
    //       112 South Park                  14.37 m   14.18 m
    //
    // So r must EXCEED 1.65 — below that the Overture gap-fill re-adds this
    // building on top of the asset, because addBuilding() returns null on
    // exclusion so markOccupied() never runs and occupiedFraction() cannot
    // block it — and stay UNDER 3.83, or 108-110 disappears and leaves a hole
    // where a real building stands (AGENTS rule 5). 2.1 sits in the middle with
    // 0.45 m below and 0.43 m of margin to 102's Overture vertex at 2.53.
    //
    // Staying under 2.53 is belt-and-braces rather than load-bearing: 102's
    // DataSF footprint survives at 3.89 m and marks its bbox occupied, so its
    // Overture twin would never be added anyway. Keeping the radius below it
    // means the re-bake diff says so without anyone having to re-derive that.
    //
    // No clearTrees: the large street tree in front of this building is real,
    // is the single most photographed thing about it, and at 2.1 m this radius
    // clears no street furniture in any case.
    id: '106SouthPark',
    name: 'Gran Oriente Filipino Hotel (104-106 South Park)',
    lon: -122.3944099,
    lat: 37.7817221,
    height: 11.58,
    exclude: 2.1,
    // app/src/camera.js places the rig at (sin(yaw), sin(pitch), cos(yaw)) x
    // distance from the pivot, and this project's +z is SOUTH, so yaw 45 puts
    // the camera south-east of the building — over the oval, looking north-west
    // at the street elevation, which is the only view of it worth flying to.
    camera: { distance: 150, yaw: 45, pitch: 26 },
  },
  {
    // The first landmark on the NORTH rim of the South Park oval, and a
    // party-wall row building attached on BOTH flanks — 104-106 (the Gran
    // Oriente Filipino Hotel, 11 m) north-east and 112 (6 m) south-west, both
    // sharing vertices with this footprint at 0.00 m in OSM. That reads like the
    // 165 South Park situation, where no radius centred on the manifest anchor
    // worked at all, so the window was measured rather than assumed — against
    // the two sources the bake actually consumes
    // (pipeline/data/buildings_datasf.geojson and
    // overture_buildings.geojsonseq), and remembering that excluded() drops a
    // footprint when its centroid OR any ring vertex is inside the radius:
    //
    //   polygon                                   vertex   centroid   trigger
    //   this building, Overture 86058388          15.04 m    0.21 m     0.21 m
    //   this building, DataSF SF3775059            4.09 m    0.71 m     0.71 m
    //   104-106 South Park, DataSF SF3775058       4.64 m    7.91 m     4.64 m  <- the ceiling
    //   112 South Park, Overture 0675706c          9.62 m    6.28 m     6.28 m
    //   112 South Park, DataSF SF3775060          10.71 m    6.62 m     6.62 m
    //   104-106 South Park, Overture aa14bd23     10.43 m    6.74 m     6.74 m
    //
    // So the safe band is (0.71, 4.64) and it is wider than 165's because the
    // two DataSF rings here are NOT vertex-coincident the way the OSM ways are.
    // 2.7 sits in the middle with ~2 m of margin at both ends, and a sweep
    // confirms every radius from 0.8 to 4.6 drops exactly these two rings and
    // nothing else. Do NOT raise it past 4.6: at 4.7 the Gran Oriente Filipino
    // — a National Register-nominated building with no hand-built replacement —
    // disappears from the baked city and nothing crashes to tell you.
    //
    // Both Overture and DataSF have to be cleared, not just DataSF: addBuilding()
    // returns null on exclusion so markOccupied() never runs, and the Overture
    // gap-fill would re-add this building afterwards. 2.7 clears both.
    id: '108SouthPark',
    name: '108-110 South Park (South Park Cafe)',
    lon: -122.3944817,
    lat: 37.7816789,
    height: 8.45,
    exclude: 2.7,
    // camera.js apply() puts the eye at target + distance*(sin yaw, ., cos yaw)
    // with +x east and +z south, so bearing = 180 - yaw and yaw 45 stands the
    // camera at 135 deg — square onto the shopfront. Same derivation as
    // 380Brannan, whose SE-facing front also carries yaw 45. 150 m suits an
    // 8.45 m building (cf. 135 South Park at 150 for 8.5 m).
    camera: { distance: 150, yaw: 45, pitch: 26 },
  },
  {
    // 166-168 South Park: a 1912 two-storey red-brick office loft on the
    // north-west rim, one lot wide and five lots deep — 6.10 m of frontage
    // running 29.82 m back. Party walls on BOTH flanks: the OSM ring shares
    // nodes with 188 South Park (way 124884339, SW) and 164 South Park (way
    // 124884357, NE). targetHeight is the raised central parapet crown (LiDAR
    // max 10.44 m); the roof deck behind it is the LiDAR median, 7.98 m.
    //
    // The anchor is the OSM ring's area centroid, NOT the DataSF LiDAR
    // centroid — the opposite of the choice made for 165-167 and 188 next door,
    // and deliberately so. On their wide, near-square footprints the two
    // centroids differ by centimetres. On a 6 m sliver they are 1.08 m apart
    // and the DataSF outline is inflated 1.3 m across a 6.10 m width, so
    // anchoring on it would place the model over a metre off its own party
    // walls. The OSM ring is also the topologically correct one: it is the
    // outline the shared walls actually follow.
    //
    // excluded() drops a footprint when its centroid OR any ring vertex falls
    // inside the radius. Measured from this anchor against the ACTUAL bake
    // input (DataSF + the Overture gap-fill, projected and simplified at the
    // 0.6 m tolerance):
    //
    //    0.00 m  this building's own Overture footprint (8b933808..., =
    //            OSM way 124884342), via centroid — the trigger
    //    1.07 m  this building's own DataSF footprint (SF3775070), via
    //            centroid — the FLOOR
    //    2.95 m  188 South Park's front (SF3775125), nearest vertex
    //    3.28 m  188 South Park's front (Overture 9f571039...), nearest vertex
    //            — both already dropped by 188SouthPark's own zone, so a
    //            radius past them changes nothing
    //    8.05 m  OSM way 124884355 (Overture c73e5800..., height 15 m,
    //            208 m2 — 188's rear block), nearest vertex — the CEILING
    //    9.93 m  164 South Park (Overture 31645c36...), nearest vertex
    //   10.04 m  164 South Park (SF3775069), nearest vertex
    //   12.60 m  160 South Park (SF3775067), nearest vertex
    //
    // The safe window is (1.07, 8.05) — 7.0 m wide. 5 sits in it with 3.93 m
    // of margin below and 3.05 m above, and matches every other South Park rim
    // landmark. The larger margin is deliberately on the floor side: that bound
    // is a LiDAR centroid, the value most likely to move in a data refresh,
    // while the ceiling is an OSM trace. Verified on the re-bake: exactly one
    // footprint dropped beyond what 188SouthPark already drops, and 164 South
    // Park still standing. Do not widen past 8 without re-running audit 1.6.
    //
    // Aside, out of scope here: way 124884355 bakes as a 15 m procedural block
    // immediately behind the 188 South Park landmark asset. That is a
    // pre-existing condition of 188's integration, not something this zone
    // creates, and it wants its own look.
    id: '168SouthPark',
    name: '166-168 South Park',
    lon: -122.3949862,
    lat: 37.7811327,
    height: 10.44,
    exclude: 5,
    camera: { distance: 170, yaw: 45, pitch: 26 },
  },
  {
    // 1907 wood-frame light-industrial loft at the WEST TIP of the South Park
    // oval — the district survey's only "wood frame instead of brick" building.
    // A 6.84 x 29.81 m stick at 45 deg, so the exclusion radius is derived
    // rather than guessed. `excluded()` in pipeline/buildings.mjs drops a
    // footprint when its AREA centroid (ringCentroid) OR any ring vertex falls
    // inside the circle, and the bake reads DataSF first then gap-fills from
    // Overture (which carries OSM geometry), so both sources bind. Measured
    // from this anchor:
    //
    //                                    nearest vertex   area centroid
    //   own footprint (DataSF SF3775064)      9.54 m          0.09 m
    //   own footprint (OSM way/124884359)     6.64 m          1.38 m  <- lower bound
    //   150 South Park (DataSF SF3775065)     5.27 m  <- upper bound   9.56 m
    //   150 South Park (OSM way/124884352)    6.64 m          9.27 m
    //   136 South Park (DataSF SF3775063)     9.57 m         13.58 m
    //
    // Safe window 1.38 < r < 5.27. 3 sits in the middle with 1.62 m of headroom
    // over the binding self-centroid and 2.27 m below the binding neighbour
    // vertex — both comfortably larger than the bake's 0.6 m SIMPLIFY_TOLERANCE.
    // Do NOT raise it: 150 South Park is an existing 8 m building on the oval
    // with no GLB behind it, and above 5.3 its party-wall vertex falls inside
    // the circle and the bake punches a hole in the row that nothing fills.
    //
    // The anchor is the DataSF OBB centre rather than the OSM centroid
    // specifically because it widens this window; from the OSM centroid the
    // safe band is only 1.46-3.99 m. The two are 1.38 m apart.
    id: '140SouthPark',
    name: '140 South Park',
    lon: -122.3947379,
    lat: 37.7814643,
    height: 10.68,
    exclude: 3,
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with +x
    // east and +z south, so yaw 45 stands south-east of the building — square
    // onto the South Park front, the only elevation with any ornament on it.
    camera: { distance: 150, yaw: 45, pitch: 26 },
  },
  {
    // 126 South Park: a 6.90 x 29.79 m sliver on the oval's west arc, 1907,
    // two storeys, party walls down BOTH long flanks at a 0.6 m gap. Same
    // radius rule as its neighbours — excluded() drops a footprint when its
    // centroid OR ANY ring vertex falls inside the circle — but the geometry
    // here is unusually forgiving, and for a reason worth recording: on a
    // 29.79 m long building the area centroid sits ~15 m from either end, so
    // the party-wall neighbours' VERTICES stay 4.67 m away even though their
    // walls are 0.6 m away. A squarer building wedged between the same two
    // neighbours would have had no valid window at all.
    //
    // Measured from this anchor against the actual bake input:
    //   0.01 m  this footprint's centroid (OSM way/124884348) — always caught
    //   2.19 m  this footprint's centroid (DataSF SF3775061) — the real floor
    //   2.32 m  this footprint's nearest vertex (DataSF)
    //   2.78 m  this footprint's nearest vertex (OSM)
    //   4.67 m  112 South Park (OSM way/124884354), nearest vertex — the ceiling
    //   4.85 m  112 South Park (DataSF SF3775060), nearest vertex
    //   4.97 m  130/134 South Park (DataSF SF3775062), nearest vertex
    //   5.53 m  130/134 South Park (OSM way/124884351), nearest vertex
    //
    // The bake reads DataSF first and gap-fills from Overture (OSM geometry),
    // so both rows bind. Safe window (2.19, 4.67); 3.5 sits in the middle with
    // 1.31 m of floor and 1.17 m of ceiling. Do not raise past 4.5 without
    // re-running audit.mjs check 1.6 — at 4.7 it starts eating 112 South Park.
    id: '126SouthPark',
    name: '126 South Park',
    lon: -122.3945863,
    lat: 37.7816006,
    height: 7.6,
    exclude: 3.5,
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with
    // +x east and +z south, so yaw 45 stands south-east of the building —
    // square onto the South Park front. 130 m rather than the ~100 m its 7.6 m
    // height suggests, because the building is 29.79 m long and needs the room.
    camera: { distance: 130, yaw: 45, pitch: 26 },
  },
  {
    // The Park View (1913, ex-Hotel Bo-Chow), the SRO over Caffe Centro on the
    // NORTH rim of the oval — the first of this set that is not on the south
    // side. A 25-foot lot with the Gran Oriente Filipino at 106 ATTACHED on the
    // southwest, sharing light wells with it.
    //
    // MEASURE ON THE SIMPLIFIED RING, NOT THE RAW ONE. `addBuilding()` in
    // buildings.mjs runs `simplifyRing(ring, 0.6)` BEFORE it calls `excluded()`,
    // so the ring the gate sees is not the ring in the geojson. On this site that
    // distinction moves the ceiling by 3.5 m: the shared light-well vertices that
    // put 106's raw ring 3.03 m from this anchor are all simplified away, and its
    // real nearest approach is 6.50 m. A raw-ring reading would have forced a
    // radius of 2.6 — workable, but sitting 0.4 m off the floor for no reason.
    //
    // Measured on simplified rings from BOTH bake inputs (the Overture gap-fill
    // runs through the same gate), distances from this anchor:
    //
    //   Overture 102 (h 14.2)   centroid  0.19 m
    //   DataSF SF3775057 (102)  centroid  2.02 m, vertex 2.16 m  <- the floor
    //   DataSF SF3775058 (106)  centroid  6.50 m, vertex 7.85 m  <- the ceiling
    //   Overture 106 (h 11)     centroid  7.53 m
    //   DataSF SF3775059 (108)  centroid 13.78 m
    //
    //   r <= 2.0 m  -> drops 1  (only the Overture copy; the DataSF block stays
    //                            and the asset sits inside a procedural building)
    //   r 2.1-6.4 m -> drops 2  (correct: both source copies of THIS building)
    //   r >= 6.5 m  -> drops 3  (eats 106, which has no GLB to replace it)
    //
    // 4 is the middle of that band: 1.84 m clear of the floor, 2.5 m clear of the
    // ceiling. Confirmed against the re-bake — tile 23_13 went 217 -> 215
    // footprints and the only one removed within 22 m of the anchor is the 15.0 m
    // block that stood at 1.95 m. Do not raise it past 6.
    //
    // Note also that Overture carries height 14.2 m for this footprint and places
    // its centroid 0.19 m from this anchor, which independently corroborates both
    // the asset's estimated 14.0 m cornice crest and the OSM-derived anchor.
    id: '102SouthPark',
    name: 'The Park View (102 South Park)',
    lon: -122.3943678,
    lat: 37.7817707,
    height: 14.0,
    exclude: 4,
    // camera.yaw is 180 - the compass bearing the camera stands at (offset is
    // (sin yaw, ., cos yaw) and +z is south, so bearing = atan2(sin yaw, -cos yaw)
    // = 180 - yaw). The front faces 135.4 deg and the exposed NE flank 45.0, so
    // bearing 105 is the three-quarter that shows both — yaw 75. Setting yaw to
    // the frontage bearing itself would park the camera at bearing 45, square
    // onto the flank with the arched facade edge-on.
    camera: { distance: 170, yaw: 75, pitch: 26 },
  },
  {
    // The 1923 Kohler Co. plumbing-supply warehouse at 544 Second Street /
    // 2 South Park, closing the east end of the South Park oval. Three storeys
    // of unreinforced brick to a 12.83 m roof deck, with a stair/lift penthouse
    // at 17.72 m. A corner lot: Second Street on the NE, South Park on the SE,
    // Taber Place (an alley) on the NW, and a party wall on the SW.
    //
    // This is the one South Park entry anchored on the DataSF surveyed PARCEL
    // centroid rather than the LiDAR footprint centroid, and the reason is that
    // it can afford to be. 165SouthPark and 188SouthPark are party-wall sites on
    // the narrow rim of the oval where the safe window is a few metres wide and
    // centring on the bake input's own ring centroid is the only way to open one.
    // Here the window is nearly 14 m, so AGENTS rule 5 wins: put the model where
    // the survey says the building is. The three surveys agree on the shape to
    // within a metre (parcel 29.81 x 20.91 m, OSM 29.77 x 21.27, DataSF LiDAR
    // 29.69 x 22.11) and their centroids sit within 2.9 m of each other.
    //
    // excluded() drops a footprint when its centroid OR any ring vertex falls
    // inside the radius. Measured from this anchor against the actual bake input
    // (DataSF footprints primary, Overture/OSM gap-fill):
    //
    //    2.10 m  this building's own DataSF footprint (SF3775005), via centroid
    //    2.90 m  this building's own OSM/Overture way 112926339, via centroid
    //            -> the FLOOR: below this the procedural twin survives
    //   16.76 m  SF3775106 (the South Park party-wall neighbour), nearest vertex
    //            -> the CEILING, and the binding constraint
    //   17.29 m  OSM way 112926341 (the same neighbour), nearest vertex
    //   19.35 m  SF3775004, nearest ring vertex
    //   19.44 m  OSM way 112926337 (524 Second Street), nearest vertex
    //   28.78 m  SF3775048 (across Taber Place), nearest ring vertex
    //
    // Safe window (2.90, 16.76) m. 9 sits near the middle with 6.10 m of margin
    // below and 7.76 m above — the most comfortable exclusion in this row, which
    // is what a corner lot with two streets and an alley around it buys you.
    // Note both of this building's own footprints clear the floor by their
    // CENTROIDS, not their vertices (nearest own vertex is 13.5-14.4 m out);
    // that is normal for a 9 m circle around the middle of a 30 x 21 m building.
    id: '2SouthPark',
    name: '2 South Park',
    lon: -122.3932364,
    lat: 37.7824236,
    height: 17.72,
    exclude: 9,
    camera: { distance: 200, yaw: 90, pitch: 26 },
  },
  {
    // 86-96 South Park: Toby S. Levy's 1996 six-unit live/work condominium, and
    // the only Modernist building on the oval. ONE surveyed 435 m2 corner parcel
    // (block 3775, lots 116-121 -- six condominium lots on one polygon) carrying
    // TWO baked footprints: the 208.7 m2 front block on South Park and the
    // 81.0 m2 rear bar down Jack London Alley, with an open paved court between
    // them. "92 South Park" is one of six unit addresses on it, all five of the
    // others created by a single 2003 address-assignment permit against 86.
    //
    // The exclusion window is 5.04 < r < 10.77 and BOTH ends are set by CENTROID
    // tests rather than vertices, which is unusual -- excluded() drops a
    // footprint when its centroid OR any ring vertex is inside the radius, and
    // sizing this one off vertices alone gives the wrong answer at both ends.
    // Measured from THIS anchor (the shipped GLB's bbox centre, 1.06 m from the
    // footprints' OBB centre) against the two files the bake actually reads
    // (pipeline/data/buildings_datasf.geojson and
    // overture_buildings.geojsonseq), after simplifyRing(0.6):
    //
    //       polygon                              centroid   vertex
    //       own front block   (DataSF)             6.02 m    0.64 m
    //       own twin 552799e9 (Overture, h 10.8)   6.06 m    2.27 m
    //       own rear bar      (DataSF)            10.16 m    4.18 m
    //       own twin ea748f47 (Overture, 4 flr)    5.04 m   12.36 m   <- floor
    //       84 South Park     (Overture, h 11)    10.77 m   13.56 m   <- ceiling
    //       84 South Park     (DataSF)            10.94 m   13.66 m
    //       76-82 South Park  (DataSF)            17.96 m   14.73 m
    //
    // So r must EXCEED 5.04 -- below that the Overture gap-fill re-adds OSM way
    // 113545691 straight through the asset. That way carries no `height` tag at
    // all, but overtureHeight() falls through to num_floors * 3.2 + 1 = 13.8 m,
    // and addBuilding() returns null on exclusion so markOccupied() never runs
    // and occupiedFraction() cannot block it. And r must stay UNDER 10.77, or
    // 84 South Park disappears and leaves a hole where a real building stands
    // (AGENTS rules 3 and 5): the two buildings share a party wall, so 84's
    // centroids sit CLOSER to this anchor than its own nearest vertices do.
    // 7.8 sits in the middle with 2.76 m below and 2.97 m of margin above, both
    // far larger than the bake's 0.6 m SIMPLIFY_TOLERANCE.
    //
    // VERIFIED AGAINST THE BAKE, not just against the source files: cell 23_13
    // goes 201 -> 199 and drops exactly these two footprints and nothing else.
    // Their baked ring centroids sit 1.61 m and 9.79 m from this anchor -- the
    // bake's own simplifyRing/orientRing pass moves an area-weighted centroid on
    // a strongly notched ring by a few metres, so the source-file numbers above
    // are the SIZING method, and these are the proof. The nearest surviving
    // neighbour in the baked cell is 84 South Park at 12.82 m, which leaves 5.0 m
    // of real margin above 7.8 rather than the 2.97 m the source files predicted.
    // Nothing was gap-filled back in.
    //
    // No clearTrees: the street trees on the South Park frontage are real, they
    // are in every photograph of this building from 1996 to 2025, and at 7.8 m
    // the radius does not reach the kerb line.
    // See docs/asset-plans/92-south-park.md 2.13 and
    // artifacts/92-south-park/REFERENCE.md 7.
    id: '92SouthPark',
    name: '92 South Park (86-96 South Park)',
    lon: -122.3941549,
    lat: 37.7819082,
    height: 13.28,
    exclude: 7.8,
    // Camera bearing = 180 - yaw (camera.js apply(): the offset is
    // (sin yaw, ., cos yaw) and +z is south), so yaw 45 stands the camera at
    // bearing 135 = SE, square onto the South Park front and looking straight
    // at the corner tower. Same value as 132SouthPark, whose front faces the
    // same way.
    camera: { distance: 200, yaw: 45, pitch: 26 },
  },
  {
    // A 0.86-acre PARK, not a building — the second such entry after
    // civicCenterPlaza, and the first where the buildings job has nothing to do
    // at all.
    //
    // `exclude: 12` deletes NOTHING, and that is the measured answer, not a
    // guess. Counted over the 320 baked footprints within 400 m of the anchor
    // in cells 22-24_12-14, with the metric `excluded()` uses (centroid OR any
    // ring vertex inside the radius):
    //   0 footprints have any vertex inside the park ring
    //   22.81 m   nearest baked ring VERTEX (24.2 m tall, the row on the
    //             Bryant side)  <- must survive
    //   r <= 20 m drops 0;  r = 30 drops 4;  r = 40 drops 12;  r = 80 drops 44
    // So the window is 0 < r < 22.8 and 12 m sits in the middle of it. The
    // usual half-diagonal rule would put r at 79.8 m and delete 44 real
    // buildings — most of the block, including houses that have no GLB to
    // replace them. The radius is kept non-zero so the site is registered in
    // exclusionZones() and audit check 1.6 guards it against a future bake
    // dropping a footprint onto the park.
    //
    // A trap for whoever runs verify-rebake.mjs next: it reports cell 23_13
    // moving 217 -> 216 and blames this entry, because this is the new landmark
    // in that cell. It is not this entry. The footprint that disappears sits
    // 102.8 m away and is taken by 188SouthPark's exclude: 5 — that entry
    // landed source-only on 15 Aug 2026 and the committed tiles were last baked
    // on the 13th, so its exclusion had never actually been applied. A fresh
    // bake settles every pending neighbour's debt at once; attribution by cell
    // cannot tell them apart.
    //
    // `clearTreesRadius: 80` is the job that actually matters here. The park is
    // leisure=park, so the landcover scatter drops procedural lollipops the
    // length of it, standing among 34 hand-modelled trees and looking like a
    // different world. Counted against the committed toyland tiles:
    //   radius   left INSIDE the park   cut OUTSIDE it
    //     40 m           11                    0
    //     60 m            5                    0
    //     80 m            0                    0     <- 79.76 m half-diagonal
    //    110 m            0                    2
    // 80 m clears all 25 and costs nothing: this is party-wall SoMa and there
    // are no mapped street trees within 80 m of the park's centre. A circle is
    // a poor fit for a 6.8:1 lozenge, and it only gets away with it because of
    // that. Measure it the same way if the block ever changes.
    id: '64SouthPark',
    name: 'South Park',
    lon: -122.3939704,
    lat: 37.7815903,
    height: 15.0,
    exclude: 12,
    clearTrees: true,
    clearTreesRadius: 80,
    // App yaw = 180 - true bearing, so yaw 315 stands the camera at 225 deg —
    // south-west, at the Third Street entry — looking north-east ALONG the
    // park's 45.47 deg axis, with the Shout nearest the eye and 160 m of
    // promenade running away from it. On a lozenge this thin there is no
    // three-quarter that shows the whole thing; the axis is the composition.
    // Verified by render, not derived on paper (the 592Third lesson).
    camera: { distance: 400, yaw: 315, pitch: 24 },
  },
  {
    // 21-29 South Park, the 1919 unreinforced-brick warehouse closing the
    // south-east side of the oval at its Second Street end. Two storeys of
    // painted brick to a 9.50 m deck, a corbelled cornice at 10.20 m and a
    // stair/lift bulkhead at 11.73 m (the LiDAR maximum, and the asset's crest).
    // Office since 1991; Redpoint Ventures took the ground floor in 2016.
    //
    // The one landmark on this oval whose STREET WALL BENDS: 19.69 m facing
    // NW 315.7 deg, a re-entrant corner, then 12.07 m facing WNW 286.7 deg,
    // because the lot fronts the curve of the oval where it closes. Party walls
    // on the other three sides (17-19 South Park NE, the Brannan row SE,
    // 35 South Park SW), so only the bent front is exposed.
    //
    // ANCHOR NOTE — this entry does NOT use the footprint's OBB centre, and that
    // is deliberate, not an oversight to be tidied later. The footprint is a
    // skewed quadrilateral (its front is cut on a 29 deg diagonal), so its OBB
    // centre and its WORLD-AXIS-ALIGNED bbox centre are 2.63 m apart.
    // placeGeneric() seats the MODEL'S ORIGIN at the anchor and the contract
    // makes that origin the model's XY bbox centre, so anchoring on the OBB
    // centre would put the building 2.63 m west of its real footprint (AGENTS
    // rule 5). The value below is the AABB centre; the area centroid is 1.63 m
    // away and the OBB centre 2.63 m.
    //
    // excluded() in buildings.mjs drops a footprint when its centroid OR any
    // ring vertex falls inside the radius. Measured from THIS anchor against the
    // real committed bake inputs, after projection and simplifyRing(0.6):
    //
    //    1.68 m  own DataSF footprint SF3775042 (1115 m2), via CENTROID
    //            -> the floor when only DataSF is in play
    //    4.74 m  Overture db50f6d6 (= OSM way 112759868, "27"), via centroid
    //    7.93 m  Overture 11e21079 (= OSM way 112759863, "21"), via centroid
    //   14.60 m  Overture 428ebb71 (= OSM way 112759865, "29"), via centroid
    //            -> the FLOOR, because OSM/Overture trace this ONE building as
    //               THREE, and the third piece's centroid is 14.6 m out
    //   17.29 m  Overture b59deafe (17-19 South Park), nearest VERTEX
    //            -> the CEILING, and the binding constraint
    //   18.79 m  DataSF SF3775046 (the same neighbour), nearest vertex
    //   19.58 m  Overture be4a983e / b57e2786 (318 / 326 Brannan), nearest vertex
    //   20.78 m  DataSF SF3775100, nearest vertex
    //
    // Safe window (14.60, 17.29) m and 16 is its midpoint: 1.40 m clear of the
    // floor, 1.29 m clear of the ceiling. It is a narrow window and it is narrow
    // for a specific reason — Overture's three-way split of one surveyed
    // building. In practice Overture is gap-fill only (occupiedFraction > 0.25
    // skips it) and DataSF covers this parcel, so the floor is really 1.68 m;
    // 16 is chosen to be correct either way. Do NOT raise past 17 — at 17.29
    // this starts deleting 17-19 South Park, which has no GLB to replace it.
    //
    // No clearTrees: this is a paved party-wall block with no landcover inside
    // the footprint. The crape myrtles in front are street trees in the road
    // reserve, outside the exclusion's job.
    id: '21SouthPark',
    name: '21-29 South Park',
    lon: -122.3931063,
    lat: 37.7817676,
    height: 11.73,
    exclude: 16,
    // App yaw = 180 - the compass bearing the camera stands at. The two front
    // planes face 315.7 and 286.7 deg and every other side is a party wall, so
    // the only informative eye is out over the park: bearing 300 -> yaw 240.
    // That splits the two planes, so the bend reads as a bend and both ranks of
    // openings stay open. Standing square on either normal collapses the other
    // plane and the bend with it. Verified by render (the 592Third lesson).
    camera: { distance: 170, yaw: 240, pitch: 26 },
  },
  {
    // 522-524 Second Street, the 1923 brick warehouse on the Taber Place corner.
    // Third bespoke landmark on block 3775, with 358 and 370-400 Brannan.
    //
    // Exclusion sized against the REAL bake input (pipeline/data/
    // overture_buildings.geojsonseq), by nearest ring VERTEX, not centroid —
    // excluded() in buildings.mjs fires on either:
    //
    //    2.84 m  this building's own footprint (h=9, 7 verts), via CENTROID.
    //            Its own nearest vertex is 14.79 m out, so the centroid test is
    //            what does the work here — any radius over ~3 m drops it.
    //   14.78 m  nearest neighbour vertex (h=12.9) — a shared party-wall point
    //   18.12 m  two more neighbours (h=12, h=13) sharing this footprint's corners
    //   19.69 m  512 Second St (h=20) and its neighbour, across Taber Place
    //
    // Safe window is therefore (2.9, 14.78) m and no other footprint has a
    // centroid inside 21 m. 11 sits in that window with 8 m of margin below and
    // 3.8 m above. Do NOT raise past 14 — at 14.78 this starts deleting the
    // party-wall neighbour at 544 Second and leaving a hole in the street wall.
    // Taber Place gives free clearance on the northwest side; all the risk is
    // southeast and southwest, where the walls actually touch.
    id: '524Second',
    name: '524 Second Street',
    lon: -122.393433,
    lat: 37.7825731,
    height: 9.9,
    exclude: 11,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so yaw 180 stands
    // the camera due NORTH — the one bearing that shows the Second Street front
    // (45.6 deg) and the Taber Place flank (315.4 deg) together.
    camera: { distance: 200, yaw: 180, pitch: 26 },
  },
  {
    // 501 Second Street, the 1925 seven-storey cream office block on the Bryant
    // corner. The largest bespoke footprint in the SoMa set: 72.79 x 42.24 m,
    // 3,074 m2, a MEASURED 33.0 m parapet and a 37.7 m penthouse crest.
    //
    // Exclusion sized against the REAL bake input (pipeline/data/
    // overture_buildings.geojsonseq), by nearest ring VERTEX, not centroid —
    // excluded() in buildings.mjs fires on either:
    //
    //    7.09 m  this building's own footprint (h=33, 6 verts), via CENTROID.
    //            Its own nearest vertex is 21.27 m out, so as at 524 Second the
    //            centroid test is what does the work.
    //   38.54 m  nearest neighbour vertex (h=15) — the first thing at risk
    //   42.50 m and 48.91 m  the next two
    //
    // Safe window (7.1, 38.54) m, and no other footprint has a centroid inside
    // 48 m. 30 sits in that window with 23 m of margin below and 8.5 m above —
    // far more generous than 524 Second's (2.9, 14.78), because this building
    // stands free on three streets instead of sharing two party walls. Note 30
    // does NOT reach this footprint's own corners at 42.1 m; it does not need
    // to, and reaching them would delete the neighbour at 38.54 m.
    id: '501Second',
    name: '501 Second Street',
    lon: -122.3929683,
    lat: 37.7831785,
    height: 37.7,
    exclude: 30,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so yaw 270 stands
    // the camera due WEST — the bisector of the Second Street elevation
    // (225.4 deg) and the Bryant Street elevation (315.4 deg).
    camera: { distance: 420, yaw: 270, pitch: 26 },
  },
  {
    // 22-24 South Park, the Hotel Madrid: a 1915 residential hotel (built as the
    // Eimoto Hotel) run by Mission Housing since 1987, and the third building in
    // the South Park Scattered Sites rehabilitation with 102SouthPark and
    // 106SouthPark.
    //
    // This lon/lat is the surveyed parcel's AREA CENTROID and deliberately
    // differs from the manifest anchor (-122.3936099, 37.7823247), which is the
    // model's bbox centre 4.8 m away. The lot is a trapezoid, so those two points
    // are not the same, and only the area centroid works as an exclusion centre:
    // measured from the bbox centre the safe band is EMPTY, because 10 South
    // Park's Overture ring comes within 5.20 m while this building's own Overture
    // ring is still 5.23 m out. Nothing downstream cares — LANDMARKS lon/lat
    // drives only the camera pivot and the search result position.
    //
    // exclude: 4.5 is the middle of a (2.21, 6.90) m band measured against BOTH
    // bake inputs with excluded()'s real test (centroid OR any ring vertex).
    // Floor = this building's own Overture ring at 2.21 m, not its DataSF one at
    // 0.63: addBuilding() returns null on exclusion so markOccupied() never runs,
    // and a smaller radius lets the Overture gap-fill re-add the building on top
    // of the asset. Ceiling = 26-28 South Park's DataSF ring at 6.90 m.
    // Expect the re-bake to drop exactly two rings, both this building's.
    id: '22SouthPark',
    name: 'Hotel Madrid (22-24 South Park)',
    lon: -122.3936498,
    lat: 37.7822952,
    height: 14.22,
    exclude: 4.5,
    // camera.yaw is 180 - the compass bearing the camera stands at (the offset is
    // (sin yaw, ., cos yaw) and this project's +z is SOUTH). The street frontage
    // is a 31 deg arc whose chord normal is 159.4 deg, so yaw 21 stands the
    // camera south-south-east of the building, out over the oval, looking back at
    // the curved facade and the cornice.
    camera: { distance: 190, yaw: 21, pitch: 26 },
  },
  {
    // 26-28 South Park (51 Taber Place): a 1907 two-storey through-lot sliver,
    // 6.69 m of frontage against 30.13 m of depth, and the low notch between the
    // Hotel Madrid and 44-46 South Park.
    //
    // height 9.05 is the LiDAR MEDIAN deck (8.35 m) plus a conventional parapet,
    // NOT the 13.59 m LiDAR maximum: that maximum matches 44-46 South Park's own
    // roof-plane median (13.52 m) to 7 cm on a 7.65 m-wide raster footprint
    // dilated into both taller party walls. See artifacts/26-south-park/REPORT.md.
    //
    // exclude: 3.4 is the middle of a (2.20, 4.60) m band — the tightest in the
    // South Park set — measured against both bake inputs. Floor = this building's
    // own Overture ring; ceiling = 44-46 South Park's nearest DataSF vertex, with
    // only 1.2 m of margin, so re-check the drop list against origin/main's
    // registry after any merge that lands 46SouthPark.
    id: '26SouthPark',
    name: '26-28 South Park',
    lon: -122.3937438,
    lat: 37.7822369,
    height: 9.05,
    exclude: 3.4,
    // Front faces 135.2 deg, so yaw 45 stands the camera south-east, over the
    // oval. Closer and flatter than its neighbour: the recognition here is the
    // 4.5:1 slot proportion and the step against both neighbours, which a high
    // pitch flattens away.
    camera: { distance: 165, yaw: 45, pitch: 24 },
  },
  {
    // 35 South Park — Accel's San Francisco office. A 1920 industrial building
    // on the NE arc of the oval (block/lot 3775/102), wearing the grandest street
    // elevation on the park: five giant round-arched bays in pale ashlar under a
    // rope-enriched architrave, a lettered frieze and a tall blank parapet. A
    // 2020-23 ground-up renovation (permits 202008222419 and its 2023 roof-trellis
    // submittal) added a set-back penthouse and a clipped hedge running the whole
    // front parapet — the two things the app's downward camera reads first.
    //
    // height is the PENTHOUSE crest, and it is estimated: the DataSF LiDAR is a
    // 2010 product and predates the penthouse entirely (its max is 12.44 m). 13.4 m
    // is photogrammetric from two Jan 2025 Street View captures, +-0.7 m, the
    // largest error term being the penthouse's setback. The front parapet is
    // 10.4 m. See artifacts/35-south-park/REFERENCE.md section 2.
    //
    // excluded() drops a footprint when its centroid OR any ring vertex falls
    // inside the radius. Measured from this anchor against the actual bake input
    // (DataSF footprints primary, Overture/OSM gap-fill):
    //
    //    0.42 m  this building's own OSM ring (way 112759864), via CENTROID
    //    1.36 m  this building's own DataSF footprint (SF3775102), via centroid
    //   10.68 m  nearest neighbour VERTEX — 41-43 South Park (SF3775040), the
    //            party-wall Victorian on the SW. This is the binding constraint.
    //   12.87 m  the same neighbour via OSM (way 112759867)
    //   15.51 m  the rear neighbour (SF3775015)
    //   24.73 m  27 South Park (way 112759868), across the 7.34 m NE gap
    //
    // Safe window is therefore (1.4, 10.68) m and 6 sits in the middle of it with
    // 4.6 m of margin on each side — the most comfortable window in the South Park
    // set, unlike 135SouthPark's 1.5 m one. Do NOT raise past 10: at 10.68 this
    // starts deleting the party-wall Victorian, which has no GLB to replace it.
    //
    // No clearTrees: this is a building, and the oval's scatter is already handled
    // by 64SouthPark's 80 m zone.
    id: '35SouthPark',
    name: 'Accel (35 South Park)',
    lon: -122.3933378,
    lat: 37.7815714,
    height: 13.4,
    exclude: 6,
    // App yaw = 180 - the true bearing the camera stands at. The arcade faces
    // 315.9 deg (NW) across the street into the park, so the camera has to stand
    // to the NW: bearing 315 -> yaw 225, square onto the one elevation that
    // carries the design. Verified against the -aerial render, not derived on
    // paper (the 592Third lesson).
    camera: { distance: 130, yaw: 225, pitch: 24 },
  },
  {
    // 1911 Edwardian two-flat on the north-east rim of the South Park oval,
    // 7.3 m of frontage against 24 m of depth. Party walls on both sides, so
    // this is one of the tightest exclusion zones in the registry and the
    // radius is MEASURED against the committed bake input, not guessed.
    //
    // `excluded()` in pipeline/buildings.mjs drops a footprint when its
    // centroid OR any ring vertex falls inside the circle, and the bake reads
    // DataSF first then gap-fills from Overture. Both datasets trace this
    // building, so a correct radius drops TWO rings, not one. Measured from
    // this lon/lat against pipeline/data/buildings_datasf.geojson and
    // pipeline/data/overture_buildings.geojsonseq:
    //
    //    0.57 m  DataSF SF3775040 centroid   — ours, must go
    //    1.83 m  Overture 177 m2 centroid    — ours, must go
    //    3.73 m  DataSF SF3775039 vertex     — 45-49 South Park, must survive
    //    8.71 m  Overture 272 m2             — 45-49 South Park
    //   11.08 m  Overture 791 m2             — 35 South Park
    //   12.12 m  DataSF SF3775102            — 35 South Park
    //
    // Safe window (1.83, 3.73) m; 2.8 sits in it with 0.97 m of margin below
    // and 0.93 m above. That window is nearly five times wider than the one at
    // the manifest anchor (2.74, 3.16), which is why this lon/lat is offset
    // 1.50 m from it — these are independent fields, and app/src/assets.js
    // places the GLB from the MANIFEST anchor alone. The 1.5 m offset also
    // moves the search/camera target, which is negligible on a 7 m building
    // flown to from 150 m.
    //
    // No clearTrees: the street tree in front of this house is real and the
    // oval's furniture sits inside the park, outside the lot.
    id: '41SouthPark',
    name: '41-43 South Park',
    lon: -122.3934867,
    lat: 37.7815158,
    height: 10.6,
    exclude: 2.8,
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with +x
    // east and +z south, so camera bearing = 180 - yaw; the 315.22 deg facade
    // wants yaw 225, standing north-west out over the park, square onto the two
    // bays. 150 m suits a 10.6 m building (cf. 165-167 at 160 for 9.0 m,
    // 160 South Park at 155 for 9.4 m, 135 South Park at 150 for 8.5 m).
    camera: { distance: 150, yaw: 225, pitch: 26 },
  },
  {
    // 44-46 South Park, the 2008 four-level glass-fronted infill house on the
    // north-west rim of the oval. Twentieth South Park building in the manifest.
    // 46 is the ground-floor commercial unit, 44 the flats above.
    //
    // Exclusion sized against the REAL bake input, by nearest ring VERTEX as
    // well as centroid — excluded() in buildings.mjs fires on either, and the
    // bake reads buildings_datasf.geojson FIRST and gap-fills from
    // overture_buildings.geojsonseq. addBuilding() returns null on exclusion so
    // markOccupied() never runs, which means the Overture twin of an excluded
    // DataSF footprint is re-attempted and has to be caught by the same circle.
    // Measured from this anchor:
    //
    //    0.26 m  this building's DataSF footprint SF3775217, via its centroid
    //    1.42 m  this building's Overture/OSM way 124884347 (h=14), via its
    //            centroid -> the FLOOR: below this the procedural twin survives
    //    4.95 m  26-28 South Park, DataSF SF3775049 (h=8.35), nearest ring
    //            VERTEX -> the CEILING, and a vertex it SHARES with this
    //            building's ring (party wall)
    //    8.79 m  22-24 South Park rear wing, Overture (h=7.7), centroid
    //    9.26 m  54-58 South Park, DataSF SF3775219 (h=13.5), centroid
    //    9.36 m  54-58 South Park, Overture (h=14), centroid
    //   13.53 m  22-24 South Park, Overture (h=12), nearest vertex
    //   14.50 m  22-24 South Park, DataSF SF3775048, nearest vertex
    //
    // Safe window (1.42, 4.95) m. 3 sits with 1.58 m of margin below and 1.95 m
    // above. excluded() fires on BOTH rings, but the observable cell-count delta
    // is -1, not -2: before this entry existed the DataSF ring was added and
    // markOccupied() ran, so the Overture twin was already being rejected as a
    // duplicate. Now the DataSF ring is excluded, markOccupied() never runs, and
    // the twin is re-attempted — and caught by the same circle. Measured:
    // verify-rebake.mjs reports cell 23_13 moving 201 -> 200 and nothing else in
    // the city; anything other than -1 there means something is wrong.
    // Do NOT raise past 4.5: at 4.95 this starts deleting 26-28 South Park and
    // leaves a hole two doors up the street wall. No clearTrees — at 3 m it
    // clears nothing, which is right, because the street tree in front of the
    // south-west end belongs to the park's rim planting.
    id: '46SouthPark',
    name: '44-46 South Park',
    lon: -122.3938219,
    lat: 37.7821864,
    height: 16.15,
    exclude: 3,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so app yaw =
    // 180 - true bearing. This building's one public face looks 135.2 deg, so
    // yaw 45 stands the camera south-east over the park, looking north-west at
    // the glazed front. It is the only view of this building worth flying to.
    camera: { distance: 130, yaw: 45, pitch: 24 },
  },
  {
    // 54-58 South Park: a 2009 four-storey mixed-use infill on the north-west
    // rim of the oval, holding three condominium lots (3775/219 = 58, the
    // ground-floor commercial condo; /220 = 56; /221 = 54, the penthouse). It
    // replaced a two-storey office demolished in 2005 and was built as one half
    // of a pair with 44-46 South Park next door under the same permit set.
    // Nine and a half metres of frontage, thirty metres deep, party walls on
    // BOTH flanks. Height 16.9 m is the roof-office crest; the main parapet is
    // 13.6 m (see docs/asset-plans/58-south-park.md 2.1 and the height caveat
    // in artifacts/58-south-park/REFERENCE.md).
    //
    // Exclusion sized against BOTH files the bake actually reads
    // (pipeline/data/buildings_datasf.geojson and overture_buildings.geojsonseq,
    // 17 Aug 2026), remembering that excluded() fires on a footprint's CENTROID
    // or ANY ring vertex, whichever is closer:
    //
    //   ring                                    vertex   centroid   trigger
    //   this building, Overture 9c9ab1d7        13.31 m    1.31 m     1.31 m
    //   this building, DataSF SF3775219         14.13 m    2.26 m     2.26 m  <- the floor
    //   70 South Park, Overture 7c04d454        13.36 m    7.75 m     7.75 m  <- the ceiling
    //   44-46 South Park, DataSF SF3775217      14.03 m    9.33 m     9.33 m
    //   70 South Park, DataSF SF3775053         13.68 m   10.37 m    10.37 m
    //   44-46 South Park, Overture 71b35ab5     13.31 m   11.57 m    11.57 m
    //
    // TWO rings are this building — DataSF and Overture both trace it — and both
    // have to go, or the survivor bakes a procedural block straight through the
    // asset. So the safe window is (2.26, 7.75) and 5 sits dead centre with
    // 2.74 m below and 2.75 m above. Do NOT raise past 7.7: at 7.75 this starts
    // deleting 70 South Park and leaving a hole in a continuous street wall
    // (AGENTS rule 5).
    //
    // Note why the window is so much wider than 106 South Park's (2.1) despite
    // the same party-wall geometry: every ring here is caught by its CENTROID,
    // not by a vertex. The shared party-wall edges are 30 m long, so their
    // endpoints sit ~13-14 m from this anchor and the vertex test never fires
    // inside the useful range. Both flanks are exact party walls all the same —
    // the neighbours' parcels share these edges vertex-for-vertex.
    //
    // No clearTrees: the two mature street trees in front of this building are
    // real, they are what makes the January 2025 pano useless above the ground
    // floor, and at 5 m this radius clears no street furniture anyway.
    id: '58SouthPark',
    name: '54-58 South Park',
    lon: -122.3938881,
    lat: 37.7821223,
    height: 16.9,
    exclude: 5,
    // app/src/camera.js places the rig at (sin(yaw), sin(pitch), cos(yaw)) x
    // distance from the pivot, and this project's +z is SOUTH, so yaw 45 puts
    // the camera south-east of the building — over the oval, looking north-west
    // at the South Park front (135.2 deg), which is the only elevation of it
    // worth flying to. Same value as 106 South Park on the same rim.
    camera: { distance: 150, yaw: 45, pitch: 26 },
  },
  {
    // A 1906 post-earthquake flats building on the NORTH-WEST rim of the South
    // Park oval, party-walled to 70 South Park on the north-east and 84 on the
    // south-west. 6.90 x 29.70 m — more than four times deeper than it is wide.
    //
    // `height` is the MEASURED ROOF DECK (DataSF LiDAR median over 763 cells),
    // not the manifest's `targetHeightM` of 16.28. The manifest number
    // normalizes the asset's tallest geometry, which is the roof-stair
    // penthouse; this number is what a search or concierge card should say the
    // building is. Same deliberate split as `64SouthPark` (15.0 here against
    // 21.0415 in the manifest).
    //
    // MEASURED ON THE SIMPLIFIED RING. `addBuilding()` in buildings.mjs runs
    // `simplifyRing(ring, 0.6)` BEFORE it calls `excluded()`, and on this site
    // that matters in both directions: it pushes 84 South Park's nearest vertex
    // out from 3.64 m to 3.97 m and pulls this footprint's own OSM centroid in
    // from 1.92 m to 1.83 m. Distances from the anchor below, against the
    // simplified rings the gate actually sees:
    //
    //   0.18 m  this footprint's centroid (DataSF SF3775054) — always caught
    //   1.83 m  this footprint's centroid (OSM way/124884340) — the real FLOOR,
    //           because the Overture gap-fill re-adds it if the radius misses
    //   3.97 m  84 South Park nearest vertex (DataSF SF3775055) — the CEILING
    //   5.52 m  84 South Park nearest vertex (OSM way/113545687)
    //   7.20 m  70 South Park centroid (DataSF SF3775053)
    //   7.34 m  70 South Park centroid (OSM way/124884345)
    //
    // The bake reads DataSF first and gap-fills from Overture (OSM geometry),
    // so both rows bind. Safe window (1.83, 3.97); 2.9 sits dead centre with
    // 1.07 m either side. Do not raise past 3.5 without re-running audit.mjs
    // check 1.6 — beyond 3.97 it starts eating 84 South Park, which is a real
    // standing building.
    //
    // No `clearTrees`: the street trees in front of this building are real and
    // are in every photograph of it.
    id: '76SouthPark',
    name: '76-82 South Park',
    lon: -122.3940170,
    lat: 37.7820261,
    height: 13.08,
    exclude: 2.9,
    // camera.js sets position = pivot + distance * (sin yaw, sin pitch, cos yaw)
    // with +x east and +z SOUTH, so yaw 45 stands the camera south-east —
    // square onto the 135 deg South Park front, which is the only elevation of
    // this building worth flying to. 130 m rather than the ~90 m its height
    // suggests, because the building is 29.70 m long and needs the room.
    camera: { distance: 130, yaw: 45, pitch: 26 },
  },
  {
    // A 6.99 x 30.07 m sliver on the north-west rim of the South Park oval —
    // the thinnest lot in this set, thinner than 106SouthPark four doors along.
    // 1907, raised 2 -> 3 storeys by a 1992-94 vertical addition; the
    // bounding-box top is the roof-deck pergola at 13.20 m, not the 11.50 m
    // parapet. See docs/asset-plans/84-south-park.md 2.13.
    //
    // THE lon/lat BELOW IS NOT THE MANIFEST ANCHOR, deliberately. Placement uses
    // the DataSF parcel centroid (-122.3940683, 37.7819798); this circle is
    // centred 0.84 m away, on bearing 344 deg. The reason is that TWO rings have
    // to be dropped here — the DataSF footprint and the Overture/OSM trace of the
    // same building sit 2.7 m apart, because OSM traces the whole lot depth while
    // the LiDAR footprint stops at the rear wing's open terrace — while both party
    // walls have neighbour vertices under 4 m out. Measured with the metric
    // excluded() uses (centroid OR any ring vertex inside the circle):
    //
    //   registry point                own rings gone by   nearest neighbour   window
    //   manifest anchor (parcel)              2.00 m            3.43 m        1.43 m
    //   DataSF LiDAR area centroid            2.66 m            3.70 m        1.04 m
    //   OSM OBB centre                        2.67 m            3.27 m        0.60 m
    //   THIS POINT                            1.48 m            3.73 m        2.25 m
    //
    // Full trigger table from this point:
    //   1.47 m  this building, OSM way/113545687 (Overture proxy)  <- must go
    //   1.48 m  this building, DataSF SF3775055                    <- must go
    //   3.73 m  86-96 South Park  (SF3775116 / 201006.0022147)     <- must survive
    //   3.86 m  76-82 South Park  (SF3775054 / 201006.0026693)     <- must survive
    //   4.36 m  OSM way/113545685, untagged, on the 86-96 lot      <- must survive
    //   4.89 m  76-82 South Park, OSM way/124884340                <- must survive
    //
    // exclude: 2.6 sits in the middle of (1.48, 3.73) with 1.12 m of margin below
    // and 1.13 m above — the widest band available anywhere near this building and
    // more than double what the manifest anchor would give.
    //
    // The lot's own 16 m2 rear structure (201006.0168103) triggers at ~14 m and
    // therefore SURVIVES the bake, which is correct: it is a real outbuilding and
    // the asset models its own version of it. If QA shows a doubled rear volume,
    // the fix is to model it OUT of the GLB, not to widen this radius past 3.73
    // and delete a neighbour (AGENTS rule 5).
    //
    // No clearTrees: the large street tree in front of this building is real and
    // is in every photograph of it; at 2.6 m the radius clears no street furniture
    // in any case.
    id: '84SouthPark',
    name: '84 South Park',
    lon: -122.3940709,
    lat: 37.7819871,
    height: 13.2,
    exclude: 2.6,
    // app/src/camera.js places the rig at (sin(yaw), sin(pitch), cos(yaw)) x
    // distance from the pivot, and this project's +z is SOUTH, so yaw 45 puts the
    // camera south-east of the building — over the oval, looking north-west at the
    // street elevation, which is the only view of it worth flying to. Same
    // convention as 106SouthPark.
    camera: { distance: 150, yaw: 45, pitch: 26 },
  },
  {
    // Gran Oriente Filipino Masonic Temple, 1951 — the third building of the
    // Gran Oriente complex, after 106SouthPark. The anchor is the DataSF LiDAR
    // area centroid and NOT the OSM one: OSM way/71211338 traces this building
    // 6.6 m too deep at the rear (DataSF assigns that strip to 41-43 South
    // Park, and Bing z20 shows a tree in a yard there), so its centroid sits
    // 2.64 m too far north-east. That 2.64 m is the whole ballgame here.
    //
    // Measured from THIS point the exclusion window is (2.64, 7.07) m:
    //   this building, DataSF 201006.0108499   triggers at 0.05 m (centroid)
    //   this building, OSM/Overture trace      triggers at 2.64 m (centroid)
    //   45-49 South Park, DataSF 201006.0014671        7.07 m (ring vertex)
    //   41-43 South Park, DataSF 201006.0038546        7.10 m (ring vertex)
    //   the warehouse SE, DataSF 201006.0003676        7.83 m (ring vertex)
    // 4.8 leaves 2.16 m of margin below and 2.27 m above, and must drop TWO
    // footprints, not one — DataSF traces this building and so does Overture,
    // and an excluded DataSF ring never calls markOccupied(), so the Overture
    // gap-fill would re-add it.
    //
    // Measured from the OSM centroid instead the window collapses to
    // (2.60, 4.47), because OSM's own trace SHARES two ring vertices with
    // 41-43 South Park at 5.41 m. Moving the anchor onto the real footprint
    // centre was the fix, not a bigger radius.
    id: '95JackLondonAlley',
    name: 'Gran Oriente Filipino Masonic Temple (95 Jack London Alley)',
    lon: -122.393443,
    lat: 37.781346,
    height: 8.4,
    exclude: 4.8,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so the convention
    // that stands the camera in front of a facade of bearing B is yaw = 180-B.
    // The alley elevation faces 225.9 deg, giving yaw 314 — south-west of the
    // building, over Jack London Alley, looking north-east at the one doorway
    // this building exists for. 120 m is deliberately close: an 8.4 m building
    // whose entire content is a 2.9 m arch is a pink dot from 420.
    camera: { distance: 120, yaw: 314, pitch: 24 },
  },
  {
    id: '318Brannan',
    name: '318 Brannan Street',
    lon: -122.3927890,
    lat: 37.7816014,
    height: 8.6,
    exclude: 8,
    camera: { distance: 180, yaw: 15, pitch: 28 },
  },
  {
    // 334 Brannan Street, the 1929 "Sherman and Clay" building — a three-storey
    // reinforced-concrete loft on a 21.08 x 21.13 m square lot, four doors
    // northeast of 350 Brannan and a contributor to the South End Historic
    // District. Gold frieze, gilt pier caps, pink Deco panels on the entry tower.
    //
    // Exclusion sized against the REAL bake input (both passes:
    // pipeline/data/buildings_datasf.geojson AND overture_buildings.geojsonseq),
    // with the rule excluded() actually uses — centroid OR ANY ring vertex:
    //
    //   THIS BUILDING IS TRACED TWICE and both rings must go:
    //     0.49 m  Overture 879ad29f (h=12), by CENTROID
    //     2.04 m  DataSF SF3775101 (h=12.14), by CENTROID
    //   the neighbours, all reached by VERTEX, never by centroid:
    //    10.96 m  Overture b57e2786 (h=5.3) — the 326 Brannan garden structure,
    //             which SHARES the 10.96 m vertex with our own Overture ring, so
    //             this is a hard ceiling that no radius can climb past
    //    11.82 m  Overture 4a643109 (h=3.1)
    //    12.07 m  DataSF SF3775012 (326 Brannan, both of its volumes)
    //    13.40 m  DataSF SF3775015 (340 Brannan, h=14.82) — the party wall
    //
    //   exclude  2 m    -> drops 1  (WRONG: misses the DataSF ring, leaving a
    //                     12.14 m procedural block inside the GLB)
    //   exclude 3-10 m  -> drops 2  (correct: both rings of this building only)
    //   exclude 11 m    -> drops 3  (eats the 326 Brannan garden structure)
    //   exclude 13 m    -> drops 7  (eats both neighbours and a fourth lot)
    //
    // 6 m sits in the middle of the (2.04, 10.96) window. Do NOT raise it past
    // 10. Note that 6 m does not reach this footprint's own vertices at 12.07 m
    // and does not need to — the centroid test does all the work here.
    id: '334Brannan',
    name: '334 Brannan Street',
    lon: -122.3930344,
    lat: 37.7814147,
    height: 13.4,
    exclude: 6,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so yaw 90 stands the
    // camera due EAST — the bisector of the Brannan Street front (135.1 deg) and
    // the exposed northeast flank (46.1 deg), which is the pair the app's aerial
    // camera sees. Square-on from the southeast would show the blind party wall.
    camera: { distance: 210, yaw: 90, pitch: 26 },
  },
  {
    id: '340Brannan',
    name: '340 Brannan Street',
    lon: -122.3932324,
    lat: 37.7812786,
    height: 17.79,
    exclude: 8,
    camera: { distance: 240, yaw: 10, pitch: 26 },
  },
  {
    // Measured against the real bake input (DataSF ynuv-fyni footprints, plus
    // the Overture/OSM ring for the same building), by nearest ring VERTEX and
    // by centroid — excluded() in buildings.mjs fires on either:
    //
    //    0.62 m  this building's own DataSF footprint (SF3775039, 278.6 m2),
    //            via CENTROID. Its own nearest vertex is 4.76 m out.
    //    1.36 m  the SAME building's Overture/OSM ring (way/71211339), also via
    //            centroid — the two traces disagree by 1.4 m. In the event only
    //            ONE ring drops: Overture is gap-fill only, and DataSF already
    //            covers this footprint, so the second trace never reaches the
    //            bake. Measured, not assumed — verify-rebake reports cell 23_13
    //            going 201 -> 200 and no other cell moving at all.
    //    7.18 m  41-43 South Park (SF3775040) — a PARTY-WALL neighbour, and the
    //            first thing at risk
    //   15.67 m  the Gran Oriente Filipino Masonic Temple, 95 Jack London Alley
    //            (SF3775039's second footprint, same lot). It must SURVIVE: it
    //            is a separate 1951 building this asset does not contain, and
    //            there is no extraExclusions entry for it on purpose.
    //   21.48 m  101 South Park
    //
    // Safe window (1.4, 7.18) m. 3 sits in it with 1.6 m of margin below and
    // 4.2 m above, and matches the rest of this block — 165SouthPark uses 1.3,
    // 160SouthPark 1.2, 132SouthPark 2, 106SouthPark 2.1, 101SouthPark 4. On a
    // party-wall site the radius must NOT reach this footprint's own far
    // corners (up to 15.4 m); reaching them would delete both neighbours.
    id: '49SouthPark',
    name: 'Gran Oriente Filipino Residence (45-49 South Park)',
    lon: -122.3935929,
    lat: 37.7814646,
    height: 13.0,
    exclude: 3,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so camera bearing =
    // 180 - yaw and yaw 270 stands the eye due WEST — the bisector of the South
    // Park front (315.8 deg) and the Jack London Alley flank (225.8 deg). Both
    // elevations are hero elevations here and the rounded corner turret joins
    // them, so the corner is the only view worth flying to. 165 m suits a 13 m
    // building (cf. 106SouthPark at 150 for 11.58 m, 181SouthPark at 190 for
    // 16.5 m). No `key`: at 13 m this is texture in the block, not a
    // destination.
    camera: { distance: 165, yaw: 270, pitch: 26 },
  },
  {
    // 49 Zoe Street — a 16-unit artist live/work loft of 1996-97, re-clad in
    // 2011-13, on the north-east side of a 25 ft SoMa alley between Bryant and
    // Brannan. Height is the DataSF LiDAR maximum 16.99 m, attributed to the
    // stair/elevator penthouse the aerial shows at the south-east end; the roof
    // plane itself is 14.42 m (median over 2,268 cells, sd 1.13 m — one flat
    // plane, no second level).
    //
    // Exclusion measured against the REAL bake inputs, both of them, with the
    // metric `excluded()` actually uses (ring CENTROID or ANY ring VERTEX
    // inside r, distance taken from THIS anchor):
    //
    //                                        nearest vertex   centroid   gate
    //   SF3776128        this building            14.13         0.11     0.11
    //   Overture twin    this building            15.94         5.37     5.37
    //   SF3776144        33-35 Zoe, PARTY WALL    14.28        21.87    14.28
    //   SF3776144        33-35 Zoe, second ring   14.29        19.37    14.29
    //   Overture         (33-35 Zoe)              14.39        26.52    14.39
    //   SF3776456        Ritch St, rear           14.92        24.17    14.92
    //   SF3776105        Ritch St, rear           15.51        30.26    15.51
    //
    // So the band is (5.37, 14.28] — 8.9 m wide, unusually comfortable for a
    // party-wall site. The floor is this building's own OVERTURE centroid, not
    // its DataSF one: an excluded DataSF ring never calls markOccupied(), so
    // the Overture gap-fill would re-add the building on top of the asset.
    // Shipping 9.5, near the middle, with 4.1 m of margin below and 4.8 m above.
    //
    // Note for anyone reading the plan's 2.13: that table listed each
    // neighbour's nearest vertex to THIS FOOTPRINT (33-35 Zoe touches at 0.00 m
    // across the party wall) and read it as the ceiling. It is not — the gate is
    // measured from the ANCHOR, and the party wall's nearest vertex to the
    // anchor is 14.28 m. Measuring is what turned an apparently impossible site
    // into an 8.9 m window.
    id: '49Zoe',
    name: '49 Zoe Street',
    lon: -122.3960338,
    lat: 37.7800764,
    height: 17.0,
    exclude: 9.5,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so camera bearing =
    // 180 - yaw. The Zoe elevation faces 225.4 deg and the parking-lot flank
    // 135.4; yaw 338 stands the eye south-south-west, square enough to the
    // striped Zoe facade to read its rhythm while the blank south-east flank
    // rakes away. 180 m suits a 17 m building (cf. 181SouthPark at 190 for
    // 16.5 m, 49SouthPark at 165 for 13.0 m). No `key`: this is fabric, not a
    // destination.
    camera: { distance: 180, yaw: 338, pitch: 28 },
  },
  {
    // 2014, five storeys, nineteen units over a ground-floor restaurant and
    // garage — the newest and tallest building on this face of Ritch Street by
    // eight metres. The bounding-box top is the roof stair/elevator penthouse at
    // 18.76 m (DataSF LiDAR maximum), NOT the 15.87 m parapet; see
    // docs/asset-plans/246-ritch.md 2.15 risk 1 and artifacts/246-ritch/REPORT.md.
    //
    // The address is a condominium: block 3776 lots 456-475 all share ONE parcel
    // polygon, and lot 456 also carries 240 Ritch (the ground-floor commercial
    // space). That is this building, not a neighbour — only one asset per parcel
    // can own the exclusion.
    //
    // Exclusion window measured from THIS point with the metric excluded() uses
    // (area centroid OR any ring vertex), against BOTH bake inputs, with the
    // bake's own simplifyRing(0.6) applied first:
    //
    //    0.01 m  this building, Overture 0e69af6c (the OSM trace, 379 m2)  <- must go
    //    1.69 m  this building, DataSF SF3776456 (394 m2)                  <- must go
    //    8.89 m  248-250 Ritch, Overture d280b71a (101 m2)                 <- must survive
    //   11.10 m  248-250 Ritch, DataSF SF3776105 (167 m2)                  <- must survive
    //   12.71 m  230/236 Ritch, DataSF SF3776144 (484 m2)                  <- must survive
    //   14.03 m  230/236 Ritch, Overture 2259b5ef (472 m2)                 <- must survive
    //
    // Safe band (1.69, 8.89) — 7.2 m wide, unusually generous for a party-wall
    // lot. 5.3 sits dead centre with 3.6 m of margin either side. Both of this
    // building's rings go by their CENTROIDS, so do not reason "the radius has to
    // cover the building": the footprint reaches 13.98 m from the anchor and that
    // is fine. Do not raise past 7 without re-running the measurement.
    //
    // No clearTrees: at 5.3 m the circle is entirely inside the building, and the
    // three street trees in front are real — the project was required to plant
    // them, and they are in every photograph of it.
    id: '246Ritch',
    name: '246 Ritch Street',
    lon: -122.3958481,
    lat: 37.7802253,
    height: 18.76,
    exclude: 5.3,
    // camera.js places the rig at (sin yaw, sin pitch, cos yaw) x distance from
    // the pivot and this project's +z is SOUTH, so yaw 135 stands the camera
    // north-east of the building — square onto the 45 deg Ritch Street front,
    // which is the only designed elevation. 130 m rather than the ~90 m its
    // height suggests, because Ritch is a 13 m alley and a closer rig clips into
    // the neighbours.
    camera: { distance: 130, yaw: 135, pitch: 26 },
  },
  {
    // 1915 two-flat on Ritch Street, the alley between Bryant and Brannan.
    // Case B: no procedural builder, so this entry exists only to carve the
    // baked footprints out from under the asset.
    //
    // `lon`/`lat` are NOT the manifest anchor. The manifest anchor
    // (-122.3956322, 37.7801278) is the model's XY bbox centre, pushed 0.53 m
    // north-east by the bay, the cornice and the stoop, which all project
    // toward the street. This point is the design footprint's centre, 0.09 m
    // from the DataSF footprint's own area centroid, and it is where the
    // exclusion window below was measured.
    //
    // `exclude` is the whole difficulty here and the window is 1.87 m wide.
    // excluded() in pipeline/buildings.mjs drops a footprint when its centroid
    // OR any ring vertex falls inside the circle. Measured from this point
    // against the real bake input, each ring first simplified at the bake's own
    // 0.6 m tolerance:
    //
    //    0.09 m  this building, DataSF 201006.0125003 (104 m2), via centroid
    //    1.95 m  this building, Overture — the OSM way 147508935 (100 m2)
    //    3.82 m  248-250 Ritch, DataSF 201006.0040021 (167 m2), nearest vertex
    //    5.08 m  248-250 Ritch, Overture (101 m2), nearest vertex
    //
    // So r must exceed 1.95 (both of OUR rings have to go — DataSF and Overture
    // each trace this building, 1.9 m apart, and a radius that clears only the
    // DataSF one leaves the Overture gap-fill standing on top of the asset) and
    // stay under 3.82 (or the party-wall neighbour goes with it). 2.9 sits
    // 0.95 m above the floor and 0.92 m below the ceiling.
    //
    // No clearTrees: at 2.9 m the circle is inside the building's own footprint,
    // there is no street tree in front of 252-254, and the surface parking lot
    // next door has no furniture to clear.
    id: '254Ritch',
    name: '252-254 Ritch Street',
    lon: -122.3956361,
    lat: 37.7801244,
    height: 8.8,
    exclude: 2.9,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so camera bearing =
    // 180 - yaw. The street front faces 45.05 deg, so yaw 135 stands the eye to
    // the north-east, out over Ritch Street, looking back at the only two
    // designed elevations — the bay-and-entry front and the exposed south-east
    // flank, which reads in three-quarter from there. 120 m suits an 8.8 m
    // building (cf. 49SouthPark at 165 for 13.0 m). No `key`: this is texture
    // in the block, not a destination.
    camera: { distance: 120, yaw: 135, pitch: 26 },
  },
  {
    // 248-250 Ritch Street, a 1915 wood-frame two-flat on a 25 x 75 ft alley lot
    // and the last pre-1920 domestic fabric on this face of Ritch. Two storeys
    // against the five of 246 Ritch immediately north-west, which is the whole
    // point of the asset - the height here is the story and it is not rounded up.
    //
    // THE REGISTRY POINT IS NOT THE MANIFEST ANCHOR, deliberately. The manifest
    // anchor -122.3956749, 37.7801751 is the model's bbox centre, which is where
    // the GLB has to sit. Measured from THAT point the exclusion window is only
    // (1.95, 2.88) m - 0.93 m wide - because the Bing-traced OSM ring of this
    // building sits ~2.5 m north-west of the survey while 252-254's equally
    // offset OSM ring pushes back from the other side. Moving the circle's
    // centre 5.4 m south-west, to the point below (still inside the house, on
    // the north-west flank 8.9 m back), opens the window to (0.92, 5.04) m.
    //
    // Measured against the REAL bake input, on the SIMPLIFIED rings - the
    // exclusion test runs after simplifyRing(ring, 0.6), and measuring on the
    // raw rings gives a window less than half as wide because 0.6 m of
    // simplification deletes exactly the small jogs that sit closest to this lot:
    //
    //   this building, DataSF SF3776105          0.91 m  vertex   <- the FLOOR
    //   this building, Overture/OSM w147508934   0.92 m  vertex
    //   252-254 Ritch, Overture/OSM w147508935   5.04 m  vertex   <- the CEILING
    //   252-254 Ritch, DataSF SF3776106          6.07 m  vertex
    //   246 Ritch,     Overture/OSM w1174904714  7.33 m  vertex
    //   246 Ritch,     DataSF SF3776456          7.83 m  vertex
    //
    // exclude 3 leaves 2.08 m of margin below and 2.04 m above. A correct
    // exclusion drops exactly TWO rings, this footprint and its Overture twin;
    // one means the gap-fill re-added the building, three or more means the
    // circle has eaten 252-254 and left a hole in the alley wall. Never above
    // 4.5, and treat a count of two as necessary but not sufficient - confirm
    // from the tile which rings went, not how many.
    id: '248Ritch',
    name: '248-250 Ritch Street',
    lon: -122.3957213,
    lat: 37.7801827,
    height: 8.6,
    exclude: 3,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so camera bearing =
    // 180 - yaw. This building has exactly ONE public elevation, looking
    // 45.05 deg, so yaw 135 stands the eye on Ritch Street north-east of the
    // pivot, square onto it. 560Third arrived at the same value by render for a
    // 44.1 deg elevation two blocks away. 120 m suits an 8.6 m building (cf.
    // 370Brannan 150 at 7.63 m, 550Third 190 at 11 m). No `key`: at 8.6 m this
    // is texture in the alley, not a destination.
    camera: { distance: 120, yaw: 135, pitch: 28 },
  },
  // 424 Brannan Street — a 2,026 m2 surface parking lot, and the ONLY entry in
  // this registry with no `exclude`. That is measured, not an oversight.
  //
  // Every other landmark here needs a radius to delete the procedural building
  // standing where its GLB goes. This site has no procedural building: DataSF's
  // footprint layer returns ZERO records for parcel 3776455, the assessor
  // carries it as class V vacant with $0 of improvements, and a scan of the
  // committed tiles (23_13 plus 22_13, 23_14, 24_13) finds no footprint whose
  // centroid lands inside the parcel. So the whole risk here runs the other
  // way: any radius large enough to matter eats a neighbour.
  //
  // Measured against the real bake inputs from this anchor — nearest ring
  // VERTEX or centroid, which is what excluded() fires on:
  //
  //   10.27 m  Overture b9c9690e-43b   <- the first thing at risk
  //   10.63 m  DataSF SF3776151 (426 Brannan, the Brickhouse block)
  //   19.58 m  Overture b9c91621-afe
  //   21.27 m  DataSF SF3776015 (434 Brannan)
  //   25.18 m  DataSF SF3776106
  //
  // Footprints with a centroid inside the parcel: DataSF 0, Overture 0. So the
  // safe band is (0, 10.27) and EVERY radius in it drops exactly nothing —
  // there is no value of `exclude` that does useful work, and omitting the key
  // is what exclusionZones() wants (it skips a falsy `exclude`). The buildings
  // and toy tiers are therefore bit-identical across this landmark's re-bake;
  // only the context tier changes, to give the lot a pick box and a search row.
  // Do not "fix" this by adding a radius: 11 m, the value 400 Brannan uses
  // 60 m away, would delete the Brickhouse.
  {
    id: '424Brannan',
    name: '424 Brannan Street Parking',
    lon: -122.3954857,
    lat: 37.7798744,
    height: 8.5649,
    // The eye stands over Brannan (bearing 135 = 180 - yaw), which is the only
    // angle from which the 15.8 m neck, the gate and the sign all read at once;
    // straight down the Ritch fence foreshortens 68 m of lot into a line. 260 m
    // suits an 88 m site (cf. 400Brannan at 170 for 24 m).
    camera: { distance: 260, yaw: 45, pitch: 30 },
  },
  {
    // 226 Ritch Street (1994-96) — eight live/work lofts on the south-west side
    // of Ritch, the alley between Bryant and Brannan. Sage-green stucco over a
    // sand-tiled garage band, a galvanised fire escape up the front, and a roof
    // deck. Three storeys, but the lofts have 15-foot ceilings, which is why the
    // parapet is 16.0 m — as tall as a five-storey building on the same block.
    //
    // `height` is the CREST (the stair bulkhead), not the parapet, because the
    // manifest scales the GLB by targetHeightM / measuredHeight and the model's
    // bbox top is the bulkhead. The parapet itself lands at 16.0 m, which is
    // where OSM's height=16 and the DataSF LiDAR median (15.90 m) both put it.
    // The 18.1 m crest is the LiDAR hgt_max (18.14 m) and is corroborated by
    // hgt_majority 17.63 m — a REPEATED value 1.7 m above a roof plane whose
    // mean and median agree to 0.1 m, which a single spurious return cannot
    // produce. See artifacts/226-ritch/REPORT.md §2 for what is still unproven.
    //
    // exclude: 5 is MEASURED, not guessed, against both bake inputs from this
    // anchor. `excluded()` in pipeline/buildings.mjs drops a footprint whose
    // ring centroid OR any ring vertex is inside the radius:
    //
    //   0.85 m  this footprint's centroid, DataSF SF3776120
    //   0.68 m  this footprint's centroid, OSM 148217483 (Overture proxy)
    //   9.75 m  the CENTROID of 218 Ritch (OSM 148217499) — the binding limit
    //  10.23 m  the nearest vertex of 218 Ritch, DataSF SF3776144
    //
    // So the window that drops exactly this footprint is 0.9 < r < 9.75 and it
    // is unusually wide for a party-wall row: 218 Ritch is a small 144 m2
    // building whose centroid, not a shared party-wall vertex, sets the ceiling.
    // 5 sits in the middle with ~4.1 m of margin below and ~4.75 m above. The
    // exclusion fires on this footprint's CENTROID — its own nearest vertex is
    // 6.1 m out — so do not shrink r below 1 expecting the vertices to catch it.
    //
    // App yaw = 180 - true bearing (camera.js `apply()`: the offset is
    // (sin yaw, ., cos yaw) with +z south). The Ritch Street front faces 45.6
    // deg, so yaw 134 stands the camera north-east, out over the alley, looking
    // back at the one designed elevation — the other three faces are two party
    // walls and a rear that the 1998 permits clad in vinyl siding. 180 m suits
    // an 18.1 m building (cf. 188SouthPark 190 at 15.93 m, 181SouthPark 190 at
    // 16.5 m). No `key`: this is texture in the block, not a destination.
    id: '226Ritch',
    name: '226 Ritch Street',
    lon: -122.3960899,
    lat: 37.7804376,
    height: 18.1,
    exclude: 5,
    camera: { distance: 180, yaw: 134, pitch: 28 },
  },
  // 414 Brannan (Epic Church, 1924) — the next lot southwest, on the Ritch
  // Street corner. ONE building, but the LiDAR footprint layer splits it into
  // THREE ~180 m2 strips under `mblr = SF3776011`, one per structural bay, and
  // all three have to go or the GLB shares its site with a procedural triplet.
  // Overture carries three more rings over the same lot. Measured against the
  // real bake input, both sources:
  //
  //   exclude  6-8 m  -> drops 2  (the middle bay + one Overture ring)
  //   exclude 10 m    -> drops 4  (two bays)
  //   exclude 11-13 m -> drops 6  (correct: all three bays + all three Overture
  //                                rings, zero collateral)
  //   exclude 14 m    -> drops 8  (eats 566-586 Third, SF3776008, vertex 13.73 m)
  //   exclude 16 m    -> drops 10 (eats 400 Brannan above, SF3776114, vertex 15.78 m)
  //
  // 12 m is the middle of the band. Note the binding limit at the BOTTOM is the
  // southwest bay's CENTROID at 10.71 m, not any vertex — this lot's own corners
  // are 16.4 m out and the radius never has to reach them.
  //
  // camera.yaw = 180 - eye bearing. This is a corner site with two finished
  // elevations, Brannan facing SE 135.2 deg and Ritch facing SW 225.2 deg; their
  // bisector is 180.2, so the eye goes due south and yaw is 0.
  {
    id: '414Brannan',
    name: '414 Brannan Street (Epic Church)',
    lon: -122.3948685,
    lat: 37.7799308,
    height: 14,
    exclude: 12,
    camera: { distance: 200, yaw: 0, pitch: 28 },
  },
  {
    // One South Park: the 1919-20 concrete tobacco warehouse that closes the
    // EAST end of the oval, converted 2004-07 by LDP Architecture into 35 lofts
    // with two set-back storeys added on the roof. At 1,570 m2 it is the
    // largest building on the oval by a factor of two, which is what makes its
    // exclusion different from every other entry on this block: those are
    // party-wall teeth whose radius must stay small enough not to reach their
    // own far corners, and this one is a whole corner block whose own footprints
    // are dropped by their CENTROIDS long before any radius could reach its
    // 28 m-distant vertices.
    //
    // excluded() in buildings.mjs drops a footprint when its centroid OR any
    // ring vertex falls inside the radius. Measured from THIS anchor against the
    // real committed bake inputs (pipeline/data/buildings_datasf.geojson and
    // overture_buildings.geojsonseq), after projection and simplifyRing(0.6):
    //
    //    0.69 m  own Overture footprint (h 18), via CENTROID
    //    3.90 m  own DataSF footprint SF3775181 (h_med 17.77), via CENTROID
    //            -> the FLOOR. Above 3.90 both of this building's own
    //               footprints are gone; their nearest VERTICES are 16.98 m and
    //               12.37 m out and are irrelevant here.
    //   18.20 m  17-19 South Park, DataSF SF3775046 (h_med 6.60), via CENTROID
    //            -> the CEILING, and the binding constraint. A real standing
    //               1934 building with no GLB; it must survive (AGENTS rules 3
    //               and 5). Its nearest vertex is 22.58 m out, so reading this
    //               neighbour off vertices alone would overstate the window by
    //               4.4 m.
    //   20.44 m  the same neighbour in Overture (h 6.7), via centroid
    //   26.52 m  300 Brannan, DataSF SF3775008 (h_med 20.84), nearest vertex
    //   27.84 m  21-29 South Park, DataSF SF3775042, nearest vertex - already
    //            dropped by 21SouthPark's own exclude: 16
    //
    // Safe window (3.90, 18.20) m. 11 sits almost exactly in the middle with
    // 7.10 m of margin below and 7.20 m above, both an order of magnitude
    // larger than the bake's 0.6 m SIMPLIFY_TOLERANCE. No Overture polygon
    // other than this building's own overlaps the footprint, so there is
    // nothing for the gap-fill to re-add into the area markOccupied() no longer
    // covers.
    //
    // No clearTrees: the street trees on both frontages are real, they are in
    // every photograph of this building, and they stand in the road reserve
    // outside the building line - at 11 m the radius does not reach the kerb.
    // See docs/asset-plans/1-south-park.md 2.13 and
    // artifacts/1-south-park/REPORT.md.
    id: '1SouthPark',
    name: 'One South Park (1 South Park)',
    lon: -122.3928634,
    lat: 37.782048,
    height: 20.2,
    exclude: 11,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so camera bearing =
    // 180 - yaw and yaw 180 stands the eye due NORTH - the bisector of the
    // Second Street elevation (45.3 deg) and the South Park elevation
    // (315.0 deg). Both are hero elevations, the re-entrant step is on the
    // Second Street run, and the roof - which is half this building's design -
    // only reads from above the corner they meet at. 240 m suits a 59 m-wide
    // 20 m block (cf. 300Brannan at 240 for 25.2 m, 49SouthPark at 165 for
    // 13 m). No `key`: keys 0-9 are taken.
    camera: { distance: 240, yaw: 180, pitch: 28 },
  },
  {
    // 501 Third Street, the 1920 unreinforced-masonry industrial loft on the
    // EAST corner of 3rd and Bryant. 23.6 x 25.05 m rhombus on the 45 deg SoMa
    // grid, 592 m2, parapet 14.0 m and a rooftop bulkhead crest at 16.4 m (OSM
    // height=14 and LiDAR hgt_median 13.73 / hgt_max 16.42 agreeing).
    //
    // Exclusion sized against the REAL bake inputs (pipeline/data/
    // buildings_datasf.geojson AND overture_buildings.geojsonseq), by
    // min(nearest ring VERTEX, centroid) -- excluded() in buildings.mjs fires
    // on either:
    //
    //    3.43 m  this building's own Overture ring (h=14)   <- floor
    //    5.70 m  this building's own DataSF ring (SF3775073) <- floor, both go
    //   16.23 m  this footprint's own nearest vertex
    //   16.31 m  DataSF SF3775075 (h=14.90), the NE party neighbour <- ceiling
    //   17.17 m  Overture 0f2baf8a (h=11), that neighbour's twin
    //   19.55 m  DataSF SF3775072 (h=13.53), across Taber Place
    //
    // Safe window (5.70, 16.23) m, 10.5 m wide; 11 is its middle, so the centre
    // needs no offset from the manifest anchor. The asset plan's original
    // suggestion of ~20 was reasoned from the half-diagonal rather than
    // measured and would delete three neighbours. Note 11 does NOT reach this
    // footprint's own corners at 17.3 m; it does not need to, and reaching them
    // would delete SF3775075, which shares a party-wall survey vertex sitting
    // 0.147 m inside this footprint -- inside a wall thickness.
    id: '501Third',
    name: '501 Third Street',
    lon: -122.3954601,
    lat: 37.7813246,
    height: 16.4,
    exclude: 11,
    // Camera offset is (sin yaw, ., cos yaw) with +z south, so yaw 270 stands
    // the camera due WEST -- the bisector of the 3rd Street front (225.4 deg)
    // and the Bryant Street elevation (315.6 deg). Both are hero elevations on
    // this corner. 190 m suits a 16.4 m building (cf. 49SouthPark at 165 for
    // 13.0 m, 106SouthPark at 150 for 11.58 m). No `key`: at 16 m this is
    // texture in the block, not a destination.
    camera: { distance: 190, yaw: 270, pitch: 26 },
  },
  {
    // The South Park Lofts, 1993, Ramon Zambrano: ten live/work loft
    // condominiums on one 585 m2 through-lot running from South Park at the
    // south-east to Taber Place at the north-west. The lot carries TWO baked
    // footprints — the front block 262 m2 and the rear block 181 m2 — with a
    // ~142 m2 courtyard between them, and the anchor sits at the courtyard's
    // edge because that is where the GLB's bounding-box centre lands. This is
    // the 132SouthPark case: no single radius works, so there is one zone per
    // structure plus a guard at the anchor.
    //
    // height is the roof stair bulkhead (LiDAR max). The parapet crest is
    // 13.10 m, photogrammetric from Street View pano aFRDCNG9w0lcHJ9ngJI8LQ and
    // flat to +-0.06 m over a 41% range change; the roof deck is 12.27 m (LiDAR
    // median). See artifacts/10-south-park/REFERENCE.md section 3 for why the
    // maximum is believed here — briefly, both neighbours are TALLER, so
    // party-wall bleed could only pull it down, and the rear block reports the
    // same 2.4 m step against different neighbours.
    //
    // excluded() drops a footprint whose ring CENTROID or any vertex is inside
    // a zone. Measured from each candidate centre against the rings the bake
    // actually reads — DataSF ynuv-fyni AND the Overture gap-fill, both
    // extracted from pipeline/data/:
    //
    //   from the anchor:        1.35 m  own front block, nearest vertex
    //                           5.21 m  2 South Park (Overture) vertex  <- ceiling
    //                           5.90 m  own rear block, nearest vertex
    //   from the front zone:    1.24 m  own front block, DataSF ring CENTROID
    //                           1.48 m  own front block, Overture ring CENTROID
    //                           8.94 m  22-24 South Park (DataSF) vertex <- ceiling
    //   from the rear zone:     2.38 m  own rear block, DataSF ring CENTROID
    //                           2.43 m  own rear block, Overture ring CENTROID
    //                           7.09 m  22-24 South Park (Overture) vertex <- ceiling
    //
    // So each block is dropped by its own ring CENTROID and no radius ever
    // reaches this lot's far corners (14.7 m front, 7.3 m rear) — reaching them
    // would delete 22-24 South Park (14.22 m) or 2 South Park (17.72 m), neither
    // of which has a GLB to replace it, and both failures are silent. Margins
    // 3.5/3.9 m on the front zone and 2.1/2.6 m on the rear.
    //
    // The 2 m guard at the anchor happens to drop the front block by vertex, but
    // its real job is 132SouthPark's: stopping the Overture gap-fill re-filling a
    // lot that markOccupied() no longer sees as occupied once the DataSF
    // footprints are excluded. A whole-lot Overture polygon would centre within
    // about a metre of the anchor and sail past both other zones. Do NOT raise
    // it — 2 South Park's Overture vertex is 5.21 m out.
    //
    // Both blocks are traced twice, by DataSF and by Overture, so a correct
    // exclusion drops FOUR rings here, not two. See
    // docs/asset-plans/10-south-park.md 2.13.
    id: '10SouthPark',
    name: '10 South Park (South Park Lofts)',
    lon: -122.3935162,
    lat: 37.7823704,
    height: 14.67,
    exclude: 2,
    extraExclusions: [
      { lon: -122.3934359, lat: 37.7823083, r: 5 },   // front block, on South Park
      { lon: -122.3936335, lat: 37.7824581, r: 4.5 }, // rear block, on Taber Place
    ],
    // Camera bearing = 180 - yaw (camera.js apply(): the offset is
    // (sin yaw, ., cos yaw) and +z is south), so yaw 30 stands the camera at
    // bearing 150 = SSE — square onto the bowed south-west two-thirds of the
    // front (normal 179.7 deg) and still oblique enough to read the straight
    // north-east third (135.2 deg). Pitch 30 rather than this block's usual 26
    // so the courtyard between the two blocks clears the front parapet; it is
    // half of what this asset is. 200 m suits a 42 m-deep lot. No `key`: at
    // 14.7 m this is texture in the block, not a destination.
    camera: { distance: 200, yaw: 30, pitch: 30 },
  },
  {
    // 521-527 Third Street: the 1914 three-storey brick apartment-over-store
    // block on the east corner of 3rd and Taber Place (Neill's Grocery &
    // Liquor). The committed bake gives this footprint a 12.9 m block (base
    // 5.4, top 18.3) against the asset's 11.40 m parapet, so without the
    // exclusion the GLB is invisible inside a taller procedural building.
    //
    // Exclusion window, measured both ways from this anchor:
    //
    //   against app/public/tiles/buildings/23_13.bin (ring 98, what excluded()
    //   consumes today)     own centroid 0.18 m, own nearest vertex 8.60 m,
    //                       nearest NEIGHBOUR vertex 18.39 m (SF3775073,
    //                       501 Third across Taber Place)
    //   against the raw DataSF LiDAR polygons (what a re-bake consumes)
    //                       own polygon centroid 1.91 m, nearest NEIGHBOUR
    //                       vertex 8.60 m — and that neighbour is 549 Third
    //                       (SF3775125), which SHARES the party-wall vertex.
    //
    // excluded() drops a ring on centroid OR any vertex, so the window that
    // drops exactly this building is 1.91 m < r < 8.60 m. 5 sits in the middle
    // with 3.1 m of margin below and 3.6 m above. It fires on the CENTROID
    // test — do not shrink it below 2 m expecting the vertices to catch it, and
    // do not push it past 8.6 m or it deletes 549 Third.
    //
    // Note 549 Third is currently ABSENT from the committed bake even though
    // DataSF carries it (565 m2, 13.03 m, 24 m to the south-east). That is a
    // pre-existing gap in the procedural city, not something this exclusion
    // causes, and the radius is NOT widened to tidy it.
    //
    // Camera: bearing = 180 - yaw, so yaw 270 stands the eye due WEST — the
    // bisector of the 3rd Street front (normal 225.1 deg) and the Taber Place
    // flank (normal 315.1 deg). Those are the two designed elevations and the
    // corner between them is the whole point of the building. 200 m suits an
    // 11.4 m building (cf. 550Third 190 at 11 m, 592Third 200 at 8.2 m). No
    // `key`: at 11.4 m this is block texture, not a destination.
    id: '521Third',
    name: '521 Third Street',
    lon: -122.3952384,
    lat: 37.7811509,
    height: 11.4,
    exclude: 5,
    camera: { distance: 200, yaw: 270, pitch: 28 },
  },
  {
    // 164 South Park — a 1907 single-storey brick warehouse at the west tip of
    // the oval, wearing a 2024-25 Stanley Saitowitz | Natoma Architects front:
    // large-format red panels in stretcher bond, one black ribbon window that
    // tracks the shift around the oval and drops to become a glazed entry
    // recess, and a slender canopy over the door. Twitter (2006-2008) and
    // Instagram (2010) were both founded in this room; the concrete doormat at
    // that entry says so.
    //
    // HEIGHT NOTE — this is the one entry on this oval that REFUSES the LiDAR
    // maximum, and it is deliberate. DataSF `SF3775069` reports hgt_max 9.25 m,
    // but over 1,715 cells the distribution is median 5.44, modal 4.61, mean
    // 5.53, sd 0.84 m. A two-mass building (156 South Park's front bar over its
    // rear shed) spreads much wider than that; 0.84 m cannot contain a 4 m step.
    // The assessor records ONE storey on both parcels (068 and 069 are both
    // addressed 164), the aerial shows an unbroken flat membrane roof, and the
    // two-storey neighbours at 160 and 166 visibly overtop this building. The
    // 9.25 m is unexplained — the record's peak_1st_m is 16.53 m, a tree, and
    // there is a large tree overhanging the north-west end of this roof. Height
    // is the MEDIAN, 5.4 m, which also matches the photogrammetry: the new
    // street screen measures 4.10 m and the old wall behind it 4.7-5.6 m.
    // See docs/asset-plans/164-south-park.md 2.15.
    //
    // The exclusion is measured against the bake's OWN input (DataSF first,
    // Overture gap-fill, both simplified at SIMPLIFY_TOLERANCE 0.6), not
    // against the live APIs, and neighbours already dropped by an existing
    // landmark are discounted because a GLB stands in their place. From this
    // anchor:
    //    0.60 m  DataSF SF3775069, our own footprint, via its centroid
    //    1.43 m  Overture 469 m2, our own footprint again, via its centroid
    //            -> the FLOOR: below 1.43 the Overture ring survives and the
    //               procedural block pokes through the model
    //    3.06 m  DataSF SF3775067 (160 South Park) nearest vertex - already
    //            dropped by 160SouthPark's own exclude, so not a constraint
    //    3.76 m  Overture 76 m2 (the OSM `158 South Park` sliver) nearest
    //            vertex -> the CEILING. It shares a party-wall vertex with our
    //            own ring, nothing fills it, and above 3.76 the re-bake punches
    //            a hole there.
    //    8.57 m+ everything else, all covered by 156/168/188SouthPark
    // Safe window (1.43, 3.76), 2.33 m wide. 2.6 sits in the middle with 1.17 m
    // below and 1.16 m above, both comfortably over the 0.6 m simplify
    // tolerance. Verified on the re-bake: exactly the two 164 footprints drop
    // and the 158 sliver still stands. Do not widen without re-running that.
    //
    // No clearTrees: there are four real street trees on this frontage - they
    // are in every photograph of the building and they belong to the app's tree
    // system, not to this asset.
    id: '164SouthPark',
    name: '164 South Park',
    lon: -122.3949366,
    lat: 37.7812097,
    height: 5.4,
    exclude: 2.6,
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with +x
    // east and +z south, so camera bearing = 180 - yaw; the street facets face
    // 86-101 deg, so yaw 85 stands the camera out over the oval square onto
    // them. 120 m, closer than the 150-190 m used elsewhere on this rim,
    // because at 5.4 m this is the shortest landmark on it and the ribbon and
    // the canopy are the whole recognition.
    camera: { distance: 120, yaw: 85, pitch: 26 },
  },
  {
    // 345 Spear Street — the 1989-91 Whisler-Patri half of Hills Plaza:
    // buff-brick office podium (Google SF), the 18-storey One Hills Plaza
    // condo tower rotated 45 deg off the grid to face the bay, terracotta hip
    // pavilion on Spear, level-8 roof garden. The Hills Brothers Building
    // (2 Harrison) is its own landmark on the same block — in flight on the
    // pipeline/2-harrison branch; the two exclusions are independent.
    //
    // Exclusion sizing, measured against BOTH bake inputs from the registry
    // anchor (the footprint OBB centre — the manifest anchor is the model's
    // bbox centre 12.3 m away, they differ by design):
    //    3.2 m  Overture 98232020 (h=17.2, the OSM levels=5 copy), centroid
    //    5.6 m  DataSF 201006.0000159 (hgt_max 68.46), centroid
    //           -> the FLOOR: both own rings caught by centroid at r > 5.6
    //   15.8 m  own rings' nearest vertices (same building, harmless)
    //   47.1 m  DataSF 201006.0000430 (Hills Brothers) nearest vertex
    //           -> the CEILING: above 47.1 the re-bake deletes the sibling
    //              landmark's baked stand-in
    //   47.4 m+ everything else (Overture fragments on the Embarcadero apron,
    //           360 Spear data center, The Infinity II)
    // Safe window (5.6, 47.1); 25 sits mid-window with ~19 m margin below and
    // ~22 m above. No other footprint's centroid falls inside 47 m and no ring
    // covers the anchor except our own two (overlap-area check, 19 Aug 2026).
    id: '345Spear',
    name: 'Hills Plaza (345 Spear)',
    lon: -122.3900655,
    lat: 37.7900324,
    height: 68.5,
    exclude: 25,
    // camera.js puts the eye at target + distance*(sin yaw, ., cos yaw) with
    // +x east and +z south; yaw 115 stands the camera ENE over the Embarcadero
    // — the identity view: the arch arcade, the terraced staircase and the
    // bay-facing tower face-on, with the red pavilion behind.
    camera: { distance: 450, yaw: 115, pitch: 26 },
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
