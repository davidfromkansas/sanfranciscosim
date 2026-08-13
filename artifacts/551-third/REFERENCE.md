# 551 Third Street (Shell Service Station) — reference dossier

Research behind `551-third.glb`. Compiled 12 August 2026, re-verifying
`docs/asset-plans/551-third.md` before modelling rather than trusting it. Two of
that plan's readings turned out to be wrong and were corrected here first; both
corrections are also folded back into the plan and are restated in `REPORT.md`.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM [way/124889461](https://www.openstreetmap.org/way/124889461) | canopy outline (151 m2, 16 vertices), `amenity=fuel`, `building=roof`, Shell brand, fuels (diesel + 87/89/91), 24/7, surveyed `check_date` 2026-04-26 |
| OSM [way/124889473](https://www.openstreetmap.org/way/124889473) | kiosk outline 12.96 x 7.11 m, `building=commercial`, `building:levels=1`, `height=4`, `shop=convenience` |
| OSM ways 1000437720–1000437730 | forecourt circulation; the three `covered=yes` segments are the fuelling lanes and are the only direct evidence of lane positions |
| [DataSF parcels](https://data.sfgov.org/resource/acdm-wktn.json) `blklot=3775025` | the 807 m2 lot polygon, 39.7 x 20.4 m, address range 551–561 3rd St |
| [DataSF 2010 LiDAR footprints](https://data.sfgov.org/resource/ynuv-fyni.json) `mblr=SF3775025` | **two** footprints on the lot: `201006.0050940` (151 m2, height median 5.09 m, majority 5.10 m, std 0.42 m over 601 cells, max 6.64 m) and `201006.0147259` (84 m2, height median 3.91 m). This is also the pipeline's own building source, so these two records are exactly what the bake draws here. |
| [DataSF DBI permits](https://data.sfgov.org/resource/i98e-djp9.json) block 3775 lot 025 | 26 records 1998–2025: the 2000 kiosk rebuild, the 2003–04 canopy fascia repaint and LED lightbar, the 2004 and 2012 dispenser/tank replacements, the 2017–19 hydrogen install, the 2024–25 hydrogen demolition |
| Esri World Imagery (Vivid Premium, Vantor), captured **2025-08-29**, 0.34 m | canopy form, umbrella count, central columns, island count, kiosk position. Reprojected into the site frame below and registered against the OSM/parcel/LiDAR geometry. |
| [Fiedler Group project recap](https://www.fiedlergroup.com/architecture-engineering-project-recaps/shell-opens-san-franciscos-first-hydrogen-stations/) | the hydrogen dispensers were placed *under the existing gasoline canopy* — the canopy predates 2018 and survived the 2025 removal unchanged |
| [H2FCP station page](https://h2fcp.org/content/san-francisco-third-st) and [Shell LD closure notice](https://h2fcp.org/sites/default/files/Shell_LD_Closure.pdf) | the hydrogen station's opening and Shell's light-duty hydrogen closure |
| [Shell site listing](https://find.shell.com/us/fuel/10008255-551-3rd-st/en_US) | the station is current and trading |

No copyrighted imagery is committed. `reference/site-plan-measured.png` is our own
line drawing of the measured geometry; the aerial itself is cited above, not
redistributed.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Anchor | `-122.3946431, 37.7806625` | measured (parcel centroid) |
| Lot | 39.7 x 20.4 m, 807 m2 | measured |
| Long-axis heading | 315.1 / 135.1 deg true | measured |
| 3rd Street frontage | faces 225.1 deg (SW) | measured |
| Canopy deck top | 5.10 m | measured (LiDAR majority, std 0.42 m) |
| Crest | 6.60 m | measured height (LiDAR max 6.64 m); **attribution to the pecten/lightbar crown is inferred** |
| Canopy clearance | 4.30 m | inferred (0.80 m fascia + standard forecourt clearance) |
| Kiosk | 7.1 x 13.0 m, parapet 3.91 m | measured |
| Ground | mean 6.88 m NAVD88, range 0.35 m — flat | measured |

## 3. Orientation

Site frame used by the build script: origin at the parcel centroid, **u** toward
315 deg (NW, along 3rd Street), **v** toward 45 deg (NE, into the lot).

```
Parcel        u -21.1 .. +18.6   v -11.4 .. +9.0
Canopy        u  -2.9 .. + 8.0   v -13.2 .. +5.6   (two octagons, 151 m2)
Kiosk         u -21.5 .. -14.3   v  -5.0 .. +8.0
Fuel lanes    v = +4.00, -4.55, -9.85 (OSM driving lines)
```

Authored with Blender +Y = true north, +X = east. The contract's "front faces
−Y" cannot be honoured: the frontage faces 225 deg. Real-world orientation wins
(AGENTS rule 5, and the orientation note in `docs/asset-plans/README.md`).

## 4. What each side shows

**South-west, 225 deg — 3rd Street front.** No building line at all: a kerb, a
bollard run and two curb cuts, with the umbrellas standing back behind them. The
lot reads as a gap in an otherwise continuous street wall — 550 Third Street
opposite is a 48 m warehouse frontage. The pecten faces this way.

**North-east, 45 deg — rear.** The back of the lot against the 14.2 m flank of
181 South Park. Perimeter kerb, the air/water point, service clutter.

**South-east, 135 deg — toward Brannan.** The kiosk end: a blank side wall and
the edge of the apron.

**North-west, 315 deg — toward South Park.** Open asphalt, the north umbrella's
fascia the dominant object, and the kiosk shopfront visible across the forecourt.

**Top — the primary facade.** Two octagons ~11 m across with radial ribs
converging on a central column, touching at a pinched waist; a figure-of-eight
in plan. Open apron north-west of them, the kiosk's flat roof with one small
plant unit to the south-east, lane markings and two chevroned curb cuts along
the 3rd Street edge.

## 5. Recognition cues (ranked)

1. The twin octagonal umbrellas on single central columns, touching at a waist.
2. The red-over-yellow fascia band ringing all eight sides of each, and the
   pecten disc.
3. The hole in the street wall — open asphalt where every neighbour is a
   continuous frontage.
4. The island cluster under each umbrella, which is what stops the apron reading
   as a car park.
5. At night, the two glowing yellow lightbar rings.

## 6. Preserve / simplify

**Preserved:** the lot rectangle; the twin-octagon plan and its waist; the single
central column per umbrella; the radial ribs; the 4.30 m clearance; deck 5.10 m,
kiosk 3.91 m, crest 6.60 m; two islands at the umbrella centres; the kiosk at the
south-east end.

**Simplified:** octagons regularised (R = 5.40 m, tangent pair) from a slightly
irregular surveyed outline; ribs are eight raised spokes, not a truss; the pecten
is a 12-lobe scalloped disc with no logotype; dispensers are chunky boxes with a
face panel and a hose loop, no nozzles or keypads; forecourt markings are an edge
line, three lane stripes and two chevrons.

**Left out:** any freestanding price pylon (unconfirmed — see 7); vehicles; all
hydrogen equipment; anything beyond the property line.

## 7. Uncertainties and conflicting evidence

- **The crest's identity is inferred.** 5.10 m to the deck is measured and tight.
  6.64 m is a real LiDAR maximum over the same footprint at more than 3σ, and the
  2003–04 permits for an internally illuminated LED lightbar and repainted fascia
  make a lit pecten crown the natural explanation — but it is inference. Since
  `targetHeightM` is the crest, an error here rescales the whole station.
- **Dispensers per island is an assumption** (two). The 2025 aerial resolves the
  islands but at 0.34 m cannot count dispensers.
- **No freestanding price pylon is confirmed.** Two permits to erect one (2000,
  2001) both expired, and nothing pylon-shaped is legible in the 2025 aerial. Left
  out. If one exists and clears 6.6 m, it becomes the crest.
- **Dated sources are actively misleading here, with one exception.** 2018–2025
  imagery shows a hydrogen installation demolished in August 2025. The 2025-08-29
  aerial post-dates the demolition by four days and is trustworthy; the 2010 LiDAR
  and Bing-traced OSM predate the hydrogen chapter and are also safe. Anything
  between those two windows is not.
- The kiosk's LiDAR footprint carries a 14.2 m maximum return over an otherwise
  3.9 m building — almost certainly overhanging vegetation or a neighbouring
  parapet caught in the polygon. Ignored.
