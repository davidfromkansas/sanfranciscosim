# 226 Ritch Street — reference dossier

Compiled 18 August 2026 for `artifacts/226-ritch/`. This is the *modeller's* record:
what was looked at, what it established, and where the plan
(`docs/asset-plans/226-ritch.md`) turned out to be wrong. Where this file and the
plan disagree, **this file and `REPORT.md` win**.

## 1. What the building is

226 Ritch Street Condominiums — eight live/work lofts on a 3,146 sq ft infill lot
on the south-west side of Ritch Street, the one-block alley between Bryant and
Brannan in SoMa. Permit `9420930s` (filed 1994, $400,000, "Erect a three story
nine unit live/work structure", new construction wood frame) was revised in 1995
(`9516754`, Type II → Type V/1-hr, "Bldg ht reduced") and one dwelling unit was
eliminated in 1996 (`9600830`), leaving the eight units DataSF lists today
(101-103, 201-203, 301-302). Assessor and MLS records date it 1996.

Each unit is a double-height loft with a mezzanine — the listings' "15-foot
ceilings … like all true lofts, the upper level is partially open to the level
below" — which is why a three-storey building stands 16 m tall. Ground floor is a
garage (the laundry is in it); the HOA fee includes an elevator. Unit 302 is
marketed as a penthouse with four private balconies.

No architect could be attributed. **Santos Prescott's *Ritch / Zoe Studio* (1998)
is a different building** on the same alley — a concrete warehouse conversion with
frontage on both Ritch and Zoe and a carved courtyard. It shares nothing but the
street name and it must not be credited here.

## 2. Sources and what each established

| Source | Established |
|---|---|
| OSM way `148217483` via Overpass (geometry + tags) | a 20.18 x 12.10 m footprint ring, `addr:housenumber=226`, `height=16` |
| DataSF *Building Footprints* `ynuv-fyni`, footprint `SF3776120` | the 21-vertex survey ring (22.80 x 12.13 m OBB, 251.5 m2), the LiDAR height distribution, ground at 5.59 m NAVD88 |
| DataSF *Addresses with Units* `ramy-di5m` | the eight condo units and parcels 3776120-3776127; the neighbours at 212/218 Ritch (NW) and 230/234/236 Ritch (SE) |
| SF DBI permit record (checkpermits.com, openpermitdata.com) | 1994 new construction; 1995 type/height revision; 1996 unit elimination; 1997 "fill-in 2 windows on 2nd flr, mezzanine level 2 south side"; **1998 vinyl siding to the rear & north sides ($22,000) and to the "left side of house not visible" ($10,000)**; 2005 stucco work at unit 302; 2006 "remove stucco around perimeter of deck (10x12) approx 12 up"; 2005 and 2024 reroofing |
| MLS 422635708 / 422696775 / 424073376 | 1996, 3 storeys, 8 units, 15-ft ceilings, mezzanines, 3,146 sq ft lot, garage, penthouse with four balconies, elevator |
| Google Street View pano `ghoSOzaNSJJK1wpjaYBtwA` ("226 Ritch St"), plus `3MCsiT2LemwvFtwJsgkTxA` and `cKwbxtiKXSiLVgZ5RJ_uFQ` up and down the alley | the **entire** north-east elevation — palette, opening positions, the fire escape, the roof railing — and the street context |
| Google satellite imagery, z21 | the roof inventory: membrane, a row of round skylight domes, a tiled deck, small raised boxes. Registration against the survey rings is off by ~3 m |
| Esri World Imagery, z20 | attempted as registration control; too soft at this scale to resolve roof objects. Not used |

No Wikipedia, Wikidata or architectural-press entry exists for this building.

## 3. Dimensions, location, orientation

| | |
|---|---|
| Anchor | `-122.3960899, 37.7804376` — DataSF `SF3776120` oriented-bounding-box centre |
| Footprint | 12.13 m frontage x 22.80 m depth, 251.5 m2 |
| Frontage bearing | 135.6° / 315.6° (along Ritch Street) |
| Front face outward normal | **45.6° — north-east, onto Ritch Street** |
| Main street parapet | **16.00 m** |
| Roof crest (stair bulkhead) | **18.10 m** |
| Ground | flat: LiDAR ground 5.27-5.72 m NAVD88 across the footprint |

**Which side faces the street was measured, not assumed.** Ritch Street's OSM
centreline (way 8917138) passes (3625.1, −1197.8) → (3675.5, −1147.3) in app
metres. The perpendicular from the anchor to that line is 17.3 m long and its foot
vector is (−12.3, +12.2) — west and south of the centreline. So the building is on
the **south-west** side and its front faces north-east. The front wall stands
~7.3 m out from the centreline.

**How the parapet height was established — three independent ways.**

1. OSM `height=16`.
2. DataSF LiDAR over `SF3776120`: `hgt_median` 15.90 m, `hgt_mean` 15.99 m,
   `hgt_std` 1.71 m, `hgt_min` 6.43 m, `hgt_majority` 17.63 m, `hgt_max` 18.14 m,
   1,018 cells at 50 cm.
3. Street View photogrammetry. Pano `ghoSOzaNSJJK1wpjaYBtwA` was pulled as a
   levelled 4096 x 2048 equirectangular. The yaw offset was calibrated against the
   two front-corner bearings computed from the footprint (179.8° and 265.1° from
   the pano's reported position); **both fitted the same 49.8° offset**, which
   corroborates the pano's position rather than condemning it. The perpendicular
   distance from lens to facade plane is then 6.5-6.7 m; the parapet subtends
   64.3° of elevation at the perpendicular foot and the pavement −17.0°, giving a
   facade height of 15.5-16.0 m for a camera 2.0-2.05 m above the pavement. The
   facade was then resampled into a metric 60 px/m rectified elevation, and every
   horizontal dimension in §4 is read off that.

## 4. What each side shows

**North-east — Ritch Street front, 12.13 m. The only designed face.** Positions
below are metres along the frontage from its SE end (`u` in the build script).

- **0 → 2.35 m: sand-tiled base.** Plain from u 0 to ~6.4; the **red roll-up
  garage door** at u 7.90, 2.83 m wide; the **residential entry** (glazed door and
  sidelight, `226` plaque, a lantern sconce each side) at u 10.90, 1.90 m wide.
- **2.35 → 16.0 m: three loft levels in sage-green stucco**, ~4.5 m floor to
  floor. Split lengthwise:
  - **SE half (u 0.5 → 6.0):** two large white-framed **multi-lite loft windows**
    per level, ~2.6 m wide and ~3.2 m tall, in a grid of small panes. The top
    level's pair is markedly smaller (~1.7 x 2.0).
  - **NW half (u 9.4 → 11.7):** a **recessed loggia** per level with a dark steel
    rail across its mouth.
  - **u 6.7 → 9.2:** the **galvanised fire escape**, a straight flight and a
    landing per level, running from ~4.2 m up to the roof.
- **16.0 m: a plain capped parapet**, no cornice. Behind it on the NW half, a dark
  steel roof-deck railing.

**North-west flank, 22.80 m — party wall to 218 Ritch.** Blind. The two 1998
permits put **vinyl siding** on this face and the rear, so it is pale siding, not
the stucco. No photography of it exists.

**South-east flank, 22.80 m — toward 230 Ritch.** Stucco. The 1997 permit filled
in two mezzanine windows on this side, which is evidence there were openings here
and that there are now two fewer. Otherwise blind.

**South-west rear, 12.13 m — block interior.** Vinyl siding. The DataSF ring puts
shallow notches in this end that OSM draws straight. Not visible from any public
street.

**Top.** Flat dark membrane. On the z21 imagery: a row of five or six round white
skylight domes down the spine, a terracotta tiled deck near the front (permit:
a 10 x 12 ft tiled deck), two small raised boxes — one of them the candidate
stair bulkhead — and a railing returning along the front parapet.

## 5. Recognition cues, in order

1. **The green.** A muted sage/olive stucco block on an alley of grey concrete
   warehouses and beige loft buildings.
2. **The red garage door in the sand-tiled base** — the only saturated accent.
3. **The fire escape** — a galvanised zig-zag running to roof level.
4. **The split facade:** loft-window grids on one half, railed loggias on the other.
5. **The proportion** — narrow and deep, standing 3-5 m above both neighbours.

## 6. Preserve / simplify

Preserve: the body proportion; the base band; the garage door; the parapet; the
fire escape as a zig-zag; the loggia recesses as shadow; the roof deck, skylight
row and bulkhead.

Simplify: the multi-lite grids become two chunky mullions and one transom per
opening — the frames are the read at this scale, the panes are noise; the fire
escape becomes three flights, three landings and solid rail panels, no balusters;
the loggia recess is a value trick (light frame ring, dark interior), not carved
geometry.

Dropped: the utility poles and overhead wiring (they dominate every photograph of
this building and belong to the street); wall sconces; hose bibs; the garage
door's vision panels; the mezzanine line; the rear notches (see `REPORT.md` §3).

## 7. Uncertainties carried into the model

1. **The 18.10 m crest is inferred, not observed.** See `REPORT.md` §2.
2. The rear and NW flank are known only from two 1998 siding permits.
3. The green is sampled from one part-shaded panorama.
4. The roof inventory may be contaminated by 218 Ritch's roof (~3 m registration
   error).
5. Night appearance is unresearched; the glow design is reasoned from the
   building's programme.
