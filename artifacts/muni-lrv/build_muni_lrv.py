"""Deterministic Blender build of the SF-SIM miniature Muni Metro LRV.

    blender -b --python build_muni_lrv.py -- [--out DIR] [--line n-judah]

Writes ``muni-lrv.blend`` and ``muni-lrv.glb`` next to this file (or into
``--out``). Every number in here is justified in ``REFERENCE.md``.

The subject is the Siemens **S200 SF** / SFMTA **LRV4**: 22.86 m, two sections,
one articulation, **a cab at each end** (REFERENCE.md §3), four doors per side,
a single-arm pantograph, and a red horseshoe framing each windshield
(REFERENCE.md §4.1) that the asset plan's dossier does not mention and that is
the vehicle's whole identity.

VEHICLE CONTRACT (not the landmark one — see docs/asset-plans/transit/README.md)
-------------------------------------------------------------------------------
Authored in Blender, Z up, metres, **nose toward +Y**, sitting on ``z = 0``,
centred in X/Y. The glTF exporter's Y-up conversion maps Blender ``(x, y, z)``
to glTF ``(x, z, -y)``, so this lands the model as the manifest requires:

    nose at glTF **-Z**  ·  ``min y = 0``  ·  origin centred in glTF X/Z

``min y = 0`` is the **street surface**. There are no rails in this scene, so
there is no top-of-rail question: the wheel contact patch sits on the road
exactly as a bus's tyre does.

``validate_muni_lrv.py`` re-imports the GLB into a fresh scene and
``glb_inspect.mjs`` reads the raw glTF buffers, so the convention is *verified*
rather than assumed.

EXPORTED STRAIGHT, BUILT SYMMETRIC
----------------------------------
The articulation is real geometry but the exported pose is a straight vehicle,
per the brief. Section B is section A mirrored through ``y = 0``, so the two
halves are symmetric about the joint and a future runtime that bends the train
around a curve can split them. The export therefore carries exactly three
nodes — ``LRV_Section_A``, ``LRV_Section_B``, ``LRV_Bellows`` — and gltfpack's
``-kn`` preserves those names through the meshopt intake.

STRUCTURE
---------
Every visible feature is a component function taking the ``cfg`` dict.
Component functions never create Blender objects directly: they push geometry
into a ``Part``, one per material. The Parts are then emitted as three
multi-material objects, so the GLB has three nodes and **one primitive per
material within each section** — the strongest form of the shrink stage's
"join objects sharing a material" step that is compatible with keeping the
sections separable. Flat detail quads are always hosted inside a closed solid
of their own colour, keeping signed volume positive (``mergeVehicle()`` flips
any primitive whose signed volume is negative).

Which bank a component is built into is load-bearing, not stylistic — see
``build`` for what mirroring the wrong one does to the normals.

The ``Part`` bank, the bevel helper and the stroke-lettering tables are carried
over from ``artifacts/muni-bus/build_muni_bus.py`` so the two Muni vehicles are
built by the same machinery and read as one fleet.

GLOW
----
``Toy_*_Glow`` surfaces are thin shells 3–5 cm proud of an opaque surface with
their edges buried. The app's landmark loader draws them in an unlit layer at
``0.12 + 0.95 * uNight`` (88% transparent by day); the vehicle loader currently
draws them opaque — see REPORT.md §7 and the muni-bus report, which found this
first. A proud shell over an opaque backing reads correctly under both.
Emission ships at 0.0 per contract.
"""

import math
import os
import sys

import bmesh
import bpy
from mathutils import Vector

# --------------------------------------------------------------- the vehicle

CFG = dict(
    slug="muni-lrv",
    # --- overall envelope (REFERENCE.md §2)
    length=22.86,           # 75 ft, measured at the prow (the lowest, furthest
                            # forward point) — see `CAB_LEVELS`
    width=2.65,             # 104.32 in
    # --- horizontal bands on the flank (REFERENCE.md §4.2). Seven values top to
    #     bottom; the near-black window band and the broad red band carry the
    #     contrast, and roof/body/skirt supply the supporting tonal steps.
    z_under=0.30,           # underframe underside
    z_skirt=(0.30, 1.00),   # medium grey, inset from the bodyside
    z_red=(1.00, 1.42),     # the broad red band
    z_lower=(1.42, 1.85),   # pale bodyside below the windows
    z_win=(1.85, 2.80),     # near-black window reveal
    z_glass=(1.93, 2.72),   # glazing, proud of the reveal so it is visible
    z_upper=(2.80, 3.26),   # pale bodyside above the windows
    z_roof=3.40,            # roof crown
    z_equip=3.51,           # top of the roof equipment -> body height 3.51
    ceiling_glow=(2.56, 2.66),
    # Lateral depths, measured inboard from the bodyside face at width/2.
    # The window reveal is recessed, the glazing sits proud of it, and the
    # ceiling glow sits 4 cm proud of the opaque glazing and flush with the
    # bodyside — a glow surface is 88% transparent by day, so it can never be
    # the primary surface and must never widen the vehicle.
    x_reveal=0.057,
    x_glass=0.037,
    skirt_inset=0.06,       # the skirt sits inboard of the bodyside
    # --- longitudinal layout, metres from the vehicle centre (REFERENCE.md §4.3)
    #     Doors per side, from each cab: single, double — mirrored about y=0
    #     gives the real single-double-double-single rhythm.
    door_single=(7.55, 8.85),      # 1.30 m clear, tucked behind the cab
    door_double=(2.55, 4.65),      # 2.10 m clear, toward the middle
    cab_start=8.90,         # where the cab transition leaves the parallel body
    # --- articulation (REFERENCE.md §4.5)
    bellows_half=0.30,      # a 0.60 m gap between the two sections
    bellows_inset=0.17,     # narrower than the body, so it reads as a recess
    bellows_ribs=5,
    # --- running gear: Bo'(2)'Bo' — a bogie under each cab, one under the joint
    axles=(9.90, 8.10, 0.95),      # mirrored about y=0 -> six axles, twelve wheels
    wheel_r=0.34,
    wheel_w=0.11,
    wheel_seg=8,
    wheel_x=0.98,
    # --- roof (REFERENCE.md §4.4)
    pano_y=6.30,            # a third of the way back from the cab, not midships
    pano=dict(
        base=(0.62, 3.40, 3.52),   # half-width, z of the plinth base and top
        # Arms and bar thickened well past scale: at true scale these are
        # centimetres of tube and vanish at the app's camera distance, and the
        # pantograph is the identity feature from an aerial camera.
        lower_len=1.15, upper_len=0.95, arm_r=0.105,
        bar_z=4.55, bar_half=1.06, bar_r=0.080,
    ),
    equip=(
        # (y centre, half-length, half-width, z0, z1, grille?)
        (9.10, 1.05, 1.02, 3.30, 3.46, True),
        (3.70, 1.35, 1.10, 3.30, 3.44, False),
    ),
    # --- the cab (REFERENCE.md §4.1)
    #     Plan outline per z level: (z, front_y, half_width, nose_radius).
    #     The prow at z 1.05 is the furthest-forward point and defines `length`;
    #     the front rakes back 1.13 m over the 2.35 m up to the roof crown
    #     (~26 deg), which is the windshield rake.
    cab_levels=(
        (0.30, 11.14, 1.16, 0.62),
        (1.05, 11.418, 1.27, 0.70),
        (1.55, 11.36, 1.325, 0.74),
        (2.10, 11.14, 1.325, 0.78),
        (2.75, 10.82, 1.30, 0.80),
        (3.15, 10.55, 1.20, 0.78),
        (3.40, 10.28, 0.96, 0.66),
    ),
    # Cab elevation, bottom to top. Everything here must stay under the 3.40 m
    # roof crown declared in `cab_levels`, or the roof cap inverts.
    fascia_z=(1.00, 1.86),       # black lower front, below the glass
    windshield_z=(1.94, 2.90),   # the glass, on the raked front
    sign_z=(2.96, 3.16),         # destination readout, above the windshield
    horseshoe_top=(3.16, 3.30),  # the frame's top bar, above the sign
    cap_z=(3.30, 3.395),         # white roof cap over the cab
    horseshoe_proud=0.035,
    head_z=(1.24, 1.46),
    bevel=0.06,
)

LINES = {
    # Surface alignments a player can actually see — the subway segments are
    # invisible in this app (transit README, "Why five").
    "n-judah": ("N", "JUDAH"),
    "j-church": ("J", "CHURCH"),
    "t-third": ("T", "THIRD"),
}
FLEET_NUMBER = "2059"   # in the verified 2001-2249 range; photographed on the L.

PALETTE_HEX = dict(
    Toy_white="f2efe8",        # roof and cab cap — the lightest value
    Toy_lrvbody="dcdcd8",      # pale silver bodyside, one step below the roof
    Toy_steel="9aa0a6",        # skirt, roof equipment, pantograph
    Toy_munired="c1272d",      # = muni-bus's Toy_munired, so the two match
    Toy_ink="2e2b28",
    Toy_glass="26405e",        # = muni-bus's Toy_glass
    Toy_mustard_Glow="d9a441",
    Toy_white_Glow="f7f4ec",
    Toy_red_Glow="c4453c",
)

MATERIALS = dict(
    white="Toy_white", body="Toy_lrvbody", steel="Toy_steel",
    munired="Toy_munired", ink="Toy_ink", glass="Toy_glass",
    mustard_glow="Toy_mustard_Glow", white_glow="Toy_white_Glow",
    red_glow="Toy_red_Glow",
)


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
    rgb = PALETTE[name]
    mat = bpy.data.materials.new(name)
    mat.use_nodes = True
    bsdf = mat.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*rgb, 1.0)
    bsdf.inputs["Roughness"].default_value = 0.85
    bsdf.inputs["Metallic"].default_value = 0.0
    if name.endswith("_Glow"):
        # Flagged for the app's night layer; emission stays 0.0 in the asset.
        # Base Color is copied into Emission Color so a night *preview* that
        # raises Emission Strength lights the surface its own colour instead of
        # white (a glTF emissiveFactor of (0,0,0) otherwise imports as white).
        bsdf.inputs["Emission Color"].default_value = (*rgb, 1.0)
        bsdf.inputs["Emission Strength"].default_value = 0.0
    mat.diffuse_color = (*[c ** (1 / 2.2) for c in rgb], 1.0)
    mat.roughness = 0.85
    # Blender 5.x removed Material.blend_method in favour of surface_render_method.
    if hasattr(mat, "surface_render_method"):
        mat.surface_render_method = "DITHERED"
    elif hasattr(mat, "blend_method"):
        mat.blend_method = "OPAQUE"
    return mat


# ------------------------------------------------------------- geometry bank


class Part:
    """Accumulates geometry for exactly one material, emits one object."""

    def __init__(self, mat_name):
        self.mat = mat_name
        self.verts = []
        self.faces = []

    def _push(self, verts, faces):
        base = len(self.verts)
        self.verts.extend(verts)
        self.faces.extend([tuple(base + i for i in f) for f in faces])

    def quad(self, a, b, c, d):
        self._push([a, b, c, d], [(0, 1, 2, 3)])

    def ngon(self, pts):
        self._push(list(pts), [tuple(range(len(pts)))])

    def box(self, centre, size, bevel=0.0, segments=2):
        cx, cy, cz = centre
        hx, hy, hz = (s / 2.0 for s in size)
        verts = [
            (cx - hx, cy - hy, cz - hz), (cx + hx, cy - hy, cz - hz),
            (cx + hx, cy + hy, cz - hz), (cx - hx, cy + hy, cz - hz),
            (cx - hx, cy - hy, cz + hz), (cx + hx, cy - hy, cz + hz),
            (cx + hx, cy + hy, cz + hz), (cx - hx, cy + hy, cz + hz),
        ]
        faces = [(3, 2, 1, 0), (4, 5, 6, 7), (0, 1, 5, 4),
                 (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
        if bevel > 0.0:
            verts, faces = _bevelled(verts, faces, bevel, segments)
        self._push(verts, faces)

    def span(self, x, y, z, bevel=0.0, segments=2):
        """Box from explicit (lo, hi) ranges — how most of this model is written.

        Ranges are sorted, so a caller that derives a range from a signed `end`
        cannot accidentally hand over an inside-out box.
        """
        x, y, z = sorted(x), sorted(y), sorted(z)
        self.box(
            ((x[0] + x[1]) / 2.0, (y[0] + y[1]) / 2.0, (z[0] + z[1]) / 2.0),
            (x[1] - x[0], y[1] - y[0], z[1] - z[0]),
            bevel, segments,
        )

    def loft(self, ring_lo, ring_hi, cap_lo=True, cap_hi=True):
        """Solid between two equal-length closed rings of 3D points."""
        n = len(ring_lo)
        verts = list(ring_lo) + list(ring_hi)
        faces = [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
        if cap_lo:
            faces.append(tuple(range(n - 1, -1, -1)))
        if cap_hi:
            faces.append(tuple(range(n, 2 * n)))
        self._push(verts, faces)

    def tube(self, rings):
        """Loft a sequence of rings, capping only the two ends. This is what
        builds the cab: each ring is a plan outline at one z level, so the nose
        rakes back and rounds in plan at the same time."""
        for i in range(len(rings) - 1):
            self.loft(rings[i], rings[i + 1],
                      cap_lo=(i == 0), cap_hi=(i == len(rings) - 2))

    def cylinder(self, centre, radius, half_len, segments, axis="x", a0=None):
        """`a0` defaults to -pi/2, which puts a vertex at the bottom of the
        section. On a wheel that is what makes `min z` land on exactly 0
        instead of the sagitta of the polygon's lowest chord."""
        cx, cy, cz = centre
        if a0 is None:
            a0 = -math.pi / 2.0
        lo, hi = [], []
        for i in range(segments):
            a = 2.0 * math.pi * i / segments + a0
            u, v = radius * math.cos(a), radius * math.sin(a)
            if axis == "x":
                lo.append((cx - half_len, cy + u, cz + v))
                hi.append((cx + half_len, cy + u, cz + v))
            elif axis == "y":
                lo.append((cx + u, cy - half_len, cz + v))
                hi.append((cx + u, cy + half_len, cz + v))
            else:  # z
                lo.append((cx + u, cy + v, cz - half_len))
                hi.append((cx + u, cy + v, cz + half_len))
        self.loft(lo, hi)

    def capsule(self, a, b, radius, segments=6):
        """A round bar between two points — the pantograph arms."""
        a, b = Vector(a), Vector(b)
        axis = (b - a)
        if axis.length < 1e-6:
            return
        axis = axis.normalized()
        up = Vector((0, 0, 1)) if abs(axis.z) < 0.9 else Vector((1, 0, 0))
        u = axis.cross(up).normalized()
        v = axis.cross(u).normalized()
        lo, hi = [], []
        for i in range(segments):
            ang = 2.0 * math.pi * i / segments
            off = u * (radius * math.cos(ang)) + v * (radius * math.sin(ang))
            lo.append(tuple(a + off))
            hi.append(tuple(b + off))
        self.loft(lo, hi)

    def append(self, other):
        """Fold another Part's geometry into this one. Used to merge the
        mirrored banks — see `build`."""
        base = len(self.verts)
        self.verts.extend(other.verts)
        self.faces.extend([tuple(base + i for i in f) for f in other.faces])

    def mirror_x(self):
        """Duplicate everything added so far across x=0. Both flanks, one call."""
        n = len(self.verts)
        self.verts.extend([(-x, y, z) for x, y, z in self.verts])
        self.faces.extend([tuple(n + i for i in reversed(f)) for f in list(self.faces)])

    def mirror_y(self):
        """Duplicate everything added so far across y=0 — section A becomes
        section B. Called AFTER the sided geometry is complete and BEFORE any
        lettering, which must never be mirrored (it would read backwards)."""
        n = len(self.verts)
        self.verts.extend([(x, -y, z) for x, y, z in self.verts])
        self.faces.extend([tuple(n + i for i in reversed(f)) for f in list(self.faces)])

    def flip_y(self):
        """Reflect this Part through y = 0 IN PLACE.

        Distinct from `mirror_y`, which duplicates. Section B is a reflection
        of section A, not section A plus its reflection — using the duplicating
        form here silently lays a whole second vehicle on top of the first.
        """
        self.verts = [(x, -y, z) for x, y, z in self.verts]
        self.faces = [tuple(reversed(f)) for f in self.faces]

    def emit(self, name=None):
        if not self.faces:
            return None
        name = name or self.mat
        mesh = bpy.data.meshes.new(name)
        mesh.from_pydata([Vector(v) for v in self.verts], [], self.faces)
        mesh.materials.append(material(self.mat))
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


def emit_group(name, bank, order):
    """Emit one Blender object carrying every material in `bank`.

    The brief asks for exactly three named nodes — `LRV_Section_A`,
    `LRV_Section_B`, `LRV_Bellows` — so a future runtime that bends the train
    around a curve can split it, and gltfpack's `-kn` preserves those names
    through the meshopt intake. glTF allows one mesh to hold several
    primitives, one per material, so three nodes and one-primitive-per-material
    are not in conflict: each section exports as a single node whose mesh has
    one primitive per `Toy_*` material it uses.
    """
    verts = []
    faces = []
    mat_index = []
    slots = []
    for key in order:
        part = bank[key]
        if not part.faces:
            continue
        slot = len(slots)
        slots.append(part.mat)
        base = len(verts)
        verts.extend(part.verts)
        for f in part.faces:
            faces.append(tuple(base + i for i in f))
            mat_index.append(slot)
    if not faces:
        return None
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata([Vector(v) for v in verts], [], faces)
    for m in slots:
        mesh.materials.append(material(m))
    mesh.validate()
    for poly, idx in zip(mesh.polygons, mat_index):
        poly.material_index = idx
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    bm = bmesh.new()
    bm.from_mesh(mesh)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bm.to_mesh(mesh)
    bm.free()
    mesh.shade_flat()
    return obj


def _bevelled(verts, faces, width, segments):
    """Style-bible §4 edge softening, done on loose geometry before banking."""
    bm = bmesh.new()
    bmv = [bm.verts.new(v) for v in verts]
    for f in faces:
        try:
            bm.faces.new([bmv[i] for i in f])
        except ValueError:
            pass
    bm.verts.index_update()
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    bmesh.ops.bevel(
        bm, geom=list(bm.verts) + list(bm.edges), offset=width, segments=segments,
        profile=0.5, affect="EDGES", clamp_overlap=True,
    )
    bm.verts.index_update()
    out_v = [tuple(v.co) for v in bm.verts]
    out_f = [tuple(v.index for v in f.verts) for f in bm.faces]
    bm.free()
    return out_v, out_f


# ------------------------------------------------------------ stroke lettering
#
# Destination glyphs and fleet numbers are extruded geometry, never a texture.
# Each stroke is one quad hosted inside a closed solid of the same colour, so a
# route name costs tens of triangles instead of the hundreds an extruded font
# would. Tables carried over from build_muni_bus.py.

SEG7 = {  # 7-segment: top, top-l, top-r, mid, bot-l, bot-r, bot
    "0": "ABCEFG", "1": "CF", "2": "ACDEG", "3": "ACDFG", "4": "BCDF",
    "5": "ABDFG", "6": "ABDEFG", "7": "ACF", "8": "ABCDEFG", "9": "ABCDFG",
}
SEG_RECT = {
    "A": (0.00, 0.86, 1.00, 1.00), "B": (0.00, 0.50, 0.16, 0.94),
    "C": (0.84, 0.50, 1.00, 0.94), "D": (0.00, 0.43, 1.00, 0.57),
    "E": (0.00, 0.06, 0.16, 0.50), "F": (0.84, 0.06, 1.00, 0.50),
    "G": (0.00, 0.00, 1.00, 0.14),
}
LETTER = {
    "A": ["B", "C", "A", "D", (0.00, 0.00, 0.16, 0.50), (0.84, 0.00, 1.00, 0.50)],
    "B": ["A", "B", "D", "E", "G", "C", "F"],
    "C": ["A", "B", "E", "G"],
    "D": ["A", "B", "E", "G", "C", "F"],
    "E": ["A", "B", "D", "E", "G"],
    "H": ["B", "C", "D", "E", "F"],
    "I": [(0.42, 0.00, 0.58, 1.00)],
    "J": ["C", "F", "G", (0.00, 0.00, 0.16, 0.30)],
    "L": ["B", "E", "G"],
    "N": ["B", "C", "E", "F", "A"],
    "R": ["A", "B", "C", "D", "E", (0.62, 0.00, 0.84, 0.46)],
    "T": ["A", (0.42, 0.00, 0.58, 0.90)],
    "U": ["B", "C", "E", "F", "G"],
    " ": [],
}


def _rects(ch):
    if ch in SEG7:
        return [SEG_RECT[s] for s in SEG7[ch]]
    return [SEG_RECT[r] if isinstance(r, str) else r for r in LETTER.get(ch, [])]


def text_width(text, cell_w, gap):
    return len(text) * cell_w + max(0, len(text) - 1) * gap


def front_text(part, text, origin, cell, gap, y_plane, end=1):
    """Lay `text` across a cab FACE on the plane y = y_plane * end.

    A viewer standing in front of the +Y cab sees +X on their LEFT, so text
    advances in -X there and in +X at the -Y cab. Getting this wrong ships a
    mirrored destination sign — the class of error that survives to production
    because nobody renders the front elevation.

    origin = (x of the first glyph's leading edge, z of the baseline).
    """
    cw, chh = cell
    x = origin[0] * end
    for ch in text:
        for (rx0, rz0, rx1, rz1) in _rects(ch):
            xa, xb = x - end * rx0 * cw, x - end * rx1 * cw
            za, zb = origin[1] + rz0 * chh, origin[1] + rz1 * chh
            part.quad((xa, y_plane * end, za), (xb, y_plane * end, za),
                      (xb, y_plane * end, zb), (xa, y_plane * end, zb))
        x -= end * (cw + gap)


def side_text(part, text, y_start, z0, cell, gap, x_plane, side):
    """Same stroke font laid on a FLANK (the plane x = x_plane * side).

    `side` is +1 for the right flank, -1 for the left. Advancing by `+side`
    makes the text read nose-to-tail on both flanks and leaves the winding
    pointing outward on each. Built explicitly per flank rather than mirrored:
    `mirror_x()` would hand back a backwards fleet number.
    """
    cw, chh = cell
    x = x_plane * side
    y = y_start
    for ch in text:
        for (rx0, rz0, rx1, rz1) in _rects(ch):
            ya, yb = y + side * rx0 * cw, y + side * rx1 * cw
            za, zb = z0 + rz0 * chh, z0 + rz1 * chh
            part.quad((x, ya, za), (x, yb, za), (x, yb, zb), (x, ya, zb))
        y += side * (cw + gap)


# ---------------------------------------------------------------- cab outline


def cab_outline(front_y, half_w, radius, back_y, segments=3):
    """One plan outline of the cab at a single z level, as a closed ring.

    A rectangle from `back_y` forward, with the nose corners rounded off by
    `radius` through `segments` chamfer steps. Faceted on purpose: the style
    bible wants chamfered planes, and a lofted surface would eat the budget
    (asset plan §2.6).

    Returned counter-clockwise seen from above, starting at the back on +X.
    """
    pts = [(half_w, back_y)]
    nose = front_y - radius
    pts.append((half_w, nose))
    for i in range(1, segments + 1):
        a = (math.pi / 2.0) * i / (segments + 1)
        pts.append((half_w - radius * (1 - math.cos(a)) if half_w > radius
                    else half_w * math.cos(a),
                    nose + radius * math.sin(a)))
    pts.append((0.0, front_y))
    mirrored = [(-x, y) for x, y in reversed(pts[:-1])]
    return pts + mirrored


def cab_rings(cfg, end=1):
    """The cab as a stack of plan outlines, one per z level."""
    back = cfg["cab_start"]
    rings = []
    for z, front_y, half_w, radius in cfg["cab_levels"]:
        ring = cab_outline(front_y, half_w, radius, back)
        rings.append([(x, y * end, z) for x, y in ring])
    return rings


def cab_level_at(cfg, z):
    """Interpolate (front_y, half_width, nose_radius) at any height."""
    levels = cfg["cab_levels"]
    lo, hi = levels[0], levels[-1]
    for a, b in zip(levels, levels[1:]):
        if a[0] <= z <= b[0]:
            lo, hi = a, b
            break
    span = (hi[0] - lo[0]) or 1.0
    t = min(1.0, max(0.0, (z - lo[0]) / span))
    return (lo[1] + (hi[1] - lo[1]) * t,
            lo[2] + (hi[2] - lo[2]) * t,
            lo[3] + (hi[3] - lo[3]) * t)


def nose_arc(cfg, z, shrink=0.0, y_push=0.0, end=1, trim=0):
    """The rounded NOSE run of the cab outline at height `z` — the front-facing
    surface only.

    `trim` drops that many chamfer steps from each end. This is the whole point
    of the function: with `trim = 0` the run reaches all the way back to where
    the nose radius meets the straight flank, so a band built on it wraps
    almost a metre down each side of the vehicle. The first render pass did
    exactly that and put the destination sign and the roof cap down both
    flanks as stripes. Front features use `trim >= 1`.

    `shrink` pulls the run inboard, `y_push` pushes it forward along the
    vehicle axis. Everything on the cab face — windshield, horseshoe, sign
    hood, fascia, roof cap — is built from this one run, so they all follow the
    same raked, rounded surface instead of floating on a guessed plane.
    """
    front_y, half_w, radius = cab_level_at(cfg, z)
    ring = cab_outline(front_y + y_push, max(0.05, half_w - shrink),
                       max(0.05, radius - shrink * 0.5), cfg["cab_start"])
    nose = front_y + y_push - max(0.05, radius - shrink * 0.5)
    arc = [p for p in ring if p[1] >= nose - 1e-4]
    if trim:
        arc = arc[trim : len(arc) - trim] or arc
    return [(x, y * end, z) for x, y in arc]


def surface_y_at(cfg, z, x_abs):
    """How far forward the cab surface reaches at height `z` and offset |x|.

    Returned for the +Y cab; callers scale by `end`. Used to seat the lamps on
    the curved fascia instead of on a guessed plane.
    """
    arc = [p for p in nose_arc(cfg, z, 0.0, 0.0, 1, trim=0) if p[0] >= -1e-6]
    arc.sort(key=lambda p: p[0])
    x_abs = min(max(x_abs, arc[0][0]), arc[-1][0])
    for a, b in zip(arc, arc[1:]):
        if a[0] <= x_abs <= b[0]:
            span = (b[0] - a[0]) or 1.0
            t = (x_abs - a[0]) / span
            return a[1] + (b[1] - a[1]) * t
    return arc[-1][1]


def _emit_quads(part, quads, end):
    for q in quads:
        part.quad(*(q if end > 0 else tuple(reversed(q))))


def _z_steps(cfg, z0, z1):
    """The heights a cab-face feature must be subdivided at.

    The cab shell is a chain of loft segments between the declared
    `cab_levels`, so it BENDS at each of those heights. A feature drawn as one
    straight row between z0 and z1 is a chord across that bend and dives inside
    the shell in the middle of its span — which is how the first build lost the
    windshield and the black fascia into the bodywork while their top and
    bottom edges still poked out. Subdividing at the same heights the shell
    bends at keeps every feature exactly on the surface.
    """
    inner = sorted(lv[0] for lv in cfg["cab_levels"] if z0 < lv[0] < z1)
    return [z0] + inner + [z1]


def surface_band(part, cfg, z0, z1, shrink, y_push, end, trim=1, segs=None):
    """A band of quads following the cab's front surface between two heights.

    `segs` restricts which chamfer segments are emitted, which is how the
    horseshoe's two A-pillar legs are drawn from the same run as the glass
    they frame.
    """
    steps = _z_steps(cfg, z0, z1)
    for za, zb in zip(steps, steps[1:]):
        lo = nose_arc(cfg, za, shrink, y_push, end, trim)
        hi = nose_arc(cfg, zb, shrink, y_push, end, trim)
        n = min(len(lo), len(hi))
        idx = range(n - 1) if segs is None else [i for i in segs if 0 <= i < n - 1]
        _emit_quads(part, [(lo[i], lo[i + 1], hi[i + 1], hi[i]) for i in idx], end)


def surface_slab(part, cfg, z0, z1, shrink_out, shrink_in, y_out, y_in, end,
                 trim=1, segs=None):
    """A closed slab between two front-surface bands — used for the red
    horseshoe, the sign hood, the fascia and the roof cap, so each is a solid
    with positive signed volume rather than a floating sheet.

    Subdivided at the shell's own bend heights for the reason in `_z_steps`.
    """
    steps = _z_steps(cfg, z0, z1)
    for k, (za, zb) in enumerate(zip(steps, steps[1:])):
        o_lo = nose_arc(cfg, za, shrink_out, y_out, end, trim)
        o_hi = nose_arc(cfg, zb, shrink_out, y_out, end, trim)
        i_lo = nose_arc(cfg, za, shrink_in, y_in, end, trim)
        i_hi = nose_arc(cfg, zb, shrink_in, y_in, end, trim)
        n = min(len(o_lo), len(o_hi), len(i_lo), len(i_hi))
        idx = list(range(n - 1)) if segs is None else [i for i in segs if 0 <= i < n - 1]
        quads = []
        for i in idx:
            quads += [
                (o_lo[i], o_lo[i + 1], o_hi[i + 1], o_hi[i]),
                (i_lo[i + 1], i_lo[i], i_hi[i], i_hi[i + 1]),
            ]
            # Cap the run's two long edges only on the first/last subdivision,
            # so interior rows stay watertight against their neighbours.
            if k == 0:
                quads.append((o_lo[i], i_lo[i], i_lo[i + 1], o_lo[i + 1]))
            if k == len(steps) - 2:
                quads.append((o_hi[i + 1], i_hi[i + 1], i_hi[i], o_hi[i]))
        # Close the run's two ends so the slab is a solid, not an open shell: an
        # open shell's signed volume is meaningless and `mergeVehicle()` flips
        # any primitive whose signed volume is negative.
        if idx:
            first, last = idx[0], idx[-1] + 1
            quads += [
                (o_lo[first], o_hi[first], i_hi[first], i_lo[first]),
                (i_lo[last], i_hi[last], o_hi[last], o_lo[last]),
            ]
        _emit_quads(part, quads, end)


# ---------------------------------------------------------------- components


def body_shell(cfg, p):
    """The parallel-sided body between the articulation and each cab, banded
    into the five horizontal values of REFERENCE.md §4.2."""
    hw = cfg["width"] / 2.0
    y0, y1 = cfg["bellows_half"], cfg["cab_start"]
    b = cfg["bevel"]
    p["body"].span((-hw, hw), (y0, y1), cfg["z_lower"], bevel=b, segments=1)
    p["body"].span((-hw, hw), (y0, y1), cfg["z_upper"], bevel=b, segments=1)
    p["munired"].span((-hw, hw), (y0, y1), cfg["z_red"], bevel=b, segments=1)
    # Window reveal: a dark recess. The glazing sits PROUD of it (see
    # `glazing`), not inside it — a reveal that swallows its own glass renders
    # as a solid black slab, which is what the first build did.
    r = hw - cfg["x_reveal"]
    p["ink"].span((-r, r), (y0, y1), cfg["z_win"])
    p["white"].span((-hw + 0.03, hw - 0.03), (y0, y1), (cfg["z_upper"][1], cfg["z_roof"]),
                    bevel=b, segments=1)
    # Skirt, inboard of the bodyside so the shadow line reads.
    s = hw - cfg["skirt_inset"]
    p["steel"].span((-s, s), (y0, y1), cfg["z_skirt"], bevel=0.04, segments=1)


def glazing(cfg, p):
    """One continuous glazed run per section, standing proud of the dark
    reveal so the window band reads as glass framed by ink rather than as a
    black slab. The doors interrupt it with mullions, not with gaps."""
    hw = cfg["width"] / 2.0 - cfg["x_glass"]
    p["glass"].span((-hw, hw), (cfg["bellows_half"] + 0.05, cfg["cab_start"] - 0.04),
                    cfg["z_glass"])


def window_runs(cfg):
    """Glazed runs along one section, split at the door mullions — used by the
    interior ceiling strip so the glow is broken where the doors are."""
    edges = [cfg["bellows_half"] + 0.10]
    for lo, hi in sorted((cfg["door_double"], cfg["door_single"])):
        edges.extend([lo - 0.04, hi + 0.04])
    edges.append(cfg["cab_start"] - 0.08)
    return [(edges[i], edges[i + 1]) for i in range(0, len(edges) - 1, 2)]


def doors(cfg, p):
    """Four per side: a single behind each cab, a double toward the middle
    (REFERENCE.md §4.3 — SFMTA's own arrangement, symmetric about the
    articulation, NOT evenly spaced).

    Drawn as dark mullions down each leaf edge plus a shallow threshold, so the
    pale bodyside and the red band run on across the door the way they do on
    the real vehicle. The first build made each door a full-height ink slab,
    which chopped the livery into pieces and made the flank read as four black
    holes.
    """
    hw = cfg["width"] / 2.0
    z0 = cfg["z_red"][0] + 0.03
    z1 = cfg["z_win"][1]
    for lo, hi in (cfg["door_single"], cfg["door_double"]):
        edges = [lo, hi] + ([(lo + hi) / 2.0] if hi - lo > 1.6 else [])
        for y in edges:
            p["ink"].span((hw - 0.030, hw + 0.004), (y - 0.035, y + 0.035), (z0, z1))
        # A shallow threshold under the leaves so the opening reads at the sill.
        p["ink"].span((hw - 0.030, hw + 0.004), (lo, hi), (z0, z0 + 0.055))


def livery_details(cfg, p):
    """The `muni` worm, low on the pale bodyside near each cab.

    Four convex quads, never one concave outline: the muni-bus build found that
    a concave worm either squares off into crenellation or self-intersects and
    triangulates into confetti at the 2-4 px it occupies on screen.
    """
    hw = cfg["width"] / 2.0
    y = 6.55
    z0 = cfg["z_lower"][0] + 0.10
    h = 0.30
    w = 0.17
    for i in range(4):
        y0 = y + i * (w + 0.035)
        top = z0 + h * (1.0 if i % 2 == 0 else 0.62)
        p["munired"].quad((hw + 0.004, y0, z0), (hw + 0.004, y0 + w, z0),
                          (hw + 0.004, y0 + w, top), (hw + 0.004, y0, top))


def bellows(cfg, p):
    """The articulation: a dark ribbed recess, narrower than the body, carried
    across the roofline as a real step so it reads from directly above
    (REFERENCE.md §4.5). The app's camera looks down at 42 degrees, where a
    bellows that only reads in side elevation is invisible."""
    hb = cfg["bellows_half"]
    hw = cfg["width"] / 2.0 - cfg["bellows_inset"]
    z0 = cfg["z_skirt"][0]
    z1 = cfg["z_roof"] - 0.06
    p["ink"].span((-hw, hw), (-hb, hb), (z0, z1))
    n = cfg["bellows_ribs"]
    for i in range(n):
        t = -hb + (i + 0.5) * (2 * hb / n)
        r = 0.045
        p["ink"].span((-hw - 0.05, hw + 0.05), (t - r, t + r), (z0 + 0.10, z1))


def wheels(cfg, p):
    """Twelve wheels on six axles — Bo'(2)'Bo', a bogie under each cab and one
    under the articulation. Set behind the skirt, showing only the 0.30 m
    below it."""
    r = cfg["wheel_r"]
    for y in cfg["axles"]:
        for sx in (-1, 1):
            p["ink"].cylinder((sx * cfg["wheel_x"], y, r), r, cfg["wheel_w"],
                              cfg["wheel_seg"], axis="x")


def underframe(cfg, p):
    """A dark underframe so the gap between the bogies is not daylight.

    Built for one section only — it is mirrored with the rest of the bank.
    """
    p["ink"].span((-0.86, 0.86), (cfg["bellows_half"], 10.35),
                  (0.26, cfg["z_skirt"][0] + 0.04))


def roof_equipment(cfg, p):
    """Two low pale masses with darker grille faces, fore and aft of the
    pantograph (REFERENCE.md §4.4). Composed by value, not part count: the roof
    is the surface the app's camera sees most of."""
    for y, hly, hlx, z0, z1, grille in cfg["equip"]:
        p["steel"].span((-hlx, hlx), (y - hly, y + hly), (z0, z1),
                        bevel=0.04, segments=1)
        if grille:
            for i in range(3):
                t = y - hly + 0.30 + i * 0.32
                p["ink"].span((-hlx + 0.10, hlx - 0.10), (t - 0.09, t + 0.09),
                              (z1 - 0.015, z1 + 0.008))


def pantograph(cfg, p):
    """A single-arm Z pantograph, raised. Arms thickened well past scale and
    the contact bar exaggerated — at true scale these are centimetres of tube
    and vanish at the app's camera distance, and this is the identity feature
    from an aerial camera (asset plan §2.6, §2.11)."""
    d = cfg["pano"]
    y = cfg["pano_y"]
    hw, z_base, z_top = d["base"]
    # Insulator plinth.
    p["ink"].span((-hw, hw), (y - hw, y + hw), (z_base, z_top))
    knee = (0.0, y - d["lower_len"] * 0.55, z_top + d["lower_len"])
    bar_z = d["bar_z"]
    for sx in (-1, 1):
        root = (sx * 0.34, y + 0.16, z_top)
        p["steel"].capsule(root, knee, d["arm_r"], segments=5)
    p["steel"].capsule(knee, (0.0, y + d["upper_len"] * 0.45, bar_z - 0.06),
                       d["arm_r"] * 0.92, segments=5)
    # The contact bar: what actually reads from above.
    p["steel"].cylinder((0.0, y + d["upper_len"] * 0.45, bar_z), d["bar_r"],
                        d["bar_half"], 6, axis="x")


def cab(cfg, p, end=1):
    """One cab. Built for `end` = +1 (nose at +Y) and again for -1, rather than
    mirrored, because the destination sign and fleet number must not reverse.

    The vehicle is double-ended (REFERENCE.md §3): there is no blank rear, and
    this geometry is what the front AND rear elevations both show.
    """
    rings = cab_rings(cfg, end)
    p["body"].tube(rings)

    # --- the red horseshoe (REFERENCE.md §4.1) — the vehicle's identity.
    #     A proud frame following the raked front surface: across the top above
    #     the sign, down both A-pillars, turning in under the glass.
    pr = cfg["horseshoe_proud"]
    zs0, zs1 = cfg["sign_z"]
    zw0, zw1 = cfg["windshield_z"]
    ht0, ht1 = cfg["horseshoe_top"]

    # EVERY feature on the cab face is a shell standing PROUD of the shell
    # along +y, in a fixed stacking order. A feature built flush (y_push = 0)
    # is coplanar with the closed cab solid and disappears into it — the first
    # build lost the windshield and the whole black fascia that way. Proud
    # along +y only, never outboard in x: pushing sideways would widen the
    # vehicle past its real 2.65 m.
    #
    #   fascia / cap  +0.012   glass  +0.016   sign hood  +0.014
    #   sign glow     +0.048   glyphs +0.062   horseshoe  +0.040
    #
    # The windshield occupies the flat-facing middle of the nose run (trim 2);
    # the frame's two A-pillar legs are the two chamfer segments outboard of it
    # on each side, so the red lands exactly where the glass ends.
    probe = nose_arc(cfg, (zw0 + zw1) / 2.0, 0.0, 0.0, end, trim=0)
    n = len(probe)
    pillars = [0, 1, n - 3, n - 2]

    surface_slab(p["munired"], cfg, ht0, ht1, 0.0, 0.03, 0.040, -0.02, end, trim=1)
    surface_slab(p["munired"], cfg, zw0 - 0.09, zw0, 0.0, 0.03, 0.040, -0.02, end, trim=1)
    surface_slab(p["munired"], cfg, zw0, zw1, 0.0, 0.03, 0.040, -0.02, end,
                 trim=0, segs=pillars)

    # --- windshield: one dark pane, framed by the horseshoe standing 2.4 cm
    #     further proud than it.
    surface_band(p["glass"], cfg, zw0 + 0.015, zw1 - 0.015, 0.018, 0.016, end, trim=2)

    # --- destination sign: an opaque ink hood; the glowing face is added by
    #     destination_sign() so it sits proud of this backing.
    surface_slab(p["ink"], cfg, zs0, zs1, 0.0, 0.05, 0.014, -0.04, end, trim=2)

    # --- lower fascia, black, below the glass.
    surface_slab(p["ink"], cfg, cfg["fascia_z"][0], cfg["fascia_z"][1],
                 0.0, 0.055, 0.012, -0.05, end, trim=1)

    # --- white roof cap over the top of the cab.
    surface_slab(p["white"], cfg, cfg["cap_z"][0], cfg["cap_z"][1],
                 0.0, 0.05, 0.012, -0.04, end, trim=1)

    # --- grey valance below the fascia, carrying the body's skirt value around
    #     the cab, and a simple coupler block. The plan allows no coupler
    #     hardware beyond a block, and at 1.6x from 120 m that is all it is.
    surface_slab(p["steel"], cfg, cfg["z_skirt"][0], cfg["fascia_z"][0],
                 0.0, 0.05, 0.010, -0.04, end, trim=1)
    # Seated so its nose stays behind the prow — the coupler must not become
    # the vehicle's longest point and quietly redefine `length`.
    y_cpl = cab_level_at(cfg, 0.62)[0] - 0.06
    p["ink"].box((0.0, y_cpl * end, 0.60), (0.46, 0.42, 0.30), bevel=0.05,
                 segments=1)

    # --- the red sweep down the cab flank, meeting the body's red band.
    sweep(cfg, p["munired"], end)


def sweep(cfg, part, end):
    """The red band's rise at the cab: on the real vehicle the low flank band
    runs forward and turns up into the horseshoe along a diagonal
    (REFERENCE.md §4.2).

    Built as horizontal strips rather than one quad, because the cab's
    half-width varies with height: a single flat quad at the body's full
    half-width floats off the surface where the cab tucks in low down.
    """
    y0 = cfg["cab_start"]
    y1 = y0 + 1.60
    z_lo, z_hi = cfg["z_red"][0], cfg["z_red"][1] + 0.78
    strips = 5
    for sx in (-1, 1):
        for i in range(strips):
            za = z_lo + (z_hi - z_lo) * i / strips
            zb = z_lo + (z_hi - z_lo) * (i + 1) / strips
            # The diagonal: the band's forward edge climbs as it runs forward.
            ta = 1.0 - i / strips
            tb = 1.0 - (i + 1) / strips
            ya = y0 + (y1 - y0) * (1.0 - ta)
            yb = y0 + (y1 - y0) * (1.0 - tb)
            xa = sx * (cab_level_at(cfg, za)[1] + 0.004)
            xb = sx * (cab_level_at(cfg, zb)[1] + 0.004)
            quad = ((xa, y0 * end, za), (xa, (y1 - (y1 - ya)) * end, za),
                    (xb, (y1 - (y1 - yb)) * end, zb), (xb, y0 * end, zb))
            part.quad(*(quad if (sx * end) > 0 else tuple(reversed(quad))))


def lights(cfg, p, end):
    """Headlight and tail-light shells, proud of an opaque ink housing. The
    vehicle is double-ended, so BOTH ends carry both: whichever cab leads shows
    white forward and red astern."""
    z0, z1 = cfg["head_z"]
    for sx in (-1, 1):
        for material_key, dz, dw in (("white_glow", 0.0, 0.34), ("red_glow", -0.27, 0.20)):
            za, zb = z0 + dz, z1 + dz
            lo, hi = sorted((sx * 0.44, sx * (0.44 + dw)))
            # Take the surface at the OUTBOARD edge, which is the most recessed
            # point the lamp spans, so the whole lamp face clears the bodywork.
            ys = surface_y_at(cfg, (za + zb) / 2.0, max(abs(lo), abs(hi)))
            y = ys * end
            # Opaque ink housing first, then the glow shell 3.5 cm PROUD of it
            # with its edges buried: a glow surface is 88% transparent by day
            # under the app's night layer, so it can never be a primary surface.
            p["ink"].span((lo - 0.05, hi + 0.05), (y - 0.20 * end, y + 0.012 * end),
                          (za - 0.05, zb + 0.05))
            p[material_key].span((lo, hi), (y - 0.05 * end, y + 0.047 * end), (za, zb))


def destination_sign(cfg, p, line, end):
    """Amber field, ink glyphs standing proud of it — the inversion the
    muni-bus build validated. It keeps the glow as one clean shell instead of
    dozens of tiny ones that vanish at 12% day opacity, and costs tens of
    triangles where an extruded font would cost hundreds."""
    route, dest = LINES[line]
    text = f"{route} {dest}"
    zs0, zs1 = cfg["sign_z"]
    # The glowing face, 3.4 cm proud of the opaque ink hood.
    surface_band(p["mustard_glow"], cfg, zs0 + 0.025, zs1 - 0.025, 0.030, 0.048, end, trim=2)
    # Glyphs sit on the flattest part of the sign face, 1.4 cm proud of the
    # glowing shell so they read as blocked-out dots against a lit field.
    arc = nose_arc(cfg, (zs0 + zs1) / 2.0, 0.036, 0.062, end, trim=2)
    y_plane = max(abs(pt[1]) for pt in arc)
    cell = (0.115, 0.15)
    gap = 0.035
    width = text_width(text, cell[0], gap)
    front_text(p["ink"], text, (width / 2.0, zs0 + 0.05), cell, gap, y_plane, end)


def fleet_number(cfg, p, end):
    """The car number, black on the pale bodyside just under the roof edge,
    built per flank so neither reads backwards."""
    label = FLEET_NUMBER + ("A" if end > 0 else "B")
    cell = (0.13, 0.19)
    gap = 0.04
    x = cfg["width"] / 2.0 + 0.004
    for side in (-1, 1):
        y = (cfg["cab_start"] - 0.55) * end
        side_text(p["ink"], label, y, cfg["z_upper"][0] + 0.09, cell, gap, x, side * end)


def ceiling_glow(cfg, p):
    """The strongest 'lit and occupied' cue on a vehicle this long: a warm
    strip behind the window band, proud of the opaque glazing."""
    # 4 cm proud of the opaque glazing and flush with the bodyside: proud
    # enough to satisfy the 3-5 cm rule, never proud enough to widen the car.
    hw = cfg["width"] / 2.0 - cfg["x_glass"] + 0.040
    for y0, y1 in window_runs(cfg):
        p["mustard_glow"].span((-hw, hw), (y0, y1), cfg["ceiling_glow"])


# -------------------------------------------------------------------- build


def build(cfg, line):
    # Three banks, by how much of the vehicle each component actually draws.
    # Mirroring the wrong bank is not a cosmetic error: mirroring geometry that
    # ALREADY spans both sides lays a second, coincident copy of every face on
    # top of the first with reversed winding. The result is non-manifold, so
    # `recalc_face_normals` can no longer tell inside from outside, and the
    # affected surfaces export with inward normals and render pure black. That
    # is exactly what happened to the roof, the skirt and the roof equipment on
    # the first pass — and it was invisible in flat-shaded previews, which do
    # not consult normals at all.
    bank = lambda: {k: Part(v) for k, v in MATERIALS.items()}
    half = bank()      # one section, full width, +Y
    quad = bank()      # one section, +X flank only
    sec_a, sec_b, centre = bank(), bank(), bank()

    body_shell(cfg, half)
    glazing(cfg, half)
    ceiling_glow(cfg, half)
    roof_equipment(cfg, half)
    wheels(cfg, half)
    underframe(cfg, half)
    doors(cfg, quad)
    livery_details(cfg, quad)

    for key in quad:
        quad[key].mirror_x()
        half[key].append(quad[key])

    # Section B is section A mirrored through y = 0 — symmetric about the joint,
    # as the brief requires of anything a runtime might later bend.
    for key in half:
        sec_a[key].append(half[key])
        flipped = Part(half[key].mat)
        flipped.append(half[key])
        flipped.flip_y()
        sec_b[key].append(flipped)

    # The pantograph is singular and rides on section A.
    pantograph(cfg, sec_a)
    # The bellows belongs to neither section: it is the joint itself.
    bellows(cfg, centre)

    # --- the two cabs, built independently so no lettering is ever reversed.
    for end, target in ((1, sec_a), (-1, sec_b)):
        cab(cfg, target, end)
        lights(cfg, target, end)
        destination_sign(cfg, target, line, end)
        fleet_number(cfg, target, end)

    order = list(MATERIALS)
    objs = [
        emit_group("LRV_Section_A", sec_a, order),
        emit_group("LRV_Section_B", sec_b, order),
        emit_group("LRV_Bellows", centre, order),
    ]
    return [o for o in objs if o]


def ground_and_centre(objs):
    """Drop the model onto z = 0 and centre it in X/Y, then apply the shift into
    the mesh data so the export carries no object-level transform."""
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    for o in objs:
        for v in o.data.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
    shift = Vector((-(mn.x + mx.x) / 2.0, -(mn.y + mx.y) / 2.0, -mn.z))
    for o in objs:
        for v in o.data.vertices:
            v.co += shift
        o.data.update()
    return mn + shift, mx + shift


def report(tag, objs):
    tris = 0
    for o in objs:
        o.data.calc_loop_triangles()
        tris += len(o.data.loop_triangles)
    print(f"[{tag}] {len(objs)} objects, {tris} triangles")
    for o in sorted(objs, key=lambda x: -len(x.data.loop_triangles)):
        print(f"[{tag}]   {o.name:22s} {len(o.data.loop_triangles):5d}")
    return tris


def export_glb(path):
    """Leak-proof export: a temp scene holding only the export collection, then
    use_active_scene so nothing selected in any other scene can ride along."""
    import contextlib
    import io

    src = bpy.context.scene
    tmp = bpy.data.scenes.new("MuniLrvExport")
    coll = bpy.data.collections.new("muni_lrv_export")
    tmp.collection.children.link(coll)
    for o in [x for x in src.collection.all_objects if x.type == "MESH"]:
        coll.objects.link(o)
    bpy.context.window.scene = tmp
    for o in bpy.data.objects:
        o.select_set(False)

    kwargs = dict(
        filepath=path, export_format="GLB", export_apply=True, export_yup=True,
        use_selection=False, use_active_scene=True, export_cameras=False,
        export_lights=False, export_animations=False, export_skins=False,
        export_morph=False, export_materials="EXPORT",
    )
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            bpy.ops.export_scene.gltf(**kwargs, export_image_format="NONE")
        except TypeError:
            bpy.ops.export_scene.gltf(**kwargs)
    bpy.context.window.scene = src
    bpy.data.scenes.remove(tmp)
    bpy.data.collections.remove(coll)


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = os.path.dirname(os.path.abspath(__file__))
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    lines = [argv[argv.index("--line") + 1]] if "--line" in argv else ["n-judah"]
    if "--all-lines" in argv:
        lines = list(LINES)
    os.makedirs(out, exist_ok=True)

    for key in lines:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        objs = build(CFG, key)
        mn, mx = ground_and_centre(objs)
        report(f"build:{key}", objs)
        print(f"[build] dims={[round(mx[i] - mn[i], 3) for i in range(3)]} "
              f"min={[round(v, 4) for v in mn]} max={[round(v, 4) for v in mx]}")
        name = CFG["slug"] if key == "n-judah" else f"{CFG['slug']}-{key}"
        glb = os.path.join(out, f"{name}.glb")
        export_glb(glb)
        print(f"[build] wrote {glb}")
        if key == "n-judah":
            blend = os.path.join(out, "muni-lrv.blend")
            bpy.ops.wm.save_as_mainfile(filepath=blend)
            print(f"[build] wrote {blend}")


if __name__ == "__main__":
    main()
