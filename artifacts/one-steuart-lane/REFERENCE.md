# One Steuart Lane — reference dossier

Compiled 18 August 2026 for `artifacts/one-steuart-lane/`. This is the modelling
side's own record: what was verified, what was observed, what was inferred, and
where the plan in `docs/asset-plans/one-steuart-lane.md` was corrected. **This
file and REPORT.md beat the plan.**

## 1. What it is

**One Steuart Lane**, 1 Steuart Lane / 75 Howard Street, San Francisco 94105.
A 20-storey, 120-unit ultra-luxury condominium tower on the Embarcadero, by
**Skidmore, Owings & Merrill** (Craig W. Hartman FAIA senior design partner;
Mark Schwettmann design director; Keith Boswell partner for the enclosure), for
**Paramount Group** with SRE Group. Topped out September 2020, completed 2021.
Built on the site of the 75 Howard Street parking garage, which stood on the
"grungy edge of the Financial District" beside the Embarcadero Freeway until the
freeway came down in 1991.

John King, reviewing it for the Chronicle: it "looks less like a formal tower
than a carefully arranged stack of skeletal cubes, each of them three or four
stories tall." That sentence is the model's brief.

## 2. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| WGS84 anchor | `-122.3916888, 37.7915643` | **measured** — AABB centre of the OSM footprint, projected with the app's tangent projection |
| Architectural height | **67.06 m = 220 ft** | **measured** — five independent sources, see §6 risk 1 |
| Footprint | 1,904.1 m2, four-vertex rectangle 40.52 x 47.02 m, rotated 44.9° | **measured** — OSM way/667097308 |
| Site area cross-check | SOM publishes 20,595 sq ft = 1,913.3 m2 | agrees to **−0.5%**, i.e. full-lot coverage |
| Storeys | 20 above grade (SOM, developer, trade press); 21 in DBI permits and OSM | see §6 risk 3 |
| Gross floor area | 335,000 sq ft = 31,120 m2 published | the model's five volume plans sum to ~29,600 m2, **−5%** — see §5 |
| Parcel | block 3741, mapblklot 3741047, base lot 045 | DataSF parcels; DBI permits |
| Ground | 3.19–3.86 m NAVD88, σ 0.13 m across the parcel — flat | DataSF; the app's terrain handles it, the asset needs no plinth |

Edges and outward normals, measured from the footprint polygon:

| Edge | Length | Outward normal | Faces |
|---|---|---|---|
| N→E | 40.52 m | **44.2°** NE | **Steuart Lane / Steuart Street** — entrance, Bay elevation |
| E→S | 47.02 m | **134.8°** SE | block interior |
| S→W | 40.63 m | **224.5°** SW | block interior |
| W→N | 46.83 m | **314.9°** NW | **Howard Street** |

Street sides were measured, not assumed — each face midpoint against the DataSF
street-centreline layer (`3psu-pn9h`): Howard 11.6 m off the NW face; Steuart
Lane 13.2 m and Steuart Street 13.7 m off the NE face with The Embarcadero
45.5 m beyond; Spear Street 48.4 m off the SW face; Folsom 141.5 m off the SE.
So the building sits inland of Steuart, in the block it shares with the Gap
headquarters, and the NE face is the one that looks across Steuart to the Bay.

## 3. Sources, and what each establishes

- **SOM project page** (`som.com/projects/one-steuart-lane/`) — the primary
  source. Architect, 220 ft, 20 storeys, 20,595 sq ft site, 335,000 sq ft gross,
  120 units, LEED Gold. Also the design intent: the outdoor spaces "break down
  the vertical orientation of the tower into horizontally-proportioned volumes",
  and the facade is "an elegantly proportioned, shifting grid of roman travertine
  pilasters and lintels", "a slender, variegated grid of silver travertine".
- **The Architect's Newspaper / Facades+**, 9 Jul 2021 — the enclosure article,
  quoting SOM's Boswell/Schwettman/Kuchen directly: "modules ranging in width
  from four to six to eight feet", stone concealing the aluminium, GFRC inside.
  Confirms "stacked square volumes, with a self-admittedly boxy massing broken
  up by wrap-around terraces placed at each zoning-mandated setback."
- **Enclos** (the facade design/build contractor) — the only hard ground-floor
  numbers: a 24 ft tall glass main entry, a glass-fin-supported canopy 17 ft 10 in
  wide cantilevering **11 ft** clear of the facade, a custom wood door with cast
  glass blocks in a bronze portal frame, blackened stainless panels, stone
  baguettes.
- **SF Chronicle**, John King, 12 Oct 2021 — the best written description:
  "thick bars of Roman travertine"; the glass "begins a full 6 inches back from
  the creamy stonework's outer edge"; "full-length terraces every few floors,
  plus a single bay of deep terraces running up each side of the tower". Also the
  source of the disputed 240 ft.
- **SF YIMBY**, 22 Sep 2020 (topping out) — "reached its 220-foot pinnacle";
  "composed of **five masses** cantilevered over what will become private
  terraces for twelve larger residences"; "forty-foot wraparound terraces".
- **Swinerton** (general contractor) — Type-1 concrete, post-tensioned decks,
  21 stories, 118 units, 3 parking levels.
- **PRNewswire** topping-out release — 20 storeys, 220 ft, 120 units.
- **CTBUH / Skyscraper Center** — lists 73.2 m / 240 ft. Conflicts; see §6.
- **OSM way/667097308** — the footprint. `building:levels=21`, `height=67.056`,
  `roof:shape=flat`.
- **Google Street View**, panoramas (May 2025 unless noted), fetched as
  rectilinear thumbnails from `streetviewpixels-pa.googleapis.com` with a
  browser User-Agent and a `google.com` referer:
  - `FgQeEOFiFPKjWDAfs-1pNg` — 222 The Embarcadero, 70.6 m out on bearing 228°.
    The north-east elevation head-on, full height. *The best elevation reference.*
  - `ovtx36arpx2McKDNysw2wA` — 250 The Embarcadero, 68.7 m out on bearing 272°.
    The three-quarter down the east corner. **The massing reference** — the five
    volumes, the alternating steps and the terraces are all legible in it.
  - `xXe2riqG1LYNcj4uxMyibw` — 275 Steuart Lane, 37.2 m out. The base.
  - `ZUh55kQzLojQ3Ae-8Z8tPg` — 58 Howard St, Aug 2024, 33.3 m out. The travertine
    grid at full size, with the module widths visibly irregular, and the deep
    terrace slot.
  - `_NsXTVXb0T8LqAa5H_NuHg` — 210 Spear St. **Does not see this building**;
    120 Spear blocks it. There is no street-level view of the south-west face.
- **Google satellite `mt1.google.com/vt/lyrs=s` at z21** — the roof. See §4.
- **Esri World Imagery z19/z20** — *construction-era here*: a tower crane,
  formwork and storage tanks on an unfinished deck. Do not read the roof from it.
- **DataSF**: parcels `acdm-wktn`; permits `i98e-djp9` (original construction
  permit 2016-0401-3681); street centrelines `3psu-pn9h`. The building-footprint
  layer `ynuv-fyni` **does not contain this building** — its ring on this parcel
  (`mblr = SF3741031`, median 21.55 m) is the demolished garage, captured by 2010
  LiDAR.

No copyrighted imagery is committed. The URLs and panorama ids above are
sufficient to re-open every reference.

## 4. Observations, side by side

**North-east (Steuart Lane), 40.52 m** — a double-height dark storefront divided
by clusters of slender vertical travertine baguettes; the main entrance toward
the north end under a projecting flat glass canopy, with a bronze portal and a
wood door; a travertine band over it; then the level-2 amenity floor set back
behind its own glass with planters. Above, five stacked volumes of travertine
cage over recessed glass, each stepping in or out from the one below. The top
volume reads noticeably more open — closer to a bare frame with sky behind it.

**South-east flank, 47.02 m** — no street-level view. Fully treated in the same
grid; this is not a party wall. Its volumes step on the opposite beat from the
north-east face, which is what makes the east corner zig-zag.

**South-west flank, 40.63 m** — the least documented elevation. Finished in the
same grid per the oblique aerials. Modelled as a quieter version of the
south-east face. Bay count *inferred*.

**North-west (Howard Street), 46.83 m** — the best close view of the grid: thick
cream pilasters and lintels framing large blue-grey panes, module widths visibly
irregular (two narrow bays beside one wide one). Dark storefront behind
baguettes at ground level with the `ONE STEUART LANE` signage; a garage/service
opening toward the west end. A one-bay-wide slot of **deep terraces** runs up
the elevation left of centre — recessed, dark soffits, clear glass balustrades.

**Top** — read from Google z21. A flat deck inside a continuous cream parapet:
a **field of dark blue photovoltaic strips** in two bays split by a pale walkway,
covering roughly half the deck; a mechanical yard with **two large round cooling
towers** and a row of low plant boxes; a light-toned **mechanical penthouse box**
which is the crest; and a **BMU (window-washing) crane** on a track running
across the deck with its boom parked. Terrace levels step in below the parapet,
paved, with square planters that read green from above. No tree canopy overhangs.

## 5. What the model does with it

Five volumes on a two-storey base, 20 storeys total, floor-to-floor 2.983 m.

| Element | Storeys | Top (m) | Per-edge insets NE / SE / SW / NW |
|---|---|---|---|
| Base | 2 | 9.80 | full lot |
| Volume A | 3 | 18.75 | 0.0 / 0.0 / 0.0 / 0.0 |
| Volume B | 4 | 30.68 | 4.6 / 0.6 / 4.8 / 0.8 |
| Volume C | 4 | 42.61 | 0.8 / 5.4 / 1.0 / 5.6 |
| Volume D | 4 | 54.55 | 5.6 / 1.4 / 5.8 / 1.6 |
| Volume E | 3 | 63.49 (roof deck) | 1.8 / 6.6 / 2.0 / 6.8 |
| Parapet / penthouse | — | 64.55 / **67.06** | — |

The insets **alternate** rather than shrink monotonically: each volume pulls back
hard on one pair of sides while coming back out over the volume below on the
other pair. On the Steuart elevation the successive wall planes stand at 23.49,
18.89, 22.69, 17.89 and 21.69 m from the anchor — out, in, out, in. That is the
correction that matters most in this build; see §6.

Setback depths are not published anywhere, so they were sized by a **gross-floor-
area cross-check**: the five plans as modelled sum to ~29,600 m2 against the
published 335,000 sq ft (31,120 m2), −5%. That is the only quantitative evidence
behind them.

Facade: a dark glass plate just proud of each volume shell, then the travertine
cage — a 0.70 m cream lintel at every floor line and a 0.58 m cream pilaster at
every module boundary — standing 0.44 m in front of it. The real wall's 4/6/8 ft
panels are kept as a *ratio* but grouped roughly 3:2, landing 11–13 bays per
elevation; one-for-one would be ~19 bays across a 47 m face, which at the app's
scale is noise rather than a grid. One module per elevation is the deep terrace
bay: its glass sits back at the shell and it gets a slab and a balustrade per
floor, so it reads as a loggia carved out of the cage.

Night: the real building is downlit from under its cantilevers, so the hero glow
is a thin cream line under each of the four terrace slabs plus the base cornice —
**five horizontal bands that restate the horizontal massing** — with a warm gold
lobby patch on Steuart Lane and a sparse scatter of pale blue lit units. Nothing
else glows.

## 6. Uncertainties and conflicting evidence

**1. The height: 220 ft or 240 ft.** SOM, Swinerton, the developer's release,
California Construction News, SF YIMBY's topping-out report ("its 220-foot
pinnacle") and OSM's `height=67.056` (220.00 ft to the centimetre) all say
**220 ft**. CTBUH says 73.2 m / 240 ft, and John King repeats 240 ft, most
likely from CTBUH. The model uses **67.06 m** on the weight of the primary
sources — the architect, the general contractor and the developer all agree.

The reconciliation that would make both true: SF measures zoning height to the
roof and permits certain rooftop features above it, so 220 ft is the approved
envelope (this site was raised from the block's 200 ft limit after the 2013–15
waterfront height fights) and 240 ft would be the top of a mechanical penthouse.
Against that, the penthouse in the aerial imagery does not look 20 ft proud of
the parapet, and "220-foot pinnacle" was written about a structure that had just
topped out.

The honest counter-argument is arithmetic: 20 storeys in 220 ft, with a 24 ft
entry level, leaves ~10 ft floor-to-floor for units with nine-foot ceilings and
tapered post-tensioned slabs. Tight. At 240 ft it is ~11.4 ft, which is normal.
**A rectified facade elevation from the 222-Embarcadero panorama would settle
it and was not attempted here.** If it is wrong, the cost is contained: the tower
body is authored at absolute heights, so a corrected crest moves the penthouse
box and rescales by 9%, not more.

**2. The footprint has only one source.** DataSF's LiDAR layer predates the
building by a decade. OSM way/667097308 is the only survey available. It agrees
with SOM's published site area to 0.5% and overlays correctly on 2024–25 Google
imagery, but there is no second measurement. Its two opposite-edge pairs differ
by 0.11 m and 0.19 m — trace noise; the model builds on the polygon as given.

**3. Twenty storeys or twenty-one.** SOM, the developer and the trade press say
20; DBI permits and OSM say 21. Both are probably right about different things —
20 residential levels above a ground floor that DBI counts separately. Unit
numbers in the permit record run to 2004, i.e. level 20. The model shows 20
levels above grade.

**4. Setback depths are inferred**, sized only by the gross-floor-area check in
§5. The published record contains the number of masses (five), the terrace
lengths (40 ft) and the deepest terrace (16 ft), but no plan dimensions.

**5. The south-west elevation is undocumented at street level.** Its bay count is
inferred from oblique aerials.

**6. The entrance canopy oversails the property line** by 3.4 m, which is why the
export's XY bounding box is 62.95 x 62.49 m rather than the footprint's
62.10 x 61.65 m. That is real — Enclos records an 11 ft cantilever over the
Steuart Lane sidewalk — and it is why the validator's dimension gate was widened.

## 7. Corrections made during the build

Recorded because they are the kind of thing that gets silently re-inherited.

1. **A ziggurat is the wrong massing.** The first build used monotonically
   shrinking concentric setbacks and rendered as a wedding cake. The published
   description is "five masses **cantilevered** over ... private terraces" — the
   volumes alternate in and out. Rebuilt with alternating per-edge insets.
2. **Recessed plates are invisible.** The facade was first authored with the glass
   at a negative offset, i.e. *inside* the solid volume shell, and the whole tower
   rendered as blank cream. Every surface must stand proud of the shell; the
   recess read comes from the frame standing in front of the glass, not from
   burying anything. (This is the 300 Brannan / 500 Third idiom and it is why the
   model needs no booleans.)
3. **Roof furniture must be laid out inside volume E's plan, not the lot's.**
   E is 27.1 m along the building's U axis against the lot's 47 m; the first roof
   put cooling towers 16.5 m off-centre, hanging in mid-air.
4. **The night render rig was lying.** glTF writes `emissiveFactor = 0` when the
   authored emission strength is 0, so raising `Emission Strength` on a
   re-imported `_Glow` material renders it **white**. `light_glow()` now copies
   Base Color into Emission Color at strength 1.0, which is also what the app
   does. The first night render showed white bands where the palette says cream
   and gold.
5. **`Toy_roofd` was avoided on the roof deck** on the standing note that it
   renders near-black under the app's lighting. The deck is `Toy_steel`.
