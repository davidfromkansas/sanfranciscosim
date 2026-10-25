"""Deterministic Blender build of the SF-SIM miniature 735 Market Street.

    blender -b --python build_735_market_street.py -- [--out DIR]

735 Market Street (1907; six storeys, SF Assessor): a post-fire commercial
office block on the south side of Market between Third and Fourth, a narrow
three-bay front on Market running 52 m back through the block to Stevenson,
with a light well on its east flank. No photograph or description could be
retrieved, so the treatment is the period's standard: shopfronts under a
mezzanine band, a pale brick front of paired windows between piers, a
projecting cornice. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "735-market-street"
CENTER = (-122.4041285, 37.7865717)   # OSM way 149332505, OBB centre
H_TOP = 27.4                           # DataSF 2010 LiDAR roof (majority 27.44 m); OSM height 28
H_SHOP, H_CORNICE, H_ROOF = 5.6, 25.2, 26.4
YAW = tk.bearing_to_yaw(45.1)         # local +x = NE along Market, +y = NW (the Market St front)
# OSM footprint in that local frame (m): light well on the east flank
FOOT = [(9.3, 26.1), (-9.3, 26.3), (-9.3, -26.1), (9.3, -26.3), (9.3, -9.9), (6.2, -9.9), (6.2, 14.6),
        (9.3, 14.6)]


def street(ei, p0, p1, nrm):
    """Market (NW) and Stevenson (SE) fronts; the flanks are party walls."""
    lx, ly = tk.rot2(nrm, -YAW)
    return abs(ly) > 0.9


def build():
    plan = tk.ccw(tk.xform(FOOT, YAW))
    tk.prism("body", plan, 0.0, H_CORNICE, "sand", bev=0.1)
    tk.panes("shops", plan, [(0.3, H_SHOP - 0.9)], 4.6, mat="glassd", margin=0.0, gap=1.0, edge_filter=street)
    tk.lit_windows("shops_lit", plan, [(0.3, H_SHOP - 0.9)], 4.6, 0.95, seed=2.0, out=0.1, margin=0.3, gap=1.2,
                   edge_filter=street)
    tk.ring_band("shop_band", plan, H_SHOP - 0.6, H_SHOP, 0.25, "cream")
    bands = tk.floors(H_SHOP, H_CORNICE - 0.4, 3.9)
    tk.panes("windows", plan, bands, 2.3, mat="glassd", margin=0.8, gap=0.8, edge_filter=street)
    tk.lit_windows("windows_lit", plan, bands, 2.3, 0.35, seed=5.0, out=0.1, margin=0.85, gap=0.9,
                   edge_filter=street)
    # three bays on Market: four piers in the gaps of the window rhythm
    p0, p1 = tk.xform([(-9.3, 26.2), (9.3, 26.2)], YAW)
    piers = []
    for i, t in enumerate((-9.3 + 0.4, -9.3 + 6.9, 9.3 - 6.9, 9.3 - 0.4)):
        c = tk.rot2((t, 26.45), YAW)
        piers.append(tk.box(f"pier_{i}", c[0], c[1], H_SHOP, H_CORNICE, 0.8, 0.5, "cream", yaw=YAW))
    tk.join(piers, "piers")
    tk.cornice("cornice", plan, H_CORNICE, h=1.2, out=0.9, mat="cream")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.3), H_ROOF, H_TOP, 0.3, "sand")
    tk.prism("roof", plan, H_ROOF - 0.2, H_ROOF + 0.1, "roofd")
    c = tk.rot2((-2.0, -6.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.1, YAW, 10.0, 14.0, seed=6.0, hmax=0.9)
    tk.glow_cap("skylight_lit", tk.xform(tk.rect(6.0, 8.0, -2.0, 12.0), YAW), H_ROOF + 0.15, "sand_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)
    a, b = tk.xform([(-7.0, 28.5), (7.0, 28.5)], YAW)   # Market St trees
    tk.tree_row("trees", a, b, 0.25, 2, h=6.5, seed=9.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
