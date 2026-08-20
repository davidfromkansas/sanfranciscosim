# 110 The Embarcadero — reference dossier

The Commonwealth Club of California headquarters, 110 The Embarcadero / 115
Steuart Street, San Francisco, CA 94105. Compiled 18 August 2026 for the SF-SIM
miniature GLB. Everything below is either **measured** (stated method and
source), **observed** (named image), or **inferred** — nothing is assumed.

---

## 1. What this building is

A 1910 two-storey waterfront warehouse that served as the International
Longshoremen's Association union hall — Harry Bridges worked from it and the
1934 Pacific Coast dock strike was organised from it, making the site of the
"Bloody Thursday" shootings. The Accornero family owned it for over 70 years
until the Commonwealth Club, the oldest and largest public-affairs forum in the
United States (founded 1903), bought it in 2012. Leddy Maytum Stacy Architects
(lead: Marsha Maytum, 1954–2024) gutted it 2015–17: the rendered Steuart Street
front was shored and restored, a light-weight glass third floor was added so the
original wooden piles in Bay mud could be reused, and a new glass curtain wall
was hung on the Embarcadero end. It opened 12 September 2017. LEED Gold,
22,600 sq ft (architect) / 24,000 sq ft (owner), California Heritage Council
Award.

Programme: a 299-seat auditorium, a 135-person multipurpose room, a library
lounge, a boardroom, three catering kitchens, a roof garden and a publicly
accessible roof terrace.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/256969674 + amenity node 9659886917 | the footprint polygon, and that this polygon is the Club (the node falls inside it). `building=commercial`, `roof:shape=flat` |
| DataSF parcels `acdm-wktn`, `mapblklot 3715002` | block 3715 lot 002, official address **115 STEUART ST**, zoning C-3-O. The parcel polygon matches the OSM ring to ≤ 1.0 m at every vertex, i.e. the building is built lot-line to lot-line |
| DBI permits `i98e-djp9` | **PA 201312174360** — "structural upgrade of (e) foundation … add 1 story to accomodate assembly", existing **2 → proposed 3**; **201601288257** — "temporary shoring of 2 story facade and 2 walls"; **201705197169** — card readers to the roof deck; every 2017 record lists 3 existing storeys |
| DataSF 2010 LiDAR `ynuv-fyni`, record `SF3715002` | the **pre-renovation** building: 2,499 half-metre cells (625 m²), ground mean 3.43 m NAVD88, height median 10.33 m, mean 11.45 m, **max 24.43 m with σ 3.38 m**. Used for the ground level and for the old two-storey shell height; the maximum is rejected (§6) |
| lmsarch.com/projects/commonwealth-club-california | architect, 22,600 sq ft, LEED Gold, "the existing two story structure, built in 1910, was renovated and a new floor added", "the historic Steuart Street façade was restored" |
| tippingstructural.com/projects/commonwealth-club | 299-seat auditorium, 135-person multipurpose room, library lounge, roof garden, **publicly accessible roof terrace**, "a new glass curtain facade alongside the historic facade" |
| commonwealthclub.org "Our Building Story" + 2017 press release | opening date, 24,000 sq ft, the 2012 purchase, "110 The Embarcadero/115 Steuart Street", Gensler's **"narrow 45-foot-wide building"**, Tipping's pile solution and the "light-weight glass third floor" |
| salter-inc.com case story | 22,000 sq ft, 300-seat auditorium, Meyer Sound Constellation, reclaimed-wood acoustic walls |
| hoodline.com, 4 April 2018 | "a berth at 110 The Embarcadero, **next to the Audiffred Building**"; "an expansive roof deck" |
| Google Street View pano `yo5P5pi5QKGaa2I7JTPGvQ` | the Embarcadero elevation. Every dimension in §4 and the building height |
| Google Street View pano `cGw3lu-Usr6Mdz7aiLS_2w` | the Steuart Street elevation |
| Bing/Vexcel near-nadir aerial, z20 (0.118 m/px) | the roof zoning in §5. Google's z22 over this block is a strong oblique and was used only for texture, never for position |

## 3. Measured geometry

Reprojected with the app's tangent projection (AGENTS.md: `x=(lon−LON0)·111320·cos(LAT0)`,
`z=−(lat−LAT0)·110540`, LON0 −122.4375, LAT0 37.77).

| | |
|---|---|
| Footprint | 41.87 × 13.91 m parallelogram, **582.1 m²** |
| Width cross-check | 13.91 m = 45.6 ft, against the press release's "narrow **45-foot**-wide building" |
| Anchor (footprint vertex mean = AABB centre) | **−122.3926624, 37.7932325** |
| Long-axis heading | 135.24 / 315.24° true |
| Embarcadero front outward normal | **44.83°** |
| Steuart front outward normal | **224.94°** |

Local footprint, metres east/north from the anchor:

```
v0 ( +19.790,  +9.833)   Embarcadero end, SE corner
v1 (  -9.935, -19.648)   Steuart end,     SE corner
v2 ( -19.781,  -9.821)   Steuart end,     NW corner
v3 (  +9.926, +19.637)   Embarcadero end, NW corner
```

Both long edges are **party walls**, confirmed by shared vertices: the Audiffred
Building's OSM ring (way/193054136) contains v2 and v3 exactly; the seven-storey
office's ring (way/193054135) contains v0 and v1 exactly.

## 4. Height — measured, because nothing publishes it

No source gives a height. The 2010 LiDAR measures the **old** building. So the
height was measured photogrammetrically from Street View, by the recipe in
`docs/asset-plans/` practice: pull the equirect/rectilinear frames keylessly,
project the footprint corners to true bearings, and resample the facade into a
metric 60 px/m rectified elevation.

**Camera solution (Embarcadero, pano `yo5P5pi5QKGaa2I7JTPGvQ` at
37.7934714, −122.3923687):** perpendicular distance to the facade plane
**D = 16.73 m**, the perpendicular foot 0.24 m off the facade centre. Verified
two independent ways before any height was read off it:

1. the two facade corners project to true bearings 203.05° and 248.50°, and both
   lines land exactly on the building's edges in Google's own rectilinear frame
   at yaw 224.8°, fov 90°;
2. the 45.45° angular span they subtend sine-rules back to a 13.93 m frontage
   against the 13.91 m measured from the polygon — 0.14 %.

**Vertical zero** is pinned on the pavement line in the rectified image, not
assumed from a nominal camera height; solving for it gives an effective eye
height of 1.93 m above the pavement (the difference from the nominal 2.5 m is the
kerb). Horizontal-edge energy in the rectified elevation then reads:

| Height (m) | Feature |
|---|---|
| 0.00 | pavement |
| 3.56 – 4.78 | ground-floor signage fascia band (COMMONWEALTH CLUB) |
| 11.01 – 12.38 | level-3 floor spandrel band |
| **16.88** | curtain-wall head / parapet |
| **17.43** | outer edge of the projecting roof fascia |

The 17.43 m is the fascia's *outer* edge, which sits ~0.5 m closer to the camera
than the facade plane and therefore reads high by ≈ 0.93 × its projection. The
architectural top is taken as **17.4 m ± 0.6**, the 0.6 being dominated by the
±0.4 m uncertainty in D.

**Two independent corroborations.** (a) The storey ladder read off the same
elevation — ground floor to ≈ 4.2 m, a ≈ 7 m double-height auditorium volume, a
≈ 4.6 m third floor, plus parapet — sums to the same crest. (b) The 2010 LiDAR
median of 10.33 m is exactly where the *old* two-storey roof should be if the new
floor was built on top of it, and the Steuart-side measurement independently puts
the retained historic parapet at 11.5 m, just above it.

**Steuart end (pano `cGw3lu-Usr6Mdz7aiLS_2w`, D = 15.73 m):** historic cornice
≈ 11.5 m, pediment apex ≈ 12.3 m, set-back glazed third floor ≈ 14.0 m, stair /
lift over-run box ≈ 14.8 m. ±0.4 m — the pavement is hidden behind parked vans
on this side, so the vertical zero is carried over from the Embarcadero solve.

**The building therefore steps.** Full height at the Embarcadero end, dropping
5.8 m to the historic parapet at the Steuart end with the new floor set back
behind it. That step is visible from every aerial angle and is the single
biggest claim in this dossier.

## 5. What each side shows

**North-east — The Embarcadero, 13.9 m (address face).** A full-width,
full-height glass curtain wall from a recessed ground floor to a projecting roof
fascia. Slender white mullions divide it into about **five structural bays of
≈ 2.6 m**, each subdivided into three ≈ 0.87 m panes; pale opaque spandrel bands
cross the full width at the floor lines. At 16.9 m the wall meets a **flat
projecting eyebrow ≈ 0.5 m deep** whose dark soffit is visible from the street
and whose outer edge is the building's crest. At ground level the wall steps back
into a dark glazed lobby with clear doors, a thin flat canopy, a white fascia
band reading **COMMONWEALTH CLUB**, and a **110** plate. **The entrance sits
toward the north-west (Audiffred) half of the frontage, not on the centreline.**
Pale plaster returns close the wall at both jambs. *Measured off the rectified
elevation.*

**South-west — Steuart Street, 13.9 m (historic face).** Two storeys of pale grey
rendered wall: a strong cornice stepping up in the centre into a wide, shallow
**triangular pediment**; a row of about six **console brackets** over a recessed
frieze; an upper storey of **four tall white-framed windows in a 2 + blank centre
bay + 2 rhythm**, each two lights wide inside a recessed moulded panel with a
broad pilaster strip between; a continuous sill band at ≈ 5.0 m; a ground storey
of three wide storefront bays with a **recessed doorway at the south-east end**;
a plain plinth. Behind and above, set back: the new third floor as a band of teal
glazing with roof-garden planting visible through it, and a solid pale-grey clad
**stair / lift over-run box on the south-east side**. *Observed directly.*

**North-west and south-east, both 41.9 m — party walls.** Blind rendered walls
against the Audiffred Building and the seven-storey office. Both neighbours are
taller (LiDAR max 19.18 m and median 26.82 m against this building's 17.4 m), so
neither face is ever seen. *Observed — both neighbours share this footprint's
vertices.*

**Top — the roof terrace.** Reading the Bing near-nadir frame along the long axis
from Steuart (SW) to Embarcadero (NE): a pale flat strip behind the historic
parapet beside the over-run box; a **planted band** occupying roughly the middle
third; a low plant volume near the centre-south; an open **paved deck** across
the north-east third; a **square roof feature** near the Embarcadero end reading
as a skylight; a parapet all round that steps down at the Steuart end. *The zones
are observed; positions within them are inferred.*

## 6. Uncertainties and conflicting evidence

1. **The 2010 LiDAR maximum of 24.43 m is rejected.** Over a 625 m² footprint the
   record reads mean 11.45, median 10.33, σ 3.38, max 24.43. A σ that large on a
   flat-roofed two-storey building is edge bleed, and the two neighbours whose
   walls bound this footprint stand at 19.18 m and 26.82 m — which is exactly
   where a 24 m return comes from. The median is used; the maximum is not.
2. **The LiDAR predates the works by five years.** It measures the two-storey
   1910 building, not what stands. It is used only for the ground level
   (3.43 m NAVD88, range 0.36 m across the footprint — flat made ground) and as
   the corroboration in §4.
3. **The setback distance at the Steuart end is inferred** from one oblique
   Street View frame. The step itself is measured; how far in the new floor
   starts is not.
4. **The Embarcadero curtain wall is planar, not curved.** Its spandrel bands bow
   strongly in the equirectangular panorama and are dead straight in the
   rectilinear frames of the same pano. Projection, not architecture.
5. **Roof-object positions are inferred.** Bing z20 at 0.118 m/px resolves zones,
   not objects; Google z22 is a strong oblique in which a 17 m roof displaces
   several metres.
6. **"110 The Embarcadero" is ambiguous in OSM** — Nominatim returns four
   objects, three of them stray address points up the waterfront. The correct
   polygon is way/256969674, identified by the Club's amenity node falling inside
   it and by the DataSF parcel matching its ring to 1 m.
7. **The rectified elevations are mirrored** on the Embarcadero side (the
   COMMONWEALTH CLUB lettering reads backwards in them) and un-mirrored on the
   Steuart side. Every left/right statement in §5 was restated in NW/SE terms
   against the raw photographs rather than inherited from the rectification.

## 7. Recognition cues, ranked

1. **Two-faced** — a three-storey glass box on one street and a rendered 1910
   pedimented front on the other, 42 m apart in the same building.
2. **The pediment on Steuart**, stepping up out of a bracketed cornice.
3. **The glass front with its fascia eyebrow and the COMMONWEALTH CLUB band.**
4. **The step in the roofline** between the two.
5. **The planted roof terrace** between two blank grey neighbours.

## 8. Corrections made to `docs/asset-plans/110-embarcadero.md` during the build

Recorded here and in REPORT.md; REPORT beats plan.

1. **Roof deck datum.** The plan put the main roof at 16.60 m with the parapet at
   16.90 — a 0.30 m upstand, which cannot guard a publicly accessible terrace and
   left nowhere to put roof planting under the 17.40 m crest. The measured 16.90
   is the parapet / curtain-wall **head**; the walking surface is a guard height
   below it. The model uses **roof deck 15.80, parapet 16.90, fascia 17.40**.
2. **No mid-roof penthouse.** The plan's massing recipe put a penthouse volume in
   the middle of the roof. The building's only stair / lift over-run is the box
   at the **Steuart** end that the elevation actually shows, at 14.8 m. The
   mid-roof volume was removed; a low plant enclosure stands in its place.
3. **Storey datums.** Level 2 at 4.20 m and level 3 at 11.20 m (the plan said
   4.2 and 11.7); the roof slab at 15.80. The 11.20 is the underside of the
   measured 11.0–12.4 m spandrel band rather than its middle.
