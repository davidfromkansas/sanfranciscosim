# 2 South Park (544 Second Street) — SF-SIM asset plan

The 1923 Kohler Co. plumbing-supply warehouse on the corner of Second Street and
South Park: a three-storey unreinforced-brick industrial loft, seismically
retrofitted in 1996–2000, now retail-over-office with the Blue Bottle Coffee
South Park café (Bohlin Cywinski Jackson, 2016) in its ground-floor storefront.
It is the building that closes the east end of the South Park oval, and its
identity is entirely typological: red brick piers, light cast-stone floor bands,
and enormous multi-pane steel industrial sash filling every bay on all three
public faces.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/2-south-park/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `2-south-park` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3932364, 37.7824236` (DataSF surveyed parcel 3775-005 area centroid, measured — see 2.13 for why not the LiDAR centroid) |
| Target height | **17.72 m** to the roof penthouse crest; main parapet ~13.6 m, roof deck 12.83 m (LiDAR-derived, see 2.1 and 2.15) |
| Footprint | 29.8 m (NE–SW, the South Park and Taber Place faces) x 20.9 m (NW–SE, the Second Street face); 623 m2 surveyed — a rectangle at bearing 45°/225° |
| Triangle cap | 9,000 |
| Category | `3` (office — retail ground floor, offices above) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 2 South Park GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 2 South Park (544 Second Street) in San
Francisco and deliver it as a downloadable, validated GLB.

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
7. `artifacts/188-south-park/` — the closest reference implementation in scale and
   neighbourhood (the loft block on the north rim of the same oval). Take its
   detail budget and its flat-roof-plus-penthouse approach; note that 188 is a
   2002 stucco building with punched windows while this is a 1923 brick warehouse
   whose windows are enormous and whose facade is a pier-and-spandrel grid — take
   its massing discipline, not its facade language.
8. `docs/asset-plans/2-south-park.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## What is already observed, and what is not

Unusually for this set, three of the four elevations and the roof were observed
directly (Google Street View May 2025 / Jan 2025 and Vexcel nadir aerial, see
2.2), and the geometry is corroborated by three independent surveys that agree
(2.3). Do not treat the facade description in 2.4 as inference — it is
observation, and if your own research contradicts it, say so loudly in
`REPORT.md`.

Two things are genuinely open and you must settle them (2.15):

1. **The 17.72 m LiDAR maximum.** It is 4.4σ above the 12.83 m median on a
   footprint with 1.12 m standard deviation. A roof penthouse is
   permit-confirmed to exist (SF permit 201810163246, 2018: elevator machine
   room moved to the *existing* penthouse on the roof) and raised structures are
   visible in the nadir aerial, so the reading here is a ~4.1 m stair/elevator
   penthouse above a 13.6 m parapet. But a mature street tree stands hard
   against the Second Street facade and rises above the parapet, and the
   matching 3.51 m LiDAR *minimum* is the classic edge-artifact signature. Check
   the max against imagery before you build a 4 m penthouse.
2. **The northwest (Taber Place) elevation.** It was not cleanly photographed.
   Every other face of this building is the same pier-and-sash grid and the
   dossier assumes this one is too, but it is an alley elevation and may be
   plainer, or may carry loading doors.

## Must capture

- The **corner**: two brick street elevations meeting at a right angle at Second
  Street and South Park, with the 20.9 m Second Street face and the 29.8 m South
  Park face both fully glazed with industrial sash. This building's identity is
  that it turns the corner.
- The **pier-and-spandrel grid**: red brick piers, four bays on Second Street,
  six on South Park and Taber Place, with light cast-stone sill/lintel bands
  running continuously between the piers at every floor line
- **Enormous multi-pane steel sash** that nearly fills each bay — the single
  loudest feature of a 1923 brick-and-timber warehouse, and the thing that must
  read from the aerial camera
- Three storeys, ~12.8 m to the roof deck, standing level with or just above its
  neighbours rather than over them
- A dark storefront band at the ground floor, with the café frontage at the
  Second Street corner (Blue Bottle) and papered/vacant bays along South Park
- The blank brick party wall on the southwest — this building has three public
  faces, not four
- A deliberately designed flat roof: light membrane, the set-back penthouse, a
  skylight and a grouped mechanical cluster toward the Taber Place side

## Research 2 South Park independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- All four elevations. Two are *ends* in the sense that matters here: the 20.9 m
  Second Street face and the 20.9 m southwest party wall. The long 29.8 m faces
  are South Park (southeast) and Taber Place (northwest).
- The roof, at higher resolution than the nadir aerial reached — this is where
  the penthouse question gets settled
- Ground-level views from Second Street and from South Park, which settle the
  storefront rhythm and the fire escape
- Day and night appearance
- Whether the building carries a historic-resource status (it sits just outside
  the South End Historic District boundary and the SoMa survey may still cover
  it); a DPR 523 form, if one exists, will describe the fenestration and cornice
  better than any photograph

Prefer architect/engineer publications, owner or institutional material,
planning and permitting documents, architectural press, geolocated photography,
and aerial/satellite imagery. Never rely on a single photograph, a single
AI-generated image, or a single unsourced 3D model. Separate verified facts from
visual inference; if sources disagree, document the disagreement and decide.

**One source conflict is already known — re-check it, do not silently
re-inherit the wrong value:** the storey count is 3 in every permit from 1996
onward and in the Assessor's roll, but the two 1992 permits say 2 and one 2017
permit says 4. Three is right; the outliers are tenant-space counts and a
clerical error. The 12.83 m LiDAR median over three floors (~4.3 m each) is
consistent with 3 and with nothing else.

## Create a reference dossier

Write `artifacts/2-south-park/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3-5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. A contact sheet of
attributed reference thumbnails is welcome if legally permissible — do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade
into broad rhythms, deliberately design every surface visible from above,
evaluate from the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21), not a hero
landmark: clear massing, one strong facade rhythm, a simple designed roof, and exactly
one identity cue carried hard — the pier-and-sash grid wrapping the corner. Resist
adding hero-tier ornament; a 1923 utility warehouse had none to begin with.

The finished asset must be immediately recognizable as 2 South Park, consistent with
the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1923 warehouse block: body, the three glazed elevations, the
blank southwest party wall, the parapet, the flat roof, the roof penthouse, the
skylight, the mechanical cluster and the South Park fire escape.

Do not include unrelated surrounding city geometry: South Park itself, its trees
or lawn, Second Street, Taber Place, the sidewalk, the café tables, the
bike-share dock, the street trees, the utility pole and overhead wires, the
neighbours at 524 Second Street or on South Park, parked cars, people, plinths,
cameras or lights. **Do not model the roof flagpole** — see 2.10; it is a thin
fixture that would corrupt the height normalization and is sub-pixel at the
app's camera. Temporary context may appear in review renders but must not leak
into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary
`.glb`; real-world meters; origin at base center; minimum geometry Z ~ 0;
applied transforms; no negative scales; outward normals; no duplicate or foreign
geometry; no image textures; no transparency; flat-color materials named `Toy_*`
from the project palette; `_Glow` suffix only on surfaces that glow at night; no
`Toy_body`; no cameras, lights, animations, armatures or constraints; no external
dependencies; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The Second
Street entrance faces **northeast, bearing 45°**; the long axis runs 45°/225°
(NE–SW), so build directly on the measured footprint rectangle in 2.3 rather than
modelling an axis-aligned box and rotating it. The contract's "front faces −Y"
cannot be honoured literally here; real-world orientation wins (AGENTS rule 5)
and the deviation goes in `REPORT.md`.

**Height normalization:** the tallest geometry in the export (the roof penthouse)
must land at exactly **17.72 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/2-south-park/build_2_south_park.py` (deterministic build script),
`artifacts/2-south-park/2-south-park.blend`, and
`artifacts/2-south-park/2-south-park.glb`. The script must rebuild the model reliably
enough for future revision. Do not modify or rename an unrelated existing GLB to satisfy
the task.

## Required review renders

Render the exact final geometry from controlled cameras:
`2-south-park-top.png`, `2-south-park-north.png`, `2-south-park-east.png`,
`2-south-park-south.png`, `2-south-park-west.png`, plus
`2-south-park-contact-sheet.png`, at least one high three-quarter aerial beauty render
`2-south-park-aerial.png`, and a night render `2-south-park-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and
projection; use orthographic or long-lens cameras; label directions from the
researched orientation; the top view must clearly show the full 29.8 x 20.9 m
roof — its penthouse, skylight and mechanical layout; the aerial view uses the
style bible's camera assumptions (30-50 degrees down, long lens). Simple tabletop
lighting, neutral warm background, minimal depth of field, and every image must
depict the same exported model.

Because the building is rotated 45° from the world axes, the four compass renders will
each show two faces at 45°. That is correct and expected — do not rotate the model to make
the elevations square on.

## Validate the exported GLB

Re-import `2-south-park.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture
count, camera count, light count, animation count, applied-transform status,
negative-scale status, normal-orientation status, unexpected geometry, and
per-material contract compliance. Render at least one review image from the
re-imported asset. Write `artifacts/2-south-park/validation.json` and
`artifacts/2-south-park/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **36 x 36 m** even though the
building is 29.8 x 20.9 m — that is the expected consequence of a 45° real-world heading,
not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "2-south-park",
  "file": "2-south-park.glb",
  "anchor": [
    -122.3932364,
    37.7824236
  ],
  "targetHeightM": 17.72,
  "cat": 3,
  "name": "2 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/2-south-park.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* are visual or
derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

**A note on the evidence quality of this dossier.** It is the strongest in the
South Park series. The geometry is corroborated by three independent surveys that
agree to within a metre (OSM trace, DataSF LiDAR footprint, DataSF surveyed
parcel), the history comes from the Assessor's roll and 56 building permits, and
three of the four elevations plus the roof were photographed. The two weak
points are named in 2.15 and both are about the roof: how much of the 17.72 m
LiDAR maximum is penthouse and how much is street tree, and what the Taber Place
alley elevation actually does. Everything else in 2.4 is observation.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Built | **1923** | SF Assessor secured roll, `year_property_built = 1923`; Dezeen and ArchDaily both describe it as a 1920s brick building |
| Original use | **Kohler Co. plumbing-supply warehouse** | Bohlin Cywinski Jackson project text via ArchDaily: "a former Kohler warehouse"; Dezeen: "once housed a Kohler plumbing supply warehouse" |
| Storeys | **3** | Assessor `number_of_stories = 3.0`; every permit 1996–2023 (two 1992 permits say 2 and one 2017 permit says 4 — see 2.15) |
| Structure | unreinforced brick masonry with heavy timber interior (Type III) | permits `constr type 3`; Assessor `construction_type = C`; BCJ text: "original brick walls and heavy timber support columns" |
| Seismic retrofit | UMB (unreinforced masonry building) compliance work 1992–2000 | permit 9205717 (1992, parapet bracing, $30k); 9612839 (1996, "to comply with umb ordinances", $150k); 9413382 (2000, "umb", $950k) |
| Building area | ~18,421 sq ft (~1,711 m2) over three floors | LoopNet listing for 2 South Park St / 544 2nd St |
| Current use | retail/café ground floor, office above | permits 201406178683, 201606069213 (retail→office 1/F), 201601076539 (2/F office TI), 201709016719 (3/F office TI) |
| Ground-floor tenant | Blue Bottle Coffee South Park, opened Nov 2016, café by Bohlin Cywinski Jackson, 1,200 sq ft; previously Jeremy's department store | permit 201605096890 ("install coffee bar millwork"); Blue Bottle Coffee Lab blog, 14 Nov 2016; SF Weekly, 18 Nov 2016; ArchDaily 898515 |
| Roof penthouse | **exists** — elevator machine room relocated into it in 2018 | permit 201810163246: "ground thru roof elevator. machine room changed fro gr fl to e penthouse on roof" |
| Roof works | skylight, gas flue and mechanical-unit bracing added 2017 | permit 201709016716 |
| Awnings | 8 canvas awnings installed 2002 (not present in 2025 imagery) | permit 200204043134 |
| Block / lot | 3775 / 005, APN 3775-005 | DataSF parcels, SF Assessor, LoopNet |
| Addresses | 544 Second Street (Assessor of record) = 2 South Park (permit and tenant address) | Assessor `property_location`; permits filed under both |
| Lot area | 6,734 sq ft (625.6 m2) | SF Assessor `lot_area` |
| Footprint (parcel, survey) | **29.81 m x 20.91 m, 622.9 m2**, rectangle at bearing 45.2°/225.2° | DataSF parcels `acdm-wktn`, blklot 3775005, reprojected — **measured** |
| Footprint (OSM cross-check) | 29.77 m x 21.27 m, 629.9 m2, bearing 45.6° | OSM way/112926339, reprojected — **measured**, agrees |
| Footprint (LiDAR cross-check) | 29.69 m x 22.11 m, 651.7 m2, bearing 45.5° | DataSF `ynuv-fyni` SF3775005 — **measured**; depth inflated 1.2 m by the usual LiDAR edge dilation |
| Roof crest | **17.72 m** above ground | DataSF LiDAR `hgt_maxcm = 1772` — **measured**, interpretation open (2.15) |
| Roof deck | **12.83 m** (median), 12.84 m (mean), 12.77 m (majority) | DataSF LiDAR `hgt_mediancm/meancm/majoritycm` — **measured**; three statistics within 7 cm of each other |
| Height std dev | 1.12 m | DataSF LiDAR `hgt_stdcm = 112` |
| LiDAR minimum | 3.51 m | DataSF LiDAR `hgt_mincm = 351` — an edge artifact, see 2.15 |
| OSM height tag | 13 | OSM way/112926339 — agrees with the LiDAR median to within 0.2 m; read as the parapet, see 2.15 |
| Ground elevation | 14.05 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Zoning | CMUO (Central SoMa Mixed Use Office); SSO on the Assessor's roll | DataSF parcels; Assessor |
| Neighbourhood | Financial District/South Beach; planning district South of Market | DataSF parcels |
| Neighbour heights | 524 Second Street 9 m, the southwest party-wall neighbour 12 m, 22–24 South Park 12 m, across Taber Place 12.4 m median | OSM `height` tags; DataSF LiDAR SF3775048 |
| Last sale | 21 June 1996 (the retrofit-and-conversion purchase) | SF Assessor `current_sales_date` |

### 2.2 Sources

- https://www.openstreetmap.org/way/112926339 — footprint, `addr:housenumber=2`, `addr:street=South Park`, `height=13`
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — footprint SF3775005 / `mblr=SF3775005`, heights 17.72 / 12.83 / 3.51 m, 2,613 cells at 50 cm
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — parcel 3775-005, 544 02ND ST, zoning CMUO — the surveyed footprint used as this plan's geometry
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor secured roll) — year built 1923, 3 storeys, lot 6,734 sq ft, sold Jun 1996
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 56 permits on block 3775 lot 005: the 1992 parapet bracing, the 1996 and 2000 UMB retrofits, the 2002 awnings, the 2016 coffee-bar and office TIs, the 2017 roof skylight/flue/mech, the 2018 elevator and its existing roof penthouse
- https://www.archdaily.com/898515/blue-bottle-south-park-bohlin-cywinski-jackson — "the street-level storefront of a former Kohler warehouse", original brick walls and heavy timber columns
- https://www.dezeen.com/2017/06/07/bohlin-cywinski-jackson-bluebottle-coffeeshop-historic-san-francisco-building-interiors-cafe-adaptive-reuse-california-usa/ — "a nearly century-old brick structure that once housed a Kohler plumbing supply warehouse"
- https://blog.bluebottlecoffee.com/posts/south-park-cold-bar — the café opening, Nov 2016
- https://www.sfweekly.com/dining/check-out-blue-bottle-s-first-cold-bar/ — "at 2 South Park, in the former home of Jeremy's department store"; "red brick, and exposed ceiling beams"
- https://sprudge.com/blue-bottle-coffee-south-park-115561.html — "It's a beautiful building… a lot of texture and history"
- https://www.loopnet.com/property/2-South-Park-Street-San-Francisco-CA-94107/06075-3775%20005 — APN 3775-005, 18,421 sq ft, built 1923
- Google Street View, **May 2025** (Second Street elevation and the corner three-quarter, panoramas near `37.78257,-122.39307` and `37.78252,-122.39300`) and **Jan 2025** (South Park elevation, panorama near `37.78228,-122.39312`) — the three public elevations, **observed**
- Google Maps satellite (Vexcel Imaging 2026, near-nadir, ~`37.78244,-122.39324` at max zoom) — the flat roof, the penthouse and skylight, the mechanical cluster, **observed**
- https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf and https://archives.sfplanning.org/documents/372-SOMA_Historic_Context_Statement_06-30-2009.pdf — the district and context statements for this warehouse type; **this building was not confirmed to be a contributor**, see 2.15

### 2.3 Orientation and placement

The building occupies the whole of its corner lot at the northeast end of the
South Park oval, where South Park meets Second Street. Taber Place, a service
alley, runs along its northwest side. Its southwest side is a party wall with
the next building on South Park. Second Street runs at bearing ~137.7°/317.7°
through SoMa, and the lot is square to it.

Three independent surveys agree on the shape: DataSF's surveyed parcel
(29.81 x 20.91 m, 622.9 m2), the OSM trace (29.77 x 21.27 m, 629.9 m2) and the
DataSF LiDAR footprint (29.69 x 22.11 m, 651.7 m2). Their bearings agree to
within 0.4°. Their centroids sit within 2.9 m of one another. **This plan takes
the surveyed parcel** for both the shape and the anchor, because the building
fills its lot (629.9 m2 of OSM building on a 622.9 m2 lot — the traces slightly
overshoot the survey, as they always do) and because the exclusion window is
wide enough here to afford it (2.13).

Rectangle corners in Blender coordinates (metres, `+X` east, `+Y` north),
centred on the anchor `-122.3932364, 37.7824236`, from the surveyed parcel:

```
(  17.93,   3.15)   East corner    (Second Street x South Park)
(   3.15,  17.93)   North corner   (Second Street x Taber Place)
( -17.93,  -3.15)   West corner    (Taber Place x the party wall)
(  -3.15, -17.93)   South corner   (South Park x the party wall)
```

in ring order: `(3.15, 17.93) → (17.93, 3.15) → (-3.15, -17.93) → (-17.93, -3.15)`.

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| N corner → E corner | 20.9 m | NE 45.2° | **Second Street front** |
| E corner → S corner | 29.8 m | SE 135.2° | **South Park front** |
| S corner → W corner | 20.9 m | SW 225.2° | **party wall** (blind) |
| W corner → N corner | 29.8 m | NW 315.2° | **Taber Place** (alley) |

Because of the 45° heading the axis-aligned bounding box is ~36 x 36 m. That is correct.

The measured parcel corners, before idealisation to a perfect rectangle, are
`(-16.95, -4.92) (4.20, 16.07) (18.94, 1.24) (-2.21, -19.75)` about the same
anchor; the departure from a true rectangle is under 0.2 m and is not worth
modelling.

### 2.4 What each side shows

Three of these four are **observed** from Google Street View. The Taber Place
elevation is the exception and is marked.

**Northeast (Second Street) — observed, May 2025.** The 20.9 m address
elevation, four bays wide. Red-brown brick piers roughly 1 m wide divide the
face; between them, on the second and third floors, sit enormous multi-pane
steel industrial sash windows that nearly fill each bay — a fine dark grid of
small panes, deeply set, with light cast-stone sills and lintels that run
continuously between the piers as horizontal bands. A further light band caps
the ground floor and another runs under the parapet coping, so the red brick
reads as four vertical piers crossed by three or four pale horizontals. The
ground floor is a dark storefront band: the Blue Bottle café at the South Park
corner end with people visible inside and café tables on the sidewalk, a
recessed timber-panelled entry with a small canopy near the middle, another
glazed bay, and a dark entry at the Taber Place end (marked "FOR LEASE" in the
May 2025 capture). A grey painted base runs below the shopfronts. The parapet is
plain brick with a stone coping and no cornice bracket work — this was a
utility building.

**Southeast (South Park) — observed, Jan 2025.** The long 29.8 m face onto the
oval, six bays of the same pier-and-sash grid, and the elevation that most of
the city sees. The upper two floors are almost entirely glass in dark steel
frames. A black steel fire escape descends the second and third floors toward
the southwest (party-wall) end. The ground floor here is a run of dark-framed
shopfronts, several papered over or blanked white in the Jan 2025 capture, with
a dark recessed entry near the southwest end and a dark painted base. Bay
centres are almost exactly 5.0 m. Bike-share docks and a street tree stand in
front of it; they are not part of the asset.

**Southwest (party wall) — observed indirectly.** Blind. The neighbour along
South Park is about 12 m tall (OSM), so almost this building's full height, and
this face carries no openings. Model it as plain brick with the parapet carried
across.

**Northwest (Taber Place) — not cleanly observed.** The alley elevation, 29.8 m,
six bays. The plan assumes the same pier-and-sash grid on the same rhythm, over
a grey painted base rather than shopfronts, because that is what this building
does on both other long faces and what its type does generally. Loading doors
would be unsurprising on a warehouse's alley face and are the most likely
correction. Marked *inferred*.

**Top — observed, Vexcel 2026 nadir.** A flat light-grey membrane roof with
visible seams running northeast–southwest, covering the full 29.8 x 20.9 m. A
raised penthouse structure sits toward the Taber Place (northwest) half, with a
bright glazed skylight beside it — consistent with the 2017 skylight permit and
the 2018 "existing penthouse on roof". A cluster of mechanical equipment
(several rectangular units and two or three round fans or condensers) is grouped
along the northwest edge near the penthouse. A few small raised boxes sit near
the Second Street parapet. The rest of the roof is empty. A flagpole flying a
US flag stands at the East corner, on the Second Street x South Park parapet; it
is a fixture, not architecture, and 2.10 excludes it.

### 2.5 Recognition cues (ranked)

1. **The corner itself** — two brick elevations of industrial sash turning a
   right angle at the head of the South Park oval. Nothing else at this end of
   the park does that.
2. **The pier-and-sash grid** — the ratio of glass to brick is extreme by
   1920s standards and is what makes the building read as a warehouse rather
   than a loft apartment block. Four bays on Second Street, six on South Park.
3. **The pale banding** — light cast-stone sill and lintel courses crossing the
   red brick at every floor line, plus the parapet coping. From the air this is
   what separates it from the plain-brick neighbours.
4. **Three storeys, flat-topped** — level with its neighbours, not above them,
   with the penthouse the only thing breaking the parapet line.
5. The dark storefront band and the black South Park fire escape.

### 2.6 Miniature translation

**Preserve**

- The 29.8 x 20.9 m footprint and the real 45°/225° heading, exactly
- The corner condition: three public faces and one blind party wall
- The pier-and-spandrel grid as a rhythm — 4 bays northeast, 6 southeast, 6 northwest
- The pale horizontal banding at every floor line; it is the cheapest and
  strongest identity carrier on the model
- The flat roof with its set-back penthouse and grouped mechanical plant

**Simplify / exaggerate**

- The multi-pane steel sash becomes **one recessed glazed panel per bay** with a
  single frame band — no mullion grid. At the app's camera a real 48-pane sash
  is noise; the *size* of the opening is the cue, not its subdivision.
- The window openings may be pushed a little wider and taller than reality so
  the glass-to-brick ratio survives simplification — this is the one place to
  spend semantic exaggeration
- The storefront becomes one dark glazed band per face with two openings broken
  out (the café at the corner, one entry) rather than a shopfitted facade
- The fire escape becomes two solid-sided platforms and one diagonal stair, no
  individual balusters
- Roof clutter becomes a composed set: one penthouse volume, one skylight, one
  tight group of three or four mechanical boxes
- Brick texture becomes flat colour; the brick reads through massing and banding

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not
a straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 rectangle from z=0 to the roof deck z=12.83, `Toy_brick`.
2. Base band, z=0 to z=0.9: `Toy_ink`, carried around the three public faces and
   the party wall.
3. Ground floor, z=0.9 to z=4.30: on the northeast face, four dark storefront
   openings (`Toy_glass` behind a 0.15 m `Toy_ink` frame), the corner one wider
   (the café); on the southeast face, six of the same; on the northwest face,
   two openings and otherwise plain; on the southwest, nothing.
4. Ground-floor cap band: 0.22 m `Toy_stone` course at z=4.30, carried around
   the three public faces.
5. Piers: on each public face, brick piers 1.0 m wide at every bay division and
   1.4 m at each corner, standing proud of the wall plane by 0.12 m from z=4.30
   to the parapet. These are what make the grid read.
6. Second floor, z=4.60 to z=8.55: per bay, one recessed opening 0.18 m deep,
   `Toy_glass`, with a 0.12 m `Toy_steel` frame band. Northeast 4 bays at 5.2 m
   centres, southeast and northwest 6 bays at 4.97 m centres.
7. Spandrel band: 0.30 m `Toy_stone` course at z=8.55, all three public faces.
8. Third floor, z=8.85 to z=12.35: same bay treatment as the second floor.
9. Parapet: brick from z=12.35 to z=13.40, capped by a 0.20 m `Toy_stone` coping
   to z=13.60, carried around all four faces including the party wall.
10. **Roof, z=12.83 to z=12.95** — a thin flat slab, `Toy_roofd`, sitting inside
    the parapet.
11. **Penthouse, z=12.95 to z=17.72** — a 7.0 x 5.0 m volume set back from the
    northwest parapet by ~2.5 m and centred toward the Taber Place half,
    `Toy_brick` walls with a `Toy_roofd` cap and one `Toy_glass` opening. This
    is the crest and must land at exactly 17.72 m.
12. Skylight: one 3.0 x 2.0 x 0.5 m raised monitor, `Toy_glass` on a `Toy_steel`
    kerb, immediately southeast of the penthouse.
13. Mechanical: three boxes (`Toy_steel`, ~1.6 x 1.1 x 0.7 m) and two low
    cylinders (10-segment, 0.9 m diameter) grouped along the northwest edge.
14. Fire escape: on the southeast face near the southwest end, two 2.6 x 1.0 m
    platforms at z=4.6 and z=8.85 with 1.0 m solid side panels and one diagonal
    stair slab between them, `Toy_ink`.
15. Bevel 0.12 m, 2 segments.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_brick` | `c96f4a` | body walls, piers, parapet, penthouse |
| `Toy_stone` | `d9d2c2` | sill/lintel/spandrel bands, ground-floor cap, parapet coping |
| `Toy_glass` | `2a4d73` | industrial sash, storefront glazing, skylight |
| `Toy_steel` | `9aa0a6` | window frame bands, skylight kerb, mechanical plant |
| `Toy_roofd` | `45454a` | roof slab, penthouse cap |
| `Toy_ink` | `3a3530` | base band, storefront frames, fire escape |
| `Toy_glass_Glow` | `6f95b8` | lit office windows at night |
| `Toy_trim_Glow` | `f3efe6` | café storefront spill at the Second Street corner |

`Toy_brick` at `c96f4a` is the palette's brick and matches the observed
red-brown well. Resist darkening it toward `Toy_rust` — the pale banding needs
the contrast, and the toy palette wants the saturated version.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
glazing — the app renders `_Glow` in a separate layer that is ~12% alpha by day,
so a primary surface must never be authored as glow. Hero glow: the café
storefront at the East corner, warm (`Toy_trim_Glow`), wrapping the corner bay on
both street faces — this is the one thing at this end of the park that is
genuinely lit and busy. Supporting accent: five or six lit office windows
scattered over the second and third floors of the two street faces, never a full
row. The Taber Place alley face and the party wall stay dark. The roof does not
glow.

### 2.9 Top surface

29.8 x 20.9 m of flat roof at 12.83 m in a district the camera flies over
constantly, and one of the lower roofs in its immediate neighbourhood — the
camera looks *down* onto this one from Second Street's taller blocks. The
composition problem is that the roof is mostly empty and the penthouse is the
only event: keep the membrane a clear value below the brick, group the
mechanical plant tightly against the northwest parapet so the southeast two
thirds stay clean, and let the penthouse and its skylight sit as one legible
pair. Seams in the membrane are not worth modelling; the parapet's inner face
and the shadow it casts do the work of giving the roof depth.

### 2.10 Scope

**In the GLB:** the single 1923 warehouse block — body, the three glazed
elevations with their piers and bands, the blind southwest party wall, the
parapet and coping, the flat roof, the penthouse, the skylight, the mechanical
cluster and the simplified South Park fire escape

**Not in the GLB:** South Park, its trees or lawn, Second Street, Taber Place,
the sidewalk and its café tables, the bike-share dock, street trees, the utility
pole and overhead wires, the neighbours, vehicles, people, plinths, cameras or
lights

**Deliberately excluded: the roof flagpole.** It is real and it is at the East
corner, but it is a thin fixture roughly 6 m above the parapet. Including it
would make the flagpole tip the bounding-box top, so `targetHeightM` would have
to describe a flagpole rather than the building and the loader would rescale the
whole model against it. At the app's camera the pole is well under a pixel wide.
Record the omission in `REPORT.md`.

### 2.11 Triangle budget

Cap 9,000 — a secondary building, and the cap should bind. Suggested split: body,
parapet, coping and base ~1.2k; the piers on three faces ~1.2k; the sixteen
upper-floor bays ~2.6k; the twelve ground-floor storefront openings ~1.4k; the
horizontal bands ~0.7k; roof slab ~0.2k; penthouse and skylight ~0.5k;
mechanical cluster ~0.6k; fire escape ~0.5k.

Two places this budget can run away. **The bays**: sixteen upper-floor openings
plus twelve storefront openings is twenty-eight recesses, so each must be a
simple inset box with one frame band — a mullion grid inside them will blow the
cap three times over and will not read. **The piers**: twelve of them across
three faces, so keep each a plain proud slab and let the bevel do the softening
rather than modelling a cap or a base.

### 2.12 Draft manifest entry

```json
{
  "id": "2-south-park",
  "file": "2-south-park.glb",
  "anchor": [
    -122.3932364,
    37.7824236
  ],
  "targetHeightM": 17.72,
  "cat": 3,
  "name": "2 South Park",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '2-south-park'`,
  `lon: -122.3932364`, `lat: 37.7824236`, `height: 17.72`, `exclude: 9`) and re-bake
  the affected tiles, or the baked procedural building on this exact footprint will
  intersect the GLB.
- **The anchor is the surveyed parcel's area centroid, not the DataSF LiDAR
  footprint centroid.** This departs from the choice made for 165–167 and 188
  South Park, and the departure is deliberate. Those are party-wall sites on the
  narrow rim of the oval where the exclusion window is a few metres wide and
  centring on the bake input's own ring centroid is the only way to open one.
  This is a corner lot with two streets and an alley around it, the window is
  more than 13 m wide, and inside a window that size the better argument is
  AGENTS rule 5: put the model where the survey says the building is. Measured
  from this anchor, `excluded()` consumes:

  | | trigger distance |
  |---|---|
  | this building's DataSF footprint SF3775005 (via its own centroid) | **2.10 m** |
  | this building's OSM/Overture way 112926339 (via its own centroid) | **2.90 m** — the lower bound |
  | SF3775106 (the southwest party-wall neighbour, nearest ring vertex) | **16.76 m** — the binding constraint |
  | OSM way 112926341 (the same neighbour, nearest vertex) | 17.29 m |
  | SF3775004, nearest ring vertex | 19.35 m |
  | OSM way 112926337 (524 Second Street), nearest vertex | 19.44 m |
  | SF3775048 (across Taber Place), nearest ring vertex | 28.78 m |

  The safe window is **(2.90, 16.76) m**. `exclude: 9` sits near the middle with
  6.10 m of margin below and 7.76 m above — the most comfortable exclusion in
  the South Park series. **Verify with `pipeline/audit.mjs` check 1.6 after the
  re-bake** and confirm visually that the party-wall neighbour on South Park and
  524 Second Street are both still standing before committing.
- Note that both this building's own footprints clear the lower bound by their
  *centroids*, not their vertices (nearest own vertex is 13.5–14.4 m out), which
  is normal: `excluded()` drops a footprint whose centroid *or* any vertex lands
  inside the circle, and a 9 m circle around the middle of a 30 x 21 m building
  catches its centroid comfortably.
- `loadRadius`: the skill's default formula gives `max(2500, 17.72 * 30) = 2500` m.
  Take the default.
- This is the ninth South Park-area building in the landmark manifest and the
  first on the oval's Second Street corner. The same standing question applies as
  for 181 and 188: a manifest of one-off SoMa blocks will not stream well
  forever, and the kit/instancing route (`KIT-INTEGRATION-PROMPT.md`) is the
  better long-term home for buildings of this class. This one has a better claim
  to landmark status than most of the row, being a corner building with three
  public faces and a named history, but the argument is about the row, not about
  this file.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 17.72 m — the penthouse, not a mechanical unit and not a flagpole (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~36 x 36 m is expected)
- [ ] The footprint is still 29.8 x 20.9 m in plan — measure it, do not eyeball it
- [ ] The roof deck sits at 12.83 m and the parapet coping at 13.60 m
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the lit office windows and the corner café; glow shells proud of opaque glazing
- [ ] The southwest party wall has no openings
- [ ] No flagpole in the export
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed
- [ ] The 2.15 penthouse question answered in `REPORT.md`, with the evidence that answered it
- [ ] The Taber Place elevation either observed or, if it stayed inferred, said so plainly in `REPORT.md`

### 2.15 Open questions and risks

- **How much of the 17.72 m LiDAR maximum is penthouse?** The maximum sits 4.89 m
  above a 12.83 m median on a footprint whose height standard deviation is 1.12 m
  — a 4.4σ outlier. `docs/asset-plans/README.md` records two precedents in
  tension: 592 Third Street, where a 6σ maximum was street-tree canopy over the
  parapet, and 370 Brannan, where a maximum just above the median was the real
  crest. This case has evidence the others did not: SF permit 201810163246 (2018)
  moves an elevator machine room into "(e) penthouse on roof", so a penthouse
  demonstrably exists, and the nadir aerial shows a raised structure with a
  skylight beside it in the northwest half of the roof. Against that, a mature
  street tree stands hard against the Second Street facade and rises well above
  the parapet in the May 2025 Street View, and the matching 3.51 m LiDAR
  *minimum* — 8.4σ *below* the median — is the classic signature of exactly that
  kind of edge contamination at the other end of the distribution. The reading
  taken here is a ~4.1 m stair-and-elevator penthouse above a 13.60 m parapet,
  which is a normal overrun for a 1923 freight elevator. **The risk is contained:**
  because the model is authored with the penthouse crest at exactly 17.72 m, the
  loader's scale is 1.0 and an error in this number makes the penthouse too tall
  without making the building too tall. But settle it from imagery if you can.
- **The parapet height is derived, not measured.** 13.60 m comes from the 12.83 m
  LiDAR median (which on a flat roof with a thin parapet ring is the deck) plus a
  conventional 0.77 m parapet, cross-checked against the OSM `height=13` tag. No
  source states it. The 1992 parapet-bracing permit confirms there is one.
- **The Taber Place elevation was not cleanly photographed.** The Street View
  panorama nearest the alley resolves onto a neighbouring facade. The
  pier-and-sash grid assumed in 2.4 is the type's default and matches both other
  long faces, but loading doors on a warehouse's alley elevation would be
  unremarkable and are the most likely correction.
- **The storey count has two outliers.** Two 1992 permits record 2 storeys and
  one 2017 electrical permit records 4; every other permit from 1996 on, and the
  Assessor's roll, say 3. The 1992 pair predate the retrofit and most likely
  describe a tenant space; the 2017 figure is a clerical error on a permit whose
  own reference permit says 3. Three floors at ~4.3 m is the only reading
  consistent with a 12.83 m roof deck.
- **Historic status is unresolved.** The building is a textbook contributor type
  for the SoMa Historic Context Statement, and the National Register South End
  Historic District nomination covers this warehouse class, but that district's
  boundary lies south of Brannan and block 3775 was not confirmed to be inside
  it. No Article 10 landmark designation was found. This affects nothing about
  the model; it is flagged so the next researcher does not repeat the search
  blind. A DPR 523 form, if one exists, would describe the fenestration and
  parapet better than any of the photographs used here.
- **The 2002 awnings are gone.** Permit 200204043134 installed eight canvas
  awnings; none are present in the 2025 imagery. Do not model them.
- **The ground floor changes tenants faster than the model will be rebuilt.**
  Jeremy's department store became Blue Bottle in 2016; several South Park bays
  were papered over and marked for lease in the Jan 2025 capture. Model the
  storefront band as architecture — dark frames, glazed openings, one wider bay
  at the café corner — and do not model signage or tenant fitout.
- **The Assessor still codes this parcel `IND` / Industrial.** It is a stale roll
  code for a 1923 warehouse; the permits record the whole building as retail over
  office since 2016. The manifest entry uses `cat: 3` (office) on that basis, not
  `cat: 20` (warehouse).
