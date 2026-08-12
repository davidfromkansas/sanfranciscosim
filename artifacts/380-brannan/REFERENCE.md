# 380 Brannan Street — reference dossier

Research compiled 12 August 2026 for the SF-SIM miniature asset. Everything below
was re-verified against primary sources during the build; where this dossier
disagrees with `docs/asset-plans/380-brannan.md`, this file and `REPORT.md` win.

## 1. What the building is

A 1908 unreinforced-brick-masonry warehouse at 380 Brannan Street in SoMa, one
block west of South Park, converted to creative office and currently occupied by
South Park Commons. Two storeys, flat roof, continuous parapet, roughly
20 x 24 m on plan.

It is not a monument. It was modelled as a *character* building: the block's most
memorable ordinary building, whose entire identity is one bold coral stripe
across a slate-gray painted front.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/1171034242](https://www.openstreetmap.org/way/1171034242) | address, `building=commercial`, occupant name, cross-check footprint (461.3 m2, 24.2 x 19.1 m) |
| DataSF Building Footprints, `ynuv-fyni` (LiDAR-derived), `mblr = SF3775022` | **authoritative footprint** (480.3 m2) and **authoritative heights**: `hgt_median_m` 11.02, `hgt_maxcm` 1264, `gnd_min_m` 8.31 |
| DataSF Assessor Secured Roll, `wv5m-vpq2`, block 3775 lot 022 | year built 1908; storey count 3 (**contradicted**, see §6) |
| DataSF Building Permits, `i98e-djp9`, block 3775 lot 022 | storey count 2 (1990-2015); 1990 "parapet reinforcing"; 1998 "earthquake retrofit-umb ordinance / anchor bolt, vertical brac"; 1993/1994 entrance canopy |
| Google Street View, Brannan Street pano, capture May 2025 | front elevation: slate-gray paint, coral band, segmental-arched ground openings, arched freight door, steel-sash upper windows, fire escape, "380" plate, roof mast |
| Google Street View, Varney Place pano, capture Jan 2025 | rear elevation: raw red brick, corbelled brick cornice, segmental-arched barred windows, arched roll-up service door |
| Google Maps satellite (Vexcel, 2026) | flat light-membrane roof, skylight cluster, mechanical units, parapet ring |
| Commercial listings (LoopNet / Showcase, "376-380 Brannan St") | 11,560 sq ft; "standalone brick and timber building"; 15 ft ceilings; second-floor skylights |

No architect is recorded for the 1908 building in any source consulted.

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| WGS84 anchor (footprint OBB centre) | `-122.3940217, 37.7806308` | measured |
| Footprint area | 480.3 m2 | measured (DataSF) |
| Brannan frontage (SE edge) | 20.17 m | measured |
| Depth (SE to NW) | 23.75-23.95 m on the flanks | measured |
| Rear width (NW edge) | 19.86 m | measured |
| Rectangular fill of the OBB | 99.1% | measured |
| Roof deck | 11.02 m above grade | measured (LiDAR median) |
| Tallest feature | 12.64 m above grade | measured (LiDAR max) |
| Parapet crest | ~11.9 m | inferred (deck + 0.9 m) |
| Storeys | 2 | permits + photography |
| Ground elevation | 8.31 m NAVD88 | measured — the app's terrain owns this, not the asset |

## 4. Orientation

The building sits at roughly 45° to the world axes, like the whole SoMa grid.
The measured footprint polygon (Blender XY, metres, `+X` east, `+Y` north, CCW,
centred on the anchor) is hard-coded as `FOOTPRINT` in the build script:

```
( 15.615,  -1.519)   ( 15.493,  -1.396)   ( -1.191,  15.507)
( -1.270,  15.586)   (-15.394,   1.621)   (  1.213, -15.642)
```

| Edge | Length | Outward | Elevation |
|---|---|---|---|
| 5 | 20.17 m | SE 135.6° | **Brannan Street front** |
| 1 | 23.75 m | NE 45.4° | northeast flank |
| 3 | 19.86 m | NW 315.3° | **Varney Place rear** |
| 4 | 23.95 m | SW 226.1° | southwest flank |

Edges 0 and 2 are 0.17 m and 0.11 m survey chamfers, kept in the model.

The asset is authored in true-world orientation because `placeGeneric()` in
`app/src/assets.js` scales and positions but never rotates. The contract's
"front faces −Y" rule cannot be honoured literally here — the real front faces
southeast — and per `docs/asset-plans/README.md` real-world orientation wins.

Consequence: the axis-aligned XY bounding box is ~31 x 31 m for a 20 x 24 m
building. That is correct, not a scale error.

## 5. What each side shows

**Southeast — Brannan Street front.** The hero elevation and the only painted
one. Top to bottom: a plain parapet cap; a continuous coral/salmon band running
the full width; tall industrial steel-sash windows with dark frames; a string
course at the floor line; and a ground floor of segmental-arched openings — a
wide arched freight door toward the southwest end, barred arched windows, and a
recessed pedestrian entrance under a small canopy with the "380" numerals above
it. A steel fire escape balcony hangs off the upper floor right of centre. A slim
twin-pole mast rises above the parapet.

**Northwest — Varney Place rear.** Raw, unpainted red brick finished with a
corbelled brick cornice. Segmental-arched windows on both floors, heavily barred,
with pale stone sills, plus a segmental-arched roll-up service door. The alley is
narrow so this face is only seen obliquely in life — but the app's aerial camera
sees it plainly, so it is built properly.

**Northeast and southwest flanks.** Raw red brick, largely blank party-wall
surfaces with sparse openings. Modelled with four arched windows per floor rather
than an invented full grid.

**Top.** Flat light-membrane roof inside a continuous parapet, carrying a
skylight cluster over the second floor, grouped mechanical units, and a stair
penthouse.

## 6. Conflicting evidence, and how it was resolved

1. **Storey count — Assessor says 3, everything else says 2.** The SF Assessor
   roll records 3.0 storeys in every year from 2007 to 2025. Every building
   permit from 1990 to 2015 records 2, and both street-level photographs plainly
   show two floors. The listed 11,560 sq ft is ~2.24x the 480 m2 footprint, which
   fits two full floors plus a mezzanine — the most likely source of the
   assessor's third storey. **Built as 2 storeys.**

2. **OSM `height=11` is the roof deck, not the crest.** It happens to match the
   LiDAR median (11.02 m) almost exactly, which makes it look like a trustworthy
   architectural height. It is not: the parapet crest is ~11.9 m and the tallest
   feature 12.64 m. This is precisely the trap `docs/asset-plans/README.md` warns
   about, in a case where the tag looks plausible.

3. **"Brick and timber" is only half true externally.** The structure is brick
   and timber and the rear and flanks are raw brick, but the Brannan front is
   painted slate gray. A modeller working from listing copy alone would build the
   wrong front elevation.

## 7. Recognition cues, ranked

1. The coral band under the parapet cap on a slate-gray box
2. A chunky two-storey masonry box with a flat roof and continuous parapet
3. The painted-front / raw-brick-back split
4. Segmental-arched ground-floor openings, especially the wide freight arch
5. The front fire escape

## 8. Preserved / simplified

**Preserved:** the single chunky volume and its real 45° heading; the coral
band's full-width continuity and position under the cap; the two-material story;
the arched ground-floor openings as true arches.

**Simplified or exaggerated:** ~14 upper windows became 6 clean bays per long
elevation; individual bricks became flat colour; the corbelled rear cornice
became one 0.22 m proud band; window bars and grilles were dropped entirely as
sub-pixel; the coral band was thickened to 1.1 m so it survives at thumbnail
size — the one place semantic exaggeration was spent; the fire escape became a
chunky balcony slab and rail with no ladder treads; roof clutter became a
five-skylight field, a three-unit mechanical row and a stair penthouse.

**Dropped:** the twin roof mast. It is a hairline at the app's camera and would
have set the bounding-box top on a feature that reads as nothing.

## 9. Remaining uncertainties

- The 6-bay window rhythm is *inferred* from oblique photography and is the
  weakest number in the dossier.
- The coral band's exact vertical extent is *inferred* (1.1 m, 10.1-11.2 m).
- The parapet crest at 11.9 m is *inferred* from the LiDAR deck plus a typical
  parapet; only the 11.02 m deck and 12.64 m maximum are measured.
- Whether the flanks are true party walls or have a small gap to the neighbours
  is unresolved; the listing calls the building "standalone". All four faces were
  modelled as finished brick, which is safe either way.
</content>
