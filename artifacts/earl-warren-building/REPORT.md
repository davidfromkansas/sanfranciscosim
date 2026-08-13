# Earl Warren Building — build report

Deliverable: `earl-warren-building.glb`, a validated miniature of the Earl Warren
Building (350 McAllister Street, Bliss & Faville's 1922 California State Building,
home of the Supreme Court of California) for SF-SIM.

Built 13 August 2026 with Blender 5.2.0 LTS, headless, from the deterministic
script `build_earl_warren_building.py`. Research and sources: `REFERENCE.md`. This
report overrides `docs/asset-plans/earl-warren-building.md` wherever the two
disagree.

## Numbers

| | Authored (stage 2) | **Shipped (after stage 4)** |
|---|---|---|
| Objects / draw submeshes | 292 | **9** |
| Triangles | 18,540 | **18,540** (budget 22,000) |
| Vertices | 35,880 | **29,834** |
| File, raw | 1,030,636 B | **453,172 B** (−56.0%, 2.27x) |
| Dimensions | 118.9369 x 50.0250 x 27.000 m | **118.9369 x 50.0250 x 27.000 m** |
| Bbox min / max Z | 0.000 / 27.000 | **0.000 / 27.000** |
| XY centre offset | (0.000, 0.000) m | **(0.000, 0.000) m** |
| Loader scale (`targetHeightM / measuredHeight`) | 1.000 | **1.000** |
| Materials | 9, all `Toy_*` | **9, identical set** |
| Ray-flip fraction | 0.0 | **0.0** |

Footprint envelope: the 115.49 x 31.52 m surveyed OBB rotated 8.67 deg onto the
Civic Center grid gives 118.94 x 48.57 m; the entrance step block takes Y to 50.03.

## Corrections to the plan

The plan is a head start, not a citation, and three of its numbers were wrong.

### 1. The footprint is a comb, not a rectangle

Plan §2.8 assumed a 115.5 × 31.5 m rectangle and put two skylights on the roof
deck at x = ±31 m. The measured OSM polygon (way/260137839, 18 nodes, reprojected
into the street grid) is an **E-shaped comb**: a continuous 115.48 m bar along
McAllister about 21 m deep, three wings running north off it, two light courts
notched between them, and recessed corners at both north ends. Full table in
`REFERENCE.md`.

Consequences:
- the two "roof skylights" are the **two light courts**, at their measured spans
  (E 19.86–44.64 and E 70.95–96.73), glazed at z = 17.50 rather than sitting on the
  deck at 25.10;
- the north elevation is not one wall but seven segments;
- the south wall really is unbroken end to end, which is what lets the arcade be
  continuous — the plan guessed this correctly for the wrong reason.

### 2. The exclusion radius in plan §2.14 would have deleted a neighbour

Plan §2.14 flagged the risk and it is real. Measured from the anchor:
Earl Warren's own centroid is **2.34 m** away, the Hiram W. Johnson Building's
nearest ring vertex is **20.21 m** away, and the next neighbour is 86.45 m out. The
safe band is **3–20 m**, not the 59.9 m OBB half-diagonal most landmarks in the
registry use. **`exclude: 12`.** Full table in `REFERENCE.md`.

### 3. Bay geometry

Plan §2.8 specified 19 bays at 5.6 m pitch over an unstated span. Built as 19 bays
at **5.5579 m** pitch from E 4.60 to E 110.90, with the three entrance portals
centred on bays 8, 9 and 10 (E 46.27 / 51.83 / 57.39) so the portals line up under
the arcade above — which is what the plaza photograph shows and what the plan's
"centred at x = −4 m" was groping towards.

## Orientation

Authored with Blender **+Y = true north, +X = east**, then rotated **+8.67°** about
Z onto the Civic Center grid (long-axis bearing **81.33°**). The loader
(`placeGeneric` in `app/src/assets.js`) applies no rotation, so the model drops in
at its real-world heading. The ceremonial front faces **south** onto McAllister, so
here the contract's "front faces −Y" rule and AGENTS rule 5 agree — no deviation to
record.

## Height

`targetHeightM` **27.00 m**, the parapet crest, normalised exactly in the build so
the loader's `targetHeightM / measuredHeight` scale lands at 1.000. Roof plane at
25.10 m. The LiDAR `hgt_max` of 46.39 m was **rejected** — it is the 54 m Hiram W.
Johnson slab bleeding across a shared party wall. See `REFERENCE.md`.

## Night state

Two glow materials, both true to the building:

- `Toy_gold_Glow` — the three entrance arch soffits and the six bracket-lantern
  pucks. The hero glow, and the one thing genuinely lit on this facade at night.
- `Toy_white_Glow` — the twin courtroom laylights on the roof lantern. The only
  glow the app's aerial camera sees, and it tells you the courtrooms are below.

The 19 arcade windows stay dark on purpose: a 115 m wall of lit windows two blocks
from City Hall would out-shout the dome.

## Draft manifest entry

```json
{
  "id": "earl-warren-building",
  "file": "earl-warren-building.glb",
  "anchor": [-122.4178413, 37.7806865],
  "targetHeightM": 27.0,
  "cat": 18,
  "name": "Earl Warren Building",
  "estimated": false,
  "dims": [x, y, z],
  "tris": N,
  "loadRadius": 2500
}
```

`loadRadius` is the default rule `max(2500, 27.0 × 30)` = 2500.

## Iteration log

| # | Change | Why |
|---|---|---|
| 1 | first build from the plan, corrected to the measured comb footprint | plan §2.8 assumed a rectangle |
| 2 | roof deck recoloured `Toy_roofd` -> `Toy_steel`; mech boxes moved onto the wings | the deck read as one black lid and the dark mansard band was invisible against it |
| 3 | arcade heads made semicircular (half-width 2.00 m, springing 16.75, crown 18.75) | the first pass rose 3.25 m over a 1.90 m half-width, which reads gothic, not Beaux-Arts |
| 4 | portals rebuilt as three nested arches — pale `Toy_trim` surround, `Toy_glass` reveal, `Toy_gold_Glow` doors | the single gold arch panel read as one flat billboard |
| 5 | mansard band narrowed to 10.5 m deep, crown raised to 26.6 m | at 15 m deep the slope was too shallow to register from the app's camera |
| 6 | flagpoles dropped | at 0.26 m radius they are sub-pixel in the app and read as scratches across the arcade in review renders |
| 7 | **deck decomposition rebuilt, one slab per plan region; everything standing on the deck embedded 0.2 m into it; lantern cornice and laylight curbs restacked** | **a real defect: the deck slabs overlapped the south bar at both recessed corners, and the lantern cornice's top face was exactly coplanar with the lantern's own top. Coincident coplanar faces z-fight, and Cycles rendered the acne as solid black — black patches on the courtroom lantern and at both north corners of the roof.** |
</content>
