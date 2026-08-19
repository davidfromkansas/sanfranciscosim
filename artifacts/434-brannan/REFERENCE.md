# 434 Brannan Street — reference dossier

Research behind `434-brannan.glb`. Compiled 18 August 2026. Everything here was
re-verified for this build; where it contradicts `docs/asset-plans/434-brannan.md`
this file wins, and `REPORT.md` records the correction.

## 1. Identification

| Item | Value | Confidence |
|---|---|---|
| Address | 434 Brannan St, San Francisco, CA 94107 | measured |
| Parcel | block 3776, lot 151 (`3776151`) — address range 434–434, one EAS record | measured |
| DataSF footprint | `mblr = SF3776151`, `sf16_bldgid 201006.0003989` | measured |
| OSM | way/124889482, `building=yes`, `height=11`, `name=Olivia Travel` | measured |
| Built | 1929 | SF Assessor roll (2008–2024, all ten years); SF Planning DPR 523A |
| Style | Art Deco, reinforced concrete industrial building (`HP8`) | DPR 523A |
| Architect | not recorded in any source consulted | — |
| Storeys | 3 | Assessor roll; DPR; photography on both streets |
| Use | Commercial Office (`COMO`); 25,000 sq ft over 3 floors | Assessor roll |
| Lot | 75 ft x 174 ft = 22.86 x 53.04 m (1,230.1 m2 surveyed) | DPR 523A; DataSF parcels |
| Corner | northeast corner of Brannan and Zoe | DPR 523A; verified from the street centrelines |

The single most valuable source is the **SF Planning DPR 523A/523L form**
(`https://sfplanninggis.org/docs/DPRForms/3776151.pdf`), recorded by Page &
Turnbull in June 2009 for the Eastern Neighborhoods SoMa Survey. It is the only
architectural description of this building anywhere, and it establishes, in its
own words: a 3-story reinforced-concrete Art Deco building clad in molded
concrete under a flat built-up roof; a primary facade of five bays divided by
molded concrete pilasters; a fully glazed main entry with sidelights; aluminium
industrial awning sash; a facade terminating in a sculpted geometric frieze; a
secondary concrete facade on Zoe Street with pivot sash; and a **rear facade clad
in corrugated metal** facing a parking lot.

## 2. Geometry

Footprint measured from the DataSF LiDAR-derived building-footprint layer
(`ynuv-fyni`), reprojected with the app's tangent projection (LON0 −122.4375,
LAT0 37.77) and reduced to its four real corners. The survey ring's ten vertices
collapse to four once sub-0.3 m duplicates are dropped; the four-corner
parallelogram encloses **763.6 m2** against the survey's 764.8 (−0.2%).

Anchor = axis-aligned bounding-box centre = **−122.3954103, 37.7796003**.

| Local (X east, Y north) | corner |
|---|---|
| (−19.816, 4.182) | W — rear x Zoe |
| (3.812, −20.052) | S — Brannan x Zoe |
| (19.816, −3.952) | E — Brannan x the 426 Brannan party wall |
| (−3.837, 20.052) | N — rear x the 426 Brannan party wall |

| Edge | Length | Outward bearing | Elevation |
|---|---|---|---|
| W→S | 33.85 m | 224.8° SW | Zoe Street flank |
| S→E | 22.70 m | 134.8° SE | **Brannan Street primary facade** |
| E→N | 33.70 m | 44.8° NE | party flank (426 Brannan) |
| N→W | 22.52 m | 314.8° NW | rear, over the parking lot |

Cross-checks. The OSM ring (which is also Overture's) measures 788.0 m2, +3.2%,
extending ~4 m further northwest. The Assessor's 25,000 sq ft over three storeys
is 774 m2 per floor — within 1.3% of the LiDAR footprint, i.e. **full-footprint
coverage on every floor**, which is what licenses a single-volume massing. The
DPR's 75 ft x 174 ft lot matches the DataSF parcel (22.86 x 53.04 m nominal,
23.0 x 53.1 m measured).

**The lot is 53.1 m deep and the building is 33.85 m.** The rear 17.8 m is a
fenced surface car park ("Ball Park Parking"). The rear elevation is therefore a
real, visible facade, not a party wall, and the asset must not be extended to
fill the lot.

Side determination was measured, not assumed: DataSF street centreline CNN
3078000 (Brannan, this block) carries `rt_fadd 422 / rt_toadd 438`, putting the
even numbers on the northwest side of the roadway, and the footprint's frontage
sits 13.5 m from that centreline. Zoe Street (CNN 13795000) meets Brannan at the
southwest end of the frontage; the flank stands 5.6 m off the Zoe centreline.

## 3. Heights

| Feature | Value | Basis |
|---|---|---|
| Roof deck | **11.46 m** | DataSF LiDAR `hgt_median_m`; mode 11.43, mean 11.36, sd 0.92 over 3,086 cells — **measured** |
| LiDAR maximum | **13.79 m** | `hgt_maxcm`, +2.5σ — accepted as the rooftop mechanical penthouse |
| Parapet crest | ~12.40 m | *inferred*, deck + 0.94 |
| Pilaster caps | ~13.05 m | *inferred*, and deliberately exaggerated — see REPORT |
| Ground | 5.46–6.24 m NAVD88 (median 5.85) | LiDAR `gnd_*`; the app's terrain handles the 0.78 m fall |

Three things support accepting 13.79 m rather than rejecting it the way 400
Brannan's 11.65 m and 592 Third's 11.65 m were rejected. First, the outlier is
+2.5σ, not +6σ. Second, `peak_1st_m` (19.68 m) equals `hgt_max` plus ground, so
no canopy overhangs this roof — and indeed the Brannan street trees on this block
are all on the odd side. Third, nadir imagery at z21 shows exactly one raised
rooftop structure, a kerbed platform carrying a large dark air-handling unit,
about 6.6 m in from the northeast parapet and two thirds of the way back, with
its own shadow.

**What could not be settled: the parapet.** Two photogrammetric solves against
Google Street View pano `o-uPNk1QbRTZseDkFhl8bw` disagree. The equirect
elevation-angle solve (elevation = (H/2 − y)/H × 180°, camera 2.5 m) puts the
sky/parapet transition at 28.44° and the wall base at −9.42°, which yields a wall
crest of ~10.6 m — **below the measured roof deck**, therefore wrong. The
rectilinear solve (facade width at two known rows, thumbfov 90 → f 512 px, pitch
−18°) yields 12.1 m from one row and 14.5 m from another, a 20% spread. The
pano's metadata reports a 0.94° tilt, which alone moves the answer ~0.4 m at this
range, so the horizon calibration is the prime suspect but probably not the whole
story. The parapet numbers used here are architectural inference, and the plan's
2.15 says so. **The mis-attribution is cheap**: the body is normalised to the
measured deck and `targetHeightM` is by definition the export's own top, so a
wrong guess costs a slightly tall penthouse, never a mis-scaled building.

## 4. What each side shows

**Southeast — Brannan Street (primary).** Six flat fluted concrete pilasters
divide five bays; each pilaster steps up through the parapet into a plain
projecting cap, so the roofline is serrated. Each bay head carries a stylised
Art Deco fan/chevron ornament in dusty salmon on the pale concrete ground — the
building's only colour. Floors 2 and 3 carry a wide multi-pane industrial steel
sash per bay (roughly 8 panes wide by 4 high, light frames, dark glazing), some
with through-wall air-conditioners. The ground floor is 1999–2000 work: shorter
window bands behind light metal grilles in bays 1–4, and in the northeast-most
bay a tall recessed main entry with a dark reveal, a glazed leaf with sidelights,
and a large shallow circular graphic on the reveal wall. Dimensional letters
reading "olivia" in dusty pink sit on the spandrel between floors 1 and 2 of the
centre bay. A light plinth runs along the pavement.

**Southwest — Zoe Street (secondary).** Plain concrete with a regular grid of
wide industrial sash on all three floors, about six bays, separated by narrow
flat piers; no pilasters, no frieze. A painted mid-grey dado runs along the base
for most of its length; ground-floor windows are larger and fitted with blinds.
**At the rear ~8 m of this flank the concrete stops and terracotta-orange
corrugated metal begins**, blank and full height over a low orange stucco base.

**Northwest — rear.** Blue-grey vertically ribbed metal siding, full height, with
punched aluminium awning windows in a loose two-by-three arrangement, some with
air-conditioners. It faces the chain-link-fenced car park that fills the rear
17.8 m of the parcel, so it is fully visible from the app's aerial camera.

**Northeast — party flank.** Plain, unfenestrated. 426 Brannan (parcel 3776015,
LiDAR deck 5.75 m — the red-brick "Brick House" with a timber restaurant patio)
abuts the 21.9 m nearest Brannan and is only 7.5 m deep, so 434 stands 5.7 m
proud of it there and the rear 11.8 m of the flank is fully open to the car park.
Modelled as a finished, quiet plane with floor-line score marks and no invented
window grid.

**Top.** Flat pale membrane inside a continuous parapet, the six caps reading as
teeth. Rear-centre-northeast: the mechanical penthouse. A duct run heads
southeast from it, parallel to and ~4.5 m inside the northeast parapet. Near the
Brannan end: a skylight, a roof hatch and three small units. A thin guy wire runs
southwest from the penthouse to a small ballast pad (the wire is not modellable
at this scale; the pad is).

## 5. Recognition cues, ranked

1. The **toothed crown** — six fluted pilasters stepping up through the parapet
   into plain caps. The silhouette from the app's downward camera, and nothing
   else on this block face has one.
2. The **salmon Deco frieze** in the five bay heads — the one saturated accent.
3. Three floors of **wide two-light industrial sash** in a strict five-bay rhythm.
4. **Concrete front, corrugated-metal back** — the honest warehouse behind the
   dressed face, standing over its own car park.
5. The corner condition: a short dressed front on Brannan and a long plain flank
   running away down Zoe.

## 6. Preserve / simplify

Preserve: the single-volume parallelogram at the real 45° heading; the fact that
it fills only the front two thirds of its lot; the six pilasters, their caps and
the toothed parapet; the five-bay rhythm and the frieze; the concrete/corrugated
split in both its places; the recessed entry at the northeast end.

Simplify or exaggerate: the caps are thickened and given more projection than
life and the frieze ornament is enlarged (the one spent exaggeration); fluting
becomes three shallow ribs; sash becomes one recessed dark panel per opening with
a light frame and a single horizontal division; the fan becomes a three-step
symmetric pyramid; corrugation becomes four or five proud strips per panel, never
rib by rib; the "olivia" lettering, air-conditioners, grilles, downpipes, wires
and graffiti are all dropped; the roof's loose scatter becomes one penthouse and
its unit, one duct run with a riser, one skylight, one hatch, three small boxes
and the ballast pad.

## 7. Sources

- `https://sfplanninggis.org/docs/DPRForms/3776151.pdf` — SF Planning DPR 523A/523L, Page & Turnbull, 5 June 2009. The architectural description above.
- `https://data.sfgov.org/resource/ramy-di5m` — EAS addresses; 434 → parcel 3776151, single record.
- `https://data.sfgov.org/resource/acdm-wktn` — parcels; the 53.1 x 23.0 m lot, address range 434–434.
- `https://data.sfgov.org/resource/ynuv-fyni` — DataSF building footprints; `SF3776151` geometry and the 11.46 / 13.79 m heights.
- `https://data.sfgov.org/resource/wv5m-vpq2` — Assessor secured roll; 1929, 3 storeys, `COMO`, 25,000 sq ft.
- `https://data.sfgov.org/resource/3psu-pn9h` — street centrelines; CNN 3078000 (Brannan) and 13795000 (Zoe).
- `https://www.openstreetmap.org/way/124889482` — cross-check ring, `height=11`.
- Google Street View panoramas `o-uPNk1QbRTZseDkFhl8bw` (Brannan, straight on), `EuNjmfDq-A_70aQ6Y0yBqQ` and `7KpMzggTKz4tObTSkg4EYg` (Zoe Street, the flank and the corrugated rear).
- Google satellite imagery z21, stitched and overlaid with the DataSF footprint and parcel rings — the roof layout, the caps as teeth, the penthouse position (measured against the ring at ~6.6 m in from the northeast edge).
- Permit history via checkpermits.com: a ~$350,000 job for window replacement, a new main entry and storefront, and the removal of two curb cuts; a $750,000 tenant improvement completed September 2000. Leasing material describes a 1999 upgrade for ADA, seismic and life safety. This is why the ground floor does not read as 1929 work.

No copyrighted imagery is committed to this repo; the URLs above are the record.
