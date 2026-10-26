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
    # crown, per the Commons photo of the Market face: a row of tall two-storey
    # arched windows flush with the shaft, a deep cornice, an attic storey with
    # urns/balustrade, and the set-back top storeys
    tk.ring_band("arch_band", base, H_SHAFT - 0.5, H_SHAFT + 0.5, 0.35, "terracotta")
    tk.prism("arch_storey", base, H_SHAFT + 0.5, 67.0, "cream", bev=0.15)
    tk.arched_panes("arches", base, H_SHAFT + 1.2, 66.0, 4.6, 3.0, mat="glassd")
    tk.arched_panes("arches_lit", base, H_SHAFT + 1.6, 65.2, 4.6, 2.2, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.cornice("crown_cornice", base, 67.0, h=1.6, out=1.2, mat="terracotta")
    t1 = P(L - 3, W - 3)
    tk.punched_block("attic", t1, 68.6, 72.5, 3.9, wall="cream", win="glassd", spacing=2.9,
                     gap=1.3, margin=0.9, lit=0.35, seed=3.0)
    tk.ring_band("balustrade", tk.offset_poly(base, -0.2), 68.6, 69.8, 0.4, "terracotta")
    t2 = P(L - 13, W - 13)
    tk.punched_block("top", t2, 72.5, 77.0, 4.2, wall="cream", win="glassd", spacing=2.9,
                     gap=1.3, margin=0.9, lit=0.4, seed=4.0)
    tk.cornice("top_cornice", t2, 77.0, h=1.0, out=0.6, mat="terracotta")
    tk.prism("roof_t1", tk.offset_poly(t1, -0.3), 72.4, 72.6, "roofd")
    tk.ring_band("t1_parapet", tk.offset_poly(t1, -0.4), 72.5, 73.4, 0.4, "terracotta")
    tk.hvac_cluster("plant", 0, 0, 78.0, YAW, (L - 15) * 0.6, (W - 15) * 0.5, seed=3.0, hmax=H_TOP - 78.0)
    tk.plinth("plaza", base, h=0.25, out=3.0)
    p0, p1 = tk.xform([(-L / 2 - 2.2, -W / 2 + 4), (-L / 2 - 2.2, W / 2 - 4)], YAW)  # Market (NW) face
    tk.tree_row("trees", p0, p1, 0.25, 3, h=6.0, seed=4.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
