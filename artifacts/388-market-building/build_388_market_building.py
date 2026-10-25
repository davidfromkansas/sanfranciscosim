"""Deterministic Blender build of the SF-SIM miniature 388 Market Street.

    blender -b --python build_388_market_building.py -- [--out DIR]

388 Market Street (Skidmore, Owings & Merrill, 1986): a 24-storey flatiron
on the triangular block between Market, Pine and Front streets. A long
wedge with a fully rounded west end at Front and Pine and a slim rounded
prow at the east tip: red granite with punched windows, a sheer dark glass
wall on Pine that sweeps over the upper floors of the Market face, stacked
glass bays up the prow, and a two-storey corner pavilion at Market and
Front. Helpers in tools/landmark-kit/toykit.py.
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

SLUG = "388-market-building"
CENTER = (-122.3981595, 37.7922638)  # OSM way 1279504526, OBB centre
H_TOP = 111.9                         # DataSF 2010 LiDAR (published 94 m conflicts; see REFERENCE.md)
H_BASE = 9.0
N_FL = 22                              # storeys above the 2-storey base
Z_VEIL = 66.0                          # where the glass sheath starts on the Market face (photo)

# OSM building:part 288505730 (the 24-storey tower), m about CENTER, arcs thinned.
TOWER = [(-3.3, -22.0), (-6.2, -22.1), (-9.5, -21.6), (-13.4, -20.4), (-17.2, -17.8), (-20.6, -13.8),
         (-22.5, -9.0), (-22.8, -4.0), (-22.0, -0.3), (-19.5, 4.6), (-15.9, 8.1), (-11.9, 10.2),
         (-8.6, 11.0), (35.7, 17.9), (36.9, 17.5), (37.8, 16.3), (37.9, 15.0), (37.0, 13.7),
         (33.1, 9.8), (27.5, 4.3), (22.2, -0.9), (15.7, -7.4), (11.0, -12.0), (6.4, -16.7),
         (2.1, -20.0)]
# building:part 288505726: the 2-storey pavilion filling the Market / Front corner
PAVILION = [(-22.5, -9.0), (-22.7, -10.1), (-18.4, -38.2), (1.0, -20.8), (2.1, -20.0), (-3.3, -22.0),
            (-9.5, -21.6), (-15.7, -19.1), (-20.6, -13.8)]


def is_pine(ei, p0, p1, n):
    """The long straight north face on Pine Street: all dark glass."""
    return math.dist(p0, p1) > 30.0 and n[1] > 0.9


def is_market(ei, p0, p1, n):
    """The long Market Street face (outward normal to the south-east)."""
    return n[0] > 0.5 and n[1] < -0.5


def is_prow(ei, p0, p1, n):
    """The rounded east prow: short edges east of x = 34 m."""
    return min(p0[0], p1[0]) > 34.0


def granite(ei, p0, p1, n):
    return not is_pine(ei, p0, p1, n) and not is_prow(ei, p0, p1, n)


def build():
    tower = tk.ccw(TOWER)
    pav = tk.ccw(PAVILION)
    tk.prism("pavilion", pav, 0.0, H_BASE, "rust", bev=0.15)
    bays("pav_glass", pav, [(0.8, 7.2)], 4.0, 0.8, "glassd", end=0.6)
    lit("pav", pav, [(1.0, 7.0)], 4.0, 0.8, 0.9, 1.0, end=0.6)
    tk.prism("pav_roof", tk.offset_poly(pav, -0.6), H_BASE - 0.3, H_BASE + 0.05, "roofd")
    tk.ring_band("pav_parapet", tk.offset_poly(pav, -0.6), H_BASE, H_BASE + 0.8, 0.6, "rust")
    # tower: red granite body over a glazed shopfront base
    tk.prism("base", tower, 0.0, H_BASE, "rust", bev=0.15)
    bays("lobby", tower, [(0.6, H_BASE - 1.2)], None, 0.92, "glassd", edge_min=1.5)
    lit("lobby", tower, [(0.8, H_BASE - 1.4)], None, 0.9, 0.85, 2.0, edge_min=1.5)
    z_roof = H_TOP - 1.5
    tk.prism("shaft", tower, H_BASE, z_roof, "rust", bev=0.2)
    fl = storeys(H_BASE, z_roof - 1.0, N_FL)
    # granite faces: punched window columns under a granite spandrel quad per storey
    bays("win", tower, [(H_BASE + 0.8, z_roof - 1.6)], 2.6, 0.5, "glassd", out=0.05, end=0.8,
         efilter=granite)
    bays("spandrel", tower, [(a, a + 1.9) for a, _ in fl[1:]], None, 0.995, "rust", out=0.08, efilter=granite)
    # Pine face: a sheer dark glass wall, top to bottom
    bays("pine_glass", tower, [(H_BASE, z_roof)], None, 1.0, "glass", out=0.05, efilter=is_pine)
    # Market face: the glass sheath that wraps over the granite in the upper floors
    bays("veil", tower, [(Z_VEIL, z_roof)], None, 1.0, "glass", out=0.11, efilter=is_market)
    # prow: stacked glass bays between thin granite bands
    bays("prow", tower, [(a + 0.7, b) for a, b in fl], None, 1.0, "glass", out=0.05, edge_min=0.5,
         efilter=is_prow)
    lit("shaft", tower, [(a + 2.1, b - 0.3) for a, b in fl], 2.6, 0.46, 0.3, 8.0, end=0.8, edge_min=3.0,
        out=0.16)
    # crown: a thin granite parapet, roof deck, plant, a light line
    tk.ring_band("parapet", tk.offset_poly(tower, -0.4), z_roof, H_TOP, 0.4, "rust")
    tk.prism("deck", tk.offset_poly(tower, -0.4), z_roof - 0.3, z_roof + 0.05, "roofd")
    tk.hvac_cluster("plant", 2.0, 1.0, z_roof + 0.05, math.radians(45.0), 26.0, 8.0, seed=4.0, hmax=1.4)
    tk.glow_ring("crown", tower, z_roof - 1.2, z_roof - 0.2, 0.18, "white_Glow")
    tk.plinth("apron", tower, h=0.25, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
