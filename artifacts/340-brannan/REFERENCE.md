# 340 Brannan Street — reference dossier

Research behind `artifacts/340-brannan/`, compiled 16 August 2026. The plan
`docs/asset-plans/340-brannan.md` was the starting point; everything below was
re-verified from primary sources for this build, and the corrections that
changed geometry are called out in `REPORT.md`.

## 1. Identification

| | |
|---|---|
| Address | 340 Brannan Street, San Francisco, CA 94107 |
| Block / lot (APN) | 3775 / 015 |
| OSM | [way 71211340](https://www.openstreetmap.org/way/71211340) — `building=yes`, `addr:housenumber=340`, `addr:street=Brannan Street`, `height=15` |
| DataSF footprint | `mblr = SF3775015`, `sf16_bldgid 201006.0003676` |
| Anchor (WGS84) | **-122.3932324, 37.7812786** — area centroid of the DataSF footprint |
| Site | northeast corner of Brannan Street and Jack London Alley, one lot northeast of 350 Brannan and directly across the alley from it |

Identification needs no derivation here: the OSM way carries the street address,
the DataSF address point resolves to the same parcel, and the "340" numerals are
legible on the building in Google Street View. This is the opposite of the
neighbouring 350 Brannan, whose OSM way is untagged.

## 2. Sources and what each establishes

**Primary / measured**

- **Page & Turnbull, *National Register Certification: South End Historic District*, 26 June 2008** — [PDF](https://sfplanninggis.org/docs/NatRegDistricts/2008-06-26_Final-NR-SouthEndHistDist.pdf). Appendix 2 carries a building data form for 340 Brannan Street: block/lot 3775/015, current use Office, date of construction **1911**, **5** stories, construction type **Reinforced-Concrete**, exterior material **Stucco**, current significance **Non-contributory**, National Register status code **7N**, other information "**Appears extensively altered from original appearance**". Architect and Builder fields are blank. This is the only source that states the exterior material, and it is the reason this asset is not brick.
- **DataSF Building Footprints (LiDAR-derived), `ynuv-fyni`** — footprint polygon; `gnd_min_m` 10.18, `gnd_mediancm` 1123; `hgt_median_m` **14.82**, `hgt_majoritycm` **1503**, `hgt_maxcm` **1779**, `hgt_mincm` 395; `median_1st_m` 26.07, `peak_1st_m` 28.74. 3,296 half-metre cells.
- **DataSF Addresses with Units, `ramy-di5m`** — 340 BRANNAN ST → parcel 3775015, point 37.781265 / -122.393229. Unit records run #101 through #501.
- **SF Assessor Historical Secured Property Tax Rolls, `wv5m-vpq2`** — 1911; 5 stories; construction class **B**; property class O (Office), use code `COMO`; lot area 8,604 sq ft (799.3 m2); property area 41,880 sq ft; zoning MUO. Identical 2020–2025.
- **SF Building Permits, `i98e-djp9`** — 80+ permits 1982–2026. The 1982–85 remodel ("interior partitions in **removated** building", 1984-06-18); **1987-10-22 "construct 460 sq ft removable panel roof deck"**; 1990 and 2011 reroofing; **2010-10-20 "replace cooling towers, replace hydronic boiler, no change in equipment size, same locations on roof"**; **2017-10-31 "water over existing 27 windows (new flashing), existing windows to remain, replace in kind"**; continuous office tenant improvements 1990–2024. `number_of_existing_stories` is **4 on nine applications and 5 on eleven**.

**Commercial / secondary**

- [Transwestern](https://transwestern.com/property/340-brannan-st) — 1911, renovated 1985, class B, 5 stories, typical floor 8,430 sq ft, 1 elevator, 39,375 sq ft listed.
- [LoopNet](https://www.loopnet.com/Listing/340-Brannan-St-San-Francisco-CA/11829135/) — 42,149 sq ft; "creative building at the entrance to South Park with great natural light"; **atrium, conference facility, kitchen, roof terrace**.
- [CompStak](https://property.compstak.com/340-Brannan-Street-San-Francisco/p/2241) — 38,317 sq ft, APN 3775-015, coordinates 37.781265 / -122.393229, last sold 2014.

**Photography**

- Google Street View, Brannan Street, **capture May 2025**, headings ~315–325° from two positions on the south side of the street — the whole SE elevation: sage stucco, four window lines of five bays, the raised parapet, the recessed bronze base, the "340" numerals, the entrance and its dark brick pier, the two mature street trees.
- Google Street View, **Jack London Alley** at 98 Jack London Alley, **capture January 2025**, heading ~30° — the SW elevation close up: same body colour, horizontal banding, the flat metal eyebrow canopy, the ground-floor window wall with an exposed diagonal brace behind the glass, one flush dark service door, wall-mounted lights and cameras, a Transwestern leasing banner (temporary — not modelled).
- Google Street View, Brannan × Jack London Alley three-quarter, capture May 2025 — the south corner with both finished elevations in one frame, and the party-wall junctions with 334 Brannan (northeast) and the block across the alley.
- Google Maps satellite (Vexcel Imaging, 2026) — white membrane roof, continuous parapet ring, the penthouse with a reddish-brown roof, the open trellis / atrium skylight frame, two round cooling towers with ductwork, the timber roof deck, small skylights.

**Consulted and not used**

- The South End Historic District's general architectural description (brick warehouses, arched loading docks, corbelling). Page & Turnbull class this building as a **non-contributor**, so district-level material descriptions are not evidence about it.

## 3. Verified dimensions and orientation

Footprint, projected with the app's tangent projection (LON0 −122.4375,
LAT0 37.77) and recentred on the anchor, in Blender metres (+X east, +Y north),
counter-clockwise:

```
(-20.281,  -0.177)   west corner
( -0.396, -20.202)   south corner  (Brannan x Jack London Alley)
( 20.429,   0.339)   east corner
(  0.267,  20.139)   north corner
```

Area **821.0 m2**. The DataSF survey carries eleven vertices; every one of them
lies within **0.115 m** of this quadrilateral, so the extra points are survey
noise, not corners, and four vertices is the honest simplification. Cross-checks:
OSM way 71211340 gives 768.1 m2 (LiDAR footprints carry the parapet/roof
overhang, so they run a few percent large); the assessor's lot is 799.3 m2; the
listed typical floor is 8,430 sq ft = 783 m2.

| Edge | Length | Outward bearing | Elevation |
|---|---|---|---|
| south → east | **29.25 m** | **135.4°** | Brannan Street front — finished |
| west → south | **28.22 m** | 225.2° | Jack London Alley flank — finished |
| north → west | 28.90 m | 315.3° | northwest party wall — blind |
| east → north | 28.26 m | 44.5° | northeast party wall — blind |

Heights (all above the building's own grade; the app's terrain handles the
NAVD88 datum):

| | Value | Basis |
|---|---|---|
| Roof deck | **14.82 m** | LiDAR `hgt_median_m`; majority cell 15.03 m — measured |
| Main parapet crest | 15.45 m | inferred, deck + 0.63 |
| Raised central parapet | 16.35 m | inferred; see §6 |
| Penthouse crest | **17.79 m** | LiDAR `hgt_maxcm` — measured, and the model's normalised top |

Because the building sits ~45° off the world axes, the axis-aligned bounding box
is 41.05 × 40.68 m for a 29.25 × 28.22 m building. That is expected, not a scale
error.

## 4. Neighbours and exposure

Polygon-to-polygon gaps from the DataSF footprints:

| Neighbour | Gap | Height (LiDAR median / max) | Side |
|---|---|---|---|
| SF3775101 (334 Brannan St) | **0.00 m** | 12.14 / 15.63 m | northeast — party wall |
| SF3775039 (Gran Oriente Filipino block) | **0.00 m** | 7.84 / 12.99 m | northwest — party wall |
| SF3775102 (same block) | **0.00 m** | 10.49 / 12.44 m | northwest — party wall |
| SF3775040 | 5.93 m | 9.83 m | north, beyond |
| SF3775016 (350 Brannan) | 12.32 m | 12.02 m | southwest, across the alley |

So exactly **two finished elevations** and two blind party walls — and because
340 is 15 m to its neighbours' 7.8–12.1 m, roughly the top 3 m of the northeast
wall and the top 4.5–7 m of the northwest wall are exposed above them. Both are
modelled as flat sage wall and left to show.

For the stage-5 exclusion radius, measured from the anchor: our own centroid is
at ~0 m, the nearest **neighbour ring vertex** is at **14.16 m** (SF3775039),
then 15.52 m (SF3775102) and 16.80 m (SF3775101). Our own footprint reaches
20.43 m from the anchor, but `excluded()` drops a footprint on its centroid
*or* any ring vertex, so the centroid test alone is enough. Safe band ~1–14.1 m.

## 5. Observations by elevation

**Southeast — Brannan Street (hero).** Flat sage / gray-green stucco. A tall
ground floor set back ~1.2 m behind a continuous light fascia band, with a dark
bronze storefront system inside it — two horizontal glass strips separated by a
metal rail, on regular mullions. The lobby entrance sits right of centre,
recessed further, under a flat metal canopy, with a dark brick-clad pier on its
northeast side and the white **"340"** numerals on the wall beside it. Above the
fascia, three floors of wide horizontal punched windows in five bays, pale
frames, a single horizontal division per window, with a broad blank spandrel
below each and a blank frieze under the parapet. The roofline steps up across the
middle of the facade on chamfered shoulders.

**Southwest — Jack London Alley.** The same wall, same colour, same rhythm. The
base is a continuous glazed window wall rather than a deep colonnade, with a flat
metal eyebrow canopy above it and one flush dark service door near the northwest
end. The stucco reads as broad horizontal bands of slightly different tone —
either tonal banding or the scored control joints catching light; modelled as a
shallow reveal at each floor line, which is defensible either way.

**Northeast and northwest — party walls.** Blind, no openings, body colour.

**Top.** Bright white membrane inside a continuous parapet. Furniture clusters in
the southwest half: a penthouse ~9 × 7 m with a reddish-brown roof (the tallest
thing on the building and the natural candidate for the 17.79 m LiDAR maximum in
a building with one elevator), an open light-framed trellis over the atrium
immediately northeast of it, two round cooling towers with ductwork to the west,
the timber roof deck southwest of the penthouse, and small skylights near the
west corner. The northeast half of the membrane is clean.

## 6. Recognition cues (ranked)

1. **The raised central parapet with chamfered shoulders** on Brannan — a stepped
   silhouette on a street of dead-flat parapets
2. **The sage / gray-green body** — the only mid-tone green-gray building on the
   block, between white 350, pale 334 and brick 380
3. **The dark recessed base under a continuous light fascia** — one hard shadow
   line at one height across both finished faces
4. Four window lines of **wide horizontal five-bay punched windows** — horizontal,
   not the vertical industrial sash of its neighbours
5. Being the **tallest building on this block face**, ~3 m proud of both party-wall
   neighbours

## 7. Simplified for the miniature

- Five identical bays per finished elevation on all three upper floors
- One flat glazing panel per opening with a single horizontal mullion
- Stucco banding reduced to a shallow scored reveal at two floor lines
- Storefront reduced to two glass strips, a rail, a head, a sill and mullions
- Roof clutter reduced to penthouse, trellis, two cylinders, deck, two skylights,
  hatch and two vents
- Dropped: the two street trees, sidewalk planters, bollards, bike hoops, the
  leasing banner, tenant signage, the exposed diagonal brace behind the alley
  glass, wall-mounted cameras and lights

## 8. Uncertainties and conflicting evidence

- **Four window lines versus five storeys of record.** Every listing, the
  assessor roll and the National Register form say five storeys; the permit
  record splits 4/5; photography from three separate Street View positions shows
  a tall recessed ground floor plus **three** upper window lines. Those reconcile
  arithmetically — 4.60 + 3 × 3.20 + a 0.62 m frieze = the measured 14.82 m deck —
  and five floors of 8,430 sq ft over a 783 m2 plate then requires a fifth
  leasable level that is not a fifth window line, most plausibly a mezzanine
  inside the double-height base where the atrium sits. **Built as photographed.**
- **The National Register report contradicts itself.** Its body text (p. 13) says
  340 and 350 Brannan "appear to be contributors"; its own list of
  non-contributors names 340 Brannan as item 7, and its Appendix 2 data form
  records "Non-contributory", code 7N, "appears extensively altered". Two places
  against one sentence — treated as non-contributory, which is also what the
  1985-remodelled building looks like.
- **OSM `height=15` is the roof deck, not the crest** — it matches the LiDAR
  majority cell (15.03 m) almost exactly, which is what makes it dangerous.
- **Whether 17.79 m is the penthouse is inferred.** The satellite view shows a
  clearly raised block with a reddish roof; the trellis frame beside it is a
  competing candidate. Either way the bounding-box top lands on 17.79.
- **The raised parapet's proportions are inferred** from foreshortened
  photography. Modelled as spanning 18–80% of the frontage with 2.2 m ramps and
  standing 0.90 m over the main crest — slightly exaggerated on purpose, as the
  style bible allows for the one signature feature.
- **The bay count is inferred.** Two mature street trees hide roughly a third of
  the Brannan facade in every capture; five bays is a regularisation of what is
  visible at the two ends plus the alley elevation.
- No architect is recorded for the 1911 building or for the 1984–85 remodel in
  any source consulted.
