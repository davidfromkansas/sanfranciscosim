"""Deterministic Blender build of the SF-SIM miniature Pacific Coast Stock Exchange.

    blender -b --python build_301_pine_street.py -- [--out DIR]

301 Pine Street at Sansome (Milton Dyer's 1915 Sub-Treasury, remodelled 1930
by Miller & Pflueger as the San Francisco Stock Exchange trading hall; now a
gym). A grey granite temple front on Pine: a deep colonnade of tall columns
between two blank pylons, a broad flight of steps, an entablature carrying the
exchange's name, and Ralph Stackpole's two monumental granite figure groups on
pedestals in front of the pylons. The 1930 Stock Exchange Tower (155 Sansome,
its own artifact) stands against its south side. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "301-pine-street"
CENTER = (-122.4013003, 37.7918285)  # OSM way 256066230, OBB centre
H_TOP = 15.9                          # DataSF 2010 LiDAR median roof of ring 201006.0002868 (measured)
YAW = tk.bearing_to_yaw(81.4)         # local +x = east along Pine, +y = north (Pine St face)
HX, HY = 20.1, 12.7                   # OSM OBB 40.2 x 25.4 m
CX = 12.6                             # pylon inner edge (colonnade spans |x| < CX)
RECESS = 4.2


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def front_only(ei, p0, p1, n):
    """North (Pine) face only."""
    ny = tk.rot2(n, -YAW)[1]
    return ny > 0.9


def build():
    body = L([(-HX, -HY), (HX, -HY), (HX, HY), (CX, HY), (CX, HY - RECESS), (-CX, HY - RECESS),
              (-CX, HY), (-HX, HY)])
    tk.prism("hall", body, 0.0, 13.0, "stone", bev=0.15)
    # pylon rustication lines and a granite base course
    tk.spandrels("courses", body, [1.6], 0.5, 0.15, "concrete")
    # recessed wall behind the columns: tall windows + doors, lit at night
    back = L(tk.rect(2 * CX, 0.6, 0.0, HY - RECESS + 0.3))
    tk.panes("back_win", back, [(1.9, 11.0)], 3.3, mat="glassd", gap=1.2, margin=0.4, edge_filter=front_only)
    tk.lit_windows("back_lit", back, [(1.9, 11.0)], 3.3, 0.75, seed=4.0, out=0.1, margin=1.0, gap=1.6,
                   edge_filter=front_only)
    # colonnade: eight columns on the steps' top landing
    for i in range(8):
        x = -CX + 1.5 + (2 * CX - 3.0) * i / 7
        c = P(x, HY - 1.3)
        tk.cylinder(f"col{i}", c[0], c[1], 1.7, 11.0, 0.72, "white", seg=8, r1=0.6)
    # entablature over the colonnade with the exchange's name band
    tk.prism("entab", L(tk.rect(2 * CX + 0.4, RECESS + 0.6, 0.0, HY - RECESS / 2 + 0.2)), 11.0, 13.0, "stone")
    tk.box("name_band", *P(0.0, HY + 0.45), 11.6, 12.4, 18.0, 0.1, "concrete", yaw=YAW)
    tk.cornice("cornice", body, 13.0, h=1.0, out=0.6, mat="white")
    # attic and roof: trading-hall skylight, plant
    attic = L(tk.rect(2 * HX - 1.0, 2 * HY - 1.0, 0.0, -0.3))
    tk.prism("attic", attic, 14.0, 15.3, "stone", bev=0.1)
    tk.ring_band("parapet", attic, 15.3, 15.9, 0.15, "white")
    tk.prism("roof", tk.offset_poly(attic, -0.4), 15.0, 15.4, "roofd")
    sky = L(tk.rect(20.0, 10.0, -2.0, -2.0))
    tk.prism("skylight", sky, 15.4, 15.75, "glassl")
    tk.glow_cap("skylight", sky, 15.8, "sand_Glow")
    tk.hvac_cluster("plant", *P(14.0, -6.0), 15.4, YAW, 6.0, 7.0, seed=3.0, hmax=0.5, fans=False)
    # steps up to the colonnade
    for k in range(3):
        tk.prism(f"step{k}", L(tk.rect(2 * CX + 0.8 - k * 0.4, 2.4 - k * 0.8, 0.0, HY + 1.2 - k * 0.4)),
                 0.0, 0.6 * (k + 1), "stone")
    # Stackpole's figure groups on pedestals in front of the two pylons
    for side, x in (("e", 16.3), ("w", -16.3)):
        tk.box(f"ped_{side}", *P(x, HY + 1.6), 0.0, 1.6, 5.0, 3.2, "stone", yaw=YAW, bev=0.15)
        tk.box(f"fig_{side}1", *P(x - 0.9, HY + 1.4), 1.6, 7.6, 1.6, 1.6, "white", yaw=YAW, bev=0.35)
        tk.box(f"fig_{side}2", *P(x + 0.9, HY + 1.2), 1.6, 8.1, 1.6, 1.6, "white", yaw=YAW, bev=0.35)
        tk.box(f"fig_{side}3", *P(x - 0.9, HY + 2.2), 1.6, 4.6, 1.2, 0.9, "white", yaw=YAW, bev=0.25)
        tk.box(f"head_{side}", *P(x, HY + 1.3), 7.6, 8.8, 2.6, 1.3, "white", yaw=YAW, bev=0.3)
    tk.prism("sidewalk", L(tk.rect(2 * HX + 4.0, 2 * HY + 4.0, 0.0, 2.0)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
