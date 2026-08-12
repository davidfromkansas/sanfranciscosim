"""Compose the review renders into muni-trolley-contact-sheet.png.

    python3 make_contact_sheet.py [--out DIR]

Pure PIL, no Blender. Labels every tile so the sheet is readable on its own in a
PR, and puts the two decision frames — the top view and the side-by-side against
the hybrid bus — at the top, because those are the two that answer the plan's
open questions.
"""

import os
import sys

from PIL import Image, ImageDraw, ImageFont

SLUG = "muni-trolley-40"
TILES = [
    ("top", "TOP — two poles, 0.60 m apart, trailing aft. THE decision view"),
    ("vs-hybrid-bus-150m-app-min", "vs HYBRID BUS @ 150 m — DIORAMA.min, the closest a player gets"),
    ("vs-hybrid-bus-120m", "vs HYBRID BUS @ 120 m — the README's far vehicle distance"),
    ("in-city-1.6x", "IN CITY @ 1.6× — real baked Nob Hill geometry, app camera"),
    ("front", "FRONT"),
    ("rear", "REAR"),
    ("left", "LEFT"),
    ("right", "RIGHT"),
    ("aerial", "AERIAL — 42° down, 100 mm"),
    ("night", "NIGHT — glow set ignited, no glow at the shoe"),
]
COLS = 2
PAD = 18
LABEL_H = 34
BG = (246, 244, 238)
INK = (58, 53, 48)


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
    argv = sys.argv[1:]
    here = os.path.dirname(os.path.abspath(__file__))
    out = argv[argv.index("--out") + 1] if "--out" in argv else os.path.join(here, "renders")

    loaded = []
    for key, label in TILES:
        path = os.path.join(out, f"{SLUG}-{key}.png")
        if os.path.exists(path):
            loaded.append((Image.open(path).convert("RGB"), label))
        else:
            print(f"[sheet] missing, skipped: {path}")
    if not loaded:
        raise SystemExit("no renders found")

    cell_w = 860
    cells = []
    for im, label in loaded:
        scale = cell_w / im.width
        cells.append((im.resize((cell_w, max(1, int(im.height * scale))), Image.LANCZOS), label))

    rows = (len(cells) + COLS - 1) // COLS
    row_h = [
        max(c[0].height for c in cells[r * COLS : (r + 1) * COLS]) + LABEL_H
        for r in range(rows)
    ]
    title_h = 62
    W = COLS * cell_w + (COLS + 1) * PAD
    H = sum(row_h) + (rows + 1) * PAD + title_h

    sheet = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(sheet)
    d.text((PAD, 16),
           "muni-trolley-40  ·  New Flyer Xcelsior XT40  ·  1 CALIFORNIA  ·  fleet 5743",
           fill=INK, font=font(30))
    d.text((PAD, 46),
           "elevations share ortho scale, framing, light rig and exposure; "
           "in-city frames use the app's own 42° / 18° fov diorama camera",
           fill=(120, 112, 104), font=font(17))

    y = title_h + PAD
    for r in range(rows):
        x = PAD
        for im, label in cells[r * COLS : (r + 1) * COLS]:
            d.text((x, y), label, fill=INK, font=font(21))
            sheet.paste(im, (x, y + LABEL_H))
            x += cell_w + PAD
        y += row_h[r] + PAD

    path = os.path.join(out, "muni-trolley-contact-sheet.png")
    sheet.save(path)
    print(f"[sheet] wrote {path}  ({W}x{H})")


if __name__ == "__main__":
    main()
