# Landmark asset plans

One plan per San Francisco landmark queued for the bespoke-GLB pipeline. Each file
contains **both** halves of the job:

1. **Part 1 — a ready-to-run task prompt.** Copy it into a fresh agent session and
   it will produce a validated GLB, renders, a reference dossier and a report under
   `artifacts/<slug>/`, exactly the way `artifacts/salesforce-tower/` was produced.
2. **Part 2 — the research and design dossier.** Sources, verified facts, the
   WGS84 anchor and architectural height, orientation, four-side and roof
   observations, recognition cues, a massing recipe, a palette map, the triangle
   budget, a draft manifest entry, integration notes and the open risks.

These are plans only. Nothing here has been modelled yet, and no app code,
manifest or pipeline data has been changed.

[**INTEGRATION-PROMPT.md**](./INTEGRATION-PROMPT.md) is the other end of the
pipeline: a reusable, runnable prompt that takes a finished GLB from
`artifacts/<slug>/` into the live scene (re-validation, manifest entry, registry +
re-bake for new landmarks, fallback drill, deployed QA), plus reference notes on how
the loader places assets and what to do when one misbehaves.

Parks are planned separately in [**`../plans/parks/`**](../plans/parks/README.md),
because a park is not a single GLB — it is landcover, terrain drape, tree
placement and paths from the pipeline, with a few hero assets inside it. Those
plans reference the landmark plans here (de Young, Cal Academy, Conservatory,
Painted Ladies, Mission Dolores Basilica, Palace of Fine Arts) rather than
duplicating them.

[**flora-kit.md**](./flora-kit.md) is the one plan here that is not a landmark:
an authored Blender kit of tree species and landscape props to replace the single
procedural lollipop that all 289,741 of the city's baked trees currently share.
It follows the street-furniture kit's architecture rather than the landmark
route, and the park plans depend on it (§E8 of the parks README).

## The set

| Landmark | Manifest id | Target height | Runtime status |
|---|---|---|---|
| [Transamerica Pyramid](./transamerica-pyramid.md) | `transamerica` | 260 m | replaces procedural |
| [Ferry Building](./ferry-building.md) | `ferry-building` | 74.7 m | replaces procedural |
| [Coit Tower](./coit-tower.md) | `coit-tower` | 64 m | replaces procedural |
| [Palace of Fine Arts](./palace-of-fine-arts.md) | `palace-of-fine-arts` | 49.4 m | replaces procedural |
| [San Francisco City Hall](./city-hall.md) | `city-hall` | 93.73 m | replaces procedural |
| [Painted Ladies](./painted-ladies.md) | `painted-ladies` | 12.5 m | replaces procedural |
| [Sutro Tower](./sutro-tower.md) | `sutro-tower` | 297.8 m | replaces procedural |
| [Oracle Park](./oracle-park.md) | `oracle-park` | 45 m | replaces procedural |
| [Grace Cathedral](./grace-cathedral.md) | `grace-cathedral` | 53 m | replaces procedural |
| [Mission Dolores Basilica](./mission-dolores.md) | `mission-dolores` | 30 m | new landmark |
| [Columbus Tower (Sentinel Building)](./columbus-tower.md) | `columbus-tower` | 29 m | new landmark |
| [555 California Street](./555-california.md) | `555-california` | 237 m | new landmark |
| [One Rincon Hill](./one-rincon-hill.md) | `one-rincon-hill` | 195 m | new landmark |
| [Cathedral of Saint Mary of the Assumption](./st-marys-cathedral.md) | `st-marys-cathedral` | 58 m | new landmark |
| [California Academy of Sciences](./cal-academy.md) | `cal-academy` | 11 m | new landmark |
| [de Young Museum](./de-young.md) | `de-young` | 44 m | new landmark |
| [Conservatory of Flowers](./conservatory-of-flowers.md) | `conservatory-of-flowers` | 18.3 m | new landmark |
| [War Memorial Opera House](./war-memorial-opera-house.md) | `opera-house` | 44 m | new landmark |
| [Herbst Theatre (War Memorial Veterans Building)](./herbst-theatre.md) | `herbst-theatre` | ~31 m (estimated) | new landmark |
| [Fairmont San Francisco](./fairmont-san-francisco.md) | `fairmont` | 99 m | new landmark |
| [350 Brannan Street](./350-brannan.md) | `350-brannan` | 13.85 m | new landmark |
| [362 Brannan Street](./362-brannan.md) | `362-brannan` | 8.6 m | new landmark |
| [370 Brannan Street](./370-brannan.md) | `370-brannan` | 7.63 m | new landmark |
| [380 Brannan Street](./380-brannan.md) | `380-brannan` | 12.6 m | new landmark |
| [550 Third Street](./550-third.md) | `550-third` | 11 m | new landmark |
| [375 Alabama Street (Ames Harris Neville Co.)](./375-alabama.md) | `375-alabama` | 22.5 m | new landmark |
| [1008 General Kennedy Avenue](./1008-general-kennedy.md) | `1008-general-kennedy` | 11.9 m | new landmark |
| [Letterman Digital Arts Center](./letterman-digital-arts-center.md) | `letterman` | ~22 m (estimated) | new landmark |
| [Chase Center](./chase-center.md) | `chase-center` | 40.8 m | new landmark |
| [540 Presidio Boulevard](./540-presidio-blvd.md) | `540-presidio-blvd` | 11.5 m (estimated) | new landmark |
| [541 Presidio Boulevard](./541-presidio.md) | `541-presidio` | 10.0 m (LiDAR-derived) | new landmark |
| [542 Presidio Boulevard](./542-presidio-blvd.md) | `542-presidio-blvd` | 10.6 m (estimated) | new landmark |
| [543 Presidio Blvd](./543-presidio-blvd.md) | `543-presidio-blvd` | 9.55 m | new landmark |
| [San Francisco Civic Center Courthouse](./civic-center-courthouse.md) | `civic-center-courthouse` | 29.6 m | new landmark |
| [Bill Graham Civic Auditorium](./bill-graham-civic-auditorium.md) | `bill-graham-civic-auditorium` | 37 m | new landmark |
| [505 Van Ness Avenue (Edmund G. "Pat" Brown Building)](./505-van-ness.md) | `505-van-ness` | 27 m (estimated) | new landmark |
| [Louise M. Davies Symphony Hall](./davies-symphony-hall.md) | `davies-symphony-hall` | 35 m | new landmark |
| [101 Grove Street (Public Health Building)](./101-grove.md) | `101-grove` | 21.4 m | new landmark |
| [Asian Art Museum (Old Main Library)](./asian-art-museum.md) | `asian-art-museum` | 28.1 m | new landmark |
| [171 South Park Street](./171-south-park.md) | `171-south-park` | 12.6 m | new landmark |
| [101 South Park](./101-south-park.md) | `101-south-park` | 10.9 m (estimated) | new landmark |

## Shared contract (all 44)
| [155 – 157 South Park Street](./155-south-park.md) | `155-south-park` | 10.1 m | new landmark |

## Shared contract (all 44)
| [135 South Park](./135-south-park.md) | `135-south-park` | 8.5 m (LiDAR-derived) | new landmark |

## Shared contract (all 44)
## Shared contract (all 44)
| [165–167 South Park](./165-south-park.md) | `165-south-park` | 9.0 m (estimated) | new landmark |

## Shared contract (all 44)
## Shared contract (all 44)

- Style: `docs/styles/miniature-toy.md` (authoritative for artistic decisions)
- Technical contract: `.agents/skills/sf-asset-check/SKILL.md` (authoritative for the GLB)
- Repo rules: `AGENTS.md` — in particular rule 3 (never delete the procedural
  fallback) and rule 5 (real coordinates, real heights; exaggerate in authoring, not
  in placement)
- Reference implementation: `artifacts/salesforce-tower/`
- Binary GLB, real meters, origin at base centre, geometry sitting on z=0, applied
  transforms, flat `Toy_*` colours from the project palette, `_Glow` only for
  night-glow surfaces, no textures, no transparency, no cameras/lights/animation,
  landmark budget <= 27,000 triangles

## Orientation note that applies to every plan

`placeGeneric()` in `app/src/assets.js` scales and positions an asset but never
rotates it, so each GLB must be authored in **true-world orientation** (Blender
`+Y` = north, `+X` = east). The asset contract's "front faces `-Y`" rule can only
be honoured literally for buildings whose real front happens to face south. Where
the two conflict, real-world orientation wins (AGENTS rule 5) and the deviation is
recorded in that asset's `REPORT.md`.

## Runtime status column

- **replaces procedural** — the id already exists in `app/src/landmarks.js` and in
  `pipeline/lib/landmarks.mjs`, so the GLB hides the procedural version on load and
  the existing exclusion zone already clears the baked city. No pipeline change.
- **new landmark** — no procedural builder and no registry entry. Integration needs
  a new entry in `pipeline/lib/landmarks.mjs` (id, lon/lat, height, exclusion
  radius, optional camera preset) **and a re-bake of the affected tiles**, or the
  baked procedural building will intersect the new GLB. Each plan's section 2.13
  spells this out.

## Research method and confidence

Anchors and footprints were measured from OSM geometry pulled directly from the
OSM API (`/api/0.6/way|relation`), reprojected locally, and reduced to a
minimum-area oriented bounding box — those numbers are marked as measured. Heights,
dates, architects and dimensions come from Wikidata claims and Wikipedia infoboxes
with the source named in each row. Anything visual, derived or unconfirmed is
labelled *inferred* or *estimated* and is called out again in each plan's section
2.15. Several OSM `height` tags describe only a low shell (City Hall 30 m, St
Mary's 18.9 m, Cal Academy 11 m, de Young 13 m) and must never be used as the
architectural target height. 550 Third Street is the sharpest case: its OSM
`height=7` and the 2010 city LiDAR agree, and both are wrong, because they
predate the rooftop penthouse that gives the building its crest. Chase Center is
the inverse case — three published figures (structural 31.755 m, OSM 38.1 m,
facade crest 40.84 m) each measure a different thing; see that plan's 2.1. 543
Presidio Blvd is a third variety: its OSM `height=8` is neither eave nor crest but
the LiDAR *median* height over a hipped roof, which by construction falls between
the two — the crest is 9.55 m. The Asian Art Museum is a fourth: its OSM
`height=46` is not a height at all but the NAVD88 roof *elevation* (152.93 ft),
1.6x the real 28.1 m crest — see that plan's 2.3 before trusting any `height` tag
that could plausibly be a sea-level datum. 101 South Park is a fifth variety and the
nastiest so far: its OSM `height=6` and the 2010 LiDAR median (5.56 m) agree with each
other and are both *correct for 2010* — they simply predate the second storey the building
has today, so every published height for that lot is stale rather than mismeasured. Check
the LiDAR's vintage against the permit history before believing a small number.

350 Brannan Street is a different kind of failure: not a wrong height but a missing
*building*. Nominatim resolves the address onto the Brannan Street roadway by TIGER
interpolation, and no footprint on that block is tagged `addr:housenumber=350`. The
resolution runs address -> DataSF parcel APN -> parcel centroid -> the footprint containing
it. When a geocoder returns `osm_type: way` for an address, check whether that way is a
building before believing it.
that could plausibly be a sea-level datum. 135 South Park is the opposite problem — no
`height` tag at all and no photograph of its street elevation anywhere, so its height is
LiDAR-only and its facade is openly a typological reconstruction; that plan's 2.15 leads
with the admission rather than burying it, and its Part 1 tells the executing agent to
read 2.15 before starting.
that could plausibly be a sea-level datum. 362 Brannan Street is a fifth variety and the
most ordinary-looking one: its OSM `height=6` is neither eave nor crest nor datum, it is
simply the *other part of the building* — the one-storey block that covers about four
fifths of the plan — while the crest, on a set-back sloped roof over a two-storey front
bay, is 8.58 m. A tag can be an honest measurement of the wrong feature.

165–167 South Park is the one plan here whose footprint is **not** measured from OSM, and
it is the case that shows why the default has limits. No OSM way carries its address at
all: the building sits inside a Bing trace tagged `167` that is larger than the whole lot
and overlaps its neighbour. That plan's geometry comes from the surveyed DataSF parcel
(`acdm-wktn`), with the DataSF LiDAR footprint (`ynuv-fyni`) supplying only the built depth
— and even those two disagree by 3.7 m, which its 2.3 reconciles. On dense narrow-lot
blocks, prefer the parcel layer and treat OSM as a cross-check.

The executing agent is expected to re-verify height, anchor, footprint and
orientation before modelling — the dossier is a head start, not a citation.

## Night renders: drive `_Glow` from Base Color, not from the imported emission

A review rig that re-imports the exported GLB (which is the required way to
render — always render the file that ships) cannot simply raise
`Emission Strength` on the `_Glow` materials. glTF writes
`emissiveFactor = 0` when the authored emission strength is 0, so a re-imported
`_Glow` material carries a **default white** emission and every glow surface
renders as a white slab. Copy `Base Color` into `Emission Color` and use
strength 1.0 — that is also exactly what the app does, since its night layer is
an unlit overlay drawn at the material's own baked colour. Caught on
`chase-center` (its blue video board rendered pure white);
`tools/glb-optimize/render_ab.py` already does it correctly.
