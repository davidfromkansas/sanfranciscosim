"""Deterministic Blender build of the SF-SIM miniature Aronson Building.

    blender -b --python build_706_mission_street.py -- [--out DIR]

706 Mission Street at Third (1903): a ten-storey warm brick commercial block
with a two-storey shopfront base, a punched brick shaft, an arcaded top
storey and a deep bracketed cornice. Since 2020 it is the restored base of the
Four Seasons Private Residences tower (handled separately; not modelled here).
Footprint is the OSM way. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "706-mission-street"
CENTER = (-122.402484, 37.7862342)    # OSM way 112878589, OBB centre
H_TOP = 44.0                          # MEASURED: LiDAR median 43.9 m (2010, before the tower); OSM 55 m unsourced
PLAN = [(-21.4, -2.5), (-3.5, -21.0), (21.4, 2.5), (3.2, 21.2)]     # OSM, m from CENTER


def build():
    plan = tk.ccw(PLAN)
    # two-storey shopfront base: terracotta piers, dark glass, lit shop windows
    tk.prism("base", plan, 0.0, 8.0, "terracotta", bev=0.12)
    tk.panes("shopfront", plan, [(0.3, 7.2)], 4.3, mat="glassd", gap=1.1, margin=0.0)
    tk.lit_windows("shop_lit", plan, [(0.5, 5.2)], 4.3, 0.8, seed=2.0, out=0.1, margin=0.2, gap=1.5)
    tk.ring_band("base_cornice", plan, 8.0, 8.8, 0.45, "terracotta")
    # brick shaft, seven storeys of paired punched windows
    tk.punched_block("shaft", plan, 8.8, 35.4, 3.8, wall="brick", win="glassd", spacing=2.15, gap=0.9,
                     margin=0.8, lit=0.3, seed=5.0, bev=0.12)
    tk.ring_band("band", plan, 35.4, 36.0, 0.35, "terracotta")
    # arcaded top storey under the deep bracketed cornice
    tk.prism("attic", plan, 36.0, 41.8, "brick", bev=0.1)
    tk.arched_panes("attic_arches", plan, 36.6, 41.2, 4.3, 3.0, mat="glassd")
    tk.arched_panes("attic_lit", plan, 36.9, 40.2, 4.3, 2.0, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("cornice", plan, 41.8, h=1.6, out=1.4, mat="terracotta")
    tk.ring_band("parapet", tk.offset_poly(plan, 0.2), 43.4, H_TOP, 0.3, "terracotta")
    tk.prism("deck", tk.offset_poly(plan, 0.1), 43.3, 43.6, "roofd")
    tk.hvac_cluster("plant", -2.0, -1.0, 43.6, tk.bearing_to_yaw(135.0), 10.0, 6.0, seed=3.0, hmax=0.4, fans=False)
    tk.prism("sidewalk", tk.offset_poly(plan, 2.5), 0.0, 0.2, "stone")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
