# 44–46 South Park — reference dossier

Research behind `46-south-park.glb`. Compiled 16–17 August 2026 by re-verifying
`docs/asset-plans/46-south-park.md` from primary sources rather than trusting it.
Where this file and the plan disagree, this file and `REPORT.md` win.

Everything below is labelled **measured**, **observed** or *inferred*. Nothing is
taken on the plan's authority alone.

---

## 1. What this building is

A four-level mixed-use infill house on the north-west rim of the South Park oval
in SoMa, San Francisco. Ground-floor commercial unit addressed **46** (currently
the venture firm MGV — Maschmeyer Group Ventures); three residential levels above
reached from a purple-painted door addressed **44**. Built 2008 on the site of a
demolished two-storey office building, wood frame, four dwelling units.

It is an anonymous building with no architect on record and no press coverage,
and its whole visual identity is one move: a white-painted, finely gridded glazed
wall filling almost the entire 9.47 m frontage, from the pavement to a charcoal
parapet, set into a grey stucco surround. It is the only glass front on this
stretch of the rim.

## 2. Sources, and what each establishes

| Source | Establishes | Kind |
|---|---|---|
| OSM way/124884347 (`addr:housenumber=44;46`, `addr:street=South Park`, `height=14`) | footprint 29.43 x 9.47 m, 278.7 m2, frontage bearing 45.2°/225.2° | measured |
| OSM node/10874867147 (`office=company`, "Maschmeyer Group Ventures", `addr:housenumber=46`) | the ground-floor tenant | observed |
| DataSF Parcels `acdm-wktn`, blklot 3775217 | surveyed parcel 30.10 x 9.74 m, 293.0 m2, "44–46 SOUTH PARK", zoning SPD, recorded 18 Dec 2007 out of former lot 050 | measured |
| DataSF Building Footprints `ynuv-fyni`, SF3775217 | 1,146 cells at 50 cm; heights max **16.15**, majority 13.91, median 13.52, mean 12.50, min 7.04, std 2.47 m; ground 11.90 m NAVD88 | measured |
| Same, SF3775048 / SF3775219 / SF3775053 | neighbour roofs: 22–24 median 12.39 (max 14.22, std 0.63); 54–58 median 13.50 (max 16.94, std 3.89); 70 South Park median 12.87 (max 16.35, std 3.57) | measured |
| SF Assessor secured roll `wv5m-vpq2` (18 roll years) | built 2008; 3 storeys; 4 units; 6,240 sq ft building on a 3,122.66 sq ft lot; class `FS` "Flat & Store 4 units or less"; use MRES; sold 8 Aug 2011 | record |
| SF Building Permits `i98e-djp9`, permit **200501052624** (5 Jan 2005) | "to erect **4 story** 1 residential condo & retail", $1,000,000, block 3775 lot 050 | record |
| Permit **200501052617** (5 Jan 2005) | "to demolish 2 story office building" — the predecessor on this site | record |
| Permit **M137205** (15 Oct 2008) | "verify address on block 3775 lot 217 - #44 south aprk - residential #46 south park - commercial unit" — the address split | record |
| Permits 200704058150 / 201608175251 / 201609147725 / 201611072151 / 201709259517 | sprinklers 2007; wood frame (Type V); 3 storeys post-2016; **re-roofing 2016, $42,400**; bathroom 2017 | record |
| augrented.com/sf/3775217-44-46-south-park | **4.96 kW solar system installed 2012**; two combi boilers 2022; owner Provincial Appliance Hldgs | secondary |
| Google Street View panorama `3UENxVRbARytZj977XeBXA`, **Jan 2025**, ~`37.78206,-122.39367` | the entire south-east elevation, and — after rectification — its metric proportions | observed + measured |
| Google Maps satellite, **2026**, near-nadir, z21–z22 over `37.78220,-122.39383` | the roof: membrane, PV array, skylight, mechanical cluster, the rear step | observed |
| mgv.vc | the tenant at 46 | secondary |

### The attribution trap, and how it was closed

Two sources place **Ogrydziak Prillinger Architects' "Gallery House" at 44–46
South Park**: an NBC Bay Area construction update, and a 2010 *T Magazine* piece
hosted by Inglett Gallery. Both are wrong for this address, and the error is
easy to inherit because the Gallery House is genuinely famous and genuinely on
this block.

The Gallery House is **70 South Park**, two doors to the south-west:

- parcel **3775-053**, permit **200510064957**, "to erect 3 stories, 1 residence
  with gallery", with revisions in 2007 and 2009 that expand a roof **penthouse**
  and add three skylights, and a 2014 permit converting the gallery to office;
- Assessor `property_area` **5,418 sq ft**, built 2009 — and 5,418 sq ft is the
  exact figure Archilovers, Architizer and 7x7 all quote for the Gallery House;
- its facade is a parametric woven lattice derived from a reading of the SF
  bay-window code. Nothing on 44–46 resembles it.

This building is parcel **3775-217**, permit **200501052624**, "4 story 1
residential condo & retail", 6,240 sq ft, built 2008, with a plain white gridded
window wall. **No lattice was modelled.**

## 3. Verified dimensions, location and orientation

| | Value | Kind |
|---|---|---|
| Frontage (onto South Park) | **9.47 m** | measured (OSM); parcel says 9.74 m |
| Depth | **29.43 m** | measured (OSM); parcel says 30.10 m |
| Footprint area | 278.7 m2 (OSM) / 284.3 m2 (LiDAR) / 293.0 m2 (parcel) | measured, three surveys within 5% |
| Street face bearing | **135.2°** (south-east) | measured |
| Frontage line bearing | 45.2° / 225.2° | measured |
| Manifest anchor | **-122.3938222, 37.7821859** | DataSF LiDAR area centroid, moved 0.26 m by the model's recentring |
| Crest (front parapet / roof screen) | **16.15 m** | measured (LiDAR max), corroborated 15.9 ± 0.5 m by photogrammetry |
| Main roof deck | 13.90 m | measured (LiDAR majority) |
| Rear block | ~8.0 m over ~24% of the plan | *derived*, see §6 |
| Ground | 11.90 m NAVD88 | measured — the app's terrain handles this, not the asset |

The three surveys' centroids sit within 2.31 m of one another. The DataSF LiDAR
centroid was taken because it is the middle of the three **and** the centroid of
the ring the bake deletes.

Both long sides are **party walls**. The north-east one abuts 22–24 South Park
(roof 12.39 m) and the south-west one abuts 54–58 South Park (roof 13.50 m), so
this building's 13.90 m deck stands 0.4–1.5 m above both neighbours and its
16.15 m crest stands 2.2–3.8 m above them. The rear faces the block interior.

### The photogrammetry

The Street View panorama is levelled equirectangular, so the horizon is exactly
the centre row and elevation angles read directly off pixel rows. The camera's
*reported* position is unusable — it puts the lens 6.9 m from the OSM front edge
but only 3.8 m from the surveyed parcel's front edge, a 3.1 m disagreement that
condemns the reported position rather than either survey. Distance was therefore
solved from the panorama itself: the 9.47 m frontage subtends **56.9°**, and the
sine rule against the known 45.2° frontage bearing puts the lens **8.5 m** from
the facade plane, 3.2 m along the frontage from the south-west party line.

At that distance, with a 2.5 m camera height:

| Feature | Elevation angle | Height |
|---|---|---|
| head of the ground-floor glazing | 10.3° | **4.0 m** |
| top rail of the window wall | 51.0° | **13.0 m** |
| crest of the stucco band above it | 57.7° | **15.9 m** |

The 0.25 m agreement between that 15.9 m and the LiDAR maximum of 16.15 m is the
strongest single result in this dossier. The weakest link in it is the assumed
camera height; a ±0.3 m error there moves the crest by ±0.3 m.

The same rectification makes the horizontal layout metric, because once a
rectilinear view is centred on the facade normal the projection along the facade
is exactly linear. That is where the frontage layout in §4 comes from — it is
measured, not eyeballed.

## 4. What each side shows

### South-east (South Park) — **observed and measured**, Jan 2025

The only public face, and the whole building.

A **white-painted gridded glazed wall** three structural bays wide (a wider
centre bay between two narrower flankers) runs from the pavement to just under
the parapet with no solid spandrel anywhere; the floors read only as heavier
white horizontal mullions. Inside the bays the glass is subdivided by a fine grid
of near-square panes roughly 1 m across — about five wide by twelve tall. The
wall stands proud of the stucco plane by a few tens of centimetres, so the stucco
returns are visible down its north-east side: a shallow bay, not a flush curtain
wall. The last two pane rows at the top are **frosted/obscure white**, a distinct
pale band capping the grid.

The **stucco** is a medium-dark neutral grey. It forms a band across the whole
frontage above the window wall, pierced by three small dark recessed vents, and a
pier down the north-east edge. No cornice, no moulding, no ornament; the parapet
is a straight edge against the sky.

The **ground floor** is glazed to the pavement, carrying the numerals `46` and an
`MGV` neon inside. Two things are broken out of it: a white-framed **double-door
service bay** at the south-west end, with three white brackets on the wall above,
and at the north-east end a shallow **aubergine-purple entry** under a small
purple awning with a white door — `44`.

Layout along the 9.47 m frontage, from the south-west party wall (measured off
the rectified panorama):

| t (m) | Element |
|---|---|
| 0.15 – 1.95 | double-door service bay |
| 1.10 – 7.35 | the glazed wall (above the ground floor) |
| 2.15 – 7.35 | ground-floor glazing (clears the doors) |
| 7.62 – 8.10 | stucco pier |
| 8.10 – 9.35 | purple residential entry |

### North-east and south-west (party walls) — **observed indirectly**

Blind. Both neighbours' roofs are below this building's deck, so each party wall
shows only a thin strip of this building above the neighbouring roof. Modelled as
plain stucco with no openings.

### North-west (rear) — **not observed**

A block-interior face with no Street View coverage; permanent shadow in the
aerial. Everything about it is *inferred* from the LiDAR height distribution
(§6) and from the plan of the building.

It is modelled as a two-level rear block at 8.0 m with the main mass rising
behind it, and it is **not blind**: both long sides are party walls, so this is
the only daylight the four flats have, and the step down to the rear block
exists precisely to give the middle of the plan a window. A wholly blind rear is
the one reading the building's own plan rules out. Four punched openings on the
rear block's own face and six on the main mass's exposed wall above it are
therefore modelled — plain, regular, and deliberately characterless, because an
unobserved alley face is not the place to invent detail. All of it is *inferred*.

### Top — **observed**, Google satellite 2026, near-nadir

A flat light-grey membrane roof, laid out along the long axis:

- a **photovoltaic array** covering the north-west half of the main deck — a
  clean rectangular grid of dark blue-black panels, roughly four to five across
  by five to six along, aligned to the building's long axis. This is the 4.96 kW
  2012 system and it is the loudest thing on the roof from above;
- immediately south-east of it, a **large flat rectangle** about 4.5 x 4.5 m in a
  mid grey-brown, read as a **skylight or roof hatch over the stair** — no side
  face and no cast shadow are visible at this sun angle, so it is not a penthouse
  box;
- the south-east half is mostly clean membrane with about a dozen small round
  penetrations, one dark rectangular mechanical unit, and a tight cluster of four
  to six pale condenser/fan units near the north-east parapet;
- the north-west end steps down to the low rear block and is in shadow;
- **nothing tall stands anywhere on the roof.** Whatever accounts for the 2.2 m
  between the 13.90 m deck and the 16.15 m maximum is at the street edge.

## 5. Recognition cues (ranked)

1. **The white grid in a dark surround.** A finely gridded white glazed wall
   filling a 9.5 m frontage, framed by grey stucco. Nothing else on this rim
   does it.
2. **Glass to the ground.** The grid runs continuously from pavement to parapet,
   so the building reads as one lit column rather than a base and a body.
3. **Tall and thin.** Four levels over 9.5 m of frontage, flat-topped, standing
   above both neighbours on a low-rise oval.
4. **The purple entry** — the only colour on an otherwise white-and-grey
   building.
5. The solar array, which is what the aerial camera sees first.

## 6. Uncertainties and conflicting evidence

**What the top 2.2 m is.** LiDAR puts the roof surface at 13.91 m and a maximum
at 16.15 m; photogrammetry puts the top of the stucco band at 15.9 ± 0.5 m. So
the street face really does continue about 2.2 m above the deck. The reading
taken is a **solid parapet / terrace screen wall with a roof terrace behind it**,
because (a) the nadir aerial shows nothing tall standing anywhere on the roof, so
the extra height is at the edge, and (b) both immediate neighbours carry the
identical bimodal LiDAR signature — 54–58 at median 13.50 / max 16.94, and 70
South Park at 12.87 / 16.35, whose permits explicitly reconfigure a roof-level
penthouse serving a terrace. Three consecutive 2005–2009 infill houses with the
same profile is a typology, not a coincidence. The alternative — a set-back top
floor whose front wall is flush — is not excluded by anything observed, and would
change the roof design without changing the 16.15 m crest.

**The storey count conflicts, and both sides are probably right.** The 2005
construction permit says **4 story**; the Assessor and every permit from 2016 on
say **3**. The reading taken is a commercial ground floor plus three residential
levels, which satisfies both (a residential roll counts dwelling levels) and is
the only reading consistent with a 13.90 m deck: 4.35 m of commercial plus three
at ~3.2 m. Two 4.8 m loft levels cannot carry 6,240 sq ft of building area over a
3,000 sq ft footprint.

**The rear block position is derived, not observed.** The LiDAR mixture that
reproduces the measured mean (12.50 m) and standard deviation (2.47 m) against a
13.90 m deck is 23.7% of the footprint at 8.0 m — predicted std 2.51 against a
measured 2.47. The *fraction* is therefore measured; that the low part is at the
north-west end, and that it is a block rather than a light court or a stepped
terrace, is read off the aerial and is *inferred*.

**The solar array postdates the height data.** LiDAR was captured in 2010, the
array installed in 2012, so the array contributes nothing to the 16.15 m maximum.
The crest question above cannot be explained away as PV.

**No architect.** Sixteen permits, the Assessor's roll and the parcel record name
no designer. The building is not attributed to anyone here.

**The tenant is transient.** MGV took the commercial unit after 2018; the
building has changed hands once since 2011. The storefront is modelled as
architecture — glazed grid, one service bay, one entry — and no signage was
modelled.

## 7. Features preserved / simplified

**Preserved:** the 9.47 x 29.43 m footprint and the 45.2°/225.2° heading exactly;
one public face and two blind party walls; the three-bay division of the window
wall and its projection in front of the stucco; the stucco band above and pier
beside; the tall glazed ground floor with the service bay south-west and the
purple entry north-east; the flat roof with the array on the north-west half and
the step down at the rear; the height relationship to both neighbours.

**Simplified:** the ~5 x 12 pane grid becomes **3 bays x 4 floor bands of raised
trim on one glass plane** — the count is invisible at the app's camera and a
faithful grid is roughly 4,000 triangles that do not read; the frosted top band
becomes one opaque trim panel; the three stucco vents become shallow recesses;
the ground floor keeps only two openings broken out of it; the array becomes one
slab scored into a 4 x 5 grid on two rails; roof clutter becomes one skylight,
one mechanical box and three cylinders.

**Inferred, not observed:** the rear block's position and height, and every
opening on the rear elevation. See §4 and §6.

**Deliberately changed from the real building, and why:** the stucco is one grey
in reality, but the band above the window wall and the pier beside it are
authored a value darker than the body. At a single mid grey the whole asset reads
as a grey box from the app's camera and the white grid — the entire recognition —
stops working. See `REPORT.md`.

**Not modelled:** South Park and its trees, the street and pavement, the street
tree in front of the south-west end, the utility pole with its transformers and
overhead wires, the streetlight bracket, the neighbours, vehicles, people, and
all tenant signage including the `MGV` neon and the `46` numerals.
