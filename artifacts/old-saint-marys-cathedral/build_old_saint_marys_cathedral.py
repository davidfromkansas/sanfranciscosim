"""Deterministic Blender build of the SF-SIM miniature Old Saint Mary's Cathedral.

    blender -b --python build_old_saint_marys_cathedral.py -- [--out DIR]

660 California Street at Grant Avenue (Craine & England, 1853-54; rebuilt
inside its brick shell by Welsh & Carey, 1908-09): California's first
cathedral, red brick Gothic Revival. A square brick tower centred on the
California Street front - stepped corner buttresses, a clock on the south and
west faces over the "Son, observe the time and fly from evil" plaque, paired
louvred lancet belfry openings, corner pinnacles and a central cross - in front
of a gabled nave whose long Grant Avenue side is buttressed and crenellated.
Lower parish buildings fill the rest of the OSM outline. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "old-saint-marys-cathedral"
CENTER = (-122.4057155, 37.7928515)  # OSM way 260520154, OBB centre
H_TOP = 33.65                         # DataSF 2010 LiDAR max of ring 201006.0002205 (tower cross)
YAW = tk.bearing_to_yaw(81.0)         # local +x = east along California, +y = north (up Grant)
# OSM outline in local street-grid metres (+y north; California St front at y = -19.4)
OUTLINE = [(7.0, -19.4), (-3.9, -19.4), (-3.9, -23.1), (-10.8, -23.1), (-10.8, -19.4), (-20.6, -19.4),
           (-20.6, -15.4), (-17.8, -15.4), (-17.8, 8.4), (-21.1, 8.4), (-21.1, 21.1), (-17.8, 21.1),
           (-17.8, 23.1), (13.5, 23.1), (13.5, 16.2), (21.1, 16.2), (21.1, -0.9), (12.9, -0.9),
           (12.9, 9.1), (3.3, 9.1), (3.3, -15.0), (7.0, -15.0)]
NX0, NX1, NY0, NY1 = -17.8, 3.3, -19.4, 23.1   # nave block
TX0, TX1, TY0, TY1 = -10.8, -3.9, -23.1, -16.2  # tower (front face projects 3.7 m)
EAVE, RIDGE, TWR = 13.0, 20.5, 26.5


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def facing(dx, dy):
    """Edge filter: keep faces whose local outward normal is (dx, dy)."""
    def f(ei, p0, p1, n):
        m = tk.rot2(n, -YAW)
        return m[0] * dx + m[1] * dy > 0.9
    return f


def oriented(verts, nrm):
    """Index order of a planar loop so its normal points along world nrm (x, y)."""
    a, b, c = verts[0], verts[1], verts[2]
    u = (b[0] - a[0], b[1] - a[1], b[2] - a[2])
    v = (c[0] - a[0], c[1] - a[1], c[2] - a[2])
    nx, ny = u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2]
    idx = list(range(len(verts)))
    return tuple(idx if nx * nrm[0] + ny * nrm[1] > 0 else reversed(idx))


def slab(name, loop, nrm, depth, mat):
    """Close a vertical planar loop into a thin solid pushed `depth` along -nrm (behind it)."""
    n = len(loop)
    back = [(x - nrm[0] * depth, y - nrm[1] * depth, z) for x, y, z in loop]
    verts = loop + back
    faces = [tuple(range(n)), tuple(range(2 * n - 1, n - 1, -1))]
    faces += [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return tk.new_mesh(name, verts, faces, [mat], recalc=True)


def build():
    # parish buildings (rectory/hall to the east, side chapel and porch to the west), outside the nave
    east = [(3.3, 9.1), (12.9, 9.1), (12.9, -0.9), (21.1, -0.9), (21.1, 16.2), (13.5, 16.2), (13.5, 23.1),
            (3.3, 23.1)]
    tk.punched_block("hall", L(east), 0.0, 11.0, 3.6, wall="brick", win="glassd", spacing=3.0, gap=1.4,
                     margin=0.8, lit=0.3, seed=2.0, bev=0.1, edge_filter=lambda ei, p0, p1, n: not facing(-1, 0)(ei, p0, p1, n))
    tk.prism("hall_roof", tk.offset_poly(L(east), -0.4), 10.8, 11.25, "roofd")
    tk.prism("porch_e", L([(3.3, -19.4), (7.0, -19.4), (7.0, -15.0), (3.3, -15.0)]), 0.0, 6.0, "brick", bev=0.1)
    tk.prism("porch_w", L([(-20.6, -19.4), (-17.8, -19.4), (-17.8, -15.4), (-20.6, -15.4)]), 0.0, 5.0, "brick")
    chapel = L([(-21.1, 8.4), (-17.8, 8.4), (-17.8, 21.1), (-21.1, 21.1)])
    tk.prism("chapel", chapel, 0.0, 8.0, "brick", bev=0.1)
    tk.arched_panes("chapel_win", chapel, 2.5, 6.8, 4.2, 1.6, mat="glassd", edge_filter=facing(-1, 0))
    # nave: brick walls, buttresses, crenellated parapet, gabled slate roof
    nave = L(tk.rect(NX1 - NX0, NY1 - NY0, (NX0 + NX1) / 2, (NY0 + NY1) / 2))
    tk.prism("nave", nave, 0.0, EAVE, "brick", bev=0.1)
    tk.pier_grid("buttress", nave, 0.0, EAVE + 1.4, 5.3, 1.0, 0.9, "brick", skip_short=8.0)
    nave_free = L(tk.rect(NX1 - NX0, 8.0 - NY0, (NX0 + NX1) / 2, (NY0 + 8.0) / 2))
    tk.arched_panes("lancets", nave_free, 4.5, 11.0, 5.3, 1.9, mat="glassd", out=0.06,
                    edge_filter=lambda ei, p0, p1, n: abs(tk.rot2(n, -YAW)[0]) > 0.9)
    tk.arched_panes("lancets_lit", nave_free, 5.0, 10.4, 5.3, 1.3, mat="mustard_Glow", out=0.1, suffix="_glow",
                    edge_filter=lambda ei, p0, p1, n: abs(tk.rot2(n, -YAW)[0]) > 0.9)
    tk.ring_band("parapet", nave, EAVE, EAVE + 0.9, 0.2, "brick")
    for i in range(8):  # merlons along the Grant Avenue (west) parapet
        y = NY0 + 3.0 + i * (NY1 - NY0 - 6.0) / 7
        tk.box(f"merlon{i}", *P(NX0 - 0.05, y), EAVE + 0.9, EAVE + 1.7, 0.5, 1.2, "brick", yaw=YAW)
    xm = (NX0 + NX1) / 2
    hw = (NX1 - NX0) / 2 - 0.3
    verts, faces = [], []
    for y in (NY0 + 0.3, NY1 - 0.3):
        for x, z in ((xm - hw, EAVE + 0.2), (xm + hw, EAVE + 0.2), (xm, RIDGE)):
            px, py = P(x, y)
            verts.append((px, py, z))
    faces = [(0, 1, 2), (5, 4, 3), (0, 3, 4, 1), (1, 4, 5, 2), (2, 5, 3, 0)]
    tk.new_mesh("roof", verts, faces, ["roofd"])
    # front gable wall + west-front door and paired windows (left of the tower)
    gable = []
    for x, z in ((NX0, EAVE), (NX1, EAVE), (xm, RIDGE + 0.6)):
        px, py = P(x, NY0 - 0.01)
        gable.append((px, py, z))
    slab("gable", gable, P(0, -1), 0.5, "brick")
    tk.arched_panes("west_door", L(tk.rect(6.0, 0.5, -15.0, NY0 + 0.25)), 0.3, 5.0, 6.0, 2.6, mat="ink",
                    out=0.06, edge_filter=facing(0, -1))
    tk.arched_panes("front_win", L(tk.rect(5.0, 0.5, -15.0, NY0 + 0.25)), 6.6, 10.6, 2.5, 1.4, mat="glassd",
                    out=0.06, edge_filter=facing(0, -1))
    # tower: shaft, corner buttresses, belfry, clocks, parapet, pinnacles, cross
    tw = L(tk.rect(TX1 - TX0, TY1 - TY0, (TX0 + TX1) / 2, (TY0 + TY1) / 2))
    tcx, tcy = (TX0 + TX1) / 2, (TY0 + TY1) / 2
    tk.prism("tower", tw, 0.0, TWR, "brick", bev=0.1)
    tk.pier_grid("tower_butt", tw, 0.0, TWR - 0.6, 6.0, 1.1, 0.6, "brick", skip_short=4.0, min_count=2)
    tk.spandrels("tower_bands", tw, [14.6, 18.6], 0.4, 0.25, "stone")
    tk.arched_panes("belfry", tw, 19.4, 25.2, 2.4, 1.5, mat="ink", out=0.62)
    tk.arched_panes("door", tw, 0.4, 5.0, 6.9, 2.6, mat="stone", out=0.62, edge_filter=facing(0, -1))
    tk.arched_panes("door_lit", tw, 0.5, 4.4, 6.9, 1.9, mat="mustard_Glow", out=0.66, suffix="_glow",
                    edge_filter=facing(0, -1))
    for nm, (dx, dy) in (("s", (0, -1)), ("w", (-1, 0))):
        ox = dx * ((TX1 - TX0) / 2 + 0.62)
        oy = dy * ((TY1 - TY0) / 2 + 0.62)
        c = P(tcx + ox, tcy + oy)
        r = 1.5
        ring = []
        for k in range(10):
            a = 2 * math.pi * k / 10
            lx = tcx + ox + (0.0 if dx else r * math.cos(a)) + dx * 0.05
            ly = tcy + oy + (r * math.cos(a) if dx else 0.0) + dy * 0.05
            px, py = P(lx, ly)
            ring.append((px, py, 16.3 + r * math.sin(a)))
        nrm = P(dx, dy)
        slab(f"clock_{nm}", ring, nrm, 0.3, "cream")
        glow = [(x + nrm[0] * 0.06, y + nrm[1] * 0.06, z) for x, y, z in ring]
        tk.new_mesh(f"clock_{nm}_glow", glow, [oriented(glow, nrm)], ["cream_Glow"], recalc=False)
        tk.box(f"plaque_{nm}", c[0] + nrm[0] * 0.05, c[1] + nrm[1] * 0.05, 13.6, 14.3,
               (0.1 if dx else 2.6), (2.6 if dx else 0.1), "ink", yaw=YAW)
    tk.ring_band("tower_parapet", tw, TWR - 0.6, TWR, 0.75, "stone")
    for i, (sx, sy) in enumerate(((-1, -1), (1, -1), (1, 1), (-1, 1))):
        px, py = P(tcx + sx * 3.6, tcy + sy * 3.6)
        tk.cylinder(f"pin{i}", px, py, TWR, TWR + 1.6, 0.55, "brick", seg=6)
        tk.cylinder(f"pin{i}_cap", px, py, TWR + 1.6, TWR + 3.4, 0.6, "stone", seg=6, r1=0.05)
    tk.pyramid("tower_gablet", L(tk.rect(3.0, 1.0, tcx, TY0 + 0.3)), TWR, TWR + 2.6, "brick")
    tk.box("cross_v", *P(tcx, TY0 + 0.3), TWR + 2.4, H_TOP, 0.35, 0.35, "ink", yaw=YAW)
    tk.box("cross_h", *P(tcx, TY0 + 0.3), H_TOP - 2.0, H_TOP - 1.6, 1.8, 0.35, "ink", yaw=YAW)
    tk.prism("sidewalk", L(tk.rect(46.0, 50.0, 0.0, -1.0)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
