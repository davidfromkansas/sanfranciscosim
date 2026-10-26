"""Deterministic Blender build of the SF-SIM miniature Folger Coffee Company Building.

    blender -b --python build_folger_coffee_building.py -- [--out DIR]

101 Howard Street at Spear (Henry A. Schulze, 1904; NRHP 1996): J. A.
Folger & Company's five-storey Renaissance Revival headquarters, which
survived both 1906 and 1989 on wooden piles in bay fill. Red-brown brick all
over: a ground storey of round-arched openings, a band course, three storeys
of tall windows between brick piers, a top-floor arcade of round-headed
windows, and a deep corbelled brick cornice. Helpers in
tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "folger-coffee-building"
CENTER = (-122.3925976, 37.7909315)  # OSM way 192305909, OBB centre
H_TOP = 26.74                         # facts-file LiDAR peak (stair bulkhead); roof 24.6 = ring majority (measured)
YAW = tk.bearing_to_yaw(45.4)         # local +x = NE along Howard St, +y = NW
W, D = 42.9, 28.4                     # OSM OBB


def build():
    plan = tk.xform(tk.rect(W, D), YAW)
    tk.prism("body", plan, 0.0, 23.4, "brick", bev=0.15)
    # ground storey: round arches, lit shopfronts
    tk.arched_panes("arches", plan, 0.4, 5.2, 4.3, 3.2, mat="glassd")
    tk.arched_panes("arches_lit", plan, 0.6, 4.2, 4.3, 2.4, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.ring_band("band", plan, 5.6, 6.3, 0.3, "stone")
    # three storeys between brick piers, 4.3 m bays
    tk.pier_grid("piers", plan, 6.3, 19.6, 4.3, 0.9, 0.35, "rust", skip_short=8.0)
    bands = tk.floors(6.3, 19.6, 4.43)
    tk.panes("win", plan, bands, 4.3, mat="glassd", gap=1.9, margin=0.6)
    tk.lit_windows("win_lit", plan, bands, 4.3, 0.35, seed=3.0, out=0.1, margin=0.8, gap=2.2)
    tk.ring_band("sill", plan, 19.6, 20.0, 0.25, "rust")
    # top-floor arcade of round-headed windows (two per bay)
    tk.arched_panes("arcade", plan, 20.4, 23.0, 2.15, 1.2, mat="glassd")
    tk.lit_windows("arcade_lit", plan, [(20.6, 22.4)], 2.15, 0.4, seed=8.0, out=0.1, margin=0.0, gap=1.35)
    # corbelled brick cornice and parapet
    tk.cornice("cornice", plan, 23.4, h=1.5, out=0.9, mat="rust")
    tk.ring_band("parapet", plan, 24.9, 25.6, 0.2, "brick")
    tk.prism("roof", tk.offset_poly(plan, -0.3), 24.6, 25.0, "roofd")
    c = tk.rot2((-10.0, 6.0), YAW)
    tk.box("bulkhead", c[0], c[1], 25.0, H_TOP, 4.0, 5.0, "brick", yaw=YAW, bev=0.1)
    tk.hvac_cluster("plant", *tk.rot2((6.0, -2.0), YAW), 25.0, YAW, 12.0, 8.0, seed=5.0, hmax=1.6, fans=False)
    tk.prism("sidewalk", tk.offset_poly(plan, 2.5), 0.0, 0.15, "concrete")
    for i, x in enumerate((-16.0, -8.0, 0.0, 8.0, 16.0)):  # the clipped street trees on Howard
        p = tk.rot2((x, -D / 2 - 1.6), YAW)
        tk.tree(f"tree{i}", p[0], p[1], 0.15, h=5.5, r=1.8, mat="leaf")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
