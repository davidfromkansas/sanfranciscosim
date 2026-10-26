"""Deterministic Blender build of the SF-SIM miniature Alexander Building.

    blender -b --python build_alexander_building.py -- [--out DIR]

155 Montgomery Street at Bush (1921): a slender fifteen-storey office tower
on a small corner lot. No photograph was available; the miniature follows the
period's San Francisco high-rise type with a vertical, late-Gothic accent: a
two-storey stone base, continuous cream terracotta piers rising past recessed
dark spandrels, an arcaded top storey and a parapet of small pinnacles.
Footprint and roof height are measured (OSM, DataSF LiDAR); the facade
treatment is inferred. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "alexander-building"
CENTER = (-122.4025673, 37.7907514)  # OSM way 132125157, OBB centre
H_TOP = 60.13                         # DataSF 2010 LiDAR median of ring 201006.0009912 (measured)
YAW = tk.bearing_to_yaw(81.1)         # local +x = east, +y = north (Montgomery St = west face, Bush = south)
W, D = 17.1, 22.4                     # OSM OBB: 17.1 m on Bush, 22.4 m on Montgomery


def street(ei, p0, p1, n):
    m = tk.rot2(n, -YAW)
    return m[0] < -0.9 or m[1] < -0.9


def build():
    plan = tk.xform(tk.rect(W, D), YAW)
    tk.prism("base", plan, 0.0, 8.4, "stone", bev=0.15)
    tk.panes("base_win", plan, [(0.0, 8.4)], 3.4, mat="glassd", gap=0.8, margin=0.7, edge_filter=street)
    tk.lit_windows("base_lit", plan, [(0.0, 4.8)], 3.4, 0.8, seed=1.0, out=0.1, margin=0.5, gap=1.0,
                   edge_filter=street)
    tk.ring_band("base_cap", plan, 8.4, 9.0, 0.3, "terracotta")
    # shaft: 12 storeys of 3.9 m, cream piers over dark recessed spandrels
    tk.prism("shaft", plan, 9.0, 55.8, "terracotta", bev=0.12)
    bands = tk.floors(9.0, 55.8, 3.9)
    tk.panes("shaft_win", plan, bands, 2.15, mat="glassd", gap=0.7, margin=0.5)
    tk.lit_windows("shaft_lit", plan, bands, 2.15, 0.3, seed=4.0, out=0.1, margin=0.7, gap=0.9)
    tk.pier_grid("piers", plan, 9.0, 57.6, 2.15, 0.55, 0.3, "cream", skip_short=6.0)
    # arcaded top storey, cornice, pinnacle parapet
    tk.ring_band("top_band", plan, 55.8, 56.3, 0.35, "cream")
    tk.prism("top", plan, 56.3, 58.6, "terracotta", bev=0.1)
    tk.arched_panes("top_arches", plan, 56.5, 58.4, 2.15, 1.3, mat="glassd")
    tk.ring_band("cornice", plan, 58.6, 59.2, 0.5, "cream")
    tk.prism("roof", tk.offset_poly(plan, -0.3), 58.9, 59.3, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.1), 59.2, 59.6, 0.2, "cream")
    tk.pier_grid("pinnacles", tk.offset_poly(plan, -0.2), 59.6, H_TOP, 4.3, 0.5, 0.5, "cream", skip_short=6.0)
    tk.box("stair", *tk.rot2((3.5, 6.0), YAW), 59.3, 60.1, 4.0, 4.0, "roofd", yaw=YAW)
    tk.prism("sidewalk", tk.xform(tk.rect(W + 4.0, D + 4.0, -1.0, -1.0), YAW), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
