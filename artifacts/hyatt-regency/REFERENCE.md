# Hyatt Regency San Francisco — reference dossier

Compiled 18 August 2026 for `artifacts/hyatt-regency/`. The plan
(`docs/asset-plans/hyatt-regency.md`) was written in the same session and its
Part 2 is the long form of this dossier; what follows is the modelling-facing
subset plus the corrections made while building.

## 1. Identity

| | |
|---|---|
| Building | Hyatt Regency San Francisco, 5 Embarcadero Center, SF CA 94111 |
| Architect | John C. Portman Jr. / John Portman & Associates |
| Built | constructed 1971, opened May 1973 |
| Structure | all-steel frame (CTBUH) |
| Rooms | 802 (architect) / 804 (Wikipedia); GBA 837,382 sf, site 84,000 sf |
| OSM | way/28319370, 6,672 m2, `height=83`, `building:levels=20` |
| Wikidata | Q5952911 |

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| CTBUH Skyscraper Center #16108 | **80.8 m / 265 ft to architectural top**, 20 floors, all-steel |
| DataSF LiDAR `ynuv-fyni` | max 80.64 m; the two-footprint split that proves the section (see §4) |
| portmanarchitects.com project page | "wedge-shaped design **steps back to open the plaza to the bay**"; 17 stories; 802 rooms; site and GBA |
| PCAD entry 3413 | 1971 construction, May 1973 opening, "Piranesian" triangular atrium 300 x 170 x 170 ft |
| Wikipedia | 77 m/253 ft (rejected, see §3), 804 rooms, Guinness lobby record, `Eclipse` sculpture, former Equinox revolving restaurant |
| OSM way/28319370 via Overpass | the surveyed footprint used for the plan |
| Commons `Hyatt Regency San Francisco (110103874).jpg` (2021-05-08) | the long elevation from Embarcadero Plaza: fin wall, diagonal roofline, podium eave |
| Commons `Hyatt Regency San Francisco 01.JPG` | the Equinox pavilion (drum + two cantilevered frames) and the stepped Drumm-Street corner |
| Commons `Five Embarcardero Center.jpg` | the wedge silhouette from the bay |
| Commons `160205-G-XX113-060.jpg` (USCG) | the terrace field and the blank plaza prow, from a low aerial |
| Commons `...(Unsplash).jpg` | facade detail: pale slab bands, vertical-bar balcony railings |
| Commons `2008 Olympic Torch Relay ... Justin Herman Plaza 69.JPG` | the podium arcade at eye level: deep piers, glazed base, canopy |
| Google / Esri satellite z19-z20, stitched with the OSM ring overlaid | the terrace field's plan extent, the wing roof band, the Equinox position, and the shadow measurement in §4 |

## 3. Height

Three published figures disagree. The decision and its evidence:

- **80.8 m / 265 ft — CTBUH "height to architectural top". USED.**
- 80.64 m — DataSF LiDAR maximum over the southern footprint. An independent
  instrument agreeing with CTBUH to **0.16 m**. This is what settles it.
- 77 m / 253 ft — Wikipedia. Best explained as the guest-room wing's roof deck
  plus parapet (*inferred*); it is 3.8 m under both measurements above.
- 83 m — the OSM `height` tag, no cited basis. Rejected.

Eave vs crest, recorded explicitly as the pipeline requires: **eave (wing roof
deck) 72.0 m, parapet 73.4 m, crest (Equinox upper frame) 80.8 m.** The model's
bbox top is the crest.

The floor count also disagrees — CTBUH and OSM say 20, the architect says 17.
Both are true of a wedge: 20 levels exist at the Market Street face, 17
guest-room levels sit in the stepped mass. Neither figure is a height input.

## 4. Orientation, plan and section

Building axes: **u** along the Market Street frontage at bearing **45.8 deg
true**, **v** perpendicular and positive toward Market (135.8 deg). Origin at
OSM node lon `-122.3958136`, lat `37.7944765`.

The 33-node OSM ring reduces to seven points at **6,663 m2** against the surveyed
6,672 (0.13% error). Edges and outward normals:

| edge | length | outward normal | what it is |
|---|---|---|---|
| P0->P1 | 95.61 m | 135.8 | Market Street — full-height fin wall |
| P1->P3 | 23.58 m | 45.8 | the Embarcadero Plaza prow — full-height, near-blank |
| P3->P4 | 102.23 m | 351.2 | the Embarcadero Center frontage — the terrace field |
| P4->P5 | 20.52 m | 273.2 | Drumm Street (upper) — terraced |
| P5->P6 | 61.49 m | 257.5 | Drumm Street (lower) — terraced below, fin wall above |
| P6->P0 | 38.84 m | 160.9 | the Market/Drumm end — full-height fin wall |

The Market frontage and the Embarcadero Center frontage **converge at P1-P3**, so
the plan is a wedge as well: 23.6 m deep at the prow, 82.7 m at Drumm.

**Which way the wedge falls** was the hardest question in this research and the
one most likely to be got wrong, because plausible camera solutions for the
ground-level photographs gave opposite answers. Three independent lines settle it:

1. The architect's own description — "steps back to open the plaza to the bay".
   The plaza is north-east of the hotel.
2. **DataSF splits this building into two LiDAR footprints**, and their statistics
   are the section:

   | ring | area | max | median | min | position |
   |---|---|---|---|---|---|
   | `201006.0000636` | 3,211 m2 | 80.64 m | 60.22 m | 11.07 m | south (Market half) |
   | `201006.0000477` | 3,730 m2 | 74.78 m | 39.72 m | 0.27 m | north (terraced half) |

   A median roof of 60.2 m on the Market side against 39.7 m on the far side is a
   wedge falling away from Market.
3. A shadow measurement on the Google z20 imagery (sun azimuth ~130 deg; the
   building's shadow reaches ~15 m past the north-west frontage) puts that outer
   edge at **~11 m** — the southern ring's LiDAR minimum of 11.07 m, to 0.1 m.

If a future pass finds evidence against this, the massing flips and must be
rebuilt, not patched.

## 5. What each side shows

- **South-east (Market Street).** One vertical plane of deep precast piers with
  narrow recessed window slots, unbroken from the podium eave to the roof
  parapet. No setbacks or balconies on this face.
- **North-east (the plaza prow).** The wedge's point: a tall, almost blank pale
  end wall meeting the fin wall at a sharp arris. The one large unfenestrated
  surface on the building.
- **North-west (Embarcadero Center).** The terrace field — floor plates stepping
  down and back, each slab edge a pale band over a dark recessed balcony.
- **West (Drumm Street).** The cut end of the wedge: a giant staircase of slab
  edges with the service core rising past them to the Equinox pavilion. The hotel
  entrance and the HYATT lettering are here.
- **South-west (Market/Drumm).** Full-height fin wall matching Market, with the
  Equinox pavilion directly above.
- **Top.** A triangular field of stepped slabs bounded by the flat wing roof
  along Market; the wing roof carries a clerestory ridge and round mechanical
  units; the Equinox frame oversails at the Drumm end.

## 6. Recognition cues (ranked)

1. The stepped wedge — terraces falling from a full-height Market wall to a
   two-storey podium.
2. The triangular plan with the sharp prow on Embarcadero Plaza.
3. The Equinox pavilion: a drum under a cantilevered rectangular concrete frame,
   sitting off-centre at the Drumm end.
4. Deep precast piers with narrow window slots — brutalist grey concrete.
5. The continuous podium eave.

## 7. Preserved / simplified / dropped

**Preserved:** the true footprint (to 0.13% on area) and its 45.8 deg heading;
the wedge in plan and section; the full-height/terraced split by face; the
Equinox pavilion's off-centre position; the podium eave line.

**Simplified:** 17 guest levels become 15 terraces at 4.0 m (semantic scale,
§9 of the style bible — the wedge angle is preserved); the pier rhythm becomes
3.2 m on centre with 2.15 m piers; the Equinox frame becomes two stacked
rectangular rings; the podium becomes plinth / recessed arcade / band / eave.

**Dropped:** the atrium (invisible from outside — its glass is the night-glow
hero instead); balcony railings; the Embarcadero Center bridges, ramps and
planters; six sub-4 m jogs on the Drumm frontage (OSM nodes 25-28) and a 6.9 m
stub at the Market/Drumm corner (node 0).

## 8. Uncertainties

1. **Equinox frame dimensions.** The 32 x 27 m upper ring and its 6 m oversail
   are *inferred* from the Drumm/California photograph, not from a drawing.
   They set the bbox top, so an error here is an error in the shipped height.
   Its plan position (u -38.0, v +18.0) is measured off Google z20 imagery to
   about +/- 4 m.
2. **Terrace count** (15 at 4.0 m) is a design decision, not a survey.
3. **Podium height** (12.0 m) is *inferred* from the podium's two storeys in the
   plaza photographs and from the ~11 m LiDAR minimum on the Market ring.
4. **Concrete colour.** Photographs run from pale beige-grey in low sun to a
   fairly dark warm grey in shade. `Toy_stone` (d9d2c2) is the palette's warm
   light grey and reads correctly against the app's neighbours; the real building
   is a shade darker.
