# 2 South Park (544 Second Street) — reference dossier

The 1923 Kohler Co. plumbing-supply warehouse at the corner of Second Street and
South Park: three storeys of unreinforced brick with a pier-and-spandrel grid of
enormous steel industrial sash, seismically retrofitted 1992–2000, now retail
over office with the Blue Bottle Coffee South Park café in its corner
storefront.

Compiled 16 August 2026 for `artifacts/2-south-park/`, executing
`docs/asset-plans/2-south-park.md`. Everything below was re-verified from
primary sources during this build rather than inherited from the plan; where the
build corrected the plan, `REPORT.md` says so.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, blklot 3775005 | The surveyed lot: 29.81 x 20.91 m, 622.9 m2, bearing 45.2°/225.2°, area centroid `-122.3932364, 37.7824236`. This is the anchor and the modelled footprint. |
| OSM way/112926339 | Cross-check footprint 29.77 x 21.27 m, 629.9 m2, bearing 45.6°; `addr:housenumber=2`, `addr:street=South Park`, `height=13` |
| DataSF Building Footprints `ynuv-fyni`, SF3775005 | Heights: `hgt_max` 17.72 m, `hgt_median` 12.83 m, `hgt_mean` 12.84 m, `hgt_majority` 12.77 m, `hgt_min` 3.51 m, `hgt_std` 1.12 m, `gnd_min` 14.05 m NAVD88, 2,613 cells at 50 cm. Cross-check footprint 29.69 x 22.11 m |
| SF Assessor secured roll `wv5m-vpq2`, 3775-005 | Built **1923**; 3 storeys; lot 6,734 sq ft; use code IND (stale); last sale 21 Jun 1996 |
| SF Building Permits `i98e-djp9`, block 3775 lot 005 (56 permits) | Storey count, construction type, the UMB retrofit sequence, the roof works and the roof penthouse — see §2 |
| ArchDaily 898515 / Dezeen (7 Jun 2017), Bohlin Cywinski Jackson project text | "a former Kohler warehouse"; "a nearly century-old brick structure that once housed a Kohler plumbing supply warehouse"; "original brick walls and heavy timber support columns" |
| SF Weekly (18 Nov 2016), Blue Bottle Coffee Lab (14 Nov 2016), Sprudge (13 Mar 2017) | The café opened Nov 2016 at 2 South Park "in the former home of Jeremy's department store"; 1,200 sq ft; "blonde wood, red brick, and exposed ceiling beams" |
| LoopNet, 2 South Park St / 544 2nd St, APN 3775-005 | 18,421 sq ft, built 1923 |
| Google Street View, May 2025 (panos near `37.78257,-122.39307` and `37.78252,-122.39300`) | **The Second Street elevation and the corner**, observed |
| Google Street View, Jan 2025 (pano near `37.78228,-122.39312`) | **The South Park elevation**, observed |
| Google Maps satellite, Vexcel Imaging 2026, near-nadir at max zoom | **The roof**: light membrane, the set-back penthouse with a skylight beside it, the mechanical group along the Taber Place edge, the corner flagpole |

No copyrighted imagery is committed. The panorama coordinates above reproduce
each observation exactly.

## 2. The permit record, which does most of the work here

| Permit | Date | What it establishes |
|---|---|---|
| 9205717 | 1992 | parapet bracing — there is a parapet |
| 9612839 | 1996 | "to comply with umb ordinances", $150k — **unreinforced masonry building** |
| 9413382 | 2000 | "umb", $950k — the main retrofit |
| 200204043134 | 2002 | eight canvas awnings — **gone by 2025, not modelled** |
| 201605096890 | 2016 | "install coffee bar millwork" — the Blue Bottle fit-out |
| 201601076539 / 201709016719 | 2016 / 2017 | 2nd- and 3rd-floor office tenant improvements |
| 201709016716 | 2017 | "addition of new skylight and gas flue and new mech unit bracing on roof" — **the skylight, flue and roof plant are permit-confirmed** |
| 201810163246 | 2018 | "ground thru roof elevator. machine room changed fro gr fl to **e penthouse on roof**" — **the roof penthouse is permit-confirmed to pre-exist** |

Storeys: 3 in every permit from 1996 onward and in the Assessor's roll. Two 1992
permits say 2 and one 2017 electrical permit says 4; both are outliers (see
`REPORT.md` §4).

## 3. Verified dimensions, location and orientation

- **Anchor:** `-122.3932364, 37.7824236` — DataSF surveyed parcel 3775-005 area
  centroid. Model origin, min Z = 0, XY centre offset 0.000 m.
- **Footprint:** 29.8 m x 20.9 m rectangle at bearing 45.2°/225.2°. Modelled
  corners in Blender metres about the anchor:
  `N (3.15, 17.93)`, `W (-17.93, -3.15)`, `S (-3.15, -17.93)`, `E (17.93, 3.15)`,
  CCW in the order N → W → S → E.
- **Heights:** roof deck 12.83 m (LiDAR median), parapet coping 13.58 m
  (derived), penthouse crest **17.72 m** (LiDAR max) = bounding-box top =
  `targetHeightM`, so the loader's scale lands at 1.0.
- **Axis-aligned bbox:** 36.30 x 36.30 x 17.72 m. The 36 m is the diagonal of a
  29.8 x 20.9 m rectangle at 45°, not a scale error.
- **Orientation:** authored in true-world orientation (Blender +Y = north,
  +X = east). The Second Street front faces NE, bearing 45.2°; South Park SE,
  135.2°; the party wall SW, 225.2°; Taber Place NW, 315.2°.

Three independent surveys agree: parcel 29.81 x 20.91 (622.9 m2), OSM
29.77 x 21.27 (629.9 m2), DataSF LiDAR 29.69 x 22.11 (651.7 m2), bearings within
0.4°, centroids within 2.9 m. The building fills its lot.

## 4. Observations, side by side

**Northeast — Second Street (20.9 m, 4 bays), observed May 2025.** Red-brown
brick piers roughly 1 m wide; between them, on floors 2 and 3, very large
multi-pane steel sash in dark frames that nearly fill each bay, with light
cast-stone sills and lintels running continuously between the piers. A further
light band caps the ground floor and another runs beneath the plain brick
parapet, so the elevation reads as four brick verticals crossed by three or four
pale horizontals. Ground floor: a dark storefront band — the Blue Bottle café at
the South Park corner end (people inside, tables on the sidewalk), a recessed
timber-panelled entry with a small canopy near the middle, another glazed bay,
and a dark entry at the Taber Place end (marked FOR LEASE in the May 2025
capture). No cornice bracket work; this was a utility building.

**Southeast — South Park (29.8 m, 6 bays), observed Jan 2025.** The long face
onto the oval and the one the city sees. Six bays of the same grid at almost
exactly 5.0 m centres; the upper two floors are nearly all glass. A black steel
fire escape descends floors 2 and 3 toward the party-wall end. Ground floor: a
run of dark-framed shopfronts, several papered over or blanked white in the Jan
2025 capture, with a dark recessed entry near the party-wall end.

**Southwest — party wall (20.9 m).** Blind. The South Park neighbour is about
12 m tall (OSM), so nearly this building's full height. No openings.

**Northwest — Taber Place (29.8 m, 6 bays).** *Inferred.* The alley elevation
was not cleanly photographed — the nearest Street View panorama resolves onto a
facade across the alley. Assumed to carry the same pier-and-sash grid on the
same rhythm, over plain brick rather than shopfronts. Loading doors would be
unsurprising on a warehouse's alley face and are the most likely correction.

**Top — observed, Vexcel 2026 nadir.** A flat **light-grey** membrane roof with
seams running NE–SW. A raised penthouse toward the Taber Place half with a
bright glazed skylight beside it; a cluster of mechanical units (rectangular
boxes plus two or three round fans) grouped along the northwest edge near it; a
few small raised boxes near the Second Street parapet; the rest empty. A
flagpole flying a US flag stands at the East corner on the parapet.

## 5. Recognition cues (ranked)

1. **The corner** — two brick elevations of industrial sash turning a right
   angle at the head of the South Park oval. Nothing else at this end of the
   park does that.
2. **The pier-and-sash grid** — a glass-to-brick ratio that is extreme for 1923
   and is what makes it read as a warehouse rather than a loft apartment block.
   Four bays northeast, six southeast, six northwest.
3. **The pale banding** — cast-stone sill, spandrel and lintel courses crossing
   the red brick at every floor line, plus the coping.
4. **Three storeys, flat-topped**, level with its neighbours, with the penthouse
   the only thing breaking the parapet.
5. The dark storefront band and the black South Park fire escape.

## 6. Preserved / simplified

**Preserved:** the surveyed footprint and its 45.2° heading; the corner
condition (three public faces, one blind party wall); the bay counts 4/6/6; the
continuous pale bands at every floor line; the flat roof with its set-back
penthouse, skylight and grouped plant; the light membrane.

**Simplified:** each multi-pane sash becomes one recessed glazed panel in a
single dark frame ring — the *size* of the opening is the cue at the app's
camera, not its subdivision; shopfronts become one dark glazed opening per bay;
the fire escape becomes two solid-sided decks and one diagonal stair with no
balusters; roof clutter becomes one penthouse, one skylight, three boxes, two
fans and one flue; brick becomes flat colour.

**Deliberately omitted:** the roof flagpole (plan 2.10 — it would put the
bounding-box top on a fixture and rescale the whole model against it, and it is
sub-pixel at the app's camera); the 2002 canvas awnings (removed in reality);
signage and tenant fit-out.

## 7. Uncertainties and conflicting evidence

- **The 17.72 m LiDAR maximum** is 4.89 m (4.4σ) above the 12.83 m median. Read
  here as a ~4.1 m stair/elevator penthouse above a 13.58 m parapet, on the
  strength of permit 201810163246 and the nadir aerial. The competing reading is
  street-tree canopy over the Second Street parapet; the 3.51 m LiDAR minimum is
  the matching edge artifact at the other end. Contained risk: the crest is
  authored at exactly 17.72 m, so an error here makes the penthouse too tall
  without making the building too tall. See `REPORT.md` §4.
- **The parapet at 13.58 m is derived**, not measured: LiDAR median plus a
  conventional parapet, cross-checked against `height=13`.
- **The Taber Place elevation is inferred**, as above.
- **The three surveys' centroids differ by up to 2.9 m.** The parcel centroid was
  chosen over the DataSF LiDAR centroid used for 165 and 188 South Park; the
  reasoning and the exclusion arithmetic are in the plan's 2.13.
- **Historic status unresolved.** No Article 10 designation found; the National
  Register South End Historic District boundary was not confirmed to reach block
  3775. Affects nothing about the model.
