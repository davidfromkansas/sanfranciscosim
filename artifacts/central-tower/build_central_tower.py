"""Deterministic Blender build of the SF-SIM miniature Central Tower.

    blender -b --python build_central_tower.py -- [--out DIR]

703 Market Street at Third and Kearny: the 1898 Claus Spreckels (Call)
Building, stripped of its Baroque dome and raised to 21 storeys in a 1938
Streamline Moderne remodel. A slim, almost square tower on the SoMa grid:
a rose granite base, then white piers and recessed grey window columns rising
to a single setback at the fifteenth floor and a narrower, flat-topped upper
shaft. Helpers in tools/landmark-kit/toykit.py.
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

SLUG = "central-tower"
CENTER = (-122.4035852, 37.787188)  # OSM way 132127810, OBB centre
H_TOP = 91.0                         # published 299 ft roof (Wikipedia); LiDAR 88.6, OSM 91
H_BASE = 12.0                        # three-storey rose granite base
H_LOW = 62.0                         # top of the full-width shaft (photo: 15th floor)
H_UP = 89.0                          # top of the set-back upper shaft
N_LOW, N_UP = 12, 6                  # storeys in each section (no sliver)

# OSM footprint (m about CENTER): a ~22.6 m square turned to the SoMa grid,
# faces bearing 315 (Market), 45 (Third St), 135 and 225; a small chamfer on
# the rear (south) corner.
PLAN = tk.ccw([(-0.8, -16.3), (0.8, -14.8), (16.5, 0.7), (0.8, 16.3), (-16.5, -0.7)])
YAW = math.radians(45.0)
# the setbacks use the clean square (the rear chamfer is too small to offset)
SQUARE = tk.ccw([(0.0, -15.6), (16.5, 0.7), (0.8, 16.3), (-16.5, -0.7)])


def moderne(name, plan, z0, z1, n, spacing, seed, end):
    """Art Moderne bay system: white piers (the body), recessed grey window
    columns, a dark window per storey in each column, scattered lit panes."""
    bays(name + "_rec", plan, [(z0, z1)], spacing, 0.56, "concrete", out=0.04, end=end, edge_min=4.0)
    fl = storeys(z0, z1, n)
    rows = [(a + 1.0, b - 0.5) for a, b in fl]
    bays(name + "_win", plan, rows, spacing, 0.4, "glassd", out=0.07, end=end, edge_min=4.0)
    lit(name, plan, rows, spacing, 0.36, 0.32, seed, end=end, edge_min=4.0, out=0.1)


def build():
    # rose granite base with tall shopfronts between square piers
    tk.prism("base", tk.offset_poly(PLAN, 0.3), 0.0, H_BASE, "granite", bev=0.15)
    bays("shopfront", tk.offset_poly(PLAN, 0.3), [(0.4, 6.0)], 3.8, 0.7, "glassd", end=0.8)
    lit("shopfront", tk.offset_poly(PLAN, 0.3), [(0.6, 5.8)], 3.8, 0.7, 0.9, 2.0, end=0.8)
    bays("base_win", tk.offset_poly(PLAN, 0.3), [(7.4, 10.4)], 3.8, 0.36, "glassd", end=0.8)
    # full-width shaft
    tk.prism("shaft", PLAN, H_BASE, H_LOW, "white", bev=0.15)
    moderne("shaft", PLAN, H_BASE, H_LOW, N_LOW, 3.4, 7.0, 1.6)
    tk.prism("setback_deck", tk.offset_poly(SQUARE, -0.4), H_LOW - 0.3, H_LOW + 0.05, "concrete")
    tk.ring_band("setback_rail", tk.offset_poly(SQUARE, -0.4), H_LOW, H_LOW + 0.9, 0.4, "white")
    # set-back upper shaft, about 3.5 m in on every side
    up = tk.offset_poly(SQUARE, -3.5)
    tk.prism("upper", up, H_LOW - 0.3, H_UP, "white", bev=0.15)
    moderne("upper", up, H_LOW, H_UP - 1.5, N_UP, 3.2, 3.0, 1.4)
    # flat crown: a parapet over a light line, roof deck, plant, flagpole mast
    tk.ring_band("parapet", tk.offset_poly(up, -0.3), H_UP, H_TOP, 0.3, "white")
    tk.prism("roof", tk.offset_poly(up, -0.4), H_UP - 0.3, H_UP + 0.05, "roofd")
    tk.glow_ring("crown", up, H_UP - 1.3, H_UP - 0.2, 0.08, "white_Glow")
    tk.hvac_cluster("plant", 0.0, 0.0, H_UP + 0.05, YAW, 8.0, 6.0, seed=3.0, hmax=1.6)
    tk.plinth("apron", PLAN, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
