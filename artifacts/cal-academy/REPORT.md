# California Academy of Sciences asset report

## Result

**PASS** — `cal-academy.glb` meets the repository's landmark contract and was
validated after fresh-scene re-import in Blender 5.2.0 LTS. Per the owner's
instruction this run delivers files locally only: nothing is committed, no
branch was created, and the production manifest, `pipeline/lib/landmarks.mjs`
and all app code are untouched. Integration remains a separate job
(`docs/asset-plans/INTEGRATION-PROMPT.md` + the notes in
`docs/asset-plans/cal-academy.md` §2.13 — note this is a NEW landmark that
needs a `pipeline/lib/landmarks.mjs` entry and a re-bake).

The exact exported GLB was re-imported before all seven review renders were
produced. `validation.json` is the machine-readable authority for the metrics
below.

## Two corrections to the plan (verified, see REFERENCE.md)

1. **`targetHeightM` is 19.3, not 11.** OSM's `height=11` is the flat
   perimeter canopy (Fondazione Renzo Piano: 11.3 m); the living-roof hill
   crests reach the architect's published **19.3 m** maximum, and the model's
   bounding box tops out at exactly 19.3 m. Scaling this model to 11 m would
   shrink the footprint ~43% (the plan's own §2.15 flags exactly this risk).
2. **The entrance front faces north-west, not north-east.** Live OSM geometry
   puts the Music Concourse and de Young at ~318° true from the Academy; the
   161 m front facade's outward normal bears **318.3°**. The task prompt's
   "north-east" is corrected in the dossier.

## Deliverables

- `REFERENCE.md` — research dossier and design decisions
- `build_cal_academy.py` — deterministic model build/export script
- `render_cal_academy.py` — fresh-GLB controlled render script
- `validate_cal_academy.py` — isolated re-import validator
- `make_contact_sheet.py` — contact-sheet composer
- `cal-academy.blend` — reproducible authoring scene (asset only)
- `cal-academy.glb` — final binary deliverable (593 KB, self-contained)
- `validation.json` — full object-level machine report
- `cal-academy-{north,east,south,west,top,aerial,night}.png` — the night render previews the app night pass (emissive `_Glow` surfaces in a dusk world)
- `cal-academy-contact-sheet.png`

Rebuild from this directory with (Blender 4.5+ / 5.x, headless CPU):

```bash
blender -b --python build_cal_academy.py
blender -b --python validate_cal_academy.py
blender -b --python render_cal_academy.py
python3 make_contact_sheet.py
```

(Authored and validated on macOS with Blender 5.2.0 LTS at
`/Applications/Blender.app/Contents/MacOS/Blender`; the scripts use no
version-specific APIs beyond the glTF exporter present in 4.5 LTS.)

## Orientation decision

Authored with Blender `+Y` = true north, `+X` = east. The measured long-axis
bearing of the OSM footprint is **48.3° true** (short axis 138.3°/318.3°), so
the local long axis is yawed **+41.7° CCW from +X**, baked into the vertex
data. The loader (`placeGeneric` in `app/src/assets.js`) applies no rotation,
so the GLB lands on its real heading: the entrance facade faces **318.3°
(NW)** toward the Music Concourse. Because this landmark's identity is its
roof and the real heading governs placement, no separate "front = −Y"
concession is made (same hierarchy as the Salesforce Tower asset, which keeps
its measured SoMa yaw).

## Contract results

| Rule | Result | Evidence |
|---|---|---|
| Binary GLB, external dependencies | PASS | 593 KB self-contained `cal-academy.glb`; 0 images |
| Plausible real-world meters | PASS | 212.5214 × 207.7346 × 19.3 m AABB — the yawed 161.3 × 102.5 m footprint plus the 8.5 m eave, crest at the architect's 19.3 m |
| Origin / base | PASS | bounding box min Z 0.0 m; XY center offset [0.0, 0.0] m |
| Orientation | PASS | +Y = true north; measured 48.3° long-axis heading baked in; NW entrance front documented |
| Triangle budget | PASS | 22,384 / 27,000 triangles |
| Applied transforms | PASS | all 153 mesh objects at location 0, rotation 0, scale 1 |
| Negative scales | PASS | none |
| Normals | PASS | 0 invalid/non-unit loop normals; 22,078 deterministic visibility rays, 0 flipped first-hits |
| Unexpected / leaked geometry | PASS | 153 mesh objects only; no studio plane, context, camera or light in GLB |
| Image textures / PBR maps | PASS | 0 images, 0 texture nodes |
| Transparency | PASS | all material alpha 1.0, opaque |
| Flat material contract | PASS | eleven `Toy_*` materials, roughness 0.85, palette hexes; no `Toy_body` |
| Glow naming | PASS | `_Glow` only on surfaces lit at night: piazza dish + porthole rims (`Toy_white_Glow`), clerestory ribbon (`Toy_gold_Glow`), entrance doors (`Toy_trim_Glow`) |
| Cameras / lights | PASS | 0 / 0 |
| Animations / armatures / constraints | PASS | 0 / 0 / 0 |
| Degenerate geometry | PASS | 0 degenerate triangles |
| Fresh isolated re-import | PASS | validator factory-resets then imports the final GLB; render script independently repeats that isolation |

## Geometry and materials

- Object count: **153 mesh objects**
- Triangle count: **22,384**
- Dimensions: **[212.5214, 207.7346, 19.3] m** (axis-aligned bounds of the yawed building)
- Bounding box min: **[-106.2607, -103.8673, 0.0] m**
- Bounding box max: **[106.2607, 103.8673, 19.3] m**
- Minimum Z: **0.0 m**
- XY center offset: **[0.0, 0.0] m**
- Materials: `Toy_glass`, `Toy_glassl`, `Toy_gold_Glow`, `Toy_ink`, `Toy_mint`,
  `Toy_stone`, `Toy_trim`, `Toy_trim_Glow`, `Toy_verdigris`, `Toy_white`,
  `Toy_white_Glow`

## Visual design

The miniature preserves the five cues ranked in `REFERENCE.md`: the
undulating living green roof with seven hills (two dominant 27 m-class domes
for the planetarium and rainforest, normalized so the crest hits exactly
19.3 m), 26 white porthole skylights tilted flush to the slopes and ringing
the domes like craters, the very low very wide profile, the thin floating
eave with its white fascia / light-glass ring / dark PV ring wrapping the
whole perimeter, and the 27 m spider-web piazza canopy at dead center —
a concave `Toy_white_Glow` dish with white rim, oculus, two ring ribs and
twelve radials, so the piazza is the lit core at night per the plan. The full
night state extends the plan's piazza-only glow with three restrained
additions (owner request): glowing porthole rims (rings of light on the dark
hills), a warm `Toy_gold_Glow` clerestory ribbon under the eave reading as
the lit interior through the glass, and lit entrance doors — every glow
surface matches its day-palette neighbour, so daylight looks are unchanged. Glass
perimeter walls carry a chunky ~6.7 m white mullion rhythm beneath the
overhang, with a modest portal-and-steps entrance on the NW concourse front;
no oversized signage is added because the roof itself is the identity.

The four review elevations share one orthographic rig (identical scale,
framing, lighting, exposure) and differ only in azimuth; labels are true
compass directions. The top view shows the hill topography, skylight rings
and flat eave bands; the aerial uses a 40° downward, 105 mm long-lens camera
per the style bible.

## Draft manifest entry (verified values — do not apply in this task)

```json
{
  "id": "cal-academy",
  "file": "cal-academy.glb",
  "anchor": [-122.4662432, 37.7698424],
  "targetHeightM": 19.3,
  "cat": 16,
  "name": "California Academy of Sciences",
  "estimated": false,
  "dims": [212.5214, 207.7346, 19.3],
  "tris": 22384
}
```

The anchor is the OSM way/28695389 centroid recomputed from live Overpass
geometry and matching the plan. **`targetHeightM` deliberately diverges from
the plan's placeholder 11** — see the corrections above; the model's 19.3 m
bounds make the loader's `targetHeightM / measuredHeight` scale exactly 1.0,
so the footprint lands at its true 161.3 × 102.5 m.

## Scope confirmation

The GLB contains the museum building, living roof, piazza canopy and
projecting eave only. No Golden Gate Park planting, Music Concourse, de
Young, paths, trees, people, vehicles, plinth, studio floor, camera or light
is present; studio elements exist only inside the render scripts. The
procedural-fallback guarantee is unaffected: nothing app-side references this
asset yet.
