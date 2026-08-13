# Davies Symphony Hall — integration (stage 5)

Executed 12 August 2026 per `docs/asset-plans/INTEGRATION-PROMPT.md`, with the
`ADDRESS-TO-ASSET.md` stage-5 amendments. **Case B** — new landmark, no
procedural builder, no prior registry entry.

## What changed

| File | Change |
|---|---|
| `app/public/sf-assets/landmarks/davies-symphony-hall.glb` | new, 211,452 B — the stage-4 output, copied byte-for-byte and **not** re-exported or re-compressed (it is already meshopt-packed with the same `-c -km -kn -noq` flags `pipeline/compress-assets.mjs` uses) |
| `app/public/sf-assets/landmarks_manifest.json` | +19 lines, one entry appended |
| `pipeline/lib/landmarks.mjs` | +1 entry, `daviesSymphonyHall`, `exclude: 55` |
| `app/public/tiles/buildings/18_14.bin`, `toy/18_14.bin` | re-baked — the procedural footprint dropped |
| `app/public/tiles/ctx/*.json` (582 files), `context*.json`, `manifest.json`, `toy.json`, `api/_data/*` | re-baked — dropping one footprint renumbers the global building ids the pick lists reference |

Manifest entry as shipped:

```json
{
  "id": "davies-symphony-hall",
  "file": "davies-symphony-hall.glb",
  "anchor": [-122.420603, 37.7776227],
  "targetHeightM": 35,
  "cat": 17,
  "name": "Davies Symphony Hall",
  "estimated": false,
  "dims": [124.747, 95.0375, 35],
  "tris": 9518,
  "loadRadius": 2500
}
```

`loadRadius` is the default rule, `max(2500, 35 × 30) = 2500` m. `cat: 17`
matches `opera-house`, so the two Performing Arts Center halls behave the same
in search and for the concierge. `estimated: false` — both the cornice and the
crest are LiDAR measurements, not guesses.

## The exclusion radius

`exclude: 55` m, not the 62 m the plan first suggested. Half the 122.6 m
envelope is 61 m, but the block's south edge sits only ~40 m from the anchor and
Hayes Street is ~20 m wide, so a 62 m radius would have reached real buildings
on the far side — `excluded()` drops a footprint if its centroid **or any ring
vertex** falls inside. 55 m clears the Davies footprint (its centroid is ~5 m
from the anchor) and leaves the Hayes and Grove frontages alone.

Confirmed by `node pipeline/audit.mjs` check **1.6 — "no procedural footprint
inside a bespoke landmark exclusion zone": PASS, 29 landmarks clear**, and by
the re-bake diff: the only geometric changes in the whole city are
`buildings/18_14.bin` (−286 B) and `toy/18_14.bin`. One cell, one building.

## Local QA

Run against `npm run dev` in this worktree, in a real foregrounded Chrome.

| Item | Result |
|---|---|
| Re-validation of the shipping GLB | **PASS** — `validation.json`, `overall: PASS`, 9,518 tris, 35.000 m |
| Manifest entry served and parsed | **PASS** — loader reports `entries: 23`, `failed: 0` |
| GLB served | **PASS** — 200, `model/gltf-binary`, 211,452 B |
| Single building, no duplicate | **PASS** — exactly one batch instance at (1487, −843) |
| **Scale factor** | **PASS — exactly `uniform x1.0000`**, the loader's `targetHeightM / measuredHeight` landing on 1 as designed |
| Orientation | **PASS** — arc faces north-east at City Hall, `yawDeg` absent (the loader applies no rotation and none is needed) |
| Terrain seating | **PASS** — placed at y = 18.50 m, against DataSF's measured mean ground of 18.91 m NAVD88 for this footprint; no float, no sink |
| Position vs. the Opera House | **PASS** — 112.9 m apart across Grove Street, Opera House at y = 20.55 m |
| Night glow | **PASS** — at `night 1.00` the two promenade levels burn warm behind the fin rhythm, the clerestory band glows, the gold fascia is picked out; shell roof and back-of-house stay dark |
| Search + card | **PASS** — "Davies" resolves to `Davies Symphony Hall · LANDMARK`, card reads "Landmark / Hayes Valley", highlight ring lands on the block |
| **Draw calls** | **PASS — 105** scene draw calls with 22 landmarks live (budget < 300). Davies costs **zero** additional calls: it goes into the shared landmark `BatchedMesh` pair |
| Fallback drill | **PASS** — see below |
| `npm run lint` | **PASS** — clean |
| `npm run build` | **PASS** — built, 3,314 tiles compressed 56.0 → 31.5 MB |

### Fallback drill

Renamed `davies-symphony-hall.glb` away and reloaded:

- exactly **one** console warning:
  `sf-assets: davies-symphony-hall failed to load (Unexpected token '<', "<!doctype "... is not valid JSON)`
- `failed: 1`, every other landmark unaffected — no crash, no black hole, no
  terrain gap
- the site shows **empty ground inside the exclusion zone**, which is the
  documented Case-B expectation (there is no procedural builder to fall back to)
- search, the landmark card and the highlight ring all still work
- restoring the file byte-for-byte brings the building straight back

### One environment caveat, reported honestly

The landmark's dither cross-fade needs continuous rendered frames, and the
automation repeatedly backgrounds the tab, which pauses `requestAnimationFrame`
(a limit the repo's own `.agents/skills/testing-sf-3d/SKILL.md` documents). So
several intermediate captures show the building part-way through its fade — a
hatched, semi-transparent read. Left foregrounded, it settles fully; the clean
day and night captures were taken that way. This is the harness, not the asset.

Separately, the in-app stats overlay reports `draw calls 1`: `renderer.info` is
reset by the post-processing pass, so the overlay ends up measuring its
fullscreen quad. The 105 figure above is the scene render, measured directly.

## Not done here

Push, PR and deployed production QA were explicitly requested by David for this
session, so the stage-5 stop is lifted — but production QA on
https://sf-3d.vercel.app can only run after the PR merges and Vercel deploys.
