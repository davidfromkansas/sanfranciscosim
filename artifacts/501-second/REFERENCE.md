# 501 Second Street — reference dossier

Compiled 16 August 2026 for `artifacts/501-second/`. This is the modeller's own
verification pass over `docs/asset-plans/501-second.md`; where the two differ, this file
and `REPORT.md` win.

501 Second Street is a 1925 seven-storey cream cast-stone office block filling the east
corner of Second and Bryant in SoMa, 78 m northeast of the 524 Second Street warehouse
built in the same batch. At 72.79 x 42.24 m and a measured 33.0 m parapet it is by a wide
margin the largest bespoke footprint in the SoMa set — five times 524 Second and eighteen
times 358 Brannan — and the only one that is a proper Renaissance-Revival commercial
block rather than an industrial shed.

## 1. Sources and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| DataSF Parcels `acdm-wktn`, `blklot=3774067` | address-to-lot link: `501 02ND ST`, zoning MUO | authoritative |
| SF Assessor `wv5m-vpq2`, block 3774 lot 067 | Office; 248,888 sq ft; `year_property_built 1985`; `number_of_stories 8` (both reconciled below) | authoritative, needs reading |
| DataSF LiDAR `ynuv-fyni`, `SF3774067` | footprint 72.67 x 42.39 m, 3,107 m2; `hgt_majority` **33.26 m**, `hgt_median` 32.72, `hgt_mean` 29.53, `hgt_std` **6.41**, `hgt_max` **37.66**, 12,467 cells; ground 13.75 m NAVD88 | measured |
| SF Building Permits `i98e-djp9` (100+ records) | **every** permit 2010–2026 gives `number_of_existing_stories = 7` and `existing_use = office`; suite-level tenant fit-outs throughout, i.e. a large multi-tenant floorplate | authoritative |
| OSM way 112758588 | `addr:housenumber=501`, `addr:street=2nd Street`, `building=yes`, **`height=33`**; footprint OBB 72.79 x 42.24 m, 3,074 m2 | measured |
| LoopNet listing "501 2nd St" | 7 storeys, 207,809 SF rentable, typical floor 29,687 SF, Class B, **built 1925, renovated 1985** | corroborating |
| Street View, Second x Bryant corner, **Jan 2025** | the tripartite composition; cream cast stone; dark steel sash; the square corner | primary visual |
| Street View, Bryant Street, **Apr 2025** | the **main entrance** under a flat canopy lettered "501 SECOND"; the bracketed belt cornice; the carved frieze; the pier rhythm; a second recessed service bay | primary visual |
| Street View, Second Street, **May 2025** | the address elevation | primary visual |
| Google Maps satellite, Vexcel 2026 | roof: penthouse, light court, scattered plant, the parking deck on the southeast side | primary visual |

## 2. Verified dimensions and location

- **Anchor (WGS84):** `-122.3929683, 37.7831785` — the footprint OBB centre.
- **Footprint:** 72.79 x 42.24 m, 3,074 m2. OSM and DataSF LiDAR agree to **1%** here
  (72.67 x 42.39, 3,107 m2) — unlike 524 Second, where three sources disagreed by 12%.
  No adjudication was needed; the OSM OBB is used.
- **Main parapet:** 33.0 m — DataSF LiDAR modal plane 33.26 m and median 32.72 m over
  12,467 cells, with OSM `height=33` agreeing independently. **Measured.**
- **Penthouse crest (`targetHeightM`):** 37.7 m — DataSF LiDAR `hgt_max` 37.66. **Measured.**
- **Ground:** 13.75 m NAVD88. The app's terrain handles this; the asset sits on z = 0.

## 3. Orientation

Rotated ~45.4° off the world axes, like the whole SoMa grid.

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| Second Street | 42.24 m | **225.4° SW** | the address |
| Federal Street side | 72.79 m | 135.4° SE | public, plainer |
| party wall to 533 Second | 42.24 m | 45.4° NE | blind |
| Bryant Street | 72.79 m | **315.4° NW** | hero, main entrance |

Footprint in Blender coordinates (metres, +X east, +Y north), CCW, centred on the anchor:

```
(-40.74, -10.51)   west corner — Second x Bryant
(-11.10, -40.59)   south corner
( 40.74,  10.51)   east corner
( 11.10,  40.59)   north corner
```

The 45.4° heading turns a 72.79 x 42.24 m building into an ~83.1 x 82.8 m axis-aligned
bounding box. That is expected, not a scale error.

## 4. What each side shows

**Northwest — Bryant Street (hero, 72.79 m).** Cream cast stone throughout. Ground floor:
tall openings, a **recessed main entrance under a flat canopy** carrying "501 SECOND" in
metal letters, and a second recessed service bay beside it. At 11.6 m a **projecting belt
cornice on modillion brackets** separates base from shaft. Above it, five storeys of flat
cream piers with slightly recessed spandrels and dark steel-sash windows in a strict grid.
Below the main cornice, a **carved frieze band** of repeating ornament. The main cornice
projects hard at 30.9–32.2 m; a plain parapet runs to 33.0 m.

**Southwest — Second Street (the address, 42.24 m).** The same tripartite system at a
narrower rhythm. No entrance of consequence — the door is round the corner.

**Southeast — Federal Street side (72.79 m).** A real elevation, plainer: same bay rhythm
and same cornices, less ornament, facing a parking deck. Seen obliquely from the street
and fully from the air.

**Northeast (42.24 m).** Party wall to 533 Second Street. Blind cream stucco.

**Top.** 3,074 m2 at 33.0 m — the largest roof in the bespoke SoMa set and the surface the
app's camera spends the most pixels on. Pale membrane inside the parapet ring; a **light
court** cut into the middle (which is what reconciles a 3,074 m2 footprint with a 2,758 m2
typical floor); a **penthouse** to 37.7 m toward the Second Street end; scattered plant.

## 5. Recognition cues (ranked)

1. **Size.** 72.8 x 42.2 m at 33 m — nothing else on these blocks is close.
2. **Cream in a brick district** — the pale mass against 524 Second's red brick 78 m away
   and against the whole South Park cluster.
3. **The tripartite composition** — base, shaft, cornice — as three horizontal moves.
4. **The two projecting cornices**, which are what make those moves legible from above.
5. The penthouse breaking an otherwise dead-level parapet.

## 6. Preserve / simplify

**Preserve:** the 72.79 x 42.24 m proportion, the 33.0 m parapet and the 45.4° heading;
the three horizontal moves and both cornice projections; the vertical pier rhythm on all
three public elevations; cream, never brick; the penthouse as the crest.

**Simplify:** both cornices thickened and pushed out so their shadow line survives at
distance (the one place semantic exaggeration is spent); ~30 panes per steel sash become
one glazed panel in a frame; the carved frieze becomes one recessed band and the modillion
brackets a continuous soffit; the "501 SECOND" lettering becomes a glowing strip, not
modelled letters; storefront mullions, downpipes, fire escapes, conduit and street trees
dropped; roof clutter reduced to the penthouse, the court, a stair bulkhead, three plant
blocks, five vents and a hatch.

## 7. Uncertainties and conflicting evidence

- **The Assessor says 8 storeys and 1985; every permit says 7.** Both are true of the same
  building: the listings give "built 1925, renovated 1985", the Assessor's
  `year_property_built` records the renovation, and its storey count includes the penthouse
  the LiDAR maximum also sees. **7 occupied storeys plus a penthouse** is the reading used.
- **`hgt_maxcm` = 37.66 m is real here, and that is the opposite call from 524 Second.**
  At 524 the equivalent figure was edge bleed — a 13.32 m maximum against a 0.95 m standard
  deviation beside a 19.7 m neighbour. Here the standard deviation is **6.41 m** over 12,467
  cells with a modal plane at 33.26 m, the aerial shows a distinct raised block, and the
  nearest taller neighbour is 60 m away, well outside bleed range.
- **The light court is inferred from arithmetic plus imagery.** 3,074 m2 of footprint
  against a 2,758 m2 typical floor leaves 316 m2 unaccounted for, and the aerial shows a
  rectangular notch. Its exact size and position are *estimated*.
- **The bay counts (7 / 13 / 13) are inferred** from obliquely-shot panoramas partly
  occluded by street trees and power poles. This is the most likely place for the model to
  be visibly wrong.
- **The belt cornice at 11.6 m and the main cornice at 30.9 m are photogrammetric**,
  derived by dividing the measured 33.0 m parapet across the permits' 2 + 5 storey split.
  Only the parapet and the crest are measured.
- **No architect is recorded** for the 1925 building in any source consulted, and the scope
  of the 1985 renovation is unknown — in particular whether the ground-floor openings are
  original.
