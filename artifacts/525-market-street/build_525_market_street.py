"""Deterministic Blender build of the SF-SIM miniature 525 Market Street.

    blender -b --python build_525_market_street.py -- [--out DIR]

525 Market Street (John Carl Warnecke & Associates, 1973; once First Market
Tower): a 39-storey cream box at First and Market, scored top to bottom by
hundreds of narrow dark window slits between cream piers, capped by a blank
cream band with no windows at all and solid corner piers. Recognition cues:
the pale pinstriped monolith and its blind top band. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "525-market-street"
CENTER = (-122.399158, 37.7905074)    # OSM way 32946570, OBB centre
H_TOP = 161.0                          # published roof (Wikipedia 161 m); LiDAR 161.76
H_LOBBY = 8.0
H_SLITS = 150.0                        # INFERRED: slits stop under a ~11 m blind top band (photo)
L, W = 57.4, 48.7                      # OSM OBB 57.7 x 48.7
YAW = tk.bearing_to_yaw(45.1)          # local +x = bearing 45.1 (parallel to Market St)


def slits(name, poly, z0, z1, spacing, width, end, mat, out=0.06, suffix="_panes"):
    """Full-height vertical window slits on every face, leaving solid corner piers `end` wide."""
    verts, faces = [], []
    for p0, p1, Ln, nrm in tk.edges(poly):
        usable = Ln - 2 * end
        cnt = max(1, int(round(usable / spacing)))
        step = usable / cnt
        ux, uy = (p1[0] - p0[0]) / Ln, (p1[1] - p0[1]) / Ln
        for i in range(cnt):
            c = end + (i + 0.5) * step
            a, b = c - width / 2, c + width / 2
            pa = (p0[0] + ux * a + nrm[0] * out, p0[1] + uy * a + nrm[1] * out)
            pb = (p0[0] + ux * b + nrm[0] * out, p0[1] + uy * b + nrm[1] * out)
            k = len(verts)
            verts += [(pa[0], pa[1], z0), (pb[0], pb[1], z0), (pb[0], pb[1], z1), (pa[0], pa[1], z1)]
            faces.append((k, k + 1, k + 2, k + 3))
    return tk.new_mesh(name + suffix, verts, faces, [mat], recalc=False)


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # dark recessed lobby behind cream columns
    tk.prism("lobby", tk.offset_poly(plan, -2.0), 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", tk.offset_poly(plan, -2.0), 0.8, H_LOBBY - 1.5, 0.06, "sand_Glow")
    tk.pier_grid("lobby_cols", tk.offset_poly(plan, -1.2), 0.0, H_LOBBY, 4.8, 1.2, 1.2, "sand")
    # the cream box: pinstripe slits, blind top band
    tk.prism("tower", plan, H_LOBBY, H_TOP - 1.2, "sand", bev=0.3)
    slits("tower", plan, H_LOBBY + 0.6, H_SLITS, 1.55, 0.55, 2.6, "glassd")
    # night: lit stretches of single slits, two storeys at a time
    bands = tk.floors(H_LOBBY + 0.6, H_SLITS, 3.535 * 2)
    tk.lit_windows("tower_win", plan, bands, 1.55, 0.22, seed=7.0, out=0.12, margin=0.4, gap=1.0)
    tk.ring_band("top_band_line", plan, H_SLITS + 0.4, H_SLITS + 0.9, 0.12, "stone")
    # roof: deck under a low parapet with the plant
    tk.prism("roof_deck", tk.offset_poly(plan, -0.6), H_TOP - 1.6, H_TOP - 1.1, "roofd")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.6), H_TOP - 1.2, H_TOP, 0.6, "sand")
    tk.hvac_cluster("plant", 0.0, 0.0, H_TOP - 1.1, YAW, L * 0.5, W * 0.45, seed=6.0, hmax=1.05, fans=False)
    tk.glow_ring("crown_light", plan, H_TOP - 4.0, H_TOP - 3.2, 0.3, "white_Glow")
    tk.plinth("plaza", plan, h=0.3, out=3.0)
    # street trees along Market (NW face, local +y)
    p0, p1 = tk.xform([(-L / 2 + 4, W / 2 + 2.2), (L / 2 - 4, W / 2 + 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 4, h=6.0, seed=2.2)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
