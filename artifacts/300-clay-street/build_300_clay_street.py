"""Deterministic Blender build of the SF-SIM miniature One Maritime Plaza (Alcoa Building).

    blender -b --python build_300_clay_street.py -- [--out DIR]

300 Clay Street (Skidmore, Owings & Merrill, 1967): a 27-storey dark office slab
wrapped in an external lattice of dark bronze aluminium-clad steel X-braces, one of the
first towers anywhere to put its seismic bracing on the outside. It rises from the
raised Maritime Plaza, a roof garden over a parking podium. Recognition cues: the
giant dark diagonal lattice on every face and the plain flat top. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "300-clay-street"
CENTER = (-122.3992506, 37.7956183)  # OSM way 28240176, OBB centre
H_TOP = 121.3                         # published roof (Wikipedia 121.3 m); LiDAR max 120.98 m
H_BASE = 9.0                          # open colonnade storeys at the plaza (estimated)
H_SHAFT = 118.0
L, W = 63.6, 32.6                     # OSM OBB 64.3 x 33.3 (long axis bearing 171)
YAW = math.radians(90 - 171.0)        # local +x = bearing 171 (S); +y = bearing 81 (E, toward Front St)
BAYS_L, BAYS_W, LEVELS = 4, 2, 7      # photo: 4 X-bays on the long faces, 2 on the ends
OUT = 1.2                             # the lattice stands proud of the glass


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # open base: recessed glass lobby under the shaft, dark columns at the bays
    lobby = tk.offset_poly(plan, -3.0)
    tk.prism("lobby", lobby, 0.0, H_BASE, "glassd")
    tk.glow_ring("lobby_lit", lobby, 0.6, H_BASE - 1.5, 0.06, "sand_Glow")
    # shaft: reflective glass (pale, for contrast with the lattice) with bronze spandrels; 27 storeys
    pitch = (H_SHAFT - H_BASE) / 27
    tk.shaft("shaft", plan, H_BASE, H_SHAFT, pitch, glass="glassg", band="bronze", band_h=0.9, band_out=0.12,
             fins=None, lit=0.28, seed=3.0, lit_spacing=5.3)
    # top: the louvred plant band, a plain dark fascia flush with the lattice
    tk.ring_band("roof_fascia", tk.offset_poly(plan, -0.2), H_SHAFT, H_TOP, 0.2 + OUT, "ink")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.3), H_SHAFT - 0.3, H_SHAFT + 0.05, "roofd")
    tk.hvac_cluster("roof_plant", 0.0, 0.0, H_SHAFT, YAW, 30.0, 14.0, seed=4.0, hmax=H_TOP - H_SHAFT - 0.3)
    # the X-brace lattice: corner and bay columns, level ties and an X in every panel, all standing OUT proud
    zl = [H_BASE + (H_SHAFT - H_BASE) * i / LEVELS for i in range(LEVELS + 1)]
    objs = []
    for ei, (p0, p1, Le, nrm) in enumerate(tk.edges(plan)):
        nb = BAYS_L if Le > 45 else BAYS_W
        o = (nrm[0] * OUT, nrm[1] * OUT)

        def at(t, z):
            return (p0[0] + (p1[0] - p0[0]) * t + o[0], p0[1] + (p1[1] - p0[1]) * t + o[1], z)
        for li in range(LEVELS):
            za, zb = zl[li], zl[li + 1]
            for bi in range(nb):
                ta, tb = bi / nb, (bi + 1) / nb
                objs.append(tk.tube(f"x_{ei}_{li}_{bi}a", at(ta, za), at(tb, zb), 1.0, 0.8, nrm, "ink"))
                objs.append(tk.tube(f"x_{ei}_{li}_{bi}b", at(tb, za), at(ta, zb), 1.0, 0.8, nrm, "ink"))
        for li in range(1, LEVELS + 1):
            objs.append(tk.tube(f"tie_{ei}_{li}", at(0.0, zl[li]), at(1.0, zl[li]), 0.7, 0.8, nrm, "ink"))
        for bi in range(1, nb):
            objs.append(tk.tube(f"col_{ei}_{bi}", at(bi / nb, 0.0), at(bi / nb, H_SHAFT), 1.0, 0.8, nrm, "ink"))
    tk.join(objs, "lattice")
    for k, p in enumerate(plan):
        c = tk.offset_poly(plan, OUT)[k]
        tk.box(f"corner_col_{k}", c[0], c[1], 0.0, H_SHAFT, 1.8, 1.8, "ink", yaw=YAW)
    tk.glow_ring("crown_light", plan, H_SHAFT + 0.8, H_SHAFT + 1.8, OUT + 0.45, "white_Glow")
    # Maritime Plaza: the raised garden deck round the tower (a strip of it), with trees
    tk.prism("plaza", tk.offset_poly(plan, 9.0), 0.0, 0.6, "stone", bev=0.1)
    for k, (x, y) in enumerate(((-L / 2 - 5.0, 0.0), (L / 2 + 5.0, 0.0))):
        px, py = tk.rot2((x, y), YAW)
        tk.tree(f"plaza_tree_{k}", px, py, 0.6, h=6.5, r=2.6, mat="leaf" if k % 2 else "leafd")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
