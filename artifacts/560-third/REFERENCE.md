# 560 Third Street — reference dossier

Compiled 16 August 2026 for the miniature GLB in this folder. Everything below is
either **measured** (a figure taken from a cited dataset or from geometry), or
labelled *derived* / *inferred* where it is not.

## 1. What this building is

A 1941 two-storey light-industrial infill on a 30 × 80 ft lot on the south-west
side of 3rd Street, between South Park and Brannan. Re-fitted in 2015–16 and
opened in January 2017 as Poppin's San Francisco showroom (street-level access
plus a second floor for ~35 people); since then a small-tenant office address.
Its street elevation was re-skinned in that renovation into a flat near-black
storefront-and-loft front — which is what the asset models.

Its structural role in the block is what makes it worth building: it is the
**low dark notch**. 550 Third to the north-west is 7.23 m to its roof and 11.0 m
to its post-2025 penthouse; 574 Third to the south-east is 11.05 m to its roof
and 15.4 m to its billboard crest. This building's parapet is 7.2 m, so it sits
in a four-metre-deep slot with party walls on three sides and one 9.4 m public
face.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/124903642 | footprint geometry; `addr:housenumber=560` (`addr:source:housenumber=survey`); `height=7` (Bing stereo trace) |
| DataSF Assessor rolls `wv5m-vpq2`, block 3776 lot 007 | 1941; 2 storeys; Industrial use, SLI zoning; 3,390 sq ft building on a 2,400 sq ft lot; `lot_depth` 80 ft |
| The same query on lots 005 and 008 | the two neighbours (1921 / 2 storeys / 19,997 sq ft; 1907 / 3 storeys / 58,530 sq ft) — the comparison that fixes this as the low building on the block face |
| DataSF DBI permits `i98e-djp9`, block 3776 lot 007 (10 records, 1993–2016) | reroofing 1993 and 2013; the 2015–16 interior renovation (demolished partitions, accessible toilets, new stairs, a new walkway joining two 2nd-floor areas, Title-24 lighting); Type V wood-frame entries; the office → "warehouse, no furniture" occupancy correction |
| DataSF LiDAR footprints `ynuv-fyni`, record `SF3776007` | 993 half-metre cells (≈248 m², corroborating the OSM polygon); ground mean 6.82 m (range 0.53 m); **height median 6.66 m**, majority 6.57 m, σ 0.88 m, max 11.43 m |
| Poppin lease press release (Nov 2016) | 560 Third Street, ~4,200 sq ft, street-level access plus a second floor for ~35 employees, opening January 2017 |
| Poppin showroom blog post | the SF space is loft-style with abundant natural light and a "treehouse" feel from the street tree seen out of the upstairs loft — the basis for reading the roof rectangles as skylights, and confirmation that the upper floor is one open volume behind the street window band |
| KartaView seq 13089 / 12016 / 10065 / 10657 (Jul–Aug 2016), 3rd Street looking NW | the block sequence brown (574) → **charcoal (560)** → cream (550); the two-storey proportion; the parapet line against 574's third floor |
| KartaView seq 50032 frame 1811 (2017-02-23, dusk) | **the night reference**: the upper glazed band lit warm amber across the full frontage with the ceiling and fittings visible through it; the ground floor almost dark |
| Esri World Imagery z20 (oblique) | the roof: pale membrane, two bright rectangles, the SE half in 574's permanent shadow. The frame leans, so roof-object positions from it are approximate |

Identification of *which* building on the block face is 560 was not taken on
faith: the OSM footprints of 550, 560 and 574 were reprojected and drawn as a
block plan, and then projected into the KartaView frames using each frame's GPS
position and a heading derived from its neighbouring frames. 574's projection
lands on the brown block with the "574" number plate; 550's lands on the cream
one; 560's lands on the charcoal building between them.

## 3. Measured geometry

Reprojected with the app's tangent projection (LON0 −122.4375, LAT0 37.77;
x east, y north, metres) and recentred on the oriented-bbox centre:

```
( 11.71,   5.31)   v0  E corner   (Third St / 574 party line)
(  4.96,  11.86)   v1  N corner   (Third St / 550 party line)
(-12.03,  -4.99)   v2  W corner   (rear / 550)
( -4.97, -12.04)   v3  S corner   (rear / 574)
```

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| v0 → v1 | 9.40 m | 44.1° (NE) | **3rd Street front — the only public elevation** |
| v1 → v2 | 23.93 m | 315.1° (NW) | party wall with 550 Third |
| v2 → v3 | 9.98 m | 224.9° (SW) | rear party wall (550 Third wraps behind this lot) |
| v3 → v0 | 24.07 m | 134.9° (SE) | party wall with 574 Third |

- Shoelace area 232.6 m²; oriented bbox 9.98 × 24.06 m = 240.2 m².
- Anchor (oriented-bbox centre): **−122.3951188, 37.7804142**.
- Long axis 43.9° / 223.9° true.
- The polygon is slightly non-rectangular (9.40 m front, 9.98 m rear) because it
  is Bing-traced. It is built **as traced**, not "corrected" to the assessor's
  30 × 80 ft rectangle: the neighbouring footprints in the bake come from the
  same trace and line up with it.

## 4. Heights, and the one number that is not measured

| | |
|---|---|
| Roof plane | **6.66 m** — LiDAR `hgt_median_m`, majority 6.57 m. Measured. |
| Parapet crest | **7.20 m** — *derived*: roof plane + a 0.55 m parapet. |
| OSM `height` | 7 m — a Bing stereo trace that lands on the parapet edge. Corroborates the derivation; not independent of it. |

**The LiDAR maximum of 11.43 m is contaminated, not a rooftop object.** It is
within centimetres of 574 Third's measured 11.05 m roof and is bleed from the
shared party wall; σ 0.88 m against a 6.57 m majority says the same thing. No
bulkhead was modelled to explain it.

## 5. What each side shows

**North-east (3rd Street), 9.4 m — the only public face.** Flat near-black paint
from parapet to pavement. Upper storey: one wide glazed band running nearly the
full frontage, four tall panes on slim dark mullions in a shallow dark reveal,
solid spandrel below and plain wall above to the parapet. Ground floor: a dark
glazed shopfront, full-height glass door at the south-east (574) end, display
glazing beside it, narrow dark base rail, and a shallow horizontal head band.
Flat plain parapet with a thin cap; no cornice, no signage band, no ornament. A
mature street tree stands at the kerb — city property, not part of the asset, and
the reason most street photography of this facade is partly obscured.

**South-east, 24.1 m.** Blind party wall with 574 Third (11.05 m roof) —
entirely buried.

**North-west, 23.9 m.** Blind party wall with 550 Third (7.23 m roof, 11.0 m
penthouse) — entirely buried.

**South-west (rear), 10.0 m.** Not a street elevation. 550 Third's 48 m bar wraps
behind this lot; the "kink at v2" recorded in *550's* party wall
(`docs/asset-plans/550-third.md` §2.3) is the notch this building occupies.
Buried.

**Top.** Flat pale membrane at 6.66 m inside a low parapet, sunk four metres
below both neighbours. Two large bright rectangles read in the satellite frame —
one about a third of the way back from the street, one near mid-depth — read here
as skylights (*inferred*, see §7). Small scattered vents and a compact mechanical
cluster in the rear third. The south-east half of the roof is in permanent shadow
from 574's wall.

## 6. Recognition cues, ranked

1. **The dark notch** — a near-black two-storey box four metres lower than the
   walls either side, between a brown 3-storey block and a cream one.
2. **The upper glazed band** — one wide four-pane window filling most of a 9.4 m
   frontage; the whole elevation is that band, a spandrel and a door.
3. **The proportion** — 9.4 m wide, 24 m deep. A sliver.
4. **The two roof skylights** on a pale membrane, the only roof event in the slot.
5. **The night lantern** — at dusk one warm rectangle in a dark facade.

## 7. Uncertainties and conflicting evidence

- **The parapet crest is derived, not measured** (see §4). If a better source
  moves it, only `targetHeightM` and the parapet top move; the shell is measured.
- **The roof rectangles are inferred as skylights.** They could be roof hatches
  or mechanical housings. If they are not glazed, the asset loses its aerial
  night cue and the street band carries the night alone.
- **Construction type is contradictory.** DBI's 2015–16 applications say wood
  frame (Type V); a 2003 permit says Type 2; the assessor codes the parcel `C`.
  This is a live disagreement, not a settled fact. It changes nothing for a
  flat-colour miniature.
- **Use is contradictory on paper.** The assessor records Industrial; DBI's 2016
  administrative permit *corrects* the occupancy from office to warehouse; the
  building has been leased as showroom and office throughout. The asset ships as
  `cat: 3` (Office) because that is what stands there and what the neighbours use.
- **The imagery is old.** The closest facade views are July–August 2016 and
  February 2017, from the Poppin fit-out; the newest usable frame is March 2019
  and is from across the street. Nothing here proves the facade is still charcoal
  in 2026. If it has been repainted, the *value* (dark, low, quiet) matters more
  than the hue — cue 1 must survive the change.
- The Esri frame leans, so the skylight positions along the roof are accurate to
  perhaps ±1.5 m in depth.

## 8. Preserved vs simplified

**Preserved:** the traced footprint including its taper; the two-storey
proportion; roof plane 6.66 m and parapet 7.20 m; the near-black facade value;
one wide four-pane band; the flat unornamented parapet; two roof skylights on a
pale membrane.

**Simplified:** the band is one glass plane behind three mullions in a proud
frame; the shopfront is one plane with two mullions, a door leaf and a vision
panel; the head band and base rail are single crisp bands, not modelled canopies;
skylights are frame + raised pane, ~15% larger than measured so they read at city
distance; the plant cluster is two beveled boxes on a curb with a duct and two
vents; the three party walls are clean planes with a parapet cap and nothing else.

**Not added:** cornice, roof deck, planting, stair bulkhead, crown, signage — the
real building has none of them, and at 7.2 m any of them would be the silhouette.
