# 574 Third Street (566–586 Third Street) — reference dossier

Research behind `artifacts/574-third/`. Compiled 13 August 2026; re-verified against the
plan `docs/asset-plans/574-third.md` before modelling. Where this file and the plan
disagree, **this file and REPORT.md win** (pipeline rule: REPORT beats plan).

## 1. What the building is

A 1907 three-storey apartment block, today the "Central Apartments", occupying a whole
through-block lot on the **southwest side of Third Street** between Brannan and Bryant
and running back to the Ritch Street alley. 104 units, 232 rooms, 58,530 sq ft of floor
area on a 1,906 m2 footprint — 2.85 floors' worth, i.e. three near-full storeys. Eleven
street numbers (566–586) on one parcel; "574 3rd St" is one of its entrances.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF EAS Addresses (`ramy-di5m`) | `574 03RD ST` → block 3776 lot 008; the full 566–586 range on the same parcel; unit numbers #110, #332 |
| SF Assessor secured roll 2025 (`wv5m-vpq2`) | Built 1907; 3 storeys; 104 units; `MRES`; 58,530 sq ft; lot 21,597 sq ft |
| DataSF Building Footprints (`ynuv-fyni`, `mblr = SF3776008`) | The survey footprint (1,906.1 m2) and the LiDAR heights: median 11.05 m, mode 11.03, mean 10.93, σ 1.18 over 7,629 cells, max 15.41 |
| DataSF Parcels (`acdm-wktn`) | The 566–586 Third address range on lot 008 |
| `5743rdstcentralapartments.com` | "Established 1907", 100+ units, rent-controlled, historic building |
| `augrented.com/sf/3776008-566-586-3rd-st` | Independent restatement of 3 floors / 1907 / 104 units / 58,530 sq ft |
| KartaView seq 1352479 frame 35 (2019-03-14), Third St at Brannan looking NW | The Third Street elevation: three storeys, dark chocolate paint, tall narrow pale-framed windows in a strict grid, ground-floor shopfronts, fire escapes, bare brick at the northwest end, **rooftop billboard** |
| KartaView seqs 2042946 / 2057142 (2019-10/11), Ritch Street | The rear elevation: unpainted buff/tan brick, segmental-arched openings, fire escapes, service doors |
| Esri World Imagery z20 nadir (2023 vintage) | Flat light-membrane roof; **two long dark light wells** running back from Third Street; scattered small skylights and vents; the billboard structure at the northwest end |
| OSM ways 124903634 + 124903638 | Bing traces that between them cover the site (1,843 m2 against the survey's 1,906) but correspond to no real building division and carry none of the addresses — cross-check only |

## 3. Verified dimensions and location

- Anchor (footprint AABB centre): **lon −122.3950551, lat 37.7801937**
- Footprint 1,906.1 m2; Third Street frontage 33.95 m; Ritch Street rear 45.22 m;
  southeast flank 42.25 m; depth ~45 m
- Roof deck 11.05 m (measured); parapet ~11.9 m (inferred); billboard crest 15.41 m
  (measured as the LiDAR maximum) → model crest 15.4 m
- Ground 5.32–7.05 m NAVD88

## 4. Orientation

Third Street front faces **NE, bearing 44.8°**; Ritch Street rear faces **SW 224.9°**;
southeast party flank 132.9°; northwest party line 314.9–315.9°. Authored in true-world
orientation, so the axis-aligned bbox is 64.9 × 60.1 m for a 34 × 45 m building.

The northwest boundary is **not a straight line**: it steps in by ~8.6 m near the Third
Street end (a court), which the model keeps because it is a real feature of the plan and
it is what makes the roof outline recognizable from the air.

## 5. What each side shows

- **Third Street (NE)** — the hero elevation and the only painted one: dark chocolate
  brown, plain parapet, no cornice, two upper floors of tall narrow windows with pale
  frames in a strict grid (~11 bays real), fire escapes, a ground floor of shopfronts and
  residential entrances. The paint stops short of the northwest end, where bare buff
  brick shows and the rooftop billboard stands above it.
- **Ritch Street (SW)** — unpainted buff/tan brick, three storeys, segmental-arched
  window heads, dark fire escapes, service and garage openings at grade.
- **Southeast flank** — party wall against 400 Brannan at the street end, exposed toward
  the block interior. No photograph of this wall was found: modelled as quiet brick with
  a sparse scatter of openings, and flagged as inference.
- **Northwest flank and court** — party line against 560 Third (LiDAR height 6.66 m), so
  roughly 4–5 m of this wall stands exposed above the neighbour.
- **Top** — flat light membrane inside a continuous parapet, cut by two long dark light
  wells running back from Third Street, with scattered skylights, vents and two
  bulkheads. This is the surface the app's camera sees most.

## 6. Recognition cues (ranked)

1. Bulk and rhythm — a three-storey mass 34 m wide and 45 m deep whose Third Street wall
   is one uninterrupted grid of tall narrow windows
2. The chocolate painted front against bare buff brick everywhere else
3. The rooftop billboard over the bare northwest end
4. Fire escapes on both long elevations
5. The two roof light wells, from above

## 7. Preserve / simplify

**Preserve:** the single long volume, its 45° heading, the full through-block depth, the
northwest court step, the window rhythm and proportion, the painted/bare split, the
billboard as the crest.

**Simplify:** ~11 bays → 9 on Third and 8 on Ritch; arch heads kept on Ritch only; fire
escapes → two chunky balconies per elevation; shopfronts → five recessed glazed bays with
piers; light wells → 0.95 m recessed slots rather than full-height voids; ghost signage,
downpipes, meters and window bars dropped; the billboard is a **blank** panel — no
advertising artwork is reproduced.

## 8. Uncertainties and conflicting evidence

- **The crest is a billboard.** 15.41 m is the LiDAR maximum, 3.5 m above the parapet, at
  exactly the northwest end where the 2019 photograph shows a rooftop hoarding. If it is
  ever removed, `targetHeightM` drops to the 11.9 m parapet.
- **OSM does not know this building.** No OSM way carries any of the eleven addresses;
  the two Bing comb traces covering the site are not real building divisions.
- **Nominatim resolves "574 3rd St" onto the Third Street roadway** by TIGER
  interpolation — the same trap as 350 Brannan.
- The 11-bay real rhythm is *inferred* from one oblique photograph at ~60 m; the 9-bay
  simplification is a design decision on top of an uncertain count.
- The southeast flank's openings are entirely *inferred*.
- The exposed height of the northwest wall is *derived* from 560 Third's LiDAR height.
- No architect is recorded for the 1907 building in any source consulted.
