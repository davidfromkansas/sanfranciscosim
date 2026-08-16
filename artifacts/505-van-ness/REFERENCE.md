# 505 Van Ness Avenue — reference dossier

**Governor Edmund G. "Pat" Brown Building** — California Public Utilities
Commission headquarters, San Francisco Civic Center. Manifest id
`505-van-ness`. Built from `docs/asset-plans/505-van-ness.md`; where this file
and the plan disagree, **this file and REPORT.md win**.

> **Which Public Utilities Commission.** 505 Van Ness is the **California** PUC
> (state). The **San Francisco** PUC is a different agency in a different
> building at 525 Golden Gate Avenue. The address drove this build.

## Sources

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Address | 505 Van Ness Ave, SF CA 94102 | CA DGS building directory | verified |
| Official name | Governor Edmund G. "Pat" Brown Building | CA DGS building directory | verified |
| Tenant | California Public Utilities Commission (HQ) | CPUC contact page | verified |
| Footprint | `relation/1735766` outer ring, 27 vertices | OSM / Overpass API | measured |
| Levels | 6 | OSM `building:levels` | measured (tag) |
| Height | 27 m | OSM `height`, consistent with 6 levels + photo storey count | **estimated** |
| Completed / architect | 1986 / Skidmore, Owings & Merrill | secondary web sources | single-sourced, attribution only — no geometry depends on it |
| Facade, seal, plaza, court | see below | 3 photographs, CC BY-SA 4.0 (Mattnotmatte, 2025-06-20) + `File:Edmund G. Brown Building.jpg`, Wikimedia Commons | observed |

## Geometry as built

| Quantity | Value |
|---|---|
| Anchor (model origin) | **lon −122.4212915, lat 37.7804835** |
| Anchor derivation | bbox centre of the measured footprint ring |
| Footprint ring | 18 verts after ε = 0.6 m closed-ring Douglas–Peucker; area 6,263 m² vs 6,277 m² surveyed (−0.2 %) |
| Drum arc | least-squares circle through the 8 measured arc vertices: centre (9.81, 8.05), **r = 46.86 m**, 93.5° sweep, resampled to 14 segments |
| Footprint extent | 113.4 m (E–W) × 93.4 m (N–S) |
| **Asset bbox** | **124.2 × 95.3 × 27.000 m** — wider than the footprint because the entrance stair projects ~12 m past the drum |
| Entrance heading | **126.3° true (ESE)** |
| Light court | chamfered octagon, r = 18 m, centred (20.0, 1.5) — designed down from the 39.3 × 39.1 m OSM inner ring so the wings keep believable depth |

### Vertical scheme

| Datum | z (m) |
|---|---|
| Grade | 0.0 |
| Plaza podium / ground-floor datum | 2.0 |
| Storey height (6 floors) | 3.75 |
| Ribbon within each floor | +1.15 → +2.60 |
| Roof deck | 24.5 |
| Top of dark fascia lid | 26.2 |
| Stone coping | 26.5 |
| **Crest (stair penthouse)** | **27.000** |

The crest is normalized to exactly 27.000 m by scaling vertex data (not object
transforms) so the loader's `targetHeightM / measuredHeight` lands on 1.000.

## Design decisions

1. **The drum is the building.** The measured arc was refitted to a circle
   rather than kept as survey chords — an 8-chord polyline reads as a facet,
   and this curve is the entire silhouette (style bible §4: smooth curves where
   they create a landmark silhouette).
2. **The pier order must beat the ribbons.** The first render came out as a
   horizontal barcode: six strong blue bands with nothing vertical. The real
   building is emphatically vertical. Piers went 2.1 → 2.7 m wide and 0.55 →
   0.75 m proud, spacing 10 → 8.5 m, and the glazing band was shortened
   (1.00–2.95 → 1.15–2.60 within each floor) so precast, not glass, is the
   dominant surface.
3. **Recess by projection, not by reveal.** No booleans on the facade: the
   ribbons sit 60 mm proud of the wall and the piers 750 mm proud, so the
   ribbons read as recessed between them at a fraction of the triangle cost.
4. **The court is cut with a boolean**, the one place a boolean earns its keep —
   it turns the body into a genuine ring so the app's downward camera sees a
   real light well with its glazed stair tower, not a painted-on square.
5. **The seal is exaggerated to ~8 m** across (real: ~4 m) so it survives the
   aerial camera — semantic scale, style bible §8/§9. It is the building's one
   saturated element, and the only thing besides the fascia that is not neutral.
6. **The plaza ships with the building.** The concentric curved stair, the two
   drum pedestals and the flagpoles are as recognisable as the facade. They
   push the asset bbox 12 m past the footprint on the ESE only — see the
   centring note below.
7. **One dark accent, one warm accent.** The red-brown fascia lid is the only
   dark element; the court's gold spandrel banding is the only warm one. Style
   bible §7 wants neutral resting areas, and a 124 m building is where you get
   them.

## Centring

The origin is the **footprint** bbox centre, not the full-asset bbox centre.
Centring on the full bbox would slide the building ~4.6 m west of its true
coordinates to compensate for a stair that only exists on one side — a direct
AGENTS rule 5 violation. `validate_505_van_ness.py` therefore allows
|centre.x| ≤ 6 m and documents why; |centre.y| stays within 1 m.

## Night state

`_Glow` surfaces are thin shells standing proud of the opaque glazing, never a
primary surface (the app renders the glow layer at ~12 % alpha by day):

- `Toy_glass_Glow` — a scatter of lit ribbon panels on every third bay, floors 2, 3 and 5.
- `Toy_trim_Glow` — the entrance soffit, the lintel band, and the **seal ring**, which is what keeps the identity legible after dusk.

## Materials

All flat, roughness 0.85, no textures, no transparency.

`Toy_stone` d9d2c2 · `Toy_trim` f3efe6 · `Toy_glass` 2a4d73 · `Toy_glassl` 6f95b8 ·
`Toy_sky` 6db3d9 · `Toy_gold` caa64a · `Toy_rust` a86444 · `Toy_roofd` 45454a ·
`Toy_steel` 9aa0a6 · `Toy_ink` 3a3530 · `Toy_glass_Glow` · `Toy_trim_Glow`

All are project-palette entries; there is no palette extension in this asset.

## Reproduce

```bash
blender -b --python build_505_van_ness.py
blender -b --python render_505_van_ness.py
blender -b --python render_505_van_ness.py -- --night
blender -b --python validate_505_van_ness.py
python3 make_contact_sheet.py
```
