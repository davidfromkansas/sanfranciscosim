"""Deterministic Blender build of the SF-SIM miniature The Jay (ex Le Meridien).

    blender -b --python build_433_clay_street.py -- [--out DIR]

333 Battery Street / 433 Clay Street (1989; Le Meridien San Francisco until
2022, now The Jay, Autograph Collection, 360 rooms): a 25-storey grey
concrete hotel slab running along Clay Street. A flat-faced central service
spine rises highest; either side, the guest-room wings are folded into a
saw-tooth of pointed bays, every room with a balcony, and the wings step
down bay by bay toward their ends so the top reads as a terraced staircase.
Helpers in tools/landmark-kit/toykit.py.
"""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "433-clay-street"
CENTER = (-122.4008921, 37.7946919)   # OSM way 35182441, OBB centre
H_TOP = 81.0                           # OSM height 81 = LiDAR mode 81.0 m (DataSF 2010, parcel 0229020)
YAW = tk.bearing_to_yaw(80.8)          # local +x = bearing 80.8 (street grid, east), +y = 350.8

# OSM outline (13 nodes) in local metres: 84 x 30 m along Clay Street (north
# face); Battery Street is the east end.
SITE = [(-41.9, -15.0), (42.0, -14.8), (42.0, 12.7), (-36.9, 14.3), (-38.5, 15.2), (-42.0, 15.0)]
D = 19.0             # slab depth between the bay points' bases (estimated)
TOOTH = 1.9          # how far each pointed bay projects
BAY = 5.5            # bay width
CORE = 8.0           # half-width of the flat central spine
H_POD = 10.0         # podium (estimated)
STOREY = 3.0
STEPS = [78.0, 75.0, 72.0, 69.0]   # wing bays, centre outwards (photo: one storey per bay)


def L(poly):
    return tk.ccw(tk.xform(poly, YAW))


def bay_plan(x0, x1):
    xm = (x0 + x1) / 2
    h = D / 2
    return [(x0, -h), (xm, -h - TOOTH), (x1, -h), (x1, h), (xm, h + TOOTH), (x0, h)]


def angled(ei, p0, p1, nrm):
    return abs(tk.rot2(nrm, -YAW)[0]) > 0.15 and abs(tk.rot2(nrm, -YAW)[1]) > 0.5


def build():
    site = L(SITE)
    # podium with dark glass ground floor
    tk.prism("podium", site, 0.0, H_POD, "concrete", bev=0.15)
    tk.panes("pod_glass", site, [(0.3, 5.2)], 4.0, mat="glassd", gap=0.8, margin=0.2)
    tk.lit_windows("pod_lit", site, [(0.3, 5.0)], 4.0, 0.7, seed=1.0, out=0.1, margin=0.3, gap=1.0)
    tk.ring_band("pod_band", site, H_POD - 0.8, H_POD, 0.3, "steel")
    tk.prism("pod_roof", tk.offset_poly(site, -0.3), H_POD - 0.1, H_POD + 0.15, "roofd")
    # central flat spine, full height, with vertical reveal strips
    core = L([(-CORE, -D / 2 - 0.6), (CORE, -D / 2 - 0.6), (CORE, D / 2 + 0.6), (-CORE, D / 2 + 0.6)])
    tk.prism("core", core, H_POD, H_TOP - 1.2, "concrete", bev=0.15)
    for side in (-1, 1):
        for k, x in enumerate((-4.5, 0.0, 4.5)):
            c = tk.rot2((x, side * (D / 2 + 0.85)), YAW)
            tk.box(f"strip_{side}_{k}", c[0], c[1], H_POD, H_TOP - 1.2, 0.6, 0.5, "steel", yaw=YAW)
    tk.ring_band("core_parapet", tk.offset_poly(core, -0.3), H_TOP - 1.2, H_TOP, 0.3, "concrete")
    c = tk.rot2((0.0, 0.0), YAW)
    tk.hvac_cluster("plant", c[0], c[1], H_TOP - 1.3, YAW, 12.0, 14.0, seed=2.0, hmax=1.2, fans=False)
    # saw-tooth wings stepping down toward each end
    for side in (-1, 1):
        for i, top in enumerate(STEPS):
            xa = side * (CORE + i * BAY)
            xb = side * (CORE + (i + 1) * BAY)
            plan = L(bay_plan(min(xa, xb), max(xa, xb)))
            name = f"bay_{'e' if side > 0 else 'w'}{i}"
            tk.prism(name, plan, H_POD, top, "concrete", bev=0.1)
            bands = tk.floors(H_POD + 1.0, top - 0.6, STOREY)
            # balcony read: a dark glazed recess in the upper part of each storey
            tk.panes(name + "_glass", plan, [(z0 + 0.9, z1) for z0, z1 in bands], 2.8, mat="glassd",
                     gap=0.5, margin=0.0, edge_filter=angled)
            tk.lit_windows(name + "_lit", plan, [(z0 + 0.9, z1) for z0, z1 in bands], 2.8, 0.22,
                           seed=7.0 + i + side, out=0.1, margin=0.25, gap=0.7, edge_filter=angled)
            tk.prism(name + "_roof", tk.offset_poly(plan, -0.3), top - 0.25, top + 0.05, "roofd")
    tk.glow_ring("crown_light", core, H_TOP - 1.6, H_TOP - 1.25, 0.12, "white_Glow")
    tk.plinth("plaza", site, h=0.25, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
