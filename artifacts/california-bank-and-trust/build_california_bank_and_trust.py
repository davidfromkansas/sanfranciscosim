"""Deterministic Blender build of the SF-SIM miniature Merchants Exchange Building.

    blender -b --python build_california_bank_and_trust.py -- [--out DIR]

Merchants Exchange Building, 465 California Street (D. H. Burnham & Co. /
Willis Polk, 1903-04; California Bank & Trust occupies the ground-floor
banking hall, hence the slug). Fifteen storeys of pale granite and terracotta:
a two-storey base whose California Street entrance is a deep portal framed by
two giant Ionic columns under the carved name, a plain punched shaft, and a
heavy top cornice over an attic storey. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "california-bank-and-trust"
CENTER = (-122.402149, 37.7925677)   # OSM way 256067740, OBB centre
H_TOP = 59.4                          # published roof 195 ft (Wikipedia infobox); LiDAR roof majority 60.4 m
H_BASE = 10.0
H_SHAFT = 52.0
PLAN = [(-22.4, 24.0), (13.7, 29.8), (20.6, -14.0), (22.2, -23.9), (12.1, -25.7), (3.2, -26.9),
        (-13.8, -29.5), (-15.3, -19.5), (-20.1, 9.8)]  # OSM, m about CENTER


def front_edge(plan):
    """The California Street (north-facing) edge."""
    return max(tk.edges(plan), key=lambda e: e[3][1])


def build():
    plan = tk.ccw(PLAN)
    p0, p1, L, n = front_edge(plan)
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    on_front = lambda ei, a, b, nrm: nrm[1] > 0.9  # noqa: E731
    off_front = lambda ei, a, b, nrm: nrm[1] <= 0.9  # noqa: E731
    # base: two storeys of granite with tall windows; banking hall lit at night
    tk.prism("base", plan, 0.0, H_BASE, "stone", bev=0.15)
    tk.panes("base_win", plan, [(0.8, 8.6)], 4.4, mat="glassd", gap=1.6, margin=0.3, edge_filter=off_front)
    tk.lit_windows("base_lit", plan, [(0.8, 8.6)], 4.4, 0.5, seed=3.0, out=0.1, margin=0.6, gap=1.9,
                   edge_filter=off_front)
    # California St portal: recessed glass bay between two giant Ionic columns
    mid = L / 2
    bay = 11.0
    a = (p0[0] + ux * (mid - bay / 2), p0[1] + uy * (mid - bay / 2))
    b = (p0[0] + ux * (mid + bay / 2), p0[1] + uy * (mid + bay / 2))
    tk.flat_quad("portal_panes", a, b, 0.0, 8.6, 0.04, "glassd", n)
    tk.flat_quad("portal_glow", a, b, 0.4, 7.6, 0.08, "sand_Glow", n)
    for k, t in enumerate((mid - 3.0, mid + 3.0)):
        cx = p0[0] + ux * t + n[0] * 1.5
        cy = p0[1] + uy * t + n[1] * 1.5
        tk.cylinder(f"column_{k}", cx, cy, 0.0, 8.4, 1.0, "white", seg=10)
        tk.box(f"capital_{k}", cx, cy, 8.4, 9.2, 2.6, 2.6, "white", yaw=math.atan2(uy, ux))
    # flanking bays of the front: tall windows either side of the portal
    for k, (t0, t1) in enumerate(((1.5, mid - bay / 2 - 1.2), (mid + bay / 2 + 1.2, L - 1.5))):
        a = (p0[0] + ux * t0, p0[1] + uy * t0)
        b = (p0[0] + ux * t1, p0[1] + uy * t1)
        tk.flat_quad(f"front_win_{k}_panes", a, b, 1.0, 8.2, 0.05, "glassd", n)
        tk.flat_quad(f"front_win_{k}_glow", a, b, 3.0, 7.6, 0.09, "sand_Glow", n)
    tk.cornice("base_cornice", plan, H_BASE, h=1.0, out=0.6, mat="white")
    # shaft: pale stone with punched windows
    tk.punched_block("shaft", plan, H_BASE + 1.0, H_SHAFT, 3.42, wall="stone", win="glassd", spacing=4.2,
                     gap=1.4, margin=0.9, lit=0.3, seed=7.0, bev=0.12)
    # crown: band, attic storey, heavy cornice
    tk.ring_band("crown_band", plan, H_SHAFT - 0.4, H_SHAFT + 0.3, 0.25, "white")
    tk.punched_block("attic", plan, H_SHAFT + 0.3, 56.6, 4.3, wall="stone", win="glassd", spacing=4.2,
                     gap=1.6, margin=1.0, lit=0.35, seed=8.0, bev=0.1)
    tk.cornice("top_cornice", plan, 56.6, h=1.6, out=1.3, mat="white")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.3), 58.2, H_TOP, 0.35, "stone")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.4), 57.9, 58.3, "roofd")
    tk.hvac_cluster("plant", 0.0, 0.0, 58.3, tk.bearing_to_yaw(80.8), 14.0, 22.0, seed=2.0, hmax=1.1, fans=False)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
