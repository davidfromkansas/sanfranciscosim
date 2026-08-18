# 521 Third Street — build report

Asset: `artifacts/521-third/521-third.glb`
Plan: `docs/asset-plans/521-third.md`
Dossier: `artifacts/521-third/REFERENCE.md`
Built 18 August 2026, Blender 5.2.0 LTS, headless.

## What shipped

| | |
|---|---|
| Manifest id | `521-third` (→ registry `521Third` via `camelId()`, verified) |
| Anchor (WGS84) | `-122.3952384, 37.7811509` — surveyed parcel oriented-bbox centre |
| `targetHeightM` | **11.40 m** — the parapet crest; `"estimated": true` |
| Category | `2` (apartments — `CAT.apartments`, 15 residential units over two shops) |
| `loadRadius` | 2500 m (`max(2500, 11.4 × 30)`) — streamed, not `alwaysLoaded` |
| Camera preset | `{ distance: 200, yaw: 270, pitch: 28 }` |
| Case | **B** — new landmark; needs the `pipeline/lib/landmarks.mjs` entry and a re-bake |

## Reproducing

```
blender -b --python artifacts/521-third/build_521_third.py
blender -b --python artifacts/521-third/render_521_third.py -- \
        --glb <abs>/521-third.glb --out <abs> --prefix 521-third
blender -b --python artifacts/521-third/render_521_third.py -- \
        --glb <abs>/521-third.glb --out <abs> --prefix 521-third --night
python3 artifacts/521-third/make_contact_sheet.py
blender -b --python artifacts/521-third/validate_521_third.py -- \
        --glb <abs>/521-third.glb --out <abs>/validation.json
```

The build script takes absolute paths from its own location; the render and
validate scripts need absolute `--glb`/`--out` (Blender's image writer resolves
relative paths against the blend, not the cwd, and fails silently-ish).

## Design decisions, and where they depart from the plan

**REPORT beats plan.** Five corrections were made during the build; all are also
recorded in `REFERENCE.md` §7.

1. **Brick colour.** The plan's §2.7 put the body in `Toy_brick` (`c96f4a`).
   Both `Toy_brick` and `Toy_rust` render as salmon terracotta at the app's
   exposure, which destroys the value contrast against the cream cornice and
   Greek-key band — and that contrast is the building's entire graphic read at
   city scale. Body is **`Toy_oxblood` (`7a4034`)**.
2. **Recessed panels.** `Toy_rust` basketweave panels read as blocked-up
   windows: a *recessed* panel reads darker than its wall, not lighter. Changed
   to **`Toy_cocoa` (`6b4a3d`)**, and the spandrel panels were made wider and
   shorter (1.15 × 0.46 m) so they stop reading as openings.
3. **Taber Place stucco.** The plan specified `Toy_peach` (`e8cdc9`), which is
   so close to `Toy_cream` that the Greek-key band vanished into it along the
   whole alley elevation. Changed to **`Toy_p_tan` (`d8a878`)**.
4. **Lit windows.** The plan specified `Toy_gold_Glow`. A `_Glow` material's
   base colour is *also* its daytime colour, and the app draws the glow layer
   over the opaque surface — gold over `Toy_glass` tinted the facade yellow by
   day. Changed to **`Toy_glass_Glow` (`6f95b8`)**, which reads as a lit window
   at night and as a lighter pane by day.
5. **No stair bulkhead.** The plan asked for one. The 11.40 m parapet crest is
   the manifest datum and the deck sits at 10.90 m, so there are only **0.50 m**
   between them — nothing on this roof can be tall. The roof therefore reads
   through **plan area and value** instead of height: a dark coping ring drawing
   the outline, a wide low stair head with a dark cap, two dark mechanical
   cabinets, three long duct runs, two roof lights, five vents, four flues and
   two drains. See "The davit question" below.

## The davit question

The DataSF LiDAR maximum on this footprint is **13.53 m**, 2.63 m above the
10.87 m roof-deck mode. The 2025 Street View capture shows a **hoist davit frame
and roof ladder** standing proud of the 3rd Street parapet, and that is what the
maximum is measuring.

Two readings were available:

- make the davits the crest, `targetHeightM` ≈ 12.4–13.5 m; or
- make the **parapet** the crest at 11.40 m and model the davits co-terminal
  with it.

The second was chosen, matching the convention every sibling on this street uses
(592 Third: *"the tallest geometry in the export (the parapet crest) must land at
exactly 8.2 m"*). It keeps `targetHeightM` equal to the architectural parapet —
which is the number the photogrammetry and the LiDAR mode both measure, and the
number the app shows on the building card — and it keeps the street silhouette
honest, which is the view the app spends most of its time in. The davits are
modelled from the deck to exactly 11.40 m, so they read as a frame against the
membrane from the aerial camera and do not change the bbox.

## Geometry

| | |
|---|---|
| Footprint | surveyed parcel `3775072`: 14.64 × 23.10 m rhombus, 338.8 m², 90° corners on the 45° SoMa grid |
| Objects | 255 |
| Triangles | **8,848** (plan cap 10,000; AGENTS landmark cap 30,000) |
| Bounding box | X −13.968 … 13.393, Y −13.659 … 13.442, Z 0 … **11.400** |
| Dimensions | 27.361 × 27.101 × 11.400 m |
| XY centre offset | (−0.288, −0.108) m — the cornice projects 0.50 m on two of four sides, so the mass centre is not the wall centre |
| min Z | 0.000 |

The 27.4 × 27.1 m axis-aligned XY box on a 14.6 × 23.1 m building is the expected
consequence of the ~45° real-world heading, not a scale error.

### Triangle budget, as spent

A beveled 12-triangle panel costs about 60 triangles. The first build came in at
**12,604** because the 44 dentil teeth and 26 Greek-key ticks were being beveled —
a quarter of the whole budget spent on edges no camera at city distance resolves.
Leaving those 70 repeats hard-edged, plus trimming the fire escapes from four
posts to three and from five treads to four, brought it to 8,848 with every
silhouette-carrying mass still softened at 0.10 m / 2 segments.

## Materials

Fourteen, all `Toy_*`, all flat, no textures, no transparency, no `Toy_body`:

`Toy_oxblood` (body, parapet), `Toy_rust` (spare warm brick), `Toy_cocoa`
(recessed panels), `Toy_cream` (cornice, dentil band, Greek-key band, window
surrounds), `Toy_greige` (roof membrane, dentil shadow ticks, stair head, ducts),
`Toy_p_tan` (Taber stucco), `Toy_cobalt` + `Toy_mint` (mural), `Toy_glass`
(glazing), `Toy_ink` (sashes, fire escapes, black fascia, entries, coping,
mechanical cabinets, downpipes, tag), `Toy_orange` (Neill's awning, blade sign),
`Toy_mustard` (527 entry awning), `Toy_steel` (roll-up shutter, davits, ladder,
vents), plus glow: `Toy_orange_Glow`, `Toy_glass_Glow`.

`Toy_roofd` was deliberately **not** used on the roof deck — it renders near-black
in the app (measured rgb(9,9,12) on a comparable deck) and this roof is a light
membrane.

## Night state

Hero glow is the **orange Neill's awning and its projecting blade sign** at the
Taber corner. Supporting glow is the shopfront glazing behind them and the
SouthBeach fascia. Ambient glow is four of the ten 3rd Street upper windows plus
one on Taber — never all of them. The Taber Place flank is otherwise dark, which
is what an alley elevation does.

Every glow shell is a thin panel proud of the opaque surface it sits on, never a
closed shell around the building: the app draws `_Glow` in a separate layer at
`opacity = 0.12 + 0.95·uNight`, so a closed shell is two such layers (~23 % tint)
by day and would wash the facade.

## Review renders

Seven images plus a contact sheet, all rendered from the **re-imported GLB**, not
from the authoring scene:

`521-third-north.png`, `-east.png`, `-south.png`, `-west.png` (four orthographic
elevations, one rig, identical scale/lighting/exposure, differing only in
azimuth), `-top.png`, `-aerial.png` (72 mm, 38° down, azimuth 270°),
`-aerial-night.png`, `-contact-sheet.png`.

**The `west` view is the hero.** Because the building sits at 45° to the world
axes, the west orthographic camera looks straight at the 3rd Street / Taber Place
corner and carries both designed elevations in one frame. The aerial uses the
same azimuth, which is also the manifest camera preset's `yaw: 270`.

## Validation

See `validation.json` — re-import into a fresh, isolated Blender scene, then the
full `sf-asset-check` contract, per-object signed-volume normals test, and a
31,500-ray visibility residual test.

## Known limitations

1. **The 11.40 m crest is estimated.** Two independent measurements agree
   (LiDAR roof-deck mode + a visible parapet, and a Street View photogrammetric
   fit giving 11.3–11.6 m in the LiDAR frame), but nothing published states it.
   `"estimated": true`.
2. **The rear (NE) elevation is inferred in full** — no public vantage reaches
   it. It is modelled as plain brick with eight small utility openings and one
   downpipe, matching the far end of the Taber flank.
3. **The SE party wall is blank.** It abuts 549 Third in reality — but 549 Third
   is **absent from the committed bake**, so this face will be visible in the app.
   It is left as honest blank brick rather than given invented openings. This is
   a pre-existing gap in the procedural city, not something this asset causes.
4. **The mural and the shopfront tenants are ephemeral.** The mural is five
   abstract flat shapes, not a portrait of the 2025 piece. Neill's orange awning
   dates to a 1991 permit and is the durable part; the lettering is not modelled
   at all.
5. **The fire escape reads busy in the flat orthographic elevation.** It is the
   correct read from the aerial camera the app actually uses, and it is the
   third-strongest recognition cue, so it stays.

## Approval

The pipeline invocation for this building was:

> BUILDING: 521 3rd St, San Francisco, CA 94107
> BATCH: yes
> APPROVE EVERYTHING DONT ASK ME FOR PERMISSION

That is a standing pre-approval covering gate 0 and gate 3, given by the owner on
**18 August 2026** before the work started. The renders above are presented as
the gate-3 evidence rather than as a request.
