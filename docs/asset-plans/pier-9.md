# Pier 9 — SF-SIM asset plan

**Pier 9**, The Embarcadero at Vallejo Street (94111) — a 1936–1938 reinforced-concrete
finger pier in the **Port of San Francisco Embarcadero Historic District** (NRHP #06000372,
contributing building), built as a near-identical twin of Pier 19 under Chief Engineer
Frank G. White. A classical stucco **bulkhead building** with a monumental arched entry and
raised-metal **`PIER 9`** lettering fronts the Embarcadero; behind it a **steel-framed
transit shed with scored precast concrete walls** runs 254 m north-east into the Bay under a
dark built-up roof that rises to a **continuous full-length glazed monitor**. The pier end
carries the **San Francisco Bar Pilots station** (renovated 1992, David Baker Architects)
with its lookout and mast cluster; the south apron berths tugboats; WETA berths vessels here
too. From 2013 to 2021 the south aisle housed Autodesk's Pier 9 digital-fabrication
workshop (Lundberg Design).

This is the third pier in the landmark set. It inherits the conventions proven by
`pier-1` and `pier-3`, and differs from both in ways that matter:

1. **Deck-top origin, like Pier 1, not water-datum like Pier 3.** The app's DEM carries
   Pier 9 as a ~2.4–2.5 m ridge along its centreline (sampled directly from
   `app/public/tiles/terrain.bin`), dying to 0 at the outer ~20 m. The origin sits at
   deck-top level with fascia and pile stubs reaching below z = 0. See 2.3.
2. **The roof is dark.** Pier 1 ships a pale membrane roof; Pier 9's six-ply built-up
   roofing reads near-black in every aerial. The dark shallow-gable roof with its pale
   glazed monitor spine is the identity from above — do not "correct" it to pale.
3. **The shed is offset south.** The deck is ~49 m wide but the shed's centreline sits
   ~2.6 m south of the pier axis: a ~10 m working apron on the north flank (cluttered
   with containers), ~4 m on the south. The asymmetry is real and measured.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/pier-9/`. Part 1 is the runnable task prompt, Part 2 the dossier behind it.

| | |
|---|---|
| Manifest id | `pier-9` (registry id `pier9`) |
| Existing procedural builder | none — new landmark, **Case B** (registry entry + tile re-bake; the exclusion is solved and verified in 2.13) |
| WGS84 anchor | `-122.3967912, 37.8006745` (model bbox centre) |
| Target height | **17.6 m** — the model's total **vertical extent** (pile-stub bottom −2.6 m to bulkhead attic crest +15.0 m above the pier deck), *not* a height above water. See 2.1 and 2.3 |
| Footprint | Building 254.3 m × 49.3 m OBB (OSM way 25478417 ✕ DataSF `ynuv-fyni` area_id 77 agree to 0.7 m); deck ≈ same width as the bulkhead |
| Axis heading | Long axis bears **054.6°**; the Embarcadero facade faces **234.6°** |
| Triangle cap | 24,000 |
| Category | `3` (office) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Pier 9 GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Pier 9, The Embarcadero at Vallejo Street,
San Francisco** and deliver it as a downloadable, validated GLB.

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
7. `docs/asset-plans/pier-1.md` — the pier precedent: deck-top origin, vertical-extent
   `targetHeightM`, true-heading authoring, pile stubs, apron furniture. Pier 9 follows
   its conventions exactly; the two must still not read as siblings (Pier 1 is a cream
   Beaux-Arts shed with a pale roof; Pier 9 is a 1930s working pier with a dark roof and
   a monitor spine).
8. `docs/asset-plans/pier-3.md` §2.15 — the flagpole trap. Pier 9's real flagpole tops
   the composition ~3 m above the attic crest; model it short or not at all.
9. `docs/asset-plans/pier-9.md` — this plan, whose dossier is your research starting
   point, not a substitute for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository and integration rules.

## Must capture

- The **bulkhead frontispiece**: a broad central pavilion with two monumental banded
  piers flanking a **semicircular arch ~9.8 m wide** (moulded archivolt, keystone), the
  incised-band **`PIER 9`** title above the arch, a **low gabled parapet** with small
  corner pylons, and a small attic block at the apex (crest 15.0 m). This is cue #1.
- The **one-storey classical wings** either side, of unequal width (the south wing is
  longer): pale stucco, panel-scored, with large multi-pane steel-sash windows in
  moulded surrounds and a plain parapet at ~8.5 m.
- The **254 m transit shed** behind: scored precast concrete walls (grey, not cream),
  regular pilaster/panel rhythm with steel-sash window bands and roll-up doors, eaves
  ~7.3 m, and a **shallow-gable dark roof rising to a continuous glazed monitor**
  (top ~10.3 m) that runs the full length. The monitor is the identity from above.
- The **dark roof, honestly dark**: near-black built-up roofing, with a crowd of pale
  grey rooftop mechanical units along the south plane (the Autodesk-era plant) and a
  cleaner north plane. Style bible §10: the camera looks down; this roof is 60 % of the
  asset's pixels and must be designed, not extruded.
- The **east (bay-end) elevation**, faintly Art Deco: six profiled pilasters rising to
  peaks just above the roofline and a gabled central pavilion (NRHP nomination). The
  **Bar Pilots station** occupies the pier end with a small lookout volume and mast
  cluster rising above the shed roof, and an annex widening the last ~8 m of the north
  side.
- The **asymmetric working aprons**: ~10 m north (with a run of freight containers —
  they are semi-permanent and belong), ~4 m south. Rail-spur score lines survive in the
  asphalt on both aprons. Fender piles, bollards, mooring bitts at the end, lamp
  standards.
- The **pier itself**: deck slab with fascia, a suggestion of pile bents below deck
  level, guard railing. Without the deck the building floats.

## Research Pier 9 independently

Verify the dossier rather than trusting it. Re-check at minimum the crest height, the
footprint decomposition, the anchor, the deck datum, and the orientation. Gather
references covering all four sides, the roof, and day/night appearance.

Primary documents: the Port of San Francisco Embarcadero Historic District National
Register nomination Section 7 (Pier 9 entry, pages 135–137 —
`sfport.com/files/2022-12/EmbarcaderoRegisterNominationSec7.pdf`), the Port's Pier 9
lease and retrofit documents, David Baker Architects' Bar Pilots project page, and
Lundberg Design / press coverage of the Autodesk workshop.

**Source traps already known and resolved in 2.1 — re-check, do not re-inherit:**

1. OSM `height=8` on way 25478417 is the shed's eaves figure and is **not** the crest.
   The crest is the bulkhead attic block at ~15.0 m above deck.
2. The DataSF LiDAR record (`ynuv-fyni` area_id 77) reports `hgt_maxcm = 1550` over a
   `gnd_mediancm = 390` that is partly water-contaminated; its `p2010_zmaxn88ft = 59.686`
   (18.19 m NAVD88) minus the ~3.1 m NAVD88 promenade gives the same ~15.0 m crest. The
   twin record for Pier 19 (`SF9900019H`, zmax 18.76 m NAVD88) corroborates it. Treat
   `hgt_max` alone as flagpole-contaminated (`sf3d-lidar-max-is-a-flagpole`).
3. "Pier 9" before 1918 was a different pier — today's Pier 7 was "old Pier 9" until the
   numbering changed, and the present Pier 9 site held Pier 11 (demolished 1935). Any
   pre-1936 photo captioned "Pier 9" shows the wrong building.
4. David Baker Architects date the Bar Pilots' shed "circa 1932"; the NRHP nomination
   dates the whole pier 1936–1938 from the construction contracts (Barrett & Hilp,
   completed 25 April 1938). Prefer the nomination; state both.

## Create a reference dossier

Write `artifacts/pier-9/REFERENCE.md`: source links and what each establishes; verified
dimensions; orientation; observations from all four sides and above; the 3–5 strongest
recognition cues; features to preserve; features to simplify; uncertainties. Do not
commit copyrighted full-resolution imagery.

## Make your own design decisions

Follow `docs/styles/miniature-toy.md` §22. This is a **hero-adjacent landmark**: a
National Register working pier, not a monument. Spend the budget on the frontispiece,
the monitor spine, the roof plant, the Bar Pilots end and the deck edge. The failure
mode is a beautiful arch on a featureless dark noodle — the shed is most of the pixels
and must be designed. The second failure mode is prettifying a working pier: no
planting, no plaza, no invented colour. Its beauty is the discipline of grey, cream and
near-black with one pale glowing arch.

## Scope of the exported asset

Export the pier: deck slab with fascia and pile stubs, aprons with rail score lines,
railing, bollards, mooring bitts, lamp standards, the container run on the north apron,
the bulkhead building, the transit shed with monitor, rooftop plant, the Bar Pilots
station volumes and short masts, and the bay-end elevation.

**Do not include**: the Embarcadero roadway, Herb Caen Way, palms, the seawall
promenade, Pier 7 (Waterfront Restaurant remnant or the 1990s recreational Pier 7),
Pier 15, the water surface, moored vessels (tugs, WETA ferries, pilot boats — the app
has a live-vessel layer), parked cars, people, plinths, cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. Binary `.glb`; real meters;
applied transforms; no negative scales; outward normals; no textures; no transparency;
flat `Toy_*` materials; `_Glow` only on night surfaces; no `Toy_body`; no
cameras/lights/animation; at most 24,000 triangles.

**Origin — deck-top rule (Pier 1 precedent, read plan 2.3).** Origin at pier-deck top,
centred on the model's XY bounding box; geometry extends below z = 0 (fascia and pile
stubs to −2.6 m). The loader seats the origin on the terrain sample at the anchor
(~2.5 m DEM ridge); at the tip, where the DEM falls to 0, the pier correctly stands out
of the water on its piles.

**Orientation:** author with Blender `+Y` = true north, `+X` = east. The long axis
bears **054.6°**; the Embarcadero facade faces **234.6°**. Build on the measured
footprint in 2.3 — never model axis-aligned and rotate by eye.

**Height normalization:** total vertical extent (pile-stub bottom to attic crest) must
land at exactly **17.6 m** so the loader's scale is 1.0. Record in `REPORT.md`, in
bold, that `targetHeightM` is a vertical extent, not a height above water. The real
flagpole would add ~3 m — model it short (top below +15.0) or omit it (pier-3 §2.15).

## Reproducible Blender workflow

Blender 5.2 LTS, headless. Keep `artifacts/pier-9/build_pier_9.py` (deterministic),
`artifacts/pier-9/pier-9.blend`, `artifacts/pier-9/pier-9.glb`.

## Required review renders

`pier-9-top.png`, `pier-9-north.png`, `pier-9-east.png`, `pier-9-south.png`,
`pier-9-west.png`, `pier-9-contact-sheet.png`, a high three-quarter aerial
`pier-9-aerial.png` from the **south-west** (frontispiece + south flank + full roof in
frame), a second aerial from the **north-east** (the Bar Pilots end and the monitor
running away toward the city), and `pier-9-aerial-night.png`.

Elevations share scale/framing/projection; render the long faces at a long aspect
(e.g. 3200×600). The top view must show the monitor, the dark roof planes, the south
plant run, the container line and the aprons legibly.

**Night render:** copy `Base Color` into `Emission Color` at strength 1.0 on `_Glow`
materials of the re-imported GLB (`docs/asset-plans/README.md`, "Night renders").

## Validate the exported GLB

Re-import into a fresh scene and validate the re-import. Write
`artifacts/pier-9/validation.json` and `REPORT.md`. Two expected results that are
**not** failures and must be stated as such:

- **min Z ≈ −2.6 m, not 0** — the deck-top origin rule (plan 2.3).
- The axis-aligned XY bbox will be roughly **215 × 175 m** despite the pier being
  254 × 49 m — the consequence of the 54.6° heading, not a scale error.

## Manifest draft

Include in `REPORT.md`; do not edit the production manifest in this task.

```json
{
  "id": "pier-9",
  "file": "pier-9.glb",
  "anchor": [-122.3967912, 37.8006745],
  "targetHeightM": 17.6,
  "cat": 3,
  "name": "Pier 9",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit `app/public/sf-assets/landmarks_manifest.json`, `pipeline/lib/landmarks.mjs`
or app code in this task. Integration is a separate job — `INTEGRATION-PROMPT.md` plus
the solved exclusion in `docs/asset-plans/pier-9.md` §2.13, which must not be re-derived
by the half-diagonal rule.
````

---

## Part 2 — Research and design dossier

Compiled 19 August 2026. Values marked *measured* were computed in this session from the
named dataset and are reproducible from 2.3; *photogrammetric* values come from the pixel
solve described in 2.16; everything else is labelled.

### 2.1 Verified facts

| Fact | Value | Confidence / source |
|---|---|---|
| Name | Pier 9 | NRHP #06000372, contributing building ("Pier 9 (Ferryboat Klamath)", The Embarcadero at Vallejo St) |
| Built | **1936–1938**: substructure by A. W. Kitchen (17 Oct 1936 – 13 Jan 1938, $408,783.89); shed + bulkhead by Barrett & Hilp (6 Nov 1936 – 25 Apr 1938, $274,149.60). Bulkhead-wharf substructure under the bulkhead building is **1917** (Clinton Construction) | NRHP nomination Sec. 7 pp. 135–137 |
| Designers | Substructure/shed plans: **G. A. Wood** in charge; bulkhead building: **H. B. Fisher** in charge; both under **Frank G. White**, Chief Engineer, BSHC | NRHP nomination |
| Twin | **Pier 19**, "identical in design and dimensions" (built same contracts); 153 ft wide × 800 ft long as constructed | NRHP nomination |
| Prior structures | Site held **Pier 11** (1890s, demolished 1935); "Pier 9" pre-1918 was today's Pier 7 | NRHP nomination; sfinfilm.com citing Corbett, *Port City* |
| Transit shed | Steel frame; **scored precast concrete walls** (poured-in-place at the Embarcadero bays, scored to match); roll-up metal doors in all three walls (two south doors enlarged 1970); steel sash + wire glass; redwood roof sheathing, six-ply built-up roofing; **roof rises to a monitor running continuously the full length**; interior in three aisles | NRHP nomination |
| East (bay-end) elevation | "Faintly Art Deco … six profiled piers rising to peaks just slightly above the roofline and a gabled central pavilion that rises to a flagpole" | NRHP nomination |
| Bulkhead building | Timber-framed, stucco; classical detailing; broad central pavilion, monumental arched entry, monumental flanking piers, **gabled parapet**; wings of **unequal width**; steel-sash windows; `PIER 9` in **raised metal letters** over the arch; cast-iron wheel guards; flagpole tops the composition | NRHP nomination |
| Aprons | Rail spur each side (south flush, north originally depressed), outlines still visible under asphalt; mooring bitts at the pier end, cleats along the sides, fender piles on the perimeter | NRHP nomination |
| Tenants | **SF Bar Pilots** (station house at the pier end, renovated **1992**, David Baker Architects, 19,560 sf; lease incl. ~19.7k sf office, ~20.1k sf shed, ~14.3k sf apron); **WETA** berths; **Autodesk Pier 9 Workshop** 2013–2021, south aisle, Lundberg Design; assorted maritime/law offices | dbarchitect.com; Port Commission memo 2006-10-18; constructiondive.com; knowlesarchitect.com |
| Building footprint | **254.3 m × 49.3 m** OBB; polygon area 9,268 m²; OSM way 25478417 and DataSF area_id 77 agree to < 0.7 m | *measured* (both datasets reprojected) |
| Massing decomposition | Bulkhead: along −127.5…−116.5 (11 m deep) × full 49.3 m width; shed head −116.5…−91 (~41 m wide, tapering); main shed −91…+126.8, north wall at perp −14.5…−15.3, south wall +19.5…+20.3 (**≈ 34.5 m wide, centreline offset +2.6 m south**); Bar Pilots annex widens the north side to −19.9 for the last ~8 m | *measured* (DataSF ring in pier frame, 2.3) |
| Aprons (today) | North ≈ 10 m (container-cluttered), south ≈ 4 m | *measured* (ring vs deck edge on rectified z19 ortho) |
| Heading | Long axis **054.59°**; frontage faces **234.59°** | *measured* (min-area OBB) |
| Anchor (OBB centre) | `-122.3967912, 37.8006745` | *measured* |
| Deck datum | App DEM ridge **2.4–2.5 m** along the centreline, → 0 beyond along ≈ +110; anchor sample **2.50 m**. Real promenade ≈ 3.1 m NAVD88 | *measured* (`terrain.bin` sampled directly) |
| Bulkhead attic crest | **15.0 m above deck** | *photogrammetric* (2.16), corroborated by p2010 zmax 18.19 m NAVD88 − 3.1 m promenade = 15.1, and twin Pier 19 zmax 18.76 |
| Pavilion gable apex | ~13.7 m | *photogrammetric* |
| Wing parapet | ~8.5 m | *photogrammetric* (±0.8) |
| Arch | opening ≈ 9.8 m wide; springing ≈ 3.4 m; intrados crown ≈ 8.3 m; archivolt crown ≈ 9.5 m | *photogrammetric* |
| Shed eaves | ~7.3 m (OSM `height=8` ≈ this figure; LiDAR `hgt_median` 8.14 mixes planes and monitor) | *inferred* |
| Monitor | ~9 m wide, top ~10.3 m, centred on the **shed** axis (perp +2.6), continuous full length | *inferred* from nadir ortho + Coit Tower aerial |
| Roof colour | Near-black built-up roofing; pale grey plant crowd on the south plane; cleaner north plane | *observed* (Commons aerial, Esri z19) |
| Flagpole | Real pole tops the composition ~+3 m above crest — **model short or omit** | *observed*; pier-3 §2.15 trap |

### 2.2 Sources

- **NRHP #06000372 nomination, Section 7** (January 2006, Michael Corbett) —
  `https://www.sfport.com/files/2022-12/EmbarcaderoRegisterNominationSec7.pdf`, Pier 9
  entry pp. 135–137 plus bulkhead-wharf Section 6 pp. 45–48. **The best single source**:
  dates, contracts, designers, structure, both elevations, aprons.
- **NoeHill district table** — `https://noehill.com/sf/landmarks/nat2006000372.aspx` —
  "Pier 9 (Ferryboat Klamath), The Embarcadero at Vallejo Street", contributing.
- **David Baker Architects** — `https://www.dbarchitect.com/projects/san-francisco-bar-pilots`
  — Bar Pilots Station House at the end of Pier 9, 1992, 19,560 sf, "building within a
  building", exposed steel trusses/steel sash.
- **Port Commission memo, 18 Oct 2006** — Bar Pilots lease areas (office/shed/apron).
- **Port of SF WRP012 one-pager (2022)** — Pier 9 Bulkhead Wall & Wharf Substructure
  Earthquake Safety Retrofit; Bar Pilots + WETA berth vessels here.
- **Construction Dive / Metropolis / Knowles Architect / Lundberg Design** — the Autodesk
  Pier 9 Workshop (2013–2021), 35,000 sf, south side, tugboat berthing alongside.
- **Wikimedia Commons, Category:Pier 9 (San Francisco)** — head-on facade photo
  (`Pier 9, San Francisco.JPG`), night arch photo (`San Francisco Pier 9.jpeg`), and the
  Coit Tower aerial (`Pier 9 and Pier 15 with construction crane - San Francisco.JPG`)
  that establishes the dark roof, monitor, south-plane plant, container run and the Bar
  Pilots end. *Observed.*
- **Esri World Imagery z19**, resampled into a pier-frame ortho at 0.33 m/px — apron
  widths, monitor position, deck edges. *Measured.* (The Google keyless Street View tile
  endpoints returned 403 this session; the facade solve in 2.16 uses the Commons head-on
  photo instead.)
- **DataSF `ynuv-fyni`** records `SF9900009` (Pier 9) and `SF9900019H` (Pier 19 twin).
- **OSM way 25478417**; Overpass confirms no separate `man_made=pier` deck polygon.

### 2.3 Orientation, placement, and the deck datum

Pier frame used throughout: **along** runs north-east on bearing 054.59°, zero at the
model bbox centre (= the anchor), negative toward the Embarcadero; **perp** runs 90°
clockwise (positive south-east). The building spans along −127.5…+126.8, perp
−24.3…+25.3.

DataSF ring (area_id 77) reduced to massing, in `(along, perp)` metres:

```
bulkhead      along −127.5 … −116.5   perp −23.8 … +25.3   (the 1917 wharf strip)
shed head     along −116.5 … −91      perp −20.3 … ~+21    (tapering on the south)
main shed     along  −91   … +126.8   perp −14.5 … +20.3   (north wall drifts −14.5→−15.3)
end annex     along +118.5 … +126.8   perp −19.9 … −14.5   (Bar Pilots, north side)
```

Deck edges (rectified ortho): north ≈ perp −25, south ≈ perp +23.5 → **north apron
≈ 10 m, south apron ≈ 4 m** beside the main shed.

**The deck datum.** Sampling the app's own `terrain.bin` across the site:

```
along    −140  −120  −100   −60   −20    20    60   100   120   140
centre    3.4   2.4   2.4   2.5   2.4   2.5   2.4   2.3   1.0   0.0
edges     3.3   2.2   0.5   0.1   0.2   0.1   0.1   0.1   0.3   0.0
```

The DEM carries the pier as a ~2.4–2.5 m centreline ridge with water either side,
falling to 0 past along ≈ +110. Exactly Pier 1's situation, so its rule applies
verbatim: **author with local z = 0 at the top of the pier deck**; deck slab, fascia
and pile stubs run down to **z = −2.6 m**; `targetHeightM = 17.6` is the vertical
extent −2.6 … +15.0. Placed at the anchor the deck lands at ~2.5 m world; at the tip,
where the DEM has fallen to 0, the pier reads as standing out of the water on piles —
which is where the sub-deck geometry earns its triangles. `min Z ≈ −2.6` is a **PASS**
and `validation.json` must say so. The bulkhead end sits over terrain of ~2.7–3.4 m, so
its plinth is buried by up to ~0.9 m at the Embarcadero corner — buried, not floating,
and the plinth must absorb it.

`yawDeg` is not used: author in true-world orientation, `+Y` north.

### 2.4 What each side shows

**South-west — the Embarcadero facade (234.6°).** A long one-storey pale stucco wall in
five parts: two flat-parapet wings of unequal width (south wing longer), then the broad
central pavilion. The pavilion: two monumental **banded/rusticated piers** flanking a
**semicircular arch** (~9.8 m opening) with a moulded archivolt and keystone; above the
arch a plain band carries **`PIER 9`** (raised metal letters, read dark against the
stucco); over that a **low gable** with raking cornice, small flat-topped pylons at its
shoulders, and a small attic block at the apex (crest 15.0 m) carrying the flagpole.
The arch is filled with a glazed steel screen (replacement) and a roll-up shutter; the
opening runs straight through to the shed so daylight shows in it. Wings: large
multi-pane steel-sash windows (roughly square, heads ~5.5 m) in moulded surrounds,
wood doors with upper lights, tenant signboards. Cast-iron wheel guards flank the arch
at grade.

**North-west flank — the slip toward Pier 15.** ~10 m of working apron under the shed's
grey precast wall: pilaster/panel rhythm, high steel-sash window band, roll-up doors, a
long run of **freight containers** parked against the wall (semi-permanent, model a
restrained run), rail-spur score lines in the asphalt, fender piles and bollards at the
edge. Ferries (WETA / Blue & Gold) berth here — not in the GLB.

**South-east flank — the slip toward Pier 7.** The same shed grammar with only ~4 m of
apron; tugboats berth along here (not in the GLB). The two enlarged 1970 roll-up doors
are on this side. Lamp standards down the apron.

**North-east — the Bay end.** The shed's end elevation, faintly Art Deco: **six
profiled pilasters rising to peaks just above the roofline**, a **gabled central
pavilion** with a short pole, roll-up doors at deck level. The **Bar Pilots station**
reads here: a small lookout volume above the shed roofline at the north corner, masts
and antennas (model short, below the bulkhead crest), the annex bay widening the north
side, mooring bitts on the end apron.

**Above.** The identity view. Near-black shallow-gable roof planes rising to the
**pale-framed continuous monitor** (glazed both sides, dark cap) running the full
length on the shed's centreline (perp +2.6, not the pier's). The south plane carries a
crowd of pale grey mechanical units and vents concentrated mid-pier; the north plane is
cleaner with a few boxes and patches. The bulkhead's lower flat roof wraps the shed
head, with the gable and attic block breaking through at the frontage. The aprons read
as asphalt-grey bands with the container run (north), the rail score lines, and the
fendered edge all the way round.

### 2.5 Recognition cues (ranked)

1. **The gabled frontispiece** — banded piers, big arch, `PIER 9`, low gable + pylons.
   Distinct from Pier 1's pedimented Beaux-Arts pavilion two blocks south.
2. **The dark roof with the pale monitor spine** — 254 m of near-black roof split by one
   continuous glazed monitor. No other Embarcadero pier reads like this from above.
3. **Length at 54.6°** — the second-longest non-bridge footprint in the set, parallel to
   Piers 1/3 but further out into deeper blue.
4. **The working clutter** — containers on the north apron, plant on the south roof
   plane, the Bar Pilots lookout and masts at the tip. This pier is *used*, and the
   miniature should say so.
5. **The grey/cream two-tone discipline** — cream stucco bulkhead, grey concrete shed,
   near-black roof. No third colour anywhere.

### 2.6 Miniature translation

- **Enlarge the arch** to ~1.15× width and deepen the archivolt so the frontispiece
  survives at thumbnail size; extrude the `PIER 9` letters (raised metal in reality —
  extrusion is honest here).
- **Exaggerate the monitor's contrast**: pale frame + glazing against the near-black
  planes, slightly proud, so the spine reads from the app's camera. Do not widen it
  past ~9.5 m.
- **Compress the shed bays**: model a repeating unit (~7.5 m pitch implied by the
  panel rhythm) and use ~20 per flank. A scored grid in one recessed plane is the
  whole window.
- **Curate the roof plant**: 8–12 confident grey boxes clustered on the south plane
  mid-pier, 2–3 on the north, never uniform. The real crowd is bigger; the miniature
  wants clusters, not confetti.
- **Containers as apron furniture**: 5–7 boxes in a broken run on the north apron, in
  2–3 restrained colours (rust, navy, steel). They are the "small clusters of life".
- **Bar Pilots end**: one lookout volume + annex + two short masts. The masts stay
  below +15.0 (the crest) — they must not become the bounding-box top.
- **Do not prettify.** No planting, no plaza furniture, no awnings. The asphalt, the
  score lines and the fender rhythm are the ornament.

### 2.7 Massing recipe

Local frame: `u` = along (NE), `v` = perp (SE), `w` = up from deck top. Origin at the
bbox centre in u/v.

1. **Deck slab** — the full outline u −127.5…+126.8, v −25…+23.5; top w = 0, fascia to
   −1.2, chamfered edge; rounded tip corners (r ≈ 3 m).
2. **Pile bents** — square stubs w −1.2…−2.6 on ~9 m centres: perimeter row plus two
   internal rows under the outer 40 m (where the DEM shows water).
3. **Bulkhead slab** — u −127.5…−116.5, v −23.8…+25.3, w 0…8.5 with 0.3 m coping;
   plinth 0…1.2 m slightly proud (absorbs the ~0.9 m burial at the shore corner).
4. **Central pavilion** — centred on the arch axis (v ≈ +0.7), ~19 m wide, projecting
   ~0.6 m, banded piers ~3 m wide at its corners (4–5 horizontal score bands), cornice
   at 10.0, **gable** raking to apex 13.7 with 0.35 m raking cornice, shoulder pylons
   (flat-topped, ~11.2), **attic block** ~3.2 × 1.6 m from 13.7 to **15.0** (sets the
   bbox top), short flagpole ≤ 14.9 if modelled.
5. **The arch** — semicircular, 11.3 m span post-exaggeration, springing 3.4, intrados
   crown ~9.0, cut ~0.5 m into the pavilion; archivolt ring 0.8 m wide, 0.2 m proud,
   keystone block; reveal dark; fill = recessed glazed screen (`Toy_glass`) with a
   `Toy_steel` mullion grid and a lettering band above; `PIER 9` extruded letters
   (~0.9 m tall) on the band over the arch.
6. **Wings** — north wing u/v per 2.3 (shorter), south wing longer; parapet 8.5;
   window units: moulded surround, recessed `Toy_glass` panel with scored sash grid,
   heads 5.5, sills 1.5; doors between. 3 windows north wing, 4 south wing.
7. **Shed head** — u −116.5…−91, v −20.3…+21 (lofted taper on the south), w 0…7.3,
   flat parapet; its roof a low dark plane at 7.3 wrapping into the main gable.
8. **Main shed** — u −91…+126.8, v −14.5…+20.3, walls w 0…7.3: pilaster strips 0.5 m
   wide 0.08 proud at ~7.5 m pitch, high window band (recessed, 4.2…6.6), roll-up door
   panels (scored, `Toy_steel`) at deck level every 4th bay, plinth 0…0.8. Belt course
   at 3.8.
9. **Roof** — shallow gable from eaves 7.3 rising to the monitor: **monitor** centred
   at v +2.9, 9 m wide, vertical glazed sides (w 8.9…10.0, `Toy_glassl` over
   `Toy_steel` frame), dark cap at 10.3. Roof planes `Toy_roofd` (near-black — correct
   here). South plane: 8–12 grey plant boxes (1.5–3 m, w +0.8…+1.6) clustered
   u −40…+60; north plane: 2–3 boxes. Bulkhead flat roof at 8.5 slightly lighter.
10. **Bay end (u +126.8)** — six profiled pilasters rising to small peaks ~7.8 (0.5
    above the eaves), gabled centre pavilion to ~9.0 with short pole (≤ 12), roll-up
    doors below; **Bar Pilots**: annex block u +118.5…+126.8, v −19.9…−14.5, w 0…6.5;
    lookout volume ~6 × 5 m rising to ~11.5 at the north corner with a wrap of
    `Toy_glassl` glazing; two masts to ≤ 14.5.
11. **Aprons** — asphalt field (`Toy_ink`-adjacent dark grey) inset from the deck edge;
    rail score lines as shallow 0.05 grooves running the length of both aprons;
    **containers**: 5–7 boxes 6.1 × 2.4 × 2.6 on the north apron u −60…+80, broken
    run; bollards ~12 m pitch; mooring bitts at the end; lamp standards 5.5 m at
    ~24 m pitch on the south apron and the end; guard railing (top rail + posts at
    3 m centres, no balusters) around the perimeter.

### 2.8 Materials and palette

| Surface | Material | Hex | Note |
|---|---|---|---|
| Bulkhead walls, pavilion, wings, parapets | `Toy_cream` | `f2ede3` | the frontage colour |
| Pavilion trim: archivolt, keystone, cornices, attic, `PIER 9` letters | `Toy_white` | `f7f4ec` | a half-step brighter |
| Shed walls, pilasters, end pilasters, bulkhead plinth | `Toy_stone` | `d9d2c2` | scored precast grey |
| Deck slab, apron field | `Toy_steel` | `9aa0a6` | asphalt-grey; keep clearly darker than the shed walls |
| Deck fascia, pile stubs, fender line, bollards, lamp poles | `Toy_ink` | `3a3530` | grounds the pier |
| Roof planes (both), monitor cap | `Toy_roofd` | `45454a` | near-black — **correct for this roof**; see risk 4 |
| Monitor frame, plant boxes, roll-up doors, railing | `Toy_steel` | `9aa0a6` | |
| Glazing (wings, shed band, arch screen) | `Toy_glass` | `2a4d73` | graphical, opaque, recessed |
| Monitor glazing, Bar Pilots lookout glazing | `Toy_glassl` | `6f95b8` | up-facing / pale |
| Containers | `Toy_rust` `a86444`, `Toy_navy` `2c4a70`, `Toy_steel` | | 2–3 colours max |
| Arch screen at night | `Toy_glass_Glow` | warm-shifted pale, see 2.9 | hero |
| Monitor, partial run | `Toy_glassl_Glow` | | supporting |
| Bar Pilots lookout | `Toy_glassl_Glow` | | supporting (pilots work nights) |
| Apron lamps | `Toy_amber_Glow` | `e8b563` | accent points |

Glow shells must be **open shells proud of the opaque geometry**, never closed boxes —
a closed glow shell reads as two alpha layers (~23 %) by day and tints the facade
(`sf3d-glow-shell-day-alpha`). A `_Glow` material's **base colour is its night look**
(`sf3d-glow-colour-is-unlit`): author glow colours as the colour to *see* at night.

### 2.9 Night state

- **Hero:** the arch screen — one warm pale glow filling the arch (a lit gateway, the
  night photo in Commons shows exactly this). The `PIER 9` letters do **not** glow
  (raised metal, not a sign — pier-3's rule).
- **Supporting:** a **partial, scattered run of the monitor** — roughly a third of its
  length lit, in 2–3 separate stretches, both sides; and the **Bar Pilots lookout** at
  the tip (the pilots dispatch around the clock — the one light at the end of the dark
  pier is both true and beautiful).
- **Accent:** the apron lamp standards as small amber points drawing the pier's line
  into the bay; 4–6 lit windows scattered on the shed's south band.
- **Not lit:** the roof planes, containers, plant, deck, letters, wings (save one or
  two windows), pile stubs.

### 2.10 Scope

**In:** everything in 2.7.

**Out:** Embarcadero roadway/tracks/palms/promenade; Pier 15; the Pier 7 restaurant
remnant and the 1990s recreational Pier 7; all vessels (tugs, ferries, pilot boats, any
historic ferryboat); floating docks and camels in the slips; water; vehicles; people;
tenant signage beyond `PIER 9`; cameras; lights; plinths.

**Deliberately omitted:** the full-height flagpole (~18 m — would become the bbox top
and rescale the pier, pier-3 §2.15); the Autodesk-era interior; the WETA float.

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Deck, fascia, aprons, score lines, tip fillets | 1,400 |
| Pile stubs | 1,600 |
| Railing, bollards, bitts, lamps | 2,800 |
| Bulkhead slab, wings, windows, doors | 2,400 |
| Pavilion, arch, archivolt, gable, pylons, attic, letters | 3,600 |
| Shed solid, pilasters, window bands, roll-up doors | 4,200 |
| Roof planes, monitor, plant boxes | 2,600 |
| Bay end: pilasters, gable, Bar Pilots annex + lookout + masts | 1,800 |
| Containers | 900 |
| Glow shells | 800 |
| Slack | 1,900 |
| **Total cap** | **24,000** |

The railing is the first cut (posts to 6 m centres), the pile field second, the shed
bays third. The frontispiece is last.

### 2.12 Draft manifest entry

```json
{
  "id": "pier-9",
  "file": "pier-9.glb",
  "anchor": [-122.3967912, 37.8006745],
  "targetHeightM": 17.6,
  "cat": 3,
  "name": "Pier 9",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

`cat: 3` (office): maritime offices, law offices, the Bar Pilots' 19.7k sf of office
space, the former Autodesk workshop. `25` (transit station) is wrong — no passengers
board here. `loadRadius` 2500 is the default rule; beyond it the site is honest empty
water (pier-3's argument).

**Do not** rewrite `landmarks_manifest.json` with `JSON.stringify` — append the entry
as text (`sf3d-manifest-text-append`).

### 2.13 Integration notes — **the exclusion is solved here**

Case **B**: `pier9` exists in neither `pipeline/lib/landmarks.mjs` nor
`app/src/landmarks.js`. Registry entry:

```js
{
  id: 'pier9',
  name: 'Pier 9',
  lon: -122.3967912,
  lat: 37.8006745,
  height: 15.0,
  exclude: 80,
  extraExclusions: [
    { lon: -122.3958844, lat: 37.8013416, r: 14 },
    { lon: -122.3978390, lat: 37.8000253, r: 12 },
  ],
  camera: { distance: 450, yaw: 235, pitch: 20 },
}
```

**Why three zones.** The bake carries Pier 9 as **five** footprints, and `excluded()`
fires on centroid *or any ring vertex* inside a zone:

| Baked footprint | Tier | Top | Extent (along, perp) | What it is | min dist from anchor |
|---|---|---|---|---|---|
| `23_9#6` | buildings | 14.3 m | −127.5…+126.8, −23.9…+25.3 | the whole pier, one ring | 65.1 m |
| `23_9#1` | toy | 10.1 m | −126.9…+126.8, −23.8…+25.1 | the whole pier, toy tier | 7.7 m |
| `23_9#2` | toy | 11.6 m (base 10.1) | rooftop garnish near the tip | 109.7 m |
| `23_9#4` | toy | 11.6 m (base 10.1) | rooftop garnish near the tip | 104.3 m |
| `23_9#3` | toy | 11.6 m (base 10.1) | rooftop garnish on the bulkhead | 115.9 m |

The nearest keeper — **Pier 15, both tiers** (`22_8#13` buildings / `22_8#2` toy) — has
its nearest test point at **111.6 m**, *closer than the bulkhead garnish at 115.9 m*.
One circle cannot take all five targets without taking Pier 15. Three zones solve it:
the main 80 m zone swallows both full-pier rings; two small zones sit exactly on the
garnish clusters (tip: local `(3662.0, −3464.5)` r 14; bulkhead: `(3490.0, −3319.0)`
r 12), each far inside the pier's own footprint.

Verified this session by replaying `excluded()`'s exact test (centroid or any vertex)
against the committed tiles of both tiers over every footprint within 400 m, across
cells `22_9, 23_9, 22_8, 23_8, 24_9, 24_8, 21_9, 21_8`:

```
buildings tier: drops 1 — 23_9#6 (14.3 m)
toy tier:       drops 4 — 23_9#1 (10.1), 23_9#2, 23_9#3, 23_9#4 (garnish)
nearest keeper margin: +31.6 m (Pier 15, both tiers)
```

Nothing else, in either tier. The garnish blocks sit *on* the toy pier (base = its
top), so dropping the parent without them would leave three floating blocks — all
five must go together. Re-run the replay after the re-bake; do **not** trust
`verify-rebake`'s per-cell counts alone (`sf3d-verify-rebake-count-blindspot`).

Other integration notes:

- **No collateral.** Unlike Pier 1's merged Overture comb, every dropped ring lies
  entirely on Pier 9. The fallback drill leaves genuinely empty water over the DEM
  ridge — correct and expected for a Case B pier (pier-3 precedent).
- **Watch the Overture height-retarget side effect**
  (`sf3d-exclusion-retargets-overture-height`): after the bake, confirm Pier 15's
  heights did not change (`git diff` on `22_8`/`23_8` beyond the expected cells).
- **Shared-batch budget:** at 254 × 49 m this joins Pier 3 at the top of the plan-area
  table. Check the `BatchedMesh` reserve *before* integrating
  (`sf3d-batch-reserve-overflow`: size from GLB accessor counts).
- **Seat check:** the merge line must show a seat of ~2.5 m at the anchor (the DEM
  ridge). A seat of 0 means the anchor drifted off the ridge — move it back, never
  compensate in the model.
- **Verify at the NE tip** that the pier stands on piles out of the water (the DEM is 0
  there) — the origin decision is actually tested at the tip, not at the shore.
- `BATCH: yes` sessions still run the bake and full QA, then
  `git checkout -- app/public/tiles api/_data` before committing source only.

### 2.14 Validation checklist

- Binary GLB, real metres, applied transforms, no negative scales
- **min Z ≈ −2.6 m — expected, stated as a PASS in `validation.json` with the reason**
- XY centre offset ≈ 0 (bbox centre); vertical extent exactly **17.6 m**
- Axis-aligned XY bbox ≈ 215 × 175 m — expected at 54.6°, not a scale error
- ≤ 24,000 triangles; ≤ 500 KB after `pipeline/compress-assets.mjs`
- No textures/transparency/cameras/lights/animation; all materials `Toy_*`, no `Toy_body`
- `_Glow` only on the 2.9 surfaces; glow shells open and proud, never closed boxes
- Masts, poles and the lookout all **below +15.0** — the attic block must set the top
- Outward normals (per-object signed volume; ray residual ≤ 0.15 %)
- Fresh-scene re-import validated; day + night renders from the re-imported file
- Contact sheet: top view shows monitor, dark planes, plant, containers, aprons

### 2.15 Open questions and risks

1. **The crest (15.0 m) is photogrammetric plus LiDAR-corroborated, not published.**
   Honest range 14.3–15.6. Two independent routes agree (2.16); if a drawing surfaces,
   rebuild rather than nudging the attic.
2. **The wing parapet (8.5 m) and shed eaves (7.3 m) are the softest numbers** —
   single-photo perspective and a mixed LiDAR median respectively. An oblique aerial
   would pin both; re-measure before committing the wall heights.
3. **The monitor's height (10.3) and width (9 m) are read from nadir + one oblique.**
   Its *existence and full length* are documentary (NRHP). If it turns out lower, the
   roof loses relief but nothing rescales (the bulkhead sets the top).
4. **`Toy_roofd` reads near-black in the app** (`sf3d-toy-roofd-reads-black` measured
   rgb(9,9,12) on a deck). Here the real roof *is* near-black, so it is the honest
   choice — but check the aerial render for a "hole in the city" effect; if the roof
   vanishes into the night background, step to a very dark grey off-palette (WARN, not
   fail) rather than lightening to `Toy_ink`.
5. **The bay-end composition is described but barely photographed** — the six-pilaster
   Deco end and the Bar Pilots volumes are from the nomination text plus one distant
   aerial. Model them restrained; do not invent detail the sources cannot support.
6. **Container run and roof plant are 2015–2020 observations.** Post-Autodesk the south
   plant may have thinned. They are the right *kind* of truth for a working pier even
   if individual boxes moved; keep the clusters generic.
7. **Pier 15 stays procedural 111.6 m north.** The exclusion margin (+31.6 m) is
   comfortable, but a future Pier 15 landmark should revisit the slip as a pair.
8. **This is the first dark-roof pier.** If the app's night pass makes the monitor glow
   read as floating (dark roof invisible), add a faint eave-line accent rather than
   lightening the roof.

### 2.16 How the crest was measured

The Google keyless Street View tile endpoints returned 403 this session, so the solve
uses the Commons head-on photo (`Pier 9, San Francisco.JPG`, 1920×1440, shot from
across the Embarcadero, near-normal to the facade) with the arch itself as the scale:

A semicircular arch's crown-to-springing height equals half its opening. In the photo
the intrados spans x ≈ 810–1190 px (380 px) and the crown sits at y ≈ 690, giving a
springing line at y ≈ 880 and a scale of **38.8 px/m** (radius 190 px = 4.9 m). The
pier bases (wheel-guard line) sit at y ≈ 1010. Then: springing (1010−880)/38.8 ≈
3.4 m; intrados crown ≈ 8.3 m; archivolt crown ≈ 9.5 m; `PIER 9` band ≈ 11.6 m; gable
apex ≈ 13.7 m; attic top ≈ 15.0 m; wing parapet ≈ 9.0 m raw, ~8.5 after the small
upward-perspective correction (camera at ~1.7 m compresses upper features; the crest
numbers carry the same ±0.4 m).

Independent corroboration: DataSF `p2010_zmaxn88ft` = 59.686 ft = **18.19 m NAVD88**
over the Pier 9 polygon; the Embarcadero promenade here is ~3.1 m NAVD88, giving a
highest LiDAR return of **15.1 m above deck** — within 0.1 m of the photo solve. The
twin Pier 19 record (`SF9900019H`) returns 18.76 m NAVD88 over a similar grade,
bracketing the same crest for the identical design. `hgt_maxcm = 1550` relative to the
record's own part-water "ground" is consistent but datum-suspect and was not used.
