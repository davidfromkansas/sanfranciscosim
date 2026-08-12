# F Market & Wharves PCC streetcar — reference dossier

Research for `artifacts/f-line/`, compiled 12 August 2026 against the task in
[`docs/asset-plans/transit/historic-streetcar.md`](../../docs/asset-plans/transit/historic-streetcar.md).

The plan's Part 2 dossier was treated as a hypothesis, not as source. Everything
below was re-verified; where this dossier **disagrees** with the plan it says so
in bold and gives the source. Values marked *inferred* are visual or derived
estimates.

No copyrighted imagery is reproduced here — only links and the facts they carry.

---

## 1. Sources and what each establishes

| Source | Establishes |
|---|---|
| [SFMTA — Muni transit](https://www.sfmta.com/muni-transit) | the five-family fleet taxonomy the transit plans are built on |
| [Wikipedia — F Market & Wharves](https://en.wikipedia.org/wiki/F_Market_%26_Wharves) | fleet composition and counts; the "cities series" concept; route (Castro → Market → Embarcadero → Fisherman's Wharf) |
| [Wikipedia — San Francisco Municipal Railway fleet](https://en.wikipedia.org/wiki/San_Francisco_Municipal_Railway_fleet) | **hard dimensions per class**, builders, build years, single/double-ended |
| [Wikipedia — PCC streetcar](https://en.wikipedia.org/wiki/PCC_streetcar) | generic dimension range, weights, seating, post-war window/door pattern, truck type, wheel diameter, gauges |
| [Market Street Railway — the streetcar fleet](https://www.streetcar.org/streetcarroster/) | the operational roster car by car with the city livery each wears |
| [Market Street Railway — complete roster](https://www.streetcar.org/wp-content/uploads/sfmsr/streetcars/roster.html) | per-car service status |
| [Market Street Railway — paint schemes selected for the "new" PCCs](https://www.streetcar.org/muni_selects_paint_schemes_for_new_pccs/) | **colours in words** for Muni "Wings", Dallas, Market Street Railway |
| [Market Street Railway — rebuilt PCC 1050 honours St. Louis](https://www.streetcar.org/rebuilt-pcc-1050-heads-sf-honoring-st-louis/) | **1050 = "the red and cream livery of St. Louis Public Service Company"** |
| [Market Street Railway — car 1063, Baltimore](https://www.streetcar.org/streetcars/1063-1063-baltimore-md/) | **1063 = "Alexandria Blue (a teal shade) and Picador cream, with an orange stripe and a Pearl gray roof"** |
| [Market Street Railway — car 1061, Pacific Electric](https://www.streetcar.org/streetcars/1061-1061-pacific-electric/) | **1061 = red, Daylight orange and silver** — three colours, and therefore the clearest documented rejection |
| [Market Street Railway — car 1052, Los Angeles Railway](https://www.streetcar.org/streetcars/1052-1052-los-angeles-railway/) | LARy was "the Yellow Car system"; "two-tone yellow cars", "a simple livery" |
| [Market Street Railway — "Boston" is back](https://www.streetcar.org/boston-is-back/) | 1059's BERy hue: the first restoration's "red-orange" was "at odds with the actual Boston hue" |
| [Market Street Railway — car 1055, Philadelphia](https://www.streetcar.org/streetcars/1055-1055-philadelphia-ptc/) | 1055 wears its own as-delivered 1948 green **with cream and red trim** |

Nothing here rests on a single photograph, a single AI image, or an unsourced
3D model. Every colour claim traces to a Market Street Railway page that names
the colours in words; the hex values in §5 are this dossier's translation of
those words into the project palette and are marked as such.

---

## 2. Verified dimensions — and where the plan is wrong

`historic-streetcar.md` §2.1 gives the generic PCC range, 14.02–15.39 m, and its
manifest draft proposes `targetLengthM: 14.0`. That is the **bottom of the
generic range for the type worldwide**, not a San Francisco car. The Muni fleet
page gives per-class figures:

| Class | Origin | Built | Operational | Length | Width | Height | Ends |
|---|---|---|---:|---|---|---|---|
| **1050** | Philadelphia Transportation Co. | 1947–48 | **13** | **48′5″ = 14.76 m** | **8′4″ = 2.54 m** | **10′3″ = 3.124 m** | single |
| 1070 | Twin City Rapid Transit → Newark | 1946–47 | 11 | 46′5″ = 14.15 m | 9′0″ = 2.74 m | 10′3″ = 3.124 m | single |
| 1006–1015 "Big Ten" | Muni | 1948 | 8 | 50′5″ = 15.37 m | 9′0″ = 2.74 m | 10′1″ = 3.07 m | **double** |
| 1040 "Baby Ten" | Muni | 1952 | 1 | 46′5″ = 14.15 m | 9′0″ = 2.74 m | 10′3″ = 3.124 m | single |

**Decision: model the 1050 class**, and author at **14.76 × 2.54 × 3.124 m**.
It is the largest operational class, it is single-ended, and its height is the
same 10′3″ as two of the other three, so the silhouette generalises.

Height is measured **rail to the top of the roof crown**. The trolley pole and
the roof ventilators stand above it, so the model's bounding box is taller than
3.124 m; §7 records both figures.

Other verified figures used in the build:

- Wheels **26 in = 0.66 m diameter** (PCC streetcar trucks).
- **Standard gauge 4′8½″ = 1.435 m** — the F line is standard gauge, visibly
  wider than the cable cars' 1.067 m, which is a real recognition cue between
  the two heritage assets.
- Truck centres ≈ 21 ft = 6.4 m, truck wheelbase 75 in = 1.905 m. *inferred*
  from PCC practice; not separately sourced.
- Weight 37,990 lb for the 1050 class — not modelled, recorded for completeness.

---

## 3. Single- or double-ended

The SF fleet contains both. Counting operational cars:

- single-ended: 13 (1050 class) + 11 (1070 class) + 1 (1040) = **25**
- double-ended: 8 (the "Big Ten" torpedoes)

**Single-ended**, and specifically the 1050 class. Consequences the model
follows:

- one cab, one windscreen, **one central headlight** at the front only;
- the rear is a rounded but blanker lid with a rear window and tail lights, no
  second headlight and no second route board;
- doors on the **right side only** — front door behind the nose and a centre
  door — because a single-ended car only ever loads kerbside.

The nominal front for the `−Z` contract is therefore unambiguous: the cab end.

---

## 4. What each side shows

**Front.** A rounded, forward-leaning nose. The windscreen is two panes with a
narrow centre post and it **wraps around** onto the front corners rather than
stopping at a flat face. A single headlight, low and dead centre in the fascia.
A metal anti-climber below it. The route board sits above the windscreen, under
the roof edge. The roof crown curves down to meet the top of the nose.

**Sides.** A long flank of rectangular windows in a regular rhythm, recessed
behind the body skin, broken by the two doors on the kerb side and unbroken on
the blind side. The post-war pattern is front door / seven windows / side door /
four windows / two rear quarter windows, with small standee windows above.

**Rear.** A rounded lid, a rear window, tail lights. No cab.

**Roof.** This is the surface the app's 42° camera sees most of, and it is where
the plan's dossier is thinnest. Two things it does not say and that matter:

1. The roof is **light** — Baltimore's 1063 wears a "Pearl gray roof", Dallas's
   1009 a "silver roof". PCC roofs are painted metal, not dark.
2. A **drip rail** runs each roof edge, and a line of small ventilators runs the
   crown. The trolley pole base stands about a third of the way back from the
   cab and the pole trails rearward.

**Night.** The single headlight, a lit route board, tail lights, and warm
incandescent light from a lit saloon spilling out of the top of the window band.
These are 1940s cars: the interior light is noticeably warmer than a modern
LRV's.

---

## 5. The liveries — chosen, and rejected

Muni's PCCs wear the colours of past PCC operators; Market Street Railway counts
22 cities and 29 liveries across the fleet. The model carries one **tinted**
body colour plus a **fixed** cream letterboard, silver roof and dark trim, so a
livery only qualifies if it reads with **one** body colour.

### Chosen — five

| Livery | Car | Source colours | Tint | Why it survives the one-colour constraint |
|---|---|---|---|---|
| Muni **"Wings"** 1948 | 1006, 1008 | "green and cream 'Wings' livery … as delivered new to Muni in 1948" | `#2f7a55` | green body + cream band. The home livery; the F line's own. |
| **St. Louis** Public Service | 1050 | "the red and cream livery of St. Louis Public Service Company" | `#c4453c` | red body + cream band. On-palette (`red`). |
| **Boston** Elevated Railway | 1059 | BERy orange with cream; MSR notes the first restoration's "red-orange" was wrong for "the actual Boston hue" | `#e0762f` | orange body + cream band. *The exact BERy orange is inferred* — MSR names the hue as a correction, not as a value. |
| **Los Angeles** Railway | 1052 | "the Yellow Car system"; "two-tone yellow cars … a simple livery" | `#e0af35` | a two-tone yellow collapses cleanly to one tinted yellow against the fixed cream. |
| **Baltimore** Transit | 1063 | "Alexandria Blue (a teal shade) and Picador cream, with an orange stripe and a Pearl gray roof" | `#3f9aa8` | blue-teal body + cream band + grey roof — the model's fixed trim *is* this livery. The orange pinstripe is dropped (§6). |

Hex values are this dossier's translation of the named colours into the project
palette; `#c4453c` is the contract's `red` verbatim, the other four are chosen to
sit in the contract's saturation range. They are proposals for the integration,
not measured paint samples.

### Rejected — and why

| Livery | Car | Reason |
|---|---|---|
| **Pacific Electric** | 1061 | "red, orange, and silver … inspired by the 'Daylight' train colors". Three saturated colours in a swept pattern. One instance tint cannot express it, and faking it with the fixed cream reads as neither. |
| **Market Street Railway** "zip stripe" | 1011 | "bright yellow roof, while retaining the solid white ends". The identity is in the **roof** and the **ends**, both of which are fixed materials on this model. |
| **Dallas** Railway & Terminal | 1009 | "predominantly red scheme with cream trim and silver roof" — would work, except it is a *double-ended* torpedo, and this is the single-ended 1050 class. Kept as the strongest candidate if a double-ended car is ever built. |
| **Philadelphia** PTC | 1055 | "1948 green livery with cream and red trim" — three colours, and its green would duplicate Muni "Wings" anyway. |
| **Newark** | 1070 | The identity cue is the **red wheels** ("Ruby Slippers"), and wheels are fixed `Toy_roofd`. |

Recording these matters as much as the choices: the plan's §2.16 flags
"one-colour liveries are a real constraint" as a risk to discover *before*
modelling, and five of the fleet's best-known schemes genuinely fail it.

---

## 6. Recognition cues, ranked

**Family**

1. Colourful vintage railcars against modern San Francisco — the liveries.
2. A trolley pole trailing back over the roof.

**PCC specifically**

3. Rounded streamlined nose and crowned roof.
4. Single central headlight.
5. Regular rhythm of rectangular side windows behind a recessed band.

---

## 7. Preserve, simplify, drop

**Preserved**

- The 1940s streamline read: rounded nose that leans out over the anti-climber,
  crowned roof curving down into it, wrapped two-pane windscreen.
- Single central headlight, low in the fascia.
- Real 14.76 m length at real scale, standard gauge 1.435 m.
- The silver roof, its drip rails and its ventilator line — the app's camera
  looks down at 42°.
- Trolley pole with base, tapered shank and shoe.

**Simplified**

- The nose is nine lofted rings, not a lofted NURBS surface — faceted enough for
  the toy language, curved enough not to be a tram.
- Ten window panes a side, in rhythm rather than the real irregular pattern.
- The trolley pole shank is thickened well past scale (75 mm base radius against
  a real car's ~30 mm); a scale pole is sub-pixel at the app camera.
- Trucks are a dark frame with the wheels outboard; no bolsters, springs or
  motors.

**Dropped, with the reason**

- **Standee windows.** Real and characteristic, but they are a 0.2 m band of
  glazing above a 0.66 m band, and at the app's camera distance they merge into
  the window band they sit over. The band reads; the sub-band does not.
- **Fleet numbers and system lettering.** The contract forbids textures, and
  extruded four-digit numerals on both flanks would cost more triangles than the
  entire running gear for something illegible past 20 m. The route letter **F**
  on the front board is extruded, because it is one glyph in the one place the
  eye goes.
- **The orange pinstripe** on the Baltimore livery, and pinstriping generally: a
  third colour by definition.
- Interior, seats, driver, passengers, coupler, retriever, rails, overhead wire.

---

## 8. Uncertainties

- **The Boston orange is inferred.** Market Street Railway describes 1059's hue
  by correcting a wrong one rather than by naming it. `#e0762f` is a judgement.
- **Truck centres and wheelbase are inferred** from general PCC practice, not
  from a 1050-class drawing. They affect only where the wheels sit under a
  skirted flank.
- **The plan's `targetLengthM: 14.0`** is superseded by 14.76 m (§2). If the
  integration wants one length for every heritage car regardless of class, that
  is a deliberate choice to make, not a measurement.
- **Roof ventilator count** is styled (seven stations, one omitted where the
  pole plinth stands), not counted from a photograph.
- **The trolley pole angle is a deliberate deviation** from the plan's 5.5 m at
  30°; see `REPORT.md`. There being no overhead wire in the scene changes what
  the pole should look like, and the plan's own §2.16 anticipates the question
  without settling the geometry.
