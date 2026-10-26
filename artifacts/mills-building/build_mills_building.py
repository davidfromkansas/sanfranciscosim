"""Deterministic Blender build of the SF-SIM miniature Mills Building.

    blender -b --python build_mills_building.py -- [--out DIR]

Mills Building, 220 Montgomery Street (Burnham & Root, 1892; restored by
Willis Polk after 1906): the ten-storey Chicago-school block on the Montgomery x
Bush corner. A two-storey white marble base with the great Romanesque entrance
arch on Montgomery, a buff-brick shaft whose middle storeys are an arcade of
tall engaged colonnettes ending in round arches, an ornamental frieze, an attic
storey and a heavy cornice. Two light courts open the roof. The 1931 Mills
Tower (artifacts/220-bush-street/) stands against the whole east wall, so
nothing here crosses that party line. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "mills-building"
CENTER = (-122.4018657, 37.7913738)   # OSM relation 3492808, OBB centre
H_TOP = 47.0                           # published 47 m (Wikipedia; infobox 46.94 m); LiDAR roof 43.7-44.8 m
H_BASE = 10.4                          # two marble storeys
H_BODY = 43.8                          # top of the attic storey = cornice line (LiDAR majority roof 43.65 m)
PITCH = (H_BODY - H_BASE) / 8          # storeys 3-10, 4.175 m

# OSM outer ring and the two light courts (inner rings), metres from CENTER (+x east, +y north)
OUTER = [(46.16, -17.07), (-38.62, -30.36), (-46.16, 17.06), (-23.76, 20.57), (-23.0, 15.75),
         (27.29, 23.63), (30.12, 24.07), (39.39, 25.49)]
COURTS = [[(3.16, 4.31), (29.39, 8.34), (31.74, -6.81), (5.51, -10.84)],
          [(-8.56, -13.18), (-25.6, -15.79), (-27.91, -0.91), (-10.86, 1.7)]]

# East party line shared with Mills Tower (OSM: the tower's west wall is this edge)
EA, EB = OUTER[0], OUTER[-1]
_dx, _dy = EB[0] - EA[0], EB[1] - EA[1]
_L = math.hypot(_dx, _dy)
EN = (_dy / _L, -_dx / _L)             # unit normal pointing east, into the tower
if EN[0] < 0:
    EN = (-EN[0], -EN[1])
GAP = 0.08                             # keep everything this far west of the party line


def clip_east(poly, gap=GAP):
    """Pull any vertex east of the party line back onto (line - gap)."""
    out = []
    for x, y in poly:
        s = (x - EA[0]) * EN[0] + (y - EA[1]) * EN[1]
        if s > -gap:
            x, y = x - (s + gap) * EN[0], y - (s + gap) * EN[1]
        out.append((x, y))
    return out


def face(ei, p0, p1, nrm):
    """Compass name of an edge's outward normal: S (Bush), W (Montgomery), N, E (party wall)."""
    brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
    return "NESW"[int(((brg + 45) % 360) // 90)]


def street(*a):
    return face(*a) in "SW"


def north(*a):
    return face(*a) == "N"


def ring(name, inner, outer, z0, z1, mat):
    """ring_band with explicit (clipped) loops of equal length."""
    n = len(inner)
    verts = []
    for loop, z in ((inner, z0), (outer, z0), (outer, z1), (inner, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return tk.new_mesh(name, verts, faces, [mat])


def band(name, plan, z0, z1, out, mat):
    return ring(name, plan, clip_east(tk.offset_poly(plan, out), 0.02), z0, z1, mat)


def build():
    plan = clip_east(tk.ccw(OUTER))
    # ---- marble base: storefronts, second-floor windows, Montgomery entrance arch
    tk.prism("base", plan, 0.0, H_BASE, "white", bev=0.1)
    base_bands = [(0.0, 5.2), (5.2, H_BASE)]
    tk.panes("base_win", plan, base_bands, 3.6, mat="glassd", margin=0.7, gap=1.2, edge_filter=street)
    tk.lit_windows("base_lit", plan, [(0.0, 5.2)], 3.6, 0.7, seed=2.0, out=0.1, margin=0.9, gap=1.4,
                   edge_filter=street)
    # entrance on Montgomery (W face, mid-length)
    w0, w1 = OUTER[2], OUTER[1]
    mx, my = (w0[0] + w1[0]) / 2, (w0[1] + w1[1]) / 2
    ux, uy = (w1[0] - w0[0]), (w1[1] - w0[1])
    ul = math.hypot(ux, uy)
    ux, uy = ux / ul, uy / ul
    nx, ny = uy, -ux                    # outward (west) normal
    if nx > 0:
        nx, ny = -nx, -ny
    yaw = math.atan2(ny, nx)
    tk.box("portal", mx + nx * 0.35, my + ny * 0.35, 0.0, H_BASE + 1.0, 0.7, 9.0, "cream", yaw=yaw, bev=0.1)
    fx, fy = mx + nx * 0.76, my + ny * 0.76
    def outward(ei, p0, p1, nrm):
        return nrm[0] * nx + nrm[1] * ny > 0.9

    tri = [(fx + ux * 3.5, fy + uy * 3.5), (fx - ux * 3.5, fy - uy * 3.5), (fx - nx * 3.0, fy - ny * 3.0)]
    tk.arched_panes("portal_arch", tri, 0.2, H_BASE - 0.4, 7.0, 5.6, mat="glassd", out=0.0,
                    edge_filter=outward, seg=6)
    tk.arched_panes("portal_lit", tri, 0.2, H_BASE - 2.2, 7.0, 3.8, mat="sand_Glow", out=0.06,
                    edge_filter=outward, suffix="_glow", seg=6)
    band("belt", plan, H_BASE, H_BASE + 0.8, 0.25, "cream")
    # ---- buff-brick shaft, storeys 3-10
    tk.prism("shaft", plan, H_BASE, H_BODY, "terracotta", bottom=False)
    st = tk.floors(H_BASE, H_BODY, PITCH)          # 8 storeys
    s3, mid, s8, s9, s10 = st[0], st[1:5], st[5], st[6], st[7]
    win_bands = [(s3[0] + 0.8, s3[1])] + mid + [(s9[0] + 0.75, s9[1]), s10]
    tk.panes("win", plan, win_bands, 3.6, mat="glassd", margin=0.75, gap=1.3, edge_filter=street)
    tk.panes("win_n", plan, mid + [s8, (s9[0] + 0.75, s9[1]), s10], 3.6, mat="glassd", margin=0.75,
             gap=1.3, edge_filter=north)
    tk.lit_windows("lit", plan, win_bands, 3.6, 0.3, seed=6.1, out=0.1, margin=0.95, gap=1.5,
                   edge_filter=street)
    tk.lit_windows("lit_n", plan, mid + [s9, s10], 3.6, 0.25, seed=3.7, out=0.1, margin=0.95, gap=1.5,
                   edge_filter=north)
    # the arcade: colonnettes on Bush and Montgomery rising to round arches in storey 8
    piers = []
    k = 0
    for p0, p1, L, nrm in tk.edges(plan):
        if not street(0, p0, p1, nrm) or L < 10:
            continue
        cnt = int(round(L / 3.6))
        step = L / cnt
        ex, ey = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        eyaw = math.atan2(ey, ex)
        for i in range(1, cnt):
            cx = p0[0] + ex * step * i + nrm[0] * 0.2
            cy = p0[1] + ey * step * i + nrm[1] * 0.2
            piers.append(tk.box(f"col_{k}", cx, cy, s3[1], s8[1] - 0.6, 0.6, 0.4, "stone", yaw=eyaw))
            k += 1
    tk.join(piers, "colonnettes")
    tk.arched_panes("arches", plan, s8[0] + 0.5, s8[1] - 0.5, 3.6, 2.6, mat="glassd", seg=5, edge_filter=street)
    tk.arched_panes("arches_lit", plan, s8[0] + 0.8, s8[1] - 1.3, 3.6, 1.6, mat="sand_Glow", out=0.1, seg=4,
                    edge_filter=lambda *a: street(*a) and tk.hash01(a[0] * 3.3) > 0.4, suffix="_glow")
    band("frieze", plan, s9[0], s9[0] + 0.75, 0.2, "cream")
    band("attic_band", plan, s10[0] - 0.3, s10[0] + 0.2, 0.15, "cream")
    # ---- cornice, parapet, roof with the two light courts
    band("cornice_fillet", plan, H_BODY, H_BODY + 0.6, 0.45, "cream")
    tk.prism("cornice_slab", clip_east(tk.offset_poly(plan, 1.0)), H_BODY + 0.6, H_BODY + 1.6, "cream", bev=0.1)
    inner = tk.offset_poly(plan, -0.5)
    ring("parapet", clip_east(inner, 0.6), clip_east(tk.offset_poly(plan, 0.2), 0.02), H_BODY + 1.6, H_TOP, "terracotta")
    tk.prism("roof", tk.offset_poly(plan, -0.3), H_BODY + 1.5, H_BODY + 1.75, "roofd")
    zr = H_BODY + 1.75
    for i, c in enumerate(COURTS):
        c = tk.ccw(c)
        tk.prism(f"court_{i}", tk.offset_poly(c, -0.1), zr - 0.2, zr + 0.06, "ink")
        tk.ring_band(f"court_coping_{i}", c, zr - 0.2, zr + 0.6, 0.45, "terracotta")
    tk.hvac_cluster("plant", -36.5, 8.0, zr, math.radians(9.0), 13.0, 7.0, seed=4.0, hmax=1.15, fans=False)
    tk.box("stair_house", 36.0, 13.0, zr, zr + 1.15, 4.0, 5.0, "terracotta", yaw=math.radians(-9.0), bev=0.1)
    # night: warm wash under the cornice on the two street faces
    for ei, (p0, p1, L, nrm) in enumerate(tk.edges(plan)):
        if street(ei, p0, p1, nrm) and L > 10:
            tk.flat_quad(f"cornice_wash_{ei}_glow", p0, p1, H_BODY - 0.8, H_BODY - 0.2, 0.3, "sand_Glow", nrm)
    # ---- sidewalk on Bush and Montgomery only (east = Mills Tower, north = neighbours)
    a, b, c = OUTER[0], OUTER[1], OUTER[2]

    def unit_normal(p, q, toward):
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy)
        n = (-dy / L, dx / L)
        return n if n[0] * toward[0] + n[1] * toward[1] > 0 else (-n[0], -n[1])

    nS = unit_normal(a, b, (0, -1))     # Bush edge, outward = south
    nW = unit_normal(b, c, (-1, 0))     # Montgomery edge, outward = west
    d = 3.0
    sw_out = [(a[0] + nS[0] * d, a[1] + nS[1] * d),
              (b[0] + (nS[0] + nW[0]) * d, b[1] + (nS[1] + nW[1]) * d),
              (c[0] + nW[0] * d, c[1] + nW[1] * d), c, b, a]
    tk.prism("sidewalk", clip_east(sw_out, 0.1), 0.0, 0.2, "stone")
    p0 = (c[0] + nW[0] * 1.8 + (b[0] - c[0]) * 0.12, c[1] + nW[1] * 1.8 + (b[1] - c[1]) * 0.12)
    p1 = (c[0] + nW[0] * 1.8 + (b[0] - c[0]) * 0.4, c[1] + nW[1] * 1.8 + (b[1] - c[1]) * 0.4)
    tk.tree_row("trees", p0, p1, 0.2, 2, h=5.5, r=1.8, seed=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
