# War Memorial Opera House — reference dossier

Compiled 2026-08-11 for the SF-SIM miniature asset. Facts verified independently of
the plan doc (`docs/asset-plans/war-memorial-opera-house.md`); corrections to the
plan are called out explicitly at the end.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM `way/32865161` (`api.openstreetmap.org/api/0.6/way/32865161/full.json`, checked 2026-08-11; tag `check_date=2026-07-14`) | Footprint polygon (95 nodes), `height=44`, `building=civic`, `amenity=theatre`, address 301 Van Ness Avenue, `ele=21` |
| OSM `way/32865757` (Overpass, same session) | The twin **Veterans Building** immediately north: `height=28` — anchors the shared main-block cornice/parapet height of both twins |
| [Wikipedia — War Memorial Opera House](https://en.wikipedia.org/wiki/War_Memorial_Opera_House) | Opened 15 Oct 1932; architects Arthur Brown Jr. + G. Albert Lansburgh; Beaux-Arts; 3,146 seats; facade scheme: “a colonnade of paired columns screens colossal arch-headed windows above a severe rusticated basement,” influenced by the Louvre Colonnade; lobby barrel vault parallel to the street |
| [structurae.net/en/structures/war-memorial-opera-house](https://structurae.net/en/structures/war-memorial-opera-house) | Independently repeats the paired-column/arch-headed-window/rusticated-basement scheme |
| [Verplanck HSR PDF](https://verplanckconsulting.com/War-Memorial-Opera-House.pdf) (historic structure report) | Granite + terra-cotta cladding; giant Doric order; all three civic buildings (City Hall, Opera House, Veterans) share rusticated granite bases + colossal Doric colonnades; scenery flies **75 ft above the stage** (fly interior clearance ⇒ tall fly tower); relieving arches with figural reliefs |
| [sfwarmemorial.org](https://sfwarmemorial.org/war-memorial-opera-house/) | 301 Van Ness Avenue (at Grove St); 38-ft main-lobby ceiling; operator context |
| Commons photos (all viewed this session): straight-on night elevation (`War Memoria Opera House at night.jpg`), oblique fronts (`San Francisco Opera House, July 2015.jpg`, `SF War Memorial Opera House (15066771483).jpg`, `San Francisco War Memorial and Performing Arts Center… (10754272665).jpg`), Grove St flank (`War Memorial Opera House side.jpg`), memorial-court flank + twins (`San Francisco City Hall, War Memorial Opera House, War Memorial Veterans Building.jpg`, `War Memorial complex (San Francisco).JPG`) | Bay counts, facade composition, roofscape, fly tower massing, night lighting behaviour |

## Verified dimensions and location

- **Footprint:** oriented bounding box **103.97 m (E–W, the auditorium axis) × 73.30 m (N–S, Van Ness frontage)**; polygon area 5,929 m². 
- **Orientation:** long edges bear **81.11° cw from true north** (56.2 m and 55.7 m edges @ 81.03–81.11°); the Van Ness front edge bears 170.7°. Front (colonnade) faces **east** onto Van Ness (facade normal ≈ bearing 81°, i.e. 9° north of due east — the standard Civic Center grid rotation, matching Grace Cathedral 81.03°, 555 California 81.23°).
- **Anchor:** oriented-bbox centre of the footprint = **−122.4209349, 37.7785711**. The plan's anchor (−122.4206423, 37.7785955) sits ~26 m ENE of this, toward the Van Ness edge — `placeGeneric` puts the exported bbox CENTRE on the anchor, so shipping the plan's anchor would push the model ~26 m east into Van Ness Avenue. Final anchor recomputed from the built model's own bbox centre in `REPORT.md`.
- **Heights:** fly tower **44 m** (OSM, the only tagged height — adopted as `targetHeightM`); main-block parapet ≈ **28 m** (inferred from the twin Veterans Building's OSM `height=28`; the two buildings read identical to the cornice in photos). Everything between is proportioned from photographs — no published section drawing was found (HSR text confirms the 75-ft fly clearance, consistent with a ~44 m tower).

## Footprint decomposition (from the 95-node polygon, building frame: u = metres back from the Van Ness front, v = metres from the south edge)

- **Front pavilion** u 0→~8: **48.7 m wide** (v 12.1→60.8), the colonnade block — NARROWER than the full frontage.
- **Side wings** u ~8→24: full **73.3 m** width, with curved reentrant quadrants (r ≈ 3.5 m) where they meet the auditorium block at u≈24–27.
- **Auditorium block** u ~27→83: **56 m** wide (v 8.6→64.5).
- **Stage/rear block** u ~83→104: steps to **48.1 m** wide (v 12.8→60.9) at the Franklin St rear face (u = 104).

## What each side shows (photo observations)

**East (Van Ness front):** rusticated basement with **7 round-arched glazed openings** (plus square-headed end doors), wrought lantern sconces between arches, broad full-width granite steps. Above a balustraded course, the giant Doric colonnade: **7 open loggia arches separated by PAIRED fluted columns (8 pairs, 16 columns)**, arch-headed openings behind an open gallery (warm lobby glass set back); balustrade between column pedestals. Full entablature, dentiled cornice, then an attic parapet with small grouped square perforations. The two **corner pavilions** are rusticated full-height with a tall blind arched niche at loggia level and “WAR MEMORIAL OPERA HOUSE” incised at the base.

**South (Grove St flank):** rusticated base with square service/entry doors under a long dark **entrance marquee**; lion-head keystones; above, **8 tall arched windows** in the auditorium run + arched windows in the wing bays; Vitruvian-scroll (wave) frieze band; low attic with small rectangular windows; then a SET-BACK attic storey with band windows and its own cornice; steep dark hipped roofs above. The fly tower rises at the west end as a plain granite box with sparse small windows, wave frieze, and its own dark hipped roof.

**North (memorial-court flank):** mirror of the south minus the marquee; corner pavilion with arched windows and quoined rustication; wings show **glazed skylight slopes facing the court** in their dark hipped roofs.

**West (Franklin St rear):** lower, plainer service block (~48 m wide) with regular small windows and parapet; the fly tower looms directly behind (east of) it.

**Top:** NOT flat — a composed roofscape of steep dark hipped roofs: front block (ridge ∥ Van Ness), two wing hips with court-facing skylights, the auditorium attic hip (ridge E–W), the fly tower's tall hipped cap (the summit, 44 m), and a low flat parapet roof on the rear block.

## Recognition cues (ranked)

1. The **7-bay paired-column loggia** over the 7-arch rusticated basement — the Louvre-colonnade formula, floodlit at night.
2. **Strong horizontality**: one unbroken entablature/cornice line across the whole 73 m front at ~24 m.
3. **Cream/pale-grey Beaux-Arts granite** matching City Hall across the avenue.
4. The **fly tower** rising quietly behind the calm front to 44 m, with its dark hipped cap.
5. The **dark steep hipped roofscape** (iron-grey) over pale walls — shared with the Veterans twin.

## Features to preserve / simplify

**Preserve:** the four-part massing (front pavilion + full-width wings + auditorium + stage/rear); paired columns as genuinely doubled cylinders (not a picket row); 7:7 arch alignment front/basement; the single cornice line; curved wing quadrants; the fly tower's height dominance; dark hips over pale walls; arched flank windows.

**Simplify:** fluting, capitals → plain shafts with square cap blocks; figural reliefs, lion keystones, inscriptions → dropped; balustrades → solid rail bands with post rhythm at the loggia only; marquee → single slim dark slab canopy; rustication → two grooved courses in the base band; attic perforations → shallow inset panels; skylights → flat glass panels set into the wing hips.

## Night appearance (photos)

The colonnade is floodlit warm-white from the balustrade level; the 7 loggia arches glow warm from the lobby behind; ground-floor arches glow amber; roofs vanish. Miniature translation: warm `Toy_mustard_Glow` lit-pane shells behind opaque glass in all arches (lit-lancet pattern), plus a thin `Toy_white_Glow` soffit strip under the entablature as the floodlight cue. Civic restraint — no roof or cornice outlines.

## Uncertainties / conflicts

- **No published cornice or intermediate heights** — 28 m parapet (Veterans tag), 9.5 m base course, 21.5 m column tops, 30 m attic block, 33.5 m attic hip peak, 40.5 m fly-tower wall / 44 m hip peak are all proportioned from photographs anchored to the two OSM tags. Marked `inferred` in REPORT.
- **Fly tower footprint** not mapped in OSM (no `building:part`): modelled ~40 × 20 m centred on the auditorium axis at u ≈ 72–92, from the Grove St photo and the 75-ft fly clearance; position/size are visual estimates.
- **Plan-doc corrections:** (1) the long axis is E–W (~81°), not N–S — the plan's “~171°” is the bearing of the front facade LINE; (2) the roofline is not “flat/low” — steep dark hips are a primary aerial cue; (3) the plan's anchor is ~26 m off the footprint centre (see above); (4) the front colonnade is 7 bays of paired columns (16 columns), not “10 columns”; (5) the front block is 48.7 m wide, not the full 73 m.
