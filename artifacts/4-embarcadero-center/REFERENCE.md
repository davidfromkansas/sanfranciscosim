# Four Embarcadero Center — reference dossier

55 Clay Street, San Francisco, CA 94111. Compiled 19 August 2026 for the SF-SIM
miniature GLB. This dossier records what was verified independently of
`docs/asset-plans/4-embarcadero-center.md`; where the two disagree, this file and
`REPORT.md` win.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/616812910](https://www.openstreetmap.org/way/616812910) | The 24-node footprint polygon (the primary geometric input), `height=174`, `building:levels=45`, `alt_name=Four Embarcadero Center`, `wikidata=Q3056626` |
| [Wikidata Q3056626](https://www.wikidata.org/wiki/Q3056626) | 45 floors, inception 1982, architect Q764692 (John Portman), coordinate 37.7953 / −122.396197 |
| [CTBUH / skyscrapercenter #2589](https://www.skyscrapercenter.com/building/four-embarcadero-center/2589) | **173.7 m architectural height**, 45 floors, all-steel structure, 55 Clay Street, LEED Gold, 13th tallest in SF. Also the primary photo set (Terri Meyer Boake, Nathaniel Lindsey) |
| [Wikipedia — Four Embarcadero Center](https://en.wikipedia.org/wiki/Four_Embarcadero_Center) | 173.74 m roof, 45 storeys, 1982, Boston Properties ownership |
| [Structurae](https://structurae.net/en/structures/four-embarcadero-center) | 174 m, 45 floors, 1982 |
| [SFYIMBY, Sept 2021](https://sfyimby.com/2021/09/number-18-four-embarcadero-center-financial-district-san-francisco.html) | Five Andrew Campbell Nelson photographs. **"rising above Sue Bierman Park" is the near-orthographic NORTH elevation**; "from the western side of the Ferry Building" is the clearest EAST-end crown. 1.1 M sq ft total / 858,600 sq ft office |
| [SPUR, "Rockefeller Center West"](https://www.spur.org/publications/urbanist-article/2014-07-17/urban-field-notes-rockefeller-center-west) | John King's silhouette description; the irregular plan giving 10–14 corner offices per floor |
| [DataSF LiDAR `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json) | `sf16_bldgid` 201006.0000633: `hgt_maxcm` 17905, `hgt_mediancm` 15099, `hgt_stdcm` 6260, 12,569 cells, `peak_1st_m` 182.69 |
| Google satellite tiles z19/z20 | The roof plan: pale deck, **four large circular cooling towers in a row**, mechanical curbs, penthouse box, window-washing davit track |

No reference imagery is committed here; the URLs above are the record.

## 2. Verified dimensions, location, orientation

Measured from the OSM polygon in the project's local tangent projection
(`x=(lon+122.4375)·111320·cos 37.77`, `z=−(lat−37.77)·110540`):

| Item | Value |
|---|---|
| Minimum-area OBB | **63.46 m × 37.34 m** |
| Long-axis bearing | **81.09°** true (perpendicular 171.09°) |
| Polygon area / OBB area | 2,169.7 m² / 2,369.9 m² |
| OBB centre (the anchor) | **−122.3961998, 37.7953001** |
| Shoelace centroid | −122.3962051, 37.7952974 — **6 cm** from the OBB centre |
| Architectural top (parapet) | **173.70 m** |
| Rooftop-plant crest | **179.05 m** (LiDAR max) → shipped as 179.00 |
| Floors / floor-to-floor | 45 / 3.86 m derived |

Because the OBB centre and the polygon centroid agree to 6 cm, there is no
service-wing centroid skew here and the anchor needs no adjustment.

**Street sides**, measured against OSM centrelines rather than taken from the
address, expressed as the nearest approach in the OBB frame:

| Street | Nearest | Side |
|---|---|---|
| Clay Street | 32.1 m | **north** |
| Drumm Street | 41.4 m | **west** |
| Sacramento Street | 82.9 m | south |

So the long faces look north and south, the short ends east and west, and the
55 Clay Street entrance is on the **north** face — the model is authored with
its front on +Y, which is the opposite of the kit's −Y convention and correct
for a true-world-oriented landmark.

## 3. The footprint, strip by strip

The single most useful measurement. In the OBB frame (`u` along the long axis,
+u east; `v` across it, **+v south**), the plan is a rectangle whose two short
ends are staircase chevrons peaking just north of centre:

**East end** — six north→south strips and how far east each reaches:

| Strip (v range, m) | Width | Reaches u = |
|---|---|---|
| −18.65 … −13.29 (north corner) | 5.36 | +26.84 |
| −13.29 … −6.30 | 6.99 | +28.65 |
| −6.30 … −1.00 | 5.30 | +29.28 |
| −1.00 … +4.89 (**spine**) | 5.89 | **+31.73** |
| +4.89 … +11.20 | 6.31 | +28.98 |
| +11.20 … +18.65 (south corner) | 7.45 | +26.52 |

**West end** — four strips: −24.46 (north corner, chopped back 5.5 m at
Clay/Drumm), −30.01, **−31.72** (spine), −30.20 across the whole south half.

**Long faces** — the south face is one straight 56.74 m run; the north face is
one straight 51.3 m run ending at the chopped north-west corner. Neither has a
bay, a facet or a setback. This is King's "blunt cliff".

## 4. What each side shows

**North (Clay Street / Sue Bierman Park)** — the flat blunt cliff, a perfectly
horizontal roofline across the full length, with the east-end fins stepping down
beyond it. The entrance side. Near-orthographic reference available.

**South (podium plaza)** — the same cliff, 63.5 m of it, rising out of the
Embarcadero Center promenade deck. Least documented side.

**East (toward the Embarcadero)** — the signature elevation: six parallel
north–south fins whose plan projections step out to a central spine and whose
tops step *down* away from it. Roughly five distinct top levels read in
photography. The flagpole sits on the spine.

**West (Drumm Street)** — the same chevron but shallower (1.7 m of plan
projection against the east end's 5.2 m), plus the chopped north-west corner.
Inferred: no usable west-side photograph was found.

**Top** — a pale flat deck with a parapet; on its north half a raised mechanical
curb carrying four large circular cooling towers in a row, a penthouse box and a
window-washing davit track. The crest at 179.05 m is those cooling towers.

## 5. Recognition cues, ranked

1. **The stepped chevron crown at both short ends** — spiked outcrops against a
   flat long roofline. Nothing else in San Francisco does this.
2. **Cream precast, not glass** — a pale, warm, opaque tower in a district of
   dark glass. Colour does most of the work at distance.
3. **The fine dark punched-window grid** — the facade reads as texture, never as
   reflection.
4. **Slab proportions** — 63.5 × 37.3 m at 174 m: broad from north/south, narrow
   from east/west.
5. **The rooftop cooling-tower row** — four circles in a line, from above.

## 6. Preserved / simplified

**Preserved:** the plan and both end chevrons strip by strip; the chopped
north-west corner; the flat unbroken north and south rooflines; the 173.70 m
parapet and 179.00 m plant crest; warm off-white against dark windows.

**Simplified:** ~45 real window bays per long face become 24 modules of 7 stacked
panes (a ~5-storey horizontal beat) rather than 45 spandrel courses; the
Embarcadero Center promenade bridges, retail spine and neighbouring towers are
out of scope and the podium becomes one low plinth; rooftop plant is exactly the
four cooling towers, one penthouse and the davit.

**Exaggerated:** the fin reveals, so the chevron reads at 200 px; and the west
end's south flank, recessed from the measured −30.20 to −29.40 / −28.60 so the
west spine stands 2.1 m proud instead of 1.7 m. The overall −31.72 … +31.73
length is untouched, so the exaggeration is spent inside the plan rather than on
it.

## 7. Uncertainties and conflicting evidence

1. **Crown step heights are estimated.** 135.10 m and 154.40 m are back-derived
   from a five-floor step counted off perspective photography at 3.86 m/floor.
   The step *count* and the *strip widths* are measured; the *heights* are not.
2. **The west end is inferred**, mirrored from the east with the measured plan
   applied. Every usable photograph found is of the east end.
3. **Cladding conflict.** `buildingsdb.com` describes a glass-and-metal curtain
   wall; the CTBUH and SFYIMBY photographs show punched windows in a solid
   precast grid, and SPUR describes the complex as concrete. The photographs win.
4. **A possible north–south roof level change.** Google's z20 tile shows the
   bright cooling-tower deck occupying only ~19.5 m of the 37.3 m footprint
   depth. The near-orthographic north elevation shows a single flat roofline,
   which says that band is the raised mechanical curb, not a lower roof. Modelled
   as a curb.
5. **Completion year** is 1982 on Wikipedia, Structurae, SkyscraperPage and
   Wikidata; CTBUH says 1984. Does not affect the model.
6. **ZIP.** The task named 94105; the building is 94111. Same building.
