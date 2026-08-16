# 358 Brannan Street — reference dossier

Compiled 12 August 2026 for `artifacts/358-brannan/`. This is the modelling
authority for the asset; where it disagrees with `docs/asset-plans/358-brannan.md`,
this file and `REPORT.md` win (the plan is a head start, not a citation).

## 1. What the building is

A 1910 two-storey industrial building on a single 25-foot SoMa lot, mid-block on the
northwest side of Brannan Street between 350 and 362-366. It is a **through-lot**: it
runs the full 25 m depth of the block and has a second front on the Varney Place alley.
The ground floor is a batting cage and bullpen (The Natural, entrance on Varney);
Goff Photography also lists at the address. It is marketed as flex space with a roof
deck.

The reason it earns a bespoke asset is proportion, not ornament: at 6.93 m of frontage
it is roughly a third the width of either neighbour, and it is painted terracotta red
between two pale warehouses.

## 2. Sources, and what each establishes

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3775017` | **The address-to-lot link.** `from_address_num = to_address_num = 358 BRANNAN ST`, active, mapped 1998-07-01, zoning CMUO. Neighbours: 016 = 350, 018 = 362-366, 020 = 370, 021 = 372-374, 022 = 376-380 (the existing `380-brannan` asset) |
| DataSF Building Footprints `ynuv-fyni`, `mblr = SF3775017` | The authoritative footprint polygon (166.5 m2) and the LiDAR height statistics: `gnd_min_m 10.27`, `hgt_median_m 7.74`, `hgt_meancm 852`, `hgt_mincm 418`, `hgt_maxcm 1332`, `hgt_stdcm 228`, 674 cells at 50 cm |
| SF Assessor Secured Roll `wv5m-vpq2`, block 3775 lot 017 | Built **1910**; **2 storeys**; property area 2,860 sq ft; lot area 1,760 sq ft; use "Industrial". Identical in every roll year 2007-2025 — no drift, unlike 380 Brannan's contested storey count |
| SF Building Permits `i98e-djp9`, block 3775 lot 017 | Three permits only. 2012-12-12 kitchen/powder-room remodel; 2014-02-28 final inspection; **2022-10-21** planning-enforcement permit for complaint #2020088enf: *"remove storefront & brannan facade, legalize varney place facade"*. All three record 2 existing / 2 proposed storeys and use "1 family dwelling" |
| OSM way 124890324 | Address confirmation only. Its geometry is `source=Bing` and is **wrong** — see §7 |
| Google Street View, Brannan Street pano, capture **May 2025** | The front elevation: terracotta paint, the canted bay, the sign band, the roll-up door, the pedestrian door, the "358" plate, and the fact that the parapet sits below both neighbours' |
| Google Street View, Varney Place pano, capture **Jan 2025** | The rear elevation: slate blue-gray multi-light timber storefront, pedestrian door, roll-up freight door, steel header with conduit and floodlights, brown horizontal wood siding above, light posts at the roof line |
| Google Maps satellite (Vexcel imagery, 2026) | The two roof levels, light membrane deck, scattered roof furniture, and that the lot is built out wall-to-wall on both flanks |
| thenaturalsf.com | *"358 Brannan St. San Francisco, CA 94107 — ENTRANCE IN BACK ALLEY ON VARNEY"* — independent confirmation of the through-lot, from the tenant rather than from the permit |
| LoopNet / Showcase listing, "358 Brannan St" | 2,860 sq ft, 1910, 2 storeys; roof deck/patio, two breakout spaces, rear loading access, one roll-up door, full kitchen |

No copyrighted imagery is committed to this repo. Panorama captures are cited by
location and date so they can be re-opened.

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.3936350, 37.7809258` | **measured** — minimum-area OBB centre of the DataSF polygon |
| Footprint | 6.93 m (SE frontage) x 25.20 m deep, 166.5 m2, 95.3% rectangular fill | **measured** |
| Cross-check | Assessor lot area 1,760 sq ft = 163.5 m2 | agrees to 1.8% |
| Brannan front heading | 135.3° true (SE) | **measured** |
| Varney rear heading | 315.3° true (NW) | **measured** |
| Rear roof deck | 7.70 m above ground | **measured** (LiDAR median 7.74) |
| Front roof deck | 8.40 m | *inferred* — reconciles the 7.74 median with the 8.52 mean |
| Front parapet crest | 9.00 m | *estimated* — photogrammetric, see §5 |
| Bay cornice cap | **9.60 m** — the export's bounding-box top | *estimated*, semantic lift of ~0.6 m over the parapet |
| Ground elevation | 10.27 m NAVD88 | measured; the app's terrain handles this, not the asset |

## 4. Orientation

Authored in true-world orientation: Blender `+Y` = north, `+X` = east, origin at the
footprint OBB centre, min Z = 0. The loader (`placeGeneric` in `app/src/assets.js`)
scales and positions but never rotates, so the model must carry its own 45° heading.

The contract's "front faces −Y" rule cannot be honoured literally — the front faces
SE at 135.3°. Real-world orientation wins (AGENTS rule 5); the deviation is recorded
here and in `REPORT.md`, consistent with every other plan in this set.

Footprint rectangle, CCW, metres from the anchor:

```
(-6.406, 11.391)   ->  (-11.328, 6.517)    6.93 m, outward NW 315.3°  Varney Place
(-11.328, 6.517)   ->  (6.406, -11.391)   25.20 m, outward SW 225.3°  party wall to 350
(6.406, -11.391)   ->  (11.328, -6.517)    6.93 m, outward SE 135.3°  Brannan Street
(11.328, -6.517)   ->  (-6.406, 11.391)   25.20 m, outward NE  45.3°  party wall to 362-366
```

The axis-aligned bounding box is therefore ~22.9 x 23.1 m for a 6.93 x 25.20 m
building. That is the 45° heading, not a scale error.

## 5. Observations, side by side

**Southeast — Brannan Street (hero).** Terracotta / brick-red painted wall, two storeys,
plainly lower than both neighbours. A flat parapet with a slight central rise. A
**canted bay window** projects from the second floor: a flat outer face carrying two
tall windows, plus one window on each angled cheek, light frames, small cornice cap
riding just proud of the parapet. Directly under the bay, a dark **sign band** carrying
the batting cage's name. Ground floor: a wide grey **roll-up freight door** taking most
of the frontage, a small diamond hanging sign, a narrow **pedestrian door** at the
northeast end, "358" above it.

**Northwest — Varney Place (second front).** Full-width **slate blue-gray painted timber
storefront**: a grid of multi-light industrial sash three panes high, a pedestrian door
left of centre, a roll-up freight door filling the right half. A steel header with
conduit and floodlights caps it. Above, a second storey clad in **brown horizontal wood
siding**. Above that, light posts at the roof line — the roof-deck railing.

**Northeast and southwest flanks.** Blind party walls, 25 m long, hard against 362-366
and 350. Nothing in any reference shows either surface; they are modelled as the pale
body colour with no openings, which is both the truthful and the calmer answer.

**Top.** Two levels. The rear two-thirds is a light membrane deck at ~7.7 m with the
roof-deck railing at its Varney end; the front third steps up ~0.7 m inside a parapet.
Scattered furniture: a short skylight run, one mechanical block, a hatch.

### How the height was derived

No published height exists for this building. The May 2025 Brannan panorama was scaled
against the **measured** 6.93 m frontage: the red facade measures ~108 px wide and
~131 px from sidewalk to parapet in the same frame, giving a parapet of 8.4-9.2 m
depending on where the sidewalk line is read; the roll-up door comes out at ~3.4 m,
which is a plausible SF freight opening and supports the calibration. **9.00 m** is
taken for the parapet, **9.60 m** for the bay cap, with roughly ±0.6 m of uncertainty.
The manifest entry is therefore `"estimated": true`.

## 6. Recognition cues (ranked)

1. **Extreme narrowness** — 6.93 m of frontage between a 20 m and a 25 m one
2. **The canted bay window** over the freight door — the only bay on this block face
3. **Terracotta red between two pale warehouses**
4. The dark sign band under the bay
5. The two-level roof with a used roof deck at the Varney end

## 7. Uncertainties and conflicting evidence

- **The OSM footprint is wrong, and it is the trap in this dossier.** Way 124890324
  (`source=Bing`) traces a 115 m2 stub, 16.7 x 7.2 m, oriented as if the building were
  wide and shallow — the opposite of the truth. The DataSF LiDAR footprint (166.5 m2,
  6.93 x 25.20 m) and the Assessor's 1,760 sq ft lot area agree with each other, and the
  through-lot they imply is independently confirmed by the 2022 permit and by the
  tenant's own directions. **DataSF is used.** An agent starting from OSM would build
  this building rotated 90° from reality.
- **DataSF `hgt_maxcm` = 13.32 m is almost certainly not this building.** The same
  record gives median 7.74, mean 8.52, min 4.18, std 2.28 over 674 cells. A 13.3 m
  maximum with a 7.7 m median on a 166 m2 roof is a handful of cells, and the taller
  neighbour at 362-366 has a wall directly on the shared boundary. Treated as
  polygon-edge bleed, not as a penthouse. This is the mirror image of the trap the
  plans README documents: there OSM `height` tags *understate* crests, here a LiDAR
  maximum *overstates* one.
- **The target height is estimated**, per §5. It is the weakest number in this dossier.
- **Photographs disagree by date.** Permit #2020088enf ordered the Brannan storefront and
  facade removed and the Varney facade legalized. Both panoramas used here post-date it
  (May 2025, Jan 2025) and show the current condition; any older photograph of this
  building may show a facade that no longer exists.
- **Assessor "Industrial" vs permits "1 family dwelling."** Both are true of a live/work
  conversion inside an industrial shell. The *form* is industrial, which is what the
  model builds, and `cat 19` (Industrial) is what the manifest carries.
- The bay is read as a true three-sided canted bay from a single frontal photograph;
  the angled cheeks and their windows are visible, but an oblique view would settle it.
  *Inferred.*
- The pale colour of the flanks is *inferred*; nothing shows them.
- No architect is recorded for the 1910 building in any source consulted.
</content>
