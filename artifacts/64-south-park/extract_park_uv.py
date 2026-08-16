"""Reduce the OSM survey of South Park to the build script's input.

    python3 extract_park_uv.py [--refetch]

Reads data/overpass_raw.json (the cached Overpass response for OSM way 24052083
and everything inside it; --refetch re-queries the API and rewrites it) and
writes data/park_uv.json: every measured feature reprojected into the park's own
(u, v) frame, plus the two things the build needs that OSM does not carry — the
derived tree infill and the tree family assignment.

Frame (see docs/asset-plans/64-south-park.md 2.3):

    origin  the minimum-area oriented bounding box centre of the park polygon,
            -122.3939704, 37.7815903
    +u      along the long axis toward the NORTH-EAST (Second Street),
            bearing 45.467 deg true
    +v      across, toward the SOUTH-EAST (Brannan Street), bearing 135.467 deg

Nothing here is art-directed. Every number that comes out of this file is either
measured from OSM or produced by a rule stated in the docstring of the function
that produces it, and every derived tree is tagged "derived" in the output so a
reader can tell the two apart at a glance.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "data", "overpass_raw.json")
OUT = os.path.join(HERE, "data", "park_uv.json")

PARK_WAY = 24052083
SHOUT_WAY = 549848249
MAIN_PATH_WAY = 549848273

# The app's one projection (pipeline/lib/geo.mjs). Never re-derived elsewhere.
LON0, LAT0 = -122.4375, 37.77
M_PER_DEG_LON = 111320 * math.cos(math.radians(LAT0))
M_PER_DEG_LAT = 110540

OVERPASS = "https://overpass-api.de/api/interpreter"
QUERY = (
    "[out:json][timeout:120];way(%d);map_to_area->.a;"
    "(node(area.a);way(area.a););out tags geom;way(%d);out geom;" % (PARK_WAY, PARK_WAY)
)


def project(lon, lat):
    """WGS84 -> the app's local tangent metres. x east, z south."""
    return ((lon - LON0) * M_PER_DEG_LON, -(lat - LAT0) * M_PER_DEG_LAT)


def refetch():
    import urllib.parse
    import urllib.request

    body = urllib.parse.urlencode({"data": QUERY}).encode()
    with urllib.request.urlopen(OVERPASS, body, timeout=180) as r:
        data = json.loads(r.read().decode())
    with open(RAW, "w") as fh:
        json.dump(data, fh)
    return data


def convex_hull(points):
    pts = sorted(set(points))

    def half(seq):
        out = []
        for p in seq:
            while len(out) >= 2:
                (x0, y0), (x1, y1) = out[-2], out[-1]
                if (x1 - x0) * (p[1] - y0) - (y1 - y0) * (p[0] - x0) > 0:
                    break
                out.pop()
            out.append(p)
        return out

    return half(pts)[:-1] + half(pts[::-1])[:-1]


def oriented_bbox(points):
    """Rotating calipers over the hull. Returns (centre, long, cross, angle) where
    `angle` is the rotation of the LONG axis in the local x/z frame."""
    hull = convex_hull(points)
    best = None
    for i in range(len(hull)):
        (x0, z0), (x1, z1) = hull[i], hull[(i + 1) % len(hull)]
        ang = math.atan2(z1 - z0, x1 - x0)
        c, s = math.cos(-ang), math.sin(-ang)
        us = [p[0] * c - p[1] * s for p in hull]
        vs = [p[0] * s + p[1] * c for p in hull]
        w, h = max(us) - min(us), max(vs) - min(vs)
        if best is None or w * h < best[0]:
            best = (w * h, ang, w, h, (min(us) + max(us)) / 2, (min(vs) + max(vs)) / 2)
    _, ang, w, h, uc, vc = best
    c, s = math.cos(ang), math.sin(ang)
    centre = (uc * c - vc * s, uc * s + vc * c)
    if w >= h:
        return centre, w, h, ang
    return centre, h, w, ang + math.pi / 2


def polygon_area(poly):
    a = 0.0
    for i in range(len(poly)):
        x0, y0 = poly[i]
        x1, y1 = poly[(i + 1) % len(poly)]
        a += x0 * y1 - x1 * y0
    return abs(a) / 2


def polyline_length(poly):
    return sum(math.dist(poly[i], poly[i + 1]) for i in range(len(poly) - 1))


# ------------------------------------------------------------------- families

# Species mix from HortScience, *Tree Assessment, South Park*, Nov 2015 (31
# London plane, 13 American elm, 3 silver dollar gum, 3 white alder, 1 Lombardy
# poplar, 1 olive of 52), reconciled with the 2016-17 works: 30 trees removed,
# 24 mature 36" box trees planted, "18 aged elm and sycamore" retained.
#
# The assignment rule, stated once so it can be argued with:
#   * the 20 OSM-mapped trees are the RETAINED mature stand. The three silver
#     dollar gums are documented as being "on the north side of the park", which
#     is v < 0 in this frame, so they go to the three lowest-v mapped trees.
#     The rest split elm/plane by a deterministic hash in the 13:31 ratio the
#     survey found, floored to give 7 elms.
#   * every DERIVED tree is a 2017 planting - a 36" box tree eight years on -
#     and gets the low broadleaf family.
# Crest heights are ESTIMATED (plan 2.15 risk 1); the tallest elm IS the asset's
# height datum and is pinned to TALLEST_ELM_M exactly.
TALLEST_ELM_M = 15.0

# crown_r_lo is the WIDEST ring and crown_r_hi the upper one, so an elm at
# 4.60/3.90 draws a crown about 9.2 m across over a 11 m rise — very close to
# 1:1, which is what a broadleaf is.
#
# Both directions were tried and both were wrong. At 2.90 m the crowns were
# taller than they were wide and the park came out planted with 34 cypresses.
# At 15% wider than the figures below, the canopy closed over the ground
# pattern, which on this asset IS the subject (plan 2.9). What makes the
# current values work is that the trees stand at |v| ~ 9.5 m on a park 23.5 m
# wide: a 4.6 m radius reaches in to v ~ 5 and stops at the edge of the
# promenade, so the canopy rings the park and the path still reads down the
# middle — which is also what the aerial photography shows.
FAMILIES = {
    # name:      (crest_lo, crest_hi, trunk_top, crown_lo, crown_r_lo, crown_r_hi)
    "elm": (13.5, TALLEST_ELM_M, 4.6, 4.0, 4.60, 3.90),
    "plane": (10.0, 12.5, 3.6, 3.0, 4.90, 4.10),
    "gum": (12.0, 14.0, 5.2, 4.6, 3.60, 2.90),
    "broadleaf": (6.0, 7.5, 2.2, 1.8, 3.30, 2.85),
}


def hash01(n):
    """The pipeline's mixer (pipeline/lib/geo.mjs), so 'random' variation is
    reproducible across rebuilds and reviewable in a diff."""
    h = (n ^ 0x9E3779B9) * 0x85EBCA6B & 0xFFFFFFFF
    h = (h ^ (h >> 13)) * 0xC2B2AE35 & 0xFFFFFFFF
    h ^= h >> 16
    return (h & 0xFFFFFFFF) / 4294967296.0


def assign_families(measured):
    """measured: list of (u, v) in survey order. Returns a parallel list of names."""
    gums = sorted(range(len(measured)), key=lambda i: measured[i][1])[:3]
    fams = [None] * len(measured)
    for i in gums:
        fams[i] = "gum"
    rest = [i for i in range(len(measured)) if fams[i] is None]
    # 13:31 elm:plane over the survey; 7 of 17 here, taken as the highest hashes
    # so the choice is deterministic and inspectable.
    ranked = sorted(rest, key=lambda i: -hash01(i * 2654435761))
    for i in ranked[:7]:
        fams[i] = "elm"
    for i in ranked[7:]:
        fams[i] = "plane"
    return fams


def derive_infill(measured, ring_v_lo, ring_v_hi):
    """One tree at the midpoint of every gap longer than GAP_M along each of the
    two long garden-bed edges (|v| > 6 m), inset to the mean |v| of the mapped
    edge trees. Plan 2.15 risk 2: OSM's 20 trees are an undercount against a
    near-continuous perimeter canopy in the aerial, and this is the bounded,
    stated rule that closes the ring. Nothing is placed inside |v| <= 6 m, where
    the lawns and the path are."""
    GAP_M = 14.0
    out = []
    for sign in (-1, 1):
        edge = sorted(u for u, v in measured if v * sign > 6.0)
        if not edge:
            continue
        vs = [v for u, v in measured if v * sign > 6.0]
        v_mean = sum(vs) / len(vs)
        span = [-79.75 + 6.0] + edge + [79.75 - 6.0]
        for a, b in zip(span, span[1:]):
            if b - a > GAP_M:
                n = int((b - a) // GAP_M)
                for k in range(1, n + 1):
                    out.append((a + (b - a) * k / (n + 1), v_mean))
    return out


# ----------------------------------------------------------------------- main


def main():
    if "--refetch" in sys.argv or not os.path.exists(RAW):
        data = refetch()
    else:
        data = json.load(open(RAW))

    elements = {(e["type"], e["id"]): e for e in data["elements"]}
    park = elements[("way", PARK_WAY)]
    ring_ll = [(p["lon"], p["lat"]) for p in park["geometry"]]
    if ring_ll[0] == ring_ll[-1]:
        ring_ll = ring_ll[:-1]
    ring_xz = [project(lon, lat) for lon, lat in ring_ll]

    centre, long_m, cross_m, ang = oriented_bbox(ring_xz)
    cx, cz = centre
    # local x east / z south -> true bearing = atan2(dx, -dz)
    bearing_long = math.degrees(math.atan2(math.cos(ang), -math.sin(ang))) % 360
    if bearing_long > 180:
        bearing_long -= 180
    rot = -ang
    rc, rs = math.cos(rot), math.sin(rot)

    def uv(lon, lat):
        x, z = project(lon, lat)
        x -= cx
        z -= cz
        return (round(x * rc - z * rs, 4), round(x * rs + z * rc, 4))

    def way_uv(e):
        return [uv(p["lon"], p["lat"]) for p in e["geometry"]]

    def closed(poly):
        if len(poly) > 1 and math.dist(poly[0], poly[-1]) < 1e-6:
            return poly[:-1]
        return poly

    out = {
        "_": "GENERATED by extract_park_uv.py - do not hand-edit",
        "source": {
            "park_way": PARK_WAY,
            "wikidata": park["tags"].get("wikidata"),
            "overpass_query": QUERY,
        },
        "anchor_lonlat": [
            round(LON0 + cx / M_PER_DEG_LON, 7),
            round(LAT0 - cz / M_PER_DEG_LAT, 7),
        ],
        "heading_long_deg": round(bearing_long, 4),
        "heading_cross_deg": round((bearing_long + 90) % 360, 4),
        "obb": {"long_m": round(long_m, 4), "cross_m": round(cross_m, 4)},
        "ring": closed(way_uv(park)),
        "walls": [],
        "lawns": [],
        "beds": [],
        "paths": [],
        "plazas": [],
        "benches": [],
        "tables": [],
        "picnic_tables": [],
        "lamps": [],
        "waste": [],
        "bike": [],
        "water": [],
    }
    out["area_m2"] = round(polygon_area(out["ring"]), 2)

    measured_trees = []
    for e in data["elements"]:
        tags = e.get("tags") or {}
        if not tags:
            continue
        if e["type"] == "node":
            p = uv(e["lon"], e["lat"])
            if tags.get("natural") == "tree":
                measured_trees.append(p)
            elif tags.get("amenity") == "bench":
                out["benches"].append(p)
            elif tags.get("amenity") == "table":
                out["tables"].append(p)
            elif tags.get("leisure") == "picnic_table":
                out["picnic_tables"].append(p)
            elif tags.get("highway") == "street_lamp":
                out["lamps"].append(p)
            elif tags.get("amenity") == "waste_basket":
                out["waste"].append(p)
            elif tags.get("amenity") == "bicycle_parking":
                out["bike"].append(p)
            elif tags.get("amenity") == "drinking_water":
                out["water"].append(p)
            continue
        if e["id"] == PARK_WAY or "geometry" not in e:
            continue
        poly = way_uv(e)
        if e["id"] == SHOUT_WAY:
            ring = closed(poly)
            us = [p[0] for p in ring]
            vs = [p[1] for p in ring]
            out["shout"] = {
                "ring": ring,
                "centre": [round((min(us) + max(us)) / 2, 4), round((min(vs) + max(vs)) / 2, 4)],
                "radius_m": round((max(us) - min(us) + max(vs) - min(vs)) / 4, 4),
            }
        elif tags.get("highway") == "footway":
            out["paths"].append(
                {"id": e["id"], "main": e["id"] == MAIN_PATH_WAY,
                 "surface": tags.get("surface"), "line": poly}
            )
        elif tags.get("amenity") == "bench":
            out["walls"].append({"id": e["id"], "line": poly})
        elif tags.get("leisure") == "garden":
            out["beds"].append({"id": e["id"], "poly": closed(poly)})
        elif tags.get("leisure") == "playground":
            out["playground"] = {"id": e["id"], "poly": closed(poly)}
        elif tags.get("landcover") == "grass" or tags.get("landuse") == "grass":
            out["lawns"].append({"id": e["id"], "poly": closed(poly)})
        elif tags.get("tourism") == "picnic_site":
            ring = closed(poly)
            us = [p[0] for p in ring]
            vs = [p[1] for p in ring]
            out["plazas"].append(
                {"id": e["id"], "centre_u": round((min(us) + max(us)) / 2, 3),
                 "half_len_u": round((max(us) - min(us)) / 2, 3)}
            )

    fams = assign_families(measured_trees)
    trees = [
        {"uv": list(p), "src": "osm", "family": f, "crest_m": None}
        for p, f in zip(measured_trees, fams)
    ]
    vs = [p[1] for p in out["ring"]]
    for p in derive_infill(measured_trees, min(vs), max(vs)):
        trees.append({"uv": [round(p[0], 4), round(p[1], 4)], "src": "derived",
                      "family": "broadleaf", "crest_m": None})

    # Crest height inside each family's band, deterministic per tree index, and
    # the ONE tallest elm pinned to the datum so max_z is exact.
    for i, t in enumerate(trees):
        lo, hi = FAMILIES[t["family"]][0], FAMILIES[t["family"]][1]
        t["crest_m"] = round(lo + (hi - lo) * hash01(i), 3)
    elms = [t for t in trees if t["family"] == "elm"]
    max(elms, key=lambda t: t["crest_m"])["crest_m"] = TALLEST_ELM_M
    out["trees"] = trees
    out["tallest_elm_m"] = TALLEST_ELM_M
    out["families"] = {
        k: dict(zip(("crest_lo", "crest_hi", "trunk_top", "crown_lo",
                     "crown_r_lo", "crown_r_hi"), v))
        for k, v in FAMILIES.items()
    }
    out["plazas"].sort(key=lambda p: p["centre_u"])

    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)

    main_path = [p for p in out["paths"] if p["main"]][0]["line"]
    print("anchor            %.7f, %.7f" % tuple(out["anchor_lonlat"]))
    print("heading long/cross %.4f / %.4f deg true" % (out["heading_long_deg"], out["heading_cross_deg"]))
    print("obb                %.3f x %.3f m, area %.1f m2 (%.3f acre)"
          % (out["obb"]["long_m"], out["obb"]["cross_m"], out["area_m2"], out["area_m2"] / 4046.86))
    print("main path          %.2f m over %d vertices" % (polyline_length(main_path), len(main_path)))
    print("seat walls         %d runs, %.1f m total"
          % (len(out["walls"]), sum(polyline_length(w["line"]) for w in out["walls"])))
    print("lawns              %d, %.0f m2" % (len(out["lawns"]), sum(polygon_area(l["poly"]) for l in out["lawns"])))
    print("beds               %d, %.0f m2" % (len(out["beds"]), sum(polygon_area(b["poly"]) for b in out["beds"])))
    print("playground         %.0f m2; Shout r=%.2f m at u=%.2f v=%.2f"
          % (polygon_area(out["playground"]["poly"]), out["shout"]["radius_m"], *out["shout"]["centre"]))
    print("plaza centres u    %s" % [p["centre_u"] for p in out["plazas"]])
    print("trees              %d osm + %d derived = %d; crests %.1f-%.1f m"
          % (len(measured_trees), len(trees) - len(measured_trees), len(trees),
             min(t["crest_m"] for t in trees), max(t["crest_m"] for t in trees)))
    for fam in FAMILIES:
        print("  %-10s %d" % (fam, len([t for t in trees if t["family"] == fam])))
    print("furniture          %d bench %d table %d picnic %d lamp %d waste %d bike %d fountain"
          % (len(out["benches"]), len(out["tables"]), len(out["picnic_tables"]),
             len(out["lamps"]), len(out["waste"]), len(out["bike"]), len(out["water"])))
    print("wrote", OUT)


if __name__ == "__main__":
    main()
