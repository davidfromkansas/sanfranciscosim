# 110 The Embarcadero — build report

**REPORT beats plan.** Where this file disagrees with
`docs/asset-plans/110-embarcadero.md`, this file is what was built and why.

| | |
|---|---|
| Asset | `artifacts/110-embarcadero/110-embarcadero.glb` |
| Manifest id | `110-embarcadero` |
| Registry id (Case B) | `110Embarcadero` |
| Anchor (WGS84) | **−122.3926614, 37.7932332** |
| Target height | **17.40 m** (bbox top = the Embarcadero roof fascia) |
| Objects / triangles | **13** / **4,944** (cap 13,000) — 137 objects before the stage-4 join |
| Dimensions (m) | 40.476 × 40.192 × 17.400 |
| min Z / XY centre offset | 0.000 / (0.000, 0.000) |
| Materials | 10 (`Toy_stone`, `Toy_trim`, `Toy_glass`, `Toy_glassl`, `Toy_ink`, `Toy_mint`, `Toy_sand`, `Toy_glassl_Glow`, `Toy_trim_Glow`, `Toy_mustard_Glow`) |
| File size (shipped, meshopt-packed) | **144,144 B / 140.8 KB** raw, from 320,764 B pre-optimize (−55.1%) |
| Draw submeshes | 16 (140 pre-optimize) |
| Blender | 5.2.0 LTS, headless, Cycles CPU |

**Why the XY box is 40 m for a 13.9 m-wide building.** The footprint is a
41.87 × 13.91 m parallelogram lying at 135.24° to the world axes, and the model
is authored in real-world orientation (`+Y` = north), so its axis-aligned bounding
box is the 45°-rotated envelope of a long thin building. That is expected, not a
scale error. The loader scales by `targetHeightM / measuredHeight`, which uses Z
only, and Z is exactly 17.400.

**Anchor.** The design anchor is the footprint centroid, −122.3926624,
37.7932325. Recentring the model on its XY bbox centre (contract rule 2) moved it
0.089 m east and 0.080 m north — the projecting roof fascia at the Embarcadero end
and the cornice at the Steuart end are not symmetric — so the manifest anchor is
the shifted value above. The building still lands on its real footprint.

**Orientation.** Authored `+Y` = true north. The Embarcadero front's outward
normal is 44.83°, the Steuart front's 224.94°, the party walls 135.24° and
315.24°. The contract's "front faces −Y" cannot be honoured: this building has two
fronts and neither faces −Y. Real-world orientation wins (AGENTS rule 5, and the
asset-plans README orientation note). The loader applies no rotation.

---

## Corrections to the dossier and the plan, made during the build

Each of these changed the model. They are also recorded in REFERENCE.md §8.

### 1. The roof deck datum was wrong in the plan (16.60 → 15.80 m)

The plan put the main roof deck at 16.60 m with the parapet at 16.90 m. That is a
0.30 m upstand around a *publicly accessible* roof terrace, which is not a guard,
and it left 0.80 m of headroom under the 17.40 m crest for planting, planters and
roof lights — not enough for any of them. 16.90 m is the height the rectified
elevation measures for the curtain-wall **head / parapet top**; the walking
surface has to sit a guard height below it. The model uses **deck 15.80, parapet
16.90, fascia 17.40**, which also makes the third floor 11.20 → 15.80 = 4.6 m
floor-to-roof, a credible storey.

### 2. There is no mid-roof penthouse

The plan's massing recipe (§2.7 item 10) put a penthouse volume in the middle of
the roof. The building's only stair / lift over-run is the solid pale box at the
**Steuart** end that the Street View elevation actually shows, at ~14.8 m, and
that box was already in the model. The mid-roof volume was both a duplicate and,
at 2.5 m above the deck, would have pushed the bounding box past the fascia. It
was removed; a low plant enclosure stands in its place.

### 3. A pergola on the roof deck broke the bounding box, and was cut

The first roof pass put a 2.55 m timber pergola over the deck to stop it reading
as a blank slab. It stood 1.75 m proud of the roof fascia and made the exported
bbox top **19.15 m** — which would have driven the loader's scale factor to
17.4/19.15 = 0.91 and shrunk the whole building by 9 %. It is also unverified: no
source and no aerial frame shows one. It was replaced with a **1.05 m trellis
screen** down each side of the deck, and a hard rule was written into the build
script: nothing on this deck above 17.35 m.

### 4. The night glow colours were both wrong on the first pass

Two separate mistakes, both caught by rendering rather than by reading the code:

- **The lit curtain wall must not be `Toy_glass_Glow`.** The app draws `_Glow` in
  a separate unlit layer, so at night a glow surface shows its **raw base
  colour** — and `Toy_glass` (2a4d73) is the navy of *unlit* glass. It is now
  `Toy_glassl_Glow` (6f95b8), a slate blue that reads as lit.
- **The ground-level cues must not be near-white.** The first pass lit the whole
  13.9 m lobby band and the Steuart storefront in `Toy_trim_Glow` (f3efe6) and
  they blew out to a white slab brighter than the hero above them. The signage
  band keeps f3efe6 — it is a sign — and the lobby and storefront moved to
  `Toy_mustard_Glow` (d9a441): warm amber at ground level under a cool lantern,
  and clearly subordinate.

The render rig's night emission was also dropped from the inherited 3.2 to
**2.4**, because at 3.2 the 6f95b8 curtain wall came back as pale cyan-white —
the render flattering a colour instead of testing it.

### 5. Window frames were built in front of their own glass

The first pass drew each Steuart opening as a glass panel with a larger solid
`Toy_trim` prism over it as a "frame". The frame covered the glass completely and
every window on the historic front rendered as a blank cream panel. Openings now
go through one helper: a **recessed frame plate** with the glass standing
**proud** of it. The ground-floor door had the same bug and the same fix.

### 6. The pediment was capped in `Toy_ink` and rendered as a black arrowhead

Sitting in front of the navy set-back glazing behind it, the dark cap read as a
black triangle rather than a crown. The pediment is now a `Toy_trim` raking
cornice with a recessed `Toy_stone` tympanum — moulding against field, which is
what actually reads at city distance.

### 7. Two 15 m blank rectangles are not a roof

The first roof was a sand deck and a green band. From the app's downward camera it
read as a lid. The roof is now composed along the long axis: paved deck with joint
bands and three roof lights at the Embarcadero end, a planter row and trellis
screens down both deck edges, three planted beds with clipped shrub masses split
by cross paths through the middle, the plant enclosure, and the quiet strip behind
the historic parapet at the Steuart end.

### 8. The Steuart doorway was on the wrong end of the building

The first pass put the recessed ground-floor doorway at the north-west end of the
Steuart front, against the Audiffred, and ran the three storefront bays back from
it. The Street View frame — read against the seven-storey brick neighbour, which
stands on the **south-east** side — has the door at the south-east end. `STE`'s
`t = 0` is the south-east corner, so the door is now at t 0.55–2.27 and the bays
run north-west from it.

### 9. Three defects the validator's glow ray test found, not the eye

`glow_strips_face_outward` casts a ray back along each night surface's own normal
and requires that surface to be the first thing hit. It failed three times:

- **Object naming.** The check finds night surfaces by the `_glow` **suffix**;
  these were named `glow_*`, so it tested zero faces and failed on the count.
  Renamed to `cw_glow`, `sign_glow`, `lobby_glow`, `shop<i>_glow`,
  `setback_glow`, `skylight<i>_glow`.
- **The set-back glow was buried inside the building.** It was placed on the
  north-west party wall using `t` as if that face ran from the Embarcadero end;
  `NW_PARTY`'s `t` starts at the Steuart corner, so the quad landed 35 m away
  inside solid geometry. It is now on the set-back volume's own south-west face,
  which is the one that shows above the historic Steuart parapet — and a party
  wall against the Audiffred could never have shown it anyway.
- **The signage band was half-buried.** The recessed lobby zone stopped at
  4.00 m while the COMMONWEALTH CLUB band runs to 4.50 m, so the top of the band
  and its glow sat inside the flush body above. The recess now runs to 4.95 m and
  the curtain wall starts at 5.00 m.

### 10. Smaller ones

- The `Toy_ink` parapet caps were 0.38 m wide and read from above as two heavy
  black rails the length of the roof. Narrowed to 0.18 m.
- The curtain wall had no horizontal transoms and read as one 12 m sheet of
  glass; two transom lines were added at the heights the rectified elevation
  shows, so it reads as three storeys.
- The day render rig left `_Glow` emission at 1.0 while dropping alpha to 0.12,
  which lit the lobby to near-white in the *day* images. The app draws these
  surfaces unlit by day, so the rig now zeroes emission as well.
- The top-view camera roll was inherited from a different building and put the
  Steuart end at the top of the frame; it now puts the Embarcadero end up.

---

## What is in the asset

The building only: both street fronts, both party walls, parapets, the cornice
and pediment, the set-back third floor and its stair over-run, the roof deck,
roof garden and planters, the trellis screens, the roof lights, the entrance
canopy and the signage band.

Not in the asset: The Embarcadero, Steuart Street, the F-line tracks, the
Audiffred Building, the seven-storey office to the south-east, street trees,
street furniture, people, vehicles, plinths, cameras or lights.

## Vertical ladder as built

| z (m) | What |
|---|---|
| 0.00 | pavement |
| 4.20 | level 2 floor / head of the recessed Embarcadero lobby |
| 4.85 – 5.10 | Steuart sill band |
| 11.20 | level 3 floor; retained historic roof line |
| 11.60 | Steuart cornice crest |
| 12.60 | Steuart pediment apex (exaggerated 0.3 m from the measured 12.3) |
| 13.90 | top of the set-back glazed third floor at the Steuart end |
| 14.80 | stair / lift over-run box |
| 15.80 | main roof deck surface |
| 16.90 | curtain-wall head / main parapet |
| **17.40** | **roof fascia — the bbox top** |

## Draft manifest entry

```json
{
  "id": "110-embarcadero",
  "file": "110-embarcadero.glb",
  "anchor": [
    -122.3926614,
    37.7932332
  ],
  "targetHeightM": 17.4,
  "cat": 17,
  "name": "The Commonwealth Club (110 The Embarcadero)",
  "estimated": false,
  "dims": [40.476, 40.192, 17.4],
  "tris": 4944,
  "loadRadius": 2500
}
```

## Validation

`validation.json`, produced by re-importing the **shipped, meshopt-packed** GLB
into a fresh isolated Blender scene: **overall PASS**, all 17 checks green. It was
re-run after the stage-4 shipping swap, because stored-normal defects surface only
in the packed file.

| | |
|---|---|
| objects / triangles | 13 / 4,944 (cap 13,000) |
| dimensions (m) | 40.4759 × 40.1923 × 17.4000 |
| min Z / XY centre offset | 0.0 / (0.0, 0.0) |
| materials | 10, all `Toy_*`, flat, no textures, no alpha, no `Toy_body` |
| glow surfaces | 20 faces, **20 outward** — all open single-layer quads |
| normals | per-object signed volume all outward; ray residual within tolerance |
| cameras / lights / animations / armatures / constraints | 0 / 0 / 0 / 0 / 0 |

## Approval (stage 3)

Given in the pipeline invocation on 19 August 2026, verbatim:

> **APPROVE EVERYTHING DONT ASK ME FOR PERMISSION**

Taken as a standing approval covering gate 0 and gate 3 for this landmark. It is
not taken as authorisation to push, open a PR, or deploy — the pipeline ends at a
local, verified source-only branch and asks (ADDRESS-TO-ASSET stage 5).
