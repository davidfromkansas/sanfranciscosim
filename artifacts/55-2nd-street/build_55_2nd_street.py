"""Deterministic Blender build of the SF-SIM miniature KPMG Building (55 Second Street).

    blender -b --python build_55_2nd_street.py -- [--out DIR]

KPMG Building, 55 Second Street (Heller Manus / HKS, 2002): a 25-storey
postmodern office tower in warm beige granite with tall green-glass window
strips. A three-storey base and an eleven-storey podium block fill the site to
a strong cornice; above it the tower rises with notched, stepped corners and
two setbacks to a small crowned top. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "55-2nd-street"
CENTER = (-122.400334, 37.7888147)   # OSM way 79377189, OBB centre
H_TOP = 100.6                         # published 100.6 m (Wikipedia tallest list / CTBUH)
H_BASE = 12.6
H_PODIUM = 44.0
H_TIER1 = 84.0
H_TIER2 = 92.0
H_TIER3 = 97.4
YAW = tk.bearing_to_yaw(134.1)
# OSM footprint about CENTER (collinear mid-edge nodes dropped; the two re-entrant notches kept)
PLAN = [(-30.8, 4.5), (-20.9, 14.6), (-20.0, 13.8), (-16.3, 17.6), (-17.1, 18.4), (-5.2, 30.5),
        (30.8, -4.5), (16.8, -18.7), (16.1, -18.1), (13.5, -20.8), (14.1, -21.5), (5.2, -30.5)]


def P(poly):
    return tk.xform(poly, YAW)


def build():
    plan = tk.ccw(PLAN)
    # base: three tall storeys of granite with big glass bays and a lit lobby
    tk.prism("base", plan, 0.0, H_BASE, "sand", bev=0.15)
    tk.panes("base_win", plan, [(0.6, H_BASE - 1.2)], 4.6, mat="verdigris", gap=1.4, margin=0.2)
    tk.lit_windows("base_lit", plan, [(0.6, H_BASE - 1.2)], 4.6, 0.55, seed=1.0, out=0.1, margin=0.8, gap=1.8)
    tk.cornice("base_cornice", plan, H_BASE, h=0.8, out=0.4, mat="stone")
    # podium: granite grid with green-glass window strips, strong cornice
    tk.punched_block("podium", plan, H_BASE + 0.8, H_PODIUM, 3.9, wall="sand", win="verdigris", spacing=3.4,
                     gap=1.2, margin=0.5, lit=0.3, seed=2.0, bev=0.12)
    tk.cornice("podium_cornice", plan, H_PODIUM, h=1.2, out=0.8, mat="stone")
    # tower: notched corners, two setbacks
    t1 = P(tk.notch_rect(46.0, 32.0, 3.0))
    t2 = P(tk.notch_rect(40.0, 26.0, 3.0))
    t3 = P(tk.notch_rect(30.0, 18.0, 2.5))
    tk.punched_block("tower", t1, H_PODIUM + 1.2, H_TIER1, 3.9, wall="sand", win="verdigris", spacing=3.4,
                     gap=1.2, margin=0.5, lit=0.3, seed=3.0, bev=0.12)
    tk.ring_band("tier1_band", t1, H_TIER1 - 0.6, H_TIER1, 0.3, "stone")
    tk.punched_block("tier2", t2, H_TIER1, H_TIER2, 4.0, wall="sand", win="verdigris", spacing=3.4,
                     gap=1.2, margin=0.5, lit=0.35, seed=4.0, bev=0.1)
    tk.ring_band("tier2_band", t2, H_TIER2 - 0.6, H_TIER2, 0.3, "stone")
    tk.punched_block("tier3", t3, H_TIER2, H_TIER3, 5.4, wall="sand", win="verdigris", spacing=3.4,
                     gap=1.2, margin=0.7, lit=0.4, seed=5.0, bev=0.1)
    tk.cornice("crown_cornice", t3, H_TIER3, h=1.0, out=0.6, mat="stone")
    # roof decks of the setbacks, top plant, crown light
    tk.prism("deck_podium", tk.offset_poly(plan, -0.3), H_PODIUM + 0.9, H_PODIUM + 1.25, "roofd")
    tk.prism("deck_t1", tk.offset_poly(t1, -0.3), H_TIER1 - 0.3, H_TIER1 + 0.05, "roofd")
    tk.prism("deck_t2", tk.offset_poly(t2, -0.3), H_TIER2 - 0.3, H_TIER2 + 0.05, "roofd")
    tk.ring_band("parapet", tk.offset_poly(t3, -0.3), H_TIER3 + 1.0, H_TIER3 + 1.8, 0.3, "sand")
    tk.prism("deck_top", tk.offset_poly(t3, -0.4), H_TIER3 + 0.8, H_TIER3 + 1.1, "roofd")
    tk.hvac_cluster("plant", 0.0, 0.0, H_TIER3 + 1.1, YAW, 16.0, 9.0, seed=6.0, hmax=H_TOP - H_TIER3 - 1.1, fans=False)
    tk.glow_ring("crown_line", t3, H_TIER3 + 1.1, H_TIER3 + 1.7, 0.12, "white_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
