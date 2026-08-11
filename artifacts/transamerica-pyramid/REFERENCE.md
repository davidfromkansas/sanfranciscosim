# Transamerica Pyramid — reference dossier

Research compiled for the SF-SIM miniature landmark asset. Everything below was
re-verified for this task; where this dossier disagrees with
`docs/asset-plans/transamerica-pyramid.md` the disagreement is called out
explicitly. Facts are separated from visual inference.

## 1. Sources and what each establishes

| Source | What it establishes |
|---|---|
| [OSM way/24222973 (raw node geometry)](https://www.openstreetmap.org/api/0.6/way/24222973/full.json) | Footprint corner coordinates (measured below), `height=260`, `building:levels=48`, `roof:shape=pyramidal`, address 600 Montgomery St, two tagged `entrance=yes` nodes on the east edge |
| [Wikipedia — Transamerica Pyramid](https://en.wikipedia.org/wiki/Transamerica_Pyramid) | 853 ft (260 m) height, 48 floors, 1972, Pereira, two "wings" (elevator shaft east, stairwell + smoke tower west), "top 212 ft is the spire", hollow spire with internal stair, 18 lifts |
| [Wikidata Q216865](https://www.wikidata.org/wiki/Q216865) | 260 m height, architect, quartz cladding material |
| [CTBUH / Skyscraper Center #1409](https://www.skyscrapercenter.com/building/transamerica-pyramid/1409) | Architectural height definition (260 m), 48 floors, office use |
| [PCAD 2499 (Univ. of Washington)](https://pcad.lib.washington.edu/building/2499/) | Precast concrete panels with **white quartz aggregate**; "at the 29th floor and rising up, two **triangular buttresses** protrude from the east and west; the east buttress supports an elevator shaft, the west braces a staircase and exhaust shaft"; 3 basement levels; original 1,150 ft proposal cut by the Planning Commission |
| [ASCE Civil Engineering Source, Oct 2024 (renovation)](https://www.asce.org/publications-and-news/civil-engineering-source/article/2024/10/28/san-franciscos-iconic-transamerica-pyramid-completes-massive-renovation) | "Two winged buttresses grow out of the tower's east and west sides **beginning at its 29th floor and ending just below its 49th floor**, where the office levels give way to a metal spire" |
| [SEAONC Legacy Project (structural engineers)](https://legacy.seaonc.org/structure/transamerica-pyramid/) | Chin & Hensolt structural engineer, 48 stories / 853 ft, wings = elevator shafts, windows pivot 360° |
| [Curbed SF — "Why is the light on…"](https://sf.curbed.com/2020/1/21/21075049/transamerica-pyramid-beacon-light-special-occasions-venom) | Night lighting: 6,000 W **"crown jewel" beacon inside the 32-pane glass enclosure at the top of the spire**, lit only on occasions (nightly from Apr 2020); separately a permanent **1,000 W red aviation warning light at the very tip** |
| [SFGate — inside the crown jewel](https://www.sfgate.com/travel/article/secret-room-top-transamerica-pyramid-pictures-13709329.php) | Confirms the 32-pane glass room is the highest space, reached by a stair and two ladders inside the hollow spire |
| [vibrationdata.com structural note](http://www.vibrationdata.com/earthquakes/Pyramid.htm) | 212 ft spire, "base width 175 ft" (53.3 m), wings from the 29th floor, exposed truss system above the first floor |
| Wikimedia Commons photographs (below) | Elevations, crown, wing extents, base truss, night appearance |

### Photographs actually examined (all Wikimedia Commons, attributed, not committed here)

| File | View | What it establishes |
|---|---|---|
| `SF_Transamerica_full_CA.jpg` | Full tower from Coit Tower (looking S/SSE — north + west faces) | Whole silhouette, the **west wing in profile**, the ground-level chevron truss, no wing on the north face |
| `SF_Transamerica_top_CA.jpg` | Crown from street level | Wing is a **blank, flat-topped, vertical-faced precast box**; spire is metal-grid clad and steps in from the crown; wide blank corner bands; deeply recessed windows |
| `Transamerica_Pyramid_2023.jpg` | Near-corner elevation, clean sky | Used for the silhouette measurement in §3 |
| `Transamerica_Pyramid_during_Orange_Skies_Day_detail_dllu.jpg` | Looking straight up a corner | Corner geometry, window recess depth, base soffit |
| `Transamerica_Pyramid_base.jpg` | Under the colonnade at night | Chunky raked precast legs, deep soffit, recessed dark lobby behind, uplighting |
| `Transamerica_Pyramid,_SF,_at_night.JPG` | Night | Facade is **not** floodlit; windows read as scattered warm points; only the tip carries light |

No AI-generated imagery and no unsourced 3D model was used. No copyrighted
full-resolution imagery is committed to this repository; the table above links
to the sources instead.

## 2. Verified dimensions, location and orientation

**Footprint (measured from the OSM node coordinates, local tangent plane at
lat 37.7952):**

| Edge | Length | Outward normal (° cw from true north) |
|---|---|---|
| NW→SW (west face) | 54.31 m | 260.90 |
| SW→SE (south face) | 54.38 m | 171.03 |
| SE→NE (east face) | 54.31 m | 80.90 |
| NE→NW (north face) | 54.38 m | 351.03 |

So the plan is a **54.3 m square rotated 9.1° counter-clockwise from cardinal**
(faces 9.1° west of north / north of east). This is the Financial District
grid. The published "175 ft (53.3 m) base width" agrees with the measured
54.3 m to within a metre; the model uses 53.3 m for the *sloping shell* at grade
and lets the splayed truss feet reach the mapped 54.3 m.

**Centroid of the four measured corners: `-122.402786, 37.795166`.**
The plan document's anchor `-122.4026508, 37.7951872` sits ~12 m east of that.
Wikipedia's infobox gives `37.7952, -122.4028`, which matches the measured
centroid. **Decision: use the measured centroid**, documented in `REPORT.md`.

**Heights**

| Quantity | Value | Confidence |
|---|---|---|
| Architectural height (tip) | 260 m / 853 ft | Verified, unanimous |
| Floors | 48 (+3 basements) | Verified |
| Top of the occupied pyramid / base of the spire | **195 m (641 ft)** used | *Decided* — see §6 conflicts |
| Spire length | 65 m (213 ft) used | Derived from the above |
| Wings | 29th floor to just below the 49th → **z ≈ 120 m to 186 m** | Floor range verified (PCAD, ASCE); metric conversion inferred from an even floor-to-floor of ~3.75 m |
| Ground colonnade / exposed truss | ~14 m tall (2 storeys) | Visual inference from photographs |

**Facade:** precast concrete panels faced with **white quartz aggregate** —
near-white, slightly warm, matte. Windows are small, deeply recessed, vertically
proportioned, in a dense regular grid; each face has wide **blank corner bands**
where the structure is expressed, and the window columns are progressively cut
off by the taper as the face narrows.

## 3. Silhouette measurement (photogrammetric, `Transamerica_Pyramid_2023.jpg`)

Sky and building were separated by channel difference and the silhouette traced
row by row. Three findings, all used in the model:

1. **The shell is a true straight-sided pyramid whose faces extrapolate to the
   tip**, not to some point above or below it: the shell's corner line reaches
   zero width at the same image row as the spire's. The half-width therefore
   follows `26.65 · (1 − z/260)` m all the way up, and the crown at 195 m is
   13.3 m across — which independently reconciles with the building's ~46,000 m²
   of floor area summed over 48 tapering floorplates.
2. **The spire is a separate, twice-as-steep needle.** Its silhouette narrows at
   0.067 px/px per side against the shell's 0.133, so at the crown the spire is
   only ~51 % as wide as the shell — about 7 m at its base — before running out
   to the same tip. The step where the crown parapet oversails the spire is
   clearly visible in the crown photograph.
3. The silhouette is **vertical between the wing's bottom and top** (constant x
   over ~200 px), confirming the wings have **vertical outer faces** and are
   therefore *triangular in profile* (flush where they start, projecting ~6.8 m
   at the top) — exactly PCAD's "triangular buttresses".

## 4. What each side shows

- **North (Clay Street side):** an unbroken taper. No wing. Dense window grid,
  blank corner bands, mechanical louvre band near the crown.
- **East (Montgomery Street, the address side):** the **elevator-shaft wing**,
  and the two `entrance=yes` nodes in OSM sit on this edge. This is the identity
  face. (The plan document calls it the "north-east" face; measured, its normal
  bears **80.9°**, i.e. essentially east, a hair north. Recorded as a
  correction.)
- **South (Washington/California approach):** the postcard elevation; taper
  reads pure with both wings seen in profile at the edges.
- **West:** the **stair / smoke-tower wing**, visually the same size as the east
  one in the Coit Tower photograph; the sources describe different contents, not
  different shapes.
- **Top:** a small square crown (~13 m across, see §3) with a parapet, sloped metal roof
  planes rising to the spire collar, the spire, and the two flat wing caps
  sitting ~9 m below the crown. Everything is tiny relative to the plan — the
  aerial camera mostly sees the four sloping roofs of the pyramid itself.
- **Night:** the facade is dark. The only lights are the red aviation beacon at
  the tip and, occasionally, the 6,000 W "crown jewel" inside the glazed room at
  the top of the spire. Nothing else glows.

## 5. Recognition cues (ranked)

1. **The steep, straight four-sided pyramid running all the way to a point** —
   unique in San Francisco.
2. **Near-white quartz-aggregate facade against small dark windows**, with the
   wide blank corner bands.
3. **The two triangular wings** breaking the upper taper on east and west.
4. **The chevron/A-frame truss colonnade at the ground**, with the tower
   apparently standing on splayed legs over an open plaza.
5. **The thin metal spire with the lit tip.**

## 6. Uncertainties and conflicting evidence

- **Where the pyramid ends and the spire begins.** Wikipedia says "the top
  212 ft (65 m) is the spire" (⇒ crown at 641 ft / 195 m) *and* lists
  "top floor 695 ft (212 m)" in the same infobox — the two cannot both be true,
  and the coincidence of "212" in both suggests a units mix-up upstream. My own
  photogrammetry puts the crown lower still (~180 m), but that measurement is
  the least trustworthy of the three because the photograph looks slightly
  upward and foreshortens the top. **Decision: crown at 195 m, spire 65 m**, the
  most widely published pairing and the middle of the range. Recorded in
  `REPORT.md`.
- **Wing heights in metres** are inferred by converting "floor 29 → just below
  floor 49" with an even floor-to-floor; no published metric figure was found.
- **Wing width across the face** is visual inference (~12 m, roughly a third of
  the face at that level).
- **Number of chevron bays at the ground** counted from one photograph (5 apexes
  per face); other photographs are consistent but not conclusive.
- The 2020–2024 Foster + Partners renovation changed the lobby, plaza and
  ground-level glazing. The model deliberately renders the ground level as the
  timeless chevron colonnade rather than tracking the current retail fit-out.

## 7. Miniature translation (per `docs/styles/miniature-toy.md` §22)

**Preserve:** the single straight taper and its exact slope; the 54 m square
plan and its 9.1° yaw; both wings on the correct faces with their triangular
profile; the vertical grain of the window columns and the blank corner bands;
the chevron colonnade; the thin spire with a lit tip.

**Simplify:** 48 window rows → 13 continuous recessed window channels per face
that terminate against the taper the way the real columns do; precast panel
joints → gone; the mechanical crown → one dark louvre band plus a parapet and a
metal hip roof; the lobby → one recessed glass box behind the legs; the renovated
plaza, Redwood Park, and every neighbouring structure → excluded entirely.

**Exaggerate (only where it buys recognition):** the chevron legs are chunkier
than scale, the corner bands slightly wider, the window channels deeper and
fewer, and the crown-jewel glow larger than a real 32-pane room.
