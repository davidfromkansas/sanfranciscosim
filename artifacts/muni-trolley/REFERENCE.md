# Muni 40-foot trolley coach — reference dossier

Research behind `muni-trolley-40`, the SF-SIM miniature of San Francisco's
40-foot electric trolley coach, **New Flyer Xcelsior XT40**.

Compiled 12 August 2026 by verifying the plan's dossier
(`docs/asset-plans/transit/trolley-coach.md` §2) against primary and secondary
sources rather than trusting it. **Three of its claims did not survive** — see
§8. Values marked *inferred* are derived or visual estimates.

No copyrighted imagery is reproduced here; photographic references are linked.

---

## 1. Sources and what each one establishes

### Agency publications

- **[SFMTA — Muni's Electric Trolley Buses](https://www.sfmta.com/getting-around/muni/munis-electric-trolley-buses)**
  — power collection is by "trolley poles on the roof of the bus"; the fleet is
  the largest ETB fleet in the US and Canada; the New Flyer vehicles were phased
  in 2015–2019 replacing the ETI fleet; modern trolley buses carry a battery
  that lets them run off-wire and reroute.
- **[SFMTA — VIDEO: New 40' Trolleys Hit San Francisco Streets](https://www.sfmta.com/blog/video-new-40-trolleys-hit-san-francisco-streets)**
  — the 40-foot trolleys entered service on lines including the **3 Jackson, 1
  California and 5 Fulton**; they have upgraded battery power and greater
  off-wire range; the operator can **re-attach the poles to the wires from the
  driver's seat** if they dewire.
- **[SFMTA — Muni Color Schemes Through the Years](https://www.sfmta.com/blog/muni-color-schemes-through-years)**
  — the current livery is **"Silver & Red", 1995–present**. Same scheme as the
  hybrid coach; this is the source that settles §5.
- **[SFMTA — Muni Trolley Coach Upgrade and Expansion](https://www.sfmta.com/projects/muni-trolley-coach-upgrade-and-expansion)**
  — in-motion charging trials: the coaches can run **4–6 miles off-wire** before
  returning to the overhead, at up to 40 mph.

### Fleet and specification references

- **[San Francisco Municipal Railway fleet — Wikipedia](https://en.wikipedia.org/wiki/San_Francisco_Municipal_Railway_fleet)**
  — XT40 **5701–5885, 185 coaches, built 2017–2019**, Presidio and Potrero
  divisions. XT60 **7201–7293, 93 coaches, 2015–2018**, Potrero.
- **[Trolleybuses in San Francisco — Wikipedia](https://en.wikipedia.org/wiki/Trolleybuses_in_San_Francisco)**
  — the system is **15 lines**, ~300 trolleybuses, **600 V DC** on **parallel
  overhead lines**; per-line rolling stock (the XT40/XT60 split in §7);
  21 Hayes ended 20 June 2025, 3 Jackson suspended.
- **[streetcarmike.com — Muni New Flyer Xcelsior XT40 5701–5885](https://www.streetcarmike.com/muni_newflyer_xcelsior_5700.html)**
  — a photo archive of individual coaches. Confirms the 5701–5885 block arrived
  from 2018 with **Vossloh Kiepe** electrical equipment, and documents specific
  units (including **5743**) in service on lines 1, 2, 5, 6, 24, 30, 41 and 45.
- **[New Flyer Industries XT40 — SamTrans Wiki](https://samtrans.fandom.com/wiki/New_Flyer_Industries_XT40)**
  — Muni ordered 185 XT40s for 2017–2019 delivery on a joint contract with King
  County Metro; **New Flyer worked with Vossloh Kiepe, and the inverters and
  resistors sit on the roof AHEAD of the current collector.** This is the single
  most useful sentence in the dossier for the roof composition (§5).

### Trolley pole geometry

- **[Trolley pole — HandWiki](https://handwiki.org/wiki/Engineering:Trolley_pole)**
  — "trolleybuses must use **two** trolley poles and dual overhead wires, one
  pole and wire for the positive 'live' current, the other for the negative or
  neutral return"; trolleybus poles are **longer than tram poles**, to exploit
  the vehicle not being on a fixed path; poles are raised and lowered by a rope
  from the back, with a "trolley catcher" or "trolley retriever".
- **[Trolleybus UK — overhead](http://www.tbus.org.uk/overhead.htm)** (secondary
  citation; the site's TLS chain would not verify from this machine, so the
  figures below are taken from search summaries and cross-checked, not read
  first-hand) — **the two wires are spaced 610–700 mm apart**, and are hung the
  same distance apart and the same height over the road, **typically 18–20 ft
  (5.5–6.1 m)**.
- General trolley-pole literature — the pole is a **tapered tube, 3–6 m**, on a
  **sprung base** on the roof, tipped by a **grooved carbon shoe on a swivel**
  that runs under the wire.

---

## 2. Verified dimensions

| Item | Value | Confidence |
|---|---|---|
| Model | New Flyer Xcelsior **XT40**, electric trolleybus | Confirmed — three independent rosters |
| Fleet numbers | **5701–5885** (185 coaches, 2017–2019) | Wikipedia + streetcarmike |
| Body | **Identical Xcelsior shell to the XDE40 hybrid**: 12.19 m nominal / 12.50 m over bumpers × 2.59 m | New Flyer Xcelsior platform |
| Height, roof sheet | ~3.20 m | Xcelsior published |
| Height over roof equipment | ~3.4 m | Xcelsior published (non-diesel powertrain figure) |
| **Height over raised poles** | **~5.7 m** — set by the wire, not the bus | Derived, §4 |
| Power | Two trolley poles, two-wire overhead, **600 V DC** | SFMTA / Wikipedia |
| Off-wire | Battery, **4–6 miles** at up to 40 mph | SFMTA project page |
| Doors, floor, wheels | As the hybrid: two double-leaf doors, low floor, 0.52 m tyre radius | Shared platform |

**Authored length: 12.19 m**, matching `muni-bus-40` exactly — the two vehicles
share a shell, and authoring them at different lengths would be the divergence
this asset exists to avoid. The reasoning for taking the nominal-class figure
over the 12.50 m over-bumpers figure is in the bus's `REFERENCE.md` §2 and
applies unchanged.

---

## 3. The body: identical, and that is the point

Every side of an XT40 that is not the roof is an XDE40. Same Xcelsior shell,
same wrapped windshield, same window band, same two double-leaf doors, same
Silver & Red livery, same worm, same four-digit fleet number, same destination
sign, same mirrors.

This is why the build script imports `artifacts/muni-bus/build_muni_bus.py`
rather than restating it. The differences are exactly four:

| # | Difference | Verified by |
|---|---|---|
| 1 | **Two trolley poles** on a plinth over the rear axle | Every source; §4 |
| 2 | **More roof electronics**, all forward of the poles | SamTrans Wiki: inverters and resistors sit on the roof ahead of the current collector |
| 3 | **No engine louvre band** on the rear panel — there is no engine | Derived from the vehicle being electric |
| 4 | Routes: trolleybus lines only | §7 |

---

## 4. Pole geometry — the part that had to be worked out

The plan's §2.4, §2.7 and §2.14 give three mutually inconsistent figures: poles
"6.0 m long", "angled 30° above horizontal", and an overall model height of
"~5.5 m". A 6 m pole at 30° off a 3.5 m roof base puts its tip at **6.5 m**, not
5.5 m, and trails **5.2 m** behind the mounting point — which on a base 2.5 m
forward of the tail is 2.7 m of pole hanging past the bumper.

So the plan's numbers cannot all be satisfied, and the model has to pick. It
picks by anchoring on the one figure that is a real physical constraint:

> **The wire is 5.5–6.1 m above the street, and the shoe has to be at the wire.**

That single constraint sets the tip height. Everything else follows:

| Quantity | Authored | Basis |
|---|---|---|
| Base plinth, top of roof | 3.22 → 3.34 m | on the roof crown |
| Pole pivot | 3.52 m | inside a 0.25 m spring housing |
| Pole length | **3.60 m** | see the note below |
| Pole angle | **38° above horizontal** | tip lands at 3.52 + 3.60·sin38° = **5.74 m** — inside the real 5.5–6.1 m wire band |
| Base spacing | **0.60 m** | the real 610–700 mm two-wire spacing |
| Splay | **4°**, tips ~1.00 m apart | readable as two from above without reading as damage |
| Base radius / tip radius | **0.095 / 0.062 m** | ~3.7× the real ~50 mm tube. §6 |
| Plinth position | **9.45 m aft of the nose** | over the rear axle (9.56 m), 2.74 m forward of the tail |
| Shoe | 0.30 × 0.17 × 0.11 m wedge | shoe + harp, compressed |

**The pole length is compressed, deliberately, and it is the one place this
asset departs from measurable reality.** A real XT40 pole is 5–6 m and its shoe
sits well behind the rear bumper when running. Authored at that length the tip
lands 2–3 m beyond the tail, which does three bad things at once:

1. it breaks the vehicle contract's "origin centred in the X/Z footprint" —
   a 14.5 m bounding box on a 12.2 m body puts the origin over a metre off;
2. at `carScale = 1.6` that is **4.8 m of thin pole projecting into the vehicle
   behind** in a traffic queue, which is a visible intersection artefact;
3. `dims[2]` in the manifest would read 14.5 m for a coach with a 12.2 m road
   footprint, which is what a later integration pass would space traffic by.

Shortening to 3.60 m at a steeper 38° keeps **the same tip height** — 5.74 m
either way, because tip height is what the wire fixes — and keeps the whole
assembly inside the body's own length. What is lost is horizontal reach; what is
kept is the vertical clearance above the roof (2.2 m, i.e. 65% of the body
height), which is what actually carries the silhouette. Style bible §26 names
this exact move: "deliberate compression of reality, not arbitrary cartoon
distortion".

Recorded so it is not mistaken for a measurement error. See `REPORT.md` §3.

---

## 5. What each side shows

**Front** — indistinguishable from the hybrid coach below the roofline:
wrapped near-black windshield, amber destination sign in its hood, silver
fascia with the four-digit fleet number and the red worm, headlights at the
outer lower corners, red lower band across the fascia, big mirrors. Above the
roofline, **two poles rise clearly into the sky** — from a low angle they are
the only tell, and from the app's aerial they are unmissable.

**Sides** — the hybrid's window band, doors, livery and worm, unchanged. The
pole pair projects up and aft off the rear third of the roof.

**Rear** — the hybrid's rear window and tail-light stacks, and the red cant band
wrapping the tail **without the hybrid's engine louvre band across it**. That
absence is recognition cue 5.

**Top** — the differentiating view, and the one the app's camera spends its time
on. Front to back: a clean white front cap, a pale hatch, the large louvred HVAC
mass, the dark electronics box (bigger than the hybrid's, per SamTrans Wiki),
then the **dark pole plinth carrying two pale bases and two poles trailing aft**,
then a second hatch on a clean white run to the tail.

---

## 6. Semantic scale: why the poles are 3.7× too thick

A real trolley pole is a ~50 mm tube. The app's diorama camera has an **18°
vertical field of view** (`main.js`, `camera.fov = 18` in toy mode) over a
1080 px viewport, at a **42° down pitch** (`camera.js`, `DIORAMA.pitch`) and a
minimum distance of **150 m** (`DIORAMA.min`).

At 150 m an 18° vertical FOV covers 47.5 m over 1080 px — **44 mm per pixel**.
A 50 mm scale-accurate pole at `carScale = 1.6` is 80 mm across: **1.8 px at the
closest the player is ever allowed to get**, and sub-pixel everywhere else. It
would render as intermittent aliasing, not as a pole.

Authored at 0.095 m radius the pole is 0.19 m across, 0.30 m at 1.6×, i.e.
**6.9 px at 150 m and 8.6 px at the 120 m the transit README budgets against**.
That is a line, not a shimmer.

Style bible §9 sanctions exactly this ("if an object disappears at the intended
camera distance but carries meaning, enlarge or simplify it") and the plan's
§2.15 asks for it aggressively. A thicker variant was built and rejected — see
`REPORT.md` §5.

---

## 7. Routes — where the two coach families actually differ

This is the detail that pays for itself, and the plan's dossier got it wrong.

Per [Trolleybuses in San Francisco](https://en.wikipedia.org/wiki/Trolleybuses_in_San_Francisco),
the current lines split by vehicle:

| Rolling stock | Lines |
|---|---|
| **XT40 — this asset** | **1 California · 2 Sutter · 6 Hayes/Parnassus · 22 Fillmore · 24 Divisadero · 31 Balboa · 33 Ashbury/18th Street · 45 Union/Stockton** |
| XT60 (articulated, out of scope) | 5 / 5R Fulton · 14 Mission · 30 Stockton · 49 Van Ness/Mission |
| Suspended | 3 Jackson · 21 Hayes (ended 20 June 2025) |

The three signs built are `1 CALIFORNIA`, `22 FILLMORE` and `24 DIVISADERO` —
each confirmed XT40 on its own Wikipedia line article
([1 California](https://en.wikipedia.org/wiki/1_California_(bus_line)),
[22 Fillmore](https://en.wikipedia.org/wiki/22_Fillmore),
[24 Divisadero](https://en.wikipedia.org/wiki/24_Divisadero)),
and lines 1 and 24 are additionally photo-documented on 5701–5885 coaches in the
streetcarmike archive.

Fleet number **5743** is in the block and appears in that archive.

---

## 8. Corrections to the plan's dossier

**8.1 Three of the plan's six suggested destination signs are the wrong
vehicle.** The plan's §"The destination sign" offers `49 VAN NESS`,
`1 CALIFORNIA`, `22 FILLMORE`, `30 STOCKTON`, `14 MISSION` and
`24 DIVISADERO`. Of those, **49 Van Ness/Mission, 30 Stockton and 14 Mission are
XT60 articulated lines** — the vehicle the plan's own §2.16 puts out of scope.
Signing a 40-footer with them is the same class of error the bus asset caught
with `38 GEARY`, and it is invisible unless someone checks the roster per line.

**8.2 `49 VAN NESS` does not "belong here" after all.** The plan's §2.15 moves
it from the hybrid bus plan to this one, on the correct observation that it is a
trolleybus route. It is — but it is an **XT60** trolleybus route, so it belongs
to the deferred articulated variant, not to either 40-footer. The plan's
suspicion that Van Ness BRT construction had shifted it to motor coach is not
what the current roster shows.

**8.3 The pole figures are internally inconsistent.** §2.7's 6.0 m at 30° and
§2.14's "~5.5 m" model height cannot both hold. §4 above resolves it by
anchoring on the wire height, which is the only one of the three that is a
physical constraint rather than a modelling choice.

**8.4 The plan's §2.4 and §2.7 disagree on the splay.** §2.4 says the poles
converge toward the tips; §2.7 says they splay 4° apart. Since the wires they
would run under are parallel at 610–700 mm, real poles are essentially parallel.
The model splays 4°, taking §2.7, because a small divergence is what makes the
pair read as two poles rather than one thick one from the aerial camera — and
1.00 m at the tips is still visibly "coupled equipment" rather than damage.

**8.5 A smaller one: the trolley coach's roof is busier than the plan expects.**
§2.9 lists "HVAC pod, electrical box, hatches, then the pole plinth". The
SamTrans Wiki sentence about inverters and resistors ahead of the current
collector says the electronics mass is a genuine difference from the hybrid, not
a carry-over — so the model enlarges it rather than copying the hybrid's.

---

## 9. Preserve / simplify

**Preserve**

- The Xcelsior body, imported unmodified from `muni-bus`
- Two poles, two bases, mounted over the rear axle, trailing aft
- The 0.60 m base spacing — it is the real two-wire spacing and the top view
  exists to show it
- Tip height inside the real 5.5–6.1 m wire band

**Simplify / exaggerate**

- Pole diameter 3.7× real (§6)
- Pole length compressed 3.6 m from 5–6 m real (§4)
- Shoe and harp become one chunky wedge; no harp wire detail
- Spring/pivot housing becomes one beveled cylinder each
- Retractor rope omitted — it will not read at any distance the app offers, and
  it would not survive the shrink pass
- No `_Glow` at the shoe: real shoes spark intermittently, and a permanently
  lit one reads as a rendering bug

---

## 10. Uncertainties

- **Exact pole length on the XT40 specifically** is not published by New Flyer
  or SFMTA and could not be sourced. The 3–6 m range is general trolley-pole
  literature. The model's 3.6 m is at the short end of that range and is a
  deliberate compression regardless (§4), so a firmer figure would not change
  the model — but it would change how §4 is worded.
- **Wire height** is cited at 18–20 ft from a UK trolleybus reference whose TLS
  chain would not verify from this machine, cross-checked against a US
  restatement of the same 18–20 ft figure. SFMTA does not publish its own.
- **Exact plinth position** is visual, from photographs of the pole assembly
  sitting over the rear axle. No dimensioned drawing was found.
- **Livery on the trolley fleet is assumed identical to the hybrid fleet**, on
  SFMTA's own statement that Silver & Red is the agency scheme since 1995, and
  on photographs of 5701-block coaches. No source describes a trolley-specific
  variation, and none of the photographs shows one.
