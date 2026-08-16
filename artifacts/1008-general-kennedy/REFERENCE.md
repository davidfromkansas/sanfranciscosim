# 1008 General Kennedy Avenue — reference dossier

Compiled 12 August 2026, before and during the build. This file records what was
verified independently of `docs/asset-plans/1008-general-kennedy.md`, what the plan got
wrong, and what remains inference.

## What the building is

A hospital ward in the Letterman complex, Presidio of San Francisco. Built in the 1930s as
one of the concrete Mission Revival wards that replaced the original 1899–1902 wood-frame
Greek Revival wards; this one replaced Ward "G". Since the 1994–96 rehabilitation it has
been part of the **Thoreau Center for Sustainability**, a non-profit office campus. It is
the middle of three parallel ward wings — 1007 (north), **1008**, 1009 (south) — that
share one Thoreau Center entrance and a connecting corridor along their west ends. It is a
contributing building in the Letterman Hospital Complex, within the Presidio National
Historic Landmark District.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| Overture Maps `addresses`, release 2026-07-22 | The authoritative point for 1008 at `-122.4515229, 37.800814`, distinct from 1007 (`-122.451433, 37.8009646`) and 1009 (`-122.4516246, 37.8006882`). **This is the only source consulted that resolves 1008 at all.** |
| Overture Maps `buildings`, release 2026-07-22 | Height 10.9 m on the parent polygon (complex-wide, not per-ward) |
| DataSF Building Footprints (LiDAR), `ynuv-fyni`, building `201006.0000207` | 101-vertex footprint of the whole complex, 5,845 m²; ground 8.69 m NAVD88; height median 8.88 m, max 15.79 m |
| OSM way `288374440` | Independent 49-vertex outline of the same complex |
| NPS, *Letterman Hospital Complex* pages and the GOGA *Letterman Hospital* brochure | The complex history; the 1930s programme that replaced wood-frame wards with concrete Mission Revival buildings |
| militarymuseum.org, *Letterman Army Medical Center* | The only source naming Building 1008 and its predecessor, Ward "G" |
| LMS Architects (Tanner Leddy Maytum Stacy), Thoreau Center project page | Rehabilitation architect; 75,000 sq ft Phase 1 + 37,000 sq ft Phase 2A; Secretary of the Interior's Standards |
| Wikipedia, *Thoreau Center for Sustainability* | Proposed to the Presidio Trust 1994, opened 1996 |
| Google Street View panos labelled "1008 General Kennedy Ave" and "1002 General Kennedy Ave", capture May 2025 | The east head elevation: smooth white stucco, exterior steel stair to an upper landing, punched double-hung windows with projecting sills, red barrel-tile hip, terracotta chimney |
| Google Street View, Edie Road parking lot, capture Apr 2022 | The row's west ends and the connecting corridor — and the wood-sided neighbouring ward that must *not* be modelled |
| Esri World Imagery, z19–z20 | Roof form: one continuous ridge the full length, hips at both ends, a splayed cross-hip over the wider east head, chimneys along the ridge, a flat-roofed connector at the west |

## Verified dimensions and location

The footprint was cut by hand out of the DataSF LiDAR polygon and cross-checked against
the OSM outline, working in a frame aligned to the ward's own axis:

| Quantity | Value | Confidence |
|---|---|---|
| Ward envelope | 55.14 m long × 12.02 m across | **measured**, two independent sources |
| Ward bar width | 9.38 m | **measured**; LiDAR and OSM agree to 0.03 m |
| East head block | 12.02 × 10.28 m | **measured**; the two agree to 0.02 m |
| Footprint area | ~570 m² | derived |
| Long axis heading | 116.85° (east head) / 296.85° | **measured** from the polygon |
| Long elevations face | 26.85° (NE) and 206.85° (SW) | **measured** |
| Ridge height | 10.9 m | Overture, complex-wide — see risks |
| Eave height | 7.8 m | *inferred*: 1.0 m raised base + two 3.4 m storeys |
| Head cross-hip ridge | 11.17 m | derived: the bar's pitch carried over the wider head span |
| Chimney crest | 11.9 m | *inferred*: ridge + 1.0 m stack |
| Footprint OBB centre | `-122.4514885, 37.8007968` | derived |
| **Manifest anchor** | `-122.4514809, 37.8007878` | OBB centre + (0.668 m E, −0.999 m N), see REPORT.md |

## Observations by elevation

**East head, facing General Kennedy Avenue.** Smooth white stucco. Two storeys over a
raised base. An exterior steel stair climbs across the elevation to a small landing at the
upper floor; a recessed doorway with a glazed panel sits beneath it. Punched double-hung
windows with white projecting sills, placed asymmetrically rather than on a grid. A
terracotta chimney stands against the sky at the roof's shoulder.

**Northeast and southwest flanks.** Two storeys of punched windows in a steady rhythm the
full length. White stucco, no string course, no ornament. Deep tile eaves shade the upper
row. The head block's own flanks continue the rhythm at a wider wall line.

**West end.** A low, flat-roofed open connector joining the ward to the corridor that runs
along the row's west side.

**Top.** One unbroken barrel-tile hipped roof: a single ridge running the full 55 m,
hipped at both ends, splaying into a wider cross-hip over the head block. Chimneys through
the ridge. No mechanical plant, no skylights — the roof's character is that it is empty.

## Recognition cues, ranked

1. Extreme slenderness — 55 m long, 9.4 m wide
2. The unbroken red tile hipped roof with a single continuous ridge and deep eaves
3. Terracotta chimneys through the ridge — the only vertical incident
4. White stucco with a steady two-storey punched-window rhythm
5. The wider hipped head block at the east end with its exterior stair

## Corrections to the plan, made during the build

1. **The head block does not have its own separate roof at its own eave height.** The plan
   put the head's eave 0.8 m above the bar's and gave it an independent hip. Aerial imagery
   shows the opposite: bar and head share an eave line, the ridge runs unbroken from end to
   end, and the head's extra width produces a *higher, splayed cross-hip* at the same
   pitch. Rebuilt that way. This was the single largest visual error in the plan.
2. **Chimney count raised from 4 to 6** (5 on the bar ridge + 1 on the head). Counted off
   Esri z20 imagery of this ward. Section reduced from 0.9 m to 0.75 m to match.
3. **The head block's flanks were left blank by the plan's massing recipe**, which put
   windows only on the bar. The real building has windows there; four were added per flank.
4. **The exterior stair was specified as `Toy_ink`.** At the app's camera that read as a
   black smear across the head elevation. Changed to `Toy_steel`, which is also closer to
   the real galvanised stair.
5. **Night state moved off a single elevation.** The plan put the lit windows on one long
   flank; from half the app's orbit the building then has no night state at all. Nine lit
   windows now sit on both flanks, weighted to the southwest.
6. **The model origin is not the footprint OBB centre.** See REPORT.md — the building is
   asymmetric about its own footprint centre, so the origin was moved to the XY bbox centre
   and the anchor moved by the same vector.

## Uncertainties

- No source isolates this ward's footprint; the cut is a judgement call at the west end,
  where the ward merges into the block shared with 1007 and 1009.
- The 10.9 m ridge is a complex-wide Overture figure, not a measurement of this building.
- The chimney positions are read off aerial imagery at the limit of its resolution.
- The 11-bay window rhythm is inferred from oblique photography.
- The build year is a decade (1930s); no exact year and no architect were found.
