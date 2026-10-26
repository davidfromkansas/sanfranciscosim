"""Deterministic Blender build of the SF-SIM miniature 350 Bush Street.

    blender -b --python build_350_bush_street.py -- [--out DIR]

350 Bush Street (Heller Manus, 2018, 19 storeys): a through-block glass office
tower, Bush to Pine, wrapped around the 1923 San Francisco Mining / Curb Exchange
(Miller & Pflueger), whose temple front - eight fluted columns in pairs under a
sculpted pediment - is kept as the Bush Street entrance. Recognition cues: the
white classical temple at the foot of a dark green-glass tower. The Exchange
portico is its own OSM way (151185875, height 16); it is included here because
it is the building's face. Tower footprint: OSM way 151185876. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "350-bush-street"
CENTER = (-122.4032981, 37.7913478)   # OSM way 151185876, OBB centre
H_TOP = 85.0                           # ESTIMATED: 19 storeys (no published height, no LiDAR - built 2018)
H_ROOF = 81.0
A = math.radians(9.0)                  # street grid: u = bearing 81 (E), v = bearing 351 (N)
U0, U1 = -21.2, -2.4                   # Exchange frontage on Bush St (grid u)
VF, VB = -41.2, -32.5                  # portico front (street line) and back


def G(poly):
    return tk.xform(poly, A)


def gbox(name, u0, u1, v0, v1, z0, z1, mat, bev=0.0):
    return tk.prism(name, G([(u0, v0), (u1, v0), (u1, v1), (u0, v1)]), z0, z1, mat, bev=bev)


def gable(name, u0, u1, v0, v1, z0, z1, mat):
    """Pediment: a triangular prism spanning u0..u1, running v0..v1, apex at z1."""
    um = (u0 + u1) / 2
    pts = [(u0, v0, z0), (u1, v0, z0), (um, v0, z1), (u0, v1, z0), (u1, v1, z0), (um, v1, z1)]
    verts = [(*G([(u, v)])[0], z) for u, v, z in pts]
    faces = [(0, 2, 1), (3, 4, 5), (0, 1, 4, 3), (1, 2, 5, 4), (2, 0, 3, 5)]
    return tk.new_mesh(name, verts, faces, [mat])


def build():
    # ---- tower: the OSM footprint minus the Exchange hall (SW corner)
    plan = G([(-22.0, -20.0), (-2.4, -20.0), (-2.4, -28.1), (1.2, -28.1), (1.2, -41.2), (22.0, -41.2),
              (22.0, -0.4), (14.5, -0.4), (14.4, 41.2), (-22.4, 41.3)])
    n = 19
    p = H_ROOF / n
    tk.shaft("shaft", plan, 0.0, H_ROOF, p, glass="glassd", band="steel", band_h=0.5, band_out=0.12,
             fins=(4.2, 0.3, 0.35, "steel"), lit=0)
    tk.lit_windows("shaft_lit", tk.offset_poly(plan, 0.45), [(i * p + 0.5, (i + 1) * p) for i in range(4, n)],
                   4.2, 0.3, seed=5.0, out=0.0, margin=0.3, gap=0.4)
    # sandstone-clad low wing beside the Exchange on Bush St (photo), with punched windows
    south = lambda ei, p0, p1, nm: -nm[0] * math.sin(A) + nm[1] * math.cos(A) < -0.7  # noqa: E731
    wing = G([(1.2, VF - 0.6), (22.0, VF - 0.6), (22.0, VF + 0.2), (1.2, VF + 0.2)])
    tk.prism("wing", wing, 0.0, 14.0, "stone", bev=0.1)
    tk.panes("wing_win", wing, [(0.4, 4.6), (5.6, 9.4), (10.2, 13.4)], 4.2, mat="glassd", gap=1.4, margin=0.3,
             edge_filter=south)
    tk.lit_windows("wing_lit", wing, [(0.4, 4.6)], 4.2, 0.9, seed=2.0, out=0.1, margin=0.5, gap=1.6, edge_filter=south)
    # crown: a glass screen around the plant deck
    tk.ring_band("crown_screen", tk.offset_poly(plan, -0.3), H_ROOF, H_TOP, 0.3, "glassl")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.4), H_ROOF - 0.3, H_ROOF + 0.05, "roofd")
    c = G([(0.0, 10.0)])[0]
    tk.hvac_cluster("roof_plant", c[0], c[1], H_ROOF + 0.05, A, 24.0, 30.0, seed=6.0, hmax=3.4)
    tk.glow_ring("crown_light", plan, H_TOP - 1.6, H_TOP - 0.6, 0.08, "white_Glow")
    # ---- the 1923 Mining / Curb Exchange: hall, portico, paired fluted columns, pediment
    gbox("hall", U0, U1, VB, -20.0, 0.0, 16.0, "stone", bev=0.12)
    gbox("hall_roof", U0 + 0.8, U1 - 0.8, VB + 0.8, -20.8, 16.0, 16.4, "roofd")
    gbox("stylobate", U0, U1, VF, VB, 0.0, 1.0, "stone")
    gbox("cella", U0 + 1.3, U1 - 1.3, VF + 2.8, VB, 1.0, 13.6, "stone")
    gbox("anta_w", U0, U0 + 1.3, VF, VB, 1.0, 13.6, "stone")
    gbox("anta_e", U1 - 1.3, U1, VF, VB, 1.0, 13.6, "stone")
    gbox("entablature", U0 - 0.3, U1 + 0.3, VF - 0.3, VB, 13.6, 16.0, "white", bev=0.1)
    gable("pediment", U0 - 0.3, U1 + 0.3, VF - 0.3, VB, 16.0, 20.2, "white")
    for k, uc in enumerate((-18.0, -13.8, -9.6, -5.4)):
        for j, du in enumerate((-0.85, 0.85)):
            x, y = G([(uc + du, VF + 1.0)])[0]
            tk.cylinder(f"column_{k}_{j}", x, y, 1.0, 13.6, 0.62, "white", seg=8)
    # tall dark windows in the cella wall between the column pairs; lit at night
    for k, uc in enumerate((-15.9, -11.7, -7.5)):
        a, b = G([(uc - 1.1, VF + 2.8), (uc + 1.1, VF + 2.8)])
        nrm = tk.rot2((0.0, -1.0), A)
        tk.flat_quad(f"cella_win_{k}", a, b, 1.6, 12.0, 0.04, "glassd", nrm)
        tk.flat_quad(f"cella_lit_{k}_glow", a, b, 1.6, 9.0, 0.1, "sand_Glow", nrm)
    tk.plinth("sidewalk", G([(-22.4, -41.2), (22.0, -41.2), (22.0, 41.2), (-22.4, 41.3)]), h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
