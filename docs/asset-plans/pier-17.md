# Pier 17 (The Embarcadero at Green Street) — SF-SIM asset plan

Built in 1912, Pier 17 is the third-oldest pier on the San Francisco waterfront:
a 232 m timber-and-concrete cargo shed running northeast into the bay beside the
Exploratorium's solar-roofed Pier 15, with the "Valley" and the Fog Bridge
between them. Its identity is the **plain cream stucco bulkhead front with a
full-width shallow gable**, a diamond-tipped **"PIER 17" sign** under a
**flagpole at the apex**, and one huge central door bay flanked by **weathered
diagonal-plank timber barn doors**. The camera sees a long, low white gable roof
pointing into the bay — the pier deck itself is part of the asset, because the
app's baked city renders no pier decks and the loader seats assets at water
level over open water.

**Deliverable:** a validated miniature GLB plus dossier, renders and report
under `artifacts/pier-17/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `pier-17` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3981053, 37.8022416` (model bbox centre; see 2.3) |
| Target height | **21.3 m** to the flagpole tip above water level (facade gable apex 16.9 m; shed ridge ≈ 14.0 m; deck +2.0 m — see 2.1) |
| Footprint | shed 232 × 43 m (10,161 m², measured, OSM); deck 243 × 53–61 m (13,024 m², measured, OSM) |
| Triangle cap | 12,000 |
| Category | `20` (warehouse) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh agent session.

````markdown
# Create a production-ready Pier 17 GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Pier 17 (The Embarcadero at Green
Street, San Francisco) and deliver it as a downloadable, validated GLB.

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
7. `artifacts/414-brannan/` — the closest reference implementation in spirit
   (industrial box, restrained palette, one hero identity feature, monitor/roof
   read from the air). Its `build_414_brannan.py` is the script skeleton to
   adapt, not to rewrite.
8. `docs/asset-plans/pier-17.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- The **pier deck as a plinth**: a 2.0 m concrete slab on the real OSM deck
  footprint, light concrete top, dark pile/fender sides dropping to water at
  y = 0. Over open water the loader seats the asset at water level
  (`Math.max(0, sampleElevation)` in `app/src/assets.js`), so the deck IS the
  ground this landmark stands on. Origin convention is the bridge/island one:
  base-centre at **water level**.
- The **cream stucco bulkhead front** (southwest, facing the Embarcadero): one
  full-width shallow gable, a recessed full-height central door bay holding an
  olive-gray roll-up door flanked by two **weathered diagonal-plank timber barn
  doors**, and the **"PIER 17" diamond-ended sign plate** centred in the gable.
- The **flagpole at the gable apex** with a small saturated pennant — the
  asset's bounding-box top at exactly 21.3 m.
- The **long, low gable shed roof** (ridge ≈ 14.0 m above water) reading white
  from the air, with a **weathered gray section near the Embarcadero end**, a
  **ridge skylight strip** (the night-glow hero), and a small clean RTU/vent
  cluster toward the bay end.
- The **notched bay end**: the northwest half of the shed stops ~5.7 m short of
  the southeast half (measured, OSM), with the deck apron continuing ~4 m
  beyond. Mount the **fog horn** — Pier 17 keeps the waterfront's last original
  fog horn — high on the bay-end gable as the storytelling accent.
- Long shed sides as **rhythm, not detail**: pilaster bays, a high strip of
  dark windows on the Valley (southeast) side where the renovation added
  glazing, plainer on the northwest side facing the Pier 19 slip.

## Research Pier 17 independently

Verify the dossier rather than trusting it. Re-check at minimum the
architectural height, both footprints, the WGS84 anchor and the real-world
orientation, and gather references covering:

- The bulkhead front (a July 2022 Wikimedia Commons photo is the primary
  street-level source, see 2.2)
- Aerial/satellite roof views (roof value split, ridge line, deck aprons)
- The bay end and both long sides, which have no good street-level imagery —
  everything said about them below eave level is *inferred* and 2.15 leads
  with that admission
- The Exploratorium campus context: do not model Pier 15, the Valley
  furniture, the Fog Bridge or the Observatory building

**Height traps already resolved in 2.1 — re-check, do not re-inherit:**

1. OSM tags the shed `building:levels=1` and carries **no height tag**. The
   solve is LiDAR-only, corroborated by photo proportions.
2. The LiDAR `peak_1st_m` of 19.26 m is the **flagpole**, not the roof
   (sd-test: `hgt_maxcm` 15.64 m is the facade gable apex; the roof plane
   majority is 10.46 m). The pole is modelled, so the export top IS the pole
   tip and `targetHeightM` = 21.3 m includes it.
3. All LiDAR heights are **above the pier deck**, and the deck is ~2.0 m above
   app water level (NAVD88 deck elevation 2.78 m, `p2010_zminn88ft`). Model
   heights = LiDAR height + 2.0.

## Create a reference dossier

Write `artifacts/pier-17/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from
all sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22. This is a
**secondary building with one hero feature** (§21): the spent exaggeration is
the **bulkhead gable + sign + flagpole** ensemble, thickened and slightly
oversized so the front reads at thumbnail size. The ridge skylight is the
night-state hero. Everything else is broad rhythm.

The finished asset must be immediately recognizable as this pier, consistent
with the real building from all sides and above, architecturally credible, and
a premium handcrafted miniature — never accurate in one view and invented in
the others.

## Scope of the exported asset

Export: the pier deck slab (real OSM deck ring), the shed with its notched bay
end, the bulkhead front composition, the roof design, the flagpole and pennant,
the fog horn, and restrained side fenestration.

Do not include: the Embarcadero, the bulkhead wharf, Pier 15 or 19 in any form,
the Valley, the Fog Bridge, the Observatory building, water, boats, mooring
dolphins, people, vehicles, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base centre **at water level** (bridge /
island convention); minimum geometry Z ≈ 0; applied transforms; no negative
scales; outward normals; no duplicate or foreign geometry; no image textures;
no transparency; flat-color materials named `Toy_*` from the project palette;
a `_Glow` set for the night state; no cameras, lights, animations, armatures
or constraints; ≤ 12,000 triangles; bounding-box top exactly 21.3 m.

**Traps this asset is squarely inside — read before building:**

- **True-world orientation**: the pier bears 54.9° (long axis pointing
  northeast into the bay). `placeGeneric()` never rotates, so author the GLB
  rotated into world axes (Blender +Y = north). The contract's "front faces
  −Y" is overridden by AGENTS rule 5; record the deviation in REPORT.md.
- **Authoring in rotated building axes**: the (s,w) → world map can be a
  reflection that inverts every winding — build through one projection helper
  and trust the validator's signed-volume test, not your eye.
- **`_Glow` day colours**: a glow material's base colour IS its night look and
  it renders unlit. Put glow panes on their own thin plates slightly proud of
  the opaque surface; never a closed glow shell, never a glow face flush ON a
  solid.
- **Never use `Toy_roofd` on a visible deck or roof** — it measures rgb(9,9,12)
  in-app. `Toy_steel` is the roof-membrane default; the weathered roof section
  and doors use it here.
- **The deck is one flat terrain-draped-like surface**: the loader seats from
  one sample at the anchor, and over water that sample is 0. Keep the deck top
  dead flat at +2.0 m.

## Deliverables

Under `artifacts/pier-17/`: `REFERENCE.md`, deterministic `build_pier_17.py` /
`render_pier_17.py` / `validate_pier_17.py` scripts, `pier-17.glb`, six review
renders plus a night render, a contact sheet, `validation.json` (all-PASS),
and `REPORT.md` documenting every dossier correction you made.

Draft manifest entry for the report (do not write it into the repo yet):

```json
{
  "id": "pier-17",
  "file": "pier-17.glb",
  "anchor": [
    -122.3981053,
    37.8022416
  ],
  "targetHeightM": 21.3,
  "cat": 20,
  "name": "Pier 17",
  "estimated": false,
  "dims": [
    234.1, 21.3, 182.9
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a
separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the
integration notes in `docs/asset-plans/pier-17.md`.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Source / method |
|---|---|---|
| Built | 1912 — third-oldest pier on the SF waterfront | Exploratorium press office ("Pier 15 Facts of Interest", April 2011) |
| Fog horn | last remaining original fog horn on the waterfront | same source |
| Campus | Piers 15/17 Exploratorium campus; Pier 17 leased to the Exploratorium (~110,000 sq ft footprint, expansion/back-of-house) | Exploratorium press office; Port of SF pier condition report (2017) |
| Campus architects (2010–13 rehabilitation) | EHDD Architecture; Page & Turnbull (historic preservation) | Port of SF project sheet, Dec 2010 |
| Shed footprint | 6-node OSM ring, 10,161 m²; OBB 232 × 43 m; notched bay end (NW half stops 5.7 m short) | OSM way `25489458`, projected and measured |
| Deck footprint | 16-node OSM ring, 13,024 m²; s ∈ [−119.3, +124.1] m, w ∈ [−35.7, +25.2] m in shed frame; SE apron 3.5 m, NW apron ~6.7 m (flaring to 10+ m at the front corner), bay apron ~4.3 m | OSM way `1390720126` (`man_made=pier`), projected and measured |
| Long-axis bearing | 54.9° (northeast into the bay); unit s = (0.81805, −0.57511) in app x/z | measured from OSM long edge |
| Deck elevation | 2.78 m NAVD88 (`p2010_zminn88ft` 9.1163 ft); modelled +2.0 m above app water level (estimated) | DataSF LiDAR `ynuv-fyni`, `sf16_bldgid 201006.0000005` |
| Roof plane | `hgt_majoritycm` 10.46 m, `hgt_median` 9.90 m above deck; 1st-return median 11.51 m (ridge influence) | same LiDAR row (102,761 cells) |
| Facade gable apex | `hgt_maxcm` 15.64 m above deck ≈ `p2010_zmax` 57.91 ft − deck 2.78 m = 14.87 m; modelled 14.9 m above deck (16.9 m above water) | same LiDAR row, two internally consistent statistics |
| Flagpole tip | `peak_1st_m` 19.26 m above deck → 21.3 m above water; corroborated by photo (pole rises well clear of the apex) | same LiDAR row + Commons photo |
| LiDAR vintage | flown 2010, published 2023 — predates the 2010–13 campus works, but the shed exterior is the preserved historic fabric | dataset metadata; Port project sheet |
| Anchor (model bbox centre) | x 3466.88, z −3564.00 → `-122.3981053, 37.8022416` | deck ring bbox in shed frame, reprojected |

Height ladder used by the build (all above app water level y = 0):
deck top **2.0** · shed eave **11.0** · shed ridge **14.0** · facade gable apex
**16.9** · flagpole tip **21.3** (= `targetHeightM`, the export's bbox top).

### 2.2 Sources

- **Wikimedia Commons** `File:Pier_17_(San_Francisco)_July_2022.JPG` — the
  primary street-level source: full bulkhead front, sign, flagpole with flag,
  central roll-up + timber barn doors, receiving door and window strip at the
  right (SE) edge. *Observed.*
- **Google satellite tiles z19/z20** over 37.8022, −122.3981 — roof value
  split (white membrane main run, weathered gray near the front, thin bright
  ridge line), deck aprons, notched bay end, Pier 15 solar roof context.
  *Observed (aerial).*
- **Exploratorium press office**, "Pier 15 Facts of Interest" (2011) — 1912
  date, third-oldest claim, fog horn, 110,000 sq ft. *Fact source.*
- **Port of SF**, Exploratorium project sheet (Dec 2010) — EHDD / Page &
  Turnbull, $205M rehabilitation, 2010–2013. *Fact source.*
- **Port of SF**, Embarcadero pier condition report (May 2017) — Pier 17
  leased to the Exploratorium. *Fact source.*
- **DataSF LiDAR** `ynuv-fyni` row `201006.0000005` (`mblr SF9900015`) — the
  full height solve in 2.1. *Measured.*
- **OSM** ways `25489458` (shed) and `1390720126` (deck). *Measured.*
- Exa queries used: "Pier 17 The Embarcadero San Francisco building history
  architect bulkhead"; "Pier 17 Embarcadero San Francisco facade photo
  bulkhead building Exploratorium"; "Pier 17 San Francisco 1912 built shed
  bulkhead Embarcadero historic district year constructed". Yielding domains:
  exploratorium.edu, sfport.com, commons.wikimedia.org, nps.gov,
  ohp.parks.ca.gov.

### 2.3 Orientation and placement

- Long axis bears **54.9°** — the shed points northeast into the bay; the
  bulkhead front faces southwest (234.9°) onto the Embarcadero at Green St.
- Author in building axes (s along the pier toward the bay, w toward the
  southeast/Valley side) and rotate into world axes in one projection helper:
  `x = s·0.81805 + w·0.57511`, `z = −s·0.57511 + w·0.81805` relative to the
  shed centroid (x 3467.93, z −3558.31), then translate so the **model bbox
  centre** sits at the origin. Blender +Y = north = −z.
- The manifest anchor is the **model bbox centre** `-122.3981053, 37.8022416`
  (deck bbox mid: s +2.41, w −5.26). The shed centroid and the deck centre do
  not coincide — the deck flares northwest at the front — so do not reuse the
  OSM shed centroid as the anchor.
- Origin at **water level** (y = 0), deck top at +2.0 m: over open water
  `placeGeneric()` clamps its terrain sample to 0, so the model's own deck is
  what lifts the shed.

### 2.4 What each side shows

- **Southwest (front, Embarcadero)** — *observed (Commons photo).* Cream
  stucco bulkhead, one full-width shallow gable (apex 14.9 m above deck,
  eaves of the gable sweeping to ~9 m at the corners). Centred recessed door
  bay (~28 m wide, ~7.5 m tall) framed by a plain cream surround: olive-gray
  roll-up centre (~12 m), weathered diagonal-plank timber barn doors either
  side (~8 m each). "PIER 17" sign plate with diamond ends centred above the
  door frame. Flagpole at the apex with a flag. At the right (SE) edge: a
  window band and small receiving door at grade.
- **Southeast (Valley side, faces Pier 15)** — *inferred.* Long cream wall in
  pilaster bays; the renovation added glazed roll-up bays opening onto the
  Valley: a high strip of dark windows over 6–8 door-height glazed bays along
  the middle third. 3.5 m deck apron.
- **Northwest (faces the Pier 19 slip)** — *inferred.* Plainest side: pilaster
  rhythm, 2–3 service doors, no glazing strip. ~6.7 m apron widening toward
  the front corner where the deck flares.
- **Northeast (bay end)** — *inferred + measured notch.* Gable end over the SE
  half; the NW half stops 5.7 m short (measured, OSM) with a lower flat-roofed
  end bay reading as a step. Large end door, fog horn mounted high in the
  gable, deck apron ~4.3 m beyond.
- **Roof (the real facade)** — *observed (aerial).* Low gable, ridge slightly
  SE of the OBB centreline; white membrane over most of the run; weathered
  gray over roughly the front 70 m; thin bright ridge line read as a ridge
  skylight strip (*inferred* as a skylight; the strip itself is observed);
  small equipment near the bay end.

### 2.5 Recognition cues (ranked)

1. A 232 m shed on its own pier deck pointing northeast into the bay, beside
   Pier 15's black solar roof.
2. The cream bulkhead front's full-width shallow gable + "PIER 17" sign +
   apex flagpole.
3. The huge central door bay: olive roll-up between weathered timber
   diagonal-plank barn doors.
4. The long white gable roof with its weathered gray front section and bright
   ridge line.
5. The notched bay end with the fog horn.

### 2.6 Miniature translation

- The deck is the ground: one crisp slab, light concrete top, dark sides to
  the water — it must read as "pier", not "barge". No piles modelled; the
  dark side face carries that meaning at this scale.
- The front ensemble (gable, sign, doors, pole) gets the detail budget; the
  sign plate and doors are slightly oversized (semantic scale) so the front
  reads from the app's aerial camera.
- The 232 m sides are rhythm only: shallow pilaster relief every ~14.5 m
  (16 bays), openings as inset dark panels, zero per-window geometry.
- The roof is designed as a graphic: two clean values (white + weathered
  gray), one glowing ridge strip, one small equipment cluster. Nothing
  scattered.
- One saturated accent: the pennant (Toy_ioorange). The fog horn stays steel
  — its shape is the accent.

### 2.7 Massing recipe

1. **Deck slab**: extrude the real 16-node OSM deck ring, y 0 → 2.0.
2. **Shed body**: the real 6-node OSM shed ring, y 2.0 → 11.0 (eaves), with
   the notched NW bay-end corner honoured.
3. **Gable roof**: ridge at 14.0 running the long axis (ridge offset ~1 m SE
   of the OBB centreline), hipped/stopped at the notch step at the bay end;
   generous eave overhang is NOT wanted — the historic shed roof is nearly
   flush.
4. **Bulkhead front plane**: the front wall rises past the roof line into the
   shallow gable parapet, apex 16.9. The gable is a parapet — the roof behind
   is lower; give the parapet real thickness (0.4 m) so it reads from above.
5. **Recessed door bay**: inset the front wall 0.6 m over a 28 × 7.5 m
   opening; fill with roll-up + barn-door planes ON the recessed plane
   (applied panels, no booleans — a recess built as a solid prism swallows
   the doors).
6. **Sign plate**: a thin proud plate (~7 × 1.4 m) centred at ~12.5 m, with
   diamond ends.
7. **Flagpole**: 6-sided pole from the apex to 21.3; pennant plate.
8. **Bay-end step**: the NW half's end wall at s ≈ +114, the SE half's at
   s ≈ +119.6, both gabled/stepped; fog horn (two stacked cylinders + cone
   mouth, ~1.5 m) high on the SE gable.
9. **Ridge skylight**: a 0.5 m wide, ~130 m long raised strip (0.25 m tall)
   along the middle of the ridge — glow plate on top, steel curb sides.
10. **Roof equipment**: 3 clean blocks near the bay end.
11. **Side fenestration**: Valley side — 7 glazed bay panels + high window
    strip as inset panels; NW side — 3 door panels. All applied/inset planes.

### 2.8 Materials and palette

| Material | Hex (sRGB) | Use |
|---|---|---|
| `Toy_trim` | `f3efe6` | shed walls, bulkhead front, gable parapet, sign plate frame |
| `Toy_stone` | `d9d2c2` | deck top, main roof membrane |
| `Toy_steel` | `9aa0a6` | weathered front roof section, roll-up door, flagpole, fog horn, RTUs, skylight curb |
| `Toy_rust` | `a86444` | timber barn doors (diagonal plank relief ≤ 3 mm) |
| `Toy_ink` | `3a3530` | deck slab sides (pile/fender line), sign lettering band, door reveals |
| `Toy_glass` | `2a4d73` | side glazing, high window strips, day state of non-glow skylight segments |
| `Toy_ioorange` | `c0402a` | pennant only |
| `Toy_glass_Glow` | `6f95b8` | ridge skylight strip (night hero), 3 of the 7 Valley-side glazed bays |
| `Toy_trim_Glow` | `f3efe6` | sign plate face, front transom strip over the roll-up |

Glow discipline: glow faces live on their own thin plates slightly proud of
opaque surfaces; no closed glow shells; day colours of glow materials match
their non-glow neighbours.

### 2.9 Top surface

The roof is the primary facade: white membrane main run (`Toy_stone`),
weathered gray front ~70 m (`Toy_steel`), bright ridge skylight strip with a
night glow, one RTU cluster (3 blocks) near the bay end, parapet gable reading
as a crisp cream band across the front from above, and the deck aprons framing
the shed on all four sides. No blank surprises from the app camera.

### 2.10 Scope

Included: deck slab, shed, roof design, front ensemble, flagpole + pennant,
fog horn, side fenestration panels. Excluded: Piers 15/19, the Valley, Fog
Bridge, Observatory, bulkhead wharf, the Embarcadero, water, boats, mooring
dolphins, cranes, people, vehicles.

### 2.11 Triangle budget

Cap **12,000**; expected ~6,000–8,000. Biggest spends: the two OSM rings
(deck 16 verts, shed 6 verts — cheap), pilaster relief (16 bays × 2 sides),
door/window inset panels, the fog horn cylinders, chamfered edges on deck,
parapet and sign. Bevel only silhouette edges (deck rim, parapet top, sign
plate); never bevel flat inset panels.

### 2.12 Draft manifest entry

See Part 1. `loadRadius` 2500 (default rule `max(2500, 21.3 × 30 = 639)`);
not `alwaysLoaded` — it is neighborhood-scale, not skyline-scale.

### 2.13 Integration notes (Case B)

- **Registry entry** (`pipeline/lib/landmarks.mjs`): id `pier-17`, lon/lat =
  the manifest anchor, height 21.3, **exclusion radius 100 m**.
- **The exclusion window is (78, ~137) m, measured from the shipped tiles**
  (cell `22_8`, decoded 2026-08-19): the baked Pier 17 is one merged DataSF
  trace (`b13`, base −0.3 m, top 15.4 m, bbox x 3359–3633, z −3647–−3383)
  whose gate distance — min(centroid, nearest vertex) from the anchor — is
  **77.5 m** (centroid; the merged trace's centroid sits 72–78 m from the
  anchor because it includes a southeast lobe toward Pier 15). The nearest
  building that must survive is Pier 19's trace (`b14`, gate 143.5 m from
  the shed centroid, ≥ ~137 m from the model anchor). Pier 15's shed
  (`23_9 b6`) gates at 204.5 m. **r = 100** clears both sides comfortably.
- **Post-bake checks specific to this pier**: (1) the merged trace's SE lobe
  overlaps Pier 15's own surviving trace — confirm the campus SE of the
  Valley is still covered after `b13` drops; (2) the Overture twin is caught
  by its centroid — verify which rings dropped, not how many; (3) the
  Overture height-correction can re-target onto the nearest survivor — check
  Pier 19/15 heights are unchanged after the bake; (4) new Overture gap-fill
  rings can appear only after a batch bake — re-check the cell then.
- **Streaming**: `loadRadius: 2500` → expect the streamed-fallback warning
  text variant, not the INTEGRATION-PROMPT Step 6 wording, during the drill.
- **Fallback drill**: Case B leaves an empty pier deck by design once the
  tiles are re-baked — one console warning, no crash, water where the pier
  was. Record it as expected behaviour.
- **Batch mode**: run the bake for QA, then discard
  (`git checkout -- app/public/tiles api/_data`) and commit source only.

### 2.14 Validation checklist

Standard contract checks plus, specific to this asset: bbox top exactly
21.3 m; minimum Z ≈ 0 (water); deck top exactly 2.0 m; the deck ring matches
the OSM pier way (not the shed way); orientation check — bay end toward
northeast (+x, −z), front toward southwest; the notch at the bay end on the
NW side (not SE); ray-test residual 0 expected only if built as a union of
closed solids — per-object signed volume is authoritative.

### 2.15 Open questions and risks

1. **No street-level imagery of the sides or bay end was found.** Both long
   elevations and the bay end are typological reconstructions constrained by
   the aerial views and the front photo. The Valley-side glazing count and
   the bay-end door are honest inventions in the shed's own language. If
   side-on photos surface later, revise before optimize.
2. **The deck height above app water level (2.0 m) is estimated.** NAVD88
   numbers put the real deck 1.8–2.8 m above local water datums depending on
   which datum the app's y = 0 really corresponds to. 2.0 m reads correctly
   at toy scale; the risk is cosmetic only.
3. **The ridge strip is observed; "skylight" is inferred.** The bright line
   along the ridge in satellite imagery is read as a ridge skylight (standard
   for 1910s pier sheds). If it is in fact a membrane cap, the night glow is
   an editorial choice — restrained enough to keep.
4. **LiDAR vintage (2010) predates the campus rehabilitation.** The historic
   shed envelope was preserved, so the height solve stands; but any new
   rooftop equipment added 2010–13 is invisible to it. Satellite shows only
   modest equipment — modelled as 3 small blocks.
5. **The merged baked trace (2.13) is the integration's real risk** — the
   exclusion drops a footprint bigger than the asset. The post-bake check
   list in 2.13 is mandatory, not advisory.
6. **`peak_1st_m` as the flagpole** is an interpretation (first-return single
   maximum). The photo confirms a tall pole; if the pole were shorter the
   only casualty is a slightly tall pole tip — the massing is unaffected.
