# Oracle Park reference dossier

Research checked 11 August 2026. Published facts are separated from independent measurement and visual inference.

## Sources and what they establish

### Primary / institutional

- [OpenStreetMap relation 7325085](https://www.openstreetmap.org/relation/7325085) — current mapped outer footprint, `height=45`, address and stadium identity. I downloaded the 26-node geometry independently through the OSM API and measured it below.
- [San Francisco Giants: Oracle Park history](https://www.mlb.com/giants/ballpark/history) — official owner material: 12.7-acre site bounded by King, Second, Third and China Basin; five light standards, 556 LED fixtures, tallest standard 178 ft; 25 ft right-field fence; 309 ft right-field line; 339 ft left-field line; classic urban design.
- [San Francisco Giants: 2019 videoboard announcement](https://www.mlb.com/press-release/giants-to-begin-2019-season-at-newly-named-oracle-park-with-annual-rev-305574976) and [videoboard facts](https://www.mlb.com/giants/ballpark/videoboard) — current center-field display is 153.28 × 70.87 ft (46.7 × 21.6 m), substantially larger than the 2007 board.
- [Port of San Francisco / Giants public-access context](https://www.mlb.com/giants/ballpark) — waterfront setting and public Portwalk relationship.

### Architecture / engineering and factual cross-checks

- [Oracle Park, Wikipedia](https://en.wikipedia.org/wiki/Oracle_Park) — HOK Sport architect, current field dimensions, right-field wall 24 ft / 7.3 m, opening date and McCovey Cove relationship. The Giants' own historical page rounds the wall to 25 ft; the model follows the requested symbolic 24 ft.
- [Thornton Tomasetti project record](https://www.thorntontomasetti.com/project/oracle-park) — structural engineer attribution and steel/concrete structural context.
- [John King, San Francisco Chronicle architectural review](https://www.sfchronicle.com/news/article/A-Beautiful-Diamond-Slightly-Flawed-S-F-s-3304505.php) — brick warehouse-like street cloak, one-storey waterfront arcade, exposed steel structure and a reported 107 ft upper-deck wall.
- [This Great Game: Oracle Park](https://thisgreatgame.com/ballparks-oracle-park/) — architectural history and the five main public-view arches in the right-field wall; concrete/light waterfront arcade treatment versus the brick street facades.
- [Sports Illustrated: McCovey Cove quirk](https://www.si.com/mlb/2014/04/18/ballpark-quirks-mccovey-cove-att-park-san-francisco) — approximately 27 ft public sidewalk between stadium and water, fenced arch openings, and the evolution of the right-field wall.
- [Clem's Baseball stadium diagram](http://www.andrewclem.com/Baseball/ATTPark.html) — independent schematic cross-check of asymmetric field dimensions and eastward field orientation. Its coarse “ESE” label conflicts with my measured approximately ENE home-to-center bearing; see Orientation.

### Attributed visual references

All listed photographs are hosted on Wikimedia Commons and were inspected but are not committed here.

- [Aerial photograph of AT&T Park](https://commons.wikimedia.org/wiki/File:Aerial_photograph_of_AT%26T_Park,_home_of_the_San_Francisco_Giants.jpg) — strongest high oblique: complete bowl, waterfront arcade, three-tier west grandstand, field geometry, scoreboard, roof/canopy, and visible light-standard positions.
- [Oracle Park category](https://commons.wikimedia.org/wiki/Category:Oracle_Park) — broad day/night, exterior/interior and aerial coverage.
- [AT&T Park northern side 1](https://commons.wikimedia.org/wiki/File:AT%26T_Park_northern_side_1.JPG) — north/Second Street brick towers, roof pavilion, sign band and exposed green upper structure.
- [AT&T Park western side 1](https://commons.wikimedia.org/wiki/File:AT%26T_Park_western_side_1.JPG) — King/Third-side brick pier rhythm, large dark glazed openings and white trim bands.
- [AT&T Park satellite view](https://commons.wikimedia.org/wiki/File:AT%26T_Park_satellite_view.png) — top-plan cross-check.
- Esri World Imagery tiles, inspected 11 August 2026 — current top plan, field bearing, roof ring, open waterfront edge and footprint relationship. Not redistributed.

## Verified dimensions and location

| Item | Decision | Evidence / treatment |
|---|---:|---|
| Outer mapped footprint | **212.2 × 191.2 m oriented bound** | Independent minimum-area rectangle of OSM relation 7325085; polygon area 32,753.7 m². Axis-aligned true-world envelope is about 245.2 × 244.2 m because the footprint is rotated. |
| Footprint long-axis heading | **44.9° / 224.9°** | Independent oriented-bound measurement clockwise from true north. |
| Architectural height for manifest | **45 m** | OSM `height=45` and task plan. The official 178 ft / 54.3 m tallest light standard is measured from field/site datum and likely includes fixtures above the architectural mass; to preserve the requested manifest scale, the miniature's tallest point is authored at 45 m. |
| Right-field wall | **24 ft / 7.32 m** | Current published and symbolic value tied to Willie Mays #24. Giants history rounds to 25 ft; the exact asset wall is 7.32 m. |
| Scoreboard face | **46.7 × 21.6 m real reference** | Current 2019 board. The toy translation reduces it to a bold 36 × 14 m readable slab so it does not overwhelm the 45 m total-height envelope. |
| Light standards | **five** | Giants owner material explicitly says five, tallest 178 ft. Older/general imagery can appear to show more structural arrays because standards overlap or read as multiple support legs. The asset uses five standards. |
| WGS84 asset anchor | **[-122.3897993, 37.7786282]** | Requested production anchor; it lands near the stadium's central placement point. Independent OSM polygon centroid is [-122.3894652, 37.7785478], about 30.7 m east and 8.9 m south. The manifest anchor is retained because placement anchors need not equal geometric centroids and it matches the existing project plan/procedural landmark. |

## Orientation

Blender coordinates are authored as **+X east, +Y true north, +Z up**. No app-side yaw is expected.

- OSM outer-footprint long axis: **44.9° clockwise from true north**.
- Independent measurement on Esri World Imagery (home-plate circle to pitcher's mound, cross-checked against the 339 ft left-field pole, which measures 104 m at bearing 40.7°) puts the home-plate-to-center-field axis at approximately **85.5° clockwise from true north** (just north of due east). An earlier coarser pitch-polygon reading suggested about 76°; the mound-line measurement is the more precise and is what the asset uses.
- The bowl therefore opens broadly east toward the Bay. The lowest right-field/Portwalk edge lies east to southeast; the tall three-tier grandstand wraps the west and north-west street sides.
- Willie Mays Plaza/main ceremonial entrance is at the north-west/Second-and-King corner.

The Clem diagram's coarse “ESE” center-field label differs from the measured bearing. The mound-line satellite measurement and the real street/water relationship are more spatially precise, so the model uses the measured approximately 85.5° bearing.

Everything in the asset — field graphic, diamond, fence, bowl, decks, outer shell, gate and scoreboard — is generated in one home-plate-centred field frame rotated to that bearing, so the parts cannot drift out of alignment with each other.

## Observations by side

### North

Second Street/Willie Mays Plaza reads as brick entry towers, white/cream trim bands, a large sign/clock composition, and exposed green steel above. The upper-deck mass is tall and visually dense behind it. This is the formal public identity side.

### East

The Bay/Portwalk side is low and porous. A long pale concrete/brick arcade with repeated arches forms the waterfront elevation, with the playing field visible through the five principal right-field openings. Arcade seating and the 24 ft wall sit above/between these openings. This low edge is essential to the open-bowl silhouette.

### South

Third Street/China Basin edge exposes more green structural steel, ramps and service volumes than the formal north/west faces. The right-field corner and tall foul pole terminate the low arcade. The model simplifies the ramps into a strong green steel bay rhythm.

### West

King Street is a long warehouse-like brick elevation with tall dark openings, substantial piers and pale horizontal trim/cornice bands. The canopy and light standards rise above. The exterior remains visually calm so the interior bowl is the dominant aerial reading.

### Above

The strongest top view is an asymmetric baseball diamond within a horseshoe bowl: tall three-tier seating behind home plate and along the west/north sides, a low right-field arcade on the water, broad dark canopy ring, five light arrays and a giant center-field scoreboard. The open east edge and the sharply short right-field corner distinguish Oracle Park from a generic stadium.

### Day and night

Day appearance is dominated by warm red brick, matte dark-green steel/seating, pale concrete trim and vivid field graphics. At night the large center-field screen and five light arrays become the strongest emissive cues; the body remains mostly dark. `_Glow` is therefore limited to those surfaces.

## Recognition cues (ranked)

1. Large asymmetric baseball bowl opening east to the Bay, low on the waterfront side.
2. Red-brick street shell combined with exposed dark-green steel and seating.
3. Low right-field Portwalk arcade, especially the five large view arches and 24 ft wall.
4. Five oversized light standards and giant center-field scoreboard breaking the rim.
5. Legible field diamond with the unusually short right-field corner.

## Miniature conversion decisions

### Preserve

- True-world heading and broad real footprint.
- Tall west/north horseshoe versus low east waterfront edge.
- Three confident seating tiers and dark canopy ring.
- Brick street facades, green structural bays and pale waterfront arcade.
- Five principal right-field arches, five light standards, scoreboard and field asymmetry.

### Simplify / exaggerate

- Tens of thousands of seats become smooth stepped green seating bands with broad pale aisles.
- Complex concourses and ramps become a few thick ring volumes and visible green support bays.
- The surveyed footprint's service notches and left-field spike are box-filtered into a smooth chunky silhouette; the brick shell steps down from 24 m on the street sides to an 18.5 m outfield arcade, the real silhouette move that opens the bowl to the Bay.
- The scoreboard stands on a solid brick pedestal growing out of the centre-field concourse block, and the Willie Mays Plaza gate towers are a thickening of the shell wall itself, so neither reads as a detached prop.
- Street facades use large arched/window recess rhythms rather than literal brick/window grids.
- The five principal Portwalk view arches are enlarged for aerial readability; smaller secondary openings are omitted to keep the east edge clean.
- The scoreboard is slightly reduced from its current literal 46.7 × 21.6 m face but remains intentionally oversized as a recognition cue.
- Light standards use chunky paired masts and one readable lamp array each, not hundreds of fixtures.
- No Coke bottle, glove, people, boats, water, streets, bridge, statues or plaza furniture in the GLB.

## Uncertainties and conflicting evidence

- **Height:** OSM/project manifest says 45 m; the official tallest light standard is 178 ft / 54.3 m. These likely use different datums/definitions. The export tops at 45 m so app height scaling does not enlarge the already huge footprint.
- **Right-field wall:** official historical material says 25 ft while current summaries and the symbolic Willie Mays value say 24 ft. Use 24 ft / 7.32 m as explicitly requested.
- **Field bearing:** a coarse independent diagram labels center field ESE; the precise mound-line satellite measurement gives about 85.5°. Use the measured satellite heading.
- **Waterfront material:** sources describe the Portwalk elevation as pale concrete while the famous field wall is brick. The asset distinguishes these: pale arcade shell, brick right-field wall/piers, green steel.
- **Anchor:** requested placement anchor differs approximately 32 m from the mapped outer polygon centroid. Keep the requested anchor for compatibility, and document rather than silently replace it.
