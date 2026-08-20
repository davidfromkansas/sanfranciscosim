# Pier 1 — reference dossier

Research behind `pier-1.glb`. The plan (`docs/asset-plans/pier-1.md`) was the starting
point; everything below was re-verified for this build, and the four corrections it
produced are listed in §8 and repeated in `REPORT.md`.

## 1. What it is

Pier 1, The Embarcadero at Washington Street, San Francisco CA 94111. A finger pier with a
shallow Neo-classical **bulkhead building** on the Embarcadero building line and a 213 m
**transit shed** running north-east into the Bay behind it, all on a reinforced-concrete
pile deck.

- **Bulkhead** designed c.1914–18 by **A. A. Pyle**; pier substructure and shed by
  **A. C. Griewank** under Chief Harbor Engineer **Jerome Newman**.
- Piers 1, 1½, 3 and 5 "opened 1918" under Chief Engineer Frank G. White; the National
  Register records Pier 1 itself as **built 1931**. Both dates are carried here — they date
  different things, and no source in this dossier reconciles them.
- **Rehabilitated 2001**, $42 M, architect **SMWM**, contractor Nibbi Brothers; seismic
  retrofit by Rutherford + Chekene (70 piles up to 170 ft × 4 ft); ~50,000 sf of inserted
  mezzanine; bay-water heat exchanger. Interiors by TEF; Perkins&Will architect of record
  for the AMB/Prologis fit-out. Bendheim channel glass at the conference volume.
- **Tenants:** Port of San Francisco headquarters (52,000 sf) and Prologis (formerly AMB)
  headquarters (36,800 sf), plus a public conference centre and the Port Walk promenade.
- **Listings:** NRHP #98001551; contributor to the Central Embarcadero Piers Historic
  District (#02001390) and the Port of San Francisco Embarcadero Historic District
  (#06000372).

## 2. Sources

| Source | What it establishes |
|---|---|
| NoeHill / NRHP #98001551 | "Pier One, The Embarcadero At Washington, Built 1931"; finger-pier typology (49 built, 11 surviving) |
| NoeHill / NRHP #02001390 | Central Embarcadero Piers HD: Piers 1, 1½, 3, 5, 1918–1931, "the southernmost Beaux-Arts grouping" |
| Wikipedia, *Central Embarcadero Piers Historic District* | "timber-frame bulkhead buildings, covered in stucco, are each two stories high"; two-storey arches; opened 1918 |
| Port of SF, *Historic Piers RFI* (2018) | A. A. Pyle (bulkhead), A. C. Griewank (pier + shed), Jerome Newman; concrete pile substructure, timber shed framing, stuccoed timber bulkhead, concrete cargo aprons; monumental arched entry with keystone and voussoirs, quoins; Pier 1 rehab completed 2001 |
| BD+C, "Bayside Renaissance" | SMWM; $42 M; 18-month schedule; 70 seismic piles; bay-water heat exchanger; ~50,000 sf mezzanine |
| TEF Architecture | Port of SF HQ, 52,000 sf; 2004 Chronicle/AIA "Best of the Bay" Green Design Award |
| Perkins&Will | Prologis HQ, 36,800 sf, opened 2001 |
| Architizer / AMB at Pier 1 | "civic wood-frame bulkhead structure and a 700-foot long concrete/steel warehouse"; added window openings, operable windows, daylighting |
| ASCE 10.1061/40555(2001)84 | Rutherford + Chekene, renovation and seismic rehabilitation |
| CEQANet 1998122027 | Pier 1 Project NOD; address confirmation |
| OSM way `25489482` | `man_made=pier`, `building=yes`, `height=10`, `wikidata=Q66078388`; the measured footprint ring |
| DataSF `ynuv-fyni` area_id 146 | `hgt_mediancm=966`, `hgt_maxcm=1273`, `p2010_zmaxn88ft=39.86` |
| Google satellite tiles z19–z21 | Re-sampled into a georeferenced ortho in the pier's own axis frame at 0.06–0.08 m/px; roof cross-sections, apron widths, deck outline |
| Google Street View panos `1DM4N8vgxv7QnYRcyFabrQ`, `_Ck7UJ3tYOXhMEKksKQ_sQ`, `49eksWulVaXoab8glx3Csw`, `BZMmgVxQOmLDPvPLxWlRYQ`, `3sGpaIsliCS9vamaU6ue_A`, `9ej82SMckZ5tGtAE8tLolw`, `Z3h5-nCuEKUDIV51fDXmVA` | Facade head-on and oblique; both shed flanks; the NE end; inside the bulkhead passage; the long view from the Ferry Building promenade |

Everything derived from imagery is **observed**, not documentary, and is labelled so below.

## 3. Measured geometry

Working frame: **along** runs north-east on bearing **053.77°** with its zero at the shed's
north-west corner on the bulkhead's inner line; **perp** runs 90° clockwise, positive
south-east. The Embarcadero facade is the plane `along = −24.2`.

Ring measured from OSM way 25489482 via the OSM API and reprojected into the app's local
tangent frame:

```
(-23.8,-14.2) (-11.8,-14.1) (-10.7,-14.0) (-10.6,-10.5) (-10.4, -5.8) ( -9.1, -5.9)
(  0.0,  0.0) (201.2, -0.0) (201.3,  2.4) (202.1, 23.4) (202.2, 26.7) (149.1, 26.5)
( 96.7, 36.3) ( 30.4, 35.8) ( 19.3, 34.5) ( 18.7, 36.7) ( 18.8, 41.0) (-11.5, 40.9)
(-11.6, 50.6) (-23.5, 50.4) (-24.2, 15.4) (-23.9,-10.4)
```

| Element | Value | How |
|---|---|---|
| Building overall | 226.4 m × 64.7 m | measured (OSM ring) |
| Bulkhead slab | 12.5 m deep × 64.7 m wide, `along −24.2…−11.5` | measured |
| Shed head | 41.0 m wide, `along −11.5…19` | measured |
| Shed body | 36.2 m wide, `along 19…97` | measured |
| Taper | 36.2 → 26.5 m over `along 97…149` | measured |
| Outer run | 26.5 m wide, `along 149…202` | measured |
| Pier deck | ~234 m × ~52 m; apron ≈11 m NW, ≈7 m SE, ~7 m past the shed at the tip | observed (ortho, 0.08 m/px) |
| Long-axis heading | 053.77° | measured from the ring's NW edge |
| Facade normal | 233.77° | derived |

## 4. Heights

All above the pier deck.

| Element | Value | How |
|---|---|---|
| Shed parapet | **9.7 m** | DataSF `hgt_mediancm = 966` |
| Roof spine crest | **~12.0 m** (2.3 m above the roof) | observed — shadow width on the ortho, corroborated by the median/max gap |
| Bulkhead wing parapet | **~8.4 m** | observed — photogrammetric, pano `1DM4N8vgxv7QnYRcyFabrQ` |
| Pavilion entablature | **~10.3 m** | observed — same pano |
| Pavilion apex | **~12.8 m** | observed — same pano; agrees with DataSF `hgt_maxcm = 1273` |
| Flagpole tip | ~17.9 m | observed — **not modelled**, see §7 |
| Pier deck above water | ~2.9–3.0 m real; **2.4 m** in the app's DEM at the anchor | inferred / measured from `app/public/tiles/terrain.bin` |

**Photogrammetric method.** The facade pano was reprojected to a rectilinear frame of known
focal length, then self-calibrated on the sidewalk line at the base of the facade (the only
point in frame whose height is known to be 0). That fixes the camera distance at 31.05 m,
after which every other height in the frame follows from its pixel row. Heights derived this
way are quoted to 0.1 m and believed to ±0.4 m.

## 5. What each side shows

- **South-west, the Embarcadero facade.** A flat 64.7 m two-storey cream wall with a plain
  coping, broken in the middle by a ~22 m pavilion stepping forward and up: quoined pilaster
  strips, a **round arch ~9.6 m wide** springing at 4.35 m and crowning at 9.14 m with
  radiating voussoirs and a keystone, a dentilled entablature carrying **`PIER · 1`**, and a
  low raked pediment with a flattened apex. The arch is filled with dark gridded glazing,
  a `PORT OF SAN FRANCISCO` band and a door screen. The wings carry 3–4 narrow tall
  steel-sash windows per bay above shopfronts; the NW wing is pierced at ground level by a
  second, flat-arched **vehicle portal** — the Belt Railroad pass-through, still open, and
  the street is visible through it from the pier deck.
- **North-west flank** (Pier 3 slip). ~213 m of the same wall on a repeating ≈7.5 m
  structural bay: a slightly projecting pilaster with a small corbel cap, a tall main window
  group on a belt course at ~2.2 m, and a continuous clerestory band just under the coping.
  Some bays are double glass doors. The parapet is dead level and hides the roof entirely.
- **South-east flank** (Ferry Building side). The same system; this is the elevation the
  city's camera sees most, and its apron carries the globe lamp standards and the benches.
- **North-east end.** A blunt 26.5 m end wall in the same language, then ~7 m of open
  concrete deck with a rounded corner, railing and bollards.
- **Above.** Pale membrane roof. A raised spine on the centreline carries a ~7 m solar array
  its whole length; past `along ≈ 145` further arrays spill onto the flat roof either side.
  Round vents and rectangular hatches. The bulkhead's roof is a lower, plainer flat plane
  wrapping the shed head in an L, with the pavilion breaking through it at the frontage.

Measured roof cross-section (ortho, `along 64–72`): 12.7 m flat white roof · 0.6 m hard
shadow line · 1.9 m raised strip · 7.0 m solar array · 12.0 m flat white roof.

## 6. Recognition cues (ranked)

1. The arched frontispiece with `PIER · 1` over it.
2. Length and taper — 213 m leaning NE, narrowing over the outer half.
3. The solar-striped white roof.
4. Cream body, slate-blue steel, and no third colour.
5. The apron promenade ring, which is what makes it read as a *pier*.

## 7. Simplifications and deliberate omissions

- **The flagpole.** Including it would put `targetHeightM` at 20.5 m — a number describing a
  0.1 m pole — and it is sub-pixel at the app's camera.
- **Bay counts compressed.** 28 real structural bays per flank become 28 modelled bays at
  7.5 m; the wing windows are modelled as three lights per bay where the real count is 3–4.
- **The channel-glass conference volume, the mezzanine, the catwalks and the bay-water heat
  exchanger** are interior or submerged and read from nowhere outside.
- **The pile field** is modelled as a perimeter row plus two internal rows under the outer
  end, not as the full field: only the perimeter and the outer end are ever seen.
- **`PORT OF SAN FRANCISCO`** is a dark band with an implied lettering rhythm rather than
  extruded letters; `PIER · 1` is extruded because it is cue #1.

## 8. Corrections to the plan made during this build

1. **The roof was inverted.** The plan described a 9 m monitor spine with two 8.4 m solar
   fields flanking it on the low roof. The ortho cross-section shows the opposite: one
   ~9.5 m raised spine whose top carries a single ~7 m array, with broad flat white roof
   either side. Built as measured.
2. **Spine height 2.3 m, not 2.7 m** — re-measured from the shadow at three stations.
3. **Wing parapet 8.4 m, not 8.6 m**, and the pavilion entablature 10.3 m, from a cleaner
   photogrammetric pass on a wider reprojection of the same pano.
4. **The arch is 9.6 m wide, not "about 10 m"**, and its springing is 4.35 m — the plan's
   5.5 m springing came from mis-reading the archivolt's outer edge as the springing line,
   which would have made the arch segmental rather than the semicircle it is. Modelled at
   10.4 m wide (enlarged per style bible §8/§9) with the springing at 4.4 m.

## 9. Uncertainties carried into the build

- The **spine** remains the least-verified element: no photograph in this dossier shows it,
  because every street-level view is taken from an apron whose parapet hides the roof. It is
  a shadow measurement plus a LiDAR median/max gap. If it turns out to be solar racking
  rather than a monitor, the roof loses 2.3 m of relief; `targetHeightM` is unaffected
  because the pavilion sets it.
- **`hgt_maxcm` and `p2010_zmaxn88ft` on this footprint are mutually inconsistent** and both
  are LiDAR statistics computed over water, where the "ground" surface is undefined. The
  12.8 m crest here is photogrammetric and only *agrees* with `hgt_max`.
- **Pier deck elevation is inferred.** ~2.9–3.0 m above water is the standard Embarcadero
  figure and matches the app's DEM ridge to within 0.6 m; no Port document in §2 states it.
- **Bay counts are inferred** from oblique Street View where the far end of every run is
  foreshortened to nothing.
- **The build date is genuinely contested** (1918 vs 1931).
