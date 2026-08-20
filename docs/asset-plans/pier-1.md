# Pier 1 — SF-SIM asset plan

The first pier north of the Ferry Building, and the first **pier** in the landmark set: a
1918–1931 finger pier whose Neo-classical **bulkhead building** stands on the Embarcadero
building line with a monumental round-arched entry carved `PORT OF SAN FRANCISCO` and
`PIER · 1` in its frieze, and whose **213 m timber-and-concrete transit shed** runs
north-east into the Bay behind it under a flat white roof striped with two long solar
arrays. Rehabilitated in 2001 (SMWM, $42 M) as the Port of San Francisco's headquarters
and Prologis's, it is a National Register listing (#98001551) and a contributor to two
historic districts.

Three things make it unlike every landmark shipped so far:

1. **It stands in water.** The app's terrain under it is the ~2.3 m ridge the Terrarium DEM
   makes of the pier deck; the asset must carry its own **deck, fascia and pile stubs**, and
   its origin sits at deck level, not at a shoreline. See 2.3.
2. **It is 226 m long and 65 m wide** — the longest landmark footprint in the set after the
   bridges — and it is a *taper*, not a box: 41 m wide at the shed head, 36 m in the body,
   26.5 m for the outer 100 m.
3. **Its exclusion cannot be a single circle around the anchor.** The bake carries Pier 1 as
   two overlapping footprints, one of which is a merged Overture polygon that also traces the
   Piers 1½–5 bulkhead row. The zone list is solved and verified in 2.13 — read it before
   touching `pipeline/lib/landmarks.mjs`.

Its neighbour `ferry-building` is already in the manifest 250 m to the south. The two must
not read as siblings: the Ferry Building is a 74.7 m grey arcaded hall with a clock tower;
Pier 1 is a 12.8 m cream shed-with-a-frontispiece that is mostly *length*. Build that
difference.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/pier-1/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `pier-1` (registry id `pier1`) |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3940638, 37.7974811` (model bbox centre) |
| Target height | **15.4 m** — this is the model's total **vertical extent** (pile-stub bottom −2.6 m to pavilion apex +12.8 m above the pier deck), *not* a height above water. See 2.1 and 2.3 |
| Footprint | Building 226.4 m x 64.7 m; pier deck ~234 m x ~52 m; measured from OSM way 25489482 and DataSF `ynuv-fyni` area_id 146 |
| Axis heading | Long axis bears **053.8°**; the Embarcadero facade faces **233.8°** |
| Triangle cap | 24,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Pier 1 GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of Pier 1, San Francisco (The Embarcadero at
Washington Street) and deliver it as a downloadable, validated GLB.

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
7. `docs/asset-plans/ferry-building.md` and `artifacts/ferry-building/` — the nearest
   reference in site and typology (250 m south, same waterfront, same Beaux-Arts family).
   Read it for the *method*, not the *look*: the Ferry Building is a tall grey arcaded hall
   with a tower; Pier 1 is a low cream shed with one frontispiece. They must not read as
   siblings.
8. `docs/asset-plans/alcatraz-island.md` §"Ground rules specific to this asset" — the only
   other plan whose asset stands in water; read its origin rule and then read **2.3 below**,
   which deliberately differs from it.
9. `docs/asset-plans/pier-1.md` — this plan, whose dossier is your research starting point,
   not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **three-part plan**: a shallow 64.7 m x 12.5 m **bulkhead building** on the Embarcadero
  line; a **41 m-wide shed head** behind it; and a **213 m shed** that steps down to 36 m and
  then tapers to 26.5 m for its outer 100 m. The taper is real and is what stops the model
  reading as an extruded rectangle.
- The **frontispiece**: a central pavilion roughly 22 m wide breaking forward and up out of
  the two-storey wings, with a **monumental round arch ~10 m wide** (radiating voussoirs,
  keystone, quoined pilasters at the pavilion corners), a dentilled entablature carrying
  **`PIER · 1`**, and a low raked pediment above it. `PORT OF SAN FRANCISCO` runs in a band
  across the glazed lunette. This is cue #1 and may be enlarged per style bible §8/§9.
- The **wing rhythm**: broad flat pilaster strips dividing each wing into bays, each bay
  carrying a band of 3–4 narrow tall steel-sash windows at the upper level; at ground level
  a **second, smaller arched vehicle portal** through the NW wing (the historic Belt Railroad
  pass-through, and a real hole you can see the Embarcadero through), plus shopfronts and
  doors.
- The **shed flanks**: a repeating structural bay ~7.5 m wide with a slightly projecting
  pilaster and a small corbel cap; a **tall main window group** and a **continuous clerestory
  band** just under a flat coping; a belt course and a plinth. Both flanks are finished — the
  camera sees them from the Embarcadero and from the Bay.
- The **roof as a facade** (style bible §10): flat pale membrane, a **raised monitor spine**
  running the length of the shed at ~12.4 m, **two long dark solar arrays** flanking it (the
  outer third of the shed is nearly fully covered), roof hatches, round vents, and the lower
  flat roof of the bulkhead wrapping the shed head.
- The **pier itself**: the concrete deck with its **apron promenade** on both flanks (≈11 m
  NW, ≈7 m SE) and around the NE end, the deck **fascia**, a suggestion of **pile bents**
  below it, the **guard railing**, bollards, and the row of globe lamp standards along the
  SE apron. Without the deck the building floats.
- The **cream / slate-blue two-colour discipline**: warm off-white painted stucco and concrete
  everywhere, slate blue-grey steel window frames and doors, dark blue-grey glazing. Pier 1
  has no third colour.

## Research Pier 1 independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint and its taper, the WGS84 anchor, the pier deck
elevation, and the real-world orientation, and gather references covering:

- The Embarcadero (south-west) elevation head-on and obliquely
- Both shed flanks (north-west from the Pier 3 slip, south-east from the Ferry Building side)
- The north-east end and the open deck beyond it
- Aerial / roof views — the monitor spine, the solar arrays, the bulkhead's flat roof
- Day and night appearance, and what is actually lit at night
- The bay count and window rhythm on the wings and on the shed flanks — the dossier's
  "3–4 narrow windows per wing bay" and "~7.5 m shed bay" are *inferred* from oblique
  Street View and must be confirmed

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. The National Register nomination (#98001551) and the Central Embarcadero Piers
Historic District nomination (#02001390) are the primary documents. Never rely on a single
photograph, a single AI-generated image, or a single unsourced 3D model. Separate verified
facts from visual inference; if sources disagree, document the disagreement and decide.

**Four source traps are already known and resolved in 2.1 — re-check them, do not silently
re-inherit the wrong value:**

1. OSM `height=10` on way 25489482 is the shed's eaves-ish figure and is **not** the crest.
   The crest is the bulkhead pavilion at ~12.8 m.
2. The DataSF LiDAR record (`ynuv-fyni` area_id 146) reports `hgt_maxcm = 1273` and
   `p2010_zmaxn88ft = 39.86` **and the two cannot both be relative to the same datum** — a
   building whose top is 12.15 m NAVD88 cannot also be 12.73 m above an Embarcadero pavement
   that is itself ~3 m NAVD88. Over water the LiDAR "ground" surface is meaningless. The
   12.8 m crest in this plan is photogrammetric (2.1) and happens to agree with `hgt_max`;
   treat that agreement as a corroboration, not as a licence to trust the record's datum.
3. Sources disagree on the build date — 1918 (Wikipedia, district nomination, "opened 1918"
   under Chief Engineer Frank G. White) vs 1931 (NRHP #98001551, "Built 1931"). Both are
   probably right about different things (bulkhead design by A. A. Pyle c.1914–18; the
   present concrete pier and shed completed 1931). Say so rather than picking one.
4. Several sources call the building a "700-foot" or "770-foot" warehouse. The measured
   building is 226.4 m (743 ft) and the pier deck ~234 m (768 ft). Use the measurement.

## Create a reference dossier

Write `artifacts/pier-1/REFERENCE.md` containing: source links and what each establishes;
verified dimensions and location; orientation; observations from all four sides and above;
the 3–5 strongest recognition cues; features to preserve; features to simplify;
uncertainties and conflicting evidence. A contact sheet of attributed reference thumbnails
is welcome if legally permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few confident
volumes, exaggerate only the signature features, simplify the facade into broad rhythms,
deliberately design every surface visible from above, evaluate from the app's high
three-quarter aerial camera, then simplify again.

This is a **hero landmark** in the style bible's detail budget (§21) but a *quiet* one: its
drama is one frontispiece and 213 m of disciplined repetition. Spend the budget on the
pavilion, the taper, the roof and the deck; do not enrich the shed bays past what the aerial
camera resolves. The failure mode here is a beautifully detailed arch on a featureless grey
noodle — the shed is 90% of the pixels and has to be *designed*, not extruded.

The finished asset must be immediately recognizable as Pier 1, consistent with the real
building from all four sides and above, architecturally credible, and a premium handcrafted
miniature — not photorealistic, not voxel art, not generic low-poly, and never accurate in
one view while invented in the others.

## Scope of the exported asset

Export the pier: the deck slab with its fascia and a suggestion of pile bents, the apron
promenade surface, the guard railing, bollards, the SE apron's globe lamp standards, the
bulkhead building, the shed, and all roof furniture.

Do not include unrelated surrounding city geometry: the Embarcadero roadway, its streetcar
tracks, palms or promenade paving outside the pier; Pier 1½, Pier 3, Pier 5 or the Ferry
Building; the moored ferries, the historic ship *Santa Rosa*, the floating docks in the
slips; the water surface; people, vehicles, plinths, cameras or lights. Temporary tenant
signage must not be modelled. Temporary context may appear in review renders but must not
leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; applied transforms; no negative scales; outward normals; no duplicate or
foreign geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`;
no cameras, lights, animations, armatures or constraints; no external dependencies; at most
24,000 triangles.

**Origin — this asset breaks the usual rule, read 2.3 before building.** The origin is at
**pier-deck top level**, centred in x/y on the model's bounding box, and geometry extends
**below** local z=0 (down to −2.6 m: deck fascia and pile stubs). It does *not* sit on z=0.
The loader seats the origin on the app's terrain sample at the anchor, which at this anchor
is the ~2.4 m DEM ridge that stands in for the pier deck; the sub-deck geometry then reaches
just under the water plane, which is exactly right.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops into
the city at its real-world heading — the loader applies no rotation (`placeGeneric` in
`app/src/assets.js` only scales and positions). The pier's long axis bears **053.8°** and the
Embarcadero facade faces **233.8°**; build directly on the measured footprint polygon in 2.3
rather than modelling an axis-aligned pier and rotating it.

**Height normalization:** the model's total vertical extent (lowest pile-stub geometry to the
pavilion apex) must land at exactly **15.4 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. Record in `REPORT.md`, in bold, that `targetHeightM` here is a vertical extent
and not a height above water — the same convention `64-south-park` uses.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/pier-1/build_pier_1.py` (deterministic build script),
`artifacts/pier-1/pier-1.blend`, and `artifacts/pier-1/pier-1.glb`. The script must rebuild
the model reliably enough for future revision. Do not modify or rename an unrelated existing
GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `pier-1-top.png`,
`pier-1-north.png`, `pier-1-east.png`, `pier-1-south.png`, `pier-1-west.png`, plus
`pier-1-contact-sheet.png`, at least one high three-quarter aerial beauty render
`pier-1-aerial.png`, and a night render `pier-1-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the top
view must clearly show the taper, the monitor spine, both solar arrays, the bulkhead's flat
roof and the apron. The aerial view uses the style bible's camera assumptions (30–50° down,
long lens).

Aim the hero aerial from the **south-west**, over the Embarcadero, so the frontispiece, the
SE flank, the taper and the whole roof are in frame at once — that is the view the app's
camera actually gets. Add one second aerial from the **north-east**, down the pier toward the
city, because the shed's outer end and the open deck are what the Bay side sees.

At 226 m the elevations will be extremely wide; render them at a long aspect (e.g. 3200×600)
rather than squeezing them into a square, and keep the contact sheet legible.

**Night render:** copy `Base Color` into `Emission Color` at strength 1.0 on every `_Glow`
material before rendering the re-imported GLB — glTF writes `emissiveFactor = 0` for
authored strength 0, so raising `Emission Strength` on a re-import renders every glow surface
white. See `docs/asset-plans/README.md`, "Night renders".

## Validate the exported GLB

Re-import `pier-1.glb` into a fresh isolated Blender scene and validate the re-import, not
the source scene. Report object count, triangle count, dimensions, bounding-box min/max,
min Z, XY center offset, material names, image-texture count, camera count, light count,
animation count, applied-transform status, negative-scale status, normal-orientation status,
unexpected geometry, and per-material contract compliance. Render at least one review image
from the re-imported asset. Write `artifacts/pier-1/validation.json` and
`artifacts/pier-1/REPORT.md`.

Two expected results that are **not** failures, and must be stated as such in
`validation.json` so the next reader does not "fix" them:

- **min Z ≈ −2.6 m, not 0.** Deliberate; see the origin rule above and 2.3.
- The axis-aligned XY bounding box will be roughly **185 × 190 m** even though the pier is
  234 × 52 m — the consequence of a 53.8° real-world heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and the vertical extent yourself, then include this draft entry
in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "pier-1",
  "file": "pier-1.glb",
  "anchor": [
    -122.3940638,
    37.7974811
  ],
  "targetHeightM": 15.4,
  "cat": 3,
  "name": "Pier 1",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 3000
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or
any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/pier-1.md` §2.13, which contains a solved and verified exclusion-zone list
that must not be re-derived by the usual half-diagonal rule.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Confidence / source |
|---|---|---|
| Name | Pier 1 (Pier One) | NRHP #98001551 |
| Address | The Embarcadero at Washington Street, San Francisco, CA 94111 | NRHP; CEQANet 1998122027 |
| OSM way | `25489482` (`man_made=pier`, `building=yes`, `height=10`, `wikidata=Q66078388`) | measured, OSM API |
| DataSF footprint | `ynuv-fyni` area_id **146** | measured |
| Built | Bulkhead designed c.1914–18 by **A. A. Pyle** (Neo-classical); pier substructure and shed by **A. C. Griewank** under Chief Harbor Engineer Jerome Newman; piers 1, 1½, 3, 5 "opened 1918"; NRHP records the pier as **built 1931** | Port of SF historic-piers RFI; Wikipedia; NRHP — *sources disagree, see trap 3* |
| Rehabilitated | **2001**, $42 M, architect **SMWM** (interiors TEF; Perkins&Will as architect of record for the Prologis/AMB fit-out); seismic retrofit by Rutherford + Chekene (70 piles to 170 ft) | BD+C "Bayside Renaissance"; TEF; Perkins&Will; ASCE 10.1061/40555(2001)84 |
| Use | Port of San Francisco HQ (52,000 sf) + Prologis (formerly AMB) HQ (36,800 sf); public conference centre and Port Walk | TEF; Perkins&Will; sfbeautiful.org |
| Listings | NRHP #98001551; contributor to Central Embarcadero Piers HD (#02001390) and Port of SF Embarcadero HD (#06000372) | noehill.com |
| Building footprint | **226.4 m** (along axis) × **64.7 m** (bulkhead frontage) | measured, OSM way 25489482 reprojected |
| Shed widths | head 41.0 m (along −11.5…19); body 36.2 m (along 19…97); tapers to **26.5 m** by along 149 and holds it to the NE end | measured, OSM ring |
| Pier deck | ~234 m × ~52 m; apron ≈ 11 m NW, ≈ 7 m SE, deck ends ~7 m beyond the shed at the NE tip | measured, Google satellite ortho at 0.08 m/px, georeferenced |
| Shed parapet | **9.7 m** above the deck | DataSF `hgt_mediancm = 966` |
| Shed monitor crest | **~12.4 m** above the deck (*estimated*) | shadow-length measurement on the ortho + DataSF `hgt_max` |
| Bulkhead wing parapet | **~8.6 m** above the deck (*photogrammetric*) | Street View pano `1DM4N8vgxv7QnYRcyFabrQ`, self-calibrated on the sidewalk line |
| Bulkhead pavilion apex | **~12.8 m** above the deck (*photogrammetric*) | same pano; agrees with DataSF `hgt_maxcm = 1273` |
| Flagpole tip | ~17.9 m (*photogrammetric*) — **deliberately not modelled**, see 2.10 | same pano |
| Pier deck elevation | ~2.9–3.0 m above water in the real world; **2.4 m** in the app's terrain at the anchor | app `terrain.bin` sampled directly; see 2.3 |
| Long-axis heading | **053.77°**; Embarcadero facade normal **233.77°** | measured from the OSM ring's NW edge |
| Anchor (model bbox centre) | `-122.3940638, 37.7974811` | derived |

### 2.2 Sources

- **NoeHill / NRHP #98001551** — "Pier One, The Embarcadero At Washington, Built 1931"; finger-pier typology, 49 built / 11 surviving.
- **NoeHill / NRHP #02001390** — Central Embarcadero Piers Historic District (Piers 1, 1½, 3, 5, 1918–1931); "the southernmost Beaux-Arts grouping along the Embarcadero".
- **Wikipedia, *Central Embarcadero Piers Historic District*** — "timber-frame bulkhead buildings, covered in stucco, are each two stories high", two-story arches, Chief Engineer Frank G. White, opened 1918.
- **Port of San Francisco, *Historic Piers RFI* (2018)** — bulkhead by A. A. Pyle, pier and shed by A. C. Griewank under Jerome Newman; reinforced-concrete pile substructure, timber shed framing, timber bulkhead with stucco exterior, concrete cargo aprons; monumental arched entry with keystone and voussoirs, quoins, and the Pier 1 rehabilitation completed **2001**.
- **BD+C, "Bayside Renaissance"** — SMWM, Nibbi Brothers, $42 M, 18-month schedule, 70 seismic piles up to 170 ft × 4 ft, bay-water heat exchanger, ~50,000 sf of added mezzanine.
- **TEF Architecture** — Port of San Francisco HQ, 52,000 sf, mezzanine + bulkhead build-out, 2004 Chronicle/AIA "Best of the Bay" Green Design Award.
- **Perkins&Will** — Prologis HQ, 36,800 sf, "opened 2001", NRHP-listed, blueprint for the Ferry Building and Exploratorium projects.
- **Bendheim** — 23 ft Solar channel glass at the conference volume; first channel-glass use in an NRHP-listed building.
- **Architizer / AMB Property Corp at Pier 1** — "civic wood-frame bulkhead structure and a 700-foot long concrete/steel warehouse"; added window openings, operable windows, daylighting.
- **ASCE 10.1061/40555(2001)84** — Rutherford + Chekene, "Renovation and Seismic Rehabilitation of Pier 1".
- **CEQANet 1998122027** — Pier 1 Project NOD, "The Embarcadero at Washington Street, San Francisco, CA 94111".
- **Imagery used for measurement** — Google satellite tiles z19–z21 resampled into a
  georeferenced ortho in the pier's own axis frame at 0.06–0.08 m/px; Google Street View
  panoramas `1DM4N8vgxv7QnYRcyFabrQ` (Embarcadero, facade head-on), `_Ck7UJ3tYOXhMEKksKQ_sQ`
  (Embarcadero looking SE), `49eksWulVaXoab8glx3Csw` and `BZMmgVxQOmLDPvPLxWlRYQ` (NW apron,
  shed flank), `3sGpaIsliCS9vamaU6ue_A` (NE end), `9ej82SMckZ5tGtAE8tLolw` (inside the
  bulkhead passage), `Z3h5-nCuEKUDIV51fDXmVA` (Ferry Building promenade, long view).
  *Observed*, not documentary.

### 2.3 Orientation, placement, and the water problem

The pier's own frame is used throughout this dossier: **along** runs north-east on bearing
053.77° with its zero at the shed's NW corner on the bulkhead's inner line
(x 3738.11, z −2995.37 in the app's local metres); **perp** runs 90° clockwise from it,
positive toward the south-east. The Embarcadero facade is the plane `along = −24.2`.

Measured ring (OSM way 25489482), in `(along, perp)` metres:

```
(-23.8,-14.2) (-11.8,-14.1) (-10.7,-14.0) (-10.6,-10.5) (-10.4, -5.8) ( -9.1, -5.9)
(  0.0,  0.0) (201.2, -0.0) (201.3,  2.4) (202.1, 23.4) (202.2, 26.7) (149.1, 26.5)
( 96.7, 36.3) ( 30.4, 35.8) ( 19.3, 34.5) ( 18.7, 36.7) ( 18.8, 41.0) (-11.5, 40.9)
(-11.6, 50.6) (-23.5, 50.4) (-24.2, 15.4) (-23.9,-10.4)
```

Read as massing: a **12.5 m-deep bulkhead slab** across `along −24.2 … −11.5`, `perp −14.2 …
50.6`; a **shed head** `along −11.5 … 19`, `perp 0 … 41`; a **shed body** `along 19 … 97`,
`perp 0 … 36.2`; a **taper** `along 97 … 149` closing to `perp 26.5`; and a **constant outer
run** `along 149 … 202`, `perp 0 … 26.5`. The pier **deck** extends about 11 m beyond the
shed's NW wall, 7 m beyond its SE wall, and about 7 m past the NE end (to `along ≈ 209`).

**The water problem, and why this asset's origin is not on z=0.**

`placeGeneric()` does exactly this:

```js
const scale = entry.targetHeightM / size.y;
const [x, z] = data.project(entry.anchor[0], entry.anchor[1]);
const y = Math.max(0, data.sampleElevation(x, z));
```

— one terrain sample at the anchor, and the GLB's origin goes there. The contract's usual
rule ("min-z ≈ 0, the model sits on the ground") assumes the terrain sample *is* the ground
the building stands on. Over the Bay it is not. Sampling the app's own `terrain.bin` across
the site gives:

```
along     -40   -20     0    20    60   100   140   180   200   220
perp -20  3.1   2.9   1.4   0.6   0.2   0.1   0.2   0.2   0.0   0.0
perp   0  3.0   2.8   2.2   2.1   2.2   2.1   2.2   2.1   0.7   0.0
perp  20  2.9   2.5   2.3   2.5   2.5   2.4   2.0   1.5   0.7   0.0
perp  40  2.9   2.9   2.0   1.8   1.0   0.5   0.1   0.0   0.0   0.0
```

The Terrarium DEM already carries the pier as a ~2.1–2.5 m ridge along its centreline, with
water (0.0) either side and beyond the tip. That ridge is the app's stand-in for the pier
deck, and it is within half a metre of the real deck elevation (~2.9 m).

So: **author with local z = 0 at the top of the pier deck.** Deck slab, fascia and pile
stubs run down to **z = −2.6 m**; the shed parapet is at +9.7; the pavilion apex at +12.8.
Placed at the anchor the deck lands at ~2.4 m world, the pile stubs reach ~−0.2 m — just
under the water plane, where they belong — and at the tip, where the DEM has fallen to 0,
the deck correctly reads as a structure standing 2.4 m out of the water on piles.

Consequences to hold on to:

- `targetHeightM = 15.4` is `size.y`, the **vertical extent** from −2.6 to +12.8. It is not a
  height above water and not an architectural height. `64-south-park` set this precedent.
- `min Z ≈ −2.6` is a **PASS**, and `validation.json` must say so explicitly.
- Do not "fix" the model by dropping it onto z = 0; that raises the whole pier 2.6 m.
- The bulkhead end sits over terrain of ~2.8–3.0 m while the model's deck lands at ~2.4 m,
  so the bulkhead's plinth is buried by ~0.5 m at the Embarcadero. That is the right way
  round (buried, not floating) and the plinth must be deep enough to absorb it.

`yawDeg` is **not** used: author in true-world orientation, `+Y` north.

### 2.4 What each side shows

**South-west — the Embarcadero facade (bearing 233.8°).** The face everybody photographs.
A flat 64.7 m two-storey wall of warm off-white painted stucco with a plain coping, broken
in the middle by a ~22 m pavilion that steps forward and up. The pavilion: quoined pilaster
strips at its corners; a **monumental round arch about 10 m wide**, springing at ~5.5 m and
crowning at ~9.3 m, with radiating voussoirs and a keystone; a dentilled entablature at
~10.0 m carrying **`PIER · 1`** in widely-spaced serif capitals; and a low raked pediment
above, apex ~12.8 m, with a small blocky finial and a flagpole. The arch is filled with a
dark gridded glazed lunette; a band across it reads `PORT OF SAN FRANCISCO`; below that a
glazed door screen. The wings: broad flat pilaster strips divide each into bays, each bay
carrying 3–4 narrow tall multi-pane steel-sash windows at the upper level. At ground level
the NW wing is pierced by a **second, smaller flat-arched portal** — the Belt Railroad
pass-through, still open, and you can see the street through it from the pier deck. Shopfront
glazing and doors fill the rest.

**North-west — the shed flank onto the Pier 3 slip.** ~213 m of the same cream wall on a
repeating structural bay ≈ 7.5 m: a slightly projecting pilaster with a small corbel cap,
then a **tall main window group** (a large steel-sash light over a transom band, ~3.5 m tall)
sitting on a belt course at ~2.2 m, and above it a **continuous clerestory band** of
horizontal multi-pane sash tucked just under the coping. Every few bays the main opening is a
double glass door instead. A plinth runs the length. The parapet is dead level; the roof is
not visible from the apron. A caged roof ladder near the NE end is the only interruption.

**South-east — the shed flank onto the Ferry Building.** The same system, and the side the
city's camera sees most: this is the elevation that faces downtown and the Ferry Building
promenade. Its apron carries the row of **globe lamp standards** and most of the benches.

**North-east — the end.** A blunt 26.5 m-wide end wall in the same language, then ~7 m of
open concrete deck with a rounded corner, railing and bollards. Nothing tall.

**Above.** Pale membrane roof. A **raised monitor spine** runs the length of the shed on the
centreline, ~9 m wide and ~2.7 m proud of the roof deck, and **two long dark solar arrays**
flank it; from `along ≈ 145` outward the arrays widen until they cover nearly the whole roof.
Round vents and rectangular hatches punctuate the field. The bulkhead's own roof is a lower,
plainer flat plane wrapping the head of the shed in an L, with the pavilion breaking through
it at the frontage. The apron reads as a broad pale-grey band all the way round, darker than
the roof, with the railing as a thin line at its edge.

### 2.5 Recognition cues (ranked)

1. **The arched frontispiece** — a low cream wall with one big round arch and `PIER · 1` over
   it, seen from the Embarcadero. Nothing else on this waterfront looks like it.
2. **Length and taper** — a 213 m shed leaning north-east into the Bay, narrowing over its
   outer half. From the aerial camera the pier's *shape* is the identity.
3. **The solar-striped white roof** — two long dark bands on a pale field. The only large
   solar roof in the Ferry Building's neighbourhood.
4. **The two-colour discipline** — cream body, slate-blue steel. No third colour anywhere.
5. **The apron promenade ring** — a pale walkway with railing and globe lamps all the way
   round, which is what makes it read as a *pier* rather than a building on fill.

### 2.6 Miniature translation

The building is already almost a toy: two clean volumes, one ornament, a striped roof. The
work is restraint plus three deliberate exaggerations.

- **Enlarge the arch** to roughly 1.15× its true width and raise the pavilion's step-out to
  ~0.9 m so the frontispiece survives at thumbnail size (style bible §8, §9).
- **Enlarge the `PIER · 1` lettering** to a band that is legible from the aerial camera, and
  extrude it rather than painting it. `PORT OF SAN FRANCISCO` may be simplified to a dark
  bar with an implied lettering rhythm if extruding it costs too much geometry.
- **Enlarge the solar arrays' visual weight** — treat them as two confident dark rectangles
  per roof section, not as individual panels, with a shallow rack step and a panel-grid score
  only where the aerial camera can resolve it.
- **Compress the shed bays.** The real shed has ~28 structural bays per flank. Model a
  repeating unit and use ~20 per flank if that keeps the triangle budget honest — the eye
  reads rhythm, not count. Do not model individual panes; a scored grid inside one recessed
  plane is the whole window.
- **Keep the monitor spine.** It is the difference between a roof and a lid, and it is what
  the DataSF `hgt_max` is measuring.
- **Do not clean it up further than it is.** Pier 1 is a restored building: no rust, no
  stains, no broken edges (style bible §6). But it is also *not* a jewel — resist adding
  planting, canopies, or colour that the real building does not have.

### 2.7 Massing recipe

Local frame: `u` = along (NE, bearing 053.8°), `v` = perp (SE), `w` = up, origin at the
deck-top plane, `u = 0` at the shed's NW corner line, `v = 0` at the shed's NW wall.

1. **Pier deck** — a slab following the deck outline: `u −24.2 … 209`, `v −11 … 43` under the
   shed body, closing in with the taper. Top at w = 0, fascia to w = −1.2, chamfered at the
   deck edge. Rounded corner at the NE tip (8-segment fillet, r ≈ 4 m).
2. **Pile bents** — a coarse grid of square stubs from w = −1.2 to −2.6, on ~9 m centres,
   visible only near the deck edges and under the outer 40 m. Do not model the whole field;
   model the perimeter row plus two internal rows near the tip. This is the only geometry
   below water level and it exists to stop the pier looking like a floating card.
3. **Bulkhead slab** — `u −24.2 … −11.5`, `v −14.2 … 50.6`, w 0 … 8.6 with a 0.35 m coping.
   Plinth from 0 to 1.0 m, slightly proud.
4. **Central pavilion** — centred at `v ≈ 19`, ~22 m wide (post-exaggeration ~24 m),
   projecting ~0.9 m forward of the wing plane, rising to a cornice at 10.0 m and a raked
   pediment apex at 12.8 m, with quoined pilaster strips at its corners.
5. **The great arch** — a round-headed recess in the pavilion, ~10 m wide (exaggerated to
   ~11.5 m), springing 5.5 m, crown 9.3 m, cut ~0.6 m into the pavilion face, with an
   extruded voussoir ring and keystone. Fill with a dark glazed lunette plane, a lettering
   band, and a door screen at the base.
6. **Wing bays** — pilaster strips 0.9 m wide, 0.12 m proud, at ~6.5 m centres; between them
   a recessed panel carrying a band of 3–4 narrow window slots at 5.0 … 7.6 m; ground floor
   glazing/doors at 1.0 … 4.2 m. One flat-arched vehicle portal through the NW wing at
   `v ≈ 2 … 9`, 4.5 m high, cut clean through to the shed head so the light shows.
7. **Shed head** — `u −11.5 … 19`, `v 0 … 41`, w 0 … 9.7.
8. **Shed body** — `u 19 … 97`, `v 0 … 36.2`; **taper** `u 97 … 149` closing to `v 26.5`;
   **outer run** `u 149 … 202`, `v 0 … 26.5`. All w 0 … 9.7 with a 0.3 m coping. Build these
   as one lofted solid so the taper is a real chamfer, not a step.
9. **Shed bays** — pilaster strips 0.6 m wide, 0.1 m proud, at ~7.5 m centres on both flanks
   and on the NE end; belt course at 2.2 m; main window recess 2.4 … 6.0 m; clerestory recess
   8.2 … 9.2 m; plinth 0 … 0.8 m.
10. **Roof** — flat at 9.7 m. Monitor spine centred on the shed's own centreline, 9 m wide,
    top at 12.4 m, with a shallow two-way slope and a scored glazing band on its SE face.
    Two solar fields at 10.1 m on low racks, widening after `u 145`. Six round vents (r 0.6 m,
    10 segments) and four hatches scattered in clear clusters, never uniformly. The bulkhead
    roof is a separate lower plane at 8.6 m.
11. **Apron furniture** — a 0.05 m score line separating apron from deck; guard railing as a
    simple top rail + posts at 3 m centres around the whole perimeter (this is a lot of
    geometry — build one instanced post and one long rail, and drop the balusters); bollards
    at ~12 m centres; eight globe lamp standards along the SE apron only.

### 2.8 Materials and palette

| Surface | Material | Hex | Note |
|---|---|---|---|
| Bulkhead + shed walls, pilasters, coping | `Toy_cream` | `f2ede3` | the body colour of the whole asset |
| Pavilion face, voussoirs, keystone, cornice, lettering | `Toy_white` | `f7f4ec` | the frontispiece reads a half-step brighter |
| Plinth, belt course, deck slab, apron | `Toy_stone` | `d9d2c2` | warm grey concrete |
| Deck fascia, pile stubs | `Toy_ink` | `3a3530` | in shadow under the deck; keeps the pier grounded |
| Window frames, doors, railing, bollards, lamp standards | `Toy_glassl` | `6f95b8` → darkened toward `Toy_navy` `2c4a70` | the real steel is a slate blue-grey; pick one and use it everywhere |
| Glazing (shed + wing windows, clerestory) | `Toy_glass` | `2a4d73` | style bible §5: graphical, opaque, recessed |
| Roof membrane, monitor | `Toy_stone` | `d9d2c2` | slightly lighter than the apron if two tones are affordable |
| Solar arrays | `Toy_navy` | `2c4a70` | two confident dark rectangles |
| Roof vents, hatches | `Toy_steel` | `9aa0a6` | |
| Arch lunette glazing (night) | `Toy_glass_Glow` | see 2.9 | hero glow |
| Ground-floor front glazing (night) | `Toy_glass_Glow` | | supporting glow |
| Shed clerestory band, partial (night) | `Toy_glass_Glow` | | supporting glow |
| `PIER · 1` lettering (night) | `Toy_white_Glow` | | accent only |

Off-palette colours are a WARN, not a fail, but Pier 1 genuinely is a two-colour building —
if a swatch is tempting you toward a third, the building is telling you no.

### 2.9 Night state

Required (`.agents/skills/sf-asset-check/SKILL.md` rule 4; ADDRESS-TO-ASSET stage 2). The
`_Glow` materials' **base colours are the night look** — the app's night layer is an unlit
overlay drawn at the material's own baked colour, so a `_Glow` swatch that looks right only
under a Blender emission boost will read too dark in the app. Author the glow colours as the
colour you want to *see* at night.

- **Hero:** the arched lunette and the door screen behind it — one warm pale glow
  (`f6e3c0`-ish) filling the arch. From the Embarcadero this is the whole identity at night.
- **Supporting:** the ground-floor shopfront band along the Embarcadero facade, at the same
  hue but a step darker; and a *partial* run of the shed clerestory — roughly half the bays
  lit, in a scattered pattern, on both flanks. An office building at night is not uniformly
  on, and a fully-lit 213 m clerestory would out-shout the arch.
- **Accent:** the `PIER · 1` lettering, thin and cool.
- **Not lit:** the roof, the solar arrays, the apron, the deck, the pile stubs, the vents.
  The globe lamps may carry a tiny warm glow if the geometry supports it without a separate
  material.

By day every `_Glow` surface must sit in the same palette family as its non-glow neighbours
so nothing reads as a discoloured patch — this is why the lit glazing is a warm pale rather
than a saturated yellow.

### 2.10 Scope

**In:** pier deck, fascia, perimeter and tip pile stubs, apron, railing, bollards, SE apron
globe lamps, bulkhead building, pavilion and arch, wing bays and the NW vehicle portal, shed
in all three plan segments, shed bays on both flanks and the NE end, roof with monitor spine,
solar arrays, vents and hatches.

**Out:** the Embarcadero roadway, streetcar tracks, promenade paving, palms; Piers 1½, 3, 5;
the Ferry Building; moored vessels including the *Santa Rosa*; the floating docks in either
slip; the water surface; the gangway to Pier 1½; people; vehicles; tenant signage; cameras;
lights; plinths.

**Deliberately omitted, and why:**

- **The flagpole** (~17.9 m). Including it would make `targetHeightM` 20.5 m — a number that
  describes a 0.1 m-thick pole rather than the building — and at the app's camera it is
  sub-pixel. If a later pass wants it, it must come with a re-derived `targetHeightM` and a
  note in `REPORT.md`.
- **The channel-glass conference volume** inside the shed head. It is an interior element;
  nothing of it reads from outside.
- **The mezzanine, the catwalks, the bay-water heat exchanger** — all interior or submerged.

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Pier deck, fascia, apron, tip fillet | 1,200 |
| Pile stubs (perimeter + tip rows) | 1,800 |
| Railing (rail + posts), bollards | 3,000 |
| Globe lamp standards (8) | 800 |
| Bulkhead slab, plinth, coping, wings | 1,500 |
| Pavilion, arch, voussoirs, keystone, pediment, lettering | 3,500 |
| Wing bays, windows, portal | 2,200 |
| Shed solid incl. taper, plinth, coping | 1,400 |
| Shed bays, windows, clerestory (both flanks + end) | 4,800 |
| Roof: monitor spine, solar arrays, vents, hatches | 2,400 |
| Slack | 1,400 |
| **Total cap** | **24,000** |

At 24k this is the heaviest landmark in the set outside the bridges, and it is justified by
226 m of frontage — but it is a *cap*, not a target. The railing is the first thing to cut:
if it costs more than 3,000 triangles, drop the posts to 6 m centres before touching the
frontispiece. The shed bays are the second: fewer, bigger bays beat more, thinner ones.

Streaming: `loadRadius: 3000`. The default rule (`max(2500, 15.4 × 30)`) gives 2500, but the
site is a Case B carve-out — beyond the radius the pier is **empty water**, and a hole in the
Embarcadero next to the Ferry Building is more legible than a hole in a SoMa block. 3000 m
puts the release boundary out past Telegraph Hill and Rincon Hill.

### 2.12 Draft manifest entry

```json
{
  "id": "pier-1",
  "file": "pier-1.glb",
  "anchor": [
    -122.3940638,
    37.7974811
  ],
  "targetHeightM": 15.4,
  "cat": 3,
  "name": "Pier 1",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 3000
}
```

`cat: 3` (Office) is the dominant use after the 2001 conversion — Prologis's headquarters
and the Port's offices. `18` (Government) is defensible on the strength of the carved
`PORT OF SAN FRANCISCO`, and `25` (Transit station) is *not* — Pier 1 has not handled
passengers since the Delta boats. Confirm at integration.

**Do not** rewrite `landmarks_manifest.json` with `JSON.stringify`: it renumbers other
landmarks' `11.0` to `11` across the file. Append the entry as text.

### 2.13 Integration notes (for later, not this task) — **the exclusion is solved here**

Case **B**: `pier1` does not exist in `pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`,
so integration needs a registry entry **and** a tile re-bake.

Registry entry:

```js
{
  id: 'pier1',
  name: 'Pier 1',
  lon: -122.3940736,
  lat: 37.7974474,
  height: 12.8,
  exclude: 25,
  extraExclusions: [{ lon: -122.3948198, lat: 37.7969113, r: 10 }],
  camera: { distance: 700, yaw: 235, pitch: 22 },
}
```

**Why two zones, and why the usual half-diagonal rule must not be used here.**

`excluded()` in `pipeline/buildings.mjs` drops a *whole* footprint when its centroid **or any
ring vertex** falls inside any zone. The bake carries Pier 1 as **two** footprints, and the
second one is a merged polygon:

| Baked footprint | Source | Toy height | Extent `(along, perp)` | What it is |
|---|---|---|---|---|
| `23_9#5` (toy) / `23_9#7` (base) | DataSF 146 | 10.3 m | `−13.3…203.1`, `−5.1…36.9` | Pier 1's shed and the NW part of its bulkhead |
| `23_9#6` (toy) / `23_9#4` (base) | Overture | 14.4 m | `−22.1…24.0`, `−134.9…50.5` | a comb: the ~9 m-deep Embarcadero frontage strip from Pier 1 to Pier 5, **plus Pier 1's bulkhead SE lobe**, **plus a 37 × 34 m tooth over Pier 3's bulkhead** |

The DataSF footprint alone is not enough: the **front 9 m of the bulkhead — the Beaux-Arts
facade itself — is covered only by the Overture polygon**, at 14.4 m, which is 5.8 m taller
than the wings it would bury. Leaving it in place buries the frontispiece. So both must go.

Both must go **without** touching the neighbours. A radius around the anchor large enough to
reach the Overture polygon (71.6 m) is only 7.5 m short of reaching `23_9#14` (Pier 1½ /
Pier 3, 10.7 m) at 79.1 m — a window too tight to defend. The second zone solves it instead:
centred at `(along 2, perp 27)`, in the middle of Pier 1's own bulkhead, it is **1.37 m** from
both target footprints and **35.5 m** from the nearest keeper.

Verified by replaying `excluded()`'s exact test (centroid **or any ring vertex**) against the
committed tiles of **both** tiers, over every footprint within 700 m:

```
buildings tier: drops 2 — 23_9#4 (16.0 m), 23_9#7 (13.7 m)
toy tier:       drops 2 — 23_9#6 (14.4 m), 23_9#5 (10.3 m)
```

Nothing else, in either tier. Re-run that check after the re-bake; do **not** trust
`verify-rebake`'s per-cell counts alone, which can call a working exclusion "dropped nothing".

**Collateral, stated plainly.** Dropping the Overture polygon costs two things that are not
ours:

1. The ~9 m-deep procedural frontage strip along the Embarcadero from Pier 1½ to Pier 5
   (~120 m). The bulk behind it survives as `23_9#14` and `23_9#15`, so the row keeps its
   mass but sits back ~9 m from the street.
2. **Pier 3's bulkhead block** — a 37 × 34 m, 14.4 m footprint about 110 m north-west —
   disappears entirely. `23_9#16` (Pier 5) and `23_9#14`/`#15` (Pier 1½ and inner Pier 3)
   are unaffected.

There is no radius that avoids this: one Overture polygon traces Pier 1's facade and Pier 3's
bulkhead as a single ring, and `excluded()` has no way to clip one. The alternative — leaving
a 14.4 m grey slab standing through the front third of a hand-built landmark — is worse.
**Queue Pier 3 as the next pier landmark**; shipping it restores the block and is the only
real fix.

Other integration steps: re-bake, audit 1.6, the fallback drill, and the local QA table are
all owned by `docs/asset-plans/INTEGRATION-PROMPT.md`. Two additions for this asset:

- Verify at street level from the Embarcadero that the **frontispiece is not buried** — that
  is the whole point of the second exclusion zone, and it is invisible from the aerial camera.
- Verify at the **NE tip** that the deck reads as standing out of the water on piles rather
  than as a slab lying on it: the DEM falls to 0 there while the model stays rigid, so this
  is where the origin decision in 2.3 is actually tested.

`BATCH: yes` sessions must still run the bake and the full QA on it, then
`git checkout -- app/public/tiles api/_data` before committing, and ship source only.

### 2.14 Validation checklist

- Binary GLB, real metres, applied transforms, no negative scales
- **min Z ≈ −2.6 m — expected, stated as a PASS in `validation.json` with the reason**
- XY centre offset ≈ 0 (bounding-box centre, not footprint centroid)
- Vertical extent exactly **15.4 m** so the loader's scale is 1.0
- Axis-aligned XY bbox ≈ 185 × 190 m — expected at a 53.8° heading, not a scale error
- ≤ 24,000 triangles; ≤ 500 KB compressed after `pipeline/compress-assets.mjs`
- No textures, no transparency, no cameras/lights/animation/armatures
- All materials `Toy_*`; `_Glow` only on the four night surfaces in 2.9; no `Toy_body`
- Outward normals: per-object signed volume authoritative for the union of solids; ray test
  ≤ 0.15 % residual, zero for single shells
- Fresh-scene re-import validated, not the source scene
- Day + night renders of the **re-imported** file, glow driven from Base Color
- Contact sheet includes the top view with the taper and both solar fields legible

### 2.15 Open questions and risks

1. **The monitor spine is the least-verified element in the plan.** Its existence and its
   ~2.7 m height come from a shadow measurement on nadir imagery (a ~0.9 m shadow at a ~72°
   solar elevation) corroborated by the 3.1 m gap between DataSF's median (9.66 m) and max
   (12.73 m). No photograph in this dossier shows it directly — every street-level view is
   taken from an apron where the parapet hides the roof. **Find an oblique aerial before
   modelling it**, and if it turns out to be solar racking rather than a monitor, the roof
   loses 2.7 m of relief and the shed's crest drops to ~10 m. That changes nothing about
   `targetHeightM` (the pavilion sets it) but it changes the roof design, which is 40 % of
   what the app's camera sees.
2. **`hgt_maxcm` and `p2010_zmaxn88ft` on this footprint are mutually inconsistent** and both
   are LiDAR statistics computed over water, where the "ground" surface is undefined. The
   12.8 m crest is photogrammetric and self-calibrated on the sidewalk in the same frame; it
   agrees with `hgt_max` to 0.07 m, which is reassuring but could be coincidence. Re-measure.
3. **The pier deck elevation is inferred, not sourced.** ~2.9–3.0 m above water is the
   standard Embarcadero figure and matches the app's own DEM ridge to within 0.6 m, but no
   Port document in the source list states it. The model is tolerant of ±0.5 m here; do not
   spend a day on it, but do not assert it as measured either.
4. **The bay counts are inferred.** Both the wing windows (3–4 per bay) and the shed bay
   spacing (~7.5 m) come from oblique Street View where the far end of every run is
   foreshortened to nothing. Count them from a rectified elevation before committing to a
   repeating unit.
5. **The build date is genuinely contested** (1918 vs 1931). Do not silently pick one for
   `REPORT.md`; state both and what each source is dating.
6. **The exclusion's collateral is real and permanent until Pier 3 ships.** 2.13 spells it
   out. If the reviewer decides losing Pier 3's block is unacceptable, the only other option
   is to ship Pier 1 with its facade buried, and that is not shipping Pier 1.
7. **Length is the budget risk.** 226 m of railing, 28 bays a side and a full pile field will
   blow 24,000 triangles on their own. Decide the repeating units *first*, count them, and
   only then start detailing the pavilion.
8. **This is the first pier in the set and it sets a precedent.** The origin-at-deck-level
   rule in 2.3, the vertical-extent `targetHeightM`, and the two-zone exclusion are all going
   to be copied by Pier 3, Pier 5 and the Embarcadero piers after them. If any of them is
   wrong, say so in `REPORT.md` loudly enough that the next plan does not inherit it.
