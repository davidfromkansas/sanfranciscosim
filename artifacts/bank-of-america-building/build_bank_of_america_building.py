"""Deterministic Blender build of the SF-SIM miniature 625 Market Street
("Bank of America Building" in OSM).

    blender -b --python build_bank_of_america_building.py -- [--out DIR]

625-631 Market Street at the corner of New Montgomery (1907; 15 storeys,
SF Assessor): a narrow post-fire office tower, three bays on Market and six
down New Montgomery, its back and east side built against 33 New Montgomery.
No photograph or description could be retrieved, so the treatment is the
period's standard: a two-storey stone base with shopfronts, a pale brick shaft
of paired punched windows, an attic storey under a projecting cornice.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "bank-of-america-building"
CENTER = (-122.4016814, 37.7886452)   # OSM way 941649434, OBB centre
H_TOP = 60.1                           # DataSF 2010 LiDAR roof (majority 60.11 m); no published height
H_BASE, H_SHAFT, H_ATTIC, H_ROOF = 9.0, 53.0, 57.2, 58.8
L, W = 30.9, 16.9                     # OSM OBB; local +x = bearing 135.6 (down New Montgomery, SE)
YAW = tk.bearing_to_yaw(135.6)


def street(ei, p0, p1, nrm):
    """Market (local -x, NW) and New Montgomery (local -y, SW); +x and +y abut 33 New Montgomery."""
    lx, ly = tk.rot2(nrm, -YAW)
    return lx < -0.5 or ly < -0.5


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    tk.prism("base", plan, 0.0, H_BASE, "stone", bev=0.12)
    tk.panes("shops", plan, [(0.3, 4.6)], 4.2, mat="glassd", margin=0.0, gap=0.9, edge_filter=street)
    tk.lit_windows("shops_lit", plan, [(0.3, 4.6)], 4.2, 0.95, seed=1.0, out=0.1, margin=0.3, gap=1.1,
                   edge_filter=street)
    tk.panes("mezz", plan, [(5.0, H_BASE - 0.4)], 2.1, mat="glassd", margin=0.6, gap=0.7, edge_filter=street)
    tk.cornice("base_cornice", plan, H_BASE, h=0.8, out=0.5, mat="cream")
    tk.punched_block("shaft", plan, H_BASE + 0.8, H_SHAFT, 3.85, wall="sand", win="glassd", spacing=2.1,
                     gap=0.8, margin=0.85, lit=0.3, seed=7.0, bev=0.1, edge_filter=street)
    tk.ring_band("attic_band", plan, H_SHAFT, H_SHAFT + 0.6, 0.3, "cream")
    tk.punched_block("attic", plan, H_SHAFT + 0.6, H_ATTIC, 3.6, wall="cream", win="glassd", spacing=2.1,
                     gap=1.2, margin=0.8, lit=0.4, seed=9.0, bev=0.1, edge_filter=street)
    tk.cornice("cornice", plan, H_ATTIC, h=1.6, out=1.2, mat="cream")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.3), H_ROOF, H_TOP, 0.3, "sand")
    tk.prism("roof", plan, H_ROOF - 0.2, H_ROOF + 0.1, "roofd")
    c = tk.rot2((4.0, 2.0), YAW)
    tk.box("lift_house", c[0], c[1], H_ROOF + 0.1, H_TOP - 0.2, 5.0, 4.0, "sand", yaw=YAW, bev=0.1)
    c = tk.rot2((-6.0, 0.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.1, YAW, 8.0, 7.0, seed=3.0, hmax=1.2)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)
    p0, p1 = tk.xform([(-L / 2 + 3.0, -W / 2 - 2.0), (L / 2 - 3.0, -W / 2 - 2.0)], YAW)   # New Montgomery trees
    tk.tree_row("trees", p0, p1, 0.25, 3, h=6.0, seed=4.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
