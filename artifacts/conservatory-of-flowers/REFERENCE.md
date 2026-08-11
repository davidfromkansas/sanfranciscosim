# Conservatory of Flowers — reference dossier

Research compiled 2026-08-10 for the SF-SIM miniature GLB. Every value used by the
build is either verified below or explicitly marked as a design decision. The
plan dossier in `docs/asset-plans/conservatory-of-flowers.md` was the starting
point; everything load-bearing was re-verified independently.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/30675038](https://www.openstreetmap.org/way/30675038) (full geometry fetched 2026-08-10, check_date 2025-10-27) | Footprint outline (58 nodes), measured 75.7 m along the long axis × 35.6 m across (incl. rear service rooms); long-axis bearing **81.0° cw from true north** (PCA over projected nodes); centroid −122.4601761, 37.7725898; `height=15` tag; NRHP ref 71000184 |
| [Wikipedia: Conservatory of Flowers](https://en.wikipedia.org/wiki/Conservatory_of_Flowers) | Dome nearly 60 ft (~18.3 m); overall length 240 ft (73 m); built 1878–79 (Lord & Burnham); wood skeleton + glass on a **raised masonry base**; octagonal central pavilion; one-story symmetrical wings with four-centered (Tudor) arches; south one-story glassed-in vestibule with gable roof; 1883 fire → replacement dome "more classically domical", raised 6 ft; ridge ventilators; 16,800 panes |
| [NRHP nomination 71000184 summary (noehill.com)](https://noehill.com/sf/landmarks/nat1971000184.asp) | **Shallow E-shaped plan on an east–west axis**; wings are L-shaped in plan with **cupolas at the intersection of the two segments**; clerestory + dome above the octagonal pavilion carried on eight wood-clad cast-iron columns; **dormer windows with peak roofs on the east, west and south** of the pavilion roof |
| HABS CAL,38-SANFRA,147 photos 1, 3, 5, 6 (Library of Congress, public domain, via [Commons HABS category](https://commons.wikimedia.org/wiki/Category:Conservatory_of_Flowers_(HABS))) | Four-side + rooftop visual evidence used for massing and detail (observations below) |
| [Commons: “Conservatory of Flowers Greenhouse from overpass” (MG 7197)](https://commons.wikimedia.org/wiki/File:Conservatory_of_Flowers_Greenhouse_from_overpassMG_7197.jpg), [front 2007](https://commons.wikimedia.org/wiki/File:Conservatory_of_Flowers,_San_Francisco,_front,_2007.jpg) | Modern colour state: all-white structure, milky pale glazing, **red-brick plinth**, formal parterre south of the building |
| [Wikidata Q1129107](https://www.wikidata.org/wiki/Q1129107) | Lord & Burnham manufacture, Italianate styling |

## Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Dome apex (architectural height) | **18.3 m** (nearly 60 ft; dome was raised 6 ft after the 1883 fire) | Published (Wikipedia); consistent with people-for-scale in HABS 147-1 |
| Overall length | **~75.7 m** measured from OSM; published 240 ft (73.2 m) — the extra ~2.5 m is the end-pavilion bulge | High |
| Depth (main E-shaped structure) | wings ~14–18 m; southward projections (both end pavilions and the vestibule) reach ~8–9 m south of the wing face; **rear north service rooms** push OSM total depth to 35.6 m | High (footprint math) |
| Long-axis bearing | **81.0° cw from true north** (wings run ENE–WSW, 9° off pure east–west) | High (PCA of OSM nodes) |
| Anchor (dome axis) | **−122.4602321, 37.7725965** — computed: footprint centroid moved to the vestibule/dome axis (local u = −4.75 m, v = +1.5 m). The plan’s anchor (−122.4601775, 37.7725877) is the raw footprint centroid, ~4.9 m ESE of the dome axis because the asymmetric rear service rooms skew the centroid | High |
| OSM `height=15` | Treated as the clerestory/skirt-roof zone, **not** the dome apex; 18.3 m governs | Judgement, per plan §2.13 |

## Orientation

Symmetric about a north–south axis through dome + vestibule; wings run along the
81° bearing; the **entrance vestibule projects south** toward JFK Drive and the
parterre. Authored with Blender +Y = true north: the model is built on local
axes and yawed **+9°** (90° − 81°) so the wings sit on the real heading; the
front (vestibule) normal is then (0.156, −0.988) — within 9° of −Y, so the
front-faces-−Y rule is naturally satisfied. No loader rotation required.

## What each side shows (from HABS 147-1/3/5/6 + modern photos)

- **South (front, hero):** raised terrace; central octagonal pavilion — drum of
  tall narrow arched glass bays with a lattice transom band, then a broad ribbed
  “skirt” roof with an ornate Gothic **dormer**, a railed gallery, the octagonal
  lattice **clerestory**, and the great ribbed dome with a multi-stage finial.
  A gabled glass **vestibule** with decorated bargeboard projects at centre,
  flanked by low lean-to glass aprons. Wings run left and right: white paneled
  knee wall, tall glass bays, elliptical-arched glass roofs with **cresting**
  along the ridge; each wing ends in a broad octagonal domed **end pavilion**
  with a small **ogee cupola + finial**, projecting slightly south (the E-plan).
- **North (rear):** same composition minus the vestibule; a **low lean-to
  service greenhouse range** runs along the back (visible in HABS 147-6);
  modern potting/boiler rooms behind (excluded from the miniature).
- **East/West (wing ends):** the octagonal end-pavilion dome on its paneled
  knee wall + brick plinth, small gabled secondary entrance porch with lattice
  posts, ogee cupola behind.
- **Top (HABS 147-6):** dense pane grids on every roof; wing ridges carry a
  continuous row of small cresting finials; the two end domes + cupolas; the
  central composition reads dome → clerestory → gallery → skirt roof; small
  vent/chimney blocks near the wing/pavilion junctions.

## Strongest recognition cues (ranked)

1. **The ribbed white dome on its two-tier pedestal** (skirt roof → gallery →
   lattice clerestory → dome → finial).
2. **Perfect bilateral symmetry**: two long arched glass wings ending in domed
   octagonal end pavilions with ogee cupolas.
3. **Dense white rib rhythm over milky glass** on every surface.
4. **The gabled south vestibule** announcing the entrance.
5. **Victorian lace**: ridge cresting and finials punctuating every apex.

## Features to preserve / simplify

**Preserve:** 18.3 m apex over ~75 m length; exact bilateral symmetry; ribs as
real geometry; the E-plan (end pavilions + vestibule stepping south); the
two-tier dome pedestal; ogee cupolas; ridge cresting presence; red-brick plinth
under white knee walls.

**Simplify (style bible §22/§26):** hundreds of glazing bays → ~1.9 m rib
rhythm with deliberately fat 0.35–0.45 m ribs (thin ribs alias at city scale);
dome meridians → 16 + 2 rings; lattice clerestory → 8 arched white-framed
bays; lace cresting → chunky finial teeth at ~1.9 m spacing; Gothic dormers →
3 simple peaked dormers (S/E/W per NRHP); ornate multi-stage finial → bold
lantern + spike; rear service clutter → one clean low lean-to range; secondary
end porches → small gabled porch masses.

## Scope decisions

- **Flower beds / parterre / lawn / JFK Drive: excluded** — park data supplies
  planting (plan §2.10). The red masonry terrace + grand stair south of the
  building are landscape, not building, and are also excluded.
- **Plinth: included** — the raised masonry (red-brick) base is architecturally
  integral; the building never touches bare grass.
- **Rear lean-to range: included in simplified form** (it is part of the
  conservatory silhouette from the north/above); the deeper modern service
  boxes that push the OSM footprint to 35.6 m are excluded, so the miniature’s
  depth (~27 m) is intentionally less than the raw OSM bounding depth.

## Uncertainties and conflicts

- **Dome height**: “nearly 60 feet” is the only published figure; 18.3 m is
  used as the apex (finial tip) per the plan. If the 60 ft was interior, the
  real exterior tip could be ~1 m higher — accepted risk, documented.
- **OSM `height=15`** conflicts with the 18.3 m apex; resolved as the wing/
  clerestory zone height (the OSM tag predates any survey of the dome).
- **Cupola placement**: NRHP puts cupolas “at the intersection of the two
  segments” of each L-wing; in HABS 147-1/147-5 they read at/near the end-dome
  apex from distance. The miniature places one cupola at each end-dome apex —
  the city camera reading, chosen deliberately.
- **Plan dossier deviations**: anchor moved ~4.9 m to the dome axis (see
  above); “6 barrel ridge turrets” replaced by cresting teeth + 2 low ridge
  ventilator monitors per wing (the photos show cresting + ridge ventilators,
  not turrets); wing roofs modelled as elliptical vaults with paneled knee
  walls rather than pure half-cylinders; night glow implemented as thin
  `Toy_white_Glow` shells proud of the (opaque `Toy_glassl`) rotunda, lantern
  and end-dome glazing plus a `Toy_gold_Glow` entry transom — the plan's
  "dome glazing = glow material" would render ~88 % transparent by day in the
  app, because the loader draws `_Glow` surfaces only in the unlit night layer
  (opacity 0.12 + 0.95·uNight).
