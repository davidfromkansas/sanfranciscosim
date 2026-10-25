"""Deterministic Blender build of the SF-SIM miniature 111 Pine Street.

    blender -b --python build_111_pine_street.py -- [--out DIR]

111 Pine Street (1963): a 19-storey office slab on the south side of Pine
between Front and Battery, beside One Front Street. A flat grey precast grid
of punched windows divided into tall bays by dark recessed piers, standing on
a polished red-brown granite base with arched bank entrances (First Republic
Bank), and finished by a slatted top storey. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "111-pine-street"
CENTER = (-122.3989068, 37.7921569)  # OSM way 148710880, OBB centre
H_TOP = 76.0                          # DataSF 2010 LiDAR roof (ring median/majority 76.0 m), measured
H_BASE = 8.0
H_SHAFT = 70.0                        # 17 office storeys of 3.65 m over the base
YAW = tk.bearing_to_yaw(81.3)
# OSM footprint about CENTER (the near-collinear 5th node dropped)
PLAN = [(-23.4, 10.5), (19.2, 17.0), (23.4, -10.5), (-19.2, -17.0)]


def build():
    plan = tk.ccw(PLAN)
    # base: polished red-brown granite with arched openings and a lit banking hall
    tk.prism("base", plan, 0.0, H_BASE, "granite", bev=0.12)
    tk.arched_panes("base_arches", plan, 0.4, 6.4, 7.2, 4.2, mat="glassd", out=0.06)
    tk.arched_panes("base_arches_lit", plan, 0.8, 5.8, 7.2, 3.2, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.ring_band("base_fascia", plan, H_BASE - 0.5, H_BASE, 0.3, "ink")
    # shaft: grey precast grid with punched windows
    tk.punched_block("shaft", plan, H_BASE, H_SHAFT, 3.65, wall="concrete", win="glassd", spacing=2.4,
                     gap=0.9, margin=0.7, lit=0.3, seed=11.0, bev=0.1)
    # dark recessed piers between the bays (six bays on the long faces)
    tk.pier_grid("piers", plan, H_BASE, H_SHAFT, 7.2, 0.9, 0.08, "ink", skip_short=6.0)
    # slatted top storey and flat roof
    tk.prism("top", tk.offset_poly(plan, -0.3), H_SHAFT, H_TOP - 2.2, "concrete")
    tk.pier_grid("louvres", tk.offset_poly(plan, -0.3), H_SHAFT + 0.4, H_TOP - 2.6, 2.4, 0.4, 0.25, "steel",
                 skip_short=6.0)
    tk.ring_band("coping", plan, H_TOP - 2.2, H_TOP - 1.5, 0.15, "concrete")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.5), H_TOP - 2.2, H_TOP - 1.9, "roofd")
    tk.hvac_cluster("plant", 0.0, 0.0, H_TOP - 1.9, YAW, 26.0, 14.0, seed=5.0, hmax=1.9)
    tk.glow_ring("crown_line", plan, H_SHAFT + 0.6, H_SHAFT + 1.2, 0.35, "white_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
