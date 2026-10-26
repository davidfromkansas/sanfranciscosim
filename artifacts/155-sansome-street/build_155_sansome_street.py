"""Deterministic Blender build of the SF-SIM miniature Stock Exchange Tower.

    blender -b --python build_155_sansome_street.py -- [--out DIR]

155 Sansome Street (Miller & Pflueger, 1929-30): the office tower of the
San Francisco Stock Exchange, built with the trading hall at 301 Pine (its own
artifact, against this tower's north side). A narrow twelve-storey Moderne
slab of pale grey granite running west from Sansome Street: an entrance under
Ralph Stackpole's carved relief and the gilt "155 SANSOME" panel, a shaft of
punched windows between flat vertical piers, and a stepped crown (the City
Club with Diego Rivera's mural sits in the top floors). Helpers in
tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "155-sansome-street"
CENTER = (-122.4012628, 37.7916701)  # OSM way 256066241, OBB centre
H_TOP = 64.05                         # facts-file LiDAR peak (stepped crown); main roof 54.6 = ring median
H_ROOF = 54.6
YAW = tk.bearing_to_yaw(81.3)         # local +x = east (Sansome St end), +y = north (301 Pine)
X0, X1, Y0, Y1 = -24.0, 24.0, -5.1, 5.1


def L(poly):
    return tk.xform(poly, YAW)


def P(x, y):
    return tk.rot2((x, y), YAW)


def east(ei, p0, p1, n):
    return tk.rot2(n, -YAW)[0] > 0.9


def build():
    plan = L(tk.rect(X1 - X0, Y1 - Y0))
    tk.prism("base", plan, 0.0, 7.6, "stone", bev=0.15)
    tk.panes("base_win", plan, [(0.0, 7.6)], 3.4, mat="glassd", gap=1.2, margin=1.0,
             edge_filter=lambda *a: not east(*a))
    # Sansome entrance: recessed lit door, Stackpole relief, gilt name panel
    tk.box("portal", *P(X1 + 0.3, 0.0), 0.0, 9.0, 0.6, 7.2, "white", yaw=YAW, bev=0.1)
    door = L(tk.rect(0.4, 3.6, X1 + 0.4, 0.0))
    tk.panes("door", door, [(0.2, 4.4)], 3.6, mat="glassd", gap=0.2, margin=0.0, edge_filter=east)
    tk.lit_windows("door_lit", door, [(0.4, 4.2)], 3.6, 1.0, out=0.1, margin=0.0, gap=0.6, edge_filter=east)
    tk.box("name_panel", *P(X1 + 0.65, 0.0), 4.7, 5.4, 0.1, 5.0, "gold", yaw=YAW)
    tk.box("relief_disc", *P(X1 + 0.7, 0.0), 5.6, 8.6, 0.25, 3.0, "stone", yaw=YAW, bev=0.08)
    tk.box("relief_fig", *P(X1 + 0.95, 0.0), 5.8, 9.3, 0.4, 0.9, "white", yaw=YAW, bev=0.15)
    tk.ring_band("base_cap", plan, 7.6, 8.2, 0.25, "white")
    # shaft: 11 storeys of 4.22 m, punched windows between flat piers
    tk.punched_block("shaft", plan, 8.2, 54.6, 4.218, wall="stone", win="glassd", spacing=2.5, gap=1.0,
                     margin=0.8, lit=0.3, seed=5.0, bev=0.12)
    tk.pier_grid("piers", plan, 8.2, H_ROOF + 0.6, 2.5, 0.5, 0.25, "white", skip_short=6.0)
    tk.ring_band("parapet", plan, H_ROOF, H_ROOF + 0.6, 0.2, "white")
    tk.prism("roof", tk.offset_poly(plan, -0.3), H_ROOF - 0.3, H_ROOF + 0.1, "roofd")
    # stepped crown toward Sansome (City Club floors)
    s1 = L(tk.rect(22.0, 8.4, 11.0, 0.0))
    tk.punched_block("crown1", s1, H_ROOF + 0.1, 59.4, 4.7, wall="stone", win="glassd", spacing=2.5, gap=1.0,
                     margin=0.9, lit=0.5, seed=9.0, bev=0.1)
    tk.ring_band("crown1_cap", s1, 59.4, 59.9, 0.2, "white")
    s2 = L(tk.rect(9.0, 6.0, 15.5, 0.0))
    tk.prism("crown2", s2, 59.9, H_TOP - 0.4, "stone", bev=0.1)
    tk.ring_band("crown2_cap", s2, H_TOP - 0.4, H_TOP, 0.2, "white")
    tk.glow_ring("crown_line", s2, H_TOP - 1.0, H_TOP - 0.5, 0.06, "white_Glow")
    tk.hvac_cluster("plant", *P(-10.0, 0.0), H_ROOF + 0.1, YAW, 14.0, 6.0, seed=2.0, hmax=2.2, fans=False)
    tk.prism("sidewalk", L(tk.rect(X1 - X0 + 4.0, Y1 - Y0 + 4.0)), 0.0, 0.15, "concrete")


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
