# 345 Spear Street (Hills Plaza) — reference dossier

Research base: `docs/asset-plans/345-spear.md` Part 2, independently re-verified
in this session. This file records what the model is built from, what was
measured versus estimated, and the corrections made to the plan.

## 1. What this building is

The 1989–91 half of the Hills Plaza complex (architect Whisler-Patri, engineer
Buehler, contractor Koll, ~$60M): a buff-brick office podium (Google's SF
office; floors 1–7) wrapping a sunken courtyard, with the 18-storey white
"One Hills Plaza" residential tower (67 condos, floors 8–18, addressed
75 Folsom St) rising beside the courtyard, a terracotta hip-roofed pavilion
on the Spear Street frontage, and a landscaped level-8 roof garden on the
Folsom/Embarcadero quadrant. The historic Hills Brothers Building
(2 Harrison St, 1926, Kelham) is the OTHER half of the complex — a separate
landmark in a parallel pipeline session, deliberately not modelled here.

## 2. Sources and what each establishes

**Geometry (measured)**
- OSM relation 12734194 (outer way 191970111, 40 pts; inner way 260320992):
  outer ring 7,108 m², min-area OBB 84.0 × 97.5 m at grid bearing 315.1°;
  courtyard hole 494 m² (14.3 × 35.0 m, grid-aligned). Anchor (OBB centre)
  −122.3900655, 37.7900324.
- DataSF LiDAR footprint `201006.0000159` (`mblr SF3744002`): hgt_max 68.46 m,
  median 28.36 m, majority 24.23 m, min 2.62 m, sd 12.38 m, ground 4.36 m.
  The second footprint on the block, `201006.0000430` (max 53.16 m), is the
  Hills Brothers Building.
- DataSF parcels (`acdm-wktn`): block 3744 = ONE merged ground parcel; active
  lots: 2 Harrison ×1, 345 Spear ×2, **75 Folsom ×67** — the 67 condos.
- Google satellite z20 nadir ortho (TL 37.7907946/−122.3911285,
  BR 37.7894380/−122.3894119) with the OSM rings overlaid: roof plan, garden,
  pavilion, and the tower's plan alignment (see §4). Esri z19/z20 as
  cross-check (leans NE; its tower roof is displaced ~10 px NE of Google's).

**Height & program (published)**
- Buehler Engineering (structural EOR): "18-story condominium tower", 900k SF
  mixed-use, architect "Whistler Patri" [sic].
- rises.co: residences on floors 8–18, completed 1991, Whisler-Patri.
- Hoodline (2015): 7 office storeys + residential above, 67 condos, and the
  project's height expectations "around 200 ft" — corroborating a ~61 m body.
- LoopNet/CompStak/commercialsearch: 1989/1990, Class A, 403–427k SF,
  Google anchor tenant.

**Elevations (observed)**
- Street View pano `C5xDvyRE7u80VkU5YnWetQ` ("389 The Embarcadero", camera
  37.789978, −122.388798, © 2026 Google): the Embarcadero elevation — buff
  brick, 6–7 storeys, precast string courses, ground arcade of round-headed
  arches, stepped-gable feature bay; the white tower with its layered stepped
  crown rising behind at bearing ≈265°, which back-projects into the block at
  the courtyard's NE side. Thumbnail recipe:
  `https://streetviewpixels-pa.googleapis.com/v1/thumbnail?cb_client=maps_sv.tactile&w=1600&h=1100&pitch=<p>&panoid=<ID>&yaw=<bearing>`
  (needs a browser UA + google.com referer).
- Street View pano `psfVQFdrsK5ierTdD5rYVg` ("301 Spear St", camera 37.790086,
  −122.390919): the Spear/Folsom corner — 8 storeys flush to the street,
  buff brick, precast spandrels, dark blue-green storefront band at ground.

## 3. Verified numbers used by the build

| Feature | Value | Basis |
|---|---|---|
| Tower crest (bbox top) | **68.50 m** | LiDAR hgt_max; storey math 7×~4.0 + 11×~3.2 ≈ 63 m + crown/mech; the 12.4 m sd is real massing spread, not noise |
| Tower shaft roof | 57.8 m; setback floors to 64.3; parapet 65.0 | derived split of the crown — *inferred* |
| Podium wings | 24.2 m | LiDAR majority (mode) |
| Street frontages | 29.4 m | LiDAR median 28.4 + parapet; SV shows 8 flush storeys at Spear/Folsom |
| SE plaza wing | 27.0 m | between mode and median — *inferred* |
| Pavilion crest | 35.8 m | *estimated* from shadow + storey count; no published figure |
| Footprint | simplified 22-vertex ring, OBB 84.0 × 97.5 m | OSM, measured; entry recess, plaza notch, Folsom service recess, 4-step staircase all real plan features |
| Courtyard | 14.3 × 35.0 m grid-aligned hole | OSM inner ring |
| Manifest anchor | **−122.3901862, 37.7900769** (bbox centre) | derived: OBB anchor + measured AABB offset (10.62, −4.92) m |
| Registry/exclusion anchor | −122.3900655, 37.7900324 (OBB centre) | measured |

## 4. The tower is rotated 45° off the street grid — the key correction

The plan's §2.7 assumed a grid-aligned tower. The nadir ortho shows the tower
roof as a **screen-axis-aligned rectangle among diagonal street-grid roofs**:
its edges run true N–S/E–W, i.e. the tower is turned 45° to the SoMa grid to
face the bay square-on. Corner mapping of its roof in the ortho gives a
~26 × 39 m world-aligned rectangle centred ≈ (12.7 E, 9.9 N) of the OBB anchor;
the build uses 23 × 34 m at (13, 11) so the shaft clears the courtyard hole.
Street View corroborates: from the Embarcadero the tower face reads dead flat
(a grid-aligned tower would show a 45° corner). This diamond-against-the-grid
is the asset's strongest aerial recognition cue after the red pavilion.

## 5. Recognition cues (final ranking)

1. White N–S-aligned tower (diamond on the diagonal grid) with stepped crown
2. Terracotta hip-roof pavilion on Spear
3. Ground arcade answering the Hills Brothers arches
4. Level-8 roof garden + sunken courtyard
5. Buff brick + precast banding + dark blue-green storefronts

## 6. Simplifications (style bible §22/§26)

- 40-vertex ring → 22 vertices (kept: entry recess, plaza notch, service
  recess, all four staircase steps; dropped: a 4.5 m notch near the N corner
  and sub-metre jogs).
- Punched window grid → pier rhythm (8.6 m pitch) + recessed full-width glass
  bands per floor.
- Arcade: 7.4 m arch pitch on the Embarcadero, plaza and step faces.
- Roof garden: paving deck, two mint lawns, one circular fountain, five
  chunky trees (trunk + sphere crown).
- Tower facade: glazing core + white spandrel rings every 3.2 m + corner piers.
- Night: hero = arcade arch glow (Toy_white_Glow); support = one gold crown
  band + six scattered lit windows (Toy_glass_Glow) + entry sign (gold).

## 7. Uncertainties

- Pavilion height is openly estimated (35.8 m crest).
- The tower crown's internal split (57.8/64.3/65.0) is inferred; only the
  68.5 m crest is measured.
- The south (plaza) elevation is a typological continuation — not
  street-visible.
- The Embarcadero staircase terraces are modelled at one level (24.2 m);
  the real steps may descend slightly toward the SE corner.
