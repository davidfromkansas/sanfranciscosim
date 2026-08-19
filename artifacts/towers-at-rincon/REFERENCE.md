# The Towers at Rincon (88 Howard Street) — reference dossier

Research behind `towers-at-rincon.glb`. Compiled 18 August 2026. Everything below is
either **measured** (from a named dataset, with the query recorded), **published**
(with the source), or **observed** (from imagery, and labelled as such). Anything
else is marked *inferred*.

The asset covers the **residential half of Rincon Center only** — the 1988–89 block
at 88 Howard Street. The 1940 Rincon Annex post office on the north-west half of the
same city block is a separate DataSF footprint and is deliberately out of scope.

---

## 1. Identity

| Item | Value | Source |
|---|---|---|
| Name | The Towers at Rincon; CTBUH "Rincon Center East / West Tower"; historically "Two Rincon Center" | CTBUH, owner sites |
| Address | 88 Howard Street, San Francisco, CA 94105 | OSM node 2038804804; CTBUH; Tidewater Capital |
| Complex | Rincon Center, phase two | Wikipedia |
| Architect | Scott Johnson, Pereira Associates (Johnson Fain) | Wikipedia; rinconcenter.wordpress.com |
| Completed | 1988 (podium/offices), 1989 (residences) | Wikipedia; CTBUH gives 1989 |
| Use | 320 market-rate flats (160 per tower) over six floors of office and ground-floor retail | CTBUH; RentCafe; Tidewater Capital |
| Neighbourhood | Transbay / East Cut, one block from the Embarcadero | OSM |

## 2. Heights — measured, then cross-checked

**DataSF Building Footprints** (`ynuv-fyni`), record `sf16_bldgid 201006.0000265`,
`mblr SF3716021`, LiDAR statistics over 20,136 half-metre cells:

```
hgt_maxcm    8713      -> 87.13 m above ground   (the crest)
hgt_mediancm 2495      -> 24.95 m                (the podium roof)
hgt_majoritycm 2421    -> 24.21 m                (mode: the podium roof again)
hgt_meancm   3828.98   -> 38.29 m
hgt_stdcm    2592.61   -> 25.93 m                (bimodal, by inspection)
gnd_min_m    3.36      peak_1st_m 90.63          (90.63 - 3.36 = 87.27 m AGL)
```

The distribution is bimodal — a podium and two towers — so the two levels can be
solved for rather than guessed. With `H = 87.0`:

```
f*H + (1-f)*L = 38.29        f(1-f)(H-L)^2 = 25.93^2 = 672.2
  => L = 24.49 m   f = 0.221
```

A six-storey podium at **24.49 m** and a tower crest at **87.0 m** fall straight out
of the raw statistics, and both agree with the published figures. (`f` = 0.221 of the
plan is the tall part; the two OSM tower footprints are 0.33 of the plan, the gap
being intermediate roof levels the two-level model cannot see. `f` corroborates *H*
and *L*, it does not measure plan area.)

**Published:** CTBUH lists both towers at **89 m / 292 ft**, architectural *and* to
tip, 22 floors above ground, 2 below.

**Decision.** `targetHeightM = 89.00 m`. The LiDAR crest of 87.13–87.27 m is the
solid arched penthouse roof, which is what LiDAR returns; the remaining ~1.8 m is
the mast, which it does not. The model therefore puts the **arch apex at 87.20 m**
and the **mast tip at exactly 89.00 m**, so the loader's
`targetHeightM / measuredHeight` lands on 1.000.

**Rejected:** OSM way/32862406 tags `height=93` and `building:levels=24`. That is
5.9 m above the LiDAR crest and 4 m above CTBUH, and OSM is not a height authority
here. Not used.

**Storeys.** CTBUH says 22 above ground per tower; Wikipedia and the owner say 23.
The model reproduces the measured heights with 6 podium storeys (ground 5.00 m + five
at 3.90 m = 24.50 m) and 16 residential floors at 3.20 m to the shoulder cornice at
75.70 m, plus 2.5 more in the central bay. That is 24 levels of structure; the height
is measured, so the storey label is a naming question, not a geometry one.

## 3. Footprint, orientation and anchor

Measured from `buildings_datasf.geojson` (the same file `pipeline/buildings.mjs`
bakes from), in the project's tangent projection:

- area **5,008 m²**; axis-aligned box **112.29 × 112.60 m**; oriented box
  **89.24 × 76.04 m at −44.68°**
- the block is a **diamond** with corners pointing roughly N, E, S, W:
  E `(56.14, 1.75)`, N `(7.02, 56.30)`, W `(−56.14, −6.64)`, S `(−1.80, −56.30)`
  in metres east/north of the anchor
- it is a **C, not a diamond**: a wedge-shaped courtyard is cut into the north-west
  side, ~45 m deep, narrowing to the south-east

Street sides, measured by nearest-segment distance from `streets_datasf.geojson` to
probes 55 m off the block centre on each diagonal:

| Face | Street | Distance to centreline |
|---|---|---|
| South-east | **Howard Street** (the address; main entrance) | 8.2 m |
| North-east | **Steuart Street** | 1.6 m |
| South-west | **Spear Street** | 0.5 m |
| North-west | *no street* — party line with the Rincon Annex | (nearest street 53.5 m) |

**Anchor `-122.3924907, 37.7919910`** — the AABB centre of the DataSF footprint,
adjusted by the 0.30 m / 0.16 m shift the build script's `recentre()` applied to put
the model's own XY bbox centre on the origin. Authored +Y = true north; the loader
applies no rotation.

## 4. The courtyard — a dossier correction

`docs/asset-plans/towers-at-rincon.md` §2.4/§2.9 placed the circular plaza and its
planting on the **podium roof** in the north-west quadrant, reading the owner's
"7th-floor outdoor resident lounge" as the whole story.

That is wrong, and the DataSF footprint says so on its own: the ring is a C, so
whatever is in that wedge returned **ground**, not a roof at 24.5 m. Google satellite
imagery at z21 confirms it — an open-air paved court with a circular plaza,
radial paving, curved stepped planting terraces with a stair, café seating under
umbrellas, and a glazed canopy over its narrow south-east end. This is the
"ground floor promenade … and a central garden courtyard" the *Los Angeles Times*
described on 16 October 1988. The model builds it at grade. See REPORT.md 1.

## 5. What each side shows (observed)

**South-east, Howard Street** — the address elevation. A dark charcoal shopfront band
behind a colonnade of square piers, then five bands of pale warm-grey precast
alternating with dark ribbon glazing. The wall does not run straight: it steps in and
out in a shallow sawtooth (visible in the DataSF ring as well as in imagery). Near
the Steuart end, a glazed pyramid entrance canopy and, above it, a monumental
semicircular arched window. The west tower stands behind.

**North-east, Steuart Street** — the same podium language; the east tower stands
directly over this frontage and reads full height from the street. The Dec 2022
street-level photosphere at 37.7916, −122.3921 shows the entrance canopy, the
"88 — THE TOWERS AT RINCON" signage band, and the arcade.

**South-west, Spear Street** — the west tower's bow and its rounded west end.

**North-west** — party line with the 29.7 m Annex, plus the mouth of the courtyard.
Plain; kept simple in the model but not blank.

**Top** — two tower roofs, each a long lozenge with a mechanical penthouse, the
central bay, the arched cap and the mast; between and around them the podium roof,
and the open courtyard.

## 6. The towers

OSM carries a `building:part` decomposition of this complex, which is the only
public source that separates the towers from the podium:

- **west tower** — way/944891683, 868 m², `height=93`, `building:levels=24`
- **east tower** — way/944891684, 803 m², same tags
- podium — ways 944891685 / 944891687 / 944891688, `building:levels=6`
- courtyard pergolas — ways 1301393950 / 1301393951, one storey, `height=3`

Each tower is an elongated lozenge, roughly **50 × 26 m**, with the outer long face
convex and the courtyard side a W of two projecting wings. Fitting a circle to the
mapper's outer chain gives a bow of radius **≈32 m** (west, sagitta 13.1 m over a
51.8 m chord) and **≈29 m** (east, sagitta 13.2 m over 48.2 m). The west tower bows
**south** over Howard/Spear; the east tower bows **east** over Steuart.

**Positions are OSM's, shapes are the photographs'.** Google satellite z21 puts both
tower-roof centroids ≈9.5 m north-north-west of the OSM ground plans — 9.5/87 = 0.11,
i.e. a ~6° off-nadir lean over an 87 m building, which is exactly what an oblique
satellite does to a tall roof. The OSM plans are the ground truth for *position*; the
mapper's ten straight segments are not the truth for *shape*, so the outer face is
rebuilt as the bow it is.

## 7. The crown — the identity

From the Wikimedia Commons photograph `Rincon_Towers.jpg` (7628 × 10171, monochrome),
which shows a tower top square-on:

1. the rounded **shoulders** (the lozenge ends) stop at a heavy **rolled bullnose
   cornice** — a thick, pipe-like moulding, the single most identifying detail;
2. a **central bay** continues about 2.5 storeys higher, with its own rolled cornice;
3. above that a **penthouse** with a band of small square windows, capped by a
   shallow **segmental arched (barrel) roof**;
4. a slender **mast** on the apex.

Floor-band spacing measured off that photograph puts the arch apex ~11.5 m above the
shoulder cornice and the central-bay cornice ~8 m above it; scaled to the measured
87.2 m crest that gives a shoulder cornice at ~75.7 m and a bay cornice at ~83.7 m,
which is what the model uses.

The same photograph shows **stacked white balcony slabs** across the bow at every
floor, stopping well short of the rounded ends, and **vertical piers** flanking the
central bay.

## 8. Materials and colour

Two photospheres disagree, and the disagreement is instructive:

- a **rooftop 360° panorama** (37.79131, −122.39289) shot into the sun shows the
  towers as dark blue-grey — shadowed precast plus dark glass reflecting a deep
  blue sky;
- a **street-level 360°** on Steuart in daylight shows the same walls as pale warm
  grey precast with dark grey-green ribbon glazing, white balcony slabs, a charcoal
  base band, and light silver mullions.

The sunlit reading is the material; the backlit one is lighting. The model uses
`Toy_sand` for the precast, `Toy_glass` for the ribbons, `Toy_trim` for the balcony
slabs and cornices, `Toy_ink` for the shopfront band. A marketing photograph of the
23rd-floor deck confirms very dark glass in light silver frames.

## 9. Recognition cues (ranked)

1. Two curvilinear towers on one podium, diagonally opposed, bows stacked with white
   balcony slabs
2. The crown: rolled bullnose cornices, taller central bay, arched penthouse, mast
3. A six-storey banded podium filling a whole diamond block, with a street arcade
4. The open garden courtyard with its circular plaza, cut into the north-west side
5. The glazed pyramid entrance canopy and the big arched window on Howard Street

## 10. Preserved / simplified

**Preserved** — the podium-plus-twin-towers silhouette and their diagonal opposition;
the curvilinear plan; the balcony rhythm; the three-step crown; the whole-block
footprint at true size; the courtyard as a void, not a roof.

**Simplified** — 97 DataSF ring vertices become 58 after per-face Douglas-Peucker at
1.5 m and selective corner cutting; ~20 storeys of curtain wall become 5 podium bands
and 16 tower bands; dozens of balconies become one continuous slab per floor across
the middle half of each bow; the roof mechanical clutter becomes five clean masses,
two solar arrays and two skylight rows.

**Exaggerated** — the rolled cornices (built as two stacked steps so the moulding
reads from the air); the arched cap; the entrance pyramid; the courtyard planting,
which is the model's only saturated colour.

## 11. Sources

- https://www.openstreetmap.org/way/32862406 (+ `building:part` ways above)
- https://www.skyscrapercenter.com/building/rincon-center-east-tower/32367
- https://www.skyscrapercenter.com/building/rincon-center-west-tower/32366
- https://en.wikipedia.org/wiki/Rincon_Center
- https://www.latimes.com/archives/la-xpm-1988-10-16-re-6436-story.html
- https://www.tidewatercap.com/listings/88-howard-san-francisco
- https://www.carmelpartners.com/project/the-towers-at-rincon/
- https://rinconcenter.wordpress.com/about/
- https://commons.wikimedia.org/wiki/File:Rincon_Towers.jpg
- DataSF Building Footprints `ynuv-fyni`, record `201006.0000265`
- DataSF Street Centerlines `3psu-pn9h`
- Google satellite tiles z20/z21 over 37.79195, −122.39246
- Two public Google Maps photospheres near Howard/Steuart (Dec 2022; rooftop)

No copyrighted full-resolution imagery is committed; the URLs and the measurements
taken from them are.

## 12. Uncertainties

- **22 vs 23 storeys** — CTBUH and Wikipedia disagree. Height is measured, so this
  affects only the label.
- **Are the towers identical?** They read as mirrored twins and are modelled as such,
  but OSM's west lozenge is ~4 m longer than the east one, and the model keeps that
  difference.
- **The sawtooth on Howard Street** is taken from the DataSF ring. It is consistent
  with imagery showing projecting and recessed bays, but the exact step depths are
  *inferred*.
- **The courtyard's internal layout** (plaza position, terrace steps, pergola) is read
  off one satellite image and is *observed*, not surveyed.
- **The Rain Column**, Rincon Center's famous water feature, was removed in the early
  2020s and is interior in any case. Not modelled.
