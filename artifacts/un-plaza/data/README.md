# un-plaza measured data

| File | What it is |
|---|---|
| `osm_raw.json` | raw Overpass pull, bbox 37.7793–37.7810 / −122.4153–−122.4125, all nodes and ways with geometry. The plaza is relation `1735771`, outer way `24588033`. |
| `frame.json` | the plaza frame: `E_BRG` 80.94, `N_BRG` 350.94, the world-metre centre, and the 39-vertex ring in `(e, n)`. |
| `elements_en.json` | every measured element in `(e, n)` metres — ring, fountain, three planting beds, south terrace, dog run, UN emblem, the 16 light standards, and the point features. This is the file the build script must read. |

`trees_en.json` does **not** exist yet: the plaza's trees are not in OSM and must be
digitised from the aerial during stage 2 (see the plan's Part 1).

Reference imagery (Google/Esri z20 mosaics and the annotated plaza-frame zooms used to
derive the layout) is deliberately **not committed** — it is copyrighted. It was written
to the session scratchpad at `un-plaza-imagery/`; regenerate it with the tile fetch
described in `docs/asset-plans/un-plaza.md` §2.2 if needed.
