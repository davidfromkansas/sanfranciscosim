# Fulton Plaza — SF-SIM asset plan

The pedestrianised block of Fulton Street between Larkin and Hyde: a 120 m × 49 m
right-of-way lying between the Asian Art Museum and the Main Library, closed to traffic
since spring 2020, with the 1894 Pioneer Monument standing dead centre on it and two
20-metre koi painted around the monument on the black asphalt. It is the middle link of
the civic spine that runs UN Plaza → Fulton Plaza → Civic Center Plaza → City Hall.

Like `civic-center-plaza.md`, this plan's subject has **no building**. Unlike it, this one
is not even a block: it is a *street* that stopped being a street. Its recognition comes
from one axis, one monument and one enormous painted graphic — and the graphic is the part
the app's downward-looking camera actually sees.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/fulton-plaza/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `fulton-plaza` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4159189, 37.7796904` (oriented-bounding-box centre, measured from DataSF parcels) |
| Target height | **13.19 m — the model's VERTICAL EXTENT** (this plan first said 10.67 m; corrected during stage 2, see the note at the end of 2.15). The asset is terrain-draped, so `min_z` is negative and `targetHeightM` is the extent, per the `64-south-park` convention. The crest is still the Pioneer Monument: SFAC records it at 420 in = 10.668 m, standing on the plaza's 1.03 m apron |
| Footprint | 119.51 m × 48.59 m oriented (heading 81.15°), 5,805 m² = 1.435 acres, measured from DataSF parcel blocks `0354001` and `0353001` |
| Axis-aligned XY bbox | 128.5 m × 67.6 m as built — the 8.85° rotation of the right-of-way, widened by the planting beds' 2 m overhang and the tree crowns (this plan first said 126.1 × 66.3, the right-of-way alone) |
| Triangle cap | 16,000 |
| Category | `0` (Miscellaneous — the slot Civic Center Plaza, Palace of Fine Arts, Coit Tower and Chase Center use) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Fulton Plaza GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Fulton Plaza**, San Francisco (147 Fulton
Street — the pedestrianised block of Fulton Street between Larkin and Hyde, between the
Asian Art Museum and the Main Library), and deliver it as a downloadable, validated GLB.

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
7. `artifacts/civic-center-plaza/` — the closest reference implementation in *kind* and in
   *place*: the only other hardscape landmark in the set, one block west across Larkin,
   on the same axis and the same 9° grid. Read its `REFERENCE.md` and `REPORT.md` before
   you design anything, and reuse its ground-plate, kerb and paving idiom rather than
   inventing a second one for the same civic spine.
8. `artifacts/sf-main-library/` and `artifacts/asian-art-museum/` — the two buildings that
   form this plaza's south and north walls. They already ship. Your asset must read as the
   floor of the room they enclose, at their palette and their level of abstraction.
9. `docs/asset-plans/fulton-plaza.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Read 2.15 before you start

This plan has two open risks that change what you build (the koi geometry and the tree
height datum) and one deliberate omission that reviewers always ask about (SPECTRA). Read
Part 2 section 2.15 first, not last.

## Must capture

- **The axis.** 119.5 m of open ground running 81.15°/261.15°, aimed at City Hall's dome
  off the west end and at UN Plaza off the east. Everything else is arranged about it.
  If the model reads as a rectangle rather than as a *route*, it has failed.
- **The Pioneer Monument**, dead centre and the model's height datum: a cruciform granite
  base 17.2 m × 12.4 m carrying a central pedestal 7.47 m tall, bronze Minerva with her
  California grizzly on top (3.20 m, crest 10.67 m), and four corner piers facing the
  cardinal directions. **The east pier is EMPTY** — "Early Days" was removed on 14
  September 2018 and never replaced. Model the empty pier; it is the truthful state and
  it is visible from above.
- **The two koi.** Jeremy Novy's 2024 mural: two white-and-orange koi, each about 20 m
  long, painted flat on the black asphalt, nose-to-tail *circling* the monument — one
  ~33 m west of it, one ~27 m east. This is the single strongest recognition cue from the
  app's aerial camera and the only reason this asset is not a grey rectangle. It must
  survive at thumbnail size, which means big confident silhouettes, not scale detail.
- **The pale circular apron** ~21 m across that the monument stands on, in light granite
  against the black asphalt. It is the visual bullseye the koi orbit.
- **The two flanks, which are different and must stay different.**
  *North (museum side):* two raised soil beds, each ~7 m wide and ~52 m long with a gap
  on the centre line, planted with mature broad-crowned London planes, then a pale
  sidewalk running along the museum's base. Ashurbanipal (1988) stands at the west end
  of the east bed.
  *South (library side):* a wide pale terrace with a low kerb wall along its plaza edge
  and a row of younger, smaller street trees. No soil bed.
- **The bollard lines** at Larkin and Hyde. They are why this is a plaza and not a street,
  and they are the only thing at either end.
- **The paving story.** Two thirds of this asset is ground. Black-grey asphalt in the
  middle (the old roadway), pale stone at the edges (sidewalks and terrace), granite at
  the monument. Give the joint between them a kerb you can read from the air.
- **Life.** This is a working public room: the Heart of the City Farmers Market twice a
  week, free concerts Tuesdays and Thursdays, people crossing it all day. Place small
  deliberate clusters — at the monument, at the concert end, at the Hyde crossing — not
  an even sprinkle.

## Research Fulton Plaza independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the WGS84
anchor, the right-of-way polygon, the 10.67 m monument height, the monument's position on
the plaza, and the real-world orientation, and gather references covering:

- **Aerial and satellite imagery, which is the primary reference for this subject** — the
  camera looks down and this asset is almost entirely a ground plane. The koi, the apron
  and the two flanks are all read from above.
- The four edges: what the plaza does at Larkin, at Hyde, at the library terrace and at
  the museum beds — kerb, wall, steps, bed or bollard.
- Ground-level views **along the axis in both directions**: west toward City Hall and east
  toward UN Plaza. These are the two compositions that explain what the place is.
- The koi: their exact position, orientation and scale, which of the two is white and
  which orange, and the fact that they are stencilled with retroreflective glass beads
  and therefore *glow* when light hits them (this drives the night state).
- The current condition. Fulton Plaza has changed repeatedly since 2020 — safe-sleeping
  site, roller rink, carnival, flea market, farmers market — and the flea market left in
  2025. Confirm against recent imagery which elements are still present before modelling
  them.
- Day and night appearance.

Prefer the SF Planning Civic Center Public Realm Plan and cultural-landscape
documentation, SF Recreation & Parks, the SF Arts Commission's Civic Art Collection record
for the Pioneer Monument, Illuminate's project pages, and DataSF (parcels `acdm-wktn`) for
survey geometry. Use the `exa` MCP server (`web_search_advanced_exa`) for photo research
per `docs/asset-pipeline/ADDRESS-TO-ASSET.md` stage 1.

## Create a reference dossier

Write `artifacts/fulton-plaza/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3–5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed reference
thumbnails is welcome if legally permissible — do not commit copyrighted full-resolution
imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22, adapted the way
`civic-center-plaza.md` adapts it: there is no massing to rebuild, so the equivalent moves
are **§12 Landscaping**, **§13 Roads and Ground Plane** and **§17 Composition**.

Two style-bible rules carry unusual weight here:

- **§13, last sentence.** "Break up any large empty asphalt with trees, vehicles,
  markings, medians, planters, activity, small structures." This asset *is* large empty
  asphalt — that is literally the criticism the real place attracts. The koi are the
  city's own answer to it. Do not add invented clutter to compensate; make the koi, the
  apron and the two flanking bands carry the composition.
- **§15 and §16.** A plaza with nobody in it reads as a car park, and this one is
  programmed almost every day. Three or four activity nodes, not a sprinkle.

The finished asset must be immediately recognizable as this plaza, consistent with the
real place from all four sides and above, credible as landscape architecture, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic low-poly,
and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the right-of-way only: the draped ground plate and its kerb, all paving, the koi
inlay, the monument's granite apron, the Pioneer Monument itself, the two north planting
beds with their trees, the south terrace with its low wall and trees, the bollard lines at
both ends, the plaza's own lamp poles, benches, litter bins and planters, the Ashurbanipal
statue, and the people clusters.

Do not include unrelated surrounding city geometry: the Main Library, the Asian Art
Museum, City Hall, United Nations Plaza, Civic Center Plaza, the Larkin or Hyde roadways
and their crossings, the library's forecourt sculptures (the Maya Angelou monument and
Rickey's "Double L Excentric Gyratory" both stand *outside* the right-of-way on library
land), terrain, cameras or lights. Temporary context may appear in review renders but must
not leak into the GLB.

**Do not model SPECTRA** — the 1,271-LED array strung between the two neighbouring roofs.
It is a temporary installation attached to two other assets, and a canopy stretched over
the plaza would hide the koi from the exact camera this asset is judged from. See 2.10 and
2.15 risk 3 for the full reasoning; carry its *effect* through the night state instead.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ≈ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 16,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The plaza's long axis
runs **81.15° / 261.15°** (the Fulton/City Hall axis) and its cross axis **351.15° /
171.15°** (the Civic Center street grid). Build directly in the measured `(u, v)` plaza
frame given in 2.3 and map to world X/Y once, rather than modelling an axis-aligned
rectangle and rotating it.

> **The grid leans 8.85° EAST of north, so the cross-axis southward bearing is 171.15°
> (= 180 − 8.85), not 188.85°.** Those two are mirror images about north and every
> bounding-box measurement reads the same 8.85° for both. `civic-center-plaza` shipped
> the wrong sign once and put a whole plaza 18° out of true against its own block while
> the report still validated — read the warning in that plan's Part 1. Check the sign
> against the neighbours (Main Library 9.06°, Asian Art Museum 9.06°, City Hall 9.62°,
> Civic Center Plaza 9.06°) rather than against a bbox.

**Terrain drape is mandatory, and this site is not flat.** The loader seats a landmark
from a *single* elevation sample at its anchor (`placeGeneric` in `app/src/assets.js`), so
a flat plate over sloping ground buries one end and floats the other. Fulton falls
**2.23 m** across this block, from 18.9 m at Larkin to 16.7 m at Hyde — a ~1.7 % eastward
grade — with about 0.2 m of cross-fall. The measured drape grid is in 2.3; author the
plate with `y = sampleElevation(x, z) − sampleElevation(anchor)` baked into its vertices
and assert the corner deltas in the validator. This is the failure the repo has already
paid for once on ground-plane assets; do not skip it.

**Deck height, and the street that is still baked underneath it.** `exclusionZones()`
clears *buildings*, not streets, and one DataSF centreline still runs the length of this
block (`streets/19_13` line 44, class `residential`). The runtime therefore draws, under
your asset: a 9 m charcoal `#3c3c40` road ribbon on the terrain, 3 m pale sidewalk plinths
lifted **0.35 m** at the kerb, and a 0.5 m white centre dash at +0.03 m. Set the plaza
deck top at **+0.55 m** above the draped terrain — 0.2 m of clearance over the kerb — and
chamfer its perimeter edge. Verify in the app that no charcoal ribbon, pale plinth or
white dash pokes through anywhere along the block; if one does, raise the deck rather than
thinning the margin.

**Height normalization:** the tallest geometry in the export (Minerva's finial) must land
at exactly **10.67 m** above the deck datum so the loader's `targetHeightM /
measuredHeight` scale is 1.0. Drive the monument height from a named constant and assert
it in the validator.

**Flatness caution:** almost every surface in this asset is within 1 m of z=0. Author the
plate, kerbs, beds and apron with real thickness and distinct levels (deck +0.55, apron
+0.57, terrace +0.70, bed top +0.95) so the loader's merge produces no coplanar
z-fighting, and so the levels are legible as a *design* from the air rather than as a flat
wash.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/fulton-plaza/build_fulton_plaza.py` (deterministic build script),
`artifacts/fulton-plaza/fulton-plaza.blend`, and `artifacts/fulton-plaza/fulton-plaza.glb`.
The script must rebuild the model reliably enough for future revision. The right-of-way
polygon, the monument ring, the planting-bed outlines, the tree positions, the koi outlines
and the terrain drape grid are measured data, not invention — commit them alongside the
script under `artifacts/fulton-plaza/data/` with their source (DataSF blklot, OSM element
id, or tile cell) and have the script read them rather than eyeballing. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`fulton-plaza-top.png`, `-north.png`, `-east.png`, `-south.png`, `-west.png`, plus
`fulton-plaza-contact-sheet.png`, at least one high three-quarter aerial beauty render
`fulton-plaza-aerial.png`, and a night render `fulton-plaza-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation.

Three subject-specific requirements:

- **The top view is the primary review image for this asset**, not a supporting one. It
  must clearly show both koi, the monument and its apron, the two north beds and the south
  terrace. Render it larger than the elevations.
- Add `fulton-plaza-axis.png`: a low three-quarter view looking **west along the plaza
  axis** with the monument in the middle distance — the real place's signature
  composition. Frame it as if City Hall were at the end of it, even though City Hall is
  not in this asset.
- The night render must show the koi glowing. That is the whole night state; if it does
  not read, the glow design is wrong.

Because the site is 119.5 m × 48.6 m and only 10.7 m tall, the elevations will be
extremely wide and almost entirely empty above the tree line. Frame them to the plan
dimension and accept the empty sky rather than zooming each view to fit.

## Validate the exported GLB

Re-import `fulton-plaza.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count, camera
count, light count, animation count, applied-transform status, negative-scale status,
normal-orientation status, unexpected geometry, and per-material contract compliance.
Render at least one review image from the re-imported asset. Write
`artifacts/fulton-plaza/validation.json` and `artifacts/fulton-plaza/REPORT.md`.

Four subject-specific validator checks, in addition to the standard ones:

1. **`max_z == 10.67 ± 0.01`** and the vertex achieving it belongs to the Minerva finial,
   not to a tree.
2. **Drape check.** Sample the deck's top surface at the four right-of-way corners and at
   the anchor; the four corner heights relative to the anchor must match the measured
   terrain deltas in 2.3 to within 0.10 m. A flat plate fails this check.
3. **XY bbox ≈ 126.1 × 66.3 m.** That is the expected consequence of the 8.85° heading on
   a 119.5 × 48.6 m rectangle, not a scale error.
4. **Koi present and glowing.** Exactly two koi objects, each 18–22 m along its own long
   axis, each carrying a `*_Glow` material whose base colour matches its day colour.

The normals test needs care on this asset: it is a union of many separate closed solids
(plate, kerbs, apron, bed walls, monument parts, trunks, crowns, bollards), so **per-object
signed volume is the authoritative check**; the whole-model ray test will show a small
residual and ≤ 0.15% is the gate. The koi are the one exception worth planning for — if
they are authored as flat inlay panels rather than solids, give them real thickness
(0.02 m) so they are closed solids like everything else. See 2.15 risk 1.

## Manifest draft

Verify the real WGS84 anchor and height datum yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "fulton-plaza",
  "file": "fulton-plaza.glb",
  "anchor": [
    -122.4159189,
    37.7796904
  ],
  "targetHeightM": 10.67,
  "cat": 0,
  "name": "Fulton Plaza",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": false` — the height datum is the San Francisco Arts Commission's own
catalogue dimension for the monument (420 in overall), not a tag or an inference.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/fulton-plaza.md`.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Source | Confidence |
|---|---|---|---|
| Common name | Fulton Plaza (also Fulton Street Mall, Fulton Street Plaza) | SF Civic Center CBD; SFMTA; Illuminate | verified |
| Postal address | 147 Fulton St, San Francisco, CA 94102 | Illuminate, Time Out, SF Standard, Secret SF | verified |
| Extent | Fulton Street between Larkin and Hyde, one block | SFMTA board item, 16 Jul 2024 | verified |
| Status | Roadway Shared Spaces closure, 24 h daily, 1 Sep 2024 → 31 Aug 2027; closed continuously to traffic since spring 2020 | SFMTA board item + MOU of 17 Jun 2024 | verified |
| Managed by | SF Rec & Park (activation), SF Public Works (maintenance), SFMTA (the closure itself) | MOU, 17 Jun 2024 | verified |
| Right-of-way polygon | 119.51 m × 48.59 m oriented, 5,805 m², heading 81.15° | DataSF parcels `acdm-wktn`, blocks `0354001` / `0353001`, reprojected | **measured** |
| Anchor (OBB centre) | −122.4159189, 37.7796904 | derived from the above | **measured** |
| Terrain | 18.91 m at the Larkin end → 16.68 m at the Hyde end, 2.23 m fall, 17.79 m at the anchor | `app/public/tiles/terrain.bin` via the manifest descriptor | **measured** |
| Pioneer Monument | 1894, Frank Happersberger; bronze on granite and marble; overall with base **420 × 488 × 676 in** = 10.67 m tall on a 12.40 × 17.17 m base; base alone 294 in = 7.47 m | SF Arts Commission Civic Art Collection, accession 1894.4.a-o | verified |
| Monument centre | −122.4159239, 37.7796960 — **0.76 m from the plaza's OBB centre** | area centroid of the baked footprint ring (`buildings/19_13` #101), cross-checked against Esri World Imagery | **measured** |
| Monument moved here | 1993, from its 1894 site in front of City Hall | Wikipedia; SFGate | verified |
| "Early Days" removed | 14 September 2018, into storage; east pier empty since | SFAC record ("removed and placed into storage in 2018"); SFGate | verified |
| Koi mural | Jeremy Novy, painted Feb – spring 2024; two koi, each ~65–70 ft (20–21 m); white and orange; stencilled in 5 ft grid sections with retroreflective glass beads in the sealant | Illuminate; KQED; UnderscoreSF | verified |
| Koi positions | west koi ~33 m west of the monument on the axis; east koi ~27 m east and ~5 m north of it | Esri World Imagery, warm-pixel centroid | **measured**, ±2 m |
| SPECTRA | Joshua Hubert / GlowFidelity; 1,271 individually programmable LEDs strung roof-to-roof between the Main Library and the Asian Art Museum, 1.6 acres, "geometric canopy"/waveform; debut 5 Apr 2025, approved for a two-year run | Illuminate; SF Rec & Park; SF Standard, 1 Apr 2025 | verified |
| Ashurbanipal statue | 1988-05-29, north edge of the plaza | OSM node 6465902729 (`wikidata` Q14660880) | verified |
| Programming | Heart of the City Farmers Market twice weekly since Sep 2023; Civic Center Soundtrack free concerts Tue/Thu 12–3 pm, third season Apr–Oct 2026 | Illuminate; SF Rec & Park; SF Standard | verified |
| Neighbours' heights | Main Library 28.98 m, Asian Art Museum 28.1 m | this repo's shipped manifest entries | verified |

### 2.2 Sources

**Exa searches run (`web_search_advanced_exa`), and what each yielded:**

1. `"Fulton Plaza 147 Fulton Street San Francisco building"` — settled the resolution.
   Yielded sfciviccenter.org (Fulton Plaza = "Fulton Street at Larkin", between museum and
   library), timeout.com and illuminate.org (both give the postal address as 147 Fulton
   St), sfmta.com's July 2024 board packet (the closure, its dates, and the MOU), and
   sfstation.com. Confirmed the address is a *plaza*, not a building.
2. `"Fulton Plaza San Francisco koi mural Jeremy Novy Pioneer Monument aerial photo"` —
   illuminate.org project page (two white and orange koi circling the Pioneer Monument on
   the blacktop), illuminate.org news (each koi ~65–70 ft, painting completed 27 Feb 2024),
   kqed.org (5 ft grid sections, two months, exterior primer + paint + sealant with
   reflective glass beads that glow when lit), underscoresf.com (~70 ft, shadow tracing for
   depth), joshuahubert.com.
3. `"Pioneer Monument San Francisco Frank Happersberger 1894 height Early Days removed
   2018 …"` restricted to Wikipedia/Wikidata/SFAC/SFGate — the SF Arts Commission kiosk
   record is the load-bearing source: 1894, Happersberger, bronze and granite on marble,
   **overall with base 420 × 488 × 676 in**, base alone 294 in, "the *Early Days* component
   was removed and placed into storage in 2018". Wikipedia supplied the four cardinal piers
   (Plenty N, Commerce S, In '49 W, Early Days E) and the Minerva/grizzly crown; SFGate
   supplied the 14 Sep 2018 pre-dawn removal.
4. `"SPECTRA Joshua Hubert Fulton Plaza LED installation …"` — illuminate.org, sfrecpark.org
   and sfstandard.com all agree on 1,271 LEDs, 1.6 acres, roof-to-roof between the library
   and the museum, waveform pattern, debut 5 Apr 2025, two-year approval. The SF Standard
   piece adds the phrase that decided this asset's scope: *"a geometric canopy of light over
   the plaza's stenciled koi fish."*

**Survey and repo data:**

- DataSF parcels `acdm-wktn` — blocks `0354001` (library block; its north line is the
  plaza's south edge) and `0353001` (museum block; its south line is the plaza's north
  edge). These two lines plus the Larkin and Hyde property lines *are* the right-of-way.
- OSM: Fulton Street ways `33789581`, `33789566`, `563926240–3`, `1469907642–5` (all
  retagged `highway=cycleway` since the closure); planting beds `1469745032` and
  `1469745033` (`area=yes`, `highway=pedestrian`, `surface=dirt`); sidewalk centrelines
  `399142439` (south) and `696627437` (north); Ashurbanipal node `6465902729`; the 1996
  "California Native Americans" plaque node `13481001521` on the monument's east pier; a
  London plane `tree_stump` node `13478787173` sourced from SF Planning's Civic Center
  Cultural Landscape Inventory.
- Esri World Imagery (`World_Imagery/MapServer/export`, WGS84 bbox) — the primary visual
  reference. The parcel-derived right-of-way quad overlays exactly onto the visible plaza
  in that imagery, which is what validates both.
- This repo's committed bake: `app/public/tiles/terrain.bin` (drape), `buildings/19_13.bin`
  (the monument's traced footprint, and the exclusion measurements in 2.13),
  `streets/19_13.bin` (the surviving street centreline), `landcover/19_13.bin` and
  `toyland/19_13.bin` (the tree-scatter count).

**Rejected sources.** Wikidata Q14683658 carries two coordinates for the Pioneer Monument,
`-122.4181304, 37.779701` and a low-precision `-122.415, 37.778889`. The first is the
monument's **pre-1993** site in Civic Center Plaza, 180 m west of where it stands. Do not
use it. Nominatim's hit for "147 Fulton Street" resolves to OSM way `33789581`, which is a
*cycleway segment*, not a footprint — the same "geocoder returns `osm_type: way`, so it
must be a building" trap that 350 Brannan and 10 South Park document in the plans README.

### 2.3 Orientation and placement

The plaza is the gap between two block faces, so its polygon is surveyed rather than
traced. The four corners, from DataSF:

| Corner | lon | lat | local x | local z |
|---|---|---|---|---|
| SW — Larkin × library line | −122.4165461 | 37.7793902 | 1843.85 | −1037.99 |
| SE — Hyde × library line | −122.4152008 | 37.7795570 | 1962.24 | −1056.43 |
| NE — Hyde × museum line | −122.4152951 | 37.7799901 | 1953.94 | −1104.31 |
| NW — Larkin × museum line | −122.4166336 | 37.7798241 | 1836.15 | −1085.96 |

South edge 119.81 m, north edge 119.20 m, both ends 48.58 m; area 5,805 m²; centroid
`-122.4159189, 37.7796904` → local `x 1899.045, z −1071.171`, in tile cell **19_13**.

**The plaza frame.** Define `u` along the long axis (positive toward Hyde, i.e. east) and
`v` across it (positive toward the library, i.e. south):

```
u_hat = ( +0.98805, −0.15391 )      # bearing 81.15°
v_hat = ( +0.15391, +0.98805 )      # bearing 171.15°
world = anchor + u·u_hat + v·v_hat   # (x, z) metres
```

Corners in this frame are `(±59.6..60.2, ±24.29)`. Everything below is quoted in it.

| Feature | u | v | Source |
|---|---|---|---|
| **Pioneer Monument** (ring centroid) | **−0.34** | **−0.68** | baked footprint ring |
| Pioneer plaque, east pier | +7.87 | −1.42 | OSM node |
| West koi centre | −33.09 | −0.86 | imagery |
| East koi centre | +27.29 | −5.44 | imagery |
| Ashurbanipal | −2.28 | −23.14 | OSM node |
| North bed, west: corners | −62.0 / −8.2 | −19.2 … −26.3 | OSM way 1469745033 |
| North bed, east: corners | +3.4 / +55.2 | −19.2 … −26.5 | OSM way 1469745032 |
| North sidewalk centreline | −65 … +59 | ≈ −18.0 | OSM way 696627437 |
| South sidewalk centreline | −65 … +59 | ≈ +17.8 | OSM way 399142439 |
| Old carriageway lane centrelines | full length | +5.72 and −8.50 | OSM Fulton ways |
| Plaza lamps (two mapped) | −10.2, +6.2 | +23.2 | OSM nodes |

Two things fall out of that table and both are design instructions:

1. **The monument is the plaza's geometric centre**, to 0.76 m. The 1993 relocation put it
   exactly on the crossing of the two axes. Build the model symmetric about it.
2. **The two flanks are not symmetric.** The north beds run from `v = −19.2` to `v = −26.3`
   — that is, they start 5 m inside the property line and *overhang it by up to 2.0 m*.
   That overhang is real (the beds are cut into the museum's forecourt) and it is harmless:
   the Asian Art Museum GLB's own wall is ~7 m further north still. Model the beds at their
   measured outline; do not clip them to the parcel line and do not move the parcel line.
   The south side has no bed at all — just terrace, kerb wall and a thinner row of trees.

**Heading.** Long axis 81.15°, cross axis 351.15°. The Civic Center grid leans 8.85° east
of north here, which agrees with every neighbour already in the repo (Main Library and
Asian Art Museum both 9.06°, City Hall 9.62°, Civic Center Plaza 9.06°). Read the signed
-angle warning in Part 1 before touching this.

**Terrain drape.** Sampled from `app/public/tiles/terrain.bin` at 10 m along the axis and
8 m across it, in metres above sea level (anchor = 17.788 m):

```
      u=-60   -50   -40   -30   -20   -10     0   +10   +20   +30   +40   +50   +60
v=-24 18.55 18.44 18.33 18.17 18.01 17.83 17.72 17.54 17.29 17.07 16.93 16.77 16.68
v=-16 18.62 18.47 18.26 18.09 17.91 17.77 17.64 17.51 17.30 17.10 16.91 16.79 16.75
v= -8 18.61 18.47 18.31 18.12 17.99 17.85 17.70 17.54 17.33 17.14 16.99 16.85 16.80
v=  0 18.69 18.46 18.33 18.14 17.99 17.90 17.79 17.61 17.38 17.23 17.06 16.85 16.80
v= +8 18.68 18.53 18.38 18.28 18.11 17.94 17.88 17.78 17.53 17.34 17.07 16.86 16.74
v=+16 18.73 18.69 18.61 18.49 18.33 18.23 18.17 18.05 17.82 17.54 17.21 16.92 16.69
v=+24 18.91 18.89 18.85 18.74 18.56 18.50 18.48 18.35 18.09 17.72 17.32 16.99 16.72
```

Relative to the anchor that is **+0.90 m at the Larkin end and −1.11 m at the Hyde end** —
a 2.0 m difference over the model's own length, and about 0.2 m of cross-fall. Commit this
grid to `artifacts/fulton-plaza/data/` and drape against it.

### 2.4 What each side shows

- **From above** — the review image that matters. Black asphalt field; a pale circular
  apron dead centre with the cruciform monument on it; two enormous pale-and-orange koi
  orbiting it, one west and one east, lying roughly across the axis; a dark green band of
  mature tree crowns down the north edge sitting in raised soil; a pale terrace with a
  thinner, lighter tree row down the south edge; bollards ruling both ends.
- **West (Larkin) end** — the plaza's grand end, aimed at Civic Center Plaza and City
  Hall's dome. Bollards, crosswalk, and the beginning of the north bed. This is the
  approach a visitor arriving from City Hall sees.
- **East (Hyde) end** — 2.0 m lower, opening onto UN Plaza and Market Street. The
  neighbourhood end: farmers-market vans stage here, the pavement is coarser.
- **South (library) elevation** — a long low pale wall and terrace, punctuated by the
  library's Fulton entrance. Younger trees, thinner canopy, more paving. Reads bright.
- **North (museum) elevation** — the opposite: two long raised soil beds, mature planes,
  deep shade, Ashurbanipal standing in it. Reads dark and green.

That north/south contrast is the second-strongest recognition cue after the koi, and it is
free — it costs one extra material and one bed profile. Do not average the two sides.

### 2.5 Recognition cues (ranked)

1. **The two koi**, 20 m each, on black asphalt, circling the monument. Nothing else in San
   Francisco looks like this from the air.
2. **The Pioneer Monument on its pale round apron**, dead centre, with one empty pier.
3. **The axis** — a 120 m open route between two civic buildings, bollarded at both ends.
4. **The asymmetric flanks** — dark planted bed north, pale terrace south.
5. **The grade** — the plaza visibly runs downhill to the east.

### 2.6 Miniature translation

- The koi become two flat inlay solids, 0.02 m proud of the deck, in two flat colours plus
  a darker outline — *not* a texture, *not* a decal, and not detailed with scales. At
  1:1000 on the aerial camera they are two pale commas around a dot; that is the target.
- The monument becomes four chunky beveled elements: cruciform granite base, tall pedestal,
  four corner piers (three with a simplified bronze figure, one bare), and a single stubby
  bronze figure on top. Minerva reads as a silhouette, not as anatomy.
- The trees follow the flora idiom already used by `civic-center-plaza`: London planes with
  knuckled trunks and wide flat crowns. North beds get full crowns; the south row gets
  smaller, rounder ones.
- Paving is *designed*, not blank: a coarse joint grid on the asphalt field, a finer one on
  the pale terrace, radial joints in the granite apron.
- The bollards are a rhythm, not a fence — chunky, widely spaced, one accent colour.

### 2.7 Massing recipe

Working in the `(u, v)` frame, `y` measured from the draped deck datum:

1. **Deck plate** — the full right-of-way quad, draped, top at **+0.55 m**, chamfered
   perimeter edge, asphalt material. This is the single largest object and the thing that
   hides the baked street.
2. **South terrace** — a band from `v = +14` to `v = +24.29`, top at **+0.70 m**, pale
   stone, with a 0.35 m low wall along its `v = +14` edge.
3. **North beds** — two boxes at the measured outlines, top at **+0.95 m**, soil material,
   0.25 m stone kerb.
4. **North sidewalk** — a pale band from `v = −20` to `v = −24.29` between and outboard of
   the beds, top at **+0.70 m**.
5. **Granite apron** — a 21 m disc centred at `(−0.34, −0.68)`, top at **+0.57 m**.
6. **Pioneer Monument** at the same centre: cruciform base footprint 17.2 × 12.4 m (use the
   committed ring), pedestal to 7.47 m, Minerva to **10.67 m**, four piers at the cardinal
   points with the **east one empty**.
7. **Koi** — two inlay solids at `(−33.1, −0.9)` and `(+27.3, −5.4)`, each ~20 m long, long
   axis roughly across the plaza, oriented head-to-tail so they read as circling.
8. **Trees** — north beds ~9 mature planes, crowns to **10.0 m**; south terrace ~7 smaller
   ones, crowns to ~7 m.
9. **Bollards** — two lines across `v` at `u ≈ ±59`, ~1.0 m tall.
10. **Furniture and life** — plaza lamps at the two mapped positions and a matching rhythm,
    benches and bins along the terrace, Ashurbanipal at `(−2.3, −23.1)`, and three clusters
    of people: at the monument, on the terrace near the library entrance, and at the Hyde
    end where the market stages.

### 2.8 Materials and palette

Draw every colour from the project palette; do not introduce new hues.

| Element | Material | Note |
|---|---|---|
| Asphalt field | `Toy_asphalt` | the darkest large surface in the asset |
| Terrace, north sidewalk | `Toy_stone` | pale, carries the plaza's brightness |
| Kerbs, low wall, bed walls | `Toy_kerb` | one step darker than the stone |
| Monument base, pedestal, piers | `Toy_granite` | warm grey, not white |
| Minerva and the three bronzes | `Toy_bronze` | the only metal in the asset |
| Koi body | `Toy_koiWhite` + `Toy_koiWhite_Glow` | see below |
| Koi markings | `Toy_koiOrange` + `Toy_koiOrange_Glow` | the asset's one saturated accent |
| Soil | `Toy_soil` | north beds only |
| Tree crowns / trunks | `Toy_foliage` / `Toy_bark` | shared with `civic-center-plaza` |
| Bollards | `Toy_accent` | the plaza's colour signature at both ends |
| Lamp heads | `Toy_lamp_Glow` | supporting glow only |

**Night state.** The hero glow is the **koi**, and it is not a licence — the real mural is
sealed with retroreflective glass beads specifically so that it lights up (KQED). Give both
koi `_Glow` materials whose **base colours equal their day colours** — a `_Glow` material's
base colour *is* its night look, and a night render that raises emission strength will
flatter a colour that is in fact too dark. Supporting glow: the lamp heads and a low wash
on the monument's pedestal face. Nothing else. Two glowing fish on a black plaza with a lit
monument between them is the whole composition, and it is a good one.

### 2.9 Top surface

The entire asset is a top surface. Everything in 2.7 is a roof. There is no "roof design"
section for this plan because there is no other kind.

### 2.10 Scope

**In:** the right-of-way quad and everything standing on it — deck, kerbs, terrace, beds,
sidewalks, apron, monument, koi, trees, bollards, lamps, benches, bins, planters,
Ashurbanipal, people.

**Out, and why:**

- The Main Library and the Asian Art Museum — they ship as their own landmarks.
- The library's forecourt sculptures. The Maya Angelou monument (`−122.416468, 37.779140`)
  and Rickey's "Double L Excentric Gyratory" (`−122.416520, 37.779355`) are both well south
  of the plaza's south edge, on library land. They belong to `sf-main-library`, not here.
- Larkin and Hyde, their crossings and their traffic. The bollard line is the boundary.
- **SPECTRA.** Three reasons, in order of weight. (1) The app's camera looks *down*; a
  canopy stretched across the plaza at ~28 m would occlude the koi and the monument from
  the only view this asset is judged from, destroying the composition it exists to deliver.
  (2) It is physically strung from the roofs of two *other* assets, so anything holding it
  up inside this footprint is a fiction. (3) It is temporary — approved for two years from
  April 2025 — and baking it in dates the asset. If SPECTRA becomes permanent it belongs on
  `sf-main-library` and `asian-art-museum`, whose roofs actually carry it. Its effect is
  already in the night state: this is a plaza that is brightly lit from above, which is why
  the koi glow.
- The Heart of the City Farmers Market and the concert stage. Both are twice-weekly
  temporary set-ups; a permanent asset should not freeze one. Their *traces* — the staging
  space kept clear at the Hyde end, the people clusters — do belong.

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Deck plate, draped, with chamfer | 1,600 |
| Terrace, sidewalks, kerbs, low wall | 1,400 |
| North beds and their walls | 500 |
| Granite apron | 300 |
| Pioneer Monument (base, pedestal, 4 piers, 3 bronzes, Minerva) | 3,200 |
| Two koi | 900 |
| 16 trees | 4,800 |
| Bollards (≈ 20) | 480 |
| Lamps, benches, bins, planters | 1,300 |
| Ashurbanipal | 250 |
| People clusters | 900 |
| **Total** | **15,630** |

Cap 16,000 — comfortably inside the 30k landmark budget, and it should stay there: this is
a ground plane, and the temptation to spend the headroom on clutter is exactly what 2.6
warns against. Expect stage 4 to take the shipped file well under 500 KB.

### 2.12 Draft manifest entry

```json
{
  "id": "fulton-plaza",
  "file": "fulton-plaza.glb",
  "anchor": [-122.4159189, 37.7796904],
  "targetHeightM": 10.67,
  "cat": 0,
  "name": "Fulton Plaza",
  "estimated": false,
  "dims": [126.1, 66.3, 10.67],
  "tris": 15630,
  "loadRadius": 2500
}
```

`loadRadius` follows the default rule — `max(2500, 10.67 × 30)` = 2500. This is not an
`alwaysLoaded` skyline piece and must not become one.

Append the entry as **text**, not by re-serialising the JSON: `JSON.stringify` rewrites
`11.0` to `11` across unrelated entries and produces a diff that touches half the file.

### 2.13 Integration notes (for later, not this task)

**Case B — new landmark.** No `fulton-plaza` id exists in `app/src/landmarks.js` or
`pipeline/lib/landmarks.mjs`, so integration needs a registry entry and a tile re-bake in
addition to the manifest entry. Registry draft (camelCase id, as the file requires):

```js
{
  id: 'fultonPlaza',
  name: 'Fulton Plaza',
  lon: -122.4159189,
  lat: 37.7796904,
  height: 10.67,
  exclude: 25,
  camera: { distance: 340, yaw: 99, pitch: 26 },
}
```

**The exclusion has exactly one job, and it is measured.** Counted over the 1,772 baked
footprints in cells 18–20 × 12–14 of the committed bake, with the metric `excluded()`
actually uses (ring centroid **or** any vertex inside the radius, measured from the anchor):

```
  1.85 m   buildings/19_13 #101 — 17-vertex cruciform, 16.90 x 11.36 m, 47.2 m2,
           baked base 17.3 m -> top 21.9 m (a 4.6 m block).  <- must go
 86.19 m   nearest surviving neighbour vertex (20_13 #8, 61.9 m tall)  <- must survive
```

Footprint #101 **is the Pioneer Monument**: DataSF traces it as a building, and the bake
extrudes it into a 4.6 m cruciform block standing exactly where the hand-modelled monument
goes. Its own dimensions (16.90 × 11.36 m) corroborate the Arts Commission's catalogue
figure (17.17 × 12.40 m) to within a metre, which is a pleasant way to discover that both
numbers are right.

```
  r <= 1.0   drops 0        r = 25   drops 1     <- proposed
  r = 15     drops 1        r = 40   drops 1
```

Anything from ~1 m to ~86 m drops that one footprint and nothing else, so the window is
enormous. **25 m** is chosen rather than the minimum because it covers the plaza's full
half-width (24.29 m), so any future data vintage that traces a kiosk or a market stall
inside the roadway band is cleared too — while stopping far short of the nearest survivor.
Do not go higher on the theory that "bigger is safer": the reason the window looks so
generous is that the Main Library and the Asian Art Museum are *already* cleared by their
own 40 m exclusions, and a radius that relies on someone else's exclusion is a trap for
whoever edits those next.

**No `clearTrees`, and that is measured too.** The landcover scatter drops **zero** trees
inside the plaza quad and zero within 80 m of the anchor, in both `landcover/19_13.bin`
(11 trees in the whole cell) and `toyland/19_13.bin` (41). Fulton Plaza is tagged as a
street, not `leisure=park`, so the scatter never reaches it — unlike `civicCenterPlaza`
and `64SouthPark`, both of which needed the flag. Do not add it speculatively.

**The street underneath is the real integration hazard.** `exclusionZones()` is consumed by
`pipeline/buildings.mjs`, `pipeline/audit.mjs` and `pipeline/verify-rebake.mjs` — **not** by
`pipeline/streets.mjs`. One DataSF centreline survives the closure and still bakes:
`streets/19_13.bin` line 44, class index 4 = `residential`, 16 points of which 12 lie
inside the plaza quad. In toy mode that renders a 9 m `#3c3c40` ribbon on the terrain, 3 m
pale sidewalk plinths at kerb height `TOY_CURB_H = 0.35 m`, and a 0.5 m centre dash at
`TOY_MARK_LIFT = 0.03 m`. The asset's +0.55 m deck is what hides all of it. Verify this in
the app at stage 5, from a low camera at both ends as well as from above — the failure
shows up as a charcoal stripe or a white dash bleeding through the deck, and it will be
worst wherever the drape and the baked terrain disagree.

**Re-bake expectations.** A Case B bake rewrites ~600 generated files under
`app/public/tiles/` and `api/_data/` whatever the landmark was; only a fraction of that
churn is yours. `verify-rebake.mjs` compares per-cell counts and will report cell 19_13
losing one footprint — that one *is* this entry. If it reports anything else moving,
attribute it before believing it: a fresh bake settles every pending source-only
neighbour's exclusion at once, and attribution by cell cannot tell them apart.

**Batch mode.** This landmark is being built alongside others, so stage 5 runs the bake,
does the full QA on it, then throws it away (`git checkout -- app/public/tiles api/_data`)
and commits source only. `git diff --name-only origin/main` must list nothing under
`app/public/tiles/` or `api/_data/`.

**Camera preset.** `yaw: 99` — the app's `apply()` offsets by `(sin yaw, ·, cos yaw)` with
`+z` south, so camera bearing = 180 − yaw = 81°, which stands the camera at the Hyde end
**on the plaza's own axis** looking west past the monument toward City Hall. That is the
composition that explains the place, and it is the same reasoning `civicCenterPlaza` used
for its `yaw: 90`. Verify it by render rather than trusting the arithmetic.

### 2.14 Validation checklist

- `max_z = 10.67 ± 0.01`, achieved by the Minerva finial.
- Deck top follows the 2.3 drape grid: corner heights relative to the anchor within 0.10 m
  of `+0.90` (Larkin) and `−1.11` (Hyde).
- XY bbox ≈ 126.1 × 66.3 m; oriented footprint 119.5 × 48.6 m at heading 81.15° (**signed**).
- Origin at base centre, min Z ≈ 0, XY centre offset ≈ 0.
- Two koi objects, 18–22 m each, both carrying `_Glow` materials whose base colour equals
  their day colour.
- Monument: four piers present, **east pier carries no figure**.
- Materials all `Toy_*`; `_Glow` only on koi, lamp heads and the monument wash; no textures,
  no transparency, no `Toy_body`.
- Per-object signed-volume normals check authoritative; whole-model ray residual ≤ 0.15%.
- Triangles ≤ 16,000; no cameras, lights, animation, armatures; transforms applied.
- Fresh-scene re-import validated, not the source scene.

### 2.15 Open questions and risks

1. **The koi are the asset and they are the least-measured thing in it.** Their published
   length (65–70 ft) and their approximate positions are solid; their exact outlines,
   orientations and which fish is which colour come from one aerial image at 0.11 m/px, and
   the mural has been on the ground since 2024 and wears. The modeller must pull better
   imagery before committing the silhouettes. If they end up wrong, the whole asset is
   wrong — no other element carries this much of the recognition. Budget the research time
   there rather than on the monument, which is fully catalogued.
2. **The tree height datum is a design decision, not a measurement.** The north beds carry
   mature London planes; nobody has measured them. This plan sets their crowns at 10.0 m so
   that the Pioneer Monument (10.67 m) stays the tallest thing on its own plaza, which is
   both compositionally right and how the height datum is defined. If the modeller measures
   a plane crest above 10.67 m, that is a real conflict: the honest resolution is to keep
   the monument as `targetHeightM` and record the trees as deliberately restrained in
   `REPORT.md`, not to silently raise the datum.
3. **SPECTRA is deliberately absent, and reviewers will ask.** The reasoning is in 2.10.
   The short version: it would hide the koi from the camera that matters, it hangs from two
   other assets, and it is temporary. It is currently the most photographed thing about the
   plaza, so expect to defend this at gate 3 — and if the answer comes back "put it in",
   the right place is the two neighbouring roofs, not this footprint.
4. **The monument's position is measured two ways that disagree by 3.5 m across the
   plaza.** The DataSF/Overture footprint ring puts its centroid at `(u −0.34, v −0.68)`;
   the Esri imagery centroid of its pale apron puts it at `(u +0.17, v −4.22)`. The survey
   ring is the better source and this plan uses it, but the imagery is what the eye checks
   against, so re-verify before placing. Along the axis the two agree to 0.5 m, which is
   the direction that matters for symmetry.
5. **"Estimated" applies to more of the flanks than to the centre.** The north beds are
   traced from OSM, the sidewalk lines from OSM centrelines, and the tree counts and
   positions in 2.7 are eyeballed from aerial imagery. Only the right-of-way, the anchor,
   the terrain drape, the monument's footprint and the monument's height are survey-grade.
   Label the rest *estimated* in `REFERENCE.md` and do not let the report imply otherwise.
6. **Corrected at stage 2 — the height datum.** This plan's Part 1 asked for
   `max_z == 10.67 m` and a manifest `targetHeightM` of 10.67. That is incompatible with the
   terrain drape the same Part 1 mandates: once z = 0 means the anchor's ground, the export
   spans −1.50 to +11.70 m and the loader's `targetHeightM / bbox height` scale must be
   computed against the 13.20 m extent. The shipped values are in
   `artifacts/fulton-plaza/REPORT.md`, which beats this plan. The monument is still 10.668 m
   of monument and still the model's crest.

7. **Corrected at stage 5 — the deck height.** Part 1 sets the deck at +0.55 m "0.20 m of
   clearance over the kerb", and that is not enough. The baked ribbon's `y` quantises up to
   0.20 m above the terrain, and `createGroundMaterial()` runs the whole ground mesh with
   `polygonOffset{Factor,Units} = -2`; the measured clearance was 0.06–0.15 m, the offset
   won, and two pale sidewalk plinths drew straight over the deck, both koi and the
   monument's apron in the running app. The deck ships at **+0.95 m**. The lesson generalises
   to any future ground-plane landmark over a surviving street: size the deck against the
   ribbon's *quantised* height plus a depth-bias margin, and confirm it in the app — no
   Blender render and no contract check can see this failure.

8. **Corrected after stage 5 — the Pioneer Monument's form.** This plan's 2.7 gave the
   monument as "cruciform base, pedestal to 7.47 m, Minerva to 10.67 m, four piers at the
   cardinal points", which is true and not enough: built from that, it came out a square
   ziggurat with four totems on it. The monument is a **circular** composition — a name drum
   with medallion busts, a panelled pedestal drum, a flaring cornice, a bronze collar, and
   Eureka with her oval shield, her grizzly and her raked spear (the spear tip is the crest).
   The four piers are **low** (1.55 m) and *Plenty* and *Commerce* are **seated**. Model it
   from the 2017 Commons photographs of the object, not from a description of it; the radii
   come off the elevation as a fraction of the monument's own height, and the first attempt
   had every one ~35% over. See `artifacts/fulton-plaza/REFERENCE.md`, "The Pioneer
   Monument".

9. **The plaza may stop being a plaza.** The SFMTA closure runs to 31 August 2027 and is a
   renewable permit, not a permanent change; the street is still a street in DataSF, which
   is exactly why a ribbon still bakes under it. If the closure lapses, this asset becomes
   historical rather than wrong — but the bollards would be the first thing to remove.
