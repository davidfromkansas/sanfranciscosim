"""Deterministic Blender build of the SF-SIM miniature 181 Fremont.

    blender -b --python build_181_fremont.py -- [--out DIR]

The slender tapering tower next to Salesforce Park (Heller Manus, 2018): pale
aqua glass, chamfered corners, and the identity cue - white exterior
mega-braces that draw a giant "A" up every face - ending in a sloped crown and
a spire at 244.4 m. See REFERENCE.md for sources; helpers in
tools/landmark-kit/toykit.py. World space, metres, +X east, +Y north.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "181-fremont"
CENTER = (-122.395309, 37.789766)   # OSM way 445566153, OBB centre
H_SPIRE = 244.4                     # architectural top (spire)
H_ROOF_LO = 206.0                   # low side of the sloped crown
H_ROOF_HI = 220.0                   # high side
H_LOBBY = 12.0
W0, D0 = 39.0, 34.0                 # plan at grade (OSM OBB 40.6 x 35.5)
W1, D1 = 29.0, 25.0                 # plan at the crown: the shaft tapers
CH0, CH1 = 6.5, 4.5                 # corner chamfer legs
YAW = math.radians(45.0)            # faces run 45 / 135 degrees


def plan_at(z, off=0.0):
    t = min(max(z / H_ROOF_HI, 0.0), 1.0)
    w, d, c = W0 + (W1 - W0) * t, D0 + (D1 - D0) * t, CH0 + (CH1 - CH0) * t
    return tk.xform(tk.offset_poly(tk.chamfer_rect(w, d, c), off), YAW)


def roof_z(x, y):
    """Sloped crown: low on the SE side, high on the NW, cut on one plane."""
    u, v = tk.rot2((x, y), -YAW)
    t = (v / (D1 / 2) + 1) / 2
    return H_ROOF_LO + (H_ROOF_HI - H_ROOF_LO) * max(0.0, min(1.0, t))


def build():
    # shaft: glass loft with storey-group bands, then the sloped top cut
    pitch = 7.6
    tk.banded_loft("shaft", plan_at, H_LOBBY, H_ROOF_LO, pitch, 0.9, 0.35,
                   tk.material("verdigris"), tk.material("trim"), glass_in=-0.2)
    # sloped crown wedge: from the low roof up to the plane
    lo = plan_at(H_ROOF_LO, -0.2)
    hi = [(x, y) for x, y in plan_at(H_ROOF_HI, -0.2)]
    verts = [(x, y, H_ROOF_LO) for x, y in lo] + [(x, y, roof_z(x, y)) for x, y in hi]
    n = len(lo)
    faces = [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    faces += [tuple(range(n - 1, -1, -1)), tuple(range(n, 2 * n))]
    tk.new_mesh("crown_glass", verts, faces, ["verdigris"])
    # crown screen frame: a white rim tracing the sloped cut
    rim_o = plan_at(H_ROOF_HI, 0.45)
    rim_i = plan_at(H_ROOF_HI, -0.9)
    verts = []
    for loop in (rim_i, rim_o):
        verts += [(x, y, roof_z(x, y) - 1.4) for x, y in loop]
    for loop in (rim_o, rim_i):
        verts += [(x, y, roof_z(x, y) + 0.6) for x, y in loop]
    faces = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    tk.new_mesh("crown_rim", verts, faces, ["white"])
    # roof deck plant + spire on the high side
    sx, sy = tk.rot2((0.0, D1 * 0.18), YAW)
    tk.cylinder("spire", sx, sy, H_ROOF_HI - 2, H_SPIRE - 1.2, 0.8, "white", seg=8, r1=0.25)
    tk.cylinder("spire_tip_glow", sx, sy, H_SPIRE - 1.2, H_SPIRE, 0.45, "red_Glow", seg=6)

    # thin white mullions every ~4.5 m: the fine vertical grain of the wall
    tk.loft_fins("mullions", plan_at, H_LOBBY, H_ROOF_LO, 4.5, 0.35, 0.3, "trim")
    # mega-braces: a giant "A" on every face (bottom corners -> top centre)
    z0, z1 = H_LOBBY, H_ROOF_LO - 2
    for fi in range(4):
        rot = YAW + fi * math.pi / 2
        def half(z):
            t = min(max(z / H_ROOF_HI, 0.0), 1.0)
            w, d, c = W0 + (W1 - W0) * t, D0 + (D1 - D0) * t, CH0 + (CH1 - CH0) * t
            return ((w if fi % 2 == 0 else d) / 2, (d if fi % 2 == 0 else w) / 2, c)
        hw0, hd0, c0 = half(z0)
        hw1, hd1, c1 = half(z1)
        for side in (-1, 1):
            a = (*tk.rot2((side * (hw0 - c0), -hd0 - 0.35), rot), z0)
            b = (*tk.rot2((side * 0.9, -hd1 - 0.35), rot), z1)
            tk.tube(f"brace_{fi}_{side}", a, b, 2.2, 1.0, tk.rot2((0, -1), rot), "white")
        # horizontal ties where the A's cross-bar would be
        zt = z0 + (z1 - z0) * 0.5
        hwt, hdt, ct = half(zt)
        xa = (hw0 - c0) + ((0.9) - (hw0 - c0)) * 0.5
        a = (*tk.rot2((-xa, -hdt - 0.35), rot), zt)
        b = (*tk.rot2((xa, -hdt - 0.35), rot), zt)
        tk.tube(f"tie_{fi}", a, b, 1.2, 0.7, tk.rot2((0, -1), rot), "white")
    # night: residential floors lit warm, crown lit cool
    bands = tk.floors(H_LOBBY + 1, H_ROOF_LO - 4, pitch / 2)
    tk.lit_loop_windows("win", plan_at, bands, 0.32, seed=5.1, out=-0.1, margin=0.7, subdiv=3, gap=0.1)
    tk.glow_ring("crown_light", plan_at(H_ROOF_LO + 1, -0.1), H_ROOF_LO + 1, H_ROOF_LO + 6, 0.0, "white_Glow")

    # lobby: tall glazed base set back behind white columns
    tk.prism("lobby", plan_at(0, -1.6), 0.0, H_LOBBY, "glassl")
    tk.glow_ring("lobby_lit", plan_at(0, -1.6), 1.0, H_LOBBY - 1.2, 0.06, "sand_Glow")
    tk.ring_band("lobby_head", plan_at(H_LOBBY - 1.6), H_LOBBY - 1.6, H_LOBBY, 0.4, "white", inset=-1.8)
    tk.pier_grid("lobby_cols", plan_at(0, -0.4), 0.0, H_LOBBY - 1.6, 7.0, 1.0, 1.0, "white", skip_short=8.0)
    tk.plinth("plaza", plan_at(0), h=0.3, out=4.0)
    p = plan_at(0, 3.0)
    tk.tree_row("trees", p[0], p[1], 0.3, 2, h=6.5, seed=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_SPIRE)
