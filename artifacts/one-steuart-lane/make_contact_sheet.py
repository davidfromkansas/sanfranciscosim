"""Compose the One Steuart Lane review contact sheet from the rendered tiles.

    python3 make_contact_sheet.py [--dir DIR] [--prefix one-steuart-lane]

Plain Pillow rather than Blender's compositor: Blender 5.x replaced
`Scene.node_tree` with a compositing node group, and a 3x3 photo montage is not
worth a version-sensitive dependency.

The aerial three-quarter down the east corner is the hero, because for this asset
the alternating stack is the subject and it only reads on a corner.
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont

CELL = (620, 640)
COLS = 4
BG = (219, 205, 176)
INK = (58, 53, 48)
TILES = [
    ("aerial", "AERIAL 3/4 — east corner, 40 deg down: the stack"),
    ("top", "TOP — roof: PV field, cooling towers, penthouse crest, BMU"),
    ("aerial-night", "NIGHT — under-slab bands + lobby + scattered units"),
    ("north", "STEUART LANE elevation (NE 44.2) — entrance, Bay side"),
    ("east", "SOUTH-EAST flank (134.8) — block interior"),
    ("south", "SOUTH-WEST flank (224.5) — block interior"),
    ("west", "HOWARD STREET elevation (NW 314.9) — deep terrace bay"),
]


def font(size):
    for path in (
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=here)
    ap.add_argument("--prefix", default="one-steuart-lane")
    args = ap.parse_args()

    present = [
        (name, label)
        for name, label in TILES
        if os.path.exists(os.path.join(args.dir, f"{args.prefix}-{name}.png"))
    ]
    rows = (len(present) + COLS - 1) // COLS
    sheet = Image.new("RGB", (CELL[0] * COLS, CELL[1] * rows), BG)
    draw = ImageDraw.Draw(sheet)
    fnt = font(19)

    for i, (name, label) in enumerate(present):
        img = Image.open(os.path.join(args.dir, f"{args.prefix}-{name}.png")).convert("RGB")
        img.thumbnail((CELL[0] - 16, CELL[1] - 46), Image.LANCZOS)
        col, row = i % COLS, i // COLS
        ox = col * CELL[0] + (CELL[0] - img.width) // 2
        oy = row * CELL[1] + 34 + (CELL[1] - 46 - img.height) // 2
        sheet.paste(img, (ox, oy))
        draw.text((col * CELL[0] + 14, row * CELL[1] + 10), label, font=fnt, fill=INK)

    out = os.path.join(args.dir, f"{args.prefix}-contact-sheet.png")
    sheet.save(out)
    print(f"[sheet] {out} ({len(present)} tiles)")


if __name__ == "__main__":
    main()
