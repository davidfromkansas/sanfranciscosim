"""Deterministic Blender build of the SF-SIM miniature Palace Hotel.

    blender -b --python build_palace_hotel.py -- [--out DIR]

2 New Montgomery Street at Market (Trowbridge & Livingston, opened 1909 on
the site of the 1875 Palace): a nine-storey block filling most of its city
block. Outside it is plain and big - a two-storey pale stone base with large
shop and lobby windows, a tan brick shaft of regular punched windows framed by
stone quoins at the corners, a top storey of round-headed windows, and a
deep cornice. Inside, the glass-roofed Garden Court, shown here as a lit
skylight in a dark court in the middle of the roof. Helpers in
tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "palace-hotel"
CENTER = (-122.4019446, 37.7879687)  # OSM relation 3492933 (outer ring), OBB centre
H_TOP = 40.0                          # DataSF 2010 LiDAR majority of ring 201006.0000105 (measured; median 37.0)
YAW = tk.bearing_to_yaw(134.7)        # local +x = SE along New Montgomery, +y = NE; Market St = -x face
W, D = 102.8, 78.6                    # OSM outer ring (a clean rectangle)


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def build():
    plan = L(tk.rect(W, D))
    # two-storey stone base: shop and lobby windows, lit
    tk.prism("base", plan, 0.0, 9.0, "stone", bev=0.15)
    tk.panes("base_win", plan, [(0.0, 6.0)], 4.6, mat="glassd", gap=1.2, margin=0.6)
    tk.lit_windows("base_lit", plan, [(0.0, 6.0)], 4.6, 0.7, seed=1.0, out=0.1, margin=0.8, gap=1.6)
    tk.ring_band("base_cap", plan, 9.0, 9.7, 0.3, "stone")
    # tan brick shaft: 6 storeys of 3.65 m, punched windows; stone quoin piers at the corners
    tk.punched_block("shaft", plan, 9.7, 31.6, 3.65, wall="granite", win="glassd", spacing=4.6, gap=2.4,
                     margin=0.9, lit=0.3, seed=4.0, bev=0.0)
    corners = [(sx * (W / 2 + 0.15), sy * (D / 2 + 0.15)) for sx in (-1, 1) for sy in (-1, 1)]
    for i, (x, y) in enumerate(corners):
        q = L(tk.rect(2.2, 2.2, x, y))
        tk.prism(f"quoin{i}", q, 9.7, 31.6, "stone")
    tk.ring_band("band", plan, 31.6, 32.3, 0.35, "stone")
    # top storey of round-headed windows, deep cornice, parapet
    tk.prism("top", plan, 32.3, 36.4, "granite")
    tk.arched_panes("top_arches", plan, 32.8, 36.0, 4.6, 1.8, mat="glassd", seg=3)
    tk.ring_band("cornice", plan, 36.4, 38.0, 1.2, "stone")
    tk.ring_band("parapet", plan, 38.0, H_TOP, 0.2, "stone")
    tk.prism("roof", tk.offset_poly(plan, -0.3), 37.6, 38.1, "roofd")
    # Garden Court: dark court with a lit glass roof in the middle of the block
    court = L(tk.rect(34.0, 26.0, 4.0, 0.0))
    tk.ring_band("court_rim", court, 38.1, 38.7, 0.5, "stone")
    tk.prism("court_glass", tk.offset_poly(court, -0.3), 38.1, 38.5, "glassl")
    tk.glow_cap("garden_court", tk.offset_poly(court, -1.2), 38.55, "sand_Glow")
    for i, y in enumerate((-26.0, 26.0)):  # two light wells
        tk.glow_cap(f"well{i}", L(tk.rect(30.0, 6.0, 4.0, y)), 38.14, "ink")
    tk.hvac_cluster("plant", *P(-36.0, 0.0), 38.1, YAW, 10.0, 18.0, seed=2.0, hmax=1.8, fans=False)
    tk.prism("sidewalk", L(tk.rect(W + 6.0, D + 6.0)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
