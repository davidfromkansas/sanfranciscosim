"""Deterministic Blender build of the SF-SIM miniature Old Federal Reserve Bank.

    blender -b --python build_301_battery_street.py -- [--out DIR]

400 Sansome / 301 Battery Street (George W. Kelham, 1924; NRHP, SF Landmark
158), now the Bently Reserve: grey granite, a giant eight-column Ionic
colonnade on Sansome under an eagle-studded entablature, three storeys of
tall pilaster-framed windows above, an attic and cornice, and a setback upper
floor. A U-shaped office block wraps a lower banking-hall court; a one-storey
annex closes the Battery end. Footprints are the OSM building:part ways.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "301-battery-street"
CENTER = (-122.4007784, 37.7943144)   # OSM way 32947510, OBB centre
H_TOP = 47.6                          # MEASURED: LiDAR majority 47.64 m (SF0229003); median 45.05, max 50.64
# OSM parts, metres from CENTER (+x east, +y north)
U_BLOCK = [(-38.5, 13.0), (-33.0, -23.6), (30.1, -14.2), (29.6, -10.8), (25.0, 18.9), (24.6, 22.1),
           (7.0, 19.5), (10.4, -2.5), (-18.4, -6.8), (-21.8, 15.5)]               # 940071571, 7 levels
COURT = [(7.0, 19.5), (10.4, -2.5), (-18.4, -6.8), (-21.8, 15.5)]                # 1285793212, 4 levels
ANNEX = [(25.0, 18.9), (33.4, 20.2), (38.0, -9.6), (29.6, -10.8)]                # 940071563, 1 level
# U_BLOCK without its two small jogs, for the setback floor offset
U_SIMPLE = [(-38.5, 13.0), (-33.0, -23.6), (30.1, -14.2), (25.2, 20.5), (7.0, 19.5), (10.4, -2.5),
            (-18.4, -6.8), (-21.8, 15.5)]
SANSOME = ((-38.5, 13.0), (-33.0, -23.6))


def near(polys, tol=1.5):
    """Edge filter: keep edges longer than 8 m that do not lie against any of `polys`."""
    def keep(ei, p0, p1, nrm):
        if math.dist(p0, p1) <= 8.0:
            return False
        m = ((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2)
        for poly in polys:
            for a, b, L, _ in tk.edges(tk.ccw(poly)):
                t = max(0.0, min(1.0, ((m[0] - a[0]) * (b[0] - a[0]) + (m[1] - a[1]) * (b[1] - a[1])) / (L * L)))
                if math.dist(m, (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)) < tol:
                    return False
        return True
    return keep


def build():
    ub, court, annex = tk.ccw(U_BLOCK), tk.ccw(COURT), tk.ccw(ANNEX)
    # banking-hall court (4 storeys) with a lit skylight, and the one-storey Battery annex
    tk.prism("court", court, 0.0, 18.0, "stone", bev=0.1)
    tk.prism("skylight", tk.offset_poly(court, -4.0), 18.0, 18.6, "glassl")
    tk.glow_cap("skylight", tk.offset_poly(court, -4.4), 18.62, "sand_Glow")
    north = lambda ei, p0, p1, nrm: nrm[1] > 0.8  # noqa: E731  (the court's street face on Commercial)
    tk.panes("court_win", court, [(0.0, 8.0), (8.0, 17.0)], 4.6, mat="glassd", gap=2.4, margin=1.2, edge_filter=north)
    tk.lit_windows("court_lit", court, [(0.0, 8.0), (8.0, 17.0)], 4.6, 0.4, seed=2.0, out=0.1, margin=1.6, gap=2.8,
                   edge_filter=north)
    tk.prism("annex", annex, 0.0, 5.0, "stone", bev=0.1)
    tk.prism("annex_roof", tk.offset_poly(annex, -0.4), 4.9, 5.2, "roofd")

    # granite office block: base, pilastered window storeys, attic, cornice
    tk.prism("block", ub, 0.0, 39.0, "stone", bev=0.15)
    base_bands = [(0.0, 8.0), (8.0, 16.0)]
    outer = near([])
    low = near([COURT, ANNEX])          # below 18 m the court and annex bury the inner faces
    tk.panes("base_win", ub, base_bands, 4.6, mat="glassd", gap=2.4, margin=1.2, edge_filter=low)
    tk.lit_windows("base_lit", ub, base_bands, 4.6, 0.35, seed=1.0, out=0.1, margin=1.6, gap=2.8, edge_filter=low)
    tk.cornice("entablature", ub, 16.0, h=1.6, out=0.8, mat="concrete")
    tall = [(17.6, 33.2)]
    tk.panes("tall_win", ub, tall, 4.2, mat="glassd", gap=1.6, margin=0.6, edge_filter=outer)
    tk.lit_windows("tall_lit", ub, [(17.6, 25.4), (25.4, 33.2)], 4.2, 0.4, seed=4.0, out=0.1, margin=0.8,
                   gap=2.0, edge_filter=outer)
    tk.pier_grid("pilasters", ub, 17.6, 33.2, 4.2, 1.1, 0.35, "concrete", skip_short=8.0)
    tk.ring_band("attic_band", ub, 33.2, 33.8, 0.4, "concrete")
    tk.panes("attic_win", ub, [(33.8, 38.4)], 4.2, mat="glassd", gap=2.6, margin=1.2, edge_filter=outer)
    tk.cornice("cornice", ub, 39.0, h=1.4, out=1.2, mat="concrete")
    tk.prism("deck", tk.offset_poly(ub, 0.3), 40.3, 40.6, "roofd")
    # setback upper floor (inferred from the LiDAR roof at 45-47.6 m)
    upper = tk.offset_poly(U_SIMPLE, -3.2)
    tk.prism("upper", upper, 40.4, 46.6, "stone", bev=0.1)
    tk.panes("upper_win", upper, [(40.4, 46.6)], 3.6, mat="glassd", gap=1.4, margin=1.4, edge_filter=outer)
    tk.lit_windows("upper_lit", upper, [(40.4, 46.6)], 3.6, 0.35, seed=9.0, out=0.1, margin=1.6, gap=1.6,
                   edge_filter=outer)
    tk.ring_band("upper_parapet", tk.offset_poly(upper, -0.4), 46.6, H_TOP, 0.4, "concrete")
    tk.prism("upper_deck", tk.offset_poly(upper, -0.2), 46.5, 46.8, "roofd")

    # the giant Ionic colonnade on Sansome: eight columns, steps, eagle entablature
    (a, b) = SANSOME
    L = math.dist(a, b)
    ux, uy = (b[0] - a[0]) / L, (b[1] - a[1]) / L
    nrm = (uy, -ux)                     # outward normal of the Sansome edge (points west)
    yaw = math.atan2(uy, ux)
    mid = ((a[0] + b[0]) / 2, (a[1] + b[1]) / 2)
    off = 2.6
    c = (mid[0] + nrm[0] * off, mid[1] + nrm[1] * off)
    tk.box("steps", c[0] + nrm[0] * 1.0, c[1] + nrm[1] * 1.0, 0.0, 1.0, L - 6.0, 6.0, "concrete", yaw=yaw)
    for i in range(8):
        t = -(L - 9.0) / 2 + (L - 9.0) * i / 7
        x, y = c[0] + ux * t, c[1] + uy * t
        tk.cylinder(f"col{i}", x, y, 1.0, 14.6, 0.85, "stone", seg=10)
        tk.box(f"cap{i}", x, y, 14.6, 15.2, 2.2, 2.2, "concrete", yaw=yaw)
    tk.box("entab", c[0], c[1], 15.2, 17.6, L - 6.0, 2.4, "concrete", yaw=yaw, bev=0.1)
    tk.flat_quad("hall_lit_glow", (a[0] + ux * 6, a[1] + uy * 6), (b[0] - ux * 6, b[1] - uy * 6), 2.0, 12.0, 0.12,
                 "sand_Glow", nrm)
    tk.prism("sidewalk", tk.offset_poly(ub, 2.5), 0.0, 0.2, "stone")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
