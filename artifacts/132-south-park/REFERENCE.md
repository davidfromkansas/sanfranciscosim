# 132 South Park (130-134 South Park) — reference dossier

The building modelled by `build_132_south_park.py`. This file records what was
verified, what was observed from a photograph, and what was inferred, so that a
later revision knows which statements it is allowed to change without new sources.

`REPORT.md` records the corrections this build made to
`docs/asset-plans/132-south-park.md`. Where the two disagree, **REPORT wins**.

## 1. Identity

| | |
|---|---|
| Addresses | 130, 132, 134, 134A South Park Street, San Francisco, CA 94107 |
| APN | block **3775**, lot **062** (`3775062`) |
| Built | **1913** |
| Type | multi-family residential; assessor class A5 (*Apartment 5 to 14 Units*) |
| Storeys | 3 residential floors over an oxblood plinth, plus a 2-storey rear cottage |
| Units | 5 per the assessor roll, 7 per the 2021 sale listing (see §5) |
| Building area | 3,630 sq ft (337 m²) per tax records |
| Lot area | 2,145 sq ft (199.3 m²) per the assessor; 200.5 m² measured from the parcel |
| Architect | none found |
| Historic status | not established either way — do not assert one |
| Manifest id | `132-south-park`; pipeline registry id `132SouthPark` |

## 2. Sources, and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| DataSF parcels `acdm-wktn`, blklot `3775062` | the surveyed lot rectangle; the whole geometry in §3 is built on it | **measured** |
| DataSF building footprints `ynuv-fyni`, MBLR `SF3775062` (2 rows) | both footprints and both heights; also the dataset the tile bake consumes | **measured** |
| DataSF EAS addresses `ramy-di5m` | 130/132/134/134A are one parcel; 126 and 136 sit either side | **verified** |
| DataSF assessor roll `wv5m-vpq2`, 19 annual rows 2007-2025 | 1913, 3 storeys, 3,630 sq ft, class A5, unchanged for 19 years | **verified** |
| [Allison Chapleau — 130-134 South Park Street (sold)](https://www.allisonchapleau.com/listing/130-south-park-street) | "Two Separate Structures on One Lot", 1913, 7 units, $2,000,000 | **verified** |
| …gallery frame `130 S Park St Drone CLEAN MLS` (2021) | **the entire front elevation** — see §4 | **observed (listing photo)** |
| …gallery frame `DJI_0611` (2021) | nadir: the shingled hood at the street edge, the flat roof, the courtyard, the wood deck and stair, the rear cottage | **observed (listing photo)** |
| …gallery frame `DJI_0602` (2021) | wide aerial context: the building in its row | **observed (listing photo)** |
| [openpermitdata.com — 130 South Park](https://openpermitdata.com/sf/address/130-south-park) | 5 permits since 2019, all minor (one $10k OTC alteration, two electrical, two plumbing) — the building is materially unchanged since the 2010 LiDAR | **verified** |
| Overpass API over the South Park oval | **OSM has no building on this lot at all** — 91 buildings returned around the oval, none on 3775/062 | **measured** |

No photographs are committed to this repository. The URLs above are the record.

**The single-photograph problem.** Every statement about the facade comes from one
2021 drone frame. It is square-on, unobstructed and high resolution, and the permit
record says the building has not changed since — but it is one frame from one
afternoon, and it shows only the front. Nothing in this dossier shows either flank
or the rear elevation.

## 3. Geometry

Projected with the app's own tangent projection (`pipeline/lib/geo.mjs`:
`LON0 −122.4375`, `LAT0 37.77`, `M_PER_DEG_LON = 111320·cos(37.77°) = 87995.7684`).

**Lot** — a standard SoMa 22 ft × 98 ft slot, **6.689 m × 29.974 m**, orthogonal to
0.14°, on the north-west arc of the South Park oval.

Local frame used throughout: `s` runs along the frontage from the **north-east**
party line (`s=0`, shared with 126 South Park) to the **south-west** party line
(`s=6.689`, shared with 136); `t` runs into the lot from the front property line
(`t=0`) to the rear line (`t=29.974`).

| Corner | `(s, t)` | World `(x, z)` |
|---|---|---|
| NE front | `(0, 0)` | `(3786.111, −1267.645)` |
| SW front | `(6.689, 0)` | `(3781.363, −1262.933)` |
| SW rear | `(6.689, 29.974)` | `(3760.204, −1284.149)` |
| NE rear | `(0, 29.974)` | `(3764.945, −1288.868)` |

| Edge | Outward bearing | What it is |
|---|---|---|
| front `t=0` | **135.1°** | the South Park front — the hero elevation |
| NE flank `s=0` | 45.2° | party line with 126 South Park (roof 7.3 m) |
| SW flank `s=6.689` | 225.2° | party line with 136 South Park (roof 3.2 m) |
| rear `t=29.974` | 315.1° | back lot line, onto the Bryant Street lots |

**Two footprints.** The 2010 LiDAR polygons land at `s [0.88, 6.91] × t [1.42, 11.71]`
and `s [0.19, 6.89] × t [20.09, 31.12]`. Both sit ~0.2 m south-west and ~1.1 m rear
of the parcel — a uniform registration offset between the two datasets, proved by the
rear polygon extending 1.15 m *past* the surveyed rear lot line. Corrected for that
offset and snapped to the lot lines, which is what a 22 ft SF lot with party walls on
both sides does:

- **front flats**: `t 0 → 10.30`, full lot width
- **courtyard**: `t 10.30 → 19.00` — **8.70 m of open ground, deliberately empty**
- **rear cottage**: `t 19.00 → 29.974`, full lot width

**Heights**, above the front block's own ground:

| | Crest | Roof deck | LiDAR σ / cells |
|---|---|---|---|
| front flats | **12.07 m** | 11.77 m | 0.36 m over 234 cells |
| rear cottage | 8.75 m | 8.40 m | 0.27 m over 241 cells |

The 12.07 m crest is corroborated by a second, unrelated method: measured off the
2021 drone frame at 76.2 px/m, the plinth reads 2.06 m and the three residential
floors 3.28 m each, totalling 12.08 m to the top of the cornice band.

**Anchor** — `-122.3946173, 37.7815393`, the XY bounding-box centre of the built
form. It lands **in the courtyard**, with no geometry within 4.4 m in either
direction. That is correct: the loader centres the GLB's bounding box on the anchor,
and anchoring on either block would put the other one 19 m off its surveyed
position. The DataSF assessor point for the parcel is 0.3 m away — an independent
check.

**Axis-aligned bounding box** 26.68 × 26.71 × 12.07 m. The XY figures are the
expected consequence of a 45° heading on a 6.7 × 30.0 m lot, not a scale error.

## 4. What each side shows

**South-east (South Park front)** — *observed, one frame*. Bottom to top: an oxblood
painted plinth to 2.10 m carrying, on the **north-east** half, a wide
segmental-arched opening filled with a black metal gate (the carriage passage to the
courtyard, brick reveal at the jambs) and, on the south-west half, a square sash
window; then three residential floors of pale lap siding to 11.77 m; **two projecting
square bays** ~2.8 m wide running all three floors with a ~1.1 m blank recessed stair
strip between them; **butter-yellow trim on every edge** — bay corner boards, window
surrounds, a belt course at each floor line, the cornice band; a **gray shingled
hipped false-mansard hood** across the facade top under the cornice; and a flat
yellow-trimmed cornice band to the 12.07 m crest.

**North-east flank** — party line with 126 South Park (7.3 m), so ~4.8 m stands
clear above the neighbour and is visible from the park and the air. *No source shows
it.* Authored as blank painted siding with a short belt-course return round the
corner, which is what a 1913 party wall over a lower neighbour is. **Inferred.**

**South-west flank** — party line with 136 South Park (3.2 m), so ~8.9 m is exposed.
Same treatment, same confidence. **Inferred.**

**North-west (rear)** — the back of the cottage on the rear lot line. *No source
shows it.* Blank. **Inferred.**

**Courtyard** — *observed, nadir frame*: bare hardstanding with a wooden deck and
external stair against the cottage's south-east face. Dumpsters and a tarped pile
also appear; they are this-week clutter and are excluded by the scope rule.

**Above** — *observed, nadir frame*: light membrane roofs on both volumes, a
skylight and two slim vent stacks on the front block, the shingled hood at the street
edge, nothing on the cottage roof.

## 5. Uncertainties and conflicting evidence

1. **One photograph carries the whole facade.** Colours, bay rhythm, gate and hood
   are all single-source. The massing and heights do not depend on it, so a wrong
   colour is a repaint, not a rebuild.
2. **Nothing shows the flanks or the rear.** Everything there is inferred and is
   deliberately blank rather than speculatively fenestrated.
3. **5 units (assessor, unchanged since 2007) vs 7 (2021 listing).** Probably
   unpermitted or unreported units, quite possibly in the cottage. No effect on
   geometry.
4. **A 0.48 m ground difference between the two LiDAR footprints** (8.98 m vs 8.50 m
   NAVD88) that comes from two different source tiles (`Sanfran_Orig_1384.flt` and
   `_1380.flt`). South Park is flat; this is read as a seam, and both volumes are
   modelled on one datum. See `REPORT.md` §3.
5. **No architect and no historic designation were found.** South Park has obvious
   historic interest and several neighbours are named contributors; nothing was
   confirmed for lot 062, so nothing is asserted.
6. **OSM has nothing here.** The footprint is a reconstruction from the surveyed
   parcel plus the LiDAR polygons plus a 1.1 m registration correction — defensible,
   because party-wall-to-party-wall on a 22 ft SF lot is not a guess, but a
   reconstruction. A source showing a real setback or light well would win.

## 6. Recognition cues, ranked

1. Twin bays outlined in butter-yellow trim over pale siding — the only painted wood
   front on this arc of the oval.
2. The two-volume lot: flats, open courtyard, cottage. The only reading available
   from directly overhead.
3. The oxblood plinth with the black arched carriage gate punched through it.
4. The height step — 12.07 m between a 7.3 m neighbour and a 3.2 m one.
5. The shingled hipped hood under the cornice.

## 7. Preserve / simplify

**Preserve:** the open courtyard as a genuine void; the bay/strip/bay rhythm; the
continuous yellow trim grid; the plinth-not-a-storey proportion of the base; the
segmental arch; the cornice ring reading from above.

**Simplify:** no shingle texture on the hood (one hipped solid); no glazing bars or
sills beyond the trim; no lap-siding relief; the external stair reduced to a deck
and a short run; the cottage to a plain box with punched openings.
