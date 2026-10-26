"""Deterministic Blender build of the SF-SIM miniature 180 Montgomery Street.

    blender -b --python build_180_montgomery_street.py -- [--out DIR]

Batch slug `180-montgomery-street`, but the footprint (OSM way 132125163, no address
tags) is 180 Montgomery Street, the Bank of the West Building (1979, 25 storeys,
109.8 m): DataSF assessor parcel 0289009 and the Wikipedia/CTBUH coordinates both
land on it. A plain beige precast-concrete box: deep horizontal ribbon windows
between thick spandrels, a few broad piers per face, solid corners. Recognition
cue: the strongly horizontal sandy grid at Montgomery x Bush. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "180-montgomery-street"
CENTER = (-122.4020118, 37.7907517)   # OSM way 132125163, OBB centre
H_TOP = 109.8                          # published (CTBUH 109.8 m; LiDAR majority 109.5)
H_ROOF = 104.2                         # measured: DataSF LiDAR median roof
H_LOBBY = 6.0
A = math.radians(9.0)                  # street grid: u = bearing 81 (E), v = bearing 351 (N)


def G(poly):
    return tk.xform(poly, A)


def build():
    # OSM footprint in the grid frame; Montgomery St on -u (W), Bush St on +v (N)
    plan = G([(-20.5, -18.8), (20.6, -18.8), (20.6, 13.8), (13.2, 13.8), (13.2, 18.9), (-20.5, 18.9)])
    # recessed glass lobby behind the piers
    tk.prism("lobby", tk.offset_poly(plan, -1.4), 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -1.4), 0.6, H_LOBBY - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("lobby_piers", tk.offset_poly(plan, -0.6), 0.0, H_LOBBY, 7.6, 1.1, 0.6, "concrete", skip_short=4.0)
    tk.prism("lobby_head", plan, H_LOBBY - 0.6, H_LOBBY + 0.4, "concrete", bev=0.1, bottom=True)
    # shaft: 24 storeys of 4.12 m; thick sandy spandrels, dark ribbon glass set deep
    z0 = H_LOBBY + 0.4
    n = 24
    p = (H_ROOF - z0) / n
    tk.shaft("shaft", plan, z0, H_ROOF, p, glass="glassd", band="concrete", band_h=2.1, band_out=0.45,
             fins=(7.6, 1.1, 0.45, "concrete"), lit=0, glass_in=-0.5)
    tk.lit_windows("shaft_lit", tk.offset_poly(plan, 0.55), [(z0 + i * p + 2.1, z0 + (i + 1) * p) for i in range(n)],
                   3.8, 0.3, seed=7.0, out=0.0, margin=0.25, gap=0.5)
    # roof: parapet cap, deck, set-back plant penthouse to the published crest
    tk.prism("cap", tk.offset_poly(plan, 0.45), H_ROOF, H_ROOF + 0.8, "concrete", bev=0.1)
    tk.prism("deck", tk.offset_poly(plan, -0.4), H_ROOF + 0.6, H_ROOF + 0.85, "roofd")
    ph = G(tk.rect(22.0, 16.0, -3.0, -1.0))
    tk.prism("penthouse", ph, H_ROOF + 0.85, H_TOP - 0.5, "concrete", bev=0.12)
    tk.panes("penthouse_louvres", ph, [(H_ROOF + 2.0, H_TOP - 1.5)], 2.6, mat="steel", gap=0.6, margin=0.0)
    tk.prism("penthouse_roof", tk.offset_poly(ph, 0.2), H_TOP - 0.5, H_TOP, "roofd")
    tk.glow_ring("crown_light", tk.offset_poly(plan, 0.45), H_ROOF + 0.15, H_ROOF + 0.65, 0.06, "white_Glow")
    c = G([(-3.0, 11.0)])[0]
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.85, A, 14.0, 5.0, seed=2.0, hmax=2.6)
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
