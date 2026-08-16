# 181 South Park — reference dossier

Compiled 13 August 2026 for the SF-SIM miniature GLB. This is the executing
side's own record: what was verified, what was corrected in
`docs/asset-plans/181-south-park.md`, and what remains unverified in the shipped
asset. `REPORT.md` records the build decisions that follow from it.

**Read this first.** This asset was built without street-level photography. The
geometry, the massing and the roof are sourced. The four elevations' *detail* —
facade material, colour, window rhythm, bay count — is not, and the model ships
with that stated rather than hidden. See §7.

---

## 1. Identity

| | |
|---|---|
| Address | 181 South Park, San Francisco, CA 94107 |
| Also known as | "Park 181" |
| Built | 2000–2002; construction permit completed 24 December 2002 |
| Programme | 5 live/work loft units over ground-floor commercial, plus a garage |
| Storeys | 4 |
| Block / lot | 3775 / 172 (map block lot); seven condominium lots, 172–178 |
| Zoning | SPD (SoMa — South Park) |
| Notable | Instagram's office on 9 April 2012, the day Facebook announced the acquisition |
| Architect | not recorded in any source consulted |

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/124889463 | the footprint rectangle, the address, and the `height=14` tag that must not be used |
| DataSF Building Footprints, LiDAR-derived (`ynuv-fyni`), record `SF3775172` | the height statistics that fix the roof: ground 6.84 m NAVD88, median 14.18 m, majority 14.28 m, mean 13.15 m, max 16.54 m, std 3.10 m, min 0.04 m |
| DataSF Parcels (`acdm-wktn`) | the seven condominium lots at this address, zoning, the mapblklot |
| SF Assessor Historical Secured Property Tax Rolls (`wv5m-vpq2`) | 2002 build year; per-lot use and area — 8,631 sq ft commercial + five residential lots of 1,058–1,740 sq ft |
| SF Building Permits (`i98e-djp9`) | permit 200005099501 "erect a four story, five unit live/work loft", $2.3M; permit 200005099504 demolishing the two-storey warehouse it replaced; permit 200108166212 "change roof deck to unoccupied roof"; permit 200211131341 "exit from garage to varney"; permit 200209106108 ground-floor change of use to retail; four storeys in every permit 2006–2022 |
| Bing Maps satellite, Vexcel 2026 nadir imagery | the roof: a light-grey standing-seam ridged metal roof with its ridge along the long axis, hipped down at the NW end, roof monitors on the ridge, mechanical grouped at the Varney end, and a lower flat section at the extreme SE end |
| Getty Images news photo 142617135, 9 April 2012 | Instagram at this address |
| Listing copy (Zillow, Redfin, Homes.com, ApartmentList) | 5 loft units, "arched hardwood high ceilings", "towering steel-framed windows", downtown skyline views, former Instagram offices |

Not consulted, because not reachable: Google Maps and Street View (blocked from
the authoring session), Bing Streetside (no coverage on this block), Bing 3D mesh
(would not render). No oblique or street-level image of this building was seen.

## 3. Verified dimensions and location

| | |
|---|---|
| Anchor (WGS84) | `-122.3945113, 37.7807582` — the footprint's oriented-bounding-box centre |
| Footprint | 43.21 x 13.84 m rectangle, 597.96 m2, long axis bearing 135.2° |
| Eave | 11.82 m (derived — see §4) |
| Ridge | 16.5 m (LiDAR max 16.54, normalized to the manifest target) |
| Ground | 6.84 m NAVD88 — the app's terrain handles this, not the asset |

The footprint came from OSM way/124889463 reduced to its four real corners: six
of its eight nodes are collinear, so the "8-vertex polygon" is a plain rectangle.
DataSF's LiDAR outline of the same building is a 42-vertex noisy version of that
rectangle (42.35 x 13.66 m OBB, 92.5% fill) and agrees within about a metre per
side. The OSM rectangle was used because it is the clean surveyed shape; the
DataSF outline was used for every height.

Corners in Blender metres, CCW, centred on the anchor, `+X` east `+Y` north:

```
(-10.443,  20.082)
(-20.255,  10.322)
( 10.438, -20.088)
( 20.250, -10.327)
```

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| 0 | 13.84 m | NW 315.2° | **South Park front** — storefront, residential entry |
| 1 | 43.21 m | SW 224.7° | **exposed flank** — faces the Shell forecourt, carries the window rhythm |
| 2 | 13.84 m | SE 135.2° | **Varney Place end** — garage |
| 3 | 43.21 m | NE 44.7° | party wall with 171 South Park |

Measured clearances: South Park sidewalk 1.9 m off the NW end, South Park
roadway centreline 10.6 m, park boundary 15.1 m; Varney Place 2.7 m off the SE
end. 171 South Park's nearest footprint node is a shared party-wall node 7.00 m
from the anchor — the number that constrains the integration exclusion radius.

## 4. The roof, and how its form was settled

The plan left this open: something reaches 16.54 m over a roof whose median is
14.18 m, and the plan could not say whether that was a penthouse, a barrel vault
or a gable. Two independent lines of evidence closed it.

**Aerial imagery** settled *ridged, not flat*: the Vexcel nadir image shows a
light-grey standing-seam metal roof with a ridge running along the long axis for
most of the building's length, hipped down at the NW end, with roof monitors on
the ridge and the plant grouped at the Varney end. No penthouse.

**The LiDAR height distribution** settled *straight, not curved*, and this is the
sharper test. Over a footprint, a roof's height distribution has a shape that
depends on its section, so the gap between the median height and the maximum
height identifies the section:

| Section | Median as a fraction of the rise | Implied eave, given median 14.18 m and ridge 16.54 m |
|---|---|---|
| straight gable (uniform) | 0.50 | **11.82 m** |
| parabolic arc | 0.75 | 7.10 m |
| circular barrel | 0.866 | −1.07 m |

A curved roof puts most of its plan area near the crown and drags the median up
toward the ridge. To reach a median as low as 14.18 m under a 16.54 m ridge, a
parabolic roof would need its eaves at 7.1 m and a circular one below ground.
Neither is possible on a four-storey building. Only the straight slope closes,
and it closes on an eave of 11.82 m — which is exactly two generous loft floors
above a 4.0 m commercial ground floor, with the fourth storey inside the roof.

That last point resolves the listings' "arched hardwood high ceilings" too: the
arch is an interior ceiling hung inside a straight-pitched roof, not the roof's
own section. Both facts are true at once and neither has to be discarded.

**Confidence.** *Ridged* is observed. *Straight-sloped* is a strong inference
from measured data, not an observation. *11.82 m* is arithmetic from that
inference. A single street-level photograph would upgrade all three, and none was
available.

## 5. What each side shows

**Top — observed.** Standing-seam metal, ridge along the long axis, hipped at the
NW end, monitors on the ridge, mechanical and a lower flat roof section at the
Varney end.

**Northwest (South Park) — inferred.** 13.84 m wide and 16.5 m tall: a distinctly
vertical face. The ground floor carries the commercial condo's storefront and the
separate residential entry to the five lofts. Above, two window bays per floor,
which is all a face this narrow will take.

**Southwest flank — inferred.** 43.21 m long, four storeys, and exposed: the
Shell station forecourt means no neighbour against it. This is where the
building's window rhythm lives and the largest surface the app's aerial camera
presents.

**Northeast flank — party wall, and that much is certain.** 171 South Park abuts
it and reaches 11 m against this building's 11.82 m eave, so only the roof clears
the neighbour. In reality this is a blind fire wall.

**Southeast (Varney Place) — inferred.** The service end: the garage door
(permit-confirmed), a pedestrian exit, and a plainer upper wall.

## 6. Recognition cues, ranked

1. The proportion — 43.21 x 13.84 m, 3.1:1, running the whole depth of the block.
   Nothing else on this side of the oval is shaped like it.
2. The long ridged metal roof — the only non-flat roof on this side of the oval.
3. Four storeys where the neighbours are two and three (171 at 11 m, 159 at 5 m,
   the Shell canopy at 4 m), standing about 5 m proud on both sides.
4. Tall loft windows in a regular bay rhythm along the exposed flank.
5. Storefront at the park end, garage door at the alley end.

## 7. Uncertainties in the shipped asset

Stated plainly, because this asset ships with them:

- **The facade is unverified.** Material, colour, window rhythm, bay count and
  the presence or absence of a signature accent are all inference. The body is
  authored in `Toy_stone`, a neutral that will sit correctly beside the
  neighbourhood, chosen because no evidence pointed anywhere else — not because
  the building is known to be that colour.
- **The eave line is derived, not measured** (§4).
- **The roof section is inferred from a height distribution, not seen** (§4).
- **The 10-bay flank rhythm is a proportion guess** — 43.21 m / 10 gives 4.32 m
  centres, a plausible loft bay, and nothing more.
- **The lower Varney-end roof section** is read from one nadir image and
  corroborated by the LiDAR mean sitting 1.03 m below its median. Its extent
  (6.5 m modelled) is an estimate.
- **No architect** is recorded, so there is no design-intent document to check
  any of the above against.

Everything in §1, §2, §3 and the observed half of §4 is sourced and can be
relied on. Everything in §7 should be re-verified the first time anyone stands
in South Park with a camera.
