# Mission Dolores Basilica + Old Mission adobe — reference dossier

Compiled 2026-08-10 for the SF-SIM miniature asset. Two buildings in one asset:
the 1913–1918 Churrigueresque Revival basilica and, immediately south of it, the
1791 adobe chapel (oldest intact building in San Francisco). This dossier
records what was independently verified, what was inferred from photographs,
and where the plan document (`docs/asset-plans/mission-dolores.md`) was found to
be wrong.

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/256442760 (fetched via Overpass 2026-08-10) | Basilica footprint polygon (22 nodes, 1,501 m²), `height=14` (eaves), start_date 1918, addr 3321 16th St |
| OSM way/256442765 (fetched via Overpass 2026-08-10) | "Old Mission Dolores" footprint polygon (14 nodes, 604 m²), `height=8`, start_date 1791, addr 320 Dolores St |
| Esri World Imagery z19 tiles (fetched, stitched, measured at 0.236 m/px) | True orientation (facades EAST onto Dolores St), roof layout: tile nave gable, large octagonal tiled crossing dome toward the west end, white flat aisle/side-chapel roofs, apse at far west, adobe's darker low gable directly south |
| SF Planning HPC packet 2019-005041COA (quotes the 2008 DPR 523A survey form) | Authoritative prose description of both buildings — see §2 |
| SF Planning Resolution 6161 / Landmarks Board report LM67-1 (in same packet) | Adobe structural description: 4-ft adobe walls, redwood roof beams, tile roof from central ridge, 4-ft eaves, four façade columns + balcony, four pilasters enclosing three belfry windows, Roman-arch doorway; lot frontage 106 ft |
| Wikimedia Commons photos (Category:Mission Dolores; 10 downloaded, incl. "Mission San Francisco de Asis and Dolores Basilica (2025).jpg", "Misión San Francisco de Asís … 008.jpg", "Mission Dolores (Mission District).JPG", "Mission Dolores old Chapel.JPG", "Misión … 001.jpg", "Mission Dolores, September 2008.jpg", "00 Mission Dolores.jpg") | Facade composition, tower asymmetry, tower caps, materials/colors, adobe facade detail, stair with scroll cheeks; tower-height measurement (§4) |
| opensfhistory.org "Streetwise: Mission Dolores – San Francisco Landmark #1"; foundsf.org "Mission Dolores"; Wikipedia "Mission San Francisco de Asís" | History: architects Frank T. Shea & John O. Lofquist; reinforced concrete; Churrigueresque ornament added and one tower extended in 1926 (after the 1915 Panama–California Exposition fashion); minor basilica 1952 |

No reference imagery is bundled in this folder. The Commons photographs are
CC-licensed but the safest handling is to link rather than redistribute, so the
downloaded working copies stayed outside the repo; every image used is
identified by its exact Commons filename in the table above and can be
re-fetched from `https://commons.wikimedia.org/wiki/Special:FilePath/<filename>`.

## 2. Authoritative description (DPR 523A via HPC packet, verbatim extracts)

Basilica: "a tall one-story, reinforced concrete, smooth stucco-clad building
with a roughly T-shaped plan … the shorter, north-south transept crossing at
the western end of the east-west [nave]. **The façade faces east** and is
flanked by **two asymmetrical, reinforced concrete towers**, which were
embellished in 1926. The Mission-style, **clay tile-clad, cross-gable roof is
interrupted by two domes**. The primary fenestration is inset, arched, fixed,
wood-sash, stained-glass windows…"

Adobe: "walls of sun-dried adobe brick, four feet thick… Roof of tiles, sloping
from central ridge. Wide eaves, some four feet, projecting from walls. Four
columns on the façade support a balcony at the second floor level; four half
columns or pilasters at the second-floor level enclose three windows in the
belfry. The main entrance is a low doorway framed in a simple Roman arch."

Note: the same packet's staff-written feature list says "symmetrical" towers;
the DPR quote and every photograph say asymmetrical. **Asymmetrical is
correct** (the north tower was extended in 1926) and is what this asset builds.

## 3. Verified dimensions, location, orientation

Local tangent projection = the project's (lon0 −122.4375, lat0 37.77).

- **Basilica footprint**: 58.7 m along the nave axis × 33.6 m max across
  (24.6 m across the east facade proper); area 1,501 m². Long-axis bearing
  ≈ **86°** (nave runs east–west; the plan's claim that "the naves run
  north–south" misread its own bearing figure). Centroid −122.4269684,
  37.7643675.
- **East face** of the basilica spans 24.6 m; the tower shafts measure ≈ 6.9 m
  square against that width in frontal photographs.
- **Adobe chapel**: footprint way is 45.7 × 17.0 m overall, but that includes
  the rear annex and the ca.-1975 gift-shop strip on its south side. The
  historic chapel volume itself (matching the polygon's north strip and its
  12.2 m east face, and the ~114 ft published nave length) is ≈ **37 m × 12.2 m**;
  front-face bearing basis ≈ **82°**. The asset models the chapel volume only.
- **Placement**: basilica north (toward 16th St), adobe south. The adobe's
  north wall passes within **≈1.9 m** of the basilica's south flank; the adobe
  front stands **≈5–6 m further east** (closer to Dolores St) than the basilica
  facade plane. The two long axes really do splay ~4°.
- **Orientation (headline correction)**: both facades face **EAST onto Dolores
  Street** (street with palm median clearly east of the block in imagery;
  DPR text agrees). The plan document said north — wrong.
- **Heights**: basilica nave eaves 14 m (OSM tag, kept); adobe tagged 8 m
  (ridge; photos against the basilica support eaves ≈ 6.8 m, ridge ≈ 10.3 m).

## 4. Tower heights (measured, no published figure)

No published tower height exists (plan agrees). Measured from the 2025 Commons
frontal photograph (rectified verticals) scaled by the known 24.6 m facade
width, cross-checked against "Misión … 008.jpg", with ±1–2 m error from
perspective and the choice of ground line:

- Shared main cornice (top of both plain shafts): ≈ **19 m**
- Central cresting (espadaña) apex: ≈ **24–25 m**
- South tower: single open cupola stage + ribbed verdigris dome ≈ **27–28 m**
- **North tower**: three diminishing ornate stages + ribbed verdigris dome
  ≈ **39–40 m** to the dome top, ≈ 41 m to the metal cross tip

The model normalizes the north-tower cross tip to exactly **41.0 m**;
`targetHeightM: 41`, `"estimated": true`.

## 5. What each side shows

- **East (Dolores St front)** — the identity view. Full-width stair with scroll
  cheek walls up to three portals (grand layered central arch + two smaller
  ornate side portals at the tower bases). Central bay: tall arched
  stained-glass window (NOT a rose window) between spiral columns and shell
  niches, under a stepped ornate cresting with a statue niche. Plain smooth
  tower shafts to a shared cornice, then the asymmetric tops. Immediately
  south: the adobe front — battered corner buttresses, four columns in two
  pairs on plinths, full-width dark-wood balcony, four pilasters framing three
  bell openings, stepped rake moldings, deep dark eaves, chunky ridge cross.
- **North (16th St flank)** — basilica only: cream stucco; low flat-roofed
  aisle/annex strip with small arched windows; nave clerestory with arched
  stained-glass windows above; tower shaft at the east corner.
- **South flank** — basilica flank like the north one, but mostly hidden
  behind the adobe at street level; the adobe's south wall is plain whitewash
  with tiny windows (the gift-shop annex is omitted).
- **West (rear)** — transept block with the south chapel wing, apse
  half-cylinder with half-dome; parish additions kept as simple massing.
- **Top** — the aerial signature: long red-tile nave gable ending at the
  white facade block; the big octagonal tiled crossing dome with lantern near
  the west end; white flat aisle roofs flanking the nave; tile transept
  cross-gable; apse half-dome; two verdigris tower domes at the street; and
  the adobe's smaller, darker tile gable tight alongside to the south.

## 6. Recognition cues (ranked)

1. The pairing: tiny 1791 whitewashed adobe beside the towering 1918 basilica
2. Asymmetric twin towers — short domed cupola vs tall three-stage wedding-cake
   tower, both with verdigris ribbed domes
3. Ornate Churrigueresque central bay between plain shafts, over a grand stair
4. Red-orange tile roofs + big octagonal tiled crossing dome (aerial cue)
5. Adobe facade kit: four columns, balcony, three bells, huge dark eaves

## 7. Preserve / simplify

**Preserve**: two-building composition at true offsets and true splay; tower
asymmetry and their verdigris ribbed domes; three-portal facade with the
arched central window and stepped cresting; full-width stair with scroll
cheeks; T-plan with crossing dome + apse; 14 m eave / 19 m cornice / 41 m
tower height relationships; adobe's column-balcony-bells facade and deep
eaves; the ~1.9 m gap (buildings do not touch).

**Simplify**: Churrigueresque ornament → broad raised `Toy_trim` panel fields,
layered arch surrounds, simple niches (style bible §22/§26 — one panel + two
niches level of density, no filigree); spiral columns → plain round columns;
belfry balustrades → simple slabs; tile texture → flat color with chunky ridge
caps and eave bands; statuary → omitted (niches stay); bells → three simple
dark-bronze bells; rear parish additions → one clean wing volume.

## 8. Uncertainties and conflicts

- **Tower height is measured, not published** (§4) — manifest stays
  `"estimated": true`.
- Symmetrical-vs-asymmetrical towers: DPR + photos beat the staff list —
  asymmetrical.
- Adobe ridge height: OSM says 8 m; photo proportion suggests ~10 m ridge.
  Model uses 10.3 m ridge / 6.8 m eaves (inferred).
- The "two domes" in the DPR: satellite shows the big octagonal crossing dome
  plus the small apse half-dome; modeled as such.
- Basilica south-flank jogs (side chapels bulge ~2 m) are straightened to keep
  the toy silhouette clean; the adobe gap becomes 1.4–2 m at the street end —
  within the real range.
- The plan's §2.7 recipe (symmetric 30 m towers, north-facing front, no dome)
  is superseded by this dossier.
