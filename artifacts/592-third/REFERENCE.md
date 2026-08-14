# 592 Third Street — reference dossier

Compiled 13 August 2026 for `artifacts/592-third/`. The plan
(`docs/asset-plans/592-third.md`) was the starting point; everything below was
verified against primary sources before modelling, and the places where this
dossier **overrides** the plan are marked ⚠ and repeated in `REPORT.md`.

The building is a 1905 two-storey wood-frame industrial loft holding the **west
corner of 3rd and Brannan** in South Beach / Central SoMa, filling its lot. A
pale stucco upper storey over a continuous near-black shopfront band that turns
the corner unbroken; six ground-floor tenants across two street frontages; a
flat parapeted roof scattered with skylights. It is the lowest thing on its
block.

---

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Building Footprints `ynuv-fyni`, record **`SF3776114`** | The authoritative footprint polygon (1,946 half-metre cells, 489.4 m²); ground 6.94–7.46 m NAVD88; height median 7.77 m, **mode 7.82 m**, mean 7.69 m, std 0.64 m, min 2.40 m, max 11.65 m |
| DataSF Parcels `acdm-wktn`, **`blklot 3776114`** | One lot, address of record **590 3rd St**, zoning CMUO (Central SoMa Mixed Use Office), parcel centroid −122.3946749 / 37.7800838 |
| SF Assessor secured roll `wv5m-vpq2`, 2025 | Built **1905**, **2 storeys**, use class Industrial, construction type D, lot area 5,318 sq ft (494 m²) |
| SF Building Permits `i98e-djp9`, block 3776 lot 114 | Six records 2003–2018, all `number_of_existing_stories = 2`, `existing_construction_type_description = "wood frame (5)"`: 2011 corner stucco repair, 2014 ballet-studio fit-out at 410 Brannan, 2015 toilet remodel at 590 3rd |
| [OSM way/124903637](https://www.openstreetmap.org/way/124903637) | `building=yes`, `height=8`, `source=Bing` — a 478 m² trace, used only as a cross-check (⚠2) |
| OSM POI nodes 10270473366 / 12983432802 / 317124808 / 13765490847 / 10869882845 / 10869882844 | Kinoko Real Estate (592), Cafe Buenos Aires (590), disused dry cleaner (588) on the 3rd Street frontage; Buhler Commercial Construction (400), Divine Yoga Studio (406), J Body Works (410) on Brannan. All `check_date=2026-04-26`. **Their positions are what establish which tenant is on which frontage** |
| Google Street View, capture **May 2025**, from 3rd Street opposite the frontage (heading ~255°) and from Brannan Street opposite (heading ~320°), plus the intersection pano from the east corner | Both street elevations in detail: the black shopfront band, the awnings, the bay divisions, the upper-window rhythm, the condenser row, the roll-up door, and the fact that the parapet does **not** step up at the corner |
| Google satellite (Vexcel/Airbus, 2026) at z20–21 and Esri World Imagery at z20, both reprojected and overlaid with the DataSF ring | The roof: flat membrane, ~8–12 small square skylights and hatch boxes in a loose scatter, a continuous parapet, **no penthouse and no rooftop plant** — and the two street-tree canopies overhanging the 3rd Street parapet (⚠1) |
| `app/public/tiles/buildings/23_13.bin` (this repo's committed bake) | What the procedural city puts here today: a 489 m² ring, base 6.5 m, top 16.7 m — **10.2 m tall**, 2 m taller than the asset. Also the exclusion measurement in `REPORT.md` |
| https://kinokorealestate.com/ | 592 3rd St is the firm's home office; South Beach |

Nothing here is behind a paywall or a login; no copyrighted imagery is committed
to the repo.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.3946805, 37.7800910` | measured — AABB centre of the de-spiked DataSF polygon |
| Footprint | 21.67 m (3rd St) × 23.07 m (Brannan) × 20.38 m (SW) × 23.44 m (NW), 488.7 m² | measured (⚠3) |
| Published DataSF ring area | 489.4 m² | agrees to 0.15 % |
| Assessor lot area | 494 m² | agrees to 1 % — the building covers its lot |
| Storeys | 2 | Assessor + all six permits |
| Construction | Type V wood frame | permits 2011–2015 |
| Roof deck | **7.82 m** above ground | LiDAR mode over 1,946 cells; median 7.77, std 0.64 |
| Parapet crest | **8.20 m** | *estimated* — deck + 0.38 m of parapet upstand (⚠1) |
| Ground | 7.25 m NAVD88 mean, 0.52 m range — flat | measured; the app's terrain handles this |
| 3rd Street front | outward normal **45.1°** (NE) | measured |
| Brannan front | outward normal **135.2°** (SE) | measured |
| SW party wall | 224.2° · NW party wall 312.0° | measured |
| Nearest neighbours (LiDAR mode) | NW party wall `SF3776008` 11.03 m · Brannan face SW `SF3776011` 9.77 / 13.76 / 11.13 m · 599 Third across 3rd `SF3775140` 15.70 m deck, 18.34 m crest · across Brannan `SF3787001/2` 8.49 / 4.96 m | measured |

Footprint in the app's tangent projection, recentred on the anchor
(x east, y north, metres, **counter-clockwise**):

```
n (  0.195,  15.815)   north corner — 3rd St / NW party wall
w (-15.485,  -1.605)   west corner  — the two party walls meet
s ( -0.875, -15.815)   south corner — Brannan / SW party wall
e ( 15.485,   0.455)   east corner  — 3rd St / Brannan, the hero corner
```

| Edge | Length | Outward normal | What it is |
|---|---|---|---|
| n→w | 23.44 m | 312.0° (NW) | party wall, the 11 m neighbour on 3rd |
| w→s | 20.38 m | 224.2° (SW) | party wall, the 414 Brannan block face |
| s→e | 23.07 m | 135.2° (SE) | **Brannan Street front** — 400 / 406 / 410 |
| e→n | 21.67 m | 45.1° (NE) | **3rd Street front** — 592 / 590 / 588 |

## 3. Overrides of the plan

**⚠1 — the crest, and why `hgt_max` is not it.** DataSF publishes
`hgt_maxcm = 1165` for this footprint. That is 3.83 m above the roof-deck mode
on a surface whose height standard deviation is 0.64 m: a six-sigma outlier. The
2026 satellite imagery and the May 2025 Street View capture both show two mature
street trees standing at the 3rd Street kerb with their canopies over the
parapet, and the same footprint's `hgt_min = 2.40` m is the matching artifact at
the low end. There is no penthouse, no bulkhead and no plant anywhere on this
roof in any imagery consulted. The plan's 8.20 m — deck plus a 0.38 m parapet —
stands, and it remains the weakest number in this dossier (±0.3 m, 4 %). This is
the 250 Van Ness failure mode; the plans README now records it.

**⚠2 — build on DataSF, not OSM.** OSM way/124903637 is a `source=Bing` trace of
478 m² whose 3rd Street edge is displaced several metres north of the surveyed
line. DataSF and the assessor's lot agree with each other against it.

**⚠3 — the published DataSF ring has a zero-width spike, and it shortens the
3rd Street frontage by 2.23 m.** This is the dossier's one genuinely new finding
and it overrides the plan's first draft. `SF3776114` is published with 13
vertices. Its last vertex before closing, `(-122.3946783, 37.7802340)`, lies on
the 3rd Street frontage line to within **9 mm**, 2.23 m short of the ring's first
vertex — so the first vertex is a degenerate spike projecting past the real
corner, not a corner. Taking the ring literally gives a 3rd Street frontage of
23.90 m and puts the AABB centre 0.79 m out of place. The real frontage is
**21.67 m** and the anchor moves to `37.7800910`. Everything built here uses the
de-spiked quadrilateral above. The seven remaining intermediate vertices along
the NW party wall deviate from the straight n→w chord by at most **0.55 m** —
under the 0.6 m tolerance the tile bake simplifies at — and are dropped as
raster-edge noise on a wall nobody can see.

## 4. What each side shows

**North-east (3rd Street, 21.67 m)** — Two horizontal bands. Below: a continuous
near-black shopfront with flat black awnings carrying white tenant lettering,
large plate-glass bays over low dark bulkheads, and a dark recessed entry with a
glass door between the Kinoko bays and the café. Kinoko (592) takes the bays
nearest the Brannan corner, Cafe Buenos Aires (590) the middle, the shuttered dry
cleaner (588) the north-west end. Above: plain pale warm-grey stucco with
white-framed punched rectangular windows in a loose rhythm — a group toward the
corner, another toward the north-west end — closed by a flat parapet with no
cornice and no ornament. Two street trees stand in front and occlude the wall in
every available photograph.

**South-east (Brannan Street, 23.07 m)** — The same two-band composition, turning
the corner without a break. Awnings for Divine Yoga Studio (406) and its
neighbours, small painted numerals on the awning valances, and a **dark roll-up
garage door** at the south-west end. Above, the same stucco with a longer, more
regular run of punched windows, and — the detail that dates the building's
conversion — a row of small **wall-mounted condenser boxes on brackets** just
below the sill line. This is the utilitarian face.

**South-west and north-west (party walls)** — Built hard against neighbours 1 to
5 m taller; invisible from the street and unsourced except from above. Modelled
as blank stucco. Inventing openings on a party wall would be a straightforward
lie.

**Top** — The largest surface the app's camera sees. A flat mid-grey membrane
deck inside a continuous parapet, with roughly a dozen small square roof
objects — pale-curbed skylights with light glazing, a couple of plain hatch
boxes, a few vent stacks — in no particular grid. A 1905 industrial floor was
daylit from above and then patched piecemeal for a century. No penthouse, no
HVAC plant, no billboard: the billboard visible in photographs of this corner
stands on the brown-brick neighbour further north-west along 3rd.

## 5. Recognition cues (ranked)

1. The **wrapped near-black shopfront band** under a pale stucco upper storey,
   turning a sharp 90° corner — at city scale this is the entire recognition
2. The **corner** itself: two nearly equal designed elevations with the same
   composition on both
3. **Being the low one** — 8.2 m against 18.3 m across the street and 11 m next
   door
4. The skylight-scattered flat roof
5. The condenser row and the roll-up garage door on Brannan

## 6. Preserved / simplified

**Preserved** — the de-spiked footprint and its 45° heading exactly; the
two-band composition turning the corner unbroken; the near-black / pale value
contrast; the 8.20 m crest, lower than every neighbour.

**Simplified** — per-bay awnings become one continuous fascia per street face;
tenant lettering, awning numerals and window decals are dropped (the contract
forbids textures, and glyph geometry at this scale is noise); the upper windows
collapse to loose groups rather than the exact real count; the condenser row
becomes four slightly enlarged boxes; the roll-up door becomes one recessed
grey panel; the skylight scatter is reduced to eight, curbs thickened; street
trees, bike racks, signals, sidewalk and wall meters all go.

## 7. Uncertainties

- **The crest** (⚠1) — derived, not published. ±0.3 m.
- **The party walls** — no street-level coverage of either; blank stucco is an
  inference from typology, not an observation.
- **Upper-window counts and positions** — inferred from two Street View captures
  partly occluded by street trees. The *rhythm* (loose groups, not a strict
  grid) is the load-bearing claim; the exact count is not.
- **Bay divisions on the ground floor** — the awning count is legible in Street
  View but the exact bay widths are estimated against the measured frontage.
- **No architect and no original-permit record** were found for the 1905
  building; the DBI record for this lot starts in 2003.
- **The address is ambiguous.** The lot's address of record is 590 3rd Street;
  592 is the Kinoko tenant node inside the same building, and 588, 400, 406, 410
  and 414 are five more tenant addresses on the same lot. There is exactly one
  building here.
