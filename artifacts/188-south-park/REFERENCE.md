# 188 South Park — reference dossier

## Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way/124884339 | Footprint rectangle (5 nodes, 4 real corners), no height tag |
| DataSF Building Footprints (ynuv-fyni) SF3775125 | LiDAR footprint polygon, hgt_maxcm=1593 (15.93 m), hgt_mediancm=1334 (13.34 m), hgt_mincm=635 (6.35 m), gnd_min_m=6.03 |
| DataSF Parcels (acdm-wktn) 3775-132 | Through-lot: 188 South Park (SE) / 549 3rd St (NW), zoning CMUO, parcel added 2001-12-26 |
| SF Building Permit 9823199S (filed 1998-11-10, issued 1999-10-20) | "Erect a four story twelve unit live work bldg", wood frame (5), $1.2M estimated / $1.4M revised |
| SF Building Permit 200503097121 (2005) | Interior alterations, 4 storeys, 12 units, apartments |
| SF Building Permit 201807174708 (2018) | Kitchen remodel, **5 storeys** (see open questions), 12 units |
| Prism Capital portfolio page | 12-unit high-end live/work loft on former gas station site, Superfund cleanup, sold $800K–$1.2M |
| Curbed SF (7 Sep 2010) | Penthouse loft with private rooftop terrace, designed by Santos-Prescott |
| Compass listing (Unit 6) | Architect Adele Santos, 16+ ft floor-to-ceiling windows, stone/stucco construction, private entrance from 3rd St, wind-protected patio, 12 units built 2002 |
| South Park Lofts HOA (CA SOS filing 2354555) | HOA filed 10 Aug 2001, address 188 South Park Lofts HOA |
| LoopNet property page | APN 3775-132, mixed-use, 0.16 AC, Rincon/South Beach |
| Bing Maps satellite (Vexcel 2026) | Roof form: flat with penthouse/roof terrace element |

## Verified dimensions and location

- **Footprint:** 23.7 m (wide, NE–SW) x 16.1 m (deep, NW–SE), 381 m², rectangle at bearing 45°/225°
  - Measured from OSM way/124884339 OBB
  - DataSF LiDAR footprint width agrees (23.8 m); depth overestimated (28.1 m) due to 42-vertex LiDAR edge jitter
  - Parcel is 27.4 x 23.1 m (634 m²); building fills lot width but only 16.1 m of 27.6 m depth (remaining ~11.5 m = patio)
- **WGS84 anchor:** -122.3950794, 37.7810118 (DataSF LiDAR footprint area centroid)
  - Chosen over OSM OBB center because it opens the widest exclusion window (see REPORT.md)
- **Target height:** 15.93 m (LiDAR hgt_maxcm = 1593 cm) — the penthouse/roof terrace parapet
- **Main roof:** ~13.3 m (LiDAR median 13.34 m)
- **Ground elevation:** 6.03 m NAVD88 (handled by app terrain, not the asset)

## Orientation

- Building sits on the north rim of the South Park oval
- South Park front faces **SE, bearing 134.8°** (the address elevation)
- 3rd St / patio rear faces **NW, bearing 314.8°** (service end)
- SW flank faces **224.8°** (toward the park oval — most exposed)
- NE flank faces **44.8°** (toward 166-168 South Park neighbour)
- Long axis runs NE-SW at bearing 45°/225°

## Observations from all four sides and above

### Top (observed from LiDAR + Bing aerial)
- Flat roof at ~13.3 m with a penthouse/roof terrace reaching 15.93 m
- Penthouse positioned on the SE third (overlooking South Park) — inferred from the Curbed article's "private rooftop terrace"
- LiDAR min of 6.35 m suggests a lower element (canopy, awning, or step) — unexplained

### Southeast (South Park front) — INFERRED
- 16.1 m wide, ~15.9 m tall — distinctly vertical
- Ground-floor commercial storefront (State Farm office per geocode)
- Three loft levels of tall floor-to-ceiling windows (16+ ft per listing)
- 4 bays per floor inferred from 23.7 m width / plausible bay width

### Northwest (3rd St / patio rear) — INFERRED
- Service end with garage door, residential entries
- At least one unit has a private entrance from 3rd St (Compass listing)
- Patio/courtyard between this face and 3rd Street

### Southwest flank — INFERRED
- 23.7 m long, four storeys — the longer of the two flanks
- Faces the open South Park oval — most exposed elevation
- Same tall window rhythm as the other faces

### Northeast flank — INFERRED
- 23.7 m long, four storeys
- Faces 166-168 South Park (~10.4 m tall neighbour)
- Same window rhythm, perhaps less glazing

## Recognition cues (ranked)

1. The penthouse/roof terrace — lifts crest to 15.93 m, ~2.6 m above main roof
2. Four storeys with tall windows — ~4 m proud of neighbours
3. The through-lot position on the north rim of the oval
4. Contemporary stucco-and-stone facade (2002)
5. Ground-floor commercial base with glazed shopfront

## Features to preserve

- 23.7 x 16.1 m footprint and real 45°/225° heading
- Four-storey height standing proud of neighbours
- Tall window grid as a rhythm
- Penthouse/roof terrace — aerial signature
- Two-different-ends: commercial front on park, residential/patio rear

## Features to simplify

- Window count → 4 identical bays per face per floor
- 16+ ft windows → single tall recessed opening per bay
- Storefront → one wide glazed opening
- Roof clutter → small composed set: penthouse, railing, 2-3 HVAC units

## Uncertainties and conflicting evidence

- **Facade material/colour:** permit says "stone, stucco"; architect is Santos-Prescott; no street-level photos available — palette is inferred
- **Window rhythm:** 4-bay reading is inferred from width / plausible bay width
- **Penthouse position:** inferred from Curbed article's "private rooftop terrace" — placed on SE third overlooking park
- **LiDAR min 6.35 m:** unexplained — could be canopy, awning, or building step
- **5 storeys vs 4:** 2018 permit says 5, all others say 4 — LiDAR supports 4 + penthouse
- **No street-level imagery was available** — all four elevations are inferred from permit record, listing copy, and architect's known work
