# 500 Third Street — reference dossier

Research behind `build_500_third.py`. Compiled 13 August 2026 for the
`pipeline/500-third` session. Everything here was re-verified in this session
against primary data (OSM, DataSF, city LiDAR, geolocated photography); where it
differs from `docs/asset-plans/500-third.md` this file wins, and `REPORT.md`
wins over both.

## 1. What the building is

A five-storey reinforced-concrete industrial loft of 1927 occupying the whole
quarter block bounded by 3rd Street, Bryant Street, Ritch Street and a surface
parking lot, in South Beach / SoMa. Roughly 140,000–150,000 sf over a 2,795 m²
footprint; assessed as industrial, used as multi-tenant creative office. The
long-standing tenant Organic Inc. gives the corner crown its sign.

It is the canonical SoMa concrete-loft type: a light concrete frame that is more
window than wall, a charcoal storefront base, a flat parapet, and no ornament
beyond pilaster strips and a belt cornice.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/147508936](https://www.openstreetmap.org/way/147508936) | Footprint geometry (4 corners), `addr:housenumber=500`, `addr:street=3rd Street`, `building=commercial`, `height=23` (source: Bing) |
| [DataSF DBI permits](https://data.sfgov.org/resource/i98e-djp9.json) `block=3776&lot=115` | 100 records, 1990–2022. Storey counts (5 in most 2012–2021 records, 6 in the 2014 records), construction type 1/2, the 1993 concrete-parapet seismic bracing, the 1998 reroof, the 2001 window-to-roll-up-door conversion, the 2014 fire-escape ladder repair, the 2015 rooftop antenna + weather sensor + equipment cabinet, floor-by-floor office TIs on floors 1–5 |
| [DataSF 2010 LiDAR building footprints](https://data.sfgov.org/resource/ynuv-fyni.json) `mblr=SF3776115` | 11,323 half-metre cells ≈ 2,831 m² (corroborates the OSM polygon); ground mean 5.64 m NAVD88, range 0.97 m; height median 22.74 m, mean 23.02 m, **max 26.62 m** |
| [PropertyShark parcel record](https://www.propertyshark.com/mason/Property/30534806/500-3-St-San-Francisco-CA-94107/) | Built 1927, "6" stories, 140,375 sf building, 31,929 sf lot, class B masonry/concrete, industrial use |
| [Cushman & Wakefield listing](https://www.cushmanwakefield.com/en/united-states/properties/for-lease/office/ca/san-francisco/500-third-street/s234823-227627-l) | 1927, ~150,000 sf, class C, SOMA |
| Google Street View, 2025 imagery | All four elevations, the corner crown and its sign, the flag masts, the storefront and "500 THIRD" entry signage. Panoids: `ZFJr8xIGkghVJpdM2pRWOg` (3rd St, opposite the entry), `qpFsB9_v9E-B6X37FmAqQA` (Bryant St), `6Hg1dMtfmyUJp_yT_3roQQ` (Ritch St), `VG7suaG1CGPCMYyyOi0dmQ` (SE parking lot), `d6j41Ahotp0p7DDR8aQ7dg` (3rd × Bryant corner — the whole block in one frame), `BNesNZmzyPdbYOhIibJ-Yg` (3rd St, south end) |
| Esri World Imagery (`services.arcgisonline.com/.../World_Imagery/MapServer/export`) | Roof plan: the bulkhead near the centre-north, a dozen small mechanical units and duct runs across the south half, a flat pale membrane field, parapet line |
| [Overpass API](https://overpass-api.de/) `way(around:90,…)["highway"]` | Which street is on which side, measured edge-by-edge: 3rd 13 m off the NE edge, Bryant 12 m off the NW edge, Ritch 5 m off the SW edge, an unnamed service way 12 m off the SE edge |

No architect attribution was found in any accessible source. Treated as unknown
rather than guessed.

## 3. Verified dimensions and location

Projected with the app's tangent projection (LON0 −122.4375, LAT0 37.77),
recentred on the footprint AABB centre. x east, y north, metres, CCW:

```
A  ( -4.197,  37.788)   north corner  (3rd × Bryant)
D  (-37.293,   3.465)   west corner   (Bryant × Ritch)
C  (  3.933, -37.788)   south corner  (Ritch × SE lot)
B  ( 37.293,  -3.587)   east corner   (SE lot × 3rd)
```

| | |
|---|---|
| Anchor (AABB centre) | −122.3958224, 37.7808279 |
| Vertex mean | −122.3958231, 37.7808276 — 0.07 m away, so the choice of centre is immaterial |
| Area | 2,790 m² by shoelace; LiDAR cell count gives 2,831 m² |
| Parapet height | **23.0 m** — OSM `height=23` and LiDAR median 22.74 / mean 23.02 agree |
| Crest | **26.5 m** — LiDAR max 26.62 m, the rooftop bulkhead |
| Grade | 5.64 m NAVD88 mean, 0.97 m range: flat |

| Edge | Length | Outward normal (true) | What it is |
|---|---|---|---|
| A → D | 47.68 m | 314.0° | Bryant Street front |
| D → C | 58.32 m | 225.0° | Ritch Street service rear |
| C → B | 47.78 m | 134.3° | SE elevation over the parking lot |
| B → A | 58.59 m | 44.9° | 3rd Street front (the address side) |

## 4. Orientation decision

Authored with Blender +Y = true north, +X = east, so the model drops in at its
real heading and the loader (`placeGeneric` in `app/src/assets.js`) applies no
rotation. The contract's "front faces −Y" cannot be honoured: the real front
faces north-east at 44.9°. Real-world orientation wins (AGENTS rule 5).

## 5. What each side shows

**North-east — 3rd Street, 58.6 m, nine bays.** Warm-grey painted concrete frame.
A tall charcoal storefront ground floor: deep bays of dark-framed glazing over a
low solid base, split by pilasters with simple moulded capitals, and a recessed
main entry near the middle with metal "500 THIRD" letters on its head beam. A
strong light band caps the ground floor. Above it four identical floors, each
structural bay holding one large steel-sash window — a fine grid of small panes
in dark frames — set back behind narrow pilaster strips over a light sill band. A
steel fire escape hangs on the southern part. Plain light parapet with a row of
slender flag masts standing on it.

**North-west — Bryant Street, 47.7 m, seven bays.** The same elevation with two
fewer bays; the ground floor reads as very tall glazed bays over a solid base
rather than as shopfronts. The corner crown carries the sign on this face too.

**South-east — over the parking lot, 47.8 m, seven bays.** The plainest glazed
face: solid painted base, then the same four window bands, a couple of
through-wall air-conditioners, a wall light. No entry. Because the neighbouring
lot is open parking, this elevation is fully exposed to the app's camera and is
modelled as a real facade.

**South-west — Ritch Street, 58.3 m.** The service rear, almost blind:
cream-painted concrete, a roll-up vehicle door (numbered 211 Ritch), a personnel
door, a large louvre panel, exposed conduit, and small punched windows instead of
big sashes. The south corner of the block is a tall blank wall.

**Top.** A pale flat membrane field: the bulkhead penthouse near the centre-north
(the crest), a smaller overrun beside it, a cluster of small mechanical units and
duct runs over the southern half, the 2015 antenna and its cabinet, the flag
masts on the two street parapets, and the raised capped crown at the north
corner.

## 6. Recognition cues (ranked)

1. The steel-sash window grid, repeated identically across three elevations.
2. The block itself: a near-square 58 × 48 m, five-storey prism at 45° on its own
   quarter block, open ground on two sides.
3. The charcoal storefront base under the light frame — the strongest value
   contrast on the building.
4. The raised, signed corner crown at 3rd and Bryant, lit at night.
5. The flag-mast row along the street parapets.

## 7. Preserved / simplified

**Preserved:** the true polygon and 45° heading; five storeys (tall ground floor
≈5.6 m, four uppers of 4.0 m); the 9 / 7 / 7 bay rhythm; the 23.0 m parapet and
26.5 m crest; the blind service character of Ritch Street; the crown's extra
height and its two sign faces.

**Simplified:** each window becomes one `Toy_glass` slab in an `Toy_ink` reveal
with a single mullion cross — the real sashes are roughly 8 × 6 panes, which at
city distance is noise (style bible §5); pilasters and sills are slightly wider
than scale so the grid still reads at 200 m; the ground floor is one continuous
charcoal band with glazed bays and one recessed entry, no capitals or mouldings;
the "500" numerals are oversized (§8); the corner sign is a plain illuminated
panel, not lettering; the mechanical cluster is eight identical boxes on a curb.

**Dropped:** the fire escape — thin diagonal steelwork is precisely the detail
the style bible tells us to strip; the through-wall air-conditioners; the real
mullion counts.

## 8. Night composition

A dark grey block with a lit corner. Hero: the crown sign band on both faces.
Supporting: fifteen scattered lit upper bays (one in four, never a whole floor)
so the building reads as occupied rather than as a light box. Ground cue: the
entry transom and the two lobby bays flanking it. Nothing else lights — the
Ritch Street rear is dark, as it is in life.

Glow shells are thin surfaces standing proud of the opaque glazing behind them;
`assets.js` renders `_Glow` in a separate layer at ~12% alpha by day, so no
primary surface is authored as glow.

## 9. Uncertainties and conflicts

- **Storey count.** The assessor says 6; DBI permits say 5 in most records and 6
  in two 2014 records; every photograph of every elevation shows one tall ground
  floor plus four upper window bands, and that division fits the measured 23 m
  parapet exactly. Modelled as 5, with the "6" read as a count including the
  ground floor's mezzanine (permits do reference first-floor mezzanine work).
- **The bulkhead** is sized from one Esri aerial and its height from a single
  LiDAR maximum cell. If it turns out smaller or lower, `targetHeightM` moves
  with it and nothing else in the model does.
- **Bay counts** (9 / 7 / 7) are counted from oblique Street View frames, not
  from a drawing.
- **Paint colour** reads warm grey on 3rd and Bryant and cream on Ritch in the
  available imagery; treated as one warm grey shell, since the difference is
  consistent with sun versus shade in those panoramas.
- **The antenna mast** is a design decision standing in for the 2015 permit's
  rooftop antennas, weather sensor and cabinet, which no aerial resolves.
- OSM `height=23` and the LiDAR median describe the **parapet**, not the crest.
  Neither is the target height.
