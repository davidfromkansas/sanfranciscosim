# Palace of Fine Arts — reference dossier

Research compiled 2026-08-10 for the SF-SIM miniature GLB. Every figure used by
`build_palace_of_fine_arts.py` traces back to a source below, or is explicitly
marked as visual inference. The plan dossier in
`docs/asset-plans/palace-of-fine-arts.md` was the starting point; everything it
asserts was re-verified independently, and two of its claims were corrected
(no dome finial; the colonnade is not two mirror-symmetric arcs).

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [Wikidata Q966263](https://www.wikidata.org/wiki/Q966263) | Height **P2048 = 49.4 m**; architect Bernard Maybeck; Beaux-Arts / Roman / Greek style; materials (wood + staff originally, concrete rebuild) |
| [OSM way/288371295](https://www.openstreetmap.org/way/288371295) | Rotunda footprint (187 nodes, surveyed), `height=48`, `building=temple`, `start_date=1915`; centroid **−122.4484012, 37.8029215** (matches the plan anchor exactly) |
| [OSM ways 288371306 / 288371310](https://www.openstreetmap.org/way/288371306) | The two colonnade arms as surveyed `building=roof` outlines, `height=19–20`; each arm ~131 m of centerline, roof band ~5.4 m wide, including the L-shaped end hooks |
| [OSM ways 288371313 / 288371314](https://www.openstreetmap.org/way/288371313) | The two detached terminal boxes at the arm ends, `height=21`, each ~9.6 m across |
| [OSM relation 7471537](https://www.openstreetmap.org/relation/7471537) | The lagoon multipolygon: due EAST of the composition, western shore hugging the rotunda's east base; extends x ∈ [−20, +118] m, y ∈ [−107, +135] m in local frame |
| [Wikipedia — Palace of Fine Arts](https://en.wikipedia.org/wiki/Palace_of_Fine_Arts) | 162 ft (49 m) rotunda; **1,100 ft (340 m) pergola**; 1964–74 demolition and poured-concrete rebuild with steel I-beam dome; Ulric Ellerhusen's weeping women atop the colonnade; eight mural insets under the dome |
| [SAH Archipedia CA-01-075-0036](https://sah-archipedia.org/buildings/CA-01-075-0036) (via search extract) | Rotunda is an open-air **octagon on eight triangular piers** framing arched openings; **paired Corinthian columns on high bases outside each pier** with stepped planters and ovoid urns; hemispherical coffered dome; colonnade bays defined by Corinthian columns; boxy vine boxes atop clustered columns with **colossal weeping maidens at the corners, looking in**; Greek-fret architrave on the entablature |
| [palaceoffinearts.org/history](https://www.palaceoffinearts.org/history) | "Weeping ladies… facing into the tops of the columns", melancholy intent; restoration timeline (1959 Weinberger, 1964 rebuild, 1970 theatre) |
| Wikimedia Commons photos (all viewed): *Aerial view of The Palace of Fine Arts*, *View of colonnade from south-east*, *Blue hour at sunset*, *SF Palace of Fine Arts Dome* (night), *Ellerhusen figures 1915* | Massing proportions, dome shape/color, column groupings, box rhythm, night lighting behavior, lagoon relationship, exhibition-hall crescent behind the composition |

Local frame used everywhere below: meters, origin at the rotunda centroid
(= the manifest anchor), +X east, +Y north (the app's authoring frame).
`osm-footprint-trace.png` in this directory is the surveyed geometry plotted in
this frame (black rotunda, blue north arm, red south arm, orange/green terminal
boxes, light-blue lagoon).

## Verified dimensions and location

- **Anchor**: −122.4484012, 37.8029215 (OSM rotunda centroid; matches plan).
- **Architectural height**: 49.4 m (Wikidata P2048; Wikipedia 162 ft = 49.4 m).
  OSM's surveyed tag says 48 m — the two disagree by 1.4 m; **49.4 m adopted**
  (two independent published sources vs one survey estimate), and the dome apex
  is built exactly to it.
- **Rotunda footprint**: 60.7 × 71.5 m overall bbox; the outline is an
  8-pointed star — octagon faces at apothem ≈ 28 m with pier/planter clusters
  projecting to r ≈ 34–38 m, waist between projections r ≈ 18–22 m.
- **Octagon orientation (measured)**: the eight pier clusters sit at azimuths
  **30° + 45k CCW from east** (radial-maximum analysis of the 187-node
  outline). The through-axis of one pair of opposite arches therefore points
  ~7.5° north of due east — straight at the lagoon.
- **Colonnade arms**: 131 m (N) and 133 m (S) of centerline each, band width
  5.4–5.5 m, entablature top 19–20 m, terminal boxes 21 m (OSM heights).
  Combined with the rotunda gap this is consistent with Wikipedia's 1,100 ft
  total pergola.
- **Lagoon edge**: the west shore runs 10–25 m east of the rotunda's east
  piers and weaves along the arms' concave side. The lagoon itself is park
  data in the app — NOT in the GLB — but the terrace is shaped so the model
  meets its shore plausibly.

## Orientation

Authored with **+Y = true north, +X = east** (the loader applies no rotation).
The composition is a crescent, concave toward the lagoon in the EAST:

- North arm: leaves the rotunda's NW shoulder (−36, 20), sweeps N/NE to
  (−3, 79), runs east to (13, 80), hooks NORTH to (16, 110); terminal box at
  (−3, 105).
- South arm: leaves the SW shoulder (−28, −30), sweeps S/SE to (9, −71),
  runs east to (43, −74), hooks SOUTH to (48, −104); terminal box at
  (30, −102).
- The arms are **not mirror images** — both hooks turn east-then-away, and
  the south arm reaches ~15 m further east. Mirroring them is the immediately
  visible error the plan warned about; the build traces each arm's surveyed
  centerline separately.

## What each side shows

- **East (from the lagoon)** — the hero view: the octagonal rotunda framed
  between the two arms, arch axis pointing at the water, paired columns and
  attic relief band, dome above the treeline, everything doubled by
  reflection. Night: warm uplight on the frieze and colonnade.
- **North / south (along the arms)** — the colonnade in elevation: long rows
  of Corinthian columns under a continuous entablature, punctuated by taller
  4-column box clusters with maiden silhouettes; the rotunda rises behind.
- **West (rear)** — the plainer back: the same octagon and dome, arms seen
  convex-side-on; in reality the giant crescent exhibition hall stands ~20 m
  west and hides much of this view (the hall is a separate OSM building —
  see Scope).
- **Top** — the low dome on its octagonal attic ring, the 8 radial pier
  clusters, and the two curved roof bands with their box rhythm — the single
  most-seen view in the app.

## Recognition cues (ranked)

1. The domed rotunda silhouette above the treeline — an open octagon, not a
   solid building.
2. The muted red-orange dome over warm ochre stone.
3. The two long curved colonnades sweeping away from the rotunda, concave to
   the lagoon.
4. Freestanding giant columns reading as separate cylinders, with chunky
   entablature boxes at intervals.
5. The weeping-maiden boxes — blocky figures at the box corners, facing in.

## Features to preserve

- 49.4 m apex; dome proportion to attic (dome base ≈ r 18 m, rise ≈ 11 m —
  visibly less than a full hemisphere above the tall attic).
- The measured octagon rotation (30° + 45k) and the east-facing arch axis.
- Both surveyed arm centerlines with their asymmetric L-hooks and terminal
  gate boxes.
- Freestanding column rhythm: paired columns at the rotunda piers, double
  rows along the arms.
- The attic band as a distinct, taller, lighter ring (the relief-panel zone).

## Features to simplify

- Corinthian capitals → two-step beveled blocks (no acanthus).
- Zimm relief panels + coffering → flat inset color panels (`Toy_trim` on
  `Toy_sand`).
- Weeping maidens → simple tapered blocky silhouettes at box corners; drop
  entirely from a box if they read as noise at aerial distance.
- Urns/planters between pier columns → low chunky pedestal blocks only.
- Real column count (~4 m real spacing) → wider miniature bays (~6.5 m) so
  columns stay separate cylinders at the app camera.
- The end hooks' wider roof structure → same band vocabulary, no special case.

## Uncertainties and conflicting evidence

- **Height 48 vs 49.4 m** — resolved to 49.4 (see above).
- **Colonnade column count**: no authoritative published count found; one
  tertiary source says "30 Corinthian columns", which cannot cover 260 m of
  double-row pergola and is treated as wrong or partial. The model uses
  rhythm-accurate spacing, not a claimed count.
- **Dome color**: night photos read gold (lighting), daytime aerials read
  muted terracotta/brown-red. Palette maps it to `Toy_ioorange` per the plan;
  this is the composition's saturated accent.
- **Small detached roof way 1104852117** (7×8 m, ~120 m SW): ambiguous
  fragment near the exhibition hall front, not part of the rotunda–colonnade
  ensemble → excluded.
- **Dome finial**: the plan's massing recipe suggested a finial to 49.4 m;
  photographs show the rebuilt dome apex is smooth with no lantern or finial
  → no finial built; the apex itself is 49.4 m.
- **Exhibition hall**: the aerial shows the giant crescent hall reads
  strongly from the air, BUT it is a separate surveyed OSM building that the
  app already bakes procedurally, and the procedural landmark this GLB
  replaces (`palaceOfFineArts()` in `app/src/landmarks.js`) does not include
  it either → excluded to avoid double geometry (scope confirmed in REPORT).

## Scope amendment — grounds (owner directive, 2026-08-10)

After the architecture-only asset passed, David directed the asset to include
the surrounding water and garden (option A: one GLB, with swans). Sources and
decisions for the added grounds:

- **Lagoon**: traced from OSM relation 7471537 — outer ring (159 surveyed
  nodes, RDP-decimated to 50) plus the large island (way 515414933). The 3 m
  islet (way 515414934) is dropped as sub-toy-scale. Water is a flat prism
  (top 0.42 m) in `Toy_glass`, with `Toy_stone` shore rims lofted around both
  rings. Where the surveyed shoreline runs against the rotunda terrace and
  the arm strips, the stone plinths rise straight from the water — matching
  the real east base of the rotunda.
- **Lawn**: a margin-offset, midpoint-smoothed convex hull of the whole
  composition in `Toy_mint` (palette green) — a designed manicured blob, not
  a survey (the real boundary is streets/paths; visual inference).
- **Trees**: 26 grouped toy trees in two silhouette species (conical
  `Toy_pine`, round `Toy_leaf` — off-palette vegetation greens, contract
  WARN) composed from the aerial photo: the dense screen west of both arms,
  groves at the hooks and gates, specimens on the east shore, three on the
  island. Tallest crown 17 m — far below the 49.4 m apex, preserving the
  silhouette hierarchy.
- **Shrubs**: eight beveled masses along the colonnade backs and rotunda
  west base.
- **Swans**: three chunky white swans (`Toy_white`) mid-lagoon east of the
  rotunda — the storytelling props (style bible §16); semantically oversized
  ~1.5×.
- **Night state** (second owner directive, same day): glow surfaces follow
  the night photographs — the real palace is uplit in warm gold, brightest
  on the attic frieze, the cornice at the dome springing, the colonnade
  entablature undersides, and the interior of the open rotunda; the dome
  itself stays a dark silhouette with a lit rim. Modeled as `Toy_gold_Glow`
  on exactly those surfaces plus an uplit interior floor pool, with
  `Toy_white_Glow` kept only for the apex crown ring. Emission ships at 0
  (the app's night pass drives it); `--night` renders preview it at 6.0.
