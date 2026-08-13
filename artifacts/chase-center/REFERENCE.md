# Chase Center — reference dossier

Research behind `chase-center.glb`. Compiled 12 August 2026 for the
address-to-asset pipeline run on `BUILDING: 1 Warriors Wy, San Francisco, CA 94158`.

Everything below is either **measured** (from the OSM API, reprojected here),
**published** (with the source named), or **inferred** (visual/derived — flagged
in place and again in §9). The plan file `docs/asset-plans/chase-center.md` was
the starting point; §8 lists where this dossier overrides it.

## 1. What the building is

An 18,064-seat NBA arena in Mission Bay, opened 6 September 2019, designed by
MANICA Architecture with Kendall Heaton, on an 11-acre privately financed site
that also carries two Uber office blocks, the Thrive City plaza and a bayfront
park. Only the arena is in scope.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/579646390](https://www.openstreetmap.org/way/579646390) | the 66-vertex surveyed footprint, address, `capacity=18,064`, `height=38.1`, Wikidata link |
| [Wikipedia: Chase Center](https://en.wikipedia.org/wiki/Chase_Center) | opening date, architects, engineers, capacity, $1.4 bn cost, site programme |
| [Enclos — Chase Center Arena](https://enclos.com/project/chase-center-arena/) | **134 ft height**, 160,000 sq ft facade, 1,165 unique aluminium mega-panels (~7,500 individual panels), "stacked drums of varying sizes", AESS curtainwall and storefront |
| [Dlubal structural reference 001159](https://www.dlubal.com/en/downloads-and-information/references/customer-projects/001159) | **31.755 m structural height**, plan **154.397 × 156.781 m**, facade areas |
| [Archpaper / Facades+ on MANICA's facade](https://www.archpaper.com/2020/05/facades-manicas-chase-center-references-san-franciscos-mission-bay-aluminum-panels/) | the sail-like aluminium facade concept, 14 panel categories |
| [Hydrotech — Chase Center](https://www.hydrotechusa.com/projects/chase-center-golden-state-warriors-stadium) | Sarnafil single-ply membrane roof (light-coloured) |
| Overpass query, 220 m radius around the centroid | the site bearings in §4 — West Entrance, Box Office, Thrive City, Bayfront Park, Uber blocks |

Nothing here relies on a single photograph, a single AI-generated image, or an
unsourced 3D model.

## 3. Verified dimensions and location

| Item | Value | Basis |
|---|---|---|
| Footprint, oriented box | 155.1 × 153.5 m | measured, OSM way/579646390 |
| Footprint, published plan | 154.397 × 156.781 m | Dlubal — corroborates the measurement to ~1.5% |
| Footprint area | 19,465 m² | measured |
| Plan radius about the centroid | 70.1–89.1 m (mean 78.6) | measured |
| **Anchor (WGS84)** | **−122.3873962, 37.7678739** | polygon **centroid**, measured |
| Architectural crest | **40.84 m (134 ft)** | Enclos |
| Roof deck | **31.755 m** | Dlubal (top of primary roof steel) |
| OSM `height` | 38.1 m | OSM — the permit-envelope figure, between the two |

**Height decision (eave vs crest, recorded explicitly as the pipeline requires):**
three published numbers measure three different things. 31.755 m is the roof
deck / eave. 40.84 m is the top of the aluminium skin — the crest. 38.1 m is the
planning envelope. The asset targets **40.8 m = crest**, with the roof membrane
authored at **31.8 m = eave**. That is a 9 m sail rise on the entry side, which
matches what photography shows.

**Anchor decision:** the pipeline requires the anchor to come from the geometry
the model actually centres on. The oriented-box centre and the polygon centroid
differ by 3.4 m here (the plan bulges NE and pinches NW). The model is built
about the **centroid**, so the centroid is the anchor.

## 4. Orientation and site

The plan's minimum-area oriented box lands 169.9° from east — about 10° off
axis, which on a lobed blob with a 78 m mean radius is not a visible rotation.
The asset is authored square to the world, Blender +Y = true north, +X = east,
because `placeGeneric()` in `app/src/assets.js` applies no rotation.

Bearings measured from the centroid (Overpass, this dossier):

| Feature | Bearing | Distance |
|---|---|---|
| West Entrance (main) | W | 76 m |
| Box Office | NW | 72 m |
| Warriors Shop | NW | 86 m |
| Third Street / Muni T "UCSF/Chase Center" | W | 145–160 m |
| Warriors Way | N | 118 m |
| Chase Center Garage | N | 106 m |
| Terry A. Francois Boulevard | E | 107 m |
| Bayfront Park | E | 162 m |
| Seeing Spheres (Eliasson) | SE | 106 m |
| Uber HQ Building 3 | NW | 112 m |
| Uber HQ Building 4 | SW | 109 m |

So the hero elevation is **west**, onto the Thrive City plaza. The contract's
nominal "front faces −Y" cannot be honoured; per
`docs/asset-plans/README.md`'s orientation note, real-world orientation wins and
the deviation is recorded in `REPORT.md`.

## 5. What each side shows

**West (Thrive City / Third Street)** — the hero. A tall glazed slot cut through
the aluminium skin, the entry canopy beneath it, the oversized outdoor video
board on the WNW quadrant, and the skin at its highest directly above.

**North (Warriors Way / 16th Street)** — continuous panelled skin over the
glazed ground-level retail band; secondary entrances; the skin falling away from
the west peak.

**East (Terry A. Francois / Bayfront Park)** — the bay-facing back. Uninterrupted
panel rhythm, the lowest skin line, back-of-house at grade.

**South** — like the north; a secondary glazed entry toward the south plaza.

**Top** — a large light membrane roof, a central mechanical yard, and the skin's
swooping edge as the outline. *Roof layout beyond "light membrane + central
mechanical cluster" is inferred from aerial imagery, not from a drawing.*

## 6. Recognition cues (ranked)

1. A big low rounded drum standing alone on flat ground — a disc among boxes
2. The swooping skin line: lowest on the bay side, peaking over the west entry
3. Pale aluminium with a broad vertical panel rhythm
4. The glazed west slot with its canopy and the oversized video board
5. The floating read: a dark glazed retail band at grade under the pale drum

## 7. Miniature translation

**Preserved**

- The real plan. The footprint is *not* a circle, an ellipse or a rounded
  square: fitting those gave 2–5 m radial residuals. It is reduced instead to a
  6-harmonic radial curve about the centroid — **rms 2.0 m** against the
  surveyed polygon, area within **0.1%**. The lobes survive (r = 85.6 m NE,
  71.8 m NW), which is what makes the roof outline read as Chase Center rather
  than as a generic arena.
- The crest at 40.8 m and the deck at 31.8 m.
- The disc silhouette at 155 m across, isolated — nothing else in the GLB.

**Simplified / exaggerated**

- ~7,500 metal panels → 40 vertical bands, 0.70 m deep, ~12 m pitch
- 14 panel categories → one flat `Toy_trim` aluminium
- the compound-curved parapet → a lofted ring whose top edge follows
  `32.9 + 7.9·((1+cos(θ−270°))/2)^2.2`
- the curtainwall atrium → one glazed slot, a pale reveal, four steel fins
- the plaza video board → one oversized panel, the night-glow hero
- roof plant → one central cluster plus twelve panel pads on a ring

## 8. Where this dossier overrides the plan

| Plan (`docs/asset-plans/chase-center.md`) | Built | Why |
|---|---|---|
| anchor `−122.387433, 37.767883` (OBB centre) | `−122.3873962, 37.7678739` (centroid) | the model centres on the centroid; 3.4 m apart |
| plan = rounded square, corner radius 34 m | 6-harmonic fit to the real outline | the rounded square implied 22,800 m²; the real polygon is 19,465 m² |
| 60 bands at 0.55 m | 40 bands at 0.70 m | 60 read as corrugation in the first aerial review; the style bible asks for broad rhythms |
| swooping **parapet** on a flat drum | the whole upper **skin** swoops | a swooping parapet was invisible from the app's aerial camera |
| navy entry canopy | pale `Toy_trim` canopy; navy moved to the video-board frame | `Toy_navy` canopy over `Toy_glass` glazing merged into one blob |
| atrium projecting 15 m | a glazed slot, 0.3 m proud, with a 6.5 m canopy | the projecting version read as a shed bolted to an arena |
| 6 roof units on a 46 m ring | 4 units flanking one central block + 12 ring pads | scattered props; the style bible asks for clusters |

Every one of these came out of a review render, and each is visible in the
iteration log in `REPORT.md`.

## 9. Uncertainties, still open

- **Which height is architectural** — resolved above in favour of the Enclos
  134 ft crest, but no elevation drawing was found to confirm it directly.
- **Where the skin peaks.** Inferred from photography as being over the west
  entry. No published elevation drawing was found. If it is really at the
  north-west corner, the phase of the swoop is wrong (the amplitude is not).
- **Roof layout** beyond "light membrane, central mechanical cluster" is
  inferred from aerial imagery — and it is the most-seen surface in the app.
- **The 12 roof pads** are a designed graphic standing in for the real roof's
  equipment field, not a survey of it.
- No reference imagery is committed here; every source above is a live link.
