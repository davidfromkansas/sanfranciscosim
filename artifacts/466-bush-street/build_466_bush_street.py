"""Deterministic Blender build of the SF-SIM miniature Orchard Garden Hotel.

    blender -b --python build_466_bush_street.py -- [--out DIR]

466 Bush Street, just east of the Chinatown Gate at Grant Avenue (2006-07):
a ten-storey hotel, San Francisco's first LEED-certified one. A narrow cream
block on a deep lot: on Bush, two full-height bays of blue-grey glass rise
between cream piers over a dark bronze ground storey with an awning and a row
of flags, under a thin projecting top; the tall west party wall carries the
hotel's name high up where it shows over its low Chinatown neighbour. Helpers
in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "466-bush-street"
CENTER = (-122.4052622, 37.7909003)  # OSM way 260279404, OBB centre
H_TOP = 34.55                         # DataSF 2010 LiDAR max (rooftop penthouse); main roof 31.0 (median)
H_ROOF = 31.0
YAW = tk.bearing_to_yaw(81.1)         # local +x = east along Bush, +y = north (Bush St front at y = -21.3)
# OSM outline in local street-grid metres; light wells on both long sides
OUTLINE = [(7.3, -21.3), (-7.4, -21.3), (-7.4, 1.8), (-1.9, 1.8), (-1.9, 21.3), (1.1, 21.3), (1.1, 18.5),
           (7.4, 18.5), (7.4, 1.3), (3.9, 1.3), (3.9, -7.2), (7.3, -7.2)]
YF = -21.3


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def not_front(ei, p0, p1, n):
    return tk.rot2(n, -YAW)[1] > -0.9


def build():
    plan = L(OUTLINE)
    # cream block: punched windows on the sides and rear, 9 guest floors over the lobby storey
    tk.punched_block("body", plan, 0.0, H_ROOF, 2.89, wall="cream", win="glassd", spacing=3.0, gap=1.5,
                     margin=0.8, lit=0.35, seed=4.0, bev=0.12,
                     edge_filter=lambda ei, p0, p1, n: not_front(ei, p0, p1, n) and p0 != p1)
    # Bush St front: dark bronze ground storey, awning, lit lobby
    tk.box("shopfront", *P(0.0, YF - 0.15), 0.0, 4.9, 14.6, 0.5, "bronze", yaw=YAW)
    front = L(tk.rect(14.6, 0.6, 0.0, YF))
    tk.lit_windows("lobby", front, [(0.3, 4.4)], 3.6, 0.9, seed=1.0, out=0.42, margin=0.3, gap=0.8,
                   edge_filter=lambda ei, p0, p1, n: tk.rot2(n, -YAW)[1] < -0.9)
    tk.box("awning", *P(-2.0, YF - 1.3), 3.9, 4.3, 4.0, 2.2, "ink", yaw=YAW)
    # two full-height glass bays between cream piers
    for i, x in enumerate((-3.4, 3.4)):
        bay = L(tk.rect(4.4, 0.8, x, YF - 0.1))
        tk.prism(f"bay{i}", bay, 4.9, H_ROOF - 1.2, "glassl")
        tk.spandrels(f"bay{i}_bands", bay, [4.9 + 2.89 * k for k in range(1, 9)], 0.35, 0.04, "steel")
        tk.lit_windows(f"bay{i}_lit", bay, tk.floors(4.9, H_ROOF - 1.2, 2.89), 2.2, 0.45, seed=7.0 + i,
                       out=0.08, margin=0.5, gap=0.3,
                       edge_filter=lambda ei, p0, p1, n: tk.rot2(n, -YAW)[1] < -0.9)
    # thin projecting top on the front, roof, penthouse
    tk.box("top_slab", *P(0.0, YF + 1.0), H_ROOF - 0.6, H_ROOF, 15.4, 3.6, "trim", yaw=YAW)
    tk.ring_band("parapet", plan, H_ROOF, H_ROOF + 0.9, 0.2, "cream")
    tk.prism("roof", tk.offset_poly(plan, -0.3), H_ROOF - 0.3, H_ROOF + 0.1, "roofd")
    ph = L(tk.rect(6.0, 9.0, -3.0, -6.0))
    tk.prism("penthouse", ph, H_ROOF + 0.1, H_TOP, "cream", bev=0.1)
    tk.hvac_cluster("plant", *P(4.0, 9.0), H_ROOF + 0.1, YAW, 5.0, 8.0, seed=2.0, hmax=1.8, fans=False)
    tk.glow_ring("crown", ph, H_TOP - 0.5, H_TOP - 0.2, 0.05, "white_Glow")
    # the hotel's name high on the west party wall
    tk.box("sign", *P(-7.75, YF + 6.0), 24.0, 28.5, 0.3, 7.0, "ink", yaw=YAW)
    tk.prism("sidewalk", L(tk.rect(18.0, 4.0, 0.0, YF - 1.6)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
