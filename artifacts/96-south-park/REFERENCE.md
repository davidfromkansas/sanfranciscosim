# 86–96 South Park — reference dossier

Compiled for `artifacts/96-south-park/`. The plan behind this build is
`docs/asset-plans/96-south-park.md`; this file records what was verified during
the build, and `REPORT.md` records what the build changed.

## What the building is

**86–96 South Park, San Francisco CA 94107.** A 1996 live/work loft building by
**Toby S. Levy, FAIA** — the practice has traded as Levy Design Partners, Levy
Art + Architecture and LDP Architecture — containing **four residential units
and two commercial spaces**, framed entirely in lightweight steel, on the
**corner of South Park and Jack London Alley**. Levy has lived in South Park
since 1985 and owns units in the building; San Francisco Heritage describes it
as "a loft unit building with an ambiguated facade of cubic forms".

The address the user asked for, **96 South Park**, is one unit in the range: the
parcel is signed 86–96, the alley elevation carries the numbers 94 and 96, and
the South Park elevation carries 86 and 88. The DataSF address point for "96
SOUTH PARK" resolves to condominium lot 3775/119 on this parcel.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF EAS `ramy-di5m`, record `423704-643402-467048` | "96 SOUTH PARK" → parcel 3775119, `-122.394155, 37.781911` |
| DataSF Parcels `acdm-wktn`, `blklot=3775119` + the block-3775 set | address range 86–96; six condominium lots (116–121) sharing one polygon; the surveyed 14.439 × 30.056 m lot |
| DataSF Building Footprints `ynuv-fyni`, `mblr = SF3775116` | **two** LiDAR rings — `201006.0022147` (208.7 m², median 11.15 m, majority 9.49 m, max 13.28 m) and `201006.0149656` (81.0 m², median 12.32 m, majority 9.86 m, max 13.73 m); ground 10.5–11.0 m NAVD88 |
| SF Assessor `wv5m-vpq2`, block 3775 lot 119, rolls 2024–25 | built **1996**; "Live/Work Condominium"; unit area 2,262 sq ft |
| architizer.com/projects/86-96-south-park/ | the firm's own text: four residential units, two commercial spaces, **corner site**, lightweight steel frame, non-toxic/renewable/recycled materials, "overlay of geometries reflecting the position of the buildings on the site" |
| sfheritage.org, *The Rise of Modern SOMA* | "In 1996, Levy Art + Architecture created a loft unit building with an ambiguated facade of cubic forms on South Park street where Georgian townhouses had stood before the 1906 earthquake and fire." |
| blockshopper 3775118 / 3775119 | owners of record: Toby S. Levy and Rick A. Holman (family trust) |
| bizprofile.net principal-address 96 South Park | five 645 Ventures limited partnerships registered here; Google Maps also pins OpenMind on this footprint |
| DataSF street centrelines (`streets_datasf.geojson`, the bake's own input) | **the corner condition**: Jack London Alley centreline 13.4 m southwest of the lot centreline, Taber Place 18.1 m northwest, South Park 21.1 m southeast — i.e. streets on three sides and a party wall only on the northeast |
| Google Street View, South Park, **Jan 2025** | the southeast front: painted numbers 86 / 88, the rust-orange perforated gate, the dark glazed brick base, the recessed barrel-soffit archway, the bronze-brown corner volume, the steel-framed upper glazing and projecting bays |
| Google Street View, Jack London Alley, **Jan 2025 and Feb 2021** | the southwest flank: painted numbers 94 / 96, the second orange gate with its stoop, the continuous coloured mosaic tile band, the ribbed metal upper wall, **the vertical-ribbed metal cylinder standing above the roofline** |
| Google Street View photosphere, South Park, **Apr 2017** | the front at distance; a rooftop trellis frame against the sky |
| Google Maps satellite, 2026 Vexcel | the roof: a stepped grey membrane, a light circular form, a bright wedge, and an open darker rectangle at the rear-northeast corner of the lot |
| OSM ways 113545685 and 113545691 | how the bake's Overture gap-fill sees this parcel — as two separate buildings, one untagged and one wrongly addressed "92 Jack London Alley" |

## Verified dimensions and location

- Anchor (model origin, = axis-aligned bbox centre of the modelled footprint):
  **`-122.3941704, 37.7818909`**. The lot's own area centroid is
  `-122.3941704, 37.7819114` and DataSF's independent EAS address point is
  `-122.3941549, 37.7819114` — 1.4 m apart, which cross-checks the projection.
- Lot: **14.439 m** of South Park frontage × **30.056 m** deep, 434.1 m².
- Modelled footprint: the full lot less a **6.42 × 8.73 m** open yard at the
  Taber Place / 84 South Park inside corner → 378 m².
- Headings (measured from the surveyed parcel polygon, confirmed by the build's
  own outward-normal report): front **135.1°** (SE, South Park), party wall
  **45.2°** (NE, 84 South Park), alley **225.2°** (SW, Jack London Alley), rear
  **315.1°** (NW, Taber Place).
- Heights as built: main roof plate **10.00 m**, two upper volumes **12.30 m**,
  gable ridge **13.35 m**, rooftop cylinder cap **13.70 m** (the bbox top).

## What each side shows

**Southeast — South Park front, 14.44 m.** Three volumes. At the alley corner a
**bronze-brown clad volume** stands proud of the wall, with a projecting box bay
and, at ground, a very large storefront window beside a **deep recessed archway
with a curved barrel soffit**. In the middle, **dark glazed blue-grey brick** to
the second floor carrying the painted numbers 86 and 88 and, between them, the
**rust-orange perforated steel gate**. At the northeast end, light ribbed metal
with steel-framed glazing, rising into an upper volume with a **gabled roof**.

**Southwest — Jack London Alley flank, 30.06 m.** The best-photographed
elevation. A dark glazed brick base over a concrete plinth, with a **continuous
band of small coloured mosaic tiles** (blue, teal, green, violet) at about
2.7 m, running the whole length. Sparse tall openings: a garage door at the
Taber Place end, narrow steel-framed windows, a dark doorway, and the **second
orange gate at "94 / 96"** reached by a short stoop. Above the base, ribbed
galvanized metal panel broken by bronze-brown panels and projecting bays. The
**ribbed metal cylinder** stands on this wall, overhanging it, and is the single
most identifiable thing about the building.

**Northeast — party wall with 84 South Park, 21.33 m.** Attached for its whole
length; 84's own LiDAR median is 11.36 m, so the two buildings are within a
metre of each other. Blind.

**Northwest — Taber Place rear, 8.02 m, plus the two yard faces.** No
photography found. Modelled as a service elevation: a roll-up door, a personnel
door and a plain rhythm of openings above. **This elevation is invented.**

**Top.** A stepped grey membrane roof in two planes with the two upper volumes
on diagonally opposite corners, the cylinder on the alley edge, the gable over
the front-northeast, a terrace with a steel trellis between them, and the open
rear-northeast yard that makes the roof read as an L rather than a rectangle.

## Recognition cues (ranked)

1. The **ribbed metal cylinder** on the alley wall — nothing else in the manifest has one
2. The **two rust-orange perforated gates**, one per street elevation
3. The **dark glazed brick base with a coloured mosaic stripe**, wrapping the corner
4. The **collage of stepped volumes in three materials** with no seam aligned
5. The **corner condition**: three exposed elevations on a rim of party-wall row buildings

## Preserved / simplified

**Preserved:** the corner condition and the real 45° heading; three material
zones with hard seams; the dark-base / light-top value split; the cylinder; both
orange gates; the mosaic band; the rear-yard notch; the gable.

**Simplified:** the cylinder is a 16-sided prism and enlarged to 5.5 m diameter;
the gates are widened to 1.8 m and brightened past the real rust colour; the
mosaic band is one flat 0.30 m teal stripe, not tiles; the archway soffit is a
five-segment half-round; the alley window rhythm is regularised to seven bays at
4.30 m; every volume step under 0.6 m is deleted; the perforation pattern, the
fold-out window hoods and the individual tiles are all dropped.

## Uncertainties

- **The cylinder's exact form, size and position.** Unmistakable in the Feb 2021
  alley pano and matched by a light curved shape in the satellite imagery, but no
  photograph establishes whether it is a full drum, a half-drum or a curved wall.
  Built as a full drum overhanging the alley wall — see `REPORT.md` §3.
- **13.70 m is a LiDAR maximum, not a measured crest.**
- **The rear-northeast yard** is inferred from LiDAR coverage, not from a
  photograph.
- **The Taber Place elevation is entirely invented.**
- **No photographs by the architect were obtained.** Architizer and
  ldparchitecture.com both host galleries for this project that did not render to
  text extraction; they remain the highest-value missing source.
- **Firm name in 1996** is unresolved (Architizer says LDP Architecture, SF
  Heritage says Levy Art + Architecture). Nothing in the model depends on it and
  it does not appear in the manifest.
