"""Deterministic Blender build of the SF-SIM miniature Three Embarcadero Center.

    blender -b --python build_embarcadero_center_3.py -- [--out DIR]

Three Embarcadero Center (John Portman, 1977): a 31-storey slab of pale precast
concrete with a fine grain of dark vertical window slots, long faces north and
south. Like its siblings (Four Embarcadero Center is already a landmark) the
blunt slab breaks up at both short ends into vertical strips whose tops step
down and whose plans step back - "a blunt cliff from north or south, spiked
outcrops from east or west". It stands on the Embarcadero Center's concrete
shopping podium. The strips are measured off the OSM polygon. Helpers in
tools/landmark-kit/toykit.py; the stepped-strip outline helper lives here.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "embarcadero-center-3"
CENTER = (-122.3973532, 37.7951239)   # OSM way 32612538, OBB centre
H_TOP = 126.0                          # 126 m (published, Wikipedia); taken as the crest
FLOORS = 31
YAW = math.radians(90 - 81.4)          # local +x = bearing 81.4 (E), +y = 351.4 (N)
H_ROOF = H_TOP - 3.0                   # main roof deck; plant penthouse to the crest (estimated)
H_POD = 10.0                           # three-level shopping podium (estimated)

# OSM polygon in the local frame, as strips across the short ends: (y0, y1, x_extent)
WEST = [(7.8, 17.3, -39.1), (-3.7, 7.8, -36.5), (-17.3, -3.7, -39.5)]
EAST = [(-17.3, -10.6, 28.5), (-10.6, -1.1, 33.1), (-1.1, 14.0, 39.5), (14.0, 17.3, 31.1)]


def outline(keep_w, keep_e, xw, xe):
    """Staircase plan: core [xw, xe] plus the end strips whose index is kept."""
    pts = []
    for i, (y0, y1, x) in enumerate(EAST):                       # east side, south -> north
        xx = x if i in keep_e else xe
        pts += [(xx, y0), (xx, y1)]
    for i, (y0, y1, x) in enumerate(WEST):                       # west side, north -> south
        xx = x if i in keep_w else xw
        pts += [(xx, y1), (xx, y0)]
    out = []
    for p in pts:                                                # drop duplicates
        if not out or math.dist(p, out[-1]) > 1e-6:
            out.append(p)
    if math.dist(out[0], out[-1]) < 1e-6:
        out.pop()
    clean = []                                                   # drop collinear points
    n = len(out)
    for i in range(n):
        a, b, c = out[i - 1], out[i], out[(i + 1) % n]
        if abs((b[0] - a[0]) * (c[1] - b[1]) - (b[1] - a[1]) * (c[0] - b[0])) > 1e-6:
            clean.append(b)
    return tk.ccw(clean)


def tiers():
    """Strip tops step down away from each end's spine (its furthest strip): 0 / -5 / -10 storeys."""
    f = H_ROOF / FLOORS
    xw = max(x for _, _, x in WEST)
    xe = min(x for _, _, x in EAST)

    def ranks(strips, core, sign):
        ext = sorted({round(sign * (x - core), 3) for _, _, x in strips if abs(x - core) > 0.05}, reverse=True)
        return {i: min(2, ext.index(round(sign * (x - core), 3))) for i, (_, _, x) in enumerate(strips) if abs(x - core) > 0.05}
    rw, re = ranks(WEST, xw, -1), ranks(EAST, xe, 1)
    levels = [H_ROOF - 10 * f, H_ROOF - 5 * f, H_ROOF]
    out, z0 = [], H_POD
    for k, z1 in enumerate(levels):
        need = 2 - k                                            # rank 0 reaches the top, rank 2 only tier 0
        kw = {i for i, r in rw.items() if r <= need}
        ke = {i for i, r in re.items() if r <= need}
        out.append((z0, z1, outline(kw, ke, xw, xe)))
        z0 = z1
    return out


def build():
    f = H_ROOF / FLOORS
    full = tk.xform(outline(set(range(len(WEST))), set(range(len(EAST))), 0, 0), YAW)
    # concrete shopping podium with lit shopfronts and planted terrace edge
    pod = tk.offset_poly(full, 4.0)
    tk.prism("podium", pod, 0.0, H_POD, "concrete", bev=0.15)
    tk.panes("shops", pod, [(0.4, 3.8)], 6.0, mat="glassd", gap=1.4, margin=0.2)
    tk.lit_windows("shops_lit", pod, [(0.4, 3.8)], 6.0, 0.8, seed=1.0, out=0.1, margin=0.3, gap=1.6)
    tk.ring_band("podium_hedge", tk.offset_poly(pod, -0.8), H_POD, H_POD + 0.9, 0.7, "leafd")
    for k, (z0, z1, loc) in enumerate(tiers()):
        plan = tk.xform(loc, YAW)
        tk.prism(f"tier{k}", plan, z0, z1, "sand", bev=0.12)
        n = max(1, int(round((z1 - z0) / (5 * f))))
        groups = [(z0 + (z1 - z0) * i / n, z0 + (z1 - z0) * (i + 1) / n) for i in range(n)]
        tk.panes(f"tier{k}_slots", plan, groups, 1.55, mat="glass", gap=0.85, margin=0.45)
        rows = tk.floors(z0, z1, f)
        tk.lit_windows(f"tier{k}_lit", plan, rows, 3.1, 0.22, seed=5.0 + k, out=0.12, margin=0.6, gap=1.9)
        if k == 2:
            tk.ring_band(f"tier{k}_cap", plan, z1 - 0.9, z1, 0.15, "cream")
        tk.prism(f"tier{k}_deck", tk.offset_poly(plan, -0.4), z1, z1 + 0.15, "steel")
    # roof plant on the main deck
    tk.prism("penthouse", tk.xform(tk.rect(16.0, 10.0, -6.0, 0.0), YAW), H_ROOF + 0.15, H_TOP, "cream", bev=0.12)
    tk.hvac_cluster("roof_plant", *tk.rot2((14.0, 0.0), YAW), H_ROOF + 0.15, YAW, 18.0, 14.0, seed=8.0, hmax=2.6)
    top = tk.xform(tiers()[-1][2], YAW)
    tk.glow_ring("crown_light", top, H_ROOF - 0.8, H_ROOF - 0.15, 0.2, "glassl_Glow")
    tk.plinth("plaza", pod, h=0.25, out=2.0)


if __name__ == "__main__":
    tk.run(SLUG, build, HERE, CENTER, H_TOP)
