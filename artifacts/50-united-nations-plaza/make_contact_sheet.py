"""Compose the seven review renders into 50-united-nations-plaza-contact-sheet.png."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BG = (237, 227, 209)
INK = (58, 52, 44)
FONT_CANDIDATES = [
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
VIEWS = ["north", "east", "south", "west", "top", "aerial", "night"]
COLS = 2
PAD = 40
LABEL_H = 56
CELL_W = 640


def font():
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, 34)
    return ImageFont.load_default(size=34)


def load(view):
    img = Image.open(HERE / f"50-united-nations-plaza-{view}.png").convert("RGB")
    w = CELL_W
    h = round(img.height * w / img.width)
    return img.resize((w, h), Image.LANCZOS)


def main():
    fnt = font()
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
            draw.text((cx, y + LABEL_H // 2), label, font=fnt, fill=INK, anchor="mm")
            sheet.paste(tile, (cx - tile.width // 2, y + LABEL_H))
        y += row_h[ri] + PAD

    out = HERE / "50-united-nations-plaza-contact-sheet.png"
    sheet.save(out)
    print(f"[contact-sheet] {out}")


if __name__ == "__main__":
    main()
