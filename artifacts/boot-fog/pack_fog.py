# Pack the Blender fog renders into the WebP plates the boot curtain ships.
#
#   python3 artifacts/boot-fog/pack_fog.py <renderDir> app/public/boot
#
# Expects karl-door-left.png, karl-door-right.png and karl-wisp.png in
# <renderDir> (see fog_render.py --mode door / --mode wisp).
#
# Two things that matter here:
#
#   * alpha_quality defaults to 100 — effectively lossless — and on a mostly
#     transparent plate that channel dominates the file. Fog edges are soft, so
#     dropping it into the 70s is invisible and saves a lot.
#   * the plates are rendered SQUARE on purpose. boot.css stretches them with
#     `background-size: 100% 100%` rather than cropping with `cover`, because
#     `cover` on a 16:9 plate blows up ~4x on a portrait phone: the billows crop
#     away to a flat grey wash and the torn seam lands off screen. Do not
#     "fix" the aspect here.

import sys
from pathlib import Path

from PIL import Image

PLATES = (
    ('karl-door-left', 80, 84),
    ('karl-door-right', 80, 84),
    ('karl-wisp', 72, 74),
)


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        raise SystemExit(2)
    src = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)

    total = 0
    for name, quality, alpha_quality in PLATES:
        source = src / f'{name}.png'
        if not source.exists():
            print(f'{name:22} MISSING ({source})')
            continue
        image = Image.open(source).convert('RGBA')
        if image.width != image.height:
            print(f'{name:22} WARNING: not square ({image.width}x{image.height}) — see note above')
        target = out / f'{name}.webp'
        image.save(target, 'WEBP', quality=quality, alpha_quality=alpha_quality, method=6)
        size = target.stat().st_size
        total += size
        print(f'{target.name:22} {size / 1024:7.1f} KB  {image.width}x{image.height}')

    print(f'{"TOTAL":22} {total / 1024:7.1f} KB')


main()
