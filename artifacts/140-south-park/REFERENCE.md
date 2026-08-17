# 140 South Park Street — reference dossier

Compiled 16 August 2026 for the SF-SIM miniature GLB, from the sources in §2.
Everything here was re-verified during the build; where this file and
`docs/asset-plans/140-south-park.md` disagree, **this file is correct**.

## 1. What the building is

A two-storey **light-industrial loft of 1907** on the north-west rim of the South Park
oval in SoMa, San Francisco, at the oval's west tip. Two levels: a ground floor
converted from industrial use to retail in 2016, and an office floor above it. Wood
frame, flat roof, no parapet, a bracketed cornice on the street front.

It is a **contributor** to the potential South Park Historic District (CHRSC status code
`5D3`), classified `HP8. Industrial`. The district's survey singles it out by name:

> The light industrial building at 140 South Park Street (1907) features wood frame
> construction, like the residential buildings going up at the time, instead of brick.

Every other industrial building on the oval — 17–19, 21–27, 135, 156 — is brick or
reinforced concrete. This one is a carpenter's building, and that is the whole design
argument of the asset.

It sits on a **6.84 m frontage**, the narrowest in the district, running 29.81 m back
from the oval toward the Bryant Street block: a 4.4 : 1 stick. The south-west long flank
is a **party wall** shared with 150 South Park at a 0.00 m gap; the north-east long flank
stands open onto a ~6 m paved **side passage** and is a real elevation.

Assessor / OSM identity: APN **3775-064**, OSM way **124884359**,
`addr:housenumber = 140`, `addr:street = South Park`, DataSF LiDAR footprint
`mblr = SF3775064`.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D continuation sheets, 30 June 2009 (`https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf`) | 1907 date; APN 3775-064; property type `HP8. Industrial`; contributor status `5D3`; and the p.5 statement that this building is **wood frame instead of brick**, the only building in the district given that treatment. Also fixes the neighbours: 150 South Park (3775-065) is a 1959 non-contributor, 136 South Park (3775-063) was recorded **vacant** in 2009 |
| DataSF Building Footprints, LiDAR-derived (`https://data.sfgov.org/resource/ynuv-fyni`) | the authoritative footprint polygon (200.8 m², 808 × 0.25 m² cells) and the height statistics: modal cell **9.89 m**, median 9.88 m, mean 9.57 m, **max 10.68 m**, min 2.99 m, ground 7.37 m NAVD88. Source raster `Sanfran_Orig_1381.flt`, **flown 2010** |
| SF Assessor Historical Secured Property Tax Rolls (`https://data.sfgov.org/resource/wv5m-vpq2`) | 1907; block 3775 lot 064; **2 storeys**, 2 units, in all 19 rolls 2007–2025; Industrial → **Commercial Office** in the 2018 roll |
| SF Building Permits (`https://data.sfgov.org/resource/i98e-djp9`) | 2005 "repair loose **stucco** in front of building & rotted wood around window"; 2016-04 change of use to 1st-floor retail + 2nd-floor office with **new storefront windows on the south elevation**; 2016-10 seismic upgrade; 2017-03 ground floor re-framed from wood joists to slab on grade; **2018-03 correction "no existing parapet"**; 2018-11 and 2019 tenant improvements; 2019-02/03 VRF mechanical with a **relocated condensing unit** |
| OSM way/124884359 | cross-check footprint (208.2 m², within 3.6% of DataSF); `height = 10` |
| Google Street View, South Park Street pano, captured **Jan 2025** | the entire front elevation in detail (see §4) |
| Google Maps place imagery for 140 S Park St | the north-east side passage, its corrugated opposite wall, and the exposed flank |
| Google Maps satellite, Vexcel imagery 2026 | flat roof; a mechanical cluster toward the middle of the bar |
| CompStak property record | 1907 built / 2018 renovated; 2 storeys; 4,310 SF; class B office; APN 3775-064; tenant Flourish Ventures (lease 2025–2028) |
| SF Registered Business Locations (via opengovus) | Thomvest Ventures LLC trades as "140 South Park Street" but is **registered at 138** — the reason press about a South Park VC office is not about this building (see §7) |

## 3. Verified dimensions, location and orientation

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.3947379, 37.7814643` | **measured** — OBB centre of the DataSF footprint |
| Footprint area | 200.8 m² (DataSF) / 208.2 m² (OSM) | **measured** |
| Overall OBB | **29.81 × 6.84 m at 45.0°** off the world axes | **measured** |
| Frontage on South Park | **6.84 m** | **measured** |
| Depth | 29.81 m (SW party wall) / 29.72 m (NE flank) | **measured** |
| Roof deck | **9.85 m** above grade | **measured** — LiDAR modal cell (`hgt_majoritycm = 989`), median 9.88 m; OSM `height = 10` agrees |
| **Cornice crest** | **10.68 m** | **measured** — LiDAR `hgt_maxcm = 1068`; see §7 for why the maximum is safe here |
| Ground elevation | 7.37 m NAVD88 (`gnd_min_m`) | measured; the app's terrain handles this, not the asset |
| Street frontage heading | faces **135.0° (SE)** | **measured** from the footprint |
| Long flanks | run 45° / 225° | **measured** |
| Storeys | 2 | **verified** |

Measured footprint in the lot's own frame (metres, `+u` = north-east across the lot
toward the side passage, `+v` = north-west along it toward the rear, origin at the
anchor), CCW:

```
(-3.325,  14.900)   rear,  south-west
(-3.419, -14.905)   front, south-west
( 3.422, -14.904)   front, north-east
( 3.327,  14.812)   rear,  north-east
```

World coordinates follow from `(E, N) = (u cos45° − v sin45°, u sin45° + v cos45°)`.
Shoelace area of the built ring is **200.77 m²** against DataSF's 200.8 m² — the two
collinear DataSF vertices on the party-wall side were dropped (they lie on the line to
within 5 mm) and nothing else was simplified.

## 4. Observations from all four sides and above

**South-east — South Park Street (the hero elevation, 6.84 m wide).** Two very tall
storeys under a bracketed cornice, painted one dark desaturated gray-green throughout.
From the top: a plain flat cap band; a projecting crown moulding; a row of small
**modillion brackets**, about nine across the frontage, reading from the street as a dark
dotted line under a lighter edge; then a plain field of **horizontal lap siding**
carrying three tall windows in near-black frames — a wider centre light between two
narrower ones, each divided into a grid of small panes three rows deep — over a plain
apron. A strong horizontal **recessed panel band** separates the floors. The ground floor
is a near-black timber shopfront the full width: a **transom band** of glazing across the
top, a wide multi-pane display window at the south-west (150 South Park) end, a
**natural-wood glazed double door** right of centre on a stone threshold, and a narrow
dark service door at the north-east end. A red fire department connection and an alarm
bell sit on the south-west pier.

**South-west — the party wall with 150 South Park (29.81 m).** Blank. 150's own facade
runs hard against it; the two footprints share a node exactly. Nothing on this flank is
visible from anywhere in the city, and it is modelled with no openings at all.

**North-east — the side passage (29.72 m).** The full depth of the wall stands open onto
a paved passage about 6 m wide with a corrugated white wall opposite. Plain body colour,
lap siding, a downpipe, and one or two small high windows read at an oblique in the Jan
2025 imagery. This is 29.7 m of wall the app's downward camera sees end to end.

**North-west — the rear (6.65 m).** **Not observed by any source consulted.** It stands
~6 m off the rears of 473 and 477 Bryant Street. Modelled as a blunt service face — a
door and one high window — on the strength of the type. *Inferred.*

**Above.** A flat roof with **no parapet ring** (2018 permit correction, explicit). The
2010 LiDAR is nearly uniform across all 200 m² — modal 9.89 m, median 9.88 m — which
proves the roof carried **nothing** when it was flown, and makes the 10.68 m maximum the
cornice at the street edge rather than any rooftop object. The 2026 satellite shows a
mechanical cluster toward the middle of the bar, which the 2019 VRF permit accounts for.

**Two roof elements are inferred, not measured, and are labelled as such:**

- the **condenser pair**'s position and count (permit-attested that they exist; position
  read off 2026 satellite imagery)
- the **two flush skylights** over the middle of the plan. A 29.8 × 6.8 m loft with
  window walls only at its two short ends has no daylight at all across its middle 20 m,
  and every South Park building of this depth solves that from above. Their 0.18 m kerbs
  sit inside the 2010 LiDAR's noise (deck standard deviation 1.11 m over 0.5 m cells), so
  the survey neither confirms nor rules them out. They are a **typological
  reconstruction**, and they are also what stops 200 m² of deck reading blank under the
  app's downward camera (style bible §10).

## 5. Recognition cues

1. **The stick.** 6.84 × 29.81 m, 4.4 : 1. From above, a long dark bar in a row of broad
   pale blocks. Nothing else on the oval is this slender.
2. **The dark gray-green body.** 150 next door is white over black, 155 is white, 135 is
   dark brick, 126 and 112 are pale. A mid-dark desaturated green-gray is a value and hue
   slot no neighbour on the rim holds.
3. **The bracketed cornice**, the only ornament on the building and also its crest.
4. **Three tall black-framed windows over a black shopfront** — a dark-base /
   dark-openings / dark-cap value stack on a mid-dark wall.
5. **The wood double door**, the single warm saturated thing on the building.

## 6. Massing recipe as built

One mass. No wing, no step, no rear block — the survey shows a single near-rectangular
prism.

| Element | Z (m) | Basis |
|---|---|---|
| Grade | 0.00 | |
| Shopfront doors / display head | 3.35 | inferred from the frontage photograph |
| Transom band | 3.50 → 4.20 | observed |
| Storefront head | 4.35 | observed |
| Panelled belt band | 4.35 → 5.20 | observed |
| Upper window group | 5.60 → 8.55 | observed proportions |
| Cornice frieze | 8.90 → 9.25 | observed |
| Bracket row | 9.25 → 9.72 | observed; **enlarged**, see §7 |
| Crown moulding | 9.72 → 10.14 | observed |
| **Cornice cap crest** | **10.68** | **measured** — LiDAR `hgt_maxcm`; sets the bbox top exactly |
| Roof deck | 9.85 | **measured** — LiDAR modal cell |
| Deck fascia (flanks + rear only) | 9.85 → 10.00 | permit: no parapet |
| Condensers / skylights / hatch / vent | ≤ 10.57 | all kept under the crest |

## 7. Palette map

| Element | Material | Hex |
|---|---|---|
| Body walls, cornice frieze, crown, cap, belt band | **`Toy_olive`** (palette extension) | `5f655c` |
| Shopfront frame, window frames, mullions, bracket row, service doors | `Toy_ink` | `3a3530` |
| Wood entrance doors | `Toy_oak` | `c08e50` |
| Glazing, transom | `Toy_glass` | `2a4d73` |
| Skylights | `Toy_glassl` | `6f95b8` |
| Roof deck, hatch, condenser plinth, door fills | `Toy_roofd` | `45454a` |
| Condensers, vent, downpipe | `Toy_steel` | `9aa0a6` |
| Fire department connection | `Toy_red` | `c4453c` |
| Shopfront + transom night glow | `Toy_gold_Glow` | `caa64a` |
| Upper window night glow (two of three lights) | `Toy_glass_Glow` | `6f95b8` |

## 8. Corrections to the plan, and what stayed uncertain

- **Nothing in the plan's measured section needed correcting.** The anchor, the
  footprint, the OBB, the heading, the roof deck and the crest were all re-derived from
  DataSF and OSM during the build and matched to the metre.
- **The transom band was re-materialled.** The plan specified `Toy_glassl`; the first
  aerial put a bright blue bar across the whole frontage that read as a light fixture
  rather than glazing. It is `Toy_glass` with three ink mullions instead.
- **The roof gained two skylights**, which the plan did not have. See §4 — a
  typological reconstruction, labelled, and the fix for a blank 200 m² deck.
- **The night state lights two of the three upper windows, not three.** Every window lit
  reads as a render rather than as a building, and it competed with the gold shopfront
  that is supposed to be the hero.
- **The bracket row is deliberately enlarged.** The cornice assembly reads about 1.2 m on
  the photograph; it is built at 1.78 m (8.90 → 10.68). Semantic exaggeration under style
  bible §9 — at the app's camera a 1.2 m cornice on a 6.84 m frontage is three pixels and
  the building loses its only ornament. This is a design decision, not a measurement.
- **Stucco or siding is still unresolved.** The 2005 permit repairs "loose stucco in
  front of building"; the Jan 2025 photograph reads as horizontal lap siding under paint.
  The asset builds **siding**, because the 2016 renovation was extensive enough to have
  stripped a stucco skin and because the DPR's emphasis on wood-frame construction makes
  siding the typologically expected finish. This is the most likely thing here to be
  wrong.
- **The cornice is undated.** Nothing establishes whether it is original 1907 or a 2016
  restoration. It is on the building now, which is what the asset models.
- **The rear elevation is unobserved** and is a reconstruction.
- **This is not 138 South Park.** Thomvest Ventures is registered at 138 and its "140
  South Park Street" DBA is a trading name. The Perkins&Will "South Park Venture Capital
  Firm" project — 16,420 sq ft, brick-clad, "originally built in the 1920s" — contradicts
  this building on all three counts (4,310 sq ft, wood frame, 1907) and is the neighbour.
- **No architect or builder is recorded** for the 1907 building in any source consulted.
