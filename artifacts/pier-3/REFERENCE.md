# Pier 3 (Hornblower Landing) — reference dossier

**374 The Embarcadero, San Francisco.** A 1918 Beaux-Arts finger pier in the Central
Embarcadero Piers Historic District, rehabilitated 2004–2006. The asset is the whole pier:
pile field, deck, bulkhead building with its arched portal, and the office block behind it.

Compiled 18 August 2026. This dossier is the authority for the build; where it disagrees with
`docs/asset-plans/pier-3.md` the dossier wins, and every disagreement is called out in §6.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| National Register nomination, Central Embarcadero Piers Historic District (`npgallery.nps.gov/GetAsset/d2f2efab-74ad-432e-ad10-4d27ffc6e593`) | 1918; Beaux-Arts; bulkheads are **two-storey stucco-on-timber-frame with two-storey arches**; **Pier 3 is a 140-ft-wide concrete slab pier on spiral-reinforced piles extending 720 ft**; rail remnants in the north breezeway; most of the transit shed lost; a single-storey addition to Pier 3's north |
| NPS district page (`nps.gov/places/central-embarcadero-piers-historic-district.htm`) | The district is Piers 1, 1½, 3 and 5; Pier 3 handled freight with a long bulkhead and transit shed |
| Tom Eliot Fisch, project 22 (`tefarch.com/projects/detail/22`) | Rehab architects (TEF with Hannum Associates and Page & Turnbull); 120,000 sq ft mixed use; seismic upgrade; Class A office; an acre of public waterfront |
| Pacific Waterfront Partners (`pacificwaterfront.com/the-piers/`) | Built 1918; condemned 2004; National Register listing taken for the federal tax credits; construction 2004–2006 |
| BayCrossings, construction announcement | $46 M; S.J. Amoroso; 22 months; CalSTRS financing; **a Hornblower ticket office fronting Herb Caen Way**; the Pier 1-to-Pier 7 waterside walkway |
| Vortex Marine Construction portfolio | **Pier 3 deck completely replaced on the existing piles**, new cast-in-place girders and deck, utility trenches, access vaults, an elevator pit, all **to support a new commercial building**; 400 piles carbon-fibre wrapped; 12 seismic bracing assemblies |
| Pragmatic Professional Engineers, "Piers 1-1/2 & 3" | 2021 MEP replacement, 21,900 sq ft, **nine rooftop HVAC units** (VAV AHUs, packaged RTUs, exhaust fans); architect Studios Architecture; owner Port of SF; tenants include Bloomberg and Starbucks |
| LoopNet listing 21091039 | "Pier 3, Hornblower landing", **2 storeys, 39,700 SF, Class B, typical floor 30,470 SF, atrium, 125 surface parking spaces** |
| SF Chronicle | The $54 M restoration; 77,000 sq ft commercial; a VC firm on a full floor |
| OSM way 281428977 (`man_made=pier`, `name=Pier 3`) | **The footprint.** There is no `building` way for Pier 3 anywhere in OSM |
| OSM way 91913148 (Pier 5 building) | A neighbouring bulkhead measured at **65.9 x 10.8 m** — the depth check that sized this one |
| OSM node 8839646288 | "City Experiences", `office=guide`, `addr:housenumber=Pier 3` — the current operator |
| DataSF `ynuv-fyni`, `mblr = CN9900003` | Ground elevation **3.07 m**; height statistics merged across three bulkheads, usable only as a bound (`hgt_max` 16.85 m) |
| Esri World Imagery z20, reprojected to local metres | Two glazed roof monitors, rooftop plant, the car-park layout, the taper, the gangway platforms |
| Google Street View panorama `MuiqVIFnVEnHxOVKIKtJhQ` (plus `H_cSsG60buJ9wEvC_z0ZnQ`, `tybmfcgGy1bcjFw6NdmDtw`) | The frontage elevation and **the height measurement in §3** |

No copyrighted imagery is committed. The panorama ids and dataset queries above reproduce
every measurement in this file.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.3947017, 37.7982322` | **measured** — OSM polygon area centroid |
| Footprint area | 8,926 m2 | **measured** |
| Oriented bounding box | 212.79 x 53.50 m, 78.4% fill | **measured** |
| Pier axis | bearing **53.92°**; frontage faces 233.92° | **measured** |
| Width | 39.6 m at the head, 53.5 m at the bulkhead — the pier **tapers** | **measured** |
| Promenade / deck grade | 3.07 m above datum | **measured** (DataSF `gnd_mediancm`) |
| Attic crest over the pediment | **18.5 m above water** (15.5 m above grade) | **measured**, §3 |
| Arch extrados crown | 12.5 m above water (9.5 m above grade) | **measured**, §3 |
| Bulkhead cornice | ~13.2 m above water | *inferred* |
| Bulkhead parapet | ~14.0 m above water | *inferred* |
| Office block roof | ~12.4 m above water | *inferred* |
| Bulkhead depth | 11.0 m | *inferred* from Pier 5's measured 10.8 m |

## 3. How the 18.5 m was measured

Google Street View panorama `MuiqVIFnVEnHxOVKIKtJhQ` at `37.79785953, -122.39632222`,
stitched from zoom-3 tiles to 4096 x 2048 equirectangular. The equirect is levelled, so the
horizon is the centre row and elevation angle is `(1024 - y) / 2048 * 180°`.

At the arch's centre column (pano x ≈ 3850): attic crest y ≈ 853 → **+15.03°**; arch extrados
crown y ≈ 930 → **+8.26°**; pavement at the wall base y ≈ 1057 → **−2.90°**.

The base angle gives `L = h_cam / tan(2.90°)`, which needs the camera height. Two independent
routes pinned `L` without assuming one:

1. **Bearing intersection.** Calibrating the panorama's yaw against the Ferry Building clock
   tower (pano x ≈ 4034, true bearing 134.83° from this camera) puts the arch at 119.1°.
   Intersecting that ray with the bulkhead line — from OSM way 91913148, Pier 5's building,
   whose street face runs 144.0°/324.0° and lies 20.32 m from the camera — gives **48.2 m**.
2. **Plan identification.** The portal's gabled pavilion is directly visible in Esri z20
   imagery reprojected into local metres, at about `(3671, −3069)` in app coordinates, which
   is **48.7 m** from the camera.

The two agree to 0.5 m. Feeding `L = 48.5 m` back through the base angle returns
`h_cam = 2.46 m` — the standard Street View camera height. That is the check that the
construction is self-consistent rather than three errors cancelling.

`H = 2.46 + 48.5·tan(15.03°) = 15.5 m above the promenade`, and the promenade is 3.07 m above
datum, giving **18.5 m above water**. The arch crown lands at 9.5 m above grade, which matches
the National Register's "two-story arches". DataSF's LiDAR maximum over the merged
three-bulkhead polygon is 16.85 m above ground = 19.9 m above datum: above the crest and
below the crest-plus-flagpole, which is exactly where it should sit.

**Honest range: 17.5–19.5 m.** No drawing, survey or Wikidata entry for this pier's height was
found.

## 4. Observations by side

**Southwest (The Embarcadero).** Two-storey pale stucco wall, rusticated ground storey,
pilaster bays, paired upper windows with moulded surrounds, shopfronts and cafe awnings at
grade, a strong continuous cornice and a low parapet. At the centre a projecting pedimented
pavilion carries one deep semicircular arch (~9 m span, springing ~5 m above grade, crown
~9.5 m), a stepped voussoir surround, "PIER · 3" incised in the tympanum, a raised attic block
and a flagpole. The arch is glazed with a dark steel-framed screen. Blue City Experiences
banners hang on the flanking piers.

**Northwest flank.** Office wall for the shoreward third, then open fendered deck with
bollards, tubular railing and light standards. The *Santa Rosa* berths here.

**Southeast flank.** Same, facing the slip and the Pier 1½ promenade; the Pier 1-to-Pier 7
waterside walkway runs along it.

**Northeast (pier head).** A plain ~40 m concrete end with fendering, rail and bollards.

**Top.** Three fields shoreward to seaward: the bulkhead roof behind its parapet with the
pediment breaking it; the office roof, flat, with **two large rectangular glazed monitors**
running with the pier axis plus a rank of grey rooftop units and a screened plant enclosure;
and the long open deck with ~125 painted bays, two service sheds, a light-standard rhythm and
the fendered perimeter.

**Underside.** Pile field and deck soffit. Original 1918 spiral-reinforced concrete piles,
carbon-fibre wrapped in 2005.

## 5. Recognition cues, ranked

1. The arched "PIER · 3" portal with its flagpole
2. The silhouette of a long low finger pier running out into the bay at 54°
3. The two glazed roof monitors — the identity from directly overhead
4. The two-storey Beaux-Arts bulkhead wall, continuous with its neighbours
5. The open working deck: parking bays, bollards, railings, sheds

## 6. Corrections to the plan, and deliberate deviations

**REPORT beats plan.** These are the places where the build does not follow
`docs/asset-plans/pier-3.md`, and why.

1. **The bulkhead is 43.5 m wide, not the plan's full 53.5 m frontage.** The plan's massing
   recipe put a 53.5 m building on the frontage edge. The OSM polygon flares to 53.5 m only at
   its outermost corner and narrows immediately: a 53.5 m block 11 m deep pokes outside the
   footprint on the northwest by 2.3 m. Real assets sit on real footprints (AGENTS rule 5), so
   the bulkhead was narrowed to 43.5 m. The real building probably does continue onto the
   seawall in front of the pier; that ground is not Pier 3's footprint and is not this asset's
   to occupy.
2. **The bulkhead is built square to the pier axis, not on the traced frontage edge.** OSM
   traces the frontage at 327.6°, which is 3.6° off perpendicular to the pier axis. The
   Embarcadero itself runs 324.0° (measured independently from Pier 5's building), so the
   traced edge is the error, and a bulkhead built on it comes out visibly skew against its
   neighbours. The deck keeps the traced polygon; everything above deck level is on the axis
   frame.
3. **The flagpole is not modelled.** The plan warned about it and the warning turned out to
   bite in both directions: a mast at true height (~22.5 m) makes the bounding box 22.5 m, so
   either the whole 213 m pier is scaled down 18% to make 18.5 fit, or a 160 mm spike becomes
   the number the entire asset is normalised against. A mast stopping below the attic crest
   reads as a mistake. Leaving it off is the least-wrong of the three.
4. **The deck surface uses `Toy_conc` `#c6bfb2`, which is off-palette.** The plan anticipated
   this and specified the fallback; `Toy_stone` for both the slab and the deck collapsed two
   planes into one from the aerial. Off-palette is a WARN, not a FAIL (contract rule 7).
5. **The large roof membranes are `Toy_steel`, not `Toy_roofd`.** `Toy_roofd` renders
   near-black over 2,100 m2 of office roof and read as a pit punched in the miniature. The
   rooftop plant took `Toy_roofd` instead, so the two still separate.
6. **Added, not in the plan: the belt-railway rails and three boarding-gangway platforms.**
   Both are documented (the National Register records the rails in the north breezeway; the
   excursion berths have fixed gangway structures) and both were added because review render 2
   showed a 190 m deck reading as a bare runway. The vessels themselves stay out.
7. **The office block is 58 x 37 m**, from imagery. LoopNet's 39,700 SF over two floors
   implies ~1,845 m2 per floor against this block's 2,146 m2, so the real building is a little
   smaller or partly atrium. Flagged as *inferred*.

## 7. Remaining uncertainties

- The height is photogrammetric, range 17.5–19.5 m (§3). It sets `targetHeightM`.
- The bay count on the frontage (11) is a design rhythm, not a survey.
- The roof monitors are unmistakable in aerial imagery but no source confirms whether they are
  skylights over the listing's "atrium" or photovoltaic arrays. If they are PV, the roof reads
  much darker and the night glow on one of them is wrong.
- The single-storey north addition named in the National Register nomination was not
  positively identified in imagery. It may be one of the deck sheds. It was not invented.
- Pile spacing is *inferred* at 7.5 m. 400 piles were wrapped in 2005; no spacing drawing was
  found, and only the edge band and a centre spine are modelled.
- The deck is modelled flat at the promenade's 3.07 m. It may step down beyond the bulkhead.
- The postal code is quoted as both 94105 and 94111 by reliable sources. It affects nothing.
