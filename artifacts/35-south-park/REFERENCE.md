# 35 South Park (Accel) — reference dossier

Research behind `35-south-park.glb`. Where this file and
`docs/asset-plans/35-south-park.md` differ, **this file and `REPORT.md` win** —
they record what was verified while modelling.

Compiled 16–17 August 2026.

## 1. What the building is

A 1920 industrial building on the **north-east arc** of the South Park oval,
block/lot **3775 / 102**, carrying the grandest street elevation on the park: five
giant round-arched bays in smooth pale ashlar under a rope-enriched architrave, a
lettered frieze, a projecting cornice and a tall blank parapet. Since a ground-up
renovation completed in 2023 it also carries a **continuous clipped hedge along the
whole front parapet** and a **set-back penthouse** behind it. It is **Accel's San
Francisco office**.

| Item | Value | Confidence |
|---|---|---|
| Address | 35 South Park, SF 94107 (Google Maps labels the frontage "33 S Park St") | **verified** — OSM way/112759864, every building permit, and Accel's own contact page |
| Built | 1920 | **verified** — SF Assessor roll, identical 2007–2025 |
| Assessor class / storeys | Industrial, 3 storeys | **verified** (roll); see §5 for the storey conflict |
| Building area / lot | 16,420 sq ft on 8,197 sq ft — FAR exactly 2.0 | **verified** — SF Assessor roll, constant 2007–2025 |
| Tenant | Accel | **verified** — `accel.com/contact-us`; OSM node 11020498922 |
| 2023 renovation | Perkins&Will, "South Park Venture Capital Firm", 16,420 sq ft, completed 2023 | project **verified**; its identification with this building **inferred** (§5) |
| Footprint | 791.2 m²; 22.72 m frontage × 35.80 m deep, with a 7.96 × 2.44 m notch out of the rear south-west corner | **measured** — OSM way/112759864 via Overpass, reprojected |
| DataSF cross-check | `SF3775102`, 750.4 m², centroid 1.36 m from the OSM anchor | **measured** |
| Anchor | −122.3933378, 37.7815714 (oriented-bounding-box centre) | **measured**; polygon area centroid 0.42 m away |
| Arcade heading | outward **315.9° (NW)**; party wall 225.5°, flank 45.5°, rear 135.8° | **measured** |
| Party wall | 41–43 South Park, gap **0.00 m**, south-west | **measured** (OSM way/112759867) |
| Side gap | 27 South Park, **7.34 m**, north-east | **measured** (OSM way/112759868) |
| Parcel address range | **35 to 35** — one address on block/lot 3775/102, so no sibling-scope conflict | **verified** — DataSF parcels `acdm-wktn`; Google's "33 S Park St" is its own geocoding, not a second address |
| Historic status | **none** — not a contributor to the NR South End Historic District (that district reaches South Park only at 1 South Park / 570 Second Street) | **verified negative**, 2008 nomination searched in full |
| Architect (1920) | not recorded in any source consulted | — |

## 2. The height ladder, and how it was measured

DataSF's LiDAR is a **2010** product and this building grew between 2020 and 2023
(permit 202008222419, "tenant improvement; new penthouse level", and its 2023-04-14
deferred submittal, "roof trellis and associated structural and penthouse deck").
The LiDAR therefore describes a building that no longer exists, and the ladder below
is **photogrammetric**, from the Jan 2025 Street View captures.

Method: ratios of tangents against a known camera geometry. From the near pano
`41nfDporXIT_NIfYe40GRQ` at `37.7817137, −122.3935663`, rendered at 1400 × 1000 with
a 90° vertical fov and a 105° tilt, so `f = 500 px` and
`elevation(y) = 15° − atan((y − 500) / 500)`. The perpendicular distance from that
pano to the facade plane is **7.48 m**, computed from the OSM ring. Solving
`h = h_cam + D·tan(e)` with the wall base pinned to 0 gives `h_cam = 2.38 m` — within
0.12 m of Street View's nominal ~2.5 m camera height, which is what validates the frame.

| feature | viewport y | elevation | height (sidewalk datum) |
|---|---|---|---|
| wall base at the sidewalk | 820 | −17.6° | 0 (datum) |
| water table | 737 | −10.4° | **1.0 m** |
| architrave / rope band | 303 | +36.5° | **7.9 m** |
| parapet crest | 215 | +44.7° | **9.8 m** (±0.25) |

Repeating on the across-the-park pano at `≈37.78196, −122.39384` (D = 43.68 m, fov 28°,
tilt 101°) and calibrating `h_cam` against the same parapet gives parapet 10.4 m,
hedge crest 10.9 m, penthouse crest 13.7 m. Taking the two frames' spread as the error
band lands on the shipped ladder:

| element | shipped | source |
|---|---|---|
| water table | 1.00 m | photogrammetric |
| arch springing | 5.20 m | photogrammetric proportion |
| arch crown | 6.60 m | derived (semicircle on a 2.80 m opening) |
| architrave (rope band) | 7.78–7.98 m | photogrammetric, 7.9 m |
| frieze top | 8.85 m | photogrammetric proportion |
| cornice top | 9.30 m | photogrammetric proportion |
| roof deck | 10.00 m | derived; DataSF `hgt_majoritycm` 10.87 m in the LiDAR datum |
| parapet crest / coping | 10.40 m | photogrammetric, both frames |
| hedge crest | 11.30 m | photogrammetric, *estimated* |
| **penthouse crest** | **13.40 m** | photogrammetric, ***estimated***, ±0.7 m |

**The consistency check that matters**: at 7.48 m the penthouse is *hidden* behind the
parapet (elevation 32° against the parapet's 47°) and at 43.68 m it is *visible above*
it (12.0° against 10.4°). That is exactly what the two captures show, so the penthouse
is genuinely set back and genuinely taller than the parapet.

DataSF LiDAR for the record: deck majority 10.87 m, median 10.49 m, maximum 12.44 m,
ground 11.71 m NAVD88. Its ground datum is the *lowest* cell under an outline that
overlaps the street, so it sits ~1 m below the sidewalk at the front door — which is
why every LiDAR figure reads about a metre high against the ladder above.

## 3. What each side shows

- **North-west (South Park arcade), 22.72 m — the hero, photographed in detail.**
  Plinth/water table to 1.0 m; five giant round-arched bays at 4.544 m centres with
  plain moulded archivolts springing from simple imposts and fine steel sash with a
  radial fan in the head; a plain circular roundel on each interior pier just below
  the entablature; a twisted rope band; a frieze whose raised letters have been
  removed (only their shadows survive — "C … O … O" is as much as the 2025 capture
  resolves); a projecting cornice; a tall blank parapet. Modern cylindrical
  glass-and-black-metal sconces on the piers, and warm ring chandeliers visible
  inside through the glass. **Smooth pale ashlar, not raw brick.**
- **North-east flank, 35.6 m** — onto the 7.34 m gap to 27 South Park. Not
  photographed by anything consulted; modelled plain, with the entablature carried
  round.
- **South-west, 33.3 m** — party wall with 41–43 South Park (a dark-red Victorian
  with bay windows). **Blank**: a party wall cannot carry openings. Verified.
- **South-east (rear), 14.76 m + 7.96 m with a 2.44 m notch between** — not
  photographed; service elevation onto the block interior.
- **Top** — a bright light-grey membrane, conspicuously brighter than every
  neighbouring roof in the Esri nadir; the hedge band along the whole front parapet;
  the set-back penthouse on the south-west half with a band of four roof lights facing
  the park; loose roof lights on the north-east half; mechanical plant and a hatch at
  the rear; the notch biting in at the rear south-west corner.

## 4. Recognition cues, as built

1. Five giant arches in pale ashlar — the identity, and unmistakable from the park.
2. Four roundels under the entablature.
3. The green hedge line along the parapet — unique on this block; the roof's identity.
4. The cornice–frieze–parapet cap: 2.5 m of heavy horizontal over a 7.9 m light arcade.
5. The set-back penthouse with its roof-light band.
6. Low, wide, flat-topped, at 45.5° to the world grid, blank on the south-west.

## 5. Uncertainties and conflicting evidence

- **The penthouse crest is the weak number and it is the one the loader divides by.**
  13.40 m is photogrammetric with a ±0.7 m band whose largest term is the penthouse's
  setback from the front parapet (assumed 8 m off a nadir aerial; at 5 m the crest is
  12.6 m, at 12 m it is 14.1 m). It is driven from a single named constant `Z_CREST`
  in the build script and asserted in the validator, so a corrected value is a one-line
  change. A tilted aerial would settle it; Google's 3D/45° view would not engage in the
  available browser.
- **Storey count.** The assessor says 3 every year from 2007; the permits say 2 existing
  until 2020 and 3 from 2021. But `property_area` is 16,420 sq ft on an 8,197 sq ft lot
  — exactly 2.0 — for all nineteen years, and the street elevation is a single giant
  order about 10 m tall. Read as **two tall interior levels behind one giant order**,
  with the 2020–23 works adding the penthouse. It does not change the exterior, and the
  arcade is deliberately **not** subdivided into two window rows.
- **The Perkins&Will attribution is inferred, not stated.** Their project page names no
  address and its client is "Confidential". The chain is: OSM and Accel both put Accel
  at 35 South Park; the assessor records 16,420 sq ft for block 3775 lot 102;
  Perkins&Will's "South Park Venture Capital Firm" is 16,420 sq ft in a brick-clad
  1920s South Park building completed 2023; and the permit record shows a 2020–23
  ground-up interior renovation at this lot. Strong, but a triangulation. Nothing in
  the model depends on it.
- **"Brick-clad" does not match the photographs.** Perkins&Will describe a brick-clad
  building; the street elevation is smooth pale ashlar with cast-stone mouldings and no
  visible brick. Both can be true — the flanks and rear of a 1920 SoMa warehouse are
  almost certainly brick and only the street face got the stone order. The model uses
  `Toy_stone` throughout and treats the unphotographed flanks as plain rendered masonry.
- **The frieze inscription is unread.** The raised letters are gone; only shadows remain.
  Deliberately not modelled — ghost lettering cannot survive flat-colour materials.
- **The bay count (five) was counted through winter foliage** on two Jan 2025 captures.
  Five over 22.72 m gives 4.544 m centres, which is a credible bay for this order.
- **The notch is measured in plan and unknown in section.** Modelled as a full-height
  void: right at the roof, which is what the camera sees, and defensible at ground level.
- **The roundels may also appear on the two end piers.** Only the four interior piers
  are modelled; the end piers are narrow and no capture resolves them cleanly.

## 6. Sources

- OSM way/112759864 (footprint, address, `height=10` — a low shell tag, not used);
  ways 112759867 (41–43), 112759868 (27); node 11020498922 (Accel)
- DataSF Building Footprints `ynuv-fyni` → `SF3775102`; Assessor rolls `wv5m-vpq2`;
  Building Permits `i98e-djp9` (40 permits, block 3775 lot 102)
- `accel.com/contact-us`
- `perkinswill.com/project/south-park-venture-capital-firm/` and
  `officesnapshots.com/2026/02/03/south-park-venture-capital-firm-offices-san-francisco/`
- Google Street View, Jan 2025: pano `41nfDporXIT_NIfYe40GRQ` (`37.7817137, −122.3935663`),
  plus panos at `≈37.78196, −122.39384` and `≈37.78185, −122.39330`
- Esri World Imagery, nadir z20 (~0.118 m/px), tiles 167789–167793 / 405269–405273
- `sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf`
- `docs/asset-plans/2-south-park.md`, `168-south-park.md` — district material language

**Excluded on purpose** (Exa's summariser attached all three to this address; none of
them belongs to it): LDP Architecture's "One South Park" (that is 1 South Park, and the
"35" in its description is a *unit count*); PCAD's Phelan Building (Third Street end,
1897); HSE Architects' "Accel Financial Staffing" (a different company, different city).
