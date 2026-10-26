"""Deterministic Blender build of the SF-SIM miniature Hobart Building.

    blender -b --python build_582_market_street.py -- [--out DIR]

582-592 Market Street (Willis Polk, 1914), at the head of Second Street: 21
storeys of tan rusticated terracotta on an asymmetric lot. A slab rises
from Market to about the fourteenth floor with a sheer, blank west flank
(exposed when its neighbour came down in 1967, "HOBART BUILDING" painted
on it); above, the tower narrows to a round-ended shaft with arched upper
windows, a deep Baroque cornice and a low crowning roof. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

# ---------------------------------------------- lean facade helpers (local)
# Flat outward quads (2 tris each) instead of extruded bands: the FiDi batch
# shares one vertex cap, so window graphics are skins over a solid prism.


def bays(name, poly, bands, spacing, frac, mat, out=0.06, density=1.01, seed=0.0, suffix="_panes",
         edge_min=2.0, efilter=None, end=0.0):
    """Per edge: cut into round(L/spacing) bays (one bay if spacing is None),
    put a quad `frac` of the bay wide in each, for every (z0, z1) band.
    `density` < 1 keeps a hashed subset (night lights)."""
    verts, faces = [], []
    for ei, (p0, p1, L, n) in enumerate(tk.edges(poly)):
        if L < edge_min or (efilter and not efilter(ei, p0, p1, n)):
            continue
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        e = min(end, L * 0.25)
        cnt = 1 if spacing is None else max(1, int(round((L - 2 * e) / spacing)))
        step = (L - 2 * e) / cnt
        w = step * frac
        for bi, (z0, z1) in enumerate(bands):
            for i in range(cnt):
                if density < 1.0 and tk.hash01(seed + ei * 71.3 + bi * 13.7 + i * 3.11) > density:
                    continue
                c = e + (i + 0.5) * step
                a, b = c - w / 2, c + w / 2
                pa = (p0[0] + ux * a + n[0] * out, p0[1] + uy * a + n[1] * out)
                pb = (p0[0] + ux * b + n[0] * out, p0[1] + uy * b + n[1] * out)
                k = len(verts)
                verts += [(pa[0], pa[1], z0), (pb[0], pb[1], z0), (pb[0], pb[1], z1), (pa[0], pa[1], z1)]
                faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return tk.new_mesh(name + suffix, verts, faces, [mat], recalc=False)


def lit(name, poly, bands, spacing, frac, density, seed, mat="sand_Glow", out=0.12, **kw):
    """Night skin aligned with `bays` (same bay maths), a hashed subset lit."""
    return bays(name, poly, bands, spacing, frac, mat, out=out, density=density, seed=seed,
                suffix="_glow", **kw)


def storeys(z0, z1, n, margin=0.0):
    """n equal storey bands between z0 and z1 (no sliver), trimmed by margin."""
    h = (z1 - z0) / n
    return [(z0 + i * h + margin, z0 + (i + 1) * h - margin) for i in range(n)]

SLUG = "582-market-street"
CENTER = (-122.4016471, 37.7894844)  # OSM way 32946628, OBB centre
H_TOP = 87.0                          # published 285 ft (Wikipedia); LiDAR max 86.7
H_BASE = 8.0
H_SLAB = 58.0                         # top of the full-lot slab (photo: ~14th floor)
H_TOWER = 79.0                        # cornice line of the round-ended tower
YAW = math.radians(45.0)              # Market Street frame: u along Market (NE), v to the NW


def M(u, v):
    return tk.rot2((u, v), YAW)


# OSM way 32946628, split at the back of the Market Street slab (m about CENTER)
FRONT = [(12.6, -6.2), (-7.7, -25.9), (-10.7, -6.9), (2.7, 6.3), (10.55, 7.5)]
REAR = [(10.55, 7.5), (2.7, 6.3), (2.1, 10.6), (-5.0, 9.3), (-7.1, 23.6), (7.8, 25.9)]


def tower_plan():
    """Upper shaft (Market frame): flush with the Market face, its east end
    following the east party line, a semicircular west end."""
    v0, v1 = -12.6, 1.2
    r = (v1 - v0) / 2
    cu = -8.0
    pts = [(cu, v0), (4.6, v0), (11.8, -2.9), (8.0, v1), (cu, v1)]
    for i in range(1, 8):
        a = math.pi / 2 + math.pi * i / 8
        pts.append((cu + r * math.cos(a), (v0 + v1) / 2 + r * math.sin(a)))
    return tk.ccw([M(u, v) for u, v in pts])


def front_or_east(ei, p0, p1, n):
    """Every face is windowed except the sheer west flank (outward normal ~ west)."""
    return n[0] > -0.8


def build():
    front, rear = tk.ccw(FRONT), tk.ccw(REAR)
    # rear wing: lower plain block behind the slab (height inferred)
    tk.prism("rear", rear, 0.0, 32.0, "stone", bev=0.15)
    bays("rear_win", rear, [(a + 1.2, b - 0.6) for a, b in storeys(4.0, 31.0, 7)], 3.2, 0.45, "glassd", end=1.0)
    lit("rear", rear, [(a + 1.2, b - 0.6) for a, b in storeys(4.0, 31.0, 7)], 3.2, 0.45, 0.3, 4.0, end=1.0)
    tk.prism("rear_roof", tk.offset_poly(rear, -0.4), 31.7, 32.3, "roofd")
    # Market Street slab: shopfront base, rusticated punched shaft, blank west flank
    tk.prism("base", front, 0.0, H_BASE, "terracotta", bev=0.15)
    bays("shops", front, [(0.6, 5.8)], 4.2, 0.8, "glassd", end=0.8, efilter=front_or_east)
    lit("shops", front, [(0.8, 5.6)], 4.2, 0.8, 0.9, 1.0, end=0.8, efilter=front_or_east)
    tk.prism("slab", front, H_BASE, H_SLAB, "terracotta", bev=0.15)
    fl = storeys(H_BASE, H_SLAB, 13)
    bays("slab_win", front, [(H_BASE + 1.0, H_SLAB - 1.2)], 3.0, 0.42, "glassd", out=0.05, end=1.0,
         efilter=front_or_east)
    bays("slab_rust", front, [(a, a + 1.6) for a, _ in fl[1:]], None, 0.99, "terracotta", out=0.08,
         efilter=front_or_east, end=0.9)
    lit("slab", front, [(a + 1.8, b - 0.3) for a, b in fl], 3.0, 0.38, 0.3, 6.0, end=1.0, efilter=front_or_east)
    # the painted sign high on the blank west flank
    p0, p1 = (-10.7, -6.9), (-7.7, -25.9)
    L = math.dist(p0, p1)
    n = ((p1[1] - p0[1]) / L, -(p1[0] - p0[0]) / L)   # outward = west (edge runs south)
    a = (p0[0] + (p1[0] - p0[0]) * 0.2, p0[1] + (p1[1] - p0[1]) * 0.2)
    b = (p0[0] + (p1[0] - p0[0]) * 0.8, p0[1] + (p1[1] - p0[1]) * 0.8)
    s = tk.flat_quad("sign_panes", a, b, H_SLAB - 7.0, H_SLAB - 3.0, 0.05, "ink", n)
    s.name = "sign_panes"
    tk.prism("slab_roof", tk.offset_poly(front, -0.4), H_SLAB - 0.3, H_SLAB + 0.6, "roofd")
    # round-ended upper tower
    tw = tower_plan()
    tk.prism("tower", tw, H_SLAB - 0.5, H_TOWER, "terracotta", bev=0.12)
    tb = storeys(H_SLAB, H_TOWER - 7.0, 4)
    bays("tower_win", tw, [(a + 1.1, b - 0.6) for a, b in tb], 2.9, 0.5, "glassd", end=0.2, edge_min=2.4)
    lit("tower", tw, [(a + 1.1, b - 0.6) for a, b in tb], 2.9, 0.5, 0.4, 2.0, end=0.2, edge_min=2.4)
    tk.ring_band("tower_band", tw, H_TOWER - 7.0, H_TOWER - 6.0, 0.35, "cream")
    tk.arched_panes("arches", tw, H_TOWER - 5.6, H_TOWER - 1.6, 3.0, 1.7, mat="glassd", seg=4)
    tk.arched_panes("arches_lit", tw, H_TOWER - 5.2, H_TOWER - 2.2, 3.0, 1.2, mat="sand_Glow", out=0.1,
                    seg=4, suffix="_glow")
    tk.cornice("cornice", tw, H_TOWER, h=2.4, out=1.4, mat="cream")
    # crowning roof: attic band and a low hipped roof with a finial
    at = tk.offset_poly(tw, -0.6)
    tk.prism("attic", at, H_TOWER + 2.4, H_TOWER + 4.2, "terracotta", bev=0.1)
    tk.frustum("roof", at, H_TOWER + 4.2, tk.scale_poly(at, 0.35, *M(0.0, -5.4)), H_TOP - 0.8, "verdigris",
               bottom=False)
    c = M(0.0, -5.4)
    tk.cylinder("finial", c[0], c[1], H_TOP - 0.9, H_TOP, 0.5, "gold", seg=6, r1=0.15)
    tk.glow_ring("crown", tw, H_TOWER - 0.6, H_TOWER + 0.1, 0.06, "sand_Glow")
    tk.plinth("apron", front, h=0.25, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
