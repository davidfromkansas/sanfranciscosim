# 590 Third Street — reference dossier

Compiled 13 August 2026 for `artifacts/590-third/`. Plan:
`docs/asset-plans/590-third.md`. Build decisions and corrections:
`REPORT.md` — where the two disagree, REPORT wins.

**What it is.** A two-storey painted-stucco commercial corner block of about
1905, holding the **west corner of 3rd and Brannan** in SoMa. One parcel, one
building, filling its lot corner to corner, addressed both **590 3rd Street**
and **400 / 408 / 410 Brannan Street**. Its ground floor is a continuous glossy
near-black shopfront band — Kinoko Real Estate around the corner, Divine Yoga
Studio and a roll-up garage door on Brannan, Cafe Buenos Aires at the north-west
end of the 3rd Street face — under a plain pale-grey upper storey. The parapet
steps up over the corner bay. It stands directly across 3rd Street from
`599-third` (18.3 m), already in the scene.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/124903637](https://www.openstreetmap.org/way/124903637) | the building's existence and an independent `height=8` tag from the `#sfbuildingheights` import. Its geometry is a Bing trace (478 m², with a 0.6 m jog on the NW edge) and is **not** what this asset is built from — see §7 |
| [OSM node/12983432802](https://www.openstreetmap.org/node/12983432802) | the `Cafe Buenos Aires` POI carrying `addr:housenumber=590`, `addr:street=3rd Street`. A point-in-polygon test ties that address to way/124903637, which is how the building was identified |
| [DataSF parcels `acdm-wktn`](https://data.sfgov.org/resource/acdm-wktn.json), `blklot=3776114` | the parcel parallelogram this asset IS built from; CMUO zoning; a single undivided lot; the published centroid used as the anchor |
| [DataSF assessor roll `wv5m-vpq2`](https://data.sfgov.org/resource/wv5m-vpq2.json), block 3776 lot 114 | year built 1905, 2 storeys, construction type D (wood frame), lot area 5,318 sf, use class Industrial |
| [DataSF DBI permits `i98e-djp9`](https://data.sfgov.org/resource/i98e-djp9.json), block 3776 lot 114 | 6 records 2003–2018, all 2 storeys / wood frame (5). PA 201403100290 + 201407080660 (2014) convert retail at **410 Brannan** to a ballet studio; PA 201502027189 (2015) remodels a ground-floor toilet room at **590 3rd** under a food/beverage occupancy; PA 201103071525 (2011) repairs "exterior stucco to (e) retail store @ corner" — the only permit that names the wall material |
| [DataSF 2010 LiDAR footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json), `mblr=SF3776114` | 1,946 half-metre cells; ground mean 7.25 m; height median 7.77 m, mean 7.69 m, majority 7.82 m, **σ 0.64 m**, max 11.65 m; and the interior ring that proves the light well |
| Google Street View, capture **May 2025** (3rd Street, the 3rd/Brannan corner) and **April 2025** (Brannan Street) | every elevation observation in §4 |
| Google Maps / Vexcel aerial imagery, 2026 | the roof reading in §4 "Top" |

**Deliberately not used as evidence:** commercial listing aggregators (LoopNet,
PropertyShark). Their floor areas at this address describe individual leased
suites, not the building.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | −122.3946749, 37.7800837 | **measured** — parcel-polygon centroid; the polygon is a true parallelogram, so this equals the vertex mean exactly. DataSF publishes −122.39467485, 37.78008375 for the same parcel |
| Footprint | 21.28 m along 3rd × 23.10 m along Brannan, **491.5 m²** | **measured** from the parcel polygon |
| Cross-check | LiDAR footprint 489 m² (−0.5%); assessor lot 5,318 sf = 494.0 m² (+0.5%); OSM trace 478 m² (−2.8%) | three of four agree inside 0.5% |
| Building fills its lot | yes — LiDAR footprint 489 m² against parcel 491.5 m² | **measured**; this is why two faces are party walls |
| 3rd Street front normal | 45.2° true | **measured** |
| Brannan front normal | 135.1° true | **measured** |
| Roof membrane | **7.77 m** median above local ground (mean 7.69, majority 7.82, σ 0.64) | **measured**, LiDAR |
| Main parapet crest | ~8.40 m | *estimated* — LiDAR roof + a 0.6 m parapet scaled off Street View; OSM's independent `height=8` corroborates the band |
| Raised corner parapet crest | **9.50 m** | *estimated* — ~1.10 m above the main parapet, scaled off Street View against the known 23.10 m Brannan face. **This is `targetHeightM`.** See §7 |
| LiDAR maximum | 11.65 m | **measured but attributed elsewhere** — see §7 |
| Ground | 7.25 m NAVD88 mean, range 6.94–7.46 m | **measured** — flat made ground |
| Light well | 3.54 × 2.18 m, centred 4.81 m west and 1.94 m south of the anchor | **measured** — interior ring of the LiDAR footprint; visible in 2026 aerial imagery |
| Nearest neighbour | the brick warehouse on the NW party wall, LiDAR median **11.05 m**, 1,906 m² — taller than this building | **measured** |

## 3. Orientation

The SoMa grid is rotated ~45° from true north: 3rd Street runs 134.5 / 314.5°,
Brannan Street 45.6 / 225.6°. The building is a parallelogram, effectively
rectangular (interior angles 88.9° / 91.1°).

Parcel polygon reprojected with the app's tangent projection and recentred on
the anchor (x east, y north, metres, CCW):

```
W (-15.709,  -0.602)
S ( -0.689, -15.669)
E ( 15.714,   0.602)   <- the street corner of 3rd and Brannan
N (  0.684,  15.669)
```

| Edge | Length | Outward normal | What it is |
|---|---|---|---|
| W → S | 21.28 m | 225.2° (SW) | party wall toward 414 Brannan |
| S → E | 23.10 m | 135.1° (SE) | **Brannan Street front**, the long face |
| E → N | 21.28 m | 45.2° (NE) | **3rd Street front**, the 590 address face |
| N → W | 23.10 m | 315.1° (NW) | party wall toward the brick warehouse at 574–578 3rd |

Note that the **shorter** face is the address face on 3rd and the **longer** one
is on Brannan. Authored `+Y` = north, `+X` = east; the loader applies no
rotation. "Front faces −Y" cannot be honoured — neither street face points south
— so real-world orientation wins (AGENTS rule 5).

## 4. What each side shows

**North-east (3rd Street), 21.3 m — the address face.** Ground floor is a
continuous **glossy near-black fascia** carrying three white `kinoko` /
`REAL ESTATE` panels, with black awnings and full-height plate glass below in
dark frames, and a recessed dark entry door between bays. At the north-west end
the fascia changes to a **blue panel reading `CAFE BUENOS AIRES` /
`COFFEE  EMPANADAS  PASTRIES`** — the 590 address and the only saturated colour
on the building. The upper storey is smooth **pale warm-grey painted stucco**,
sparsely windowed: large square-ish windows with dark frames and interior blinds,
two or three across the face. A **flat white blade sign** (blank, vertical,
roughly 0.9 × 2.2 m) is fixed to the wall near the north-west end and stops below
the parapet. Plain flat parapet, thin dark cap, no cornice.

**South-east (Brannan Street), 23.1 m — the long face.** Same two storeys, same
grey stucco, same black band. This face is the regular one: **seven or eight tall
punched windows** in a steady rhythm, several with **through-wall air
conditioners** in the wall directly below. Ground floor carries a
`DIVINE YOGA STUDIO` awning with the numbers 410 / 408 / 400, and at the
south-west end a **black roll-up garage door**. The `kinoko` band wraps round
from 3rd and runs to the corner.

**The east corner.** The wall **steps up over the corner bay**, roughly 1.1 m
above the main parapet, spanning about a third of each street face, with a clean
vertical jog down on both sides. Blank grey stucco above the shopfront band, no
window in the raised portion. This is the building's only composition, and it is
aimed at the intersection. The step is a real vertical discontinuity, not a
perspective artefact — it is visible as a jog in both the May 2025 corner pano
and the April 2025 Brannan pano.

**North-west party wall, 23.1 m.** Abuts the brick warehouse at 574–578 3rd,
which is *taller* (11.05 m LiDAR), so this wall is not merely blind but largely
hidden. Plain stucco. *Inferred.*

**South-west party wall, 21.3 m.** Abuts 414 Brannan. Plain stucco, no openings.
*Inferred.*

**Top — a working brown roof.** Flat, behind the parapet, and notably **warm
brown** in 2026 aerial imagery — a built-up cap-sheet roof, not the grey membrane
of its neighbours. On it: five or six small skylights (pale squares, loosely
scattered rather than gridded); two or three mechanical / vent boxes; the
**light well** reading as a dark rectangle toward the south-west rear; one larger
pale raised box near the centre-west, *inferred* to be a roof hatch or stair
head; and the parapet cap running the perimeter, stepping up once over the east
corner. Item counts and positions are *inferred* from aerial imagery — the
pattern is real, the coordinates are free. The light well and the brown colour
are the two things worth being faithful to.

## 5. Recognition cues (ranked)

1. **The two-tone reading** — a dark ribbon wrapping the whole ground floor under
   a plain pale block. From the app's camera this is the building.
2. **The raised corner parapet** over the 3rd/Brannan corner: the only silhouette
   event, and what makes the corner read as a corner.
3. **The Brannan window rhythm with its air conditioners** — seven tall openings
   with small dark boxes under them.
4. **The brown roof with its light well** — warm brown against its neighbours'
   grey, punched by one dark rectangle.
5. **The blue `CAFE BUENOS AIRES` panel** at the north-west end of the 3rd Street
   face — the single saturated accent, and literally the address.

## 6. Preserve / simplify

**Preserved:** the parallelogram footprint and its 45.2° heading, filling the
lot; two storeys to a ~8.4 m parapet with the corner block at 9.5 m; the
continuous black band unbroken around the east corner; the step in the parapet
and its asymmetric placement; two designed street faces and two blind party
walls; grey walls + black base.

**Simplified / exaggerated:** the fascia is thickened and stands 0.20 m proud so
the band survives at city distance (style bible §9); the parapet step is built at
its full 1.10 m with a crisp ink cap so it holds a shadow line from the air;
Brannan's windows are seven punched openings on a 2.95 m pitch (rhythm, not sash
count, §5); 3rd Street's are three larger squares, deliberately sparser, because
the contrast between the two faces is real; the café sign is one flat `Toy_sky`
panel; the garage door is one recessed `Toy_roofd` panel with two ribs; the roof
carries seven skylights, four plant boxes and one stair head; the light well is a
genuine opening cut through the shell, not a painted rectangle.

**Deliberately not added:** a cornice, a corbel course, storefront pilasters, a
corner turret, a chamfered corner. Every one of those was checked against Street
View and is not there.

## 7. Uncertainties and conflicting evidence

- **The crest is estimated, not measured.** LiDAR gives the roof membrane at
  7.77 m with σ 0.64 m and OSM independently tags `height=8` — those agree and
  are safe. The 8.40 m parapet and the 9.50 m raised corner block are scaled off
  Street View against the known 23.10 m Brannan face with an eye-level camera
  ~20 m out, so ±0.5 m is possible. This is why the manifest entry carries
  `estimated: true`.
- **The 11.65 m LiDAR maximum is attributed to the neighbour, not this
  building.** It is 6σ above a roof whose σ is 0.64 m, and the NW party wall is
  shared with a brick warehouse whose own LiDAR median is 11.05 m — edge cells
  along that wall produce exactly this number. Nothing on the roof in 2026 aerial
  imagery or in any street-level view rises near 11.6 m. No penthouse was modelled
  to explain it.
- **"Built 1905" is an assessor's date on a block that burned in April 1906.** A
  post-fire rebuild of 1906–08 recorded under the pre-fire year is the likelier
  reading, and the fabric fits. It changes nothing about the massing.
- **The Brannan window count is inferred** from oblique Street View; seven is the
  built number, eight is possible.
- **The raised corner parapet's extent is inferred.** The step itself is observed
  and unambiguous; how far it runs back along each face is read off one oblique
  photograph. Built at 8.0 m along Brannan and 7.0 m along 3rd.
- **The roof is read from one aerial source.** The brown colour and the light well
  are corroborated (the well independently by the LiDAR footprint's interior
  ring); skylight and box positions are not.
- **The OSM footprint disagrees with the parcel by 2.8%** and carries a 0.6 m jog
  on the NW edge no other source shows. This asset is built from the parcel
  polygon, which agrees with the assessor's lot to 0.5% and with the LiDAR
  footprint to 0.5%. The anchor and heading barely move either way.
- **This asset must not drift toward 599 Third.** They are 57 m apart and will be
  in frame together permanently. 599 is buff walls + white window grids + a
  residential night scatter; 590 is grey walls + a black base + a continuous
  ground-level night ribbon. That contrast is the point.

## 8. Deliverables in this folder

| File | What it is |
|---|---|
| `build_590_third.py` | deterministic Blender build (`blender -b --python build_590_third.py --`) |
| `590-third.blend` | authoring scene |
| `590-third.glb` | the shipping asset |
| `render_590_third.py` | controlled review renders from the re-imported GLB |
| `validate_590_third.py` | fresh-scene contract validation of the exported GLB |
| `make_contact_sheet.py` | composes the contact sheet from the rendered tiles |
| `590-third-{aerial,top,north,east,south,west,night}.png` | review renders |
| `590-third-contact-sheet.png` | the review sheet |
| `validation.json` | machine-readable validation report |
| `REPORT.md` | build report, corrections, height decision, validation, manifest entry |
