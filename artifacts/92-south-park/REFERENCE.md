# 92 South Park (86–96 South Park) — reference dossier

The building this asset depicts is **86–96 South Park Street**, a six-unit live/work
condominium of **1996** by **Toby S. Levy, FAIA** (Levy Design Partners / LDP
Architecture), on the corner of South Park Street and Jack London Alley in SoMa.
**"92 South Park" is one of its six unit addresses, not a separate building** — see §1.

This file outranks `docs/asset-plans/92-south-park.md` wherever the two disagree.

## 1. What the building is, and what "92 South Park" means

Block 3775, lots **116–121**: six condominium lots on ONE surveyed 435 m² corner
parcel. The SF Assessor roll records five of the six as `Live/Work Condominium` and one
as `Office - Condominium`, all built 1996, with unit areas 741 / 1,195 / 1,257 / 1,947 /
2,262 / 2,345 sq ft (9,747 sq ft total). The architect's own project record describes
"four residential units and two commercial spaces … framed entirely in lightweight
steel", with "non-toxic, renewable, and recycled materials".

The DataSF EAS address file lists **86, 88, 90, 94 and 96** South Park on this parcel and
**does not list 92 at all**. 92 exists because of a single SF building permit dated
**8 Oct 2003, "address assignment - additional"**, filed against 86 South Park alongside
identical assignments for 88, 90, 94 and 96 — six numbers, six units. A Kidder Mathews
lease flyer markets **"92 South Park St"** as a ±1,075 RSF ground-floor office, i.e. one
of the two commercial condominiums. LoopNet lists the whole property as
**"90–96 S Park St"**.

So this asset models the whole building. Anyone re-running the pipeline on 86, 88, 90, 94
or 96 South Park will arrive at exactly this parcel and exactly this GLB.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| Architizer, **"86 - 96 South Park" by LDP Architecture, Inc.** | The firm's own record: 4 residential + 2 commercial units, corner site, "overlay of geometries", lightweight-steel frame, "a complex vocabulary of materials that will express their nature and age gracefully". Also the **seven 1996–97 project photographs** (`JLSP_Front`, `JLSP_Back`, `JLSP_Deck2`, `JLSP_Entry2`, `JLSP_Ext_Statue`, `8912EXT`, `8912X1`) that carry nearly all the material evidence below |
| **SF Heritage, "The Rise of Modern SOMA"** (Woody LaBounty, 27 Oct 2025) | The 1996 date, the attribution, the phrase **"an ambiguated facade of cubic forms"**, the pre-1906 Georgian townhouses on the site, and the **only 2020s photograph** — which is what establishes that the copper has weathered from orange to dark chocolate |
| DataSF building footprints `ynuv-fyni` (2010 LiDAR) | The two footprints (`201006.0022147`, 208.7 m²; `201006.0149656`, 81.0 m²; both `mblr = SF3775116`) and their height statistics — front block median **11.15 m**, max **13.28 m**, std 1.51 m over 837 cells; rear bar median **12.32 m**, max 13.73 m, std 1.56 m over 324 cells; both peaking at **≈24.13 m NAVD88** |
| DataSF parcels `acdm-wktn`, blklot 3775116–121 | The 14.45 × 30.04 m, 435 m² corner parcel and the six identical condominium lots |
| SF Assessor rolls `wv5m-vpq2` | 1996; six live/work condominium units; unit areas; the Holman-Levy ownership of lot 118 (94 South Park) |
| SF building permits `i98e-djp9` | Application 9318430 (20 Oct 1993) and its 1994–95 revision run; the 8 Oct 2003 address assignments; a 2015 ground-floor office fit-out; 2024 reroofing; a 2025 third-floor bathroom remodel. `number_of_existing_stories` reads **4** on every permit from 2015 onward |
| OSM ways 113545691 / 113545685 | `building = apartments`, `building:levels = 4`; cross-check footprints |
| Overture Maps buildings (the bake's own input) | The two polygons over this lot that the exclusion zone has to reach — see §7 |
| Google Maps satellite, Vexcel 2026 | The current roofscape: a triangular skylight over the front block, a curved element at the court's south end, and the open court itself |

## 3. Verified dimensions

| Item | Value | Confidence |
|---|---|---|
| Parcel | 14.448 × 30.042 m, 435 m² | **measured** (build report) |
| Frontage bearing | **135.1° true** (SE), flanks 45.2° / 225.2°, rear 315.1° | **measured** |
| Built footprint | 289.7 m² of 435 m² — front block 208.7, rear bar 81.0 | **measured** |
| Storeys | 4 | **verified** |
| Front block roof deck | 11.15 m | **measured** — LiDAR median |
| Rear bar roof deck | 12.32 m | **measured** — LiDAR median |
| **Corner-tower crest (target height)** | **13.28 m** | **measured** — LiDAR max on the front block; see §6 |
| Anchor (WGS84) | **`-122.3941549, 37.7819082`** | **measured** — the shipped GLB's XY bbox centre |
| Plinth top / floor lines | 3.55 / 6.15 / 8.75 m | *inferred* from the 1996 frontage photographs against the LiDAR deck |

## 4. Observations from all four sides and above

**South-east — South Park Street (14.45 m, the hero elevation).** Four storeys as three
cubic volumes that align at neither the floor lines nor the parapet. At the south corner
a projecting weathering-metal tower runs the full height above every other parapet, with
a **saturated red column** up its outer corner. North-east of it a silver metal-panel
volume under a **raked parapet** — a straight diagonal — then a further volume stepped
back ~0.35 m with a rust band across its fourth floor. Windows are large, rectangular,
near-black-framed and deliberately unaligned; several carry projecting hinged sunshade
panels, one a shallow balcony with a teal rail. The ground floor is a **blue-black glazed
tile plinth** carrying two commercial shopfronts, a recessed entry with an orange-red
door, and a thin **mosaic accent stripe** at ~1.6 m.

**South-west — Jack London Alley (30.04 m).** Photograph `JLSP_Back` shows it whole:
lead-coated metal panel over three storeys in large flat sheets with faint diagonal
creases; sparse punched windows; at the north-west end a **copper-shingle panel cut to a
raked triangular profile**; the tile plinth with its mosaic stripe and **two beige
roll-up garage doors**.

**North-east — the party wall with 84 South Park.** Blank where the two buildings touch;
the narrow arm behind it encloses the court and carries an external steel stair on its
court face.

**North-west — the rear.** **Not observed by any source consulted.** Authored as a blunt
service face in the body material.

**The court (~5 × 14 m, open).** Photograph `JLSP_Deck2` is taken in it: chequered warm
and gray slate paving, a **curved corrugated galvanized wall** at the south end, an
external steel stair with teal rails, curved balcony rails, a Cor-Ten volume above with a
raked parapet, and a dark projecting box with recessed downlights oversailing.

**Above.** Four parapet heights and one rake. The 2010 LiDAR's 1.5 m height standard
deviation across both polygons is the stepped massing, not noise. Current aerial imagery
adds the triangular skylight, a roof deck with rail, mechanical, and two polished
stainless flues rising past the court elevation.

## 5. Massing recipe as built

Lot frame: `s` runs along the frontage from the Jack London Alley corner (s = 0) to the
84 South Park party line (s = 14.448); `t` runs into the lot from the front property line
(t = 0) to the rear (t = 30.042).

| Mass | s | t | Deck | Parapet |
|---|---|---|---|---|
| A — front block | 0 … 9.40 | 0 … 15.95 | 11.15 | **raked** 12.60 → 11.45 |
| A2 — stepped-back east half | 9.40 … 14.45 | 0.35 … 15.95 | 11.15 | 11.45 |
| A′ — corner tower | −0.40 … 4.30 | −0.40 … 4.30 | — | **13.28 crest** |
| A1_cube — oversailing copper cube | 1.30 … 4.60 | 12.55 … 16.50 | 12.60 | — |
| B — rear bar | 0 … 6.60 | 15.95 … 30.04 | 12.32 | 12.62 |
| C — party arm | 11.70 … 14.45 | 15.95 … 25.65 | 11.15 | 11.45 |
| court | 6.60 … 14.45 | 15.95 … 30.04 | floor at 0.06 | walls 2.60 |

## 6. Why 13.28 m and not 13.73 m

The two footprints give two LiDAR maxima 0.45 m apart. They are not measurements of
different things: their absolute first-return peaks are **24.11 and 24.15 m NAVD88** —
the same physical high point — and the difference is entirely in the two polygons' ground
references. This build takes **13.28 m**, the front block's `hgt_maxcm`, because that
polygon lies wholly inside the parcel while the rear bar's overhangs the north-west
parcel line by ~1.6 m into the backs of the Bryant Street block, so part of its ground
statistic is somebody else's grade. If a measured source puts the tower above 13.3 m, the
target height moves and the manifest entry with it.

## 7. Exclusion window (for stage 5)

`excluded()` drops a footprint when its area centroid **or any ring vertex** falls inside
the radius, and both DataSF and Overture bind. Measured from the **plan** anchor
(`-122.3941630, 37.7819166`) against the two files the bake reads, after
`simplifyRing(0.6)`:

|  | centroid | nearest vertex |
|---|---|---|
| own front block (DataSF `SF3775116`) | 7.18 m | 0.83 m |
| own rear bar (DataSF `SF3775116`) | 9.17 m | 3.13 m |
| own Overture twin `552799e9…` (h 10.8) | 7.04 m | 1.53 m |
| **own Overture twin `ea748f47…`** (OSM, 4 floors, no `height`) | **4.67 m** ← lower bound | 13.53 m |
| **84 South Park (Overture `0b2c3805…`, h 11)** | **10.45 m** ← upper bound | 13.04 m |
| 84 South Park (DataSF `SF3775055`) | 10.90 m | 13.29 m |

Both ends are set by **centroid** tests, which is unusual — sizing this radius off
vertices alone gives the wrong answer at both ends. **The shipped anchor is 1.06 m from
the anchor these numbers were measured at, so stage 5 must re-measure before committing
a radius.** The plan's provisional value is `exclude: 7.5`.

## 8. Palette as built

| Element | Material | Hex |
|---|---|---|
| Lead-coated zinc body, court walls, curved corrugated wall | `Toy_steel` | `9aa0a6` |
| Corner tower, oversailing cube, rear bar's court face, fourth-floor band | `Toy_rust` | `a86444` |
| Copper-shingle raked panel, Jack London Alley end | `Toy_cocoa` | `6b4a3d` |
| Ground-floor glazed tile plinth, court enclosure walls | **`Toy_bluestone`** (extension) | `2f3a44` |
| Court paving | **`Toy_greige`** (extension) | `b0aa9e` |
| Window frames, sunshades, shopfront frames, doors, roof hatch | `Toy_ink` | `3a3530` |
| **Red corner column** | `Toy_ioorange` | `c0402a` |
| Mosaic accent stripe, balcony and stair rails | `Toy_teal` | `3fa8a0` |
| Glazing | `Toy_glass` | `2a4d73` |
| Shopfronts, skylight | `Toy_glassl` | `6f95b8` |
| Roll-up garage doors | `Toy_sand` | `ece4d4` |
| Roof decks, stair treads | `Toy_roofd` | `45454a` |
| Stainless flues, roof rail, mechanical | `Toy_trim` | `f3efe6` |
| Shopfront / entry / court night glow | `Toy_gold_Glow` | `caa64a` |
| Lit upper windows | `Toy_glass_Glow` | `6f95b8` |

Two palette extensions, both recorded as WARN in `REPORT.md` §4.

## 9. What is inferred rather than measured

- Every floor line below `Z_DECK_A` (plinth top 3.55, floors at 6.15 and 8.75).
- The **positions** of the materials come from photographs taken in 1996–97; only their
  weathered **appearance** comes from 2025. Nothing in the permit record suggests a
  re-clad, but nothing rules one out either.
- The rear (north-west) elevation is entirely reconstructed.
- The court's current contents: the 1996 photographs establish the curved wall, the
  external stair and the paving; the skylight comes from 2026 aerial imagery; a pale
  object over part of the court in that imagery is unexplained by any source and is not
  modelled.
- The red column is fattened to 0.42 m from a real ~0.2 m — style bible §9 semantic
  exaggeration, not a measurement error.
