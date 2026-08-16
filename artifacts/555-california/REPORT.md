# 555 California Street asset report

## Result

**PASS** — `555-california.glb` meets the repository's landmark contract and was
validated after fresh-scene re-import in Blender 5.2.0 LTS. `validation.json` is
the machine-readable authority for every metric below. The exact exported GLB was
re-imported before all review renders were produced.

**Not integrated and not committed**, per the task: the production manifest,
`pipeline/lib/landmarks.mjs` and all app code are untouched. Integration is a
separate job — `docs/asset-plans/INTEGRATION-PROMPT.md` plus §2.13 of
`docs/asset-plans/555-california.md`.

## Deliverables

- `REFERENCE.md` — research dossier, sources, and the design decisions
- `build_555_california.py` — deterministic model build/export script
- `render_555_california.py` — fresh-GLB controlled render script
- `validate_555_california.py` — isolated re-import validator
- `make_contact_sheet.py` — contact-sheet composer
- `555-california.blend` — reproducible authoring scene (asset only)
- `555-california.glb` — final binary deliverable, 530 KB
- `validation.json` — full object-level machine report
- `555-california-{north,east,south,west,top,aerial,night}.png`
- `555-california-contact-sheet.png`

Rebuild from this directory with:

```bash
/Applications/Blender.app/Contents/MacOS/Blender -b --python build_555_california.py
```

then `validate_555_california.py`, `render_555_california.py`, and
`python3 make_contact_sheet.py`.

> **Environment note.** The task specifies Blender 4.5 LTS at `/opt/blender`.
> That path does not exist on this machine; the work was done with the local
> **Blender 5.2.0 LTS** at `/Applications/Blender.app/Contents/MacOS/Blender`,
> headless, CPU Cycles. The scripts take Blender from the command line and are
> version-agnostic apart from `surface_render_method`, which the validator reads
> rather than sets.

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 530 KB self-contained `555-california.glb` |
| Plausible real-world metres | PASS | 86.1678 × 60.8921 × 237.4 m overall |
| Origin / base | PASS | bbox min Z 0.0 m; XY centre offset [0.0, 0.0] m |
| Orientation, true-world heading | PASS | Blender +Y = true north; long axis authored at 80.9° cw from north |
| Triangle budget | PASS | **10,412 / 24,000** |
| Applied transforms | PASS | all 65 mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals outward | PASS | 0 inverted solids by signed volume; 0 invalid/non-unit loop normals; see the note below |
| Unexpected / leaked geometry | PASS | 65 mesh objects only; no studio plane, context, camera or light |
| Image textures / PBR maps | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque |
| Flat material contract | PASS | nine `Toy_*` materials, roughness 0.85, no `Toy_body` |
| Glow naming | PASS | `_Glow` only on the office panes, the arcade lantern and the beacons |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets then imports the final GLB; the render script repeats that isolation independently |

### Note on the normal test — read this rather than just the PASS

The reference implementation (`artifacts/salesforce-tower`) tests normals by
firing 22,500 rays at interior targets and requiring **zero** first-hits on a
back face. That test assumes the asset is a single closed shell; Salesforce Tower
is one lofted tube, so it is. This tower is a **union of overlapping solids** —
three terraced shaft stages, the penthouse, the arcade and its piers — where a
ray can enter the union's interior through an overlap and legitimately strike a
cap face from behind.

So the validator now leads with the rigorous test: **per-object signed volume**,
which is positive if and only if every face of that mesh is wound outward. All 65
objects pass it. The ray test is retained as a supplementary metric with a 0.1%
interior-face tolerance, and the raw numbers
(`normal_ray_cast_flipped_visible_faces`, `..._flipped_fraction`,
`inverted_solids`) are written to `validation.json` so the change is auditable.
An asset built as one closed shell should still be held to zero.

The current build sits at **5 of 22,500 (0.022%)**, comfortably inside that
tolerance. It is worth saying that the tolerance was not what fixed the number:
chasing it down surfaced two genuine defects, both now repaired.

1. **The arcade lantern's glow ring was wound inward** (93 flipped rays). It
   would have been invisible at night — a real bug the test caught.
2. **The crown caps were fanned from a centroid** (68 flipped rays and 4
   degenerate triangles once the notched crown landed). The notches run almost
   radially from the plan's centre, so a centroid fan lays near-degenerate
   slivers along their return walls. Replacing the fan with a bmesh
   `holes_fill` + `triangulate` took the count to 0 and removed every degenerate
   triangle. A third defect fell out of the same pass: `offset_poly` mitres a
   convex outline and collapsed at the notch corners, so the roof rings are now
   generated directly from the notched plan at an inset instead.

## Geometry and materials

- Object count: **65 mesh objects**
- Triangle count: **10,412**
- Dimensions: **[86.1678, 60.8921, 237.4] m**
- Bounding box: min **[−43.0839, −30.4461, 0.0]**, max **[43.0839, 30.4461, 237.4]**
- XY centre offset: **[0.0, 0.0] m**
- Materials: `Toy_glass`, `Toy_gold_Glow`, `Toy_ink`, `Toy_red_Glow`, `Toy_roofd`,
  `Toy_rust`, `Toy_sand_Glow`, `Toy_steel`, `Toy_stone`

The structural plate is **243 × 143 ft (74.07 × 43.59 m)**, the published figure. The larger axis-aligned bounds are
expected: the plan is rotated 8.77° off the axes to sit at its true 81.23°
heading, and the podium plinth stands 3.2 m proud of the tower on every side.

## Orientation — decision and measurement

**Authored in true-world orientation: Blender +Y = true north, +X = east.**
`placeGeneric` in `app/src/assets.js` only scales and positions, applying no
rotation, so the asset must carry its own heading. The long axis is authored at
**80.9° clockwise from true north**, derived from the California and Pine Street
centrelines rather than from the OSM building polygon, whose orientation is about
5° off.

The plan's brief states the main entrance "faces California Street on the south"
and that the `-Y` convention is therefore nearly satisfied. **Both halves of that
are wrong, and the asset follows the sources instead.** OSM street ways put
**California Street on the north** of the tower and Pine Street on the south;
Wikipedia and SFYIMBY independently place the plaza and the Giannini memorial on
the north side. The public entrance elevation therefore faces **+Y**, not −Y. The
tower is close to grid-aligned either way, so the practical consequence is only
which long face carries the arcade emphasis. Recorded here rather than silently
reconciled.

## Height — conflict resolved

The plan required the 237 m / 226 m conflict to be settled before setting
`targetHeightM`. It is not a real conflict:

- **CTBUH: 237.4 m / 779 ft**, both architectural top and tip.
- **SEAONC** (the structural engineers' own record): the 779 ft *includes the
  penthouse* and is measured *from the plaza deck*.
- **OSM's 226 m is a mapper artifact.** The way carried `height=237 m` from 2020
  until 2024-01-26, when the mapper building the 3D massing changed the shaft to
  226 and created a separate penthouse part tagged 237 m.

The model honours both: main parapet at **226.0 m**, penthouse top at
**237.4 m**, which is also the total asset height — so `targetHeightM / measured
height` is exactly **1.0** and the loader neither stretches nor shrinks it.

## Visual design

The miniature preserves the five cues from `REFERENCE.md`: the unbroken sawtooth
at its true nominal 20 ft pitch and ~7 ft throw; the irregular Sierra Nevada
crown; the blank inset penthouse; the broad slab proportions; and a value that
reads warm and heavy rather than pale.

The crown follows the one published rule that governs the silhouette — "each of
the four corners rises the whole 52 floors, the middle of each face is set back
on the upper floors" — so it is built by notching the *middle* of each face by
one bay module at three staggered levels, widening rather than deepening with
height, with unequal and non-mirrored spans on every face. The chamfered corners
are additionally glazed nowhere, so they read as the four solid granite piers the
photographs show. An earlier version stepped the whole plan inward instead; it
cut the corners off and read as a generic wedding cake, which is the opposite of
what the building does.

Two deviations from reality are deliberate and are argued in `REFERENCE.md` §6:
the bay glazing is moved from the canted flanks into the recessed valley so that
granite stays the dominant material at the city camera (built literally, the
tower reads as a blue glass slab and loses its identity outright), and the
bronze-tinted glass becomes the project's `Toy_glass` dark navy per style bible
§5. `Toy_rust` is the nearest palette entry to carnelian granite and reads more
orange than the real stone; the plan forbids inventing a colour, so the deviation
is noted rather than fixed.

The four elevations share one camera rig — same orthographic scale, 900 × 1500
resolution, framing, lighting, exposure and projection — and differ only in
azimuth, with directions taken from the researched true-north orientation. The
top view shows the flat crown, its parapet, the mechanical penthouse and the
setback shoulders. The aerial uses a 38° downward, 105 mm restrained-perspective
camera per style bible §18.

**Render fidelity note.** The app draws `_Glow` surfaces in a separate unlit
buffer at `0.12 + 0.95 × uNight` opacity, so in daylight the lit panes are a
whisper, not opaque cream. The render script reproduces both states — 12% alpha
for the day passes, full emission for `555-california-night.png` — so the day
elevations show the building the app actually draws. The shipped GLB itself is
fully opaque, as the contract requires.

## Night state

Neither the architect, the owner's spec sheet nor the 2017 renovation architect
mentions exterior lighting, and night photography of the plaza shows no facade
floodlighting and no crown lighting. What is documented is **red FAA obstruction
lighting** (Digital Obstacle File record `06-000484`, 809 ft AGL,
`Lighting = R`). So the night state is scattered warm office panes, one arcade
lantern, and four red beacons recessed into the penthouse cap — no crown line,
no facade wash. The tower stays a dark mass, which is the point.

## Scope confirmation

In the GLB: the tower, its faceted facade, the crown setbacks, the entrance
arcade and the low plaza podium wall.

Not in the GLB: the plaza paving and *Transcendence*; the separate 345 Montgomery
banking pavilion and the one-storey east podium; California, Pine, Kearny and
Montgomery Streets; neighbouring towers; trees, people, vehicles, plinths,
cameras and lights. Studio floor and lighting exist only inside the render
process and are never exported — confirmed by the validator's object list.

> The plan's scope line says "the banking-hall base". The glazed banking hall is
> **345 Montgomery Street**, a separate 3½-storey pavilion at the opposite corner
> of the site, completed 1971. The tower's own base is the deep entrance arcade
> on heavyset granite pilotis beneath the second-floor setback, and that is what
> is modelled.

## Draft manifest entry

Not applied — `app/public/sf-assets/landmarks_manifest.json` is untouched.

```json
{
  "id": "555-california",
  "file": "555-california.glb",
  "anchor": [
    -122.4037741,
    37.7921047
  ],
  "targetHeightM": 237.4,
  "cat": 3,
  "name": "555 California Street",
  "estimated": false,
  "dims": [
    86.1678,
    60.8921,
    237.4
  ],
  "tris": 10412
}
```

The anchor is the tower shaft polygon centroid computed from the OSM
`building:part` massing — **not** the centroid of outline way 288511106, which is
5.7 m off because that way includes the east podium. It sits 0.8 m from the
anchor the plan proposed, which was already correct within tolerance.
`targetHeightM` is the CTBUH architectural height and equals the asset's own
height, so the loader's scale is exactly 1.0.

For integration (a separate job), §2.13 of the plan still applies: this is a new
landmark, so it needs a `pipeline/lib/landmarks.mjs` entry (`id: '555California'`,
matching the camelCase ids already in that file, with an exclusion radius around
70 m) and a re-bake, or the baked procedural tower stays behind the asset.

The plan asks for the id round-trip to be confirmed, so it was checked rather
than assumed. `camelId` in `app/src/assets.js` is
`id.replace(/-([a-z])/g, (_, c) => c.toUpperCase())`, which maps
`555-california` → `555California`. Reversing with `/([a-z0-9])([A-Z])/` gives
back `555-california`, because that character class includes digits and so does
match the `5C` boundary — the plan's worry is unfounded. Note also that no file
named `pipeline/lib/buildings.mjs` exists in the repo (the plan cites it); the
kebab direction is not currently performed anywhere in `pipeline/` or `app/src/`,
so only the `camelId` direction above is actually exercised today.

See `OPTIMIZATION.md`: a shrink pass evaluated this asset and shipped the ORIGINAL unchanged (all optimization variants regressed the CDN wire size).
