"""Deterministic Blender build of the SF-SIM miniature One Hawthorne.

    blender -b --python build_one_hawthorne_street.py -- [--out DIR]

One Hawthorne (EHDD, 2010): a 24-storey, 165-unit condominium tower at Howard x
Hawthorne in SoMa, on "a simple, eight-storey pre-cast concrete and limestone
base" (EHDD) with a glassy residential shaft above and a panoramic roof garden.
No usable photo could be fetched (Wikimedia rate-limited): the base/shaft split
and roof garden are published, the glass colours, the wing height and the crown
form are inferred. Heights are measured (2010 LiDAR, after topping out in 2009).
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "one-hawthorne-street"
CENTER = (-122.3989027, 37.7858049)   # OSM way 260318176, OBB centre
H_TOP = 83.9                           # measured: DataSF LiDAR peak (crown/plant)
H_ROOF = 73.0                          # measured: DataSF LiDAR roof majority 72.9 m, median 74.0 m
H_BASE = 26.0                          # eight storeys (EHDD) of 3.25 m
A = math.radians(45.0)                 # SoMa grid: u = bearing 45 (NE), v = bearing 315 (NW)


def G(poly):
    return tk.xform(poly, A)


def build():
    base = G([(-15.1, -24.7), (15.1, -24.8), (15.0, -11.5), (6.3, -11.5), (6.2, 24.8), (-15.1, 24.8)])
    tower = G([(-15.1, -24.7), (6.3, -24.8), (6.2, 24.8), (-15.1, 24.8)])
    # limestone / precast base: tall ground floor, seven storeys of punched windows
    tk.prism("ground", base, 0.0, 5.0, "stone", bev=0.1)
    tk.panes("ground_win", base, [(0.4, 4.4)], 4.0, mat="glassd", gap=1.2, margin=0.2)
    tk.lit_windows("ground_lit", base, [(0.4, 4.0)], 4.0, 0.85, seed=1.0, out=0.1, margin=0.3, gap=1.6)
    tk.punched_block("base", base, 5.0, H_BASE, 3.0, wall="stone", win="glassd", spacing=3.0, gap=1.2, margin=0.7,
                     lit=0.35, seed=2.0)
    tk.cornice("base_cap", base, H_BASE, h=0.8, out=0.5, mat="cream")
    wing = G([(6.3, -24.8), (15.1, -24.8), (15.0, -11.5), (6.3, -11.5)])
    tk.prism("wing_garden", tk.offset_poly(wing, -0.6), H_BASE + 0.8, H_BASE + 1.3, "leafd")
    # glassy residential shaft: 16 storeys of 2.94 m, white slab edges, light mullions
    z0, n = H_BASE + 0.8, 16
    p = (H_ROOF - z0) / n
    tk.shaft("shaft", tower, z0, H_ROOF, p, glass="glassl", band="white", band_h=0.6, band_out=0.35,
             fins=(3.2, 0.25, 0.3, "white"), lit=0)
    tk.lit_windows("shaft_lit", tk.offset_poly(tower, 0.45), [(z0 + i * p + 0.6, z0 + (i + 1) * p) for i in range(n)],
                   3.2, 0.35, seed=3.0, out=0.0, margin=0.25, gap=0.4)
    # roof garden behind a white parapet; glazed lift/plant crown to the LiDAR peak
    tk.ring_band("parapet", tk.offset_poly(tower, 0.35), H_ROOF, H_ROOF + 1.2, 0.0, "white", inset=-0.4)
    tk.prism("roof", tk.offset_poly(tower, -0.1), H_ROOF - 0.3, H_ROOF + 0.1, "roofd")
    g1 = G(tk.rect(8.0, 14.0, -9.0, -14.0))
    g2 = G(tk.rect(8.0, 10.0, -9.0, 14.0))
    tk.prism("garden_s", g1, H_ROOF + 0.1, H_ROOF + 0.6, "leaf")
    tk.prism("garden_n", g2, H_ROOF + 0.1, H_ROOF + 0.6, "leaf")
    tk.glow_cap("garden_lamps", G(tk.rect(6.0, 12.0, -9.0, -14.0)), H_ROOF + 0.62, "sand_Glow")
    cr = G(tk.rect(10.0, 14.0, -3.0, 2.0))
    tk.prism("crown", cr, H_ROOF + 0.1, H_TOP - 0.5, "glassl", bev=0.1)
    tk.ring_band("crown_frame", cr, H_TOP - 0.5, H_TOP, 0.3, "white")
    tk.prism("crown_roof", cr, H_TOP - 0.7, H_TOP - 0.3, "roofd")
    tk.glow_ring("crown_light", cr, H_TOP - 2.6, H_TOP - 1.2, 0.08, "white_Glow")
    tk.plinth("sidewalk", base, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
