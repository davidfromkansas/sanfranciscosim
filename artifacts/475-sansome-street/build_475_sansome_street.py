"""Deterministic Blender build of the SF-SIM miniature 475 Sansome Street.

    blender -b --python build_475_sansome_street.py -- [--out DIR]

475 Sansome Street (1969 per the assessor, 20 storeys, ~483,000 sq ft): a broad
late-modernist office slab, long axis east-west, in the north Financial District.
No usable photo could be fetched (Wikimedia rate-limited), so the skin is
inferred from its period and type: close-set pale precast piers over bronze-tinted
glass, a recessed colonnaded lobby and a set-back mechanical penthouse. Massing
and heights are measured. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "475-sansome-street"
CENTER = (-122.4019396, 37.7945776)   # OSM way 32859284, OBB centre
H_TOP = 89.7                           # measured: DataSF LiDAR peak (penthouse)
H_ROOF = 82.3                          # measured: DataSF LiDAR median roof
H_LOBBY = 7.0
A = math.radians(9.0)                  # street grid: u = bearing 81 (E), v = bearing 351 (N)


def G(poly):
    return tk.xform(poly, A)


def build():
    plan = G([(-30.8, -16.6), (30.7, -16.8), (30.8, 13.7), (26.1, 13.7), (26.1, 16.7), (-27.3, 16.8),
              (-27.3, 14.4), (-30.7, 14.4)])
    # recessed glass lobby behind a colonnade
    tk.prism("lobby", tk.offset_poly(plan, -2.0), 0.0, H_LOBBY, "bronze")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -2.0), 0.6, H_LOBBY - 1.4, 0.06, "sand_Glow")
    tk.pier_grid("colonnade", tk.offset_poly(plan, -0.7), 0.0, H_LOBBY, 6.0, 0.9, 0.7, "concrete", skip_short=2.5)
    tk.prism("lobby_head", plan, H_LOBBY - 0.5, H_LOBBY + 0.5, "concrete", bev=0.1)
    # shaft: 19 office storeys of 3.94 m; pale piers every 3 m over bronze glass
    z0, n = H_LOBBY + 0.5, 19
    p = (H_ROOF - z0) / n
    tk.shaft("shaft", plan, z0, H_ROOF, p, glass="bronze", band="concrete", band_h=1.1, band_out=0.2,
             fins=(3.0, 0.7, 0.5, "concrete"), lit=0)
    tk.lit_windows("shaft_lit", tk.offset_poly(plan, 0.6), [(z0 + i * p + 1.1, z0 + (i + 1) * p) for i in range(n)],
                   6.0, 0.3, seed=8.0, out=0.0, margin=0.3, gap=0.6)
    # roof: cap, deck, set-back mechanical penthouse to the LiDAR peak
    tk.prism("cap", tk.offset_poly(plan, 0.5), H_ROOF, H_ROOF + 0.9, "concrete", bev=0.1)
    tk.prism("deck", tk.offset_poly(plan, -0.5), H_ROOF + 0.6, H_ROOF + 0.95, "roofd")
    ph = G(tk.rect(30.0, 14.0, -2.0, 0.0))
    tk.prism("penthouse", ph, H_ROOF + 0.95, H_TOP - 0.4, "concrete", bev=0.12)
    tk.panes("louvres", ph, [(H_ROOF + 2.2, H_TOP - 1.4)], 2.4, mat="steel", gap=0.5, margin=0.0)
    tk.prism("penthouse_roof", tk.offset_poly(ph, 0.2), H_TOP - 0.4, H_TOP, "roofd")
    tk.glow_ring("crown_light", tk.offset_poly(plan, 0.5), H_ROOF + 0.2, H_ROOF + 0.7, 0.06, "white_Glow")
    c = G([(21.0, 0.0)])[0]
    tk.hvac_cluster("plant", c[0], c[1], H_ROOF + 0.95, A, 12.0, 18.0, seed=5.0, hmax=3.0)
    tk.plinth("sidewalk", plan, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
