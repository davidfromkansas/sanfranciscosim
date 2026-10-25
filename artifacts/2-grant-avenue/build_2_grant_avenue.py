"""Deterministic Blender build of the SF-SIM miniature Union Trust Bank Building.

    blender -b --python build_2_grant_avenue.py -- [--out DIR]

The Union Trust Bank Building, 2 Grant Avenue at Market and O'Farrell (1910;
now a Wells Fargo branch): a granite neoclassical banking temple, two very tall
storeys high, with a giant-order colonnade along Grant Avenue that wraps the
rounded Market Street corner, a heavy entablature and a plain attic over a
skylit banking hall. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "2-grant-avenue"
CENTER = (-122.4046777, 37.7871346)   # OSM way 149335980, OBB centre
H_TOP = 19.5                           # DataSF 2010 LiDAR roof (majority 19.51 m); OSM height 20
H_COL, H_ENT, H_ATTIC = 15.6, 17.8, 19.5
YAW = tk.bearing_to_yaw(80.8)         # local +x = east (O'Farrell axis), +y = north along Grant Ave
# OSM footprint in that local frame (m): Grant on the west, rounded Market corner to the SE
FOOT = [(-11.5, 18.8), (-11.5, -17.8), (-9.7, -18.8), (-1.6, -18.7), (2.1, -17.9), (5.2, -16.2), (9.3, -13.7),
        (11.5, -11.9), (5.3, 14.5), (4.4, 18.5)]


def street(ei, p0, p1, nrm):
    """Grant (W), O'Farrell (S) and the rounded Market corner (SE); not the two party walls."""
    lx, ly = tk.rot2(nrm, -YAW)
    return lx < -0.9 or ly < -0.5


def build():
    plan = tk.ccw(tk.xform(FOOT, YAW))
    tk.prism("steps", tk.offset_poly(plan, 0.8), 0.0, 0.9, "stone")
    tk.prism("hall", plan, 0.9, H_ENT, "stone", bev=0.12)
    # tall windows between the columns, lit like a banking hall at night
    tk.panes("windows", plan, [(1.6, H_COL - 1.2)], 4.4, mat="glassd", margin=0.0, gap=1.9, edge_filter=street)
    tk.lit_windows("windows_lit", plan, [(1.6, H_COL - 1.2)], 4.4, 0.9, seed=2.0, out=0.1, margin=0.4, gap=2.2,
                   edge_filter=street)
    # the giant colonnade standing proud of the wall, a column at every window pier
    cols = []
    for k, (p0, p1, L, nrm) in enumerate(tk.edges(plan)):
        if not street(k, p0, p1, nrm) or L < 3.0:
            continue
        cnt = max(1, int(round(L / 4.4)))
        step = L / cnt
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        for i in range(cnt + 1):
            if i == 0 and k > 0:
                continue  # shared with the previous edge's last column
            t = i * step
            cx, cy = p0[0] + ux * t + nrm[0] * 1.3, p0[1] + uy * t + nrm[1] * 1.3
            cols.append(tk.cylinder(f"col_{k}_{i}", cx, cy, 0.9, H_COL, 0.65, "white", seg=8))
            cols.append(tk.box(f"cap_{k}_{i}", cx, cy, H_COL - 0.6, H_COL, 1.7, 1.7, "stone",
                               yaw=math.atan2(uy, ux)))
    tk.join(cols, "colonnade")
    # entablature carried out over the columns, attic, skylit banking-hall roof
    tk.prism("entablature", tk.offset_poly(plan, 2.1), H_COL, H_ENT, "stone", bev=0.12)
    tk.ring_band("attic", tk.offset_poly(plan, 0.6), H_ENT, H_ATTIC, 0.3, "stone")
    tk.prism("roof", tk.offset_poly(plan, 0.6), H_ENT - 0.2, H_ENT + 0.2, "roofd")
    sky = tk.xform(tk.rect(9.0, 18.0, -3.0, 0.0), YAW)
    tk.prism("skylight", sky, H_ENT + 0.2, H_ENT + 1.0, "glassl")
    tk.glow_cap("skylight_lit", tk.offset_poly(sky, -0.4), H_ENT + 1.05, "sand_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=3.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
