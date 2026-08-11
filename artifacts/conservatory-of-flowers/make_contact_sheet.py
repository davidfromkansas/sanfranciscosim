"""Compose the six review renders into conservatory-of-flowers-contact-sheet.png."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BG = (237, 227, 209)
INK = (58, 52, 44)
FONT_CANDIDATES = [
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
    "/System/Library/Fonts/Supplemental/Arial Bold.ttf",
    "/System/Library/Fonts/Helvetica.ttc",
]
for path in FONT_CANDIDATES:
    try:
        FONT = ImageFont.truetype(path, 34)
        break
    except OSError:
        continue
else:
    FONT = ImageFont.load_default()
VIEWS = ["north", "east", "south", "west", "top", "aerial", "night"]
COLS = 2
PAD = 40
LABEL_H = 56
CELL_W = 760


def load(view):
    img = Image.open(HERE / f"conservatory-of-flowers-{view}.png").convert("RGB")
    w = CELL_W
    h = round(img.height * w / img.width)
    return img.resize((w, h), Image.LANCZOS)


def main():
    tiles = [load(v) for v in VIEWS]
    rows = [tiles[i : i + COLS] for i in range(0, len(tiles), COLS)]
    row_h = [LABEL_H + max(t.height for t in r) for r in rows]
    width = PAD + COLS * (CELL_W + PAD)
    height = PAD + sum(h + PAD for h in row_h)
    sheet = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(sheet)
    y = PAD
    k = 0
    for r, row in enumerate(rows):
        for c, tile in enumerate(row):
            x = PAD + c * (CELL_W + PAD)
            draw.text((x, y), VIEWS[k].upper(), fill=INK, font=FONT)
            sheet.paste(tile, (x, y + LABEL_H))
            k += 1
        y += row_h[r] + PAD
    out = HERE / "conservatory-of-flowers-contact-sheet.png"
    sheet.save(out)
    print(f"[sheet] {out}")


if __name__ == "__main__":
    main()
