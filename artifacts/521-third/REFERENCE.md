# 521 Third Street — reference dossier

Compiled 18 August 2026 for `artifacts/521-third/`. The plan behind this asset is
`docs/asset-plans/521-third.md`; this file records what was **verified during the
build**, what was corrected, and what remains inferred. Where the two disagree,
this file and `REPORT.md` win.

## 1. What the building is

521–527 3rd Street, San Francisco 94107 — a 1914 three-storey brick
apartment-over-store block on the east corner of **3rd Street and Taber Place**,
in the Central SoMa / South Beach edge of the South of Market. Fifteen
residential units over two shops: **Neill's Grocery & Liquor** (521, the orange
awning at the Taber corner) and **SouthBeach Food Collective** (521A, the black
fascia over a roll-up shutter), with the residential entries at 521A and 527
between and beside them.

Assessor class **AC — "Apartment & Commercial Store"**; construction type **C**
(masonry). The 1989 permit in the block/lot record reads *"seismic bracing,
parapet bracing, electrical & plumbing"*, the signature of an unreinforced-masonry
retrofit, which is what a 1914 SoMa brick lodging block would have needed.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| DataSF parcels `acdm-wktn`, `blklot 3775072` | The surveyed footprint the asset is built on: a 14.74 × 23.13 m rhombus, 338.8 m², address range **521–527**, zoning CMUO |
| SF Assessor secured roll `wv5m-vpq2`, block 3775 lot 072, rolls 2023–2025 | **1914**, **3 storeys**, 15 units, 25 rooms, class AC, construction type C, lot 3,610 sq ft, **lot depth 76.0 ft**, floor area 10,260 sq ft |
| DataSF LiDAR footprints `ynuv-fyni`, `SF3775072` | Roof deck **10.87 m** (`hgt_majoritycm`; median 10.95, mean 10.98, std 0.96 over 1,309 cells), max 13.53 m, ground 5.66–6.57 m NAVD88 — and every neighbour height quoted below |
| SF building permits `i98e-djp9`, block 3775 lot 072 (9 records, 1989–2024) | 3 storeys throughout; the 1989 seismic/**parapet** bracing; the **1991 awning fabrication** permit that dates Neill's orange awning; the 2014 kitchen hoods; the 2023 fire alarm; the 2024 counter repair |
| OSM way/124884350 | Footprint cross-check (325.4 m²), `height = 11`, `addr:housenumber = 521;523;525;527` |
| OSM node 10874867136 | Neill's Grocery & Liquor, `check_date = 2026-04-26` |
| Google Street View panoramas `8bbQy0YWLwpYOWjU44C52Q` (3rd Street) and `Z7M9DH3anUhr-UCyCfWsJw` (Taber Place mouth), 2025 capture | Both designed elevations, the corner, the cornice and Greek-key band, the bay rhythm, the shopfronts, the mural, the roof-edge davits |
| Google satellite tiles z21 | Flat white membrane roof inside a parapet ring |
| SF business registration `0441146`; CA ABC licence `00554688` | HRD Coffee Shop held 521A from July 2009 to 23 June 2023 — dates the black fascia's predecessor |
| `https://www.hbgrealty.net/soma/` | "521-527 3rd Street" managed as restored historic residential |
| SF Planning, *Central SoMa Historic Context Statement & Historic Resource Survey* (draft, 2015) | The building **type**: post-1906 brick lodging houses and apartment-over-store blocks on 3rd with Classical Revival detailing. No parcel-level rating was located |
| `app/public/tiles/buildings/23_13.bin` (committed bake) | What the procedural city puts here today: ring 98, 330 m², base 5.4 m, top 18.3 m — a **12.9 m** block, 1.5 m taller than the asset |

No paywalled or login-gated source was used, and no copyrighted imagery is
committed to the repo.

## 3. Verified dimensions and location

| | Value |
|---|---|
| Anchor (WGS84) | **-122.3952384, 37.7811509** — the surveyed parcel's oriented-bbox centre |
| Footprint | **14.74 m** (3rd Street) × **23.13 m** (Taber Place), 338.8 m², a rhombus with 90° corners on the 45° SoMa grid |
| Roof deck | 10.90 m (LiDAR mode 10.87, median 10.95) |
| Parapet crest / `targetHeightM` | **11.40 m** |
| Axis-aligned XY bbox of the export | 27.36 × 27.10 m — expected at a 45° heading, plus the 0.50 m cornice overhang |

### Orientation

Footprint in Blender coordinates (metres, +X east, +Y north), CCW, centred on the
anchor:

```
s ( -3.032, -13.320)   S — 3rd Street / SE party wall
e ( 13.368,   2.960)   E — SE party wall / rear
n (  2.998,  13.350)   N — rear / Taber Place
w (-13.372,  -2.950)   W — 3rd Street / Taber Place, the hero corner
```

| Edge | Length | Outward normal | Elevation |
|---|---|---|---|
| s→e | 23.11 m | **135.2°** SE | blind party wall (549 Third) |
| e→n | 14.68 m | **45.1°** NE | rear, block interior |
| n→w | 23.10 m | **315.1°** NW | **Taber Place flank** |
| w→s | 14.64 m | **225.1°** SW | **3rd Street front** |

## 4. What each side shows

**3rd Street (SW, 14.64 m).** Three bands. A shopfront to 3.50 m, capped by the
cream **Greek-key belt band** at 3.55–3.95 m. Above it two storeys of dark brick
in **five bays** — bay 1 a window, **bay 2 the fire-escape door**, bays 3–5
windows — with plain rectangular openings, cream surrounds, dark 1-over-1 sashes,
and a **black fire escape** on bay 2 (a landing at each floor and a diagonal
flight between). Recessed **basketweave brick panels** on the end piers at the
2nd/3rd floor spandrel and in a row under the top corbel course. The wall is
closed by a **corbelled brick band → dentil course → heavy cream cornice →
dark-brick parapet lip**, and a dark coping. The shopfront reads left to right:
Neill's orange awning and glazing on a brick bulkhead, a projecting black-and-
orange **blade sign** near the corner, the recessed 521A residential entry, the
black SouthBeach fascia with its round emblem over a **steel roll-up shutter**
carrying a tag, then the small mustard awning over the 527 apartment door.

**Taber Place (NW, 23.10 m).** The same three bands, demoted. The Greek-key band
runs the **full** length; the cornice group only **returns 6.2 m** from the
corner and then stops, leaving a plain brick parapet for the rest. Below the band
the ground storey is painted **stucco**, not brick, carrying a **mural and
graffiti**. Above it, plain brick with three punched windows per floor near the
corner, four vent openings per floor behind them, two **downpipes**, and a
secondary fire escape near the rear end.

**Rear (NE, 14.68 m).** No public vantage reaches it. **Inferred**: plain brick,
four small utility openings per upper floor and one downpipe, matching the far
end of the Taber flank.

**Party wall (SE, 23.11 m).** Blind. It abuts 549 Third, which stands 1.6 m
taller — but 549 Third is **absent from the committed bake**, so this face will
be seen in the app. It is modelled as honest blank brick with the coping running
across it; no openings were invented for it.

**Roof.** Flat pale membrane inside a parapet ring under a dark coping. The
roof-edge **hoist davit frame and ladder** on the 3rd Street parapet — the thing
the 13.53 m LiDAR maximum is actually measuring — plus a stair head, two
mechanical cabinets with a duct run, two roof lights, five vents, four flues and
two drains.

## 5. Recognition cues, in priority order

1. The **cream cornice + Greek-key band pair** — two bright horizontal lines on a
   dark red box, both turning the corner. Nothing else on the block face has them.
2. The **orange Neill's awning** at the corner: the only saturated colour for a
   hundred metres.
3. The **black fire escape on the middle bay** of the 3rd Street front.
4. The **dark red-brown brick**, read against 501 Third's brighter brick across
   the alley.
5. The **mural wall down Taber Place** — from the aerial camera this is what says
   the building has a second designed side.

## 6. Simplified deliberately

- The Greek-key meander is a row of shadow ticks, not a modelled fret, and only
  on the 3rd Street elevation.
- The basketweave brick panels are flat recessed rectangles, not woven courses.
- The fire escapes are one landing + three uprights + a four-tread flight each.
- The mural is five abstract flat shapes, not the 2025 piece (which is ephemeral).
- The shopfront lettering is not modelled at all — signage reads as coloured
  fields, per the style bible's semantic-scale rule.

## 7. Corrections made against the plan

1. **Palette.** The plan's §2.7 put the body in `Toy_brick` (c96f4a). Both
   `Toy_brick` and `Toy_rust` render as salmon terracotta at the app's exposure
   and destroy the value contrast against the cream bands, which is the
   building's whole graphic read. The body is **`Toy_oxblood` (7a4034)**, the
   recessed panels **`Toy_cocoa` (6b4a3d)** — a recessed panel reads darker than
   its wall, and `Toy_rust` panels looked like blocked-up windows.
2. **Taber stucco.** The plan specified `Toy_peach` (e8cdc9). It is so close to
   `Toy_cream` that the Greek-key band vanished into it. Changed to
   **`Toy_p_tan` (d8a878)**.
3. **Lit windows.** The plan specified `Toy_gold_Glow` for the lit upper windows.
   A `_Glow` material's base colour is also its daytime colour, and gold over
   `Toy_glass` tinted the facade yellow by day. Changed to **`Toy_glass_Glow`**.
4. **Roof furniture height.** The plan asked for a stair bulkhead. The 11.40 m
   crest leaves only 0.50 m above the deck, so the roof reads through **plan area
   and value** — wide low blocks with dark caps, long ducts and a dark coping
   ring — rather than through height. Recorded in REPORT.md.
5. **Triangle budget.** The plan's 10,000 cap holds (8,848), but only after the
   44 dentil teeth and 26 meander ticks were left hard-edged: a beveled 12-triangle
   panel costs ~60, and beveling those 70 repeats alone spent a quarter of the
   budget on edges no camera resolves.

## 8. Remaining uncertainties

- **The 11.40 m crest is estimated**, not published — see `docs/asset-plans/521-third.md`
  §2.16 for the photogrammetric fit and §2.15 risk 2 for the error budget.
  Manifest entry carries `"estimated": true`.
- **The rear elevation is inferred** in full.
- **The mural and the shopfront tenants are ephemeral.** The orange awning dates
  to a 1991 permit and is the durable part; the lettering is not, and is not
  modelled.
- **No parcel-level historic rating was located** for 3775/072.
