# FERRY-LIVE-PROMPT.md — Live SF Bay Ferry vessels from real-time data

Integration task spec for this repo. Read `AGENTS.md` first, then this file top to bottom before writing any code. When done, deploy and report per the QA section. Do not improvise beyond this spec; where the spec says STOP, stop and ask David.

## Mission

Replace the two fake looping ferries with the **real San Francisco Bay Ferry fleet**: every WETA vessel currently underway on the Bay appears in the scene as the hand-made ferry GLB, at its real position, moving and turning the way the real boat is moving right now. Watching the app should feel like a live tabletop view of the Bay. When live data is unavailable (no key, API down, dev without network), the existing procedural ferries keep sailing — rule 3 in `AGENTS.md` (procedural fallback is a guarantee) applies to this feature exactly.

Data source: 511 SF Bay Open Data — SIRI **VehicleMonitoring** endpoint for agency **`SB`** (San Francisco Bay Ferry / WETA). JSON, free API key. Details and the VERIFIED live response shape are in Appendix A. ⚠️ The agency code is `SB` — `SF` is Muni and `GF` is Golden Gate Ferry; using the wrong one gives you 600+ buses instead of 16 boats.

## Preflight gates (check before anything else)

1. **The model exists at `app/public/sf-assets/vehicles/SF_Bay_Ferry.glb`** (merged in PR #15; 2.4 MB). Verified measurements: 1 mesh, **27,224 tris**, dims W 11.94 × H 14.70 × L 41.70 m, bbox y −1.89 … +12.81.
2. Run the intake checklist from `.agents/skills/sf-asset-check/SKILL.md`. **Known conform items, found in advance — fix all three, they are not optional:**
   - Materials are named `Ferry_*` (Livery, DeckGrey, Steel, Glass, AlumDull, PaintWhite, Red, Green, DarkGrey, Orange, Rubber, Teak). The loader convention is `Toy_*` — rename each to `Toy_Ferry*` equivalents during conform.
   - **The file contains 2 textures.** The contract is flat-color materials only; the loader bakes material base colors to vertex colors, so textured surfaces will silently lose their look. Bake or replace the textured materials with flat colors (per the skill's conform workflow), then strip the textures from the export.
   - Confirm the front axis in Blender per the skill (bbox is Z-symmetric so it can't be read from the file listing). The manifest `front` field you write must match reality; the fleet convention is −Z.
   - Hull geometry below y=0 (draft −1.89 m) is CORRECT for a vessel and stays — the water plane hides it. Do not re-zero the mins like a road vehicle.
3. Add a manifest entry (see Part 3) — the loader scales by manifest dims, never by trusting the file.
4. Confirm `FERRY_511_KEY` handling is OPTIONAL end to end (iron rule 4: zero required keys). The build, dev server, and deploy must all work with no key present.

## Architecture (three parts)

```
511 SIRI VehicleMonitoring (JSON, 60 req/hr limit)
        │  polled by
        ▼
api/ferries.mjs        zero-dep Vercel function; caches; normalizes; CDN-cached response
        │  GET /api/ferries every ~60 s
        ▼
app/src/ferries.js     loads GLB once → InstancedMesh; interpolates vessels between polls
        │  hides
        ▼
agents.js procedural ferries   (visible again the moment live data goes away)
```

## Part 1 — Server: `api/ferries.mjs`

New file, **zero npm dependencies** (match the style of `api/agent.mjs`). Runtime behavior:

1. Read `process.env.FERRY_511_KEY`. If unset/empty → respond `200` with `{ "live": false, "reason": "no-key", "vessels": [] }`. Never throw, never 500 for a missing key. **The key is ALREADY provisioned in the Vercel project env (Production, Preview, Development)** — do not add it, do not print it; for local testing run `vercel env pull`.
2. Fetch `https://api.511.org/transit/VehicleMonitoring?api_key=${KEY}&agency=SB&format=json` with a 10 s timeout (`AbortController`). Node's `fetch` transparently handles the gzip encoding 511 always sends; if you test with `curl`, you must pass `--compressed`.
3. **Strip a UTF-8 BOM defensively before parsing** — some 511 endpoints prefix one (the verified SB response did not, but 511's own docs warn about it): `JSON.parse(text.replace(/^﻿/, ''))`.
4. Normalize to this exact shape (field names verbatim — the client depends on them):

```json
{
  "live": true,
  "fetchedAt": 1786300000000,
  "vessels": [
    {
      "id": "SB:Dorado",
      "label": "Dorado",
      "lat": 37.7961,
      "lon": -122.3906,
      "bearingDeg": 219.0,
      "routeName": "Richmond",
      "destination": "San Francisco Ferry Building Gate E",
      "inService": true,
      "recordedAt": 1786299985000
    }
  ]
}
```

Mapping from SIRI (verified live shape in Appendix A): one entry per `VehicleActivity`; `id` = `"SB:" + VehicleRef`; `label` = `VehicleRef` (it IS the vessel name — "Dorado", "Karl", "Hydrus"...); `bearingDeg` = `Bearing` (absent on many docked vessels — omit the field then, do NOT invent 0); `routeName` = `PublishedLineName` or `LineRef`; `destination` = `DestinationName` (may be null); `inService` = `LineRef != null`; `recordedAt` = `RecordedAtTime` parsed to epoch ms. Drop entries with no `VehicleLocation`. Drop entries whose `recordedAt` is older than 10 minutes. Return ALL remaining vessels including out-of-service ones — the client decides what to show.

5. **Rate-limit protection, in this order:**
   - Response header `Cache-Control: s-maxage=60, stale-while-revalidate=300` — Vercel's CDN then serves all clients from one fetch per minute. This is the primary mechanism.
   - Module-scope memo as second layer: if the last upstream fetch was < 55 s ago, return the memoized result without calling 511.
   - On upstream 429 or 5xx: return the memoized data with `"live": true, "stale": true` if you have it (≤ 10 min old), else `{ "live": false, "reason": "upstream" }`, and back off (don't retry upstream for 5 min).
6. Register the function in `vercel.json` `functions` only if it needs non-default settings; default limits are fine (it does a single small fetch).
7. `FERRY_511_KEY` is already set on the Vercel project (all three targets) — nothing to provision. Never log it, never commit it, never echo it into build output.

## Part 2 — Client: `app/src/ferries.js`

New module `createLiveFerries(scene, data)`, wired in `main.js` right after `createAgents(...)`. It owns: fetching, the GLB fleet mesh, and per-frame animation. Follow these rules exactly.

### Loading the model
- Load `sf-assets/vehicles/SF_Bay_Ferry.glb` with the same GLTFLoader + merge approach the fleet/landmark loader uses (bake material colors → vertex colors, ONE `MeshLambertMaterial({vertexColors:true})` + one glow set if `*_Glow` materials exist). Target: **≤ 2 draw calls for the entire live fleet** (one `InstancedMesh` body + optionally one glow), plus one wake mesh.
- Capacity 24 instances (WETA operates ~16 vessels; headroom is cheap). `instanceMatrix.setUsage(DynamicDrawUsage)`, `frustumCulled = false`, `count` = active vessel count each frame.
- Scale: `targetLengthM / measuredLength` from the new manifest entry. Orientation: manifest `front` is −Z; boats must sail nose-first.
- If the GLB fails to load → console.warn once, do nothing else (procedural ferries stay visible). Never crash (iron rule 3).

### Polling
- `fetch('/api/ferries')` on start, then every 60 s + random 0–5 s jitter. Pause polling when `document.hidden`; poll immediately on visibility regain.
- Response `live: false` or fetch error → enter/remain in fallback state (below). `live: true` → update the vessel table.
- In local Vite dev there is no `/api` — a failed fetch is the expected fallback path and must be silent after one warn. For end-to-end testing use `vercel dev`, or the demo mode below.

### Position, projection, movement
- Project with `data.project(lon, lat)` — the ONE projection function (see `AGENTS.md` conventions). Never re-derive the math. Boats sit at **y = 0** (water level) plus the same gentle bob the procedural ships use (copy the bob idiom from `agents.js`, don't invent a new one).
- **Never teleport a visible boat.** Keep per-vessel state `{ current: Vector3, heading: number, target: Vector3, targetHeading, lastFixAt }`. Between polls, dead-reckon: advance `current` toward/past `target` along `heading` at implied speed (distance between the last two fixes / time between them, clamped to 0–13 m/s — WETA boats top out ~34 kn). When a new fix arrives, ease the correction in over 2–3 s (lerp position, shortest-arc lerp heading) instead of snapping.
- Heading: use `bearingDeg` when present — convert compass bearing (0° = north, clockwise) to scene yaw knowing +x = east, −z = north; **write the conversion once, with a comment showing the two test cases** (north-bound boat faces −z; east-bound faces +x). When `bearingDeg` is absent, derive heading from the movement vector between fixes; keep the previous heading when nearly stationary (docked boats must not spin).
- **Which vessels to show ("operational"):** render a vessel if `inService` is true OR it has moved > 100 m between consecutive polls (covers boats repositioning without a trip assignment, like *Pyxis* crossing the Bay off-schedule). Do NOT render stationary out-of-service vessels — WETA's laid-up boats cluster at the Alameda maintenance basin (≈ 37.771, −122.300) and rendering that raft of parked ferries looks like a bug.
- A vessel not present in two consecutive responses, or with `recordedAt` older than 10 min → remove it (shrink `count`, swap-with-last like the instancing code elsewhere in the repo).
- Cull vessels whose projected position falls outside the water actually present in the scene: check the water extent in `app/src/water.js` and clamp to it (Vallejo-bound boats sail far north of the modeled Bay; they should sail off-scene and be culled, not float over void). State the extent you found in a code comment.
- Wake: reuse the exact wake technique from `agents.js` ships (stretched translucent quad per hull, `renderOrder` 3), one instanced wake mesh for the live fleet, length scaled by current speed.

### Fallback + procedural handoff
- Export from `agents.js` a small setter — `setProceduralFerriesVisible(visible)` — that toggles `mesh.visible` and `wake.visible` for ship entries with `route.kind === 'ferry'` ONLY (sail + container traffic always stays). Do not restructure `agents.js` beyond adding this.
- `ferries.js` calls it: live data flowing → `false`; fallback state (no key, no vessels for > 5 min, fetch failures) → `true`. The swap must be seamless and repeatable in both directions in one session.
- **The bar:** at no moment may the Bay show zero ferries when the app is healthy, and at no moment may it show BOTH a live vessel and a procedural ferry ghosting through it.

### Demo mode (required, for testing without a key)
`?ferries=demo`: skip the network and feed the module a scripted set of 3 synthetic vessels running plausible loops (Ferry Building ↔ Oakland, ↔ Alameda Seaplane, ↔ Vallejo heading off-scene north — real terminal coords are in Appendix B) with fixes emitted every 20 s, including one vessel that goes stale and disappears, and a bearing-less vessel. This exercises interpolation, heading derivation, removal, and culling deterministically.

### Performance (iron rule 2 applies)
Budget for this whole feature: **≤ 4 draw calls** (fleet body, glow, wake, plus one spare). The mesh is 27k tris; at a typical 5–8 live vessels that's ~150–220k instanced triangles in one draw call — acceptable, but verify the stats overlay confirms no fps regression at the Ferry Building. Zero per-frame allocation (reuse `Object3D`/`Vector3` scratch objects module-wide), no timers other than the poll interval, no memory growth across an hour of polling (vessel table is bounded).

## Part 3 — Manifest + docs

1. Add to `app/public/sf-assets/vehicles_manifest.json`:

```json
{
  "id": "sf-bay-ferry",
  "file": "vehicles/SF_Bay_Ferry.glb",
  "kind": "ferry",
  "dims": [11.94, 14.70, 41.70],
  "targetLengthM": 41.7,
  "front": "-Z",
  "tris": 27224,
  "weight": 0,
  "notes": "Live-data vessel; spawned by ferries.js from /api/ferries, not by road traffic. weight 0 keeps it out of the road spawner."
}
```
   `weight: 0` matters — the road-vehicle spawner must ignore it. Verify the spawner actually skips weight-0 entries; if it doesn't, guard it.
2. Update `AGENTS.md` "Current state" with one sentence about the live ferry system and the optional `FERRY_511_KEY` env var.
3. Note in the concierge data docs is NOT required — do not wire ferries into the concierge in this task.

## How to work

Order: preflight → Part 1 (verify with `curl` against the deployed preview, including BOM handling and the no-key path) → demo mode + Part 2 against `?ferries=demo` → live end-to-end with the real key → fallback drills (kill the key in preview env, confirm procedural ferries return) → QA + deploy. Screenshot after each milestone. If 511 field names differ in practice from Appendix A, trust the live response, fix the mapping, and record the actual shape in a comment in `api/ferries.mjs`.

## QA checklist (report PASS/FAIL for each, production URL first line)

- [ ] `GET /api/ferries` with key: `live: true`, plausible vessel list, `s-maxage` header present; without key: `live: false`, HTTP 200; upstream forced to fail: stale-or-false per spec
- [ ] With the real key at ~commute time: multiple vessels visible, positions match the SF Bay Ferry live map (spot-check 2 vessels by name), boats point nose-first along their motion
- [ ] No teleporting: watch one vessel across ≥ 3 poll cycles; motion is continuous, corrections eased
- [ ] Docked boats sit still at terminals without spinning
- [ ] `?ferries=demo`: all 4 scripted behaviors observable (loop, stale-removal, bearing-less heading, off-scene cull)
- [ ] Fallback drill: procedural ferries return within one poll cycle of data loss; no frame ever shows double ferries or zero ferries
- [ ] Perf: draw-call delta for the feature ≤ 4 in the stats overlay; no memory growth over 10 min of polling; 60 fps maintained at the Ferry Building street level
- [ ] Build passes with no `FERRY_511_KEY` anywhere
- [ ] Commit hygiene per `AGENTS.md` rule 6; deployed with `vercel deploy --prod`

## Appendix A — 511 API facts (VERIFIED against the live feed, 2026-08-10)

- Portal: https://511.org/open-data. Rate limit **60 requests/hour per key** — hence the CDN caching design; never call 511 from the browser.
- Endpoint: `https://api.511.org/transit/VehicleMonitoring?api_key=KEY&agency=SB&format=json`.
  **Agency codes (verified from the operators endpoint):** `SB` = San Francisco Bay Ferry ✓ · `SF` = SFMTA/Muni (WRONG — returns 600+ buses/cable cars) · `GF` = Golden Gate Ferry (out of scope) · `TF`/`AF` = Treasure Island / Angel Island ferries (out of scope).
- Response is **gzip-encoded** (Node `fetch` handles it; `curl` needs `--compressed`). The SB response carried **no BOM** on 2026-08-10, but strip one defensively — other 511 endpoints do prefix it.
- **Verified live shape** (actual response, 16 vessels at 2026-08-10 12:29 PT):

```
Siri.ServiceDelivery.VehicleMonitoringDelivery   // object, NOT array, in this response — handle both
  .VehicleActivity[] = {
    RecordedAtTime: "2026-08-10T19:29:26Z",
    ValidUntilTime: "...",
    MonitoredVehicleJourney: {
      LineRef: "Richmond" | null,          // null = not on a scheduled trip
      PublishedLineName: "Richmond" | null,
      DirectionRef, DestinationRef,
      DestinationName: "San Francisco Ferry Building Gate E" | null,
      OperatorRef: "SB",
      VehicleRef: "Dorado",                // the vessel's actual name
      Bearing: 219.0 | absent,             // absent on most docked vessels
      VehicleLocation: { Longitude: -122.390579, Latitude: 37.7961502 },
      Monitored, InCongestion, Occupancy, OriginRef, OriginName,
      MonitoredCall: { ... arrival predictions, unused in this task }
    }
  }
```
- Real observations to design against: in-service vessels (`LineRef` set) had bearings; ~10 laid-up vessels sat at the Alameda maintenance basin (≈ 37.771, −122.300) with no `LineRef` and no `Bearing`; Vallejo-area vessels (*Karl*, *Intintoli*) were ~36 km north of downtown — the water-extent cull must handle them.
- Backup plan (only if VehicleMonitoring for `SB` breaks in the future): the GTFS-Realtime `vehiclepositions` endpoint has the same data in protobuf. Decoding protobuf zero-dep is out of scope — if you hit this, STOP and report rather than adding a dependency.

## Appendix B — Reference coordinates (projection sanity + demo mode)

Terminals (lon, lat): Ferry Building Gate B/E ≈ (−122.3930, 37.7955) · Oakland Jack London ≈ (−122.2790, 37.7946) — off the modeled water's east edge, good for cull testing · Alameda Seaplane ≈ (−122.2985, 37.7877) · Vallejo ≈ (−122.2565, 38.1000) — far north, always culled.
Projection check: Ferry Building should land ≈ x = +3919, z = −502 (meters) with the canonical projection constants; if you compute something wildly different, you re-derived the projection — go back and use `data.project`.

— End of spec. The finish line: open the deployed app during commute hours, look at the Bay next to the real SF Bay Ferry live map, and watch the same boats make the same crossings.
