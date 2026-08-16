# Herbst Theatre / War Memorial Veterans Building — SF-SIM asset plan

The northern half of the War Memorial pair: the near-twin of the Opera House across
the memorial court, holding the 916-seat Herbst Theatre where the UN Charter was
signed. The whole brief is *matched restraint* — this building only works if it
reads as the Opera House's sibling from the app's aerial camera.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/herbst-theatre/`. This document is the plan only: Part 1 is the runnable
task prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `herbst-theatre` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.4210354, 37.7795452` (oriented-bbox centre, measured) |
| Target height | **~31 m** at the attic hip ridge — the OSM `height=28` tag is the parapet, NOT the target (see 2.1) |
| OSM footprint | 67.38 m (N–S, Van Ness frontage) x 83.06 m (E–W depth), 4,437 m², long edges 81.11° cw from true north (OSM way/32865757) |
| Triangle cap | 18,000 |
| Category | `17` (Theatre or cinema) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Herbst Theatre (War Memorial Veterans Building) GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of the War Memorial Veterans Building — the
building that contains Herbst Theatre, 401 Van Ness Avenue — and deliver it as a
downloadable, validated GLB.

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
7. **`artifacts/war-memorial-opera-house/`** — the reference implementation AND the
   architectural twin. Read `REFERENCE.md`, `REPORT.md` and
   `build_war_memorial_opera_house.py` in full: the two buildings are officially
   "substantially identical structures", so every facade constant in that build
   script is a candidate constant here.
8. `artifacts/salesforce-tower/` — the canonical shape of this deliverable
9. `docs/asset-plans/herbst-theatre.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- The matched-twin relationship with the Opera House: identical cornice line,
  identical basement course, identical colonnade order, identical roof colour
- Giant-order Doric colonnade over a rusticated granite basement, facing east
- An OPEN second-floor loggia behind the colonnade (the Green Room loggia looks
  out at City Hall)
- Round-arched openings in a regular bay rhythm on every visible elevation
- One unbroken entablature and cornice line around the whole mass
- Dark metal hipped roofs with skylights over pale terra-cotta walls
- Flat, calm, strongly horizontal massing — no fly tower (this is the half of the
  pair that does NOT have one)

## Research the Veterans Building independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- North (McAllister St), east (Van Ness), south (memorial court) and west
  (Franklin St) elevations
- Aerial and roof/top views — the metal hipped roofs and skylights are the
  primary aerial cue
- Ground-level views, day and night
- Publicly available drawings, plans or diagrams
- The column count / bay count in the Van Ness colonnade, and the arched-window
  bay count on the flanks
- **Explicitly verify which of the two twins you are modelling.** The Opera House
  is way/32865161 at 301 Van Ness, SOUTH of the memorial court, and has a fly
  tower. This task is way/32865757 at 401 Van Ness, NORTH of the court, no fly
  tower. Getting this backwards is the single most likely failure of this task.

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

## Create a reference dossier

Write `artifacts/herbst-theatre/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence; and an explicit
section on **what differs from the Opera House twin** and what must match it
exactly. A contact sheet of attributed reference thumbnails is welcome if legally
permissible — do not commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

The finished asset must be immediately recognizable as the Veterans Building,
consistent with the real building from all four sides and above, architecturally
credible, and a premium handcrafted miniature — not photorealistic, not voxel
art, not generic low-poly, and never accurate in one view while invented in the
others.

**The twin test is a gate, not a nicety.** Render the finished model next to
`artifacts/war-memorial-opera-house/war-memorial-opera-house.glb`, both at scale
1.0, from the app's aerial camera. The basement course, cornice line and roof
colour must line up. If they do not, this asset is wrong.

## Scope of the exported asset

Export the Veterans Building block: colonnade, loggia, arched-window elevations,
entrance bays, cornice, attic and hipped roofs.

Do not include unrelated surrounding city geometry: the Opera House, City Hall,
Van Ness Avenue, McAllister or Franklin Streets, the memorial court, trees,
people, vehicles, plinths, cameras or lights. Temporary context may appear in
review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 18,000 triangles.

**Normalize the bbox top to the verified architectural height exactly**, so the
loader's `targetHeightM / measuredHeight` scale lands at 1.0.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The main
facade faces **east** onto Van Ness Avenue; the long axis bears 81.11° cw from
true north, the same bearing as the Opera House twin. Author true-world
orientation and document the heading. Record the decision and the measured
heading in `REPORT.md`.

## Reproducible Blender workflow

Blender 4.5 LTS or newer, headless only: `blender -b --python script.py -- args`;
no GPU, so use Workbench or CPU Cycles.

Keep `artifacts/herbst-theatre/build_herbst_theatre.py` (deterministic build
script), `artifacts/herbst-theatre/herbst-theatre.blend`, and
`artifacts/herbst-theatre/herbst-theatre.glb`. The script must rebuild the model
reliably enough for future revision. Do not modify or rename an unrelated
existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`herbst-theatre-top.png`, `herbst-theatre-north.png`, `herbst-theatre-east.png`,
`herbst-theatre-south.png`, `herbst-theatre-west.png`, plus
`herbst-theatre-contact-sheet.png` and at least one high three-quarter aerial
beauty render `herbst-theatre-aerial.png`. A night render
(`herbst-theatre-night.png`) is required, not optional.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the hipped roof planes,
the skylights and the parapet rhythm; the aerial view uses the style bible's
camera assumptions (30-50 degrees down, long lens). Simple tabletop lighting,
neutral warm background, minimal depth of field, and every image must depict the
same exported model.

## Validate the exported GLB

Re-import `herbst-theatre.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Normals: the per-object signed-volume test is
authoritative for a union of solids; the supplementary ray test must land within
0.15% residual. Render at least one review image from the re-imported asset.
Write `artifacts/herbst-theatre/validation.json` and
`artifacts/herbst-theatre/REPORT.md`.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "herbst-theatre",
  "file": "herbst-theatre.glb",
  "anchor": [
    -122.4210354,
    37.7795452
  ],
  "targetHeightM": 31,
  "cat": 17,
  "name": "Herbst Theatre (War Memorial Veterans Building)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`,
`pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a
separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md`
for that, together with the integration notes in
`docs/asset-plans/herbst-theatre.md`.
````

---

## Part 2 — Research and design dossier

Compiled 12 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address | 401 Van Ness Avenue, SF 94102 | OSM `addr:*` tags, SF Public Works |
| Dedicated | 11 November 1932 (Armistice Day) | SF Public Works, sfwarmemorial.org |
| Designed | 1927–28 | Wikipedia (War Memorial and Performing Arts Center) |
| Architects | Arthur Brown Jr. and G. Albert Lansburgh | Wikipedia, noehill SF Landmark #84 |
| Style | Beaux-Arts — "one of the last Beaux-Arts style structures erected in the United States" | Wikipedia |
| Relationship to Opera House | "two substantially identical structures, the Opera House and the Veterans Building, separated by a formal court"; "identical exteriors" | noehill (SF Landmark #84 designation), Wikipedia |
| Herbst Theatre | 916 seats, inside this building; originally "Veterans Auditorium", renamed 1977; UN Charter signed here 26 June 1945 | Wikipedia, SGH, SF Public Works |
| Envelope | Steel frame; terra-cotta-clad concrete infill walls; granite base; terra-cotta and steel-framed windows; terra-cotta balustrades | [SGH project page](https://www.sgh.com/project/san-francisco-war-memorial-veterans-building/) |
| Roof | **Metal roof with skylights** (both replaced in the 2013–16 rehabilitation) | SGH |
| Loggia | The second-floor Green Room "opens to a loggia facing City Hall" — i.e. an OPEN east-facing loggia behind the Van Ness colonnade | SGH |
| Rehabilitation | 2013–16 seismic upgrade + rehabilitation, $96.5 M city budget / $156 M total | SF Public Works, SGH |
| Footprint | **67.38 m (N–S) × 83.06 m (E–W)** oriented bbox; polygon area 4,437 m²; 37 nodes | OSM way/32865757, measured this session |
| Orientation | Long edges bear **81.11° cw from true north** (weighted dominant edge angle over 37 edges), identical to the Opera House twin and to the Civic Center grid | measured |
| OSM `height` | **28 m** — the parapet, *not* the summit (see below) | OSM way/32865757, `check_date=2026-02-23` |
| OSM `ele` | 22 m — ground elevation, not a building height | OSM |
| Architectural top | **~31 m** at the attic hip ridge — *inferred* | see 2.15 |

**On the height (this is the number most likely to be wrong).** AGENTS rule 5 and
the pipeline's iron rule both forbid taking an OSM `height` tag as the
architectural target when it describes a low shell. Here the evidence is:

- The Opera House twin's `height=44` is its **fly tower**, and the Opera House
  dossier explicitly derived its *main-block parapet ≈ 28 m* from **this
  building's** `height=28` tag, on the grounds that "the two buildings read
  identical to the cornice in photos". So 28 m is a parapet number on both twins.
- The Veterans Building has no fly tower, so its summit is the ridge of the
  hipped metal roof set back behind that parapet.
- The Opera House model's front-block hip — the same architectural element on the
  same cornice line — peaks at **31.0 m**. Adopting 31.0 m here makes the two
  buildings share a base course, a cornice line and a roof ridge, which is what
  "substantially identical structures" means.

Target height **31 m**, `"estimated": true`. The cornice at 24.5 m must match the
Opera House GLB exactly; that alignment is the real accuracy requirement, and it
is checkable in-app.

### 2.2 Sources

- https://www.openstreetmap.org/way/32865757 — footprint (37 nodes), `height=28`, `ele=22`, `building=civic`, `amenity=theatre`, `alt_name=Herbst Theatre`, address, `wikidata=Q5736243`
- https://www.openstreetmap.org/way/32865161 — the Opera House twin, for the pair geometry
- https://en.wikipedia.org/wiki/San_Francisco_War_Memorial_and_Performing_Arts_Center — architects, 1927–32, "identical exteriors", 7.5-acre site, matched pair across a formal courtyard, Herbst 916 seats, UN Charter
- https://noehill.com/sf/landmarks/sf084.asp — SF Landmark #84 designation: "two substantially identical structures … separated by a formal court", conceived to complement City Hall
- https://www.sgh.com/project/san-francisco-war-memorial-veterans-building/ — envelope materials, terra cotta, granite base, terra-cotta balustrades, **metal roof with skylights**, the Green Room loggia facing City Hall, rehabilitation scope
- http://sfpublicworks.org/veteransbuilding — dedication date, seismic upgrade scope, budget
- https://www.wikidata.org/wiki/Q5736243 — entity for Herbst Theatre
- `artifacts/war-memorial-opera-house/` (this repo) — the twin's verified dossier, facade decomposition, height ladder and build script; the single most useful reference for this asset

### 2.3 Orientation and placement

A rectangular block, front (colonnade) facing **east** onto Van Ness Avenue,
extending 83 m west to Franklin Street. Long edges bear 81.11° cw from true
north — the standard Civic Center grid rotation (Opera House 81.11°, Grace
Cathedral 81.03°, 555 California 81.23°).

The building sits **north** of the memorial court; the Opera House is south of
it. So this building's **south** flank faces the court and the Opera House, its
**north** flank faces McAllister Street, its **west** face is on Franklin. The
Opera House dossier's "north (memorial-court flank)" is this building's *south*
flank — the mirror. Do not copy the flank treatments across without flipping them.

Anchor: oriented-bbox centre of the footprint = **−122.4210354, 37.7795452**.
Recompute from the built model's own bbox centre before shipping — `placeGeneric`
puts the exported bbox CENTRE on the anchor, and the model's front steps push the
centre slightly east of the raw footprint centre (this is exactly the trap the
Opera House plan fell into: its plan anchor was 26 m off).

### 2.4 Footprint decomposition (measured from the 37-node polygon; u = metres back/west from the Van Ness front plane, v = metres north from the south edge, full frontage 67.38 m)

| Zone | u range | Width | v range |
|---|---|---|---|
| **Front pavilion** (colonnade block) | 0 → −3.1 | **45.49 m** | 10.98 → 56.47 |
| Shoulder step | −3.1 → −4.3 | 51.15 m | 8.26 → 59.41 |
| Shoulder step | −4.3 → −7.0 | 53.27 m | 7.14 → 60.41 |
| **Wings** (full frontage) | −7.4 → −20.1 | **67.38 m** | 0 → 67.38 |
| **Main block** | −22.6 → −78.5 | **51.4 m** | 7.8 → 59.3 |
| **Rear block** (Franklin St) | −78.5 → −83.06 | **41.15 m** | 12.86 → 54.01 |

The same four-part scheme as the Opera House (narrow front pavilion → full-width
wings → narrower main block → narrower rear block), at ~92% of the twin's N–S
dimensions and 80% of its depth. The two shoulder steps are the pavilion's
projecting end blocks; fold them into the corner-pavilion massing.

### 2.5 What each side shows

**East (Van Ness front)** — the hero elevation, matched to the Opera House:
rusticated granite basement with round-arched glazed openings; above a
balustraded course, the giant-order Doric colonnade of paired columns screening
an **open loggia** (the Green Room loggia, confirmed by SGH); full entablature,
cornice, then a low attic parapet. Rusticated full-height corner pavilions at
each end. *Inferred by twinning: 7 loggia bays / 8 column pairs, as on the Opera
House, at a slightly tighter pitch to fit the 45.5 m pavilion.*

**South (memorial-court flank)** — faces the court and the Opera House across it.
The formal flank: arched windows in a regular rhythm between pilasters, the same
cornice line, court-facing skylights in the hipped roof. This is the elevation
the app's camera sees when it looks at the pair, so it carries the twin test.

**North (McAllister St flank)** — the working flank: same rhythm, service doors
in the base course, no court skylights.

**West (Franklin St rear)** — lower, plainer service block (~41 m wide) with a
regular small-window grid and a parapet. No fly tower.

**Top** — NOT flat. Dark metal hipped roofs with skylights (SGH), a large flat
deck behind the parapets, and modest roof plant. Because there is no fly tower,
the roofscape *is* the whole aerial read for this building — design it, don't
default it.

### 2.6 Recognition cues (ranked)

1. **It is the Opera House's twin** — same base course, same cornice line, same
   Doric colonnade, same roof colour, seen as a matched pair across the court.
2. The **7-bay paired-column loggia** over the rusticated arcaded basement.
3. **Strong horizontality**: one unbroken cornice line across the whole 67 m front.
4. **No fly tower** — the calm, level silhouette is what distinguishes it from
   the Opera House at a glance from the air.
5. Dark metal hipped roofs with skylights over pale terra-cotta walls.

### 2.7 Miniature translation

**Preserve**

- The four-part massing straight from the footprint table in 2.4
- Paired columns as genuinely doubled cylinders, not a picket row
- Arch alignment: basement arches under loggia arches, same bay grid
- The single unbroken cornice line at 24.5 m — **must equal the Opera House GLB's**
- The open loggia (recessed back wall, real depth), not applied pilasters
- Hipped roofs with court-facing skylights on the south slope

**Simplify / exaggerate**

- Fluting and capitals → plain shafts with square cap blocks
- Rustication → two grooved courses in the base band
- Balustrades → solid rail bands with post rhythm at the loggia only
- Attic perforations → shallow inset panels
- Skylights → flat glass panels set into the hip slopes
- Inscriptions, sculpture and lamp standards → dropped entirely

### 2.8 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render. **Every z value is
lifted unchanged from `build_war_memorial_opera_house.py` so the twins align.**

1. Basement course, rusticated `Toy_stone`, z 0 → **9.5**, proud 0.3, in the four
   footprint zones of 2.4; two grooved course lines across the front.
2. Front steps, three treads, `Toy_stone`, full colonnade width.
3. Corner pavilions, `Toy_stone`, full height z 9.5 → 27.0, ~5.6 m wide each,
   with a blind arched niche on the front face.
4. Loggia back wall recessed 2.6 m, `Toy_sand`, z 9.5 → 21.0; loggia floor slab.
5. 7 basement arches + 7 loggia arches on one bay grid (pitch ≈ 4.83 m).
6. Colonnade: 8 pedestals, **16 shafts in 8 pairs** (r 0.6, z **10.7 → 20.3**),
   8 cap blocks, bay balustrades.
7. Entablature z **21.0 → 23.0**, cornice z **23.0 → 24.5** projecting 1 m,
   attic parapet to **27.0** — the same ladder as the twin.
8. Wings, full 67.38 m frontage, u −7.0 → −20.5, with arched windows on the
   front and outer flanks and curved reentrant quadrants where they meet the
   main block.
9. Main block, 51.4 m wide, u −20.5 → −78.5, arched windows in a regular rhythm
   on both flanks, frieze band, cornice return.
10. Rear service block, 41.15 m wide, u −78.5 → −83.06, to z 20, window grid,
    parapet, deck.
11. Roofscape: `Toy_roofd` hipped roofs over the front block (ridge ∥ Van Ness,
    peak **31.0** = the summit) and over the main block (ridge E–W, peak ≤ 31.0),
    flat decks behind the parapets, glass skylight panels on the south slopes,
    two tidy plant clusters and a stair penthouse.
12. Bevel 0.12 m, 2 segments.

### 2.9 Materials and palette

Flat colors only, from the `sf-asset-check` palette. **Identical to the Opera
House's material set** — a different palette on a "substantially identical"
twin would be the loudest possible error.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `d9d2c2` | rusticated granite basement, corner pavilions, steps |
| `Toy_sand` | `ece4d4` | terra-cotta walls, loggia back wall, attic, rear block |
| `Toy_trim` | `f3efe6` | entablature, cornice, columns, pedestals, balustrades |
| `Toy_glass` | `2a4d73` | windows, skylights |
| `Toy_ink` | `3a3530` | arch reveals, doors, niches |
| `Toy_roofd` | `45454a` | metal hipped roofs, decks |
| `Toy_steel` | `9aa0a6` | roof plant |
| `Toy_mustard_Glow` | `d9a441` | lit panes behind every arch (night) |
| `Toy_white_Glow` | `f7f4ec` | colonnade floodlight soffit strip (night) |

**Night state (required).** Same restrained scheme as the twin: a
`Toy_mustard_Glow` lit pane set 5 cm proud behind each opaque `Toy_glass` arch
(basement, loggia, flank windows), plus one thin `Toy_white_Glow` soffit strip
under the entablature as the floodlit-colonnade cue. Rear service windows stay
dark. No roof or cornice outlining. The day colours of the glow surfaces are the
same palette entries the non-glow neighbours use, so nothing shifts at noon.

### 2.10 Scope

**In the GLB:** the Veterans Building block — basement, steps, colonnade, loggia,
corner pavilions, wings, main block, rear block, cornice, attic, hipped roofs,
skylights, roof plant.

**Not in the GLB:** the Opera House, City Hall, Davies Symphony Hall, Van Ness
Avenue, McAllister or Franklin Streets, the memorial court and its planting,
trees, people, vehicles, plinths, cameras or lights.

### 2.11 Triangle budget

Cap 18,000. Suggested split: basement and steps ~2k, colonnade and loggia ~4k,
arched windows ~5k, cornice/entablature/attic ~2k, wings and main block ~2k,
roofs and skylights ~2k, plant ~0.5k. The Opera House came in at 9,696 with a fly
tower; this should land lower.

### 2.12 Draft manifest entry

```json
{
  "id": "herbst-theatre",
  "file": "herbst-theatre.glb",
  "anchor": [
    -122.4210354,
    37.7795452
  ],
  "targetHeightM": 31,
  "cat": 17,
  "name": "Herbst Theatre (War Memorial Veterans Building)",
  "estimated": true,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`estimated` is `true` because the 31 m architectural top is inferred, not
published.

**Streaming decision:** `loadRadius: 2500` (the skill's default,
`max(2500, targetHeightM * 30)`). At 2,500 m the whole Civic Center is a small
cluster on screen and the swap to the baked stand-in is illegible. Note the
Opera House twin ships with no `loadRadius` (boot-loaded); beyond 2,500 m the
pair will therefore be GLB + baked, which is acceptable at that distance but
should be eyeballed once during QA.

### 2.13 Integration notes (for later, not this task)

- **New landmark (Case B).** Add a `pipeline/lib/landmarks.mjs` entry
  (`id: 'herbstTheatre'`, `name: 'Herbst Theatre'`, lon/lat from the manifest,
  `height: 31`, `exclude: ~58` — the Opera House uses 62 for a larger footprint,
  scale down accordingly) **and re-bake the affected tiles**, or the baked
  procedural building will intersect the GLB.
- Manifest id `herbst-theatre` maps to `herbstTheatre`.
- Add a camera preset matching the twin's style: `{ distance: 700, yaw: 90, pitch: 18 }`.
- Run audit 1.6 per `INTEGRATION-PROMPT.md`.
- After integration, verify the pair from the aerial camera: base course, cornice
  and roof colour must line up across the memorial court. This closes the open
  item the Opera House's REPORT.md left behind ("the near-identical Veterans
  Building stays procedural — check the pair still reads as twins").

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Max Z equals the target height exactly (loader scale = 1.0000)
- [ ] Dimensions plausible in meters and consistent with 2.1 / 2.4
- [ ] Triangles at or under 18,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on lit panes and the colonnade soffit strip, emission 0
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed
      volume authoritative; ray test residual ≤ 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + night + contact sheet regenerated from the final export
- [ ] **Twin test**: side-by-side aerial render with the Opera House GLB, cornice
      lines aligned
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The 31 m architectural top is inferred**, not published. It is derived from
  the twin's identical cornice ladder plus this building's own OSM parapet tag of
  28 m. No section drawing was found. Ship `"estimated": true`. If a published
  elevation turns up, this is the first number to correct.
- **The 7-bay colonnade is inferred by twinning.** The 45.5 m front pavilion is
  3.1 m narrower than the Opera House's 48.6 m, so the bay pitch tightens from
  5.14 m to ≈ 4.83 m. If photographic evidence shows a different bay count on
  this building, the photograph wins.
- **Mirror error is the top risk.** This building is north of the court; the
  Opera House is south of it. Every flank treatment copied from the twin's
  dossier must be flipped. Check the south flank is the formal one.
- **Nothing distinguishes it from the twin except the silhouette.** Resist the
  urge to add invented differentiating detail — the correct outcome is a building
  that looks *almost the same*, which is what the real pair does.
- A calm symmetrical block with no tower is easy to make boring. The loggia
  depth, the cornice projection and a genuinely designed roofscape are what give
  it life from the app's aerial camera.
