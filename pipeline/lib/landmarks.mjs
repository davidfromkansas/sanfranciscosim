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
