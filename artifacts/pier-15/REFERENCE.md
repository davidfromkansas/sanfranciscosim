# Pier 15 (Exploratorium) — reference dossier

Research and verification record for the miniature GLB. The plan behind this
asset is `docs/asset-plans/pier-15.md`; this file records what was verified in
the build session, the sources, and the design decisions taken. All heights are
above the WATERLINE (Z = 0); the deck sits at 3.05 m.

## What was verified this session

| Fact | Value | How |
|---|---|---|
| Footprint (deck) | OSM way 1390720125, 18,441 m2, OBB 245.0 x 94.8 m, axis 54.9° | Overpass, reprojected with the app's tangent projection |
| Footprint (shed+bulkhead+observatory) | OSM way 25478444, 13,301 m2, shed walls 54.7 m apart | same |
| Anchor | -122.3974662, 37.8016046 = deck polygon area centroid, over open water | shoelace centroid |
| Bulkhead gable crest | 16.4 m above water (13.3 above grade) | Street View pano `kxhcO1Z21OvTtJA4wdYHZg` (2025), photogrammetric solve; camera position verified two independent ways (pavilion bearing + SE corner column); person-height cross-check 1.82 m |
| Arch crown / wing parapet | ~11.0 m above water each | same solve |
| Monitor ridge | 13.9 ± 0.8 m above water | second pano `2OZhgFbvl-4wmtDZpfAZcw` (2022), sight-ray intersection with the monitor's plan line |
| Shed wall top | ~8.5 m above water | same |
| Monitor plan position | centreline ~7.5 m SE of today's shed centreline (t = 9.0 in the pier frame), over the 1931 central aisle | Google z20 aerial (Aug 2026) rectified into the shed's axis frame; matches the 1955 north-widening history |
| Roof layout | 3 longitudinal PV bands + monitor band, pale walkway seams, cross-platforms at ~55 m stations | same rectified aerial |
| Bulkhead composition | central gabled pavilion, monumental arch, tapering piers, "PIER 15" raised letters, white Exploratorium "O" on the fanlight, 2 window bays per wing, flagpole on the gable | 2025 pano + National Register nomination pp. 131-135 |
| Shed construction | 1931 steel frame, precast scored concrete walls, clerestory steel sash, roll-up door bays, canopies both flanks | nomination + 2022 pano |
| Bay end | Observatory Building (2013, glazed, 2 storeys, PV roof + square skylight) at the north corner; Observatory Terrace between it and the shed's original narrow east bays; faintly Art Deco shed end wall | Port project sheet, Architectural Record, z21 aerial |
| Water courtyard | deck notch along the NW flank kept open (valley paved area removed 2010-13) | Port project sheet + aerial |

## Primary sources

- National Register nomination, Embarcadero Historic District, Section 7
  (sfport.com, pp. 131-135) — the 1931 construction record: shed 823 x 123 ft,
  pier 794 x 160 ft, monitor over the central aisle, bulkhead composition,
  H. B. Fisher / Frank G. White (BSHC), the 1955-56 widening and quay joining
- NPS: nps.gov/articles/pier-15-ca.htm — 1931, 5,874 solar panels, net-zero
- Port of SF project sheet (450-ExplorPROJECT-December2010.pdf) — EHDD, Page &
  Turnbull, Observatory Building, water courtyard, $205M, opened 2013
- Architectural Record 2831 (2013) — stripped patinated exterior, redone stucco
  entrance, Bay Observatory Gallery and Terrace
- ENR / AIA Top Ten / HPB case study — 1,126 pilings repaired, 1.3-1.4 MW PV,
  93% of envelope retained, south-tilted low-slope roof, rooftop monitor
- OSM ways 25478444 / 1390720125; Google z20/z21 satellite (Aug 2026); official
  Street View panoramas kxhcO1Z21OvTtJA4wdYHZg (2025) and 2OZhgFbvl-4wmtDZpfAZcw
  (2022)

## Recognition cues (ranked, from the plan)

1. The PV-wrapped roof with the offset glazed monitor
2. The bulkhead pavilion: gable, "PIER 15", tapering piers, arch + white "O"
3. The open water courtyard between Piers 15 and 17
4. The glazed Bay Observatory at the bay end
5. The long low silhouette at 54.9° with the gable as the only tall element

## Design decisions (deviations & simplifications, all deliberate)

- **No flagpole.** The real pole tops ~22.6 m; modelled at true height it
  becomes the bbox top and shrinks the pier ~27% under targetHeightM
  normalisation. The crest cap at 16.4 m is the architectural top.
- **"O" enlarged** to 5.1 m outer diameter (real ~4 m) and kept low so its whole
  interior reads glazing; "PIER 15" letters 1.10 m proud blocky caps on a
  shallow arc — the only text on the asset. Neither glows at night.
- **Roof PV as 3-4 broad bands** with pale seams and three cross-platform
  breaks, not 5,874 modules. Monitor gets glazed cap slopes so it reads as a
  lightband from the aerial camera.
- **Shed walls carry one clerestory strip + four door bays with canopies per
  flank** in place of seventeen roll-up doors and scored panel joints.
- **East end Art Deco wall** reduced to a central gabled proud plane + four
  pier strips.
- **The 9 m floating-dock cove and sub-2 m survey doglegs** in the OSM deck
  ring are merged; the water courtyard notch and both apron widenings are kept.
- **Group-entry pavilion** (the dark charcoal gateway on the forecourt's NW
  flare, old Terminal Office site) modelled as a low ink box with a pale sign
  band — it anchors the valley-gate view.
- **Not modelled:** vessels, water-taxi float, courtyard pedestrian bridges,
  the Buckyball sculpture (on the seawall, not the pier), F-line furniture,
  people, cars.
- **Corrections to the plan discovered while building:** the plan's predicted
  AABB of "~250 x 178 m" was a rotation-math slip — the correct expectation for
  a 245 x 94.8 m OBB at 54.9° is ~249 x 221 m, which is what the build
  measures. The monitor centreline sits at t = +9.0 (7.5 m SE of the shed
  centreline), used in place of the plan's provisional "t = 11".

## Night design

Hero: the monitor's glazing strips both sides plus glazed cap slopes
(`Toy_glassl_Glow`) — the pier reads as one warm lit line riding a dark roof,
which is exactly how the real museum reads across the water. Supporting: an
amber arch-outline band inside the voussoirs (a filled fanlight panel washed
the glazing warm at the app's 12% day alpha — rebuilt as a quad-strip band);
the observatory's upper band; two lit wing bays. Accents: apron light
standards as amber points; the entry pavilion's warm doorway. The PV panels,
the "O" and the lettering do not glow.
