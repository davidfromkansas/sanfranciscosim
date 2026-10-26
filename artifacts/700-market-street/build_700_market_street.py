"""Deterministic Blender build of the SF-SIM miniature Mutual Savings Bank Building.

    blender -b --python build_700_market_street.py -- [--out DIR]

700 Market Street at Kearny and Geary (William Curlett, 1902; NRHP 2014): a
slim 12-storey French Renaissance Revival tower, grey stone on all street
fronts - an arched two-storey base, a three-bay shaft, an arcaded top storey
under a deep cornice and balustrade - capped by a red-tile mansard with a
pedimented oculus dormer and green cresting. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "700-market-street"
CENTER = (-122.4038104, 37.7877247)   # OSM way 149335987, OBB centre
H_TOP = 57.9                          # MEASURED: LiDAR max 57.93 m (mansard cresting); median 47.7 = balustrade
PLAN = [(11.7, -0.9), (0.1, -12.4), (-11.7, -0.3), (-13.1, 10.4), (9.6, 13.8)]   # OSM, m from CENTER


def market(ei, p0, p1, nrm):
    """The SE face on Market Street (the photographed front)."""
    return nrm[0] > 0.5 and nrm[1] < -0.5


def build():
    plan = tk.ccw(PLAN)
    # arched two-storey base (rusticated stone)
    tk.prism("base", plan, 0.0, 12.0, "concrete", bev=0.15)
    tk.arched_panes("base_arches", plan, 0.4, 10.6, 5.4, 3.6, mat="glassd")
    tk.arched_panes("base_lit", plan, 0.6, 8.8, 5.4, 2.6, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.ring_band("belt", plan, 12.0, 12.8, 0.35, "trim")
    # three-bay shaft, eight storeys of punched paired windows
    tk.punched_block("shaft", plan, 12.8, 40.4, 3.45, wall="concrete", win="glassd", spacing=2.7, gap=1.0,
                     margin=0.7, lit=0.3, seed=4.0, bev=0.12)
    tk.cornice("mid_cornice", plan, 40.4, h=0.9, out=0.8, mat="trim")
    # arcaded top storey and the deep main cornice + balustrade
    tk.prism("attic", plan, 41.3, 45.6, "concrete", bev=0.1)
    tk.arched_panes("attic_arches", plan, 41.8, 45.2, 5.4, 3.4, mat="glassd")
    tk.arched_panes("attic_lit", plan, 42.0, 44.6, 5.4, 2.4, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("cornice", plan, 45.6, h=1.3, out=1.3, mat="trim")
    tk.ring_band("balustrade", tk.offset_poly(plan, 0.3), 46.9, 47.7, 0.4, "stone")
    tk.prism("terrace", tk.offset_poly(plan, 0.2), 46.6, 47.0, "roofd")
    # red-tile mansard with flat top, green cresting
    inner = tk.offset_poly(plan, -1.0)
    top = tk.offset_poly(plan, -5.2)
    tk.frustum("mansard", inner, 47.0, top, 55.8, "coral")
    tk.prism("mansard_top", top, 55.6, 56.0, "roofd")
    tk.ring_band("cresting", tk.offset_poly(top, -0.3), 56.0, H_TOP, 0.3, "verdigris")
    # pedimented oculus dormer on the Market face
    for p0, p1, L, nrm in tk.edges(plan):
        if not market(0, p0, p1, nrm):
            continue
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        yaw = math.atan2(uy, ux)
        c = (p0[0] + ux * L / 2 - nrm[0] * 1.6, p0[1] + uy * L / 2 - nrm[1] * 1.6)
        tk.box("dormer", c[0], c[1], 47.0, 54.2, 5.0, 4.4, "stone", yaw=yaw, bev=0.1)
        tk.prism("dormer_pediment", tk.xform(tk.rect(5.8, 4.8), yaw, c[0], c[1]), 54.2, 54.9, "trim")
        dr = tk.xform(tk.rect(5.0, 4.4), yaw, c[0], c[1])
        face = lambda ei, q0, q1, nn: nn[0] * nrm[0] + nn[1] * nrm[1] > 0.9  # noqa: E731
        tk.panes("dormer_win", dr, [(47.6, 51.0)], 2.4, mat="glassd", gap=0.7, margin=0.2, edge_filter=face)
        tk.lit_windows("dormer_lit", dr, [(47.6, 51.0)], 2.4, 1.01, out=0.1, margin=0.5, gap=1.1, edge_filter=face)
        tk.arched_panes("oculus", dr, 51.6, 53.6, 5.0, 1.8, mat="glassd", edge_filter=face)
    tk.prism("sidewalk", tk.offset_poly(plan, 2.5), 0.0, 0.2, "stone")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
