# Hiram W. Johnson State Office Building — reference dossier

455 Golden Gate Avenue, San Francisco, CA 94102 · OSM way/35176304 ·
Skidmore, Owings & Merrill, completed 1998 · 14 storeys.

This is the modelling dossier for `artifacts/hiram-johnson-state-office-building/`.
The plan it executes is `docs/asset-plans/hiram-johnson-state-office-building.md`.
Where this file and the plan disagree, **this file wins** — every disagreement is
listed in §6 with the evidence that settled it.

---

## 1. Identity, and the two buildings it is not

| | |
|---|---|
| Name | Hiram W. Johnson State Office Building |
| Complex | the northern half of the Ronald M. George State Office Complex |
| Address | 455 Golden Gate Avenue |
| Block | bounded by Golden Gate Avenue (N), Polk (E), McAllister (S), Larkin (W) |
| Architect | Skidmore, Owings & Merrill (Page & Turnbull on the Earl Warren half) |
| Structural | Forell/Elsesser — welded steel moment frame + 292 passive dampers |
| Contractor | Clark Construction; developer Hines; owner CA Dept of General Services |
| Completed | 1998 (design finished 1996, selected 1995) |
| Size | 830,000 sq ft, 14 storeys, ~50,000 sq ft floor plates, twin 10-storey atria |
| Occupants | 1st District Court of Appeal, Judicial Council, ~11 state agencies |

**Not this building #1 — the Earl Warren Building**, 350 McAllister Street, the
1922 Bliss & Faville Beaux-Arts bar with the giant round-arched arcade, 27 m tall,
already shipped as the landmark `earl-warren-building`. It occupies the southern
half of the same block and stands in front of this building in every plaza
photograph. DGS manages the two under one record, which is where the address
confusion starts.

**Not this building #2 — the Phillip Burton Federal Building**, 450 Golden Gate
Avenue, directly across the street to the north. It is also a big pale slab with a
curved plan, a US flag and a glazed entrance, and a Street View camera standing on
Golden Gate Avenue sees it filling half the sky. During this build's research a
mis-signed panorama projection made it look like the subject for several passes.
**The tell is the lettering:** this building carries `STATE OF CALIFORNIA` etched
across its entrance glazing with `THE HIRAM W. JOHNSON STATE OFFICE BUILDING`
beneath it.

## 2. Measured geometry

All values reprojected into the app's local tangent frame
(`x=(lon−122.4375)·111320·cos(37.77)`, `z=−(lat−37.77)·110540`).

| Item | Value | How |
|---|---|---|
| Footprint polygon | 5,614 m² | OSM way/35176304, 26 nodes, shoelace |
| Oriented bounding box | 127.38 × 47.81 m | min-area OBB over the polygon |
| Long-axis bearing | 81.27° (8.73° N of E) | derived from the OBB |
| OBB centre (anchor) | −122.4179151, 37.7810345 | derived |
| Area-weighted centroid | −122.4179135, 37.7810351 | 0.15 m from the OBB centre |
| LiDAR footprint | 5,632 m² (22,530 cells @ 0.5 m) | DataSF `mblr=SF0765003` |
| Roof plane | **53.61 m** | DataSF `hgt_median_m` |
| Highest return | **60.04 m** | DataSF `hgt_maxcm` = 6004 |
| Roof height s.d. | 4.21 m over 22,530 cells | DataSF `hgt_stdcm` |
| Site grade | 19.96 m min / 23.18 m median NAVD88 | DataSF `gnd_*` |
| Published height | **203 ft = 61.87 m** | SOM project page |

### The end profiles (the important measurement)

The OSM polygon reprojected and rotated into the Civic Center grid frame
(E from the west face, S from the north face) traces both short ends as a
five-part step. That trace is the mapper's polygonal reading of a sculpted
end — two convex granite piers with a deeply recessed curved glass bay between
them, and the outer corners cut back:

| S band | west E | east E | what it is |
|---|---|---|---|
| 0.00 – 7.3 | 8.00 | 119.63 | north corner, cut back |
| 7.3 – 17.2 | 1.40 | 126.64 | convex granite pier |
| 17.2 – 29.5 | 8.00 | 120.10 | **recessed curved glass bay** |
| 29.5 – 40.4 | 0.00 | 127.38 | convex granite pier |
| 40.4 – 47.7 | 7.20 | 121.25 | south corner, cut back |

The build rebuilds this as smooth arcs (`BLEND = 5.0 m`, `PIER_BOW = 1.10 m`,
`BAY_BOW = 0.50 m`), which is what the Larkin Street and Polk Street panoramas
show.

## 3. Height — three numbers, one composition

| Source | Value | What it describes |
|---|---|---|
| DataSF `hgt_median_m` | 53.61 m | the main roof plane over most of the plate |
| OSM `height` | 54 | the same thing, tagged |
| DataSF `hgt_maxcm` | 60.04 m | the highest thing on the roof |
| SOM | 203 ft = 61.87 m | the architect's published building height |

Modelled as a 53.60 m slab with a set-back mechanical penthouse reaching 59.90 m
and its cap at **61.90 m**, which satisfies all four. Sanity check: 53.6 m over
14 storeys is 3.83 m floor to floor — right for a 1990s court/office building.
61.9 m over 14 would be 4.42 m, which is not.

This is the opposite verdict from `docs/asset-plans/earl-warren-building.md` §2.3,
which rejects *its* record's 46.39 m maximum. That rejection is correct and
specific: the Earl Warren's maximum is a single 0.5 m LiDAR cell on the party wall
it shares with **this** building. This record's maximum is a large coherent
in-footprint return and it is corroborated by the architect.

## 4. What each side shows

**North (Golden Gate Avenue) — the entrance.** Flat granite wall in large ashlar
panels with a punched grid of square windows, interrupted at the centre by a
**convex curved glass bay** bulging out of the wall, in pale glass with strong
horizontal mullions and a projecting metal eyebrow. Under it a wide, gently curved
projecting **glass-and-metal canopy** on square granite piers, and behind that a
two-storey glazed lobby with the building's lettering. Pano
`W2bcY729K7xMvPk6BrBEiw`.

**South (Civic Center Plaza) — the hero.** Above the Earl Warren's cornice, a broad
pale wall of about nine punched-grid storeys, then three lighter and more
continuously glazed storeys, then a level parapet with the set-back mechanical
penthouse behind it. The glass reads pale **sea-green** in daylight. Pano
`ztTkGZ3MnkjO_cs4mOvpRw` from Civic Center Plaza.

**East (Polk) and west (Larkin) — the drums.** Two convex granite masses with the
recessed teal glass bay between them, tall narrow full-height louvre slots cut
into the stone, no punched windows over long stretches. A small retail window in
the Polk base. Panos `4c8cOs4QIqxMprgTr44lKg`, `hairaoqsCzZ5yUF9ZZO4-Q`.

**Top.** Pale deck inside a level parapet, the long set-back mechanical penthouse
down the centre, skylights over the two ten-storey atria, mechanical enclosures
and a stair penthouse. Weakest evidence in the dossier — see §6.

## 5. Recognition cues, ranked

1. The two sculpted end drums: convex granite piers flanking a deeply recessed
   ten-storey curved glass bay
2. Near-white granite + dense square window grid + pale sea-green glass, at twice
   the height of the Beaux-Arts bar in front
3. The Golden Gate Avenue entrance bay and canopy
4. The lighter, more glazed top three storeys over the punched grid
5. From above: level parapet, long set-back mechanical penthouse, teal skylights

## 6. Corrections to the plan, and open uncertainties

- **The plan's first draft called the south front a 5 m convex bow and made it
  recognition cue #1. It is flat, and the plan was corrected before this build
  started.** Two independent checks: the OSM south edge is collinear to within
  1 cm over 91 m, and a **rectilinear** re-projection of the Civic Center Plaza
  panorama shows the Johnson parapet running dead straight beside the Earl
  Warren's straight cornice. The arcs that appear in a **cylindrical** crop of the
  same panorama are the projection — the Earl Warren cornice arcs identically in
  those frames, and it is known to be straight. SOM's "sweeping curve of the
  tallest slab gestures out toward the plaza" is realised here as the end drums
  and the north entrance bay.
- **Google Street View panorama tiles are north-aligned at u = 0 plus 180°, not at
  the metadata `yaw`.** Calibrated twice against City Hall's dome (true bearing
  194.5° from the Larkin/McAllister pano, found at raw 18.9°) and against the Earl
  Warren and Bill Graham Civic Auditorium in the same frame. Getting this wrong by
  180° is what made the Federal Building look like the subject.
- **Google's pano tile grid at zoom z is 2^z × 2^(z−1) tiles, not
  2^(z−1) × 2^(z−2).** The wrong grid silently fetches the top-left quadrant of
  the sphere, which still renders a plausible-looking strip of *some other*
  building.
- *Inferred*: the z = 42.9 m break between the punched grid and the glazed top
  band. Read off the plaza photograph, where the upper three storeys visibly
  change character. Not counted off drawings.
- *Estimated*: the mechanical penthouse footprint (E 34–92, S 16.5–31.5). The
  LiDAR maximum and 4.21 m standard deviation say something substantial stands
  ~6.4 m above the median plane; they do not say where or how big.
- *Estimated*: the two atrium skylights. "Twin atria rising ten storeys" is
  published; their roof glazing is not visible in the only nadir-ish imagery
  available (Esri z20, off-nadir enough that the north facade leans across its own
  roof, and half the block in the building's shadow).

## 7. Deliberate departures from reality

- **Window colour.** The real punched windows read pale sea-green in daylight.
  They are modelled `Toy_glass` `#2a4d73` (dark navy) anyway: ~260 pale windows in
  a pale wall give the app's aerial camera nothing to read, and the style bible
  §5 is explicit that windows are graphical elements before they are literal
  openings. The sea-green is kept where it does identity work — the two end bays
  and the roof skylights, in `Toy_teal`.
- **Entrance semantic scale.** The bay and canopy are wider, taller and deeper
  than scale demands (style bible §9); they are the building's face and are a few
  pixels from the app's camera.
- **Roof deck colour.** `Toy_steel` `#9aa0a6`, not `Toy_roofd` `#45454a`. On a
  large flat deck under the review rig `Toy_roofd` renders near-black and the roof
  reads as a hole in the model.

## 8. Sources

- https://www.openstreetmap.org/way/35176304 — footprint, `height=54`,
  `building:levels=14`, name, `addr:housenumber=455`
- https://www.som.com/projects/san-francisco-civic-center-complex/ — 203 ft,
  14 storeys, 1998, and the massing statement
- https://www.hines.com/properties/san-francisco-civic-center-complex-san-francisco
  — 830,000 sq ft, 50,000 sq ft floor plates, twin atriums, $265M
- https://www.clarkconstruction.com/our-work/projects/san-francisco-civic-center —
  1998, design-build, ~11 agencies, 2,100 staff
- https://forell.com/projects/hiram-w-johnson-state-office-building-earl-warren-supreme-court-building
  — 292 passive dampers, welded moment frame, seismic joint, atria
- https://www.foundsf.org/Fun_Facts_about_the_Ronald_M._George_State_Office_Complex
  — the 14-storey limit and the school playground, the 1950s predecessor
- https://www.flickr.com/photos/wallyg/3953727511 — "twin atria rising 10 stories
  above the law libraries", SOM 1998
- https://www.dgs.ca.gov/RESD/Resources/List-of-DGS-Managed-Office-Buildings/Page-Content/List-of-DGS-Office-Buildings/Balance-of-the-State/Earl-Warren-Hiram-W-Johnson-Building
  — the one-record complex
- https://data.sfgov.org/resource/ynuv-fyni.json (`mblr=SF0765003`) — 2010 LiDAR
- Google Street View panoramas `W2bcY729K7xMvPk6BrBEiw` (Golden Gate Ave),
  `4c8cOs4QIqxMprgTr44lKg` (Polk), `hairaoqsCzZ5yUF9ZZO4-Q` (Larkin),
  `ztTkGZ3MnkjO_cs4mOvpRw` (Civic Center Plaza), `by2PvOmdKeqlMZAdVQyy3Q`
  (Larkin & McAllister) — resampled to metric cylindrical and rectilinear views
- Esri World Imagery nadir tiles at z20 over the block
