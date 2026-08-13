# Earl Warren Building — reference dossier

Research behind `earl-warren-building.glb`. Compiled 13 August 2026. Everything
here was re-verified for this build; where it disagrees with
`docs/asset-plans/earl-warren-building.md`, this file and `REPORT.md` win.

## What this building is

The **Earl Warren Building**, 350 McAllister Street, San Francisco — the 1922
California State Building by Bliss & Faville, home of the Supreme Court of
California and the First District Court of Appeal. Six storeys of grey granite and
terra-cotta in the Beaux-Arts manner, 115 m long and 27 m tall, facing City Hall
across Civic Center Plaza. Vacated after the 1989 Loma Prieta earthquake,
base-isolated and restored by Page & Turnbull, reoccupied 1999.

## Not this building

The pipeline request named the address **455 Golden Gate Avenue**. That address
belongs to the **Hiram W. Johnson State Office Building** (OSM way/35176304,
14 storeys, `height=54`), the white bow-fronted slab that fills the north half of
the same block and appears behind the Earl Warren Building in essentially every
photograph of it. DGS manages the pair as one "Earl Warren / Hiram W. Johnson"
complex under a single address, which is where the conflation comes from. The
Johnson building is **not** in this asset, and the validator explicitly checks the
model's north extent for it.

## Sources

| Source | What it establishes |
|---|---|
| [OSM way/260137839](https://www.openstreetmap.org/way/260137839) | the 18-node footprint polygon, `height=27`, `building:levels=5`, wikidata link |
| [OSM API full.json](https://api.openstreetmap.org/api/0.6/way/260137839/full.json) | the geometry actually measured here |
| [Wikidata Q1829495](https://www.wikidata.org/wiki/Q1829495) | 1922, 6 floors, occupant Supreme Court of California (Q2629503), named after Earl Warren (Q311197) |
| [Wikipedia — Earl Warren Building](https://en.wikipedia.org/wiki/Earl_Warren_Building) | **87 ft (27 m) to roof**, 6 storeys, granite + terra-cotta, Bliss & Faville, Page & Turnbull, Loma Prieta vacancy, Ronald M. George complex |
| [courthouses.co — District Court of Appeal, San Francisco](https://courthouses.co/us-states/states-a-g/california/district-court-of-appeal-san-francisco/) | six-storey grey granite and concrete; **three large arches at the centre of the south front with recessed porch and entrances**; second-storey arched windows; recessed fourth floor; 30 ft courtroom skylight |
| [DataSF Building Footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni.json) `mblr=SF0765002`, `area_id=671` | 2010 LiDAR: `hgt_median_m` **25.11**, `hgt_maxcm` 4639, `gnd_min_m` 17.85, polygon area 3,019 m² |
| same dataset, `mblr=SF0765003`, `area_id=218` | the Hiram W. Johnson record next door: `hgt_median_m` 53.61, `hgt_maxcm` 6004 — the source of the bad `hgt_max` on our record |
| [DGS — Earl Warren / Hiram W. Johnson Building](https://www.dgs.ca.gov/RESD/Resources/List-of-DGS-Managed-Office-Buildings/Page-Content/List-of-DGS-Office-Buildings/Balance-of-the-State/Earl-Warren-Hiram-W-Johnson-Building) | the two buildings share one DGS address record |
| [LoC HABS "California State Building, 350 McAllister Street"](https://www.loc.gov/pictures/item/ca2183/) | the documentation set; not used for measurements here, listed as the route to certainty on bay counts |
| [Commons — Earl Warren Building (San Francisco).JPG](https://commons.wikimedia.org/wiki/File:Earl_Warren_Building_(San_Francisco).JPG) | the full south elevation from Civic Center Plaza: the arcade, the cornice, the attic, the entrance group, and the Johnson slab behind |
| [Commons — The Earl Warren Building and Courthouse.jpg](https://commons.wikimedia.org/wiki/File:The_Earl_Warren_Building_and_Courthouse.jpg) | close oblique of the entrance arches: carved archivolts, keystone cartouches, bracket lanterns, diagonal flagpoles, rusticated ashlar |
| Esri World Imagery, z19 nadir tiles over the block | the roof: two turquoise light-court skylights, central lantern with twin laylights, dark mansard band along McAllister |

No copyrighted full-resolution imagery is committed with this asset.

## Verified dimensions and location

| | Value | How |
|---|---|---|
| Footprint polygon | 2,968 m² | OSM way/260137839 reprojected to the local tangent plane, shoelace |
| Oriented bounding box | **115.49 × 31.52 m** | min-area OBB over that polygon |
| Long-axis bearing | **81.33°** (8.67° north of due east) | derived from the OBB |
| OBB centre (the anchor) | **−122.4178413, 37.7806865** | derived |
| LiDAR footprint area | 3,019 m² | DataSF — within 2% of OSM, confirming the record matches the building |
| Parapet crest | **27.00 m** | Wikipedia 87 ft = 26.52 m, OSM `height=27`; taken as 27.00 |
| Roof plane | **25.10 m** | DataSF `hgt_median_m` 25.11 |

The OBB code was validated against the Asian Art Museum (way/24588037) first: it
reproduces that plan's published 106.60 × 54.71 m, 81.68°, −122.4159859/37.7802817
exactly.

## The two height traps

1. **`hgt_maxcm` = 4639 (46.39 m) is unusable.** It is 19 m above this building's
   own roof plane. The Earl Warren footprint shares a party wall with the Hiram W.
   Johnson record, whose median roof is 53.61 m, and a 0.5 m LiDAR cell straddling
   that wall samples the tower. Nadir imagery shows nothing on this roof more than
   ~1.5 m above the deck. A single-cell `hgt_max` at a shared wall is the least
   reliable number in the dataset.
2. **`building:levels=5` in OSM contradicts Wikidata's 6.** Six is right (the
   architectural descriptions place the Supreme Court courtroom on the fourth floor
   under a recessed fifth and an attic). It does not affect the massing: the arcade
   reads as one double-height order regardless.

Three independent figures — Wikipedia 87 ft, OSM 27 m, LiDAR 25.11 m roof plane +
a parapet — agree on 27 m. That is unusual for this repo and it is what makes this
target height high-confidence.

## Orientation

The building fills the southern band of the block bounded by McAllister (south),
Polk (west), Golden Gate Avenue (north) and Larkin (east). The Hiram W. Johnson
slab fills the northern band. Long axis at bearing 81.33° — the Civic Center grid,
within 0.35° of the Asian Art Museum one block east.

The ceremonial front faces **south** onto McAllister. This is the one landmark in
the set where the asset contract's "front faces −Y" and real-world orientation
agree; the model is authored with +Y = true north and rotated +8.67° about Z.

## The footprint correction (the plan was wrong)

`docs/asset-plans/earl-warren-building.md` §2.8 assumed a simple 115.5 × 31.5 m
rectangle. The measured polygon is **not** a rectangle — it is a comb. Reprojected
into the street grid (E = 0 at Polk running 115.48 m east to Larkin; S = 0 at the
north property line running 31.52 m south to McAllister):

| E span | North wall at S | What it is |
|---|---|---|
| 0.00 – 5.07 | 14.71 | recessed north-west corner |
| 5.07 – 19.86 | 0.70 | west wing |
| 19.86 – 44.64 | 9.90 | **light court A** (24.8 × 9.9 m) |
| 44.64 – 70.95 | 0.40 | centre wing |
| 70.95 – 96.73 | 10.15 | **light court B** (25.8 × 10.2 m) |
| 96.73 – 110.60 | 0.05 | east wing |
| 110.60 – 115.48 | 14.85 | recessed north-east corner |

The south wall runs unbroken from E 0.00 to E 115.48 at S = 31.52 — which is
exactly what the plaza photograph shows, and why the arcade can be continuous.

The two courts are the **turquoise panels in the nadir aerial**: glazed over well
below the roof plane. They are modelled at z = 17.50 with a `Toy_teal` deck and a
`Toy_trim` curb, so they read as bright wells from the app's camera.

## What each side shows

**South (McAllister) — the hero.** Granite plinth; rusticated ashlar base storey
with small rectangular windows, interrupted at the centre by **three tall arched
portals** with deeply carved archivolts, keystone cartouches and paired bronze
bracket lanterns; a low second storey of square windows over a string course; then
the **giant arcade of tall round-arched bays** running unbroken end to end, each
with a keystone, springing from a continuous impost course, with small square
spandrel windows between the heads; an architrave and a heavy **modillion cornice**;
a light **attic storey** of small square windows, slightly inset; a plain parapet
cap. Three flagpoles project diagonally at arcade level.

**East (Larkin) and west (Polk).** The short returns, only 16.7 m of wall each
south of the recessed corners. Same banding; the arcade continues as three bays.

**North (Golden Gate side).** Faces the service gap and the Johnson building, not a
street. Plain rectangular windows on the same pitch, no arches, with the two court
notches cut into it.

**Top.** South to north: a broad dark sloping **mansard band** along McAllister with
vent dormers; the pale parapet ring; a mid-grey deck over the wings; the **two
turquoise light courts**; between them the **raised central lantern** with its
**twin square laylights** (the courtroom skylights, the 30 ft one among them); and
low grey plant and stair penthouses.

## Recognition cues (ranked)

1. The unbroken giant arcade of round-arched bays along a 115 m front
2. The proportion — four times as long as it is tall, a low bar at the foot of the
   much taller white Johnson slab
3. The three carved entrance arches at the centre of the south front
4. From above: two turquoise light courts flanking a raised central lantern, with a
   dark mansard band along McAllister
5. The heavy modillion cornice and pale attic capping the whole length

## Preserve / simplify

**Preserve** — the 115 × 31 × 27 m proportion and the 8.67° grid rotation; the
comb plan with its two courts; the arcade as one continuous rhythm corner to
corner; the cornice as a single hard silhouette line; the roof's symmetry.

**Simplify** — 19 arcade bays with plain half-cylinder heads and a keystone block
each, no mouldings; all carving collapsed into three horizontal `Toy_trim` bands;
the bracket lanterns become six gold pucks; the flagpoles become three plain
cylinders with no flags; rooftop clutter becomes two court decks, one lantern with
two laylights, one mansard band, six penthouses.

**Exaggerate** — the three entrance portals, taller and deeper than scale demands,
because they are the building's face and are four pixels tall otherwise; and the
turquoise of the courts, which is what makes the building findable from altitude.

## Uncertainties

- The arcade bay count (19 south, 3 per end) was read off one plaza photograph and
  chosen for a 5.56 m pitch, not counted authoritatively. *Inferred.* The HABS set
  would settle it.
- The mansard band's depth (16.4 m north of the parapet) and the lantern's height
  (26.6 m, laylights to 27.0 m) come from a nadir aerial where verticals are
  foreshortened to nothing. *Estimated.*
- The court glazing level (17.50 m) is a design choice that makes the turquoise
  legible from the app's camera; the real glazing level is not published.
  *Estimated.*
- The entrance group is centred on arcade bay 9 of 19 (E = 51.83 m), slightly west
  of the building's midpoint, matching the plaza photograph. *Inferred.*
</content>

## Exclusion-radius measurement (for stage 5)

`excluded()` drops a baked footprint if its centroid **or any ring vertex** falls
inside the radius. Measured from the anchor (−122.4178413, 37.7806865) against the
OSM rings, distances in metres:

| Feature | Distance from anchor | Meaning |
|---|---|---|
| Earl Warren centroid | **2.34** | any radius ≳ 3 m drops this building |
| Earl Warren nearest vertex | 14.40 | — |
| **Hiram W. Johnson nearest vertex** | **20.21** | any radius ≳ 20 m deletes the 54 m slab next door |
| Earl Warren farthest vertex | 59.85 | the OBB half-diagonal — the number NOT to use |
| Civic Center Courthouse nearest vertex | 86.45 | next neighbour out |
| SFPUC HQ nearest vertex | 88.57 | |
| Asian Art Museum nearest vertex | 109.56 | |
| Phillip Burton Federal Building nearest vertex | 118.19 | |

Safe band is **3 – 20 m**. Take **`exclude: 12`**. The plan's first instinct — the
59.9 m OBB half-diagonal, which is what most landmarks in the registry use — would
have punched a hole through the Hiram W. Johnson building. This is a party-wall
site, not a free-standing one.

### Verified against the real bake input

Re-run against `pipeline/data/overture_buildings.geojsonseq` — the actual bake
input — using the metric `excluded()` uses (centroid **or** any ring vertex inside
the radius). 13 candidate footprints in the surrounding bbox:

| `exclude` | footprints dropped | which |
|---|---|---|
| 6 – 20 m | **1** | Earl Warren Building (nearest point 5.1 m) — correct |
| 22 – 40 m | 2 | + Hiram W. Johnson State Office Building (20.2 m, `height=54`) — **wrong** |
| 60 m | 3 | + Civic Center Plaza Garage Kiosk (58.8 m) |

Safe band **6 – 20 m**; **`exclude: 12`** is the middle of it. The 59.9 m
half-diagonal would have deleted a 54 m building.
