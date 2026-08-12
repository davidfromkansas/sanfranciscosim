"""Deterministic Blender build of the SF-SIM miniature Muni 40-foot hybrid bus.

    blender -b --python build_muni_bus.py -- [--out DIR] [--route 29-sunset]

Writes ``muni-bus.blend`` and ``muni-bus-40.glb`` next to this file (or into
``--out``). Every number in here is justified in ``REFERENCE.md``.

VEHICLE CONTRACT (not the landmark one — see docs/asset-plans/transit/README.md)
-------------------------------------------------------------------------------
Authored in Blender, Z up, metres, **nose toward +Y**, sitting on ``z = 0``,
centred in X/Y. The glTF exporter's Y-up conversion maps Blender ``(x, y, z)``
to glTF ``(x, z, -y)``, so this lands the model as the manifest requires:

    nose at glTF **-Z**  ·  ``min y = 0``  ·  origin centred in glTF X/Z

``validate_muni_bus.py`` re-imports the GLB in a fresh scene and
``glb_inspect.mjs`` reads the raw glTF buffers, so the convention is *verified*
rather than assumed.

STRUCTURE
---------
Every visible feature is a component function taking the ``cfg`` dict, so the
trolley coach (same body, different roof and livery) can import them and a
future XDE60 can extend ``wheels()``/``body_shell()`` rather than fork the file.
Component functions never create Blender objects directly: they push geometry
into a ``Part``, one per material. A ``Part`` emits exactly one Blender object,
which means the exported GLB has one primitive per material, flat detail quads
are always hosted inside a closed solid of their own colour (so per-object
signed volume stays positive), and the shrink stage's "join objects sharing a
material" step is satisfied at authoring time.

GLOW
----
``Toy_*_Glow`` surfaces are thin shells 3–5 cm proud of an opaque surface with
their edges buried, per the Conservatory/Grace Cathedral pattern: the app's
landmark loader draws them in an unlit layer at ``0.12 + 0.95 * uNight``, i.e.
88% transparent by day, and the vehicle loader currently draws them opaque
(see REPORT.md). A proud shell over an opaque backing reads correctly in both.
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
    slug="muni-bus-40",
    # --- overall envelope (REFERENCE.md §2)
    length=12.19,          # nominal 40 ft; the low end of the 12.19-12.50 range
    width=2.59,            # 102 in
    z_under=0.30,          # underside of the skirt
    z_body0=0.34,          # bottom of the painted body
    z_sill=1.02,           # top of the wheel-arch openings
    z_cant=3.14,           # top of the silver sides
    z_roof=3.22,           # roof crown
    z_equip=3.40,          # top of the roof equipment -> overall height 3.40
    # --- livery band heights (REFERENCE.md §4, measured off #8613)
    red_lo=(0.34, 0.90),
    red_hi=(2.46, 2.82),
    win=(1.36, 2.40),      # dark reveal
    glass=(1.44, 2.32),    # glazing inside the reveal
    ceiling_glow=(2.19, 2.26),
    # --- longitudinal layout, metres aft of the nose (REFERENCE.md §4)
    windshield=(1.52, 2.66),
    door_front=(1.15, 2.20),
    axle_front=2.35,
    door_mid=(6.95, 8.15),
    axle_rear=9.56,
    arch_half=0.60,        # half-length of a wheel-arch opening
    win_front=1.05,        # window band dies against the A-pillar
    win_rear=0.35,         # ... and returns short of the rear corner
    # --- wheels
    wheel_r=0.52,
    wheel_w=0.30,
    wheel_seg=10,
    hub_r=0.26,
    hub_seg=8,
    # --- mirrors (style bible §9: enlarged because they are a strong bus cue)
    mirror_x=1.65,         # outboard face -> overall width 3.30 m
    mirror_z=(2.16, 2.62),
    mirror_y=5.35,
    # --- roof composition (REFERENCE.md §6)
    hvac=dict(y=1.55, ly=3.30, lx=2.06, z0=3.14, z1=3.40),
    elec=dict(y=-1.75, ly=1.70, lx=1.42, z0=3.14, z1=3.31),
    hatches=(-4.45, 4.15),
    # --- destination sign
    sign_z=(2.72, 3.08),
    sign_x=1.06,
    bevel=0.10,
)

ROUTES = {
    # Every one verified as a New Flyer XDE40 motor-coach line — REFERENCE.md §9.
    "29-sunset": ("29", "SUNSET"),
    "9-san-bruno": ("9", "SAN BRUNO"),
    "43-masonic": ("43", "MASONIC"),
}
FLEET_NUMBER = "8632"  # photographed, in range, and photographed on the 29.

PALETTE_HEX = dict(
    Toy_silver="aab1b9",        # Muni silver; darkened from the shipped fleet's
                                # Toy_Silver so the sides separate from the
                                # white roof under flat diorama light
    Toy_white="f7f4ec",
    Toy_munired="c1272d",       # off-palette by design — REFERENCE.md §4
    Toy_ink="3a3530",
    Toy_glass="26405e",   # palette glass, taken a step darker: the brief
                            # wants a BLACK window band and 2a4d73 reads navy
                            # across a 10 m panel
    Toy_steel="9aa0a6",
    Toy_tire="2c2c2f",          # = the shipped fleet's Toy_Tire
    Toy_mustard_Glow="d9a441",
    Toy_white_Glow="f7f4ec",
    Toy_red_Glow="c4453c",
)


# Short name used inside the component functions -> contract material name.
MATERIALS = dict(
    silver="Toy_silver", white="Toy_white", munired="Toy_munired", ink="Toy_ink",
    glass="Toy_glass", steel="Toy_steel", tire="Toy_tire",
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
        # white (glTF emissiveFactor (0,0,0) otherwise imports as white).
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
    """Accumulates geometry for exactly one material, emits one object.

    Flat detail (logos, glyphs, pillars) is added to the same Part as that
    colour's solids, so the emitted object always has positive signed volume.
    """

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
        """Box from explicit (lo, hi) ranges — how most of this model is written."""
        self.box(
            ((x[0] + x[1]) / 2.0, (y[0] + y[1]) / 2.0, (z[0] + z[1]) / 2.0),
            (x[1] - x[0], y[1] - y[0], z[1] - z[0]),
            bevel, segments,
        )

    def loft(self, ring_lo, ring_hi):
        """Closed solid between two equal-length closed rings of 3D points."""
        n = len(ring_lo)
        verts = list(ring_lo) + list(ring_hi)
        faces = [(i, (i + 1) % n, (i + 1) % n + n, i + n) for i in range(n)]
        faces.append(tuple(range(n - 1, -1, -1)))
        faces.append(tuple(range(n, 2 * n)))
        self._push(verts, faces)

    def cylinder(self, centre, radius, half_len, segments, axis="x", a0=None):
        """`a0` defaults to -pi/2, which puts a vertex at the bottom of the
        section. On a wheel that is what makes `min y` land on exactly 0
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
            else:  # z
                lo.append((cx + u, cy + v, cz - half_len))
                hi.append((cx + u, cy + v, cz + half_len))
        self.loft(lo, hi)

    def mirror_x(self):
        """Duplicate everything added so far across x=0. Both sides, one call."""
        n = len(self.verts)
        self.verts.extend([(-x, y, z) for x, y, z in self.verts])
        self.faces.extend([tuple(n + i for i in reversed(f)) for f in list(self.faces)])

    def emit(self):
        if not self.faces:
            return None
        mesh = bpy.data.meshes.new(self.mat)
        mesh.from_pydata([Vector(v) for v in self.verts], [], self.faces)
        mesh.materials.append(material(self.mat))
        mesh.validate()
        obj = bpy.data.objects.new(self.mat, mesh)
        bpy.context.collection.objects.link(obj)
        bm = bmesh.new()
        bm.from_mesh(mesh)
        bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
        bm.to_mesh(mesh)
        bm.free()
        mesh.shade_flat()
        return obj


def _bevelled(verts, faces, width, segments):
    """Style-bible §4 edge softening, done on loose geometry before it is banked."""
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
# Each stroke is one quad on the sign face, hosted inside the closed Toy_ink
# solid, so 9 characters cost ~60 triangles instead of the ~600 a real extruded
# font would. Cells are unit squares; the caller scales and places them.

SEG7 = {  # 7-segment: top, top-l, top-r, mid, bot-l, bot-r, bot
    "0": "ABCEFG", "1": "CF", "2": "ACDEG", "3": "ACDFG", "4": "BCDF",
    "5": "ABDFG", "6": "ABDEFG", "7": "ACF", "8": "ABCDEFG", "9": "ABCDFG",
}
SEG_RECT = {  # name -> (x0, y0, x1, y1) in the unit cell
    "A": (0.00, 0.86, 1.00, 1.00), "B": (0.00, 0.50, 0.16, 0.94),
    "C": (0.84, 0.50, 1.00, 0.94), "D": (0.00, 0.43, 1.00, 0.57),
    "E": (0.00, 0.06, 0.16, 0.50), "F": (0.84, 0.06, 1.00, 0.50),
    "G": (0.00, 0.00, 1.00, 0.14),
}
# Block letters: axis-aligned rectangles, plus explicit quads for diagonals.
LETTER = {
    "A": ["B", "C", "A", "D", (0.00, 0.00, 0.16, 0.50), (0.84, 0.00, 1.00, 0.50)],
    "B": ["A", "B", "D", "E", "G", "C", "F"],
    "C": ["A", "B", "E", "G"],
    "D": ["A", "B", "E", "G", "C", "F"],
    "E": ["A", "B", "D", "E", "G"],
    "G": ["A", "B", "E", "G", "F", (0.50, 0.43, 1.00, 0.57)],
    "H": ["B", "C", "D", "E", "F"],
    "I": [(0.42, 0.00, 0.58, 1.00)],
    "K": ["B", "E", (0.30, 0.42, 1.00, 0.58)],
    "L": ["B", "E", "G"],
    "M": ["B", "C", "E", "F", (0.38, 0.55, 0.62, 1.00)],
    "N": ["B", "C", "E", "F", "A"],
    "O": ["A", "B", "C", "E", "F", "G"],
    "P": ["A", "B", "C", "D", "E"],
    "R": ["A", "B", "C", "D", "E", (0.62, 0.00, 0.84, 0.46)],
    "S": ["A", "B", "D", "F", "G"],
    "T": ["A", (0.42, 0.00, 0.58, 0.90)],
    "U": ["B", "C", "E", "F", "G"],
    "V": ["B", "C", (0.20, 0.00, 0.80, 0.16)],
    "W": ["B", "C", "E", "F", (0.38, 0.00, 0.62, 0.45)],
    "Y": ["B", "C", "D", (0.42, 0.00, 0.58, 0.46)],
    "'": [(0.42, 0.72, 0.58, 1.00)],
    " ": [],
}


def _rects(ch):
    if ch in SEG7:
        return [SEG_RECT[s] for s in SEG7[ch]]
    return [SEG_RECT[r] if isinstance(r, str) else r for r in LETTER.get(ch, [])]


def stroke_text(part, text, origin, cell, gap, y_plane):
    """Lay `text` across the bus FRONT, on the plane y = y_plane.

    The front faces +Y in Blender, so a viewer standing in front of the bus
    sees +X on their LEFT. Text therefore advances in -X: laying it out in +X
    ships a mirrored destination sign, which is exactly the kind of thing that
    survives to production because nobody renders the front elevation.

    origin = (x_of_first_glyph_left_edge_as_seen, z_bottom).
    """
    cw, chh = cell
    x = origin[0]
    for ch in text:
        for (rx0, rz0, rx1, rz1) in _rects(ch):
            xa, xb = x - rx0 * cw, x - rx1 * cw
            za, zb = origin[1] + rz0 * chh, origin[1] + rz1 * chh
            part.quad((xa, y_plane, za), (xb, y_plane, za),
                      (xb, y_plane, zb), (xa, y_plane, zb))
        x -= cw + gap


def text_width(text, cell_w, gap):
    return len(text) * cell_w + max(0, len(text) - 1) * gap


def side_text(part, text, y_start, z0, cell, gap, x_plane, side):
    """Same stroke font, laid on a bus SIDE (the plane x = x_plane * side).

    `side` is +1 for the right flank and -1 for the left. A viewer off the RIGHT
    flank (standing at +X, looking -X, +Z up) has their right hand toward +Y, so
    text reads tail-to-nose; off the LEFT flank it reads nose-to-tail. Advancing
    by `+side` satisfies both, and the resulting winding then points outward on
    each flank without any extra reversal.

    Building both flanks explicitly rather than mirroring one is the whole point
    of this function: `mirror_x()` would hand back a backwards fleet number.
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


# ---------------------------------------------------------------- components
#
# Each takes (cfg, parts) and adds geometry for the +X side (or the whole
# vehicle where it is on the centreline). Anything added to a "sided" Part is
# mirrored once at the end, so left and right can never drift apart.


def _y(cfg, t):
    """Blender y for a distance `t` metres aft of the nose."""
    return cfg["length"] / 2.0 - t


def lower_runs(cfg, proud=0.0):
    """The three longitudinal runs of lower bodywork, i.e. everything below the
    sill except the two wheel-arch openings. Returned as Blender y ranges so
    `body_shell` and `livery_band` cut the arches identically — a band that
    crossed an arch would read as a bus with its wheels painted on."""
    L = cfg["length"] / 2.0 + proud
    a = cfg["arch_half"]
    cuts = []
    for t in (cfg["axle_front"], cfg["axle_rear"]):
        cuts.append((_y(cfg, t + a), _y(cfg, t - a)))
    cuts.sort()
    runs, edge = [], -L
    for lo, hi in cuts:
        runs.append((edge, lo))
        edge = hi
    runs.append((edge, L))
    return runs


def body_shell(cfg, p):
    """The one big volume everything else is hung on, plus the white roof cap.

    Split at the sill so the lower bodywork can be interrupted by the wheel
    arches; the XDE60 variant only has to add a third axle to `lower_runs`.
    """
    hw = cfg["width"] / 2.0
    L = cfg["length"] / 2.0
    p["silver"].span((-hw, hw), (-L, L), (cfg["z_sill"], cfg["z_cant"]),
                     bevel=cfg["bevel"], segments=2)
    for y0, y1 in lower_runs(cfg):
        p["silver"].span((-hw, hw), (y0, y1), (cfg["z_body0"], cfg["z_sill"] + 0.02),
                         bevel=0.07, segments=2)
    # Arch liners: a dark recess behind each wheel so the opening reads as a
    # cavity instead of a hole you can see daylight through.
    for t in (cfg["axle_front"], cfg["axle_rear"]):
        a = cfg["arch_half"]
        p["ink"].span((-hw + 0.20, hw - 0.20), (_y(cfg, t + a), _y(cfg, t - a)),
                      (cfg["z_body0"] - 0.02, cfg["z_sill"]))
    # Roof cap: slightly inset so a silver edge still shows from the side, and
    # clearly lighter than the sides so the two planes separate (plan §2.9).
    p["white"].span((-hw + 0.05, hw - 0.05), (-L + 0.07, L - 0.07),
                    (cfg["z_cant"] - 0.03, cfg["z_roof"]), bevel=0.06, segments=2)


def skirt(cfg, p):
    for y0, y1 in lower_runs(cfg):
        p["ink"].span((-cfg["width"] / 2.0 + 0.05, cfg["width"] / 2.0 - 0.05),
                      (y0 + 0.06, y1 - 0.06),
                      (cfg["z_under"], cfg["z_body0"] + 0.02))


def livery_band(cfg, p, z_range, runs=None, proud=0.022, bevel=0.05):
    """A red belt around the body. The two-band scheme is the entire identity of
    this asset (REFERENCE.md §3); taking a z-range and an optional list of y
    runs keeps it reusable for the trolley coach, whose bands sit elsewhere.

    `runs=None` means one continuous belt wrapping nose and tail."""
    hw = cfg["width"] / 2.0 + proud
    L = cfg["length"] / 2.0 + proud
    for y0, y1 in runs or [(-L, L)]:
        p["munired"].span((-hw, hw), (y0, y1), z_range, bevel=bevel, segments=1)


def cant_band(cfg, p, proud=0.022):
    """The upper red band runs the sides and wraps the tail, but stops at the
    A-pillar: on a real XDE40 the front cap above the windshield is silver with
    the sign hood set into it, not a red stripe across the face."""
    hw = cfg["width"] / 2.0 + proud
    L = cfg["length"] / 2.0 + proud
    p["munired"].span((-hw, hw), (-L, _y(cfg, cfg["win_front"])), cfg["red_hi"],
                      bevel=0.05, segments=1)


def window_band(cfg, p):
    """One continuous dark reveal per side with the glazing set inside it, and
    three pillars as flat quads. Individually modelled windows would be spent
    triangles (style bible §5: rhythm, not detail)."""
    hw = cfg["width"] / 2.0
    y0, y1 = _y(cfg, cfg["length"] - cfg["win_rear"]), _y(cfg, cfg["win_front"])
    # Dark reveal, then the glazing PROUD of it, so the ink reads as a frame
    # around the glass rather than burying it.
    p["ink"].span((hw - 0.05, hw + 0.012), (y0, y1), cfg["win"])
    p["glass"].span((hw - 0.03, hw + 0.024), (y0 + 0.07, y1 - 0.07), cfg["glass"])
    # Pillars: flat quads hosted in the silver solid, 3 per side.
    for t in (3.35, 5.25, 9.35):
        yy = _y(cfg, t)
        p["silver"].quad(
            (hw + 0.027, yy - 0.07, cfg["glass"][0]),
            (hw + 0.027, yy + 0.07, cfg["glass"][0]),
            (hw + 0.027, yy + 0.07, cfg["glass"][1]),
            (hw + 0.027, yy - 0.07, cfg["glass"][1]),
        )
    # Interior ceiling strip: a Toy_mustard_Glow shell 3 cm proud of the opaque
    # glazing, edges buried inside the ink reveal. Reads as a lit, occupied bus
    # at night and as a warm strip along the window tops by day.
    p["mustard_glow"].span((hw + 0.01, hw + 0.054), (y0 + 0.14, y1 - 0.14),
                           cfg["ceiling_glow"])


def door(cfg, p, t_range):
    """Double-leaf door: one red panel with the glazing proud of it, so the red
    reads as the frame. Both Muni doors are framed in red (REFERENCE.md §5)."""
    hw = cfg["width"] / 2.0
    y0, y1 = _y(cfg, t_range[1]), _y(cfg, t_range[0])
    p["munired"].span((hw - 0.05, hw + 0.034), (y0, y1), (0.40, 2.44), bevel=0.03,
                      segments=1)
    p["glass"].span((hw - 0.04, hw + 0.042), (y0 + 0.10, y1 - 0.10), (1.02, 2.30))


def windshield(cfg, p):
    """A single chamfered volume wrapping the front corners, raked back ~11 deg.
    Four plan segments is enough for the wrap to read at 15 m and cheap enough
    to be invisible in the budget."""
    L = cfg["length"] / 2.0
    hw = cfg["width"] / 2.0
    z0, z1 = cfg["windshield"]
    # The rake has to stay shallower than the amount the glass stands proud
    # of the body, or the top of the windshield ends up buried inside the shell.
    rake = 0.095
    out = [(-1.225, L + 0.03), (-1.05, L + 0.125), (1.05, L + 0.125), (1.225, L + 0.03)]
    inn = [(x, y - 0.09) for x, y in out]
    ring_lo = [(x, y, z0) for x, y in out] + [(x, y, z0) for x, y in reversed(inn)]
    ring_hi = [(x, y - rake, z1) for x, y in out] + \
              [(x, y - rake, z1) for x, y in reversed(inn)]
    p["glass"].loft(ring_lo, ring_hi)
    # Dark A-pillar returns tie the windshield into the side window band.
    for sx in (-1, 1):
        p["ink"].span((sx * (hw - 0.02), sx * (hw + 0.014)),
                      (_y(cfg, cfg["win_front"]) - 0.02, L - 0.30),
                      (cfg["win"][0], cfg["win"][1]))


def destination_sign(cfg, p, route):
    """Amber field, dark glyphs, extruded — never a texture.

    Real Muni signs are amber dots on black. This inverts that: a
    Toy_mustard_Glow field with Toy_ink block glyphs proud of it. The brief
    wants a lit amber rectangle at 120 m and a legible number at 15 m, and the
    inversion delivers both for a fraction of the triangles while keeping the
    glow as one clean shell rather than dozens of tiny ones that would vanish
    at 12% day opacity. Recorded as a deliberate deviation in REPORT.md.
    """
    number, dest = route
    L = cfg["length"] / 2.0
    z0, z1 = cfg["sign_z"]
    sx = cfg["sign_x"]
    # Opaque backing + hood, recessed into the front cap so the sign never
    # protrudes past the bumper line (real signs sit in a hood behind the
    # windshield's leading edge).
    p["ink"].span((-sx - 0.06, sx + 0.06), (L - 0.26, L + 0.005), (z0 - 0.06, z1 + 0.07),
                  bevel=0.03, segments=1)
    # The lit face: a shell 4 cm proud of the backing, edges inside the hood.
    face_y = L + 0.040
    p["mustard_glow"].span((-sx, sx), (face_y - 0.045, face_y), (z0, z1))

    # Glyphs, 1.2 cm proud of the lit face. The route number is set large enough
    # to be legible at 15 m; the destination only has to read as text.
    gy = face_y + 0.012
    num_h = (z1 - z0) * 0.80
    num_w = num_h * 0.60
    gap = num_w * 0.22
    dst_h = num_h * 0.60
    dst_w = dst_h * 0.62
    dgap = dst_w * 0.26
    space = num_w * 0.55
    total = text_width(number, num_w, gap) + space + text_width(dest, dst_w, dgap)
    zc = (z0 + z1) / 2.0
    x = total / 2.0  # left edge as the viewer sees it (+X is viewer-left)
    stroke_text(p["ink"], number, (x, zc - num_h / 2.0), (num_w, num_h), gap, gy)
    x -= text_width(number, num_w, gap) + space
    stroke_text(p["ink"], dest, (x, zc - dst_h / 2.0), (dst_w, dst_h), dgap, gy)


def roof_pod(cfg, p):
    """The roof is a primary surface at a 42 deg camera, so it is composed by
    VALUE, not by part count: two dark masses and two pale hatches on a large
    white field (REFERENCE.md §6). The first pass made the HVAC white on a white
    roof and the whole roof read as a blank sticker.
    """
    h = cfg["hvac"]
    p["steel"].span((-h["lx"] / 2, h["lx"] / 2),
                    (h["y"] - h["ly"] / 2, h["y"] + h["ly"] / 2),
                    (h["z0"], h["z1"]), bevel=0.05, segments=2)
    # Condenser louvres: four dark slats across the HVAC top. The one detail
    # that tells the eye this mass is machinery and not a box.
    y0 = h["y"] - h["ly"] / 2 + 0.30
    pitch = (h["ly"] - 0.60) / 4.0
    for i in range(4):
        p["ink"].span((-h["lx"] / 2 + 0.16, h["lx"] / 2 - 0.16),
                      (y0 + i * pitch, y0 + i * pitch + pitch * 0.52),
                      (h["z1"] - 0.02, h["z1"] + 0.016))
    e = cfg["elec"]
    p["ink"].span((-e["lx"] / 2, e["lx"] / 2),
                  (e["y"] - e["ly"] / 2, e["y"] + e["ly"] / 2),
                  (e["z0"], e["z1"]), bevel=0.04, segments=1)
    for hy in cfg["hatches"]:
        p["silver"].span((-0.40, 0.40), (hy - 0.40, hy + 0.40),
                         (cfg["z_roof"] - 0.02, cfg["z_roof"] + 0.045),
                         bevel=0.03, segments=1)


def wheels(cfg, p, axles=None):
    """One wheel per side per axle. `axles` is a list so the XDE60 variant can
    pass three without touching this function."""
    if axles is None:
        axles = [cfg["axle_front"], cfg["axle_rear"]]
    x = cfg["width"] / 2.0 - 0.16
    for t in axles:
        yy = _y(cfg, t)
        p["tire"].cylinder((x, yy, cfg["wheel_r"]), cfg["wheel_r"],
                           cfg["wheel_w"] / 2.0, cfg["wheel_seg"], axis="x")
        p["steel"].cylinder((x + cfg["wheel_w"] / 2.0 - 0.01, yy, cfg["wheel_r"]),
                            cfg["hub_r"], 0.035, cfg["hub_seg"], axis="x")


def mirrors(cfg, p):
    """Enlarged per style bible §9 — a strong bus cue that would otherwise
    disappear, and the widest point of the model."""
    hw = cfg["width"] / 2.0
    z0, z1 = cfg["mirror_z"]
    zc = (z0 + z1) / 2.0
    p["ink"].span((hw - 0.04, cfg["mirror_x"] - 0.04),
                  (cfg["mirror_y"] - 0.05, cfg["mirror_y"] + 0.05),
                  (zc + 0.12, zc + 0.20))
    p["ink"].span((cfg["mirror_x"] - 0.15, cfg["mirror_x"]),
                  (cfg["mirror_y"] - 0.075, cfg["mirror_y"] + 0.075),
                  (z0, z1), bevel=0.04, segments=1)


def lights(cfg, p):
    """Opaque ink housings with glow shells 4 cm proud of them."""
    L = cfg["length"] / 2.0
    # Headlights: outer lower corners of the fascia, in the silver just above
    # the lower red band. Opaque ink housing, glow shell 4 cm proud of it.
    p["ink"].span((0.64, 1.06), (L - 0.02, L + 0.045), (0.96, 1.22), bevel=0.03,
                  segments=1)
    p["white_glow"].span((0.71, 0.99), (L + 0.040, L + 0.085), (1.01, 1.17))
    # Tail lights: vertical stacks at the rear outer corners.
    p["ink"].span((0.74, 1.06), (-L - 0.050, -L + 0.02), (1.00, 1.66), bevel=0.03,
                  segments=1)
    p["red_glow"].span((0.79, 1.01), (-L - 0.090, -L - 0.045), (1.05, 1.61))


def bumpers(cfg, p):
    L = cfg["length"] / 2.0
    hw = cfg["width"] / 2.0
    p["ink"].span((-hw - 0.01, hw + 0.01), (L - 0.05, L + 0.10), (0.30, 0.62),
                  bevel=0.05, segments=1)
    p["ink"].span((-hw - 0.01, hw + 0.01), (-L - 0.10, -L + 0.05), (0.30, 0.62),
                  bevel=0.05, segments=1)


def rear_face(cfg, p):
    """Engine louvre band and the rear window — the two things that stop the
    back of the bus reading as a blank slab (REFERENCE.md §5)."""
    L = cfg["length"] / 2.0
    p["ink"].span((-1.02, 1.02), (-L - 0.035, -L + 0.02), (2.44, 2.84))
    p["glass"].span((-0.88, 0.88), (-L - 0.020, -L + 0.02), (1.62, 2.30))


# The Muni worm, compressed to four CONVEX quads in a unit cell.
#
# The real Landor mark is one continuous ribbon whose stroke rises and dips to
# spell "muni". Two earlier attempts drew it as a single concave outline: the
# first squared the humps off and read as castle crenellation, the second
# self-intersected and triangulated into confetti. A wave is not worth an n-gon
# at this size — a baseline bar plus three risers reads as the mark at 15 m and
# as a red tick at 120 m, is convex everywhere, and costs 8 triangles.
_WORM_QUADS = [
    (0.00, 0.00, 1.00, 0.52),   # the ribbon's baseline, deliberately heavy so
    (0.10, 0.52, 0.28, 1.00),   # the mark reads as one connected wordmark
    (0.41, 0.52, 0.59, 1.00),   # rather than as three loose blocks
    (0.72, 0.52, 0.90, 1.00),
]


def _worm_cells(size):
    w, h = size
    return [(u0 * w, v0 * h, u1 * w, v1 * h) for u0, v0, u1, v1 in _WORM_QUADS]


def worm(cfg, p, t_positions):
    """The Muni worm on the silver field below the windows, twice per side.

    Built explicitly on both flanks for the same reason as `side_text`: a
    mirrored wordmark is a backwards wordmark.
    """
    hw = cfg["width"] / 2.0 + 0.014
    zc = cfg["red_lo"][1] + 0.14
    for t in t_positions:
        y0 = _y(cfg, t)
        for side in (1, -1):
            x = hw * side
            for u0, v0, u1, v1 in _worm_cells((0.86, 0.28)):
                ya, yb = y0 + side * u0, y0 + side * u1
                quad = ((x, ya, zc + v0), (x, yb, zc + v0),
                        (x, yb, zc + v1), (x, ya, zc + v1))
                p["munired"].quad(*quad)


def fleet_number(cfg, p, number, t_positions):
    hw = cfg["width"] / 2.0 + 0.014
    for t in t_positions:
        for side in (1, -1):
            side_text(p["ink"], number, _y(cfg, t), 1.00, (0.15, 0.24), 0.05, hw, side)


def front_fleet_number(cfg, p, number):
    """Small four-digit number on the fascia, offset to one side of the worm as
    on #8759 ("8759 K") and #8632."""
    L = cfg["length"] / 2.0
    w, hgt, gap = 0.135, 0.21, 0.045
    stroke_text(p["ink"], number, (1.10, 1.26), (w, hgt), gap, L + 0.014)


def front_worm(cfg, p):
    """The worm also sits low and central on the front fascia (#8759, #8632).
    Laid out in -X like every other front-facing mark, so it is not mirrored."""
    L = cfg["length"] / 2.0
    w, h = 0.64, 0.22
    z = 0.98
    for u0, v0, u1, v1 in _worm_cells((w, h)):
        xa, xb = w / 2.0 - u0, w / 2.0 - u1
        p["munired"].quad((xa, L + 0.014, z + v0), (xb, L + 0.014, z + v0),
                          (xb, L + 0.014, z + v1), (xa, L + 0.014, z + v1))


# --------------------------------------------------------------------- build


def build(cfg, route_key="29-sunset"):
    route = ROUTES[route_key]

    # Parts that exist on both sides are built once on +X and mirrored; parts on
    # the centreline are built whole. Both banks key on the same short names, so
    # a component function reads the same wherever it is called from.
    def bank():
        return {short: Part(name) for short, name in MATERIALS.items()}

    whole, sided = bank(), bank()

    # --- centreline / full-width components
    body_shell(cfg, whole)
    skirt(cfg, whole)
    livery_band(cfg, whole, cfg["red_lo"], runs=lower_runs(cfg, proud=0.022))
    cant_band(cfg, whole)
    windshield(cfg, whole)
    destination_sign(cfg, whole, route)
    roof_pod(cfg, whole)
    bumpers(cfg, whole)
    rear_face(cfg, whole)
    front_fleet_number(cfg, whole, FLEET_NUMBER)
    front_worm(cfg, whole)
    # Lettering and wordmarks are laid on BOTH flanks here rather than mirrored:
    # `mirror_x` would reverse them (see side_text).
    worm(cfg, whole, (4.55, 11.10))
    fleet_number(cfg, whole, FLEET_NUMBER, (3.05,))

    # --- one-sided components, mirrored below
    window_band(cfg, sided)
    door(cfg, sided, cfg["door_front"])
    door(cfg, sided, cfg["door_mid"])
    wheels(cfg, sided)
    mirrors(cfg, sided)
    lights(cfg, sided)
    for part in sided.values():
        part.mirror_x()

    # --- one object per material
    merged = {}
    for bank in (whole, sided):
        for part in bank.values():
            if not part.faces:
                continue
            tgt = merged.setdefault(part.mat, Part(part.mat))
            base = len(tgt.verts)
            tgt.verts.extend(part.verts)
            tgt.faces.extend([tuple(base + i for i in f) for f in part.faces])
    objs = [p.emit() for p in merged.values()]
    return [o for o in objs if o]


def report(tag="build"):
    dg = bpy.context.evaluated_depsgraph_get()
    tris = 0
    mn = Vector((1e9, 1e9, 1e9))
    mx = Vector((-1e9, -1e9, -1e9))
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    per = []
    for o in objs:
        me = o.evaluated_get(dg).to_mesh()
        me.calc_loop_triangles()
        per.append((o.name, len(me.loop_triangles)))
        tris += len(me.loop_triangles)
        for v in me.vertices:
            w = o.matrix_world @ v.co
            for i in range(3):
                mn[i] = min(mn[i], w[i])
                mx[i] = max(mx[i], w[i])
        o.evaluated_get(dg).to_mesh_clear()
    print(f"[{tag}] objects={len(objs)} tris={tris}")
    for name, n in sorted(per, key=lambda kv: -kv[1]):
        print(f"[{tag}]   {name:22s} {n:5d}")
    print(f"[{tag}] bbox min={[round(v, 3) for v in mn]} max={[round(v, 3) for v in mx]}")
    print(f"[{tag}] dims={[round(mx[i] - mn[i], 3) for i in range(3)]}")
    return tris


def export_glb(path):
    """Leak-proof export: a temp scene holding only the export collection, then
    use_active_scene so nothing selected in any other scene can ride along."""
    import contextlib
    import io

    src = bpy.context.scene
    tmp = bpy.data.scenes.new("MuniBusExport")
    coll = bpy.data.collections.new("muni_bus_export")
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
    routes = [argv[argv.index("--route") + 1]] if "--route" in argv else ["29-sunset"]
    if "--all-routes" in argv:
        routes = list(ROUTES)
    os.makedirs(out, exist_ok=True)

    for i, key in enumerate(routes):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        build(CFG, key)
        report(f"build:{key}")
        name = CFG["slug"] if key == "29-sunset" else f"{CFG['slug']}-{key}"
        glb = os.path.join(out, f"{name}.glb")
        export_glb(glb)
        print(f"[build] wrote {glb}")
        if key == "29-sunset":
            blend = os.path.join(out, "muni-bus.blend")
            bpy.ops.wm.save_as_mainfile(filepath=blend)
            print(f"[build] wrote {blend}")


if __name__ == "__main__":
    main()
