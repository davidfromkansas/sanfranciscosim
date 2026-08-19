# 501 Second Street — SF-SIM asset plan

A 1925 cream terracotta office block filling the whole east corner of Second and Bryant,
one block northwest of the 524 Second Street warehouse. Seven storeys, a measured 33 m
parapet with a penthouse to 37.7 m, and a 72.8 x 42.2 m footprint — **3,074 m2, the
largest bespoke footprint the SoMa cluster has carried**, five times 524 Second and
eighteen times 358 Brannan.

It is the opposite design problem from every other landmark on these blocks. Those are
low industrial boxes whose identity is proportion or one ornament. This one is a proper
Renaissance-Revival commercial block with a full tripartite composition: a two-storey
base under a bracketed belt cornice, a five-storey shaft of vertical piers, and a
projecting main cornice under a plain parapet — and it is **cream in a district of brick**.
The brief is "the big pale office block on the Bryant corner", and the whole job is
holding that tripartite reading at thumbnail size without spending 40,000 triangles on
window frames.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/501-second/`. This document is the plan only: Part 1 is the runnable task
prompt, Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `501-second` |
| Existing procedural builder | none — new landmark (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3929683, 37.7831785` |
| Target height | **37.7 m** to the penthouse crest; main parapet 33.0 m (measured); cornice 32.2 m; belt cornice 11.6 m |
| Footprint | 72.79 m (Bryant / Federal long axis) x 42.24 m (Second Street frontage); 3,074 m2, measured |
| Triangle cap | 20,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready 501 Second Street GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of 501 Second Street in San Francisco and deliver
it as a downloadable, validated GLB.

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
7. `artifacts/524-second/` — the nearest reference implementation: 78 m away on the other
   side of Second Street, same session, and a build script whose footprint, bay, opening,
   cornice-ring and roof helpers this asset should reuse rather than reinvent
8. `artifacts/500-third/` and `artifacts/574-third/` — the closest precedents for a
   MULTI-STOREY SoMa block rather than a two-storey shed; check their triangle split
   before designing the window rhythm
9. `docs/asset-plans/501-second.md` — this plan, whose dossier is your research
   starting point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract,
`AGENTS.md` governs repository and integration rules. Do not invent a new style
and do not copy visual instructions from unrelated prompts.

## Must capture

- A **big pale block**: 72.79 x 42.24 m, seven storeys, main parapet at a measured
  33.0 m. It is the tallest and by far the largest thing on these blocks and it must
  read that way — do not shrink it toward its neighbours
- The **tripartite composition**, which is the entire identity:
  1. a **two-storey base** of tall openings, ending in a **projecting belt cornice with
     brackets** at 11.6 m,
  2. a **five-storey shaft** of vertical cream piers with recessed spandrels between
     regular dark windows,
  3. a **projecting main cornice** at 31.1–32.2 m under a plain parapet to 33.0 m,
     with an ornamented frieze band immediately below it
- **Cream, not brick.** This is cast stone / terracotta in a district of red brick
  warehouses; the colour contrast against 524 Second, 358 Brannan and the South Park
  cluster is half of why it is recognisable from the air
- **Three public elevations**: Second Street (southwest, 42.24 m — the address),
  Bryant Street (northwest, 72.79 m — the **main entrance**, with the "501 SECOND"
  lettering over a flat canopy), and the southeast flank facing the Federal Street side.
  Only the northeast end is a party wall
- A **roof penthouse** rising to 37.7 m — the crest, and the only silhouette break on a
  building whose parapet is otherwise dead level

## Research 501 Second Street independently

Verify the dossier in this plan rather than trusting it. Re-check at minimum the
architectural height, the footprint, the WGS84 anchor, and the real-world orientation,
and gather references covering:

- All three public elevations. A model built from the Second Street photograph alone
  will have two invented 73 m walls
- Aerial and roof views — the penthouse, the light court, the plant, and whether the
  roof steps
- Ground-level views, day and night
- The storey count, the belt-cornice height and the main-cornice height — the weakest
  numbers in this dossier (see 2.15)
- The architect and the 1985 renovation's scope

Prefer architect/engineer publications, owner or institutional material, planning and
permitting documents, architectural press, geolocated photography, and aerial/satellite
imagery. Never rely on a single photograph, a single AI-generated image, or a single
unsourced 3D model. Separate verified facts from visual inference; if sources disagree,
document the disagreement and decide.

**Three source conflicts are already known and resolved in 2.1 — re-check them, do not
silently re-inherit the wrong value:** the Assessor says **8 storeys and 1985**, every
building permit says **7 storeys**, and the commercial listings say **built 1925,
renovated 1985** — 1925/7 is the building, 1985 is the renovation and the Assessor's
"8" counts the penthouse; the Assessor's 248,888 sq ft and the listings' 207,809 sq ft
differ by the parking and basement; and DataSF LiDAR `hgt_maxcm` **37.66 m is real here**
(unlike at 524 Second, where the equivalent figure was edge bleed) — see 2.15 for why.

## Create a reference dossier

Write `artifacts/501-second/REFERENCE.md` containing: source links and what each
establishes; verified dimensions and location; orientation; observations from all four
sides and above; the 3-5 strongest recognition cues; features to preserve; features to
simplify; uncertainties and conflicting evidence. A contact sheet of attributed
reference thumbnails is welcome if legally permissible — do not commit copyrighted
full-resolution imagery.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22: identify the
recognition cues, strip nonessential information, rebuild the massing from a few
confident volumes, exaggerate only the signature features, simplify the facade into
broad rhythms, deliberately design every surface visible from above, evaluate from the
app's high three-quarter aerial camera, then simplify again.

This is the largest building in the SoMa bespoke set and sits between the style bible's
secondary and hero tiers (§21). Spend the detail on the **three horizontal moves** —
belt cornice, cornice, parapet — and on the vertical pier rhythm. Spend nothing on
individual window muntins, the carved frieze ornament, the lion-head brackets or the
storefront mullions; at city scale they are sub-pixel and they will eat the triangle
budget that the three cornices need.

The finished asset must be immediately recognizable as 501 Second Street, consistent
with the real building from all four sides and above, architecturally credible, and a
premium handcrafted miniature — not photorealistic, not voxel art, not generic
low-poly, and never accurate in one view while invented in the others.

## Scope of the exported asset

Export the single 1925 building: three public elevations, the northeast party wall, all
three cornices, the parapet, the roof and its penthouse and plant.

Do not include unrelated surrounding city geometry: Second Street, Bryant Street,
Federal Street, the neighbours at 533 Second and 355 Bryant, the parking deck on the
southeast side, street trees, the sidewalk, parked cars, people, plinths, cameras or
lights. Temporary context may appear in review renders but must not leak into the GLB.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms;
no negative scales; outward normals; no duplicate or foreign geometry; no image
textures; no transparency; flat-color materials named `Toy_*` from the project palette;
`_Glow` suffix only on surfaces that glow at night; no `Toy_body`; no cameras, lights,
animations, armatures or constraints; no external dependencies; at most 20,000 triangles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real-world heading — the loader applies no rotation (`placeGeneric`
in `app/src/assets.js` only scales and positions). The Second Street front faces
**southwest, bearing 225.4°**; the Bryant Street elevation faces **northwest, 315.4°**;
the Federal side faces **southeast, 135.4°**; the party wall to 533 Second faces
**northeast, 45.4°**. The building is rotated about 45° off the world axes, so build
directly on the measured footprint rectangle in 2.3 rather than modelling an
axis-aligned box and rotating it.

**Height normalization:** the tallest geometry in the export (the penthouse roof) must
land at exactly **37.7 m** so the loader's `targetHeightM / measuredHeight` scale is 1.0.

## Reproducible Blender workflow

Blender 5.2 LTS. Headless: `blender -b --python script.py -- args`.

Keep `artifacts/501-second/build_501_second.py` (deterministic build script),
`artifacts/501-second/501-second.blend`, and `artifacts/501-second/501-second.glb`.
The script must rebuild the model reliably enough for future revision. Do not modify or
rename an unrelated existing GLB to satisfy the task.

## Required review renders

Render the exact final geometry from controlled cameras: `501-second-top.png`,
`501-second-north.png`, `501-second-east.png`, `501-second-south.png`,
`501-second-west.png`, plus `501-second-contact-sheet.png`, at least one high
three-quarter aerial beauty render `501-second-aerial.png`, and a night render
`501-second-aerial-night.png`.

The four elevations must share scale, framing, lighting, exposure and projection; use
orthographic or long-lens cameras; label directions from the researched orientation; the
top view must clearly show the parapet ring, the cornice overhang, the penthouse and the
roof plant; the aerial view uses the style bible's camera assumptions (30-50 degrees
down, long lens), from the **west** so that the Second Street and Bryant Street
elevations are seen together.

Note that the axis-aligned elevation renders will each show the building at 45°. That is
the expected consequence of the real heading, not a camera error.

## Validate the exported GLB

Re-import `501-second.glb` into a fresh isolated Blender scene and validate the
re-import, not the source scene. Report object count, triangle count, dimensions,
bounding-box min/max, min Z, XY center offset, material names, image-texture count,
camera count, light count, animation count, applied-transform status, negative-scale
status, normal-orientation status, unexpected geometry, and per-material contract
compliance. Render at least one review image from the re-imported asset. Write
`artifacts/501-second/validation.json` and `artifacts/501-second/REPORT.md`.

Note that the axis-aligned XY bounding box will be roughly **81.5 x 81.2 m** even though
the building is 72.79 x 42.24 m — that is the expected consequence of a ~45° real-world
heading, not a scale error.

## Manifest draft

Verify the real WGS84 anchor and architectural height yourself, then include this draft
entry in `REPORT.md`. Do not edit the production manifest in this task.

```json
{
  "id": "501-second",
  "file": "501-second.glb",
  "anchor": [
    -122.3929683,
    37.7831785
  ],
  "targetHeightM": 37.7,
  "cat": 3,
  "name": "501 Second Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`, or any app code in this task. Integration is a separate, explicitly requested job — run `docs/asset-plans/INTEGRATION-PROMPT.md` for that, together with the integration notes in `docs/asset-plans/501-second.md`.
````

---

## Part 2 — Research and design dossier

Compiled 16 August 2026 from the sources in 2.2. Values marked *inferred* or *estimated*
are visual or derived, not published figures — the executing agent must re-verify
anything it relies on.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Block / lot | 3774 / 067 | DataSF parcels `acdm-wktn` — `blklot=3774067`, `from_address_num = to_address_num = 501`, `02ND ST`, zoning MUO |
| Built | **1925**, renovated 1985 | commercial listings; the Assessor's `year_property_built = 1985` is the renovation (its record also reads 8 storeys against the permits' 7 — see 2.15) |
| Storeys | **7** | every SF building permit 2010-2026 records `number_of_existing_stories = 7`; listings agree |
| Use | Office (Class B) | SF Assessor `Office`; permits `existing_use = office`; a heavily tenanted multi-tenant building |
| Building area | 248,888 sq ft (Assessor) / 207,809 sq ft rentable (listings) | the gap is parking + basement + common area |
| Typical floor | 29,687 sq ft = 2,758 m2 | listings; against a 3,074 m2 footprint this implies light courts, which the aerial confirms |
| Footprint | 3,074 m2; **72.79 m x 42.24 m**, 99.8% rectangular fill | OSM way 112758588 OBB — **measured**; DataSF LiDAR `SF3774067` independently gives 72.67 x 42.39 m and 3,107 m2, a 1% agreement |
| Main roof height | **33.0 m** | DataSF LiDAR `hgt_majoritycm 3326` (the modal roof plane) and `hgt_mediancm 3272`, over 12,467 cells; OSM `height=33` agrees independently — **measured** |
| Penthouse crest | **37.66 m** | DataSF LiDAR `hgt_maxcm` — **measured**, and real here (see 2.15) |
| Ground elevation | 13.75 m (NAVD88) | DataSF LiDAR `gnd_min_m` — app terrain handles this, not the asset |
| Corner condition | Second Street (SW) x Bryant Street (NW); Federal Street side (SE); party wall to 533 Second (NE) | OSM ways; the 2nd x Bryant intersection node is at `-122.39362, 37.7830916`, 58 m west-southwest of the anchor |
| Frontage headings | Second St 225.4° (SW); Bryant St 315.4° (NW); Federal side 135.4° (SE); party wall 45.4° (NE) | measured from the footprint OBB |
| Main entrance | on **Bryant Street**, under a flat canopy carrying "501 SECOND" | Street View, April 2025 |
| Current occupants | GoodRx, LangChain, atSpoke, Square 1 Bank, IDG, WRNS Studio, Stride Health, ChargePoint, Axia by Qcells | Google Maps "at this place"; a full multi-tenant floorplate |

### 2.2 Sources

- `https://data.sfgov.org/resource/acdm-wktn` (DataSF Parcels) — the address-to-lot link,
  `3774067 = 501 02ND ST`, MUO zoning
- `https://data.sfgov.org/resource/ynuv-fyni` (DataSF Building Footprints, LiDAR-derived)
  — polygon `SF3774067`: 72.67 x 42.39 m, `hgt_median 32.72`, `hgt_majority 33.26`,
  `hgt_mean 29.53`, `hgt_std 6.41`, `hgt_max 37.66`, 12,467 cells, ground 13.75 m
- `https://data.sfgov.org/resource/wv5m-vpq2` (SF Assessor) — Office, 248,888 sq ft;
  `year_property_built 1985` and `number_of_stories 8` (both reconciled in 2.15)
- `https://data.sfgov.org/resource/i98e-djp9` (SF Building Permits) — 100+ permits,
  every one `number_of_existing_stories = 7`, `existing_use = office`; the volume of
  suite-level tenant-improvement work is itself evidence of a large multi-tenant floorplate
- https://www.openstreetmap.org/way/112758588 — `addr:housenumber=501`,
  `addr:street=2nd Street`, `addr:postcode=94107`, `building=yes`, **`height=33`**
- LoopNet listing "501 2nd St" — 7 storeys, 207,809 SF, typical floor 29,687 SF, Class B,
  built 1925, renovated 1985
- Google Street View, Second x Bryant corner pano (capture **Jan 2025**) — the tripartite
  composition, the cream cast-stone facade, the dark-framed steel sash, the corner
- Google Street View, Bryant Street pano (capture **April 2025**) — the main entrance,
  the "501 SECOND" lettering, the bracketed belt cornice, the frieze band, the pier rhythm
- Google Street View, Second Street pano (capture **May 2025**) — the address elevation
- Google Maps satellite (Vexcel imagery, 2026) — the roof: penthouse, light court,
  plant, and the parking deck on the southeast side

### 2.3 Orientation and placement

The building fills the east corner of Second and Bryant and runs 72.8 m back toward
Federal Street. It is rotated about 45.4° from the world axes, like the whole SoMa grid.

OSM and DataSF LiDAR agree to 1% on the footprint here — unlike at 524 Second, where
three sources disagreed by 12%. The OSM OBB is used.

Footprint rectangle, in Blender coordinates (metres, `+X` east, `+Y` north),
counter-clockwise, already centred on the anchor `-122.3929683, 37.7831785`:

```
(-40.74, -10.51)   west corner   — Second x Bryant
(-11.10, -40.59)   south corner
( 40.74,  10.51)   east corner
( 11.10,  40.59)   north corner
```

Edges, with outward normals:

| Edge | Length | Faces | Elevation |
|---|---|---|---|
| `(-40.74,-10.51) -> (-11.10,-40.59)` | 42.24 m | SW 225.4° | **Second Street** (the address) |
| `(-11.10,-40.59) -> (40.74,10.51)` | 72.79 m | SE 135.4° | Federal Street side |
| `(40.74,10.51) -> (11.10,40.59)` | 42.24 m | NE 45.4° | party wall to 533 Second Street |
| `(11.10,40.59) -> (-40.74,-10.51)` | 72.79 m | NW 315.4° | **Bryant Street** (the main entrance) |

Because of the 45.4° heading the axis-aligned bounding box is ~81.5 x 81.2 m for a
building that is 72.79 x 42.24 m. That is correct.

### 2.4 What each side shows

**Southwest — Second Street (the address, 42.24 m).** The short elevation, and the one
the street number belongs to. Same tripartite system as Bryant at a narrower rhythm:
a two-storey base of tall dark openings; the bracketed belt cornice; five storeys of
cream piers with dark windows between them; the frieze and main cornice; the parapet.
No entrance of consequence — the door is round the corner.

**Northwest — Bryant Street (the main entrance, 72.79 m).** The hero elevation and the
longest. Cream cast stone throughout. Ground floor: tall openings, a **recessed main
entrance under a flat canopy** carrying "501 SECOND" in metal letters, a second recessed
service bay beside it, and small carved brackets at the cornice springing. At 11.6 m a
**projecting belt cornice on modillion brackets** separates base from shaft. Above it,
five storeys of flat cream piers with slightly recessed spandrels and dark steel-sash
windows in a strict grid. Below the main cornice, a **carved frieze band** of repeating
ornament. The main cornice projects hard at 31.1–32.2 m, and a plain parapet runs to
33.0 m.

**Southeast — Federal Street side (72.79 m).** A real elevation but a plainer one: the
same bay rhythm and the same cornices, without the entrance and with less ornament. It
faces a parking deck, so it is seen obliquely from the street and fully from the air.

**Northeast (42.24 m).** Party wall to 533 Second Street. Blind cream stucco. Do not
invent windows.

**Top.** 3,074 m2 of roof at 33.0 m — the biggest roof in the bespoke SoMa set and the
surface the app's camera spends the most pixels on. The Vexcel aerial shows a pale
membrane inside the parapet ring, a **light court** cut into the middle (which is what
reconciles a 3,074 m2 footprint with a 2,758 m2 typical floor), a **penthouse** rising to
37.7 m toward the Second Street end, and scattered mechanical plant. Design it: at this
size a blank tray is the single most visible failure available.

### 2.5 Recognition cues (ranked)

1. **Size.** 72.8 x 42.2 m at 33 m — nothing else on these blocks is close. If it does
   not dominate its corner, nothing else matters
2. **Cream in a brick district.** The pale cast-stone mass against 524 Second's red brick
   78 m away, and against the whole South Park cluster
3. **The tripartite composition** — base, shaft, cornice — read as three horizontal moves
   at distance
4. **The two projecting cornices**, which are what make those moves legible from above
5. The penthouse breaking an otherwise dead-level parapet

### 2.6 Miniature translation

**Preserve**

- The 72.79 x 42.24 m proportion, the 33.0 m parapet and the real 45.4° heading, exactly
- The three horizontal moves and both cornice projections — exaggerate the projections
  rather than lose them
- The vertical pier rhythm on all three public elevations
- Cream. Never brick, never grey
- The penthouse as the crest

**Simplify / exaggerate**

- Both cornices are thickened and their projection increased so they survive at distance.
  This is where the semantic exaggeration is spent
- ~30 panes per steel sash become one glazed panel per opening in a light frame
- The carved frieze becomes one recessed band; the modillion brackets become a single
  continuous soffit; the lion-head ornaments are dropped
- The entrance canopy is kept (it carries the night glow); the "501 SECOND" lettering is
  a glowing strip, not modelled letters
- Storefront mullions, downpipes, fire escapes, conduit, the banner brackets and the
  street trees are dropped
- Roof clutter becomes the penthouse, the light court, three plant blocks and two vents

### 2.7 Massing recipe

Build order for the deterministic script; dimensions are the starting point, not a
straitjacket — adjust after the first aerial review render.

1. Body: extrude the 2.3 rectangle from z=0 to z=33.0 (`Toy_cream` walls), cap
   `Toy_sand` — the roof membrane. (`Toy_sand` and not `Toy_steel`: see 2.8.)
2. Base band: 0.10 m proud panel on the three public faces, z=0 to z=11.6, `Toy_cream`
   with a slightly deeper reveal, so the base reads as a distinct storey group.
3. **Belt cornice**: ring on the three public faces, z=11.6 to z=12.25, projecting 0.55 m,
   `Toy_stone` — the first of the three horizontal moves.
4. Shaft piers: on each public face, one 0.9 m `Toy_cream` pier per bay boundary,
   z=12.25 to z=31.1, projecting 0.12 m.
5. Openings, base: one per bay, z=1.4 to z=10.6, `Toy_glass` in `Toy_stone` frames.
6. Openings, shaft: one per bay per floor at 11.6 + k*3.90 (k = 0..4), each 2.5 m tall,
   `Toy_glass` in `Toy_stone` frames.
7. Frieze band: recessed `Toy_cream` band z=29.9 to z=31.1 on the three public faces.
8. **Main cornice**: ring on all four faces, z=31.1 to z=32.2, projecting 0.85 m,
   `Toy_stone`.
9. Parapet: ring, z=32.2 to z=33.0, 0.4 m thick, `Toy_cream` with a `Toy_stone` coping.
10. Bryant entrance: a recessed `Toy_ink` opening 4.6 m wide, z=0 to z=5.2, under a flat
    `Toy_stone` canopy at z=5.2 to z=5.6 projecting 1.6 m, with a `Toy_gold_Glow` sign
    strip on its fascia — the night hero.
11. **Penthouse**: 16 x 11 m block toward the Second Street end, z=33.0 to **z=37.7**,
    `Toy_cream` with a `Toy_sand` cap — this sets the bounding-box top and must land
    exactly on 37.7.
12. **Light court**: a 14 x 9 m well cut into the roof toward the Federal side, floor at
    z=26.0, `Toy_sand` — modelled as a recessed box, not a boolean.
13. Roof plant: three `Toy_steel` blocks (max 1.8 m tall), two `Toy_roofd` vents, one
    hatch. Nothing may out-top the penthouse.
14. Bevel 0.10 m, 2 segments on the masses; 0.04/1 on applied panels and cornices.

### 2.8 Materials and palette

Flat colors only, from the `sf-asset-check` palette.

| Material | Hex | Used for |
|---|---|---|
| `Toy_cream` | `#f2ede3` | the whole cast-stone mass, piers, base, parapet, penthouse — **the identity colour** |
| `Toy_stone` | `#d9d2c2` | both cornices, the parapet coping, window frames, the entrance canopy |
| `Toy_sand` | `#ece4d4` | the roof membrane and the light-court floor |
| `Toy_glass` | `#2a4d73` | all windows |
| `Toy_glassl` | `#6f95b8` | penthouse glazing |
| `Toy_roofd` | `#45454a` | roof vents, hatch |
| `Toy_steel` | `#9aa0a6` | rooftop plant blocks |
| `Toy_ink` | `#3a3530` | the recessed entrance and service bay |
| `Toy_glass_Glow` | `#6f95b8` | lit windows at night |
| `Toy_gold_Glow` | `#caa64a` | the "501 SECOND" canopy sign strip — the night hero |

**Roof membrane note.** `Toy_sand`, not `Toy_steel`. This was settled empirically on
`524-second` in the same session: `Toy_roofd` was rejected at authoring time on
`358-brannan`'s recorded lesson, `Toy_steel` shipped, and then the live scene measured its
lit deck at (90, 98, 107) against (146, 133, 104) on the baked neighbours — 27% darker,
the darkest roof on the block. This roof is three times bigger. Start pale.

**Night state (required).** Glow surfaces must be thin shells proud of the opaque surface
behind them — the app renders `_Glow` in a separate layer that is ~12% alpha by day, so a
primary surface must never be authored as glow. Hero glow: the **entrance canopy's sign
strip** in `Toy_gold_Glow`. Supporting: lit windows in `Toy_glass_Glow` scattered across
the shaft — this is a full multi-tenant office building, so a *scatter* across several
floors is the truthful pattern, not a uniform grid and not a single lit floor. Keep it
under about a fifth of the openings; a nine-tenths-lit block reads as a render, not a
building.

### 2.9 Top surface

3,074 m2 — the largest roof in the bespoke SoMa set, and the reason this asset cannot be
judged from the street. The composition is: the parapet ring and the main cornice
overhang framing the whole thing; the **light court** as the one strong negative shape;
the **penthouse** as the one positive one, placed toward the Second Street end so the
corner reads as the tall end; and the plant grouped against the northeast party wall so
the middle stays open. Keep the membrane pale (2.8) and the plant dark, so the roof reads
as a designed plane with objects on it rather than a grey field.

### 2.10 Scope

**In the GLB:** the single 1925 building — body, base, both cornices, parapet, the pier
and window rhythm on three public elevations, the blind northeast party wall, the Bryant
entrance and canopy, the roof, the penthouse, the light court and the plant

**Not in the GLB:** Second Street, Bryant Street, Federal Street, 533 Second, 355 Bryant,
the southeast parking deck, street trees, sidewalk, vehicles, people, plinths, cameras
or lights

### 2.11 Triangle budget

Cap 20,000 — the largest in the SoMa set, and justified by 190 m of public elevation over
seven storeys. Suggested split: body, base, parapet and both cornices ~3.0k; piers ~2.0k;
base openings ~1.8k; shaft openings ~9.5k; entrance and canopy ~0.7k; penthouse, light
court and plant ~2.0k. **The shaft openings are the risk.** 26 bays x 5 floors is 130
openings before the base; if the first build lands over budget, cut bays before cutting
cornices — the cornices are the identity and the windows are texture.

### 2.12 Draft manifest entry

```json
{
  "id": "501-second",
  "file": "501-second.glb",
  "anchor": [
    -122.3929683,
    37.7831785
  ],
  "targetHeightM": 37.7,
  "cat": 3,
  "name": "501 Second Street",
  "estimated": false,
  "dims": [
    x, y, z
  ],
  "tris": N,
  "loadRadius": 2500
}
```

`dims` and `tris` are placeholders until the asset is built and validated.
`"estimated": false` because both the 33.0 m parapet and the 37.7 m crest are LiDAR
measurements corroborated by the OSM height tag — unusually, nothing here is
photogrammetric.

### 2.13 Integration notes (for later, not this task)

- **New landmark.** Add a `pipeline/lib/landmarks.mjs` entry (`id: '501Second'`) and
  re-bake the affected tiles, or the baked procedural building on this footprint will
  intersect the GLB.
- **Exclusion radius.** Size it from the bake input's ring **vertices**, not centroids,
  and measure it against the real `pipeline/data/overture_buildings.geojsonseq`. The
  footprint half-diagonal is 42.1 m, and the nearest neighbour parcel centroids sit
  50-66 m out, so the safe window here is unusually generous compared with 524 Second's
  (2.9, 14.78) m. Do the measurement anyway; the party wall to 533 Second is the risk
  edge, and vertices are what fire the test.
- `loadRadius`: the default formula gives `max(2500, 37.7 * 30) = 2500` m. Take the
  default.
- **Judge it against `524-second`**, 78 m away and built in the same batch. They are
  deliberate opposites — a 9.9 m red brick shed and a 37.7 m cream office block — and if
  the pair does not read that way from the aerial, the tripartite composition on this one
  has collapsed into a plain box.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import of the exported GLB (never validate the authoring scene)
- [ ] `min Z` within 0.5 m of 0, XY center offset within ~1 m
- [ ] Bounding-box top exactly 37.7 m (loader scale lands at 1.0)
- [ ] Dimensions plausible in meters and consistent with 2.1 (XY bbox ~81.5 x 81.2 m is expected)
- [ ] Footprint proportion preserved: the building must measure 72.79 x 42.24 m along its own axes
- [ ] Main parapet lands at 33.0 m; both cornices project and read from directly above
- [ ] Triangles at or under 20,000
- [ ] Materials all `Toy_*`, flat, no textures, no alpha, no `Toy_body`
- [ ] `_Glow` only on the canopy sign strip and the scattered lit windows; glow shells proud of the opaque surface
- [ ] No cameras, lights, animations, armatures, constraints
- [ ] Applied transforms, no negative scales, outward normals (per-object signed volume for the union of solids; ray test residual <= 0.15%)
- [ ] No foreign/leaked geometry from other Blender scenes
- [ ] Six review renders + contact sheet + night render regenerated from the final export
- [ ] `REFERENCE.md`, `REPORT.md`, `validation.json` committed

### 2.15 Open questions and risks

- **The Assessor says 8 storeys and 1985; every permit says 7.** Both are true of the
  same building: the listings give "built 1925, renovated 1985", the Assessor's
  `year_property_built` records the renovation, and its storey count includes the
  penthouse that the LiDAR maximum also sees. **7 occupied storeys plus a penthouse** is
  the reading used here. An agent that builds 8 full floors will get the floor-to-floor
  height wrong by 0.6 m on every level.
- **`hgt_maxcm` = 37.66 m is real here, and that is the opposite call from 524 Second.**
  At 524 the equivalent figure was edge bleed: a 13.32 m maximum against a 0.95 m standard
  deviation on a small roof beside a 19.7 m neighbour. Here the standard deviation is
  **6.41 m** over 12,467 cells with a modal plane at 33.26 m, the aerial shows a distinct
  raised block on the roof, and the nearest taller neighbour is 60 m away — far outside
  bleed range. Model the penthouse.
- **The light court is inferred from arithmetic plus imagery.** A 3,074 m2 footprint
  against a 2,758 m2 typical floor leaves 316 m2 unaccounted for, and the Vexcel aerial
  shows a rectangular notch in the roof. Its exact size and position are *estimated*.
- **The bay counts are inferred.** 6 bays on Second Street and 10 each on Bryant and the
  Federal side are read from obliquely-shot panoramas partly occluded by street trees and
  power poles. Verify from a square-on photograph before committing; this is the most
  likely place for the model to be visibly wrong.
- **The belt cornice at 11.6 m and the main cornice at 31.1 m are photogrammetric**,
  derived by dividing the measured 33.0 m parapet across a 2 + 5 storey split. Only the
  parapet and the crest are measured.
- **No architect is recorded** for the 1925 building in any source consulted, and the
  scope of the 1985 renovation is unknown — in particular whether the ground-floor
  openings are original.
- The southeast elevation's detail level is a judgement call: it is a real public
  elevation but faces a parking deck. It is given the same rhythm and cornices with less
  ornament. If the triangle budget binds, this is the face to simplify first.
