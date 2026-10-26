"""Deterministic Blender build of the SF-SIM miniature Savings Union Bank Building.

    blender -b --python build_1_grant_avenue.py -- [--out DIR]

1 Grant Avenue at O'Farrell and Market (1910): a granite banking temple,
used today for travelling exhibitions. Only a distant aerial view was found (in the
Phelan Building's Commons photo); the miniature follows it and the LiDAR: a near-square granite block on a low plinth, colossal columns set
between corner piers on its two street faces (Grant Avenue east, O'Farrell
south), a deep entablature with a pediment over O'Farrell, an attic, and a white dome on a drum rising
about 4.6 m above the attic (LiDAR median 25.6 m, max 30.2 m). Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "1-grant-avenue"
CENTER = (-122.4051939, 37.786999)   # OSM way 32946683, OBB centre
H_TOP = 30.22                         # DataSF 2010 LiDAR max of ring 201006.0004905 (dome)
H_ATTIC = 25.6                        # LiDAR median (attic roof)
YAW = tk.bearing_to_yaw(81.4)         # local +x = east (Grant Ave face), +y = north; O'Farrell = south face
W, D = 26.7, 24.2
REC = 2.6                             # colonnade recess depth


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def build():
    hw, hd = W / 2, D / 2
    pier = 4.2
    body = L([(-hw, -hd), (-hw + pier, -hd), (-hw + pier, -hd + REC), (hw - pier, -hd + REC),
              (hw - pier, -hd), (hw, -hd), (hw, -hd + pier), (hw - REC, -hd + pier), (hw - REC, hd - pier),
              (hw, hd - pier), (hw, hd), (-hw, hd)])
    tk.prism("plinth", L(tk.rect(W + 1.2, D + 1.2)), 0.0, 1.4, "stone", bev=0.1)
    tk.prism("walls", body, 1.4, 20.0, "white", bev=0.12)
    # tall windows/doors in the recessed bays, lit at night
    def bay(ei, p0, p1, n):
        m = tk.rot2(n, -YAW)
        c = tk.rot2(((p0[0] + p1[0]) / 2, (p0[1] + p1[1]) / 2), -YAW)
        return (m[1] < -0.9 and abs(c[1] + hd - REC) < 0.1) or (m[0] > 0.9 and abs(c[0] - hw + REC) < 0.1)
    tk.panes("bay_win", body, [(1.4, 18.4)], 3.6, mat="glassd", gap=1.4, margin=0.6, edge_filter=bay)
    tk.lit_windows("bay_lit", body, [(1.4, 7.0)], 3.6, 0.9, seed=2.0, out=0.1, margin=0.4, gap=1.8,
                   edge_filter=bay)
    # colossal columns: four on O'Farrell, three on Grant
    for i in range(4):
        x = -hw + pier + 1.6 + (W - 2 * pier - 3.2) * i / 3
        c = P(x, -hd + 1.1)
        tk.cylinder(f"colS{i}", c[0], c[1], 1.4, 18.6, 0.85, "stone", seg=8, r1=0.72)
    for i in range(3):
        y = -hd + pier + 1.6 + (D - 2 * pier - 3.2) * i / 2
        c = P(hw - 1.1, y)
        tk.cylinder(f"colE{i}", c[0], c[1], 1.4, 18.6, 0.85, "stone", seg=8, r1=0.72)
    full = L(tk.rect(W, D))
    tk.prism("capitals", full, 18.6, 20.0, "stone")
    tk.prism("entablature", full, 20.0, 22.2, "white", bev=0.1)
    tk.cornice("cornice", full, 22.2, h=0.9, out=0.6, mat="stone")
    attic = tk.offset_poly(full, -0.8)
    tk.prism("attic", attic, 23.1, H_ATTIC - 0.3, "white", bev=0.1)
    tk.ring_band("attic_cap", attic, H_ATTIC - 0.3, H_ATTIC, 0.2, "stone")
    tk.prism("roof", tk.offset_poly(attic, -0.3), H_ATTIC - 0.6, H_ATTIC - 0.2, "roofd")
    # pediment over the O'Farrell colonnade (seen from the Phelan Building)
    pv = []
    for y in (-hd - 0.3, -hd + 2.2):
        for x, z in ((-hw + 0.4, 23.1), (hw - 0.4, 23.1), (0.0, 26.6)):
            px, py = P(x, y)
            pv.append((px, py, z))
    tk.new_mesh("pediment", pv, [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)], ["white"])
    # drum and shallow dome with a lit oculus
    cx, cy = 0.0, 0.0
    tk.cylinder("drum", cx, cy, H_ATTIC - 0.2, 27.2, 7.0, "stone", seg=16)
    rings = []
    for r, z in ((7.3, 27.2), (6.6, 28.6), (5.0, 29.6), (2.4, 30.1)):
        rings.append((z, [(cx + r * math.cos(2 * math.pi * i / 16), cy + r * math.sin(2 * math.pi * i / 16))
                          for i in range(16)]))
    tk.loft("dome", rings, "white", cap_top=True)
    tk.cylinder("lantern", cx, cy, 30.0, H_TOP - 0.02, 1.2, "stone", seg=8)
    tk.glow_cap("oculus", tk.ellipse(1.0, 1.0, 8), H_TOP, "sand_Glow")
    tk.prism("sidewalk", L(tk.rect(W + 5.0, D + 5.0)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
