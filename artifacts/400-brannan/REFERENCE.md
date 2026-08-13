# 400 Brannan Street — reference dossier

Research behind `artifacts/400-brannan/`. Compiled 13 August 2026 from the sources
below; re-verified against the plan `docs/asset-plans/400-brannan.md` before modelling.
Where this file and the plan disagree, **this file and REPORT.md win** (pipeline rule:
REPORT beats plan).

## 1. What the building is

The corner block on the **west corner of Third and Brannan** in SoMa: a two-storey
commercial/industrial building of 1905, 489 m2 on the ground, holding the corner with
two finished street elevations. Assessor use code `IND`, one unit, 22 rooms — a
shopfront-and-loft block, not a factory. Current ground-floor tenants include Avant
Barre (400 Brannan), a gallery/retail unit at 406–410 Brannan, and Cafe Buenos Aires
(590 Third) and Kinoko (592 Third) around the corner.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF EAS Addresses (`ramy-di5m`) | `400 BRANNAN ST` → block 3776 lot 114; 406 and 410 Brannan share the parcel |
| DataSF Parcels (`acdm-wktn`) | **No parcel is numbered 400 Brannan.** Even numbers on Brannan run 376–380 then jump to 414 — the address exists only in EAS |
| SF Assessor secured roll 2025 (`wv5m-vpq2`) | Built 1905; 2 storeys; `IND`; lot 5,318 sq ft; primary address 590 Third Street |
| DataSF Building Footprints (`ynuv-fyni`, `mblr = SF3776114`) | The survey footprint (489.4 m2) and the LiDAR heights: median 7.77 m, mode 7.82, mean 7.69, σ 0.64 over 1,946 cells, max 11.65, min 2.40 |
| OSM way/124903637 (`source=Bing`, `height=8`) | Cross-check footprint, 478 m2 — agrees within 2.3% |
| KartaView seq 7003, frame `574e630a394a5` (2016-05-31), Brannan approaching Third | The Brannan elevation: address plates 410 / 406 / 400, black awnings, white roll-up freight door, upper sash band, gooseneck lamps, wall A/C units, cream body over chocolate bands |
| KartaView seq 1352479 frames 34–36 (2019-03-14), Third at Brannan | The Third Street elevation and the current tonal scheme (light-gray upper wall over a charcoal shopfront level, same Avant Barre awnings) |
| Esri World Imagery z20 nadir (2023 vintage) | Flat dark membrane roof; vent/mechanical scatter grouped toward the block interior; the street-facing third of the deck empty; a large street-tree canopy overhanging the Brannan parapet |

## 3. Verified dimensions and location

- Anchor (footprint AABB centre, which is what the loader's origin convention needs):
  **lon −122.3946805, lat 37.7800981**
- Footprint 489.4 m2; Third Street frontage 23.89 m; Brannan frontage 23.07 m; rear
  20.38 m; northwest party wall stepped, ~23 m overall
- Roof deck 7.77 m (measured); parapet crest ~8.6 m (inferred); model crest 8.8 m at
  the roof bulkhead
- Ground 6.94–7.24 m NAVD88 (the app's terrain handles this, not the asset)

## 4. Orientation

Third Street elevation faces **NE, bearing 45.2°**; Brannan Street elevation faces
**SE, bearing 135.2°**; rear faces SW 224.2°; northwest party wall faces ~315.6°.
Authored in true-world orientation (`+Y` = north), so the axis-aligned bbox is
31.4 × 33.8 m for a 23.9 × 23.1 m building — expected at a 45° heading.

## 5. What each side shows

- **Brannan (SE)** — plain parapet, no cornice; upper floor of wide *landscape*
  steel/aluminium sash, some with through-wall A/C; a horizontal band at the floor
  line; shopfront level with a white roll-up freight door at the southwest end and
  glazed shopfronts under continuous black awnings; two gooseneck lamps.
- **Third (NE)** — the same composition turning the corner, more glass and no freight
  door; the café frontages (590, 592).
- **Southwest rear and northwest party wall** — blank painted masonry with sparse
  openings, invisible from the street but plainly visible from the app's aerial camera.
- **Top** — flat dark membrane inside a continuous parapet; loose vent/mechanical
  scatter grouped toward the block interior; one light-roofed appendage at the north
  corner. The large dark blob over the Brannan edge in nadir imagery is the street
  tree, not a roof feature.

## 6. Recognition cues (ranked)

1. The corner itself — two finished elevations meeting at a sharp 90° on the city's
   diagonal grid, only two storeys where the neighbours are three
2. Light upper wall over a dark base
3. The continuous black awning line carried around both frontages
4. Wide **landscape** industrial sash upstairs
5. The white roll-up freight door at the southwest end of Brannan

## 7. Preserve / simplify

**Preserve:** the single-volume box and its real 45° heading; the northwest notch; the
two-tone split; the awning line turning the corner; the landscape window proportion.

**Simplify:** upper sash → 6 identical bays per frontage; shopfronts → four/five
recessed glazed bays divided by piers; A/C units, gooseneck lamps, signage, address
plates → dropped; roof scatter → a plant plinth with three units, a duct, a hatch, one
skylight and the bulkhead.

## 8. Uncertainties and conflicting evidence

- **The address has no parcel.** Resolution runs address → EAS → parcel 3776114 →
  footprint. A geocoder returns either a POI node (Nominatim: "Buhler Commercial
  Construction") or nothing. Same class of trap as 350 Brannan.
- **LiDAR `hgt_max` 11.65 m is not the crest.** It is +6σ over a roof with σ 0.64 m
  and a minimum of 2.40 m; the nadir imagery shows a street tree breaking over the
  Brannan parapet. The crest used is the inferred 8.6 m parapet, with the model top at
  8.8 m on a modest bulkhead. Recorded as a deliberate rejection, not an oversight.
- **The paint scheme changed between 2016 and 2019** (cream + chocolate → light-gray
  over charcoal). The model uses the common denominator: warm light body, near-black
  base. See REPORT.md §Decisions.
- The 6-bay rhythm per frontage is *inferred* from oblique photography.
- Whether the northwest party wall has a gap to 574 Third is unresolved; the survey
  rings touch, so both walls are modelled finished.
- No architect is recorded for the 1905 building in any source consulted.
