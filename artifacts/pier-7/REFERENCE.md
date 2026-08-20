# Pier 7 — reference dossier

Asset: `pier-7.glb` — Pier 7, the Broadway public access pier, 7 The Embarcadero,
San Francisco. Built from `docs/asset-plans/pier-7.md` (stage 1 of ADDRESS-TO-ASSET);
this file records what was verified, what was estimated, and every deviation.

## What the sources establish

| Source | What it establishes |
|---|---|
| OSM way 23605169 (`man_made=pier`, `surface=wood`, `area=yes`) | The footprint used verbatim: 257.3 × 26.9 m OBB, long axis 54.65° true, five-part plan (entry plaza 20.7 × 12.3 m / 7.5 m walkway / 16.8 × 22 m mid bay / 7.4 m walkway / 26.9 m-wide end platform). No height tag, no building tag — there is nothing on the pier to mis-measure |
| pierfishing.com/pier-7-san-francisco | Dedicated October 1990; a Pier 7 here since 1901; 840 ft long; 35 ft of water; $6,568,581 of pooled public funding; timber decking; ornamental iron handrails; **42 in (1.07 m) metal railing**; antique iron-and-wood benches; Embarcadero light fixtures; fish-cleaning stations |
| Wikipedia (ROMA Design Group) | Designer credit (Boris Dramov, principal); **1993 ASLA National Honor Award** |
| bolerium.com (1983 booklet listing) | "Pier 7: a recreation and public access design project" — ROMA Architects + **T.Y. Lin International, Engineers** |
| stevegillmansculpture.com | "Bay Bench", 1990: two granite benches **17 in high × 8 ft 6 in square** flanking the entry, bronze grill giving visual access to the water; Kring Design Studio site design |
| Baked heightmap (`pipeline/out/terrain.json/bin`, sampled) | Terrain = 0.00 across the whole footprint; 1.6–2.9 m only at the seawall joint. Origin therefore sits on the waterline (pier-3 convention) |
| Geotagged photography (Unsplash `EkXPhMNdKBg` and the pier's large photo corpus) | The look: two straight rows of single-globe dark lamp standards, near-black ornamental railing, warm plank deck, benches against the rails |

## Verified vs estimated

**Verified (measured or documented):** footprint and its five parts; axis 54.65°;
railing height 1.07 m; Bay Bench dimensions (0.43 m high × 2.6 m square); the pier's
emptiness (no building); concrete piles; timber deck.

**Estimated (photo-derived, labelled):**
- Deck top **+3.0 m** above the waterline — inferred from the flush joint with the
  Embarcadero promenade (~2.9–3.0 m); the DEM corroborates 2.9 m at the seawall.
- Lamp standards **4.6 m** above the deck (globe tops 7.6 m above water) — scaled from
  the documented 1.07 m railing in street-level photographs (lamps ≈ 4.3× railing).
- Lamp spacing ~12 m / count 44 — satellite dot-counting plus photo rhythm; the model
  uses 38 flank lamps + 4 end + 2 plaza on an 11.4–12.5 m beat.
- Bench count/placement — observational; densest at the mid bay and end platform.

## Recognition cues (ranked, from the plan)

1. The converging lamp rows — two straight dotted lines, 257 m.
2. The five-part plan: plaza / walkway / mid bay / walkway / wide end platform.
3. Near-black ornamental railing boxing every edge of a warm timber deck.
4. Benches against the rails on a beat.
5. A pier with no shed among the built-up finger piers.

## Simplifications (style bible §22)

- Railing scrollwork → posts (3.8 m beat) + top and mid rails. The ornament is
  sub-pixel from every camera that matters; the rhythm is not.
- Globes enlarged to 0.5 m diameter so they read as dots from the aerial camera.
- Plank field → one warm timber tone with a darker centre lane per walkway; no
  per-plank scoring (sub-pixel).
- Piles → perimeter bents on a 5.6 m beat, doubled rows under the wide bays; no
  interior forest.
- Benches → 4-box units (seat, back, two iron legs).
- Water taps, signage, flag holders, railing scroll pattern: omitted (sub-pixel or
  unverified).

## Deviations from the plan (documented, REPORT beats plan)

- The plan's first draft placed the 26.9 m width at the shore plaza; the measured
  footprint puts it at the **Bay-end platform** (plaza is 20.7 m). The plan was
  corrected before modelling; the model follows the measured polygon.
- Railing post beat relaxed 3.2 → 3.8 m and lamp globes 8×6 → 8×5 segments to land
  under the 14,000-triangle cap (13,860).
- 22 benches, not 16: the end platform takes four (two per flank) instead of two,
  which is what the photographs show.

## Materials

Toy_timber `8a6a4a` (deck, bullrail, bench wood — off-palette WARN: the palette has
no wood; rust `a86444` reads as brick from altitude), Toy_timberd `7a5c3e` (centre
lanes), Toy_ink `3a3530` (ironwork, fascia, piles), Toy_stone `d9d2c2` (plaza band,
Bay Benches), Toy_steel `9aa0a6` (fish stations), Toy_gold `caa64a` (bronze grill),
Toy_amber_Glow `f6e3c0` (the 44 lamp globes — the only night light; base colour IS
the night look).

## Datum and placement

Z = 0 is the **waterline** (`placeGeneric` seats the origin at
`max(0, sampleElevation)` = 0 over the bay). Piles 0→2.4, deck 3.0, walking surface
3.08, railing 4.07, lamp tops exactly **7.60 = targetHeightM**. Origin = footprint
OBB centre = manifest anchor `-122.3955159, 37.7994429`. Authored in true-world
orientation (+Y north); the loader applies no rotation.
