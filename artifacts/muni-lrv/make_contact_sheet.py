"""Compose the muni-lrv review renders into one contact sheet.

    python3 make_contact_sheet.py [--out renders/muni-lrv-contact-sheet.png]

Pure standard library plus Pillow if present; falls back to a plain vertical
stack via Blender's image API when Pillow is not installed.
"""

import os
import sys

TILES = [
    ("muni-lrv-front.png", "FRONT (cab A) — the red horseshoe is the identity"),
    ("muni-lrv-rear.png", "REAR (cab B) — double-ended, so this is a second cab"),
    ("muni-lrv-left.png", "LEFT"),
    ("muni-lrv-right.png", "RIGHT"),
    ("muni-lrv-top.png", "TOP — roof equipment, pantograph, articulation step"),
    ("muni-lrv-aerial.png", "AERIAL 42° — the app's own camera angle"),
    ("muni-lrv-night.png", "NIGHT — the glow set ignited"),
    ("muni-lrv-in-city-1.6x.png", "IN CITY @ 1.6× — N Judah, real baked geometry"),
    ("muni-lrv-coupled-pair-1.6x.png", "COUPLED PAIR @ 1.6× — 74.4 m on a 94.5 m block"),
    ("muni-lrv-in-city-120m.png", "120 m — the far end of the vehicle camera band"),
]

WIDTH = 1800
PAD = 18
LABEL_H = 34
BG = (238, 234, 224)
INK = (58, 53, 48)


def main():
    argv = sys.argv[1:]
    here = os.path.dirname(os.path.abspath(__file__))
    renders = os.path.join(here, "renders")
    out = argv[argv.index("--out") + 1] if "--out" in argv else \
        os.path.join(renders, "muni-lrv-contact-sheet.png")

    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print("[sheet] Pillow not installed — run: python3 -m pip install Pillow")
        return 1

    try:
        font = ImageFont.truetype(
            "/System/Library/Fonts/Supplemental/Arial Bold.ttf", 19)
    except OSError:
        font = ImageFont.load_default()

    # Two columns: a ten-tile vertical strip is 10,000 px tall, which is both
    # unusable to review and a 12 MB blob in the repo.
    col_w = (WIDTH - 3 * PAD) // 2
    loaded = []
    for name, label in TILES:
        path = os.path.join(renders, name)
        if not os.path.exists(path):
            print(f"[sheet] missing {name} — skipped")
            continue
        img = Image.open(path).convert("RGB")
        img = img.resize((col_w, max(1, int(img.height * col_w / img.width))),
                         Image.LANCZOS)
        loaded.append((img, label))

    if not loaded:
        print("[sheet] nothing to compose")
        return 1

    # Fill columns by running height so the two stay roughly level.
    cols = [[], []]
    heights = [PAD, PAD]
    for img, label in loaded:
        i = 0 if heights[0] <= heights[1] else 1
        cols[i].append((img, label))
        heights[i] += img.height + LABEL_H + PAD

    sheet = Image.new("RGB", (WIDTH, max(heights)), BG)
    draw = ImageDraw.Draw(sheet)
    for i, col in enumerate(cols):
        x = PAD + i * (col_w + PAD)
        y = PAD
        for img, label in col:
            draw.text((x, y + 6), label, fill=INK, font=font)
            y += LABEL_H
            sheet.paste(img, (x, y))
            y += img.height + PAD

    sheet.save(out, optimize=True)
    print(f"[sheet] wrote {out} ({sheet.width}x{sheet.height}, {len(loaded)} tiles)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
