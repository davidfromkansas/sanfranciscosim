# 345 Spear Street (Hills Plaza) — SF-SIM asset plan

The 1989–91 Whisler-Patri half of the Hills Plaza complex: a buff-brick office
podium wrapping a private courtyard, an 18-storey white residential tower
(One Hills Plaza, addressed 75 Folsom Street) rising from its Embarcadero
corner, and a red-tile hip-roofed pavilion on the Spear Street side. Google's
San Francisco office. The historic Hills Brothers Building (2 Harrison Street)
is the *other* half of the complex and is **its own separate landmark,
in flight in a sibling pipeline session** — it is not part of this asset.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/345-spear/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `345-spear` |
| Existing procedural builder | none — new landmark (Case B: needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3900655, 37.7900324` (OBB centre, measured) |
| Target height | **68.5 m** (LiDAR `hgt_max`, read as the tower's mechanical crown — see 2.1/2.15) |
| OSM footprint | relation/12734194 — outer ring 7,108 m², OBB 84.0 × 97.5 m, courtyard hole 494 m² |
| Triangle cap | 24,000 |
| Category | `3` (Office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 345 Spear Street (Hills Plaza) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 345 Spear Street (the 1989–91 Hills
Plaza building) in San Francisco and deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render
review images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/salesforce-tower/` — the reference implementation of this exact
   deliverable (dossier, deterministic build script, validator, renders, report)
8. `docs/asset-plans/345-spear.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- A full-height buff-brick office podium (7–8 storeys) with a regular punched
  window grid, precast spandrel bands and a dark blue-green storefront band
- The ground-floor arcade of round-headed arches facing the Embarcadero and the
  interior plaza, echoing the historic Hills Brothers arches next door
- The 18-storey white residential tower rising from the courtyard's south-east
  quarter with its stepped, layered crown
- The red terracotta hip-roofed pavilion on the Spear Street frontage
- The landscaped level-8 roof garden on the Folsom side (the camera looks down;
  roofs are facades)
- The private interior courtyard (the OSM ring has a real hole)

## Scope of the exported asset

Export ONLY the 345 Spear Street building: podium, tower, pavilion, courtyard
floor and roof terraces. Do NOT model the Hills Brothers Building
(2 Harrison Street, the brick 1926 landmark with the campanile) — it is a
separate landmark being built in a parallel session. Do not include streets,
palm trees on the Embarcadero, the Muni platform, vehicles, people, plinths,
cameras or lights.

## Research 345 Spear Street independently

Verify the dossier rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation. The dossier's Street View pano ids and satellite georefs in §2.2
reproduce every observation.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no image textures;
no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras,
lights, animations, armatures or constraints; at most 24,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east. The block
sits on the rotated SoMa grid: Spear Street frontage bearing ≈ 315°, Folsom
≈ 45°. The loader applies no rotation — model at the true heading.

## Reproducible Blender workflow

Keep `artifacts/345-spear/build_345_spear.py` (deterministic build script),
`artifacts/345-spear/345-spear.blend`, and `artifacts/345-spear/345-spear.glb`.

## Required review renders

`345-spear-top.png`, `345-spear-north.png`, `345-spear-east.png`,
`345-spear-south.png`, `345-spear-west.png`, plus
`345-spear-contact-sheet.png` and a high three-quarter aerial
`345-spear-aerial.png` (day) and `345-spear-aerial-night.png`.
All from the exported GLB, shared scale and lighting.

## Validate the exported GLB

Re-import `345-spear.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Write `artifacts/345-spear/validation.json`
and `artifacts/345-spear/REPORT.md`.

## Manifest draft

Include in REPORT.md; do not edit the production manifest in this task.

```json
{
  "id": "345-spear",
  "file": "345-spear.glb",
  "anchor": [-122.3900655, 37.7900324],
  "targetHeightM": 68.5,
  "cat": 3,
  "name": "Hills Plaza (345 Spear)",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N
}
```
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026. Values marked *inferred* or *estimated* are visual or
derived estimates, not published figures.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Completed | 1989–91 (office listings say 1989/1990; the residential floors opened 1991) | LoopNet, CompStak, rises.co |
| Architect | Whisler-Patri | Buehler Engineering project page (structural engineer of record; spells it "Whistler Patri"), rises.co |
| Program | office floors 1–7, residential floors 8–18 (67 condominiums, "One Hills Plaza", addressed 75 Folsom St) | rises.co, Hoodline, DataSF (exactly 67 condo lots at 75 Folsom in block 3744) |
| Office area | 403,415–426,760 SF Class A; anchor tenant Google | LoopNet, CompStak |
| Footprint | outer ring 7,108 m²; OBB **84.0 × 97.5 m**; courtyard hole 494 m² (14.3 × 35.0 m) | OSM relation/12734194, measured via API |
| Anchor (OBB centre) | `-122.3900655, 37.7900324` | measured (footprint centroid is `-122.3901094, 37.7900484`, 4 m away — see 2.13) |
| LiDAR heights | `hgt_max` 68.46 m, median 28.36 m, majority (mode) 24.23 m, sd 12.38 m, ground 4.36 m NAVD88 | DataSF ynuv-fyni, `sf16_bldgid 201006.0000159`, `mblr SF3744002` |
| Target height | **68.5 m** — tower crown | LiDAR max; corroborated by storey math (7 office × ~4.0 m + 11 residential × ~3.2 m ≈ 63 m + mechanical crown) and by the ~200 ft height envelope reported for the project's approval (Hoodline). The sd (12.4 m) reflects the real multi-level massing, not noise |
| Podium roof | main wings ~24.2 m (LiDAR mode), upper band/parapet ~28.4 m (LiDAR median); Spear/Folsom corner reads 8 storeys in Street View | measured, mixture read — see 2.15 |
| Grid heading | long axis bearing 315.1° (Spear/Embarcadero direction); cross axis 45° (Folsom) | measured from OSM geometry |
| OSM `building:levels` | 5 — **wrong as a height source** (the relation averages the stepped podium; the tower is unmapped in OSM) | OSM; rejected |
| Overture height | 17.18 m / 5 floors on the twin trace — **also wrong**, copied from OSM levels | pipeline bake input; rejected as height, matters for exclusion (2.13) |

### 2.2 Sources

- https://www.openstreetmap.org/relation/12734194 — footprint (outer way 191970111, courtyard way 260320992)
- DataSF `ynuv-fyni` (LiDAR building footprints): `201006.0000159` = this building; `201006.0000430` = Hills Brothers Building (max 53.2 m)
- DataSF `acdm-wktn` (parcels): block **3744** is one merged ground parcel; active lots are 2 Harrison ×1, 345 Spear ×2, 75 Folsom ×67
- https://buehlerengineering.com/project/hills-plaza — 18-storey condo tower, 900,000 SF project, $60M, Koll Construction, architect Whisler-Patri
- https://rises.co/developments/hills-plaza — residences on floors 8–18, completed 1991
- https://hoodline.com/2015/08/two-hills-plaza-residents-talk-about-soma-in-the-1990s/ — 7 office storeys + 10–11 residential above, 67 condos, ~200 ft height context
- https://www.loopnet.com/Listing/345-Spear-St-San-Francisco-CA/8581973/ — 1989, Class A, Google anchor
- https://www.upi.com/Business_News/2004/08/16/Morgan-Stanley-Fund-buys-Hills-Plaza/43871092674205/ — two-building complex, ~600,000 SF offices
- SFGate John King, "Hills Plaza is contextualism at its best" (2011) — critical context (body behind paywall)
- **Street View** (keyless recipe, see `docs/asset-plans/10-south-park.md` §sources): pano `C5xDvyRE7u80VkU5YnWetQ` (389 The Embarcadero, camera 37.789978, −122.388798) — Embarcadero elevation + tower; pano `psfVQFdrsK5ierTdD5rYVg` (301 Spear St, camera 37.790086, −122.390919) — Spear/Folsom corner. *Observed.*
- **Esri World Imagery z19/z20** (georef in session scratch: z20 TL 37.7907946/−122.3911285, BR 37.7894380/−122.3894119) — roof plan, terrace, tower position. *Observed; imagery leans NE.*

### 2.3 Orientation and placement

Full-block frontage on three streets: Spear (west, bearing 315° frontage),
Folsom (north, 45°), The Embarcadero (east). Harrison side is occupied by the
Hills Brothers Building. The tower sits at the courtyard's south-east quarter,
between the courtyard and the Embarcadero frontage. The main office entry is
mid-block on Spear; the retail arcade faces the Embarcadero and the interior
plaza shared with 2 Harrison.

### 2.4 What each side shows

**East (Embarcadero)** — ground arcade of round-headed arches; 6–7 storey buff
brick elevation with precast string courses; a stepped-gable feature bay; the
white tower and its layered crown rising behind. *Observed (pano C5xD…).*

**North (Folsom)** — 8-storey street wall at the Spear corner stepping along
Folsom; upper floors set back behind the level-8 landscaped roof garden
(planting beds, a circular feature, small trees). *Observed (pano psfV… + z20).*

**West (Spear)** — buff brick punched-window grid, precast spandrels, dark
blue-green storefront band at ground; the red terracotta hip-roof pavilion
(~30 × 34 m in plan) mid-block above the entry. *Observed.*

**South (plaza/2 Harrison)** — office wings around the courtyard facing the
shared palm plaza; lower wing roofs ~24 m. *Inferred from satellite; not
street-visible.*

**Top** — four distinct roof states: the landscaped level-8 garden (Folsom),
grey mechanical roofs on the wings (~24 m), the red hip pavilion roof (Spear),
and the tower's stepped white crown with a dark mechanical core (68.5 m crest).
*Observed (z20).*

### 2.5 Recognition cues (ranked)

1. The white 18-storey tower with a stepped, layered crown at the Embarcadero
   corner of an otherwise mid-rise buff-brick block
2. The ground-floor arch arcade answering the Hills Brothers arches next door
3. The red terracotta hip-roofed pavilion on Spear
4. The level-8 roof garden and the private interior courtyard
5. Buff brick + precast banding, dark blue-green storefronts

### 2.6 Miniature translation

**Preserve** — the podium-vs-tower two-scale massing; the courtyard void; the
arcade rhythm; the red hip pavilion; the roof garden as a designed surface.

**Simplify / exaggerate** — the window grid becomes clean recessed bands; the
tower crown becomes 2–3 crisp setback steps; roof mechanicals become a few tidy
blocks; the garden becomes 3–4 planting beds + one circular feature.

### 2.7 Massing recipe

Author in building axes (long axis = Spear bearing 315°), then rotate the whole
model onto true heading before export. Dimensions from the measured OBB
(84.0 × 97.5 m) and the z20 roof plan; heights from 2.1.

1. Podium ring: full footprint with courtyard void, z 0–24.2, `Toy_sand`;
   ground floor arcade band z 0–6 with arched openings on the Embarcadero and
   plaza faces, `Toy_stone` piers, `Toy_navy` storefront glazing.
2. Upper podium band on the street frontages: z 24.2–28.4 set back ~2 m
   (`Toy_sand`), parapet `Toy_trim`.
3. Spear corner bay at Folsom rises to ~32 m (8 storeys observed).
4. Tower: ~24 × 34 m plan at the courtyard SE quarter, z 0–61 `Toy_white`
   body with `Toy_glass` window bands; crown steps at 61 → 64.5 → 68.5 m with
   a `Toy_roofd` mechanical core.
5. Spear pavilion: ~30 × 34 m, body to ~30 m, red hip roof `Toy_brick`
   crest ~35 m (estimated).
6. Level-8 roof garden (Folsom side): `Toy_stone` deck at 28.4 m, planting
   beds `Toy_mint`, one circular `Toy_trim` feature.
7. Wing roofs `Toy_roofd` at 24.2 m with 2–3 mechanical blocks.
8. Courtyard floor at z ~1 m: paving + planting.
9. Bevel 0.12 m, 2 segments, on hero edges only (budget).

### 2.8 Materials and palette

| Material | Hex | Used for |
|---|---|---|
| `Toy_sand` | `#ece4d4` | podium brick body |
| `Toy_stone` | `#d9d2c2` | arcade piers, base, terrace deck |
| `Toy_trim` | `#f3efe6` | precast bands, parapets, terrace feature |
| `Toy_white` | `#f7f4ec` | tower body |
| `Toy_glass` | `#2a4d73` | window grids |
| `Toy_navy` | `#2c4a70` | ground-floor storefront band |
| `Toy_brick` | `#c96f4a` | pavilion terracotta hip roof |
| `Toy_roofd` | `#45454a` | wing roofs, mechanical, tower core |
| `Toy_mint` | `#8fd0a8` | roof-garden and courtyard planting |
| `Toy_white_Glow` | `#f7f4ec` | the arcade arches at night (hero glow) |
| `Toy_gold_Glow` | `#caa64a` | a restrained tower-crown accent |

Night: hero glow = the arch arcade; supporting = a thin crown band. Day colors
of `_Glow` surfaces must match their non-glow neighbours (contract).

### 2.9 Top surface

The camera looks down: the roof garden, the courtyard, the red hip roof and the
stepped tower crown are the four signatures. Design all four deliberately;
no undesigned grey slab anywhere.

### 2.10 Scope

**In the GLB:** the 345 Spear building only (podium + tower + pavilion +
courtyard + terraces). **Not in the GLB:** the Hills Brothers Building
(2 Harrison — separate in-flight landmark), the shared palm plaza's trees,
streets, Muni platform, vehicles, people.

### 2.11 Triangle budget

Cap 24,000. Split: podium + arcade ~9k, tower ~5k, pavilion ~3k, roofscape +
garden ~4k, courtyard ~2k, reserve ~1k.

### 2.12 Draft manifest entry

```json
{
  "id": "345-spear",
  "file": "345-spear.glb",
  "anchor": [-122.3900655, 37.7900324],
  "targetHeightM": 68.5,
  "cat": 3,
  "name": "Hills Plaza (345 Spear)",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N
}
```

### 2.13 Integration notes (Case B)

- New landmark: add `pipeline/lib/landmarks.mjs` entry (`id: '345-spear'`) and
  re-bake. **BATCH mode** — bake for QA, then discard tiles before commit.
- **Bake-input rings near the anchor** (size `exclude` against `excluded()`'s
  min(centroid, any-vertex) test, per the Earl Warren / 150 South Park lessons):
  - own DataSF ring `201006.0000159` — centroid ~6 m from anchor (caught easily)
  - own Overture twin (id `98232020…`, 17.18 m) — centroid ~5 m (caught)
  - **Hills Brothers Building** (DataSF `201006.0000430`, Overture named ring,
    56 m): its north-west corner is ~35–40 m from our anchor. The sibling
    session ships it as its own landmark with its own exclusion, but at *our*
    bake time it may still be procedural — the radius must NOT reach any of its
    vertices or its centroid.
  - two unheighted Overture fragments east of the ring (centroids ~50–70 m,
    along the Embarcadero frontage) — check whether they fall inside the
    footprint's coverage at bake time; do not chase them with a bigger radius.
  - Preliminary safe window: **r ≈ 12–30 m** (own centroids at ≤6 m; nearest
    foreign vertex ~35 m). Verify with the real bake inputs before setting.
- Block 3744 is one merged assessor parcel (2 Harrison + 345 Spear + 67 condo
  lots) — parcel data cannot separate the two buildings; the LiDAR/Overture
  building rings can, and they are what the bake uses.
- Coordinate with the `pipeline/2-harrison` branch at batch time: the two
  exclusions are independent, but grep each plan for the other before merging.
- `loadRadius`: default rule gives max(2500, 68.5 × 30) = **2,500 m**; no
  `alwaysLoaded` (not skyline-scale).

### 2.14 Validation checklist

Standard checklist (see 501-second): fresh-scene re-import, min Z ≈ 0, centre
≈ 0,0, dims ≈ 84 × 97.5 × 68.5 m, ≤ 24k tris, all `Toy_*` flat, `_Glow` only
arcade + crown, no cameras/lights/animations, outward normals, renders from
export.

### 2.15 Open questions and risks

1. **The 68.5 m target is a LiDAR maximum.** Accepted here because the sd
   (12.4 m) reflects real stepped massing, the storey math lands at 63–66 m
   plus crown, and no canopy reaches a tower roof. If the build's Street View
   check contradicts it, prefer the measured crown and re-normalize.
2. **The tower's exact plan position/size is satellite-derived** (leaning
   imagery). ±3 m uncertainty; the courtyard hole in OSM constrains its west
   edge.
3. **Pavilion height (~35 m crest) is estimated** from shadow and storey count;
   no published figure. Openly inferred.
4. **The south (plaza) elevation is not street-visible**; it is a typological
   continuation of the courtyard elevations. Inferred.
5. **Podium level structure is a mixture read** (mode 24.2 / median 28.4):
   wings at ~6 storeys, street frontages at 7–8. The build should keep the
   two-level read; exact floor assignment is not critical at miniature scale.
6. **2 Harrison adjacency**: any geometry crossing the shared plaza line, or an
   exclusion radius reaching its rings, breaks the sibling landmark. The scope
   rule in Part 1 and the radius window in 2.13 both guard this.
