"""Deterministic Blender build of the SF-SIM miniature Hearst Building.

    blender -b --python build_hearst_building.py -- [--out DIR]

The Hearst Building, 5 Third Street at Market and Kearny (1909, after the 1906
fire; entrance remodelled by Julia Morgan, 1937): the San Francisco Examiner's
twelve-storey Beaux-Arts office block. A pale terracotta frontage wraps three
faces of the five-way Market x Kearny x Third intersection, over a stone base
of tall arched openings, under an arcaded top storey and a deep cornice; light
courts open on the back. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "hearst-building"
CENTER = (-122.4030649, 37.7874126)   # OSM way 132127809, OBB centre
H_TOP = 50.2                           # DataSF 2010 LiDAR roof (majority 50.19 m); OSM height 49
H_BASE, H_SHAFT, H_ATTIC, H_ROOF = 8.0, 40.5, 46.6, 48.2
YAW = tk.bearing_to_yaw(45.6)         # local +x = NE along Market, +y = NW (Market St side)
# OSM footprint in that local frame (m); two light courts open to the east party wall
FOOT = [(15.6, 13.6), (15.6, 24.2), (-3.4, 24.1), (-15.5, 4.6), (-15.5, -10.3), (2.1, -10.4), (2.1, -24.3),
        (15.0, -24.3), (15.0, -14.4), (6.9, -14.3), (6.9, -8.3), (13.3, -8.3), (13.2, 4.5), (1.0, 4.5),
        (1.0, 9.4), (3.9, 13.6)]


def front(ei, p0, p1, nrm):
    """Street fronts: Market (NW), the corner face (W) and Third (SW); not the courts or party walls."""
    brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
    mx, my = (p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2
    lx, ly = tk.rot2((mx, my), -YAW)
    return 200 < brg < 330 and (ly > 20 or lx < -8)


def not_party(ei, p0, p1, nrm):
    """Everything but the east party walls (outward normal ~45 deg): fronts, rear and light courts."""
    brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
    return not 20 < brg < 70


def build():
    plan = tk.ccw(tk.xform(FOOT, YAW))
    # stone base with tall arched openings, warm lit at night
    tk.prism("base", plan, 0.0, H_BASE, "stone")
    tk.arched_panes("base_arches", plan, 0.4, H_BASE - 0.8, 4.4, 3.2, mat="glassd", edge_filter=front)
    tk.arched_panes("base_lit", plan, 0.6, H_BASE - 1.8, 4.4, 2.4, mat="sand_Glow", out=0.1, edge_filter=front,
                    suffix="_glow")
    tk.cornice("base_cornice", plan, H_BASE, h=0.9, out=0.5, mat="cream")
    # shaft: pale terracotta, punched windows on the street fronts only
    tk.punched_block("shaft", plan, H_BASE + 0.9, H_SHAFT, 3.95, wall="terracotta", win="glassd", spacing=2.9,
                     gap=1.0, margin=0.8, lit=0.25, seed=3.3, bev=0.0, edge_filter=not_party)
    # arcaded top storeys, deep cornice, parapet
    tk.ring_band("attic_band", plan, H_SHAFT, H_SHAFT + 0.6, 0.3, "cream")
    tk.prism("attic", plan, H_SHAFT + 0.6, H_ATTIC, "cream")
    tk.arched_panes("attic_arches", plan, H_SHAFT + 1.0, H_ATTIC - 0.4, 3.4, 2.4, mat="glassd", edge_filter=not_party)
    tk.arched_panes("attic_lit", plan, H_SHAFT + 1.3, H_ATTIC - 1.2, 3.4, 1.6, mat="sand_Glow", out=0.1,
                    edge_filter=front, suffix="_glow")
    tk.cornice("cornice", plan, H_ATTIC, h=1.6, out=1.2, mat="cream")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.3), H_ROOF, H_TOP, 0.3, "terracotta")
    tk.prism("roof", plan, H_ROOF - 0.2, H_ROOF + 0.1, "roofd")
    # roof: elevator house and a small plant over the corner wing
    c = tk.rot2((-6.0, 6.0), YAW)
    tk.box("lift_house", c[0], c[1], H_ROOF + 0.1, H_TOP - 0.3, 6.0, 5.0, "terracotta", yaw=YAW, bev=0.1)
    c = tk.rot2((8.0, -18.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.1, YAW, 9.0, 8.0, seed=5.5, hmax=1.5)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)
    p0, p1 = tk.xform([(-1.0, 26.5), (13.0, 26.5)], YAW)   # Market St trees
    tk.tree_row("trees", p0, p1, 0.25, 2, h=6.5, seed=7.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
