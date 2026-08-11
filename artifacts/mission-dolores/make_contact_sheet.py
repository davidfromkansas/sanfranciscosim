"""Assemble the Mission Dolores review renders into one contact sheet.

    python3 make_contact_sheet.py [--dir DIR] [--prefix mission-dolores]

Pure Pillow; run after render_mission_dolores.py. Every tile is a crop-free
letterboxed copy of the render it labels, so the sheet cannot show anything the
individual images do not.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

TILES = [
    ("aerial", "AERIAL - high three-quarter (app camera)"),
    ("top", "TOP - roofs, dome, tower caps"),
    ("east", "EAST - Dolores Street front"),
    ("north", "NORTH - 16th Street flank"),
    ("west", "WEST - apse and parish wing"),
    ("south", "SOUTH - adobe flank"),
    ("night", "NIGHT - app dusk state"),
    ("night-front", "NIGHT - street front"),
]

CELL = (760, 560)
PAD = 16
LABEL_H = 30
COLS = 2
BG = (226, 219, 205)
INK = (58, 53, 48)


def font(size):
    for path in (
        "/System/Library/Fonts/SFNSMono.ttf",
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ):
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                pass
    return ImageFont.load_default()


def main():
    argv = sys.argv[1:]

    def arg(flag, default):
        return argv[argv.index(flag) + 1] if flag in argv else default

    here = os.path.dirname(os.path.abspath(__file__))
    directory = arg("--dir", here)
    prefix = arg("--prefix", "mission-dolores")

    tiles = [t for t in TILES if os.path.exists(os.path.join(directory, f"{prefix}-{t[0]}.png"))]
    rows = (len(tiles) + COLS - 1) // COLS
    W = COLS * CELL[0] + (COLS + 1) * PAD
    H = rows * (CELL[1] + LABEL_H) + (rows + 1) * PAD
    sheet = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(sheet)
    f = font(20)

    for i, (name, label) in enumerate(tiles):
        col, row = i % COLS, i // COLS
        x = PAD + col * (CELL[0] + PAD)
        y = PAD + row * (CELL[1] + LABEL_H + PAD)
        img = Image.open(os.path.join(directory, f"{prefix}-{name}.png")).convert("RGB")
        img.thumbnail(CELL, Image.LANCZOS)
        cell = Image.new("RGB", CELL, BG)
        cell.paste(img, ((CELL[0] - img.width) // 2, (CELL[1] - img.height) // 2))
        sheet.paste(cell, (x, y))
        draw.text((x + 4, y + CELL[1] + 6), label, font=f, fill=INK)

    out = os.path.join(directory, f"{prefix}-contact-sheet.png")
    sheet.save(out)
    print(f"[sheet] wrote {out} ({len(tiles)} tiles)")


if __name__ == "__main__":
    main()
