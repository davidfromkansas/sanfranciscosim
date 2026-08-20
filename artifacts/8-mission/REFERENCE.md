# 8 Mission Street — reference dossier

**1 Hotel San Francisco**, formerly **Hotel Vitale**. 8 Mission Street, San Francisco,
CA 94105. Heller Manus Architects (Clark Manus, FAIA), completed 2005; LDA Architects
were the record architect; interiors by Colum McCartan. 199–200 rooms, 143,960 sq ft,
$53 M. OSM way `193054134`; DataSF LiDAR footprint `201006.0001079` (`mblr` SF3714019).

It fills the whole block between **Mission Street** (south-east), **Steuart Street**
(south-west), **The Embarcadero** (north-east) and **Don Chee Way / Harry Bridges
Plaza** (north-west), directly across the Embarcadero from the Ferry Building.

## Sources, and what each establishes

| Source | Establishes |
|---|---|
| [Heller Manus — 1 Hotel San Francisco](https://www.hellermanus.com/1-hotel-san-francisco) and [Hotel Vitale](https://hellermanus.com/projects/hotel-vitale) | architect; **eight storeys**; 200 rooms; **the circular turret with seven suites**; the rooftop spa |
| [LDA Architects — Hotel Vitale](https://www.ldaarch.com/hotel-vitale) | 2005; 143,960 sq ft; "200 guest rooms in **a series of stepped floors, topped by accessible terraces**"; "decks that bring the public out onto **the cascade of roofs**" |
| [SF Chronicle / SFGate, John King, 21 Apr 2005](https://www.sfgate.com/bayarea/place/article/SAN-FRANCISCO-COMMENTARY-Hotel-Vitale-failed-2678501.php) | **the load-bearing source.** Materials ("a base of rough Jerusalem limestone that after five feet or so gives way to smooth brown brick", "yellowish plaster on the upper stories"); massing ("eight stories along Mission Street but uses terraces to descend to **four-story and six-story wings** facing Harry Bridges Plaza", "tallest where it faces the three-story Audiffred, and shortest on Steuart Street"); **"a circular bay where Mission meets the Embarcadero"**; **"the inwardly curved notch where Steuart and Mission streets meet"** with "opaque glass that allows light into the lobby"; the porte-cochere entrance with its metal canopy; "the brown slab facing the northern plaza"; the Muni bus-yard site, the 1998 65-year lease and the Prop K shadow limits that produced the setbacks |
| [LA Times, 13 Mar 2005](https://www.latimes.com/travel/la-tr-ntb13mar13-story.html) | opening date; 199 rooms; $53 M |
| [SKYDB](https://www.skydb.net/building/935532621/hotel-vitale/), [Archello](https://archello.com/project/hotel-vitale) | 8 floors, 2005; five Heller Manus project photographs |
| [Condé Nast Traveler — Spa Vitale](https://www.cntraveler.com/activities/san-francisco/spa-vitale-at-hotel-vitale) | the spa "takes up **a rooftop corner** … a rooftop terrace … overlook the Ferry Building" — *observed (marketing photography)* |
| [Ocean Home](https://www.oceanhomemag.com/travel/hotel-vitale-offers-seaside-luxury/), [Time Out](https://www.timeout.com/san-francisco/hotels/hotel-vitale), [JustLuxe](https://www.justluxe.com/community/vital-relaxation-hotel-vitale-in-san-francisco-920011536/) | "penthouse-level spa set in a tranquil **bamboo garden**"; the circular suites' 180°/360° views — *observed (marketing photography)* |
| OSM API way `193054134` (37 nodes) | the footprint geometry, measured |
| [DataSF Building Footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni) | record `201006.0001079`: `hgt_maxcm` 2866, `hgt_majoritycm` 2510, `hgt_mediancm` 1964, `hgt_meancm` 1964.7, `hgt_stdcm` 601, 8,649 cells; record `201006.0017562` (the Muni vent pavilion): mode 4.49 m, max 6.28 m |
| Google satellite z21, stitched and overlaid with the OSM ring | the roof composition: green terrace decks on the low plateaus, the white mechanical field at the Mission end, the turret's circular roof, the spa deck, the vent pavilion's circular louvre — *observed* |
| Google Street View panoramas `5PjWOJB0thBrZhZJcrczXA` (Mission), `zXBL9q5JhlYVXn7nZUrCrQ` (Embarcadero), `NLmEUwDtUklmyMct15R5FA` (Steuart), `yPQsEQlbilZVbI4250XrJw` and `fee0fFoI73P9eoY8ahIbrw` (the east corner and the step-down), `dWxwJrZ7v60AQHfr5ZELPw` (from Harry Bridges Plaza) | the four elevations — *observed* |

## Verified dimensions and location

| | Value | Confidence |
|---|---|---|
| Footprint | **L-shaped**, 2,133 m²; minimum-area OBB **64.08 × 42.07 m** at bearing 135.37° | measured (OSM); DataSF agrees to 1.4% |
| Design anchor (OBB centre) | `-122.3932805, 37.7937365` | measured |
| **Shipping anchor (model XY bbox centre)** | **`-122.3932861, 37.7936872`** | derived — the L-shape puts the bbox centre 5.45 m south of the OBB centre |
| Crest — turret crown | **28.66 m** | measured (LiDAR `hgt_maxcm`) |
| Plateau A parapet — Mission block, 8 storeys | **25.10 m** | measured (LiDAR mode) |
| Plateau B parapet — middle, 6 storeys | **19.64 m** | measured (LiDAR median) |
| Plateau C parapet — plaza end, 4 storeys | **14.18 m** | **derived** — see correction 1 |
| Storey heights | ground 5.99 m, typical 2.73 m | derived from the 25.10 / 19.64 pair over 8 vs 6 storeys |
| Turret | circle centre (u,v) = (27.57, −16.52), **r 4.52 m** | measured (least-squares fit to OSM arc nodes) |
| Notch | concave arc, centre (32.29, 21.01), **r 5.96 m** | measured (three-point fit to OSM arc nodes) |
| Ground | 3.20 m min / 3.57 m mean | measured (LiDAR) |

Local frame used throughout: **u** along the 64.08 m axis toward bearing 135.37°
(Mission Street); **v** along the 42.07 m axis toward bearing 225.37° (Steuart Street);
origin at the OBB centre.

## Orientation

| Elevation | Faces | Length | Character |
|---|---|---|---|
| Mission Street | 135.37° | 30.68 m straight | hero. Arcade, entry canopy, plaster attic, 8 storeys |
| The Embarcadero | 45.37° | 37.38 m over two plateaus | hero. Projecting glazed bays on brick piers |
| Steuart Street | 225.37° | 58.33 m over three plateaus | the long one — the elevation that shows the setbacks |
| Don Chee Way | 315.37° | 17.70 m | the plaza end. Deliberately blank |
| Notch returns | 45.37° (20.4 m) and 315.37° (24.1 m) | | face the Muni vent shaft |

Free-standing on all four sides; **no party wall**.

## Corrections to `docs/asset-plans/8-mission.md`

The plan is a head start, not a citation. Seven things changed:

1. **Plateau C is 14.18 m, not "~13.80 m".** The plan's own derivation (ground 6.0 m,
   typical 2.73 m, four storeys) gives 5.99 + 3 × 2.73 = **14.18 m**; the 13.80 figure
   printed in the plan came from an earlier, discarded storey grid and was not
   re-derived after the grid was fixed. Arithmetic, not a re-measurement.
2. **The shipping anchor is not the OBB centre.** `-122.3932861, 37.7936872`, 5.45 m
   south. The L-shape's axis-aligned bounding box is not centred on the OBB.
3. **The XY bounding box is 74.14 × 56.55 m, not "~75 × 75 m".** The notch and the
   missing north quadrant shorten one world diagonal; a rotated *rectangle* would have
   been square-ish, an L is not.
4. **The Mission wall is 30.68 m of straight run, not 26.4 m.** The plan measured
   between two OSM vertices; the wall actually runs to the turret's tangent at
   v = −15.62. The OSM vertices at v ≈ −11.3 bound a 2.9 × 0.65 m service recess that
   was simplified away.
5. **The notch tangent on Mission is v = 15.06, not 15.10** (solved from the fitted
   circle rather than read off a vertex). Both tangents are now derived, which is what
   removed a duplicated polygon vertex — see REPORT.md 1.
6. **`8-mission-steps.png` is rendered from the SOUTH-WEST, not the north-east.** The
   plan asked for a north-east frame; the north-east elevation only carries two of the
   three plateaus. Steuart Street is the only elevation that contains all three.
7. **Renders are EEVEE, not Cycles.** Load average on the build machine was 149 with
   ~16 concurrent Blender processes; CPU Cycles makes no progress there. Nothing this
   pass judges needs path tracing.

## Recognition cues, ranked

1. The **circular turret** at the Mission × Embarcadero corner with its dark metal
   lantern crown — the only feature any source calls distinctive.
2. The **stepped roofline**, 25.10 → 19.64 → 14.18 m descending north-west, with
   planted terraces on the two lower plateaus.
3. **Pale plaster attic over brown brick over pale limestone** — three horizontal bands.
4. The **concave notch** at the Mission × Steuart corner, opposed to the convex turret.
5. The **arcaded ground floor** and the arched entry canopy on Mission.

## Preserved / simplified

**Preserved:** three plateaus and their parapets; the turret, its glazed shaft, its
eight brick ribs and its lantern crown; the notch and its curved lobby glazing; the
limestone plinth; the arcade; the entry canopy; the Embarcadero glazed bays; the
planted terraces; the spa pavilion and bamboo; the roof plant and its screen.

**Simplified away:** archivolt mouldings and keystones; window muntins; per-room
balcony rails; limestone rustication texture; individual bamboo canes (three or four
massed clumps instead); the porte-cochere column; the 2.9 × 0.65 m service recess on
Mission; the temporary clear marquee tent on the Embarcadero sidewalk (not
architecture).

**Excluded by scope:** the Muni subway vent-shaft pavilion in the notch (OSM way
`260290226`, ~20 × 15 m, 5.4 m). It is a separate structure on the same parcel, it
stays procedural, and the integration exclusion radius is sized to spare it.

## Uncertainties

- **Where the two setbacks fall in plan** is the weakest number here and remains
  *estimated*: u = +6 and u = −11.4, read off z21 satellite imagery (the extent of the
  white mechanical roof against the green decks) and cross-checked against the LiDAR
  mean and σ. The three *heights* are measured; their *positions* are not.
- **Plateau C's 14.18 m** is derived, not measured. No LiDAR statistic isolates it.
- **`hgt_maxcm` = 28.66 m is taken as the crest.** It is 1.5 σ above the mean, sits
  3.56 m — one storey — above the modal roof plane, has no party wall to bleed from,
  and the Street View panoramas show a turret crown standing about one storey proud of
  the parapet at that corner. Four reasons, so it is recorded as measured.
- **Storey heights are arithmetic**, from two LiDAR planes and two published storey
  counts, not from a rectified elevation.
- **`Toy_brick` (`c96f4a`) against King's "brown brick".** Kept per 2 South Park's
  recorded lesson; the deviation is noted rather than a new hex invented.
