# 434 Brannan Street — SF-SIM asset plan

The 1929 Art Deco concrete industrial loft on the northeast corner of Brannan and
Zoe. Three storeys, full-lot, and — unusually for this corridor — a building with a
designed **crown**: six fluted concrete pilasters divide the Brannan front into five
bays, each bay capped by a salmon-toned frieze of stylised geometric fans, and every
pilaster steps up through the parapet into a plain block so the roofline reads as a
row of teeth from above. Behind that face it is an honest warehouse: a long plain
concrete flank down Zoe Street and a rear third clad in corrugated metal, looking
out over its own parking lot. It is the best-dressed building on the block and the
only one whose top edge is worth modelling for its own sake.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/434-brannan/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `434-brannan` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3954103, 37.7796003` |
| Target height | **13.79 m** to the rooftop mechanical penthouse; parapet crest ~12.40 m and pilaster caps ~12.75 m (both *inferred*); roof deck **11.46 m** (LiDAR, measured) |
| Footprint | 22.70 m (Brannan frontage, SE) x 33.85 m deep; 763.6 m2, measured — a clean parallelogram at the 45 deg SoMa heading |
| Triangle cap | 9,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 434 Brannan Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 434 Brannan Street in San Francisco and
deliver it as a downloadable, validated GLB.

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
7. `artifacts/340-brannan/` and `artifacts/400-brannan/` — the two closest reference
   implementations. 340 Brannan is the right *scale* comparison (a three-storey SoMa
   masonry block at the same 45 deg heading, 17.79 m); 400 Brannan is the right
   *budget and script skeleton* comparison. Adapt one of their build scripts, do not
   rewrite from scratch.
8. `docs/asset-plans/434-brannan.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification. **Read 2.15 before you
   start**: the height above the roof deck is the weakest number here and two
   photogrammetric attempts failed to settle it.

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules.

## Must capture

- A **three-storey flat-roofed concrete box** on a clean 22.70 x 33.85 m parallelogram
  at the 45 deg SoMa heading, filling the front two thirds of its lot
- The Brannan front's **six fluted pilasters dividing five bays**, each pilaster
  stepping up through the parapet into a plain projecting **cap** — this is the
  building's signature and the only thing it has that its neighbours do not
- The **salmon Art Deco frieze** in the five bay heads: stylised geometric fan /
  chevron panels, the one saturated accent on an otherwise neutral building
- Three floors of **wide multi-pane industrial sash** between the pilasters on
  Brannan and down the Zoe flank
- The **corrugated-metal rear**: a blue-grey ribbed rear elevation and a terracotta
  ribbed section at the rear end of the Zoe flank, against concrete everywhere else.
  The front/back split is the truth of the building — do not clad it in concrete all
  round for tidiness
- The recessed **main entry** in the northeast-most Brannan bay
- A designed flat roof: continuous parapet, the pilaster caps reading as teeth from
  above, one rooftop mechanical penthouse toward the rear, a duct run along the
  northeast side, a skylight and a small cluster of units near the Brannan end

## Research 434 Brannan Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world
orientation, and gather references covering:

- The Brannan (southeast) primary elevation, straight on and oblique
- The Zoe Street (southwest) flank, and the bay count on it — the dossier's 6 is
  *inferred* from oblique photography and is the weakest facade number
- The rear (northwest) elevation from the parking lot on Zoe
- Nadir/aerial views for the roof layout and the parapet-cap rhythm
- Night views if any exist

**The known source trap is the height above the roof deck, and it is not resolved.**
DataSF LiDAR gives the roof deck at 11.46 m to better than 0.1 m (mode 11.43, median
11.46, mean 11.36, sd 0.92 over 3,086 cells) and a maximum of 13.79 m. This plan
attributes the 13.79 to the rooftop mechanical penthouse visible in nadir imagery and
sets `targetHeightM` there. Two photogrammetric solves from the Google Street View
panorama (equirect elevation angles, and a rectilinear width/pitch solve) disagreed
with each other by 20% and neither is quotable — see 2.15. **The safe property of
this arrangement is that a mis-attribution is cheap**: the body height comes from the
measured deck, and `targetHeightM` is by definition the export's own top, so the
worst case is a slightly tall penthouse, never a mis-scaled building. Do not let a
new number move the 11.46 m deck without new evidence about the *deck*.

## Create a reference dossier

Write `artifacts/434-brannan/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all
four sides and above; the 3–5 strongest recognition cues; features to preserve;
features to simplify; uncertainties and conflicting evidence. Do not commit
copyrighted full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from
the app's high three-quarter aerial camera, then simplify again.

This is a **secondary building** in the style bible's detail budget (§21). Its one
spent exaggeration is the **crown** — the pilaster caps and the frieze band together.
Thicken the caps and deepen the frieze recess beyond life so the toothed roofline and
the salmon band survive at thumbnail size from the aerial camera. Everything else
(window mullions, the "olivia" lettering, air-conditioners, downpipes, graffiti,
signage) is stripped.

The finished asset must be immediately recognizable as this building, consistent with
the real one from all four sides and above, architecturally credible, and a premium
handcrafted miniature — not photorealistic, not voxel art, not generic low-poly, and
never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single block: body, plinth and base band, both street elevations' bays and
openings, the pilasters and their caps, the frieze band, the corrugated rear and
rear-Zoe sections, the northeast party flank, the parapet, the roof deck and its
furniture.

Do not include unrelated surrounding city geometry: Brannan Street, Zoe Street, the
rear parking lot and its fence, 426 Brannan (the brick "Brick House" building and its
timber patio) next door, power poles, overhead wires, the street tree at the Brannan
kerb, sidewalks, parked cars, people, plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ≈ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project
palette; `_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no
cameras, lights, animations, armatures or constraints; at most 9,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model
drops into the city at its real-world heading — the loader applies no rotation
(`placeGeneric` in `app/src/assets.js` only scales and positions). The **Brannan
elevation faces southeast, bearing 134.8°**; the **Zoe Street flank faces southwest,
bearing 224.8°**; the **rear faces northwest, 314.8°**; the **party flank faces
northeast, 44.8°**. Build directly on the measured footprint polygon in 2.3 rather
than modelling an axis-aligned box and rotating it. Record the measured headings in
`REPORT.md`.

**Height normalization:** the tallest geometry in the export (the rooftop mechanical
penthouse) must land at exactly **13.79 m** so the loader's
`targetHeightM / measuredHeight` scale is 1.0. The roof deck must land at **11.46 m**.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/434-brannan/build_434_brannan.py` (deterministic build script),
`artifacts/434-brannan/434-brannan.blend`, and `artifacts/434-brannan/434-brannan.glb`.
The script must rebuild the model reliably enough for future revision.

## Required review renders

Render the exact final geometry from controlled cameras: `434-brannan-top.png`,
`434-brannan-north.png`, `434-brannan-east.png`, `434-brannan-south.png`,
`434-brannan-west.png`, plus `434-brannan-contact-sheet.png`, at least one high
three-quarter aerial beauty render `434-brannan-aerial.png`, and a night render
`434-brannan-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; the
top view must clearly show the parapet ring, the pilaster caps as teeth, the
penthouse, the duct run and the skylight. Place the aerial camera to the southeast so
it sees the Brannan crown and the Zoe flank together — that pairing is the building.

## Validate the exported GLB

Re-import `434-brannan.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Write `artifacts/434-brannan/validation.json` and
`artifacts/434-brannan/REPORT.md`.

The axis-aligned XY bounding box will be roughly **40 x 40 m** even though the
building is 22.7 x 33.9 m — that is the expected consequence of a 45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this
draft entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "434-brannan",
  "file": "434-brannan.glb",
  "anchor": [
    -122.3954103,
    37.7796003
  ],
  "targetHeightM": 13.79,
  "cat": 3,
  "name": "434 Brannan Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/434-brannan.md`.
````

---

## Part 2 — Research and design dossier

Compiled 18 August 2026 from the sources in 2.2. Values marked *inferred* are visual
or derived estimates, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Address resolution | `434 BRANNAN ST` → parcel **3776151** (block 3776, lot 151) | DataSF EAS address layer (`ramy-di5m`) — **measured** |
| Other addresses on the parcel | none — the parcel's address range is 434–434 | DataSF Parcels (`acdm-wktn`); one EAS record only. Unusually clean for SoMa (cf. 400 Brannan) |
| Built | **1929** | SF Assessor secured roll (`wv5m-vpq2`, all ten years 2008–2024 agree); SF Planning DPR 523A form |
| Style / type | **Art Deco**, reinforced concrete industrial building (`HP8. Industrial Building`) | SF Planning DPR 523A (Page & Turnbull, Eastern Neighborhoods SoMa Survey, recorded 5 June 2009) |
| Storeys | **3** | Assessor roll (`number_of_stories = 3`); DPR ("3-story"); confirmed in street-level photography on both streets |
| Use | Commercial Office (`COMO`), 9 rooms, 0 units | SF Assessor roll — a loft office building; tenants have included Hipmunk, Brightidea, Aurora Solar and Olivia Travel |
| Building floor area | 25,000 sq ft (2,323 m2) | Assessor roll. Over 3 storeys that is 774 m2 per floor — within 1.3% of the LiDAR footprint, i.e. **full-lot-footprint coverage on every floor** |
| Lot | 75 ft x 174 ft (22.86 x 53.04 m), 13,087 sq ft | DPR 523A; Assessor roll; DataSF parcel measures 1,230.1 m2 = 13,241 sq ft (+1.2%) |
| Footprint | **763.6 m2**; 22.70 m (SE, Brannan) x 33.85 m (SW, Zoe) x 22.52 m (NW, rear) x 33.70 m (NE, party) | DataSF building footprints (`ynuv-fyni`, `mblr = SF3776151`), reprojected and reduced to its 4 real corners — **measured** |
| OSM footprint (cross-check) | 788.0 m2 | OSM way/124889482 (`height=11`), which is also Overture's ring — agrees within 3.2%, extending ~4 m further northwest |
| Roof deck height | **11.46 m** above ground | DataSF LiDAR `hgt_median_m`; mode 11.43, mean 11.36, sd 0.92 over 3,086 cells — **measured**, and the tightest number in this dossier |
| LiDAR maximum | **13.79 m** | DataSF LiDAR `hgt_maxcm` — +2.5σ, accepted as the rooftop mechanical penthouse, see 2.15 |
| OSM `height` (cross-check) | 11 | OSM way/124889482 — agrees with the LiDAR *deck*, not with the crest |
| Parapet crest | ~12.40 m; pilaster caps ~12.75 m | ***inferred***, deck + a ~0.95 m parapet. See 2.15 — this is the weakest number here |
| Ground elevation | 5.46–6.24 m (NAVD88), median 5.85 | DataSF LiDAR `gnd_*` — a 0.78 m fall across the footprint; the app's terrain handles this, not the asset |
| Frontage headings | Brannan front faces **134.8°** (SE); Zoe flank **224.8°** (SW); rear **314.8°** (NW); party flank **44.8°** (NE) | measured from the footprint polygon and cross-checked against the DataSF Brannan centreline (CNN 3078000) |
| Which side of Brannan | northwest side (the even numbers) | DataSF street centrelines: CNN 3078000 carries `rt_fadd 422 / rt_toadd 438` — **measured**, not assumed |
| Rear of the lot | a **surface parking lot** occupying the rear ~17.8 m of the parcel ("Ball Park Parking / Public Parking") | DPR 523A ("rear facade facing parking lot"); nadir imagery; Zoe Street photography |
| Nearest neighbour | **426 Brannan St** (parcel 3776015, LiDAR deck 5.75 m) — the red-brick "Brick House" — abuts the northeast flank for 21.9 m of its 33.7 m length, 7.5 m deep | DataSF footprints; the two rings share their party-wall vertices exactly |
| Architect | not recorded in any source consulted | DPR 523A leaves the architect field empty |

### 2.2 Sources

- `https://sfplanninggis.org/docs/DPRForms/3776151.pdf` — **SF Planning DPR 523A/523L form**, Page & Turnbull for the Eastern Neighborhoods SoMa Survey, recorded 5 June 2009. The single best source: it establishes the 1929 date, the Art Deco attribution, the reinforced-concrete construction, the 5-bay pilastered primary facade, the sculpted geometric frieze, the Zoe Street secondary facade, and the corrugated-metal rear. Found via `web_search_advanced_exa("434 Brannan Street San Francisco building")` — it was the top result and the only architectural description in the entire result set.
- `https://data.sfgov.org/resource/ramy-di5m` (DataSF EAS Addresses) — address → parcel 3776151
- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — the 53.1 x 23.0 m parallelogram lot, address range 434–434
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived) — `mblr = SF3776151`, the authoritative footprint and the 11.46 / 13.79 m heights
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor Historical Secured Property Tax Rolls) — 1929, 3 storeys, Commercial Office, 25,000 sq ft
- `https://data.sfgov.org/resource/3psu-pn9h` (DataSF Street Centrelines) — CNN 3078000 (Brannan) and 13795000 (Zoe); the left/right address ranges that put 434 on the northwest side
- `https://www.openstreetmap.org/way/124889482` — cross-check footprint, `height=11`, `name=Olivia Travel`
- Google Street View panorama `o-uPNk1QbRTZseDkFhl8bw` (labelled "434 Brannan St") — the Brannan elevation straight on: pilasters, frieze, sash rhythm, entry, plinth
- Google Street View panoramas `EuNjmfDq-A_70aQ6Y0yBqQ` and `7KpMzggTKz4tObTSkg4EYg` (Zoe Street) — the Zoe flank, the terracotta corrugated rear-Zoe section, and the blue-grey corrugated rear elevation over the parking lot
- Google satellite imagery at z21 (`https://mt1.google.com/vt/lyrs=s&x=&y=&z=21`), stitched and overlaid with the DataSF footprint and parcel rings — the roof: flat light membrane, the pilaster caps reading as teeth on both street parapets, the mechanical penthouse toward the rear, the duct run along the northeast side, a skylight and small units near the Brannan end, and an antenna guy wire running to a ballast pad
- Exa searches also returned the leasing record (16,499 sq ft and 8,664 sq ft floor plates offered separately, a 1999 code-compliance upgrade covering ADA, seismic and life safety) and the DBI permit history (2000: `$750,000` tenant improvement; a `$350,000` job for "window replacement, main entry, (n) entry store front, removal of 2 curb cut") — which is why the Brannan ground floor reads newer than 1929

### 2.3 Orientation and placement

434 Brannan holds the **northeast corner of Brannan and Zoe**. Its southeast elevation
fronts Brannan Street, its southwest flank fronts Zoe Street (a 12 m alley), its
northwest elevation is the rear and faces the parcel's own parking lot, and its
northeast flank is a party wall against 426 Brannan for the 21.9 m nearest Brannan and
then open to the parking lot behind.

The footprint is a clean parallelogram — the four-corner simplification below encloses
763.6 m2 against the survey ring's 764.8 m2 (−0.2%); the discarded vertices are
sub-0.3 m duplicates in the survey. Measured DataSF footprint, in Blender coordinates
(metres, `+X` east, `+Y` north), already centred on the anchor `-122.3954103, 37.7796003`
(the axis-aligned bounding-box centre, which is what the loader's origin convention
needs):

```
( 19.816,  -3.952)   E corner — Brannan front, northeast end (party corner with 426)
(  3.812, -20.052)   S corner — Brannan front, southwest end (the Brannan/Zoe corner)
(-19.816,   4.182)   W corner — rear, Zoe end
( -3.837,  20.052)   N corner — rear, northeast end
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| S→E | 22.70 m | SE 134.8° | **Brannan Street primary facade** — 5 bays, 6 pilasters, frieze |
| W→S | 33.85 m | SW 224.8° | **Zoe Street flank** — concrete for ~25.8 m, corrugated for the rear ~8.0 m |
| N→W | 22.52 m | NW 314.8° | **Rear** — corrugated metal, faces the parking lot |
| E→N | 33.70 m | NE 44.8° | **Party flank** — 426 Brannan (5.75 m) abuts the first 21.9 m; the rest is open |

Because of the 45° heading the axis-aligned bounding box is ~40 x 40 m. That is correct.

The lot runs 53.1 m deep but the building only occupies the front 33.85 m. **Do not
extend the massing to fill the lot** — the rear 17.8 m is asphalt, and the rear
elevation is a real, visible, corrugated-metal facade, not a party wall.

### 2.4 What each side shows

**Southeast (Brannan Street) — the primary facade.** A flat three-storey concrete wall
divided into **five bays by six pilasters**. The pilasters are shallow flat piers with
fine vertical fluting, running from a low light plinth to a plain projecting **cap**
that steps up above the parapet line — so the top of this facade is a row of six blocks
with the parapet field running between them. Each bay head carries a **frieze panel of
stylised Art Deco fans / chevrons in a dusty salmon** on the pale concrete ground; this
is the only colour on the building and the reason it is worth modelling. Floors 2 and 3
each carry a wide multi-pane industrial steel sash window per bay, roughly 8 panes wide
by 4 high, with light frames and dark glazing; a few carry through-wall
air-conditioners. The ground floor is later work (the 1999–2000 permit): shorter window
bands behind light metal grilles in bays 1–4, and in the northeast-most bay a **tall
recessed main entry** with a dark reveal, a glazed leaf door with sidelights, and a
large shallow circular graphic on the reveal wall. Dimensional letters reading
**"olivia"** in dusty pink sit on the spandrel between floors 1 and 2 of the centre bay.
The whole elevation is pale warm grey concrete over a light grey plinth.

**Southwest (Zoe Street) — the secondary facade.** The DPR calls it "clad in concrete
and features industrial windows with pivot mechanism," and that is exactly what it is:
a plain concrete wall with a regular grid of wide industrial sash — three floors of
roughly **6 bays** (*inferred*, ±1) — separated by narrow flat piers, with no pilasters,
no frieze and no cap rhythm except where the parapet's coping continues. A painted
mid-grey dado runs along the base for most of its length, and the ground-floor windows
are larger and fitted with venetian blinds. At the **rear ~8 m of this flank the
concrete stops and terracotta-orange corrugated metal begins**, blank and full height,
over a low orange stucco base — a later rear addition or re-clad. This flank is a real
street elevation, 5.6 m from the Zoe centreline, and it is what the camera sees from
the west.

**Northwest (rear) — corrugated metal.** Blue-grey vertically ribbed metal siding for
the full three storeys, with punched aluminium awning windows in a loose two-by-three
arrangement, some with air-conditioners. It faces the chain-link-fenced surface car
park that fills the rear 17.8 m of the parcel, so it is fully visible from the aerial
camera and from Zoe Street.

**Northeast (party flank).** Plain unfenestrated concrete. 426 Brannan — a two-storey
red-brick building at 5.75 m with a timber restaurant patio in front of it — abuts the
21.9 m of this flank nearest Brannan and is 7.5 m deep, so 434 stands 5.7 m proud above
it there and the rear 11.8 m of the flank is fully exposed to the parking lot. Build it
as a finished, quiet wall plane with floor-line score marks; **do not invent a window
grid**.

**Top.** A flat pale membrane roof inside a continuous parapet. From above the two
street parapets read as **toothed**, because the pilaster caps project above the coping —
six teeth on Brannan and the coping run down Zoe. Toward the rear-centre of the deck
sits a raised **mechanical penthouse**: a light kerbed platform roughly 5 x 4 m carrying
a large dark air-handling unit, with a **duct run** heading southeast from it, parallel
to and about 4.5 m inside the northeast parapet, for some 18 m. Near the Brannan end
there is a **skylight**, a roof hatch and a small cluster of low units. A thin guy wire
runs from the penthouse southwest to a small ballast pad — the wire is not modellable
at this scale, the pad is.

### 2.5 Recognition cues (ranked)

1. **The toothed crown** — six fluted pilasters stepping up through the parapet into
   plain caps. It is the silhouette from the aerial camera and nothing else on this
   block face has it.
2. **The salmon Art Deco frieze** in the five bay heads — the one saturated accent.
3. Three floors of **wide multi-pane industrial sash** in a strict five-bay rhythm.
4. **Concrete front, corrugated-metal back** — the honest warehouse behind the dressed
   face, and the rear elevation standing over its own car park.
5. The corner condition: a short dressed front on Brannan and a long plain flank
   running away down Zoe.

### 2.6 Miniature translation

**Preserve**

- The single-volume parallelogram at the real 45° heading, and the fact that it fills
  only the front two thirds of its lot
- The six pilasters, their caps, and the toothed parapet they produce
- The five-bay rhythm and the frieze band
- The concrete / corrugated split, in both its places (rear elevation, rear-Zoe flank)
- The recessed entry at the northeast end of the Brannan front

**Simplify / exaggerate**

- The pilaster caps are **thickened and given more projection than life** and the frieze
  recess is deepened — the plan's one spent exaggeration, so the crown survives at
  thumbnail size (style bible §8, §21)
- The fluting becomes three shallow grooves per pilaster, not a full reed count
- Industrial sash becomes one recessed dark glazed panel per opening with a light frame
  and a single mullion cross — no 32-pane grids
- The frieze fan ornament becomes one flat salmon panel per bay with two shallow chevron
  grooves, not modelled motif by motif
- Corrugation becomes four or five shallow vertical grooves per panel, never rib by rib
- The "olivia" lettering, air-conditioners, grilles, downpipes, wires and graffiti all
  disappear
- The roof's loose scatter becomes: one penthouse (with its unit), one duct run, one
  skylight, one hatch, three small boxes, one ballast pad

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render. Floor-to-floor is
4.20 / 3.63 / 3.63 m, summing to the measured 11.46 m deck.

1. **Body**: extrude the 2.3 footprint from z=0 to z=11.46 in `Toy_stone`. Its top cap
   is the roof deck.
2. **Cladding split**: on the southwest (Zoe) edge, the 8.05 m nearest the rear, and the
   whole northwest (rear) edge, become separate wall panels — `Toy_rust` on Zoe,
   `Toy_steel` on the rear — each carrying four shallow vertical grooves to imply ribs.
   Concrete elsewhere.
3. **Plinth** (Brannan only): a 0.08 m proud skirt, z=0 to z=0.55, `Toy_trim`.
4. **Base dado** (Zoe concrete portion only): flush band z=0 to z=2.60, `Toy_steel`.
5. **Pilasters** (Brannan): six piers 1.15 m wide, projecting 0.18 m, z=0.55 to z=12.15,
   `Toy_stone`, each with three 0.03 m grooves. Bay openings between them are 3.16 m.
6. **Windows**: openings recessed 0.16 m, `Toy_glass` panes with `Toy_trim` frames and
   one horizontal mullion.
   - Brannan, 5 bays: ground sill 1.35 head 3.60; floor 2 sill 5.10 head 7.35; floor 3
     sill 8.73 head 10.90. Replace the ground-floor opening of the **northeast-most bay**
     with the entry (step 7).
   - Zoe, 6 bays over the concrete portion, openings 3.40 m wide, same three sill/head
     bands.
   - Rear, 6 punched openings 1.30 x 1.50 m in a loose 2 x 3 arrangement.
7. **Main entry** (Brannan, northeast bay): a 3.00 m wide x 4.00 m tall reveal recessed
   0.50 m, `Toy_ink`, with a `Toy_trim` door plane and a 1.6 m flat disc on the reveal's
   back wall in `Toy_stone` (the circular graphic).
8. **Frieze band** (Brannan, between pilasters): five panels z=11.05 to z=12.22,
   recessed 0.09, `Toy_coral`, each with two 0.04 m chevron grooves.
9. **Parapet**: the wall continues from z=11.46 to z=12.22 all round, 0.35 m thick, with
   a `Toy_trim` coping z=12.22 to z=12.40.
10. **Pilaster caps**: six blocks 1.35 x 0.35 m in plan, z=12.15 to z=**12.75**,
    `Toy_trim`, projecting 0.35 m beyond the pilaster face. These are the teeth.
11. **Roof deck** at z=11.46, `Toy_steel` — **not** `Toy_roofd`, which renders
    near-black in the app's lighting. Furniture, in the local coordinates of 2.3:
    - mechanical penthouse platform 5.2 x 4.0 x 0.45 m at (−3.0, +9.8), `Toy_stone`,
      carrying an air-handling unit 3.4 x 2.4 m from z=11.91 to **z=13.79** in
      `Toy_roofd` — **this sets the bounding-box top and must land exactly on 13.79**
    - duct run 0.6 x 0.6 m, 18 m long, from the penthouse southeast along a line 4.5 m
      inside the northeast parapet, z=11.46 to z=12.06, `Toy_steel`
    - skylight 2.2 x 2.2 m at (+9.0, +1.0), `Toy_glass` on a 0.25 m `Toy_trim` kerb
    - roof hatch 1.3 x 1.0 x 0.50 m at (+6.5, −3.0), `Toy_roofd`
    - three small units, 1.6 x 1.2 x 0.8, 1.2 x 1.0 x 0.6 and 0.9 x 0.9 x 1.0 m,
      grouped in the Brannan third, `Toy_steel`
    - ballast pad 1.4 x 1.4 x 0.25 m at (−7.0, −6.0), `Toy_stone`
12. **Bevel** 0.12 m / 2 segments on the chunky solids; 0.05 m / 1 segment on window
    frames, pilaster caps and roof units; none on fills and glow shells.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_stone` | `#d9d2c2` | concrete body, pilasters, parapet, penthouse platform, entry disc |
| `Toy_trim` | `#f3efe6` | plinth, parapet coping, pilaster caps, window frames, skylight kerb, entry door |
| `Toy_coral` | `#e8735a` | the five frieze panels — the single saturated accent |
| `Toy_glass` | `#2a4d73` | all sash glazing and the skylight |
| `Toy_ink` | `#3a3530` | entry reveal |
| `Toy_steel` | `#9aa0a6` | roof deck, rear corrugated cladding, Zoe base dado, duct run, small roof units |
| `Toy_rust` | `#a86444` | the terracotta corrugated section at the rear of the Zoe flank |
| `Toy_roofd` | `#45454a` | the rooftop air-handling unit and the roof hatch only |
| `Toy_coral_Glow` | `#e8735a` | the five frieze panels, uplit at night — hero glow |
| `Toy_glass_Glow` | `#6f95b8` | ~10 lit sash windows scattered across floors 2–3 |
| `Toy_trim_Glow` | `#f3efe6` | the main entry reveal at night |

Two palette notes. The real frieze is a **muted** dusty salmon, not `Toy_coral`'s
saturation; the lift is deliberate semantic exaggeration under style bible §8, and is
the only place it is spent on colour. And the real Zoe dado and rear cladding are
different greys; both collapse to `Toy_steel` so the building reads as two materials
(concrete and metal), not five.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque
surface, never a closed shell around a volume — the app draws `_Glow` as a separate
layer that is ~12% alpha per face by day, so a closed shell reads at ~23% and tints the
facade. Hero glow: the **five frieze panels**, as an uplit crown; their `_Glow` colour
is identical to the opaque `Toy_coral` beneath, so the daytime tint is invisible and the
night look is the frieze's own colour (a `_Glow` material's base colour *is* its night
appearance — do not rely on emission strength). Supporting accents: about ten lit sash
windows (four on Brannan, five on Zoe, one on the rear — a scatter, never a full band)
and the recessed entry. Nothing else glows.

### 2.9 Top surface

764 m2 of flat roof 11.5 m up, in the block of SoMa the camera crosses most often. Two
things must read from directly above: the **toothed parapet** (six caps on Brannan,
coping down Zoe) and the **penthouse-plus-duct** composition in the rear half. Keep the
deck clearly lighter than the roof units so the furniture reads as objects on a surface,
keep the Brannan third of the deck comparatively clean — the real roof is empty there
apart from the skylight cluster — and do not centre the penthouse: it sits toward the
rear and slightly southwest, which is what makes the roof look observed rather than
decorated.

### 2.10 Scope

**In the GLB:** the single block — body, plinth, Zoe dado, both street elevations' bays
and openings, pilasters and caps, frieze band, entry, corrugated rear and rear-Zoe
sections, northeast party flank, parapet and coping, roof deck and roof furniture

**Not in the GLB:** Brannan Street, Zoe Street, the rear parking lot, its fence and its
signage, 426 Brannan and its timber patio, power poles, overhead wires, the street tree,
sidewalks, vehicles, people, plinths, cameras or lights

### 2.11 Triangle budget

Cap 9,000 — a secondary building, but one with two finished street elevations, a
designed crown and a third material on the back. Suggested split: body, parapet, coping
and plinth ~1.2k; six pilasters with fluting and caps ~1.5k; five frieze panels ~0.6k;
Brannan openings (15) ~2.2k; Zoe openings (18) ~2.0k; corrugated panels and rear
openings ~0.8k; entry ~0.2k; roof furniture ~0.7k.

### 2.12 Draft manifest entry

```json
{
  "id": "434-brannan",
  "file": "434-brannan.glb",
  "anchor": [
    -122.3954103,
    37.7796003
  ],
  "targetHeightM": 13.79,
  "cat": 3,
  "name": "434 Brannan Street",
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

- **New landmark (Case B).** No `434-brannan` id exists in
  `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs` or
  `app/src/landmarks.js`. Integration needs a registry entry **and** a re-bake of the
  affected tiles, or the baked procedural building on this exact footprint will
  intersect the GLB.

- **Exclusion radius: 10 m, measured, and the window is narrow on one side only.**
  Measured against the real bake inputs (`pipeline/data/buildings_datasf.geojson` and
  `pipeline/data/overture_buildings.geojsonseq`, both of which trace this building), from
  the anchor above, using the metric `excluded()` actually applies — ring centroid **or**
  any ring vertex:

  ```
  target: DataSF  SF3776151 (763.6 m2, h 11.46)  centroid  4.65 m, nearest vertex 12.45 m
          Overture b9c9690e (788.0 m2, h 11)     centroid  8.11 m, nearest vertex 12.00 m
  nearest NEIGHBOUR — 426 Brannan, both sources:
          DataSF  SF3776015 (163.8 m2, h 5.75)   nearest vertex 12.45 m
          Overture b9c91621 (178.4 m2, h 6)      nearest vertex 12.00 m

  exclude  8 m    -> drops 1  (DataSF only — Overture's copy survives and will fight the GLB)
  exclude  9-12 m -> drops 2  (correct: this building in both sources)
  exclude 12.5 m  -> drops 4  (eats 426 Brannan in both sources)
  ```

  **TWO rings is the correct answer, not one.** The binding constraint below is
  Overture's *centroid* at 8.11 m — not a vertex — because Overture's ring reaches
  4 m further northwest than DataSF's and pulls its centroid off the anchor. The
  binding constraint above is a **shared party-wall vertex**: 426 Brannan's nearest
  vertex is numerically identical to this building's own in both sources, so any radius
  that reaches our corner reaches the neighbour's. The safe band is therefore
  `8.11 < r < 12.00`, and **10 m sits in the middle of it** with 1.9 m of headroom under
  and 2.0 m over. Do not raise past 11.5 or lower under 9 without re-running the
  measurement.

- Registry entry:

  ```js
  {
    id: '434Brannan',
    name: '434 Brannan Street',
    lon: -122.3954103,
    lat: 37.7796003,
    height: 13.79,
    exclude: 10,
    // camera.js apply() puts the eye at pivot + (sin yaw, sin pitch, cos yaw)*distance
    // with +z south, so yaw = 180 - the outward bearing you want to look down. The
    // Brannan front's normal is 134.8 deg true -> yaw 45, which also happens to face
    // the Zoe flank obliquely. yaw 225 would be the mirror image and stare at the
    // parking lot. Verify from a rendered frame, not from the arithmetic.
    camera: { distance: 240, yaw: 45, pitch: 26 },
  },
  ```

- `loadRadius`: the default rule gives `max(2500, 13.79 x 30) = 2500` m. Take the default.
- **Append the manifest entry as text**, not by `JSON.parse`/`JSON.stringify` round-trip —
  re-serialising the manifest rewrites unrelated `targetHeightM` values such as `11.0`
  to `11` across other landmarks and pollutes the diff.
- This is the thirteenth asset in the Brannan family (300, 318, 326, 334, 340, 350, 358,
  362, 370, 380, 400, 414 precede it). **Batch mode applies** — see 2.15. No in-flight
  sibling is within 40 m of this anchor, and neither 426 nor 440 Brannan is planned, so
  there is no exclusion conflict to reconcile.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 13.79 m (loader scale lands at 1.0) and the roof deck at 11.46 m
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~40 x 40 m is expected)
- [ ] Triangles at or under 9,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] Roof deck is **not** `Toy_roofd`
- [ ] `_Glow` only on the frieze panels, ~10 sash windows and the entry; glow shells thin and proud, never closed
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual ≤ 0.15%)
- [ ] Outward direction derived from ring winding, **not** from the footprint centroid
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

1. **Everything above the roof deck is inferred, and two photogrammetric attempts
   failed to settle it.** The deck at 11.46 m is as solid as this dossier gets — mode
   11.43, median 11.46, mean 11.36, sd 0.92 m over 3,086 LiDAR cells, and OSM's
   `height=11` agrees with it. The LiDAR maximum of 13.79 m sits +2.5σ above that, which
   is a moderate outlier rather than the +6σ absurdity that condemned 400 Brannan's and
   592 Third's maxima; `peak_1st_m` (19.68 m) equals `hgt_max` plus ground, so there is
   **no canopy over this roof** (the Brannan street trees are all on the odd side), and
   nadir imagery shows exactly one raised rooftop structure — a kerbed platform with a
   large dark unit — that could produce it. This plan therefore attributes 13.79 m to
   that penthouse and puts the parapet crest at ~12.40 m and the pilaster caps at
   ~12.75 m by architectural inference (deck + ~0.95 m).
   Two independent photogrammetric solves were run against Street View pano
   `o-uPNk1QbRTZseDkFhl8bw` and **neither is quotable**: the equirect elevation-angle
   solve (horizon at row H/2, camera at 2.5 m) returns a wall crest of ~10.6 m, which is
   below the measured deck and therefore wrong; the rectilinear width-and-pitch solve
   returns 12.1–14.5 m depending on which row's facade width is used, and its two rows
   disagree by 20%. The pano's own metadata reports a 0.94° tilt, which is enough to
   move the answer by ~0.4 m and is probably not the whole story. **If you re-attempt
   it, calibrate the horizon against a levelled reference first**, or use the nadir
   shadow-length ratio between the pilaster caps and the penthouse instead, which needs
   no sun angle. What makes this risk survivable is that the mis-attribution is cheap:
   the body is normalised to the *measured* deck and `targetHeightM` is by definition the
   export's own top, so if 13.79 m turns out to be the pilaster caps rather than the
   penthouse, the cost is a penthouse ~1 m too tall — not a mis-scaled building.
2. **The Zoe bay count (6) is inferred** from oblique photography down a 12 m alley; no
   straight-on view of that flank exists in Street View, because the camera cannot get
   far enough back. ±1 bay. Re-count before modelling if any other imagery turns up.
3. **The concrete/corrugated boundary on the Zoe flank is inferred at 8.05 m from the
   rear corner.** It is clearly visible in Street View but its exact position along the
   flank was eyeballed, not measured. The *existence* of the split, and the two
   different metal colours (terracotta on Zoe, blue-grey on the rear), are observed.
4. **The ground floor is not 1929 work.** The DBI permit history carries a
   `$350,000` job for window replacement, a new main entry and storefront, and the
   removal of two curb cuts, and the leasing material describes a 1999 code-compliance
   upgrade. Model the ground floor from current photography, not from what a 1929
   industrial building "should" have, and expect it to keep changing.
5. **The frieze ornament is simplified past the point of literal accuracy.** The real
   panels are stylised fans with layered stepped detail; the plan reduces them to a flat
   panel with two chevron grooves. That is a deliberate call under the detail budget, but
   it is the place where an executing agent with triangles to spare should spend them
   first.
6. **The rear parking lot is not in the asset and must not be.** The parcel is 53.1 m
   deep and the building is 33.85 m; the empty 17.8 m behind it is asphalt that the
   pipeline's ground plane already draws. A modeller who "completes" the lot will produce
   a building 57% too deep.
7. **Batch:** this asset is being built alongside the rest of the Brannan family. Stage 5
   must run in batch mode (source-only branch, bake discarded before committing) or the
   tile re-bakes will collide — `git diff --name-only origin/main` must list nothing
   under `app/public/tiles/` or `api/_data/`.
