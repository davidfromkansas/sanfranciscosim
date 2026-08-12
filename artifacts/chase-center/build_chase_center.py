"""Deterministic Blender build of the SF-SIM miniature Chase Center.

    blender -b --python build_chase_center.py -- [--out DIR]

Writes chase-center.blend and chase-center.glb next to this file (or into --out).
Geometry is authored directly in world space in metres, Z up, +X east,
+Y true north, origin at the footprint centroid, min Z = 0, so the export needs
no transforms applied after the fact.

Design (see REFERENCE.md for the sources behind every number):

* the plan is NOT an idealised circle or rounded square - it is the real OSM
  footprint (way/579646390) reduced to a 6-harmonic radial curve r(theta),
  rms 2.0 m against the surveyed polygon and within 0.1% on area, so the drum
  keeps its true lobes (it bulges NE to r=85.6 and pinches NW to r=71.8);
* a stone plinth, a recessed glazed retail band and a soffit band, so the pale
  drum reads as floating on its base;
* the main drum in pale aluminium carrying 60 vertical panel bands - the
  documented compression of ~7,500 real metal panels into a broad rhythm;
* the signature sail parapet: a ring above the roof deck whose top edge swoops
  from 34.0 m on the bay side to the 40.8 m crest directly over the west entry,
  its crest course projecting 0.25 m so its underside can carry the cove light;
* the glazed west entry atrium on the Thrive City axis, its navy canopy, and
  the oversized video board on the WNW facade - the night-glow hero;
* a designed roof: pale membrane, perimeter catwalk, one central mechanical
  block and six ringed units (the camera looks down on 19,000 m2 of it);
* flat Toy_* materials only. Three glow surfaces: the video board, the atrium
  front, and the west arc of the parapet cove.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# ---------------------------------------------------------------- parameters

H_CREST = 40.8        # architectural crest: 134 ft facade height (Enclos)
H_DECK = 31.8         # roof deck: 31.755 m structural height (Dlubal)
H_PARAPET_MIN = 32.9  # parapet top on the bay (east) side
CREST_BEARING = 270.0 # the sail peak sits over the west entry
CREST_POWER = 2.2     # how concentrated the peak is

# Real footprint, OSM way/579646390, as a radial Fourier series about the
# polygon centroid. Bearing theta: 0 = true north, 90 = east.
R0 = 78.5904
HARM = [
    (+0.0081, -0.1728),
    (+0.1430, +2.4505),
    (+3.1665, +1.1815),
    (-1.3078, +3.0476),
    (-1.0559, -0.9333),
    (+0.1432, +0.1980),
]

SEG_FINE = 240        # drum and parapet: 6 samples per panel band
SEG_COARSE = 120      # plinth, glazing, roof rings
BANDS = 40            # vertical panel bands around the drum (~12 m pitch)
BAND_DEPTH = 0.70

Z_PLINTH = 1.6
Z_GLASS = 8.4
Z_SOFFIT = 11.2

# "Stacked drums of varying sizes" (Enclos): the skin steps back once, which is
# what stops a 155 m cylinder reading as a tin can.
DRUM_INSET = 1.0      # lower drum, set back from the plinth face
UPPER_INSET = 2.1     # upper drum, one shallow ledge two thirds up
Z_LEDGE = 20.0        # top of the lower drum
Z_SKIN = 19.6         # bottom of the upper skin (overlapped, never coplanar)

CREST_PROUD = 0.25    # the crest course oversails the drum
PARAPET_INNER = 4.5   # parapet wall thickness (inset from the plan)
CREST_H = 1.0         # depth of the crest course

GOLD_ARC = 20.0       # +/- degrees of Warriors gold on the crest
COVE_ARC = 45.0       # +/- degrees of cove light under the crest

ROOF_INSET = 4.4      # membrane, tucked 0.1 m into the parapet's inner face
CATWALK_IN, CATWALK_OUT = 7.4, 4.6
BOWL_R = 50.0         # the raised deck over the seating bowl
PAD_R = 61.0          # ring radius of the twelve roof pads

ATRIUM_BEARING = 270.0
ATRIUM_PROJ = 0.3     # a glazed slot cut through the skin, not a projecting shed
ATRIUM_DEPTH = 12.0
ATRIUM_W = 36.0
ATRIUM_TOP = 24.0

BOARD_BEARING = 297.0 # the video board faces the plaza's north half
BOARD_W, BOARD_H = 26.0, 13.0
BOARD_Z = 14.5

# Project palette from .agents/skills/sf-asset-check (hex, sRGB). Materials are
# authored with the linear equivalents, which is what the shipped kit GLBs hold.
PALETTE_HEX = {
    "Toy_trim": "f3efe6",
    "Toy_sand": "ece4d4",
    "Toy_stone": "d9d2c2",
    "Toy_glass": "2a4d73",
    "Toy_steel": "9aa0a6",
    "Toy_roofd": "45454a",
    "Toy_navy": "2c4a70",
    "Toy_gold": "caa64a",
    "Toy_sky_Glow": "6db3d9",
    "Toy_white_Glow": "f7f4ec",
}


def srgb_to_linear(hexcode):
    out = []
    for i in (0, 2, 4):
        c = int(hexcode[i : i + 2], 16) / 255.0
        out.append(c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4)
    return tuple(out)


PALETTE = {k: srgb_to_linear(v) for k, v in PALETTE_HEX.items()}


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
        # Flagged for the app's night pass; emission is off in the daylight asset.
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    return mat


# ------------------------------------------------------------ the real plan


def radius(theta):
    """The surveyed footprint radius at compass bearing theta (radians)."""
    r = R0
    for k, (ak, bk) in enumerate(HARM, 1):
        r += ak * math.cos(k * theta) + bk * math.sin(k * theta)
    return r


def band_depth(theta):
    """Vertical panel rhythm: 60 shallow recesses around the drum."""
    return BAND_DEPTH * (0.5 - 0.5 * math.cos(BANDS * theta))


def outline(seg, inset=0.0, fluted=False):
    """`seg` points around the plan, clockwise seen from +Z (bearing order)."""
    pts = []
    for i in range(seg):
        t = 2 * math.pi * i / seg
        r = radius(t) - inset
        if fluted:
            r -= band_depth(t)
        pts.append((r * math.sin(t), r * math.cos(t)))
    return pts


def parapet_top(theta):
    """Sail profile: HP_MIN on the bay side rising to the crest over the entry."""
    d = theta - math.radians(CREST_BEARING)
    f = ((1.0 + math.cos(d)) * 0.5) ** CREST_POWER
    return H_PARAPET_MIN + (H_CREST - H_PARAPET_MIN) * f


def bearing_of(i, seg):
    return (math.degrees(2 * math.pi * i / seg)) % 360.0


def arc_delta(bearing, centre):
    d = abs((bearing - centre + 180.0) % 360.0 - 180.0)
    return d


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
    """Miniature-style edge softening on the chunky solids (style bible s.4)."""
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    bmesh.ops.bevel(
        bm,
        geom=list(bm.verts) + list(bm.edges),
        offset=width,
        segments=segments,
        profile=0.5,
        affect="EDGES",
        clamp_overlap=True,
    )
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(obj.data)
    bm.free()
    obj.data.shade_flat()
    return obj


def prism(name, pts, z0, z1, mat):
    """A closed solid extrusion of a closed 2-D outline."""
    n = len(pts)
    verts = [(x, y, z0) for x, y in pts] + [(x, y, z1) for x, y in pts]
    faces = [(i, n + i, n + (i + 1) % n, (i + 1) % n) for i in range(n)]
    faces.append(tuple(range(n)))
    faces.append(tuple(range(2 * n - 1, n - 1, -1)))
    return new_mesh(name, verts, faces, [mat])


def ring(name, outer, inner, z0, z1, mats, face_mat=None):
    """A closed band. `z0`/`z1` may be scalars or per-index lists. `face_mat` is
    called with (k, i) where k = 0 outer wall, 1 top, 2 inner wall, 3 bottom."""
    n = len(outer)
    z0s = z0 if isinstance(z0, list) else [z0] * n
    z1s = z1 if isinstance(z1, list) else [z1] * n
    rings = [
        [(outer[i][0], outer[i][1], z0s[i]) for i in range(n)],
        [(outer[i][0], outer[i][1], z1s[i]) for i in range(n)],
        [(inner[i][0], inner[i][1], z1s[i]) for i in range(n)],
        [(inner[i][0], inner[i][1], z0s[i]) for i in range(n)],
    ]
    verts = [v for r in rings for v in r]
    faces = []
    fmats = []
    for k in range(4):
        a0, b0 = k * n, ((k + 1) % 4) * n
        for i in range(n):
            j = (i + 1) % n
            faces.append((a0 + i, b0 + i, b0 + j, a0 + j))
            fmats.append(face_mat(k, i) if face_mat else 0)
    return new_mesh(name, verts, faces, mats, fmats)


def rot2(p, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (p[0] * c - p[1] * s, p[0] * s + p[1] * c)


def box(name, cx, cy, z0, z1, sx, sy, mat, yaw=0.0, bev=0.12):
    hx, hy = sx / 2, sy / 2
    corners = [rot2(c, yaw) for c in ((-hx, -hy), (hx, -hy), (hx, hy), (-hx, hy))]
    verts = [(cx + x, cy + y, z0) for x, y in corners]
    verts += [(cx + x, cy + y, z1) for x, y in corners]
    faces = [
        (3, 2, 1, 0),
        (4, 5, 6, 7),
        (0, 1, 5, 4),
        (1, 2, 6, 5),
        (2, 3, 7, 6),
        (3, 0, 4, 7),
    ]
    obj = new_mesh(name, verts, faces, [mat])
    if bev:
        bevel(obj, width=bev)
    return obj


def facade_box(name, bearing_deg, standoff, along, z0, z1, size_along, depth,
               mat, bev=0.12):
    """A box hung on the facade at a compass bearing: `standoff` is how far its
    OUTER face stands beyond the plan radius at that bearing, `along` is the
    sideways offset on the tangent, `depth` its thickness inward."""
    t = math.radians(bearing_deg)
    out = (math.sin(t), math.cos(t))
    tan = (math.cos(t), -math.sin(t))
    r_out = radius(t) + standoff
    cr = r_out - depth / 2
    cx = out[0] * cr + tan[0] * along
    cy = out[1] * cr + tan[1] * along
    return box(name, cx, cy, z0, z1, size_along, depth, mat,
               yaw=-t, bev=bev)


# ------------------------------------------------------------------- volumes


def build_base(stone, glass):
    prism("plinth", outline(SEG_COARSE), 0.0, Z_PLINTH, stone)
    prism("retail_glazing", outline(SEG_COARSE, inset=1.4), Z_PLINTH, Z_GLASS, glass)
    prism("concourse_band", outline(SEG_COARSE), Z_GLASS, Z_SOFFIT, stone)


def build_drum(trim, sand):
    prism("drum_lower", outline(SEG_FINE, inset=DRUM_INSET, fluted=True),
          Z_SOFFIT, Z_LEDGE, trim)
    prism("drum_ledge", outline(SEG_COARSE, inset=UPPER_INSET - 0.45),
          Z_LEDGE - 0.4, Z_LEDGE + 0.25, sand)


def build_parapet(trim, sand, gold, glow):
    """The sail. The whole upper skin carries the swoop - a swooping *parapet*
    on a flat-topped drum was invisible from the app's camera in review, so the
    skin itself rises from 1.1 m above the deck on the bay side to 8 m over the
    west entry, and the silhouette does the recognition work."""
    outer = outline(SEG_FINE, inset=UPPER_INSET, fluted=True)
    crest_outer = outline(SEG_FINE, inset=UPPER_INSET - CREST_PROUD, fluted=True)
    inner = outline(SEG_FINE, inset=PARAPET_INNER)
    tops = [parapet_top(2 * math.pi * i / SEG_FINE) for i in range(SEG_FINE)]
    unders = [t - CREST_H for t in tops]

    # the sail wall, aluminium outside, warmer inside where the roof sees it
    ring("sail_skin", outer, inner, Z_SKIN, unders, [trim, sand],
         face_mat=lambda k, i: 1 if k == 2 else 0)

    # the crest course: oversails 0.25 m, carries the gold over the entry and
    # the cove light on its exposed underside through the west quadrant
    def crest_mat(k, i):
        b = bearing_of(i, SEG_FINE)
        if k in (0, 1):                                   # outer wall and top
            return 1 if arc_delta(b, CREST_BEARING) <= GOLD_ARC else 0
        if k == 3:                                        # exposed underside
            return 2 if arc_delta(b, CREST_BEARING) <= COVE_ARC else 0
        return 0

    ring("sail_crest", crest_outer, inner, unders, tops,
         [trim, gold, glow], face_mat=crest_mat)


def build_roof(stone, sand, steel, roofd):
    # membrane, then the raised deck over the seating bowl: two clean values,
    # not a field of scattered props (style bible s.10)
    prism("roof_membrane", outline(SEG_COARSE, inset=ROOF_INSET),
          H_DECK - 0.9, H_DECK, stone)
    prism("roof_bowl_deck", [(BOWL_R * math.sin(2 * math.pi * i / 72),
                              BOWL_R * math.cos(2 * math.pi * i / 72))
                             for i in range(72)],
          H_DECK - 0.2, H_DECK + 0.35, sand)
    ring("roof_catwalk", outline(SEG_COARSE, inset=CATWALK_OUT),
         outline(SEG_COARSE, inset=CATWALK_IN), H_DECK - 0.2, H_DECK + 0.5,
         [roofd])
    # one plant cluster: a central block flanked by two tidy rows of units
    box("roof_plant_main", 0.0, 0.0, H_DECK + 0.1, H_DECK + 5.2, 44.0, 24.0, steel)
    box("roof_plant_cap", 0.0, 0.0, H_DECK + 5.2, H_DECK + 5.6, 39.0, 19.0, roofd)
    for k, (ux, uy) in enumerate(
        (x, y) for y in (-17.5, 17.5) for x in (-13.5, 13.5)
    ):
        box(f"roof_unit_{k}", ux, uy, H_DECK + 0.1, H_DECK + 2.8, 21.0, 6.5, steel)
    # twelve panel pads on a ring: the graphical repetition a 19,000 m2 roof needs
    for k in range(12):
        b = math.radians(15.0 + 30.0 * k)
        box(f"roof_pad_{k}", PAD_R * math.sin(b), PAD_R * math.cos(b),
            H_DECK - 0.1, H_DECK + 0.3, 15.0, 6.5, roofd, yaw=-b, bev=0.08)


def build_entry(glass, trim, steel, glow):
    """A glazed slot cut through the aluminium skin, with a pale reveal so the
    dark glass separates from the equally dark retail band below it, and a
    canopy narrower than the slot so the two do not fight."""
    facade_box("atrium", ATRIUM_BEARING, ATRIUM_PROJ, 0.0, 0.0, ATRIUM_TOP,
               ATRIUM_W, ATRIUM_DEPTH, glass, bev=0.25)
    for k, off in enumerate((-19.5, 19.5)):
        facade_box(f"atrium_cheek_{k}", ATRIUM_BEARING, ATRIUM_PROJ + 1.0, off,
                   0.0, ATRIUM_TOP + 1.4, 3.0, 2.4, trim, bev=0.15)
    facade_box("atrium_head", ATRIUM_BEARING, ATRIUM_PROJ + 1.0, 0.0,
               ATRIUM_TOP, ATRIUM_TOP + 1.4, ATRIUM_W + 6.0, 2.4, trim, bev=0.15)
    for k, off in enumerate((-11.0, -3.7, 3.7, 11.0)):
        facade_box(f"atrium_fin_{k}", ATRIUM_BEARING, ATRIUM_PROJ + 1.2, off,
                   0.0, ATRIUM_TOP, 1.1, 1.8, steel)
    facade_box("atrium_glow", ATRIUM_BEARING, ATRIUM_PROJ + 0.5, 0.0,
               1.8, 5.8, 26.0, 0.5, glow, bev=0.06)
    facade_box("entry_canopy", ATRIUM_BEARING, ATRIUM_PROJ + 6.5, 0.0,
               6.0, 7.4, 28.0, 8.0, trim, bev=0.15)


def build_board(navy, sky_glow):
    facade_box("board_frame", BOARD_BEARING, 0.9, 0.0, BOARD_Z - 1.1,
               BOARD_Z + BOARD_H + 1.1, BOARD_W + 2.2, 1.6, navy, bev=0.1)
    facade_box("board_screen", BOARD_BEARING, 1.5, 0.0, BOARD_Z,
               BOARD_Z + BOARD_H, BOARD_W, 0.7, sky_glow, bev=0.06)


# --------------------------------------------------------------------- build


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    scene = bpy.context.scene
    scene.unit_settings.system = "METRIC"
    scene.unit_settings.length_unit = "METERS"

    trim = material("Toy_trim")
    sand = material("Toy_sand")
    stone = material("Toy_stone")
    glass = material("Toy_glass")
    steel = material("Toy_steel")
    roofd = material("Toy_roofd")
    navy = material("Toy_navy")
    gold = material("Toy_gold")
    sky_glow = material("Toy_sky_Glow")
    white_glow = material("Toy_white_Glow")

    build_base(stone, glass)
    build_drum(trim, sand)
    build_parapet(trim, sand, gold, white_glow)
    build_roof(stone, sand, steel, roofd)
    build_entry(glass, trim, steel, white_glow)
    build_board(navy, sky_glow)
    return scene


def signed_volume(obj, dg):
    me = obj.evaluated_get(dg).to_mesh()
    me.calc_loop_triangles()
    total = 0.0
    for tri in me.loop_triangles:
        a, b, c = (me.vertices[i].co for i in tri.vertices)
        total += a.dot(b.cross(c)) / 6.0
    obj.evaluated_get(dg).to_mesh_clear()
    return total


def report():
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    inverted = []
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        o.evaluated_get(dg).to_mesh_clear()
        if signed_volume(o, dg) <= 0:
            inverted.append(o.name)
    print(f"[build] objects={len(objs)} tris={tris}")
    print(f"[build] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    print(f"[build] inverted_solids={inverted}")
    return tris


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    os.makedirs(out, exist_ok=True)

    build()
    report()

    blend = os.path.join(out, "chase-center.blend")
    glb = os.path.join(out, "chase-center.glb")
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
