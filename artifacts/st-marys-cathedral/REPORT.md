# Cathedral of Saint Mary of the Assumption asset report

## Result

**PASS** — `st-marys-cathedral.glb` meets the repository's landmark contract
and was validated after fresh-scene re-import in Blender 5.2.0 LTS. Per the
owner's instruction this run delivers files **locally only**: nothing is
committed, no branch was created, and the production manifest,
`pipeline/lib/landmarks.mjs` and all app code are untouched. Integration
remains a separate job (`docs/asset-plans/INTEGRATION-PROMPT.md` plus the
notes in `docs/asset-plans/st-marys-cathedral.md` §2.13 — this is a NEW
landmark that needs a `pipeline/lib/landmarks.mjs` entry and a re-bake).

The exact exported GLB was re-imported before every review render.
`validation.json` is the machine-readable authority for the metrics below.

## Three corrections to the plan (verified, see REFERENCE.md)

1. **The anchor moves ~30 m.** The plan's `-122.4252894, 37.7839772` is the
   OSM *site* relation's centroid, which includes the plaza and parking. The
   cupola's own centroid, from the OSM `building:part` that traces it
   (way 436473547), is **-122.4253877, 37.7842352**.
2. **`targetHeightM` is 78.7, not 58.** 190 ft / 57.9 m is the crown height
   *above the nave floor*; the sources also record a 55 ft (16.8 m) golden
   cross above the crown, and the nave floor sits on a raised plaza. Measured
   from the podium base the asset tops out at 78.7 m, and the manifest figure
   must be the full modelled height or the loader will shrink the whole model
   by 26 %.
3. **There is no entrance canopy.** The plan's massing recipe specifies a
   20 × 6 m canopy on four piers; every photograph shows the projecting base
   fascia and recessed bronze doors doing that job instead. The canopy and
   the plan's corner buttresses were both built and then removed as
   unsupported by the references.

## Deliverables

- `REFERENCE.md` — research dossier, sources, and design decisions
- `build_st_marys_cathedral.py` — deterministic model build/export script
- `render_st_marys_cathedral.py` — fresh-GLB controlled render script
- `validate_st_marys_cathedral.py` — isolated re-import validator
- `make_contact_sheet.py` — contact-sheet composer
- `st-marys-cathedral.blend` — reproducible authoring scene (asset only)
- `st-marys-cathedral.glb` — final binary deliverable, 251 KB
- `validation.json` — full object-level machine report
- `st-marys-cathedral-{north,east,south,west,top,aerial}.png`
- `st-marys-cathedral-contact-sheet.png`
- `st-marys-cathedral-{south,aerial}-night.png` — dusk-pass preview

Rebuild from this directory with:

```bash
blender -b --python build_st_marys_cathedral.py
```

```bash
blender -b --python validate_st_marys_cathedral.py
```

```bash
blender -b --python render_st_marys_cathedral.py
```

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, no external dependencies | PASS | 251 KB self-contained `st-marys-cathedral.glb` |
| Plausible real-world meters | PASS | 94.8154 × 94.8154 × 78.7 m; plan bounds are the 84 m podium turned 9.1° onto the city grid |
| Origin / base | PASS | bounding-box min Z 0.0 m; XY centre offset [0.0, 0.0] m |
| Orientation | PASS | authored +Y = true north; whole model yawed 9.1° CCW to the measured OSM heading; the entrance is on the −Y-most face (see below) |
| Triangle budget | PASS | 7,074 / 18,000 triangles |
| Applied transforms | PASS | all 40 imported mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | 0 invalid/non-unit loop normals; 0 flipped visible first-hits across 22,500 deterministic rays (20,615 hits) |
| Unexpected / leaked geometry | PASS | 40 mesh objects only; no studio floor, context, camera or light in the GLB |
| Image textures / PBR maps | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | every material alpha 1.0, opaque |
| Flat material contract | PASS | eight `Toy_*` materials, roughness 0.85, no `Toy_body` |
| Glow naming | PASS | `Toy_white_Glow` only on the four slot ribbons, `Toy_gold_Glow` only on the entrance lamp band |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | the validator factory-resets then imports the final GLB; the render script repeats that isolation independently |

## Geometry and materials

- Object count: **40 mesh objects**
- Triangle count: **7,074**
- Dimensions: **[94.8154, 94.8154, 78.7] m**
- Bounding box min **[-47.4077, -47.4077, 0.0]**, max **[47.4077, 47.4077, 78.7]**
- Minimum Z: **0.0 m**; XY centre offset **[0.0, 0.0] m**
- Materials: `Toy_glass`, `Toy_gold`, `Toy_gold_Glow`, `Toy_ink`, `Toy_stone`,
  `Toy_trim`, `Toy_white`, `Toy_white_Glow`

The 94.8 m plan bounds are the 84 m styled plaza rotated 9.1° onto the city
grid; the cathedral itself is the 77.7 m ground-floor square with a 60 m
shell springing off it.

## Orientation decision

Authored with Blender `+Y` = true north and `+X` = east, and the entire model
yawed **+9.1° CCW**, which is the heading measured from the OSM footprint
(building edges bear 81.0° / 170.9° / 261.0° / 350.9°). `placeGeneric` in
`app/src/assets.js` applies no rotation, so the asset lands on the city at its
real heading.

The contract's "front faces −Y" rule is nearly moot here: the cupola is
four-way symmetric, and the only asymmetric cues are the Geary entrance —
doors, lamp band and monumental stair. Those sit on the face whose outward
normal bears 171° true, i.e. the −Y-most face, so true-world orientation and
the −Y rule agree to within the 9.1° grid yaw. Authoring the real heading was
chosen over snapping the entrance to exactly −Y because the whole point of the
yaw is that the building sits on its real block.

## Visual design

The conversion followed `docs/styles/miniature-toy.md` §22. The recognition
cues preserved are the hyperbolic-paraboloid silhouette, the stark white
monochrome, the dark glass cross, the golden cross, and the tall shell over a
low wide base.

The shell is built as a **genuine ruled surface**: every vertical line of the
mesh is a straight ruling from a point on the square spring plan to the
arc-length-matched point on the Greek-cross crown plan. That one construction
produces all eight hyperbolic-paraboloid segments — vertical at the face
centres, scooping inward and down at the corners — and it is the difference
between reading as St Mary's and reading as a tapered box. An earlier pass
that eased the corners on a power curve instead produced exactly that box and
was discarded. The shell and its crown are the only smooth-shaded surfaces in
the asset; the style bible explicitly prefers smooth curves where they create
a landmark silhouette (§4), and every chunky solid stays flat-shaded.

Simplified away: the precast panel grid, travertine coursing, door reliefs,
and the entire interior. Designed deliberately for the app's downward camera:
the crown tent with its four ridges and apex skylight, the recessed base roof
deck inside a low parapet, and a flush paving inlay on the plaza.

The four elevations share one camera rig — same 106 m orthographic scale,
1200 × 1000 resolution, camera height, warm tabletop lighting, exposure and
projection — and differ only in azimuth. The aerial uses a 36° downward,
110 mm restrained-perspective camera per §18.

## Night state

The day/night switch is entirely app-side. `app/src/env.js` computes the real
San Francisco sun elevation and drives `uNight`; the landmark loader merges
every `*_Glow` material into one unlit overlay whose opacity is
`0.12 + uNight × 0.95` (`updateLandmarkGlow`, `app/src/kit.js`). The GLB
encodes *what* lights up and the city decides *when*.

Because that overlay is ~12 % opaque in daylight, glow materials are never
used for structure here. The asset uses the light-strip pattern: five glow
bodies in total — four `Toy_white_Glow` ribbons running up each face's glass
slot and over its crown ridge to the apex, and one `Toy_gold_Glow` lamp band
above the Geary doors. Each ribbon is a closed thin tube 1.1 m wide inside a
2.6 m dark glass slot, so the dark glass frames the light by day and the
cross of light reads at night.
`st-marys-cathedral-aerial-night.png` and `st-marys-cathedral-south-night.png`
preview the effect by rendering the re-imported GLB with those materials
emissive under a dusk sky — the same surfaces the app ignites.

## Draft manifest entry (not applied)

```json
{
  "id": "st-marys-cathedral",
  "file": "st-marys-cathedral.glb",
  "anchor": [
    -122.4253877,
    37.7842352
  ],
  "targetHeightM": 78.7,
  "cat": 8,
  "name": "Cathedral of Saint Mary of the Assumption",
  "estimated": false,
  "dims": [
    94.8154,
    94.8154,
    78.7
  ],
  "tris": 7074
}
```

The anchor is the centroid of the OSM `building:part` that traces the cupola
(way 436473547), cross-checked against the site relation and 1111 Gough
Street. `targetHeightM` 78.7 is the modelled height from the podium base to
the tip of the golden cross: 4.0 m podium + 57.9 m (190 ft) crown above the
nave floor + 16.8 m (55 ft) cross. Because that equals the model's own
measured height, the loader's scale factor is 1.0.

`"estimated": false` is defensible for the anchor and the 190 ft crown, both
of which are sourced. Note for whoever integrates this: the podium height is
a styling decision, not a survey, so if the app's terrain already raises the
site, the podium may need trimming rather than the height re-tagged.

## Scope confirmation

No parish centre, school, parking structure beyond the podium, Geary
Boulevard, trees, people, vehicles, plinth, studio background, camera or
light is present in the GLB. Studio elements exist only inside the render
script and are never exported. No existing GLB was modified or renamed, and
no app code, production manifest or pipeline file was touched.

## Known tension, carried forward

The published figures produce a shell whose visible height/width ratio is
about 0.70, while both straight-on reference photographs read 0.88–1.04. The
asset splits this: the spring square was pulled from the OSM-traced 62.7 m in
to 60 m and the base kept low, giving 0.76. If a primary elevation drawing
ever surfaces, the two numbers to re-check are the shell's springing level and
whether the crown is 190 ft above the floor or above the street.
