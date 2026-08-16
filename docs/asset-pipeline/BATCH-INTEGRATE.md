# Batch integrate — many landmarks, one bake, one PR

Takes several finished landmark branches and puts them all into the city at
once. Run it when a batch of `ADDRESS-TO-ASSET.md` sessions have reached gate 5
in batch mode — each one a source-only branch with no tiles committed.

**Why this exists.** Baking the city rewrites ~600 generated files no matter
which landmark caused it, so a branch that commits its own bake conflicts with
every other landmark branch, including ones on the far side of the city. In
August 2026 five such branches were all mutually unmergeable (#107, #108, #109,
#111, #112) and had to be untangled by hand into #113. Baking once for the whole
batch avoids the situation rather than resolving it.

Budget about 40 minutes, most of it waiting on the bake.

---

## 1. Merge the source branches

```
git worktree add ../sf-wt-batch -b pipeline/<batch-name> origin/main
cd ../sf-wt-batch
git merge --no-ff origin/pipeline/<slug>      # once per landmark
```

Merging (rather than cherry-picking or rebuilding the files by hand) keeps each
landmark's own commits and authorship in the history.

Expect conflicts in exactly three files, all append-only lists, all resolved by
keeping **both** sides:

| File | Resolution |
|---|---|
| `app/public/sf-assets/landmarks_manifest.json` | union by `id` — keep every entry from both sides |
| `pipeline/lib/landmarks.mjs` | keep both `LANDMARKS` entries; the branches append at the same place, so the conflict is adjacent objects, not overlapping ones |
| `docs/asset-plans/README.md` | keep both table rows, then set the "Shared contract (all N)" heading to the number of plan rows |

Two traps in the `landmarks.mjs` resolution, both of which produce a file that
looks right and does not parse:

- The conflict markers usually sit **inside** the array, so each side is a bare
  entry sharing the array's closing `},\n];`. Splicing the two sides together
  needs a `},` between them AND a `{` opening the second — dropping the `{` is
  the easy mistake.
- Verify before moving on: `node -e "import('./pipeline/lib/landmarks.mjs').then(m => console.log(m.LANDMARKS.length))"`,
  and `git diff origin/main -- pipeline/lib/landmarks.mjs` should show
  **insertions only**. Any deletion means a merge ate an existing landmark.

If a branch also touched `app/public/tiles/` or `api/_data/`, it was not run in
batch mode. Take `origin/main`'s side for those files — this run regenerates
them anyway.

## 2. Bake once

From the repo root:

```
(cd pipeline && npm install)
ln -s ~/sf-worktrees/<any-worktree-with-data>/pipeline/data pipeline/data   # ~700 MB, gitignored
```

`pipeline/data/` is the raw download cache and is safe to share between
worktrees. `pipeline/out/` is **not** — it is pipeline output, and seeding it
from a worktree on another branch mixes two versions of the pipeline's own code.
Let this run regenerate `out/` from scratch.

Run every stage, in order, with a raised heap (`buildings` and `lore` are killed
at the default limit while reading the 320 MB DataSF file):

```
cd pipeline
for s in loredata terrain bridges buildings streets landcover \
         validate lore toy notables context muni-shapes; do
  node --max-old-space-size=12288 $s.mjs || break
done
cd ..
```

Roughly 10 minutes; `lore` is most of it. Run it in the background — a
foreground run that hits a 10-minute tool timeout leaves the tree mid-chain with
thousands of files deleted.

Do not stop early. `validate` wipes `app/public/tiles/` before republishing, so
a chain that ends before `context` leaves the committed sidecars deleted and
search and the concierge broken. `lore` must precede `context`.

Then remove the symlink (`rm pipeline/data`) — it is not covered by the
`pipeline/data/` gitignore rule and will otherwise be committed as a link.

Then confirm `git status` shows nothing deleted under `app/public/tiles/`. The
publish step used to wipe that directory wholesale and take
`app/public/tiles/muni-shapes.bin` with it — the one file no later stage
restores, since `muni-shapes.mjs` needs `MUNI_511_KEY` and no-ops without it.
`validate.mjs` now clears only the tiers it owns, so this should come up clean;
if the file is missing, `git checkout -- app/public/tiles/muni-shapes.bin` puts
it back. Symptom if it slips through: a `sf-muni: no route shapes (shapes bad
magic)` console warning and buses that dead-reckon.

## 3. Verify

```
node pipeline/verify-rebake.mjs
node pipeline/audit.mjs
```

`verify-rebake` is the one that matters here. It compares every cell's building
count against `origin/main` and reports the distance from each new landmark to
the nearest surviving footprint. Two things must hold:

- **Only the new landmarks' cells changed.** A cell that moves anywhere else
  means either a radius reaching further than its author measured, or a bake run
  against a different `pipeline/data/` snapshot than main was baked from — which
  churns tiles citywide with invisible sub-quantum vertex drift and inflates the
  PR to thousands of files. The script's failure text explains how to tell those
  apart.
- **Nothing survives inside any exclusion radius**, or the baked block is still
  standing where the GLB goes.

A landmark whose cell count did not change is not automatically a failure — the
footprint may simply not exist in the source data, as the Veterans Building's
does not — but the script says so explicitly, because a silent pass would read
as proof the exclusion worked when it did nothing.

From `audit.mjs`, **check 1.6 must pass**. Checks 1.2b, 1.3c and 1.7b fail on
main today; they are pre-existing and not yours.

Finally, per AGENTS.md, run `node pipeline/landmark-streaming-check.mjs` against
a build — the procedural fallback hides loader failures from the eye, and this
is what catches them.

## 4. One PR

Commit the regenerated tiles in a single commit separate from the merges, so a
reviewer can see the source changes without the generated noise. Then open one
PR that supersedes the batch, and close the individual landmark PRs pointing at
it.

Put `verify-rebake`'s per-cell table in the PR body. It is the only part of a
600-file diff a human can actually check.

Two things worth stating in the body rather than leaving to be discovered:

- Any landmark whose exclusion dropped nothing, and why.
- If the diff is large: the great majority of changed `ctx/*.json` sidecars are
  usually pure renumbering, not content. Buildings are keyed by a global running
  index, so dropping one footprint shifts every later id and rewrites nearly
  every sidecar with no semantic change. Spot-check one far-away cell and quote
  it.
