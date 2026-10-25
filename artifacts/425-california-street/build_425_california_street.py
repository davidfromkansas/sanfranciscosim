"""Deterministic Blender build of the SF-SIM miniature 425 California Street.

    blender -b --python build_425_california_street.py -- [--out DIR]

425 California Street (1967-68): a slender 27-storey office tower of black
glass on the south side of California between Sansome and Leidesdorff. Deep
black mullion fins run the full height and end in small gold caps at the
roofline; the base is a dark granite storey with glass storefronts. Helpers
in tools/landmark-kit/toykit.py.
"""

import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "425-california-street"
CENTER = (-122.4013729, 37.7928108)  # OSM way 260283289, OBB centre
H_TOP = 109.4                        # published 109.4 m (Wikipedia tallest list / CTBUH); LiDAR median 108.8
H_BASE = 6.6
N_FLOORS = 26                        # storeys above the base
H_ROOF = 105.6
PLAN = [(-14.3, 10.1), (10.8, 13.7), (14.3, -10.1), (-10.8, -13.7)]  # OSM, m about CENTER


def build():
    plan = tk.ccw(PLAN)
    # base: dark granite piers, glass storefronts, lit lobby
    tk.prism("base", tk.offset_poly(plan, -1.0), 0.0, H_BASE, "glassd")
    tk.pier_grid("base_piers", tk.offset_poly(plan, -1.0), 0.0, H_BASE, 5.0, 1.0, 1.0, "ink")
    tk.glow_ring("lobby", tk.offset_poly(plan, -1.0), 0.6, H_BASE - 1.4, 0.05, "sand_Glow")
    tk.prism("transfer", plan, H_BASE, H_BASE + 0.8, "ink", bev=0.1)
    # shaft: black glass, dark spandrels, full-height black fins
    pitch = (H_ROOF - H_BASE - 0.8) / N_FLOORS
    tk.shaft("shaft", plan, H_BASE + 0.8, H_ROOF, pitch, glass="glassd", band="ink", band_h=0.9,
             band_out=0.15, fins=(2.6, 0.45, 0.55, "ink"), lit=0.28, seed=4.25, lit_spacing=2.6)
    # gold caps on the fin tops (the photographed crown cue)
    tk.pier_grid("gold_caps", tk.offset_poly(plan, -0.2), H_ROOF - 2.2, H_ROOF, 2.6, 0.6, 0.85, "gold",
                 skip_short=2.3)
    tk.roof_kit("roof", plan, H_ROOF, seed=2.0, parapet=1.0, pmat="ink", plant_frac=0.4,
                yaw=tk.bearing_to_yaw(81.7))
    tk.glow_ring("crown_line", plan, H_ROOF - 1.6, H_ROOF - 0.6, 0.8, "gold_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
