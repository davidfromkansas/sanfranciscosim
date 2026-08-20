"""Compose the One Market Plaza towers review contact sheet from the rendered tiles.

    python3 make_contact_sheet.py [--dir DIR] [--prefix one-market-plaza-towers]

Plain Pillow rather than Blender's compositor: Blender 5.x replaced
`Scene.node_tree` with a compositing node group, and a 3x3 photo montage is not
worth a version-sensitive dependency.

The aerial three-quarter on the Market x Steuart corner is the hero; the top
view is the one that proves the U, the courtyard and the atrium roof.
"""

import argparse
import os

from PIL import Image, ImageDraw, ImageFont

CELL = (700, 470)
COLS = 3
BG = (219, 205, 176)
INK = (58, 53, 48)
TILES = [
    ("aerial", "AERIAL — Mission St, 26 deg: the 172/111 m height contrast"),
    ("top", "TOP — two canted shafts, the plaza, the garden, the canopies"),
    ("night", "NIGHT — scattered lit slots, retail band, lit canopies"),
    ("east", "MISSION STREET (SE 135.2 deg) — the public front"),
    ("north", "STEUART ST / DON CHEE WAY (NE 45.2 deg)"),
    ("south", "SOUTH-WEST flank (225.2 deg)"),
    ("west", "NORTH-WEST (315.2 deg) — the Southern Pacific Building boundary"),
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
    ap.add_argument("--prefix", default="one-market-plaza-towers")
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
