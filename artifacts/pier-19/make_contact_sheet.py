"""Compose the review renders into pier-19-contact-sheet.png."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BG = (237, 227, 209)
INK = (58, 52, 44)
# The two hero elevations first: the South Park front and the Jack London Alley
# flank are both fully exposed and both are judged. The compass names are the
# nearest name for each building-aligned face — see render_49_south_park.py.
# "facade" is the square-on long-lens view of the 315.8 deg park front, the only
# frame that takes it head-on.
# The frontispiece first: it is 24 m of a 234 m asset and the shared-rig
# elevations cannot show it at a readable size. Then the roof (which is what the
# app's camera actually sees), then both aerials, then the two flanks and the
# two end elevations.
VIEWS = ["facade", "top", "aerial", "aerial-ne", "aerial-night",
         "north", "south", "west", "east"]
COLS = 1
PAD = 40
LABEL_H = 56
CELL_W = 1500

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/SFNSDisplay.ttf",
    "/Library/Fonts/Arial Bold.ttf",
]


def load_font(size=34):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            try:
                return ImageFont.truetype(path, size)
            except OSError:
                continue
    return ImageFont.load_default()


def load(view):
    img = Image.open(HERE / f"pier-19-{view}.png").convert("RGB")
    w = CELL_W
    h = round(img.height * w / img.width)
    return img.resize((w, h), Image.LANCZOS)


def main():
    font = load_font()
    tiles = [load(v) for v in VIEWS]
    rows = [tiles[i : i + COLS] for i in range(0, len(tiles), COLS)]
    row_h = [LABEL_H + max(t.height for t in r) for r in rows]
    width = PAD + COLS * (CELL_W + PAD)
    height = PAD + sum(h + PAD for h in row_h)
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)

    y = PAD
    for ri, row in enumerate(rows):
        for ci, tile in enumerate(row):
            cx = PAD + ci * (CELL_W + PAD) + CELL_W // 2
            label = VIEWS[ri * COLS + ci].upper()
            draw.text((cx, y + LABEL_H // 2), label, font=font, fill=INK, anchor="mm")
            sheet.paste(tile, (cx - tile.width // 2, y + LABEL_H))
        y += row_h[ri] + PAD

    out = HERE / "pier-19-contact-sheet.png"
    sheet.save(out)
    print(f"[contact-sheet] {out}")


if __name__ == "__main__":
    main()
