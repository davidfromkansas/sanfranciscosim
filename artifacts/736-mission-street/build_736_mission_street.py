"""Deterministic Blender build of the SF-SIM miniature Contemporary Jewish Museum.

    blender -b --python build_736_mission_street.py -- [--out DIR]

736 Mission Street on Jessie Square: Willis Polk's 1907 Jessie Street
Substation (red brick, white terracotta cornice, a tall round-arched window)
gutted and extended by Daniel Libeskind in 2008 with a tilted blue-steel cube
(the "Yud") over a dark slanted wing (the "Chet") at the south-west end.
Footprint is the OSM museum way split at its setback. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "736-mission-street"
CENTER = (-122.4036847, 37.7860037)   # OSM way 118106934, OBB centre
H_TOP = 24.0                          # MEASURED: LiDAR max 24.05 m (the blue cube); median 13.95 = substation roof
H_HALL = 13.2                         # substation wall top under the cornice (LiDAR median 14.0 incl. cornice/roof)

# OSM footprint split at the setback (metres from CENTER, +x east, +y north)
SUBSTATION = [(1.6, -12.9), (37.7, 22.6), (33.7, 26.5), (20.7, 39.6), (-15.3, 4.2)]
ADDITION = [(-17.4, -37.2), (-13.2, -27.4), (1.6, -12.9), (-15.3, 4.2), (-37.5, -17.5),
            (-31.9, -25.0), (-32.3, -26.5), (-25.5, -34.8)]
FULL = [(-17.4, -37.2), (-25.5, -34.8), (-32.3, -26.5), (-31.9, -25.0), (-37.5, -17.5), (1.0, 20.2),
        (20.7, 39.6), (33.7, 26.5), (37.7, 22.6), (1.6, -12.9), (-13.2, -27.4)]
U = (0.7071, 0.7071)                  # along Mission (bearing 45)


def front(ei, p0, p1, nrm):
    """The long SE (Jessie Square / Mission) face of the substation."""
    return nrm[0] > 0.5 and nrm[1] < -0.5 and math.dist(p0, p1) > 40


def tilted_block(name, poly, z0, ztop_fn, lean, mat):
    """Prism whose top follows ztop_fn(x, y) and whose top ring is shifted by `lean`."""
    poly = tk.ccw(poly)
    n = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x + lean[0], y + lean[1], ztop_fn(x, y)) for x, y in poly]
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces.append(tuple(range(n - 1, -1, -1)))
    faces.append(tuple(range(n, 2 * n)))
    return tk.new_mesh(name, verts, faces, [mat])


def build():
    sub = tk.ccw(SUBSTATION)
    # --- Jessie Street Substation: brick hall, granite base, white cornice
    tk.prism("hall_base", tk.offset_poly(sub, 0.15), 0.0, 1.2, "stone")
    tk.prism("hall", sub, 1.2, H_HALL, "brick", bev=0.1)
    tk.cornice("hall_cornice", sub, H_HALL, h=1.0, out=0.7, mat="cream")
    tk.prism("hall_roof", tk.offset_poly(sub, -0.4), H_HALL + 0.6, H_HALL + 1.1, "roofd")
    tk.prism("skylight", tk.xform(tk.rect(26.0, 6.0), math.radians(45), 11.0, 13.0), H_HALL + 1.1, H_HALL + 1.9,
             "glassl", bev=0.1)
    # the great arched window near the NE end and the central portal, on the SE front
    for p0, p1, L, nrm in tk.edges(sub):
        if not front(0, p0, p1, nrm):
            continue
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L

        def seg(t, w):
            c = (p0[0] + ux * L * t, p0[1] + uy * L * t)
            return [(c[0] - ux * w / 2, c[1] - uy * w / 2), (c[0] + ux * w / 2, c[1] + uy * w / 2)]
        # tk.arched_panes works on a polygon's edges: give it a 2-point "edge" via a thin triangle
        for tag, t, w, z0, z1 in (("arch", 0.80, 7.0, 1.2, 12.0), ("portal", 0.45, 4.0, 1.2, 6.0)):
            a, b = seg(t, w + 2.0)
            frame_c = ((a[0] + b[0]) / 2 + nrm[0] * 0.25, (a[1] + b[1]) / 2 + nrm[1] * 0.25)
            tk.box(tag + "_frame", frame_c[0], frame_c[1], 1.2, z1 + 0.8, w + 2.0, 0.5, "cream",
                   yaw=math.atan2(uy, ux))
            fr = tk.xform(tk.rect(w + 2.0, 0.5), math.atan2(uy, ux), frame_c[0], frame_c[1])
            face = lambda ei, q0, q1, nn: nn[0] * nrm[0] + nn[1] * nrm[1] > 0.9  # noqa: E731
            tk.arched_panes(tag + "_glass", fr, z0, z1, w + 2.0, w, mat="glassd", out=0.03, edge_filter=face)
            tk.arched_panes(tag + "_lit", fr, z0 + 0.3, z1 - 1.0, w + 2.0, w - 1.6, mat="sand_Glow", out=0.07,
                            edge_filter=face, suffix="_glow")
    # tall upper windows along the hall (the brick is otherwise blank), lit at night
    tk.lit_windows("hall_lit", sub, [(8.0, 11.6)], 6.0, 0.5, seed=7.0, out=0.08, margin=0.2, gap=3.6,
                   edge_filter=lambda ei, p0, p1, nrm: not front(ei, p0, p1, nrm) and math.dist(p0, p1) > 20
                   and not (nrm[0] < -0.5 and nrm[1] < -0.5))

    # --- Libeskind addition: dark slanted "Chet" wing
    add = tk.ccw(ADDITION)
    tk.prism("chet", add, 0.0, 1.0, "ink")
    tilted_block("chet_body", tk.offset_poly(add, -0.2), 1.0,
                 lambda x, y: 9.0 + 0.10 * ((x + 15.3) * U[0] + (y - 4.2) * U[1]) + 3.0, (0.0, 0.0), "ink")
    tk.lit_windows("chet_lobby", add, [(0.3, 5.0)], 4.0, 0.7, seed=3.0, out=0.08, margin=0.4, gap=1.0,
                   edge_filter=lambda ei, p0, p1, nrm: nrm[1] < 0.3 and math.dist(p0, p1) > 6)

    # --- the blue "Yud" cube, tilted and leaning out toward Jessie Square
    cx, cy = -20.0, -17.0
    yud = tk.xform(tk.rect(17.0, 17.0), math.radians(45 + 14), cx, cy)

    def ztop(x, y):  # roof plane rising to the SW corner
        return 21.63 - 0.20 * ((x - cx) * U[0] + (y - cy) * U[1]) + 0.05 * ((x - cx) * -U[1] + (y - cy) * U[0])
    tilted_block("yud", yud, 4.0, ztop, (-0.6, -1.0), "sky")
    # the scatter of small square windows on the cube's skin
    for k in range(9):
        h = tk.hash01(k * 3.7 + 1.0)
        lx, ly = -6.0 + 12.0 * tk.hash01(k * 1.3), -6.0 + 12.0 * h
        px, py = tk.rot2((lx, ly), math.radians(59))
        z = ztop(cx + px, cy + py) + 0.03
        s = 0.7
        quad = [(cx + px - 0.6 - s, cy + py - 1.0 - s), (cx + px - 0.6 + s, cy + py - 1.0 - s),
                (cx + px - 0.6 + s, cy + py - 1.0 + s), (cx + px - 0.6 - s, cy + py - 1.0 + s)]
        verts = [(x, y, ztop(x + 0.6, y + 1.0) + 0.03) for x, y in quad]
        tk.new_mesh(f"yud_win{k}_glow", verts, [(0, 1, 2, 3)], ["white_Glow"], recalc=False)
        del z

    tk.plinth("square", tk.ccw(FULL), h=0.25, out=2.5)
    tk.tree_row("trees", (12.0, -14.0), (36.0, 10.0), 0.25, 3, h=6.0, r=2.0, seed=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
