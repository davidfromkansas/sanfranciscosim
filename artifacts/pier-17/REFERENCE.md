# Pier 17 — reference dossier

Sources, verified numbers and design decisions behind `pier-17.glb`. The plan
(`docs/asset-plans/pier-17.md`) is the research starting point; everything
below was re-verified during the build, and the corrections are in REPORT.md.

## Sources

| Source | What it establishes |
|---|---|
| Wikimedia Commons `File:Pier_17_(San_Francisco)_July_2022.JPG` | The bulkhead front, street level: cream stucco, full-width shallow gable, "PIER 17" diamond-ended sign plate, apex flagpole with flag, central olive-gray roll-up flanked by weathered diagonal-plank timber barn doors, receiving door + window band at the right (SE) edge. *Observed.* |
| Google satellite tiles z19/z20 (37.8022, −122.3981) | Roof value split (white membrane main run, weathered gray front section), thin bright ridge line, deck aprons all around, bay-end step, Pier 15 solar roof next door. *Observed (aerial).* |
| Exploratorium press office, "Pier 15 Facts of Interest" (2011) | Built **1912**, third-oldest pier on the waterfront; ~110,000 sq ft; keeps the **last remaining original fog horn**. |
| Port of SF, Exploratorium project sheet (Dec 2010) | Campus rehabilitation 2010–13, EHDD Architecture + Page & Turnbull, $205M. |
| Port of SF, pier condition report (2017) | Pier 17 leased to the Exploratorium. |
| OSM way `25489458` | Shed footprint (6 nodes, 10,161 m²; OBB 232 × 43 m, bearing 54.9°; bay-end step measured). *Measured.* |
| OSM way `1390720126` (`man_made=pier`) | Deck footprint (13,024 m²; simplified to 5 true corners; front flare on the NW side). *Measured.* |
| DataSF LiDAR `ynuv-fyni` row `201006.0000005` (`mblr SF9900015`, 102,761 cells) | The full height solve (below). *Measured.* |

## Verified dimensions and location

- Shed OBB 232 × 43 m; deck 243 × 53–61 m. Long axis bearing **54.9°** true
  (front faces 234.9° — SW onto the Embarcadero at Green St).
- Anchor (model AABB centre, printed by the build): app (3466.88, −3561.04) =
  **lon −122.3981018, lat 37.8022149**.
- Height ladder above app water level (y = 0):
  - deck top **2.0 m** (NAVD88 deck 2.78 m / `p2010_zminn88ft` 9.1163 ft;
    2.0 m is the toy-scale seat, estimated)
  - shed eaves **11.0 m** (LiDAR `hgt_majoritycm` 10.46 m above deck)
  - ridge **14.0 m** (1st-return median 11.51 m + parapet logic, rounded)
  - facade gable apex **16.9 m** (`hgt_maxcm` 15.64 m ≈ `p2010_zmax`
    57.91 ft − deck = 14.87 m above deck)
  - flagpole tip **21.3 m** = `targetHeightM` (`peak_1st_m` 19.26 m above
    deck; the photo confirms a tall pole over the apex)
- The LiDAR is 2010 vintage; the shed envelope is preserved historic fabric,
  so the solve stands.

## Orientation

Authored in world axes (Blender +Y = north): the loader applies no rotation.
The shed frame used by the build script: s toward the bay at bearing 54.9°,
w toward the Valley (SE). The (s,w) → world map is a REFLECTION — every ring
goes through `ring_ccw()` after mapping, and outward normals come from the
winding, never from a centroid.

## Observations by side

- **SW front** (observed): everything in the Commons photo, translated at
  semantic scale — parapet gable to 16.9 m, sign plate at 13.1 m, roll-up
  12 m wide, barn doors 7.8 m with diagonal battens, window band + receiving
  door at the SE end, pole + pennant.
- **SE Valley side** (inferred): pilaster rhythm (16 bays), 7 glazed
  door-height bays in the middle third (renovation-era), high strip windows,
  3.5 m deck apron.
- **NW side** (inferred): plainest — pilasters, 3 service doors, apron
  flaring toward the front corner (measured flare in the deck ring).
- **NE bay end** (measured step + inferred detail): the NW two-thirds runs
  ~5.6 m further into the bay (OSM: SE third ends s≈114.05, NW strip
  s≈119.6); step block modelled at 12.2 m with a flat white roof carrying
  the RTU cluster; end door + the fog horn (barrel, throat, flared ink
  mouth) high on the gable face, pointing out to sea.
- **Roof** (observed): white membrane (`Toy_white`), weathered gray overlay
  plates on the front ~70 m of both slopes, ridge skylight strip (steel
  curb + opaque dark glass + glow plate) from s −80 to +60.

## Recognition cues (ranked)

1. A 232 m shed on its own pier deck pointing NE into the bay beside
   Pier 15's solar roof.
2. Cream bulkhead front: shallow full-width gable + "PIER 17" sign + apex
   flagpole.
3. The central door bay: olive roll-up between weathered timber barn doors.
4. Long white gable roof, weathered gray at the front, bright ridge line.
5. The stepped bay end with the fog horn.

## Preserved vs simplified

- Preserved: both real OSM rings, the measured bay-end step, the deck flare,
  the height ladder, the front composition, the roof value split.
- Simplified: pilaster count regularized to 16 bays; glazing counts on the
  long sides are typological; no Valley furniture, Fog Bridge, or campus
  neighbours; no piles (the dark deck fascia carries that read); lettering
  on the sign is not modelled (the diamond plate is the cue).

## Uncertainties

See REPORT.md corrections and `docs/asset-plans/pier-17.md` §2.15: the long
sides and bay end have no street-level imagery (typological); deck height
above app water is an estimate (cosmetic); "skylight" is an interpretation of
an observed bright ridge line; `peak_1st_m` read as the flagpole.

## Night state

Hero: the ridge skylight strip (`Toy_glass_Glow`). Supporting: the sign face
and the transom strip over the roll-up (`Toy_trim_Glow`), 3 of the 7 Valley
bays (`Toy_glass_Glow`). Every glow face is a thin plate proud of an opaque
surface; day colours match their non-glow neighbours.
