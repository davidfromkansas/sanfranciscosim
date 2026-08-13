# 362 Brannan Street — reference dossier

Research behind `artifacts/362-brannan/362-brannan.glb`. The plan
(`docs/asset-plans/362-brannan.md`) was the starting point; everything below was
re-verified from source before modelling, and the two corrections that came out of
that re-verification are called out in §7 and repeated in `REPORT.md`.

Compiled 12 August 2026.

## 1. What the building is

362 Brannan Street — also addressed 366 Brannan Street on the front door and
**25 Varney Place** on the back — is a 1925 industrial building on the northwest
side of Brannan in South Beach / SoMa, occupying the whole of block 3775 lot 018
and running the full depth of the block from Brannan to the Varney Place alley.

It still does the work it was built for: **Standard Sheet Metal & Marine
Plumbing** occupies it, which on this block makes it the odd one out. Its
immediate neighbours are a venture-office conversion (370, "Spherecast" /
"Typeform US"), a design showroom (358, "The Natural") and, four doors southwest,
`380-brannan` — a 1908 warehouse turned incubator that is already in this manifest.
362 is the one that never converted.

There is no published history. No architect is recorded in any source consulted,
the architectural press has nothing, and SF Planning's historic surveys returned
nothing. The dossier below is municipal records plus photography, and that is the
honest state of it.

## 2. Sources and what each establishes

| Source | Establishes |
|---|---|
| [OSM way 124890322](https://www.openstreetmap.org/way/124890322) | footprint, `addr:housenumber=362;366`, `building=yes`, `height=6` (`source=Bing`) |
| [DataSF Building Footprints `ynuv-fyni`](https://data.sfgov.org/resource/ynuv-fyni), record `mblr=SF3775018` | the authoritative footprint polygon; the 4.90 m majority / 5.63 m median / **8.58 m max** heights; the neighbour footprints used for the exclusion radius |
| [SF Assessor Secured Roll `wv5m-vpq2`](https://data.sfgov.org/resource/wv5m-vpq2), block 3775 lot 018 | built **1925**, `use_code = IND` (Industrial), 2 storeys, construction type C, lot area 5,279 sq ft, unchanged 2022–2025 |
| [SF Building Permits `i98e-djp9`](https://data.sfgov.org/resource/i98e-djp9), block 3775 lot 018 | three permits only: parapet strengthening 1991-01-02 and 1992-03-25 (the UMB parapet-bracing programme), reroofing 2014-05-20 |
| Google Street View pano `QGmjHr1j26kBQJg4CIIlyQ`, Brannan Street, capture 2025 | the entire SE front: cream stucco, the green steel-sash band, the two frieze diamonds, the green water table, the slot windows, the "366" entrance, the height step, the ribbed roof over the parapet |
| Google Street View pano `zsvZkZZuwu-5Yt5suLIXbQ`, Varney Place, capture 2025 | the NW back: plain cream wall, three roll-up freight doors, the "25 VARNEY PLACE" plaque, an NFPA 704 placard |
| Google Maps satellite, Vexcel imagery 2026 | roof layout: rows of skylights/monitors parallel to the Brannan edge, scattered mechanical units, the sloped front roof reading distinctly from the flat deck |
| [standardsheetmetalsf.com](https://standardsheetmetalsf.com/) and the Yelp listing for "Standard Sheet Metal & Marine Plumbing, 366 Brannan St" | current occupant, address confirmation |

No reference imagery is committed. The Street View panoramas above are the visual
record and are cited by pano id so they can be re-opened.

## 3. Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| WGS84 anchor (footprint OBB centre) | `-122.3937450, 37.7808430` | measured |
| Footprint | 487.0 m2; 20.12 m (SE frontage) x 24.79 m deep | measured, DataSF |
| Footprint as modelled | convex hull of the survey, 7-gon, 489.3 m2 (+0.5%) | derived |
| OSM cross-check | 479.9 m2, 24.39 x 19.67 m | agrees within ~1.5 m |
| Lot area | 5,279 sq ft = 490.4 m2 | assessor — the building covers essentially the whole lot |
| One-storey roof deck | **5.63 m** (`hgt_median_m`) | measured |
| Most common roof height | 4.90 m (`hgt_majoritycm`) | measured |
| Crest / bay roof ridge | **8.58 m** (`hgt_maxcm`) | measured — the model's target, 8.6 m |
| Bay street parapet / eave | ~7.1 m | *inferred*, photogrammetric — see §7 |
| Ground elevation | 9.57 m NAVD88 (`gnd_min_m`) | measured; the app's terrain handles this, not the asset |
| Brannan front heading | **135.9°** true (SE) | measured from the footprint |
| Varney back heading | 315.2° true (NW) | measured |

## 4. Orientation

Authored in true-world orientation: Blender `+Y` = north, `+X` = east, so the GLB
drops into the city at its real heading — `placeGeneric()` in `app/src/assets.js`
scales and positions but never rotates.

The asset contract's "front faces −Y" rule cannot be honoured literally here: the
Brannan front faces **southeast**, not south. Real-world orientation wins
(AGENTS rule 5, and the orientation note in `docs/asset-plans/README.md`); the
deviation is recorded in `REPORT.md`.

Because the building sits ~45° off the world axes like the whole SoMa grid, the
axis-aligned XY bounding box is **31.3 x 30.9 m** for a building that is
20.1 x 24.8 m. That is expected, not a scale error.

Footprint as modelled, in metres relative to the anchor, CCW:

```
(-15.870,   1.705)   west corner
(  1.102, -15.100)
(  2.037, -15.118)   south corner
( 15.392,  -2.180)   east corner
( 14.815,  -1.242)
(  6.729,   7.498)
( -1.735,  15.745)   north corner
```

| Edge | Length | Outward | Elevation |
|---|---|---|---|
| 0 | 23.88 m | SW 224.7° | party wall to 370 Brannan |
| 1 | 0.94 m | S 181.1° | survey jog at the south corner |
| 2 | 18.59 m | **SE 135.9°** | **Brannan Street front** |
| 3 | 1.10 m | NE 58.4° | survey jog at the east corner |
| 4 | 11.91 m | NE 47.2° | party wall to 358 Brannan |
| 5 | 11.82 m | NE 44.3° | party wall, continued |
| 6 | 19.92 m | **NW 315.2°** | **Varney Place back** |

## 5. What each side shows

**Southeast — Brannan Street (front).** Two heights. The southwest end rises two
storeys in cream stucco and carries a continuous band of steel-sash factory
windows: pale multi-light glazing inside a **dark bottle-green** frame and mullion
system, roughly three units of about 6 x 5 lights each. Above it a plain frieze
carries **two dark green diamond lozenges**, then a cornice band, then the ribbed
metal roof sloping up and back behind it. The rest of the frontage is a
single-storey cream wall: a **dark green water-table stripe** at roughly 1.2–1.8 m
running the full width, and four small dark horizontal slot windows set high. The
entrance sits at the step — a narrow glazed aluminium storefront, "366" above it,
the Standard Sheet Metal signboard beside it. A faint ghost sign survives on the
upper wall.

**Northwest — Varney Place (back).** Plain painted cream wall under a continuous
simple parapet. **Three roll-up freight doors** — two dark green corrugated, one
gray — plus a green corrugated infill panel toward the northeast end. No windows.
The "25 VARNEY PLACE" plaque and an NFPA 704 placard. The alley is narrow and this
face is only ever seen obliquely in life, but the app's aerial camera sees it
plainly, so it is built properly.

**Northeast and southwest flanks.** Party walls, hard against 358 and 370 Brannan.
Not visible from any public vantage and not photographable. Built as plain cream
stucco with no openings — inventing a window grid here would be inventing.

**Top.** Predominantly flat light membrane over the one-storey block, with the
low-pitched ribbed metal roof over the bay sloping up away from Brannan. Satellite
shows rows of small dark roof monitors/skylights running parallel to the Brannan
edge, two or three larger gridded skylight panels, and scattered mechanical units.

## 6. Recognition cues, ranked

1. **Cream stucco with dark bottle-green joinery** — band frame, diamonds, water
   table, freight doors. One colour pair carries the whole building.
2. The **steel-sash factory window band** on the raised front bay.
3. The **two green frieze diamonds** — the only ornament, and the thing that makes
   it not-generic.
4. The **two-height massing**, with the ribbed roof sloping up behind the front
   parapet.
5. The green water table with slot windows above it on the long low wall.

### Preserved

The two-height massing and the real 45° heading; the green-on-cream discipline
with no third colour; the window band as one continuous horizontal event; the two
diamonds at readable size; the unbroken water table; three roll-up doors on the
back.

### Simplified

~6 x 5 lights per sash unit become 4 x 3 (finer is sub-pixel from the app's
camera); the diamonds are enlarged to 0.92 m so they survive at thumbnail size —
the one place semantic exaggeration is spent; the water table is thickened to
0.6 m; the slot windows become four identical recessed rectangles; stucco texture,
the ghost sign, downpipes, conduit and signage all disappear; the ribbed roof
keeps seven ribs rather than the real sheet pitch.

## 7. Uncertainties and conflicting evidence

**OSM `height=6` measures the wrong feature.** The tag is `source=Bing` and lands
between the LiDAR majority (4.90 m) and median (5.63 m) — it describes the
one-storey part that covers most of the plan and misses the two-storey bay
entirely. Building to 6 m produces a flat box and loses the whole silhouette.
Resolved: the target is the LiDAR max, 8.58 m → **8.6 m**.

**"2 storeys" is true of about a sixth of the floor plate.** The assessor and the
2014 permit both record 2, and the front bay genuinely is two storeys — but the
LiDAR distribution (majority 4.90 m, mean 5.74 m, std 0.96 m) says most of the
building is one tall industrial storey. Resolved: a one-storey block at 5.6 m with
a two-storey bay on it.

**The crest and the street parapet are different numbers.** DataSF's 8.58 m is the
ridge of the bay's roof, set back from the street. Scaling the Brannan pano off a
sidewalk waste bin and a parking sign — two objects of known height in the same
image plane — puts the *front* parapet at ~7.0–7.1 m; the same photo scaled off
the entrance storefront gives 5.4 m (if it is a bare 2.15 m door) to 7.4 m (if it
is a 2.9 m storefront with transom), which is why the storefront was rejected as a
datum. **Both numbers are modelled**: eave 7.1 m, ridge 8.6 m, and the slope
between them is what reconciles the LiDAR with the photograph.

**The bay's extent is the weakest number here.** Frontage share and depth are
derived from LiDAR area statistics plus oblique photography, not measured. The
LiDAR variance puts the bay at 8–20% of the roof area; photography puts it at
rather under half the frontage. The model uses 9.0 m x 8.5 m = 76 m2 = 16%, where
those two agree. A later source that pins it should override this.

**Google's address point for "362 Brannan St" is on Varney Place**, at the back of
the lot, and the pano it opens looks at a dusty-rose corrugated gate belonging to
the property *across* the alley. Both pano ids are recorded in §2 for this reason.

**Inferred, not verified:** the sash band's unit count and light grid; the number
of slot windows (3–4 visible through street trees); whether the two frieze
diamonds are the only ones or the series continues across the blank upper wall
northeast of the band (trees obscure it); the exact positions of the three rear
freight doors along the Varney wall.
