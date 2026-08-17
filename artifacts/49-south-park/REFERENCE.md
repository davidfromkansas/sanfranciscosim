# 45–49 South Park — Gran Oriente Filipino Residence — reference dossier

Compiled 16–17 August 2026 for `artifacts/49-south-park/`. This is the research the
model was built from; `REPORT.md` records what the build actually did, including the
places where it departs from `docs/asset-plans/49-south-park.md`.

A 1909 Edwardian flats building on the corner of the South Park oval and Jack London
Alley, bought in September 1947 by the **Gran Oriente Filipino** — the first
Filipino-founded Masonic lodge in the United States — and still owned by them. It is
one of the three buildings in a proposed Article 10 landmark complex; the other two
are the Gran Oriente Filipino Hotel at 104–106 South Park (already in this manifest
as `106-south-park`) and the 1951 Masonic Temple at 95 Jack London Alley, which
stands at the far end of this same lot and is **not** part of this asset.

## 1. Sources, and what each establishes

| Source | Establishes |
|---|---|
| **SF Planning, *Gran Oriente Filipino Hotel, Residence, and Masonic Temple Complex* landmark designation report**, draft 2017 ([PDF](https://static1.squarespace.com/static/5b2c30b58f51305e3d641e81/t/607d36dc86015c6f61d7e31e/1618818784827/Gran+Oriente_Landmark+Designation+Report.pdf)) | The primary source. Edwardian style attribution; the itemised character-defining features quoted in §3; the history in §2; the landmark site boundary ("Lots 058 and 039 in Assessor's Block 3775"); and **two January 2017 colour photographs of this building** on p. 19 — one of the South Park front from the park, one of the South Park × Jack London Alley corner taking in most of the alley flank. Those two photographs are the entire visual basis of this model. |
| **DataSF Building Footprints** `ynuv-fyni` (LiDAR/Pictometry, 2010 survey) | Footprint `201006.0014671`, `mblr = SF3775039`: 278.6 m², OBB 14.63 × 20.91 m at 45.8°; roof height **median 12.08 m** (majority 12.05, mean 11.93, σ 0.73, 1,099 cells) and **max 13.00 m**; ground 10.99 m NAVD88. Second footprint on the same lot, `201006.0108499`, 112.9 m², median 7.84 m — the 1951 Masonic Temple. Neighbours: 41–43 (`SF3775040`) median 9.83 m; 101 South Park (`SF3775038`) median 5.56 m. |
| **DataSF parcels** `acdm-wktn`, lot `3775039` | Lot 13.84 m frontage × 32.29 m deep = 447 m², address range 45–49, zoning SPD. Fixes which of the two lot buildings is which. |
| **DataSF Enterprise Addressing System** `ramy-di5m` | 45, 47 and 49 South Park are one address point at `-122.393530, 37.781406` — which is the parcel centroid, not a frontage, and therefore useless for orientation. Orientation came from the footprint polygon. |
| **SF Assessor secured roll** `wv5m-vpq2` | `0049 0045 SOUTH PARK`; built **1909**; **3 storeys**; **7 units**, 40 rooms, 8 baths; class A5 "Apartment 5 to 14 Units"; construction type **D** (wood frame); 11,010 ft² of building on a 4,887 ft² lot. |
| **SF Building Permits** `i98e-djp9` | 12 permits on lot 039, 1982–2018. Every one of them records **3 existing storeys**. The most recent building permits are a 2015 mandatory soft-storey retrofit and a 2016 rear-stair repair; after that only a November 2018 street-space permit. **Nothing on this lot resembles a facade project.** See §6. |
| **OSM** [`way/71211339`](https://www.openstreetmap.org/way/71211339) | Independent footprint (271 m², 3% off DataSF) with `addr:housenumber = 45;47;49` and `height = 12` — which agrees with the LiDAR median to 0.08 m. |
| **Google Maps satellite** (Vexcel/Airbus/Maxar, 2026) | The roof: a taupe / warm mid-grey membrane, clearly darker and warmer than the near-white roofs of the newer buildings across the alley; a hatch near the centre, a pale grid-like skylight or light-well toward the rear third, scattered small vents. |
| `artifacts/106-south-park/` | The sibling building's dossier and build script; the authoring conventions this model follows. |

Not obtained: Google Street View. The January 2025 pano exists for this corner but
would not render in the available browser during this pass, and no substitute for
current photography was found. This is the single largest gap in the dossier — see §6.

## 2. History

Filipino merchant marines pooled earnings and bought 104–106 South Park, formerly the
Japanese-run Hotel Omiya, in 1921. Local dues later bought two residential flats
buildings on the same oval: 41–43 South Park (sold in 2011) and **45–49 South Park, in
September 1947**. In 1951 the lodge built its Masonic Temple behind 45–49; that
building is addressed 95 Jack London Alley and stands at the south-east end of this
lot. The complex's period of significance is 1947–1951. The Gran Oriente served a
mainly bachelor community of farm labourers, cannery workers and domestic servants at
a time when unions and much of society were openly hostile; by 1940 the organisation
had 700 members across seven states.

## 3. Verified form — the designation report's character-defining features

Quoted from the report, and the spine of the model:

> - Three-story, plus raised basement rectangular massing and plan with flat roof
> - Brick cladding at basement, drop channel horizontal wood siding at first floor, and
>   horizontal tongue and groove horizontal wood siding
> - Regularly spaced fenestration pattern with brick sills at basement and wood window
>   frames and sills at first, second, and third stories
> - Rounded bay windows supported by brackets spanning second and third stories at
>   northeast, northwest and southwest corners of the building
> - Angled bay windows supported by brackets spanning the second and third stories
>   between rounded bays
> - Simple raised spandrel panels at bay windows
> - Wide, overhanging cornice supported by brackets
> - Two primary entrances on South Park Street flanked by wood squared engaged columns
>   and round columns both with Corinthian capitals
> - Four quatrefoil shaped stained glass windows surrounded by heavy molding flanking
>   primary entrances

The report treats the park front as facing north. In true bearings its "north-east,
north-west and south-west corners" are this model's **N**, **W** and **S** corners.

The report also records the one loss: the original wood-sash double-hung windows have
been replaced with aluminium. Everything else it lists — the siding, the bays and
their brackets, the columns and Corinthian capitals, the quatrefoils and their heavy
moulding, the cornice — it finds intact.

## 4. Dimensions, orientation and placement

Everything below is measured from the DataSF LiDAR polygon unless marked otherwise.

| | |
|---|---|
| Wall box | **12.90 m** (South Park front) × **17.70 m** deep = 228 m² |
| LiDAR outline | 278.6 m² — the wall box plus bay and cornice overhang plus rear stairs |
| Anchor (model XY bbox centre) | `-122.3935926, 37.7814648` |
| Front outward normal | **315.8°** (NW, over the park) |
| Alley flank outward normal | **225.8°** (SW, Jack London Alley) |
| Party wall | 45.8° (NE, toward 41–43 South Park) |
| Rear | 135.8° (SE, toward the Masonic Temple) |
| Roof deck | **12.05 m** — LiDAR median 12.08, OSM `height=12` |
| Cornice crest | 12.30 m |
| Turret crown / model height | **13.00 m** — LiDAR `hgt_max` |

Wall-box corners, in Blender coordinates (metres, `+X` east, `+Y` north) relative to
the plan's design anchor `-122.3935869, 37.7814643`:

```
W corner (front x alley)   ( -10.794,   1.848 )
N corner (front x party)   (  -1.546,  10.841 )
E corner (party x rear)    (  10.794,  -1.848 )
S corner (alley x rear)    (   1.546, -10.841 )
```

**Why the wall box is smaller than the LiDAR outline.** The LiDAR polygon's south-west
line sits 1.36 m outboard of the wall box and its front line about 0.9 m outboard.
That is the bay windows and the cornice, which is exactly what a roof-derived outline
traces. The reading is self-consistent: the polygon's two clean measured sides — a
12.88 m front edge and a 17.71 m south-west flank edge — reproduce the wall box to
within 0.02 m. The rear edge additionally carries three small projections reaching a
further ~2.3 m; those are the exterior wood rear stairs the 2010 and 2016 permits
record repairing, and they are why the LiDAR OBB is 20.91 m deep against a 17.70 m
building.

Because the building sits at 45.8° to the world axes, the model's axis-aligned XY
bounding box is 23.63 × 22.61 m. That is the rotation, not a scale error.

## 5. What each side shows

**North-west (South Park front), 12.90 m — hero.** Three registers. A raised basement
of dark painted brick about 1.5 m tall with small grilled openings and a thin red-oxide
water-table stripe at its head. A first storey carrying, from the party end to the
alley end: a plain double-hung window, a quatrefoil rosette, an entrance, two rosettes
side by side, a second entrance, a rosette, a plain window — each entrance a shallow
recess behind a decorative iron gate framed by round columns with Corinthian capitals
against squared engaged columns; the rosettes four-lobed cloverleaves in heavy cream
moulding, glazed dark green-teal. Second and third storeys **entirely bay**: a rounded
bay at the party corner, two canted bays, and the rounded corner turret. Above it all a
wide overhanging cornice on chunky brackets, unbroken, with the flat roof behind.

**South-west (Jack London Alley flank), 17.70 m — hero.** A real elevation, not a
service side, and the app's camera sees it as much as the front. Same three registers,
same rhythm: the turret wrapping the corner, then flat wall with paired double-hung
windows, two canted bays with flat wall between, and a rounded bay near the rear corner.

**North-east (party wall), 17.70 m.** Blind. 41–43 South Park's roof is 2.3 m lower, so
about 2.3 m of this wall really is exposed above the neighbour and shows in the baked
city. Plain siding; one light-well notch about 2.3 m long and 2.3 m deep two-thirds of
the way back, visible in the LiDAR outline. *Partly inferred.*

**South-east (rear), 12.90 m.** Faces the ~6 m gap to the Masonic Temple. *Inferred*:
plain, a rear door, and the wood stair structure the permits describe. No usable
photography, and none is needed — no camera position the app allows can see it.

**Top.** Flat at 12.05 m. Taupe / warm mid-grey membrane inside a continuous cornice
ring. The story from above is that **the ring is not a rectangle**: the seven bays push
it out into three rounded and four canted bulges along two of its four sides, while the
party and rear sides stay straight. Roof furniture from satellite: a hatch, a skylight
or light-well toward the rear third, scattered vents.

## 6. Uncertainties, conflicts, and the one that mattered

1. **Has anything changed since January 2017?** This is the live risk, and it has a
   specific reason for existing: the sibling at 104–106 South Park was gutted and
   re-skinned in a $3.1 M rehabilitation between 2019 and 2022 that *removed* its
   painted ornament, and `106-south-park` had to be modelled as the post-rehab
   building rather than the nominated one. The evidence that 45–49 escaped that project
   is negative but strong: every rehabilitation permit is on block 3775 lot **058**
   (permit 201912189921, "rehab/renovation improvement for sing room occupancy, new
   interiors, new mep, new stairs", $3,100,000, filed 2019-12-18, with revisions through
   2023 including "full stucco replacement scope at the south elevation corner to
   corner"), while lot **039** shows nothing after a November 2018 street-space permit
   and no building permit after the 2016 rear-stair repair. The same dataset therefore
   demonstrably *does* capture work of this kind, which is what makes the absence
   meaningful. It is still an absence. **The first thing anyone revising this asset
   should do is open the January 2025 Street View pano.**
2. **The paint is the weakest observation.** Both photographs are January 2017,
   overcast, the elevation in shadow, part of it behind a full-grown street tree. What
   they establish reliably is the *relation* — a pale, faintly green-grey body; trim
   clearly lighter but not white; a distinctly darker basement; a thin red line between
   them — not the hues. See REPORT.md 1 for what the model does with that.
3. **The bay rhythm is read from two photographs.** The *count* of rounded bays — three,
   one per exposed corner — is stated in the designation report and is solid. The number
   and spacing of the canted bays between them is inferred: four in this model, two per
   hero elevation. The front photograph is half-hidden by a street tree and the flank
   photograph is oblique.
4. **Does the corner bay really wrap the corner?** This model builds it as a rounded
   turret centred on the West corner and swung onto the corner bisector, because that is
   what the 2017 corner photograph appears to show and because it is by far the strongest
   reading for a miniature. The alternative — two separate rounded bays meeting at the
   corner — is not fully excluded by the available imagery.
5. **The 13.00 m figure is measured; its attribution is not.** DataSF's `hgt_max` over
   this footprint is 13.00 m against a 12.08 m median — a textbook flat roof with one
   taller element. This model assigns that element to the turret crown, because that is
   what the photographs show standing above the cornice line. It could instead be a vent
   or a stair bulkhead; if it is, the crown should still hold 13.00 m, because a vent
   must never be a model's height normalization target.
6. **The floor-area arithmetic does not close.** The assessor records 11,010 ft²
   (1,023 m²) on this lot. Three storeys plus basement on a 228 m² wall box is about
   912 m², and the temple adds roughly 226 m² over two floors — 1,138 m² together, about
   11% over. Not large enough to change anything; AGENTS rule 5 settles the method
   regardless.

## 7. Recognition cues, ranked

1. **The bays — seven, three of them rounded, wrapping two adjacent elevations.**
   Nothing else on the oval looks like this, and from the aerial camera the bulged
   cornice ring identifies the building on its own.
2. **The rounded corner turret** at South Park × Jack London Alley, crowned above the
   cornice.
3. **The wide bracketed cornice.**
4. **Pale body over a dark raised basement**, with cream trim — the SF Edwardian
   base / body / cap sandwich, with a red-oxide line at the joint.
5. **The four quatrefoil rosettes and the twin columned entrances** — small, odd,
   heraldic, and the thing anyone who knows this building remembers about its ground
   floor.

## 8. Preserved, simplified, dropped

**Preserved** — the corner condition and the real 45.8° heading; the seven-bay rhythm
and the distinction between rounded and canted; one shared bracket shelf and one shared
cap line; the three-register elevation; the four rosettes; the two entrances with their
columns; the red water-table stripe.

**Simplified** — rounded bays are 6-segment cylinder segments and the turret an
8-segment one, not smooth revolutions; bay brackets are one continuous chamfered shelf,
not individual scrolls; cornice brackets are a run of blocks on the flat stretches of
the two hero elevations only; each bay light is one flat glass band in a chunky cream
frame; entrance columns are 8-sided with a square abacus.

**Dropped** — window mullions and meeting rails; the ironwork of the gates; column
fluting and acanthus; the drop-channel siding boards; the individual rear stairs
(one simplified box stands for them).

**Exaggerated** — exactly one thing: the quatrefoil rosettes, from a real ~0.90 m to
**1.30 m**. At 12.90 m of frontage the real thing is a couple of pixels from the app's
camera, and it is the ground floor's whole identity.
