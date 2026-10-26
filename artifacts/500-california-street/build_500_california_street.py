"""Deterministic Blender build of the SF-SIM miniature Omni San Francisco Hotel.

    blender -b --python build_500_california_street.py -- [--out DIR]

Omni San Francisco Hotel, formerly the Financial Center Building, 500
California Street at Montgomery (Frederick H. Meyer and Albin R. Johnson,
1926-27; hotel conversion and raised roof 2001-02). A Florentine Renaissance
block: five storeys of rusticated tan cast stone with a run of round-arched
openings and a big arched entrance, a red-brick shaft of punched windows,
and a top storey of arched windows under a corbelled cornice. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "500-california-street"
CENTER = (-122.4031981, 37.7931212)  # OSM way 1279459281, OBB centre
H_TOP = 65.3                          # LiDAR crest 65.3 m (batch facts file); DataSF ring majority 61.7 / max 68.3
H_BASE = 20.0                         # five storeys of rusticated cast stone
H_SHAFT = 54.0
H_ARCH = 59.6
H_ROOF = 62.0
YAW = tk.bearing_to_yaw(171.1)
# OSM footprint about CENTER, collinear nodes dropped
PLAN = [(17.6, 24.3), (-24.2, 17.7), (-17.5, -24.2), (24.2, -17.7)]


def build():
    plan = tk.ccw(PLAN)
    # base: rusticated cast stone, arched ground storey, punched windows above
    tk.prism("base", plan, 0.0, H_BASE, "terracotta", bev=0.15)
    tk.arched_panes("arcade", plan, 0.3, 7.6, 5.2, 3.6, mat="glassd", out=0.06)
    tk.arched_panes("arcade_lit", plan, 0.6, 6.8, 5.2, 2.8, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.panes("base_win", plan, [(8.6, 12.4), (12.4, 16.2)], 3.4, mat="glassd", gap=1.6, margin=0.7)
    tk.ring_band("base_band", plan, 16.4, 17.0, 0.2, "terracotta")
    tk.panes("base_win2", plan, [(17.0, 20.0)], 3.4, mat="glassd", gap=1.6, margin=0.6)
    tk.cornice("base_cornice", plan, H_BASE, h=1.0, out=0.6, mat="terracotta")
    # shaft: red brick with punched windows
    tk.punched_block("shaft", plan, H_BASE + 1.0, H_SHAFT, 3.3, wall="rust", win="glassd", spacing=3.0,
                     gap=1.4, margin=0.8, lit=0.32, seed=4.0, bev=0.12)
    # top storey: arched windows in a cast-stone band, corbelled cornice
    tk.ring_band("arch_band_base", plan, H_SHAFT - 0.3, H_SHAFT + 0.3, 0.2, "terracotta")
    tk.prism("arch_storey", plan, H_SHAFT + 0.3, H_ARCH, "rust", bev=0.1)
    tk.arched_panes("arches", plan, H_SHAFT + 0.9, H_ARCH - 0.4, 3.0, 1.8, mat="glassd", out=0.06)
    tk.arched_panes("arches_lit", plan, H_SHAFT + 1.2, H_ARCH - 0.8, 3.0, 1.2, mat="sand_Glow", out=0.1,
                    suffix="_glow")
    tk.cornice("crown_cornice", plan, H_ARCH, h=H_ROOF - H_ARCH, out=1.3, mat="terracotta")
    # 2002 raised roof: set-back penthouse storey, plant
    pent = tk.offset_poly(plan, -3.0)
    tk.prism("roof_deck", tk.offset_poly(plan, -0.4), H_ROOF - 0.3, H_ROOF + 0.1, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), H_ROOF, H_ROOF + 0.8, 0.4, "terracotta")
    tk.punched_block("penthouse", pent, H_ROOF, H_TOP - 0.8, 2.5, wall="stone", win="glassd", spacing=3.0,
                     gap=1.2, margin=0.5, lit=0.4, seed=6.0, bev=0.08)
    tk.prism("pent_roof", pent, H_TOP - 0.8, H_TOP - 0.5, "roofd")
    tk.hvac_cluster("plant", 0.0, 0.0, H_TOP - 0.5, YAW, 14.0, 10.0, seed=2.0, hmax=0.5, fans=False)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)
    # lollipop trees along California (S face), per the photo
    p0, p1 = tk.xform([(-19.0, -23.4), (19.0, -18.0)], 0.0)
    nx, ny = 0.15, -0.99
    tk.tree_row("trees", (p0[0] + nx * 1.8, p0[1] + ny * 1.8), (p1[0] + nx * 1.8, p1[1] + ny * 1.8), 0.25, 3,
                h=3.2, r=1.0, seed=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
