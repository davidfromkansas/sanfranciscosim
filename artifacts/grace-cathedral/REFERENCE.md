# Grace Cathedral — reference dossier

Compiled 2026-08-10 for the SF-SIM miniature asset. Every figure used by the
build was re-verified against the sources below; where this dossier contradicts
`docs/asset-plans/grace-cathedral.md`, THIS FILE (and REPORT.md) wins, and the
disagreement is called out explicitly.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way/32946942](https://www.openstreetmap.org/way/32946942) (fetched via Overpass 2026-08-10) | 27-node footprint polygon; `height=53`; place_of_worship/episcopal tags. Measured from the nodes: long axis bearing **81.0° cw from true north**, oriented extent **95.8 × 43.4 m**, projected bbox center **lon −122.4134968, lat 37.7918332** |
| [Wikipedia — Grace Cathedral, San Francisco](https://en.wikipedia.org/wiki/Grace_Cathedral,_San_Francisco) | Length **329 ft / 100 m**, width **162 ft / 49 m at the transepts**; facade towers **174 ft / 53 m above street** (154 ft above entry floor); **flèche 117 ft / 35 m from roof ridge to cross top = 247 ft / 75.3 m above street**; entry floor **20 ft / 6.1 m above street**; French Gothic in ferroconcrete, 1928–1964, Lewis P. Hobart; Ghiberti-door replicas installed 1964 |
| [SFTravel guide](https://www.sftravel.com/article/guide-to-san-franciscos-grace-cathedral) + [constructingtheuniverse.com/Grace.html](https://www.constructingtheuniverse.com/Grace.html) | East rose window "Canticle of the Sun" (Gabriel Loire, 1964): **25 ft / 7.6 m wide**, 3,765 faceted-glass pieces, geometry = the Chartres 12-fold scheme, sits above the Ghiberti doors on the **east** front. North tower = 44-bell carillon ("Singing Tower"); south tower has the tour deck |
| Wikimedia Commons photos (geolocated, viewed 2026-08-10): `Grace Cathedral San Francisco facade.jpg` (E front), `View of Grace Cathedral from Huntington Park…jpg` (E from park), `Grace Cathedral-Nob_Hill-San francisco.jpg` + `Grace Cathedral, San Francisco.jpg` (NE corner, N flank), `The spire of Grace Cathedral, San Francisco.JPG` (flèche + roof close-up) | All facade/flank/roof observations below; flèche is **verdigris copper with a gold cross**; roofs are **brown-copper standing-seam metal**, not gray; nave-flank buttresses are **engaged stepped piers with pinnacle caps — no true flying arches visible**; tower crowns are **flat parapets with corner turrets** (no spires) |

## Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Footprint | 95.8 × 43.4 m oriented, long axis 81.0° cw from N | measured from OSM nodes |
| Overall published size | 100 m long × 49 m wide at transepts | published (Wikipedia/Structurae) |
| Towers | 53 m above street | published; matches OSM `height=53` |
| Nave roof ridge | ≈ 130 ft ≈ **39.6 m** above street (derived: 247 ft cross − 117 ft flèche) | derived from published figures |
| Flèche cross top | **75.3 m above street — the true architectural top** | published |
| Entry floor / podium | 6.1 m above (east) street; full-width great steps climb it | published |
| Rose window | 7.6 m wide, centered on the east front above the doors, center ≈ 27–28 m up | published dia; height inferred from photos |
| Anchor (footprint bbox center) | **lon −122.4134968, lat 37.7918332** | measured; see REPORT for the final anchor incl. the east steps offset |

**Plan disagreements (resolved here):**
1. The plan's `targetHeightM: 53` treats the towers as the top. The flèche —
   a major, photo-verified feature the plan never mentions — rises to 75.3 m.
   The model includes it; `targetHeightM` becomes **75.3** so the app's
   scale-to-height keeps every other storey at true size.
2. The plan's palette gives all roofs `Toy_roofd` (dark gray). Close-up and
   flank photos show brown-copper standing-seam roofs. The model uses a muted
   copper-brown (`Toy_roofc`, off-palette WARN) + the palette `Toy_verdigris`
   flèche, which also rescues the model from the all-gray deadness the plan
   itself warns about (§2.15).

## Orientation

Long axis bearing 81.0° cw from true north; the twin-tower entrance front with
the rose window faces ~E (bearing 81°) onto Taylor Street; polygonal apse at
the west end; north transept arm is slightly longer than the south one
(footprint v +23.8 / −19.6 m about the bbox center). Authored world-true:
Blender +Y = north, +X = east.

## What each side shows (photo observations)

- **East (hero):** full-width double flight of steps to the entry terrace; one
  dominant central portal in a crocketed gabled porch holding the gold
  Ghiberti doors, flanked by two small side doors at the tower bases; the
  7.6 m rose in a heavy circular molding above; an open arcade gallery band
  spanning the center bay above the rose; the nave gable peak visible behind
  it between the towers.
- **Towers:** massive corner buttresses with set-offs; a tall belfry stage
  with two deep paired pointed openings per face (bells visible in the north
  tower); flat crown parapet with four corner turrets. No spires.
- **North/south flanks:** 6 aisle bays of tall paired lancets between engaged
  stepped buttress piers with pinnacle caps; clerestory band above the
  lean-to aisle roof; the transept gable (big pointed window) interrupts the
  rhythm; a small clock face on the north tower base (omitted at this scale).
- **West:** narrower, slightly lower choir block (3 bays), then a polygonal
  apse with radiating buttresses; ground rises westward (Nob Hill), so the
  podium story shrinks toward the west.
- **Top:** steep nave gable ridge at 39.6 m with transept ridges at the same
  height crossing it; lower lean-to aisle roofs; lower choir ridge and the
  faceted apse half-cone; the verdigris flèche with gold cross at the
  crossing; brown-copper roof color; buttress combs along both flanks.

## Recognition cues (ranked)

1. Twin flat-crowned Gothic towers over a full-width flight of steps
2. The big rose window centered between them above the gold doors
3. The verdigris flèche + gold cross at the crossing of a long cruciform body
4. Repeating engaged-buttress comb down both flanks
5. Warm gray stone body with brown-copper steep roofs

## Preserve / simplify

**Preserve:** true footprint (95.8 × 43.4 m at bearing 81°), tower:ridge:flèche
height trio (53 / 39.6 / 75.3 m), cruciform plan with unequal transept arms,
rose at true 7.6 m, podium + full-width east steps, buttress rhythm (6 nave
bays), gold doors accent, verdigris flèche.

**Simplify:** tracery → one recessed lancet per bay; rose → ring + 12 chunky
spokes + glass disc (the Chartres 12-scheme is documented); belfry pairs →
two deep pointed recesses per face; crockets/statuary/gargoyles deleted;
tower turrets → simple octagonal posts with pyramid caps; arcade gallery →
recessed colonnette band; clock omitted; apse → 5 facets.

## Night appearance

Photos and the app's dusk system drive: 7,290 sq ft of stained glass lit from
within (warm amber panes down both flanks and around the apse), the floodlit
rose reading cooler and brighter than the windows, warm uplight in the portal,
and the flèche lantern stage as a small warm beacon. Glow set:
`Toy_mustard_Glow` lit panes in every window, `Toy_white_Glow` rose tracery,
`Toy_gold_Glow` portal tympanum + flèche lantern liner. Every glow surface is
a thin separate shell inset behind its opaque glazing (per the loader's
12%-opacity unlit-overlay behavior), never a primary surface.

## Uncertainties

- Nave ridge 39.6 m is derived, not directly published — consistent with
  photo proportions (ridge clearly below the 53 m towers).
- Rose center height (27–28 m) and aisle/clerestory eave heights are photo
  inferences.
- Whether the apse carries small true flyers is unresolved from available
  photos; engaged radiating buttresses modeled (conservative).
- OSM `height=53` describes the towers only; no published figure contradicts
  75.3 m as the overall top (Wikipedia's own infobox uses 247 ft).
