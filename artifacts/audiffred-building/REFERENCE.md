# The Audiffred Building — reference dossier

**1–21 Mission Street / 100 The Embarcadero, San Francisco, CA 94105.**
San Francisco City Landmark **No. 7** (designated 13 October 1968); National
Register of Historic Places **79000528** (listed 10 May 1979). Block 3715, Lot
001 (`mblr` `SF3715001`). Wikidata `Q38585977`. OSM way
[193054136](https://www.openstreetmap.org/way/193054136).

Compiled at stage 2 of `docs/asset-pipeline/ADDRESS-TO-ASSET.md` from the plan in
`docs/asset-plans/audiffred-building.md`, re-verifying every number the model
depends on. Where this file and the plan disagree, **this file and REPORT.md
win** — see REPORT.md for the corrections made.

---

## 1. What it is

An 1889 Second Empire commercial block built for Hippolite d'Audiffret, a
Frenchman who reached San Francisco from Veracruz and made money selling charcoal
in Chinatown, to a pattern-book Parisian model "to remind him of home". Three
storeys, the third inside a wood-framed slate mansard, brick over a cast-iron
shopfront, on a 585 m² corner lot running from The Embarcadero back to Steuart
Street.

It is the only building on the landward side of The Embarcadero left intact after
the 1906 earthquake and fire — spared, by the account every source repeats,
because the bartender of the ground-floor Bulkhead saloon bought the demolition
crew off with two quarts of whiskey a man and a fire cart of wine. It housed the
Coast Seamen's Union, later the Sailors' Union of the Pacific, and was the
strike headquarters for the 1901 City Front strike and the 1934 waterfront strike;
Howard Sperry and Nick Bordoise were shot dead outside it on Bloody Thursday, and
the unions still hold a ceremony there every year. In the 1940s and 50s the two
upper floors, condemned and without electricity, were artists' lofts —
Ferlinghetti, Bischoff, Lobdell, Hassel Smith.

A gas-main fire gutted it in 1978 and it was scheduled for demolition; public
pressure and the NRHP listing saved the shell. It was rebuilt in 1983–84 by
William E. Cullen for Dusan Mills, with a **glazed barrel-vaulted penthouse added
over the roof** — which is why the Assessor records four storeys on a building
every historical source calls three. Boulevard restaurant has occupied the ground
floor since 1993.

## 2. Sources, and what each establishes

| Source | Establishes |
|---|---|
| [NRHP nomination 79000528](https://npgallery.nps.gov/GetAsset/3aa06aad-5c07-4dd2-8e26-752c546519a8/) | **The most valuable source.** Construction system storey by storey; **"a common brick party wall and three exposed walls"**; "the masonry common wall continues to the roof while the three exposed walls are of wood frame covered with slate shingles"; corner quoins; corbelled brick "eyebrow" window mouldings; corbel table of soldier course over dentils; the 1924 Bank of Italy nautical frieze on **the eastern entablature only**; hand-cut **blue-grey** slate with a diamond-cut centre band; **double-width corner windows on the end elevations**; the surveyed lot, 45 ft 10 in x 135½ ft, Lot 1 Block 3715 |
| [NRHP photo set](https://npgallery.nps.gov/GetAsset/48cabe18-9d82-4d86-a5d9-930d166003fa/) | 15 photographs, December 1978, captioned by elevation — pre-restoration, so read for form, not for the present roof |
| [Wikipedia](https://en.wikipedia.org/wiki/Audiffred_Building) | Three floors; Second Empire; brick with projecting quoins; wood-framed tiled mansard with a diamond pattern; fluted cast-iron columns with floral "A" capitals; the nautical frieze; **the domed penthouse added in the reconstruction** |
| [PCAD 2370](https://pcad.lib.washington.edu/building/2370/) | "A remodeling of this building occurred in 1983. **A penthouse was also added at this time**"; landmark numbers and dates |
| [FoundSF](https://www.foundsf.org/Audiffred_Building) | Labour history; three dated photographs (c. 1905, 1964 under the freeway, 2012) |
| [CAENLUCIER](https://caenlucier.com/blog-press/2019/1/18/the-survival-of-landmark-7) | The 1983–84 refurbishment, Cullen for Mills |
| [Wikimedia Commons category](https://commons.wikimedia.org/wiki/Category:Audiffred_Building) | **26 freely-licensed photographs — the working reference set.** See §3 |
| DataSF `ynuv-fyni` (LiDAR footprints) | `SF3715001`: 2,238 cells, `hgt_median 15.36`, `hgt_majority 15.44`, `hgt_mean 14.66`, `hgt_std 2.33`, `hgt_max 19.18`, ground 3.27 m NAVD88 |
| DataSF `acdm-wktn` (parcels) | `3715001 = 1 MISSION ST`, C-3-O, Financial District/South Beach |
| DataSF `wv5m-vpq2` (Assessor, 2025 roll) | Commercial Office; **built 1889**; **4.0 stories**; 24,908 sq ft; **lot 6,301.63 sq ft = 585.4 m²** |
| OSM way 193054136 | `name=The Audiffred Building`, `building=retail`, `building:levels=3`, `roof:shape=mansard`. **No `height` tag** |
| `pipeline/data/overture_buildings.geojsonseq` | The ring named "The Audiffred Building", **`height 17.4`** |
| Google satellite (Vexcel), z21 | The roof: mansard ring on three sides, glazed barrel vault just inside it turning both end corners, pale flat deck, mechanical cluster on the party-wall half, the neighbour's roof garden beyond the party wall |

The three photographs the model was actually built from, all CC-licensed on
Commons and all re-examined at stage 2:

- **`Audiffred Building (San Francisco).JPG`** — the Mission x Embarcadero corner
  from the north-east (camera 37.793851 / −122.392617). The one frame that shows
  the corner, the mansard, the chimneys and the barrel vault together. Every
  vertical proportion in this model was measured on it
- **`Audifred Building, The Embarcadero, San Francisco, California.jpg`** — the
  Steuart end and the full Mission run from the south-west. The bay count, the
  chimney spacing and the vault's continuity around the corners come from here
- **`Audiffred Building-5.jpg`** — the Steuart corner close up: brick coursing,
  eyebrow hoods, corbel table, the diamond-cut slate band, a chimney cap

## 3. Verified dimensions and location

| Item | Value | How |
|---|---|---|
| Anchor (manifest) | **−122.3927766, 37.7933230** | OSM OBB centre, adjusted by the model's recentring shift (−0.16 m E, +0.16 m N) |
| Footprint | **41.82 x 14.00 m**, 585.5 m² | OSM way 193054136 OBB. Cross-checked: NRHP surveyed lot 13.97 x 41.30 m (0.2% / 1.3%); Assessor `lot_area` 585.4 m² (**0.03%**) |
| Roof deck / mansard crest | **15.40 m** | DataSF LiDAR `hgt_majority 15.44`, `hgt_median 15.36`, 2,238 cells — measured |
| Barrel-vault crest | **17.50 m** | Overture `height 17.4`, corroborated photogrammetrically at 17.4–18.1 m — *estimated* |
| Corbel table | 10.95 m | photogrammetric, 0.71 of the deck height |
| Entablature | 6.15 m | photogrammetric, 0.40 of the deck height |
| Ground elevation | 3.27 m NAVD88 | DataSF `gnd_min_m`; the app's terrain handles this, not the asset |
| Heading | 45.2° off the world axes | measured from the OBB |

**Orientation, and what is on each side.** Blender `+Y` = true north, `+X` = east;
the loader applies no rotation.

| Elevation | Length | Outward normal | What it is |
|---|---|---|---|
| **Mission Street** | 41.80 m | **315.2° (NW)** | the address, the hero, 13 bays |
| The Embarcadero | 14.00 m | 44.8° (NE) | the waterfront end, 3 bays, double-width corner windows |
| **Party wall** | 41.84 m | 135.2° (SE) | blind brick to the deck. No mansard, no dormers, no quoins |
| Steuart Street | 14.00 m | 225.0° (SW) | the inland end, 3 bays, double-width corner windows |

Footprint corners, metres from the anchor, clockwise:
`( 9.88, 19.66)` north — Mission x Embarcadero · `( 19.81, 9.79)` east ·
`( −9.89, −19.67)` south · `( −19.80, −9.78)` west — Steuart x Mission.

**The axis-aligned XY bounding box is 40.42 x 40.29 m — nearly square — for a
building that is 41.82 x 14.00 m.** That is the consequence of a 45.2° heading,
not a scale error, and it is the single most likely thing for a reviewer to
misdiagnose. Check the footprint along the building's own axes.

## 4. What each side shows

**Mission Street (NW, 41.80 m).** Bottom: a cream-painted cast-iron shopfront,
columns fluted with a lattice wainscot and floral "A" capitals, glazed near-black
with dark awnings, under a heavy white entablature carrying "The Audiffred
Building" in incised lettering — with the 1924 Bank of Italy **nautical frieze**
(dolphins, lighthouses, sailing ships, seahorses in bas relief) on the eastern
half only and the original plain sawtooth fascia on the western half. Middle: red
common-bond brick, white quoins at the corners, segmental-arched window pairs
under corbelled brick eyebrow hoods, ending in a corbel table of white dentils
over brick brackets. Top: blue-grey slate mansard, a white pedimented dormer per
bay, red brick chimneys with white corbelled caps, and the glazed vault behind
the crown moulding.

**The Embarcadero (NE, 14.00 m).** Three bays of the same three bands, with the
corner windows double width. A chimney at each corner. The vault turns the corner
here with a mitred hip — the one place its crest reads unambiguously.

**Steuart Street (SW, 14.00 m).** The mirror of the Embarcadero end. Boulevard's
street sign and the "100 STEUART" plate are here. No nautical frieze: the 1924
band never reached this end.

**Party wall (SE, 41.84 m).** Blind brick straight to the deck, with a low brick
firewall above it. Its neighbour at 100 The Embarcadero is 24.4 m tall, so this
face is buried for most of its height.

**Top.** 586 m² at 15.40 m. The mansard ring on three sides with its dormer and
chimney rhythm; the verdigris barrel vault as one continuous ribbon just inside
the crown moulding, mitring around both end corners; a pale membrane deck; the
mechanical cluster grouped against the party wall so the ribbon stays unbroken.

## 5. Recognition cues (ranked)

1. **The dark slate mansard with its dormer-and-chimney skyline.** Nothing else
   in the Financial District has one
2. **The cream / red / slate horizontal sandwich** — three colours bottom to top
3. **The glazed barrel vault** riding the crest on three sides
4. **Thinness.** 41.8 x 14.0 m at 17.5 m, hard against a 24.4 m neighbour
5. The waterfront corner position, with the Ferry Building across the street

## 6. Preserved / simplified

**Preserved:** the 41.82 x 14.00 m proportion, the 15.40 m deck, the 17.50 m
crest, the 45.2° heading; the three colour bands and both white dividing lines;
the mansard on the three exposed sides only; the chimneys; the vault as crest;
red brick and blue-grey slate.

**Simplified:** the cast-iron colonnade loses its fluting, lattice wainscot and
floral "A" capitals; the nautical frieze becomes one recessed strip on the
eastern half of Mission and around the Embarcadero end; each window pair becomes
one arched opening in a white ring; the corbel table becomes one dentil band; the
slate's diamond-cut centre band is dropped; each dormer becomes a box with a
white pedimented hood; downpipes, conduit, awning scallops, the sidewalk Bloody
Thursday memorial and all street furniture are dropped.

## 7. Uncertainties and conflicting evidence

- **`hgt_maxcm` 19.18 m is REJECTED as the architectural height.** It is 1.64 σ
  above a 15.36 m median on a 2.33 σ distribution, the reference photograph shows
  a large mechanical unit and a tank standing on the deck, and Overture
  independently gives 17.4 m. Resolved to 17.50 m; see REPORT.md 1
- **The Mission bay count (13) is inferred** off a foreshortened photograph. The
  ends' three bays are confident. This is the most likely place for the model to
  be visibly wrong
- **Every intermediate height is photogrammetric.** Only the 15.40 m deck is
  measured
- **The architect is genuinely unresolved.** NRHP and NPS NRIS both say unknown;
  PCAD and Wikipedia name the owner d'Audiffret and William Cullen, who did the
  1983–84 rebuild ninety-four years later. Treated as owner-built to a
  pattern-book model, which is what every primary source says
- **How much fabric is 1889 and how much 1984 is unclear.** The model is of the
  CURRENT building; a reviewer comparing it to the c. 1905 or 1964 photographs
  will find differences that are not errors
- **The nautical frieze covers half of one elevation only.** Applying it
  uniformly would be a visible factual error on the face the camera sees most
