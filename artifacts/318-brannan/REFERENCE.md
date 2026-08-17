# 318 Brannan Street — reference dossier

Compiled 16-17 August 2026 for `artifacts/318-brannan/`. Everything below was
re-verified against primary sources during the build; where it corrects
`docs/asset-plans/318-brannan.md`, the correction is called out and repeated in
`REPORT.md`. Nothing here is inherited on trust.

## 1. Identity

| | |
|---|---|
| Address | 318 Brannan Street, San Francisco, CA 94107 |
| Block / lot | 3775 / 100 (`blklot 3775100`, active, mapped 1998-07-01) |
| Built | **1961** (National Register district report) / 1962 (SF Assessor) |
| Structure | Reinforced concrete, concrete exterior |
| Storeys | 2 |
| Use | Commercial office (Assessor class `O`, 0 dwelling units) |
| Historic status | Within the **South End Historic District** (NR-listed 2008) but **Not Evaluated / Non-contributory** — a modern intrusion among 1900s-20s warehouses |
| Zoning | CMUO — Central SoMa Mixed Use (Office) |
| Occupants | KCA Engineers, Inc., 2nd floor (est. 1960; the address "318 Brannan St #2" is their suite). Ground floor marketed vacant 2024-25; previously Zephyr Real Estate; earlier Botrista Technology, Funomena, ScoutRFP, Izmocars |

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3775100` | the address→lot link, the parcel polygon (627.7 m2), and therefore the side and rear yards |
| DataSF Building Footprints `ynuv-fyni`, `sf16_bldgid 201006.0008516` (`mblr SF3775100`) | the **measured footprint**: a clean four-vertex 17.96 x 23.87 m rectangle, 428.8 m2. Heights: `hgt_majoritycm 778`, `hgt_median_m 8.11`, `hgt_mincm 322`, `hgt_maxcm 4202`, `gnd_min_m 11.56`, 1,730 cells at 50 cm |
| SF Assessor Historical Secured Rolls `wv5m-vpq2` | 1962, 2 storeys, 9,600 sq ft building on a 6,769 sq ft lot, Commercial Office — **identical in all 19 roll years 2007-2025** |
| SF Building Permits `i98e-djp9` | 1982-05-13 #8203762 "bldg use: office"; 2004-05-18 #200405184153 reroofing ($32k). **No facade alteration on record** — the photographs and the 1961 fabric agree |
| National Register certification, South End Historic District (2008-06-26), sfplanninggis.org | "1961, 2-story reinforced-concrete office structure with concrete exterior"; Not Evaluated / Non-contributory |
| THG Commercial listing + flyer `318-Brannan-Ken-20250909_compressed.pdf` (Sept 2025) | a near-orthographic **front elevation photograph**; the **ground-floor plan at 1" = 10'**; two interior photographs; attributes: roll-up door, high ceilings, two sides of windows, dedicated reception, six private offices, two conference rooms, data room, kitchenette, ±4,500 sq ft |
| kcaengineers.com | occupancy, and the locating sentence "the second building on the north side of Brannan Street west of the intersection of Brannan and Second Street" |
| Google Street View, Brannan St — **May 2025** (straight-on and close obliques) and **Dec 2024** (oblique from the southwest) | current condition: both awnings, the ribbon window, the storefront, the broad pier, the number bay and its recessed entrance; 318 read against 334/340 next door |
| Bing / Vexcel aerial, z20 | the roof: pale membrane, white coping ring, one square skylight, the duct ladder, the mechanical cluster; and the side-yard parking against the NE flank |
| OSM way 112759869 | address and `height=8` corroboration only. Its 6-vertex ring (451 m2) agrees with DataSF to 5% and was **not** used for measurement |

## 3. Verified dimensions and location

- **Anchor (WGS84):** `-122.3927890, 37.7816014` — the centroid of the DataSF footprint rectangle, which is the geometry the model is centred on.
- **Footprint:** 17.96 m (Brannan frontage, SE) x 23.87 m deep. Opposite edges agree to 3 mm; this is a true rectangle and nothing was regularised away.
- **Area cross-check:** 428.8 m2 x 2 storeys = 9,232 sq ft against the Assessor's 9,600 sq ft, and the THG plan's depth:width ratio of 1.32 against a measured 1.329. Three independent sources, one footprint.
- **Heights:** roof membrane **7.90 m**; parapet cap **8.60 m** (the model's bbox top). Derived from the LiDAR modal roof plane of 7.78 m plus a 0.7 m parapet; the LiDAR *median* of 8.11 m is inflated by the extensive rooftop ductwork and is not the deck.
- **Ground:** 11.56 m NAVD88 minimum, 12.00 m modal. The app's terrain handles this; the asset sits on z = 0.

## 4. Orientation

Rotated ~45.8° off the world axes, like the whole SoMa grid.

| Elevation | Length | Outward bearing |
|---|---|---|
| Brannan Street front | 17.96 m | **135.8° (SE)** |
| Northeast flank | 23.87 m | 45.8° |
| Rear | 17.96 m | 315.8° |
| Southwest flank | 23.87 m | 225.8° |

Authored with Blender `+Y` = true north, `+X` = east, so the loader applies no
rotation. The axis-aligned bounding box is therefore ~29.6 x 30.2 m for a
17.96 x 23.87 m building — expected, not a scale error. (Y runs 0.5 m longer
than X because the awnings project up to 1.2 m off the SE face.)

## 5. Site — why all four sides are designed

Measured, parcel polygon against footprint polygon:

- **Northeast:** a **4.75 m side yard** running the full depth, used for parking. The flank is fully exposed.
- **Northwest:** a **5.7 m rear yard**.
- **Southwest:** the building sits ~0.9 m off the property line, and 326 Brannan beyond it is a single-storey tasting room in an open fenced yard. The flank is exposed above it.
- **Southeast:** on the Brannan property line.

This is the only landmark on this block face without a party wall. There is
nowhere to hide an undesigned elevation.

## 6. Observations by side

**Southeast (Brannan front) — the hero.** Off-white painted concrete in five
horizontal layers: a low pale bulkhead; large plate-glass storefront bays in
slim pale frames around one broader central pier; a **full-width dark awning**
projecting over the whole storefront and carrying the ground-floor tenant's
name; a plain pale spandrel; a continuous **second-floor ribbon window** —
horizontal aluminium sash, two rows of lights, split into two unequal groups by
one broad pale pier; a second **full-width dark awning** at the second-floor
head carrying the upper tenant's sign; a thin strip of pale wall; the flat
parapet. Past a broad pale pier at the northeast end: a dark **number panel**
with large white numerals over a **recessed glass entrance door**.

**Northeast flank.** Blank pale concrete for its full 23.87 m, with cars parked
against it. The ground-floor plan puts lobby, stairs, restrooms, copy room and
electrical room along this wall — it is a blind service elevation, and no
reference shows a window in it.

**Southwest flank.** Exposed above 326 Brannan's low yard. The listing's "two
sides of windows" and the plan's wall openings establish daylight here; the
exact rhythm is **inferred**.

**Northwest rear.** A working back onto the rear yard: pale concrete, a wide
roll-up freight door (established by the listing's attribute list and visible at
the rear of the open floor in the interior photograph), a pedestrian service
door, a second-floor window group. Position and width are **inferred** — no
reference photographs the rear.

**Top.** 429 m2 of pale-grey membrane inside a white coping ring. Northeast of
centre, a **~2.6 m square skylight** on a raised white curb — the brightest
thing up there. Across the southwest two-thirds, a **ladder-and-comb network of
raised white ducts** roughly 0.6-0.8 m wide: two trunk runs parallel to Brannan
with four branches running back from them and one spur. On the southwest side, a
cluster of **dark mechanical units**. Small round vents elsewhere. The northeast
third is clear membrane.

## 7. Recognition cues (ranked)

1. **Two full-width dark awning bands on a pale box** — the whole identity, and the only cue that survives to thumbnail size
2. **Low and wide** — 8.6 m against 334/340 Brannan's 12.1 m two doors away
3. **Mid-century concrete character** — flat pale planes, a horizontal ribbon window, no brick, no cornice, no ornament
4. **The roof's duct maze plus one bright square skylight**
5. The northeast number-panel bay with its recessed glass door

## 8. Preserved / simplified

**Preserved:** the 17.96 x 23.87 m proportion and the 45.8° heading exactly; the
two dark bands' width and their vertical relationship to the ribbon between
them; four designed elevations; the unbroken flat parapet.

**Simplified:** the ribbon's many small lights become one glazed panel per group
with a single transom reveal; the storefront becomes four glazed bays; awning
lettering, the numerals, door hardware, utility wires, parking meters, hydrant
and street trees are dropped; roof clutter reduces to one skylight, two duct
trunks + four branches + one spur, three mechanical boxes and three vent cans.

**Exaggerated:** only the awnings — thickened and raked so they cast a real
shadow line from the app's downward camera.

## 9. Uncertainties and conflicting evidence

1. **The parcel is 23.64 m wide on Brannan; the building is 17.96 m.** The
   northeast 4.75 m is a low entry / side-yard strip carrying the number panel,
   the front door and the driveway. It is **not modelled as mass**: the DataSF
   footprint excludes it, the aerial shows no roof at 7.8 m over it, and the
   Assessor's 9,600 sq ft matches 2 x 428.8 m2 but not 2 x 564 m2. Its identity
   — the number panel and the recessed entrance — is carried on the northeast
   end of the main block's own front instead. Documented at plan §2.15 risk 1.
2. **DataSF `hgt_maxcm` = 42.02 m is not this building.** Same record:
   `hgt_median 8.11`, `hgt_majority 7.78`, `hgt_min 3.22`, `std 3.51`;
   first-return stats (`median_1st_m 19.98`, `peak_1st_m 54.07`) are vegetation
   and neighbours. Scan bleed, an order of magnitude worse than the 13.32 m trap
   358 Brannan documented.
3. **The parapet height is derived, not published** (±0.4 m). The manifest entry
   is therefore `"estimated": true`. Street View cannot settle it: every
   panorama of this facade is steeply oblique (nearest camera 10 m from one
   corner, 20 m from the other), and a naive height/width ratio off them
   overstates the building by 30-40%.
4. **Build year 1961 (NR) vs 1962 (Assessor).** Both plausible — permit vs
   completion. Nothing in the model depends on it.
5. **Awning graphics change by reference date** (blank + "AVAILABLE" in the
   listing photograph, "ZEPHYR REAL ESTATE" in May 2025, marketed vacant again
   in the Sept 2025 flyer). The upper "KCA ENGINEERS, INC." awning is constant.
   The model carries the *bands*, not the lettering.
6. **The southwest flank's window rhythm is inferred** — no reference photographs
   that flank directly.
7. **The rear has never been photographed** in any source consulted.
</content>
