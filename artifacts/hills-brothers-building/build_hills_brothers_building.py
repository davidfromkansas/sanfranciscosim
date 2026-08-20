"""Deterministic Blender build of the SF-SIM miniature Hills Brothers Building.

    blender -b --python build_hills_brothers_building.py -- [--out DIR]

Writes hills-brothers-building.blend and hills-brothers-building.glb next to
this file (or into --out). Geometry is authored in the building's own grid —
u along the 75.4 m Embarcadero facade toward the north-east, v inland toward
the plaza — then rotated +45 deg about Z so the model lands at its true
heading (the SoMa waterfront grid runs 45 deg off north here; the map
building-frame -> world is a pure rotation, chosen so no winding flips — see
sf3d-building-axis-winding). After rotation the whole model is recentred so
its world-axis bbox centre sits at the origin, matching the manifest anchor
convention (bbox centre, -122.3892854 37.7894167).

Design (see REFERENCE.md for the sources behind every number):

* the OSM relation/2280956 footprint idealized to its 75.5 x 44.2 m rectangle
  with the 15.8 m lightwell offset toward the plaza side, and the campanile
  projecting 12.7 m from the north-west wall (vertex table in the plan's 2.3);
* Kelham's Romanesque grammar: two-storey brick base with tall segmental-
  arched openings, four floors of recessed sash pads, an arcaded sixth floor
  under a corbel band, tall parapet with a light cap;
* the campanile: smooth shaft with paired slit recesses, arcaded top stage,
  corbel cornice, low parapet, terracotta pyramid, finial — crest exactly
  53.2 m (DataSF LiDAR hgt_max; the flagpole above it is omitted, plan 2.15);
* the 1985 penthouse floor as cream volumes with hipped terracotta roofs
  ringing the lightwell (the aerial identity), the NE wing kept as the pale
  mechanical roof the satellite shows;
* the rooftop neon sign as a steel lattice carrying chunky red letter blocks
  reading HILLS BROS COFFEE toward the bay — the hero night glow.

Night state: sign letters glow red, the tower arcade glows warm white (both
lit in the Commons night photo). Glow faces are thin plates proud of opaque
geometry, never primary surfaces (sf3d-glow-face-needs-own-plate).
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Matrix, Vector

# ---------------------------------------------------------------- parameters

# Idealized footprint in building frame (u north-east along the Embarcadero
# facade, v north-west toward the plaza). Max deviation from the measured OSM
# ring is 0.5 m (documented in REPORT.md).
U0, U1 = -38.0, 37.4          # SW (Harrison) / NE (Folsom) walls
V0, V1 = -22.0, 22.2          # SE (Embarcadero) / NW (plaza) walls
WELL = (-11.5, 4.3, -1.5, 14.2)   # lightwell u0,u1,v0,v1 (measured)
TWR = (-11.1, 4.3, 19.2, 34.9)    # tower u0,u1,v0,v1 — embedded 3 m into the wing

Z_DECK = 23.9      # main roof deck (LiDAR mode 23.88)
Z_CORBEL = 23.0    # corbel band under the parapet
Z_PARAPET = 25.6   # parapet crest (deck + HPC pedestal/parapet arithmetic)
Z_BASE = 6.8       # top of the two-storey arched base
Z_ARCADE0 = 20.3   # sixth-floor arcade sill band
FLOOR_ROWS = 4     # sash rows between base and arcade

Z_PH_WALL = 28.1   # 1985 penthouse walls
Z_PH_CREST = 29.2  # penthouse hip crest (estimated, LiDAR shoulder)

Z_TWR_SHAFT = 40.2   # top of the smooth tower shaft
Z_TWR_ARC = 47.8     # top of the arcade stage
Z_TWR_CORBEL = 48.6  # corbel cornice
Z_TWR_PARAPET = 49.0
Z_TWR_APEX = 52.9    # pyramid apex
Z_CREST = 53.2       # finial tip = bbox top = targetHeightM

BAY = 5.8            # facade bay module

PALETTE_HEX = {
    "Toy_brick": "c96f4a",
    "Toy_rust": "a86444",
    "Toy_trim": "f3efe6",
    "Toy_cream": "f2ede3",
    "Toy_glass": "2a4d73",
    "Toy_ink": "3a3530",
    "Toy_stone": "d9d2c2",
    "Toy_roofd": "45454a",
    "Toy_steel": "9aa0a6",
    "Toy_red": "c4453c",
    "Toy_red_Glow": "c4453c",
    "Toy_white_Glow": "f7f4ec",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# -------------------------------------------------------------- mesh helpers


def new_mesh(name, verts, faces, materials, face_mats=None):
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in materials:
        mesh.materials.append(m)
    if face_mats:
        for poly, mi in zip(mesh.polygons, face_mats):
            poly.material_index = mi
    mesh.validate()
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def bevel(obj, width=0.12, segments=2):
    """Miniature-style edge softening, capped by the thinnest dimension so
    applied panels never collapse (clamp + degenerate sweep)."""
    thin = min((d for d in obj.dimensions if d > 1e-6), default=width)
    offset = min(width, thin * 0.30)
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=offset,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-4)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-4, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def box(name, u0, u1, v0, v1, z0, z1, mat, mat_top=None):
    verts = [
        (u0, v0, z0), (u1, v0, z0), (u1, v1, z0), (u0, v1, z0),
        (u0, v0, z1), (u1, v0, z1), (u1, v1, z1), (u0, v1, z1),
    ]
    faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    mats = [mat] if mat_top is None else [mat, mat_top]
    face_mats = [0, 1 if mat_top else 0, 0, 0, 0, 0]
    return new_mesh(name, verts, faces, mats, face_mats)


def hip_roof(name, u0, u1, v0, v1, ze, zr, mat, ridge_axis="u", overhang=0.35):
    """Closed hip-roof solid: eave rectangle (with overhang) at ze, ridge line
    along the long axis at zr, hip ends. 6 verts, 5 faces + base."""
    u0, u1, v0, v1 = u0 - overhang, u1 + overhang, v0 - overhang, v1 + overhang
    if ridge_axis == "u":
        inset = min((v1 - v0) / 2.0, (u1 - u0) / 2.0 * 0.9)
        r0 = (u0 + inset, (v0 + v1) / 2.0, zr)
        r1 = (u1 - inset, (v0 + v1) / 2.0, zr)
    else:
        inset = min((u1 - u0) / 2.0, (v1 - v0) / 2.0 * 0.9)
        r0 = ((u0 + u1) / 2.0, v0 + inset, zr)
        r1 = ((u0 + u1) / 2.0, v1 - inset, zr)
    verts = [(u0, v0, ze), (u1, v0, ze), (u1, v1, ze), (u0, v1, ze), r0, r1]
    if ridge_axis == "u":
        faces = [(0, 1, 5, 4), (2, 3, 4, 5), (1, 2, 5), (3, 0, 4), (3, 2, 1, 0)]
    else:
        faces = [(0, 1, 4), (1, 2, 5, 4), (2, 3, 5), (3, 0, 4, 5), (3, 2, 1, 0)]
    return new_mesh(name, verts, faces, [mat])


def pyramid(name, u0, u1, v0, v1, ze, za, mat):
    cu, cv = (u0 + u1) / 2.0, (v0 + v1) / 2.0
    verts = [(u0, v0, ze), (u1, v0, ze), (u1, v1, ze), (u0, v1, ze), (cu, cv, za)]
    faces = [(0, 1, 4), (1, 2, 4), (2, 3, 4), (3, 0, 4), (3, 2, 1, 0)]
    return new_mesh(name, verts, faces, [mat])


# Facade helpers. A facade is described by (axis, coord, sign): axis "v" means
# the wall is a v=coord plane extending in u, outward normal sign*v; axis "u"
# the reverse. Panels are closed prisms of a (t, z) profile in the wall plane,
# extruded from depth d0 to d1 along the outward normal.


def facade_point(f, t, d, z):
    axis, coord, sign = f
    if axis == "v":
        return (t, coord + sign * d, z)
    return (coord + sign * d, t, z)


def face_panel(name, f, t_centre, profile, d0, d1, mat):
    verts = []
    # Wall-plane handedness: for +normal facades the profile's t axis must run
    # one way, for -normal the other, so prisms keep outward windings; the
    # recalc in new_mesh fixes any residue, but start correct.
    for d in (d0, d1):
        for dt, z in profile:
            verts.append(facade_point(f, t_centre + dt, d, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


def arch_profile(w, z0, z_spring, rise, seg=6):
    a = w / 2.0
    pts = [(-a, z0), (a, z0), (a, z_spring)]
    radius = (a * a + rise * rise) / (2.0 * rise)
    cz = z_spring + rise - radius
    th0 = math.atan2(z_spring - cz, a)
    th1 = math.pi - th0
    for k in range(1, seg):
        th = th0 + (th1 - th0) * k / seg
        pts.append((radius * math.cos(th), cz + radius * math.sin(th)))
    pts.append((-a, z_spring))
    return pts


def material(name):
    mat = bpy.data.materials.get(name)
    if mat:
        return mat
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    rgb = PALETTE[name]
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- build


def bays_on(t0, t1, margin=2.4):
    """Bay centres between t0..t1 with corner margins, on the BAY module."""
    span = (t1 - margin) - (t0 + margin)
    n = max(2, round(span / BAY))
    return [(t0 + margin) + span * (i + 0.5) / n for i in range(n)], span / n


def facade_windows(tag, f, t0, t1, mats, skip=lambda t: False):
    """Base arches, four sash rows, arcade row for one facade."""
    brick, glass, ink, trim = mats
    centres, step = bays_on(t0, t1)
    w_pad = min(3.3, step - 1.6)
    # base: tall segmental-arched openings, every other bay (freight rhythm)
    for i, t in enumerate(centres):
        if skip(t):
            continue
        face_panel(f"{tag}_arch{i}", f, t, arch_profile(w_pad, 0.5, 4.6, 1.1), 0.0, 0.08, ink)
        face_panel(f"{tag}_archg{i}", f, t, arch_profile(w_pad - 0.7, 1.0, 4.4, 0.9), 0.0, 0.14, glass)
    # four sash rows
    row_h = (Z_ARCADE0 - 0.8 - Z_BASE) / FLOOR_ROWS
    for r in range(FLOOR_ROWS):
        z0 = Z_BASE + 0.7 + r * row_h
        z1 = z0 + row_h - 1.15
        for i, t in enumerate(centres):
            if skip(t):
                continue
            face_panel(f"{tag}_wf{r}_{i}", f, t, rect_profile(w_pad, z0, z1), 0.0, 0.07, ink)
            face_panel(f"{tag}_wg{r}_{i}", f, t, rect_profile(w_pad - 0.55, z0 + 0.22, z1 - 0.22), 0.0, 0.13, glass)
    # sixth-floor arcade
    for i, t in enumerate(centres):
        if skip(t):
            continue
        face_panel(
            f"{tag}_arc{i}", f, t, arch_profile(w_pad - 0.5, Z_ARCADE0, Z_CORBEL - 1.6, 0.9),
            0.0, 0.12, glass,
        )
    # sill band at the arcade floor
    face_panel(
        f"{tag}_sill", f, (t0 + t1) / 2.0, rect_profile((t1 - t0) - 1.4, Z_ARCADE0 - 0.45, Z_ARCADE0 - 0.1),
        0.0, 0.14, trim,
    )


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)

    brick = material("Toy_brick")
    rust = material("Toy_rust")
    trim = material("Toy_trim")
    cream = material("Toy_cream")
    glass = material("Toy_glass")
    ink = material("Toy_ink")
    stone = material("Toy_stone")
    roofd = material("Toy_roofd")
    steel = material("Toy_steel")
    red = material("Toy_red")
    rglow = material("Toy_red_Glow")
    wglow = material("Toy_white_Glow")

    wu0, wu1, wv0, wv1 = WELL

    # --- body: four interpenetrating wing prisms leave the lightwell open ---
    # (union of solids; slight overlaps, never coincident faces)
    box("wing_se", U0, U1, V0, wv0, 0.0, Z_DECK, brick, mat_top=roofd)
    box("wing_nw", U0, U1, wv1, V1, 0.0, Z_DECK, brick, mat_top=roofd)
    box("wing_sw", U0, wu0 + 0.05, wv0 - 0.05, wv1 + 0.05, 0.0, Z_DECK, brick, mat_top=roofd)
    box("wing_ne", wu1 - 0.05, U1, wv0 - 0.05, wv1 + 0.05, 0.0, Z_DECK, brick, mat_top=roofd)
    # lightwell floor (a lower roof; the well reads as a real void from above)
    box("well_floor", wu0 + 0.02, wu1 - 0.02, wv0 + 0.02, wv1 - 0.02, 4.6, 5.1, brick, mat_top=roofd)

    # --- parapet: outer ring + light cap, low curb around the well ----------
    t = 0.55
    for name, (a0, a1, b0, b1) in {
        "par_se": (U0 - 0.1, U1 + 0.1, V0, V0 + t),
        "par_nw": (U0 - 0.1, U1 + 0.1, V1 - t, V1),
        "par_sw": (U0, U0 + t, V0, V1),
        "par_ne": (U1 - t, U1, V0, V1),
    }.items():
        box(name, a0, a1, b0, b1, Z_DECK - 0.2, Z_PARAPET, brick)
        box(name + "_cap", a0 - 0.08, a1 + 0.08, b0 - 0.08, b1 + 0.08, Z_PARAPET - 0.35, Z_PARAPET, trim)
    for name, (a0, a1, b0, b1) in {
        "curb_se": (wu0 - 0.4, wu1 + 0.4, wv0 - 0.4, wv0),
        "curb_nw": (wu0 - 0.4, wu1 + 0.4, wv1, wv1 + 0.4),
        "curb_sw": (wu0 - 0.4, wu0, wv0, wv1),
        "curb_ne": (wu1, wu1 + 0.4, wv0, wv1),
    }.items():
        box(name, a0, a1, b0, b1, Z_DECK - 0.1, Z_DECK + 0.6, brick)

    # --- corbel band under the parapet, all four facades --------------------
    F_SE = ("v", V0, -1)
    F_NE = ("u", U1, 1)
    F_SW = ("u", U0, -1)
    F_NW = ("v", V1, 1)
    for tag, f, t0, t1 in (
        ("se", F_SE, U0, U1), ("ne", F_NE, V0, V1), ("sw", F_SW, V0, V1), ("nw", F_NW, U0, U1),
    ):
        face_panel(
            f"corbel_{tag}", f, (t0 + t1) / 2.0, rect_profile((t1 - t0) - 0.3, Z_CORBEL, Z_CORBEL + 0.55),
            0.0, 0.22, trim,
        )
        face_panel(
            f"base_band_{tag}", f, (t0 + t1) / 2.0, rect_profile((t1 - t0) - 0.3, Z_BASE - 0.35, Z_BASE),
            0.0, 0.16, stone,
        )

    # --- facades ------------------------------------------------------------
    mats = (brick, glass, ink, trim)
    tower_span = lambda tv: TWR[0] - 1.0 < tv < TWR[1] + 1.0
    facade_windows("se", F_SE, U0, U1, mats)
    facade_windows("ne", F_NE, V0, V1, mats)
    facade_windows("sw", F_SW, V0, V1, mats)
    facade_windows("nw", F_NW, U0, U1, mats, skip=tower_span)

    # entrance: one grander arch on Harrison near the Embarcadero corner
    face_panel("entry_frame", F_SW, V0 + 8.0, arch_profile(4.6, 0.0, 5.4, 1.3), -0.05, 0.35, stone)
    face_panel("entry_fill", F_SW, V0 + 8.0, arch_profile(3.6, 0.0, 5.2, 1.1), 0.0, 0.12, ink)

    # --- lightwell inner window pads (visible from the aerial camera) -------
    IW_SE = ("v", wv0, 1)   # inner face of the SE wing looks north-west into the well
    IW_NW = ("v", wv1, -1)
    for tag, f in (("iwse", IW_SE), ("iwnw", IW_NW)):
        for r in range(3):
            z0 = 8.0 + r * 4.6
            face_panel(
                f"{tag}_w{r}", f, (wu0 + wu1) / 2.0, rect_profile(wu1 - wu0 - 4.0, z0, z0 + 2.6),
                0.0, 0.10, glass,
            )

    # --- penthouse (1985): cream volumes + terracotta hips ring the well ----
    # NE wing stays the pale mechanical roof the satellite shows.
    ph = [
        ("ph_se", -26.0, 19.0, -13.5, wv0 + 0.6, "u"),
        ("ph_sw", U0 + 3.0, wu0 + 0.6, -8.0, 17.0, "v"),
        ("ph_nw", -26.0, 19.0, wv1 - 0.6, V1 - 1.2, "u"),
    ]
    for name, a0, a1, b0, b1, axis in ph:
        box(name, a0, a1, b0, b1, Z_DECK, Z_PH_WALL, cream)
        hip_roof(name + "_roof", a0, a1, b0, b1, Z_PH_WALL, Z_PH_CREST, rust, ridge_axis=axis, overhang=0.25)
    # the cream gable with the arched window that peeks over the sign
    box("ph_gable", -21.0, -13.5, -16.8, -13.0, Z_DECK, Z_PH_WALL + 0.4, cream)
    hip_roof("ph_gable_roof", -21.0, -13.5, -16.8, -13.0, Z_PH_WALL + 0.4, Z_PH_CREST + 0.6, rust, ridge_axis="v", overhang=0.25)
    face_panel("ph_gable_arch", ("v", -16.8, -1), -17.25, arch_profile(2.4, Z_DECK + 1.2, Z_PH_WALL - 1.0, 0.8), 0.0, 0.10, glass)

    # --- NE wing mechanical roof --------------------------------------------
    box("mech_field", 9.0, 35.0, wv0 + 1.2, wv1 - 1.2, Z_DECK, Z_DECK + 0.25, stone)
    for i, u in enumerate((12.0, 17.5, 23.0, 28.5)):
        box(f"mech{i}", u, u + 3.6, 1.2, 5.2, Z_DECK + 0.25, Z_DECK + 1.8, steel)
    box("mech_pent", 6.0, 12.5, 8.0, 13.4, Z_DECK, Z_DECK + 2.6, cream, mat_top=roofd)
    # roof deck (2011) on the SE wing toward the Folsom corner
    box("roofdeck", 0.0, 34.0, -20.6, -16.4, Z_DECK, Z_DECK + 0.18, stone)

    # --- the campanile ------------------------------------------------------
    tu0, tu1, tv0, tv1 = TWR
    box("tower_shaft", tu0, tu1, tv0, tv1, 0.0, Z_TWR_ARC, brick)
    # paired slit recesses on the three exposed faces of the shaft
    T_NW = ("v", tv1, 1)
    T_SW = ("u", tu0, -1)
    T_NE = ("u", tu1, 1)
    tcu, tcv = (tu0 + tu1) / 2.0, (tv0 + tv1) / 2.0
    for tag, f, tc in (("tnw", T_NW, tcu), ("tsw", T_SW, tcv), ("tne", T_NE, tcv)):
        for k, dt in enumerate((-2.2, 2.2)):
            face_panel(
                f"{tag}_slit{k}", f, tc + dt, rect_profile(0.7, 9.0, Z_TWR_SHAFT - 2.7),
                0.0, 0.08, ink,
            )
    # arcade stage: four arched recesses per exposed face, glow plates behind
    arc_w = 2.15
    for tag, f, tc in (("anw", T_NW, tcu), ("asw", T_SW, tcv), ("ane", T_NE, tcv)):
        for k, dt in enumerate((-5.1, -1.7, 1.7, 5.1)):
            face_panel(
                f"{tag}_arch{k}", f, tc + dt,
                arch_profile(arc_w, Z_TWR_SHAFT + 0.6, Z_TWR_ARC - 2.6, 1.0),
                0.0, 0.10, ink,
            )
            face_panel(
                f"{tag}_glow{k}", f, tc + dt,
                rect_profile(arc_w - 0.5, Z_TWR_SHAFT + 1.1, Z_TWR_ARC - 2.9),
                0.10, 0.16, wglow,
            )
    # the SE face of the tower rises over the wing roof; give it two arches
    T_SE = ("v", tv0, -1)
    for k, dt in enumerate((-3.4, 3.4)):
        face_panel(
            f"ase_arch{k}", T_SE, tcu + dt,
            arch_profile(arc_w, Z_TWR_SHAFT + 0.6, Z_TWR_ARC - 2.6, 1.0),
            0.0, 0.10, ink,
        )
        face_panel(
            f"ase_glow{k}", T_SE, tcu + dt,
            rect_profile(arc_w - 0.5, Z_TWR_SHAFT + 1.1, Z_TWR_ARC - 2.9),
            0.10, 0.16, wglow,
        )
    # corbel cornice, parapet, pyramid, finial
    box("tower_corbel", tu0 - 0.5, tu1 + 0.5, tv0 - 0.5, tv1 + 0.5, Z_TWR_ARC, Z_TWR_CORBEL, trim)
    box("tower_parapet", tu0 - 0.15, tu1 + 0.15, tv0 - 0.15, tv1 + 0.15, Z_TWR_CORBEL, Z_TWR_PARAPET, brick)
    pyramid("tower_pyramid", tu0 + 0.6, tu1 - 0.6, tv0 + 0.6, tv1 - 0.6, Z_TWR_PARAPET - 0.15, Z_TWR_APEX, rust)
    box("tower_finial", tcu - 0.22, tcu + 0.22, tcv - 0.22, tcv + 0.22, Z_TWR_APEX - 0.3, Z_CREST, steel)

    # --- the rooftop neon sign ----------------------------------------------
    # Steel lattice + chunky red letter blocks, SE wing roof near the Harrison
    # corner, face to the bay. Letter widths spell the three-word rhythm; glow
    # plates sit proud of the letter faces on the SE side only.
    sign_v = -20.2
    z_lo, z_hi = Z_PARAPET + 0.7, Z_PARAPET + 3.6
    words = [
        ("HILLS", -34.0),
        ("BROS", -21.5),
        ("COFFEE", -12.5),
    ]
    letter_w, gap = 1.65, 0.45
    u_cursor_end = None
    for word, u_start in words:
        u_c = u_start
        for li, ch in enumerate(word):
            w = letter_w * (1.25 if ch in "MW" else 0.75 if ch in "I" else 1.0)
            box(
                f"sig_{word}_{li}", u_c, u_c + w, sign_v - 0.15, sign_v + 0.15,
                z_lo, z_hi, red,
            )
            # glow plate proud of the bay-side face
            face_panel(
                f"sig_{word}_{li}_glow", ("v", sign_v - 0.15, -1), u_c + w / 2.0,
                rect_profile(w - 0.12, z_lo + 0.1, z_hi - 0.1), 0.02, 0.09, rglow,
            )
            u_c += w + gap
        u_cursor_end = u_c
    # lattice: posts and two rails
    for i, u in enumerate((-34.5, -28.0, -21.8, -16.0, -12.8, -7.5, -4.2)):
        box(f"sig_post{i}", u, u + 0.18, sign_v - 0.09, sign_v + 0.09, Z_DECK, z_lo, steel)
    box("sig_rail_lo", -34.6, u_cursor_end + 0.3, sign_v - 0.08, sign_v + 0.08, z_lo - 0.16, z_lo, steel)
    box("sig_rail_hi", -34.6, u_cursor_end + 0.3, sign_v - 0.08, sign_v + 0.08, z_hi, z_hi + 0.16, steel)

    # ------------------------------------------------------------- bevels
    HEAVY = {
        "wing_se", "wing_nw", "wing_sw", "wing_ne", "tower_shaft", "tower_corbel",
        "tower_parapet", "tower_pyramid", "mech_pent",
    }
    MEDIUM_PREFIX = ("par_", "ph_", "curb_", "mech", "roofdeck")
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        name = obj.name
        if "glow" in name or "_w" in name or "arch" in name or "slit" in name or name.startswith("sig_"):
            continue  # flat pads, glow plates and sign parts stay sharp (budget)
        if name in HEAVY:
            bevel(obj, width=0.12, segments=2)
        elif name.startswith(MEDIUM_PREFIX):
            bevel(obj, width=0.06, segments=1)

    # ---------------------------------------------------- rotate to world
    # Pure rotation +45 deg (building u -> bearing 45), then recentre so the
    # world-axis bbox centre = origin = the manifest anchor.
    rot = Matrix.Rotation(math.radians(45.0), 4, "Z")
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.data.transform(rot)
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for obj in bpy.data.objects:
        if obj.type != "MESH":
            continue
        for v in obj.data.vertices:
            for i in range(3):
                mn[i] = min(mn[i], v.co[i])
                mx[i] = max(mx[i], v.co[i])
    shift = Matrix.Translation((-(mn.x + mx.x) / 2.0, -(mn.y + mx.y) / 2.0, -mn.z))
    for obj in bpy.data.objects:
        if obj.type == "MESH":
            obj.data.transform(shift)


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] xy centre offset={[round((mn[i] + mx[i]) / 2, 3) for i in range(2)]}")
    print("[build] anchor lon/lat: -122.3892854 37.7894167 (OSM ring bbox centre)")
    print("[build] Embarcadero facade normal 135 deg true (SE); tower projects NW")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "hills-brothers-building.blend")
    glb = os.path.join(out, "hills-brothers-building.glb")
    bpy.ops.wm.save_as_mainfile(filepath=blend)
    bpy.ops.export_scene.gltf(
        filepath=glb,
        export_format="GLB",
        export_apply=True,
        export_yup=True,
        use_selection=False,
        export_cameras=False,
        export_lights=False,
        export_animations=False,
        export_skins=False,
        export_morph=False,
        export_materials="EXPORT",
        export_image_format="NONE",
    )
    print(f"[build] wrote {blend}")
    print(f"[build] wrote {glb}")


if __name__ == "__main__":
    main()
