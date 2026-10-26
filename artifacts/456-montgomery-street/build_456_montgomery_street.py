"""Deterministic Blender build of the SF-SIM miniature 456 Montgomery Street.

    blender -b --python build_456_montgomery_street.py -- [--out DIR]

456 Montgomery Street (1986, 26 storeys, 115.2 m): a crisp white tower ribbed with
close-set vertical piers, cantilevered on a dark recessed floor over a preserved
two-storey granite Beaux-Arts bank at the Montgomery x Sacramento corner (columns
in antis, balustrade). Recognition cues: the white pinstripe shaft floating over
the old grey bank. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "456-montgomery-street"
CENTER = (-122.402634, 37.7935765)   # OSM way 151183779, OBB centre
H_TOP = 115.2                         # published (CTBUH via Wikipedia list)
A = math.radians(9.0)                 # street grid: local u = bearing 81 (E), v = bearing 351 (N)
H_BANK, H_GAP, H_ROOF = 15.0, 21.0, 111.5


def G(poly):
    return tk.xform(poly, A)


def build():
    # OSM footprint in grid frame (u, v): Montgomery St on -u (W), Sacramento on +v (N)
    base = G([(-14.5, -13.8), (4.2, -13.9), (6.3, -13.9), (6.3, -20.9), (14.4, -21.0), (14.5, 20.9), (-14.4, 21.0)])
    base = [p for i, p in enumerate(base) if i != 1]  # drop the collinear node
    # the old granite bank: two tall storeys, cornice, balustrade
    tk.prism("bank", base, 0.0, H_BANK, "stone", bev=0.15)
    street = lambda ei, p0, p1, n: (n[0] * math.cos(A + math.pi) + n[1] * math.sin(A + math.pi) > 0.7  # noqa: E731
                                    or -n[0] * math.sin(A) + n[1] * math.cos(A) > 0.7)
    bands = [(0.8, 7.2), (7.8, 14.0)]
    tk.panes("bank_win", base, bands, 4.2, mat="glassd", gap=1.6, margin=0.4, edge_filter=street)
    west = lambda ei, p0, p1, n: n[0] * math.cos(A + math.pi) + n[1] * math.sin(A + math.pi) > 0.7  # noqa: E731
    tk.lit_windows("bank_lit", base, [(0.8, 7.2)], 4.2, 0.9, seed=1.0, out=0.1, margin=0.6, gap=2.0, edge_filter=west)
    tk.cornice("bank_cornice", base, H_BANK, h=1.0, out=0.7, mat="stone")
    tk.ring_band("balustrade", base, H_BANK + 1.0, H_BANK + 2.2, 0.3, "stone")
    # four columns in antis on the Sacramento (N) face near the Montgomery corner
    for k in range(4):
        cx, cy = G([(-12.0 + k * 3.4, 21.9)])[0]
        tk.cylinder(f"col_{k}", cx, cy, 0.0, H_BANK, 0.75, "stone", seg=8)
    # dark recessed transfer floor: the tower floats over the bank
    tower = G(tk.rect(29.4, 38.4, 0.0, 1.5))
    tk.prism("gap", tk.offset_poly(tower, -2.5), H_BANK + 2.2, H_GAP, "glassd")
    tk.glow_ring("gap_lit", tk.offset_poly(tower, -2.5), H_BANK + 2.8, H_GAP - 0.6, 0.06, "sand_Glow")
    tk.prism("soffit", tower, H_GAP, H_GAP + 1.6, "white", bev=0.15)
    # white pinstripe shaft: 25 office storeys of 3.56 m, white piers every ~1.9 m
    tk.shaft("shaft", tower, H_GAP + 1.6, H_ROOF, (H_ROOF - H_GAP - 1.6) / 25, glass="glassd", band="white",
             band_h=0.9, band_out=0.15, fins=(1.9, 0.8, 0.45, "white"), lit=0)
    # night skin laid just proud of the piers (panes wider than a pier bay would be hidden)
    z0 = H_GAP + 1.6
    p = (H_ROOF - z0) / 25
    tk.lit_windows("shaft_lit", tk.offset_poly(tower, 0.55), [(z0 + i * p + 0.9, z0 + (i + 1) * p) for i in range(25)],
                   3.8, 0.28, seed=4.0, out=0.0, margin=0.3, gap=0.4)
    # crown: a plain white parapet storey with dark louvre slots, deck and plant
    deck = 112.6
    tk.prism("crown", tk.offset_poly(tower, 0.25), H_ROOF, deck, "white", bev=0.12)
    tk.ring_band("parapet", tk.offset_poly(tower, 0.25), deck, H_TOP, 0.0, "white", inset=-0.6)
    tk.panes("crown_slots", tk.offset_poly(tower, 0.25), [(H_ROOF + 0.3, H_TOP - 0.5)], 3.0, mat="glassd", gap=1.2,
             margin=0.4)
    tk.prism("roof_deck", tk.offset_poly(tower, -0.5), deck - 0.2, deck + 0.05, "roofd")
    c = G([(0.0, 1.5)])[0]
    tk.hvac_cluster("roof_plant", c[0], c[1], deck + 0.05, A, 16.0, 22.0, seed=3.0, hmax=2.4)
    tk.glow_ring("crown_light", tk.offset_poly(tower, 0.25), H_TOP - 2.6, H_TOP - 1.4, 0.12, "white_Glow")
    tk.plinth("sidewalk", base, h=0.25, out=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
