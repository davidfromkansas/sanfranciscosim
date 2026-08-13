"""Compose the review renders into 542-presidio-blvd-contact-sheet.png.

Row 1 is the four shared-rig elevations; row 2 is the roof, the app-camera
aerial and the night state. The night tile is not optional for this asset -
the pipeline requires the glow design to be reviewable alongside the day one.
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PREFIX = "542-presidio-blvd"
BG = (237, 227, 209)
INK = (58, 52, 44)
VIEWS = ["north", "east", "south", "west", "top", "aerial", "night"]
COLS = 4
PAD = 40
LABEL_H = 56
CELL_W = 460

FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
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
    img = Image.open(HERE / f"{PREFIX}-{view}.png").convert("RGB")
    h = round(img.height * CELL_W / img.width)
    return img.resize((CELL_W, h), Image.LANCZOS)


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

    out = HERE / f"{PREFIX}-contact-sheet.png"
    sheet.save(out)
    print(f"[contact-sheet] {out}")


if __name__ == "__main__":
    main()
