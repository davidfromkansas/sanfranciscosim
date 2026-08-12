# Bill Graham Civic Auditorium — build report

A stylized miniature of 99 Grove Street for SF-SIM, produced by running
`docs/asset-pipeline/ADDRESS-TO-ASSET.md` end to end on
`BUILDING: Bill Graham Civic Auditorium, 99 Grove St`.

Where this report and `docs/asset-plans/bill-graham-civic-auditorium.md` disagree,
**this report is correct** — it records what was actually built and measured.

## Files

| File | What it is |
|---|---|
| `build_bill_graham_civic_auditorium.py` | Deterministic Blender build; `blender -b --python …` rebuilds the GLB byte-for-byte |
| `render_bill_graham_civic_auditorium.py` | Controlled review renders, always from the **exported** GLB |
| `validate_bill_graham_civic_auditorium.py` | Fresh-scene contract validation of the exported GLB |
| `make_contact_sheet.py` | Composes the eight review images |
| `bill-graham-civic-auditorium.glb` | The shipping asset |
| `bill-graham-civic-auditorium.blend` | Source scene |
| `validation.json` | Machine-readable contract report |
| `*-north/east/south/west/top/aerial/night/night-front.png`, `*-contact-sheet.png` | Review renders |

## Validated result (fresh-scene re-import of the GLB)

| | |
|---|---|
| Overall | **PASS** (all 15 checks) |
| Objects / triangles | 209 / **6,408** (cap 26,000; repo hard gate 30,000) |
| Dimensions (world-aligned bbox) | 140.836 x 100.144 x **37.000** m |
| Footprint it represents | 127.95 x 78.64 m at 80.69° — the world-aligned bbox is larger because the building is rotated 9.31° off the world axes |
| min Z / XY centre | 0.0 m / (0.0, 0.0) |
| Materials | `Toy_stone`, `Toy_trim`, `Toy_sand`, `Toy_white`, `Toy_glass`, `Toy_ink`, `Toy_roofd`, `Toy_steel`, `Toy_white_Glow`, `Toy_mustard_Glow` |
| Textures / transparency | 0 / 0 |
| Cameras / lights / animation / armatures / constraints | 0 / 0 / 0 / 0 / 0 |
| Transforms applied / negative scales | yes / none |
| Normals | PASS — per-object signed volume positive on every object; 22,500-ray visibility test within tolerance |
| Glow emission strength on ship | 0.0 (night-only, as the contract requires) |

## Orientation & placement

- Authored **world-true**: Blender `+Y` = true north, `+X` = east. The long axis bears
  **80.69° cw from true north** and the arcade front faces **north** onto Grove Street
  and Civic Center Plaza.
- **Deviation from the contract, recorded deliberately:** the asset contract asks for
  the front to face `−Y`. This building's front faces north, so honouring that rule
  literally would place it backwards in the city. Real-world orientation wins
  (AGENTS rule 5, and the standing note in `docs/asset-plans/README.md`). No `yawDeg`
  override is used or needed.
- **Anchor after recentring: `-122.4173309, 37.7780621`.** This differs from the
  measured OBB centre (−122.4173272, 37.7780592) by ~0.4 m because the exported model's
  bounding box includes the marquee canopy projecting north and the cornice returns; the
  manifest anchor must be the model's own origin, which is what the build script prints.
- Target height **37.0 m**, so `targetHeightM / measuredHeight = 37.0 / 37.0 = 1.000`.
  The dome apex is normalised to the verified height exactly, so the loader applies a
  scale of 1.0.

## Design decisions (vs the plan doc)

1. **The dome is the asset.** It is measured — a regular octagon 58.6 m flat-to-flat,
   centred 7 m south of the building centre — and it is the only thing about this
   building that the app's camera can see and the street cannot. Everything else is
   built to keep out of its way: a light deck around it so the dark octagon has maximum
   contrast, roof plant pushed to the deck outside the octagon's corners, no clutter.
2. **Dome profile changed from three segments to four.** The plan's three-frustum stack
   read as a circus tent from the aerial. A four-segment saucer
   (31.71 → 27.5 → 20.0 → 11.0 → 4.6 m) matches the satellite's shading better and costs
   ~80 extra triangles.
3. **End pavilions shortened from 34 m deep to 24 m.** At 34 m they read as two blank
   white slabs sitting on the roof and competed with the dome. Their roofs are now
   designed (deck plus two plant boxes each) rather than blank — §10.
4. **The ground storey is one continuous dark recess**, not nine separate openings.
   The real thing reads as a single shadowed slot under the marquee; nine boxes fought
   the rusticated base and produced visual noise.
5. **Link bays added** between the arcade and each pavilion: two pilasters, two punched
   windows and a wreath medallion each. Without them 14 m of frontage on each side was
   dead wall.
6. **Three arches, not more.** Counted on a near-frontal photograph and confirmed on a
   night close-up. It is a low count for a 128 m frontage and it looks sparse beside the
   Opera House's seven bays — it is correct, and the sparseness is what makes the arches
   monumental. Recorded here because it is the single most likely thing to be
   "corrected" by a later reviewer.
7. **Flagpoles omitted.** They are a real identity cue but rise to ~39 m, above the
   dome, so keeping them would have made the model's crest something other than the
   measured 37.0 m and broken the loader's 1.0 scale. At ~0.1 m thick they are also
   sub-pixel at the app's camera. If a future revision wants them, the target height
   must be re-decided first.
8. **Palette.** `Toy_trim` granite front against `Toy_sand` flanks is the model's
   reading of "grey granite main facade, brick sides and rear": a value step, not a
   colour step, so the building stays in the Civic Center family instead of turning red.
   Sources say brick; photographs read grey-beige, and the photographs win.

## Corrections to the dossier made during the build

- **The 37 m height is the dome apex, not the parapet.** Two independent sources (OSM
  survey 2025-11 and 2010 city LiDAR `hgt_max`) agree to 2 cm, and the LiDAR median
  22.99 m gives the main roof deck separately. Treating 37 m as the parapet would have
  made the building half again too tall at street level.
- **The dome's offset is real.** It is centred ~7–8 m *south* of the footprint centre,
  not on it, because the 20 m front range takes the north edge. Building it concentric
  put the octagon through the arcade parapet.

## Glow set (night)

| Material | Where | Role |
|---|---|---|
| `Toy_mustard_Glow` | panes behind the three giant arches | **Hero** — the real building floodlights exactly these three windows, routinely in colour |
| `Toy_white_Glow` | one band along the marquee soffit | The marquee's bulb band |

Nothing else glows. The dome stays dark at night, as it does in life. Every glow
surface's day colour matches a non-glow palette neighbour, and all ship with emission
strength 0 — the app's dusk pass drives them.

## Approval (Gate 3)

Approved by David on 12 August 2026, verbatim:

> "Do it on a new branch and PR -- i approve all stages just proceed"

## Manifest entry (as integrated)

```json
{
  "id": "bill-graham-civic-auditorium",
  "file": "bill-graham-civic-auditorium.glb",
  "anchor": [-122.4173309, 37.7780621],
  "targetHeightM": 37,
  "cat": 17,
  "name": "Bill Graham Civic Auditorium",
  "estimated": false,
  "dims": [140.836, 100.144, 37.0],
  "tris": 6408,
  "loadRadius": 2500
}
```

**Streaming decision:** `loadRadius: 2500`. The default rule gives
`max(2500, 37 × 30) = 2500`. The building is broad rather than tall, so it is illegible
long before 2.5 km; and because this is Case B the baked block underneath is carved out,
so beyond the radius the site is empty ground. A longer radius would only cost boot
bandwidth for a shape nobody can resolve.

## Integration (Case B)

`camelId('bill-graham-civic-auditorium')` → `billGrahamCivicAuditorium`, which did not
exist in `pipeline/lib/landmarks.mjs` or `app/src/landmarks.js`. Integration therefore
added the registry entry and re-baked the affected tiles. The exclusion radius is the
largest of any Civic Center asset (the footprint is 128 x 79 m), so it was checked
against City Hall's and the Opera House's zones. See the integration section of the PR.
