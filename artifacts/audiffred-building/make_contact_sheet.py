"""Compose the review renders into audiffred-building-contact-sheet.png."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BG = (237, 227, 209)
INK = (58, 52, 44)
# The hero first: Mission Street is the address, the long side and the only
# elevation with thirteen bays. "south" is the blind party wall, included
# because proving it is blind is part of the contract. The compass names are the
# nearest name for each building-aligned face - see render_audiffred_building.py.
# "facade" is the square-on long-lens view of the 315.2 deg Mission elevation,
# the only frame that takes it head-on.
VIEWS = ["facade", "aerial", "top", "north", "east", "west",
         "aerial-night", "south"]
COLS = 3
PAD = 40
LABEL_H = 56
CELL_W = 460

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
    img = Image.open(HERE / f"audiffred-building-{view}.png").convert("RGB")
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

    out = HERE / "audiffred-building-contact-sheet.png"
    sheet.save(out)
    print(f"[contact-sheet] {out}")


if __name__ == "__main__":
    main()
