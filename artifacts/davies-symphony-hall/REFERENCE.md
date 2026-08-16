# Louise M. Davies Symphony Hall — reference dossier

Research behind `davies-symphony-hall.glb`. Compiled 12 August 2026. Everything
dimensional here was measured from geometry or LiDAR; everything visual was read
from the photographs listed in §2 and is labelled *inferred* where it is a
reading rather than a measurement.

The plan this executes is `docs/asset-plans/davies-symphony-hall.md`. Where this
file and the plan disagree, **this file and `REPORT.md` win** — they record what
was verified at build time.

## 1. What it is

The San Francisco Symphony's concert hall, 201 Van Ness Avenue, opened 1980,
by Skidmore, Owings & Merrill with Pietro Belluschi, acoustics by Bolt, Beranek
and Newman; 2,743 seats; 252,000 sq ft gross. It is the Modernist member of the
Civic Center's Beaux-Arts family, and SOM's answer to that problem is the whole
design: match the neighbours' cornice line and materials, then sweep a
convex glass arc across the Van Ness/Grove corner aimed diagonally at City Hall.

It fills its own block — Grove north, Van Ness east, Hayes south, Franklin west
— and is the southern half of the War Memorial and Performing Arts Center, with
the Opera House 25 m away across Grove.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way 32865746](https://www.openstreetmap.org/way/32865746) | 39-node footprint (the geometry this model is built on), address, `capacity=2743`, `wikidata=Q6688842`, and the **rejected** `height=49 m` |
| [DataSF Building Footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json), record `201006.0000141` | The height authority: 28,160 LiDAR cells at 0.5 m, ground mean 18.91 m NAVD88, roof **median 26.12 m**, **max 34.95 m**, peak 53.91 m absolute. Its bounding box matches the OSM way to five decimals. |
| [Wikipedia — Louise M. Davies Symphony Hall](https://en.wikipedia.org/wiki/Louise_M._Davies_Symphony_Hall) | Architects, 1980, US$28 M, capacity, the one-inch structural glass curtain wall, the 1992 acoustic renovation |
| [Wikidata Q6688842](https://www.wikidata.org/wiki/Q6688842) | 1980 (P571/P1619), capacity (P1083), architect (P84). Carries **no** height claim (P2048). |
| [SOM project page](https://www.som.com/projects/davies-symphony-hall-san-francisco-war-memorial-and-performing-arts-center/) | 252,000 sq ft; "glass-enclosed promenades along Grove Street and Van Ness Avenue"; the curved facade facing City Hall diagonally; the explicit intent to relate to the neighbours by "matching cornices, roof forms, colors, and textures" |
| Wikimedia Commons `Daviessymphonyhall.jpg` | The north-east corner in daylight: the whole arc, the fin rhythm, the two promenade levels, the clerestory band, and the shallow ribbed shell roof |
| Wikimedia Commons `Louise M. Davies Symphony Hall at night.jpg` | The night state, and the source of this asset's entire glow design |
| Wikimedia Commons `San Francisco Davies Symphony Hall 2.jpg` | The back: plain precast panel walls, the stepped parapet, the cantilevered curved canopy nose, the single arched window |
| Wikimedia Commons `Aerial view of the Beaux Arts Civic Center of SF.jpg` | Davies' shell read against the Opera House roof and City Hall's dome — the cross-check that rejected the 49 m tag |

Reference photography is linked, not committed: all of it is Wikimedia Commons
material under its own licences, and the repo does not need full-resolution
copies.

## 3. Verified dimensions and location

| Item | Value | How |
|---|---|---|
| WGS84 anchor | `-122.4206030, 37.7776227` | centre of the footprint's axis-aligned bounding box, which is what the model is centred on |
| Footprint envelope | 122.61 m E–W × 91.16 m N–S | measured, OSM way reprojected to the repo's local tangent frame |
| Footprint area | 7,396 m² | shoelace on the same polygon |
| Oriented bbox | 121.58 × 84.27 m | rotating-calipers minimum-area fit |
| Grid heading | long axis 99.0° / 279.0° | from the oriented bbox; the Civic Center grid, ~9° off the world axes |
| **Front arc** | circle centre `(10.03, −1.02)` local, **R = 44.75 m**, sweep −4.5° → 99.1° = **103.6°** | least-squares circle fit to the eleven OSM arc nodes; residuals −0.82 … +0.53 m |
| Cornice / parapet | **26.1 m** | DataSF LiDAR median over 28,160 cells |
| Roof crest | **34.95 m → built at 35.0 m** | DataSF LiDAR max; cross-checked as `peak_1st_m 53.91 − gnd_mean 18.91 = 35.0` |
| Ground | 18.91 m NAVD88 mean (18.28 min) | same record; OSM `ele=20` |

### The height correction — the dossier's one hard conflict

**OSM tags `height=49 m`. That is wrong and this asset does not use it.**

Three independent things say so:

1. The LiDAR record gives 26.12 m median and 34.95 m max over 28,160 samples.
   Those are not noise, and they land exactly on the two datums any photograph
   of the building shows: the parapet ring, and the crest of the shell.
2. SOM says the design matches its neighbours' cornices. 26.1 m puts the Davies
   parapet within a metre of the Opera House's — which is what the photographs
   show. A 49 m building could not do that.
3. 49 m would make Davies taller than the Opera House's fly tower (44 m in this
   repo's own manifest). Every aerial of Civic Center contradicts that; the
   Davies shell sits visibly *below* the Opera House's tower.

Recorded again in `REPORT.md`. If a published architectural height ever
surfaces, prefer it — but it has to beat a 28,000-sample measurement.

## 4. Orientation

Authored with Blender `+Y` = true north, `+X` = east, built directly on the
measured polygon, so the model carries the Civic Center grid's ~9° rotation in
its own geometry and the loader (`placeGeneric`, which only scales and
positions) never rotates it.

The asset contract's "front faces −Y" cannot be honoured literally: Davies'
front arc faces **north-east**. Real-world orientation wins (AGENTS rule 5, and
the standing note in `docs/asset-plans/README.md`). Recorded in `REPORT.md`.

## 5. What each side shows

**North-east — the arc (Van Ness × Grove).** The face the design exists for.
Bottom to top: a low stone plinth wall with steps and planting; two levels of
continuous glass promenade behind a close rhythm of slender white precast fins,
the upper level taller, separated by a slim spandrel; a solid precast attic
band; a row of narrow dark clerestory slots near its top; a thin cornice; then
the shell oversailing, its fascia carrying the gold `LOUISE M DAVIES SYMPHONY
HALL` lettering. A curved terrace slab cantilevers from each end of the arc with
a rounded nose and a pipe rail.

**East (Van Ness) and north (Grove).** The promenade glazing and the fin rhythm
run off the arc onto both streets, so the arc never reads as a bolt-on. A small
radiused stair bay interrupts each flank — kept in the model because they are in
the measured polygon, but deliberately not made into events.

**South (Hayes) and west (Franklin).** Back-of-house, and blank on purpose:
large plain precast panels, a stepped parapet, one arched window high on the
Franklin wall, a cantilevered canopy over the Hayes service entrance, a loading
recess. The contrast between this and the arc *is* the composition.

**Top.** A broad shallow ribbed metal shell, ~8 m of rise across a ~100 m span,
cresting at 35.0 m on a flat crown (the real building carries a flagpole there;
not modelled — see §8). The shell springs off the fascia along the arc and dies
onto a narrow flat deck strip inside the parapet elsewhere. Over the south-west
back-of-house block the roof is flat, dark and carries tidy plant. The rib
direction — running *with* the curve — is what makes the shell read as metal
from directly overhead.

## 6. Recognition cues, ranked

1. The 103.6° glass arc turning the corner toward City Hall
2. The shallow ribbed shell cresting over it
3. Two glowing promenade levels behind a fin rhythm
4. Pale precast held to the Civic Center cornice line — a horizontal building,
   never a tower
5. The cantilevered curved terrace noses at the ends of the arc

## 7. Preserve / simplify

**Preserved exactly:** the arc's measured radius, centre and sweep; the 26.1 m
cornice and 35.0 m crest as two distinct datums; the real footprint polygon
including its awkward bays and its south-west wing; the near-blank back.

**Simplified:** individual mullions gone (each promenade level is one recessed
band, 75 fins rather than the real hundred-plus); the clerestory becomes 78
regular slots; standing seams become 40 modelled ribs; the gold lettering
becomes a plain gold band on the arc's fascia only; back-of-house parapet steps
reduce to one; the plinth is thickened to 1.6 m so it also hides the terrain
seam; the flagpole is dropped.

## 8. Uncertainties and decisions taken

- **The shell's rise is derived, not published.** 35.0 − 26.9 (fascia top) =
  8.1 m, modelled as a paraboloid cap. The real roof may be a segmental vault;
  at the app's camera distance the difference is a few pixels. An architect's
  section would settle it.
- **The shell's rear extent is a design decision.** The photographs establish
  the shell over the arc; how far back it runs before becoming flat roof is not
  documented. It is built as a polar curve about the arc centre that reaches to
  1.4 m inside the parapet everywhere, which matches the day photograph's
  reading that the roof meets the parapet on the visible sides.
- **The fin count (75) and slot count (78) are stylistic**, tuned to survive at
  thumbnail size, not counted from drawings.
- **The flagpole is deliberately not modelled.** It would take the bounding-box
  top and cost the height normalization for two pixels of mast.
- **The terraces cantilever 4.5 m** past the footprint at the ends of the arc,
  so the model's XY bounding box (124.7 × 95.0 m) is slightly larger than the
  footprint plus plinth. That is a cantilever, not a scale error.
- **No architect-published dimensions exist.** Wikidata has no P2048 and SOM
  publishes only gross area, which is why everything in §3 is measured rather
  than cited.
- **The Henry Moore *Large Four Piece Reclining Figure*** stands in the
  forecourt at the Van Ness/Grove corner. Out of scope for this asset; worth a
  props pass later.
