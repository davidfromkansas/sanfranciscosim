"""Deterministic Blender build of the SF-SIM miniature I. Magnin & Co. Building.

    blender -b --python build_i_magnin_building.py -- [--out DIR]

50 Grant Avenue at Geary (I. Magnin & Co.'s San Francisco store from 1912
until the move to Union Square in 1948): an eight-storey department-store
block faced in white glazed terracotta - a tight grid of slender piers and
very large dark multi-pane windows, a delicate frieze and a flat cornice,
iron fire-escape balconies on Geary, and a plainer, taller white block rising
behind at the south-east. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "i-magnin-building"
CENTER = (-122.4047095, 37.7875147)   # OSM way 149335991, OBB centre
H_TOP = 50.5                           # LiDAR max 50.54 m = the rear block (DataSF 2010, parcel 0312008)
H_MAIN = 44.0                          # main block parapet: OSM 43, LiDAR median 42.8 / mode 47.3 (see REFERENCE)
YAW = tk.bearing_to_yaw(81.0)          # local +x = bearing 81 (street grid), +y = 351

# OSM outline in local metres. West face (x = -15.4) = Grant Avenue, north
# face (y = 23.3) = Geary Street; the south-east corner is cut by lot lines.
LOCAL = [(-15.4, -23.3), (0.6, -23.4), (9.3, -17.0), (9.9, -4.4), (15.4, -0.7), (15.4, 23.3), (-15.4, 23.3)]
REAR = [(-3.0, -20.2), (0.6, -21.6), (8.0, -16.4), (8.4, -5.0), (-3.0, -5.0)]
Z_SHOP, Z_CORN = 6.5, 42.0


def is_street(nrm):
    lx, ly = tk.rot2(nrm, -YAW)
    return lx < -0.7 or ly > 0.7


def street(ei, p0, p1, nrm):
    return is_street(nrm)


def street_piers(name, plan, z0, z1, spacing, w, d, mat):
    """Slender terracotta piers on the two street faces."""
    objs = []
    for k, (p0, p1, ln, nrm) in enumerate(tk.edges(plan)):
        if not is_street(nrm):
            continue
        n = int(round(ln / spacing))
        ux, uy = (p1[0] - p0[0]) / ln, (p1[1] - p0[1]) / ln
        for i in range(n + 1):
            t = w / 2 + (ln - w) * i / n
            cx, cy = p0[0] + ux * t + nrm[0] * d / 2, p0[1] + uy * t + nrm[1] * d / 2
            objs.append(tk.box(f"{name}_{k}_{i}", cx, cy, z0, z1, w * (1.8 if i in (0, n) else 1.0), d, mat,
                               yaw=YAW))
    return tk.join(objs, name)


def lbox(name, x, y, z0, z1, sx, sy, mat):
    c = tk.rot2((x, y), YAW)
    return tk.box(name, c[0], c[1], z0, z1, sx, sy, mat, yaw=YAW, bev=0.06)


def build():
    plan = tk.ccw(tk.xform(LOCAL, YAW))
    rear = tk.ccw(tk.xform(REAR, YAW))
    # shop floor: tall display windows behind white piers
    tk.prism("shop", plan, 0.0, Z_SHOP, "white", bev=0.12)
    tk.panes("shop_win", plan, [(0.4, Z_SHOP - 0.6)], 5.6, mat="glassd", gap=1.4, margin=0.2, edge_filter=street)
    tk.lit_windows("shop_lit", plan, [(0.4, Z_SHOP - 0.9)], 5.6, 0.8, seed=1.0, out=0.1, margin=0.3, gap=1.6,
                   edge_filter=street)
    # seven storeys of big multi-pane windows in a white terracotta grid
    tk.punched_block("body", plan, Z_SHOP, Z_CORN, 5.07, wall="white", win="glassd", spacing=5.6, gap=1.5,
                     margin=0.7, lit=0.3, seed=5.0, bev=0.12)
    street_piers("piers", plan, Z_SHOP, Z_CORN, 5.6, 0.7, 0.35, "white")
    # frieze, flat cornice and parapet
    tk.ring_band("frieze", plan, Z_CORN - 1.0, Z_CORN, 0.4, "cream")
    tk.cornice("cornice", plan, Z_CORN, h=1.1, out=0.8, mat="white")
    tk.prism("roof", tk.offset_poly(plan, -0.3), Z_CORN + 1.0, Z_CORN + 1.25, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), Z_CORN + 1.1, H_MAIN, 0.4, "white")
    # iron fire-escape balconies on the Geary front (one stack, two bays)
    for k, z in enumerate([Z_SHOP + 5.07 * i for i in range(1, 7)]):
        lbox(f"fire_escape_{k}", -1.0, 23.75, z - 0.2, z + 0.9, 7.0, 0.9, "ink")
    # the taller rear block (plain white, smaller windows) and its roof
    tk.punched_block("rear", rear, H_MAIN - 1.0, H_TOP - 1.4, 3.6, wall="white", win="glassd", spacing=2.6,
                     gap=1.1, margin=0.8, lit=0.3, seed=9.0, bev=0.12)
    tk.prism("rear_roof", tk.offset_poly(rear, -0.2), H_TOP - 1.5, H_TOP - 1.3, "roofd")
    tk.ring_band("rear_parapet", tk.offset_poly(rear, -0.4), H_TOP - 1.4, H_TOP, 0.4, "white")
    c = tk.rot2((-6.0, 10.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], Z_CORN + 1.25, YAW, 12.0, 12.0, seed=3.0, hmax=1.6, fans=False)
    tk.glow_ring("crown_light", plan, Z_CORN - 0.8, Z_CORN - 0.3, 0.45, "white_Glow")
    tk.plinth("plaza", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
