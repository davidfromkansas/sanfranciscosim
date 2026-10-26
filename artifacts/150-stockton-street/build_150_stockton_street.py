"""Deterministic Blender build of the SF-SIM miniature Neiman Marcus Union Square.

    blender -b --python build_150_stockton_street.py -- [--out DIR]

Neiman Marcus, 150 Stockton Street at Geary (Philip Johnson / John Burgee,
1982), on the site of the City of Paris department store (1896), whose glass
rotunda and stained-glass dome were kept and set into the new building's
Stockton x Geary corner. A long, nearly windowless box clad in a rose-and-
white granite checkerboard, a green glass corner pavilion around the
rotunda, and a lighter set-back service storey on the roof. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "150-stockton-street"
CENTER = (-122.4059193, 37.78737)    # OSM way 332521036, OBB centre
H_TOP = 33.9                          # LiDAR crest 33.9 m (batch facts file); DataSF ring majority 32.9 m
H_BOX = 28.0                          # main roof: DataSF ring median 28.4 m, OSM height 28
YAW = tk.bearing_to_yaw(80.9)
# OSM footprint about CENTER (the slightly bowed east end simplified)
PLAN = [(42.5, 28.1), (-49.1, 13.5), (-42.5, -28.1), (34.4, -15.2), (48.8, -13.0), (45.0, 12.2)]
CORNER = (-49.1, 13.5)                # Stockton x Geary (NW) corner, the rotunda


def L(x, y):
    return tk.rot2((x, y), YAW)


def inside(pt, poly):
    x, y = pt
    c = False
    for i in range(len(poly)):
        (x1, y1), (x2, y2) = poly[i - 1], poly[i]
        if (y1 > y) != (y2 > y) and x < x1 + (y - y1) * (x2 - x1) / (y2 - y1):
            c = not c
    return c


def checker(name, poly, bands, cell, mat, out=0.05):
    """Checkerboard of flat cells on every edge, offset by one cell on alternate bands."""
    verts, faces = [], []
    for ei, (p0, p1, Ln, n) in enumerate(tk.edges(poly)):
        cnt = int(Ln // cell)
        if cnt < 2:
            continue
        ux, uy = (p1[0] - p0[0]) / Ln, (p1[1] - p0[1]) / Ln
        pad = (Ln - cnt * cell) / 2
        for bi, (z0, z1) in enumerate(bands):
            for i in range(bi % 2, cnt, 2):
                a, b = pad + i * cell, pad + (i + 1) * cell
                pa = (p0[0] + ux * a + n[0] * out, p0[1] + uy * a + n[1] * out)
                pb = (p0[0] + ux * b + n[0] * out, p0[1] + uy * b + n[1] * out)
                k = len(verts)
                verts += [(pa[0], pa[1], z0), (pb[0], pb[1], z0), (pb[0], pb[1], z1), (pa[0], pa[1], z1)]
                faces.append((k, k + 1, k + 2, k + 3))
    return tk.new_mesh(name + "_panes", verts, faces, [mat], recalc=False)


def build():
    plan = tk.ccw(PLAN)
    # main box: rose granite with a checkerboard of darker diamonds
    tk.prism("box", plan, 0.0, H_BOX, "granite", bev=0.15)
    checker("check", plan, tk.floors(5.0, H_BOX - 0.5, 3.75), 3.75, "rust")
    # ground floor: shop windows and a lit storefront band
    tk.ring_band("storefront", plan, 0.0, 4.6, 0.1, "glassd")
    tk.glow_ring("storefront_lit", plan, 0.8, 4.0, 0.16, "sand_Glow")
    tk.ring_band("fascia", plan, 4.6, 5.0, 0.25, "stone")
    # the corner glass pavilion around the City of Paris rotunda
    cx, cy = CORNER[0] + L(8.0, -7.0)[0], CORNER[1] + L(8.0, -7.0)[1]
    ring = tk.ellipse(11.0, 11.0, 12, cx, cy)
    exposed = lambda ei, a, b, n: not inside(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), plan)  # noqa: E731
    tk.cylinder("rotunda", cx, cy, 0.0, H_BOX + 1.0, 11.0, "glassl", seg=12)
    tk.lit_windows("rotunda", ring, tk.floors(0.5, H_BOX, 4.6), 5.7, 0.9, seed=1.0, out=0.08, margin=0.4,
                   gap=0.5, edge_filter=exposed)
    tk.cylinder("dome", cx, cy, H_BOX + 1.0, H_BOX + 3.2, 8.0, "glassl", seg=12, r1=3.0)
    tk.glow_cap("dome_lit", tk.ellipse(3.0, 3.0, 12, cx, cy), H_BOX + 3.25, "gold_Glow")
    # roof: deck, parapet and the lighter set-back upper storey toward the east end
    tk.prism("roof_deck", tk.offset_poly(plan, -0.4), H_BOX - 0.3, H_BOX + 0.05, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), H_BOX, H_BOX + 1.0, 0.4, "granite")
    upper = tk.xform(tk.rect(46.0, 30.0, 12.0, 0.0), YAW)
    tk.prism("upper", upper, H_BOX, H_TOP - 1.6, "stone", bev=0.12)
    tk.panes("upper_win", upper, [(H_BOX + 1.2, H_TOP - 2.4)], 4.0, mat="glassd", gap=1.4, margin=0.3)
    tk.lit_windows("upper_lit", upper, [(H_BOX + 1.2, H_TOP - 2.4)], 4.0, 0.35, seed=3.0, out=0.1, margin=0.5,
                   gap=1.6)
    tk.prism("upper_roof", tk.offset_poly(upper, -0.3), H_TOP - 1.9, H_TOP - 1.5, "roofd")
    tk.hvac_cluster("plant", *L(12.0, 0.0), H_TOP - 1.5, YAW, 28.0, 18.0, seed=7.0, hmax=1.5, fans=False)
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
