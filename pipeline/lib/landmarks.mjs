// Bespoke landmark registry: true coordinates, the exclusion radius that keeps
// procedural footprints from fighting the hand-built model, and the camera
// preset the runtime flies to. Consumed by buildings.mjs (exclusion) and
// emitted to the app as landmarks.json (presets + placement).

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
  {
    id: '380Brannan',
    name: '380 Brannan Street',
    lon: -122.3940217,
    lat: 37.7806308,
    height: 12.6,
    exclude: 9,
    camera: { distance: 220, yaw: 45, pitch: 24 },
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
];

// Parks/green spaces the landcover bake must match at least one source polygon
// for; validate.mjs fails if any of these come up empty.
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
