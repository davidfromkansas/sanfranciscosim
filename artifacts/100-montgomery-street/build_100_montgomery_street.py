"""Deterministic Blender build of the SF-SIM miniature 100 Montgomery Street.

    blender -b --python build_100_montgomery_street.py -- [--out DIR]

100 Montgomery Street, the Equitable Life Building (William Peugh / Irwin
Clavan, 1955): a 25-storey slab, one of San Francisco's first post-war office
towers - white marble piers in a steady vertical rhythm between bays of
aluminium-framed windows, solid marble corners, a two-storey stone base, and a
flat roof. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "100-montgomery-street"
CENTER = (-122.4018706, 37.7903435)   # OSM way 132125166, OBB centre
H_ROOF = 104.3                         # main parapet (estimated: crest minus the penthouse)
H_TOP = 107.9                          # 354 ft (published); taken as the crest incl. the plant penthouse
H_BASE = 9.0
L, W = 51.8, 33.4                      # OSM OBB 52.0 x 33.7
YAW = math.radians(90 - 81.7)          # long faces look N and S


def build():
    plan = tk.xform(tk.rect(L, W), YAW)
    # two-storey marble base with big punched windows
    tk.prism("base", plan, 0.0, H_BASE, "white", bev=0.15)
    tk.panes("base_win", plan, [(0.4, 3.9), (4.8, 8.2)], 5.4, mat="glassd", gap=1.6, margin=0.3)
    tk.lit_windows("base_lit", plan, [(0.4, 3.9)], 5.4, 0.85, seed=2.0, out=0.1, margin=0.3, gap=1.8)
    # shaft: 23 storeys of silvery glass with aluminium spandrels behind broad marble piers
    tk.shaft("shaft", plan, H_BASE, H_ROOF - 1.2, (H_ROOF - 1.2 - H_BASE) / 23, glass="glassg", band="steel",
             band_h=0.6, band_out=0.08, fins=(6.4, 2.0, 0.35, "white"), lit=0.3, seed=3.0, lit_spacing=6.4)
    tk.ring_band("parapet", tk.offset_poly(plan, -0.4), H_ROOF - 1.2, H_ROOF, 0.75, "white")
    tk.prism("roof_deck", tk.offset_poly(plan, -0.3), H_ROOF - 1.5, H_ROOF - 0.9, "roofd")
    # plant penthouse set back on the roof
    ph = tk.xform(tk.rect(22.0, 14.0, 4.0, 0.0), YAW)
    tk.prism("penthouse", ph, H_ROOF - 0.9, H_TOP, "stone", bev=0.15)
    c = tk.rot2((-16.0, 0.0), YAW)
    tk.hvac_cluster("roof_plant", c[0], c[1], H_ROOF - 0.9, YAW, 12.0, 18.0, seed=5.0, hmax=2.8)
    tk.glow_ring("crown_light", plan, H_ROOF - 1.0, H_ROOF - 0.3, 0.42, "white_Glow")
    tk.plinth("plaza", plan, h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
