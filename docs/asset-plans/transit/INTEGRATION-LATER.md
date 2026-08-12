# Transit integration — deferred

<!--
Nothing here is in scope for the five asset plans. This file exists so the
findings behind those plans are not lost while the models are being built.
-->

The five plans in this directory produce **validated GLBs and nothing else**.
Placement, spawning, weighting and live data are a separate job, deliberately
deferred (owner decision, 12 August 2026).

This file parks what was already found so the follow-up session does not have to
rediscover it. Everything below is measured from `origin/main`.

---

## The headline: live Muni positions are one parameter away

`api/ferries.mjs` normalises **511.org's SIRI VehicleMonitoring feed** for the
ferry fleet, and its own source comment names the answer:

```js
const UPSTREAM = 'https://api.511.org/transit/VehicleMonitoring';
const AGENCY = 'SB'; // SB = SF Bay Ferry / WETA (SF is Muni, GF is Golden Gate).
```

`agency=SF` on the same endpoint is live Muni. The feed carries vehicle
positions, line references and journey references, which means the follow-up
does not need a route whitelist, a rail network, or invented paths — it needs the
same treatment the ferries already got:

- `api/muni.mjs` as a thin normaliser over the same endpoint (the ferry file is a
  ready-made template: memoisation, rate-limit budgeting, stale-serving, backoff)
- `app/src/muni.js` mirroring `app/src/ferries.js` — its own spawner, its own
  interpolation between fixes, its own clickable context cards
- The optional-key discipline of AGENTS rule 4: without `MUNI_511_KEY` the
  endpoint answers `{ live: false }` and procedural/roaming vehicles stay

**Unverified — check this first.** That every Muni *mode* appears in the feed is
an assumption, not a confirmed fact. Buses and Metro certainly do. The F line
almost certainly does (third-party apps show live F-line vehicle positions on the
route map). **Cable cars are unconfirmed** — SFMTA material refers to tracking
"bus, train, streetcar or cable car," but nothing consulted confirms they are in
511's SIRI feed, and 511's own SFMTA page does not list modes. One authenticated
request with `agency=SF` settles it: read the distinct `LineRef` values and see
which modes are present. Do that before designing anything around the feed.

If a mode turns out to be missing, the model is still wanted — it just needs a
different placement route (the whitelist option below). Nothing about the asset
plans changes.

Three further things to check when that work starts:

- **The 60 requests/hour key limit is shared.** `api/ferries.mjs` budgets against
  it carefully (90 s memoisation, a per-hour timetable cap). A second agency
  polling the same key needs to be budgeted alongside it, not independently.
- **Muni is a much larger fleet than WETA** — hundreds of vehicles versus a
  handful. The response size, the interpolation cost and the instance count all
  scale accordingly, and `CAR_COUNT = 720` is the whole city's vehicle budget
  today.
- **`LineRef` maps to the asset.** The feed says which line a vehicle is on,
  which is exactly what picks between hybrid bus, trolley coach, LRV and
  streetcar — no heuristics needed.

This supersedes the route-constraint discussion below, which was written before
the live-data direction was confirmed. Keep the fallback options in mind only
for the no-key path.

---

## Hard prerequisite: `weight` does not work

```js
// app/src/agents.js ~line 1040
const type = i % fleet.length;

// ~line 548 — the only use of weight in the entire codebase
entries = entries.filter((entry) => (entry.weight ?? 1) > 0);
```

`CAR_COUNT = 720` vehicles are dealt to fleet types in strict rotation. The
manifest's `weight` field is read **only** as a `> 0` filter — it does not
weight anything.

Consequence: adding the ~13 transit types these plans define would make Muni
**~48% of San Francisco's traffic**, roughly 350 transit vehicles against 370
cars, under the current spawner.

The fix is small — build a cumulative weight table at load, sample it with the
existing per-car hash — but note that the **existing 14 road types also need
explicit weights** at that point, since they currently rely on round-robin for
their distribution. Suggested target: transit ≈ 6% of traffic, ≈ 45 of 720.

Under a live-data implementation this matters less for the transit types (their
count comes from the feed) but still has to be solved for the car fleet they
share the budget with.

---

## Route constraint (only needed on the no-key path)

Without live data, vehicles would be placed by the road spawner, which puts them
anywhere. A cable car in the Outer Sunset or an LRV on Lombard is a visible
error.

**Path records carry no street name.** From `app/src/city.worker.js:816`:

```js
paths.push({ points: path, klass: d.klass[l], width: cls.width,
             speed: cls.speed, lift: PATH_LIFT, sidewalk: cls.sidewalk || null });
```

`klass`, `width`, `speed` — no name. So name-matching routes is not possible from
the runtime paths as they stand.

- **Option A — constrain by `klass`.** Free today. Restricting long vehicles
  (articulated coaches, LRVs) to arterial classes prevents the worst of it. Will
  not stop a cable car on the wrong arterial.
- **Option B — a hand-authored polyline whitelist.** A small JSON of lon/lat for
  the three cable car lines, the F line, and the N/J/T surface segments — a few
  hundred points. Data, not infrastructure: no pipeline change, no baked tiles.

Per-family need, if this path is taken: buses none · trolley coach optional ·
LRV recommended · cable car and F line strongly recommended.

---

## Per-type scale is an open question

```js
// app/src/agents.js, setToy()
carScale = on ? 1.6 : 1;
```

Diorama mode is the only mode, so `carScale` is always 1.6 and it applies to
fleet instances, not just the procedural fallback boxes.

| Vehicle | Real | At 1.6× |
|---|---|---|
| 40 ft bus | 12.2 m | 19.5 m |
| 60 ft articulated | 18.3 m | 29.3 m |
| Siemens S200 LRV | 22.9 m | 36.6 m |
| Coupled 2-car LRV | 45.7 m | 73.2 m |
| PCC streetcar | 14.0 m | 22.4 m |
| Powell cable car | 8.4 m | 13.4 m |

A 29 m articulated coach is most of a Sunset block; a coupled Metro pair at 73 m
is longer than many of the blocks it would run down. Each asset plan requires a
1.6× in-city render, so **the evidence for this decision will already exist** by
the time integration starts — read those reports before deciding whether to add a
per-type scale override.

---

## Other integration-side items

- **Per-instance tinting for the F-line PCC liveries.** The historic-streetcar
  plan authors the PCC with its livery panels on `Toy_body` so one geometry
  serves 3–5 colourways at one draw call. That needs `kitfleet.js`'s mechanism
  (`tintVectors()`, `BODY_BASE`, an `instanceColor` on the `InstancedMesh`)
  ported into the vehicle path in `agents.js`. Without it: one PCC colour, or
  three baked-livery GLBs at three draw calls. See that plan's §2.6.
- **Every manifest entry is a permanent draw call.** `loadVehicles()` builds one
  `InstancedMesh` per entry, `frustumCulled = false`, alive for the session. The
  five plans add ~13 types = ~13 calls against the 300-call budget of AGENTS
  rule 2. That arithmetic already shaped the plans' variant counts; it also caps
  how many more variants can ever be added.
- **`commuter-bus.glb` stays.** It is a plausible non-Muni coach (charter,
  shuttle). Deleting it when the Muni buses land would be a regression.
- **Articulation bending** (LRV, artic coaches) is a runtime feature, not a
  modelling one. The GLBs export straight with named section nodes
  (`LRV_Section_A` / `_B` / `_Bellows`); a runtime that bends them needs a hinge
  transform at the joint. Node names survive meshopt intake because
  `pipeline/compress-assets.mjs` runs `-kn` — verify after compression.
- **`carArchetype()` stays** — AGENTS rule 3, the procedural fallback is a
  guarantee.
- **Clickable transit cards** would follow the ferry precedent naturally: a
  cable car naming its line and 1873 landmark status, a PCC naming its livery's
  home city.

---

## Also worth fixing while in here

`.agents/skills/sf-asset-check/SKILL.md` rule 5 says **"vehicle piece ≤ 300"**
triangles. The shipped fleet runs 4,888–9,688 — every vehicle in the tree fails
the contract it is checked against. The skill line is the stale one and should be
corrected to match the shipped fleet.
