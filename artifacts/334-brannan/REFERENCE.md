# 334 Brannan Street (Sherman and Clay Building) — reference dossier

Compiled 16 August 2026 for `artifacts/334-brannan/`. This file records what the
model was built from and where the plan
(`docs/asset-plans/334-brannan.md`) was corrected. Where this file and the plan
disagree, this file — and `REPORT.md` — win.

## 1. Identity

| | |
|---|---|
| Address | 334 Brannan Street, San Francisco, CA 94107 |
| Building name | **Sherman and Clay** |
| Block / lot (APN) | 3775 / 101 |
| Built | **1929** |
| Storeys | 3 |
| Style | 20th-Century Industrial |
| Construction / exterior | Reinforced concrete / concrete |
| Historic status | **Contributory**, South End Historic District; National Register status code **3D** |
| Original / current use | Office & light industrial; a printing plant into the 2000s, boutique creative office today |
| Architect | none recorded in any source consulted |

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3775101` | address-to-lot link; the **surveyed parcel polygon** the model is built on; zoning CMUO |
| OSM way 71211341 | the same polygon, vertex for vertex; `addr:housenumber=334`; `height=12` (agrees with LiDAR for once) |
| DataSF LiDAR building footprints `ynuv-fyni`, `mblr=SF3775101` | 1,862 cells at 50 cm = 465.5 m2; `hgt_median 12.14 m`, `hgt_majority 12.18`, `hgt_mean 12.14`, `hgt_std 1.41`, `hgt_min 5.03`, `hgt_max 15.63`; `gnd_min 11.44 m` NAVD88 |
| DataSF LiDAR, `SF3775015` (340 Brannan) and `SF3775012` (326 Brannan) | the neighbours: 340 is 14.82 m median / 17.79 m max on ground 1.26 m lower; 326 is two low volumes, 2.93 m and 5.66 m median |
| SF Assessor secured roll `wv5m-vpq2`, parcel 3775101 | **1929**, 3 storeys, use Industrial, construction class B, lot area 5,597 sq ft, identical in every roll year 2007-2025 |
| SF Building Permits `i98e-djp9`, block 3775 lot 101 | 2006-12-06 ground-floor assembly room, use "printing plant"; 2009-06-15 final; **2010-08-04 re-roofing, $88,855** — the light membrane roof the aerial shows |
| Page & Turnbull, *South End Historic District* National Register certification, 26 June 2008, Appendix A2 (`sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf`) | the **building data form** for APN 3775/101: name "Sherman and Clay", 1929, 20th-Century Industrial, 3 storeys, reinforced concrete, Contributory, 3D. Also the form for 340 Brannan (1911, 5 storeys, non-contributory) — the source of the listings' wrong date |
| The same document, section V | the district's character-defining features: rectangular massing, rhythmically spaced deeply recessed fenestration, large arched loading docks, restrained detailing of "abstract pilaster-like elements", earth-tone colour |
| Google Street View, Brannan Street panorama, capture **May 2025** | the whole facade: two-tone paint, six bays of steel sash, the gilt pier caps, the gold frieze, the entry tower with its two pink panels and vertical "334", the wide roll-up freight door, the two ground-floor sash windows, the fire escape at the southwest end |
| Google Street View from in front of 317 Brannan, capture May 2025 | the northeast end in oblique: the entry tower reads as a distinct element; 326 Brannan next door is a walled garden, not a building wall |
| User photosphere inside JAX Vineyards, 326 Brannan, capture Jan 2019 | the **exposed northeast flank**: a plain painted wall with a planted living wall at its base |
| Google Maps satellite (Vexcel, 2026) | the roof: light membrane, a furnished deck zone toward Brannan, a low structure near the north corner, no penthouse breaking the skyline |
| Avison Young / Showcase / TenantBase / CompStak listings | 15,868 RSF over three floors, roof deck with city views, loading dock, showers per floor; **their 1911 date is wrong** |

No copyrighted imagery is committed with this asset; the references above are
links and observations only.

## 3. Verified dimensions, location, orientation

- **Anchor (WGS84):** `-122.3930344, 37.7814147` — the parcel-polygon centroid,
  which agrees with the Assessor's published centroid to 0.4 m.
- **Footprint:** a near-perfect square standing on a corner. Corner offsets from
  the anchor, in metres, `+X` east / `+Y` north:
  `S (-0.04, -15.17)`, `E (14.89, -0.28)`, `N (0.04, 15.17)`, `W (-14.88, 0.22)`.
  Edge lengths 21.08 (SE), 21.43 (NE), 21.12 (NW), 21.38 (SW); area 452 m2.
  A fifth surveyed vertex at `(7.30, 7.66)` lies 0.03 m off the straight N→E edge
  and is dropped as survey noise.
- **Heading:** Brannan front faces **135.1° true (SE)**; exposed flank 46.1° (NE);
  rear 314.9° (NW); party wall 226.1° (SW).
- **Heights as built:** roof deck **12.15 m** (LiDAR median 12.14, *measured*);
  parapet coping crest **13.10 m** (*inferred*); gold pier caps **13.40 m**
  (*inferred*) = the bounding-box top and the manifest `targetHeightM`.
- The axis-aligned bounding box is ~30.2 x 30.6 m for a 21 x 21 m building. That
  is the 45° heading, not a scale error.

## 4. Observations by elevation

**Southeast — Brannan Street (hero).** Three storeys of painted reinforced
concrete in two tones: a **warm greige** structural frame (broad flat piers,
spandrel and lintel bands, window surrounds) against **sage-green** recessed
panels. Six bays of tall near-black steel industrial sash fill floors 2 and 3,
the top floor slightly taller. Every pier terminates in a small **gilded capital
block** that rises above the parapet, and a band of **gold geometric ornament**
runs across the top of every bay. Ground floor: a very wide sage roll-up freight
door under a heavy greige lintel, then two multi-light sash windows, then the
**entry tower** — a narrower sage bay projecting slightly, carrying a
round-headed portal, a vertical `334` plate and two **pale-pink vertical panels**
under their own gilt caps. A dark painted plinth runs along the base.

**Northeast — exposed flank.** 326 Brannan is a one-storey 1959 building set back
from the street and the gap is JAX Vineyards' walled garden, so this whole 21 m
elevation reads from the sidewalk. It is a plain sage-painted wall with a
**planted living wall** across its base. No window rhythm appears in any
reference and none was invented.

**Southwest — party wall.** Hard against 340 Brannan, which is two to three
metres taller. Blind, and invisible in practice.

**Northwest — rear.** Faces the block interior with no public vantage. Modelled
plain with one service door; labelled *inferred*.

**Top.** One flat level at 12.15 m inside a parapet at 13.10 m. Light membrane
(re-roofed 2010). The Brannan half is a **used roof deck** — tables, chairs and
planters. Toward the north corner a low bulkhead, plus two skylights, a mechanical
block, a duct, a hatch and two vents. Everything is below the parapet, which is
why no street photograph shows any of it.

## 5. Recognition cues (ranked)

1. **The gilded crest** — gold frieze band plus a gold cap on every pier. The only
   gold on the block face
2. **Two-tone greige-and-sage paint** over the six-bay pier rhythm
3. **The entry tower** with its two pale-pink Deco panels
4. **The very wide roll-up freight door**
5. The square 45°-on footprint and the used roof deck

## 6. Preserved / simplified

**Preserved:** the surveyed square footprint and the real heading; six bays,
countable from the app's aerial; the gold frieze and every pier cap; the greige
frame / sage recess split; the pink tower panels; the exposed northeast flank and
its living wall; a roof deck that is furnished rather than blank.

**Simplified:** the frieze's repeating cast ornament becomes one flat gold panel
per bay; ~40 panes per sash become one glazed panel in a frame; the pier caps are
pushed a little proud of the parapet so the crest reads as a deliberate saw-tooth;
the pink panels are widened to 0.58 m to survive at city scale; the fire escape at
the southwest end is dropped (it stands in the shadow of a taller neighbour, reads
as noise at city scale, and 350 Brannan two doors away already carries the block's
one modelled fire escape).

## 7. Corrections to the plan (`docs/asset-plans/334-brannan.md`)

1. **§2.3 winding order.** The plan lists the footprint corners `E, S, W, N` and
   calls that "the winding order the build script uses". That order is *clockwise*
   and would invert every outward normal. The build script uses `S, E, N, W`
   (counter-clockwise), which puts the Brannan front on edge 0. Corner
   coordinates are unchanged.
2. **§2.7 / §2.8 body colour.** The plan made the body `Toy_stone` and applied
   sage "recesses" on top of a full-width greige skin panel. A recess cannot be
   cut out of an applied skin without booleans. Built instead as: greige **body**,
   sage recess panels applied flush per bay, greige piers and bands proud between
   them, and a separate sage skin on the northeast flank (which is genuinely
   painted sage). Same photographed result, fewer parts.
3. **§2.7 step 8 living wall.** Raised to sit on the plinth (0.40-3.30 m) and
   widened to 15.4 m; at the planned 12.8 m x 0.30 m base it read as a green
   rectangle floating on a blank wall.
4. **Palette.** `Toy_leaf` deepened from `6d8558` to `5b7347` so the living wall
   separates from the sage behind it.
5. **§2.7 step 10 roof furniture.** Re-laid out after the first aerial: two tables
   with chairs and three planters in the Brannan half, skylights beside the
   bulkhead, rather than the planned scatter.

## 8. Uncertainties and conflicting evidence

- **The 1911 date in every commercial listing is wrong.** It is 340 Brannan's
  construction date (South End Historic District data form, APN 3775/015). The
  Assessor's roll and the district's own form for 3775/101 both say 1929, and the
  gold frieze and pink Deco panels are 1929 detailing.
- **`hgt_max` 15.63 m is not this building.** 340 Brannan shares the southwest
  property line, has a 14.82 m median and a 17.79 m max on ground 1.26 m lower,
  and its rooftop penthouse stands on that boundary — expressed against this
  building's ground it reads 15-16.5 m. Treated as polygon-edge bleed. The same
  trap 358 Brannan's dossier documents at 13.32 m, with the neighbour identified
  this time. No fourth storey was built.
- **The parapet (13.10) and pier caps (13.40) are estimated**, scaled off the May
  2025 panorama against the measured 21.08 m frontage; ±0.5 m. The manifest entry
  is therefore `"estimated": true`. The 12.15 m deck is LiDAR-measured.
- **The Assessor's 5,597 sq ft lot area disagrees with the 4,865 sq ft surveyed
  polygon by 15%.** The parcel polygon, the OSM way and the LiDAR footprint all
  agree with one another; the model sits on them.
- **Six bays is read from one panorama** (counted twice — window columns and
  frieze groups). At a 45° heading the northeast end foreshortens.
- **The portal head** reads as a segmental arch in the one frontal photograph;
  whether it is a true arch or a flat head with a rounded soffit is *inferred*.
- **The rear elevation is unphotographed.** Modelled blind deliberately: a
  truthful blank beats an invented window grid.
- **No architect is recorded.** "Sherman and Clay" is the building name from the
  district data form; Sherman, Clay & Co. was the West Coast piano and
  Victor-phonograph house, and a 1929 warehouse-and-service building for them fits
  the use history, but no source consulted states the original owner explicitly.
