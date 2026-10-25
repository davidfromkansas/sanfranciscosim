"""Deterministic Blender build of the SF-SIM miniature 535 Mission Street.

    blender -b --python build_535_mission_street.py -- [--out DIR]

535 Mission Street (HOK, 2014): a 27-storey, 115 m office tower clad in a
four-sided structural-silicone blue glass skin. Its one flourish is a folded
corner: a tall triangular facet that is a sliver at the base and opens to a
full chamfer at the roof, so each face reads as a single blue pane twisting
past the next. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "535-mission-street"
CENTER = (-122.398156, 37.7888799)   # OSM way 127460048, OBB centre
H_TOP = 115.0                         # published 378 ft roof (Wikipedia / Emporis)
H_LOBBY = 8.0
H_ROOF = 112.6                        # glass parapet screen runs up to H_TOP
L, W = 45.0, 28.4                    # OSM OBB 45.4 x 28.7; local +x = bearing 135.5 (away from Mission)
YAW = tk.bearing_to_yaw(135.5)
C0, C1 = 0.8, 10.0                   # folded-corner chamfer at the base and at the roof
N_STOREYS = 26                       # whole storeys between the lobby and the parapet


def chamfer_at(z):
    t = max(0.0, min(1.0, (z - H_LOBBY) / (H_TOP - H_LOBBY)))
    return C0 + (C1 - C0) * t


def plan_local(c):
    # local (-x, +y) corner = the north corner, Mission St x the 1st St side (inferred face)
    hx, hy = L / 2, W / 2
    return [(-hx, -hy), (hx, -hy), (hx, hy), (-hx + c, hy), (-hx, hy - c)]


def outline(z, off):
    return tk.offset_poly(tk.xform(plan_local(chamfer_at(z)), YAW), off)


def build():
    base = outline(0.0, 0.0)
    # lobby: recessed clear glass under the skin, steel mullions, warm lit band
    tk.prism("lobby_glass", tk.offset_poly(base, -1.0), 0.0, H_LOBBY, "glassl")
    tk.glow_ring("lobby_lit", tk.offset_poly(base, -1.0), 0.6, H_LOBBY - 1.4, 0.06, "sand_Glow")
    tk.pier_grid("lobby_mullions", tk.offset_poly(base, -0.5), 0.0, H_LOBBY, 3.0, 0.22, 0.5, "steel")
    tk.prism("canopy", tk.offset_poly(base, 0.6), H_LOBBY - 0.6, H_LOBBY, "steel")
    # the blue glass shaft: thin flush bands, the folded corner growing with height
    pitch = (H_ROOF - H_LOBBY) / N_STOREYS
    tk.banded_loft("shaft", outline, H_LOBBY, H_ROOF, pitch * 2, 0.35, 0.12,
                   tk.material("glassl"), tk.material("glass"), glass_in=0.0)
    # the facet itself reads darker (photo): a dark-glass skin on the chamfer face
    zs = [H_LOBBY, H_ROOF]
    pts = []
    for z in zs:
        loop = tk.xform(plan_local(chamfer_at(z)), YAW)
        a, b = loop[3], loop[4]
        nx, ny = b[1] - a[1], -(b[0] - a[0])
        ln = math.hypot(nx, ny)
        nx, ny = nx / ln * 0.18, ny / ln * 0.18
        pts.append(((a[0] + nx, a[1] + ny, z), (b[0] + nx, b[1] + ny, z)))
    (a0, b0), (a1, b1) = pts
    tk.new_mesh("facet", [a0, b0, b1, a1], [(0, 1, 2, 3)], ["glass"], recalc=False)
    bands = [(z0, z1) for z0, z1 in tk.floors(H_LOBBY, H_ROOF, pitch)]
    tk.lit_loop_windows("shaft_win", outline, bands, 0.28, seed=5.35, out=0.24, margin=0.7, subdiv=6, gap=0.12)
    # parapet: the glass skin continues as a screen around a dark deck and tidy plant
    top = outline(H_ROOF, 0.0)
    tk.ring_band("parapet", tk.offset_poly(top, -0.35), H_ROOF, H_TOP, 0.35, "glass")
    tk.prism("roof_deck", tk.offset_poly(top, -0.3), H_ROOF - 0.4, H_ROOF + 0.3, "roofd")
    c = tk.rot2((4.0, -1.0), YAW)
    tk.hvac_cluster("roof_plant", c[0], c[1], H_ROOF + 0.3, YAW, L * 0.45, W * 0.45, seed=3.0, hmax=2.0)
    tk.glow_ring("crown_light", top, H_TOP - 1.2, H_TOP - 0.4, 0.4, "white_Glow")
    tk.plinth("plaza", base, h=0.3, out=3.0)
    # street trees along Mission (the NW face, local -x)
    p0, p1 = tk.xform([(-L / 2 - 2.2, -W / 2 + 4), (-L / 2 - 2.2, W / 2 - 6)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=2.2)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
