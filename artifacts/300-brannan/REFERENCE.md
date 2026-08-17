# 300 Brannan Street — reference dossier

The **Blinn Estate Building**, 1912. Six storeys of reinforced concrete filling the
whole east corner of Second and Brannan in SoMa, a contributor to the South End
Historic District, and the tallest thing on its block by two storeys.

Compiled 16–17 August 2026 for `artifacts/300-brannan/`. Everything below was
re-verified against primary sources for this build; where this file and
`docs/asset-plans/300-brannan.md` disagree, this file and `REPORT.md` win.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| Page & Turnbull, *National Register Certification: South End Historic District*, 26 June 2008, Appendix A2 (`https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf`) | **Primary.** Building name (Blinn Estate Building), 1912, architects Charles C. Frye & George A. Schastey with Alvin E. Horlein as engineer, original use (wholesale furniture and carpet warehouse for Peck & Hills Furniture Co. and Wm. G. Volker & Co.), **six storeys**, **height 70 ft**, reinforced-concrete construction, **stucco** exterior, style "Commercial", Contributory / NR status 3D |
| Same document, Section V | The district's character-defining features: "rectangular-massed, utilitarian, rough-textured, earth tone-colored, brick or concrete structures with rhythmically spaced and deeply recessed fenestration, large arched loading docks, and restrained detailing consisting of flattened arch window treatment, brick corbelling, sheet metal cornices and abstract pilaster-like elements", plus "a preponderance of steel, multi-lite industrial sash windows … exterior wall-mounted fire escapes and distinctive parapet detailing" |
| DataSF EAS Addresses (`ramy-di5m`) | `300 BRANNAN ST` → parcel **3775008** (block 3775, lot 008) |
| DataSF Building Footprints (`ynuv-fyni`, `mblr = SF3775008`) | The surveyed footprint polygon (1,139.8 m2) and the LiDAR heights: `hgt_median_m` **20.84 m**, `hgt_majoritycm` 20.82, mean 20.91, σ 1.35 over 4,591 50 cm cells; `hgt_maxcm` **25.67 m**; ground 11.64–12.60 m NAVD88 |
| SF Assessor secured roll 2025 (`wv5m-vpq2`, block 3775 lot 008) | 1912, `number_of_stories = 6.0`, industrial use class, building area 68,884 sq ft, **lot area 12,300 sq ft (1,142.7 m2)** |
| OSM way/112758589 | Cross-check footprint (1,123 m2) and `height=21`. **Wrong about the corner** — see §5 |
| Google Street View, capture **May 2025**, panoramas at `37.781857,-122.392039` (the intersection), `37.781665,-122.392344` (Brannan, opposite the frontage), `37.782068,-122.392320` and `37.782221,-122.392513` (Second Street) | The current paint scheme, the canted corner, the bay counts, the segmental-arched ground-floor openings on Second Street, the roll-up loading bay, the fire escape on Brannan, the charcoal base and its cornice |
| KartaView sequences 2057142 (24 Nov 2019) and 1352479 (14 Mar 2019) | The 2008-renovation base at close range: charcoal storefronts, projecting entrance canopy, cylindrical wall lanterns, etched **300 BRANNAN** signage |
| Esri World Imagery, z20 nadir (~2023) | Roof: flat dark membrane inside a continuous parapet; the penthouse cluster just north-west of centre with its shadow; a low light-toned mechanical platform toward Brannan; a round tank west of the cluster; scattered vents and two pipe runs. **No tree canopy overhangs the roof** |
| LoopNet 16830204 / CompStak / Showcase / Cityfeet | *Observed (listing data).* Reinforced concrete, 6 stories, built 1912, renovated 2008, 67,792 sq ft rentable, class B creative office |

No copyrighted imagery is committed; the URLs and the panorama coordinates above
reproduce every view used.

## 2. Verified dimensions and location

| | |
|---|---|
| Anchor (WGS84) | **−122.3925543, 37.7818313** — the simplified footprint's AABB centre |
| Footprint | 1,136.5 m2 as built (survey 1,139.8 m2, −0.3%); lot area 1,142.7 m2, i.e. **full-lot coverage** |
| Roof deck | **20.84 m** (LiDAR median) |
| Parapet crest | **21.34 m** = the surveyed 70 ft |
| Penthouse crest | **25.20 m** — the export's bounding-box top and the manifest `targetHeightM` |
| Storeys | 6: one 5.00 m ground storey, five upper floors of 3.052 m |
| Elevations | Second St 28.18 m · cant 5.05 m · Brannan 27.73 m · Stanford 30.03 m · NW party wall 36.60 m |
| AABB of the export | 47.53 × 49.29 × 25.20 m — the 45° heading, plus the 0.74 m cornice projection |

**The height reconciliation, which is what makes this dossier hang together:**
LiDAR deck 20.84 m + a ~0.5 m parapet = 21.34 m = the surveyed 70 ft. Two
independent measurements agree, so the deck and the architectural height are
*measured*, and only the penthouse crest is estimated.

## 3. Orientation

Authored with Blender `+Y` = true north, `+X` = east; the loader applies no
rotation.

| Elevation | Length | Outward normal |
|---|---|---|
| Second Street (NE front) | 28.18 m | **45.2°** |
| The canted corner (E) | 5.05 m | **95.1°** |
| Brannan Street (SE front) | 27.73 m | **135.5°** |
| south-corner setback (2 edges) | 5.14 + 1.14 m | 135.6° / 224.1° |
| Stanford Street flank (SW) | 30.03 m | **225.5°** |
| north-west lot-line wall | 36.60 m | **315.1°** |

Simplified seven-vertex ring, metres, `+X` east / `+Y` north, CCW, centred on the
anchor:

```
(  3.036,  23.634)   N corner — Second St x NW party line
(-22.883,  -2.212)   W corner — NW party line x Stanford St
( -1.837, -23.634)   S corner — Stanford St x Brannan St
(  1.839, -20.035)   setback, 1.19 m in from the Brannan wall plane
(  2.660, -20.830)   setback returns — start of the Brannan frontage
( 22.437,  -1.398)   south end of the canted corner
( 22.883,   3.629)   north end of the canted corner
```

## 4. What each side shows

**Second Street (NE).** The service-and-entry face. Ground floor: a run of six deeply
recessed **segmental (flattened) arch** openings in a charcoal base, the last of them
a **roll-up loading bay** with a ramp, and one a stepped entrance with railings.
Above: five floors of light pilaster strips against dark recessed bays of very large
multi-lite steel sash, six bays wide. This face is north-east-facing and reads much
darker than Brannan in photographs — that is shade, not paint.

**The canted corner (E).** The identity. One window bay per floor in the same rhythm
as the frontages, flanked by its own pilaster pair, over a charcoal base whose heavy
cornice returns round it with a rounded soffit. In 2025 imagery a recessed corner
entrance sits under it behind temporary scaffolding.

**Brannan Street (SE).** Ground floor: large rectangular storefronts, the main
entrance under a projecting flat canopy with light metal **300** numerals and
cylindrical wall lanterns. A black steel **fire escape** climbs from the second floor
to the parapet roughly a fifth of the way along from the Stanford end. The
south-westernmost ~5 m of the frontage steps back 1.19 m.

**Stanford Street (SW).** A service flank on an 8 m alley: the same window rhythm in
a plainer version with no pilasters, a service door, and simpler ground-floor
openings. *No street-level photography was found for this face; its six-bay rhythm is
**inferred** from the frontages.*

**North-west lot-line wall.** A party wall against 577 Second Street and 318 Brannan,
both of them lower (8–18 m), so its upper storeys stand clear and the aerial camera
sees them. Built as a finished blank stucco plane with shallow lisenes, floor-line
courses and a sparse scatter of small openings on the top two floors. *Whether the
real wall carries more than that is **unresolved** — no view of it exists in any
source consulted.*

**Roof.** Flat dark membrane inside a continuous parapet; penthouse cluster just
north-west of centre (the crest), a lower bulkhead beside it, a light mechanical
platform with a row of units toward Brannan, a round tank, four vents, two duct
runs, one hatch and a walkway. The Second Street and Brannan thirds of the deck are
deliberately clean, matching the nadir imagery.

## 5. Recognition cues (ranked)

1. **The canted corner** carrying one bay per floor across the Second/Brannan
   intersection — nothing else on this block does it
2. **Six storeys** where every neighbour is two or three: this is the block's wall
3. The **light pilaster grid over dark recessed bays** — a strong vertical
   light/dark alternation across both frontages
4. The **charcoal base with its heavy projecting cornice**, wrapping the cant
5. **Segmental-arched** ground-floor openings on Second Street; the black fire
   escape on Brannan

## 6. Preserved / simplified

**Preserved:** the single full-lot volume and its real 45° heading; the canted
corner; the south-corner setback; the two-tone split; six-storey proportions (one
tall ground floor under five equal upper floors); the 6 / 1 / 6 bay rhythm; the
segmental arches; the fire escape; the penthouse-over-parapet silhouette.

**Simplified:** multi-lite sash → one glazed panel with a light sill per bay per
floor; pilaster mouldings → a single stepped capital block; the fire escape → flat
landings, two posts and diagonal stringers; roof plant → penthouse + bulkhead +
platform with four units + tank + four vents + two ducts; signage, lanterns,
canopies beyond the entrance one, address numerals, scaffolding and street trees all
removed.

**Exaggerated (one place only):** the base cornice is 0.78 m deep and projects
0.74 m — heavier than life — because the cornice line is what makes the cant read as
a cant from the app's aerial camera.

## 7. Uncertainties and conflicting evidence

1. **The penthouse crest, 25.20 m, is the least certain number here.** LiDAR maximum
   is 25.67 m over a 20.84 m deck (σ 1.35 m). A ~4.4 m elevator/stair overrun is
   normal for a 1912 freight-elevator loft and the nadir imagery shows a real,
   bright, shadow-casting box cluster, but a mast or railing would also return
   25.67 m; the build shades it down by ~0.5 m for that reason.
2. **OSM traces this building as a clean 37.71 × 29.78 m rectangle with a sharp east
   corner** and agrees on area to within 1.5%, which makes it a plausible-looking
   trap. The DataSF survey and May-2025 Street View both show the cant.
3. **The cant has two lengths.** The raw DataSF ring's corner edge is 8.09 m because
   its ends sit 2.18 m and 0.98 m proud of the two wall planes — a shallow projecting
   corner bay. Intersecting the cant line with the two facade lines gives the flush
   chord, **5.05 m**, which is also what the nadir parapet measures and exactly one
   window bay in Street View. The build uses 5.05 m.
4. **Bay counts** (6 / 1 / 6) are read off oblique May-2025 Street View; the Stanford
   count of 6 is inferred with no photograph at all.
5. **The paint scheme is post-2008** and documented only by photography. It is also
   the whole visual identity of the asset.
6. **Do not confuse this with 301 Brannan**, the red-brick 1909 Crane Company
   Building (Lewis P. Hobart) directly across Brannan, which dominates community
   street-level imagery of this intersection. 300 Brannan is the *stucco* one.
