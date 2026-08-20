# Ferry Station Post Office Building — reference dossier

The **Agriculture Building**, 101 The Embarcadero at Mission Street, San
Francisco. NRHP #78000756 (listed 1 December 1978); contributor to the Port of
San Francisco Embarcadero Historic District (NRHP 2006).

Compiled 18 August 2026 for `artifacts/ferry-station-post-office/`. This
dossier records what was verified, how, and what is still inferred. It
supersedes `docs/asset-plans/ferry-station-post-office.md` wherever the two
disagree — the corrections are listed in §8.

---

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| NRHP nomination form, Pamela McGuire, 8 Feb 1978 (`npgallery.nps.gov/NRHP/GetAsset/feff6419-1b0b-49e6-ba3c-9bcb8d6a6ff4`) | Architect A. A. Pyle (State Dept of Engineering), structural drawings R. T. Alden; contractor Teichert and Ambrose; begun 30 Apr 1915; second-storey rear addition 1918; dolphin extension between ferry slips 7 and 8 begun 31 Jan 1919. **First floor 167 ft x 125 ft; second floor same width but only 85 ft deep.** Two-storey steel frame, tile hip roof, 12-inch long red pressed brick in Flemish bond with light mortar, granite base, artificial-stone details of cement-coloured French ochre, copper cornice. The principal facade's composition: central entrance, lesser entrances at each end set off "as if they were separate pavilions" by wide full-height piers of artificial stone; bracketed lintels over the end entrances; a **cast iron griffin and shield carrying a flag pole** over the central entrance; horizontal courses of artificial stone dividing the facade into a **high first floor and a squat second floor**; tall rectangular first-floor windows in brick architraves outlined in a recessed course of brick; **elaborate decorative brickwork panels between the square second-floor windows**. The rear's high ground floor "crowned with an artificial stone band". |
| NRHP asset metadata | Reference #78000756, architect `Pyle,A.A.`, significant year 1915 |
| Wikipedia, *Ferry Station Post Office Building* | Address 101 The Embarcadero; completed 6 May 1915; cost $31,981.50; enlarged 1918; post office until 1925, transport offices to 1933, state Agriculture Dept thereafter; **Amtrak's San Francisco terminal until March 2015**. Arch over the double entrance doors with a phoenix and a flagpole; upper storey with two terracotta shields and patterned brick panels. Its infobox coordinates are wrong — see §8.1 |
| NoeHill #78000756 | "The prominent trim on the brick building is **trompe l'oeil, not real stone**". Wood casement windows, iron doors in cast-iron casings. Three photographs, 26 May 2008 |
| Port of SF *Historic Piers RFI*, Aug 2018 | "two-story, pile-supported … riveted steel frame, reinforced concrete deck, beams, girders … brick-clad, terracotta-trimmed façade with a granite base, copper cornice, wood casement windows … iron door and clay tile roof". The phrase **"one-story east portion"** — the fact that fixes the rear massing |
| Port of SF Availability Report, May 2025 | Current use: Port office suites 310–6,000 sq ft at $4.05 psf/mo and interior storage at $2.00. *Observed (listing data)* |
| SF Chronicle, Nov 2018; Pacific Waterfront Partners RFI response | Unbuilt proposals: hotel or office with a one-storey glass addition, and raising the building ~8 ft for sea-level rise. **Not modelled** |
| OSM way/104599975 | The footprint ring used for all geometry here. Its `height=15 m` and `roof:shape=flat` are both wrong (§8.2) |
| DataSF `ynuv-fyni`, `sf16_bldgid` 201006.0001038, `mblr` SF9900278 | The height statistics (§3) and the polygon the city bake actually reads |
| Google Street View pano `PJ2Y60ERa8pqvq0e-Pwxlw` (2025), 37.79393616 −122.39254082, labelled "101 The Embarcadero" | The whole principal elevation. Used for the photogrammetric eave height (§3) and for a metric rectification of the facade (§5) |
| Street View panos `PX-RCbub6-akkld2ohlZGA` (NW, on the plaza) and `32-vZMNCrEPriUP4k5vL2g` (SE, on a ferry gangway) | The two flanks and the step from the two-storey front block down to the one-storey work room |
| Google satellite z20, stitched and rectified into the building's own (s, w) frame | The roof plan: the tile band and its hipped ends, the two flat decks, the three roof monitors, the light-well slot, the 1918/19 SE wing |

No copyrighted imagery is committed; the URLs and the measurements taken from
them are the record.

## 2. Location, footprint and orientation

Anchor (footprint axis-aligned bounding-box centre, which is what the loader's
origin convention needs): **lon −122.3921505, lat 37.7941368**.

The building stands on the bay side of the Embarcadero on its own
pile-supported wharf, at the foot of Mission Street, one short block SE of the
Ferry Building and immediately NW of the Downtown Ferry Terminal gangways.

Everything below is authored in the building's own **(s, w)** frame: `s` runs
along the Embarcadero frontage from the west corner, `w` runs inward from that
frontage. In that frame the footprint is exactly a **50.74 x 39.00 m rectangle
plus a 10.89 x 8.20 m bump-out** on the bay side at the SE end (the 1919 dolphin
extension) — 2,068 m2, against the projected OSM ring's 2,069.3 m2.

| Vertex | Blender X (east) | Blender Y (north) | (s, w) |
|---|---|---|---|
| V0 north corner | −2.43 | +31.87 | (0.26, 38.97) |
| V1 west corner | −34.10 | +9.15 | (0.00, 0.00) |
| V2 south corner | −4.25 | −31.87 | (50.72, 0.00) |
| V3 east corner | +34.10 | −4.36 | (51.04, 47.23) |
| V4 | +27.51 | +4.70 | (39.85, 47.22) |
| V5 | +20.83 | −0.10 | (39.80, 39.00) |

| Face | Length | Outward bearing |
|---|---|---|
| Embarcadero front (V1→V2) | **50.74 m** | **234.0°** |
| NW flank (V0→V1) | 38.97 m | 324.3° |
| SE flank (V2→V3) | 47.20 m | 144.3° |
| bump-out end (V3→V4) | 11.20 m | 53.9° |
| bump-out step (V4→V5) | 8.22 m | **324.3° — re-entrant; the centroid test returns the wrong normal here** |
| rear (V5→V0) | 39.54 m | 54.0° |

The NRHP's 167 ft (50.9 m) frontage and the measured 50.74 m agree to 0.3%; its
125 ft (38.1 m) original depth and the measured 39.00 m agree to 2.3%.

## 3. Height — how 12.65 m was arrived at

Nobody publishes a height for this building; Wikidata Q38251704 has none.

**The shipped height, 12.65 m, is the clay-tile hip ridge**, from DataSF LiDAR
`hgt_maxcm = 1265` over 8,886 half-metre cells. It is corroborated arithmetically
by the same record's absolute first-return peak: `peak_1st_m 15.83` −
`gnd_meancm 3.07` = 12.76 m. `peak_1st_m` sitting *just above* `hgt_max` rather
than far above it is the tell that no tree canopy overhangs the footprint, so
the maximum is real roof.

**The cornice/eave, 10.8 m ±0.3, was measured photogrammetrically.** Street View
pano `PJ2Y60ERa8pqvq0e-Pwxlw` sits 18.63 m off the perpendicular foot of the
frontage (solved from the footprint, not from the pano's reported position — the
two agree here: the 50.74 m frontage subtends 107.4° from that point, and the
observed silhouette spans 1,224 equirectangular columns = 107.6°). Fitting the
roofline silhouette against `elev = atan(h·cos θ / 18.63)` over 152 samples
across 60° of azimuth gives **h = 8.60 m above the camera, rms 0.32°**. The
camera height is 2.16 m, cross-checked against three pedestrians in the same
frame (heads 1.71 m above their feet at the same solved distance). An
independent reading at the NW corner — top edge at 15.51° elevation, D = 31.33 m
— gives 8.69 m above camera, 0.09 m from the fit.

**The two flat decks, 9.80 m and 6.60 m, are inferred** from the same LiDAR
record's median (`hgt_median_m 9.80`) and mode (`hgt_majoritycm 666`), and are
what the documents describe: the two-storey block is 85 ft (25.9 m) deep against
a 125 ft first floor, and the Port calls the rear a "one-story east portion".

Full LiDAR record: mean 8.72 m, median 9.80, mode 6.66, min 0.42, max 12.65,
σ 2.67 over 8,886 cells; ground 3.07 m NAVD88 mean (median 3.11, σ 0.32, min
1.07 — the low tail is the bay under the wharf edge).

**Residual tension, recorded honestly.** The massing as built implies an
area-weighted mean of about 9.6 m against the reported 8.72 m, and a median
nearer 10.5 m than 9.80 m. Both errors point the same way: the real roof has
more low area than this model. Two things explain part of it — the DataSF
polygon is 2,221 m2 against the ring's 2,069 m2, so roughly 7% of its cells are
eave-overhang cells that sample the wharf deck (`hgt_min 0.42 m`), and the
sloped tile planes spread across bins rather than concentrating in one. What the
LiDAR pins hard is the **maximum**, and that is the number the asset ships.

## 4. What each side shows

**South-west — the Embarcadero elevation, 50.74 m.** The subject. Granite base;
a high first floor of tall rectangular windows in recessed brick architraves; a
deep horizontal terracotta string course; a squat second floor of near-square
windows with ornamental brick panels between them and two carved terracotta
shield panels flanking the centre. Full-height rusticated terracotta corner
quoins; terracotta end-pavilion entrances under bracketed lintels; wide
full-height terracotta piers setting those pavilions off; a terracotta central
pavilion with a grilled transom over double iron-framed doors, the cast number
**101**, the phoenix-and-shield ornament and an out-thrust flagstaff. Dark
copper cornice the whole length, clay tile above it.

**North-west flank, 38.97 m.** The finished design returns for the depth of the
two-storey block, then drops to the one-storey work room with a plain brick
parapet, service doors and openings, looking onto Harry Bridges Plaza. The step
from two storeys to one is plainest from here.

**South-east flank, 47.20 m.** The front block, then the 1918/19 addition
running back along the flank as a narrower two-storey tiled-hip wing over the
former driveway, out to the bump-out over the ferry slips. A recessed light-well
slot separates that wing from the central block.

**North-east rear, over the water.** Utilitarian: the work room's brick rear
wall, roll-up and service doors, parapet with its terracotta coping.

**Above.** A tiled hip band 16.6 m deep across the whole frontage, hipped at
both ends, ridge 8.3 m in; a flat deck at 9.80 m behind it over the middle of
the frontage only; a larger flat work-room deck at 6.60 m carrying three
light-topped roof monitors and a mechanical scatter; a dark light-well slot; and
the SE wing's own tiled hip. Terraces, not a box.

## 5. The facade, measured

A metric rectification of the Street View equirectangular panorama onto the
facade plane (22–46 px/m) gave the composition directly. Positions are metres
from the west corner, made exactly symmetric about the frontage centre (25.37 m)
after measurement, since the building is symmetric and the rectification drifts
~1.2 m toward the far end.

| s0 | s1 | element |
|---|---|---|
| 0.00 | 2.10 | rusticated terracotta corner quoin |
| 2.10 | 6.80 | NW end-pavilion terracotta surround; door centred 4.45 |
| 6.80 | 9.00 | wide full-height terracotta pier |
| 9.00 | 21.57 | brick field A — 3 window bays |
| 21.57 | 29.17 | central terracotta pavilion; door centred 25.37; shields at 23.00 and 27.74 |
| 29.17 | 41.74 | brick field B — 3 window bays |
| 41.74 | 43.94 | wide full-height terracotta pier |
| 43.94 | 48.64 | SE end-pavilion surround; door centred 46.29 |
| 48.64 | 50.74 | corner quoin |

Measured window pitch within a field was 4.6 m; the model uses even thirds
(4.19 m) for a clean toy rhythm. Vertical bands, all rectified measurements:
granite base to 1.00; first-floor windows 1.90–5.30; terracotta string course
5.70–6.70; second-floor windows 7.40–9.50; copper cornice 10.20–10.80.

## 6. Recognition cues (ranked)

1. The wide clay-tile hip roof over a long brick two-storey block on the water,
   one block from the Ferry Building.
2. The three-pavilion terracotta-and-brick front.
3. The stepped roof section — tile band, mid deck, work-room deck.
4. The entrance ensemble: transom, phoenix shield, out-thrust flagstaff.
5. The two-band fenestration with ornamental panels between the upper windows.

## 7. Kept, simplified, dropped

**Kept:** tile hip band and its hipped ends; the three-pavilion rhythm and its
rustication courses; granite base; cornice line; both window bands; the string
course; shield panels; the entrance with its flagstaff; the roof monitors; the
light-well slot; the SE wing; the parapet copings.

**Exaggerated:** nothing beyond what the geometry gives. The roof pitch came out
at 12.3° from the measured 16.6 m band and the 1.85 m eave-to-ridge rise, which
is already enough for the hip to read from above — no further steepening was
needed, and none was applied.

**Simplified:** Flemish bond → flat brick colour; trompe-l'œil ashlar → thin
proud course lines on the terracotta blocks; the elaborate brick panels → a
shallow recessed panel with a terracotta lozenge; the phoenix-and-shield → one
chunky gold plaque on a terracotta ground; wood casement muntins → flat dark
glass; cast-iron door frames → a plain reveal.

**Dropped:** fire escape fine members; wall lanterns; downpipes; the
"THE EMBARCADERO" street blade and traffic signals (street furniture, not
building); the ferry gangways, canopies and pontoons; everything outside the
footprint ring.

## 8. Corrections to the plan, and uncertainties

1. **Wikipedia's coordinates are wrong by ~90 m** (it gives −122.39111). The
   measured anchor is −122.3921505, 37.7941368. *Resolved.*
2. **OSM `height=15 m` and `roof:shape=flat` are both wrong.** 15 m is 2.35 m
   above the LiDAR crest; the roof is a clay-tile hip, per the NRHP nomination,
   the Port's own description and nadir imagery. *Resolved — neither tag used.*
3. **The plan said the wharf bump-out was an open concrete apron. It is not.**
   The rectified roof plan shows the 1918/19 SE wing's tiled hip roof covering
   the bump-out out to w = 47.2 m, with a hipped end. The model was changed to
   match and the apron was dropped; there is no open deck inside the footprint.
4. **The plan said the two-storey block runs the full frontage to 25.9 m deep.**
   The rectified roof plan shows it doing so only over s 9.0–36.5; at both ends
   the work-room deck runs from the tile straight back to the bay, which is
   where the three roof monitors sit. The model follows the imagery. This also
   moves the model toward the LiDAR summary rather than away from it.
5. **The plan called for the tile roof to be clearly darker than the brick.**
   The imagery says otherwise — the clay tile is a *lighter, more saturated*
   terracotta than the deep red brick. The value ladder actually used is
   brick (mid) / tile (mid, more saturated) / terracotta trim (light), separated
   at the roofline by the dark copper cornice. Checked in the aerial render.
6. **The SE wing's dimensions remain the softest number.** Its 10.74 m width and
   ~30.6 m run come from the nadir tile mask, which suffers parallax on a
   12.65 m building; the wing's own eave (9.40 m walls, 9.90 m cornice, 11.05 m
   ridge) is an estimate constrained only by "lower than the front block, higher
   than the work room" plus a shadow-length reading of ~3.8 m onto the adjacent
   deck. The satellite tile mask also *misses* this wing's tile entirely because
   it is in shadow — the rectified visual, not the colour classifier, is what
   establishes it.
7. **The 9.80 m mid deck is inferred**, from the LiDAR median plus the NRHP's
   85 ft second-floor depth. No photograph in the source set looks straight down
   on it.
8. **The building may be raised ~8 ft** and given a glass storey under Port
   proposals. None is built; the asset is the building as it stands.
