# 95 Jack London Alley — Gran Oriente Filipino Masonic Temple — reference dossier

Compiled 17 August 2026 for `artifacts/95-jack-london-alley/`. The plan behind it
is `docs/asset-plans/95-jack-london-alley.md`; where this file and the plan differ,
this file and `REPORT.md` win — they record what was verified at build time.

## 1. What the building is

A 1951 two-storey stucco lodge hall on Jack London Alley, in the interior of the
South Park block. Built by the Gran Oriente Filipino — the first Filipino-founded
Masonic order in the United States — behind the tenement they already owned at
45–49 South Park, on the same lot. Rizal Lodge No. 12, the last Gran Oriente lodge
in California, still meets in it.

It is the third building of the Gran Oriente complex to enter this manifest, after
104–106 South Park (the hotel). The residence at 45–49 South Park is still
procedural.

## 2. Sources and what each establishes

| Source | Establishes | Confidence |
|---|---|---|
| **Gran Oriente Filipino Hotel, Residence, and Masonic Temple Complex — Landmark Designation Report (draft, 2017)**, `static1.squarespace.com/static/5b2c30b58f51305e3d641e81/t/607d36dc86015c6f61d7e31e/1618818784827/Gran+Oriente_Landmark+Designation+Report.pdf` | 1951 construction; "Architects: Unknown"; two-storey rectangular massing with flat roof; a nine-item character-defining-features list for 95 Jack London Alley; **the only two photographs of this building located anywhere** — a square-on 2016 facade shot and a 2016 close-up of the entrance transom | **primary**, survey-grade prose |
| DataSF `ynuv-fyni`, `sf16_bldgid` 201006.0108499, `mblr` SF3775039 | footprint (OBB 13.68 × 8.57 m at 43.9°, 112.9 m², 457 cells at 50 cm); roof deck **7.84 m** median, 7.76 m majority, σ 1.27 m, max 12.99 m; ground 11.20–12.35 m NAVD88 | **measured** |
| Bing Maps aerial (Vexcel) z20 around `37.78135, -122.39344` | the roof plane (~14.5 × 8.8 m), the coping ring, one light patch and two small reddish boxes, no PV/bulkhead/plant — and the tree in the yard that kills the OSM depth | **measured / observed** |
| OSM `way/71211338` | a footprint trace, `building=yes`, no height, no name, no address | **rejected at the rear**, see §3 |
| OSM `node/2353636746` and **note 3830661** | the name, `amenity=place_of_worship` `religion=christian` `denomination=Masonic`, and two mappers disputing that tagging since 2023 — the note that commissioned this asset | tags disputed |
| DataSF `wv5m-vpq2`, parcel 3775039 | that the assessor records this lot as the **1909 three-storey 7-unit apartment building** in front. There is no assessor record of the temple at all, which is why no storey count or height comes from it | **measured, and not about this building** |
| California Freemason, "Portal to the Past" (2 June 2021) | the only source that calls the building **Moorish**; Rizal Lodge No. 12 still meeting here | secondary |
| SOMA Pilipinas cultural-asset page; SF Examiner (10 March 2023); knowthis.place 45–49 South Park | the 1951 date corroborated three ways; the cultural framing | secondary |
| OSM `way/8919615` (Jack London Alley) | the alley centreline bears 134.4°, parallel to the facade to 1.5°; the facade stands ~6.6 m off it | **measured** |

Esri World Imagery is monochrome and useless at z20 here (a known SF limitation).
No street-level imagery beyond the two designation-report photographs was
available to this session. That is the single biggest limitation of this dossier.

## 3. The footprint correction (the most important thing in this file)

**OSM `way/71211338` over-traces this building by about 6.6 m at the rear.** Three
independent checks:

1. Sampling the OSM rectangle along its own long axis against every DataSF
   building polygon in the block: the south-west **13.0 m** falls inside the
   temple's polygon (median height 7.84 m); the next **3.0 m** falls inside
   **41–43 South Park's** polygon (median 9.83 m); the last **2.0 m** falls inside
   no building at all.
2. Bing z20 shows a **tree canopy** in OSM's rear third, and the dark roof
   membrane visibly stops short of the OSM outline.
3. The two footprint centroids are **2.64 m** apart, displaced along the long axis
   toward the alley — the signature of a rectangle extended at one end.

| Source | Dimensions | Verdict |
|---|---|---|
| DataSF LiDAR SF3775039 | 13.68 × 8.57 m at 43.9°, centroid `-122.3934430, 37.7813460` | **built on this** |
| Bing z20 roof plane, read against a metric grid | ~14.5 × 8.8 m, same axis, same centre to ~1 m | confirms |
| OSM `way/71211338` | 20.35 × 9.37 m at 45.9° | rejected at the rear |

**Design footprint: 8.60 m frontage × 13.70 m depth, 117.8 m², long axis 45.9°.**
Anchor `-122.3934430, 37.7813460`. Alley facade faces **225.9°**.

## 4. Verified dimensions

| Item | Value | Basis |
|---|---|---|
| Frontage (Jack London Alley) | **8.60 m** | DataSF OBB short axis, rounded |
| Depth | **13.70 m** | DataSF OBB long axis, rounded |
| Roof deck | **7.84 m** | DataSF LiDAR median, 457 cells — measured |
| Facade parapet crest (target height) | **8.40 m** | **derived**: deck + ~0.56 m of parapet. Two photogrammetric reductions of the 2016 square-on photograph gave 8.3 m and 8.6 m; 8.40 is between them and sits sensibly on the measured deck. **Ships as `"estimated": true`** |
| Side/rear parapet crest | 8.15 m | inferred — the facade parapet clearly steps up in both photographs |
| Facade heading | 225.9° (SW) | both footprint sources; agrees with the alley centreline to 1.5° |
| Axis-aligned XY bbox | 16.20 × 16.09 m | consequence of 45.9°, not a scale error |

The LiDAR maximum of **12.99 m is rejected**: it is 4.0σ above the median and
matches 45–49 South Park's own 13.00 m maximum exactly. A 0.5 m raster cell
sampling the taller neighbour — the Earl Warren / 106 South Park failure mode.

## 5. What each side shows

The designation report's character-defining-features list for 95 Jack London Alley,
in full, is the backbone of the facade:

> Two-story, rectangular massing and plan with flat roof · Textured stucco cladding
> on the façade and north elevation · Central entrance with incised pointed arch and
> tripartite arch detail, columns topped by globe shapes, inset rectangular entry
> opening surmounted by three arched fixed transom windows separated by engaged
> columns · Gold leaf compass and square with the letter "G" at the center painted on
> center transom window above door · Incised text above main entry reading "GRAN
> ORIENTE FILIPINO MASONIC TEMPLE" · Incised text at the parapet reading "DEDICATED
> TO THE SUPREME ARCHITECT OF THE UNIVERSE" · Small rectangular window openings
> flanking central entrance · Horizontal rectangular window opening at second floor ·
> Incised text located at the base of the façade near northwest corner reading
> "MCMLI AD"

**South-west (alley facade)** — *observed, 2016 photograph.* One uninterrupted
plane of blush-pink textured stucco from grade to parapet, with no cornice line,
no string course and no base. Every feature is cut into it. Top to bottom: the
DEDICATED… course incised just under the parapet coping; a single **horizontal**
white-framed window high and centred at second-floor level, filled with a warm
amber grille; the two-line GRAN ORIENTE FILIPINO / MASONIC TEMPLE course; then the
entrance. MCMLI AD is incised at the base near the north-west corner.

The entrance: a pointed, slightly ogee arch recessed into the wall; a **trilobed**
arch head springing inside it over the doorway; three round-arched transom windows
above dark panelled double doors, separated by white engaged colonettes, the centre
one carrying the **gold-leaf square and compass with a letter G**; two
**free-standing white columns capped with white spheres** standing proud of the
door plane, one either side. Two small roughly square white-framed windows flank
the entrance at ground level.

**North-west (long flank)** — *observed, 2016 oblique.* A finished stucco
elevation, **not a party wall** (the report cites stucco on "the façade and north
elevation"). Nearly blank: one small opening near the alley end and one projecting
element. Its parapet carries a **dentilled band** along the top — the report's
"cornice", and the only ornament on the building besides the doorway.

**South-east (long flank)** — *assumed.* No photograph located. Built plain, with
one small opening.

**North-east (rear, onto the yard)** — *assumed.* No photograph located. Built
plain, with a service door and one small opening.

**Top** — *observed, Bing z20.* Flat at 7.84 m inside a parapet whose coping reads
as a bright line against a dark charcoal membrane. The facade parapet at the alley
end stands ~0.25 m proud of the side parapets. One light patch on the north-west
half, two small reddish boxes near the alley end. **No PV, no bulkhead, no plant.**

## 6. Recognition cues (ranked)

1. **The Moorish arch ensemble** — ogee recess, trilobed head, three transoms, two
   white globe-capped columns. Nothing else in the manifest looks like it.
2. **The pink box among gray giants** — 8.4 m of blush pink in a well formed by a
   12.1 m tenement, a 14.8 m warehouse and a 9.8 m neighbour.
3. **The two white spheres** — at thumbnail size the arch reduces to a dark notch
   with two bright dots either side, and that reduced silhouette is still
   unmistakable.
4. **The banded top edge** — bright coping ring, dentil course on the north-west
   flank only, facade parapet stepping up at the alley end.
5. **The blank everything-else** — three bare elevations reads as *hall*.

## 7. Preserved / simplified

**Preserved:** the 8.60 × 13.70 m footprint at 45.9°; the 7.84 m deck / 8.40 m
crest relationship and the 0.25 m parapet step; the entrance ensemble in full; the
gold emblem; both text courses; the horizontal second-floor window; the dentil band
on the north-west flank only; the pink.

**Simplified:** the arch recess is modelled ~0.15 m wider and ~0.25 m taller than
measured so the notch survives the app's distance; the trilobe is one extruded
profile, not three arches; the three transoms are one glazed panel with two
mullions and the colonettes disappear; globes are 10-segment spheres; incised text
is a shadow-edged band with **no glyphs at any scale** and MCMLI AD is gone
entirely; the dentil course is one band with the bevel doing the shadow; stucco
texture, downpipes, meters, conduit, the wall light and the utility pole are gone.

## 8. Uncertainties (carried into REPORT.md and the plan's 2.15)

1. **The height is derived, not published.** The deck is measured; the parapet on
   top of it is not. `"estimated": true`.
2. **The footprint correction rests on three remote-sensing inferences**, not a
   survey. If ground evidence shows a low rear wing under that tree, the depth,
   the anchor **and the whole exclusion analysis** have to be redone.
3. **The facade may not be symmetric.** The 2016 photograph puts the north-west
   flanking window visibly closer to the entrance than the south-east one, but its
   verticals converge hard enough that its vanishing points will not solve
   consistently. Built symmetric at ±2.85 m — see REPORT.md.
4. **Three of the four elevations are assumed**, not observed.
5. **The paint hue is inferred** from two 2016 photographs, one fully shaded. The
   *relation* is confident; the hue is not.
6. **It is a *draft* designation report** ("DRAFT report dated XXX 2017",
   "Landmark No. XXX"). Do not call this a designated City Landmark.
