# 1 South Park — build report

Asset: `artifacts/1-south-park/1-south-park.glb` — a miniature of **One South Park**,
the 1919–20 concrete tobacco warehouse at the east end of the South Park oval,
converted 2004–07 to 35 lofts with a two-storey set-back penthouse.

Built 18 August 2026 from `docs/asset-plans/1-south-park.md` and the dossier in
`REFERENCE.md`. **REPORT beats plan**: where this file and the plan disagree, this file
records what shipped.

| | |
|---|---|
| Triangles | **18,938** (cap 20,000) |
| Objects | 402 |
| Dimensions | **58.92 × 54.91 × 20.20 m** |
| min Z | 0.000 |
| XY centre offset | 0.000, 0.000 |
| Crest | **20.200 m** — `targetHeightM / measuredHeight` = **1.000** |
| Anchor (shipped) | `-122.3928634, 37.7820480` |
| Materials | 11, all `Toy_*`; 2 `_Glow` |
| Validation | `validation.json` — **all checks PASS** |

The axis-aligned XY box is 58.9 × 54.9 m even though the longest side of the building
is 43.2 m. That is the ~45° real-world heading, not a scale error.

## 1. What was verified before modelling, and what it changed

The plan was re-verified rather than trusted. Three things were confirmed and none
moved:

- **The storey structure.** Permit PA #200405194312 (2004-05-19) reads "renovation of
  (e) **3 story** concrete warehouse. **add 2 more stories**. adding 35 residential
  units, off street park…", existing 3 → proposed 5. The assessor's 36 condo lots on
  block 3775 number 101–103 / 201–211 / 301–311 / 401–411, of which eight 4xx lots are
  two-storey: 2 + 11 + 11 + 11 = **35 units**, the developer's own figure. Three
  storeys of arcaded wall with a two-level penthouse behind the cornice is therefore
  measured, not inferred.
- **The re-entrant step.** Predicted from the OSM ring at equirect columns 254 and 341
  of pano `Bm7I6a4Jcm8yGuvM9xB_Iw`, the 5.1 m return wall appears there flat-on with
  one arch in it. Modelled as measured.
- **The two-level roof.** The DataSF LiDAR summary is bimodal (mean 17.21 < median
  17.77 < mode 18.76, σ 1.80). Solving the two-level mixture at the satellite-measured
  bright fraction f = 0.62 gives H = 18.6 m and L = 14.9 m. Independently, the
  rectified Street View elevation puts the cornice crest at 15.75 m with the deck just
  below it. The two were not tuned to each other. See `REFERENCE.md` §3.

## 2. Departures from the plan

1. **Penthouse setbacks.** The plan proposed 12.0 m (north-west) and 11.0 m
   (south-west), which produced a penthouse covering only **40%** of the plan against
   the ~60% the satellite segmentation measures. Shipped values are **9.5 m** and
   **8.5 m**, giving **48% gross** (755 m²) — still under the segmentation figure,
   because that segmentation cannot separate bright roof membrane from bright terrace
   pavers and is an upper bound. The terraces remain generous at 9.5 m and 8.5 m.
2. **The cornice is a full closed ring.** The plan called for the moulding on the hero
   faces only. The real party walls carry a plain parapet, but a cornice that stops
   dead at a corner reads as a modelling error from the app's aerial camera, which is
   the view this building is judged from first. The string course *is* hero-faces-only,
   as planned — it is a street feature and 1.5 m of it at a party-wall corner would
   never be seen.
3. **Bevels are on the massing only.** The first build beveled everything and came out
   at **67,890 triangles** — 3.4× the budget. Every arch ring, glazing plate, surround
   and mullion is a thin slab whose bevel triples its triangle count for an edge
   softening nobody can see at a 4 m bay pitch. Restricting the bevel to the massing,
   and dropping `ARCH_SEGS` from 7 to 5 and `MED_SEGS` from 12 to 10, brought it to
   15,522 before the roof was finished, 18,938 shipped.
4. **The lawn moved inboard** from d 1.8–8.4 m to 2.6–7.4 m on the north-west terrace:
   at the planned position it interpenetrated the hedge row and the coplanar faces
   z-fought into a black patch on the aerial render.

## 3. Three bugs worth recording, because each has a general form

**A prism of an OUTSET polygon is a slab, not a ring.** The cornice was first built as
`prism(inset_polygon(FOOTPRINT, -0.28), 14.55, 15.20)` and
`prism(inset_polygon(FOOTPRINT, -0.46), 15.20, 15.75)`. Offsetting a polygon outward
and extruding it fills the whole plan: the two "cornices" were solid slabs that buried
the entire roof design — penthouse, terraces, light court and all — under a featureless
15.75 m plateau. It looked plausible in the aerial (a big flat roof is a normal thing)
and was only caught from the top view. The same mistake then reappeared on the
penthouse coping, where a slab coincident with the penthouse roof z-fought into a moiré
across the whole top. Both are now `ring()`, which builds the band between a polygon and
its inward offset. **If a band is wanted, build a band.**

**Geometry behind the wall face is invisible by day.** The body is a solid prism with no
real openings, so the first pass's glazing — arcade glass at d −0.09…−0.02 and upper
windows at −0.14…−0.05, both entirely inside the wall — showed nothing at all. What
made it hard to see was that the *lit* windows looked fine: their `_Glow` plates stood
0.02 m proud, so roughly two thirds of the openings had glass and one third were blank
wall, which reads as a modelling glitch rather than a systematic error. All glazing now
reaches the wall face (+0.015 to +0.025 m) and the openings read as recessed because
the white archivolts and surrounds stand 0.07–0.11 m proud of them instead.

**A glow plate on a tiled seam is buried.** The light court is a real hole, tiled around
rather than booleaned, so the penthouse is three pieces whose adjoining edges face each
other. A `_Glow` band laid on every edge put one plate on a seam, where it is invisible
and where the validator's ray test — each glow face must be the first thing hit from
outside — correctly failed it, 117 of 118. `glow_seg()` now probes 1.2 m along its own
outward normal and skips the segment if that point falls inside another piece.

## 4. The light court is a real cut

`docs/styles/miniature-toy.md` is explicit that the roof is an elevation, and from the
app's aerial camera a painted dark rectangle reads as a stain, not a court. There is no
boolean anywhere in this model, so `poly_minus_slot()` tiles the footprint into up to
four simple pieces around the slot, and the body is split at the court floor (9.40 m,
LiDAR `hgt_min`) so the hole goes through the deck as well as the penthouse. Each piece
stays a closed prism, so the validator's per-object signed-volume test needs no special
case; the pieces share internal faces at their joints, which are buried between two
solids. Court, penthouse and deck all come from the same slot definition, so they cannot
drift apart.

## 5. Palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_dove` | `c9cecd` | body — all three storeys of wall on all six faces, plinth, piers, parapet |
| `Toy_white` | `f7f4ec` | cornice, string course, archivolts, medallions, window surrounds, copings |
| `Toy_slate` | `6f7883` | penthouse and stair/lift overrun |
| `Toy_ink` | `3a3530` | arch reveals, roller-shutter and entrance bays, mullions, mechanical, pergolas, court floor |
| `Toy_glass` | `2a4d73` | upper-storey glazing and the penthouse band |
| `Toy_glassl` | `6f95b8` | arcade fanlights |
| `Toy_steel` | `9aa0a6` | roof membrane, penthouse roof, deck, vents |
| `Toy_rust` | `a86444` | roof-terrace timber decking |
| `Toy_verdigris` | `9fb8a8` | hedges, planters, lawn, court planting |
| `Toy_mustard_Glow` | `d9a441` | the arcade at night — hero glow |
| `Toy_glassl_Glow` | `6f95b8` | lit flats and the penthouse band |

`Toy_dove` is **off-palette** — a WARN in `sf-asset-check`, not a fail, and deliberate.
Both party-wall neighbours (`21-south-park`, `300-brannan`) are `Toy_stone` bodies, and
three adjacent stone blocks on one corner merge into one beige mass from the aerial
camera; this building's paint is measurably cooler and lighter than either. It was set
one step darker than the first pass's `d4d6d4`, because at a half-step separation the
`Toy_white` cornice, string course and medallions read as more wall rather than as trim.

`Toy_roofd` (45454a) was **rejected** for the penthouse: it renders as rgb(9,9,12) under
the app's lighting, and the penthouse is this model's second-largest visible mass — it
has to read as a dark grey, not a hole. `Toy_slate` is precedented by `300-brannan`,
the neighbour across the south-east party wall.

## 6. Night state

The hero is the **arcade** — a continuous warm ribbon at eye level round both street
elevations, which is what this building actually does at night behind 24 glazed arches
of retail and lobby. Supporting it: an uneven scatter of **64% of the 48 upper windows**
(35 flats, not an office floor, so the scatter is deterministic pseudo-random rather
than a pattern) and one quiet cool band on the penthouse.

The arcade glow plate is deliberately **smaller than its opening** (0.72 × the arch
width, from 1.60 m to 5.25 m). The app draws `_Glow` at `0.12 + 0.95·uNight`, so a plate
that fills the arch tints the whole arcade brown by day; the first pass did exactly
that. Keeping a margin of unlit `Toy_glass` around it leaves the day read cool and still
gives night a continuous ribbon.

Every glow surface is an **open single-layer plate** standing proud of the opaque
glazing, never a closed shell — a shell is two alpha layers deep and reads at roughly
twice the intended day alpha. `validation.json` confirms 116 of 116 glow faces are the
first surface hit from outside along their own normal.

## 7. Orientation

Authored in world space: Blender `+Y` = true north, `+X` = east, so the loader applies
no rotation. The contract's "front faces −Y" cannot be honoured literally — the block
stands at ~45° to the world axes and real-world orientation wins (`AGENTS.md` rule 5).
Measured outward normals as built:

```
SE party (300 Brannan)      37.78 m   135.42°
NE Second Street (south)    28.20 m    45.28°
NE step return               5.10 m   315.10°
NE Second Street (north)    15.29 m    44.60°
NW South Park               33.00 m   315.04°
SW party (17-19 South Park) 43.24 m   224.61°
```

## 8. Draft manifest entry

```json
{
  "id": "1-south-park",
  "file": "1-south-park.glb",
  "anchor": [-122.3928634, 37.7820480],
  "targetHeightM": 20.2,
  "cat": 2,
  "name": "One South Park (1 South Park)",
  "estimated": false,
  "dims": [58.92, 54.91, 20.2],
  "tris": 18938,
  "loadRadius": 2500
}
```

## 9. Approval

_Pending — stage 3._
