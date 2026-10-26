"""Deterministic Blender build of the SF-SIM miniature Hallidie Building.

    blender -b --python build_130_150_sutter_street.py -- [--out DIR]

130-150 Sutter Street (Willis Polk, 1918; SF Landmark #37, NRHP): a
seven-storey office building whose Sutter Street front is one of the first
glass curtain walls in the US - a sheer grid of glass hung in front of the
structure, painted dark blue, laced with gilded cast-iron bands, framed by
stacked semicircular fire-escape balconies at both ends and crowned by a
gilded cornice with a row of finials. The other three sides are plain party
and light-court walls. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "130-150-sutter-street"
CENTER = (-122.4030688, 37.7902105)   # OSM way 151195286, OBB centre
H_TOP = 30.3                           # LiDAR median roof (DataSF 2010, parcel 0288027); OSM 30
YAW = tk.bearing_to_yaw(260.6)         # local +x = bearing 260.6 (street grid, west), +y = 170.6 (south)

# OSM outline in local metres, authored facing the street: local +y points
# SOUTH, so the front (y = 22.75) is the Sutter Street face - the building
# stands on the north side of Sutter (OSM centreline 7 m off the edge). The
# 32 x 45 m lot widens by 2.4 m at the rear (north) court.
LOCAL = [(14.8, 22.75), (-17.3, 22.75), (-17.1, -22.7), (17.2, -22.7), (17.2, -8.9), (14.8, -8.9)]
XW, XE, YN = -17.3, 14.8, 22.75
H_ROOF = 28.3                          # roof deck behind the cornice
# storey lines of the glass front (photo): storefront, mezzanine, 4 office
# floors, top floor, then the cornice
Z_SHOP, Z_MEZZ, Z_TOPF, Z_CORN = 5.0, 9.0, 23.6, 27.6


def front_box(name, x0, x1, z0, z1, out, depth, mat):
    """A box on the Sutter front: spans local x0..x1, stands `out` proud."""
    cx, cy = tk.rot2(((x0 + x1) / 2, YN + out - depth / 2), YAW)
    return tk.box(name, cx, cy, z0, z1, x1 - x0, depth, mat, yaw=YAW)


def build():
    plan = tk.ccw(tk.xform(LOCAL, YAW))
    # plain body: light party walls, punched windows on the rear (north) court side only
    tk.prism("body", plan, 0.0, H_ROOF, "sand", bev=0.15)
    rear = lambda ei, p0, p1, nrm: tk.rot2(nrm, -YAW)[1] < -0.7  # noqa: E731
    tk.panes("rear_win", plan, tk.floors(Z_MEZZ, Z_CORN, 3.65), 3.0, mat="glassd", gap=1.2, margin=0.8,
             edge_filter=rear)
    # the curtain wall: a dark-blue frame slab with a grid of pale glass panes
    front = tk.ccw(tk.xform([(XW, YN - 0.2), (XE, YN - 0.2), (XE, YN + 0.5), (XW, YN + 0.5)], YAW))
    tk.prism("frame", front, Z_SHOP, Z_CORN, "navy")
    front_f = lambda ei, p0, p1, nrm: tk.rot2(nrm, -YAW)[1] > 0.7  # noqa: E731
    bands = [(Z_SHOP + 0.6, Z_MEZZ - 0.6)] + tk.floors(Z_MEZZ + 0.6, Z_TOPF - 0.4, 3.5) + [(Z_TOPF + 0.4, Z_CORN - 0.5)]
    tk.panes("glass", front, bands, 1.75, mat="glassl", gap=0.22, margin=0.12, edge_filter=front_f)
    lit_front = tk.ccw(tk.xform([(XW + 4.0, YN - 0.2), (XE - 4.0, YN - 0.2), (XE - 4.0, YN + 0.5), (XW + 4.0, YN + 0.5)], YAW))
    tk.lit_windows("glass_lit", lit_front, bands, 3.5, 0.45, seed=3.0, out=0.1, margin=0.3, gap=0.4,
                   edge_filter=front_f)
    # storefront: inset dark glass with a warm lit band
    shop = tk.ccw(tk.xform([(XW + 0.6, YN - 1.2), (XE - 0.6, YN - 1.2), (XE - 0.6, YN + 0.3), (XW + 0.6, YN + 0.3)], YAW))
    tk.prism("shop", shop, 0.0, Z_SHOP, "glassd")
    tk.lit_windows("shop_lit", shop, [(0.3, Z_SHOP - 0.6)], 4.0, 0.9, seed=1.0, out=0.06, margin=0.3,
                   gap=0.6, edge_filter=front_f)
    # gilded cast-iron bands (two at the mezzanine, one under the top floor,
    # a deep cornice frieze) and the gilded cresting with finials
    for i, (z0, z1) in enumerate([(Z_SHOP - 0.2, Z_SHOP + 0.7), (Z_MEZZ - 0.4, Z_MEZZ + 0.5),
                                  (Z_TOPF - 0.4, Z_TOPF + 0.4), (Z_CORN - 0.5, Z_CORN + 0.9)]):
        front_box(f"gilt_{i}", XW - 0.2, XE + 0.2, z0, z1, 1.0 if i == 3 else 0.8, 0.6, "gold")
    front_box("cornice", XW - 0.3, XE + 0.3, Z_CORN + 0.9, H_ROOF + 0.8, 1.2, 1.1, "navy")
    front_box("cresting", XW, XE, H_ROOF + 0.8, H_ROOF + 1.3, 0.9, 0.4, "gold")
    n = 15
    for i in range(n):
        x = XW + 0.6 + (XE - XW - 1.2) * i / (n - 1)
        h = 2.0 if i == n // 2 else 1.0
        cx, cy = tk.rot2((x, YN + 0.7), YAW)
        tk.pyramid(f"finial_{i}", tk.xform(tk.rect(0.45, 0.45), YAW, cx, cy), H_ROOF + 1.3, H_ROOF + h, "gold")
    # stacked semicircular fire-escape balconies at both ends of the front
    for side, x in (("w", XW + 2.4), ("e", XE - 2.4)):
        for k, z in enumerate([Z_MEZZ + 2.2, Z_MEZZ + 5.7, Z_MEZZ + 9.2, Z_MEZZ + 12.7]):
            cx, cy = tk.rot2((x, YN + 0.5), YAW)
            tk.cylinder(f"balcony_{side}{k}", cx, cy, z, z + 1.0, 1.25, "gold", seg=8)
    # the gilded side returns of the frame
    for side, x in (("w", XW), ("e", XE)):
        front_box(f"jamb_{side}", x - 0.35, x + 0.35, Z_SHOP, Z_CORN, 0.8, 0.8, "gold")
    # roof: deck with low plant, white crown light on the cornice
    tk.prism("deck", tk.offset_poly(plan, -0.3), H_ROOF - 0.2, H_ROOF + 0.05, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), H_ROOF, H_ROOF + 0.8, 0.4, "sand")
    pc = tk.rot2((2.0, -6.0), YAW)
    tk.hvac_cluster("plant", pc[0], pc[1], H_ROOF + 0.05, YAW, 12.0, 14.0, seed=2.0, hmax=1.9)
    cx, cy = tk.rot2(((XW + XE) / 2, YN + 1.25), YAW)
    p0, p1 = tk.rot2((XE, 0), YAW), tk.rot2((XW, 0), YAW)  # right-to-left so the quad faces out
    nrm = tk.rot2((0.0, 1.0), YAW)
    tk.flat_quad("crown_glow", (p0[0] + cx - (p0[0] + p1[0]) / 2, p0[1] + cy - (p0[1] + p1[1]) / 2),
                 (p1[0] + cx - (p0[0] + p1[0]) / 2, p1[1] + cy - (p0[1] + p1[1]) / 2),
                 Z_CORN + 1.0, Z_CORN + 1.5, 0.0, "white_Glow", nrm)
    tk.plinth("plaza", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
