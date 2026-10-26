"""Deterministic Blender build of the SF-SIM miniature 601-605 Market Street.

    blender -b --python build_605_market_street.py -- [--out DIR]

The fifteen-storey 1917 office tower on the Market x Second corner (assessor
parcel 3707001, "601 Market", 15 storeys, built 1917; believed to be the
Santa Fe Building - unverified). A narrow early-skyscraper "column": a
two-storey base, a ten-storey pier-and-spandrel shaft, an ornamented two-storey
top and a deep cornice. No photo could be fetched (Wikimedia rate limits); the
facade treatment is INFERRED from the period type. Footprint is the OSM way.
Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "605-market-street"
CENTER = (-122.4013149, 37.7889421)   # OSM way 79377175, OBB centre
H_TOP = 54.3                          # MEASURED: LiDAR median 54.30 m (SF3707001); OSM height=54
PLAN = [(15.6, -5.0), (-4.9, 15.5), (-15.6, 5.0), (3.1, -13.7), (4.9, -15.5)]   # OSM, m from CENTER


def build():
    plan = tk.ccw(PLAN)
    # two-storey base: tall shop windows and the entrance
    tk.prism("base", plan, 0.0, 8.0, "stone", bev=0.12)
    tk.panes("base_win", plan, [(0.4, 7.4)], 4.2, mat="glassd", gap=1.2, margin=0.0)
    tk.lit_windows("base_lit", plan, [(0.6, 5.6)], 4.2, 0.8, seed=1.0, out=0.1, margin=0.2, gap=1.6)
    tk.cornice("base_cornice", plan, 8.0, h=0.8, out=0.5, mat="trim")
    # shaft: ten storeys, pale terracotta piers with recessed windows and spandrels
    shaft = tk.offset_poly(plan, -0.3)
    tk.prism("shaft", shaft, 8.8, 46.8, "terracotta", bev=0.1)
    bands = tk.floors(8.8, 46.8, 3.8)
    tk.panes("shaft_win", shaft, bands, 2.4, mat="glassd", gap=0.8, margin=0.7)
    tk.lit_windows("shaft_lit", shaft, bands, 2.4, 0.3, seed=7.0, out=0.12, margin=0.8, gap=1.0)
    tk.pier_grid("piers", shaft, 8.8, 46.8, 4.8, 0.7, 0.35, "trim", skip_short=3.0)
    # ornamented top: band, arched two-storey attic, deep cornice, parapet
    tk.ring_band("top_band", plan, 46.8, 47.4, 0.4, "trim")
    tk.prism("attic", plan, 47.4, 52.0, "terracotta", bev=0.1)
    tk.arched_panes("attic_arches", plan, 47.9, 51.5, 2.4, 1.5, mat="glassd")
    tk.arched_panes("attic_lit", plan, 48.2, 50.6, 2.4, 1.0, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("cornice", plan, 52.0, h=1.4, out=1.3, mat="trim")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), 53.4, H_TOP, 0.4, "terracotta")
    tk.prism("deck", tk.offset_poly(plan, 0.2), 53.3, 53.6, "roofd")
    tk.hvac_cluster("plant", 0.0, 0.0, 53.6, tk.bearing_to_yaw(135.0), 8.0, 6.0, seed=2.0, hmax=0.7, fans=False)
    tk.prism("sidewalk", tk.offset_poly(plan, 2.5), 0.0, 0.2, "stone")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
