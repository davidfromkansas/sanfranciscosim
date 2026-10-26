"""Deterministic Blender build of the SF-SIM miniature 450 Sutter Street.

    blender -b --python build_450_sutter_street.py -- [--out DIR]

450 Sutter Street, the Four Fifty Sutter Building (Miller & Pflueger, 1929):
a 26-storey Art Deco medical-dental tower in pinkish-tan terracotta moulded
with "Neo-Mayan" relief. Recognition cues: a dense rhythm of slim cream piers
running the full height and breaking the skyline as a toothed crest, rounded
corners, two stepped masses (the Sutter St wing taller than the rear wing)
and a higher central block on top. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "450-sutter-street"
CENTER = (-122.4078719, 37.7896446)   # OSM way 1186086081, OBB centre
H_TOP = 105.0                          # published roof 105 m / 344 ft (Wikipedia); DataSF LiDAR max 103.3 m
H_BASE = 7.5                           # two-storey base
PITCH = 3.6458                         # (95 - 7.5) / 24: storeys divide both wings exactly
H_SOUTH = H_BASE + 24 * PITCH          # 95.0, Sutter St wing (LiDAR majority roof 95 m)
H_NORTH = H_BASE + 21 * PITCH          # 84.06, rear wing, about three storeys lower (photo)
H_CORE = 101.5
YAW = math.radians(8.6)                # local +x runs along Sutter St (OSM edge bearing 98.6)
PTS = [(-16.5, -27.32), (-13.96, -26.91), (22.04, -21.45), (24.29, -21.08), (20.04, 4.9), (19.49, 8.29),
       (17.62, 19.74), (16.96, 23.76), (-0.3, 21.04), (-0.9, 24.79), (-24.28, 21.09), (-22.98, 13.01),
       (-19.87, -6.37)]
# wings in the local (Sutter-aligned) frame: (width, depth, cx, cy)
SOUTH = (40.8, 18.2, -0.1, -15.3)
NORTH = (40.4, 17.0, -0.2, 6.0)
LINK = (24.0, 5.0, -0.5, -4.0)
CORE = (15.0, 9.0, -1.0, -4.0)
R_CORNER = 1.6


def P(w, d, cx, cy):
    return tk.xform(tk.rect(w, d, cx, cy), YAW)


def wing(name, spec, z1, seed, inner):
    w, d, cx, cy = spec
    plan = P(w, d, cx, cy)
    # inner = +1/-1: the face toward the link (local +y / -y) gets no night skin, the link covers it
    # dark windows behind recessed terracotta spandrels, one band per storey
    tk.shaft(name, plan, H_BASE, z1, PITCH, glass="glassd", band="terracotta", band_h=1.7, band_out=0.15,
             fins=None, lit=0.0, glass_in=-0.25)
    # slim cream piers, proud of everything, running past the roof as a toothed crest
    tk.pier_grid(name + "_piers", tk.offset_poly(plan, -0.25), H_BASE, z1 + 1.8, 3.0, 0.55, 0.85, "cream",
                 corners=False)
    bands = [(H_BASE + i * PITCH + 1.7, H_BASE + (i + 1) * PITCH) for i in range(round((z1 - H_BASE) / PITCH))]
    tk.lit_windows(name + "_win", tk.offset_poly(plan, -0.25), bands, 3.0, 0.3, seed=seed, out=0.95,
                   margin=0.2, gap=0.8, edge_filter=lambda ei, p0, p1, nrm: tk.rot2(nrm, -YAW)[1] * inner < 0.9)
    # rounded corners, wrapped in terracotta
    for sx in (-1, 1):
        for sy in (-1, 1):
            x, y = tk.rot2((cx + sx * (w / 2 - R_CORNER * 0.6), cy + sy * (d / 2 - R_CORNER * 0.6)), YAW)
            tk.cylinder(f"{name}_corner_{sx}_{sy}", x, y, H_BASE, z1 + 1.0, R_CORNER, "terracotta", seg=6)
    # roof: parapet, deck raised clear of the glass cap
    tk.ring_band(name + "_parapet", tk.offset_poly(plan, -0.25), z1, z1 + 1.0, 0.2, "terracotta")
    tk.prism(name + "_deck", tk.offset_poly(plan, -0.6), z1 - 0.2, z1 + 0.1, "roofd")
    return plan


def build():
    base = tk.ccw(PTS)
    # base: terracotta podium on the full lot, tall bronze-framed openings on Sutter
    tk.prism("base", base, 0.0, H_BASE, "terracotta")
    south_face = lambda ei, p0, p1, nrm: nrm[1] < -0.9  # noqa: E731
    tk.arched_panes("base_arches", base, 0.6, H_BASE - 1.0, 4.5, 3.0, mat="bronze", edge_filter=south_face)
    tk.arched_panes("base_lit", base, 0.9, H_BASE - 2.0, 4.5, 2.2, mat="sand_Glow", out=0.1,
                    edge_filter=south_face, suffix="_glow")
    tk.ring_band("base_band", base, H_BASE - 0.6, H_BASE, 0.3, "cream")
    tk.prism("base_deck", tk.offset_poly(base, -0.3), H_BASE - 0.2, H_BASE + 0.1, "roofd")
    wing("south", SOUTH, H_SOUTH, 3.3, 1)
    wing("north", NORTH, H_NORTH, 8.1, -1)
    # link between the wings, set back to form light courts on the east and west faces
    w, d, cx, cy = LINK
    tk.prism("link", P(w, d, cx, cy), H_BASE, H_NORTH - 0.3, "terracotta", bottom=False)
    # the higher central block standing over the Sutter wing
    w, d, cx, cy = CORE
    core = P(w, d, cx, cy)
    tk.prism("core", core, H_NORTH - 0.5, H_CORE, "terracotta")  # stands on the link, no floating gap
    tk.pier_grid("core_piers", tk.offset_poly(core, -0.1), H_SOUTH, H_CORE + 1.2, 3.0, 0.55, 0.6, "cream")
    tk.panes("core_win", core, tk.floors(H_NORTH, H_SOUTH, PITCH) + [(H_SOUTH + 0.5, H_SOUTH + 3.3), (H_SOUTH + 3.3, H_CORE - 0.5)], 3.0,
             mat="glassd", gap=1.0, margin=0.5)
    tk.lit_windows("core_lit", core, [(H_SOUTH + 3.3, H_CORE - 0.5)], 3.0, 0.6, seed=1.9, out=0.1,
                   margin=0.5, gap=1.0, mat="white_Glow")
    tk.prism("core_cap", tk.offset_poly(core, -1.5), H_CORE, H_TOP, "terracotta")
    tk.glow_ring("crown_light", core, H_CORE + 0.2, H_CORE + 1.0, 0.65, "white_Glow")
    tk.plinth("sidewalk", base, h=0.3, out=3.0)
    p0, p1 = tk.xform([(-14.0, -27.0), (14.0, -27.0)], YAW)   # Sutter St trees
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=2.6)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
