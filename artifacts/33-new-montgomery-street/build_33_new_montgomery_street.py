"""Deterministic Blender build of the SF-SIM miniature 33 New Montgomery.

    blender -b --python build_33_new_montgomery_street.py -- [--out DIR]

33 New Montgomery Street: a 20-storey office tower on an L-shaped lot just off
Market Street beside the Palace Hotel. DataSF LiDAR puts the main roof at 80 m with
a smaller element rising to about 102 m; no usable photograph was obtained, so the
skin (granite with punched windows) and the position of the taller corner element
are modelled from the LiDAR statistics and the footprint, and are flagged as
inferred in REFERENCE.md. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "33-new-montgomery-street"
CENTER = (-122.4015151, 37.7886476)  # OSM way 79377223, OBB centre
H_TOP = 101.8                         # DataSF 2010 LiDAR max 101.80 m (measured crest)
H_ROOF = 80.0                         # main roof: LiDAR majority plane 79.98 m (OSM height=80, 20 levels)
H_BASE = 7.0
YAW = math.radians(90 - 45.8)         # local +x along the Market-parallel grid (bearing 45.8)
# OSM way 79377223 in metres about CENTER (+x east, +y north)
PTS = [(-4.21, 31.51), (14.39, 12.67), (14.98, 12.07), (10.85, 8.04), (27.51, -8.85), (4.07, -31.65),
       (-9.87, -17.18), (2.26, -5.46), (-19.4, 16.63)]
CORNER = PTS[4]                       # outer corner of the L (east)


def build():
    plan = tk.ccw(PTS)
    tk.prism("base", plan, 0.0, H_BASE, "granite", bev=0.15)
    tk.panes("base_glass", plan, [(0.3, H_BASE - 1.2)], 4.5, mat="glassd", gap=1.0, margin=0.0)
    tk.lit_windows("base_lit", plan, [(0.3, H_BASE - 1.6)], 4.5, 0.85, seed=1.0, out=0.1, margin=0.3, gap=1.4)
    tk.ring_band("base_band", plan, H_BASE, H_BASE + 0.8, 0.3, "stone")
    # shaft: granite with punched windows; 18 storeys of 4.0 m
    tk.punched_block("shaft", plan, H_BASE + 0.8, H_ROOF, (H_ROOF - H_BASE - 0.8) / 18, wall="granite",
                     win="glassd", spacing=3.6, gap=1.4, margin=0.9, lit=0.3, seed=4.0, bev=0.12)
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), H_ROOF, H_ROOF + 1.4, 0.6, "stone")
    tk.prism("roof", tk.offset_poly(plan, -0.3), H_ROOF - 0.3, H_ROOF + 0.05, "roofd")
    tk.hvac_cluster("roof_plant", -2.0, 12.0, H_ROOF + 0.05, YAW, 10.0, 12.0, seed=2.0, hmax=3.0)
    # the taller element at the L's outer corner (position inferred): 12 m square to the crest
    a = (PTS[3][0] - CORNER[0], PTS[3][1] - CORNER[1])
    b = (PTS[5][0] - CORNER[0], PTS[5][1] - CORNER[1])
    la, lb = math.hypot(*a), math.hypot(*b)
    cx = CORNER[0] + a[0] / la * 7.0 + b[0] / lb * 7.0
    cy = CORNER[1] + a[1] / la * 7.0 + b[1] / lb * 7.0
    tw = tk.xform(tk.rect(12.0, 12.0), YAW, cx, cy)
    tk.punched_block("tower", tw, H_ROOF + 0.05, H_TOP - 3.0, (H_TOP - 3.0 - H_ROOF - 0.05) / 5, wall="granite",
                     win="glassd", spacing=3.0, gap=1.0, margin=0.9, lit=0.35, seed=8.0, bev=0.12)
    tk.ring_band("tower_cap", tw, H_TOP - 3.0, H_TOP, 0.4, "stone")
    tk.prism("tower_roof", tk.offset_poly(tw, -0.2), H_TOP - 3.3, H_TOP - 2.95, "roofd")
    tk.glow_ring("tower_light", tw, H_TOP - 2.2, H_TOP - 1.2, 0.46, "white_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
