# Matson Building — reference dossier

215 Market Street, San Francisco. Bliss & Faville, 1922–24 (annex 1945–47). NRHP 1995.
Plan: `docs/asset-plans/matson-building.md`.

## Sources and what each establishes

| Source | Establishes |
|---|---|
| OSM way 1279504249 (https://www.openstreetmap.org/way/1279504249) | footprint 44.7 x 42.5 m, 1,864 m², edges 135.4° / 45.4°, OBB centre (anchor) |
| Wikipedia "Matson Building" | 16 storeys, Renaissance Revival, terra cotta, "column-like" three sections, dates, twin of PG&E |
| Commons infobox photo, File:Matson Building & Annex (San Francisco).jpg | Market facade: arcaded base, central entrance arch, punched shaft, paired arched top storey, bracketed cornice, rooftop arcaded penthouse |
| DataSF 2010 LiDAR `201006.0000581` (https://data.sf.gov/resource/ynuv-fyni) | nothing usable: one ring covers tower + annex + plaza (max 94.69, majority 6.07 m) |
| DataSF query 2026-10-25, box around the anchor | no separate Matson ring exists |
| CTBUH "215-245 Market Street" | 93.5 m / 18 fl is the PG&E building next door, not Matson — ruled out |
| Structurae, SKYDB | 16 floors, no height |

## Verified dimensions and location

- Anchor `-122.3965080, 37.7926550` (OSM OBB centre; the bbox recentre moved it < 0.1 m).
- Modelled plan 43.5 x 41.5 m (OBB minus ~0.6 m per side for the cornice overhang).
- **Height 73.0 m, ESTIMATED.** 16 storeys scaled from the twin: PG&E's 17 storeys
  measure 79.8 m (LiDAR crest), ~4.2 m a storey with a double-height base, so ~70 m to the
  Matson balustrade and ~73 m to the penthouse cornice. OSM `height=83` is unsourced.

## Orientation

True-world, +Y north. Local +X = bearing 135.4°. **Market Street = NW face (local −X)**,
Main Street = NE, PG&E = SW, annex = SE. The entrance arch is on the NW face.

## Recognition cues (ranked)

1. Cream terracotta block matched to PG&E.
2. Three-part column: arcade / plain shaft / arched capital storey.
3. Deep cornice and balustrade.
4. Grand entrance arch on Market.
5. Arcaded rooftop penthouse.

## Preserved / simplified

- Preserved: storey count read (13 shaft storeys + base + capital), arch rhythms, cornice
  depth (exaggerated to 1.6 m for the aerial camera), the penthouse.
- Simplified: fluted pilasters, frieze, medallions and the "MATSON BUILDING" sign are
  omitted; paired arches are single arches at 2.8 m; all four faces share the Market
  treatment except the portal.
- Off-palette: `Toy_terracotta` (warm cream), same as PG&E.

## Uncertainties

- Height (above). The single biggest risk.
- Penthouse size/position from one street photo.
- NE/SW/SE elevations not photographed; inferred.
