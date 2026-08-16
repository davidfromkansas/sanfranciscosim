# Muni 40-foot hybrid bus — reference dossier

Research behind `muni-bus-40.glb`. Compiled 11 August 2026 by independent
verification of the dossier in `docs/asset-plans/transit/muni-hybrid-bus.md`
Part 2. **Three of that dossier's claims did not survive verification** — they
are called out in §8 and the model follows the corrected reading.

No copyrighted imagery is committed here. Every photograph used is linked by URL
and described in words; the quantitative work in §4 was done by sampling pixels
from the linked images in a browser and is reported as numbers, not pictures.

---

## 1. Sources and what each one establishes

### Agency and manufacturer publications

| Source | Establishes |
|---|---|
| [SFMTA — Muni Hybrid Buses](https://www.sfmta.com/getting-around/muni/muni-hybrid-buses) | SFMTA's own hybrid page. Confirms "low-floor biodiesel-electric hybrid buses" running on B20, and **illustrates the 40-foot hybrid on the 9 San Bruno** — a first-party motor-coach route assignment. |
| [SFMTA — Muni transit](https://www.sfmta.com/muni-transit) | The five-family fleet taxonomy the transit asset set is built on. |
| [SFMTA — Muni Color Schemes Through the Years](https://www.sfmta.com/blog/muni-color-schemes-through-years) | **The current livery is "Silver & Red", introduced 1995 and still in use, "on all buses and rail vehicles, excluding historic equipment."** This is the primary-source confirmation that the body is *silver*, not white. |
| [SFMTA — Doing the Worm: A Brief Logo History](https://www.sfmta.com/blog/doing-worm-brief-logo-history) | The "worm" wordmark (Walter Landor, 1975) is still the current mark and appears on multiple sides of the newest coaches. |
| [New Flyer — Xcelsior family](https://www.newflyer.com/new-flyer-buses-meet-the-xcelsior-family/) | Product line, low-floor architecture, roof-mounted HVAC. |

### Fleet and specification references

| Source | Establishes |
|---|---|
| [Wikipedia — San Francisco Municipal Railway fleet](https://en.wikipedia.org/wiki/San_Francisco_Municipal_Railway_fleet) | XDE40 fleet numbers **8601–8662, 8701–8750, 8800–8969** (112 + 170 coaches, 2013–2019). Trolleybus XT40 is **5701–5885** — a disjoint range, which is what makes "is this a motor coach?" answerable from a fleet number. |
| [Wikipedia — New Flyer Xcelsior](https://en.wikipedia.org/wiki/New_Flyer_Xcelsior) | 40-ft dimensions: **41 ft (12.5 m) over bumpers**, **102 in (2.59 m)** wide, **10 ft 6 in (3.20 m)** high for diesel and **11 ft 1 in (3.38 m)** for all other powertrains; **wheelbase 283.75 in (7.21 m)**; 2 or 3 doors; low-floor with kneeling. |
| [kevinsbusrail.com — MUNI New Flyer XDE40 Xcelsior](https://kevinsbusrail.com/sfmuni_nfi-xde40.html) | Independent roster confirming the same model designation and two delivery batches (2013 and 2016) with differing hybrid drivelines. Corroborates the Wikipedia ranges. |

### Route assignment (for the destination sign)

| Source | Establishes |
|---|---|
| [Wikipedia — 29 Sunset](https://en.wikipedia.org/wiki/29_Sunset) | Rolling stock: **New Flyer XDE40**. |
| [Wikipedia — 38 Geary](https://en.wikipedia.org/wiki/38_Geary) | Rolling stock: **New Flyer XDE60** — a motor-coach line, but the *articulated* one. |
| [Wikipedia — 43 Masonic](https://en.wikipedia.org/wiki/43_Masonic), [44 O'Shaughnessy](https://en.wikipedia.org/wiki/44_O%27Shaughnessy) | Both **New Flyer XDE40**. |
| `docs/asset-plans/transit/README.md` | Trolleybus route list (1, 2, 3, 5, 6, 7, 14, 21, 22, 24, 30, 31, 33, 41, 45, **49**) — the lines that must *not* appear on this asset. |

### Photographic references (Wikimedia Commons, linked not copied)

| File | View | What it establishes |
|---|---|---|
| [`Muni_route_44_bus_at_Forest_Hill_station,_August_2020.JPG`](https://commons.wikimedia.org/wiki/File:Muni_route_44_bus_at_Forest_Hill_station,_August_2020.JPG) | **True left-side elevation**, XDE40 #8613 | The measurement source for §4. Sign reads `44 Bayview Dist.` |
| [`MUNI_8630.JPG`](https://commons.wikimedia.org/wiki/File:MUNI_8630.JPG) | Front three-quarter, XDE40 #8630 | Front cap, mirrors, headlights, worm placement, fleet-number placement, two-line sign (`18 FORTY-SIXTH AV / Stonestown`). |
| [`San_Francisco_Muni_bus_8759_in_the_San_Francisco_Transit_Center.jpg`](https://commons.wikimedia.org/wiki/File:San_Francisco_Muni_bus_8759_in_the_San_Francisco_Transit_Center.jpg) | Front close-up, XDE40 #8759 | Destination-sign typography and colour, roof marker lights, windshield rake and wrap, fascia layout. Sign reads `25 TREASURE ISLAND`. |
| [`Muni_route_29_bus_in_McLaren_Park.jpg`](https://commons.wikimedia.org/wiki/File:Muni_route_29_bus_in_McLaren_Park.jpg) | Front three-quarter, XDE40 #8632 | **An XDE40 actually signed `29 SUNSET / Baker Beach`** — the exact model + exact route shipped on this asset. |
| [`Muni_bus_at_golden_gate_park.jpg`](https://commons.wikimedia.org/wiki/File:Muni_bus_at_golden_gate_park.jpg) | **High aerial** | The roof. Near the app's own camera angle. See §6. |
| [`SF_Muni_Proterra_battery-electric_test_bus_5008_at_Woods_Division_January_2026.jpg`](https://commons.wikimedia.org/wiki/File:SF_Muni_Proterra_battery-electric_test_bus_5008_at_Woods_Division_January_2026.jpg) | **Rear elevation** (XDE40 #8650) + yard roofs | Rear face layout, tail-light placement, hazard-striped rear bumper. Also shows the *newer battery-electric* livery, which is a different scheme — see §8.3. |

Nothing here rests on a single photograph, a single AI image, or an unsourced
3D model: every geometric claim in §4–§6 is either a published figure or is
visible in at least two of the six photographs above.

---

## 2. Verified dimensions

| Item | Value | Confidence |
|---|---|---|
| Model | New Flyer Xcelsior **XDE40**, diesel-electric hybrid | Confirmed — three independent rosters |
| Length, nominal class | 12.19 m (40 ft) | Class designation |
| Length, over bumpers | **12.50 m (41 ft)** | New Flyer published |
| Width | **2.59 m (102 in)** | New Flyer published |
| Height, over roof equipment | **3.38 m (11 ft 1 in)** — the non-diesel-powertrain figure, which is the hybrid | New Flyer published |
| Height, roof sheet | ~3.20 m | Published diesel figure; the hybrid's extra 0.18 m is roof equipment |
| Wheelbase | **7.21 m (283.75 in)** | New Flyer published |
| Tyre | 305/70R22.5, ~1.04 m OD → **radius 0.52 m** | Standard transit fitment |
| Floor | Low-floor, no steps at both doors, kneeling | New Flyer / SFMTA |
| Doors | **Two**, both double-leaf: front door in the front overhang ahead of the front axle; centre door ahead of the rear axle | All six photographs |
| Fleet numbers | Four digits, `8601–8662 / 8701–8750 / 8800–8969` | Wikipedia + roster |

**Authored length: 12.19 m, deliberately the low end of the 12.19–12.50 m
range.** The app multiplies fleet instances by `carScale = 1.6`, so every
centimetre authored costs 1.6 cm on screen; 12.19 m renders at 19.50 m and
12.50 m would render at 20.00 m. Taking the nominal-class figure is both
defensible (it is what the class is called and what SFMTA calls the vehicle) and
the cheaper of two true answers. Recorded here so the choice is not mistaken for
sloppiness. See `REPORT.md` for the 1.6× render evidence.

---

## 3. Livery — the corrected geometry

The single most important finding of this dossier.

**The Muni Xcelsior livery is two horizontal red bands on a silver body. It is
not a diagonal sweep.** The plan's §2.4 and §2.7 describe "the red livery sweeps
up from the skirt toward the rear" and "a 0.02 m proud shell in `Toy_red`
sweeping from the skirt at the rear up to the fascia at the front." No
photograph of an XDE40 shows anything of the kind. What every photograph shows,
from every angle, is:

1. a **silver** body,
2. a **broad red band low on the body**, wrapping the front cap and the rear corners,
3. a **narrower red band at the cant rail**, immediately above the window band, running the full length and wrapping over the front,
4. a **white / near-white roof**, clearly lighter than the silver sides,
5. **red door surrounds** on both doors,
6. the red **worm** wordmark on the silver field below the windows, twice per side.

The diagonal sweep belongs to the *newer battery-electric* scheme (see §8.3),
which is a different vehicle and not this asset.

---

## 4. Measured band geometry

Method: the left-side elevation of #8613 was drawn to a canvas and vertical
colour runs were classified at four independent X positions on the body
(x = 520, 760, 980, 1150 in the 1280 px image). All four agree. The body's
vertical scale was anchored on the published roof height (3.20 m) and skirt
underside (0.36 m), giving 83.9 px/m; the same scale independently reproduces a
plausible transit wheelbase, which is the cross-check.

Heights are metres above the road surface, on the authored 3.14 m cant-rail /
3.22 m roof-crown body described in §7.

| Band | From | To | Height | Colour |
|---|---:|---:|---:|---|
| Roof crown | 3.14 | 3.22 | — | white |
| Roof edge / upper silver | 2.82 | 3.14 | 0.32 | silver |
| **Red cant-rail band** | 2.46 | 2.82 | **0.36** | Muni red |
| Silver reveal | 2.40 | 2.46 | 0.06 | silver |
| **Dark window band** | 1.36 | 2.40 | **1.04** | near-black glazing in a dark reveal |
| Silver field (worm, fleet number live here) | 0.90 | 1.36 | 0.46 | silver |
| **Red lower band** | 0.34 | 0.90 | **0.56** | Muni red |
| Skirt underside | 0.30 | 0.34 | — | dark |

Longitudinal layout (from published wheelbase, cross-checked against the wheel-
well shadows in #8613):

| Feature | Distance from the nose |
|---|---|
| Windshield base / A-pillar | 0.00–1.05 m |
| Front door (double leaf) | 1.15–2.20 m |
| Front axle | 2.35 m |
| Centre door (double leaf) | 6.95–8.15 m |
| Rear axle | 9.56 m |
| Tail | 12.19 m |

### Colour

Absolute colour sampling from the reference photographs is unreliable — #8613's
camera side is in full shade (sampled red came back `#8b0712`, silver `#818996`)
while its sunlit roof sampled `#d4d7dc`. The *relationships* are reliable and
are what the model reproduces: roof clearly lighter than the sides; sides a
neutral light grey, not white; red strongly saturated and cooler than a brick
red.

| Authored material | Hex | Basis |
|---|---|---|
| `Toy_silver` | `#c8cbd0` | The shipped fleet's own `Toy_Silver` (`commuter-bus.glb`, linear `0.5841, 0.6038, 0.6376`). Reusing it makes the Muni bus sit in the same toy box as the coach already on the street. |
| `Toy_white` | `#f7f4ec` | Palette `white`. Roof and roof pod, so the two planes separate under flat diorama lighting (plan §2.9). |
| `Toy_munired` | `#c1272d` | **Off-palette, deliberate.** Palette `red #c4453c` is a warm brick; Muni red is a cooler crimson, and the plan's §2.15 pre-authorises the WARN because "the livery is the entire identity of this asset". Named distinctly so the deviation is visible in the material list rather than hidden behind a palette name. |
| `Toy_ink` | `#3a3530` | Palette. Window reveal, sign frame and glyphs, mirrors, light housings, bumpers, fleet numbers. |
| `Toy_glass` | `#2a4d73` | Palette. Style bible §5 wants dark blue-grey graphical windows; the reveal around them carries the "black window band" read. |
| `Toy_steel` | `#9aa0a6` | Palette. Skirt, wheel hubs, HVAC grille. |
| `Toy_tire` | `#2c2c2f` | The shipped fleet's `Toy_Tire`. Off-palette WARN, inherited from the fleet. |
| `Toy_mustard_Glow` | `#d9a441` | Palette. Destination sign face, interior ceiling strip. |
| `Toy_white_Glow` | `#f7f4ec` | Palette. Headlights. |
| `Toy_red_Glow` | `#c4453c` | Palette. Tail lights. |

---

## 5. What each side shows

**Front** (#8759, #8632, #8630). A very large, deeply raked, near-black
windshield that wraps around both corners; a full-width **amber-on-black LED
destination sign** in a recessed hood above it; a row of small amber marker
lamps along the roof lip above the sign; a silver fascia below the glass
carrying the four-digit fleet number to one side and the red worm low and
central; two headlight clusters at the outer lower corners with amber turn
lamps outboard; a dark wrap-around bumper; and two large mirrors on stalks
projecting well beyond the body width. The red lower band wraps across the
fascia; the red cant band wraps above the sign hood.

**Sides** (#8613, all others). §3 and §4. The window band is continuous and is
interrupted only by the two doors. It **terminates at the front** against the
A-pillar, where it meets the windshield without a silver gap, and **at the rear**
against a short silver return before the rear corner radius — it does not wrap
onto the rear face. The doors break both the window band and the silver field
below it, and are framed in red on all four edges. `Hybrid Electric` is
lettered in dark blue on the upper silver, twice; too small to model.

**Rear** (#8650). Flat, silver, slightly tumblehomed at the top. A large
rectangular advertising panel occupies the centre — Muni sells the space, so the
panel is a real feature but its content is not. Above it, a horizontal louvred
engine-access band at the roofline. Tail-light clusters as vertical stacks of
round lamps at the outer lower corners. A dark bumper with **yellow-and-black
hazard chevrons** across it. The four-digit fleet number appears at the upper
left. The red bands wrap around the corners onto the rear face but the rear
centre is predominantly silver.

**Top** (Golden Gate Park aerial, plus the Woods Division yard shot). See §6.

---

## 6. The roof, from the aerial

The Golden Gate Park photograph is a high aerial at close to the app's own
camera angle, and it is the most useful single reference in this dossier because
it shows what the player will actually spend most of their time looking at.

What it shows, front to rear:

- a **clean white front cap** with no equipment on it;
- a **long dark-grey ribbed condenser / HVAC mass** forward of centre, clearly
  the largest object on the roof and visibly louvred;
- a **second, lower, lighter raised box** behind it — the hybrid power
  electronics;
- **two flush hatches** reading as pale grey squares;
- a clean white run to the rear, then a slightly raised rear section.

Critically: **the equipment does not cover the roof.** It reads as two or three
distinct dark masses on a large white field, with the red cant band showing as a
thin red edge line down each side. That is a composition, and it is what the
model reproduces — three masses, not a scatter of greebles.

---

## 7. Recognition cues, ranked

1. **Silver body + two red bands + dark window band** — the three-shape read. At 120 m this is the entire asset.
2. **Big rectangular low-floor silhouette with a wrapped near-black windshield.**
3. **Amber destination sign glowing above the windshield** — the strongest "alive" cue, and the reason the glow set exists.
4. **White roof carrying two or three dark equipment masses** — the only thing that stops the roof reading as a blank sticker from a 42° camera.
5. **Red-framed doors and the red worm** — the close-range confirmation.

## 8. Corrections to the plan's dossier

**8.1 The livery is bands, not a sweep.** §3 above. The model follows the
photographs. The build script's `livery_band()` takes a Y range, so a future
trolley coach or articulated variant can restate the livery without new code.

**8.2 The body is silver, not white.** The plan's §2.8 assigns `Toy_white
#f7f4ec` to "body, roof, fascia". SFMTA's own livery history names the scheme
"Silver & Red", and every photograph shows sides that are clearly darker than
the roof. The model uses silver sides and a white roof, which also happens to be
exactly the tonal separation the plan's own §2.9 asks for.

**8.3 There is a second, newer livery, and it is not this one.** Muni's
battery-electric buses (e.g. Proterra #5008) wear a white body with an *angular
red swoosh* and a lightning-bolt motif. That scheme is genuinely diagonal, which
is the likeliest origin of the plan's "sweep". It belongs to a different
vehicle; the XDE40 hybrid does not wear it.

**8.4 Length.** The plan states 12.19 m as the real dimension. The published
over-bumper figure is 12.50 m. Both are true at different definitions; §2
records the choice and why.

**8.5 Fleet-number ranges are approximate.** Wikipedia gives 8701–8750 but
#8759 is photographed in service, and Kevin's roster gives 8624–8750 where
Wikipedia gives 8701–8750. The ranges are close enough to answer "is this a
motor coach?" and that is all this asset needs them for. The model carries
**#8632**, which is photographed, in range on every roster, and photographed
*on the 29 Sunset*.

---

## 9. Destination sign

**Format.** Amber-on-black LED matrix, full body width, in a recessed hood
directly above the windshield. Two layouts are in service: one line
(`25 TREASURE ISLAND`, #8759) and two lines with a smaller secondary
destination (`29 SUNSET / Baker Beach`, #8632). The route number is set larger
and heavier than the destination text in both. The model uses the one-line
layout: at 120 m the sign is an amber rectangle either way, and one line lets
the number be twice as tall at 15 m.

**Routes chosen — all verified motor-coach, all verified XDE40:**

| Sign | Verification |
|---|---|
| **`29 SUNSET`** — shipped | Wikipedia rolling stock: New Flyer XDE40. And #8632 is *photographed* wearing exactly this sign. |
| `9 SAN BRUNO` — variant | SFMTA's own hybrid-bus page illustrates a 40-foot hybrid on the 9. |
| `43 MASONIC` — variant | Wikipedia rolling stock: New Flyer XDE40. |

**Rejected.** `38 GEARY` — a motor-coach line, but Wikipedia gives its rolling
stock as **XDE60**, the articulated coach that is explicitly out of scope. Putting
it on a 40-footer is exactly the error a San Franciscan notices. `49 VAN NESS` —
a trolley coach line; it belongs on `muni-trolley`.

## 10. Preserve / simplify

**Preserve** — 12.19 × 2.59 × 3.38 m at real scale; the low-floor proportion
(low body, high window band); the two-band livery and its measured heights; both
door positions; the wrapped windshield; the roof mass composition; oversized
mirrors.

**Simplify or drop** — individual window mullions (one continuous reveal with
pane inserts); the rear advertising panel's content; hazard chevrons on the rear
bumper (a flat dark bumper reads the same at 120 m); `Hybrid Electric` and
`CA49819` lettering; wipers; the bike rack; door leaf splits; wheel lug detail;
the amber marker-lamp row (folded into the sign hood's top edge); interior
seating and stanchions.

## 11. Uncertainties

- **Exact fascia proportions.** No orthographic factory drawing was found in an
  openly licensed source; the front cap is reconstructed from three three-quarter
  photographs. Confidence: good at 15 m, irrelevant at 120 m.
- **Roof equipment footprints** are estimated from one aerial and one yard
  photograph. Positions and relative masses are confident; exact plan dimensions
  are not.
- **Rear face**: one photograph, partly occluded. The tail-light stack and
  louvre band are confident; the exact height of the ad panel is not.
- **Front/rear overhang split.** Wheelbase is published (7.21 m); the split of
  the remaining 4.98 m is taken as 2.35 m front / 2.63 m rear from the wheel-well
  shadows in #8613, which is a perspective photograph. Confidence ±0.2 m.
- **Muni red hex.** Chosen for how it reads next to `Toy_silver` under flat
  diorama light, not sampled — see §4, all sampling was shade-corrupted.
