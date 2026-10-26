"""Deterministic Blender build of the SF-SIM miniature U.S. Custom House.

    blender -b --python build_us_customs_house.py -- [--out DIR]

555 Battery Street (Eames & Young, 1906-11): a six-storey Beaux-Arts federal
block faced in pale Raymond granite. U-shaped plan (wings on Battery, Jackson
and Washington) around a two-storey oval pavilion holding the Custom Hall and
its three skylights. Three zones: rusticated granite ground storey, smooth
middle storeys with pedimented windows, a recessed top storey with eagles and a
parapet; a sculpture group stands over the cornice at the Battery entrance.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "us-customs-house"
CENTER = (-122.4009459, 37.7962972)  # OSM way 32859013, OBB centre
H_TOP = 30.46                         # DataSF 2010 LiDAR max (sculpture group); roof 28.87 (majority)
YAW = tk.bearing_to_yaw(81.5)         # local +x = Battery St face (E), +y = Jackson St (N)
HX, HY = 16.9, 39.6                   # OSM OBB 33.8 x 79.3 m


def L(poly):
    return tk.xform(poly, YAW)


# U plan in local metres (OSM light courts at y = +-9..20, pavilion between them)
U = [(-HX, -HY), (HX, -HY), (HX, HY), (-HX, HY), (-HX, 20.5), (-1.0, 20.5), (-1.0, -20.2), (-HX, -20.2)]


def pavilion_plan():
    """Oval-ended Custom Hall pavilion, x -16.4..-4.8, y -16..16.5 (OSM outline)."""
    r, cx = 5.8, -10.6
    pts = []
    for i in range(7):
        a = math.pi + math.pi * i / 6
        pts.append((cx + r * math.cos(a), -10.3 + r * math.sin(a)))
    for i in range(7):
        a = math.pi * i / 6
        pts.append((cx + r * math.cos(a), 10.6 + r * math.sin(a)))
    return pts


def build():
    u = L(U)
    # ground storey: rusticated granite (stone) with joint bands
    tk.prism("base", u, 0.0, 6.4, "stone", bev=0.15)
    tk.spandrels("rustic", u, [3.1], 0.3, 0.12, "concrete")
    tk.panes("base_win", u, [(0.0, 6.4)], 4.2, mat="glassd", gap=2.0, margin=1.2)
    tk.lit_windows("base_lit", u, [(0.0, 6.4)], 4.2, 0.45, seed=3.0, out=0.1, margin=1.6, gap=2.4)
    tk.cornice("base_course", u, 6.4, h=0.7, out=0.35, mat="white")
    # middle zone: smooth granite, three storeys
    tk.punched_block("mid", u, 7.1, 22.0, 4.97, wall="white", win="glassd", spacing=4.2, gap=2.1,
                     margin=1.0, lit=0.3, seed=5.0, bev=0.12)
    tk.cornice("cornice", u, 22.0, h=1.3, out=1.0, mat="stone")
    # recessed top storey + parapet
    top = L([(-HX + 1.6, -HY + 1.6), (HX - 1.6, -HY + 1.6), (HX - 1.6, HY - 1.6), (-HX + 1.6, HY - 1.6),
             (-HX + 1.6, 22.1), (-2.6, 22.1), (-2.6, -21.8), (-HX + 1.6, -21.8)])
    tk.punched_block("attic", top, 23.3, 28.2, 4.9, wall="stone", win="glassd", spacing=3.2, gap=1.4,
                     margin=0.9, lit=0.35, seed=7.0, bev=0.1)
    tk.ring_band("parapet", top, 28.2, 28.87, 0.25, "white")
    tk.prism("roof", tk.offset_poly(top, -0.3), 27.9, 28.3, "roofd")
    tk.hvac_cluster("plant", *tk.rot2((8.0, 0.0), YAW), 28.3, YAW, 6.0, 30.0, seed=2.0, hmax=1.6, fans=False)
    # Battery entrance: projecting granite frontispiece + sculpture group over the cornice
    tk.box("portal", *tk.rot2((HX + 0.5, 0.0), YAW), 0.0, 22.0, 1.4, 18.0, "white", yaw=YAW, bev=0.15)
    tk.pier_grid("portal_cols", L([(HX + 1.2, -7.5), (HX + 1.2, 7.5), (HX - 2.0, 7.5), (HX - 2.0, -7.5)]),
                 7.1, 21.6, 3.0, 1.1, 0.7, "stone", skip_short=10.0, min_count=6)
    door = L([(HX + 1.25, -2.0), (HX + 1.25, 2.0), (HX + 1.0, 2.0), (HX + 1.0, -2.0)])
    tk.arched_panes("door", door, 0.3, 6.0, 5.0, 3.6, mat="glassd", out=0.05,
                    edge_filter=lambda ei, p0, p1, n: abs(n[0] - math.cos(YAW)) < 0.2)
    tk.arched_panes("door_lit", door, 0.5, 4.8, 5.0, 2.8, mat="sand_Glow", out=0.1, suffix="_glow",
                    edge_filter=lambda ei, p0, p1, n: abs(n[0] - math.cos(YAW)) < 0.2)
    tk.box("sculpt_base", *tk.rot2((HX - 0.2, 0.0), YAW), 23.3, 25.4, 2.6, 9.0, "stone", yaw=YAW, bev=0.15)
    tk.box("sculpt_mid", *tk.rot2((HX - 0.2, 0.0), YAW), 25.4, 28.6, 1.8, 5.0, "white", yaw=YAW, bev=0.3)
    tk.box("sculpt_l", *tk.rot2((HX - 0.2, -3.2), YAW), 25.4, 27.4, 1.6, 1.4, "white", yaw=YAW, bev=0.3)
    tk.box("sculpt_r", *tk.rot2((HX - 0.2, 3.2), YAW), 25.4, 27.4, 1.6, 1.4, "white", yaw=YAW, bev=0.3)
    tk.pyramid("sculpt_eagle", L(tk.rect(1.4, 2.6, HX - 0.2, 0.0)), 28.6, H_TOP, "stone")
    # smaller eagle groups over the cornice at the Washington (S) and Jackson (N) centres (photo: S)
    for s in (-1, 1):
        tk.box(f"eagle_base{s}", *tk.rot2((6.0, s * (HY - 0.3)), YAW), 23.3, 25.0, 5.0, 1.6, "stone", yaw=YAW, bev=0.12)
        tk.pyramid(f"eagle{s}", L(tk.rect(2.6, 1.2, 6.0, s * (HY - 0.3))), 25.0, 28.4, "white")
    # Custom Hall pavilion in the court, connector to the Battery wing, skylights
    pav = L(pavilion_plan())
    tk.prism("pavilion", pav, 0.0, 10.5, "stone", bev=0.15)
    tk.arched_panes("pav_win", pav, 3.5, 9.4, 4.4, 2.6, mat="glassd")
    tk.arched_panes("pav_lit", pav, 3.8, 8.6, 4.4, 2.0, mat="sand_Glow", out=0.1, suffix="_glow")
    tk.ring_band("pav_cornice", pav, 10.5, 11.1, 0.4, "white")
    tk.frustum("pav_roof", tk.offset_poly(pav, 0.1), 11.1, tk.scale_poly(pav, 0.75, *tk.rot2((-10.6, 0.2), YAW)),
               12.6, "verdigris")
    tk.prism("link", L(tk.rect(4.4, 18.0, -2.9, 0.0)), 0.0, 10.5, "stone")
    for i, y in enumerate((-8.0, 0.0, 8.0)):
        sk = L(tk.rect(3.2, 3.6, -10.6, y))
        tk.prism(f"sky{i}", sk, 12.4, 12.9, "glassl")
        tk.glow_cap(f"sky{i}", sk, 12.95, "white_Glow")
    tk.prism("sidewalk", L(tk.rect(2 * HX + 5.0, 2 * HY + 5.0)), 0.0, 0.2, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
