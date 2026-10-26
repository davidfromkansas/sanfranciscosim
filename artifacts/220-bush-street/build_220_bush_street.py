"""Deterministic Blender build of the SF-SIM miniature Mills Tower.

    blender -b --python build_220_bush_street.py -- [--out DIR]

Mills Tower, 220 Bush Street (Lewis P. Hobart, 1931): the 22-storey annex
behind the 1892 Burnham & Root Mills Building, a thin north-south slab in buff
brick and terracotta that matches the older block. Vertical window strips
between brick piers, a stone base on Bush, round-arched windows on the top two
storeys under a cornice and a stepped parapet. Helpers in
tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "220-bush-street"
CENTER = (-122.4013027, 37.7914215)   # OSM way 256066232, OBB centre
H_TOP = 92.0                           # published roof 92 m (Wikipedia infobox); LiDAR roof 93.1 m
H_BASE, H_SHAFT, H_ATTIC, H_ROOF = 6.5, 82.5, 88.8, 90.0
H_OLD = 47.0                           # the 10-storey Mills Building against the west wall (46.94 m)
L, W = 42.6, 13.5                     # OSM OBB 43.1 x 13.7; local +x = bearing 171 (Bush St, south)
YAW = tk.bearing_to_yaw(171.0)


def face(ei, p0, p1, nrm):
    """Compass name of an edge's outward normal: S (Bush), N, E, W (party wall)."""
    brg = math.degrees(math.atan2(nrm[0], nrm[1])) % 360
    return "NESW"[int(((brg + 45) % 360) // 90)]


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # granite base with the Bush St entrance arch
    tk.prism("base", plan, 0.0, H_BASE, "stone", bev=0.12)
    tk.panes("base_win", plan, [(0.0, H_BASE - 1.0)], 3.6, mat="glassd", margin=0.6, gap=1.0,
             edge_filter=lambda *a: face(*a) != "W")
    tk.lit_windows("base_lit", plan, [(0.0, H_BASE - 1.0)], 3.6, 0.8, seed=2.0, out=0.1, margin=0.8, gap=1.2,
                   edge_filter=lambda *a: face(*a) != "W")
    c = tk.rot2((L / 2 + 0.3, 0.0), YAW)
    tk.box("portal", c[0], c[1], 0.0, H_BASE + 1.2, 0.8, 6.0, "cream", yaw=YAW, bev=0.1)
    # shaft: buff brick, window strips between piers, a terracotta spandrel band each storey
    tk.prism("shaft", plan, H_BASE, H_SHAFT, "terracotta", bev=0.12)
    tk.ring_band("base_band", plan, H_BASE, H_BASE + 0.8, 0.25, "cream")
    tk.panes("strips", plan, [(H_BASE + 0.8, H_SHAFT)], 2.65, mat="glassd", margin=0.0, gap=1.25,
             edge_filter=lambda *a: face(*a) != "W")
    tk.panes("strips_w", plan, [(H_OLD + 0.5, H_SHAFT)], 2.65, mat="glassd", margin=0.0, gap=1.25,
             edge_filter=lambda *a: face(*a) == "W")
    bands = tk.floors(H_BASE + 0.8, H_SHAFT, 4.0)
    tk.spandrels("spandrels", plan, [z for z, _ in bands[1:]], 0.7, 0.12, "terracotta")
    tk.lit_windows("lit", plan, bands, 2.65, 0.28, seed=6.1, out=0.1, margin=0.8, gap=1.35,
                   edge_filter=lambda *a: face(*a) != "W")
    tk.lit_windows("lit_w", plan, [b for b in bands if b[0] > H_OLD], 2.65, 0.28, seed=9.3, out=0.1, margin=0.8,
                   gap=1.35, edge_filter=lambda *a: face(*a) == "W")
    # arched top two storeys, cornice, stepped parapet and the roof
    tk.ring_band("attic_band", plan, H_SHAFT, H_SHAFT + 0.6, 0.3, "cream")
    tk.prism("attic", plan, H_SHAFT + 0.6, H_ATTIC, "terracotta")
    tk.arched_panes("attic_arches", plan, H_SHAFT + 1.0, H_ATTIC - 0.4, 2.65, 1.5, mat="glassd")
    tk.arched_panes("attic_lit", plan, H_SHAFT + 1.2, H_ATTIC - 1.0, 2.65, 1.0, mat="sand_Glow", out=0.1,
                    suffix="_glow")
    tk.cornice("cornice", plan, H_ATTIC, h=1.2, out=0.7, mat="cream")
    tk.ring_band("parapet", tk.offset_poly(plan, -0.3), H_ROOF, H_ROOF + 1.0, 0.3, "terracotta")
    tk.prism("roof", plan, H_ROOF - 0.2, H_ROOF + 0.1, "roofd")
    ph = tk.xform(tk.rect(L - 16.0, W - 5.0), YAW)
    tk.prism("penthouse", ph, H_ROOF + 0.1, H_TOP - 0.5, "terracotta", bev=0.1)
    tk.cornice("penthouse_cap", ph, H_TOP - 0.5, h=0.5, out=0.3, mat="cream")
    tk.glow_ring("crown_light", ph, H_TOP - 1.6, H_TOP - 0.9, 0.06, "sand_Glow")
    pc = tk.rot2((-L / 2 + 4.5, 0.0), YAW)
    tk.hvac_cluster("plant", pc[0], pc[1], H_ROOF + 0.1, YAW, 6.0, 7.0, seed=4.0, hmax=1.6)
    tk.plinth("sidewalk", plan, h=0.25, out=2.5)
    p0, p1 = tk.xform([(L / 2 + 2.0, -W / 2 + 2.5), (L / 2 + 2.0, W / 2 - 2.5)], YAW)
    tk.tree_row("trees", p0, p1, 0.25, 2, h=6.0, seed=3.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
