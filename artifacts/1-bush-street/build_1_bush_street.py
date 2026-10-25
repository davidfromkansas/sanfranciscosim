"""Deterministic Blender build of the SF-SIM miniature Crown Zellerbach Building (One Bush Plaza).

    blender -b --python build_1_bush_street.py -- [--out DIR]

1 Bush Street (Skidmore, Owings & Merrill with Hertzka & Knowles, 1959): San
Francisco's first International Style tower, a 20-storey slab of green-tinted glass
held by a dense grid of slender aluminium mullions, lifted on dark granite columns
over a recessed glass lobby, with its elevator and service core pulled out into a
separate, solid tower on the south side. Recognition cues: the pure green glass slab
on stilts and the solid core tower beside it. Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "1-bush-street"
CENTER = (-122.4000448, 37.7909383)  # OSM way 93817367, OBB centre
H_TOP = 93.9                          # published roof 308 ft (Wikipedia) = core-tower crest; LiDAR max 93.78
H_SLAB = 86.7                         # slab roof: DataSF LiDAR majority plane 86.68 m (measured)
H_LOBBY = 7.6
YAW = math.radians(90 - 80.8)
# OSM way 93817367 in metres about CENTER (+x east, +y north)
PTS = [(-34.51, 13.92), (-30.94, -7.83), (-15.87, -5.4), (-12.14, -4.79), (-10.91, -12.27), (-13.69, -12.72),
       (-12.25, -21.5), (11.08, -17.72), (9.53, -8.31), (6.51, -8.8), (5.35, -1.74), (10.81, -0.86),
       (31.84, 2.54), (28.3, 24.1)]
SLAB = [PTS[0], PTS[1], PTS[12], PTS[13]]
CORE = PTS[3:11]


def build():
    slab = tk.ccw(SLAB)
    core = tk.ccw(CORE)
    # stilts: dark granite columns round a recessed glass lobby
    lobby = tk.offset_poly(slab, -3.0)
    tk.prism("lobby", lobby, 0.0, H_LOBBY, "glassd")
    tk.glow_ring("lobby_lit", lobby, 0.6, H_LOBBY - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("stilts", tk.offset_poly(slab, -1.6), 0.0, H_LOBBY, 6.9, 1.3, 1.3, "ink", min_count=3)
    tk.prism("soffit", slab, H_LOBBY - 0.6, H_LOBBY + 0.4, "ink")
    # the slab: green glass, thin dark spandrel lines and a dense mullion grid; 19 storeys
    pitch = (H_SLAB - 1.2 - H_LOBBY - 0.4) / 19
    tk.shaft("slab", slab, H_LOBBY + 0.4, H_SLAB - 1.2, pitch, glass="teal", band="glassd", band_h=0.7,
             band_out=0.12, fins=(2.1, 0.2, 0.3, "steel"), lit=0.28, seed=4.0, lit_spacing=2.1)
    tk.ring_band("slab_top", tk.offset_poly(slab, -0.2), H_SLAB - 1.2, H_SLAB, 0.42, "glassd")
    tk.prism("slab_roof", tk.offset_poly(slab, -0.3), H_SLAB - 0.5, H_SLAB - 0.1, "roofd")
    c = tk.rot2((14.0, 8.0), YAW)
    tk.hvac_cluster("slab_plant", c[0], c[1], H_SLAB - 0.1, YAW, 18.0, 10.0, seed=3.0, hmax=3.0)
    # the solid service core: mosaic-clad tower with slit windows, rising over the slab
    tk.prism("core", core, 0.0, H_TOP - 0.6, "verdigris", bev=0.15)
    tk.panes("core_slits", core, tk.floors(H_LOBBY, H_SLAB, 4.0), 6.0, mat="glassd", gap=4.6, margin=1.0,
             edge_filter=lambda ei, p0, p1, n: math.dist(p0, p1) > 10.0)
    tk.ring_band("core_cap", core, H_TOP - 0.6, H_TOP, 0.2, "steel")
    tk.prism("core_roof", tk.offset_poly(core, -0.3), H_TOP - 0.9, H_TOP - 0.55, "roofd")
    tk.glow_ring("core_light", core, H_TOP - 2.6, H_TOP - 1.6, 0.06, "white_Glow")
    # granite plaza wall and street trees along Market (the low pavilion is a separate building)
    tk.plinth("plaza", slab, h=0.3, out=4.0, mat="granite")
    p0, p1 = tk.xform([(-26.0, -18.0), (-16.0, -24.0)], 0.0)
    tk.tree_row("trees", p0, p1, 0.3, 2, h=6.0, seed=1.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
