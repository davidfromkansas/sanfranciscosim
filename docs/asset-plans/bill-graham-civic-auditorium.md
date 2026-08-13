# Bill Graham Civic Auditorium — SF-SIM asset plan

The 1915 Exposition Auditorium on the south side of Civic Center Plaza: a granite
Beaux-Arts front of three giant arched windows between two heavy end pavilions, and —
the thing nobody sees from the street and everybody sees from this app's camera — a
**dark octagonal dome ~58 m across** covering the great hall behind it.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/bill-graham-civic-auditorium/`. This document is the plan only: Part 1 is the
runnable task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `bill-graham-civic-auditorium` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4173272, 37.7780592` (measured OBB centre, OSM way/25759141) |
| Target height | **37.0 m** — apex of the octagonal hall dome (OSM `height=37 m`, corroborated by 2010 city LiDAR `hgt_max` 36.98 m) |
| OSM footprint | 127.95 x 78.64 m oriented bbox, 9,314 m² polygon, long axis bearing **80.69°** cw from N |
| Triangle cap | 26,000 |
| Category | `17` (theater_cinema / concert hall) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Bill Graham Civic Auditorium GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the Bill Graham Civic Auditorium
(99 Grove Street) and deliver it as a downloadable, validated GLB.

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
7. `artifacts/war-memorial-opera-house/` — the reference implementation of this exact
   deliverable, and the closest sibling building: same Civic Center, same street grid,
   same Beaux-Arts vocabulary (arched openings, colonnade, entablature, cornice, hipped
   roofscape), same lit-arch night pattern
8. `docs/asset-plans/bill-graham-civic-auditorium.md` — this plan, whose dossier is your
   research starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The **dark octagonal dome** over the great hall — the dominant form from above and
  the reason this building is worth an asset at all
- The Grove Street (north) front: **three giant round-arched windows** between paired
  engaged columns, over a rusticated base, under a frieze, cornice and parapet
- The two heavy **end pavilions** (Larkin west, Polk east), taller than the arcade, each
  crowned by a large cartouche and parapet sculpture blocks
- The continuous **marquee canopy** running the length of the arcade at street level
- Plainer, warmer flanks and rear against the granite front
- A designed roof: the bright flat deck around the dome with its clusters of plant

## Research the auditorium independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North, east, south and west elevations
- Aerial and roof/top views — **the dome is only legible from above; do not skip this**
- Ground-level views
- Day and night appearance (the arched windows are routinely floodlit in colour)
- Publicly available drawings, plans or diagrams — HABS documented this building
- The dome's plan geometry: octagon, its span, and how far south of the building's
  centre it sits
- Whether the 37 m OSM tag is the dome apex or something else (it is the dome apex)

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/bill-graham-civic-auditorium/REFERENCE.md` containing: source links and
what each establishes; verified dimensions and location; orientation; observations from
all four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Bill Graham Civic Auditorium,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel art,
not generic low-poly, and never accurate in one view while invented in the others.

It must also read as a family member of `city-hall` and `opera-house`, which stand
within 200 m of it: same slab thicknesses, same bevel weight, same restrained palette,
same lit-arch night language. Three giant arches is a *smaller* count than the Opera
House's seven — resist the temptation to add bays to fill the frontage. The front is
mostly wall, and that is what makes the three arches monumental.

## Scope of the exported asset

Export the auditorium block only: base, arcade, pavilions, marquee, cornice, parapet,
roof deck, roof plant and the dome.

Do not include unrelated surrounding city geometry: City Hall, the Civic Center Plaza
lawns, Brooks Hall below the plaza, Grove/Larkin/Polk streets, trees, people, vehicles,
plinths, cameras or lights. Temporary context may appear in review renders but must not
leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 26,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The long axis bears
**80.69° cw from true north** and the arcade front faces **north** onto Grove Street and
Civic Center Plaza. The contract's "front faces −Y" rule therefore cannot be honoured
literally; real-world orientation wins (AGENTS rule 5) and the deviation goes in
`REPORT.md`.

## Reproducible Blender workflow

Headless only: `blender -b --python script.py -- args`; no GPU, so use Workbench or
CPU Cycles. Keep
`artifacts/bill-graham-civic-auditorium/build_bill_graham_civic_auditorium.py`
(deterministic build script),
`artifacts/bill-graham-civic-auditorium/bill-graham-civic-auditorium.blend`, and
`artifacts/bill-graham-civic-auditorium/bill-graham-civic-auditorium.glb`. The script must
rebuild the model reliably enough for future revision. Do not modify or rename an
unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`bill-graham-civic-auditorium-top.png`, `-north.png`, `-east.png`, `-south.png`,
`-west.png`, plus `-contact-sheet.png`, at least one high three-quarter aerial beauty
render `-aerial.png`, and a night render `-night.png` showing the glow set.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; **the top view must clearly show the octagonal dome, the bright
deck around it and the roof plant clusters**; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting, neutral
warm background, minimal depth of field, and every image must depict the same exported
model.

## Validate the exported GLB

Re-import `bill-graham-civic-auditorium.glb` into a fresh isolated Blender scene and
validate the re-import, not the source scene. Report object count, triangle count,
dimensions, bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/bill-graham-civic-auditorium/validation.json` and
`artifacts/bill-graham-civic-auditorium/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "bill-graham-civic-auditorium",
  "file": "bill-graham-civic-auditorium.glb",
  "anchor": [
    -122.4173272,
    37.7780592
  ],
  "targetHeightM": 37,
  "cat": 17,
  "name": "Bill Graham Civic Auditorium",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate, explicitly requested job — run
`docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in
`docs/asset-plans/bill-graham-civic-auditorium.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Fact | Value | Source |
|---|---|---|
| Official name | Bill Graham Civic Auditorium (San Francisco Exposition Auditorium 1915; San Francisco Civic Auditorium 1916–92) | Wikipedia, OSM `name`/`alt_name` |
| Address | 99 Grove Street, San Francisco, CA 94102 | OSM `addr:*` |
| OSM element | way/25759141, `amenity=theatre`, `building=civic`, `wikidata=Q4909197`, surveyed 2025-11-22 | Overpass |
| Opened | 2 March 1915 (groundbreaking December 1913), for the Panama–Pacific International Exposition | Wikipedia |
| Architects | John Galen Howard, Frederick H. Meyer, John W. Reid Jr. | Wikipedia |
| Style | Beaux-Arts with French and Italian Renaissance elements | noehill (SF Point of Historical Interest) |
| Structure & cladding | four storeys on a steel frame; grey granite to the main facade, brick to the sides and rear | noehill |
| Capacity | 8,500 | Wikipedia |
| Below grade | Brooks Hall (1958) under Civic Center Plaza, immediately north | Wikipedia |
| Renovations | 1962–64, 1989–90, 1994–96, 2005, 2010 | Wikipedia |
| Footprint (measured) | 127.95 x 78.64 m minimum-area oriented bbox; 9,314 m² polygon area (45-node) | OSM geometry, reprojected |
| Long-axis bearing (measured) | **80.69°** cw from true north | same |
| OBB centre (measured) | −122.4173272, 37.7780592 | same |
| **Crest height** | **37.0 m** | OSM `height=37 m`; 2010 city LiDAR `hgt_max` 36.98 m (mblr SF0812001) — two independent sources to 2 cm |
| Main roof deck | ~23.0 m | LiDAR median 22.99 m, mean 24.26 m over 37,661 cells |
| Ground elevation | ~16.4 m NAVD88 | LiDAR `gnd_min_m` |
| Dome (measured from imagery) | regular octagon, **58.6 m flat-to-flat**, centred ~8 m south of the building centre | Esri World Imagery z19, rotated to the building axis |

### 2.2 Sources

- OSM way/25759141 via the Overpass API — footprint geometry (45 nodes), tags, `height`,
  `wikidata`, survey date.
- Nominatim (bounded to the SF bbox) — address resolution.
- DataSF *Building Footprints (with LiDAR-derived heights)*, resource `ynuv-fyni`,
  building `SF0812001` — `hgt_median` 22.99 m, `hgt_max` 36.98 m, ground elevation.
  Independently confirms the OSM height tag.
- Esri World Imagery (z19, ~0.24 m/px), rotated to the building axis and measured
  photometrically — the octagonal dome's span and offset, the deck, the plant clusters.
- Wikimedia Commons, in particular:
  - `CIVIC AUDITORIUM, CORNER VIEW … HABS CAL,38-SANFRA,71-C-1` — the best single
    elevation reference: front arcade, end pavilion, cornice, parapet, flagpoles;
  - `Exposition Auditorium (9615942845).jpg` — near-frontal view of the whole Grove
    front, from which the bay count is taken;
  - `Bill Graham Civic Auditorium 1 2018-09-19.jpg` — night close-up of three bays:
    the lit arched windows and the marquee light band;
  - `Bill Graham Civic Auditorium from Larkin and Grove St, SF.jpg` and
    `… from NE.JPG` — the Larkin pavilion, the flank, and the parapet sculpture.
- noehill.com SF Point of Historical Interest entry — storey count, structure, cladding.

### 2.3 Orientation and placement

Long axis bears 80.69° cw from N — the Civic Center grid, within half a degree of the
War Memorial Opera House's 81.11°. Build frame: `u+` runs ENE along Grove Street,
`v+` runs NNW (north). The arcade front faces **north** onto Grove Street and Civic
Center Plaza, looking straight at City Hall. Larkin Street is the **west** end, Polk
Street the **east** end, and the rear faces **south**.

Because the front faces north, the contract's "front faces −Y" cannot hold; the plans
README already resolves this — real-world orientation wins and the deviation is recorded.

### 2.4 What each side shows

- **North — Grove Street (the front, 128 m).** Rusticated granite base; a continuous flat
  **marquee canopy** at ~4.6 m running the length of the central range; above it
  **three giant round-arched windows** (~11 m wide, ~17 m pitch) filled with a fine
  gridded glazing, separated by paired engaged columns on pedestals carrying projecting
  entablature blocks; above, an architrave and frieze carrying the incised name and
  circular wreath medallions over each pier; a modillioned cornice; a parapet with
  sculptural groups. **Two end pavilions** flank the arcade, each ~24 m wide, rising
  higher than the arcade parapet and crowned by a large oval cartouche flanked by
  figures. A row of tall flagpoles stands on the parapet.
- **West — Larkin Street.** The pavilion turns the corner in the same granite with
  pedimented upper windows, balustraded balconies on consoles and a heavy cornice;
  behind it the hall's flank is a long, much plainer wall with sparse punched openings.
- **East — Polk Street.** Mirrors the west: pavilion, then plain flank.
- **South — rear.** The plainest elevation: service doors, loading, a flat wall.
- **Above.** A bright flat membrane deck inside the parapet, with the **dark octagonal
  dome** filling the southern two-thirds; a small circular lantern at its apex; clusters
  of rooftop plant along the north edge and at the corners.

### 2.5 Recognition cues (ranked)

1. The dark octagonal dome, ~58 m across, seen from above — unmistakable and unique in
   the city.
2. Three giant arched windows, monumentally spaced, over a granite front.
3. The end pavilions with their oval cartouches, taller than the range between them.
4. The unbroken marquee canopy at street level.
5. The long, low, plaza-facing horizontality: 128 m of front, only ~26 m tall.

### 2.6 Miniature translation

Per §22 of the style bible. Keep 1–5. Drop: the fine window mullion grid inside each
arch (one flat `Toy_glass` pane instead), the column fluting and capitals (paired
pilaster strips with a cap block), the modillion teeth (one clean cornice slab), the
incised inscription, the balcony balustrades on the pavilions, the figure sculpture
(chunky pedestal blocks in its place), and **the flagpoles**.

The flagpoles are the one painful cut: they are a real identity cue, but they rise to
~39 m — above the dome — so keeping them would break the height contract, and at 0.1 m
thick they are sub-pixel at the app's camera and would read as noise. Cut, and recorded
in 2.15.

Exaggerate: the dome's rise (a shallow real dome flattens into nothing at this scale —
push the apex to the measured 37 m and keep the octagon's facets crisp), the marquee's
projection, and the depth of the arch reveals.

### 2.7 Massing recipe

Build frame `(u, v, z)`: `u+` ENE along Grove at bearing 80.69°, `v+` north,
origin at the OBB centre. `u ∈ [−64, +64]`, `v ∈ [−39.3, +39.3]`.
North face (Grove) `v = +39.3`, south `v = −39.3`, west (Larkin) `u = −64`,
east (Polk) `u = +64`.

| Element | extent | z range | Notes |
|---|---|---|---|
| Great-hall block | full 128 x 78.6 | 0 → 23.0 | `Toy_sand` walls; the mass |
| Rusticated base | all round, proud +0.4 | 0 → 5.0 | `Toy_stone` |
| Front range | `v` +19.3 → +39.3 | 0 → 25.8 | `Toy_trim` granite |
| Central arcade | `u` −26 → +26 | — | 3 arches, pitch 17.0, width 11.0 |
| Giant arches | — | sill 7.6, spring 14.8, crest 18.3 | round heads, 10 segments |
| Marquee canopy | `u` −28 → +28, proj 4.5 | 4.6 → 5.4 | `Toy_ink` fascia |
| Paired pilasters | 4 pairs on the arcade | 5.4 → 20.0 | `Toy_white` |
| Frieze + medallions | front range | 20.0 → 22.9 | wreath discs over each pier |
| Cornice | front range, proud +1.1 | 22.9 → 24.3 | `Toy_white` |
| Parapet | front range | 24.3 → 25.8 | plain, with pedestal blocks |
| End pavilions | 24 wide x 34 deep, both ends | 0 → 29.8 | attic + cartouche above the cornice |
| Roof deck | inside the parapet | 23.0 | `Toy_roofd` |
| **Octagonal dome** | R 31.7 (flat-to-flat 58.6), centre `v` −7 | 23.0 → 36.3 | `Toy_roofd`, 8 facets |
| Apex lantern | R 4.0 octagon | 36.3 → **37.0** | `Toy_roofd` cap, `Toy_steel` collar |
| Roof plant | 5 clusters per imagery | 23.0 → 25.5 | `Toy_steel` |

### 2.8 Materials and palette

| Surface | Material | Hex |
|---|---|---|
| Rusticated base | `Toy_stone` | d9d2c2 |
| Grove-front granite, pavilions | `Toy_trim` | f3efe6 |
| Flanks and rear walls | `Toy_sand` | ece4d4 |
| Columns, frieze, cornice, parapet, medallions | `Toy_white` | f7f4ec |
| Arched windows, punched windows | `Toy_glass` | 2a4d73 |
| Marquee fascia, arch reveals, doors | `Toy_ink` | 3a3530 |
| Roof deck, dome, lantern cap | `Toy_roofd` | 45454a |
| Roof plant, lantern collar | `Toy_steel` | 9aa0a6 |
| Lit arch panes (night) | `Toy_mustard_Glow` | d9a441 |
| Marquee light band (night) | `Toy_white_Glow` | f7f4ec |

The `Toy_trim` front against `Toy_sand` flanks is the model's reading of "granite front,
brick sides and rear": a value step, not a colour step, so the building still sits in
the Civic Center family instead of turning red.

### 2.9 Top surface

This is the asset's most important surface (§10) and the only place the dome exists.
The design: dark octagonal dome, hard-edged facets, on a bright `Toy_roofd` deck inside
a light parapet, with five compact plant clusters placed where the imagery shows them —
two flanking the front range, three along the flanks. Nothing else; the octagon must not
compete with clutter.

### 2.10 Scope

The auditorium block only. No City Hall, no plaza lawns, no Brooks Hall, no street
furniture, no trees, no vehicles, no plinth, **no flagpoles** (2.6).

### 2.11 Triangle budget

Cap 26,000; target 12,000–16,000. The dome and lantern are cheap (~200 tris); the cost
is the arcade heads, the pavilion window grids and the bevels on ~120 boxes.

### 2.12 Draft manifest entry

```json
{
  "id": "bill-graham-civic-auditorium",
  "file": "bill-graham-civic-auditorium.glb",
  "anchor": [-122.4173272, 37.7780592],
  "targetHeightM": 37,
  "cat": 17,
  "name": "Bill Graham Civic Auditorium",
  "estimated": false,
  "loadRadius": 2500
}
```

`loadRadius`: the default rule gives `max(2500, 37 × 30) = max(2500, 1110) = 2500`.
The building is broad rather than tall, so it is illegible well before 2.5 km; and the
baked block under it is carved out, so a longer radius would only cost boot bandwidth.

### 2.13 Integration notes (for later, not this task)

New landmark — **Case B**. `bill-graham-civic-auditorium` exists in neither
`pipeline/lib/landmarks.mjs` nor `app/src/landmarks.js`, so integration needs:

1. a manifest entry (2.12);
2. a registry entry in `pipeline/lib/landmarks.mjs` with id, lon/lat, height and an
   exclusion radius large enough to clear the 128 x 78.6 m footprint (≈75 m — the
   largest exclusion zone of any Civic Center asset, so check it does not swallow City
   Hall's or the Opera House's baked blocks);
3. a re-bake of the affected 500 m tiles;
4. audit 1.6 and `node pipeline/landmark-streaming-check.mjs` against a build.

Run `docs/asset-plans/INTEGRATION-PROMPT.md` for the full procedure.

### 2.14 Validation checklist

`validation.json` must show: fresh-scene re-import; `min_z ≈ 0`; XY centre within 0.5 m;
dims ≈ 128.0 x 78.6 x 37.0 m; tris ≤ 26,000; zero image textures; zero transparent
materials; every material `Toy_*` and none named `Toy_body`; no cameras, lights,
animation, armatures or constraints; transforms applied; no negative scales; normals
outward by the per-object signed-volume test with the ray test as a supplementary
metric; glow materials present and shipping with emission strength 0.

### 2.15 Open questions and risks

- **The dome's profile is *inferred*.** Its plan geometry is measured from imagery, but
  whether it rises as a straight-sided octagonal pyramid or a curved octagonal dome is a
  judgement from the satellite shading. The model uses straight facets, which is the
  more legible choice at this scale and the safer one for the triangle budget.
- **Bay count.** Three giant arches is counted from `Exposition Auditorium
  (9615942845).jpg` and the 2018 night close-up. It is a low number for a 128 m frontage
  and will look wrong to anyone expecting an Opera-House-like colonnade — it is correct.
- **Flagpoles omitted** (2.6). If a future revision wants them, the target height must be
  re-decided first; they are the true crest of the real building.
- **Pavilion attic height 29.8 m is *inferred*** from photographs scaled against the
  25.8 m parapet; no drawing was found.
- **Flank cladding.** Sources say brick; photographs read as painted grey-beige. The
  model follows the photographs (`Toy_sand`) and treats the source as describing the
  substrate, not the finish.
- The 2010 LiDAR predates the 2010 renovation's rooftop work; plant positions come from
  more recent imagery and are *inferred* in height.
