"""Deterministic Blender build of the SF-SIM miniature Galleria Park Hotel.

    blender -b --python build_191_sutter_street.py -- [--out DIR]

191 Sutter Street (opened December 1911 as the Hotel Sutter): an eight-storey
hotel on the south side of Sutter between Kearny and the Crocker Galleria. A
two-storey base re-clad in grey granite with a red-awninged restaurant and a
flat metal entrance canopy, six storeys of tan brick with deep-set paired
windows and a few iron balconies, a deep dark bracketed cornice, and a tall
"GALLERIA PARK HOTEL" blade sign. Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "191-sutter-street"
CENTER = (-122.4035139, 37.7896066)   # OSM way 132125160, OBB centre
H_TOP = 32.1                           # LiDAR median roof (DataSF 2010, parcel 0292009); OSM 32
YAW = tk.bearing_to_yaw(81.0)          # local +x = bearing 81 (street grid), +y = 351

# OSM rectangle 30.7 x 37.3 m (local). North face (y = +18.6) = Sutter
# Street, 10 m off the OSM centreline; east/west are party walls, south is
# the rear light-court side.
X0, X1, Y0, Y1 = -15.4, 15.3, -18.6, 18.6
Z_BASE, Z_CORN = 8.6, 29.6


def front(ei, p0, p1, nrm):
    return tk.rot2(nrm, -YAW)[1] > 0.7


def not_party(ei, p0, p1, nrm):
    return abs(tk.rot2(nrm, -YAW)[0]) < 0.7


def lbox(name, x, y, z0, z1, sx, sy, mat):
    c = tk.rot2((x, y), YAW)
    return tk.box(name, c[0], c[1], z0, z1, sx, sy, mat, yaw=YAW, bev=0.08)


def build():
    plan = tk.ccw(tk.xform([(X0, Y0), (X1, Y0), (X1, Y1), (X0, Y1)], YAW))
    # two-storey granite base (Sutter front) over a plain stone podium
    tk.prism("base", plan, 0.0, Z_BASE, "stone", bev=0.12)
    face = tk.ccw(tk.xform([(X0, Y1 - 0.3), (X1, Y1 - 0.3), (X1, Y1 + 0.35), (X0, Y1 + 0.35)], YAW))
    tk.prism("granite", face, 0.0, Z_BASE, "steel", bev=0.08)
    tk.panes("shop", face, [(0.3, 4.6)], 5.1, mat="glassd", gap=1.6, margin=0.2, edge_filter=front)
    tk.lit_windows("shop_lit", face, [(0.3, 4.4)], 5.1, 0.85, seed=2.0, out=0.1, margin=0.3, gap=1.8,
                   edge_filter=front)
    tk.panes("mezz", face, [(5.2, 8.0)], 5.1, mat="glassd", gap=2.4, margin=0.3, edge_filter=front)
    tk.ring_band("base_band", plan, Z_BASE - 0.4, Z_BASE + 0.2, 0.55, "steel")
    # red restaurant awning (east) and the flat hotel canopy (west of centre)
    lbox("awning", 9.0, Y1 + 1.6, 3.4, 4.4, 5.0, 2.6, "red")
    lbox("canopy", -2.5, Y1 + 2.2, 3.9, 4.4, 8.5, 4.0, "steel")
    # tan brick shaft, six storeys of deep-set windows
    tk.punched_block("shaft", plan, Z_BASE + 0.2, Z_CORN, 3.43, wall="stone", win="glassd", spacing=2.55,
                     gap=1.15, margin=0.75, lit=0.33, seed=6.0, bev=0.12, edge_filter=not_party)
    # wrought-iron balconies on the Sutter front
    for i, (x, z) in enumerate([(-11.0, 12.6), (-11.0, 22.9), (11.0, 12.6), (11.0, 22.9), (0.0, 19.5)]):
        lbox(f"balcony_{i}", x, Y1 + 0.55, z, z + 1.0, 3.2, 1.1, "ink")
    # deep bracketed cornice (painted dark) and parapet
    tk.ring_band("frieze", plan, Z_CORN - 0.9, Z_CORN, 0.25, "stone")
    tk.cornice("cornice", plan, Z_CORN, h=1.4, out=1.5, mat="roofd")
    tk.prism("roof", tk.offset_poly(plan, -0.4), Z_CORN + 1.3, Z_CORN + 1.5, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.5), Z_CORN + 1.4, H_TOP - 0.9, 0.5, "stone")
    c = tk.rot2((2.0, -6.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], Z_CORN + 1.5, YAW, 12.0, 10.0, seed=4.0, hmax=H_TOP - Z_CORN - 1.5,
                    fans=False)
    # vertical "GALLERIA PARK HOTEL" blade sign near the west end of the front
    lbox("blade", X0 + 3.0, Y1 + 1.6, 9.5, 18.5, 0.45, 2.2, "navy")
    for side in (-1, 1):
        nrm = tk.rot2((side * 1.0, 0.0), YAW)
        a = tk.rot2((X0 + 3.0 + side * 0.25, Y1 + 1.6 - side * 0.85), YAW)
        b = tk.rot2((X0 + 3.0 + side * 0.25, Y1 + 1.6 + side * 0.85), YAW)
        tk.flat_quad(f"blade_{'e' if side > 0 else 'w'}_glow", a, b, 10.0, 18.0, 0.02, "white_Glow", nrm)
    tk.glow_ring("crown_light", plan, Z_CORN - 0.85, Z_CORN - 0.35, 0.3, "sand_Glow")
    tk.plinth("plaza", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
