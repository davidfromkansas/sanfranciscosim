# 248–250 Ritch Street — reference dossier

Compiled 18 August 2026 for `artifacts/248-ritch/`. Everything here was verified
in this session against the sources named; where this dossier disagrees with
`docs/asset-plans/248-ritch.md`, the disagreement is called out explicitly and
**this file wins** (and `REPORT.md` records why).

---

## 1. What this building is

A **1915 wood-frame two-flat** at 248 and 250 Ritch Street, San Francisco 94107 —
one building, two units, two storeys over a raised basement, on a standard
25 × 75 ft SoMa alley lot. It is the last pre-1920 domestic fabric on this face
of Ritch Street, standing directly against a 2013 five-storey apartment block.

| Item | Value | Source | Confidence |
|---|---|---|---|
| Address | 248 **and** 250 Ritch St — both on one parcel | DataSF EAS `ramy-di5m` | **verified** |
| Parcel | Block 3776 Lot 105 (APN 3776-105), range 248–250 | DataSF Parcels `acdm-wktn` | **verified** |
| Built | 1915 | SF Assessor `wv5m-vpq2`, all roll years | **verified** |
| Class / use | `F` "Flats & Duplex", Multi-Family Residential, 2 units, 9 rooms | SF Assessor | **verified** |
| Storeys | 2 — and never altered: every DBI permit 1996–2025 records "2 → 2" | DBI `i98e-djp9` (7 records) | **verified** |
| Construction | Wood frame, Type V | DBI permits ×4 | **verified** |
| Building area | 2,100 sq ft (195.1 m²) over two floors ≈ 97.6 m²/floor | SF Assessor | **verified** |
| Lot area | 1,873 sq ft (174.0 m²) | SF Assessor | **verified** |
| Zoning | CMUO (Central SoMa Mixed Use Office) | DataSF Parcels | **verified** |
| Frontage | **7.601 m** between party lines | DataSF surveyed parcel geometry | **measured** |
| Lot depth | 23.9 m | DataSF surveyed parcel geometry | **measured** |
| Built depth | **13.9 m** — the rear ~10 m of the lot is garden | derived twice, §4 | **measured** |
| Roof deck | **7.95 m** | DataSF LiDAR `hgt_mediancm`, 657 cells | **measured** |
| Cornice crest | **8.6 m** | two independent derivations, §4 | **measured** |
| Front normal | **45.05° true** (north-east, onto Ritch St) | surveyed corners + DataSF street centreline | **measured** |
| Works | reroof 1996; rear-only vinyl siding on #250 and two fireplaces + their "chimneys 1/2 way back on side" removed, both 2008; reroof May 2023 ($24,800); front-stair concrete repair Oct 2025 | DBI `i98e-djp9` | **verified** |
| Neighbours | **246 Ritch** (NW): 2013, five storeys, 50 ft, 19 units, LiDAR median **15.87 m**. **252–254 Ritch** (SE): a twin two-flat, LiDAR median **8.04 m** | DataSF LiDAR; SocketSite | **measured** |

---

## 2. Sources, and what each one establishes

**Records**

- `data.sfgov.org/resource/acdm-wktn` — the surveyed parcel. Establishes the
  7.601 m frontage, the 23.9 m depth, the two street corners the whole model is
  laid out from, and the address range 248–250 (which is what rules out a
  sibling session building an overlapping asset).
- `data.sfgov.org/resource/wv5m-vpq2` — the Assessor's roll. 1915, two storeys,
  two units, 2,100 sq ft. Nineteen roll years, no disagreement.
- `data.sfgov.org/resource/i98e-djp9` — seven DBI permits. The load-bearing ones
  are the 2008 pair (both "2 → 2 storeys", wood frame, the rear-only vinyl
  siding, the chimney removal) and the Oct 2025 front-stair repair, which is the
  only record that mentions the stoops.
- `data.sfgov.org/resource/ramy-di5m` — the EAS address file. 248 and 250 both
  on parcel 3776105; 246 carries 24 unit rows (the condo block); 252/254 sit on
  3776106.
- `data.sfgov.org/resource/ynuv-fyni` — LiDAR building footprints. SF3776105
  (this lot, 657 cells), SF3776456 (246), SF3776106 (252–254).
- `data.sfgov.org/resource/3psu-pn9h` — street centrelines. CNN 11039000, Ritch
  St Bryant→Brannan, bearing **135.08°**. *This* is how the street side was
  established. The EAS address point is 3 m off the footprint and was not used.
- `openstreetmap.org/way/147508934` — `addr:housenumber=248;250`,
  `source=Bing`. Its **size** is useful (13.84 × 7.88 m oriented bbox); its
  **position** is not — see §7.

**Visual**

- Google Street View panorama `NZPnD4HS00ZlmXcGCinZew` (2025), plus
  `HQ6do5b67CwJjoJKQJ0G3w` and `Ygw6B2E0AIVV9jLc04IjdQ` for cross-checks. The
  whole north-east elevation, **rectified to metres** in §4.
- Google Maps satellite, z21 tiles over 37.78017,−122.39572, with the surveyed
  parcel ring overlaid. Establishes the roof outline, the built depth and the
  rear garden.
- augrented.com/sf/3776105-248-250-ritch-st — a permit-derived building summary.
  Corroborates 1915 / two units / two storeys and dates the 2023 reroof.
- socketsite.com (2009, 2012) on **246 Ritch** — the five-storey, 50 ft, 19-unit
  block next door. This is the source that explains the LiDAR maximum (§4).

**A finding about the sources themselves.** An Exa sweep with four query
variants returned ten results, and **nine of them are about 246 Ritch, not this
building**. There is no architectural press, no listing photography, no
Wikipedia entry and no historic-survey document for this house. The visual
record is Street View and the satellite, and nothing else. That is why §5's rear
and party-wall entries are marked *inferred* and why §7 lists them as the
standing risks.

---

## 3. Orientation and placement

Ritch Street is a 25-foot alley on the SoMa 45° grid, centreline bearing
**135.08° / 315.08°**. This lot is on the south-west side; the house faces
**north-east**.

Surveyed street corners, in app metres (`+x` east, `+z` south):

```
E = (3687.77, -1126.69)   front × south-east party line (252-254)
S = (3682.40, -1132.07)   front × north-west party line (246)
```

Frontage line bearing **315.05°**, front outward normal **45.05° true**. The
house occupies the front 13.90 m, built to the street line and both side lines.

| Edge | Length | Outward normal | What it is |
|---|---|---|---|
| front | 7.60 m | **45.05°** | Ritch Street — the only public face |
| SE flank | 13.90 m | 135.05° | party wall against 252–254 (same height — never shows) |
| rear | 7.60 m | 225.05° | onto the garden |
| NW flank | 13.90 m | 315.05° | party wall against 246 — **exposed**, 246 is 15.87 m |

Manifest anchor (bbox centre after recentring): **−122.3956749, 37.7801751**.
The design anchor — the centre of the built quad — is −122.3956780, 37.7801725;
the 0.4 m difference is the two stoops, which project 1.20 m onto the pavement
exactly as they do in the real city and pull the bounding box north-east.

Because the building sits at 45°, the axis-aligned XY bounding box is
**15.82 × 15.82 m** for a 7.60 × 13.90 m building. That is expected.

---

## 4. The measurements

### 4.1 Why the LiDAR maximum is refused

`ynuv-fyni` reports `hgt_maxcm = 1427` for this footprint — 14.27 m, which would
make it a five-storey building. It is not: the Assessor says two storeys and all
seven permits record "2 → 2". The maximum is **the neighbour**. 246 Ritch was
rebuilt in 2012–13 as a 50-foot, 19-unit block; its own LiDAR record reads median
15.87 m, and its wall stands on the shared party line, so a handful of boundary
cells is all it takes. The January 2025 fallen-tree report on this address is a
second candidate for a few high returns.

### 4.2 Method A — the LiDAR as a two-level mixture

The summary reads **mean 6.24 < median 7.95 < mode 8.27**, sd **3.08 m** over
657 cells. Mean below median below mode with a large sigma is the signature of a
**two-level** footprint, not a noisy one-level one. Solving

```
f·H + (1−f)·L = mean        f(1−f)(H−L)² = sd²
```

- fixing H at Method B's answer gives **f = 0.650, L = 2.04 m**
- fixing f from the OSM ring's share of the LiDAR ring (0.62) gives
  **H = 8.65 m, L = 2.30 m**

The two levels are the house (high) and the garden with its shrubs and fence
(low). f = 0.650 of 164.25 m² is **106.8 m² of house**, i.e. **14.05 m of depth**
on a 7.601 m frontage — which agrees with the OSM oriented bbox (13.84 m) to
0.2 m without being derived from it. The satellite frame shows exactly this: light
membrane roof over the front two-thirds of the parcel ring, dense green over the
rear third.

### 4.3 Method B — the panorama, rectified

Pano `NZPnD4HS00ZlmXcGCinZew`'s **reported position was wrong and was discarded**.
It places the lens 5.32 m from the block face; solving instead from three
collinear surveyed corners — 252–254's far corner, the 252|248 party line and the
248|246 party line, spaced 7.601 m apart — against their observed columns in the
zoom-3 equirectangular tiles gives

```
perpendicular distance  8.56 m
position along the face  essentially opposite the 252|248 party line
```

a **3.9 m correction**. It is the difference between a facade that measures 4.3 m
wide and one that measures 7.60 m. Reading the rectified equirect at a 2.5 m lens
height:

| Feature | Height |
|---|---|
| main floor / top of the raised basement | **1.46 m** |
| lower window sills | 2.31 m |
| lower window heads | **4.00 m** |
| upper bay sill course | 5.44 m |
| upper window heads | **7.26 m** |
| cornice springing | ~7.60 m |
| **cornice crest** | **8.50 m ± 0.4** |

### 4.4 Why the two agree

The rectification returns the storey structure as a by-product: **3.26 m floor to
floor**. Stacking 1.46 + 3.26 + 3.26 puts the second-floor ceiling at **7.98 m**,
against the LiDAR's median roof of **7.95 m**. Neither number was fitted to the
other. That is what licenses "measured" rather than "estimated", and it pins the
2.5 m camera-height assumption to about 0.1 m.

**Adopted: roof deck 7.95 m, cornice crest 8.60 m** (the mean of 8.65 and 8.50,
rounded to the nearest 5 cm).

---

## 5. What each side shows

**North-east (Ritch Street) — observed and rectified.** 7.60 m wide, two storeys
of cream-painted shiplap with slate blue-grey trim, in two unequal halves.

*South-east half (t 0.5–3.9 m from the party line):* a **canted bay** through both
storeys — a ~2.3 m flat front face with a 45° return either side, projecting
about 0.4 m. Three lights per level: a narrow sash on each return, a wide one
across the front, all in broad flat cream architraves. Blue-grey sill courses cap
the bay at 5.44 m and 2.31 m, and a water table at 1.46 m marks where it meets the
raised basement.

*North-west half (t 3.9–7.60 m):* flat wall. One tall window upstairs, head at
7.26 m. Downstairs, **two entries side by side** under one continuous dentilled
hood at ~4.0 m — **250** to the south-east, **248** to the north-west — each on
its own blue-grey concrete stoop, the north-west one with a thin metal handrail.
Both doors sit behind a shallow reveal.

*Across the top:* a **bracketed cornice** — modillion brackets over a dentil band,
plain crown above, projecting ~0.35 m, stepping out and back around the bay's two
angles. Its top edge is the highest point of the building.

*Below:* the **raised basement**, a 1.46 m blue-grey band with a small square
window under the bay and a service opening toward the north-west end.

**South-east flank (13.9 m) — inferred.** Blind. 252–254 is the same era and
within 0.1 m of the same height (LiDAR median 8.04 against 7.95), built to the
same party line, so almost none of this wall is ever exposed.

**South-west rear (7.60 m) — inferred; nothing observed it.** The 2008 permit put
vinyl siding on the back of #250 only, "not visible from the street", so it is
utilitarian rather than designed. A 1915 two-flat of this type carries a rear
stair and small windows.

**North-west flank (13.9 m) — inferred, and it matters.** Blind like the other,
but 246 Ritch is 15.87 m against this building's 8.6, so this wall **is** exposed
in the app whenever the camera is north-west of the site. The 2008 permit's
"chimneys 1/2 way back on side" places a chimney breast on one of the two flanks
about 7 m back; this model puts a shallow breast on **both**, which is what the
plural in the permit describes and is the only event on either wall. **No
property-line windows are invented** — unlike 550 Third, no permit here records
any.

**Top — a designed facade.** Flat deck at 7.95 m behind a cornice standing
0.55–0.65 m proud on the street side, re-roofed May 2023 so the membrane is clean
and light. Nothing on the satellite contradicts a plain deck.

---

## 6. Recognition cues, ranked

1. **The canted two-storey bay** on the left half of a 7.6 m front.
2. **The bracketed cornice** stepping around it.
3. **Twin stoops, twin doors, one hood** — the visible signature of a two-flat.
4. **Cream over slate blue-grey.**
5. **Its size next to 246** — two storeys against five. Getting 8.6 m exactly
   right is what makes that contrast land in the scene.

**Preserve:** the bay's three-light rhythm; the cornice's step around the bay;
two doors, not one; the raised basement as a distinct dark base; the building
stopping two-thirds back.

**Simplify:** the dentil band to one scored strip, not individual teeth; the
brackets to ten arrayed blocks; the handrail to two posts and a bar; window sash
subdivision to nothing at all.

---

## 7. Uncertainties and conflicting evidence

1. **The rear and both party walls are unobserved.** Nothing in the record shows
   them. §5's entries for them are inference from the type plus two permit
   fragments. This is the largest open question in the asset.
2. **OSM is misregistered here.** Way 147508934 is Bing-traced and sits ~2.5 m
   north-west of the survey — far enough that its centroid lands nearer 246's
   ring than the middle of this lot. Its size is used as a depth check; its
   position is not used at all. 252–254's OSM trace (way 147508935) is offset the
   same way, which matters for the exclusion radius (`docs/asset-plans/248-ritch.md`
   §2.13).
3. **The bay's exact geometry is rectified, not surveyed** — good to roughly
   ±0.15 m horizontally. Treat the widths and entry positions as proportions.
4. **The Street View camera position conflict** (§4.3) was resolved in favour of
   the panorama-solved position. The reported lat/lon disagrees by 3.9 m and
   would have produced a facade 43% too narrow.
5. **`hgt_maxcm` disagrees with everything else** and is refused (§4.1). Any
   future reader who reaches for 14.27 m should read that section first.
