# 524 Second Street — reference dossier

Compiled 16 August 2026 for `artifacts/524-second/`. This is the modeller's own
verification pass over `docs/asset-plans/524-second.md`; where the two differ, this
file and `REPORT.md` win.

522–524 Second Street is a 1923 two-storey brick warehouse on the southeast corner of
Second Street and Taber Place in SoMa, three lots southeast of Bryant. It is the lowest
building on its block face and the only one carrying a crenellated parapet. It has been
an office building for decades — Oculus VR 2014–2017, Menlo Ventures today — inside an
industrial shell the Assessor still classes as Industrial.

## 1. Sources and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3775004` | the address-to-lot link: `from_address_num 522`, `to_address_num 524`, `02ND ST`, active, CMUO zoning; lot polygon 639.1 m2 | authoritative |
| SF Assessor secured roll `wv5m-vpq2`, block 3775 lot 004 | built **1923**, **2 storeys**, building area **13,475 sq ft**, class Industrial | authoritative |
| DataSF LiDAR footprints `ynuv-fyni`, `mblr=SF3775004` | roof membrane **8.96 m** (`hgt_mediancm 896`, mean 8.98, std 0.95, 2,293 cells); ground 14.73 m NAVD88; polygon 569.7 m2 | measured |
| SF Building Permits `i98e-djp9`, block 3775 lot 004 (29 permits) | every permit 2005–2020 records 2 existing / 2 proposed storeys and `existing_use = office`; **2006-11-27** one rooftop HVAC unit + three exhaust fans; **2012-03-27** electric single-faced door/window sign; **2020-08-22** one fan coil, one condensing unit, one rooftop unit | authoritative |
| OSM way 112926337 | `addr:housenumber=524`, `addr:street=2nd Street`, `building=yes`, `height=9`; a clean 6-node rectangle, 619.9 m2 | measured geometry, tag caveat below |
| OSM way 88559680 (2nd Street) + the Taber Place way | Taber Place T's into Second Street 18 m northwest of the frontage midpoint and runs the full 29.6 m flank ~2.9 m off the wall — **this is a corner lot** | authoritative |
| Google Street View, Second Street, capture **May 2025** | the crenellated parapet and its nine merlons; the two-tone facade; six window bays; the projecting grey entrance bay dead centre; recessed dark double doors; the "524" plate at the Taber end; the TABER PL. street sign | primary visual |
| Google Street View, Taber Place, capture **Jan 2025** | the northwest flank: red brick piers, continuous multi-light steel sash both storeys, grey painted base ~1.5 m, security mesh | primary visual |
| Google Maps satellite, Vexcel imagery 2026 | flat pale membrane roof, parapet ring, three skylights, mechanical cluster toward the street end, a diagonal run of small fixtures | primary visual |
| DataSF LiDAR, neighbours `SF3775002` / `SF3775005` / `SF3775001` | 512 Second **19.71 m** (5 storeys, 1909), 544 Second **12.83 m** (3 storeys, 1923), 500 Second 13.66 m — 524 is the lowest by 3.9 m | measured |
| menlovc.com/contact; SF registered-business records | current and former tenants; "524 Second St, 2nd Floor" independently confirms a second floor | corroborating |

## 2. Verified dimensions and location

- **Anchor (WGS84):** `-122.3934330, 37.7825731` — the footprint OBB centre.
- **Footprint:** 20.92 m of Second Street frontage x 29.63 m deep, 619.9 m2, 99.2%
  rectangular fill.
- **Roof membrane:** 8.96 m — measured, and the only hard height in the asset.
- **Parapet coping:** 9.32 m — photogrammetric, estimated.
- **Merlon tops (crest, `targetHeightM`):** 9.90 m — photogrammetric, estimated, ±0.6 m.
- **Ground:** 14.73 m NAVD88. The app's terrain handles this; the asset sits on z = 0.

**Three footprint sources disagree by 12%, and the choice matters:**

| Source | Dimensions | Area |
|---|---|---|
| DataSF LiDAR `SF3775004` | 19.3 x 29.5 m | 569.7 m2 |
| **OSM way 112926337 — used** | **20.92 x 29.63 m** | **619.9 m2** |
| DataSF parcel `3775004` | 21.5 x 29.8 m | 639.1 m2 |

OSM is used because it sits between the other two exactly where a real wall sits: a
lot-line warehouse fills its lot, inset from the property line by about 0.3 m per side.
The LiDAR polygon is the outlier and it is short specifically on the Second Street edge,
where 512 Second Street — 19.7 m tall across a 6 m alley — shadows the scan. Note this is
the **opposite** call from `358-brannan`, where OSM was demonstrably wrong and DataSF
right. Reconcile all three every time; do not trust one source by habit.

## 3. Orientation

Rotated ~45.6° off the world axes, like the whole SoMa grid.

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| Second Street | 20.92 m | **45.6° NE** | hero, public |
| Taber Place | 29.63 m | **315.4° NW** | second public elevation |
| party wall to 544 Second | 29.63 m | 135.4° SE | blind |
| rear, to the 10 South Park block | 20.92 m | 225.6° SW | blind |

Footprint in Blender coordinates (metres, +X east, +Y north), CCW, centred on the anchor:

```
(  3.240,  17.813)   north corner — Second St x Taber Pl
(-17.929,  -2.918)   west corner
( -3.240, -17.813)   south corner
( 17.929,   2.918)   east corner
```

The 45.6° heading turns a 20.92 x 29.63 m building into a ~36.0 x 35.8 m axis-aligned
bounding box. That is expected, not a scale error.

## 4. What each side shows

**Northeast — Second Street (hero).** A crenellated parapet: a plain brick parapet
carrying **nine chunky square merlon blocks**, pale against the brick, evenly spaced
across the frontage with the outermost pair on the corners. Below it a shallow brick
band. Then the second storey: **six bays** of large multi-light steel-sash window, dark
framed, between plain red brick piers. Then a hard horizontal line where the paint
starts, and the ground floor: warm **grey painted** piers and plinth with tall
multi-light steel storefront glazing between them; a **projecting grey entrance bay**
dead centre carrying its own window and a small cornice cap; **recessed dark glazed
double doors** in a grey reveal in the second bay from the 544 end; and a painted "524"
high on the brick at the Taber Place end.

**Northwest — Taber Place (second public elevation).** 29.6 m of bare red brick piers at
the same rhythm as the front, with continuous **large multi-light steel sash** between
them on both storeys, some behind security mesh, over a **grey painted stucco base band**
about 1.5 m high. No ornament. The alley is narrow, so this wall is seen close-up,
obliquely, and from directly above.

**Southeast — party wall to 544 Second Street.** Blind, 29.6 m, hard against a neighbour
3.9 m taller. Only the top ~1 m is ever visible, and only from the air.

**Southwest — rear.** 20.9 m against the 10 South Park block. Blind or nearly so, never
seen from the street. No reference imagery exists for it; plain brick is an assumption.

**Top.** 620 m2 of flat pale membrane at 8.96 m inside a parapet ring, and what the app's
camera actually looks at. Vexcel shows: the parapet ring reading against the deck; three
pale skylights across the middle; a mechanical cluster toward the Second Street end
(consistent with the permitted two rooftop units, condenser, fan coil and three exhaust
fans); and a straight diagonal run of small fixtures. Nothing tall — the whole roof reads
flat, which is why the merlon row is the only silhouette this building has.

## 5. Recognition cues (ranked)

1. **The crenellated parapet.** Nothing else on this block face has it, and on a
   dead-flat roof it is the only thing that breaks the silhouette. If the merlons do not
   read at thumbnail size, the asset has failed.
2. **Lowest on the block.** 8.96 m between a 19.71 m and a 12.83 m neighbour.
3. **The two-tone facade** — grey painted ground floor under bare red brick, on a hard
   horizontal line.
4. **Two glazed elevations turning a corner** — the same brick-pier-and-steel-sash
   rhythm on Second Street and Taber Place.
5. The projecting grey entrance bay at the centre of the front.

## 6. Preserve / simplify

**Preserve:** the 20.92 x 29.63 m proportion and the real 45.6° heading; the merlons as
**discrete blocks with visible gaps**; the corner condition, with Taber Place as a
designed elevation; the hard horizontal paint line; the building's lowness relative to
its neighbours.

**Simplify:** merlons thickened and lifted for distance legibility (the one place
semantic exaggeration is spent); ~30 small panes per window become one glazed panel in a
frame; six front bays and nine alley bays kept as *rhythm*, not counted panes; the
recessed vertical brick panels under the merlons dropped for a single corbel band;
security mesh, downpipes, conduit, wall boxes, banner bracket and street signs dropped;
roof clutter reduced to three skylights, two rooftop units, a condenser, five vents and a
hatch.

## 7. Uncertainties and conflicting evidence

- **The target height is the weakest number.** The 8.96 m membrane is measured; everything
  above it is photogrammetric, from the May 2025 panorama rectified against the measured
  20.92 m frontage and a 2.35 m camera height derived from the same image (the width- and
  height-derived scales agree to 6%, which is what makes the camera height credible).
  Parapet 9.32 m, merlons 9.90 m, ±0.6 m. The manifest entry is `"estimated": true`.
- **The OSM `height=9` tag is the roof, not the architectural top.** It agrees with the
  LiDAR membrane to 0.04 m, which is reassuring about the membrane and says nothing about
  the parapet.
- **DataSF `hgt_maxcm` = 13.32 m is not this building.** Against `hgt_median 8.96`,
  `mean 8.98`, `std 0.95` over 2,293 cells, a 13.3 m maximum is a handful of cells — and
  512 Second Street, 19.7 m tall, stands across a 6 m alley on that side. Polygon-edge
  bleed. `hgt_mincm` 2.29 m is the same artefact at the other end. (The identical 13.32 m
  figure appears in `358-brannan.md` for a different record on the same block; two
  edge-bleed maxima, not a shared source.)
- **Whether the merlon row returns around the Taber Place corner is inferred.** The front
  panorama shows a block at the corner itself; the January 2025 Taber panorama was shot
  too close and too low to see the parapet. Three blocks are returned as the conservative
  reading.
- **The merlon count of nine** is read from one photograph partly occluded by four street
  trees. It is consistent with the 20.92 m frontage at ~2.5 m centres.
- **The Taber Place bay rhythm is extrapolated** from three piers visible in one
  close-range panorama plus the front's rhythm. Nine bays over 29.63 m. This is the most
  likely place for the model to be wrong in a way the aerial camera will see.
- **The rear elevation has no reference at all.** Assumed blind brick.
- **No architect is recorded** for the 1923 building in any source consulted. The owner of
  record, L Myers Company, has held the property since at least 1968.
