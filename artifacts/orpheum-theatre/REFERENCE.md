# Orpheum Theatre — reference dossier

Built for `artifacts/orpheum-theatre/` from the plan in
`docs/asset-plans/orpheum-theatre.md`, re-verified independently on 19 August 2026.
Where this file and the plan disagree, **this file wins** — corrections are listed
in §7.

## 1. What the building is

The Orpheum Theatre, 1192 Market Street at Hyde, Grove and 8th, Civic Center. Opened
20 February 1926 as the **Pantages Theatre**, the fifth of Market Street's six movie
palaces, in a mixed theatre-and-offices block called the **Marshall Square Building**
(developer William Wagnon, theatre leased to Alexander Pantages). Architect
**B. Marcus Priteca**, who had designed the whole Pantages circuit since about 1912 and
turned here from his earlier classicism to a **Plateresque / late Spanish Gothic**
terra-cotta front — "the most impressive theater façade surviving on Market Street"
(SF Landmarks Preservation Advisory Board, Final Case Report, 20 October 1976).
Renamed Orpheum by RKO in 1929; Cinerama house 1953–68; live theatre since 1977; a
$20 m rebuild in 1997–98 demolished and rebuilt the stagehouse for Broadway touring.
**San Francisco Designated Landmark #94.** Operated by BroadwaySF.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/35115840 (`name=Orpheum Building`, `heritage:ref=94`, wikidata Q121306407) via Overpass | footprint geometry, heritage refs. **Its `height=46 m` tag is wrong** — see §7.1 |
| Nominatim, node/11100318800 | address resolution. The theatre is a POI node, not the building; matched into the way by point-in-polygon |
| DataSF *Building Footprints (LiDAR heights)* `ynuv-fyni`, building `SF0351022` | every height in this dossier. 11,595 cells: `hgt_max` 27.19 m, median 21.47, mean 20.61, sd 3.36, mode 16.80, min 7.86; ground 15.68 m NAVD88 min / 16.22 median |
| Wikipedia, *Orpheum Theatre (San Francisco)* | names, architect, 1926 opening, landmark status, capacity 2,197, the 1998 renovation |
| NoeHill, *SF Landmark 94* (quotes the 1976 Final Case Report at length) | designation, Priteca attribution, the Spanish Gothic turn, the six Market Street palaces |
| San Francisco Theatres blog, *The Pantages / Orpheum Theatre* (June 2017) | Marshall Square Building name; developer; **stage before/after: grid height 60 ft → 75 ft**, depth 30 ft → 39 ft 10 in, proscenium 48 → 50 ft, wall-to-wall 68 → 82 ft; ~30 reproductions of Priteca's 1926 drawings (Gary Parks collection) |
| historictheatrephotos.com, *Orpheum — San Francisco* | independent confirmation of the 1997–98 stagehouse demolition and rebuild, and the same stage dimensions |
| PCAD (U. Washington) building 1555 | architect firm, opening date, capacity, use history |
| Cinema Treasures #234, Clio #40678, cinematour | corroborating style descriptions (Spanish Baroque / Moorish; "patterned after a 12th-century cathedral") |
| Wikimedia Commons, *Category:Orpheum Theatre (San Francisco)* | the photographic basis for §4. Principally `San Francisco Orpheum Theatre 01.jpg` (Joe Mabel, CC BY-SA — the full Market elevation from the Grove/Market corner), `…03.jpg`, `…04.jpg`, `Orpheum Theatre - panoramio.jpg`, `Orpheum Theater - panoramio.jpg` |
| Google satellite imagery, z20, tiled on the anchor | the roof plan: hipped auditorium roof, red tile eaves, mechanical valley, stage house at the NE |
| `pipeline/data/buildings_datasf.geojson` + `overture_buildings.geojsonseq` | the exclusion measurement in §8, taken against the geometry the bake actually consumes |

No copyrighted imagery is committed. Reference photographs were read, not redistributed.

## 3. Verified dimensions and location

| | Value | How |
|---|---|---|
| Footprint | 64.74 m E–W x 74.99 m N–S axis-aligned; 2,967 m² polygon | OSM geometry reprojected to the app's local tangent frame |
| Market frontage | 59.63 m at bearing **45.9°** cw from N, plus a 13.04 m chamfer at the Hyde corner | same |
| Hyde flank | 61.41 m at bearing 171.5° | same |
| DataSF cross-check | `SF0351022` traces the same block, 2,884 m² after `simplifyRing(0.6)` — within 3 % of OSM | pipeline geometry |
| **Architectural top** | **27.2 m** (stage-house roof) | LiDAR `hgt_max` 27.19 m; corroborated in §5 |
| Main street eave (tall block) | 23.3 m, parapet 24.3 m | photogrammetric, §5 |
| NE wing eave | 16.5 m, parapet 17.5 m | photogrammetric, §5 |
| Blade-sign crown | ~25.7 m real, modelled at 26.0 m | photogrammetric |
| Ground | 15.68 m NAVD88 | DataSF `gnd_min_m` |
| **Anchor as shipped** | **−122.4146087, 37.7793182** | the exported model's AABB centre, printed by the build script — see §7.2 |

## 4. What each side shows

- **South-east — Market Street.** The show face, and it steps. From the Hyde corner to
  the entrance bay (~35 m): a ground arcade of round arches on barley-twist terra-cotta
  columns, three storeys of large steel-sash glazing in heavily ornamented piers, a deep
  relief frieze, a projecting red mission-tile pent roof, then a low parapet pierced by
  oval oculi. North-east of the bay the same language drops to two glazed storeys over
  the arcade. Between them the entrance bay: taller, more encrusted, crested above the
  eave, carrying the blade sign, with the marquee at its foot and the arched poster panel
  standing to the sign's west.
- **The blade sign.** Projecting perpendicular to the facade, dark green with a
  gold-bead frame, an ornate finialled crown, ORPHEUM reading downward in white bulb
  letters. ~8.5 m to ~25.7 m — the tallest thing on the street front.
- **South-west — the 13 m chamfer** at Market x Hyde, full height, same treatment.
- **West — Hyde Street (61.4 m).** The same terra-cotta wall, less ornamented, arcade
  continuing at street level; the tile eave and parapet run its length in the satellite,
  dropping to the lower wing partway along.
- **North — Grove Street (~35 m).** Plainer, back of house; tile eave and parapet continue.
- **North-east — the party wall** shared with City College of San Francisco at 1170
  Market. Blind. The site steps out 7.4 x 6.1 m here, and that step carries the site's
  northernmost point.
- **Above.** A large low-pitch **hipped roof** over the auditorium across the centre and
  north — light silver-grey, hipped at its west end, ridge running SW–NE. Along Market
  and Hyde the red tile pent roof caps the parapet with a flat strip behind it. The
  valley between wings and hip is packed with mechanical plant. At the **north-east
  corner the stage house** stands clear of everything: a pale flat-roofed box with a
  small rigging penthouse, the highest element at 27.2 m.

## 5. Heights: how 27.2 m was settled

There is no published architectural height for the Orpheum. 27.19 m is the 2010 city
LiDAR `hgt_max`, and it sits only 1.96 sd above the mean — the zone where a maximum can
turn out to be a parapet spike or a stray return. It survives four independent checks:

1. **The published grid height.** The 1998 rebuild raised the fly grid from 60 ft to
   75 ft (22.9 m) above the stage. A stage floor near street level plus the usual
   ~3 m of headroom over the grid puts the stagehouse roof at ~26–27 m.
2. **Photographs.** A distinctly taller stepped block stands behind the Market facade
   in every street-level view, with a flagpole on it.
3. **Satellite.** A large elevated flat-roofed mass at the NE with its own visible walls
   and cast shadow — a broad block, not a spike, which is what makes a LiDAR maximum
   trustworthy.
4. **Internal consistency.** `maxcm_1st − gnd_median` = 27.0 m independently.

The sub-element heights (23.3 m tall eave, 16.5 m wing eave, 25.7 m sign crown, 4.1 m
marquee soffit) are **photogrammetric**, ±1 m, measured off
`San Francisco Orpheum Theatre 01.jpg` — parallel verticals, so height is linear in
pixel row at fixed depth — calibrated on pedestrians at the lobby line and a 4.1 m
marquee soffit. The two that matter bracket the LiDAR median (21.47 m) and the LiDAR
mode (16.80 m) respectively, which is the only independent check available.

## 6. Recognition cues (ranked) and what was kept

1. The vertical ORPHEUM blade sign — **kept and exaggerated** (~15 % wider and deeper).
2. The marquee and its poster panel — **kept**, panel moved west of the blade as built.
3. Cream terra-cotta over a round-arched arcade under a red mission-tile eave — **kept**.
4. The step down along Market: tall corner block, taller entrance bay, lower NE wing — **kept**.
5. The hipped auditorium roof with the pale stage house above its NE corner — **kept**.

**Dropped:** every literal Plateresque relief (rosettes, grotesques, colonnette shafts,
cartouches, frieze figures), the barley-twist flutes, window mullion grids, pierced
oculi (kept as shallow recesses), the address plaque, the window air conditioners, the
street furniture. The ornament is translated into **rhythm and depth** — bay pitch,
proud piers, sill courses, an ornament band under the eave, recessed reveals — because
modelled literally it is 100k triangles that dissolve into grey noise at the app's
altitude.

## 7. Corrections to the plan (REPORT beats plan)

1. **OSM `height=46 m` is not a height.** DataSF records `p2010_zmaxn88ft` = 150.96 ft
   = 46.01 m — the roof's **absolute NAVD88 elevation**. Someone converted that to
   metres and tagged it as building height. The real height above ground is 27.19 m.
   A 19 m error, and the single trap on this building. The plan already flagged this;
   it is repeated here because it is the one thing a future editor must not "fix".
2. **The anchor moved 3.0 m east and 0.1 m south** of the plan's value, to
   **−122.4146087, 37.7793182**. The plan gave the *footprint* AABB centre; the loader
   places the GLB **origin**, and the contract puts the origin at the **model** bbox
   base-centre — which includes the 1.2 m tile eave overhang and the 4.2 m marquee and
   blade projecting over the Market sidewalk. The build script computes the shipped
   anchor from the model it actually exports.
3. **Shipped dims are 67.65 x 77.62 m**, not the plan's "≈ 64.7 x 75.0". Same cause:
   eave and marquee overhang. The walls still stand on the real footprint.
4. **The tall block wraps at 7 m depth, not 13 m behind Market.** A 13 m Market inset
   against a 6 m chamfer inset put the miter at their shared corner 12 m *outside* the
   building and inverted the whole band — the two offset lines meet at 34°, and mixed
   insets are only safe across near-right-angle corners. Uniform 10 m then collapsed the
   13 m chamfer's inner edge to 0.4 m. 7 m leaves a 3.7 m chamfer inner edge and is the
   value that ships.
5. **The north-east step-out is a separate solid.** It is concave, so a polygon
   containing it self-intersects under any inward offset, and it carries the site's
   northernmost point. `CORE` is the convex remainder; `NE_ANNEX` restores the step;
   `CORE + NE_ANNEX` is the real outline exactly. Clipping it would have shortened the
   building 5 m; straightening the flank to reach it would have trespassed 6.3 m onto
   1170 Market.
6. **Openings are applied, never cut.** There are no booleans here: the first pass built
   the arcade and windows as recessed prisms, which are simply buried inside the wall
   solid and render as nothing at all. Every opening now stands proud, and the depths
   only increase outward (pier 0.12 < reveal 0.08 … glass 0.18) so no surround shadows
   what it surrounds.
7. **The blade sign's frame moved to its long edges.** Full-height trim strips beside
   the letters made the sign read near-white by day — the exact opposite of a dark blade
   with bulbs. The beads now run down the blade's two long edges.
8. **`Toy_stone` is not used on the stage house.** It read as a second white mass against
   the cream. `Toy_sand` walls under a `Toy_trim` roof cap keeps the bright-box read from
   above without shouting from the street.
9. **The whole roof palette moved one step lighter, measured in the running app.**
   `Toy_roofd` (`#45454a`) renders near-black under the diorama light — a whole city
   block of it read as a hole in the first local QA, which the style bible forbids. The
   flat decks are therefore `Toy_steel`, the auditorium hip is `Toy_stone` one step
   lighter again (the satellite reads it as the light plane against darker decks, and
   that value break is what makes the roof legible from altitude), and `Toy_roofd`
   survives only on the small machinery units, where dark is right and the area is
   tiny. The plan's §2.8 table predates this; it was corrected from the app, not from
   a render.
10. **Camera preset changed to a southern view.** The plan proposed `yaw: 44` (camera SE,
    square onto Market). The blade sign's faces point NE and SW, so from the SE the hero
    cue is edge-on and invisible. `yaw: 0` puts the camera due south: the Market front is
    44° off-normal and the sign's SW face 45.9° off-normal — both read.

## 8. Exclusion measurement (for integration)

Measured against the geometry the bake actually consumes (DataSF + Overture, projected,
`simplifyRing(0.6)`), distances from the shipped anchor:

| Ring | Source | Area | Centroid | Nearest vertex |
|---|---|---|---|---|
| Orpheum `SF0351022` | DataSF | 2,883 m² | 6.11 m | 24.14 m |
| Orpheum `7ad3c2dc…` (OSM w35115840) | Overture | 2,967 m² | 7.28 m | 28.27 m |
| Civic Center Station `837db0e8…` | Overture | 6,944 m² | 66.18 m | **24.55 m** |
| City College 1170 Market `SF0351051` | DataSF | 578 m² | 33.64 m | 25.65 m |
| City College `e757eceb…` | Overture | 521 m² | 33.79 m | 28.27 m |
| 35 Fulton St sliver `876a881a…` | Overture | 29 m² | 38.66 m | 34.90 m |

`excluded()` drops a ring when its centroid **or any vertex** is inside the radius, so the
window is (7.28, 24.55). **`exclude: 20`** takes it with 12.7 m of margin on our side and
4.5 m on the neighbours'. Two rings drop, both ours — the normal DataSF-plus-Overture
double trace, not collateral. Point-in-polygon confirms the Civic Center Station strip
does not overlap the theatre footprint, so there is no unavoidable-collateral case here.

Residual: the 29 m² Overture sliver at 35 Fulton Street shares two vertices with the
north-east corner and survives, as a ~5 x 11 m, 11.6 m procedural nub against the party
wall. No single radius removes it without eating City College. If QA shows it, add
`extraExclusions: [{ lon: -122.4144084, lat: 37.7796474, r: 6 }]`, which catches that ring
on its own centroid and reaches nothing else.

## 9. Uncertainties

- Every sub-element height in §3 except 27.2 m is photogrammetric, ±1 m.
- Attribution of the LiDAR maximum to the stage house rather than the corner block's
  parapet is inferred from photographs; the number is the same either way.
- The **interior arrangement is inferred from the roof**, not from plans: the hip roof's
  position in the satellite and the stage house's position at the NE are what set the
  auditorium and stage placement. Priteca's 1926 drawings would settle it.
- The dark green of the sign and marquee is off-palette; `Toy_ink` is the substitute.
- Storey counts on Hyde and Grove are inferred — no photograph of those elevations was
  found at a usable angle.
