# DEVIN PROMPT — Integrate Building Kit v2 (207 pieces) into the SF diorama

You are integrating the full building kit into sanfranciscosim. The GLBs and index are already committed at `app/public/sf-assets/kit/` (207 `.glb` + `kit_index.json`). This builds on the Golden Gate Bridge pilot (see PILOT-ASSET-PROMPT.md) and replaces procedural buildings with kit instances wherever a piece fits. Read AGENTS.md first. Do not modify any GLB.

## 1. What the kit is

207 hand-authored toy-diorama buildings in 9 residential typologies + commercial/office/civic/tower/industrial families, all sharing one visual language (flat colors, subtle bevels, dark blue-gray windows, designed roofs). Piece families by id prefix:

| Prefix | Family | Count | Where it belongs |
|---|---|---|---|
| `sunset_` | Doelger stucco rowhouse (garage + stair + bay, 3 parapet shapes, `_m` = mirrored) | 24 | Sunset, Parkside, Outer Richmond — the dominant residential fill west of Twin Peaks |
| `rich_` | Richmond special (full-width bay band over double garage) | 9 | Richmond, Inner Richmond, Ingleside |
| `ital_` | Italianate Victorian (false front, bracketed cornice, slant bay, high stoop) | 9 | Alamo Sq, Western Addition, Haight, Mission Dolores, Noe |
| `stick_` | Stick/Eastlake (squared bay, front gable w/ sunburst) | 6 | same Victorian belt as `ital_` |
| `qa_` | Queen Anne (corner turret + cone) | 5 | Victorian belt; prefer street corners for `turret`/`wrap` variants |
| `edw_` | Edwardian flat stack (curved bay, doors side-by-side) | 6 | citywide infill: NoPa, Inner Richmond/Sunset, Mission, Castro |
| `marina_` | Marina style (arch entry + faceted bay over garage, tile hip) | 6 | Marina, Cow Hollow |
| `aptfe_` | Fire-escape apartment (full-height bays, zigzag escape; `corner_` = storefront) | 7 | Tenderloin, Nob/Russian Hill, Chinatown, Polk, Mission corridors |
| `liquor_corner*` | Chamfered-corner shop + housing | 3 | corners in residential grids |
| `apt_` | Bay/punched apartments (+`senior_home`, `dorm_slab`) | 20 | denser residential streets citywide |
| `mixed_`, `shop_`, `corner_`, + named shops (`taqueria`, `bakery`, `diner`, `laundromat`, `dispensary`) | storefront commercial | 25 | neighborhood commercial strips (Clement, Irving, Valencia, Castro, Polk, Columbus, Fillmore…) |
| `office_` | SF offices: `punched`=pre-war masonry, `grid`=deco pier-and-spandrel, `ribbon`=curtain wall on plaza | 18 | FiDi + Market St corridor + SoMa |
| `tower_` | Skyline towers (grid/slat/deco/slab/setback, h60–240) | 22 | downtown core, by height field |
| `church_`, `firehouse_`, `school_`, `library`… | civic set | 24 | at their real POI locations where known, else zoned |
| `warehouse_`, `factory`, `piershed`… + `gas`, `motel`, `market_`, `parking_` | industrial/special | 16 | SoMa, Dogpatch, Bayview, waterfront |

## 2. kit_index.json format (CHANGED from v1 — object, not array)

```json
{ "version": 2, "note": "...", "pieces": [ {"id","file","kind","cat","w?","h?","dims":[x,y,z],"tris"} ], "renames_v2": { "old_v1_id": "new_v2_id" } }
```

- **`renames_v2` is load-bearing.** 67 v1 residential ids no longer exist as files. Resolve every id lookup through `renames_v2` first (e.g. `house_w9_hip_b1 → marina_w9_hip`, `apt_w16_f6_fe → aptfe_w16_f6`) so any existing assignment keys keep working.
- `dims` = world-size in meters `[width(x), depth(y), height(z)]`. `w` on residential = lot-width class (7≈7.6 m, 9, 11).

## 3. Asset contract (same as landmarks)

- Meters, real scale. Origin = base-center at z=0. **Front faces −Y**; +Y is the lot's rear.
- Flat vertex-less colors via `Toy_*` materials, no textures. Merge each piece's meshes at load and render via instancing (see §6).
- **`Toy_body` is the ONLY tintable material.** Everything else (trim, glass, roofs, doors, awnings) is fixed palette — never tint those.

## 4. Placement rules

1. **Typology→zone mapping** per the table in §1. Use the existing neighborhood polygons/zoning you built for the context layer; when a lot is in none of the mapped zones, fall back on: residential lot → `edw_`/`apt_`; commercial frontage → `shop_`/`mixed_`.
2. **Lot fitting:** pick the widest piece whose `dims[0]` ≤ lot frontage (widths cluster at 7.6/9/11 m for houses). Target ≥70% of building footprints kit-filled; keep the procedural TOY2 extrusion as fallback for the rest — kit pieces and procedural buildings must coexist.
3. **Rows must abut.** SF rows are contiguous: place row pieces edge-to-edge (gap ≤ 0.2 m). Alternate sub-variants and use `sunset_*_m` mirrors so garages/stairs create rhythm, never the same piece twice adjacent.
4. **Depth:** you may stretch depth (Y) up to +20% to reach mid-block. NEVER scale width or height — trim and floor heights break.
5. **Orientation:** rotate so −Y faces the fronting street. Corner pieces (`qa_*_turret`, `liquor_corner*`, `corner_*`, `aptfe_corner_*`) go on intersections with the turret/chamfer pointing at the crossing (chamfer face bisects the corner angle).
6. **Landmarks win.** Existing landmark exclusion zones (landmarks_manifest) suppress kit placement; never place a kit piece inside one.
7. Civic pieces: place at real POIs where the context layer knows them (firehouses, schools, libraries, churches); at most one per few blocks otherwise.

## 5. Tinting

- Per-instance color multiply on `Toy_body` only (instanceColor). Palette (pick deterministically by lot hash so reloads are stable):
  `#e8d9a8 #a8c4d4 #d4b0c0 #c9d4c0 #e6d0b8 #b8d4cc #d8c8b0 #cfc3de #e2b8a8 #dcd3c4` + plain `#ffffff` (no tint) at ~20% weight.
- Victorians/Sunset rows lean saturated-pastel (SF painted rows are the identity); offices/civic/industrial mostly `#ffffff`–warm-white range so downtown reads calm (style bible: neutral base + saturated accents).
- Adjacent lots must differ in tint.

## 6. Performance (budgets: <300 draw calls, 60 fps, unchanged)

- One merged geometry per (piece × material-bucket): bucket A = `Toy_body` (tintable), bucket B = everything else merged. ⇒ ≤2 draw calls per piece TYPE via `InstancedMesh`, not per instance.
- Only instantiate piece types actually used in loaded tiles; keep instanced draws tile-friendly with your 500 m cell system.
- Kit tris: avg 838, houses ≤1.04k, apartments ≤1.34k, offices ≤3.1k, towers ≤10.3k (towers are few and downtown-only).
- Night mode: treat `Toy_glass` (and `Toy_glassl` on shopfronts) as the window-emissive surface using the same warm-amber night treatment as procedural windows; do NOT make doors/awnings/roofs glow.

## 7. Acceptance gates (screenshot each, diorama camera 42°)

1. **Alamo test:** a Victorian block (ital/stick/qa/edw mix) next to `sf-3d-assets` reference render `hv2_row_alamo.png` — must read as the same world.
2. **Sunset test:** ≥6 contiguous blocks of `sunset_`/`rich_` rows with mirrors + tint variety, aerial: pastel grid like the real Sunset.
3. **Commercial strip test:** Clement or Irving: `shop_`/`mixed_`/`corner_` with awnings facing the street, no floating pieces.
4. **Downtown test:** FiDi with `office_` mid-rises ringing `tower_` core; pre-war/deco/curtain-wall mix visible.
5. **Contract checks:** no piece scaled in X/Z; fronts face streets; corners chamfer to intersections; landmark zones clean; renames_v2 resolves with zero missing-file errors.
6. **Perf:** draw calls <300 and 60 fps at diorama camera over the densest downtown tile; report numbers.
7. Day + night screenshot pair of the same block showing window glow on kit pieces.

Deliver: the integration PR + the 7 screenshots + a one-paragraph summary of fit rate (% footprints kit-filled) per neighborhood.
