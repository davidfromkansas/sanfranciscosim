"""Deterministic Blender build of the SF-SIM miniature Hunter-Dulin Building.

    blender -b --python build_hunter_dulin_building.py -- [--out DIR]

111 Sutter Street (Schultze & Weaver, 1927): a 22-storey buff terracotta office
tower in a French chateau / Romanesque dress. Above a plain shaft of punched
windows the block splits into two corner pavilions with steep brown hipped roofs,
copper-green cresting and dormers, with a lower flat-topped centre bay between
them. Recognition cues: the twin chateau roofs and the warm buff colour.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "hunter-dulin-building"
CENTER = (-122.4025497, 37.7897258)  # OSM way 942664247, OBB centre
H_TOP = 93.88                         # published roof (Wikipedia infobox 93.88 m); LiDAR 93.98 m
H_SHAFT = 66.0                        # main cornice (inferred from photo: ~17 of 22 storeys)
H_PAV = 80.0                          # pavilion eaves (inferred)
H_MID = 78.0                          # centre bay roof (inferred)
L, W = 49.6, 33.2                     # OSM OBB
YAW = math.radians(9.08)              # local +x along Sutter (bearing 80.9); +y = Sutter face (N)
PW = 15.0                             # pavilion width along Sutter


def R(w, d, cx=0.0, cy=0.0):
    return tk.xform(tk.rect(w, d, cx, cy), YAW)


def hip_roof(name, w, d, cx, z0, z1, mat):
    """Steep hipped chateau roof on a w x d pavilion: a frustum to a short ridge."""
    lo = R(w + 0.8, d + 0.8, cx)
    hi = R(1.2, d * 0.22, cx)
    tk.frustum(name, tk.ccw(lo), z0, tk.ccw(hi), z1, mat)


def build():
    plan = R(L, W)
    # base: a taller ground storey of dark shopfront glass under a stone band
    tk.prism("base", plan, 0.0, 7.5, "terracotta", bev=0.15)
    tk.panes("base_shops", plan, [(0.4, 6.4)], 5.0, mat="glassd", gap=1.0, margin=0.3)
    tk.lit_windows("base_lit", plan, [(0.4, 6.0)], 5.0, 0.8, seed=2.0, out=0.1, margin=0.5, gap=1.4)
    tk.ring_band("base_band", plan, 7.5, 8.5, 0.35, "cream")
    # shaft: buff terracotta with paired punched windows (16 storeys of 3.6 m)
    tk.punched_block("shaft", plan, 8.5, H_SHAFT, (H_SHAFT - 8.5) / 16, wall="terracotta", win="glassd",
                     spacing=3.6, gap=1.4, margin=0.9, lit=0.3, seed=4.0, bev=0.12)
    tk.cornice("shaft_cornice", plan, H_SHAFT, h=1.0, out=0.6, mat="cream")
    # upper tier: two corner pavilions with a recessed, lower centre bay between them
    for k, sx in enumerate((-1, 1)):
        cx = sx * (L / 2 - PW / 2)
        pav = R(PW, W, cx)
        tk.punched_block(f"pav_{k}", pav, H_SHAFT + 1.0, H_PAV, (H_PAV - H_SHAFT - 1.0) / 4, wall="terracotta",
                         win="glassd", spacing=3.4, gap=1.3, margin=0.8, lit=0.35, seed=7.0 + k, bev=0.12)
        tk.ring_band(f"pav_crest_{k}", pav, H_PAV, H_PAV + 0.8, 0.5, "verdigris")
        hip_roof(f"pav_roof_{k}", PW, W, cx, H_PAV + 0.8, H_TOP - 0.6, "rust")
        # dormers on the long roof slopes and copper finials on the corners
        for j, dy in enumerate((-W / 4, W / 4)):
            for side in (-1, 1):
                c = tk.rot2((cx + side * (PW / 2 - 2.4), dy), YAW)
                tk.box(f"dormer_{k}_{j}_{side}", c[0], c[1], H_PAV + 1.0, H_PAV + 3.8, 1.8, 2.6, "terracotta",
                       yaw=YAW, bev=0.1)
        for j, (ux, uy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))):
            c = tk.rot2((cx + ux * (PW / 2 + 0.2), uy * (W / 2 + 0.2)), YAW)
            tk.cylinder(f"finial_{k}_{j}", c[0], c[1], H_PAV + 0.8, H_PAV + 4.0, 0.45, "verdigris", seg=6, r1=0.1)
        rc = tk.rot2((cx, 0.0), YAW)
        tk.box(f"ridge_crest_{k}", rc[0], rc[1], H_TOP - 0.6, H_TOP, 0.5, W * 0.22, "verdigris", yaw=YAW)
    mid = R(L - 2 * PW, W - 6.0, 0.0, 0.0)
    tk.punched_block("mid", mid, H_SHAFT + 1.0, H_MID, (H_MID - H_SHAFT - 1.0) / 3, wall="terracotta",
                     win="glassd", spacing=3.4, gap=1.3, margin=0.8, lit=0.3, seed=11.0, bev=0.1)
    tk.ring_band("mid_crest", mid, H_MID, H_MID + 0.7, 0.4, "verdigris")
    tk.prism("mid_roof", tk.offset_poly(mid, -0.3), H_MID - 0.3, H_MID + 0.05, "roofd")
    tk.hvac_cluster("mid_plant", 0.0, 0.0, H_MID, YAW, 12.0, 14.0, seed=3.0, hmax=3.0)
    # the deck between pavilions and centre bay, front and back
    for sy in (-1, 1):
        c = tk.rot2((0.0, sy * (W / 2 - 1.5)), YAW)
        tk.box(f"terrace_{sy}", c[0], c[1], H_SHAFT + 0.9, H_SHAFT + 1.2, L - 2 * PW, 3.0, "roofd", yaw=YAW)
    # warm floodlight on the pavilion roofs at night
    for k, sx in enumerate((-1, 1)):
        tk.glow_ring(f"pav_light_{k}", R(PW, W, sx * (L / 2 - PW / 2)), H_PAV - 1.4, H_PAV - 0.6, 0.62, "sand_Glow")
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
