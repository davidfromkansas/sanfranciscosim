# Pier 19 — SF-SIM asset plan

**Pier 19, The Embarcadero (at Green Street)** — a 1936–1938 reinforced-concrete finger pier
on the northeast waterfront, a **Contributing Resource of the Port of San Francisco
Embarcadero Historic District** (National Register, 2006). A 153-foot-wide, 800-foot-long
pile-supported deck carrying a full-length steel-frame transit shed with a continuous roof
monitor, fronted on the Embarcadero by a classical stucco bulkhead building whose broad
central pavilion carries a **monumental semicircular arch, "PIER 19" in raised metal letters,
and a gabled parapet**. Pier 19 and Pier 9 are near-identical twins, built at the same time
to the same drawings. Since 1961 a plain connector shed (non-contributing) has joined
Pier 19's shoreward end to Pier 23; today the pier is Port of San Francisco storage/shed
space with a Hornblower layberth on the south apron — an honest working pier, not a
destination.

This is a **water asset**: nothing under it is land. The loader seats generic landmarks at
`max(0, sampleElevation(x, z))`, so over the bay the origin lands exactly on the water plane
y = 0 — the same contract Pier 1, Pier 3, the bridges and Alcatraz use. Every height in this
plan is quoted **above water level**, not above the promenade.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/pier-19/`. This document is the plan only: Part 1 is the runnable task prompt,
Part 2 is the research and design dossier behind it.

| | |
|---|---|
| Manifest id | `pier-19` |
| Existing procedural builder | none — new landmark, **Case B** (needs a `pipeline/lib/landmarks.mjs` entry and a re-bake, see 2.13) |
| WGS84 anchor | `-122.3988051, 37.8030166` (deck-rectangle centre, over water) |
| Target height | **17.0 m** to the gabled-parapet crest above water; shed roof field ~13.0 m; deck top 2.0 m. The LiDAR max (19.5 m) and first-return peak (20.4 m) are the flagpole and are excluded by design |
| Footprint | deck 46.63 m × 262.13 m (153 ft × 800 ft pier + 60 ft bulkhead wharf); transit shed 34.3 m × 194.9 m measured; long axis bearing 54.89° |
| Triangle cap | 18,000 |
| Category | `25` (maritime/transit, same as `ferry-building`) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Pier 19 GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Pier 19, The Embarcadero, San Francisco** and
deliver it as a downloadable, validated GLB.

Do not integrate or deploy the model yet. Create the asset, validate it, render review
images, and commit the deliverables to your working branch.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `artifacts/pier-1/` — the closest reference implementation: the same pier typology
   (bulkhead building + transit shed on a pile deck over water), already shipped and
   integrated. Reuse its palette decisions and its deck/pile approach.
8. `docs/asset-plans/pier-19.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules.

## Must capture

- The **bulkhead pavilion**: a broad central pavilion on the Embarcadero frontage with a
  single monumental semicircular arch (steel roll-up door inside it), a molded archivolt,
  flanking piers with strong horizontal banding, "PIER 19" lettering in the attic band
  over the arch, and a **gabled (pedimented) parapet** whose peak is the top of the whole
  asset. This is the identity of the pier and where the semantic exaggeration goes.
- The **flanking bulkhead wings**: lower flat-roofed stucco bays either side of the
  pavilion with horizontal scoring and rows of tall dark steel-sash windows.
- The **transit shed**: a 195 m long, 34 m wide volume filling most of the deck — scored
  precast concrete walls, roll-up doors down both flanks, a low-pitch roof rising to a
  **continuous monitor (clerestory) running the full length of the shed**. From the app's
  aerial camera this roof and its monitor are the primary reading of the asset.
- The **rear (east/bay-end) elevation**: faintly Art Deco — six profiled pilasters rising
  to peaks just above the roofline around a gabled central bay (NRHP description). One
  restrained gesture here is enough.
- The **pier deck on piles**: fendered edges, mooring bitts at the head apron, narrow side
  aprons (the south apron is the working one — the north apron along the Pier 23 slip is
  closed/deteriorated in reality; keep it plain).
- The **taper of use, not form**: unlike Pier 3 there is no parking field — the deck
  reads as shed + narrow aprons + open head apron.

## Research Pier 19 independently

Verify the dossier rather than trusting it. Re-check at minimum the architectural height,
the footprint, the WGS84 anchor, the deck elevation above water, and the orientation, and
gather references covering: the Embarcadero (southwest) elevation straight on; both long
flanks; the pier head from the bay; aerial/roof views (monitor, roof color, apron state);
night views if any exist.

Prefer the National Register nomination for the Port of San Francisco Embarcadero Historic
District (Section 7 has a per-element description of Pier 19), Port of San Francisco
documents, geolocated photography (Wikimedia Commons category "Pier 19 (San Francisco)"),
and aerial/satellite imagery. Never rely on a single photograph or a single unsourced 3D
model.

**Known source conflicts, already resolved in 2.1 — re-check, do not re-inherit:**

- OSM has **no way named "Pier 19"**. Building way 91913152 (`building=yes, height=10`) is
  a **single merged polygon** covering the Pier 19 shed, the Pier 23 shed and the 1961
  connector between them. The DataSF LiDAR footprint (`sf16_bldgid 201006.0000010`,
  `mblr SF9900019H`) traces the same merged complex. Neither is "Pier 19's footprint";
  use the south finger + the BSHC dimensions (153 ft × 800 ft) as this plan does.
- The LiDAR `hgt_maxcm = 1751` (19.5 m above water) and `peak_1st_m = 20.45` are **the
  flagpole**, not the masonry crest. The modeled top is the gabled-parapet crest at
  17.0 m; do not normalize the model to the flagpole.
- The Port's leasing pages quote rentable areas (5,699 / 4,000 / 10,000 sq ft) — these are
  interior lease subdivisions, not the building footprint.
- Photographs from 2011–2017 show roof colors that have since changed (the 2017 Coit
  Tower photo shows Pier 19 pale and Pier 23 dark; current imagery shows both pale grey
  with buff weathering on Pier 19). Model the current state, in toy palette terms.

## Create a reference dossier

Write `artifacts/pier-19/REFERENCE.md`: source links and what each establishes; verified
dimensions and location; orientation; observations from all four sides and above; the 3–5
strongest recognition cues; features to preserve; features to simplify; uncertainties.

## Make your own design decisions

Follow the conversion process in `docs/styles/miniature-toy.md` §22. This is a
**hero-adjacent landmark**: a National Register contributor on the postcard waterfront,
but a plain working pier — the plainest of the pier row. Spend the budget on the bulkhead
pavilion, the shed's monitor, and the deck edge. Resist monument-tier ornament: the shed
walls are scored concrete panels with roll-up doors, nothing more. The asset must read as
the modest, slightly weathered sibling between Pier 17 and Pier 23.

## Scope of the exported asset

Export the Pier 19 structure only: the pile-supported deck (46.63 m × 262.13 m including
the bulkhead-wharf strip), the transit shed with its monitor, the bulkhead building
(pavilion + wings, ~53 m frontage), and fixed deck furniture (fender line, mooring bitts,
a few light standards).

**Do not include** the Embarcadero roadway, Herb Caen Way, the F-line tracks, palm trees,
the seawall promenade, the **Pier 19–23 connector shed**, **Pier 23**, Pier 17, the water
surface, or any moored vessel (the Hornblower layberth boats move; the app has a live
vessel layer). The connector is real but it is (a) non-contributing, (b) mostly over the
Pier 23 slip, and (c) excluded from scope so that a future `pier-23` asset can own it or
its absence; Pier 19's north wall and north bulkhead wing must therefore be finished
plainly, as built (they exist inside the connector today).

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. At minimum: binary `.glb`;
real-world meters; origin at base center; minimum geometry Z ~ 0; applied transforms; no
negative scales; outward normals; no duplicate or foreign geometry; no image textures; no
transparency; flat-color materials named `Toy_*` from the project palette; `_Glow` suffix
only on surfaces that glow at night; no `Toy_body`; no cameras, lights, animations,
armatures or constraints; at most 18,000 triangles.

**Water datum — read this twice.** The origin sits on the water plane. Minimum geometry
Z = 0 is the **waterline**, not the deck. The pile field and deck soffit occupy 0 → 2.0 m
and must be modelled, not implied — the camera goes to water level. Every height in 2.1
and 2.7 is already above this datum; do not add the promenade elevation a second time.

**Orientation:** author with Blender `+Y` = true north, `+X` = east, so the model drops
into the city at its real heading — the loader applies no rotation. The pier runs into the
bay on a bearing of **54.89°**; the bulkhead frontage faces southwest at **234.89°**.
Build on the measured rectangle in 2.3 rather than rotating an axis-aligned box by eye.

**Height normalization:** the tallest geometry in the export (the gabled-parapet crest
cap) must land at exactly **17.0 m** so the loader's `targetHeightM / measuredHeight`
scale is 1.0. **Do not model the flagpole to its real 19.5–20.4 m** — a hairline pole as
the bounding-box top is exactly the trap 2.15 documents. Either omit it or keep a stub
below 16.5 m.

## Reproducible Blender workflow

Blender headless: `blender -b --python build_pier_19.py`. Keep
`artifacts/pier-19/build_pier_19.py` (deterministic build script) and
`artifacts/pier-19/pier-19.glb`. The script must rebuild the model reliably.

## Required review renders

`pier-19-top.png`, `pier-19-north.png`, `pier-19-east.png`, `pier-19-south.png`,
`pier-19-west.png`, `pier-19-contact-sheet.png`, a high three-quarter aerial
`pier-19-aerial.png` flown from the **southwest** (the only angle that reads the pavilion
and the full shed run at once), a night render `pier-19-aerial-night.png`, and one **low
three-quarter from the water** proving the piles, soffit and deck edge exist. Elevations
share scale, framing, lighting and projection; the top view must clearly show the monitor,
the roof planes and the aprons. Review from the high three-quarter aerial FIRST, iterate,
then run the formal rig.

## Validate the exported GLB

Re-import `pier-19.glb` into a fresh isolated Blender scene and validate the re-import.
Report object count, triangle count, dimensions, bbox min/max, min Z, XY center offset,
material names, texture/camera/light/animation counts, applied transforms, negative
scales, normals, per-material contract compliance. Write `artifacts/pier-19/validation.json`
and `artifacts/pier-19/REPORT.md`.

The axis-aligned XY bounding box will be roughly **241 × 189 m** even though the pier is
262 × 47 m — the expected consequence of the 54.89° heading, not a scale error.

## Manifest draft

Include this draft in `REPORT.md`; do not edit the production manifest in this task.

```json
{
  "id": "pier-19",
  "file": "pier-19.glb",
  "anchor": [-122.3988051, 37.8030166],
  "targetHeightM": 17.0,
  "cat": 25,
  "name": "Pier 19",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`,
or any app code in this task. Integration is a separate job —
`docs/asset-plans/INTEGRATION-PROMPT.md` plus the notes in 2.13 of this plan.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026. Values marked *inferred* are visual or derived estimates; the
executing agent must re-verify anything it relies on. Everything marked *measured* was
computed in this session from the named dataset and is reproducible from 2.3 and 2.16.

### 2.1 Verified facts

| Item | Value | Source / confidence |
|---|---|---|
| Name | **Pier 19** | Port of SF; NRHP |
| Address | Pier 19, The Embarcadero, San Francisco 94111 (task input gave "1098 The Embarcadero"; the Port and all federal documents use pier numbers, not street numbers) | Port of SF leasing pages |
| Built | **1936–1938** (shed + bulkhead building; bulkhead-wharf substructure 1922). Substructure by Ben C. Gerwick Inc. ($408,783.89); sheds by Barrett & Hilp ($274,149.60) | NRHP Section 7, pp. 122–125 — the single best source |
| Twin | **Pier 9** — "identical in design and dimensions, except for minor differences at the inner ends" | NRHP §7, quoting BSHC [1938]:51 |
| Designers | Substructure/shed plans by G. A. Wood, bulkhead building by H. B. Fisher, both under Frank G. White, Chief Engineer, BSHC | NRHP §7 |
| Historic status | **Contributing Resource, Port of San Francisco Embarcadero Historic District** (NRHP, Jan 2006) | NRHP §7 |
| Pier dimensions | **153 ft wide × 800 ft long** (46.63 m × 243.84 m); bulkhead wharf **60 ft deep** at the pier (1922) | BSHC [1938]:51 via NRHP §7 |
| Substructure | concrete deck on timber piles in precast concrete jackets under the shed; **creosoted timber aprons**; rail spur each side (north one depressed); Topeka asphalt paving | NRHP §7 |
| Transit shed | steel frame; **precast concrete walls, scored on the exterior**; roof on steel trusses divides interior into three aisles; **continuous monitor along the full length**; steel-sash windows (south wall ones mostly plated over); roll-up doors in all three walls | NRHP §7 |
| Rear (east) elevation | "faintly Art Deco — six profiled piers rising to peaks just slightly above the roofline and a gabled central pavilion" | NRHP §7 |
| Bulkhead building | 1936–1938, timber-framed, stucco; classical; broad central pavilion, monumental arched entry with steel roll-up door, monumental flanking piers, **gabled parapet**; "PIER 19" raised metal letters over the arch; flagpole on top; pedestrian doors flank the arch; two flat-roofed bays north (unequal), matching bays south | NRHP §7 + Commons photo (2012) |
| 1961 alteration | **Pier 19–23 connector shed** (S.S. Gorman, Chief Engineer): removed the western 80 ft of the shed's north wall, obscured the bulkhead building's north elevation. Non-contributing, **out of scope** | NRHP §7 |
| Operator history | Pacific Oriental Terminal Company, 1939–1962 | NRHP §7 |
| Current use | Port of SF shed/storage space for lease (divisible fenced storage; $1.65–1.80/sf); **Hornblower layberth on Pier 19 South**; north apron deteriorated (dry-rot wood piles), reconstruction tied to the Pier 27 project | Port leasing flyer 2024; Port availability report May 2025; Port berthing schedule; Port facility assessment |
| Merged footprint | OSM way 91913152 and DataSF `201006.0000010` (`SF9900019H`) both trace **Pier 19 shed + Pier 23 shed + connector as ONE polygon**, 21,598 m² — **measured** | Overpass + DataSF `ynuv-fyni` |
| Shed footprint | **34.3 m wide × 194.9 m long**, long axis bearing **54.89°** | south finger of the merged ring, reprojected — **measured**, see 2.3 |
| Anchor (deck centre) | **-122.3988051, 37.8030166** | deck rectangle from BSHC dims laid on the measured axis — **measured**, see 2.3 |
| Deck elevation | **2.0 m** above water datum | DataSF `gnd_mediancm = 203` for SF9900019H — **measured** |
| Shed roof field | **~13.0 m** above water | LiDAR `hgt_majoritycm = 1096` + deck 2.03 — **measured** (dominant plane over the merged ring; both sheds are the same design so the statistic transfers) |
| Roof median | 12.2 m above water (`hgt_mediancm = 1014`) | same — **measured** |
| Gabled-parapet crest | **17.0 m** above water | *inferred*: LiDAR max region minus flagpole, cross-checked against facade proportions in the 2012 photo (see 2.16); ±1 m |
| Flagpole | 19.5 m (`hgt_maxcm`) to 20.4 m (`peak_1st_m`) above water — **excluded from the model top** | DataSF — **measured**; the max/peak pair is the classic flagpole signature |
| Embarcadero promenade | ~3.0 m above datum at the frontage | consistent with Pier 1/Pier 3 plans; *inferred* |

### 2.2 Sources

- `https://www.sfport.com/files/2022-12/EmbarcaderoRegisterNominationSec7.pdf` — NRHP
  Section 7, Port of San Francisco Embarcadero Historic District (Jan 2006). Pages
  122–125: complete description + construction history of Pier 19 (substructure, shed,
  bulkhead building, connector). **Authoritative for everything architectural.**
- `https://commons.wikimedia.org/wiki/Category:Pier_19_(San_Francisco)` — four photos:
  the 2012 frontal facade photo (`Pier 19, San Francisco.JPG` — pavilion, arch, banding,
  lettering, flag), the June 2017 Coit Tower aerial (`Pier 19 and 23 from Coit Tower` —
  roofs, monitor, connector roof, aprons), a 2011 wharves panorama, a 1977 HABS view of
  Piers 23 & 19.
- Google satellite imagery (current, fetched this session at z19) — roof state: pale grey
  with buff weathering, continuous monitor, pale side aprons, boat at the south apron,
  deteriorated north-apron strip along the Pier 23 slip; connector roof flat pale grey.
- DataSF `ynuv-fyni` (LiDAR building footprints), row `sf16_bldgid 201006.0000010`
  (`mblr SF9900019H`) — merged-ring geometry + height statistics used in 2.1.
- OSM: way 91913152 (merged building), node 1436065856 (Pier 23 Cafe, locates the north
  end of the frontage); ways 25489458 / 1390720126 (Pier 17, the southern neighbour).
- `https://www.sfport.com/files/2024-03/pier_19_marketing_flyer.pdf`,
  `https://www.sfport.com/sites/default/files/2025-05/availability_report_may_2025.pdf`,
  Port berthing schedules (`sfport.com/media/10573`, `/media/10181`) — current use.
- `https://www.sfport.com/files/Business/Docs/Permit%20Services/Finger%20Pier%20Exiting%20Guidelines%20-%2012.2013%20Final.pdf`
  — Port finger-pier typology document; Pier 19 is its "fully built-out without parking"
  model case (confirms: no parking field on the deck, shed fills the pier).
- Exa searches this session: `Pier 19 The Embarcadero San Francisco history built transit
  shed bulkhead` (surfaced the NRHP PDFs), `Pier 19 ... bulkhead facade photo arch
  flagpole` (surfaced Commons + HABS + Port flyer), `Pier 19 San Francisco Port tenant
  current use 2024 2025` (surfaced availability report + berthing schedules).

### 2.3 Footprint & orientation (measured)

Local tangent projection per AGENTS.md (`LON0 -122.4375, LAT0 37.77`). The Pier 19 shed is
the south finger of merged OSM way 91913152 / DataSF SF9900019H:

- Shed north edge: `37.802761,-122.399600` → `37.803775,-122.397788`; length **194.90 m**,
  bearing **54.89°**. Shed width (south edge to north-edge line): **34.2–34.4 m**.
- The bulkhead frontage runs `37.802154,-122.399864` → `37.803242,-122.400850` at bearing
  **324.19°** — 90.7° to the pier axis, i.e. the pier meets the street square within 1°.
- The model rectangle is the BSHC pier laid on the measured axis: **width 46.63 m**
  (153 ft) centred on the shed axis, **length 262.13 m** (60 ft bulkhead wharf + 800 ft
  pier) from the street frontage. Its seaward end lands 9.6 m past the measured shed rear
  — the open head apron, visible in satellite imagery. Consistency check: street corner →
  shed rear measures 252.5 m vs 252.5 m predicted (57.6 setback + 194.9 shed).
- **Anchor (deck-rectangle centre): `-122.3988051, 37.8030166`.**
- Axis-aligned bbox of the rotated rectangle ≈ 241 × 189 m (with the 53 m bulkhead
  frontage adding a fringe).

### 2.4 Massing recipe (build order)

All heights above water datum y = 0. Author in the pier frame (s = along axis from the
street frontage, w = across axis, centred), then map to world with the 54.89° bearing.

1. **Pile field + deck slab**: deck top 2.0 m, slab ~0.55 m thick; chunky toy piles
   (~0.45 m square, ~6 m grid, two rows visible along each flank) from z 0 to the soffit.
   Deck 46.63 × 262.13 m. Fender line: a darker continuous rub strip + regularly spaced
   fender piles along both flanks and the head.
2. **Transit shed**: 34.3 × 194.9 m, s from 57.6 to 252.5. Side walls to eave ~11.8 m;
   low-pitch roof planes rising to the monitor; **monitor** ~6 m wide, full length, top
   ~14.8 m, clerestory band down each monitor side. Scored-panel rhythm on the walls
   (shallow pilaster strips every ~9 m), roll-up door bays along both flanks, high strip
   windows between (south-wall ones read blind/plated).
3. **Rear (bay-end) elevation**: six shallow profiled pilasters rising just above the
   roofline + a gabled centre bay; one roll-up door at deck level.
4. **Bulkhead building**: frontage at s = 0, ~53 m wide (wings extend ~3 m past the deck
   edges), ~12 m deep to where the shed begins reading. Wings: flat parapet 11.5 m,
   horizontal scoring, tall dark window bays. **Central pavilion**: ~18 m wide, banded
   flanking piers, semicircular arch (opening ~11 m wide, crown ~12 m), archivolt, attic
   band with "PIER 19" (raised dark blocky letters or an incised band — keep it legible,
   not literal type), **gabled parapet with crest cap at exactly 17.0 m**. Pedestrian
   doors flanking the arch; cast-iron wheel-guard bollards at the jambs.
5. **Deck furniture**: mooring bitts on the head apron, a few toy light standards along
   the south apron, nothing on the closed north apron.
6. **No connector, no Pier 23, no vessels, no street furniture.**

### 2.5 Palette map (Toy_* from the project palette, matching pier-1)

- Bulkhead stucco + pavilion: `Toy_cream` / `Toy_white` (trim, cope, archivolt)
- Shed precast walls: `Toy_stone` (scored panels), plinth `Toy_stone` darker sibling if
  the palette provides one
- Shed roof planes: `Toy_stone`-family warm grey (buff-weathered pale grey in reality)
- Monitor clerestory + shed strip windows: `Toy_glass` / `Toy_glassl`, with
  `Toy_glassl_Glow` for the night state (see 2.6)
- Steel-sash bulkhead windows: `Toy_navy` or `Toy_glass` (dark blue-grey graphical
  windows per the style bible)
- Roll-up doors: `Toy_steel` / `Toy_ink`
- Deck + aprons: `Toy_stone` warm concrete; fender line + piles: `Toy_ink` /
  dark timber tone
- Lettering: `Toy_ink`

Exact RGB values: reuse `artifacts/pier-1/build_pier_1.py`'s palette block — same
family, proven in the app's lighting (a dark palette that looks right in a Blender rig
can render black in the app; pier-1's values are calibrated).

### 2.6 Night state (required)

Restrained composition: **hero glow = the monitor clerestory** — two long thin
`Toy_glassl_Glow` strips running the shed's length, which is what makes a working pier
read alive from the aerial night camera. Supporting accent: a warm glow transom band over
the arch entry (inside the archivolt, above the door) and the two pedestrian-door lights.
Day colors of glow materials must match their non-glow neighbours (`_Glow` base colour IS
the night look — do not darken it for day, see the glow memory rules). No apron
floodlights, no outline glow.

### 2.7 Height table (model targets)

| Element | Height above water |
|---|---|
| Deck top | 2.0 m |
| Deck soffit | ~1.45 m |
| Shed eave | 11.8 m |
| Shed roof at monitor base | 13.0 m |
| Monitor top | 14.8 m |
| Bulkhead wing parapet | 11.5 m |
| Arch crown (opening) | ~12.0 m |
| Attic band / "PIER 19" | 13.5–14.5 m |
| **Gabled-parapet crest cap (bbox top)** | **17.0 m** |
| Flagpole (real, NOT modeled to height) | 19.5–20.4 m |

### 2.8 Recognition cues (ranked)

1. The gabled bulkhead pavilion with the monumental arch and "PIER 19" lettering
2. The continuous monitor running the full 195 m of the shed roof
3. The long low scored-concrete shed between Pier 17 and Pier 23, plainest of the row
4. The fendered pile deck with narrow aprons and an open head apron with bitts
5. The Art Deco pilaster peaks on the bay-end elevation

### 2.13 Integration notes (Case B)

- **Registry entry** (`pipeline/lib/landmarks.mjs`): id `pier19`, name "Pier 19",
  lon/lat at the anchor, `height: 15.0` (crest above deck — the registry height is the
  procedural-block height above ground; the manifest `targetHeightM 17.0` is the model's
  vertical extent from the water, a different quantity — same distinction Pier 1
  documents).
- **Exclusion**: the bake carries the pier as the **merged DataSF ring** (Pier 19 shed +
  Pier 23 shed + connector, 21,598 m², ~11 m) plus whatever Overture traces here —
  check the actual bake inputs at integration time; Overture often adds a twin or a comb
  (Pier 1 precedent). The merged ring's centroid is ~96 m from the anchor and its nearest
  vertices ~75 m, while keepers (Pier 17's ring to the south, the Pier 23 Cafe block to
  the north) need measuring against the same inputs before choosing between one radius
  and the `exclude`-small + `extraExclusions` pattern Pier 1 used. **Do not size the
  radius from the half-diagonal rule** — measure vertices AND centroids of every ring
  within ~700 m against the committed tiles, both tiers.
- **Collateral, stated plainly**: dropping the merged ring removes Pier 23's shed and the
  connector too. There is no radius that avoids this — one polygon traces all three
  (same situation as Pier 1/Pier 3, resolved the same way). The result is a temporary
  hole where Pier 23 stood; **shipping Pier 23 as a landmark is the only real fix** and
  should be queued next for this stretch of waterfront.
- **Camera**: app yaw = 180 − true bearing. Eye from the south-southwest reads the
  pavilion, the south flank and the monitor at once: `camera: { distance: 700, yaw: 330,
  pitch: 22 }` (eye bearing ~210°) — verify against a shipped neighbour before committing
  (street-side memory rule).
- **loadRadius**: 2500 (default rule; 17 m × 30 = 510 < 2500).
- **Streaming**: standard batched landmark; ~241 × 189 m bbox is large but Pier 1
  (215 × 185) already ships this way.

### 2.15 Risks

1. **The flagpole trap**: normalizing the model to the LiDAR max (19.5 m) would shrink
   every wall by ~13%. The crest is 17.0 m; the pole is excluded. (Same trap Pier 3
   documents for its flagpole.)
2. **Merged footprint**: neither OSM nor DataSF has a Pier 19-only polygon; anyone
   re-measuring must use the south finger + BSHC dims, not the merged ring's OBB
   (257 × 153 m — that is three structures).
3. **North side finish**: in reality the connector hides Pier 19's north wall and north
   bulkhead wing. Model them finished and plain; when a `pier-23` asset ships the seam
   will read as the slip it historically was. Do not model any part of the connector.
4. **Roof color drift**: photos 2011–2017 contradict current imagery; follow current
   (pale grey, buff-weathered) in toy terms.
5. **Two coincident-face traps** from the repo's memory: no glow shells over solids (use
   opaque pane + thin proud glow plate), and no coincident roof faces (Cycles renders
   the unlit interior black).

### 2.16 Height derivation

- Deck: `gnd_mediancm 203` over the merged ring → 2.03 m; rounded 2.0.
- Roof field: `hgt_majoritycm 1096` (+2.03) → 13.0 m; `hgt_mediancm 1014` → 12.2 m. The
  spread 12.2–13.0 is the two low-pitch planes; eave modeled 11.8, monitor top 14.8
  (proportioned from the Coit Tower photo; the monitor rises ~1.5–2 m over the field).
- Crest: `hgt_maxcm 1751` → 19.54 m and `peak_1st_m 20.45` differ by 0.9 m at the same
  location — the flagpole signature (max = pole/ball, peak = first return off the tip).
  The masonry crest scales from the 2012 frontal photo: gable peak ≈ 1.35 × the wing
  parapet (11.5 m − 3.0 m grade = 8.5 m above sidewalk → peak ~14.0 m above sidewalk
  ≈ 17.0 m above water). ±1 m, *inferred*; re-verify from the photo during the build.
