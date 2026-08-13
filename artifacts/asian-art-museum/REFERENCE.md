# Asian Art Museum — reference dossier

Research behind `asian-art-museum.glb`. Compiled 12 August 2026 by the executing
agent, re-verifying `docs/asset-plans/asian-art-museum.md` rather than trusting it.
Two dossier facts turned out to be wrong and are corrected below (§7).

The building: **Asian Art Museum of San Francisco — Chong-Moon Lee Center for Asian
Art and Culture**, 200 Larkin Street, in George Kelham's 1917 Main Library.
OSM way/24588037 · Wikidata Q727277 (institution) / Q111931359 (the building).

---

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/24588037](https://www.openstreetmap.org/way/24588037) (`/api/0.6/way/24588037/full.json`) | The 17-vertex footprint polygon, the address, `building:levels=3`, the wikidata link, and the misleading `height=46` tag |
| [DataSF Building Footprints](https://data.sfgov.org/resource/ynuv-fyni.json) `mblr=SF0353001`, `area_id=255` | 2010 LiDAR: `hgt_maxcm` 2810, `hgt_median_m` 23.22, `gnd_min_m` 15.15, `gnd_maxcm` 1980, `p2010_zmaxn88ft` 152.927, `peak_1st_m` 47.16 |
| [Wikipedia — Asian Art Museum (San Francisco)](https://en.wikipedia.org/wiki/Asian_Art_Museum_(San_Francisco)) | Kelham 1917; Gae Aulenti base-isolation conversion reopening 20 March 2003; 200,000 sq ft; the 2023 pavilion and terrace |
| [Wikidata Q111931359](https://www.wikidata.org/wiki/Q111931359) | "The Old Main Library": architect George W. Kelham, inception 1917, Beaux-Arts. **No height claim** |
| [noehill — SF Point of Historical Interest](https://noehill.com/sf/landmarks/poi_asian_art_museum.asp) | Modelled on Cass Gilbert's Detroit Public Library; "the long arcade of the Fulton Street facade"; "the Larkin Street facade ... reflects the design of the City Hall in its main features"; Civic Center Historic District, NRHP #78000757, NHL |
| [ArchDaily — wHY unveils the addition](https://www.archdaily.com/880551/why-unveils-90-dollars-million-san-francisco-asian-art-museum-addition) | Akiko Yamazaki & Jerry Yang Pavilion 8,500 sq ft; East West Bank Art Terrace 7,200 sq ft; "a rusticated gray terracotta facade" echoing the Beaux-Arts original |
| [wHY project page](https://why-site.com/work/the-asian-art-museum-in-san-francisco/) | "the pavilion as a whole fits within the datum lines of historic structure"; terracotta as "a reinterpretation of the rusticated granite on the original façade"; the terrace as the transition between old and new |
| [Destination Accessible](https://destinationaccessible.org/asian-art-museum/) | "eight steps as well as ramps ... leading to the three sets of double doors" — the main entrance is on Larkin |
| [Commons: Asianartmuseumnight.jpg](https://commons.wikimedia.org/wiki/File:Asianartmuseumnight.jpg) | The Larkin night elevation: colonnade, balustraded bay balconies, incised frieze inscription, dentil cornice, low attic, uplit columns, lit entrance lanterns |
| [Commons: Asian Art Museum (6000548677).jpg](https://commons.wikimedia.org/wiki/File:Asian_Art_Museum_(6000548677).jpg) | The Hyde Street side: Aulenti-era pale granite retaining walls, raised planted terrace, glass railings, a bronze relief panel, and a glazed metal-framed bay projecting from the historic wall |
| Esri World Imagery nadir aerial over the block | The roof: parapet band, dark low-slope deck, two light courts, the raised hipped monitor, and the pale terrace with the pavilion and round sculptures over the eastern third |

No source was used twice for the same fact without a second one agreeing, and no
AI-generated image or unsourced 3D model was used at all.

## 2. Verified dimensions and location

Footprint measured from the OSM polygon, reprojected with the repo's own
tangent projection (`AGENTS.md`), then rotated into the Civic Center street grid.

| Quantity | Value | How |
|---|---|---|
| Polygon area | 4,893.2 m² | shoelace on the reprojected polygon |
| Oriented envelope | 106.60 × 54.71 m | min-area OBB over the polygon |
| Long-axis bearing | 81.68° (8.32° north of due east) | OBB principal edge |
| OBB centre | −122.4159859, 37.7802817 | **the manifest anchor** |
| Polygon centroid | −122.4160441, 37.7802533 | 5 m west of the OBB centre — not used |
| Crest above grade | **28.10 m** | DataSF `hgt_maxcm` |
| Main roof plane | **23.22 m** | DataSF `hgt_median_m` |
| Site grade | 15.15 – 19.80 m NAVD88 | DataSF `gnd_*`; the block falls ~4.7 m |

## 3. Orientation

Bounded by Larkin (west), McAllister (north), Hyde (east), Fulton (south — the
pedestrianised Fulton Mall with the Pioneer Monument). The main entrance faces
**west** onto Larkin, across Civic Center Plaza from City Hall.

The asset is authored in true-world orientation (Blender `+Y` = north, `+X` =
east) with the whole assembly rotated **+8.32°** about Z, because `placeGeneric()`
in `app/src/assets.js` scales and positions but never rotates. The contract's
"front faces −Y" rule cannot be honoured literally — the front faces west — and
real-world orientation wins under AGENTS rule 5.

## 4. What each side shows

**West — Larkin Street (hero).** Rusticated pale-granite base roughly a third of the
facade height with tall openings; above it a giant order of engaged columns on a
continuous stylobate, glazed bays and small balustraded balconies between them;
solid end pavilions each pierced by a tall arched opening with a geometric lattice
grille; a full entablature carrying the incised inscription, a dentil cornice and a
low attic. Eight steps and flanking ramps rise to three sets of double doors. At
night the colonnade is washed by uplight and the cornice reads as a bright band.

**South — Fulton Street.** The long arcade: the longest continuous rhythm on the
building and, per noehill, the elevation that defines the Civic Center's principal
planning axis from Market Street to the City Hall dome.

**North — McAllister Street.** The matching flank, plainer, and **stepped back**: the
north wall jogs ~9.7 m south at E≈62.5 and a further ~4.2 m at E≈70 (see §7).

**East — Hyde Street.** The modern face: Aulenti-era granite walls and a raised
planted terrace behind glass railings, with a glazed metal-framed bay projecting
from the historic wall. Only ~26 m wide, because the south wall steps north here.

**Top.** The asset's largest surface. A light parapet band round the whole block; a
dark low-slope deck inside it; two rectangular light courts in the western half
separated by a cross-wing; a raised square monitor with a hipped roof between them
and the east (this is the 28.10 m crest); and over the eastern third the pale
terracotta pavilion along the north edge with a glazed roof panel, beside the open
sculpture terrace with its round sculptures and planters.

## 5. Recognition cues (ranked)

1. A long, low, pale block under one unbroken heavy cornice — the civic twin of City
   Hall across the plaza
2. The giant-order colonnade and inscribed frieze on the Larkin front
3. The fourteen-bay arched arcade along Fulton
4. From above: dark historic roof with two courts and a hipped monitor in the west,
   pale terracotta pavilion and sculpture terrace in the east — the building's whole
   history split across one roof
5. The rusticated granite base wrapping all four sides

## 6. Preserve / simplify

**Preserved:** the 106 × 55 m envelope and its stepped north-east and south-east
corners; the 8.32° grid rotation; the continuous cornice and attic as one silhouette
line; the colonnade as the west front's entire identity; the roof's old/new split.

**Simplified:** dozens of columns → eight chunky ones between two end pavilions, on a
single stylobate and abacus rather than individual plinths (individual plinths read
as a picket fence from the aerial camera — tried and rejected); the arcade → fourteen
arched openings on one impost course; all ornament → three horizontal bands (base
cap, entablature, attic); the inscription → one proud frieze course, not letterforms;
rooftop clutter → two court wells, one hipped monitor, one pavilion box, one terrace,
three sculpture pucks, two planter strips, two plant clusters; the eight entrance
steps → one three-tread plinth, semantically enlarged.

## 7. Corrections to the plan's dossier

Both were found by re-verification and both changed the model.

**7.1 The height tag is an elevation.** OSM way/24588037 carries `height=46`. That is
not a height: it is the NAVD88 roof *elevation*, 152.927 ft = 46.61 m, which appears
verbatim as `p2010_zmaxn88ft` in the DataSF LiDAR record for the same footprint.
Extruding it would have produced a museum 1.6× too tall — half the height of City
Hall's dome. The plan already flagged this; re-verification confirmed it. **Crest
28.10 m, cornice 23.22 m**, both from LiDAR.

**7.2 The footprint is not a rectangle.** The plan (§2.8) described a clean
106.60 × 54.71 m block. Projecting the OSM polygon into the street grid shows it
steps back twice on the north-east (north wall at S≈0 to E=62.5, then S≈11.5, then
S≈15.75) and once on the south-east (south wall at S=54.71 only to E=93.6, then
S=41.78). The east end is therefore a 13 × 26 m block, not a full-depth one. The
model uses the surveyed ten-vertex rectilinear outline; jogs under 2 m are absorbed
and the area error against OSM is under 2%. The aerial imagery independently shows
both setbacks.

## 8. Uncertainties and conflicting evidence

- **Does the 2023 pavilion rise above the historic parapet?** wHY say it "fits within
  the datum lines of historic structure"; the 2010 LiDAR predates it and cannot
  answer. The nadir aerial shows a low box that clearly does not challenge the
  monitor. The model puts the pavilion top at 26.0 m — above the 24.2 m attic so it
  reads from the street, below the 28.10 m crest so the datum claim holds. **Inferred.**
- **The terrace level.** The aerial cannot resolve whether the sculpture terrace sits
  on the main 23.2 m roof plane or on a lower east wing. The model puts it on the main
  plane, which is what keeps the cornice unbroken (recognition cue #1) and what the
  LiDAR median across the whole footprint supports. **Inferred.**
- **Column and arcade bay counts** were read from photography, not drawings. Eight
  columns and fourteen arcade bays are chosen for rhythm at the app's camera
  distance, not counted off a survey. **Inferred.**
- **The site falls ~4.7 m across the block.** The app seats an asset on terrain
  sampled at one anchor, so the model's base is level while the real building's is
  stepped. Accepted deliberately; a stepped base would fight the loader.
- A small separate structure (~8.6 m tall, ~100 m², a distinct DataSF LiDAR record)
  stands off the north-east corner. It is **not** part of this asset.
