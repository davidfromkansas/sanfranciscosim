"""Deterministic Blender build of the SF-SIM miniature 715-719 Market Street.

    blender -b --python build_715_market_street.py -- [--out DIR]

715-719 Market Street (assessor parcel 3706064: commercial office, built
1908, 7 storeys), today the Digital Garage coworking building, next to the
Central Tower near Third Street. A post-1906 masonry commercial block: shop
base, a punched shaft and a bracketed cornice, on a deep L-shaped lot. No
photo could be fetched (Wikimedia rate limits); materials and facade rhythm
are INFERRED from the period type. Footprint is the OSM way. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "715-market-street"
CENTER = (-122.4037015, 37.7869053)   # OSM way 149332501, OBB centre
H_TOP = 32.6                          # MEASURED: LiDAR median 32.58 m (SF3706064); OSM height=33
PLAN = [(-16.0, 21.0), (-27.5, 9.7), (-6.6, -11.3), (9.4, -27.4), (27.5, -9.7), (12.4, 5.5), (5.8, -0.9)]


def street(ei, p0, p1, nrm):
    """Facades with windows: every edge except the long party walls to the SW."""
    return not (nrm[0] < -0.5 and nrm[1] < -0.5)


def build():
    plan = tk.ccw(PLAN)
    tk.prism("base", plan, 0.0, 5.6, "stone", bev=0.12)
    tk.panes("shopfront", plan, [(0.3, 5.0)], 4.0, mat="glassd", gap=1.0, margin=0.0, edge_filter=street)
    tk.lit_windows("shop_lit", plan, [(0.5, 4.0)], 4.0, 0.8, seed=3.0, out=0.1, margin=0.2, gap=1.4,
                   edge_filter=street)
    tk.ring_band("belt", plan, 5.6, 6.2, 0.35, "trim")
    tk.punched_block("shaft", plan, 6.2, 30.2, 4.0, wall="cream", win="glassd", spacing=2.6, gap=1.0,
                     margin=0.9, lit=0.3, seed=12.0, bev=0.12, edge_filter=street)
    tk.cornice("cornice", plan, 30.2, h=1.4, out=1.1, mat="trim")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.3), 31.6, H_TOP, 0.4, "cream")
    tk.prism("deck", tk.offset_poly(plan, 0.2), 31.5, 31.8, "roofd")
    tk.hvac_cluster("plant", 2.0, -12.0, 31.8, tk.bearing_to_yaw(135.0), 14.0, 6.0, seed=5.0, hmax=0.8, fans=False)
    # Market St (NW face): a projecting entrance bay with a sign band and lobby glow
    for p0, p1, L, nrm in tk.edges(plan):
        if nrm[0] < -0.5 and nrm[1] > 0.5 and L > 12:
            ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
            c = (p0[0] + ux * L / 2 + nrm[0] * 0.3, p0[1] + uy * L / 2 + nrm[1] * 0.3)
            tk.box("sign", c[0], c[1], 4.6, 5.4, L - 2.0, 0.6, "ink", yaw=math.atan2(uy, ux))
            a = (c[0] - ux * 5.0, c[1] - uy * 5.0)
            b = (c[0] + ux * 5.0, c[1] + uy * 5.0)
            tk.flat_quad("sign_glow", a, b, 4.75, 5.25, 0.32, "white_Glow", nrm)
    tk.prism("sidewalk", tk.offset_poly(plan, 2.5), 0.0, 0.2, "stone")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
