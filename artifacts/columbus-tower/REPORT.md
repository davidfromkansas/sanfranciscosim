# Columbus Tower (Sentinel Building) — build & validation report

**Status: PASS** (14/14 contract checks, fresh-scene re-import of the exported
GLB). Asset built locally, not committed and not integrated.

| | |
|---|---|
| File | `columbus-tower.glb` (~600 KB) |
| Objects / triangles | 306 mesh objects / **9,360 tris** (budget 12,000) |
| Dimensions (X,Y,Z m) | 19.883 × 18.251 × **29.000** |
| bbox min / max | (−9.823, −9.101, 0.000) / (10.060, 9.150, 29.000) |
| min Z | 0.0000 |
| XY centre offset | (0.119, 0.024) m |
| Materials | 11, all `Toy_*`, flat, opaque, roughness 0.85 |
| Glow materials | `Toy_white_Glow`, `Toy_gold_Glow`, `Toy_red_Glow` |
| Textures / cameras / lights / animations / armatures / constraints | 0 / 0 / 0 / 0 / 0 / 0 |
| Transforms applied / negative scales | yes / none |
| Normals | 31,500 visibility rays, 0 flipped visible faces → PASS |
| Blender | 5.2.0 LTS, headless (`-b --python`) |

## Orientation decision (required by the task)

The asset is authored in **true-world orientation**: Blender `+Y` = true north,
`+X` = east, so `placeGeneric` needs no rotation. The measured heading of the
apex — the bisector of the Columbus and Kearny street edges at the nose — is
**330.4° true (NNW)**, pointing into the Columbus/Kearny fork; the apex, not any
flat face, is the identity, so no face was turned to −Y. The three edges sit at
their surveyed bearings: Kearny (east) 130.4°, Jackson (south) 260.7°, Columbus
(west) 350.3°. The rounded nose is the arc of the OSM polygon itself: best-fit
circle centre (−6.778, 6.005) m from the origin, radius 2.482 m, sweeping
4.2°→230° (measured CCW from +X), max fit residual 3.4 cm.

The origin is the **footprint bounding-box centre**, which is where the manifest
anchor must sit.

## Anchor and height — verified, and where they differ from the plan

- **Anchor**: the plan's `-122.4050773, 37.7965842` is ~5 m NW of the actual
  footprint centre. Recomputed from OSM way/288485994 through the app's tangent
  projection: **−122.4050266, 37.7965554**. Since `placeGeneric` puts the model
  *origin* on the anchor and this model is centred on its bbox, the recomputed
  value is the correct one and is used in the manifest draft below.
- **Height**: OSM `height=29` is the only published figure and is adopted as the
  **total height to the finial tip**, matching photo proportions (main cornice
  ≈ 22 m, then drum/dome/lantern/finial). The bbox top is normalised to exactly
  29.000 so the loader's `targetHeightM / measuredHeight` scale is 1.000.
- **Storeys**: OSM says 7, Wikidata/Wikipedia say 8. Modelled as **7
  above-ground levels** (ground + 6 bay-window floors), which is what the
  photographs show; the 8th is almost certainly the documented occupied
  basement (the hungry i, later the Kingston Trio studio). Reasoning in
  `REFERENCE.md`.

## Design decisions (style bible §22)

Recognition cues kept: the acute wedge with the rounded nose; verdigris bays,
cornice and dome **on white glazed brick** (the green is on the metalwork, not
the walls — a detail the plan's prose blurs); the per-floor segmental eyebrow
hoods; the full turret sequence (windowed drum → dome → lantern → gold ball →
spire); the red Cafe Zoetrope awnings.

Simplified away: ornamented spandrels and rosettes, curved bow glass (flat bay
fronts with beveled corners), fire escapes, per-pane sashes, the flat-wall attic
arches. Bay counts follow the photographs — **three stacks on Kearny, two on
Columbus** — leaving broad white strips so the green/white contrast reads at
city scale.

Roof (fully designed, ~40% of the visible asset from the app camera): parapet
return, stair penthouse with a verdigris cap, three HVAC blocks on a plant pad,
skylight, water tank on a stand, vent and flue.

Jackson (the back) is deliberately the plain elevation: a regular window grid
and a **service base** with a loading door — not the cafe glazing, which only
wraps Columbus, the nose and Kearny.

## Night state

The app's loader puts `_Glow` surfaces in a separate unlit layer at
`0.12 + 0.95·uNight` opacity, so glow shells are ~12% alpha by day. Every glow
surface here is therefore a **thin shell 3–4 cm proud of opaque glazing**, never
a primary surface. Emission ships at 0 — the app's night pass drives it.
`render_columbus_tower.py` renders both states: the day images fade glow to 12%
alpha (so reviews judge what the app actually shows) and `--night` raises
emission under a moonlit world (`columbus-tower-night.png`).

**The whole building lights up** (David's directive, 2026-08-11): all 73 glow
shells — every bay window on Kearny and Columbus, all six floors of the apex
round bay, the full Jackson grid, all five turret-drum windows, the lantern, the
cafe frontage and service doors, and the cupola beacon.
`Toy_white_Glow` carries the office windows and drum, `Toy_gold_Glow` the warm
ground-floor cafe and lantern, `Toy_red_Glow` the beacon — matching the night
photograph, where the building reads lit throughout with a warm base and a red
light at the cupola.

Day-state trade-off, handled deliberately: lighting every window means every
window carries a shell, and at 12% day alpha that lightens the glazing. The
shells are therefore sized to ~55% of each glazed area rather than covering it,
so by day each window keeps a `Toy_glass` navy border (the style bible's dark
blue-gray window still reads) while at night the lit panel fills the frame.
Gold was reserved for the base for the same reason — gold at 12% over navy glass
goes muddy brown, so upper windows use white.

## Renders

All from the exported GLB, re-imported into an empty scene. Four elevations
share one rig (orthographic, ortho scale 33.64, same lighting/exposure, labelled
by true compass direction): `-north`, `-east`, `-south`, `-west`. Plus `-top`
(orthographic, shows the wedge plan, cornice, apex turret and roof plant),
`-aerial` (105 mm lens, 38° down, azimuth 330° — the app's high three-quarter
camera looking at the apex), `-contact-sheet`, and `-night`.

## Files

```
artifacts/columbus-tower/
  REFERENCE.md                     research dossier + sources
  REPORT.md                        this file
  build_columbus_tower.py          deterministic build (rebuild: blender -b --python)
  render_columbus_tower.py         review renders (add -- --night for the night state)
  validate_columbus_tower.py       fresh-scene contract validation
  make_contact_sheet.py            contact sheet composition
  columbus-tower.blend             authoring scene
  columbus-tower.glb               the deliverable
  validation.json                  machine-readable validation output
  columbus-tower-{north,east,south,west,top,aerial,night,contact-sheet}.png
```

## Manifest draft (not applied — integration is a separate job)

```json
{
  "id": "columbus-tower",
  "file": "columbus-tower.glb",
  "anchor": [
    -122.4050266,
    37.7965554
  ],
  "targetHeightM": 29,
  "cat": 3,
  "name": "Columbus Tower (Sentinel Building)",
  "estimated": false,
  "dims": [
    19.883,
    18.251,
    29.0
  ],
  "tris": 9360
}
```

Integration notes carried forward from `docs/asset-plans/columbus-tower.md`
§2.13, for whoever runs `INTEGRATION-PROMPT.md`: this is a **new** landmark, so
`pipeline/lib/landmarks.mjs` needs an entry (`id: 'columbusTower'`,
`exclude: ~35`) and a re-bake, or the baked block building will occupy the same
wedge. Use the anchor above, not the plan's.

## Contract checklist

| Check | Result |
|---|---|
| Binary GLB, real metres, plausible dims | PASS (19.88 × 18.25 × 29.00 m) |
| Origin base-centre, min Z ≈ 0 | PASS (min Z 0.000, XY offset 0.12 m) |
| Applied transforms, no negative scales | PASS |
| Outward normals | PASS (31,500 rays, 0 flipped) |
| No duplicate/foreign geometry | PASS (306 objects, all authored here) |
| No image textures | PASS (0) |
| No transparency | PASS (all alpha 1.0) |
| Flat `Toy_*` palette materials, no `Toy_body` | PASS (11 materials) |
| `_Glow` only where it should light | PASS (windows, cafe transom, lantern, beacon) |
| No cameras/lights/animations/armatures/constraints | PASS (0 each) |
| ≤ 12,000 triangles | PASS (9,360) |
| No degenerate geometry | PASS (0) |
| Scope: building only, no street/context geometry | PASS |
| Six review renders + contact sheet from the final export | PASS |

See `OPTIMIZATION.md`: a shrink pass evaluated this asset and shipped the ORIGINAL unchanged (all optimization variants regressed the CDN wire size).
