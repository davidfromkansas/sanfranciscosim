"""Deterministic Blender build of the SF-SIM miniature 211 Main Street.

    blender -b --python build_211_main_street.py -- [--out DIR]

211 Main Street, the Charles Schwab Building (1973, Corwin Booth & Associates,
17 storeys, ~417,000 sq ft), Rincon Hill edge of the Financial District: a
near-square 1970s office block. No usable photo could be fetched (Wikimedia
rate-limited), so the skin is inferred from the period and the architect's
contemporary 180 Montgomery: continuous ribbon windows of bronze glass between
deep sandy precast spandrels, broad corner piers, a recessed lobby and a set-back
mechanical penthouse. Massing and heights are measured. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "211-main-street"
CENTER = (-122.392854, 37.7905947)   # OSM way 154217696, OBB centre
H_TOP = 82.0                          # measured: DataSF LiDAR peak (penthouse)
H_ROOF = 73.3                         # measured: DataSF LiDAR median roof
H_LOBBY = 6.0
A = math.radians(45.0)                # SoMa grid: u = bearing 45 (NE), v = bearing 315 (NW)


def G(poly):
    return tk.xform(poly, A)


def build():
    plan = G([(-21.0, -24.7), (20.9, -25.0), (20.9, 24.7), (-20.9, 25.0)])
    tk.prism("lobby", tk.offset_poly(plan, -2.2), 0.0, H_LOBBY, "bronze")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -2.2), 0.6, H_LOBBY - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("lobby_piers", tk.offset_poly(plan, -0.8), 0.0, H_LOBBY, 8.3, 1.2, 0.8, "sand", skip_short=4.0)
    tk.prism("lobby_head", plan, H_LOBBY - 0.5, H_LOBBY + 0.5, "sand", bev=0.1)
    # 16 office storeys of 4.18 m: ribbon glass between deep spandrels, broad piers
    z0, n = H_LOBBY + 0.5, 16
    p = (H_ROOF - z0) / n
    tk.shaft("shaft", plan, z0, H_ROOF, p, glass="bronze", band="sand", band_h=1.9, band_out=0.4,
             fins=(8.3, 1.2, 0.4, "sand"), lit=0, glass_in=-0.5)
    tk.lit_windows("shaft_lit", tk.offset_poly(plan, 0.5), [(z0 + i * p + 1.9, z0 + (i + 1) * p) for i in range(n)],
                   4.15, 0.3, seed=9.0, out=0.0, margin=0.25, gap=0.5)
    tk.prism("cap", tk.offset_poly(plan, 0.4), H_ROOF, H_ROOF + 0.9, "sand", bev=0.1)
    tk.prism("deck", tk.offset_poly(plan, -0.4), H_ROOF + 0.6, H_ROOF + 0.95, "roofd")
    ph = G(tk.rect(20.0, 26.0, 0.0, 0.0))
    tk.prism("penthouse", ph, H_ROOF + 0.95, H_TOP - 0.4, "sand", bev=0.12)
    tk.panes("louvres", ph, [(H_ROOF + 2.2, H_TOP - 1.4)], 2.4, mat="steel", gap=0.5, margin=0.0)
    tk.prism("penthouse_roof", tk.offset_poly(ph, 0.2), H_TOP - 0.4, H_TOP, "roofd")
    tk.glow_ring("crown_light", tk.offset_poly(plan, 0.4), H_ROOF + 0.2, H_ROOF + 0.7, 0.06, "white_Glow")
    c = G([(15.0, 0.0)])[0]
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.95, A, 6.0, 30.0, seed=4.0, hmax=2.6)
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
