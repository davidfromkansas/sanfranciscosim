# 326 Brannan — stage 5 local integration QA evidence

Captured 17 August 2026 in headless Chrome over CDP against a production build of
`app/dist`, clock pinned with `SF.setClock`, camera at `SF.goTo(-122.3928965,
37.7815080, …)`. See `../REPORT.md` §8b for the PASS table and for why the
Browser pane could not be used (a hidden pane suspends rAF, so the renderer
reports zero frames).

| File | What it proves |
|---|---|
| `qa-isolated-day-se.png` | The asset alone in the scene (everything but the shared landmark batch and terrain hidden): correct position, correct 45° heading, gate with its five bottles and red disc facing Brannan on the SE, shed at the NW rear. |
| `qa-isolated-night-se.png` | All four `_Glow` groups light in the app's own night pass: the 12-pane roll-up door, both string-light catenaries, the fire-table burner, the JAX disc. |
| `qa-integrated-day-se.png` | The lot in the finished scene at 190 m. The olive crown reads in the gap between the neighbours; there is no procedural twin and no baked block poking through. A 5.9 m walled court between a 12.1 m and an 8.1 m neighbour is *supposed* to be mostly hidden from a locked 42° aerial. |
| `qa-block-context-day-se.png` | The wider block face at 420 m, with South Park top-left, for orientation. |
| `qa-fallback-drill.png` | The mandatory drill: with the GLB renamed aside the app logs one warning per load attempt, throws no uncaught exception, keeps rendering, and the lot degrades to empty ground — the documented Case B fallback. Both neighbours still stand, which is the visual half of the exclusion-radius proof. |

Diorama mode locks the camera pitch at 42°, so `SF.goTo`'s pitch argument has no
effect; the framing differences between these shots are distance and yaw only.
