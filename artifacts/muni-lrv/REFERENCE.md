# muni-lrv — reference dossier

Research behind the SF-SIM miniature of San Francisco's Muni Metro light rail
vehicle, the **Siemens S200 SF**, which SFMTA calls the **LRV4**.

The task brief said to verify the plan's dossier rather than trust it. Five of
its claims did not survive contact with the sources; §3 and §4 record what
replaced them, and §8 lists every correction in one place. The model follows the
corrected reading.

No copyrighted imagery is reproduced here. Every reference is a link to its
source; the photographs studied are identified by their Wikimedia Commons file
names so anyone can pull the same frame.

---

## 1. Identity

| | |
|---|---|
| Manufacturer designation | Siemens **S200 SF** |
| Operator designation | **LRV4** |
| Operator | San Francisco Municipal Transportation Agency (SFMTA), Muni Metro |
| Fleet numbers | **2001–2249** |
| Order | 219 vehicles |
| First revenue service | **17 November 2017** |
| Delivery window | 2016–2026 |

Fleet numbers carry a cab suffix in service — `2059A`, `2024B`, `2037A` are all
visible in the photographs below. The suffix identifies **which end** of the
double-ended car is leading, which is itself evidence for §3.

---

## 2. Verified dimensions

| Item | Value | Source |
|---|---|---|
| Length | **22.86 m** (75 ft) | Wikipedia S200; CPTDB — "75 feet (23 m)" for the SF variant |
| Width | **2.650 m** (104.32 in) | Wikipedia S200 |
| Height, pantograph locked down | **3.51 m** (11 ft 6 in) | CPTDB / SamTrans wiki |
| Height range over roof equipment | 3.5–4.1 m (all S200 variants) | Wikipedia S200 |
| Floor height | **0.85 m** | Wikipedia S200, SF-specific |
| Articulated sections | **2, one articulation** | Wikipedia S200 |
| Doors | **8 plug doors — 4 per side** | Wikipedia S200; SFMTA LRV4 blog |
| Weight | 35,730 kg (78,770 lb) | CPTDB |
| Max speed | 80 km/h (50 mph) | CPTDB |
| Capacity | ~203 per car (SF configuration) | CPTDB |
| Current collection | **Faiveley single-arm pantograph**, 600 V DC | Wikipedia S200 / Muni Metro |
| Bogies | Bo′(2)′Bo′ — powered, unpowered centre, powered | Wikipedia S200 |
| Track gauge | 1,435 mm standard | Muni Metro |

**On the plan's "22.86 m × 2.65 m × ~3.6 m".** Length and width hold exactly. The
height figure is the loose one: the sourced number is **3.51 m with the
pantograph locked down**, and the 3.5–4.1 m band in the S200 infobox spans every
operator's variant, not San Francisco's. The model is built to 3.51 m of body and
roof equipment, with the pantograph rising above that — see §6.

**Gauge is modelling trivia here, not placement data.** There is no track in this
scene (transit README, "no rails, no overhead wires, no cable slot"). It matters
only in that it sets the wheel spacing on the model itself, and it is worth
recording that Metro is standard gauge while the cable cars are narrow gauge
(1,067 mm), so the two families' wheels genuinely sit at different widths.

---

## 3. The open question, closed: the LRV4 is DOUBLE-ENDED

The plan's §2.4 flagged this as unresolved and warned that "a wrong answer here
is visible from every angle and doubles or halves the cab budget". It is
resolved, and the answer is the expensive one.

**The S200 SF has an operator cab at each end and runs in both directions.**

- Wikipedia's S200 article gives the vehicle as bi-directional with **2 cabs**.
- CPTDB describes the S200 as "designed for bi-directional operation".
- The fleet-number suffixes `A` and `B` in the photographs are the two cab ends.
- Muni Metro has no turning loops on most of its alignments; bidirectional
  operation is why the design exists.

**Consequence for the model: there is no blank rear.** The rear elevation is a
second cab, and the vehicle is symmetric end-to-end about the articulation. Two
things follow, and they pull in opposite directions:

- *Cost:* the cab — the most expensive geometry in the asset — is built twice.
- *Saving:* section B is section A mirrored, so the build script authors one
  section and mirrors it. That also satisfies the brief's requirement that the
  two sections be "separable and symmetric about the joint" for a future runtime
  that bends the train around curves.

Net effect on the budget is close to neutral, because the mirror costs no
authoring effort and the plan's triangle split already allocated for two
sections. What it does change is that **the rear render is not a freebie** — it
is a second view of the hardest geometry in the asset and gets equal scrutiny.

---

## 4. What the photographs actually show

Studied from Wikimedia Commons, all of the SF fleet:

| File | Establishes |
|---|---|
| `Muni_Metro_outbound_L_Taraval_Siemens_LRV4_(S200)_heading_to_SF_Zoo.jpg` | front three-quarter **on a surface street in mixed traffic**; cab livery; pantograph raised; destination sign |
| `Siemens_LRV4_at_Muni_Metro_East,_San_Francisco_(42754084164).jpg` | full side elevation; flank composition; door spacing; articulation; pantograph folded |
| `Muni_1080_and_LRV4_from_above_at_Muni_Metro_East,_July_2019.jpg` | elevated three-quarter; roof value; cab roof cap |
| `Two-car_LRV4_train_testing_at_Embarcadero_station,_May_2018.JPG` | **coupled pair**; coupler gap; cab-to-cab geometry |
| `Side_view_of_LRV4_truck_at_Muni_Metro_East,_July_2019.jpg` | bogie behind the skirt |
| `Door_of_Muni_LRV4_during_testing,_April_2019.jpg` | door leaf proportions |

### 4.1 The cab — a red horseshoe, which the plan does not mention

This is the single most important finding in the dossier.

The plan's §2.4 describes the front as "a rounded, forward-raked face dominated by
a single large dark windshield… Red Muni accent below the glass", and §2.7 item 7
asks for a red band "sweeping up across the cab fascia".

What every photograph shows is a **bold red U — a horseshoe — framing the entire
windshield**: red across the top of the cab above the destination sign, down both
A-pillars, and turning in under the bottom corners of the glass. The white
bodyside meets it along a diagonal that runs down and back toward the skirt.

The red frame is not an accent on the cab. **It is the cab's graphic identity**,
and it is what makes an LRV4 recognisable at a glance from the front or the front
three-quarter — which is the angle the app's camera spends most of its time at.
A model that puts a thin red band under the windshield and calls it done gets the
single most legible feature of this vehicle wrong.

Inside the horseshoe, top to bottom:

1. a white roof cap curving over the top of the cab;
2. the fleet number in black on the white cap (`2059A`);
3. a black sign panel carrying the amber dot-matrix destination readout;
4. the large dark windshield, one pane, raked back and curved in plan;
5. a black lower fascia carrying the headlight clusters, the red `muni` worm,
   and the yellow `STOP / DO NOT PASS` legend;
6. a grey skirt and the coupler.

### 4.2 The flank — five horizontal bands, not a silver slab

Top to bottom on the side elevation:

| Band | Value | Approx. height |
|---|---|---|
| Roof | white / palest grey | — |
| Upper bodyside | **near-white pale silver** | to ~2.65 m |
| Window band | **near-black**, continuous | ~1.75–2.65 m |
| Lower bodyside | near-white pale silver | ~1.35–1.75 m |
| **Red band** | broad, full length | ~1.00–1.35 m |
| Skirt | **medium grey**, darker than the body | ~0.45–1.00 m |
| Bogie shadow | near-black, recessed | below 0.45 m |

The red band runs the full length low on the body and then **sweeps up at each
cab** to become the horseshoe of §4.1. So the plan's "sweeping up across the cab
fascia" is right about the side and wrong about the front: the sweep is real,
but it terminates in a frame around the windshield rather than a band under it.

The `muni` worm sits in red on the pale bodyside between the window band and the
red band, near each cab. The fleet number sits in black at the top of the
bodyside just under the roof edge.

### 4.3 Doors — four per side, and **not** evenly spaced

SFMTA states it directly: "LRV4 trains have four doors on each side of the train,
two single doors at either end of the cab and two double doors in the middle of
the train." The side elevation confirms it.

So the arrangement per side is, from the cab: **single — double — double —
single**, symmetric about the articulation, with the singles tucked close behind
each cab and the doubles straddling the middle of each section.

The plan's §2.6 asks for "4 chunky `Toy_ink` recesses per side, evenly spaced".
The count is right and is not even a simplification — four per side is the real
number. The **spacing is wrong**: evenly spacing them discards a real, visible
rhythm that costs nothing to keep, and the singles-at-the-ends pattern is part of
how the vehicle reads as an LRV rather than a bus.

### 4.4 The roof and the pantograph

The roof is the **lightest value on the vehicle** — white to palest grey, clearly
lighter than the flanks and much lighter than the skirt. The plan's §2.8 instinct
to make the roof a lighter value than the body is not a stylistic liberty; it is
what the vehicle looks like.

The pantograph is a **single-arm (Z) pantograph**, folded flat when down and
rising to the wire when up. It is mounted on the roof of one section, set back
from the cab — roughly a third to 40% of the way along the car, not at the
midpoint and not over the cab. Roof equipment boxes sit fore and aft of it, low
and wide, in the same pale value as the roof with darker grille faces.

### 4.5 The articulation

A dark, deeply ribbed bellows, visibly **narrower than the body** so it reads as a
recess rather than a continuation. The roofline crosses it as a real step — the
pale roof stops, the dark bellows crosses, the pale roof resumes. That step is
what makes the articulation legible from directly above, which the plan
correctly identifies as the view that matters.

### 4.6 The coupled pair

Two cars couple **cab to cab**, nose to tail, with the cab faces roughly 0.6–1.0 m
apart and the coupler and its rubber buffers filling the gap. There is no
gangway between coupled cars — the pair is two complete vehicles, not a longer
one. A coupled pair is therefore **2 × 22.86 m plus the coupler gap ≈ 46.3 m**,
consistent with the plan's 45.7 m (150 ft) figure for a two-car train.

---

## 5. Recognition cues, ranked

1. **The red horseshoe around the cab windshield** — the identity of the vehicle.
2. **Length**: a very long, low, pale vehicle with a continuous dark window band.
3. **The pantograph on the roof** — the read from the app's aerial camera.
4. **The broad red band low on the flank**, sweeping up at each end.
5. **The articulation** breaking the body into two, visible as a step in the roof.
6. A low skirt hiding the wheels — it does not read as a heavy-rail train.

---

## 6. Miniature translation

**Preserve**

- 22.86 m × 2.65 m at real scale; body and roof equipment to 3.51 m
- 2 sections, 1 articulation, symmetric end to end
- **Two cabs** — double-ended (§3)
- The red horseshoe on both cabs (§4.1)
- Four doors per side in the real single–double–double–single rhythm (§4.3)
- A roof lighter than the flanks, a skirt darker than them (§4.2)

**Simplify / exaggerate**

- The cab's compound curvature becomes chamfered planes, not a lofted surface —
  the toy style wants faceted, and a lofted cab would eat the whole budget
- The pantograph is exaggerated well past scale in arm thickness and simplified
  to a single-arm Z with a chunky contact bar; at true scale the arms are a few
  centimetres of tube and vanish at the app's camera distance
- The bellows gets fewer, deeper ribs than reality so the step reads from above
- Bogies reduce to wheel discs behind a solid skirt
- Door hardware, couplers beyond a simple block, interiors, seats and the
  `STOP / DO NOT PASS` legend are all dropped — invisible at any app distance
- The `muni` worm is kept as a small red mark: it is four strokes and it is the
  cheapest possible "this is Muni and not a generic tram"

---

## 7. Palette

Corrected from the plan's §2.8 to match §4.2. The plan's scheme — mid-silver
body, dark ink skirt, white roof — inverts the real tonal order of the skirt and
would also lose the red band's dominance.

| Material | Hex | Used for |
|---|---|---|
| `Toy_white` | `#f2efe8` | roof, cab roof cap |
| `Toy_lrvbody` | `#dcdcd8` | bodysides — pale silver, one step below the roof |
| `Toy_steel` | `#9aa0a6` | skirt, roof equipment, pantograph |
| `Toy_munired` | `#c1272d` | the horseshoe, the flank band, the worm |
| `Toy_ink` | `#2e2b28` | window band reveal, doors, bellows, wheels, fascia |
| `Toy_glass` | `#26405e` | windows, windshield, door glazing |
| `Toy_mustard_Glow` | `#d9a441` | destination sign face, interior ceiling strip |
| `Toy_white_Glow` | `#f7f4ec` | headlights |
| `Toy_red_Glow` | `#c4453c` | tail lights |

`Toy_munired` and the glass value are carried over from `muni-bus` deliberately,
so the two Muni vehicles read as one fleet; that asset's REPORT §2 records why
each deviates from the palette. `Toy_lrvbody` is new: the palette has no
near-white silver, and `Toy_white` is needed for the roof one step above it.

**The silver-slab risk the plan warns about is real but is not solved by three
greys.** Four of the seven horizontal bands on this vehicle are not grey at all —
the near-black window band and the broad red band do most of the work. The value
separation between roof, body and skirt is the supporting structure, not the
main event.

---

## 8. Corrections to the plan's dossier

| # | Plan said | Sources say | Where |
|---|---|---|---|
| 1 | Rear end unresolved; "verify whether the LRV4 is double-ended" | **Double-ended, two cabs.** No blank rear exists | §3 |
| 2 | Red is an accent band below the windshield | Red is a **horseshoe framing the whole windshield** — the vehicle's identity | §4.1 |
| 3 | Doors "evenly spaced" | **single–double–double–single**, symmetric about the articulation | §4.3 |
| 4 | Skirt dark (`Toy_ink`), body mid-silver | Skirt is **medium grey**, body is **near-white**; the dark band is the windows | §4.2, §7 |
| 5 | Height "~3.6 m" | **3.51 m** pantograph down; the 3.5–4.1 m band is all S200 variants, not SF | §2 |

A sixth, softer one: the plan's §2.7 massing recipe puts the pantograph on
"Section A's roof" at an unspecified position. The photographs place it about a
third of the way along the car from one cab, not at the midpoint.

---

## 9. Uncertainties

- **Exact band heights on the flank** are read off photographs, not drawings. The
  values in §4.2 are ±0.1 m. Nothing in the asset depends on more precision than
  that.
- **Roof equipment layout** is partly obscured in every available overhead frame;
  the model composes two low pale boxes with darker grille faces fore and aft of
  the pantograph, which matches what is visible without inventing detail that
  cannot be checked.
- **Coupler gap** of 0.6–1.0 m is scaled off the Embarcadero photograph rather
  than a published figure. The coupled-pair render uses 0.8 m and the figure is
  stated in `REPORT.md` so it can be corrected.
- **Which cab leads** is a service matter, not a modelling one. The asset is
  symmetric, so `front = −Z` is satisfied by either end; the `−Z` end is the one
  whose destination sign carries the route.

---

## 10. Sources

- [Siemens S200 — Wikipedia](https://en.wikipedia.org/wiki/Siemens_S200) — dimensions, sections, doors, pantograph, floor height, bi-directional operation, two cabs, bogie arrangement, delivery
- [Muni Metro — Wikipedia](https://en.wikipedia.org/wiki/Muni_Metro) — fleet, surface lines, gauge, 600 V DC
- [LRV4: What You Need To Know — SFMTA](https://www.sfmta.com/blog/lrv4-what-you-need-know) — **door arrangement: four per side, singles at the cab ends, doubles in the middle**
- [SFMTA — Muni transit](https://www.sfmta.com/muni-transit) — the five-family taxonomy
- [Muni Color Schemes Through the Years — SFMTA](https://www.sfmta.com/blog/muni-color-schemes-through-years) — the red-and-silver livery lineage; the three candidate LRV4 exterior designs ("Gate", "Presidio", "Skyline")
- [San Francisco MUNI 2001-2249 — CPTDB Wiki](https://cptdb.ca/wiki/index.php/San_Francisco_MUNI_2001-2249) — SF-specific length, width, height pantograph-down, weight, capacity, fleet numbers
- Wikimedia Commons photographs listed in §4
- This repository: `docs/asset-plans/transit/README.md`, `app/src/agents.js`,
  `app/public/sf-assets/vehicles_manifest.json`, `artifacts/muni-bus/`
