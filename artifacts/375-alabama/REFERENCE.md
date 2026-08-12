# 375 Alabama Street — reference dossier

Research behind `375-alabama.glb`. Compiled 12 August 2026 from the sources below.
Anything not marked **measured** is inference and is called out again in §8.

The building is the **Ames Harris Neville Co. Building** (1926) — a four-storey
reinforced-concrete daylight factory filling the northeast corner of 17th and Alabama in the
Inner Mission, running the full block width east to Florida Street. Ames Harris Neville was a
San Francisco bag and canvas manufacturer; the building later housed Koret of California,
then a City College campus, and is marketed today as "The Koret Building". Its ornament still
carries the original firm's monogram, which is why this dossier uses the historic name.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [SF Planning DPR 523 survey form, APN 3966002](https://sfplanninggis.org/docs/DPRForms/3966002.pdf) — South Mission survey, recorded by Tim Kelley Consulting, 12 Jun 2008 | Historic name **Ames Harris Neville Co.**; 1926; HP8 Industrial Building; "Intensive" survey level; four dated photographs (16 Nov 2007) — `100_5330` view to NE (the 17th/Alabama corner), `100_5325` tower detail, `100_5327` view to W, `100_5328` parapet detail |
| [OSM way 242990064](https://www.openstreetmap.org/way/242990064) | Footprint; `addr:housenumber=375`; `addr:street=Alabama Street`; `height=16` |
| DataSF Building Footprints (LiDAR), `https://data.sfgov.org/resource/ynuv-fyni`, record `mblr = SF3966002` | **Measured** footprint polygon; `hgt_median_m = 15.89`; `hgt_majoritycm = 1921`; `gnd_min_m = 10.07`; `hgt_maxcm = 3684` (rejected, §8) |
| DataSF Assessor Secured Roll, `https://data.sfgov.org/resource/wv5m-vpq2`, parcel 3966002 | `year_property_built = 1926`; `number_of_stories = 4`; `construction_type = C` (concrete); `use_definition = Industrial`; `zoning_code = M1`; `property_area = 129,940` sq ft; `lot_area = 38,000` sq ft; Inner Mission |
| DataSF Building Permits, `https://data.sfgov.org/resource/i98e-djp9`, block 3966 lot 002 (50 records, 1981–2023) | Four storeys in every permit 1984–2023; the rooftop wireless build-out ("install antennas at roof provide equipment rm at roof", 2000; "9 panel antennas, one gps antenna", 2001; "(3) 1' microwave dishes", 2012; "install 6 new antennas on roof", 2019); reroofing 1999/2009/2012; ground-floor lobby renovation 2023 |
| Esri World Imagery, z20 aerial, reprojected and overlaid on the measured footprint | The sawtooth monitor field across the south of the roof, the flat dark membrane across the north, rooftop clutter |
| Commercial listings (LoopNet / Showcase / SquareFoot, "The Koret Bldg") | Reinforced concrete; ~128,000–129,940 sq ft; current PDR/office/warehouse tenancy |
| OSM highway ways within 120 m | Street context: Alabama St west, Florida St east, 17th St south; the block runs north to 16th St |

Reference photographs are public-record images inside the SF Planning DPR form and are cited
by URL rather than committed to this repo.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor (WGS84) | `-122.4118477, 37.7645633` | **measured** — OBB centre of the DataSF footprint |
| Footprint OBB | 61.10 m x 54.63 m, 3,321 m2, 99.5 % rectangular fill | **measured** |
| OSM cross-check | 60.72 m x 54.00 m, 3,275 m2 | **measured**, agrees within 0.7 m |
| Heading | 17th Street walls bear 85.68°; Alabama/Florida walls 355.68° (block rotated +4.32° CCW) | **measured** |
| Storeys | 4 | **verified** (assessor + 40 years of permits) |
| Roof deck | 15.89 m above minimum ground | **measured** (LiDAR median; OSM `height=16` independently agrees) |
| Sawtooth ridge | 19.21 m | **measured, interpreted** (LiDAR modal height over 13,355 cells) |
| Ground elevation | 10.07 m NAVD88 | **measured** — the app's terrain handles this, not the asset |
| Main parapet crest | 17.6 m | *inferred* |
| Stepped pier caps | 18.4 m; corner caps 18.9 m | *inferred* |
| **Stair tower crest** | **22.5 m** | *inferred* — the target height, and the weakest number here (§8) |
| Floor heights | ground 4.9 m, upper floors 3.67 m | *inferred*, back-solved from the deck height and the photographed floor lines |

## 3. Orientation

`placeGeneric()` scales and positions but never rotates, so the asset is authored in true
world orientation (Blender `+Y` = north, `+X` = east) and the 4.32° block rotation is built
into the geometry. The contract's "front faces −Y" rule cannot be honoured literally: the
address front faces **west** (265.7°). Real-world orientation wins (AGENTS rule 5) and the
deviation is recorded in `REPORT.md`.

Because of the heading, the axis-aligned XY bounding box (67.3 x 61.6 m) is larger than the
building (61.1 x 54.6 m). That is expected, not a scale error.

## 4. What each side shows

**West — Alabama Street.** The address elevation and the hero. Cream painted concrete divided
by wide flat piers into roughly ten bays, each filled nearly edge to edge with tall
multi-light steel-sash industrial windows on all four floors. Above the top-floor glazing runs
the frieze: a cast **cog-wheel medallion over every pier**, and a parapet that steps up over
each pier so the skyline reads as a low crenellated rhythm. Two to three bays north of the
17th Street corner the wall breaks for the **stair tower** — a shallow projecting shaft with
pale vertical fins flanking a darker mauve-taupe centre panel, rising to a notched Art Deco
crown. Directly beneath it is the arched pedestrian entrance with the **"375" numerals** on
the pier beside it, and immediately south of that a wide roll-up freight door.

**South — 17th Street.** The long elevation (~61 m), same grammar: eleven bays, the same
medallion frieze and stepped parapet, a taller chamfered cap at the corner bay. Ground floor
is mostly service — wide roll-up freight doors and a scatter of openings. No tower.

**East — Florida Street.** Same structural grammar, plainer treatment: bay rhythm and steel
sash continue, the medallion frieze does not. Ground floor is loading. *Inferred* — no
source photograph covers this side straight on.

**North — rear.** Faces a narrow yard and the rest of the block, not a street. Largely blank
concrete with sparse openings and one service door. The app's aerial camera sees it plainly,
so it is built properly, but it carries no ornament.

**Top.** The most important surface. The southern ~60 % is a sawtooth monitor field: five
parallel ridges running east–west at ~19.2 m, glazing facing north (*inferred* — the standard
for a daylight factory of this date), opaque slope facing south. The northern ~40 % is a clean
dark membrane roof at deck level. The stair tower breaks the west edge. A rooftop
antenna/equipment cluster — an equipment room, dishes and a mast, permitted from 2000 onward —
sits toward the northeast. Vent stacks scatter along the west. A continuous parapet rings all
of it.

## 5. Recognition cues (ranked)

1. **The cog-wheel "AHN" medallions** in the parapet frieze — the one ornament nobody else in
   the Mission has
2. **The stepped Art Deco stair tower** over the Alabama Street entrance, the only break in
   the skyline
3. The **sawtooth monitor roof** — the identity from above, which is the app's default view
4. A long cream four-storey wall of tall steel-sash bays between expressed piers, wrapping a
   whole block corner
5. The stepped parapet with raised pier caps and chamfered corner bays

## 6. Preserved

- The single chunky block at its real 4.32° heading, at full block-corner scale
- The medallion frieze on the two street elevations, enlarged so it survives at city scale
- The tower's stepped silhouette and its pairing with the arched entrance
- The sawtooth roof as real geometry, not a texture
- The pier / glazing-band / spandrel grammar as a clear rhythm

## 7. Simplified

- Roughly twelve real bays per short elevation become ten; the long elevations get eleven
- Multi-light steel sash becomes a continuous recessed glazing band per floor, cut into bays
  by the proud piers — a concrete frame really does glaze continuously between its piers, and
  banding costs a fraction of what 126 punched openings would
- Medallions enlarged from ~1.2 m to 1.7 m and cut as a 12-tooth cog; the "AHN" monogram
  inside them is dropped as sub-pixel
- The medallion frieze runs on the west and south elevations only
- Five sawteeth at a constant pitch
- The rooftop antenna farm becomes one equipment room, one low unit, two dishes and a mast
- Window guardrails and fire-escape ironwork dropped entirely
- Ground-floor openings reduced to one arched entrance, six roll-up doors and the glazing band
- The survey's two sub-620 mm jogs on the east and west walls are absorbed into the expressed
  pier rhythm rather than modelled as footprint steps

## 8. Uncertainties and conflicting evidence

- **The stair-tower height (22.5 m) is the weakest number in this dossier.** It is a
  photogrammetric read of the 2007 DPR photograph, calibrated against the LiDAR roof deck
  (15.89 m) using the four photographed floor lines as a ruler. The honest range is 21–24 m.
  Because the tower is the tallest geometry, this number *is* `targetHeightM` and it scales
  the whole asset.
- **The tower's position along the west wall (13 m north of the southwest corner) is
  inferred** from bay counting in one oblique photograph; available aerial imagery did not
  resolve it. The pairing with the arched entrance is certain — the "375" numerals are on the
  pier beside that arch — so the tower stays on the Alabama Street side over the entrance
  whatever the exact offset.
- **`hgt_maxcm = 36.84 m` in the LiDAR record is not the building.** This corner carries a
  dense web of overhead trolley and utility wires, plainly visible across the 2007 photograph,
  and the LiDAR first return picked them up. `hgt_mincm = 0.24 m` in the same record shows the
  polygon also samples ground, so neither extreme is usable.
- **`height=16` in OSM is the roof deck, not the architectural top.** It agrees with the LiDAR
  median to within 0.11 m, which makes it look well sourced. The architectural top is the
  tower, ~6.6 m higher.
- **"The Koret Building" is the marketing name, not the historic one.** Every listing uses it;
  the survey form and the building's own ornament say Ames Harris Neville Co.
- **The sawtooth glazing orientation is inferred.** North-facing is the standard for a daylight
  factory of this date and the aerial imagery is consistent with it, but the imagery is not
  sharp enough to prove which slope is glass.
- **The east (Florida Street) elevation is unphotographed in the sources consulted.** It is
  modelled as the bay grammar without the medallion frieze.
- **The bay counts (10 / 11) are a design simplification**, not a survey.
- The large flat north roof section reads in aerial imagery as a single dark membrane at deck
  level; it could also be a slightly lower roof over a light court. Modelled flat at deck
  level, which is safe either way.
- **No architect is recorded** for the 1926 building in any source consulted; the DPR form
  names only the surveyor.
