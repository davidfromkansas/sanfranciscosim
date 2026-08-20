# Pier 19 — reference dossier

Compiled 19 August 2026 for the SF-SIM miniature build. Everything below was
re-verified this session; the plan (`docs/asset-plans/pier-19.md`) is the fuller
document and its §2.1/2.2 carry the source-by-source table.

## Sources and what each establishes

1. **NRHP, Port of San Francisco Embarcadero Historic District, Section 7
   (Jan 2006), pp. 122–125**
   (`sfport.com/files/2022-12/EmbarcaderoRegisterNominationSec7.pdf`) — the
   authoritative architectural description. Establishes: built 1936–38 (bulkhead
   wharf substructure 1922); near-identical twin of Pier 9 ("identical in design
   and dimensions … 153 feet in width and 800 feet in length", BSHC [1938]:51);
   steel-frame transit shed with scored precast concrete walls, three interior
   aisles, **continuous monitor along the full length**, steel-sash windows
   (south-wall ones plated over), roll-up doors in all three shed walls; rear
   elevation "faintly Art Deco" with six profiled pilasters rising just above
   the roofline and a gabled central bay; stucco bulkhead building with broad
   central pavilion, monumental arched entry (steel roll-up door), monumental
   flanking piers, gabled parapet, "PIER 19" in raised metal letters, flagpole;
   pedestrian doors flanking the arch, cast-iron wheel guards; 1961 connector
   shed to Pier 23 (non-contributing) removed 80 ft of the shed's north wall
   and obscured the bulkhead building's north elevation. Contributing Resource.
2. **Wikimedia Commons, Category "Pier 19 (San Francisco)"** — the 2012 frontal
   photo (`Pier 19, San Francisco.JPG`): pale warm-grey stucco, banded
   monumental piers, semicircular arch with dark roll-up, "PIER·19" dark
   letters on the attic, gabled parapet with cap, white flag on the flagpole,
   tall dark steel-sash window bays in the wings. The June 2017 Coit Tower
   aerial: both sheds + connector roof massing, monitor lines, apron widths.
3. **Google satellite imagery (current, z19)** — roof state now: pale grey with
   buff weathering on Pier 19, continuous centerline monitor, pale side aprons,
   vessel moored at the south apron, deteriorated strip along the north apron,
   flat pale connector roof shoreward.
4. **DataSF `ynuv-fyni` LiDAR footprints, `sf16_bldgid 201006.0000010`
   (`mblr SF9900019H`)** — a single merged ring for Pier 19 shed + Pier 23 shed +
   connector (21,598 m²). Heights over the merged ring: ground (deck) median
   2.03 m; roof majority 10.96 m / median 10.14 m above deck; max 17.51 m and
   first-return peak 20.45 m — **the max/peak pair is the flagpole**, not the
   masonry crest (they differ 0.9 m at one point; classic pole signature).
5. **OSM** — way 91913152 (the same merged three-structure building, h=10);
   node 1436065856 (Pier 23 Cafe) fixing the north end of the frontage; ways
   25489458/1390720126 (Pier 17) fixing the southern neighbour.
6. **Port of SF documents** — 2024 marketing flyer + May 2025 availability
   report (storage/shed space, "Pier 19 Shed" and "Pier 19 Bulkhead/Shed");
   berthing schedules (Hornblower layberth, "Pier 19 South"); facility
   assessment (north apron dry-rot, reconstruction tied to Pier 27 project);
   2013 Finger Pier Exiting Guidelines (Pier 19 is the "pier fully built-out
   without parking" model case).

## Verified dimensions and location

- Pier: **153 ft × 800 ft (46.63 × 243.84 m)**, plus the 60 ft (18.29 m)
  bulkhead wharf at the street — model deck 46.63 × 262.13 m.
- Transit shed: **34.3 × 194.9 m measured** from the merged ring's south
  finger; its shore end sits 57.6 m from the street frontage (the 1961 flat
  extension fills that strip today); its rear sits 9.6 m short of the pier
  head (the open head apron).
- Long axis bearing **54.89°**; frontage bearing 324.19° (square within 1°).
- Anchor (model bbox centre after recentring): **-122.3988181, 37.8030032**.
- Heights above water: deck 2.0; shed eave 11.8; roof planes to 13.0; monitor
  top 14.8; wing parapet 11.5; arch crown ~12; **gable crest 17.0 (bbox top)**;
  flagpole 19.5–20.4 (excluded from the model).
- Model origin: deck top (pier-1 convention — the app's DEM carries the
  Embarcadero piers as low ridges); pile stubs to −2.2; vertical extent
  **17.2 m = targetHeightM**.

## Observations by side

- **SW (Embarcadero facade)**: the identity view. Pavilion with monumental
  arch, banded flanking piers, "PIER 19", gabled parapet; wings with tall
  steel-sash bays over a low plinth; everything pale warm stucco; dark sashes.
- **SE (south flank, Pier 17 slip)**: the working side. Scored panel rhythm,
  roll-up doors, high strip windows mostly plated (steel), narrow apron with
  lamp standards, mooring bitts and fender piles; Hornblower layberth.
- **NW (north flank, Pier 23 slip)**: same rhythm with glazed strips; in
  reality hidden shoreward by the 1961 connector and fronted by a closed,
  deteriorated apron — modeled finished and plain, no furniture.
- **NE (bay end)**: six profiled pilasters to small peaks above the eave,
  gabled centre bay echoing the roof, one roll-up, head apron with bitts.
- **Above (the app's view)**: the long pale roof with its full-length monitor
  is the primary read; the flat lower extension roof breaks the run at the
  shore end; gable + wing copes mark the street end.

## Recognition cues (ranked)

1. Gabled bulkhead pavilion + monumental arch + "PIER 19"
2. Continuous full-length roof monitor
3. Plain long shed between Pier 17 and Pier 23 (the modest one of the row)
4. Fendered pile deck, narrow aprons, open head apron
5. Art Deco pilaster peaks on the bay end

## Preserved / simplified / omitted

- Preserved: all five cues; deck-on-piles massing; plated south windows;
  scattered night lighting.
- Simplified: scored panels → pilaster rhythm + bevels; roll-up doors → steel
  panels with seam bars; letters → extruded blocky navy glyphs; monitor
  clerestory → continuous glassl band with proud glow quads on lit bays.
- Omitted deliberately: the flagpole (LiDAR-max trap — a hairline bbox top
  would rescale the pier); the 1961 connector and Pier 23 (out of scope,
  future `pier-23` asset); moored vessels (live-vessel layer's job); rail
  spurs (flush, invisible at scale); the Embarcadero streetscape.

## Uncertainties

- Gable crest 17.0 m is *inferred* (LiDAR max region minus flagpole, photo
  proportions) ±1 m.
- Monitor rise (14.8 m) proportioned from photos; LiDAR majority covers the
  roof field, not the monitor top.
- Wing parapet 11.5 m inferred from the 2012 photo against the crest.
