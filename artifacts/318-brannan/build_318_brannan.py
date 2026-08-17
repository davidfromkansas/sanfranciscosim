"""Deterministic Blender build of the SF-SIM miniature 318 Brannan Street.

    blender -b --python build_318_brannan.py -- [--out DIR]

Writes 318-brannan.blend and 318-brannan.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east, +Y north,
so the model drops into the city at its real-world heading — the loader applies
no rotation. Origin = footprint centroid (anchor lon -122.3927890,
lat 37.7816014), min Z = 0, parapet cap exactly 8.60 m.

Design (see REFERENCE.md for the sources behind every number):

* the measured DataSF LiDAR footprint (mblr SF3775100) — a clean four-vertex
  17.96 x 23.87 m rectangle at ~45.8 deg off the world axes, like the whole
  SoMa grid;
* a low, wide, PALE PAINTED CONCRETE box (1961, reinforced concrete per the
  National Register district report) — deliberately NOT the brick-and-timber
  warehouse of every other Brannan landmark in this manifest. It is a
  non-contributor in a historic warehouse district and it should look like one;
* the identity feature: TWO FULL-WIDTH DARK AWNING BANDS, one at the
  second-floor head and one over the ground-floor storefront, with the
  continuous ribbon window trapped between them. Three stripes on a cream box
  is the whole read at city scale;
* a narrow northeast end bay past a broad pier, carrying the dark number panel
  and the recessed glass entrance door;
* FOUR finished elevations — this building is free-standing (4.75 m side yard
  NE, 5.7 m rear yard NW, an open neighbour's yard SW), so there is no party
  wall to hide behind: blank service flank NE, punched windows SW, a working
  rear with a roll-up freight door NW;
* night state: the second-floor ribbon lit end to end (the hero — a bright band
  between two dark awnings), two lit storefront bays and a warm strip over the
  entrance. Glow surfaces are thin shells proud of the opaque glazing (the app
  renders _Glow in a separate layer that is ~12% alpha per layer by day — never
  author a primary surface as glow);
* a designed roof for the app's downward camera: a MID-GREY membrane (the real
  one is a pale grey membrane, not tar), a white coping ring, one 2.6 m square
  skylight northeast of centre, a ladder-and-comb network of raised white ducts
  across the southwest two-thirds, a dark mechanical cluster on the southwest
  side, and a deliberately EMPTY northeast third.

Corrections to docs/asset-plans/318-brannan.md made from the references (REPORT
beats plan): the two awnings stop at the broad pier and do NOT run across the
number bay (plan 2.7 steps 5/9 said full width); the storefront pier and the
ribbon pier are at different u, as photographed, rather than stacked.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

# DataSF building footprint SF3775100 projected with the app's tangent
# projection and recentred on the footprint centroid. CCW. A true rectangle:
# opposite edges agree to 3 mm, so nothing is regularised away here.
FOOTPRINT = [
    (1.867, -14.819),    # front-SW
    (14.756, -2.312),    # front-NE
    (-1.867, 14.819),    # rear-NE
    (-14.756, 2.312),    # rear-SW
]

EDGE_FRONT = 0   # 17.96 m, faces SE 135.8 deg — Brannan Street
EDGE_NE = 1      # 23.87 m, faces NE  45.8 deg — side yard / parking
EDGE_REAR = 2    # 17.96 m, faces NW 315.8 deg — rear yard
EDGE_SW = 3      # 23.87 m, faces SW 225.8 deg — 326 Brannan's yard

Z_DECK = 7.90        # roof membrane / top of the body (LiDAR mode 7.78)
Z_PARAPET = 8.60     # parapet cap -> the bbox top
Z_BULK = 0.55        # storefront bulkhead
Z_SFA, Z_SFB = 0.55, 3.35    # ground-floor storefront glazing
Z_AW1A, Z_AW1B = 3.35, 4.35  # lower awning band
Z_SPAN = 4.90        # top of the spandrel / sill of the ribbon
Z_RIBA, Z_RIBB = 4.90, 6.35  # second-floor ribbon window
Z_TRANSOM = 5.75     # transom reveal inside the ribbon
Z_AW2A, Z_AW2B = 6.40, 7.60  # upper awning band (the sign band)

AW1_PROJ = 1.20      # lower awning projection from the wall plane
AW2_PROJ = 0.85      # upper awning projection — shortened from 1.10 so the
                     # ribbon behind it is not wholly occluded from the app's
                     # 30-50 deg downward camera, where the ribbon is the night hero

SKIN = 0.10          # applied-panel standoff from the wall plane
PARAPET_T = 0.30     # parapet wall thickness

# Front elevation layout, u measured along the Brannan edge from its SW corner.
U_BAND_A, U_BAND_B = 0.50, 15.20   # the banded zone (awnings + glazing)
U_PIER_A, U_PIER_B = 15.20, 15.75  # the broad pier
U_END_C = 16.85                    # centre of the number / entrance bay

PALETTE_HEX = {
    # The painted concrete body. Toy_cream is the palette's warm off-white; the
    # real paint reads warm white in sun and cool grey in shade.
    "Toy_cream": "f2ede3",
    "Toy_white": "f7f4ec",   # coping, window and storefront frames, roof ducts
    "Toy_stone": "d9d2c2",   # bulkhead, the NE flank's reveal
    # BOTH AWNINGS. Plan 2.8 specified Toy_navy (2c4a70) on the strength of the
    # listing photograph; the first aerial render killed it — navy awnings and
    # Toy_glass glazing (2a4d73) are 2 hex points apart and the three-stripe
    # composition collapsed into one navy mass, which is the exact failure the
    # plan's own §2.6 warned about. Toy_ink is also the truer reading of the
    # May 2025 Street View, where both awnings are effectively black.
    "Toy_ink": "3a3530",     # BOTH AWNINGS, number panel, doors
    "Toy_glass": "2a4d73",   # storefront, ribbon, flank and rear glazing
    "Toy_glassl": "6f95b8",  # the roof skylight
    "Toy_steel": "9aa0a6",   # roof membrane, vent cans
    "Toy_roofd": "45454a",   # rear roll-up door, roof mechanical units
    # Glow colours are the LIT appearance, not the day colour: a night window
    # that glows in its own dark navy reads as a hole.
    "Toy_glassl_Glow": "6f95b8",
    "Toy_glass_Glow": "6f95b8",
    "Toy_gold_Glow": "caa64a",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}

# --------------------------------------------------------------- 2D helpers


def poly_edge(i):
    """Edge i of FOOTPRINT: (origin, length, tangent unit, outward normal)."""
    a = FOOTPRINT[i]
    b = FOOTPRINT[(i + 1) % len(FOOTPRINT)]
    dx, dy = b[0] - a[0], b[1] - a[1]
    length = math.hypot(dx, dy)
    t = (dx / length, dy / length)
    n = (t[1], -t[0])  # CCW polygon -> outward
    return a, length, t, n


def offset_polygon(poly, d):
    """Miter offset of the convex CCW footprint; positive d moves outward."""
    npts = len(poly)
    normals = []
    for i in range(npts):
        a, b = poly[i], poly[(i + 1) % npts]
        dx, dy = b[0] - a[0], b[1] - a[1]
        length = math.hypot(dx, dy) or 1.0
        normals.append((dy / length, -dx / length))
    out = []
    for i in range(npts):
        n1, n2 = normals[i - 1], normals[i]
        v = poly[i]
        det = n1[0] * n2[1] - n1[1] * n2[0]
        if abs(det) < 1e-6:
            out.append((v[0] + n2[0] * d, v[1] + n2[1] * d))
            continue
        c1 = v[0] * n1[0] + v[1] * n1[1] + d
        c2 = v[0] * n2[0] + v[1] * n2[1] + d
        out.append(((c1 * n2[1] - c2 * n1[1]) / det, (c2 * n1[0] - c1 * n2[0]) / det))
    return out


def rect_profile(w, z0, z1):
    a = w / 2.0
    return [(-a, z0), (a, z0), (a, z1), (-a, z1)]


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
    """Miniature-style edge softening on the chunky solids (style bible s.4).

    The width is capped at a third of the object's thinnest dimension: the
    applied panels here are only 60-200 mm thick, and a flat bevel on those
    relies entirely on clamp_overlap, which collapses opposing profiles into
    zero-area slivers. The 1 mm remove_doubles/dissolve_degenerate pass
    afterwards sweeps up whatever clamping still pinches shut — the same
    tolerance Phase B of the optimize pass welds at, and three orders of
    magnitude below any authored feature here.
    """
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
    bmesh.ops.remove_doubles(bm, verts=list(bm.verts), dist=1e-3)
    bmesh.ops.dissolve_degenerate(bm, dist=1e-3, edges=list(bm.edges))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, poly, z0, z1, mat, mat_caps=None):
    """Closed extrusion of a CCW polygon (walls + both caps)."""
    npts = len(poly)
    verts = [(x, y, z0) for x, y in poly] + [(x, y, z1) for x, y in poly]
    faces, face_mats = [], []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
        face_mats.append(0)
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    face_mats += [1 if mat_caps else 0] * 2
    mats = [mat, mat_caps] if mat_caps else [mat]
    return new_mesh(name, verts, faces, mats, face_mats)


def ring_band(name, poly, z0, z1, off_in, off_out, mat):
    """Closed band following a footprint: 4 loops, quads between."""
    lo_in = offset_polygon(poly, off_in)
    lo_out = offset_polygon(poly, off_out)
    npts = len(lo_in)
    verts = []
    for loop, z in ((lo_in, z0), (lo_out, z0), (lo_out, z1), (lo_in, z1)):
        verts.extend([(x, y, z) for x, y in loop])
    faces = []
    for k in range(4):
        a0, b0 = k * npts, ((k + 1) % 4) * npts
        for i in range(npts):
            j = (i + 1) % npts
            faces.append((a0 + i, a0 + j, b0 + j, b0 + i))
    return new_mesh(name, verts, faces, [mat])


def face_panel(name, edge, u_centre, profile, d0, d1, mat):
    """Closed prism of a (u, z) profile lying in the plane of wall `edge`,
    extruded outward from offset d0 to d1 along that wall's normal."""
    a, _length, t, n = poly_edge(edge)
    verts = []
    for d in (d0, d1):
        for du, z in profile:
            px = a[0] + t[0] * (u_centre + du) + n[0] * d
            py = a[1] + t[1] * (u_centre + du) + n[1] * d
            verts.append((px, py, z))
    npts = len(profile)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(name, verts, faces, [mat])


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0):
    """Box with local +x along yaw and local +y 90 deg ccw of it."""
    c, s = math.cos(yaw), math.sin(yaw)
    corners = []
    for lx, ly in ((-sx / 2, -sy / 2), (sx / 2, -sy / 2), (sx / 2, sy / 2), (-sx / 2, sy / 2)):
        corners.append((cx + lx * c - ly * s, cy + lx * s + ly * c))
    verts = [(x, y, z0) for x, y in corners] + [(x, y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    return new_mesh(name, verts, faces, [mat])


def roof_box(name, u, v, z0, z1, su, sv, mat):
    """Box on the roof, aligned to the building's own grid rather than to the
    world axes: u runs along the Brannan edge from its SW end, v runs INTO the
    block (against the outward normal)."""
    origin, _l, t, n = poly_edge(EDGE_FRONT)
    cx = origin[0] + t[0] * u - n[0] * v
    cy = origin[1] + t[1] * u - n[1] * v
    return box(name, cx, cy, z0, z1, su, sv, mat, yaw=math.atan2(t[1], t[0]))


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
        # Flagged for the app's night pass; emission is off in the day asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    return mat


# --------------------------------------------------------------------- parts


def rect_opening(tag, edge, u, w, z0, z1, frame_mat, fill_mat, glow_mat=None, glow_inset=0.30):
    """Frame panel + a smaller fill that protrudes further, so the frame reads
    as a border ring around a recessed opening. No booleans, all closed solids."""
    face_panel(f"{tag}_frame", edge, u, rect_profile(w, z0, z1), 0.0, SKIN + 0.06, frame_mat)
    inset = 0.16
    face_panel(
        f"{tag}_fill",
        edge,
        u,
        rect_profile(w - 2 * inset, z0 + inset, z1 - inset),
        0.0,
        SKIN + 0.13,
        fill_mat,
    )
    if glow_mat is not None:
        g = glow_inset
        face_panel(
            f"{tag}_glow",
            edge,
            u,
            rect_profile(w - 2 * g, z0 + g, z1 - g),
            SKIN + 0.10,
            SKIN + 0.16,
            glow_mat,
        )


def awning(tag, edge, u_a, u_b, z0, z1, proj, rise, mat):
    """A shed awning: vertical valance at the outer edge (the face that carries
    the sign and does all the work at city scale), a flat underside, and a top
    that rakes back UP to the wall.

    The first build extruded these as plain slabs and let the 0.12 m mass bevel
    round them off; from the aerial they read as navy pipes bolted to the
    facade, not as awnings. The rake is what tells the eye which way is up, and
    it also gives the app's downward camera a dark sloped plane instead of a
    flat dark stripe.
    """
    a, _length, t, n = poly_edge(edge)
    prof = [(0.0, z0), (proj, z0), (proj, z1), (0.0, z1 + rise)]
    verts = []
    for u in (u_a, u_b):
        for d, z in prof:
            verts.append((a[0] + t[0] * u + n[0] * d, a[1] + t[1] * u + n[1] * d, z))
    npts = len(prof)
    faces = []
    for i in range(npts):
        j = (i + 1) % npts
        faces.append((i, j, npts + j, npts + i))
    faces.append(tuple(range(npts - 1, -1, -1)))
    faces.append(tuple(range(npts, 2 * npts)))
    return new_mesh(f"{tag}_awning", verts, faces, [mat])


def build():
    for coll in (bpy.data.objects, bpy.data.meshes, bpy.data.materials):
        for item in list(coll):
            coll.remove(item)
    scene = bpy.context.scene

    cream = material("Toy_cream")
    white = material("Toy_white")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    glassl = material("Toy_glassl")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    ink = material("Toy_ink")
    lglow = material("Toy_glassl_Glow")
    gglow = material("Toy_glass_Glow")
    warm = material("Toy_gold_Glow")

    len_front = poly_edge(EDGE_FRONT)[1]   # 17.96
    len_flank = poly_edge(EDGE_NE)[1]      # 23.87

    # --- painted concrete body; its top cap IS the roof membrane ------------
    prism("body", FOOTPRINT, 0.0, Z_DECK, cream, mat_caps=steel)

    # --- parapet ring + light coping ---------------------------------------
    # The membrane is a mid grey, so the ring reads from the coping being
    # clearly lighter than the deck (plan 2.9). 0.70 m total, which is what
    # reconciles the LiDAR mode (7.78) with the architectural top.
    ring_band("parapet", FOOTPRINT, Z_DECK, Z_PARAPET - 0.14, -PARAPET_T, 0.0, cream)
    ring_band("coping", FOOTPRINT, Z_PARAPET - 0.14, Z_PARAPET, -PARAPET_T - 0.06, 0.06, white)

    # ======================= BRANNAN STREET FRONT ==========================
    # Five horizontal layers. The two dark bands ARE the building; everything
    # else on this elevation exists to give them something to band.

    # bulkhead under the storefront
    face_panel(
        "bulkhead", EDGE_FRONT, (U_BAND_A + U_BAND_B) / 2.0,
        rect_profile(U_BAND_B - U_BAND_A, 0.0, Z_BULK), 0.0, SKIN - 0.02, stone,
    )

    # four storefront bays around one broader central pier at u = 7.85
    SFRONT = [(2.37, 3.33), (5.91, 3.33), (9.79, 3.33), (13.32, 3.33)]
    LIT_SFRONT = {1, 2}
    for i, (u, w) in enumerate(SFRONT):
        rect_opening(
            f"sfront{i}", EDGE_FRONT, u, w, Z_SFA, Z_SFB, white, glass,
            gglow if i in LIT_SFRONT else None, glow_inset=0.34,
        )

    # THE IDENTITY, part 1: the ground-floor awning
    awning("aw_low", EDGE_FRONT, U_BAND_A, U_BAND_B, Z_AW1A, Z_AW1B, AW1_PROJ, 0.30, ink)

    # second-floor ribbon: two unequal groups split by one pale pier at u = 9.40
    # (photographed off-centre; deliberately NOT stacked over the storefront
    # pier). Each group is one glazed panel with a single transom reveal —
    # individual mullions are sub-pixel at city scale.
    RIBBON = [(4.89, 8.37), (12.35, 5.25)]
    for i, (u, w) in enumerate(RIBBON):
        rect_opening(f"ribbon{i}", EDGE_FRONT, u, w, Z_RIBA, Z_RIBB, white, glass,
                     lglow, glow_inset=0.26)
        face_panel(
            f"ribbon{i}_transom", EDGE_FRONT, u,
            rect_profile(w - 0.28, Z_TRANSOM, Z_TRANSOM + 0.10), 0.0, SKIN + 0.17, white,
        )

    # THE IDENTITY, part 2: the second-floor sign awning
    awning("aw_up", EDGE_FRONT, U_BAND_A, U_BAND_B, Z_AW2A, Z_AW2B, AW2_PROJ, 0.28, ink)

    # the broad pier, then the northeast end bay: number panel over a recessed
    # glass entrance. The awnings stop at the pier — photographed, and a
    # correction to plan 2.7 steps 5/9.
    face_panel(
        "pier_end", EDGE_FRONT, (U_PIER_A + U_PIER_B) / 2.0,
        rect_profile(U_PIER_B - U_PIER_A, 0.0, Z_PARAPET - 0.16), 0.0, SKIN + 0.04, cream,
    )
    face_panel(
        "number_panel", EDGE_FRONT, U_END_C, rect_profile(1.85, 4.35, 5.75),
        0.0, SKIN + 0.06, ink,
    )
    rect_opening("entrance", EDGE_FRONT, U_END_C, 1.60, 0.0, 2.70, white, glass)
    face_panel(
        "entrance_glow", EDGE_FRONT, U_END_C, rect_profile(1.30, 2.78, 2.96),
        SKIN + 0.04, SKIN + 0.11, warm,
    )

    # ======================= SOUTHWEST FLANK ===============================
    # Exposed above 326 Brannan's low fenced yard, so it is seen from the
    # street and from above. The listing's "two sides of windows" and the
    # ground-floor plan's openings put daylight here; the rhythm is inferred
    # and deliberately restrained (plan 2.15 risk 6).
    SW_BAYS = (3.6, 8.0, 12.4, 16.8, 21.2)
    for i, u in enumerate(SW_BAYS):
        rect_opening(f"swup{i}", EDGE_SW, u, 2.40, 4.90, 6.20, white, glass,
                     lglow if i in (1, 3) else None, glow_inset=0.30)
    # Ground-floor openings sit UNDER two of the upper bays, not between them:
    # the first build scattered them and the flank read as sprinkled portholes.
    for i, u in enumerate((SW_BAYS[1], SW_BAYS[3])):
        rect_opening(f"swlo{i}", EDGE_SW, u, 2.40, 1.10, 2.70, white, glass)

    # ======================= NORTHEAST FLANK ===============================
    # Blind service elevation: the ground-floor plan puts lobby, stairs,
    # restrooms, copy room and electrical room along this wall. One reveal at
    # the floor line and one service door. Do NOT add windows here.
    face_panel(
        "ne_reveal", EDGE_NE, len_flank / 2.0,
        rect_profile(len_flank - 0.80, 4.35, 4.41), 0.0, SKIN - 0.02, stone,
    )
    rect_opening("ne_door", EDGE_NE, 19.5, 1.00, 0.0, 2.40, white, ink)

    # ======================= NORTHWEST REAR ================================
    # A working back onto the rear yard, not a designed elevation. The roll-up
    # door is established by the listing and the interior photograph; its
    # position is inferred (plan 2.15 risk 7).
    rect_opening("rear_rollup", EDGE_REAR, 12.5, 3.60, 0.0, 3.40, white, roofd)
    rect_opening("rear_door", EDGE_REAR, 2.2, 1.00, 0.0, 2.40, white, ink)
    rect_opening("rear_win", EDGE_REAR, 8.0, 6.00, 4.90, 6.20, white, glass)

    # ============================ THE ROOF =================================
    # 429 m2 and the surface the app's camera actually looks at. u runs along
    # the Brannan edge from its SW end, v goes back into the block (23.87 m
    # deep). Nothing here is taller than the 0.70 m parapet.
    Z_D = Z_DECK
    roof_box("skylight_kerb", 12.6, 8.5, Z_D, Z_D + 0.24, 2.60, 2.60, white)
    roof_box("skylight", 12.6, 8.5, Z_D + 0.18, Z_D + 0.42, 2.24, 2.24, glassl)

    # the duct ladder: two trunks parallel to Brannan, four branches running
    # back from them, one spur. Irregular on purpose — the aerial shows a comb,
    # not a grid.
    DUCTS = [
        ("duct_trunk_f", 7.2, 6.2, 12.2, 0.70),
        ("duct_trunk_r", 6.4, 16.4, 10.6, 0.70),
        ("duct_br1", 1.6, 11.3, 0.60, 9.50),
        ("duct_br2", 5.2, 9.6, 0.60, 6.20),
        ("duct_br3", 9.0, 11.3, 0.60, 9.50),
        ("duct_br4", 10.6, 8.0, 0.60, 3.00),
        ("duct_spur", 11.2, 19.6, 4.60, 0.60),
    ]
    for name, u, v, su, sv in DUCTS:
        roof_box(name, u, v, Z_D, Z_D + 0.48, su, sv, white)

    # mechanical cluster, southwest side
    roof_box("mech_a", 3.0, 13.4, Z_D, Z_D + 0.65, 1.90, 1.40, roofd)
    roof_box("mech_b", 3.4, 17.2, Z_D, Z_D + 0.55, 1.60, 1.20, roofd)
    roof_box("mech_c", 5.4, 14.6, Z_D, Z_D + 0.45, 1.00, 0.80, roofd)

    # vent cans scattered over the deliberately clear northeast third
    for i, (u, v) in enumerate(((15.4, 4.6), (16.2, 13.0), (14.2, 19.4))):
        roof_box(f"vent{i}", u, v, Z_D, Z_D + 0.55, 0.45, 0.45, steel)

    # Bevel budget: the chunky masses and the awning slabs carry the miniature
    # read, so they get the full 0.12/2. Applied window panels are small and
    # numerous — their frames get a token 1-segment softening and the
    # fills/glow shells none at all, which is what keeps this under the cap.
    for obj in list(bpy.data.objects):
        if obj.type != "MESH":
            continue
        if obj.name.endswith(("_fill", "_glow")) or obj.name == "entrance_glow":
            continue
        if obj.name.endswith(("_frame", "_transom")):
            bevel(obj, width=0.05, segments=1)
        elif obj.name.startswith(("duct", "vent", "mech", "skylight", "aw_")):
            # Roof furniture and the awnings are 0.45-0.70 m thin. The mass
            # bevel clamps to a third of that and rounds them into tubes.
            bevel(obj, width=0.06, segments=1)
        else:
            bevel(obj, width=0.12, segments=2)

    return scene


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
    print("[build] anchor lon/lat: -122.3927890 37.7816014 (footprint centroid)")
    print("[build] Brannan front heading: 135.8 deg true (SE)")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "318-brannan.blend")
    glb = os.path.join(out, "318-brannan.glb")
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
