"""Deterministic Blender build of the SF-SIM miniature 650 California Street.

    blender -b --python build_650_california_street.py -- [--out DIR]

650 California Street, the Hartford Building (SOM / Edward Charles Bassett,
1964): a 34-storey square modernist tower, briefly the tallest in California.
Recognition cues: a plain square prism wrapped in a white precast-concrete
square grid with dark windows recessed deep inside it, a tall glazed lobby
behind white columns, and a flat top whose last storey has taller openings.
Helpers in tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "650-california-street"
CENTER = (-122.4052193, 37.7928669)   # OSM way 260520160, OBB centre
H_TOP = 142.0                          # published roof 142 m / 466 ft; DataSF LiDAR roof median 142.8 m
H_LOBBY = 9.0
H_SHAFT = 134.0                        # 31 office storeys of ~4.03 m above the lobby
H_PARAPET = 140.4
YAW = math.radians(8.9)                # local +x runs along California St (OSM edge bearing 98.9)
PTS = [(16.04, 22.19), (22.11, -16.2), (-15.98, -22.19), (-22.11, 16.2)]
BAY = 3.2                              # 12 bays per 38.7 m face, as in the photo
GLASS_IN = -0.35


def build():
    plan = tk.ccw(PTS)
    # lobby: tall glazing set back behind white columns on every other grid line
    lob = tk.offset_poly(plan, -3.0)
    tk.prism("lobby_glass", lob, 0.0, H_LOBBY, "glassl")
    tk.glow_ring("lobby_lit", lob, 0.6, H_LOBBY - 1.2, 0.06, "sand_Glow")
    tk.pier_grid("lobby_columns", tk.offset_poly(plan, -0.6), 0.0, H_LOBBY, BAY * 2, 0.9, 0.9, "white")
    tk.prism("lobby_soffit", plan, H_LOBBY - 0.8, H_LOBBY, "white")
    # shaft: dark glass recessed behind white horizontal and vertical precast members (one grid)
    pitch = (H_SHAFT - H_LOBBY) / 31
    tk.shaft("shaft", plan, H_LOBBY, H_SHAFT, pitch, glass="glassd", band="white", band_h=1.3,
             band_out=0.3, fins=None, lit=0.0, glass_in=GLASS_IN)
    # top storey: taller openings under a deep white parapet
    tk.shaft("top", plan, H_SHAFT, H_PARAPET, H_PARAPET - H_SHAFT, glass="glassd", band="white",
             band_h=1.3, band_out=0.3, fins=None, lit=0.0, glass_in=GLASS_IN)
    tk.ring_band("parapet", tk.offset_poly(plan, GLASS_IN), H_PARAPET, H_TOP, 0.65, "white")
    tk.pier_grid("grid_piers", tk.offset_poly(plan, GLASS_IN), H_LOBBY, H_PARAPET, BAY, 0.75, 0.65, "white",
                 skip_short=3.0)
    bands = [(H_LOBBY + i * pitch + 1.3, H_LOBBY + (i + 1) * pitch) for i in range(31)]
    tk.lit_windows("shaft_win", tk.offset_poly(plan, GLASS_IN), bands, BAY, 0.3, seed=6.5, out=0.72,
                   margin=0.35, gap=1.0)
    tk.lit_windows("top_win", tk.offset_poly(plan, GLASS_IN), [(H_SHAFT + 1.3, H_PARAPET)], BAY, 0.5,
                   seed=2.2, out=0.72, margin=0.4, gap=1.0)
    # roof: deck raised clear of the glass cap, low plant behind the parapet
    tk.prism("roof_deck", tk.offset_poly(plan, -0.8), H_PARAPET - 0.2, H_PARAPET + 0.1, "roofd")
    tk.hvac_cluster("roof_plant", 0.0, 0.0, H_PARAPET + 0.1, YAW, 20.0, 16.0, seed=5.0, hmax=1.4, fans=False)
    tk.plinth("plaza", plan, h=0.3, out=3.0)
    # street trees along California St (south face)
    hx = 19.3
    p0, p1 = tk.xform([(-hx + 4, -hx - 2.2), (hx - 4, -hx - 2.2)], YAW)
    tk.tree_row("trees", p0, p1, 0.3, 3, h=6.0, seed=4.1)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
