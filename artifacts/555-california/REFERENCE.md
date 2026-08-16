# 555 California Street — reference dossier

Research for the SF-SIM miniature landmark asset. Compiled 10 August 2026 by
independent verification of `docs/asset-plans/555-california.md`; that plan's
dossier was the starting point, not the authority. Where this file disagrees
with the plan, **this file is the record of what was checked and decided**, and
the disagreements are called out explicitly in §8.

---

## 1. Verified facts

| Item | Value | Source | Confidence |
|---|---|---|---|
| Architectural height | **237.4 m / 779 ft** (to architectural top) | CTBUH | verified |
| Height to tip | 237.4 m / 779 ft — identical, nothing rises above the penthouse | CTBUH | verified |
| Height datum | "779 feet above the **Plaza level**", penthouse included | SEAONC | verified |
| Main parapet / occupied roof | ≈ 226 m | OSM `building:part`; photogrammetry | estimated |
| Floors | **52 above ground, 4 below** | CTBUH, Vornado, Wikipedia | verified |
| Floor-to-floor | **13 ft / 3.96 m** slab-to-slab | Vornado leasing data | verified |
| Completed | **1969**, as the Bank of America Center | CTBUH, SOM, Wikipedia | verified |
| Architects | **Wurster, Bernardi & Emmons with Pietro Belluschi**, SOM providing coordination and production assistance | SF Planning HRER 2017 (SOM's own page and Wikipedia credit SOM as lead — see §8) | verified |
| Plaza landscape architect | **Lawrence Halprin** | SF Planning HRER 2017 | verified |
| Stone | **Coldspring "Carnelian®"**, quarried at Milbank, South Dakota; **polished** on the tower | Coldspring; Encyclopedia.com (Cold Spring Granite history); HRER | verified / strong inference |
| Aviation lighting | **Red obstruction lights**, FAA Digital Obstacle File record **06-000484**, 809 ft AGL / 862 ft AMSL, `Lighting = R` | FAA DOF | verified |
| Antenna masts | reach **~809 ft AGL**, i.e. ~30 ft above the 779 ft architectural top; FCC ASR #1205157 gives 249.9 m AGL, structure type BANT | FAA DOF; FCC bulk ASR data | verified |
| Historic status | Not a city landmark and NR-ineligible (OHP status 6Y), but **determined California Register eligible** in 2017 under Criterion 3, CEQA Category A | SF Planning HRER; OHP BERD | verified |
| Structural engineer | H.J. Brunnier Associates; all-steel moment frames, caisson foundations | CTBUH, SEAONC | verified |
| Tower plate | **243 × 143 ft (74.07 × 43.59 m)** | SkyscraperPage; Emporis (archived) | verified |
| Typical floor | ~30,000 RSF — independently corroborates the plate above | Vornado | verified |
| Long-axis bearing | **80.9° clockwise from true north** | derived from the California/Pine St centrelines | verified |
| Corner treatment | **All four corners chamfered 45°**, consuming **11.5 ft (3.5 m)** of each face; the plan closes exactly as 11 × 20 ft + 2 corner bays = 243 ft, and 6 × 20 ft + 2 corner bays = 143 ft | arithmetic on the published plan dims; *Architectural Record* typical-floor plan | verified |
| Bay module pitch | **nominal 20 ft (6.096 m)**; **11 full bays + 2 corner bays** per long face, **6 + 2 corner bays** per short end (= 12 and 7 bay-widths corner to corner) | five independent measurements agreeing within 2.5%: three photogrammetric elevations, the roof parapet zigzag in nadir aerial, and the *Architectural Record* typical-floor plan. **No source publishes the figure.** | measured |
| Bay projection | **≈ 7 ft (2.1–2.4 m)** | roof parapet zigzag amplitude in nadir aerial; OSM implies 7.2–7.7 ft | measured |
| Floor-to-floor | 13 ft — photogrammetry gives 12.95 ft from the same calibration as the 20 ft module, an independent check on both | Vornado; photogrammetry | verified |
| Mechanical floors | **15th and 27th**, read as bands of narrow louvre slots | *Architectural Record* July 1970 section | verified |
| Main roof deck | **740 ft (225.6 m) above plaza** | USGS 3DEP lidar (2023) | measured |
| Penthouse | **~166 × 68 ft, +40 ft above the main roof**, centred, granite sawtooth cladding | lidar, nadir aerial, *AR* roof plan (three methods within 7%); SF DBI permit 202411064461 | verified |
| Cladding | **Polished red "Carnelian" granite**; **bronze-tinted** glass | SOM, SEAONC, Wikipedia | verified |
| WGS84 anchor | **−122.4037741, 37.7921047** (tower shaft centroid) | computed from OSM | verified |
| Streets | **N = California, S = Pine, W = Kearny, E = Montgomery** | OSM street ways | verified |
| Plaza | A.P. Giannini / Bank of America Plaza, on the **north** side facing California St; ~84 × 43 m, raised above the sidewalk | Wikipedia, OSM rel 17101142 | verified |
| Sculpture | *Transcendence* ("the Banker's Heart"), Masayuki Nagare, 200 t black Swedish granite, in the plaza | Wikipedia, OSM node 3357102023 | verified |

### The height conflict — resolved

The plan flagged Wikipedia's 237 m against OSM's `height=226 m` and asked for
resolution before setting `targetHeightM`. There is no real conflict:

- **CTBUH gives 237.4 m / 779 ft** for both architectural top and tip.
- **SEAONC**, the structural engineers' own record, states the 779 ft *includes
  the penthouse* and is measured *from the plaza deck*.
- **OSM's 226 m is a mapper artifact, not a published figure.** The way's tag
  history shows `height=237 m` from 2020 until 2024-01-26, when the mapper who
  built the 3D massing changed the shaft to 226 and created a separate penthouse
  part tagged `height=237 m`. 226 m is that mapper's estimate of the main
  parapet.

**Decision: `targetHeightM` = 237.4**, modelled as the top of the mechanical
penthouse, with the main parapet at 226 m. Both numbers are therefore honoured —
they simply measure different things. (buildingsdb's 778 ft is a rounding
variant; CTBUH is preferred.)

### The footprint correction — important

The plan quotes "84.0 × 44.1 m" from OSM way 288511106. That way is the **tower
plus the one-storey east podium**, which is why its bounding box runs ~10 m
further east and why its eastern end reads as a flat unserrated wall. The tower
itself is **243 × 143 ft (74.07 × 43.59 m)**, published by SkyscraperPage and the
archived Emporis record, corroborated by Vornado's ~30,000 RSF floor plate, and
closing exactly against the 20 ft bay module. The asset uses that figure.

### The bay module — what it actually is

This was got **backwards** in the first pass and is worth stating plainly.
The module is a **two-facet chevron pointing outward, glazed on both flanks**;
the **granite column face sits at the re-entrant (inner) corner** between bays,
in a single continuous plane. There is no granite "nose" at the projecting apex.
The decisive evidence is the architects' own text in *Architectural Record*,
July 1970:

> p. 126: "As the eye moves to the ground a projected bay becomes an indented
> bay at the second floor, **while the column faces remain in the same plane**."

> p. 129: "A **W-shaped** basic work platform moves up and down the facade within
> permanent grooves set **in the interior corners of the bays**."

A W-profile washing cradle riding grooves at the *interior* corners is only
possible over a continuous two-facet zigzag whose re-entrant corners are the
piers. *Architectural Forum* (Jul/Aug 1968, p. 94) calls them "continuous
saw-tooth bays of polished red granite and bronze-tinted glass".

Why photographs nonetheless read as alternating granite and glass verticals:
each glass flank carries a **carnelian granite spandrel band at every floor**, so
in raking sun one flank's spandrels blaze — reading as a ~10 ft granite pier —
while the other goes black. That photographic read is what the miniature
reproduces; see §6.

---

## 2. Sources

| Source | What it establishes |
|---|---|
| [CTBUH / Skyscraper Center #1027](https://www.skyscrapercenter.com/building/555-california-street/1027) | Authoritative heights (237.4 m / 779 ft architectural and tip), 52/4 floors, 1969, all-steel structure, architects, engineer, GFA |
| [SEAONC — 555 California Street](https://legacy.seaonc.org/structure/555-california-street/) | "The height including penthouse is 779 feet above the Plaza level"; "saw tooth exterior carnelian granite walls"; steel moment frames, caissons |
| [Wikipedia — 555 California Street](https://en.wikipedia.org/wiki/555_California_Street) | "thousands of bay windows… to symbolize the bay windows common in San Francisco residential real estate"; "The irregular cutout areas near the top of the building were designed to suggest the Sierra Nevada"; plaza on the **north** side; *Transcendence*; Carnelian Room on 52 |
| [SOM — 555 California Street](https://www.som.com/projects/555-california-street/) | The architect's own text: "faceted bronze-tinted bay windows"; "upper-floor setbacks… evoking the jagged rock formations of the Sierra Nevada"; plaza occupies half the site |
| [Vornado — 555 California Street](https://www.vno.com/office/property/555-california-street/3311899/landing) | Owner data: 52 floors, 1,507,000 RSF, ~30,000 RSF typical floor, **13 ft slab-to-slab**, entrances on all four streets |
| [SFYIMBY](https://sfyimby.com/2021/11/number-6-555-california-street-financial-district-san-francisco.html) | Tower sited at the **southwest corner of its block**; main entrance "in a deep arcade beneath the setback of the tower's second floor" |
| OSM way 288511106 (Overpass) | Outline: 65-vertex chamfered sawtooth polygon, tags, `building:levels=52` |
| OSM ways 1243267628, 1244283830–36; rel 17101142 | The 3D massing: tower plate, four level-48 setback strips, penthouse, east podium, plaza polygon |
| OSM way history API | Provenance of the 226 m tag (was 237 m until 2024-01-26) |
| [Commons: *555 California Street from Coit Tower*](https://commons.wikimedia.org/wiki/File:555_California_Street_from_Coit_Tower.jpg) | North elevation, long lens: bay count, mechanical louvre band, multi-level crown, penthouse |
| [Commons: *555 California Street and 333 Bush Street from One Montgomery*](https://commons.wikimedia.org/wiki/File:555_California_Street_and_333_Bush_Street_from_One_Montgomery,_San_Francisco.jpg) | South elevation: the irregular asymmetric terraced setbacks; full-height chamfered corner masses; granite colour in raking sun |
| [Commons: *Perspective view of 555 California Street building*](https://commons.wikimedia.org/wiki/File:Perspective_view_of_555_California_Street_building,_San_Francisco,_California,_USA.jpg) | Worm's-eye at a chamfered corner: the V-bay section, bay continuity full height, louvre slots |
| [Commons: *555 California Street 2 2023-12-29*](https://commons.wikimedia.org/wiki/File:555_California_Street_2_2023-12-29.jpg) | Plaza at night: raised granite deck, steps and railing, and **no facade floodlighting** |

No published architectural elevation, landmark nomination or SF Planning HRE was
located; the setback geometry is therefore read from photography (see §8).

Reference imagery was consulted online and is **not** committed to this
repository — the Commons files above are individually licensed and full-resolution
copies are not ours to redistribute. The links are the contact sheet.

---

## 3. Orientation

The tower's long axis runs **81.23° clockwise from true north**, along
California Street, and it sits at the **southwest corner of its block**:

- **North — California Street.** The public face, set ~36 m back behind the
  raised granite plaza. Main entrance, in a deep arcade under the second-floor
  setback.
- **South — Pine Street.** Same sawtooth, only ~8 m from the property line, and
  its crown setbacks are **not** a mirror of the north face.
- **West — Kearny Street.** The short end, effectively on the sidewalk line.
- **East — Montgomery Street.** The short end; a one-storey podium continues east
  toward 345 Montgomery.

The asset is authored in true-world orientation (Blender +Y = north, +X = east)
because `placeGeneric` in `app/src/assets.js` applies no rotation.

---

## 4. What each side shows

**North (California Street)** — Twelve projecting granite-nosed V-bays, unbroken
from the arcade to the parapet. The upper ~10 floors terrace back irregularly.
The chamfered NW and NE corners run full height as solid masses.

**South (Pine Street)** — Geometrically the same skin; a different, non-mirrored
setback pattern at the crown.

**East / West (short ends)** — Seven bays each. The sawtooth reads most strongly
here because the flanks catch light at an angle.

**Chamfered corner faces (×4)** — Narrow, granite-dominant, visibly less glassy
than the main elevations. They read as solid vertical piers and anchor the
silhouette.

**Top** — A flat roof deck with a parapet, crenellated by the bay noses. A blank,
windowless granite **mechanical penthouse** inset ~11 m all round (≈52 × 22 m),
its sawtooth continued as solid stone. Masts and dishes cluster at the west end;
window-washing rigs on rails at the east end. Nothing rises above the penthouse.

**Facade bands** — At least one full-width **mechanical louvre band** at roughly
155–160 m (floors ~36–38): tall narrow slots, about two per bay module, spanning
two floor heights. A strong horizontal accent on an otherwise uniform shaft.

---

## 5. Recognition cues (ranked)

1. **The unbroken granite sawtooth.** ~12 V-bays per long face, 7 per short end,
   dead straight from base to parapet. Nothing else in San Francisco looks like
   this. If only one thing is right, it must be this.
2. **The irregular terraced "Sierra Nevada" crown, governed by one published
   rule:** "While **each of the four corners rises the whole 52 floors**, the
   **middle of each face is set back on the upper floors**. The final form
   visually elongates each corner and emphasizes the height" (SFYIMBY). Roughly
   four staggered step levels across the top ~10–12 floors, each about one bay
   module deep, at different positions on every face — not mirrored, not
   rotationally symmetric.
3. **The blank granite penthouse box**, inset and windowless, reading as a
   distinct second mass on a flat deck.
4. **Value, not hue.** Dark oxblood-to-charcoal granite plus dark bronze mirror
   glass: the tower must read *darker* than its pale neighbours. The red shows
   only as pink highlights in raking light.
5. **Broad slab proportions** — it is emphatically not a point tower.

---

## 6. Miniature translation

**Preserve**

- 237.4 m over the real 74.5 × 44.45 m plate at the real 81.23° heading
- The sawtooth at its true 6.21 m pitch and 2.1 m throw, full height, all faces
- Chamfered corners running full height, uninterrupted by the crown setbacks
- The asymmetric, multi-level crown and the inset blank penthouse
- The tower reading darker and warmer than its neighbours

**Simplify / exaggerate**

- 52 storeys of granite spandrel bands → the vertical sawtooth corrugation alone.
  The real facade is a grid, but its dominant grain is vertical, and at the app's
  camera a 52-row grid aliases into mush (style bible §26).
- Individual bay columns terminating at many different floor levels → three
  notch levels, each one bay module deep, widening rather than deepening with
  height, with unequal and non-mirrored spans on every face and the four corner
  masses left intact.
- Roof plant → three masts, three plant blocks, two washing rigs and a rail. The
  three cooling towers are real but sit *below* the granite screen (lidar puts
  them at 768–773 ft against a 779 ft parapet), which is why they never appear in
  a skyline photograph, so they are not modelled.
- The plaza, its paving and *Transcendence* → out of scope; only the low granite
  podium plinth is modelled.

**Documented deviations from reality**

- **Bronze-tinted glass → `Toy_glass` (dark navy).** The style bible (§5) makes
  dark blue-grey the project's window language, and warm glass against warm
  granite would collapse the facet legibility that is cue #1. Authority order
  puts the style bible above literal accuracy for artistic interpretation.
- **The chevron is inverted: granite on the projecting facet, glass in the
  valley.** In reality the apex points out and is glazed on both flanks, with the
  granite pier at the re-entrant corner. Built that way at this scale the tower
  renders as a blue glass slab and loses cue #1 and cue #4 outright — that
  version was built and rejected. The miniature keeps the true 20 ft pitch, the
  ~7 ft throw, the module counts and the corrugation frequency, but makes the
  projecting facet granite and recesses the glazing into the valley.

  This is defensible rather than merely convenient: because every real glass
  flank carries a granite spandrel band at each floor, in raking light one flank
  reads as a ~10 ft granite pier and the other goes dark, so **photographs of the
  real building already read as alternating granite and glass verticals**. The
  miniature produces that same read directly, at a scale where per-floor
  spandrels would be sub-pixel. What is lost is the true material assignment;
  what is kept is the appearance and the geometry.
- **Carnelian granite → `Toy_rust` (#a86444).** The nearest palette entry, and
  the plan explicitly forbids inventing a new colour. It reads more orange and
  lighter than the real stone; the deep sawtooth shadows and the dark glass do
  the darkening that cue #4 asks for.

---

## 7. Materials

| Material | Hex | Used for |
|---|---|---|
| `Toy_rust` | `a86444` | granite: bay noses, valleys, arcade piers, parapet, penthouse |
| `Toy_glass` | `2a4d73` | canted bay flanks, arcade glazing |
| `Toy_stone` | `d9d2c2` | plaza podium plinth |
| `Toy_roofd` | `45454a` | roof deck, plant blocks |
| `Toy_steel` | `9aa0a6` | terrace decks, masts, washing rigs, rail |
| `Toy_ink` | `3a3530` | mechanical louvre band |
| `Toy_sand_Glow` | `ece4d4` | scattered lit office panes (night) |
| `Toy_gold_Glow` | `caa64a` | the arcade lantern (night) |
| `Toy_red_Glow` | `c4453c` | FAA obstruction beacons on the penthouse (night) |

**Night.** Neither the architect, the owner's spec sheet, nor the 2017
renovation architect mentions any exterior lighting, and night photography of the
plaza shows **no facade floodlighting and no crown lighting** — unlike Salesforce
Tower, whose LED crown is heavily documented. 555 California is not a *Let's Glow
SF* projection venue and carries no rooftop sign. What it does have is confirmed:
**red FAA obstruction lighting** (Digital Obstacle File record `06-000484`,
809 ft AGL, `Lighting = R`), on the penthouse.

So the night state is: sparse `Toy_sand_Glow` panes on the bay flanks, one
`Toy_gold_Glow` arcade lantern, and four small `Toy_red_Glow` beacons recessed
into the penthouse cap. No crown line, no facade wash — the tower stays a dark
mass, which is the point.

---

## 8. Uncertainties and conflicting evidence

- **The setback *rule* is published; the specific floor numbers are not.** The
  corners-full-height / middles-set-back rule is documented (SFYIMBY), as is the
  "last 10 floors" extent (buildingsdb) and the Sierra Nevada intent (SOM). But
  no published elevation, landmark nomination or planning drawing gives step
  floors, depths or the per-face pattern. Those are measured off the
  *Architectural Record* section (west end ~3 steps around floors 45/43/41; east
  end ~2 steps around 42/40 — the two ends are drawn differently) and off the
  north and south elevation photographs (~4 staggered levels each, at different
  horizontal positions). Treat the exact levels in the build script as an
  informed reconstruction, not a citation. A web summariser's claim that
  "setbacks begin at floor 43" appears in none of the sources actually fetched
  and was discarded.
- **OSM's `building:levels=48` perimeter ring is a modelling convenience.** It
  gets the idea right (corners tall, middles cut) but flattens a deliberately
  asymmetric design into one symmetric ring. OSM's orientation is also ~5° off
  and its bounding box oversized (77.2 × 45.2 m against the published 74.07 ×
  43.59 m), with the two long faces mapped at different lengths — hand-tracing
  noise. The published dimensions are used instead.
- **CTBUH's "height to tip" looks wrong.** It lists tip = architectural top =
  237.4 m, but the FAA Digital Obstacle File and FCC ASR #1205157 both put
  antenna masts at ~809 ft AGL, roughly 30 ft above the architectural top.
  Immaterial here — the asset models the architectural top, as `targetHeightM`
  should.
- **The plan doc places the entrance and plaza on the south/California side.
  That is wrong on both counts.** OSM street ways put California Street on the
  **north** of the tower and Pine Street on the south, and both Wikipedia and
  SFYIMBY put the plaza on the north. Decided in favour of the sources: north =
  California = the public face.
- **The plan doc's footprint (84.0 × 44.1 m) is the tower plus its east podium.**
  Corrected to 74.51 × 44.45 m; see §1.
- **Bay count ±1.** An FFT of the louvre band gives a dominant k=12 with k=11 and
  k=13 as neighbours; the OSM trace independently gives 11.9. Twelve is solid but
  not certain to ±1. The build divides each edge by the 6.21 m pitch and lands on
  the same count.
- **Plaza height above the sidewalk is unverified numerically** — photographs
  suggest roughly half a storey. It does not affect this asset, whose podium is a
  1.6 m plinth.
- **The 779 ft datum is the plaza deck**, which is itself raised above the
  street. Height above the lowest surrounding sidewalk is therefore slightly
  greater. Not corrected for: the app grounds the asset on sampled terrain.
- **Authorship is contested between sources.** SOM's own project page, CTBUH and
  Wikipedia present SOM as the designer. SF Planning's 2017 HRER instead credits
  Wurster, Bernardi & Emmons with Pietro Belluschi, "with Skidmore, Owings &
  Merrill providing coordination and production assistance." The HRER is the more
  rigorous document and is followed here; it does not change any geometry.
- **The "banking hall" is a different building.** The glazed banking pavilion is
  345 Montgomery Street, a separate 3½-storey structure at the opposite (north-
  east) corner of the site, completed 1971. The tower's own base is a deep
  entrance arcade on "heavyset granite-clad pilotis" beneath the second-floor
  setback. The plan doc's "banking-hall base" scope item is modelled as that
  arcade; 345 Montgomery is out of scope.
- **An Article 11 "Category I" rating displays against this parcel and is an
  artifact.** DataSF's Article 11 layer keys a `315 MONTGOMERY / BANK OF AMERICA /
  Category I` record to APN 0259026; the Article 11 appendices themselves contain
  no entry for 555 California. The Category I building is the 1921 bank at 315
  Montgomery, not this tower.
- **Plaza rise above the California Street sidewalk is unverified numerically.**
  The HRER records "tapered stairs reflecting the descending grade" so the rise
  varies along the block; the pavilion's plaza entry at "partial third story"
  suggests roughly two storeys at the east end. Estimated 15–25 ft, tapering.
  Does not affect this asset.
- **The "dark mass at night" characterisation has no direct citation.** It is an
  inference from the documented absence of any facade or crown lighting plus the
  dark polished granite and bronze glass. The FAA beacon record, by contrast, is
  hard evidence.
- **Stone finish split unverified.** Sources say "polished or rough carnelian
  granite" without saying which element got which.
