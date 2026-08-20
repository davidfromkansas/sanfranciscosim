"""Compose the review renders into pier-17-contact-sheet.png."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
BG = (237, 227, 209)
INK = (58, 52, 44)
VIEWS = ["north", "east", "south", "west", "top", "aerial", "aerial-night"]
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
    img = Image.open(HERE / f"pier-17-{view}.png").convert("RGB")
    w = CELL_W
    h = round(img.height * w / img.width)
    return img.resize((w, h), Image.LANCZOS)


def main():
    font = load_font()
    imgs = {v: load(v) for v in VIEWS}
    rows = (len(VIEWS) + COLS - 1) // COLS
    cell_h = max(i.height for i in imgs.values()) + LABEL_H
    sheet = Image.new(
        "RGB",
        (COLS * CELL_W + (COLS + 1) * PAD, rows * cell_h + (rows + 1) * PAD + 70),
        BG,
    )
    d = ImageDraw.Draw(sheet)
    d.text((PAD, PAD - 10), "Pier 17 — review contact sheet", fill=INK,
           font=load_font(44))
    y0 = PAD + 60
    for i, v in enumerate(VIEWS):
        r, c = divmod(i, COLS)
        x = PAD + c * (CELL_W + PAD)
        y = y0 + r * (cell_h + PAD)
        img = imgs[v]
        sheet.paste(img, (x, y))
        d.text((x, y + img.height + 8), v, fill=INK, font=font)
    out = HERE / "pier-17-contact-sheet.png"
    sheet.save(out)
    print(f"[sheet] {out}")


if __name__ == "__main__":
    main()
