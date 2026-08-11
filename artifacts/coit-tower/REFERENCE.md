# Coit Tower reference dossier

Research checked 2026-08-10. Facts below separate published/measured values from
visual inference. No third-party imagery is committed with the model; the model
and review renders are original. Where this dossier contradicts
`docs/asset-plans/coit-tower.md` Part 2, the evidence is stated and this dossier
governs the asset.

## Verified facts

| Item | Value | Confidence / source |
|---|---:|---|
| Location | 1 Telegraph Hill Blvd, Pioneer Park, Telegraph Hill | OSM, SF Rec & Park |
| WGS84 anchor | **-122.4058338, 37.8023742** | OSM way/28824850 polygon centroid, computed from node coordinates; the plan's anchor (-122.4058407, 37.8023762) agrees within ~0.6 m |
| Height | **64 m / 210 ft** above its own base terrace | OSM `height=64`, Wikipedia 210 ft, Wikidata P2048 |
| Structure | Three nested concrete cylinders; outer fluted shaft 180 ft / 55 m supports the viewing platform; intermediate = stair, inner = elevator | Wikipedia; SEAONC Hensolt Legacy Project |
| Observation deck | 32 ft / 9.8 m below the top, arcade and skylights above it | Wikipedia |
| Base footprint | Near-circular, 22.4 x 23.1 m extent, 395 m² (measured from the polygon); radius ~11.2 m with four flat bays | OSM way/28824850, measured locally |
| Material / colour | Unpainted reinforced concrete, mapped `#E0E0E0` | OSM tags, Wikipedia "unpainted reinforced concrete" |
| Built / architects | 1932–1933; Arthur Brown Jr. with Henry Temple Howard; phoenix relief by Robert Boardman Howard | Wikipedia, OSM `architect` |
| Style | Art Deco ("fluted tower, its arches, textured reinforced concrete") | Wikipedia, Wikidata |
| Hilltop | Telegraph Hill summit; OSM `ele=89` on the building node | The app samples terrain; the GLB still starts at z=0 |

## Source list and what each establishes

- [OpenStreetMap way/28824850](https://www.openstreetmap.org/way/28824850) —
  footprint polygon (fetched raw via the OSM API and measured in local meters),
  height 64, concrete, architect, 1933. The polygon is a **notched circle**:
  radius 10.0–12.4 m with four long flat edges. The longest flat edge (6.1 m)
  faces bearing **≈ 346°** (NNW); three more flat bays face ≈ 82°, ≈ 182° and
  ≈ 255°.
- [Overpass API, surroundings](https://overpass-api.de) — Telegraph Hill
  Boulevard ends in a parking loop whose ring (OSM way 8917644) centers
  **~50 m north-northwest** of the tower; a footway/steps chain leaves the
  tower at bearing ≈ 345° toward that loop; a second steps chain descends
  south to the boulevard's lower leg (crossing + stop nodes ~63 m south).
- [Wikipedia — Coit Tower](https://en.wikipedia.org/wiki/Coit_Tower) — nested
  cylinders, 180 ft fluted shaft, deck 32 ft below the top, arcade and
  skylights above it, rotunda base with display space, phoenix relief above
  the main entrance, unpainted concrete, Art Deco.
- [SEAONC Hensolt Legacy Project — Coit Tower](https://legacy.seaonc.org/structure/coit-tower/) —
  engineer-side confirmation: 210 ft reinforced concrete, three nested
  cylinders, first cylinder 180 ft supporting the viewing platform, stair in
  the intermediate and elevator in the inner shaft.
- [Wikidata Q1107297](https://www.wikidata.org/wiki/Q1107297) — height, Art
  Deco style, architect.
- [SF Recreation & Parks — Coit Tower](https://sfrecpark.org/facilities/facility/details/Coit-Tower-290) —
  operator material, opening context.
- [Wikimedia Commons — Category:Coit Tower](https://commons.wikimedia.org/wiki/Category:Coit_Tower) —
  geolocated photography used for all four sides, the crown and the base.
  Studied closely (not committed): *Architect and Engineer* 1933 scans
  (period full elevations and crown), "Coit Tower top.jpg" (inside the
  arcade), "Coit Tower aerial.jpg" (open lantern well, parking loop north of
  the tower), "Coit Tower From Above (Unsplash).jpg", "Christopher Columbus
  statue and Coit Tower (July 2012).jpg" (statue + entrance in one frame),
  "Coit Tower, San Francisco (south facing side).jpg" (base colonnade bay),
  "Coit Tower 2021.jpg" (high-resolution crown study).

## Orientation — the entrance faces NNW, not south-east

The plan dossier (`docs/asset-plans/coit-tower.md` §2.3/§2.4) places the
entrance "on the south-east side" facing the parking circle. Three
independent lines of evidence all say the parking circle — and the entrance —
are on the **north-northwest** side:

1. **Footprint geometry:** the longest flat facade edge of the OSM polygon
   (6.1 m) faces bearing ≈ 346°.
2. **Road topology:** the Telegraph Hill Boulevard parking loop centers ~50 m
   NNW of the tower (bearing 337–355°); the footway/steps chain from the
   tower to the loop leaves at bearing ≈ 345°.
3. **Photography:** the July 2012 Columbus-statue photo shows the statue
   (which stands in the parking circle) directly in front of the entrance
   steps, flag and visitor queue; the file "south facing side" shows a
   colonnaded window bay with no door on the opposite side; the
   "Coit Tower aerial.jpg" frame shows the circle and entrance walkway on the
   parking side with Garfield School (mapped WSW of the tower) behind.

The asset is therefore authored with Blender +Y = true north and the entrance
bay facing **bearing 346°** (14° west of north). The measured base-bay cross
(346° / 82° / 182° / 255°) is close to a regular cross yawed ~14°
counter-clockwise from the cardinal grid; the model uses exactly
346/76/166/256 (a regular cross at 14° CCW yaw). This deviates from the
generic "front faces −Y" landmark rule on purpose: the loader applies no
rotation (`placeGeneric` in `app/src/assets.js`), so the real-world heading
must be baked in. Recorded again in `REPORT.md`.

## Directional observations

### All four elevations

Nearly identical by design: a tapering, fluted, unpainted concrete cylinder,
unbroken for ~42 m, over a two-tier round base, under a two-tier arched crown.
The only azimuthal differences are the four flat base bays and the entrance.

### North (entrance side, bearing ≈ 346°)

- Projecting flat-faced entrance bay with steps up from the walkway to the
  parking circle.
- Recessed doorway; Robert Howard's phoenix relief panel above the door.
- The American flag and the Columbus statue stand outside in the circle
  (excluded from the GLB).

### East / South / West

- Each has a flat colonnaded bay: square piers in antis with tall dark
  multi-pane windows between them ("south facing side" photo).
- Above the bays the rotunda steps back twice (a plain drum band, then a
  narrow step ring) before the fluted shaft begins.

### Top / crown (aerial + 2021 close study)

Two distinct tiers, both arcaded, both slightly faceted rather than smoothly
round:

- **Loggia (observation) tier:** 8 tall round-arched openings; each arch has a
  balustrade across its lower opening; deep reveals; behind them the enclosed
  viewing gallery (small inner arches and round oculus windows visible in
  photos). Above each of the 8 piers sits a **group of 3 narrow arched slots**
  (confirmed in the 1933 *Architect and Engineer* scan, the 2012 twilight
  photo and the 2021 photo).
- **Lantern tier:** a set-back smaller drum with 8 round-arched openings and a
  slightly flared rim — and critically the **top is open**: aerial photos look
  straight down into the well (the "skylights above the deck" ring the
  well floor). No dome, no roof disc.
- The fluted shaft terminates in a small dentil/corbel course just below the
  loggia sills.

### Fluting

Wide, shallow concave channels separated by narrow fillets, running the full
shaft from just above the rotunda to the corbel course. **No published flute
count was found**; counting channels across the visible half of the shaft in
the 1933 scan and the 2021 high-resolution photo gives ~11–12 over the visible
half, i.e. **~22–24 around** (visual inference). The model uses 24, which also
locks cleanly to the 8 crown bays (3 flutes per bay).

## Day and night appearance

- **Day:** pale warm-white/grey unpainted concrete all over; openings read as
  dark voids; the concrete rim shadows do all the drawing.
- **Night:** the tower is floodlit and the crown openings glow warm from
  interior lighting — the crown is the identity feature after dark. The shaft
  stays non-emissive (floodlighting is the city's job, not the asset's).

### How the night state works in the app (and how the asset encodes it)

The trigger lives entirely app-side: `app/src/env.js` computes the real sun
elevation for San Francisco at the real wall clock and drives the shared
`uNight` uniform (toy mode blends day → golden → dusk → night across
elevation +8° … −4°). The landmark loader (`app/src/assets.js`) buckets
geometry by material-name suffix: `*_Glow` faces merge into one **unlit**
overlay mesh whose opacity is `0.12 + uNight × 0.95`
(`updateLandmarkGlow` in `app/src/kit.js`), colored by the baked material
color. The asset therefore never decides when it is night — it only tags
which surfaces are lamps.

Because glow surfaces are only ~12 % opaque in daylight, **structural
surfaces must never be glow-only** (they would turn ghost-transparent by
day). The asset follows the light-strip pattern instead (as the Golden Gate
GLB does): solid `Toy_white` structure everywhere, with thin dedicated glow
surfaces floating just proud of it —

- a `Toy_white_Glow` shell between the loggia's white inner drum and the
  arch backs: invisible against the white core by day, the warm lit gallery
  behind all 8 arches and balustrades at night;
- a `Toy_white_Glow` liner inside the lantern well: the open top and the 8
  lantern arches read as a lit lamp from the air and the street;
- narrow `Toy_white_Glow` centres over the dark `Toy_ink` pier slots: dark
  graphics by day, 24 lit slivers at night (the real slots are lit
  openings);
- one small `Toy_gold_Glow` strip over the entrance door — a warm porch
  lamp on the approach side.

## Strongest recognition cues (ranked)

1. Plain white/ivory cylinder with a subtly wider, two-tier arched crown.
2. Vertical fluting running the full shaft.
3. The ring of 8 tall arched openings (with balustrades) at the top, with the
   open-topped lantern above.
4. A tower standing on a hill — the app's terrain supplies Telegraph Hill;
   the round rotunda base grounds it.

## Translation to the SF-SIM miniature style

### Preserved

- 64 m total height, ~22.4 m base extent, ~13.4 m shaft base diameter
  tapering to ~12.3 m (the 22 m footprint is the rotunda, **not** the shaft).
- Real-world heading: entrance bay at bearing 346°, base-bay cross at 14° CCW.
- Two-tier rotunda base with four flat bays; two-tier arcaded crown with open
  lantern top; continuous flute rhythm; slight taper.

### Simplified / exaggerated

- Fluting becomes 24 crisp geometric channels (cut as geometry, no texture).
- The crown is slightly widened and its arches deepened so it survives the
  city camera at 64 m (plan §2.15 risk); balustrades become chunky toy rails.
- The 3-slot pier groups become dark inset panels (they are lit openings in
  reality; keeping them dark preserves one clear glow story — the arches).
- The phoenix relief becomes one raised `Toy_trim` panel over the door.
- Interior murals, stair, elevator: not modelled. Windows have no interiors
  (style bible §5).
- The skylight ring at the lantern floor becomes a flat `Toy_glass` annulus
  visible from above (style bible §10 — the roof is a designed surface).

## Uncertainties and conflicting evidence

- **Flute count** is visual inference (~22–24); no drawing was found that
  states it. The model's 24 is a design decision, documented here.
- **Arch count**: 8 loggia arches / 8 lantern arches is counted from aerial
  and ground photos (3 visible across ~135° at ground level, 45° spacing from
  the air). No published count found.
- **Entrance bearing**: the plan said SE; all measured evidence says NNW
  (≈ 346°). Resolved in favour of the measured geometry, documented above.
- The exact rotunda tier heights are scaled from photographs against people
  (~1.75 m) and the OSM footprint; they are plausible-meters, not surveyed.
- OSM `ele=89` vs the commonly quoted ~84 m summit: irrelevant to the GLB
  (min Z = 0; the app's terrain places the base).
