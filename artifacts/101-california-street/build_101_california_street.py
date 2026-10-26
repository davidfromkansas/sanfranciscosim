"""Deterministic Blender build of the SF-SIM miniature 101 California Street.

    blender -b --python build_101_california_street.py -- [--out DIR]

101 California Street (Johnson/Burgee, 1982): a 48-storey faceted cylinder in
pale rose granite with continuous dark ribbon windows, rising beside a
triangular low annex whose diagonal face carries the famous seven-storey
sloping glass atrium lobby facing the granite plaza at California and Davis.
Recognition cues: the round banded shaft (unique downtown) and the glass
lean-to at its foot. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "101-california-street"
CENTER = (-122.3981195, 37.7929555)   # OSM way 1279505488, OBB centre
H_TOP = 183.0                          # published roof (Wikipedia 183 m); LiDAR 175.24 (main roof)
H_ROOF = 175.0                         # LiDAR main roof; two stepped crown tiers rise to 183
H_ANNEX = 36.0                         # INFERRED: pale granite annex, ~9 storeys (photo)
H_COLS = 28.0                          # INFERRED: seven-storey colonnade / atrium height (photo)
YAW = tk.bearing_to_yaw(81.3)          # local +x = bearing 81.3 (California St), +y = 351.3

TC = (13.1, -10.9)                     # tower centre, least-squares fit of the 100-node serrated arc
R = 27.7                               # fitted radius (arc nodes 25.7-30.6 m: the serrations)
SEG = 28

# triangular annex (local), from the OSM outline west of the tower: Front St = west face,
# Pine St = south face, the diagonal faces the plaza (NE)
ANNEX = [(-41.6, 41.6), (-41.6, -41.3), (-11.4, -41.6), (-11.5, -26.6), (8.0, -12.0), (-6.4, 7.5)]


def build():
    cx, cy = tk.rot2(TC, YAW)
    ring = [(cx + R * math.cos(2 * math.pi * (i + 0.5) / SEG), cy + R * math.sin(2 * math.pi * (i + 0.5) / SEG))
            for i in range(SEG)]
    # seven-storey colonnade: the shaft stands on tall square columns over a recessed lobby
    lobby = tk.offset_poly(ring, -4.0)
    tk.prism("tower_lobby", lobby, 0.0, H_COLS, "glassl")
    tk.glow_ring("tower_lobby_lit", lobby, 0.8, H_COLS - 2.0, 0.06, "sand_Glow")
    for i in range(0, SEG, 2):
        a = 2 * math.pi * (i + 0.5) / SEG
        px, py = cx + (R - 1.3) * math.cos(a), cy + (R - 1.3) * math.sin(a)
        tk.box(f"col{i}", px, py, 0.0, H_COLS, 1.8, 1.8, "stone", yaw=a)
    tk.prism("soffit", ring, H_COLS, H_COLS + 1.5, "stone")
    # blue glass shaft: thin pale mullion line every two storeys over the faceted cylinder
    tk.prism("tower", ring, H_COLS + 1.5, H_ROOF, "glass")
    bands = tk.floors(H_COLS + 1.5, H_ROOF, 7.1364)    # 20 two-storey bands
    tk.panes("tower_lines", ring, [(z0, z0 + 0.6) for z0, _ in bands], 5.5, mat="glassl", out=0.06,
             margin=0.0, gap=0.0)
    tk.lit_windows("tower_win", ring, [(z0 + 0.6, z1) for z0, z1 in bands], 5.5, 0.3, seed=3.0, out=0.12,
                   margin=0.6, gap=1.2)
    # stepped crown: two setback tiers with a crown light, plant on the top deck
    r1, r2 = tk.offset_poly(ring, -2.5), tk.offset_poly(ring, -6.0)
    tk.prism("crown1", r1, H_ROOF, H_ROOF + 4.0, "glass")
    tk.prism("crown2", r2, H_ROOF + 4.0, H_TOP, "glass")
    tk.prism("ledge1", tk.offset_poly(ring, -0.2), H_ROOF - 0.2, H_ROOF + 0.25, "glassl")
    tk.prism("ledge2", tk.offset_poly(r1, -0.2), H_ROOF + 3.8, H_ROOF + 4.25, "glassl")
    tk.prism("roof_deck", tk.offset_poly(r2, -0.4), H_TOP - 0.4, H_TOP - 0.1, "roofd")
    tk.ring_band("crown_rim", tk.offset_poly(r2, -0.4), H_TOP - 0.4, H_TOP, 0.4, "glassl")
    tk.glow_ring("crown_light", r1, H_ROOF + 1.0, H_ROOF + 1.8, 0.1, "white_Glow")
    # triangular annex
    annex = tk.ccw(tk.xform(ANNEX, YAW))
    tk.punched_block("annex", annex, 0.0, H_ANNEX, 4.0, wall="stone", win="glassd", spacing=4.2,
                     gap=1.4, margin=0.9, lit=0.35, seed=8.0, bev=0.15,
                     edge_filter=lambda ei, p0, p1, n: abs(n[0] * DIAG_N[0] + n[1] * DIAG_N[1]) < 0.9)
    tk.prism("annex_deck", tk.offset_poly(annex, -0.5), H_ANNEX - 0.2, H_ANNEX + 0.1, "roofd")
    tk.ring_band("annex_parapet", tk.offset_poly(annex, -0.5), H_ANNEX, H_ANNEX + 1.0, 0.5, "stone")
    # roof garden on the annex
    gx, gy = tk.rot2((-28.0, -26.0), YAW)
    tk.box("annex_garden", gx, gy, H_ANNEX + 0.1, H_ANNEX + 0.6, 14.0, 14.0, "leafd", yaw=YAW)
    # the sloping glass atrium on the annex's diagonal (plaza) face
    a, b = tk.xform([(-6.4, 7.5), (-41.6, 41.6)], YAW)
    ux, uy = DIAG_N
    a = (a[0] - ux * 0.3, a[1] - uy * 0.3)
    b = (b[0] - ux * 0.3, b[1] - uy * 0.3)
    run = 16.0
    foot = [(a[0] + ux * run, a[1] + uy * run), (b[0] + ux * run, b[1] + uy * run)]
    verts = [(a[0], a[1], 0.0), (b[0], b[1], 0.0), (foot[1][0], foot[1][1], 0.0), (foot[0][0], foot[0][1], 0.0),
             (a[0], a[1], H_COLS), (b[0], b[1], H_COLS)]
    faces = [(0, 3, 2, 1), (3, 4, 5, 2), (0, 4, 3), (1, 2, 5), (0, 1, 5, 4)]
    tk.new_mesh("atrium", verts, faces, ["glassl"])
    # lit atrium skin just outside the sloped glass
    off = 0.12
    sl = (ux * off * 0.95, uy * off * 0.95, off * 0.3)
    gv = [(foot[0][0] + sl[0], foot[0][1] + sl[1], 1.0 + sl[2]), (foot[1][0] + sl[0], foot[1][1] + sl[1], 1.0 + sl[2])]
    t = 1.0 - (H_COLS - 3.0) / H_COLS
    top0 = (a[0] + ux * run * t + sl[0], a[1] + uy * run * t + sl[1], H_COLS - 3.0 + sl[2])
    top1 = (b[0] + ux * run * t + sl[0], b[1] + uy * run * t + sl[1], H_COLS - 3.0 + sl[2])
    tk.new_mesh("atrium_lit_glow", [gv[0], top0, top1, gv[1]], [(0, 3, 2, 1)], ["sand_Glow"], recalc=False)
    # mullion ribs over the atrium slope
    for k in range(1, 8):
        t = k / 8
        p = (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
        tk.tube(f"atrium_rib{k}", (p[0] + ux * (run - 0.2), p[1] + uy * (run - 0.2), 0.4), (p[0], p[1], H_COLS),
                0.35, 0.4, (ux, uy), "steel")
    # plaza: granite apron over the whole site with the planting terraces and trees
    site = tk.xform(tk.rect(83.2, 83.2), YAW)
    tk.prism("plaza", site, 0.0, 0.3, "stone", bev=0.1)
    for k, (px, py, s) in enumerate(((10.0, 30.0, 9.0), (30.0, 25.0, 7.0), (28.0, 36.0, 6.0))):
        bx, by = tk.rot2((px, py), YAW)
        tk.box(f"terrace{k}", bx, by, 0.3, 0.3 + 0.5 * (k + 1), s, s, "leafd", yaw=YAW, bev=0.1)
    p0, p1 = tk.xform([(-30.0, 38.0), (36.0, 38.0)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 5, h=6.5, seed=6.6)


_dx, _dy = -41.6 - (-6.4), 41.6 - 7.5
_dl = math.hypot(_dx, _dy)
# outward (NE) normal of the diagonal, in world coordinates
DIAG_N = tk.rot2((_dy / _dl, -_dx / _dl), YAW)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
