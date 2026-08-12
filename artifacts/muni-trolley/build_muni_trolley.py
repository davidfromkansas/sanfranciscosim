"""Deterministic Blender build of the SF-SIM miniature Muni 40-foot trolley coach.

    blender -b --python build_muni_trolley.py -- [--out DIR] [--route 1-california]

Writes ``muni-trolley.blend`` and ``muni-trolley-40.glb`` next to this file (or
into ``--out``). Every number is justified in ``REFERENCE.md``.

THE BODY IS IMPORTED, NOT REBUILT
---------------------------------
A New Flyer Xcelsior XT40 trolley coach and an XDE40 hybrid coach are the same
shell with different power. Forking the body would be a bug, so this script
imports the component functions from ``artifacts/muni-bus/build_muni_bus.py``
and adds only what is genuinely different:

    imported unchanged   body_shell · lower_runs · skirt · livery_band ·
                         cant_band · window_band · door · windshield ·
                         destination_sign · roof_pod · wheels · mirrors ·
                         lights · bumpers · worm · fleet_number ·
                         front_worm · front_fleet_number
                         ... plus Part, the palette, the stroke font and the
                         leak-proof exporter

    new here             pole_plinth · pole_bases · poles · pole_shoes
                         rear_face_trolley (no engine louvre band)

The only body change beyond that is a cfg override: the roof electronics box is
enlarged, because New Flyer puts the trolley's inverters and braking resistors
up there and a hybrid has nothing equivalent.

``build_muni_bus.py`` is imported, never edited: a diverged trolley body and a
diverged bus body are the same bug seen from two directions.

THE POLES ARE THE ASSET
-----------------------
Everything above the cant rail is inherited and solved. The only thing that
distinguishes this vehicle from the hybrid coach at any distance is two poles
angled back off the roof, so they get the attention and a disproportionate share
of the triangle budget. They are authored at ~3.7x scale diameter (style bible
§9, semantic scale) because a scale-accurate 50 mm tube is a sub-pixel line at
the app's camera and simply vanishes.

VEHICLE CONTRACT — see the bus script's header. Authored Z up, metres, nose
toward +Y, sitting on z = 0, centred in X/Y; the exporter's Y-up conversion
lands it as nose at glTF -Z, ``min y = 0``.
"""

import math
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "muni-bus"))

import build_muni_bus as bus  # noqa: E402  (path has to be set up first)
from build_muni_bus import (  # noqa: E402
    Part, _y, body_shell, bumpers, cant_band, destination_sign, door,
    export_glb, front_fleet_number, front_worm, fleet_number, lights,
    livery_band, lower_runs, mirrors, report, roof_pod, skirt, wheels,
    window_band, windshield, worm,
)

# The shared stroke font never needed an F — no XDE40 route has one. Two of the
# three trolley coach lines do. Added to the shared bank at import time rather
# than by editing the bus script, so the bus GLB is provably untouched: a new
# key cannot change a glyph the bus never draws.
#   F = top bar + both left verticals + middle bar (E without the bottom bar).
bus.LETTER.setdefault("F", ["A", "B", "D", "E"])


# --------------------------------------------------------------- the vehicle

CFG = dict(bus.CFG)
CFG.update(
    slug="muni-trolley-40",
    # --- pole assembly (REFERENCE.md §4) -----------------------------------
    # The plinth sits over the rear axle, which is where the pole base
    # structure is actually supported and ~2.7 m forward of the tail.
    plinth=dict(t=9.45, lx=1.20, ly=0.90, z0=3.22, z1=3.34),
    base_r=0.14,            # spring housing radius
    base_z=(3.34, 3.59),
    base_dx=0.30,           # -> bases 0.60 m apart, the real two-wire spacing
    pivot_z=3.52,           # where the pole leaves the housing
    pole_len=3.60,
    pole_deg=38.0,          # above horizontal, trailing aft
    pole_splay_deg=4.0,     # tips 1.00 m apart; the wires are ~0.61-0.70 m
    pole_r0=0.095,          # ~3.7x scale-accurate. REFERENCE.md §4, §6.
    pole_r1=0.062,
    pole_seg=8,
    shoe=(0.30, 0.17, 0.11),
    # --- roof electronics (REFERENCE.md §5). New Flyer puts the Vossloh Kiepe
    # inverters and braking resistors on the roof AHEAD of the current
    # collector, so the trolley coach's electronics mass is visibly bigger than
    # the hybrid's. Expressed by enlarging the box the bus already has rather
    # than adding a second one: a fourth mass turned the roof into a barcode,
    # which is the exact failure style bible §10 warns about.
    elec=dict(y=-1.55, ly=2.30, lx=1.66, z0=3.14, z1=3.32),
)

ROUTES = {
    # All three verified as **XT40** (40 ft rigid trolley coach) lines, not
    # XT60 — REFERENCE.md §7. This is where the two coach families differ and
    # it is the easiest thing in the asset to get quietly wrong.
    "1-california": ("1", "CALIFORNIA"),
    "22-fillmore": ("22", "FILLMORE"),
    "24-divisadero": ("24", "DIVISADERO"),
}
FLEET_NUMBER = "5743"  # in the 5701-5885 XT40 block and photographed in service


# ---------------------------------------------------------------- new parts


def _ring(centre, axis, radius, segments, a0=-math.pi / 2.0):
    """A closed ring of `segments` points, radius `radius`, centred on `centre`
    and perpendicular to the unit vector `axis`.

    The poles are the only geometry in the transit set that is neither
    axis-aligned nor a body of revolution about an axis, so they cannot use
    `Part.cylinder`. Building explicit perpendicular rings and lofting between
    them is what keeps a *tapered, tilted, splayed* rod a closed solid with
    consistent winding — which is exactly the object the shrink stage's signed
    volume gate is most likely to catch inverted.
    """
    ax = [axis[0], axis[1], axis[2]]
    # Any vector not parallel to the axis works as the seed for the frame.
    seed = (0.0, 0.0, 1.0) if abs(ax[2]) < 0.9 else (1.0, 0.0, 0.0)
    u = (ax[1] * seed[2] - ax[2] * seed[1],
         ax[2] * seed[0] - ax[0] * seed[2],
         ax[0] * seed[1] - ax[1] * seed[0])
    ul = math.sqrt(sum(c * c for c in u)) or 1.0
    u = tuple(c / ul for c in u)
    v = (ax[1] * u[2] - ax[2] * u[1],
         ax[2] * u[0] - ax[0] * u[2],
         ax[0] * u[1] - ax[1] * u[0])
    out = []
    for i in range(segments):
        a = 2.0 * math.pi * i / segments + a0
        c, s = math.cos(a) * radius, math.sin(a) * radius
        out.append((centre[0] + u[0] * c + v[0] * s,
                    centre[1] + u[1] * c + v[1] * s,
                    centre[2] + u[2] * c + v[2] * s))
    return out


def pole_axis(cfg, side):
    """Unit direction of one pole: aft (-Y), up (+Z), splayed outboard in X.

    `side` is +1 for the right-hand pole and -1 for the left. Aft is -Y because
    the nose is +Y — the single most important sign in this file. A coach whose
    poles lean toward the nose is wrong from every angle and is exactly the kind
    of error that reads as "fine" on an isolated turntable.
    """
    th = math.radians(cfg["pole_deg"])
    sp = math.radians(cfg["pole_splay_deg"])
    horiz = math.cos(th)
    return (side * horiz * math.sin(sp), -horiz * math.cos(sp), math.sin(th))


def pole_endpoints(cfg, side):
    ax = pole_axis(cfg, side)
    base = (side * cfg["base_dx"], _y(cfg, cfg["plinth"]["t"]), cfg["pivot_z"])
    tip = tuple(base[i] + ax[i] * cfg["pole_len"] for i in range(3))
    return base, tip, ax


def pole_plinth(cfg, p):
    """Low dark box the two pole bases stand on. Dark against the white roof so
    the pole assembly separates from a distance under flat diorama lighting —
    the roof is a primary surface at the app's 42 deg camera and this is the one
    thing on it that says trolley coach."""
    pl = cfg["plinth"]
    y = _y(cfg, pl["t"])
    p["ink"].span((-pl["lx"] / 2, pl["lx"] / 2),
                  (y - pl["ly"] / 2, y + pl["ly"] / 2),
                  (pl["z0"], pl["z1"]), bevel=0.03, segments=1)


def pole_bases(cfg, p):
    """One beveled cylinder per pole, standing in for the whole spring/pivot
    housing (plan §2.6). Two of them, 0.60 m apart, which is the real spacing of
    the two overhead wires — the fact the top view exists to prove."""
    y = _y(cfg, cfg["plinth"]["t"])
    z0, z1 = cfg["base_z"]
    for side in (1, -1):
        p["steel"].cylinder((side * cfg["base_dx"], y, (z0 + z1) / 2.0),
                            cfg["base_r"], (z1 - z0) / 2.0, 10, axis="z")


def poles(cfg, p):
    """The asset. Two tapered rods, trailing aft and up.

    Deliberately ~3.7x scale diameter: a real trolley pole is a ~50 mm tube, and
    at the app's far camera (120 m, 18 deg vertical FOV over 1080 px, x1.6 render
    scale) that is a third of a pixel. At the authored 0.095 m base radius it is
    about 8 px — a legible line rather than an aliasing artefact. Style bible §9
    sanctions exactly this, and §2.15 of the plan asks for it aggressively.
    """
    for side in (1, -1):
        base, tip, ax = pole_endpoints(cfg, side)
        p["steel"].loft(_ring(base, ax, cfg["pole_r0"], cfg["pole_seg"]),
                        _ring(tip, ax, cfg["pole_r1"], cfg["pole_seg"]))


def pole_shoes(cfg, p):
    """A chunky wedge at each tip standing in for shoe + harp (plan §2.6).

    Deliberately NOT a `_Glow` surface: real shoes spark intermittently and a
    permanently lit one reads as a rendering bug, so the brief forbids it.
    Axis-aligned rather than swept along the pole — at 3-4 px it is a dark cap
    that terminates the rod, and a rotated box would cost triangles to say the
    same thing.
    """
    sx, sy, sz = cfg["shoe"]
    for side in (1, -1):
        _base, tip, _ax = pole_endpoints(cfg, side)
        p["ink"].box(tip, (sx, sy, sz), bevel=0.02, segments=1)


def rear_face_trolley(cfg, p):
    """The bus's `rear_face()` minus the engine louvre band.

    A trolley coach has no engine bay: its propulsion equipment is on the roof
    and there is nothing to vent through the back panel. Recognition cue 5 in
    the plan is literally "the absence of an exhaust or engine bay at the rear",
    so the louvre band is dropped and the red cant band runs clean across the
    tail. The rear window is kept — that is body, not powertrain.
    """
    L = cfg["length"] / 2.0
    p["glass"].span((-0.88, 0.88), (-L - 0.020, -L + 0.02), (1.62, 2.30))


# --------------------------------------------------------------------- build


def build(cfg, route_key="1-california"):
    route = ROUTES[route_key]

    def bank():
        return {short: Part(name) for short, name in bus.MATERIALS.items()}

    whole, sided = bank(), bank()

    # --- inherited body, unchanged -----------------------------------------
    body_shell(cfg, whole)
    skirt(cfg, whole)
    livery_band(cfg, whole, cfg["red_lo"], runs=lower_runs(cfg, proud=0.022))
    cant_band(cfg, whole)
    windshield(cfg, whole)
    destination_sign(cfg, whole, route)
    roof_pod(cfg, whole)
    bumpers(cfg, whole)
    front_fleet_number(cfg, whole, FLEET_NUMBER)
    front_worm(cfg, whole)
    worm(cfg, whole, (4.55, 11.10))
    fleet_number(cfg, whole, FLEET_NUMBER, (3.05,))

    # --- trolley-only -------------------------------------------------------
    rear_face_trolley(cfg, whole)
    pole_plinth(cfg, whole)
    pole_bases(cfg, whole)
    poles(cfg, whole)
    pole_shoes(cfg, whole)

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
    for bnk in (whole, sided):
        for part in bnk.values():
            if not part.faces:
                continue
            tgt = merged.setdefault(part.mat, Part(part.mat))
            base = len(tgt.verts)
            tgt.verts.extend(part.verts)
            tgt.faces.extend([tuple(base + i for i in f) for f in part.faces])
    objs = [p.emit() for p in merged.values()]
    return [o for o in objs if o]


def main():
    argv = sys.argv[sys.argv.index("--") + 1 :] if "--" in sys.argv else []
    out = HERE
    if "--out" in argv:
        out = argv[argv.index("--out") + 1]
    routes = [argv[argv.index("--route") + 1]] if "--route" in argv else ["1-california"]
    if "--all-routes" in argv:
        routes = list(ROUTES)
    cfg = dict(CFG)
    if "--pole-radius" in argv:
        # Reproduces the pole-thickness A/B in REPORT.md §5. Base radius; the tip
        # keeps the authored 0.65 taper ratio.
        r0 = float(argv[argv.index("--pole-radius") + 1])
        cfg.update(pole_r0=r0, pole_r1=round(r0 * 0.653, 4))
    os.makedirs(out, exist_ok=True)

    for key in routes:
        bpy.ops.wm.read_factory_settings(use_empty=True)
        build(cfg, key)
        report(f"build:{key}")
        name = CFG["slug"] if key == "1-california" else f"{CFG['slug']}-{key}"
        glb = os.path.join(out, f"{name}.glb")
        export_glb(glb)
        print(f"[build] wrote {glb}")
        if key == "1-california":
            blend = os.path.join(out, "muni-trolley.blend")
            bpy.ops.wm.save_as_mainfile(filepath=blend)
            print(f"[build] wrote {blend}")


if __name__ == "__main__":
    main()
