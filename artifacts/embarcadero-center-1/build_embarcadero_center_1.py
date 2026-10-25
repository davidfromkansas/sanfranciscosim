"""Deterministic Blender build of the SF-SIM miniature One Embarcadero Center.

    blender -b --python build_embarcadero_center_1.py -- [--out DIR]

One Embarcadero Center (John Portman, 1971), the tallest and westernmost of
the four Embarcadero Center slabs, between Sacramento, Battery, Clay and
Front streets. A 45-storey pale precast slab on the Financial District grid,
its narrow east and west ends broken into staggered vertical fins (the
"sawtooth" plan read straight off OSM), a fine even grid of dark punched
windows, a glazed band just under the flat roof, and a three-storey base.
Sister of artifacts/4-embarcadero-center/. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

# ---------------------------------------------- lean facade helpers (local)
# Flat outward quads (2 tris each) instead of extruded bands: the FiDi batch
# shares one vertex cap, so window graphics are skins over a solid prism.


def bays(name, poly, bands, spacing, frac, mat, out=0.06, density=1.01, seed=0.0, suffix="_panes",
         edge_min=2.0, efilter=None, end=0.0):
    """Per edge: cut into round(L/spacing) bays (one bay if spacing is None),
    put a quad `frac` of the bay wide in each, for every (z0, z1) band.
    `density` < 1 keeps a hashed subset (night lights)."""
    verts, faces = [], []
    for ei, (p0, p1, L, n) in enumerate(tk.edges(poly)):
        if L < edge_min or (efilter and not efilter(ei, p0, p1, n)):
            continue
        ux, uy = (p1[0] - p0[0]) / L, (p1[1] - p0[1]) / L
        e = min(end, L * 0.25)
        cnt = 1 if spacing is None else max(1, int(round((L - 2 * e) / spacing)))
        step = (L - 2 * e) / cnt
        w = step * frac
        for bi, (z0, z1) in enumerate(bands):
            for i in range(cnt):
                if density < 1.0 and tk.hash01(seed + ei * 71.3 + bi * 13.7 + i * 3.11) > density:
                    continue
                c = e + (i + 0.5) * step
                a, b = c - w / 2, c + w / 2
                pa = (p0[0] + ux * a + n[0] * out, p0[1] + uy * a + n[1] * out)
                pb = (p0[0] + ux * b + n[0] * out, p0[1] + uy * b + n[1] * out)
                k = len(verts)
                verts += [(pa[0], pa[1], z0), (pb[0], pb[1], z0), (pb[0], pb[1], z1), (pa[0], pa[1], z1)]
                faces.append((k, k + 1, k + 2, k + 3))
    if not faces:
        return None
    return tk.new_mesh(name + suffix, verts, faces, [mat], recalc=False)


def lit(name, poly, bands, spacing, frac, density, seed, mat="sand_Glow", out=0.12, **kw):
    """Night skin aligned with `bays` (same bay maths), a hashed subset lit."""
    return bays(name, poly, bands, spacing, frac, mat, out=out, density=density, seed=seed,
                suffix="_glow", **kw)


def storeys(z0, z1, n, margin=0.0):
    """n equal storey bands between z0 and z1 (no sliver), trimmed by margin."""
    h = (z1 - z0) / n
    return [(z0 + i * h + margin, z0 + (i + 1) * h - margin) for i in range(n)]

SLUG = "embarcadero-center-1"
CENTER = (-122.3996218, 37.7944839)  # OSM way 32612608, OBB centre
H_TOP = 173.4                         # published 569 ft roof (Wikipedia/CTBUH); LiDAR 167.9, OSM 173
BEARING = 81.2                        # long axis, deg true
YAW = math.radians(90.0 - BEARING)
H_POD = 12.0                          # podium / base band
N_FL = 45


def L(u, v):
    """Slab frame (u east along the long axis, v north across it) -> world."""
    return tk.rot2((u, v), YAW)


# OSM footprint in the slab frame: (v0, v1, u_west, u_east) per north-south strip.
STRIPS = [
    (-16.2, -10.7, -19.0, 17.9),
    (-10.7, -4.4, -31.2, 37.5),
    (-4.4, 0.5, -33.2, 35.1),
    (0.5, 5.3, -37.5, 29.3),
    (5.3, 11.2, -37.5, 26.7),
    (11.2, 16.4, -25.4, 16.2),
]


def footprint(shrink=0.0, strips=STRIPS):
    """The staircase plan as one CCW polygon in world coordinates."""
    east = []
    for v0, v1, uw, ue in strips:
        east += [(ue - shrink, v0), (ue - shrink, v1)]
    west = []
    for v0, v1, uw, ue in reversed(strips):
        west += [(uw + shrink, v1), (uw + shrink, v0)]
    pts = east + west
    clean = []
    for p in pts:
        if not clean or abs(p[0] - clean[-1][0]) > 1e-6 or abs(p[1] - clean[-1][1]) > 1e-6:
            clean.append(p)
    return tk.ccw([L(u, v) for u, v in clean])


def build():
    plan = footprint()
    # base: the three-storey podium level of the Center, kept to the tower's own
    # footprint (the shared podium and bridges are separate OSM buildings)
    pod = tk.offset_poly(plan, 0.8)
    tk.prism("podium", pod, 0.0, H_POD, "stone", bev=0.2)
    bays("podium_glass", pod, [(1.0, 4.6), (6.6, 10.2)], 5.0, 0.8, "glassd", end=1.5)
    lit("podium", pod, [(1.2, 4.4), (6.8, 10.0)], 5.0, 0.8, 0.7, 4.0, end=1.5)
    tk.prism("podium_roof", tk.offset_poly(pod, -0.5), H_POD - 0.3, H_POD + 0.05, "steel")
    tk.ring_band("podium_parapet", tk.offset_poly(pod, -0.6), H_POD, H_POD + 1.0, 0.6, "cream")
    # slab: pale precast body, a fine grid of dark punched windows: full-height
    # window columns under one precast spandrel quad per storey
    z_top = H_TOP - 1.2
    tk.prism("slab", plan, H_POD, z_top, "sand", bev=0.2)
    fl = storeys(H_POD, z_top - 1.0, N_FL - 3)
    bays("cols", plan, [(H_POD + 0.6, z_top - 1.4)], 2.6, 0.62, "bronze", out=0.05, end=0.4)
    bays("spandrels", plan, [(a, a + 1.25) for a, _ in fl[1:]], None, 1.0, "sand", out=0.08, edge_min=1.5)
    # the glazed mechanical band just under the roof (photo)
    bays("band", plan, [(z_top - 13.0, z_top - 10.6)], None, 1.0, "glassl", out=0.11, edge_min=1.5)
    groups = storeys(H_POD + 1.0, z_top - 14.0, 14)
    lit("slab", plan, [(z0 + 0.6, z1 - 0.6) for z0, z1 in groups], 2.6, 0.5, 0.26, 11.0, end=0.4, out=0.14)
    # crown: cream parapet, roof deck, a north curb of cooling towers, crown light
    tk.ring_band("parapet", tk.offset_poly(plan, -0.5), H_TOP - 1.2, H_TOP, 0.5, "cream")
    tk.prism("deck", tk.offset_poly(plan, -0.4), H_TOP - 1.6, H_TOP - 1.0, "steel")
    for k, u in enumerate((-12.0, -4.0, 4.0, 12.0)):
        x, y = L(u, 7.0)
        tk.cylinder(f"ct_{k}", x, y, H_TOP - 1.0, H_TOP - 0.2, 3.0, "steel", seg=10)
        tk.cylinder(f"ctg_{k}", x, y, H_TOP - 0.2, H_TOP - 0.05, 2.2, "ink", seg=10)
    pc = L(0.0, -6.0)
    tk.box("penthouse", pc[0], pc[1], H_TOP - 1.0, H_TOP - 0.1, 18.0, 6.0, "cream", yaw=YAW, bev=0.15)
    tk.glow_ring("crown", plan, H_TOP - 3.6, H_TOP - 1.6, 0.14, "glassl_Glow")
    tk.plinth("apron", pod, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
