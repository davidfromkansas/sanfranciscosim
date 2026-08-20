# Pier 7 — SF-SIM asset plan

**Pier 7 (the Broadway Pier)**, 7 The Embarcadero — an **840-foot public access and fishing
pier** at the foot of Broadway, dedicated in **October 1990** on the site of a 1901 cargo
pier demolished after Loma Prieta. Designed by **ROMA Design Group** with **T.Y. Lin
International** engineers for $6.57 M of pooled public money, and awarded the **1993 ASLA
National Honor Award**: timber decking, ornamental iron handrails, antique iron-and-wood
benches, and two full-length rows of Embarcadero-style lamp standards marching 256 m out
into the Bay toward nothing at all. It is the city's photography pier — the fog pictures
with the lamp rows converging at infinity are all taken here — and one of its best fishing
spots. There is **no building on it**. The asset is deck, piles, railings, lamps and
benches, and the discipline is to let those four systems *be* the design.

This is a **water asset** in the `pier-3` mould: nothing under it is land. The loader seats
generic landmarks at `max(0, sampleElevation(x, z))`; the app's terrain samples **0.00
across the entire footprint** (verified against the baked heightmap), so the origin lands
exactly on the water plane y = 0. Every height in this plan is quoted **above water level**.

**Deliverable:** a validated miniature GLB plus dossier, renders and report under
`artifacts/pier-7/`. Part 1 is the runnable task prompt, Part 2 the dossier behind it.

| | |
|---|---|
| Manifest id | `pier-7` (registry id `pier-7` — camelId keeps the hyphen before a digit, the pier-3 rule) |
| Existing procedural builder | none — new landmark, **Case B** (registry entry + tile re-bake; the bake DOES carry the pier as a 1.2 m slab, see 2.13) |
| WGS84 anchor | `-122.3955159, 37.7994429` (footprint OBB centre, over open water) |
| Target height | **7.6 m** — waterline to lamp-globe tops: deck top +3.0 m, lamps +4.6 m above deck. A vertical extent, not an architectural height |
| Footprint | 257.3 m × 26.9 m OBB, 6,920 m² measured from OSM way 23605169; plan is plaza / walkway / mid bay / walkway / end platform, see 2.3 |
| Axis heading | Long axis bears **054.7°** into the Bay; the entry faces **234.7°** (same family as Pier 1's 053.8° and Pier 3's 053.9°) |
| Triangle cap | 14,000 |
| Category | `0` (misc — open space; the taxonomy has no park category, and `golden-gate-bridge` set the precedent) |

---

## Part 1 — Task prompt

Copy everything in the block below into a fresh Devin/Claude session.

````markdown
# Create a production-ready Pier 7 GLB for SF-SIM

Work in: https://github.com/davidfromkansas/sanfranciscosim

Create a stylized miniature 3D model of **Pier 7 (the public access pier at the foot of
Broadway), 7 The Embarcadero, San Francisco** and deliver it as a downloadable, validated
GLB. Do not integrate or deploy the model yet.

## Read the project sources first

Before any research or modeling, read in this order:

1. `AGENTS.md`
2. `docs/styles/README.md`
3. `docs/styles/miniature-toy.md`
4. `.agents/skills/sf-miniature-style/SKILL.md`
5. `.agents/skills/sf-asset-check/SKILL.md`
6. `app/public/sf-assets/landmarks_manifest.json`
7. `docs/asset-plans/pier-3.md` — the governing water-datum precedent (origin on the
   waterline, pile field modelled, heights above water)
8. `docs/asset-plans/pier-1.md` — the pier-typology precedent (deck/fascia/pile recipe,
   railing and lamp budgets, the long-thin-asset render advice)
9. `docs/asset-plans/pier-7.md` — this plan; your research starting point, not a substitute
   for your own verification

Authority order: `docs/styles/miniature-toy.md` governs artistic interpretation,
`.agents/skills/sf-asset-check/SKILL.md` governs the technical contract, `AGENTS.md`
governs repository rules.

## Must capture

- **The two lamp rows.** Forty-plus Embarcadero-style standards — slim dark posts with a
  single warm opal globe — in two dead-straight rows the full 256 m, on a regular beat.
  This is the identity. At night the pier IS the lamp rows; from the aerial camera by day
  it is the rhythm of small bright dots down a dark timber deck.
- **The plan sequence**: a ~20.7 × 12.3 m **entry plaza** at the seawall with rounded
  seaward corners (granite "Bay Bench" pair and a bronze water-viewing grill); a
  **7.5 m timber walkway**; a **~16.8 × 22 m widened mid-pier fishing bay**; the walkway
  again; and a **26.9 m-wide, ~15.6 m-deep end platform** with clipped corners, 257 m
  out. The wide-narrow-wide-narrow-wider beat is what the aerial camera reads.
- **The ornamental iron railing** — 1.07 m (42 in) high, near-black, continuous around
  every edge, with a visible post rhythm. Simplify the scrollwork to posts + two rails; do
  not omit the railing anywhere, it is the pier's only wall.
- **The timber deck** reading as *planked wood*, not concrete: warm brown, with plank
  direction along the pier and a subtle two-tone strip pattern if the budget allows.
- **The bench rhythm** — antique iron-and-wood benches parked against the railing along
  both flanks, densest at the mid bay and end platform.
- **The pile field.** Concrete piles from the waterline to the deck soffit at +3.0 m; the
  camera goes to water level and an unsupported 257 m slab will be seen. Perimeter bents
  plus a suggestion of interior rows at the wide bays; fascia band all round.

## Research Pier 7 independently

Verify the dossier rather than trusting it. Re-check at minimum the footprint and its
five-part plan, the anchor, the deck height above water, the lamp spacing and height, and
the real-world heading. Gather references covering: the pier head-on down its axis (the
classic fog photograph), both flanks from the water, the entry plaza from the Embarcadero,
aerial/satellite views, and night shots of the lamp rows. Good starting points:
pierfishing.com's Pier 7 page, foundsf.org, the Port's Waterfront Design & Access document,
stevegillmansculpture.com (Bay Bench), Unsplash/Flickr geotagged photography. Label
anything measured from photos *estimated*.

**Known source traps, already resolved in 2.1 — re-check, don't re-inherit:**

- OSM way 23605169 is `man_made=pier` with **no height tag and no building tag**. There is
  nothing to mis-read; the heights in this plan are photogrammetric estimates and say so.
- The pier is quoted as "840 feet" (256 m). The measured OSM footprint is 257.3 m — use the
  measurement.
- The deck height above MLLW is **estimated at 3.0 m** from the Embarcadero promenade level
  (~2.9–3.0 m) it meets flush at the seawall. The app's DEM reads 0.0 over the whole pier
  and ~1.6–2.9 m only at the seawall joint, so the model must carry the full deck height
  itself.

## Create a reference dossier

Write `artifacts/pier-7/REFERENCE.md`: source links and what each establishes; verified
dimensions; orientation; observations from both flanks, the axis and above; recognition
cues; simplifications; uncertainties. No copyrighted full-res imagery in the repo.

## Make your own design decisions

Follow `docs/styles/miniature-toy.md` §22. This is a **quiet landmark with one loud
feature** (the lamp rows). Spend the budget on lamp/railing/bench rhythm and the pile
field; there is no facade, no roof furniture, no massing drama. The failure mode is a
featureless brown plank: the fix is crisp repetition, not added invention. The second
failure mode is scale creep — a 4.6 m lamp is small, and making it "read better" at 8 m
would wreck the pier's horizontality and its `targetHeightM`.

## Scope of the exported asset

Export: deck slab with fascia and bullrail, pile field, entry plaza paving band with the
two granite benches and bronze grill, railing on every edge, lamp standards, benches, the
two fish-cleaning stations near the end platform.

Do NOT include: the Embarcadero roadway or promenade, seawall, lawn, palms; Pier 5 or
Pier 9; boats; the water surface; people; birds; fishing gear; signage; cameras or lights.

## Technical asset contract

Follow `.agents/skills/sf-asset-check/SKILL.md` in full. Binary GLB, real metres, applied
transforms, no negative scales, outward normals, no textures/transparency, flat `Toy_*`
materials, `_Glow` only on the lamp globes, no `Toy_body`, no cameras/lights/animations,
≤ 14,000 triangles.

**Water datum — the pier-3 rule.** Origin on the water plane; minimum geometry Z = 0 is
the **waterline** (pile feet), deck top at +3.0 m, lamp tops at +7.6 m. Do not sit the
deck on z = 0.

**Orientation:** author with Blender `+Y` = true north, `+X` = east. The pier runs out on
bearing **054.7°**; build directly on the measured footprint polygon in 2.3, never an
axis-aligned box rotated by eye.

**Height normalization:** the bbox top (lamp globes) must land at exactly **7.6 m** so the
loader's scale is 1.0. Record in REPORT.md that `targetHeightM` is a vertical extent above
the waterline, and that the tallest geometry is a lamp, by design.

## Reproducible Blender workflow

Blender 5.2 LTS headless. Keep `artifacts/pier-7/build_pier_7.py` (deterministic),
`pier-7.blend`, `pier-7.glb`.

## Required review renders

`pier-7-top.png`, `pier-7-north.png`, `pier-7-east.png`, `pier-7-south.png`,
`pier-7-west.png`, `pier-7-contact-sheet.png`, a high three-quarter aerial
`pier-7-aerial.png` from the **south-west** (the app's view: entry plaza in front, lamp
rows converging away), a second low view from the water off the SE flank, and
`pier-7-aerial-night.png`. At 257 m the elevations need a long aspect (e.g. 3200×500).
Night render: copy Base Color into Emission Color at strength 1.0 on `_Glow` materials of
the re-imported GLB (glTF drops authored emissive colour otherwise).

## Validate the exported GLB

Fresh-scene re-import; write `artifacts/pier-7/validation.json` and `REPORT.md`. Expected
non-failures to state explicitly: min Z = 0 **is the waterline** (pile feet), and the
axis-aligned XY bbox will be roughly **218 × 165 m** for a 257 × 27 m pier — the 54.7°
heading, not a scale error.

## Manifest draft

```json
{
  "id": "pier-7",
  "file": "pier-7.glb",
  "anchor": [-122.3955159, 37.7994429],
  "targetHeightM": 7.6,
  "cat": 0,
  "name": "Pier 7",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

Do not edit the production manifest, `pipeline/lib/landmarks.mjs`, or app code in this
task. Integration is `docs/asset-plans/INTEGRATION-PROMPT.md` plus §2.13 of this plan,
which contains a measured exclusion analysis.
````

---

## Part 2 — Research and design dossier

### 2.1 Verified facts

| Fact | Value | Confidence / source |
|---|---|---|
| Name | Pier 7 ("Broadway Pier" colloquially) | pierfishing.com; CDFW Fishing in the City |
| Address | 7 The Embarcadero (foot of Broadway), SF 94111 | Nominatim; CDFW |
| OSM way | `23605169` (`man_made=pier`, `area=yes`, `surface=wood`, `floating=no`, no height, no building) | measured, Overpass |
| History | A Pier 7 has stood here since **1901** (passenger terminal → cargo → post-1973-fire parking and fishing); damaged in the **1989 Loma Prieta** quake; old Piers 5 and 7 demolished; the present pier **dedicated October 1990** | pierfishing.com; foundsf.org |
| Designer | **ROMA Design Group** (Boris Dramov, principal); engineers **T.Y. Lin International**; entry-plaza site design Kring Design Studio; "Bay Bench" granite/bronze art by Steve Gillman (SF Arts Commission, 1990) | bolerium.com (1983 design booklet listing); Wikipedia (ROMA Design Group); stevegillmansculpture.com |
| Award | **1993 ASLA National Honor Award** (Design) | Wikipedia, ROMA Design Group |
| Cost / funding | $6,568,581 — SF Rec & Parks, Port of SF, State Wildlife Conservation Board, LWCF (NPS), State Coastal Conservancy, State Block Grant | pierfishing.com |
| Length | **840 ft**; measured footprint **257.3 m** along axis | pierfishing.com; OSM ring reprojected |
| Width | 26.9 m max (the Bay-end platform); entry plaza 20.7 m; main walkway **7.4–7.5 m**; mid bay 16.8 m | measured, OSM ring |
| Water depth at end | ~35 ft | pierfishing.com |
| Structure | **Concrete pilings**, **timber decking** (closely spaced planks, wheelchair-safe), **42 in (1.07 m) ornamental metal railing**, antique-style iron-and-wood benches, Embarcadero light fixtures, fish-cleaning stations, water taps | pierfishing.com (two pages) |
| Deck height above water | **~3.0 m** (*estimated* — meets the Embarcadero promenade, itself ~2.9–3.0 m, flush at the seawall; app DEM reads 1.6–2.9 m at the joint) | inferred + baked heightmap sampled |
| Lamp standards | single-globe Embarcadero style, **~4.6 m** (*estimated*, ~4.3× the 1.07 m railing in photos); two rows full length plus plaza and end units, spacing **~12 m** (*estimated* from photos/satellite) | observed (Unsplash/Flickr photography) |
| App terrain at site | 0.00 across the pier; 1.59 m at 128 m shoreward of the anchor, 2.93 m at the seawall | measured, baked heightmap |
| Long-axis heading | **054.65°** out into the Bay; entry faces 234.65° | measured, OSM ring OBB |
| Anchor (OBB centre) | `-122.3955159, 37.7994429` → local x 3694.4, z −3254.6, tile cell **23_9** | derived |

### 2.2 Sources

- **pierfishing.com/pier-7-san-francisco** — the richest single source: 1901 origin, 1990
  dedication, funding table and $6,568,581 total, 840 ft length, 35 ft water, timber
  decking, ornamental iron handrails, antique benches, Embarcadero light fixtures,
  42-inch railing, plank surface, fish-cleaning stations. *Secondary but detailed.*
- **Wikipedia, ROMA Design Group** — designer credit; 1993 ASLA National Honor Award.
- **bolerium.com** — "Pier 7: a recreation and public access design project", ROMA
  Architects and T.Y. Lin International Engineers, 1983 — the design booklet itself.
- **stevegillmansculpture.com/bayBench.html** — Bay Bench, 1990: two granite benches
  17 in high × 8 ft 6 in square flanking the entry, bronze grill viewing the water; Kring
  Design Studio site design; SF Arts Commission.
- **foundsf.org/Pier_7** — site history photos 1900s–1970s (parking-lot era, freeway era).
- **sfport.com WDesAcc.pdf** — Waterfront Design & Access: Pier 7 as the key public-access
  feature of the Broadway Open Water Basin; railing transparency guidance.
- **CDFW Fishing in the City** — "Pier Seven … at the end of Broadway", public fishing.
- **Photography (observed)** — Unsplash `EkXPhMNdKBg` (fog, lamp rows, benches) and the
  large geotagged corpus at this pier: dark deck, near-black ironwork, warm globes.
- **Exa queries used:** "Pier 7 San Francisco public fishing pier Broadway Embarcadero
  history built 1990 design"; ""Pier 7" San Francisco pier wooden deck iron railings lamp
  posts photos"; "Pier 7 San Francisco 1990 public access pier designer architect award
  concrete piles timber deck Port of San Francisco". Domains that yielded facts:
  pierfishing.com, wikipedia.org, bolerium.com, stevegillmansculpture.com, sfport.com.

### 2.3 Footprint, orientation and the water datum

Measured ring (OSM way 23605169) reduced to the pier's own frame — `u` along the axis
(0 at the seawall, 257.3 at the Bay end), `v` across (0…26.9):

In the pier frame — `s` along the axis (0 at the OBB centre/anchor, −128.6 at the
seawall, +128.6 at the Bay end), `t` across (+ toward the SE):

```
entry plaza    s −128.6 … −116.3   ~20.7 m wide, 12.3 m deep, rounded corners
                                   necking into the walkway; asymmetric — the SE
                                   side steps in at s ≈ −123.5
walkway 1      s −116.3 … −21.9    7.5 m wide (t −0.8…6.7, drifting ~1 m)
mid bay        s  −21.9 …  +1.9    16.8 m wide fishing bay, ~22 m long, 45°
                                   transition chamfers both ends
walkway 2      s   +1.9 … +113.0   7.4 m wide (t −3.6…5.1)
end platform   s +113.0 … +128.6   26.9 m wide (full OBB width), ~15.6 m deep,
                                   clipped corners, small step notches at the joint
```

The plaza sits against the seawall where the DEM rises to 2.9 m; the rest of the pier
samples 0.00. **Origin on the waterline** (pier-3 rule): pile feet at z = 0, deck top at
+3.0, bullrail +3.35, railing top +4.07, bench backs +4.0, lamp globes topping out at
+7.6. The loader seats y = 0 at the anchor; at the seawall the plaza edge meets terrain
that has risen to ~2.9 m, so the plaza joint buries by a few decimetres — right way round.

`yawDeg` is not used: author in true-world orientation, `+Y` north, on the measured
polygon.

### 2.4 What each view shows

**Down the axis from the entry (the classic photograph).** Two rows of dark lamp standards
converging to a vanishing point; between them a dark planked deck; near-black ornamental
railings closing both edges; benches every few bays facing inward; the Bay beyond.

**The flanks from the water.** A long dark horizontal band (fascia + bullrail) on a rhythm
of paired concrete piles; above it the railing filigree and the lamp beat; nothing taller.
The mid bay and end platform step the band outward.

**From above (the app's camera).** The five-part plan reading as a long tool-handle:
plaza at the shore, thin shaft, a swelling at the middle, thin shaft, and the widest
platform at the Bay end. Warm plank field, pale plaza band at the shore end, the lamp
dots in two lines, bench dashes along the edges.

**At night.** Two dotted lines of warm globes over black water. Nothing else. This is the
easiest night state in the whole landmark set and it must not be over-lit.

### 2.5 Recognition cues (ranked)

1. **The converging lamp rows** — two straight lines of single-globe standards, 256 m.
2. **The five-part plan** — plaza / walkway / mid bay / walkway / end platform.
3. **Near-black ornamental railing** boxing every edge of a warm timber deck.
4. **Benches against the rails**, iron-and-wood, evenly beaten.
5. **A pier with no shed** — its emptiness IS the identity among the built-up finger piers.

### 2.6 Miniature translation

- **Lamps are the hero.** Model one beautiful standard (fluted-suggestion post, collar,
  globe) and instance it on a strict beat. Exaggerate the globe to ~0.45 m diameter so it
  reads as a dot from altitude (style bible §8).
- **Railing simplified to posts + top rail + mid rail**, posts on a ~3 m beat with a
  slightly heavier principal post at the lamp positions. The scroll ornament is sub-pixel;
  the *rhythm* is not.
- **Deck as two-tone planking**: broad field `Toy_timber` with thin darker strips every
  ~2.4 m suggesting plank courses; a pale granite band across the entry plaza.
- **Benches as one 5-face unit** (seat, back, two ends), instanced.
- **Piles**: perimeter bents on a ~5.5 m beat (pairs under the walkway edges, triples
  under the wide bays), plus fascia; no interior forest.
- **Do not add**: kiosks, flags, planting, boats, a building. The pier is bare by design.

### 2.7 Massing recipe

1. **Deck slab** — extrude the measured polygon, top +3.0, soffit +2.4; fascia band
   +2.4…+3.0 all round in `Toy_ink`.
2. **Bullrail** — 0.3 × 0.35 m timber curb at the deck edge, top +3.35.
3. **Piles** — 0.45 m square posts, waterline to soffit, chamfered; bents every ~5.5 m
   along both edges, inset 0.4 m; doubled rows under mid-bay and end-platform edges.
4. **Railing** — posts 0.08 m square to +4.07 with a small finial cube, top rail and mid
   rail 0.06 m; runs on every edge except a 4 m entry gap at the plaza.
5. **Lamps** — 42 standards: 18 per flank at ~12.8 m centres along the walkways and bays,
   4 on the end platform, 2 flanking the entry plaza. Post 0.14 m ⌀ to +6.9, collar,
   0.45 m globe centred +7.35, top +7.6 (`Toy_lamp_Glow`).
6. **Benches** — 16 units, 1.8 m, backs to the railing: 3 pairs along each walkway, 2 at
   the mid bay, 2 on the end platform.
7. **Entry plaza** — granite paving band (`Toy_stone`, +3.02 to avoid z-fight with the
   timber field), the two Gillman granite benches (0.43 m high, 2.6 m square) flanking the
   axis, a 1.2 × 2 m bronze grill plate inset flush.
8. **Fish-cleaning stations** — two 1.5 m steel tables against the end-platform railing.

### 2.8 Materials and palette

| Surface | Material | Hex | Note |
|---|---|---|---|
| Deck planking field | `Toy_timber` | `8a6a4a` | warm mid-brown; strips `7a5c3e` |
| Bullrail, bench wood | `Toy_timber` | `8a6a4a` | one wood everywhere |
| Deck fascia, piles | `Toy_ink` | `3a3530` | pier-1 precedent; grounds the slab |
| Railing, lamp posts, bench frames, grill | `Toy_ink` | `3a3530` | near-black ironwork — do NOT go darker; the app's light will crush it (see sf3d app-lighting rule) |
| Entry plaza band, granite benches | `Toy_stone` | `d9d2c2` | |
| Fish-cleaning tables | `Toy_steel` | `9aa0a6` | |
| Lamp globes | `Toy_lamp_Glow` | `f6e3c0` | the base colour IS the night look (unlit overlay); warm pale, never saturated yellow. By day it reads as an opal globe — correct |

Two woods, one iron, one stone, one glow. Nothing else.

### 2.9 Night state

- **Hero and only:** the 42 lamp globes. `Toy_lamp_Glow` base `f6e3c0`.
- **Not lit:** everything else. No deck wash, no railing glow, no plaza accent. The real
  pier at night is two lines of dots; restraint is the design.
- Globes are solid glow-material spheres standing proud on their posts — never a glow
  shell wrapped over another surface (day-alpha trap).

### 2.10 Scope

**In:** deck, fascia, bullrail, piles, railing, 42 lamps, 16 benches, plaza band, 2
granite benches, bronze grill, 2 fish stations.
**Out:** roadway, promenade, seawall, palms, Piers 5/9, boats, water, people, gear,
signage. **Deliberately omitted:** the water taps (sub-pixel), the pier's flag holders
(unverified), any interpretation of scroll-work in the railing (sub-pixel).

### 2.11 Triangle budget

| Element | Budget |
|---|---|
| Deck slab, fascia, bullrail, plaza band | 1,600 |
| Piles (perimeter bents, doubled at bays) | 2,000 |
| Railing (posts, finials, 2 rails, all edges) | 3,200 |
| Lamps (42 × ~110) | 4,600 |
| Benches (16 × ~110) | 1,800 |
| Plaza: granite benches, grill | 300 |
| Fish stations | 200 |
| Slack | 300 |
| **Total cap** | **14,000** |

First cut if over: lamp globe subdivision, then railing post rate (3 m → 4 m), never the
lamp count — the beat is the identity.

Streaming: `loadRadius: 2500` (default rule `max(2500, 7.6 × 30 = 228)`). Beyond 2.5 km
the site is open water; take the default, the pier-3 argument applies verbatim.

### 2.12 Draft manifest entry

```json
{
  "id": "pier-7",
  "file": "pier-7.glb",
  "anchor": [-122.3955159, 37.7994429],
  "targetHeightM": 7.6,
  "cat": 0,
  "name": "Pier 7",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

**Do not** rewrite `landmarks_manifest.json` with `JSON.stringify` — append as text (the
serializer renumbers other landmarks' `11.0` → `11`).

### 2.13 Integration notes — the bake DOES carry Pier 7

Case **B**, and unlike a vacant lot the committed tiles carry the pier itself as
procedural geometry. Measured against the committed `23_9` tiles (min of centroid- and
any-vertex-distance to the anchor, i.e. `excluded()`'s own test):

| Record | What it is | Extent (pier frame) | Top | Dist to anchor |
|---|---|---|---|---|
| buildings `23_9#16` | the pier as a low slab (Overture) | u −131…128, v −16…14 (full pier) | 1.2 m | **4.5 m** |
| toy `23_9#7` | toy-tier twin of the same footprint | full pier | 2.1 m | **4.5 m** |
| toy `23_9#8/#9/#10` | 2.5 × 2.5 m toy roof bumps on the slab | u 85, 24, −2 | 2.5 m | **85.2 / 23.7 / 10.0 m** |
| nearest keeper | toy `23_9#16` (Embarcadero side) | — | 4.5 m | **126.1 m** |

Registry entry:

```js
{
  id: 'pier-7',
  name: 'Pier 7',
  lon: -122.3955159,
  lat: 37.7994429,
  height: 7.6,
  exclude: 60,
  camera: { distance: 420, yaw: 215, pitch: 20 },
}
```

**Why r = 60 (re-measured against the bake input, 12 Aug data vintage):** the pier
bakes from exactly ONE input footprint — **DataSF `area_id 855`** (495 verts tracing
the whole pier, `hgt_max` 4.96 m / median 2.55 m), whose min(centroid, vertex)
distance to the anchor is **1.4 m** — any radius catches it. The tiles' small toy
bumps (`23_9#8/#9/#10`) do **not** exist in the input: they are toy-pass roof
furniture on the slab and vanish with their parent. The binding constraint is the
**San Francisco Belle** (Overture, from OSM w281243626) — the moored riverboat off
Pier 3, whose nearest vertex is **98.6 m** from the anchor: the plan's first-draft
r = 100 would have deleted a boat that is not ours. r = 60 catches the target at
1.4 m and spares the Belle by 38.6 m; the next input footprints are at 116.3 m
(Overture, 11 m) and 126.1 m (DataSF 3757, Pier 5 side).

Integration checks specific to this asset:

- After the bake, decode `23_9` both tiers and confirm the slab records are gone and the
  keeper count is otherwise unchanged; do not trust per-cell counts alone.
- Watch for the **Overture height-correction re-targeting** onto a surviving neighbour
  (it has made a keeper taller after an exclusion before).
- Check the **streets tier** over the pier: if OSM carries a footway on the deck, a baked
  path may float at deck height inside the model. If present, judge visually — a path
  strip under our deck at +2 m is invisible; one above it is a defect to fix by exclusion
  or report.
- `placeGeneric` must seat at exactly **y = 0** (merge line). A non-zero seat means the
  anchor drifted onto the seawall; move the anchor back, never compensate in the model.
- QA from **water level at the pier end** (piles must read) and **down the axis at night**
  (the lamp rows are the acceptance test).
- Shared-batch reserve: check before integrating; the batch has overflowed before.

`BATCH: yes`: run the bake and full QA, then `git checkout -- app/public/tiles api/_data`
and commit source only.

### 2.14 Validation checklist

- [ ] Fresh-scene re-import validated, not the source scene
- [ ] min Z = 0 **is the waterline** (pile feet), deck top at +3.0 — stated in
      validation.json as a PASS with the reason
- [ ] Bbox top exactly **7.6 m** (lamp globes; loader scale 1.0)
- [ ] XY bbox ≈ 218 × 165 m — the 54.7° heading, not a scale error; stated as PASS
- [ ] ≤ 14,000 triangles; ≤ 500 KB after `pipeline/compress-assets.mjs`
- [ ] Materials all `Toy_*`, flat, no textures/alpha; `_Glow` only on lamp globes
- [ ] No cameras/lights/animations/armatures; applied transforms; no negative scales
- [ ] Outward normals (per-object signed volume; ray residual ≤ 0.15%)
- [ ] Day + night renders from the re-imported GLB; night = two dotted lamp lines only

### 2.15 Open questions and risks

1. **Lamp height (4.6 m) and spacing (~12.8 m) are photo estimates.** Check the
   lamp-to-railing ratio on a head-on photo before finalizing; the railing's 42 in is
   documented and calibrates the frame. If lamps land at 4.0 or 5.2 m, `targetHeightM`
   moves with them — re-derive, don't fudge.
2. **Deck height 3.0 m is inferred** from the promenade joint. Tolerant of ±0.4 m; the
   pile proportions absorb it.
3. **The toy bumps (#8–10) are explained** — verified absent from the bake input, so
   they are toy-pass roof furniture on the DataSF 855 slab and vanish with it. The
   binding neighbour is the San Francisco Belle at 98.6 m; r = 60 clears it (2.13).
4. **Lamp count (42) is an estimate** from satellite dot-counting and photos. The beat
   matters more than the count; keep the spacing honest and let the count fall out.
5. **Bench count/placement is observational.** Benches are dense at the mid bay and end
   in photos; exact positions unverifiable and unimportant at this scale.
6. **This is the first *unbuilt* pier in the set** — deck-furniture-only. If the lamp
   instancing budget works here it becomes the template for the Agua Vista / Torpedo
   Wharf class of open piers.
