"""Deterministic Blender build of the SF-SIM miniature Mechanics' Institute building.

    blender -b --python build_first_national_bank_building.py -- [--out DIR]

57 Post Street (Albert Pissis, 1910): the nine-storey Beaux-Arts home of the
Mechanics' Institute library and chess room. The OSM way is tagged with a
ground-floor tenant ("First National Bank of Northern California"); assessor
parcel 0311013 and the 2010 LiDAR ring identify the building. Light stone: a
rusticated base with a round-arched entrance, a double-height arcade of
library windows, a punched office shaft and a deep cornice. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "first-national-bank-building"
CENTER = (-122.4030303, 37.7887399)   # OSM way 32946665, OBB centre
H_TOP = 43.0                          # MEASURED: LiDAR median 42.97 m (SF0311013); OSM height=43
PLAN = [(-13.8, 14.1), (-10.1, -10.1), (-8.8, -17.7), (12.1, -8.7), (8.9, 17.7)]   # OSM, m from CENTER


def post(ei, p0, p1, nrm):
    """The north face on Post Street (the street front)."""
    return nrm[1] > 0.9


def build():
    plan = tk.ccw(PLAN)
    # rusticated base with the arched entrance (Post St) and shopfronts
    tk.prism("base", plan, 0.0, 6.0, "stone", bev=0.12)
    for z in (1.5, 3.0, 4.5):
        tk.ring_band(f"rustic{z}", plan, z - 0.15, z, 0.12, "concrete")
    tk.arched_panes("base_arches", plan, 0.3, 5.4, 5.6, 3.6, mat="glassd")
    tk.arched_panes("base_lit", plan, 0.5, 4.2, 5.6, 2.6, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("base_cornice", plan, 6.0, h=0.8, out=0.5, mat="trim")
    # double-height library arcade
    tk.prism("library", plan, 6.8, 14.6, "stone", bev=0.1)
    tk.arched_panes("library_arches", plan, 7.4, 14.0, 5.6, 4.0, mat="glassd")
    tk.arched_panes("library_lit", plan, 7.8, 13.0, 5.6, 3.0, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.ring_band("band", plan, 14.6, 15.2, 0.35, "trim")
    # office shaft: six storeys of punched windows
    tk.punched_block("shaft", plan, 15.2, 38.4, 3.866, wall="stone", win="glassd", spacing=2.8, gap=1.1,
                     margin=0.8, lit=0.3, seed=8.0, bev=0.1)
    # top storey, deep cornice, parapet and roof
    tk.ring_band("top_band", plan, 38.4, 38.9, 0.3, "trim")
    tk.prism("top", plan, 38.9, 41.2, "stone", bev=0.1)
    tk.panes("top_win", plan, [(38.9, 41.2)], 2.8, mat="glassd", gap=1.3, margin=0.5)
    tk.cornice("cornice", plan, 41.2, h=1.2, out=1.2, mat="trim")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.3), 42.4, H_TOP, 0.5, "stone")
    tk.prism("deck", tk.offset_poly(plan, 0.2), 42.3, 42.6, "roofd")
    tk.hvac_cluster("plant", 0.0, -2.0, 42.6, tk.bearing_to_yaw(171.4), 8.0, 10.0, seed=6.0, hmax=0.4, fans=False)
    # the Mechanics' Institute portal: a cream arch frame proud of the Post facade
    for p0, p1, L, nrm in tk.edges(plan):
        if not post(0, p0, p1, nrm):
            continue
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        c = (p0[0] + ux * L * 0.35 + nrm[0] * 0.3, p0[1] + uy * L * 0.35 + nrm[1] * 0.3)
        tk.box("portal", c[0], c[1], 0.0, 6.4, 5.6, 0.6, "trim", yaw=math.atan2(uy, ux), bev=0.08)
        fr = tk.xform(tk.rect(5.6, 0.6), math.atan2(uy, ux), c[0], c[1])
        face = lambda ei, q0, q1, nn: nn[0] * nrm[0] + nn[1] * nrm[1] > 0.9  # noqa: E731
        tk.arched_panes("portal_door", fr, 0.0, 5.6, 5.6, 3.4, mat="ink", out=0.03, edge_filter=face)
        tk.arched_panes("portal_lit", fr, 0.2, 3.6, 5.6, 2.2, mat="sand_Glow", out=0.07, edge_filter=face,
                        suffix="_glow")
    tk.prism("sidewalk", tk.offset_poly(plan, 2.5), 0.0, 0.2, "stone")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
