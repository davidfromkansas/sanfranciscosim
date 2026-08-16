# Cathedral of Saint Mary of the Assumption — reference dossier

Research pass executed 10 August 2026 for the SF-SIM miniature asset. The plan
dossier (`docs/asset-plans/st-marys-cathedral.md` Part 2) was used as a starting
point and independently re-verified; the corrections found are listed at the
end. Values below marked *(inferred)* are visual or derived estimates rather
than published figures.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| [Wikipedia — Cathedral of Saint Mary of the Assumption (San Francisco)](https://en.wikipedia.org/wiki/Cathedral_of_Saint_Mary_of_the_Assumption_(San_Francisco)) | 255 ft (78 m) square plan; 190 ft (58 m) high; "crowned with a 55 feet (17 m) golden cross"; saddle roof of **eight** hyperbolic-paraboloid segments; 2,400 seats; consecrated 5 May 1971; Belluschi + Nervi with McSweeney, Ryan & Lee |
| [ArchEyes — Nervi/Belluschi feature](https://archeyes.com/cathedral-of-saint-mary-of-the-assumption-in-san-francisco-by-pier-luigi-nervi-and-pietro-belluschi/) | Confirms 255 ft square and 190 ft height; **eight prefabricated concrete shell segments** joined in-situ; cross-shaped skylight at the apex lighting the central altar; column-free interior |
| [Twentieth Century Society — building of the month](https://c20society.org.uk/building-of-the-month/cathedral-of-st-mary-of-the-assumption-san-francisco) | Confirms 255 ft / 190 ft / **55 ft golden cross atop**; four corner pylons (10 million lb each); stained glass as "narrow linear sections which rise steeply from the four compass points to form a bold cross"; cupola "19 stories above the floor" |
| [OSM relation 7814696](https://www.openstreetmap.org/relation/7814696) | Site multipolygon (124 × 106 m incl. plaza and parking); site grid edge bearings measured 81.0° / 170.9° / 261.0° / 350.9°; outer `height=18.90` (the low base building) |
| [OSM way 436473547](https://www.openstreetmap.org/way/436473547) (building:part, layer 2) | The cupola block: **62.7 m square**, same 81°/351° grid, centroid **-122.4253877, 37.7842352**, tagged `height=60` |
| [OSM way 435831007](https://www.openstreetmap.org/way/435831007) (building:part, layer 4) | The crown traced as a Greek cross: 12 edges all ≈ 18.6–19.0 m → **arm width ≈ 18.8 m, overall span ≈ 56 m**; its `height=77.7 m` tag is almost certainly a data error (77.7 m = 255 ft, the *span* figure) |
| Wikimedia Commons photography (files `Saint Mary of the Assumption - San Francisco, CA - 01`, `Cathedral Hill, San Francisco, St Mary's`, `Saint Mary's Cathedral San Francisco`, `Cathedral of Saint Mary of the Assumption.jpg`) | All four elevations + three-quarter views used for massing calibration (see "What the photographs show") |

The parish site (smcsf.org) and SAH Archipedia returned HTTP 403 to automated
fetches; the smcsf figures reached us via search excerpts (four pylons rated
ten million pounds, cupola 19 stories) and agree with the C20 Society text.

## Verified dimensions and location

| Item | Value | Confidence |
|---|---|---|
| Ground-floor plan | 255 ft = **77.7 m square** | published (Wikipedia, ArchEyes, C20) |
| Cupola crown height above the nave floor | 190 ft = **57.9 m** | published (all three) |
| Golden cross atop the crown | 55 ft = **16.8 m** → apex ≈ 74.7 m above the floor | published (Wikipedia, C20) |
| Shell footprint at its spring | **≈ 62.7 m square** | OSM building:part trace *(inferred from aerial tracing)* |
| Crown plan | Greek cross, arms ≈ 18.8 m wide, span ≈ 56 m | OSM building:part trace *(inferred)* |
| Base building height | OSM tags 18.9 m from street; photographs read ≈ 12–14 m of wall + fascia above the plaza deck | *(inferred; the site slopes and the plaza is raised over a garage)* |
| Roof segments | 8 hyperbolic-paraboloid shells (2 per face, mirrored about each face's glass strip) | published |
| WGS84 anchor (cupola centre) | **-122.4253877, 37.7842352** | OSM building:part centroid |
| Grid orientation | building edges bear 81.0° / 170.9° / 261.0° / 350.9° → the square is rotated **9.1° CCW from cardinal**; the entrance facade faces ≈ 171° true (Geary Boulevard side) | measured from OSM geometry |

## Orientation

The building is four-way symmetric above the base. The Western Addition grid
here runs 81° (Geary) × 171°; the main entrance, monumental stair, and garage
entry face Geary on the south-southeast (bearing ≈ 171°). The asset is authored
with Blender +Y = true north and the whole model yawed +9.1° CCW so it drops
onto the city at its real heading; the entrance face is the −Y-most face,
satisfying the front-faces-−Y rule as closely as the real heading allows.

## What the photographs show

**All four elevations (near-identical above the base):** a taut white shell
whose central ~19 m band rises almost vertically the full height, split down
the middle by a narrow, nearly black stained-glass slot (~2 m wide); from the
central band the surface sweeps out to the corners in a strong concave flare
that does most of its widening in the bottom third and is nearly vertical
above mid-height. The bottom corners continue *past* the base fascia as
buttress sweeps that land at plaza level. The shells carry a fine precast
panel grid (dropped in the miniature — flat color).

**South (Geary) front:** a wide monumental stair rises over the garage entry
to the raised plaza; tall dark bronze relief doors sit in a travertine base
wall; above the base runs a thin projecting white fascia/eave slab on which
the shells appear to sit. Glazed curtain-wall bays occupy the flanking base
corners.

**Top/aerial:** the crown reads as a Greek cross; each arm's top edge slopes
gently *up* toward the centre where the slender openwork golden cross stands.
The glass slots continue from the four faces over the arm crests, meeting at
the apex as the cross-shaped skylight. Around the cupola, the flat roof of the
base forms a pale ring out to the fascia edge.

**Night:** the four glass slots and the crest cross glow warm from the lit
interior — a cross of light on each face and a glowing + seen from above.
This is the asset's night signature.

## Recognition cues (ranked)

1. The hyperbolic-paraboloid silhouette: near-vertical centre, dramatic
   concave corner sweeps — nothing else in the city looks like it
2. Monolithic white/travertine monochrome with essentially no ornament
3. The narrow dark stained-glass cross: a full-height slot up each face,
   continuing over the crown
4. The slender golden cross standing 17 m above the crown
5. A tall sculptural roof on a very low, wide travertine base with a thin
   projecting fascia

## Features to preserve

- True concave corner-sweep curvature (fast flare low, vertical high); a
  straight-sided pyramid or cone will not read as this building
- The proportions 77.7 m base square / 62.7 m shell spring / ~57.9 m crown
- The full-height glass slots, dark by day, glowing by night
- The corner buttresses running past the fascia down to the plaza
- The 16.8 m golden cross (kept at real scale — it is already semantically large)
- The stark monochrome; saturated color appears nowhere except the gold cross

## Features to simplify

- Precast panel grid on the shells → flat `Toy_white`
- Travertine coursing, door reliefs → flat `Toy_stone` base + `Toy_ink` door panels
- The eight structural shells → one lofted square-to-cross surface with the
  mirrored-halves geometry implied by the recessed glass slots
- The plaza (real site is 124 × 106 m with parking) → a compact symmetric
  podium with the south monumental stair; parish centre, school and the
  parking structure are out of scope
- Interior (Lippold sculpture, organ, baldachin) → not modelled

## Uncertainties and conflicts

- **The published numbers make a squatter building than the photographs
  show.** 190 ft (57.9 m) to the crown, minus a ~14 m base, leaves ~44 m of
  visible shell over a 62.7 m spring square — a height/width ratio of about
  0.70. Measured off the two straight-on photographs (`Cathedral Hill, San
  Francisco, St Mary's` and `Saint Mary's Cathedral San Francisco`) the
  visible shell reads 0.88–1.04, and both are wide-angle or low-angle shots
  that would *understate* height if anything. Two explanations fit: the shell
  continues down behind the base annex (so its true springing is at plaza
  level), or OSM's `height=77.7 m` on the crown part is a real measurement
  rather than the 255 ft span misfiled. **Decision:** keep the published
  190 ft crown — data accuracy is the product — and close part of the gap
  from the other side: spring square pulled in to 60 m, base walls kept to
  13.2 m with the fascia at 14.6 m. That yields ~0.76, which is honest about
  the sources while letting the signature feature dominate as the style bible
  permits (§3 semantic scale, §22 exaggerate the signature feature).
- **Crown span:** OSM traces the crown cross at ≈ 56 m span; the photographs
  show a crown at least as wide as the springing. Decision: arm half-span
  31 m (62 m span), just proud of the 60 m spring square.
- **Base height:** OSM says 18.9 m, probably measured from the sloping street;
  photographs read ~10–13 m above the plaza deck. Decision: 9.2 m of base wall
  plus a 1.4 m fascia above a 4 m podium.
- **The 55 ft golden cross** is consistently published, but no source states
  whether "190 ft high" includes it. Decision: crown apex at 57.9 m above the
  nave floor with the cross above it, matching the phrase "crowned with a
  55 feet (17 m) golden cross"; the model therefore tops out at 78.7 m above
  the podium base.
- The OSM `height=77.7 m` tag on the crown part is not used; it equals the
  255 ft span figure exactly, which makes a transcription error likely.

## Corrections to the plan dossier

1. **Eight shells, not four.** Each face is a mirrored pair of hypar segments
   split by its glass slot; visually this is captured by the slot geometry.
2. **The anchor was the site centroid.** The plan's anchor
   (-122.4252894, 37.7839772) is ~30 m south-east of the cupola centre; the
   asset anchors at the cupola centroid **(-122.4253877, 37.7842352)**.
3. **The golden cross is 16.8 m tall,** not the ~4 m cap in the plan's massing
   recipe, so the asset tops out at ≈ 74.7 m and `targetHeightM` must be the
   full modelled height, not 58.
4. **No entrance canopy exists** on the real south front — the projecting
   fascia and recessed doors do that job; the plan's 20 × 6 m canopy + piers
   are replaced by the faithful fascia + recessed entrance.
5. **The shells spring from ≈ 62.7 m square** (OSM building:part), not from
   the full 77.7 m square, which is the ground-floor plan.
6. **There are no corner buttresses below the fascia.** The plan's massing
   recipe and an early build pass both added them; the photographs show the
   shell corners simply landing on the base roof behind the projecting
   fascia. They were removed.
