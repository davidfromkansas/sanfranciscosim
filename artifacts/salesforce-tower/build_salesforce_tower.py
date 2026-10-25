"""Deterministic Blender build of the SF-SIM miniature Salesforce Tower (v2).

    blender -b --python build_salesforce_tower.py -- [--out DIR]

v2 (2026-10-25, Transbay landmark batch) rebuilds the August asset to the
batch's standard. What changed and why is in REPORT.md; the short version:

* the shaft is PALE: silvery glass (`Toy_glassg`) crossed by white
  sunshade bands, which is how the tower reads from anywhere in the city.
  v1 used dark `Toy_glass` and read as a navy cylinder;
* the profile follows the photographs: a gentle taper to about two thirds of
  the height, then the shoulders roll inward to a BLUNT, open crown about 55%
  of the base width - v1 closed to an ogive point that the tower doesn't have;
* the crown is a perforated screen: a lattice of hoops and ribs continuing
  the shaft's curve, open at the top, with the "Day for Night" LED floors and
  the roof plant visible inside it from the app's downward camera;
* the base is the real ground condition: a tall glazed lobby behind white
  piers and the two entrance canopies on Mission and Fremont.

World space, metres, Z up, +X east, +Y north, origin at the base centre.
Shared helpers: tools/landmark-kit/toykit.py.
"""

import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(REPO, "tools", "landmark-kit"))
import toykit as tk  # noqa: E402

SLUG = "salesforce-tower"

H_ARCH = 326.0   # architectural top, rim of the crown screen
H_ROOF = 297.0   # occupied roof (top of the LED floors)
H_LED = 272.0    # the six "Day for Night" floors sit below the roof
H_SHOULDER = 215.0  # where the taper turns into the rounded top
H_LOBBY = 15.0
A_BASE = 27.2    # half-width across the flats at grade (OSM: 54.5 x 54.1 m)
A_SHOULDER = 24.6
A_TOP = 15.2     # half-width at the crown rim: ~56% of the base
YAW = math.radians(44.6)  # flats run 45 / 135 degrees (OSM way 431972186)

PITCH = 8.3      # one modelled sunshade band per two real floors
BAND_H = 1.15
BAND_OUT = 0.55
SEG_FLAT = 3
SEG_ARC = 5


def half_width(z):
    if z <= H_SHOULDER:
        t = z / H_SHOULDER
        return A_BASE + (A_SHOULDER - A_BASE) * t ** 1.15
    # roll the shoulders in along a quarter-ellipse to the blunt crown
    t = min((z - H_SHOULDER) / (H_ARCH - H_SHOULDER), 1.0)
    return A_TOP + (A_SHOULDER - A_TOP) * math.sqrt(max(0.0, 1.0 - t ** 2.3))


def corner_frac(z):
    t = min(max(z / H_ARCH, 0.0), 1.0)
    return 0.30 + 0.38 * t ** 1.4


def outline(z, off=0.0):
    a = half_width(z) + off
    r = min(corner_frac(z) * half_width(z), a - 0.2)
    s = a - r
    pts = []
    for q in range(4):
        base = q * math.pi / 2
        for i in range(SEG_FLAT):
            u = -s + 2 * s * i / SEG_FLAT
            pts.append(tk.rot2((a, u), base))
        for i in range(SEG_ARC):
            ang = (math.pi / 2) * i / SEG_ARC
            pts.append(tk.rot2((s + r * math.cos(ang), s + r * math.sin(ang)), base))
    return [tk.rot2(p, YAW) for p in pts]


def face_point(z, off, face_deg, along=0.0):
    """A point on a flat face; face_deg is the compass bearing of its normal."""
    a = half_width(z) + off
    ang = math.radians(90 - face_deg)
    nx, ny = math.cos(ang), math.sin(ang)
    return (nx * a - ny * along, ny * a + nx * along), (nx, ny), ang


def door_edge(px, py, nx, ny, w, out):
    tx, ty = -ny, nx
    cx, cy = px + nx * out, py + ny * out
    return (cx - tx * w / 2, cy - ty * w / 2), (cx + tx * w / 2, cy + ty * w / 2)


def build():
    # --- shaft: pale glass + white sunshade bands (one loft) -------------
    tk.banded_loft("shaft", outline, H_LOBBY, H_ROOF, PITCH, BAND_H, BAND_OUT,
                   tk.material("glassg"), tk.material("white"), glass_in=-0.25)
    office = []
    z = H_LOBBY
    while z + PITCH <= H_LED:
        office.append((z + BAND_H, z + PITCH))
        z += PITCH
    tk.lit_loop_windows("win_office", outline, office, density=0.28, seed=3.7, out=-0.17,
                        margin=0.9, subdiv=2, gap=0.08)
    led = []
    z = H_LED
    while z < H_ROOF - 1:
        led.append((z, min(z + PITCH / 2, H_ROOF)))
        z += PITCH / 2
    # "Day for Night": the LED floors glow solid and cool, so the crown ignites
    tk.lit_loop_windows("win_led", outline, led, density=1.0, seed=1.0, out=-0.17,
                        margin=0.35, mat="white_Glow")

    # --- crown: perforated screen continuing the curve, open at the top --
    crown_z = [H_ROOF + i * (H_ARCH - H_ROOF) / 10 for i in range(11)]
    for i, zc in enumerate(crown_z):
        zt = zc + 1.0 if i < len(crown_z) - 1 else H_ARCH
        z0 = zc if i < len(crown_z) - 1 else H_ARCH - 1.6
        zt = z0 + 0.75 if i < len(crown_z) - 1 else H_ARCH
        tk.loft(f"crown_hoop_{i}", [(z0, outline(z0, -0.6)), (z0, outline(z0, 0.35)),
                                    (zt, outline(zt, 0.35)), (zt, outline(zt, -0.6)),
                                    (z0, outline(z0, -0.6))], "white")
    # vertical ribs between the hoops: the screen's perforation, abstracted
    n = len(outline(0))
    rz = [H_ROOF + (H_ARCH - H_ROOF) * k / 6 for k in range(7)]
    for i in range(0, n):
        rings = []
        for zr in rz:
            lo, hi = outline(zr, -0.55), outline(zr, 0.3)
            p_lo, p_hi = lo[i], hi[i]
            tx, ty = hi[(i + 1) % n][0] - hi[i - 1][0], hi[(i + 1) % n][1] - hi[i - 1][1]
            m = math.hypot(tx, ty) or 1
            tx, ty = tx / m * 0.3, ty / m * 0.3
            rings.append((zr, [(p_lo[0] - tx, p_lo[1] - ty), (p_hi[0] - tx, p_hi[1] - ty),
                               (p_hi[0] + tx, p_hi[1] + ty), (p_lo[0] + tx, p_lo[1] + ty)]))
        tk.loft(f"crown_rib_{i}", rings, "white", cap_top=True, cap_bottom=True)
    # the crown's light: a cool inner skin behind the lattice
    tk.loft("crown_light_glow", [(H_ROOF + 1.0, outline(H_ROOF + 1.0, -0.75)),
                                 (H_ARCH - 3.0, outline(H_ARCH - 3.0, -0.75))], "white_Glow")
    # roof deck inside the crown, seen from above: plant, BMU track, a garden
    deck = outline(H_ROOF, -0.8)
    tk.prism("roof_deck", deck, H_ROOF - 0.5, H_ROOF, "roofd")
    yaw = YAW
    tk.hvac_cluster("plant_a", *tk.rot2((-5.0, 4.0), yaw), H_ROOF, yaw, 14, 9, seed=2.0)
    tk.hvac_cluster("plant_b", *tk.rot2((6.5, -4.5), yaw), H_ROOF, yaw, 9, 7, seed=5.0)
    tk.ring_band("bmu_rail", tk.offset_poly(outline(H_ROOF), -5.0), H_ROOF, H_ROOF + 0.5, 0.8, "steel")
    bx, by = tk.rot2((9.0, 8.0), yaw)
    tk.box("bmu", bx, by, H_ROOF + 0.5, H_ROOF + 3.2, 7.0, 2.4, "steel", yaw=yaw, bev=0.15)
    tk.box("bmu_arm", *tk.rot2((9.0, 4.5), yaw), H_ROOF + 2.6, H_ROOF + 3.4, 1.0, 9.0, "steel", yaw=yaw)
    for i in range(4):
        tk.antenna(f"mast_{i}", *tk.rot2(((-1) ** i * 2.2, (1 if i < 2 else -1) * 2.2), yaw), H_ROOF + 4.0, 5.0)
    # plant platform on which the masts stand
    tk.box("mast_base", 0, 0, H_ROOF, H_ROOF + 4.0, 7.0, 7.0, "steel", yaw=yaw, bev=0.2)

    # --- lobby: tall recessed glass box behind white piers ---------------
    lobby = outline(0.0, -2.2)
    tk.prism("lobby_glass", lobby, 0.0, H_LOBBY, "glassl", bottom=True)
    tk.glow_ring("lobby_lit", outline(0.0, -2.2), 1.2, H_LOBBY - 1.0, 0.06, "sand_Glow")
    tk.ring_band("lobby_head", outline(H_LOBBY - 1.8), H_LOBBY - 1.8, H_LOBBY, BAND_OUT, "white", inset=-2.4)
    for i in range(0, n, 2):
        lo = outline(0.0, -0.4)
        p = lo[i]
        q = lo[(i + 1) % n]
        ang = math.atan2(q[1] - p[1], q[0] - p[0])
        tk.box(f"pier_{i}", p[0], p[1], 0.0, H_LOBBY - 1.8, 1.4, 1.4, "white", yaw=ang, bev=0.2)

    # --- entrances: canopies on Mission (NW face) and Fremont (NE face) --
    for name, face, w in (("mission", 315.0, 24.0), ("fremont", 45.0, 16.0)):
        (px, py), (nx, ny), ang = face_point(0.0, 0.0, face)
        cx, cy = px + nx * 3.0, py + ny * 3.0
        tk.box(f"canopy_{name}", cx, cy, 8.0, 9.0, 8.0, w, "white", yaw=ang, bev=0.25)
        tk.box(f"door_{name}", px + nx * 0.2, py + ny * 0.2, 0.0, 7.6, 1.2, w * 0.55, "glass", yaw=ang)
        tk.flat_quad(f"door_{name}_glow", *door_edge(px, py, nx, ny, w * 0.55, 1.0), 0.6, 7.0, 0.0,
                     "sand_Glow", (nx, ny))
    # the blue cloud by the Mission doors, semantically enlarged (style s.8)
    (px, py), (nx, ny), ang = face_point(0.0, 0.0, 315.0, along=-16.0)
    for k, (dx, w, h) in enumerate(((-1.8, 2.6, 2.0), (0.3, 3.6, 2.8), (2.4, 2.2, 1.6))):
        tx, ty = -ny, nx
        tk.box(f"sign_cloud_{k}", px + nx * 2.5 + tx * dx, py + ny * 2.5 + ty * dx, 0.4, 0.4 + h,
               1.0, w, "sky", yaw=ang, bev=0.4)

    # --- plaza apron: the Mission St frontage + a few street trees -------
    tk.plinth("plaza", outline(0.0), h=0.3, out=4.5, mat="stone")
    for name, face in (("mission", 315.0), ("fremont", 45.0)):
        (px, py), (nx, ny), ang = face_point(0.0, 3.2, face)
        tx, ty = -ny, nx
        tk.tree_row(f"trees_{name}", (px - tx * 24, py - ty * 24), (px - tx * 10, py - ty * 10), 0.3, 2,
                    h=7.0, r=2.4, seed=4.0 if name == "mission" else 9.0)



def main():
    # tk.run resets, builds, recalcs normals, merges by material, recentres,
    # normalizes the crest to H_ARCH and exports <slug>.glb/.blend
    tk.run(SLUG, build, HERE, (-122.396930, 37.789775), H_ARCH)


if __name__ == "__main__":
    main()
