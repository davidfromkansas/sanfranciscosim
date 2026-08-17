# 104–106 South Park (Gran Oriente Filipino Hotel) — build report

**REPORT beats plan.** Where this file and
[`docs/asset-plans/106-south-park.md`](../../docs/asset-plans/106-south-park.md)
disagree, this file is what was built and why.

| | |
|---|---|
| Asset | `106-south-park.glb` |
| Build | `blender -b --python build_106_south_park.py` (deterministic, Blender 5.2.0 LTS) |
| Renders | `blender -b --python render_106_south_park.py` and `-- --night`; `python3 make_contact_sheet.py` |
| Validation | `blender -b --python validate_106_south_park.py` → `validation.json` |
| Triangles | **3,920** against a 7,000 cap |
| Objects | 73 |
| Dimensions | 26.373 × 26.368 × **11.580** m (the XY box is the exact 45° rotation of a 7.32 × 29.72 m sliver) |
| min Z / XY centre | 0.000 m / (0.000, 0.000) |
| Materials | 10, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| Glow | `Toy_glassl_Glow` (four upper street windows), `Toy_trim_Glow` (entry soffit) |
| Manifest anchor | `-122.3944099, 37.7817221` |
| Street facade heading | 135.00° true; long axis 315.00°; south-west flank 225.00° |
| Overall | **PASS** — every contract check in `validation.json` |

## Dossier corrections and design reversals

### 1. The palette keys in the plan's 2.8 do not exist — three materials changed

`Toy_bone` and `Toy_wood` are not in the `sf-asset-check` palette. The built asset
uses `Toy_cream` (`f2ede3`) for the upper stucco and, after the reversal below,
`Toy_sand` (`ece4d4`) for the flank boarding. The plan's 2.8 has been amended to
match.

### 2. The exposed south-west flank is NOT a warm accent — reversed after review

The plan made the exposed strip above 108–110's roof `Toy_rust` and said in terms:
"the one warm accent … do not neutralise it into the body colour". The first aerial
review killed that on two grounds:

- **It looked wrong.** A saturated 29.7 m band along an otherwise blank wall read
  as a painted racing stripe and dominated the entire model from the app's camera
  angle. It was the loudest thing about a background building.
- **It is probably factually wrong.** The nomination's "horizontal wood boards" is
  a 2019 observation. The 2020–21 rehabilitation repainted the building, and the
  January 2025 Street View pano shows pale wall above 108–110's roofline, no brown.

The strip is now `Toy_sand` — a hair warmer and darker than the body — with three
shallow `Toy_steel` shadow grooves to say "horizontal boards, not stucco". The
stepped-silhouette cue it was supposed to carry does not need a stripe: in the
baked city the shorter neighbour supplies the step for free.

### 3. The roof membrane is pale, not charcoal

The plan gave the roof deck `Toy_roofd` (`45454a`). The Bing/Maxar aerial masked to
this footprint (`REFERENCE.md` §5) shows a **pale cool-roof membrane**, which is
what the 2020–21 rehabilitation would have installed and is also what makes the
dark PV array and the raised skylights read from above. The deck is now
`Toy_stone` (`d9d2c2`); `Toy_roofd` is kept for the Taber Place rear face, where
the dark value is both accurate and the intended break from the pale street front.

### 4. The PV question is closed: PV is present

The plan (2.9) left this open and explicitly forbade inventing a token array. It
was settled by masking a Bing/Maxar z20 mosaic to the DataSF footprint — see
`REFERENCE.md` §5. Three array blocks are modelled over the north-east half of the
rear two thirds, with two light rails each so the array reads as panels rather
than a black slab, plus the three large skylights along the south-west edge and
mechanical plant at the street end.

### 5. Rooftop plant is capped at 0.50 m so the cornice stays the crest

The first build put the mechanical block at deck + 0.75 m, which made the bbox top
11.77 m and would have made the loader scale the whole building down by 1.6%.
Nothing on this roof is documented above the cornice — the LiDAR maximum that
might suggest otherwise is the neighbour, see 6 — so plant is capped below the
crest. That is a conservative reading, not a convenience.

### 6. The LiDAR maximum is the neighbour, confirmed

`hgt_max` for SF3775058 is 13.50 m against a median of 11.02 m and σ 0.67 — a 3.7σ
outlier — on a footprint sharing a party wall with 102 South Park, whose own LiDAR
median is 12.88 m and maximum 15.20 m. This is the Earl Warren party-wall failure
mode. The nomination describes the roof in detail and records no bulkhead or
penthouse. **There is no penthouse; the crest is the published 38 ft.**

### 7. OSM `height=11` agrees with the LiDAR deck and is still not the target

11 m vs a LiDAR roof-deck median of 11.02 m looks like corroboration. Both are
measuring the roof membrane behind the parapet. The target is the cornice crest at
11.58 m.

## Iteration log

| Pass | Problem found | Fix |
|---|---|---|
| 1 | Bounding-box top 11.77 m, not 11.58 | Rooftop plant capped at deck + 0.50 m |
| 1 | `PERP` was derived as `AXIS − 90°`, which points **south-west**, mirroring the whole building: the vestibule landed at the north-east end, the skylights on the north-east edge and the boarded strip on the wrong party wall | `AXIS + 90°`; verified by the reported face headings (front 135°, rear 315°, south-west flank 225°) |
| 2 | The ground-floor band was one solid slab spanning the frontage, so the vestibule recess and the shopfront glass were buried **inside** it and the ground floor rendered as a blank gray panel | Rebuilt as three piers + a bulkhead + a shopfront lintel + a vestibule lintel, leaving real openings |
| 2 | Flank strip read as a racing stripe | Reversal 2 above |
| 2 | Roof deck too dark against the aerial evidence | Reversal 3 above |
| 3 | Shopfront glass still invisible — recessed entirely behind the wall plane | Glass and mullions now poke 0.02–0.035 m proud of the wall so they sit *behind the proud piers* and read as recessed |
| 4 | Rear elevation rendered as six sills and no windows: the fills were buried inside the 0.04 m asbestos-shingle cladding slab | `window()` grew a `wall_d` argument; rear fills, sills and the service door now measure from the cladding face |
| 4 | Fire escape was on the two **south-west** bays | The rear face frame runs t=0 at the north-east party wall, so the nomination's "two eastern bays" are the first two: `FE_T0/T1` moved to 1.45–4.05 |
| 5 | Night: the entry accent was invisible — a glow shell on the back wall of a 1.10 m deep recess is hidden by its own reveals from every angle the app's camera can reach (the same failure 165 South Park logged with its gate) | Moved to a soffit band just inside the head of the opening |
| 5 | Night: lit windows blew to flat white at the 165 South Park emission of 6.0 | Render preview emission reduced to 3.2 |

## Style notes

- **The removed ornament is the trap on this building and it was avoided
  deliberately.** The 1996 elevation photograph is the only clear, complete,
  square-on record of the street front, and it shows painted Corinthian columns and
  trompe-l'œil pediment lintels that were removed after 2020. The model carries a
  plain three-bay grid, which is the 2026 building.
- **Detail budget:** background building (style bible §21). The budget went to six
  things and nothing else — the bay grid, the cornice and dentil course, the sign
  band, the two-part ground floor, the exposed flank strip, and the roof.
- **Renders:** the four cardinal elevations are aligned to the *building's* axes,
  not to true compass directions, because it stands at exactly 45°; each keeps its
  nearest compass filename (`-south` = street, `-north` = Taber Place, `-west` =
  the 108–110 flank, `-east` = the blind 102 flank). `-facade.png` is an extra
  square-on long-lens view of the 135° street front, because none of the four
  cardinal views takes the public face head-on.
- **Night state:** four of six upper street windows lit, unevenly — 24 studios of
  affordable housing on a quiet oval, not an office — plus the entry soffit. The
  shopfront, the rear, the skylights and the roof do not glow.

## Approval

> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

— David, 16 August 2026, standing approval given with the pipeline invocation.
Stage 3 recorded as approved on that instruction; the contact sheet, the aerial day
and night renders and the numbers above are the evidence presented.

## Draft manifest entry

```json
{
  "id": "106-south-park",
  "file": "106-south-park.glb",
  "anchor": [
    -122.3944099,
    37.7817221
  ],
  "targetHeightM": 11.58,
  "cat": 2,
  "name": "Gran Oriente Filipino Hotel (104–106 South Park)",
  "estimated": false,
  "dims": [
    26.3728,
    26.3678,
    11.58
  ],
  "tris": 3920,
  "loadRadius": 2500
}
```

`"estimated": false` — the 38 ft crest is published in the National Register
nomination and independently corroborated by the LiDAR roof deck plus a plausible
cornice.
