"""Compose the 501 Third Street review contact sheet from the rendered tiles.

    python3 make_contact_sheet.py [--dir DIR] [--prefix 501-third]

Plain Pillow rather than Blender's compositor: Blender 5.x replaced
`Scene.node_tree` with a compositing node group, and a 3x3 photo montage is not
worth a version-sensitive dependency.

The aerial from due north-east gets the hero slot: it is the only frame in which
the 3rd Street front, the rhombus footprint and the rooftop bulkhead read at
once.
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont

CELL = (700, 470)
COLS = 3
BG = (219, 205, 176)
INK = (58, 53, 48)
TILES = [
    ("aerial", "AERIAL 3/4 — the 3rd/Bryant corner, from due W, 40° down (hero)"),
    ("top", "TOP — rhombus roof, bulkhead, deck, mechanical"),
    ("night", "NIGHT — gallery front lit, Bryant tails off"),
    ("north", "NORTH elevation"),
    ("east", "EAST elevation"),
    ("south", "SOUTH elevation"),
    ("west", "WEST elevation"),
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
    ap.add_argument("--prefix", default="501-third")
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
