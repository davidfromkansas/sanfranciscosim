"""Deterministic Blender build of the SF-SIM miniature PG&E General Office Annex.

    blender -b --python build_pge_annex.py -- [--out DIR]

The 1945 annex of the PG&E General Office Building (Bakewell & Brown's
245 Market Street, 1923-25), built behind it on Beale Street and designed to
match: the same cream terracotta, an arcaded base, a plain punched shaft, a
terracotta cornice and a set-back attic. It shares a party wall with the
general office (artifacts/pge-general-office/), whose style, palette and
storey pitch this build copies. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "pge-annex"
CENTER = (-122.3965063, 37.7921155)  # OSM way 260291406, OBB centre
H_TOP = 55.8                          # DataSF 2010 LiDAR max of ring 201006.0003729 (measured)
H_BASE = 9.0
H_SHAFT = 48.6
YAW = tk.bearing_to_yaw(45.0)
# OSM footprint about CENTER; its four extra nodes are collinear and dropped
PLAN = [(-29.4, -0.5), (0.3, 29.2), (29.4, 0.5), (-0.3, -29.2)]


def outside(ei, p0, p1, n):
    """Skip the NW party wall shared with the 1925 general office."""
    return not (n[0] < -0.5 and n[1] > 0.5)


def build():
    plan = tk.ccw(PLAN)
    # base: terracotta, arcaded like the general office
    tk.prism("base", plan, 0.0, H_BASE, "terracotta", bev=0.2)
    tk.arched_panes("arcade", plan, 0.6, H_BASE - 1.4, 5.4, 3.4, mat="glassd", out=0.06, edge_filter=outside)
    tk.lit_windows("arcade_lit", plan, [(0.6, H_BASE - 3.0)], 5.4, 0.8, seed=2.0, out=0.1, margin=0.4,
                   gap=2.6, edge_filter=outside)
    tk.cornice("base_cornice", plan, H_BASE, h=0.9, out=0.5, mat="cream")
    # shaft: cream terracotta, punched windows (general office pitch 3.9 m, spacing 2.9 m)
    tk.punched_block("shaft", plan, H_BASE + 0.9, H_SHAFT, 3.87, wall="cream", win="glassd", spacing=2.9,
                     gap=1.3, margin=0.9, lit=0.3, seed=6.0, bev=0.15, edge_filter=outside)
    # crown: terracotta cornice, set-back attic storey, plant
    tk.cornice("crown_cornice", plan, H_SHAFT, h=1.4, out=0.9, mat="terracotta")
    attic = tk.offset_poly(plan, -2.0)
    tk.punched_block("attic", attic, H_SHAFT + 1.4, 53.6, 4.2, wall="cream", win="glassd", spacing=2.9,
                     gap=1.3, margin=0.9, lit=0.35, seed=7.0, bev=0.1, edge_filter=outside)
    tk.ring_band("balustrade", tk.offset_poly(plan, -0.2), H_SHAFT + 1.4, H_SHAFT + 2.4, 0.4, "terracotta")
    tk.cornice("attic_cornice", attic, 53.6, h=0.8, out=0.5, mat="terracotta")
    tk.prism("roof_deck", tk.offset_poly(attic, -0.3), 54.2, 54.5, "roofd")
    tk.hvac_cluster("plant", 0.0, 0.0, 54.5, YAW, 22.0, 18.0, seed=3.0, hmax=H_TOP - 54.5, fans=False)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
