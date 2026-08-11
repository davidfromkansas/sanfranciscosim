# Fairmont San Francisco reference dossier

Research checked 10 August 2026. Published facts are separated from visual
inference throughout; anything the model relies on that has no published figure
is marked *estimated*. No third-party imagery is committed with this asset —
the model and review renders are original work.

## Verified facts

| Item | Value | Confidence / source |
|---|---:|---|
| Address | 950 Mason Street, between California and Sacramento, atop Nob Hill | OSM tags, NRHP listing |
| WGS84 complex centroid | **-122.4101606, 37.7924935** | OSM relation/16217497 outer-way centroid (measured via Overpass) |
| Opened | 18 April 1907 (shell survived the 1906 fire; Julia Morgan led the reconstruction) | Wikipedia, Historic Hotels of America |
| Architects | Reid & Reid (James W. and Merritt J. Reid); Julia Morgan (post-fire); tower 1961–62 | Wikipedia, Wikidata |
| Style | Beaux-Arts (NRHP text: "Italian Renaissance") | Wikidata P149, noehill.com NRHP page |
| Main building floors | 9 | Wikipedia infobox |
| Tower floors / height | 29 floors, **99.06 m (325 ft)**, completed 1962 | Wikipedia infobox |
| Main block height | **~33 m to the main cornice, ~38 m with penthouses** | *estimated from the 9-storey count and photographic proportion — no published figure found; must stay `estimated` if the historic block ever anchors `targetHeightM`* |
| Mapped complex footprint | **117.9 × 84.1 m facade-aligned** (axis-aligned bbox 124.9 × 100.1 m), 14-node outer ring | OSM relation/16217497, measured via Overpass in the project's tangent projection |
| Interior courtyard (roof garden) | **22.2 × 38.4 m** hole in the multipolygon (`leisure=common`), west-center of the lot | OSM inner way 32947167 |
| Grid orientation | Facade axes bear **80.95° / 170.9°** true — the Nob Hill grid is rotated **~9.05° counter-clockwise from cardinal** | Measured from OSM edge bearings (10 long edges agree within 0.4°) |
| Landmark status | NRHP #02000373 (2002); SF Landmark #185 (1987) | noehill.com, Wikipedia |

## Orientation — corrects the asset-plan dossier

The plan document (`docs/asset-plans/fairmont-san-francisco.md` §2.3) states the
entrance "faces east onto Mason Street" with the tower "behind (west of) it".
**Street-network data and satellite imagery show the opposite.** Overpass
returns Mason Street at lon ≈ −122.4109 (≈65 m WEST of the complex centroid),
Powell Street ≈76 m east, California Street ≈65 m south, Sacramento Street
north. The building footprint spans x ∈ [−52, +73] m of the centroid, so Mason
runs along its **west** edge:

- **The Mason Street entrance faces WEST** (facade line bears 170.9°; outward
  normal ≈ **261° true**).
- **The 1961/62 tower stands EAST of the historic block** (downhill, toward
  Powell); Esri World Imagery shows the tall slab with its long shadow at the
  east edge of the lot, its long axis running north–south.
- The Mark Hopkins is across California to the SSE; its ornate crowned tower
  appears behind the Fairmont in many photos and must not be confused with the
  plain-crowned Fairmont tower.

The model is authored with Blender +Y = true north and +X = east, whole
composition yawed **+9.05° CCW** to the measured grid, entrance on the −X
(west) side. This satisfies the plan's real-orientation requirement; the
generic-landmark loader applies no rotation.

## Sources and what each establishes

- [OSM relation 16217497](https://www.openstreetmap.org/relation/16217497) —
  complex footprint, centroid, courtyard hole, address tags. Geometry measured
  locally via Overpass for every plan dimension used in the build.
- [Overpass street query] — Mason/California/Sacramento/Powell positions around
  the block; the basis for the west-facing-entrance correction above.
- [Wikipedia — Fairmont San Francisco](https://en.wikipedia.org/wiki/Fairmont_San_Francisco) —
  1907 opening, architects, 9 main floors, 29-floor tower at 99.06 m (1962),
  591 rooms, NRHP/SF landmark status.
- [Wikidata Q1393862](https://www.wikidata.org/wiki/Q1393862) — architects,
  Beaux-Arts style, opening date.
- [noehill — NRHP #02000373](https://noehill.com/sf/landmarks/nat2002000373.asp) —
  landmark listing, "Italian Renaissance" style note, 950 Mason between
  Sacramento and California.
- [Historic Hotels of America — Fairmont San Francisco](https://www.historichotels.org/us/hotels-resorts/the-fairmont-hotel-san-francisco) —
  1907 history, granite/marble/terra-cotta materials note.
- [Wikimedia Commons — Category:Fairmont Hotel (San Francisco)](https://commons.wikimedia.org/wiki/Category:Fairmont_Hotel_(San_Francisco)) —
  geolocated photography used to cross-check all four sides: the 2009 Mason &
  California corner view (south + west facades, flags, cornice), the 2013
  Mason & Sacramento view (porte-cochère, flag arc, giant colonnade, with the
  Mark Hopkins behind), the Powell-side tower view (slab massing, picket crown,
  round balcony, east-base rusticated arcade), and the 1906 R.J. Waters plate
  (east/downhill elevation with its tall arched base, pre-fire).
- Esri World Imagery satellite tiles (z19, fetched 2026-08-10) — roof layout:
  U-wings around the garden courtyard, penthouse positions, tower placement and
  N–S elongation, podium terrace between block and tower.

## What each side shows

**West (Mason Street) — the hero elevation.** Rusticated granite base (~2
storeys of horizontal-groove joints); projecting one-to-two-storey
porte-cochère at the center (the mapped 21.3 m × 6.9 m projection) carrying an
arc of ~20 international flags on its balustraded roof; above it a projecting
center pavilion with a giant Corinthian colonnade through roughly floors 4–7;
slightly projecting corner pavilions; regular window grid between; deep
modillioned cornice with continuous ornamental cresting; stepped parapet blocks
at the center and corners; two rooftop flagpoles (US and California flags) near
the west corners.

**South (California Street).** Long symmetrical flank in the same language —
base, six upper window rows, colossal-order accents, the full cornice — and at
the east (downhill) end the lower rusticated annex/podium with big arched bays
continues the block face toward Powell.

**North (Sacramento Street).** Same rhythm as the south flank with a secondary
entrance; the tower's north end and the parking/podium structures read at the
east end of this frontage.

**East (Powell side, downhill).** The slope exposes extra base storeys as a
tall rusticated arcade; the 29-storey tower slab dominates: pale
gray-cream, long axis N–S, mostly blank north/south ends with a narrow window
column, gridded west and east faces, a small round balcony near the top of the
north end, a glassy Crown Room band at the top floor, and a distinctive
projecting picket/crenellated parapet crown. Between tower and block sits the
lower ballroom podium with a roof terrace.

**Top.** The historic block reads as a ring of flat roof around the sunken
garden courtyard (west-center); penthouse/mechanical structures on the roof;
continuous cornice cresting outlines every edge; the tower roof is flat with
mechanical blocks inside the picket crown; the podium terrace sits between.

## Recognition cues (ranked)

1. A massive pale symmetrical Beaux-Arts block crowning Nob Hill — white/cream
   over a rusticated base, unmistakable at city scale.
2. The porte-cochère with its arc of colorful international flags on the Mason
   (west) front.
3. Heavy crested cornice line with stepped parapet blocks and rooftop flags.
4. Regular grid of identical windows + center giant colonnade.
5. The plain pale tower slab with its picket crown standing just east
   (downhill) of the ornate block — the pair is how the Fairmont reads from the
   air.

## Features to preserve

- The 9-storey historic block proportion and its full-block Mason frontage
  (84 m) at real footprint scale.
- Facade symmetry; window-grid regularity; base/body/cornice tripartition.
- The porte-cochère + flag arc (identity accent, semantically enlarged).
- The interior garden courtyard — the roof is highly exposed to the app camera.
- The tower's slab massing, N–S elongation, east placement, and picket crown.
- Hilltop prominence: do not shrink; the complex keeps real plan dimensions.

## Features to simplify

- Hundreds of ornamented window surrounds → identical recessed dark-glass
  openings on a clean grid (~4.3 m bay pitch, slightly oversized).
- All classical ornament → three readable horizontals: grooved base, one string
  course, chunky cornice with rhythmic cresting blocks.
- The colonnade → 8 chunky cylinders with simple capital blocks.
- Rooftop clutter → two penthouse volumes + flagpoles.
- The tower's curtain grid → recessed vertical glass strips crossed by thin
  spandrel ledges; crown pickets as a repeated-post ring.
- The sloped-site base → flat z=0 base (the app's terrain placement handles the
  hill; noted for integration).

## Uncertainties and conflicts

- **Historic block height is unpublished.** ~33 m cornice / ~38 m overall is
  scaled from storey counts and photos. The asset's overall height is anchored
  by the published 99.06 m tower instead, so the manifest can stay
  `estimated: false`; if the tower were ever dropped, the height must be marked
  estimated.
- **Plan-doc orientation conflict** (entrance east vs west) — resolved by map
  data + imagery in favor of **west**; see above.
- Tower completion 1961 vs 1962: sources say construction 1961, opening 1962.
  Cosmetic for the model.
- OSM `building:levels=2` on the relation is a podium-level artifact and was
  ignored.
- The exact tower footprint is not separately mapped; its 24 × 38 m slab is
  measured from satellite imagery (*inferred*) and sits within the mapped east
  arm of the complex polygon.
