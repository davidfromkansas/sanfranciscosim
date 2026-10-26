"""Deterministic Blender build of the SF-SIM miniature San Francisco Marriott Marquis.

    blender -b --python build_marriott_marquis.py -- [--out DIR]

780 Mission Street / 55 Fourth Street (Anthony J. Lumsden of DMJM with the
Zeidler Partnership, 1989): a 39-storey postmodern hotel tower that Herb Caen
called "the jukebox". A cross-shaped tower of light precast stone whose four
wings step down in ziggurat terraces, each terrace topped by a glass
greenhouse storey and marked by a fan-shaped glass window; dark glass slots
run up the re-entrant corners; the core ends in a glass crown under a huge
glass barrel vault whose fan-shaped ends face Market and Mission (the View
lounge). It stands on a six-storey podium that fills the block from 4th St
to Jessie Square. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "marriott-marquis"
CENTER = (-122.4045982, 37.7854182)   # OSM relation 6483285, OBB centre
H_TOP = 133.0                          # published 132.89 m / 133 m (Wikipedia); LiDAR peak 128.1 m (2010)
Z0 = 23.6                              # podium roof: LiDAR majority 23.6 m, OSM 6 levels
P = 3.1                                # hotel storey
YAW = tk.bearing_to_yaw(45.0)          # local +x (u) = bearing 45 (NE, along Mission St); +y (w) = NW
TU, TW = 4.0, -22.0                    # tower hub in local (u, w): centre of the OSM tower part's cross
CU, CW = 10.0, 11.0                    # core half-sizes (u, w)
N_CORE = 30                            # core storeys above the podium -> 116.6 m
VAULT_R = 8.4                          # crown vault radius: 124.6 + 8.4 = 133.0
Z_CROWN = Z0 + N_CORE * P + 8.0

# OSM outer ring and the podium light court (inner ring), metres from CENTER (+x east, +y north)
SITE = [(-32.59, 41.09), (-46.4, 55.35), (-52.08, 61.1), (-43.34, 69.67), (-36.53, 62.84), (-32.45, 66.84),
        (-26.82, 61.2), (-22.59, 65.34), (-16.96, 59.69), (-11.69, 64.88), (5.4, 47.73), (42.2, 10.8),
        (83.1, -30.24), (66.67, -46.38), (59.73, -53.2), (55.31, -57.55), (35.03, -77.48), (32.56, -75.0),
        (30.01, -77.51), (27.37, -74.86), (24.38, -77.8), (0.89, -54.15), (-4.26, -48.98), (-14.71, -38.48),
        (-22.73, -30.41), (-42.02, -10.97), (-43.87, -9.17), (-12.51, 21.58), (-4.96, 28.97),
        (-9.28, 33.32), (-24.71, 48.81)]   # OSM's 0.7 m jog at (-5.45, 29.46) dropped
COURT = [(67.54, -30.24), (58.78, -38.48), (38.37, -18.06), (46.93, -9.61)]

# wings: (direction (du, dw), half-width, [(outer extent from hub, storeys)...] inner to outer)
WINGS = {
    "sw": ((-1, 0), CW, [(14.4, 26), (18.8, 22), (23.2, 18), (27.6, 14), (32.0, 10)]),   # toward 4th St
    "ne": ((1, 0), CW, [(19.0, 28), (28.0, 24)]),                                          # toward Jessie Sq
    "nw": ((0, 1), CU, [(20.0, 27), (29.0, 23)]),                                          # toward Market
    "se": ((0, -1), CU, [(20.0, 26), (29.0, 21)]),                                         # toward Mission
}


def L2W(u, w):
    """Local tower (u, w) -> model (x east, y north)."""
    return tk.rot2((u + TU, w + TW), YAW)


def lrect(u0, u1, w0, w1):
    return [L2W(u0, w0), L2W(u1, w0), L2W(u1, w1), L2W(u0, w1)]


def zt(n):
    return Z0 + n * P


def face_quads(name, p0, p1, nrm, bands, spacing, mat, density=1.01, seed=0.0, out=0.06, margin=0.6,
               gap=1.2, suffix="_panes"):
    """Window quads on one facade p0->p1 with outward normal nrm (local helper)."""
    L = math.dist(p0, p1)
    if L < spacing * 0.8:
        return None
    cnt = max(1, int(round(L / spacing)))
    step = L / cnt
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    verts, faces = [], []
    for bi, (z0, z1) in enumerate(bands):
        za, zb = z0 + margin, z1 - margin
        if zb - za < 0.5:
            continue
        for i in range(cnt):
            if tk.hash01(seed + bi * 13.7 + i * 3.11) > density:
                continue
            a, b = i * step + gap / 2, (i + 1) * step - gap / 2
            pa = (p0[0] + ux * a + nrm[0] * out, p0[1] + uy * a + nrm[1] * out)
            pb = (p0[0] + ux * b + nrm[0] * out, p0[1] + uy * b + nrm[1] * out)
            k = len(verts)
            verts += [(pa[0], pa[1], za), (pb[0], pb[1], za), (pb[0], pb[1], zb), (pa[0], pa[1], zb)]
            faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return tk.new_mesh(name + suffix, verts, faces, [mat], recalc=False)


FACES = []   # (p0, p1, nrm, zlo, zhi) exposed stone tower faces, filled by build()


def wall(u0, w0, u1, w1, zlo, zhi):
    """Register an exposed tower face from local (u0,w0) to (u1,w1); the outward
    normal is to the right of the direction of travel (CCW plan)."""
    if zhi - zlo < P * 0.9:
        return
    p0, p1 = L2W(u0, w0), L2W(u1, w1)
    L = math.dist(p0, p1)
    nrm = ((p1[1] - p0[1]) / L, -(p1[0] - p0[0]) / L)
    FACES.append((p0, p1, nrm, zlo, zhi))


def fan(name, p0, p1, nrm, zb, zt_, wb, r, mat, out, seg=6):
    """Fan window: narrow foot widening to a semicircular head, centred on p0-p1."""
    cx, cy = (p0[0] + p1[0]) / 2 + nrm[0] * out, (p0[1] + p1[1]) / 2 + nrm[1] * out
    L = math.dist(p0, p1)
    ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
    zc = zt_ - r
    prof = [(-wb / 2, zb), (wb / 2, zb)]
    for k in range(seg + 1):
        a = math.pi * k / seg
        prof.append((r * math.cos(a), zc + r * math.sin(a)))
    verts = [(cx + ux * s, cy + uy * s, z) for s, z in prof]
    return tk.new_mesh(name, verts, [tuple(range(len(verts)))], [mat], recalc=False)


def build():
    FACES.clear()
    # ---------------- podium: six storeys over the whole OSM footprint
    site = tk.ccw(SITE)
    court = tk.ccw(COURT)
    tk.prism("podium", site, 0.0, Z0, "sand")
    tk.prism("podium_deck", tk.offset_poly(site, -0.8), Z0 - 0.2, Z0 + 0.15, "roofd")
    tk.prism("court_well", tk.offset_poly(court, -0.1), Z0 - 0.3, Z0 + 0.22, "ink")
    tk.ring_band("court_coping", court, Z0 - 0.3, Z0 + 0.8, 0.5, "sand")

    def street_edge(ei, p0, p1, nrm):
        # 4th St (SW), Mission (SE) and Jessie Square (NE) faces; skip short jogs
        if math.dist(p0, p1) < 8.0:
            return False
        brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
        return any(abs((brg - b + 180) % 360 - 180) < 20 for b in (225, 135, 45))

    pod = tk.floors(5.6, Z0 - 0.4, 3.6)
    tk.panes("podium_win", site, pod, 8.0, mat="glassd", margin=0.8, gap=3.0, edge_filter=street_edge)
    tk.panes("podium_lobby", site, [(0.0, 5.6)], 6.0, mat="glassl", margin=0.5, gap=1.0, edge_filter=street_edge)
    tk.lit_windows("podium_lobby_lit", site, [(0.0, 5.6)], 6.0, 0.75, seed=1.0, out=0.1, margin=0.8, gap=1.4,
                   edge_filter=street_edge)
    tk.lit_windows("podium_lit", site, pod, 8.0, 0.22, seed=2.0, out=0.1, margin=1.0, gap=3.4,
                   edge_filter=street_edge)

    # ---------------- tower core (hub), Z0 -> 116.6, then the glass crown and the jukebox vault
    zc = zt(N_CORE)
    core = lrect(-CU, CU, -CW, CW)
    tk.prism("core", core, Z0, zc, "stone", bottom=False)
    top_of = {}
    for key, ((du, dw), hw, steps) in WINGS.items():
        top_of[key] = zt(steps[0][1])
    # core faces above each wing (CCW: SE face w=-CW runs u -CU -> +CU, etc.)
    wall(-CU, -CW, CU, -CW, top_of["se"], zc)
    wall(CU, -CW, CU, CW, top_of["ne"], zc)
    wall(CU, CW, -CU, CW, top_of["nw"], zc)
    wall(-CU, CW, -CU, -CW, top_of["sw"], zc)
    tk.prism("crown_box", core, zc, Z_CROWN, "glassg", bottom=False)
    tk.ring_band("crown_sill", core, zc - 0.2, zc + 0.5, 0.35, "stone")
    tk.glow_ring("crown_lit", core, zc + 2.0, Z_CROWN - 1.5, 0.06, "white_Glow")
    # barrel vault along w (its arched fan ends face Market NW and Mission SE)
    seg = 10
    prof = [(VAULT_R * math.cos(math.pi * k / seg), Z_CROWN + VAULT_R * math.sin(math.pi * k / seg))
            for k in range(seg + 1)]
    verts = []
    for wv in (-CW - 0.4, CW + 0.4):
        for uu, z in prof:
            x, y = L2W(uu, wv)
            verts.append((x, y, z))
    n = len(prof)
    faces = [(i, i + 1, n + i + 1, n + i) for i in range(n - 1)]
    faces.append(tuple(range(n)))                      # SE end
    faces.append(tuple(range(2 * n - 1, n - 1, -1)))   # NW end
    faces.append((0, n, 2 * n - 1, n - 1))             # floor
    tk.new_mesh("vault", verts, faces, ["glassg"])
    for s, wv in ((-1, -CW - 0.4), (1, CW + 0.4)):
        pts = []
        for k in range(seg + 1):
            a = math.pi * k / seg
            x, y = L2W((VAULT_R - 1.0) * math.cos(a) * (-s), wv + s * 0.08)
            pts.append((x, y, Z_CROWN + 0.3 + (VAULT_R - 1.3) * math.sin(a)))
        tk.new_mesh(f"vault_fan_{'nw' if s > 0 else 'se'}_glow", pts, [tuple(range(len(pts)))], ["white_Glow"],
                    recalc=False)
    tk.prism("crown_cap", tk.offset_poly(core, -0.3), Z_CROWN - 0.1, Z_CROWN + 0.05, "roofd")

    # ---------------- stepped wings
    fans = []
    for key, ((du, dw), hw, steps) in WINGS.items():
        inner = CU if du else CW
        for i, (outer, nst) in enumerate(steps):
            ztop = zt(nst)
            zstone = ztop - P
            r0 = inner if i == 0 else steps[i - 1][0]
            if du:
                u0, u1 = sorted((du * r0, du * outer))
                poly = lrect(u0, u1, -hw, hw)
            else:
                w0, w1 = sorted((dw * r0, dw * outer))
                poly = lrect(-hw, hw, w0, w1)
            tk.prism(f"{key}_{i}", poly, Z0, zstone, "stone", bottom=False)
            tk.prism(f"{key}_{i}_glass", tk.offset_poly(poly, -0.4), zstone, ztop, "glassg", bottom=False)
            znext = zt(steps[i + 1][1]) if i + 1 < len(steps) else Z0
            # exposed faces: both sides full height, the outer end above the next step
            if du:
                ua, ub = (r0, outer) if du > 0 else (-outer, -r0)
                wall(ua, -hw, ub, -hw, Z0, zstone)       # SE-facing side
                wall(ub, hw, ua, hw, Z0, zstone)         # NW-facing side
                ue = du * outer
                if du > 0:
                    wall(ue, -hw, ue, hw, znext, zstone)
                    end = (L2W(ue, -hw), L2W(ue, hw))
                else:
                    wall(ue, hw, ue, -hw, znext, zstone)
                    end = (L2W(ue, hw), L2W(ue, -hw))
            else:
                wa, wb = (r0, outer) if dw > 0 else (-outer, -r0)
                wall(hw, wa, hw, wb, Z0, zstone)         # NE-facing side
                wall(-hw, wb, -hw, wa, Z0, zstone)       # SW-facing side
                we = dw * outer
                if dw > 0:
                    wall(hw, we, -hw, we, znext, zstone)
                    end = (L2W(hw, we), L2W(-hw, we))
                else:
                    wall(-hw, we, hw, we, znext, zstone)
                    end = (L2W(-hw, we), L2W(hw, we))
            # the fan window on the end face just under the glass storey
            p0, p1 = end
            L = math.dist(p0, p1)
            nrm = ((p1[1] - p0[1]) / L, -(p1[0] - p0[0]) / L)
            fh = min(zstone - znext - 0.6, 9.5)
            if fh > 4.0:
                fans.append(fan(f"{key}_{i}_fan_panes", p0, p1, nrm, zstone - 0.3 - fh, zstone - 0.3, 1.4, 3.4,
                                "glassg", 0.15))
                fans.append(fan(f"{key}_{i}_fan_glow", p0, p1, nrm, zstone - 0.3 - fh + 1.2, zstone - 1.0, 0.8,
                                2.5, "sky_Glow", 0.22))
    # dark glass slots up the four re-entrant corners
    for su in (-1, 1):
        for sw in (-1, 1):
            hu = top_of["ne" if su > 0 else "sw"]
            hv = top_of["nw" if sw > 0 else "se"]
            x, y = L2W(su * (CU + 1.1), sw * (CW + 1.1))
            tk.box(f"slot_{su}_{sw}", x, y, Z0, min(hu, hv) - P - 0.4, 2.2, 2.2, "glassd", yaw=YAW, bottom=False)

    # ---------------- punched windows + night skin on every exposed stone face
    for k, (p0, p1, nrm, zlo, zhi) in enumerate(FACES):
        k0 = max(0, int(math.ceil((zlo - Z0) / P - 1e-6)))
        k1 = int(math.floor((zhi - Z0) / P + 1e-6))
        bands = [(zt(j), zt(j + 1)) for j in range(k0, k1)]
        face_quads(f"tw_{k}", p0, p1, nrm, bands, 5.0, "glassd", margin=0.75, gap=2.2, out=0.06)
        face_quads(f"tw_{k}_lit", p0, p1, nrm, bands, 5.0, "sand_Glow", density=0.28, seed=k * 7.7,
                   margin=0.95, gap=2.6, out=0.1, suffix="_glow")

    # ---------------- podium roof plant, sidewalk, trees
    for i, (a, b) in enumerate(((27.0, -50.0),)):
        x, y = tk.rot2((a, -b), YAW)
        tk.hvac_cluster(f"plant_{i}", x, y, Z0 + 0.15, YAW, 12.0, 9.0, seed=3.0 + i, hmax=3.0)
    sw = [(-40.8, -24.5), (-37.7, -24.5), (-37.7, 72.3), (-30.0, 80.0), (37.4, 80.0), (37.4, 83.0), (-40.8, 83.0)]
    tk.prism("sidewalk", [tk.rot2((a, -b), YAW) for a, b in sw], 0.0, 0.2, "stone")
    p0, p1 = tk.rot2((-39.6, -10.0), YAW), tk.rot2((-39.6, 60.0), YAW)
    tk.tree_row("trees_4th", p0, p1, 0.2, 3, h=6.0, seed=2.2)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
