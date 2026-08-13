# 234 Van Ness Avenue — The Kelsey Civic Center — reference dossier

Research behind `234-van-ness.glb`. Compiled 13 August 2026 from the sources in
§2. Anything marked *inferred* is visual reasoning, not a published figure.

## 1. Identity — and its four names

| Alias | Where it comes from |
|---|---|
| **The Kelsey Civic Center** | the building's own name (The Kelsey + Mercy Housing) |
| **234 Van Ness Avenue** | the Van Ness street number of the parcel frontage; the form SF YIMBY files it under, and the form this asset is slugged with |
| **240 Van Ness Avenue** | the address the architect, developer and press publish |
| **165 Grove Street** | the assessor's address for the assembled lot |

All four are one building: **block 0811, lot 0811204**, created 2022-09-17 out of
lots 0811016 / 018 / 019 / 021. Recording every alias here so the app's search
index finds the building whichever way a visitor asks for it.

| Item | Value | Confidence |
|---|---|---|
| Architects | WRNS Studio with Santos Prescott & Associates | verified |
| Developers | Mercy Housing California + The Kelsey | verified |
| Contractor | Cahill Contractors | verified |
| Ground broken / topped out / opened | mid-2023 / Aug 2024 / Oct 2025 | verified |
| Programme | 112 apartments (80 studios, 32 two-bedroom) at 20–60 % AMI, 25 % reserved for people with disabilities; ~1,400 sq ft Disability Cultural Center; ground-floor retail; 62 bike spaces | verified |
| Cost | $88.3 M | verified |
| Storeys | 8, all at grade; **no basement** (the previous building's was filled) | verified |
| Site | 13,815 sq ft (1,283 m²) | verified (geotechnical) |
| Courtyard | 3,450 sq ft (320 m²), open-air, at ground level | verified |
| Structure | mat foundation on drilled displacement columns; all-electric | verified |

## 2. Sources

1. **WRNS Studio, `SOUTH ELEVATION - TOM WADDELL`, 1/8" = 1'-0"** — published via
   SF YIMBY, January 2021. The most valuable source in this dossier: it carries
   the complete level schedule and the material keynotes, and every height in §4
   is read off it.
   https://sfyimby.com/2021/01/renderings-for-the-kelsey-civic-center-at-240-van-ness-avenue-civic-center-san-francisco.html
2. **SF YIMBY, "Grand Opening For The Kelsey Civic Center", October 2025** — the
   completion account ("84 feet tall", the L-shaped footprint wrapping a central
   courtyard, "vertical bands of textured fiber cement panels and vertical
   copper-anodized aluminum fins", the unit mix) plus four **Bruce Damonte**
   photographs that are the primary visual reference for §5: an establishing
   dusk view up Van Ness with City Hall, a sunlit three-quarter of the Van
   Ness/Waddell corner, the courtyard, and the rooftop deck.
   https://sfyimby.com/2025/10/grand-opening-for-kelsey-civic-center-at-240-van-ness-avenue-san-francisco.html
3. **Rockridge Geotechnical project page** — 13,815 sq ft site footprint, 8
   levels at grade, no basement, mat foundation, $88.3 M, 2025 completion.
   https://www.rockridgegeo.com/projects/affordable-senior-housing/the-kelsey-civic-center/
4. **WRNS Studio project page** — authorship, the 3,450 sq ft garden courtyard,
   rooftop deck, commons and retail programme.
   https://wrnsstudio.com/projects/the-kelsey-civic-center/
5. **The Kelsey / Mercy Housing** — programme, AMI bands, and the
   disability-forward design process that drove the plan.
6. **OpenStreetMap** — ways `1547771521` and `1547771522` (`building=yes`, both
   created 2026-08-06 by user *pootriarch*, untagged), the built footprint; way
   `8917756`, Dr. Tom Waddell Place.
7. **DataSF parcels** (`acdm-wktn`) — block 0811, the 2022 lot assembly and its
   geometry; **DataSF 2010 LiDAR building footprints** (`ynuv-fyni`, as bundled
   in `pipeline/data/buildings_datasf.geojson`) — the footprints the tile bake
   actually reads, and the basis of the exclusion arithmetic in REPORT.md.

No photograph of the Grove Street elevation or of either party wall was located.

## 3. Footprint, anchor, orientation — *measured*

OSM ways 1547771521 + 1547771522 unioned along their shared edge and reprojected
with the app's tangent projection (`LON0 −122.4375`, `LAT0 37.77`):

- union area **1,304 m²** vs the geotechnical report's 1,283 m² — **1.6 %**.
  That agreement is the whole reason two untagged, one-week-old, unverified OSM
  traces are trusted as this building's footprint.
- axis-aligned extent 55.60 m (E–W) × 44.80 m (N–S)
- minimum-area OBB 54.10 × 36.58 m at **170.75°** — the Civic Center grid
- **anchor (model origin = ring AABB centre): `−122.4193071, 37.7780541`**
- furthest ring vertex from the anchor: 34.02 m

Expressed in the building's own grid (u along the Dr. Tom Waddell frontage from
its west end, v into the block), the survey ring is startlingly rectilinear:

```
(0.00, 0.00) (54.10, 0.00) (54.02, 11.26) (54.07, 22.20) (54.09, 36.58)
(31.57, 36.40) (31.74, 21.88) (31.81, 15.49) (0.29, 15.46)
```

so the model is built on a **regularised L** — `u ∈ [0, 54.06] × v ∈ [0, 15.47]`
plus `u ∈ [31.70, 54.06] × v ∈ [15.47, 36.58]`. **No vertex moves more than
0.30 m** and the area lands at 1,308 m² (+0.3 %). The L is what the eye reads;
the 80 mm wobble in the east party line is survey noise.

Three public faces and two lot lines:

| Face | Length | Outward normal | What it is |
|---|---|---|---|
| south | 54.06 m | 170.7° | **Dr. Tom Waddell Place** — the long face |
| west | 15.47 m | 261.8° | **Van Ness Avenue** — the address frontage |
| north (wing) | 22.36 m | 350.3° | **Grove Street** |
| east | 36.58 m | 80.8° | party line against 101 Grove |
| west + north (bar) | 21.11 + 31.70 m | 260.1° / 350.7° | lot lines against the 171 Grove corner building and 244 Van Ness |

**The building wraps a corner it does not own.** The Van Ness/Grove corner is a
separate lot (171 Grove) carrying a standing one-storey commercial building —
which is the low stucco block immediately north of the white mass in source 2's
photographs, and the reason the L has a notch in it.

Dr. Tom Waddell Place is a one-way service alley about 6.4 m clear of the south
wall; the "DO NOT ENTER" sign in the corner photograph stands in it.

Authored `+Y` = true north, `+X` = east. The contract's "front faces −Y" cannot
be honoured — the address front faces west — so real-world orientation wins per
AGENTS rule 5.

## 4. Heights — *measured off source 1*

| Datum | Drawing | Metres |
|---|---|---|
| Level 1 (grade) | 0'-0" | 0.000 |
| Level 2 | 15'-0" | 4.572 |
| Levels 3–8 | +9'-11" each | 7.595 / 10.617 / 13.640 / 16.662 / 19.685 / 22.708 |
| **ROOF** | **84'-5"** | **25.730** — the published "84 feet above Van Ness" |
| Copper fascia / parapet top | +3'-6" | 26.797 |
| **Mechanical penthouse crest** | **+14'-5"** | **30.120** — the bbox top |

The tall ground floor over seven short residential floors is the whole facade
rhythm, and it is built on these lines rather than on a uniform division.

## 5. What each side shows

**South (Dr. Tom Waddell Place), 54 m — the long face.** A 15'-0" textured
concrete base with storefront glazing, painted aluminium vents, an anodized
coiling door and hollow-metal service doors. Above, seven floors of strict
vertical rhythm: broad white fibre-cement panel bands alternating with narrower
charcoal window-wall bays, each bay a stack of vision glass over opaque glass
infill, divided by slim copper-anodized fins running the full seven storeys
uninterrupted. A copper-anodized fascia band caps the wall at 25.73 → 26.80 m —
the one warm horizontal on a cool elevation. Behind it, set back, the
fibre-cement penthouse and its darker anodized mechanical screen.

**West (Van Ness Avenue), 15.5 m — the address face.** The same system, only 15 m
wide: a narrow white end wall with three bays and a scatter of coral accent
panels. At the south-west corner a **projecting glazed bay** stacks six storeys
of large charcoal-framed windows and cantilevers over the ground floor on a
copper-toned soffit — the strongest street-level move on the building. Below it,
glazed lobby and retail under a **wood-slat trellis canopy** on charcoal steel
outriggers.

**North (Grove Street), 22.4 m.** *Inferred* from the same facade system; no
photograph located.

**East and the two west lot lines.** *Inferred.* Party walls: the same white
panel field, far fewer openings, no fins, plain parapet.

**The courtyard — the identity.** An open-air court cut through the wing. Its
walls are the opposite of the street: eight storeys of full-height vertical panel
stripes in sky blue, coral, mustard, olive-green, pale blue, cream and charcoal,
in an irregular patchwork with no two adjacent bays alike. One wall carries
**open-air access galleries** — a stack of cream decks behind light metal picket
railings, with a warm orange-red perforated screen at one end. The ground plane
is pale plank paving and grey unit pavers with planted beds, small trees, loose
seating and a festoon of catenary lights; one end wall is a flat mustard-yellow
plane. A big soft segmental arch frames the covered passage into it.

**The roof.** An occupied deck facing City Hall: pale concrete pavers, dark
bronze raised planters with vivid mixed planting, wood-topped benches, a
perimeter guardrail of fine vertical pickets, and the penthouse with its
mechanical screen. Nothing else.

## 6. Recognition cues (ranked)

1. **The open courtyard with candy-coloured walls** — visible only from above,
   which is exactly where the app's camera is.
2. **The white-and-charcoal vertical stripe** with thin copper fins and the
   copper fascia lid.
3. **The L that wraps a corner it does not own.**
4. **The projecting glazed corner bay** at Van Ness and Waddell.
5. **The planted roof deck** facing City Hall.

## 7. Preserve / simplify

**Preserve** — the regularised L and its notch; the 15'-0"-over-7×9'-11" storey
rhythm; the courtyard void and its colour patchwork; the fin-and-band vertical
system; the copper fascia; the corner bay; the planted roof deck.

**Simplify** — panel joints, fin profiles, mullion patterns, balcony pickets and
railing infill all disappear; window bays become one charcoal reveal with a
vision slab and an infill slab per floor; the courtyard patchwork becomes ~40
full-height stripes rather than a per-floor mosaic; the trees become a trunk and
one hexagonal crown each; the guardrail becomes two rails and 0.10 m pickets at
1.1 m pitch.

**Do not add** a tower, a signature curve, rooftop signage or silhouette drama.
This building's job in the scene is to be the crisp modern block that makes City
Hall across the street look monumental.

## 8. Uncertainties

1. **The courtyard's exact position and size is the largest inference here.**
   3,450 sq ft is published; *where* it sits in the L is reasoned from the
   massing and the photographs, not read off a plan. The modelled void is
   15.80 × 18.30 m in the building grid, sitting at the junction of the bar and
   the wing with the east party wall as its fourth side — which is what makes
   the resulting floor plate (≈ 989 m²/floor) land where 112 units over seven
   floors needs it, and what puts the open-air access galleries on the thin
   4.9 m western strip exactly where the photograph shows them. Any published
   floor or site plan overrides it.
2. **The arch's location** is inferred to the courtyard's south wall. The
   photograph proves the arch exists and is big; the dimensioned south elevation
   shows a service-heavy Waddell ground floor, which argues against a street
   portal there.
3. **Grove elevation and both party walls are inferred** from the photographed
   system.
4. **The courtyard colour sequence is designed, not surveyed** — the palette is
   read off one photograph of two walls; the sequence is the modeller's, and is
   a fixed list in the build script so the model rebuilds identically.
5. **The OSM footprint is one week old, untagged and single-sourced.** The 1.6 %
   agreement with the geotechnical site area is what makes it trustworthy.
