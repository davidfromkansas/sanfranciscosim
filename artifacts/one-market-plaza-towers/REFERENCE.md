# One Market Plaza — Spear Tower and Steuart Tower — reference dossier

Compiled 19 August 2026 for `artifacts/one-market-plaza-towers/`. Records what
was verified independently before modelling, and where the plan needed
correcting. Where this file and the plan disagree, this file and `REPORT.md` win.

## 1. Identity

| Item | Value | Source |
|---|---|---|
| Complex | **One Market Plaza**, alt. *Del Monte Building*; 1 Market Street, block **3713** lot **007** | Wikipedia; SF Planning ZA letter; SF Assessor |
| Completed | **1976**; renovated 1996 (César Pelli) and 2014–16 | Wikipedia |
| Architect | **Welton Becket Associates** | Wikipedia (One Market Plaza; Steuart Tower) |
| Owner | Paramount Group / Blackstone | Wikipedia |
| **Spear Tower** | **172 m (564 ft)**, 43 storeys (CTBUH: 42 above ground) | Wikipedia + CTBUH agree; **DataSF LiDAR `hgt_median` 172.41 m** agrees to 0.4 m |
| **Steuart Tower** | **111 m (364 ft)**, 27 storeys (its own Wikipedia article says 28) | Wikipedia + CTBUH agree; corroborated below |
| Podium | **6 storeys**, roof **27.8 m** | SF Planning ZA letter; DataSF LiDAR `hgt_median` 27.75 m |
| Complex floor area | 1,460,071 sq ft (Wikipedia); lot roll 1,534,312 sq ft on 113,198 sq ft | Wikipedia; SF Assessor |
| Facade | both towers **white**, dark recessed window slots | Wikipedia aerial caption names them "the shorter white building" and "the taller white building"; the pier detail is *observed* from nadir imagery |

**Not this asset:** the 1916 Southern Pacific Building on the same address, and
the glazed atrium in its courtyard. Both belong to `artifacts/1-market/`, built
in the same batch. The two assets abut along the shared survey edge from
`(3777.2, −2606.5)` to `(3814.4, −2569.9)` in the app's local frame.

## 2. Heights

**Spear Tower is measured, not just published.** Its shaft has its own DataSF
LiDAR footprint (`ynuv-fyni`, `mblr = SF3713007`, `sf16_bldgid` 201006.0001309):
`hgt_median` **172.41 m** against a published 172 m, and `hgt_maxcm` **177.56 m**,
which is the rooftop plant. The export normalizes to that 177.6 m crest.

**Steuart Tower has no footprint of its own in the survey** — it sits inside the
podium polygon (201006.0000212), whose `hgt_median` is the *podium's* 27.75 m and
whose `hgt_maxcm` of 163.58 m is **Spear Tower spilling over the shared
boundary**, not Steuart. That is the same first-return artefact that put 114.92 m
on the Southern Pacific Building's footprint next door.

So the published 111 m was checked a different way. On the z20 nadir tile both
towers lean in the same direction and the lean is proportional to height.
Measured roof-corner displacement from each shaft's ground ring:

| Tower | Lean | Implied height |
|---|---|---|
| Spear (known 172 m) | **26.7 m** | — (the calibrator) |
| Steuart | **17.6 m** | 172 × 17.6 / 26.7 = **113 m** |

Ratio 1.52 against the published 172/111 = **1.55**. 113 m against a published
111 m is inside the ±10 m that ±10 px of corner reading buys, so the published
value stands and is used.

## 3. Plan

| Element | Dimensions | Source |
|---|---|---|
| Lot envelope | 7,521 m2, AABB 120.7 × 126.5 m, twelve vertices | DataSF podium ring ∪ Spear shaft ring, shared edge removed — measured |
| **Spear shaft** | **52.5 × 35.7 m**, 1,868 m2, centred local (3783.1, −2575.7) | DataSF 201006.0001309 — measured |
| **Steuart shaft** | **43.3 × 33.7 m**, 1,460 m2, centred local (3843.6, −2583.6) | OSM way/132238431, shifted **+1.9, −2.0 m** into the DataSF frame — *inferred* |
| Both long axes | NW–SE, bearing 135.2° | measured on both rings and confirmed on imagery |
| Canted corners | ~4.05 m chord in the survey; modelled at 4.6 m | OSM Spear ring's corner jog; exaggerated ~15% |

The OSM→DataSF registration offset was measured on the one building both sources
trace independently — Spear Tower — and then applied to Steuart, which only OSM
has. OSM's Spear ring is 51.4 × 34.4 m against DataSF's 52.5 × 35.7 m and offset
by (+1.9, −2.0); DataSF is the survey and is used for Spear directly.

## 4. Plaza

Located from the z20 nadir tile and **corrected for that tile's building lean**
(−0.0116, +0.1547 m per metre of height, derived from Spear's 26.7 m lean over
172 m), which at the 27.8 m plaza level is a 4.3 m correction:

| Feature | Model position | Size |
|---|---|---|
| Circular sunken garden | (−7.5, −30.7) | r 8.9 m |
| Glazed barrel-vault canopy run | (2.5, −10.8) → (22.6, −20.1) | 22.1 m long, 11 m wide, 5 vaults |

## 5. Facade

Both towers are the same building at two sizes: a canted-corner rectangle wrapped
in close-spaced white precast piers over dark recessed window slots, running
**unbroken from the podium to the parapet**. No spandrels, no banding, no crown,
no setback, and no principal elevation — all four faces are identical. Pier pitch
measured off the nadir imagery at ~3.5 m.

That uniformity is what makes the model cheap: because the slots are continuous
vertically, each shaft is **one dark prism with white pier strips applied**, with
no per-storey geometry at all.

## 6. Sources

- `https://en.wikipedia.org/wiki/One_Market_Plaza` — the complex, both heights,
  1976, Welton Becket Associates, and the aerial caption establishing the colour.
- `https://en.wikipedia.org/wiki/Steuart_Tower` — 111 m / 364 ft.
- `https://www.skyscrapercenter.com/complex/1071` (CTBUH) — independent
  confirmation of 172 m and 111 m.
- `https://sfplanning.org/sites/default/files/za/1%20Market%20Street.pdf` — lot
  007, 43 stories / 27 stories / 6-story podium.
- `https://data.sfgov.org/resource/ynuv-fyni` — the Spear shaft footprint and its
  heights; the podium polygon.
- `https://data.sfgov.org/resource/wv5m-vpq2` — SF Assessor, block 3713 lot 007.
- OSM `way/132238423` (Spear part), `way/132238431` (Steuart part),
  `way/132238424` (One Market Plaza), `way/944977178` (6-storey podium part) —
  the only source that separates Steuart's shaft from the podium.
- Google satellite z20 — canted corners, pier rhythm, plaza, garden, canopies,
  roof plant, and the lean measurement in §2.

## 7. Uncertainties carried into the model

- **Steuart's shaft footprint** is OSM-derived and shifted, not surveyed.
- **Steuart's plant crest (115.5 m)** is inferred by analogy with Spear's
  measured 5.6 m. It does not set the export height.
- **The podium is modelled as one flat 27.8 m mass.** The LiDAR polygon's mean
  (54.5 m) sits far above its median with a 40 m sigma because the polygon also
  contains both shafts, so the median is the best available read of the podium
  itself. Parts of the lot at plaza grade may sit lower in life.
- **The plaza layout** is read off a leaning nadir tile and lean-corrected; it is
  right to a metre or two, not to a survey.
