# 155 – 157 South Park Street — reference dossier

Compiled 12–13 August 2026 for the SF-SIM miniature GLB, from the sources in §2.
Everything here was re-verified during the build; where this file and
`docs/asset-plans/155-south-park.md` disagree, **this file is correct**.

## 1. What the building is

A two-unit residential **flats** building of 1925 on the south-east side of the
South Park oval in SoMa, San Francisco. Three levels: a ground floor built as a
garage and long since converted to commercial space (a café), and two residential
flats above it. Wood frame, smooth stucco, flat front, flat roof.

It is a **contributor** to the potential South Park Historic District (CHRSC status
code `5D3`), one of the ten contributing residential flats buildings that give the
oval its scale. It sits on a **through lot** running the full 31 m from South Park
Street to the Varney Place alley, with party walls on both long sides.

Assessor / OSM identity: APN **3775-030**, OSM way **124889488**,
`addr:housenumber = 155;157`, `addr:street = South Park`, DataSF LiDAR footprint
`mblr = SF3775030`.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| SF Planning / Page & Turnbull, *South Park Historic District*, DPR 523D continuation sheets, 30 June 2009 (`https://default.sfplanning.org/GIS/SouthSoMa/Docs/2009-06-30_South%20Park%20Dform.pdf`) | 1925 date; contributor status `5D3`; property type "HP3. Multiple Family Property; HP6. 1-3 Story Commercial Building"; the flats typology on the oval; and the explicit statement that **this building's ground-floor garage was converted to commercial space while the upper floors remained residential** |
| DataSF Building Footprints, LiDAR-derived (`https://data.sfgov.org/resource/ynuv-fyni`) | the authoritative footprint polygon (209.3 m2) and the height statistics: modal cell 9.25 m, median 8.87 m, mean 8.62 m, max 16.23 m, ground 8.23 m NAVD88 |
| SF Assessor Historical Secured Property Tax Rolls (`https://data.sfgov.org/resource/wv5m-vpq2`) | 1925; block 3775 lot 030; 2 storeys; 2 units; 2,350 sq ft over a 2,443 sq ft lot; construction type `D` (wood frame); zoning `SPD` |
| SF Registered Business Locations (`https://data.sfgov.org/resource/g8m3-pdis`) | the current ground-floor tenant, Flour & Branch, registered 17 Feb 2026 at "155 South Park St **Bldg A**" — the "Bldg A" suffix independently confirms more than one structure on the lot |
| OSM way/124889488 | cross-check footprint (206.6 m2, within 1.3% of DataSF); `height = 9` |
| Google Street View, South Park Street pano, captured Jan 2025 | the entire front elevation in detail (see §4) |
| Google Street View, Varney Place pano, captured Jan 2025 | the alley and the rears of the row (see §4) |
| Google Maps satellite, Vexcel imagery 2026 | flat roofs, the step down from front block to rear block, the rear roof deck and its screen |
| Press coverage of the ground-floor tenancies | the café lineage: The Butler & The Chef Bistro at 155A until end of 2017, then The Velvet Raven (signage in place Jan 2025), then Flour & Branch |

## 3. Verified dimensions, location and orientation

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.3942202, 37.7808993` | **measured** — OBB centre of the DataSF footprint |
| Footprint area | 209.3 m2 | **measured** |
| Overall OBB | 8.16 x 31.22 m at 41.4° off the world axes | **measured** |
| Front block | ~6.2 m wide x 12.6 m deep | **measured** |
| Rear block | ~8.2 m wide x 18.6 m deep | **measured** |
| Front roof deck | 9.25 m above grade | **measured** — LiDAR modal height cell (`hgt_majoritycm = 925`) |
| Front parapet crest | **10.10 m** | *inferred* — deck + 0.85 m, read from the frontage photograph |
| Rear block roof deck | 7.00 m | *inferred* — Varney Place photograph |
| Ground elevation | 8.23 m NAVD88 | measured; the app's terrain handles this, not the asset |
| Street frontage heading | faces **327.2° (NNW)** | **measured** from the footprint |
| Party walls | run 140.8° / 320.8° | **measured** |
| Frontage skew | ~6° off the party walls, because South Park Street curves around the oval | **measured** |

Measured footprint in the lot's own frame (metres, `+u` = north-east across the
lot, `+v` = north-west toward the street, origin at the anchor), rounded to the
survey:

```
front block   (-2.30, 2.95) (3.80, 2.95) (4.06, 14.68) (-2.10, 15.61)
rear block    (-2.94, -15.61) (4.08, -15.08) (4.08, 2.95) (-4.08, 2.95)
```

World coordinates follow from `(E, N) = (u cos41.4° − v sin41.4°, u sin41.4° + v cos41.4°)`.
Spot-checked against the DataSF ring: survey vertex 13 → `(−11.898, 10.320)`,
vertex 5 → `(13.033, −8.614)`, both exact.

## 4. Observations from all four sides and above

**North-north-west — South Park Street (the hero elevation).** Three levels. A
plain coped parapet with a slightly raised centre bay. Below it, smooth bright
white / off-white stucco carrying two **sage-green (celadon) window groups**, one
per floor: a wide fixed centre light flanked by two narrow double-hung sashes, in
thick painted trim with a shallow sill apron. A pair of **cast-plaster diamond /
lozenge rosettes** sits in the stucco either side of the second-floor group. Below a
horizontal break, the ground floor is a **near-black painted timber shopfront** with
fine copper pinstripe lines outlining its panels, a black fabric awning across the
full width, a recessed centre entrance with pale curtained double doors and brass
hardware under a transom, a display window to the left of the entrance and a smaller
one to the right, and at the far north-east end a tall **black wrought-iron security
gate** over the passage to the flats, carrying the "155 / 157" address plate. The
"155A" number is at the south-west end. A downpipe and a run of ivy sit at the
south-west edge.

**South-south-east — Varney Place (the rear).** Two storeys of salmon / peach
painted stucco, blunt and utilitarian: a pair of white roll-up garage doors at
alley level with a painted pilaster strip between them, small windows above, and a
**diagonal-lattice screen** enclosing a roof deck above the parapet. Varney Place is
about 5 m wide, so this face is only ever seen at an extreme oblique in the real
world — but the app's aerial camera reads it plainly.

**North-east and south-west — party walls.** Blank stucco against 147 South Park
(a modern replacement building; its own rear on Varney Place is the blue
corrugated-metal 62 Varney Pl) and 159 South Park (1907 industrial,
non-contributing). The survey shows one sub-2 m light-well notch in each party
wall. Nothing else.

**Top.** Two flat roofs at different heights: the front block's plain membrane roof
inside its parapet ring at 9.25 m, then a step down to the rear block at 7.00 m,
part of which is a timber roof deck behind the screen, with a stair bulkhead, a
skylight and a scatter of vents.

## 5. The five strongest recognition cues, ranked

1. **A near-black shopfront under a bright white box.** The value contrast is the
   entire silhouette at diorama scale, and no neighbour on the oval has it.
2. Tall, narrow, flat-fronted three-level stucco block on a very deep lot.
3. The two **sage-green window groups**, thick-trimmed, one per upper floor.
4. The **pair of plaster lozenges** flanking the second-floor window.
5. The step down to a lower salmon rear block with an alley garage and a roof deck.

## 6. Preserved / simplified

**Preserved:** three levels with a clearly taller ground floor; the white body over
black base split carried to both party-wall corners; the sage-green window colour;
the two-block through-lot massing at its real 41.4° heading; the ~6° skewed
frontage; the raised centre parapet bay.

**Simplified:** each window group is one frame panel with three light fills rather
than three separate openings; the lozenges are enlarged to 0.80 m and given 0.12 m
relief; the shopfront reduces to awning, gate, two windows and a recessed entrance;
the copper pinstriping survives only as a single trim line along the awning fascia;
ivy, downpipe, signage lettering and the address plate are dropped; the diagonal
lattice becomes a plain screen wall; the two survey light-well notches are dropped
(invisible between party walls, and the triangles are better spent on the windows).

## 7. Uncertainties and conflicting evidence

- **Storey count.** Assessor says 2, photographs show 3. Resolved: the assessor
  counts dwelling floors and not the converted ground-floor garage. **Built as 3
  levels.** The DPR form's Integrity section is the evidence that settles it.
- **The assessor's 2,350 sq ft is not the whole mass.** 218 m2 of floor area
  against a 209 m2 footprint is less than one full floor over the through lot,
  which cannot describe a three-level front block. It describes the flats; the rear
  block and the ground-floor commercial space are recorded separately, which is the
  same signal as the business registration's "Bldg A". Not used for anything.
- **OSM `height = 9` and the LiDAR median 8.87 m both describe the roof deck**, not
  the crest, and they are close enough to each other to look like corroboration.
  They are not. The modal LiDAR cell, 9.25 m, is the better deck figure and the
  parapet stands above it.
- **The parapet crest (10.10 m) is the weakest number in this dossier.** Roof deck
  measured, parapet height read off one street-level photograph. So is the raised
  centre bay.
- **The rear block was identified by elimination** along Varney Place: the blue
  corrugated building at 62 Varney Pl is the rear of the modern 147 South Park,
  which puts the salmon-stucco rear with the garage doors and the screened deck on
  lot 030. That inference is sound but it is an inference, and the 7.00 m height is
  a visual estimate.
- **No architect or builder is recorded** for the 1925 building in the DPR form or
  in any other source consulted, although several other South Park buildings in the
  same document do name theirs.
