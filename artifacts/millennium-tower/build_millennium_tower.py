"""Deterministic Blender build of the SF-SIM miniature Millennium Tower.

    blender -b --python build_millennium_tower.py -- [--out DIR]

301 Mission Street (Handel Architects, 2009): a 58-storey residential tower
of deep blue glass striped by fine white vertical mullions, on a long
rounded plan, whose top steps down in three terraces. Recognition cues: the
dark-blue column, the white pinstripes, the stepped crown. Helpers in
tools/landmark-kit/toykit.py; sources in REFERENCE.md.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "millennium-tower"
CENTER = (-122.396191, 37.790415)   # OSM way 72963089, OBB centre
H_TOP = 197.0                        # architectural top (645 ft)
H_LOBBY = 10.0
L, W = 46.0, 30.0                    # OSM OBB 47.9 x 33.1 m
YAW = math.radians(90 - 135.5)      # long axis runs 135.5 degrees (SE)
TIERS = [(171.0, 1.0), (179.0, 0.82), (187.0, 0.64), (193.5, 0.46)]


def plan(length=1.0, off=0.0):
    """Rounded plan, shortened from the NW end (the SE end stays put)."""
    l = L * length
    p = tk.rounded_rect(l, W, 9.0, seg=4, cx=(L - l) / 2)
    return tk.xform(tk.offset_poly(p, off), YAW)


def build():
    base = plan()
    tk.prism("lobby", plan(1.0, -1.5), 0.0, H_LOBBY, "glassl")
    tk.glow_ring("lobby_lit", plan(1.0, -1.5), 0.8, H_LOBBY - 1.0, 0.06, "sand_Glow")
    tk.ring_band("canopy", base, H_LOBBY - 1.2, H_LOBBY, 2.2, "white", inset=-1.6)
    z = H_LOBBY
    for i, (zt, frac) in enumerate(TIERS):
        p = plan(frac)
        # whole storey-groups per tier: a leftover sliver shorter than a band
        # would leave a zero-height loft row (degenerate triangles)
        pitch = (zt - z) / max(1, round((zt - z) / 6.0))
        tk.shaft(f"tier{i}", p, z, zt, pitch, glass="navy", band="glass", band_h=0.6, band_out=0.12,
                 fins=(3.0, 0.32, 0.35, "white"), lit=0.34, seed=2.0 + i, lit_spacing=3.0)
        # terrace edge on each setback, with a planter line
        nxt = TIERS[i + 1][1] if i + 1 < len(TIERS) else None
        if nxt:
            tk.prism(f"terrace{i}", tk.offset_poly(p, 0.2), zt, zt + 0.6, "trim")
        z = zt
    top = plan(TIERS[-1][1])
    tk.roof_kit("roof", top, H_TOP - 3.5, seed=4.0, parapet=1.0, plant_frac=0.5, yaw=YAW)
    # crown screen: the last metres are a white mechanical screen
    tk.ring_band("crown_screen", tk.offset_poly(top, -0.4), H_TOP - 3.5, H_TOP, 0.5, "white")
    tk.glow_ring("crown_light", top, H_TOP - 3.2, H_TOP - 0.4, 0.15, "white_Glow")
    tk.plinth("plaza", base, h=0.3, out=3.5)
    a = tk.xform([(-L / 2 + 6, -W / 2 - 2.5), (L / 2 - 6, -W / 2 - 2.5)], YAW)
    tk.tree_row("trees", a[0], a[1], 0.3, 3, h=6.0, seed=7.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
