"""Deterministic Blender build of the SF-SIM miniature Matson Building Annex.

    blender -b --python build_matson_building_annex.py -- [--out DIR]

The 1945-47 annex of Bliss & Faville's Matson Building (215 Market Street):
a seven-storey strip along the old building's south-east wall, running from
Main Street back to the PG&E annex and designed to match it. The miniature
reuses the Matson landmark's language (artifacts/matson-building/) at a lower,
plainer scale: a cream terracotta block on an arcaded terracotta base, punched
windows at the same 2.8 m rhythm, a terracotta cornice. Its north-west face
stands 0.75 m clear of the Matson model (past its 0.6 m base cornice), and its
south-west end is a party wall against the PG&E annex. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "matson-building-annex"
CENTER = (-122.3962731, 37.7924648)  # OSM way 260291407, OBB centre
H_TOP = 23.4                          # facts-file LiDAR height (measured); consistent with 7 storeys
YAW = tk.bearing_to_yaw(45.9)         # local +x = NE (Main St end), +y = NW (toward the Matson Building)
# Matson landmark (artifacts/matson-building/build_matson_building.py): OBB centre, 43.5 m along 135.4 deg
M_CENTER = (-122.396508, 37.792655)
M_HALF, M_BEARING, CLEAR = 21.75, 135.4, 0.75
X0, X1, Y_SE = -21.0, 21.0, -7.3    # OSM: SW end, NE end, SE face


def matson_face_y(x):
    """Local y of the plane CLEAR metres in front of Matson's SE face, at local x."""
    mx = (M_CENTER[0] - CENTER[0]) * tk.KX
    my = (M_CENTER[1] - CENTER[1]) * tk.KY
    u = (math.sin(math.radians(M_BEARING)), math.cos(math.radians(M_BEARING)))
    ul = tk.rot2(u, -YAW)                     # Matson's +X in annex-local axes (about -y)
    ml = tk.rot2((mx, my), -YAW)
    # points p with (p - ml) . ul = M_HALF + CLEAR
    k = M_HALF + CLEAR + ml[0] * ul[0] + ml[1] * ul[1]
    return (k - x * ul[0]) / ul[1]


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def street(ei, p0, p1, n):
    """Windows on the SE face and the NE (Main St) end only."""
    m = tk.rot2(n, -YAW)
    return m[1] < -0.9 or m[0] > 0.9


def build():
    loc = [(X0, Y_SE), (X1, Y_SE), (X1, matson_face_y(X1)), (X0, matson_face_y(X0))]
    plan = L(loc)
    tk.prism("base", plan, 0.0, 5.4, "terracotta", bev=0.15)
    tk.arched_panes("arcade", plan, 0.5, 4.6, 4.6, 2.8, mat="glassd", edge_filter=street)
    tk.lit_windows("arcade_lit", plan, [(0.5, 3.6)], 4.6, 0.8, seed=3.0, out=0.1, margin=0.3, gap=2.2,
                   edge_filter=street)
    tk.ring_band("base_band", plan, 5.4, 6.0, 0.35, "cream")
    tk.punched_block("shaft", plan, 6.0, 21.6, 2.6, wall="cream", win="glassd", spacing=2.8, gap=1.2,
                     margin=0.7, lit=0.3, seed=5.0, bev=0.12, edge_filter=street)
    tk.ring_band("frieze", plan, 21.6, 22.3, 0.2, "terracotta")
    # cornice: proud on the street sides only (the NW side must stay clear of Matson)
    se = L([(X0 + 0.3, Y_SE - 0.8), (X1 + 0.8, Y_SE - 0.8), (X1 + 0.8, matson_face_y(X1) - 0.2),
            (X0 + 0.3, matson_face_y(X0) - 0.2)])
    tk.prism("cornice", se, 22.3, 23.0, "terracotta", bev=0.1)
    tk.prism("roof", tk.offset_poly(plan, -0.5), 22.8, 23.1, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), 23.0, H_TOP, 0.25, "cream")
    tk.hvac_cluster("plant", *P(-6.0, 0.0), 23.1, YAW, 12.0, 6.0, seed=4.0, hmax=H_TOP - 23.1 - 0.02,
                    fans=False)
    tk.prism("sidewalk", L([(X0, Y_SE - 2.5), (X1 + 2.5, Y_SE - 2.5), (X1 + 2.5, matson_face_y(X1 + 2.5) - 0.3),
                            (X0, matson_face_y(X0) - 0.3)]), 0.0, 0.12, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
