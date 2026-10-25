"""Deterministic Blender build of the SF-SIM miniature PG&E General Office Building.

    blender -b --python build_pge_general_office.py -- [--out DIR]

245 Market Street (Bakewell & Brown, 1923-25; annex 1945): seventeen storeys
of cream terracotta - an arcaded two-storey base, a plain punched shaft, and
setbacks over the top four storeys crowned by a row of arched windows and a
deep cornice. It is the twin of the Matson Building next door. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "pge-general-office"
CENTER = (-122.396849, 37.792385)   # OSM way 1279504251, OBB centre
H_TOP = 79.8                         # DataSF LiDAR crest 79.77 m (measured)
H_BASE = 10.0
H_SHAFT = 60.0
L, W = 43.0, 41.0                   # OSM OBB 44.1 x 42.4
YAW = math.radians(90 - 135.3)
ON_MARKET = lambda ei, p0, p1, n: True  # noqa: E731


def P(w, d, cx=0.0, cy=0.0):
    return tk.xform(tk.rect(w, d, cx, cy), YAW)


def build():
    base = P(L, W)
    # base: rusticated two storeys with a run of tall arches
    tk.prism("base", base, 0.0, H_BASE, "terracotta", bev=0.2)
    tk.arched_panes("arcade", base, 0.6, H_BASE - 1.4, 5.4, 3.6, mat="glassd", out=0.06)
    tk.lit_windows("arcade_lit", base, [(0.6, H_BASE - 3.2)], 5.4, 0.85, seed=1.0, out=0.1, margin=0.4, gap=2.4)
    tk.cornice("base_cornice", base, H_BASE, h=1.0, out=0.6, mat="cream")
    # shaft: plain cream with punched windows
    tk.punched_block("shaft", base, H_BASE + 1.0, H_SHAFT, 3.9, wall="cream", win="glassd", spacing=2.9,
                     gap=1.3, margin=0.9, lit=0.32, seed=2.0, bev=0.15)
    tk.cornice("shaft_cornice", base, H_SHAFT, h=1.0, out=0.7, mat="terracotta")
    # setbacks: two receding tiers, the upper one with the arched loggia
    t1 = P(L - 5, W - 5)
    tk.punched_block("tier1", t1, H_SHAFT + 1.0, 68.5, 3.8, wall="cream", win="glassd", spacing=2.9,
                     gap=1.3, margin=0.9, lit=0.35, seed=3.0)
    t2 = P(L - 11, W - 11)
    tk.prism("tier2", t2, 68.5, 76.0, "cream", bev=0.15)
    tk.arched_panes("loggia", t2, 69.3, 74.8, 3.4, 2.3, mat="glassd")
    tk.arched_panes("loggia_lit", t2, 69.6, 74.0, 3.4, 1.7, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("crown_cornice", t2, 76.0, h=1.6, out=1.1, mat="terracotta")
    # roof terraces on the setbacks, and plant on the top
    tk.prism("roof_t1", tk.offset_poly(t1, -0.3), 68.4, 68.6, "roofd")
    tk.hvac_cluster("plant", 0, 0, 77.6, YAW, (L - 15) * 0.7, (W - 15) * 0.6, seed=3.0, hmax=H_TOP - 77.6)
    tk.plinth("plaza", base, h=0.25, out=3.0)
    p0, p1 = tk.xform([(-L / 2 + 4, -W / 2 - 2.2), (L / 2 - 4, -W / 2 - 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.25, 3, h=6.0, seed=4.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
