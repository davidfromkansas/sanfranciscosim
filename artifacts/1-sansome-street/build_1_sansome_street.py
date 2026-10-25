"""Deterministic Blender build of the SF-SIM miniature One Sansome Street.

    blender -b --python build_1_sansome_street.py -- [--out DIR]

One Sansome Street (William L. Pereira & Associates, 1984; Citigroup Center):
a 41-storey pale grey granite tower with generously rounded corners and rows
of green-tinted windows, standing on tall piers behind the 1910 Anglo and
London Paris National Bank (Albert Pissis) - a granite temple with 38 ft
Doric columns and a balustrade at the Sutter x Sansome corner, kept as the
tower's glass-roofed conservatory. Deep recessed openings cut the top storeys.
Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "1-sansome-street"
CENTER = (-122.4011756, 37.7904654)   # OSM way 32963344, OBB centre
H_TOP = 168.0                          # published roof (Wikipedia 168 m); LiDAR 174.18
H_PIERS = 21.0                         # INFERRED: tower body starts just above the bank balustrade (photo)
H_BANK = 18.0                          # INFERRED: 38 ft columns + base + entablature + balustrade
H_WING = 21.0                          # INFERRED: low west wing
YAW = tk.bearing_to_yaw(81.5)          # local +x = bearing 81.5 (along Sutter St), +y = 351.5 (Sansome St)

# Local plans (x ~ east, y ~ north) from the 11-node OSM outline. Sansome St = east
# face, Sutter St = south face; the bank holds the SE corner.
TOWER_W, TOWER_D = 37.5, 33.4
TOWER_C = (-8.95, -4.3)
BANK = [(9.8, -21.0), (36.5, -21.1), (36.5, 21.0), (9.8, 20.9)]
WING = [(-36.5, -16.3), (-27.7, -16.3), (-27.7, 12.4), (-36.5, 12.4)]


def build():
    tower = tk.xform(tk.rounded_rect(TOWER_W, TOWER_D, 6.5, seg=3), YAW, *tk.rot2(TOWER_C, YAW))
    core = tk.xform(tk.rounded_rect(TOWER_W - 6, TOWER_D - 6, 4.0, seg=2), YAW, *tk.rot2(TOWER_C, YAW))
    # tall piers and a recessed glass lobby under the tower
    tk.prism("lobby", core, 0.0, H_PIERS, "glassd")
    tk.glow_ring("lobby_lit", core, 0.8, 8.0, 0.06, "sand_Glow")
    tk.pier_grid("piers", tk.xform(tk.rect(TOWER_W - 3, TOWER_D - 3), YAW, *tk.rot2(TOWER_C, YAW)), 0.0, H_PIERS,
                 7.0, 1.6, 1.6, "stone")
    # tower body: pale granite, one row of green windows per storey on the flat faces
    tk.prism("tower", tower, H_PIERS, H_TOP - 1.0, "stone", bev=0.2)
    rows = tk.floors(H_PIERS + 0.5, H_TOP - 9.0, 3.7244)    # 37 storeys of windows
    flat = lambda ei, p0, p1, n: tk.edges(tower)[ei][2] > 10.0  # noqa: E731
    tk.panes("tower", tower, [(z0 + 1.4, z1 - 0.3) for z0, z1 in rows], 4.1, mat="copper", out=0.07,
             margin=0.0, gap=1.5, edge_filter=flat)
    tk.lit_windows("tower_win", tower, [(z0 + 1.4, z1 - 0.3) for z0, z1 in rows], 4.1, 0.28, seed=4.0,
                   out=0.13, margin=0.1, gap=1.7, edge_filter=flat)
    # the crown: three deep dark openings cut into the top storeys of the long faces
    long_faces = lambda ei, p0, p1, n: tk.edges(tower)[ei][2] > 20.0  # noqa: E731
    tk.panes("crown_slots", tower, [(H_TOP - 8.5, H_TOP - 2.5)], 8.0, mat="ink", out=0.07, margin=0.0, gap=3.5,
             edge_filter=long_faces)
    tk.lit_windows("crown_slots", tower, [(H_TOP - 8.5, H_TOP - 2.5)], 8.0, 1.01, seed=1.0, out=0.13,
                   margin=0.6, gap=4.4, edge_filter=long_faces, mat="white_Glow")
    tk.prism("roof_deck", tk.offset_poly(tower, -0.5), H_TOP - 1.3, H_TOP - 0.9, "roofd")
    tk.ring_band("parapet", tk.offset_poly(tower, -0.5), H_TOP - 1.0, H_TOP, 0.5, "stone")
    tk.hvac_cluster("plant", *tk.rot2(TOWER_C, YAW), H_TOP - 0.9, YAW, 18.0, 14.0, seed=2.0, hmax=0.9, fans=False)
    # the 1910 bank: granite temple, columns on Sutter and Sansome, balustrade, glass roof
    bank = tk.ccw(tk.xform(BANK, YAW))
    tk.prism("bank", tk.offset_poly(bank, -1.5), 0.0, H_BANK - 4.0, "white")
    tk.arched_panes("bank_arches", tk.offset_poly(bank, -1.5), 1.0, 10.5, 6.0, 3.6, mat="glassd")
    tk.arched_panes("bank_lit", tk.offset_poly(bank, -1.5), 1.6, 9.0, 6.0, 2.6, mat="sand_Glow", out=0.12,
                    suffix="_glow")
    tk.pier_grid("bank_columns", tk.offset_poly(bank, -1.4), 1.2, 12.8, 4.6, 1.3, 1.3, "white", skip_short=8.0)
    tk.prism("bank_plinth", bank, 0.0, 1.2, "stone")
    tk.cornice("bank_entablature", tk.offset_poly(bank, -0.4), 12.8, h=2.2, out=0.6, mat="white")
    tk.ring_band("bank_balustrade", tk.offset_poly(bank, -0.3), H_BANK - 3.0, H_BANK, 0.3, "white")
    tk.prism("bank_roof", tk.offset_poly(bank, -0.4), H_BANK - 4.0, H_BANK - 2.8, "glassl")
    tk.glow_cap("bank_skylight", tk.offset_poly(bank, -3.0), H_BANK - 2.75, "sand_Glow")
    # low west wing
    wing = tk.ccw(tk.xform(WING, YAW))
    tk.punched_block("wing", wing, 0.0, H_WING, 4.2, wall="stone", win="copper", spacing=4.1, gap=1.5,
                     margin=1.0, lit=0.4, seed=6.0)
    tk.ring_band("wing_parapet", tk.offset_poly(wing, -0.4), H_WING, H_WING + 0.8, 0.4, "stone")
    tk.plinth("plaza", tk.xform(tk.rect(73.0, 42.1, 0.0, 0.0), YAW), h=0.25, out=2.5)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
