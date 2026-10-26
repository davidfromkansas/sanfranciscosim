"""Deterministic Blender build of the SF-SIM miniature Rincon Center (Rincon Annex).

    blender -b --python build_rincon_annex.py -- [--out DIR]

The 1940 Rincon Annex post office (Gilbert Stanley Underwood), the historic
half of Rincon Center: a three-storey Streamline Moderne block in white
plaster on a blue-grey base, with tall two-storey windows, rows of blue
dolphin reliefs over the openings, and the Rincon Center atrium skylight
rising behind. Its residential half, The Towers at Rincon, is already a
landmark (`towers-at-rincon`). Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "rincon-annex"
CENTER = (-122.3931459, 37.7925002)  # OSM way 44106213, OBB centre
H_TOP = 29.7                         # DataSF LiDAR crest 29.74 m: the atrium skylight
H_PARAPET = 18.1                     # LiDAR majority roof plane 18.08 m
H_BASE = 2.4
# OSM way 44106213, metres east/north of CENTER (simplified: tiny jogs dropped)
PLAN = [(-2.3, 61.6), (59.6, -3.3), (43.7, -19.3), (34.5, -25.0), (25.3, -39.2), (16.7, -43.1),
        (2.0, -60.4), (-61.5, 3.9)]
YAW = math.radians(45.7)


def build():
    p = tk.ccw(PLAN)
    tk.prism("base", tk.offset_poly(p, 0.25), 0.0, H_BASE, "glassl", bev=0.12)   # blue-grey plinth
    tk.prism("body", p, H_BASE, H_PARAPET - 1.2, "white", bev=0.2)
    # tall two-storey windows, then a row of square upper windows
    tk.panes("tall_win", p, [(H_BASE + 0.6, 11.0)], 6.5, mat="ink", gap=3.2, margin=0.0)
    tk.lit_windows("tall_lit", p, [(H_BASE + 0.6, 11.0)], 6.5, 0.6, seed=2.0, out=0.1, margin=0.6, gap=3.8)
    tk.panes("upper_win", p, [(12.4, 15.2)], 6.5, mat="ink", gap=4.2, margin=0.0)
    # the dolphin friezes: blue relief panels over each tall window
    tk.lit_windows("dolphins", p, [(10.9, 12.3)], 6.5, 1.01, out=0.12, margin=0.0, mat="sky", gap=3.0,
                   suffix="_panes")
    tk.ring_band("cornice", p, H_PARAPET - 1.2, H_PARAPET, 0.35, "glassl")
    tk.prism("roof", tk.offset_poly(p, -0.6), H_PARAPET - 1.4, H_PARAPET - 1.0, "roofd")
    # the Rincon Center atrium skylight behind (toward the towers, SE side)
    c = tk.rot2((0.0, -14.0), YAW)
    sky = tk.xform(tk.rect(34.0, 22.0), YAW, *c)
    tk.prism("atrium_drum", sky, H_PARAPET - 1.0, 23.5, "white", bev=0.15)
    tk.pyramid("atrium_roof", tk.offset_poly(sky, -0.3), 23.5, H_TOP, "glassl")
    tk.glow_ring("atrium_lit", sky, 19.0, 23.0, 0.06, "sand_Glow")
    tk.hvac_cluster("plant", *tk.rot2((0.0, 16.0), YAW), H_PARAPET - 1.0, YAW, 26.0, 14.0, seed=5.0, hmax=3.5)
    # sawtooth of long roof skylights over the old sorting floor
    for k, off in enumerate((-30.0, -18.0, 22.0, 32.0)):
        c2 = tk.rot2((off, 6.0), YAW)
        tk.box(f"skylight_{k}", c2[0], c2[1], H_PARAPET - 1.0, H_PARAPET + 0.6, 4.0, 40.0, "glassl",
               yaw=YAW, bev=0.15)
    tk.plinth("sidewalk", p, h=0.25, out=3.0)
    a, b = tk.xform([(-34.0, 48.5), (34.0, 48.5)], YAW)   # Mission St sidewalk (NW face at y~45-47)
    tk.tree_row("mission_trees", a, b, 0.25, 5, h=6.0, seed=6.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
