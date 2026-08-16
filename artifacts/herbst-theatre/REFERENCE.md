# Herbst Theatre / War Memorial Veterans Building — reference dossier

Compiled 2026-08-12 for the SF-SIM miniature asset. Facts verified independently of
the plan doc (`docs/asset-plans/herbst-theatre.md`); corrections to the plan are
called out explicitly at the end.

**Which building this is.** 401 Van Ness Avenue, the *northern* half of the War
Memorial pair, OSM `way/32865757` (`name=War Memorial Veterans Building Herbst
Theatre`, `alt_name=Herbst Theatre`, `wikidata=Q5736243`). The Opera House —
already modelled in `artifacts/war-memorial-opera-house/` — is `way/32865161` at
301 Van Ness, *south* of the memorial court, and has a fly tower. This one does
not. Both were checked against the same Overpass pull this session.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM `way/32865757` (Overpass, checked 2026-08-12; tag `check_date=2026-02-23`) | Footprint polygon (37 nodes), `height=28`, `ele=22`, `building=civic`, `amenity=theatre`, address 401 Van Ness Avenue, `wikidata=Q5736243` |
| OSM `way/32865161` (same pull) | The Opera House twin, for the pair geometry and the shared grid bearing |
| [Wikipedia — SF War Memorial and Performing Arts Center](https://en.wikipedia.org/wiki/San_Francisco_War_Memorial_and_Performing_Arts_Center) | Arthur Brown Jr., designed 1927–28, both buildings completed and opened 1932; "one of the last Beaux-Arts style structures erected in the United States"; 7.5-acre site; "a matched pair of buildings across a formal courtyard park"; **"identical exteriors"**; Herbst Theatre 916 seats, originally the Veterans Auditorium, renamed 1977; UN Charter signed here 26 June 1945 |
| [noehill — SF Landmark #84, War Memorial Complex](https://noehill.com/sf/landmarks/sf084.asp) | The designation language: **"two substantially identical structures, the Opera House and the Veterans Building, separated by a formal court"**; conceived to complement City Hall; architects Arthur Brown Jr. and G. Albert Lansburgh |
| [SGH — Veterans Building rehabilitation](https://www.sgh.com/project/san-francisco-war-memorial-veterans-building/) | Steel frame with **terra-cotta-clad** concrete infill walls; **granite base**; terra-cotta and steel-framed windows; **terra-cotta balustrades**; **metal roof with skylights** (both replaced 2013–16); the second-floor Green Room "opening to a **loggia facing City Hall**" — i.e. an open east-facing loggia behind the Van Ness colonnade; 916-seat Herbst Theatre |
| [SF Public Works — Veterans Building seismic upgrade](http://sfpublicworks.org/veteransbuilding) | Dedicated Armistice Day, 11 November 1932; designed by Arthur Brown Jr.; 1989 Loma Prieta damage; 2013–16 seismic upgrade, $96.5 M city budget |
| `artifacts/war-memorial-opera-house/REFERENCE.md`, `REPORT.md`, `build_*.py` (this repo) | The twin's verified facade scheme, height ladder and material set. Because the designation calls the two buildings substantially identical, this is a primary source for this asset, not a convenience. |

The 1978 National Register nomination for the Civic Center Historic District
(`npgallery.nps.gov/NRHP/GetAsset/NRHP/78000757_text`) was retrieved but is a
scanned PDF with no extractable text; no bay-count evidence could be read from it.
No published elevation or section drawing was found for this building.

## Verified dimensions and location

- **Footprint:** oriented bounding box **67.38 m (N–S, the Van Ness frontage) ×
  83.06 m (E–W, front to Franklin St)**; polygon area 4,437 m² (78.6% fill —
  the rear is notched). Measured from the 37-node OSM way, reprojected with the
  repo's local tangent projection.
- **Orientation:** long edges bear **81.11° cw from true north** (length-weighted
  dominant edge angle over all 37 edges; the Opera House twin measures the same,
  as do Grace Cathedral 81.03° and 555 California 81.23° — the Civic Center grid).
  The colonnade front faces **east** onto Van Ness Avenue.
- **Anchor:** oriented-bbox centre of the footprint = **−122.4210354, 37.7795452**.
  The shipped anchor is recomputed from the exported model's own bbox centre
  (`REPORT.md`) because `placeGeneric` puts the exported bbox CENTRE on the
  anchor and the model carries its own front steps.
- **Heights:** OSM `height=28` — see below. Architectural top **31.0 m**,
  *inferred*. `ele=22` is ground elevation, not a building dimension.

### The height, in detail

AGENTS rule 5 and the pipeline's iron rule forbid adopting an OSM `height` tag as
the architectural target where it describes a low shell. The chain here is:

1. The Opera House's `height=44` is its **fly tower**, not its cornice.
2. The Opera House dossier derived its own *main-block parapet ≈ 28 m* from
   **this building's** `height=28`, on the grounds that the two read identical to
   the cornice in photographs. So 28 m is a parapet figure on both twins, and the
   Opera House GLB was built with its cornice at 24.5 m and its front attic
   parapet at 27.0 m on that basis.
3. This building has no fly tower, so its summit is the ridge of the hipped metal
   roof (SGH) set back behind that parapet.
4. The Opera House's front-block hip — the same element on the same cornice line —
   peaks at **31.0 m**.

Adopting **31.0 m** therefore makes the pair share a base course (9.5 m), a
cornice line (24.5 m), a front attic parapet (27.0 m) and a roof ridge height,
which is what "substantially identical structures" means, while leaving the
silhouette difference (fly tower vs none) as the real distinguishing cue. Shipped
as `"estimated": true`. If a published elevation surfaces, this is the first
number to correct.

## Footprint decomposition (37-node polygon; u = metres back/west from the Van Ness front plane, v = metres north from the south edge, frontage 67.38 m)

| Zone | u range | Width | v range |
|---|---|---|---|
| Front pavilion (colonnade block) | 0 → −3.1 | **45.49 m** | 10.98 → 56.47 |
| Shoulder step | −3.1 → −4.3 | 51.15 m | 8.26 → 59.41 |
| Shoulder step | −4.3 → −7.0 | 53.27 m | 7.14 → 60.41 |
| Wings (full frontage) | −7.4 → −20.1 | **67.38 m** | 0 → 67.38 |
| Main block | −22.6 → −78.5 | **51.4 m** | 7.8 → 59.3 |
| Rear block (Franklin St) | −78.5 → −83.06 | **41.15 m** | 12.86 → 54.01 |

Every zone is centred on the frontage axis to within 0.3 m, so the model is built
symmetric about v = 0. This is the same four-part scheme as the Opera House
(narrow front pavilion → full-width wings → narrower main block → narrower rear
block) at ~92% of the twin's N–S dimensions and 80% of its depth — a further
independent confirmation of the "identical structures" claim, arrived at from
geometry rather than text.

## What each side shows

**East (Van Ness front)** — the hero elevation, and by the designation the same
elevation as the Opera House: rusticated granite basement with round-arched
glazed openings; above a balustraded course, the giant-order Doric colonnade of
paired columns screening an **open loggia** (the Green Room loggia, confirmed by
SGH as facing City Hall); full entablature, dentiled cornice, low attic parapet.
Rusticated full-height corner pavilions at each end with blind arched niches.

**South (memorial-court flank)** — the formal flank, facing the court and the
Opera House across it. Arched windows in a regular rhythm, the same cornice line,
court-facing skylights in the hipped roof. This is the elevation the app's camera
sees when it frames the pair.

**North (McAllister St flank)** — the working flank: the same window rhythm plus
service doors and a slim canopy in the base course; no court skylights.

**West (Franklin St rear)** — a plainer end block (41 m wide) with a regular
small-window grid, a service entrance and a parapet. **No fly tower.**

**Top** — NOT flat. Dark metal hipped roofs with skylights, a large flat deck
behind the perimeter slopes, and modest roof plant. Because there is no tower,
the roofscape carries the entire aerial read of this building.

## Recognition cues (ranked)

1. **It is the Opera House's twin** — same base course, same cornice line, same
   Doric colonnade, same roof colour, read as a matched pair across the court.
2. The **7-bay paired-column loggia** over the rusticated arcaded basement.
3. **Strong horizontality** — one unbroken cornice line across the whole 67 m front.
4. **No fly tower.** The level silhouette is what tells it from the Opera House
   at a glance from the air.
5. Dark metal hipped roofs with skylights over pale terra-cotta walls.

## Features to preserve / simplify

**Preserve:** the four-part massing straight from the footprint table; paired
columns as genuinely doubled cylinders; arch alignment (basement arches under
loggia arches on one bay grid); the single unbroken cornice line at 24.5 m,
identical to the twin's; a real recessed loggia rather than applied pilasters;
hipped roofs with court-facing skylights; the calm level silhouette.

**Simplify:** fluting and capitals → plain shafts with square cap blocks;
rustication → two grooved courses in the base band; balustrades → solid rail
bands with post rhythm at the loggia only; attic perforations → shallow inset
panels; skylights → flat glass panels on the roof decks; inscriptions, sculpture
and lamp standards → dropped entirely.

## Night appearance

Matched to the twin, and for the same reason: warm `Toy_mustard_Glow` lit panes
set 5 cm proud behind each opaque `Toy_glass` arch (7 basement + 7 loggia + 24
flank/wing/shoulder windows), plus one thin `Toy_white_Glow` soffit strip under
the entablature as the floodlit-colonnade cue. Rear service windows stay dark. No
roof or cornice outlining — civic restraint. Every glow surface's day colour is a
palette entry its non-glow neighbours already use, so nothing shifts at noon.

## What differs from the Opera House, and what must match

**Must match exactly** (or the pair fails): basement course top 9.5 m; column
shafts 10.7–20.3 m; entablature 21.0–23.0 m; cornice 23.0–24.5 m; front attic
parapet 27.0 m; the palette (`Toy_stone` / `Toy_sand` / `Toy_trim` / `Toy_glass`
/ `Toy_ink` / `Toy_roofd` / `Toy_steel` + the two glow materials); the glow
scheme; the 81.11° bearing.

**Legitimately differs:** the plan (67.4 × 83.1 m vs 73.3 × 104.0 m); the front
pavilion is 45.5 m wide vs 48.6 m, so the bay pitch tightens from 5.14 m to
4.84 m; there is no fly tower, no stage house and no raised auditorium attic, so
the summit is 31.0 m rather than 44 m; the formal flank is the **south** one, the
opposite hand to the twin; the rear block is a 4-storey end bay on the cornice
line rather than a low back-of-house.

## Uncertainties / conflicting evidence

- **The 31.0 m architectural top is inferred** (see above). No section or
  elevation drawing was found. Shipped `"estimated": true`.
- **The 7-bay colonnade is inferred by twinning**, from the designation's
  "substantially identical" plus the Opera House's sourced 7-bay/8-pair scheme
  and this building's measured 45.5 m front pavilion. No photograph was read at a
  resolution that settles the count independently. If one does, it wins.
- **The intermediate heights** (base course 9.5, shafts 10.7–20.3, cornice
  23–24.5, attic 27, roof eaves 25.6, ridge 31.0) are the twin's, proportioned
  from its photographic study rather than measured on this building.
- **Roof pitch and skylight positions** are visual inference from "metal roof
  with skylights" (SGH) plus the twin's roofscape; the skylight count and layout
  are designed, not surveyed.
- **The shoulder steps** at u −3.1 and −4.3 are 1.1–2.7 m deep in plan. They are
  modelled as the corner pavilions' outer returns; whether they are full-height
  masonry or only a base-course widening is not established by any source.

## Corrections applied to the plan doc

1. **The plan's roofscape recipe (§2.8 item 11) described two ridged hips.** Built
   as *truncated* hips (flat deck inside a hipped perimeter) instead: it matches
   "metal roof with skylights" better, lets both roofs share one pitch, and gives
   the deck a surface to design — which matters more here than on the twin,
   because with no tower the roof is the whole aerial read.
2. **The plan implied the front hip could span the full 67.38 m wing width.** It
   cannot: the pavilion is only 45.5 m wide and the shoulders 52.2 m, so a
   full-width front roof hangs over open air at the front corners (this was
   visible in the first build's aerial). The front hip is bounded to the 52.2 m
   shoulder width, and the wings outboard of it get flat decks behind their
   parapets.
3. **The plan's §2.8 item 4 called for a loggia "back wall".** A wall alone left a
   void between it and the wings. Built as a solid 52.2 m front core to the
   cornice, with the loggia as a real 2.9 m recess in front of it.
4. **The plan gave the shoulders as an extension of the stone corner pavilions.**
   Built in `Toy_sand` and starting above the entablature instead: full-height
   stone shoulders merged with the pavilions into one blank slab corner that
   swallowed the colonnade's proportions.
5. The plan's §2.13 exclusion-radius suggestion of ~58 is kept, but see `REPORT.md`
   for the value actually used.
