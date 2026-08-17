# 95 Jack London Alley (Gran Oriente Filipino Masonic Temple) — SF-SIM asset plan

A 1951 two-storey stucco lodge hall on a back alley off South Park, built by the
Gran Oriente Filipino — the first Filipino-founded Masonic order in the United
States — behind the tenement they already owned at 45–49 South Park. It is the
**third and last** building of the Gran Oriente complex to enter this manifest,
after the hotel at 104–106 South Park; the residence at 45–49 is still procedural.

It is a plain box with one extraordinary face. The designation report describes it
in a single sentence — *"a simple, two-story rectangular building that lacks
ornament, except for the main entrance and cornice"* — and that is exactly the
design problem: 8.6 m of blush-pink stucco carrying a Moorish ogee arch, two white
columns capped with globes, a gold square-and-compass on the transom, and two
courses of incised text, one of which reads DEDICATED TO THE SUPREME ARCHITECT OF
THE UNIVERSE. Everything else about the building is a flat parapeted slab.

It still meets. Rizal Lodge No. 12, the last Gran Oriente lodge in California,
assembles here.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/95-jack-london-alley/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `95-jack-london-alley` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor (manifest **and** registry) | `-122.3934430, 37.7813460` — one point serves both, see 2.13 |
| Target height | **8.40 m** to the facade parapet crest; roof deck 7.84 m (measured, LiDAR) — `estimated: true`, see 2.1 and 2.15 risk 1 |
| Footprint | 8.6 m frontage × 13.7 m deep, ~118 m² — **not** the 20.35 m depth OSM traces, see 2.3 |
| Axis | long axis 45.9° / 225.9°; alley facade faces **225.9°** (south-west, onto Jack London Alley) |
| Triangle cap | 6,000 |
| Category | `8` (worship — `temple` / `meeting_house`) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 95 Jack London Alley (Gran Oriente Filipino Masonic Temple) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Gran Oriente Filipino Masonic Temple at
95 Jack London Alley, San Francisco, and deliver it as a downloadable, validated
GLB.

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
7. `artifacts/106-south-park/` — the sibling building, 85 m away across the same
   block, owned by the same organisation, planned from the same designation
   report. Take its restraint and its party-wall discipline. Note the
   differences: that one is a three-storey rooming house whose facade is now a
   plain grid; **this one is a two-storey hall whose entire interest is a single
   2.8 m wide doorway**, and the detail budget has to go there
8. `artifacts/135-south-park/` — the nearest reference for a small masonry box
   whose identity is one designed top edge, and for the palette-name-with-adjusted-hex
   convention this plan relies on (see its REPORT round on `Toy_rust`)
9. `docs/asset-plans/95-jack-london-alley.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Three source problems are already resolved — re-check them, do not silently re-inherit the wrong value

1. **OSM `way/71211338` over-traces this building by about 6.6 m at the rear.**
   Its trace is a clean 20.35 × 9.37 m rectangle and it is wrong: DataSF's
   LiDAR-derived footprint stops at 13.7 m, the strip beyond it is assigned to the
   neighbouring building at 41–43 South Park, and Bing z20 aerial imagery shows a
   **tree canopy in a yard** where OSM's rear third is. Build on the DataSF
   footprint — **8.6 × 13.7 m** — not the OSM one. This changes the anchor by
   2.6 m as well as the depth. See 2.3.
2. **There is no published height for this building.** The designation report
   describes it, but gives no dimension; the assessor's roll records the whole lot
   (3775/039) as the 1909 apartment building in front of it. The 7.84 m roof deck
   is a real LiDAR measurement; the 8.40 m parapet crest on top of it is a
   photogrammetric estimate from a single square-on photograph. Ship it as
   `"estimated": true` and say so. See 2.1 and 2.15 risk 1.
3. **This is a Masonic lodge, not a church.** OSM tags it `amenity=place_of_worship`
   `religion=christian`, and an OSM note (3830661) has been arguing about that tag
   since 2023. Category `8` is still right — `temple` and `meeting_house` both map
   to it, and it buys the punched-masonry facade treatment this building needs —
   but nothing in the card copy, lore or model should read as a church. No cross,
   no steeple, no nave.

## Must capture

- **The blank box and the one loaded face.** 8.6 × 13.7 m, two storeys, flat
  roof, parapet all round. Three of the four elevations are bare stucco. The
  fourth is the whole reason the building is in the manifest.
- **The Moorish ogee entrance.** A pointed, slightly ogee arch recessed into the
  facade, with a **trilobed (three-lobe) arch** springing inside it over the
  doorway, and three round-arched transom windows above the door separated by
  engaged colonettes. This is the single strongest recognition cue and it is
  worth more triangles than the rest of the building combined.
- **The two free-standing white columns with globe caps.** They stand proud of the
  door plane, flanking the opening — Jachin and Boaz, and the spheres on top are
  the terrestrial and celestial globes. At the app's scale they are two bright
  dots either side of a dark arch, which is exactly the silhouette that makes this
  building legible from the aerial camera.
- **The gold square-and-compass with the letter G** painted on the centre transom.
  It is the night hero (see the night state below).
- **Two courses of incised text**, at the parapet (DEDICATED TO THE SUPREME
  ARCHITECT OF THE UNIVERSE) and above the entrance (GRAN ORIENTE FILIPINO
  MASONIC TEMPLE). Carry both as shallow inset bands of a slightly darker value.
  **Do not model glyphs** — they are far below a pixel in the app.
- **The blush-pink stucco.** This building is pink, in a block of gray, white and
  olive. Under the style bible's SF exception for tinted facades this colour is the
  building's second-strongest cue and must survive the miniature translation.
- **A designed roof.** The camera looks down. Charcoal membrane deck at 7.84 m
  inside a light coping ring, the facade parapet stepping up 0.25 m above the side
  parapets at the alley end, a stair/hatch bulkhead and two small vent boxes.
- **The exposed north-west flank.** The designation report records stucco cladding
  on "the façade and north elevation", and photography confirms the long north-west
  elevation stands free with a dentilled parapet band along its top. It is not a
  party wall. Build it as a finished elevation.

## Research 95 Jack London Alley independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint (see problem 1 above), the WGS84 anchor, and
the real-world orientation, and gather references covering:

- **The height.** This is the weakest number in the plan and the one most worth
  your research time. Look for the 1951 building permit in DataSF, a measured
  drawing in the Page & Turnbull 2009 primary record, or any photograph with a
  known-scale object in frame. If you find a published figure, use it and say so
  in `REPORT.md`; the plan's 8.40 m is a derived value, not a source.
- **The facade composition.** One square-on photograph exists (2016, in the
  designation report). It suggests the two small ground-floor windows are **not**
  symmetric about the entrance — the north-west one sits closer to the door than
  the south-east one — but that reading is perspective-sensitive and unconfirmed.
  Settle it. See 2.15 risk 3.
- **The paint.** Both photographs in this dossier are 2016 and one is fully
  shaded. Confirm the building is still pink and get a better hue.
- **The south-east elevation and the rear (north-east) elevation**, which no
  photograph in this dossier shows.
- **The roof from above** — bulkhead, vents, skylights, any PV.
- Day and night appearance.

Prefer DataSF datasets, SF Planning records, the landmark designation report,
assessor data, geolocated photography and aerial imagery. Never rely on a single
photograph, a single AI-generated image, or a single unsourced 3D model. Separate
verified facts from visual inference; if sources disagree, document the
disagreement and decide.

## Create a reference dossier

Write `artifacts/95-jack-london-alley/REFERENCE.md` containing: source links and
what each establishes; verified dimensions and location; orientation; observations
from all four sides and above; the 3–5 strongest recognition cues; features to
preserve; features to simplify; uncertainties and conflicting evidence. A contact
sheet of attributed reference thumbnails is welcome if legally permissible — do
not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **background building** in the style bible's detail budget (§21) with a
**secondary-tier front door**. That inversion is the whole design brief. Spend
almost nothing on the mass and almost everything on the 2.8 m of arch, columns,
globes and transom — and then check from the aerial camera that the arch still
reads, because a doorway that disappears at the app's distance has bought you
nothing.

The finished asset must be immediately recognizable as this building, consistent
with the real one from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single building: the two-storey stucco volume on the measured
footprint, the parapet with its coping and dentil band, the alley facade with its
entrance ensemble, two text bands, second-floor window and two flanking windows,
the finished north-west elevation, the plain south-east and north-east
elevations, and the flat roof with its bulkhead and vents.

Do not include unrelated surrounding city geometry: 45–49 South Park, 41–43 South
Park, the warehouse to the south-east, the rear yard or its tree, Jack London
Alley, the street, the sidewalk, the utility pole and its guy wires, parked cars,
people, plinths, cameras or lights. Temporary context may appear in review renders
but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; at most
6,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The alley
facade faces **225.9°** and the long axis runs back at **45.9°**. Build on the
measured rectangle in 2.3 rather than modelling an axis-aligned bar and rotating
it. Record the measured heading in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the facade parapet
crest) must land at exactly **8.40 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/95-jack-london-alley/build_95_jack_london_alley.py` (deterministic
build script), `artifacts/95-jack-london-alley/95-jack-london-alley.blend`, and
`artifacts/95-jack-london-alley/95-jack-london-alley.glb`. The script must rebuild
the model reliably enough for future revision. Do not modify or rename an
unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`95-jack-london-alley-top.png`, `-north.png`, `-east.png`, `-south.png`,
`-west.png`, plus `95-jack-london-alley-contact-sheet.png`, at least one high
three-quarter aerial beauty render `95-jack-london-alley-aerial.png`, and a night
render `95-jack-london-alley-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection;
use orthographic or long-lens cameras; label directions from the researched
orientation; the top view must clearly show the roof plane, the coping ring and
the parapet step at the alley end; the aerial view uses the style bible's camera
assumptions (30–50 degrees down, long lens). Simple tabletop lighting, neutral
warm background, minimal depth of field, and every image must depict the same
exported model.

Because the building stands at 45.9°, none of the four cardinal elevations shows
its public face square-on. Add **two** extra views: one square-on at the 225.9°
alley facade, and one **close** three-quarter of the entrance ensemble alone
(arch, columns, globes, transom) at a scale where the modelling can actually be
judged. The entrance is where this asset succeeds or fails and a 15 m-wide
elevation render will not show you.

## Validate the exported GLB

Re-import `95-jack-london-alley.glb` into a fresh isolated Blender scene and
validate the re-import, not the source scene. Report object count, triangle count,
dimensions, bounding-box min/max, min Z, XY center offset, material names,
image-texture count, camera count, light count, animation count,
applied-transform status, negative-scale status, normal-orientation status,
unexpected geometry, and per-material contract compliance. Render at least one
review image from the re-imported asset. Write
`artifacts/95-jack-london-alley/validation.json` and
`artifacts/95-jack-london-alley/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **15.8 × 15.7 m** even
though the building is 8.6 × 13.7 m — that is the exact consequence of a 45.9°
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "95-jack-london-alley",
  "file": "95-jack-london-alley.glb",
  "anchor": [
    -122.393443,
    37.781346
  ],
  "targetHeightM": 8.4,
  "cat": 8,
  "name": "Gran Oriente Filipino Masonic Temple (95 Jack London Alley)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`"estimated": true` is deliberate and is the honest call: the roof deck is
measured, the parapet crest on top of it is not. See 2.1.

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/95-jack-london-alley.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or
*derived* are visual or photogrammetric estimates, not published figures — the
executing agent must re-verify anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 95 Jack London Alley, San Francisco CA 94107 | OSM `node/2353636746`; landmark designation report; SOMA Pilipinas |
| Also known as | Gran Oriente Masonic Temple; home of Rizal Lodge No. 12 | designation report; California Freemason |
| Block / lot | 3775 / 039 — **shared with 45–49 South Park**, which fronts the same lot; zoning `SPD` (SOMA–South Park) | designation report property table; DataSF assessor roll `wv5m-vpq2` |
| Built | **1951** — corroborated on the building itself by `MCMLI AD` incised at the base of the facade near the north-west corner | designation report ("Built: 1907, 1909, 1951"); SF Examiner; knowthis.place |
| Architect | **Unknown** | designation report, "Architects: Unknown" — do not attribute |
| Structure | **two storeys, rectangular plan, flat roof** | designation report §character-defining features — **surveyed** |
| Roof deck | **7.84 m** above grade (LiDAR height median over 457 cells at 50 cm); majority 7.76 m; mean 8.06 m; σ 1.27 m | DataSF `ynuv-fyni`, `sf16_bldgid` 201006.0108499 — **measured**; flat roof, so median ≈ deck |
| Parapet crest | **8.40 m** — *derived*: the LiDAR deck plus ~0.55 m of parapet, cross-checked photogrammetrically against the 2016 square-on facade photograph (two independent reductions gave 8.3 m and 8.6 m) | **derived, not published** — this is the plan's weakest number, see 2.15 risk 1 |
| LiDAR maximum | 12.99 m | same — **rejected**, it is 4.0σ above the median and matches 45–49 South Park's own 13.00 m maximum exactly; a 0.5 m cell sampling the taller neighbour, the same failure the Earl Warren and 106 South Park plans document |
| DataSF LiDAR footprint | `mblr` SF3775039 / `sf16_bldgid` 201006.0108499, OBB **13.68 × 8.57 m** at 43.9°, 112.9 m² polygon, 457 cells at 50 cm | DataSF `ynuv-fyni` — **measured**, and the source this plan builds on |
| OSM footprint | `way/71211338`, min-area OBB **20.35 × 9.37 m** at 45.9°, 190.0 m², 99.6% rectangular fill | OSM API, reprojected — **measured but wrong at the rear**, see 2.3 |
| Design footprint | **8.6 × 13.7 m, ~118 m²** | the DataSF OBB, rounded; corroborated by Bing z20 aerial at ~8.8 × 14.5 m |
| Ground | 11.20 m NAVD88 minimum, 11.64 m median, 12.35 m maximum (1.15 m of fall) | DataSF `ynuv-fyni` — the app's terrain handles this, not the asset |
| OSM tags (POI node) | `amenity=place_of_worship`, `religion=christian`, `denomination=Masonic`, `name=Gran Oriente Filipino Masonic Temple`, `check_date=2026-05-31` | OSM `node/2353636746` — the `religion` tag is disputed, see 2.15 risk 5 |
| OSM tags (building way) | `building=yes` only — **no height, no name, no address** | OSM `way/71211338` |
| Facade heading | alley elevation faces **225.9°** (south-west, onto Jack London Alley); long axis runs back at 45.9° | measured from both footprint sources, which agree to 2.0°; Jack London Alley's own centreline bears 134.4°, parallel to the facade to within 1.5° |
| Setback | facade ~6.6 m from the alley centreline; the building stands essentially on the property line | measured, OSM highway `way/8919615` |
| Neighbours | **45–49 South Park** (north-west, LiDAR median 12.08 m — *taller by 4.2 m*), **41–43 South Park** (north-east/rear, LiDAR median 9.83 m), and an unnamed warehouse to the south-east (LiDAR median 14.82 m — *much taller*) | DataSF `ynuv-fyni` — **measured**; the temple is the shortest thing on its block |
| Designation | subject of a **draft** Article 10 landmark designation report (2017, Landmark No. XXX, never numbered in the document available); a SOMA Pilipinas cultural asset; period of significance 1947–1951, Criterion: Events | SF Planning / OASIS draft report — **verify current status before calling it a designated landmark**, see 2.15 risk 6 |
| Owner / use | Gran Oriente Filipino; assembly hall, still in use by Rizal Lodge No. 12, the last Gran Oriente lodge in California | designation report; SF Examiner; California Freemason |

### 2.2 Sources

- **Gran Oriente Filipino Hotel, Residence, and Masonic Temple Complex — Landmark
  Designation Report (draft, 2017)**,
  `https://static1.squarespace.com/static/5b2c30b58f51305e3d641e81/t/607d36dc86015c6f61d7e31e/1618818784827/Gran+Oriente_Landmark+Designation+Report.pdf`
  — **the backbone of this plan.** Supplies the 1951 date, the two-storey
  rectangular flat-roofed massing, the "Architects: Unknown" attribution, the
  Masonic symbolism, and a nine-bullet character-defining-features list for 95
  Jack London Alley specifically (see 2.4). It also contains the only two
  photographs of the building located anywhere: a square-on 2016 facade shot and a
  2016 close-up of the entrance transom. Found via `exa` `web_search_advanced_exa`.
- SOMA Pilipinas, "Gran Oriente Masonic Temple",
  `https://www.somapilipinas.org/cultural-assets-1/gran-oriente-masonic-temple`
  — reproduces the designation report's description; the cultural-asset framing.
- California Freemason, "Portal to the Past" (2 June 2021),
  `https://californiafreemason.org/2021/06/02/portal-to-the-past/`
  — the only source that calls the building **Moorish**, and the source for Rizal
  Lodge No. 12 still meeting here.
- SF Examiner, "The amazing saga of the Gran Oriente Filipino Hotel" (10 March 2023)
  — the 1951 construction and the "last Gran Oriente lodge in California" claim.
- Know This Place, 45–49 South Park — "Gran Oriente Filipino Masonic Temple built
  behind it in 1951"; the 1982 alterations permit on the shared lot.
- DataSF `ynuv-fyni` (Building Footprints, LiDAR-derived, 2010 survey, refreshed
  2023-09-11), `sf16_bldgid` 201006.0108499 — footprint, ground elevation, roof-deck
  height, and the neighbours' heights that explain the 12.99 m maximum.
- DataSF `wv5m-vpq2` (Assessor Historical Secured Property Tax Rolls), parcel
  3775039 — **records the lot as the 1909, three-storey, 7-unit apartment building.
  It does not describe this building at all.** That is why there is no assessor
  height or storey count here.
- OSM `way/71211338` (the footprint, and the over-trace of 2.3),
  `node/2353636746` (the POI and its tags), `way/8919615` (Jack London Alley),
  and **note 3830661** — the open note that started this build, in which two
  mappers argue about whether a Masonic lodge is a place of worship.
- Bing Maps aerial (Vexcel), z20, tiles around `37.78135, -122.39344` — the roof
  surface, the coping ring, the rooftop boxes, and the decisive evidence that
  OSM's rear third is a tree in a yard. Esri World Imagery at the same location is
  monochrome and useless at z20 (a known SF limitation).
- Google/other street-level imagery was **not** available to this session; the two
  designation-report photographs are the entire visual record this dossier rests
  on. That is a real limitation — see 2.15.

### 2.3 Orientation and placement

The building sits in the interior of the block bounded by South Park (north-west),
Third Street, Brannan Street and Second Street, addressed on **Jack London Alley**,
the narrow lane that bisects the South Park oval north-west to south-east. It was
built *behind* 45–49 South Park, on the same lot, and it faces **south-west across
the alley**. Its long axis runs back to the north-east into what is now a small
yard with a mature tree.

**The two footprint sources disagree, and OSM is the one that is wrong.**

| Source | What it is | Verdict |
|---|---|---|
| DataSF LiDAR footprint SF3775039 / 201006.0108499 | 2010 raster-derived built area, 457 cells | **authoritative** — OBB 13.68 × 8.57 m at 43.9°, area centroid `-122.3934430, 37.7813460` |
| Bing z20 aerial, roof plane read against a metric grid | 2020s imagery | **confirms** — roof reads ~14.5 × 8.8 m, same axis, same centre to ~1 m |
| OSM `way/71211338` | untagged building trace | **rejected at the rear** — OBB 20.35 × 9.37 m at 45.9°; its south-west two-thirds match, its north-east third does not exist |

Three independent checks kill the OSM depth:

1. Sampling the OSM rectangle along its own long axis against every DataSF
   building polygon in the block: the south-west 13.0 m falls inside the temple's
   polygon (median height 7.84 m); the next 3.0 m falls inside **41–43 South
   Park's** polygon (median height 9.83 m); the last 2.0 m falls inside no
   building at all.
2. Bing z20 aerial shows a **tree canopy** occupying OSM's rear third, and the
   dark roof membrane visibly stops short of the OSM outline.
3. The two footprint centroids are 2.64 m apart, displaced along the long axis
   toward the alley — exactly the signature of a rectangle extended at one end.

Design footprint: a plain rectangle **8.6 m × 13.7 m** centred on the manifest
anchor, long axis running back at 45.9° (north-east). In Blender coordinates
(metres, `+X` east, `+Y` north, origin on the anchor) the four corners are:

```
corner                 X (east)   Y (north)   which end / which flank
alley  north-west        -7.91      -1.68     Jack London Alley frontage, NW side
alley  south-east        -1.92      -7.86     Jack London Alley frontage, SE side
rear   north-west        +1.92      +7.86     yard end, NW side
rear   south-east        +7.91      +1.68     yard end, SE side
```

The alley frontage is the −7.91/−1.92 edge (8.6 m long, facing 225.9°); the two
long 13.7 m edges are the north-west flank (facing 315.9°, toward 45–49 South
Park) and the south-east flank (facing 135.9°, toward the warehouse).

Because the heading is 45.9° off the axes, the axis-aligned XY bounding box of the
bare volume is **15.81 × 15.72 m**. That is correct and is not a scale error.

**No party walls.** Unusually for this neighbourhood, all four elevations stand
free. 45–49 South Park is 4.2 m taller and set back across a narrow gap to the
north-west; the warehouse to the south-east is 7.0 m taller and also detached. The
designation report's "textured stucco cladding on the façade and north elevation"
confirms the north-west flank is a finished elevation, not a blind wall — and the
2016 oblique photograph shows it standing free with a dentilled parapet band along
its top. This building is a small pink box in a well of much taller neighbours,
which is exactly how it reads in the app.

### 2.4 What each side shows

The designation report's character-defining-features list for 95 Jack London Alley
is quoted here in full, because it is the only survey-grade description of this
building that exists:

> Two-story, rectangular massing and plan with flat roof · Textured stucco
> cladding on the façade and north elevation · Central entrance with incised
> pointed arch and tripartite arch detail, columns topped by globe shapes, inset
> rectangular entry opening surmounted by three arched fixed transom windows
> separated by engaged columns · Gold leaf compass and square with the letter "G"
> at the center painted on center transom window above door · Incised text above
> main entry reading "GRAN ORIENTE FILIPINO MASONIC TEMPLE" · Incised text at the
> parapet reading "DEDICATED TO THE SUPREME ARCHITECT OF THE UNIVERSE" · Small
> rectangular window openings flanking central entrance · Horizontal rectangular
> window opening at second floor · Incised text located at the base of the façade
> near northwest corner reading "MCMLI AD"

**South-west (alley elevation, the public face)** — Blush-pink textured stucco,
edge to edge, with no cornice line, no string course and no base. It is one
uninterrupted plane from grade to parapet, and every feature is cut into it. From
the top down: the parapet carries the DEDICATED TO THE SUPREME ARCHITECT OF THE
UNIVERSE course in shallow incised capitals just below its coping; a single
**horizontal** rectangular window sits high and centred at second-floor level,
white-framed, filled with a warm amber grille; below it the two-line GRAN ORIENTE
FILIPINO / MASONIC TEMPLE course; then the entrance.

The entrance is the building. A pointed, slightly ogee arch is incised into the
wall as a recess ~0.8 m deep. Inside it, a **trilobed** arch head springs over the
doorway. Above the double panelled wood doors (dark, with the numeral 95 over
them) sit three round-arched transom windows separated by short white engaged
colonettes; the centre one carries the **gold-leaf square and compass with a
letter G** on dark glass. Two **free-standing white columns** stand in front of the
door plane, one either side of the opening, each capped with a **white sphere**.
Two small, roughly square, white-framed windows flank the entrance at ground
level. MCMLI AD is incised at the base near the north-west corner.

**North-west (long flank, toward 45–49 South Park)** — A finished stucco
elevation, not a party wall. Nearly blank: the 2016 oblique shows one small
opening near the alley end and one projecting element. Its parapet carries a
**dentilled band** along the top — a repeating tooth course, the report's
"cornice". This band is the only thing besides the pink that distinguishes this
building's top edge from a plain slab, and it is genuinely visible from the app's
aerial camera.

**South-east (long flank, toward the warehouse)** — Not photographed. Assume plain
stucco, likely without the dentil band (the report cites stucco on the facade and
north elevation only, which suggests this face was treated more cheaply). Build it
blind and plain, and say so in `REPORT.md`.

**North-east (rear, onto the yard)** — Not photographed. Utilitarian. Assume plain
stucco with a service door and one or two small openings. Faces the yard and its
tree; visible in the app only obliquely and from above.

**Top** — Flat, at 7.84 m, ringed by a parapet whose coping reads as a bright line
against the dark deck in the Bing aerial. The facade parapet at the alley end
stands ~0.25 m proud of the side parapets, which is what carries the inscription
band. The deck itself is a **dark charcoal membrane** with a small light-coloured
patch near the north-west edge, two small reddish-brown boxes near the alley end
(vent or skylight kerbs) and an irregular darker patch mid-roof. No PV, no
large plant, no bulkhead visible — a genuinely sparse roof, which for once is the
truth rather than a gap in the research.

### 2.5 Recognition cues (ranked)

1. **The Moorish arch ensemble.** Ogee recess, trilobed head, three transoms, two
   white globe-capped columns. Nothing else in this manifest looks like it, and it
   occupies a third of an 8.6 m facade — big enough to survive the miniature.
2. **The pink box among gray giants.** A 8.4 m blush-pink cube in a well formed by
   a 12.1 m tenement, a 14.8 m warehouse and a 9.8 m neighbour. From the aerial the
   colour and the height step together are instantly locatable.
3. **The two white spheres.** At thumbnail size the arch collapses into a dark
   notch with two bright dots either side. That reduced silhouette is still
   unmistakable, which is the definition of a good cue.
4. **The banded top edge** — a light coping ring with a dentil course along the
   long north-west flank, and the facade parapet stepping up above it at the alley
   end with an inscription band across it.
5. **The blank everything-else.** Three bare elevations is itself a cue: this is a
   hall, not a house or a shop, and the emptiness reads that way.

### 2.6 Miniature translation

**Preserve**

- The 8.6 × 13.7 m footprint, the 45.9° axis and the 225.9° facade heading, exactly
- Two storeys, 7.84 m deck / 8.40 m facade-parapet crest, and the 0.25 m step
  between the facade parapet and the side parapets
- The entrance ensemble in full: recess, ogee, trilobe, three transoms, two
  columns, two globes
- The gold square-and-compass on the centre transom, as a distinct flat shape
- Both incised text courses, as inset bands
- The single **horizontal** second-floor window — the proportion matters; a
  vertical window there mis-reads the building as a house
- The dentil band on the north-west parapet
- The pink

**Simplify / exaggerate**

- The ogee arch is exaggerated: model the recess ~0.15 m wider and ~0.25 m taller
  than measured so the notch still reads from 150 m up
- The trilobe becomes three tangent circular arcs on a single extruded profile —
  one object, not three
- The three transom windows become one recessed `Toy_glass` panel with two
  0.09 m `Toy_trim` mullions; the arched heads are cut into the panel's top edge,
  not modelled as separate arcs
- The colonettes between the transoms disappear (the mullions stand for them)
- The globes are 10-segment UV spheres, not 32 — they read as dots
- Incised text becomes a 0.02 m inset band of a marginally darker value. **No
  glyphs, at any scale.** MCMLI AD disappears entirely
- The dentil course becomes a single `Toy_trim` band with a 0.04 m shadow reveal
  under it; individual teeth are sub-pixel
- Stucco texture becomes flat colour
- Downpipes, meters, conduit, the wall-mounted light and the utility pole
  disappear
- The south-east and north-east elevations get one service door and two small
  openings between them, and nothing else
- Neighbours, the alley, the sidewalk, the yard and its tree are not modelled

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. All z from grade.

1. Main volume: extrude the 2.3 rectangle from z=0 to z=7.84, `Toy_peach`.
2. Roof deck: flat cap at z=7.84, `Toy_roofd`.
3. Side/rear parapet: a 0.22 m thick wall on the north-west, south-east and
   north-east edges, z=7.84 → **8.15**, `Toy_peach`, with a `Toy_trim` coping
   0.10 m tall and 0.04 m proud on top.
4. Facade parapet: the same wall on the south-west edge but z=7.84 → **8.40**,
   with its own `Toy_trim` coping. This is the tallest geometry and must land
   exactly on 8.40.
5. Facade inscription band: an 8.0 × 0.26 m strip inset 0.02 m into the facade
   parapet, centred at z=8.05, `Toy_stone`.
6. Dentil band, north-west flank only: a 0.20 m `Toy_trim` band running the full
   13.7 m at z=7.90 → 8.10, 0.05 m proud, with a 0.04 m shadow groove under it.
7. Second-floor window: 1.80 × 0.95 m, centred on the facade, sill at z=4.85,
   recessed 0.10 m, `Toy_glassl` (the real one is filled with an amber grille, not
   dark glass — that is why it is the light glass key and not `Toy_glass`), with a
   0.09 m proud `Toy_trim` frame.
8. Name band: a 6.0 × 1.05 m strip inset 0.02 m into the facade, centred at
   z=3.40, `Toy_stone`.
9. Entrance recess: a 2.90 m wide opening in the facade, 0.80 m deep, from grade
   to an ogee apex at z=3.05. Profile: vertical jambs to z=2.05, then two arcs
   meeting at a point. Recess back plane and soffit `Toy_coral` — the recess is
   noticeably warmer and more saturated than the facade in every photograph, and
   that warmth is what makes the notch read as a doorway rather than a hole.
10. Trilobe head: a three-lobe arch profile 2.30 m wide springing at z=2.10 with
    lobe crowns at z=2.55/2.70/2.55, extruded 0.12 m proud of the recess back
    plane, `Toy_coral`.
11. Transom panel: 2.10 × 0.62 m at z=2.05 → 2.67, recessed 0.06 m behind the
    trilobe, `Toy_glass`, split by two 0.09 m `Toy_trim` mullions.
12. Square and compass: a flat 0.44 × 0.44 m `Toy_gold` emblem, 0.015 m proud of
    the centre transom pane. Model it as a compass-and-square silhouette if the
    triangle budget allows, otherwise as a chamfered diamond — but do **not** omit
    it, it is the night hero.
13. Doors: a 1.55 × 2.05 m `Toy_ink` slab set into the recess back plane, with a
    0.04 m centre reveal.
14. Columns: two `Toy_trim` cylinders, 0.22 m diameter, z=0 → 2.15, at x = ±1.05 m
    from the entrance centreline, standing 0.35 m proud of the door plane, each on
    a 0.30 × 0.30 × 0.12 m plinth and capped with a 0.30 m `Toy_trim` sphere at
    z=2.30. 10 segments, 6 rings.
15. Flanking windows: two openings 0.95 × 1.05 m, sills at z=1.35, recessed 0.08 m,
    `Toy_glass`, with 0.07 m proud `Toy_trim` surrounds and sills. Centres at
    **−2.20 m and +3.30 m** from the facade centreline (north-west negative) — see
    2.15 risk 3 before committing to that asymmetry.
16. Service door on the north-east (rear) elevation: 1.10 × 2.10 m `Toy_ink` inset
    0.06 m, off-centre toward the north-west.
17. Two small openings, 0.70 × 0.70 m, `Toy_glass`, one on the south-east flank at
    z=5.20 and one on the rear at z=5.20.
18. Roof furniture: one 1.20 × 0.90 × 0.45 m `Toy_stone` box near the north-west
    edge and two 0.55 × 0.55 × 0.35 m `Toy_rust` boxes near the alley end, all
    below the parapet line.
19. Bevel 0.08 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, palette **names** from `sf-asset-check`; two hexes are adjusted
off-palette under the style bible's SF exception for tinted facades, following the
precedent set in `artifacts/165-south-park/REPORT.md` (keep the key, move the hex,
record the WARN).

| Material | Hex | Used for |
|---|---|---|
| `Toy_peach` | `#e8cdc9` | the stucco body on all four elevations and the parapets — **off-palette, pre-authorised**; the building's identity colour |
| `Toy_coral` | `#d9a189` | the entrance recess back plane, soffit and trilobe — **off-palette, pre-authorised**; warmer and more saturated than the body |
| `Toy_trim` | `#f3efe6` | parapet coping, dentil band, the two columns and their globes, window frames and sills, transom mullions |
| `Toy_stone` | `#d9d2c2` | the two incised text bands, the roof box |
| `Toy_glass` | `#2a4d73` | transom panel, the two flanking windows, the two small rear/flank openings |
| `Toy_glassl` | `#6f95b8` | the second-floor window (amber grille reads light, not dark) |
| `Toy_ink` | `#3a3530` | the entrance doors, the rear service door |
| `Toy_gold` | `#caa64a` | the square-and-compass emblem |
| `Toy_roofd` | `#45454a` | the flat roof deck |
| `Toy_rust` | `#a86444` | the two small roof boxes |
| `Toy_gold_Glow` | `#e6c46a` | the square-and-compass at night — the hero |
| `Toy_trim_Glow` | `#f6e6c4` | the two globes and a thin warm spill in the entrance recess |

Two notes on colour:

- **The pink is read from two 2016 photographs, one of them fully shaded**, and
  the sampled values disagree by a lot: `#c7b8be` from the shaded square-on shot
  (a facade lit only by blue sky, so it reads cold and mauve) and `#ddc7ca` from
  the overcast oblique. `#e8cdc9` is the reconciled warm reading and it is
  *inferred*. What is **not** in doubt is the relation: a warm light pink body,
  off-white trim, a distinctly warmer recess, dark doors, a charcoal roof. Hold
  the relation; move the hue if better photography turns up, and say so in
  `REPORT.md`.
- Do not desaturate the pink toward `Toy_sand` "to fit the palette". A pale beige
  box in this block is invisible, and the colour is cue #2 in 2.5.

**Night state (required).** Category 8 is night profile 3 (dark) and that is
correct for a lodge that meets a few evenings a month — this asset should be one
of the quietest things in the night city. Hero glow: **the gold square and compass
on the centre transom**, a single small bright emblem. Supporting accents: the two
**globes** on the columns and a thin warm spill on the floor and jambs of the
entrance recess. Nothing else lights — not the second-floor window, not the
flanking windows, not the roof, not the text bands.

Glow-shell discipline, which this asset is unusually exposed to because its glow
elements are *spheres*: the app renders `_Glow` in a separate layer, and a
**closed** shell is two alpha layers deep, so it reads about 23% opaque by day
rather than 12% — on a pale pink facade that will tint everything behind it. Author
the globes as opaque `Toy_trim` spheres with a **single-sided outward glow cap**
(the upper hemisphere only) proud of the surface, never as closed glow spheres.
Same rule for the emblem: a flat one-sided glow quad 0.015 m proud of an opaque
`Toy_gold` emblem.

### 2.9 Top surface

A 8.6 × 13.7 m rectangle at 7.84 m, seen constantly from above and — because this
building sits at the bottom of a well of taller neighbours — from almost nowhere
else at street level. Three things carry it:

1. **The bright coping ring** against the charcoal deck, with the facade end
   stepping 0.25 m higher and reading as a thicker, brighter bar. From directly
   overhead this asymmetric frame is the roof's whole composition.
2. **The dentil band** along the north-west parapet, which from a shallow aerial
   angle catches the eye as a textured edge on one side only.
3. **The height step.** The roof sits 4.2 m below 45–49 South Park's and 7.0 m
   below the warehouse's, so in the baked city it is a distinct pit in the block
   rather than part of a continuous surface. Nothing needs to be modelled for this
   to work — the neighbours are really there — but the roof must be *designed*
   enough to reward looking into that pit.

The Bing z20 aerial shows no PV, no bulkhead and no large plant: one light patch
near the north-west edge, two small reddish boxes near the alley end, and an
irregular darker patch mid-deck that is most likely a membrane repair. Resist
inventing rooftop equipment to fill the plane. A sparse roof is the correct answer
here and step 18 is already generous.

### 2.10 Scope

**In the GLB:** the single building — the two-storey stucco volume on the measured
footprint, the stepped parapet with its coping and dentil band, the alley facade
with its entrance ensemble (recess, ogee, trilobe, transoms, emblem, doors,
columns, globes), the two text bands, the second-floor window, the two flanking
windows, the plain south-east and north-east elevations with their service door
and two small openings, and the flat roof with its three boxes

**Not in the GLB:** 45–49 South Park, 41–43 South Park, the warehouse to the
south-east, the rear yard or its tree, Jack London Alley, the street, the
sidewalk, the utility pole and its guy wires, the wall-mounted light, vehicles,
people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 6,000 — smaller than 106 South Park's 7,000 because the mass is smaller and
three elevations are empty, but with a much heavier concentration in one place.
Suggested split: main volume ~200, roof deck ~50, stepped parapet with coping ring
~700, dentil band ~250, two text bands ~150, second-floor window with frame ~350,
entrance recess and ogee profile ~700, trilobe ~450, transom panel with mullions
~350, emblem ~150, doors ~120, two columns with plinths and globes ~1,000, two
flanking windows with surrounds ~600, rear/flank door and two openings ~350, roof
boxes ~200, bevel overhead ~350.

If the first build lands above 6,000 the answer is fewer sphere segments and a
simpler ogee profile, not a raised cap — and never a simplified entrance, which is
the only reason this building is bespoke rather than a kit piece.

### 2.12 Draft manifest entry

```json
{
  "id": "95-jack-london-alley",
  "file": "95-jack-london-alley.glb",
  "anchor": [
    -122.393443,
    37.781346
  ],
  "targetHeightM": 8.4,
  "cat": 8,
  "name": "Gran Oriente Filipino Masonic Temple (95 Jack London Alley)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark, Case B.** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: '95JackLondon'`) and re-bake the affected tiles, or the baked procedural
  building will intersect the GLB. This is the Case B path in
  `docs/asset-plans/INTEGRATION-PROMPT.md`.

- **The exclusion radius is comfortable, and it is comfortable only because the
  anchor moved.** `excluded()` in `pipeline/buildings.mjs` drops a footprint when
  its centroid **or** any ring vertex falls inside the circle. Measured from the
  manifest anchor (the DataSF LiDAR area centroid) the bake reads:

  | Polygon | Triggers at | Via |
  |---|---|---|
  | this building, DataSF SF3775039 / 201006.0108499 | **0.05 m** | its own centroid |
  | this building, OSM `way/71211338` as an Overture proxy | **2.64 m** | its centroid |
  | 45–49 South Park, DataSF 201006.0014671 | **7.07 m** | nearest ring vertex |
  | 41–43 South Park, DataSF 201006.0038546 | 7.10 m | nearest ring vertex |
  | 41–43 South Park, OSM `way/112759867` | 7.48 m | nearest ring vertex |
  | warehouse, DataSF 201006.0003676 | 7.83 m | nearest ring vertex |

  The safe window is therefore **(2.64, 7.07) m** — it has to exceed 2.64 so the
  Overture gap-fill version is dropped too (`addBuilding()` returns null on
  exclusion, so `markOccupied()` never runs and `occupiedFraction()` cannot be
  relied on to block a re-add), and stay under 7.07 so 45–49 South Park survives.
  **Use `exclude: 4.8`** — 2.16 m of margin below and 2.27 m above.

  **Do not measure this from the OSM centroid.** Anchoring on OSM's (wrong) OBB
  centre collapses the window to (2.60, 4.47): the neighbouring buildings' rings
  reach within 4.47 m of it, and OSM's own trace **shares two vertices** with
  41–43 South Park's ring at 5.41 m, so a radius large enough to be safe on one
  side eats a standing 9.8 m building on the other. Moving the anchor 2.6 m
  south-west onto the true footprint centre — which is where the building actually
  is — widens the window from 1.87 m to 4.43 m. This is the same "measure from
  vertices, against the real bake input" lesson as 165 South Park, with the
  additional twist that here the *anchor* was the fix, not the radius.

  Expect **two** footprints dropped in this cell, not one: DataSF traces this
  building and so does Overture. Confirm against the real
  `pipeline/data/overture_buildings.geojsonseq` at integration time and prove the
  outcome with `pipeline/verify-rebake.mjs` — exactly two footprints dropped, no
  neighbour lost, and specifically 41–43 South Park and 45–49 South Park still
  standing.

- **Do not set `clearTrees: true`.** The tree in the rear yard is real, it is the
  reason OSM's over-trace was detectable, and at `exclude: 4.8` the radius does not
  reach it anyway.

- `loadRadius`: the default formula gives `max(2500, 8.4 × 30) = 2500` m. Take the
  default.

- **Camera preset.** In `app/src/camera.js` the rig places the camera at
  `(sin(yaw), sin(pitch), cos(yaw)) × distance` from the pivot, and this project's
  `+z` is **south**, so the convention that puts the camera in front of a facade of
  bearing *B* is `yaw = 180 − B`. For B = 225.9° that gives **yaw ≈ 314**, putting
  the camera south-west of the building, over the alley, looking north-east at the
  entrance. Start from `camera: { distance: 120, yaw: 314, pitch: 24 }` and tune
  against the live scene. The distance is short on purpose: this is an 8.4 m
  building whose only content is a 2.9 m doorway, and the 150 m used for 106 South
  Park would fly the user to a pink dot.

- **Verify the arch survives the bake.** After integration, look at the building
  from the default flight altitude, not just from the camera preset. If the
  entrance has collapsed into an undifferentiated dark smudge, the fix is a wider
  and deeper recess in stage 2, not a closer camera preset.

- **The Gran Oriente complex is now two-thirds modelled.** 104–106 South Park (the
  hotel) shipped; this is the temple; 45–49 South Park (the residence, 1909,
  three storeys, the tenement this building was built behind) is still procedural.
  Finishing the set would let the concierge and any lore copy treat the three
  buildings as one story, which is how the designation report treats them and how
  they are actually understood in SoMa Pilipinas.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 8.40 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~15.8 × 15.7 m
      is expected for an 8.6 × 13.7 m building at 45.9°)
- [ ] Footprint 8.6 × 13.7 m — **not** 9.37 × 20.35 m; the OSM trace was rejected
- [ ] Facade on the **south-west** 8.6 m end, facing 225.9°, not on a long side
- [ ] Entrance ensemble complete: recess, ogee apex, trilobe, three transom bays,
      emblem, doors, two columns, two globes
- [ ] The dentil band exists on the **north-west** flank only
- [ ] The second-floor window is **horizontal** (wider than tall)
- [ ] Facade parapet stands 0.25 m proud of the side parapets
- [ ] Triangles at or under 6,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`; the two
      off-palette hexes (`Toy_peach`, `Toy_coral`) recorded as accepted WARNs with
      this plan's 2.8 cited
- [ ] `_Glow` only on the emblem, the two globes and the recess spill; every glow
      surface a **single-sided** shell proud of opaque geometry, no closed shells
- [ ] No cross, steeple, nave, bell or any other church signifier
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + the square-on 225.9° facade view + the close entrance
      three-quarter + contact sheet + night render, all regenerated from the final
      export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **The height is derived, not published, and it is the largest single risk in
   this plan.** The 7.84 m roof deck is a real LiDAR median over 457 cells and is
   solid. The 8.40 m crest is that deck plus a parapet measured off one
   photograph, by two reductions that disagreed by 0.3 m. No published figure was
   located: the designation report gives no dimension, OSM's building way carries
   no `height` tag, and the assessor's record for lot 3775/039 describes the 1909
   apartment building in front of it instead. If the executing agent finds a
   permit, a drawing or a better photograph, that source wins. Until then the
   manifest entry says `"estimated": true`, and it should.
2. **The footprint correction is confident but it rests on three inferences, not a
   survey.** DataSF's polygon, the Bing aerial and the polygon-membership test all
   agree that OSM's rear third is not building — but all three are remote sensing.
   If ground evidence shows a low rear wing under that tree, the depth goes back
   toward 20 m, the anchor moves back north-east, and **the exclusion analysis in
   2.13 must be redone from scratch**, because it is anchored on the corrected
   centre. Flag it loudly rather than quietly re-tracing.
3. **The facade may not be symmetric, and the plan guesses that it is not.** In the
   2016 square-on photograph the north-west flanking window sits visibly closer to
   the entrance than the south-east one does. That could be real, or it could be
   the perspective of a wide-angle lens used close to a building on a 6 m alley —
   the same photograph's verticals converge hard enough that its vanishing points
   will not solve consistently. Step 15 encodes the asymmetry (−2.20 / +3.30).
   **Verify before building.** If the evidence is inconclusive, build it
   symmetric at ±2.60: a wrong asymmetry is a worse error than a lost one, because
   an asymmetric facade looks deliberate and will be copied forward.
4. **Two photographs is the entire visual record.** No street-level imagery of the
   south-east flank, the north-east rear, or the roof at any usable resolution was
   available to this session, and the two photographs that exist are both from
   2016 and both in the designation report. Three of the four elevations in 2.4
   are therefore *assumed*, not observed. The risk is bounded — a lodge hall's back
   walls are genuinely plain, and the app sees them obliquely at best — but the
   dossier should not be mistaken for a survey.
5. **The building's own use is contested in the source data.** OSM note 3830661,
   still open, is two mappers disagreeing about whether `amenity=place_of_worship`
   `religion=christian` is correct for a Masonic lodge; the tag was added in 2026
   and the note reopened a fortnight later. It is a lodge. Category 8 is the right
   *bucket* — `meeting_house` and `temple` both map there, and the punched-masonry
   facade treatment it triggers is what this building needs — but no church
   signifier belongs in the model, the card copy or any lore text. If the pipeline
   ever grows a `lodge` or `fraternal_hall` subcategory this is its first member.
6. **It is a *draft* designation report, not a designation.** The document is
   headed "DRAFT report dated XXX 2017" and carries "Landmark No. XXX". Whether the
   Gran Oriente complex was ever adopted as an Article 10 City Landmark was not
   established in this session. Describe it as a SOMA Pilipinas cultural asset and
   as the subject of a landmark designation report; **do not call it a designated
   City Landmark** until someone checks the adopted Article 10 list.
7. **The pink is a hue guess on top of a confident value relation.** See 2.8.
8. **The globes are almost certainly also lamps.** They read as white spheres on
   column caps in both photographs and the designation report describes them
   purely as symbols — the terrestrial and celestial globes — but their placement
   either side of a doorway is where you would put entrance lighting, and the
   night state in 2.8 lights them. If research shows they are solid stone or
   plaster and unlit, keep them glowing anyway: it is a defensible miniature
   exaggeration of the building's one symbolic gesture, and the alternative is a
   night facade carrying a single 0.44 m emblem and nothing else. Record the
   decision in `REPORT.md` either way.
