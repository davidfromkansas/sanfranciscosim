# 252–254 Ritch Street — reference dossier

Compiled 18 August 2026 for the SF-SIM miniature asset. This is the modelling
record: what each source establishes, what was measured, what was inferred, and
what the plan (`docs/asset-plans/254-ritch.md`) got wrong.

Reference photographs are **not committed**. They are 2025 marketing photography
(© Elite Studios LLC, via the Compass / Allison Chapleau offering memorandum) and
only their URLs and descriptions belong in this repo.

---

## 1. What this building is

A 1915 two-flat at 252–254 Ritch Street, San Francisco 94107 — one of the SoMa
alleys between Bryant and Brannan. Two storeys over a raised base, flat roof,
7.60 m of frontage on a 25 × 78 ft lot. Two units, nine rooms, classified by the
assessor as Flats & Duplex / Multi-Family Residential in every roll year on
record. Sold October 2025 for $1,250,000 against a $995,000 list.

It is not a monument and has no architect on record. It is in the manifest
because it is *legible*: the whole building is painted one dark warm grey on a
block of cream neighbours, and the lot to its south-east is a surface parking
lot, so three of its four elevations are public.

## 2. Sources

| Source | What it establishes | Confidence |
|---|---|---|
| DataSF `acdm-wktn` parcel `3776106` | the surveyed lot: 7.601 m frontage, 23.91 m deep, 181.7 m²; address range 252–254; zoning SLI | measured |
| DataSF `acdm-wktn` parcel `3776105` | 248–250 Ritch, the party-wall neighbour to the north-west; used to show the footprint offset in §4 is systematic | measured |
| DataSF `ramy-di5m` addresses | 252 and 254 resolve to one coordinate and one parcel | measured |
| DataSF `wv5m-vpq2` assessor roll, block 3776 lot 106 | built 1915; 2 storeys; 2 units; 9 rooms; 2,100 sq ft; lot 1,875 sq ft | published |
| DataSF `ynuv-fyni` footprint `201006.0125003` | 102.9 m² outline; ground 18.50 m NAVD88; `hgt_median_m` 8.04; `hgt_maxcm` 881; `hgt_mincm` 213; σ 1.18 m | measured |
| DataSF `3psu-pn9h` centrelines, `street=RITCH` | the Bryant→Brannan block runs 135.05°, addresses 200–299 | measured |
| OSM way `147508935` | `addr:housenumber=252;254`, `height=8`, `source=Bing` | corroboration only |
| Overture (repo copy, 2026-08-13) | the ring at this site is the OSM way verbatim: 100.0 m², height 8.0 | measured |
| Offering memorandum PDF (URL in the plan §2.2) | five exterior frames: a near-orthographic street elevation, a high three-quarter aerial, an oblique reading the whole roof, a wide aerial showing the exposed flank, and a **true top-down drone frame** | observed (listing photo) |
| Compass / Allison Chapleau listings | 2 × 1BD/1BA, upper unit vacant at sale, large basement, in-unit laundry, "well-maintained" | published |
| Augrented `3776106` | assessor-derived ownership and sale history (Ritch Street LLC, prior sale 1996) | secondary |

## 3. Verified dimensions and location

| Item | Value | How |
|---|---|---|
| Frontage | **7.60 m** | surveyed parcel front edge |
| Built depth | **14.2 m** | LiDAR footprint 0.64–15.23 m behind the property line, front extent read as cornice overhang, wall plane taken at 1.00 m |
| Footprint | 108 m² | derived |
| Roof deck | **7.95 m** | LiDAR median 8.04 m, flat roof |
| Tallest point | **8.80 m** | LiDAR maximum 8.81 m |
| Facade heading | **45.05°** (north-east) | perpendicular to the 135.05° street centreline; confirmed against the parcel's front edge (135.05°) |
| Manifest anchor | `-122.3956316, 37.7801280` | the model's XY bbox centre after recentring |
| Design anchor | `-122.3956361, 37.7801244` | the wall-box centre, 0.56 m south-west of the above |

**Photogrammetric height check.** Using the 7.60 m frontage as a horizontal
scale bar on the straight-on listing elevation (110 px/m), the roof edge reads
7.8 m above the sidewalk and three facade-plane features land within 5 cm of the
design section: the entry-hood crest / floor line at 4.27 m (design 4.30), the
upper sill at 5.14 m (design 5.15) and the upper head at 6.89 m (design 6.85).
A first attempt using the entry door as the scale reference gave 11.9 m and was
discarded: the doors sit ~1.5 m back inside a recess and the camera was elevated,
so the reference was both farther away and lower than the plane being measured.

## 4. Orientation and placement — the one real decision

Three geometries exist for this building and they do not agree. Measured in the
lot frame (origin at the parcel's north-west front corner, *along* positive
toward Brannan, *setback* positive away from the street):

| Source | along | setback |
|---|---|---|
| parcel `3776106` (ours) | −0.12 … 7.60 | 0.00 … 23.92 |
| parcel `3776105` (248–250) | −7.72 … 0.00 | 0.00 … 23.91 |
| DataSF footprint (ours) | −1.28 … 6.70 | 0.64 … 15.23 |
| DataSF footprint (248–250) | −8.93 … −1.21 | 0.54 … 24.35 |
| OSM / Overture | −2.33 … 5.57 | 2.74 … 16.55 |

The two parcels share a party line at along 0; the two footprints share one at
along ≈ −1.24. Both footprints are therefore shifted ~1.2 m north-west of the
survey, **in step with each other** — a registration offset in the footprint
layer, not a defect in either polygon. OSM is offset a further ~1.1 m along and
~1.7 m back from the street on top of that, and is rejected for placement.

**The asset is placed in the DataSF footprint frame.** Everything it will stand
next to in the app is baked from those footprints, 248–250 Ritch included, and
248–250 is not excluded. Anchoring on the surveyed parcel would be 1.2 m more
correct in absolute terms and would open a 1.2 m slot between this asset's party
wall and its neighbour's — the one error the aerial camera would actually see.
The parcel-frame anchor, if this is ever revisited, is `-122.3956253, 37.7801171`.

## 5. What each side shows

**North-east — Ritch Street, 7.60 m, the public face.** Horizontal lap siding
over a raised base band, all one dark warm grey. The south-east 3.68 m is a
two-storey canted bay projecting 0.60 m with 45° cheeks: three double-hung
sashes per storey (narrow cheek, wide centre face, narrow cheek), a small
cornice at the bay head and a flared skirt into the base. The north-west 2.28 m
carries one double-hung window upstairs and, at ground level, a deep entry recess
holding **two** part-glazed doors — 254 to the south-east, 252 to the north-west,
the numbers painted on the reveals — under a small bracketed hood at the floor
line. A straight six-step stoop with a solid cheek wall on its south-east side
climbs from the sidewalk. Over everything, a bracketed cornice: a dentil course
under widely spaced modillion blocks, projecting ~0.35 m, returning over the bay.

**South-east — the exposed flank, 14.2 m.** The neighbouring lot is a surface
parking lot, so this whole elevation is public. Blind: flat siding, a downpipe,
and one rectangular recess where the south-east light well opens, 4.2–7.8 m back
from the front wall. Its value is that it exists — the building reads as a
free-standing object on this side, which almost nothing else on the block does.

**North-west — party wall against 248–250 Ritch, 14.2 m.** Blind. The neighbour
is a two-storey cream building of about the same height with its own bay
(DataSF `201006.0040021`, `hgt_median_m` 7.95).

**South-west — rear.** Faces the rear yard, visible only from the air. **Entirely
unverified**: no source shows it. Modelled as a door and two windows.

**Top — the surface the app's camera actually sees.** A flat pale membrane
(measured `#cac8c9` overcast, `#c3bdb8` sunlit) clearly lighter than the walls,
bounded on the street side by the cornice band with the bay's chamfer notched
into it. Two light wells cut through it, measured off the top-down drone frame
against the 14.2 m roof as a scale bar (good to ~0.3 m):

- **Well A**, 1.1 m (deep) × 2.1 m (wide), hard against the party wall,
  7.0–8.1 m back from the front wall
- **Well B**, 3.6 m × 1.4 m, notched into the exposed flank, 4.2–7.8 m back

Between them, mid-roof and ~3.8 m from the party edge, a mechanical cluster: a
mini-split condenser on a low stand, a mushroom vent and a small equipment box.
Near the party wall about 9 m back, a capped flue — the tallest object.

## 6. Recognition cues (ranked)

1. **The monochrome dark grey**, against a block of cream neighbours.
2. **The two-storey canted bay** taking half of a 7.6 m frontage.
3. **The exposed south-east flank** — a small building standing free.
4. **The pale roof against the dark walls**, with two dark wells punched through.
5. **The bracketed cornice**, the only ornament.

## 7. Preserve / simplify

**Preserve** — the 7.60 × 14.2 m footprint and the 45.05° heading exactly; the
dark monochrome on every painted surface; the bay's share of the frontage and
its projection; **two** doors in one recess; both light wells at their measured
sizes; the value inversion between roof and walls.

**Simplify** — clapboards become flat colour with one shadow groove at the floor
line; the dentil course and modillions become three corbelled cornice steps (the
blocks are sub-pixel at this scale, the *projection* is what reads); windows
become recessed rectangles with proud sills and surrounds; the stoop loses its
railing; the flue is exaggerated to a chunky 0.35 m cylinder; overhead wires, the
utility cabinet, gas meters, landscape boulders, downpipe and satellite dish all
disappear; the rear yard is not modelled.

## 8. Corrections to the plan, made at stage 2

1. **The manifest anchor and the registry point are NOT the same**, as the plan
   §2.3 predicted they would be. Recentring the model on its XY bbox centre moved
   the origin 0.56 m north-east, because the bay, the cornice and the stoop all
   project toward the street and the rear does not. Manifest anchor
   `-122.3956316, 37.7801280`; registry `lon`/`lat` stays at the design point
   `-122.3956361, 37.7801244`, which is where the exclusion window was measured.
   `exclude: 2.9` is unaffected — re-measured from the design point, the window
   is still 1.95 m < r < 3.82 m.
2. **`Toy_slate` is off-palette by design** (`#756f69`). See REPORT.md.
3. The light wells are modelled as **upper-storey shafts**, plugged back to solid
   below 4.70 m. The plan's plan-bite construction, taken literally, ran them the
   full height of the wall.

## 9. Uncertainties

- **The tallest rooftop object is measured but not named.** `hgt_maxcm` is
  computed over this footprint's own cells, so something here reaches 8.81 m; the
  capped flue is the most plausible candidate from the oblique frame but it could
  belong to 248–250's roof.
- **The assessor's 2,100 sq ft does not reconcile.** 195 m² over two storeys
  implies a 12.8 m depth; LiDAR measures 14.6 m and OSM 13.8 m. The listing
  separately advertises unit 254 alone as ~1,700 sq ft, which cannot fit inside
  2,100 sq ft for the whole building. The assessor figure is the outlier.
- **The rear elevation is invented** within the constraints of the type.
- **The light wells' 3.0 m depth is a guess**, constrained only by `hgt_mincm`
  = 2.13 m. Read as holes from above, the depth barely matters.
- **"Studio 254" is a red herring.** Several directories list a recording studio
  at this address and Ritch Street's alley blocks did host studios. The assessor
  has classified the parcel as residential in every roll year on record and the
  2025 sale was as a 2-unit residential building. No commercial ground floor, no
  roll-up door, no signage.
- **All five exterior photographs come from one 2025 marketing shoot** — one
  photographer, one day, one set of colour decisions. The measured `#6b696a`
  inherits that grade.
