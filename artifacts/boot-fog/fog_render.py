# Karl — volumetric fog plates for the app's boot curtain.
#
# Run headless (does not touch an open Blender session):
#   /Applications/Blender.app/Contents/MacOS/Blender --background \
#     --python artifacts/boot-fog/fog_render.py -- --mode still --out /tmp/fog
#
# Modes:
#   still   3 fog-bank plates (the safe tier: swapped in for the SVG tiles)
#   loop    N frames of rolling fog, cross-faded into a seamless loop
#   burn    N frames of the bank clearing, for the reveal
#
# Everything renders RGBA over a transparent film, so alpha IS fog density and
# the plates composite straight onto the curtain's own sky gradient — the
# existing parallax/drift/mask CSS keeps working unchanged.

import argparse
import math
import sys

import bpy

# ----------------------------------------------------------------------- args

argv = sys.argv[sys.argv.index('--') + 1:] if '--' in sys.argv else []
parser = argparse.ArgumentParser()
parser.add_argument('--mode', default='still', choices=['still', 'loop', 'burn', 'door', 'wisp'])
# Which half of the parting curtain to render. The fog is torn away past the
# seam by the volume itself, so the inner edge is real wisps, not a CSS cut.
parser.add_argument('--door', default='left', choices=['left', 'right'])
# Door plates fill the frame instead of sitting as a low bank with sky above.
parser.add_argument('--fill', action='store_true')
parser.add_argument('--out', required=True, help='output directory')
parser.add_argument('--width', type=int, default=1024)
parser.add_argument('--height', type=int, default=576)
parser.add_argument('--samples', type=int, default=96)
parser.add_argument('--frames', type=int, default=32)
parser.add_argument('--density', type=float, default=6.0)
parser.add_argument('--camy', type=float, default=-17.0)
parser.add_argument('--camz', type=float, default=2.4)
parser.add_argument('--campitch', type=float, default=85.0)
# Lower = the noise displaces the crown further, i.e. puffier cumulus tops.
parser.add_argument('--puff', type=float, default=0.6)
args = parser.parse_args(argv)


def clean():
    """Start from an empty file — the script owns the whole scene."""
    bpy.ops.wm.read_factory_settings(use_empty=True)


def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'
    scene.cycles.samples = args.samples
    scene.cycles.use_denoising = True
    # Volumes are the whole subject: give the integrator room to resolve them
    # but keep bounces low, since fog against nothing needs no global light.
    scene.cycles.max_bounces = 8
    scene.cycles.volume_bounces = 12
    scene.cycles.volume_step_rate = 0.5
    scene.cycles.volume_max_steps = 2048
    scene.cycles.transparent_max_bounces = 16

    scene.render.resolution_x = args.width
    scene.render.resolution_y = args.height
    scene.render.resolution_percentage = 100
    # Alpha carries fog density; the curtain supplies its own sky behind it.
    scene.render.film_transparent = True
    scene.render.image_settings.file_format = 'PNG'
    scene.render.image_settings.color_mode = 'RGBA'
    scene.render.image_settings.color_depth = '8'
    scene.view_settings.view_transform = 'Standard'

    # Metal on this Mac if it is available, else CPU.
    try:
        prefs = bpy.context.preferences.addons['cycles'].preferences
        prefs.compute_device_type = 'METAL'
        prefs.get_devices()
        enabled = 0
        for device in prefs.devices:
            device.use = device.type in {'METAL', 'CPU'}
            enabled += 1 if device.use else 0
        scene.cycles.device = 'GPU'
        print(f'[fog] Metal enabled on {enabled} devices')
    except Exception as err:  # noqa: BLE001 - any failure just means CPU
        scene.cycles.device = 'CPU'
        print(f'[fog] falling back to CPU ({err})')


def build_fog(name='KarlDomain'):
    """A wide slab of scattering volume with billow structure in its density."""
    bpy.ops.mesh.primitive_cube_add(size=2, location=(0, 0, 0))
    domain = bpy.context.active_object
    domain.name = name
    if args.mode == 'wisp':
        domain.scale = (11.0, 1.6, 4.2)
        domain.location = (0.0, -6.0, 1.2)
    elif args.fill:
        domain.scale = (9.0, 3.6, 5.2)
        domain.location = (0.0, 0.0, 1.4)
    else:
        domain.scale = (15.0, 3.2, 2.4)
        domain.location = (0.0, 0.0, -0.5)

    material = bpy.data.materials.new('Karl')
    material.use_nodes = True
    tree = material.node_tree
    tree.nodes.clear()

    out = tree.nodes.new('ShaderNodeOutputMaterial')
    out.location = (900, 0)

    volume = tree.nodes.new('ShaderNodeVolumePrincipled')
    volume.location = (620, 0)
    volume.inputs['Color'].default_value = (0.92, 0.95, 1.0, 1.0)
    # Strong forward scattering: light keeps going the way it was travelling,
    # which is why real fog blooms around a light source.
    volume.inputs['Anisotropy'].default_value = 0.42
    volume.inputs['Emission Strength'].default_value = 0.0

    coord = tree.nodes.new('ShaderNodeTexCoord')
    coord.location = (-600, 0)

    mapping = tree.nodes.new('ShaderNodeMapping')
    mapping.name = 'Drift'
    mapping.location = (-400, 0)

    # Two noise scales multiplied: big masses, then bitten into by finer
    # detail. One noise alone reads as mist however it is shaped.
    coarse = tree.nodes.new('ShaderNodeTexNoise')
    coarse.name = 'Coarse'
    coarse.location = (-200, 140)
    coarse.inputs['Scale'].default_value = 2.1 if args.mode == 'wisp' else 0.85
    coarse.inputs['Detail'].default_value = 12.0
    coarse.inputs['Roughness'].default_value = 0.7

    fine = tree.nodes.new('ShaderNodeTexNoise')
    fine.name = 'Fine'
    fine.location = (-200, -160)
    fine.inputs['Scale'].default_value = 3.4
    fine.inputs['Detail'].default_value = 9.0
    fine.inputs['Roughness'].default_value = 0.55

    # Blend rather than multiply: multiplying two noises crushes the contrast
    # into mush, which is what made the first pass a grey wall.
    mix = tree.nodes.new('ShaderNodeMix')
    mix.data_type = 'FLOAT'
    mix.blend_type = 'MIX'
    mix.location = (40, 0)
    mix.inputs['Factor'].default_value = 0.28

    # The height gradient is SUBTRACTED from the noise before the threshold,
    # not multiplied after it. That is the whole trick: the surface where
    # (noise - height) crosses the threshold is displaced by the noise, so the
    # bank gets a lumpy cauliflower crown instead of a flat ceiling.
    sep = tree.nodes.new('ShaderNodeSeparateXYZ')
    sep.location = (-200, -420)
    gradient = tree.nodes.new('ShaderNodeMapRange')
    gradient.location = (40, -420)
    gradient.inputs['From Min'].default_value = -1.0
    gradient.inputs['From Max'].default_value = 2.4 if args.fill else 0.9
    gradient.inputs['To Min'].default_value = 0.0
    gradient.inputs['To Max'].default_value = args.puff
    gradient.clamp = False

    carve = tree.nodes.new('ShaderNodeMath')
    carve.operation = 'SUBTRACT'
    carve.location = (240, -200)

    # Seam falloff. Subtracting a horizontal ramp from the same noise field
    # tears the inner edge exactly the way the vertical ramp tears the crown —
    # so a door's edge is wisps and holes, never a straight cut.
    seam = tree.nodes.new('ShaderNodeMapRange')
    seam.name = 'Seam'
    seam.location = (40, -640)
    seam.clamp = False
    seam_cut = tree.nodes.new('ShaderNodeMath')
    seam_cut.operation = 'SUBTRACT'
    seam_cut.location = (330, -420)
    if args.mode == 'door':
        # Full density out at the far edge, gone a little past centre so the
        # two halves overlap and leave no gap when closed.
        # Object space is ±1 across the domain, but the camera only sees about
        # ±0.64 of it, so the tear has to be placed inside that window or it
        # falls off the edge of frame. Fog runs solid to just past centre, then
        # tears out by ~70% across — the two halves overlap when closed.
        near, far = (-0.22, 0.46) if args.door == 'left' else (0.22, -0.46)
        seam.clamp = True
        seam.inputs['From Min'].default_value = near
        seam.inputs['From Max'].default_value = far
        seam.inputs['To Min'].default_value = 0.0
        seam.inputs['To Max'].default_value = 0.5
    else:
        seam.inputs['To Min'].default_value = 0.0
        seam.inputs['To Max'].default_value = 0.0

    ramp = tree.nodes.new('ShaderNodeValToRGB')
    ramp.location = (420, 0)
    ramp.color_ramp.interpolation = 'B_SPLINE'
    ramp.color_ramp.elements[0].position = 0.04
    ramp.color_ramp.elements[0].color = (0, 0, 0, 1)
    ramp.color_ramp.elements[1].position = 0.32
    ramp.color_ramp.elements[1].color = (1, 1, 1, 1)

    density = tree.nodes.new('ShaderNodeMath')
    density.name = 'Density'
    density.operation = 'MULTIPLY'
    density.location = (660, 60)
    density.inputs[1].default_value = args.density

    links = tree.links
    links.new(coord.outputs['Object'], mapping.inputs['Vector'])
    links.new(mapping.outputs['Vector'], coarse.inputs['Vector'])
    links.new(mapping.outputs['Vector'], fine.inputs['Vector'])
    links.new(coarse.outputs['Fac'], mix.inputs['A'])
    links.new(fine.outputs['Fac'], mix.inputs['B'])
    links.new(coord.outputs['Object'], sep.inputs['Vector'])
    links.new(sep.outputs['Z'], gradient.inputs['Value'])
    links.new(mix.outputs['Result'], carve.inputs[0])
    links.new(gradient.outputs['Result'], carve.inputs[1])
    links.new(sep.outputs['X'], seam.inputs['Value'])
    links.new(carve.outputs['Value'], seam_cut.inputs[0])
    links.new(seam.outputs['Result'], seam_cut.inputs[1])
    links.new(seam_cut.outputs['Value'], ramp.inputs['Fac'])
    links.new(ramp.outputs['Color'], density.inputs[0])
    links.new(density.outputs['Value'], volume.inputs['Density'])
    links.new(volume.outputs['Volume'], out.inputs['Volume'])

    domain.data.materials.append(material)
    return domain, mapping, density


def build_lights():
    """Top-lit, the way a marine layer reads at golden hour: a strong key from
    above and behind so the billow crowns blow out and the troughs stay cool."""
    key = bpy.data.lights.new('Key', type='SUN')
    key.energy = 7.0
    key.color = (1.0, 0.96, 0.9)
    key.angle = math.radians(6)
    key_obj = bpy.data.objects.new('Key', key)
    key_obj.rotation_euler = (math.radians(52), 0, math.radians(28))
    bpy.context.collection.objects.link(key_obj)

    fill = bpy.data.lights.new('Fill', type='SUN')
    fill.energy = 1.8
    fill.color = (0.66, 0.78, 0.95)
    fill_obj = bpy.data.objects.new('Fill', fill)
    fill_obj.rotation_euler = (math.radians(112), 0, math.radians(-140))
    bpy.context.collection.objects.link(fill_obj)

    # Warm rim raking through from behind: this is what gives real fog its
    # glow-from-within instead of looking like flat grey cotton.
    rim = bpy.data.lights.new('Rim', type='SUN')
    rim.energy = 1.5
    rim.color = (1.0, 0.88, 0.72)
    rim.angle = math.radians(3)
    rim_obj = bpy.data.objects.new('Rim', rim)
    rim_obj.rotation_euler = (math.radians(74), 0, math.radians(186))
    bpy.context.collection.objects.link(rim_obj)


def build_camera():
    cam = bpy.data.cameras.new('Cam')
    cam.lens = 42
    cam_obj = bpy.data.objects.new('Cam', cam)
    # Outside the bank, a little above it, so the crown reads against sky.
    cam_obj.location = (0, args.camy, args.camz)
    cam_obj.rotation_euler = (math.radians(args.campitch), 0, 0)
    bpy.context.collection.objects.link(cam_obj)
    bpy.context.scene.camera = cam_obj
    return cam_obj


def render_to(path):
    bpy.context.scene.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print(f'[fog] wrote {path}')


def main():
    clean()
    setup_render()
    domain, mapping, density = build_fog()
    build_lights()
    build_camera()

    out = args.out.rstrip('/')

    if args.mode == 'door':
        render_to(f'{out}/karl-door-{args.door}')
        return

    if args.mode == 'wisp':
        render_to(f'{out}/karl-wisp')
        return

    if args.mode == 'still':
        # Three plates from different slices of the noise field: same bank,
        # different weather. These are the drop-in replacements for the SVG.
        for index, offset in enumerate(((0, 0, 0), (37.4, 11.2, 5.5), (81.9, -24.6, -3.1)), start=1):
            mapping.inputs['Location'].default_value = offset
            render_to(f'{out}/karl-plate-{index}')
        return

    scene = bpy.context.scene
    scene.frame_start = 1
    scene.frame_end = args.frames

    if args.mode == 'loop':
        # Drift the noise field steadily; the seam is removed in post by
        # cross-fading the tail over the head (Perlin does not tile in time).
        span = 6.0
        for frame in range(1, args.frames + 1):
            t = (frame - 1) / args.frames
            mapping.inputs['Location'].default_value = (t * span, t * span * 0.22, 0)
            render_to(f'{out}/loop-{frame:03d}')
        return

    if args.mode == 'burn':
        # The bank clearing: density falls away while the field keeps drifting,
        # so it dissolves rather than simply fading out.
        for frame in range(1, args.frames + 1):
            t = (frame - 1) / max(1, args.frames - 1)
            mapping.inputs['Location'].default_value = (t * 3.2, t * 0.9, t * 1.6)
            density.inputs[1].default_value = args.density * (1.0 - t) ** 1.6
            render_to(f'{out}/burn-{frame:03d}')
        return


main()
