# Performance baseline beyond fps — 2026-08-17

Measured against production (`https://sf-3d.vercel.app`, commit `5c91f3b`, i.e. after the
camera-radius residency PR #142) with `pipeline/health-probe.mjs`:

```
node pipeline/health-probe.mjs --url https://sf-3d.vercel.app --label prod-baseline --flight 150
```

Raw JSON: `artifacts/perf/prod-baseline-v2-2026-08-17T00-53-23-875Z.json`.

## Why this exists

`pipeline/perf-harness.mjs` answers "how long is a frame", which this VM (SwiftShader, no
`/dev/dri`) cannot answer honestly. The health probe collects the half of the guardrail that is
either GPU-independent or a structural count, so the same command produces comparable numbers on a
real machine, in CI, or on the deployed site.

## What it measures

| Group | Metric | Why it matters |
| --- | --- | --- |
| Loading | time to first frame, time to boot-curtain lift, MB and requests on a cold cache-cleared Fast 4G visit | what a first-time visitor waits through |
| Main thread | long tasks > 50 ms, tasks > 200 ms, total blocking time, event-loop lag p50/p95/max | the stutter you feel while dragging; a 200 ms hitch reads worse than a steady low fps |
| Memory | heap start/peak/end, growth per minute over a continuous 8-waypoint flight, renderer geometry/texture/program counts | the mobile crash-and-reload mechanism |
| Work per frame | peak scene-pass draw calls and triangles (read inside `renderer.render`, not polled) | the leading indicator for fps on hardware we cannot test on |
| Stability | `webglcontextlost`, renderer crashes, failed requests, 404s, uncaught errors | silent failures the eye does not catch |

## Baseline (production, post-#142)

| | desktop profile | mobile profile (CPU 4×, 390×844 @ dpr 3) |
| --- | --- | --- |
| Time to first frame (Fast 4G, cold) | 23.7 s | 33.1 s |
| Time to boot curtain lift | 81.8 s | 71.3 s |
| Transferred to curtain lift | 15.5 MB / 330 requests | 12.6 MB / 194 requests |
| Heap after load | 208 MB | 191 MB |
| Heap over a 150 s flight | 203 → 223 MB (peak 223) | 205 → 202 MB (peak 214) |
| Heap growth | +8 MB/min | −1.2 MB/min |
| Renderer geometries / textures / programs | 93 / 15 / 31 | 89 / 15 / 30 |
| Peak scene-pass draw calls | 56 | 55 |
| Peak scene-pass triangles | 6.5 M | 5.2 M |
| Context lost / crashes / 404s / errors | 0 / 0 / 0 / 0 | 0 / 0 / 0 / 0 |
| Governor tier settled on | high | medium |

Reference points for the memory rows: the pre-#142 audit measured 1.2–2.1 GB of JS heap and 413 MB
of GPU geometry with the whole city resident. Draw calls have never been the problem (budget 300).

## What these numbers do NOT say

- **Frame timings, long tasks, blocking time and event-loop lag are host-limited here.** The probe
  recorded ~0.7 frames/sec, event-loop lag in the seconds, and 66–150 long tasks per flight, but
  only 2.6 ms (desktop) / 9.8 ms (mobile) per frame was spent inside `renderer.render` — the rest is
  the software rasterizer blocking the compositor. On real hardware these collapse. They are logged
  for reproducibility, not quoted as findings.
- **The city never settles on this box.** Streaming is driven by the render loop, so at 0.7 fps only
  472 of 1656 cells and 0 near chunks had loaded after 150 s of flying. Residency counts, triangle
  peaks and heap figures are therefore *floors*, not steady-state values, and the load timings are
  inflated by rendering, not by the network.
- **Nothing here proves 60 fps.** That still needs a real desktop GPU and real iOS/Android devices,
  per the browser matrix in `PERF-PLAN.md`.

## Open question this baseline raises

The only honest source for frame timings, hitches and peak memory on the devices that actually
crash is those devices. Two ways to get them, in increasing effort:

1. A `?perf` self-test in the app: runs ~20 s, prints fps / p95 frame time / hitch count / heap /
   load time on screen, no backend. Anyone can run it on their own phone and read the numbers off.
2. Real-user monitoring: the same numbers sampled from a fraction of real visits and beaconed to an
   existing `/api` function, so the crash rate and the p95 come from real traffic rather than from
   one device.

Neither is implemented yet.
